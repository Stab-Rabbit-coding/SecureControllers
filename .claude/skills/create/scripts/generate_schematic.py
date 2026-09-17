#!/usr/bin/env python3
"""
generate_schematic.py — AI-powered KiCad 10 schematic creation.

Usage:
    python3 generate_schematic.py \\
        --prompt "ESP32 with USB-C power, LiPo charging, and 4 GPIO LEDs" \\
        --output ~/Documents/KiCad/MyProject/MyProject.kicad_sch

Requires:
    pip install anthropic
    ANTHROPIC_API_KEY environment variable
"""
from __future__ import annotations

import argparse
import json
import os
import re
import sys
import difflib
from pathlib import Path


# ── Symbol library scanner ────────────────────────────────────────────────────

def _find_symbol_dir() -> str:
    candidates = [
        "/Applications/KiCad/KiCad.app/Contents/SharedSupport/symbols",
        "/usr/share/kicad/symbols",
        "/usr/local/share/kicad/symbols",
        os.path.expanduser("~/kicad/symbols"),
    ]
    for c in candidates:
        if os.path.isdir(c):
            return c
    return ""


def _scan_library(lib_file: Path) -> list:
    with open(lib_file, encoding="utf-8", errors="replace") as f:
        content = f.read()
    names = re.findall(r'^\t\(symbol "([^"]+)"', content, re.MULTILINE)
    return [n for n in names if not re.search(r"_\d+_\d+$", n)]


def build_symbol_index(symbol_dir: str) -> dict:
    index: dict = {}
    p = Path(symbol_dir)
    cache = p.parent / ".kicad_create_cache.json"
    if cache.exists():
        try:
            cache_mtime = cache.stat().st_mtime
            newest = max(f.stat().st_mtime for f in p.glob("*.kicad_sym"))
            if cache_mtime > newest:
                with open(cache, encoding="utf-8") as f:
                    return json.load(f)
        except Exception:
            pass
    print("[create] Scanning KiCad symbol libraries…", file=sys.stderr)
    for lib_file in sorted(p.glob("*.kicad_sym")):
        syms = _scan_library(lib_file)
        if syms:
            index[lib_file.stem] = sorted(syms)
    total = sum(len(v) for v in index.values())
    print(f"[create] {total} symbols across {len(index)} libraries.", file=sys.stderr)
    try:
        with open(cache, "w", encoding="utf-8") as f:
            json.dump(index, f, separators=(",", ":"))
    except Exception:
        pass
    return index


class SymbolIndex:
    def __init__(self, index: dict):
        self._index = index
        self._flat: set = {
            f"{lib}:{sym}" for lib, syms in index.items() for sym in syms
        }
        self._lower = {s.lower(): s for s in self._flat}

    def exists(self, lib_id: str) -> bool:
        return lib_id in self._flat

    def search(self, query: str, limit: int = 12) -> list:
        q = query.lower()
        exact = [s for s in self._flat if q == s.lower()]
        if exact:
            return exact[:limit]
        substr = [s for s in self._flat if q in s.lower()]
        substr.sort(key=lambda x: (0 if x.lower().split(":")[-1].startswith(q) else 1, len(x)))
        if substr:
            return substr[:limit]
        return difflib.get_close_matches(query, list(self._flat), n=limit, cutoff=0.5)

    def find_best(self, lib_id: str) -> str:
        if lib_id in self._flat:
            return lib_id
        lower = lib_id.lower()
        if lower in self._lower:
            return self._lower[lower]
        if ":" not in lib_id:
            hits = self.search(lib_id, limit=1)
            return hits[0] if hits else ""
        library, symbol = lib_id.split(":", 1)
        lib_lower = {k.lower(): k for k in self._index}
        actual_lib = lib_lower.get(library.lower(), "")
        if actual_lib:
            m = difflib.get_close_matches(symbol, self._index[actual_lib], n=1, cutoff=0.5)
            if m:
                return f"{actual_lib}:{m[0]}"
        m = difflib.get_close_matches(lib_id, list(self._flat), n=1, cutoff=0.6)
        return m[0] if m else ""

    def validate_and_correct(self, lib_id: str) -> tuple:
        if self.exists(lib_id):
            return lib_id, False, ""
        best = self.find_best(lib_id)
        if best:
            return best, True, f"Auto-corrected '{lib_id}' → '{best}'"
        return lib_id, False, f"No match for '{lib_id}'"

    def prompt_context(self) -> str:
        COMMON = {
            "Device":            "R R_Small C C_Small C_Polarized L D LED Crystal Fuse",
            "power":             "GND +3V3 +5V +12V +3.3V VCC VDD PWR_FLAG",
            "Connector_Generic": "Conn_01x02 Conn_01x03 Conn_01x04 Conn_01x06 Conn_01x08 Conn_02x04",
            "Switch":            "SW_Push SW_SPDT",
            "Transistor_BJT":    "Q_NPN_BCE Q_PNP_BCE",
            "Transistor_FET":    "NMOS PMOS",
            "Regulator_Linear":  "LM7805 AMS1117-3.3",
        }
        lines = [
            "## KiCad 10 Symbol Libraries",
            "ALWAYS call search_symbols before using any lib_id not listed below.",
            "Never invent or guess a symbol name.",
            "",
            "### Pre-verified common symbols (no search needed)",
        ]
        for lib, syms in COMMON.items():
            lines.append(f"  {lib}: {syms}")
        lines += ["", "### All installed libraries"]
        libs = sorted(self._index.keys())
        for i in range(0, len(libs), 5):
            lines.append("  " + "  ".join(libs[i:i + 5]))
        return "\n".join(lines)


