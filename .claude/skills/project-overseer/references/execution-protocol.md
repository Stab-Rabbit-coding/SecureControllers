# Execution Protocol — Context Switching and Integrity

Read this before the first task switch of a session. The protocols below exist because a context
switch is the moment a file-based project is most likely to lose data: the conversation still
holds the work, the file does not yet, and one more step in either direction decides which
survives.

## Entering a task — `start <task>`

**1. Validate the request.**
Check the task's current state before doing anything else:

- `completed` → refuse. Explain that finished tasks are reopened deliberately, via `reopen
  <task>` or a requirement change, so that reopening always leaves a reason in the record.
- `in_progress` → warn that a session is already open on it, and confirm before continuing.
- `blocked` → say what it's blocked on and confirm the user wants to start anyway. Sometimes
  they legitimately do; make it a decision rather than an accident.
- `pending` or `reopened` → proceed.

**2. Record the start.** Set the start timestamp if time tracking is on.

**3. Load the task file.** If it's missing, stop, report the exact path, and list what does exist
in `tasks/`. Do not reconstruct the task from the plan and carry on — a reconstructed task file
silently discards whatever discussion the real file held.

**4. Update state.** Mark the task in progress and set it as the current task.

**5. Orient.** Show the basics and the pre-start notes, and summarize the standards that apply.
The pre-start notes are the highest-value part of this step — they carry what earlier tasks
decided that constrains this one, and reading them is what stops the project from contradicting
itself.

Then tell the user where the file is and that you're ready to work in it.

## Returning to the top level — `back to master`

**1. Confirm you're in a task.** If not, say so and render the dashboard.

**2. Save first, always.** Append the discussion to the task file's log under a
`### YYYY-MM-DD HH:MM` heading, then verify the file reads back correctly. This happens before
anything else, because every later step can be redone and this one cannot.

**3. Handle completion.** If the user marked the task done during the session:

- Record the end time and duration.
- Set status to `completed`.
- Run impact extraction and propagation — see `impact-propagation.md`.
- Tell the user what was extracted and which tasks received notices, and ask them to check it.

If they did not mark it done, leave it `in_progress`. Do not infer completion from the
conversation sounding finished; an unfinished task marked complete stops receiving the impact
notices it still needs.

**4. Load the top level.** Read the plan and the state, read the impact outputs of completed
tasks in dependency order, and render the dashboard.

## Integrity check

Run this after every switch, before continuing work. It takes seconds and it catches the class
of problem that is nearly impossible to untangle once more work is layered on top.

**Files exist.** The plan file, the state file, and the current task's file if one is set. Any
missing → report exactly which, list what exists, and stop.

**State parses and agrees with the filesystem.** If the state file won't parse, show the error
and the raw content and ask how to recover — don't rewrite it from inference. Then compare: the
number of tasks in state versus the number of files in `tasks/`. A mismatch means one of them is
wrong, and the user needs to know which they'd rather trust. Validate that every status value is
one of the allowed five.

**Current task is consistent.** If a current task is set, its file exists and its status is
`in_progress`. If none is set, no task should be sitting in `in_progress` — a stranded
`in_progress` task usually means an earlier session ended without saving, and its file may be
missing the last discussion.

**Report, don't repair.** If a check fails, present the finding and wait. Auto-repairing state
can destroy the evidence of what actually went wrong, and the user may know something you can't
see — such as which of two conflicting files they were editing by hand.

In governed mode there is no state file, so the equivalent check is narrower: confirm the task
files named in the index exist, and confirm no item is checked in one file and unchecked in
another. Cross-file checkbox disagreement is the governed-mode analogue of corrupt state.

## Session recovery

If a session begins with a task already marked `in_progress`, the previous session ended without
returning to the top level. Say so plainly, show the task's last logged entry with its
timestamp, and ask whether to resume it or close it out. Note explicitly that anything discussed
after that last entry was not saved — the user is the only one who can tell you what's missing.
