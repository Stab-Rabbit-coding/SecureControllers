# NoNFO-Pilot-PB2 — Board Status

**Owner / engineer of record:** Steve Griffing (GitHub `Stab-Rabbit-coding`)
**Drafted by:** Claude (Anthropic), sprint S34, 2026-11-14
**License:** CC BY-SA 4.0 (documentation)
**Plan:** Serenity-UAV `docs/plans/2026-11-14-001-feat-nonfo-pilot-pb2-stern-stack-plan.md` (sprints S34 to S41)
**Stage:** S36 done (2026-11-18): generated schematic, ERC 0 errors and 0 warnings, ledger match, KiCad CI job. S35 closed 2026-11-18. No PCB yet (S37 and S38).

## What this board is

One carrier that merges the Serenity Pilot and TACCO capes onto one PocketBeagle 2 Industrial (PB2-I). First use: the stern (Simon) control stack of Serenity-UAV. The PB2-I rides on top of the carrier.

## Owner decisions in force

| Decision | Value | Date |
|---|---|---|
| Use | Serenity stern stack; the other three stacks stay Pilot + TACCO | 2026-11-12 |
| Outline | BeagleBone Black cape size; mass minimised, no floor | 2026-11-12, 2026-11-14 |
| Ethernet | DP83825I on RMII2 plus AX88772E on USB1, Linux bridge | 2026-11-12 |
| GNSS | On-cape MAX-M10S, first function removed if space, mass or routing is short | 2026-11-12 |
| Architecture (OD-18) | B+: MSPM0G3519-Q1 owns CAN-FD, RS-485, the HI-6138 and the slow lines | 2026-11-14 |
| PACE (OD-19) | Option B; Simon is Watchdog P, Flight Control E | 2026-11-14 |
| Wi-Fi (OD-20) | Ezurio Sterling-LWB5+ 453-00046 (MHF4), USB mode | 2026-11-14 |

## S34 results (2026-11-14)

| Gate | Result | Tool |
|---|---|---|
| PB2-I header, option B+ | FITS, 2 spare (P2-35, P2-36) | `pin_ledger/pin_ledger.py --require B+` |
| MCU, MSPM0G3519-Q1 RGZ-48 | FITS: 31 lines on 44 ports, 12 spare; SWD (PA19, PA20) and BSL invoke (PA18) kept free | `pin_ledger/mcu_ledger.py` |
| Fit at Simon | PASS standing portrait (3.40 in vertical), shifted 0.04 in (1 mm) to starboard, harness zone to port. Landscape fails. Margin is 1 mm: re-run on the placed board's STEP in S38. | Serenity-UAV `tools/nonfo_simon_fit.py` |
| Stack height | 0.777 in (19.74 mm) against the 0.81 in (20.5 mm) target | same |
| Stack mass, pouched | 0.201 lbm (91.0 g) on a 1.6 mm board, 0.189 lbm (85.7 g) on 1.0 mm; limit below 107 g | same |
| 5 V peak load | 3.12 A, 15.6 W (several lines assumed; see the zone contract) | same |

**Mass credit.** Against the 107 g pouched pair it replaces, the stack saves 16.0 g (1.6 mm board) to 21.3 g (1.0 mm). The ledger's −58 g figure assumed a merged board as light as Pilot and is replaced in S41.

**Thermal.** The peak electrical load, 15.6 W, all ends as heat in the stack. A temperature rise needs the heat path to the hull, which S40 computes; nothing here says the stack is thermally safe yet.

## MCU allocation (option B+)

From `pin_ledger/mcu_ledger.py`, TI SLASFA6B Table 6-2:

| Function | Ports |
|---|---|
| CAN-FD | CAN0 TX PA12, RX PA13; standby PA3 |
| RS-485 | UART0 TX PA28, RX PA31, DE (RTS) PA15 |
| MIL-STD-1553 (HI-6138) | SPI1 SCK PA17, PICO PB15, POCI PA16; CS PA4, MR PA5, TX inhibit PA6, IRQ PA0 (open-drain-only port, input) |
| Host link to the PB2-I | SPI0 SCK PA11, PICO PA14, POCI PA10, CS0 PA2; IRQ to host PA7 |
| Write-block PLD | PA8, PA9, PA22 to PA27, PB2 |
| Fan PWM, Wi-Fi enable | PA21 (timer), PB3 |
| Spare | PA1, PB6 to PB9, PB14, PB16 to PB20, PB24 |

