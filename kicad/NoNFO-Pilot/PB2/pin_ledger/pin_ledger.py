#!/usr/bin/env python3
# SPDX-License-Identifier: CERN-OHL-W-2.0 (hardware-generating tool; licence-by-output rule, Serenity-UAV AGENTS.md §3)
"""NoNFO-Pilot-PB2 pin ledger: does a net set fit the PocketBeagle 2 Industrial P1/P2 headers?

Reads the AM625 header mux table (SPRSP58C Table 5-1, extracted in Serenity-UAV
avionics/datasheets/extracted/AM625_PB2I_header_mux.json; a hashed copy sits beside this file)
and pb2_net_demand.json, then searches for a legal allocation for each architecture option:
fixed-function nets take the only pin that carries the signal, UART / SPI2 / I2C groups take one
peripheral instance, DSHOT takes PRU0 outputs, and GPIO-class nets fill what is left.

Exit status is 1 when the option named by --require does not fit (for CI).
Drafted by Claude (Anthropic) for S. Griffing, 2026-11-14.
"""

from __future__ import annotations

import argparse
import itertools
import json
import re
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
# Header pins that also carry a PB2-I MSPM0L1105 analog pin (PB2I_AM625_HEADER_CAPABILITIES.md §6).
AIN_SHARED = {"P1.02", "P1.19", "P1.21", "P1.23", "P1.25", "P1.27", "P2.35", "P2.36"}


def load_pins(path: Path) -> dict[str, set[str]]:
    """Header pin -> every signal any of its balls can carry ('P1.02A' folds into 'P1.02')."""
    pins: dict[str, set[str]] = {}
    for ball in json.loads(path.read_text())["balls"].values():
        pin = ball["pin"].rstrip("A")
        pins.setdefault(pin, set()).update(ball["modes"].values())
    return pins


def pins_with(pins: dict[str, set[str]], pattern: str) -> list[str]:
    rx = re.compile(pattern + r"$")
    return sorted(p for p, sigs in pins.items() if any(rx.match(s) for s in sigs))


def group_options(
    pins: dict[str, set[str]], kind: str, roles: list[str]
) -> list[dict[str, list[str]]]:
    """Every peripheral instance that offers all roles: [{role: [candidate pins]}, ...]."""
    if kind == "uart":
        insts = [f"UART{i}" for i in range(7)]
        pat = "{inst}_{role}"
    elif kind == "spi2":
        insts, pat = ["SPI2"], "{inst}_{role}"
    else:  # i2c
        insts, pat = ["I2C1", "I2C2", "I2C3"], "{inst}_{role}"
    out = []
    for inst in insts:
        cand = {}
        for role in roles:
            sig = pat.format(inst=inst, role=role) + (r"\d" if role == "CS" else "")
            cand[role] = pins_with(pins, sig)
        if all(cand.values()):
            out.append({"inst": [inst], **cand})
    return out


