#!/usr/bin/env python3
# SPDX-License-Identifier: CERN-OHL-W-2.0 (hardware-generating script; licence-by-output rule, Serenity-UAV AGENTS.md §3)
"""Generate the NoNFO-Pilot-PB2 footprints that no verified library footprint covers.

Every dimension below is transcribed from the OEM land-pattern drawing named in the footprint's
docstring; nothing is scaled from a neighbouring package. Output: ../kicads/NoNFO-PB2.pretty/.
Run under KiCad 9.0.2's Python only to *check* the result (tests/test_footprints.py loads each
file with pcbnew); generation itself is plain Python.

Drafted by Claude (Anthropic) for S. Griffing, sprint S35, 2026-11-17.
"""

from __future__ import annotations

import uuid
from pathlib import Path

OUT = Path(__file__).resolve().parents[1] / "kicads" / "NoNFO-PB2.pretty"
NS = uuid.UUID("6f1d3c2e-5a1b-4c7d-9e8f-0a1b2c3d4e5f")  # stable pad UUIDs per footprint


def _u(*parts: object) -> str:
    return str(uuid.uuid5(NS, "/".join(map(str, parts))))


def pad(
    fp: str, num: str, x: float, y: float, w: float, h: float, shape: str = "roundrect"
) -> str:
    rr = "(roundrect_rratio 0.25) " if shape == "roundrect" else ""
    return (
        f'\t(pad "{num}" smd {shape} (at {x:.4f} {y:.4f}) (size {w:.4f} {h:.4f}) '
        f'(layers "F.Cu" "F.Paste" "F.Mask") {rr}(uuid "{_u(fp, num, x, y)}"))'
    )


def rect(
    layer: str, x0: float, y0: float, x1: float, y1: float, width: float = 0.1
) -> str:
    return (
        f"\t(fp_rect (start {x0:.4f} {y0:.4f}) (end {x1:.4f} {y1:.4f}) "
        f'(stroke (width {width}) (type solid)) (fill no) (layer "{layer}") '
        f'(uuid "{_u(layer, x0, y0, x1, y1)}"))'
    )


def text(kind: str, value: str, y: float, layer: str) -> str:
    return (
        f'\t(property "{kind}" "{value}" (at 0 {y:.3f} 0) (layer "{layer}") '
        f'(uuid "{_u(kind, value)}") (effects (font (size 0.8 0.8) (thickness 0.12))))'
    )


def dot(x: float, y: float) -> str:
    return (
        f"\t(fp_circle (center {x:.4f} {y:.4f}) (end {x + 0.15:.4f} {y:.4f}) "
        f'(stroke (width 0.12) (type solid)) (fill yes) (layer "F.SilkS") (uuid "{_u("dot", x, y)}"))'
    )


def write(
    name: str,
    descr: str,
    pads: list[str],
    body: tuple[float, float, float, float],
    crt_margin: float,
    extra: list[str] | None = None,
) -> Path:
    """Write one footprint; a pin-1 dot goes just outside the body's top-left corner."""
    x0, y0, x1, y1 = body
    extra = [dot(x0 - 0.45, y0 - 0.45), *(extra or [])]
    lines = [
        f'(footprint "{name}"',
        "\t(version 20241229)",
        '\t(generator "gen_nonfo_pb2_footprints")',
        '\t(layer "F.Cu")',
        f'\t(descr "{descr}")',
        text("Reference", "REF**", y0 - 1.0, "F.SilkS"),
        text("Value", name, y1 + 1.0, "F.Fab"),
        "\t(attr smd)",
        rect("F.Fab", x0, y0, x1, y1),
        rect(
            "F.CrtYd",
            x0 - crt_margin,
            y0 - crt_margin,
            x1 + crt_margin,
            y1 + crt_margin,
            0.05,
        ),
        *(extra or []),
        *pads,
        ")",
    ]
    OUT.mkdir(parents=True, exist_ok=True)
    p = OUT / f"{name}.kicad_mod"
    p.write_text("\n".join(lines) + "\n")
    return p


