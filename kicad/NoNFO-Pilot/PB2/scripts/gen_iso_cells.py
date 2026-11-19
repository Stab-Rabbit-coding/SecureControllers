# SPDX-License-Identifier: CERN-OHL-W-2.0
"""gen_iso_cells.py — NoNFO-Pilot-PB2 isolation cells, each on its own board (sprint S37).

Run under KiCad 9.0.2's Python (``kicad-python3`` / the ``kicad902`` wrapper):

    python3 gen_iso_cells.py place  <cell>          # build cells/<cell>/<cell>.kicad_pcb, write route.dsn
    python3 gen_iso_cells.py finish <cell> <ses>    # import the FreeRouting session, pour, save

``route_iso_cells.sh`` runs both stages and FreeRouting between them for all five cells.

Each cell holds one isolation barrier and everything the S36 schematic hangs on it.  The
parts, nets and footprints come from ``gen_nonfo_pb2_sch.all_parts()``, so a cell can only
differ from the board by placement.  Logic-side nets leave through one row of port pads on
the -X edge, standing in for the rest of the board; field-side copper ends at the field
connector, and chassis PGND at one pad on the +X edge.

Layer use (4 layers, 1.6 mm): F.Cu parts and signals; In1.Cu ground planes, GND on the
logic side and the isolated ground on the field side, split by the moat; In2.Cu and B.Cu
routing.  Every ground pad has its own via to In1.Cu, so ground is not left to the router.

Isolation rules (``NoNFO-Pilot-PB2.kicad_dru``, copied next to each cell):
  * ``ISOLATION_MOAT``: a keep-out on every copper layer, 1.0 mm wide, under the isolator
    or transformer bodies.  Only isolator and transformer pins and the X2Y bridge capacitor
    cross it.  The X2Y's isolated-ground terminals reach the field side through one
    documented opening on In2.Cu (an X2Y has its two ground terminals in the middle of the
    part, between the two signal terminals, so no straight moat can separate them).
  * ``iso_cross_domain_clearance``: 0.5 mm between field-side and logic-side copper (Pilot
    rule, X2Y exempt).
  * ``BUBBLE_CAN`` / ``BUBBLE_485``: ISOW1044 SLLSFF7A sec 13.1 item 5 / ISOW1412 SLLSF86C
    sec 13.1, "no metal traces or ground pour within 4 mm of VISOOUT (pin 12) and GND2
    (pin 11)".  Read here as the region outward of the pin row: item 4 of the same list
    puts the GND2 bead between pin 11 and pin 15 (5 mm apart), and pin 15's own lead lies
    inside a 4 mm circle, so the pin row itself cannot be inside the keep-out.  Only the
    converter-side ``*_DCDC`` nets (the item-1 10 nF and item-2 bulk capacitors, and the
    item-4 beads) may have copper there.  Owner review item, S37.
  * Clearance 0.3 mm everywhere except the documented fine-pitch footprints (``FINE``).

Author: Claude (Anthropic), 2026-11-19, for S. Griffing (Griffing Technology LLC).
"""

from __future__ import annotations

import importlib.util
import json
import math
import re
import shutil
import sys
from pathlib import Path

import pcbnew  # type: ignore

PB2 = Path(__file__).resolve().parents[1]
CELLS = PB2 / "cells"
DRU = PB2 / "kicads" / "NoNFO-Pilot-PB2.kicad_dru"
FPLIB = {
    "NoNFO": PB2 / "kicads" / "NoNFO-PB2.pretty",
    "Serenity-Custom": Path("/home/user/Serenity-UAV/avionics/kicad/Serenity-Custom.pretty"),
    "SecureControllers": PB2.parents[2] / "kicad" / "libraries" / "SecureControllers.pretty",
}
MM = pcbnew.FromMM
TRACK, POWER_TRACK, FINE_TRACK = 0.25, 0.4, 0.15
VIA_D, VIA_DRILL = 0.6, 0.3
MOAT_W = 1.0


def _gen():
    spec = importlib.util.spec_from_file_location("gen", PB2 / "scripts" / "gen_nonfo_pb2_sch.py")
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod


PARTS = {p["ref"]: p for p in _gen().all_parts()}


