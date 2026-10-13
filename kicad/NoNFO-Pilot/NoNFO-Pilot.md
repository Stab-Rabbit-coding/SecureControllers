# NoNFO-Pilot — Single-Node Flight, Comms and Payload Board Family

**Owner / engineer of record:** Steve Griffing (GitHub `Stab-Rabbit-coding`)
**Drafted by:** Claude Opus 5.5 (`claude-opus-5-5`), 2026-10-12
**License:** CC BY-SA 4.0 (documentation)
**Stage:** requirements and ideation only. No schematic, PCB or generator exists yet.

## Purpose

NoNFO-Pilot merges the Serenity-UAV Pilot cape (flight control and sensors) and TACCO cape (comms, logging and payload) into one board, so that one node carries the capability of a whole Serenity avionics stack. The name drops the "NFO" (naval flight officer) seat that TACCO represented: one crew position instead of two.

It is a SecureControllers fleet product. Serenity-UAV is its first customer and sets its qualification bar.

## Variants

| Variant | Host SBC | Outline | Status | Source document |
| --- | --- | --- | --- | --- |
| NoNFO-Pilot (BBE) | SanCloud BeagleBone Enhanced Industrial WiFi [REF-NFP-001] | 3.402 x 2.098 in (86.4 x 53.3 mm), BeagleBone cape | Requirements-only plan | `docs/plans/2026-10-12-001-feat-nonfo-pilot-bbe-plan.md` |
| NoNFO-Pilot-PB2 | PocketBeagle 2 Industrial (AM6254) [REF-NFP-004], [REF-NFP-005] | Same outline, mounts and harness positions as the BBE variant | Ranked ideation; not yet brainstormed | `docs/ideation/2026-10-12-nonfo-pilot-pb2-ideation.html` |

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