S36 may reassign ports inside these instances for routing; the ledger re-checks every change.

## Files

| File | What it is |
|---|---|
| `ARCHITECTURE_BRIEF.md` | OD-18 brief (decided B+) |
| `zone_contract.json` | Outline, holes, zones, height limits, mass and power lines (canonical; Serenity-UAV keeps a copy) |
| `pin_ledger/` | AM625 and MSPM0G3519 mux tables, net demand, solvers |
| `tests/test_pin_ledger.py` | Ledger tests (run in `.github/workflows/kicad.yml`) |
| `scripts/port_blocks.py` | Copies the Pilot and TACCO schematic blocks from Serenity-UAV into `sch/ported_blocks.json` |
| `scripts/gen_nonfo_pb2_sch.py` | S36 schematic generator: ported blocks, ledger-driven header and MCU, new hub, Wi-Fi and rail blocks |
| `kicads/NoNFO-Pilot-PB2.kicad_{sch,sym,pro}`, `.net`, `sym-lib-table`, `fp-lib-table` | Generated KiCad project (do not hand-edit) |
| `tests/test_sch_matches_ledger.py` | Schematic-to-ledger, isolation, decoupling and pull-resistor tests, with negative controls |
| `spice/input_filter.cir` | 5 V entry filter under the merged load step (ngspice) |

## S35 results (2026-11-17)

See `NONFO_PB2_FOOTPRINT_VERIFICATION.md`: 53-line BOM, all makers pass the sourcing gate, three footprints drawn from OEM land patterns (Sterling-LWB5+, USB2422, TPS63031), one corrected (W25Q128JV 208-mil). Findings F1 to F7, including two TACCO footprint defects and a commercial-temperature NIC on every Pilot.

## S36 results (2026-11-18)

**Schematic.** 265 parts, 1,270 pins, 217 nets on one generated sheet. ERC (KiCad 9.0.2): **0 errors, 0 warnings, so there are no accepted warnings to list.** The netlist exporter prints a generic annotation notice, because references such as `CAN-TR` do not end in a number (the Pilot and TACCO convention). This is not an ERC result. 28 tests pass.

| Test | Result |
|---|---|
| Every B+ ledger net is on exactly its ledger header pin; no other header signal; console free | PASS |
| Every MCU ledger net is on its RGZ-48 pin | PASS |
| Every net reaches at least two pins | PASS |
| No DC path from GND2_CAN or GND2_RS485 to GND, or between them | PASS (negative control: a 0 R bridge is caught) |
| Every IC power pin has a capacitor to ground on its net | PASS |
| Data-sheet-mandatory pull resistors present (MCU NRST and BSL, hub reset and SPI_CLK, Wi-Fi strap, flash WP, 1553 IRQ, card detect, BT/15.4 PDn) | PASS (negative control: removing `R-MCU-RST` is caught) |
| Every fitted S35 BOM part is on the schematic | PASS |

The plan asked for the pull-up negative control to fail KiCad's ERC. It cannot: on a net-label schematic, a missing pull-up leaves every pin connected, so ERC has nothing to flag. The control therefore runs on the design-rule test above instead.

**What changed from the two source boards.**
- **Header:** P1 and P2 come from `pin_ledger.py` option B+. The power and USB pins come from Pilot's map.
- **MCU:** the bus transceivers, HI-6138 SPI, PLD inputs, fan and Wi-Fi enable are re-pointed to the MCU, per `mcu_ledger.py`.
- **USB:** USB1 now feeds the USB2641i hub. Port 2 goes to the AX88772E, port 3 to the LWB5+, and the hub's card reader serves the logging microSD (OD-23).
- **Not carried over:**
  - TACCO's 1553, CAN, RS-485, TPM and PHY blocks, because the Pilot copies are newer.
  - TACCO's TPS62933 3V3 buck.
  - Pilot's M2.5 holes, which become M3 holes for the BeagleBone Black pattern.

