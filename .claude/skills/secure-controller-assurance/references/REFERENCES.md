# REFERENCES — Secure Controller Assurance

Citation catalog for the `secure-controller-assurance` skill.  Every control in
[`control-matrix.md`](control-matrix.md) traces to a REF-ID below.  Format follows the
IEEE citation style required by the user's global engineering instructions.

**Verification status legend:**

- **VERIFIED — local copy** — the cited document is held locally and the cited section was
  read directly during authoring of this skill.
- **VERIFIED — public** — document is publicly retrievable at the listed URL; designation,
  title, and issuing body confirmed.
- **REQUIRES VERIFICATION** — the standard is real and correctly designated, but it is
  paywalled and no local copy was available.  Clause-level numbers marked with this status
  **must be checked against the purchased document before being quoted in a design record.**

---

## Primary sources (local copies held)

### REF-NIST-8259R1

[1] M. Fagan, K. N. Megas, B. Cuthill, J. Marron, and B. Hoehn, *Foundational Cybersecurity
Activities for IoT Product Manufacturers*, National Institute of Standards and Technology,
Gaithersburg, MD, NIST IR 8259r1, Apr. 2026. doi: 10.6028/NIST.IR.8259r1.

- URL: <https://doi.org/10.6028/NIST.IR.8259r1>
- Landing page: <https://csrc.nist.gov/pubs/ir/8259/r1/final>
- Supersedes NIST IR 8259 (May 2020), doi: 10.6028/NIST.IR.8259
- **Sections applied:** §1.1 (securable product definition); §2.2 (composition of IoT
  products); §2.5–2.6 (needs/goals, capabilities, means); §3.1–3.6 (Activities 0–5,
  pre-market); §4.1–4.3 (Activities 6–8, post-market); §4.3.1–4.3.6 (what to communicate).
- **Status:** VERIFIED — local copy (`SecureControllers/datasheets/NIST.IR.8259r1.pdf`).
- **Used by:** `references/nist-8259-8425.md`; controls SCA-NT-*, all phase gates.

### REF-NIST-8425

[2] M. Fagan, J. Marron, K. N. Megas, B. Cuthill, R. Herold, D. Lemire, and B. Hoehn,
*Profile of the IoT Core Baseline for Consumer IoT Products*, National Institute of
Standards and Technology, Gaithersburg, MD, NIST IR 8425, Sep. 2022.
doi: 10.6028/NIST.IR.8425.

- URL: <https://doi.org/10.6028/NIST.IR.8425>
- Landing page: <https://csrc.nist.gov/pubs/ir/8425/final>
- **Sections applied:** §2.2 (consumer profile); §2.2.1 (product capabilities: Asset
  Identification, Product Configuration, Data Protection, Interface Access Control, Software
  Update, Cybersecurity State Awareness); §2.2.2 (non-technical supporting capabilities:
  Documentation, Information and Query Reception, Information Dissemination, Product
  Education and Awareness).
- **Note on authorship:** the author list above is taken from the NIST landing page for
  IR 8425.  Only the cover pages of the local PDF were read during authoring; if this
  citation is reproduced in a formal design record, re-confirm the full author list against
  the landing page.  **Status of author list: REQUIRES VERIFICATION.**  Designation, title,
  date, and DOI: VERIFIED — local copy.
- **Used by:** `references/nist-8259-8425.md`; controls SCA-ID-*, SCA-CFG-*, SCA-DP-*,
  SCA-IA-*, SCA-SU-*, SCA-CS-*, SCA-NT-*.

### REF-NIST-800-82R3

[3] K. Stouffer, M. Pease, C. Tang, T. Zimmerman, V. Pillitteri, S. Lightman, A. Hahn,
S. Saravia, A. Sherule, and M. Thompson, *Guide to Operational Technology (OT) Security*,
National Institute of Standards and Technology, Gaithersburg, MD, NIST SP 800-82r3,
Sep. 2023. doi: 10.6028/NIST.SP.800-82r3.

- URL: <https://doi.org/10.6028/NIST.SP.800-82r3>
- Landing page: <https://csrc.nist.gov/pubs/sp/800/82/r3/final>
- **Sections applied:** §4.1 (managing OT security risk); §4.2.2 (safety systems);
  §5.1.2 (defense-in-depth strategy); §5.2.1–5.2.5 (DiD architecture layers 1–5:
  Security Management, Physical Security, Network Security, Hardware Security, Software
  Security); §5.3.1 (cyber-related safety considerations); §5.3.2 (availability);
  §5.3.6 (Field I/O — Purdue Level 0); §5.3.7 (additional considerations for IIoT);
  §5.4 (architecture models); §6 (applying the CSF to OT); App. C (threat sources,
  vulnerabilities, incidents); App. E (OT security capabilities and tools);
  App. F (OT Overlay), incl. F.3 (overlay summary), F.4 (tailoring), F.5 (OT communication
  protocols), F.7.1–F.7.19 (detailed overlay control specifications by SP 800-53 family).
