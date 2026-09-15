---
name: disposition-ledger
description: >
  Use when review findings from plan-auditor, code-auditor, pr-reviewer,
  /code-review, or any audit agent need tracking to a resolution before
  work is called done - especially when blockers or major findings risk
  evaporating into conversation without an explicit accept, reject, or
  defer decision.
---

# disposition-ledger

Domain: review-finding lifecycle tracking. Findings from an audit agent or `/code-review` are worthless the moment they're read and not acted on. This skill maintains a file-backed ledger so every finding reaches exactly one terminal state before the work it concerns is called complete.

Distinct from `superpowers:receiving-code-review`, which governs *how* to evaluate one piece of feedback (verify against the codebase, push back with technical reasoning, or implement). This skill governs *whether the set is fully resolved*: it doesn't replace that judgement, it records the outcome of it and gates on completeness. Use receiving-code-review's rigour to decide a disposition; use this skill to write it down and check nothing was skipped.

## The gate (core rule)

**NO BLOCKER OR MAJOR FINDING SHIPS WITHOUT A DISPOSITION.**

Every blocker/major/critical/high finding from a review gets exactly one of:

- **accepted** - will be fixed; row links to the commit, task, or fix location that resolves it.
- **rejected** - will not be actioned; row cites the specific code, test, or fact that makes the finding wrong. A bare "won't fix" is not a disposition.
- **deferred** - postponed; row records who (a human, by name) approved the deferral and what condition reopens it. A model cannot self-approve a deferral - it can only propose one and note whose sign-off is pending.

A **proposed** deferral awaiting human sign-off is not a closed row. Mark it `deferred (PENDING <name>)` in the Disposition cell so it reads distinctly from a blank, untouched finding - a pending-approval row is an open row and does not pass the gate. The Evidence cell holds a re-checked fact (a file, a line, a test result you confirmed), never a recollection: "I believe middleware covers it" is a belief, not evidence, and leaves the finding open.

Deferring an **irreversible** change (a dropped column, a data migration, a deletion) needs a sharper reopen condition than a reversible one. "Reopen if we need it" is meaningless once the column is already gone - the reopen condition must fire *before* the destructive step runs, or the deferral is not valid.

When a finding cannot be verified from the evidence at hand, that is itself an outcome, not a reason to guess or to dig without limit: mark it `blocked (needs <what>)` and escalate. This is the pressure valve against both failure modes - marking accepted on a glance, and rabbit-holing on one finding while the rest of the ledger goes untouched. Deciding *how hard* to verify a given finding is the job of `superpowers:receiving-code-review`, not this skill; this skill only insists that the outcome is one of accepted / rejected / deferred / blocked, never a blank or a guess.

Minor/low/nit findings should also get a disposition where practical, but the gate is absolute for blocker/major severity: work is not done while one sits blank.

## Ledger format

Markdown table in a tracked file (e.g. `docs/disposition-ledger.md` or a per-branch `REVIEW.md`), one row per finding:

| ID | Source | Severity | Finding | Disposition | Evidence / Link | Approved by |
|---|---|---|---|---|---|---|
| `pr-reviewer-1` | pr-reviewer | Blocker | ... | accepted | commit `a1b2c3d` | - |

Markdown, not JSON: it's greppable and diffable in the same PR the findings concern, needs no parser, and sits next to the plan or branch it tracks - a schema would need tooling this fleet doesn't have for a net loss in reviewability.

ID = `<source-agent>-<n>`, sequential per source. Severity and Finding copy the auditor's own wording verbatim - plan-auditor's `#### [SEVERITY] Title` / Issue, pr-reviewer's Critical/Important Issues, code-auditor's `### [SEVERITY] Title` / Issue all map onto Severity + Finding without reformatting. Don't paraphrase the finding when transcribing it; copy it.

## Carrying rejections into the next round

**This is the orchestrator's job.** A dispatched auditor cannot invoke this skill - fleet agents declare explicit `tools:` lists and none includes `Skill` - so none of it reaches the auditor unless the orchestrator writes the list into the brief.

When a multi-round audit opens a new round, the ledger's `rejected` rows go into that round's brief as a settled list. This is what stops the same non-defect being re-investigated: one numerical convention was independently re-settled five times before this was adopted.

Carry each row's **evidence**, not just its conclusion. "We looked at this, it is fine" invites re-litigation; "not a defect because `parser.rs:88` clamps the index" ends it.

A row is carried only while its evidence still stands. **If the evidence cites a file that has been edited since, the row is reopened, not carried** - the artefact moved underneath the reasoning, which has not been rechecked against it.

