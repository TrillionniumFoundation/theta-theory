# CM2 Gate 1: canonical-holonomy resonance audit

Date: 2026-07-15  
Model: frozen centered rational fixed-section pilot  
Scope: the natural physical derivative cocycle at the exact QNL period-two orbit  
Verdict: **Park--Piraino is NO-GO on the two frozen natural codings; the Butler--Park class-`H` canonical-limit condition fails for any faithful coded representative retaining the QNL stable branch in the frozen natural trivialisation; a new cohomology/non-fiber-bunched theorem or genuinely alternative coding remains open; unconditional Gate 1 remains OPEN / NO-GO**

## 1. Result

The earlier audit showed only that the two natural codings fail the usual
uniform fiber-bunching inequality.  That left open the logical possibility
that the canonical limits might nevertheless converge by a special
cancellation.  The new exact cubic calculation closes that loophole.

Let `F` be the physical gray--white--gray QNL return in exact QNL
eigen-coordinates `(x,y)`, with `x` unstable and `y` stable.  Write

```text
A = D F(0) = diag(lambda,mu),   lambda*mu=1,
lambda>1, 0<mu<1.
```

The frozen exact Taylor algebra gives

```text
all second derivatives of F at 0 = 0,
partial_x partial_y^2 F_2(0) / mu = -325/72.
```

For every sufficiently local nonzero `z` on `W^s(QNL)`, the canonical
stable comparison sequence

```text
H_n = D F^n(z)^(-1) D F^n(0)
```

does **not** converge.  More precisely, if `c(z) != 0` is the asymptotic
stable coordinate defined below, then

```text
lim (H_n^(-1) H_(n+1))_21 = (325/144) c(z)^2 > 0.
```

Convergence of `H_n` would force `H_n^(-1)H_(n+1) -> I`, so the displayed
strictly positive limit is a contradiction.  This is a local obstruction
at the selected QNL pinching fiber; it is independent of the symbolic
metric and stronger than failure of a sufficient fiber-bunching bound.

Consequently:

| statement | verdict |
|---|---|
| finite 96-collision same-orbit shadow | **CERTIFIED by frozen predecessor** |
| four finite-shadow wedges | **CERTIFIED by frozen predecessor** |
| QNL canonical stable holonomy for the physical derivative | **DOES NOT CONVERGE** |
| Butler--Park class-`H` canonical-limit condition for a faithful frozen-trivialisation representative | **FAILS** |
| faithful Hölder cohomology to a locally constant QNL cocycle | **NOT CERTIFIED; not refuted here** |
| finite shadow equals a QNL holonomy loop | **REFUTED** |
| Park--Piraino on the two frozen natural codings | **NO-GO by periodic fiber-bunching obstruction** |
| Butler--Park `H` after a new certified cohomology/non-FB theorem | **OPEN; not refuted here** |
| genuinely alternative coding/transport | **OPEN; not refuted here** |
| unconditional CM2 Gate 1 | **OPEN / FAIL-CLOSED** |

No claim about the certified literal common vertex, 24-collision
four-face full cross, 96-collision closed shadow, or its finite derivative
wedges is retracted.

## 2. Exact resonant-increment lemma

The following elementary lemma isolates the entire obstruction.

**Lemma.**  Let `F` be a `C^3` area-preserving local diffeomorphism of the
plane fixing the origin.  In coordinates with

```text
D F(0)=diag(lambda,mu),  lambda*mu=1,
lambda>1, 0<mu<1,
```

assume all quadratic derivatives vanish and put

```text
g = (1/2) partial_x partial_y^2 F_2(0).
```

If `g != 0`, then for every sufficiently local nontrivial
`z in W^s_loc(0)`, the sequence

```text
H_n=D F^n(z)^(-1)D F^n(0)
```

cannot converge whenever `-lambda*g != 0`.

**Proof.**  The local stable graph has the form `x=h(y)`.  Its tangent is
the `y` axis.  The vanishing quadratic jet and the invariance equation give
`h''(0)=0`, hence `h(y)=O(y^3)`.  On the graph,

```text
y_(n+1)=mu*y_n+O(y_n^3).
```

The convergent infinite product for this one-dimensional contraction gives

```text
y_n/mu^n -> c(z) != 0
```

for nonzero `z`.  If `B_n=D F(F^n z)` and `b21(n)` is its lower-left
entry, Taylor expansion along the stable graph yields

```text
b21(n)=g*y_n^2+o(y_n^2).
```

With `P_n=D F^n(z)` and `A=D F(0)`, set `H_n=P_n^(-1)A^n`.  Exact cocycle
algebra gives

