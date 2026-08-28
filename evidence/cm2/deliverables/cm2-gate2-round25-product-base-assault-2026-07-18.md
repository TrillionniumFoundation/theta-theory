# CM2 Gate 2 round 25: actual R1 cone-product anchor and exact nonpromotion frontier

Date: 2026-07-18 (Asia/Shanghai)  
Frozen parent root: `cm2-twenty-fourth-direct-assault-manifest-2026-07-18.sha256`  
Strict verdict: **one actual full-dimensional `RETURN_AT_1_INNER` atom now
carries a strictly interior positive-area affine cone-product tile, an
explicit cone-unstable reference interval, a full interval-indexed affine
cone-stable candidate foliation, its projection, and an exact collision-area
disintegration. These are 7/7 candidate cone-product layers only. The number
of invariant stable-product dynamical layers is 0, and the official Gate-2
score remains 0/17.**

## 1. Actual frozen R1 input

The selected row is not a midpoint sample or a synthetic branch. It is the
first `RETURN_AT_1_INNER` leaf in the complete frozen 33,960-row adaptive
one-step registry:

```text
atom id:
  full-core-step1:2f14a5ba38ba80f0089ec976791bc0760f2ca800bf00dc287883e57407856bc0
raw row SHA-256:
  b6b5bfb29286e65fd568f89893a3ca4fdccd95c7b3f4be54e9b22bbbcc9b6b89
full raw-leaf rows SHA-256:
  1cfd4d6f7fdd57034655fd002e370c5c1c80b2da53bff06e4ff3b7c0f8c71209
source core index: 1
dyadic path:      00000000100000
depth:            14
source box:
  t in [-7/10,-2239/3200]
  p in [-1/50,-3/160]
  s in [-3/1600,-1/640]
classification:  RETURN_AT_1_INNER
```

The source and destination core identifiers are independently rebuilt from
their exact frozen payloads:

```text
source:      chart G:E, t=[-7/10,-69/100], p=[-1/50,1/50],
             target W[0,-1], no transparent crossing
source id:   core:353ad74b3709b7628481fade52784ee19a4a4d159f4eb1b520f42f796455a670

destination: chart W:N, t=[-7/10,-69/100], p=[-1/50,1/50],
             target G[0,1], no transparent crossing
destination id:
  core:0d155400725ff145cad8ec2e7b26a044a629a022f501fa09f9c800c27f05d74f
```

This also closes the component/radius join needed below: the source is the
Gray component and `R_G=9/25`. The verifier independently replays the atom-id
payload, both core-id payloads, the complete-parent first-owner witness, the
strict destination-core witness, and the exact parameter-averaged mass

```text
(9/25)*(1/3200)*(1/800)*(1/3200)/(1/200)
  = 9/1024000000.
```

The upper collision-mass row is independently recovered by multiplying by
`1401/1000`.

## 2. Strictly interior affine cone-product tile

At every parameter in the selected slab, put

```text
t = -4479/6400 + u + v,
p = -31/1600 + (3/2)u - (3/2)v,
|u|,|v| <= 1/25600.
```

The exact margins to the selected R1 atom are

```text
t margin = 1/12800,
p margin = 13/25600.
```

Thus the closed tile is strictly inside the atom in the two collision-phase
coordinates for every `s` in its frozen slab. The Jacobian is

```text
|det d(t,p)/d(u,v)| = 3,
area_(t,p) = 3/163840000.
```

The whole tile therefore inherits the row's complete strict first-collision
owner and its unique time-one return into the displayed destination core.
Nothing is inferred from a center point.

## 3. Cone directions and positive collision mass

In canonical collision coordinates

```text
r=R_G asin(t),  phi=asin(p),
|dphi/dr|=(3/2)*sqrt(1-t^2)/(R_G*sqrt(1-p^2)).
```

The tile obeys `|t|<7/10` and `|p|<499/25600<1/50`. Exact square witnesses
give `sqrt(1-t^2)>7/10` and `sqrt(1-p^2)>49/50`, hence

```text
35/12 < |dphi/dr| < 625/147.
```

The positive `u` direction lies strictly inside the frozen unstable cone;
the negative `v` direction lies strictly inside the frozen stable cone. This
is a geometric cone statement only. It does not establish invariance of
either direction under all future iterates.

