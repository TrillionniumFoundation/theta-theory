# Response to the independent referee report on A2 revision 87

**Revision:** 88, 19 September 2026.  
**Controlling report:** `reviews/a2-v87-independent-harsh-top4-2026-09-19/REFEREE_REPORT.md`, commit `976d23ef269126e68dd90c4c9d3184ee67ff0b54`.  
**New branch:** `revision/a2-v88-projective-polynomial-rigidity-2026-09-19`.  
**Principal article:** `papers/A2-v17-boundary-information-coarsening/rigidity_v88.tex`, with source in `article/v88/`.  
**Title:** *Projective polynomial observations: normalization, spectrum, and singular inference*.

We thank the referee for distinguishing the mathematical coherence of revision 87 from the remaining questions of structural scope, intrinsic conditioning and literature position. The revision responds by proving a broader normalization theorem, replacing factorization optimization by an observable residue condition, and constructing a direct estimator. The affine results and the historical derivations have not been removed or weakened. The new article is self-contained; the unchanged historical companion is retained as an archive, not imposed as a prerequisite for reading the principal proofs.

## 1. Scope and the finite-clock principle (report §§2, 9, 14)

Theorem 1.1 now treats degree-d component polynomials rather than only an affine numerator with one common pole. The observations determine a linear normalization residual operator N_P. Its least singular value tau is defined with explicit coefficient and observation norms.

Lemma 2.1 proves, for full-rank channels and at least 2d+1 distinct clocks,

`ker N_P = { (q/g)s : deg s < deg g }`, where `g = gcd(f_1,...,f_k)`.

Thus the defect has an algebraic meaning: it is exactly the degree of the factor erased by projective normalization. At any design with at least d+1 clocks, full column rank of N_P is the relevant normalization certificate. Lemma 2.2 realizes a nonzero kernel by a positive, fixed-channel local exact fibre at interior parameters with internally simple roots. Proposition 2.3 proves that 2d+1 is sharp in the worst case for every fixed admissible capacity, while allowing better designs for richer curves.

The same theorem proves a one-sided aggregate-root modulus against the entire closed competitor model. The loss is additive in `kappa^{-1}+tau^{-1}`: the normalization error remains diagonal after reduction by the true channel inverses. It has exponent 1/d uniformly, and exponent one when roots within each component polynomial are separated. Cross-component collisions are allowed. Degree one recovers the earlier gap-free action theorem without an additional separation assumption. We do not call the 1/d exponent optimal on every real-rooted stratum.

## 2. A structural observable condition (report §§4, 12.2)

Theorem 3.2 supplies a replacement for the fibre maximum. After the pole and the observable coefficients A,C have been recovered, form the reduced pencil M(z)=zA_0-C_0 in orthonormal observed row and column frames. For every distinct action x, take the residue R_x of M(z)^{-1} and define

`beta(P) = sum_x ||R_x||_op`,  `eta(P) = (beta(P) + ||B||_F^{-1})^{-1}`.

This is independent of the frames and of the latent factorization, including at repeated actions. The theorem establishes:

- positivity exactly when `rank P_1=k` and `P_2 != P_3`, equivalently when the old envelope is positive;
- `1/sigma_k(A) <= beta <= k/(alpha_* kappa)` and `eta >= c theta_*`;
- the stronger one-sided Lipschitz inverse with eta in the denominator;
- lower semicontinuity of beta, upper semicontinuity of eta, continuity on fixed multiplicity strata, and vanishing at rank-loss or constant-curve boundary limits.

The proof first applies the exact two-clock pole-shift fibre to the true pencil, and only then uses the resolvent. This avoids multiplying the pole loss by the spectral condition. Remark 3.3 gives an explicit collision with beta changing from 9 to 6; global continuity of eta would be false. The old envelope theta_* is retained and proved upper semicontinuous by compactness. No unsupported equality with a metric slope or distance to a discriminant is asserted.

## 3. Perturbation predecessors (report §§3, 11)

The introduction now distinguishes rational interpolation, coefficient perturbation, normalization recovery, factor recovery, and multiset recovery. It directly discusses Chu (1987, 2003), Higham--Mackey--Tisseur (2006), Tisseur--Higham (2001), Su--Bai (2011), Van Barel--Bultheel (1990), and Bhaskara--Charikar--Vijayaraghavan (2014), in addition to the retained references.

