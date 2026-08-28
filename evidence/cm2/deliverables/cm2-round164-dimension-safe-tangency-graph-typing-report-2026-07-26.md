# CM2 Round164 v2 — dimension-safe tangency-graph typing

Date: 2026-07-26

## Decision

Round164 v1 is withdrawn and superseded.  Its Arb replay correctly typed
32 physical first-tangency graphs, but it incorrectly subtracted the 12
prefix-mismatch graphs from a census of three-dimensional ambient leaves.
A codimension-one graph does not classify either open side of its parent.
Consequently the v1 counts

```text
combined recordwise exclusions   37,492
remaining ambient leaves         39,336
```

are invalid.

Round164 v2 keeps the valid graph result, removes all whole-leaf credit, and
restores the Round163 ambient census:

```text
typed codimension-one graphs          32
  frozen-owner graphs                 20
  prefix-mismatch graphs              12
new full-dimensional exclusions        0

combined ambient exclusions       37,480
remaining ambient leaves          39,348
  prefix stage-one matches           518
  outgoing-chart seam leaves         618
  tangency-parent bulk                 32
  multi-candidate leaves           38,180
```

The component identity is exact:

```text
518 + 618 + 32 + 38,180 = 39,348.
```

## Graph theorem and dimensional scope

Each of the 32 parent boxes carries one unique monotone physical
first-tangency graph

```text
D_target(t,p,s) = 0,
```

with base variables `(t,s)` and graph variable `p`.  The producer replays a
strict nonzero `partial_p D_target` enclosure and strict opposite signs on
the two `p` faces at 192-bit Arb precision.  Every row now records

```text
ambient dimension        3
typed graph dimension    2
credit scope             CODIMENSION_ONE_GRAPH_ONLY
ambient bulk             UNRESOLVED_OFF_GRAPH_BULK.
```

Serialized Arb strings are labelled display outers.  Sign credit comes only
from the internal strict Arb comparisons and is independently recomputed by
the verifier.

No parent is replaced until the three pieces `D<0`, `D=0`, and `D>0` are
materialized, classified, and shown to cover the parent with a consistent
half-open ownership rule.

## Live off-graph regressions

Two strict interior points demonstrate why whole-parent pruning is invalid.

```text
W:N:05.00.00100110
  (t,p,s) = (7611/32000, -12599/12800, 0)
  tangency target G[1,1] discriminant < 0
  point classification unique_first W[1,0]
  outgoing chart W

W:S:H.05.00.00100110
  (t,p,s) = (7611/32000, 12599/12800, 0)
  tangency target G[1,0] discriminant < 0
  point classification unique_first W[1,0]
  outgoing chart W.
```

Both points are strictly inside their three-dimensional parents.  Their
tangency-target discriminants are approximately `-0.00942225`, and both
outgoing-chart margins are strictly positive.  The points are frozen in the
v2 certificate as regression rows.

## Verification hardening

The v1 verifier also had incomplete semantic coverage: several result,
provenance, census, and next-gate fields could be changed and re-signed
without rejection.  The v2 verifier independently rebuilds the complete
expected document and requires exact canonical equality.

The semantic attack suite now mutates 36 fields and re-signs every result
mutation.  It rejects all 36/36 attacks, including:

- codimension-two/full-dimensional credit confusion;
- restoration of the withdrawn `39,336` count;
- removal or mutation of either live regression;
- forged status, provenance, D02/CM2 promotion, and next-gate text;
- added unknown result keys.

All 7/7 strict JSON and encoding attacks are also rejected.

The optimized producer and independent verifier each evaluate phase geometry
once per box while preserving the pinned root-operation order.  Under
different hash seeds they produce byte-identical outputs.  Observed cold
replay times were about 89 seconds for the producer and 91 seconds for the
verifier.

## Strict state and next core gate

```text
D02                                  BLOCKED
D03 negative oracle            UNAUTHORIZED
global Gate5                         10/18
global complete 18-field blocks          0
CM2                        NO-GO_FOR_CLAIM
```

The next exterior work is to materialize and classify `D<0 / D=0 / D>0`
replacements for all 32 tangency parents, adaptively resolve the 618
outgoing-chart seam parents, and refine the 38,180 multi-candidate parents.
No D02 reconsideration is authorized until the full compact fundamental
domain has zero unresolved leaves across all relevant signatures, chart
seams, grazing strata, and corners.
