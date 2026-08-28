# CM2 Gates 3/4: C24 sparse hit-gap and exponential-tail assault

Date: 2026-07-18 (Asia/Shanghai)  
Parameter range: uniformly for `|s|<=1/400`  
Precursor: the frozen `C24` `O1/O1'/O2` open-hole leaf

## Verdict

The missing **unnormalized** sparse-block mass-loss inequality is now closed.
There is one theorem-supplied uniform integer `N_open>=1` such that every
normalized positive pre-hole density in the Demers--Liverani base cone loses
strictly more than

```text
epsilon_hit = 21/111718750
```

at the next scheduled `C24` opening.  Hence

```text
mu_s(intersection_{j=1}^k T_s^(-j*N_open)(C24^c))
  < (111718729/111718750)^k.
```

All-time avoidance is a subset of scheduled avoidance.  With the old core
mass lower bound this gives, for every integer `n>=0`,

```text
P_{mu_C24,s}(tau_C24^+>n)
  < (550000/147)
    (111718729/111718750)^floor(n/N_open).
```

Thus the physical unweighted first-return tail is uniformly exponential in
collision time.  The block length, and therefore the numerical one-collision
base

```text
rho_open=(111718729/111718750)^(1/N_open),
```

remain theorem-supplied rather than numerically evaluated.  The result does
not include branchwise strong `q` weights and does not close Gates 3, 4 or 5.

## 1. One explicit global `C1` hit observable

Inside the `G:E` axial core

```text
t in [1/100,1/50],   p in [-1/500,1/500],
```

set

```text
t_c=3/200,   a=1/250,   b=3/2000,
x=(t-t_c)/a, y=p/b,
g=(1-x^2)^2(1-y^2)^2
```

on `|x|,|y|<=1`, and set `g=0` outside.  Its support is

```text
t in [11/1000,19/1000],
p in [-3/2000,3/2000],
```

whose closure lies strictly inside that single core.  Both the polynomial
and its first derivative vanish on every support face, so extension by zero
is a global `C1` function on the collision section.  Pointwise,

```text
0<=g<=1_C24<=1.
```

The exact one-dimensional integral is

```text
integral_{-1}^1 (1-u^2)^2 du =16/15.
```

Using `R_G=9/25` and `dtheta/dt>=1`, its unnormalized collision integral is
strictly larger than

```text
(9/25)(1/250)(3/2000)(16/15)^2
=24/9765625.
```

The full collision volume is below `4*(22/7)*(13/25)`.  Therefore

```text
mu_s(g)>21/55859375=2*epsilon_hit
```

uniformly in `s`.

For the loss-of-memory estimate a global `C1` norm is also needed.  On
`[-1,1]`, `|(1-u^2)^2|' <2`.  In the chosen chart,

```text
|partial_t g|<500,
|dt/dr|<25/9,
|partial_r g|<12500/9,
|partial_phi g|<4000/3.
```

Consequently the conservative sum norm satisfies

```text
|g|_C1 <1+12500/9+4000/3
       =24509/9
       <2724.
```

## 2. Recovery, normalization and the next-hit gap

Let `C=C_{c,A,L}(delta)` be the base projective cone, and let `f>=0` be a
normalized pre-hole density in `C`.  Write

```text
h_0=1_{C24^c} f.
```

The precursor leaf certified `O1'` with `P0=49`, `O2` with `Ct=1493`, and
`mu_s(C24)<1/2500`.  Demers--Liverani Lemma 8.8 therefore supplies a uniform
recovery time after which

```text
L_s^n h_0 in C'
```

for one fixed enlarged cone `C'`.  Equation (8.7) gives strictly positive
surviving mass, so normalization is valid.  Set

```text
h = L_s^n h_0 / integral(h_0)dmu_s.
```

Both `h` and the invariant constant density `1` belong to `C'` and have mass
one.  Apply Theorem 7.3(b) in that cone, with the global `C1` observable `g`.
After `m` additional closed collisions,

```text
| integral g L_s^m h dmu_s - integral g dmu_s |
  <= C' (vartheta')^m |g|_C1.
```

The constants are uniform over the admissible compact table family.  Choose
one common existential `m` such that

```text
C' (vartheta')^m 2724 <21/111718750.
```

Combining this with `mu_s(g)>2 epsilon_hit` gives

```text
integral_C24 L_s^m h dmu_s
 >= integral g L_s^m h dmu_s
 > epsilon_hit.
```

Finally choose one `N_open` large enough both for this recovery-plus-mixing
step and for Proposition 8.7 to return the normalized output to the original
base cone.  This closes the induction: the same statement applies before
every scheduled restriction.  No spectral-continuity assumption is used.

## 3. Scheduled survival and all-time return

The first scheduled opening occurs at time `N_open`.  Before it, invariance
leaves the density equal to `1`, and its hit mass is

```text
mu_s(C24)>147/550000>epsilon_hit.
```

Every later block loses more than `epsilon_hit` by the preceding induction.
Thus scheduled survival after `k` openings is strictly below

```text
(1-epsilon_hit)^k
=(111718729/111718750)^k.
```

For `k=floor(n/N_open)`,

```text
{x in C24: tau_C24^+(x)>n}
```

is contained in `C24` at time zero and in `C24^c` at every sampled time
`j*N_open`, `1<=j<=k`.  Dropping the time-zero restriction only enlarges
the ambient event.  Dividing the scheduled bound by
`mu_s(C24)>147/550000` proves the displayed normalized return-tail estimate.

Equivalently, with

```text
rho_open=(111718729/111718750)^(1/N_open)<1,
A_open=61445312500000/16422653163,
```

one has

```text
P_{mu_C24,s}(tau_C24^+>n)<A_open rho_open^n.
```

The unweighted positive exponential moment follows for every
`0<c<-log(rho_open)`.

## 4. Exact scope

```text
C24 explicit recovered-cone hit gap:              CERTIFIED
C24 uniform unweighted exponential return tail:   CERTIFIED
C24 numeric N_open and numeric collision rho:      NOT CERTIFIED
q-weighted exponential excursion/cemetery tail:   NOT CERTIFIED
full 2d branch-materialized R_n/Q_n partition:     NOT CERTIFIED
branch Jacobian/distortion/mass/q payload:         NOT CERTIFIED
common fw/rev strong restriction:                  NOT CERTIFIED
induced common strong Lasota--Yorke coefficient:   NOT CERTIFIED
complete 18-field operator blocks:                 0
Gates 3/4/5:                                       NOT CERTIFIED
```

This leaf upgrades the earlier geometry leaf's local scope boundary; it does
not mutate that frozen precursor.

## 5. Replay

```bash
PYTHONPATH=deliverables .venv-neurips/bin/python \
  deliverables/cm2_gate34_c24_sparse_hit_gap_verifier.py \
  --integrity-only

PYTHONPATH=deliverables .venv-neurips/bin/python \
  deliverables/cm2_gate34_c24_sparse_hit_gap_verifier.py \
  --replay

PYTHONPATH=deliverables .venv-neurips/bin/python \
  deliverables/cm2_gate34_c24_sparse_hit_gap_verifier.py \
  --self-test
```

All explicit audit modes pass; hostile mutations pass `74/74`.  Default live
mode exits `2` because the strong `q` tail, induced strong operator and Gates
3/4/5 remain open.
