# Python Project Standards

## Naming

- Variables/Functions: snake_case (`user_name`, `get_user_data()`)
- Classes: PascalCase (`class UserService`)
- Constants: UPPER_SNAKE_CASE (`MAX_RETRY_COUNT`)
- Files: snake_case.py (`user_service.py`)
- Private: prefix `_` (`_internal_helper()`)

## Formatting

- Indentation: 4 spaces
- Line width: 88 characters (Black default)
- Formatter: Ruff / Black
- Import sorting: isort / Ruff

## Code Style

- Type annotations: required for all function parameters and return values
- Error handling: use custom exception classes, never bare `raise Exception`
- Logging: use the `logging` module, never `print`
- Async: asyncio + async/await consistently

## Testing

- Framework: pytest
- File naming: `test_*.py`
- Test coverage: (optional)

## Project Structure

```text
project/
  src/
    __init__.py
    main.py
    services/
    models/
  tests/
    conftest.py
```