- **Status:** VERIFIED — local copy (`SecureControllers/datasheets/NIST.SP.800-82r3.pdf`).
  Section numbers above read from the document's table of contents.
- **Used by:** `references/ot-ics-62443.md`; controls SCA-OT-*, SCA-SL-*.

### REF-NIST-800-207

[4] S. Rose, O. Borchert, S. Mitchell, and S. Connelly, *Zero Trust Architecture*, National
Institute of Standards and Technology, Gaithersburg, MD, NIST SP 800-207, Aug. 2020.
doi: 10.6028/NIST.SP.800-207.

- URL: <https://doi.org/10.6028/NIST.SP.800-207>
- Landing page: <https://csrc.nist.gov/pubs/sp/800/207/final>
- **Sections applied:** §2.1 (the seven tenets of zero trust); §2.2 (zero trust view of a
  network — six assumptions); §3 (logical components: policy engine, policy administrator,
  policy enforcement point, and the CDM / industry compliance / threat intelligence /
  activity log / data access policy / PKI / ID management / SIEM data sources);
  §3.1.1–3.1.3 (ZTA approach variants: enhanced identity governance, micro-segmentation,
  network infrastructure and software defined perimeters); §3.2.1 (device agent/gateway
  deployment).
- **Status:** VERIFIED — local copy (`SecureControllers/datasheets/NIST.SP.800-207.pdf`).
  Tenets and component definitions read directly.
- **Used by:** `references/zero-trust-207.md`; controls SCA-ZT-*.

### REF-NIST-800-213

[5] M. Fagan, J. Marron, K. N. Megas, and K. Boeckl, *IoT Device Cybersecurity Guidance for
the Federal Government: Establishing IoT Device Cybersecurity Requirements*, National
Institute of Standards and Technology, Gaithersburg, MD, NIST SP 800-213, Nov. 2021.
doi: 10.6028/NIST.SP.800-213.

- URL: <https://doi.org/10.6028/NIST.SP.800-213>
- Landing page: <https://csrc.nist.gov/pubs/sp/800/213/final>
- **Sections applied:** §2.1 (systems and elements); §2.2 (how IoT devices support
  security); §2.3 (how IoT devices may create security challenges); §3.1 (IoT device
  cybersecurity considerations); §3.2 and §3.2.1–3.2.5 (assessing risk: effects on threat
  sources and events, vulnerabilities and predisposing conditions, likelihood, magnitude of
  impact, updated risk assessment); §3.3 and §3.3.1–3.3.2 (identifying device cybersecurity
  requirements using SP 800-213A and other resources); §4.1 (challenges meeting device
  requirements); §4.2 (managing gaps).
- **Note on authorship:** author list taken from the NIST landing page; only the front
  matter and TOC of the local PDF were read.  **Status of author list: REQUIRES
  VERIFICATION.**  Designation, title, and section structure: VERIFIED — local copy.
- **Used by:** `SKILL.md` risk-and-gap workflow; controls SCA-GOV-*.

### REF-NIST-800-213A

[6] M. Fagan, J. Marron, K. N. Megas, and K. Boeckl, *IoT Device Cybersecurity Guidance for
the Federal Government: IoT Device Cybersecurity Requirement Catalog*, National Institute of
Standards and Technology, Gaithersburg, MD, NIST SP 800-213A, Nov. 2021.
doi: 10.6028/NIST.SP.800-213A.

- URL: <https://doi.org/10.6028/NIST.SP.800-213A>
- Landing page: <https://csrc.nist.gov/pubs/sp/800/213/a/final>
- **Sections applied:** §1.1 (purpose and applicability; definitions of *device
  cybersecurity capability* and *non-technical supporting capability*); §2 (Device
  Cybersecurity Capability Catalog — families DI, DC, DP, LA, SU, CS, DS and all
  subfamilies); §3 (Non-Technical Supporting Capability Catalog — families DO, IQ, ID, EA
  and all subfamilies); App. A (definition of the Federal Profile); App. B (mapping of
  SP 800-53 controls to device cybersecurity requirements); App. C (mapping of Cybersecurity
  Framework outcomes to device cybersecurity requirements).
