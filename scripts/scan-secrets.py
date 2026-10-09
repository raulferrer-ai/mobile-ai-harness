#!/usr/bin/env python3
"""Lightweight secret and forbidden-file scan (standard library only).

Complements, never replaces, an enterprise scanner (e.g. your org's secret scanning / push protection).
Scans tracked and untracked-but-not-ignored files (git), or walks the tree when git is unavailable.
Allow a known false positive with an inline marker `secrets:allow` or a glob in `.secrets-allowlist`.
Exit 1 when something is found.
"""
import fnmatch
import re
import subprocess
import sys

from harness_config import ROOT

SKIP_DIRS = {".git", "node_modules", "build", ".gradle", "DerivedData", "Pods", ".build", ".idea"}
SKIP_EXT = {".png", ".jpg", ".jpeg", ".webp", ".gif", ".ico", ".jar", ".zip", ".pdf", ".ttf", ".otf", ".woff",
            ".woff2", ".keystore", ".jks", ".p12", ".mobileprovision", ".car", ".xcassets"}
SELF = {"scripts/scan-secrets.py", "scripts/tests/test_scan_secrets.py"}
MAX_BYTES = 1_000_000

CONTENT_PATTERNS = [
    (r"-----BEGIN (?:RSA |EC |DSA |OPENSSH |PGP )?PRIVATE KEY-----", "private key"),
    (r"\bAKIA[0-9A-Z]{16}\b", "AWS access key id"),
    (r"\bAIza[0-9A-Za-z_\-]{35}\b", "Google API key"),
    (r"\bxox[baprs]-[0-9A-Za-z\-]{10,}", "Slack token"),
    (r"\bgh[pousr]_[0-9A-Za-z]{36,}\b", "GitHub token"),
    (r"(?i)\b(?:api[_-]?key|secret|passwd|password|token)\b\s*[:=]\s*[\"'][^\"'\s]{12,}[\"']", "hardcoded credential"),
]
FORBIDDEN_NAMES = [".env", ".env.*", "*.jks", "*.keystore", "keystore.properties", "*.p12", "*.pfx", "*.pem",
                   "*.mobileprovision", "*.provisionprofile", "google-services.json", "GoogleService-Info.plist",
                   "local.properties"]
ALLOWED_NAMES = {".env.example", ".env.sample"}


def candidate_files():
    try:
        out = subprocess.run(["git", "ls-files", "-co", "--exclude-standard"], cwd=ROOT,
                             capture_output=True, text=True, check=True).stdout.splitlines()
        return [ROOT / p for p in out if p]
    except (subprocess.CalledProcessError, FileNotFoundError):
        return [p for p in ROOT.rglob("*") if p.is_file() and not (set(p.relative_to(ROOT).parts) & SKIP_DIRS)]


def allowlist():
    path = ROOT / ".secrets-allowlist"
    if not path.is_file():
        return []
    return [l.strip() for l in path.read_text(encoding="utf-8").splitlines() if l.strip() and not l.startswith("#")]


def main():
    allowed = allowlist()
    findings = []
    for path in candidate_files():
        if not path.is_file():
            continue
        rel = path.relative_to(ROOT).as_posix()
        if rel in SELF or any(fnmatch.fnmatch(rel, g) for g in allowed):
            continue
        name = path.name
        if name not in ALLOWED_NAMES and any(fnmatch.fnmatch(name, pat) for pat in FORBIDDEN_NAMES):
            findings.append(f"{rel}: forbidden file type is present in the repository ({name})")
            continue
        if path.suffix.lower() in SKIP_EXT or path.stat().st_size > MAX_BYTES:
            continue
        try:
            text = path.read_text(encoding="utf-8")
        except (UnicodeDecodeError, OSError):
            continue
        for lineno, line in enumerate(text.splitlines(), 1):
            if "secrets:allow" in line:
                continue
            for pattern, label in CONTENT_PATTERNS:
                if re.search(pattern, line):
                    findings.append(f"{rel}:{lineno}: possible {label}")
    if findings:
        print("SECRET SCAN FAILED:", file=sys.stderr)
        for f in findings:
            print(f"  - {f}", file=sys.stderr)
        print("Remove the secret and ROTATE it (it is compromised once committed). "
              "False positive? add `secrets:allow` on the line or a glob to .secrets-allowlist.", file=sys.stderr)
        return 1
    print("OK: no secrets or forbidden files detected.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
