# REFERENCES.md — SecureControllers Standards and Regulatory Reference Catalog

Catalogs every applicable standard cited anywhere in this repository, per
`CLAUDE.md`. Format: `[REF-ID §section]`.

## Documentation Standards

### REF-MIL-001: CNAF M-3710.7 — NATOPS General Flight and Operating Instructions Manual, §1.5 (Warnings, Cautions, and Notes) and §1.6 (Wording)

| Field | Value |
| --- | --- |
| **Publisher** | Department of the Navy, Commander, Naval Air Forces (CNAF) |
| **Designation** | CNAF M-3710.7 (COMNAVAIRFOR M-3710.7), 2 May 2016, Original |
| **Official URL** | <https://www.mynatec.navair.navy.mil/> (NATEC NATOPS library, access-restricted); verified against pages 1–52 of the issued manual (front matter, Chapter 1, Glossary, List of Abbreviations/Acronyms), held locally in this repository at `docs/cnaf-3710.7_1-52.pdf` — the canonical local copy referenced by every sibling repo's own `REFERENCES.md`/`REF-MIL-001` entry in this workspace |
| **Applied sections** | §1.5 "Warnings, Cautions, and Notes" (p.1-5); §1.6 "Wording" (p.1-5) |
| **Note** | This repository is not a Navy NATOPS publication and does not claim compliance as a whole — only the §1.5 callout-severity definitions and §1.6 requirement-verb conventions are adopted. The active-vs-passive-voice guidance paired with this citation in `CLAUDE.md` is a project addition, not sourced from CNAF M-3710.7. |
| **Cross-repo ID** | The same manual is **REF-MIL-003** in Serenity-UAV's `REFERENCES.md` (there, REF-MIL-001 is MIL-STD-1553C). IDs are repo-local: cite the ID of the repository you are writing in. |

**Used in:** `CLAUDE.md` "Documentation Standards → Warnings, Cautions, Notes, and Wording".

## NoNFO-Pilot Design Sources

These entries catalog the external resources cited by the NoNFO-Pilot board family (`kicad/NoNFO-Pilot/`). They are vendor, community and prior-art sources rather than standards. Entries marked **requires verification** have not yet been checked against the issuing body by a human reviewer.

### REF-NFP-001: SanCloud, "BeagleBone Enhanced (BBE)" product and variant comparison page

| Field | Value |
| --- | --- |
| **Publisher** | SanCloud Ltd |
| **Official URL** | <https://sancloud.com/beaglebone-enhanced-bbe/> (fetched 2026-10-11) |
| **Applied sections** | Variant comparison table: SoC, RAM, Ethernet, Wi-Fi/BT, IMU/barometer, USB, temperature range, secure-boot SPI-NOR, dimensions 86.40 x 53.3 mm |
| **Note** | The page states both -40 to 105 degC and -40 to 85 degC for the Industrial variants; the design uses 85 degC. No mass or mounting drawing is published. |

**Used in:** `docs/plans/2026-10-12-001-feat-nonfo-pilot-bbe-plan.md`; `kicad/NoNFO-Pilot/NoNFO-Pilot.md`.

### REF-NFP-002: BBBMINI autopilot cape for BeagleBone (GitHub user `mirkix`)

| Field | Value |
| --- | --- |
| **Publisher** | GitHub user `mirkix` (CC BY-SA 4.0) |
| **Official URL** | <https://github.com/mirkix/BBBMINI> (fetched 2026-10-11) |
| **Applied sections** | README interface list: PRU1 PWM/RC capture, SPI1 IMU/barometer, CAN for ESCs |

**Used in:** `docs/plans/2026-10-12-001-feat-nonfo-pilot-bbe-plan.md`.

### REF-NFP-003: PocketPilot flight controller for PocketBeagle

| Field | Value |
| --- | --- |
| **Publisher** | PocketPilot project (CC BY-SA 4.0) |
| **Official URL** | <https://github.com/PocketPilot/PocketPilot> (fetched 2026-10-11) |
| **Applied sections** | README version history: v1 loose connections led to JST-GH connectors in v2/v3 |

