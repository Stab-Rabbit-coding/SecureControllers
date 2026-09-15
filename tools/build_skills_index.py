#!/usr/bin/env python3
"""Build the skills index: index/skills.json (machine) + .claude/skills/INDEX.md (human).

Reads every `.claude/skills/<name>/SKILL.md`, extracts the YAML frontmatter
`name`/`description`, and groups skills into categories by filename/topic
convention. Re-run this after adding, removing, or editing any skill under
`.claude/skills/`.
"""

import json
import re
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parents[1]
SKILLS_DIR = REPO_ROOT / ".claude" / "skills"
JSON_OUT = REPO_ROOT / "index" / "skills.json"
MD_OUT = SKILLS_DIR / "INDEX.md"

# (category label, match predicate on skill dir name) — first match wins.
CATEGORIES: list[tuple[str, callable]] = [
    ("Security & SOC Operations", lambda n: re.match(r"^\d\d-", n) is not None),
    ("GRC & Compliance", lambda n: n in {
        "iso27001", "iso27701", "iso42001", "fedramp", "nist-csf", "nist-800-53",
        "nist-ai-rmf", "tsa-compliance", "ear", "itar", "cis-controls",
        "gdpr-compliance", "secure-controller-assurance",
    }),
    ("Engineering (PE-aligned)", lambda n: n in {
        "aeronautical-engineering", "mechanical-engineering", "statics-and-dynamics",
        "control-systems-engineering",
    }),
    ("PCB / KiCad / Electronics", lambda n: n in {
        "kicad", "create", "autoroute", "emc", "spice", "bom", "datasheets",
        "digikey", "mouser", "lcsc", "element14", "jlcpcb", "pcbway", "kidoc",
        "pcb-designer", "pcb-engineer",
    }),
    ("3D / Mechanical Design", lambda n: n in {"3d-print-design", "openscad", "openfoam-cfd"}),
    ("Compound Engineering (ce-*)", lambda n: n.startswith("ce-") or n == "lfg"),
    ("Project & Workflow Governance", lambda n: n in {
        "project-overseer", "wbs-generator", "planning-and-task-breakdown",
        "spec-driven-development", "source-driven-development", "incremental-implementation",
        "git-workflow-and-versioning", "readme-conventions", "documentation-and-adrs",
        "deprecation-and-migration", "disposition-ledger", "shipping-and-launch",
        "negative-controls", "doubt-driven-development", "fleet-audit-loop",
        "fleet-qa-loop", "flaky-tests", "wiki-first", "idea-refine",
        "upstream-prs-to-hermes-agent", "github-actions", "cosmos-compose",
    }),
    ("Code Quality & Dev Practice", lambda n: n in {
        "code-quality", "test-driven-development", "debugging-and-error-recovery",
        "performance-optimization", "api-and-interface-design", "context-engineering",
        "observability-and-instrumentation", "security-and-hardening",
        "browser-testing-with-devtools", "frontend-design",
    }),
    ("Meta / Tooling", lambda n: n in {
        "skill-creator", "find-skills", "model-bakeoff", "remember", "claude-security",
    }),
    ("Misc", lambda n: True),
]


def load_skills() -> list[dict]:
    entries = []
    for d in sorted(SKILLS_DIR.iterdir()):
        if not d.is_dir():
            continue
        sm = d / "SKILL.md"
        name, desc = d.name, ""
        if sm.exists():
            text = sm.read_text(errors="replace")
            m = re.match(r"^---\n(.*?)\n---", text, re.DOTALL)
            if m:
                fm = m.group(1)
                nm = re.search(r"^name:\s*(.+)$", fm, re.MULTILINE)
                if nm:
                    name = nm.group(1).strip().strip('"').strip("'")
                # description: either inline ("description: foo") or a YAML
                # folded/literal block scalar ("description: >" / "|" followed
                # by indented lines until the next top-level key or EOF).
                ds_inline = re.search(r"^description:\s*(?![>|][+-]?\s*$)(\S.*)$", fm, re.MULTILINE)
                ds_block = re.search(r"^description:\s*[>|][+-]?\s*\n((?:[ \t]+.*\n?)*)", fm, re.MULTILINE)
                if ds_inline:
                    desc = ds_inline.group(1).strip().strip('"').strip("'")
                elif ds_block:
                    block_lines = [ln.strip() for ln in ds_block.group(1).splitlines()]
                    desc = " ".join(ln for ln in block_lines if ln)
        file_count = sum(1 for _ in d.rglob("*") if _.is_file())
        category = next(label for label, pred in CATEGORIES if pred(d.name))
        entries.append({
            "dir": d.name,
            "name": name,
            "description": desc,
            "path": f".claude/skills/{d.name}",
            "category": category,
            "file_count": file_count,
        })
    return entries


def write_json(entries: list[dict]) -> None:
    JSON_OUT.write_text(json.dumps(entries, indent=2) + "\n")


def write_md(entries: list[dict]) -> None:
    by_cat: dict[str, list[dict]] = {}
    for e in entries:
        by_cat.setdefault(e["category"], []).append(e)

    cat_order = [label for label, _ in CATEGORIES]
    lines = [
        "# Skills Index",
        "",
        f"{len(entries)} agent skills available under `.claude/skills/` in this repo "
        "(local Claude Code, and any cloud/web session running against this repo or "
        "branch). Token-optimized for lookup: scan the table for your task, then invoke "
        "the skill by directory name — do not read every `SKILL.md` to find the right "
        "one.",
        "",
        "Regenerate with `python3 tools/build_skills_index.py` after adding, removing, "
        "or editing any skill. Machine-readable form: `index/skills.json`.",
        "",
        "For other reusable assets in this repo (datasheets, KiCad symbols/footprints, "
        "mechanical shapes, shared scripts) see [`../../INDEX.md`](../../INDEX.md) at "
        "the repo root — same lookup pattern, different asset types.",
        "",
    ]
    for cat in cat_order:
        if cat not in by_cat:
            continue
        lines.append(f"## {cat}")
        lines.append("")
        lines.append("| Skill | Description |")
        lines.append("| --- | --- |")
        for e in sorted(by_cat[cat], key=lambda x: x["dir"]):
            desc = e["description"] or "(no description in frontmatter)"
            if len(desc) > 140:
                desc = desc[:137] + "..."
            desc = desc.replace("|", "\\|")
            lines.append(f"| `{e['dir']}` | {desc} |")
        lines.append("")

    MD_OUT.write_text("\n".join(lines).rstrip() + "\n")


def main() -> None:
    entries = load_skills()
    write_json(entries)
    write_md(entries)
    print(f"Indexed {len(entries)} skills -> {JSON_OUT} and {MD_OUT}")


if __name__ == "__main__":
    main()
