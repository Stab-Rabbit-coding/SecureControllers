---
name: doubt-driven-development
description: Subjects every non-trivial decision to a fresh-context adversarial review before it stands. Use when correctness matters more than speed, when working in unfamiliar code, when stakes are high (production, security-sensitive logic, irreversible operations), or any time a confident output would be cheaper to verify now than to debug later.
---

# Doubt-Driven Development

## Overview

A confident answer is not a correct one. Long sessions accumulate context that quietly turns assumptions into "facts" without anyone noticing. Doubt-driven development is the discipline of materializing a fresh-context reviewer — biased to **disprove**, not approve — before any non-trivial output stands.

This is not `/review`. `/review` is a verdict on a finished artifact. This is an in-flight posture: non-trivial decisions get cross-examined while course-correction is still cheap.

## When to Use

A decision is **non-trivial** when at least one of these is true:

- It introduces or modifies branching logic
- It crosses a module or service boundary
- It asserts a property the type system or compiler cannot verify (thread safety, idempotence, ordering, invariants)
- Its correctness depends on context the future reader cannot see
- Its blast radius is irreversible (production deploy, data migration, public API change)

Apply the skill when:

- About to make an architectural decision under uncertainty
- About to commit non-trivial code
- About to claim a non-obvious fact ("this is safe", "this scales", "this matches the spec")
- Working in code you don't fully understand

**When NOT to use:**

- Mechanical operations (renaming, formatting, file moves)
- Following a clear, unambiguous user instruction
- Reading or summarizing existing code
- One-line changes with obvious correctness
- Pure tooling operations (running tests, listing files)
- The user has explicitly asked for speed over verification

If you doubt every keystroke, you ship nothing. The skill applies only to non-trivial decisions as defined above.

## Loading Constraints

This skill is designed for the **main-session orchestrator**, where Step 3 (DOUBT, detailed below) can spawn a fresh-context reviewer.

- **Do NOT add this skill to a persona's `skills:` frontmatter.** A persona that follows Step 3 would spawn another persona — the orchestration anti-pattern explicitly forbidden by `references/orchestration-patterns.md` ("personas do not invoke other personas").
- **If you find yourself applying this skill from inside a subagent context** (where Claude Code prevents nested subagent spawn): the preferred path is to surface to the user that doubt-driven cannot run nested and let the main session handle it. As a last resort only, a degraded self-questioning fallback exists — rewrite ARTIFACT + CONTRACT as a fresh self-prompt with a hard mental separator from your prior reasoning, and walk Steps 1–5. This is **not fresh-context review** (you carry your own context with you), so flag the result as degraded and prefer escalation whenever the user is reachable.

## The Process

Copy this checklist when applying the skill:

```text
Doubt cycle:
- [ ] Step 1: CLAIM — wrote the claim + why-it-matters
- [ ] Step 2: EXTRACT — isolated artifact + contract, stripped reasoning
- [ ] Step 3: DOUBT — invoked fresh-context reviewer with adversarial prompt
- [ ] Step 4: RECONCILE — classified every finding against the artifact text
- [ ] Step 5: STOP — met stop condition (trivial findings, 3 cycles, or user override)
```

### Step 1: CLAIM — Surface what stands

Name the decision in two or three lines:

```text
CLAIM: "The new caching layer is thread-safe under the
        read-heavy workload described in the spec."
WHY THIS MATTERS: a race here corrupts user data and is
                  hard to detect in QA.
```

If you can't write the claim that compactly, you have a vibe, not a decision. Surface it before scrutinizing it.

### Step 2: EXTRACT — Smallest reviewable unit

A fresh-context reviewer needs the **artifact** and the **contract**, not the journey.

