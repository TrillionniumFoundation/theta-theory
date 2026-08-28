# CM2 Round146 physical centered-jet 2D frontier

Date: 2026-07-24

## Result

Round146 certifies a local physical two-dimensional R1648 seed atlas and
the first collision-three D0-candidate zero in the positive-`delta_beta`
direction.  The exact certificate status is

```text
CERTIFIED_LOCAL_PHYSICAL_2D_SEED_CELL_AND_TRANSVERSE_D3_EVENT_FRONTIER__D02_STILL_BLOCKED
```

This is deliberately local.  It does not certify a maximal
two-dimensional H1 component, exhaust every component exit, or close
Round144 node D02.

## Physical coordinates

The two genuine physical generators are

```text
delta_x    = x - x_star,              x = sqrt(17) r
delta_beta = (asin(p) - 4 r) - b_star
```

The exact initial map is

```text
t = sin(asin(t_star) + delta_x/(R_W sqrt(17)))
p = sin(asin(p_star) + 4 delta_x/sqrt(17) + delta_beta).
```

The numerical enclosure of `t_star` is charged to the initial interval
remainder; it is not treated as a third parameter.  The angle-coordinate
Jacobian is

```text
[ 1/(R_W sqrt(17))    0 ]
[ 4/sqrt(17)          1 ]
```

with determinant `1/(R_W sqrt(17)) > 0`, so the physical parameter rank is
exactly two.

## Connected two-cell atlas

Let `h = 2^-4296`.  Both certified cells use

```text
delta_x in [-2h,-h].
```

Their transverse intervals are

```text
negative cell: delta_beta in [-3h,-h]
central cell:  delta_beta in [ -h, h].
```

They meet on the exact artificial face `delta_beta=-h`.  The adjacency
graph is the path on two vertices, with identifiers

```text
atlas:
round146-local-physical-2d-two-cell-atlas:
e47b52e4580d12fb35fffa627e89640308586fa76b8056448068fb5d6b73fcce

negative cell:
round146-physical-2d-cell:
e415d8526bfba4fd94ec5e6fd8e668731197aef7293405f99922508398e1ade5

central cell:
round146-physical-2d-cell:
ff9cfb4990a38f017b3fbbad9bcf6f1eaef9fa84edd7f4569f7830cba756f8e3

shared face:
round146-artificial-shared-beta-face:
ad7a2d1880e0f5ea4447f48c239de71d66f4681adad150788c351a39499dfc0d
```

Each cell independently passed all 1,648 collision stages:

- the complete radius-four universe of 161 candidates per stage;
- retained owner, official word, outgoing chart and strict event ordering;
- `H0_CENTRAL` homogeneity at all 1,648 stages;
- incidence rank 14 at all 1,648 stages;
- 1,647 strict nonreturns and one strict terminal return to the frozen
  destination core.

The official word SHA256 is
`f504289edce554d47e17a90d7c886586a69f3ec4b64fafd90c718c50ca93221e`;
the compact path SHA256 is
`c37571201fa15065a7f8e4eeec9df5a79f36e077feac37a1aec7b910970e1f17`.
The Round27-compatible 1,648-word tuple SHA256 remains
`5cec1061ec331e8f37929dfb1b2b2a78757309ba60198d571abd9e8cf6c70ed9`.

The negative and central radius-ledger hashes are respectively

```text
06c81e504a7cb791dc5b7690f4b071c63ad85b4733e9608608b21bb635a459b3
b1ae4b21f8007e2056ef21b6a2b72542d77ffc6232c00430d34d51f6cf95533b
```

with worst dyadic depths 4,291 and 4,292.  Both terminal state-radius
exponent vectors are `[-16,-16,-13,-13]`.

## Positive transverse event frontier

On the whole certified upper face `delta_beta=h`, the collision-three
`W[0,0]` D0 discriminant `D3` is strictly negative.  On the event box

```text
delta_x    in [-2h,-h]
delta_beta in [ 2h, 6h]
```

interval differentiation gives

```text
partial D3 / partial delta_x       approximately 32.93856964046068 > 0
partial D3 / partial delta_beta    approximately 11.73432390816745 > 0
implicit graph slope               approximately -2.807027477529782 < 0.
```

The parametric interval-Newton image, in units of `h`, is approximately

```text
[2.807027457281947, 5.614054976031184],
```

strictly inside `[2,6]`.  The central-`delta_x` single Newton estimate is
approximately `4.210541216294673 h`.  Thus there is exactly one
`delta_beta` root for each fixed `delta_x` in the event box, and the event
curve is transverse to the `delta_beta` fibres.

The whole corridor `delta_beta in [h,6h]` has both partial derivatives
strictly positive; `D3` is negative at the certified upper/frontier face
`delta_beta=h` and at the event-box bottom.  Therefore no earlier zero of
this same collision-three D0 candidate family lies between the certified
face and the interval-Newton event graph.

The adjacent positive cell `delta_beta in [h,3h]` is only certified as
event-entering.  No complete 1,648-step frozen-owner path is claimed on
that cell.  The event is not claimed to be first among all physical event
families and is not a global exhaustion of the component frontier.

## Counts

```text
physical parameter generators                 2
complete physical 2D cells                    2
exact internal shared faces                   1
collision-stage/cell pairs                3,296
complete radius-four candidate tests    530,656
preterminal strict nonreturn pairs        3,294
terminal strict-return cells                  2
local transverse event graphs                 1
global complete 18-field blocks               0
```

## Frozen core hashes

```text
Round146 engine       ac332c1cc99c96a56251a53b2432caaba951f028de810045d840b8991bdf27eb
Round146 producer     db0241c9bae4937cd1a01f23b4951247fa69fd16d9b06a75d446e5336c9930c4
Round146 certificate  38ad7cdd5a2af7cda94792a31a8a83275022f943e8e6b9801ee4bece73b04eac
certificate result    66936a51409bbe87ef2a10e80f081d345954c8104a23a4a05a21019f0d3b0e67
Round146 verifier     d75af7cc251c212a11522a8884ad9afbb983197ba9e6e0d43598ffe06916ad44
formal verification  c25646413467deb2c1c5ea68f92e97116546eb62333596afc61973430e002dd4
verification result   7d2fa9fdaff97bf1267ebf9c03a31f38145badeab7410c136f91aaeab3f929d7
```

## Strict global nonpromotion

The two local cells and one local event graph do not exhaust the outer
atlas, exits or event frontiers of a maximal two-dimensional component.
Round144 D02 remains `BLOCKED`; the D03 least-rank negative oracle is not
authorized.

All historical Round27/Round35 ranks, the natural short-cell index `k`,
and the component, interval, parent-W, image-recut and restriction
identifiers remain null.  No Round50 owner, Round54 token or Round67 `q_j`
is emitted.

```text
Gate5 maturity                  10/18
complete 18-field blocks             0
Gate5                    NOT_CERTIFIED
CM2                 NO-GO_FOR_CLAIM
```
