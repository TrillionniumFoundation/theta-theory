# CM2 Round 73: shared base-R1 subdivision/incidence quotient

Date: 2026-07-21

## Scope and verdict

This round closes the finite shared quotient of the `96` stationary faces and
`32` certified pullback components on the actual `s=0`, depth-1 union of the
`24` physical core rectangles. It does not promote the construction to
depth 2, arbitrary rank, or the limiting weighted tower.

The composite verdict remains `0/5`; CM2 remains `NO-GO_FOR_CLAIM`.

## Certified vertices

For each of the `16` positive return cells, the two pullback components meet
once in the core interior and meet two stationary core faces once each.

- `32/32` stationary/pullback endpoints are enclosed by 90-step rational
  sign-changing brackets.
- `16/16` pullback/pullback intersections are enclosed by strict interval
  Krawczyk inclusions using Arb collision-map jets.
- Each positive cell is therefore a curvilinear quadrilateral with one
  original core corner, two stationary/pullback endpoints, and one interior
  pullback/pullback vertex.

The frozen vertex proof is
`cm2-round73-base-r1-quotient-vertices-2026-07-21.json`.

## Shared quotient

The `32` stationary faces hit by pullbacks split once. The other `64`
stationary faces remain unsplit. Hence

```text
stationary segments: 64 + 2*32 = 128
pullback edges:                      32
all quotient edges:                160
```

The vertex and cell counts are

```text
original core corners:              96
stationary/pullback endpoints:       32
pullback/pullback intersections:     16
all quotient vertices:              144

survival two-cells:                  24
positive return two-cells:           16
all quotient two-cells:              40
```

The exact Euler audit is

```text
V-E+F = 144-160+40 = 24,
```

which equals the number of disjoint core rectangles. This independently
checks the complete finite subdivision.

## Field attachment and cancellation

The Round-72 numeric rows attach without relabeling:

```text
F10 sum on 32 pullbacks:                 480
F13 total current variation:             <4/125000000
F16 total Piola flux cost:                <4/125000000
```

On the cellular quotient, `partial_1 partial_2=0`. In the oriented boundary
sum of all `40` two-cells, every one of the `32` pullback edges occurs twice
with opposite orientations and cancels before total variation is taken.
This closes the base-fibre boundary sector of the F17 quotient route and
removes the artificial duplicate-trace cost there.

## F14/F15/F17 attack

No official field is promoted:

- F14 still lacks a recovered strong block even though the base-fibre F10
  integer sum is now `480`.
- F15 still lacks the raw/Orlicz recovery and positive cemetery sectors.
- F17 now has exact base-fibre internal boundary cancellation, but its bulk
  sector still lacks an all-input anisotropic vector-current recipient and a
  billiard-specific suffix bound.
- F18 still lacks a single all-depth block carrying all 18 fields.

Thus Gate 5 remains `10/18`, complete blocks remain `0`, and the full
composite gate count remains `0/5`.

## Audit

- Arb/Krawczyk proof cold reemit: byte-identical.
- Quotient producer reemit: byte-identical.
- Independent quotient replay: `16/16` cells, `32/32` endpoint brackets,
  `16/16` Krawczyk boxes, Euler identity pass.
- Hostile semantic mutations: `120/120` rejected.
- Strict JSON adversaries: `4/4` rejected.

## Next shortest route

Lift the same chart-aware interval/Krawczyk engine to the actual depth-2 path
registry, construct the first nontrivial cross-rank quotient map, and test
whether its internal oriented trace cancellation survives the rank join.
Only after that can the finite F10/F13/F16 sums be assigned a genuine rank
weight and used toward F14/F15/F17 rather than remaining base-fibre data.
