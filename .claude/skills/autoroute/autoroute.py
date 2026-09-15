#!/usr/bin/env python3
"""
KiCad Auto-Router using FreeRouting
Usage: python3 autoroute.py <path/to/board.kicad_pcb> [--keepout-margin 0.25]
"""

import sys
import os
import shutil
import subprocess
import tempfile
import argparse
import re

KICAD_PYTHON = "/Applications/KiCad/KiCad.app/Contents/Frameworks/Python.framework/Versions/3.9/bin/python3"
FREEROUTING_JAR = os.path.join(os.path.dirname(__file__), "freerouting.jar")

# ── DSN export via KiCad Python ────────────────────────────────────────────

EXPORT_SCRIPT = """
import sys
sys.path.insert(0, '/Applications/KiCad/KiCad.app/Contents/Frameworks/Python.framework/Versions/3.9/lib/python3.9/site-packages')
import pcbnew

pcb_path = sys.argv[1]
dsn_path = sys.argv[2]

board = pcbnew.LoadBoard(pcb_path)
board.BuildConnectivity()

# Remove all existing tracks and vias so FreeRouting starts clean
for t in list(board.GetTracks()):
    board.Remove(t)

# Assign temp refs to no-ref footprints (e.g. mounting holes) so DSN export works
i = 1
for fp in board.GetFootprints():
    if not fp.GetReference():
        fp.SetReference(f"H{i}")
        i += 1

board.Save(pcb_path)
print(f"Cleared existing tracks")

result = pcbnew.ExportSpecctraDSN(board, dsn_path)
if not result:
    print("ERROR: ExportSpecctraDSN returned False")
    sys.exit(1)
print(f"Exported DSN: {dsn_path}")
"""

# ── SES import via KiCad Python ────────────────────────────────────────────

IMPORT_SCRIPT = """
import sys
sys.path.insert(0, '/Applications/KiCad/KiCad.app/Contents/Frameworks/Python.framework/Versions/3.9/lib/python3.9/site-packages')
import pcbnew

pcb_path = sys.argv[1]
ses_path = sys.argv[2]
out_path = sys.argv[3]

board = pcbnew.LoadBoard(pcb_path)
result = pcbnew.ImportSpecctraSES(board, ses_path)
if not result:
    print("ERROR: ImportSpecctraSES returned False")
    sys.exit(1)

# Remove temp refs from mounting holes
for fp in board.GetFootprints():
    ref = fp.GetReference()
    if ref and ref.startswith('H') and ref[1:].isdigit():
        fp.SetReference('')

board.Save(out_path)

# Count routed tracks
tracks = [t for t in board.GetTracks() if t.GetClass() == 'PCB_TRACK']
print(f"Imported SES: {len(tracks)} track segments written to {out_path}")
"""

# ── DRC summary via KiCad Python ───────────────────────────────────────────

DRC_SCRIPT = """
import sys, json
sys.path.insert(0, '/Applications/KiCad/KiCad.app/Contents/Frameworks/Python.framework/Versions/3.9/lib/python3.9/site-packages')
import pcbnew

pcb_path = sys.argv[1]
board = pcbnew.LoadBoard(pcb_path)

# Ratsnest (unrouted)
board.BuildConnectivity()
connectivity = board.GetConnectivity()
unrouted = connectivity.GetUnconnectedCount(False)

# Count tracks
tracks = [t for t in board.GetTracks() if t.GetClass() == 'PCB_TRACK']
vias  = [t for t in board.GetTracks() if t.GetClass() == 'PCB_VIA']

print(json.dumps({
    "unrouted": unrouted,
    "tracks": len(tracks),
    "vias": len(vias),
}))
"""


def run_kicad_python(script_text: str, args: list[str]) -> str:
    with tempfile.NamedTemporaryFile(suffix=".py", mode="w", delete=False) as f:
        f.write(script_text)
        script_path = f.name
    try:
        result = subprocess.run(
            [KICAD_PYTHON, script_path] + args,
            capture_output=True, text=True, timeout=120
        )
        if result.returncode != 0:
            raise RuntimeError(f"KiCad Python error:\n{result.stderr}")
        return result.stdout.strip()
    finally:
        os.unlink(script_path)


def export_dsn(pcb_path: str, dsn_path: str):
    out = run_kicad_python(EXPORT_SCRIPT, [pcb_path, dsn_path])
    print(f"  {out}")


