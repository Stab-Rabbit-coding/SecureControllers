# Resin Printing (SLA / MSLA / DLP) Design Rules

Design rules for vat photopolymerisation processes. Covers SLA (laser),
MSLA (masked/LCD), and DLP (projector) resin printing.

## Table of Contents

1. [Technology Overview](#technology-overview)
2. [When to Use Resin over FDM](#when-to-use-resin)
3. [Dimensional Tolerances](#tolerances)
4. [Wall Thickness and Features](#wall-thickness)
5. [Supports and Orientation](#supports-and-orientation)
6. [Hollowing and Drain Holes](#hollowing)
7. [Resin Types](#resin-types)
8. [Post-Processing](#post-processing)
9. [Safety](#safety)
10. [Design Rule Summary](#design-rule-summary)

---

## Technology Overview

All three processes cure liquid photopolymer resin with UV light, layer by
layer, building the part upside-down from a build plate that lifts out of (or
peels away from) a resin vat.

| Process | Light source | How it works | Strengths |
| --- | --- | --- | --- |
| SLA | UV laser | Laser traces each layer point by point | Highest accuracy, excellent surface finish |
| MSLA | UV LED + LCD mask | Entire layer exposed at once through LCD | Fast (entire layer at once), affordable printers |
| DLP | UV projector | Entire layer projected at once | Fast, good detail, higher power than LCD |

**Key difference from FDM**: resin prints are isotropic (equally strong in all
directions) because each layer chemically bonds to the previous one, rather
than relying on thermoplastic adhesion. However, resin parts are generally
more brittle than FDM thermoplastics unless using tough/engineering resins.

## When to Use Resin

Use resin printing when:

- Fine surface finish matters (Ra 1-5 µm vs FDM's ~15-25 µm)
- Small, intricate details are required (miniatures, jewellery, dental)
- Dimensional accuracy better than ±0.15mm is needed
- Transparent or optically clear parts are required
- The part will be used as a master pattern for moulding
- Specific resin properties are needed (castable, biocompatible, high-temp)

Use FDM instead when:

- Part needs to be tough and impact-resistant
- Part is larger than ~200mm in any dimension
- Cost per part matters (resin is 2-5x more expensive per part)
- Food contact is needed (resins are not food-safe)
- Extensive post-processing is not acceptable (resin always needs wash + cure)

## Tolerances

### Dimensional accuracy by printer class

| Printer class | XY tolerance | Z tolerance | Notes |
| --- | --- | --- | --- |
| Desktop MSLA (Elegoo, Anycubic) | ±0.1-0.15mm | ±0.05-0.1mm | Good for hobbyist use |
| Prosumer MSLA/DLP (Phrozen, Prusa) | ±0.05-0.1mm | ±0.05mm | Higher-res LCD panels |
| Professional SLA (Formlabs Form 4) | ±0.15% (min ±0.02mm) for <30mm features | ±0.05mm | Best accuracy at small scale |
| Industrial SLA | ±0.1mm + 0.1% of dimension | ±0.05mm | Large build volume, calibrated |

### Shrinkage

Resin parts shrink during curing and again during post-cure:

- During print: 0.2-0.5% volumetric shrinkage (resin-dependent)
- During post-cure: additional 0.1-0.3%
- Total: plan for 0.3-0.8% linear shrinkage

Most slicers include shrinkage compensation. Calibrate with a test print for
critical dimensions. Thick cross-sections shrink and warp more than thin ones
because differential cooling creates internal stresses.

### Clearance for mating parts

| Fit type | Clearance per side | Notes |
| --- | --- | --- |
| Press fit | 0.05mm | Very tight, may need sanding |
| Snug/push fit | 0.1mm | Parts stay together without fasteners |
| Sliding fit | 0.15-0.2mm | Moveable joints |
| Assembly clearance | 0.5mm | Between parts printed together |

## Wall Thickness

### Minimum wall thickness

| Feature | Minimum | Recommended |
| --- | --- | --- |
| Unsupported wall | 0.5mm | 0.8-1.0mm |
| Supported wall (backed by other geometry) | 0.3mm | 0.5mm |
| Floor/ceiling (horizontal thin section) | 0.3mm | 0.5mm |
| Pin/post diameter | 1.0mm | 1.5mm |
| Slot/channel width | 0.5mm | 0.8mm |
| Minimum feature size (detail) | 0.2mm | 0.3mm |
| Text height (embossed) | 0.3mm rise | 0.5mm rise, bold font |
| Text height (debossed) | 0.3mm depth | 0.5mm depth |
| Hole diameter (minimum printable) | 0.5mm | 1.0mm |

### Large solid sections (avoid)

Large solid cross-sections cause:

- Increased shrinkage and warping during cure
- Longer print times and higher resin consumption
- Greater suction forces during peel, risking print failure

Hollow the part where possible (see Hollowing section).

## Supports and Orientation

### Support requirements

Unlike FDM, resin parts print upside-down and are pulled upward from the vat.
Every layer must resist peel forces. Supports serve two purposes:

1. Hold overhanging geometry (same as FDM)
2. Anchor the part to the build plate against peel forces

### Orientation strategy

1. **Tilt the part 15-45° from flat** to reduce the cross-sectional area of
   each layer. This reduces peel forces and prevents large flat layers from
   causing suction-cup effects.
2. **Place the least important surface toward the build plate** (where
   supports attach). Support contact points leave small marks (nubs).
3. **Orient to minimise large horizontal cross-sections** — each layer's area
   determines peel force and print reliability.
4. **Minimise "cupping"** — concave shapes facing the build plate trap resin
   and create suction. Add drain holes or rotate to avoid cups.

### Support settings

| Parameter | Typical value | Notes |
| --- | --- | --- |
| Support tip diameter | 0.3-0.5mm | Smaller = easier removal, larger = more reliable |
| Support density | Medium (auto-generated) | More supports = safer print but more cleanup |
| Contact depth | 0.2-0.3mm | How deep supports penetrate the part surface |
| Raft | Yes (recommended) | Provides stable base for supports |

## Hollowing

### Why hollow

Hollowing reduces resin consumption (40-60% savings), print time, and internal
stresses. For parts thicker than ~5mm, hollowing is recommended.

### Shell thickness

Hollow with 1.5-2.5mm wall thickness. Thinner shells risk cracking; thicker
shells negate the savings.

### Drain holes

Hollow parts must have at least 2 drain holes (ideally 3) to:

1. Let uncured resin flow out during printing
2. Allow IPA wash solution to circulate during cleaning
3. Prevent pressure buildup during post-cure (trapped resin expands when
   heated and can crack the part)

Drain hole minimum diameter: 2.5-3mm. Place them at the lowest points when
the part is in print orientation.

## Resin Types

### Standard resin

General-purpose, cheapest. Good surface finish, moderate strength, brittle.
Suitable for display models, visual prototypes, miniatures.

Tensile strength: 30-50 MPa. Elongation: 3-6%. HDT: 50-60°C.

### Tough / ABS-like resin

Improved impact resistance and slight flexibility compared to standard.
Suitable for functional prototypes that may be dropped or handled.

Tensile strength: 40-55 MPa. Elongation: 20-40%. HDT: 55-70°C.

### Flexible / rubber-like resin

Produces elastomeric parts. Shore hardness ranges from 30A (very soft) to 80A
(firm rubber). Suitable for gaskets, grips, bumpers, wearable prototypes.

Tensile strength: 3-10 MPa. Elongation: 100-200%.

### High-temperature resin

Withstands sustained high temperatures without deformation. Suitable for
moulds, jigs near heat sources, under-bonnet automotive prototypes.

HDT: 200-300°C (after extended post-cure). Brittle at room temperature.

### Engineering / rigid resin (e.g., Formlabs Rigid 10K)

Glass-fibre-filled. Very stiff, minimal shrinkage. Suitable for moulds,
jigs, fixtures, wind tunnel models.

Tensile strength: 50-65 MPa. Flexural modulus: 7-10 GPa.

### Castable resin

Burns out cleanly in a kiln for investment casting (lost-wax). Used in
jewellery and dental applications. The printed part is not the final product;
it is the sacrificial pattern.

### Dental / biocompatible resin

Certified for intraoral use (surgical guides, aligners, denture bases).
Requires specific post-processing protocols for biocompatibility. Not
relevant to typical maker/engineering projects but worth knowing exists.

### Transparent / clear resin

Produces optically clear parts when properly post-processed (sanding through
progressive grits + clear coat or dip in resin and cure). Suitable for light
pipes, lenses, fluidic channels, display cases.

Standard clear resin prints translucent; achieving true transparency requires
significant post-processing.

## Post-Processing

Every resin print requires post-processing. This is non-negotiable.

### Mandatory steps

1. **Wash** — remove uncured resin in isopropyl alcohol (IPA, 90%+) or a
   manufacturer's wash solution. 2-5 minutes in agitated bath, or use a wash
   station (Elegoo Mercury, Anycubic Wash & Cure, Formlabs Form Wash).
   Two-stage wash (dirty IPA then clean IPA) gives better results.

2. **Dry** — let the part dry fully after washing. Residual IPA on the
   surface causes a cloudy/chalky finish after curing.

3. **Post-cure** — expose the part to UV light at elevated temperature
   (typically 60°C + 405nm UV for 15-60 minutes depending on resin).
   Post-curing completes the polymerisation, dramatically improving
   mechanical properties and dimensional stability. Uncured prints are
   soft and will degrade over time.

### Optional steps

1. **Support removal** — remove supports with flush cutters. Sand nubs smooth.
2. **Sanding** — progressive grit (220 → 400 → 800 → 1500) for smooth finish.
3. **Clear coating** — spray clear lacquer for UV protection and gloss.
4. **Painting** — resin accepts primer and paint well after light sanding.

### UV stability

Most resin prints yellow and become brittle with prolonged UV/sunlight
exposure. For parts used outdoors or near windows, apply UV-resistant clear
coat, or use a UV-stable resin formulation (available from some manufacturers).

## Safety

Resin printing involves hazardous chemicals. The skill must warn the user:

- **Uncured resin is a skin sensitiser.** Repeated skin contact causes
  allergic reactions (contact dermatitis) that may become permanent. Always
  wear nitrile gloves when handling resin or uncured prints.
- **Wear safety glasses** to protect from splashes.
- **Ventilation**: printing and especially IPA washing release VOCs. Print in
  a ventilated area. Post-processing (IPA wash) generates the highest VOC
  concentrations — do this near an open window or under extraction.
- **IPA is flammable.** Store away from heat sources.
- **Dispose of resin properly.** Cure waste resin in sunlight before disposal.
  Do not pour liquid resin down the drain.

## Design Rule Summary

Quick reference for resin design:

```text
Minimum wall thickness:          0.5mm (unsupported), 0.3mm (supported)
Minimum feature size:            0.2mm
Minimum pin diameter:            1.0mm
Minimum hole diameter:           0.5mm
Minimum slot width:              0.5mm
Dimensional tolerance:           ±0.1mm (desktop), ±0.05mm (professional)
Clearance (assembly):            0.5mm between printed-together parts
Clearance (push fit):            0.1mm per side
Shrinkage compensation:          0.3-0.8% (resin-dependent)
Hollow shell thickness:          1.5-2.5mm
Drain hole minimum:              2.5mm diameter, 2-3 holes
Post-cure:                       Always required (15-60 min UV @ 60°C)
```
