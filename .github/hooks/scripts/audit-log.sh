#!/usr/bin/env bash
# .github/hooks/scripts/audit-log.sh
#
# PostToolUse hook: logs every tool invocation to .copilot-audit.log
# for compliance and debugging purposes.

set -euo pipefail

# Portable Python: prefer python3, fall back to python (Windows Git Bash compatibility)
PYTHON=$(python3 -c "import sys" >/dev/null 2>&1 && echo "python3" || echo "python")

INPUT=$(cat)
LOG_FILE=".copilot-audit.log"
TIMESTAMP=$(date -u "+%Y-%m-%dT%H:%M:%SZ")

TOOL_NAME=$(echo "$INPUT" | "$PYTHON" -c "import sys,json; d=json.load(sys.stdin); print(d.get('tool_name','unknown'))" 2>/dev/null || echo "unknown")
SESSION_ID=$(echo "$INPUT" | "$PYTHON" -c "import sys,json; d=json.load(sys.stdin); print(d.get('sessionId','unknown'))" 2>/dev/null || echo "unknown")

# Log the tool use (append to audit log)
echo "${TIMESTAMP} | session=${SESSION_ID} | tool=${TOOL_NAME}" >> "$LOG_FILE" 2>/dev/null || true

# Always exit 0 — this is a silent logger, not a blocker
exit 0
