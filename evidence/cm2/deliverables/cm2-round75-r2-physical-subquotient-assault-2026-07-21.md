# CM2 Round 75: physical R2 continuation and depth-two subquotient assault

Date: 2026-07-21

## Scope and verdict

This round replaces the Round-74 dyadic R2 witnesses by actual physical
time-two pullback curves on all 16 certified source/destination branches. It
certifies their endpoints, owner qualification, continuation, pairwise
nonintersection, cross-rank incidence, and oriented trace cancellation on a
finite depth-two physical subquotient.

The construction is deliberately not promoted to a complete fixed-`s=0`
depth-two atlas: additional R2 components may remain inside the Round-74
residual outer. Composite gates remain `0/5`; CM2 remains
`NO-GO_FOR_CLAIM`.

## Owner-chart separated T² equations

For each of the 8 main and 8 narrow-corner R2 branches, the exact fixed-`s=0`
time-two map is evaluated as

```text
source W core -> strict time-one G hit -> physical second owner W[0,0]
```

At the destination, the active `t` side and active `p` side give two scalar
level equations. Their source preimages are the two physical boundaries of a
boundary-attached R2 band. Every curve joins one source stationary `t` side
to one source stationary `p` side.

Outgoing-chart seams are not assigned arbitrarily. Where the ordinary chart
classifier is unresolved, all four outgoing-chart candidate lists are
unioned and the same physical winner `W[0,0]` is proved strictly earlier than
every competitor. The exact qualification ledger is

```text
curves using chart-free owner proof somewhere: 16
curves using it on every slab:                   8
chart-free owner slabs:                       1360
scan/bisection continuation fallbacks:           0
```

Thus a chart seam changes only the proof coordinate, not the physical second
collision owner.

## Physical curve continuation

Each curve has two rational endpoint brackets, one on each source stationary
side. A 4,096-cell sign scan followed by 90 exact rational bisections gives
opposite endpoint signs for all `64/64` endpoint vertices.

Every curve is then continued across 128 parameter slabs with 384-bit Arb
parametric interval Newton. On every slab the proof checks:

- strict interval-Newton inclusion in the source coordinate interval;
- a nonzero fixed sign for the level derivative;
- strict survival through time one;
- strict unique physical second owner, with chart-free union where needed;
- strict destination chart membership; and
- strict interior membership of the other destination coordinate.

The resulting atlas is

```text
certified R2 band components:       16
physical R2 boundary curves:        32
stationary endpoint vertices:       64
strict interval-Newton slabs:     4096
unresolved slabs:                    0
```

This is the first actual physical R2 face registry attached to the same
fixed-parameter quotient as the R1 faces.

## Pairwise nonintersection

Each affected source core contains four R2 curves: two main-branch faces and
two narrow-corner faces. All six unordered pairs on each of the eight source
cores are excluded by a separate 384-bit Arb adaptive tree:

```text
source cores:                   8
curve pairs:                   48
certified nonintersections:    48
Arb box tests:              24752
excluded terminal leaves:   12400
maximum binary depth:          21
unresolved intersections:       0
```

Consequently all 16 bands are embedded, disjoint physical components and
the 32 curves can be inserted into the Round-73 quotient without an
unclassified crossing vertex.

## Depth-two physical subquotient

Round 73 starts from

```text
V=144, E=160, F=40
```

The 64 distinct stationary endpoints each split one stationary segment.
Adding the 32 pairwise-disjoint physical R2 crosscuts then adds 32 edges and
32 two-cells. The refined physical subquotient therefore has

```text
stationary segments:       192
R1 + R2 pullback edges:     64
V=208, E=256, F=72
Euler: 208-256+72=24
```

The Euler value remains the 24 disjoint physical core rectangles. Its cell
ledger is

```text
certified R1 cells:           16
certified R2 band cells:      16
residual complement cells:    40
all two-cells:                 72
```

The 40 residual cells are not relabelled as Q2. They retain the possibility
of additional R2 components that were not selected by the 16 Round-74
witness branches.

## Cross-rank incidence and physical cancellation

All 16 R2 bands receive an actual same-source-core Round-73 survival parent;
their 32 boundary curves provide 32 curve-to-parent incidence edges and 64
one-sided trace records.

In the oriented sum of all 72 cell boundaries, every internal physical
pullback edge occurs once with each orientation:

```text
Round-73 internal R1 pullback edges:       32
Round-75 internal R2 pullback edges:       32
physical opposite-orientation pairs:      64/64
duplicate trace cost before total variation: 0
```

This upgrades the Round-74 artificial dyadic cancellation to actual physical
trace cancellation through the first rank join. The scope is exactly the
certified 72-cell subquotient, not an exhaustive or all-depth quotient.

## F17 and gate effect

The F17 boundary sector now has a concrete depth-two physical recipient:
all 64 internal R1/R2 pullback traces cancel before total variation. Official
F17 is not promoted because the all-input anisotropic current recipient and
the all-depth suffix bound remain absent. F14 still lacks a recovered strong
block; F15 still lacks raw/Orlicz recovery and a positive cemetery; F18 still
lacks a single all-depth 18-field block.

Accordingly:

```text
Gate 4: 1/7 landing/join rows, not certified
Gate 5: 10/18 fields, complete blocks 0
complete composite gates: 0/5
CM2: NO-GO_FOR_CLAIM
```

## Technology audit

Round 74 identified arXiv:2602.07718's generalized interval-Krawczyk surface
certification as the relevant recent algorithmic direction. This round uses
the concrete one-equation/two-variable specialization directly: the physical
T² level equation is covered by parametric interval-Newton inclusions, while
collision ownership and chart seams are certified independently. No generic
surface theorem is treated as a billiard result and no gate is promoted from
the paper alone.

## Audit

- Physical R2 components: `16/16` replayed.
- Physical boundary curves: `32/32` replayed.
- Rational endpoint brackets: `64/64` replayed.
- Parametric interval-Newton slabs: `4096/4096` replayed.
- All same-source curve pairs: `48/48` excluded.
- Unresolved physical intersections: `0`.
- Hostile semantic mutations: `224/224` rejected.
- Strict JSON adversaries: `4/4` rejected.
- Manifest producer: byte-identical reemit.
- Curve and nonintersection proof generators: cold byte-identical reemit.

## Strict frontier

```text
16 actual physical R2 components:              certified
32 actual time-two pullback faces:              certified
72-cell depth-two physical subquotient:         certified
physical trace cancellation through rank join: certified on subquotient
complete fixed-s0 depth-two face atlas:         not certified
arbitrary-depth Rn atlas:                       not certified
limiting weighted rank/path sum:                not certified
Gate 4 / Gate 5:                                1/7 / 10/18, blocks 0
complete composite gates / CM2:                 0/5 / NO-GO_FOR_CLAIM
```

## Next shortest route

Enumerate every remaining destination-face candidate in the 40 residual
cells and use the same owner-qualified interval engine to certify exclusion
or continuation. This decides whether the current 16 bands exhaust the
fixed-`s=0` depth-two R2 atlas. In parallel, attach numeric F8/F9/F10/F13/F16
rows to the 32 R2 faces so the first finite cross-rank weighted face sum can
be audited rather than only its oriented boundary cancellation.