```text
K_n := H_n^(-1)H_(n+1)=A^(-n) B_n^(-1) A A^n.
```

Because `det B_n=1`, the `(2,1)` entry is exactly

```text
(K_n)_21 = -lambda*(lambda/mu)^n*b21(n).
```

Using `lambda*mu=1` and the stable asymptotic gives

```text
(K_n)_21 -> -lambda*g*c(z)^2.
```

If `H_n` converged, its determinant-one limit would be invertible and
`K_n=H_n^(-1)H_(n+1)` would tend to the identity, a contradiction.  QED.

For the exact QNL jet,

```text
g = -(325/144) mu,
-lambda*g = 325/144.
```

Thus the limiting obstruction has a fixed positive coefficient, with no
interval sign decision and no fitted numerical constant.

## 3. Why this is the relevant canonical limit

Butler--Park, arXiv:1909.11548v2, equations defining their class `H`, require
for every stable pair `x,y` the convergence of

```text
H^s_(x,y)=lim A^n(y)^(-1)A^n(x),
```

and Hölder continuity of the resulting holonomies.  Park--Piraino's
typicality loop likewise uses stable and unstable holonomies on a genuine
homoclinic point of the pinching periodic fiber.

Take `x` to be the QNL periodic point and `y=z` on its local stable
manifold.  The sequence in the lemma is exactly that canonical limit for
the induced two-collision return.  If a canonical holonomy existed for the
original solid-collision cocycle, its even-time subsequence would converge;
the induced nonconvergence rules this out too.  Thus any faithful symbolic
representative that contains this physical stable pair and keeps the frozen
natural trivialisation fails the class-`H` canonical-limit condition.  A
global faithful coding has not itself been constructed, so this statement
is deliberately conditional on such a representative rather than a claim
that an unconstructed global object is outside `H`.

Any nontrivial QNL-homoclinic point eventually enters the local stable
manifold at a nonzero point.  Invertibility prevents it from landing
exactly on the QNL periodic point in finite time.  A finite prefix or suffix
cannot repair failure of the local canonical tail.  Hence constructing a
new exact homoclinic orbit through the already certified full cross would
not close the canonical-holonomy gate for this cocycle.

This conclusion is for the frozen natural physical derivative in its
declared smooth Birkhoff/eigencoordinate trivialisation.  It must not be
promoted to a general cohomology obstruction.  Under a point-dependent
fiber gauge, the terminal gauge discrepancy is conjugated by long
hyperbolic products and need not remain small without an additional
bunching/rate estimate.  Therefore a faithful Hölder cohomology to a
locally constant model is **not certified**, but is not refuted solely by
the calculation above.

## 4. Why the finite shadow remains a different object

The frozen 96-collision word is a genuine periodic orbit `z_*` distinct
from the QNL orbit.  Its derivative is a legitimate endomorphism of
`T_(z_*)M`, and its four finite wedges are strict.  It is not a QNL
homoclinic point, and the raw identification of `T_(z_*)M` with the QNL
fiber by the common `(s,p)` chart was already shown to be gauge-dependent.

The new result is stronger: even replacing `z_*` by a genuine homoclinic
orbit would not create the canonical stable tail required by the cited
typicality framework.  The problem is the resonant cubic jet at QNL, not
the accuracy or dwell length of the finite shadow.

## 5. Literature audit through 2026-07-15

The audit used the live arXiv API and exact paper sources.  The following
are the closest alternatives located; none supplies the missing theorem.

1. **Butler--Park, arXiv:1909.11548v2.**  Fiber bunching is not necessary
   in their abstract class `H`, but convergence and Hölder regularity of the
   canonical holonomies are explicit assumptions.  The exact QNL resonance
   above refutes the first assumption.

2. **Freijo--Marin, arXiv:1910.14102v2.**  Non-uniform fiber bunching gives
   full-measure non-uniform holonomy blocks.  Their Lyapunov-continuity
   Theorem A additionally assumes one uniform stable holonomy (or the
   reversed analogue), while the locally constant special case is handled
   separately.  It is not a pinching--twisting/projective spectral-gap
   theorem at a prescribed periodic fiber; a measure-full block may simply
   exclude QNL.  It therefore does not override the direct failure of the
   frozen natural canonical stable limit at QNL.

3. **Mohammadpour--Varandas, arXiv:2508.05771.**  The abstract and main
   framework explicitly assume a `1`-typical **fiber-bunched** cocycle.
   This does not cover the QNL derivative.

