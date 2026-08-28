# CM2 Round 88 — rank-three physical-port component quotient

Date: 2026-07-22

## Outcome

The live registered-side rank-three continuation frontier is now exactly
localized.  Crosswalking all `4,216` Round-85 ports against the complete
Round-87 local-event classification proves that none of the `1,672` frozen
box-components mixes locally physical and locally nonphysical non-source
ports.

Only `352` components, carrying `496` registered elementary arcs, meet the
`945` locally physical next-tangency ports.  The other registered rows split
into `920` nonphysical-open components carrying `1,212` arcs and `400`
source-boundary-only components carrying `400` arcs.

This is a strict reduction of the global continuation workload from all
`2,108` registered arcs to `496` live registered arcs.  It is not a global
outward-branch pairing and is not a complete-face certificate.

## Exact partition

| Frontier class | Components | Arcs | Source ports | Physical non-source ports | Nonphysical non-source ports |
|---|---:|---:|---:|---:|---:|
| source-boundary only | 400 | 400 | 800 | 0 | 0 |
| physical-open | 352 | 496 | 47 | 945 | 0 |
| nonphysical-open | 920 | 1,212 | 157 | 0 | 2,267 |
| mixed physicality | 0 | 0 | 0 | 0 | 0 |

Every row satisfies the exact component identity

`registered_port_count = 2 × registered_elementary_arc_count`.

## Installed registered-side pair rows

Among the `352` live components, `320` contain exactly one elementary arc.
Their two registered-side endpoints are therefore uniquely paired without
any geometric guess:

- `285` physical-port to physical-port pairs;
- `35` source-boundary to physical-port pairs.

The only remaining registered-side pairing ambiguity is concentrated in
`32` multi-arc live components containing `176` arcs, `340` physical ports,
and `12` source-boundary ports.  Those rows need an exact zero-set incidence
reconstruction before their endpoints can be paired.

## Verification

The producer pins the Round-85 port census, the Round-87 1536-bit-audited
local-event result, and both executable producers.  No new floating-point or
interval classification is introduced: the Round-88 step is an exact
closed-schema incidence quotient over those pinned analytic results.

The independent verifier rebuilds all component/port incidence rows directly
from the two upstream manifests and independently repeats the physicality
crosswalk.

- full independent recomputation: `PASS`;
- file pins: `4/4`;
- hostile semantic mutations rejected: `6/6`;
- strict-JSON attacks rejected: `4/4`;
- producer and verifier cold replay: byte-for-byte identical;
- Python compilation: passed.

## Strict limits and next frontier

The certificate does not assert that locally nonphysical boundary behavior
rules out an internal physical subarc.  It does not relabel source-core
boundary ports as physical endpoints.  It does not pair any branch outside a
registered union and does not pair the `32` multi-arc live components.

The next exact tasks are therefore sharply bounded:

1. rebuild zero-set incidence inside the `32` multi-arc live components;
2. globally continue the `945` physical outward branches through owner,
   chart, translation, radicand, flight-order, and rank-transition events;
3. form a physical-face quotient only after both ledgers have no unmatched
   physical ports.

No complete physical face, Gate 5, or RN row is promoted in this round.
