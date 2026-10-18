---
title: NoNFO-Pilot (BBE) - Plan
type: feat
date: 2026-10-12
topic: nonfo-pilot-bbe
artifact_contract: ce-unified-plan/v1
artifact_readiness: requirements-only
product_contract_source: ce-brainstorm
execution: code
---

<!-- markdownlint-configure-file { "MD025": { "front_matter_title": "" } } -->

# NoNFO-Pilot (BBE) - Plan

**Owner / engineer of record:** Steve Griffing (GitHub `Stab-Rabbit-coding`) made every product decision recorded here.
**Drafted by:** Claude Opus 5.5 (`claude-opus-5-5`), 2026-10-11/12, from a `ce-brainstorm` session; repository grounding extraction by a Claude Haiku 5.5 sub-agent.
**License:** CC BY-SA 4.0 (documentation), per the workspace licence-by-output rule.

---

## Goal Capsule

- **Objective:** define one cape, NoNFO-Pilot, that gives a SanCloud BeagleBone Enhanced (BBE) node the full capability of one Serenity avionics stack (today a Pilot cape and a TACCO cape on two PocketBeagle 2 Industrial (PB2-I) nodes), with every duplicated function fitted once.
- **Product authority:** S. Griffing. NoNFO-Pilot is a SecureControllers fleet product; Serenity-UAV is its first and most demanding customer. The PB2-I-hosted, BBE-outline sibling variant is separate work (see "How This Work Fits Together").
- **Open blockers:** the GNSS source (R13) must be resolved before planning; see Outstanding Questions.

---

## Product Contract

### Summary

NoNFO-Pilot is a single 6-layer cape for the BBE Industrial WiFi that merges Pilot and TACCO into one board and one node. It ships first as a monolithic design (the AM3358 drives every peripheral) with area and pins reserved so a trust-module bus front end can be populated later without a respin. The host BBE is reworked so every field and service connector on the stack is a locking JST-GH or USB-C.

### Problem Frame

A Serenity stack is two PB2-I nodes, each with its own 55 x 35 mm (2.165 x 1.378 in) cape. Pilot and TACCO each carry their own isolated CAN-FD, isolated RS-485, MIL-STD-1553C interface, Ethernet PHYs and magnetics, TPM and power-entry filter, so a stack pays for those functions twice. Both capes are also at the edge of routability: Pilot sits at 196 unconnected after automated routing, and TACCO left about 90 logic connections unrouted at 55 x 35 mm (`avionics/kicad/Pilot/Pilot.md`, `avionics/kicad/TACCO/TACCO.md` §13b in Serenity-UAV). TACCO's Wi-Fi is a fab blocker because the PB2 brings no SDIO to its headers.

The two halves of a stack are not co-located either: Inara's TACCO node lies on the cargo chin floor while its Pilot node sits on the aft strip (`docs/CARGO_SECTION_LAYOUT.md` in Serenity-UAV), so each stack is also two pouches, two harness drops and two power feeds.

### Key Decisions

