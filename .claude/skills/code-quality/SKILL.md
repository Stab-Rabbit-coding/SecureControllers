---
name: code-quality
description: >
  Write production-grade code: secure, efficient, maintainable. Applies to
  all languages. Includes code review mode producing a downloadable findings
  file. Consult for any code beyond one-liners.
---

# Code Quality

Defines how to write, review, and architect code - applies to every language. The user isn't a professional developer and relies on you for sound architectural decisions without shortcuts. Treat every piece of code as if it will run unattended in production, because it probably will.

### Guiding principle: the end user's experience is paramount

When two valid approaches compete, pick the one that produces a better experience for the person who will use the software even if it's harder to implement. Never optimise for your own convenience at the user's expense.

---

## Core principles (higher wins on conflict)

### 1. Security is non-negotiable

- **Validate all external input.** Network data, file contents, env vars, CLI args - anything crossing a trust boundary gets validated before use.
- **Least privilege.** Processes, files, DB users, API tokens - minimum permissions to function. Never root/admin when not strictly necessary.
- **Never hardcode secrets.** Credentials, API keys, tokens, sensitive config in env vars or secrets manager - never source, comments, or committed config.
- **Allowlists over denylists.** Permit known-good rather than blocking known-bad.
- **Parameterised queries and templating.** No string concatenation for SQL, shell, HTML output, or any injection-prone context.
- **Cryptography: established libraries, never roll your own.** Current algorithms, current key sizes, highest-level abstraction available (`libsodium` over raw OpenSSL primitives).
- **Audit dependency security** - maintenance status, known vulnerabilities, attack surface.
- **Pin to exact versions** and commit lockfile; verify lockfile integrity in CI. Prevents silent upgrades from introducing malicious code.
- **Verify package provenance.** Name exactly as expected (typosquatting: `requets` vs `requests`), owner matches expected maintainer, package scoped to correct namespace/registry.
- **Prefer scoped packages** (`@org/pkg` in npm, namespaced in Python) to avoid dependency confusion where a public package shadows an intended private one.

Network-touching or background code gets extra scrutiny: rate-limit endpoints, timeouts on all network calls, bind to localhost unless external access is required, clean shutdown paths.

### 2. Efficiency: least code, fewest resources

Not premature optimisation - just not being wasteful by default.

- **No duplicated work.** Compute or fetch once, pass through. Never retrieve the same data twice when it can be cached or stored in a variable.
- **No hardcoded values.** Configuration, thresholds, paths, URLs into constants/config/env vars. Group related config in one clear location.
- **Prefer standard library.** Don't pull dependencies for something a few stdlib lines can do. But when a well-maintained library handles significant functionality, edge cases you'd otherwise miss, or complex error-prone logic - recommend it and explain why it's the better choice.
- **Prefer the native tool over a workaround.** Before writing a compensating chain (replace-then-split-then-replace), a magic sentinel string that stands in for a real token, or a hand-rolled parser, tokeniser, or serialiser, check whether the stdlib or a mature library solves it natively. The trigger is mechanical: the moment you reach for a placeholder, a sentinel, or a second copy of the same logic, stop and ask whether a tool is designed for this. A workaround is only the right approach when it is the only approach, and you should know you are in that bucket and say why. A second copy of the same logic is the signal to extract the helper, not to keep duplicating.
- **Efficient data structures and algorithms.** Right collection type for the access pattern. Avoid O(n²) when O(n log n) or O(n) exists without much more complexity. Watch operations inside loops.
- **Minimise allocations in hot paths.** Reuse buffers, stream over loading entire files, use generators/iterators where appropriate.
- **Clean up resources.** Close file handles, DB connections, sockets, temp files. Use the language's idiomatic resource management (`with`, `defer`, `using`, RAII, `try-finally`). Never rely on GC for resource cleanup.

### 3. Maintainability: easy to change later

Since the user isn't a professional developer, the code must be especially clear.

