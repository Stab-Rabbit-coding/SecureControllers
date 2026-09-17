---
name: secure-controller-assurance
description: Verify that controller hardware — servos, ESCs, flight/motion controllers, sensor nodes, Raspberry Pi HATs, and BeagleBone capes — has zero trust, IoT, industrial control, vehicle, and safety security baked in. Applies NIST IR 8259r1, IR 8425, SP 800-213/213A, SP 800-207 (zero trust), SP 800-82r3 (OT), and ISA/IEC 62443 across all design phases. Use when ideating a new controller, defining requirements, reviewing a schematic or firmware for security, closing gaps before fabrication, or producing an assurance case. Covers air, ground, marine, fixed-industrial, and SBC-carrier platforms. Trigger on "is this board secure", "security requirements for this controller", "zero trust for my ESC", "62443 for this design", "secure boot", "debug port", "threat model this board", "IoT baseline", "assurance case", "HAT security", "cape security".
version: 1.0.0
author: Claude (Opus 5) for Steve Griffing (@Stab-Rabbit-coding)
tags: [security, zero-trust, iot, ics, ot, 62443, nist, controllers, uav, usv, ugv, robotics, safety, hardware]
---

# Secure Controller Assurance

## Purpose

Apply the NIST IoT and zero-trust publication set, the NIST OT guidance, and ISA/IEC 62443
to **controller hardware you are building** — so that security is designed in at ideation
rather than assessed at the end, when the only remaining options are a respin or an accepted
risk.

This skill assesses **the board**.  It is deliberately scoped that way; see *Skill
integration* for what to hand off.

## Authorship and attribution

Per the user's global instructions, AI-generated work is distinguished from human work.
This skill's control statements, translations, and engineering commentary were authored by
**Claude Opus 5**, derived from the cited publications.  Standard text is quoted and
attributed; nothing is presented as normative text unless it is.  Cite this skill's output
as AI-generated analysis requiring engineering review.

**Never fabricate a citation.** If a clause number cannot be verified against a document in
hand, mark it `REQUIRES VERIFICATION` in `references/REFERENCES.md` and open a TODO item.
See the *Citation discipline* section below — it is the rule most likely to be violated
under time pressure.

---

## Step 1 — Establish scope (always do this first)

Answer these four before anything else.  They determine which controls apply and at which
gate.  Do not skip to findings.

| Question | Where the answer changes things |
| --- | --- |
| **What phase are we in?** Ideate / Create / Refine / QA / Sustain | Selects the workflow below |
| **What platform overlay?** A air · G ground · M marine · F fixed industrial · C carrier/SBC | `references/platform-overlays.md` — changes gates, severity, and fail-state design |
| **What is the SL-T?** (62443 security level target 1–4) | `references/ot-ics-62443.md` — determines whether a secure element is required |
| **Is it standalone, or a HAT/cape on a Linux host?** | `references/sbc-carrier-boards.md` — Overlay C adds the whole SCA-HC family |

If the user has not said, **ask** — these four change the answer materially.  Overlay C
composes with the others (a Pi HAT motor driver in a boat is `C + M`).  If one board ships
into several overlays, assess against the union and take the strictest gate.

---

## Phase workflows

### Ideate — before anything is committed to a schematic

**Goal: make the unrecoverable decisions consciously.**  Every 🔒 control in
`references/control-matrix.md` is unrecoverable or expensive after layout.  Missing one is a
respin, not a patch.

1. Establish scope (Step 1 above).
2. Define expected customers and use cases (SCA-GOV-02).  "Anyone who buys a servo" is not
   an answer and produces a control set that is simultaneously over-built and wrong.
3. Build the threat model (SCA-GOV-04).  Name the adversary capability.  Map attack paths to
   ATT&CK for ICS where the board sits in an OT context.
4. Walk the **Ideate 🔒 gate list** in the control matrix.  For each, produce a decision, not
   a to-do.  These are the ones that drive part selection and board area.
5. Produce the hardware consequences with **real numbers**, per the user's engineering
   standards: secure element BOM line and board area; potting mass and thermal impact;
   crypto cycle cost against the control-loop deadline; log storage against flash endurance.
   Quote as imperial-primary with metric in parentheses where they are physical quantities.
