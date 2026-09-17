# Go Project Standards

## Naming

- Variables/Functions: camelCase internal, PascalCase exported (`getUser()`, `GetUser()`)
- Package names: lowercase singular (`user`, `service`)
- Files: snake_case.go (`user_service.go`)
- Interface names: method name + er suffix (`Reader`, `Writer`)

## Formatting

- Use gofmt/gopls standard formatting (no alternatives)
- Indentation: tab
- Line width: no hard limit

## Code Style

- Error handling: return error, don't panic (except during startup)
- Error wrapping: use `fmt.Errorf("context: %w", err)` with context
- Logging: use structured logging (zerolog/slog), never fmt.Print
- Concurrency: use errgroup to manage goroutines, never bare `go`
- Configuration: use environment variables + viper, never global variables

## Testing

- Framework: testing standard library
- File naming: `*_test.go`
- Table-driven tests: preferred

## Project Structure

```text
project/
  cmd/          # Entry points
  internal/     # Private packages
  pkg/          # Exportable packages
  api/          # API definitions
  config/       # Configuration
```
