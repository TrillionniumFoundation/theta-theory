# Derivation map — Revision 94

Theorem spectralvalue94 evaluates all initial spectra for the fixed biased experiment. Lemma secular94 proves continuity, concavity and strict Schur concavity of the secular function. Lemma spectralleaf94 optimizes arbitrary rank-constrained fresh Grams, with an explicit singular-support reduction. Lemma spectralroof94 evaluates the rank-capped envelope for any continuous symmetric concave spectral objective. Corollary messagevalue94 supplies a necessary and sufficient strict-feedback criterion, with a two-outcome normalized example. Corollary spectralsaturation94 gives exact spectral loss and initial-rank saturation. All inherited equal-prior, general variational and local geometric results remain active with unchanged statements.

1. The biased payoff has only equal-label positive gain; its branch objective is the negative mass of a filtered swap.
2. Fix A and rank(B)<=ell. Compress B to supp(A), write Z=sqrt(A) B sqrt(A), and use tr(A^-1 Z)=1. Rearrangement and normalization put Z on leading A-eigenspaces without lowering its spectral objective or increasing rank.
3. The commuting objective is a Rayleigh quotient for vv* - diag(a), whose positive eigenvalue is chi. Its eigenvector gives b_i proportional to a_i/(a_i+chi)^2.
4. Positive superlevel sets of chi are convex because sum a_i/(a_i+c) is concave. Homogeneity upgrades this to concavity; strict scalar concavity gives strict Schur monotonicity.
5. A rank-r atom decomposition has lambda(rho) majorized by its averaged ordered spectrum. The least rank-r majorant q minimizes concentration, so Jensen gives an upper chi(q). A convex hull of permutations supplies commuting atoms all with spectrum q, at most d of them.
6. The common Gram sum and superadditivity give the full fixed-initial protocol upper. The support inverse constructs its attaining receiver instrument; fresh states are prepared independently given the record.
7. With no receiver message only the leading r spectrum is available. It is strictly smaller than q precisely when 2<=r<rank(rho), at nonzero t. The explicit d=3 instrument verifies attainability without postselection.
8. The majorants become strictly less concentrated until r reaches the initial rank and then stabilize. This yields exact saturation and exact loss from the optimized rank-r benchmark.

Each step is written as an all-matrix argument in the manuscript. Exact fixtures and rational enclosures validate the implementation only.
