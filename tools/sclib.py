#!/usr/bin/env python3
"""Build and check the shared SecureControllers KiCad symbol library.

Source of truth
---------------
One TOML spec per part in ``kicad/libraries/parts/<MPN>.toml``.  Each spec
records the manufacturer datasheet, the exact table/figure the pin map was
verified against, every package option the datasheet offers, and the
pin list grouped by symbol side.  This script turns the specs into

* ``kicad/libraries/SecureControllers.kicad_sym`` -- KiCad 9 symbol library
  (library nickname ``SecureControllers``), and
* ``kicad/libraries/VERIFICATION.md`` -- the human-readable verification
  and package-options ledger.

Why generated, not hand-drawn
-----------------------------
* Every pin endpoint lands on the 100 mil (2.54 mm) grid, so ERC's
  ``endpoint_off_grid`` cannot originate in this library.
* Symbol names are the manufacturer part number (never a board name or a
  reference designator), so any board can reuse any symbol.  Board-scoped
  names (``Observer_ISOW1044BDFMR``, ``S_C-485-1``) were the root cause of
  copy drift found on 2026-09-26.
* Pin electrical types come from the datasheet, not ``passive``, so ERC's
  driver/power checks actually run.

Pin line grammar (TOML string)::

    "<number> <name> <type>[ ~]"      ~ = hidden pin (stacked GND etc.)

``<type>``: W power_in, w power_out, I input, O output, B bidirectional,
P passive, N no_connect, T tri_state, C open_collector, E open_emitter,
F free, U unspecified.  An empty string leaves a one-pitch gap.

Usage::

    python3 tools/sclib.py build     # regenerate library + ledger
    python3 tools/sclib.py check     # exit 1 if regeneration would differ

Attribution: authored by Claude Opus 5.5 (Anthropic) for the
SecureControllers library, 2026-09-26.  File-format reference: KiCad
Developer Documentation, "Symbol Library File Format" [REF-KICAD-FMT].
"""

import argparse
import pathlib
import re
import sys
import tomllib

ROOT = pathlib.Path(__file__).resolve().parent.parent
LIB_DIR = ROOT / "kicad" / "libraries"
PARTS_DIR = LIB_DIR / "parts"
SYM_OUT = LIB_DIR / "SecureControllers.kicad_sym"
LEDGER_OUT = LIB_DIR / "VERIFICATION.md"
NICK = "SecureControllers"

GRID = 2.54          # pin pitch and pin length, 100 mil
CHAR_W = 1.27 * 0.6  # approximate width of one 1.27 mm glyph, mm
TYPES = {
    "W": "power_in", "w": "power_out", "I": "input", "O": "output",
    "B": "bidirectional", "P": "passive", "N": "no_connect",
    "T": "tri_state", "C": "open_collector", "E": "open_emitter",
    "F": "free", "U": "unspecified",
}


def q(text):
    """Quote a string for a KiCad S-expression."""
    return '"' + str(text).replace("\\", "\\\\").replace('"', '\\"') + '"'


def snap(v):
    """Round *v* up to the next multiple of GRID (keeps pins on grid)."""
    n = int(v / GRID)
    return (n if abs(n * GRID - v) < 1e-9 else n + 1) * GRID


def parse_pin(line):
    """Return (number, name, etype, hidden) or None for a gap."""
    if not line.strip():
        return None
    hidden = line.rstrip().endswith("~")
    parts = line.replace("~", "").split()
    if len(parts) != 3 or parts[2] not in TYPES:
        raise ValueError("bad pin line %r" % line)
    return parts[0], parts[1], TYPES[parts[2]], hidden


def load_specs():
    """Load every part spec, sorted by symbol name."""
    specs = []
    for f in sorted(PARTS_DIR.glob("*.toml")):
        with f.open("rb") as fh:
            s = tomllib.load(fh)
        s["_file"] = f.name
        specs.append(s)
    names = [s["symbol"]["name"] for s in specs]
    dup = {n for n in names if names.count(n) > 1}
    if dup:
        raise SystemExit("duplicate symbol names: %s" % sorted(dup))
    return specs


