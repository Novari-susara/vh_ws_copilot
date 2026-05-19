---
name: debug-test
description: "Systematically debug a failing pytest test — reads the test, traces the code path, identifies the root cause, and proposes a fix"
mode: agent
tools:
  - read
  - search
  - terminal
  - edit
---

# Debug Failing Test

Systematically debug a failing test without guessing.

## Step 1: Run the Failing Test
```bash
pytest {test_path} -v --tb=long -s
```
Capture the FULL output including the traceback.

## Step 2: Read the Test
Read the test file and understand:
- What is this test trying to verify?
- What inputs is it providing?
- What output is it expecting?
- What fixtures does it use?

## Step 3: Trace the Code Path
Follow the execution path from the test:
- What function/method is called?
- Read that function's source
- What does it call? Read those too
- Where does the actual vs expected diverge?

## Step 4: Form a Hypothesis
State clearly:
- "The test expects X"
- "The code actually does Y"  
- "This is because Z"

Do NOT guess. Do NOT fix before you understand.

## Step 5: Verify the Hypothesis
Before fixing, verify your hypothesis:
```bash
# Add a temporary print to verify (remove after)
pytest {test_path} -v -s --tb=short
```

## Step 6: Fix
Apply the minimal fix:
- Fix the code if the code is wrong
- Fix the test if the test expectation is wrong
- Fix the fixture if the test setup is wrong

## Step 7: Verify the Fix
```bash
pytest {test_path} -v
pytest tests/ -v  # make sure nothing else broke
```

## Output Format
Report:
1. **Root Cause:** {one sentence}
2. **Fix Applied:** {what was changed}
3. **Verification:** {test output showing green}
