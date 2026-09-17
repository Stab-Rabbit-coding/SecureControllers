---
name: fleet-audit-loop
description: Use when auditing a set of agent or skill definitions and one sweep is not enough - each round points a different auditor at a different dimension instead of re-running the same sweep until findings taper. Invoke for "audit these agents", "audit my skills", "multi-round audit of the fleet", or when a previous audit's falling finding count is being read as the artefact being clean.
---

# Fleet Audit Loop (rotate dimensions, not repetitions)

Domain: multi-round auditing of agent and skill definitions. Each round selects a
**dimension** and the auditor that covers it, briefs that auditor on recurring
patterns rather than on the specific defects already found, and reads the round's
result from a report file on disk. The loop ends when the dimensions are
exhausted, not when a round comes back clean.

**Announce at start:** "Using fleet-audit-loop to audit `<target set>` across N dimensions."

## Scope boundary

- **`fleet-qa-loop`** governs *code*: mechanical linters first, then the QA fleet,
  until lint is clean and tests are green. Where an idea below is already stated
  there (append-as-you-go reporting, adversarial verification before fixing),
  this skill references it rather than restating it. **Termination is not
  shared.** This skill's own terminal states are DIMENSIONS EXHAUSTED and
  STALLED (Step 6) - it has no CLEAN state. Nor is the iteration cap shared:
  this skill's six-round roster (Step 2) is fixed, not `fleet-qa-loop`'s default
  cap of 5 - round 6 verifies rounds 1-5's fixes, so a cap of 5 would end the
  loop before its own regression check runs.
- **`plan-audit-loop`** (an agent, at `/media/owner/Workspace/claude-agents/agents/plan-audit-loop.md`)
  governs *plans*: it loops `plan-auditor` and `requirements-auditor` over a plan
  document before execution begins. It is not superseded or wrapped by this skill.
- **This skill** governs *definitions*: `agents/*.md` and `src/*/SKILL.md`, artefacts
  that are themselves prompts. Use `plan-audit-loop` for a document describing work
  not yet done; use this for the definitions that will do the work.

The three do not overlap in target. They do differ in loop shape: the other two
re-run one sweep until findings taper, and this one rotates. That difference is
the subject of Step 2 and is the reason this skill exists separately.

**This skill is deliberately house-specific.** The dimension roster names agents in
`/media/owner/Workspace/claude-agents/`, and the standards it audits against
(`SKILL_CHECKLIST.md`, `REPORT_PROTOCOL.md`) are this collection's. The loop shape
transfers to any fleet; the roster does not, and a different fleet needs its own
dimension-to-agent mapping in Step 2.

## Consumer and reach

**Only a caller holding `Skill` (an orchestrator, or an agent with `tools: *`)
can invoke a skill at all** (`SKILL_CHECKLIST.md:82-83`). None of this loop's
seven roster auditors do: all 55 agents in
`/media/owner/Workspace/claude-agents/agents/` declare an explicit `tools:` list
and not one includes `Skill` or `*` (verified 18 July 2026; re-check with
`grep '^tools:' /media/owner/Workspace/claude-agents/agents/*.md`). Built-in
dispatchable types outside that directory - `general-purpose`, `claude`,
`Explore` - do carry `tools: *` and can invoke a skill; this roster names none
of them. **Every rule below that a roster auditor must follow reaches it only
because the orchestrator copies it into that agent's dispatch brief.** Sections
marked **[relay]** are text to be written into a brief; everything else is yours
to execute.

As of 18 July 2026 the orchestrator is also this skill's only reader, because no
agent carries a `skills:` preload (verify:
`grep -l '^skills:' /media/owner/Workspace/claude-agents/agents/*.md`, which matches
nothing). A preload would add a reader without adding an invoker, so the relay
requirement stands either way. `SKILL_CHECKLIST.md` covers the two delivery
mechanisms in full.

A loop skill written as though its auditors will read its rules is silently inert:
the orchestrator behaves correctly and the fleet does not.

## Inputs

- **target set**: the definition files to audit. Name them explicitly; "the fleet"
  is not a target set, and a round pointed at a set the orchestrator cannot
  enumerate cannot be checked for completion.
- **ledger path**: a `disposition-ledger` file for this audit. See that skill for
  the format and the gate; do not define a second one here.
- Work on a branch. Commit only when the user has authorised it.

## Step 1 - Confirm the previous round actually finished

Skip on round 1. Otherwise, before dispatching anything:

