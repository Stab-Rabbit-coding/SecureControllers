#!/usr/bin/env python3
"""Workspace-wide reusable-asset inventory scanner.

Walks each configured repo under the Browncoats workspace, classifies files
by extension, hashes them, and writes one raw JSON record file per repo to
index/_raw/<repo>.json. Also runs cross-repo duplicate detection (by
basename+ext, and separately by content hash alone) and writes
index/placeholders.json for the confirmed-empty repos.

See docs/plans/2026-09-08-001-feat-workspace-resource-library-plan.md (U1).

Script classification is provisional: only files under a top-level `tools/`
directory in each repo are treated as reusable scripts today. Per-board
generator scripts (e.g. kicad/gen_*.py) are intentionally excluded pending
resolution of the "recognized shared-tool scripts" open question in the plan.
"""

import hashlib
import json
import sys
from pathlib import Path

WORKSPACE_ROOT = Path(__file__).resolve().parents[2]

ASSET_REPOS = [
    "Serenity-UAV",
    "SecureControllers",
    "LibreServo_v4",
    "Open-Secure-ESC",
    "open-servo-core-secure",
    "Tactical-WX-RX",
]

KNOWLEDGE_REPOS = ["engineering-pe-skills"]

PLACEHOLDER_REPOS = ["Bento-boat", "TidySweep", "obd2-recorder", "dasGoat-USV"]

EXT_TYPE_MAP = {
    ".pdf": "datasheet",
    ".kicad_sym": "kicad_symbol",
    ".kicad_mod": "kicad_footprint",
    ".step": "shape",
    ".stp": "shape",
    ".wrl": "shape",
    ".stl": "shape",
}

ALWAYS_SKIP_DIRS = {"node_modules", "__pycache__"}


def has_skip_part(parts: tuple[str, ...]) -> bool:
    """Skip hidden directories (.git, .worktrees, .venv, etc.) and known noise dirs."""
    return any(part.startswith(".") or part in ALWAYS_SKIP_DIRS for part in parts)

OUTPUT_ROOT = WORKSPACE_ROOT / "SecureControllers" / "index"


def parse_gitignore(repo_root: Path) -> list[str]:
    """Minimal gitignore pattern loader (plain fnmatch semantics, not full spec)."""
    gi = repo_root / ".gitignore"
    if not gi.exists():
        return []
    patterns = []
    for line in gi.read_text(errors="replace").splitlines():
        line = line.strip()
        if not line or line.startswith("#"):
            continue
        patterns.append(line.lstrip("/").rstrip("/"))
    return patterns


def is_ignored(rel_path: Path, patterns: list[str]) -> bool:
    import fnmatch

    rel_str = str(rel_path)
    parts = rel_path.parts
    for pat in patterns:
        if fnmatch.fnmatch(rel_str, pat) or fnmatch.fnmatch(rel_str, f"*/{pat}"):
            return True
        if any(fnmatch.fnmatch(part, pat) for part in parts):
            return True
    return False


def sha256_of(path: Path) -> str:
    h = hashlib.sha256()
    with path.open("rb") as f:
        for chunk in iter(lambda: f.read(1 << 16), b""):
            h.update(chunk)
    return h.hexdigest()


def classify_ext(rel_path: Path) -> str | None:
    suffix = rel_path.suffix.lower()
    if suffix in EXT_TYPE_MAP:
        return EXT_TYPE_MAP[suffix]
    # Only a *top-level* tools/ directory counts as reusable-script scope;
    # nested per-board tools/ dirs (e.g. kicad/<board>/tools/) hold one-off
    # generator/fixup scripts, not shared tools.
    if suffix == ".py" and len(rel_path.parts) >= 2 and rel_path.parts[0] == "tools":
        return "script"
    return None


def scan_repo(repo_name: str, is_knowledge: bool = False) -> list[dict]:
    repo_root = WORKSPACE_ROOT / repo_name
    if not repo_root.is_dir():
        print(f"WARNING: repo not found on disk: {repo_root}", file=sys.stderr)
        return []

    if is_knowledge:
        return scan_knowledge_repo(repo_name, repo_root)

    patterns = parse_gitignore(repo_root)
    records = []
    for path in sorted(repo_root.rglob("*")):
        if not path.is_file():
            continue
        rel = path.relative_to(repo_root)
        if has_skip_part(rel.parts):
            continue
        if is_ignored(rel, patterns):
            continue
        asset_type = classify_ext(rel)
        if asset_type is None:
            continue
        records.append(
            {
                "repo": repo_name,
                "rel_path": str(rel),
                "ext": path.suffix.lower(),
                "asset_type": asset_type,
                "size_bytes": path.stat().st_size,
                "sha256": sha256_of(path),
                "mtime": int(path.stat().st_mtime),
            }
        )
    return records


