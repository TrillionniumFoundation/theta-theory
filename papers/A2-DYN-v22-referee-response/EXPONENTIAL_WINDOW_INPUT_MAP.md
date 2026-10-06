# Exponential finite-record and return-window input map

## Primary source checked

S. Basu, R. Pollack and M.-F. Roy, *An asymptotically tight bound on the number of semi-algebraically connected components of realizable sign conditions*, Combinatorica 29 (2009), 523--546; DOI `10.1007/s00493-009-2357-x`; arXiv `math/0603256v3` (14 July 2009). The paper is already cited as `BPR` in the inherited bibliography.

The input is the **finite bound in Section 3.2, equation (3.3), printed page 5**, with zeroth Betti number and the full ambient real space. It bounds the sum of component counts by

`d (2d-1)^(k-1) sum_{j=0}^k binom(s,j) 4^j`.

The new proof uses `sum binom(s,j)4^j <= 5^s`. Both `k` and `s` in the actual lifted collision graph are bounded by constants times `L+1`, and `d` is fixed. The resulting bound is `C exp(C L)`. This uses no fixed-dimension asymptotic in `s` and no unspecified dependence on dimension. No new bibliographic item is needed.

## Hypotheses and geometry checked in the source

The full first-admissible-flight graph in `lem:finite-record-variation` has bounded-degree polynomial constraints, linearly many variables/tests and exponentially many disk-label alternatives. Exact moving-section membership adds only a bounded number of tests per collision. A fixed coordinate and a superlevel add only a bounded number. Coordinates of the moving rectangles enter as real coefficients, which the finite bound allows uniformly.

Coordinate projection maps each connected component to a connected set. Summing the component counts before projection therefore bounds the interval components of a slice superlevel without elimination of quantifiers. One-dimensional coarea and integration of slices give first distributional variation, including word jumps. A fixed angular atlas, bounded coordinate changes and a Lipschitz extension of a smooth function from the embedded cylinder give the smooth-composition bound.

This is **first variation in the initial collision coordinates**, not a count of inverse-coarea density singularities or a bound for their second derivatives. The finite raw extraction of v18 is retained separately.

## New deductions in the article

1. The exact peripheral lift and its top/height normalizations are unchanged. Finite-age regularization has the same L1/L2 errors, but variation `C M exp(C L)(1+epsilon^(-1)+|z|)`. Taking logarithms now costs one logarithm of the accuracy and norm budget rather than an additional log-log factor.
2. The original joint collision defect theorem then gives actual-return circle and complex-function estimates under `rho^2[1+log(H/rho)] <= a`. The complex accuracy is chosen first; the proof explicitly absorbs `epsilon_0[1+|log epsilon_0|]`. It does not divide by a pointwise modulus or by the shifted spatial frequency.
3. The exact grid reconstruction and orthogonal residual identity are reused to sharpen the finite-rank resolvent. The finite-time comparison retains the original characteristic function with its negative Fourier sign. These statements do not give full-circle uncompressed power decay.
4. A multiple-return observation product is first smoothed factor by factor in the original section measure. Invariance controls the error before a collision cutoff is imposed. A binary membership partition then fixes all observation collision indices on each word; the exponential finite-record bound controls the entire approximant's variation.
5. The inherited marked central and moment theorems apply only after this variation bound is supplied. L1 approximation and the actual fourth-moment bound remove the approximation. The final event and denominator are unchanged.
6. The existing raw finite extraction can be applied to these same weights when they additionally satisfy its subanalytic hypothesis. Arbitrary BV functions are not asserted to satisfy that hypothesis.

The sharp binomial estimate and the algebraic, window and projection diagnostics are finite checks. They do not independently certify the underlying collision-space construction, full raw derivative growth or complementary-integral estimates.
