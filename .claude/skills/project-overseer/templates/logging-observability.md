# Logging & Observability Standards (Universal — Optional Layer)

> Field standards, level definitions, and discipline for structured logging.
> Applicable to Python, TypeScript, Go, Rust, and other mainstream languages.

---

## Log Level Definitions

| Level | Meaning | Who Responds | Example |
| --- | --- | --- | --- |
| `ERROR` | Actual system failure | On-call / developer | DB connection failure, 3rd-party API returns 500, uncaught exception |
| `WARN` | Potential issue | Developer monitors dashboard | Retry exceeded 3 times, abnormal request params handled by fallback, close to rate limit |
| `INFO` | Key business event | Business monitoring | User registered successfully, order created, scheduled task completed, service started/stopped |
| `DEBUG` | Debugging info | Developer investigating | Function input/output, loop iteration intermediate values |
| `TRACE` | Finest granularity | Rarely used, only when tracking a specific bug | Per-SQL query duration, per-external-call request/response body |

### Discipline

- **INFO: don't log loop-internal events** (e.g., "Row 1 processed", "Row 2 processed")
- **ERROR: don't log expected behavior** (e.g., user input validation failure → that's WARN or INFO)
- **DEBUG: should not appear in production** unless temporarily enabled for investigation
- **Never log sensitive data**: passwords, tokens, full credit card numbers, PII

---

## Standard Log Fields

Every structured log line must include these fields:

| Field | Type | Required | Description |
| --- | --- | --- | --- |
| `timestamp` | ISO 8601 | ✅ | `2026-06-04T14:30:00.000+08:00` |
| `level` | string | ✅ | `error` / `warn` / `info` / `debug` |
| `message` | string | ✅ | Human-readable description |
| `request_id` | string | ✅ | Request ID across the full chain, `-` when no request |
| `service` | string | ✅ | Service name (e.g., `user-service`) |
| `caller` | string | Recommended | File name + line number (e.g., `auth/handler.go:42`) |
| `duration_ms` | int | Recommended | Operation duration in milliseconds |
| `error` | object | On error | `{"kind": "timeout", "stack": "..."}` and other error context |
| `trace_id` | string | Conditional | Distributed tracing ID (when tracing system is used) |

### Log Format

```json
{
  "timestamp": "2026-06-04T14:30:00.000+08:00",
  "level": "error",
  "message": "Database connection timeout",
  "request_id": "req-abc123",
  "service": "order-service",
  "caller": "db/postgres.go:87",
  "duration_ms": 5023,
  "error": {
    "kind": "timeout",
    "retry_attempts": 3
  }
}
```

---

## Log Context

### Request-Level Context

Attached from the moment a request enters, carried throughout its lifecycle:

```text
request_id:    Unique per request
user_id:       Attached when user is authenticated
action:        Current operation (e.g., "create_order")
resource_id:   Operation target (e.g., "order-456")
```

### Error Log Context

Error logs must answer: "If I see this log again, what can I do about it?"

```json
{
  "level": "error",
  "message": "Payment callback processing failed",
  "request_id": "req-789",
  "error": {
    "order_id": "order-456",
    "provider": "stripe",
    "provider_status": "charge.failed",
    "provider_code": "card_declined"
  }
}
```

---

## Toolchain Recommendations

| Language | Recommended Solution |
| --- | --- |
| TypeScript | pino (fastest), winston (most extensive ecosystem) |
| Python | structlog (structured-first), loguru (user-friendly) |
| Go | slog (standard library), zerolog (zero-allocation JSON) |
| Rust | tracing (natively integrated with tokio) |

- All solutions should output JSON format — plain text logs are not supported
- Log to stdout / stderr, not directly to files (container/process managers handle log rotation)
