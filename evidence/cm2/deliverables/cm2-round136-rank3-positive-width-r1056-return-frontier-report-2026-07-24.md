# CM2 Round 136 — positive-width rank-1056 return frontier

Date: 2026-07-24

Round 136 materializes the first frozen positive-area local return cylinder
on the selected corrected rank-three branch. Starting in source core 14, the
whole rational source box has no C24 return at collisions 1 through 1055 and
lands strictly in one frozen C24 core at collision 1056.

This is an actual local return component witness. It is not yet the canonical
global `c24-component` required by Round27, and it does not create a Round35
restriction, Round50 owner, Round54 token, or Round67 `q_j`.

## Exact source box

The box lies at `s=0` in corrected face

```text
physical-s0-rank3-corrected-face:
02a116578e4b096df6c1575632590e5e6202442803da780fb13cdb6ff1026773
```

with link rank 1 and Round116 strip 128. Its `p` center is
`-1587/1638400`.

The `t` seed is selected by 1500 exact rational bisections of the strict
third-collision equation

```text
Delta3(t,p_center) = (4/25)^2 * (2^-64)^2.
```

The frozen source half-width is `2^-3815` in both `t` and `p`. Consequently
the exact source area is

```text
2^-7628 > 0.
```

The whole box is strictly on the HIT side, remains strictly below the
construction cosine target, and has positive transverse `D_t`. The target
cosine is used only to locate the rational source box; it is not used to
force any later collision.

## Complete collision replay

Every collision owner is selected from the complete translated retained
candidate list. The replay independently establishes:

```text
collision rows:                         1056
preterminal strict nonreturns:          1055
terminal strict returns:                   1
destination:
  core:d6e30c5e3160559018e3ed757ec6d3fc12eb97cbd9d9673c7907621b2fe97ee8
official-word occurrences:              1056
unique official-word IDs:                125
```

The first three official registry ordinals are
`266945 / 285659 / 42355`, matching the corrected Round116 HIT prefix. That
three-word prefix remains only a prefix; the return path is the complete
1056-word sequence.

Each word is rebuilt after removing the incoming owner's exact lattice
translation. Its relative target, ordered wall record, registry row hash,
ordinal, and `gate5-word` ID are all closed independently.

The frozen row-group hash is

```text
81edef669aedd3a79a0a3ef6e0fb433d865ff94ce016e477d89380abbb7d35e3
```

and the local cylinder identifier is

```text
round136-local-return-cylinder:
51fca5b65a5bfef1067ea3bf60e464db5fe9d4fd192db0696160184c2781026e
```

## Homogeneity, incidence, and strict margins

The complete whole-box classification is:

```text
H0_CENTRAL collisions:                  1055
H4294967295 collisions:                    1
tail collision index:                      3
incidence rank B=14 rows:                1054
incidence rank B=65 rows:                   2
```

The second rank-65 row is the next collision's source endpoint, inherited
from the tail cosine at collision 3.

Seventeen margin families are recorded. They cover every candidate
discriminant and time decision, unique-winner gaps, positive flight and
flight-cap bounds, chart dominance, C24 exclusion or inclusion, central and
tail homogeneity boundaries, and both sides of every capped
reciprocal-cosine rank. The ledger contains 54,420 strict miss-discriminant
observations and 37,790 strict nonreturn-core separators. The terminal
landing has six strict inside-core margins.

## Typed occurrence and canonical-rank boundary

The complete 64-row Round132 label registry has one row with label

```text
["G", "W[0,-1]", 1, "W[0,-2]", -1].
```

This remains a typed occurrence singleton only. Its Round67 owner and `q_j`
fields are null.

The frozen Round27 and Round35 contracts still do not provide an executable
least-dyadic-basis component enumeration. Round136 therefore certifies the
actual positive-width local cylinder but leaves these values null:

```text
canonical Round27 path ID
c24-component ID
Round35 rn-restriction ID
Round50 owner key
Round54 t54 token
Round67 q_j output
```

No claim is made that the selected D=0 occurrence face belongs to the closure
of this R1056 cylinder.

## Independent verification

The independent verifier does not import or execute the Round136 producer.
It reconstructs the rational box and the full 1056-collision result from
byte-pinned upstream inputs, re-closes every row and group hash, and checks
the complete result against the frozen certificate.

The primary replay uses 8192-bit Arb precision. A second 12288-bit replay
independently confirms the complete discrete collision projection, summary,
and every margin name/depth/count/witness tuple. Exact Arb enclosure endpoints
are precision-dependent and are intentionally compared only in the primary
8192-bit reconstruction.

Formal verification is `PASS`:

```text
re-signed semantic mutations rejected:  70/70
strict-JSON attacks rejected:           19/19
in-process path attacks rejected:       13/13
dual PYTHONHASHSEED replay:              byte-identical
process-level hostile I/O:               fail-closed
```

Frozen hashes:

```text
producer:            4e78309d5275bf367e6df03509c40ebaaac6f344c7948446a25b3b508c8c2bc2
certificate:         d9b7b7823dddce2dcbc16412294c8ecef42b304712d4bb968896d2221b8aa7f9
certificate result:  407bc2dbecaacb2ed8527a3fe8a41f97ed523a43f428c37b76e14639425cf545
verifier:            597778df1deefa34b690c4ed665fcb1f8df965aa45d9a7c03093a0e632cf23ad
verification:        501035c235124e1c1a57fa198ee63e4f90c7a729497b600c31b2212e5260964c
verification result: a59b1ef17ba18862663f8f77cfde99a6db9cccf5dbf93d96ed4b6d6cea4d4bdc
```

## Strict global state

```text
actual positive-width local R1056 cylinders: 1
canonical global c24-components:             0
Round35 restrictions:                        0
Round50 owners:                              0
Round67 q_j outputs:                         0
global complete 18-field blocks:             0
Gate5 global maturity:                   10/18
Gate5:                            NOT_CERTIFIED
CM2:                           NO-GO_FOR_CLAIM
```
