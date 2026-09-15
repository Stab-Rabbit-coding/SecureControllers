# Overlay C — Raspberry Pi HATs, BeagleBone Capes, and SBC Carriers

Sources: REF-RPI-HAT [46], REF-BB-CAPE [47], plus the base NIST set.  This overlay covers
any add-on board that mounts onto a Linux single-board computer through an expansion header:
Raspberry Pi HAT / HAT+, BeagleBone cape, Jetson carrier, and equivalents.

---

## Why this is a different security architecture, not just a different form factor

A standalone servo controller owns its whole trust boundary: its firmware, its identity, its
network interface, its update path.  A HAT or cape owns almost none of that.

| Property | Standalone controller | HAT / cape |
| --- | --- | --- |
| Network interface | Its own | The **host's** |
| Operating system | Its own firmware | The **host's** Linux — patched by someone else |
| Identity | Provisioned per unit | Usually **none**; the host has the identity |
| Update mechanism | Its own signed update | `apt`, an image rewrite, or nothing |
| Logging | Its own | `journald` on the host |
| Attack surface | Its bus and its ports | Its bus, its ports, **the header, the ID EEPROM, peer boards, and the host OS** |
| Blast radius of compromise | The board | The board **and the host**, in both directions |

**The consequence for the 213A scope test:** a HAT typically has a transducer but no
independent network interface, so it is not an "IoT device" in SP 800-213A §1.1 terms.  It is
an **IoT product component** under REF-NIST-8259R1 §2.2 — and IR 8259r1 is explicit that
customers manage the *product*, so the securability argument must be made at the host+HAT
product level.  That is not a loophole; it is a requirement to write down the division of
responsibility (SCA-HC-05).

---

## The ID EEPROM — the defining attack surface of this overlay

### Raspberry Pi HAT

The HAT specification (REF-RPI-HAT) requires an ID EEPROM on the dedicated ID pins
**ID_SD / ID_SC (header pins 27 and 28)**, read by the firmware at boot.  Its contents are
structured as *atoms*, including a vendor-info atom (UUID, product ID, version, vendor and
product strings), a GPIO map atom, and optionally a **device tree blob atom**.

### BeagleBone cape

Cape EEPROMs sit on **I2C2 at addresses 0x54–0x57**, one per stacking position, which is how
the host distinguishes up to four stacked capes.  Contents include board name, version,
manufacturer, part number, serial number, pin usage, and **declared current draw** on the
supply rails.

> **Verification note.** The pin numbers, bus, and address range above are reproduced from
> the published specifications and are widely documented.  **Field-level layouts, atom
> formats, and byte offsets: REQUIRES VERIFICATION** against the current specification
> revision before you write a programming tool against them.  Both specs have revised.

### Why it matters

The host reads this EEPROM at boot and **acts on its contents** — including, on the Pi,
loading a device tree overlay from it.  That produces three real vulnerabilities that do not
exist on a standalone board:

1. **Unprotected identity.** These are ordinary I²C EEPROMs.  If the write-protect pin is
   left floating or tied inactive — which is extremely common, because it makes factory
   programming easier — then anyone with momentary physical access can rewrite the board's
   identity.  This defeats SCA-ID-05 and, if the host trusts the EEPROM for asset inventory,
   SCA-ID-01 and SCA-ID-06.

2. **Device-tree injection into the host kernel.** An overlay is not passive data — it tells
   the kernel which drivers to bind, which pins to claim, and which buses to enable.  An
   attacker who rewrites the DT blob atom can make the host load different drivers, remap
   peripherals, or claim buses belonging to other boards.  This is a **configuration-injection
   path into the host kernel from a modifiable, unauthenticated storage device.**  Treat it
   with the seriousness of an unsigned firmware update (SCA-SU-01), because functionally
   that is what it is.

3. **A lying power declaration.** The cape EEPROM declares current draw so the host can
   budget its rails.  A falsified declaration can induce the host to power a load it cannot
   support — an availability attack with a physical mechanism (SCA-HC-04).

**Mitigation, in order of preference:** tie WP active in production and program at
manufacture only; sign the EEPROM contents and have the host verify before acting (requires
host-side cooperation — document it as an assumption under SCA-NT-01); or ship the device
tree overlay through the host's package management, where it is covered by the distribution's
signing, and use the EEPROM for identification only.

---

## Shared-bus threat model — your peers are not your friends

The expansion header is a **shared bus**, and this is the part most designs get wrong.  On a
stacked configuration, every board on the header can reach:

| Shared resource | What a hostile or compromised peer board can do |
| --- | --- |
| I²C (incl. the ID bus) | Read and **write** every device on the bus, including **other boards' ID EEPROMs** |
| SPI | Assert chip selects, observe all traffic on the shared MOSI/MISO/SCK |
| UART | Read and inject on a shared serial line |
| GPIO | Drive a pin another board is using as an input; contend on a shared line |
| Power rails | Brown out the host or peers; backfeed; exceed the host's budget |
| Interrupt lines | Deny service by holding a shared IRQ asserted |

This is SP 800-207 §2.2 assumption 2 — "devices on the network may not be owned or
configurable by the enterprise" — rendered in copper at 2.54 mm pitch.  **The header is a
network, and it has no access control whatsoever.**

