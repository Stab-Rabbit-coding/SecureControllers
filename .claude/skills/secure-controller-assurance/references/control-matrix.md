# SCA Control Matrix — Unified Controller Assurance Control Set

The single control set this skill assesses against.  Every control traces to at least one
REF-ID in [`REFERENCES.md`](REFERENCES.md).  Control **statements** are authored by this
skill; the **sources** column names the standards the statement is derived from.  Nothing
here is presented as verbatim standard text unless quoted and attributed.

## How to read a row

| Column | Meaning |
| --- | --- |
| **ID** | Stable identifier.  Cite as `SCA-XX-nn` in commits, TODO items, and design records |
| **Gate** | The phase by which this must be **decided**.  `I` Ideate, `C` Create, `R` Refine, `Q` QA, `S` Sustain |
| **Alloc** | Where it is implemented: `HW` hardware, `FW` firmware, `DOC` documentation, `PROC` process |
| **Sources** | REF-IDs and, where applicable, the 213A capability code / 62443 FR / ZT tenet |

**Notation.** In `assets/control-register-template.csv` the gate `🔒 I` is written `I-LOCK`,
because the register is plain ASCII for spreadsheet and script use.  The two mean the same
thing.

**Family codes never collide with NIST codes.** An SCA family code is always written
`SCA-XX-nn`; a NIST SP 800-213A family/subfamily is always written `213A XX/YYY`.  This
matters in two places where the letters coincide: `SCA-ID` is *Device Identity and
Attestation*, while `213A ID` is *Information Dissemination*; `SCA-DS` is *Device Security*,
while `213A DS` is the same — but `SCA-CS` and `213A CS` are also aligned.  Read the prefix,
not the letters.

**A `Gate` of `I` means unrecoverable-after-layout.** Missing an `I`-gate control is a
respin, not a patch.  These are flagged 🔒 and are the first thing to check on any new design.

## Status vocabulary

Aligned with the installed `19-grc-compliance` skill so registers are interchangeable:

`Implemented` · `Partial` · `Not Implemented` · `Not Applicable` (requires the recorded
rationale form in `nist-213a-catalog.md`) · `Accepted Risk` (requires a named accepter and a
review date).

## Platform overlays

This matrix is platform-independent.  Before assessing, select the deployment overlay from
[`platform-overlays.md`](platform-overlays.md) — **A** Air, **G** Ground, **M** Marine,
**F** Fixed industrial, **C** Carrier/SBC — and apply its gate and severity shifts.  Overlay
**C** composes with the others; a Pi HAT motor driver in a boat is `C + M`.

If one board ships into several overlays, assess against the **union** and take the strictest
gate for each control.  The one place the overlays genuinely contradict each other is the
actuation fail state (SCA-ZT-05): air and marine must not halt, ground and fixed must.  That
makes fail state a **provisioned configuration**, not a compile-time constant — see the
cross-platform reuse section of `platform-overlays.md`.

---

## SCA-GOV — Governance and Requirements

Derived from REF-NIST-8259R1 Activities 0–2, REF-NIST-800-213 §3, REF-ISA-62443-4-1 SM/SR.

| ID | Control | Gate | Alloc | Verification evidence | Sources |
| --- | --- | --- | --- | --- | --- |
| SCA-GOV-01 | A named individual owns security decisions for this board and has veto authority over a release | I | PROC | Named in the repo's AGENTS.md/CLAUDE.md or design record | 8259r1 §3.1 (Act. 0); 62443-4-1 SM |
| SCA-GOV-02 | Expected customer and expected use cases are written down before requirements are set | 🔒 I | DOC | Design record section; not "anyone who buys it" | 8259r1 §3.2 (Act. 1) |
| SCA-GOV-03 | A target Security Level (SL-T) is assigned, with SL-C and SL-A tracked separately | 🔒 I | DOC | `SL-T=n, SL-C=n, SL-A=n` recorded with rationale | 62443-3-3 |
| SCA-GOV-04 | A threat model exists, names adversary capability, and is revisited when the architecture changes | I | DOC | Threat model doc; attack paths mapped to ATT&CK for ICS | 8259r1 §3.3 (Act. 2); 800-213 §3.2; 62443-4-1 SD |
| SCA-GOV-05 | Every control in this matrix has a status and, for anything other than Implemented, a recorded rationale and owner | R | DOC | Control register (`assets/control-register-template.csv`) | 8425 §2.2.2 Documentation 1(c) |
| SCA-GOV-06 | Security requirements are traceable from threat → control → implementation → test | R | DOC | Traceability column populated in the register | 62443-4-1 SR/SVV |