4. **Rush, arXiv:2601.14061.**  The 2026 Frostman theorem concerns compactly
   supported i.i.d. `SL(2,R)` products satisfying strong irreducibility and
   proximality.  It is useful only after an actual random/product quotient
   has been constructed; it neither constructs billiard holonomies nor
   turns the place-dependent physical derivative into an i.i.d. law.

5. **Kalinin--Sadovskaya, arXiv:2604.13401.**  The 2026 periodic-data rigidity
   results require conjugate periodic data together with narrow-spectrum,
   constant-cocycle, measurable-cohomology, or bounded-conjugacy hypotheses.
   Their differentiable stable-holonomy conclusion is derived inside that
   rigidity setting.  None of those hypotheses or a corresponding
   cohomology is certified here.

6. **Locally constant/one-step matrix products.**  They possess identity
   canonical holonomies without fiber bunching, but freezing each billiard
   word to its periodic matrix changes the actual place-dependent
   derivative.  No faithful Hölder transfer making that shortcut exact is
   currently certified; the natural-gauge resonance alone does not refute
   every such transfer.

The arXiv search also returned no 2024--2026 theorem that simultaneously
accepts a singular dispersing-billiard derivative, dispenses with canonical
holonomy convergence, and concludes the Park--Piraino projective spectral
gap from a finite shadow product.

## 6. Minimal honest remaining route

Park--Piraino on either frozen natural coding is closed-negative: its
periodic fiber-bunching obstruction is preserved under a same-coding
Hölder cohomology because the periodic return products remain conjugate and
retain their eigenvalue ratio.  Independently, the Butler--Park class-`H`
canonical-limit condition fails for any faithful representative retaining
the physical QNL stable branch in the frozen natural trivialisation, by the
new `325/144` resonance.  Continuing to lengthen the shadow word cannot
change either obstruction.

A separately certified cohomology that creates valid canonical holonomies
could still open a Butler--Park/non-fiber-bunched route, because natural-gauge
canonical-limit convergence is not invariant under arbitrary point-dependent
gauges.  A genuinely alternative coding or invariant transport is likewise
not refuted here.  Neither object is currently certified.

An unconditional proof must instead replace this route with a theorem whose
objects do not require the failed full-tangent canonical holonomy.  The two
remaining plausible directions are:

1. construct the actual full-mass physical quotient and prove the required
   projective Frostman/PPE estimate directly by pair-energy or
   place-dependent kernel methods; or
2. identify a different, explicitly typed lower-dimensional cocycle with
   its own invariant transport and prove that its projective coordinate is
   exactly the physical endpoint slope.

Both are Gate-2-level constructions.  Neither is supplied by the literal
Gate-1 full cross or by the finite shadow.  Therefore the correct final
labels remain

```text
QNL_CANONICAL_STABLE_HOLONOMY: DOES_NOT_CONVERGE
PARK_PIRAINO_ON_TWO_FROZEN_NATURAL_CODINGS: NO_GO
BUTLER_PARK_H_VIA_NEW_COHOMOLOGY_OR_OTHER_NON_FB_THEOREM: OPEN
GENUINELY_ALTERNATIVE_CODING_OR_TRANSPORT: OPEN
FINITE_SHADOW_TRANSPORTED_TWISTING: CERTIFIED
GATE1_UNCONDITIONAL_TYPICALITY_INPUT: OPEN / FAIL-CLOSED
UNCONDITIONAL_CM2: NO_GO FOR CLAIM
```

## 7. Reproduction

```bash
/tmp/cm2-flint-venv/bin/python -m py_compile \
  deliverables/cm2_gate1_canonical_holonomy_resonance_cert.py \
  deliverables/cm2_gate1_canonical_holonomy_resonance_manifest_verifier.py

/tmp/cm2-flint-venv/bin/python \
  deliverables/cm2_gate1_canonical_holonomy_resonance_cert.py

/tmp/cm2-flint-venv/bin/python \
  deliverables/cm2_gate1_canonical_holonomy_resonance_manifest_verifier.py \
  --self-test

/tmp/cm2-flint-venv/bin/python \
  deliverables/cm2_gate1_canonical_holonomy_resonance_manifest_verifier.py
# expected exit 2: unconditional Gate 1 remains fail-closed

sha256sum -c \
  deliverables/cm2-gate1-canonical-holonomy-resonance-manifest-2026-07-15.sha256

sha256sum -c deliverables/cm2-v52-manifest.sha256
```

The positive obstruction certificate and verifier self-test must exit zero.
The live completion check must exit `2` by design.  No v51/v52 artifact,
Gate-3 atlas, or shared research log is modified.
