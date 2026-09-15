---
name: autoroute
description: >-
  Auto-route a KiCad PCB using FreeRouting — connects all ratsnest traces
  automatically, then reports track count, via count, and any remaining
  unrouted connections. Backs up the original PCB before modifying it.
  Use whenever the user says "auto-route", "route the board", "route the PCB",
  "connect the traces", "finish routing", or wants to route all connections
  on a KiCad .kicad_pcb file.
---

# KiCad Auto-Router Skill

Auto-routes a KiCad `.kicad_pcb` file using FreeRouting (open-source Specctra-based router), then imports the result back into the PCB file.

## How it works

1. Backs up the original `.kicad_pcb`
2. Clears any existing tracks (starts clean)
3. Exports a Specctra `.dsn` file via KiCad's Python API (`pcbnew`)
4. Runs FreeRouting headlessly (up to 100 passes, 4 threads)
5. Imports the `.ses` result back into the PCB
6. Reports: track segments, vias, unrouted connections

## Usage

```bash
python3 ~/.claude/skills/autoroute/autoroute.py path/to/board.kicad_pcb
```

Optional flags:

- `--output path/to/output.kicad_pcb` — write to a different file (default: overwrites input)
- `--passes N` — max routing passes (default: 100)

## When invoked as a skill

Run the script on the current project's `.kicad_pcb` file and report results. The PCB file is auto-detected from the working directory or the user's project path.

## Requirements

- Java 18+ (`java` in PATH) — already installed at `/usr/bin/java`
- KiCad 10 at `/Applications/KiCad/KiCad.app` — provides `pcbnew` Python API
- `freerouting.jar` — bundled at `/Users/prithvigupta/.claude/skills/autoroute/freerouting.jar`

## Notes

- 78–100% routing completion is typical depending on component placement
- Remaining unrouted connections require manual routing or component repositioning in KiCad
- Backup saved as `<board>.kicad_pcb.pre-autoroute.bak`