# ---------------------------------------------------------------------------
# Cell definitions.  (x, y, rotation in degrees) per part, board origin top-left, mm.
# ---------------------------------------------------------------------------
def isow_cell(name, iso, c, fb_v, fb_g, chk, tvs, rterm, conn, x2y, sig, gnd2, vcc2):
    """Both ISOW cells share one layout; c = the six capacitors C1..C6 in schematic order."""
    return {
        "name": name, "size": (40.0, 26.0), "moat_x": 18.0,
        "place": {
            iso: (18.0, 12.0, 0),
            c[0]: (11.7, 17.08, 90), c[1]: (9.2, 17.08, 90), c[2]: (11.7, 6.3, 90),
            x2y: (14.6, 22.0, 0),
            c[3]: (24.3, 17.08, 90), c[4]: (26.6, 17.08, 90),
            fb_v: (29.4, 16.3, 0), fb_g: (29.4, 17.9, 0),
            c[5]: (24.6, 4.2, 0),
            chk: (27.6, 8.2, 0), rterm: (31.6, 5.6, 0), tvs: (30.2, 12.2, 0),
            conn: (36.4, 8.6, None),
        },
        "orient": {  # (net that must be the upper / left pad) for two-pin parts
            c[3]: f"{vcc2}_DCDC", c[4]: f"{vcc2}_DCDC", fb_v: f"{vcc2}_DCDC", fb_g: f"{gnd2}_DCDC",
        },
        "ports_logic": ["+3V3", "GND", *sig, "+5V"],  # +5V last, beside the VDD capacitors
        "ports_field": ["PGND"],
        "planes": {"GND": "logic", gnd2: "field"},
        "hand_nets": [f"{vcc2}_DCDC", f"{gnd2}_DCDC"],
        "iso_ref": iso, "x2y": x2y, "gnd2": gnd2,
        "bubble": (iso, ("11", "12"), f"BUBBLE_{'CAN' if 'CAN' in iso else '485'}"),
    }


CAN = isow_cell("can", "CAN-TR", ["C-CAN1", "C-CAN2", "C-CAN3", "C-CAN4", "C-CAN5", "C-CAN6"],
                "FB-CAN-V", "FB-CAN-G", "CHK-CAN", "TVS-CAN", "R-CANT", "CAN-FD", "X2Y-CAN",
                ["MCAN_TX", "MCAN_RX", "CAN_STB"], "GND2_CAN", "VCC2_CAN")
RS485 = isow_cell("rs485", "RS485", ["C-485-1", "C-485-2", "C-485-3", "C-485-4", "C-485-5", "C-485-6"],
                  "FB-485-V", "FB-485-G", "CHK-RS485", "TVS-RS485", "R-485T", "RS-485", "X2Y-RS485",
                  ["RS485_TX", "RS485_RX", "RS485_DE"], "GND2_RS485", "VCC2_RS485")


def eth_cell(name, port):
    """Two TC1G00 per port.  Each TC1G00 mixes its windings across its two pad columns
    (Pulse TC002.C p.2: left pads 1, 2 primary and 3/4 secondary centre tap; right pads
    5, 6 secondary and 7/8 primary centre tap), so the moat steps under each body in a Z:
    the secondary centre tap stays on the line side above the step, the primary centre
    tap on the device side below it."""
    p, cx, yt, yr = port, 15.0, 6.0, 14.5
    ym = (yt + yr) / 2
    rmii = p == "RMII2"
    return {
        "name": name, "size": (34.0, 20.0), "moat_x": cx, "pgnd_field": True,
        # the under-body steps are 0.5 mm wide: they sit between pad 6 and pad 2, 1.41 mm apart
        "moat_path": [(cx - 3.2, 0), (cx - 3.2, yt, 0.5), (cx + 3.2, yt), (cx + 3.2, ym),
                      (cx - 3.2, ym), (cx - 3.2, yr, 0.5), (cx + 3.2, yr), (cx + 3.2, 20.0)],
        "place": {
            f"T-{p}-TX": (cx, yt, 0), f"T-{p}-RX": (cx, yr, 0),
            (f"C-{p}-CTD1" if rmii else f"C-{p}-CTD"): (cx, 9.1, 0),
            (f"C-{p}-CRD1" if rmii else f"C-{p}-CRD"): (cx, 17.6, 0),
            **({f"C-{p}-CTD2": (cx - 3.6, 9.1, 0), f"C-{p}-CRD2": (cx - 3.6, 17.6, 0)} if rmii else {}),
            f"R-{p}-BST": (21.0, 2.2, 0), f"R-{p}-BSR": (21.5, 11.4, 0),
            f"C-{p}-BS": (24.5, 6.0, 90),
            f"J-ETH-{p}": (30.5, 10.0, None),
        },
        "line_parts": [f"R-{p}-BST", f"R-{p}-BSR", f"C-{p}-BS", f"J-ETH-{p}"],
        "orient": {},
        "ports_logic": [f"ETH_{p}_TXP", f"ETH_{p}_TXN", f"ETH_{p}_RXP", f"ETH_{p}_RXN", "GND"],
        "ports_field": ["PGND"],
        "planes": {"GND": "logic", "PGND": "field"},
        "hand_nets": [],
    }


