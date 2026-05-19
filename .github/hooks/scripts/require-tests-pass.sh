#!/usr/bin/env bash
# .github/hooks/scripts/require-tests-pass.sh
#
# Stop hook: prevents the agent from finishing if tests are failing.
# The agent MUST fix failing tests before it can stop.
# 
# IMPORTANT: Check stop_hook_active to prevent infinite loops!

set -euo pipefail

INPUT=$(cat)

# Check if we're already in a stop-hook loop (prevent infinite looping)
HOOK_ACTIVE=$(echo "$INPUT" | python3 -c "
import sys, json
d = json.load(sys.stdin)
print(d.get('stop_hook_active', False))
" 2>/dev/null || echo "False")

# If we've already been called once, let the agent stop
if [[ "$HOOK_ACTIVE" == "True" ]]; then
    exit 0
fi

# Only run if there are Python test files
if ! find tests/ -name "test_*.py" -type f | grep -q .; then
    exit 0
fi

# Run the tests
echo "🧪 Running tests before allowing agent to stop..."
if command -v pytest &>/dev/null; then
    TEST_OUTPUT=$(pytest tests/ -v --tb=short -q 2>&1 || true)
    EXIT_CODE=$?
    
    if [ $EXIT_CODE -ne 0 ]; then
        # Tests failed — block the agent from stopping
        FAILURE_SUMMARY=$(echo "$TEST_OUTPUT" | tail -20)
        python3 -c "
import json, sys
summary = sys.argv[1]
print(json.dumps({
    'hookSpecificOutput': {
        'hookEventName': 'Stop',
        'decision': 'block',
        'reason': f'Tests are failing! Fix the failing tests before stopping.\n\nTest output:\n{summary}'
    }
}))
" "$FAILURE_SUMMARY"
        exit 0
    else
        echo "✅ All tests passing — agent may stop"
    fi
fi

exit 0
