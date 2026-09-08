# C1 Author Response — Round Twenty

The hidden-state model is now fully typed.  A controlled hidden transition
`M(x,dx')` is followed by an observation kernel `G(x',dy)`, and the belief
update conditions the new state.  Atomic, lattice, and continuous observation
coordinates are placed on one stratified reference measure (counting measure
on zero-dimensional/lattice strata and smooth volume on continuous strata),
so finite-volume atomic data are not artificially smoothed.

The reachable regular chart explicitly includes a fixed hidden reference
measure `m0`.  Common state and observation domination, evidence bounds,
Sobolev observation regularity, parameter derivatives, tail control, and
compact forward invariance are derived from the A2/B1/B2/B4 inputs on the
prepared finite-horizon class.  Beliefs outside that reachable class are not
silently assumed dominated.  Zero evidence is handled by one isolated,
absorbing cemetery belief; no projective direction is assigned to the zero
measure.

The posterior kernel is proved Feller by splitting positive and small evidence
sets.  The relaxed action correspondence, timing, measurable graph,
continuity of the exponential reward, and measurable selectors are stated and
verified in the risk-sensitive DPP.  Finite coordinates are selected on one
forward-invariant reachable compact set, and their value error is controlled
by a finite-horizon continuity recursion rather than an unproved Bellman
contraction.

The statistical section now proves a uniform triangular-array log-likelihood
expansion directly.  A third-order remainder is summed at the effective
information scale, the score martingale and information are controlled
uniformly over the compact strategy class, and contiguity follows.  Separate
likelihood-ratio tests, prior denominator bounds, and posterior contraction
precede the strategy-uniform Bernstein--von Mises theorem.  QMD plus a score
CLT is no longer treated as sufficient by itself.