---

## SCA-ID — Device Identity and Attestation

213A family **DI**.  62443 **FR 1**.  ZT tenets 1, 5.

| ID | Control | Gate | Alloc | Verification evidence | Sources |
| --- | --- | --- | --- | --- | --- |
| SCA-ID-01 | Each unit has a unique cryptographic identity, provisioned in manufacturing, not derivable from public information | 🔒 I | HW+FW | Provisioning procedure; key-injection fixture defined in the build plan | 213A DI/IMS; 8425 Asset Identification 1; FR 1 |
| SCA-ID-02 | The private key is generated in, or injected into, a boundary from which it cannot be read in the clear | 🔒 I | HW | Part selection: secure element, TPM, or MCU with key storage.  Datasheet-verified | 213A DP/KEY; FIPS 140-3 |
| SCA-ID-03 | The board can attest its identity and firmware measurement to a challenger | I | HW+FW | Attestation protocol defined; challenge-response demonstrated on bench | ZT tenet 5; 213A DS/DIN, CS/AWR |
| SCA-ID-04 | Bus access decisions are made on cryptographic identity, not on address, arbitration ID, or unit number | C | FW | Code path review; negative test with a spoofed ID | 213A DI/AID; FR 1 |
| SCA-ID-05 | A durable physical identifier on the board matches the logical identity | C | HW | Silkscreen/laser mark; QR or DataMatrix; matches provisioning record | 213A DI/PID |
| SCA-ID-06 | Product and each component are enumerable, and an inventory of connected components is maintained | C | FW | Component inventory readable over the bus | 8425 Asset Identification 2; 213A DI/IMS |

> **The MCU-UID trap.** A vendor unique ID is not a cryptographic identity: it is readable by
> anyone with debug access, it is not secret, it cannot sign, and in several families it is
> not globally unique.  Using it as an identity fails SCA-ID-01 and SCA-ID-02.

---

## SCA-CFG — Configuration and Secure Defaults

213A family **DC**.  62443 **FR 2**.

| ID | Control | Gate | Alloc | Verification evidence | Sources |
| --- | --- | --- | --- | --- | --- |
| SCA-CFG-01 | No default credential, shared key, or universal unlock exists in shipped firmware | C | FW | Grep of the release image; provisioning requires per-unit secrets | 8425 Interface Access Control; 213A DS/ONB |
| SCA-CFG-02 | Authorized entities can change configuration; unauthorized entities cannot | C | FW | Positive and negative auth test per config surface | 8425 Product Configuration 1; 213A DC/CTL |
| SCA-CFG-03 | The board can be restored to a secure default (uninitialized) state | C | FW | Factory-reset path tested; verifies keys/calibration cleared | 8425 Product Configuration 2; 213A EA/EOL |
| SCA-CFG-04 | Configuration and calibration data are integrity-protected; corruption is detected and refused | C | FW | Checksum/MAC over parameter blocks; fault-injection test | 213A DP/STO; FR 3; ATT&CK T0836 |
| SCA-CFG-05 | Privilege is separated: tune / flash / unlock-debug are distinct rights | C | FW | Role matrix; test each role's boundary | 213A DC/PRV, LA/ROL; FR 2 |
| SCA-CFG-06 | Configuration changes are logged with actor identity and timestamp | R | FW | Log inspection after a config write | 213A CS/RDL; FR 6 |

