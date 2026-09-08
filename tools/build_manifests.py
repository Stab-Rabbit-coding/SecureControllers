#!/usr/bin/env python3
"""Build type-sharded, low-token-cost manifests from the raw inventory scan.

Reads index/_raw/<repo>.json (from inventory_scan.py) and writes:
  index/datasheets.json
  index/kicad-symbols.json
  index/kicad-footprints.json
  index/shapes.json
  index/scripts.json
  index/knowledge.json

Each entry carries verification_tier: "unverified" (Phase 2 / U4 fills in
"A", "B", or "C"). See docs/plans/2026-09-08-001-feat-workspace-resource-library-plan.md (U2).
"""

import json
import re
from pathlib import Path

WORKSPACE_ROOT = Path(__file__).resolve().parents[2]
SC_ROOT = WORKSPACE_ROOT / "SecureControllers"
RAW_DIR = SC_ROOT / "index" / "_raw"
OUT_DIR = SC_ROOT / "index"

# Matches a manufacturer-part-number-shaped token: letters/digits, at least
# one digit, length >= 4, allowing internal - and _. Deliberately permissive;
# Phase 2 (U4) confirms or corrects mpn_guess against actual datasheet content.
MPN_TOKEN_RE = re.compile(r"[A-Za-z]{1,6}[A-Za-z0-9_-]{2,}\d[A-Za-z0-9_-]*")
NOISE_WORDS = {
    "datasheet",
    "data",
    "sheet",
    "rev",
    "v1",
    "v2",
    "v3",
    "en",
    "final",
    "summary",
}


def load_raw() -> list[dict]:
    records = []
    for f in sorted(RAW_DIR.glob("*.json")):
        records.extend(json.loads(f.read_text()))
    return records


def guess_mpn(basename: str) -> str | None:
    stem = Path(basename).stem
    tokens = re.split(r"[\s\-_.]+", stem)
    candidates = [
        t for t in tokens if t.lower() not in NOISE_WORDS and MPN_TOKEN_RE.fullmatch(t)
    ]
    if not candidates:
        return None
    # Prefer the longest candidate token as the most specific part identifier.
    return max(candidates, key=len).upper()


def base_entry(rec: dict) -> dict:
    return {
        "repo": rec["repo"],
        "path": rec["rel_path"],
        "sha256": rec["sha256"],
        "size_bytes": rec.get("size_bytes"),
        "verification_tier": "unverified",
        "verified": False,
        "canonical_path": None,
        "possible_duplicate": rec.get("possible_duplicate", False),
        "duplicate_hash_match": rec.get("duplicate_hash_match", False),
        "renamed_duplicate": rec.get("renamed_duplicate", False),
    }


def build_datasheets(records: list[dict]) -> list[dict]:
    out = []
    for rec in records:
        if rec["asset_type"] != "datasheet":
            continue
        entry = base_entry(rec)
        entry["mpn_guess"] = guess_mpn(Path(rec["rel_path"]).name)
        out.append(entry)
    return out


def build_kicad(records: list[dict], asset_type: str) -> list[dict]:
    out = []
    for rec in records:
        if rec["asset_type"] != asset_type:
            continue
        entry = base_entry(rec)
        path_parts = Path(rec["rel_path"]).parts
        entry["library"] = path_parts[-2] if len(path_parts) > 1 else None
        entry["symbol_or_footprint_name"] = Path(rec["rel_path"]).stem
        out.append(entry)
    return out


def build_shapes(records: list[dict]) -> list[dict]:
    shape_records = [r for r in records if r["asset_type"] == "shape"]
    by_key: dict[tuple[str, str], dict] = {}
    for rec in shape_records:
        p = Path(rec["rel_path"])
        key = (rec["repo"], str(p.with_suffix("")))
        group = by_key.setdefault(
            key,
            {
                "repo": rec["repo"],
                "basename": p.stem,
                "files": {},
                "verification_tier": "unverified",
                "verified": False,
                "canonical_path": None,
            },
        )
        group["files"][rec["ext"].lstrip(".")] = {
            "path": rec["rel_path"],
            "sha256": rec["sha256"],
            "size_bytes": rec.get("size_bytes"),
        }

    out = []
    for group in by_key.values():
        exts = set(group["files"].keys())
        group["pair_incomplete"] = not ({"step", "wrl"} <= exts) and bool(
            exts & {"step", "wrl"}
        )
        out.append(group)
    return out


def build_scripts(records: list[dict]) -> list[dict]:
    return [base_entry(r) for r in records if r["asset_type"] == "script"]


def build_knowledge(records: list[dict]) -> list[dict]:
    out = []
    for rec in records:
        if rec["asset_type"] != "knowledge":
            continue
        out.append(
            {
                "repo": rec["repo"],
                "path": rec["rel_path"],
                "description": rec.get("description", ""),
                "file_count": rec.get("file_count"),
                "sha256": rec["sha256"],
            }
        )
    return out


def write_json(name: str, data) -> None:
    with (OUT_DIR / name).open("w") as f:
        json.dump(data, f, indent=2, sort_keys=True)
        f.write("\n")
    count = len(data)
    print(f"{name}: {count} entries")


def main() -> None:
    records = load_raw()

    write_json("datasheets.json", build_datasheets(records))
    write_json("kicad-symbols.json", build_kicad(records, "kicad_symbol"))
    write_json("kicad-footprints.json", build_kicad(records, "kicad_footprint"))
    write_json("shapes.json", build_shapes(records))
    write_json("scripts.json", build_scripts(records))
    write_json("knowledge.json", build_knowledge(records))


if __name__ == "__main__":
    main()
