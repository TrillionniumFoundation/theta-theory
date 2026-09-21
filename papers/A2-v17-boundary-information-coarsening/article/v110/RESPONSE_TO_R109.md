# A2 revision 110 — response to the v109 referee

Controlling review: `review/a2-v109-independent-harsh-top4-2026-09-21`, commit `87b63e155dac402ec6a9d0a34f69ff0ba5363fdb`.
Reviewed mathematical source: `60999f38f745072d240909fe8c77aee5be2df69a`.
New principal: `article/v110/paper.tex`.
Preserved complete companions: `article/v109/paper.tex` and `article/v108/paper.tex`, with all inherited dependencies unchanged.

The revision addresses the natural optimization problem identified by the referee, rather than extending the old witness by another sufficient construction. No earlier theorem is withdrawn, and no inherited source is removed.

## R109.1 — Replace the loose witness by a sharp threshold

Theorem 1.1 gives the exact native answer for every d >= 2:

`k_min(d) = d + ceil((3 + sqrt(16d+1))/2)`.

Equivalently, generic recovery occurs exactly when `binom(k-d+1,2) >= 2k-1`. This improves `3d+2` to `d+2 sqrt(d)+O(1)`, with the optimal leading constant and exact integer correction.

The proof has five distinct ingredients: exact normal-block fibres; native score interpolation; the positive loading submersion (Lemma 4.1); the classical rational maximal-rank theorem (Proposition 4.3); and generic global separation (Lemma 4.2). The rational maximal-rank input is expressly attributed to Ballico–Ellia, not presented as a new proof of classical postulation. Its use of restriction of quadrics is spelled out, including real descent and the embedding range c >= 4. In the native theorem the inequality forces c >= 5.

The monomial problem is separated, not silently identified with the general-subspace problem. Proposition 5.1 improves the raw pair-count lower bound by one for restricted additive bases, using the forced collision `0+n=1+(n-1)`. At (d,k)=(3,8) and (5,11), the exact native optimum is therefore impossible for every monomial normal space. Proposition 5.2 gives an elementary restricted basis with at most `2 sqrt(2n)+O(1)` elements. The referee's two smaller witnesses are reproduced and checked. The complete old `3d+2` construction is retained in Appendix B and in its unmodified full companion.

## R109.2 — Genericity and failure geometry

Lemma 4.1 characterizes the locally realizable Grassmannian image exactly by `J U^perp` containing a strictly positive vector. The map is a submersion, not merely a map meeting one witness neighbourhood: on each sign chamber, `A -> diag(Ae1) A` is a diffeomorphism onto frames with positive first column. This establishes the generic native assertion at the sharp threshold.

Section 6 treats the failure locus as the determinantal scheme of the tautological multiplication map. Proposition 6.1 gives its projective incidence description, its kernel-to-cokernel differential, the tangent space to its defining minor scheme, and a stated sufficient transversality condition for smooth expected codimension. Rank strata give exact partial-recovery fibre dimensions.

Proposition 6.2 exhibits an irreducible base-point subvariety of codimension c-1, lying in corank at least two, and proves that it meets every native realizable family by placing its real base point beyond the roots. This also explains why importing generic-matrix codimensions would be wrong in some parameter ranges. Theorem 6.3 proves local linear conditioning versus distance at transverse corank-one points, and an upper distance bound generally. These statements do not assume that every point is transverse or every minor ideal is reduced.

A classification of all irreducible components, or a dimension-free random-design condition-number estimate, is not claimed. The report presents those as stronger desirable directions; the revision supplies a sharp generic recovery theorem, an exact incidence/tangent description, and an explicit native degeneracy family rather than inventing such a classification.

## R109.3 — Begin with the actual categorical observations

Theorem 8.1 begins with empirical four-cell frequencies at the original clocks. A clipped linear mixture estimator yields an explicit nonasymptotic bound for the native moment coordinates and the induced normal Hessian blocks. It remains valid when the mixing probabilities are coupled by the original polynomial model. It does not replace the original model by independent unknown clock probabilities.

