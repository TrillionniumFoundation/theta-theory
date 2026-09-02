# Author response to Referee Round Twenty-Two — B1

The referee's normalization and covariance objections are accepted and have been incorporated as exact algebraic regression checks.

## B1.1 — canonical normalization

The active partition function is a moment generating function under a normalized exact-`N` canonical probability.  It equals one at zero source and zero centered multiplier, so its pressure is exactly zero there for every `N`.  When absolute free energy is discussed, the factor `N!/|T^3|^N` is displayed explicitly.  The divergent `-log N` ideal-gas term is therefore neither ignored nor called a finite pressure.

## B1.2 — product damping

Particles are first lifted to a labelled symmetric integral and divided into deterministic blocks of labels.  Blocks are exposed in lexicographic order.  A fixed finite partition of unity over full-rank position--velocity charts is expanded at each step, so every chart choice is adapted to the successive conditioning sigma-field.  No family of blocks is selected after observing the full configuration, and no frequency-independent exceptional remainder is left on the unbounded Fourier domain.

## B1.3 — push-forward regularity

Chart cutoffs are supported in the chart interior and vanish, with derivatives through the required order, at the boundary.  Coarea densities can therefore be extended by zero without boundary distributions.  The manuscript proves a uniform `W^{s,1}` norm for these extensions.

## B1.4 — mixed local covariance

The local theorem uses the full joint covariance matrix.  After conditioning on a lattice deviation `z`, the continuous Gaussian mean is shifted by

`Sigma_RZ Sigma_ZZ^{-1} z`

and its covariance is the Schur complement

`Sigma_RR - Sigma_RZ Sigma_ZZ^{-1} Sigma_ZR`.

These expressions are carried into source-inserted exact-number coefficient extraction.  Relative error is stated only for windows whose Gaussian mass dominates the absolute inversion error.

The positive exact-number and microcanonical transfer theorems are retained with the corrected normalization and covariance.
