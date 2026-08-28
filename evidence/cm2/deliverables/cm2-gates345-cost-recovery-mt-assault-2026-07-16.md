# CM2 Gates 3--5: bidirectional costs, controlled recovery, and MT_DQ frontier

Date: 2026-07-16 (Asia/Shanghai)  
Model: centred rational two-disk torus pilot, corrected 64-row physical event atlas  
Frozen inputs: v51/v52 and the first eight direct-assault freezes were read only

## 1. Verdict

This ninth-pass assault closes substantially more of the one-collision and
controlled-recovery geometry, but it does **not** close a composite gate.

```text
GATE 3 complete dynamic branch-record MT_DQ:                  NOT CERTIFIED
GATE 4 finite-s complete numeric C_fw/C_rev and final q:      NOT CERTIFIED
GATE 5 physical prefix/suffix three-norm lift:                NOT CERTIFIED

CONTROLLED s=0 STOPPED-PARENT RECOVERY:                       CERTIFIED
UNCONDITIONAL CM2:                                             NO-GO FOR CLAIM
STRICT COMPOSITE GATES CLOSED:                                 0/5
```

The new positive results are:

1. all 128 maximal-row endpoint germs are simple and carry one canonical
   endpoint rank with raw mass tail `O(4^-B)`;
2. one-collision forward and reverse chart costs, exact arclength densities,
   raw boundary `Z`, a fixed invariant geometric cone, carrier `C2`, and
   logarithmic-density costs are numeric;
3. a query-independent product stopped-depth kernel has exact tail `4^-K`
   and `E[2^K]=3/2`;
4. a `3/2`-power density mesh makes every one-time controlled atom an
   orientation-specific initial standard family with `Z<=C 2^K`;
5. the closed-map Growth Lemma then gives controlled `s=0` stopped-parent
   recovery and a finite depth-plus-recovery moment for some `gamma>0`;
6. depth-one DQ now allows strongly convergent moving tests, and the exact
   fixed-time noncommutative DQ telescope is closed through depth 64.

The remaining finite-`s`, iterated-cut, and Banach-space interfaces are
listed exactly in Section 9.

## 2. Mandatory convention audit

The frozen one-collision Birkhoff derivative, up to its common scalar, is

```text
[[tau*kappa_0+cp_0, tau],
 [tau*kappa_0*kappa_1+kappa_0*cp_1+kappa_1*cp_0,
  tau*kappa_1+cp_1]].
```

For `V=dphi/dr`, direct division gives

```text
V_1 = kappa_1 + cp_1/(tau + cp_0/(V_0+kappa_0)).       (2.1)
```

The denominator contains `V_0+kappa_0`, not `V_0-kappa_0`.  An early draft
of the new cone certificate used the wrong sign.  It was rejected during
the matrix audit and corrected before any manifest was frozen.  The corrected
formula is also guarded by an exact rational matrix-slope identity and a
mutation test.

The eighth-pass collision-flux correction remains in force:

```text
dm_e = R_source*cp_source*abs(u_y)/ell_T dtheta,       (2.2)
```

with one power of `cp`, not two.

## 3. Endpoint rank and first-order costs

Every maximal row has two endpoint incidences.  The complete count is

```text
source grazing                              32
parameter polarity                          16
physical first-visibility boundary          16
physical later-miss switch boundary         64
total                                      128
```

On the common inward collar `1/2048`, the certified one-sided derivative
margins are respectively

```text
99/100, 9/50, 3/40, 3/80.
```

The compact complement is covered by 3,206 Arb leaves, maximum subdivision
depth 14, and has

```text
cp_source       > 1/4096,
abs(u_y)        > 1/16384,
cp_miss^2       > 1/16384,
transition^2    > 1/16384.
```

The canonical rank is

```text
B=max(14,ceil(log2(1/scale)))
```

on the active endpoint collar and `B=14` on the compact core.  For every
integer `b>=14`, the exact global unnormalized tail bound is

```text
sum_e m_e{B>b} <= (9158592/6875) 4^-b.               (3.1)
```

Thus raw moments `integral 2^(chi B) dm` are finite for `chi<2`.  The exact
one-collision derivative matrix gives

```text
||DF_e||_infinity     < 150/cp_miss,
||DF_e^-1||_infinity  < 150/cp_source,
```

and both one-collision `C1` chart/test-pullback subcosts are bounded by

```text
C_fw^(1)=C_rev^(1)=151*2^B.                           (3.2)
```

The corresponding first-order charge has finite mass, but its remaining
rank-moment window is correctly degraded to `chi<1`.

## 4. Exact two-view densities and boundary Z

With respect to source arclength,

```text
rho_rev = cp_source*abs(u_y)/ell_T,                   (4.1)
rho_rev < 10.
```

If `L=t_miss-ell_T`, the caustic-to-miss Jacobian is

```text
abs(dr_miss/dtheta)
 = L*R_source*cp_source/(ell_T*cp_miss),              (4.2)
```

and hence

```text
rho_fw = cp_miss*abs(u_y)/L,
rho_fw < 800000/36337.                                (4.3)
```

