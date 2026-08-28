# CM2 Round 66 Gate 2/4 — collision-SRB product crosswalk and variation frontier

Date label: 2026-07-21

Strict verdict: **the explicit invariant Sinai collision density gives an
exact conditional-density/holonomy formula once a genuine physical product
chart is supplied.  It does not supply that chart, an owner-to-landing joint
law, stable saturation of the common marker, a positive all-depth survivor,
or a physical strong/Piola recipient.  The best survivor lower bound from the
frozen actual first-failure rows is still zero.  Gate 2 remains `0/17`, Gate
4's landing join remains `1/7` with fields 1, 4 and 7 partial, the actual
stable-tree instantiation remains `0/7`, all complete composite gates remain
`0/5`, and CM2 remains `NO-GO_FOR_CLAIM`.**

## 1. Frozen scope and physical chain

This is an append-only Round-66 leaf.  It pins the Round-65 Gate-2/4 and
cross-gate leaves, Round-65 independent audit and aggregate, the direct
Round-58--64 owner/landing/holonomy chain, and the older physical
collision-SRB, affine-product, projected-shadow and boundary-tube inputs.
No old artifact is modified.

The compatible physical facts remain:

```text
common invariant collision probability proportional to cos(phi) dr dphi:
                                                               CERTIFIED
actual finite owner/root law nu on its stated owner carrier:   CERTIFIED
tagged Borel first-return inverse:                              CERTIFIED
kappa_B=g_B mu_C, 0<=g_B<=1:                                  CERTIFIED
marker-weighted finite-depth cone-curve lift:                  CERTIFIED
actual branchwise RN covariance:                               CERTIFIED
96 collision-shadow rows on one positive-width strip:         CERTIFIED
```

They are marginal or finite-depth statements.  No frozen row says that the
owner law, collision-SRB plaque law and common landing marker are the
marginals of one immutable product-tree law.

## 2. What the explicit Sinai density does give

### 2.1 Exact product-chart disintegration

On the usual collision section the normalized invariant density is

```text
dmu=c cos(phi) dr dphi.
```

With `p=sin(phi)`, this is the flat density

```text
dmu=c dr dp.                                             (2.1)
```

The restriction `mu_C` to the induced section has the same constant density
after the scalar normalization by `mu(C)`.  This is an exact and useful
physical fact, but it is a density in collision coordinates, not a stable
disintegration.

Let a future genuine product rectangle be parameterized by a one-to-one
`C1` chart

```text
Phi:I x S -> R subset (r,p),
```

where `u in I` is the common root coordinate and `s in S` labels unstable
plaques.  Put

```text
a(u,s)=|partial_u Phi(u,s)|,
q(u,s)=c |det D Phi(u,s)|,
Z(s)=integral_I q(u,s) du.                              (2.2)
```

Then the outer plaque law has density proportional to `Z(s)`, while the
conditional law on plaque `s`, relative to adapted arclength `dell_s`, has
the exact density

```text
rho_s(u)=q(u,s)/(Z(s)a(u,s)).                           (2.3)
```

If stable holonomy keeps the root coordinate fixed,

```text
h_st(Phi(u,s))=Phi(u,t),
```

its arclength derivative and conditional-measure RN factor are exactly

```text
lambda_st(u)=a(u,t)/a(u,s),                             (2.4)
J_st(Phi(u,t))=q(u,s)Z(t)/(q(u,t)Z(s)).                 (2.5)
```

Equations (2.3)--(2.5) replay the Round-64 compatibility identity

```text
J_st(hx) rho_t(hx)=rho_s(x)/lambda_st(x).               (2.6)
```

Thus the constant collision density cancels from the final ratio, but the
product-chart determinant, plaque speed and outer normalization do not.
Knowing (2.1) alone does not determine any of them.

For a common root interval of length `L_0`, if a future keyed chart proves

```text
0<q_-<=q<=q_+,       0<a_-<=a<=a_+,
```

then it would give the explicit bounds

```text
q_-/(q_+ L_0 a_+) <=rho_s<=q_+/(q_- L_0 a_-),
a_-/a_+             <=lambda_st<=a_+/a_-,
(q_-/q_+)^2         <=J_st<=(q_+/q_-)^2.              (2.7)
```

The metric version of the Round-63 path budget would reduce to

```text
F R (a_+/a_-)^3 < C_p theta L.                         (2.8)
```

This is conditional.  The Round-25 affine tile has a computable collision
area density but its affine fibres are cone candidates, not invariant stable
plaques.  Substituting that candidate chart into (2.3)--(2.8) would be a type
promotion.

### 2.2 Exact owner/landing crosswalk that is still missing

