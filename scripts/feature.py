#!/usr/bin/env python3
"""Feature board CLI - the sanctioned way to change feature_list.json.

Why a CLI instead of hand-editing JSON?  Because the board is a state machine:
  planned -> in_progress -> done   (plus blocked)
Some transitions must be earned (a sensor must really pass, a gate must be recorded,
a human must confirm). The CLI refuses transitions that were not earned.
"""
import argparse
import datetime
import json
import re
import sys

from harness_config import ROOT, load_env, platforms as env_platforms

BOARD = ROOT / "feature_list.json"
STATUSES = ("planned", "in_progress", "blocked", "done")
PLATFORM_STATES = ("pending", "in_progress", "sensor_green", "done")
MANUAL_PLATFORM_STATES = ("pending", "in_progress")  # sensor_green is written only by sensors
ID_RE = re.compile(r"^[a-z0-9]+(-[a-z0-9]+)*$")
SCENARIO_RE = re.compile(r"^\s*(Scenario|Scenario Outline|Example):", re.M)
FEATURE_RE = re.compile(r"^\s*Feature:", re.M)
TEMPLATE_MARK = "@template-placeholder"


def now():
    return datetime.datetime.now(datetime.timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")


def die(message, code=1):
    print(f"ERROR: {message}", file=sys.stderr)
    sys.exit(code)


def load():
    if not BOARD.is_file():
        die("feature_list.json not found. Run: sh init.sh")
    try:
        return json.loads(BOARD.read_text(encoding="utf-8"))
    except json.JSONDecodeError as exc:
        die(f"feature_list.json is not valid JSON: {exc}")


def save(data):
    BOARD.write_text(json.dumps(data, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")


def find(data, feature_id):
    for feat in data.get("features", []):
        if feat.get("id") == feature_id:
            return feat
    die(f"feature '{feature_id}' not found in feature_list.json")


def active(data):
    return [f for f in data.get("features", []) if f.get("status") == "in_progress"]


def spec_errors(spec_rel):
    errors = []
    path = ROOT / spec_rel
    if not path.is_file():
        return [f"spec file not found: {spec_rel}"]
    text = path.read_text(encoding="utf-8")
    if not FEATURE_RE.search(text):
        errors.append(f"{spec_rel}: no 'Feature:' line")
    if not SCENARIO_RE.search(text):
        errors.append(f"{spec_rel}: no 'Scenario:' found")
    if TEMPLATE_MARK in text:
        errors.append(f"{spec_rel}: still contains '{TEMPLATE_MARK}' (copied from template, not completed)")
    return errors


def validate(data=None):
    """Return a list of invariant violations of the board."""
    data = data if data is not None else load()
    errors = []
    allowed = env_platforms(load_env())
    if data.get("schema_version") != 2:
        errors.append("feature_list.json: schema_version must be 2 (see CHANGELOG for migration)")
    features = data.get("features")
    if not isinstance(features, list):
        return errors + ["feature_list.json: 'features' must be a list"]
    seen, in_progress = set(), 0
    for idx, feat in enumerate(features):
        where = f"features[{idx}]"
        if not isinstance(feat, dict):
            errors.append(f"{where}: must be an object")
            continue
        fid = feat.get("id", "")
        where = f"feature '{fid or idx}'"
        for key in ("id", "title", "spec", "status", "platforms", "verified"):
            if key not in feat:
                errors.append(f"{where}: missing '{key}'")
        if fid and not ID_RE.match(fid):
            errors.append(f"{where}: id must be kebab-case")
        if fid in seen:
            errors.append(f"{where}: duplicate id")
        seen.add(fid)
        status = feat.get("status")
        if status not in STATUSES:
            errors.append(f"{where}: invalid status '{status}'")
        if status == "in_progress":
            in_progress += 1
        spec = feat.get("spec")
        if isinstance(spec, str) and not (ROOT / spec).is_file():
            errors.append(f"{where}: spec file not found: {spec}")
        plats = feat.get("platforms")
        if not isinstance(plats, dict) or not plats:
            errors.append(f"{where}: 'platforms' must be a non-empty object")
            plats = {}
        for name, state in plats.items():
            if name not in allowed:
                errors.append(f"{where}: platform '{name}' not in PLATFORMS ({' '.join(allowed)})")
            if state not in PLATFORM_STATES:
                errors.append(f"{where}: invalid platform state '{state}' for {name}")
        if status == "planned" and any(s != "pending" for s in plats.values()):
            errors.append(f"{where}: planned features must have all platforms 'pending'")
        if status == "done":
            if feat.get("verified") is not True:
                errors.append(f"{where}: done requires verified=true")
            if any(s != "done" for s in plats.values()):
                errors.append(f"{where}: done requires every platform 'done'")
            gate = feat.get("gate") or {}
            covered = set(gate.get("sensors", []))
            if not gate.get("legacy") and not set(plats) <= covered:
                errors.append(f"{where}: done requires a recorded gate covering {sorted(plats)}")
        elif feat.get("verified") is True:
            errors.append(f"{where}: verified=true is only valid for done features")
    if in_progress > 1:
        errors.append(f"only one feature may be in_progress (found {in_progress})")
    return errors


# ---------------------------------------------------------------- commands
def cmd_status(args):
    data = load()
    feats = data.get("features", [])
    counts = {s: sum(1 for f in feats if f.get("status") == s) for s in STATUSES}
    print(f"Project: {data.get('project', '?')}")
    print("Board:   " + "  ".join(f"{s}={n}" for s, n in counts.items()))
    cur = active(data)
    if cur:
        f = cur[0]
        print(f"Active:  {f['id']} - {f['title']}")
        print("         " + "  ".join(f"{p}={s}" for p, s in f["platforms"].items()))
        print(f"Spec:    {f['spec']}")
        return
    planned = sorted((f for f in feats if f.get("status") == "planned"), key=lambda f: f.get("priority", 999))
    if planned:
        f = planned[0]
        print(f"Active:  none. Next planned: {f['id']} - {f['title']}")
        print(f"Start:   python3 scripts/feature.py start {f['id']}")
    elif not feats:
        print("Active:  none. Board is empty. Write a spec (skill: feature-spec-writer), then:")
        print("         python3 scripts/feature.py add <id> \"<title>\" --spec features/NN-<id>.feature")
    else:
        print("Active:  none. All features are done or blocked.")


def cmd_list(args):
    for f in load().get("features", []):
        plats = ",".join(f"{p}:{s}" for p, s in f["platforms"].items())
        print(f"{f.get('priority', '-'):>3}  {f['status']:<11} {f['id']:<32} {plats}")


def cmd_next(args):
    data = load()
    cur = active(data)
    if cur:
        print(cur[0]["id"])
        return
    if args.active_only:
        return
    planned = sorted((f for f in data["features"] if f["status"] == "planned"), key=lambda f: f.get("priority", 999))
    if planned:
        print(planned[0]["id"])


def cmd_platforms(args):
    print(" ".join(find(load(), args.id)["platforms"].keys()))


def cmd_add(args):
    data = load()
    if not ID_RE.match(args.id):
        die("id must be kebab-case (e.g. plant-detail)")
    if any(f["id"] == args.id for f in data["features"]):
        die(f"feature '{args.id}' already exists")
    errs = spec_errors(args.spec)
    if errs:
        die("; ".join(errs) + ". Create the spec from features/00-template.feature first.")
    chosen = args.platforms.split(",") if args.platforms else env_platforms(load_env())
    unknown = [p for p in chosen if p not in env_platforms(load_env())]
    if unknown:
        die(f"unknown platform(s): {', '.join(unknown)}")
    priority = args.priority or (max([f.get("priority", 0) for f in data["features"]] or [0]) + 1)
    data["features"].append({
        "id": args.id, "title": args.title, "spec": args.spec, "status": "planned",
        "priority": priority, "platforms": {p: "pending" for p in chosen},
        "gate": None, "verified": False,
    })
    save(data)
    print(f"Added '{args.id}' (priority {priority}).")


def cmd_start(args):
    data = load()
    feat = find(data, args.id)
    other = [f["id"] for f in active(data) if f["id"] != args.id]
    if other:
        die(f"'{other[0]}' is already in_progress. One feature at a time.")
    if feat["status"] not in ("planned", "blocked"):
        die(f"cannot start a feature that is '{feat['status']}'")
    errs = spec_errors(feat["spec"])
    if errs:
        die("; ".join(errs))
    feat["status"] = "in_progress"
    feat.pop("blocked_reason", None)
    save(data)
    print(f"'{args.id}' is now in_progress.")


def cmd_platform(args):
    data = load()
    feat = find(data, args.id)
    if feat["status"] != "in_progress":
        die("feature must be in_progress")
    if args.name not in feat["platforms"]:
        die(f"'{args.name}' is not a platform of this feature ({', '.join(feat['platforms'])})")
    if args.state == "sensor_green":
        die("sensor_green is written only by a passing sensor (make sensor-ios / sensor-android).", 2)
    if args.state not in MANUAL_PLATFORM_STATES:
        die(f"state must be one of {MANUAL_PLATFORM_STATES}")
    feat["platforms"][args.name] = args.state
    save(data)
    print(f"{args.id}: {args.name} -> {args.state}")


def cmd_record_sensor(args):
    data = load()
    cur = active(data)
    if len(cur) != 1:
        print("note: no single in_progress feature; sensor result not recorded on the board.")
        return
    feat = cur[0]
    if args.platform not in feat["platforms"]:
        print(f"note: {args.platform} is not a platform of '{feat['id']}'; not recorded.")
        return
    sensors = feat.setdefault("sensors", {})
    if args.fail:
        feat["platforms"][args.platform] = "in_progress"
        sensors.pop(args.platform, None)
        gate_note = " (previous gate invalidated)" if feat.get("gate") else ""
        feat["gate"] = None
        save(data)
        print(f"{feat['id']}: {args.platform} -> in_progress (sensor red){gate_note}")
        return
    feat["platforms"][args.platform] = "sensor_green"
    sensors[args.platform] = {"at": now(), "mode": args.mode}
    feat["gate"] = None  # any new sensor result invalidates an older gate
    save(data)
    print(f"{feat['id']}: {args.platform} -> sensor_green ({args.mode})")


def cmd_gate(args):
    data = load()
    feat = find(data, args.id)
    if feat["status"] != "in_progress":
        die("gate can only be recorded for the in_progress feature")
    passed = [s for s in args.sensors.split(",") if s]
    missing = [p for p in feat["platforms"] if p not in passed]
    if missing:
        die(f"gate incomplete: no passing sensor for {', '.join(missing)}", 3)
    recorded = feat.get("sensors", {})
    degraded = sorted(p for p in passed if recorded.get(p, {}).get("mode", "test") != "test")
    feat["gate"] = {"passed_at": now(), "sensors": sorted(passed), "degraded": degraded}
    save(data)
    print(f"Gate recorded for '{feat['id']}'" + (f" (degraded: {', '.join(degraded)})" if degraded else "."))


def cmd_done(args):
    if not args.human_checklist_ok:
        die("closing a feature is a HUMAN decision. Complete docs/dual-checklist.md, then re-run with "
            "--human-checklist-ok.", 2)
    data = load()
    feat = find(data, args.id)
    if feat["status"] != "in_progress":
        die("only an in_progress feature can be closed")
    gate = feat.get("gate")
    if not gate or not set(feat["platforms"]) <= set(gate.get("sensors", [])):
        die("no recorded gate covering every platform. Run: sh scripts/verify-feature.sh " + args.id)
    not_green = [p for p, s in feat["platforms"].items() if s != "sensor_green"]
    if not_green:
        die(f"platform(s) not sensor_green: {', '.join(not_green)}")
    for name in feat["platforms"]:
        feat["platforms"][name] = "done"
    feat["status"], feat["verified"], feat["completed_at"] = "done", True, now()
    save(data)
    if gate.get("degraded"):
        print(f"WARNING: closed with degraded sensors: {', '.join(gate['degraded'])}")
    print(f"'{args.id}' is done.")


def cmd_block(args):
    data = load()
    feat = find(data, args.id)
    if feat["status"] == "done":
        die("a done feature cannot be blocked")
    feat["status"] = "blocked"
    feat["blocked_reason"] = args.reason
    feat["gate"] = None
    save(data)
    print(f"'{args.id}' is blocked: {args.reason}")


def cmd_check(args):
    data = load()
    if args.id:
        feat = find(data, args.id)
    else:
        cur = active(data)
        if not cur:
            print("No in_progress feature.")
            return
        feat = cur[0]
    errs = spec_errors(feat["spec"])
    if errs:
        die("; ".join(errs))
    print(f"OK: spec for '{feat['id']}' has Feature and Scenario(s).")


def cmd_validate(args):
    errs = validate()
    if errs:
        for e in errs:
            print(f"  - {e}", file=sys.stderr)
        sys.exit(1)
    print("OK: feature_list.json is consistent.")


def cmd_import_legacy(args):
    """Convert a Leafly-style array board (v1) into the schema_version 2 object."""
    src = json.loads(open(args.path, encoding="utf-8").read())
    if not isinstance(src, list):
        die("legacy board must be a JSON array")
    out = {"schema_version": 2, "project": load_env().get("PROJECT_NAME", "project"), "features": []}
    for item in src:
        plats = item.get("platforms") or ["ios", "android"]
        plats = plats if isinstance(plats, list) else list(plats)
        status = item.get("status", "planned")
        feat = {
            "id": item["id"], "title": item.get("title", item["id"]), "spec": item.get("spec", ""),
            "status": status, "priority": item.get("priority", 999),
            "platforms": {p: ("done" if status == "done" else "pending") for p in plats},
            "gate": {"legacy": True} if status == "done" else None,
            "verified": status == "done",
        }
        out["features"].append(feat)
    save(out)
    print(f"Imported {len(out['features'])} feature(s). Review feature_list.json, then run: make validate-harness")


def build_parser():
    p = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    sub = p.add_subparsers(dest="cmd", required=True)
    sub.add_parser("status").set_defaults(fn=cmd_status)
    sub.add_parser("list").set_defaults(fn=cmd_list)
    s = sub.add_parser("next"); s.add_argument("--active-only", action="store_true"); s.set_defaults(fn=cmd_next)
    s = sub.add_parser("platforms"); s.add_argument("id"); s.set_defaults(fn=cmd_platforms)
    s = sub.add_parser("add"); s.add_argument("id"); s.add_argument("title")
    s.add_argument("--spec", required=True); s.add_argument("--priority", type=int)
    s.add_argument("--platforms", help="comma-separated subset, default: all in harness.env"); s.set_defaults(fn=cmd_add)
    s = sub.add_parser("start"); s.add_argument("id"); s.set_defaults(fn=cmd_start)
    s = sub.add_parser("platform"); s.add_argument("id"); s.add_argument("name"); s.add_argument("state"); s.set_defaults(fn=cmd_platform)
    s = sub.add_parser("record-sensor"); s.add_argument("platform"); s.add_argument("--fail", action="store_true")
    s.add_argument("--mode", default="test"); s.set_defaults(fn=cmd_record_sensor)
    s = sub.add_parser("gate"); s.add_argument("id"); s.add_argument("--sensors", required=True); s.set_defaults(fn=cmd_gate)
    s = sub.add_parser("done"); s.add_argument("id"); s.add_argument("--human-checklist-ok", action="store_true"); s.set_defaults(fn=cmd_done)
    s = sub.add_parser("block"); s.add_argument("id"); s.add_argument("--reason", required=True); s.set_defaults(fn=cmd_block)
    s = sub.add_parser("check"); s.add_argument("id", nargs="?"); s.set_defaults(fn=cmd_check)
    sub.add_parser("validate").set_defaults(fn=cmd_validate)
    s = sub.add_parser("import-legacy"); s.add_argument("path"); s.set_defaults(fn=cmd_import_legacy)
    return p


if __name__ == "__main__":
    args = build_parser().parse_args()
    args.fn(args)
