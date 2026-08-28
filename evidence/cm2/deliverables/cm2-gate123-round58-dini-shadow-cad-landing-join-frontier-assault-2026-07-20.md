# CM2 Round 58 Gate 1/2/3: Dini, projected-shadow, CAD and landing-join frontier

Date: 2026-07-20  
Scope: the three independent structural gates and the requested Gate-2 to
Gate-4 landing join, on the frozen Round-57 carriers  
Strict verdict: **no composite gate closes.  Gate 1 gains a uniform
weighted-projective Dini criterion and an explicit same-fibre twisting
robustness radius.  Gate 2 gains the correct projected-singularity-shadow
criterion for passing from finite to infinite future plaques, and the exact
landing-redistribution join is typed.  Gate 3 gains a computable CAD
component recurrence for any branch encoding proved to fit one declared
finite-depth formula budget.  The corresponding physical Dini rows,
projected-shadow rows, stable quotient, physical formula budget, strong
restriction/Piola maps and `MT_DQ` are absent.  Gates 1/2/3 remain
`NOT_CERTIFIED`; CM2 remains `NO-GO_FOR_CLAIM`.**

## 1. Frozen baseline

This leaf is append-only and hash-pins the Round-57 Gate-1/2/3 package, the
selected numerical QNL loop, the actual Gate-2 cone-product tile and the two
Round-57 Gate-4 landing reports.  It preserves the strict baseline:

```text
Gate 1 physical full-cross/common vertex:             CERTIFIED
Gate 1 physical weighted-defect convergence:          NOT_CERTIFIED
Gate 1 same representative class H plus twisting:     NOT_CERTIFIED

Gate 2 affine cone-product candidate layers:          7/7 NON-OFFICIAL
Gate 2 immutable physical fields:                     0/17

Gate 3 fixed-depth semialgebraic atlas existence:     CERTIFIED_QUALITATIVELY
Gate 3 weak Borel/TV R_s,Q_s:                         CERTIFIED_FIXED_DEPTH
Gate 3 strong physical R_s,Q_s/Piola/MT_DQ:           NOT_CERTIFIED

Gate 4 exact time-n first-return graph:                CERTIFIED_BUT_UNPROPER
Gate 4 proper physical time-n landing kernel:          NOT_CERTIFIED
```

No statement below changes those official gate statuses.

## 2. Gate 1: weighted-projective Dini closure

### 2.1 One invariant Cauchy target for both critical coordinates

Round 57 proved that for a general gauge

```text
D_x=[[a_x,b_x],[c_x,e_x]],
p_x=b_x/a_x, q_x=c_x/e_x, Delta_x=a_x e_x-b_x c_x,

(D_y D_x^-1)_12=a_y a_x(p_y-p_x)/Delta_x,
(D_y D_x^-1)_21=e_y e_x(q_y-q_x)/Delta_x.
```

Absorb the appropriate forward/backward diagonal normalization into the two
weighted critical sequences `C_n^+` and `C_n^-`.  On every relevant local
plaque suppose one common physical registry provides

```text
|C_0^sigma(x,y)| <= H_0 d(x,y)^beta,

sup_plaque |C_(n+1)^sigma-C_n^sigma|
  <= eta_n d(x,y)^beta,      sigma in {+,-},

sum_n eta_n < infinity.                                  (2.1)
```

Then telescoping gives, uniformly in the plaque pair,

```text
|C_M^sigma-C_N^sigma|
 <= d(x,y)^beta sum_(n=N)^(M-1) eta_n,

|C_infinity^sigma-C_N^sigma|
 <= d(x,y)^beta sum_(n>=N) eta_n,

|C_infinity^sigma|
 <= (H_0+sum_n eta_n)d(x,y)^beta.                        (2.2)
```

Thus both canonical critical coordinates converge with one explicit Hölder
tail.  This is broader than the Round-29 sufficient condition `omega<m`:
an exponential rate gap implies (2.1), but cancellations or nongeometric
summable increments may also satisfy it.

The exact replay uses

```text
C_n=1-2^-n,
eta_n=2^-(n+1),
|C_infinity-C_N|=2^-N.
```

This is a conditional mathematical interface.  No physical all-plaque
increment row `eta_n` has been produced.

### 2.2 Vanishing increments are not enough

There is a sharp elementary separator.  In block `m`, start at zero, rise to
one in `m` increments of `1/m`, then fall to zero in `m` increments of
`-1/m`.  As `m` tends to infinity every increment tends to zero, but the
sequence visits both zero and one forever and does not converge.  The
certificate replays blocks `m=2,...,7` exactly over the rationals.

