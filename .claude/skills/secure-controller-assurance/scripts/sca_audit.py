#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Secure Controller Assurance — evidence scanner.

Walks a controller project (KiCad schematics, firmware sources, repository
artifacts) and reports **observable evidence** relevant to the SCA control
matrix.  It is an aid to an assessment, not the assessment itself.

Design principle
----------------
This tool never reports a control as *satisfied*.  Presence of a string in a
source file is evidence that something was attempted; it is not proof that the
control works.  Only a human review with negative-test evidence closes a
control.  Every finding is therefore emitted as one of:

    EVIDENCE_FOUND   -- an artifact consistent with the control exists
    CONCERN          -- an artifact inconsistent with the control exists
    NOT_DETERMINED   -- nothing observable either way

Authorship
----------
Authored by Claude (Opus 5) for Steve Griffing (@Stab-Rabbit-coding).
Derived from the control matrix in ``references/control-matrix.md``, which in
turn derives from the publications catalogued in ``references/REFERENCES.md``.

Usage
-----
    python3 sca_audit.py --project /path/to/repo --overlay A --sl-target 3
    python3 sca_audit.py --project . --output register.csv --json report.json

Exit codes
----------
    0  scan completed
    1  usage or I/O error
    2  scan completed and at least one CONCERN was raised