- **Status:** VERIFIED — local copy
  (`SecureControllers/datasheets/NIST.SP.800-213A.pdf`).  All family and subfamily
  designators reproduced in `references/nist-213a-catalog.md` were read from the document's
  table of contents (pp. v–vii).
- **Note on authorship:** author list taken from the NIST landing page.  **Status of author
  list: REQUIRES VERIFICATION.**
- **Used by:** `references/nist-213a-catalog.md`; the capability spine of the entire
  control matrix.

---

## Secondary sources (public, not held locally)

### REF-NIST-8259A

[7] M. Fagan, K. N. Megas, K. Scarfone, and M. Smith, *IoT Device Cybersecurity Capability
Core Baseline*, National Institute of Standards and Technology, Gaithersburg, MD, NIST IR
8259A, May 2020. doi: 10.6028/NIST.IR.8259A.

- Landing page: <https://csrc.nist.gov/pubs/ir/8259/a/final>
- **Relationship:** IR 8425 §2.2.1 states its product capabilities derive from IR 8259A.
  That relationship is VERIFIED — local copy (IR 8425, Fig. 1).  The content of IR 8259A
  itself is **REQUIRES VERIFICATION** (not held locally).

### REF-NIST-8259B

[8] M. Fagan, K. N. Megas, K. Scarfone, and M. Smith, *IoT Non-Technical Supporting
Capability Core Baseline*, National Institute of Standards and Technology, Gaithersburg, MD,
NIST IR 8259B, Aug. 2021. doi: 10.6028/NIST.IR.8259B.

- Landing page: <https://csrc.nist.gov/pubs/ir/8259/b/final>
- **Relationship:** IR 8425 §2.2.2 states its developer activities derive from IR 8259B.
  VERIFIED — local copy (IR 8425, Fig. 1).  Content of IR 8259B: REQUIRES VERIFICATION.

### REF-NIST-800-53

[9] Joint Task Force, *Security and Privacy Controls for Information Systems and
Organizations*, National Institute of Standards and Technology, Gaithersburg, MD, NIST SP
800-53 Rev. 5, Sep. 2020 (incl. updates). doi: 10.6028/NIST.SP.800-53r5.

- Landing page: <https://csrc.nist.gov/pubs/sp/800/53/r5/upd1/final>
- **Sections applied:** control families referenced by the SP 800-82r3 OT Overlay
  (App. F.7.1–F.7.19) and by the SP 800-213A App. B mapping.
- **Status:** VERIFIED — public.  Specific control text: REQUIRES VERIFICATION before quotation.

### REF-NIST-CSF2

[10] National Institute of Standards and Technology, *The NIST Cybersecurity Framework
(CSF) 2.0*, NIST CSWP 29, Feb. 2024. doi: 10.6028/NIST.CSWP.29.

- Landing page: <https://csrc.nist.gov/pubs/cswp/29/the-nist-cybersecurity-framework-20/final>
- **Caution:** SP 800-82r3 §6 maps to **CSF 1.1** function/category identifiers
  (ID.AM, PR.AC, DE.CM, RS.MI, RC.RP, …), not CSF 2.0.  CSF 2.0 adds the **GOVERN (GV)**
  function and renumbers several categories.  Do not silently substitute one for the other.
  The CSF 1.1 identifiers used in `references/ot-ics-62443.md` are VERIFIED — local copy
  (SP 800-82r3 TOC §6.1–6.5).

### REF-NIST-SSDF

[11] M. Souppaya, K. Scarfone, and D. Dodson, *Secure Software Development Framework
(SSDF) Version 1.1: Recommendations for Mitigating the Risk of Software Vulnerabilities*,
National Institute of Standards and Technology, Gaithersburg, MD, NIST SP 800-218,
Feb. 2022. doi: 10.6028/NIST.SP.800-218.

- Landing page: <https://csrc.nist.gov/pubs/sp/800/218/final>
- **Practice groups applied:** PO (Prepare the Organization), PS (Protect the Software),
  PW (Produce Well-Secured Software), RV (Respond to Vulnerabilities).
- **Status:** VERIFIED — public (practice-group designators are stable and widely
  published).  Individual task numbers (e.g., PW.4.1): REQUIRES VERIFICATION.

### REF-NIST-FIPS-140-3