def solve(
    pins: dict[str, set[str]], nets: list[dict], reserved: dict[str, str]
) -> tuple[dict[str, str] | None, str]:
    """Return ({net: pin}, note). None when no allocation exists."""
    free = set(pins) - set(reserved)
    alloc: dict[str, str] = {}
    # 1. fixed-function nets: exactly one header pin carries the signal
    for n in nets:
        if n["need"].startswith("fixed:"):
            cand = [p for p in pins_with(pins, n["need"][6:]) if p in free]
            if not cand:
                return None, f"no free pin carries {n['need'][6:]} for {n['net']}"
            alloc[n["net"]] = cand[0]
            free.discard(cand[0])
    # 2. grouped peripherals: collect groups, then search instance + pin choices
    groups: dict[str, dict[str, str]] = {}
    for n in nets:
        parts = n["need"].split(":")
        if parts[0] == "uart":
            groups.setdefault("uart:" + parts[1], {})[parts[2]] = n["net"]
        elif parts[0] in ("spi2", "i2c"):
            groups.setdefault(parts[0], {})[parts[1]] = n["net"]
    pru = [n["net"] for n in nets if n["need"] == "pru0"]
    pwm = [n["net"] for n in nets if n["need"] == "ehrpwm"]
    gpio = [n["net"] for n in nets if n["need"] == "gpio"]
    gkeys = sorted(groups)
    gopts = [group_options(pins, k.split(":")[0], sorted(groups[k])) for k in gkeys]
    if any(not o for o in gopts):
        return None, "a peripheral group has no instance on the header"
    best: tuple[int, dict[str, str]] | None = None

    def place(
        i: int, used: set[str], cur: dict[str, str], insts: tuple[str, ...]
    ) -> None:
        nonlocal best
        if i == len(gkeys):
            finish(used, cur)
            return
        for opt in gopts[i]:
            inst = opt["inst"][0]
            if inst in insts and not gkeys[i].startswith(("spi2", "i2c")):
                continue
            roles = sorted(groups[gkeys[i]])
            for combo in itertools.product(*[opt[r] for r in roles]):
                if len(set(combo)) < len(combo) or any(
                    p in used or p not in free for p in combo
                ):
                    continue
                nxt = dict(cur)
                nxt.update(
                    {
                        groups[gkeys[i]][r]: f"{p} ({inst}_{r})"
                        for r, p in zip(roles, combo)
                    }
                )
                place(i + 1, used | set(combo), nxt, insts + (inst,))

    def finish(used: set[str], cur: dict[str, str]) -> None:
        nonlocal best
        left = free - used
        # DSHOT prefers PRU0 outputs off the MSPM0-shared pins
        pru_c = sorted(
            (p for p in pins_with(pins, r"PR0_PRU0_GPO\d+") if p in left),
            key=lambda p: (p in AIN_SHARED, p),
        )
        if len(pru_c) < len(pru):
            return
        pick = dict(cur)
        for net, p in zip(pru, pru_c):
            pick[net] = p + " (PRU0)"
            left = left - {p}
        pwm_c = [p for p in pins_with(pins, r"EHRPWM\d_[AB]") if p in left]
        if len(pwm_c) < len(pwm):
            return
        for net, p in zip(pwm, pwm_c):
            pick[net] = p + " (EHRPWM)"
            left = left - {p}
        gp = sorted(
            (
                p
                for p in left
                if any(s.startswith("GPIO") or "_GPIO" in s for s in pins[p])
            ),
            key=lambda p: (p in AIN_SHARED, p),
        )
        spare = len(gp) - len(gpio)
        if best is None or spare > best[0]:
            for net, p in zip(gpio, gp):
                pick[net] = p + " (GPIO)"
            pick["_spare"] = ", ".join(gp[len(gpio) :]) if spare > 0 else ""
            best = (spare, pick)

    place(0, set(), {}, ())
    if best is None:
        return None, "peripheral groups do not fit together"
    if best[0] < 0:
        return None, f"short by {-best[0]} GPIO-class pins"
    alloc.update(best[1])
    return alloc, f"{best[0]} spare"


def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__.split("\n")[0])
    ap.add_argument("--mux", type=Path, default=HERE / "AM625_PB2I_header_mux.json")
    ap.add_argument("--demand", type=Path, default=HERE / "pb2_net_demand.json")
    ap.add_argument("--require", help="option that must fit (exit 1 if it does not)")
    ap.add_argument("--show", help="print the allocation for this option")
    ap.add_argument(
        "--drop", default="", help="comma-separated net-name prefixes to leave out"
    )
    args = ap.parse_args()
    pins = load_pins(args.mux)
    dem = json.loads(args.demand.read_text())
    drop = tuple(d for d in args.drop.split(",") if d)
    usable = len(pins) - len(dem["reserved_pins"])
    print(
        f"header signal pins: {len(pins)} ({usable} after reserving "
        f"{', '.join(dem['reserved_pins'])} for the console)"
    )
    ok = True
    for opt in dem["options"]:
        nets = [
            n
            for n in dem["nets"]
            if opt in n["arch"] and not n["net"].startswith(drop or ("\0",))
        ]
        alloc, note = solve(pins, nets, dem["reserved_pins"])
        ain = sorted(
            v.split()[0]
            for k, v in (alloc or {}).items()
            if k != "_spare"
            and v.split()[0] in AIN_SHARED
            and not k.startswith("RMII2")
        )
        print(
            f"{opt:7s} nets {len(nets):2d}  {'FITS' if alloc else 'NO FIT':6s} {note}"
            + (
                f"; non-RMII nets on MSPM0-shared pins: {', '.join(ain) or 'none'}"
                if alloc
                else ""
            )
        )
        if args.show == opt and alloc:
            for k in sorted(alloc, key=lambda k: (alloc[k], k)):
                print(f"    {k:18s} {alloc[k]}")
        if args.require == opt and not alloc:
            ok = False
    return 0 if ok else 1


if __name__ == "__main__":
    sys.exit(main())