---

## SCA-DP — Data Protection and Cryptography

213A family **DP**.  62443 **FR 4**.  ZT tenet 2.

| ID | Control | Gate | Alloc | Verification evidence | Sources |
| --- | --- | --- | --- | --- | --- |
| SCA-DP-01 | Cryptographic primitives are current, standard, and named — no custom or obfuscation-as-crypto | C | FW | Algorithm list in the design record; FIPS-approved where feasible | FIPS 140-3; FIPS 186-5 |
| SCA-DP-02 | The crypto implementation's cycle cost is measured against the control-loop deadline | 🔒 I | FW | Benchmark table: operation, cycles, worst-case latency vs deadline | FR 7; 800-82r3 §5.3.2 |
| SCA-DP-03 | Keys have a defined lifecycle: generation, storage, use, rotation, destruction | C | FW+PROC | Key management plan; rotation demonstrated | 213A DP/KEY |
| SCA-DP-04 | Secrets at rest are protected; flash readout protection is enabled in the production fuse map | 🔒 I | HW+FW | Production programming script sets protection; verified on a built unit | 213A DP/STO; 800-82r3 §5.2.4 |
| SCA-DP-05 | Data leaving the board is integrity-protected; confidentiality applied where the data warrants it | C | FW | Protocol spec; captured traffic shows MAC present | 8425 Data Protection 3; 213A DP/STX; FR 4 |
| SCA-DP-06 | Replay protection exists on every authenticated channel (counter, nonce, or timestamp) | C | FW | Replay test: captured valid frame re-injected and rejected | FR 3; ZT tenet 3 |
| SCA-DP-07 | Cryptographic agility: algorithms and key sizes can be changed without a hardware change | I | FW | Algorithm identifier in the protocol; migration path documented | FIPS 203/204 (long-lived signing keys) |
| SCA-DP-08 | Stored customer/mission data can be deleted or rendered inaccessible on command | C | FW | Erase command tested; verified unreadable afterwards | 8425 Data Protection 2; 213A EA/EOL |

> **MAC truncation on CAN 2.0B.** An 8-byte frame cannot carry a full-length MAC alongside
> payload.  Choose deliberately among: truncated MAC with a defended length, multi-frame
> authentication, CAN FD, or integrity-only on a segregated conduit.  Record the choice, the
> truncation length, and the forgery probability you accepted.  An undocumented default is a
> finding against SCA-DP-05.

---

## SCA-IA — Interface Access Control

213A family **LA**.  62443 **FR 1, FR 2, FR 5**.  This is the highest-yield family on a
hardware review.

| ID | Control | Gate | Alloc | Verification evidence | Sources |
| --- | --- | --- | --- | --- | --- |
| SCA-IA-01 | Every interface is enumerated — including unpopulated headers, test points, and bootloader pins | 🔒 I | HW+DOC | Interface inventory cross-checked against the schematic and fab drawing | 8425 Interface Access Control 1; 213A LA/IFC |
| SCA-IA-02 | Interfaces not necessary for operation are removed or secured | 🔒 I | HW+FW | Each interface marked *necessary* or *removed/secured* with rationale | 8425 IAC 1(a) — normative |
| SCA-IA-03 | Every necessary interface has an access-control measure | C | FW | Test each interface unauthenticated; expect refusal | 8425 IAC 1(b); FR 1 |
| SCA-IA-04 | Debug access (SWD/JTAG/UART console) is disabled, locked, or authenticated in production units | 🔒 I | HW+FW | Attempt debug attach on a production-configured unit; must fail or require auth | 8425 IAC 1(a); 800-82r3 §5.2.4; ATT&CK T0839 |
| SCA-IA-05 | Data received across an interface is validated against a specified format and content before use | C | FW | Fuzz/malformed-frame test; parser rejects out-of-spec input | 8425 IAC 2(a); FR 3 |
| SCA-IA-06 | The board cannot make unauthorized transmissions to, or access, other components | C | FW | Traffic capture shows only expected flows | 8425 IAC 2(b); FR 5 |
| SCA-IA-07 | Access control is maintained during onboarding and on reconnection after an outage | C | FW | Power-cycle and link-drop tests; no unauthenticated window | 8425 IAC 2(c); 213A DS/ONB |

