# CM2 Round 62 Gate 1/3 — plaque-tempered gauge and moving-trace Piola frontier

Date: 2026-07-21  
Scope: append-only Gate-1/Gate-3 assault from the frozen Round-61 aggregate  
Strict verdict: **Round 62 does not promote Gate 1 or Gate 3.  It replaces
the vague “third gauge” requirement by an exact forward/backward
plaque-tempered cohomology criterion, and it installs an exact
moving-branch Reynolds/Piola formula together with the minimal stopped-face
current ledger.  Neither interface is presently paid on the physical
all-plaque/all-depth law.  Gate 1 and Gate 3 remain `NOT_CERTIFIED`, complete
composite gates remain `0/5`, and CM2 remains `NO-GO_FOR_CLAIM`.**

## 1. Frozen recursive inputs

This leaf pins, without modifying, the following recursive root:

```text
Round61 aggregate report SHA256
  b9ad28ed23e88768234b304dd9f9ecb02577c7aa18dc8a982185690ea8f6f02b

Round61 aggregate recursive-ledger SHA256
  2a3ae3ebf1a6e11b734611e260a340398f475d70e4888010c8294ac321d84265
```

It also pins the Round-61 Gate-1/2/3 leaf, the frozen third-gauge escape and
compact common-frame leaves, the fixed free graph-current carrier, and the
Round-53 physical graph-current/Piola frontier.  The immutable facts used
below are:

```text
diagonal faithful clean-subsystem representative in class H: CERTIFIED
same-axis twisting in that representative:                   REFUTED
compact QNL candidate has four selected nonzero wedges:       CERTIFIED
compact candidate all-plaque class H on connector set:        REFUTED
finite local SL(2) jet repairs preserving selected orbit:      CERTIFIED
actual countable stopped weak graph-TV restriction:            NORM-ONE
fixed 41,508-slot free graph-current carrier:                  CERTIFIED
physical source graph-current injection into Lip*:            CONSTANT ONE
boundary Piola TV multiplier:                                 ONE
uniform bulk L1 Piola from determinant one alone:              REFUTED
```

The existing two gauges therefore cannot be spliced or renamed into the
missing representative.  A future third gauge must pass the exact global
compatibility rows below.

## 2. Gate 1 — exact plaque-tempered third-gauge criterion

### 2.1 Finite cocycle identity

Use the frozen cohomology convention

```text
B(x)=C(fx)^(-1) A(x) C(x).
```

For a local stable pair `x,y`,

```text
B^n(x)=C(f^n x)^(-1) A^n(x) C(x)
```

and hence

```text
H_B^s(x,y;n)
 =C(y)^(-1) A^n(y)^(-1)
   [C(f^n y) C(f^n x)^(-1)]
   A^n(x) C(x).                                      (2.1)
```

Put

```text
Delta_n^s(x,y)
 =A^n(y)^(-1)
  [C(f^n y)C(f^n x)^(-1)-I]
  A^n(x).                                             (2.2)
```

If `H_A^s(x,y)=lim A^n(y)^(-1)A^n(x)` exists, then (2.1) gives the exact
equivalence

```text
H_B^s(x,y)=C(y)^(-1)H_A^s(x,y)C(x)
iff Delta_n^s(x,y)->0.                                (2.3)
```

The backward formula is identical with `f^(-n)`, `A^(-n)` and
`Delta_n^u`.  Thus one determinant-one transfer `C` puts `B` in the same
all-plaque class `H` and transports the canonical loop if:

1. `C` is defined and Hölder on the entire actual plaque registry;
2. `Delta_n^s->0` and `Delta_n^u->0` uniformly on local plaques;
3. the transported formula has a uniform Hölder modulus; and
4. the periodic base, homoclinic orbit and loop token are the immutable
   physical ones.

Uniform defect convergence alone does not preserve a Hölder exponent or
constant: the conjugations by `A^n` can amplify the approximants.  One must
independently prove a uniform Hölder modulus for the defect/holonomy
approximants; equi-Hölder control plus uniform convergence then passes that
modulus to the limit in (2.3).  At the selected periodic base `p`, the
eigenvectors and loop are simultaneously transported by `C(p)^(-1)`.  Every
twisting wedge is multiplied by
`det(C(p)^(-1))`; for `C in SL(2)` it is numerically unchanged.  This is the
precise all-plaque prerequisite behind the Round-61 same-token covariance.

### 2.2 Sharp determinant-one/same-token separator

Neither determinant one nor equality at the periodic token pays (2.2).
Take the constant class-`H` cocycle

```text
A=diag(2,1/2)
```

on a logical hyperbolic orbit closure with a stable pair satisfying
`d(f^n x,f^n y)=2^(-n)`.  Let

```text
C(f^n x)=I,
C(f^n y)=I+2^(-n)E_21,
C(p)=I.
```

This transfer is Lipschitz on the orbit closure, belongs to `SL(2)`, lies in
the positive biprojective cell with `q=1`, and fixes the periodic token.
Nevertheless,

```text
A^(-n)[C(f^n y)C(f^n x)^(-1)-I]A^n
 =2^n E_21.                                           (2.4)
```

