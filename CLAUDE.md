# SecureControllers — Claude Code Project Instructions

## Scope and role

`SecureControllers` is the **Browncoats workspace's shared hardware-design-asset library**
(copy-with-index, not a git submodule or symlink) — see [`INDEX.md`](INDEX.md) for the lookup
workflow and [`PROJECT_INDEX.md`](PROJECT_INDEX.md) for the directory-level shape. Canonical,
verified copies of shared datasheets, KiCad symbols/footprints, and mechanical shapes live under
`datasheets/`, `kicad/`, and `shared.3dshapes/`, each entry hashed and cross-referenced against
its counterpart in every consuming repo (Serenity-UAV, Open-Secure-ESC, and others).

This repo also carries the workspace's shared agent-skills library
(`.claude/skills/`, indexed at `.claude/skills/INDEX.md`) and a Zephyr-based firmware tree
(`firmware/`) shared across comms-node (CN) and flight-control-node (FC) capes.

**This file previously carried a full copy of Serenity-UAV's avionics cape architecture,
PACE/workload-balancing tables, and per-cape (Wash/TACCO/Emma/Observer/FlightEngineer) design
narrative, frozen at Rev S (2026-07-04/05).** That content described the *Serenity-UAV*
airframe's board designs, not an asset-library policy, and had drifted ~12 weeks out of date
against Serenity-UAV's own tracking (which has since renamed the boards — Wash→Pilot, XO→TACCO,
Emma→Commo — and completed a substantial amount of the work that copy still listed as open).
Resolved 2026-09-27, closing the open question logged in
`docs/plans/2026-09-08-001-feat-workspace-resource-library-plan.md` ("Open Questions" —
`TODO.md` identity): retire the duplicate narrative here rather than maintain two
independently-drifting copies of the same board status.

**For current avionics board architecture, PACE assignments, per-cape status
(Pilot/TACCO/Commo/FlightEngineer/Observer/Bus-Gateway), and open engineering work, read
Serenity-UAV's own `AGENTS.md` (§1, §9) and `avionics/{AGENTS,WBS,TODO}.md` federation — that
repo is the single source of truth for the airframe this workspace's shared assets support.**

**Known open item (not resolved by this pass, flagged for the user):** `kicad/Emma/`,
`kicad/Wash/`, `kicad/Zoë/`, `kicad/Jayne/`, `kicad/Kaylee/`, and `kicad/ENC-NACELLE-1.*` under
this repo's own `kicad/` directory are full per-board KiCad projects (schematic + PCB + gerbers +
scripts + `.md` status notes), not just shared symbols/footprints — last touched 2026-08-15,
before Serenity-UAV's board renames. Whether these are meant to become part of the shared-symbol/
footprint library (with the full board projects retired the same way this file was), kept as a
frozen historical snapshot, or something else, is a separate decision from this file's identity
and is still open — see the same plan's "Drift resolution authority" question. Do not delete or
rewrite those project files without the user's explicit direction.

## Generic conventions that do apply here

These are workspace-wide conventions for any KiCad asset maintained in this repo (symbols,
footprints, or a board project), independent of which specific airframe consumes them:

- **Footprint/symbol accuracy:** verify every footprint against its OEM datasheet before adding
  or editing it — check `datasheets/` (or the requesting repo's own datasheets folder) for an
  existing PDF before searching online, and use the OEM datasheet as the authoritative reference.
- **DRC/ERC workflow for any board project touched here:** run ERC on the schematic and DRC on
  the PCB after any edit; document unresolved violations with the specific rule and reason rather
  than silently leaving them; commit only once every violation is resolved or documented.
- **Index hygiene:** after adding, removing, or changing a datasheet, symbol, footprint, shape,
  or script, regenerate the manifests (`tools/inventory_scan.py` then `tools/build_manifests.py`,
  via `/usr/bin/python3`) so `index/*.json` and `INDEX.md` stay accurate — see `PROJECT_INDEX.md`.

## Documentation Standards

### Warnings, Cautions, Notes, and Wording

Callout severity and requirement-verb usage follow CNAF M-3710.7 §1.5–1.6
(NATOPS General Flight and Operating Instructions Manual) [REF-MIL-001
§1.5, §1.6] — the manual is held locally at `docs/cnaf-3710.7_1-52.pdf` (the
source of this convention for this workspace):

- **WARNING** — a procedure or condition that may result in injury, death,
  or destruction of hardware if not carefully observed or followed.
- **CAUTION** — a procedure or condition that may result in equipment
  damage (board, MCU, secure element) with no injury or asset-loss risk.
- **Note** — information that must be emphasized but carries no
  WARNING/CAUTION-level risk.

Never downgrade a WARNING-level risk into a Note, and never use an ad hoc
label ("IMPORTANT:", "ATTENTION:") in place of one of these three.

Requirement wording, same source [REF-MIL-001 §1.6]:

- **Shall** — mandatory.
- **Should** — recommended, not mandatory.
- **May** / **need not** — optional.
- **Will** — futurity only; never a degree of requirement. Do not write
  "will" where "shall" is meant.

**Active vs. passive voice (project addition, not in CNAF M-3710.7):** write
procedural text in the active voice except where the shall/should/may/will
wording above requires the passive construction to state the requirement
itself.
