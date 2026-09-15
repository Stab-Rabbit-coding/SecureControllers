# Python Django Backend Project Standards (Project Type — Layered)

> Stacked with the Python language template. Only Django-specific rules are listed here.

## Project Structure

- **Split settings by environment**: `settings/base.py`, `dev.py`, `prod.py`
- **One app per business domain**: each business area gets its own independent app

```text
apps/
  users/          # Users
    models.py
    views.py
    serializers.py
  orders/         # Orders
  products/       # Products
config/
  settings/
    base.py
    dev.py
    prod.py
  urls.py
```

## Code Conventions

- **Prevent N+1 ORM queries**: use `select_related()` and `prefetch_related()` for foreign keys and many-to-many relations
- **Querysets go in model Manager**: `User.objects.active()` is better than `User.objects.filter(is_active=True)`
- **Views: choose class-based views or DRF ViewSet consistently** — don't mix
- **Signals managed via receivers.py**: don't put `@receiver` decorators in models.py
- **Pagination configured globally**: use DRF's `DEFAULT_PAGINATION_CLASS` setting

## API Standards

### Unified Error Response Format

DRF global exception handler with a consistent error structure:

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

- code uses snake_case: `validation_error`, `not_found`, `permission_denied`, `authentication_failed`
- Field-level errors go in `details`; omit if no field-level errors

### Pagination I/O Convention

**Input**: `?page=1&page_size=20` (page starts at 1, page_size defaults to 20, max 100)

**Output** (custom format, configured in `DEFAULT_PAGINATION_CLASS`):

```json
{
  "items": [...],
  "total": 100,
  "page": 1,
  "page_size": 20,
  "total_pages": 5
}
```

If using DRF's built-in pagination, keep the default `count`/`next`/`previous`/`results` format.

## Toolchain

- **Logging**: structlog or standard logging (JSON format output)
- **Testing**: pytest (over unittest)
- **CORS**: use django-cors-headers
- **Static files (production)**: use whitenoise
- **Secret management**: use django-environ or environment variables — `.env` never committed to git
