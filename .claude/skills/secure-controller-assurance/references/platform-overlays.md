# Platform Overlays — One Control Set, Five Deployment Contexts

The SCA control matrix is platform-independent by design.  What changes between an aircraft,
a boat, a ground vehicle, a fixed robot cell, and an SBC carrier board is:

1. **Which regulations actually bind** (jurisdiction and applicability),
2. **Which functional-safety framework supplies the severity scale**,
3. **The threat model deltas** — what an attacker reaches and what the consequence is,
4. **Which SCA controls shift gate or severity.**

Pick the overlay, apply it on top of the base matrix, and record the choice.  A servo, an
ESC, or a sensor node is frequently the **same board** across several of these — which means
the *product* must satisfy the union of the overlays it will be sold into, or the datasheet
must state the exclusions.

> **The reusable-component rule.** If you sell one ESC into UAS, USV, and fixed-robot
> applications, you have three sets of expected customers and use cases under
> REF-NIST-8259R1 §3.2 (Activity 1).  Either satisfy the strictest overlay, or state the
> intended and excluded applications explicitly.  A board qualified only for a bench robot,
> sold without qualification into a flying vehicle, is a foreseeable-misuse problem —
> IR 8425 §2.2.2 Documentation 1(d)(iv) requires recording "known risks related to the IoT
> product and known potential misuses."

---

## Overlay selection table

| Overlay | Platform | Primary US regulator | Severity scale source |
| --- | --- | --- | --- |
| **A — Air** | UAS, small unmanned aircraft | FAA (14 CFR 107, 89) | DO-326A methodology; project hazard scale |
| **G — Ground** | UGV, AGV/AMR, off-road, road vehicle | NHTSA (road); OSHA (industrial site) | ISO 26262 ASIL (road); ISO 13849 PL / IEC 62061 (machinery) |
| **M — Marine** | USV, small boats, surface craft | USCG (MTSA-regulated); otherwise none | IMO/USCG cyber risk management; project hazard scale |
| **F — Fixed industrial** | Robot cell, gantry, stationary actuator | OSHA | ISO 13849 PL / IEC 62061 SIL; ISO 10218 |
| **C — Carrier/SBC** | Pi HAT, BeagleBone cape, Jetson carrier | None inherently — inherits host's context | Inherits from the platform it is installed in |

Overlay **C** composes with the others: a Pi HAT motor driver in a boat is `C + M`.

---

## Overlay A — Air (UAS)

Detail in [`vehicle-safety-aviation.md`](vehicle-safety-aviation.md).  Summary:

- **Binds:** 14 CFR Part 107 (operations), 14 CFR Part 89 (Remote ID).
- **Does not bind** a non-type-certificated small UAS: DO-326A/DO-356A, ISO/SAE 21434,
  UN R155/R156.  Use as methodology; never claim compliance.
- **Threat deltas:** mandated position broadcast (Part 89); GNSS spoofing/jamming is the
  dominant sensor threat; loss of control means uncontrolled descent onto people or property;
  no ability to "stop and stay put."
- **Control shifts:** SCA-SL-07 (untrusted navigation) elevated to 🔒 Ideate; SCA-ZT-05
  fail-**safe** on actuation is mandatory, never fail-closed in flight.

---

## Overlay G — Ground (UGV, AGV/AMR, off-road, road)

**Applicability triage — the ground category splits three ways and they are not
interchangeable:**

| Sub-case | Binds | Notes |
| --- | --- | --- |
| **On-road production vehicle** | FMVSS via NHTSA; ISO/SAE 21434 commercially expected; ISO 26262 ASIL | UN R155/R156 apply for type approval **outside** the US |
| **Off-road / agricultural / construction** | OSHA on-site; ISO 25119 or ISO 13849 for functional safety | Not FMVSS |
| **AGV/AMR in a facility** | OSHA; ANSI/ITSDF B56.5; ISO 3691-4 | Industrial truck safety standards, not vehicle standards |

