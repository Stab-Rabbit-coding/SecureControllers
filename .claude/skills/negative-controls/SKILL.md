---
name: negative-controls
description: Checks that a control can actually fail before you trust it passing. Use when writing or reviewing a test, lint rule, CI gate, feature flag, ignore rule, or runbook check, or when a QA pass, audit, or review comes back clean. Covers the check that greps for a string that never appears, the gate that never closes, the assertion too weak to tell two bugs apart, the fixture neutered before the code sees it, and the documented control with no implementation.
---

# Negative Controls

## Overview

In the laboratory a negative control is not optional: an assay without one is worthless, because you cannot tell a true negative from a dead assay. The same holds for every control in a codebase - a test, a lint rule, a gate, a checklist item - and each earns trust only once you have watched it fail. Where `test-driven-development` demands you watch a feature's test go red before it goes green, this skill extends that same demand to everything that is *not* a test, and to controls someone else wrote.

## When to Use

- Writing or reviewing a test, a lint rule, a CI gate, a runbook check, a feature flag, an ignore rule, or any other control.
- A QA pass, audit, or review comes back clean - a clean result from a broken instrument looks exactly like a clean result.
- Before repeating a claim that a control exists when you have read that it exists but never seen it act.

## The failure: an unfalsifiable control

**A check whose output is the same whether or not the thing it checks is true.**

It passes. It has always passed. It would pass if the system were broken, if the feature were never implemented, if the variable were misspelled, if the guard were deleted. Nobody notices, because the signal it emits when everything is fine is identical to the signal it emits when nothing is there.

This is not the same as a wrong assertion, and existing review gates do not catch it. Adversarial refuters ask "is this finding real?"; provenance checks ask "is this claim supported?" Both interrogate conclusions. An unfalsifiable control produces no conclusion to interrogate - it produces a green tick, and the green tick is the bug.

The tell: **you have never seen it fail.**

## What it looks like in the wild

Each of these is real, from one repository, found over a single working day, each discovered by accident while doing something else:

| Shape | Instance |
|---|---|
| Documented control with no implementation | A rollout flag named in the changelog and the launch checklist, present in no source file. Setting it to `0` or `1` did the same thing: nothing. |
| Check that greps for a string that never appears | A checklist item grepping the crontab for a systemd unit name. The crontab invokes the binary directly, so the string is never present. Reads zero when configured and zero when not. |
| Check against the wrong mechanism | `systemctl show -p Environment` for a value loaded via `EnvironmentFile=`, which that flag never displays. Empty either way, even against a correctly configured unit. |
| Silent fallback | `env.Or("JBG_DB_STRIPE", "./data/stripe.db")`. A misspelled name in the environment does not fail - it quietly writes to the default path. Working-but-wrong instead of broken-and-loud. |
| Assertion too weak to discriminate | A test asserting `err == nil` for an ungated subcommand, when a *gated* dispatch also returns nil. Adding the bug left the suite green. |
| Correct behaviour, no guard | A date layout whose fixed-width millis are load-bearing for day-boundary comparisons, with no test at a day boundary. Swapping it for `time.RFC3339` would misfile events and pass everything. |
| Vacuously-constructed fixture | An output-escaping test whose hostile payload was built with the default JSON marshaller, which escapes HTML - neutering the payload before the code under test ever saw it. |
| Environment-dependent green | A lint config validated locally against one tool version and run in CI against a newer one. Same config, zero issues locally, three failures in CI. |

The unifying property is not "these are bugs". It is that **in every case the instrument could not distinguish the two states it existed to distinguish.**

## The practice: never trust a control you have not seen fail

For any control you write or review, produce the failing state once and observe it:

1. **Identify what the control is supposed to detect.** State it as a concrete broken world: "the gate is missing", "the escaping is gone", "the variable is misspelled", "the flag is never set".
2. **Create that broken world.** Delete the guard, invert the condition, misspell the name, swap the safe call for the unsafe one, remove the fixture row.
3. **Run the control. Watch it fail.** Record what the failure actually looked like - the message, the exit code, the count that changed.
4. **Restore the world.** Verify by diff that you restored it exactly.
5. **Run the control again. Watch it pass.**

Report both observations. "It passes" is half a result. "It fails when I remove the guard and passes when I restore it" is a whole one.

If a control cannot be made to fail, it is not a control. Either strengthen it until it can, or delete it and say plainly that this thing is unverified - an honest gap is worth more than a false tick.

## Where to apply it

Highest value where the cost of a silent failure is highest and the feedback is weakest:

- **Security guards.** Output escaping, authentication checks, bind restrictions, permission modes, ignore rules for credentials. These are correct until one edit makes them not, and nothing complains.
- **Gates and flags.** Anything whose purpose is to *prevent* something. A gate that never closes and a gate that does not exist behave identically until the day it matters.
- **Operational checklists.** Every command in a runbook should have been executed at least once against a system in the wrong state. A go-live checklist whose items cannot fail produces confidence rather than verification, at precisely the wrong moment.
- **Ignore rules.** `git check-ignore -v <the actual path>` rather than reading the pattern and believing it.
- **Documentation of controls.** If a document says a control exists, grep for its implementation before repeating the claim. Documentation is a claim about the system, not a property of it.

## When you cannot falsify it

Sometimes producing the broken state is genuinely impractical - it needs production credentials, an irreversible action, or hardware you do not have.

Say so explicitly, in the artefact itself. Mark the control as unverified and name what would verify it. A checklist item reading "verified 2026-07-18 by removing the guard and observing failure" and one reading "never observed failing - would require a production drain" are both useful. An unmarked item that has never been exercised is the thing to avoid, because it reads identically to one that has.

Do not let the difficulty of falsifying a control become a reason to assert it works.

## Verification

Before you record a control as trusted:

- [ ] You have seen this control emit its failing signal at least once, on a deliberately broken world - not only its passing signal.
- [ ] You restored the world and confirmed by diff that the pass returned.
- [ ] Both observations are reported, not just the pass.
- [ ] Any control you could not falsify is marked `UNVERIFIED:` with what would verify it, rather than recorded as passing.
- [ ] For any documented control, you grepped for its implementation before repeating the claim that it exists.

## Related

- `test-driven-development` - red-green is the same idea applied to features. This extends it to everything else, including the checks that are not tests.
- `flaky-tests` - a control that passes intermittently is a control you have seen fail; the question there is why, not whether.
- `doubt-driven-development` - adversarial review of decisions. This is adversarial review of instruments.
- `fleet-qa-loop` - Step 2c applies this to a QA fleet's own findings and to any `AGENT_VERDICT: PASS` resting on a mechanical check.
