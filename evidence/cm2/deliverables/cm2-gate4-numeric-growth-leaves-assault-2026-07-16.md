# CM2 Gate 4 numerical Growth-leaf assault

Date: 2026-07-16 (Asia/Shanghai)

## Verdict

This assault numerically instantiates the hyperbolicity and metric leaves
that can be extracted directly from the certified finite-`s` collision
geometry.  It also closes a strict one-step expansion/cut sum on every
single true continuity branch.

It does **not** produce numerical global Growth-Lemma constants.  The full
true-singularity weighted branch sum, the `n`-step small-curve thresholds,
and map-Jacobian distortion constants are separate leaves and remain absent.
Therefore `C_p,vartheta_p,A0,A1,C_fw,C_rev,q` remain nonnumeric and Gate 4
remains open.

```text
NUMERIC ADAPTED-METRIC HYPERBOLICITY LEAVES:          CERTIFIED
NUMERIC SINGLE-TRUE-BRANCH ONE-STEP CUT SUM:          CERTIFIED
NUMERIC GLOBAL C_gr,vartheta_gr:                      NOT CERTIFIED
NUMERIC C_p,vartheta_p AND PROPAGATED q:              NOT CERTIFIED
GATE 4:                                               NOT CERTIFIED
```

## 1. Scope and frozen inputs

The calculation applies uniformly to the constant fixed-configuration maps

```text
T_s=F_(K_s,K_s),  |s|<=1/400,
```

used by the tenth-round stopped-parent recovery.  It does not identify these
maps with a source-target moving-configuration map.

Read-only inputs provide

```text
kappa in [25/9,25/4],
tau > 36337/800000,
25/9 < V=dphi/dr < 4108425/145348 < 29,
```

the exact Birkhoff derivative matrix, circular scatterers, and the uniform
finite-horizon class.

## 2. Exact adapted-metric expansion

Canestrari's adapted metric, equation (6.11) of arXiv:2604.19671v2, reduces
on a graph vector of slope `V=dphi/dr` to

```text
N_*(dr,dphi)=(kappa+V)|dr|.                            (2.1)
```

Write `A=kappa_0+V_0`.  The frozen collision matrix and the already audited
wavefront recurrence give

```text
|dr_1/dr_0|=(tau A+cp_0)/cp_1,
V_1=kappa_1+cp_1 A/(tau A+cp_0).                       (2.2)
```

Substitution into (2.1) yields the exact identity

```text
N_1/N_0
 =1+(2 kappa_1/cp_1)(tau+cp_0/(kappa_0+V_0)).         (2.3)
```

The factor `2` is forced by the metric's `kappa_1+V_1`; it is guarded by an
exact rational matrix/recurrent-slope replay.  Since `cp_1<=1`,
`cp_0/(kappa_0+V_0)>=0`, and the finite-`s` gap is strict,

```text
N_1/N_0
 >1+2(25/9)(36337/800000)
 =180337/144000.                                      (2.4)
```

Thus every homogeneous collision branch has adapted inverse contraction

```text
norm(DT_s^-1)_* < 144000/180337.                       (2.5)
```

This is a numerical hyperbolicity leaf, not yet the sum over cut branches.

## 3. Metric, cone, curve-length, and separation constants

On the invariant cone,

```text
N_*/norm_2=(kappa+V)/sqrt(1+V^2).
```

Using `kappa+V>=50/9` and `sqrt(1+V^2)<30` gives

```text
(5/27) norm_2 < N_* < (141/4) norm_2.                 (3.1)
```

A safe common equivalence constant is therefore

```text
C_metric=141/4.                                       (3.2)
```

The graph projection factor is `<30`, so the corresponding cone/coordinate
constant is

```text
C_cone=30.                                            (3.3)
```

Combining (2.4) and (3.1) gives explicit Euclidean cone hyperbolicity:

```text
norm(DT_s^n v)_2
 >(20/3807)(180337/144000)^n norm(v)_2.                (3.4)
```

Thus one may take

```text
c_hat=20/3807,
Lambda=180337/144000.                                 (3.5)
```

Every carrier is a graph over one circular boundary component.  Curvature
`>=25/9` gives radius `<=9/25`; with `pi<22/7`, its circumference is less
than `396/175`.  Paying the projection factor 30 gives

```text
L_0 < 2376/35 < 68.                                   (3.6)
```

Applying (3.4) to the common homogeneous segment up to separation time gives
the explicit metric-comparison constant

```text
d_M(x,y) < C_s Lambda^-s(x,y),
C_s=68 Lambda/c_hat
   =1296803367/80000.                                 (3.7)
```

Equations (2.4)--(3.7) numerically close the cone-hyperbolicity,
metric-equivalence, projection, maximum-length, and separation-metric leaves
that were qualitative in the imported proof chain.

## 4. One true branch: a numerical homogeneity-cut sum

