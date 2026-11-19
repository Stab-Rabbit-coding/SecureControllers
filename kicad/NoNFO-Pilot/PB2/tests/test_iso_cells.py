# SPDX-License-Identifier: CERN-OHL-W-2.0
"""S37 tests that need no KiCad install: cell contents, clearance policy and rule text.

KiCad's own DRC on each cell (errors 0, unconnected 0) and the moat negative control run
in the CI ``drc`` job (``.github/workflows/kicad.yml``), which has KiCad 9.0.2.
"""

import json
import re
from pathlib import Path

HERE = Path(__file__).resolve().parents[1]
CELLS = ("can", "rs485", "eth_rmii2", "eth_usb1", "m1553")
DRU = (HERE / "kicads" / "NoNFO-Pilot-PB2.kicad_dru").read_text()
# Rules allowed to set a clearance below 0.3 mm, each documented in the DRU header.
FINE_PITCH = {"fine_pitch_hi6138": 0.15, "fine_pitch_tc1g00": 0.2}


def rules():
    return dict(re.findall(r"\(rule (\S+)\s*\n(.*?)(?=\n\(rule |\Z)", DRU, re.S))


def test_every_cell_board_exists_with_its_rules():
    for c in CELLS:
        d = HERE / "cells" / c
        assert (d / f"{c}.kicad_pcb").exists(), c
        assert (d / f"{c}.kicad_dru").read_text() == DRU, c


def test_default_clearance_is_0p3_mm_in_every_cell():
    for c in CELLS:
        pro = json.loads((HERE / "cells" / c / f"{c}.kicad_pro").read_text())
        classes = pro["net_settings"]["classes"]
        assert all(k["clearance"] >= 0.3 for k in classes), c
        assert pro["board"]["design_settings"]["rules"]["min_clearance"] >= 0.3, c


def test_only_documented_rules_go_below_0p3_mm():
    low = {}
    for name, body in rules().items():
        for v in re.findall(r"\(constraint clearance \(min ([0-9.]+)mm\)\)", body):
            if float(v) < 0.3:
                low[name] = float(v)
    assert low == FINE_PITCH


def test_cross_domain_rule_does_not_use_reference_on_tracks():
    # Pilot's form tested A.Reference, which is undefined on tracks and vias and silently
    # turned the rule off for them (S37 finding).  The cell rules must not repeat it.
    for name in ("iso_cross_domain_clearance", "bubble_can", "bubble_485"):
        assert "Reference" not in rules()[name], name


def test_cross_domain_barrier_is_0p5_mm():
    assert "(constraint clearance (min 0.5mm))" in rules()["iso_cross_domain_clearance"]


def test_bubble_rules_allow_only_converter_side_nets():
    for name, net in (("bubble_can", "CAN"), ("bubble_485", "RS485")):
        body = rules()[name]
        assert f"GND2_{net}_DCDC" in body and f"VCC2_{net}_DCDC" in body
        assert "disallow track via pad zone" in body
