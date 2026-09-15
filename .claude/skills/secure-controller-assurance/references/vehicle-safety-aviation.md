# Vehicle, Aviation, and Safety Overlays

Sources: REF-ISO-SAE-21434 [23], REF-UNECE-R155 [24], REF-UNECE-R156 [25],
REF-RTCA-DO-326A [26], REF-RTCA-DO-356A [27], REF-14CFR-107 [28], REF-14CFR-89 [29],
REF-ASTM-F3411 [30], REF-IEC-61508 [22], REF-NIST-800-82R3 [3].

> **Jurisdiction.** Per the user's global instructions, all legal and regulatory analysis
> here is **United States**.  Non-US instruments (UN R155/R156, EUROCAE ED-series) appear
> only as reference models and are labelled as such.

---

## Applicability triage — run this before citing anything

The most common error in this domain is claiming compliance with a standard that does not
apply.  Work down the table and record the result in the assurance case.

| Question | If yes | If no |
| --- | --- | --- |
| Is this a **road vehicle** component for a production vehicle? | ISO/SAE 21434 applies commercially; UN R155/R156 apply for type approval **outside** the US | 21434 is a *reference methodology only* — say so |
| Is the aircraft **type-certificated** (14 CFR Part 21)? | DO-326A / DO-356A / DO-355 are the airworthiness security process | DO-326A **does not bind you**; cite as best practice only |
| Is it a small UAS operated under **14 CFR Part 107**? | Part 107 and Part 89 (Remote ID) apply | Check Part 91 / 135 / waiver conditions |
| Does it carry a **safety function** with a hazard rate target? | IEC 61508 SIL applies (or ISO 26262 ASIL for road) | Safety-security interaction analysis still required |
| Is it sold as a **component to an integrator**? | Your assumptions become their requirements — IR 8259r1 §4.3.1 | You own the whole product argument |

**For this user's typical work — a small UAS servo, ESC, or flight node — the honest
answer is usually:** Part 107 and Part 89 apply; DO-326A does not bind but is the right
methodology; 21434 is a useful analogue; no SIL is formally assigned but the safety
consequence is severe.  Write exactly that.  Do not write "DO-326A compliant."

---

## 14 CFR Part 89 — Remote ID is a security input, not a security defect

Part 89 (REF-14CFR-89) requires a standard remote identification unmanned aircraft to
broadcast identity and position.  ASTM F3411 (REF-ASTM-F3411) is the associated broadcast
specification.

This has three consequences a controller designer must handle, and none of them is "turn it
off":

1. **The aircraft deliberately broadcasts its position, in the clear, to anyone.** Any threat
   model that assumes the vehicle's location is confidential is wrong by regulation.  Write
   the assumption down and design around it.
2. **The Remote ID message set is an unauthenticated broadcast** in the basic broadcast
   profile.  Treat received Remote ID from *other* aircraft as untrusted input — it is
   trivially spoofable and must never gate a safety decision without corroboration.
3. **Remote ID data path integrity matters to you.** If your controller sources the position
   that gets broadcast, corrupting your position solution corrupts a regulatory broadcast.
   That elevates GNSS spoofing from a navigation problem to a compliance problem.

**Do not** implement, advise, or assist with defeating, spoofing, or suppressing Remote ID.
That is outside what this skill will help with.  Detecting spoofed Remote ID from other
aircraft, and hardening your own position solution, are both squarely in scope.

---

## GNSS as an untrusted sensor

Not a standard, but the most consequential threat for any vehicle controller, and it belongs
in every vehicle threat model:

| Threat | Effect | Board-level mitigation |
| --- | --- | --- |
| GNSS jamming | Loss of position | Detect (C/N₀ collapse, loss of lock), fail over to inertial/visual, defined degraded mode |
| GNSS spoofing | **Confidently wrong** position — worse than loss | Cross-check against IMU dead reckoning, barometric altitude, multi-constellation consistency, clock-jump detection |
| Time spoofing via GNSS | Corrupts the log timestamp source (213A CS/SRT) | Do not source audit time solely from GNSS; monotonic counter as anchor |

The spoofing case is the dangerous one because every downstream consumer — navigation,
geofence, Remote ID broadcast, return-to-home — trusts the position.  A geofence enforced
against a spoofed position is not a geofence.

---

## Safety–security interaction: the analysis that must actually happen

SP 800-82r3 §5.3.1 requires cyber-related safety considerations; §4.2.2 flags safety systems
as a special area.  ISA-TR84.00.09 covers the interaction with the functional safety
lifecycle.  IEC 61508 supplies the SIL framework.