def render_symbol(spec):
    """Return the S-expression text for one symbol."""
    sym = spec["symbol"]
    name = sym["name"]
    sides = {k: [parse_pin(p) for p in spec["pins"].get(k, [])]
             for k in ("left", "right", "top", "bottom")}

    # Every pin number must be unique across the symbol.
    nums = [p[0] for side in sides.values() for p in side if p]
    dup = {n for n in nums if nums.count(n) > 1}
    if dup:
        raise SystemExit("%s: duplicate pin numbers %s" % (name, sorted(dup)))

    def longest(side):
        return max([len(p[1]) for p in sides[side] if p] or [0])

    # Body size: vertical extent from the taller of left/right, horizontal
    # from name lengths (or top/bottom pin count), both snapped to grid.
    rows = max(len(sides["left"]), len(sides["right"]), 1)
    cols = max(len(sides["top"]), len(sides["bottom"]), 0)
    half_h = snap((rows + 1) * GRID / 2)
    width = (longest("left") + longest("right")) * CHAR_W + 4 * GRID
    half_w = snap(max(width, (cols + 1) * GRID, 4 * GRID) / 2)
    if sides["top"] or sides["bottom"]:
        half_h = max(half_h, snap((longest("top") + longest("bottom"))
                                  * CHAR_W / 2 + 2 * GRID))

    out = []
    w = out.append
    w("\t(symbol %s" % q(name))
    w("\t\t(pin_names (offset 1.016))")
    w("\t\t(exclude_from_sim no)")
    w("\t\t(in_bom %s)" % ("yes" if sym.get("in_bom", True) else "no"))
    w("\t\t(on_board yes)")
    props = [
        ("Reference", sym["reference"], (-half_w, half_h + 1.27), False),
        ("Value", name, (-half_w, -half_h - 1.27), False),
        ("Footprint", sym.get("footprint", ""), (0, 0), True),
        ("Datasheet", spec["datasheet"]["url"], (0, 0), True),
        ("Description", sym["description"], (0, 0), True),
        ("Manufacturer", sym.get("manufacturer", ""), (0, 0), True),
        ("MPN", sym.get("mpn", name), (0, 0), True),
        ("ki_keywords", sym.get("keywords", ""), (0, 0), True),
    ]
    if sym.get("fp_filters"):
        props.append(("ki_fp_filters", sym["fp_filters"], (0, 0), True))
    for key, val, (x, y), hide in props:
        just = " (justify left)" if key in ("Reference", "Value") else ""
        w("\t\t(property %s %s" % (q(key), q(val)))
        w("\t\t\t(at %.2f %.2f 0)" % (x, y))
        w("\t\t\t(effects (font (size 1.27 1.27))%s%s)"
          % (just, " (hide yes)" if hide else ""))
        w("\t\t)")

    # Unit 0 style 1: body rectangle.
    w("\t\t(symbol %s" % q(name + "_0_1"))
    w("\t\t\t(rectangle (start %.2f %.2f) (end %.2f %.2f)"
      % (-half_w, half_h, half_w, -half_h))
    w("\t\t\t\t(stroke (width 0.254) (type default))")
    w("\t\t\t\t(fill (type background))")
    w("\t\t\t)")
    w("\t\t)")

    # Unit 1 style 1: pins.  Pin (at) is the connection point; the angle
    # points from the connection point toward the body.
    w("\t\t(symbol %s" % q(name + "_1_1"))

    def emit(pin, x, y, angle):
        num, pname, etype, hidden = pin
        w("\t\t\t(pin %s line" % etype)
        w("\t\t\t\t(at %.2f %.2f %d)" % (x, y, angle))
        w("\t\t\t\t(length %.2f)%s" % (GRID, " (hide yes)" if hidden else ""))
        w("\t\t\t\t(name %s (effects (font (size 1.27 1.27))))" % q(pname))
        w("\t\t\t\t(number %s (effects (font (size 1.27 1.27))))" % q(num))
        w("\t\t\t)")

    top_y = half_h - GRID
    for i, p in enumerate(sides["left"]):
        if p:
            emit(p, -half_w - GRID, top_y - i * GRID, 0)
    for i, p in enumerate(sides["right"]):
        if p:
            emit(p, half_w + GRID, top_y - i * GRID, 180)
    left_x = -snap((len(sides["top"]) - 1) * GRID / 2) if sides["top"] else 0
    for i, p in enumerate(sides["top"]):
        if p:
            emit(p, left_x + i * GRID, half_h + GRID, 270)
    left_x = (-snap((len(sides["bottom"]) - 1) * GRID / 2)
              if sides["bottom"] else 0)
    for i, p in enumerate(sides["bottom"]):
        if p:
            emit(p, left_x + i * GRID, -half_h - GRID, 90)
    w("\t\t)")
    w("\t\t(embedded_fonts no)")
    w("\t)")
    return "\n".join(out)