> **SCA-IA-04 is the most frequently failed control in this matrix.** Decide the debug-port
> lifecycle at ideation: development units debug-open and *permanently marked as such*,
> production units locked in the programming step.  If the team needs field debug, the
> answer is an authenticated unlock (challenge-response against the device key), not a live
> port.  A live SWD port on a fielded controller means firmware extraction, key extraction,
> and arbitrary code execution with physical access.

---

## SCA-SU — Software and Firmware Update

213A family **SU**.  62443-4-1 **SUM**.

| ID | Control | Gate | Alloc | Verification evidence | Sources |
| --- | --- | --- | --- | --- | --- |
| SCA-SU-01 | Firmware images are cryptographically signed and the signature is **verified before execution** | 🔒 I | HW+FW | Load an unsigned and a tampered image; both must be refused | 8425 Software Update 1 — normative; 800-193; ATT&CK T0857 |
| SCA-SU-02 | The verification root of trust is immutable or itself protected against unauthorized change | 🔒 I | HW | Boot ROM, OTP, or secure element holds the root key | 800-193 (protection) |
| SCA-SU-03 | An interrupted update leaves the board in a bootable, known state | C | FW | Power-cut test during write, repeated at multiple points | 800-193 (recovery); 213A SU/APP |
| SCA-SU-04 | Anti-rollback prevents installing a known-vulnerable image, while still permitting recovery to a known-good image | C | FW | Monotonic security-version counter; downgrade test | 213A SU/APP |
| SCA-SU-05 | Updates cannot be applied in an unsafe operational state | C | FW | Attempt update while armed/in flight; must be refused | ZT tenet 4; 800-82r3 §5.3.1 |
| SCA-SU-06 | A defined update cadence and an end-of-support date are published | R | DOC+PROC | Support policy document | 8425 Information Dissemination 1(a)(b); 8259r1 §4.3.2 |
| SCA-SU-07 | The update channel itself is authenticated and integrity-protected in transit | C | FW | Protocol review; MITM test on the update path | 213A DP/STX; ZT tenet 2 |

---

## SCA-CS — Cybersecurity State Awareness and Logging

213A family **CS**.  62443 **FR 6**.  ZT tenets 5, 7.

| ID | Control | Gate | Alloc | Verification evidence | Sources |
| --- | --- | --- | --- | --- | --- |
| SCA-CS-01 | Security-relevant events are identified and captured (auth failure, config change, update, boot verification result, tamper, reset cause) | C | FW | Event catalogue; each event produced on demand in test | 8425 Cybersecurity State Awareness 1; 213A CS/EIM |
| SCA-CS-02 | A trustworthy time or sequence source anchors every log entry | 🔒 I | HW+FW | Time strategy documented; survives power cycle | 213A CS/SRT |
| SCA-CS-03 | Log storage is bounded with a defined overwrite policy, sized against the flash endurance spec | I | HW+FW | Storage budget: entry size × rate × life vs endurance rating | 213A CS/LSR |
| SCA-CS-04 | Logs resist tampering and deletion by an attacker who has compromised the application | C | FW | Log region write-protected or MAC-chained; tamper test | 213A CS/AUP; FR 6 |
| SCA-CS-05 | An authorized entity can retrieve logs; an unauthorized one cannot | C | FW | Retrieval requires auth; negative test | 213A CS/AEI |
| SCA-CS-06 | The board reports its own security posture on request (boot result, firmware measurement, config hash) | C | FW | Posture query returns signed report | ZT tenet 5; 213A CS/AWR |
| SCA-CS-07 | The board takes a defined action on a detected security event, not only logging it | R | FW | Event-response matrix; behavior tested | 213A CS/EVR |

