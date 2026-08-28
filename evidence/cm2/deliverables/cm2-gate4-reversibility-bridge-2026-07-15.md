# CM2 Gate 4: reversibility and a same-occurrence face-time bridge

Date: 2026-07-15  
Model: centered rational two-disk table, standard solid-boundary section
`N=G disjoint-union W`, with gray radius `9/25`, white radius `4/25`, gray
center `(0,0)`, white center `(1/2,1/2)`, and white translation
`c(s)=(1/2+s,1/2)`.  The frozen v51/v52 files and the shared research log
were read but not edited.

## Decision

**Gate 4 remains `NOT_CERTIFIED`.**  Time-reversal invariance proves a useful
operator-level conjugacy and a local regular tangency gives a finite
order-zero switching current on the compactified target.  It does **not** by
itself produce two typed, nonadditive representations of one immutable
occurrence with identical coefficient measure, polarity and owner.

The obstruction is already visible on one explicit physical tangency:

1. the forward source is an interior non-grazing gray collision and carries a
   nonzero coarea coefficient;
2. the source of the genuinely reversed flight is the white tangency contact,
   which is a grazing boundary point with `cos(phi)=0`;
3. hence invariance of the two-dimensional SRB density
   `cos(phi) dr dphi` cannot identify the nonzero one-dimensional forward
   coarea law with a bounded-density reverse interior standard-family law;
4. the complete defect is reversible, but its event decomposition is only
   permuted/conjugated.  Eventwise equality on the **same occurrence id** is
   an additional theorem, not a consequence of the equality of the sums.

Thus reversibility closes only the pure global algebra below.  Banach typing,
the exact occurrencewise coefficient/current bridge, and both recovery
moments under one single-charged `q` remain open.

The exact quadratic-field checks for the explicit witness are executable in
`cm2_gate4_explicit_tangency_cert.py`; the script deliberately leaves the
same-occurrence and recovery layers fail-closed.

## 1. One instantiated regular moving-target tangency

Let the source be the rightmost point of the central gray disk,

\[
 q=(9/25,0),\qquad d=c(0)-q=(7/50,1/2),
\]

and put

\[
 \ell=\sqrt{|d|^2-(4/25)^2}=\frac{\sqrt{610}}{50},
\]

\[
 u=\left(
 \frac{200+7\sqrt{610}}{674},
 \frac{25\sqrt{610}-56}{674}
 \right).
\]

Direct calculation gives

\[
 |u|=1,\qquad u\cdot d=\ell,\qquad
 u^\perp\cdot d=4/25.
\]

Numerically,

\[
 u=(0.5532451728\ldots,0.8330184744\ldots),\qquad
 \ell=0.4939635614\ldots .
\]

The gray outgoing flux is non-grazing because `u_x>0`.  The line segment
`q+[0,ell]u` is tangent to the central white disk.  It is a physical first
singularity: for example its closest approach to the neighboring gray center
`(1,0)` occurs before the contact and equals

\[
 \frac{16}{25}u_y=0.5331318236\ldots>9/25;
\]

the other nearby gray and white lifts are excluded immediately by the
coordinate box
`x in [0.36,0.634]`, `y in [0,0.412]` (the central white disk is the only
exception, and is met tangentially).  Hence a sufficiently small source
chart around this point is a genuine one-target tangency chart.

With `u` fixed at the displayed source point, define the standard circular
discriminant

\[
 H_s=R^2-\{u^\perp\cdot(c(s)-q)\}^2,
 \qquad R=4/25.
\]

At the tangency,

\[
 \partial_sH_0=2Ru_y
 =\frac{4(25\sqrt{610}-56)}{8425}>0,
 \qquad
 \partial_\varphi H_0=2R\ell
 =\frac{4\sqrt{610}}{625}>0.
\]

Thus this is a regular, nonzero moving-target coarea occurrence.  If the gray
boundary is parametrized by polar angle `theta`, with arclength
`r=(9/25)theta`, implicit differentiation of `H=0` gives

