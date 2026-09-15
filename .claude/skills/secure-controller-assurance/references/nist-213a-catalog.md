# NIST SP 800-213A Capability Catalog — Controller Translation

Source: REF-NIST-800-213A [6].  Family and subfamily designators below are reproduced from
the document's table of contents (pp. v–vii) and are **verbatim**.  The "controller
translation" column is this skill's engineering interpretation for a microcontroller-class
motion/flight controller — it is authored guidance, not NIST text, and is marked as such.

> **Reading rule.** NIST writes this catalog from the *acquiring organization's* point of
> view ("what must the device I buy be able to do?").  You are the *manufacturer*.  Read
> every capability as: *what must I build in so that my customer can satisfy this?*  That
> inversion is exactly what REF-NIST-8259R1 §1.1 calls **securability**.

---

## Scope check before you use this catalog

SP 800-213A §1.1 scopes "IoT device" to equipment with **at least one transducer**
(sensor or actuator) **and at least one network interface**.  A device meeting only one half
is out of the publication's stated scope.

| Board | Transducer? | Network interface? | In 213A scope? |
| --- | --- | --- | --- |
| Servo / ESC controller with CAN or RS-485 | Yes — motor, encoder | Yes — CAN/RS-485 | Yes |
| Flight-control node on a vehicle bus | Yes — IMU, actuators | Yes — bus | Yes |
| Sensor pod with SPI-only link to a host | Yes | No independent net iface | Component of a product; assess at product level |
| Bare power-supply board | No | No | No — use SCA-OT and SCA-SL only |

A board that fails the scope check is still a **component of an IoT product** under
REF-NIST-8259R1 §2.2, and the product-level obligations still land on you.  Do not use a
scope failure to skip the catalog; use it to decide *at what level* you satisfy it.

---

## 2 — Device Cybersecurity Capability Catalog

Seven families.  These are things **the device does through its own hardware and software**
(REF-NIST-800-213A §1.1).

### DI — Device Identification

| Code | NIST subfamily title | Controller translation (authored) |
| --- | --- | --- |
| IMS | Identifier Management Support | Immutable per-unit ID fused at provisioning; MCU UID alone is **not** sufficient — it is not attestable and often not unique across families |
| AID | Actions Based on Device Identity | Bus node accepts/rejects commands by cryptographic identity, not by CAN arbitration ID or Modbus unit number |
| PID | Physical Identifiers | Silkscreen serial, QR/DataMatrix, or laser-marked ID that a technician can read without powering the board; must match the logical ID |

**Hardware consequence:** IMS and PID together mean a per-unit provisioning step in
manufacturing.  Budget the fixture, the marking process, and the key-injection station in
the build plan — this is a real cost line, not a firmware `#define`.

### DC — Device Configuration

| Code | NIST subfamily title | Controller translation (authored) |
| --- | --- | --- |
| PRV | Logical Access Privilege Configuration | Distinct privilege for *tune* vs *flash* vs *unlock debug* |
| AUT | Authentication and Authorization Configuration | Credentials/roles changeable in the field without a rebuild |
| INT | Interface Configuration | Each physical port individually disableable and its state readable |
| DSP | Display Configuration | Usually N/A on a headless controller — record the N/A with a reason |
| CTL | Device Configuration Control | Config changes are authenticated, logged, and revertible to a known-good |

### DP — Data Protection

| Code | NIST subfamily title | Controller translation (authored) |
| --- | --- | --- |
| CRY | Cryptography Capabilities and Support | Real crypto engine or a secure element; measure the cycle cost against the control loop deadline |
| KEY | Cryptographic Key Management | Generation, storage, rotation, destruction; keys never leave the secure boundary in the clear |
| STO | Secure Storage | Calibration, keys, and logs protected at rest; readout protection actually enabled in the production fuse map |
| STX | Secure Transmission | Integrity and confidentiality on every link that leaves the board |

**The hard one on a controller is STX.** CAN 2.0B carries 8 data bytes.  A 128-bit MAC does
not fit in one frame.  You will be choosing among truncated MACs, multi-frame authentication,
CAN FD (64 bytes), or accepting integrity-only on a segregated conduit.  Make that decision
explicitly, record it, and defend the truncation length — do not let it happen by default.

