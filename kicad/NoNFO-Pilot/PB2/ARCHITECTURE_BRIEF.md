# NoNFO-Pilot-PB2 — Owner Decision Brief: who drives the buses (OD-18)

**Owner / engineer of record:** Steve Griffing (GitHub `Stab-Rabbit-coding`)
**Drafted by:** Claude (Anthropic), 2026-11-14, at the owner's request of 2026-11-12 ("check the pinmux and pin ledger, then brief the options on hardware and firmware capabilities")
**License:** CC BY-SA 4.0 (documentation)
**Closes when decided:** `TODO.md` §5.2.4.
**Citations:** `REF-SENSOR-0xx` IDs are entries in Serenity-UAV's `REFERENCES.md`. They are not yet catalogued in this repository (`TODO.md` §5.0.2). **Format:** Serenity-UAV `docs/DOC_TEMPLATES.md`, "Owner Decision Briefs".

## The decision

NoNFO-Pilot-PB2 puts the Pilot and TACCO functions on one PocketBeagle 2 Industrial (PB2-I). The PB2-I header has 53 usable signal pins once the console is kept. The question is which processor drives the fleet buses and the slow housekeeping lines: the PB2-I alone, or the PB2-I with a trust-module microcontroller (MCU) beside it.

**Decided 2026-11-14: option B+** (owner). The recommendation was B+. It is the only option that fits the header with every function aboard, including the on-cape GNSS receiver. It costs a second firmware image and a host-link protocol that does not exist yet.

## How the answer was computed

`pin_ledger/pin_ledger.py` reads the AM625 mux table for every header ball [REF-SENSOR-049 Table 5-1] and the merged net list in `pin_ledger/pb2_net_demand.json`, then searches for a legal allocation. The net list is the union of the Pilot and TACCO header maps in the Serenity-UAV generators, with each duplicated function fitted once.

Changes from the two source maps, all applied to every option:

- The mLRS radio moves off UART0, so the PB2-I console stays free.
- A USB 2.0 hub on USB1 carries the AX88772E ring NIC and the Wi-Fi module (owner decision 2026-11-12: Pilot Ethernet pattern). One hub-reset line replaces Pilot's NIC VBUS line and TACCO's Wi-Fi interrupt.
- The on-cape GNSS receiver is restored (owner decision 2026-11-12): one UART and a PPS line.
- The microSD card-detect line is dropped. MMC2 data does not reach the header, so the TACCO microSD slot has no host; logging uses the PB2-I's eMMC and the W25Q128JV NOR flash.

## Options side by side

| | A | A-diet | B | **B+** |
|---|---|---|---|---|
| Who drives CAN-FD, RS-485, 1553 | PB2-I | PB2-I | MCU | MCU |
| Who drives the write-block PLD inputs, fan, Wi-Fi enable | PB2-I | I²C expander | PB2-I | MCU |
| Header nets needed | 66 | 55 | 59 | **48** |
| Fit, everything aboard | short 16 | short 5 | short 9 | **fits, 2 spare** |
| Fit, GNSS jettisoned | short 13 | short 2 | short 6 | **fits, 5 spare** |
| Fit, GNSS and the expansion SPI port both dropped | short 9 | fits, 2 spare | short 2 | fits, 9 spare |
| Firmware images | 1 | 1 | 2 | 2 |
| Bus presence while the PB2-I boots or hangs | none | none | kept | kept |

Source: `python3 pin_ledger/pin_ledger.py`, and the same with `--drop GNSS` and `--drop GNSS,EXT_SPI`.

