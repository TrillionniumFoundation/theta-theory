# Proof ledger — A2 v38

## New finite-stencil statements

`lem:stencil-polytope`: finite killed compass transience follows from the
squared-displacement martingale. Flow conservation realizes every feasible
continuation measure by randomized stopping. Nonnegative Green multiplication
bounds each coordinate and the total mass. Linear-program duality and
transience give the attained dual and unique Bellman value.

`thm:finite-stencil`: every killed stopping payoff is bounded by occupation.
The target component is contained in the prior-bounded square, and its exit
lands at zero before the square exit. This supplies equality without knowing
the component and without imposing zero physical occupation on the square's
edge. Maximizing objectives gives a Green-weighted Lipschitz modulus for
arbitrary data vectors.

`cor:stencil-local-stability`: apply the same functional to two experiments
or two translated stencils. The errors are local, not whole-plane assumptions.

`thm:stencil-sampling`: estimate the 2M raw means with fresh batches, apply
Hoeffding and the fixed Green bound, and reserve half the error for a certified
rational primal--dual evaluation. The finite-state matrix is fixed independently
of the accuracy. This estimates occupation, not a discontinuous membership bit.

## New direction-free statements

`thm:general-command-rigidity`: pointwise reciprocal balance and independence
give the Poisson equation for a known bounded centered displacement law.
The trace second moment supplies a component exit-time bound even with singular
covariance. Positivity and support cancellation yield the full period group.

`lem:isotropic-perimeter`: directionwise collision strip area, Tonelli, and
Cauchy's perimeter formula give the isolated mean integral. Minkowski perimeter
addition turns its deficit into footprint perimeter. The normalization is t/pi,
not t/(2pi).

`thm:isotropic-registration`: ratios of positive perimeter deficits recover
scales. Centered support envelopes cancel the obstacle collection without a
matching. Support subtraction recovers the translated configurations. Equality
of all recovered configurations forces the stated period-shift gauge; coupling
translated densities proves sufficiency at the binary-law level.

## Preserved dependencies and scope

The complete v37 core tree `12a9e42058be2b228f6855e8fbf296ac97555d52` is
retained, with every file active. It contains the sharp Hellinger estimate,
stopped information argument, shrinking-layer upper controller, the full
translation ambiguity and all earlier reconstruction/calibration proofs.
The new work does not reclassify those results as conditional on a new lemma.

The finite-stencil proof assumes the positive component diameter bound and a
gap larger than a walk step. The general displacement theorem assumes zero
mean and positive trace variance. The isotropic footprint inverse assumes
labelled exactly homothetic supports and two distinct scales. No theorem here
asserts finite uniform crystallinity testing without a nonperiod margin.

Continuum proofs are in the TeX manuscript. The validator checks source and
finite algebra, not validity of every mathematical inference.
