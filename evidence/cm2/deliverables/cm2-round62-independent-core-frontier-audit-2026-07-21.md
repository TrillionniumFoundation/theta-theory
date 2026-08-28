# CM2 Round 62 — independent core-frontier audit

Date: 2026-07-21  
Verdict: **PASS after red-team corrections.  No Round-62 leaf closes a
composite gate.  The consistent strict state is `Gate 1/2/3/4/5 =
NOT_CERTIFIED`, complete composite gates `0/5`, Gate-5 maturity `10/18` with
zero complete 18-field blocks, and `CM2=NO-GO_FOR_CLAIM`.**

## 1. Independence and frozen scope

This audit pins the complete Round-61 recursive root and the three final
Round-62 leaves.  No frozen file is modified.

The present audit agent authored the Gate-4/2 leaf.  It therefore does **not**
describe its own checks of that leaf as independent.  The root agent
independently reran its syntax, semantic audit, hostile suite, producer-based
re-emission, sidecar SHA and both default fail-closed entries, and separately
reviewed the branch/holonomy/current types.  Section 2 records that root
verdict and checks only its consistency with the other leaves.  Sections 3
and 4 are the present agent's independent mathematical and executable audits
of the Gate-1/3 and Gate-5 leaves.

Final pinned leaf roots are:

```text
Gate 4/2 manifest:
e0b89d604e89852b574638428a60daa1f6e8231b85177230a5dd67615205bad1
Gate 4/2 SHA ledger:
b94df87ba8362827bb1115f474c0beec59f887325e8db58b55a9020bf99ae6bc

Gate 1/3 manifest:
eb9e086e973866beaba19111a74e67772f5b0998bbee7c43f06c273c96c68fe2
Gate 1/3 SHA ledger:
14e13e71fbe1a9c0ed1ef8524da549939417c8406fa60a78f60d56e45deab450

Gate 5 manifest:
ddbe8545e6471977ac7bd06b584717cbe7ffeeb62df2ac3baeb8cb70f0ad27d9
Gate 5 SHA ledger:
ce399f98596b9906eb89d1bd68b80d5f49a5ed29471ba2b8d9648c250a805e61
```

The recursive Round-61 pins are

```text
aggregate report:
b9ad28ed23e88768234b304dd9f9ecb02577c7aa18dc8a982185690ea8f6f02b
aggregate ledger:
2a3ae3ebf1a6e11b734611e260a340398f475d70e4888010c8294ac321d84265
```

## 2. Gate 4/2 — root-independent review

The root agent independently obtained:

```text
syntax:                         PASS
verifier --audit:              PASS
hostile semantic / JSON:       180/180 + 4/4 rejected
producer-derived reemit:       byte-identical
SHA sidecar:                   4/4
default cert/verifier:         2/2 exit 2
type review:                    PASS
```

The typed conclusions are correct.

### 2.1 Actual dynamic branch covariance

On one already certified invertible tagged first-return branch
`H:U->V`, simultaneous transport of `mu_U` and `kappa_U=a mu_U` gives

```text
mu_V=H_#mu_U,
kappa_V=H_#kappa_U,
g_B=d kappa_V/dmu_V=a o H^-1,
a=g_B o H.
```

The branch coordinate Jacobian cancels in this RN ratio.  The result is
actual and preserves `n/path/ID/owner/once`, but it is dynamic first-return
covariance, not stable-holonomy covariance between distinct plaques.

### 2.2 Holonomy defect remains an interface

For a future nonsingular bijective holonomy with
`h_#mu_u=J_uv mu_v`, the positive `L1` isometry

```text
P_uv f=(f o h^-1)J_uv
```

and defect `Delta_uv=g_v-P_uv g_u` satisfy

```text
Delta_uw=Delta_vw+P_vw Delta_uv.
```

This is exact algebra.  The leaf does not claim the physical `h`, `J_uv` or
zero defect.  Gate 2 therefore remains `0/17`, and the landing join remains
`1/7` with fields 1, 4 and 7 only partial.

### 2.3 Weighted/unweighted current guard

The ordinary graph-cylinder current satisfies

```text
M(T_nu)=|nu|,
M(partial T_nu)=2|nu|.
```

The weighted companion has exact mass `||nu||_X`, but its traces are
`w nu`, not `nu`; the leaf explicitly recovers the physical trace only by
the multiplier `w^-1=2^-D_land`.  The cylinder is an artificial tagged
record cylinder.  It is not a collision-phase anisotropic current, a Piola
carrier, or singular cemetery.  Thus the graph-cylinder ledger can be
`4/5` while the requested physical strong ledger remains open.

## 3. Gate 1/3 — independent algebra and type audit

### 3.1 Plaque-tempered cohomology

