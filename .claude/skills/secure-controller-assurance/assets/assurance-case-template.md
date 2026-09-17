# Security Assurance Case — [Board Name] [Revision]

| Field | Value |
| --- | --- |
| Board | [name, revision, repo] |
| Date | [YYYY-MM-DD] |
| Phase | [Ideate / Create / Refine / QA / Sustain] |
| Platform overlay | [A air / G ground / M marine / F fixed / C carrier — or a union] |
| SL-T / SL-C / SL-A | [n / n / n] |
| Assessor | [name] |
| AI assistance | [model and version — e.g. Claude Opus 5; analysis requires engineering review] |
| Supersedes | [prior revision, or "none"] |

> **Structure borrowed from the cybersecurity case concept in ISO/SAE 21434
> (REF-ISO-SAE-21434), and from the practice of running security risk assessment inside the
> safety assessment in RTCA DO-326A (REF-RTCA-DO-326A).  Neither standard is claimed as
> binding unless the applicability triage in §2 says it is.**

---

## 1. Claim

> *State the top-level claim in one sentence, and make it falsifiable.*

**Claim:** [Board] is securable by its expected customer, over its stated support life, against
an adversary of capability SL-T [n], when deployed within the assumptions stated in §7.

A claim that cannot be falsified is not a claim.  "The board is secure" is not acceptable.

---

## 2. Scope and applicability

### 2.1 What this board is and does

[Function, what it actuates or senses, what it can physically cause, product boundary.]

### 2.2 Expected customer and use cases

#### (SCA-GOV-02; IR 8259r1 §3.2 Activity 1.)

[Named customer type and concrete use cases.  "Anyone who buys a servo" is not acceptable.]

### 2.3 Excluded applications

[Applications this board is **not** qualified for.  Required if the board could plausibly be
used in a stricter overlay than it was assessed against — IR 8425 requires recording known
potential misuses.]

### 2.4 Regulatory applicability triage

#### (SCA-SL-06.)

| Instrument | Applies? | Basis |
| --- | --- | --- |
| 14 CFR Part 107 | | |
| 14 CFR Part 89 (Remote ID) | | |
| DO-326A / DO-356A | | Methodology only unless type-certificated |
| ISO/SAE 21434 | | Methodology only unless road vehicle |
| ISO 13849 / IEC 62061 | | |
| ANSI/RIA R15.06 / ISO 10218 | | |
| USCG maritime cyber (33 CFR subch. H) | | MTSA-regulated only — verify citation |
| ISA/IEC 62443-4-2 | | |

**No unearned compliance claims.** Where a standard supplies methodology but does not bind,
write "methodology applied; standard does not bind this platform."

---

## 3. Threat model summary

### (SCA-GOV-04.)

| Adversary | Capability | Access assumed | Motivation |
| --- | --- | --- | --- |

### 3.1 Attack paths considered

| Path | ATT&CK for ICS | Physical consequence | Controls that interrupt it |
| --- | --- | --- | --- |

### 3.2 Explicitly out of scope

[Threats deliberately not addressed, with the reason.  An out-of-scope threat is an accepted
risk and belongs in §6.]

---

## 4. Architecture and trust boundaries

### 4.1 Zone and conduit placement

#### (SCA-OT-01.)

[Zones, conduits, SL-T per zone.  Purdue level if in an OT context.]

### 4.2 Zero trust allocation

#### (SP 800-207 §3 logical components.)

| ZT component | Where it lives | Notes |
| --- | --- | --- |
| Policy Engine | | |
| Policy Administrator | | |
| Policy Enforcement Point | **On this board** | |
| Identity / PKI | | |

### 4.3 Fail-state policy

#### (SCA-ZT-05 — the control that differs most between overlays.)

| Resource class | Behavior on policy expiry or link loss | Rationale |
| --- | --- | --- |
| Actuation | [fail-safe / fail-stop / hold — per overlay] | |
| Configuration | fail-closed | |
| Firmware update | fail-closed | |
| Key operations | fail-closed | |

State whether the fail state is **provisioned configuration** or compile-time.  If the board
ships into more than one overlay, it must be provisioned — see `platform-overlays.md`.

### 4.4 Board / host division of responsibility

#### (Overlay C only — SCA-HC-05.  Delete for standalone boards.)

| Capability | Board | Host | Notes |
| --- | --- | --- | --- |
| Unique device identity | | | |
| Secure boot | | | |
| Firmware/software update | | | |
| Network interface and auth | | | |
| Command authorization | | | |
| Logging and retention | | | |
| Time source | | | |
| Key storage | | | |
| Physical tamper detection | | | |
| Safety envelope enforcement | | | **must not be host alone** |

---

## 5. Control coverage

*(SCA-GOV-05.  Status vocabulary matches `19-grc-compliance`.)*

