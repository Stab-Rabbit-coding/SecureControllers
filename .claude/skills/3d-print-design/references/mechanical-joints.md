# Mechanical Joints Reference

Fastening and joining methods for 3D-printed parts.

## Table of Contents

1. [Heat-Set Inserts](#heat-set-inserts)
2. [Self-Tapping Screws](#self-tapping-screws)
3. [Machine Screws with Nuts](#machine-screws-with-nuts)
4. [Snap Fits](#snap-fits)
5. [Press Fits](#press-fits)
6. [Living Hinges](#living-hinges)
7. [Threaded Interfaces](#threaded-interfaces)
8. [Adhesive Bonding](#adhesive-bonding)
9. [Joint Selection Guide](#joint-selection-guide)

---

## Heat-Set Inserts

Brass threaded inserts pressed into 3D-printed plastic using a soldering iron.
The gold standard for reusable threaded connections in printed parts.

### How they work

The insert has a knurled outer surface. A soldering iron (at ~200-230°C for
PLA, ~240-260°C for PETG/ABS) melts the surrounding plastic as the insert is
pushed in. The plastic flows into the knurls and solidifies, creating a strong
mechanical lock. The result is a metal thread embedded in the plastic that can
handle dozens of screw insertion cycles.

### Sizing

| Insert size | Hole diameter | Hole depth | Boss OD (min) | Recommended boss OD |
| --- | --- | --- | --- | --- |
| M2 × 3.5mm | 3.0-3.2mm | 4.0mm | 5.5mm | 6.0mm |
| M2.5 × 4mm | 3.5-3.6mm | 4.5mm | 6.5mm | 7.0mm |
| M3 × 4mm | 4.0-4.2mm | 4.5mm | 7.0mm | 8.0mm |
| M3 × 5.7mm | 4.0-4.2mm | 6.2mm | 7.0mm | 8.0mm |
| M4 × 5.6mm | 5.3-5.6mm | 6.2mm | 9.0mm | 10.0mm |
| M5 × 7mm | 6.4-6.7mm | 7.5mm | 11.0mm | 12.0mm |

Exact hole diameter depends on the specific insert (check the datasheet).
These values are for CNC Kitchen / McMaster / Ruthex style inserts. Start
with the smaller hole diameter; if the insert pushes in too easily (no
resistance), increase by 0.1mm.

### Installation tips

- Use a dedicated soldering iron tip (flat or insert-shaped, not pointed) —
  a point concentrates heat and can push through the insert
- Slow and steady: let the iron melt the plastic, do not force it
- Push the insert slightly below flush (~0.2mm) so the mating surface sits flat
- Keep the insert perpendicular — a jig or printed alignment guide helps
- Let it cool for 30+ seconds before applying force

### Common insert brands

- CNC Kitchen (excellent documentation and tested dimensions)
- Ruthex (widely available on Amazon)
- McMaster-Carr (industrial supply, precise datasheets)
- Virtjoule (good budget option)

## Self-Tapping Screws

Screws that cut their own thread directly into the plastic. Simpler than
heat-set inserts but less durable.

### When to use

- Low assembly/disassembly frequency (< 5-10 cycles)
- Cost-sensitive designs (no insert needed)
- Prototypes where insert installation is not worth the effort

### Pilot hole sizing

| Screw | Pilot hole dia | Boss OD (min) | Engagement depth (min) |
| --- | --- | --- | --- |
| M2 self-tap | 1.6-1.7mm | 4.5mm | 4mm |
| M2.5 self-tap | 2.0-2.1mm | 5.5mm | 5mm |
| M3 self-tap | 2.4-2.5mm | 6.5mm | 6mm |
| M4 self-tap | 3.2-3.3mm | 8.0mm | 8mm |
| #4 (US) | 2.0-2.1mm | 5.0mm | 5mm |
| #6 (US) | 2.6-2.7mm | 6.0mm | 6mm |

### Screw type

Use thread-forming screws (not thread-cutting). Thread-forming displaces
plastic without removing material, creating a stronger joint. Look for:

- "PT" or "Plastite" style screws
- Or standard sheet metal screws with coarse thread pitch

### Design notes

- Make the pilot hole 1-2mm deeper than the screw penetration (so the screw
  does not bottom out)
- Add a countersink or counterbore if a flush surface is needed
- First insertion creates the thread; re-insertion follows the same thread
  path if the screw is started carefully
- Overtightening strips the threads — use a screwdriver, not a power driver

## Machine Screws with Nuts

Standard metric machine screws (M2, M2.5, M3, M4) with hex nuts or square
nuts captured in printed pockets.

### Through-hole sizing

| Screw | Clearance hole | Close-fit hole |
| --- | --- | --- |
| M2 | 2.4mm | 2.2mm |
| M2.5 | 3.0mm | 2.7mm |
| M3 | 3.4mm | 3.2mm |
| M4 | 4.5mm | 4.2mm |

### Hex nut pockets

Print a hexagonal pocket on the blind side so the nut drops in and is held
captive while the screw is tightened from the other side.

| Nut | Across flats (AF) | Pocket size (AF + clearance) | Pocket depth |
| --- | --- | --- | --- |
| M2 | 4.0mm | 4.4mm | 1.8mm (or 2.0mm for easy insertion) |
| M2.5 | 5.0mm | 5.4mm | 2.2mm |
| M3 | 5.5mm | 5.9mm | 2.6mm |
| M4 | 7.0mm | 7.4mm | 3.4mm |

Design the pocket so the nut can be inserted from one direction but cannot
spin when the screw is tightened. A hexagonal pocket does this naturally.

### Square nut channels

An alternative to hex pockets: a channel that the nut slides into from the
side. Easier to assemble in tight spaces.

Channel width = nut width + 0.3mm
Channel height = nut thickness + 0.2mm

## Snap Fits

Flexible arms that deflect during assembly and lock into a mating feature.
No fasteners required.

### Cantilever snap fit (most common)

A flexible arm with a hook at the end. The arm deflects as the mating part is
pressed on, then the hook snaps into a catch.

```text
Design parameters:
  Arm length (L):    10-20mm (longer = more flexible, less insertion force)
  Arm thickness (t): 1.0-1.5mm (thinner = more flexible)
  Arm width (w):     3-5mm
  Hook depth (h):    0.3-0.8mm (how far the hook engages)
  Lead-in angle:     30-45° (ramp for easy insertion)
  Return angle:      60-90° (steeper = harder to remove)
```

### Strain calculation

Maximum strain in the arm during deflection must stay below the material's
yield strain:

```text
Strain = 1.5 × h × t / L²

Material yield strains:
  PLA:   ~1.5% (brittle, snap fits often break)
  PETG:  ~3-4% (good for snap fits)
  ABS:   ~3-4% (good)
  Nylon: ~5-7% (excellent, very flexible)
  TPU:   ~20%+ (extremely flexible)
```

Example: arm 15mm long, 1.2mm thick, 0.5mm hook depth:
Strain = 1.5 × 0.5 × 1.2 / (15²) = 0.4% — safe for all materials.

### FDM-specific considerations

- **Print orientation matters**: the arm must flex along the layers, not
  between them. If the arm flexes between layers, it will delaminate and snap.
- **PLA snap fits are fragile** — they work initially but become brittle
  over time and with temperature cycling. Use PETG or ABS for production.
- **Add fillets** at the arm base to reduce stress concentration.
- **Design for disassembly**: if the snap fit needs to be opened, add a lever
  feature (small tab the user can press to release the hook).

### Annular snap fit (circular)

A ring of flexible material that snaps over or into a cylindrical feature.
Used for bottle caps, pen caps, round enclosures.

Design: a ring with a slight undercut (0.3-0.5mm interference). The ring
expands as it passes over the larger diameter and contracts into the groove.

## Press Fits

One part is slightly larger than the hole it goes into, so it's held by
friction/interference.

### Interference values for FDM

| Application | Interference per side | Notes |
| --- | --- | --- |
| Light press (removable) | 0.05-0.1mm | Pin can be pulled out by hand |
| Medium press (firm) | 0.1-0.15mm | Needs tool to remove |
| Tight press (semi-permanent) | 0.15-0.2mm | May crack PLA; use PETG |

Example: a 5mm pin into a 5mm hole with 0.1mm interference per side:
design the hole as 4.8mm diameter.

### Alignment features

Press-fit pins alone do not resist rotation. Add at least 2 pins spaced apart,
or combine a pin with a flat/D-shape to prevent spinning.

## Living Hinges

A thin, flexible section that acts as a hinge between two rigid sections.
Allows a lid to open and close without a separate hinge mechanism.

### FDM living hinges

FDM is poorly suited to living hinges because:

- Layer lines create weak points perpendicular to the bend
- PLA is too brittle for repeated bending
- Even PETG fatigues after 50-100 cycles in thin sections

### If you must

- **Material**: TPU or Nylon only (PETG for <20 cycles)
- **Thickness**: 0.4-0.6mm (1-2 layers)
- **Width**: as wide as the hinge line
- **Print orientation**: layer lines parallel to the hinge axis (NOT
  perpendicular)
- **Geometry**: add a semicircular groove at the hinge line to concentrate
  bending and prevent cracking across the full section

### Better alternatives

- Separate hinge pin (printed cylinder through printed lugs)
- Commercial small hinge (sourced from hardware store)
- TPU flex joint (a short section of TPU between rigid PLA parts, printed as
  a multi-material assembly or glued)

## Threaded Interfaces

### Printed threads (coarse only)

FDM can produce functional threads, but only coarse ones:

| Thread | Minimum printable | Notes |
| --- | --- | --- |
| M6 × 1.0mm pitch | Marginal | Fine pitch, barely printable |
| M8 × 1.25mm | Acceptable | Functional with cleanup |
| M10 × 1.5mm | Good | Reliable |
| M12+ | Good | Works well |
| Bottle threads (e.g., 28mm PCO-1881) | Good | Very coarse, designed for plastic |

For threads smaller than M8, use heat-set inserts instead.

### OpenSCAD thread libraries

- **BOSL2** library: `thread_helix()`, `threaded_rod()`, `threaded_nut()`
- **NopSCADlib**: parametric screws, nuts, washers, inserts

### Thread tolerance

Add 0.2-0.3mm to the thread profile clearance for FDM. A bolt and nut printed
on the same printer with nominal dimensions will not thread together — the
male thread needs to be undersized or the female thread oversized.

## Adhesive Bonding

### Adhesive selection

| Adhesive | Best for | Set time | Strength | Gap-filling? |
| --- | --- | --- | --- | --- |
| Cyanoacrylate (super glue) | PLA, PETG, ABS | 10-30 sec | Medium | No (thin bond line only) |
| CA + accelerator | Same, faster cure | 2-5 sec | Medium | No |
| 5-minute epoxy | All plastics | 5-10 min | High | Yes |
| Slow epoxy (30 min) | Structural bonds | 30 min+ | Very high | Yes |
| Solvent (acetone) | ABS only | 1-5 min | Very high | Somewhat |
| Solvent (MEK/DCM) | ABS, PETG | 1-5 min | Very high | Somewhat |
| Hot glue | Temporary, non-structural | 30 sec | Low | Yes |
| 3M VHB tape | Flat mating surfaces | Instant hold | Medium-High | No |

### Joint design for adhesives

- Maximise contact area (wide, thin bond lines are stronger than narrow, thick)
- Use tongue-and-groove or lap joints to increase area
- Surface prep: light sanding (220 grit) dramatically improves adhesion
- Avoid relying on adhesive alone for joints that see peel forces (where the
  bond line is opened from one edge) — adhesives are strong in shear but weak
  in peel

## Joint Selection Guide

| Requirement | Best method |
| --- | --- |
| Repeated disassembly (>10 cycles) | Heat-set inserts + machine screws |
| Occasional disassembly (5-10 cycles) | Self-tapping screws |
| Tool-free assembly | Snap fits |
| Permanent assembly | Adhesive (epoxy or solvent weld) |
| Vibration resistance | Heat-set inserts or Nyloc nuts |
| Alignment-critical | Press-fit pins + screws |
| Low cost, no hardware | Snap fits or adhesive |
| Prototype (will be redesigned) | Self-tapping screws or clips |
| Waterproof joint | Epoxy or solvent weld + gasket |
