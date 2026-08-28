# CM2 Round 66 Gate 1/3 — same-representative gauge and material-trace frontier

Date: 2026-07-21  
Scope: append-only Gate-1/Gate-3 assault from the frozen Round-65 aggregate  
Strict verdict: **Round 66 does not promote Gate 1 or Gate 3.  It performs
the missing same-gauge audit rather than substituting selected QNL numbers,
derives the exact relative-shear transfer and the sharp all-plaque
tail/selected-loop transport criterion, and proves one genuine but local
physical finite-depth material-atlas result.  It also reduces a global
countable Piola remainder to a uniform block supremum and refines the stopped
`MT_DQ` debt to the derivative of a depth generating function.  The required
same-key actual transfer, all-depth strong trace, uniform anisotropic
remainder and strong subunit contraction are not frozen.  Gate 1 and Gate 3
remain `NOT_CERTIFIED`, complete composite gates remain `0/5`, and CM2
remains `NO-GO_FOR_CLAIM`.**

## 1. Frozen roots and immutable type audit

This leaf pins and does not modify the Round-65 aggregate, independent audit,
Gate-1/3 leaf and cross-gate positive-potential leaf.  It also directly pins
the Round-59 physical formula/selected-germ audit, the Round-62
plaque-tempered/Piola frontier, both Round-64 Gate-1/3 leaves and the original
5000-bit selected QNL loop artifact.

The frozen manifests expose the following exact distinction:

```text
selected QNL gauge matrix syntax:       B_u(x) B_s(y)
selected QNL carrier:                   one immutable homoclinic in E_p
selected loop/tail/four wedges:          CERTIFIED_LOCAL

combined Green gauge matrix syntax:     U_v L_u
separate one-sided all-plaque gauges:    CERTIFIED_THEOREMS
combined cross scalar T_n:               CERTIFIED_EXACT_INTERFACE
same scalar functions as QNL B_u/B_s:   NOT_CERTIFIED
same orbit/plaque/gauge registry key:    NOT_CERTIFIED
compact-QNL to combined finite loop:     NOT_CERTIFIED
```

Both matrices are products of an upper and a lower shear.  That shared
surface syntax is not an equality of their scalar functions.  The QNL
manifest has no all-plaque registry field; the combined-Green manifest
explicitly records selected twisting in that representative as absent.
Therefore the frozen `0.091`, `0.092809...`, depth-260 loop and four wedges
still have no lawful same-gauge transport into `T_n`.

## 2. Gate 1 — exact relative shear and tail/loop transport

### 2.1 Relative transfer between two upper-lower gauges

Write the compact and combined gauge matrices on a hypothetical common keyed
carrier as

```text
G_q=U_(v_q)L_(u_q),       G_c=U_(v_c)L_(u_c),
dv=v_c-v_q.
```

Their exact relative transfer is

```text
C=G_q^(-1)G_c
 =L_(-u_q) U_(dv) L_(u_c)
 =[[1+dv*u_c,                    dv],
   [u_c-u_q*(1+dv*u_c), 1-u_q*dv]].                  (2.1)
```

It has determinant one.  More sharply,

```text
C=I  iff  dv=0 and u_c=u_q.                          (2.2)
```

Thus matching matrix *form* cannot identify the gauges; the two scalar
Green/shear functions must agree on the same keyed carrier, or the resulting
nontrivial transfer must be paid by the renormalized endpoint defects below.

For an exact rational replay take

```text
u_q=1/2, v_q=1/3, u_c=2/3, v_c=5/6.
```

Then `dv=1/2` and

```text
C=[[4/3,1/2],[0,3/4]],       det C=1,                (2.3)
```

despite cancellation of its lower-left coordinate.  This makes explicit why
checking only one shear defect or determinant one is insufficient.

### 2.2 Sharp all-plaque transport iff

Let two cocycles on one actual plaque registry satisfy the exact convention

```text
B(x)=C(fx)^(-1) A(x) C(x).
```

For a stable plaque pair `(x,y)`, put

```text
Delta_n^s
 =A^n(y)^(-1)[C(f^n y)C(f^n x)^(-1)-I]A^n(x).       (2.4)
```

The finite canonical approximants obey

```text
H_B^s(x,y;n)
 =C(y)^(-1)[H_A^s(x,y;n)+Delta_n^s(x,y)]C(x).        (2.5)
```

There is an identical backward formula for `Delta_n^u`.  Assume `A` already
has uniform Holder canonical families on the declared all-plaque registry,
and `C,C^-1` have the declared bounded Holder endpoint control.  Then (2.5)
gives the exact equivalence:

```text
B is class H on that same registry
iff Delta_n^s and Delta_n^u have uniform Holder limits
    L_s and L_u on every local plaque.                (2.6)
```

Zero tails are not required.  Nonzero limits change the canonical families:

```text
H_B^s=C(y)^(-1)(H_A^s+L_s)C(x),
H_B^u=C(y)^(-1)(H_A^u+L_u)C(x).                       (2.7)
```