[12] National Institute of Standards and Technology, *Security Requirements for
Cryptographic Modules*, FIPS PUB 140-3, Mar. 2019. doi: 10.6028/NIST.FIPS.140-3.

- Landing page: <https://csrc.nist.gov/pubs/fips/140-3/final>
- Validated module search (CMVP): <https://csrc.nist.gov/projects/cryptographic-module-validation-program/validated-modules>
- **Status:** VERIFIED — public.

### REF-NIST-FIPS-186-5

[13] National Institute of Standards and Technology, *Digital Signature Standard (DSS)*,
FIPS PUB 186-5, Feb. 2023. doi: 10.6028/NIST.FIPS.186-5.

- Landing page: <https://csrc.nist.gov/pubs/fips/186-5/final>
- **Status:** VERIFIED — public.

### REF-NIST-FIPS-203

[14] National Institute of Standards and Technology, *Module-Lattice-Based Key-Encapsulation
Mechanism Standard*, FIPS PUB 203, Aug. 2024. doi: 10.6028/NIST.FIPS.203.

- Landing page: <https://csrc.nist.gov/pubs/fips/203/final>
- **Status:** VERIFIED — public.  Cited only for the crypto-agility control (SCA-DP-07);
  no claim is made here that any specific controller must implement ML-KEM today.

### REF-NIST-FIPS-204

[15] National Institute of Standards and Technology, *Module-Lattice-Based Digital
Signature Standard*, FIPS PUB 204, Aug. 2024. doi: 10.6028/NIST.FIPS.204.

- Landing page: <https://csrc.nist.gov/pubs/fips/204/final>
- **Status:** VERIFIED — public.  Relevant to long-lived secure-boot signing keys
  (see SCA-DS-02 crypto-agility note).

### REF-NIST-800-193

[16] A. Regenscheid, *Platform Firmware Resiliency Guidelines*, National Institute of
Standards and Technology, Gaithersburg, MD, NIST SP 800-193, May 2018.
doi: 10.6028/NIST.SP.800-193.

- Landing page: <https://csrc.nist.gov/pubs/sp/800/193/final>
- **Principles applied:** firmware **protection**, **detection**, and **recovery**; roots of
  trust and chains of trust for update, detection, and recovery.
- **Status:** VERIFIED — public (the three resiliency principles are the document's
  defining structure).  Clause-level requirements: REQUIRES VERIFICATION.

### REF-NIST-8228

[17] K. Boeckl, M. Fagan, W. Fisher, N. Lefkovitz, K. N. Megas, E. Nadeau, D. G. O'Rourke,
B. Piccarreta, and K. Scarfone, *Considerations for Managing Internet of Things (IoT)
Cybersecurity and Privacy Risks*, National Institute of Standards and Technology,
Gaithersburg, MD, NISTIR 8228, Jun. 2019. doi: 10.6028/NIST.IR.8228.

- Landing page: <https://csrc.nist.gov/pubs/ir/8228/final>
- **Relationship:** SP 800-213 §1 (footnote 3) cites IR 8228 and IR 8259 as the source of
  the IoT device definition used across the series.  That relationship is VERIFIED —
  local copy (SP 800-213, p. 1, fn. 3).

---

## Industrial control standards (paywalled — designations verified, clauses not)

### REF-ISA-62443-4-1

[18] International Society of Automation / International Electrotechnical Commission,
*Security for industrial automation and control systems — Part 4-1: Secure product
development lifecycle requirements*, ISA/IEC 62443-4-1.

- Official series page: <https://www.isa.org/standards-and-publications/isa-standards/isa-iec-62443-series-of-standards>
- IEC catalogue: <https://webstore.iec.ch/publication/33615>
- **Practices applied (eight):** SM — Security Management; SR — Specification of Security
  Requirements; SD — Secure by Design; SI — Secure Implementation; SVV — Security
  Verification and Validation Testing; DM — Management of Security-Related Issues;
  SUM — Security Update Management; SG — Security Guidelines.
