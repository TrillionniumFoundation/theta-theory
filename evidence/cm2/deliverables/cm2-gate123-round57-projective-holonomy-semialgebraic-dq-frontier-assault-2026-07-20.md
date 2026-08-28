# CM2 Round 57 Gate 1/2/3: projective holonomy and semialgebraic DQ frontier

Date: 2026-07-20  
Scope: the three independent structural gates, on the frozen Round-56
physical carriers  
Strict verdict: **no composite gate closes.  Gate 1 gains a
gauge-order-independent exact critical-coordinate interface; Gate 2 gains an
explicit stable-holonomy product/tail bound and a sharp finite-prefix
separator; Gate 3 gains a qualitative finite-parameter common branch atlas at
every fixed depth and norm-one weak Borel/TV lift and assembly maps.  The
physical twisting replay, invariant stable quotient, strong restriction
bounds, directional Piola estimate and `MT_DQ` remain absent.  CM2 remains
`NO-GO_FOR_CLAIM`.**

## 1. Frozen baseline and what changes

This append-only leaf hash-pins the Round-56 independent audit and the
strongest surviving Gate-1/2/3 carriers.  In particular it preserves:

```text
Gate 1 physical full-cross/common vertex:              CERTIFIED
Gate 1 same representative class-H plus twisting:      NOT CERTIFIED

Gate 2 candidate affine cone-product layers:           7/7 NON-OFFICIAL
Gate 2 immutable physical fields:                      0/17

Gate 3 complete finite-s future side-owner current TV: <=518152320
Gate 3 fixed free graph-current slots:                  41,508
Gate 3 physical strong Q_s/R_s and MT_DQ:               NOT CERTIFIED
```

The new Gate-3 statement is qualitative and fixed-depth.  It is stronger than
the former absence of any finite-`s` future atlas, but deliberately weaker
than the physical strong-space and growing-depth theorem required by
`MT_DQ`.

## 2. Gate 1: every gauge order has the same weighted projective frontier

### 2.1 Exact general identity

Let one pointwise gauge chart be

```text
D_x=[[a_x,b_x],[c_x,e_x]],
Delta_x=a_x e_x-b_x c_x !=0,
p_x=b_x/a_x,
q_x=c_x/e_x.
```

On a chart where `a_x,e_x,a_y,e_y` are nonzero, direct `2x2` algebra gives

```text
(D_y D_x^-1)_12
  =a_y a_x (p_y-p_x)/Delta_x,

(D_y D_x^-1)_21
  =e_y e_x (q_y-q_x)/Delta_x.                         (2.1)
```

The certificate verifies (2.1) on three independent exact rational rows; the
verifier uses three different rows.  Thus the canonical critical coordinates
are not intrinsically “upper shear” and “lower shear” differences.  They are
the two **weighted projective defects** in (2.1).

This unifies the earlier order-dependent calculations:

```text
D=U_v L_u:
  lower =du,
  upper =dv-v_y du v_x;

D=L_u U_v:
  upper =dv,
  lower =du-u_y u_x dv;

D=[[1,v],[u,1]]:
  upper =dv/(1-u_x v_x),
  lower =du/(1-u_x v_x).                              (2.2)
```

Changing the order moves the nonlinear compatibility term from one
projective chart to the other.  Replacing the product by an additive gauge
moves it into the determinant weight; it does not remove it.

### 2.2 Uniform invertibility does not make the weight converge

The exact additive-gauge countermodel uses

```text
R_n=2^-n,
u_x=1/2,
u_y-u_x=2^-n/10,
v_x=v_y=0       for even n,
v_x=v_y=1/2     for odd n.
```

Every gauge is uniformly invertible; the determinant is strictly at least
`29/40`.  Nevertheless

```text
(D_y D_x^-1)_21/R_n
  =1/10,2/15,1/10,2/15,...,
```