# ── Symbol definition extraction ─────────────────────────────────────────────

def _extract_sym_block(content: str, symbol_name: str) -> str:
    search = f'(symbol "{symbol_name}"'
    start = 0
    while True:
        idx = content.find(search, start)
        if idx == -1:
            return ""
        after = content[idx + len(search)] if idx + len(search) < len(content) else ""
        if after in (" ", "\n", "\t", "\r", "(", ")"):
            break
        start = idx + 1
    depth = 0
    for i in range(idx, len(content)):
        if content[i] == "(":
            depth += 1
        elif content[i] == ")":
            depth -= 1
            if depth == 0:
                return content[idx:i + 1]
    return ""


def get_symbol_definition(symbol_dir: str, library: str, symbol: str) -> str:
    lib_file = os.path.join(symbol_dir, f"{library}.kicad_sym")
    if not os.path.exists(lib_file):
        return ""
    with open(lib_file, encoding="utf-8", errors="replace") as f:
        content = f.read()
    raw = _extract_sym_block(content, symbol)
    if not raw:
        return ""
    # Only prefix the root symbol declaration (first occurrence)
    return raw.replace(f'(symbol "{symbol}"', f'(symbol "{library}:{symbol}"', 1)


# ── Schematic file writer ─────────────────────────────────────────────────────

_BLANK_SCHEMATIC = """\
(kicad_sch
  (version 20231120)
  (generator "kicad-happy-create")
  (lib_symbols)
  (sheet_instances (path "/" (page "1")))
)
"""


def _sym_instance(lib, sym, x, y, angle, ref, value, footprint="", datasheet="") -> str:
    return (
        f'  (symbol (lib_id "{lib}:{sym}")\n'
        f'    (at {x:.4f} {y:.4f} {angle:.4f})\n'
        f'    (unit 1)\n'
        f'    (in_bom yes) (on_board yes)\n'
        f'    (property "Reference" "{ref}"\n'
        f'      (at {x:.4f} {y - 2.54:.4f} 0)\n'
        f'      (effects (font (size 1.27 1.27))))\n'
        f'    (property "Value" "{value}"\n'
        f'      (at {x:.4f} {y + 2.54:.4f} 0)\n'
        f'      (effects (font (size 1.27 1.27))))\n'
        f'    (property "Footprint" "{footprint}"\n'
        f'      (at 0 0 0) (effects (font (size 1.27 1.27)) (hide yes)))\n'
        f'    (property "Datasheet" "{datasheet}"\n'
        f'      (at 0 0 0) (effects (font (size 1.27 1.27)) (hide yes)))\n'
        f'  )'
    )


def _power_instance(net, x, y, angle) -> str:
    return (
        f'  (symbol (lib_id "power:{net}")\n'
        f'    (at {x:.4f} {y:.4f} {angle:.4f})\n'
        f'    (unit 1)\n'
        f'    (in_bom yes) (on_board yes)\n'
        f'    (property "Reference" "#PWR?"\n'
        f'      (at 0 0 0) (effects (font (size 1.27 1.27)) (hide yes)))\n'
        f'    (property "Value" "{net}"\n'
        f'      (at {x:.4f} {y + 1.27:.4f} 0)\n'
        f'      (effects (font (size 1.27 1.27))))\n'
        f'  )'
    )


