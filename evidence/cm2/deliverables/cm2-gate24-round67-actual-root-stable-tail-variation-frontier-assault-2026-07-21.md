# CM2 Round 67 Gate 2/4 — actual-root, stable-tail and variation frontier

Date label: 2026-07-21

Strict verdict: **this leaf constructs the first graph-supported positive
physical pre-registry on one frozen `RETURN_AT_1_INNER` tile: the same root
now carries its complete first-collision owner, source collision coordinate,
time-one landing, affine cone-product coordinate and persistent material
tag.  It also gives the exact collision-SRB disintegration of that keyed
affine chart, an exact conditional-hazard criterion for a positive all-depth
stable survivor, and a necessary-and-sufficient fixed-material weighted-BV
Piola multiplier criterion.  The affine fibres are not invariant stable
plaques, the actual 96-word stable-plaque anchor is a different frozen root,
and no crosswalk to the common landing marker is available.  Therefore no
actual stable-tree row is complete: Gate 2 remains `0/17`, Gate 4 remains
`1/7` with fields 1, 4 and 7 partial, the actual tree remains `0/7`, and CM2
remains `NO-GO_FOR_CLAIM`.**

## 1. Append-only scope

This Round-67 leaf pins the Round-66 aggregate and independent audit, the
Round-66 Gate-2/4, material-trace and immutable-registry leaves, and the
direct physical collision/product/marker/branch inputs used below.  It does
not modify any frozen artifact and does not identify records merely because
their marginal laws or informal names agree.

Two positive physical anchors must be kept distinct:

```text
Round-25 R1 tile:
  positive three-parameter root, exact affine collision disintegration,
  complete one-step owner and landing branch; no invariant stable plaque

Round-15 / Round-59 96-word strip:
  one validated actual stable-plaque crossing and a positive-width strict
  96-collision continuation strip; no stable saturation or product quotient
```

No frozen identifier or Borel crosswalk says these are the same root.  The
new construction uses the first anchor exactly and retains the second as a
separate finite-depth input.

## 2. A graph-supported actual owner/collision/material pre-registry

### 2.1 The physical root law

Use the exact Round-25 root

```text
S=[-3/1600,-1/640],       I=V=[-1/25600,1/25600],
t=t0+u+v,                 t0=-4479/6400,
p=p0+(3/2)(u-v),          p0=-31/1600,
R_G=9/25.
```

The map `(u,v)->(t,p)` has determinant `-3`, and the entire closed root
lies strictly inside the same frozen first-owner atom.  In the canonical
collision coordinate `r=R_G asin(t)`, the physical invariant section law is
flat in `(r,p)`.  Thus, up to its single harmless normalization scalar, the
pullback positive law is

```text
dLambda_0 = 3 R_G / sqrt(1-t(u,v)^2) ds du dv.        (2.1)
```

It has positive finite mass.  The frozen fixed-parameter lower bound is
`27/4096000000`; after the frozen parameter averaging over this slab it is
still at least `27/65536000000`.

From every `(s,u,v)` define, deterministically,

```text
owner = (frozen atom ID, s, source core, RETURN_AT_1_INNER, half-open owner),
x     = (r,p) on the Gray collision section,
y     = T_s(x) in the frozen destination core,
prod  = (u,v),
mat   = (s, Gray source, West destination, depth 1, persistent branch).
```

The joint pushforward is supported on all five equality graphs by
construction.  It is therefore an actual graph-supported root certificate,
not an abstract gluing of marginals.  Its exact scope is deliberately named
a **pre-registry**: its owner is the Round-25 complete first-collision owner,
not the later Round-50/58 owner/root law; `(u,v)` is a cone-product chart,
not an invariant stable product; and its landing has not been crosswalked to
the common marker `kappa_B`.

### 2.2 Exact keyed collision-SRB chart formulas

For fixed `s`, regard `v` as the candidate plaque label and `u` as its root
coordinate.  In `(r,p)` put

