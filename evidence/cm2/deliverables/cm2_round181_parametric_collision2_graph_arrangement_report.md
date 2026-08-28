# CM2 Round181 — parametric collision-2 graph arrangement

Date: 2026-07-26

## Verdict

`PARTIAL`, with no global disposition or integer promotion.

Round181 pins the frozen Round178 certificate and independently verified
chain.  It resolves 9,430 of the 11,416 collision-2 candidate/root-order
collar boxes at the owner/root-order level and materializes 8,292 additional
strict local 3D exact-key boxes.  It does not close any complete live
stratum: collision2 remains 0/16 fully closed and 16/16 partial.  D02 remains
`BLOCKED`, Gate5 remains `10/18`, and CM2 remains `NO-GO_FOR_CLAIM`.

## Exact continuation improvement

All 55 recentered `W:W` collision-2 candidates have pairwise disjoint
physical boundaries on the full parameter interval.  The exact registry
checks all 1,485 pairs and has strictly positive squared separation margin.
Consequently two strict future near roots cannot be equal; their order on a
connected fixed-status cell is determined by one strict point.

Round181 adds two fail-closed bounds for a candidate whose discriminant is
still interval-unresolved:

- `candidate.ell + candidate.radius < 0`: even its far root is behind;
- `incumbent.near < candidate.ell - candidate.radius`: it is later whenever
  real.

These certify 22,848 exact box-candidate relation exclusions:

- 15,864 `UNIVERSALLY_BEHIND_WHEN_REAL`;
- 6,984 `UNIVERSALLY_LATER_WHEN_REAL`.

This corrects the preliminary interpretation of `W[1,-2]`.  The frozen
minimum regression
`W:E:00.14.01101 / 00.14.01101000000000000000`
has interval-unresolved Delta but satisfies `ell+R<0`; its Delta-positive
point is an intersection behind, not a forward birth graph.

## Root-order census

The exact conservation of the 11,416 Round178 root/order boxes is:

| Round181 status | Boxes | Exact volume |
|---|---:|---:|
| local exact key + strict outgoing chart | 8,292 | `4977063/13421772800000` |
| exact owner/root/wall word; outgoing-chart graph outer | 1,128 | `34869/335544320000` |
| exact owner/root; Y-endpoint wall graph outer | 10 | `177/167772160000` |
| point winner non-strict on the full box | 1,396 | `172929/838860800000` |
| regular-if-nonempty single-Delta outer | 584 | `21771/335544320000` |
| two-Delta arrangement outer | 6 | `531/419430400000` |

The input volume is `10040679/13421772800000`.

The 584 single-candidate outers have a strict nonzero derivative

`dDelta/dp1 = 2 eta ell / sqrt(1-p1^2)`

and a strict negative center witness, but no positive-owner witness on the
ordered 27-point rational grid.  They are therefore only
`REGULAR_IF_NONEMPTY_DELTA_GRAPH_OUTER`; Round181 certifies zero nonempty
candidate graph carriers.  It does not infer a Delta-positive chamber or a
nonempty Delta-zero graph from interval overwrap.

The six two-candidate boxes retain 12 nominal 2D graph carriers and six
nominal pairwise 1D intersection outers.  No 1D intersection is declared
nonempty.

## Wall, chart, and dimensional ledger

The exact owner/root continuation exposes:

- 168 nominal Y-endpoint integer-wall graph outers: 158 inherited and 10 new;
- 1,128 nominal collision-2 outgoing-chart `H2=0` graph outers;
- 596 nominal candidate-Delta graph carriers if present.

For all three classes, certified nonempty carrier count remains zero.  Wall
side words, wall pullback Jacobians, and the two outgoing-chart side chambers
remain unclosed.  The `H2=0` half-open rule is retained: `E/W` owns the
diagonal and `N/S` excludes it.

The inherited collision-1/source-boundary ledger remains:

- 276 Delta/root collars;
- 172 collision-1 outgoing-chart collars;
- 50 collision-1 root-order/root-sign outers;
- 32 source-seam collars.

The two guard recharts retain `E` as the physical 2D source-seam owner, with
the four 1D Delta/H intersections counted once.  No lower-dimensional
integer credit is issued.

## Exact residual

Across the 12,104 targeted Round178 boxes:

- targeted exact coordinate volume:
  `71388171/2684354560000`;
- new local exact-key boxes: 8,292;
- new local exact-key volume:
  `4977063/13421772800000`;
- residual parent boxes: 3,812;
- residual exact coordinate outer volume:
  `21997737/838860800000`;
- integer census delta: 0.

Together with Round178, there are 9,652 strict resolved inner boxes, still
concentrated in six parents.  The other ten parents have no resolved inner
box.  No inner occurrence, including ordinal 290575, and no point
observation, including ordinal 289591, becomes a global Gate5 disposition.

## First analytic blocker

The first blocker is existence and side bracketing for the 584
regular-if-nonempty single-Delta outers.  A face-bracketed interval-Newton
solve in the exact recentered coordinate is needed before asserting a
nonempty graph or positive chamber.

After that:

1. coupled interval-Newton/Krawczyk isolation is needed for the six
   two-Delta boxes and their six nominal 1D incidences;
2. 168 Y-endpoint wall graphs need a nonzero pullback Jacobian and both
   half-open wall words;
3. 1,128 outgoing-chart outers need both strict side chambers;
4. the inherited collision-1 and source-seam carriers must be closed.

## Independent verification

The verifier does not import or execute the Round181 producer.  It rebuilds
the complete approximately 19 MB result from frozen Round178, including all
22,848 relation rows, and requires full canonical equality.  It does not use
a frozen Round181 result digest as a semantic rejection shortcut.

Verification is `PASS`:

- re-signed semantic attacks rejected: 23/23;
- strict JSON attacks rejected: 9/9;
- path/alias attacks rejected: 11/11.

The semantic suite includes behind-to-forward promotion of `W[1,-2]`,
9,430-to-whole promotion, 8,292 local-to-global promotion, a forged positive
witness for the 584 outers, forged closure of the six pair incidences, wall
and outgoing carrier closure, relation digest/count, volume/conservation,
source-seam ownership, D02, Gate5, 289591, and 290575.

Producer and verifier are byte-identical under `PYTHONHASHSEED=1` and
`PYTHONHASHSEED=987654321`.  Effective Arb precision is 384 bits from the
pinned Round178/registry transitive import chain.
