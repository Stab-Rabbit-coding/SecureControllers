# Enclosure Design Reference

Design patterns for 3D-printed enclosures housing PCBs and electronics.

## Table of Contents

1. [Enclosure Sizing from PCB](#enclosure-sizing)
2. [Parting Line Strategies](#parting-line-strategies)
3. [PCB Mounting Methods](#pcb-mounting-methods)
4. [Connector Cutouts](#connector-cutouts)
5. [Button and Switch Access](#button-and-switch-access)
6. [LED Light Pipes](#led-light-pipes)
7. [Display Windows](#display-windows)
8. [Ventilation Design](#ventilation-design)
9. [Cable Management](#cable-management)
10. [Labelling and Branding](#labelling-and-branding)
11. [IP Rating Considerations](#ip-rating-considerations)
12. [Standard Enclosure Templates](#standard-enclosure-templates)

---

## Enclosure Sizing

### Calculating internal dimensions from PCB

Start with these measurements from the PCB design (or physical board):

- **Board X, Y** — overall PCB dimensions
- **Board Z** — PCB thickness (typically 1.6mm)
- **Top clearance** — height of tallest component on the top side
- **Bottom clearance** — height of tallest component on the bottom side (often
  just solder joints: 0.5-1mm; more if through-hole components are present)
- **Connector protrusion** — how far connectors extend beyond the board edge
- **Mounting hole positions** — X,Y coordinates and hole diameter

### Internal cavity formula

```
Internal width  = Board X + 2 × side_clearance
Internal depth  = Board Y + 2 × side_clearance
Internal height = bottom_clearance + Board Z + top_clearance + lid_clearance

Where:
  side_clearance  = 0.5mm (minimum) to 1.0mm (comfortable)
  lid_clearance   = 1.0mm (minimum gap between tallest component and lid)
```

### Overall external dimensions

```
External width  = Internal width  + 2 × wall_thickness
External depth  = Internal depth  + 2 × wall_thickness
External height = Internal height + floor_thickness + ceiling_thickness

Where:
  wall_thickness    = 1.6-2.0mm (recommended for FDM enclosures)
  floor_thickness   = 1.2-1.6mm
  ceiling_thickness = 1.2-1.6mm
```

### Parametric approach

Define all dimensions as parameters at the top of the design:

```
// Example parameters (adapt to actual board)
pcb_x = 65;          // Board width
pcb_y = 35;          // Board depth
pcb_z = 1.6;         // Board thickness
top_clearance = 12;  // Tallest top component
bot_clearance = 1;   // Bottom side clearance
side_clearance = 0.8;
wall = 2.0;
floor_t = 1.6;
ceil_t = 1.6;
lid_gap = 1.0;

// Derived
int_x = pcb_x + 2*side_clearance;
int_y = pcb_y + 2*side_clearance;
int_z = bot_clearance + pcb_z + top_clearance + lid_gap;
ext_x = int_x + 2*wall;
ext_y = int_y + 2*wall;
ext_z = int_z + floor_t + ceil_t;
```

## Parting Line Strategies

The "parting line" is where the enclosure splits into separate printed parts.

### Top/bottom shell (most common)

The enclosure splits horizontally into a bottom tray and a top lid. The PCB
sits in the bottom tray on standoffs.

**Advantages**: simple, both halves print flat-side-down with no supports,
connectors can be accessed from the sides.

**Parting height**: typically at the PCB level or just above the tallest
bottom-side component.

### Clamshell (left/right split)

The enclosure splits vertically. Both halves are mirror images (or near
mirrors).

**Advantages**: both connector-side walls are part of the same half (no
alignment issues at cutouts), good for elongated shapes.

**Disadvantages**: usually needs supports for internal features in each half.

### Slide-on lid

The bottom tray has rails, and the lid slides on from one end. No screws
needed.

**Advantages**: tool-free assembly, clean appearance.
**Disadvantages**: one end must remain open or have a separate endcap. Rail
tolerances must be tight.

### Bayonet/twist-lock

Circular enclosures with a twist-to-lock lid. Good for sensor housings and
round devices.

## PCB Mounting Methods

### Screw-down standoffs (most reliable)

Cylindrical posts rising from the enclosure floor, with holes matching the
PCB mounting holes. The PCB sits on the standoff shoulders and is secured with
screws from below or above.

```
Standoff dimensions:
  Height = bot_clearance (space under PCB for bottom components/solder joints)
  Outer diameter = mounting_hole_dia + 2 × 2.0mm (minimum wall around hole)
  Inner hole = screw clearance diameter (e.g., 3.4mm for M3) if screw comes
               from above, or tap diameter (2.5mm for M3) if self-tapping
               into the plastic

For heat-set insert standoffs:
  Inner hole = insert outer diameter - 0.1mm (press fit; check insert datasheet)
  Outer diameter = insert OD + 2 × 1.5mm minimum
```

### Self-tapping into plastic

Use screws designed for plastic (thread-forming, e.g., "plastite" style). The
standoff hole is slightly smaller than the screw's major diameter. The screw
cuts its own thread on first insertion.

| Screw size | Pilot hole diameter | Boss OD (minimum) |
|---|---|---|
| M2 self-tap | 1.6-1.7mm | 4.0mm |
| M2.5 self-tap | 2.0-2.1mm | 5.0mm |
| M3 self-tap | 2.4-2.5mm | 6.0mm |

Limitations: 5-10 insertion cycles before the threads strip. For designs
needing frequent disassembly, use heat-set inserts.

### Heat-set insert standoffs (best for repeated assembly)

Brass threaded inserts are pressed into a slightly undersized hole using a
soldering iron. They provide durable metal threads in the plastic.

Standard sizes: M2, M2.5, M3. Knurled outer surface grips the plastic.

See `mechanical-joints.md` for detailed installation parameters.

### Snap-in clips (no fasteners)

Flexible arms with hooks grip the PCB edges. No screws needed.

Design considerations:

- Arm thickness: 1.0-1.5mm (must flex without breaking)
- Hook engagement: 0.5-0.8mm over the PCB edge
- Must grip at a minimum of 2 opposite edges (preferably 3-4)
- Include a slight lead-in ramp for easy PCB insertion
- PLA snap arms are brittle and may break over time; PETG is better

### Friction slot

The PCB slides into grooves (rails) molded into the enclosure walls. Simple
but only constrains 4 DOF — need an additional feature (end wall or retainer
clip) to prevent sliding out.

Rail dimensions:

- Slot width = PCB thickness + 0.3-0.4mm (for 1.6mm PCB: 1.9-2.0mm)
- Slot depth = 1.5-2.0mm
- Rail height = at least 5mm for stable grip

## Connector Cutouts

### Sizing connector openings

Measure the connector's mating face (where the cable plugs in) and add
clearance:

| Connector | Opening width | Opening height | Notes |
|---|---|---|---|
| USB-C | 9.5mm | 3.5mm | Centred on connector; allow ±0.5mm alignment tolerance |
| USB Micro-B | 8.5mm | 3.2mm | Wider at top for cable strain relief |
| USB-A | 13.5mm | 6.0mm | Tight fit reduces wobble |
| Barrel jack (5.5/2.1mm) | 6.0mm dia hole | — | Round hole, may need flat for alignment |
| RJ45 | 12.5mm | 11.5mm | Large; structural wall around it helps |
| 3.5mm audio jack | 4.0mm dia hole | — | Round hole |
| DB9 | 18.5mm | 10.5mm | Plus screw holes at 24.99mm apart |
| Pin header (2.54mm) | Per pin count | 3.5mm | Slot for pin header access |

### Cutout placement

1. Measure connector position on the PCB: distance from board edge to
   connector centre
2. Account for PCB mounting position in the enclosure: standoff height, side
   clearance
3. The cutout in the enclosure wall must align with the connector position
   on the mounted PCB

```
cutout_centre_from_floor = floor_t + bot_clearance + pcb_z/2 + connector_centre_above_pcb
cutout_centre_from_wall  = wall + side_clearance + connector_centre_from_pcb_edge
```

### Alignment tolerance

Add 0.3-0.5mm to each side of the cutout for alignment tolerance. A cable
that cannot plug in because the cutout is 0.2mm off is the most frustrating
kind of failure.

If precision alignment is critical, consider an overly large cutout with a
removable bezel that snaps or screws around the connector. The bezel is a
small, quick print if it needs adjustment.

## Button and Switch Access

### Through-wall button plunger

For tactile switches on the PCB, a printed plunger passes through a hole in
the enclosure wall and contacts the switch button.

```
Plunger design:
  Shaft diameter = hole diameter - 0.4mm (0.2mm clearance per side)
  Shaft length = wall_thickness + travel + 1mm (so it protrudes slightly)
  Head diameter = shaft + 3-4mm (prevents falling inward)
  Retention: internal shoulder or snap ring to prevent pushing too far

Hole in enclosure:
  Diameter = plunger shaft + 0.4mm total clearance
  Countersink on outside for a flush appearance
```

Alternative: a flexible membrane (thin-wall dome) integrated into the
enclosure wall, printed in TPU or as a thin PLA/PETG section. Deforms under
finger pressure and returns. More elegant but harder to get right.

### Toggle switch cutout

Standard mini toggle switch (MTS series) needs a 6.0-6.5mm round hole.
Add a flat on one side for the anti-rotation tab if present.

### Rocker switch cutout

Standard KCD1 rocker switch: 19.5mm × 13mm rectangular cutout.
Snap-fit from outside; the switch's own clips hold it in the panel.

## LED Light Pipes

To make a PCB-mounted LED visible through the enclosure wall:

### Simple hole method

Drill or print a hole above the LED, sized to the LED diameter + 0.5mm.
Light spills and is visible. Not elegant but functional.

### Printed light pipe

A transparent or translucent cylindrical rod bridging from the LED to the
enclosure surface. Print in transparent PETG or clear resin.

```
Light pipe dimensions:
  Inner end: sits 0.5-1mm above the LED
  Outer end: flush with or slightly protruding from enclosure surface
  Diameter: 2-3mm (for standard 3mm LEDs)
  Press fit into the enclosure wall with 0.1mm interference
```

For FDM, light pipes work poorly because layer lines scatter light. Best
results come from:

- Printing vertically (layer lines parallel to light direction)
- Using clear PETG with 100% infill
- Polishing the ends

For production quality, consider a commercial acrylic light pipe (Bivar,
Dialight, VCC) press-fit into the enclosure.

## Display Windows

For OLED/LCD displays visible through the enclosure:

### Open window

A rectangular cutout in the lid, sized to the display's active area + 0.5mm
per side. Simple but exposes the display to dust and fingers.

### Recessed window with clear panel

The cutout is larger than the display, with a step (rebate) on the inside for
a clear acrylic or polycarbonate window panel to sit in.

```
Window rebate:
  Outer opening: display active area + 1mm per side
  Rebate depth: acrylic panel thickness + 0.3mm (e.g., 1.8mm for 1.5mm acrylic)
  Rebate inset: 1.5-2.0mm per side (ledge for the panel to sit on)
```

Secure the window panel with a dab of clear silicone, double-sided tape, or
snap-in retainer clips.

## Ventilation Design

### When ventilation is needed

Any electronics dissipating more than ~1W in an enclosed space should have
ventilation. Calculate: if the internal temperature rise matters (e.g., near
a voltage regulator's thermal limit), ventilation is required.

### Slot ventilation

Horizontal or vertical slots through the enclosure wall:

- Slot width: 1.0-1.5mm (small enough to block fingers and most debris)
- Slot length: 10-30mm
- Spacing: 2-3mm between slots (thinner ribs are fragile)
- Total open area: aim for 20-30% of the ventilated wall section

### Honeycomb/hex grid

More aesthetically pleasing and structurally rigid than slots:

- Hex cell size: 4-6mm across flats
- Wall between cells: 1.0-1.5mm
- Print orientation: the hex grid should be in the X-Y plane (each hex wall
  is vertical, prints perfectly with no supports)

### Convection flow

Place intake vents low, exhaust vents high. Hot air rises — design the airflow
path so it enters at the bottom (near cool ambient air) and exits at the top
(where the heated air naturally wants to go). Position heat-generating
components (regulators, power resistors) near the exhaust vents.

If active cooling is needed, standard 25mm, 30mm, or 40mm DC fans can be
mounted in the enclosure with a circular cutout + screw holes. Fan hole
patterns are standardised.

## Cable Management

### Strain relief

External cables entering the enclosure need strain relief so tugging on the
cable does not stress the PCB solder joints.

**Printed strain relief**: a channel or clip inside the enclosure that grips
the cable jacket near the entry point. The cable exits through a hole in the
wall and is anchored inside before reaching the PCB.

**Zip-tie anchor**: a slot near the cable entry for a zip tie around the cable.
Simple and effective.

**PG-style cable gland**: for more professional/sealed applications. The
enclosure needs a round hole matching the gland's thread diameter (typically
PG7 for small cables: 12.5mm hole).

### Internal cable routing

- Add channels or clips to route flat-flex cables or wire harnesses
- Keep cables away from hot components
- Leave slack for assembly and service access
- Consider how the enclosure goes together — can the lid be removed without
  disconnecting any cables? If not, add connectors.

## Labelling and Branding

### Embossed/debossed text on enclosure

- Use debossed text on top surfaces (recessed into the surface) — it prints
  more reliably than embossed
- Font: bold sans-serif, minimum 8pt (see `fdm-design-rules.md` for detail
  limits)
- Depth: 0.4-0.6mm
- For product labels, include: product name, version, regulatory marks,
  power input rating, company/logo

### Connector labels

Label each connector cutout on the enclosure exterior:

- Debossed text above or beside each connector opening
- Include: port name (USB, POWER, HDMI), polarity for DC jacks, voltage

### Regulatory marking space

If the product will be certified (CE, FCC), reserve space on the enclosure
for the required marks. Typical: 10mm × 5mm area on the bottom or rear.

## IP Rating Considerations

IP (Ingress Protection) ratings define resistance to dust and water. Relevant
for outdoor or wet-environment enclosures.

### Achievable IP ratings with FDM

| Rating | Protection | Achievable with FDM? | How |
|---|---|---|---|
| IP20 | Touch-safe (no finger entry) | Yes, trivially | <12.5mm openings |
| IP40 | No objects >1mm | Yes | Vent slots <1mm or filtered |
| IP54 | Dust-protected, splash-proof | Difficult | Gaskets at parting line, sealed cutouts |
| IP65+ | Dust-tight, water jet proof | Not really | Use resin printing or injection moulding |

### Sealing the parting line

For IP54-ish protection:

- Add a groove in one half and a ridge in the other (tongue-and-groove joint)
  to create a labyrinth seal
- Or add a groove for an O-ring or foam gasket strip
- Seal connector cutouts with the connector's own gasket (if rated) or with
  silicone sealant
- Cable entry via PG/metric cable glands

FDM parts are inherently porous between layers. For true water-tightness,
post-process with epoxy coating or vapour smoothing (ABS only), or use resin
printing.

## Standard Enclosure Templates

### Simple box with screw-down lid

The most common first enclosure. Bottom tray with standoffs, four corner screw
bosses. Lid screws down with M3 screws into heat-set inserts in the bosses.

Key parameters:

- 4 screw bosses at corners (inset 5mm from edges)
- Heat-set M3 inserts in bottom half
- Lid has countersunk M3 through-holes
- 1mm lip/ridge on the tray for lid alignment
- PCB standoffs at board mounting hole locations

### Snap-fit box

Bottom tray and top lid join with snap-fit hooks. No screws, no inserts.

Key parameters:

- 4 snap hooks on tray walls (midpoint of each wall, or 2 per long side)
- Matching catch slots in the lid
- Alignment ridge/groove at the parting line
- Slightly rounded hooks for easy engagement

### Slide-on lid enclosure

Tray with dovetail rails on two walls. Lid has matching dovetail grooves and
slides on from one end.

Key parameters:

- Dovetail angle: 60°
- Rail height: 2-3mm
- Clearance: 0.2mm per mating surface
- End stop or catch to prevent the lid overshooting
