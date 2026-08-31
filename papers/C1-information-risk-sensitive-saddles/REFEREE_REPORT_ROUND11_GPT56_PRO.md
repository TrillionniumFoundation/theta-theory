# Independent Referee Report — Round Eleven

**Manuscript:** C1 — Information and Risk-Sensitive Saddles  
**Editorial standard:** *Annals of Mathematics*, *Acta Mathematica*, *Inventiones Mathematicae*, or *JAMS*  
**Recommendation:** **Reject**  
**Reviewed branch:** `revision/round11-referee-positive-closure-11paper-2026-08-31@e81cbf57624d21be23ee9d982a1255c076363761`  
**Reviewed source:** `revision/round11-referee-final/C1_SLICED_CURRENT_ZERO_EVIDENCE_FILTER.tex` (Git blob `20d0f13d2f0cc0892e61b5d4507d82788fe237e0`))

## Executive assessment

The paper now uses Federer slices rather than ordinary restriction to a level set, retains unnormalized evidence, and attempts to compactify the zero-evidence direction. These are appropriate responses to the previous report.

The resulting state is still not mathematically typed. A positive-dimensional normal current cannot be paired with the scalar \(1\) to define evidence, and replacing that pairing by mass would be nonlinear and orientation-dependent. The asserted projective current sphere is not compact in the declared infinite-dimensional topology. The Feller kernel, inserted coefficient theorem, reachable-chaos reduction, and Bernstein–Von Mises conclusion therefore have no established state space.

## Major mathematical objections

### 1. The evidence pairing is ill-defined for normal currents

An \(r\)-dimensional current acts on \(r\)-forms. After slicing a high-dimensional phase current by a \(d\)-dimensional observation, the result generally still has positive dimension. The expression

\[
Z=\langle1,\Lambda\rangle
\]

is therefore not defined: \(1\) is a \(0\)-form.

If the authors intend the mass \(\mathbf M(\Lambda)\), that quantity is nonlinear, loses orientation information, and is not the Bayes evidence of a general slice. A separate positive measure/disintegration coordinate is required.

### 2. Normal-current orientation and posterior positivity are conflated

Federer slices are oriented currents and need not be positive measures. A posterior is a positive probability measure. The manuscript does not identify a positive coefficient measure on each slice, show that prediction/reflection preserve positivity of that coefficient, or explain how lower-rank components are normalized consistently.

### 3. The projectivized weighted current sphere is not compact

The unit sphere of an infinite-dimensional mass-plus-boundary Banach space is not compact. Federer–Flemming compactness requires fixed dimension, locally compact support or tightness, and uniform mass and boundary mass. Here the state is a countable direct sum of strata with unbounded weights and changing codimension. “Compact after projectivation” is false without a much stronger topology and compact-containment theorem.

Hence a sequence with evidence tending to zero need not have a convergent projective subsequence in the proposed state space.

### 4. Local finiteness of the observation–collision complex is unproved

Repeated observations, collision faces, lower-rank sets, and Whitney refinements can create infinitely many strata accumulating in a compact region. A finite observation family does not imply that the chronological countable refinement is locally finite. The B2 trace complexity estimate concerns collision histories, not arbitrary observation singular sets.

### 5. Closedness of slices is overstated

Slicing is defined for almost every level and is stable in integrated mass, not necessarily pointwise in \(y\) under ordinary weak convergence. A Feller observation kernel needs a measurable disintegration and continuity after integration over observations. The theorem instead asserts a closed pointwise update on the completed current domain.

### 6. The zero-evidence transition is not uniquely determined by adjoining one direction

Even if a projective direction is retained, prediction or the next slice may send that direction to zero again, requiring a further blow-up. Continuity must be checked for every transition and independent of the approximating sequence. The proof only notes that the unnormalized payoff is multiplied by \(Z_n\); future normalized belief values can still depend discontinuously on the direction.

### 7. The inserted coefficient theorem inherits the false B1 block construction

The proof adjoins observations to the B1 dynamic blocks. Those linearly many spatially independent blocks do not exist. Moreover, an additive global path/contact statistic can couple all local cells through its exponential tilt; additivity does not imply conditional independence.

### 8. Analytic division requires complex zero-free control

A positive real evidence denominator on a compact chart may have complex zeros arbitrarily close to the real domain. Dividing two analytic generating functionals does not automatically preserve a common analytic radius. The reachable-chaos theorem assumes the zero-free estimate it needs to prove.

### 9. Cumulant bounds do not imply Wasserstein kernel reduction by themselves

Bounds of the form \(C^j\mu^{1-j}\) on listed connected currents do not automatically construct a coupling between the full belief transition and a reduced finite coordinate transition. Moment determinacy, tail control, and a quantitative metric comparison are required. The Bellman error estimate is therefore unsupported.

### 10. The Bernstein–von Mises theorem is only a list of standard hypotheses

LAN, positive information, posterior tightness away from phase boundaries, and a uniform local coefficient under adaptive control are all assumed. None is proved from the preceding current construction.

## Status of earlier objections

The manuscript correctly replaces level-set restriction by slicing and explicitly recognizes zero-evidence directions. The new current/evidence state is ill-typed and noncompact, so the repair does not close the filtering theorem.

## Minimum reconstruction

The authors need a positive sliced-measure/disintegration framework separate from oriented currents, a rigorously compact projective state topology, and a Feller theorem formulated after integrating over the observation law. Statistical reduction and BvM should be deferred until that state and the B1 coefficient theorem exist.

## Recommendation

**Reject.** The intended geometric filtering state is not a well-defined compact Bayes state, and all downstream control/statistical claims depend on it.