**Used in:** `docs/plans/2026-10-12-001-feat-nonfo-pilot-bbe-plan.md`.

### REF-NFP-004: BeagleBoard.org PocketBeagle 2 documentation

| Field | Value |
| --- | --- |
| **Publisher** | BeagleBoard.org Foundation |
| **Official URL** | <https://docs.beagleboard.io/boards/pocketbeagle-2/01-introduction.html> and <https://docs.beagleboard.io/boards/pocketbeagle-2/03-design-and-specifications.html> (not re-fetched: this host is outside the session's network allowance) |
| **Verified against** | The PocketBeagle 2 System Reference Manual held in Serenity-UAV at `avionics/datasheets/beagleboard/pocketbeagle2_srm.pdf` (Serenity REF-SENSOR-041), read 2026-11-14 |
| **Applied sections** | SRM §3.8.1 Table 3.2, Dimensions & weight: PCB 55 x 35 mm, 1.6 mm, 10 layers, max height 13.6 mm, net weight 12.7 g; SRM Quick Start: 5 V at 1 A supply via USB-C or the cape header |

**Used in:** `docs/ideation/2026-10-12-nonfo-pilot-pb2-ideation.html`; `kicad/NoNFO-Pilot/PB2/zone_contract.json`.

### REF-NFP-005: CNX Software, "PocketBeagle 2 SBC gets Industrial version with 1GB RAM, 64GB eMMC flash" (2026-02-24)

| Field | Value |
| --- | --- |
| **Publisher** | CNX Software |
| **Official URL** | <https://www.cnx-software.com/2026/02/24/pocketbeagle-2-sbc-gets-industrial-version-with-1gb-ram-64gb-emmc-flash/> (**requires verification**, as for REF-NFP-004) |
| **Applied sections** | PB2-I memory, storage and temperature range |

**Used in:** `docs/ideation/2026-10-12-nonfo-pilot-pb2-ideation.html`.

### REF-NFP-006: Pixhawk Autopilot Bus, Pixhawk standard DS-010

| Field | Value |
| --- | --- |
| **Publisher** | Dronecode Foundation / Pixhawk standards |
| **Official URL** | <https://docs.px4.io/main/en/flight_controller/pixhawk_autopilot_bus> (**requires verification**; DS-010 PDF itself not yet retrieved) |
| **Applied sections** | Prior art for an FMU module on a carrier baseboard |

**Used in:** `docs/ideation/2026-10-12-nonfo-pilot-pb2-ideation.html`.

### REF-NFP-012: Microchip USB2422 2-port USB 2.0 hub controller, data sheet DS00001726B

| Field | Value |
| --- | --- |
| **Publisher** | Microchip Technology Inc., DS00001726B (2013-2015) |
| **Official URL** | <https://ww1.microchip.com/downloads/en/DeviceDoc/00001726B.pdf> (HTTP 200, 2026-11-17) |
| **Local copy** | `datasheets/USB2422-DS00001726B.pdf` (MD5 a98a88516e71d96bd846e0b8afd5d52c) |
| **Applied sections** | Features (24 MHz crystal, -40 to +85 C industrial grade -I/MJ); Figure 2-1 pinout; §7.0 Figure 7-1 24-SQFN package and PCB land pattern |
| **Openness / sourcing** | Public, no NDA. Microchip is US-domiciled. |

**Used in:** `kicad/NoNFO-Pilot/PB2/NONFO_PB2_FOOTPRINT_VERIFICATION.md`; `kicad/NoNFO-Pilot/PB2/scripts/gen_nonfo_pb2_footprints.py`.

### REF-NFP-013: TI TUSB4020BI two-port USB 2.0 hub, data sheet SLLSEI0E (rejected candidate)

| Field | Value |
| --- | --- |
| **Publisher** | Texas Instruments, SLLSEI0E, July 2015, revised July 2024 |
| **Official URL** | <https://www.ti.com/lit/ds/symlink/tusb4020bi.pdf> (HTTP 200, 2026-11-17) |
| **Local copy** | `datasheets/tusb4020bi-SLLSEI0E.pdf` (MD5 b50cf563fcef53e51397946646911ce9) |
| **Applied sections** | Package HTQFP-48 (PHP); -40 to +85 C. Recorded as the rejected alternative on area. |
| **Openness / sourcing** | Public, no NDA. TI is US-domiciled. |

