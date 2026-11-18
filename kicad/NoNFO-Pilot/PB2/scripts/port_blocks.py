# SPDX-License-Identifier: CERN-OHL-W-2.0
"""Port the Pilot and TACCO schematic blocks into NoNFO-Pilot-PB2 (S36).

Run once beside a Serenity-UAV checkout; it writes ``sch/ported_blocks.json``, which
``gen_nonfo_pb2_sch.py`` reads, so this repository's CI does not need Serenity-UAV.

Sources (Serenity-UAV, CC BY 4.0, pin tables transcribed from OEM data sheets there):
  * ``avionics/kicad/Pilot/scripts/gen_pilot_sch.py`` at HEAD: buses, Ethernet, sensors,
    TPM, 1553, +3V3, power entry, PWM and expansion port.
  * ``avionics/kicad/TACCO/scripts/gen_tacco_sch.py`` at HEAD: mLRS radio, BT/802.15.4
    module, NOR flash, write-block PLD, fan, microSD, RF rails, antenna feeds.
  * ``gen_pilot_sch.py`` at commit 3f55d58^ (the last revision with the cape GNSS): the
    MAX-M10S block, restored by owner decision 2026-11-12.

Each ported part keeps its pins, nets and data-sheet note and gains an ``origin`` field.
Net renames and the B+ re-pointing happen in ``gen_nonfo_pb2_sch.py``, not here, so the
port is a faithful copy that can be re-run and diffed.

Usage: python3 port_blocks.py /path/to/Serenity-UAV
Author: Claude (Anthropic), 2026-11-18, for S. Griffing.
"""

from __future__ import annotations

import importlib.util
import json
import subprocess
import sys
import tempfile
from pathlib import Path

OUT = Path(__file__).resolve().parents[1] / "sch" / "ported_blocks.json"

# Pilot: everything but the PB2 rails (rebuilt from the ledger) and the M2.5 holes (M3 here).
PILOT_SKIP = {"PB2-P1", "PB2-P2", "H1", "H2", "H3", "H4"}
# TACCO: the RF, logging and fan blocks.  Parts TACCO shares with Pilot come from Pilot.
TACCO_PREFIX = (
    "MLRS-", "X-MLRS", "RFSW-MLRS", "C-MLRS-", "L-MLRS-", "R-MLRS-", "FB-MLRS-", "SW-MLRS",
    "LED-MLRS-", "J-MLRS-", "WIFI-BT-ZB", "C-ZB-", "NOR-FLASH", "C-FLASH1", "R-FLASH-WP",
    "SD-WB", "C-PLD1", "J-FAN", "J-SD", "U-3V3RF", "U-1V8RF", "C-1V8RF", "L-RF1", "C-RF-",
    "D-ANT-", "J-ANT-", "C-ANT-", "L-ANT-SER",
)
GPS_REFS = {"GPS", "C-GPS1", "C-GPS2", "R-ANT", "C-ANT", "L-ANT", "J-ANT"}


def load(name: str, path: Path):
    spec = importlib.util.spec_from_file_location(name, path)
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod


def part(ic: dict, origin: str) -> dict:
    return {
        "ref": ic["ref"], "value": ic["value"], "fp": ic["fp"], "mpn": ic.get("mpn", ""),
        "mfr": ic.get("mfr", ""), "ds": ic.get("ds", ""), "dnp": bool(ic.get("dnp")),
        "in_bom": ic.get("in_bom", True), "origin": origin,
        "pins": [list(p) for p in ic["pins"]],
    }


def main() -> None:
    root = Path(sys.argv[1]).resolve()
    kic = root / "avionics" / "kicad"
    pilot = load("pilot", kic / "Pilot" / "scripts" / "gen_pilot_sch.py")
    tacco = load("tacco", kic / "TACCO" / "scripts" / "gen_tacco_sch.py")
    old = subprocess.run(
        ["git", "-C", str(root), "show", "3f55d58^:avionics/kicad/Pilot/scripts/gen_pilot_sch.py"],
        check=True, capture_output=True, text=True,
    ).stdout
    with tempfile.TemporaryDirectory() as td:
        p = Path(td) / "pilot_gnss.py"
        p.write_text(old)
        gnss = load("pilot_gnss", p)
    head = subprocess.run(["git", "-C", str(root), "rev-parse", "--short", "HEAD"],
                          check=True, capture_output=True, text=True).stdout.strip()
    parts = [part(i, f"Pilot@{head}") for i in pilot.ICS if i["ref"] not in PILOT_SKIP]
    taken = {p["ref"] for p in parts}
    parts += [part(i, f"TACCO@{head}") for i in tacco.ICS
              if i["ref"].startswith(TACCO_PREFIX) and i["ref"] not in taken]
    parts += [part(i, "Pilot@3f55d58^") for i in gnss.ICS if i["ref"] in GPS_REFS]
    OUT.parent.mkdir(parents=True, exist_ok=True)
    OUT.write_text(json.dumps({"_source": f"Serenity-UAV {head}; see port_blocks.py",
                               "parts": parts}, indent=1) + "\n")
    print(f"wrote {OUT.name}: {len(parts)} parts")


if __name__ == "__main__":
    main()
