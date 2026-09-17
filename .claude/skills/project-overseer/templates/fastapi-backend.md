# Python FastAPI Backend Project Standards (Project Type — Layered)

> Stacked with the Python language template. Only FastAPI-specific rules are listed here.

## Architecture Conventions

- **Synchronous I/O: do NOT use async def**: If using synchronous libraries (SQLAlchemy sync, requests), use regular `def` — otherwise the event loop will block
- **Pydantic v2 input validation is required**: use Pydantic schemas for all requests/responses, never raw dicts
- **Dependency injection over repeated code**: use `Depends()` for shared logic (auth, DB session, pagination)
- **Dependency caching is per-request**: calling the same `Depends()` multiple times in one request only executes once (auto-cached), but is not shared across requests
- **Sensitive data must not leak in Pydantic `model_dump()`**: use `response_model_exclude` or `SecretStr`
- **Async DB driver**: use asyncpg + SQLAlchemy async in production, never synchronous DB drivers
- **ValueError may be swallowed by Pydantic**: inherit custom exceptions from `HTTPException`, don't raise `ValueError` directly

## Project Structure

```text
src/
  auth/
    router.py      # Routes
    schemas.py     # Pydantic schemas
    models.py      # DB models
    service.py     # Business logic
    dependencies.py
  posts/
    ...
  config.py
  main.py
```

## API Standards

### Unified Error Response Format

All error responses are defined with Pydantic schemas using a consistent structure:

```json
{
  "error": {
    "code": "validation_error",
    "message": "Request parameter validation failed",
    "details": [
      { "field": "email", "message": "Invalid email format" }
    ]
  }
}
```

- code uses snake_case: `validation_error`, `not_found`, `unauthorized`, `internal_error`
- Field-level errors go in `details`; omit if no field-level errors

### Pagination I/O Convention

**Input**: `?page=1&limit=20` (page starts at 1, limit defaults to 20, max 100)

**Output**:

```json
{
  "items": [...],
  "total": 100,
  "page": 1,
  "limit": 20,
  "total_pages": 5
}
```

Pagination logic extracted into a reusable `Depends()`.

## Toolchain

- **Database migration**: Alembic (`alembic revision --autogenerate`)
- **Logging**: structlog or loguru
- **Testing**: pytest + httpx AsyncClient
- **Config management**: Pydantic Settings (`from pydantic_settings import BaseSettings`), no scattered `os.getenv`
- **Lint/format**: ruff
- **Health check**: `GET /health`
- **CORS**: specify explicit `allowed_origins`, never `["*"]`
- **Database table naming**: all lowercase with underscores (`user_accounts`)
