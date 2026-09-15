# Rust Project Standards

## Naming

- Variables/Functions: snake_case (`let user_name`, `fn get_user()`)
- Types/Traits: PascalCase (`struct User`, `trait UserRepository`)
- Constants: UPPER_SNAKE_CASE (`MAX_RETRY_COUNT`)
- Files: snake_case.rs (`user_service.rs`)
- Modules: snake_case (`mod user_service`)

## Formatting

- Use rustfmt standard formatting
- Indentation: 4 spaces
- Line width: 100 characters

## Code Style

- Error handling: use `Result<T, E>`, never `unwrap()` (except in main and tests)
- Error libraries: anyhow + thiserror
- Cloning: prefer references `&T`, minimize `clone()`
- Async: tokio + async/await
- Logging: tracing / log consistently
- Type inference: annotate complex types explicitly, omit for simple types

## Testing

- Framework: built-in `#[cfg(test)]` + `#[test]`
- Integration tests: tests/ directory
- File naming: write `#[cfg(test)] mod tests` at the end of the same file

## Project Structure (Generic)

```text
project/
  src/
    main.rs
    lib.rs
    routes/
    models/
    handlers/
    db/
  tests/
  Cargo.toml
```
