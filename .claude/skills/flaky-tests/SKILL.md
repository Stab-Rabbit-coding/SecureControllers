---
name: flaky-tests
description: Diagnoses flaky and intermittently-failing tests. Use when a test passes and fails without a code change, when the reflex fix is "widen the timeout", or before claiming a flake is resolved. Covers timeouts that budget the wrong thing, skip()-on-timeout, process-global mock pollution, live-service leakage, and assertions that can't distinguish two bugs.
---

# Flaky Tests

## Overview

A flaky test's timeout is almost never a budget for the thing the test claims to measure. Widening it is the reflex fix and it is usually wrong, because the number was never measuring what you thought. Diagnose by measurement, timing the actual path and reading the shape of the degradation curve, before touching the number.

## When to Use

- A test passes and fails with no code change (the definition of flaky).
- The instinct is to widen a timeout, add a retry, or mark a test `skip`/`xfail`.
- Before claiming a flake fix is done - every fix here needs a mutation-check (below) before it stands.
- A test patches a process-global (`shutil.which`, `subprocess.run`, env vars) or talks to `localhost`.

## Six Causes (each seen in one suite, one day)

### 1. Timeout that's secretly a budget for a *failure* path

A poll budget for "did the notification arrive" measured, instead, how long an auxiliary client took to exhaust its provider list with no API key configured: 3.464s of a 3.520s budget. If a timeout is generous and still flakes, time the path before widening it; it may be budgeting a detour the test never meant to take.

- Fix: pin the mode so the irrelevant path is never entered, and wait on an event the producer signals, not a sleep-poll. A poll measures whatever happens to be slow; an event measures the thing you named.

### 2. Timeout that's secretly a *cold-boot* budget

A 10s budget covered booting an interpreter, importing the stack, spawning a second interpreter, and completing a handshake, before the test's own question was even asked. Degradation under load was smooth and monotonic (0.96s to 5.20s across 0x-6x oversubscription), no cliff.

- Read the shape of the degradation curve before the number. Smooth and monotonic means the budget is too small for the work it covers; a cliff, or an EOF/decode error, means something actually died. Those get different fixes.

### 3. `skip()` on timeout launders a coverage hole into green

A browser test called `pytest.skip()` when Chrome missed its boot budget. A test reporting success when it never ran is worse than one that fails: it occupies the slot where the failure would have been visible.

- If a skip is conditioned on slowness, convert it to a failure. Skips are legitimate only when conditioned on *absence* (no browser installed), never on *slowness*.

### 4. Last-call assertions on process-global mocks

`assert_called_with` / `assert_called_once_with` check only the mock's final recorded call. When the mock patches a process-global (`shutil.which`, `subprocess.run`), any unrelated code touching that global during the patch window rewrites what "last call" means, and the failure looks environment-dependent, sending you hunting the wrong thing.

- Grep any suite that patches globals. Use `assert_any_call` where the claim is about the argument; keep the strict form only where the count itself is the assertion. (One suite: 67 sites of this shape, 8 genuinely wrong.)

### 5. Tests that probe live local services

A test declared a provider at `localhost:11434` with no mocked fetch. On a machine with Ollama actually running, the test consumed 11 real models instead of its own fixtures. Loopback is network: a "no network" assumption that permits `127.0.0.1` permits an entire local service estate. Mock the fetch.

### 6. An assertion that can't distinguish two bugs

A cross-session routing test polled `if notified_a or notified_b`, then asserted A specifically, so a message delivered to the *wrong* session failed with the identical message as one that never arrived at all. If two distinct defects can produce the same red, the test is under-specified.

- Wake on "landed anywhere", then assert the more specific failure (the leak) before the general one (the arrival), so a routing regression reports as itself rather than as its shadow.

## Two Rules for Every Fix

**Mutation-check before claiming it's fixed.** Reintroduce the original bug and confirm the test fails, fast, with the right message. Without this, a deterministic wait is indistinguishable from a vacuous one: you may have removed the flake's ability to speak rather than the flake itself. This is cheap, local mutation testing, and it belongs on every flake fix.

**A streak of green runs is weak evidence; say so.** Six consecutive green runs bound a remaining per-run flake probability at only roughly p < 39% (95% confidence); three runs, p < 63%. Reproducing the flake under deliberate load (e.g. busy loops well past core count), measuring it, and showing fail-before/pass-after is a controlled experiment and far stronger. If you're unsure which kind of evidence you actually have, say so rather than asserting the flake is gone: "six green runs" and "reproduced under load, fixed, no longer reproduces" are different claims.

## Checklist

```
- [ ] For every timeout in the test: timed the actual path - a budget for what, exactly?
- [ ] Sleep-polls replaced with events the producer signals, where possible
- [ ] Grepped for skip() conditioned on timing; converted to failure or re-conditioned on absence
- [ ] Grepped for assert_called_with / assert_called_once_with on mocks patching process globals
- [ ] Grepped for localhost / 127.0.0.1 endpoints with no mocked fetch
- [ ] Checked whether two distinct bugs could produce this same red; split the assertion if so
- [ ] Mutation-checked: reintroduced the original bug, confirmed the test fails with the right message
- [ ] Evidence claim is honest: green-streak count, or fail-before/pass-after under load, named as what it is
```

## Common Rationalizations

| Rationalization | Reality |
|---|---|
| "Just widen the timeout" | The number was never measuring what you think. Time the path first. |
| "It's environment-dependent" | Often a process-global mock whose last call is being overwritten by unrelated code. Check before blaming the environment. |
| "Skip it if the browser's slow, we'll catch it another way" | Skip on slowness launders a coverage hole into a green run. Convert to a failure. |
| "It's green now, ship it" | A deterministic-looking pass can be a vacuous one. Mutation-check first. |
| "Six green runs in CI proves it's fixed" | Six greens bound the remaining flake rate at only roughly p < 39% (95% CI). Reproduce under load instead, or say plainly that a streak is what you have. |
| "`localhost` isn't really network" | It's whatever happens to be listening on that machine. Mock the fetch. |

## Red Flags

- Widening a timeout with no measurement of what the path actually spends its time on
- `skip()` gated on elapsed time rather than on a confirmed-absent dependency
- `assert_called_with` / `assert_called_once_with` on a mock patching a process-global, with no check for other code touching it in the same window
- A test with an unmocked `localhost` / `127.0.0.1` fetch
- An assertion that would produce the same failure message for two different underlying bugs
- Claiming a flake is fixed without reintroducing the bug to watch the test fail again
- Reporting "N green runs" as proof without naming it as weak evidence

## Interaction with Other Skills

- **`debugging-and-error-recovery`**: general root-cause debugging; this skill is the flaky-test-specific taxonomy layered on top.
- **`doubt-driven-development`**: its "refute before you relay" step is the same discipline applied to causal claims generally, not just test flakes.
- **`test-driven-development`**: TDD's RED step, seeing the test fail for the right reason, is the mutation-check above, generalised.
- **`github-actions`**: sampling a flake in CI needs serial dispatch, not concurrent; see that skill's CI traps.

## Verification

After a flake fix:

- [ ] The timeout (if any) was timed against the real path, not just widened
- [ ] The fix was mutation-checked: the original bug reintroduced, the test fails with the correct message
- [ ] Any `skip()` in the test is conditioned on absence, never on slowness
- [ ] Evidence offered for "fixed" is named honestly (green-streak vs controlled fail-before/pass-after)
