# Owner Decision Brief -- template

Copy of the check sets in Serenity-UAV `docs/DOC_TEMPLATES.md` ("Owner Decision Briefs", owner
direction 2026-11-08; "Avionics and power-electrical check set", owner direction 2026-11-14). If the
repo you are in has its own template, that one governs.

## Check sets

### Airframe / mechanical (default)

| Check | What it must show |
|---|---|
| **Statics and dynamics** | Free-body diagram of the affected part(s): applied loads, reactions, moments as vectors with magnitudes; the governing load case (hover, gust, landing, tilt slew, vibration); stresses or allowables where one exists, and "requires verification" where it does not. |
| **Function** | What the part has to do and whether each option still does it (stroke, clearance, electrical or flow path, service access, install/remove). |
| **Structural integrity** | Minimum walls (repo rule, or the material study where it covers the part), load path continuity, stress concentrations, fastener/insert margins, print orientation where it governs strength. |
| **Mechanism and component interactions** | Every neighbour the change touches, at rest and through the full range of motion: interference volumes, nearest gaps, wire/harness routes. Run both sides when the parts are handed. |
| **Weight and balance** | Mass change per part and per aircraft (lbm (g)), CG shift, pivot residual, hover arm and ground clearance, T/W; which ledger picks the change up and when. |
| **Canonical shape** | Effect on the outer mould line against the canonical references in their authority order; "internal only" is an answer when true. |

### Avionics, power electrical, motors and sensors

| Check | What it must show |
|---|---|
| **Electrical engineering** (replaces Statics and dynamics) | Each rail's typical and peak current against source, regulator, connector and wire rating, with margin; switching/clock frequencies and transmit bands against the nearest victim and the isolation/filtering between them. |
| **Function** | As above. |
| **Structural integrity** | As above, for the board, its mounts and connectors. |
| **Mechanism and component interactions** | As above, plus every bus, harness and neighbouring board touched. |
| **Weight and balance** | As above; fasteners, connectors and harness tracked as their own ledger lines per PCB. |
| **Wire harness, fastener and mounting fit** (replaces Canonical shape) | Route and bend radius, connector mating clearance, fastener type/length/engagement, mount fit, service access -- on the real meshes. |
| **Thermal load** (added) | Heat at typical and peak load, the heat path to ambient, design ambient, each part's temperature against its datasheet limit. |

An outer-mould-line change caused by an avionics item still gets the Canonical shape check.

## Brief skeleton

```markdown
## Brief <letter / OD-n> -- <the question in plain words>

> [!WARNING] ENGINEERING REVIEW REQUIRED ... (verbatim notice)
> [!CAUTION] This informs engineering judgment ... (verbatim)

**Question.** <one sentence: what must be decided>.
**Trigger.** <finding / gate / owner question, with WBS ID and date>.
**If nothing is decided.** <consequence>.
**Bound by.** <decisions in force that the options respect, with IDs>.
**Bottom line.** Recommend <option> because <one reason>.

### What we measured
<facts the options rest on: number, method, source, cross-check; one picture>

### Options
- **X1 <name>** -- <what changes, with parameters>.
- **X2 <name>** -- ...
- **X3 <name>** -- ...

### Six checks
![<sheet title>](figures/<brief>_six_checks.png)

| Check | X1 | X2 | X3 |
|---|---|---|---|
| Statics and dynamics | <number, margin, verdict> | ... | ... |
| Function | ... | ... | ... |
| Structural integrity | ... | ... | ... |
| Mechanism and component interactions | ... | ... | ... |
| Weight and balance | ... | ... | ... |
| Canonical shape | ... | ... | ... |

<plain-words explanation of any mechanism a reader would otherwise have to infer>

### Recommendation
**<option>.** <reason, tied to the checks>.

### Adversarial review
Fresh-context reviewer, <n> cycle(s), verdict: <recommendation stands / stands with changes / does not
stand>. **Strongest case against <option>:** <the reviewer's best argument, one paragraph>.

| # | Challenge | Class | Response |
|---|---|---|---|
| 1 | <what is wrong, with evidence> | fixed / rebutted / open | <change made, evidence, or what would settle it> |

### Still unverified
- <item> -- what would verify it (test, analysis, datasheet), and who.

### If chosen
1. <work item it creates, owning WBS ID>.

### Changelog
- <date> -- <what changed>.
```
