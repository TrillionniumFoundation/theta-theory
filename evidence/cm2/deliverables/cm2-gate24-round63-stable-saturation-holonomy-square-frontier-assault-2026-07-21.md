# CM2 Round 63 Gate 2/4 — stable-saturation, holonomy-square, and quantitative landing frontier

Date: 2026-07-21  
Strict status: **the actual tagged first-return branch covariance from Round
62 now has an exact commuting-square join with any future physical stable
holonomy, and the missing marker descent to a stable quotient has an exact
two-plaque `L^1` distance.  These results prove that dynamic branch
covariance transports stable-saturation debt but cannot erase it.  A separate
holonomy-distortion calculation identifies the exact `m^2` cost in
transporting the landing properness bound.  No physical invariant product
rectangle, stable holonomy, zero actual marker defect, quantitative
fragmentation/span/density estimate, or physical strong assembly is
constructed.  Gate 2 and Gate 4 remain `NOT_CERTIFIED`; the global state
remains `0/5` and `CM2=NO-GO_FOR_CLAIM`.**

## 1. Frozen Round-62 root and dependencies

This leaf is append-only and edits no frozen artifact.  It pins the complete
Round-62 aggregate, the Round-62 Gate-4/2 leaf, the independent Round-62
audit, and the Round-59--61 physical-landing manifests used below.

```text
Round-62 aggregate report:
873557a6653a826700d5daf11e8b118f5ddca1cf911e085f9c20aa591ab2136f

Round-62 recursive ledger:
e54b5a1de2b4bddf0c7589b77997b1f28284040b64b31fdfbf58af9e73233bac

Round-62 Gate-4/2 report / manifest / ledger:
4acca86b074ce3f6792aa04625c9576d2affeacb0ad9d7cdeb09cabd08d45b00
e0b89d604e89852b574638428a60daa1f6e8231b85177230a5dd67615205bad1
b94df87ba8362827bb1115f474c0beec59f887325e8db58b55a9020bf99ae6bc

Round-62 independent audit report / manifest / ledger:
123f8ffc563e7d2b364f7caf565ac1a953ecc45123d1c483bc0f97b24c3cfeb4
19a02d00e2ac85849f6197054166e193e1d4e3433c21505fd4bfd2b450faea20
32504c8eda5125d11a460199c3471158720127bf2bc1081664a8a20747c7a414
```

The exact pinned physical input is the actual branchwise identity

```text
g_i=D_i a_i=a_i o H_i^-1,
```

where `H_i` is one immutable tagged invertible first-return branch and
`D_i:L^1(mu_i^S)->L^1(mu_i^L)` is the positive dynamic isometry.  Round 62
did not provide a stable product quotient, physical stable holonomy or zero
marker defect.

## 2. Exact branch--holonomy square calculus

### 2.1 Measures and transfer directions

Take two source plaques `U_u,U_v` with reference laws
`mu_u^S,mu_v^S`, two landing plaques `V_u,V_v` with
`mu_u^L,mu_v^L`, and actual tagged invertible branches

```text
H_u:U_u->V_u,       H_v:U_v->V_v,
mu_i^L=(H_i)_#mu_i^S.
```

The dynamic density transfers are

```text
D_i f=f o H_i^-1,
||(D_i f)||_L1(mu_i^L)=||f||_L1(mu_i^S).             (2.1)
```

Suppose a future physical product registry supplies source and landing
stable holonomies

```text
s:U_u->U_v,       ell:V_u->V_v,
s_#mu_u^S=J_S mu_v^S,       ell_#mu_u^L=J_L mu_v^L.
```

Their positive density transfers point from the `u` plaque to the `v`
plaque:

```text
P_S f=(f o s^-1)J_S,
P_L q=(q o ell^-1)J_L.                               (2.2)
```

Both are `L^1` isometries.  For source markers `a_u,a_v` and the actual
landing markers `g_i=D_i a_i`, define

```text
Delta_S=a_v-P_S a_u          in L^1(mu_v^S),
Delta_L=g_v-P_L g_u          in L^1(mu_v^L),
C_uv=D_v P_S-P_L D_u.                                (2.3)
```

Direct addition and subtraction gives the exact identity

```text
Delta_L=D_v Delta_S+C_uv(a_u),                        (2.4)
||Delta_L||_1<=||Delta_S||_1+||C_uv(a_u)||_1.         (2.5)
```

If the physical square commutes,

```text
H_v o s=ell o H_u,                                   (2.6)
```

then pushforward uniqueness gives `D_vP_S=P_LD_u`, hence

```text
C_uv=0,
Delta_L=D_v Delta_S,
||Delta_L||_1=||Delta_S||_1.                         (2.7)
```

Thus an exact square **preserves** stable-marker debt.  It does not make
that debt zero.  Landing marker covariance is equivalent to source marker
covariance only after (2.6) and the same reference-law transfers have both
been installed.

### 2.2 Exact finite square replay

Use uniform three-point reference laws on both source plaques, the same
cyclic dynamic branch

```text
H:0->1, 1->2, 2->0,
```

and identity source/landing holonomies.  Let