> **SCA-CS-02 on a controller without an RTC.** Acceptable strategies: monotonic boot counter
> plus tick offset; time from an authenticated bus master with the trust dependency recorded;
> GNSS time with spoofing caveats and a monotonic anchor.  Unacceptable: raw `HAL_GetTick()`
> alone, which resets to zero every power cycle and makes ordering across boots impossible.

---

## SCA-DS — Device Security (boot, execution, integrity, resources)

213A family **DS**.  62443 **FR 3, FR 7**.

| ID | Control | Gate | Alloc | Verification evidence | Sources |
| --- | --- | --- | --- | --- | --- |
| SCA-DS-01 | Secure boot verifies each stage before transferring control to it | 🔒 I | HW+FW | Chain-of-trust diagram; tampered-stage test at each link | 800-193; 213A DS/EXE |
| SCA-DS-02 | The signing key lifetime and algorithm are chosen against the product's service life | 🔒 I | PROC | Key policy: algorithm, size, rotation, compromise plan | FIPS 186-5; FIPS 204 (long-life keys) |
| SCA-DS-03 | Resource exhaustion cannot prevent the control loop meeting its deadline | 🔒 I | FW | Bus flood, malformed-frame storm, log-full, crypto-queue saturation tests | FR 7; ATT&CK T0814; 800-82r3 §5.3.2 |
| SCA-DS-04 | Memory protection separates privileged from application code (MPU, TrustZone, or equivalent) | I | HW+FW | MPU/TZ configuration reviewed; fault test | 213A DS/EXE; 800-82r3 §5.2.5 |
| SCA-DS-05 | The board detects unauthorized change to itself and reports it | C | FW | Integrity check at boot and periodically; tamper test | 213A DS/DIN; FR 3 |
| SCA-DS-06 | First network join is authenticated; no open pairing window | C | FW | Onboarding test with an unprovisioned unit | 213A DS/ONB |
| SCA-DS-07 | Physical tamper measures appropriate to SL-T are specified and implemented | 🔒 I | HW | Conformal coat / potting / seals / mesh, per SL-T; mass and thermal impact quoted | 800-82r3 §5.2.2 |
| SCA-DS-08 | Test points and probe-accessible nets are placed and treated per SL-T | 🔒 I | HW | Fab drawing review; sensitive nets on inner layers or under coat | 800-82r3 §5.2.2, §5.2.4 |

---

## SCA-ZT — Zero Trust Enforcement

REF-NIST-800-207.  See [`zero-trust-207.md`](zero-trust-207.md) for the full tenet mapping.

| ID | Control | Gate | Alloc | Verification evidence | Sources |
| --- | --- | --- | --- | --- | --- |
| SCA-ZT-01 | Resources exposed by the board are enumerated individually, each with its own policy | I | DOC+FW | Resource list; not a single connected/disconnected state | ZT tenet 1 |
| SCA-ZT-02 | The command path to the actuator is authenticated and enforced **before** actuation | 🔒 I | FW | PEP location in the code path; negative test at the actuator | ZT tenets 2, 6 |
| SCA-ZT-03 | Authorization is session-scoped and re-evaluated at arm, mode change, config write, and update | C | FW | Session model documented; re-auth observed at each transition | ZT tenet 3 |
| SCA-ZT-04 | Policy decisions may consider operational and environmental state, not identity alone | C | FW | At minimum: refuse firmware update while airborne | ZT tenet 4 |
| SCA-ZT-05 | Cached policy has a defined validity window and a defined, safe behavior on expiry | 🔒 I | FW+DOC | Fail state per resource class: fail-closed on config/update, fail-**safe** on actuation | ZT tenet 6; 800-82r3 §5.3.1 |
| SCA-ZT-06 | The board never grants access on the basis of network location or bus membership | C | FW | Code review for "trusted because local" logic | ZT tenet 2; §2.2 assumption 1 |
| SCA-ZT-07 | Third-party payload interfaces are treated as untrusted and mediated by a gateway | 🔒 I | HW+FW | Payload boundary in the block diagram; gateway PEP present | §2.2 assumption 2; §3.1.2 |

