# CM2 Round171 — compact-to-Gate3 source-G coordinate bridge

Date: 2026-07-26

## Decision

Round171 closes the source-G *coordinate-cover* interface.  It proves exact
state agreement between the compact half-angle charts and all four pinned
source-G Gate3 charts.  It does not classify a Gate3 leaf or add a
return-signature disposition.

The source-G state is rebuilt independently as

```text
center_G = (0,0)
R_G      = 9/25
x_G      = center_G + (9/25)n.
```

The source-W position templates in the Round162 infrastructure are not
reused.  The parameter `s` remains in the common product window
`[-1/400,1/400]`; the source-G position, normal, velocity and `p` are exactly
independent of `s`, while target-W centres retain the shift
`x_W=(2i+1)/2+s`.

## Exact four-chart identities

For every chart, with denominator `1+z²`, the compact normal numerators are

```text
E: ((1-z²),  2z)
N: (   -2z, 1-z²)
W: (-(1-z²),  -2z)
S: (    2z,-(1-z²)).
```

They agree coefficient-by-coefficient with the pinned Gate3 normal formulas
under

```text
E,S: t= 2z/(1+z²)
N,W: t=-2z/(1+z²).
```

The quarter-turn normal agrees exactly.  With

```text
p      = 2q/(1+q²)
radial = (1-q²)/(1+q²)
u      = radial*n+p*Jn,
```

the complete velocity numerator tensor agrees coefficient-by-coefficient in
`q⁰,q¹,q²`.  Scaling the normal numerators by `9/25` gives the exact source-G
position numerator.

## Endpoints, seams and grazing

The pinned algebraic endpoint satisfies

```text
kappa² = 1-2kappa,       0<kappa<1.
```

Independent reduction in `Q(kappa)` gives

```text
(2kappa/(1+kappa²))² = 1/2
```

with residue `[0,0]`.  Hence the compact `z` endpoints map to the true
dominant-coordinate boundaries `|t|=1/sqrt(2)`.  The conservative Gate3
bound is strictly wider because

```text
(177/250)²-1/2 = 79/62500 > 0.
```

All four cyclic seams

```text
E(+kappa)=N(-kappa)
N(+kappa)=W(-kappa)
W(+kappa)=S(-kappa)
S(+kappa)=E(-kappa)
```

were independently reduced in `Q(kappa)`.  Normal, quarter-turn normal,
velocity for every `q`, and the source-G position glue exactly.

The endpoints `q=-1,+1` map to `p=-1,+1`.  They remain physical
source-grazing strata, not coordinate singularities.

## Gate3 binding

```text
chart    leaves    unique-first    tangency    multi       leaf-row digest
G:E      16,580          5,276          38   11,266   6d0efa44...2799c491
G:N      16,630          5,340          42   11,248   887de520...5201a8b
G:W      16,580          5,276          38   11,266   49ca4f4d...81639fda
G:S      16,630          5,340          42   11,248   6bd373be...1bf201fd
total    66,420         21,232         160   45,028
```

Every compact source-G state maps into the pinned Gate3 cover.  The wider
rational Gate3 guard bands remain deferred to the exterior reverse-rechart
ledger.

## Exact-key guard

Round171 pins the independently verified Round169 survey and preserves

```text
source-G candidate exact-key envelope          224,580
global geometric exact-key dispositions              0
keys still lacking a global disposition        224,580.
```

No signed wall-word transport or outgoing-chart transport is claimed.  The
coordinate bridge therefore adds zero unresolved-leaf dispositions and zero
exact-key dispositions.

## Verification

The verifier imports or executes no Round171 producer code.  It independently
derives the four normal polynomials from the compact chart axes, reconstructs
quarter turns, velocity and source-G position, reduces all four seams and the
endpoint identity in `Q(kappa)`, rebuilds the complete expected certificate,
and rechecks the Gate3/Round169 censuses.

It rejects:

```text
re-signed semantic mutations    30/30
strict JSON attacks              9/9
path-safety attacks             13/13.
```

Producer and verifier replay byte-identically under two distinct hash seeds
each.

## Strict state

```text
source-G coordinate cover                         CERTIFIED
signed wall-word exact-key transport              NOT CERTIFIED
outgoing-chart exact-key transport                NOT CERTIFIED
source-G global exact-key dispositions            0/224580
all return signatures excluded or connected       false
D02                                                BLOCKED
D03 negative oracle                                UNAUTHORIZED
global Gate5                                       10/18
global complete 18-field blocks                    0
CM2                                                NO-GO_FOR_CLAIM
```

The next shortest interface is the exact `Jx`/`Jy` transformation of signed
wall words and outgoing charts, followed by owner/wall-word/outgoing-chart
materialization on the 21,232 unique-first leaves.
