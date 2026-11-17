# SPDX-License-Identifier: CERN-OHL-W-2.0
"""S35 tests: BOM completeness, the sourcing gate, generated footprints and the courtyard budget."""

import csv
import importlib.util
import json
import re
from pathlib import Path

HERE = Path(__file__).resolve().parents[1]
BOM = list(csv.DictReader((HERE / "docs" / "BOM.csv").open()))
GEOM = json.loads((HERE / "docs" / "footprint_geometry.json").read_text())
# Root AGENTS.md §5 (owner rule 2026-10-17): restricted domiciles, and makers controlled from one.
RESTRICTED = {"China", "PRC", "Hong Kong", "Macau", "Russia", "Iran", "North Korea"}
CONTROLLED = {"Nexperia": "Wingtech (PRC)"}


def sourcing_ok(row: dict) -> bool:
    return (
        row["domicile"] not in RESTRICTED
        and row["manufacturer"].split()[0] not in CONTROLLED
    )


def _load(name):
    spec = importlib.util.spec_from_file_location(name, HERE / "scripts" / f"{name}.py")
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod


def test_every_row_has_mpn_maker_footprint_and_source():
    for r in BOM:
        assert r["mpn"] and r["manufacturer"] and r["footprint"] and r["datasheet"], r[
            "line"
        ]


def test_every_row_passes_the_sourcing_gate():
    assert all(sourcing_ok(r) for r in BOM)


def test_sourcing_gate_rejects_a_known_failing_part():
    # TACCO's PRTR5V0U2X: Nexperia is owned by Wingtech (PRC), so the gate must refuse it.
    nexperia = {
        "manufacturer": "Nexperia",
        "domicile": "Netherlands",
        "mpn": "PRTR5V0U2X,315",
    }
    wch = {"manufacturer": "WCH (Nanjing Qinheng)", "domicile": "China", "mpn": "CH334"}
    assert not sourcing_ok(nexperia) and not sourcing_ok(wch)


def test_every_fixed_footprint_has_geometry():
    for r in BOM:
        if not r["qty"].startswith("~"):
            assert r["footprint"] in GEOM, r["footprint"]


def test_generated_footprints_match_their_land_patterns():
    g = {k.split(":", 1)[1]: v for k, v in GEOM.items() if k.startswith("NoNFO:")}
    lwb = g["Ezurio_LWB5plus_LGA-68_17x12mm"]
    assert (
        lwb["pads"] == 68
        and lwb["sizes"]["(0.4, 1.0)"] == 42
        and lwb["sizes"]["(1.2, 1.2)"] == 9
    )
    hub = g["Microchip_VQFN-48-1EP_7x7mm_P0.5mm_EP4.2x4.2mm"]
    assert (
        hub["pads"] == 49
        and hub["sizes"]["(4.2, 4.2)"] == 1
        and hub["sizes"]["(0.85, 0.3)"] == 24
    )
    dsk = g["TI_DSK0010A_WSON-10-1EP_2.5x2.5mm_P0.5mm_EP1.2x2mm"]
    assert (
        dsk["pads"] == 11
        and dsk["sizes"]["(0.6, 0.25)"] == 10
        and dsk["min_pitch"] == 0.5
    )


def test_generator_is_deterministic():
    gen = _load("gen_nonfo_pb2_footprints")
    before = {p.name: p.read_text() for p in gen.OUT.glob("*.kicad_mod")}
    gen.main()
    after = {p.name: p.read_text() for p in gen.OUT.glob("*.kicad_mod")}
    assert before == after


def test_courtyard_budget_reports_every_zone():
    top, bottom, area = _load("courtyard_budget").budget()
    assert (
        set(top)
        == set(bottom)
        == set(area)
        == {"iso_island", "logic", "rf", "power_entry"}
    )
    assert all(v > 0 for v in area.values())


def test_no_row_is_marked_unverified_without_an_open_item():
    open_items = (HERE / "NONFO_PB2_FOOTPRINT_VERIFICATION.md").read_text()
    for r in BOM:
        if r["fp_check"] == "UNVERIFIED":
            assert re.search(re.escape(r["mpn"]), open_items), r["mpn"]
