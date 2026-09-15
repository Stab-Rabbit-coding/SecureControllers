# Change Management — Requirements That Move

Read this when something invalidates work that is already planned or finished.

Requirements change. A plan that can only absorb changes by restarting is a plan people abandon
rather than update, and an abandoned plan is how a project ends up with no record at all. The
goal here is that a change costs proportionally to its actual blast radius — not the whole
project, and not nothing.

## Two directions

**Bottom-up** — work inside a task reveals that finished work is wrong. Someone building the
order module discovers the user schema can't represent what's needed.

**Top-down** — the user introduces a new or changed requirement at the top level.

Both converge on the same sequence: **assess, report, get approval, then change.** Never modify
the plan before the assessment has been seen. An unassessed change looks small and quietly
reopens six tasks; the assessment is what makes the real cost visible while it's still a
decision.

## Bottom-up

When a conflict surfaces during a task, raise it immediately rather than working around it. A
local workaround for a structural conflict is technical debt created deliberately and forgotten
instantly.

State it concretely — which task, which shared thing, what the conflict actually is:

> The approach here needs a `role` field on the user record. Task 1.1 is complete and its schema
> doesn't have one, and tasks 2.1 and 3.4 were built against that schema. Reopen 1.1?

On approval: reopen the affected task, mark its impact output superseded, update the dependents'
pre-start notes with what changed, and tell the user which task to revisit first.

## Top-down

On `add requirement <desc>` or `impact analysis`, assess **every** task — pending, in progress,
and completed. Completed tasks are the ones that matter most here, and the ones most often
skipped, because it's tempting to treat "done" as settled.

For each task ask: does this change its scope? its dependencies? its estimate, feasibility, or
approach? Then report:

```text
Impact of: <the change>

  1.1 Database schema    [COMPLETED]  → affected: needs a role column; reopen
  1.2 Registration       [COMPLETED]  → not affected
  2.1 Product module     [pending]    → scope grows; re-estimate 4h → 7h
  2.4 Permissions        [NEW]        → new task; estimate below
  3.1 Frontend           [pending]    → not affected

  Net: +1 new task, 1 reopened, 1 re-estimated.
  Progress goes from 5/8 to 5/9 with 1 reopened.

Approve?
```

Show the progress change explicitly. "5/8 complete" becoming "5/9 with one reopened" is the
honest picture, and it's what lets the user decide whether the change is worth it.

On approval: update the plan and estimate table, create any new task files, set affected
completed tasks to `reopened`, mark their impact outputs superseded, refresh dependents'
pre-start notes, and add a revision-history row. Then report the new state.

If the user declines, record that too — a considered rejection is project history worth keeping,
and it stops the same proposal from being re-litigated later.

## What happens to a reopened task

Five properties, each protecting something:

1. **The discussion log is preserved.** The original reasoning stays readable, so rework can be
   surgical instead of a rediscovery exercise.
2. **The old impact output is marked superseded, not deleted.** Dependents may have been built
   against it, and knowing what they were built against is how you find what needs fixing.
3. **Pre-start notes explain what changed and why**, so whoever picks it up starts oriented.
4. **Dependents are re-evaluated** — some may become blocked again.
5. **Rework is incremental.** Discuss what changed, not the whole task from scratch.

## Governed mode

Same logic, different mechanics. There is no status field, so reopening means unchecking the box
in the owning `WBS.md` and adding a dated note stating what invalidated it and which change
authorized the reopen. Then restore the item's line in the matching `TODO.md`.

Never silently uncheck a box. An item that goes from done to open with no recorded reason makes
the whole record untrustworthy — and the record is the only durable artifact the project has.

If the repo uses revision letters or numbered modifications, follow its convention for labeling
the change. Ask rather than guess which one applies; the distinction usually carries meaning
about scope that isn't yours to assign.
