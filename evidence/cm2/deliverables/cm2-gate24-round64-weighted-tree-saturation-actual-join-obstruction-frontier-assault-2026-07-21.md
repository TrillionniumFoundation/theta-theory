# CM2 Round 64 Gate 2/4 — weighted-tree saturation, actual-data join, and strong-assembly obstruction

Date: 2026-07-21  
Strict status: **this leaf gives a genuinely many-plaque exact calculus.  On
any finite weighted holonomy tree, stable-saturation distance is the
integral of the pointwise weighted-median cost.  Its pairwise dispersion
`P` satisfies the sharp universal sandwich `P <= delta_sat <= 2P`; zero
saturation is equivalent to zero marker defect on every spanning-tree edge.
The same tree carries an exact branch-square transport law and a root-to-all
plaques quantitative distortion budget.  A field-level join of the pinned
actual branch, owner and landing artifacts finds all five available physical
fragments but no instantiable physical stable tree.  A smooth four-plaque
separator additionally shows that zero defect plus the strict scalar
properness budget still does not imply uniform BV/derivative strong
assembly.  No physical invariant product rectangle, stable holonomy, zero
actual marker defect, actual strict `F,R,theta,L,m,M` budget, or physical
strong restriction/assembly is constructed.  Gate 2 and Gate 4 remain
`NOT_CERTIFIED`; the global state remains `0/5` and
`CM2=NO-GO_FOR_CLAIM`.**

## 1. Frozen recursive root and actual inputs

This append-only leaf edits no frozen artifact.  It pins the complete Round
63 recursive root, the Round-63 independent audit, the complete Round-63
Gate-2/4 leaf, and the actual physical fragments used by the join.

```text
Round-63 aggregate report / recursive ledger:
9cde412ba689be87d777906404c9c9426a2a8a102385a2c4c510df8f9b7a6a05
a0b512f32914ef2692b31466a4ea156c44698b1eaf44d8ead45b2c74ee73230e

Round-63 independent audit report / manifest / ledger:
b30aff208e9e5707e443f59abd07507f7f9d93d765ecaf3fd675f4150c5bf978
3aae6d018fc15aaab47116d311eed8333c56b87542b0b5761b849221cbf76d6b
8227dd32e36d2879f9dbbdced54f3c50b3eac1536ce8fceac480d22cb8617bfd

Round-63 Gate-2/4 report / manifest / ledger:
e57ba8db9a7ab0a8dc7643b575d02de99a10377ce36ba0efd1ba8ae75477325c
955908ee74ff6ec0354224978850ef683aeacd1923ce85bffd1290467321d23f
a739ffbe1bb9f14fdc8c72c573594f56930a7c4f32efb77fa4dac60d256ec870
```

The used actual manifests are pinned exactly:

```text
Round-59 tagged branch inverse / same-graph reconditioning:
e7305e0b72eed28bc68b115e1201fc02e2b66d3cc95906fc6d1efc5e9463a4f5

Round-60 collision-SRB landing RN marker:
08cda3c966ce03967471c5d87216f4b32ee29a293d81d9dcdd434eb39f7696b3

Round-61 actual tagged cone-curve marker lift:
2edf4d7801525c746c619cb85b39c59d30018df7c6971f5e48639dc390573b9b

Round-62 actual tagged first-return branch RN covariance:
e0b89d604e89852b574638428a60daa1f6e8231b85177230a5dd67615205bad1

Round-58 physical owner/root law:
27c5d2e9a6ac9ed8eeb3d42dc96aa1c0a8faa8e50e006811efea22b45c86b859
```

These inputs certify actual dynamic branch covariance, a physical ambient
landing marker, a tagged finite-depth curve-measure lift, a Borel branch
inverse retaining `n/path/physical-ID/half-open-owner`, and a finite physical
owner/root law.  None asserts an invariant unstable/stable product quotient.

## 2. Exact finite weighted-tree saturation theorem

### 2.1 Common-root formulation

Let `T` be a finite rooted tree with node set `I`, positive outer weights
`w_i` summing to one, and probability reference laws `mu_i` on its plaques.
Every oriented tree edge is a bijective nonsingular stable holonomy, so the
path from the root `r` to node `i` induces a positive onto `L1` isometry

```text
P_ri:L1(mu_r)->L1(mu_i).
```

For plaque markers `g_i`, pull all of them to the root:

```text
f_i=P_ri^-1 g_i in L1(mu_r).
```

Define the distance to one common quotient marker by

```text
delta_T(g)
 =inf_f sum_i w_i ||g_i-P_ri f||_L1(mu_i)
 =inf_f integral sum_i w_i |f_i(x)-f(x)| dmu_r(x).       (2.1)
```

Because there are finitely many measurable `f_i`, one can select a
measurable pointwise weighted median `m(x)`.  The scalar weighted-median
property and Tonelli then give the exact formula

```text
delta_T(g)
 =integral min_t sum_i w_i |f_i(x)-t| dmu_r(x)
 =sum_i w_i ||f_i-m||_1.                                (2.2)
```

Thus no global nonlinear quotient optimization remains once an actual
rooted holonomy tree exists.  The quotient marker is the weighted median.
This strictly shortens the missing zero-saturation interface: it is enough
to supply one root law, a spanning tree of positive onto `L1` isometries,
and zero marker defect on each tree edge.  One need not separately guess a
global quotient marker.

### 2.2 Pairwise dispersion and sharp constants

Put

```text
P(g)=sum_(i<j) w_i w_j ||f_i-f_j||_1.                  (2.3)
```

For every scalar competitor `t`, triangle inequality yields

```text
sum_(i<j) w_i w_j |f_i-f_j|
 <=sum_i w_i(1-w_i)|f_i-t|
 <=sum_i w_i|f_i-t|.
```

Conversely, average the competitor costs obtained by choosing `t=f_k`
with probability `w_k`; their average is exactly `2P`.  Hence

```text
P(g) <= delta_T(g) <= 2P(g).                           (2.4)
```

Both constants are sharp: the upper equality occurs for two equal-weight
atoms, while the lower ratio tends to one for a vanishing-weight outlier.

For an edge `e=(p,c)`, let

```text
d_e=||g_c-P_pc g_p||_1
```

and let `W_e` be the total outer weight below `c`.  Tree paths give

```text
delta_T
 <=min{sum_e W_e d_e,
       2 sum_e W_e(1-W_e)d_e},                         (2.5)

delta_T
 >=max_e min(w_p,w_c)d_e.                              (2.6)
```

In particular,

```text
delta_T=0
 iff every pulled marker f_i is equal a.e.
 iff d_e=0 on every spanning-tree edge.                (2.7)
```

Equation (2.6) is a quantitative falsification rule: one positive actual
edge defect rules out stable saturation without solving (2.1).

### 2.3 Four-plaque exact replay

The executable replay uses weights

```text
(w_0,w_1,w_2,w_3)=(1/10,2/10,3/10,4/10),
```

uniform five-point root law, identity stable transports, and tree edges
`0->1`, `0->2`, `2->3`.  Its pointwise weighted-median marker is

```text
(1/4,1/4,1/2,3/4,3/4),
```

and exact arithmetic gives

```text
delta_T=3/20,
P=19/200,
2P=19/100,
root-competitor tree bound=6/25,
pairwise tree-path bound=129/500,
edge lower obstruction=21/200.
```

All inequalities are strict in this replay.  Applying one common cyclic
invertible dynamic branch to all four plaques preserves the median cost,
pairwise dispersion and every edge norm exactly.

## 3. Whole-tree branch--holonomy square calculus

For every edge `e=(p,c)` let `P_e^S,P_e^L` be source and landing stable
density transfers and let the actual tagged branch transfers be
`D_i f=f o H_i^-1`.  Define

```text
Delta_e^S=a_c-P_e^S a_p,
Delta_e^L=g_c-P_e^L g_p,
C_e=D_c P_e^S-P_e^L D_p.                              (3.1)
```

The exact edge identity is

```text
Delta_e^L=D_c Delta_e^S+C_e(a_p).                     (3.2)
```

Therefore

```text
||Delta_e^S||_1-||C_e(a_p)||_1
 <=||Delta_e^L||_1
 <=||Delta_e^S||_1+||C_e(a_p)||_1.                   (3.3)
```

Combining (2.5)--(2.6) with (3.3) gives the explicit whole-tree bounds

```text
delta_T^L
 <=2 sum_e W_e(1-W_e)
          (||Delta_e^S||_1+||C_e(a_p)||_1),           (3.4)

delta_T^L
 >=max_e min(w_p,w_c)
          (||Delta_e^S||_1-||C_e(a_p)||_1)_+.         (3.5)
```

