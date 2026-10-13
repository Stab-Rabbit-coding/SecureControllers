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