- **Threat deltas vs air:** the safe state is usually **stop**, which makes fail-closed
  behavior far more defensible than it is in the air.  A ground vehicle that halts is
  usually safe; an aircraft that halts is not.  This is the single biggest overlay
  difference and it inverts the SCA-ZT-05 guidance.
- Collision with people is the dominant hazard; a spoofed navigation solution drives the
  vehicle into a person rather than into terrain.
- Physical access to the vehicle is far easier than to an aircraft in flight — SCA-IA-04
  (debug ports) and SCA-DS-07/08 (tamper, test points) rise in severity.
- Longer unattended dwell time in accessible locations: assume hands-on attacker time.

- **Control shifts:** SCA-ZT-05 fail state for actuation becomes **fail-stop** (safe) rather
  than continue-degraded; SCA-IA-04 and SCA-DS-07 severity elevated; SCA-SL-04 (hardware
  limit) should include a hardware-enforced speed/torque cap reachable independent of
  firmware.

---

## Overlay M — Marine (USV, small boats)

**Regulatory position — read carefully, this area is genuinely murky:**

- A small, privately operated USV or recreational boat is **not** subject to a specific
  federal cybersecurity rule.  Do not invent one.
- **If the vessel or facility is MTSA-regulated**, the US Coast Guard's maritime
  cybersecurity requirements apply (33 CFR subchapter H).  The USCG issued a Maritime
  Security Directive and a cybersecurity rulemaking affecting US-flagged vessels and
  regulated facilities.  **Status: REQUIRES VERIFICATION** — confirm the current CFR
  citation and compliance dates at <https://www.ecfr.gov/current/title-33> and
  <https://www.dco.uscg.mil/> before citing it in a design record.  Do not cite a specific
  section number from memory.
- **USCG NVIC 01-20**, *Guidelines for Addressing Cyber Risks at MTSA Regulated Facilities* —
  guidance, not regulation.  **REQUIRES VERIFICATION** of current revision.
- **IMO Resolution MSC.428(98)** and **MSC-FAL.1/Circ.3**, maritime cyber risk management —
  international, applies to SOLAS vessels' safety management systems.  Not applicable to a
  small USV; useful as a reference model.  **REQUIRES VERIFICATION** of circular revision.

- **Threat deltas:**
  - **Recovery is the problem.** A ground robot that stops is retrievable; a boat that stops
    drifts, and may drift into a shipping lane, aground, or out of radio range.  The safe
    state is *not* simply "stop" — it may be "hold station" or "return to launch," both of
    which require the control system to keep working.  This makes Overlay M closer to Air
    than to Ground for fail-state design.
  - **Water ingress is a tamper vector and a reliability threat simultaneously.**  Sealing
    decisions (SCA-DS-07) are being made anyway for IP rating — make them serve tamper
    evidence at the same time.  This is the cheapest security win in the marine overlay.
  - Long-duration unattended operation with intermittent link; extended periods where the
    PEP must enforce on cached policy (SCA-ZT-05 validity window is longer and matters more).
  - AIS is an unauthenticated broadcast protocol — treat received AIS exactly like received
    Remote ID in the air overlay: untrusted input, never gates a safety decision alone.
  - Salt-fog and condensation degrade connectors and seals over time; a tamper seal that
    fails from corrosion produces false positives that train operators to ignore it.

- **Control shifts:** SCA-ZT-05 fail-safe (hold/return), not fail-stop; SCA-DS-07 sealing
  serves double duty and should be specified once for both IP and tamper; SCA-CS-03 log
  storage sized for long unattended missions; SCA-SL-07 extended to cover AIS and any
  received navigation broadcast.

---

## Overlay F — Fixed industrial (robot cell, gantry, stationary actuator)

This is where the ISA/IEC 62443 material in [`ot-ics-62443.md`](ot-ics-62443.md) applies most
directly and least by analogy — a fixed industrial actuator on a plant network **is** the
IACS component 62443-4-2 was written for.