M1553 = {
    "name": "m1553", "size": (46.0, 28.0), "moat_x": 27.0, "pgnd_field": True,
    "place": {
        "1553-XCVR": (11.0, 14.0, 0), "X-50M": (11.0, 24.0, 0), "C-50M": (14.4, 24.0, 90),
        "C-1553A": (3.9, 9.0, 90), "C-1553B": (3.9, 19.0, 90), "C-1553C": (17.0, 19.6, 90),
        "C-1553D": (17.0, 8.4, 90), "R-1553IRQ": (3.9, 14.0, 90),
        "1553-XFM": (27.0, 14.0, 0),
        "R-1553P": (36.0, 10.0, 0), "R-1553N": (36.0, 18.0, 0),
        "TVS-1553P": (36.5, 4.0, 0), "TVS-1553N": (36.5, 24.0, 0),
        "MIL-1553": (42.0, 14.0, None),
    },
    "orient": {},
    "ports_logic": ["+3V3", "GND", "M1553_IRQN", "M1553_TX_INH", "M1553_CSN", "M1553_SCK",
                    "M1553_MISO", "M1553_MOSI", "M1553_MRN"],
    "ports_field": ["PGND"],
    "planes": {"GND": "logic", "PGND": "field", "+3V3": "logic"},
    "plane_layer": {"+3V3": "In2"},  # five HI-6138 supply pins: a plane, not five routes
    "hand_nets": [],
    "fanout": "1553-XCVR",
}
DEFS = {"can": CAN, "rs485": RS485, "eth_rmii2": eth_cell("eth_rmii2", "RMII2"),
        "eth_usb1": eth_cell("eth_usb1", "USB1"), "m1553": M1553}


def moat_rects(path, gap=None):
    """Rectangles, MOAT_W wide, along a rectilinear path; gap = (y0, y1) left open."""
    out = []
    for (x0, y0, *w0), (x1, y1, *_w1) in zip(path, path[1:]):
        h = (w0[0] if w0 else MOAT_W) / 2
        xa, xb, ya, yb = min(x0, x1) - h, max(x0, x1) + h, min(y0, y1) - h, max(y0, y1) + h
        spans = [(ya, yb)]
        if gap and x0 == x1:
            spans = [(ya, min(yb, gap[0])), (max(ya, gap[1]), yb)]
        for a, b in spans:
            if b > a:
                out.append([(xa, a), (xb, a), (xb, b), (xa, b)])
    return out


def field_nets(cell) -> set:
    """Nets on the field side of the barrier: every net of a part placed right of the moat."""
    mx = cell["moat_x"]
    out = set()
    if "line_parts" in cell:
        for ref in cell["line_parts"]:
            out |= {n for _pn, _fn, n, _ in PARTS[ref]["pins"] if n}
        return out if cell.get("pgnd_field") else out - {"PGND"}
    keep_pgnd = cell.get("pgnd_field")
    for ref, (x, _y, _r) in cell["place"].items():
        if x > mx and ref not in (cell.get("iso_ref"), cell.get("x2y")) and not ref.startswith(("T-", "1553-XFM")):
            out |= {n for _pn, _fn, n, _ in PARTS[ref]["pins"] if n}
    return out if keep_pgnd else out - {"PGND"}


# ---------------------------------------------------------------------------
# Board construction.
# ---------------------------------------------------------------------------
def load_fp(fpid: str):
    lib, name = fpid.split(":", 1)
    path = FPLIB.get(lib, Path(f"/usr/share/kicad/footprints/{lib}.pretty"))
    fp = pcbnew.FootprintLoad(str(path), name)
    if fp is None:
        raise SystemExit(f"footprint not found: {fpid}")
    return fp


def net(board, name):
    n = board.FindNet(name)
    if n is None:
        n = pcbnew.NETINFO_ITEM(board, name)
        board.Add(n)
    return board.FindNet(name)


