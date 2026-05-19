#!/usr/bin/env bash
# Plugin bundled format script — same logic as workspace hook
INPUT=$(cat)
TOOL_NAME=$(echo "$INPUT" | python3 -c "import sys,json; d=json.load(sys.stdin); print(d.get('tool_name',''))" 2>/dev/null || echo "")
if [[ "$TOOL_NAME" != *"edit"* ]] && [[ "$TOOL_NAME" != *"write"* ]]; then exit 0; fi
FILE_PATH=$(echo "$INPUT" | python3 -c "import sys,json; d=json.load(sys.stdin); print(d.get('tool_input',{}).get('path',''))" 2>/dev/null || echo "")
if [[ "$FILE_PATH" == *.py ]] && command -v ruff &>/dev/null; then
    ruff format "$FILE_PATH" --quiet 2>/dev/null || true
fi
exit 0