\[
 \frac{d\varphi}{d\theta}
 =-\frac{\ell+(9/25)u_x}{\ell}
 =-1.4032043611\ldots,
 \qquad
 \frac{d\varphi}{dr}=-3.8977898921\ldots .
\]

The forward singularity curve is therefore stable-oriented in the usual
Birkhoff convention; applying the phase involution changes the sign of this
slope, but produces the past-tangency chart, not an identity of occurrence
currents.

At the contact point the velocity is tangent to the white circle.  Specular
reflection leaves it unchanged, so the corresponding white collision has
`cos(phi_W)=0`.  It is on the phase boundary of `N`, not in an interior
homogeneous standard curve.

## 2. Layer A: what reversibility proves algebraically

Let `P_s` be the push-forward transfer operator on measures on `N`, and let
`R` be push-forward by the billiard time-reversal involution.  For every
fixed table,

\[
 P_s^{-1}=R P_s R,\qquad R^2=I.
\]

At `s=0`, differentiating the inverse identity gives

\[
 R\dot P R=-P^{-1}\dot P P^{-1},
 \qquad
 \boxed{\dot P=-P R\dot P R P}.                 \tag{2.1}
\]

Consequently, for every typed source `eta` and test `phi` for which all
pairings make sense,

\[
 \langle\dot P\eta,\phi\rangle
 =-\langle\dot P(RP\eta),R^*P^*\phi\rangle.     \tag{2.2}
\]

This is the exact **complete-defect** forward/reverse scalar identity.  It is
the full algebraic content supplied by reversibility.

Now decompose the physical defect into immutable event rows,

\[
 \dot P=\sum_{a\in A}D_a.
\]

Equation (2.1) gives only

\[
 \sum_aD_a=-PR\left(\sum_aD_a\right)RP.
\]

It does not give

\[
 D_a=-PRD_aRP                                      \tag{2.3}
\]

for each `a`.  In a billiard atlas, reversal normally sends `a` to a distinct
past-event row `rho(a)`, may exchange the two one-sided traces, and reverses
the coarea orientation.  The eventwise statement that is actually needed is

\[
 D_a=-PRD_{\rho(a)}RP                              \tag{2.4}
\]

together with a Borel identification of `a` and `rho(a)` as two views of one
unoriented physical incidence.  Neither (2.4) nor this quotient of the event
registry follows from (2.1).

This logical distinction is strict: a symmetry may swap two disjoint event
currents while leaving their sum equivariant.  Equality of the equivariant
sum then contains no assertion that either tagged summand is fixed.  Merging
the swapped tags without an exact scalar-current proof either changes the
physical sum or counts the coefficient twice.

### Local order-zero statement

On a regular switching face `Sigma={H_0=0}`, the Reynolds/coarea term has the
form

\[
 J_{\rm face}(\Phi)=
 \int_\Sigma b(x)
 \{\Phi(F_0^{\rm miss}x)-\Phi(F_0^{\rm hit}x)\}\,d\sigma(x),
 \qquad
 b=h\rho\frac{\partial_sH_0}{{|\nabla H_0|}}.
                                                        \tag{2.5}
\]

On a compact regular chart this is a finite order-zero signed measure on the
**compactified** target, provided both one-sided traces are retained.  This
closes a local algebraic/order-zero sublayer.  It does not make either trace
a positive proper standard family, and it does not identify (2.5) with its
reversed occurrence on every record restriction.

For the induced Stenlund section `M`, the hit continuation and direct trace
agree at a regular tangency, so the artificial face term cancels.  On the
direct solid-boundary section `N`, the one-step hit trace is instead the white
grazing state while the miss trace is a later solid collision; the induced
trace cancellation cannot simply be imported.

## 3. Layer B: Banach typing is not supplied by reversibility

The invariant collision law is

