#!/usr/bin/env python3
"""
.github/hooks/scripts/block-dangerous-commands.py

PreToolUse hook (Windows-compatible): blocks dangerous terminal commands.
Reads JSON from stdin (tool_name + tool_input).
Exit 2 = hard block (shown to user, tool call cancelled).
Exit 0 = allow.
"""

import json
import re
import sys


def block(reason: str, system_message: str) -> None:
    print(
        json.dumps(
            {"continue": False, "stopReason": reason, "systemMessage": system_message}
        )
    )
    sys.exit(2)


def warn(system_message: str) -> None:
    print(json.dumps({"systemMessage": system_message}))
    sys.exit(0)


def main() -> None:
    try:
        data = json.load(sys.stdin)
    except (json.JSONDecodeError, ValueError):
        sys.exit(0)

    tool_name: str = data.get("tool_name", "")
    tool_input = data.get("tool_input", {})

    # Only inspect terminal/shell tool calls
    terminal_keywords = ("terminal", "shell", "bash", "execution", "run_")
    if not any(kw in tool_name for kw in terminal_keywords):
        sys.exit(0)

    # Extract the command string
    if isinstance(tool_input, dict):
        command: str = tool_input.get(
            "command", tool_input.get("cmd", tool_input.get("input", ""))
        )
    else:
        command = str(tool_input)

    # ── BLOCKED PATTERNS ──────────────────────────────────────────────────────

    # Protect tests/ directory from deletion (bash and PowerShell)
    if re.search(
        r"(rm\s+(-rf|-r|-f)+\s+.*tests|Remove-Item.*tests)", command, re.IGNORECASE
    ):
        block(
            "🚫 BLOCKED: Attempted deletion of the tests/ directory. "
            "Test files are protected. Remove this protection in "
            "block-dangerous-commands.py if intentional.",
            "Test directory deletion blocked by PreToolUse hook.",
        )

    # rm -rf / or rm -rf ./
    if re.search(r"rm\s+-rf\s+(/|\.\/)", command):
        block(
            "🚫 BLOCKED: Detected 'rm -rf /' or 'rm -rf ./' — this would delete "
            "critical files. Please specify the exact directory to remove.",
            "Dangerous command blocked by PreToolUse hook.",
        )

    # PowerShell Remove-Item -Recurse -Force on protected directories
    if re.search(
        r"Remove-Item\s+.*-Recurse.*-Force.*(src|tests|\.)\b", command, re.IGNORECASE
    ):
        block(
            "🚫 BLOCKED: Destructive Remove-Item -Recurse -Force on a protected directory detected.",
            "Destructive PowerShell command blocked by PreToolUse hook.",
        )

    # DROP DATABASE / DROP TABLE CASCADE
    if re.search(r"drop\s+database|drop\s+table\s+.*cascade", command, re.IGNORECASE):
        block(
            "🚫 BLOCKED: DROP DATABASE / DROP TABLE CASCADE detected. Use migrations instead.",
            "Destructive database command blocked.",
        )

    # Direct push to main/master
    if re.search(r"git push.*origin\s+(main|master)\b", command):
        block(
            "🚫 BLOCKED: Direct push to main/master. Create a feature branch and open a PR instead.",
            "Direct push to protected branch blocked.",
        )

    # curl | bash  /  wget | sh
    if re.search(r"curl.*\|.*bash|wget.*\|.*sh", command):
        block(
            "🚫 BLOCKED: curl|bash pattern detected. Download the script first, "
            "review it, then run it explicitly.",
            "Arbitrary code execution pattern blocked.",
        )

    # pip install outside a venv — warning only (exit 0)
    if re.search(r"pip install", command) and not re.search(
        r"--break-system-packages|venv|virtualenv", command
    ):
        warn(
            "⚠️  Tip: If you're not in a venv, add --break-system-packages "
            "or activate your virtual environment first."
        )

    # All checks passed — allow
    sys.exit(0)


if __name__ == "__main__":
    main()