```text
a_u=(1,0,1/2),       a_v=(3/4,1/4,1/2).
```

Then every dynamic branch RN identity is exact, the branch--holonomy square
commutes, and

```text
g_u=(1/2,1,0),       g_v=(1/2,3/4,1/4),
Delta_S=(-1/4,1/4,0),
Delta_L=(0,-1/4,1/4),
||Delta_S||_1=||Delta_L||_1=1/6.                     (2.8)
```

This is an exact logical product-law replay, not a claim that the billiard
realizes these markers.  It proves that actual-style branch covariance plus
a perfect commuting product square still does not imply stable saturation.

## 3. Exact two-plaque `L^1` stable-saturation distance

For two plaques with outer weights exactly `1/2`, let `P` be the positive
`L^1` stable-holonomy isometry from `u` to `v`.  A single quotient marker
anchored on `u` is a function `f`; its two plaque representatives are
`f` and `Pf`.  Define

```text
delta_sat(g_u,g_v)
 =1/2 inf_f {||g_u-f||_L1(mu_u)+||g_v-Pf||_L1(mu_v)}. (3.1)
```

The triangle inequality and the isometry give

```text
||g_v-Pg_u||_1
 <=||g_v-Pf||_1+||P(f-g_u)||_1.
```

Choosing `f=g_u` attains equality.  Therefore

```text
delta_sat=1/2||g_v-Pg_u||_1.                         (3.2)
```

In particular, `delta_sat=0` iff the two markers descend to one stable
quotient marker.  In the replay (2.8), `delta_sat=1/12`.

Equation (3.2) deliberately uses an infimum, not a conditional expectation.
Conditional expectation is the canonical `L^2` projection; it is not in
general the `L^1` best approximant, where conditional medians are relevant.
No `L^1` projection theorem is smuggled into the result.

For more than two plaques, the exact physical object remains a quotient
approximation problem or, equivalently, a zero-defect registry on a spanning
holonomy tree.  Round 62's defect cocycle controls consistency around that
tree, but no actual tree or zero defect is currently available.

## 4. Quantitative holonomy transport of `F,R,theta,L`

The stable-holonomy Jacobian relative to conditional measures and the metric
derivative relative to adapted arclength are different rows.  The following
calculation keeps them separate.

Let `W_u` be an adapted-arclength plaque of length `L_u`, let
`E_u subset W_u` have at most `F_u` interval components and

```text
|E_u|>=theta_u L_u,
0<d_-<=f_u<=d_+<=R_u d_- on E_u.
```

Let `h:W_u->W_v` be an orientation-preserving `C^1` holonomy with arclength
metric derivative

```text
0<m<=lambda=dh/ds<=M<infinity.                        (4.1)
```

Assume the same positive plaque law is transported up to an outer scalar
`c>0`:

```text
E_v=h(E_u),
f_v(hx)=c f_u(x)/lambda(x).                          (4.2)
```

Then a homeomorphism preserves components, while (4.1)--(4.2) give

```text
F_v=F_u,
|E_v|>=m theta_u L_u,
R_v<=R_u M/m.                                        (4.3)
```

Applying the frozen component-boundary estimate on the target plaque yields

```text
z_v<=F_v R_v/|E_v|
    <=F_u R_u M/(m^2 theta_u L_u).                   (4.4)
```

The two powers of `m` have different origins: one comes from possible span
contraction, and one from the density ratio through `1/lambda`.  A sufficient
base-to-target strict budget is therefore

```text
F_u R_u M<C_p m^2 theta_u L_u.                       (4.5)
```

Equivalently, with `K_hol=M/m`, it is
`F_u R_u K_hol<C_p m theta_u L_u`.

For the rational magnitude replay

```text
F_u=3, R_u=4, theta_u=1/2, L_u=2, m=1/2, M=3/2,
```

the certified upper bound in (4.4) is `72<C_p`.  This is arithmetic only;
none of those six values has been materialized on the actual common landing
law.

A two-sided measure RN bound for `J_hol` alone does not determine `m,M` in
adapted arclength, and a bi-Lipschitz plaque map alone does not bound the
marker density ratio unless (4.2) is known.  Hence fields 2--4 cannot be
collapsed into one qualitative absolute-continuity assertion.

## 5. Zero stable defect still does not pay properness

Two exact logical product models keep the branch square commuting, use
identity stable holonomy, and put the same marker on every plaque.  Thus
`C_uv=0` and `delta_sat=0` in both models.

### 5.1 Short-span separator

Use a full plaque of length

```text
L=1/(2C_p),       F=R=theta=1.
```

With constant positive density,

```text
z=F R/(theta L)=2C_p>C_p.                            (5.1)
```

### 5.2 Fragmentation separator

Use a unit plaque and

```text
N=floor(C_p)+1
```

equal retained intervals of total length `1/2`, separated by positive gaps,
with constant density.  Then

```text
F=N, R=1, theta=1/2,
J=N, h=1/2,
z=2N>C_p.                                             (5.2)
```

These models independently retain the short-span and fragmentation debts
already isolated in Round 60, now with the stronger hypotheses of an exact
commuting branch--holonomy square and zero marker-saturation defect.  Product
geometry and marker descent are necessary interfaces, not a quantitative
properness theorem.

