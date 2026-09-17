---
name: fleet-qa-loop
description: Use to QA a target until clean - runs mechanical linters (auto-fix) first, then loops the qa/audit subagent fleet, fixing findings until lint is clean, tests are green, and every agent returns PASS. Generalised to any language/target. Invoke when the user asks for a "qa pass", "lint and clean up", "fleet qa loop", or "loop til clean" on code.
---

# Fleet QA Loop (loop-til-clean)

A generalised, **loop-until-clean** quality pass for any target. Cheap mechanical
linters run first and auto-fix what they safely can; then the qa/audit subagent
fleet handles judgment-level issues. The loop repeats until the target is clean
(lint green, tests green, every dispatched agent returns `AGENT_VERDICT: PASS`) or
progress stalls.

**Announce at start:** "Using fleet-qa-loop to QA `<target>` until clean."

## Inputs

- **target** (arg): a path (file / dir / repo), a PR, or "current working tree".
  Default to the current repo/branch if none given.
- Work on a branch, never straight on the default branch. Commit only when the
  user has authorised it.

## Two ordering rules (non-negotiable)

1. **Mechanical before fleet.** Never pay agents to find missing-import or
   formatting nits a linter finds for free. Linters first, agents second.
2. **Tests stay green between every change.** Re-run the target's tests after any
   edit (yours or an agent's). A red test bar halts the loop until fixed.

---

## Step 0 - Detect the target toolchain (never assume)

Probe what's actually installed with `command -v` before invoking anything; skip
and *note* absent tools (don't fail the whole loop on one missing linter).

| Target | Lint / format | Tests | Notes |
| -------- | --------------- | ------- | ------- |
| Python | `ruff check --fix`, (ruff format / black) | `pytest`, `python -m py_compile` | `ruff` is fast + auto-fixes |
| JS/TS | `eslint --fix`, `prettier -w`, `tsc --noEmit` | `vitest`/`jest` | |
| Go | `golangci-lint run`, `gofmt -w`, `go vet` | `go test ./...` | |
| Rust | `cargo clippy --fix`, `cargo fmt` | `cargo test` | host may lack the toolchain - verify, else skip+note |
| Shell | `shellcheck`, `shfmt -w` | - | |

Detect by files present (`pyproject.toml`/`*.py`, `package.json`, `go.mod`,
`Cargo.toml`, `*.sh`). A polyglot repo runs each relevant toolchain.

## Step 1 - Mechanical lint (auto-fix, then triage)

1. Run the linter; **apply safe auto-fixes** (`ruff check --fix`, `eslint --fix`,
   `gofmt -w`, etc.).
2. Re-run to confirm the fixes introduced nothing new. Re-run tests.
3. Run the provenance check (Step 1b) alongside the linter - e.g.
   `scripts/check-claims.sh` where the target has one. It is cheap and mechanical,
   so it belongs here, before any agent is paid to think.
4. Triage what the linter could NOT auto-fix:
   - **Real bugs** (undefined name, unreachable code, broken import) -> fix by
     hand and verify each.
   - **Judgment calls** (unused variable/assignment, dead code, complexity) ->
     carry to the fleet step. **Do NOT blind-delete "unused" code** - an unused
     computed value is often a *missing-use bug*, not dead code. Apply
     Chesterton's fence: understand why it's there before removing it.

## Step 1b - Provenance: the tree's own claims are not evidence

A comment that asserts what an external system does - a compositor, a GPU driver,
a kernel, a specific version of some other program - cannot be checked by reading
the code, and no test covers it. It is invisible to every other stage of this
loop. And because it *reads* like hard-won field knowledge, the next reader
(human or agent) will take it as established and reason from it.

That is how a fabricated rationale becomes load-bearing. Assume it has happened.

- **Never treat an in-tree rationale as a verified fact.** A comment, a commit
  message, a docstring, a `NOTE:` - these are claims by a previous author, at the
  same evidentiary level as a finding. If you are about to use one as a reason to
  keep, change, or not-change code: check it, or mark it unchecked.
- **Ask what hardware and software the claim needs, then ask whether anyone had
  it.** A claim about NVIDIA behaviour written on an AMD-only machine, or about a
  compositor on a box with no such session, was not observed. It was invented.
  `lspci`, `$XDG_CURRENT_DESKTOP`, `$XDG_SESSION_TYPE`, `uname` settle this in
  seconds, and they are the first thing to run when a comment cites a platform.
- **Facts that ARE checkable are not suspect** - a cited spec, protocol XML, man
  page, or standard. Verify and move on. This is not a hunt for every comment.
- Mechanical support: `scripts/check-claims.sh` (if the target has one) flags
  added comments that assert external behaviour without citing a source. Run it
  in Step 1. It is a smoke alarm, not a substitute for judgment.

When a claim cannot be checked, say so in place - `UNVERIFIED:` - rather than
deleting it. It may well be true; the point is that nobody knows, and the next
reader is entitled to that.

## Step 2 - Fleet QA (judgment-level), with append-as-you-go reporting

Pick the agents that match the target's concerns and dispatch them (in parallel
where independent):

- **code-auditor** - quality, bugs, the F841-style judgment calls from Step 1
- **coverage-analyst** - test-coverage gaps + dead code
- **qa-agent** - correctness of recent changes / claimed fixes
- security/red-team (`rt-*`), `dependency-auditor` - if security/supply-chain in scope
- `a11y-auditor`, `seo-auditor`, `visual-hygiene` - for web targets
- `conformance-auditor` - implementation vs spec/README/tests

**Every dispatched agent MUST be instructed to:**

1. **Create its report file FIRST** - a skeleton with section headers - before any
   deep analysis: `<target>/docs/qa-review/<agent>.md` (or `./qa-review/<agent>.md`
   if the target isn't a repo).
2. **Append each finding to that file the moment it is found**, per
   `/media/owner/Workspace/claude-agents/REPORT_PROTOCOL.md`'s skeleton-first,
   append-as-you-go procedure - reference it, don't restate it here.
3. **Cite the failure path in every finding.** State the symptom *and* the
   `file:line` of the code path that produces it. A severity claim with no code
   path behind it is a guess wearing a lab coat - mark it `UNVERIFIED:` or drop
   it. See Step 3b.
4. **Take no runtime evidence from the user's live system.** See Step 2a.
5. **End its final message with** `AGENT_VERDICT: PASS | FAIL | NEEDS_WORK | BLOCKED`
   (PASS only if it actually verified the target is clean for its concern). This
   drives the loop's completion gate - a non-PASS verdict keeps the loop open.

## Step 2a - Runtime evidence, without touching the user's machine

An agent handed a display will use it. On a neowall QA pass, a subagent asked for
hardware evidence built the patched daemon and ran it against `DISPLAY=:0` - the
user's actual desktop. Both monitors went unusable mid-session and the daemon
rewrote `~/.config/neowall/cycle_list`. The agent was following its brief; the
brief simply never said not to.

Wanting runtime evidence was right. Taking it from the user's live session,
unannounced, was not. State the bar in the brief - **an agent will not infer it**:

- Read-only inspection of a live system is fine.
- **Starting a process against the user's display or session, or writing to
  `~/.config/**`, dotfiles, daemons or installed binaries, needs a yes first.**
- Prefer a sandbox: Xvfb, a nested compositor, a container, a VM, a scratch `HOME`.
- **If no sandbox will do:** name what you want to run and what it may disturb,
  then stop and wait. Do not proceed on your own judgement.

Boilerplate for the dispatch brief: *"Do not run anything against the user's live
session. Do not launch daemons or write outside the repo. If you believe a runtime
check is essential, say so and stop."*

## Step 2b - Adversarial verification (never trust a finding's own author)

A finding graded only by the agent that produced it is a self-assessment, and
self-assessment is how confident-but-wrong findings reach the user. Before any
finding earns a fix, it must survive an independent attempt to kill it.

For each finding from Step 2, dispatch **3 refuters in parallel**, each given the
finding, the file, and the surrounding source - but *not* the finding author's
reasoning (it anchors them). Brief each to **REFUTE**, not to review:

> Try to prove this finding is wrong. It is wrong if the code path is
> unreachable, the input can't take that value, a caller already guards it, the
> "bug" is the documented/intended behaviour, or the author misread the code.
> Default to `refuted: true` when uncertain - the burden of proof is on the
> finding, not on you. State the concrete input/state that triggers the bug, or
> concede you cannot construct one.
>
> Attack the PREMISES, not only the conclusion. If the finding leans on a code
> comment, a commit message, or any claim about what an external system does,
> check that claim yourself rather than inheriting it. An unverifiable premise
> refutes whatever was built on top of it, however good the reasoning above it.

Give the refuters **distinct lenses** where the finding could fail in more than
one way (correctness / reachability / does-it-actually-reproduce), rather than
three identical skeptics - diversity catches what redundancy can't.

- **Survives** (≥2 of 3 fail to refute) -> real; carry to Step 3.
- **Refuted** (≥2 of 3 refute) -> drop it, and record it in the report file as
  `REFUTED: <finding> - <why>`. Do not silently discard: a dropped finding is
  evidence about the fleet's false-positive rate.
- A refuter that constructs a **concrete triggering input** upgrades the finding
  to CONFIRMED and that input becomes the regression test in Step 3.

`AGENT_VERDICT: PASS` from Step 2 does **not** skip this step - an agent that
found nothing is itself a claim ("this area is clean") worth one refuter.

## Step 2c - Negative controls (a clean result from a broken instrument looks clean)

Step 2b interrogates findings: *is this claim true?* It cannot catch the opposite
failure - a control that emits the same signal whether or not the thing it checks
is true. There is no finding to refute, because the instrument produced a green
tick, and the green tick is the bug. See the `negative-controls` skill for the
pattern and its catalogue.

This step applies to two things:

**1. Controls the fleet touched or wrote.** Any test added in Step 3, any lint
rule, gate, guard, ignore rule, or checklist item in scope. For each, produce the
broken world once and observe the control fail: delete the guard, invert the
condition, misspell the name, swap the safe call for the unsafe one. Then restore
it (verify by diff) and observe it pass. Record both outcomes. A control that
passes in both worlds is not a control - strengthen it until it can fail, or
delete it and report the gap honestly.

**2. Any `AGENT_VERDICT: PASS` that rests on a check rather than on reading.**
If an agent concluded "clean" from a grep, a `check-ignore`, a `systemctl show`,
or any command whose empty output was read as absence of a problem, confirm that
command can produce non-empty output at all. Empty because clean and empty
because the command was aimed at the wrong mechanism are indistinguishable
without this.

Prioritise by the cost of silent failure: security guards (escaping, auth, bind
restrictions, credential ignore rules), then gates and flags whose whole purpose
is to prevent something, then operational checklist items that gate a release.

Where falsifying a control is genuinely impractical - it needs production
credentials, an irreversible action, hardware you do not have - mark it
**UNVERIFIED** in the report with what would verify it. Do not let difficulty
become a reason to assert it works, and do not leave it looking the same as a
control that was exercised.

## Step 3 - Triage + fix the findings

- Read each agent's **report file** (it exists on disk even if the agent died
  mid-run - that's the point of Step 2).
- Fix only findings that **survived Step 2b**.
- Fix actionable findings. For any **behaviour change**, keep or add a regression
  test for the prior behaviour and verify the new behaviour.
- For judgment calls outside the rules, flag options + a recommendation to the
  user; don't improvise irreversible choices.

## Step 3b - Re-derive every claim before it ships

Applies to every claim that leaves the loop: in a finding, a code comment, a
commit message, or the final summary.

**The failure mode: false claims are regenerated, not inherited.** An audit of six
commits on a neowall fork scored 27 claims verified, 4 false, 8 overstated, 3
unsourced. Two fresh agents were then briefed on the false claims **by name** -
told in writing that "a failed shader load leaves a black wallpaper" was false and
that the real symptom was a silently stalled cycle - and both wrote the false
version straight back into their new commit messages. The pull is toward the more
dramatic symptom: "blank screen" is a better story than "the cycle fails to
advance", so whoever holds the pen keeps writing it. **A checklist of known-bad
claims does not stop this. The mechanism is not memory.**

**The gate that does work:** hand a fresh agent the *code* and have it derive the
symptom itself. Do not hand it a symptom to check - a description handed over is a
description agreed with. Every catch in that session came from an agent that
re-read the failure path instead of trusting the sentence it was given.

Per claim:

1. **Find the failure path.** What does the *caller* do when this operation fails?
   Read that code.
2. **Judge severity against the failure path, not against the fix.** Both false
   claims above would have died in thirty seconds this way - the caller logged and
   skipped, so nothing ever blanked.
3. **Cite `file:line`.** If you cannot cite the line that produces the symptom you
   are about to assert, you have not verified it. Assert the symptom you *can*
   cite, or mark it `UNVERIFIED:`.

Treat existing comments, `NOTE:`s and commit messages as **claims at the same
evidentiary level as a finding**, never as facts to reason from. When a claim cites
a platform, check whether anyone ever had that platform: `lspci`,
`$XDG_CURRENT_DESKTOP`, `$XDG_SESSION_TYPE`, `uname` settle it in seconds. (The
neowall comment that started all this invented KWin and NVIDIA behaviour on an
AMD/X11/Cinnamon box.) Claims citing a spec, man page or protocol are **not**
suspect - verify and move on.

**Honest limits.** This lowers the rate; it does not eliminate it. Four of five
agents caught a false claim that round, which means one did not. And a pre-commit
grep for suspicious wording is a backstop, not a gate: neowall's `check-claims.sh`
never reads **commit messages** and only flags claims about **external** systems,
so "glGetError forces a synchronous flush of the GL command stream" and "a broken
shader blanks the output" both sail past it.

## Step 3c - Check each citation against the tree it names

Step 3b makes every claim carry a `file:line`. This step exists because that is
not enough.

**Specificity is not verification.** A neowall commit message said `wl->initialized`
is set at `wayland_core.c:536` of upstream commit `5aa206f`. That was **true**. A
review agent "corrected" it to `:544`, and the correction was propagated into the
commit message and then into a draft issue addressed to an upstream maintainer we
had never spoken to. `:544` is where that line sits **after our own patch is
applied**. The reviewer had measured the working tree it had checked out, not the
commit the sentence cited. A true claim was turned into a false one, one step from
being posted in public against a hash where it demonstrably is not true.

It survived **three** reviews. Each reviewer checked the claim against the tree in
front of it, which is the natural move and is silently wrong whenever the sentence
names a different commit. It was caught only when one agent stopped reading the
prose and ran `git show 5aa206f:<path>` to look at the blob.

Note what this defeats: Step 3b's rule was *followed*. The citation existed, it was
specific, and it was wrong. Specificity feels like rigour, and that feeling is the
trap.

Per citation:

1. **Name the tree.** A `file:line` is true only relative to one. An uncited
   citation silently means "the tree I have checked out", and it stops being true
   the moment anyone patches that file.
2. **Read the blob, not the working copy.** `git show <cited-sha>:<path> | sed -n
   '<line>p'` and confirm the line says what the sentence says. Opening the file in
   the editor measures *your* tree, and your tree already carries the patch that the
   sentence is about. Line numbers move under the very change being described.
3. **Anything going outward gets this on every citation.** An issue, a PR, a comment
   on someone else's repo: check each `file:line` at the blob before it ships.
4. **Cite only commits the reader can resolve.** A branch carrying fork-local
   scaffolding commits quotes hashes that dangle for anyone outside the fork. Squash
   before submitting.

## Step 4 - Loop / terminate

Re-run Step 1 (lint + tests), then **re-dispatch the same agent type** until it
returns `AGENT_VERDICT: PASS`. Each round:

- **CLEAN** (terminate success): lint clean, tests green, all agents PASS, every
  surviving claim cites the failure path that produces it (Step 3b), and every
  citation has been checked against the tree it names (Step 3c).
- **STALLED** (terminate, report): the identical finding survives two rounds, or
  an agent returns `BLOCKED`, or you hit the **iteration cap (default 5)**. Stop -
  do not spin. Report exactly what remains and why, with the report files as
  evidence.

## Output

- Per-agent report files under `docs/qa-review/` (append-as-you-go, survive
  truncation).
- A short final summary to the user: what was auto-fixed, what bugs were fixed by
  hand, what the fleet found, what was fixed vs deferred, and the terminal state
  (CLEAN or STALLED-with-reason).

## Pitfalls (learned)

- **Verify every tool exists** before invoking it; skip + note absent ones rather
  than crashing the loop.
- **Mechanical first, agents second.**
- **Don't blind-delete "unused" code** - Chesterton's fence; it may be a latent
  missing-use bug.
- **Keep tests green** between every single change.
- **Append findings as you go** - a long auditor agent can truncate before a
  deferred final write; skeleton-first + append is the mitigation.
- **Honest verdicts only** - PASS means verified clean, not "I ran out of things
  to say." A false PASS defeats the loop.
- **Never ask an agent to *describe* a symptom.** Ask it to state the symptom and
  cite the `file:line` of the failure path that produces it.
- **Briefing an agent on a false claim does not immunise it against that claim.**
  Two agents told a claim was false reproduced it anyway. Make the reviewer
  re-derive the symptom from the code; don't give it the answer to grade.
- **A `file:line` is only true against a named tree.** Check it with `git show
  <sha>:<path>`, never by opening the working copy - line numbers move under the
  patch the sentence is describing. A reviewer that skipped this "corrected" a true
  citation into a false one, and the false version survived three more reviews.
- **The user's live session is not test hardware.** Sandbox it, or name what you
  want to run and wait for a yes.
- **Never fix an unrefuted finding.** Acting on a plausible-but-wrong finding is
  worse than missing it: it churns working code and burns the loop's credibility.
  Step 2b is the gate.
- **Never write a comment asserting external behaviour you have not observed.**
  Inventing a plausible reason ("KWin closes this surface", "the driver rejects
  that flag") to justify a change plants a fact that no test covers and no reader
  can check, and it will be believed. If you cannot verify it, either don't claim
  it or mark it `UNVERIFIED:`. This applies to commit messages too.
- **The tree lies, and it lies with confidence.** The failure that motivated
  Step 1b was real: a comment on an AMD/X11/Cinnamon machine confidently
  described KWin's behaviour on NVIDIA under Wayland. It was read back as
  evidence, quoted to the user as their own field observation, and nearly decided
  a design question - none of which requires anyone to be careless, only for a
  comment to look like knowledge. Check the platform a claim needs before you
  spend it as currency.