Design consequences:

- Do not assume exclusive use of a shared bus.  Handle NAKs, arbitration loss, and
  unexpected traffic without wedging (SCA-DS-03, SCA-HC-03).
- Do not put a secret on a shared bus.  A secure element on the shared I²C is readable by
  address from any peer board — put it on a dedicated bus or use a part with an
  authenticated session.
- Never rely on a GPIO from another board as a security signal.
- If your board carries a safety function, that function must not depend on a shared bus
  remaining available (SCA-HC-08).

---

## The host is a trust domain you do not control

Your HAT's security posture is bounded above by a Linux system that:

- is patched (or not) by the end user,
- runs arbitrary other software,
- probably grants your userspace driver access via `/dev/i2c-*`, `/dev/spidev*`, `gpiod`, or
  a kernel module — often with root or broad group membership,
- may be imaged, cloned, or restored from an untrusted source,
- frequently ships with SSH enabled and a well-known default account.

Two directions of compromise, both real:

**Host → board.** A compromised host issues arbitrary commands to your actuator.  If your
board's only authorization check is "the command came over SPI from the host," a web
vulnerability in a Python service on the Pi becomes physical actuation.  This is the single
most important finding in this overlay.  **The fix is that the board authenticates commands
independently of the transport** — the same on-board PEP requirement as SCA-ZT-02, applied to
the header instead of a bus.

**Board → host.** Your board, or a counterfeit copy of it, is a hardware implant with
kernel-level reach via device tree, DMA-capable peripherals on some carriers, and physical
access to the host's buses.  A HAT is an excellent supply-chain implant vector precisely
because it is expected to be there and nobody inspects it.  SCA-SC-02 and SCA-SC-05 matter
more here than on a standalone board.

---

## Practical guidance by control

| Concern | What to do on a HAT/cape |
| --- | --- |
| Identity (SCA-ID) | Add a real secure element on a **dedicated** bus if the board needs an identity independent of the host.  The ID EEPROM is an inventory label, not a credential |
| Secure boot (SCA-DS-01) | If the board has its own MCU, it gets its own secure boot — do not inherit the host's.  If it is passive I/O only, record that the host owns boot integrity |
| Update (SCA-SU) | Decide who owns firmware update for the on-board MCU: host-mediated (document the trust dependency) or independent signed update.  Host-mediated means a compromised host can flash you — mitigate with signature verification **on the MCU** |
| Interfaces (SCA-IA-01) | The header is an interface — enumerate every pin you connect, and every pin you leave connected but unused |
| Debug (SCA-IA-04) | Header pins double as debug on many designs.  A UART console on pins 8/10 is a console, not a debug convenience |
| Logging (SCA-CS) | If logs go to the host, they inherit host integrity.  For anything that must survive host compromise, log on-board |
| Power (SCA-HC-04) | Declare current draw truthfully; add a hardware limit so a fault on your board cannot take the host down |
| Safety (SCA-SL-04) | A hardware limit below both your firmware **and** the host is mandatory if the board drives anything with a safety consequence.  Linux is not a real-time safety controller and must never be the only thing between a command and a motor |

---

## The Linux-is-not-a-safety-controller rule

This deserves its own statement because it is the most common architectural error in this
class of board.

A general-purpose Linux SBC has non-deterministic scheduling, a large attack surface, an
update cadence outside your control, and no functional-safety pedigree.  It is an excellent
mission computer and an unacceptable sole authority over a motion actuator with a safety
consequence.

**Correct pattern:** the Pi or BeagleBone issues *intent* (setpoints, waypoints, enables); an
on-board MCU or an independent hardware limiter enforces the *envelope* (current, speed,
torque, travel, timeout).  The limiter must remain effective when the host is compromised,
hung, or rebooting.

**Incorrect pattern:** a Python process on the host writing PWM duty cycles directly to a
motor driver with no independent limit.  This fails SCA-SL-04 in every overlay, and it fails
SCA-DS-03 the first time the host swaps to disk under memory pressure.

This is the concrete reason the platform overlays in
[`platform-overlays.md`](platform-overlays.md) treat Overlay C as composing with — never
replacing — the physical platform's overlay.

---

## Documenting the division of responsibility

Every HAT/cape needs this table filled in and shipped to the integrator.  It is the
SCA-HC-05 artifact and it satisfies IR 8259r1 §4.3.1 (assumptions) and IR 8425 Documentation.

```text
Capability                | Owned by board | Owned by host | Notes
--------------------------|----------------|---------------|---------------------------
Unique device identity    |                |               |
Secure boot               |                |               |
Firmware/software update  |                |               |
Network interface & auth  |                |               |
Command authorization     |                |               |  <- if "host", say so loudly
Logging & retention       |                |               |
Time source               |                |               |
Key storage               |                |               |
Physical tamper detection |                |               |
Safety envelope enforcement|               |               |  <- must not be "host" alone
```

Any row marked "host" is a **security assumption you are transferring to your customer**.
Under IR 8259r1 §4.3.1 that transfer is only legitimate if you state it.  A HAT datasheet
that is silent on this table has an unmitigated risk that both parties believe the other
one handled.
