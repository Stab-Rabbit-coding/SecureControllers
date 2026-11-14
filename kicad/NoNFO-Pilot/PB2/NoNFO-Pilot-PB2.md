# NoNFO-Pilot-PB2 — Board Status

**Owner / engineer of record:** Steve Griffing (GitHub `Stab-Rabbit-coding`)
**Drafted by:** Claude (Anthropic), sprint S34, 2026-11-14
**License:** CC BY-SA 4.0 (documentation)
**Plan:** Serenity-UAV `docs/plans/2026-11-14-001-feat-nonfo-pilot-pb2-stern-stack-plan.md` (sprints S34 to S41)
**Stage:** S34 complete. No schematic, PCB or generator exists yet; S35 (parts and footprints) is next.

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

## Open items

Tracked in `TODO.md` §5.2 and Serenity-UAV `avionics/WBS.md` §1.11.
