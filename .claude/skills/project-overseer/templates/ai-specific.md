# AI Behavior Constraints (Universal — Always Layer)

> This template governs the AI agent's behavior patterns during code generation, not code style.
> Always layered into any project's project-standards.md.

---

## 🔴 CRITICAL — Must Follow

### 1. File Size Limit

- **Single source file: max 400 lines** (test files: max 500 lines)
- Exceed the limit → split into multiple files by functional responsibility
- Exceptions: configuration files, auto-generated migration files, data/constant definitions

### 2. Read Before Write

- Before modifying an existing file, **read it in full first** — don't overwrite from "memory"
- Newly generated code must match the project's **existing code style exactly** (naming, indentation, brace placement, blank line habits)
- Do not insert code blocks unrelated to the file's responsibility into existing files — create a new file instead

### 3. State Coverage Discipline

- **Every API endpoint / function must cover**: success path, error path, empty/zero values, edge cases
- Every branch must have an else/fallback — no implicit uncovered states
- When unable to handle: return error, never panic / unwrap / crash

### 4. Abstraction Restraint

- **Extract functions/classes/interfaces only after 3+ repetitions** of the same logic — no premature abstraction
- Don't extract interfaces for dependencies that don't need mocking yet — use concrete types, refactor when needed
- **One file, one primary responsibility**: no "while you're at it" additions to a file

### 5. No Magic Values

- All literal values (numbers, strings) must be replaced with named constants or enums
- Exceptions: `0`/`1` for array indexing, `""` for empty string initialization, `true`/`false` boolean literals

### 6. Comment Discipline

| Write (Why) | Don't Write (What) |
| --- | --- |
| Why this design was chosen | `// increment by 1` |
| Complex business logic explanation | `// get user` |
| Known pitfalls and limitations | JSDoc repeating the type signature |
| Reason behind a TODO | Code that is self-explanatory |

- Code should be self-documenting — use comments for "why", not "what"

### 7. Reference Discipline

- Before referencing an existing module in a new file, verify the path exists
- When the project defines path aliases (`@/`), prefer them
- **Unused import / using / use statements must be removed** — no dead references

---

## 🟡 HIGH — Strongly Recommended

### 8. Test Structure

- **AAA Pattern**: Arrange → Act → Assert (separated by blank lines)
- Test naming: `should_<expected_behavior>_when_<condition>` format
- Each test covers exactly one behavior — no "while we're at it" extras
- Test data via factory functions or inline — never depend on external state

### 9. Error Priority

| Error Source | Handling |
| --- | --- |
| User input errors | Return 4xx with clear error message |
| Business logic errors | Return serialized business error codes |
| Infrastructure errors (DB/network) | Retry or degrade — never expose directly to the user |

### 10. Logging Discipline

- No temporary debug logs in business logic (`console.log`/`print`/`println`)
- Error logs must contain actionable context: request ID, parameter values (sanitized), failure reason
- Log levels: business events → info, potential issues → warn, actual failures → error

---

## 🟢 Intermediate (Selected)

### 11. Naming Consistency

- The same concept always uses the same term across the project: `user`/`User` should not be aliased as `person`/`account`
- Abbreviations are fixed: don't mix `id`/`ID`/`Id`, `url`/`URL`/`Url`
