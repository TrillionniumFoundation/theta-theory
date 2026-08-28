# CM2 Round 87 — rank-three port event continuation

Date: 2026-07-22

## Outcome

All `3,212` non-source algebraic discriminant roots in the frozen Round-85 registered box unions have a certified, positive-width local continuation across the exposed union boundary.  Exactly `945` of those port neighborhoods belong to the locally physical next-tangency locus, and none of those `945` is a physical endpoint.  The other `2,267` are not locally physical third-tangency points.

This is a local continuation theorem, not a global port pairing.  It does not identify `1,606` gaps and does not promote the `2,108` registered elementary arcs to complete physical faces.

## Exact construction

For every Round-85 port, the producer:

1. bisects the third-candidate discriminant equation

   `candidate_radius^2 - signed_transverse^2 = 0`

   for 128 exact dyadic steps on the exposed segment;
2. constructs a positive-width slab on the outward side of the registered union boundary;
3. proves uniform opposite signs on the two parameter faces and strict nonzero derivatives in both source coordinates, hence a unique algebraic implicit root graph crosses the boundary;
4. uses the pinned Gate-25 physical-core theorem for the first collision, then replays the second collision and certifies the same second owner and outgoing chart throughout the slab;
5. uses the oriented-line projective chart `q = u_y/(1+u_x)`, with `1+u_x > 0`, and preserves the frozen transverse-sign ledger;
6. evaluates the complete translated third-candidate table and strictly orders every future near root against the nominated tangent flight.

The required outward dyadic normal depth lies between 127 and 142.  Every slab stays strictly inside its source C24 core, with a uniform rational coordinate margin greater than `1/100000`.

## Local physical-event partition

| Local type at the registered port | Count |
|---|---:|
| Physical next tangency, locally continuing | 945 |
| Algebraic tangency strictly behind the second collision | 980 |
| Algebraic tangency beyond `tau_max = 3` | 432 |
| Algebraic tangency occluded by an earlier strict third owner | 855 |
| Unresolved | 0 |
| Physical endpoints among the 945 locally physical next-tangency ports | 0 |

Thus `945` ports lie on locally physical rank-transition tangencies.  The other `2,267` ports are locally continuing algebraic discriminant roots but are not physical third-collision tangencies at those source points.

The old Round-85 outward-cell classes are both resolved by the local slabs:

| Round-85 outward class | Local type | Count |
|---|---|---:|
| no unresolved seed registered | physical next tangency | 677 |
| no unresolved seed registered | behind second collision | 972 |
| no unresolved seed registered | beyond `tau_max` | 432 |
| no unresolved seed registered | occluded | 615 |
| second-chart/geometry blocker only | physical next tangency | 268 |
| second-chart/geometry blocker only | behind second collision | 8 |
| second-chart/geometry blocker only | occluded | 240 |

This reproduces the frozen input partition `3,212 = 2,696 + 516` and resolves the earlier whole-cell blockers without relabelling algebraic roots as physical points or endpoints.

## Complete competitor ledger

The certificate evaluates `86,315` non-target candidate event equations:

| Candidate-root classification | Count |
|---|---:|
| no real intersection | 81,417 |
| intersection strictly behind | 1,481 |
| strict future near root | 3,417 |

The `3,417` strict future roots split into `1,908` before and `1,509` after the nominated tangent flight.  All order, chart, transverse, root-derivative, source-margin and `tau_max` comparisons are strict; no equality branch remains indeterminate.

The frozen transverse-factor partition remains exactly `1,606` negative and `1,606` positive.  This equality is only a sign ledger and is not a port pairing.

## Verification

The producer runs at 512-bit Arb precision.  The verifier independently repeats all `3,212` root isolations, outward implicit-graph tests, two-collision replays and `86,315` competitor equations at 768 bits.

- independent audit: `PASS`
- executable CM2 source pins verified: `15/15`
- Gate-25 physical-core theorem manifest pin verified
- hostile semantic mutations rejected: `6/6`
- upstream/source pin mutations rejected: `20/20`
- strict-JSON attacks rejected: `4/4`
- producer cold replay: byte-for-byte identical
- verifier cold replay: byte-for-byte identical
- Python compilation: passed

## Frozen files and SHA-256

- `cm2_round87_rank3_port_event_continuation_cert.py`: `71f10cde22ea191c7710090e2e7474fdbc2925ded94fe60071159b2c262dc834`
- `cm2-round87-rank3-port-event-continuation-2026-07-22.json`: `f63f5d627def35f87dd3dfac075f8ecc0e8a5adfa725ddbe0eb692a39b54393b`
- `cm2_round87_rank3_port_event_continuation_verifier.py`: `fea97dec6f10d378b67664863c4fbb18d6fb4c6dd8b83b55734db50627b1692c`
- `cm2-round87-rank3-port-event-continuation-audit-2026-07-22.json`: `3dec9c052a0163feb5ac5a239b5dabd61d40c8e69e9fc13d4c895ff757d356b2`

## Remaining frontier

The next global step is to continue the `945` locally physical tangent branches and the relevant chart/translation seams until each reaches another certified local arc or an exact typed event.  Only after that global quotient has no unmatched physical port can a final physical-face count be computed.  The values `1,672`, `2,108`, and `1,606` remain unavailable as complete physical-face counts.
