# CM2 Gates 4--5: immutable-subrow Kac/q ledger assault

Date: 2026-07-15  
Model: centred rational two-disk pilot on the standard solid-boundary section
`N=G disjoint-union W`  
Verdict: **a refined 64-component certified bulk now has an exact structural
same-occurrence/common-`m`/single-`q` Kac ledger, and one complete four-row
physical symmetry orbit has exact `mu(dot r)=0`; global physical coarea
matching, stopped recovery and the CM2 norm lifts remain `NOT_CERTIFIED`.**

The frozen v51/v52 files and the shared research log were not modified.

## 1. New certified bulk input

The endpoint-identity Gate-3 refinement covers the eight exact source charts
and binds every positive box to the complete label

```text
(source chart, tangent target, tangency sign, miss target, polarity).
```

Its certified positive part contains

```text
11,812 compact physical boxes
64 complete labels
64 connected same-label immutable subrow components
16 exact Jx/Jy four-label symmetry orbits.
```

The boxes have strict first visibility, a unique first non-grazing miss after
the tangent contact, and a constant nonzero parameter polarity.  Therefore
each of the 64 connected unions is already a legitimate physical
**subrow**.  The atlas also proves that box count and parameter area agree
within each symmetry orbit, `Jx` reverses polarity, `Jy` preserves polarity,
and the polarity-weighted parameter area of the certified bulk is exactly
zero.  Relative to the predecessor, the exact identity
`cp^2+p^2=1` and the sign factorization `sign(eta*epsilon*u_y)` remove
70.53% of its unresolved area; the refined certified physical parameter area
is `5569/25600`.

The limitations are binding.  The refinement leaves the exact area fraction

\[
  \frac{5263}{196608}
\]

in unresolved collars.  All surviving endpoint collars are genuine
source-grazing collars (not artificial target-coordinate or `tau=3` tests),
but their outgoing event labels are not all resolved.  The atlas does not
quotient diagonal chart seams and does not claim that the 64 connected
unions are the maximal global physical rows.
Its own `global_dq` and `global_scalar_matching` fields are false.

## 2. Exact 64-component Gate-4 ledger

For every certified connected subrow `e`, let `A_e` be its parameter base,
`z_e(a)` its compactified grazing trace, and `y_e(a)` its certified first
non-grazing miss collision.  The all-sheet reversal theorem now applies
without a missing geometric premise on this bulk:

\[
 J_e(\Phi)=\sigma_e\int_{A_e}
   \{\Phi(z_e(a))-\Phi(y_e(a))\}\,dm_e(a).
\tag{2.1}
\]

Reversing the same oriented ghost/direct path gives a second nonadditive view
of (2.1), and collision-flux preservation transports exactly the same
positive coefficient law `m_e` to that view.  The two views are alternatives;
they are never summed.

Consequently the refined structural ledger has exactly

```text
physical connected subrow occurrences          64
singular Kac coordinates                       128
pre-recovery q expressions                      64
incorrect per-coordinate double-charge count  128.
```

For every occurrence the frozen charge expression is

\[
 q_e=\max\{C_e^{\rm fw},C_e^{\rm rev},2\}\,m_e.
\tag{2.2}
\]

This is an exact **pre-recovery expression ledger**.  It proves the counting
and common-law statement, not numerical finiteness of the missing physical
CM2 costs `C_e^fw,C_e^rev`.  Distinct connected subrows remain additive.

## 3. Typed singular Kac current on every certified subrow

At the bounded-Borel level the types are now explicit on all 64 components:

```text
m_e                         in M_+(A_e)
J_e(h)                      in M_b(compactified N)
dual tests                  in B_b(compactified N)
singular coordinate mark   (+1,-1).
```

The two singular Kac coordinates on one occurrence are

```text
moving-level dot(S) face,
roof dot(r) times the phase mean.
```

They share the single coefficient law `m_e` and are contracted with the
fixed mark `(+1,-1)`.  For bounded `h,g`, the exact row pairing is

\[
 \int_{A_e}g(x_e(a))
 \{h_1(z_e(a))-\widehat\mu(h)\}\,dm_e(a),
\tag{3.1}
\]

and hence

\[
 |(3.1)|\le
 2\|h\|_\infty\|g\|_\infty m_e(A_e).
\tag{3.2}
\]

The executable independently replays the exact finite endpoint adjoint,
normalized Kac tower and prefix/suffix pairings.  Thus the bounded-Borel
singular current is genuinely typed; it is not merely a formal label.

## 4. What is now proved about `mu(dot r)=0`

Two different cancellations must not be conflated.

### 4.1 Complete physical four-row orbit

The previously certified immutable orbit

```text
id, Jx, Jy, JxJy
```

