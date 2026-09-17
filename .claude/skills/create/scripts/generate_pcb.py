#!/usr/bin/env python3
"""
generate_pcb.py — AI-powered KiCad 10 PCB layout from a schematic netlist.

Usage:
    python3 generate_pcb.py \\
        --schematic ~/Documents/KiCad/MyProject/MyProject.kicad_sch \\
        --output    ~/Documents/KiCad/MyProject/MyProject.kicad_pcb \\
        --board-size 50x50 \\
        --prompt "Two-layer board, connectors on edges, power stage top-left"

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
from pathlib import Path


# ── Schematic netlist parser ──────────────────────────────────────────────────

def parse_schematic(sch_path: str) -> dict:
    """
    Extract component references, values, and footprints from a .kicad_sch file.
    Returns {"components": [{"reference", "value", "footprint", "lib_id"}]}
    """
    with open(sch_path, encoding="utf-8", errors="replace") as f:
        content = f.read()

    components = []
    # Match symbol instances
    for m in re.finditer(r'\(symbol\s+\(lib_id\s+"([^"]+)"\)', content):
        lib_id = m.group(1)
        # find the block around this match
        start = m.start()
        depth = 0
        end = start
        for i in range(start, min(start + 2000, len(content))):
            if content[i] == "(":
                depth += 1
            elif content[i] == ")":
                depth -= 1
                if depth == 0:
                    end = i
                    break

        block = content[start:end + 1]

        ref_m   = re.search(r'"Reference"\s+"([^"]+)"', block)
        val_m   = re.search(r'"Value"\s+"([^"]+)"', block)
        foot_m  = re.search(r'"Footprint"\s+"([^"]+)"', block)

        ref = ref_m.group(1) if ref_m else "?"
        val = val_m.group(1) if val_m else "?"
        foot = foot_m.group(1) if foot_m else ""

        # Skip power symbols and already-placed PWR refs
        if ref.startswith("#PWR") or ref.startswith("#FLG"):
            continue
        if lib_id.startswith("power:"):
            continue

        components.append({
            "reference": ref,
            "value":     val,
            "footprint": foot,
            "lib_id":    lib_id,
        })

    return {"components": components}


# ── Blank PCB template ────────────────────────────────────────────────────────

def _blank_pcb(width_mm: float, height_mm: float) -> str:
    edge_pts = (
        f"  (gr_line (start 0 0) (end {width_mm} 0) (layer \"Edge.Cuts\") (width 0.05))\n"
        f"  (gr_line (start {width_mm} 0) (end {width_mm} {height_mm}) (layer \"Edge.Cuts\") (width 0.05))\n"
        f"  (gr_line (start {width_mm} {height_mm}) (end 0 {height_mm}) (layer \"Edge.Cuts\") (width 0.05))\n"
        f"  (gr_line (start 0 {height_mm}) (end 0 0) (layer \"Edge.Cuts\") (width 0.05))\n"
    )
    return (
        "(kicad_pcb\n"
        "  (version 20231120)\n"
        "  (generator \"kicad-happy-create\")\n"
        "  (general\n"
        "    (thickness 1.6)\n"
        "  )\n"
        "  (layers\n"
        "    (0 \"F.Cu\" signal)\n"
        "    (31 \"B.Cu\" signal)\n"
        "    (32 \"B.Adhes\" user)\n"
        "    (33 \"F.Adhes\" user)\n"
        "    (34 \"B.Paste\" user)\n"
        "    (35 \"F.Paste\" user)\n"
        "    (36 \"B.SilkS\" user)\n"
        "    (37 \"F.SilkS\" user)\n"
        "    (38 \"B.Mask\" user)\n"
        "    (39 \"F.Mask\" user)\n"
        "    (44 \"Edge.Cuts\" user)\n"
        "  )\n"
        "  (setup\n"
        "    (pad_to_mask_clearance 0)\n"
        "  )\n"
        + edge_pts +
        ")\n"
    )


def _fp_instance(ref: str, value: str, footprint: str,
                 x: float, y: float, angle: float, layer: str = "F.Cu") -> str:
    if not footprint:
        return ""
    parts = footprint.split(":", 1)
    lib  = parts[0] if len(parts) == 2 else ""
    name = parts[1] if len(parts) == 2 else parts[0]
    return (
        f'  (footprint "{lib}:{name}"\n'
        f'    (layer "{layer}")\n'
        f'    (at {x:.4f} {y:.4f} {angle:.4f})\n'
        f'    (property "Reference" "{ref}" (at 0 -3 0) (layer "F.SilkS"))\n'
        f'    (property "Value" "{value}" (at 0 3 0) (layer "F.Fab"))\n'
        f'  )'
    )


def write_pcb(output_path: str, placements: list, components: list,
              board_size: tuple) -> dict:
    w, h = board_size
    content = _blank_pcb(w, h)

    comp_map = {c["reference"]: c for c in components}
    body = []
    placed = 0

    for move in placements:
        ref = move.get("reference", "")
        comp = comp_map.get(ref)
        if not comp or not comp.get("footprint"):
            continue
        fp = _fp_instance(
            ref=ref,
            value=comp["value"],
            footprint=comp["footprint"],
            x=float(move.get("x_mm", w / 2)),
            y=float(move.get("y_mm", h / 2)),
            angle=float(move.get("angle_deg", 0)),
        )
        if fp:
            body.append(fp)
            placed += 1

    pos = content.rfind("\n)")
    if pos != -1 and body:
        content = content[:pos] + "\n" + "\n".join(body) + "\n" + content[pos:]

    Path(output_path).parent.mkdir(parents=True, exist_ok=True)
    with open(output_path, "w", encoding="utf-8") as f:
        f.write(content)

    return {
        "status": "ok",
        "output": output_path,
        "placed": placed,
        "board_size_mm": list(board_size),
    }


# ── Claude placement loop ─────────────────────────────────────────────────────

_PLACEMENT_TOOL = {
    "name": "place_components",
    "description": "Output the final PCB component placement.",
    "input_schema": {
        "type": "object",
        "required": ["moves"],
        "properties": {
            "moves": {
                "type": "array",
                "items": {
                    "type": "object",
                    "required": ["reference", "x_mm", "y_mm"],
                    "properties": {
                        "reference": {"type": "string"},
                        "x_mm":      {"type": "number"},
                        "y_mm":      {"type": "number"},
                        "angle_deg": {"type": "number", "default": 0},
                        "reason":    {"type": "string"},
                    },
                },
            },
            "routing_hints": {"type": "array", "items": {"type": "string"}},
        },
    },
}


def run_placement_loop(components: list, board_size: tuple,
                       extra_prompt: str, model: str) -> list:
    try:
        import anthropic
    except ImportError:
        raise RuntimeError("Run: pip install anthropic")

    api_key = os.environ.get("ANTHROPIC_API_KEY", "")
    if not api_key:
        raise RuntimeError("ANTHROPIC_API_KEY not set.")

    client = anthropic.Anthropic(api_key=api_key)
    w, h = board_size

    comp_table = "\n".join(
        f"  {c['reference']:<10} {c['value']:<25} {c['footprint']}"
        for c in components
    )

    user_msg = (
        f"Place these components on a {w}×{h} mm two-layer PCB.\n\n"
        f"Components:\n{comp_table}\n\n"
        f"Guidelines:\n"
        f"• Keep decoupling caps within 3 mm of their IC supply pins.\n"
        f"• Group functional blocks (power, MCU, connectors, sensors).\n"
        f"• Place connectors on board edges.\n"
        f"• Leave 2 mm clearance from Edge.Cuts.\n"
        f"• Coordinates must be within 0–{w} mm (X) and 0–{h} mm (Y).\n"
        + (f"\nExtra requirements: {extra_prompt}\n" if extra_prompt else "")
        + "\nCall place_components with exact X,Y coordinates for every component."
    )

    resp = client.messages.create(
        model=model,
        max_tokens=4096,
        system="You are an expert PCB layout engineer. Place components for optimal signal integrity, EMC, and DFM.",
        messages=[{"role": "user", "content": user_msg}],
        tools=[_PLACEMENT_TOOL],
        tool_choice={"type": "tool", "name": "place_components"},
    )

    for block in resp.content:
        if block.type == "tool_use" and block.name == "place_components":
            return block.input.get("moves", [])

    return []


# ── CLI ───────────────────────────────────────────────────────────────────────

def main():
    parser = argparse.ArgumentParser(
        description="Generate a KiCad 10 PCB layout from a schematic."
    )
    parser.add_argument("--schematic",  required=True, help=".kicad_sch source file")
    parser.add_argument("--output",     required=True, help="Output .kicad_pcb path")
    parser.add_argument("--board-size", default="100x80", help="WxH in mm, e.g. 50x50")
    parser.add_argument("--prompt",     default="",
                        help="Extra placement guidelines")
    parser.add_argument("--model", default="claude-sonnet-4-6")
    args = parser.parse_args()

    # Parse board size
    try:
        w_str, h_str = args.board_size.lower().replace("mm", "").split("x")
        board_size = (float(w_str), float(h_str))
    except ValueError:
        print(json.dumps({"status": "error",
                          "error": f"Invalid --board-size '{args.board_size}'. Use WxH, e.g. 50x50"}))
        sys.exit(1)

    if not os.path.exists(args.schematic):
        print(json.dumps({"status": "error",
                          "error": f"Schematic not found: {args.schematic}"}))
        sys.exit(1)

    print(f"[create] Parsing schematic: {args.schematic}", file=sys.stderr)
    netlist = parse_schematic(args.schematic)
    components = netlist["components"]
    print(f"[create] Found {len(components)} components.", file=sys.stderr)

    if not components:
        print(json.dumps({"status": "error",
                          "error": "No components with footprints found in schematic."}))
        sys.exit(1)

    print(f"[create] Requesting placement from Claude…", file=sys.stderr)
    try:
        placements = run_placement_loop(components, board_size, args.prompt, args.model)
    except RuntimeError as exc:
        print(json.dumps({"status": "error", "error": str(exc)}))
        sys.exit(1)

    result = write_pcb(args.output, placements, components, board_size)
    print(json.dumps(result, indent=2))


if __name__ == "__main__":
    main()
