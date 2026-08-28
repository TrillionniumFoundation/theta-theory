# CM2 Round 76: residual refinement and cross-rank numeric-field assault

Date: 2026-07-21

## Scope and verdict

This round attacks both branches left by Round 75. It refines the actual
fixed-`s=0` depth-two tree from binary depth 16 to depth 20, tests every
strict R2 leaf against the 16 certified physical components, and attaches
numeric F8/F9/F10/F13/F16 rows to all 32 physical R2 faces. It also evaluates
the first finite two-rank geometric-depth weighted field sum.

The residual outer is reduced but not eliminated. Therefore the complete
fixed-parameter depth-two atlas, the official limiting path-law weighted sum,
and all composite gates remain unproved. CM2 remains `NO-GO_FOR_CLAIM`.

## Fixed-s0 depth-20 refinement

The Round-74 tree is rerun from the 24 physical source cores with four more
binary levels. The exact terminal registry is

```text
R1 strict leaves:       45,080
R2 strict leaves:       23,184
Q2 strict leaves:      339,388
depth-two outer:       263,072
all terminal leaves:  670,724
```

The normalized coordinate-area ledger is exact:

```text
R1 inner:       108625/131072
R2 inner:         5501/65536
Q2 inner:      2993217/131072
outer:             8221/32768
total:                     24
```

Compared with depth 16,

```text
outer: 8157/8192 -> 8221/32768
ratio: 8221/32628 < 1/3
R2 lower area: 19/512 -> 5501/65536
R2 lower-area gain: 3069/65536
```

Thus the unresolved area contracts by more than a factor of three while the
strictly certified R2 area more than doubles.

## Strict R2 pair registry

Every one of the 23,184 strict R2 leaves has a strict unique second collision
owner. Their source/destination labels give exactly

```text
R2 source cores:                 8
source/destination pairs:       16
Round-75 component pairs found: 16/16
new strict pair labels:          0
```

The branch split is

```text
main-branch strict leaves:       23,136
narrow-corner strict leaves:         48
```

All eight narrow-corner pairs, previously visible only through positive
witness boxes and physical curve continuation, now contain strict dyadic R2
leaves. No strict R2 leaf lands outside the 16 Round-75 pair labels.

This is not an all-depth exhaustion theorem. The retained outer area
`8221/32768` could still contain an open component too thin for the current
uniform tree. Consequently the 40 Round-75 residual cells remain unpromoted.

## Three-variable T² Jet

For each Round-75 face, the exact two-collision map is differentiated with a
384-bit Arb second-order Jet in

```text
(source t, source p, moving parameter s).
```

The physical graph is written as `source t = T(source p,s)`. On every one of
the 128 continuation slabs per face, the implicit derivatives `T_p`, `T_s`,
`T_pp`, `T_ps`, and `T_ss` are evaluated from the exact T² Hessian. The signed
moving current density is

```text
rho = (4/25)/sqrt(1-t^2) * partial_s T.
```

F10 uses the rigorous slab envelope

```text
abs(rho) + abs(partial_p rho) + abs(partial_s rho).
```

F13 integrates the full face parameter range, rather than using only a local
witness germ. F16 uses the same bound through the exact area-preserving Piola
flux identity.

## Numeric R2 fields

All 32 physical time-two faces receive actual numeric rows:

```text
F8 common normalized transversality lower:       1/2
F9 integer upper on every face:                    1
F9 32-face sum:                                   32
F10 integer upper on every face:                   1
F10 32-face sum:                                  32
F13 32-face current variation: < 5354421251/250000000000
F16 32-face Piola flux cost:    < 5354421251/250000000000
```

The F8/F9/F10/F13/F16 attachment is therefore complete on the certified R2
face registry. It does not fill the still-unclassified residual atlas.

## Finite cross-rank sums

Combining the 32 Round-72 R1 rows with the 32 new R2 rows under counting
measure gives

```text
faces: 32 R1 + 32 R2
F10 sum: 512
F13 current variation: < 5354429251/250000000000
F16 Piola flux cost:    < 5354429251/250000000000
```

For the explicit finite geometric depth rule

```text
weight(time_j) = 2^(-time_j),
```

the two-rank ledger is

```text
R1 weight: 1/2
R2 weight: 1/4
common F8 lower: 1/5
F9 weighted upper: 11069429950031259185971208
F10 weighted upper: 248
F13 weighted upper: 5354437251/1000000000000
F16 weighted upper: 5354437251/1000000000000
```

This is the first certified finite cross-rank weighted field sum. The weight
is an explicit geometric-depth demonstration, not the physical limiting path
law. It is not used to promote the official global weighted-sum row.

## Gate effect

Round 75's exact physical boundary cancellation on the 72-cell subquotient is
retained. Round 76 adds complete numeric F8/F9/F10/F13/F16 rows on its 32 R2
faces and a finite two-rank weighted sum. Official F17 remains open because
the bulk anisotropic recipient and all-depth suffix bound are absent. F14,
F15, and F18 remain open for the same reasons recorded in Round 75.

```text
complete depth-two physical atlas: not certified
official limiting weighted face sum: not certified
Gate 4: 1/7 landing/join rows
Gate 5: 10/18 fields, complete blocks 0
complete composite gates: 0/5
CM2: NO-GO_FOR_CLAIM
```

## Audit

- Depth-20 terminal leaves: `670724/670724` replayed.
- Strict R2 rows: `23184/23184` replayed.
- Known physical pair labels: `16/16`; new strict pair labels: `0`.
- Numeric R2 rows: `32/32`.
- F8/F9/F10/F13/F16 aggregate replay: pass.
- Residual and numeric generators: cold byte-identical reemit.
- Manifest producer: byte-identical reemit.
- Hostile semantic mutations: `256/256` rejected.
- Strict JSON adversaries: `4/4` rejected.

## Strict frontier

```text
all 16 known R2 pair labels visible at depth 20: certified
32-face numeric F8/F9/F10/F13/F16 registry:       certified
finite two-rank geometric-depth weighted sum:     certified
residual candidate exhaustion:                    not certified
complete fixed-s0 depth-two atlas:                 not certified
official limiting physical path-law sum:           not certified
arbitrary-depth Rn atlas:                          not certified
complete composite gates / CM2:                    0/5 / NO-GO_FOR_CLAIM
```

## Next shortest route

Replace uniform dyadic refinement by a boundary-following residual atlas for
the owner-competition, outgoing-chart, tangency, and destination-face level
sets. Cover every depth-20 outer box by those certified codimension-one
carriers and prove that each complementary open cell has a fixed R1/R2/Q2
label. That is the shortest rigorous route from “no new strict pair at depth
20” to actual residual exhaustion. Afterward replace the demonstration
`2^(-time_j)` weights by the physical path-law/Radon–Nikodym weights and lift
the same ledger to rank three.