def _wire_instance(sx, sy, ex, ey) -> str:
    return (
        f'  (wire (pts\n'
        f'    (xy {sx:.4f} {sy:.4f})\n'
        f'    (xy {ex:.4f} {ey:.4f})\n'
        f'  ))'
    )


def _label_instance(name, x, y, angle) -> str:
    return (
        f'  (label "{name}"\n'
        f'    (at {x:.4f} {y:.4f} {angle:.4f})\n'
        f'    (effects (font (size 1.27 1.27))))'
    )


def _inject_lib_symbols(content: str, new_defs: list) -> str:
    if not new_defs:
        return content
    block = "\n".join(new_defs)
    if "(lib_symbols" not in content:
        pos = content.find("\n") + 1
        return content[:pos] + f"  (lib_symbols\n{block}\n  )\n" + content[pos:]
    ls = content.find("(lib_symbols")
    depth = 0
    for i in range(ls, len(content)):
        if content[i] == "(":
            depth += 1
        elif content[i] == ")":
            depth -= 1
            if depth == 0:
                return content[:i] + f"\n{block}\n  " + content[i:]
    return content


def write_schematic(output_path: str, symbol_dir: str, sym_index: SymbolIndex,
                    schematic_data: dict) -> dict:
    components    = schematic_data.get("components", [])
    power_symbols = schematic_data.get("power_symbols", [])
    wires         = schematic_data.get("wires", [])
    net_labels    = schematic_data.get("net_labels", [])

    corrections: list = []
    skipped: list = []

    def resolve(library, symbol):
        lib_id = f"{library}:{symbol}"
        corrected, was_fixed, msg = sym_index.validate_and_correct(lib_id)
        if was_fixed:
            corrections.append(msg)
            new_lib, new_sym = corrected.split(":", 1)
            return new_lib, new_sym, True
        if not sym_index.exists(lib_id):
            skipped.append(lib_id)
            return library, symbol, False
        return library, symbol, True

    resolved_comps = []
    for c in components:
        try:
            lib, sym, ok = resolve(c["library"], c["symbol"])
            if ok:
                resolved_comps.append({**c, "library": lib, "symbol": sym})
        except (KeyError, TypeError):
            skipped.append(str(c))

    resolved_pwr = []
    for p in power_symbols:
        try:
            _, sym, ok = resolve("power", p["net"])
            if ok:
                resolved_pwr.append({**p, "net": sym})
        except (KeyError, TypeError):
            pass

    content = _BLANK_SCHEMATIC
    all_pairs = (
        [(c["library"], c["symbol"]) for c in resolved_comps]
        + [("power", p["net"]) for p in resolved_pwr]
    )

    new_defs = []
    seen = set()
    for library, symbol in all_pairs:
        lib_id = f"{library}:{symbol}"
        if lib_id in seen:
            continue
        seen.add(lib_id)
        sym_def = get_symbol_definition(symbol_dir, library, symbol)
        if sym_def:
            new_defs.append(sym_def)

    content = _inject_lib_symbols(content, new_defs)

    body = []
    for c in resolved_comps:
        body.append(_sym_instance(
            c["library"], c["symbol"],
            float(c["x_mm"]), float(c["y_mm"]),
            float(c.get("angle_deg", 0)),
            c["reference"], c["value"],
            c.get("footprint", ""), c.get("datasheet", ""),
        ))
    for p in resolved_pwr:
        body.append(_power_instance(
            p["net"], float(p["x_mm"]), float(p["y_mm"]),
            float(p.get("angle_deg", 0)),
        ))
    for w in wires:
        try:
            if isinstance(w, dict):
                s, e = w["start"], w["end"]
                body.append(_wire_instance(s[0], s[1], e[0], e[1]))
            elif isinstance(w, (list, tuple)) and len(w) == 2:
                body.append(_wire_instance(w[0][0], w[0][1], w[1][0], w[1][1]))
        except (KeyError, TypeError, IndexError):
            pass
    for lbl in net_labels:
        try:
            body.append(_label_instance(
                lbl["name"], float(lbl["x_mm"]), float(lbl["y_mm"]),
                float(lbl.get("angle_deg", 0)),
            ))
        except (KeyError, TypeError):
            pass

    pos = content.rfind("\n)")
    if pos == -1:
        raise RuntimeError("Cannot find insertion point in schematic template.")
    content = content[:pos] + "\n" + "\n".join(body) + "\n" + content[pos:]

    Path(output_path).parent.mkdir(parents=True, exist_ok=True)
    with open(output_path, "w", encoding="utf-8") as f:
        f.write(content)

    return {
        "status": "ok",
        "output": output_path,
        "placed": len(resolved_comps) + len(resolved_pwr),
        "wires": len(wires),
        "labels": len(net_labels),
        "corrections": corrections,
        "skipped": skipped,
    }


