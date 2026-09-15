# Zero Trust for a Controller — NIST SP 800-207 Applied

Source: REF-NIST-800-207 [4].  Tenet and assumption titles below are **verbatim** from
SP 800-207 §2.1 and §2.2.  Everything under "On a controller" is authored engineering
interpretation.

---

## Why this is not a category error

SP 800-207 is written for enterprise networks, and it is fair to ask what it is doing in a
servo controller's design review.  Two reasons it belongs:

1. **§2.1 tenet 1 is explicit that small-footprint devices and actuator-command systems are
   in scope.** The tenet text names "small footprint devices that send data to
   aggregators/storage" and "systems sending instructions to actuators."  A flight
   controller commanding an ESC is the literal example.
2. **A vehicle bus is the purest possible implicit trust zone.** SP 800-207 §2.2 assumption
   1 says the private network is not an implicit trust zone.  A classic CAN bus is the
   opposite: any node can assert any arbitration ID, and every other node believes it.  One
   compromised node owns the aircraft.  That is precisely the failure mode zero trust
   addresses.

What does **not** transfer: SP 800-207 assumes a policy engine with network reach, telemetry
feeds, and human-timescale re-authentication.  A 400 Hz control loop cannot make a round trip
to a policy engine before applying a torque command.  The adaptation is to move the PEP onto
the controller and make policy decisions *cacheable and locally enforceable*, which is the
agent/gateway model of §3.2.1 pushed to its embedded limit.

---

## The seven tenets, translated

### Tenet 1 — "All data sources and computing services are considered resources."

**On a controller:** every actuator command endpoint, every telemetry stream, every
parameter table, and every diagnostic service is a distinct resource with its own policy.
The failure pattern is a single "connected/not connected" state that grants everything.

**Design question at ideation:** enumerate the resources this board exposes.  If the list is
"the CAN interface", you have not done the exercise.

### Tenet 2 — "All communication is secured regardless of network location."

**On a controller:** the fact that the bus is inside a sealed airframe does not make it
trusted.  Authenticate bus traffic.  Where the frame budget genuinely will not carry it
(see the CAN 2.0B problem in `nist-213a-catalog.md`, DP/STX), record the residual risk and
the compensating control — do not silently drop the requirement.

**Trap:** "it's an air-gapped internal bus" is the exact reasoning SP 800-207 §2.2
assumption 1 rejects.

### Tenet 3 — "Access to individual enterprise resources is granted on a per-session basis."

**On a controller:** an armed session is not a permanent grant.  Bind authorization to a
session with a defined lifetime and an explicit teardown.  Re-authorize on state
transitions — arm, disarm, mode change, parameter write, firmware update.

**Real-time adaptation:** you cannot re-authorize per control cycle.  Authorize per
*session*, then protect every frame in that session with a MAC and a monotonic counter.  The
session is the unit of authorization; the frame MAC is the unit of integrity.

### Tenet 4 — "Access to resources is determined by dynamic policy — including the observable state of client identity, application/service, and the requesting asset — and may include other behavioral and environmental attributes."

**On a controller:** the policy that decides whether to accept a command should be able to
consider more than "is this node on the bus."  Weight-on-wheels, armed state, flight mode,
geofence status, and link health are all environmental attributes that can gate a command.

**Concrete win:** refuse a firmware-update request while airborne.  That is dynamic policy
using an environmental attribute, and it is cheap to implement.

### Tenet 5 — "The enterprise monitors and measures the integrity and security posture of all owned and associated assets."

**On a controller:** this is the direct hardware requirement.  The board must be able to
*measure and report* its own posture — firmware measurement, secure-boot result, tamper
state, config hash.  Maps to 213A **DS/DIN** and **CS/AWR**.

**Consequence:** if you want the platform to be zero trust, the controller needs an
attestation path.  Decide at ideation whether that is a TPM, a secure element, an MCU with
a hardware root of trust, or an accepted gap.  Retrofitting it after layout is expensive.

### Tenet 6 — "All resource authentication and authorization are dynamic and strictly enforced before access is allowed."

**On a controller:** enforcement happens **before** the command reaches the actuator path,
not after.  The PEP is on the board.

**Anti-pattern:** authenticating the telemetry uplink while the actuator command path is
unauthenticated because "it's local."

### Tenet 7 — "The enterprise collects as much information as possible about the current state of assets, network infrastructure and communications and uses it to improve its security posture."

**On a controller:** the logging capability (213A **CS** family) is the feed.  Design the log
schema so it is useful to a fleet-level analytic, not just to a bench technician.

---

## The six network assumptions, translated

| # | SP 800-207 §2.2 assumption (verbatim title) | Controller consequence |
| --- | --- | --- |
| 1 | The entire enterprise private network is not considered an implicit trust zone | The vehicle bus is hostile.  Design for a compromised peer node |
| 2 | Devices on the network may not be owned or configurable by the enterprise | Third-party payloads, contractor ground equipment, and field-replaced units will attach |
| 3 | No resource is inherently trusted | The autopilot does not get a free pass because it is the autopilot |
| 4 | Not all enterprise resources are on enterprise-owned infrastructure | Telemetry backhaul crosses carrier LTE, third-party ground stations, cloud |
| 5 | Remote enterprise subjects and assets cannot fully trust their local network connection | A deployed vehicle assumes the RF link is monitored and modifiable |
| 6 | Assets and workflows moving between enterprise and nonenterprise infrastructure should have a consistent security policy and posture | A unit that flies a contract mission and comes back must retain posture; re-onboarding must re-verify it |

