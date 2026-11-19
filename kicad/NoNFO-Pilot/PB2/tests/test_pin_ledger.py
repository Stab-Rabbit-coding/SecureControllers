# SPDX-License-Identifier: CERN-OHL-W-2.0
"""Tests for the NoNFO-Pilot-PB2 header and MCU pin ledgers."""

import importlib.util
import json
from pathlib import Path

LEDGER = Path(__file__).resolve().parents[1] / "pin_ledger"


def _load(name):
    spec = importlib.util.spec_from_file_location(name, LEDGER / f"{name}.py")
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod


pl = _load("pin_ledger")
ml = _load("mcu_ledger")
PINS = pl.load_pins(LEDGER / "AM625_PB2I_header_mux.json")
DEMAND = json.loads((LEDGER / "pb2_net_demand.json").read_text())
MUX = json.loads((LEDGER / "MSPM0G3519_RGZ48_mux.json").read_text())
MCU = json.loads((LEDGER / "mcu_net_demand.json").read_text())


def _nets(option, drop=()):
    return [
        n
        for n in DEMAND["nets"]
        if option in n["arch"] and not n["net"].startswith(drop or ("\0",))
    ]


def _pins_used(alloc):
    return [v.split()[0] for k, v in alloc.items() if k != "_spare"]


def test_bplus_fits_the_header_without_reuse_or_console():
    alloc, _ = pl.solve(PINS, _nets("B+"), DEMAND["reserved_pins"])
    assert alloc is not None
    used = _pins_used(alloc)
    assert len(used) == len(set(used))
    assert not set(used) & set(DEMAND["reserved_pins"])


def test_option_a_does_not_fit():
    alloc, note = pl.solve(PINS, _nets("A"), DEMAND["reserved_pins"])
    assert alloc is None and "short" in note


def test_dropping_gnss_adds_spare_pins():
    _, with_gnss = pl.solve(PINS, _nets("B+"), DEMAND["reserved_pins"])
    _, without = pl.solve(PINS, _nets("B+", ("GNSS",)), DEMAND["reserved_pins"])
    assert int(without.split()[0]) > int(with_gnss.split()[0])


def test_extra_nets_on_a_full_header_fail():
    extra = [{"net": f"X{i}", "need": "gpio", "arch": ["B+"]} for i in range(3)]
    alloc, _ = pl.solve(PINS, _nets("B+") + extra, DEMAND["reserved_pins"])
    assert alloc is None


def test_mcu_lines_fit_rgz48_and_keep_swd_free():
    alloc = ml.solve(MUX, MCU)
    assert alloc is not None
    used = _pins_used(alloc)
    assert len(used) == len(set(used))
    assert not set(used) & set(MCU["reserved"])
    assert alloc["MCAN_TX"].startswith("PA12") and alloc["MCAN_RX"].startswith("PA13")


def test_mcu_open_drain_ports_take_inputs_only():
    alloc = ml.solve(MUX, MCU)
    for k, v in alloc.items():
        if k != "_spare" and v.split()[0] in MCU["open_drain_only"]:
            assert "GPIO in" in v


def test_mcu_overfull_demand_fails():
    over = dict(
        MCU,
        nets=MCU["nets"] + [{"net": f"Y{i}", "need": "gpio_out"} for i in range(13)],
    )
    assert ml.solve(MUX, over) is None