- **Meaningful names.** Describe purpose. Avoid abbreviations unless universally understood in the domain (`url`, `id`).
- **Small, single-purpose functions.** Each does one thing. A function needing a comment to explain *what* it does should probably be two functions with descriptive names. Exception: if profiling shows function boundaries are a measurable bottleneck in a hot path, consolidate. Performance wins trump purity when backed by evidence.
- **Flat over nested.** Early returns, guard clauses, pipelines over deep conditionals. Restructure when indentation exceeds three levels.
- **Separation of concerns.** IO, business logic, presentation stay separate. A function that calculates shouldn't also print or write.
- **Consistent patterns.** Within a project, handle errors the same way, structure modules the same way, name things the same way. Consistency beats individual cleverness.
- **Design for extension.** Composition over inheritance. Interfaces/traits to define boundaries. Structure so new features don't require modifying existing logic.
- **Don't invent abstractions before you need them.** Three similar lines are clearer than a premature helper that hides them. Extract only once the duplication is real and the shared logic has a name worth giving it.
- **Leave no trash behind.** Remove dead code, stale comments, unused imports, and debug leftovers as part of the change. Left in place they read as load-bearing and mislead the next person who touches the file.
- **Sweep sibling references, not just the code you touched.** A fix landing correctly in one place is only half the job if another artefact still asserts, restates, or depends on the behaviour you just changed: a comment or rationale string elsewhere explaining the old reasoning, a doc paragraph enumerating "the one exception" that a later edit made three, a sibling test whose inline comment only holds under the old value, a second copy of the same claim in another file. After any fix, grep for the old value, name, or claim beyond the file you edited - not just for leftover dead code inside it. A correct fix next to a now-false comment is worse than no comment, because the false one reads as authoritative.

---

## Error handling

Three-tier approach:

### Development: fail fast, crash loudly

Assertions, panics, unhandled exceptions on invariant violations. Every error message includes what operation failed, the inputs, and why it's unexpected.

### Production, fatal errors: surface for bug reports

Unrecoverable state, missing critical resources, security violations → clear user-readable message and what the user should do (usually: report the issue). Include a reference ID or timestamp for log correlation. Never expose stack traces, internal paths, or implementation details to end users.

### Production, non-fatal errors: log and continue

Transient network failures, malformed optional data, recoverable state → small human-readable log file in an obvious, accessible location. Each entry: timestamp, brief description, enough context to diagnose. Rotate or cap the log.

Log format: one or two lines per entry, plain text. No complex structured formats unless the project already uses one. The user must be able to open it and understand what happened.

### Security-critical errors: fail closed

Authentication, authorisation, input validation, cryptographic operations → deny by default, don't log and continue. A timeout on an auth check means "denied", not "skip the check". Fail-closed takes precedence over the non-fatal tier for any error affecting a trust boundary. If unsure whether an error is security-sensitive, fail closed.

---

## Comments and documentation

- **Comment complicated sections inline - explain *why*, not *what*.** The code shows what happens; the comment explains reasoning.
- **When a fix exists because of a specific failure, name the failure and cite where it happens.** A comment carrying an argument is load-bearing: a later editor tidying up has to delete the argument deliberately, whereas a bare assertion reads as noise and goes. Not `// must be non-empty` but `// empty here means the regex matched nothing and ctest exits 0 having run no tests - see tests/CMakeLists.txt:47`.
- **Minimal.** One or two concise lines, reasons in order of importance.
- **Don't justify the obvious.** Well-named code is self-documenting. Reserve comments for non-obvious decisions: workarounds, performance choices, security rationale, external-system constraints.
- **Document public interfaces.** Functions, classes, modules other code depends on get a brief docstring or header: purpose, parameters, return values, notable failure modes.

---

## Testing guidance

Every code change ends with a short **Testing** section:

1. **List edge cases ranked by severity** (most dangerous first): empty inputs, boundary values, malformed data, concurrent access, resource exhaustion, permission failures, network timeouts, injection attempts. Evaluate severity yourself - the user may share the output, and you can't assume others will catch edge cases you miss.
2. **Concrete test commands or steps** - copy-pasteable. Use the language's built-in test runner; if none, a minimal script or manual steps.
3. **State what "pass" looks like** for each test. The user shouldn't have to guess whether the output is correct.
4. **Keep it brief.** A few well-chosen tests on critical paths and the nastiest edge cases beat an exhaustive list nobody will run.
5. **Verify LLM-generated code independently.** Any LLM output (this skill included) can contain subtle security flaws, incorrect API usage, or hallucinated function names. Run static analysis (`bandit` for Python, `eslint-plugin-security` for JavaScript, `cargo clippy` for Rust); test every security-sensitive path manually.
6. **Treat warnings as errors, and audit outputs not just inputs.** Never suppress, silence, or `# noqa` a warning to get a clean run - find and fix the root cause. If the root cause is genuinely unclear, note what you tried and why it was inconclusive rather than hiding it. Compiler warnings, linter output, and test results are reality; intention is not, so read what the tools actually emitted.
7. **Run environment discovery through the mechanical gate, don't eyeball it.** If the code resolves a hardware or SDK path, or locates a tool on `PATH`, run the repo's `env_discovery_gate.py` (reference implementation: `music-video-pipeline/audio-analysis/tools/env_discovery_gate.py`, also runnable standalone against other repos) rather than judging it by reading. It catches, mechanically: unversioned vendor paths hardcoded in source (`/opt/rocm` instead of a versioned or glob form), a `which`/`command -v` probe with no registered fallback, a capability-downgrade note that restates `field=value` without naming a cause, and an installer that consumes an env var before resolving it. Three of those were real, passing-tests bugs on real hardware, and the agent review that read the diffs missed all three - which is why this is a script rather than a checklist item you could satisfy by looking.

