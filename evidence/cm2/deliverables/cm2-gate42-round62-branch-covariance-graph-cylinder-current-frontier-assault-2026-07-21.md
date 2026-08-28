# CM2 Round 62 Gate 4/2 — actual branch covariance and tagged graph-cylinder current frontier

Date: 2026-07-21  
Strict status: **the actual common first-return law now has an exact
branchwise Radon--Nikodym covariance identity, and the positive bad graph
defect has a canonical endpoint-traced normal metric-current recipient on a
tagged graph cylinder.  These are exact same-law/current interfaces.  They do
not construct invariant stable product rectangles, a physical stable
holonomy, the strict fibrewise properness inequality, a physical
phase-space anisotropic current, or an accepted strong cemetery.  Gate 2 and
Gate 4 remain `NOT_CERTIFIED`; the global state remains `0/5` and
`CM2=NO-GO_FOR_CLAIM`.**

## 1. Frozen Round-61 baseline

This leaf is append-only and changes no frozen artifact.  It pins and replays
the complete Round-61 aggregate:

```text
Round-61 aggregate report SHA256:
b9ad28ed23e88768234b304dd9f9ecb02577c7aa18dc8a982185690ea8f6f02b

Round-61 recursive ledger SHA256:
2a3ae3ebf1a6e11b734611e260a340398f475d70e4888010c8294ac321d84265
```

The pinned Gate-4 facts are

```text
0<=kappa_B<=mu_C,  g_B=d kappa_B/d mu_C, 0<=g_B<=1,

kappa_B=integral (g_B mu_omega)dP(omega),

X_D^graph={nu: integral 2^D_land d|nu|<infinity},

||Gamma_B||_X=integral_B h(y)2^D_land(y)dlambda(y)<infinity.
```

Round 61 also froze the exact *future* stable-holonomy equation

```text
g_v=(g_u o h_uv^-1)J_uv.
```

It did not supply the physical `h_uv`, `J_uv`, product quotient, marker
fragmentation, or strong assembly.  The present leaf does not reinterpret an
artificial slope-four cone foliation as invariant unstable plaques.

## 2. Actual first-return branch marker covariance

Fix one immutable tagged invertible branch

```text
H=T_s^n|U: U -> V
```

of the already certified exact raw physical first-return graph.  Let

```text
mu_V=H_#mu_U,
kappa_V=H_#kappa_U,
a=d kappa_U/dmu_U,
g_B=d kappa_V/dmu_V.
```

For every Borel `E subset V`,

```text
integral_E g_B dmu_V
 =kappa_V(E)
 =kappa_U(H^-1E)
 =integral_E (a o H^-1)dmu_V.
```

Uniqueness of Radon--Nikodym derivatives therefore gives

```text
g_B=a o H^-1       mu_V-a.e.,
a=g_B o H          mu_U-a.e.                         (2.1)
```

on every tagged branch.  Equation (2.1) is an actual same-law result, not a
conditional future interface.  The one-dimensional branch Jacobian appears
in both the marked and unmarked coordinate densities and cancels in their RN
ratio.  Thus inserting an extra `J_ell H` into (2.1) would be a type error.

This result preserves `n/path/physical-ID/half-open owner/once charge` because
the identity is asserted before branch tags are forgotten.  It is dynamic
first-return covariance.  It is **not** covariance across stable holonomy
between distinct unstable plaques.

An exact finite replay uses

```text
mu_U=(1/2,1/3,1/6),  a=(1,1/2,0),
H:0->1, 1->2, 2->0.
```

Then

```text
mu_V=(1/6,1/2,1/3),
kappa_V=(0,1/2,1/6),
g_B=(0,1,1/2)=a o H^-1.
```

## 3. Exact stable-holonomy defect cocycle

The missing physical join can now be represented by one exact defect rather
than by several qualitative surrogates.  Suppose a future physical product
rectangle supplies nonsingular bijective holonomies

```text
h_uv:u->v,
(h_uv)_#mu_u=J_uv mu_v.
```

Define the positive transfer isometry

```text
P_uv f=(f o h_uv^-1)J_uv,
||P_uv f||_L1(mu_v)=||f||_L1(mu_u),                  (3.1)
```

and the marker defect

```text
Delta_uv=g_v-P_uv g_u.                               (3.2)
```

The exact same-common-law condition is equivalent to `Delta_uv=0`
`mu_v`-a.e.  If `h_uw=h_vw o h_uv`, then

```text
P_uw=P_vw P_uv,
Delta_uw=Delta_vw+P_vw Delta_uv,                     (3.3)
||Delta_uw||_1<=||Delta_vw||_1+||Delta_uv||_1.       (3.4)
```

Thus one base-plaque registry plus zero defects on a spanning holonomy tree
would propagate the marker consistently.  Equations (3.1)--(3.4) do not
manufacture that registry or prove any physical defect zero.

For an independent rational replay take three uniform three-point fibres,
identity holonomies and

