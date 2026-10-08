# Independent specialist audit map: v45

No independent human audit is claimed. The inherited v44 specialist map is available in the immutable baseline. New checks are localized as follows.

1. Verify the exact internal Hessian `D_c A D_c`, the tridiagonal inverse estimate and the incidence cancellation in an endpoint derivative. Check the endpoints and the empty-matrix case m=1.
2. Check continuation on the full endpoint square when margins decrease as `epsilon q^(distance/4)`. In particular verify that collision states and flight clearance are uniformly Lipschitz in adjacent contact positions without an inverse-incidence loss.
3. Verify the product/determinant formula for the endpoint cross derivative, including its normalization by `4 pi R c`. Check that the log-determinant derivative sums with exponent `1/4`, yielding a collar of radius `r_* epsilon^3` and a relative, not merely absolute, density bound.
4. Check the convex closed level's total-turning coarea calculation and the lower mass comparison with the intrinsic local jump. Distinct physical word collars must be disjoint and preserve the original return index.
5. Verify the endpoint-strip spectral pairing and scalar continuity at parameter transitions. At a surviving resonance the amplitude is bounded by the product of two `O(d)` physical masses; a large strong norm at small d must not be used as that amplitude.
6. Check the quantifier order: endpoint width and interval fixed; band fixed; collision-count limit; envelope-band limit; then collar-width limit. No LLT rate for prescribed shrinking widths is assumed.
7. Check that the final pointwise source domination is uniform over bounded measurable weights and that the all-band convolution assertion applies only to the already-small protected critical part.
8. Keep the remaining unprotected boundary source, complete signed inverse and arithmetic residues distinct. The result does not certify the full raw endpoint.
