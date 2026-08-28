# CM2 Gates 3/4: C24 open-hole geometry assault

Date: 2026-07-18 (Asia/Shanghai)  
Parameter range: `|s|<=1/400`  
Physical section: `N=G disjoint-union W` in common `(r,phi)` collision coordinates

## Verdict

The three geometric inputs left open in Round 24 are now frozen uniformly on
the complete parameter interval:

```text
normalized collision-SRB mass of C24:  <29021/75000000<1/2500,
Demers--Liverani O1 and O1':             P0=49,
Demers--Liverani O2:                     Ct=1493,
stable diameter of C24:                  <1/20.
```

Consequently `C24` is rigorously admitted to the qualitative large-hole,
sparse-opening cone-recovery interface of Demers--Liverani,
arXiv:`2104.06947v3`, Section 8.2 and Proposition 8.7.  The compact table
family and the mass condition `mu_s(C24)<=1/2` are both bound to the same
fixed collision gauge.

This does **not** yet certify an every-collision exponential return tail.
The cited proposition and Theorem 8.9 recover a normalized cone and give
loss of memory when openings are separated by a theorem-supplied mixing
block.  The current chain has neither a numerical block length nor an
unnormalized killed-operator mass-loss/eigenvalue gap for this `C24` hole.
That distinction is kept fail-closed.

## 1. Exact collision-SRB mass upper bound

The 24 cores consist of eight axial and sixteen diagonal source rectangles.
Their rational `R Delta t Delta p` bases are

```text
axis:     13/156250,
diagonal: 26/15625.
```

Since `dtheta/dt=(1-t^2)^(-1/2)`, exact square comparisons give

```text
dtheta/dt <1001/1000  for |t|<=1/50,
dtheta/dt <1401/1000  for |t|<=7/10.
```

Thus the unnormalized core mass is strictly below

```text
(13/156250)(1001/1000)+(26/15625)(1401/1000)
=377273/156250000.
```

The full collision volume is `4*pi*(R_G+R_W)`.  Using `pi>3` and
`R_G+R_W=13/25` yields

```text
mu_s(C24)<(377273/156250000)/(156/25)
         =29021/75000000
         <1/2500
         <1/2.
```

Together with the old strict lower bound, the physical mass interval is now

```text
147/550000 < mu_s(C24) < 29021/75000000.
```

It is independent of `s` because the normalized `dr dp` collision measure
and the source rectangles are fixed in the common gauge.

## 2. `O1`, `O1'` and stable diameter

Each collision component contains twelve rectangles and hence 48 boundary
segments: 24 vertical `r=constant` segments and 24 horizontal
`phi=constant` segments.  A stable curve is a `C2` graph `phi(r)` with
strictly negative slope.  It therefore meets every vertical or horizontal
segment at most once.  Any stable curve is cut into at most

```text
48+1=49
```

pieces.  This proves both `O1` and the stronger `O1'` with `P0=49`.

For a stable graph wholly contained in the hole, connectedness places it in
one core rectangle.  Monotonicity bounds its length by total `r` plus `phi`
variation.  Exact derivative bounds give

```text
axis component length      <19019/2500000<1/100,
diagonal component length  <112709/2500000<1/20.
```

Hence `diam_s(C24)<1/20`.  This is a new quantitative input, but it is not
silently substituted into the small-hole lemma: the chain still lacks a
comparison with its cone-dependent threshold

```text
delta*(1/(4*P0*A))^(1/q).
```

## 3. `O2` uniform transversality

Time reversal of the frozen invariant geometric cone gives

```text
-4108425/145348 < dphi/dr < -25/9,
4108425/145348<29.
```

Near one vertical edge,

```text
ds/dr < sqrt(1+29^2)<30,
```

so an ambient epsilon-neighborhood contributes less than `60 epsilon` of
stable arclength.  Near one horizontal edge,

```text
|dr/dphi|<9/25,
ds/dphi<sqrt(1+(9/25)^2)<11/10,
```

and the contribution is less than `(11/5) epsilon`.  Summing all edges on
the collision component containing the stable curve gives

```text
24*60+24*(11/5)=7464/5<1493.
```

For `epsilon>=1/(2*1493)`, the trivial bound
`|W|<delta0<1/2<=1493 epsilon` closes the large-neighborhood case.  Therefore

```text
m_W(N_epsilon(boundary C24)) <=1493 epsilon
```

for every admissible stable curve and every `epsilon>0`, uniformly in `s`.

## 4. Exact theorem match and remaining mass-loss pole

The following hypotheses of Demers--Liverani are now on one physical
carrier:

```text
common compact finite-horizon table family,       certified,
fixed-s constant sequence admissible,             certified,
O1 and O1' with P0=49,                            certified,
O2 with Ct=1493,                                  certified,
mu_s(C24)<=1/2,                                   certified.
```

Proposition 8.7 therefore supplies qualitative uniform sparse-opening cone
recovery with existential `delta`, `chi<1`, `J` and `n_*`; footnote 25 gives
the uniform choice over holes with mass at most one half.

The next irreducible scalar interface is now precise.  One must certify
either

```text
inf { integral_C24 f dmu_s : f is a normalized recovered-cone density }
    >= epsilon_hit >0,
```

or an equivalent stationary killed-operator bound

```text
nu_s <=1-epsilon_hit<1
```

uniformly in `s`.  Only then does sparse sampled survival decay
exponentially; every-collision avoidance, being a subset, inherits that
bound.  Neither normalized loss of memory nor the Kac first moment alone
provides this missing unnormalized inequality.

## 5. Strict nonpromotion

```text
C24 exact mass upper:                              CERTIFIED
C24 O1/O1'/O2 geometry:                            CERTIFIED
C24 qualitative sparse-opening theorem admission: CERTIFIED
numeric sparse block / contraction:                NOT CERTIFIED
sampled exponential survivor mass:                 NOT CERTIFIED
every-collision exponential return tail:           NOT CERTIFIED
q-weighted excursion/cemetery tail:                NOT CERTIFIED
full 2d R_n/Q_n partition and payload:              NOT CERTIFIED
induced common strong Lasota--Yorke coefficient:    NOT CERTIFIED
Gates 3/4/5:                                       NOT CERTIFIED
```

The 2026 review arXiv:`2606.10155v1`, Section 5.6.1, was also checked.  It
confirms the same boundary: large holes require sparse intervening mixing,
and the recovered normalized cone is not itself an escape-rate certificate.

## 6. Replay

```bash
PYTHONPATH=deliverables .venv-neurips/bin/python \
  deliverables/cm2_gate34_c24_open_hole_geometry_verifier.py \
  --integrity-only

PYTHONPATH=deliverables .venv-neurips/bin/python \
  deliverables/cm2_gate34_c24_open_hole_geometry_verifier.py \
  --replay

PYTHONPATH=deliverables .venv-neurips/bin/python \
  deliverables/cm2_gate34_c24_open_hole_geometry_verifier.py \
  --self-test
```

All explicit audit modes pass; hostile mutations pass `70/70`.  Default live
mode exits `2` because the unnormalized exponential tail and Gates 3/4/5
remain open.
