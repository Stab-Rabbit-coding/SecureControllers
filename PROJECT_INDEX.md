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
| `.claude/` | Claude Code project config; `.claude/skills/` is the local agent-skills library (128 skills) — see below |
| `CLAUDE.md` | Avionics design project instructions (Serenity-UAV subsystem scope; this repo also serves as the workspace library — see Open Questions in the plan below) |
| `.gitignore` | Excludes `__pycache__/`, `*.pyc` |
| `INDEX.md` | Workspace resource library entry point — read this first for asset lookups |
| `LICENSE.md` | Repository license |
| `not-a-real-datasheet.txt` | Test fixture (deliberately not a real datasheet; excluded from the scanner's matched extensions) |
| `PROJECT_INDEX.md` | This file |
| `SecureControllers.code-workspace` | VS Code workspace file |
| `TODO.md` | Work Breakdown Structure. Currently scoped as "Serenity UAV — Avionics WBS"; identity vs. this repo's new workspace-library role is an open question in the plan (see `docs/plans/`) |

## `.claude/skills/`

128 agent skills (security/SOC, GRC compliance, PE-aligned engineering,
PCB/KiCad, compound-engineering, dev-workflow) mirrored into this repo from
the user's `~/.claude/skills/` and plugin installs, so they're available to
any Claude Code session — local or cloud/web — running against this repo or
branch, not just this machine. Human/agent-searchable index, grouped by
category, one-line description per skill:
[`.claude/skills/INDEX.md`](.claude/skills/INDEX.md). Machine-readable form:
`index/skills.json`. Regenerate after adding/removing/editing a skill:
`python3 tools/build_skills_index.py`.

Excluded from this mirror: `pr-review-toolkit`, `security-guidance`, and
`github` plugins — they ship as agents/hooks/commands, not `SKILL.md`
folders, so there was nothing skill-shaped to copy.

## `datasheets/`

48 manufacturer/standards PDFs (ISOW1044, SLB9670, ADIN1300, ADM2795E,
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
| `index/datasheets.json` | Type-sharded datasheet manifest (196 entries workspace-wide) |
| `index/kicad-symbols.json` | KiCad symbol manifest (40 entries) |
| `index/kicad-footprints.json` | KiCad footprint manifest (103 entries) |
| `index/shapes.json` | Mechanical shape manifest, STEP/WRL pairs collapsed (445 entries) |
| `index/scripts.json` | Reusable top-level `tools/` script manifest (49 entries) |
| `index/knowledge.json` | `engineering-pe-skills` knowledge-asset manifest (4 entries) — workspace-wide, cross-repo; distinct from this repo's own `index/skills.json` |
| `index/skills.json` | This repo's local `.claude/skills/` agent-skills manifest (128 entries). See `.claude/skills/INDEX.md` for the human-readable form |
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
| `tools/build_skills_index.py` | Builds `index/skills.json` + `.claude/skills/INDEX.md` from this repo's local `.claude/skills/` — separate from the workspace-wide scan/manifest pair above |

Regenerate both after any workspace repo's assets change:
`/usr/bin/python3 tools/inventory_scan.py && /usr/bin/python3 tools/build_manifests.py`
(must use `/usr/bin/python3`, not a repo-local `.venv`).