---

## Code review mode

### Verify before you report: no finding without evidence in context

Before a candidate problem enters the findings list, it has to survive verification. For each one: name the specific evidence that proves it is real; run the actual check (compiler, linter, tests); read the output for false positives; and confirm it still holds when you look at the surrounding code. A candidate that skips any of these steps is unverified, and an unverified candidate is not a finding - it goes in notes as a flagged possibility, or not at all. The linter confirms that a pattern exists, not that it is a real problem here; the patterns that look most obvious are exactly where false positives hide; and an issue with no test evidence is an assumption however confident it feels. If a verification step genuinely cannot be run, say so plainly - a finding carrying an honest uncertainty flag is worth more than a confident claim that later turns out wrong.

When reviewing existing code, evaluate against all principles above and report findings in this order:

1. **Security** - anything exploitable.
2. **Bugs** - logic errors, off-by-one, race conditions, resource leaks.
3. **Efficiency** - duplicated work, unnecessary allocations, poor algorithm choice.
4. **Maintainability** - unclear naming, tangled logic, missing error handling.
5. **Style and minor** - only if the above are clean.

Each finding states what the problem is, why it matters, and how to fix it. Corrected snippet if the fix is non-obvious. If the code is sound, say so; don't invent problems. Report and fix findings at every severity, Low and Info included - don't defer the small ones on the grounds that they are minor, because a cheap fix now is cheaper than the same fix after later work has built on top of it.

### Review recommendations file

After completing a review, produce a self-contained markdown file for download - someone reading it without the conversation should understand every finding.

```
# Code Review: [filename(s)]

**Reviewed:** [date]
**Files:** [list of files reviewed]

## Summary

[2–3 sentence overview: overall quality, most critical findings, whether anything
 needs immediate attention.]

## Findings

### 1. Security

[Findings or "No issues found."]

### 2. Bugs

[Findings or "No issues found."]

### 3. Efficiency

[Findings or "No issues found."]

### 4. Maintainability

[Findings or "No issues found."]

### 5. Style

[Findings or "No issues found." Only include if higher categories are clean.]

## Recommended actions

[Numbered list of concrete actions, ordered by priority. Each item should state
 what to change, in which file/function, and why. Keep it actionable; the user
 should be able to work through this list top to bottom.]
```

Direct, concise language. Code snippets in fenced blocks where the fix is non-obvious. Save as `review-[filename].md` (or `review-[project-name].md` for multi-file reviews) and present for download.

---

## What this skill is NOT for

- One-liner commands or CLI arguments.
- Choosing between tools or technologies (unless the choice has security or efficiency implications in the code being written).
- Documentation not directly attached to code.

---

## Checklist: before presenting code

- [ ] No hardcoded secrets, paths, or config values that should be variable.
- [ ] All external input is validated.
- [ ] No duplicated computation or redundant data fetches.
- [ ] Resources (files, connections, handles) properly cleaned up.
- [ ] Error handling follows the three-tier model.
- [ ] Dependencies justified; stdlib used where practical.
- [ ] Functions small, single-purpose, clearly named.
- [ ] Warnings addressed at the root cause - none suppressed, silenced, or ignored.
- [ ] No dead code, stale comments, unused imports, or debug leftovers.
- [ ] Searched beyond the changed file for sibling comments, docs, or tests that assert the old behaviour and updated them to match.
- [ ] Complicated sections have brief inline comments explaining *why*.
- [ ] Network-facing or background: timeouts, rate limits, least-privilege, clean shutdown.
- [ ] Brief Testing section with edge cases ranked by severity.
- [ ] Security-critical error paths fail closed.
- [ ] Dependencies pinned to exact versions with lockfile committed.
- [ ] New dependencies verified for typosquatting, provenance, and scope.
- [ ] Code review: recommendations markdown produced and presented for download.