If every square commutes, path composition gives

```text
D_i P_ri^S=P_ri^L D_r
```

on every node.  Since `D_r` is an onto `L1` isometry, it bijects all
quotient-marker competitors, and consequently

```text
delta_T^L=delta_T^S,        P_L=P_S.                  (3.6)
```

This is the exact many-plaque upgrade of Round 63.  It does not make either
distance zero: exact dynamics transports stable-saturation debt over the
entire tree.

## 4. Root-to-all-plaques strict quantitative budget

Assume the zero-defect tree has a root retained set with at most `F_r`
components, retained fraction `theta_r`, adapted length `L_r`, and density
ratio `R_r`.  On each edge let the adapted-arclength derivative satisfy

```text
0<m_e<=dh_e/ds<=M_e.
```

For node `i`, form the path products

```text
m_i=product_(e in path(r,i)) m_e,
M_i=product_(e in path(r,i)) M_e.                     (4.1)
```

Repeated exact density transport gives

```text
F_i=F_r,
|E_i|>=m_i theta_r L_r,
R_i<=R_r M_i/m_i,
z_i<=F_r R_r M_i/(m_i^2 theta_r L_r).                (4.2)
```

Hence one root tuple and two constants per tree edge suffice:

```text
F_r R_r max_i(M_i/m_i^2)<C_p theta_r L_r             (4.3)
```

implies the strict scalar bound simultaneously on every plaque.  This is a
strict shortening from six unrelated values on every plaque.  It remains a
conditional interface because no actual physical tree or any actual input
to (4.3) exists.

The rational replay has root tuple `(3,4,1/2,2)` and edge bounds

```text
0->1: (m,M)=(1/2,3/2),
0->2: (m,M)=(2/3,4/3),
2->3: (m,M)=(3/4,5/4).
```

The node bounds are exactly `12,72,36,80`, all below the frozen `C_p`.
They are arithmetic witnesses only.

## 5. Actual branch/owner/landing join

The executable join reads the five pinned actual manifests, not prose
summaries.  Its positive matches are:

1. Round 59 supplies a Borel tagged branch inverse and same-graph
   reconditioning retaining `n/path/ID/owner` almost surely.
2. Round 60 supplies the actual collision-SRB landing RN marker
   `g_B=d kappa_B/d mu_C`, `0<=g_B<=1`.
3. Round 61 supplies an exact countable tagged finite-depth cone-curve
   measure lift of that marker, while explicitly denying that the proof
   foliation is an invariant Rokhlin/stable-holonomy product.
4. Round 62 supplies actual branchwise dynamic RN covariance on every
   frozen `n/path/physical-ID/half-open-owner` branch.
5. Round 58 supplies a finite standard-Borel physical owner/root law on
   `A_col`, while explicitly leaving coverage and all-depth moments open.

The relational join then fails closed at the first cross-plaque key.  None
of the pinned actual artifacts supplies all of

```text
tree ID and root plaque;
positive outer plaque weights on one common root law;
source and landing stable-holonomy edge IDs and RN Jacobians;
edge square commutators on the same branch keys;
edge marker defects on the collision-SRB marker;
root F,R,theta,L and edge m,M in one adapted arclength;
one endpoint-preserving strong recipient/intertwiner.
```

In particular, the Gate-5 owner law `nu`, the landing collision-SRB law
`mu_C`, and the weak quotient law `eta` are not identified by a certified
stable-tree crosswalk.  Their names or common owner tags cannot be used as a
measure-law equality.  The actual anti-join is thus a falsifiable missing-key
certificate, not a declaration that a future physical tree is impossible.

The shortest actual zero-saturation route is now exact: materialize the root
law and spanning stable tree, compute every edge defect, and prove each is
zero.  A separate global quotient-marker construction is unnecessary.  If
any edge has certified positive norm, (2.6) immediately falsifies zero
saturation.

## 6. Zero defect plus strict scalar budget still does not assemble strongly

On four identity product plaques with arbitrary positive weights, use the
same smooth marker

```text
g_N(x)=1/2+(1/4)sin(2 pi N x),      0<=x<=1.
```

Take identity stable holonomies and identity dynamic branches.  Then for
every positive integer `N`,