```text
g_u=(1,0,1/2),
g_v=(3/4,1/4,1/2),
g_w=(1/2,1/2,1/2).
```

Then

```text
Delta_uv=(-1/4,1/4,0),  ||Delta_uv||_1=1/6,
Delta_vw=(-1/4,1/4,0),  ||Delta_vw||_1=1/6,
Delta_uw=(-1/2,1/2,0),  ||Delta_uw||_1=1/3,
```

and (3.3) is exact.  This replay is algebraic evidence only, not a billiard
product rectangle.

## 4. Canonical tagged graph-cylinder normal current

### 4.1 The recipient

Let `Z` be the standard-Borel record space of the bad first-return graph.  A
record contains both physical endpoints and the immutable tuple

```text
(n,path,physical-ID,half-open owner,once charge,D_land).
```

Standard-Borel refinement permits a bounded complete compatible metric
`d_Z` for which the finitely many endpoint and tag coordinate maps are
continuous; adding their bounded target distances to `d_Z` makes those maps
Lipschitz without changing the Borel sets.  This topology is a bookkeeping
topology, not a new physical invariant foliation.

For a finite signed graph measure `nu`, define on
`C=[0,1]xZ` the one-dimensional metric current

```text
T_nu(f,pi)
 =integral_Z integral_0^1 f(t,z) partial_t pi(t,z) dt dnu(z).  (4.1)
```

It is the superposition of oriented unit intervals over the exact graph
records.  Standard product-current calculus gives

```text
M(T_nu)=|nu|(Z),
partial T_nu=(i_1)_#nu-(i_0)_#nu,
M(partial T_nu)=2|nu|(Z).                            (4.2)
```

The two boundary slices are disjoint, so no source/landing or tag
cancellation is hidden in the last equality.  Pushing the two traces through
their Lipschitz record-coordinate maps gives exactly

```text
(pr_landing)_#nu  and  (pr_source)_#nu.              (4.3)
```

Hence the Round-61 positive bad measure has a legitimate endpoint-traced
normal metric-current recipient.

### 4.2 How the dyadic moment pays it

Put `w(z)=2^D_land(z)>=1`.  The ordinary current `T_nu` preserves the
physical charge and obeys

```text
M(T_nu)+M(partial T_nu)=3|nu|(Z)<=3||nu||_X.         (4.4)
```

The weighted companion has the exact mass identity

```text
M(T_(w nu))=integral w d|nu|=||nu||_X,
M(partial T_(w nu))=2||nu||_X.                       (4.5)
```

Its endpoint traces are the **weighted** measures `w nu`, not `nu`.
The original trace is recovered only by multiplying the two boundary
0-currents by `w^-1=2^-D_land`:

```text
w^-1 partial T_(w nu)=partial T_nu.                  (4.6)
```

Equation (4.6) is recorded explicitly to prevent a weighted/unweighted
charge substitution.

For the three Round-61 replay atoms

```text
(mass,D)=(3/20,2),(1/80,5),(1/320,7),
```

the exact totals are

```text
|nu|(Z)=53/320,
M(partial T_nu)=53/160,
||nu||_X=M(T_(w nu))=7/5,
M(partial T_(w nu))=14/5.
```

### 4.3 Exact hybrid identity in the recipient

For the positive bad graph measure `Gamma_B`, the trace map is injective:
`(i_1)^* partial T_Gamma_B=Gamma_B`.  Consequently the full original-time
graph identity becomes

```text
Gamma_cap
 =Gamma_G+trace_1(partial T_Gamma_B).                (4.7)
```

All physical endpoints, first-hit semantics, immutable tags and the single
parent charge remain present.  This gives `4/5` in a newly typed
**tagged graph-cylinder normal-current ledger**: positive embedding, exact
tags, norm payment, and exact full=good+bad recovery are complete; downstream
CM2 acceptance is absent.

### 4.4 Exact type boundary

The current lives on the bookkeeping cylinder `[0,1]xZ`.  It is not a
current in collision phase space, not an anisotropic distribution space for
the billiard transfer operator, and not a Piola-compatible moving-domain
carrier.  The positive bad law remains ordinary collision-SRB mass and is not
renamed singular/collision-null cemetery.

A sharp logical separator makes this distinction unavoidable.  Let the
physical endpoint space be the discrete two-point space `{a,b}` and take one
record from `a` to `b`.  The graph cylinder carries the unit interval current
with boundary `delta_b-delta_a` in its labelled traces.  Every metric
1-current on the discrete physical space itself is zero, so no physical
current there can have that boundary.  This is a type/nonimplication model,
not a billiard realization.

## 5. Quantitative properness remains unpaid

The actual branch covariance (2.1), the future defect calculus (3.1)--(3.4)
and the current lift (4.1) do not bound marker fragmentation.  In particular,
they supply none of the actual quantities in

```text
F(u)R(u)<C_p theta(u)L(u).                            (5.1)
```

