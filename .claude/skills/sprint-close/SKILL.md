---
name: sprint-close
description: "Close a sprint of a sprint-based plan (for example the Open-Secure-ESC 70 A nacelle-64 ESC plan). Runs ce-doc-review, ce-compound-refresh, ce-code-review, ce-compound, ce-handoff and ce-commit-push-pr in order, scoped to what the sprint touched. Use at the end of every sprint, or when a sprint hits its usage stop line."
argument-hint: "<U-ID, e.g. U1> [plan path; default: the plan the sprint belongs to]"
---

# Sprint Close

Run this at the end of each sprint of a sprint-based plan under
`docs/plans/`, for example Open-Secure-ESC's
`docs/plans/2026-11-22-001-feat-70a-nacelle64-esc-sprint-plan.md`. Also run
it when a sprint reaches the plan's usage stop line (about 70 % of the usage
window), even if the sprint is not finished. The repo's `AGENTS.md` (or
`CLAUDE.md`) governs every step.

The six steps run in a fixed order. Each step scopes its skill to what this
sprint touched, which keeps the close-out inside the window.

## Inputs

- **U-ID** (required): the sprint's unit, for example `U1`.
- **Plan path** (optional): defaults to the plan in `docs/plans/` whose
  Implementation Units contain the U-ID. If more than one plan matches, ask.

Before step 1, take one snapshot of the sprint's scope:

1. List the files this sprint changed: `git diff --name-only <base>...HEAD`
   plus uncommitted changes. `<base>` is the branch point from `main`.
2. Sort the files into three groups:
   - **docs**: `*.md`;
   - **code**: `*.py`, firmware sources and CI files;
   - **design**: `*.kicad_*`, `*.json` specs and gerbers.
3. Pass the snapshot to every step below. Do not re-scan the tree per step.

## Steps

Run every step. If a step cannot run, record why in the handoff (step 5)
and go on. Never skip a step to save tokens. Use its narrowest scope.

1. **`/ce-doc-review`** in `mode:non-interactive`:
   - Review the plan file, plus each new or changed doc in the "docs" group
     except `TODO.md`.
   - Apply only the `safe_auto` fixes.
   - Carry the remaining findings to step 5.
2. **`/ce-compound-refresh`** in `mode:non-interactive`:
   - Give it a scope hint: the modules or directories the sprint touched.
   - Refresh only the `docs/solutions/` learnings that those paths make stale.
3. **`/ce-code-review`** on the current branch:
   - If the "code" and "design" groups are empty, ask for a quick review.
   - If either group has files, run the full review.
   - The review is report-only. Fix real findings in the sprint, or carry
     them to step 5.
4. **`/ce-compound`** in `mode:non-interactive depth:lightweight`:
   - Add the sprint's one hard-won lesson to `docs/solutions/` (`AGENTS.md`
     §4.1), with frontmatter `applies_when`.
   - If the sprint taught nothing new, record "none" in the handoff and
     write no file.
5. **`/ce-handoff create <U-ID>`**. Write it to
   `docs/handoffs/<date>-<U-ID>-<slug>.md` in the repo, not the managed
   `/tmp` store: the cloud container is reclaimed after the session, so a
   `/tmp` handoff does not reach the next sprint. The handoff states:
   - what changed and the exit-gate result;
   - every open finding from steps 1–3;
   - every `UNVERIFIED` item added, with its `TODO.md` line;
   - the budgets (mass in lbm, loss in W, clearance in in (mm));
   - the next sprint's first read (its plan section and files).
6. **`/ce-commit-push-pr`**, after the gates and the close-out record
   below are done:
   - Commit on the session's development branch.
   - Push, and update the open PR for the branch (or open a draft PR if none
     is open).
   - Never push to `main`.

## Gates before step 6

Run each gate on the files in the snapshot:

- `markdownlint-cli2` on changed `*.md` files, with the repo's own config.
  If CI does not pin the linter version, say so in the handoff.
- If the repo has `tools/precommit_doc_wording.py`, stage the changed docs
  first, then run it. It takes no arguments and checks staged `*.md` files
  only, so an unstaged doc is not checked (Open-Secure-ESC
  `docs/solutions/developer-experience/doc-wording-check-reads-staged-files-only.md`).
- For each touched board, run ERC/DRC per the plan's Verification Contract.
  Document every remaining violation by rule and reason.
- Run the repo's review checklist on the diff (Open-Secure-ESC:
  `AGENTS.md` §5).

If a gate fails, fix the cause and re-run that gate. Never disable a check to
pass it.

## Close-out record (after the gates, before step 6)

In the plan's owning `TODO.md` index line (Open-Secure-ESC: §19):

- check the line if the sprint's exit gate passed;
- otherwise leave it open, with a dated note naming the blocker.

The `TODO.md` line indexes the plan. Record the detail (what closed and why) in
the plan's handoff and the build README first, then check or prune the §19
line. If a gate result changes the handoff, update the handoff before step 6.
