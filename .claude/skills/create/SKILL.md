---
name: create
description: >-
  Generate KiCad 10 schematics and PCB layouts from natural language prompts.
  Writes production-ready .kicad_sch and .kicad_pcb files directly to disk.
  Uses an agentic search loop to verify every component against the installed
  KiCad symbol libraries before placing it — no unknown '?' symbols ever.
  Supports full circuits: MCUs, power supplies, connectors, passives, ICs.
  Use whenever the user says "create a schematic", "design a circuit",
  "generate a PCB", "make a KiCad file", "design a board", "draw a schematic",
  or describes a circuit they want built. Also for "Arduino shield", "ESP32
  board", "motor driver", "power supply", "sensor breakout", "LED driver",
  or any request to produce a new KiCad design from scratch.
---

# KiCad Design Creation Skill

Generates production-ready KiCad 10 schematics (`.kicad_sch`) and PCB layouts
(`.kicad_pcb`) from a plain-English circuit description. Every symbol is
verified against the installed KiCad libraries before placement — the output
will never contain unknown `?` symbols.

## Related Skills

| Skill | Purpose |
|-------|---------|
| `kicad` | Analyze and review the generated design |
| `emc` | EMC pre-compliance check after generation |
| `spice` | Simulate subcircuits in the generated schematic |
| `bom` | Extract and enrich the BOM from the generated design |
| `jlcpcb` | Order PCBs from the generated Gerbers |
| `pcbway` | Alternative PCB fabrication |

## Requirements

- **Python 3.10+** — uses `anthropic` package  
- **Anthropic API key** — set `ANTHROPIC_API_KEY` environment variable  
  Get one at https://console.anthropic.com/settings/keys  
- **KiCad 10 installed** at `/Applications/KiCad/KiCad.app` (macOS) or  
  `/usr/share/kicad` (Linux) for the symbol library scan  

Install the Python dependency:

```bash
pip install anthropic
```

## Workflow

### Step 1 — Generate a schematic

```bash
python3 <skill-path>/scripts/generate_schematic.py \
  --prompt "Arduino Uno shield with 4 MOSFETs, flyback diodes, and a 5V regulator" \
  --output ~/Documents/KiCad/MyProject/MyProject.kicad_sch
```

The script:

1. Scans all installed KiCad symbol libraries and builds a searchable index
2. Calls Claude with the circuit description
3. Claude searches the index for every component, then calls `create_schematic`
4. Symbols and wires are written to the `.kicad_sch` file with full `lib_symbols`
   definitions embedded — KiCad opens it with no missing symbols

### Step 2 — Generate a PCB layout (optional)

```bash
python3 <skill-path>/scripts/generate_pcb.py \
  --schematic ~/Documents/KiCad/MyProject/MyProject.kicad_sch \
  --output ~/Documents/KiCad/MyProject/MyProject.kicad_pcb \
  --board-size "50x50" \
  --prompt "Two-layer board, group power components top-left, connectors on edges"
```

The script places footprints from the schematic netlist onto the PCB with
Claude-suggested coordinates.

## Usage in conversation

When the user describes a circuit to build, run `generate_schematic.py` and
report the result. Offer to run `generate_pcb.py` afterwards.

**Example triggers:**

- "Design me an Arduino motor driver shield"
- "Create a KiCad schematic for a 3.3 V buck converter"
- "Generate a schematic for an ESP32 with USB-C power and LiPo charging"
- "Make a KiCad PCB for a 4-channel relay board"

## Output format

`generate_schematic.py` prints a JSON summary to stdout:

```json
{
  "status": "ok",
  "output": "/path/to/file.kicad_sch",
  "placed": 18,
  "wires": 34,
  "corrections": ["Auto-corrected 'Device:CP' → 'Device:C_Polarized'"],
  "skipped": [],
  "search_rounds": 7
}
```

`generate_pcb.py` prints:

```json
{
  "status": "ok",
  "output": "/path/to/file.kicad_pcb",
  "placed": 18,
  "board_size_mm": [50, 50]
}
```

## Limitations

- Schematic wiring is logical (net labels) rather than drawn wire routing for
  complex multi-IC designs. Open the file in KiCad's Schematic Editor to tidy
  wire routing visually.
- PCB layout places components with correct relative grouping but does not run
  the KiCad auto-router. Use KiCad's built-in router or FreeRouting after.
- Footprint assignment is best-effort; review and assign exact footprints in
  KiCad before ordering PCBs.
