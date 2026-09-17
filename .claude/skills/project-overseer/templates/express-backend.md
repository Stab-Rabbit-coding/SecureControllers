# Express / Fastify Backend Project Standards (Project Type — Layered)

> Stacked with the TS/JS language template. Only backend-specific rules are listed here.

## Architecture Conventions

- **Middleware order convention**: Security middleware (CORS, helmet, rate-limit) outermost → routes → error handling last
- **Error-handling middleware must be written**: 4 parameters `(err, req, res, next)`
- **Async route errors must be caught**: Express 4 does not auto-catch async errors — use `express-async-errors` or wrap with `catch(fn)`
- **Fastify uses Schema serialization**: `reply.send()` auto-filters by schema — don't manually `JSON.stringify`

## Project Structure

```text
src/
  modules/
    users/          # Users module
      routes.ts
      controller.ts
      service.ts
      validation.ts
  middleware/
  utils/
  app.ts
```

- **Organize by feature module**, not by file type
- **Fastify uses plugin encapsulation**: plugins have isolated scopes, no global pollution

## API Standards

### Unified Error Response Format

All error responses use a consistent JSON structure:

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
- Error-handling middleware outputs this format uniformly

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

## Toolchain

- **Structured logging**: use pino / winston, never console.log
- **Input validation**: use zod / joi — never trust `req.body`
- **Health check endpoint**: `GET /health` returns database and service status
- **Global request ID**: assign a unique ID to each request, correlate with logs