6. Run the four-way safety–security interaction analysis (SCA-SL-01).

**Output:** a scoped control register with 🔒 decisions made, hardware implications costed,
and open questions listed.

### Create — while the schematic and firmware are being written

1. Allocate every applicable control to HW / FW / DOC / PROC.
2. Work the Create-gate controls.
3. Check the design against the **top ten findings** list in the control matrix — they are
   ordered by how often they actually occur.
4. Where a control cannot be met, record `Partial` or `Accepted Risk` with a named owner and
   a rationale, using the N/A form in `references/nist-213a-catalog.md`.  A bare "N/A" is an
   open finding, not a closed one.

### Refine — closing gaps before release

1. Re-run the full matrix; compute coverage per family (the `19-grc-compliance` gap-analysis
   format works directly here).
2. Close out or formally accept every `Partial` and `Not Implemented`.
3. Write the assumptions down (SCA-NT-01) — this is the deliverable that transfers risk
   legitimately to the integrator.  An unstated assumption is a risk both parties think the
   other one handled.
4. Produce the SBOM (SCA-SC-01) and the vulnerability-disclosure channel (SCA-NT-03).

### QA — verification before fabrication or release

1. For every `Implemented` row, demand **evidence**, not assertion.  The evidence column in
   the control matrix says what would satisfy each one.
2. Run the negative tests — an unauthenticated command, a tampered image, a replayed frame,
   a debug attach on a production unit, a bus flood.  A control that has never been tested
   negatively is unverified.
3. Produce the assurance case from `assets/assurance-case-template.md`.
4. Confirm every citation used resolves to a `REFERENCES.md` entry with a verification
   status.

### Sustain — after release

Activities 6 and 8 of IR 8259r1: vulnerability monitoring over the support life, update
cadence, and the end-of-support notice.  See `references/nist-8259-8425.md`.

---

## Reference files

Load only what the current question needs.

| File | Load when |
| --- | --- |
| `references/control-matrix.md` | **The core.** Any assessment, any phase |
| `references/platform-overlays.md` | Always at scoping — selects gates and severity |
| `references/nist-213a-catalog.md` | Mapping to NIST capability codes; writing an N/A rationale |
| `references/nist-8259-8425.md` | Manufacturer obligations, phase mapping, what to communicate |
| `references/zero-trust-207.md` | Zero-trust questions; fail-state design; real-time conflicts |
| `references/ot-ics-62443.md` | 62443, security levels, Purdue placement, safety precedence |
| `references/vehicle-safety-aviation.md` | Air and road detail; regulatory applicability triage |
| `references/sbc-carrier-boards.md` | Any Pi HAT, BeagleBone cape, or SBC carrier |
| `references/REFERENCES.md` | **Before writing any citation** |

## Scripts

### `scripts/sca_audit.py`

Evidence scanner.  Walks a project and reports **observable evidence** for controls that
leave a filesystem trace — schematic parts, firmware symbols, repo artifacts.

```bash
python3 scripts/sca_audit.py --project /path/to/repo --overlay A --sl-target 3 \
    --output register.csv
```

It reports what it **found** and what it **could not determine**.  It never reports a control
as satisfied — only a human review, with evidence, does that.  Treat its output as the
starting point of an assessment, not the result.

## Assets

| File | Use |
| --- | --- |
| `assets/assurance-case-template.md` | The QA-phase deliverable — a structured, evidenced security argument |
| `assets/control-register-template.csv` | Per-project control register; column format matches `19-grc-compliance` |

---

## Citation discipline

The user's global instructions forbid fabricated references absolutely.  For this skill:

1. **Look up the REF-ID in `references/REFERENCES.md` first.** If the standard is not
   catalogued, add it — with a validated URL on the issuing body's own site and the specific
   sections applied — before using it.
2. **Never write an ISA/IEC 62443 CR number, an ISO clause, or a CFR section from memory.**
   The paywalled standards are catalogued at the level this skill can verify: 62443 at
   Foundational Requirement level, ISO at concept level.  Going deeper requires the document
   in hand.
3. **Never claim compliance with a standard that does not apply.** The applicability triage
   in `references/vehicle-safety-aviation.md` and `references/platform-overlays.md` exists
   because "DO-326A compliant" on a Part 107 aircraft is a false claim.  Say "DO-326A
   methodology applied; the standard does not bind this aircraft."