## 6. Strong assembly and graph-cylinder type boundary

Round 62's graph-cylinder current remains exact and useful as bookkeeping:
it keeps both endpoints, all immutable tags, once charge and the weighted
`D_land` norm.  Nothing in Sections 2--5 constructs a bounded map

```text
E_phys:X_D^graph -> B_strong
```

that simultaneously

1. preserves the physical source and landing traces;
2. intertwines restriction with the billiard transfer operator;
3. is compatible with the moving-domain Piola/current calculus;
4. recovers `Full=Good+Bad` on the same physical carrier; and
5. sends only an accepted singular/current remainder to cemetery.

The positive bad law may be regular collision-SRB mass.  Neither a stable
quotient marker nor a normal current on `[0,1]xZ` makes it collision-null.
The weighted trace remains `2^D nu`, with multiplication by `2^-D` required
to recover the original charge.  Field 7 therefore stays partial at the
graph-ledger level and absent at the required physical strong-operator
level.

## 7. Seven-field landing audit

| # | physical landing field | Round-63 state |
|---:|---|---|
| 1 | physical invariant product rectangles | `PARTIAL`: tagged finite-depth cone-curve atlas only |
| 2 | stable projection and two-sided `J_hol` | `NOT_CERTIFIED`; exact square/defect calculus only |
| 3 | full span or marker fragmentation | `NOT_CERTIFIED`; exact transport budget only |
| 4 | same-law conditionals and density bounds | `PARTIAL`: actual dynamic branch RN covariance plus exact saturation-distance interface; no physical stable quotient |
| 5 | physical boundary charge below `C_p` | `NOT_CERTIFIED`; (4.5) has no actual inputs |
| 6 | tagged Borel branch inverse | `CERTIFIED` (Round 59) |
| 7 | strong restriction and assembly | `PARTIAL`: graph-cylinder assembly only; no physical strong operator |

The complete count remains `1/7`; Gate 2's official immutable count remains
`0/17`.

## 8. Latest official-technology audit

The official-source surface was checked through 2026-07-21.  No current
theorem was found that supplies the pinned common Liouville/SRB landing law
with an all-depth physical stable quotient, zero marker defect, inverse
component/retained-span bounds, and a compatible strong assembly.

- Canestrari `2604.19671v2` evolves an already regular standard family and
  normalizes by survival mass; it does not build this common landing
  quotient or prove (4.5).
- The current Axiom-A/SRB response literature, including `2604.18929`, has
  the wrong smooth hyperbolic type for the singular moving billiard and does
  not install the pinned landing carrier.
- The Round-62 MME/review candidates remain the wrong physical law or a
  review rather than a theorem closing the typed join.

No external result is promoted into the certificate.

## 9. Strict frontier

```text
actual tagged first-return branch RN covariance:      CERTIFIED_PINNED
branch--holonomy square defect identity:              CERTIFIED_EXACT
exact square preserves source/landing defect norm:    CERTIFIED_EXACT
two-plaque L1 stable-saturation distance:             CERTIFIED_EXACT
actual physical stable quotient / holonomy:           NOT_CERTIFIED
actual marker zero defect:                            NOT_CERTIFIED
holonomy transport bound with m^2 cost:               CERTIFIED_CONDITIONAL
actual F,R,theta,L,m,M budget:                         NOT_CERTIFIED
fibrewise F R<C_p theta L:                            NOT_CERTIFIED
tagged graph-cylinder normal current:                 CERTIFIED_PINNED
physical anisotropic/Piola/current assembly:          NOT_CERTIFIED
seven-field landing join:                             1/7; fields 1,4,7 partial
official immutable Gate-2 fields:                     0/17
proper physical same-ID first-return kernel:          NOT_CERTIFIED
original R_n intermediate C24 avoidance:              CERTIFIED_PINNED
later/repeated recovery-clock moments:                NOT_CERTIFIED
physical q in L^(6/5):                                NOT_CERTIFIED
strong singular/current cemetery:                     NOT_CERTIFIED
Gate 2:                                               NOT_CERTIFIED
Gate 4:                                               NOT_CERTIFIED
complete composite gates:                             0/5
CM2:                                                  NO-GO_FOR_CLAIM
```

## 10. Executable evidence

- `cm2_gate24_round63_stable_saturation_holonomy_square_frontier_cert.py`;
- `cm2_gate24_round63_stable_saturation_holonomy_square_frontier_verifier.py`;
- `cm2-gate24-round63-stable-saturation-holonomy-square-frontier-manifest-2026-07-21.json`;
- `cm2-gate24-round63-stable-saturation-holonomy-square-frontier-manifest-2026-07-21.sha256`.

The suite pins and replays the complete Round-62 root, Gate-4/2 leaf and
independent audit plus the necessary Round-59--61 landing manifests.  It
independently verifies the square identity, exact `L^1` saturation distance,
the `m^2` transport budget, both zero-defect properness separators, strict
nonpromotion, deterministic producer regeneration, byte-identical re-emission
and hostile semantic/strict-JSON rejection.  Both default entry points fail
closed with exit code `2`.