```text
delta_T=0,
C_e=0 and Delta_e^S=Delta_e^L=0 on every edge,
F=1, R=3, theta=1, L=1,
F R/(theta L)=3<C_p,
integral_0^1 |g_N'(x)| dx=N.                          (6.1)
```

Thus exact product geometry, whole-tree zero marker defect and the strict
scalar properness inequality coexist with unbounded plaquewise
BV/derivative trace.  These weak/scalar rows cannot by themselves produce a
uniform strong recipient that controls such variation.  This exact smooth
logical separator is not a billiard realization and does not claim to rule
out every possible anisotropic norm; it keeps the required physical
restriction/intertwining/Piola assembly as an independent debt.

## 7. Latest official-source audit

The official arXiv API was checked on 2026-07-21.

- `arXiv:2604.25881v1`, *Every finite horizon Sinai billiard map has a
  unique measure of maximal entropy*, constructs the unique MME as a product
  of Hausdorff measures on one-sided subshifts.  That is not the frozen
  collision-SRB/owner law `mu_C`, so its product structure cannot be inserted
  as the actual stable quotient used here.
- `arXiv:2606.10155v1`, *Recent Progress in the Application of Transfer
  Operators to Dispersing Billiards*, explicitly identifies itself as a
  review.  It does not materialize this typed branch/owner/landing join or a
  physical strong assembly.

No external theorem is promoted into the certificate.

## 8. Seven-field and strict frontier

| # | physical landing field | Round-64 state |
|---:|---|---|
| 1 | physical invariant product rectangles | `PARTIAL`: tagged finite-depth cone-curve atlas only; no invariant tree |
| 2 | stable projection and two-sided `J_hol` | `NOT_CERTIFIED`; exact weighted-tree calculus only |
| 3 | full span or marker fragmentation | `NOT_CERTIFIED`; root-to-tree conditional transport only |
| 4 | same-law conditionals and density bounds | `PARTIAL`: actual landing RN marker and branch covariance; no stable quotient |
| 5 | physical boundary charge below `C_p` | `NOT_CERTIFIED`; no actual inputs to (4.3) |
| 6 | tagged Borel branch inverse | `CERTIFIED` (Round 59) |
| 7 | strong restriction and assembly | `PARTIAL`: graph/current ledger only; physical strong map absent |

The count remains `1/7`; Gate 2's immutable official count remains `0/17`.

```text
finite weighted-tree median formula:                 CERTIFIED_EXACT
pairwise dispersion sandwich P<=delta<=2P:           CERTIFIED_EXACT_SHARP
zero saturation iff all spanning-tree defects zero:  CERTIFIED_EXACT
whole-tree branch-square transport:                  CERTIFIED_EXACT_INTERFACE
actual physical stable tree / root reference law:    NOT_CERTIFIED
actual marker zero defect:                           NOT_CERTIFIED
root-to-all-plaques m-path budget:                    CERTIFIED_CONDITIONAL
actual F,R,theta,L,m,M strict budget:                 NOT_CERTIFIED
strict scalar rows imply uniform BV/strong assembly: FALSE_BY_SEPARATOR
actual physical strong restriction/assembly:         NOT_CERTIFIED
seven-field landing join:                            1/7; fields 1,4,7 partial
official immutable Gate-2 fields:                    0/17
Gate 2:                                              NOT_CERTIFIED
Gate 4:                                              NOT_CERTIFIED
complete composite gates:                            0/5
CM2:                                                 NO-GO_FOR_CLAIM
```

## 9. Executable evidence

- `cm2_gate24_round64_weighted_tree_saturation_actual_join_obstruction_frontier_cert.py`;
- `cm2_gate24_round64_weighted_tree_saturation_actual_join_obstruction_frontier_verifier.py`;
- `cm2-gate24-round64-weighted-tree-saturation-actual-join-obstruction-frontier-manifest-2026-07-21.json`;
- `cm2-gate24-round64-weighted-tree-saturation-actual-join-obstruction-frontier-manifest-2026-07-21.sha256`.

The producer emits canonical deterministic JSON.  The independent verifier
recomputes the four-plaque median, all pairwise and edge bounds, whole-tree
dynamic invariance, path distortion products, actual pinned-field join, and
smooth strong separator.  It also checks byte-identical regeneration and
re-emission, rejects hostile semantic mutations and duplicate/non-finite
JSON, and verifies all four SHA rows.  Both default entry points fail closed
with exit code `2`.
