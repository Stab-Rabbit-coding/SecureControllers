# Impact Extraction and Propagation

Read this when a task is being completed.

## The problem this solves

In a multi-task project, task 2 makes decisions — a schema, an interface, an error format, a
library choice — that task 7 will be built on top of. Nobody writes those decisions down where
task 7 will see them, because at the time they felt like local implementation detail. Six tasks
later, task 7 is built against an assumption that stopped being true, and the conflict surfaces
during integration, which is the most expensive place to find it.

Extraction and propagation is the fix: when a task finishes, pull out what it decided that
*other* tasks need, and push it into those tasks' files so it is waiting there when they start.

## When it runs

Automatically, whenever a task is marked `completed` — including re-completion after rework.

## What to extract

Eight categories. They're separated because each one has a different audience and a different
failure mode when it goes unrecorded.

| Category | Capture | Example |
| --- | --- | --- |
| **Data structures** | Tables, fields, types, units added or changed | `user(id, name, role)`; mass in grams |
| **Interface contracts** | Endpoints, function signatures, events, message formats, pinouts, connector definitions | `POST /api/v1/auth/register`; `event: order.created` |
| **Conventions** | Naming, framework, and the unspoken choices — error shape, logging, null handling, where validation lives | PascalCase; `{code, msg}` errors; validation at the boundary |
| **Files and modules** | What was created or modified | `src/models/user.js`; `airframe/wing.scad` |
| **Dependencies and config** | Packages with versions, environment variables, build/CI settings, part numbers | `bcrypt@5.1`; `JWT_SECRET`; MPN for a selected component |
| **Key decisions** | What was chosen **and what was ruled out**, with the reason | "JWT, not sessions — mobile client can't hold a cookie" |
| **Reusable utilities** | Signatures of helpers others should use rather than rewrite | `verifyToken()`, `hashPassword()` |
| **Risks and edge cases** | Assumptions about external behavior, timing dependencies, known gotchas, physical margins | "third-party API has no retry"; "clearance margin is 2 mm" |

**Record what was ruled out, not just what was chosen.** Without it, a later task re-proposes
the rejected option, the discussion repeats, and sometimes the rejection is reversed by accident
because nobody remembered the reason.

On hardware projects, mass, CG shift, power draw, and clearance changes belong in *Data
structures* or *Risks* every time — those are exactly the values other tasks are budgeting
against.

## Output format

Write into the task file's `Impact Output` section:

```markdown
## Impact Output

**Type:** Data structures
**Content:** user table — user(id, username, password_hash, role, created_at)
**Affects:** every task using user_id as a foreign key

**Type:** Interface contracts
**Content:** API prefix /api/v1/auth; POST /register; emits event user.created
**Affects:** product module, order module
```

Each entry names what it affects. That field is what drives propagation, and writing it forces
the question "who else cares about this?" while the context is still fresh.

## Propagation

For each task not yet complete:

- **It depends on the finished task** → convert the impact entries into pre-start notes and
  append them to that task's `Pre-start Notes` section.
- **It doesn't formally depend on it, but the impact is plainly relevant** — a shared schema, a
  project-wide convention, a framework choice, a shared power or mass budget → append anyway.

**Prefer over-notifying.** A note someone skims and discards costs a few seconds. A note that
was never delivered costs a rebuild. The asymmetry is large enough that the judgment call should
always break toward sending it.

Date each note and name the task it came from, so a reader can tell a current constraint from a
stale one.

In governed mode, "the task's file" is the task's entry in the owning `WBS.md`. Write the notes
there, in that repo's format.

## What this cannot catch

Two blind spots, stated because pretending they don't exist is how they bite:

- **Implicit conventions.** Choices made in code without ever being discussed — one task uses
  `null`, another `undefined`; one logs to stdout, another through a library. Nothing was
  decided, so nothing gets extracted. These surface in code review, not here.
- **External drift.** These categories record *what was assumed* about a third-party API, a
  dependency version, or a supplier's part. They cannot record whether the assumption is still
  true next month. Anything time-sensitive should be written as a risk with a date attached.

This is the concrete reason to ask the user to check the extraction rather than accepting it
silently: they hold the project's implicit context, and no extraction from a transcript can.

## Re-completion after rework

When a reopened task finishes again:

1. **Replace** the old impact output — do not append. Two sets of contradictory notes are worse
   than one set that might be stale, because a reader can't tell which is current.
2. Propagate the new notes, marking clearly what changed.
3. Check whether any blocked task is now unblocked, and say so in the dashboard.
4. Add a revision-history row giving the reason for the rework.
