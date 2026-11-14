#!/usr/bin/env python3
# SPDX-License-Identifier: CERN-OHL-W-2.0 (hardware-generating tool; licence-by-output rule, Serenity-UAV AGENTS.md §3)
"""NoNFO-Pilot-PB2 MCU ledger: do the option-B+ lines fit the MSPM0G3519-Q1 RGZ-48?

Reads MSPM0G3519_RGZ48_mux.json (TI SLASFA6B Table 6-2, restricted to the 44 ports the RGZ-48
bonds) and mcu_net_demand.json. Each peripheral group takes one instance; group roles, timers
and GPIO then take distinct free ports. Open-drain-only ports (PA0, PA1) take inputs only.
Exit 1 when no allocation exists. Drafted by Claude (Anthropic) for S. Griffing, 2026-11-14.
"""

from __future__ import annotations

import argparse
import itertools
import json
import re
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent


def instances(
    ports: dict[str, dict[str, int]], inst: str, roles: list[str]
) -> list[dict[str, list[str]]]:
    names = sorted(
        {
            s.split("_")[0]
            for sigs in ports.values()
            for s in sigs
            if re.fullmatch(inst.replace("*", r"\d+"), s.split("_")[0])
        }
    )
    out = []
    for n in names:
        cand = {
            r: sorted(p for p, sigs in ports.items() if f"{n}_{r}" in sigs)
            for r in roles
        }
        if all(cand.values()):
            out.append({"_inst": [n], **cand})
    return out


def solve(mux: dict, dem: dict) -> dict[str, str] | None:
    ports = mux["ports"]
    free = set(ports) - set(dem["reserved"])
    od = set(dem["open_drain_only"])
    if len(dem["nets"]) > len(free):
        # Every group takes a fixed port count, so a count shortfall is final.
        return None
    gnets: dict[str, dict[str, str]] = {}
    for n in dem["nets"]:
        g, _, role = n["need"].partition(":")
        if g in dem["groups"]:
            gnets.setdefault(g, {})[role] = n["net"]
    gkeys = sorted(gnets)
    opts = [instances(ports, dem["groups"][g]["inst"], sorted(gnets[g])) for g in gkeys]
    timers = [n["net"] for n in dem["nets"] if n["need"] == "timer"]
    outs = [n["net"] for n in dem["nets"] if n["need"] == "gpio_out"]
    ins = [n["net"] for n in dem["nets"] if n["need"] == "gpio_in"]
    best: list[dict[str, str] | None] = [None]

    def place(i: int, used: set[str], insts: set[str], cur: dict[str, str]) -> bool:
        if i == len(gkeys):
            left = free - used
            tim = [
                p
                for p in sorted(left - od)
                if any(re.match(r"TIM[AG]\d+_C\d$", s) for s in ports[p])
            ]
            if len(tim) < len(timers):
                return False
            pick = dict(cur)
            for net, p in zip(timers, tim):
                pick[net] = p + " (timer)"
                left = left - {p}
            push = sorted(left - od, key=lambda p: (p[1], int(p[2:])))
            if len(push) < len(outs):
                return False
            for net, p in zip(outs, push):
                pick[net] = p + " (GPIO out)"
                left = left - {p}
            inp = sorted(left, key=lambda p: (p not in od, p))
            if len(inp) < len(ins):
                return False
            for net, p in zip(ins, inp):
                pick[net] = p + " (GPIO in)"
                left = left - {p}
            pick["_spare"] = ", ".join(sorted(left, key=lambda p: (p[1], int(p[2:]))))
            best[0] = pick
            return True
        for opt in opts[i]:
            inst = opt["_inst"][0]
            if inst in insts:
                continue
            roles = sorted(gnets[gkeys[i]])
            for combo in itertools.product(*[opt[r] for r in roles]):
                if len(set(combo)) < len(combo) or any(
                    p in used or p not in free or p in od for p in combo
                ):
                    continue
                nxt = dict(cur)
                nxt.update(
                    {
                        gnets[gkeys[i]][r]: f"{p} ({inst}_{r})"
                        for r, p in zip(roles, combo)
                    }
                )
                if place(i + 1, used | set(combo), insts | {inst}, nxt):
                    return True
        return False

    place(0, set(), set(), {})
    return best[0]


def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__.split("\n")[0])
    ap.add_argument("--mux", type=Path, default=HERE / "MSPM0G3519_RGZ48_mux.json")
    ap.add_argument("--demand", type=Path, default=HERE / "mcu_net_demand.json")
    args = ap.parse_args()
    mux = json.loads(args.mux.read_text())
    dem = json.loads(args.demand.read_text())
    alloc = solve(mux, dem)
    n = len(dem["nets"]) + 2  # plus SWD
    print(
        f"ports on package: {len(mux['ports'])}; lines: {n} (incl. SWD); "
        f"{'FITS' if alloc else 'NO FIT'}"
    )
    if not alloc:
        return 1
    for k in sorted(alloc, key=lambda k: (k == "_spare", alloc[k])):
        print(f"    {k:14s} {alloc[k]}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
