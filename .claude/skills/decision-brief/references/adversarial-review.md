# Adversarial review of a brief

A brief is written by someone who has spent hours inside the problem, and long work quietly turns
assumptions into "facts". Before the brief goes to the owner, a reviewer with **fresh context** and
a brief to **break it, not approve it** attacks the recommendation and the facts under it. This is the
`doubt-driven-development` cycle (CLAIM -> EXTRACT -> DOUBT -> RECONCILE -> STOP) applied to an
engineering decision. The owner then sees both the case and the strongest case against it.

## 1. CLAIM

Write the recommendation as a claim that could be false, and why it matters:

```text
CLAIM: Option X2 closes the breach with >= 2.0 mm of skin over every channel, at no OML change,
       and costs less mass than X1.
WHY IT MATTERS: if wrong, the pod prints with wiring open to the airflow (aircraft-loss CAUTION).
```

## 2. EXTRACT -- what the reviewer gets

Give the reviewer the artifact and the contract, not the journey:

- the brief text and its figures (paths), and the claim above;
- the rules it must meet (template, unit and callout rules, wall rules, decisions in force);
- the raw inputs the key numbers came from (meshes, tool commands, JSON outputs), so numbers can be
  re-derived rather than trusted.

Leave out your reasoning and your doubts -- the point is an independent view.

## 3. DOUBT -- spawn the reviewer

Spawn a fresh subagent (Agent tool, general-purpose) with the prompt below. If you are already inside
a subagent and cannot spawn, say so to the user and let the main session run it; only as a last resort
do a self-review with a hard separator, and label it **degraded** in the brief.

```text
You are an adversarial reviewer for an engineering Owner Decision Brief. Your job is to find what is
wrong, missing or overstated -- not to approve it. Assume the recommendation is wrong until the
evidence forces you otherwise. Re-derive numbers from the raw inputs where you can; do not trust the
brief's arithmetic or its figures.

Attack along these lines, and for each finding give: what is wrong, the evidence (file, number,
re-derivation), how much it matters (would it change the recommendation? yes / maybe / no), and what
would settle it.

1. Load-bearing numbers: which 2-3 numbers does the recommendation rest on? Re-derive them, or show
   why they cannot be trusted (wrong frame, wrong part revision, artifact of the method, unit slip,
   fallback used where a study or allowable applies, remembered rather than sourced).
2. Sensitivity: how far would each have to move to flip the recommendation? Is the margin larger than
   the method's uncertainty?
3. Steelman the losers: make the strongest honest case for the best non-recommended option. Is the
   comparison fair (same load case, same geometry state, same assumptions)?
4. Missing option: is there a cheaper, simpler or already-decided path the brief did not consider?
   Does something decided elsewhere change the problem?
5. Checks that pass by construction, or were skipped, or were waved through with "does not apply".
6. Pre-mortem: it is a year later and the chosen option failed in service. Write the three most likely
   stories. Which are covered by the brief's unverified list, and which are not?
7. Second-order effects: neighbours, both handed sides, the full range of motion, mass and CG, the
   ledger, the build sequence, and anything published to other teams (issues, envelopes).
8. Presentation: callouts graded by hazard (WARNING only with an injury path), units imperial-first,
   citations that exist, figures that match the text, claims stronger than the evidence.

Return a numbered list of findings, most decision-relevant first, then a one-line verdict:
"recommendation stands", "stands with changes", or "does not stand".
```

## 4. RECONCILE -- answer every finding

Classify each finding against the brief, in the brief:

| Finding | Class | Response |
| --- | --- | --- |
| ... | **fixed** (brief changed) / **rebutted** (evidence that it does not hold) / **open** (moved to "still unverified", with what would settle it) | ... |

Rebuttals need evidence, not confidence. A finding that would flip the recommendation and cannot be
fixed or rebutted changes the recommendation, or makes the brief say plainly that the choice hinges on
it.

## 5. STOP

Stop when a cycle returns only presentation-level findings, after three cycles, or when the user says
so. Record the cycle count and the final verdict in the brief.

## In the brief

Add a section after the recommendation:

```markdown
### Adversarial review

Fresh-context reviewer, <n> cycle(s), verdict: <recommendation stands / stands with changes / ...>.
**Strongest case against <recommended option>:** <one paragraph, the reviewer's best argument>.

| # | Challenge | Class | Response |
| --- | --- | --- | --- |
| 1 | ... | fixed / rebutted / open | ... |
```

The owner should be able to read the case for and the case against without opening anything else.
