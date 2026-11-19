# SPDX-License-Identifier: CERN-OHL-W-2.0
"""S36 tests: the generated schematic agrees with the pin ledger and the board's design rules.

The checks run on the generator's part table (the same table the .kicad_sch is written
from), so they need no KiCad install; CI runs KiCad's own ERC as a separate job.
"""

import importlib.util
import json
from pathlib import Path

HERE = Path(__file__).resolve().parents[1]


def _gen():
    spec = importlib.util.spec_from_file_location("gen", HERE / "scripts" / "gen_nonfo_pb2_sch.py")
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod


GEN = _gen()
PARTS = GEN.all_parts()
NETS = GEN.netlist(PARTS)
BY_REF = {p["ref"]: p for p in PARTS}
GROUNDS = {n for n in NETS if n.startswith(("GND", "PGND"))}

# DC paths between nets: resistors, inductors, ferrite beads and fuses.  ICs, connectors and
# capacitors do not join ground domains galvanically; the isolators are the intended barrier.
CONDUCTS = ("R-", "L-", "FB", "F-")

# Pull-ups and pull-downs the board needs, net -> resistor.  Each one sets a pin state
# that the data sheet makes mandatory, so losing one is a defect.
REQUIRED_PULLS = {
    "MCU_RSTN": "R-MCU-RST",        # MSPM0 NRST must be pulled high (SLASFA6B sec 9.1)
    "MCU_BSL": "R-MCU-BSL",         # PA18 low at reset or the MCU enters its boot loader
    "USB_HUB_RSTN": "R-HUB-RST",
    "HUB_SPI_CLK": "R-HUB-SPICLK",  # USB2641i SPI_CLK low during reset
    "WIFI_STRAP": "R-WIFI-STRAP",   # LWB5+ USB/USB host strap
    "FLASH_WP_N": "R-FLASH-WP",
    "M1553_IRQN": "R-1553IRQ",
    "SD_NCD": "R-SD-CD",
    "ZB_PDN": "R-ZB-PDN",
}


def ledger_alloc():
    return GEN.header_alloc()


def header_nets():
    out = {}
    for ref in ("PB2-P1", "PB2-P2"):
        for pn, fn, net, _ in BY_REF[ref]["pins"]:
            if net:
                out.setdefault(net, []).append(fn)
    return out


def test_every_ledger_net_is_on_exactly_its_ledger_pin():
    hn = header_nets()
    for net, pin in ledger_alloc().items():
        assert hn.get(net) == [pin], (net, pin, hn.get(net))


def test_no_header_signal_outside_the_ledger():
    fixed = {"+5V", "GND", "USB1_DM", "USB1_DP"}
    assert set(header_nets()) - fixed == set(ledger_alloc())


def test_console_pins_stay_free():
    p1 = {fn: net for _pn, fn, net, _ in BY_REF["PB2-P1"]["pins"]}
    assert p1["P1.30"] is None and p1["P1.32"] is None


def test_every_net_reaches_two_pins():
    assert {n: p for n, p in NETS.items() if len(p) < 2} == {}


def test_mcu_pins_match_the_mcu_ledger():
    alloc = GEN.mcu_alloc()
    pins = {fn: net for _pn, fn, net, _ in BY_REF["MCU"]["pins"]}
    for net, port in alloc.items():
        assert pins[port.split()[0]] == GEN.MCU_HOST.get(net, net), net


def _domains(parts):
    parent = {}

    def find(x):
        parent.setdefault(x, x)
        while parent[x] != x:
            parent[x] = parent[parent[x]]
            x = parent[x]
        return x

    for p in parts:
        nets = [n for _pn, _fn, n, _ in p["pins"] if n]
        if p["ref"].startswith(CONDUCTS) and len(nets) == 2:
            parent[find(nets[0])] = find(nets[1])
    return find


def test_isolated_grounds_have_no_dc_path_to_logic_ground():
    find = _domains(PARTS)
    for iso in ("GND2_CAN", "GND2_RS485"):
        assert find(iso) != find("GND"), iso
    assert find("GND2_CAN") != find("GND2_RS485")


def test_barrier_check_catches_a_bridge():
    # Negative control: a 0 R from the CAN island to logic ground must be caught.
    bridge = {"ref": "R-BRIDGE", "pins": [("1", "A", "GND2_CAN", "L"), ("2", "B", "GND", "R")]}
    find = _domains(PARTS + [bridge])
    assert find("GND2_CAN") == find("GND")


def _decoupled(net):
    for p in PARTS:
        nets = [n for _pn, _fn, n, _ in p["pins"]]
        if len(nets) == 2 and net in nets and p["value"][0].isdigit() and "F" in p["value"]:
            other = nets[1] if nets[0] == net else nets[0]
            if other in GROUNDS:
                return True
    return False


POWER_NAMES = ("VDD", "VCC", "VIN", "VBAT", "VIO", "AVDD", "DVDD", "VDDA", "VDDRF", "VDDPA",
               "VDDSMPS", "VDD33", "V_IO", "VCCP", "VSIN", "VISOIN", "VDDIO", "USB2_AVDD33")


# Power-named pins that are outputs, not loads.
OUTPUTS = {("GPS", "VCC_RF")}


def test_every_ic_power_pin_has_a_decoupling_capacitor():
    missing = []
    for p in PARTS:
        if len(p["pins"]) <= 4 or p["ref"].startswith(("PB2-", "J-", "J")):
            continue
        for _pn, fn, net, _ in p["pins"]:
            if (net and fn and fn.upper().startswith(POWER_NAMES) and (p["ref"], fn) not in OUTPUTS
                    and not _decoupled(net)):
                missing.append((p["ref"], fn, net))
    assert missing == []


def _pulls(parts):
    found = {}
    for p in parts:
        nets = [n for _pn, _fn, n, _ in p["pins"]]
        if p["ref"].startswith("R-") and len(nets) == 2:
            for n in nets:
                found.setdefault(n, set()).add(p["ref"])
    return {n: r for n, r in REQUIRED_PULLS.items() if r not in found.get(n, set())}


def test_required_pull_resistors_are_present():
    assert _pulls(PARTS) == {}


def test_pull_check_catches_a_missing_pull_up():
    # Negative control: drop the MCU reset pull-up and the check must report it.
    assert _pulls([p for p in PARTS if p["ref"] != "R-MCU-RST"]) == {"MCU_RSTN": "R-MCU-RST"}


def test_every_s35_bom_part_is_on_the_schematic():
    import csv

    mpns = {p["mpn"] for p in PARTS}
    skip = {"TPS62933DRLR", "74438335033"}  # the 3V3 alternative S36 did not pick
    for r in csv.DictReader((HERE / "docs" / "BOM.csv").open(newline="")):
        if r["qty"].startswith("~") or r["qty"] == "0" or r["mpn"] in skip or "(no part)" in r["manufacturer"]:
            continue
        if r["mpn"] in ("TC2030-IDC-NL footprint", "0603 green / red", "M3 PGND",
                        "32.768kHz LPO (to select)"):
            continue
        assert r["mpn"] in mpns or any(r["mpn"] in (p["value"] or "") for p in PARTS), r["mpn"]


def test_generator_is_deterministic():
    before = GEN.OUT.read_text()
    GEN._uid = __import__("itertools").count(1)
    GEN.main()
    assert GEN.OUT.read_text() == before


def test_ported_blocks_record_their_source():
    data = json.loads((HERE / "sch" / "ported_blocks.json").read_text())
    assert all(p["origin"] for p in data["parts"])
