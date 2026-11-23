# Which skill for which check

Invoke the skill (Skill tool) for the check it owns; it brings the method, the validity limits and the
citation rules. Several checks often need two skills. If a listed skill is not installed, do the work
inline to the same standard and say which method you used.

| Check / question | Skill(s) | What to get from it |
| --- | --- | --- |
| Free-body diagram, reactions, moments, mechanism forces, virtual work | `statics-and-dynamics` | FBD with every load as a vector and magnitude; determinacy; an independent check equation. |
| Flight loads, drag, lift, gust, V-n, weight and balance, CG, pivot, T/W, hover clearance | `aeronautical-engineering` | Governing load case, drag increments, W&B roll-up and margins; the mandatory notice. |
| Stress, fatigue, fasteners, inserts, bearings, shafts, gears, springs | `mechanical-engineering` | Allowables with sources, margins, fatigue basis; "requires verification" where no allowable exists. |
| Walls, print orientation, SLS/FDM/resin DFM, tolerances, supports | `3d-print-design` | Minimum wall per process and load category (use the repo's material study where it applies), orientation that governs strength. |
| Geometry, renders, sections, clash volumes, OML departure | `openscad` (+ the repo's mesh tools) | Real renders from several sides; X-ray / transparent views for clashes; look at every image. |
| Flow, drag deltas, blockage, cooling air paths | `openfoam-cfd` (+ the repo's CFD cases) | A case with stated mesh, y+, convergence and domain; drag with its spread; compare like with like. |
| Heat, cooling, temperature rise | `thermodynamics` (`mechanical-engineering` for heat exchangers) | Heat path, resistances, temperature against datasheet limits. |
| Rails, wire/connector/fuse ratings, fault current, protection coordination | `electrical-engineering` | Current against every rating in the path, margins, coordination curves. |
| Board-level: EMC, signal integrity, regulators, isolation | `electronics-engineering`, `emc`, `pcb-engineer` | Victim/aggressor list, filtering, isolation distances. |
| Firmware/real-time, buses, timing | `computer-engineering`, `control-systems-engineering` | Timing budgets, loop stability margins. |
| Parts, datasheets, sourcing | `datasheets`, `bom` (+ distributor skills) | Verified datasheet values with REF-IDs; BOM rows. |
| Figures and charts | `dataviz` | Clear, consistent plots; one message per panel. |
| Adversarial review of the recommendation (step 7) | `doubt-driven-development` (+ a spawned fresh-context reviewer, `references/adversarial-review.md`) | Findings that try to disprove the recommendation; each fixed, rebutted or left open. |
| Editorial review of the brief before it goes out | `ce-doc-review` | Role-based critique of the document (clarity, structure), after the adversarial pass. |

## Picture per check (what usually works)

- **Statics and dynamics:** FBD on a simple outline of the part, arrows to scale or labelled, reactions
  at supports, the governing case in the title.
- **Function:** the motion or path itself (stroke sweep, flow arrows, wire route) with the limit shown.
- **Structural integrity:** a section through the thinnest wall with its dimension, or a bar chart of
  walls against the rule line.
- **Mechanism:** X-ray render with clashes in a contrasting colour and nearest gaps labelled; for
  motion, overlay the extreme positions.
- **Weight and balance:** CG stations on a side outline with the pivot and the hover arm; bars for
  mass deltas and clearances.
- **Canonical shape:** the canonical outline against each option's outline (side and plan), departures
  coloured and dimensioned.
