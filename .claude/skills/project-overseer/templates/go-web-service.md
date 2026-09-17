# Go Web Service Project Standards (Project Type — Layered)

> Stacked with the Go language template. Only Go Web service-specific rules are listed here.

## Error Handling

- **Wrap errors with `%w`**: `fmt.Errorf("context: %w", err)` preserves the error chain so `errors.Is()` and `errors.As()` can traverse it

## Project Structure

```text
cmd/
  server/main.go     # Entry point
internal/
  handler/           # HTTP handlers
  service/           # Business logic
  repository/        # Data access
  middleware/        # Middleware
  model/             # Data structures
pkg/                 # Reusable public packages
config/
  config.go
```

## Interfaces & Dependencies

- **Abstract dependencies with interfaces**: `type UserRepository interface` — enables mocking in unit tests
- **Middleware chain convention**: logging → recovery → auth → router

## API Standards

### Unified Response Format

All responses (including errors) use a consistent structure:

```json
{
  "code": 0,
  "message": "ok",
  "data": { ... }
}
```

- `code`: 0 indicates success, non-zero indicates a specific error code
- `message`: human-readable description
- `data`: payload on success, `null` on failure
- Field-level errors return `{ "field": "email", "error": "invalid format" }` within `data`

### Pagination I/O Convention

**Input**: `?page=1&limit=20` (page starts at 1, limit defaults to 20, max 100)

**Output**:

```json
{
  "code": 0,
  "message": "ok",
  "data": {
    "items": [...],
    "total": 100,
    "page": 1,
    "limit": 20,
    "total_pages": 5
  }
}
```

## Operations & Toolchain

- **Graceful shutdown**: use `signal.NotifyContext` to catch SIGTERM/SIGINT, complete in-flight requests before exiting
- **Structured logging**: slog / zerolog in JSON format, include `request_id` field
- **Request ID across the full chain**: generate or propagate X-Request-ID via middleware
- **Health check endpoint**: `GET /health` returns DB connection status
- **API version prefix**: `/v1/users`
- **Testing with httptest**: use `net/http/httptest` for handler tests — no need to start a real server