This is sharper than the Round-62 zero-defect sufficient route and sharper
than a mere scalar rate gap: it is the necessary-and-sufficient transport
test once the common representative and endpoint Holder bounds are fixed.

### 2.3 Exact selected-loop comparison

At the immutable homoclinic token, the target loop is

```text
Psi_B=C(p)^(-1)(H_A^s+L_s)(H_A^u+L_u)C(p).           (2.8)
```

Consequently exact transport of the source loop
`Psi_A=H_A^sH_A^u` occurs if and only if

```text
H_A^s L_u + L_s H_A^u + L_s L_u =0.                 (2.9)
```

When (2.9) holds, simultaneous transport of the two eigenaxes preserves all
four nonzero twisting wedges.  When it fails, the target loop must be
recomputed; selected QNL wedge values cannot simply be copied.

For the faithful diagonal source

```text
H_A^s=diag(a,a^-1), H_A^u=diag(b,b^-1),
L_s=l E_21, L_u=u E_12,        ab!=0,
```

the correction in (2.9) is

```text
[[0,a*u],[l*b,l*u]].                                  (2.10)
```

It vanishes exactly when `l=u=0`.  Hence the nonzero resonant tails needed
to create twisting from the faithful diagonal zero-twisting representative
necessarily change its loop; they cannot be justified by the Round-61
pure-covariance shortcut.  Conversely, transport of the already nonzero QNL
loop is lawful only after a common transfer `C`, both tail limits and (2.9)
are certified.

### 2.4 Minimal immutable Gate-1 registry

The remaining physical construction is now an eight-row keyed object:

1. one base/orbit/plaque ID and one physical derivative cocycle;
2. exact `G_q` and `G_c` matrices on that carrier;
3. the oriented relative transfer (2.1), including endpoint axes;
4. all-plaque forward/backward `Delta_n` records;
5. uniform convergence and uniform Holder moduli for both tail families;
6. the selected finite approximants aligned to the QNL return counts;
7. either the loop correction identity (2.9) or a direct recomputation of
   the changed loop;
8. the four axes/wedges in that same representative.

No frozen artifact materializes this common eight-row registry.  The
selected and all-plaque inputs are valuable, but they remain different typed
leaves.

## 3. Gate 3 — physical local atlas and sharp global criteria

### 3.1 A genuine fixed-depth compact-interior material atlas

Round 59 supplies an actual positive-width strict 96-collision word and the
exact circular branch equations with centers affine in `s`.  On any compact
substrip `K` strictly inside that regular word cell, continuity and compactness
give a positive common margin

```text
|u_j dot n_(j+1)|>=gamma,
gamma<=tau_j<=3-gamma,
```

together with positive clearance from competing contacts, ties and chart
faces.  The derivative of the contact equation with respect to flight time
is `2 R_i (u_j dot n_(j+1))`, hence is bounded away from zero on `K`.
The implicit-function theorem, followed by the polynomial reflection
formula, therefore gives one finite-parameter `C^2` material branch atlas
for this compact depth-96 core.  Its regular smooth Piola family has a
uniform `O(s^2)` Taylor remainder on any fixed `W^{2,1}->L^1`-type local
scale.

This is a physical local promotion, not a global Gate-3 promotion:

```text
one compact regular depth-96 physical material atlas: CERTIFIED_LOCAL
all cells and all stopped depths on one s-window:     NOT_CERTIFIED
uniform lower grazing/face margin across cells:       NOT_CERTIFIED
physical anisotropic strong recipient:                NOT_CERTIFIED
```

Cell birth/death, grazing, clock and cemetery records are outside this
persistent compact core and must remain in the tagged trace/current ledger.

### 3.2 Countable Piola remainder is exactly a supremum

Let persistent keyed branches carry operators

```text
J_(s,k):X_k -> Y_k,       generator G_k,
```

and put `J_s=direct_sum_k J_(s,k)` between the `ell1` direct sums.  Direct-sum
norm algebra gives the exact identity

```text
||(J_s-I-sG)/s||
 =sup_k ||J_(s,k)-I-sG_k||/|s|.                       (3.1)
```

Therefore the global anisotropic uniform remainder holds if and only if

```text
sup_k epsilon_k(s) ->0.                               (3.2)
```

Every fixed branch being differentiable is insufficient.  The sharp model

```text
epsilon_k(1/N)=min(1,k/N)
```

has `epsilon_k(1/N)->0` for every fixed `k`, while the supremum is one for
every `N`.  The exact criterion (3.2), rather than pointwise branch
differentiability, is the missing uniform Piola row.

Together with Round 65, a common material restriction derivative requires
both:

1. (3.2) on persistent branches; and
2. boundedness of the two-sided weighted trace map

       Gamma:X -> ell1(face/side tags).

Because the persistent and topology-change rows retain disjoint immutable
tags, neither can cancel the other.  This is the shortest strong
material/trace join.