**Used in:** `kicad/NoNFO-Pilot/PB2/NONFO_PB2_FOOTPRINT_VERIFICATION.md`; `kicad/NoNFO-Pilot/PB2/scripts/gen_nonfo_pb2_footprints.py`.

### REF-NFP-014: Microchip USB2640i/USB2641i industrial USB 2.0 hub and flash media controller, data sheet DS00001948C

| Field | Value |
| --- | --- |
| **Publisher** | Microchip Technology Inc., DS00001948C (2015-2021) |
| **Official URL** | <https://ww1.microchip.com/downloads/aemDocuments/documents/UNG/ProductDocuments/DataSheets/USB2640i-USB2641i-Data-Sheet-DS00001948C.pdf> (HTTP 200, 2026-11-17) |
| **Local copy** | `datasheets/USB2640i-USB2641i-DS00001948C.pdf` (MD5 132e0d33cbe65b2074dc651efb96bc5d) |
| **Applied sections** | General Description (three downstream ports, one wired to the internal flash media reader; -40 to +85 C); pin diagram (pin 13 SD_WP, pin 14 SD_nCD); Figure 11-1 sheet 2 recommended land pattern, variant C; product identification (USB2641i-HZH-02) |
| **Openness / sourcing** | Public, no NDA. Microchip is US-domiciled. |

**Used in:** `kicad/NoNFO-Pilot/PB2/scripts/gen_nonfo_pb2_footprints.py`; `kicad/NoNFO-Pilot/PB2/docs/BOM.csv`.

### REF-NFP-015: C&K (Littelfuse) KMR2 Series tactile switch data sheet

| Field | Value |
| --- | --- |
| **Publisher** | Littelfuse, Inc. (C&K Switches), KMR2 Series data sheet, revised 01/28/26 |
| **Official URL** | Supplied by the owner 2026-11-17 (Littelfuse/C&K product documentation) |
| **Local copy** | `datasheets/Littelfuse-CK-KMR2-Series-Datasheet.pdf` (MD5 5d8b01a9b0bbd012a3dcad50e27d6585) |
| **Applied sections** | p.1 NG terminations recommended layout; Environmental Characteristics (silver: -40 to +85 C); ordering table (KMR211NG LFS) |
| **Openness / sourcing** | Public, no NDA. Littelfuse is US-domiciled. |

**Used in:** `kicad/NoNFO-Pilot/PB2/docs/BOM.csv`; `kicad/NoNFO-Pilot/PB2/NONFO_PB2_FOOTPRINT_VERIFICATION.md`.

### REF-NFP-016: Molex Nano-Fit 105313 right-angle header sales drawing and product sheet

| Field | Value |
| --- | --- |
| **Publisher** | Molex Electronic Technologies, LLC, sales drawing SD-105313-100 rev P1 (released 2025/06/26, EC 826596), and product sheet for 1053131204 (generated 2026-11-18) |
| **Official URL** | Supplied by the owner 2026-11-18 from the molex.com part page for 1053131204 |
| **Local copy** | `datasheets/molex/1053131204_sd.pdf` (MD5 276602c0cdc35cfd3e95e8173daabd34); `datasheets/molex/1053131204.pdf` (MD5 8d9eb01aec0167edafec7f23d97d5d48) |
| **Applied sections** | Drawing sheet 1 "RECOMMENDED PCB (CONNECTOR SIDE VIEW)"; sheet 4 table row 105313-1204 (A 10.94, B 7.50, C 8.14); product sheet: 8.0 A per contact, 0.510 g, PCB locator and retention |
| **Openness / sourcing** | Public, no NDA. Molex is US-domiciled (Lisle, Illinois). |

**Used in:** `kicad/NoNFO-Pilot/PB2/docs/BOM.csv`; `kicad/NoNFO-Pilot/PB2/NONFO_PB2_FOOTPRINT_VERIFICATION.md`.