---

## SCA-OT — OT Zone, Conduit, and Field-Device Controls

REF-NIST-800-82R3, REF-ISA-62443-3-3.  See [`ot-ics-62443.md`](ot-ics-62443.md).

| ID | Control | Gate | Alloc | Verification evidence | Sources |
| --- | --- | --- | --- | --- | --- |
| SCA-OT-01 | The board's zone and the conduits crossing its boundary are identified with an SL-T each | 🔒 I | DOC | Zone/conduit diagram | 62443-3-3 |
| SCA-OT-02 | The board enforces restricted data flow at its own boundary — it does not forward between zones without mediation | C | FW | Traffic capture; no unmediated cross-zone forwarding | FR 5; 800-82r3 §5.4 |
| SCA-OT-03 | Industrial/vehicle protocol implementations are hardened against malformed and out-of-sequence input | C | FW | Protocol fuzzing on the bench, never on a live vehicle | 800-82r3 App. F.5; FR 3 |
| SCA-OT-04 | Defense-in-depth is present at the hardware layer, not only in firmware | 🔒 I | HW | 800-82r3 §5.2.4 layer addressed explicitly in the design record | 800-82r3 §5.2.4 |
| SCA-OT-05 | Field-I/O (Purdue Level 0) exposure is analyzed — what an attacker achieves with only bus access | I | DOC | Level-0 threat analysis section | 800-82r3 §5.3.6, §5.3.7 |
| SCA-OT-06 | Availability degradation modes are defined and tested, not assumed | C | FW | Degraded-mode matrix with tested behavior | FR 7; 800-82r3 §5.3.2 |

---

## SCA-SL — Safety–Security Interaction

REF-NIST-800-82R3 §4.2.2, §5.3.1; REF-ISA-TR84-00-09; REF-IEC-61508.  See
[`vehicle-safety-aviation.md`](vehicle-safety-aviation.md).

| ID | Control | Gate | Alloc | Verification evidence | Sources |
| --- | --- | --- | --- | --- | --- |
| SCA-SL-01 | The four-way safety–security interaction analysis is performed and recorded | 🔒 I | DOC | All four directions populated, including Safety→Security | 800-82r3 §5.3.1; TR84.00.09 |
| SCA-SL-02 | No security control can prevent a safety function from executing | 🔒 I | HW+FW | Trace each safety function; confirm no security gate on its path | 800-82r3 §4.2.2 |
| SCA-SL-03 | The failsafe/stop path is unauthenticated; the arm/enable path is authenticated | 🔒 I | FW | Command classification table; tested both ways | Authored pattern; TRITON lesson |
| SCA-SL-04 | Independent hardware limits bound the damage a compromised firmware can do | 🔒 I | HW | Hardware current limit, mechanical stop, or separate limiter — on the schematic | 800-82r3 §5.2.4 |
| SCA-SL-05 | Security-caused failure conditions are classified on the project's safety severity scale and carried in the same hazard log | R | DOC | Hazard log entries with security cause | DO-326A methodology (not compliance) |
| SCA-SL-06 | Regulatory applicability is triaged and recorded — no unearned compliance claims | I | DOC | Applicability triage table completed | 14 CFR 107, 89; 21434; DO-326A |
| SCA-SL-07 | Position/navigation sources are treated as untrusted; spoofing and jamming have defined detection and response | I | FW | GNSS cross-check logic; spoofing test or documented gap | Authored; 14 CFR 89 dependency |

---

## SCA-SC — Supply Chain

REF-NTIA-SBOM-MIN, REF-CISA-SBOM, REF-NIST-SSDF, REF-NIST-800-82R3 §4.2.1.

