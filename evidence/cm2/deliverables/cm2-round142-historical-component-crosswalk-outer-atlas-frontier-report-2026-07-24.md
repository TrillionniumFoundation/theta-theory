# CM2 Round142 historical-component crosswalk / outer-atlas frontier

Date: 2026-07-24

Formal status:

```text
CERTIFIED_HISTORICAL_ENUMERATION_UNDERDETERMINATION_AND_OUTER_ATLAS_FRONTIER
```

This is a fail-closed frontier result.  It proves a new obstruction and
freezes the exact prospective outer-atlas/negative-oracle contract.  It does
not construct the maximal Round27 component, compute a historical rank, or
mint a `c24-component` ID.

## 1. Exact historical-definition audit

Round27 defines the rank as:

```text
least natural-number index in a fixed bijective enumeration of rational
dyadic basis elements whose closure is contained in the component
```

The frozen Round27 bytes do not give the enumeration.  In particular, they
contain no executable:

```text
enumeration ID or digest
basis-row encoding
coordinate normalization
zero/one-based index origin
ordering or seed
rank function
unrank function
```

Round137 had already recorded these absences.  Round142 checks them again
against the pinned Round27 object and proves that this omission is
identifiability-critical, not merely a missing implementation.

## 2. Two-model underdetermination proof

The Round140 basis box at level 5883 has closure strictly inside the
positive-area R1648 seed cell.  Round142 independently recomputes its v1 rank,
subdivides it, and certifies two distinct primitive level-5884 basis boxes
whose closures remain inside the same maximal component `U`.

It also constructs the primitive level-5 box

```text
[5,30,31,8,9]
```

and verifies that its closure contains the complete normalized Round139 D0
collar enclosure, hence the exact collision-3 D3=0 endpoint.  That endpoint
is excluded from the regular path fibre, so this box's closure is not
contained in `U`.

These witnesses admit two fixed bijections satisfying the exact Round27
sentence:

```text
E0: index 0 -> inside box A
E1: index 0 -> D0-crossing outside box, index 1 -> inside box A
```

Each finite injective prefix extends to a bijection of the countably infinite
dyadic basis.  Therefore the least index is 0 in `E0` and 1 in `E1`
(respectively 1 and 2 under a one-based convention).  The ambiguity is
independent of the indexing-origin convention.

```text
ambiguity proof ID:
round142-historical-enumeration-underdetermination:
6d68f69bd4f7774b417bbeb5a7481636f3dc72c780b205deb8f18bce88ef649f
```

Consequently, no geometric computation—not even a complete outer atlas—can
recover a unique historical Round27 numeric rank from the frozen bytes.

## 3. Only legal schema remediation

The historical label must not be invented and Round137-v1 must not be called
a crosswalk to the unnamed enumeration.

The only legal remediation available from the present record is a versioned
superseding component-ID schema that explicitly adopts the
`round137-dyadic-basis-enumeration-v1` normalization, row encoding, zero-based
rank/unrank functions, and digest.  Such a schema change must migrate every
downstream consumer that embeds the component identity, including the
Round35 restriction/parent-W and image-recut chain and the Round50, Round54,
and Round67 owner/token/Omega/q_j chains.

Until that migration is explicitly authorized and certified, all historical
Round27 ranks and `c24-component` IDs remain null.

## 4. Geometric blocker kept separate

Under a prospective v1 schema, leastness still needs:

1. a positive basis-box membership witness;
2. a complete outer enclosure `U subset O`;
3. a symbolic proof that no earlier v1 basis-box closure is contained in
   `O`.

For one rational outer rectangle, the third step is level/lex arithmetic:
compute the earliest primitive v1 box strictly inside the outer rectangle.
For a finite cell union, it is an exact dyadic-box subset query against the
exhausted atlas.  This is the frozen negative-oracle contract; it does not
brute-force every earlier integer rank.

The current certified global outer enclosure is only the normalized source
chart `(0,1)^2`, whose earliest v1 rank is 0, while the current positive
upper-bound rank has 23,530 bits.  It therefore closes none of the negative
gap.

The centered-jet atlas contract now fixes:

```text
leaf coordinate:       x=sqrt(17)*r, r=(4/25)*asin(t)
transverse coordinate: beta=(asin(p)-4r)-b_star
generators:            (delta_x, delta_beta)
seed cells:            1
complete 2D cells:     0
complete adjacencies:  0
complete event faces:  0
```

Every future cell must carry all 1,648 owner/official-word decisions,
nonreturn/return decisions, chart/homogeneity/incidence/core margins, event
Jacobians, and determinant/transversality ledgers.  Every open frontier must
be continued or classified as a physical event face.  The exact D3=0
collision-3 endpoint is certified only on the leaf and is not promoted to a
complete two-dimensional face.

The first geometric oracle after prospective-v1 adoption is therefore:

```text
a complete validated two-generator centered-jet outer atlas with exhausted
event frontier
```

## 5. Independent verification

The verifier does not import or execute the producer.  It independently
rebuilds the critical objects from byte-pinned Round27/137/139/140 inputs.

```text
formal verification:            PASS
semantic mutations rejected:    34/34
strict JSON attacks rejected:     7/7
in-process path attacks rejected: 8/8
process hostile I/O attacks:     17/17
dual producer hash seeds:        byte-identical
dual verifier hash seeds:        byte-identical
```

## 6. Strict state

```text
historical Round27 component ranks / IDs: 0
complete maximal-component outer atlases: 0
complete 2D centered-jet atlas cells:      0
Round35 restrictions:                     0
Round50 owners / Round54 tokens:           0
Round67 Omega_j records / q_j outputs:     0
global complete 18-field blocks:           0
Gate5 global maturity:                 10/18
Gate5:                          NOT_CERTIFIED
CM2:                         NO-GO_FOR_CLAIM
```