"A first, B reserved" (the BBE variant's choice) is not a separate column: it has to fit as A, and A is 16 pins short.

## Hardware capability

- **PB2-I header** [REF-SENSOR-049 Table 5-1]. 55 signal positions; three are the fixed USB1 pins and two are the console. RMII2, MDIO0, SPI0 and USB1 each exist on one set of pins only, so those 16 positions are not negotiable in any option.
- **MSPM0-shared pins.** Eight header pins also carry the PB2-I's own MSPM0L1105 analog pins. In B+ with everything aboard, two inputs land on them: the 802.15.4 interrupt on P1-21 and the GNSS PPS on P1-23. The four DSHOT outputs move off the shared pins (Pilot has two there today). With GNSS jettisoned, no non-Ethernet net lands on a shared pin.
- **MCU.** MSPM0G3519-Q1 in the 48-pin RGZ package: Cortex-M0+ at 80 MHz, 512 KB flash, 128 KB SRAM, one CAN-FD controller in this package, AES and TRNG [REF-SENSOR-017 §1 and ordering table]. It is already on Observer, with a verified symbol and footprint in `Serenity-UAV/avionics/kicad/symbols/`. B+ asks about 31 of its I/O pins (CAN 3, RS-485 3, HI-6138 SPI and control 7, host SPI and IRQ 5, PLD 9, fan 1, Wi-Fi enable 1, SWD 2). Whether those 31 fit the RGZ-48 function map is **not yet verified**; it is pre-decision check PD1, owed before OD-18.
- **One CAN-FD bus only.** The RGZ-48 has one CAN-FD controller. The merged node needs one. A second bus would force the 64-pin package.
- **Sensors and motor outputs stay on the PB2-I in every option.** The IMU, barometer, TPM, flash and 802.15.4 radio stay on SPI0, and DSHOT stays on PRU0. No flight-critical loop crosses the MCU link.
- **Area.** B+ adds a 0.28 in (7 mm) square MCU and about ten passives. It removes nothing from the board that A would not also carry.

## Firmware capability

- **PB2-I today.** Debian with userspace daemons (`Serenity-UAV/avionics/firmware/fc`, `cn`). CAN-FD is the kernel's MCAN0 and RS-485 is a kernel UART with hardware driver-enable. In A and A-diet those drivers are used unchanged.
- **MCU today.** `Serenity-UAV/avionics/firmware/mspm0` is one template shared by every fleet MCU: XRCE-DDS over CAN-FD or RS-485, with a TPM-keyed message authentication code. Its README records two gaps: the peripheral drivers are open work, and the tree has not been re-targeted from the MSPM0G3507 to the MSPM0G3519-Q1.
- **What B and B+ add.** A host link between the PB2-I and the MCU over SPI0, on both ends. Nothing in either firmware tree implements it. The PB2-I end can be a userspace daemon that presents the MCU's CAN-FD bus as a virtual SocketCAN interface, so the flight software above it does not change. This is new work for Theme F (Serenity-UAV Rev U plan, S22 and S23), not for the board sprints.
- **What B and B+ buy.** The MCU answers bus heartbeats and holds the node's bus address while the PB2-I reboots. The stern stack is the bus-end terminator, and under the 2026-10-31 forward-trim plan it is the PACE Emergency path, so a node that drops off the bus for a Linux boot is the case to avoid.
- **Throughput.** A CAN-FD bus at 5 Mbit/s and 1553 at 1 Mbit/s are both below what an SPI link of several megahertz carries. The HI-6138 runs the 1553 protocol itself; the MCU only services its registers. Worst-case link latency is **not yet measured**.

## The checks

Avionics check set, Serenity-UAV `docs/DOC_TEMPLATES.md` (owner direction 2026-11-14).

| Check | Result |
|---|---|
| Electrical engineering: load | B and B+ add one MCU on the 3V3 rail. Its current is small beside the radios and the PB2-I, but it is **not yet computed**; the merged 5 V and 3V3 budget is sprint S34 work and applies to every option. |
| Electrical engineering: emissions | No option adds a switching converter or a radio. B and B+ add one SPI host link on the already-busy SPI0 and move the bus transceivers' logic side to the MCU. A-diet adds an I²C bus. No option changes the isolated converters, which are the board's main emitters. Not yet quantified. |
| Function | A, A-diet and B cannot carry the full function set. A-diet works only without GNSS and without the expansion SPI port. B+ carries everything. |
| Structural integrity | Does not apply: same board, same mounts in every option. |
| Mechanism and component interactions | B+ changes who talks to the three bus transceivers and the PLD. The write-block interlock moves from the logged host to the MCU, which separates the lock from the processor it protects. The MCU becomes a single point for the node's three wired buses; Ethernet and the radios do not pass through it. |
| Weight and balance | MCU and passives add under 0.02 oz (0.5 g). No option changes a fastener, a connector or the harness, so those ledger lines are equal across options. |
| Wire harness, fastener and mounting fit | Does not apply between options: connectors, harness and mounts are the same in all four. |
| Thermal load | B and B+ add the MCU's dissipation, expected to be a few tens of milliwatts and **not yet computed**. It does not change the board's main heat sources (PB2-I, radios, isolated converters). |

## Still unverified

1. The MSPM0G3519-Q1 RGZ-48 function map for the 31 lines above [REF-SENSOR-017 Table 6-2]. The package bonds 44 I/O pins, so the count fits; the function assignment is unchecked. This is pre-decision check PD1 in the Serenity-UAV plan, and its result is to be appended here before OD-18 is decided.
2. Host-link latency and the SocketCAN bridge design.
3. Whether the MCU needs its own secure element, or takes its keys from the PB2-I's SLB9672 at provisioning. This brief assumes one TPM, on the PB2-I.
4. The JEDEC fuse map of the write-block PLD, which decides how many of its nine inputs are really needed.

## Owner decision

The PACE role of the stern stack (OD-19) is an input: the case for B+ leans on the Emergency role, and Serenity-UAV `AGENTS.md` §9 lists Simon as A / C / A / P.

- [x] OD-18: architecture for NoNFO-Pilot-PB2 — A / A-diet / B / **B+ (recommended)**. **Decided 2026-11-14 by the owner: B+.** The MCU function-map check (PD1) becomes the first task of sprint S34; a failure there means the 64-pin package, not a different option.

## PD1 result (2026-11-14, sprint S34)

All 31 B+ lines fit the MSPM0G3519-Q1 RGZ-48 with 12 ports to spare, SWD and the BSL invoke pin kept free; the 64-pin package is not needed. The allocation and its source table are in `NoNFO-Pilot-PB2.md` and `pin_ledger/mcu_ledger.py` [REF-SENSOR-017 Table 6-2].