- **Binds (US):** OSHA general duty and machine-guarding rules.  **ANSI/RIA R15.06** adopts
  ISO 10218 for industrial robots.  **Status: VERIFIED — public** for the adoption
  relationship; clause content REQUIRES VERIFICATION.
- **Functional safety:** ISO 13849-1 Performance Levels (PL a–e) or IEC 62061 SIL for
  machinery; ISO 10218-1/-2 for industrial robots; ISO/TS 15066 for collaborative operation.
  These supply the severity scale in place of DO-326A or ASIL.
- **62443 applies fully:** the board is an EDR in a real zone-and-conduit architecture with
  a real asset owner, a real Purdue hierarchy, and probably a real IDMZ.  Skill
  `18-ot-ics-security` becomes directly relevant for the surrounding network.

- **Threat deltas:**
  - The board is **reachable from an enterprise network** through however many layers the
    plant actually has — which in practice is fewer than the drawing shows.
  - Persistent, network-based, remote attacker instead of a physical-access attacker.
    This inverts the ground-vehicle emphasis: SCA-IA-03/05/06 and SCA-OT-02 rise; the
    physical-tamper controls fall in relative priority (but do not disappear — insider and
    maintenance-window access is real).
  - **Collaborative operation means a human is inside the envelope by design.**  A
    manipulated torque or speed command reaches a person directly.  ISO/TS 15066 force and
    pressure limits become security-relevant values: if firmware can raise them, firmware
    compromise is a physical-harm path.
  - Safety-instrumented systems may be present and are a deliberate target (TRITON).

- **Control shifts:** SCA-SL-04 hardware limit is **mandatory and must be independent of the
  safety-rated controller as well as the main firmware** where a human shares the envelope;
  SCA-ZT-05 fail state is **fail-stop, protective stop**; SCA-OT-01/02 elevated; SCA-DS-03
  (resource exhaustion) elevated because a plant network carries broadcast storms that a
  vehicle bus does not.

---

## Overlay C — Carrier and SBC add-on boards

Full detail in [`sbc-carrier-boards.md`](sbc-carrier-boards.md).  Summary of why this is
architecturally different:

- The board is **not a standalone IoT device** — it is a component of a product whose
  network interface, OS, update mechanism, and identity belong to the **host**.
- The 213A scope test resolves differently: transducer yes, independent network interface
  usually no.  Assess at the **product** level with the host, and be explicit about the
  division of responsibility.
- New attack surface that does not exist on a standalone controller: the expansion header as
  a shared bus, the ID EEPROM, device-tree overlay loading, shared power rails, and stacked
  peer boards.
- **The host OS is a shared trust domain you do not control.** Your board's security is
  bounded by a Linux system that someone else patches.

---

## Cross-platform reuse — the practical workflow

When the same board serves multiple overlays:

1. **Build the union control set.** Take the base matrix, apply every overlay the board will
   ship into, and take the strictest gate and severity for each control.
2. **Resolve fail-state conflicts explicitly.**  This is the one place the overlays genuinely
   contradict each other:

   | Overlay | Actuation fail state on policy expiry |
   | --- | --- |
   | A — Air | Continue degraded, land — **never halt** |
   | G — Ground | Fail-stop |
   | M — Marine | Hold station or return — **not halt** |
   | F — Fixed | Protective stop |

   A single firmware image cannot hardcode one of these and serve all four.  The correct
   design is a **configured fail-state policy**, set at provisioning, with the configuration
   itself integrity-protected (SCA-CFG-04) and the safe default being the most conservative
   value for the configured platform.  Shipping a motor controller whose fail-state is
   compile-time and undocumented is a defect against SCA-ZT-05 in every overlay.

3. **State the exclusions in the datasheet.** "Qualified for Overlay G and F; not qualified
   for airborne or marine use" is a legitimate, honest scope statement and satisfies
   IR 8425's misuse-documentation criterion.
4. **Record the union in the control register** with an overlay column, so a reviewer can
   see which requirement came from which platform.