The role of exposures is now explicit. In the fixed-count experiment, exposures are known design weights, and geometrically varying them does not create new unknown likelihood coordinates. Theorem 8.2 separately specifies a Poissonized exposure protocol in which the group counts themselves are observed. Its conditional mark laws are the original calibrated laws; it gives O(N^-1) squared risk on an open full-dimensional moment image. In the known-mark-law subexperiment, the covariance formula and the ordinary local asymptotic efficiency statement are derived from the Poisson information.

Theorem 8.3 then propagates raw-sample estimation through finitely many computed contact values. Its bound is `2K/N + 2 C^2 h^4/gamma^2`, with `h_N=o(N^-1/4)` for root-N equivalence at a fixed informative design. It also states the joint scaling as gamma degenerates and the allowed numerical contact-computation error. These are correlated plug-in contact readings; their covariance is not replaced by independent Gaussian noise. Direct metric estimation is acknowledged to be simpler when the fitted model is retained.

The v109 independent Gaussian-contact theorem remains, with its exact-mean fit and its own `1/(N h^4)` scaling, in Appendix A and the full v109 companion. It is no longer offered as a substitute for raw-sample inference.

## R109.4 — Broaden the information-family theorem or sharpen Hankel

Both routes are addressed. The Hankel threshold is exact. In addition, Theorem 7.1 transfers the maximal Grassmannian compression rank of any fixed linear matrix family to generic positive globally valid synchronized loadings. For the diagonal family it proves the exact condition `binom(c+1,2)>=k`, with a constructive outer-product basis and the corresponding integer threshold. Independent Bernoulli log-odds coordinates provide a native diagonal information model. Arbitrary linear families are not falsely asserted to arise from the square-clock experiment.

## R109.5 — Literature and novelty accounting

The introduction and bibliography now distinguish rational-curve maximal rank (Ballico–Ellia), binary-form product spaces and Gram spectrahedra (Scheiderer), finite and restricted additive 2-bases (Yu and Kohonen), structured Hankel duality (Mourrain–Pan), classical discriminants (GKZ), and regular statistical asymptotics (van der Vaart). The contribution claimed is the positive native realization and generic global transfer, its sharp threshold and monomial separation, the native degeneracy geometry, and the explicit raw-sample/contact pipeline. Classical maximal rank and regular LAN are not rebranded as new principles.

## R109.6 — Immutable source and actual execution evidence

The mathematical source is committed before the execution receipt. The principal has no generated TeX inputs. Its exact Git blob is compared with the locally compiled bytes. The new verifier checks every principal input against a Git source commit and verifies that the entire diff from the review consists only of new v110 paths, its index and workflow. In full mode it runs the inherited v109 verifier, thereby rebuilding both complete companions and replaying their diagnostics, then runs the independent v109 referee checks and the new v110 exact diagnostics. Only a fully successful run can write `evidence/verification.json`.

A local-only build writes `local-verification.json`, explicitly marking the narrower scope and no Git-checkout binding. A separately committed binding receipt can record the remote-confirmed principal blob and source SHA without claiming execution of unbuilt companions. Workflow existence, a queued run, or a verifier script is never reported as a passed three-volume replay. The evidence receipt, not this response letter, is authoritative for the execution scope achieved in this revision.

## Proof-level requests and preservation

The exact fibre now has a basis-free formulation. Global separation and transfer to the global distance have their own lemma. The dimension inequality is solved exactly. The nonorthogonal `K G^{-1} K` identity is retained and checked independently. Positive targets, compact convex parameter regions and norm choices remain visible. One contact is explicitly a full normal block, not one scalar sample. The complete-conormal, reciprocal-budget, exact-query, endpoint-QE and local-root-reduction statements retain their original scopes in the appendices, with all complete historical proofs unchanged in the two companions.

Finite checks verify specified identities and rational loading examples. They are not claimed to prove the all-dimensional theorem or to predict a journal decision.
