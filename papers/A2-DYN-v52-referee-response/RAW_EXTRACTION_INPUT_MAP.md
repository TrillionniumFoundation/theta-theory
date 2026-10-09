# Raw extraction: exact source and hypothesis map

## Added primary source

Raf Cluckers and Daniel J. Miller, *Stability under integration of sums of products of real globally subanalytic functions and their logarithms*, Duke Mathematical Journal 156 (2011), no. 2, 311--348, DOI `10.1215/00127094-2010-213`; inspected version `arXiv:0911.4373v1`.

The precise inputs are Definition 1.2 and Theorem 1.3 (constructible algebra and stability under parameterized Lebesgue integration), and Theorem 3.11 (cell preparation of constructible functions). In the inspected preprint these are on printed pages 3 and 15--16. The prepared terms have rational powers, nonnegative integral logarithmic powers and strong subanalytic units. These are qualitative finite-dimensional theorems, not a uniform long-time derivative estimate for a billiard.

## Application checks in the article

1. The original finite physical graph, including the first admissible hit and actual section membership at every collision, is supplied by `lem:finite-record-variation`. At fixed radius and cutoff it is semialgebraic in bounded rational charts, with finitely many words and labels. The count restriction is not a restriction to only regular critical words.
2. The initial chart density is semialgebraic. The weight is explicitly required to be bounded and globally subanalytic on each finite chart. The class includes the weight one and finite subanalytic observation conditions up to the nth actual return; arbitrary BV functions are not asserted to be subanalytic.
3. The cumulative time distribution is an integral of a globally subanalytic function over its full domain, with the exact inequality `total flight time < t`. Its integrability follows from boundedness and finite chart area. Theorem 1.3 therefore applies.
4. Absolute continuity is proved independently by the inherited regular-word coarea argument. The physical critical-point theorem `prop:general-edge` is retained and is not claimed as a new result. The actual section normalization is `1/(4 pi c*)`, not the old section's constant.
5. One-variable differentiation of the constructible representation is justified after a finite analytic partition, using the product rule and definability of derivatives of the subanalytic generators. No unverified higher-dimensional differentiation theorem is used.
6. The one-variable specialization of preparation gives convergent Puiseux-log germs. The proof also explains this directly from the Puiseux germs of the finitely many subanalytic generators. Thus the first two derivatives of the remainder are estimated from convergent analytic representations, not by differentiating an arbitrary asymptotic equality.
7. Integrability removes all combined exponents at most minus one. Subtracting every remaining exponent at most one removes divergent second derivatives and the value/slope boundary distributions. A C2 piecewise-polynomial cutoff is sufficient; no nonzero compactly supported analytic cutoff is assumed.
8. The sum is finite for each actual count restriction. Its derivative budget is expressed in terms of its actual germ coefficients, radii and regular-interval derivatives. Neither this source nor compactness of the physical parameter interval gives a growth bound for that sum as n and L increase.

## What is proved without another external input

Trace cancellation, membership of the residual in `W^{2,1}`, the mixed Fourier `L1` and far-roof estimates, exact count-fiber agreement, and the corrected central inversion identity are proved in the new sections. The existing cumulative-return tail gives an additional finite-band cutoff bound. The rapid central count-convolution bound needs only the count support separation and the Schwartz kernel, not an extra stochastic independence or mixing assumption.

The finite diagnostics test power/log formulas and exact algebraic identities. They do not verify the continuum integration/preparation theorem or quantitatively bound every physical germ.
