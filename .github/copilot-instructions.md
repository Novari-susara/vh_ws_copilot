# TaskManager API — GitHub Copilot Custom Instructions
# Applied automatically to EVERY chat request in this project.
# This file lives at: .github/copilot-instructions.md

## Project Context
This is a Python FastAPI REST API called "TaskManager". It provides task and user
management endpoints with JWT authentication. The codebase uses:
- **FastAPI** for the web framework
- **Pydantic v2** for data validation and serialization
- **pytest + pytest-asyncio** for testing
- **JWT** (PyJWT) for authentication
- **In-memory storage** (would be asyncpg + PostgreSQL in production)

## Python Code Style
- Python 3.11+ syntax — use `match/case`, `X | Y` union types, `tomllib`
- Type annotations on ALL function parameters and return types (no exceptions!)
- `async/await` everywhere — this is an async codebase; no sync DB calls
- Use `logging.getLogger(__name__)` — never `print()` statements
- f-strings for string formatting (never `%` or `.format()`)
- Maximum line length: 100 characters
- Imports: stdlib → third-party → local (blank line between groups)

## Naming Conventions
- `snake_case` → variables, functions, methods, module names
- `PascalCase` → classes, Pydantic models, exceptions
- `UPPER_SNAKE_CASE` → constants and environment variable names
- `_leading_underscore` → "private" module-level variables (e.g. `_tasks = {}`)
- Router files: noun-plural (e.g. `tasks.py`, `users.py`)
- Service files: noun + `_service.py` (e.g. `task_service.py`)

## API Design Rules
- All endpoints require authentication EXCEPT `/health` and `/api/v1/auth/login`
- Always use `Depends(get_current_user)` for protected routes
- Return `404` for missing resources, never `200` with empty body
- Use `status.HTTP_201_CREATED` for POST, `204` for DELETE
- Partial updates use `PATCH` with `exclude_unset=True` on the update model
- Filter parameters go in `Query()` annotations, not request body

## Error Handling Rules
- Wrap all `async` service calls in try/except where errors are expected
- Raise `HTTPException` in router layer, never in service layer
- Service layer returns `None` for not-found, raises for unexpected errors
- Always log errors with `logger.error("message", exc_info=True)`

## Testing Rules
- Every public function/method must have at least one test
- Use `pytest.fixture` for shared setup, never repeat setup code
- Test naming: `test_<what>_<condition>_<expected_result>`
- Use `autouse=True` fixtures to clear in-memory stores between tests
- Group tests in classes: `class TestCreateTask:`, `class TestGetTask:`

## Security Rules (IMPORTANT)
- NEVER log or return passwords, tokens, or sensitive data
- NEVER store plaintext passwords — always hash (bcrypt in production)
- Validate all user input via Pydantic models before use
- Environment variables for all secrets (SECRET_KEY, DATABASE_URL, etc.)
- Check the OWASP Top 10 for any auth, input handling, or data exposure code

## Comments and Documentation
- Docstrings on all modules, classes, and public functions (Google style)
- Comment the "why", not the "what" — code should be self-documenting
- Mark demo/stub code with `# TODO: Replace with real implementation`
- Mark security-critical sections with `# SECURITY:` comment prefix
