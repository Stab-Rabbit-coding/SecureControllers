# Workspace Resource Index

`SecureControllers` is the canonical library for reusable hardware design
assets across the Browncoats workspace (`designs/`) — **copy-with-index**,
not a git submodule or symlink. Canonical, verified copies of shared
datasheets, KiCad symbols/footprints, and mechanical shapes live in this
repo's `datasheets/`, `kicad/`, and `shared.3dshapes/` directories, each with
a recorded SHA-256 hash. Consuming repos keep their own local copies; this
index is how you check whether yours matches the canonical one, and where to
find a verified asset before adding a new copy.

Full plan and rationale:
[`docs/plans/2026-09-08-001-feat-workspace-resource-library-plan.md`](docs/plans/2026-09-08-001-feat-workspace-resource-library-plan.md).
GitHub issue tracking all four phases:
[`SecureControllers#1`](https://github.com/Stab-Rabbit-coding/SecureControllers/issues/1).

## How to look something up (minimum token cost)

Read **one** manifest file below for your asset type — never grep the PDFs,
`.kicad_sym`/`.kicad_mod` files, or shape files themselves, and never load
more than one manifest for a single lookup.

| Looking for...                    | Read this file                | Key field to match on                                |
| --------------------------------- | ----------------------------- | ---------------------------------------------------- |
| A datasheet by part number        | `index/datasheets.json`       | `mpn_guess` (Tier B-confirmed once `verified: true`) |
| A KiCad symbol                    | `index/kicad-symbols.json`    | `symbol_or_footprint_name`                           |
| A KiCad footprint                 | `index/kicad-footprints.json` | `symbol_or_footprint_name`                           |
| A mechanical shape (STEP/WRL/STL) | `index/shapes.json`           | `basename`                                           |
| A shared script/tool              | `index/scripts.json`          | `path`                                               |
| A skill/knowledge resource        | `index/knowledge.json`        | `path`, `description`                                |
| Whether a repo has assets yet     | `index/placeholders.json`     | `repo`                                               |

There is currently no single-file "everything from repo X" lookup — that
would require reading each type manifest and filtering by `repo`. See the
Open Questions in the plan (per-repo lookup surface) before relying on one;
none exists yet.

Every entry carries `verification_tier` (`unverified` until Phase 2 runs,
then `"A"` = full pin/pad-verified, `"B"` = provenance/hash-verified, `"C"` =
placeholder-only) and `verified: true/false`. An entry with
`possible_duplicate: true` or `renamed_duplicate: true` has a same- or
differently-named twin in another repo — check `canonical_path` (once Phase 3
runs) for which copy is authoritative.

## Current scope (as of the last scan)

| Repo                   | Datasheets | KiCad symbols | KiCad footprints | Shapes | Scripts |
| ---------------------- | ---------: | ------------: | ---------------: | -----: | ------: |
| Serenity-UAV           |         50 |             9 |               17 |    367 |      43 |
| SecureControllers      |         38 |             8 |               15 |     37 |       2 |
| Open-Secure-ESC        |         58 |            20 |                9 |      1 |       0 |
| open-servo-core-secure |         11 |             1 |               40 |     37 |       0 |
| LibreServo_v4          |         15 |             2 |               22 |      3 |       0 |
| Tactical-WX-RX         |          3 |             0 |                0 |      0 |       0 |

"Scripts" counts only top-level `tools/` directories (per the provisional
classification rule below) — nested per-board generator/fixup scripts (e.g.
`Open-Secure-ESC`'s many `kicad/<board>/tools/*.py` one-offs) are
intentionally excluded, not missed.

`engineering-pe-skills` is indexed separately as a **knowledge asset** (4
skill entries in `index/knowledge.json`) — it has no MPN/hash-drift concerns
in the hardware sense, but is still a citable reusable resource.

**Placeholder-hook repos** (no hardware assets yet — `index/placeholders.json`):
Bento-boat, TidySweep, obd2-recorder, dasGoat-USV. Consult this index when
starting hardware work in any of them.

**Confirmed cross-repo duplication:** 87 of 175 cataloged datasheets and 74 of
445 shape entries (`possible_duplicate: true` in `index/datasheets.json` /
`index/shapes.json`) already have a same-named copy in another repo — this is
exactly the drift risk this index exists to catch. 4 renamed-but-content-
identical datasheet duplicates were also found (`renamed_duplicate: true`).

## Verification tiers (Phase 2 / U4, not yet run)

- **Tier A** — full pin/pad-level check against the source datasheet. Applied
  to flight-critical parts and anything already flagged as suspect (e.g. the
  7 known-bad Wash footprints tracked in `TODO.md`).
- **Tier B** — provenance + cross-repo hash-consistency check. Everything
  else.
- **Tier C** — placeholder only, no file to verify (the four empty repos).

See the plan's Open Questions for two items that block a clean Tier-A pass:
worklist completeness for un-audited flight-critical parts, and the
provisional "scripts live under `tools/`" classification rule used by
`tools/inventory_scan.py`.

## Regenerating the index

```bash
/usr/bin/python3 tools/inventory_scan.py    # rescan all repos -> index/_raw/*.json
/usr/bin/python3 tools/build_manifests.py   # rebuild index/*.json from the raw scan
```

Both scripts are stdlib-only (no `kiutils`/`manifold3d` dependency) and must
be run with `/usr/bin/python3`, not a repo's local `.venv`, which shadows
system packages without providing everything the workspace tooling needs.

## Cross-links from consuming repos

Each consuming repo's own `AGENTS.md`/`CLAUDE.md` carries a one-line pointer
back to this file (Phase 4 / U6) — check there first if you arrived at a
board's design docs and are wondering whether an asset already exists
elsewhere in the workspace.