There are 48 simple density-zero endpoints in each orientation.  The raw
boundary sums are finite and satisfy

```text
global reverse source Z <= 163855/256,
global forward miss Z   <= 102409375/72674.           (4.4)
```

These are raw orientation-specific boundary costs.  They are not, by
themselves, a uniform standard-pair density statement near a zero endpoint;
Section 7 supplies the required density-regular mesh.

## 5. Fixed invariant cone and geometric regularity

The global free-flight gap is

```text
tau > 36337/800000.
```

Equation (2.1) makes the fixed interval

```text
25/9 < V=dphi/dr < 4108425/145348 < 29              (5.1)
```

strictly forward invariant.  Time reversal sends every source carrier into
this cone with upper slope `65/4`, and every miss image is already in the
same cone.  All 64 forward and all 64 reverse views therefore have cone-entry
time zero.  This is a geometric cone statement, not yet the full moving-
parameter proper-family theorem.

For either oriented circular-caustic family,

```text
V=kappa+cp/d,
abs(dV/dr) <= kappa/d + 2/d^2 + R_caustic/d^3.       (5.2)
```

The resulting exact bounds are

```text
source reverse: 1245/2 < 623,
miss forward:   237433247845000000/47978559724753 < 4949.  (5.3)
```

The missing nonactive parameter-velocity companion bound was replayed on
all endpoint collars:

```text
abs(u_y)>1/32 on all 112 non-polarity collars.        (5.4)
```

Together with the endpoint rank this yields

```text
abs(d log rho_rev/dr_source) < 27*2^B,
abs(d log rho_fw/dr_miss)    < 52*2^B.               (5.5)
```

The one-collision geometric subcosts can therefore be charged as

```text
C_rev^(geom,Z)=204*2^B+C_Z_rev,
C_fw^(geom,Z)=204*2^B+C_Z_fw,                        (5.6)
```

where `204=151+52+1`, with the last unit absorbing (5.3) because `B>=14`.
One common partial charge is

```text
q_e^(geom,Z)=max(C_fw^(geom,Z),C_rev^(geom,Z),2)m_e.
```

Its global mass before `Z_N^-1` is bounded by

```text
344740673672569503213/63953120000.                   (5.7)
```

This is the complete raw one-collision geometric layer, not the final
finite-`s` recovery/prefix charge.

## 6. A genuine supercritical stopped-depth law

The eighth-pass dyadic algebra fixes the normalization cost `2^K` but not
a law for `K`.  The critical model `P(K>=k)=2^-k` has

```text
E[2^K]=1+N/2
```

at cutoff `N`, so the critical tail is insufficient.

The new query-independent product kernel samples

```text
w_K=(3/4)4^-K, K>=0,                                 (6.1)
```

before orientation, product time, mode, and final test.  Given the row mass
coordinate `u_e`, it records the unique atom

```text
j=floor(2^K u_e).
```

Each `(K,j)` atom has joint mass

```text
(3/4)8^-K m_e,                                      (6.2)
```

and forgetting `(K,j)` returns exactly `m_e`.  The same mark is used in both
orientations.  Exactly,

```text
P(K>=k)=4^-k,
E[2^K]=3/2,
E[2^(5K/4)]<15/8.                                   (6.3)
```

Thus the stopped-depth obstruction is removed inside this declared policy.
This auxiliary kernel is not called a native dynamical stopping antichain.

## 7. Density-regular mesh and controlled s=0 recovery

On a shell whose density-zero scale is

```text
2^(-(b+1)) <= h < 2^-b,
```

use the carrier-arclength mesh

```text
delta_b=2^-ceil(3(b+1)/2).                           (7.1)
```

Then `delta_b^2<=h_lower^3`.  Since (5.5) gives the common shell bound
`abs(d log rho/dr)<=52/h_lower`, every mesh component satisfies

```text
abs(log rho(x)-log rho(y)) <= 52 d(x,y)^(1/3).       (7.2)
```

The common shell carrier-length and piece-count envelopes are

```text
length <= 8192*2^-b,
pieces <= 32769*2^ceil(b/2).
```

The density on a zero shell is at most `23*2^-b`; hence one zero endpoint
has unnormalized boundary-series bound

```text
sum_b Z_b <= 753687/32.                              (7.3)
```

The common positive row-mass lower bound is

```text
m_e(row)>169/2147483648000.                          (7.4)
```

For each orientation separately, every single depth-`K` atom therefore has
an initial standard-family representation with

```text
uniform unstable cone,
uniform C2 bound 4949,
uniform one-third log-Hoelder constant,
Z_fw(K,j),Z_rev(K,j) <= C_mesh 2^K.                 (7.5)
```

The forward and reverse decompositions may differ, but they represent the
same restricted measure and retain the same `(e,K,j)` record.

Canestrari, `arXiv:2604.19671v2`, Lemma 6.14 supplies the closed-billiard
Growth Lemma

```text
Z(F^((p+1)n_*)G) <= theta Z(F^(pn_*)G)+Z_0,
0<theta<1.                                           (7.6)
```

Its hypotheses are exactly (5.1), (5.3), (7.2), and (7.5).  Time reversal
gives the reverse statement.  Therefore finite table-dependent constants
`A0,A1` exist with