**Carrying the disproved list runs against `fleet-audit-loop`'s "Brief with classes, not instances" rule (Step 3), on purpose.** That rule biases a briefed auditor toward confirming named instances rather than checking, so it briefs recurring patterns and withholds the specific defects already found. The disproved list inverts that: naming the specific rejected instance is what stops it being re-investigated, because it removes ground from the search rather than directing it. Both rules are intended; the tension between them is not a defect to be edited out.

## Append-as-you-go

Write the row the moment a finding is dispositioned, not in a batch at the end. `/media/owner/Workspace/claude-agents/REPORT_PROTOCOL.md` owns the append-as-you-go rule and the failure it prevents; this is that same rule applied to ledger rows instead of report findings - reference it, don't restate it here.

## Where it plugs in

- **Adjudication, before implementation.** After plan-auditor or code-auditor emits findings and before a branch is started, every blocker/major gets a row. This is the step the branch's spec is written against - specification work should cite accepted findings, not raw audit output.
- **Before a branch is called done.** Alongside `superpowers:verification-before-completion` and `superpowers:finishing-a-development-branch`: re-open the ledger, confirm no blocker/major row is blank, confirm every `deferred` row names an approver. A green test suite does not close a ledger with a blank row in it.
- Consumes findings from plan-auditor, code-auditor, pr-reviewer, and `/code-review` as-is; produces no new finding format for them to conform to.

## Worked example

```
| ID              | Source        | Severity | Finding                                  | Disposition | Evidence / Link                                                        | Approved by |
|-----------------|---------------|----------|-------------------------------------------|--------------|-------------------------------------------------------------------------|-------------|
| code-auditor-1  | code-auditor  | Critical | Unparameterised query in `order.rs:88`   | accepted     | fixed in commit `9f3ab21`                                                | -           |
| plan-auditor-2  | plan-auditor  | High     | No rollback point for migration step 3    | rejected     | step 3 is `ALTER TABLE ... ADD COLUMN` with a default; re-running it is idempotent, see `migrations/0042.sql:1-6` - nothing to roll back | -           |
| pr-reviewer-3   | pr-reviewer   | Blocker  | New `/export` endpoint has no rate limit  | deferred     | endpoint is behind the internal VPN only for this release; reopen when it's exposed externally | J. Alvarez, 2026-07-09 |
| code-auditor-4  | code-auditor  | Medium   | `unwrap()` on user-supplied path in CLI arg | accepted   | fixed in commit `9f3ab21`                                                | -           |
```

Contrast row 2 with a bad rejection: "not a real issue, skip it" cites nothing and would not satisfy the gate - it's a bare assertion wearing a disposition's clothes. Row 2's actual entry names the file, the line range, and the specific property (idempotency) that makes the finding false.

## Anti-pattern: bulk dispositioning

"Accepting all 6" or "rejecting the whole batch, these are all fine" is not four dispositions and three dispositions - it's the gate failing quietly under a different name. Evidence and approval are per finding; a batch note satisfies none of them individually. Give every row its own reasoning line, even a short one - "duplicate of row 2" is a valid one-line reason, "batch approved" is not.

## Red Flags - STOP

| Excuse | Reality |
|--------|---------|
| "I'll write the ledger once the whole review is triaged" | Batching write access is why interrupted reviews lose findings. Append per-row. |
| "It's obviously not a real issue, no need to spell it out" | Obvious-to-you is not evidence on the row. Cite the fact or code that makes it wrong. |
| "There's middleware that probably covers it" / "the tests are green, so it's handled" | A recollection is not evidence and a passing suite is not proof the specific finding is fixed - the green suite may have no test for it at all. Re-check the exact file/line, or the row stays open. This is the most common way a blocker gets silently marked accepted. |
| "It's a major like the other one, defer them together" | Reversibility, not severity, decides how a defer is judged. A destructive migration and a missing rate-limit are both major and are not the same risk - defer each on its own reopen condition or not at all. |
| "I'm confident this is fine to defer" | Confidence is not approval. Deferral needs a named human sign-off and a reopen condition. |
| "These four findings are basically the same, one row covers it" | One row per finding, even near-duplicates - link them, don't merge them. |
| "Low severity, skip the ledger" | The gate is absolute for blocker/major; minors still benefit from a row, don't let habit erode into skipping those either. |

## Guiding principle

A ledger with three rows dispositioned and one blank is not a passing gate with an outstanding nit - it's a failing gate that hasn't been checked yet.