so the normalized critical coordinate has no limit.  This is stronger than
the previous product-shear amplitude separator: even a bounded additive
gauge with determinant uniformly separated from zero can fail by an
oscillating weight.

### 2.3 Exact physical boundary

The last Gate-1 input can now be stated invariantly.  One actual combined
physical gauge must make both weighted projective defects in (2.1) converge
with the required plaque Hölder modulus after diagonal normalization.  The
Round-29 `omega<m` estimate remains one sufficient way to do this, but merely
reordering or adding the one-sided Green shears is not a third route.

After that convergence is proved, all selected twisting wedges must still be
recomputed in that identical gauge.  Therefore:

```text
general weighted-projective critical identity:          CERTIFIED
shear-order/additive-gauge no-free-lunch separator:      CERTIFIED
physical weighted-defect convergence:                   NOT CERTIFIED
same representative class H plus twisting:              NOT CERTIFIED
Gate 1:                                                  NOT CERTIFIED
```

## 3. Gate 2: an exact holonomy-product interface and a codimension-one gap

### 3.1 Quantitative stable-holonomy product theorem

Suppose one actual stable plaque family on a common registry supplies

```text
d(T^n x,T^n y)<=C_s lambda^n d(x,y),
|log J^uT(z)-log J^uT(z')|<=H d(z,z')^alpha,
0<lambda^alpha<1.
```

Then the logarithm of the usual stable-holonomy Jacobian product converges
absolutely, and

```text
|log J_hol(x,y)|
 <=K=H C_s^alpha d(x,y)^alpha/(1-lambda^alpha),

|log J_hol-log J_hol^(N)|
 <=K lambda^(alpha N),

exp(-K)<=J_hol<=exp(K).                               (3.1)
```

The exact replay uses `H=3`, `C_s=2`, `d=1/8`,
`lambda^alpha=1/2`.  It gives

```text
K=3/2,
tail_N=(3/2)2^-N.
```

Thus once physical spanning plaques, `C_s`, `lambda`, `H` and `alpha` are
registered on the selected tile, the holonomy Jacobian and its two-sided
bound require no additional qualitative theorem.  Equation (3.1) is a
conditional interface, not a current physical field promotion.

### 3.2 Zero area can still destroy every spanning candidate fibre

Positive two-dimensional mass and arbitrarily long finite regular prefixes
do not prove an infinite homogeneous stable product.  For any declared
finite depth `N`, compare two abstract future-cut models on the Round-25
candidate coordinate square:

```text
|u|,|v|<=1/25600,
candidate stable fibres: u=constant.
```

The models have identical regular data through depth `N`.  The good model has
no next cut.  The second model introduces only the line `v=0` at depth
`N+1`.  That line has two-dimensional area zero but meets every spanning
candidate fibre.  Hence the good model has spanning fibres and the cut model
does not.  The certificate replays the construction for
`N=1,2,5,17,257`.

This is a logical nonimplication, not a claim that the physical billiard
realizes the separator.  It proves that finite-depth branch coverage, an
area-null singular set, and the seven affine candidate layers cannot replace
an infinite homogeneous future-domain theorem.

The strict Gate-2 boundary is therefore:

```text
conditional holonomy product and tail:                 CERTIFIED
finite-prefix spanning-plaque separator:                CERTIFIED
physical invariant stable-saturated base/projection:    NOT CERTIFIED
immutable physical fields:                              0/17
Gate 2:                                                  NOT CERTIFIED
```

## 4. Gate 3: fixed-depth semialgebraic common atlas

### 4.1 Why the circular pilot is semialgebraic at finite depth

The CM2 pilot has two rational-radius circular scatterers, centres affine in
`s`, eight source chart cells, and a conservative finite horizon alphabet of

```text
2 obstacle types * 9 * 9 torus lifts = 162 targets per collision.
```

Use auxiliary nonnegative radical and flight-time variables.  Each source
normal and velocity chart is described by polynomial equalities and sign
inequalities.  A candidate collision satisfies

