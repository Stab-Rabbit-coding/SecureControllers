# NoNFO-Pilot-PB2 — Parts and Footprint Verification (S35)

**Owner / engineer of record:** Steve Griffing (GitHub `Stab-Rabbit-coding`)
**Drafted by:** Claude (Anthropic), sprint S35, 2026-11-17
**License:** CC BY-SA 4.0 (documentation)
**Tooling:** KiCad 9.0.2 `pcbnew` (pad geometry read from every `.kicad_mod`); data sheets read with `pdftotext` and, for drawings, rendered at 300 to 400 dpi.

## Method

1. Export the Pilot and TACCO bills of materials from their schematics with `kicad-cli sch export bom`, merge them, fit each duplicated function once, and add the option-B+ and owner-decided parts (`docs/BOM.csv`, 54 lines).
2. Read every footprint's pad count, pad sizes, pitch and courtyard with `pcbnew` (`docs/footprint_geometry.json`). All 60 footprints load in KiCad 9.0.2.
3. Compare each against its manufacturer's data sheet, and record the result in the `fp_check` column:
   - `generator-cited`: drawn by the Pilot or TACCO generator from the cited figure or table, and the generator does not flag it.
   - `kicad-lib-vs-ds`: KiCad library footprint whose package code, pitch and outline match the data sheet's package.
   - `regenerated-S35` or `corrected-S35`: new or replaced in this sprint from the OEM land pattern (`scripts/gen_nonfo_pb2_footprints.py`).
   - `UNVERIFIED`: no OEM drawing could be read this sprint; listed under open items.
4. Apply the sourcing gate (root `AGENTS.md` §5) to every manufacturer by domicile and control.

## Findings

| ID | Finding | Effect here | Effect on the fleet |
|---|---|---|---|
| F1 | TACCO's `TPS6303x_VSON-10_2p5` was scaled from a 3 x 3 mm part and draws 3-2-3-2 pads on four sides. TI's DSK0010A has 5 pads on each of two sides (example board layout 4218903/C). It would not solder. | Replaced by `NoNFO:TI_DSK0010A_WSON-10-1EP_2.5x2.5mm_P0.5mm_EP1.2x2mm`. | TACCO carries the defect. |
| F2 | TACCO's W25Q128JVSIQ uses the 150-mil SOIC-8 footprint. Winbond package code S is the 8-pin SOIC 208-mil (D/E 5.28 mm, H 7.90 mm; data sheet §10.1). | Corrected to `Package_SO:SOIC-8_5.3x5.3mm_P1.27mm` (pad centres 7.17 mm apart). | TACCO carries the defect. |
| F3 | The AX88772E is sold only as AX88772EQF, "Commercial temperature range: 0 to 70 C" (ASIX data sheet v1.03 §7). The fleet requires -40 to +85 C. | The owner-chosen Ethernet pattern (OD-4) carries a commercial-grade part. **Owner decision OD-22.** | Every Pilot carries it. |
| F4 | TACCO's CAN and RS-485 TVS, Nexperia PRTR5V0U2X, fails the sourcing rule: Nexperia is owned by Wingtech (PRC). It is also a 5 V part on a -7 to +12 V RS-485 line. | Not used: Pilot's ESD2CAN24 and CDSOT23-SM712 are kept. | TACCO carries it. |
| F5 | `avionics/AGENTS.md` requires logging to "hardware-enforced non-executable microSD", but the PB2-I header carries no SD bus. **Resolved by OD-23 (owner, 2026-11-17): the microSD runs on the USB hub.** The hub becomes the Microchip USB2641i, which has a built-in SD reader on its third port; the write-block PLD drives the reader's SD_WP input (pin 13), as it drives the NOR flash /WP. | Molex 105162-0001 socket restored; USB2422 replaced by USB2641i-HZH-02. | TACCO's slot is unhosted for the same reason; the same hub fix applies. |
| F6 | The LWB5+ module data sheet is behind a free Ezurio login. Root `AGENTS.md` §5 allows a free registration wall when the documents carry no confidentiality terms; none were found. | Passes; access route recorded in Serenity `REFERENCES.md` REF-SENSOR-066. | — |
| F7 | KiCad library pads differ slightly in length from two OEM land patterns: SLB9672 (KiCad 0.80 mm vs Infineon 0.70 mm) and MAX-M10S (pitch and widths match Table 44; pad length to confirm against Figure 30). | Accepted for S36; S37 confirms or regenerates. | — |

