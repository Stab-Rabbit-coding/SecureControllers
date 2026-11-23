# Grounding checklist -- how briefs here have gone wrong

Each item is a real failure from this project's briefs (Serenity-UAV Theme N, Nov 2026), with the
check that would have caught it. Run through the list before trusting a number.

## Frames and handedness

- **Mirrored keep-outs.** An optimiser ran on the left-shell (port) frame with keep-outs measured on
  the starboard pod; inboard and outboard were swapped (az -> 180 - az). A board landed in the
  trunnion gear cavity. *Check:* confirm every input is in the same frame -- ray-test the render
  against each candidate shell and see which matches (median radial difference ~0).
- **Which side the render is.** A default render was the left shell although it was published under
  the other side's name. *Check:* never infer the frame from a file name; measure it.

## Ray-cast artifacts

- **Far-side hits.** Rays cast through an axis kept the farthest hit, so each azimuth read the larger
  of its own and the opposite radius. *Check:* keep near-side hits only (positive projection on the
  ray's outward direction) and test on an asymmetric case.
- **Grazing rays.** A radial ray skimming a pocket rim or window edge "measured" a 0.3 mm wall that
  was a chord. *Check:* compare the ray against the surface normal at the hit; a ray > 60 deg off the
  normal is not measuring a wall. Inscribed-sphere and normal-direction measures also fail at sharp
  edges -- for real wall thickness use a proper thickness analysis.
- **Attribution.** A defect was blamed on the cavity when another cut (wire channels) had opened the
  skin. *Check:* render with and without the suspected feature and compare.

- **Outermost hit instead of first crossing.** A ray's farthest hit counted a fairing beyond an air gap
  as "skin". *Check:* take the first outward crossing, and test containment of the point first -- a
  point in air has no skin, whatever lies beyond it.
- **Exclusion zone hid the defect.** A tool skipped "r < 40 mm, the bay's designed mouth (Z 65-77)";
  the SCAD bay ended at Z 68.1 and the skipped band held a 7.4 mm open run through a socket in the
  canonical shell. *Check:* every mask comes from the source parameter, is shaded on the figure, and is
  inspected on its own. (Serenity-UAV Brief I, 2026-11-23.)

## Models that look right

- **Re-tilted panels.** A fit model narrowed a rigid PCB ring by ring by re-tilting each ring; the real
  board keeps its tilt. Results were optimistic by up to 15 %. *Check:* ask whether the model's degrees
  of freedom exist in the part.
- **Construction-checks-itself.** A wall "measured" by the same expression that built it always passes.
  *Check:* measure on the built solid by an independent method; add a negative control that must fail.
- **Tolerance ties.** A part built to exactly envelope + clearance read as failing by float round-off.
  *Check:* compare with a stated tolerance.

- **Patched numbers instead of patched geometry.** An option's fill was modelled as a per-sample
  override keyed on Z only; it credited a wire outside the fill in Y and shrank its pad to two strips.
  *Check:* model each option as geometry (boolean the candidate solid) and measure that solid with the
  same tool. (Brief I, review cycle 2.)
- **Inherited defect.** An open socket traced to none of the project's cuts; it was in the imported
  canonical shell. *Check:* render the imported source alone in the same box.

## Rules and values

- **Wrong wall rule.** A 2.0 mm "fallback for unstated load category" was used where the material
  study gave 1.5 mm for the actual category -- and it recurred in a later brief as a hand-typed "pad
  target 2.0". *Check:* import the target from the study's code/constant; find the study or allowable that covers the part
  and its load category; use the fallback only when none does, and say so.
- **Remembered constants.** If a property needs a source and the source cannot be reached, leave it
  open and say what would close it -- do not fill it from memory.
- **Callout inflation.** "Not ready to print" was labelled WARNING. *Check:* WARNING only with an
  injury path to people; CAUTION for equipment/aircraft loss; Note otherwise.

## Process

- **Something already decided changes the answer.** Re-evaluate at the decided state (e.g. the new
  pivot), not only the current one.
- **Stale published parts.** Published meshes may lag the source; say which one you measured.
- **Look at the picture.** Several errors above were visible in a render before they were visible in a
  number.