def render_library(specs):
    """Return the complete .kicad_sym text."""
    head = ("(kicad_symbol_lib\n\t(version 20241209)\n"
            "\t(generator \"sclib\")\n\t(generator_version \"9.0\")\n")
    return head + "\n".join(render_symbol(s) for s in specs) + "\n)\n"


STOCK_FP = pathlib.Path("/usr/share/kicad/footprints")
LOCAL_FP = LIB_DIR / "SecureControllers.pretty"


def footprint_pads(fp_id):
    """Return the set of pad numbers of footprint ``Lib:Name``, or None.

    ``SecureControllers:`` resolves to the in-repo ``.pretty``; every other
    nickname resolves to the stock KiCad library of the same name.
    """
    if ":" not in fp_id:
        return None
    lib, name = fp_id.split(":", 1)
    base = LOCAL_FP if lib == NICK else STOCK_FP / (lib + ".pretty")
    path = base / (name + ".kicad_mod")
    if not path.exists():
        return None
    return set(re.findall(r'\(pad "([^"]*)"',
                          path.read_text(encoding="utf-8")))


def check_footprints(specs):
    """Return a list of symbol-to-footprint consistency errors.

    Each symbol pin number must exist as a pad in the footprint; this is
    the check that exposes wrong-package errors such as a 4-pin SOT143B
    part drawn on a 6-pad SOT-363.
    """
    errs = []
    for s in specs:
        fp = s["symbol"].get("footprint", "")
        pads = footprint_pads(fp)
        if pads is None:
            errs.append("%s: footprint %r not found" % (s["symbol"]["name"], fp))
            continue
        pins = {parse_pin(p)[0] for side in s["pins"].values()
                for p in side if parse_pin(p)}
        missing = sorted(pins - pads, key=lambda x: (len(x), x))
        if missing:
            errs.append("%s: pins %s have no pad in %s"
                        % (s["symbol"]["name"], missing, fp))
    return errs


def render_ledger(specs):
    """Return VERIFICATION.md text (package options + pin-map evidence)."""
    lines = [
        "# SecureControllers KiCad library -- verification ledger",
        "",
        "Generated by `tools/sclib.py build` from `kicad/libraries/parts/*.toml`;",
        "do not hand-edit.  Each row records the datasheet table the pin map was",
        "checked against and every package option the datasheet offers, so",
        "smaller or easier-to-route alternatives stay visible.",
        "",
        "| Symbol | Status | Verified against | Footprint (check) | "
        "Packages offered (body) | Recommendation |",
        "| --- | --- | --- | --- | --- | --- |",
    ]
    for s in specs:
        d = s["datasheet"]
        pk = "; ".join("%s %s (%s)" % (p["code"], p["pins"], p["body"])
                       for p in s.get("packages", []))
        fp = "`%s` %s" % (s["symbol"].get("footprint", ""),
                          s.get("footprint_check", "(pad-set only)"))
        lines.append("| %s | %s | [%s](%s) %s | %s | %s | %s |" % (
            s["symbol"]["name"], d.get("status", "verified"), d["doc"],
            d["url"], d["section"], fp, pk or "--",
            s.get("recommendation", "--").replace("\n", " ")))
    lines.append("")
    notes = [s for s in specs if s.get("findings")]
    if notes:
        lines += ["## Findings against existing board copies", ""]
        for s in notes:
            lines.append("### %s" % s["symbol"]["name"])
            lines.append("")
            for f in s["findings"]:
                lines.append("- %s" % f)
            lines.append("")
    return "\n".join(lines)


def main():
    """CLI entry point."""
    ap = argparse.ArgumentParser(description=__doc__.split("\n")[0])
    ap.add_argument("mode", choices=["build", "check"])
    args = ap.parse_args()
    specs = load_specs()
    lib, ledger = render_library(specs), render_ledger(specs)
    fp_errs = check_footprints(specs)
    for e in fp_errs:
        print("FOOTPRINT: " + e)
    if fp_errs:
        return 1
    if args.mode == "check":
        stale = [p.name for p, txt in ((SYM_OUT, lib), (LEDGER_OUT, ledger))
                 if not p.exists() or p.read_text(encoding="utf-8") != txt]
        if stale:
            print("stale: %s -- run tools/sclib.py build" % ", ".join(stale))
            return 1
        print("ok: %d symbols" % len(specs))
        return 0
    SYM_OUT.write_text(lib, encoding="utf-8")
    LEDGER_OUT.write_text(ledger, encoding="utf-8")
    print("wrote %s (%d symbols) and %s" % (SYM_OUT.name, len(specs),
                                            LEDGER_OUT.name))
    return 0


if __name__ == "__main__":
    sys.exit(main())
