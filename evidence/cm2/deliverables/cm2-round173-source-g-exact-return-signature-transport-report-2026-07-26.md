# CM2 Round173 — source-G exact return-signature transport

Date: 2026-07-26

## Decision

Round173 certifies the exact `Jx`/`Jy` transport dictionary on the complete
source-G prefix of the immutable Gate5 candidate-key registry.  The contract
transports source chart, target lift, signed integer-wall word and event
order, roof, immutable ordinal, and strict or half-open outgoing chart.

It does not materialize a dynamical row.  In particular, the 21,232
source-G unique-first leaves receive no automatic credit.

```text
source-G Gate5 candidate keys                 224,580
dynamic rows materialized by Round173                0
global geometric key dispositions                    0
keys still lacking a global disposition        224,580
D02                                             BLOCKED
Gate5                                            10/18
complete 18-field blocks                             0
```

## Source-G rebased reflections

The pinned Gate3 atlas describes ambient torus representatives by `1-x` and
`1-y`.  After the exact deck translation that returns the reflected source
to `G[0,0]`, the maps used by the source-G return word are

```text
Jx: (x,y,s,p) -> (-x, y,-s,-p)
Jy: (x,y,s,p) -> ( x,-y, s,-p).
```

This rebasing is essential.  It gives the exact target-lift dictionaries

```text
          G target                 W target
Jx   G[ix,iy] -> G[-ix,iy]    W[ix,iy] -> W[-ix-1,iy]
Jy   G[ix,iy] -> G[ix,-iy]    W[ix,iy] -> W[ix,-iy-1].
```

For source G, a W-centre displacement is
`(ix+1/2+s, iy+1/2)`.  Substitution of `s'=-s` for `Jx` and `s'=s` for `Jy`
checks the displayed relabeling coefficient-by-coefficient for every one of
the 456 generator/pair rows.

## Signed integer-wall words

In the source-G rebased lift, reflection sends an integer wall `k` to `-k`.
For example, under `Jx`,

```text
(qx,hx,k) -> (-qx,-hx,-k)

(-k-(-qx))/((-hx)-(-qx)) = (k-qx)/(hx-qx).
```

Thus every crossing parameter is unchanged.  Strict event order is
preserved, while the displacement sign on the reflected axis reverses:

```text
Jx: X+ <-> X-; Y+ -> Y+; Y- -> Y-
Jy: Y+ <-> Y-; X+ -> X+; X- -> X-.
```

The number of tokens is unchanged, so the Gate5 roof
`r=number_of_tokens+1` is unchanged.  A simultaneous X/Y corner remains in
the pinned cemetery rather than acquiring an artificial order.

## Gate3 and compact charts

The Gate3 chart-coordinate maps are cell dependent:

```text
          E,W cells      N,S cells       p       s
Jx          t              -t           -p      -s
Jy         -t               t           -p       s.
```

The compact half-angle map is different: on all four source cells and for
both generators,

```text
z'=-z,  q'=-q,
```

with `s'=-s` for `Jx` and `s'=s` for `Jy`.  The verifier independently
rebuilds all eight coefficientwise identities

```text
R_generator n_source(z) = n_destination(-z)
```

from the four Round171 normal numerator polynomials.

Strict outgoing charts transform by

```text
Jx: E<->W, N->N, S->S
Jy: N<->S, E->E, W->W.
```

On diagonal chart seams, the pinned half-open owner rule is
`E or W owns; N or S excludes`.  The owner set `{E,W}` is invariant under
both generators, so duplicate traces remain identified rather than added.

## Immutable Gate5 action

The producer and verifier independently rebuild:

```text
retained chart/target pairs, all sources             448
retained source-G chart/target pairs                  228
clean signed crossing patterns                        985
all Gate5 candidate keys                          441,280
source-G ordinal prefix                           224,580
source-G ordinal interval                     0..224,579
```

The pinned full-registry digests are recovered exactly:

```text
pair rows      ccf4e9e42c7b17f6ebb7f33ec707616bb49ec1d755a817ce141dc92d47056f75
pattern rows   2d655b1b83918b0cc42845e465d05f7309657b776f0acbd3d3003e8ae17bb39d
key rows       841cb96798c9bd41e1440c8b2cdd93af5d80f2f64d693f2aa00175a440045ab9
```

For each generator the 228-pair, 985-pattern and 224,580-ordinal maps are
bijective involutions.  The ordinal statistics are

```text
generator    fixed ordinals    two-cycles    permutation-row digest
Jx                        54        112,263    71ffd0a4...63df65
Jy                        54        112,263    4d463d2a...cc1caf
JxJy                       0        112,290    f066155b...3a11e
```

`Jx` and `Jy` commute on every ordinal.  Their Klein-four action has 56,172
orbits:

```text
orbit size 2       54
orbit size 4   56,118
```

The orbit sizes sum exactly to 224,580.

## Legal use and nonpromotion

The pinned direct/reflected Gate3 bindings

```text
G:E --Jx--> G:W    46da8d49...e4a4683
G:N --Jy--> G:S    e91640f1...e4a3aa5b9
```

now have a complete exact return-signature transport contract.  Once a
future computation materializes a direct dynamic row and binds it to its
official Gate5 key, the corresponding reflected row may use this dictionary
without guessing its target lift, signed wall word, ordinal, roof, or
outgoing chart.

The contract itself does not prove that a candidate key is nonempty, select
an owner on a Gate3 leaf, type a grazing/corner event, or exclude an exterior
sheet.  Round169 therefore remains at `0/224580` global dispositions.

## Independent verification

The verifier imports or executes no Round173 producer code.  It reconstructs
the complete expected document and checks exact document equality.  It
rejects:

```text
re-signed semantic mutations    45/45
strict JSON attacks               9/9
path-safety attacks             13/13
```

Producer and verifier replay byte-identically under two distinct hash seeds
each.  The certificate result digest is
`948ab0a8539b08adc96c9493de415b44a5ffb75a1ee3ef47a4742902c211c11f`;
the verification result digest is
`047a580eb546cdb3880b93a9d0358e390d7ce418b371612f8e9fc4b0528f4644`.