```text
Phi(u,v)=(R_G asin(t0+u+v), p0+(3/2)(u-v)),
q(u,v)=3 R_G/sqrt(1-t^2),
a(u,v)=sqrt(R_G^2/(1-t^2)+9/4),
Z(v)=3 R_G[asin(t0+h+v)-asin(t0-h+v)],
h=1/25600.                                             (2.2)
```

The candidate conditional arclength density and the root-coordinate
holonomy formulas are exactly

```text
rho_v(u)=q(u,v)/(Z(v)a(u,v)),
lambda_(v,w)(u)=a(u,w)/a(u,v),
J_(v,w)(Phi(u,w))=q(u,v)Z(w)/(q(u,w)Z(v)),             (2.3)
J rho_w = rho_v/lambda.
```

Unlike Round 66's abstract chart formula, (2.2)--(2.3) are now attached to
one actual owner/collision root.  Their stable meaning is still conditional:
the lines `v=constant` and `u=constant` were certified only as cone
candidates.

The affine `(t,p)` derivative has squared singular values `2` and `9/2`.
Consequently, if a future same-key graph-transform chart differs from this
affine map by a Lipschitz error `epsilon<sqrt(2)`, it is globally injective
on the convex tile and has lower Lipschitz constant `sqrt(2)-epsilon`.
This is the exact quantitative chart-upgrade interface; the needed error row
is not frozen.

On the candidate chart `8957/12800<=|t|<=8959/12800`.  Direct rational
algebra gives

```text
(a_+/a_-)^3 < 101/100.                                (2.4)
```

Thus, if the same chart were proved physical stable and the marker fields
were supplied, the strict path budget would follow from the clean sufficient
row

```text
101 F R < 100 C_p theta L.                            (2.5)
```

No value among `F,R,theta,L` is presently available for the common marker,
so (2.5) is a sharp typed target, not a promotion.

## 3. Full first-failure tails: exact conditional hazards

Let `S_N` be the same-key root set on which the required stable chart
survives through depth `N`, let `F_N=S_(N-1)\S_N`, and, while
`eta(S_(N-1))>0`, define the conditional first-failure hazard

```text
h_N=eta(F_N)/eta(S_(N-1)).                             (3.1)
```

Then for every finite `N`, exactly

```text
eta(S_N)=eta(S_0) product_(n=1)^N (1-h_n).             (3.2)
```

Hence the all-depth survivor has positive mass if and only if no hazard is
one and

```text
sum_n h_n < infinity.                                 (3.3)
```

This criterion is sharper than summing unconditional failure upper bounds
because it is intrinsic to the surviving physical law.  It also separates
two superficially similar tails exactly:

```text
h_n=1/(n+1)^2: product through N=(N+2)/(2(N+1)) -> 1/2;
h_n=1/(n+1):   product through N=1/(N+1) -> 0.
```

For a fail-closed audit, split every full failure lexicographically into
collision singularity, graph-transform/domain, and registry/key loss.  The
96 frozen rows set only the collision component to zero.  They give no
upper row for either other component, even at depth one.  Thus the number of
actual **full** hazard rows remains zero and the sharp actual survivor lower
bound remains zero.

The hazard formulation does identify the shortest lawful future input:
same-root bounds `h_n<=b_n<1` with `sum b_n<infinity`.  A return-time tail,
one-step spatial tube bound, or collision-shadow row cannot be substituted
unless it is first pushed to these full conditional hazards on the same
root.

## 4. Marker saturation, variation and a sharp fixed-material recipient

On a genuine all-depth chart the actual marker must satisfy

```text
g(u,v)=g_bar(u) almost everywhere                     (4.1)
```

on the common root.  This is equivalent to `P_eta=0` and to zero stable
marker defect on a spanning holonomy tree.  The pre-registry of Section 2
does not carry `g_B`, so it cannot test (4.1).  Even if (4.1) were true, it
would give no variation estimate on `g_bar`.

A precise strong recipient can nevertheless be frozen.  On a finite
interval `I` use

```text
||f||_BV=||f||_1+Var(f),
Y=ell^1_a(BV(I)),
M_q f=(q_r f)_r,
S_q=sum_r a_r ||q_r||_BV.
```

Then

