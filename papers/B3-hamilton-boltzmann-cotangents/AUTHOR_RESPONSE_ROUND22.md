# Author response to Referee Round Twenty-Two — B3

The referee's explicit Hessian computation is correct.  The former formula has been removed and the action is now expanded in a normal defect coordinate.

## B3.1 — global form comparison

The regular reference path is globally comparable above and below with fixed Maxwellian weights, with weighted derivative bounds.  The collision form is therefore globally comparable with the cutoff Maxwellian form.  Compact-by-compact positivity is not used to claim one global coercivity constant.

## B3.2 — closed range

The paper proves closed range of the linearized balance operator after quotienting the five explicit collision invariants.  It does not infer a general Fredholm theorem or an unrelated finite-dimensional cokernel.  The bounded right inverse follows from the stated transport--collision graph estimate.

## B3.3 — stopping times

At a microscopic stopping time the proof conditions on the complete hard-sphere phase point, for which deterministic flow has the exact restart property.  B2's full collision-history factorial bound is uniform after that restart and gives a conditional increment estimate.  No independent-increment or history-free Markov claim is made for the reduced density.

## B3.4 — second epi-derivative

At the zero-cost reference `Gamma=A_f`, the normal coordinate is

`h = delta Gamma - D A_f[u]`.

The collision quadratic form is

`(1/2) integral h^2/A_f`.

Thus a tangent with `delta Gamma=D A_f[u]` has zero collision cost, exactly as required.  The manuscript also records the general direct differentiation formula

`ell(q)a^2 + 2q log(q) a k + q(1+log q) k^2`

before second-order chart corrections.  A positive exponential chart and the closed-range right inverse impose the nonlinear balance exactly and prove the matching upper bound.

The Gaussian process is constructed from B2 cumulants before the Mosco theorem; the inverse quadratic form is then identified with that already constructed covariance.  The positive CLT and cotangent conclusions are retained.
