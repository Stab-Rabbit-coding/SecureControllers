# Skills Index

128 agent skills available under `.claude/skills/` in this repo (local Claude Code, and any cloud/web session running against this repo or branch). Token-optimized for lookup: scan the table for your task, then invoke the skill by directory name — do not read every `SKILL.md` to find the right one.

Regenerate with `python3 tools/build_skills_index.py` after adding, removing, or editing any skill. Machine-readable form: `index/skills.json`.

For other reusable assets in this repo (datasheets, KiCad symbols/footprints, mechanical shapes, shared scripts) see [`../../INDEX.md`](../../INDEX.md) at the repo root — same lookup pattern, different asset types.

## Security & SOC Operations

| Skill | Description |
| --- | --- |
| `01-recon-osint` | Passive and active reconnaissance, subdomain enumeration, DNS analysis, technology fingerprinting, and OSINT data correlation for authori... |
| `02-vulnerability-scanner` | Dependency auditing, CVE detection, configuration security review, CVSS scoring, and prioritized vulnerability reporting |
| `03-exploit-development` | Proof-of-concept development, payload crafting, shellcode analysis, and exploitation technique research for authorized security testing |
| `04-reverse-engineering` | Binary analysis, assembly interpretation, disassembly, decompilation, firmware RE, and protocol reverse engineering |
| `05-malware-analysis` | Static and dynamic malware analysis, YARA rule generation, sandbox configuration, behavioral profiling, and malware family classification |
| `06-threat-hunting` | IOC extraction, threat intelligence correlation, MITRE ATT&CK mapping, hunt hypothesis generation, and detection rule creation |
| `07-incident-response` | IR playbook execution, evidence collection, forensic timeline analysis, memory forensics, and post-incident reporting following NIST SP 8... |
| `08-network-security` | Network traffic analysis, PCAP parsing, IDS/IPS rule creation, firewall configuration auditing, and network anomaly detection |
| `09-web-security` | OWASP Top 10 testing, injection vulnerability detection, API security assessment, authentication testing, and web vulnerability reporting... |
| `10-cloud-security` | AWS/Azure/GCP security auditing, container and Kubernetes hardening, Infrastructure as Code scanning, and cloud compliance assessment |
| `11-csoc-automation` | SOC alert triage, incident playbook automation, escalation workflows, shift reporting, and SOC KPI tracking |
| `12-log-analysis` | Security log parsing, anomaly detection, SIEM query building, Sigma rule creation, and correlation rule development across Splunk, Elasti... |
| `13-crypto-analysis` | SSL/TLS auditing, cipher suite analysis, hash algorithm identification, encryption implementation review, and cryptographic weakness dete... |
| `14-red-team-ops` | Authorized red team engagement planning, C2 architecture design, attack methodology, lateral movement strategy, OPSEC, and professional r... |
| `15-blue-team-defense` | System hardening, detection engineering, security baseline monitoring, patch management, defense-in-depth architecture, and security post... |
| `16-ai-llm-security` | LLM and AI application security testing — prompt injection, jailbreak resistance, OWASP LLM Top 10 (2025), RAG and agent/tool-use securit... |
| `17-mobile-security` | Android and iOS application security testing — static and dynamic analysis, APK/IPA inspection, OWASP MASVS/MASTG verification, secure-st... |
| `18-ot-ics-security` | Operational Technology and industrial control system security — Purdue model segmentation, industrial protocol analysis (Modbus, DNP3, S7... |
| `19-grc-compliance` | Governance, risk, and compliance — risk assessment and scoring, control mapping across NIST CSF 2.0 / ISO 27001:2022 / SOC 2 / CIS Contro... |

## GRC & Compliance

| Skill | Description |
| --- | --- |
| `cis-controls` | Expert CIS Controls v8 (CIS Top 18) advisor — implementation group scoping (IG1/IG2/IG3), control gap assessments, safeguard-level guidan... |
| `ear` | Export Administration Regulations (EAR, 15 CFR Parts 730-774) compliance advisor — ECCN classification across all 10 CCL categories and 5... |
| `fedramp` | Expert guidance for FedRAMP certification and compliance under CR26 (FedRAMP Consolidated Rules for 2026). Use this skill whenever a user... |
| `gdpr-compliance` | Expert GDPR compliance assistant covering all four core workflows: (1) auditing code and systems for GDPR violations, (2) drafting GDPR-c... |
| `iso27001` | Expert ISO 27001 compliance assistant for security and compliance teams. Use this skill whenever a user asks about ISO 27001 or ISO/IEC 2... |
| `iso27701` | Expert ISO 27701 Privacy Information Management System (PIMS) compliance advisor. Use this skill whenever a user asks about ISO/IEC 27701... |
| `iso42001` | Expert ISO 42001 AI Management System (AIMS) compliance advisor. Use this skill whenever a user asks about ISO/IEC 42001:2023, AI governa... |
| `itar` | Expert ITAR compliance advisor for US defense contractors, exporters, and manufacturers. Use this skill for any question about 22 CFR Par... |
| `nist-800-53` | NIST SP 800-53 Rev 5 compliance advisor — all 20 control families (AC, AT, AU, CA, CM, CP, IA, IR, MA, MP, PE, PL, PM, PS, PT, RA, SA, SC... |
| `nist-ai-rmf` | Expert NIST AI Risk Management Framework (AI RMF 1.0) advisor covering all four functions: GOVERN, MAP, MEASURE, MANAGE. Use this skill w... |
| `nist-csf` | Expert NIST Cybersecurity Framework (CSF) advisor covering CSF 2.0 and CSF 1.1. Use this skill whenever a user asks about NIST CSF, cyber... |
| `secure-controller-assurance` | Verify that controller hardware — servos, ESCs, flight/motion controllers, sensor nodes, Raspberry Pi HATs, and BeagleBone capes — has ze... |
| `tsa-compliance` | Expert TSA cybersecurity compliance advisor for critical infrastructure owners and operators. Use this skill whenever a user asks about T... |

## Engineering (PE-aligned)

| Skill | Description |
| --- | --- |
| `aeronautical-engineering` | Aeronautical and aerospace engineering analysis with authoritative citations — airfoil and wing aerodynamics, lift/drag/moment build-up, ... |
| `control-systems-engineering` | Control systems engineering aligned to the NCEES PE Control Systems exam — PID tuning, loop dynamics, transfer functions, stability and f... |
| `mechanical-engineering` | Mechanical engineering design and analysis aligned to the NCEES PE Mechanical exam — machine design, stress and fatigue, shafts, bearings... |
| `statics-and-dynamics` | Statics and rigid-body dynamics at FE level — free-body diagrams, equilibrium, trusses and frames, centroids and moments of inertia, fric... |

## PCB / KiCad / Electronics

| Skill | Description |
| --- | --- |
| `autoroute` | Auto-route a KiCad PCB using FreeRouting — connects all ratsnest traces automatically, then reports track count, via count, and any remai... |
| `bom` | BOM (Bill of Materials) management for electronics projects — the primary orchestrator skill that coordinates DigiKey, Mouser, LCSC, elem... |
| `create` | Generate KiCad 10 schematics and PCB layouts from natural language prompts. Writes production-ready .kicad_sch and .kicad_pcb files direc... |
| `datasheets` | Extract structured specifications from electronic component datasheet PDFs — pinouts, electrical characteristics, peripherals, topology, ... |
| `digikey` | Search DigiKey for electronic components and download datasheets — primary source for prototype orders and the preferred API method for f... |
| `element14` | Search Newark, Farnell, and element14 for electronic components — find parts by MPN or distributor part number, check pricing/stock, down... |
| `emc` | EMC pre-compliance risk analysis for KiCad PCB designs — 18 check categories, 44 rule IDs covering ground planes, decoupling, I/O filteri... |
| `jlcpcb` | JLCPCB PCB fabrication and assembly — BOM/CPL generation, basic vs extended parts, assembly constraints, design rules, ordering workflow.... |
| `kicad` | Analyze KiCad projects and PDF schematics: schematics, PCB layouts, Gerbers, footprints, symbols, netlists, and design rules. Reviews des... |
| `kidoc` | Generate professional engineering documentation from KiCad projects — Hardware Design Descriptions (HDD), CE Technical Files, Interface C... |
| `lcsc` | Search LCSC Electronics for electronic components — find parts by LCSC number (Cxxxxx) or MPN, check stock/pricing, download datasheets, ... |
| `mouser` | Search Mouser Electronics for electronic components — secondary source for prototype orders. Find parts, check pricing/stock, download da... |
| `pcb-designer` | Comprehensive PCB design for embedded / IoT / mixed-signal projects. Use this skill whenever the user mentions PCB design, schematic capt... |
| `pcb-engineer` | Senior EE and PCB designer: requirements through manufacturing. Schematic design, component selection with alternatives, BOM generation, ... |
| `pcbway` | PCBWay PCB fabrication and assembly — turnkey/consigned assembly, design rules, ordering workflow. Alternative to JLCPCB for manufacturin... |
| `spice` | Run automatic SPICE simulations on subcircuits detected from KiCad schematic analysis — validates filter frequencies, divider ratios, opa... |

## 3D / Mechanical Design

| Skill | Description |
| --- | --- |
| `3d-print-design` | Design 3D-printable parts, enclosures, and mechanical components. Full workflow: requirements, CAD (FreeCAD/OpenSCAD), DFM, manufacturing... |
| `openfoam-cfd` | Set up turbulent flow simulations in OpenFOAM with automated case generation |
| `openscad` | Create and render OpenSCAD 3D models. Generate preview images from multiple angles, extract customizable parameters, validate syntax, and... |

## Compound Engineering (ce-*)

| Skill | Description |
| --- | --- |
| `ce-babysit-pr` | Babysits or watches an open GitHub PR until merge-ready, continuously reacting to review comments, CI failures, and routine base movement... |
| `ce-brainstorm` | Explore vague or ambitious ideas into a right-sized requirements-only unified plan. Use when the user wants to brainstorm, think through ... |
| `ce-code-review` | Structured code review for bugs, regressions, tests, and standards. Use before PRs or when asked for review; report-only by default, with... |
| `ce-commit` | Create a git commit with a clear, value-communicating message. Use when the user asks to commit/save staged or unstaged changes with a re... |
| `ce-commit-push-pr` | Commit, push, and open a PR. Use when asked to ship/open a PR, or for PR-description-only flows like writing, rewriting, or describing a ... |
| `ce-compound` | Document a recently solved problem as a durable repo learning, or capture project vocabulary in CONCEPTS.md. Use when capturing a learnin... |
| `ce-compound-refresh` | Refresh the repo's captured learnings against the current codebase. Use when auditing stale, overlapping, superseded, or drifted learning... |
| `ce-debug` | Diagnosis loop for bugs and failing behavior. Use for errors, stack traces, regressions, failed tests, issue-tracker bugs, stuck investig... |
| `ce-doc-review` | Review requirements, plans, or specs with role-specific lenses. Use when the user wants to improve an existing planning document. |
| `ce-dogfood` | Hands-off, diff-scoped browser QA of the active branch: maps user flows, drives a real browser, autonomously fixes small breakages with r... |
| `ce-explain` | Create a durable, visual teaching artifact — plus an optional check-in (predict-then-reveal for diffs, corrected exercises) that makes it... |
| `ce-handoff` | Create a session handoff for another agent, or resume, find, and read any user-selected continuity source. Use when work or conversation ... |
| `ce-ideate` | Generate and evaluate grounded ideas. Use when the user asks for ideas, improvements, surprising options, or AI-generated directions befo... |
| `ce-optimize` | Run metric-driven optimization loops. Use when improving measurable outcomes such as search relevance, clustering quality, build performa... |
| `ce-plan` | Create structured plans for multi-step work, including software and non-software tasks. Use when asked to plan, break down implementation... |
| `ce-polish` | Start the dev server, inspect the feature in browser, and iterate on polish. |
| `ce-pov` | Give a decisive, project-grounded point of view in the subject's own shape: a graded verdict on an external-adoption question, a holistic... |
| `ce-product-pulse` | Generate time-windowed product pulse reports from configured signals. |
| `ce-promote` | Draft launch or promotion copy for a shipped feature. |
| `ce-proof` | Publish, read, comment on, or edit markdown in Proof. Use for Proof links, sharing specs/plans/drafts, or publish handoffs from planning ... |
| `ce-resolve-pr-feedback` | Resolve PR review feedback. Use when addressing review comments, resolving review threads, or fixing code-review feedback. |
| `ce-retune` | Retune a skill corpus for a new model, measurement-first: mine the run archive for a baseline, establish a noise floor, audit the corpus ... |
| `ce-riffrec-feedback-analysis` | Analyze Riffrec feedback captures from bundles or standalone recordings. Always load for `riffrec-*.zip`, `session.json` + `events.json` ... |
| `ce-setup` | Check Compound Engineering health and repo-local config. |
| `ce-simplify-code` | Simplify settled, recently changed code for clarity, reuse, quality, and efficiency while preserving behavior. Use after implementation a... |
| `ce-strategy` | Create or update STRATEGY.md. Use when starting a product, changing direction or roadmap, or when ce-ideate, ce-brainstorm, or ce-plan ne... |
| `ce-sweep` | Sweep configured feedback sources (Slack, GitHub Issues; email experimental) for new items: acknowledge at source, analyze recordings, ve... |
| `ce-test-browser` | Run browser tests for pages affected by the current branch or PR. |
| `ce-test-xcode` | Build and test iOS apps on simulator with XcodeBuildMCP. |
| `ce-work` | Execute a plan or concrete work prompt end-to-end. Use when implementing from a plan document, a spec path, or a clear build request; use... |
| `ce-worktree` | Set up isolated git worktrees — create a new branch for fresh work, or attach a worktree to an existing branch/PR/commit to work on it in... |
| `lfg` | Run the full autonomous shipping pipeline end-to-end, hands-off with no check-ins: plan, implement, review and fix, commit, push a branch... |

## Project & Workflow Governance

| Skill | Description |
| --- | --- |
| `cosmos-compose` | Generate cosmos-compose.json files and administer Cosmos Cloud. Covers services, volumes, routes, reverse proxy, OpenID/SSO, Constellatio... |
| `deprecation-and-migration` | Manages deprecation and migration. Use when removing old systems, APIs, or features. Use when migrating users from one implementation to ... |
| `disposition-ledger` | Use when review findings from plan-auditor, code-auditor, pr-reviewer, /code-review, or any audit agent need tracking to a resolution bef... |
| `documentation-and-adrs` | Records decisions and documentation. Use when making architectural decisions, changing public APIs, shipping features, or when you need t... |
| `doubt-driven-development` | Subjects every non-trivial decision to a fresh-context adversarial review before it stands. Use when correctness matters more than speed,... |
| `flaky-tests` | Diagnoses flaky and intermittently-failing tests. Use when a test passes and fails without a code change, when the reflex fix is "widen t... |
| `fleet-audit-loop` | Use when auditing a set of agent or skill definitions and one sweep is not enough - each round points a different auditor at a different ... |
| `fleet-qa-loop` | Use to QA a target until clean - runs mechanical linters (auto-fix) first, then loops the qa/audit subagent fleet, fixing findings until ... |
| `git-workflow-and-versioning` | Structures git workflow practices. Use when making any code change. Use when committing, branching, resolving conflicts, or when you need... |
| `github-actions` | Create, debug, and review GitHub Actions workflows. Covers reusable workflows, composite actions, custom JS/Docker actions, matrix builds... |
| `idea-refine` | Refines raw ideas into sharp, actionable concepts through structured divergent and convergent thinking. Use when an idea is still vague, ... |
| `incremental-implementation` | Delivers changes incrementally. Use when implementing any feature or change that touches more than one file. Use when you're about to wri... |
| `negative-controls` | Checks that a control can actually fail before you trust it passing. Use when writing or reviewing a test, lint rule, CI gate, feature fl... |
| `planning-and-task-breakdown` | Breaks work into ordered tasks. Use when you have a spec or clear requirements and need to break work into implementable tasks. Use when ... |
| `project-overseer` | Full-cycle project management across a whole repository: capture requirements, decompose into a Work Breakdown Structure, estimate effort... |
| `readme-conventions` | Use when writing or rewriting a README, or when a release adds capabilities the README does not yet describe. Covers the section order, b... |
| `shipping-and-launch` | Prepares production launches. Use when preparing to deploy to production. Use when you need a pre-launch checklist, when setting up monit... |
| `source-driven-development` | Grounds every implementation decision in official documentation. Use when you want authoritative, source-cited code free from outdated pa... |
| `spec-driven-development` | Creates specs before coding. Use when starting a new project, feature, or significant change and no specification exists yet. Use when re... |
| `upstream-prs-to-hermes-agent` | Sends a change from a fork up to NousResearch/hermes-agent, or reviews a branch before it goes. Use when preparing an upstream PR, writin... |
| `wbs-generator` | Generate and validate Work Breakdown Structures with automated decomposition |
| `wiki-first` | Use before any web search - query the local wiki corpus first for a verified, cited answer or an explicit refusal, then ingest what the w... |

## Code Quality & Dev Practice

| Skill | Description |
| --- | --- |
| `api-and-interface-design` | Guides stable API and interface design. Use when designing APIs, module boundaries, or any public interface. Use when creating REST or Gr... |
| `browser-testing-with-devtools` | Tests in real browsers via Chrome DevTools MCP. Use when building or debugging anything that runs in a browser. Use when you need to insp... |
| `code-quality` | Write production-grade code: secure, efficient, maintainable. Applies to all languages. Includes code review mode producing a downloadabl... |
| `context-engineering` | Optimizes agent context setup. Use when starting a new session, when agent output quality degrades, when switching between tasks, or when... |
| `debugging-and-error-recovery` | Guides systematic root-cause debugging. Use when tests fail, builds break, behavior doesn't match expectations, or you encounter any unex... |
| `frontend-design` | Design and build production-grade web UIs. WCAG 2.2 AA, Nielsen's heuristics, AI trope blacklist. Covers layout, typography, colour, anim... |
| `observability-and-instrumentation` | Instruments code so production behavior is visible and diagnosable. Use when adding logging, metrics, tracing, or alerting. Use when ship... |
| `performance-optimization` | Optimizes application performance. Use when performance requirements exist, when you suspect performance regressions, or when Core Web Vi... |
| `security-and-hardening` | Hardens code against vulnerabilities. Use when handling user input, authentication, data storage, or external integrations. Use when buil... |
| `test-driven-development` | Drives development with tests. Use when implementing any logic, fixing any bug, or changing any behavior. Use when you need to prove that... |

## Meta / Tooling

| Skill | Description |
| --- | --- |
| `claude-security` | The Claude Security menu — pick a job: scan the codebase (the whole repository or a scoped part of it), scan changes (this branch's or a ... |
| `find-skills` | Helps users discover and install agent skills when they ask questions like "how do I do X", "find a skill for X", "is there a skill that ... |
| `model-bakeoff` | Use when choosing between models or prompts by measuring them against ground truth - benchmarking extraction, classification or OCR candi... |
| `remember` | Save session state for clean continuation next session. |
| `skill-creator` | Create new skills, modify and improve existing skills, and measure skill performance. Use when users want to create a skill from scratch,... |

## Misc

| Skill | Description |
| --- | --- |
| `copywriting` | Multi-domain writing: journalism, technical writing, narrative non-fiction, conversion copywriting. AI-trope blacklist with a verificatio... |
| `research` | Use before dispatching any research subagent or doing external lookups directly. The house layer over generic deep research: source order... |
| `songwriting` | Use when writing, structuring, or polishing a song or its lyrics, including turning a rough idea or lyric sheet into a sectioned song wit... |
| `svg-illustrator` | Hand-author stylised SVG illustrations - covers, figures, icons, diagrams - that read clearly at a glance and survive print-PDF rendering... |