"""

from __future__ import annotations

import argparse
import csv
import json
import os
import re
import sys
from dataclasses import dataclass, field, asdict
from pathlib import Path
from typing import Iterable

# ---------------------------------------------------------------------------
# Constants
# ---------------------------------------------------------------------------

#: Findings vocabulary.  Deliberately excludes any "PASS" state -- see module
#: docstring.  A control is only closed by a human with negative-test evidence.
EVIDENCE_FOUND = "EVIDENCE_FOUND"
CONCERN = "CONCERN"
NOT_DETERMINED = "NOT_DETERMINED"

#: Platform overlays defined in references/platform-overlays.md.
OVERLAYS = {
    "A": "Air (UAS)",
    "G": "Ground (UGV, AGV/AMR, off-road, road)",
    "M": "Marine (USV, small boats)",
    "F": "Fixed industrial (robot cell, gantry)",
    "C": "Carrier / SBC add-on (Pi HAT, BeagleBone cape)",
}

#: File extensions worth reading, grouped by the kind of evidence they carry.
FIRMWARE_SUFFIXES = {
    ".c", ".h", ".cpp", ".hpp", ".cc", ".cxx", ".s", ".asm",
    ".py", ".rs", ".ino", ".ld",
}
SCHEMATIC_SUFFIXES = {".kicad_sch", ".kicad_pcb", ".kicad_pro", ".net"}
CONFIG_SUFFIXES = {".cfg", ".conf", ".ini", ".yaml", ".yml", ".toml", ".json", ".mk", ".cmake"}
DOC_SUFFIXES = {".md", ".rst", ".txt"}

#: Directories never worth walking.  Keeps the scan fast and avoids reporting
#: evidence that lives in a vendored dependency rather than in this design.
SKIP_DIRS = {
    ".git", ".svn", "node_modules", "__pycache__", ".venv", "venv",
    "build", "dist", ".mypy_cache", ".pytest_cache", ".tox",
    "fp-info-cache", "gerbers", "archive", "Archive",
}

#: Cap on file size read, in bytes.  Schematics and netlists can be large; a
#: multi-megabyte binary blob is never useful evidence and slows the scan.
MAX_FILE_BYTES = 8 * 1024 * 1024


# ---------------------------------------------------------------------------
# Data model
# ---------------------------------------------------------------------------

@dataclass
class Finding:
    """One observation about one control."""

    control_id: str
    verdict: str
    summary: str
    #: ``path:line`` locations supporting the observation, capped for readability.
    locations: list[str] = field(default_factory=list)
    #: What a human must do to turn this observation into a closed control.
    next_step: str = ""


@dataclass
class Probe:
    """A pattern-based evidence probe bound to a control.

    Attributes:
        control_id:   SCA control this probe informs.
        summary:      Human-readable description of what was sought.
        positive:     Regexes whose presence is evidence *for* the control.
        negative:     Regexes whose presence is a *concern* against it.
        suffixes:     File suffixes to search.  Empty means all text files.
        next_step:    What the assessor must verify by hand.
    """

    control_id: str
    summary: str
    positive: tuple[str, ...] = ()
    negative: tuple[str, ...] = ()
    suffixes: frozenset[str] = frozenset()
    next_step: str = ""


# ---------------------------------------------------------------------------
# Probe definitions
# ---------------------------------------------------------------------------
# Each probe maps to a control in references/control-matrix.md.  Patterns are
# intentionally broad: a false positive costs a moment of human review, while a
# false negative hides a real defect.  Case-insensitive matching throughout.

PROBES: tuple[Probe, ...] = (
    Probe(
        control_id="SCA-ID-02",
        summary="Hardware root of trust / secure element present in the design",
        positive=(
            r"\bATECC[0-9]{3}\w*", r"\bSLB96[0-9]{2}\w*", r"\bOPTIGA\b",
            r"\bSE050\b", r"\bATSHA204\w*", r"\bDS28[EC]\w*",
            r"\bTPM2?_", r"\bsecure[_\s-]?element\b",
        ),
        next_step="Confirm the part is on the BOM, is populated, and that a firmware "
                  "path actually uses it. A secure element no code touches is not a "
                  "capability.",
    ),
    Probe(
        control_id="SCA-ID-01",
        summary="Per-unit identity provisioning versus a hardcoded shared secret",
        positive=(r"\bprovision\w*", r"\bdevice[_\s-]?cert\w*", r"\bper[_\s-]?unit\b"),
        negative=(
            r"\b(?:default|shared|master)[_\s-]?(?:key|secret|password|passwd)\b",
            r"\bhardcoded[_\s-]?key\b",
        ),
        next_step="Verify identity is unique per unit and not derived from the MCU UID "
                  "alone (see nist-213a-catalog.md, DI/IMS).",
    ),
    Probe(
        control_id="SCA-CFG-01",
        summary="Default or embedded credentials in the shipped image",
        negative=(
            r"password\s*[=:]\s*[\"'][^\"']{1,64}[\"']",
            r"\bDEFAULT_(?:PASSWORD|PASSWD|KEY|SECRET|PIN)\b",
            r"\badmin\s*[:=]\s*[\"']admin[\"']",
            r"-----BEGIN (?:RSA |EC |OPENSSH )?PRIVATE KEY-----",
        ),
        next_step="Any private key or literal credential in the tree is a finding. "
                  "Confirm it is a test fixture and excluded from release builds.",
    ),
    Probe(
        control_id="SCA-SU-01",
        summary="Firmware signature verification before execution",
        positive=(
            r"\bverify[_\s-]?signature\b", r"\bsignature[_\s-]?verif\w*",
            r"\becdsa[_\s-]?verify\b", r"\bed25519[_\s-]?verify\b",
            r"\bmcuboot\b", r"\bimage[_\s-]?validate\b", r"\bsecure[_\s-]?boot\b",
        ),
        next_step="Confirm verification happens BEFORE control transfer, and that a "
                  "tampered image is actually refused on hardware (negative test).",
    ),
    Probe(
        control_id="SCA-DS-01",
        summary="Secure boot / chain of trust",
        positive=(
            r"\bsecure[_\s-]?boot\b", r"\bchain[_\s-]?of[_\s-]?trust\b",
            r"\broot[_\s-]?of[_\s-]?trust\b", r"\bRDP[_\s-]?LEVEL",
            r"\bboot[_\s-]?verif\w*",
        ),
        next_step="Verify each stage is measured/verified before transfer, and that "
                  "the root key is immutable (SCA-SU-02).",
    ),
    Probe(
        control_id="SCA-DP-04",
        summary="Flash readout protection configured in the production flow",
        positive=(
            r"\bRDP\b", r"\breadout[_\s-]?protect\w*", r"\bFLASH_OPTR\b",
            r"\bCRP[123]\b", r"\block[_\s-]?bits?\b", r"\bfuse[_\s-]?map\b",
        ),
        next_step="Confirm protection is enabled by the PRODUCTION programming script, "
                  "not just available on the part. Verify on a built unit.",
    ),
    Probe(
        control_id="SCA-IA-04",
        summary="Debug port lifecycle (SWD / JTAG / serial console)",
        positive=(r"\bdebug[_\s-]?(?:lock|disable|off)\b", r"\bRDP[_\s-]?LEVEL[_\s-]?[12]\b"),
        negative=(
            r"\bSWD\b", r"\bJTAG\b", r"\bTCK\b", r"\bTMS\b", r"\bTDI\b",
            r"\bdebug[_\s-]?header\b", r"\bICSP\b",
        ),
        next_step="THIS IS THE MOST FREQUENTLY FAILED CONTROL. Enumerate every debug "
                  "path in the schematic and state its production disposition. Attempt "
                  "a debug attach on a production-configured unit.",
    ),
    Probe(
        control_id="SCA-DP-01",
        summary="Cryptographic primitives in use, and weak/legacy algorithms",
        positive=(
            r"\bAES[_\s-]?(?:128|256|GCM|CCM|CMAC)\b", r"\bSHA-?256\b",
            r"\bChaCha20\b", r"\bPoly1305\b", r"\bHMAC\b", r"\bECDSA\b", r"\bEd25519\b",
        ),
        negative=(
            r"\bMD5\b", r"\bSHA-?1\b", r"\bDES\b", r"\bRC4\b",
            r"\bECB\b", r"\bTLS1[._]0\b", r"\bSSLv3\b",
        ),
        next_step="Weak primitives are a finding. Confirm the algorithm list is recorded "
                  "in the design record and benchmarked (SCA-DP-02).",
    ),
    Probe(
        control_id="SCA-DP-06",
        summary="Replay protection on authenticated channels",
        positive=(
            r"\bnonce\b", r"\breplay\b", r"\bmonotonic\b",
            r"\bfreshness\b", r"\bsequence[_\s-]?(?:number|counter)\b", r"\banti[_\s-]?replay\b",
        ),
        next_step="Verify a captured valid frame, replayed, is rejected.",
    ),
    Probe(
        control_id="SCA-CS-02",
        summary="Trustworthy time or sequence anchor for logs",
        positive=(r"\bRTC\b", r"\bmonotonic\b", r"\bboot[_\s-]?count\w*", r"\btime[_\s-]?sync\b"),
        negative=(r"\bHAL_GetTick\b", r"\bmillis\s*\(", r"\bxTaskGetTickCount\b"),
        next_step="A tick counter alone resets every power cycle and cannot order events "
                  "across boots. Confirm a monotonic anchor exists.",
    ),
    Probe(
        control_id="SCA-DS-03",
        summary="Resource bounding on inputs and buffers",
        positive=(
            r"\brate[_\s-]?limit\w*", r"\bwatchdog\b", r"\bIWDG\b", r"\bWWDG\b",
            r"\btimeout\b", r"\bmax[_\s-]?(?:queue|depth|retries)\b",
        ),
        negative=(r"\bstrcpy\s*\(", r"\bsprintf\s*\(", r"\bgets\s*\(", r"\bstrcat\s*\("),
        next_step="Unbounded string functions are memory-safety findings. Confirm bus "
                  "flood and malformed-frame storms cannot break the loop deadline.",
    ),
    Probe(
        control_id="SCA-SL-04",
        summary="Independent hardware limit below the firmware",
        positive=(
            r"\bcurrent[_\s-]?limit\b", r"\bOCP\b", r"\bover[_\s-]?current\b",
            r"\beFuse\b", r"\bcomparator\b", r"\bhardware[_\s-]?limit\b",
            r"\bDESAT\b", r"\bnFAULT\b",
        ),
        next_step="Confirm the limit is enforced in HARDWARE and survives a fully "
                  "compromised firmware. A firmware-checked limit is not this control.",
    ),
    Probe(
        control_id="SCA-SL-03",
        summary="Arm/enable versus stop/failsafe command separation",
        positive=(
            r"\bfailsafe\b", r"\be[_\s-]?stop\b", r"\bemergency[_\s-]?stop\b",
            r"\bdisarm\b", r"\barm(?:ed|ing)?[_\s-]?state\b",
        ),
        next_step="Verify the STOP path is unauthenticated and always available, while "
                  "the ARM/ENABLE path is authenticated.",
    ),
    Probe(
        control_id="SCA-HC-01",
        summary="Carrier ID EEPROM and its write-protect (Overlay C)",
        positive=(r"\bID_SD\b", r"\bID_SC\b", r"\bcape[_\s-]?eeprom\b", r"\bhat[_\s-]?eeprom\b",
                  r"\b24[Cc]w?32\b", r"\bWP\b"),
        next_step="Confirm the EEPROM write-protect pin is DRIVEN ACTIVE in production, "
                  "not left floating. Attempt a write on a production unit.",
    ),
    Probe(
        control_id="SCA-HC-02",
        summary="Device tree overlay delivery path (Overlay C)",
        positive=(r"\.dtbo\b", r"\bdevice[_\s-]?tree\b", r"\bdtoverlay\b", r"\bfdt\b"),
        next_step="An overlay loaded from a writable EEPROM is unsigned configuration "
                  "injected into the host kernel. Confirm delivery via the host's signed "
                  "package channel, or that the blob is integrity-protected.",
    ),
    Probe(
        control_id="SCA-OT-03",
        summary="Industrial / vehicle protocol stacks present",
        positive=(
            r"\bmodbus\b", r"\bDNP3\b", r"\bEtherNet/?IP\b", r"\bCANopen\b",
            r"\bJ1939\b", r"\bMAVLink\b", r"\bDroneCAN\b", r"\bUAVCAN\b",
            r"\bOPC[_\s-]?UA\b", r"\bBACnet\b", r"\bIEC[_\s-]?61850\b",
        ),
        next_step="Most of these protocols are unauthenticated by design. Confirm the "
                  "parser is hardened against malformed input and that authentication "
                  "is layered on where the conduit requires it.",
    ),
)

#: Repository-level artifacts expected by the non-technical control families.
REPO_ARTIFACTS: tuple[tuple[str, tuple[str, ...], str], ...] = (
    ("SCA-NT-03", ("SECURITY.md", ".github/SECURITY.md", "docs/SECURITY.md"),
     "Vulnerability disclosure contact and handling process (ISO 29147/30111)."),
    ("SCA-SC-01", ("sbom.json", "sbom.spdx.json", "sbom.cdx.json", "bom.json",
                   "SBOM.md", "sbom.xml"),
     "SBOM carrying the NTIA minimum elements."),
    ("SCA-GOV-04", ("THREAT_MODEL.md", "docs/THREAT_MODEL.md", "threat-model.md",
                    "docs/threat-model.md"),
     "Threat model naming adversary capability and attack paths."),
    ("SCA-GOV-05", ("REFERENCES.md",),
     "Repository citation catalog required by the project engineering standards."),
    ("SCA-NT-02", ("ASSURANCE_CASE.md", "docs/ASSURANCE_CASE.md",
                   "SECURITY_ASSURANCE_CASE.md"),
     "Security assurance case (see assets/assurance-case-template.md)."),
    ("SCA-NT-05", ("HARDENING.md", "docs/HARDENING.md", "INTEGRATION.md",
                   "docs/INTEGRATION.md"),
     "Hardening / deployment guide shipped to the integrator (62443-4-1 SG)."),
)


# ---------------------------------------------------------------------------
# Scanning
# ---------------------------------------------------------------------------

def iter_files(root: Path) -> Iterable[Path]:
    """Yield candidate files under *root*, skipping noise directories.

    Args:
        root: Project directory to walk.

    Yields:
        Paths to regular files worth reading.
    """
    for dirpath, dirnames, filenames in os.walk(root):
        # Prune in place so os.walk does not descend into skipped trees.
        dirnames[:] = [d for d in dirnames if d not in SKIP_DIRS and not d.startswith(".")]
        for name in filenames:
            path = Path(dirpath) / name
            suffix = path.suffix.lower()
            if suffix in (FIRMWARE_SUFFIXES | SCHEMATIC_SUFFIXES
                          | CONFIG_SUFFIXES | DOC_SUFFIXES):
                yield path


def read_text(path: Path) -> str:
    """Read *path* as text, tolerating encoding problems and oversized files.

    Returns an empty string when the file cannot be read or is too large; a
    file that cannot be read simply produces NOT_DETERMINED rather than an
    error, which matches this tool's fail-open-to-human-review posture.
    """
    try:
        if path.stat().st_size > MAX_FILE_BYTES:
            return ""
        return path.read_text(encoding="utf-8", errors="replace")
    except (OSError, ValueError):
        return ""


def scan_probe(probe: Probe, corpus: dict[Path, str], root: Path,
               max_locations: int = 8) -> Finding:
    """Evaluate one probe against the pre-read file corpus.

    A CONCERN outranks EVIDENCE_FOUND: if a probe finds both a good pattern and
    a bad one, the bad one is reported, because the concern is the thing that
    needs a human decision.

    Args:
        probe:         The probe to evaluate.
        corpus:        Mapping of path to file text.
        root:          Project root, used to shorten reported paths.
        max_locations: Cap on reported hit locations.

    Returns:
        A Finding for this probe's control.
    """
    # Hits are partitioned by whether they came from a *design artifact*
    # (firmware, schematic, build config) or from *prose* (Markdown, text).
    #
    # This distinction matters more than it looks.  A REFERENCES.md that cites
    # "FIPS 186-5 supersedes SHA-1 usage" or a TODO.md item reading "disable
    # SWD before release" will match a concern pattern, but neither is a defect
    # -- they are the project discussing the defect.  Raising a CONCERN from
    # prose produces exactly the kind of false finding that trains an engineer
    # to ignore the tool.  So: concerns come only from design artifacts; prose
    # matches are reported as discussion, which is weaker but still useful.
    design_pos: list[str] = []
    design_neg: list[str] = []
    prose_pos: list[str] = []
    prose_neg: list[str] = []

    pos_res = [re.compile(p, re.IGNORECASE) for p in probe.positive]
    neg_res = [re.compile(p, re.IGNORECASE) for p in probe.negative]

    for path, text in corpus.items():
        if probe.suffixes and path.suffix.lower() not in probe.suffixes:
            continue
        if not text:
            continue

        is_prose = path.suffix.lower() in DOC_SUFFIXES
        pos_bucket = prose_pos if is_prose else design_pos
        neg_bucket = prose_neg if is_prose else design_neg

        # Only split into lines when at least one pattern matches the whole
        # file; line-by-line matching over every file is needlessly slow.
        if any(r.search(text) for r in pos_res + neg_res):
            rel = path.relative_to(root)
            for lineno, line in enumerate(text.splitlines(), start=1):
                if len(neg_bucket) < max_locations:
                    for r in neg_res:
                        if r.search(line):
                            neg_bucket.append(f"{rel}:{lineno}")
                            break
                if len(pos_bucket) < max_locations:
                    for r in pos_res:
                        if r.search(line):
                            pos_bucket.append(f"{rel}:{lineno}")
                            break

    if design_neg:
        return Finding(
            control_id=probe.control_id,
            verdict=CONCERN,
            summary=f"{probe.summary} — pattern of concern in a design artifact",
            locations=design_neg[:max_locations],
            next_step=probe.next_step,
        )
    if design_pos:
        return Finding(
            control_id=probe.control_id,
            verdict=EVIDENCE_FOUND,
            summary=f"{probe.summary} — supporting artifact present",
            locations=design_pos[:max_locations],
            next_step=probe.next_step,
        )
    if prose_neg:
        return Finding(
            control_id=probe.control_id,
            verdict=NOT_DETERMINED,
            summary=(f"{probe.summary} — discussed in documentation only "
                     f"(no design artifact matched)"),
            locations=prose_neg[:max_locations],
            next_step="Documentation mentions this. Confirm whether it describes an "
                      "implemented control, an open item, or a superseded decision. "
                      + probe.next_step,
        )
    if prose_pos:
        return Finding(
            control_id=probe.control_id,
            verdict=NOT_DETERMINED,
            summary=f"{probe.summary} — documented but no design artifact matched",
            locations=prose_pos[:max_locations],
            next_step="Documentation claims this. Confirm it is implemented in firmware "
                      "or hardware, not only described. " + probe.next_step,
        )
    return Finding(
        control_id=probe.control_id,
        verdict=NOT_DETERMINED,
        summary=f"{probe.summary} — nothing observable found",
        next_step=probe.next_step or "Assess by hand; no filesystem evidence either way.",
    )


def scan_repo_artifacts(root: Path) -> list[Finding]:
    """Check for repository-level documentation artifacts.

    Args:
        root: Project directory.

    Returns:
        One Finding per expected artifact.
    """
    findings: list[Finding] = []
    for control_id, candidates, description in REPO_ARTIFACTS:
        found = [c for c in candidates if (root / c).is_file()]
        if found:
            findings.append(Finding(
                control_id=control_id,
                verdict=EVIDENCE_FOUND,
                summary=f"{description} — file present",
                locations=found,
                next_step="Confirm the file has real content and is current.",
            ))
        else:
            findings.append(Finding(
                control_id=control_id,
                verdict=NOT_DETERMINED,
                summary=f"{description} — no such file found",
                next_step=f"Expected one of: {', '.join(candidates)}",
            ))
    return findings


# ---------------------------------------------------------------------------
# Reporting
# ---------------------------------------------------------------------------

def print_report(findings: list[Finding], root: Path, overlay: str,
                 sl_target: int | None) -> None:
    """Write a human-readable report to stdout."""
    concerns = [f for f in findings if f.verdict == CONCERN]
    evidence = [f for f in findings if f.verdict == EVIDENCE_FOUND]
    unknown = [f for f in findings if f.verdict == NOT_DETERMINED]

    print("=" * 78)
    print("Secure Controller Assurance — Evidence Scan")
    print("=" * 78)
    print(f"Project      : {root}")
    print(f"Overlay      : {overlay} — {OVERLAYS.get(overlay, 'unspecified')}")
    print(f"SL-T         : {sl_target if sl_target is not None else 'not set'}")
    print(f"Findings     : {len(concerns)} concern(s), "
          f"{len(evidence)} with evidence, {len(unknown)} not determined")
    print()
    print("This tool reports OBSERVATIONS ONLY. It never marks a control satisfied.")
    print("Only human review with negative-test evidence closes a control.")
    print()

    for title, group in (("CONCERNS", concerns),
                         ("EVIDENCE FOUND", evidence),
                         ("NOT DETERMINED", unknown)):
        if not group:
            continue
        print("-" * 78)
        print(f"{title}  ({len(group)})")
        print("-" * 78)
        for f in group:
            print(f"[{f.control_id}] {f.summary}")
            for loc in f.locations:
                print(f"    at {loc}")
            if f.next_step:
                print(f"    NEXT: {f.next_step}")
            print()

    if sl_target is not None and sl_target >= 3:
        print("-" * 78)
        print("SL-T >= 3 reminder: a discrete hardware root of trust is normally")
        print("required at this level. Confirm SCA-ID-02 is met by a real part.")
        print()

    if overlay == "C":
        print("-" * 78)
        print("Overlay C reminder: the SCA-HC family applies. The host is a trust")
        print("domain you do not control, and Linux is not a safety controller.")
        print("See references/sbc-carrier-boards.md.")
        print()


def write_csv(findings: list[Finding], path: Path) -> None:
    """Write findings as CSV suitable for pasting into a control register."""
    with path.open("w", newline="", encoding="utf-8") as handle:
        writer = csv.writer(handle)
        writer.writerow(["control_id", "verdict", "summary", "locations", "next_step"])
        for f in findings:
            writer.writerow([
                f.control_id, f.verdict, f.summary,
                "; ".join(f.locations), f.next_step,
            ])


def write_json(findings: list[Finding], path: Path, root: Path,
               overlay: str, sl_target: int | None) -> None:
    """Write the full report as JSON for downstream tooling."""
    payload = {
        "project": str(root),
        "overlay": overlay,
        "overlay_name": OVERLAYS.get(overlay),
        "sl_target": sl_target,
        "disclaimer": (
            "Observations only. This tool never marks a control satisfied. "
            "Only human review with negative-test evidence closes a control."
        ),
        "findings": [asdict(f) for f in findings],
    }
    path.write_text(json.dumps(payload, indent=4), encoding="utf-8")


# ---------------------------------------------------------------------------
# Entry point
# ---------------------------------------------------------------------------

def main(argv: list[str] | None = None) -> int:
    """Parse arguments, run the scan, and emit the report."""
    parser = argparse.ArgumentParser(
        description="Scan a controller project for SCA control evidence.",
    )
    parser.add_argument("--project", required=True, type=Path,
                        help="Path to the project directory to scan.")
    parser.add_argument("--overlay", default="", choices=sorted(OVERLAYS) + [""],
                        help="Platform overlay: A air, G ground, M marine, "
                             "F fixed industrial, C carrier/SBC.")
    parser.add_argument("--sl-target", type=int, choices=(1, 2, 3, 4), default=None,
                        help="ISA/IEC 62443 target security level.")
    parser.add_argument("--output", type=Path, default=None,
                        help="Write findings to this CSV path.")
    parser.add_argument("--json", type=Path, default=None,
                        help="Write the full report to this JSON path.")
    args = parser.parse_args(argv)

    root = args.project.expanduser().resolve()
    if not root.is_dir():
        print(f"error: not a directory: {root}", file=sys.stderr)
        return 1

    # Read every candidate file once; probes then run against the in-memory
    # corpus rather than re-walking the tree per probe.
    corpus: dict[Path, str] = {}
    for path in iter_files(root):
        text = read_text(path)
        if text:
            corpus[path] = text

    if not corpus:
        print(f"error: no readable source files found under {root}", file=sys.stderr)
        return 1

    findings = [scan_probe(p, corpus, root) for p in PROBES]
    findings.extend(scan_repo_artifacts(root))
    findings.sort(key=lambda f: (
        {CONCERN: 0, EVIDENCE_FOUND: 1, NOT_DETERMINED: 2}[f.verdict],
        f.control_id,
    ))

    print_report(findings, root, args.overlay or "-", args.sl_target)

    try:
        if args.output:
            write_csv(findings, args.output)
            print(f"CSV written to {args.output}")
        if args.json:
            write_json(findings, args.json, root, args.overlay or "-", args.sl_target)
            print(f"JSON written to {args.json}")
    except OSError as exc:
        print(f"error: could not write output: {exc}", file=sys.stderr)
        return 1

    return 2 if any(f.verdict == CONCERN for f in findings) else 0


if __name__ == "__main__":
    sys.exit(main())
