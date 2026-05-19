---
name: api-doc-generator
description: "Generates comprehensive API documentation from FastAPI source code. Creates endpoint reference docs, request/response examples, and curl snippets. Saves to docs/api/."
---

# API Documentation Generator Skill

You generate clear, accurate API documentation directly from FastAPI source code.
Never invent or assume API behaviour — always read the source first.

## Step 1: Discover All Endpoints

Read all router files:
```python
# Files to read:
src/api/tasks.py
src/api/users.py  
src/api/auth.py
src/models/schemas.py  # for request/response models
```

## Step 2: Extract for Each Endpoint
For each `@router.get/post/patch/delete`:
- HTTP method + path
- Query parameters (from `Query()` annotations)
- Request body model (from function parameter types)
- Response model (from `response_model=`)
- Status codes (default + explicit raises)
- Auth requirement (has `Depends(get_current_user)`?)

## Step 3: Generate Documentation

### File Structure to Create
```
docs/api/
├── README.md          (API overview + base URL)
├── authentication.md  (auth flow + token usage)
├── tasks.md           (task endpoints)
├── users.md           (user endpoints)
└── errors.md          (error codes reference)
```

### Endpoint Documentation Template
```markdown
## {METHOD} {path}

{description from docstring}

**Authentication:** {Required / Not required}

### Request

**Query Parameters:**
| Parameter | Type | Required | Default | Description |
|-----------|------|----------|---------|-------------|

**Request Body:**
```json
{example JSON}
```

### Response

**{STATUS_CODE} — {status_name}**
```json
{example JSON response}
```

### Error Responses
| Status | Condition |
|--------|-----------|
| 401 | Missing or invalid Bearer token |
| 404 | Resource not found |

### Example (curl)
```bash
curl -X {METHOD} http://localhost:8000{path} \
  -H "Authorization: Bearer $TOKEN" \
  -H "Content-Type: application/json" \
  -d '{example body}'
```
```

## Step 4: Generate Example Values

Use realistic example data:
- IDs: `"550e8400-e29b-41d4-a716-446655440000"`
- Emails: `"alice@example.com"`
- Dates: `"2025-01-15T10:30:00Z"`
- Task titles: `"Implement OAuth2 login"`, `"Fix pagination bug"`

## Step 5: Cross-Reference

After generating, verify:
- Every endpoint is documented
- All Pydantic fields are in the request/response tables
- Error codes match what's in the source
- Curl examples would actually work

## Output
Save generated docs to `docs/api/` directory.
Update `docs/api/README.md` with a table of contents linking to each file.
