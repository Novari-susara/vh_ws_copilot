#!/usr/bin/env bash
# .github/hooks/scripts/auto-format.sh
#
# PostToolUse hook: runs ruff formatter on Python files after every edit.
# Only triggers when a .py file was modified.

set -euo pipefail

INPUT=$(cat)
TOOL_NAME=$(echo "$INPUT" | python3 -c "import sys,json; d=json.load(sys.stdin); print(d.get('tool_name',''))" 2>/dev/null || echo "")
TOOL_INPUT=$(echo "$INPUT" | python3 -c "import sys,json; d=json.load(sys.stdin); print(json.dumps(d.get('tool_input','')))" 2>/dev/null || echo "{}")

# Only run for file edit tools
if [[ "$TOOL_NAME" != *"edit"* ]] && [[ "$TOOL_NAME" != *"write"* ]] && [[ "$TOOL_NAME" != *"create"* ]]; then
    exit 0
fi

# Extract file path from tool input
FILE_PATH=$(echo "$TOOL_INPUT" | python3 -c "
import sys, json
d = json.load(sys.stdin)
print(d.get('path', d.get('file_path', d.get('filePath', ''))))
" 2>/dev/null || echo "")

# Only format Python files
if [[ "$FILE_PATH" != *.py ]]; then
    exit 0
fi

# Run ruff format if available
if command -v ruff &>/dev/null; then
    FORMAT_OUTPUT=$(ruff format "$FILE_PATH" 2>&1 || true)
    LINT_OUTPUT=$(ruff check "$FILE_PATH" --fix --quiet 2>&1 || true)
    
    MSG="✅ Auto-formatted: $FILE_PATH"
    if [ -n "$LINT_OUTPUT" ]; then
        MSG="$MSG\n⚠️ Lint issues (auto-fixed where possible):\n$LINT_OUTPUT"
    fi
    
    python3 -c "
import json, sys
msg = sys.argv[1]
print(json.dumps({
    'hookSpecificOutput': {
        'hookEventName': 'PostToolUse',
        'additionalContext': msg
    }
}))
" "$MSG"
else
    # ruff not installed — suggest it
    python3 -c "
print('{\"systemMessage\": \"💡 Tip: Install ruff for auto-formatting: pip install ruff\"}')
"
fi

exit 0