def place(board, ref, x, y, rot, orient_net=None):
    part = PARTS[ref]
    fp = load_fp(part["fp"])
    fp.SetReference(ref)
    fp.SetValue(part["value"])
    board.Add(fp)
    pins = {}
    for pn, _fn, n, _ in part["pins"]:
        pins.setdefault(pn, n)
    for pad in fp.Pads():
        n = pins.get(pad.GetNumber())
        if n:
            pad.SetNet(net(board, n))
    fp.SetPosition(pcbnew.VECTOR2I(MM(x), MM(y)))
    if rot is None:  # field connector: mating face toward +X
        rot = 0
        for r in (0, 90, 180, 270):
            fp.SetOrientationDegrees(r)
            mp = [p for p in fp.Pads() if p.GetNumber() == "MP"]
            sig = [p for p in fp.Pads() if p.GetNumber() != "MP"]
            if sum(p.GetPosition().x for p in mp) / len(mp) > sum(p.GetPosition().x for p in sig) / len(sig) + MM(1):
                rot = r
                break
    fp.SetOrientationDegrees(rot)
    fp.Reference().SetLayer(pcbnew.F_Fab)  # cells are layout proofs: no silkscreen text
    fp.Value().SetVisible(False)
    for it in fp.GraphicalItems():
        if it.GetLayer() == pcbnew.F_SilkS:
            it.SetLayer(pcbnew.F_Fab)
    if orient_net:
        pads = [p for p in fp.Pads() if p.GetNetname() == orient_net]
        others = [p for p in fp.Pads() if p.GetNetname() != orient_net]
        if pads and others:
            a, b = pads[0].GetPosition(), others[0].GetPosition()
            vertical = abs(a.y - b.y) > abs(a.x - b.x)
            wrong = (a.y > b.y) if vertical else (a.x > b.x)
            if wrong:
                fp.SetOrientationDegrees(rot + 180)
    return fp


def port_row(board, ref, nets, x, y0, pitch=2.4):
    fp = pcbnew.FOOTPRINT(board)
    fp.SetReference(ref)
    fp.SetValue("cell port")
    fp.SetFPID(pcbnew.LIB_ID("NoNFO_cell", f"Port_{len(nets)}x1"))
    fp.SetPosition(pcbnew.VECTOR2I(MM(x), MM(y0)))
    board.Add(fp)
    for i, n in enumerate(nets):
        pad = pcbnew.PAD(fp)
        pad.SetNumber(str(i + 1))
        pad.SetShape(pcbnew.PAD_SHAPE_RECT)
        pad.SetAttribute(pcbnew.PAD_ATTRIB_SMD)
        pad.SetLayerSet(pad.SMDMask())
        pad.SetSize(pcbnew.VECTOR2I(MM(1.4), MM(1.0)))
        pad.SetPosition(pcbnew.VECTOR2I(MM(x), MM(y0 + i * pitch)))
        pad.SetNet(net(board, n))
        fp.Add(pad)
    return fp


def track(board, a, b, n, layer=pcbnew.F_Cu, w=POWER_TRACK):
    t = pcbnew.PCB_TRACK(board)
    t.SetStart(a)
    t.SetEnd(b)
    t.SetWidth(MM(w))
    t.SetLayer(layer)
    t.SetNet(net(board, n))
    board.Add(t)


def crosses(a, b, pads, margin=0.3):
    """True when segment a-b passes over any of the pads (bounding boxes grown by margin)."""
    for p in pads:
        bb = p.GetBoundingBox()
        bb.Inflate(MM(margin))
        for i in range(1, 40):
            q = pcbnew.VECTOR2I(int(a.x + (b.x - a.x) * i / 40), int(a.y + (b.y - a.y) * i / 40))
            if bb.Contains(q):
                return True
    return False


def link(board, a, b, n, others):
    """Straight F.Cu link, or a via hop over B.Cu when the straight line would cross a pad."""
    if not crosses(a, b, others):
        track(board, a, b, n)
        return
    for off in (1.0, 1.4, 1.8, -1.0, -1.4):
        va = pcbnew.VECTOR2I(a.x + MM(off), a.y)
        vb = pcbnew.VECTOR2I(b.x + MM(off), b.y)
        if not crosses(a, va, others) and not crosses(vb, b, others):
            track(board, a, va, n)
            via(board, va, n)
            track(board, va, vb, n, layer=pcbnew.B_Cu)
            via(board, vb, n)
            track(board, vb, b, n)
            return
    raise SystemExit(f"no hand route for {n}")


def via(board, p, n):
    v = pcbnew.PCB_VIA(board)
    v.SetPosition(p)
    v.SetDrill(MM(VIA_DRILL))
    v.SetWidth(pcbnew.F_Cu, MM(VIA_D))
    v.SetNet(net(board, n))
    board.Add(v)


