---
name: pr-description
description: "Generate a clear, structured GitHub Pull Request description from git diff"

tools:
  - execute
  - read
---

# Pull Request Description Generator

Generate a professional GitHub Pull Request description for the current changes.

## Step 1: Gather Information

Run these commands to understand the changes:
```bash
git diff main...HEAD --stat
git diff main...HEAD
git log main...HEAD --oneline
```

Also check if there are related issues mentioned in commit messages.

## Step 2: Generate the PR Description

Use this exact format:

```markdown
## Summary
<!-- 2-3 sentences: WHAT changed and WHY -->

## Changes

### Added
- 

### Modified
- 

### Removed
- 

## Testing
<!-- How was this tested? -->
- [ ] Unit tests added/updated
- [ ] Integration tests added/updated
- [ ] Manually tested with curl/Postman

## Test Results
```
pytest tests/ -v
```
<!-- Paste test output here -->

## API Changes
<!-- If endpoints were added/modified, document them here -->
| Method | Path | Change |
|--------|------|--------|

## Breaking Changes
<!-- List any breaking changes, or write "None" -->

## Checklist
- [ ] Code follows project style guide (`.github/copilot-instructions.md`)
- [ ] All new functions have type annotations
- [ ] All new functions have docstrings
- [ ] No hardcoded secrets
- [ ] No `print()` statements
- [ ] Tests pass locally

## Related Issues
Closes #
```

## Rules
- Be specific — avoid generic phrases like "various improvements"
- If no breaking changes, explicitly write "No breaking changes"
- The Summary should be understandable by a non-technical reviewer
