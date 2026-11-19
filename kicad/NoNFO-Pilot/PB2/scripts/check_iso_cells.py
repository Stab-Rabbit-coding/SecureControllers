# SPDX-License-Identifier: CERN-OHL-W-2.0
"""check_iso_cells.py — S37 gate for the five isolation cells (KiCad 9.0.2 Python).

For every cell: KiCad DRC must report 0 errors and 0 unconnected items.  Then, as the
negative control, a copy of the cell gets one logic-net track drawn straight across the
moat on F.Cu; DRC on the copy must report the ISOLATION_MOAT keep-out.  A gate that cannot
see a moat crossing proves nothing about the cells that pass it.

Usage: python3 check_iso_cells.py [kicad-cli]      (exit 1 on any failure)
Author: Claude (Anthropic), 2026-11-19, for S. Griffing.
"""

from __future__ import annotations

import json
import shutil
import subprocess
import sys
import tempfile
from pathlib import Path

import pcbnew  # type: ignore

CELLS = Path(__file__).resolve().parents[1] / "cells"
NAMES = ("can", "rs485", "eth_rmii2", "eth_usb1", "m1553")
CLI = sys.argv[1] if len(sys.argv) > 1 else "kicad-cli"


def drc(pcb: Path) -> dict:
    out = pcb.with_suffix(".drc.json")
    subprocess.run([CLI, "pcb", "drc", "--format", "json", "--severity-all", "-o", str(out), str(pcb)],
                   check=True, capture_output=True)
    return json.loads(out.read_text())


def errors(rep: dict) -> list:
    return [v for v in rep["violations"] if v["severity"] == "error"]


def crossing_copy(name: str, tmp: Path) -> Path:
    src = CELLS / name
    dst = tmp / name
    shutil.copytree(src, dst)
    pcb = dst / f"{name}.kicad_pcb"
    board = pcbnew.LoadBoard(str(pcb))
    moat = [z for z in board.Zones() if z.GetIsRuleArea() and z.GetZoneName() == "ISOLATION_MOAT"]
    bb = moat[0].GetBoundingBox()
    y = bb.GetTop() + pcbnew.FromMM(0.8)
    t = pcbnew.PCB_TRACK(board)
    t.SetStart(pcbnew.VECTOR2I(bb.GetLeft() - pcbnew.FromMM(2), y))
    t.SetEnd(pcbnew.VECTOR2I(bb.GetRight() + pcbnew.FromMM(2), y))
    t.SetWidth(pcbnew.FromMM(0.25))
    t.SetLayer(pcbnew.F_Cu)
    t.SetNet(board.FindNet("GND"))
    board.Add(t)
    pcbnew.SaveBoard(str(pcb), board)
    return pcb


def main() -> int:
    ok = True
    with tempfile.TemporaryDirectory() as td:
        for name in NAMES:
            rep = drc(CELLS / name / f"{name}.kicad_pcb")
            e, u = errors(rep), rep["unconnected_items"]
            warn = sorted({v["type"] for v in rep["violations"] if v["severity"] == "warning"})
            print(f"{name:10s} DRC errors {len(e)}  unconnected {len(u)}  warnings: {', '.join(warn) or 'none'}")
            for v in e[:5]:
                print("   ", v["type"], v["description"])
            neg = drc(crossing_copy(name, Path(td)))
            hit = [v for v in errors(neg) if "ISOLATION_MOAT" in json.dumps(v)]
            print(f"{'':10s} negative control (track across the moat): {'caught' if hit else 'MISSED'}")
            ok &= not e and not u and bool(hit)
    print("PASS" if ok else "FAIL")
    return 0 if ok else 1


if __name__ == "__main__":
    sys.exit(main())