```text
|q+tau u-C_j(s)|^2=R_j^2,
tau>0,
```

together with finitely many least-positive-root comparisons.  Specular
reflection is polynomial once the contact normal is included:

```text
u_plus=u_minus-2(u_minus dot n)n.
```

At every fixed depth `n`, a branch word therefore gives a finite Boolean
combination of polynomial equalities and inequalities in the physical and
auxiliary variables.  Tarski--Seidenberg projection preserves
semialgebraicity.  Semialgebraic sets have finitely many connected
components, and Hardt triviality gives a finite parameter stratification on
the compact window `|s|<=1/400` with fixed component labels and empty slots.
Regular cells carry the ordinary real-analytic billiard branch; singular and
grazing cells remain in a cemetery slot.

The raw branch-word universes, before emptiness and connected-component
resolution, are exactly

| depth `n` | `8*162^n` words |
|---:|---:|
| 1 | 1,296 |
| 2 | 209,952 |
| 3 | 34,012,224 |
| 4 | 5,509,980,288 |
| 5 | 892,616,806,656 |

These counts are not component counts and are not proposed as an efficient
enumeration.  Their role is to certify a finite universal word carrier at
every fixed `n`.

The resulting theorem is:

```text
for every fixed finite n:
  finite full-parameter semialgebraic branch atlas exists;
  a finite Hardt parameter stratification exists;
  fixed component labels with empty slots exist;
  regular branches are analytic;
  singular/grazing strata are retained.
```

This closes qualitative fixed-depth atlas existence.  It gives no explicit
cell list, degree bound, boundary-`Z` constant, or depth-uniform complexity.

### 4.2 Weak Borel/TV lift and assembly

For one fixed depth and parameter, let the finite atlas cells be `C_a(s)`,
including the cemetery.  On finite signed Borel measures define

```text
R_s mu=(1_{C_a(s)}mu)_a,
Q_s(nu_a)=sum_a nu_a
```

with the appropriate physical pushforward on output slots.  Disjointness
gives exactly

```text
||R_s mu||_l1(TV)=||mu||_TV,
||Q_s(nu_a)||_TV<=sum_a||nu_a||_TV,
Q_s R_s=Id.                                           (4.1)
```

Componentwise branch pushforward then gives the bulk identity

```text
Q_s^out P_hat_s^n R_s=P_s^n                           (4.2)
```

on the regular bulk.  The verifier independently replays (4.1) on signed
masses `1/3,-1/6,1/2`: source `l1` TV is one and merged output TV is `2/3`.

Equations (4.1)--(4.2) are weak Borel/TV maps only.  Characteristic
restrictions in a physical strong anisotropic space create boundary traces;
their norm is not controlled by (4.1).  The existing complete future current
and 41,508-slot free carrier therefore remain useful but are not promoted to
physical strong `R_s/Q_s`.

### 4.3 Reusable uniform-component theorem and its limit

There is one safe uniform version.  Fix depth `n` and a compact
semialgebraic family of regular input intervals whose defining format and
degree are uniformly bounded by `B`.  The same argument plus uniform
semialgebraic finiteness gives some

```text
N(n,B)<infinity
```

uniform over `|s|<=1/400` and over that input family, bounding the number of
interval components created by the `n`-step singular/branch partition and
any fixed finite family of terminal `C24` predicates.  A fixed finite list of
artificial homogeneity cuts may be included by increasing `B`; an unbounded
homogeneity-strip index cannot be hidden in this statement.

This theorem does **not** currently close Gate-4 `J_cap`.  On a
preproperisation stratum `{Dbar=d}`, fully cutting the orbit makes every leaf
a regular interval on which `T_s^(696d)` is a diffeomorphism.  But before
that cut one physical fibre is generally a finite whole family, and its
semialgebraic complexity `B(d)` grows with `696d`.  Since `Dbar` is unbounded,
fixed terminal time `H_joint` gives only

