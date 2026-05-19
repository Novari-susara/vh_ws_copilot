---
name: new-endpoint
description: "Scaffold a complete new FastAPI endpoint with router, service, Pydantic models, and tests"
mode: agent
tools:
  - read
  - write
  - edit
  - terminal
---

# New FastAPI Endpoint Scaffold

You are scaffolding a new endpoint for the TaskManager API.

## Before You Start
Read these files to understand existing patterns:
- `src/api/tasks.py` — router pattern to follow
- `src/services/task_service.py` — service pattern to follow  
- `src/models/schemas.py` — Pydantic model patterns to follow
- `tests/unit/test_task_service.py` — test patterns to follow

## What to Create

For the new resource named **{resource_name}** (replace with actual name), create:

### 1. Pydantic Models → `src/models/schemas.py`
Add to the existing file:
```python
class {Resource}Base(BaseModel):
    # core fields here

class {Resource}Create({Resource}Base):
    # creation-only fields

class {Resource}Update(BaseModel):
    # all optional for PATCH

class {Resource}Response({Resource}Base):
    id: str
    created_at: datetime
    model_config = {"from_attributes": True}
```

### 2. Service → `src/services/{resource}_service.py`
Implement:
- `list_{resources}()` with filter params
- `create_{resource}(data, creator_id)` 
- `get_{resource}(id)` → returns None if not found
- `update_{resource}(id, data)` → returns None if not found
- `delete_{resource}(id)` → returns bool

### 3. Router → `src/api/{resources}.py`
Implement all CRUD endpoints:
- `GET /` — list with filters
- `POST /` — create (201)
- `GET /{id}` — get one (404 if not found)
- `PATCH /{id}` — partial update
- `DELETE /{id}` — delete (204)

### 4. Register Router → `src/main.py`
Add: `app.include_router({resource}s_router, prefix="/api/v1/{resources}", tags=["{resources}"])`

### 5. Tests → `tests/unit/test_{resource}_service.py`
Cover: create, get (found + not found), update, delete, list with filters

### 6. Integration Tests → `tests/integration/test_{resources}_api.py`
Cover: create, read, update, delete, 401 without auth, 404

## After Scaffolding
Run tests to verify everything works:
```bash
pytest tests/ -v -k "{resource}"
```

Fix any failures before finishing.
