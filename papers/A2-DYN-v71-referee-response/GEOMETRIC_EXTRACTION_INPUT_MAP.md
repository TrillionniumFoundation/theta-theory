# Geometric raw extraction: input and output map

## Inputs

The fixed triangular family has radii in `[0.45,0.47]`, minimum flight length `3/50`, a uniform finite horizon, collision probability `(4 pi)^(-1) d alpha d p`, and the exact rectangle section of the inherited article. Existing inputs are the exact action identity, invariance of the collision and return measures, mean-preserving BV smoothing, and the cumulative return-count tail.

The one-collision differential is checked against Stenlund--Young--Zhang, *Dispersing billiards with moving scatterers*, Comm. Math. Phys. 322 (2013), 909--955, arXiv:1210.0011v4, Section 3.1. Only its fixed-table differential is used, not its nonstationary mixing theorem. The arc-length/angle differential is converted to `(alpha,p)` explicitly. The converted determinant is one.

## New arguments

1. Positive matrix products preserve the ratio bound `A_m/B_m <= 53/6`. The action identity gives `|grad L_m| >= c|p|` and an explicit vector field transverse to the roof levels.
2. Every candidate tangency is cut off, including nonselected disks. Rational angle charts make each discriminant numerator degree at most eight. The elementary interpolation/Fubini lemma gives the uniform sublevel exponent `1/16`.
3. An orbit product of cutoffs loses at most `C(L+1)epsilon^(1/16)` in source mass by invariance. Fixed-order derivatives grow at most `exp(C(L+1)log(C/epsilon))`.
4. Mark smoothing occurs before actual-return composition. Exact itinerary indicators become locally constant on the regularized source. Pushforward derivatives are source divergences; summing disjoint source integrals avoids an itinerary-count factor.
5. The residual has an explicit all-label second-derivative budget. A fixed-label interval transform costs only a logarithm when replacing the residual by the full law over a finite roof band.

## Outputs and boundaries

Theorem V provides an exact geometric decomposition and arbitrary polynomial-accuracy microscopic interval inversion with `log B_n=O(n log n)`. It does not estimate the original jet residual, the pointwise extracted density, the finite complementary integral, the Gaussian microscopic denominator, or relative replacement of a microscopic physical event. Those distinctions are recorded next to the final raw identity.