```text
N(H_joint,B(d))<infinity for each d,
```

not one global `N_H`.  Bounded curvature and properness alone do not bound
the number of intersections of an analytic curve with a fixed analytic
boundary.  A global `J_cap` deduction still needs one of:

1. a uniform bound `B(d)<=B_*`;
2. a quantitative growth bound on `N(H_joint,B(d))` integrable against the
   installed `Dbar/J_pair` moment; or
3. a hereditary standard-family **average-`Z`** intersection theorem.

This limitation prevents misuse of a qualitative Hardt theorem as a global
uniform complexity estimate.

## 5. Gate-3 strict boundary

Certified in this leaf:

```text
fixed-depth full-parameter semialgebraic branch atlas: CERTIFIED_QUALITATIVELY
fixed-depth weak Borel/TV R_s and Q_s:                  CERTIFIED_NORM_ONE
regular-bulk fixed-depth intertwining:                  CERTIFIED
uniform N(n,B) for fixed definable input complexity:    CERTIFIED_EXISTENTIALLY
```

Not certified:

```text
explicit or depth-uniform atlas complexity:             NOT CERTIFIED
uniform boundary-Z / strong restriction invariance:     NOT CERTIFIED
physical strong R_s/Q_s:                                NOT CERTIFIED
directional Piola/coboundary suffix bound:              NOT CERTIFIED
operator-norm DQ and MT_DQ:                             NOT CERTIFIED
Gate 3:                                                  NOT CERTIFIED
```

## 6. Latest-technology check

The official arXiv API was rechecked at `2026-07-20T08:17:40Z`.  The latest
directly relevant search results remain:

- Kalinin--Sadovskaya, `arXiv:2604.13401v1`, for periodic-data cocycle
  rigidity;
- Demers--Liverani, `arXiv:2606.10155v1`, for dispersing-billiard transfer
  operators and the still-open characteristic-restriction frontier;
- Canestrari, `arXiv:2604.19671v2`, for fixed-billiard small-hole linear
  response.

The Round-56 audit already hash-pins the official PDFs and checks their
hypotheses.  No later official result found in the new query constructs the
CM2 same-representative gauge, stable quotient, physical strong current maps,
or `MT_DQ`.  The Gate-3 advance here is direct semialgebraic geometry, not a
theorem-name substitution.

## 7. Strict global verdict

```text
Gate 1:                    NOT_CERTIFIED
Gate 2:                    NOT_CERTIFIED
Gate 3:                    NOT_CERTIFIED
complete composite gates: 0/5
CM2:                       NO-GO_FOR_CLAIM
```

## 8. Replay

```bash
python -m py_compile \
  deliverables/cm2_gate123_round57_projective_holonomy_semialgebraic_dq_frontier_cert.py \
  deliverables/cm2_gate123_round57_projective_holonomy_semialgebraic_dq_frontier_verifier.py

python deliverables/cm2_gate123_round57_projective_holonomy_semialgebraic_dq_frontier_cert.py \
  --summary
python deliverables/cm2_gate123_round57_projective_holonomy_semialgebraic_dq_frontier_verifier.py \
  --integrity-only
python deliverables/cm2_gate123_round57_projective_holonomy_semialgebraic_dq_frontier_verifier.py \
  --replay
python deliverables/cm2_gate123_round57_projective_holonomy_semialgebraic_dq_frontier_verifier.py \
  --self-test

# Both default entries deliberately fail close with exit 2.
python deliverables/cm2_gate123_round57_projective_holonomy_semialgebraic_dq_frontier_cert.py
python deliverables/cm2_gate123_round57_projective_holonomy_semialgebraic_dq_frontier_verifier.py
```

Exit `2` means that the frontier package is valid while no composite claim is
certified.  Integrity or semantic replay failure exits `1`.