With

```text
B(x)=C(fx)^-1 A(x)C(x),
```

direct multiplication gives

```text
H_B^s(x,y;n)
=C(y)^-1 A^n(y)^-1
 [C(f^n y)C(f^n x)^-1]
 A^n(x)C(x).
```

Consequently, provided `H_A^s` exists, the desired transported limit is
equivalent to

```text
Delta_n^s
=A^n(y)^-1[C(f^n y)C(f^n x)^-1-I]A^n(x) ->0.
```

The backward row is analogous.  Uniform convergence does not by itself
preserve a Hölder exponent; the final leaf correctly lists a uniform
Hölder/equi-Hölder approximant modulus as a separate required row.

The separator is exact.  For `A=diag(2,1/2)` and endpoint defect
`2^-n E_21`, conjugation yields

```text
A^-n(2^-n E_21)A^n=2^n E_21.
```

The twelve replay rows end at `4096`.  Therefore determinant one, an exact
periodic token and a positive big cell do not supply the missing all-plaque
renormalized-defect registry.

### 3.2 Moving faces and directional Piola

Leibniz--Reynolds differentiation of a moving interval gives the stated
bulk derivative plus the two endpoint atoms.  At a shared cut `e`, the face
current is exactly

```text
B_e=e'[f_-(e)delta_(Y_-(e))-f_+(e)delta_(Y_+(e))].
```

Half-open ownership does not cancel distinct landing atoms.  The rational
sample has zero pairing for matching landings and signed pairing `-1`, TV
`2`, for landings separated by one.

For the contravariant pushforward pairing

```text
<Piola_(Phi_s)K,psi>
=integral psi(Phi_s(x)) dot D Phi_s(x) dK(x),
```

direct differentiation gives

```text
integral [Dpsi V dot dK + psi dot DV dK].
```

The area-preserving diagonal replay splits its derivative as `1/2+1/2=1`.
The frozen determinant-one separator has source norm `1/L`, target norm
`1`, and unbounded multiplier `L`; the face separator has TV `2m` at fixed
weak-TV/intrinsic norm.  Hence the bulk-plus-face recipient is correctly
typed as `CERTIFIED_EXACT_CONDITIONAL`, while physical all-depth traces,
strong `R_s/Q_s`, directional Piola and `MT_DQ` remain unproved.

Independent executable results:

```text
dependencies:                    12/12
Gate-1 defect rows:              12
Gate-3 face/Piola rows:          2 / 1
Gate-3 fragmentation/bulk rows: 6 / 5
integrity/replay/reemit:         PASS / PASS / byte-identical
hostile+strict JSON:             300/300 rejected
SHA:                             4/4
default cert/verifier:           2/2 exit 2
```

## 4. Gate 5 — independent measure and series audit

### 4.1 Exact source-grazing null subtrace

On the raw endpoint law,

```text
B=max(14,ceil(log2(1/eta))),
m_occ{B>b}<=(9158592/6875)4^-b.
```

For every finite `b`, `{eta=0} subset {B>b}`.  Continuity from above gives
raw coarea mass zero.  Round 52's source-marked owner restriction has the
same tail domination, and the Round-61 map retains `eta/B`, so the nullity
pushes to every actual fixed-`j` regular owner law.

The scope is correctly narrow.  Exact artificial chart/owner cuts,
future/full-word accumulation and pre-regularization corner/simultaneous
cemetery charge remain open.  No `A_col` full coverage or global complement
nullity is claimed.

### 4.2 Canonical time-labelled registry and outer Abel identity

The implementation

```text
X_all=disjoint_union_(j>=0)({j}xX_j)
```

is canonical and minimal, not a unique encoding.  Any injectively equivalent
Borel encoding is legal, but `j` or an equivalent immutable insertion
coordinate must survive.  Collapsing distinct insertion times changes the
Duhamel/operator identity and is illegal owner deduplication.

For nonnegative complement charges `c_j` and tails
`T_n=sum_(j>=n)c_j`, coefficient counting gives the exact extended identity

```text
sum_j w_Z^j c_j
=T_0+(w_Z-1)sum_(n>=1)w_Z^(n-1)T_n.
```

Indeed the coefficient of `c_j` on the right is
`1+(w_Z-1)sum_(n=1)^j w_Z^(n-1)=w_Z^j`.  The available fixed-time bound has
no decay in `j` and cannot pay the series.

The separator `b_j=w_Z^-j/(j+1)` has finite unweighted sum and finite
fixed-time anchors, while `sum w_Z^j b_j` is harmonic.  Immutable time labels
prevent owner minimization from merging these events.

### 4.3 Clearance/Orlicz and Jordan ledgers

Round 61's uniform pointwise bounds