| ID | Control | Gate | Alloc | Verification evidence | Sources |
| --- | --- | --- | --- | --- | --- |
| SCA-SC-01 | An SBOM exists for the firmware, carrying the NTIA minimum elements | R | DOC | SBOM file: supplier, component, version, other IDs, dependency, author, timestamp | NTIA minimum elements |
| SCA-SC-02 | A hardware BOM records security-relevant parts with authentic-source provenance | C | DOC | BOM flags the secure element / MCU / transceiver source | 800-82r3 §4.2.1; 213A DO/DAU |
| SCA-SC-03 | Third-party and open-source components are tracked for vulnerabilities over the support life | S | PROC | Monitoring process; CVE review cadence | SSDF RV; 8259r1 §4.1 (Act. 6) |
| SCA-SC-04 | Toolchain and build are reproducible enough to establish what is in a shipped image | R | PROC | Pinned toolchain version; build recorded with the release | SSDF PS/PW |
| SCA-SC-05 | Counterfeit-part risk for security-critical devices is addressed in sourcing | C | PROC | Authorized-distributor policy for the secure element and MCU | 800-82r3 §4.2.1; 213A DO/DAU |

---

## SCA-HC — Host and Carrier Boards (Overlay C only)

Applies when the board is a Raspberry Pi HAT, BeagleBone cape, or other SBC add-on.  Full
rationale in [`sbc-carrier-boards.md`](sbc-carrier-boards.md).  Mark the whole family
Not Applicable, with the reason, on a standalone controller.

| ID | Control | Gate | Alloc | Verification evidence | Sources |
| --- | --- | --- | --- | --- | --- |
| SCA-HC-01 | The ID EEPROM is write-protected in production; WP is driven, not floating | 🔒 I | HW | Schematic shows WP tied active; write attempt on a production unit fails | REF-RPI-HAT; REF-BB-CAPE; 213A DI/PID |
| SCA-HC-02 | Device tree overlay contents are integrity-protected, or delivered through the host's signed package channel instead of the EEPROM | 🔒 I | HW+PROC | Overlay delivery path documented; EEPROM DT atom absent or verified | REF-RPI-HAT; 800-193; analogous to SU-01 |
| SCA-HC-03 | The board tolerates a hostile or faulty peer on every shared bus without wedging | C | FW | NAK, arbitration-loss, bus-hold, and unexpected-traffic tests | ZT §2.2 assumption 2; FR 7 |
| SCA-HC-04 | Declared current draw is truthful and a hardware limit prevents the board faulting the host's rails | 🔒 I | HW | Measured draw vs declaration; fuse/eFuse/current limit on the schematic | REF-BB-CAPE; FR 7 |
| SCA-HC-05 | The board/host division of responsibility is documented and shipped to the integrator | R | DOC | The completed responsibility table in `sbc-carrier-boards.md` | 8259r1 §4.3.1; 8425 Documentation |
| SCA-HC-06 | Commands from the host are authorized by the board, not trusted merely because they arrived over the header | 🔒 I | FW | Negative test: unauthorized host process cannot actuate | ZT tenet 2; ZT-02 applied to the header |
| SCA-HC-07 | Secrets are not placed on a bus shared with peer boards | 🔒 I | HW | Secure element on a dedicated bus, or an authenticated-session part | 213A DP/KEY |
| SCA-HC-08 | Safety-envelope enforcement survives host compromise, hang, and reboot | 🔒 I | HW | Independent limiter; host held in reset during test, envelope still enforced | SL-04; 800-82r3 §5.2.4 |
| SCA-HC-09 | The board requires the least host privilege necessary; required privileges are documented | C | DOC+FW | Driver/permission requirements stated; no blanket root requirement | 213A LA/AUZ; 62443 FR 2 |

> **SCA-HC-08 restates the Linux-is-not-a-safety-controller rule.** A general-purpose SBC has
> non-deterministic scheduling, an update cadence outside your control, and no
> functional-safety pedigree.  It may issue intent; it may not be the only thing between a
> command and a motor.

---

## SCA-NT — Non-Technical Supporting Capabilities