def lwb5plus() -> Path:
    """Ezurio Sterling-LWB5+ 453-00045/46/47, 17 x 12 mm LGA, 68 pads.

    Source: Ezurio Sterling LWB5+ data sheet v5.2 (REF-SENSOR-066), "Mechanical Drawings",
    TOP VIEW "The PCB footprint recommend" (PDF p.25). Origin = module outline lower-left,
    +X along the 17.00 mm edge, +Y up; converted to KiCad (+Y down) about the outline centre.
    Edge pads 0.40 x 1.00 mm at 0.66 mm pitch; bottom/top rows overhang the outline 0.10 mm;
    corner pads G1/G2 1.00 x 1.00 mm, outer edge 0.075 mm inside the right outline; right
    column pin-19/33 centres 0.98 mm from the G1/G2 centres; G3..G8 at 1.125 mm, 1.35 mm to the
    first signal pad; G9..G17 1.20 mm squares on a 2.50 mm grid, G10 centre 5.69 mm from the
    right outline and G13 centre 6.00 mm below the top outline. The drawing closes to
    within 0.025 mm (G5 left edge 0.425 vs the 0.40 shown); positions are anchored to G1.
    """
    name = "Ezurio_LWB5plus_LGA-68_17x12mm"
    W, H = 17.0, 12.0
    p: list[str] = []

    def at(x: float, y: float) -> tuple[float, float]:  # drawing frame -> KiCad frame
        return x - W / 2, H / 2 - y

    g1x, row_y = W - 0.075 - 0.5, -0.10 + 0.5
    pin18 = g1x - 0.98
    xs = [pin18 - (17 - i) * 0.66 for i in range(18)]  # pins 1..18 left to right
    for i, x in enumerate(xs):
        p.append(pad(name, str(i + 1), *at(x, row_y), 0.40, 1.00))
        p.append(
            pad(name, str(51 - i), *at(x, H - row_y), 0.40, 1.00)
        )  # top row 51..34
    for i in range(15):  # right column 19 (bottom) .. 33 (top)
        y = row_y + 0.98 + i * 0.66
        p.append(pad(name, str(19 + i), *at(g1x, y), 1.00, 0.40))
    p.append(pad(name, "G1", *at(g1x, row_y), 1.00, 1.00))
    p.append(pad(name, "G2", *at(g1x, H - row_y), 1.00, 1.00))
    gx = [xs[0] - 1.35 - k * 1.125 for k in range(3)]  # G8/G3, G7/G4, G6/G5
    for k, x in enumerate(gx):
        p.append(pad(name, f"G{8 - k}", *at(x, row_y), 0.40, 1.00))
        p.append(pad(name, f"G{3 + k}", *at(x, H - row_y), 0.40, 1.00))
    g10x, g13y = W - 5.69, H - 6.00
    for r, y in enumerate((g13y + 2.5, g13y, g13y - 2.5)):
        for c, x in enumerate((g10x - 2.5, g10x, g10x + 2.5)):
            p.append(pad(name, f"G{9 + 3 * r + c}", *at(x, y), 1.20, 1.20, "rect"))
    keep = rect(
        "Cmts.User", -W / 2, H / 2 - 1.13 - 8.0, -W / 2 + 5.0, H / 2 - 1.13, 0.05
    )
    return write(
        name,
        "Ezurio Sterling-LWB5+ 453-00045/46/47 LGA, 17x12 mm, per data sheet "
        "v5.2 recommended footprint (REF-SENSOR-066). Cmts.User box: chip-antenna "
        "keep-out (not needed for the 453-00046 MHF4 variant)",
        p,
        (-W / 2, -H / 2, W / 2, H / 2),
        0.35,
        [keep],
    )


def usb2641i() -> Path:
    """Microchip USB2641i 48-pin VQFN 7 x 7 mm (HZH), 0.50 mm pitch, exposed pad variant C.

    Source: Microchip DS00001948C, Figure 11-1 sheet 2, RECOMMENDED LAND PATTERN (drawing
    C04-2223B): C1 = C2 6.90 (pad centre to pad centre across the package), X1 0.30 max,
    Y1 0.85 max, E 0.50, centre pad X2 = Y2 4.20 (variant C, the note says "This product is a
    variant 'C'"). Pin 1 heads the left column at the marked corner; pins run counter-clockwise.
    """
    name = "Microchip_VQFN-48-1EP_7x7mm_P0.5mm_EP4.2x4.2mm"
    c, px, py, e = 6.90 / 2, 0.30, 0.85, 0.50
    p: list[str] = []
    offs = [(-5.5 + i) * e for i in range(12)]
    for i, o in enumerate(offs):
        p.append(pad(name, str(1 + i), -c, o, py, px))  # left, top->bottom
        p.append(pad(name, str(13 + i), o, c, px, py))  # bottom, left->right
        p.append(pad(name, str(25 + i), c, -o, py, px))  # right, bottom->top
        p.append(pad(name, str(37 + i), -o, -c, px, py))  # top, right->left
    p.append(pad(name, "49", 0, 0, 4.20, 4.20, "rect"))
    return write(
        name,
        "Microchip USB2641i VQFN-48 7x7 mm (HZH), DS00001948C Fig 11-1 land pattern "
        "variant C",
        p,
        (-3.5, -3.5, 3.5, 3.5),
        0.4,
    )


def ti_dsk0010a() -> Path:
    """TI DSK0010A WSON-10 2.5 x 2.5 mm (TPS6303x), replaces TACCO's flagged TPS6303x_VSON-10_2p5.

    Source: TI TPS63031 data sheet, "DSK0010A EXAMPLE BOARD LAYOUT" (PDF p.25, 4218903/C
    09/2025): 10X pads 0.6 x 0.25, 8X pitch 0.5, the two pad columns 2.3 apart centreline to
    centreline, thermal pad 1.2 x 2.0, pins 1-5 down the left, 6-10 up the right.
    """
    name = "TI_DSK0010A_WSON-10-1EP_2.5x2.5mm_P0.5mm_EP1.2x2mm"
    cx = 2.3 / 2
    p: list[str] = []
    for i in range(5):
        y = (-2 + i) * 0.5
        p.append(pad(name, str(1 + i), -cx, y, 0.6, 0.25))
        p.append(pad(name, str(10 - i), cx, y, 0.6, 0.25))
    p.append(pad(name, "11", 0, 0, 1.2, 2.0, "rect"))
    return write(
        name,
        "TI DSK0010A WSON-10 2.5x2.5 mm (TPS6303x), TPS63031 data sheet example "
        "board layout 4218903/C",
        p,
        (-1.25, -1.25, 1.25, 1.25),
        0.35,
    )


def main() -> None:
    for f in (lwb5plus, usb2641i, ti_dsk0010a):
        print("wrote", f().relative_to(OUT.parents[1]))


if __name__ == "__main__":
    main()
