# Project Index — SecureControllers

Directory structure and active files, per the repository-root governance
convention in the user's global `CLAUDE.md`. For high-volume, single-format
directories (datasheets, KiCad symbols/footprints, shared 3D shapes), this
file gives the directory-level shape; the authoritative per-file listing
(with hash, MPN guess, verification tier, and cross-repo duplicate flags) is
[`INDEX.md`](INDEX.md) and the machine-readable manifests under `index/`.
Duplicating hundreds of filenames here as well would drift out of sync with
the generated manifests on every rescan — regenerate `index/*.json` via
`tools/inventory_scan.py` / `tools/build_manifests.py`, not this file, and
treat those as the source of truth for asset inventories.

## Root

| Path | Purpose |
| --- | --- |
| `CLAUDE.md` | Avionics design project instructions (Serenity-UAV subsystem scope; this repo also serves as the workspace library — see Open Questions in the plan below) |
| `.gitignore` | Excludes `__pycache__/`, `*.pyc` |
| `INDEX.md` | Workspace resource library entry point — read this first for asset lookups |
| `LICENSE.md` | Repository license |
| `not-a-real-datasheet.txt` | Test fixture (deliberately not a real datasheet; excluded from the scanner's matched extensions) |
| `PROJECT_INDEX.md` | This file |
| `SecureControllers.code-workspace` | VS Code workspace file |
| `TODO.md` | Work Breakdown Structure. Currently scoped as "Serenity UAV — Avionics WBS"; identity vs. this repo's new workspace-library role is an open question in the plan (see `docs/plans/`) |

## `datasheets/`

38 manufacturer/standards PDFs (ISOW1044, SLB9670, ADIN1300, ADM2795E,
BMP388, SAM-M10Q, NIST SP 800-series, etc.). Full per-file listing with
MPN guesses: `index/datasheets.json`.

## `docs/`

| Path | Purpose |
| --- | --- |
| `docs/plans/` | Compound-engineering plan documents (`ce-plan` output). Currently: `2026-09-08-001-feat-workspace-resource-library-plan.md` |

## `firmware/`

Zephyr-based firmware tree, shared across the CN (comms node) and FC
(flight-control node) capes.

| Path | Purpose |
| --- | --- |
| `firmware/CMakeLists.txt` | Top-level build |
| `firmware/README.md` | Firmware build/flash instructions |
| `firmware/common/` | Shared code between CN and FC (`include/`, `src/`) |
| `firmware/cn/` | Comms-node-specific firmware (`src/`) |
| `firmware/fc/` | Flight-control-node-specific firmware (`src/`, `tools/`) |
| `firmware/dts/` | Devicetree overlays for `cape-a`/`cape-b`, `Makefile`, `README.md` |

## `index/` (generated — do not hand-edit)

| Path | Purpose |
| --- | --- |
| `index/_raw/<repo>.json` | Raw per-repo scan output from `tools/inventory_scan.py` |
| `index/datasheets.json` | Type-sharded datasheet manifest (175 entries workspace-wide) |
| `index/kicad-symbols.json` | KiCad symbol manifest (40 entries) |
| `index/kicad-footprints.json` | KiCad footprint manifest (103 entries) |
| `index/shapes.json` | Mechanical shape manifest, STEP/WRL pairs collapsed (445 entries) |
| `index/scripts.json` | Reusable top-level `tools/` script manifest (45 entries) |
| `index/knowledge.json` | `engineering-pe-skills` knowledge-asset manifest (4 entries) |
| `index/placeholders.json` | Empty-repo hooks (4 entries: Bento-boat, TidySweep, obd2-recorder, dasGoat-USV) |

## `kicad/`

| Path | Purpose |
| --- | --- |
| `kicad/symbols/` | Shared KiCad symbols + pinmap CSVs (ISOW1044BDFMR, KSZ9477, MSPM0G3507, SLB9670 TPM, SoM symbols) |
| `kicad/Serenity-Custom.pretty/` | Shared custom footprint library |
| `kicad/Vera.pretty/` | Vera-board-specific footprint library |
| `kicad/Emma/`, `kicad/Jayne/`, `kicad/Kaylee/`, `kicad/Wash/`, `kicad/Zoë/` | Per-board `kicads/`, `gerbers/`, `scripts/`, and board `.md` docs |
| `kicad/ENC-NACELLE-1.kicad_sch`, `.md` | Nacelle tilt-encoder schematic + notes |
| `kicad/*.py` | Per-board generator/fixup scripts (not indexed as reusable — see `INDEX.md`'s script-classification note) |
| `kicad/fp-lib-table`, `kicad/drc_report.txt`, `kicad/xcrv-DRC.rpt` | KiCad project config and DRC output |

## `shared.3dshapes/`

37 STEP/WRL/STL mechanical shape files for shared connectors, passives, and
packages (CONN-SMD/TH series, DFN/SON/SOT/QFN/UQFN/WSON/XSON packages,
USB-C, switches, LED). Full per-file listing: `index/shapes.json`.

## `tools/`

| Path | Purpose |
| --- | --- |
| `tools/inventory_scan.py` | Workspace-wide asset scanner (U1) — writes `index/_raw/*.json` and `index/placeholders.json` |
| `tools/build_manifests.py` | Builds the type-sharded `index/*.json` manifests from the raw scan (U2) |

Regenerate both after any workspace repo's assets change:
`/usr/bin/python3 tools/inventory_scan.py && /usr/bin/python3 tools/build_manifests.py`
(must use `/usr/bin/python3`, not a repo-local `.venv`).