```text
2^(K+1)<=Phi(w_Z^r_K)<C 2^(K+1)
```

pass through the positive outer weights by Tonelli, proving the outer
raw-`Z_col`/power-Orlicz finiteness iff.  They do not make either side finite.
The active-clock double Abel identity is likewise an equality in
`[0,infinity]`.

For positive measures, the measure-lattice identity

```text
mu_j^+ + mu_j^-
=|J_j|+2(mu_j^+ wedge mu_j^-)
```

survives multiplication by any nonnegative `phi_j`, outer weighting and
Tonelli summation.  Disjoint-sign and equal-sign harmonic models separately
force divergence of variation and common mode.  The Round-61 orientation
cost laws are not identified with these Jordan marginals or their charge.

Accordingly the final Gate-5 state is exactly

```text
maturity:                         10/18
complete blocks:                  0
suffix typing/truth:              7/7 Borel; 2 true / 5 open
physical R>=r_K:                  NOT_CERTIFIED
all-time complement/Abel/Orlicz: exact interfaces, finite RHS NOT_CERTIFIED
Jordan variation/common mode:     NOT_CERTIFIED
strong cemetery:                  NOT_CERTIFIED
Gate 5:                           NOT_CERTIFIED
```

Independent executable results:

```text
dependency+aggregate pins:       9/9
integrity/replay/reemit:         PASS / PASS / byte-identical
hostile+strict JSON:             168/168 rejected
SHA:                             4/4
default cert/verifier:           2/2 exit 2
```

## 5. Cross-leaf consistency audit

No cross-leaf substitution is legal:

- Gate-4's `D_land`-weighted graph cylinder is a bookkeeping current and
  does not pay Gate-3's moving physical endpoint-face series or bulk Piola
  norm.
- Gate-3's signed face current cannot absorb Gate-4's ordinary positive bad
  collision-SRB mass, and neither is Gate-5's positive all-time cemetery.
- Gate-5's immutable insertion coordinate `j` indexes distinct Duhamel
  events.  It cannot be deduplicated using Gate-4's once-charge tag.
- Gate-4 dynamic branch covariance does not manufacture Gate-2 stable
  holonomy; Gate-1 plaque-tempered cocycle covariance concerns a different
  operator/gauge layer and cannot supply it.
- `D_land`, the stopped `Dbar`, endpoint rank `B`, collar clearance `K` and
  insertion time `j` remain distinct marks.  No moment is transferred
  between them without a typed same-law inequality.

All leaves agree on `0/5` and `CM2=NO-GO_FOR_CLAIM`; Gate 5 alone carries
the unchanged maturity `10/18`, blocks `0`.

## 6. Red-team corrections before freeze

The frozen leaves include the following corrections:

1. Gate-1 uniform defect convergence is not said to generate Hölder
   regularity; the required uniform/equi-Hölder approximant modulus is a
   separate row.
2. Gate-4's weighted current traces are not called the original physical
   charge; explicit multiplication by `2^-D_land` is required for recovery.
3. Gate-5's `X_all` is a canonical minimal implementation, not the unique
   legal Borel encoding.  Only loss of `j` or an equivalent immutable
   insertion coordinate is forbidden.
4. Gate-5 uses distinct notation for record spaces `X_j`, scalar charges
   `c_j`, generic Jordan integrands `phi_j`, and separator masses `b_j`.

No unresolved claimed-scope blocker or cross-leaf contradiction remains.

## 7. Source-leaf acceptance matrix

```text
syntax:                         6/6
dependency / baseline pins:    31/31
integrity / replay / reemit:   3/3 each
hostile + strict JSON:          652/652 rejected
SHA sidecar rows:               12/12
default entry points:           6/6 exit 2
stale/temp Round-62 files:      0 after cleanup
```

The total hostile count is `184+300+168=652`; Gate-4/2's `184` is the
root-independent `180` semantic plus `4` strict-JSON attacks.

## 8. Strict final audit state

```text
Gate 1: NOT_CERTIFIED
Gate 2: NOT_CERTIFIED (official fields 0/17)
Gate 3: NOT_CERTIFIED
Gate 4: NOT_CERTIFIED (landing join 1/7; fields 1,4,7 partial)
Gate 5: NOT_CERTIFIED (10/18; complete blocks 0)

complete composite gates: 0/5
CM2: NO-GO_FOR_CLAIM
```

The next shortest routes remain physical rather than algebraic: install the
actual stable product/marker-holonomy and strict landing threshold; prove
all-plaque tempered gauge decay; pay the moving stopped face and bulk Piola
series; and obtain a same-owner insertion-time decay that simultaneously
controls complement, clearance/Orlicz, Jordan/common mode and cemetery.
