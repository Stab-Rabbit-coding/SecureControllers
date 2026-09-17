# Governed Mode — Driving an Existing Repository Federation

Read this before editing anything in a repository that already has its own policy file and task
files. The governing idea: **you are a contributor to someone else's system, not the owner of a
new one.** Everything below serves that.

## Contents

- [Why governed mode exists](#why-governed-mode-exists)
- [Detection and confirmation](#detection-and-confirmation)
- [Read the policy first](#read-the-policy-first)
- [The two-file pattern](#the-two-file-pattern)
- [Where state lives without a state file](#where-state-lives-without-a-state-file)
- [Making a change](#making-a-change)
- [Standards vetting and citations](#standards-vetting-and-citations)
- [Engineering budgets](#engineering-budgets)
- [Attribution](#attribution)
- [Commits](#commits)
- [Conflicts](#conflicts)
- [Anti-patterns](#anti-patterns)

## Why governed mode exists

A repository with an `AGENTS.md` and a maintained WBS has already answered most of the questions
this skill would otherwise ask: what a task looks like, how it gets closed, what units to use,
how to cite a standard, what a revision means. Creating a second task system alongside it does
not add organization — it splits the truth in half. Within a week nobody knows which list is
current, and the answer to "what's left?" depends on which file you opened.

So in governed mode the skill contributes process and discipline, and the repo keeps ownership
of format and policy.

## Detection and confirmation

Governed mode applies when the working tree has **both**:

- a root policy file — `AGENTS.md`, or a `CLAUDE.md` that points to one; **and**
- an existing task structure — `WBS.md`, `TODO.md`, or an equivalent the policy file names.

Announce the detection and the evidence before you act on it. If a repo has a policy file but no
task files, ask which the user wants: adopt the repo's conventions and create the task files in
that style, or run greenfield mode in a subdirectory. Don't decide that alone — it determines
where every future task lives.

## Read the policy first

Before the first edit, read:

1. The root policy file, in full.
2. The subsystem policy file matching the work's scope, if the root file federates to per-folder
   files. A subsystem file is normally authoritative inside its own scope.
3. Any federation inventory the policy names (a document listing which folders own which task
   files, and where detail is split).
4. The repo's reference catalog, if it has one, before using any citation.

This is not ceremony. These files hold the line-length caps, the citation format, the units
convention, and the close-out order that make an edit acceptable rather than something the user
has to revert.

## The two-file pattern

Repositories that federate a WBS commonly split the record in two, and the split has a purpose
worth respecting:

- **`WBS.md` — the full historical record.** Every task ever defined, open or closed, with the
  notes and rationale. Closed items stay, checked, forever. This is what makes project
  progression legible a year later.
- **`TODO.md` — only what is still open.** One short line per item, pointing back to the
  `WBS.md` entry. This is the "what's actually left" view, and it earns its keep by staying
  short.

The consequence for how you work: **`TODO.md` is generated from `WBS.md`, never the reverse.**
Close an item in the `WBS.md` that owns it first — with the notes explaining *why* it closed —
then prune the matching line from `TODO.md`. Editing `TODO.md` as if it were the source of truth
produces a file that disagrees with the record, and the record is what gets trusted.

Watch line-length and formatting caps. If the policy says items are one line of 70 characters or
fewer with no prose, a three-line item with an explanatory paragraph is a defect even if the
content is correct — it breaks the scannability the file exists for.

### Never leave a resolved item unchecked

If an item's own text says it is resolved, superseded, obsolete, or done, close it out in the
same edit. An unchecked box whose text reads "resolved 2026-07-18" is worse than no entry: it
makes every other unchecked box less believable, and the next person has to re-verify the whole
list. This applies whenever you touch a task file, not only to items you were sent to change.

## Where state lives without a state file

Governed mode has no `status.json`. State is derived, and derivation is the point — a state file
would be a second thing to keep in sync with the checkboxes, and it would lose that race.

| Concept | Where it lives in governed mode |
| --- | --- |
| Task exists | A heading or checkbox line in the owning `WBS.md` |
| Task open / closed | The checkbox state, `[ ]` or `[x]` |
| Task detail, rationale | The subsystem `WBS.md` section the root indexes |
| Dependencies | Stated in the task's detail entry |
| Reopened for rework | Unchecked again, with a dated note saying what invalidated it |
| Impact notes | Written into the dependent task's own entry |
| Who did it, when | Git history |

For the dashboard, count checkboxes. For "what changed recently," read `git log`. If the user
wants elapsed-time tracking in governed mode, ask where they want it recorded rather than
introducing a state file on your own.

## Making a change

The sequence that keeps root and subsystem files consistent:

1. **Locate the owner.** Find the subsystem `WBS.md` that owns the branch. The root file is
   usually an index, not the place detail belongs.
2. **Write the detail there** — full notes, rationale, sub-steps, citations.
3. **Update the root index line** if the root tracks that item, respecting its length cap.
4. **Prune or add the `TODO.md` line** in both the subsystem and the root, matching format.
5. **Update any file index** the policy requires when files were added, moved, or archived.
6. **Re-read what you wrote** and confirm the caps and formats hold.

When a task list is generated from another file, regenerate it rather than hand-patching both —
hand-patching is where drift starts.

## Standards vetting and citations

If the policy requires design decisions to be vetted against published standards, that applies
to work this skill plans, not just to code it writes. Practically:

- Look up a standard by its catalog ID before citing it. If it isn't catalogued, add it with a
  **validated URL** and the **exact section**, then cite the ID.
- **Never guess a section number.** A plausible-looking wrong section is more damaging than an
  admitted gap, because it survives review. If it can't be verified, mark it "requires
  verification" and raise it as an open item.
- Use the repo's citation format exactly as written.

## Engineering budgets

On a hardware project, a task is not decomposed until its physical cost is accounted for. Mass,
balance/CG shift, power draw, volume, and clearance are task outputs, not afterthoughts — a WBS
that defers them produces a design that reaches fabrication with unquoted numbers, and the
correction at that point is expensive.

Follow the repo's units convention precisely. Where a repo specifies imperial-primary with
metric in parentheses, and distinguishes mass from force, honor both: `2.5 lbm (1.13 kg)` for
mass, `4.8 lbf (21.4 N)` for force, and never a bare "lb" where the distinction matters. Getting
this wrong in a plan propagates it into every task that reads the plan.

## Attribution

Where the repo requires AI work to be distinguished from human work, mark it. Where it requires
each model to be cited separately, name the specific model rather than "AI" — a record that
lumps models together cannot be audited afterward, which is the entire reason the rule exists.
Credit human contributors the way the policy specifies.

## Commits

Follow the repo's git policy rather than habit. Common requirements worth checking for: create
new commits rather than amending, never bypass hooks or signing, never force-push the default
branch, use a heredoc for multi-line messages, and credit the authoring model in a trailer.

## Conflicts

1. Subsystem policy governs within its own scope; the root policy governs project-wide.
2. **Root and subsystem policy contradict each other → stop and ask the user.** Do not pick a
   side, and do not average them.
3. A verified reference catalog outranks a comment or an assumption.
4. Actual file and code state outranks stale documentation — if they diverge, fix the
   documentation to match reality and note why it diverged.
5. Task unclear or information missing → ask. Never invent the detail.

## Anti-patterns

Each of these has a specific failure mode, which is why it's listed:

- **Creating `projects/` in a governed repo** — splits the truth; both lists rot.
- **Editing the open-items file as the source of truth** — the record and the summary disagree,
  and the record wins in review, so the work is lost.
- **Closing a root index line without closing the detail entry** — the project looks finished
  while the actual work is still open.
- **Adding prose to a file capped at one line per item** — destroys the scannability the file
  exists to provide.
- **Citing a section number you didn't verify** — survives review, and is discovered late.
- **Leaving a "TBD" mass or power figure** — the number is never filled in later; it ships.
- **Introducing a state file "just for the dashboard"** — becomes stale within days and then
  actively misleads.
