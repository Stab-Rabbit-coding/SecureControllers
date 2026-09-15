# Electronics / PCB Standards

Layer this over the language template for projects with electronic hardware. Repository policy
overrides anything here.

## Every edit gets an ERC and a DRC

After **every** schematic or layout change, run electrical rule check and design rule check.
Resolve the violations, or document each one you're accepting with the rule and the reason.

An undocumented accepted violation is indistinguishable from an unnoticed one at review time,
which means the whole clean report stops meaning anything.

## Definition of production-ready

A board is ready to fabricate when it has, together and consistent with each other:

- A complete schematic with every net named and no unconnected pins left unmarked
- A layout matching that schematic — verify against the netlist, not by eye
- Copper: routed traces sized for their current and impedance, and the intended plane structure
- Correct footprints for the **exact** ordered part — package, pitch, pin 1, and thermal pad
- Generated fabrication and assembly outputs, checked in a viewer before release

A footprint that matches the part family but not the specific package is the single most
expensive error in this list, because it is only discovered at assembly.

## Component selection

Record the exact manufacturer part number, package, tolerance, voltage and temperature rating,
and the datasheet reference for anything whose behavior matters. Note availability and at least
one alternate for parts on the critical path.

Verify pin functions against the datasheet rather than against a symbol — library symbols carry
errors, and a symbol error becomes a board error silently. Where a part family varies by suffix,
confirm the specific variant has the feature you're relying on; sub-family capability
differences are a recurring source of late respins.

## Power

Quote the power budget per rail: nominal and worst-case current, headroom, and thermal
dissipation. State the sequencing requirement if there is one. Give every switching supply its
required passives from the datasheet, not from a similar design.

## Signal integrity, EMI, and isolation

State the requirements before layout, since they constrain placement:

- Controlled-impedance nets and the stackup that achieves them
- Differential pairs, with length matching and skew tolerance
- Return-path continuity — a plane split under a fast signal is a defect
- Decoupling per device, placed against the pin
- Isolation barriers, with the rated voltage and the creepage/clearance that supports it
- Where an EMI performance target exists, state it and how the layout addresses it

## Layout placement authority

Where the project's policy places final footprint positioning with the user, respect it. If a
rule violation can only be fixed by moving a placed footprint, refer it to the user with the
specific conflict rather than moving it. Other violations may be fixed directly.

## Comments and file hygiene

For formats without comment syntax, keep the design notes in an accompanying Markdown file. Where
a format has a native comment form, use that form only — injecting a foreign comment character
into a structured file can corrupt it in ways that are not obvious until the tool refuses to open
it.

## Security-relevant hardware

Where the design includes a secure element, TPM, or cryptographic accelerator, state precisely
what it provides and what it does not. These parts differ significantly within a family, and
assuming a capability that a specific variant lacks is discovered at bring-up. Record the
protected-operation timing budget so it isn't placed in a latency-critical path.

## Task checklist

Before marking a PCB task complete:

- [ ] ERC run; violations resolved or documented with rule and reason
- [ ] DRC run; violations resolved or documented with rule and reason
- [ ] Layout verified against the netlist
- [ ] Footprints confirmed against datasheets for the exact ordered parts
- [ ] Power budget per rail quoted, with headroom and thermal figures
- [ ] Impedance, pairs, and return paths verified
- [ ] Decoupling placed per device
- [ ] Isolation barriers meet rated creepage and clearance
- [ ] Fabrication outputs generated and inspected in a viewer
- [ ] Part numbers, alternates, and datasheet references recorded
- [ ] Board mass and power recorded in the task's impact output
