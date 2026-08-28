# CM2 Round 74: fixed-s0 depth-two and cross-rank quotient assault

Date: 2026-07-21

## Scope and verdict

This round constructs the first actual fixed-parameter, two-dimensional
depth-two registry on the same 24 physical core rectangles used by the
Round-73 base-R1 quotient. It certifies strict R2 cells and their parent
incidence, and tests oriented trace cancellation through the rank join.

It does not close the complete physical R2 face atlas. Composite gates remain
`0/5`; CM2 remains `NO-GO_FOR_CLAIM`.

## Legacy depth-two root audit

The frozen three-dimensional Q2 registry cannot simply be sliced at `s=0`.
Among the 2,868 frozen Q1 parents:

```text
closed boxes touching s=0:                         804
s=0 strictly inside the open s interval:            32
touching only at an adaptive s endpoint:            772
strict fixed-s0 Q2 cells retained by that registry:   4
```

The 772 endpoint-only boxes are rejected because the old registry explicitly
excludes fixed-parameter claims on adaptive `s` endpoints. The four retained
cells are whole G-axis rectangles. Their join with Round 73 is only the
identity and is not a complete fixed-s0 depth-two atlas.

## Actual fixed-s0 depth-16 tree

A new two-dimensional Arb tree freezes `s=0` from the start, splits only the
source `(t,p)` coordinates, and applies the exact time-one and time-two
collision classifiers on all 24 cores. At binary depth 16 it gives

```text
R1 strict leaves:       9,112
R2 strict leaves:       2,432
Q2 strict leaves:      76,708
depth-two outer:       65,256
all terminal leaves: 153,508
```

The normalized coordinate-area ledger is exact:

```text
R1 inner:       3069/4096
R2 inner:         19/512
Q2 inner:     182009/8192
outer:           8157/8192
total:                    24
```

Thus the certified strict inner area is `188451/8192`; the unresolved outer
is retained rather than declared null. The 2,432 strict dyadic R2 boxes occur
on eight W-diagonal source cores and already give an R2 normalized-area lower
bound of `19/512`.

## Narrow R2 branches

The depth-16 dyadic tree detects eight main source/destination pairs. A
separate positive-box search finds a second narrow corner branch on every one
of those source cores. All `16/16` boxes have:

- strict Q1 parent classification at time one;
- a strict unique second collision owner;
- strict R2 classification at time two; and
- positive rational `(t,p)` area.

Hence the actual fixed-s0 R2 registry has at least 16 distinct certified
source/destination pairs: eight main and eight narrow-corner branches. The
narrow branches are not promoted to complete connected components.

## Cross-rank incidence

The Round-73 quotient has 40 parent two-cells. The new strict child map is

```text
R1 child -> same-core return parent:       9,112
Q2/R2 child -> same-core survival parent: 79,140
certified child-parent incidence edges:   88,252
outer children with no promoted edge:     65,256
```

All 16 positive R2 witness boxes have an actual same-core survival parent.
This is the first nonempty physical rank-one child registry attached to the
Round-73 rank-zero quotient.

## Oriented trace test

The binary forest has exactly

```text
153508 - 24 = 153484
```

internal split faces. Every split face occurs once with each orientation in
the sum of its two child boundaries. Therefore all `153,484/153,484`
artificial dyadic trace pairs cancel exactly through the rank join.

The physical test has a split verdict:

```text
artificial adaptive-face cancellation: CERTIFIED_EXACT
physical R2 pullback-face cancellation: NOT_CERTIFIED
```

The physical R2 level sets still lie partly inside the retained depth-two
outer. Therefore no physical F17, Gate-4 commuting square, or limiting
weighted face sum is promoted.

## Latest technology audit

The targeted search found arXiv:2602.07718, *Certified surface approximations
using the interval Krawczyk test* (Burr, Hauenstein, Lee, 2026). Its generalized
Krawczyk test certifies non-square analytic systems and higher-dimensional
varieties. This is algorithmically relevant to certifying the one-equation
R2 boundary curves in two source variables. It is not a ready-made billiard
theorem: the collision owner/tangency charts must first be separated and the
analytic branch equations supplied. No current gate is promoted from the
paper alone.

## Audit

- Legacy fixed-s0 split replay: `804=32+772`.
- Depth-16 area ledger: exact pass.
- Strict dyadic R2 rows: `2432/2432`.
- Positive R2 pair boxes: `16/16`.
- Artificial oriented trace pairs: `153484/153484`.
- Hostile semantic mutations: `192/192` rejected.
- Strict JSON adversaries: `4/4` rejected.
- Manifest producer: byte-identical reemit.

## Strict frontier

```text
actual fixed-s0 depth-two inner registry: PARTIAL DEPTH-16 CERTIFIED
actual positive R2 cells:                 2432 dyadic + 16 pair witnesses
cross-rank child-parent incidence:        88252 certified
artificial rank-join trace cancellation:  certified exact
complete physical R2 face atlas:          not certified
physical rank-join trace cancellation:    not certified
limiting weighted rank/path sum:          not certified
Gate 4 / Gate 5:                          1/7 landing / 10/18, blocks 0
complete composite gates / CM2:           0/5 / NO-GO_FOR_CLAIM
```

## Next shortest route

Replace rectangle-only exclusion around the 16 R2 source/destination pairs
with chart-separated generalized Krawczyk continuation of each one-dimensional
physical boundary curve. Then classify all curve endpoints/intersections,
build the complete R2 pullback quotient, and retest physical oriented trace
cancellation rather than only artificial dyadic cancellation.