The defect diverges.  The replay checks `n=1,...,12`, ending at `4096`.
This is an exact logical connector model, not a new billiard realization.
It proves that all of

```text
exact Hölder cohomology + determinant one + same periodic token
+ uniform positive big cell
```

still do not imply all-plaque class `H`.  The missing physical row is the
forward/backward **renormalized endpoint-defect registry**, not another
matrix determinant check.

### 2.3 Strict Gate-1 boundary

The frozen fork remains decisive:

```text
faithful diagonal gauge: class H, but selected same-axis twisting = 0;
compact QNL gauge: selected twisting != 0, but connector class H refuted.
```

Finite disjoint `SL(2)` bumps can repair the two known first jets while
leaving the selected orbit fixed, so those jets are not a universal no-go.
They do not furnish the uniform two-sided defect limits.  Accordingly:

```text
exact plaque-tempered cohomology criterion:             CERTIFIED_INTERFACE
det-one/same-token implication without defect control:  CERTIFIED_FALSE
physical all-plaque third-gauge defect registry:         NOT_CERTIFIED
same physical representative with class H plus twisting: NOT_CERTIFIED
Gate 1:                                                   NOT_CERTIFIED
```

## 3. Gate 3 — moving stopped branches as a bulk-plus-face current

### 3.1 Exact Reynolds graph formula

For one moving branch let

```text
I_i(s)=[a_i(s),b_i(s)],
Y_i(s,.):I_i(s)->M,
Lambda_i(s,phi)=integral_(a_i(s))^(b_i(s))
                 f_i(s,x) phi(Y_i(s,x)) dx.
```

For `C^1` data the exact derivative at `s=0` is

```text
Lambda_i'(0,phi)
 = integral_I [partial_s f_i phi(Y_i)
                +f_i Dphi(Y_i) dot partial_s Y_i] dx
   +b_i' f_i(b_i-) phi(Y_i(b_i-))
   -a_i' f_i(a_i+) phi(Y_i(a_i+)).                     (3.1)
```

The first line is the bulk response/directional graph-Piola term.  The
second is a signed endpoint current.  At a shared moving cut
`e=b_i=a_(i+1)`, the exact current is

```text
B_e=e' [ f_i(e-) delta_(Y_i(e-))
        -f_(i+1)(e+) delta_(Y_(i+1)(e+)) ].             (3.2)
```

It cancels for every test exactly when the two weighted landing atoms agree
(or when `e'=0`).  Half-open ownership alone does not cancel it.  When the
landings differ,

```text
||B_e||_TV=|e'|(|f_i(e-)|+|f_(i+1)(e+)|).              (3.3)
```

For a countable stopped partition, assume in addition one
parameter-neighbourhood dominator for the branch derivatives and endpoint
traces, so that differentiation may pass through the countable sum.
Dominated differentiation is then valid on the current-completed recipient
if the bulk series is absolutely summable and

```text
E_stop=sum_e ||B_e||_TV < infinity.                    (3.4)
```

The actual Round-61 partition supplies the countable Borel labels and
norm-one weak-TV restriction.  It does not supply (3.4), trace existence in
the physical anisotropic source space, a common finite-`s` moving atlas, or
the bulk strong norm.

The rational replay takes `e(s)=1/2+s`, unit traces and two adjacent
branches.  Identical landings give the face pairing `0`.  Translating the
right landing by one gives the signed current
`delta_(1/2)-delta_(3/2)`, TV `2`, and pairing `-1` against `phi(t)=t`.

### 3.2 Directional Piola on one regular branch

Let `Phi_s` be a `C^1` family of diffeomorphisms, `Phi_0=Id`, velocity
`V=partial_s Phi_s|_0`, and let the contravariant Piola pushforward of a
vector measure `K` be paired with a `C^1` vector test `psi` by

```text
<Piola_(Phi_s)K,psi>
 =integral psi(Phi_s(x)) dot D Phi_s(x) dK(x).
```

Direct differentiation gives the exact weak directional formula

```text
d/ds|_0 <Piola_(Phi_s)K,psi>
 =integral [Dpsi(x)V(x) dot dK(x)
            +psi(x) dot DV(x)dK(x)].                  (3.5)
```

Consequently its norm in `(C^1)^*` is bounded by

```text
(||V||_infinity+||DV||_infinity) ||K||_TV.             (3.6)
```

For the area-preserving sample

```text
Phi_s=diag(1+s,(1+s)^(-1)), K=e_1 dx,
psi(y)=(y_1,0), U=[0,1]^2,
```

the exact derivative is `1`, split as `1/2+1/2` between the two terms in
(3.5).  This is a local regular-branch current identity.  It is not the
missing physical billiard strong operator.

### 3.3 Why determinant one still does not control the bulk

Round 53 already isolates the unavoidable type boundary.  For

```text
U_L=[0,1/L]x[0,1],
S_L=diag(L,L^(-1)),
K=e_1,
```

`det DS_L=1`, but