```text
M_q:BV(I)->Y is bounded  iff  S_q<infinity,            (4.2)
S_q/|I| <= ||M_q|| <= 2 max(1,|I|^-1) S_q.            (4.3)
```

Necessity is obtained by applying the operator to `1`; sufficiency is the
one-dimensional BV product inequality.  More strongly, for a moving
coefficient family

```text
q_r(s)=q_r(0)+s qdot_r+R_r(s),
```

operator-norm differentiability into this recipient holds if and only if

```text
sum_r a_r ||R_r(s)||_BV = o(|s|).                     (4.4)
```

This is an exact weighted Piola remainder criterion, not merely sufficient.
For the replay `I=[0,1]`, `(q_1,q_2)=(x,1-x)` and weights `(1,2)`, one has
`S_q=9/2` and `9/2<=||M_q||<=9`.

Round 66 supplies a genuine `C^2` physical material atlas and local
`O(s^2)` Piola remainder on every compact persistent depth-96 core.  Thus
the finite local coefficient analogue of (4.4) is available there.  It is
not on the Round-25 root, not all-depth, not weighted over topology changes,
and not intertwined with the requested anisotropic current space.  The
global physical sum in (4.4) therefore remains `NOT_CERTIFIED`.

## 5. Current technology boundary

An official arXiv API search was rerun on 2026-07-21.

- `arXiv:2502.07765v2` gives a CLT with error bounds for sequential systems,
  including sequential dispersing billiards, through projective cones.  It
  supplies neither the present stable-product root nor a moving-boundary
  strong Piola remainder.
- `arXiv:2104.06947v3` develops projective cones for sequential dispersing
  billiards.  Its memory-loss machinery starts from standard-family inputs;
  it does not manufacture the missing common marker saturation or physical
  material recipient.
- `arXiv:2604.25881v1` concerns the billiard measure of maximal entropy,
  not the collision-SRB marker law.
- `arXiv:2402.02496v2` treats local product structure for smooth
  diffeomorphisms of closed manifolds, not the singular collision atlas.

No external theorem is promoted.

## 6. Strict frontier

```text
actual positive owner/source/landing/material pre-registry: CERTIFIED_LOCAL
same-root exact affine collision-SRB disintegration:         CERTIFIED_EXACT
candidate RN/arclength formulas and chart-upgrade criterion: CERTIFIED_EXACT
candidate metric factor <101/100:                            CERTIFIED_EXACT
actual invariant stable chart/holonomy on that root:         NOT_CERTIFIED

full conditional-hazard survivor iff:                        CERTIFIED_EXACT
actual full first-failure hazard rows:                        0
physical positive all-depth survivor:                        NOT_CERTIFIED

actual marker P_eta=0 on the root:                            NOT_CERTIFIED
weighted-BV multiplier boundedness iff:                       CERTIFIED_EXACT
weighted-BV moving Piola remainder iff:                       CERTIFIED_EXACT
local compact depth-96 physical Piola:                        CERTIFIED_LOCAL
global physical weighted variation/strong recipient:         NOT_CERTIFIED

actual stable-tree instantiation:                             0/7
Gate 2 official immutable fields:                             0/17
Gate 4 landing join:                                          1/7; fields 1,4,7 partial
complete composite gates:                                     0/5
CM2:                                                         NO-GO_FOR_CLAIM
```

## 7. Executable evidence

- `cm2_gate24_round67_actual_root_stable_tail_variation_frontier_cert.py`;
- `cm2_gate24_round67_actual_root_stable_tail_variation_frontier_verifier.py`;
- `cm2-gate24-round67-actual-root-stable-tail-variation-frontier-manifest-2026-07-21.json`;
- `cm2-gate24-round67-actual-root-stable-tail-variation-frontier-manifest-2026-07-21.sha256`.

The producer and independent verifier pin every physical input, replay the
root Jacobian, exact candidate density and singular values, both hazard
families, the BV equivalence bounds and the strict `0/7` ledger.  They reject
hostile semantic and strict-JSON mutations, reproduce byte-identical output,
replay the SHA sidecar, and fail closed with default exit status `2`.