# ── Claude agentic loop ───────────────────────────────────────────────────────

_BASE_SYSTEM = """\
You are a principal PCB design engineer with expertise in KiCad 10 schematic capture.

## KiCad 10 coordinate conventions
  • Schematic coordinates in mm. Grid: 1.27 mm (50 mil).
  • Space ICs ~20 mm apart. Keep the schematic tidy.
  • Angles in degrees (0, 90, 180, 270).

## Critical rule — NO unknown symbols
  BEFORE including any library:symbol in a schematic, call search_symbols to
  confirm it exists. Do NOT guess or invent lib_ids. A missing symbol shows as '?'.

## Workflow
  1. Read the circuit description.
  2. List every component type you plan to use.
  3. Call search_symbols for each non-trivial component to get the exact lib_id.
  4. Once ALL lib_ids are verified, call create_schematic exactly once.
"""

_SEARCH_TOOL = {
    "name": "search_symbols",
    "description": (
        "Search installed KiCad 10 symbol libraries. "
        "Returns valid library:symbol identifiers. "
        "ALWAYS call this before using any lib_id not in the pre-verified list."
    ),
    "input_schema": {
        "type": "object",
        "required": ["query"],
        "properties": {
            "query": {"type": "string"},
            "limit": {"type": "integer", "default": 10},
        },
    },
}

_SCHEMATIC_TOOL = {
    "name": "create_schematic",
    "description": "Emit the final schematic after every lib_id is verified.",
    "input_schema": {
        "type": "object",
        "required": ["components", "nets"],
        "properties": {
            "components": {
                "type": "array",
                "items": {
                    "type": "object",
                    "required": ["reference", "value", "library", "symbol", "x_mm", "y_mm"],
                    "properties": {
                        "reference": {"type": "string"},
                        "value":     {"type": "string"},
                        "library":   {"type": "string"},
                        "symbol":    {"type": "string"},
                        "x_mm":      {"type": "number"},
                        "y_mm":      {"type": "number"},
                        "angle_deg": {"type": "number", "default": 0},
                        "footprint": {"type": "string", "default": ""},
                        "datasheet": {"type": "string", "default": ""},
                    },
                },
            },
            "power_symbols": {
                "type": "array",
                "items": {
                    "type": "object",
                    "required": ["net", "x_mm", "y_mm"],
                    "properties": {
                        "net":       {"type": "string"},
                        "x_mm":     {"type": "number"},
                        "y_mm":     {"type": "number"},
                        "angle_deg": {"type": "number", "default": 0},
                    },
                },
            },
            "nets": {
                "type": "array",
                "items": {
                    "type": "object",
                    "required": ["name", "connections"],
                    "properties": {
                        "name": {"type": "string"},
                        "connections": {
                            "type": "array",
                            "items": {
                                "type": "object",
                                "required": ["reference", "pin"],
                                "properties": {
                                    "reference": {"type": "string"},
                                    "pin":       {"type": "string"},
                                },
                            },
                        },
                    },
                },
            },
            "wires": {
                "type": "array",
                "items": {
                    "type": "object",
                    "required": ["start", "end"],
                    "properties": {
                        "start": {"type": "array", "items": {"type": "number"}, "minItems": 2, "maxItems": 2},
                        "end":   {"type": "array", "items": {"type": "number"}, "minItems": 2, "maxItems": 2},
                    },
                },
            },
            "net_labels": {
                "type": "array",
                "items": {
                    "type": "object",
                    "required": ["name", "x_mm", "y_mm"],
                    "properties": {
                        "name":      {"type": "string"},
                        "x_mm":     {"type": "number"},
                        "y_mm":     {"type": "number"},
                        "angle_deg": {"type": "number", "default": 0},
                    },
                },
            },
        },
    },
}


