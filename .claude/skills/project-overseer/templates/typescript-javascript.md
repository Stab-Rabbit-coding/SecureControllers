# TypeScript / JavaScript Project Standards

## Naming

- Variables/Functions: camelCase (`const userName`, `function fetchData()`)
- Classes/Components: PascalCase (`class UserService`, `const UserCard = () =>`)
- Files: kebab-case (`user-service.ts`, `auth-controller.ts`)
- Component files (.tsx/.jsx): PascalCase (`UserCard.tsx`, `LoginForm.tsx`)
- Constants: UPPER_SNAKE_CASE (`MAX_RETRY_COUNT`, `API_BASE_URL`)
- Types/Interfaces: PascalCase + optional I prefix (`UserProps`, `IUserService`?)

## Formatting

- Indentation: 2 spaces
- Semicolons: required
- Quotes: single quotes
- Line endings: LF
- Line width: 80 characters

## Code Style

- Null handling: null for explicit empty, undefined for unassigned
- Error handling: try/catch wrapping async functions, no .catch()
- Imports: named exports preferred, avoid default exports
- async/await: use consistently, no bare .then()
- Type declarations: `type` preferred, `interface` only for declaration merging
- `unknown` over `any`: use `unknown` for uncertain types, narrow with `typeof` / type guards, prohibit `as any`
- `never` for exhaustiveness checks: use `assertNever(value)` in switch default branches
- `import type` separated: use `import type { X } from './y'` separate from runtime imports
- Immutability: `const` preferred, never use `var`
- Readonly: use `ReadonlyArray<T>` / `readonly` for parameters that should not be mutated

## Framework Conventions (adjust per project stack)

- State management: (optional)
- CSS: (optional)
- API style: (optional)
- Component structure: (optional)

## Testing

- Framework: Vitest / Jest
- File naming: `*.test.ts`
- Test coverage: (optional)

## Project Structure (Generic)

```text
src/
  modules/      # Feature modules
  middleware/   # Middleware
  utils/        # Utility functions
  types/        # Type definitions
  app.ts
```
