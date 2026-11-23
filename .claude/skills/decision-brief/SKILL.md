---
name: decision-brief
description: Write an Owner Decision Brief -- options for a design, part, spec or OD-x decision presented against the six required checks, each with a picture (vectors wherever a load or motion is involved), measured or computed numbers with sources, options side by side, a recommendation, a fresh-context adversarial review of that recommendation, and what is still unverified. Use this skill whenever the user asks for a "decision brief", "brief", "options for the owner", "OD-x", "trade study", "should we do A or B", or wants a finding turned into choices to decide on, and whenever an engineering finding needs an owner decision before work can continue -- even if they don't say "brief". It routes each check to the right engineering skill (statics-and-dynamics, aeronautical-engineering, control-systems/mechanical/electrical/electronics/thermodynamics, 3d-print-design, openscad, openfoam-cfd, dataviz).
---

# Decision Brief

An Owner Decision Brief puts a real choice in front of the owner so they can decide it in one reading.
Every option is shown against the same six checks, each with a picture, and every number in it is
either measured on the real geometry / computed from stated inputs, or cited. The brief recommends;
it never decides. The owner's choice is recorded afterwards.

The brief is only as good as the facts under it. Most of the work is establishing those facts
correctly -- the writing is the last 20 %.

> [!WARNING]
> **ENGINEERING REVIEW REQUIRED -- this output is not a substitute for a qualified engineer.** Every
> result, calculation, and recommendation in a brief must be independently reviewed and accepted by
> a properly qualified individual before it is applied to any system carrying risk to life or
> safety. Carry this notice (and the engineering skills' CAUTION) at the top of every brief.

## The template

If the repo has its own template, it governs: in Serenity-UAV it is `docs/DOC_TEMPLATES.md`
"Owner Decision Briefs" (airframe check set) and its "Avionics and power-electrical check set".
Read it first. `references/brief-template.md` holds a copy of both check sets and the brief skeleton
for repos that do not have one -- if the two ever differ, the repo copy wins and you say so.

The six airframe checks: **Statics and dynamics, Function, Structural integrity, Mechanism and
component interactions, Weight and balance, Canonical shape.** The avionics / power set swaps in
**Electrical engineering** and **Wire harness, fastener and mounting fit**, and adds **Thermal load**.
No check is skipped silently: if one does not apply, say so in one line and why.

## Workflow

### 1. Frame the decision

- Find the trigger (a finding, a failed gate, an owner question) and the owning WBS item. Read the
  item and everything it links. Write one sentence: *what must be decided, and what happens if
  nothing is*.
- List the decisions already in force that bound the options (earlier OD-x, owner directions, repo
  rules such as `AGENTS.md` wall and unit rules). An option that silently reverses one is not an
  option; one that deliberately reopens it must say so in its name.
- Check whether something already decided or in progress changes the problem. (Example from this
  project: a skin breach that a pivot move, already decided, partly covered -- the "do nothing extra"
  option was real and nearly sufficient.)

### 2. Establish the facts -- measure, then doubt the measurement

Read `references/grounding-checklist.md` before measuring anything. It lists the failure modes that
have produced wrong briefs here (mirrored frames, far-side ray hits, grazing rays read as thin walls,
the wrong wall rule, a fallback value used where a study applies).

- Measure on the real parts (current renders, published meshes, the repo's own check tools and
  gates) rather than on idealisations. Prefer the repo's tools; extend them rather than writing
  one-off scripts when the measurement will be needed again.
- Cross-check every number the recommendation rests on by a second, independent method (volumetric
  vs ray, analytic vs mesh, two frames). When the two disagree, find out why before writing.
- Label each number: measured (tool + inputs), computed (equation + inputs), cited (REF-ID +
  section), or ESTIMATE / ASSUMED / REQUIRES VERIFICATION. Never present a remembered value as a
  result; if a source is needed and cannot be reached, say so and leave the value open.
- **Audit every exclusion and mask in the measuring tool before trusting its minimum.** A region the
  tool skips ("designed opening", "inside the bay", "below r 40") must take its bounds from the source
  geometry (the SCAD parameter, not memory), be shaded on the figure, and be inspected on its own.
  The worst defect is often exactly where the tool was told not to look.
- **Pin the target to its source in code.** A sizing target (wall, margin, clearance) comes from the
  governing study or rule imported as a constant, not typed in; a fallback is used only where no study
  covers the case, and the brief says so.
- **Inherited geometry can carry defects.** When a defect will not trace to any of your features,
  render the imported/canonical source alone in the same box before concluding.

### 3. Build the options

Three to four real options, usually including the cheapest path (often "accept / do nothing more",
or an already-decided path) and the one that reopens a decision, if that is honestly on the table.
Each option gets concrete parameters (dimensions, parts, stations) so it can be checked, not a slogan.

### 4. Run the six checks per option

Use `references/skill-routing.md` to pick the skill for each check and invoke it (Skill tool) -- the
engineering skills carry the method, the validity limits and the citation discipline. Typical:
statics-and-dynamics for the free-body diagram, aeronautical-engineering for loads / drag / W&B,
3d-print-design for walls and print orientation, openscad for geometry and renders, openfoam-cfd for
flow questions, electrical/electronics/thermodynamics for the avionics set, control-systems for control logic or dynamic control limits, dataviz for the figures.

For each check give: the governing case, the number(s) with units and source, the margin against a
stated limit, and a one-line verdict per option. If a check cannot be closed in the time available,
say what would close it.

### 5. Make the pictures

Every check has a picture; every load or motion has vectors with magnitudes. Use real geometry where
the question is geometric (renders, sections, X-ray / transparent views highlighting clashes and
mould-line departures), plots where it is quantitative, and a free-body diagram where it is a load.

- `scripts/brief_fig.py` gives a 2 x 3 six-check sheet, labelled force / moment arrows in
  imperial (metric), margin bars against a limit line, and the review stamp. Import it or copy the
  pattern into a committed figure tool in the repo (`tools/brief_<x>_fig.py`), so the figure is
  reproducible from its inputs.
- Look at every figure before using it (Read the PNG). Check orientation, labels, units, that the
  highlighted thing is where the text says it is, and that nothing is clipped.
- Copyrighted references (e.g. QMx blueprints) are internal only: compare against them, never embed
  them in a committed figure.

### 6. Write the brief

Use the skeleton in `references/brief-template.md`. In particular:

- Lead with the question, the trigger and the bottom line (recommendation in one sentence).
- One table row per check, one column per option; each cell a number and a verdict, the picture
  beside or below. Explain the mechanism in plain words where a reader would otherwise have to
  infer it -- a brief that the owner cannot follow is not finished.
- Options side by side, the recommendation and its reason, then **what is still unverified** and
  **what each option commits us to** (the work items it creates). The adversarial review (step 7) adds
  its own section after the recommendation.
- Units imperial first, metric in parentheses (knots for airspeed). Requirement words per the repo
  (shall / should / may / will). Callouts strictly by hazard: WARNING only for injury or death to
  people, CAUTION for equipment or aircraft loss, Note for everything else -- state the mechanism.
- No fabricated or unverified citation. Copyrighted material is referenced, not reproduced.

### 7. Adversarial review -- try to break it before the owner sees it

Read `references/adversarial-review.md` and run it. In short: state the recommendation as a claim that
could be false; give a **fresh-context** reviewer (a spawned subagent, not you re-reading your own
work) the brief, the rules, the raw inputs and the exact command that regenerates the numbers, with
orders to audit the measuring tool's exclusions and masks and to disprove rather than approve -- re-derive
the load-bearing numbers, test their sensitivity, steelman the losing options, look for a missing or
already-decided option, run a pre-mortem, and hunt checks that pass by construction. Then answer every
finding in the brief as **fixed**, **rebutted** (with evidence) or **open** (moved to "still
unverified"), and add the "Adversarial review" section with the strongest case against the
recommendation. If a finding that would flip the choice cannot be fixed or rebutted, the recommendation
changes or the brief says plainly that the choice hinges on it. This follows the library's
`doubt-driven-development` cycle; up to three rounds, and a cycle that changes the recommendation is
always followed by another cycle on the re-issued brief.

**Order of operations.** The review runs *before* the brief is presented as finished, before the WBS
says "owner decision pending", and before any chat message asks for the decision. Commit the draft if
the session needs it pushed, but mark its bottom line DRAFT -- UNDER REVIEW until the review closes.

**If you are a subagent** (you cannot spawn the reviewer): stop at the end of step 6, return the
draft, the claim, and the review inputs (paths, regenerate command) to the main session, and say that
step 7 is pending there. Do not substitute a self-review unless the user says so; if they do, label it
**degraded** in the brief.

Why: the author of a brief has been inside the problem for hours and is the person least able to see
its blind spots. Most of the errors in `references/grounding-checklist.md` were found only when
someone tried to break a number instead of confirming it.

### 8. Record and hand over

- Put the brief where the repo keeps them (Serenity-UAV: the theme's `docs/THEME_*_DECISION_BRIEFS.md`
  or the subject document), figures in `docs/figures/`, and a pointer plus "owner decision pending"
  in the owning WBS item. Add a changelog line.
- Run the repo's lint / doc checks on what you changed, commit, and push if the session works that way.
- In chat, give the owner the question, the options in one line each, the recommendation, the
  strongest case against it, and what is unverified -- and ask for the decision. Record the answer,
  with its date, when it comes.

## Self-check before handing over

- Every check present for every option (or a one-line "does not apply because ...").
- Every figure viewed; vectors carry magnitudes and units; no figure contradicts the text.
- Every number traceable (tool, equation, REF-ID, or labelled estimate); the key ones cross-checked.
- The facts were measured in the right frame, on current geometry, with the right rule.
- Callouts graded by hazard; units imperial-first; the review notice at the top.
- The recommendation follows from the checks, and the unverified list is honest.
- Every exclusion/mask in the measuring tool is sourced, shaded on its figure, and inspected.
- The adversarial review ran with fresh context, before the brief was handed over; every finding is fixed, rebutted with evidence, or
  open in the unverified list; the strongest case against the recommendation is in the brief.
