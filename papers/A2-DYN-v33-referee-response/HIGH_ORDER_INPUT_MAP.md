# High-order and separate-width input map

## Fixed-order partition estimate

`lem:all-small-mass-moments` uses the inherited `lem:small-mass-cumulants` and the exact moment-partition identity at a fixed order 2P. A partition with b nonsingleton blocks contributes `(m delta)^b L_delta^(2P-b)`. There is no theorem about factorial growth or analytic continuation of an unsmoothed twist. The finite algebra is consistent with the joint-cumulant convention in Döring--Jansen--Schubert, *Probability Surveys* 19 (2022), 185--270, DOI 10.1214/22-PS7, already cited as DJS. The general survey's all-orders assumptions are not imported.

## Heterogeneous factors

`lem:heterogeneous-cumulant-comparison` uses `lem:all-finite-product`, which is already multilinear. The proof compares every cross-gap subset moment, writes the product-difference telescoping identity in full, and cancels the independent-block cumulant. The worked centered four-factor example covers a centered section mark. Anchored exponential diameter summability follows at each fixed order.

## Operator word

`thm:high-order-damped-unsmoothing` uses `lem:bv-smoothing`, the smooth multiplier bound in `lem:collision-spectral-input`, and `cor:finite-jet-damping`. The latter inherits the Demers--Zhang local collision-space construction and the explicit finite spectral jet. The source conventions remain in `COLLISION_INPUT_MAP.md` and the norm appendix. At most 2P multipliers and 2P+1 powers occur; their number is independent of m. Multiplying their damping factors is legitimate because the nonnegative power lengths sum to m. The product of power-bound constants is included in the fixed-order constant. The fine residual is not made into a twist.

The concrete choice is P=16, residual degree 31, spectral degree Q=29. Thus 32 smooth multipliers can occur. This does not require derivatives of the coarse eigenvalue through order 32: the moment and spectral estimates have different inputs and independent fixed orders.

## Actual count and mark

`thm:anisotropic-fixed-count-band` uses the actual-return recentering and `eq:quarter-characteristic-stopping`. Its error integrates as `M_a n^(-1/4+Theta+theta_*)`. It concerns a prescribed k uniformly in k, not a random choice of mark or a maximum over marks. The deterministic collision length is `n/c*+O(1)`.

## Raw geometry and normalization

The coordinatewise kernel is the product inverse of a fixed smooth compactly supported one-dimensional cutoff. At small physical frequencies its torus inverse equals the restricted Euclidean integral, evaluated at integer lattice/count coordinates. The high-count support is separated in the third coordinate; its scale is not the larger fourth, roof coordinate. No replacement of the discrete measure is used. The finite extraction and raw residual inverse are the inherited `thm:finite-count-raw-extraction` and count-localized identities. They remain qualitative at each fixed packet until the explicit long-time terms are estimated.

## Verification boundary

The exact rational balances, fixed partition identities, chronology sums, and finite heterogeneous examples are executable checks. They are not continuum proofs of the collision norm construction, high-order decoupling, finite-count preparation, full complement, or relative event replacement. No additional external geometric theorem is introduced in revision 25.
