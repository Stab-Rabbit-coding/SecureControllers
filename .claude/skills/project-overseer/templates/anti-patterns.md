# Common Anti-Patterns (Universal — Optional Layer)

> This template lists anti-patterns frequently seen in AI-generated code.
> Designs marked with 🚫 should be actively avoided during generation.

---

## 🔴 CRITICAL — Must Avoid

### 🚫 1. Multi-Responsibility File Bloat

**Symptom**: A single 500+ line file containing route definitions, database queries, JSON serialization, and error handling all mixed together

**Should do**:

- One file, one primary responsibility
- Route files: routes + parameter binding only — no business logic
- Business logic in the `service` layer, data access in `repository` / `DAO` layer

### 🚫 2. Shotgun try/catch

**Symptom**:

```python
try:
    user = get_user()       # might raise 404
    order = get_order()     # might raise 404
    result = process(order) # might raise business exception
except Exception:
    return {"error": "something wrong"}
```

**Should do**: Catch each failure-prone operation separately, or distinguish by exception type. Don't let `process()` errors swallow `get_user()` errors.

### 🚫 3. God Function

**Symptom**: A 50+ line function doing validation, computation, persistence, logging, and notification all at once

**Should do**: Single responsibility — one function, one level of abstraction. If you need comments like "Step 1... Step 2... Step 3..." inside a function, it's time to split.

### 🚫 4. Premature Abstraction

**Symptom**: Having only one `UserService` implementation but already extracting `IUserService`, a factory, a registry, and decorators

**Should do**: **Abstract only after 3 repetitions**. One implementation with one consumer → use concrete types. Refactor to interfaces when mock testing is actually needed.

### 🚫 5. Deep Nesting

**Symptom**: if inside if inside if — exceeding 3 levels

```js
if (user) {
  if (user.isActive) {
    if (order) {
      if (order.status === 'paid') {
```

**Should do**: **Early returns / guard clauses** — invert each condition and return early.

---

## 🟡 HIGH — Strongly Avoid

### 🚫 6. Ghost State

**Symptom**:

- Variable assigned but never read
- `isLoading = true` set but never reset to `false`
- Function parameters declared but unused

**Should do**: Don't write dead code. AI-generated code must be checked for unused variables.

### 🚫 7. Implicit Dependencies

**Symptom**: Functions that directly `new HttpClient()` / `new Database()` internally instead of receiving dependencies via parameters

```js
async function getUsers() {
  const db = new Database()  // ❌ Who calls this? Where's the connection config?
  return db.query(...)
}
```

**Should do**: Inject dependencies via parameters — let the caller decide the concrete implementation.

### 🚫 8. Null Neglect

**Symptom**: Assuming `findUser()` always returns a user, `getConfig()` always returns config, `parseJSON()` always succeeds

**Should do**: Every optional return value must handle `null`/`None`/`undefined`/`Optional`. No "that won't happen" assumptions — if it truly shouldn't happen, use `assert`/`unwrap` to declare it explicitly.

### 🚫 9. String Concatenation for Structured Data

**Symptom**: Building SQL / HTML / URL / JSON with string interpolation

```python
query = f"SELECT * FROM users WHERE id = {user_id}"   # ❌
html = f"<div class={cls}>{content}</div>"             # ❌
```

**Should do**: SQL → parameterized queries / ORM / query builder; HTML → template engine; URL → URL builder library; JSON → serializer.

### 🚫 10. Copy-Paste Code

**Symptom**: Similar logic appearing 3+ times, each with one variable name changed

**Should do**: Extract the repeated part into a function or loop. AI is especially prone to this because "write something similar" costs less than "abstract".

### 🚫 11. Tests Dependent on External State

**Symptom**: Tests that need specific database records, file existence, environment variables, or network access to pass

```python
def test_get_user():
    user = User.objects.get(id=123)  # ❌ Does id=123 exist in the database?
```

**Should do**: Tests create their own data via mock / factory / fixture — never depend on external state. Don't share mutable state between tests.

### 🚫 12. Hardcoded Configuration

**Symptom**: URLs, ports, secrets, timeouts written directly in code

```python
API_URL = "http://localhost:8080"      # ❌
TIMEOUT = 30                            # ❌
```

**Should do**: All environment-dependent values come from environment variables / config files — zero hardcoded values in code.