def scan_knowledge_repo(repo_name: str, repo_root: Path) -> list[dict]:
    """One record per skill directory, hash = hash of concatenated file hashes.

    Skill directories live under a `skills/` subdirectory when present
    (confirmed layout for engineering-pe-skills); falls back to repo root
    otherwise.
    """
    skills_root = repo_root / "skills" if (repo_root / "skills").is_dir() else repo_root
    records = []
    for entry in sorted(skills_root.iterdir()):
        if not entry.is_dir() or entry.name.startswith("."):
            continue
        file_hashes = []
        description = ""
        for readme_name in ("SKILL.md", "README.md"):
            readme = entry / readme_name
            if readme.exists():
                text = readme.read_text(errors="replace")
                for line in text.splitlines():
                    line = line.strip()
                    if line and not line.startswith("#") and not line.startswith("---"):
                        description = line[:200]
                        break
                break
        for f in sorted(entry.rglob("*")):
            if f.is_file() and not has_skip_part(f.relative_to(repo_root).parts):
                file_hashes.append(sha256_of(f))
        combined = hashlib.sha256("".join(file_hashes).encode()).hexdigest()
        records.append(
            {
                "repo": repo_name,
                "rel_path": str(entry.relative_to(repo_root)),
                "ext": None,
                "asset_type": "knowledge",
                "description": description,
                "file_count": len(file_hashes),
                "sha256": combined,
                "mtime": int(entry.stat().st_mtime),
            }
        )
    return records


def write_placeholders() -> None:
    entries = []
    for repo_name in PLACEHOLDER_REPOS:
        entries.append(
            {
                "repo": repo_name,
                "path": f"../{repo_name}",
                "note": (
                    "No hardware assets cataloged yet. When this repo starts hardware "
                    "work, add its assets to index/_raw/ via inventory_scan.py and to "
                    "the type manifests in SecureControllers/index/."
                ),
            }
        )
    OUTPUT_ROOT.mkdir(parents=True, exist_ok=True)
    with (OUTPUT_ROOT / "placeholders.json").open("w") as f:
        json.dump(entries, f, indent=2, sort_keys=True)
        f.write("\n")


def detect_duplicates(all_records: list[dict]) -> None:
    """Annotate records in-place with possible_duplicate / renamed_duplicate flags."""
    by_basename: dict[tuple[str, str], list[dict]] = {}
    by_hash: dict[str, list[dict]] = {}
    for rec in all_records:
        if rec["asset_type"] == "knowledge":
            continue
        basename_key = (Path(rec["rel_path"]).name, rec["ext"])
        by_basename.setdefault(basename_key, []).append(rec)
        by_hash.setdefault(rec["sha256"], []).append(rec)

    for group in by_basename.values():
        repos_in_group = {r["repo"] for r in group}
        if len(repos_in_group) > 1:
            for r in group:
                r["possible_duplicate"] = True
                r["duplicate_hash_match"] = len({g["sha256"] for g in group}) == 1

    for sha, group in by_hash.items():
        repos_in_group = {r["repo"] for r in group}
        basenames_in_group = {Path(r["rel_path"]).name for r in group}
        if len(repos_in_group) > 1 and len(basenames_in_group) > 1:
            for r in group:
                r["renamed_duplicate"] = True


def main() -> None:
    OUTPUT_ROOT.mkdir(parents=True, exist_ok=True)
    raw_dir = OUTPUT_ROOT / "_raw"
    raw_dir.mkdir(parents=True, exist_ok=True)

    all_records: list[dict] = []
    per_repo: dict[str, list[dict]] = {}

    for repo_name in ASSET_REPOS:
        records = scan_repo(repo_name)
        per_repo[repo_name] = records
        all_records.extend(records)

    for repo_name in KNOWLEDGE_REPOS:
        records = scan_repo(repo_name, is_knowledge=True)
        per_repo[repo_name] = records
        all_records.extend(records)

    detect_duplicates(all_records)

    for repo_name, records in per_repo.items():
        with (raw_dir / f"{repo_name}.json").open("w") as f:
            json.dump(records, f, indent=2, sort_keys=True)
            f.write("\n")
        print(f"{repo_name}: {len(records)} records")

    write_placeholders()
    print(f"placeholders.json: {len(PLACEHOLDER_REPOS)} entries")


if __name__ == "__main__":
    main()
