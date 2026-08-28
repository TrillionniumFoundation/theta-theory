# CM2 Round169 — source-G return-signature coverage survey

Date: 2026-07-26

## Decision

Round169 certifies a bounded exact-key deficit census.  It does not exclude
an exterior leaf, complete a return-signature domain, or promote D02.

The pinned Gate-3/Gate-5 inputs provide a complete *candidate* key envelope
for source-G:

```text
source-G charts                         4
retained targets per chart             57
clean-wall patterns per target        985
source-G chart/target pairs           228
source-G candidate exact keys     224,580
```

The producer independently replays the rational horizon/outgoing-halfspace
candidate reduction and all 441,280 eight-chart immutable key rows.  Their
pair and row digests equal the frozen Gate-5 registry.

## Existing source-G atlas

```text
chart    leaves    unique-first    tangency graphs    multi-candidate
G:E      16,580          5,276                  38             11,266
G:W      16,580          5,276                  38             11,266
G:N      16,630          5,340                  42             11,248
G:S      16,630          5,340                  42             11,248
total    66,420         21,232                 160             45,028
```

`G:E` and `G:N` are direct 192-bit Arb atlases.  `G:W` and `G:S` are the
pinned exact `Jx`/`Jy` reflected atlases.  The reflection certificate
transports leaf rows and target labels.  It does not certify the signed
clean-wall word or outgoing-chart transformation at the immutable exact-key
level, so no return key is transported by symmetry in Round169.

## Exact-key coverage

The Round139 positive-area R1648 cylinder contains 1,143 source-G collision
occurrences and 103 distinct immutable source-G keys:

```text
chart    occurrences    distinct keys    distinct chart/target pairs
G:E              284               25                              13
G:W              282               26                              13
G:N              289               26                              13
G:S              288               26                              13
total          1,143              103                              52
```

The 103 witnessed keys have roof histogram

```text
roof 1    28
roof 2    56
roof 3    17
roof 4     2
roof 5-9   0.
```

They are local positive-area witnesses on one cylinder, not global
dispositions of complete chart-key domains.  The strict coverage ledger is
therefore

```text
candidate envelope registered                 224,580 / 224,580
local Round139 positive-area key witnesses          103 / 224,580
global geometric exact-key dispositions               0 / 224,580
keys lacking a global disposition                 224,580.
```

The pinned Round162 compact-to-Gate3 bridge explicitly has
`source_obstacle=W`; no source-G compact bridge exists in the current chain.

## Source-W baseline audit

Round169 also rechecks the current dimension-safe source-W baseline.  The
single frozen prefix is collision-one owner `W[1,0]` with outgoing chart
`W`.  Round164-v2 preserves

```text
source-W chart-leaf records              76,828
recordwise ambient exclusions            37,480
ambient unresolved                       39,348
  stage-one match                            518
  outgoing-chart seam                        618
  tangency ambient leaf bulk                  32
  multi-candidate                         38,180.
```

The 32 tangency graphs add zero whole-dimensional exclusions.  None of the
37,480 one-prefix source-W exclusions is transported to source-G or to
another return-signature search.

## Shortest extension

1. Certify a source-G compact-to-Gate3 bridge and exact `Jx`/`Jy`
   transformations for signed wall words and outgoing charts.
2. Materialize wall-crossing order and outgoing chart on the 21,232
   unique-first leaves, splitting only at exact event surfaces.
3. Apply cached active-target refinement to the 45,028 multi-candidate
   leaves.
4. Keep the 160 tangency graphs, source-grazing faces, chart seams and wall
   corners in separate dimension-safe ledgers.
5. Aggregate by immutable ordinal and require every key to be
   empty/nonempty/connected/excluded/cemetery with zero unresolved before
   any exterior claim.

A naive `66,420 × 224,580` leaf/key cross-product is unnecessary; the
candidate target and wall-word stages should remain factored.

## Verification

The independent verifier imports or executes no Round169 producer code.  It
rebuilds all 162 target classifications per chart, 448 chart-target pairs,
441,280 exact keys, both 1,648-row Round139 key copies and the complete
expected certificate.  It rejects 20/20 re-signed semantic mutations and
7/7 strict JSON attacks.

Producer and verifier replay byte-identically under distinct hash seeds.

## Strict state

```text
source-G global exact-key dispositions complete    false
all return signatures excluded or connected        false
D02                                                 BLOCKED
D03 negative oracle                                 UNAUTHORIZED
global Gate5                                        10/18
global complete 18-field blocks                     0
CM2                                                 NO-GO_FOR_CLAIM
```
