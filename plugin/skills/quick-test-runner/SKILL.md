---
name: quick-test-runner
description: "Runs the TaskManager test suite, interprets results, and suggests fixes for failing tests. One command to test everything."
---

# Quick Test Runner Skill

Run the full test suite and interpret the results intelligently.

## Step 1: Run All Tests
```bash
pytest tests/ -v --tb=short 2>&1
```

## Step 2: Parse Results
Categorise results into:
- ✅ **Passed**: working correctly
- ❌ **Failed**: test assertion failed — code bug likely
- 💥 **Error**: test couldn't run — import/setup error
- ⚠️ **Warning**: deprecation or configuration issues

## Step 3: For Each Failure, Diagnose

Read the failing test file:
- What is the test checking?
- What did it get vs. what did it expect?
- Is the bug in the test or the implementation?

Trace the code path in `src/services/` or `src/api/`.

## Step 4: Report and Fix

```markdown
## Test Results

**Passed:** {n} | **Failed:** {n} | **Errors:** {n}

### Failures

#### {test_name}
**Root cause:** {one sentence}
**Fix:** {concrete code change}

### Summary
{overall health statement}
```

If there are ≤3 failures, offer to fix them immediately.
If there are >3 failures, summarise the pattern and ask how to proceed.
