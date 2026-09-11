#!/usr/bin/env python3
"""Validate harness integrity: structure, budgets, schemas, skills, links and anti-drift checks."""
import json
import re
import subprocess
import sys

from harness_config import ROOT, REQUIRED_KEYS, budgets, load_env, skill_budget
import feature as board

ERRORS, WARNINGS = [], []

REQUIRED_FILES = [
    "AGENTS.md", "CLAUDE.md", "GEMINI.md", "README.md", "CHANGELOG.md",
    "android/AGENTS.md", "ios/AGENTS.md",
    "harness.env", "Makefile", "init.sh", ".gitignore", ".gitattributes", ".editorconfig",
    ".aiexclude", ".cursorignore",
    ".claude/settings.json", ".opencode/opencode.json", ".codex/config.toml", ".cursor/hooks.json",
    ".github/workflows/ci.yml", ".github/pull_request_template.md",
    ".agents/skills/README.md",
    ".agents/hooks/block-destructive.py", ".agents/hooks/guard-sensitive-paths.py",
    ".agents/hooks/check-contract-size.py",
    ".agents/references/ios-stack.md", ".agents/references/android-stack.md",
    ".agents/references/gherkin-guide.md",
    "docs/architecture.md", "docs/stack.md", "docs/customizing.md", "docs/workflow.md",
    "docs/flywheel.md", "docs/design-system.md", "docs/parity-matrix.md", "docs/product.md",
    "docs/dual-checklist.md", "docs/decisions/0000-template.md", "docs/decisions/0001-stack-defaults.md",
    "docs/security.md", "docs/privacy-compliance.md", "docs/ai-governance.md", "docs/bootstrap.md",
    "SECURITY.md", "CONTRIBUTING.md", ".github/CODEOWNERS", ".github/dependabot.yml", ".secrets-allowlist",
    "scripts/scan-secrets.py", "scripts/doctor.sh", "templates/sample-feature/README.md",
    "templates/sample-feature/spec/01-sample-items.feature",
    "features/00-template.feature", "feature_list.json",
    "progress/current.md", "progress/log.md", "progress/flywheel-log.md",
    "scripts/validate-harness.py", "scripts/feature.py", "scripts/harness_config.py",
    "scripts/sensor.sh", "scripts/verify-feature.sh",
]

env = load_env()

# 1. Symlinks are forbidden (portability)
for path in ROOT.rglob("*"):
    if ".git" in path.parts:
        continue
    if path.is_symlink():
        ERRORS.append(f"forbidden symlink: {path.relative_to(ROOT)}")

# 2. Required files
for rel in REQUIRED_FILES:
    if not (ROOT / rel).is_file():
        ERRORS.append(f"missing required file: {rel}")

# 3. harness.env keys
for key in REQUIRED_KEYS:
    if key not in env:
        ERRORS.append(f"harness.env: missing key {key}")

# 4. Contract line budgets
for rel, limit in budgets(env).items():
    target = ROOT / rel
    if target.is_file():
        count = len(target.read_text(encoding="utf-8").splitlines())
        if count > limit:
            ERRORS.append(f"{rel} exceeds its budget: {count} > {limit} lines")

# 5. Pointer files must point at AGENTS.md
for rel in ("CLAUDE.md", "GEMINI.md"):
    target = ROOT / rel
    if target.is_file() and "AGENTS.md" not in target.read_text(encoding="utf-8"):
        ERRORS.append(f"{rel} must point to AGENTS.md")

# 6. Script hygiene: shebangs, shell syntax, python compiles
for sh_file in list((ROOT / "scripts").glob("*.sh")) + [ROOT / "init.sh"]:
    if not sh_file.is_file():
        continue
    text = sh_file.read_text(encoding="utf-8")
    if not text.startswith("#!/usr/bin/env sh"):
        ERRORS.append(f"{sh_file.relative_to(ROOT)}: expected '#!/usr/bin/env sh' shebang")
    try:
        result = subprocess.run(["sh", "-n", str(sh_file)], capture_output=True, text=True)
        if result.returncode != 0:
            ERRORS.append(f"{sh_file.relative_to(ROOT)}: shell syntax error: {result.stderr.strip()}")
    except FileNotFoundError:
        pass
for py_file in list((ROOT / "scripts").rglob("*.py")) + list((ROOT / ".agents" / "hooks").glob("*.py")):
    try:
        compile(py_file.read_text(encoding="utf-8"), str(py_file), "exec")
    except SyntaxError as exc:
        ERRORS.append(f"{py_file.relative_to(ROOT)}: python syntax error: {exc}")

# 7. JSON and TOML configs
for rel in (".claude/settings.json", ".opencode/opencode.json", ".cursor/hooks.json", "feature_list.json"):
    target = ROOT / rel
    if target.is_file():
        try:
            json.loads(target.read_text(encoding="utf-8"))
        except json.JSONDecodeError as exc:
            ERRORS.append(f"invalid JSON in {rel}: {exc}")
try:
    import tomllib
    toml = ROOT / ".codex" / "config.toml"
    if toml.is_file():
        try:
            tomllib.loads(toml.read_text(encoding="utf-8"))
        except tomllib.TOMLDecodeError as exc:
            ERRORS.append(f"invalid TOML in .codex/config.toml: {exc}")
