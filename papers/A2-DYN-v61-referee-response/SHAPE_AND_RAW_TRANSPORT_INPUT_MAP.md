# Inputs for revision 26

The revision imports no new continuum theorem. All new arguments are proved in full in the two new core modules, from the frozen v25 inputs below.

## Shape-adaptive fixed-count estimate

`eq:quarter-characteristic-stopping` supplies the pointwise actual-mark stopping cost `C M_a |v| n^(-1/4)`. `thm:high-order-damped-unsmoothing`, together with `cor:finite-jet-damping`, supplies the deterministic collision estimate. The coarse scale is `n^(-19/100)/4`; residual half-order is fixed at 26 (Taylor degree 51), spectral degree at 29, fine scale at `n^(-32)/4`. There are at most 52 multipliers and 53 collision powers; power lengths still sum to the deterministic interval. All 26 nonsingleton block counts remain.

The shape is controlled by its ordinary four-dimensional volume and first radial moment. The dyadic estimate is elementary: the number of nonnegative integer four-tuples with sum plus maximum equal to t is O((t+1)^3). The threshold is divided by log(2+n)^3 to pay this entire sum without altering the central exponent. This is not an application of an external mixed-smoothness approximation theorem, and no unproved uniformity over expansion orders or varying width exponents is used.

## Raw cutoff transport

`thm:finite-count-raw-extraction` supplies E+Q=mu^L and an integrable residual transform. `lem:central-count-support` localizes the original law exactly on count labels below L. The new identity R_chi-R_psi=(K_psi-K_chi)*mu^L follows by retaining cancellation between E and Q. The full-law difference is bounded by the new shape theorem plus the inherited isotropic and roof-box estimates. The high-count difference is bounded by the actual third-coordinate support gap and the dyadic kernel scale sum. It is not bounded by treating a small tail mass as a small raw density.

The theorem compares signed combined corrections. It does not bound an isolated edge correction, an absolute residual integral, or the actual long-time A_2. It applies only to the intersection of marked bounded-BV weights and finite-record admissible weights, with the same count, mark, weight, extraction and cutoff conventions throughout.
