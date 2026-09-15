# FDM Design Rules Reference

Constraints and guidelines for designing parts to be printed on FDM (Fused
Deposition Modelling) printers. All values assume a standard 0.4mm nozzle
unless noted otherwise.

## Table of Contents

1. [Wall Thickness](#wall-thickness)
2. [Overhangs and Bridging](#overhangs-and-bridging)
3. [Tolerances and Clearances](#tolerances-and-clearances)
4. [Holes and Cylinders](#holes-and-cylinders)
5. [Supports](#supports)
6. [Infill and Strength](#infill-and-strength)
7. [Print Orientation Strategy](#print-orientation-strategy)
8. [Text and Fine Detail](#text-and-fine-detail)
9. [Thin Features](#thin-features)
10. [Warping and Bed Adhesion](#warping-and-bed-adhesion)
11. [Multi-Part Design](#multi-part-design)
12. [Dimensional Accuracy Table](#dimensional-accuracy-table)

---

## Wall Thickness

### Minimum wall thickness by purpose

| Purpose | Minimum | Recommended | Notes |
|---|---|---|---|
| Structural wall | 1.2mm (3 perimeters) | 1.6-2.0mm (4-5 perimeters) | Load-bearing walls, enclosure sides |
| Non-structural wall | 0.8mm (2 perimeters) | 1.2mm | Internal dividers, cosmetic panels |
| Snap-fit arm | 1.0mm | 1.2-1.5mm | Needs flexibility without breaking |
| Screw boss wall | 1.6mm | 2.0mm | Around heat-set insert or self-tap hole |
| Floor/ceiling (horizontal) | 0.8mm | 1.2mm | Top/bottom of enclosures |
| Tall thin wall (>30mm) | 1.2mm | 1.6mm | Thin tall walls wobble during print |

### Why these values

A 0.4mm nozzle produces extrusion lines ~0.45mm wide. Wall thickness should
be a multiple of line width for clean results:

- 2 perimeters = ~0.8-0.9mm
- 3 perimeters = ~1.2-1.35mm
- 4 perimeters = ~1.6-1.8mm

Non-integer multiples leave thin gaps between perimeters that the slicer fills
poorly, creating weak spots.

## Overhangs and Bridging

### Overhang rules

An "overhang" is any surface that extends outward from the layer below with no
support underneath.

| Overhang angle (from vertical) | Printability |
|---|---|
| 0-40° | Prints cleanly with no support |
| 40-50° | Acceptable, slight surface degradation |
| 50-60° | Marginal, noticeable sagging |
| 60-90° | Requires support or redesign |
| 90° (horizontal ceiling) | Requires support or bridging |

**45° is the safe maximum.** Design overhangs at ≤45° from vertical wherever
possible to eliminate supports entirely.

### Designing out overhangs

- **Chamfers instead of fillets** on bottom edges (a 45° chamfer prints clean;
  a fillet creates a gradually increasing overhang)
- **Teardrop holes** for horizontal holes — replace the top arc of a circle
  with a 45° pointed roof, eliminating the worst overhang
- **Split the part** so that overhang surfaces become flat-on-bed surfaces in
  one of the halves
- **Change print orientation** — an overhang in one orientation may be a
  vertical wall in another

### Bridging

A "bridge" is a horizontal span between two supported points with nothing
underneath. The printer stretches filament across the gap.

| Bridge length | Reliability |
|---|---|
| <20mm | Usually successful with standard settings |
| 20-40mm | May sag slightly; use bridge-specific settings in slicer |
| 40-60mm | Likely to sag noticeably; consider supports or redesign |
| >60mm | Redesign to avoid this span |

To improve bridging: reduce print speed for bridge layers, increase fan speed
to 100%, and ensure the material is dry (moisture causes bubbling and poor
adhesion).

## Tolerances and Clearances

### General dimensional tolerance

| Printer quality | Typical tolerance |
|---|---|
| Well-calibrated consumer (Prusa, Bambu, Voron) | ±0.15mm |
| Average consumer printer | ±0.2-0.3mm |
| Cheap/poorly calibrated | ±0.3-0.5mm |

These are per-axis tolerances. Cumulative error over large distances is
proportionally larger.

### Clearance for mating parts

| Fit type | Clearance per side | Total gap | Use for |
|---|---|---|---|
| Press fit | -0.05 to 0mm (interference) | Tight | Permanent assembly, pins |
| Snug fit | 0.1mm | 0.2mm total | Lids that stay put without fasteners |
| Sliding fit | 0.15-0.2mm | 0.3-0.4mm total | Lids that slide on/off, drawers |
| Loose/clearance fit | 0.25-0.3mm | 0.5-0.6mm total | Parts that must move freely |

These are starting points. Always recommend a tolerance test: print two
mating test pieces (e.g., a peg and hole at various clearances) to calibrate
for the user's specific printer.

### Clearance for specific applications

| Application | Clearance | Notes |
|---|---|---|
| PCB in slot | 0.2-0.3mm per side | PCB is 1.6mm; slot should be 2.0-2.2mm |
| Screw through-hole (M3) | 3.4-3.5mm hole dia | M3 screw is 3.0mm shaft |
| Heat-set insert hole | See insert datasheet | Typically 0.1-0.2mm smaller than insert OD |
| Snap-fit hook clearance | 0.3-0.5mm | Needs enough play to engage/disengage |
| Cable pass-through | +1.0mm over cable OD | Accounts for connector + tolerance |

## Holes and Cylinders

### Horizontal holes (axis parallel to build plate)

Horizontal holes are the most problematic feature in FDM. The top of the
circle is a bridge/overhang.

**Strategies**:

- **Teardrop shape**: replace the circular hole with a teardrop (circle with a
  pointed top at 45°). Post-process with a drill if a round hole is needed.
- **Print vertically**: if the part allows, orient so the hole axis is vertical.
- **Support inside the hole**: slicer-generated support, then clean out.
  Results in rough interior surface.
- **Sacrifice bridge**: design a thin (0.3-0.6mm) bridge layer across the top
  of the hole that is easily broken out with a screwdriver. Better surface
  finish than support.

### Vertical holes (axis perpendicular to build plate)

Vertical holes print much more accurately because each layer is a circle.

| Hole purpose | Design diameter | Notes |
|---|---|---|
| M2 screw clearance | 2.4mm | M2 shaft is 2.0mm |
| M2.5 screw clearance | 3.0mm | M2.5 shaft is 2.5mm |
| M3 screw clearance | 3.4mm | M3 shaft is 3.0mm |
| M3 tap hole | 2.5mm | For self-tapping into plastic |
| M4 screw clearance | 4.5mm | M4 shaft is 4.0mm |
| Heat-set M3 insert | Per insert datasheet | Typically 4.0-4.2mm |

Holes tend to print slightly undersized (by ~0.1-0.2mm) due to the nozzle's
outer edge intruding into the hole. Either oversize the design or drill out
after printing.

### Screw bosses

A screw boss is a cylindrical protrusion with a hole for a screw. Design:

- Outer diameter: ≥2× screw diameter (e.g., 6mm OD for M3)
- Wall thickness around hole: ≥1.5mm (for heat-set insert) or ≥2mm (self-tap)
- Add a fillet at the base (where the boss meets the wall) for strength
- If the boss is tall (>10mm), add buttress ribs connecting it to the nearest
  wall

## Supports

### When supports are unavoidable

- Overhangs >50-55°
- Floating geometry (nothing below to build on)
- Horizontal holes without teardrop modification
- Complex organic shapes

### Minimising support impact

- **Orient the part** so the most important surfaces face up or are vertical
- **Use tree supports** (available in most modern slicers) — they use less
  material and are easier to remove
- **Increase support Z distance** to 0.2-0.3mm for easier removal (at the
  cost of slightly worse overhang surface)
- **Support interface layers** (2-3 dense layers between support and part)
  give a smoother surface where supports contact the part
- **Design support-free geometry** — the best support is no support. Chamfers,
  teardrops, and smart parting lines eliminate most supports.

## Infill and Strength

### Infill percentage guidelines

| Application | Infill % | Pattern | Notes |
|---|---|---|---|
| Visual prototype | 10-15% | Gyroid or grid | Saves material and time |
| General functional part | 20-30% | Gyroid or cubic | Good balance of strength and speed |
| Structural part | 40-60% | Gyroid or cubic | Significant strength increase |
| Maximum strength | 80-100% | Rectilinear | Diminishing returns above 60% |
| Snap-fit features | 40-60% | — | Needs toughness, not just stiffness |

### Perimeters vs infill for strength

More perimeters (outer walls) contribute more to part strength than higher
infill percentage. For structural parts, 4-5 perimeters with 20-30% infill
is typically stronger than 2 perimeters with 60% infill, and prints faster.

### Infill patterns

- **Gyroid**: best all-round — good strength in all directions, easy to print,
  good for flexible parts
- **Cubic**: good isotropic strength, slightly faster than gyroid
- **Grid/rectilinear**: strong in X and Y, weak diagonally. Fast to print.
- **Honeycomb**: high stiffness-to-weight ratio but slower to print
- **Lightning**: minimal material, fast, only supports top surfaces. Good for
  visual models, not structural.

## Print Orientation Strategy

The user needs to understand that orientation is one of the most impactful
decisions in FDM design.

### Key principles

1. **Layer lines are the weak point.** Parts break between layers, not through
   them. Orient the part so that the primary stress direction runs along the
   layers (X-Y plane), not between them (Z axis).

2. **Bottom surface is smoothest.** The face on the build plate (or on
   supports) is the smoothest surface.

3. **Top surface is second-smoothest.** Good quality with proper settings.

4. **Vertical surfaces have visible layer lines.** Can be sanded or post-
   processed but will never match top/bottom surface quality.

5. **Minimise supports.** Rotate the part to reduce overhang area.

### Orientation for common parts

| Part type | Recommended orientation | Reason |
|---|---|---|
| Enclosure bottom shell | Open side up | No overhangs, smooth outside bottom |
| Enclosure top/lid | Upside down (outside face on bed) | Smooth outer surface |
| Bracket (L-shape) | Standing on the long leg | Maximises strength at the bend |
| Cylinder (hollow) | Vertical (axis = Z) | Clean circular layers |
| Flat plate with holes | Flat on bed | Holes are vertical, print clean |
| Snap-fit arm | So the arm flexes along layers | Prevents layer delamination |

## Text and Fine Detail

### Embossed text (raised)

| Parameter | Minimum | Recommended |
|---|---|---|
| Height above surface | 0.4mm (1 layer at 0.2mm LH) | 0.6-0.8mm |
| Line width | 0.5mm | 0.8mm |
| Font size | 6pt | 8-10pt |
| Font choice | Sans-serif, bold | Arial Bold, Liberation Sans Bold |

### Debossed text (recessed into surface)

| Parameter | Minimum | Recommended |
|---|---|---|
| Depth below surface | 0.4mm | 0.6-0.8mm |
| Line width | 0.5mm | 0.8mm |

Debossed text is generally more reliable than embossed because the slicer
handles it as an inward offset rather than a tiny raised feature.

### Fine detail limits

| Feature | Minimum dimension |
|---|---|
| Positive detail (bump, ridge) | 0.5mm wide, 0.4mm tall |
| Negative detail (groove, channel) | 0.5mm wide, 0.4mm deep |
| Pin / post diameter | 1.5mm (structural), 1.0mm (decorative) |
| Slot width | 0.5mm |

## Thin Features

### Thin walls

Very thin walls (<0.8mm) may not slice correctly — the slicer may skip them
if they are thinner than 2× nozzle diameter. Check the slicer preview before
printing.

### Thin floor/ceiling

Horizontal thin features down to 0.4mm (2 layers at 0.2mm) are printable but
fragile. Use 0.8mm minimum for functional parts.

### Knife edges and sharp points

FDM cannot produce true sharp edges — the minimum radius is approximately
half the nozzle diameter (0.2mm with a 0.4mm nozzle). Design features with
at least 0.5mm radius or flat.

## Warping and Bed Adhesion

### Causes

Warping occurs when the bottom layers cool and contract faster than the upper
layers, pulling corners off the bed. Worse with:

- Large flat parts
- High-shrinkage materials (ABS, nylon, PC)
- Poor bed adhesion
- No heated bed or enclosure

### Mitigation in design

- **Chamfer or fillet bottom edges** — sharp 90° corners concentrate stress
  and peel off. A 1-2mm chamfer helps adhesion enormously.
- **Add mouse ears** — small thin discs (10mm dia, 0.2mm thick) at corners
  for extra adhesion surface. Remove after printing.
- **Avoid large flat surfaces** if possible — slight curvature or ribbing
  reduces warping forces.
- **Brim** — the slicer can add a thin skirt around the part's first layer
  for extra adhesion. 3-5mm brim width is typical.

### Material warping tendency

| Material | Warp risk | Needs heated bed? | Needs enclosure? |
|---|---|---|---|
| PLA | Very low | Helpful (50-60°C) | No |
| PETG | Low | Yes (70-80°C) | No |
| ABS | High | Yes (90-110°C) | Yes |
| ASA | High | Yes (90-110°C) | Yes |
| Nylon | Very high | Yes (70-80°C) | Yes |
| TPU | Very low | Optional (50°C) | No |
| PC | Very high | Yes (110-120°C) | Yes |

## Multi-Part Design

### When to split into multiple parts

- Part exceeds build volume
- Different sections need different materials or colours
- Overhangs would be extreme in a single piece
- Assembly/service access is needed (e.g., replaceable battery door)
- Certain surfaces need specific orientation for quality

### Alignment features

When splitting a part, add registration features so the pieces align correctly:

- **Pins and holes**: 2-3mm diameter pin on one part, matching hole (with
  0.15mm clearance) on the other. Place at least 2 pins for rotational
  alignment.
- **Tongue and groove**: a ridge on one part fits into a channel on the other.
  Good for long straight joints.
- **Dovetail**: mechanical interlock that also resists pull-apart. Good for
  joints that might see tension.

### Joining methods for printed parts

| Method | Strength | Reversible? | Notes |
|---|---|---|---|
| Cyanoacrylate (super glue) | Medium | No | Quick, works on PLA/PETG |
| Epoxy | High | No | Best strength, gap-filling |
| Solvent welding (acetone for ABS) | High | No | Fuses the plastic together |
| Screws + heat-set inserts | High | Yes | Best for serviceable assemblies |
| Snap fits | Medium | Depends on design | No fasteners needed |
| Press-fit pins | Medium | Semi | Simple, needs tight tolerance |
| Friction welding (spin or vibration) | Medium-High | No | Specialised equipment |

## Dimensional Accuracy Table

Quick reference for expected accuracy across common features:

| Feature | Expected accuracy | How to improve |
|---|---|---|
| Overall X/Y dimension | ±0.2mm | Calibrate printer steps/mm, enable pressure advance |
| Overall Z dimension | ±0.1mm | Z is the most accurate axis (stepper-controlled) |
| Hole diameter (vertical) | -0.1 to -0.2mm (undersized) | Oversize in design or drill after |
| Hole diameter (horizontal) | -0.2 to -0.4mm (undersized) | Use teardrop, drill after |
| Slot width | -0.1 to -0.2mm (narrow) | Oversize by 0.1-0.2mm |
| Pin diameter | +0.1 to +0.2mm (oversized) | Undersize by 0.1-0.15mm |
| Mating surface flatness | ~0.1mm over 50mm | Use brim, ensure bed is level |
| First layer elephant's foot | +0.1-0.3mm bulge at base | Reduce first layer squish or add chamfer |

### Elephant's foot compensation

The first layer is usually squished slightly for bed adhesion, causing the base
of the part to bulge outward by 0.1-0.3mm. This matters for parts that need to
mate at the base. Solutions:

- Add a 0.4mm 45° chamfer at the bottom edge (hides the bulge)
- Enable "elephant's foot compensation" in the slicer (shrinks the first layer
  outline slightly)
- Design critical mating features above the first few layers
