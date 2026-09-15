# PCB Design Rules Reference

Design rule values for PCB layout. Defaults target JLCPCB/PCBWay budget
fabrication. Generic/conservative values noted where they differ.

## Table of Contents

1. [Fabrication Capabilities](#fabrication-capabilities)
2. [Trace Width Calculator](#trace-width-calculator)
3. [Via Sizing](#via-sizing)
4. [Clearance Rules](#clearance-rules)
5. [Impedance Control](#impedance-control)
6. [Copper Pour Rules](#copper-pour-rules)
7. [Silkscreen Rules](#silkscreen-rules)
8. [Board Outline Rules](#board-outline-rules)
9. [Panelisation](#panelisation)
10. [Surface Finishes](#surface-finishes)
11. [Solder Mask](#solder-mask)
12. [Design Rule Summary Table](#design-rule-summary-table)

---

## Fabrication Capabilities

### JLCPCB standard capabilities (2-layer, most common)

| Parameter | Minimum | Recommended |
|---|---|---|
| Minimum trace width | 0.127mm (5mil) | 0.2mm (8mil) or wider |
| Minimum spacing | 0.127mm (5mil) | 0.2mm (8mil) or wider |
| Minimum via drill | 0.3mm | 0.3mm |
| Minimum via annular ring | 0.13mm | 0.15mm |
| Minimum via pad diameter | 0.56mm (drill+2×ring) | 0.6mm |
| Board thickness | 0.4-2.4mm | 1.6mm (standard, cheapest) |
| Copper weight | 1oz (35µm) standard | 1oz for signal, 2oz for power |
| Min hole-to-hole | 0.5mm | 0.5mm |
| Min hole-to-edge | 0.3mm | 0.5mm |
| Min board dimension | 10×10mm | — |
| Max board dimension | 400×500mm | — |

### JLCPCB 4-layer standard capabilities

| Parameter | Minimum | Recommended |
|---|---|---|
| Minimum trace width | 0.09mm (3.5mil) | 0.15mm (6mil) |
| Minimum spacing | 0.09mm (3.5mil) | 0.15mm (6mil) |
| Standard stackup | 1.6mm total | Sig/GND/PWR/Sig |
| Inner layer copper | 0.5oz (17.5µm) | 0.5oz |
| Outer layer copper | 1oz (35µm) | 1oz |

### Generic/conservative rules (any fab)

When designing for unknown or high-reliability fabrication:

| Parameter | Conservative value |
|---|---|
| Minimum trace width | 0.25mm (10mil) |
| Minimum spacing | 0.25mm (10mil) |
| Minimum via drill | 0.4mm |
| Minimum annular ring | 0.2mm |
| Min via pad diameter | 0.8mm |

Explain to the user: tighter rules cost more and have higher defect rates.
Budget fabs can reliably hit 5mil, but 8mil traces with 8mil spacing is the
sweet spot for cost and yield.

## Trace Width Calculator

Use IPC-2152 methodology. The key variables:

- **I** = current in amps
- **ΔT** = allowable temperature rise in °C (typically 10-20°C)
- **t** = copper thickness in oz (1oz = 35µm = 1.378mil)
- **Layer** = external (better cooling) vs internal (worse cooling)

### Quick reference table (1oz copper, 10°C rise, external layer)

| Current (A) | Min width (mm) | Recommended width (mm) |
|---|---|---|
| 0.5 | 0.13 | 0.25 |
| 1.0 | 0.38 | 0.50 |
| 2.0 | 1.10 | 1.50 |
| 3.0 | 2.10 | 2.50 |
| 5.0 | 5.00 | 6.00 |
| 10.0 | 16.0 | 20.0 |

### Quick reference table (1oz copper, 10°C rise, internal layer)

Internal layers have worse thermal dissipation — traces must be wider:

| Current (A) | Min width (mm) | Recommended width (mm) |
|---|---|---|
| 0.5 | 0.25 | 0.40 |
| 1.0 | 0.76 | 1.00 |
| 2.0 | 2.20 | 2.80 |
| 3.0 | 4.20 | 5.00 |
| 5.0 | 10.0 | 12.0 |

### Calculation method

For precise calculation, use the IPC-2152 formula:

```
Area (mil²) = (I / (k × ΔT^b))^(1/c)
Width (mil) = Area / (thickness in mil)
```

Where for external layers: k=0.048, b=0.44, c=0.725
For internal layers: k=0.024, b=0.44, c=0.725

Always explain to the user what current flows through each trace so they
understand why the width was chosen.

## Via Sizing

### Standard via (through-hole)

| Application | Drill | Pad diameter | Current capacity |
|---|---|---|---|
| Signal via (general) | 0.3mm | 0.6mm | ~1A |
| Power via (moderate) | 0.4mm | 0.8mm | ~1.5A |
| Power via (high current) | 0.6mm | 1.0mm | ~3A |
| Thermal via | 0.3mm | 0.6mm | For heat transfer |

For high-current paths, use multiple vias in parallel. Example: a 3A power
rail transition between layers should use 3-4 standard 0.3mm vias, not one
large via.

### Thermal vias

Place under thermal pads (QFN, PowerPAD packages):

- Drill: 0.3mm
- Grid: 1.0-1.2mm pitch
- Fill: solid copper (not tented) for thermal transfer
- Connect to ground/thermal plane on opposite side
- Add solder mask between vias to prevent solder wicking during reflow

Explain to the user: thermal vias are the primary heat path for ICs with
exposed thermal pads. Without them the chip overheats even if the copper pour
on top looks adequate — heat needs a path through the board to the ground plane
and ultimately to the ambient air.

### Via-in-pad

JLCPCB supports via-in-pad with resin fill and cap plating, but at extra cost.
Default to dog-bone breakout (short trace from pad to nearby via) for budget
designs. Note when via-in-pad is genuinely necessary (BGA escape routing,
QFN thermal pads with no room for dog-bones).

## Clearance Rules

### Copper-to-copper clearance

| Voltage difference | Minimum clearance (IPC-2221B, internal) | Min clearance (external, conformal coated) |
|---|---|---|
| 0-15V | 0.1mm | 0.1mm |
| 16-30V | 0.1mm | 0.1mm |
| 31-50V | 0.6mm | 0.6mm |
| 51-100V | 0.6mm | 0.25mm |
| 101-150V | 1.5mm | 0.4mm |
| 151-300V | 3.2mm | 0.8mm |
| 301-500V | 6.4mm | 1.5mm |

For mains voltage (230V/120V AC), use creepage and clearance values from
IEC 60664-1 based on the pollution degree and overvoltage category. This is
critical for safety — always flag mains-voltage designs as requiring
professional review.

### Other clearances

| Rule | JLCPCB min | Recommended |
|---|---|---|
| Pad-to-pad | 0.127mm | 0.2mm |
| Pad-to-trace | 0.127mm | 0.2mm |
| Trace-to-board-edge | 0.3mm | 0.5mm |
| Copper-to-board-edge | 0.3mm | 0.5mm |
| Via-to-via | 0.5mm (centre) | 0.5mm |
| Component courtyard | — | 0.25mm (0402), 0.5mm (larger) |

## Impedance Control

### Common controlled-impedance targets

| Interface | Impedance | Type | Typical trace width (1.6mm FR4, outer) |
|---|---|---|---|
| USB 2.0 | 90Ω ±10% | Differential pair | ~0.2mm trace, ~0.15mm gap |
| USB 3.0 | 90Ω ±10% | Differential pair | ~0.2mm trace, ~0.15mm gap |
| Ethernet 100BASE-TX | 100Ω ±10% | Differential pair | ~0.15mm trace, ~0.2mm gap |
| SPI/I2C (>10MHz) | 50Ω ±10% | Single-ended | ~0.3mm |
| General CMOS | 50Ω ±10% | Single-ended | ~0.3mm |

Impedance depends on stackup (dielectric thickness, Er), copper weight, and
trace geometry. JLCPCB provides an impedance calculator — recommend the user
use it with their exact stackup for precision.

For 2-layer boards, controlled impedance is harder because the reference plane
is on the opposite side of the full board thickness. This limits designs to
lower-speed interfaces. Recommend 4-layer for anything requiring tight
impedance control.

### Differential pair routing rules

- Maintain constant spacing throughout the route
- Route both traces of a pair on the same layer
- Length-match within a pair to ±0.1mm for USB, ±0.5mm for general
- Keep pairs away from other signals (3× trace width clearance)
- Minimise via transitions; when unavoidable, transition both traces together

## Copper Pour Rules

### Ground pour strategy

- **2-layer boards**: fill unused areas on both layers with ground copper.
  Top layer will be broken up by signal traces; bottom layer should be as
  continuous as possible.
- **4-layer boards**: dedicate one inner layer to solid ground. This is the
  single most impactful thing for signal integrity and EMC.

### Pour parameters

| Parameter | Value | Why |
|---|---|---|
| Clearance to traces | 0.3mm | Prevents unintended coupling |
| Thermal relief spoke width | 0.5mm | Allows soldering without heat sink effect |
| Thermal relief gap | 0.5mm | Balance between thermal relief and ground connection |
| Minimum fill width | 0.2mm | Thinner copper slivers can peel or cause etching issues |
| Remove islands | Yes | Floating copper acts as an antenna — always remove |

Explain to the user: copper islands (disconnected fragments of pour) are worse
than no copper at all. They pick up noise and re-radiate it. KiCad's DRC can
flag these; always run a zone fill check before generating Gerbers.

## Silkscreen Rules

| Parameter | JLCPCB min | Recommended |
|---|---|---|
| Minimum text height | 0.8mm | 1.0mm |
| Minimum line width | 0.15mm | 0.2mm |
| Silk-to-pad clearance | 0.15mm | 0.2mm |
| Silk-to-board-edge | 0.3mm | 0.5mm |

Silkscreen text must not overlap exposed copper (pads, vias without mask).
KiCad DRC checks this. Include reference designators for all components,
polarity marks for diodes/electrolytic caps/ICs, and pin-1 indicators.

## Board Outline Rules

- Draw on the `Edge.Cuts` layer
- Use closed contours (no gaps)
- Minimum corner radius for routed boards: 1.0mm (JLCPCB)
- V-scored panels: straight lines only, no curves
- Internal cutouts: minimum 1.0mm width for routing bit

## Panelisation

For production quantities, boards are grouped into panels for efficient
handling. JLCPCB and PCBWay offer auto-panelisation, but custom panels give
more control.

| Parameter | Typical value |
|---|---|
| Panel border | 5mm (for tooling rails) |
| Tab width | 3-5mm |
| Mouse-bite drill | 0.6mm holes, 0.8mm pitch |
| V-score clearance | Components >1mm from V-score line |
| Tooling holes | 3× M3 (3.2mm) or alignment pins |

## Surface Finishes

| Finish | Cost | Shelf life | Lead-free | Notes |
|---|---|---|---|---|
| HASL (leaded) | Cheapest | Long | No | Uneven surface, fine for through-hole and large SMD |
| HASL (lead-free) | Low | Long | Yes | Same as above but compliant |
| ENIG | Medium | 12+ months | Yes | Flat pads, good for fine-pitch. Gold over nickel. |
| OSP | Low | 3-6 months | Yes | Flat but short shelf life. Re-solderable once. |
| Immersion silver | Medium | 6 months | Yes | Good flatness, tarnishes over time |
| Hard gold | High | Very long | Yes | For edge connectors, contact surfaces |

**Default recommendation**: ENIG for production (flat pads, good shelf life).
HASL lead-free for prototypes (cheapest). Note that JLCPCB's "economic PCBA"
option requires LeadFree HASL or ENIG.

## Solder Mask

| Parameter | JLCPCB min | Recommended |
|---|---|---|
| Solder mask expansion | 0.05mm | 0.05mm |
| Solder mask bridge (between pads) | 0.1mm | 0.15mm |
| Available colours | Green, black, white, blue, red, yellow, purple | Green (cheapest/fastest) |

Green solder mask has the best optical inspection properties and is cheapest
at every fab. Use green for prototypes; choose other colours for cosmetic
reasons on final products.

## Design Rule Summary Table

Quick-copy values for KiCad DRC setup:

### Budget fab (JLCPCB/PCBWay) — recommended values

```
Minimum clearance:           0.2mm
Minimum track width:         0.2mm
Minimum via diameter:        0.6mm
Minimum via drill:           0.3mm
Minimum annular ring:        0.15mm
Minimum hole-to-hole:        0.5mm
Copper to edge clearance:    0.5mm
Silk to pad clearance:       0.2mm
Minimum silk line width:     0.15mm
Minimum silk text height:    1.0mm
Solder mask expansion:       0.05mm
Solder mask bridge min:      0.15mm
```

### Conservative (any fab)

```
Minimum clearance:           0.25mm
Minimum track width:         0.25mm
Minimum via diameter:        0.8mm
Minimum via drill:           0.4mm
Minimum annular ring:        0.2mm
Minimum hole-to-hole:        0.5mm
Copper to edge clearance:    0.5mm
Silk to pad clearance:       0.25mm
Minimum silk line width:     0.2mm
Minimum silk text height:    1.0mm
Solder mask expansion:       0.05mm
Solder mask bridge min:      0.2mm
```