## Rejected candidates

| Candidate | Reason | Source |
|---|---|---|
| TI TUSB4020BI (USB 2.0 hub) | Passes sourcing (TI, US) and temperature, but HTQFP-48 at about 9 x 9 mm against 4 x 4 mm for the USB2422 | TI SLLSEI0E |
| WCH CH334 (USB hub) | Manufacturer domiciled in the PRC | sourcing rule |
| Nexperia PRTR5V0U2X (TVS) | Manufacturer controlled from the PRC (Wingtech); 5 V rating too low for RS-485 | F4 |
| Wurth 749010012A (magnetics) | 8.9 mm tall; Pilot's 1.9 mm Pulse TC1G00 pair does the job | TACCO.md, Pilot BOM |
| Microchip USB2422 (USB hub) | Two downstream ports only; OD-23 needs a third for the SD reader. Superseded by the USB2641i | DS00001726B |
| Silex SX-USBAC, Edimax IEW-7811UTC (Wi-Fi) | Temperature range; licence-gated driver (Silex) | Serenity `docs/WIFI_MODULE_OD20_BRIEF.md` |

## Courtyard budget (`scripts/courtyard_budget.py`)

| Zone | Top face | Bottom face (0402 passives) | Result |
|---|---:|---:|---|
| Isolation island | 72 % | 7 % | PASS |
| Logic | **89 %** | 7 % | **FAIL by 9 points** |
| RF | 72 % | 8 % | PASS |
| Power entry | 64 % | 15 % | PASS |

The logic zone fails because the two PB2-I header rails alone take about 840 mm2 of its 2,134 mm2; the 7 x 7 mm hub and the microSD socket (OD-23) added 7 points. The zone boundaries are S34 placeholders that S38's floorplan sets; the candidate fixes, for S38, are moving the two oscillators, the NOR flash and the PLD into the RF zone's spare area (it is at 72 %), or widening the RF zone. Passive counts are estimates until S36 generates the schematic.

## Per-part result

