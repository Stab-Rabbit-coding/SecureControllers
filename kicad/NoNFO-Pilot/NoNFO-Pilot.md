# NoNFO-Pilot — Single-Node Flight, Comms and Payload Board Family

**Owner / engineer of record:** Steve Griffing (GitHub `Stab-Rabbit-coding`)
**Drafted by:** Claude Opus 5.5 (`claude-opus-5-5`), 2026-10-12
**License:** CC BY-SA 4.0 (documentation)
**Stage:** PB2 variant planned (2026-11-14): pin ledger and architecture brief exist; no schematic, PCB or generator yet. BBE variant: requirements only.

## Purpose

NoNFO-Pilot merges the Serenity-UAV Pilot cape (flight control and sensors) and TACCO cape (comms, logging and payload) into one board, so that one node carries the capability of a whole Serenity avionics stack. The name drops the "NFO" (naval flight officer) seat that TACCO represented: one crew position instead of two.

It is a SecureControllers fleet product. Serenity-UAV is its first customer and sets its qualification bar.

## Variants

| Variant | Host SBC | Outline | Status | Source document |
| --- | --- | --- | --- | --- |
| NoNFO-Pilot (BBE) | SanCloud BeagleBone Enhanced Industrial WiFi [REF-NFP-001] | 3.402 x 2.098 in (86.4 x 53.3 mm), BeagleBone cape | Requirements-only plan | `docs/plans/2026-10-12-001-feat-nonfo-pilot-bbe-plan.md` |
| NoNFO-Pilot-PB2 | PocketBeagle 2 Industrial (AM6254) [REF-NFP-004], [REF-NFP-005] | Same outline, mounts and harness positions as the BBE variant | Sprint plan S34–S41; owner decision OD-18 (architecture) open | `PB2/ARCHITECTURE_BRIEF.md`, `PB2/pin_ledger/`; Serenity-UAV `docs/plans/2026-11-14-001-feat-nonfo-pilot-pb2-stern-stack-plan.md`; ideation `docs/ideation/2026-10-12-nonfo-pilot-pb2-ideation.html` |

## PB2 variant: decisions on record (owner, 2026-11-12)

- First use: the stern (Simon) control stack of Serenity-UAV. The other three Serenity stacks stay Pilot + TACCO pairs.
- Outline: the specification outline, 3.402 x 2.098 in (86.4 x 53.3 mm), with a fit gate at the Simon site before layout.
- Ethernet: the Pilot pattern, DP83825I on RMII2 plus the AX88772E USB NIC.
- GNSS: on-cape MAX-M10S, the first function removed if space, mass or routing is short.
- Architecture: open (OD-18). The pin ledger shows that only option B+ fits the PB2-I header with every function aboard.

## Open gates shared by both variants

- The GNSS source must be reconciled with the 2026-10-12 decision to move GNSS to isolated CAN-FD dorsal pucks (Serenity-UAV `avionics/WBS.md`).
- No 86.4 x 53.3 mm envelope exists yet in the Serenity airframe fit gates. The outline fits the cargo chin floor but not the aft strip.
- Every external source in `REFERENCES.md` marked **requires verification** has to be verified before a design file cites it.

## Work tracking

Tracked in `TODO.md` §5 (NoNFO-Pilot board family).

## References

1. [REF-NFP-001] SanCloud, "BeagleBone Enhanced (BBE)".
2. [REF-NFP-002] BBBMINI, GitHub user `mirkix`, CC BY-SA 4.0.
3. [REF-NFP-003] PocketPilot project, CC BY-SA 4.0.
4. [REF-NFP-004] BeagleBoard.org, PocketBeagle 2 documentation.
5. [REF-NFP-005] CNX Software, PocketBeagle 2 Industrial article, 2026-02-24.
6. [REF-NFP-006] Pixhawk Autopilot Bus, DS-010.

Full entries are in `../../REFERENCES.md`.