Since the collision density is

```text
R_G/sqrt(1-t^2) dt dp,
```

the tile has the strict fixed-parameter lower bounds

```text
unnormalized collision-SRB mass > 27/4096000000,
normalized collision-SRB mass   > 189/187432960000.
```

The normalization uses `pi<22/7` and `R_G+R_W=13/25`.

## 4. Exact affine disintegration, not stable holonomy

Use `v=0` as the reference cone-unstable candidate `I_A^cand`, use the
segments `u=constant` as affine cone-stable candidates, and project by

```text
pi_aff(u,v)=(u,0).
```

Direct change of variables disintegrates collision area with the exact base
density

```text
rho_aff(u)
 = integral_{-1/25600}^{1/25600}
     (27/25)/sqrt(1-(-4479/6400+u+v)^2) dv,

27/320000 < rho_aff(u) < 37827/320000000.
```

This is an exact affine area disintegration. It is deliberately not typed as
the conditional Jacobian of physical stable holonomy: the affine fibres have
not been proved to be invariant local stable manifolds, and `pi_aff` has not
been identified with `pi^s`.

## 5. Why the new return tail does not close Gate 2

The round-24 `C24` exponential return tail controls the event

```text
no return to C24 by collision time n.
```

A spanning stable plaque instead needs uniform control of a different event:
distance from every future singularity cut, plus an invariant graph-transform
domain. The two event carriers have not been identified. Existing qualitative
Young-rectangle/absolute-continuity theorems also do not bind their rectangles,
plaque spans, or conditional Jacobian constants to this exact atom, parameter
slab, and R1 branch registry.

The minimal missing interface remains:

1. a positive spanning length and actual local stable plaques across this
   tile;
2. an infinite homogeneous future domain for every registered plaque;
3. explicit separation and contraction constants `C_sep, lambda_s<1`;
4. a uniform Hölder modulus for `log J^u T` along paired stable orbits;
5. the convergent holonomy-product bound and its two-sided Jacobian estimate;
6. connected stable-saturated first-return strips compatible with the same
   registered branch identifiers.

## 6. Exact maturity boundary

The seven certified candidate cone-product layers are:

```text
1. positive two-dimensional physical R1 anchor
2. strict inner cone-product tile
3. explicit cone-unstable interval I_A^cand
4. interval-indexed cone-stable affine candidate leaves
5. affine candidate projection pi_aff
6. positive exact affine area disintegration rho_aff
7. same unique physical one-step C24 return branch on the whole tile
```

The score `7/7` refers only to that candidate-interface list. It is not an
official Gate-2 score. The strict boundary is

```text
candidate cone-product layers:                 7/7
invariant stable-product dynamical layers:     0
official immutable Gate-2 physical fields:     0/17
Gate 2:                                        NOT_CERTIFIED
CM2:                                           NO-GO FOR CLAIM
```

In particular, the affine candidate does not promote the first four Gate-2
fields (`Lambda_A`, physical `I_A`, `pi^s`, conditional holonomy Jacobian),
so none of the downstream quotient, stopping, near-collision, or moment
fields can be promoted either.

## 7. Fail-closed replay

The verifier does not import the producer. It independently reconstructs the
actual atom row, core ids, cone bounds, area, mass, density, all 17 immutable
field statuses, and the internal digest. It rejects duplicate JSON keys,
non-finite numbers, malformed JSON, shape changes, hash substitutions, input
rewrites, geometric promotions, and score promotions. Its hostile suite is
`67/67`.

```bash
python -m py_compile \
  deliverables/cm2_gate2_round25_product_base_cert.py \
  deliverables/cm2_gate2_round25_product_base_verifier.py

python deliverables/cm2_gate2_round25_product_base_verifier.py --integrity-only
python deliverables/cm2_gate2_round25_product_base_verifier.py --replay
python deliverables/cm2_gate2_round25_product_base_verifier.py --self-test

# Expected fail-closed live verdict and process exit status 2.
python deliverables/cm2_gate2_round25_product_base_verifier.py

sha256sum -c \
  deliverables/cm2-gate2-round25-product-base-manifest-2026-07-18.sha256
```