Assumption 2 is the one people miss on a vehicle: **the payload bay is a third-party
device port.**  Treat it as such.

---

## Logical components on an embedded platform

SP 800-207 §3 splits the policy decision point into a **policy engine (PE)** and **policy
administrator (PA)**, with a **policy enforcement point (PEP)** in the data path.  §3.2
states plainly that these are *logical* components and one asset may perform the duties of
several.

Practical allocation for a vehicle:

| SP 800-207 component | Where it lives on a small UAS |
| --- | --- |
| Policy Engine (PE) | Ground control station or fleet trust service — decides *policy* |
| Policy Administrator (PA) | Fleet/ground service that issues credentials and session tokens |
| Policy Enforcement Point (PEP) | **On the controller itself** — gates the actuator path |
| CDM system | Fleet health/attestation service consuming posture reports |
| PKI | Provisioning CA that issues per-unit device certificates |
| ID management | Unit registry: serial ↔ public key ↔ configuration ↔ role |
| SIEM | Fleet log aggregation |

**The critical design consequence:** the PEP is on the board and must keep enforcing when
the link to the PE is down.  That means cached policy with a defined validity window and a
defined **fail state**.  Pick the fail state consciously:

- **Fail-closed** on configuration, firmware update, key operations, and parameter writes.
- **Fail-safe (not fail-open)** on the actuator path — a vehicle in flight that stops
  accepting control because a token expired is now an uncontrolled vehicle.  The safe
  behavior is usually to continue the last authorized mission under a degraded-mode policy
  and land, not to halt.

That distinction is a **safety-security interaction** and must go in the safety assessment,
not only the security one.  See `ot-ics-62443.md` on safety precedence.

---

## The three ZTA approach variants (§3.1) for a vehicle platform

| Variant | SP 800-207 §  | Fit for a vehicle bus |
| --- | --- | --- |
| Enhanced identity governance | 3.1.1 | Strong fit — per-unit cryptographic identity is achievable and is the foundation for the rest |
| Micro-segmentation | 3.1.2 | Partial — a gateway between flight-critical and payload domains is a realistic PEP |
| Network infrastructure / SDP | 3.1.3 | Poor fit — assumes programmable network infrastructure a CAN segment does not have |

SP 800-207 §3.1 notes a full solution includes elements of all three.  On a small vehicle,
lead with identity governance, add a segmentation gateway at the payload boundary, and
document SDP as not applicable with the reason.

---

## Minimum credible zero-trust posture for a controller

Use this as the ideation-phase bar.  Anything less should be a recorded, accepted gap.

1. **Unique, attestable, per-unit cryptographic identity** provisioned in manufacturing —
   not a shared key, not the MCU UID alone.  (Tenet 5, 213A DI/IMS.)
2. **Authenticated command path** to the actuator, with replay protection.  (Tenets 2, 6.)
3. **On-board PEP** that enforces before actuation, with cached policy and a declared fail
   state.  (Tenet 6, §3.2.1.)
4. **Session-scoped authorization** re-evaluated at arm, mode change, and config write.
   (Tenet 3.)
5. **Posture reporting** — secure-boot result, firmware measurement, config hash.
   (Tenet 5, 213A DS/DIN + CS/AWR.)
6. **Secure onboarding** with no default credential.  (213A DS/ONB.)
7. **Segmentation at the payload boundary**, treating payloads as untrusted.
   (§2.2 assumption 2, §3.1.2.)

---

## Where zero trust and real-time control genuinely conflict

Do not paper over these.  Record each as an explicit trade with a named decision-maker.

| Conflict | Why it is real | Resolution pattern |
| --- | --- | --- |
| Per-request authorization vs control-loop deadline | Crypto and round trips do not fit in a 2.5 ms cycle | Session-scoped auth + per-frame MAC; benchmark the MAC against the actual deadline |
| Continuous re-authentication vs link loss | Tenet 6 wants dynamic re-auth; the RF link drops | Cached policy with validity window; degraded-mode policy on expiry |
| Fail-closed vs flight safety | ZT default is deny; denying control in flight is a hazard | Fail-closed on config/update, fail-**safe** on actuation; document in the safety case |
| Logging volume vs flash endurance | Tenet 7 wants data; the part has finite write cycles | Bounded ring buffer, severity-gated writes, offload on landing; size it against the endurance spec |
| MAC length vs CAN 2.0B payload | 8-byte frames will not carry a full MAC | Truncated MAC with a defended length, multi-frame auth, or CAN FD; record the choice |

Each row is a legitimate engineering answer.  An **undocumented** choice in any row is a
finding.