- **Status:** Designation, title, and the eight practice designators: VERIFIED — public
  (these are published in the standard's abstract and in ISASecure SDLA program material).
  **All individual requirement numbers (e.g., SD-4, SVV-3): REQUIRES VERIFICATION** against
  a purchased copy before use in a design record.

### REF-ISA-62443-4-2

[19] International Society of Automation / International Electrotechnical Commission,
*Security for industrial automation and control systems — Part 4-2: Technical security
requirements for IACS components*, ISA/IEC 62443-4-2.

- Official series page: <https://www.isa.org/standards-and-publications/isa-standards/isa-iec-62443-series-of-standards>
- IEC catalogue: <https://webstore.iec.ch/publication/34421>
- **Foundational Requirements (seven), applied throughout:** FR 1 — Identification and
  Authentication Control (IAC); FR 2 — Use Control (UC); FR 3 — System Integrity (SI);
  FR 4 — Data Confidentiality (DC); FR 5 — Restricted Data Flow (RDF); FR 6 — Timely
  Response to Events (TRE); FR 7 — Resource Availability (RA).
- **Component types applied:** EDR (embedded device requirements); HDR (host device
  requirements); NDR (network device requirements); SAR (software application
  requirements).  A microcontroller-based servo, ESC, or flight-control node is normally
  assessed as an **EDR**.
- **Status:** Designation, title, the seven FRs, and the four component-type designators:
  VERIFIED — public.  **Individual CR/EDR requirement numbers: REQUIRES VERIFICATION.**

### REF-ISA-62443-3-3

[20] International Society of Automation / International Electrotechnical Commission,
*Security for industrial automation and control systems — Part 3-3: System security
requirements and security levels*, ISA/IEC 62443-3-3.

- Official series page: <https://www.isa.org/standards-and-publications/isa-standards/isa-iec-62443-series-of-standards>
- IEC catalogue: <https://webstore.iec.ch/publication/7033>
- **Concepts applied:** zones and conduits; Security Levels SL 0 through SL 4, defined by
  the capability of the threat actor the system is expected to resist (SL 1 casual or
  coincidental violation → SL 4 sophisticated means, extended resources, IACS-specific
  skills, high motivation).  Target SL (SL-T), Achieved SL (SL-A), Capability SL (SL-C).
- **Status:** Designation, title, and the SL 0–4 / SL-T / SL-A / SL-C scheme: VERIFIED —
  public.  **Individual SR numbers: REQUIRES VERIFICATION.**

### REF-ISA-TR84-00-09

[21] International Society of Automation, *Cybersecurity Related to the Functional Safety
Lifecycle*, ISA-TR84.00.09.

- Publisher page: <https://www.isa.org/standards-and-publications/isa-standards>
- **Relevance:** the safety–security interaction requirement (SCA-SL-01).  SP 800-82r3
  App. D.1.5.4 lists this technical report by designation and title.
- **Status:** Designation and title: VERIFIED — local copy (SP 800-82r3 TOC, D.1.5.4).
  Content: REQUIRES VERIFICATION.

### REF-IEC-61508

[22] International Electrotechnical Commission, *Functional safety of
electrical/electronic/programmable electronic safety-related systems*, IEC 61508 (all parts).

- IEC catalogue: <https://webstore.iec.ch/publication/5515>
- **Concepts applied:** Safety Integrity Levels SIL 1–4; the safety lifecycle.
- **Status:** Designation, title, and the SIL 1–4 scheme: VERIFIED — public.
  Clause numbers: REQUIRES VERIFICATION.

---

## Vehicle, aviation, and UAS sources

### REF-ISO-SAE-21434

[23] International Organization for Standardization and SAE International, *Road vehicles —
Cybersecurity engineering*, ISO/SAE 21434:2021.

- ISO catalogue: <https://www.iso.org/standard/70918.html>
- **Concepts applied:** TARA (Threat Analysis and Risk Assessment); cybersecurity
  case; cybersecurity interface agreement; the concept → product development →
  post-development (production, operations and maintenance, end of support) lifecycle.
- **Status:** Designation, title, year, and the TARA / cybersecurity-case concepts:
  VERIFIED — public.  Clause numbers: REQUIRES VERIFICATION.
- **Applicability caution:** ISO/SAE 21434 is a *road vehicle* standard.  It is cited here
  as an analogous, mature methodology for an electric propulsion/actuation controller —
  **not** as a binding requirement for an unmanned aircraft.  Do not claim 21434 compliance
  for a UAS controller.

### REF-UNECE-R155

[24] United Nations Economic Commission for Europe, *UN Regulation No. 155 — Uniform
provisions concerning the approval of vehicles with regards to cyber security and cyber
security management system*.

- UNECE page: <https://unece.org/transport/documents/2021/03/standards/un-regulation-no-155-cyber-security-and-cyber-security>
- **Status:** VERIFIED — public.
- **Applicability caution:** United Nations vehicle-type-approval instrument; **not**
  applicable in United States jurisdiction and **not** applicable to unmanned aircraft.
  Retained only as a reference model for a Cyber Security Management System (CSMS).

### REF-UNECE-R156

[25] United Nations Economic Commission for Europe, *UN Regulation No. 156 — Uniform
provisions concerning the approval of vehicles with regards to software update and software
update management system*.

- UNECE page: <https://unece.org/transport/documents/2021/03/standards/un-regulation-no-156-software-update-and-software-update>
- **Status:** VERIFIED — public.  Same applicability caution as REF-UNECE-R155.

### REF-RTCA-DO-326A

[26] RTCA, Inc., *Airworthiness Security Process Specification*, RTCA DO-326A
(EUROCAE ED-202A).

- RTCA store: <https://my.rtca.org/productdetails?id=a1B36000001IcmqEAC>
- **Concepts applied:** the airworthiness security process; security risk assessment
  integrated with the safety assessment process.
- **Status:** Designation, title, and ED-202A equivalence: VERIFIED — public.
  Clause content: REQUIRES VERIFICATION.
- **Applicability caution:** DO-326A applies to **type-certificated** aircraft.  A small
  unmanned aircraft operated under 14 CFR Part 107 is **not** type-certificated and DO-326A
  does not bind it.  Cited as best practice for airborne security risk assessment.

### REF-RTCA-DO-356A

[27] RTCA, Inc., *Airworthiness Security Methods and Considerations*, RTCA DO-356A
(EUROCAE ED-203A).

- RTCA store: <https://my.rtca.org/productdetails?id=a1B36000001IcmrEAC>
- **Status:** Designation and title: VERIFIED — public.  Content: REQUIRES VERIFICATION.
  Same applicability caution as REF-RTCA-DO-326A.

### REF-14CFR-107

[28] *Small Unmanned Aircraft Systems*, 14 C.F.R. pt. 107.

- eCFR: <https://www.ecfr.gov/current/title-14/chapter-I/subchapter-F/part-107>
- **Status:** VERIFIED — public.  United States jurisdiction.

### REF-14CFR-89

[29] *Remote Identification of Unmanned Aircraft*, 14 C.F.R. pt. 89.

- eCFR: <https://www.ecfr.gov/current/title-14/chapter-I/subchapter-F/part-89>
- **Sections applied:** the Remote ID message-element and broadcast obligations, which
  create a **deliberate, mandated broadcast of aircraft identity and position**.  This is a
  privacy/OPSEC input to the threat model, not a defect (see SCA-SL-04).
- **Status:** VERIFIED — public.  United States jurisdiction.
  Specific paragraph numbers: REQUIRES VERIFICATION before quotation.

### REF-ASTM-F3411

[30] ASTM International, *Standard Specification for Remote ID and Tracking*,
ASTM F3411.

- ASTM catalogue: <https://www.astm.org/f3411-22a.html>
- **Status:** Designation and title: VERIFIED — public.  Revision letter and clause
  content: REQUIRES VERIFICATION (ASTM revises this specification frequently — confirm the
  revision accepted by the FAA means-of-compliance list before citing a revision).

---

## Supply chain and disclosure sources

### REF-CISA-SBOM

[31] Cybersecurity and Infrastructure Security Agency, *Software Bill of Materials (SBOM)*.

- URL: <https://www.cisa.gov/sbom>
- **Status:** VERIFIED — public.

### REF-NTIA-SBOM-MIN

[32] National Telecommunications and Information Administration, *The Minimum Elements For
a Software Bill of Materials (SBOM)*, Jul. 2021.

- URL: <https://www.ntia.gov/report/2021/minimum-elements-software-bill-materials-sbom>
- **Minimum data fields applied:** supplier name; component name; version of the component;
  other unique identifiers; dependency relationship; author of SBOM data; timestamp.
- **Status:** VERIFIED — public.

### REF-ISO-29147

[33] International Organization for Standardization / International Electrotechnical
Commission, *Information technology — Security techniques — Vulnerability disclosure*,
ISO/IEC 29147.

- ISO catalogue: <https://www.iso.org/standard/72311.html>
- **Status:** Designation and title: VERIFIED — public.  Clause content: REQUIRES
  VERIFICATION.

### REF-ISO-30111

[34] International Organization for Standardization / International Electrotechnical
Commission, *Information technology — Security techniques — Vulnerability handling
processes*, ISO/IEC 30111.

- ISO catalogue: <https://www.iso.org/standard/69725.html>
- **Status:** Designation and title: VERIFIED — public.  Clause content: REQUIRES
  VERIFICATION.

---

## Ground, marine, and machinery overlays

### REF-ISO-26262

[35] International Organization for Standardization, *Road vehicles — Functional safety*,
ISO 26262 (all parts), 2018.

- ISO catalogue: <https://www.iso.org/standard/68383.html>
- **Concepts applied:** Automotive Safety Integrity Levels ASIL A–D; the hazard analysis and
  risk assessment (HARA) process.
- **Status:** Designation, title, and the ASIL A–D scheme: VERIFIED — public.  Clause
  numbers: REQUIRES VERIFICATION.  Applies to **road** vehicles; not to UAS, USV, or
  fixed industrial machinery.

### REF-ISO-13849

[36] International Organization for Standardization, *Safety of machinery — Safety-related
parts of control systems — Part 1: General principles for design*, ISO 13849-1.

- ISO catalogue: <https://www.iso.org/standard/73481.html>
- **Concepts applied:** Performance Levels PL a–e; categories B, 1–4.
- **Status:** Designation, title, and the PL a–e scheme: VERIFIED — public.  Clause content
  and the current edition year: REQUIRES VERIFICATION.

### REF-IEC-62061

[37] International Electrotechnical Commission, *Safety of machinery — Functional safety of
safety-related control systems*, IEC 62061.

- IEC catalogue: <https://webstore.iec.ch/publication/59927>
- **Concepts applied:** SIL for machinery control systems; the machinery-sector counterpart
  to IEC 61508.
- **Status:** Designation and title: VERIFIED — public.  Edition and clause content:
  REQUIRES VERIFICATION.

### REF-ISO-10218

[38] International Organization for Standardization, *Robotics — Safety requirements for
industrial robots*, ISO 10218-1 (robots) and ISO 10218-2 (robot systems and integration).

- ISO catalogue: <https://www.iso.org/standard/73933.html>
- **Status:** Designations and titles: VERIFIED — public.  Edition year and clause content:
  REQUIRES VERIFICATION (this standard was revised recently — confirm the current edition
  and the corresponding ANSI adoption before citing).

### REF-ISO-TS-15066

[39] International Organization for Standardization, *Robots and robotic devices —
Collaborative robots*, ISO/TS 15066:2016.

- ISO catalogue: <https://www.iso.org/standard/62996.html>
- **Relevance:** force and pressure limits for collaborative operation.  Where firmware can
  alter those limits, firmware compromise becomes a physical-harm path — see Overlay F in
  `platform-overlays.md`.
- **Status:** Designation, title, and year: VERIFIED — public.  Limit values: REQUIRES
  VERIFICATION.

### REF-ANSI-RIA-R1506

[40] American National Standards Institute / Association for Advancing Automation,
*Industrial Robots and Robot Systems — Safety Requirements*, ANSI/RIA R15.06.

- Publisher: <https://www.automate.org/robotics/standards>
- **Relevance:** the US national adoption of ISO 10218; the operative robot-safety standard
  in United States jurisdiction.
- **Status:** Designation, title, and the ISO 10218 adoption relationship: VERIFIED —
  public.  Current revision year and clause content: REQUIRES VERIFICATION.

### REF-ISO-3691-4

[41] International Organization for Standardization, *Industrial trucks — Safety
requirements and verification — Part 4: Driverless industrial trucks and their systems*,
ISO 3691-4.

- ISO catalogue: <https://www.iso.org/standard/70660.html>
- **Relevance:** AGV / AMR safety in Overlay G.
- **Status:** Designation and title: VERIFIED — public.  Edition and clauses: REQUIRES
  VERIFICATION.

### REF-ANSI-B565

[42] ANSI / Industrial Truck Standards Development Foundation, *Safety Standard for
Driverless, Automatic Guided Industrial Vehicles and Automated Functions of Manned
Industrial Vehicles*, ANSI/ITSDF B56.5.

- Publisher: <https://www.itsdf.org/>
- **Relevance:** the US counterpart to ISO 3691-4 for AGVs.
- **Status:** Designation, title, and issuing body: VERIFIED — public.  Revision year and
  clause content: REQUIRES VERIFICATION.

### REF-ISO-25119

[43] International Organization for Standardization, *Tractors and machinery for agriculture
and forestry — Safety-related parts of control systems*, ISO 25119 (all parts).

- ISO catalogue: <https://www.iso.org/standard/69026.html>
- **Concepts applied:** Agricultural Performance Levels (AgPL) for off-road machinery.
- **Status:** Designation and title: VERIFIED — public.  Edition and clauses: REQUIRES
  VERIFICATION.

### REF-USCG-CYBER

[44] United States Coast Guard, cybersecurity requirements for MTSA-regulated vessels and
facilities, 33 C.F.R. subchapter H.

- eCFR title 33: <https://www.ecfr.gov/current/title-33>
- USCG Office of Port and Facility Compliance: <https://www.dco.uscg.mil/>
- **Status: REQUIRES VERIFICATION — do not cite a section number from this entry.**  The
  USCG has issued both guidance (NVIC series) and rulemaking affecting maritime cyber risk
  management, and the compliance dates and CFR citations have moved.  Confirm the current
  part, section, and applicability at eCFR before using this in a design record.
- **Applicability:** MTSA-regulated vessels and facilities only.  A small privately operated
  USV is normally **not** in scope — do not assert a requirement that does not exist.

### REF-IMO-MSC-428

[45] International Maritime Organization, *Maritime Cyber Risk Management in Safety
Management Systems*, Resolution MSC.428(98); and *Guidelines on Maritime Cyber Risk
Management*, MSC-FAL.1/Circ.3 (as revised).

- IMO maritime cyber risk page: <https://www.imo.org/en/OurWork/Security/Pages/Cyber-security.aspx>
- **Status:** Designations and titles: VERIFIED — public.  Current circular revision:
  REQUIRES VERIFICATION.
- **Applicability:** SOLAS vessels' safety management systems.  Cited as a reference model
  for small USV work, not as a binding requirement.

---

## Carrier and SBC add-on board specifications

### REF-RPI-HAT

[46] Raspberry Pi Ltd., *HAT (Hardware Attached on Top) and HAT+ specifications*.

- Specification repository: <https://github.com/raspberrypi/hats>
- Documentation: <https://www.raspberrypi.com/documentation/computers/raspberry-pi.html>
- **Elements applied:** the requirement for an ID EEPROM on the dedicated ID_SD / ID_SC pins
  (header pins 27 and 28); EEPROM *atom* structure including vendor-info, GPIO map, and
  device tree blob atoms; the write-protect provision.
- **Status:** Existence of the ID EEPROM requirement, the ID_SD/ID_SC pin assignment, and
  the atom-based structure: VERIFIED — public and long-standing.  **Byte-level atom layouts,
  field offsets, and HAT+ additions: REQUIRES VERIFICATION** against the current
  specification revision in the repository above before writing tooling.

### REF-BB-CAPE

[47] BeagleBoard.org Foundation, *BeagleBone cape specification and System Reference
Manual* (cape EEPROM contents and expansion header definition).

- Documentation: <https://docs.beagleboard.org/>
- System Reference Manual: <https://github.com/beagleboard/beaglebone-black/wiki/System-Reference-Manual>
- **Elements applied:** cape EEPROM on I2C2 at addresses 0x54–0x57 (one per stacking
  position, up to four capes); EEPROM contents including board name, version, manufacturer,
  part number, serial number, pin usage, and declared current draw per supply rail.
- **Status:** The I2C2 bus, the 0x54–0x57 address range, four-cape stacking, and the
  presence of a current-draw declaration: VERIFIED — public and long-standing.
  **Field-level EEPROM layout and offsets: REQUIRES VERIFICATION** against the current
  System Reference Manual revision.

---

## Removed / superseded citations

| Designation | Reason | Replaced by |
| --- | --- | --- |
| NIST IR 8259 (May 2020) | Superseded Apr. 2026 per IR 8259r1 publication history | REF-NIST-8259R1 |
| NIST SP 800-82r2 | Superseded Sep. 2023 | REF-NIST-800-82R3 |
| "NIST 800-82 ICS Overlay" (informal name) | Not a real designation; the OT Overlay is App. F of SP 800-82r3 | REF-NIST-800-82R3, App. F |
| "IEC 62443-4-2 CR-x.y" quoted verbatim | No local copy; quoting would fabricate clause text | REF-ISA-62443-4-2 at FR level only |

---

## Rules for adding a citation to this catalog

1. Look up the standard here by REF-ID first.  If it is absent, add it **before** using it
   in a control or a design record.
2. A new entry needs: designation, full title, issuing body, date/revision, a validated URL
   on the issuing body's own site, the specific sections applied, and a verification status.
3. If a section number cannot be verified against a document in hand, mark the entry
   **REQUIRES VERIFICATION** and open a TODO item.  Never guess a clause number.
4. When a citation is dropped or superseded, move it to *Removed / Superseded Citations*
   with the reason — do not delete it silently.
