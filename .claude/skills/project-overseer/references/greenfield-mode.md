# Greenfield Mode — Creating a Project Structure

Read this when the working directory has no existing governance to defer to, and this skill owns
the project files.

## Layout

```text
projects/<project_name>/
├── plan.md                # Requirements, WBS, estimate table, revision history
├── project-standards.md   # Merged from templates/, confirmed by the user
├── REFERENCES.md          # Vetted external sources (see external-source-vetting.md)
├── status.json            # Machine-readable state
└── tasks/
    ├── <task-name>.md     # One file per task
    └── ...
```

Archived projects move to `projects/_archived/<project_name>-<YYYY-MM-DD>/`.

One task, one file. That is what makes the context isolation work: entering a task loads that
file and nothing else, so a twenty-task project never has to fit in one conversation.

## plan.md

```markdown
# Project: <name>

## Basics

- Goal:
- Deliverables:
- Time constraint:
- Resources:
- Known risks:

## Work Breakdown Structure
<numbered tree, e.g. 1.1, 1.2, 2.1>

## Estimate Table
| Task | Effort (opt / likely / pess) | Expected | Feasibility | Tech requirements | Approach | Dependencies | Risk |
|---|---|---|---|---|---|---|---|

## Current Phase
Phase <n>: <name>

## Revision History
| Date | Change |
|---|---|
| YYYY-MM-DD | Initial plan |
```

Three-point estimates are not busywork. A task estimated 2h / 3h / 4h and a task estimated
1h / 3h / 20h have the same "likely" value and completely different risk, and only the spread
tells you which one to schedule early. Where a project has physical deliverables, the estimate
table is also where mass, power, and volume budgets get their first numbers — quote real ones,
never "TBD."

## status.json

```json
{
    "project": "project name",
    "schema": "1.0",
    "phase": 4,
    "time_tracking": true,
    "tasks": [
        {
            "id": "1.1",
            "name": "User Module",
            "status": "completed",
            "file": "tasks/user-module.md",
            "dependencies": [],
            "has_impact_output": true,
            "started": "2026-06-01T09:00:00-04:00",
            "ended": "2026-06-01T11:30:00-04:00",
            "duration_seconds": 9000
        }
    ],
    "current_task": null,
    "updated": "2026-06-01T12:00:00-04:00"
}
```

Indent with 4 spaces. Timestamps are ISO 8601 with an explicit offset — a bare local timestamp
becomes ambiguous the moment the project crosses a machine or a timezone.

**Status values**: `pending`, `in_progress`, `completed`, `blocked`, `reopened`.

`reopened` means a task that was finished and has been unlocked because something invalidated
it. It behaves like `pending` — it can be started — but its discussion log is preserved, so the
rework is incremental rather than a restart from nothing.

## Task file

Every task file carries these sections. Keep the empty ones present rather than omitting them;
a missing section reads as "nothing to say here" when it usually means "nobody filled this in."

```markdown
# Task: <name>

## Basics

- Project:
- Dependencies:
- Expected effort:
- Feasibility:
- Tech requirements:
- Approach:

## Pre-start Notes
<populated automatically from completed dependencies>

## Discussion Log
### YYYY-MM-DD HH:MM
<what was decided, and why>

## Impact Output
<populated on completion; see impact-propagation.md>

## Revision History
| Rev | Date | Reason | Completed by |
|---|---|---|---|
| 1 | YYYY-MM-DD | Initial completion | <model or person> |
```

Record *why* a decision was made, not only what was decided. The rationale is what lets a future
reader — including a future session of yourself — tell whether a change is safe. "Chose JWT" is
a fact; "chose JWT because the mobile client can't hold a session cookie" is a constraint you
can check against later.

Name task files in kebab-case matching the task name, so the filesystem stays predictable.

## File naming and portability

Avoid spaces in project and task directory names; use kebab-case. A space in a path is a
recurring source of broken commands and quoting bugs, and it makes the project harder to script
against later.

## Standards file

Generate `project-standards.md` in Phase 3 by reading the language template, then layering a
project-type template and any relevant supplementary templates from `templates/`. Merge them —
don't concatenate blindly; where two templates state the same rule, keep one copy.

Ask the user to confirm before decomposition begins. Standards that arrive without agreement get
ignored in practice, and a standards file nobody follows is worse than none because it makes
review results ambiguous.

## Lessons capture at close-out

When the project completes, offer to write what was learned somewhere durable — the default is
`projects/_lessons/<project_name>.md`. Worth capturing: the tech stack and why it was chosen,
architecture decisions and what was ruled out, conventions that emerged during the work, and
estimates that turned out badly wrong along with the reason. That last one is the most valuable
and the most often skipped: an estimate that was off by 4x is a reusable lesson about a whole
category of task.

Only write this if the user says yes.