### 3.3 Stopped `MT_DQ` is a generating-function derivative

Let a stopped depth have positive weights `p_n`, and suppose on one strong
fixed material scale

```text
||T||<=M,       ||DT||<=L.
```

The iterate rule gives

```text
||D(T^n)||<=n M^(n-1)L.
```

Thus the exact positive scalar depth ledger is

```text
L * sum_n p_n n M^(n-1) = L P'(M),
P(z)=sum_n p_n z^n.                                  (3.3)
```

For tagged positive scalar blocks (3.3) is necessary and sufficient; for
general operators it is the sharp norm-majorant route.  This refines the
Round-65 phrase “depth-weighted derivative moment”:

- at `M=1`, it is the ordinary first depth moment;
- at `M<1`, a finite stopped mass can pay heavy depth tails because the
  derivative is exponentially damped;
- at `M>1`, an exponential depth moment is required.

For the exact Round-65 separator `p_n=1/[n(n+1)]`,

```text
P'(M)=sum_(n>=1) M^(n-1)/(n+1)
     =[-log(1-M)-M]/M^2,       0<M<1,                (3.4)
```

which is finite for every `M<1` and diverges at `M=1`.  So a genuine strong
subunit contraction would repair that separator.  The frozen physical map
has only weak graph-TV norm one; it does not supply a common strong space or
a strict `M<1` for the derivative carrier.

### 3.4 Minimal physical Gate-3 registry

The exact remaining package is:

```text
immutable branch/word/component/depth/side/time key:       PARTIAL_FIXED_DEPTH
one common all-depth finite-s incidence atlas:             NOT_CERTIFIED
uniform J_s and J_s^-1 on the strong scale:                NOT_CERTIFIED
two-sided weighted trace Gamma:                            NOT_CERTIFIED
anisotropic generators G_k:                                NOT_CERTIFIED
uniform supremum remainder (3.2):                          NOT_CERTIFIED
bounded differentiable fixed-material Rhat/Phat/Qhat:      NOT_CERTIFIED
clock, face and one-shot cemetery current sums:            NOT_CERTIFIED
same-law P'(M) / positive path-potential bound:             NOT_CERTIFIED
physical MT_DQ:                                             NOT_CERTIFIED
```

The depth-96 compact core proves that the local smooth geometry is not the
obstruction.  The obstruction is uniform assembly across the actual
countable singular/stopped registry.

## 4. Same-type technology boundary

The most recent directly relevant sources already pinned in the frozen
stack were rechecked by type.

- `arXiv:2603.19509v3` assumes common strong spaces, differentiability and
  memory loss; its verified applications are expanding/noisy maps.
- `arXiv:2604.19671v2` starts with regular standard families for a fixed
  billiard with a changing hole, not a moving-scatterer material atlas.
- `arXiv:2604.25746v1` concerns smooth compact boundaryless flows.
- `arXiv:2606.10155v1` is an anisotropic billiard-space review.
- Butler--Park `arXiv:1909.11548v2` defines the required canonical
  holonomies; it does not make them invariant under an unpaid non-fibre-
  bunched transfer.

None supplies the same-key relative transfer, all-depth trace map or uniform
anisotropic remainder.  No external theorem is promoted.

## 5. Strict Round-66 Gate-1/3 state

```text
exact relative-shear transfer and identity test:          CERTIFIED_EXACT
all-plaque tail transport iff:                            CERTIFIED_EXACT
selected-loop correction iff:                            CERTIFIED_EXACT
actual compact-QNL/combined common registry:              NOT_CERTIFIED
actual all-plaque combined limit and twisting:            NOT_CERTIFIED

physical compact depth-96 material atlas:                 CERTIFIED_LOCAL
global direct-sum uniform-remainder iff:                   CERTIFIED_EXACT
stopped generating-function derivative criterion:         CERTIFIED_EXACT
all-depth strong trace/Piola/MT_DQ:                        NOT_CERTIFIED

Gate 1:                                                    NOT_CERTIFIED
Gate 3:                                                    NOT_CERTIFIED
complete composite gates:                                 0/5
CM2:                                                       NO-GO_FOR_CLAIM
```

## 6. Executable evidence

- `cm2_gate13_round66_same_representative_material_trace_frontier_cert.py`;
- `cm2_gate13_round66_same_representative_material_trace_frontier_verifier.py`;
- `cm2-gate13-round66-same-representative-material-trace-frontier-manifest-2026-07-21.json`;
- `cm2-gate13-round66-same-representative-material-trace-frontier-manifest-2026-07-21.sha256`.

The producer and independent verifier hash-pin all frozen inputs, replay the
relative-shear matrices, tail/loop correction algebra, direct-sum remainder
rows and stopped generating-function partial sums, require canonical strict
JSON, reject hostile semantic/parser mutations, regenerate byte-for-byte and
fail closed with default exit code 2.