After matching total masses, a lawful join needs one positive Borel law
`Lambda` on owner records and product coordinates such that

```text
(pr_owner)_# Lambda = nu_*,
(Phi o pr_(u,s))_# Lambda = kappa_B,
Lambda{immutable owner/tree/branch/physical-ID keys agree}=Lambda(total).
                                                               (2.9)
```

The source and landing versions must additionally be joined by the frozen
tagged branch and the stable squares.  No such `Lambda`, endpoint pushforward
identity, common normalizer or key-support statement is frozen.

The obstruction is exact.  Let owner and plaque keys both be `{0,1}` with
uniform marginals.  The two couplings

```text
Lambda_align={(0,0),(1,1)} with mass 1/2 each,
Lambda_switch={(0,1),(1,0)} with mass 1/2 each
```

have identical owner and plaque marginals.  If the immutable registry
requires `owner=plaque`, the first coupling has compatible mass one and the
second has compatible mass zero.  Marginals, even when their scalar masses
and densities agree, do not determine the keyed joint crosswalk.

## 3. Smooth invariant density does not pay marker saturation

Even granting a perfect product rectangle, identity holonomy and a commuting
identity branch square, a positive landing marker need not descend through
the stable quotient.

Use four equally weighted plaques with a common unit root law and flat
collision density.  Compare two common-landing markers, both strictly
positive and both of total mass `1/2`:

```text
g_sat=(1/2,1/2,1/2,1/2),
g_var=(5/16,7/16,9/16,11/16),
```

where each value is constant along its plaque.  For `g_sat`, the Round-65
dispersion and median distance are zero.  For `g_var`, direct rational
calculation gives

```text
P_eta=5/64,
delta_eta=1/8,
P_eta<delta_eta<2P_eta.                                (3.1)
```

All reference densities, holonomy Jacobians, arclength derivatives, branch
squares and total landing masses are the same in the two completions.  Only
the cross-plaque marker field differs.  Therefore

```text
explicit invariant density + perfect product geometry + kappa_B<=mu_C
does not imply P_eta=0.                                (3.2)
```

This is a smooth product-law nonimplication model, not a claim that the
physical billiard realizes `g_var`.  It identifies the exact missing physical
row: the actual pulled-back marker equality, or equivalently `P_eta=0`, must
be proved on the same keyed product law.

## 4. First-failure assault and the sharp actual bound

Let `S_N` be the stable-base parameters with compatible graph transforms
through depth `N`, and `F_N=S_(N-1)\S_N`.  The exact identity is

```text
eta(S_infinity)=eta(S_0)-sum_(N>=1) eta(F_N).          (4.1)
```

On the frozen positive-width 96-word strip the actual rows say only that the
**collision-singularity shadow component** is zero:

```text
eta(C_N)=0, 1<=N<=96.                                  (4.2)
```

The same manifest explicitly records graph-transform chart survival as
`NOT_CERTIFIED`.  Since full failure also includes loss or nonexistence of the
required chart, (4.2) is not an upper bound for `eta(F_N)`, even at the first
96 depths.  There are therefore zero actual full first-failure upper-bound
rows.  Even under the optimistic completion `F_1=...=F_96=empty`, there is no
bound at depth 97.  Hence the sharp lower bound implied by all current rows is

```text
inf eta(S_infinity)=0,                                 (4.3)
```

attained by a compatible completion with immediate chart failure; under the
optimistic 96-prefix completion it is attained by `F_97=S_96`.  This is
logical sharpness, not an assertion that the physical strip fails.

The Round-26 estimate

```text
mass(U_d)<8*2^(-floor(d/3))
```

does not improve (4.3).  Its index `d` is adaptive spatial resolution for a
one-step `C24` boundary classifier; `N` is temporal stable graph-transform
depth.  No frozen map sends `F_N` into a same-law `U_d`, and no schedule
`d(N)` is pinned.  Likewise the Kac return tail controls return time, not
loss of a stable chart.

The shortest usable future row is now quantitative.  If, on the identical
base and keys, one proves for `k>=1`

```text
eta(F_(96+k))<=A sigma^k,       0<sigma<1,             (4.4)
```

then

```text
eta(S_infinity)>=eta(S_0)-A sigma/(1-sigma).           (4.5)
```

For the exact replay `eta(S_0)=1`, `A=1/4`, `sigma=1/2`, the survivor lower
bound is `3/4`.  The inequality is sharp at the level of failure masses.
Neither `A` nor `sigma` is available for the physical strip.

## 5. Transverse variation and physical strong/Piola recipient

The flat reference density also does not regularize the multiplier `g_B`.
On a perfect unit product rectangle take

