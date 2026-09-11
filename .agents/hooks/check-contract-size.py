#!/usr/bin/env python3
"""Fail if an always-loaded contract file exceeds its line budget (limits live in harness.env)."""
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent.parent
sys.path.insert(0, str(ROOT / "scripts"))
from harness_config import budgets, load_env  # noqa: E402

failures = []
for rel, limit in budgets(load_env()).items():
    path = ROOT / rel
    if path.is_file():
        count = len(path.read_text(encoding="utf-8").splitlines())
        if count > limit:
            failures.append(f"{rel}: {count} lines (max {limit})")

if failures:
    print("CONTRACT SIZE CHECK FAILED:", file=sys.stderr)
    for item in failures:
        print(f"  - {item}", file=sys.stderr)
    sys.exit(1)
print("OK: all contract files are within their line budgets.")
