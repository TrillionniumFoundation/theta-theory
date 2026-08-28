# CM2 Gate 4 numeric invariant-family/Growth/recovery frontier assault

Date: 2026-07-16 (Asia/Shanghai)

## Verdict

This assault closes the numerical standard-family layer that remained after
the componentwise one-step contraction.  The new argument does **not** use the
grazing-singular coordinate `D2T` envelope as a curvature bound.  Instead it
keeps the exact endpoint-cosine factors in the graph transform and obtains a
four-phase invariant curvature family covering every iterate.

The resulting strict status is:

```text
ALL-ITERATED PHASE-TYPED D_std < 30000000:             CERTIFIED
ALL-STANDARD-CURVE ADAPTED LOG-JACOBIAN DISTORTION:    CERTIFIED
INVARIANT REGULAR-DENSITY CONE:                        CERTIFIED
NUMERIC LINEAR GROWTH RECURRENCE:                      CERTIFIED
NUMERIC C_p,vartheta_p,A0,A1:                          CERTIFIED
NATIVE LEVELWISE UNNORMALISED RECOVERY MOMENT:         CERTIFIED
FULL UNNORMALISED/REWEIGHTED NATIVE CONTRACT:          NOT CERTIFIED
COMPLETE NUMERIC C_fw,C_rev AND FINAL q:               NOT CERTIFIED
GATE 4:                                                NOT CERTIFIED
```

The major new constants are

```text
D_std < 30000000,
delta_* = 10^-90                         (adapted length),
vartheta_p = 360134800/360493663 < 1,
1-vartheta_p = 358863/360493663,
A0 = 301500,
A1 = 1005.
```

The enormous `C_p` below is intentional.  No asymptotic or floating-point
claim is used.

Evidence:

- `deliverables/cm2_gate4_numeric_invariant_family_growth_recovery_frontier_cert.py`;
- `deliverables/cm2_gate4_numeric_invariant_family_growth_recovery_frontier_verifier.py`;
- `deliverables/cm2-gate4-numeric-invariant-family-growth-recovery-frontier-manifest-2026-07-16.json`;
- `deliverables/cm2-gate4-numeric-invariant-family-growth-recovery-frontier-manifest-2026-07-16.sha256`.

## 1. Read-only typed inputs

The certificate pins and replays the frozen manifests for:

1. the global componentwise one-step bound
   `Xi_1(delta_1)<900337/901685`, with
   `delta_1=1/37724355673552103994`;
2. the fixed invariant cone
   `25/9<V<4108425/145348<29`;
3. the exact adapted inverse contraction
   `<144000/180337`;
4. the all-physical-branch coordinate envelope
   `||D2T||_infinity<42672/c_1^3`;
5. the 128 physical oriented carriers and their initial curvature `<4949`;
6. the finite-`s` density mesh and
   `C_mesh=69986663973833932800`;
7. the physical native prefix antichain and the finite-cemetery scope audit.

The 35,024 horizon leaves are still used only to supply the scalar finite
horizon bounds.  The 448 chart candidates remain conservative candidates,
not physical children.  The componentwise `Xi` theorem retains its original
true-owner and true-component typing.

## 2. Exact graph-curvature recurrence

Fix a homogeneous physical branch.  Write

```text
c_i = cos(phi_i),
B   = kappa_0+V_0,
h   = tau+c_0/B,
A   = B h = tau B+c_0.
```

The exact projected derivative and slope recurrence are

```text
|dr_1/dr_0| = A/c_1,
V_1 = kappa_1+c_1/h.                                  (2.1)
```

Let `D_i=|dV_i/dr_i|`.  Differentiating (2.1), while keeping the
determinant/cosine structure, gives

```text
D_1
 <= V_1/h
  + c_1^2/(B h^3)
      (|tau'_W|+|c'_0|/B+c_0 D_0/B^2).                (2.2)
```

The already certified branch bounds give

```text
|tau'_W| < 108/c_1,
|c'_0| < 29,
B > 50/9 > 5,
h > tau > 36337/800000 > 9/200.
```

