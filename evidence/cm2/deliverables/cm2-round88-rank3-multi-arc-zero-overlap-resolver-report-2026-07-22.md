# CM2 Round 88 — multi-arc zero-overlap resolver

Date: 2026-07-22

## Outcome

All registered-side pairing ambiguity left by the Round-88 physical-port
component quotient is closed.  The `32` live multi-arc box-components contain
`1,020` exact registered boxes and `176` elementary zero-set pieces.  Every
piece has exactly two exposed registered ports and no port has ambiguous
piece incidence.

Together with the previously frozen `320` single-arc pairs, this installs an
exact registered-side endpoint pairing for all `496/496` live registered
arcs, using `992` distinct endpoints.

## Zero-overlap graph

For every pair of intersecting registered boxes in a live multi-arc
component, the certificate evaluates the physical third-tangency
discriminant on the exact rectangular intersection.  Both coordinate
derivatives are strictly nonzero.  Strict corner signs then decide whether
the overlap contains a zero:

- overlapping-box pair tests: `1,524`;
- zero-connecting overlaps: `844`;
- strict zero-excluding overlaps: `680`;
- unresolved equality/critical overlaps: `0`.

The connected components of this strict zero-overlap graph reproduce the
expected elementary-arc count component by component.  All `176` graph
components receive exactly two and only two Round-85 registered ports.

## Complete live registered-side pairing

| Pair type | Count |
|---|---:|
| physical port to physical port | 449 |
| source-boundary port to physical port | 47 |
| total | 496 |

There are no source-to-source pairs in the live physical-open frontier.  The
separate `400` source-boundary-only components and the `1,212`
nonphysical-open registered arcs remain outside this live pairing ledger.

## Verification

The producer runs at 512-bit Arb precision.  The verifier independently
rebuilds all `1,524` overlap decisions and all port-to-piece incidences at
768 bits, using a separate centered-Taylor evaluation path for overlap
gradients.

- independent audit: `PASS`;
- resolved pieces: `176/176`;
- port degree histogram: `2:176`;
- ambiguous incidences: `0`;
- manifest, upstream and executable pins: `10/10`;
- hostile semantic mutations rejected: `6/6`;
- strict-JSON attacks rejected: `4/4`;
- producer/verifier cold replay: byte-for-byte identical;
- Python compilation: passed.

## Strict limits

This certificate pairs endpoints only through the exact frozen registered
box unions.  It does not pair any of the `945` physical ports along the
outward continuation, does not turn source-core boundary contacts into
physical endpoints, and does not compute complete physical faces.  No Gate 5
or RN row is promoted.

The remaining global topology problem is now purely the continuation of the
`945` outward physical tangent branches through owner, chart, translation,
radicand, flight-order and rank-transition events.