def run_freerouting(dsn_path: str, ses_path: str):
    cmd = [
        "java", "-jar", FREEROUTING_JAR,
        "-de", dsn_path,   # design file (DSN)
        "-do", ses_path,   # output SES
        "-mp", "100",      # max passes
        "-mt", "4",        # threads
    ]
    print(f"  Running FreeRouting (max 100 passes, 4 threads)...")
    result = subprocess.run(cmd, capture_output=True, text=True, timeout=300)
    # FreeRouting prints progress to stderr
    for line in result.stderr.splitlines():
        if any(k in line.lower() for k in ["pass", "complete", "route", "error", "warning"]):
            print(f"    {line.strip()}")
    if result.returncode != 0 and not os.path.exists(ses_path):
        raise RuntimeError(f"FreeRouting failed:\n{result.stderr[-2000:]}")


def import_ses(pcb_path: str, ses_path: str, out_path: str):
    out = run_kicad_python(IMPORT_SCRIPT, [pcb_path, ses_path, out_path])
    print(f"  {out}")


def drc_summary(pcb_path: str) -> dict:
    import json
    out = run_kicad_python(DRC_SCRIPT, [pcb_path])
    return json.loads(out)


def main():
    parser = argparse.ArgumentParser(description="Auto-route a KiCad PCB using FreeRouting")
    parser.add_argument("pcb", help="Path to .kicad_pcb file")
    parser.add_argument("--output", "-o", help="Output PCB path (default: overwrites input)")
    parser.add_argument("--passes", "-p", type=int, default=100, help="Max routing passes (default: 100)")
    args = parser.parse_args()

    pcb_path = os.path.abspath(args.pcb)
    out_path = os.path.abspath(args.output) if args.output else pcb_path

    if not os.path.exists(pcb_path):
        print(f"ERROR: {pcb_path} not found")
        sys.exit(1)

    if not os.path.exists(FREEROUTING_JAR):
        print(f"ERROR: freerouting.jar not found at {FREEROUTING_JAR}")
        sys.exit(1)

    # Backup original
    backup_path = pcb_path + ".pre-autoroute.bak"
    if not os.path.exists(backup_path):
        shutil.copy2(pcb_path, backup_path)
        print(f"[1/5] Backup saved → {backup_path}")
    else:
        print(f"[1/5] Backup already exists, skipping")

    with tempfile.TemporaryDirectory() as tmpdir:
        dsn_path = os.path.join(tmpdir, "board.dsn")
        ses_path = os.path.join(tmpdir, "board.ses")

        # Pre-route DRC
        print("[2/5] Checking board before routing...")
        pre = drc_summary(pcb_path)
        print(f"       Unrouted connections: {pre['unrouted']}")
        if pre["unrouted"] == 0:
            print("       Board is already fully routed!")
            sys.exit(0)

        # Export DSN
        print("[3/5] Exporting Specctra DSN...")
        export_dsn(pcb_path, dsn_path)
        if not os.path.exists(dsn_path):
            print("ERROR: DSN export failed")
            sys.exit(1)
        print(f"       DSN size: {os.path.getsize(dsn_path):,} bytes")

        # Run FreeRouting
        print("[4/5] Auto-routing with FreeRouting...")
        run_freerouting(dsn_path, ses_path)
        if not os.path.exists(ses_path):
            print("ERROR: FreeRouting did not produce a SES file")
            sys.exit(1)
        print(f"       SES size: {os.path.getsize(ses_path):,} bytes")

        # Import SES
        print("[5/5] Importing routes back into PCB...")
        import_ses(pcb_path, ses_path, out_path)

    # Post-route summary
    print("\n── Routing complete ──────────────────────────────────")
    post = drc_summary(out_path)
    print(f"  Track segments : {post['tracks']}")
    print(f"  Vias           : {post['vias']}")
    print(f"  Unrouted       : {post['unrouted']}")
    if post["unrouted"] == 0:
        print("  Result         : FULLY ROUTED ✓")
    else:
        pct = round(100 * (pre['unrouted'] - post['unrouted']) / max(pre['unrouted'], 1))
        print(f"  Result         : {pct}% routed ({post['unrouted']} connections remain)")
    print(f"  Output         : {out_path}")
    if post["unrouted"] > 0:
        print("\n  Tip: Re-run to continue routing, or open in KiCad and manually route remaining connections.")


if __name__ == "__main__":
    main()
