---
applyTo: "src/api/*.py"
---

# API Router File Instructions
These instructions apply ONLY to router files inside `src/api/`.

## Router Pattern
- Always use `APIRouter()` — never put routes directly on `app`
- Import and use the service via `Depends()` — never instantiate directly in route
- Keep route functions thin: validate → call service → return/raise
- Never put business logic in router functions — it belongs in the service layer

## Response Models
- Always specify `response_model=` on every endpoint
- Use `response_model_exclude_unset=True` for PATCH endpoints
- List endpoints: `response_model=List[XResponse]`

## HTTP Status Codes (use `fastapi.status` constants)
- GET single: 200 (default)
- GET list: 200 (default)  
- POST (create): `status.HTTP_201_CREATED`
- PATCH (update): 200 (default)
- DELETE: `status.HTTP_204_NO_CONTENT`
- Not found: `status.HTTP_404_NOT_FOUND`
- Conflict: `status.HTTP_409_CONFLICT`
- Unauthorized: `status.HTTP_401_UNAUTHORIZED`