Therefore

```text
D_1 < A_curv + b(c_0,c_1)D_0,                         (2.3)

A_curv
 < 29/(9/200)
   +108/[5(9/200)^3]
   +29/[25(9/200)^3]
 =182549800/729
 <251000,

b(c_0,c_1)
 =c_0 c_1^2/[tau(kappa_0+V_0)+c_0]^3.                 (2.4)
```

This is the key difference from substituting the coordinate
`42672/c_1^3` bound into a generic graph transform.  Equation (2.4) retains
the `c_0 c_1^2` factor that removes the apparent grazing divergence.

## 3. Correlated products and the four-phase invariant family

Since

```text
(kappa_0+V_0)tau
 > (50/9)(36337/800000)
 =36337/144000
 >1/4,
```

one step has the safe endpoint bound

```text
b_j
 < c_j c_(j+1)^2/(1/4+c_j)^3,
sup_[0,1] c/(1/4+c)^3 =64/27 <12/5.                  (3.1)
```

The endpoint cosine of one step is the source cosine of the next.  Hence an
`n`-step product is not bounded by `(12/5)^n`; its internal factors combine:

```text
product_(j=0)^(n-1) b_j
 < (12/5)(64/125)^(n-1),                              (3.2)
```

because

```text
sup_[0,1] [c/(1/4+c)]^3 = (4/5)^3=64/125.
```

For four steps,

```text
P_4 < (12/5)(64/125)^3
    =3145728/9765625
    <1.                                               (3.3)
```

Start phase zero with `D_0<=2000000`.  Applying the one-step endpoint bound
for the three intermediate phases gives

```text
phase 0:  2000000,
phase 1:  5051000,
phase 2: 12373400,
phase 3: 29947160.                                    (3.4)
```

Using the correlated four-step product and its exact suffix sum,

```text
S_4 =1+(12/5)[1+64/125+(64/125)^2]
    =410777/78125,

D_4
 <251000 S_4 + P_4(2000000)
 =49099736/25
 =1963989.44
 <2000000.                                            (3.5)
```

Thus phase zero returns strictly inside itself every four collisions.  True
singularity cuts, homogeneity cuts, and artificial length cuts only restrict
a graph: they do not change its curvature or phase.  Since all 128 initial
oriented carriers have curvature `<4949`, every descendant belongs to one of
the four phases, and globally

```text
D_std <30000000.                                      (3.6)
```

This is an all-iterate statement on the declared physical standard-curve
family.  It is not the old one-step carrier `<4949` statement.

## 4. Numerical distortion on every phase-typed standard curve

The frozen conditional projected-Jacobian formula is

```text
C_log(D)=710+(3836+3D)(144000/36337).
```

At `D=30000000`,

```text
C_log(D)=12960578183270/36337 <360000000.             (4.1)
```

Replaying the exact homogeneity-strip cubed comparisons at the enlarged
cutoff `k0=6121` gives

```text
high strips:  C_high =5000000000,
central:      C_cent =14000000000000000000000000.     (4.2)
```

For the adapted line element

```text
dell_*=(kappa+V)|dr|,
(5/27)dell_E < dell_* < (141/4)dell_E,                (4.3)
```

the Jacobian differs from the projected `r`-Jacobian by the source/target
factors `kappa+V`.  Since

```text
|d_r log(kappa+V)| <= (9/50)D_std =5400000,
```

the single constant

```text
C_d^* =15000000000000000000000000                     (4.4)
```

satisfies, on every phase-typed homogeneous child,

```text
|log(J_*(x)/J_*(y))|
 < C_d^* ell_*(x,y)^(1/3).                            (4.5)
```

No initial-carrier distortion is being relabelled as an iterated theorem;
(4.5) uses the new global `D_std`.

## 5. Invariant density cone and the tiny canonical length

Use the adapted log-density cone

```text
|log rho(x)-log rho(y)|
 <= L_rho ell_*(x,y)^(1/3),
L_rho=500000000000000000000000000.                    (5.1)
```

The adapted inverse contraction satisfies

