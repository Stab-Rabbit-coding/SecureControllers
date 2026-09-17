# Testing Standards (Universal — Optional Layer)

> Cross-language testing conventions, not tied to any specific testing framework.

---

## Test Structure

### AAA Pattern

Each test function is organized into three phases, **separated by blank lines**:

```text
Arrange  → Set up test data and preconditions
Act      → Execute the operation under test
Assert   → Verify the results
```

```python
# ✅

def test_calculate_total():
    items = [Item(price=10), Item(price=20)]
    cart = Cart(items)

    total = cart.calculate_total()

    assert total == 30
```

```python
# ❌ All mixed together — can't tell what's being tested at a glance

def test_calculate_total():
    items = [Item(price=10), Item(price=20)]
    cart = Cart(items)
    total = cart.calculate_total()
    assert total == 30
```

### Test Naming

```text
should_<expected_behavior>_when_<condition>
```

| ✅ Good names | ❌ Bad names |
| --- | --- |
| `should_return_400_when_email_invalid` | `test_email` |
| `should_throw_when_user_not_found` | `test_user_not_found_works` |
| `should_create_order_when_payment_success` | `test_create_order` |

- Use one language consistently (all English or all Chinese) — **don't mix**
- The name is documentation — someone should know what's being tested without reading the body

### Single Behavior Principle

- **Each test covers exactly one behavior**
- One test can have multiple assertions, but all assertions verify different aspects of the same thing
- Don't "also test" something else in the same test

---

## Testing Principles

### Independence & Order

- **Tests must not have order dependencies**: any single test must pass when run alone
- Each test cleans up its own side effects (created data, files, DB records)
- Tests don't share mutable state

### Mock Boundaries

- **Mock external boundaries**: database, network requests, file system, external APIs
- **Don't mock internal logic**: don't mock a service within the same project to test a controller — use integration tests instead
- Verification: only verify necessary interactions — don't verify implementation details ("how many times was it called, what arguments")

### Test Data

- Use **factory functions** or inline data — never share mutable fixtures globally
- Don't depend on specific database record IDs
- Date/time tests: use fixed values or time freezing — never assert against `now()`

### Coverage

| Type | What to Cover |
| --- | --- |
| **Unit tests** | Core business logic, edge cases, error paths |
| **Integration tests** | Full API endpoint flow (request → response), database interactions |
| **Contract tests** | Detect changes to external API return value structures |

### Unit vs Integration

- **Unit tests don't start servers or connect to databases**
- **Integration tests start a real server + test database (or in-memory DB)**
- Distinction: unit tests verify "is the logic correct", integration tests verify "does everything work together"

---

## Prohibited

- ❌ Never use try/catch in tests to verify exceptions — use the framework's `assertRaises` / `expect.toThrow` / equivalent
- ❌ Never use `print` / `console.log` to "check if results look right"
- ❌ Never write tests that always pass (`assert True`)
- ❌ Never write tests that only run on a specific machine
- ❌ Never let tests access production databases or APIs
