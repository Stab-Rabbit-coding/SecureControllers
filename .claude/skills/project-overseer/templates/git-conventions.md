# Git Conventions (Universal — Optional Layer)

---

## Commit Format (Conventional Commits)

```text
<type>(<scope>): <short description>

<optional detailed explanation>
```

### type Values

| type | Meaning |
| --- | --- |
| `feat` | New feature |
| `fix` | Bug fix |
| `chore` | Build, config, tooling changes |
| `refactor` | Code refactoring (no bug fix, no feature) |
| `docs` | Documentation |
| `test` | Tests |
| `style` | Code formatting (no logic change) |
| `perf` | Performance improvement |

### scope Examples

`feat(auth): add login endpoint`, `fix(orders): handle empty cart`

### Rules

- Description uses imperative mood: `feat: add login` ✅ / `feat: added login` ❌
- No capital first letter, no trailing period
- One commit = one logical change — don't mix changes in the same commit
- Breaking changes: `feat!: drop v1 API`

---

## Branch Naming

```text
<type>/<short-kebab-case-description>

Examples: feat/user-login, fix/order-overflow, chore/upgrade-deps
```

- All lowercase, words separated by hyphens
- One branch = one issue / feature point

---

## PR Standards

- PR title format: same as commit (type + short description)
- PR body includes:
  - Summary of changes
  - How to verify / test
  - Frontend changes → attach screenshots
- **Single PR — no more than 400 lines changed** (auto-generated code excluded)
- Breaking changes: add `!` to the title

---

## Prohibited Behavior

- ❌ Never push directly to `main` / `master` (must go through review)
- ❌ Never commit `node_modules/`, `.env`, build artifacts
- ❌ Never commit large files (use Git LFS for files over 5MB)
- ❌ Never commit merge conflict markers (`<<<<<<<`, `=======`, `>>>>>>>`)
- ❌ Never commit meaningless messages (`fix`, `update`, `asd`, `wip`)
