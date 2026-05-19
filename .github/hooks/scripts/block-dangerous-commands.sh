#!/usr/bin/env bash
# .github/hooks/scripts/block-dangerous-commands.sh
#
# PreToolUse hook: blocks dangerous terminal commands before they run.
# Reads TOOL_NAME and TOOL_INPUT_COMMAND from environment.
# Exit 2 = hard block (shown to user as error, tool call cancelled).
# Exit 0 = allow.
#
# VS Code passes tool info via stdin as JSON.

set -euo pipefail

# Read stdin JSON input
INPUT=$(cat)
TOOL_NAME=$(echo "$INPUT" | python3 -c "import sys,json; d=json.load(sys.stdin); print(d.get('tool_name',''))" 2>/dev/null || echo "")
TOOL_INPUT=$(echo "$INPUT" | python3 -c "import sys,json; d=json.load(sys.stdin); print(json.dumps(d.get('tool_input','')))" 2>/dev/null || echo "{}")

# Only check terminal/shell tool calls
if [[ "$TOOL_NAME" != *"terminal"* ]] && [[ "$TOOL_NAME" != *"shell"* ]] && [[ "$TOOL_NAME" != *"bash"* ]]; then
    exit 0
fi

# Extract the command string from tool input
COMMAND=$(echo "$TOOL_INPUT" | python3 -c "
import sys, json
d = json.load(sys.stdin)
# Handle both 'command' and 'cmd' keys
print(d.get('command', d.get('cmd', d.get('input', ''))))
" 2>/dev/null || echo "")

# ─── BLOCKED PATTERNS ─────────────────────────────────────────────────────────

# Destructive file operations
if echo "$COMMAND" | grep -qE "rm\s+-rf\s+(/|\./)"; then
    cat << 'EOF'
{"continue": false, "stopReason": "🚫 BLOCKED: Detected 'rm -rf /' or 'rm -rf ./' — this would delete critical files. Please specify the exact directory to remove.", "systemMessage": "Dangerous command blocked by PreToolUse hook."}
EOF
    exit 2
fi

# Prevent dropping production database
if echo "$COMMAND" | grep -qiE "drop\s+database|drop\s+table\s+.*cascade"; then
    cat << 'EOF'
{"continue": false, "stopReason": "🚫 BLOCKED: DROP DATABASE / DROP TABLE CASCADE detected. Use migrations instead.", "systemMessage": "Destructive database command blocked."}
EOF
    exit 2
fi

# Prevent pushing to main/master directly
if echo "$COMMAND" | grep -qE "git push.*origin\s+(main|master)\b"; then
    cat << 'EOF'
{"continue": false, "stopReason": "🚫 BLOCKED: Direct push to main/master. Create a feature branch and open a PR instead.", "systemMessage": "Direct push to protected branch blocked."}
EOF
    exit 2
fi

# Prevent installing packages without --break-system-packages notice
if echo "$COMMAND" | grep -qE "pip install" && ! echo "$COMMAND" | grep -qE "\-\-break\-system\-packages|venv|virtualenv"; then
    # This is a warning, not a block (exit 0 with systemMessage)
    cat << 'EOF'
{"systemMessage": "⚠️  Tip: If you're not in a venv, add --break-system-packages or activate your virtual environment first."}
EOF
    exit 0
fi

# Prevent curl | bash (arbitrary code execution)
if echo "$COMMAND" | grep -qE "curl.*\|.*bash|wget.*\|.*sh"; then
    cat << 'EOF'
{"continue": false, "stopReason": "🚫 BLOCKED: curl|bash pattern detected. Download the script first, review it, then run it explicitly.", "systemMessage": "Arbitrary code execution pattern blocked."}
EOF
    exit 2
fi

# All checks passed — allow the command
exit 0