| Family | Implemented | Partial | Not Impl | N/A | Not Determined | Coverage |
| --- | --- | --- | --- | --- | --- | --- |
| GOV | | | | | | |
| ID | | | | | | |
| CFG | | | | | | |
| DP | | | | | | |
| IA | | | | | | |
| SU | | | | | | |
| CS | | | | | | |
| DS | | | | | | |
| ZT | | | | | | |
| OT | | | | | | |
| SL | | | | | | |
| SC | | | | | | |
| HC | | | | | | |
| NT | | | | | | |
| **Total** | | | | | | |

Full register: [link to the project's control register CSV].

### 5.1 Evidence index

#### (One row per Implemented control.  Assertion without evidence does not close a control.)

| Control | Evidence artifact | Location | Date | Verified by |
| --- | --- | --- | --- | --- |

### 5.2 Negative test results

#### (SCA verification requires that controls were tested by trying to break them.)

| Test | Control | Expected | Observed | Pass? | Date |
| --- | --- | --- | --- | --- | --- |
| Unauthenticated actuator command | SCA-ZT-02 | Rejected | | | |
| Tampered firmware image | SCA-SU-01 | Refused at boot | | | |
| Replayed authenticated frame | SCA-DP-06 | Rejected | | | |
| Debug attach on production unit | SCA-IA-04 | Fails or requires auth | | | |
| Bus flood at line rate | SCA-DS-03 | Loop deadline held or safe fail | | | |
| Power cut mid-update | SCA-SU-03 | Bootable known state | | | |
| Firmware update while armed | SCA-SU-05 | Refused | | | |
| Malformed protocol frames | SCA-IA-05 | Rejected, no wedge | | | |

**All negative testing on a bench with the actuator disconnected or a dummy load fitted.
Never on a live vehicle or live plant.**

---

## 6. Safety–security interaction

### (SCA-SL-01 — all four directions must be populated.)

| Direction | Finding | Resolution |
| --- | --- | --- |
| Security → Safety (harm) | | |
| Security → Safety (help) | | |
| Safety → Security (harm) | | |
| Safety → Security (help) | | |

### 6.1 Security-caused failure conditions

*(SCA-SL-05 — classified on the project's safety severity scale and carried in the same
hazard log.)*

| Failure condition | Security cause | Severity | Hazard log ref | Mitigation |
| --- | --- | --- | --- | --- |

### 6.2 Independent hardware limits

#### (SCA-SL-04.)

[What bounds the damage a fully compromised firmware can do, and how it was verified.  If
the answer is "nothing," say so — it is a finding, not an omission.]

---

## 7. Assumptions transferred to the integrator

### (SCA-NT-01; IR 8259r1 §4.3.1.  This section is a deliverable, not internal notes.)

| # | Assumption | Risk transferred | Who must handle it |
| --- | --- | --- | --- |

**An unstated assumption is an unmitigated risk that both parties believe the other one
handled.**  Every row here must appear in the customer-facing documentation.

---

## 8. Accepted risks

*(Every `Accepted Risk` and `Partial` row needs an entry here.)*

| ID | Control | Risk | Rationale | Accepter | Date | Review date |
| --- | --- | --- | --- | --- | --- | --- |

---

## 9. Physical budget impact

*(Per the user's engineering standards — real numbers, imperial primary with metric in
parentheses.  No TBD.)*

| Security decision | Mass | Board area | Power | Cycles / latency | Other |
| --- | --- | --- | --- | --- | --- |
| Secure element | | | | | BOM cost |
| Potting / conformal coat | | | | | Thermal impact; rework impact |
| Crypto on control path | — | — | | | Deadline margin |
| Log storage | | | | | Endurance-limited life |
| Independent limiter | | | | | Second signed image |
| **Total** | | | | | |

Gross platform mass: [x lbm (y kg)].  Security fraction: [z %].

---

## 10. Support commitment

### (SCA-SU-06, SCA-NT-07; IR 8259r1 §4.3.2.)

| Item | Value |
| --- | --- |
| Expected support life | |
| End-of-support date | |
| Update cadence | |
| Vulnerability disclosure contact | |
| Target response time | |
| EOL reprovisioning/disposal procedure | |

---

## 11. Citations used

Every citation in this document resolves to a REF-ID in the skill's `references/REFERENCES.md`
and in this repository's own `REFERENCES.md`.

| REF-ID | Designation | Sections applied | Verification status |
| --- | --- | --- | --- |

**Any entry marked REQUIRES VERIFICATION must be resolved or removed before this case is
used as a release gate.**

---

## 12. Conclusion and residual claim

[Restate the §1 claim as supported, supported-with-conditions, or not supported.  If
conditions apply, list them.  If not supported, say what would change that.]

**Signed:** [name, role, date]
**AI-assisted analysis:** [model, version] — this document requires review by a qualified
engineer before use as a release gate.