\[
 d\mu=Z^{-1}\cos\varphi\,dr\,d\varphi,
 \qquad R_*\mu=\mu.
\]

At the displayed forward source, `cos(phi)=u_x>0`, and the two nonzero
derivatives of `H` above give a nonzero finite coarea coefficient.  The
genuinely reversed flight starts at the tangent white contact, where
`cos(phi_W)=0`.  Therefore there is no bounded Radon--Nikodym density that
turns the interior SRB flux at that reversed source into the nonzero forward
coarea coefficient.  Invariance of `mu` is a two-dimensional statement and
does not perform this singular one-dimensional change of variables.

The full tangent area formula contains, in addition to the SRB factor,
`|nabla H|^{-1}`, the curve Jacobian, the billiard derivative and all
one-sided trace choices.  At grazing, these factors have nontrivial
zero/infinity cancellation.  Reversibility says the correctly constructed
reverse formula has the same *form*; it does not construct its chart or prove
that its coefficient is the same measure `m`.

Accordingly:

- the face current (2.5) is locally order zero only on a compactified
  trace space;
- its white-hit trace is not an interior homogeneous standard curve;
- the clean-diffeomorphic-branch order-reduction theorem does not apply at
  this tangency;
- a separately typed flux/cemetery source, or an exact one-sided continuation
  through the tangent contact to the next non-grazing collision, is required;
- that continuation must prove the restrictionwise scalar identity, not only
  a norm inequality.

The explicit negative face slope also shows why analyticity is insufficient:
the source face is stable-oriented forward.  Hyperbolicity does not turn a
stable tangent into a forward unstable standard curve on a smooth branch.
The reverse orientation is geometrically plausible, but plausibility of one
orientation is not the required pair of exact alternative views.

## 4. Layer C: recovery moments are a separate obstruction

Even if an eventwise identity (2.4) and two typed sources were constructed,
SRB invariance would still not imply the stopped/restricted recovery bounds.
The relevant law is the singular occurrence envelope `q` after owner, clock,
word and carrier restrictions, not the unconditioned probability `mu`.

For one occurrence `a`, the required data are

\[
 J_a=\langle U_a^-\nu_a^-,E_a^-\rangle
    =\langle U_a^+\nu_a^+,E_a^+\rangle,           \tag{4.1}
\]

with the same immutable

\[
 (a,\operatorname{phys},\text{coefficient},m,
   \operatorname{polarity},\operatorname{owner}),
\]

and predictable oriented costs `C_a^-`, `C_a^+`.  Before a product-time query
is known one must set

\[
 \boxed{q_a=\max\{C_a^-,C_a^+\}\,m_a}             \tag{4.2}
\]

and charge it once.  Both recovery clocks must then satisfy their exponential
moments under restrictions of this exact `q_a`.  Neither a moment under `mu`,
nor two moments under separately normalized laws, nor
`q_a^-+q_a^+` proves this statement.

The latest standard-family results used in v52 start only after a concrete
positive regular family has been produced.  They do not produce the missing
grazing trace continuation, eventwise reverse identity, or stopped-parent
moments.  Likewise the recent discontinuous-map response theorem assumes the
summable foliation/recovery input; it does not derive it from reversibility.

## 5. Conditional same-occurrence bridge theorem

The following small theorem isolates exactly what would close the local Gate
4 row.

**Theorem (single-charge bidirectional occurrence).**  Let `A` be a fixed
standard-Borel occurrence registry.  Suppose that for every `a` in a Borel
set `A_bi` the following are constructed before any product-time query:

1. one positive coefficient measure `m_a`, one polarity and one owner;
2. two typed positive source/operator/test tuples satisfying (4.1) on every
   record-measurable restriction;
3. proper-family recovery times `R_a^-`, `R_a^+` and finite predictable costs
   `C_a^-`, `C_a^+` containing every carrier, operator, density, boundary and
   recovery weight;
