#!/usr/bin/env python3
"""Shared helpers for harness scripts (standard library only)."""
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
ENV_FILE = ROOT / "harness.env"

REQUIRED_KEYS = (
    "PROJECT_NAME", "PLATFORMS",
    "IOS_DIR", "IOS_PROJECT", "IOS_SCHEME", "IOS_DESTINATION", "IOS_SENSOR_MODE",
    "ANDROID_DIR", "ANDROID_TEST_TASK", "MIN_JDK",
    "BUDGET_ROOT_AGENTS", "BUDGET_PLATFORM_AGENTS", "BUDGET_POINTER", "BUDGET_SKILL",
)

_LINE = re.compile(r"^([A-Z][A-Z0-9_]*)=(.*)$")


def load_env(path=ENV_FILE):
    """Parse KEY=VALUE lines (optionally quoted) from harness.env."""
    values = {}
    if not Path(path).is_file():
        return values
    for raw in Path(path).read_text(encoding="utf-8").splitlines():
        line = raw.strip()
        if not line or line.startswith("#"):
            continue
        match = _LINE.match(line)
        if not match:
            continue
        key, value = match.group(1), match.group(2).strip()
        if len(value) >= 2 and value[0] == value[-1] and value[0] in "\"'":
            value = value[1:-1]
        values[key] = value
    return values


def platforms(env=None):
    env = env if env is not None else load_env()
    return env.get("PLATFORMS", "ios android").split()


def budgets(env=None):
    """Return {relative_path: max_lines} for always-loaded contract files."""
    env = env if env is not None else load_env()

    def num(key, default):
        try:
            return int(env.get(key, default))
        except ValueError:
            return int(default)

    root, plat, pointer = (
        num("BUDGET_ROOT_AGENTS", 150),
        num("BUDGET_PLATFORM_AGENTS", 130),
        num("BUDGET_POINTER", 15),
    )
    return {
        "AGENTS.md": root,
        "ios/AGENTS.md": plat,
        "android/AGENTS.md": plat,
        "CLAUDE.md": pointer,
        "GEMINI.md": pointer,
    }


def skill_budget(env=None):
    env = env if env is not None else load_env()
    try:
        return int(env.get("BUDGET_SKILL", 80))
    except ValueError:
        return 80