def run_agentic_loop(prompt: str, sym_index: SymbolIndex,
                     model: str = "claude-sonnet-4-6") -> tuple:
    try:
        import anthropic
    except ImportError:
        raise RuntimeError(
            "anthropic package not installed.\n"
            "Run: pip install anthropic"
        )

    api_key = os.environ.get("ANTHROPIC_API_KEY", "")
    if not api_key:
        raise RuntimeError(
            "ANTHROPIC_API_KEY environment variable not set.\n"
            "Get a key at https://console.anthropic.com/settings/keys"
        )

    client = anthropic.Anthropic(api_key=api_key)
    system_text = _BASE_SYSTEM + "\n\n" + sym_index.prompt_context()

    user_message = (
        f"Design a production-ready KiCad 10 schematic for:\n\n{prompt}\n\n"
        "Requirements:\n"
        "• Pre-verified (NO search needed): Device:R, Device:C, Device:C_Polarized, "
        "Device:L, Device:D, Device:LED, Device:Crystal, "
        "power:GND, power:+3V3, power:+5V, power:+12V, power:VCC, power:VDD, power:PWR_FLAG, "
        "Connector_Generic:Conn_01x02 through Conn_01x08, "
        "Switch:SW_Push, Transistor_BJT:Q_NPN_BCE, Transistor_BJT:Q_PNP_BCE, "
        "Transistor_FET:NMOS, Transistor_FET:PMOS, "
        "Regulator_Linear:LM7805, Regulator_Linear:AMS1117-3.3.\n"
        "• Call search_symbols for MCUs, ICs, and parts NOT in the pre-verified list.\n"
        "• Include decoupling caps, pull-up/down resistors, and all support passives.\n"
        "• Add power symbols for every rail and ground.\n"
        "• Place on 1.27 mm grid, ~20 mm between ICs.\n"
        "• Use net labels on signals that cross regions.\n"
        "• Once all non-trivial parts are searched, call create_schematic immediately."
    )

    messages = [{"role": "user", "content": user_message}]
    tools = [_SEARCH_TOOL, _SCHEMATIC_TOOL]
    rounds = 0

    for _round in range(40):
        resp = client.messages.create(
            model=model,
            max_tokens=8192,
            system=system_text,
            messages=messages,
            tools=tools,
        )
        rounds += 1
        tool_calls = [b for b in resp.content if b.type == "tool_use"]

        if not tool_calls:
            raise RuntimeError("Claude stopped without generating a schematic.")

        for block in tool_calls:
            if block.name == "create_schematic":
                return block.input, rounds

        tool_results = []
        for block in tool_calls:
            if block.name == "search_symbols":
                query = block.input.get("query", "")
                limit = int(block.input.get("limit", 10))
                results = sym_index.search(query, limit=limit)
                tool_results.append({
                    "type":        "tool_result",
                    "tool_use_id": block.id,
                    "content":     json.dumps({"results": results}),
                })

        messages.append({"role": "assistant", "content": resp.content})
        messages.append({"role": "user",      "content": tool_results})

    raise RuntimeError("Claude did not produce a schematic after 40 rounds.")


# ── CLI ───────────────────────────────────────────────────────────────────────

def main():
    parser = argparse.ArgumentParser(
        description="Generate a KiCad 10 schematic from a natural language prompt."
    )
    parser.add_argument("--prompt",  required=True, help="Circuit description")
    parser.add_argument("--output",  required=True, help="Output .kicad_sch path")
    parser.add_argument("--model",   default="claude-sonnet-4-6", help="Claude model")
    parser.add_argument("--symbol-dir", default="", help="Override KiCad symbol directory")
    args = parser.parse_args()

    symbol_dir = args.symbol_dir or _find_symbol_dir()
    if not symbol_dir:
        print(json.dumps({"status": "error",
                          "error": "KiCad symbol directory not found. "
                                   "Use --symbol-dir to specify it."}))
        sys.exit(1)

    index_data = build_symbol_index(symbol_dir)
    sym_index = SymbolIndex(index_data)

    print(f"[create] Generating schematic for: {args.prompt[:80]}…", file=sys.stderr)

    try:
        schematic_data, rounds = run_agentic_loop(args.prompt, sym_index, model=args.model)
    except RuntimeError as exc:
        print(json.dumps({"status": "error", "error": str(exc)}))
        sys.exit(1)

    result = write_schematic(args.output, symbol_dir, sym_index, schematic_data)
    result["search_rounds"] = rounds
    print(json.dumps(result, indent=2))


if __name__ == "__main__":
    main()