### EMC and bus standards inherited from Serenity-UAV

The NoNFO-Pilot plan carries the Serenity Pilot and TACCO EMC targets and MIL-STD-1553C. Their Serenity IDs collide with this repository's `REF-MIL-001`, so they are catalogued here under non-colliding IDs. Each entry below is copied from Serenity-UAV `REFERENCES.md` (2026-11-14), where it was validated; the Serenity ID is kept in each heading for traceability.

### REF-NFP-007 (Serenity REF-IEC-003): IEC 61000-4-2:2008 — Electromagnetic Compatibility (EMC) — Testing and Measurement Techniques — Electrostatic Discharge (ESD) Immunity Test

| Field | Value |
| --- | --- |
| **Issuing authority** | International Electrotechnical Commission (IEC) |
| **Edition** | Second edition (2008-12) |
| **Official URL (purchase)** | <https://webstore.iec.ch/> — search "IEC 61000-4-2" |
| **Note** | Supersedes IEC 61000-4-2:1995+AMD1:1998+AMD2:2000. Exact webstore product-page URL not confirmed during catalog entry (see Open Standards Verification Items). |

**Clauses applied in this project:**

| Clause | Title | Application |
| --- | --- | --- |
| §5 | Classification of ESD generators | Contact discharge ±8 kV (Level 4), air discharge ±15 kV (Level 4) at all field connectors |
| §8 | Test levels | Level 4 is the highest defined test level; selected as design target for the 500 W/m² hostile EMI environment [REF-NIST-002 §6.2.5] |

**Applied to:** TVS arrays at all JST-GH field connectors on Pilot (ESD2CAN24-Q1 on CAN, CDSOT23-SM712
on RS-485 since 2026-10-18) and XO (PRTR5V0U2X, pending the fleet sourcing audit);
shielded Flight Engineer enclosure provides ESD isolation for PDB connectors.

**Used in:** `avionics/kicad/Pilot.md`, `avionics/kicad/XO.md`, `avionics/kicad/FlightEngineer.md`

---

### REF-NFP-008 (Serenity REF-IEC-004): IEC 61000-4-4:2012 — Electromagnetic Compatibility (EMC) — Testing and Measurement Techniques — Electrical Fast Transient/Burst (EFT/Burst) Immunity Test

| Field | Value |
| --- | --- |
| **Issuing authority** | IEC |
| **Edition** | Third edition (2012-04) |
| **Official URL (purchase)** | <https://webstore.iec.ch/> — search "IEC 61000-4-4" |
| **Note** | Supersedes IEC 61000-4-4:2004+AMD1:2010. Exact webstore product-page URL not confirmed during catalog entry (see Open Standards Verification Items). |

**Clauses applied in this project:**

| Clause | Title | Application |
| --- | --- | --- |
| §5.2 | Test levels | Level 4 (4 kV peak, 5/50 ns) on all signal lines |

**Applied to:** Common-mode chokes (CM2: Bourns SRF2012-100Y) and isolated transceivers
(ISOW1044BDFMR, ADM2795EBRWZ) on Pilot and XO signal buses.

**Used in:** `avionics/kicad/Pilot.md`, `avionics/kicad/XO.md`

---

### REF-NFP-009 (Serenity REF-IEC-005): IEC 61000-4-5:2014+AMD1:2017 — Electromagnetic Compatibility (EMC) — Testing and Measurement Techniques — Surge Immunity Test

| Field | Value |
| --- | --- |
| **Issuing authority** | IEC |
| **Edition** | Third edition 2014-05, consolidated with Amendment 1 (2017-03) |
| **Official URL (purchase)** | <https://webstore.iec.ch/> — search "IEC 61000-4-5" |
| **Note** | Supersedes IEC 61000-4-5:2005. The 2017 Amendment 1 introduced clarifications to coupling/decoupling network parameters. Exact webstore product-page URL not confirmed during catalog entry (see Open Standards Verification Items). |

**Clauses applied in this project:**