def pad_of(board, ref, n):
    fp = board.FindFootprintByReference(ref)
    return [p for p in fp.Pads() if p.GetNetname() == n]


def poly(points):
    sh = pcbnew.SHAPE_LINE_CHAIN()
    for x, y in points:
        sh.Append(MM(x), MM(y))
    sh.SetClosed(True)
    return sh


def rule_area(board, name, pts, layers, keepout=True, pour=False):
    z = pcbnew.ZONE(board)
    z.SetIsRuleArea(True)
    z.SetZoneName(name)
    ls = pcbnew.LSET()
    for la in layers:
        ls.AddLayer(la)
    z.SetLayerSet(ls)
    z.Outline().AddOutline(poly(pts))
    z.SetDoNotAllowTracks(keepout)
    z.SetDoNotAllowVias(keepout)
    z.SetDoNotAllowCopperPour(not pour)
    z.SetDoNotAllowPads(False)
    z.SetDoNotAllowFootprints(False)
    board.Add(z)


def copper_zone(board, n, layer, pts, prio=0):
    z = pcbnew.ZONE(board)
    z.SetLayer(layer)
    z.SetNet(net(board, n))
    z.Outline().AddOutline(poly(pts))
    z.SetAssignedPriority(prio)
    z.SetMinThickness(MM(0.2))
    z.SetLocalClearance(MM(0.3))
    z.SetPadConnection(pcbnew.ZONE_CONNECTION_FULL)
    board.Add(z)


CU = [pcbnew.F_Cu, pcbnew.In1_Cu, pcbnew.In2_Cu, pcbnew.B_Cu]


def ground_vias(board, cell):
    """One via per ground pad, offset away from its part, with a short stub."""
    planes = cell["planes"]
    bubbles = [z.GetBoundingBox() for z in board.Zones() if z.GetIsRuleArea() and z.GetZoneName().startswith("BUBBLE")]
    for b in bubbles:
        b.Inflate(MM(0.6))  # once: BOX2I.Inflate changes the box in place
    for fp in board.GetFootprints():
        port = fp.GetReference().startswith("P-")
        c = fp.GetPosition()
        for pad in fp.Pads():
            n = pad.GetNetname()
            if n not in planes or not pad.IsOnLayer(pcbnew.F_Cu):
                continue
            if fp.GetReference() == cell.get("x2y") and n == cell.get("gnd2"):
                continue  # the X2Y isolated-ground terminals use the In2 crossing
            p = pad.GetPosition()
            if port:  # port pads: via inboard of the pad
                side = 1 if p.x < MM(cell["moat_x"]) else -1
                q = pcbnew.VECTOR2I(p.x + side * MM(1.6), p.y)
                via(board, q, n)
                track(board, p, q, n)
                continue
            if fp.GetReference() == cell.get("fanout") and pad.GetNumber() != "49":
                continue  # the QFN pins get their vias from fanout_qfn()
            if pad.GetNumber() == "49" and fp.GetReference() == "1553-XCVR":
                for dx, dy in ((-1, -1), (1, -1), (-1, 1), (1, 1)):
                    via(board, pcbnew.VECTOR2I(p.x + MM(1.2 * dx), p.y + MM(1.2 * dy)), n)
                continue
            dx, dy = p.x - c.x, p.y - c.y
            if abs(dx) < MM(0.05) and abs(dy) < MM(0.05):
                dx, dy = 0, MM(1)
            L = math.hypot(dx, dy)
            half = max(pad.GetSize().x, pad.GetSize().y) / 2
            off = half + MM(0.75)
            q = pcbnew.VECTOR2I(int(p.x + dx / L * off), int(p.y + dy / L * off))
            if any(b.Contains(q) for b in bubbles):
                # inside the sec 13.1 keep-out: join the nearest same-net pin of this part
                mates = [m for m in fp.Pads() if m.GetNetname() == n and m.GetNumber() != pad.GetNumber()]
                if mates:
                    m = min(mates, key=lambda m: (m.GetPosition() - p).EuclideanNorm())
                    track(board, p, m.GetPosition(), n)
                    continue
                # no mate: via inboard of the pad, under the package body
                q = pcbnew.VECTOR2I(int(p.x - dx / L * (half + MM(0.5))), int(p.y - dy / L * (half + MM(0.5))))
                via(board, q, n)
                track(board, p, q, n)
                continue
            via(board, q, n)
            track(board, p, q, n)