Consequently neither pointwise small critical increments nor a qualitative
continuity statement replaces the summable/Cauchy ledger in (2.1).

### 2.3 Same-fibre twisting needs only one explicit loop-error enclosure

The frozen selected QNL loop has interval-certified axis wedges whose
absolute values are strictly larger than

```text
10^77, 700, 10^47, 10^-28.
```

In the same physical QNL fibre and the same normalized eigenbasis, every one
of these four wedges is one signed loop-matrix entry.  Therefore

```text
||Psi_new-Psi_frozen||_max <= 10^-29                    (2.3)
```

preserves all four nonzero wedges.  This turns the final twisting replay into
a single explicit same-fibre max-entry enclosure; it does not supply that
enclosure.  Comparing matrices in a different fibre, eigenbasis or merely a
cohomologous representative does not meet (2.3).

The Gate-1 boundary is now:

```text
weighted-projective Dini/Cauchy theorem:             CERTIFIED_CONDITIONAL
same-fibre four-wedge robustness radius 10^-29:      CERTIFIED
physical all-plaque Dini increment registry:         NOT CERTIFIED
combined-gauge selected-loop error <=10^-29:         NOT CERTIFIED
same representative class H plus twisting:           NOT CERTIFIED
Gate 1:                                               NOT_CERTIFIED
```

## 3. Gate 2: singular shadows, not singular area

### 3.1 The projected-shadow theorem

Parameterize the candidate stable fibres of the Round-25 cone-product tile
by a reference base interval `I`:

```text
W_u, u in I.
```

For future depth `j`, define the **bad projected shadow**

```text
B_j={u in I:
       W_u meets the depth-j singularity, or
       its depth-j graph transform is undefined}.       (3.1)
```

This is a one-dimensional projection along the candidate fibres; it is not
the two-dimensional area of the singular set.  If every `B_j` is Borel and
one physical registry proves

```text
Leb(B_j)<=b_j,
sum_j b_j<|I|,                                          (3.2)
```

and all surviving finite graph transforms have common cone, contraction and
`C^1` compactness bounds, then

```text
Leb(I \ union_j B_j) >= |I|-sum_j b_j>0.                (3.3)
```

Every parameter in the complement has all finite transforms.  The common
compact graph-transform estimate gives an infinite stable plaque.  Once the
Round-57 Hölder distortion constants are also physically instantiated, its
holonomy product and Jacobian tail follow from the already certified
geometric-series theorem.

For a normalized base, the replay uses

```text
b_j=2^-(j+2),
sum_j b_j=1/2,
surviving base measure >=1/2.
```

This isolates the shortest real Gate-2 input: projected singular-shadow
summability plus graph-transform compactness.

### 3.2 Why null area and finite futures do not supply (3.2)

The Round-57 separator becomes exact in this language.  The line `v=0` in
the affine tile has two-dimensional area zero but meets every candidate
fibre.  Its bad shadow is all of `I`, so one such future line gives

```text
Leb_2(singularity)=0,
Leb_1(B_j)=|I|.
```

Thus collision-area nullity, arbitrarily long finite regular prefixes and
the seven affine candidate layers do not control the required transverse
shadow.  Existing a.e. local-stable-manifold and absolute-continuity results
also do not identify a full-span product base on this immutable R1 tile or
provide its branch-labelled `B_j` ledger.

Strict status:

```text
projected-shadow/graph-transform bridge:             CERTIFIED_CONDITIONAL
physical projected-shadow rows:                      0
physical stable-saturated base/projection/J_hol:      NOT_CERTIFIED
official immutable Gate-2 fields:                    0/17
Gate 2:                                               NOT_CERTIFIED
```

## 4. Gate 2 to Gate 4: can stable holonomy properize the time-n landing?

The answer has two sharply different branches.

### 4.1 Pushing to a quotient reference is only a latent lift

Let `pi^s` move a landing point along its stable plaque to a long reference
unstable interval.  The quotient image may have a proper boundary charge,
but

```text
pi^s(y) != y
```

in general.  Retaining the original landing requires an endpoint map
`Y_ref(z)=y`.  This produces a proper latent graph lift with an endpoint map,
the same legal type already obtained in Round 57.  It is not a proper
physical time-`n` landing kernel.

The exact support separator is unchanged.  With

```text
C_p=4*10^90*360493663/358863,
ell=1/(2 C_p), mass=1,
```

an isolated physical landing support of length `ell` satisfies, for every
positive same-support decomposition,

```text
Z/mass >=1/ell=2 C_p>C_p.                              (4.1)
```