### LA — Logical Access to Interfaces

| Code | NIST subfamily title | Controller translation (authored) |
| --- | --- | --- |
| AUN | Authentication Support | Device can authenticate the entity talking to it |
| ACF | Authentication Configuration | Authentication parameters are configurable |
| USE | System Use Notification Support | Often N/A headless — record N/A with reason |
| AUZ | Authorization Support | Authenticated ≠ authorized; separate the decision |
| AIM | Authentication & Identity Management | Lifecycle of identities the device accepts |
| ROL | Role Support & Management | Operator / maintainer / manufacturer are different roles |
| LDU | Limitations on Device Usage | Device can constrain what it will do (e.g., refuse arming outside envelope) |
| XCN | External Connections | Control over what the device will connect to |
| IFC | Interface Control | Enumerate and gate **every** interface — including the ones you did not intend to ship |

**IFC is where debug ports die.** SWD/JTAG, a UART console, an unpopulated header with
pads, a bootloader entry pin, an ICSP footprint, test points on the bottom layer — all are
interfaces.  IFC requires each one enumerated and access-controlled, not merely
undocumented.

### SU — Software Update

| Code | NIST subfamily title | Controller translation (authored) |
| --- | --- | --- |
| UPD | Update Capabilities | Field-updatable firmware, cryptographically verified before it runs |
| APP | Update Application Support | Roll-back to known-good, anti-rollback version counter, and a fail-safe if power is lost mid-write |

**Anti-rollback and roll-back-to-known-good are in tension.** Resolve it deliberately: a
monotonic security-version counter that blocks *vulnerable* images, plus an A/B slot that
allows reverting to the last *good* image at the same or higher security version.

### CS — Cybersecurity State Awareness

| Code | NIST subfamily title | Controller translation (authored) |
| --- | --- | --- |
| AEI | Access to Event Information | Events retrievable by an authorized entity |
| EIM | Event Identification & Monitoring | Device recognizes security-relevant events |
| EVR | Event Response | Device does something about them |
| LCT | Logging Capture & Trigger Support | What triggers a log write |
| RDL | Support of Required Data Logging | The mandated fields are actually captured |
| LSR | Audit Log Storage & Retention | Bounded storage; defined overwrite policy |
| SRT | Support for Reliable Time | A log without trustworthy time is weak evidence |
| AUP | Audit Support & Protection | Logs resist tampering and deletion by the attacker |
| SRT/AWR | State Awareness Support | Device can report its own security posture on demand |

**SRT is the quiet trap on an embedded controller.** Most MCUs have no battery-backed RTC
and no trusted time source.  Options: monotonic boot counter plus uptime tick, time from an
authenticated bus master, or GNSS time where the platform already has it (with spoofing
caveats recorded).  Choose one and write down why.  "Timestamps come from `HAL_GetTick()`"
is not an audit trail across a power cycle.

**AWR is the direct feed to zero trust.** SP 800-207 tenet 5 requires the enterprise to
measure the integrity and security posture of every asset (REF-NIST-800-207 §2.1).  A
controller that cannot report its own posture cannot participate in a ZTA — it can only be
trusted implicitly, which is the thing zero trust exists to eliminate.

### DS — Device Security

| Code | NIST subfamily title | Controller translation (authored) |
| --- | --- | --- |
| EXE | Secure Execution | Code runs in an intended, protected state (MPU/TrustZone/privilege separation) |
| COM | Secure Communication | The communication stack itself is sound |
| RSC | Secure Resource Usage | Resource exhaustion cannot take out the control loop |
| DIN | Device Integrity | Device detects unauthorized change to itself |
| ONB | Secure Network Onboarding Support | First join to a network is authenticated, not open |
| OPS | Secure Device Operation | Continues to operate securely in its real environment |

**ONB is the provisioning story.** A controller that ships with a well-known default key,
or that accepts an unauthenticated first-boot pairing on the bench, has no ONB — and that is
the single most common finding in this whole catalog.

---