- Code: the diff or the function — not the whole file
- Decision: the proposal in 3–5 sentences plus the constraints it has to satisfy
- Assertion: the claim plus the evidence that supposedly supports it (kept distinct from the Step 1 CLAIM block, which is the orchestrator's hypothesis under scrutiny)

Strip your reasoning. If you hand over conclusions, you'll get back validation of your conclusions. The unit must be small enough that a reviewer can hold it in mind in one read — if it's a 500-line PR, decompose first.

### Step 3: DOUBT — Invoke the fresh-context reviewer

The reviewer's prompt **must be adversarial**. Framing decides the answer.

```text
Adversarial review. Find what is wrong with this artifact.
Assume the author is overconfident. Look for:
- Unstated assumptions
- Edge cases not handled
- Hidden coupling or shared state
- Ways the contract could be violated
- Existing conventions this might break
- Failure modes under unexpected input

Do NOT validate. Do NOT summarize. Find issues, or state
explicitly that you cannot find any after thorough examination.

ARTIFACT: <paste artifact>
CONTRACT: <paste contract>
```

**Pass ARTIFACT + CONTRACT only. Do NOT pass the CLAIM.** Handing the reviewer your conclusion biases it toward agreement. The reviewer must independently determine whether the artifact satisfies the contract.

#### Withhold the claim even when you are trying to refute it

The rule above is usually read as "don't let the reviewer agree with you." It is stronger than that: **naming a claim plants it, whether you name it as true or as false.**

On a neowall fork, two fresh agents were briefed on a false claim *by name*: told in writing that "a failed shader load leaves a black wallpaper" was false, and that the real symptom was a silently stalled cycle. Both wrote the false version back into their own commit messages anyway. Fabrication is not an inheritance problem that a warning intercepts; it is regenerated from the same pressure every time, because the dramatic symptom is the better story. A list of known-bad claims does not immunise a reviewer against them.

So when the claim under doubt is a **symptom or severity claim** ("this leaves the screen blank", "this corrupts the row", "this hangs the request"):

- The ARTIFACT is the **failure path**: the error branch and, crucially, **what the caller does on error**. Not the fix.
- Ask the reviewer to **derive** the symptom from that code, in its own words. Do not give it a symptom to grade. A description handed over is a description agreed with.
- Require a `file:line` citation for whatever symptom it derives. **A severity claim with no code path behind it is a guess wearing a lab coat.** If the reviewer cannot cite the line that produces the symptom, that is the finding.
- If your derived symptom and the reviewer's disagree, that disagreement is the most valuable output of the cycle. Re-read the failure path yourself before deciding which is right.

This lowers the rate; it does not eliminate it. In the neowall audit, four of five independent re-derivations caught a false claim, which means one did not.

#### When the claim names a commit, the ARTIFACT is that commit's blob

A reviewer reviews what you hand it. Hand it the wrong tree and it will review the wrong tree with full confidence, and that confidence will read back to you as verification.

The same neowall fork carried a commit message saying `wl->initialized` is set at `wayland_core.c:536` of upstream commit `5aa206f`. **That was true.** A review agent "corrected" it to `:544`, which is where the line sits *after our own patch is applied*. It had measured the working tree it had checked out, not the commit the sentence named. The correction was propagated into the commit message and then into a draft issue addressed to an upstream maintainer we had never spoken to. **Three** review cycles passed it. It died only when one agent ran `git show 5aa206f:<path>` and read the blob instead of the prose.

Notice what that defeats. The rule immediately above says a symptom claim must cite the `file:line` that proves it. Here the citation existed, it was specific, and it was false. **Specificity is not verification.** A precise wrong number is harder to doubt than a vague right one, because precision is what doubt usually looks for.

So when the claim under doubt cites a commit, tag or release:

- **The ARTIFACT is the blob at that ref**, fetched with `git show <ref>:<path> | sed -n '<line>p'`. Not the file on disk. The working copy is a different artifact that happens to share a filename, and the patch under review is precisely what makes them differ.
- **Never settle a citation by opening the working copy.** It is the natural move and it is silently wrong whenever the sentence names a tree other than the one you have checked out.
- **Outward-facing artifacts get every citation checked at the blob before they ship**: an upstream issue, a PR, a comment on a repo that is not yours. There the reader cannot see your working tree, and a wrong line number against a named hash is checkable by them and not by you.
- **Cite only refs the reader can resolve.** Fork-local scaffolding commits produce hashes that dangle for everyone outside the fork; squash before submitting.

In Claude Code, the role-based reviewers in `agents/` start with isolated context by design and are usable here — see `agents/` for the roster and per-domain match.

**The adversarial prompt above takes precedence over the persona's default response shape.** Personas like `code-reviewer` are written to produce balanced verdicts with both strengths and weaknesses; doubt-driven needs issues-only output. Paste the adversarial prompt verbatim into the invocation so it overrides the persona's default. If a persona's response shape can't be overridden cleanly, fall back to a generic subagent with the adversarial prompt.

#### Cross-model escalation

A single-model reviewer shares blind spots with the original author — a colder, different-architecture model catches them. Doubt-driven is already opt-in for non-trivial decisions, so within that scope offering cross-model is part of the skill's value, not optional friction.

**Interactive sessions: always offer. Never silently skip.**

##### Step 1: Ask the user

After the single-model review in Step 3 above, but before RECONCILE, pause and ask:

> *"Single-model review complete. Want a cross-model second opinion? Options: Gemini CLI, Codex CLI, manual external review (you paste it elsewhere), or skip."*

This question is mandatory in every interactive doubt cycle — even on artifacts that feel low-stakes. The user — not the agent — decides whether the cost is worth it. The agent's job is to surface the choice.

##### Step 2: If the user picks a CLI — verify, then invoke

1. Check the tool is in PATH (`which gemini`, `which codex`).
2. Test it works (`gemini --version` or equivalent) before passing the full prompt — a stale or broken binary may pass `which` but fail on real input.
3. Confirm the exact invocation with the user, including required flags, auth, and env vars (e.g., API keys). Implementations vary; never assume.
4. Pass ARTIFACT + CONTRACT + the adversarial prompt **only**. No session context, no CLAIM.
5. Mind shell escaping. If the artifact contains quotes, `$(...)`, or backticks, prefer stdin (`echo … | gemini`) or a heredoc over inline `-p "…"`. When in doubt, ask the user to confirm the invocation before running it.
6. Take the output into Step 4 (RECONCILE).

**Never interpolate the artifact into a shell-quoted argument.** Code, markdown, and review prompts routinely contain backticks, `$(...)`, and quote characters that will either truncate the prompt or execute embedded shell. Write the full prompt to a file and pipe it through stdin.

Example shapes (verify flags against your installed tool — syntax differs across implementations and versions):

```bash
# Write the adversarial prompt + ARTIFACT + CONTRACT to a temp file first.
# Then pipe via stdin so shell metacharacters in the artifact stay inert.

# Codex (read-only sandbox keeps the CLI from writing to your workspace):
codex exec --sandbox read-only -C <repo-path> - < /tmp/doubt-prompt.md

# Gemini ('--approval-mode plan' is read-only; '-p ""' triggers non-interactive
# mode and the prompt is read from stdin):
gemini --approval-mode plan -p "" < /tmp/doubt-prompt.md
```

A read-only sandbox is the load-bearing detail: a doubt artifact may itself contain instructions (intentional or accidental prompt injection) that the cross-model CLI would otherwise execute against your workspace.

##### Step 3: If the CLI is unavailable or fails

Surface the failure explicitly. Offer: run it manually, try a different tool, or skip. Do not silently fall back to single-model — the user should know cross-model didn't happen.

##### Step 4: If the user skips

Acknowledge the skip in the output (*"Proceeding with single-model findings only"*) and continue to RECONCILE. Skipping is fine; silent skipping is not.

**Non-interactive contexts** (CI, `/loop`, autonomous-loop, scheduled runs):

- Cross-model is **skipped**, and the skip must be **announced** in the output: *"Cross-model skipped: non-interactive context."*
- **Never invoke an external CLI without explicit user authorization** — this is a load-bearing safety property.

Cross-model adds cost, latency, and tool fragility. The agent surfaces the choice every cycle; the user decides whether this artifact warrants it.

#### Root-cause claims: refute before you relay

A causal claim ("X causes Y") gets the same DOUBT treatment as a code claim, with one addition: design the experiment that would disprove it, and run that one first, not the one that would confirm it. Five coherent root-cause stories were stated and believed in a single debugging session; all five were wrong, and each was killed by an experiment that could have gone either way - cutting the network refuted "the network is the problem" in one run.

**A hypothesis that only restates the symptom is not a hypothesis.** "It times out" and "it's environment-dependent" rename the observation instead of explaining it. Ask: what would I see if this were not true? If the answer is "the same thing", it's a paraphrase, not a cause.

**Silence from a diagnostic you just added is evidence, not a null result.** A fix had added error reporting on a timeout path. When the failure recurred and that reporting stayed silent, the silence proved the failure mode had changed: the code was completing, not erroring, on a path the new instrument didn't cover.

**Relaying a subagent's hypothesis in your own voice is authoring a claim, not reporting one.** Say "agent X found Y, on evidence Z", never bare "Y". Five subagent hypotheses were repeated by their orchestrator as findings, and all five were later refuted; the paraphrase, not the guess, is what reached the user's notes as fact.

### Step 4: RECONCILE — Fold findings back

The reviewer's output is data, not verdict. **You are still the orchestrator.** Re-read the artifact text against each finding before classifying — rubber-stamping the reviewer is the same failure mode as ignoring it.

For each finding, classify in this **precedence order** (first matching class wins):

1. **Contract misread** — reviewer flagged something specifically because the CONTRACT you provided was unclear or incomplete. Fix the contract first, re-classify on the next cycle.
2. **Valid + actionable** — real issue requiring a change to the artifact. Change it, re-loop.
3. **Valid trade-off** — issue is real but cost of fixing exceeds cost of accepting. Document the trade-off explicitly so the user sees it.
4. **Noise** — reviewer flagged something that's actually correct under context the reviewer didn't have. Note it, move on, and ask: would adding that context to the contract have prevented the false flag?

A fresh reviewer can be wrong because it lacks context. Don't defer just because it's "fresh."

### Step 5: STOP — Bounded loop, not recursion

Stop when:

- Next iteration returns only trivial or already-considered findings, **or**
- 3 cycles completed (escalate to user, don't grind a fourth alone), **or**
- User explicitly says "ship it"

If after 3 cycles the reviewer still surfaces substantive issues, the artifact may not be ready. Surface this to the user — three unresolved cycles is information about the artifact, not a reason to keep looping.

If 3 cycles is "obviously insufficient" because the artifact is large: the artifact is too big — return to Step 2 and decompose. Do not lift the bound.

## Common Rationalizations

| Rationalization | Reality |
| --- | --- |
| "I'm confident, skip the doubt step" | Confidence correlates poorly with correctness on novel problems. Moments of certainty are exactly when blind spots hide. |
| "Spawning a reviewer is expensive" | Debugging a wrong commit in production is more expensive. The check is bounded; the bug isn't. |
| "The reviewer will just nitpick" | Only if unscoped. Constrain the prompt to "issues that would make this fail under the contract." |
| "I'll do doubt at the end with `/review`" | `/review` is a final gate. Doubt-driven catches wrong directions early when course-correction is cheap. By PR time it's too late. |
| "If I doubt every step I'll never ship" | The skill applies to non-trivial decisions, not every keystroke. Re-read "When NOT to Use." |
| "Two opinions are always better than one" | Not when the second has less context and produces noise. Reconcile, don't defer. |
| "The reviewer disagreed so I was wrong" | The reviewer lacks your context — disagreement is information, not verdict. Re-read the artifact, classify, then decide. |
| "Cross-model is always better" | Cross-model catches blind spots a single model shares with itself, but it adds cost and tool fragility. Offer it every interactive doubt cycle — the user decides whether the artifact warrants it. The agent's job is to surface the choice, not to gate it. |
| "User said yes once, so I can keep invoking the CLI" | Each invocation is its own authorization. The artifact, the prompt, and the flags change between calls — re-confirm the exact command with the user before every run. |
| "I warned the reviewer that this claim is false, so it won't repeat it" | It will. Two agents told a claim was false wrote it back into their own commits. Withhold the claim and make the reviewer derive the symptom from the failure path. |
| "The symptom is obvious from the fix" | The fix tells you what changed, not what breaks without it. Severity lives in the failure path: read what the caller does on error. |
| "The network/environment is obviously the problem" | A causal story that only renames the symptom isn't a hypothesis. Design the experiment that would refute it and run that first - cutting the network took one run to refute a belief already written into the project's notes. |

## Red Flags

- Spawning a fresh-context reviewer for a one-line rename or formatting change
- Treating reviewer output as authoritative without re-reading the artifact text
- Looping >3 cycles without escalating to the user
- Prompting the reviewer with "is this good?" instead of "find issues"
- Skipping doubt under time pressure on a high-stakes decision
- Re-spawning fresh-context on an unchanged artifact (you'll get the same findings; you're stalling)
- **Doubt theater (checkable signal)**: across 2 or more cycles where the reviewer surfaced substantive findings, zero findings were classified as actionable. You are validating, not doubting. Stop and escalate.
- Doubting only after committing — that's `/review`, not doubt-driven development
- Hardcoding an external CLI invocation without confirming with the user that the tool exists, is configured, and accepts that exact syntax
- **Silently skipping cross-model in an interactive doubt cycle.** Even when not recommending it, the offer must be visible. Skipping is fine; silent skipping is not.
- Falling back silently when an external CLI errors or is missing — surface the failure and let the user redirect
- Stripping the contract from the reviewer's input
- Passing the CLAIM to the reviewer (biases toward agreement)
- Naming a suspected-false claim to the reviewer "so it knows to avoid it" (it plants the claim instead)
- Asserting a symptom or severity with no `file:line` behind it, or reading severity off the fix instead of the failure path
- Designing an experiment that would confirm a causal hypothesis instead of one that would refute it
- Repeating a subagent's causal hypothesis as your own finding, without naming the claimant or its evidence

## Interaction with Other Skills

- **`code-quality` / `/review`**: complementary. `/review` is post-hoc PR verdict; doubt-driven is in-flight per-decision. Use both.
- **`source-driven-development`**: SDD verifies *facts about frameworks* against official docs. Doubt-driven verifies *your reasoning about the artifact*. SDD checks the API exists; doubt-driven checks you used it correctly under the contract.
- **`test-driven-development`**: TDD's RED step is doubt made concrete — a failing test is a disproof attempt. When TDD applies, that failing test *is* the doubt step for behavioral claims.
- **`debugging-and-error-recovery`**: when the reviewer surfaces a real failure mode, drop into the debugging skill to localize and fix.
- **Repo orchestration rules** (`references/orchestration-patterns.md`): this skill orchestrates from the main session. A persona calling another persona is anti-pattern B — see Loading Constraints above.

## Verification

After applying doubt-driven development:

- [ ] Every non-trivial decision (per the definition above) was named explicitly as a CLAIM before standing
- [ ] At least one fresh-context review per non-trivial artifact (a failing test produced by TDD's RED step satisfies this for behavioral claims, per Interaction with Other Skills)
- [ ] The reviewer received ARTIFACT + CONTRACT — NOT the CLAIM, NOT your reasoning, and NOT any claim you suspect is false
- [ ] For symptom or severity claims: the reviewer derived the symptom itself from the failure path, and every surviving claim cites `file:line`
- [ ] The reviewer's prompt was adversarial ("find issues"), not validating ("is it good")
- [ ] Findings were classified against the artifact text (not rubber-stamped) using the precedence: contract misread / actionable / trade-off / noise
- [ ] A stop condition was met (trivial findings, 3 cycles, or user override)
- [ ] In interactive mode, cross-model was **explicitly offered** to the user (regardless of artifact stakes) and the response was acknowledged in the output
- [ ] In non-interactive mode, cross-model was skipped and the skip was announced
- [ ] Any external CLI invocation was preceded by a PATH check, a working-binary test, syntax confirmation with the user, and explicit authorization to run
- [ ] For causal ("X causes Y") claims: the disproving experiment was designed and run before the confirming one
- [ ] Any subagent hypothesis relayed onward carries its claimant and evidence, never repeated as a bare finding
