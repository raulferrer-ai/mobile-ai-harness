#!/usr/bin/env python3
"""PreToolUse guard for shell commands (Claude Code, Cursor beforeShellExecution, or plain stdin).

Exit 2 = blocked (stderr is shown to the agent). Exit 0 = allowed.
This is a guardrail against accidents, not a security boundary.
"""
import json
import re
import sys

DESTRUCTIVE = [
    (r"\brm\s+(-[a-zA-Z]*[rR][a-zA-Z]*[fF]|-[a-zA-Z]*[fF][a-zA-Z]*[rR])\b", "recursive force delete (rm -rf)"),
    (r"\brm\s+-[rR]\s+-[fF]\b|\brm\s+-[fF]\s+-[rR]\b", "recursive force delete (rm -r -f)"),
    (r"\bgit\s+reset\s+--hard\b", "git reset --hard"),
    (r"\bgit\s+push\b.*(\s--force(?!-with-lease)\b|\s-f\b)", "git push --force"),
    (r"\bgit\s+clean\s+-[a-zA-Z]*f", "git clean -f"),
    (r"\bgit\s+checkout\s+(--\s+)?\.(\s|$)", "git checkout . (discards changes)"),
    (r"\bgit\s+branch\s+-D\b", "git branch -D"),
    (r"--no-verify\b", "skipping git hooks (--no-verify)"),
    (r"\bsudo\b", "sudo"),
    (r"\b(curl|wget)\b[^|;]*\|\s*(sh|bash|zsh)\b", "piping a download into a shell"),
    (r"\bchmod\s+-R\s+777\b", "chmod -R 777"),
]

HUMAN_ONLY = [
    (r"feature\.py\s+done\b", "closing a feature is a human decision (dual checklist)"),
    (r"--human-checklist-ok", "the human checklist flag must be typed by a human"),
]


def extract_command(raw):
    try:
        payload = json.loads(raw)
    except (json.JSONDecodeError, ValueError):
        return raw
    if isinstance(payload, dict):
        tool_input = payload.get("tool_input")
        if isinstance(tool_input, dict) and "command" in tool_input:
            return str(tool_input["command"])
        if "command" in payload:
            return str(payload["command"])
    return raw


def main():
    command = extract_command(sys.stdin.read())
    for pattern, label in DESTRUCTIVE:
        if re.search(pattern, command):
            print(f"BLOCKED: {label}. Ask the human for explicit approval.", file=sys.stderr)
            return 2
    for pattern, label in HUMAN_ONLY:
        if re.search(pattern, command):
            print(f"BLOCKED (human-only): {label}.", file=sys.stderr)
            return 2
    return 0


if __name__ == "__main__":
    sys.exit(main())