contains two exact `Jx` coefficient-law pairs.  Their polarity pattern is
`(+,-,+,-)`, and `Jx` transports the full coarea law of one member to the
other.  If the pair laws are denoted `m_0,m_1`, the scalar roof coefficient
is identically

\[
 (+1-1)m_0+(+1-1)m_1=0.
\tag{4.1}
\]

Therefore

```text
mu(dot r) on this complete four-row physical orbit = 0: CERTIFIED.
```

This is coefficientwise, not a floating-point mass comparison.

### 4.2 The refined 64-component bulk

The bulk symmetry audit proves exact cancellation of **parameter area**.
It does not yet prove equality of the physical coarea-current laws on every
paired component, because the unresolved collars and seam quotient are not
the global DQ/scalar match.  Therefore the following stronger statement is
deliberately rejected:

```text
physical mu(dot r) obtained by summing only the 64 bulk rows: NOT_CERTIFIED.
```

This verdict is deliberately scoped to the structural Kac/q artifact, which
does not import a physical coarea transformation theorem.  A separate later
certificate, `cm2_gate3_bulk_jx_coarea_pairing_cert.py`, replays these same
11,812 refined boxes and proves the exact `Jx` pushforward of the positive
physical coarea laws.  That separate artifact certifies the refined-bulk
**scalar** `mu(dot r)=0`, but still does not prove arbitrary-test DQ or a
CM2 current norm.  The false fields in this ledger therefore prevent an
unsupported inference inside this artifact; they do not contradict the
separately typed scalar certificate.

Independently, the fixed collision-flux gauge gives the already certified
global scalar identity `mu_N(dot r)=0` whenever the displayed Borel current
pairings exist.  This global algebraic identity cannot be used to invent the
missing rowwise physical current match or its norm bound.

## 5. Sharp CM2 typing obstruction

The bounded-Borel type in Section 3 is strictly weaker than the required
standard-family/flux-face versus dynamic-`C^1` CM2 pair.

On a two-point reflection orbit consider the exact signed current

\[
 J_n=n(\delta_a-\delta_b).
\]

For every `n`, `J_n(1)=0`, but the reflection-odd test `(1,-1)` gives `2n`
and `||J_n||_TV=2n`.  The executable checks the scale family through
`n=128`, where both exact quantities are 256.  Thus scalar roof cancellation
and the fixed `(+1,-1)` mark imply neither current cancellation against
general tests nor a uniform physical norm.

The exact arbitrary-Borel recovery obstruction also remains: a positive-mass
fat-Cantor restriction stays nowhere dense under every finite clean branch
and cannot equal a positive-density interval standard pair.  Hence the
single-`q` expression (2.2) cannot be promoted to a global recovery measure
without either a controlled interval/cylinder stopped algebra or the actual
Gate-2 stopped-parent PPE.

The minimal missing quantitative fields are now isolated:

1. a homogeneity-cut registry and cut-growth sum;
2. numeric forward standard-family/flux cost `C_fw` on every row;
3. numeric reverse cost `C_rev` on every row;
4. dynamic `C^1` test-pullback constants;
5. a bidirectional stopped-parent recovery envelope under one frozen `q`;
6. physical prefix/suffix inverse-Jacobian and distortion sums.

Without these, none of the standard-family, flux-face or dynamic-test CM2
norm lifts follows from the exact finite ledger.

## 6. Fail-closed verdict

```text
64-COMPONENT STRUCTURAL OCCURRENCE LEDGER: CERTIFIED
SAME-OCCURRENCE TWO-VIEW/COMMON-m ON ALL 64: CERTIFIED
ONE PRE-RECOVERY q EXPRESSION PER COMPONENT: CERTIFIED
BOUNDED-BOREL SINGULAR KAC TYPING ON ALL 64: CERTIFIED
FOUR-ROW PHYSICAL ORBIT mu(dot r)=0: CERTIFIED
BULK PARAMETER-AREA PROXY CANCELLATION: CERTIFIED

BULK PHYSICAL COAREA-CURRENT MATCHING: NOT_CERTIFIED
BULK PHYSICAL mu(dot r) FROM ROWS: NOT_CERTIFIED
MAXIMAL GLOBAL PHYSICAL EVENT ROWS: NOT_CERTIFIED
GLOBAL STOPPED-PARENT RECOVERY: NOT_CERTIFIED
PHYSICAL FOUR-TERM CM2 TYPING: NOT_CERTIFIED
STANDARD-FAMILY CM2 NORM LIFT: NOT_CERTIFIED
FLUX-FACE CM2 NORM LIFT: NOT_CERTIFIED
DYNAMIC-TEST CM2 NORM LIFT: NOT_CERTIFIED
GATE 4: NOT_CERTIFIED
GATE 5: NOT_CERTIFIED
```

No unconditional CM2 claim follows from this partial but exact promotion.