- Every report file from the previous round exists and its `## Completion` block
  reads `**Status:** COMPLETE` (the protocol is at `/media/owner/Workspace/claude-agents/REPORT_PROTOCOL.md`).
- No agent from the previous round still holds a file in this round's target set.

**Idle is not done, and neither state reports itself.** An agent gone quiet with
`Status: IN PROGRESS` died mid-pass. An agent gone quiet with no file never
started. Dispatching a second agent onto a file another was still holding caused a
near-collision that was caught by luck, not by a check.

If a report is missing or incomplete, re-dispatch that auditor before opening the
new round. **The report file is what this loop reads; re-prompting is the fallback,
not the mechanism.** In one session six subagents went idle without sending a final
message: the five that had written their file lost nothing, and the one that had
not had to be recovered by re-prompting.

## Step 2 - Select this round's dimension

The round counter selects a dimension, not a repetition.

| Round | Dimension | Agent |
| --- | --- | --- |
| 1 | Structural conformance to the checklist | `agent-auditor` (agents) / `skill-auditor` (skills) |
| 2 | Domain coverage gaps | `blind-spot-auditor` |
| 3 | Context and token waste | `token-usage-auditor` |
| 4 | Trigger and activation (skills only) | `skill-trigger-auditor` |
| 5 | Internal coherence, weighted to the newest material | `conformance-auditor` |
| 6 | Fixes from rounds 1-5 still achieve their intent | `fix-regression-checker` |

**Why rotation rather than repetition.** Across eleven rounds, findings tracked
wherever each round was pointed and did not decay with repetition: rounds aimed at
a new dimension were still producing CRITICALs and HIGHs after eight rounds. A
falling finding count across rounds that reuse a dimension means **the sweep is
exhausted, not the artefact**. Reading that as convergence is the specific error
this loop exists to prevent.

**Round 5 is weighted to the most recently written material** and its brief says
so. A coherence audit found every one of its defects there, because each new
section had been written against a snapshot its predecessors had since modified.

## Step 3 - Write the brief

**[relay] Brief with classes, not instances.** Carry recurring defect *patterns*
from prior rounds. Do not carry the specific defects already found and fixed.
Pattern briefing produced findings in new locations; instance briefing produced
confirmation of the instances. One auditor described the mechanism: content
recalled from its own memory arrives as "here is what was true, verify it", which
invites checking, whereas the same content in a brief arrives as instruction.

- Carries: *"Parallel-place omission recurs in this corpus: a rule updated in one
  of several places that must agree. Check every place a rule of this kind lives."*
- Does not carry: *"Round 2 found the description in `src/foo/SKILL.md` disagreed
  with `foo.md`; check whether that is fixed."* That is round 6's job, and putting
  it here converts an audit into a confirmation.

**Round 6 is the deliberate exception.** `fix-regression-checker` holds the
instance list, because confirming a named list of applied fixes is exactly its job.

**[relay] Carry the disproved list.** The `rejected` rows from the ledger go into
the brief with their evidence, per the `disposition-ledger` skill's
"Carrying rejections into the next round". That skill owns the rule, including
the reopen condition when the cited file has since been edited. Reference it;
do not restate it.

**Report path convention.** `.superpowers/sdd/audit/<round>-<dimension-slug>.md`

- e.g. `.superpowers/sdd/audit/1-structural-conformance.md`,
`.superpowers/sdd/audit/6-fix-regression.md`. The orchestrator sets this path and
puts it in the brief; it is not left to `REPORT_PROTOCOL.md`'s default naming,
because Step 1 has to check for a specific previous-round file without guessing
at a timestamp.

**[relay] Report to disk before replying.** Copy `REPORT_PROTOCOL.md`'s "block
that goes into an agent body" into the brief, with the path from the convention
above in place of its default. Reference the block; do not restate its
skeleton-first, append-as-you-go procedure in fresh wording. A reply is lost if
the agent goes idle; a file is not - which is why this skill reads the report
file rather than `fleet-qa-loop`'s `AGENT_VERDICT` message. The two loops use
different completion channels on purpose, not by accidental drift.

**[relay] Invite abstention.** State in every brief: *"If you cannot verify a
finding, mark it UNCERTAIN in the report rather than asserting or omitting it."*
`SKILL_CHECKLIST.md`'s Self-verification section owns the rule this rests on
("an unverified claim marked uncertain is more useful than a confident guess");
reference it. Here it is also what lets the orchestrator weight the finding
correctly at Step 5.

Give each brief the target paths, the report file path (the convention above),
and the standard the round is auditing against (`SKILL_CHECKLIST.md` for
skills). **State the standard; an agent will not infer it.**

