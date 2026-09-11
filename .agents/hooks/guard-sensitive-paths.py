#!/usr/bin/env python3
"""PreToolUse guard for file edits: secrets, signing material, local IDE state, and the feature board.

Exit 2 = blocked. Exit 0 = allowed. Guardrail, not a security boundary.
"""
import fnmatch
import json
import os
import sys

SENSITIVE_NAMES = [
    ".env", ".env.*", "*.jks", "*.keystore", "keystore.properties", "*.p12", "*.pfx", "*.pem", "*.key",
    "*.cer", "*.crt", "*.der", "*.mobileprovision", "*.provisionprofile", "local.properties",
    "google-services.json", "GoogleService-Info.plist", "*.xcuserstate",
]
ALLOWED_NAMES = [".env.example", ".env.sample"]
SENSITIVE_PARTS = ["xcuserdata", os.path.join(".idea", "workspace.xml")]
ROOT = os.path.realpath(os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", ".."))
BOARD_PATHS = [os.path.join(ROOT, "feature_list.json")]


def extract_paths(raw):
    try:
        payload = json.loads(raw)
    except (json.JSONDecodeError, ValueError):
        return [raw.strip()] if raw.strip() else []
    paths = []
    if isinstance(payload, dict):
        for source in (payload.get("tool_input"), payload):
            if isinstance(source, dict):
                for key in ("file_path", "path", "notebook_path"):
                    if isinstance(source.get(key), str):
                        paths.append(source[key])
    return paths


def main():
    for path in extract_paths(sys.stdin.read()):
        norm = path.replace("\\", "/")
        name = norm.rsplit("/", 1)[-1]
        if name in ALLOWED_NAMES:
            continue
        if os.path.realpath(path) in BOARD_PATHS:
            print("BLOCKED: feature_list.json is a state machine. Use `python3 scripts/feature.py ...`.", file=sys.stderr)
            return 2
        if any(fnmatch.fnmatch(name, pat) for pat in SENSITIVE_NAMES) or any(
            part.replace("\\", "/") in norm for part in SENSITIVE_PARTS
        ):
            print(f"BLOCKED: '{path}' is a secret, signing file or local IDE state.", file=sys.stderr)
            return 2
    return 0


if __name__ == "__main__":
    sys.exit(main())