| Clause | Title | Application |
| --- | --- | --- |
| §5.2 | Test levels | Level 3 (2 kV CM, 1 kV DM) on CAN FD and RS-485 bus lines; Level 3 (±2 kV CM, ±1 kV DM) on VBAT |
| Annex A | Combination wave generator | Defines the 1.2/50 µs (voltage) / 8/20 µs (current) surge waveform |

**Applied to:** ADM2795EBRWZ RS-485 transceiver (rated ±42 V bus fault — exceeds IEC 61000-4-5
Level 3 ±2 kV CM surge on bus); SMBJ33CA TVS (D1) on Flight Engineer VBAT line; TVS arrays at
field connectors on Pilot (ESD2CAN24-Q1 / CDSOT23-SM712, both rated to IEC 61000-4-5 surge per
REF-SENSOR-053 / REF-SENSOR-054) and XO (PRTR5V0U2X).

**Used in:** `avionics/kicad/Pilot.md`, `avionics/kicad/XO.md`, `avionics/kicad/FlightEngineer.md`

---

### REF-NFP-010 (Serenity REF-MIL-002): MIL-STD-461G — Requirements for the Control of Electromagnetic Interference Characteristics of Subsystems and Equipment

| Field | Value |
| --- | --- |
| **Issuing authority** | U.S. Department of Defense (DoD), Assistant Secretary of Defense for Acquisition |
| **Edition** | Revision G (11 August 2015); Change Notice 1 (CN1) issued 9 December 2019 |
| **Official access** | DLA ASSIST QuickSearch: <https://assist.dla.mil/> (search "MIL-STD-461") |
| **Note** | Public domain per 10 U.S.C. §4252; no purchase required. Revision G supersedes MIL-STD-461F (2007). The CN1 addendum corrects test procedures; G+CN1 is the current applicable revision. |

**Requirements applied in this project:**

| Requirement | Title | Application |
| --- | --- | --- |
| RE102 | Radiated Emissions, Electric Field | Limit C applies to all avionics subsystems; 100BASE-TX EMI suppressed via HX1188NL magnetics, CMCs, and TVS arrays on Pilot and XO |
| RS103 | Radiated Susceptibility, Electric Field | 200 V/m, 10 kHz–18 GHz; isolated buses + chassis-grounded Flight Engineer enclosure provide margin |
| CS101 | Conducted Susceptibility, Power Leads | 50 V, 30 Hz – 150 kHz; π-filter bulk caps on Flight Engineer BECs |
| CS114 | Conducted Susceptibility, Bulk Cable Injection | Curve 05; two-stage CM filter (CM1+CM2, > 80 dB at 10 MHz) + Y-caps to chassis |
| CE102 | Conducted Emissions, Power Leads | Limit B; CM1+CM2 input chokes + π-filter on each BEC |

**Applied to:** Pilot (Cape-A-2), XO (Cape-B-2), and Flight Engineer EMC compliance targets.  The
design environment (500 W/m², E ≈ 434 V/m) [REF-NIST-002 §6.2.5] exceeds all MIL-STD-461G
RS103 limits; compliance with 200 V/m RS103 is a design floor, not the design ceiling.  Full
MIL-STD-461G qualification testing is deferred pending airframe integration.

**Used in:** `avionics/kicad/Pilot.md`, `avionics/kicad/XO.md`, `avionics/kicad/FlightEngineer.md`,
`docs/AVIONICS_PB2_REDESIGN.md`

---

### REF-NFP-011 (Serenity REF-MIL-001): MIL-STD-1553C — Digital Time Division Command/Response Multiplex Data Bus

| Field | Value |
| --- | --- |
| **Issuing authority** | U.S. Department of Defense (DoD); comments to AFLCMC/EZSS, Wright-Patterson AFB |
| **Edition** | MIL-STD-1553C, 28 February 2018, superseding MIL-STD-1553B (21 September 1978). AMSC N/A, Area AVCS. |
| **Official access** | DLA ASSIST: <https://assist.dla.mil/> (search "MIL-STD-1553"). Public mirror of the ASSIST copy: <https://www.altadt.com/wp-content/uploads/dlm_uploads/2020/12/MIL-STD-1553C.pdf> |
| **Distribution** | Distribution Statement A: approved for public release; distribution is unlimited |
| **Verified** | Text checked against the ASSIST-sourced copy on 2026-09-28 (Claude Opus 5.5) |

