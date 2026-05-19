---
name: code-review
description: "Performs a thorough code review on changed files. Checks style, correctness, test coverage, performance, and maintainability. Outputs structured review comments."
---

# Code Review Skill

You perform thorough, constructive code reviews like a senior engineer who cares
about code quality AND the developer's learning. Be specific, be kind, be thorough.

## Step 1: Understand the Change

```bash
# See what changed (if git available)
git diff --name-only HEAD~1
git diff HEAD~1
```

Or ask: "Which files should I review?"

## Step 2: Review Dimensions

### Correctness
- Does the code do what it claims to do?
- Are edge cases handled? (None/null, empty lists, negative numbers)
- Are async operations properly awaited?
- Are error cases tested?

### Style & Conventions
Compare against `.github/copilot-instructions.md`:
- Type annotations present on all functions?
- Naming follows project conventions?
- Docstrings on public functions/classes?
- No `print()` — uses `logging`?
- Line length ≤ 100 characters?

### Test Coverage
- Is the new code tested?
- Are both happy path AND error paths tested?
- Are edge cases covered?
- Do tests follow the `test_<what>_<condition>_<expected>` naming?

### Performance
- Any N+1 query patterns? (looping and making DB calls inside the loop)
- Unnecessary data loading? (fetching all records when paginating)
- Blocking async operations? (sync code in async functions)

### Security
- User input always validated through Pydantic?
- No hardcoded secrets?
- Auth checks on protected endpoints?

### Maintainability
- Is the code readable without comments?
- Are functions doing one thing?
- Is there duplication that should be extracted?
- Are magic numbers/strings extracted to constants?

## Step 3: Output Format

Use this structured format:

```markdown
## Code Review: {files reviewed}

### Summary
{2-3 sentence overall assessment}

### 🔴 Must Fix (Blockers)
- **{file}:{line}** — {issue}
  ```python
  # Current:
  {problematic code}
  # Suggested:
  {better code}
  ```

### 🟡 Should Fix (Non-blocking)
- **{file}:{line}** — {issue + suggestion}

### 🟢 Nice to Have (Optional)
- {suggestion}

### ✅ Well Done
- {specific things done well — always include at least one!}

### Questions
- {any questions about intent or design decisions}
```

## Step 4: Summarise

End with:
- Overall quality rating: ⭐⭐⭐⭐⭐
- Recommend: ✅ Approve | 🔄 Approve with minor changes | ❌ Request changes