Round 60's two smooth perfect-product separators already show that even
physical product coordinates, identity holonomy, constant densities, zero
log distortion, exact inverse and finite assembly do not force (5.1): short
plaque debt and fragmentation debt are independent.  Round 61's smooth
`g_N` separator additionally shows that the installed scalar `D_land` moment
does not control marker BV/derivative trace.  The present current construction
does not change any of those facts.

The seven-field landing join therefore remains:

| # | physical landing field | Round-62 state |
|---:|---|---|
| 1 | physical invariant product rectangles | `PARTIAL`: exact tagged finite-depth cone-curve atlas only |
| 2 | stable projection/two-sided `J_hol` | `NOT_CERTIFIED`; exact defect calculus only |
| 3 | full span/marker fragmentation | `NOT_CERTIFIED` |
| 4 | same-law conditionals/density bounds | `PARTIAL`: actual dynamic branch RN covariance; no stable quotient or two-sided density bounds |
| 5 | physical boundary charge below `C_p` | `NOT_CERTIFIED` |
| 6 | tagged Borel branch inverse | `CERTIFIED` (Round 59) |
| 7 | strong restriction/assembly | `PARTIAL`: exact graph-cylinder normal-current assembly; no physical strong operator assembly |

The complete count stays `1/7`; Gate 2's official immutable score stays
`0/17`.

## 6. Downstream audit

The original first-hit predicate and intermediate `C24` avoidance are
retained recordwise in (4.7).  This is an exact semantic preservation result,
but not an accepted killed strong kernel.  The remaining implications fail
at their declared types:

- the good landing subkernel may have zero mass and source properness is not
  inferred;
- `D_land` is not a later/repeated recovery clock;
- normal graph-cylinder mass is not physical `q in L^(6/5)`;
- no same-law all-time forward/reverse Jordan ledger is produced;
- ordinary positive bad mass is not a collision-null singular cemetery;
- no transfer operator acts on the cylinder current and no Piola or
  `MT_DQ` intertwining has been installed.

## 7. Latest official-technology audit

The current official arXiv surface was checked through 2026-07-21.  No new
`2607` entry was found that supplies the pinned Liouville/SRB common-landing
product quotient, marker fragmentation/inverse-length estimate, or a
moving-billiard strong current/Piola theorem.

The closest entries remain:

- Climenhaga--Day `2604.25881v1`: total image-length and product-law results
  for the measure of maximal entropy, not the pinned common Liouville/SRB
  marker; total length does not control component inverse lengths;
- Canestrari `2604.19671v2`: evolution of an already regular standard family
  with survival-mass normalization, not construction of the present landing
  regularity or strict threshold;
- Demers--Liverani `2606.10155v1`: a transfer-operator review, not a theorem
  installing this graph carrier in a physical strong/Piola space.

No external theorem is promoted into the certificate.

## 8. Strict frontier

```text
actual first-return branch RN covariance:             CERTIFIED_EXACT
physical stable-holonomy marker covariance:           NOT_CERTIFIED
holonomy defect/isometry/cocycle interface:            CERTIFIED_EXACT
physical invariant product quotient and J_hol:         NOT_CERTIFIED
fibrewise F R<C_p theta L:                             NOT_CERTIFIED
tagged graph-cylinder normal current:                  CERTIFIED_EXACT
D_land pays ordinary+weighted cylinder current norms: CERTIFIED_EXACT
physical anisotropic/current/Piola recipient:          NOT_CERTIFIED
downstream accepts positive bad current:               NOT_CERTIFIED
seven-field landing join:                              1/7; fields 1,4,7 partial
official immutable Gate-2 fields:                      0/17
proper physical same-ID first-return kernel:           NOT_CERTIFIED
original R_n intermediate C24 avoidance:               CERTIFIED (pinned)
later/repeated recovery-clock moments:                 NOT_CERTIFIED
physical q in L^(6/5):                                 NOT_CERTIFIED
strong singular/current cemetery:                      NOT_CERTIFIED
Gate 2:                                                NOT_CERTIFIED
Gate 4:                                                NOT_CERTIFIED
complete composite gates:                              0/5
CM2:                                                   NO-GO_FOR_CLAIM
```

## 9. Executable evidence

- `cm2_gate42_round62_branch_covariance_graph_cylinder_current_frontier_cert.py`;
- `cm2_gate42_round62_branch_covariance_graph_cylinder_current_frontier_verifier.py`;
- `cm2-gate42-round62-branch-covariance-graph-cylinder-current-frontier-manifest-2026-07-21.json`;
- `cm2-gate42-round62-branch-covariance-graph-cylinder-current-frontier-manifest-2026-07-21.sha256`.

The suite pins the Round-61 aggregate and both relevant Round-61 leaves,
replays their semantic inputs, independently checks the branch RN transport,
holonomy-defect cocycle, ordinary/weighted current mass and boundary
identities, exact trace recovery, strict nonpromotion, deterministic
regeneration and byte-identical re-emission.  Both default entry points fail
closed with exit code `2`.