def fanout_qfn(board, ref, planes=("GND",)):
    """Manual fan-out for the 0.4 mm-pitch QFN: straight out, then spread to 1.0 mm pitch."""
    fp = board.FindFootprintByReference(ref)
    c = fp.GetPosition()
    sides = {}
    for pad in fp.Pads():
        n = pad.GetNetname()
        if not n or pad.GetNumber() == "49":
            continue
        p = pad.GetPosition()
        dx, dy = (p.x - c.x) / 1e6, (p.y - c.y) / 1e6
        side = ("L" if dx < 0 else "R") if abs(dx) > abs(dy) else ("T" if dy < 0 else "B")
        sides.setdefault(side, []).append((pad, dx, dy))
    for side, pads in sides.items():
        along = (lambda t: t[2]) if side in "LR" else (lambda t: t[1])
        pads.sort(key=along)
        n = len(pads)
        centre = sum(along(t) for t in pads) / n
        for i, (pad, dx, dy) in enumerate(pads):
            if pad.GetNetname() == "GND":
                # ground pins tie straight inward to the grounded exposed pad (pad 49)
                ix, iy = (math.copysign(2.0, dx), dy) if side in "LR" else (dx, math.copysign(2.0, dy))
                track(board, pad.GetPosition(), pcbnew.VECTOR2I(c.x + MM(ix), c.y + MM(iy)), "GND", w=FINE_TRACK)
                continue
            spread = centre + (i - (n - 1) / 2) * 1.0
            spread = max(-4.2, min(4.2, spread))
            out1, out2 = 3.55, 5.6
            if side == "L":
                pts = [(-out1, dy), (-out2, spread)]
            elif side == "R":
                pts = [(out1, dy), (out2, spread)]
            elif side == "T":
                pts = [(dx, -out1), (spread, -out2)]
            else:
                pts = [(dx, out1), (spread, out2)]
            prev = pad.GetPosition()
            for x, y in pts:
                q = pcbnew.VECTOR2I(c.x + MM(x), c.y + MM(y))
                track(board, prev, q, pad.GetNetname(), w=FINE_TRACK)
                prev = q
            if pad.GetNetname() in planes:
                via(board, prev, pad.GetNetname())


def hand_copper(board, cell):
    """Copper drawn by this script, not the router: converter-side links, ground vias, the
    X2Y crossing and the QFN fan-out.  Drawn before routing (as obstacles) and again after
    the session import, which replaces every track on the board."""
    W, H = cell["size"]
    mx = cell["moat_x"]
    m1 = mx + MOAT_W / 2
    x2y = cell.get("x2y")
    for n in cell["hand_nets"]:
        pads = [p for fp in board.GetFootprints() for p in fp.Pads() if p.GetNetname() == n]
        others = [p for fp in board.GetFootprints() for p in fp.Pads() if p.GetNetname() not in (n, "")]
        done, todo = [pads[0]], pads[1:]
        while todo:
            a, b = min(((x, y) for x in done for y in todo),
                       key=lambda xy: (xy[0].GetPosition() - xy[1].GetPosition()).EuclideanNorm())
            link(board, a.GetPosition(), b.GetPosition(), n, others)
            done.append(b)
            todo.remove(b)
    ground_vias(board, cell)
    if x2y:
        g = cell["gnd2"]
        a, b = pad_of(board, x2y, g)
        track(board, a.GetPosition(), b.GetPosition(), g)
        low = max((a, b), key=lambda p: p.GetPosition().y).GetPosition()
        v1 = pcbnew.VECTOR2I(low.x, MM(H - 2.3))
        v2 = pcbnew.VECTOR2I(MM(m1 + 1.6), MM(H - 2.3))
        track(board, low, v1, g)
        via(board, v1, g)
        track(board, v1, v2, g, layer=pcbnew.In2_Cu)
        via(board, v2, g)
    if cell.get("fanout"):
        fanout_qfn(board, cell["fanout"], tuple(cell["planes"]))