```text
g_N(u,s)=1/2+(1/4)sin(2 pi N u).                       (5.1)
```

It is the same on every plaque, lies in `[1/4,3/4]`, has total mass `1/2`,
and has `P_eta=0`.  Nevertheless

```text
Var_u(g_N)=N -> infinity.                              (5.2)
```

Thus even the conjunction

```text
smooth invariant density + perfect holonomy + zero stable defect
```

does not supply the Round-65 weighted transverse-variation row.

In a fixed material coordinate, a useful exact sufficient recipient bound
can be stated as follows.  Let `q_r=b_r k_r` be the positive tag kernel
multiplied by its physical Piola coefficient, with tag weights `a_r>=1`.
If

```text
B_0=||sum_r a_r |q_r|||_infinity<infinity,
B_inf=sum_r a_r ||q_r||_infinity<infinity,
B_1=sum_r a_r Var(q_r)<infinity,                       (5.3)
```

then the BV product rule gives

```text
sum_r a_r ||q_r f||_BV
 <=(B_0+B_inf+B_1)||f||_BV.                            (5.4)
```

This joins tag depth and Piola multiplication only after all factors live in
one material chart.  The frozen chain supplies neither the physical `b_r`,
their variation, the moving-domain `o(s)` remainder, nor an intertwining
from this material BV ledger into the requested anisotropic current space.
The Round-65 exact `L1 -> strong -> BV` trace no-go remains in force.

## 6. Technology boundary

The directly relevant current sources remain type-mismatched:

- `arXiv:2604.25881v1` constructs local product structure for the billiard
  MME from symbolic Hausdorff leaf laws, not for the pinned common
  collision-SRB marker;
- `arXiv:2604.19671v2` starts from an already regular Sinai standard family
  and normalizes surviving mass; it does not create the present marked
  landing product law or a physical Piola recipient;
- `arXiv:2606.10155v1` is a transfer-operator review and supplies no immutable
  crosswalk or first-failure constants.

A fresh official arXiv API query for Sinai/dispersing billiard SRB holonomy
results returned `Rate exceeded`; no unseen result is inferred and no
external theorem is promoted.  The MME and smooth boundaryless-flow results
remain explicitly excluded as wrong-law/wrong-interface substitutes.

## 7. Strict frontier

```text
Sinai collision density cos(phi)drdphi=drdp:          CERTIFIED_PINNED
product-chart conditional density/RN/arclength:       CERTIFIED_EXACT_CONDITIONAL
actual invariant product chart and common root:       NOT_CERTIFIED
owner/landing immutable joint crosswalk Lambda:       NOT_CERTIFIED
same marginals imply keyed crosswalk:                  FALSE_BY_EXACT_COUPLING_SEPARATOR

flat invariant density/product geometry imply P_eta=0:FALSE_BY_SMOOTH_SEPARATOR
actual common marker P_eta=0:                          NOT_CERTIFIED

first-failure geometric-tail criterion:               CERTIFIED_EXACT_CONDITIONAL
actual full first-failure upper-bound rows:            0
sharp survivor lower bound from current actual rows:  0
physical all-depth positive survivor:                  NOT_CERTIFIED

zero stable defect implies transverse BV:             FALSE_BY_SMOOTH_SEPARATOR
material tag/Piola BV bound under B_0+B_inf+B_1:       CERTIFIED_CONDITIONAL
actual weighted transverse variation:                  NOT_CERTIFIED
physical strong restriction/intertwining/Piola:        NOT_CERTIFIED

actual stable-tree instantiation:                      0/7
Gate 2 official immutable fields:                      0/17
Gate 4 landing join:                                   1/7; fields 1,4,7 partial
Gate 2 / Gate 4:                                       NOT_CERTIFIED
complete composite gates:                             0/5
CM2:                                                   NO-GO_FOR_CLAIM
```

## 8. Executable evidence

- `cm2_gate24_round66_collision_srb_product_variation_frontier_cert.py`;
- `cm2_gate24_round66_collision_srb_product_variation_frontier_verifier.py`;
- `cm2-gate24-round66-collision-srb-product-variation-frontier-manifest-2026-07-21.json`;
- `cm2-gate24-round66-collision-srb-product-variation-frontier-manifest-2026-07-21.sha256`.

The producer and independent verifier pin the frozen chain, replay the exact
product-chart formulas and bounds, both binary crosswalk couplings, the
marker dispersion, the sharp first-failure optimization, the variation
separator and the material BV estimate.  They enforce strict JSON,
deterministic byte-identical regeneration, hostile semantic rejection,
sidecar replay and fail-closed default exit `2`.
