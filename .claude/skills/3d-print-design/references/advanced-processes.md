# Advanced 3D Printing Processes

Design rules for professional and industrial processes beyond desktop FDM and
resin. These are typically accessed through service bureaus (JLCPCB 3D, JLC3DP,
Shapeways, Craftcloud, Xometry, Protolabs) rather than owned machines.

## Table of Contents

1. [Process Selection Guide](#process-selection-guide)
2. [SLS — Selective Laser Sintering](#sls)
3. [MJF — Multi Jet Fusion](#mjf)
4. [DMLS / SLM — Metal Printing](#metal-printing)
5. [Metal Binder Jetting](#metal-binder-jetting)
6. [Metal Extrusion (FFF/BMD)](#metal-extrusion)
7. [Service Bureau Selection](#service-bureaus)

---

## Process Selection Guide

| Need | Best process | Why |
| --- | --- | --- |
| Tough nylon parts, no supports | SLS | Support-free, isotropic nylon |
| Short-run production (50-500 units) | SLS or MJF | Cost-effective at volume, consistent |
| Metal prototype (1-10 units) | DMLS/SLM | Full-density metal, any geometry |
| Metal production (100+ units) | Metal binder jetting | Faster, cheaper per part than DMLS |
| Stainless steel enclosure/bracket | Metal binder jetting or DMLS | Depends on tolerance needs |
| Titanium / Inconel (aerospace) | DMLS/SLM | Full melting for max density |
| Lightweight lattice structures | DMLS/SLM | Impossible with subtractive methods |
| Very fine detail, smooth surface | SLA/MSLA resin | See resin-printing.md |
| Cheap prototype, any geometry | FDM | See fdm-design-rules.md |

## SLS

### What it is

Selective Laser Sintering uses a laser to fuse polymer powder (typically
nylon PA12 or PA11) layer by layer. The unsintered powder surrounding the
part acts as its own support structure, so SLS parts need no supports at all.
This enables complex geometries impossible with FDM or resin.

### When to use SLS

- Functional nylon parts with complex geometry
- Interlocking or moving assemblies printed in one piece
- Parts that need near-isotropic mechanical properties
- Short production runs where injection moulding tooling is not justified
- Parts with internal channels or lattice structures

### Materials

| Material | Properties | Use for |
| --- | --- | --- |
| PA12 (Nylon 12) | Strong, slightly flexible, chemical-resistant | General functional parts, housings, brackets |
| PA11 (Nylon 11) | More ductile than PA12, better fatigue life, bio-based (castor oil) | Snap fits, living hinges, repeated-stress parts |
| PA12 GF (glass-filled) | Higher stiffness, better dimensional stability | Stiff structural parts, housings needing rigidity |
| PA12 CF (carbon-filled) | Highest stiffness, lightweight | Drone frames, high-stiffness brackets |
| TPU (SLS grade) | Flexible, fatigue-resistant | Gaskets, seals, flexible joints |
| PP (Polypropylene) | Chemical-resistant, low density | Chemical containers, lightweight parts |

### Design rules

| Parameter | Minimum | Recommended | Notes |
| --- | --- | --- | --- |
| Wall thickness (PA12) | 0.7mm | 1.0mm | 2.0mm for GF-filled |
| Wall thickness (PA12 GF) | 1.5mm | 2.0-2.5mm | Glass fibre makes it stiffer but more brittle |
| Feature size | 0.5mm | 0.8mm | Text, thin ribs |
| Clearance (moving parts) | 0.5mm | 0.6mm | Between interlocking printed parts |
| Clearance (assembly) | 0.3mm | 0.5mm | Between separate printed parts |
| Press fit offset | 0.1mm | 0.15mm | Interference per side |
| Hole diameter (min) | 1.0mm | 1.5mm | Powder removal limits smaller holes |
| Internal channel (min) | 2.0mm | 3.0mm | Must allow powder evacuation |
| Escape holes for hollow parts | 2.0mm dia | 3.5mm dia | At least 2, at lowest points |

### Tolerances

| Dimension range | Tolerance |
| --- | --- |
| General | ±0.3mm or ±0.3%, whichever is greater |
| Across build volume | ±0.5mm + 0.1% of dimension |
| Holes and internal features | -0.1 to -0.2mm (undersized due to powder sintering at edges) |

### Shrinkage

PA12 shrinks ~2-3% during cooling. SLS machines apply compensation
automatically, but residual anisotropic shrinkage (XY vs Z) of ~0.3% may
remain. Large flat parts are most affected — add ribs or curvature to
resist warping.

### Key advantages over FDM

- No supports: complex geometry prints freely
- Near-isotropic: ~10-15% Z-axis strength reduction vs ~40-60% for FDM
- Consistent surface texture (slightly granular, uniform)
- Nesting: many parts packed into one build reduces per-part cost

### Post-processing

- **Depowdering**: compressed air and brushes to remove unsintered powder
- **Bead blasting**: media blasting for uniform matte surface (removes ~0.1-0.2mm)
- **Dyeing**: SLS parts are naturally white/grey; dye in black or colours
  (parts absorb dye ~0.5mm deep)
- **Vapour smoothing**: chemical smoothing for glossy, sealed surface
- **Machining**: CNC-mill critical surfaces for tight tolerances

### Cost

SLS parts cost ~$15-50 for typical hand-sized parts through service bureaus.
Price is driven by bounding-box volume (the space the part occupies in the
build chamber), not just material volume. Hollowing and nesting help.

## MJF

### What it is (MJF)

HP Multi Jet Fusion. Similar concept to SLS (powder bed, no supports) but
uses an inkjet head to deposit fusing and detailing agents onto nylon powder,
then an infrared lamp fuses the layer. Produces parts with properties
comparable to SLS but faster and with finer detail on downward-facing surfaces.

### When to use MJF

- Same applications as SLS but with slightly better surface finish
- Short production runs where dimensional consistency matters
- Parts needing fine text or small features (detailing agent improves edges)

### Materials (MJF)

Primarily PA12 and PA11 (HP branded). Also TPU (HP branded flexible).
Glass-bead-filled PA12 available for higher stiffness.

### Design rules (MJF)

Very similar to SLS. Key differences:

- Minimum wall: 0.5mm (MJF can resolve thinner features than SLS)
- Minimum feature: 0.5mm
- Tolerances: ±0.3mm or ±0.3%, whichever is greater (same as SLS)
- Parts are naturally grey/dark. Dyeing is common.

## Metal Printing

### DMLS and SLM

DMLS (Direct Metal Laser Sintering) and SLM (Selective Laser Melting) are the
dominant metal 3D printing processes. Both use a laser to fuse metal powder
layer by layer. SLM fully melts the powder (higher density, >99.5%); DMLS
sinters it (slightly lower density but often sufficient). The terms are
frequently used interchangeably.

### When to use metal printing

- Complex metal geometry impossible to machine (internal channels, lattices,
  topology-optimised shapes)
- Prototyping metal parts before committing to casting or machining tooling
- Low-volume production of high-value metal components
- Lightweight structures (lattice infill reduces weight while maintaining
  strength)
- Consolidated assemblies (combining multiple machined parts into one printed
  part)

### Materials (Metal Printing)

| Material | Typical alloy | Use for |
| --- | --- | --- |
| Stainless steel | 316L, 17-4 PH | General purpose, corrosion-resistant |
| Aluminium | AlSi10Mg | Lightweight, good thermal conductivity |
| Titanium | Ti6Al4V (Grade 5) | Aerospace, medical, high strength-to-weight |
| Inconel | 718, 625 | High-temperature, corrosion-resistant |
| Cobalt-chrome | CoCr | Medical implants, dental, high wear |
| Tool steel | H13, Maraging | Moulds, tooling, dies |
| Copper alloys | CuSn10, pure Cu | Thermal management, electrical |

### Design rules (Metal Printing)

| Parameter | Minimum | Recommended | Notes |
| --- | --- | --- | --- |
| Wall thickness | 0.5mm | 0.8-1.0mm (2.0mm for load-bearing) | Thin walls risk warping or incomplete fusion |
| Minimum feature size | 0.3mm | 0.5mm | Depends on material and orientation |
| Overhangs | 45° from vertical | <40° for self-supporting | Steeper overhangs need support |
| Clearance between features | 0.4mm | 0.5mm | Prevents powder fusion between features |
| Hole diameter (min) | 0.5mm | 1.0mm | Smaller holes may seal with sintered powder |
| Internal channel (min) | 1.0mm | 2.0mm | Powder removal required |
| Thread size (min printable) | M6 | M8+ | Finer threads should be tapped post-print |

### Tolerances (Metal Printing)

| Specification | Value |
| --- | --- |
| General tolerance | ±0.3mm or ±0.3%, whichever is greater |
| As-printed surface finish | Ra 5-20 µm (material-dependent) |
| After machining | Ra 0.8-3.2 µm |
| Achievable tolerance after CNC | ±0.05-0.1mm |

### Critical design considerations

**Supports are always required** — unlike polymer SLS, metal printing needs
supports to anchor parts to the build plate and dissipate heat. Support
removal is manual or by CNC and leaves surface marks. Design to minimise
support contact on critical surfaces.

**Thermal stress** — metal parts experience significant thermal gradients
during printing. Large solid cross-sections, sharp internal corners, and
rapid thickness changes all concentrate stress and cause warping or cracking.
Use fillets (R ≥ 0.5mm), uniform wall thickness, and gradual transitions.

**Build orientation** — determines support placement, surface finish, and
residual stress distribution. The service bureau typically optimises this,
but flag critical surfaces and toleranced features.

**Post-processing is mandatory**:

1. Stress-relief heat treatment (usually before removing from build plate)
2. Support removal (manual, wire EDM, or CNC)
3. Build plate removal (wire EDM or bandsaw)
4. Optional: HIP (Hot Isostatic Pressing) for maximum density
5. Optional: CNC machining of critical surfaces/interfaces
6. Optional: surface finishing (bead blasting, polishing, electropolishing)

### Cost (Metal Printing)

Metal 3D printing is expensive. Typical pricing:

- Small parts (fits in palm): $50-200
- Medium parts (fist-sized): $200-1000
- Material cost: $100-300/kg for powder (titanium at the high end)
- Post-processing adds 20-50% to base printing cost

Use metal printing when geometry demands it. For simple shapes, CNC machining
is almost always cheaper.

## Metal Binder Jetting

### What it is (Metal Binder Jetting)

An inkjet head deposits binder onto metal powder layer by layer, creating a
"green" part. The green part is then cured, depowdered, and sintered in a
furnace to burn out the binder and fuse the metal particles. The result is a
fully metal part at ~97-99% density.

### When to use

- Medium production volumes (50-500+ parts) in stainless steel
- Cost-sensitive metal parts where DMLS/SLM is too expensive
- Parts that do not need the full density or mechanical properties of SLM
- Complex geometry that would be expensive to machine

### Materials (Metal Binder Jetting)

Primarily stainless steel 316L and 17-4 PH. Some services offer bronze
infiltration for improved density. Expanding to tool steels and other alloys.

### Design rules (Metal Binder Jetting)

Similar to DMLS/SLM with additional considerations:

- **Shrinkage**: parts shrink ~15-20% during sintering. The service bureau
  compensates, but feature-to-feature accuracy is lower than DMLS.
- **Wall thickness minimum**: 1.0mm (green parts are fragile before sintering)
- **Tolerances**: ±0.5mm or ±0.5%, whichever is greater (less precise than
  DMLS/SLM)
- **Internal features**: must allow depowdering; minimum channel diameter 3mm
- **No supports needed** during printing (powder bed is self-supporting, like
  polymer SLS)

### Cost (Metal Binder Jetting)

Significantly cheaper than DMLS/SLM for volume production. Per-part cost
drops substantially above 50 units. Typical: $20-100 for small stainless
steel parts.

## Metal Extrusion

### What it is (Metal Extrusion)

Metal filament or rods (metal powder bound in a polymer matrix) are extruded
like FDM to create a "green" part. The part is then debinded (polymer removed)
and sintered in a furnace to produce a solid metal part. Desktop Metal, Markforged,
and BASF (Ultrafuse) offer this technology.

### When to use (Metal Extrusion)

- Office-safe metal prototyping (no loose powder)
- Simple metal geometries where DMLS complexity is not needed
- Small metal parts at lower cost than DMLS/SLM

### Materials (Metal Extrusion)

Stainless steel 316L, 17-4 PH, tool steel H13, copper. Limited selection
compared to DMLS/SLM.

### Design rules (Metal Extrusion)

- Wall thickness: ≥ 2.0mm (green parts are very fragile)
- Shrinkage: ~16-20% during sintering (compensated by slicer)
- Tolerances: ±0.5mm typical
- No internal channels smaller than 5mm (debinding requires access)
- Simple geometry recommended; complex overhangs are difficult

### Limitations

Lower accuracy and density than DMLS/SLM. Limited material selection.
Sintering furnace is an additional capital expense. Best suited for simple
metal parts where the alternative is machining from bar stock.

## Service Bureaus

Since SLS and metal printing require expensive industrial equipment, most
users access these through service bureaus.

### Recommended services

| Service | Processes | Strengths | Notes |
| --- | --- | --- | --- |
| JLC3DP / JLCPCB 3D | SLS, SLA, MJF, SLM | Budget-friendly, fast, integrates with JLCPCB PCB orders | Good for electronics project enclosures |
| Xometry | All processes | Instant quoting, wide material selection | US/EU based |
| Protolabs (Hubs) | All processes | Professional, design feedback | Higher price, higher quality |
| Shapeways | SLS, MJF, metals | Consumer-friendly, marketplace | Good for small quantities |
| Craftcloud | Aggregator | Compares prices across services | Useful for finding cheapest option |
| Sculpteo | SLS, SLA, metals | EU-based, good material range | Professional service |
| i.materialise | All processes | Materialise's consumer arm | Wide material range including ceramics |

### Ordering workflow

1. Export your design as STL or 3MF (STEP also accepted by most services)
2. Upload to the service bureau's website
3. Select material and process
4. Review auto-generated quote (based on bounding box, volume, material)
5. Service bureau prints, post-processes, and ships
6. Typical lead time: 3-7 working days for SLS, 5-15 for metals

### Design tips for service bureau orders

- **Mesh quality**: export STL at high resolution (deviation <0.01mm). Low-res
  meshes produce faceted prints.
- **Units**: confirm the service expects millimetres. Inch/mm mixups are the
  most common order error.
- **Consolidate parts**: SLS pricing is by bounding box — nesting multiple
  small parts into one order reduces cost.
- **Specify critical dimensions**: if any features need tight tolerances, note
  them. Default is "best effort" at standard process tolerances.
- **Orientation requests**: if a specific surface must be smooth or a dimension
  must be accurate, note which surface and why.
