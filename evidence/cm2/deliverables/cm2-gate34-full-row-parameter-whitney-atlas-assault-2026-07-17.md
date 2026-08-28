# CM2 Gates 3/4: full-row parameter Whitney germ atlas

Date: 2026-07-17 (Asia/Shanghai)  
Frozen inputs: the 64 maximal reference occurrence rows and the selected
actual-parameter all-scale shell certificate  
Strict verdict: **every interior point of every reference maximal row now
has two actual-parameter all-scale hit/miss germs in a countable Whitney
atlas.  This is not a finite uniform-radius atlas and does not yet give a
bounded common-strong-space grazing pushforward, so Gates 3 and 4 remain
open.**

## 1. Correct full-row object

Normalize each open maximal row to `t in (0,1)`.  Use the countable family

```text
central cell: [1/4,3/4),
left/right dyadic Whitney cells: every level n>=2.
```

The closure of each cell is compactly contained in one constant physical
label row.  The relevant collision predicates form a finite strict system,
and all moving centres and regular competitor roots are continuous.
Compactness therefore supplies a positive actual-parameter radius on every
cell.  Dyadic halving is a terminating certificate search for such a
radius.  Consequently all interior points of all 64 rows have both hit and
miss all-scale germs.

No radius uniform over the countable family is asserted.  Endpoint collars
are handled by vanishing tails, not by silently adjoining singular endpoints.

## 2. Materialized level-16 prefix

The finite replay prefix contains

```text
31 cells per row,
1984 Whitney cells,
3968 oriented parameter-germ records,
covered interval [1/131072,131071/131072),
omitted endpoint length per row 1/65536.
```

Using the row-angle width bound `2*pi<7`, its omitted positive-coarea mass
and graph-current tails satisfy

```text
positive coarea tail <= 63/2560,
hit-minus-miss graph TV tail <= 63/1280.
```

Both tails tend to zero along the finite prefixes.  This order-zero tail is
not promoted to a strong-space norm estimate.

## 3. Endpoint audit

The 128 endpoint incidences split exactly as

```text
later miss-switch boundary: 64,
source grazing:              32,
parameter polarity:          16,
earlier first visibility:    16.
```

Source-grazing density vanishes through `cos(phi)` and polarity density
through `|u_y|`; first-visibility and miss-switch endpoints have zero base
mass.  There are no extra endpoint atoms.

## 4. Strict frontier

```text
REFERENCE FULL-ROW COUNTABLE GERMS, 64 ROWS:       CERTIFIED
MATERIALIZED WHITNEY CELLS:                         1984
MATERIALIZED ORIENTED GERMS:                        3968
LEVEL-16 GRAPH-TV ENDPOINT TAIL <=63/1280:         CERTIFIED

FINITE UNIFORM-RADIUS FULL-ROW ATLAS:              NOT CERTIFIED
WEIGHTED LOCAL-RADIUS SUMMABILITY:                 NOT CERTIFIED
FINITE-s FUTURE SINGULARITY ATLAS:                 NOT CERTIFIED
BOUNDED COMMON-STRONG-SPACE GRAZING PUSHFORWARD:   NOT CERTIFIED
STRONG DQ / MT_DQ / FACE:                         NOT CERTIFIED
GATE 3 / GATE 4:                                  NOT CERTIFIED
```

The fail-closed verifier replays the atlas and rejects `23/23` hostile
mutations.  Live mode exits `2` because no composite gate closes.