except ImportError:
    pass  # Python < 3.11

# 7b. CODEOWNERS must cover the harness control files; placeholders only warn
owners = ROOT / ".github" / "CODEOWNERS"
if owners.is_file():
    text = owners.read_text(encoding="utf-8")
    for needed in ("/AGENTS.md", "/scripts/", "/.agents/", "/.github/"):
        if needed not in text:
            ERRORS.append(f".github/CODEOWNERS must cover {needed}")
    if "@your-org/" in text:
        WARNINGS.append(".github/CODEOWNERS still has @your-org placeholders (replace before adoption)")

# 8. Feature board invariants and specs
if (ROOT / "feature_list.json").is_file():
    try:
        data = json.loads((ROOT / "feature_list.json").read_text(encoding="utf-8"))
        ERRORS.extend(board.validate(data))
        referenced = {f.get("spec") for f in data.get("features", []) if isinstance(f, dict)}
        for spec in sorted((ROOT / "features").glob("*.feature")):
            rel = spec.relative_to(ROOT).as_posix()
            if spec.name == "00-template.feature":
                continue
            if rel not in referenced:
                WARNINGS.append(f"spec not registered in feature_list.json: {rel}")
    except json.JSONDecodeError:
        pass

# 9. Skills: frontmatter, name == folder, budget, index consistency
skills_dir = ROOT / ".agents" / "skills"
skill_names = []
limit = skill_budget(env)
if skills_dir.is_dir():
    for skill_md in sorted(skills_dir.glob("*/SKILL.md")):
        folder = skill_md.parent.name
        skill_names.append(folder)
        text = skill_md.read_text(encoding="utf-8")
        rel = skill_md.relative_to(ROOT)
        match = re.match(r"^---\n(.*?)\n---\n", text, re.S)
        if not match:
            ERRORS.append(f"{rel}: missing YAML frontmatter")
            continue
        front = match.group(1)
        name = re.search(r"^name:\s*(.+)$", front, re.M)
        desc = re.search(r"^description:\s*(.+)$", front, re.M)
        if not name or name.group(1).strip() != folder:
            ERRORS.append(f"{rel}: frontmatter name must equal folder name '{folder}'")
        if not desc or not desc.group(1).strip():
            ERRORS.append(f"{rel}: missing description")
        elif len(desc.group(1)) > 1024:
            ERRORS.append(f"{rel}: description longer than 1024 chars")
        if len(text.splitlines()) > limit:
            ERRORS.append(f"{rel}: exceeds skill budget ({len(text.splitlines())} > {limit} lines)")
    index = skills_dir / "README.md"
    if index.is_file():
        listed = set(re.findall(r"^- `([a-z0-9-]+)`", index.read_text(encoding="utf-8"), re.M))
        for n in skill_names:
            if n not in listed:
                ERRORS.append(f"skills/README.md does not list skill '{n}'")
        for n in listed - set(skill_names):
            ERRORS.append(f"skills/README.md lists missing skill '{n}'")

# 10. Markdown links and backticked path references (anti-drift)
md_files = [p for p in ROOT.rglob("*.md") if ".git" not in p.parts]
link_re = re.compile(r"\[[^\]]+\]\(([^)#\s]+)(?:#[^)]*)?\)")
path_re = re.compile(
    r"`((?:scripts|\.agents|docs|progress|\.github|\.claude|\.opencode|\.codex|\.cursor)/[^`\s<>*{}\u2026]+)`"
)
for md in md_files:
    text = md.read_text(encoding="utf-8")
    rel_md = md.relative_to(ROOT)
    for target in link_re.findall(text):
        if target.startswith(("http://", "https://", "mailto:")):
            continue
        if not (md.parent / target).resolve().exists():
            ERRORS.append(f"broken link '{target}' in {rel_md}")
    if rel_md.parts[0] in ("docs", ".agents") or rel_md.name in ("README.md", "AGENTS.md"):
        for ref in path_re.findall(text):
            ref = ref.rstrip(".,:;)")
            if not (ROOT / ref).exists():
                ERRORS.append(f"{rel_md} references missing path '{ref}'")

# 11. `make <target>` mentioned in docs must exist in the Makefile
makefile = ROOT / "Makefile"
if makefile.is_file():
    targets = set(re.findall(r"^([a-zA-Z_-]+):", makefile.read_text(encoding="utf-8"), re.M))
    for md in md_files:
        for tgt in re.findall(r"`make ([a-z]+(?:-[a-z]+)*)(?![a-z*-])", md.read_text(encoding="utf-8")):
            if tgt not in targets:
                ERRORS.append(f"{md.relative_to(ROOT)} mentions unknown make target '{tgt}'")

for w in WARNINGS:
    print(f"warning: {w}", file=sys.stderr)
if ERRORS:
    print("HARNESS VALIDATION FAILED:", file=sys.stderr)
    for err in ERRORS:
        print(f"  - {err}", file=sys.stderr)
    sys.exit(1)
print("OK: harness is valid, portable, symlink-free and consistent.")