**Relation to 1553B.** 1553C is a document revision. Its electrical and protocol
requirements are the same as 1553B. The changes are clarified text and figures, the EMC
wiring reference moved to MIL-STD-464 (§4.5.1.5.3), and added "superseding valid commands"
paragraphs for RT and BC operation (§4.4.3.2, §4.6.3.2). Alta Data Technologies, which
publishes the mirror, says in its cover note: "1553C is a document change only … There
are no functional changes to 1553B." A terminal that meets 1553B electrically therefore
meets 1553C electrically. RT firmware must still implement §4.4.3.2.

**Sections applied in this project (verified against the 1553C text):**

| Section | Title | Requirement applied |
| --- | --- | --- |
| §4.3.3.8 | Response time | RT responds to a valid command within 4.0–12.0 µs |
| §4.4.3.2 | Superseding valid commands | RT behavior when a new valid command arrives; required in the RT firmware or protocol engine |
| §4.5.1.2 | Characteristic impedance | Cable Zo of 70.0–85.0 Ω at 1.0 MHz |
| §4.5.1.3 | Cable attenuation | ≤ 1.5 dB per 100 ft (30.5 m) at 1.0 MHz |
| §4.5.1.5.1 | Transformer coupled stubs | Stub should not exceed 20 ft (6.1 m) |
| §4.5.1.5.1.1 | Coupling transformer | Bus coupler turns ratio 1:1.41 ± 3.0 % |
| §4.5.1.5.2 | Direct coupled stubs | Stub should not exceed 1 ft (0.305 m) |
| §4.5.1.5.2.1 | Fault isolation | 55.0 Ω ± 2.0 % isolation resistor in series with each bus connection |
| §4.5.1.5.3 | Wiring and cabling for EMC | MIL-STD-464 wiring and cabling provisions apply |
| §4.5.2 | Terminal characteristics | Terminal output and input levels for transformer and direct coupling |

**Corrected 2026-09-28.** The earlier 1553B entry cited §4.1, §4.2, §4.3, §4.4, §4.6, and
Table IV. It also gave a transformer-coupling threshold of "0.9 m (0.03 ft)", which is
wrong: the direct-stub limit is 1 ft (0.305 m). Those citations did not match the
standard's paragraph numbering and are replaced by the verified rows above. The old
"Applied to" text described the retired DS26LV31/DS26LV32 and PE-68515 chain. The current
chain is the HI-1573 or HI-6138 with the PM-DB2791S (`avionics/WBS.md` §1.2a.2 and
§1.2a.3).

**Used in:** `docs/AVIONICS_PB2_REDESIGN.md`, `avionics/kicad/Pilot/Pilot.md`,
`avionics/kicad/TACCO/TACCO.md`, `avionics/WBS.md` §1.2a.2 and §1.2a.3,
`avionics/kicad/HI6138_FOOTPRINT_VERIFICATION.md`, `avionics/kicad/Pilot/scripts/gen_pilot_sch.py`,
`avionics/kicad/TACCO/scripts/gen_tacco_sch.py`, `avionics/firmware/WBS.md`,
`avionics/firmware/dts/Pilot/k3-am6254-pocketbeagle2-serenity-cape-a2.dts`,
`avionics/firmware/dts/TACCO/k3-am6254-pocketbeagle2-serenity-cape-b2.dts`,
`docs/plans/2026-09-29-001-feat-commo-standalone-bus-node-plan.md`

---

## Removed / Superseded Citations

None yet.

<!-- workspace-rule: component-sourcing-openness 2026-10-17 -->
## Component Sourcing and Open-Hardware References (workspace rule, 2026-10-17)

Entries added by Claude Opus 5.5 on 2026-10-17 for the workspace "Component Sourcing and
Openness" rule in `AGENTS.md`; each source was read from the URL shown on that date.

