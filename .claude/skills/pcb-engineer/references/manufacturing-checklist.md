# Manufacturing Checklist

Step-by-step checklist for preparing a KiCad design for PCB fabrication and
assembly. Walk the user through each step.

## Table of Contents

1. [Pre-Export Checks](#pre-export-checks)
2. [Gerber File Generation](#gerber-file-generation)
3. [Drill File Generation](#drill-file-generation)
4. [BOM for Assembly](#bom-for-assembly)
5. [Pick-and-Place File](#pick-and-place-file)
6. [Assembly Drawings](#assembly-drawings)
7. [Fabrication Notes](#fabrication-notes)
8. [Ordering from JLCPCB](#ordering-from-jlcpcb)
9. [Ordering from PCBWay](#ordering-from-pcbway)
10. [Pre-Order Review Checklist](#pre-order-review-checklist)

---

## Pre-Export Checks

Run these checks in KiCad before generating any output files:

### Schematic checks

- [ ] Run ERC (Electrical Rules Check) — resolve all errors; warnings may be
      acceptable if intentional (document why)
- [ ] Verify all components have footprints assigned
- [ ] Verify all components have MPN (manufacturer part number) fields
- [ ] Check net names are consistent and meaningful
- [ ] Power flags present on all power nets
- [ ] No unconnected pins that should be connected (ERC catches most of these)
- [ ] Decoupling caps present for every IC supply pin
- [ ] Pull-up/pull-down resistors on all open-drain/open-collector signals
- [ ] Reset circuits present where needed
- [ ] ESD protection on all external-facing signals

### PCB checks

- [ ] Run DRC (Design Rules Check) — resolve all errors
- [ ] All footprints placed and routed (no unrouted ratsnest lines)
- [ ] Board outline closed on Edge.Cuts layer
- [ ] Mounting holes placed per mechanical requirements
- [ ] Copper pours filled and up to date (Edit → Fill All Zones)
- [ ] No orphaned copper islands (DRC reports these)
- [ ] Silkscreen legible and not overlapping pads
- [ ] Polarity marks on all polarised components (diodes, electrolytic caps, ICs pin 1)
- [ ] Component reference designators visible and sensibly positioned
- [ ] Test points accessible for probe contact
- [ ] Fiducial marks placed (at least 3, asymmetric arrangement) if using
      pick-and-place assembly
- [ ] Board dimensions match mechanical requirements
- [ ] Courtyard violations resolved (no overlapping components)

### Visual inspection

- [ ] 3D viewer check (View → 3D Viewer): verify component heights, check for
      mechanical interference, confirm connectors are on the correct side of the board
- [ ] Layer-by-layer review: F.Cu, B.Cu, F.SilkS, B.SilkS, Edge.Cuts
- [ ] Check that high-current traces are appropriately wide
- [ ] Check that differential pairs maintain consistent spacing
- [ ] Verify thermal vias under thermal pads

## Gerber File Generation

In KiCad: File → Fabrication Outputs → Gerbers (.gbr)

### Required layers

| Layer | KiCad name | Gerber suffix | Purpose |
| --- | --- | --- | --- |
| Front copper | F.Cu | .gtl or F_Cu.gbr | Top copper traces |
| Back copper | B.Cu | .gbl or B_Cu.gbr | Bottom copper traces |
| Front solder mask | F.Mask | .gts or F_Mask.gbr | Top solder mask openings |
| Back solder mask | B.Mask | .gbs or B_Mask.gbr | Bottom solder mask openings |
| Front silkscreen | F.SilkS | .gto or F_Silkscreen.gbr | Top text and markings |
| Back silkscreen | B.SilkS | .gbo or B_Silkscreen.gbr | Bottom text and markings |
| Front paste | F.Paste | .gtp or F_Paste.gbr | Solder paste stencil (for assembly) |
| Back paste | B.Paste | .gbp or B_Paste.gbr | Solder paste stencil |
| Board outline | Edge.Cuts | .gm1 or Edge_Cuts.gbr | Board shape |

For 4-layer boards, also include:
| In1.Cu | Inner layer 1 | .g2 or In1_Cu.gbr |
| In2.Cu | Inner layer 2 | .g3 or In2_Cu.gbr |

### Gerber settings in KiCad

- Format: Gerber X2 (preferred) or RS-274X (legacy, wider compatibility)
- Coordinate format: 4.6 (4 integer, 6 decimal places)
- Coordinate origin: Drill/place file origin (set this in KiCad first)
- Check "Subtract soldermask from silkscreen" to avoid silk on exposed pads
- Check "Use Protel filename extensions" if the fab requires it (JLCPCB accepts
  both naming conventions)

### Output

Generate all Gerbers into a single folder, then zip the folder. The zip file
is what you upload to the fab.

## Drill File Generation

In KiCad: File → Fabrication Outputs → Drill Files (.drl)

### Settings

- Format: Excellon
- Drill units: millimetres
- Zero format: Decimal format
- Drill origin: same as Gerber origin (Drill/place file origin)
- Generate a single drill file for through-hole vias; separate files for blind/
  buried vias if applicable
- Check "PTH and NPTH in single file" (some fabs prefer separate — JLCPCB
  accepts both)

### Drill map (optional)

Generate a drill map (.pdf or .ps) for visual verification of hole positions
and sizes. Not uploaded to the fab, but useful for review.

## BOM for Assembly

If using JLCPCB's SMT assembly service, the BOM must be in their specific CSV
format:

```csv
Comment,Designator,Footprint,LCSC Part #
10uF,C1,0805,C15850
100nF,C2 C3 C4,0402,C1525
10k,R1 R2,0402,C25744
AP2112K-3.3,U1,SOT-23-5,C51118
```

Columns:

- **Comment**: component value or part name
- **Designator**: reference designator(s), space-separated if grouped
- **Footprint**: package name
- **LCSC Part #**: the LCSC catalogue number (starts with C followed by digits)

To find LCSC part numbers: search on lcsc.com by MPN or description. JLCPCB
maintains a "basic parts" library (cheaper assembly fee) and an "extended parts"
library (small surcharge per unique part). Prefer basic parts where possible.

### PCBWay BOM format

PCBWay accepts a more flexible format but recommends:

```csv
Designator,MPN,Manufacturer,Quantity,Description,Package
C1,CL21A106KAYNNNE,Samsung,1,10uF 25V X5R,0805
R1 R2,RC0402FR-0710KL,Yageo,2,10k 1%,0402
```

## Pick-and-Place File

Also called "centroid file" or "CPL" (Component Placement List).

In KiCad: File → Fabrication Outputs → Component Placement (.pos)

### Settings (Pick-and-Place File)

- Format: CSV
- Units: millimetres
- Coordinate origin: same as Gerber/drill origin
- Include footprint position reference point (usually pad 1 or centre)

### JLCPCB CPL format

JLCPCB expects these exact column headers:

```csv
Designator,Val,Package,Mid X,Mid Y,Rotation,Layer
C1,10uF,0805,25.4,15.2,0,top
R1,10k,0402,30.1,20.3,90,top
U1,AP2112K-3.3,SOT-23-5,35.0,12.5,270,top
```

KiCad's position file output may need column renaming. Common adjustments:

- "Ref" → "Designator"
- "PosX" → "Mid X"
- "PosY" → "Mid Y"
- "Rot" → "Rotation"
- "Side" → "Layer" (map "top"/"bottom" to "top"/"bottom")

### Rotation corrections

JLCPCB's component rotation may differ from KiCad's by 0°, 90°, 180°, or 270°.
JLCPCB provides rotation correction data, or the user can adjust during order
review. Common corrections:

- SOT-23 family: often needs +180°
- QFN packages: often needs +90° or -90°
- 0402/0603 passives: usually correct

The JLCPCB order review shows a 3D preview — always verify component rotations
visually before confirming.

## Assembly Drawings

Generate a PDF showing:

- Component outlines on both sides of the board
- Reference designators clearly labelled
- Polarity markings for diodes, electrolytic caps, pin 1 of ICs
- Board outline and mounting holes
- Any special assembly instructions (hand-solder components, conformal coating
  areas, potting areas)

In KiCad: File → Plot → select F.Fab, B.Fab, F.SilkS, B.SilkS, Edge.Cuts
layers → output PDF.

Alternatively, export from the 3D viewer for a visual reference.

## Fabrication Notes

Include a text file or drawing with:

- Board dimensions (overall and any critical dimensions)
- Number of layers
- Board thickness (typically 1.6mm)
- Copper weight: outer layers and inner layers
- Surface finish (ENIG, HASL lead-free, etc.)
- Solder mask colour
- Silkscreen colour
- Material (FR4 standard, or specify TG value for high-temp applications:
  TG 130 standard, TG 155/170 for lead-free reflow or high-temp environments)
- Impedance control requirements (if any): target impedance, layer, trace
  width, reference layer
- Minimum trace/space (if tighter than standard capabilities)
- Via type (through-hole only, or blind/buried)
- Panelisation requirements (if custom panel, include panel drawing)
- IPC class: Class 2 (standard) or Class 3 (high reliability)
- UL marking requirements (if applicable)

## Ordering from JLCPCB

### PCB-only order

1. Go to jlcpcb.com → "Order Now"
2. Upload Gerber zip file
3. Review auto-detected parameters (layers, dimensions, drill count)
4. Set options:
   - Quantity (5 minimum for standard)
   - Layers: 2 or 4
   - Thickness: 1.6mm (standard, cheapest)
   - Colour: green (cheapest and fastest, others add $1-2 and 1-2 days)
   - Surface finish: HASL lead-free (default) or ENIG (for fine-pitch)
   - Copper weight: 1oz (default)
   - Remove order number: "Specify a location" (add JLCJLCJLCJLC text on
     silkscreen where you want it, or "Yes" to have them remove it for a fee)
5. Review the Gerber viewer — check all layers visually
6. Add to cart → checkout

### PCB + Assembly order (PCBA)

1. Follow PCB-only steps above
2. Enable "SMT Assembly" toggle
   - Side: Top (most common) or Top+Bottom
   - Tooling holes: "Added by JLCPCB" (they add 3 holes at board edges)
   - Confirm: check pad count against your design
3. Upload BOM (CSV in their format — see BOM section above)
4. Upload CPL (pick-and-place file — see CPL section above)
5. Component matching:
   - JLCPCB matches your BOM entries to their LCSC inventory
   - Review matches — red items mean no match found; search LCSC manually
   - Verify orientation of each component in the 3D preview
   - Pay special attention to IC pin 1 orientation and diode polarity
6. Confirm component placement and quantities
7. Review total cost (PCB + assembly fee + component costs)
8. Place order

### JLCPCB pricing notes

- PCB only (5 pcs, 2-layer, green, 100×100mm): typically $2-5
- Assembly setup fee: $8 per unique design (one-time)
- Basic parts: $0.0015 per joint
- Extended parts: $0.0015 per joint + $3 per unique extended part
- Economy PCBA: cheaper but slower; standard PCBA is 3-5 working days

## Ordering from PCBWay

### PCB-only order (Ordering from PCBWay)

1. Go to pcbway.com → "Quote Now"
2. Enter board dimensions, layers, quantity, etc. manually OR upload Gerbers
   for auto-detection
3. Select options (similar to JLCPCB)
4. Upload Gerber zip
5. PCBWay reviews the design (may take a few hours) and contacts you if there
   are issues
6. Confirm and pay

### PCBWay Assembly

1. Select "Assembly" when quoting
2. Upload Gerbers, BOM, and pick-and-place file
3. PCBWay's engineering team reviews and may ask questions
4. They source components (from their stock or order from distributors)
5. Turnaround is typically longer than JLCPCB for assembly

## Pre-Order Review Checklist

Final checks before submitting the order:

- [ ] Gerber viewer at the fab matches your design (check every layer)
- [ ] Board dimensions in the fab's system match your design
- [ ] Drill count matches your design
- [ ] Surface finish selected correctly
- [ ] Solder mask colour correct
- [ ] Copper weight correct
- [ ] If assembly: all components matched to LCSC/supplier parts
- [ ] If assembly: component rotations verified in 3D preview
- [ ] If assembly: BOM quantities match schematic
- [ ] Shipping method selected (DHL/FedEx for speed, standard post for cost)
- [ ] Delivery address correct
- [ ] Order total reviewed and approved

### Common mistakes to catch

- Forgetting to fill copper zones before exporting Gerbers (the Gerber will
  have empty zones)
- Drill/place origin not set, causing offset between Gerber and drill files
- Silkscreen text overlapping pads (causes rejection at some fabs)
- Board outline not closed (causes rejection)
- Missing paste layer in Gerber export (needed for stencil generation)
- Wrong component rotation in pick-and-place file
- BOM references not matching schematic (e.g., after renumbering components)
