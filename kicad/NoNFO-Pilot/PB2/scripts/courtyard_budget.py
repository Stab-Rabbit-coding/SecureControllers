#!/usr/bin/env python3
# SPDX-License-Identifier: CERN-OHL-W-2.0
"""S35 courtyard budget: summed part courtyards per zone against 80 % of each face's zone area.

Parts with a fixed quantity go on the top face. The '~N' passive families (0402 class, under the
zone contract's 1.0 mm bottom-face limit) go on the bottom face.

Reads docs/BOM.csv, zone_contract.json and docs/footprint_geometry.json (pad and courtyard
geometry extracted from every footprint with KiCad 9.0.2's pcbnew). Passive families with a
"~N" quantity are spread across zones by PASSIVE_SHARE (an assumption until S36 counts them).
Exit 1 when any zone exceeds the limit. Drafted by Claude (Anthropic), S35, 2026-11-17.
"""

from __future__ import annotations

import csv
import json
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parents[1]
LIMIT = 0.80
PASSIVE_SHARE = {
    "iso_island": 0.30,
    "logic": 0.40,
    "rf": 0.20,
    "power_entry": 0.10,
}  # [ASSUMED]
PASSIVE_FP = "Capacitor_SMD:C_0402_1005Metric"  # every '~N' family is costed as 0402


def zone_areas(c: dict) -> dict[str, float]:
    a = {z["name"]: (z["x1"] - z["x0"]) * (z["y1"] - z["y0"]) for z in c["zones"]}
    a["logic"] -= (
        a["rf"] + a["power_entry"]
    )  # rf and power entry sit inside the logic zone
    return a


def budget() -> tuple[dict[str, float], dict[str, float], dict[str, float]]:
    """Return (top-face courtyard, bottom-face courtyard, zone area) per zone, mm2."""
    c = json.loads((HERE / "zone_contract.json").read_text())
    geom = json.loads((HERE / "docs" / "footprint_geometry.json").read_text())
    used = dict.fromkeys(PASSIVE_SHARE, 0.0)
    bottom = dict.fromkeys(PASSIVE_SHARE, 0.0)
    for r in csv.DictReader((HERE / "docs" / "BOM.csv").open()):
        fp, q = r["footprint"], r["qty"]
        if q.startswith("~"):
            w, h = geom[PASSIVE_FP]["courtyard"]
            for z, s in PASSIVE_SHARE.items():
                bottom[z] += int(q[1:]) * s * w * h
            continue
        if fp not in geom:
            raise SystemExit(f"no geometry for {fp} (line {r['line']})")
        w, h = geom[fp]["courtyard"]
        used[r["zone"]] += int(q) * w * h
    return used, bottom, zone_areas(c)


def main() -> int:
    top, bot, area = budget()
    ok = True
    print(
        f"{'zone':12s} {'area mm2':>9s} {'top mm2':>8s} {'top':>5s} {'bottom mm2':>11s} {'bottom':>7s}"
    )
    for z in PASSIVE_SHARE:
        ft, fb = top[z] / area[z], bot[z] / area[z]
        ok &= ft <= LIMIT and fb <= LIMIT
        print(
            f"{z:12s} {area[z]:9.0f} {top[z]:8.0f} {ft:5.0%} {bot[z]:11.0f} {fb:7.0%}  "
            f"{'PASS' if ft <= LIMIT and fb <= LIMIT else 'FAIL'}"
        )
    return 0 if ok else 1


if __name__ == "__main__":
    sys.exit(main())