213A families **DO, IQ, ID, EA**.  IR 8425 §2.2.2.  62443-4-1 **SG, DM**.

| ID | Control | Gate | Alloc | Verification evidence | Sources |
| --- | --- | --- | --- | --- | --- |
| SCA-NT-01 | Development assumptions are recorded and communicated to the integrator | R | DOC | Assumptions section; explicitly lists risk transferred to the integrator | 8259r1 §4.3.1; 8425 Documentation 1(a); 213A DO/SMP |
| SCA-NT-02 | Implemented cybersecurity capabilities are documented, including which baseline criteria are **not** met and why | R | DOC | Control register with rationale for every non-Implemented row | 8425 Documentation 1(c); 213A DO/CAP |
| SCA-NT-03 | A monitored channel receives vulnerability reports, with a documented handling process | R | PROC | `SECURITY.md` with contact and expected response time | 8425 Information and Query Reception; ISO 29147/30111; 213A IQ/BUG |
| SCA-NT-04 | The minimum dissemination set can be broadcast to customers: support terms, EOL, maintenance, new vulnerabilities, breach | R | PROC | Notification channel identified and reachable | 8425 Information Dissemination 1 — normative; 213A ID/CRI, ID/VNT |
| SCA-NT-05 | A hardening/deployment guide ships with the board | Q | DOC | Integration guide covering secure configuration | 62443-4-1 SG; 213A EA/CSC |
| SCA-NT-06 | End-of-life reprovisioning and disposal instructions exist, backed by a working erase capability | R | DOC+FW | EOL procedure; erase verified | 8425 Product Education; 213A EA/EOL |
| SCA-NT-07 | Expected support lifespan and anticipated cybersecurity costs are stated | I | DOC | Support policy with an explicit end date | 8259r1 §4.3.2; 8425 Documentation 1(a)(viii) |

---

## Phase-gate quick reference

Run this list at the start of any new controller design.  Every 🔒 control below is
**unrecoverable or expensive after layout**:

| Gate | Controls |
| --- | --- |
| **Ideate 🔒** | GOV-02, GOV-03, ID-01, ID-02, DP-02, DP-04, IA-01, IA-02, IA-04, SU-01, SU-02, CS-02, DS-01, DS-02, DS-03, DS-07, DS-08, ZT-02, ZT-05, ZT-07, OT-01, OT-04, SL-01, SL-02, SL-03, SL-04 — **plus, Overlay C:** HC-01, HC-02, HC-04, HC-06, HC-07, HC-08 |
| **Ideate** (not 🔒) | GOV-01, GOV-04, ID-03, DP-07, CS-03, DS-04, ZT-01, OT-05, SL-06, SL-07, NT-07 |
| **Create** | ID-04…06, CFG-01…05, DP-01/03/05/06/08, IA-03/05/06/07, SU-03…05/07, CS-01/04…06, DS-05/06, ZT-03/04/06, OT-02/03/06, SC-02/05, HC-03/09 |
| **Refine** | GOV-05/06, CFG-06, CS-07, SU-06, SL-05, SC-01/04, NT-01…04/06, HC-05 |
| **QA** | Verification evidence for every row; NT-05 |
| **Sustain** | SC-03, and the Activity 6/8 obligations in `nist-8259-8425.md` |

## Top ten findings, in the order they usually appear

From the failure patterns these standards exist to address.  Check these first on any board:

1. **SCA-IA-04** — live debug port in production
2. **SCA-SU-01** — unsigned or unverified firmware update
3. **SCA-ID-01** — shared key or MCU UID used as identity
4. **SCA-ZT-02** — unauthenticated actuator command path
5. **SCA-CFG-01** — default credential in the shipped image
6. **SCA-DP-04** — flash readout protection available but not enabled in production
7. **SCA-SL-04** — no hardware limit below the firmware
8. **SCA-CS-02** — logs with no trustworthy time anchor
9. **SCA-ZT-07** — payload port with flight-critical bus access
10. **SCA-NT-01** — security assumptions never written down or handed to the integrator