### REF-LAW-001: Public Law 117-263 (FY2023 NDAA) §5949 — Prohibition on certain semiconductor products and services

| Field | Value |
| --- | --- |
| **Issuing authority** | 117th U.S. Congress; James M. Inhofe National Defense Authorization Act for Fiscal Year 2023, Pub. L. 117-263, 136 Stat. 2395; §5949 at 136 Stat. 3485 ff., codified as a note to 41 U.S.C. §4713 |
| **Official access** | <https://www.congress.gov/117/plaws/publ263/PLAW-117publ263.htm> (enrolled text, HTTP 200, 2026-10-17) |
| **Section applied** | §5949(a)(1) prohibition on executive-agency procurement of electronic parts that include covered semiconductor products or services; §5949(c)(1) effective five years after enactment; §5949(j)(3)(A)-(C) covered semiconductor products (SMIC, CXMT, YMTC, and entities owned or controlled by, or connected to, the government of a foreign country of concern); §5949(j)(5) foreign country of concern -> 15 U.S.C. §4651(7) |
| **Cited in** | `AGENTS.md` "Component Sourcing and Openness" |

### REF-LAW-002: Public Law 118-31 (FY2024 NDAA) Div. A Title XVIII Subtitle B — American Security Drone Act of 2023

| Field | Value |
| --- | --- |
| **Issuing authority** | 118th U.S. Congress; National Defense Authorization Act for Fiscal Year 2024, Pub. L. 118-31, 137 Stat. 136; Subtitle B "Drone Security", §§1821-1833 at 137 Stat. 691 ff., codified as a note preceding 41 U.S.C. §3901 |
| **Official access** | <https://www.congress.gov/118/plaws/publ31/PLAW-118publ31.htm> (enrolled text, HTTP 200, 2026-10-17) |
| **Section applied** | §1821 short title; §1822(1)(A)-(E) "covered foreign entity", incl. (D) entities domiciled in, or subject to influence or control by the government or Communist Party of, the People's Republic of China and (E) their subsidiaries and affiliates; §1823(a) prohibition on executive-agency procurement of unmanned aircraft systems manufactured or assembled by a covered foreign entity, including "communication links and the components that control the unmanned aircraft" |
| **Cited in** | `AGENTS.md` "Component Sourcing and Openness" |

### REF-LAW-003: 15 U.S.C. §4651(7) "foreign country of concern" and 10 U.S.C. §4872 "covered nation"

| Field | Value |
| --- | --- |
| **Issuing authority** | United States Code (Office of the Law Revision Counsel), read via Cornell LII |
| **Official access** | <https://www.law.cornell.edu/uscode/text/15/4651>; <https://www.law.cornell.edu/uscode/text/10/4872> (HTTP 200, 2026-10-17); authoritative text <https://uscode.house.gov/> |
| **Section applied** | 15 U.S.C. §4651(7)(A)-(B): a "covered nation" under 10 U.S.C. §4872 plus any country the Secretary of Commerce determines to be engaged in conduct detrimental to U.S. national security or foreign policy. 10 U.S.C. §4872 "covered nation" = the Democratic People's Republic of Korea, the People's Republic of China, the Russian Federation and the Islamic Republic of Iran (§4651(7)(A) cites §4872(d); the current code places the definition at §4872(f)(2)). §4872's own restriction covers magnets, tungsten, tantalum, molybdenum, germanium and gallium — only its country list is used here |
| **Cited in** | `AGENTS.md` "Component Sourcing and Openness" |

### REF-LIC-001: OSHWA Open Source Hardware Certification — requirements

| Field | Value |
| --- | --- |
| **Publisher** | Open Source Hardware Association (OSHWA) |
| **Official access** | <https://certification.oshwa.org/requirements.html> (HTTP 200, 2026-10-17) |
| **Section applied** | "Requirements" item 3: all parts within the creator's control open source; third-party proprietary components distinguished; "Third-party components such as chips must have fully accessible and shareable datasheets" |
| **Cited in** | `AGENTS.md` "Component Sourcing and Openness" |