| Line | MPN | Maker (domicile) | Footprint | Check |
|---|---|---|---|---|
| 1 | HI-6138PCIF | Holt Integrated Circuits (US) | `Holt_HI-6138_QFN-48_6x6mm_P0.4mm_EP4.6mm` | generator-cited |
| 2 | PM-DB2791S | Premier Magnetics (US) | `Xfmr_1553_SMD_0.40in_8pin` | generator-cited |
| 3 | SMAJ33CA | Bourns (US) | `D_SMA` | kicad-lib-vs-ds |
| 4 | ISOW1044BDFMR | Texas Instruments (US) | `SOIC-20W_7.5x12.8mm_P1.27mm` | kicad-lib-vs-ds |
| 5 | ISOW1412DFMR | Texas Instruments (US) | `SOIC-20W_7.5x12.8mm_P1.27mm` | kicad-lib-vs-ds |
| 6 | SRF2012-121YA | Bourns (US) | `Bourns_SRF2012_4T` | generator-cited |
| 7 | CX0805MRX7R0BB472 | YAGEO (Taiwan) | `X2Y_0805_4T` | generator-cited |
| 8 | ESD2CAN24DCKRQ1 | Texas Instruments (US) | `SOT-323_SC-70` | kicad-lib-vs-ds |
| 9 | CDSOT23-SM712 | Bourns (US) | `SOT-23` | kicad-lib-vs-ds |
| 10 | DP83825IRMQR | Texas Instruments (US) | `Texas_RMQ0024A_WQFN-24-1EP_3x3mm_P0.4mm_EP1.` | kicad-lib-vs-ds |
| 11 | AX88772EQF | ASIX Electronics (Taiwan) | `QFN-32-1EP_4x4mm_P0.4mm_EP2.9x2.9mm` | kicad-lib-vs-ds; PART FAILS -40 to +85 C (0 to 70 C only): owner decision OD-22 |
| 12 | TC1G00 | Pulse Electronics (YAGEO) (Taiwan) | `Pulse_TC1G00_PulseChip_4.7x3.2mm` | generator-cited |
| 13 | ECS-2520MV-500-BN-TR | ECS Inc. (US) | `Oscillator_SMD_ECS_2520MV-xxx-xx-4Pin_2.5x2.` | kicad-lib-vs-ds |
| 14 | ECS-2520MV-250-BN-TR | ECS Inc. (US) | `Oscillator_SMD_ECS_2520MV-xxx-xx-4Pin_2.5x2.` | kicad-lib-vs-ds |
| 15 | ECS-200-20-33-AGM-TR | ECS Inc. (US) | `Crystal_SMD_3225-4Pin_3.2x2.5mm` | kicad-lib-vs-ds |
| 16 | SLB9672XU20FW1611XUMA1 | Infineon Technologies (Germany) | `QFN-32-1EP_5x5mm_P0.5mm_EP3.6x3.6mm` | kicad-lib-vs-ds |
| 17 | ICM-42688-P | TDK InvenSense (Japan) | `Bosch_LGA-14_3x2.5mm_P0.5mm` | kicad-lib-vs-ds |
| 18 | BMP388 | Bosch Sensortec (Germany) | `Bosch_BMP388_LGA-10_2x2mm` | generator-cited |
| 19 | M0G3519QRGZRQ1 | Texas Instruments (US) | `VQFN-48-1EP_7x7mm_P0.5mm_EP4.1x4.1mm` | kicad-lib-vs-ds |
| 20 | USB2641i-HZH-02 | Microchip Technology (US) | `Microchip_VQFN-48-1EP_7x7mm_P0.5mm_EP4.2x4.2` | regenerated-S35 |
| 21 | ECS-240-20-33-AGM-TR | ECS Inc. (US) | `Crystal_SMD_3225-4Pin_3.2x2.5mm` | kicad-lib-vs-ds |
| 22 | 453-00046 | Ezurio (US) | `Ezurio_LWB5plus_LGA-68_17x12mm` | regenerated-S35 |
| 23 | MAX-M10S-00B | u-blox (Switzerland) | `ublox_MAX` | kicad-lib-vs-ds |
| 24 | STM32WLE5JCU6 | STMicroelectronics (Switzerland) | `QFN-48-1EP_7x7mm_P0.5mm_EP5.6x5.6mm` | kicad-lib-vs-ds |
| 25 | TG2520SMN 32MHz 1.8V | Seiko Epson (Japan) | `Oscillator_SMD_SeikoEpson_TG2520SMN-xxx-xxxx` | kicad-lib-vs-ds |
| 26 | PE4259-63 | pSemi (Murata) (US) | `SOT-363_SC-70-6` | kicad-lib-vs-ds |
| 27 | LBES5PL2EL-923 | Murata (Japan) | `Murata_Type2EL_LGA107` | generator-cited |
| 28 | ESD101-B1-02ELS | Infineon Technologies (Germany) | `Infineon_TSSLP-2-4_0.62x0.32mm` | library-verified (SecureControllers VERIFICATION.md) |
| 29 | U.FL-R-SMT-1(10) | Hirose (Japan) | `U.FL_Hirose_U.FL-R-SMT-1_Vertical` | kicad-lib-vs-ds |
| 30 | W25Q128JVSIQ | Winbond (Taiwan) | `SOIC-8_5.3x5.3mm_P1.27mm` | corrected-S35 (TACCO used the 150-mil SOIC-8) |
| 54 | 105162-0001 | Molex (US) | `microSD_Molex_105162-0001` | generator-cited |
| 31 | ATF16V8BQL-15XU | Microchip Technology (US) | `TSSOP-20_4.4x6.5mm_P0.65mm` | kicad-lib-vs-ds |
| 32 | TPD4E05U06DQAR | Texas Instruments (US) | `TI_DQA0010A_USON-10_2.5x1.0mm_P0.5mm` | generator-cited |
| 33 | MF-PSMF035X-2 | Bourns (US) | `Fuse_0805_2012Metric` | kicad-lib-vs-ds |
| 34 | TPSM828224SILR | Texas Instruments (US) | `TI_SIL0010D_uSiP-10_2.0x2.5mm_P0.5mm` | generator-cited |
| 35 | TPS62933DRLR | Texas Instruments (US) | `SOT-583-8` | kicad-lib-vs-ds |
| 36 | 74438335033 | Wurth Elektronik (Germany) | `L_WE-MAPI_3015` | generator-cited |
| 37 | TPS63031DSKR | Texas Instruments (US) | `TI_DSK0010A_WSON-10-1EP_2.5x2.5mm_P0.5mm_EP1` | regenerated-S35 |
| 38 | TLV75718PDBVR | Texas Instruments (US) | `SOT-23-5` | kicad-lib-vs-ds |
| 39 | TSM-118-04-L-DV-LC | Samtec (US) | `PocketBeagle2_2x18_P1_TSM-DV-LC` | generator-cited |
| 40 | TSM-118-04-L-DV-LC | Samtec (US) | `PocketBeagle2_2x18_P2_TSM-DV-LC` | generator-cited |
| 41 | TSM-108-01-L-DV | Samtec (US) | `Samtec_TSM-108-01-x-DV` | generator-cited |
| 42 | 105313-1204 | Molex (US) | `Molex_NanoFit_1x04_Horizontal` | UNVERIFIED |
| 43 | SM04B-GHS-TB(LF)(SN) | JST (Japan) | `JST_GH_SM04B-GHS-TB_1x04-1MP_P1.25mm_Horizon` | kicad-lib-vs-ds |
| 44 | SM03B-GHS-TB(LF)(SN) | JST (Japan) | `JST_GH_SM03B-GHS-TB_1x03-1MP_P1.25mm_Horizon` | kicad-lib-vs-ds |
| 45 | SM06B-GHS-TB(LF)(SN) | JST (Japan) | `JST_GH_SM06B-GHS-TB_1x06-1MP_P1.25mm_Horizon` | kicad-lib-vs-ds |
| 46 | KMR211NG LFS | C&K (US) | `SW_Push_1P1T_NO_CK_KMR2` | UNVERIFIED |
| 47 | TC2030-IDC-NL footprint | Tag-Connect (no part) (US) | `Tag-Connect_TC2030-IDC-NL_2x03_P1.27mm_Verti` | not-a-part |
| 48 | 0603 green / red | to select in S36 (-) | `LED_0603_1608Metric` | passive-case |
| 49 | BLM15EX331SN1D | Murata (Japan) | `L_0402_1005Metric` | passive-case |
| 50 | 742792512 | Wurth Elektronik (Germany) | `L_0805_2012Metric` | passive-case |
| 51 | M3 PGND | (no part) (-) | `MountingHole_3.2mm_M3_DIN965` | kicad-template |
| 52 | CC0402/0603/0805/1210 series | YAGEO (Taiwan) | `C_0402/0603/0805/1210` | passive-case |
| 53 | RC0402/0603 series | YAGEO (Taiwan) | `R_0402/0603` | passive-case |

## Open items

- **105313-1204** (Molex Nano-Fit power entry): the Molex sales drawing could not be fetched (molex.com is outside this session's network allowance; Mouser serves a bot-block page). Pilot's generator already flags this land as not verified. Owner: supply the drawing, or allow `www.molex.com`.
- **KMR211NG LFS** (C&K KMR2 mLRS boot button): no data sheet in the repository. Owner: supply it, or drop the button if the STM32WLE5 boot pin can be reached over the Tag-Connect pads.
- **OD-22**: industrial-grade replacement for the AX88772EQF, or accept a commercial part (F3).
- S38: logic-zone courtyard fill (89 % against 80 %).
