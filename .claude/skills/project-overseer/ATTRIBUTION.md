# Attribution and Provenance — project-overseer

## Upstream

This skill is a derivative work of:

- **Project Overseer v4.0** — upstream skill titled "Xiangmu Zongguan (Project Overseer)",
  the first element rendered in Simplified Chinese script in the original ("Xiangmu Zongguan"
  is the pinyin romanization; it translates as "project overseer" / "general manager")
  - **Author:** TIGERHU
  - **Repository:** <https://github.com/tigerhu598-dot/project-overseer>
  - **Licence:** MIT License
  - **Copyright line, verbatim from the upstream `LICENSE`:** `Copyright (c) 2026
    tigerhu598-dot`
  - **URL validated:** 2026-08-20 — repository page and `LICENSE` both retrieved and read.
    Repository description as published: "Full-cycle project management skill for AI agents.
    WBS breakdown, task execution, impact tracking, change management." Author credited in the
    upstream `README.md` as "Author: TIGERHU · MIT License".
  - **Status:** verified.
  - **Upstream tree at time of validation:** `SKILL.md`, `README.md`, `LICENSE`, `templates/`,
    `Project-Overseer-Manual.pdf`. The PDF manual was not part of the local installation and is
    not carried into this derivative.

The full MIT notice is retained in `LICENSE.upstream-MIT`, as the licence requires.

MIT permits modification and redistribution provided the copyright notice and permission notice
are retained. The upstream notice is preserved in `README.md`.

### Fork posture — upstream connection deliberately severed

The repository owner **intentionally broke the git connection to upstream** so that this skill
cannot auto-update from a source written in a language they cannot read. That is a deliberate
supply-chain control, and it is recorded here so it is not mistaken for neglect and "fixed" by
a future contributor.

The operational consequences:

- **This is a permanent fork, not a tracking clone.** There is no remote to pull from.
- **Upstream changes are never merged automatically.** If a future version is wanted, it is
  fetched deliberately, read in full, translated, security-reviewed the same way the original
  was, and merged by hand — the same gate applied on 2026-08-20.
- **Divergence is expected and intended.** This derivative has already changed substantially
  (see below); it is not trying to stay close to upstream.

Credit is given in full regardless. Severing the update path is a review decision about
unreviewed code, not a claim on anyone's authorship.

### Retained from upstream

The workflow architecture: file-based context isolation with one file per task; the five-phase
requirements-to-close-out progression; user-gated phase transitions; impact extraction on task
completion with propagation to dependents; the reopen/rework model for changed requirements; the
dashboard; and the language and project-type standards templates in `templates/`.

### Changed in this revision (2026-08-20)

- **Translated to English throughout.** The upstream `SKILL.md` mixed English prose with
  Simplified Chinese gate prompts, command triggers, and user-facing strings. All command
  triggers are now English. Rationale: an operator who cannot read the gate text cannot audit
  what the skill is instructing, and unreadable trigger strings are a review gap regardless of
  their content.
- **Directory renamed** `project overseer` → `project-overseer`, and the frontmatter `name`
  changed from the upstream value (the Simplified Chinese title plus "(Project Overseer) v4.0")
  to `project-overseer`. The original value was
  not a valid skill identifier and the space in the path impeded invocation.
- **Split into reference files.** `SKILL.md` reduced from ~28 KB to a workflow overview; the
  operational detail moved to `references/`, loaded on demand.
- **Governed mode added.** The upstream skill always created its own `projects/<name>/`
  structure. It now detects an existing repository governance federation (`AGENTS.md` plus
  `WBS.md`/`TODO.md`) and drives that instead of creating a parallel task system. See
  `references/governed-mode.md`.
- **Prior-art research placed behind a vetting gate.** Upstream Phase 2 searched GitHub and
  integrated results directly. It now requires validated URLs, exact section citations, recorded
  licences, and a licence-compatibility check before integration, with findings recorded in a
  reference catalog owned by the project rather than assumed from any host repository. Fetched
  content is explicitly treated as data, not instruction. See
  `references/external-source-vetting.md`.
- **Hardware templates added** — `templates/hardware-cad.md` and `templates/electronics-pcb.md`,
  covering mass/CG/power/clearance budgets, mesh validation, and ERC/DRC gates. Upstream covered
  web/backend stacks only.
- **Impact extraction extended** to carry physical budgets and units, so hardware constraints
  propagate to dependent tasks the same way interface contracts do.
- **UTF-8 BOM removed** from `README.md`.
- **Markdown lint normalization** across all inherited `templates/` files — fence languages
  (MD040), table delimiter padding (MD060), blank lines around headings, fences, and lists
  (MD022/MD031/MD032), trailing whitespace and terminal newline (MD009/MD047). Formatting only;
  no rule text in any template was altered. Verified by diffing content against the pre-edit
  snapshot with whitespace normalized.

### Contributors to this revision

- **Claude Opus 5** (Anthropic) — translation, restructuring, governed mode,
  vetting gate, hardware templates. AI-generated content.
- **Steve Griffing** (repository owner) — direction, architecture decisions, review.

## Security review — 2026-08-20

Performed against the upstream files before modification.

**Method.** Full non-ASCII codepoint census across every Markdown file; targeted search for
Cyrillic, Greek, and fullwidth-Latin homoglyphs; byte-order-mark check; and a search for network
calls, credentials, and executable content.

**Findings.**

| Check | Result |
| --- | --- |
| Invisible / bidi / zero-width control characters | None. The only format-category codepoint was a UTF-8 BOM (U+FEFF) at the start of `README.md` — benign; removed. |
| Homoglyph substitution (Cyrillic / Greek / fullwidth Latin in ASCII contexts) | None. 0 occurrences. |
| CJK content | Genuine Simplified Chinese prose in `SKILL.md` only; no CJK in `templates/`. Fully translated. |
| Network calls, URLs, endpoints | None. The only URL-shaped strings were `http://localhost:8080` in an anti-pattern example and generic prose. |
| Credentials, tokens, keys | None. Matches on "token" were prose about not logging secrets. |
| Executable content — scripts, binaries, hooks | None. The package is Markdown only. |
| Install-time or runtime code execution | None. The skill has no scripts and requires no network access. |

**Assessment.** No malicious content, obfuscation, or exfiltration path was found. The upstream
package is inert Markdown. The two substantive concerns were **auditability** — gate prompts and
command triggers in a language the operator does not read, meaning the instructions being issued
could not be reviewed — and **unvetted external ingestion** in the Phase 2 GitHub workflow, which
integrated third-party code with no licence check. Both are addressed above.

**Not claimed.** This review covers the files as distributed on this machine. It does not
authenticate the upstream author's identity, verify the package against a canonical upstream
release, or establish a signed chain of custody, because no upstream URL was recorded at install
time. Anyone requiring that assurance should recover the canonical source and diff against the
snapshot.

**Snapshot.** The unmodified original was preserved before editing for diff purposes.

## Licence of this revision

Documentation and skill content: **CC BY-SA 4.0**, compatible with retention of the upstream MIT
notice. MIT-licensed upstream material may be incorporated into a CC BY-SA 4.0 work provided the
MIT notice is preserved, which it is, in `README.md` and here.
