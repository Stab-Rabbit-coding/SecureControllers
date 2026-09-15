# Hardware / CAD / Mechanical Standards

Layer this over the language template when the project has physical deliverables. If the
repository states its own values for any of these, the repository wins — this file is a default,
not an override.

## Budgets are deliverables

A mechanical task is not done until its physical cost is quoted. Every change that adds, removes,
or moves geometry states:

- **Mass** — the delta, and the new total.
- **Balance** — CG shift along each affected axis.
- **Power** — draw added or removed, continuous and peak.
- **Volume and clearance** — space consumed, and the remaining margin to the nearest neighbour.

Never write "TBD" for one of these. A deferred number is not deferred — it is skipped, and it is
discovered during fabrication, where the correction costs a re-print or a re-order. If a figure
genuinely cannot be computed yet, say what is blocking it and raise it as an open item with an
owner.

## Units

Follow the project's convention exactly. Where it is imperial-primary with metric in
parentheses, write `10 in (254 mm)`, `2.5 lbm (1.13 kg)`, `4.8 lbf (21.4 N)`, `25 kt (12.8 m/s)`.

Keep mass and force distinct: **lbm** for mass, **lbf** for force, never a bare "lb" where the
distinction matters. Component weights and payload capacity are masses; thrust, lift, and
aerodynamic loads are forces. Conflating them produces errors of a factor of g that survive
review because both numbers look plausible.

State the units in every table header and every extracted impact note. A unitless number in a
shared budget is a defect.

## Structural design

- Size fasteners, walls, and structural members for **real loads** — quote the load and the
  margin, not just the chosen size.
- Load-bearing joints need a positive mechanical stop and adequate contact area. Friction fit
  alone is not acceptable for a flight- or safety-critical joint.
- Design field-serviceable parts for disassembly with common hand tools.
- Integrate brackets, bosses, and ribs into the parent part where feasible rather than adding
  separate hardware.

## Additive manufacturing

State material, layer height, perimeter count, and infill for every printed part, and
distinguish load-bearing from non-structural settings. Exterior shells that must be sealed state
wall thickness and the fill strategy.

## Mesh validation is mandatory

After **every** model edit, validate: watertight, no self-intersections, correct normals,
manifold topology. Report findings and resolve them before committing.

This is not optional diligence. A non-manifold mesh slices into a part that looks right on screen
and fails on the plate, and the failure is usually discovered hours into a print.

## Coordinate discipline

Where a project defines a canonical coordinate frame, every artifact uses it. Note the axis
convention and origin in the file header. Never apply a transform twice — baking an
already-baked mesh produces a part that is subtly, consistently misplaced, and the error is hard
to see and easy to propagate.

Where a canonical outer profile exists, interior changes blend into it and do not alter the
exterior unless structurally required.

## Traceability

Cite the source of any geometry technique, profile, or design decision drawn from an external
reference — in the file's comment block and in the commit message. For file formats without
comment syntax, keep the notes in an accompanying Markdown file of the same name.

## Task checklist

Before marking a mechanical task complete:

- [ ] Mass delta and new total quoted, with units
- [ ] CG shift quoted for each affected axis
- [ ] Power delta quoted, continuous and peak
- [ ] Clearance margin to nearest neighbour stated
- [ ] Loads and margins stated for structural members
- [ ] Material, layer height, perimeters, infill specified
- [ ] Mesh validated — watertight, manifold, normals correct
- [ ] Coordinate frame confirmed, no double transform
- [ ] External references cited in file and commit
- [ ] Budgets recorded in the task's impact output