**Defects found in the source boards (fleet pass, Serenity-UAV NFP-TACCO-FP):**
- **F9, TACCO mLRS UART.** The PB2-I transmit line reaches STM32WLE5 PA2, which is USART2_TX [stm32wle5jc.pdf pin table]. It is crossed here: PB2-I TX to PA3 (RX), PA2 to PB2-I RX.
- **F10, input bead.** Pilot's FB1 (742792512) is rated 2 A against a 3.5 A merged peak, so it was changed to Wurth 742792510 (5 A) on its data-sheet high-current land. TACCO already uses 742792510, but on the narrower IPC land.

### Power budget (worst case)

"(est.)" marks a figure not yet taken from a data-sheet current table. S40's electrical-load check replaces each one.

| Rail, regulator (rating) | Loads | Worst case | Margin |
|---|---|---|---|
| +3V3, TPSM828224 (2 A) | HI-6138 transmit 695 mA [Pilot.md]; DP83825I 58 mA [Pilot.md]; TPM 35 mA [Pilot.md]; AX88772E 100 mA (est.); USB2641i 80 mA (est.); microSD card at the CRD_PWR limit, 200 mA [DS00001948C Table 6-1]; GNSS 25 mA (est.); NOR flash 25 mA (est.); MCU, PLD, IMU, baro, LPO 20 mA (est.) | 1.24 A | 62 % load |
| +3V3_RF, TPS63031 (800 mA step-down) | mLRS STM32WLE5 at +22 dBm, 140 mA (est.); BT/15.4 module, 100 mA (est.); 1V8 LDO loads, 60 mA (est.) | 0.30 A | 38 % load |
| +3V6_WIFI, TPSM82822 (2 A) | LWB5+ peak PHY calibration, 768 mA [LWB5+ data sheet, current consumption] | 0.77 A | 38 % load |
| +5V, harness entry (Nano-Fit 8 A/contact, two contacts; FB1 5 A) | PB2-I 1.0 A (est.); two ISOW converters, 0.3 A (est.); the three regulators above at 88 to 90 % efficiency, 1.79 A; fan 0.1 A (est.); expansion port fuse hold 0.35 A | 3.5 A | FB1 at 70 % of its 5 A rating |

The J-PWM +5V pins are treated as an ESC signal reference, not a servo power bus. This is an assumption, and the owner should confirm it.

**5 V entry simulation** (`spice/input_filter.cir`, ngspice 42). The model is a 0.5 A to 3.5 A step at 1 A/µs behind an assumed 3 ft (0.9 m) harness of 0.6 µH and 30 mΩ. Results: minimum 4.53 V, overshoot 5.23 V, settled 4.79 V.

> **CAUTION:** the dip comes within 30 mV of the 4.5 V ISOW VDD floor [Pilot.md 2026-10-17], so a weak supply or a longer harness would brown out the bus transceivers. Hold the supply at least 5.1 V at the stern-stack connector, or keep the harness resistance at or below 30 mΩ; S41's harness check confirms one or the other. Most of the steady drop (0.21 V at 3.5 A) is the harness and FB1 DC resistance, so a larger bulk capacitor would not fix it.

**Open items from S36** (tracked in `TODO.md` §5.2):
- Select the 32.768 kHz LPO part (BOM line 56).
- Confirm the LWB5+ VBAT and VOUT_3P3 decoupling values against an Ezurio reference schematic, which is not in the repository.
- The TACCO mLRS RF matching values are still marked "VERIFY AN5457" (carried over unchanged).
- The PLD JEDEC fuse map, which now also drives the microSD SD_WP.
- The MSPM0 SYSOSC frequency-correction resistor (100 kΩ, 0.1 %) is not fitted, because PA2 carries HOST_CSN.
- The FB-MLRS-1/2 signal-bead part number is still open from TACCO.

## Open items

Tracked in `TODO.md` §5.2 and Serenity-UAV `avionics/WBS.md` §1.11.