```text
144000/180337 < (93/100)^3.
```

Thus one push-forward changes the right side of (5.1) by at most

```text
(93/100)L_rho+C_d^*
 =480000000000000000000000000
 <L_rho.                                              (5.2)
```

The cone is invariant.  Choose the deterministic maximum adapted length

```text
delta_* =10^-90.                                      (5.3)
```

This is inside the componentwise theorem's scope by a colossal margin:

```text
length_E(W)
 <(27/5)delta_*
 <1/37724355673552103994
 =delta_1.                                            (5.4)
```

Consequently every canonical curve is short enough for the already
certified global `Xi_1(delta_1)` bound.  Equation (5.1) also gives

```text
osc_W(log rho) <=L_rho delta_*^(1/3)=1/2000,
max rho/min rho
 <=exp(1/2000)
 <=1/(1-1/2000)
 =2000/1999.                                          (5.5)
```

The frozen physical densities fit (5.1) after canonical subdivision: their
old one-third log-Hölder constant is `52`, and changing from `dr` to
`dell_*` adds only the controlled `log(kappa+V)` factor.

## 6. A fully numerical linear Growth recurrence

For a weighted family `F={(p_a,W_a,rho_a)}`, use

```text
Z_*(F)=sum_a p_a/ell_*(W_a).                          (6.1)
```

On a parent of length at most `delta_*`, normalized density satisfies

```text
max rho <=(2000/1999)/ell_*(W).
```

For a true/homogeneity child `V_i`, its preimage adapted length is at most
the child's adapted length times the certified inverse-expansion mark
`lambda_i`.  Therefore

```text
sum_i p_i/ell_*(V_i)
 <(2000/1999)(900337/901685) p/ell_*(W).              (6.2)
```

The exact contraction is

```text
vartheta_p
 =(2000/1999)(900337/901685)
 =360134800/360493663
 =1-358863/360493663
 <1.                                                  (6.3)
```

After the physical and homogeneity cuts, every long child is partitioned
into equal adapted-length pieces in `[delta_*/2,delta_*]`.  For all long
children together,

```text
sum_pieces mass(piece)/ell_*(piece)
 <=(2/delta_*) total_long_child_mass.                 (6.4)
```

The charge in (6.4) is applied **once to the total long-child mass**.  It is
not multiplied again by the number of physical components, candidate rows,
or artificial pieces.  Physical true/homogeneity cuts are counted once in
`Xi`; artificial maximum-length cuts are counted once by (6.4).

Hence

```text
Z_*(T F)
 <=vartheta_p Z_*(F)+2*10^90 mass(F).                 (6.5)
```

Iteration gives

```text
Z_n^*/mass
 <=vartheta_p^n Z_0^*/mass
   +(2*10^90)/(1-vartheta_p).                         (6.6)
```

One valid adapted properness constant is

```text
C_p^*
 =4*10^90*360493663/358863.                           (6.7)
```

Using (4.3), the Euclidean SYZ-form bound holds with

```text
C_p
 =141*10^90*360493663/358863,

Z_n^E/mass
 <=(C_p/2)(1+vartheta_p^n Z_0^E/mass).                (6.8)
```

Equations (6.3) and (6.8) are explicit numerical `vartheta_p,C_p`; no
unnamed theorem constants remain in this layer.

## 7. Numerical recovery clocks

The first `delta_*` subdivision adds at most `2/delta_*` to adapted `Z`.
Converting the old boundary by the safe metric factor `27/5` gives, for a
depth-`D` atom,

```text
Z_0^*/mass
 <[2*10^90+(27/5)C_mesh]2^D
 <2^(D+300).                                          (7.1)
```

Set

```text
m=1-vartheta_p=358863/360493663.
```

Since `1005m>=1`, Bernoulli's inequality gives

```text
vartheta_p^1005 <=1/2.                                (7.2)
```

Combining (7.1)--(7.2),

```text
R(D) <=1005(D+300)
     =301500+1005D.                                   (7.3)
```

The recovery target is explicit: at this time