On a target homogeneity strip `H_(+/-k)`,

```text
cp_1=cos(phi_1)<k^-2.
```

Dropping the positive unit and `cp_0` term from (2.3) gives

```text
norm(DT_s^-1)_*
 <cp_1/(2 kappa_min tau_min)
 <(144000/36337)k^-2
 <4k^-2.                                              (4.1)
```

The image of one true continuity branch is an unstable graph, so it meets
each horizontal strip at most once.  Including both grazing signs,

```text
sum_(sign=+/-) sum_(k>=k0) 4k^-2
 <8/(k0-1).                                           (4.2)
```

For the expansion-sum arithmetic, choose `k0=41`.  The one central component
costs at most (2.5), while the two grazing tails cost less than `1/5`.
Therefore

```text
Xi_1^(one true branch)
 <144000/180337+1/5
 =900337/901685
 =1-1348/901685
 <1.                                                  (4.3)
```

This is a genuine numerical one-step expansion/cut sum on a single true
continuity branch.  It does not certify that `k0=41` is large enough for all
distortion/regular-density parts of the standard-family atlas; that requires
the missing distortion leaf below.

## 5. Why the local sum is not the Growth Lemma

The global one- or `n`-step coefficient has the form

```text
Xi_n(delta)
 =sup_(|W|<=delta)
   sum_j inf_(W_(n,j)) norm(DT_s^-n)_*,                (5.1)
```

where `j` registers every true collision singularity and every homogeneity
cut.  Equation (4.3) controls only the descendants of one true continuity
branch.

Pointwise expansion cannot supply (5.1).  A piecewise-affine model with `M`
disjoint continuity branches can give every branch the same inverse
contraction `144000/180337`, while the branch sum is

```text
M(144000/180337).                                     (5.2)
```

It already exceeds one at `M=2`.  Thus a physical weighted multiplicity
ledger or an `n`-step complexity recurrence is indispensable.  The finite
horizon bounds flight lengths but does not, by itself, provide the needed
executable `delta_n` and weighted sum over all iterated singularity branches.

## 6. Why carrier `C2` is not map distortion

The existing bound `<4949` controls the curvature of the event carrier.  A
Growth Lemma also needs the oscillation of the map Jacobian on every
homogeneous branch, hence `D2T_s` information.

The exact family

```text
f_N(x)=2x+(1/(2N))sin(Nx)                              (6.1)
```

has

```text
3/2 <= f_N'(x) <= 5/2                                 (6.2)
```

uniformly in `N`, but at `x=pi/(2N)`,

```text
abs((log f_N')')=N/4 -> infinity.                     (6.3)
```

So cone and first-derivative expansion data do not determine a distortion
constant.  For the billiard instance, the missing numerical leaf is an
all-homogeneity-branch `D2T_s`/log-Jacobian oscillation ledger with the
correct grazing weights.  It cannot be replaced by the carrier-curvature
certificate.

## 7. Exact remaining dependency DAG

Numerically closed now:

1. adapted `p`-metric one-collision expansion;
2. two-sided adapted/Euclidean metric equivalence;
3. Euclidean `c_hat,Lambda` on the invariant cone;
4. `C_metric,C_cone,L_0,C_s`;
5. the high-strip inverse-contraction tail;
6. the one-continuity-branch expansion/cut sum below one.

Still required before numerical `C_gr,vartheta_gr`:

1. one homogeneity cutoff certified simultaneously for distortion and
   standard-density regularity;
2. the complete physical true-singularity weighted sum (5.1);
3. an explicit `n`-step small-curve threshold `delta_n` and complexity
   recurrence;
4. numerical `D2T_s`/Jacobian-distortion constants `C_d0,C_d`;
5. the resulting regular-density constant `C_r`.

Only after those leaves are closed can Lemma 16 yield numerical
`C_p,vartheta_p`, followed by `A0,A1` and propagated `C_fw,C_rev,q`.

## 8. Reproducibility and fail-closed behavior

Files:

```text
deliverables/cm2_gate4_numeric_growth_leaves_frontier_cert.py
deliverables/cm2_gate4_numeric_growth_leaves_frontier_verifier.py
deliverables/cm2-gate4-numeric-growth-leaves-frontier-manifest-2026-07-16.json
```

Replay:

```bash
PYTHONPATH=deliverables python \
  deliverables/cm2_gate4_numeric_growth_leaves_frontier_verifier.py \
  --replay --integrity-only

PYTHONPATH=deliverables python \
  deliverables/cm2_gate4_numeric_growth_leaves_frontier_verifier.py \
  --self-test

PYTHONPATH=deliverables python \
  deliverables/cm2_gate4_numeric_growth_leaves_frontier_verifier.py
```

Replay/integrity and mutation modes exit zero.  Live default exits `2`
because global numerical Growth constants, `C_p,vartheta_p`, propagated
costs, and Gate 4 remain unproved.
