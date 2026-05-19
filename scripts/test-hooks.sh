#!/usr/bin/env bash
# Test script for block-dangerous-commands.sh and audit-log.sh
# Run from the project root with: bash scripts/test-hooks.sh

set -uo pipefail

PASS=0
FAIL=0

run_test() {
    local label="$1"
    local input="$2"
    local expected_exit="$3"

    actual_exit=0
    echo "$input" | bash .github/hooks/scripts/block-dangerous-commands.sh > /tmp/hook-output.txt 2>&1 || actual_exit=$?

    if [ "$actual_exit" -eq "$expected_exit" ]; then
        echo "  PASS: $label (exit=$actual_exit)"
        PASS=$((PASS + 1))
    else
        echo "  FAIL: $label (expected exit=$expected_exit, got exit=$actual_exit)"
        cat /tmp/hook-output.txt
        FAIL=$((FAIL + 1))
    fi
}

echo ""
echo "=== block-dangerous-commands.sh tests ==="

# Should BLOCK (exit 2)
run_test "run_in_terminal + Remove-Item tests" \
    '{"tool_name":"run_in_terminal","tool_input":{"command":"Remove-Item -Recurse -Force tests"}}' 2

run_test "execution_subagent + rm -rf tests/" \
    '{"tool_name":"execution_subagent","tool_input":{"command":"rm -rf tests/"}}' 2

run_test "execution_subagent + rm -rf /src" \
    '{"tool_name":"execution_subagent","tool_input":{"command":"Remove-Item -Recurse -Force src"}}' 2

run_test "run_in_terminal + rm -rf /" \
    '{"tool_name":"run_in_terminal","tool_input":{"command":"rm -rf /"}}' 2

run_test "run_in_terminal + git push origin main" \
    '{"tool_name":"run_in_terminal","tool_input":{"command":"git push origin main"}}' 2

# Should ALLOW (exit 0)
run_test "non-terminal tool (file read)" \
    '{"tool_name":"read_file","tool_input":{"path":"src/main.py"}}' 0

run_test "run_in_terminal + pytest (safe)" \
    '{"tool_name":"run_in_terminal","tool_input":{"command":"pytest tests/ -v"}}' 0

run_test "run_in_terminal + git status (safe)" \
    '{"tool_name":"run_in_terminal","tool_input":{"command":"git status"}}' 0

echo ""
echo "=== audit-log.sh test ==="
echo '{"tool_name":"run_in_terminal","sessionId":"test-session-abc","tool_input":{"command":"pytest"}}' \
    | bash .github/hooks/scripts/audit-log.sh
echo "  Audit log tail:"
tail -3 .copilot-audit.log 2>/dev/null | sed 's/^/    /'

echo ""
echo "=== Results: $PASS passed, $FAIL failed ==="
[ "$FAIL" -eq 0 ] && exit 0 || exit 1
