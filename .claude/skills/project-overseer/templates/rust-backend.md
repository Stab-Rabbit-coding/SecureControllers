# Rust Backend Project Standards (Project Type — Layered)

> Stacked with the Rust language template. Only Rust Web service-specific rules are listed here.

## Architecture Conventions

- **Do not hold locks across `.await` points in async functions**: `MutexGuard` cannot cross `.await` — use `tokio::sync::Mutex` instead of `std::sync::Mutex`
- **Pass request context via dependency injection**: use State extractors (Axum) or Data (Actix), never global statics
- **Define errors with `thiserror`**: auto-implements `Display` and `Error`, returns structured errors to the client
- **No string concatenation for SQL queries**: use sqlx's `query!()` macro or SeaORM to prevent SQL injection
- **Sensitive data: use `secrecy::SecretString`**: prevents passwords/tokens from leaking in logs and core dumps

## Project Structure

```text
src/
  main.rs
  lib.rs
  routes/
    mod.rs
    users.rs
  models/
    mod.rs
    user.rs
  handlers/
    mod.rs
    user_handler.rs
  db/
    mod.rs
    migrations/
```

## API Standards

### Unified Response Format

Use a generic `ApiResponse<T>` struct for all responses:

```json
{
  "code": 0,
  "message": "ok",
  "data": { ... }
}
```

- `code`: 0 for success, non-zero for error codes
- `message`: human-readable description
- `data`: payload on success, `null` on failure
- Error types defined via `thiserror` enum, auto-mapped to code

### Pagination I/O Convention

**Input**: `?page=1&limit=20` (page starts at 1, limit defaults to 20, max 100. Use reusable `Pagination` extractor)

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

- **Logging with tracing**: structured logging + span tracing, natively integrated with tokio
- **Graceful shutdown**: `shutdown_signal()` listens for termination signals, completes in-flight requests before exiting
- **Middleware order**: tracing → CORS → compression → auth → router
- **Use tower middleware layers**: Axum is built on tower — reuse `tower-http` middleware
- **Health check**: `GET /health` returns dependency status
- **API version**: route prefix `/v1/`
- **Integration tests in tests/**: end-to-end tests use `reqwest` or `axum_test`
