# Multiscale proof input map

## Source-level dependencies

- `core/20_cumulative_returns.tex`: exponential tail for the collision time of the nth actual return. Backward clocks have the same marginal law by actual-return invariance; no independence of the two clocks is used.
- `core/28_marked_return_band.tex`: exact recentering at the mark and the conventions for zero-length backward/forward intervals.
- `core/30_unsmoothed_moments.tex`: fourth moments, deterministic maxima, quadratic insertion conventions, and the actual covariance/Cesaro identity.
- `core/46_finite_order_damping.tex`: every fixed finite collision cumulant, the finite spectral jet, and smoothed real-frequency damping. The mixed anchored cumulant extension is proved in file 50, not assumed as induced mixing.
- `core/48_damped_unsmoothing.tex`: fixed even maximal moments, higher-moment clock tails, and the cubic residual expansion with separate coarse/fine scales.
- `core/49_wider_fixed_count_band.tex`: the precise marked measure normalization, finite-record admissibility, and exact weighted count-localized raw decomposition.

## New deductions

For a fixed desired moment q, select a fixed integer p with 2p>3q/2. Holder's inequality on a deviation shell L yields n^(p-q/2) L^(3q/2-2p). At L~sqrt(n) this is n^(q/4), and the remaining moderate shells form a convergent geometric series. Exponential far shells justify summation to infinity. At q=2 the choice p=2 suffices. No optional-stopping theorem or martingale model is invoked.

For a fixed moment d, cumulants with one centered collision-state mark are absolutely summable over their other anchored time indices. Their block in a moment partition contains at least one collision factor; other nonzero blocks contain at least two. The resulting parity losses are n^(-1/2) for odd degree and n^(-1) for even degree. Actual stopping costs M_a n^(-1/4).

The Fourier choice 67/1400 solves 1/4-5 epsilon=3/280. Every other coarse/fine error has strict slack; the degree-19 analytic remainder retains the factor delta^(-40). The new kernel is used in every local edge and residual term.

## Verification boundary

No new external continuum theorem is invoked. The finite tests check shell exponents and summability, partition identities, exact pathwise cyclic-word identities, raw Jacobians and kernel exponents. Finite cyclic rotations are not offered as mixing billiard models. The whole-circle, finite-cover, anisotropic-space and constructible-preparation inputs remain the inherited mathematical dependencies. The full raw complement and long-time density estimates are not established by these checks.