Stable absolute continuity cannot fill points absent from that support.
Mapping it to a unit reference interval gives `Z/mass=1`, but changes the
physical landing point and hence falls on the latent side of the type split.

### 4.2 Same-time physical redistribution is possible only with more fields

Graph determinism is not by itself an absolute obstruction.  One may
Rokhlin-disintegrate the **same joint first-return graph measure** on the same
physical landing points, provided the target already has a suitable
physical unstable foliation.  The branch inverse then lifts every target
conditional back to its unique source and preserves the endpoint pair and
once charge.

Stable-holonomy absolute continuity alone is insufficient, however.  The
common-event restriction may leave arbitrarily short or fractured pieces on
each unstable plaque, and weak Borel disintegration gives no strong standard-
family norm.  The shortest sufficient Gate-2 to Gate-4 interface is:

1. a countable physical product-rectangle cover of the common landing
   support;
2. an immutable stable projection and two-sided Borel holonomy-Jacobian
   bounds;
3. full-span or uniformly bounded fragmentation of the common restriction
   on the physical unstable plaques;
4. same-measure unstable conditionals with density and log-distortion
   bounds;
5. the quantitative boundary charge
   `sum_W p_W/|W|<C_p`;
6. a Borel branch inverse retaining `n`, path, same-ID and half-open owner;
7. strong restriction and assembly bounds for the resulting physical
   carrier.

Under all seven fields, re-disintegration occurs at the original time `n`,
does not append a recovery clock, preserves `(source,landing)` exactly and
charges every raw point once.  Without items 3--5 it cannot beat (4.1);
without item 6 it can reshuffle graph endpoints; without item 7 it remains a
weak measure-level representation rather than the required physical strong
kernel.

Therefore this cross-gate join is `CONDITIONAL_JOIN_ONLY`, not a current
Gate-4 promotion.

## 5. Gate 3: a computable CAD budget, with its physical limit explicit

### 5.1 Conditional declared-encoding majorant

Round 57 proved semialgebraicity and Hardt finiteness at every fixed depth,
but gave no explicit complexity.  The present leaf records a reusable CAD
majorant.  For any explicitly enumerated branch formula proved to fit the
declared envelope

```text
k_n=400n+20 auxiliary/physical variables,
S_0=2000n+100 polynomial constraints,
D_0=8 maximum degree,
8*162^n branch words,                                  (5.1)
```

apply the conservative projection/lifting recurrence

```text
S_(r+1)=2(S_r D_r+1)^2,
D_(r+1)=2D_r^2,
L_r=2S_rD_r+1,

CAD_cells(n) <= product_(r=0)^(k_n-1) L_r.             (5.2)
```

The count in (5.2) accommodates coefficient, discriminant and pairwise
resultant projection polynomials and the real-root stacks at the lifting
stage.  Multiplying it by `8*162^n` bounds the declared word universe.  A
coordinate projection cannot split a connected component, so retaining the
collision times, contact normals and radical variables avoids a separate
quantifier-elimination component penalty.

The certificate independently computes the first three recurrence rows for
depths one, two and three and rechecks the Round-57 word counts through depth
five.

The scope is deliberately conditional: this leaf does **not** machine-
enumerate every physical root-comparison, specular-reflection and source-
chart polynomial and prove that it fits (5.1).  Therefore the certified
statement is

```text
CAD majorant for any formula fitting declared budget: CERTIFIED
physical circular-pilot formula budget (5.1):         NOT_CERTIFIED
```

It is not an unconditional physical component bound.

### 5.2 Unbounded depth still defeats the installed moment

Even after an actual formula budget is installed, its depth dependence
must be integrated.  An exponential clock moment alone does not pay an
arbitrary superexponential complexity majorant.  The exact separator uses

```text
p_d=2^-d, d>=1,
sum_d p_d=1.
```

Since `exp(1/6)<3/2`,

```text
sum_d p_d exp(d/6)
 < sum_d (3/4)^d=3<infinity.                            (5.3)
```

For the test growth `G(d)=d^d`, however,

```text
p_d G(d)=(d/2)^d
```

does not even tend to zero.  This proves only a logical nonimplication:
the installed `Dbar` exponential moment cannot integrate the CAD upper
majorant merely by naming it.  It does **not** assert that the physical
number of components has a `d^d` lower bound.

### 5.3 Strong restriction and directional Piola remain separate

Semialgebraic cell counts do not bound the physical anisotropic restriction
operator.  The exact determinant-one family

```text
S_n=diag(2^n,2^-n), K=e_1
```