```text
vartheta_p^R Z_0^*/mass <1,
```

so (6.6)--(6.8) give

```text
Z_R^*<C_p^* mass,
Z_R^E<C_p mass.                                       (7.4)
```

Thus the new numerical constants are

```text
A0=301500,
A1=1005.                                              (7.5)
```

Their size comes from the deliberately microscopic `delta_*`, not from an
arbitrary assignment.

## 8. Native levelwise unnormalised recovery

For the frozen native prefix antichain,

```text
w_K=(3/4)4^-K,
D_K=3K+2.                                             (8.1)
```

The forward and reverse views share the same record `(e,s,K,q,j)`.  Applying
(7.3) separately to them gives

```text
R_fw(D_K),R_rev(D_K) <=303510+3015K,
R_fw+R_rev <=607020+6030K.                            (8.2)
```

Take

```text
gamma=1/12060.
```

Then the shell ratio in the payload moment is

```text
2 exp(6030 gamma)/4
 =exp(1/2)/2
 <sqrt(3)/2
 <7/8.                                                (8.3)
```

Also `exp(607020 gamma)=exp(151/3)<3^51`.  Consequently

```text
sum_(K>=0)
  w_K 2^K exp(gamma(R_fw+R_rev))
 <2*3^52.                                             (8.4)
```

This is a full-mass, query-independent, record-preserving **levelwise
unnormalised recovery-clock moment**.  It uses the shell mass `w_K` and the
payload factor `2^K`; it never charges the forbidden leafwise inverse mass or
`2^D_K`.

The countably infinite native partition still has infinite time-zero `Z` if
all leaves are materialized as one family.  Thus (8.4) is not relabelled as a
single initially finite-`Z` family theorem.

## 9. Exact remaining `C_fw,C_rev,q` boundary

The following inputs are now numerical:

1. all-iterate curvature and distortion;
2. invariant density regularity;
3. one-step and iterated Growth recurrence;
4. `C_p,vartheta_p,A0,A1`;
5. a native levelwise payload/recovery moment.

Complete `C_fw,C_rev` still cannot be assigned.  Four exact fields remain:

1. an unnormalised recordwise strong-operator norm proving that each actual
   physical indicator/test cost aggregates with shell mass and payload
   `2^K`, rather than the forbidden `2^D_K` or leafwise inverse mass;
2. a query-independent finite levelwise boundary numerator after every
   repeated physical indicator;
3. one forward/reverse propagation ledger preserving the identical physical
   occurrence, coefficient, and restriction record through the two recovery
   clocks;
4. the Gate-3 common branch-record `MT_DQ` interface identifying those
   recovered factors with the physical current.

In particular, the marginal rank tail in `B` and the native shell tail in
`K` do not by themselves supply the missing joint `(B,K)` strong-cost moment.
Multiplying two critical marginal estimates without a joint ledger would be
invalid.

Therefore

```text
C_fw:                              NOT CERTIFIED,
C_rev:                             NOT CERTIFIED,
q=max(C_fw,C_rev,2)m:              NOT CERTIFIED,
full reweighted native recovery:   NOT CERTIFIED,
Gate 4:                            NOT CERTIFIED.
```

The new `vartheta_p` is a Growth coefficient.  It is neither the old local
`q_branch` nor the final same-occurrence `q`.

## 10. Replay and fail-close contract

```bash
PYTHONPATH=deliverables python \
  deliverables/cm2_gate4_numeric_invariant_family_growth_recovery_frontier_verifier.py \
  --replay --integrity-only

PYTHONPATH=deliverables python \
  deliverables/cm2_gate4_numeric_invariant_family_growth_recovery_frontier_verifier.py \
  --self-test

PYTHONPATH=deliverables python \
  deliverables/cm2_gate4_numeric_invariant_family_growth_recovery_frontier_verifier.py
```

Replay/integrity and mutation testing must exit `0`.  Default live execution
must exit `2`, because complete reweighted recovery, `C_fw,C_rev`, final `q`,
and Gate 4 remain open.

All frozen inputs are read-only dependencies.