4. the two exponential recovery moments and proper-source domination on the
   common law (4.2).

Then the two tuples are nonadditive views of one occurrence, `q_a` is counted
once, and a fixed deterministic priority may choose an available long-side
view without putting the unused view into the positive tail.

**Proof.**  Equality (4.1) makes either tuple a representation of the same
scalar summand on every restriction.  The pointwise maximum in (4.2)
dominates both predictable costs and is one measure on the one base row.
Selecting a view therefore changes only a factorization, not the occurrence
sum or its mass.  The two assumed moments give the corresponding recovery
tail estimates by Markov's inequality; a pre-fixed priority makes the chosen
level sets Borel and disjoint.  No second copy of `m_a` or `q_a` is introduced.

This theorem is deliberately conditional.  Reversibility supplies (2.1),
but none of items 2--4 occurrencewise for the explicit tangent event.

## 6. Minimum decision-changing evidence still required

For the explicit event above (and then for every row of the global event
manifest), the first evidence that would change the verdict is:

1. an unoriented physical-incidence id and a Borel reversal map identifying
   the forward and past event charts without merging additive currents;
2. an exact trace-by-trace proof of (2.4), including the inverse-derivative
   minus sign, parameter polarity, lift, first-hit root and occurrence time;
3. a common-base proof that the forward and reverse coarea coefficients are
   the same `m`, including the grazing flux/Jacobian cancellation;
4. a typed reverse source for the white grazing trace (or an exact grouped
   continuation to a non-grazing target) and a simultaneous bounded physical
   test lift;
5. finite `C_fw,C_rev`, the immutable digest of
   `q=max(C_fw,C_rev)m`, and restrictionwise `m/q/current` matching;
6. both proper-family recovery clocks and their exponential moments under
   that identical `q`, including the stopped-parent/owner restrictions;
7. a pre-query orientation policy and an exponentially small set on which no
   active long-side representation is available.

Until these fields exist, the exact status is:

```text
GLOBAL_REVERSIBILITY_ALGEBRA: PROVED
LOCAL_REGULAR_FACE_ORDER_ZERO_ON_COMPACTIFICATION: PROVED
EVENTWISE_SAME_OCCURRENCE_IDENTITY: NOT CERTIFIED
FORWARD_REVERSE_BANACH_TYPING: NOT CERTIFIED
SINGLE_CHARGE_q_MAX: NOT CERTIFIED
BIDIRECTIONAL_RECOVERY_MOMENTS: NOT CERTIFIED
GATE_4: NOT CERTIFIED
```

## Reproduction

```bash
python3 -m py_compile deliverables/cm2_gate4_explicit_tangency_cert.py
python3 deliverables/cm2_gate4_explicit_tangency_cert.py
sha256sum -c deliverables/cm2-v52-manifest.sha256
```

## 7. v52 audit anchors

- Lines 744--908: the two recovery views must represent the same coefficient
  occurrence and physical current; they are alternatives, not summands.
- Lines 4422--4580: occurrence fields are immutable, exact current matching is
  restrictionwise, and the maximum recovery envelope is charged once.
- Lines 7332--7377: forward and reverse tangent-coarea formulas require the
  full curve Jacobian; reversibility supplies the form, not the event row.
- Lines 9733--9758: reverse mixing is available only after a separately typed
  reverse representation has been constructed.
- Lines 11134--11147 and 12281--12298: common invariance/reversibility do not
  identify a moving coarea occurrence with its source proposal.
- Lines 11685--11718: regular tangency trace cancellation is an induced-section
  statement and does not apply a transfer block to a grazing boundary point.
- Lines 11848--11926: regular circular tangency has local square-root
  integrability and a finite positive current envelope, but attachment to the
  complete occurrence tree remains global work.
- Lines 13952--13972: an analytic face can have only one clean orientation,
  and two additive one-sided occurrences do not satisfy same-occurrence face
  time.
