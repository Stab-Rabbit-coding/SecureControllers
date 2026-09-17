# Project Overseer — User Manual

Turn an AI assistant into a project manager that keeps its own records.

Derived from **[Project Overseer](https://github.com/tigerhu598-dot/project-overseer)** by
TIGERHU, MIT License, Copyright (c) 2026 tigerhu598-dot. The upstream notice is retained in
`LICENSE.upstream-MIT`. See `ATTRIBUTION.md` for the full provenance chain, the record of what
this revision changed, and the security review.

---

## 1. What it is

A project-management framework that runs entirely on plain Markdown files. It takes a project
from a vague idea to finished work through five phases — **requirements, prior art,
decomposition, execution, close-out** — and keeps a written record at every step.

No configuration, no API keys, no external services, no scripts. It works offline.

## 2. The problem it solves

| Symptom | What the skill does about it |
| --- | --- |
| The assistant loses track once the conversation gets long | One file per task; entering a task loads only that file |
| Task 7 is built against assumptions task 2 invalidated | Finished tasks extract what they decided and push it into dependents |
| A changed requirement means starting over | Impact assessment identifies only what actually has to be reopened |
| Progress lives in your head | Derived dashboard, and every decision written down with its reason |
| Work drifts from the project's own conventions | Standards agreed up front, or inherited from the repo's policy file |

The unifying idea: **nothing is remembered, everything is written down.** A conversation that
ends unexpectedly costs you the last few minutes, not the project.

## 3. Two modes

The skill checks what kind of directory it's in before doing anything, and says which mode it
picked.

**Governed mode** — the repository already has a policy file (`AGENTS.md` or a `CLAUDE.md`
pointing to one) and its own task files (`WBS.md`, `TODO.md`). The skill works *inside* that
structure: it reads the policy, edits the existing task files in their own format, and follows
the repo's rules on citations, units, commits, and revisions. It does **not** create a second
task system, because two task lists means neither one can be trusted.

**Greenfield mode** — no governance exists. The skill creates and owns `projects/<name>/` with
its own plan, standards, references, state, and task files.

If it guesses wrong, tell it — mode is announced precisely so you can correct it before any
files are written.

## 4. A session, end to end

```text
You:  project overseer
AI:   Greenfield mode — no AGENTS.md or WBS.md here, so I'll create projects/.
      What's the project, and what does "done" look like?

You:  A blog — registration, login, posts, comments. Three people, two weeks.
AI:   (asks about constraints, risks, resources; writes plan.md)
      Requirements are in projects/blog/plan.md. Please read it and tell me
      what I got wrong.

You:  requirements done
AI:   Want me to research prior art? Anything I bring back gets its licence
      and URL recorded before it goes anywhere near the project.

You:  skip research
AI:   (reads templates, writes project-standards.md) Standards drafted.

You:  standards confirmed
AI:   (writes the WBS and estimate table)

      | Task              | opt/likely/pess | Feasibility | Depends on |
      |-------------------|-----------------|-------------|------------|
      | 1.1 Schema        | 2h / 3h / 5h    | High        | -          |
      | 1.2 Registration  | 3h / 4h / 8h    | High        | 1.1        |
      | 2.1 Post CRUD     | 5h / 8h / 20h   | Medium      | 1.1        |

      2.1's spread is wide — that's where the schedule risk is.

You:  approved
AI:   (creates task files)

You:  start schema
AI:   (loads only that task; shows its pre-start notes)
      ...discussion...
You:  done
AI:   Complete. Extracted: user and post table schemas, naming convention,
      "soft delete, not hard — audit requirement".
      Sent to 1.2 and 2.1 as pre-start notes. Please check the extraction.

You:  add requirement: admin panel
AI:   Impact of: admin panel

        1.1 Schema      [COMPLETED]  → needs a role column; reopen
        1.2 Registration[COMPLETED]  → not affected
        2.1 Post CRUD   [pending]    → scope grows; 8h → 12h likely
        2.4 Admin auth  [NEW]        → new task

        Progress goes from 2/6 to 2/7 with 1 reopened. Approve?
```

## 5. Commands

All commands are English; plain synonyms work.

**Phases** — `project overseer` · `requirements done` · `research` / `skip research` ·
`integrate references` · `standards confirmed` · `approved`

**Execution** — `start <task>` · `back to master` · `done` · `status` · `notices <task>`

**Changes** — `add requirement <desc>` · `impact analysis` · `reopen <task>`

**Close-out** — `time summary` · `archive` · `archive list` · `restore <project>`

## 6. What makes it different from a task list

**Impact propagation.** When a task completes, the skill extracts eight categories of
consequence — data structures, interface contracts, conventions, file changes, dependencies and
config, key decisions *including what was ruled out*, reusable utilities, and risks — then writes
them into the tasks that depend on it. Later tasks open with earlier decisions already in front
of them.

It errs toward over-notifying. A note you skim costs seconds; a note never delivered costs a
rebuild.

**Change management that costs what the change costs.** Every requirement change is assessed
against *all* tasks including finished ones, reported with the honest new progress figure, and
applied only after approval. Reopened tasks keep their discussion log, so rework is incremental.

**Gates you control.** No phase advances on the assistant's inference that things "seem done."

**Integrity checks.** Every context switch verifies the files exist, parse, and agree with each
other — and *reports* problems rather than silently repairing them, because auto-repair destroys
the evidence of what went wrong.

## 7. External research is vetted

Prior-art research is available but gated, for two reasons.

**Licence.** Anything integrated without a licence check becomes a violation that lives in your
repository and propagates into derivatives. So every source is recorded with a validated URL, the
exact section relied on, and the licence as the source actually states it — and compatibility is
confirmed *before* integration, never after. Absent licence means no permission, not implied
permission.

**Untrusted content.** Text fetched from a web page or repository is data, not instruction. If
retrieved material contains directives aimed at an AI agent, the skill reports that fact and does
not act on them. Requirements come from you.

The reference catalog belongs to the project — `projects/<name>/REFERENCES.md` in greenfield
mode, or the repository's own catalog in governed mode. Nothing is ever fabricated: a URL that
wasn't retrieved is not validated, and a section number that wasn't checked is marked "requires
verification" rather than guessed.

## 8. Layout

```text
project-overseer/
├── SKILL.md                  # Workflow, modes, commands, dashboard
├── README.md                 # This manual
├── ATTRIBUTION.md            # Provenance, changes, security review
├── LICENSE.upstream-MIT      # Retained upstream MIT notice
├── references/               # Operational detail, loaded on demand
│   ├── governed-mode.md
│   ├── greenfield-mode.md
│   ├── execution-protocol.md
│   ├── impact-propagation.md
│   ├── change-management.md
│   └── external-source-vetting.md
└── templates/                # Standards, merged in greenfield mode
    ├── typescript-javascript.md · python.md · go.md · rust.md
    ├── nextjs-fullstack.md · express-backend.md · fastapi-backend.md
    ├── django-backend.md · go-web-service.md · rust-backend.md
    ├── hardware-cad.md · electronics-pcb.md
    └── ai-specific.md · anti-patterns.md · testing-conventions.md
        git-conventions.md · logging-observability.md
```

Greenfield projects look like this:

```text
projects/<name>/
├── plan.md                # Requirements, WBS, estimates, revision history
├── project-standards.md   # Merged from templates/, confirmed by you
├── REFERENCES.md          # Vetted external sources
├── status.json            # Task state
└── tasks/<task-name>.md   # Discussion log, pre-start notes, impact output
```

Governed projects get no new files — the skill edits the repo's existing `WBS.md`/`TODO.md`
pairs, and derives state from checkbox state and git history rather than adding a state file that
would immediately start drifting out of sync.

## 9. Hardware projects

`templates/hardware-cad.md` and `templates/electronics-pcb.md` extend the skill to physical work.
The substantive difference is that **budgets are task outputs, not afterthoughts**: mass delta and
new total, CG shift, power draw, and clearance margin are quoted for every change, and "TBD" is
not an accepted value — a deferred number is a skipped number, discovered at fabrication.

They also add the gates that matter for physical work: mesh validation after every model edit,
ERC and DRC after every schematic or layout change, footprints verified against the datasheet for
the exact ordered part, and units kept honest (`lbm` for mass, `lbf` for force, never a bare
"lb").

## 10. Installation

Place the `project-overseer/` folder — `SKILL.md`, `references/`, and `templates/` together — in
your agent's skills directory. For Claude Code that is `~/.claude/skills/` for personal use or
`.claude/skills/` inside a project. The `references/` and `templates/` folders are not optional;
`SKILL.md` points into both.

For agents that only read a single instruction file, reference `SKILL.md` from that file and keep
the folder structure intact alongside it.

## 11. Upstream corrections

Two defects in the upstream v4.0 documentation, noted here so anyone comparing against it isn't
confused:

- The upstream README listed a `templates/react-frontend.md` and claimed 16 template files. That
  file was not present in the distribution; there were 15. This revision ships 17 (15 upstream,
  minus nothing, plus the two hardware templates) and the list above matches what is on disk.
- The upstream README advertised a "Feature Toggles" config file, while its own `SKILL.md`
  recorded that toggles were removed in v3.1 and replaced with direct prompts. There is no toggle
  file. Behaviour is chosen by answering the skill's questions.

---

*Original work: [Project Overseer](https://github.com/tigerhu598-dot/project-overseer) by
TIGERHU — MIT License, Copyright (c) 2026 tigerhu598-dot, notice retained in
`LICENSE.upstream-MIT`. This revision is licensed CC BY-SA 4.0. See `ATTRIBUTION.md`.*