We explicitly credit the classical resolvent exclusion and cluster-counting mechanism; it is not presented as a new theorem about generalized eigenvalues merely because repeated actions are allowed. The additional assertions are the observable normalization defect, its positive fibres, the additive observation-to-coefficient conversion, and the projective pole-shift/residue estimate. `LITERATURE_AUDIT.md` records the exact comparison and the source-verification scope. It does not claim an exhaustive priority certificate.

## 4. Exact-fibre uniqueness and root matching (report §§6, 7, 12.1)

Proposition 3.4 now starts with the missing rank implication. The observable leading coefficient A has rank k, so every alternative exact factorization `A=U' diag(alpha') V'^T` has two full-column-rank channels. Only after this step is spectral factor reconstruction applied. Equality of theta_* with theta on the simple-spectrum lower-bound families is justified by this exact-fibre argument.

Lemma 2.4 replaces the compressed matching proof by a detailed argument: nonexceptional inflated disk radii, contours uniformly free of roots along the whole homotopy, preservation of algebraic root counts, matching within each component, and a finite-permutation limiting argument. It does not replace multiset matching by a mere Hausdorff bound.

## 5. A direct estimator (report §8)

Theorem 4.1 gives an explicit procedure: solve the observed least-squares normalization equation, clear and interpolate the observations, reduce in the leading singular subspaces of the first observed matrix, and solve a regular matrix-polynomial eigenvalue problem. In the affine case it attains the stronger eta modulus. No latent factor search, parameter net, or supplied signal floor is required for this point estimator.

`verification/reconstruct_v88.py` implements this procedure and reports numerical deficiency rather than silently assuming regularity. The arithmetic theorem is not a uniform bit-complexity theorem. The residual confidence region remains an information-theoretic optimization; the article now separates that issue from constructive point estimation.

## 6. Sharpness and statistical details (report §§5, 12.3--12.6)

Theorem 5.4 retains the old sharp signal-class statement and additionally proves the same minimax order for the observable eta classes. Both least-favourable families remain in the principal article, with their exact identities: arbitrary-rank product singularities with both marginals fixed, and full-spectrum collapse with fixed well-conditioned channels. Lemma 5.3 chooses their positivity floor, displacement interval, contrast bounds and comparison constants together. The class proof then fixes M, sets the product contrast to Ms, and restricts s_* before selecting the testing displacement.

The adaptive experiment is formally specified by parameter-independent conditional clock kernels and one subsequent categorical draw. The entropy bound is for the complete transcript, including clock choices and external randomization.

The empty-confidence-set convention is stated in Theorem 5.2 itself. Fixed-dimension, interval, clock and weight-floor dependencies are adjacent to Theorem 1.1 and repeated at Theorem 3.2. The class and pathwise sharpness claims are not expanded into an unproved classification of every local directional modulus.

## 7. Submission boundary and preservation (report §10)

The principal article contains every proof it needs. The revised affine fibre, modulus, factor reconstruction, confidence construction, product family, collapse family, adaptive lower bound, binary determinant implication and logarithmic observation law are all present. The shared spatial, other detector, and geometric regimes retain their original assumptions in the unchanged repository archive. The revision adds new paths only; it does not overwrite a report or historical manuscript. `PRESERVATION_AND_SUBMISSION_BOUNDARY.md` supplies the correspondence and exact baseline.

## 8. Reproducibility and next review (report §13)

The local native build produces a 16-page article with no unresolved references, unresolved citations, multiply defined labels or overfull boxes. Exact symbolic checks cover the affine gauge and normalization kernels in degrees one through three, plus a nontrivial four-clock quadratic fibre. Numerical diagnostics cover reconstruction with partial collisions, internal repeated roots, rectangular channels, residue identities, and the two least-favourable families.

Source hashes, compiler information and the actual local records are provided separately. The local result is not represented as a completed GitHub Actions run. The branch workflow reruns the diagnostics, checks additive preservation against the controlling report commit, compiles the article, and records its own source-pinned evidence. Neither finite diagnostics nor a successful build is formal proof certification or a prediction of editorial acceptance. The new proofs and their precise novelty comparison are submitted for independent mathematical review.
