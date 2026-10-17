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
| **Official URL** | <https://docs.beagleboard.io/boards/pocketbeagle-2/01-introduction.html> and <https://docs.beagleboard.io/boards/pocketbeagle-2/03-design-and-specifications.html> (**requires verification**: retrieved by a research sub-agent, not yet read by a human reviewer) |
| **Applied sections** | Board size 55 x 35 mm, mass 12.7 g, USB-C power and data, expansion-header shared-ball warning |

**Used in:** `docs/ideation/2026-10-12-nonfo-pilot-pb2-ideation.html`.

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

### EMC and bus standards inherited from Serenity-UAV

The NoNFO-Pilot plan carries the Serenity Pilot and TACCO EMC targets (IEC 61000-4-2, 61000-4-4 and 61000-4-5; MIL-STD-461G RE102/RS103) and MIL-STD-1553C. Those are catalogued in Serenity-UAV's `REFERENCES.md` (`REF-IEC-003`, `REF-IEC-004`, `REF-IEC-005`, `REF-MIL-002`; Serenity's MIL-STD-1553 entry). They are **not yet** catalogued here; their Serenity IDs collide with this repository's `REF-MIL-001`. **Requires verification** before any NoNFO-Pilot design file cites them, tracked in `TODO.md` §5.0.

## Removed / Superseded Citations

None yet.

<!-- workspace-rule: component-sourcing-openness 2026-10-17 -->
## Component Sourcing and Open-Hardware References (workspace rule, 2026-10-17)

Entries added by Claude Opus 5.5 on 2026-10-17 for the workspace "Component Sourcing and
Openness" rule in `AGENTS.md`; each source was read from the URL shown on that date.

### REF-LAW-001: Public Law 117-263 (FY2023 NDAA) §5949 — Prohibition on certain semiconductor products and services

| Field | Value |
|---|---|
| **Issuing authority** | 117th U.S. Congress; James M. Inhofe National Defense Authorization Act for Fiscal Year 2023, Pub. L. 117-263, 136 Stat. 2395; §5949 at 136 Stat. 3485 ff., codified as a note to 41 U.S.C. §4713 |
| **Official access** | <https://www.congress.gov/117/plaws/publ263/PLAW-117publ263.htm> (enrolled text, HTTP 200, 2026-10-17) |
| **Section applied** | §5949(a)(1) prohibition on executive-agency procurement of electronic parts that include covered semiconductor products or services; §5949(c)(1) effective five years after enactment; §5949(j)(3)(A)-(C) covered semiconductor products (SMIC, CXMT, YMTC, and entities owned or controlled by, or connected to, the government of a foreign country of concern); §5949(j)(5) foreign country of concern -> 15 U.S.C. §4651(7) |
| **Cited in** | `AGENTS.md` "Component Sourcing and Openness" |

### REF-LAW-002: Public Law 118-31 (FY2024 NDAA) Div. A Title XVIII Subtitle B — American Security Drone Act of 2023

| Field | Value |
|---|---|
| **Issuing authority** | 118th U.S. Congress; National Defense Authorization Act for Fiscal Year 2024, Pub. L. 118-31, 137 Stat. 136; Subtitle B "Drone Security", §§1821-1833 at 137 Stat. 691 ff., codified as a note preceding 41 U.S.C. §3901 |
| **Official access** | <https://www.congress.gov/118/plaws/publ31/PLAW-118publ31.htm> (enrolled text, HTTP 200, 2026-10-17) |
| **Section applied** | §1821 short title; §1822(1)(A)-(E) "covered foreign entity", incl. (D) entities domiciled in, or subject to influence or control by the government or Communist Party of, the People's Republic of China and (E) their subsidiaries and affiliates; §1823(a) prohibition on executive-agency procurement of unmanned aircraft systems manufactured or assembled by a covered foreign entity, including "communication links and the components that control the unmanned aircraft" |
| **Cited in** | `AGENTS.md` "Component Sourcing and Openness" |

### REF-LAW-003: 15 U.S.C. §4651(7) "foreign country of concern" and 10 U.S.C. §4872 "covered nation"

| Field | Value |
|---|---|
| **Issuing authority** | United States Code (Office of the Law Revision Counsel), read via Cornell LII |
| **Official access** | <https://www.law.cornell.edu/uscode/text/15/4651>; <https://www.law.cornell.edu/uscode/text/10/4872> (HTTP 200, 2026-10-17); authoritative text <https://uscode.house.gov/> |
| **Section applied** | 15 U.S.C. §4651(7)(A)-(B): a "covered nation" under 10 U.S.C. §4872 plus any country the Secretary of Commerce determines to be engaged in conduct detrimental to U.S. national security or foreign policy. 10 U.S.C. §4872 "covered nation" = the Democratic People's Republic of Korea, the People's Republic of China, the Russian Federation and the Islamic Republic of Iran (§4651(7)(A) cites §4872(d); the current code places the definition at §4872(f)(2)). §4872's own restriction covers magnets, tungsten, tantalum, molybdenum, germanium and gallium — only its country list is used here |
| **Cited in** | `AGENTS.md` "Component Sourcing and Openness" |

### REF-LIC-001: OSHWA Open Source Hardware Certification — requirements

| Field | Value |
|---|---|
| **Publisher** | Open Source Hardware Association (OSHWA) |
| **Official access** | <https://certification.oshwa.org/requirements.html> (HTTP 200, 2026-10-17) |
| **Section applied** | "Requirements" item 3: all parts within the creator's control open source; third-party proprietary components distinguished; "Third-party components such as chips must have fully accessible and shareable datasheets" |
| **Cited in** | `AGENTS.md` "Component Sourcing and Openness" |