```text
||K||_(L1(U_L))=1/L,
||Piola_(S_L)K||_(L1(S_L U_L))=1.
```

The multiplier is `L`, unbounded.  The executable replay checks
`L=2,4,8,16,32`.  Hence area preservation and boundary-flux naturality do
not provide the bulk physical `F17`/Gate-3 strong constant.  A
billiard-specific anisotropic directional bound or a legitimate
quotient/coboundary cancellation is still needed.

There is an independent fragmentation separator.  A unit source on one
interval has fixed intrinsic `W^{1,1}` norm.  If `m` moving internal faces
send their two traces to distinct landing labels, (3.3) gives face-current
TV `2m`.  The stopped weak-TV norm remains one.  Thus even replacing
zero-extension BV by intrinsic cell norms cannot remove the physical face
ledger.

### 3.4 Exact conditional recipient and strict boundary

The countable stopped construction now has a minimal typed strong-current
recipient:

```text
regular bulk directional Piola series
plus
the signed physical face current sum_e B_e.
```

It yields a bounded `(C^1)^*` graph current and allows countable assembly if
all of the following are installed on the same physical branch records:

1. a common finite-`s` stopped atlas and trace maps;
2. the absolutely summable endpoint mismatch ledger (3.4);
3. a uniform anisotropic bulk directional-Piola bound;
4. assembly of duplicate/artificial traces before absolute values;
5. cemetery and moving-test tightness on the same carrier.

Under those hypotheses the usual finite-time telescope is valid,

```text
D(P^n)=sum_(k=0)^(n-1) P^(n-1-k) (DP) P^k,
```

but the hypotheses are precisely the missing physical `MT_DQ` input.  The
strict ledger is:

```text
moving-branch bulk-plus-face formula:                 CERTIFIED_EXACT_INTERFACE
directional regular-branch Piola formula:             CERTIFIED_EXACT_INTERFACE
current-completed stopped recipient:                  CERTIFIED_CONDITIONAL
weak TV -> endpoint trace/current implication:        CERTIFIED_FALSE
det-one -> uniform bulk Piola implication:            CERTIFIED_FALSE
physical strong R_s/Q_s:                              NOT_CERTIFIED
physical directional Piola/current:                   NOT_CERTIFIED
MT_DQ:                                                 NOT_CERTIFIED
Gate 3:                                                NOT_CERTIFIED
```

## 4. Latest official-technology audit

Official arXiv API searches were repeated on 2026-07-21 for moving
dispersing billiards, Piola/shape derivatives, anisotropic strong operators,
canonical holonomy and non-fibre-bunched cohomology.  No 2026-07 result
supplies either missing physical interface.

- `arXiv:2603.19509v3` puts common strong/weak spaces, uniform strong bounds,
  strong differentiability and memory loss among the hypotheses of its
  nonautonomous response framework.  Its applications are expanding/noisy
  maps, not moving singular billiards.
- `arXiv:2604.19671v2` evolves already regular standard families for a fixed
  billiard with a changing small hole.  It does not construct the stopped
  moving-domain trace/Piola operator.
- `arXiv:2606.10155v1` surveys anisotropic billiard spaces; it does not
  provide the all-depth characteristic-restriction theorem or CM2
  directional current.
- Butler--Park `arXiv:1909.11548v2` defines class `H` by the canonical
  limits and their Hölder regularity; it does not make them invariant under
  an arbitrary non-fibre-bunched Hölder transfer.

No external result is promoted.  Each useful theorem has the missing CM2
strong differentiability, regular-family input, or plaque-tempered
cohomology as an assumption rather than a conclusion.

## 5. Round-62 strict status and continuation

```text
Gate 1:                  NOT_CERTIFIED
Gate 3:                  NOT_CERTIFIED
complete composite gates: 0/5
CM2:                     NO-GO_FOR_CLAIM
```

The shortest next steps are now exact:

1. **Gate 1:** materialize one physical determinant-one transfer on every
   actual plaque and prove uniform forward/backward defect decay in (2.2),
   then identify the same immutable loop token.  This would transport the
   selected wedges algebraically.
2. **Gate 3:** on the actual stopped branch law, prove the all-depth
   endpoint-current sum (3.4), a common moving atlas, and a billiard-specific
   anisotropic directional-Piola bound.  Only then install physical
   `R_s/Q_s`, the finite-time telescope and `MT_DQ`.

## 6. Executable evidence

- `cm2_gate13_round62_plaque_tempered_gauge_moving_trace_piola_frontier_cert.py`;
- `cm2_gate13_round62_plaque_tempered_gauge_moving_trace_piola_frontier_verifier.py`;
- `cm2-gate13-round62-plaque-tempered-gauge-moving-trace-piola-frontier-manifest-2026-07-21.json`;
- `cm2-gate13-round62-plaque-tempered-gauge-moving-trace-piola-frontier-manifest-2026-07-21.sha256`.

The producer and independent verifier pin twelve recursive artifacts,
replay all exact rational identities and separators, require canonical JSON,
reject hostile semantic and JSON mutations, regenerate the manifest
byte-for-byte, and fail closed with default exit `2`.