def build(cell, router: bool):
    board = pcbnew.BOARD()
    board.SetCopperLayerCount(4)
    ds = board.GetDesignSettings()
    ds.SetBoardThickness(MM(1.6))
    W, H = cell["size"]
    for a, b in (((0, 0), (W, 0)), ((W, 0), (W, H)), ((W, H), (0, H)), ((0, H), (0, 0))):
        s = pcbnew.PCB_SHAPE(board)
        s.SetShape(pcbnew.SHAPE_T_SEGMENT)
        s.SetStart(pcbnew.VECTOR2I(MM(a[0]), MM(a[1])))
        s.SetEnd(pcbnew.VECTOR2I(MM(b[0]), MM(b[1])))
        s.SetLayer(pcbnew.Edge_Cuts)
        s.SetWidth(MM(0.1))
        board.Add(s)
    for ref, (x, y, r) in cell["place"].items():
        place(board, ref, x, y, r, cell["orient"].get(ref))
    port_row(board, "P-LOGIC", cell["ports_logic"], 2.4, 4.0)
    port_row(board, "P-FIELD", cell["ports_field"], W - 2.4, H - 2.4)
    mx = cell["moat_x"]
    m0, m1 = mx - MOAT_W / 2, mx + MOAT_W / 2
    x2y = cell.get("x2y")
    # moat: every layer; In2 keeps an opening for the X2Y ground-terminal crossing
    for la in CU:
        gap = (H - 3.0, H - 1.6) if (x2y and la == pcbnew.In2_Cu) else None
        for r in moat_rects(cell.get("moat_path", [(mx, 0), (mx, H)]), gap):
            rule_area(board, "ISOLATION_MOAT", r, [la])
    if "bubble" in cell:
        iso, pins, name = cell["bubble"]
        fp = board.FindFootprintByReference(iso)
        ps = [p for p in fp.Pads() if p.GetNumber() in pins]
        x0 = max(p.GetBoundingBox().GetRight() for p in ps) / 1e6 + 0.2
        y0 = min(p.GetBoundingBox().GetTop() for p in ps) / 1e6 - 4.0
        y1 = max(p.GetBoundingBox().GetBottom() for p in ps) / 1e6 + 4.0
        x1 = x0 - 0.2 + 4.0
        rule_area(board, name, [(x0, y0), (x1, y0), (x1, y1), (x0, y1)], CU, keepout=router)
    if router:
        # router-only edge band: the DSN boundary does not carry KiCad's 0.5 mm edge clearance
        e = 0.7
        for r in ([(0, 0), (W, 0), (W, e), (0, e)], [(0, H - e), (W, H - e), (W, H), (0, H)],
                  [(0, 0), (e, 0), (e, H), (0, H)], [(W - e, 0), (W, 0), (W, H), (W - e, H)]):
            rule_area(board, "EDGE_BAND", r, CU)
    if cell.get("fanout") and not router:
        # DRC-only area: the DSN export turns every rule area into a router keep-out
        fp = board.FindFootprintByReference(cell["fanout"])
        cx, cy = fp.GetPosition().x / 1e6, fp.GetPosition().y / 1e6
        rule_area(board, "FANOUT_1553", [(cx - 6.0, cy - 6.0), (cx + 6.0, cy - 6.0), (cx + 6.0, cy + 6.0), (cx - 6.0, cy + 6.0)],
                  CU, keepout=False, pour=True)
    if router:
        hand_copper(board, cell)
    if not router:
        path = [(x, y) for x, y, *_ in cell.get("moat_path", [(mx, 0), (mx, H)])]
        inner = [(x, min(max(y, 0.3), H - 0.3)) for x, y in path]
        logic = [(0.3, 0.3)] + inner + [(0.3, H - 0.3)]
        field = [(W - 0.3, 0.3)] + inner + [(W - 0.3, H - 0.3)]
        for n, where in cell["planes"].items():
            # the moat keep-out (no pour) and the 0.5 mm barrier rule clear each plane off the path
            layer = pcbnew.In2_Cu if cell.get("plane_layer", {}).get(n) == "In2" else pcbnew.In1_Cu
            copper_zone(board, n, layer, logic if where == "logic" else field)
    return board


NETCLASS_PATTERNS = [("POWER", r"^(\+5V|\+3V3|GND.*|VCC2.*|PGND)$")]


def netclasses(board, cell):
    """Default 0.3 mm clearance; POWER 0.4 mm tracks; ISOLATION for the field-side nets
    (same 0.3 mm, the 0.5 mm barrier is the DRU rule).  Set through pcbnew so the DSN
    export and the saved project carry them."""
    ds = board.GetDesignSettings()
    ds.m_MinClearance = MM(0.3)
    ns = ds.m_NetSettings
    d = ns.GetDefaultNetclass()
    for nc, w in ((d, TRACK),):
        nc.SetClearance(MM(0.3))
        nc.SetTrackWidth(MM(w))
        nc.SetViaDiameter(MM(VIA_D))
        nc.SetViaDrill(MM(VIA_DRILL))
    for name, w in (("POWER", POWER_TRACK), ("ISOLATION", TRACK)):
        nc = pcbnew.NETCLASS(name)
        nc.SetClearance(MM(0.3))
        nc.SetTrackWidth(MM(w))
        nc.SetViaDiameter(MM(VIA_D))
        nc.SetViaDrill(MM(VIA_DRILL))
        ns.SetNetclass(name, nc)
    for n in sorted(field_nets(cell)):
        ns.SetNetclassPatternAssignment(re.escape(n), "ISOLATION")
    for name, pat in NETCLASS_PATTERNS:
        ns.SetNetclassPatternAssignment(pat, name)
    ns.RecomputeEffectiveNetclasses()
    board.SynchronizeNetsAndNetClasses(True)