4. When adding a citation to a repo, follow the user's workflow: add it to that repo's own
   `REFERENCES.md` by REF-ID, then cite the REF-ID in the code or doc.

## Repository conventions this skill respects

- Findings and actions become **WBS sub-tasks in the repo's `TODO.md`**, in proper WBS style,
  so unresolved items survive the session.
- Never leave a `TODO.md` checkbox open once its own text says the item is resolved or
  superseded — close it out in the same edit.
- Cite SCA IDs (`SCA-IA-04`) in commit messages and design records so findings are traceable.
- Security-relevant design decisions get a citation in the source file docstring **and** the
  commit message.

---

## Operating rules

**Safety precedence.** A security control may never be introduced in a way that defeats a
safety function.  Where they genuinely conflict, safety wins and the residual security risk
is documented and accepted — not engineered away by weakening safety.  The inverse is also
true: a safety argument is not a license to skip security.  See `references/ot-ics-62443.md`.

**Never test on a live vehicle or live plant.** Protocol fuzzing, fault injection, bus
flooding, and negative authentication tests belong on a bench with the actuator
disconnected or a dummy load fitted.  This mirrors the passive-first rule in
`18-ot-ics-security` and applies with more force here, because this skill's tests are active
by nature.

**Evidence over assertion.** "We have secure boot" is not a finding closure.  "Tampered
stage-2 image rejected at boot, log line captured, test 2026-08-10" is.

**Report honestly.** If a control cannot be verified from what is available, say
`Not Determined` and name what would settle it.  Do not infer `Implemented` from the presence
of a part on a BOM — a secure element no firmware path uses is not a capability.

**Real numbers, not TBD.** Security decisions consume mass, power, board area, cycles, and
flash endurance.  Quote them.  Imperial-primary with metric in parentheses for physical
quantities, per the user's engineering standards.

**No offensive assistance against systems the user does not own.** This skill is for
building and assessing the user's own controllers.  It will not help defeat, spoof, or
suppress Remote ID, nor assess third-party equipment without authorization.

---

## Skill integration

| Need | Skill |
| --- | --- |
| Deployed OT network, Purdue segmentation, PCAP, ATT&CK-for-ICS paths | `18-ot-ics-security` |
| Org-level risk register, policy, SoA, gap-analysis formatting | `19-grc-compliance` |
| Schematic/PCB evidence — does the layout implement the control? | `kicad` |
| Does the chosen security IC actually do what we assumed? | `datasheets` |
| Firmware vulnerability review of the current diff | `security-review` |
| Firmware binary analysis / RE | `04-reverse-engineering` |
| Dependency CVEs for the firmware SBOM | `02-vulnerability-scanner` |
| Crypto implementation review | `13-crypto-analysis` |
| Formal document package (HDD, design review, PDF) | `kidoc` |
| Reviewing this skill's own output as a document | `compound-engineering:ce-doc-review` |

## Output format

```markdown
# Secure Controller Assurance — [Board] [Rev]
Date: [YYYY-MM-DD] | Phase: [Ideate/Create/Refine/QA/Sustain]
Overlay: [A/G/M/F/C] | SL-T: [1-4] | Assessor: [name] (AI-assisted: Claude Opus 5)

## Scope
[Board, what it controls, expected customer and use case, product boundary]

## Coverage
| Family | Implemented | Partial | Not Impl | N/A | Not Determined |

## Findings (most severe first)
### [SCA-IA-04] Debug port live in production  (Critical, Gate: Ideate 🔒)
- Capability: 213A LA/IFC | 62443 FR 1 | IR 8425 Interface Access Control 1(a)
- ATT&CK for ICS: T0839 Module Firmware
- Evidence: [what was observed, and where]
- Physical consequence: [what an attacker achieves — this drives severity, not CVSS]
- Recoverable after layout? [Yes / No — respin]
- Remediation: [specific action]

## Accepted risks
| ID | Risk | Rationale | Accepter | Review date |

## Hardware/mass/power implications
[Real numbers — imperial primary, metric in parentheses]

## TODO.md WBS items generated
[§x.y.z entries added]
```
