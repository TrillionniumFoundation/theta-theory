# CM2 Round172 — dimension-safe tangency-parent frozen-owner absence pruning

Date: 2026-07-26

## Decision

Round172 independently replays all 32 Round164-v2 source-W tangency parents
at 192-bit Arb precision.  Among the 12 parents whose codimension-one
tangency target is not the frozen owner, it proves:

```text
frozen owner W[1,0] absent on the full 3D parent      10
frozen owner W[1,0] strict-future exceptions           2
total prefix-mismatch graph parents                    12
```

The ten absence results are strict whole-parent records:

```text
record classification             no_real_intersection
frozen-owner discriminant sign    strictly negative
scope                              entire 3D ambient parent box
```

They therefore support ten new whole-parent frozen-prefix exclusions.  The
exclusion proof does not use the fact that another target's tangency graph is
a prefix mismatch.  A codimension-one mismatch graph by itself still receives
zero whole-parent credit.

The other 20 Round164 parents have a typed frozen-owner tangency graph and
remain live.  The two strict-future exceptions also remain live composites,
so 22 tangency-parent composites remain.

## Exact ten-parent exclusion set

```text
W:E:00.14.11111
W:E:00.15.0011101
W:E:07.00.1100010
W:E:07.01.00000
W:N:00.00.0110111
W:N:02.15.11011001
W:N:07.15.1001000
W:S:H.00.00.0110111
W:S:H.02.15.11011001
W:S:H.07.15.1001000
```

For every key, the replay evaluates every retained candidate target from one
192-bit source-W geometry enclosure for the entire parent box.  The W[1,0]
line-circle discriminant is strictly negative throughout that enclosure, so
no real W[1,0] intersection exists anywhere in the parent.

The stored Arb strings are display outers only.  Some concise display strings
visually straddle zero even when Arb's full internal enclosure certifies a
strict sign.  Neither producer nor verifier uses the display string as a sign
witness; both independently require the native 192-bit predicate
`discriminant < 0`.

## Two live strict-future exceptions

```text
W:N:05.00.00100110
W:S:H.05.00.00100110
```

On both entire parent boxes, W[1,0] has a strictly positive discriminant and a
strictly positive near root.  They therefore cannot receive frozen-owner
absence credit.

Each exception is also bound to and independently replays the corresponding
Round164-v2 strict-interior regression.  At that point:

```text
first-hit classification                  unique_first
first owner                               W[1,0]
outgoing chart                            W
mismatch tangency target                  no_real_intersection
mismatch-target discriminant              strictly negative
```

Thus the exception has a certified live off-mismatch-graph point and remains
one conservative parent composite.

## Full 32-parent census

The replay reconstructs the complete Round164-v2 partition:

```text
all tangency parents                                  32
prefix-mismatch tangency-target parents               12
  full-parent frozen-owner absence                    10
  strict-future live exceptions                        2
frozen-owner tangency-target parents                  20
remaining live parent composites                     22
```

For the 20 frozen-owner graph parents, the W[1,0] discriminant crosses the
typed graph inside the parent, so no whole-parent absence proof is possible.
Their graph is two-dimensional inside a three-dimensional ambient parent and
receives zero whole-parent credit.

## Composition with Round168

Round172 pins the Round164-v2 certificate and independent verification, plus
the Round168 combined-ledger certificate and independent verification.  Its
new credit lies inside the Round168 tangency live class, which is disjoint
from all three Round168 credit blocks.

```text
Round168 whole-record exclusions                  73,162
Round172 new whole-parent exclusions                  10
combined whole-record exclusions                  73,172

original prefix stage-one matches                    518
Round165 seam live composites                        504
remaining tangency parent composites                  22
Round166 owner-active multi parents                2,616
combined conservative live                         3,660

conservation                              73,172+3,660=76,832
```

The refined source-W total remains 76,832.  Round165 collar mismatch sides
and the Round166 unverified deep refinement profile continue to receive zero
whole-record credit.

## Independent verification

The Round172 verifier byte-pins but does not import or execute the Round172
producer.  It also imports or executes neither the Round164 nor Round168
producers.  The executable geometry closure pins the candidate registry,
eight-cell atlas, and its GE interval-atlas dependency, and requires
`python-flint 0.9.0` with a 192-bit Arb context.  It independently:

```text
rebuilds the source-W atlas at 192 bits                  true
reconstructs all 32 tangency parents                     true
reconstructs all 12 prefix-mismatch parents              true
reconstructs all 10 whole-parent absences                true
reconstructs both strict-future exceptions               true
reconstructs all 20 frozen-owner graph parents           true
replays both Round164 live regressions                   true
requires recursive exact-key equality                    true
requires full expected canonical document equality       true
```

Its fail-closed attack suites pass:

```text
re-signed semantic mutations rejected                  78/78
strict JSON attacks rejected                             9/9
path-safety attacks rejected                             7/7
```

Every semantic mutation is re-signed at the result-envelope level.  The
suite covers the 32/12/10/2/20 census, every dimension-safe credit guard,
full-parent record scope, discriminant classification, exact key sets, row
and table digests, exception regressions, the remaining-22 ledger,
Round168 composition and disjointness, prohibited graph/collar/deep-profile
credit, upstream pins, nonpromotion, and next-gate wording.

The strict-JSON suite rejects duplicate keys, floats, NaN, BOM, raw and
escaped NUL, unpaired surrogates, trailing documents, and a non-object top
level.  The path suite rejects symlink, hardlink, and oversized inputs plus
outside-directory, protected-alias, symlink, and hardlink outputs.

Cold replay in separate clean processes under `PYTHONHASHSEED=1` and
`PYTHONHASHSEED=987654321` is byte-identical for both the certificate and
verification:

```text
producer source SHA256
81f147cf6106d7436df282de106fc47e793e8f97a43282b35719e28182e07980

certificate result SHA256
a436b4a82b1e8d5c617fe576e0e4e76b6f6f38ad8ac3eda4ddde544c2769a776

certificate file SHA256
3185188c476a64d3e732674fa724ce9a49afe84c61abab448f746a5a3555b66c

verifier source SHA256
066f84d1517338774a8fc8132bd61006cabedbe7674129a433016fc16ddcad99

verification result SHA256
aa0fb2c28176cf46b058506658a21070679e0a91a4f94ed65245fb378e088603

verification file SHA256
d095ecdd1b59a6577f96f0317f8a30122e8cd3f6baf73ed550c5d227ed1811c3
```

## Strict state and next gate

```text
D02                                      BLOCKED
D03 negative oracle                     UNAUTHORIZED
Global Gate5                            10/18
global complete 18-field blocks             0
CM2                                      NO-GO_FOR_CLAIM
```

All 22 remaining tangency composites still require dimension-safe
materialization and separate ledgering of their `D<0`, `D=0`, and `D>0`
strata.  Outgoing-chart and later frozen-prefix processing may continue only
on the resulting live strata.  The 224 whole-W rectangles and 2,616
owner-active multi parents also remain downstream core work.