satisfies

```text
det S_n=1,
|S_n K|=2^n.
```

Hence area preservation, weak-TV norm one and finite component count do not
give a directional Piola/current bound.  A physical strong theorem must
control branch boundaries, density traces, derivative directions and the
weighted suffix sum simultaneously.

The Gate-3 boundary is:

```text
conditional computable CAD recurrence:              CERTIFIED
physical formula-budget instantiation:              NOT_CERTIFIED
depth-integrated component/restriction bound:        NOT_CERTIFIED
strong physical R_s/Q_s:                             NOT_CERTIFIED
directional Piola suffix bound:                      NOT_CERTIFIED
MT_DQ:                                               NOT_CERTIFIED
Gate 3:                                              NOT_CERTIFIED
```

## 6. Latest-technology audit

The official arXiv API was rechecked at `2026-07-20T11:45:20Z`.  Exact query
responses were hashed before parsing:

| query | latest relevant returned record | response SHA-256 |
|---|---|---|
| `(ti:billiard OR abs:"dispersing billiard") AND (abs:holonomy OR abs:"stable manifold" OR abs:"Young tower")` | `2509.07657v2` | `52a696a784ac85a2d61fb5b35b2300aa4658d2245460fa08c28fac6c79d84067` |
| `(ti:cocycle OR abs:"linear cocycle") AND (abs:holonomy AND (abs:twisting OR abs:cohomology))` | `2604.13401v1` | `3349f389ad2b540e6a7edb309677334d81a90999d50cbf1b4b3ab160801e17a2` |
| `(abs:"dispersing billiard" OR ti:billiard) AND (abs:"linear response" OR abs:"transfer operator" OR abs:perturbation)` | `2606.10155v1` | `e8c5429717c3522177ca15b601a2d66e0a91c64efd6092a41a4063ac4cc4d99f` |

The pinned Demers--Liverani `arXiv:2606.10155v1` PDF has SHA-256

```text
3330b5467c5c7107e58ba7966a0386f2ab51415990399b387ad2f7e571f61798.
```

It reviews local stable manifolds, absolute-continuous holonomy, Young
towers and transfer-operator strong norms, but it does not bind a spanning
stable rectangle, its projected singular shadows or a physical time-`n`
landing re-disintegration to the present immutable CM2 registry.  The
cocycle and perturbation searches likewise found no result that supplies the
physical Dini rows, same-gauge loop enclosure, strong `R_s/Q_s`, directional
Piola bound or `MT_DQ`.  No theorem-name promotion is made.

## 7. Strict global verdict

```text
Gate 1:                    NOT_CERTIFIED
Gate 2:                    NOT_CERTIFIED
Gate 3:                    NOT_CERTIFIED
complete composite gates: 0/5
CM2:                       NO-GO_FOR_CLAIM
```

## 8. Replay and acceptance

```bash
python -m py_compile \
  deliverables/cm2_gate123_round58_dini_shadow_cad_landing_join_frontier_cert.py \
  deliverables/cm2_gate123_round58_dini_shadow_cad_landing_join_frontier_verifier.py

python deliverables/cm2_gate123_round58_dini_shadow_cad_landing_join_frontier_cert.py \
  --summary
python deliverables/cm2_gate123_round58_dini_shadow_cad_landing_join_frontier_verifier.py \
  --integrity-only
python deliverables/cm2_gate123_round58_dini_shadow_cad_landing_join_frontier_verifier.py \
  --replay
python deliverables/cm2_gate123_round58_dini_shadow_cad_landing_join_frontier_verifier.py \
  --self-test

# Deterministic byte-identical manifest regeneration.
python deliverables/cm2_gate123_round58_dini_shadow_cad_landing_join_frontier_cert.py \
  --reemit /tmp/cm2-round58-gate123-manifest.json
cmp /tmp/cm2-round58-gate123-manifest.json \
  deliverables/cm2-gate123-round58-dini-shadow-cad-landing-join-frontier-manifest-2026-07-20.json

# Both default entries deliberately fail close with exit 2.
python deliverables/cm2_gate123_round58_dini_shadow_cad_landing_join_frontier_cert.py
python deliverables/cm2_gate123_round58_dini_shadow_cad_landing_join_frontier_verifier.py
```

Acceptance target:

```text
syntax:                 2/2 PASS
dependency hashes:      7/7 PASS
independent replay:     PASS
hostile mutations:      67/67 REJECTED
deterministic reemit:   byte-identical PASS
artifact SHA ledger:    4/4 PASS
default entries:        2/2 exit exactly 2
```