## Step 4 - Dispatch, then verify on disk

Dispatch the round's auditor. When it returns, or when it goes quiet, apply Step 1's
disk check to this round before reading anything as a result.

Do not treat `## Findings` reading `_None._` and an absent file as the same
outcome. The first is a clean dimension; the second is a round that did not happen.
Telling them apart is most of the value of the report protocol.

## Step 5 - Triage and fix

Verify findings before fixing them: `fleet-qa-loop` Step 2b owns the refutation
procedure and applies unchanged here. Record every disposition in the ledger as it
is decided, not in a batch at the end.

**Prefer a gate to prose where an invariant can fail.** Parallel-place omission was
the single most recurrent defect: eleven occurrences across eleven rounds, one of
them in work by an agent that had been explicitly briefed about that exact pattern.
Briefing did not prevent it. So where a round's finding can be expressed as a check
that fails, the fix step writes the check as well as the fix, under `scripts/`.

- A gate: `check-skills.sh` compares `src/<name>/` against the built archive and
  exits non-zero when they differ. It can fail, so its passing means something.
- Not a gate: a `ctest` invocation whose regex matched nothing and exited 0,
  read as coverage. `SKILL_CHECKLIST.md`'s Self-verification section owns the
  rule this incident produced; reference it, do not restate it.

**Not every invariant is mechanisable.** Of the eleven occurrences, one was a
briefing error and one was domain knowledge; neither is expressible as a script.
When an invariant cannot be mechanised, record it as a prose rule sited at the
point of use rather than in a distant document, and say in the ledger which of the
two you chose. A rule stated far from where it is needed gets missed, which is the
evidence behind this rule.

## Step 6 - Loop or terminate

Re-enter at Step 1 with the next dimension.

- **DIMENSIONS EXHAUSTED** (terminate): every dimension in the roster has had a
  round that completed on disk. **Termination is not on a clean round.** A clean
  round in one dimension says nothing about the next.
- **STALLED** (terminate, report): an auditor returns BLOCKED, or the same finding
  survives two rounds in the dimension that owns it, or a re-dispatched auditor
  fails to produce a completed report twice.

**The honest limit, and state it in the final summary.** Six dimensions is what
this fleet currently has. Running out of dimensions is not proof the artefact is
clean; it is proof this fleet has nothing further to point at it. A seventh
dimension would likely still find things, on the evidence above.

## Verification before you report the loop done

- Every roster agent named in a brief is **dispatchable in the harness actually
  running this loop**, not merely present as a file. `ls
  /media/owner/Workspace/claude-agents/agents/{agent-auditor,skill-auditor,blind-spot-auditor,token-usage-auditor,skill-trigger-auditor,conformance-auditor,fix-regression-checker}.md`
  confirms the definitions exist in the companion repo; it does not confirm the
  harness you are dispatching from has that name registered as a callable agent
  type. Check the harness's own agent-type listing (e.g. Claude Code's available
  `Agent` types) before the round, not after a dispatch fails. A roster name
  that resolves as a file but is not a registered type in this harness is not a
  passing check - substitute the nearest available type for that round, and
  record the substitution in the report and the final summary: which roster
  name, which type stood in for it. This is the same shape as the `ctest`
  incident (`SKILL_CHECKLIST.md`'s Self-verification section) applied to agent
  dispatch: a check that only confirms the file exists reads as coverage for a
  claim - "this agent can be dispatched" - that it never tested.
- Every round has a report file whose `## Completion` block reads COMPLETE.
- Every blocker and major row in the ledger has a disposition.
- For skill targets: `scripts/check-skills.sh <name>` exits 0 for each skill edited
  during the loop. Capture `$?` directly, not after a pipe; `$?` after a pipeline
  reports the last command in the pipe.

## Output

- Per-round report files, per `REPORT_PROTOCOL.md`.
- The ledger, with every finding dispositioned.
- A final summary: which dimensions ran, what each found, what was fixed by gate
  and what by prose rule, what was rejected and on what evidence, and the terminal
  state with the honest limit above.

## Status of this mechanism

**Unrun as of 2026-07-18.** The design is written from eleven rounds of evidence,
but the loop itself has not been executed end to end. Two properties are therefore
untested: that round 2's brief in practice receives round 1's *patterns* and not
its *instances*, and that the loop reads round 1's report file rather than falling
back to re-prompting the agent. Treat both as intended behaviour, not as verified
behaviour, until a run confirms them.