Run this four-way analysis for every controller with a safety consequence.  All four
directions are real and the last two are usually skipped:

| Direction | Question | Example on a UAS controller |
| --- | --- | --- |
| **Security → Safety (harm)** | Can a security control cause a hazard? | Auth timeout disarms motors in flight; secure-boot verification delays startup past a launch window; log write blocks the control loop |
| **Security → Safety (help)** | Does a security control protect a safety function? | Signed firmware prevents a malicious image from disabling the motor-stop path |
| **Safety → Security (harm)** | Does a safety mechanism open an attack path? | An always-available unauthenticated failsafe command; a watchdog reset that clears security state; a maintenance override that bypasses auth |
| **Safety → Security (help)** | Does a safety mechanism bound an attack? | Envelope limiter caps the damage from a spoofed command; independent hardware current limit survives firmware compromise |

**The Safety → Security (harm) row is where TRITON lives.** The 2017 TRITON/TRISIS malware
targeted a safety instrumented system specifically. The lesson for a controller designer:
the failsafe path is a high-value target *precisely because* it is designed to always work
and is often designed without authentication. Do not exempt it from the threat model.

Recommended resolution pattern for the classic conflict:

- **Authenticate the enable, not the stop.** A motor-stop / disarm / failsafe command should
  remain unconditional. An arm / enable / parameter-write command must be authenticated.
  An attacker who can only stop the vehicle causes a controlled failure; an attacker who can
  start or steer it causes an uncontrolled one.
- **Independent hardware limits below the firmware.** A hardware current limit, a mechanical
  stop, or a separate limiter MCU keeps a firmware compromise inside a survivable envelope.
  This is the single highest-value safety-security control on a motion controller.

---

## ISO/SAE 21434 as a borrowed methodology

Even where 21434 does not bind, two of its artifacts are worth producing because nothing in
the NIST set replaces them:

**TARA (Threat Analysis and Risk Assessment).** Item definition → asset identification →
threat scenario → attack path → attack feasibility → impact rating → risk determination →
treatment decision.  The impact rating covers safety, financial, operational, and privacy —
which is exactly the multi-axis view a vehicle needs and which a pure CIA analysis misses.

**Cybersecurity case.** A structured argument, backed by evidence, that the item is
adequately secure.  This is the template for the deliverable in
`assets/assurance-case-template.md`.

Cite these as *methodology borrowed from ISO/SAE 21434 [23]*, not as compliance.

---

## The DO-326A idea worth keeping

DO-326A's central move is to run the **security risk assessment inside the safety assessment
process** rather than alongside it, so that a security-caused failure condition is classified
on the same severity scale as any other failure condition.

For a small UAS that is not type-certificated, adopt the *idea* without claiming the
standard: classify each security-caused failure condition using the same severity scale the
project uses for safety (e.g., No Effect / Minor / Major / Hazardous / Catastrophic), and
carry it in the same hazard log.  A security finding that produces a Catastrophic failure
condition then automatically inherits the project's rigor for that classification.

This is what makes a security finding legible to a safety engineer, and it is why
`assets/assurance-case-template.md` carries a failure-condition column.

---

## Weight, power, and area — security has physical cost

Per the user's global engineering instructions, security decisions must be accounted in the
mass, power, and space budget like any other component.  Record actual numbers, not "TBD":

| Decision | Typical cost to budget |
| --- | --- |
| Discrete secure element / TPM | Package mass, board area, 1 BOM line, quiescent + active current, SPI/I²C pins |
| Tamper mesh or potting | Mass (potting compound is heavy), thermal impedance change, **rework becomes impossible** |
| Conformal coat | Mass, cure time, thermal effect, test-point access |
| Crypto acceleration in firmware | Flash and RAM footprint, control-loop cycle budget, peak current |
| Log storage | External flash part, write current, endurance-limited lifetime |
| CAN FD instead of CAN 2.0B | Transceiver part change, possible harness/EMC requalification |
| Redundant limiter MCU | Mass, area, power, second firmware image to maintain and sign |

Quote these against the actual airframe budget.  A 0.05 lbm (23 g) potting decision on a
2.5 lbm (1.13 kg) airframe is 2 % of gross mass and must be justified, not assumed.

**Thermal note:** potting and conformal coating change the thermal path of a motor
controller that is already dissipating real power.  A security decision that raises MOSFET
junction temperature is a reliability decision.  Check it against the thermal analysis before
committing.