def patch_project(path: Path):
    """Footprint-library checks off: the cells hold two synthetic port footprints and the
    Serenity-Custom library is not checked out in CI."""
    pro = json.loads(path.read_text())
    sev = pro.setdefault("board", {}).setdefault("design_settings", {}).setdefault("rule_severities", {})
    sev.update({"lib_footprint_issues": "ignore", "lib_footprint_mismatch": "ignore"})
    path.write_text(json.dumps(pro, indent=2) + "\n")


def save(board, cell, name):
    d = CELLS / cell["name"]
    d.mkdir(parents=True, exist_ok=True)
    pcb = d / f"{name}.kicad_pcb"
    netclasses(board, cell)
    pcbnew.SaveBoard(str(pcb), board)
    patch_project(d / f"{name}.kicad_pro")
    shutil.copy(DRU, d / f"{name}.kicad_dru")
    return pcb


def strip_hand_nets(dsn: Path, nets):
    """Drop hand-routed and plane nets from the DSN network so the router leaves them alone."""
    text = dsn.read_text()
    for n in nets:
        text = re.sub(r'\(net "?' + re.escape(n) + r'"?\s*\(pins[^)]*\)\s*\)', "", text)
    dsn.write_text(text)


def fine_class(dsn: Path, nets, clearance_um=200, width_um=250):
    """Router-only: give the fan-out part's nets a 0.2 mm clearance class.  The fixed
    0.4 mm-pitch fan-out wires sit 0.25 mm apart, which the router otherwise reads as a
    0.3 mm violation and refuses to route from.  KiCad's DRC keeps 0.3 mm outside the
    documented FANOUT area, so any router shortcut there still fails the gate."""
    text = dsn.read_text()
    nets = set(nets)

    def strip(m):
        head, body = m.group(1), m.group(2)
        toks = head.split()
        keep = [toks[0]] + [t for t in toks[1:] if t.strip('"') not in nets]
        return "(class " + " ".join(keep) + "\n" + body
    text = re.sub(r"\(class ([^(]*?)\n?(\s*\(circuit)", strip, text, flags=re.S)
    block = ("    (class FINE " + " ".join(f'"{n}"' for n in sorted(nets)) +
             '\n      (circuit (use_via "Via[0-3]_600:300_um"))\n'
             f"      (rule (width {width_um}) (clearance {clearance_um}))\n    )\n")
    i = text.rindex("(class ")
    text = text[:i] + block + "    " + text[i:]
    # the structure rule sets the clearance of the QFN's no-net pads
    text = re.sub(r"(\(structure.*?\(rule\s*\(width \d+\)\s*\(clearance )\d+", rf"\g<1>{clearance_um}", text, count=1, flags=re.S)
    dsn.write_text(text)


def main() -> None:
    stage, name = sys.argv[1], sys.argv[2]
    cell = DEFS[name]
    if stage == "place":
        pcb = save(build(cell, router=True), cell, "route")
        b = pcbnew.LoadBoard(str(pcb))
        dsn = pcb.with_suffix(".dsn")
        pcbnew.ExportSpecctraDSN(b, str(dsn))
        strip_hand_nets(dsn, list(cell["planes"]) + cell["hand_nets"])
        print(f"wrote {dsn}")
    elif stage == "finish":
        board = build(cell, router=False)
        pcb = save(board, cell, name)
        board = pcbnew.LoadBoard(str(pcb))
        if not pcbnew.ImportSpecctraSES(board, sys.argv[3]):
            raise SystemExit("session import failed")
        hand_copper(board, cell)
        pcbnew.ZONE_FILLER(board).Fill(board.Zones())
        pcbnew.SaveBoard(str(pcb), board)
        patch_project(pcb.with_suffix(".kicad_pro"))
        for f in (CELLS / name).glob("route.*"):
            f.unlink()
        print(f"wrote {pcb}")


if __name__ == "__main__":
    main()
