---
applyTo: "tests/**/*.py"
---

# Test File Instructions
These instructions apply ONLY to files inside the `tests/` directory.

## Test Structure
- All test classes inherit from nothing (plain classes, not unittest.TestCase)
- Group related tests: `class TestCreateX:`, `class TestUpdateX:`, `class TestDeleteX:`
- One assert per test is preferred; multiple asserts only when they test ONE behaviour
- Always use `@pytest.mark.asyncio` for async tests

## Fixtures
- Place shared fixtures in `conftest.py` at the appropriate level
- Name fixtures after what they provide: `auth_headers`, `sample_task`, `client`
- Use `autouse=True` only for cleanup fixtures (clearing stores, resetting state)

## Assertions
- Prefer specific assertions: `assert resp.status_code == 201` over `assert resp.ok`
- Always assert the response body, not just the status code
- For list responses, assert both length AND content

## What to Test
- Happy path: valid input, expected output
- Error path: missing resource → 404, invalid auth → 401/403
- Edge cases: empty lists, boundary values, None fields
- Never test implementation details — test observable behaviour only