- **One node per stack; the fleet goes from 8 compute nodes to 4.** Loss of a node now drops that stack's whole role set; PACE failover runs across 4 nodes. (session-settled: user-directed — chosen over an in-stack backup MCU or two BBEs per stack: the size and weight goal outranks per-stack compute redundancy.) Governs R27, R28.
- **Fleet product, Serenity first.** Serenity's node-site, harness and EMC numbers qualify the board, but airframe changes are Serenity integration work, not board constraints. (session-settled: user-directed — chosen over a Serenity-only drop-in or a Serenity-agnostic generic board.)
- **Host is the BBE Industrial WiFi; the BBE Industrial is the backup.** It is the only variant with industrial temperature range, the onboard 2.4 GHz radio and Winbond TrustME secure-boot flash; the Lite, WiFi 512 and WiFi 1G are 0 to 60 degC parts. (session-settled: user-approved — chosen over the other four SanCloud variants after a side-by-side comparison.) Governs R1, R2.
- **Consumer connectors are reworked, not kept.** RJ45, USB-A and Mini-USB are replaced by adapter boards; this is the only route to the volume goal and removes non-locking connectors (the PocketPilot v1 loose-connector lesson). (session-settled: user-directed — chosen over a stock, as-shipped BBE.) Governs R4, R5, R6, R7.
- **The BBE's own PHY is ring port 1.** Its RJ45 is swapped for a JST-GH magnetics adapter and the cape adds one DP83825I as ring port 2; the AM3358's CPSW switch carries RSTP. This drops the switch IC, one PHY and one magnetics set from the cape, at the cost of a host-dependent forwarding path. (session-settled: user-directed — chosen over a cape-side 3-port switch with the BBE PHY abandoned.) Governs R11.
- **USB-C replaces the USB-A host pair, and the Mini-USB OTG becomes a USB-C device port.** The owner directed USB-C in place of USB-A so the board keeps a programming port; because the AM3358's programming, flashing and console port is the Mini-USB OTG (USB0) rather than the USB-A host ports (USB1), the agent extended the swap to that port too. Governs R5, R6.
- **Wi-Fi is split: 2.4 GHz and BT on the BBE, 5 GHz on a cape USB module.** (session-settled: user-directed — chosen over BBE 2.4 GHz only, and over a cape-owned dual-band radio: keeps the fleet's 5 GHz C2 path.) Governs R16.
- **Heavy vision stays on the Observer board.** NoNFO-Pilot relays encoded streams only. (session-settled: user-approved — chosen over a node-hosted UVC camera: the AM3358 is one Cortex-A8 core.) Governs R3.
- **Architecture A first, B as a population upgrade.** A: the AM3358 drives everything, with CAN-FD from an SPI CAN-FD controller. B: a fleet trust-module MCU (the pattern on CAN-PERIPH-GW-1, Observer and Flight Engineer) owns CAN-FD, watchdogs the host and keeps the node's health and bus presence alive through a host hang. (session-settled: user-directed — chosen over committing to B or to A alone: one firmware image now, no respin later.) Governs R20, R21.
- **Security split: TPM on the cape, TrustME on the host.** TrustME authenticates and rollback-protects the host's boot image; the cape's SLB9672 TPM holds fleet keys and attestation, as on every node today. (session-settled: user-approved.) Governs R18, R19.

### Requirements

#### Host and compute

- R1. NoNFO-Pilot shall be designed for and qualified on the SanCloud BBE Industrial WiFi, and shall also mate with the BBE Industrial without layout change.
- R2. The board documentation shall list the BBE Lite, WiFi 512 and WiFi 1G as not qualified for flight, on operating temperature.
- R3. Flight-critical loops shall run on the PRUs or real-time-priority threads, with vision and camera processing excluded from the node (see Success Criteria for the CPU ceiling).

#### Host rework (controlled configuration change)

- R4. The BBE RJ45 shall be replaced by an adapter board carrying 10/100 magnetics and a locking JST-GH 4-pin ring connector, fitted in the RJ45 footprint.
- R5. The BBE USB-A host pair shall be replaced by one USB-C host (DFP) receptacle on an adapter board.
- R6. The BBE Mini-USB OTG port shall be replaced by a USB-C device (UFP) receptacle on an adapter board and shall remain the node's programming, flashing and console port, reachable with the stack assembled.
- R7. The rework shall be a documented, inspectable procedure, and a reworked BBE shall carry its own configuration identity distinct from a stock BBE.

#### Buses and network

- R8. The node shall present isolated CAN-FD to the fleet trunk, and the AM3358 DCAN controllers shall not be attached to that trunk (a classic-CAN controller error-frames every FD frame).
- R9. The node shall present isolated half-duplex RS-485 using the fleet ISOW1412.
- R10. The node shall present MIL-STD-1553C bus A through one Holt HI-6138 and one PM-DB2791S transformer, with bus B left parked as on Pilot Rev T.
- R11. The node shall present two Ethernet ring ports, BBE PHY on port 1 and a cape DP83825I on CPSW port 2, both fixed at 100 Mb/s, with RSTP across them.
- R12. Every field connector shall be a shielded, locking JST-GH (or U.FL for RF), with shields returned to PGND, and no field harness shall terminate on the BBE except through the R4 to R6 adapters.

#### Sensors and radios

- R13. The node shall carry the Pilot GNSS function (u-blox MAX-M10S with a U.FL feed to the airframe antenna and its bias-T).
- R14. The node shall carry the Pilot IMU and barometer on the cape, and the BBE's onboard MPU-6050 and LPS331AP shall not be used as primary flight sensors.
- R15. The node shall carry the TACCO mLRS radio (STM32WLE5JC), the 802.15.4 ZigBee radio and the 49 MHz sub-module header.
- R16. 2.4 GHz Wi-Fi and BT shall come from the BBE onboard radio, and 5 GHz Wi-Fi from a cape-mounted USB module on a BBE internal USB host port.
- R17. The node shall keep Pilot's 4-channel PWM/DSHOT/BDSHOT platform-portability port driven from the PRUs.

#### Security

- R18. The cape shall carry one SLB9672 TPM on an AM3358 SPI bus.
- R19. The BBE shall be strapped to boot from its TrustME flash.

#### Upgrade path

- R20. The cape shall reserve placement area, routing and host pins for the trust-module MCU and its secure element, so B is reached by population and firmware alone.
- R21. When B is populated, CAN-FD shall move from the A-path SPI controller to the trust-module MCU, with the A-path controller left unpopulated.

#### Consolidation

- R22. Each function duplicated across Pilot and TACCO shall appear once: the CAN-FD group, the RS-485 group, the 1553C group, the TPM, the power-entry filter and Nano-Fit connector, and the GNSS.

#### Physical and power

- R23. The cape outline and mounting holes shall follow the BeagleBone Black cape outline the BBE keeps, and the BBE and cape holes shall be the stack's primary structural load path, with the P8/P9 headers carrying no structural load.
- R24. The node shall take one 5 V power entry that feeds both the cape and the BBE, sized for the combined worst case including radio TX peaks.
- R25. The cape shall budget its top-face and bottom-face component heights against the reworked BBE and the R4 to R6 adapters, measured, not assumed.

#### EMC and isolation

- R26. The board shall carry Pilot Rev T's functional isolation scheme (`ISO_BAND` rule area and the 0.5 mm `ISOLATION` DRC rule) and TACCO's EMC targets (IEC 61000-4-2 Level 4, 61000-4-4 Level 4, 61000-4-5 Level 3, MIL-STD-461G RE102 / RS103), with the RF radios in a shielded zone separate from the isolation band.

#### Failover

- R27. The node shall take any PACE role (watchdog, comms, flight control, payload) by the fleet's heartbeat negotiation, with no hardwired role at power-on.
- R28. Loss of any one node shall leave the remaining three connected on every bus and on the Ethernet ring.

### Acceptance Examples

- AE1. **Covers R11, R28.** **Given** a 4-node ring, **when** one node loses power, **then** RSTP reconverges the other three into a line and they keep exchanging traffic on Ethernet, CAN-FD, RS-485 and 1553C.
- AE2. **Covers R8.** **Given** the node on a live CAN-FD trunk, **when** another node sends FD frames, **then** the node produces no error frames.
- AE3. **Covers R20, R21.** **Given** an A-build board, **when** the trust-module MCU and secure element are populated and the A-path CAN-FD controller is removed, **then** the node passes the same bus tests with new firmware and no board change.
- AE4. **Covers R6.** **Given** a fully assembled, pouched stack, **when** a technician plugs a USB-C cable into the device port, **then** the host enumerates for flashing and console access without disassembly.

### Success Criteria

- Mass: the reworked BBE plus cape weighs less than the two-node stack it replaces, measured on first articles of both (the two-node stack is about 140 g (0.31 lbm) by estimate; a BeagleBone Black is 39.68 g (0.0875 lbm)).
- Volume: the stack envelope does not exceed 1.10 times the pair of pouched nodes, 2 x 2.28 x 1.46 x 0.87 in (2 x 58 x 37 x 22 mm), about 5.76 in3 (94.4 cm3). The current estimate is about 6.2 in3 (101 cm3), that is about 1.07 times.
- CPU: ArduPilot plus the full comms stack runs on a real BBE Industrial WiFi at no more than 60 % average CPU on the bench (assumed threshold).
- Routability: the board reaches 0 unconnected, 0 DRC and 0 parity, which neither predecessor cape reached at its outline.

### Scope Boundaries

- ArduPilot and Linux bring-up, and the B trust-module firmware.
- Re-siting Serenity's nodes. The 3.402 x 2.098 in (86.4 x 53.3 mm) outline fits the cargo chin floor but not the aft strip; that re-siting is Serenity integration work.
- Changes to the Observer, Commo, Flight Engineer or Bus-Gateway boards.
- Dual-redundant 1553 (bus B), and the anti-tamper mesh that Pilot Rev T did not carry forward.
- The SanCloud Automotive add-on cape (CAN, GNSS, cellular): it duplicates NoNFO-Pilot functions and its CAN controller is unpublished.

<!-- ce-section: work-relationships -->
### How This Work Fits Together

This plan owns the BBE-hosted NoNFO-Pilot. The breakdown below is the current understanding, not a committed roadmap.

- NoNFO-Pilot-PB2 (BBE outline, PB2-I host): a sibling variant on the same outline and mounting positions. Shares the consolidated function set, harness and mounting interface with this plan. Can proceed independently of this plan. Still to decide: its name, and whether both variants share one cape layout.
- Serenity node re-siting: depends on this plan's final outline and stack height.
- Fleet trust module (Serenity-UAV): enables R20 and R21.

### Dependencies / Assumptions

- SanCloud has published no mass, mounting-hole drawing, Wi-Fi chip, Ethernet PHY part or boot-strap detail for the BBE. All five are assumed equal to the BeagleBone Black where the BBE is described as a BBB enhancement, and shall be confirmed.
- The 140 g stack mass is an estimate (Pilot about 50 g and TACCO about 65 g are estimates in Serenity-UAV `docs/AVIONICS_PB2_REDESIGN.md`, which is marked superseded).
- The BBE Industrial temperature range is stated as both -40 to 105 degC and -40 to 85 degC on SanCloud's page; design to 85 degC.

### Outstanding Questions

#### Resolve Before Planning

- R13 conflicts with the 2026-10-12 owner decision to move GNSS to isolated CAN-FD pucks in the dorsal cups (Serenity-UAV `avionics/WBS.md`, GNSS puck item). Decide whether NoNFO-Pilot keeps an on-cape MAX-M10S or consumes the puck over CAN-FD.

#### Deferred to Planning (first gates)

- Whether CPSW port 2 RMII and its reference clock reach P8/P9 on the BBE without conflicting with eMMC or other fixed functions. If not, ring port 2 falls back to USB Ethernet.
- Whether Linux CPSW switchdev with STP/RSTP offload is supported on the AM3358 kernel the fleet will run.
- Which Ethernet PHY the BBE carries, and whether it links reliably on two pairs at a forced 100 Mb/s.
- The measured height of the R4 to R6 adapters under the cape.
- The P9 VDD_5V back-power path on the BBE (R24) and the combined 5 V current budget.
- Which SPI CAN-FD controller the A path uses, and the SPI chip-select map across CAN-FD, HI-6138, TPM, IMU and 802.15.4.

### Sources / Research

- SanCloud, "BeagleBone Enhanced (BBE)" product and comparison page, <https://sancloud.com/beaglebone-enhanced-bbe/> (accessed 2026-10-11).
- BeagleBoard.org, "SanCloud BeagleBone Enhanced", <https://www.beagleboard.org/?p=1687>, and "SanCloud Industrial", <https://beagleboard.org/boards/sancloud-beaglebone-enhanced-industrial> (accessed 2026-10-11).
- GitHub user `mirkix`, BBBMINI, <https://github.com/mirkix/BBBMINI>, CC BY-SA 4.0: PRU1 for 12 PWM outputs and RC capture, SPI1 for IMU and barometer, CAN for ESCs.
- PocketPilot project, <https://github.com/PocketPilot/PocketPilot>, CC BY-SA 4.0: the v1 to v2 move to JST-GH connectors after loose connections on moving vehicles.
- Serenity-UAV `avionics/kicad/Pilot/Pilot.md` (Rev T), `avionics/kicad/TACCO/TACCO.md` (Rev T), `avionics/kicad/PB2_HEADER_PINMAP.md`, `avionics/AGENTS.md`, `docs/CARGO_SECTION_LAYOUT.md`.
- BeagleBoard.org, BeagleBone Black System Reference Manual (BBB mass 39.68 g); this figure shall be re-verified against the SRM before it is used in a mass roll-up.