## 3 — Non-Technical Supporting Capability Catalog

Four families.  These are things **the manufacturer or a designated third party does**
(REF-NIST-800-213A §1.1).  They are not optional extras: SP 800-213A treats them as
*requirements* on the same footing as the device capabilities, and IR 8425 §2.2.2 makes them
developer obligations for a consumer product.

### DO — Documentation

| Code | NIST subfamily title |
| --- | --- |
| SMP | Assumptions Made in Product Development |
| CAP | Technical Cybersecurity Capabilities Implemented |
| DSC | Design and Support Considerations |
| MNT | Maintenance Requirements |
| DAU | Device Authenticity Support |

SMP occupies pp. 41–48 of SP 800-213A — the single largest subfamily in the catalog.  Your
recorded **assumptions** are a first-class deliverable.  If you assumed the CAN bus is
physically protected inside a sealed airframe, that assumption is a security requirement
levied on the airframe, and it must be written down and handed to whoever owns the airframe.

### IQ — Information and Query Reception

| Code | NIST subfamily title |
| --- | --- |
| BUG | Reception of Vulnerability Information |
| QRY | Query Response |

Concretely: a published contact that receives vulnerability reports (REF-ISO-29147) and a
process that handles them (REF-ISO-30111).  A `SECURITY.md` with a monitored address is the
minimum viable artifact.

### ID — Information Dissemination

| Code | NIST subfamily title |
| --- | --- |
| CRI | Cybersecurity Related Information Alert |
| VNT | Cybersecurity Event Notification |

IR 8425 §2.2.2 fixes a **minimum** broadcast set: updated terms of support; end of term of
support or functionality; needed maintenance operations; new vulnerabilities with mitigation
actions; and breach discovery with mitigation actions.  That list is normative in IR 8425 —
it is introduced by "At a minimum, this information shall include".

### EA — Education and Awareness

| Code | NIST subfamily title |
| --- | --- |
| CSC | Cybersecurity Capabilities |
| EOL | End-of-Life (Reprovisioning and Disposal) |
| RSP | Cybersecurity Responsibilities |
| EXP | Cybersecurity Expectations and Assumptions |
| BAK | Data Back-up |
| VMG | Vulnerability Management Options |

**EOL is a hardware requirement disguised as documentation.** "Reprovisioning and disposal"
means the board must be able to erase its keys and calibration on command and prove it did.
That is a firmware feature and a fuse-map decision, and it has to exist before you can write
the EOL page.

---

## Appendices worth knowing

| Appendix | Contents | Use it when |
| --- | --- | --- |
| A | Definition of the Federal Profile for IoT Device Cybersecurity Requirements | The controller may be procured by a federal agency |
| B | Mapping of SP 800-53 controls to device cybersecurity requirements | You need to answer "which 800-53 control does this satisfy?" |
| C | Mapping of CSF outcomes to device cybersecurity requirements | You are reporting posture in CSF terms |

Appendix B is the bridge from this catalog to the SP 800-82r3 OT Overlay (REF-NIST-800-82R3
App. F), because the overlay is itself organized by SP 800-53 family.  Route
**213A capability → 800-53 control (App. B) → OT Overlay tailoring (App. F.7.x)** when you
need OT-specific tailoring of a device capability.

---

## Recording a not-applicable determination

IR 8425 §2.2.2 requires documenting "which baseline product criteria are **not** met by IoT
product components **and why** (e.g., the capability is not needed based on risk
assessment)".  A bare "N/A" fails that.  Use this form:

```text
Capability:      LA/USE — System Use Notification Support
Determination:   Not applicable
Rationale:       Controller is headless; no human-facing interface exists on which a use
                 notification could be displayed. No display, no console at operator
                 privilege.
Compensating:    Use notification is presented by the GCS at the product level, which is the
                 component that owns the human interface (product boundary per IR 8259r1
                 §2.2).
Residual risk:   None identified at device level.
Decided by:      <name/handle>   Date: <YYYY-MM-DD>   Review: <YYYY-MM-DD>
```

An N/A without a named decider and a compensating-control line is an open finding, not a
closed one.