```text
R_fw(K,j)+R_rev(K,j) <= A0+A1 K.                    (7.7)
```

Combining (6.1) and (7.7), any

```text
0<gamma<log(2)/A1
```

gives

```text
E[2^K exp(gamma(R_fw+R_rev))] < infinity.            (7.8)
```

Thus controlled one-time stopped-parent recovery is certified at `s=0`.
The constants in (7.6)--(7.7) are theorem-supplied table constants rather
than newly interval-evaluated rational numbers; this is one reason the full
numeric finite-`s` `C_fw/C_rev` gate remains open.

## 8. MT_DQ progress

For a fixed `C1` source `h`, the eighth-pass theorem gives norm convergence

```text
L_s(h)=(P_s-P_0)h/s -> D_0h in (C^{1,alpha})*.       (8.1)
```

If `Phi_s->Phi_0` in `C^{1,alpha}`, then

```text
|L_s(h)(Phi_s)-D_0h(Phi_0)|
 <= ||L_s(h)-D_0h|| ||Phi_0||
  + ||L_s(h)|| ||Phi_s-Phi_0||.                     (8.2)
```

Norm convergence in (8.1) bounds `||L_s(h)||`, so (8.2) proves the centered
and uncentered **depth-one strong moving-test DQ**.

For every fixed `n`, the exact noncommutative identity

```text
(P_s^n-P_0^n)/s
 = sum_(j=0)^(n-1) P_s^(n-1-j) ((P_s-P_0)/s) P_0^j  (8.3)
```

was replayed as a formal word cancellation for every `1<=n<=64`.

Equations (8.2)--(8.3) close the moving-test and algebraic portions of the
fixed-time upgrade.  They do not turn branchwise iterated sources into fixed
`C1` inputs, do not construct the four-type common atlas, and do not prove
the summable two-time majorant.

## 9. Exact remaining boundary

### Gate 3

1. uniform operator-norm DQ from the frozen strong space to the DQ space;
2. branch-record `C1/BL` tightness across every iterated moving singularity;
3. fixed-time convergence of `Q_s^m` sources in the frozen strong space;
4. regular, face, product-current, and response convergence on one common
   finite component atlas;
5. the `FACE_2CUT` middle tail and summable two-time CM2 majorant.

### Gate 4

1. uniform finite-`s` moving-face versions of the standard-family mesh and
   recovery bound;
2. interval-evaluated numeric replacements for the table constants
   `C_mesh,A0,A1` if the final exponent ledger requires explicit numbers;
3. the final propagated common `q`, including every finite-`s` operator and
   recovery mark, rather than the present one-collision partial charge;
4. hereditary repeated-indicator recovery if a later handler uses more than
   the certified one-time controlled atom.

### Gate 5

1. complete return-word/operator-block registration, not merely the already
   certified component spanning graph and cycle gcd one;
2. physical prefix/suffix homogeneity, inverse-Jacobian, distortion, and
   cut-growth sums;
3. the regular-density, standard-family/flux-face, and dynamic-test norm
   intertwiners;
4. operator-valued Wiener/phase transfer on those completed blocks.

Gates 1 and 2 retain their previous same-carrier holonomy and full-mass
physical PPE obstructions.

## 10. Latest literature audit

The newest directly relevant source found in the 16 July search is

```text
Mark F. Demers and Carlangelo Liverani,
Recent Progress in the Application of Transfer Operators to Dispersing Billiards,
arXiv:2606.10155v1, submitted 2026-06-08.
```

Its Theorem 5.7 surveys uniform cone contraction for sequential finite-
horizon dispersing billiards.  Its Problem 8.7 explicitly warns that after
multiplication by a characteristic function, the selected density can
concentrate on atypical trajectories; general loss of memory in that setting
remains open.  This exactly forbids using the review to claim arbitrary
hereditary stopped recovery.

The present bridge avoids that overclaim: it first represents each one-time
controlled atom as a genuine standard family and then applies the closed-map
Growth Lemma.  No latest theorem found closes the remaining finite-`s`
moving-face DQ, repeated-indicator, or three-space norm interfaces.

## 11. Reproduction

The eight new certificate/verifier pairs are:

```text
cm2_gate45_endpoint_rank_first_order_cost
cm2_gate45_stopped_depth_kac_frontier
cm2_gate45_bidirectional_boundary_z_cost
cm2_gate45_global_invariant_cone
cm2_gate45_curvature_log_density_cost
cm2_gate45_product_stopped_depth_kernel
cm2_gate45_density_regular_mesh_recovery_bridge
cm2_gate3_moving_test_telescope_frontier
```

Run Arb-dependent artifacts with the recorded environment:

```bash
PY=/tmp/cm2-flint-venv/bin/python
$PY -m pip show python-flint
```

For each base name above:

```bash
$PY deliverables/${base}_verifier.py --replay --integrity-only
$PY deliverables/${base}_verifier.py --self-test
$PY deliverables/${base}_verifier.py
```

The first two commands exit zero.  The live default command exits two by
design until the remaining composite interfaces are certified.

