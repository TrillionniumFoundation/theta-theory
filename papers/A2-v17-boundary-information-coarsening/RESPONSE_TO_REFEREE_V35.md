# Response to the external referee of A2 v33

Author revision v35 · September 13, 2026

We respond to `reviews/a2-v33-external-harsh-top4-2026-09-13/REFEREE_REPORT.md` at `d51c06689ba540711b2f890beb35eb235dba13e4`. The reviewed assembled source is `b577cffcb3ca5597cb4905269bea9de3bd4ead38`. We also retain the intervening author work at `127f9334f15c5fb12307bd691973d1eb44e499e8` (v34); it has not been represented as a newly reviewed submission. The complete active source is `main.tex` on the v35 branch. Its theorem statements and observation models are not weakened.

## R1 — local-alternative mean and quadratic-risk integrability

The requested calculation is inserted in place near the end of the proof of `thm:v22-vector-boundary-gaussian`, in `article/18a_vector_boundary_information_v26.tex`. It is not advertised as a new theorem.

Equation `eq:v35-one-mark-expansion` expands the successful-observation density on the common collar before division by the defining function. Integration against the reference score then gives `eq:v35-alternative-mean`:

\[
\mathbb E_{n,h}\Delta_n=np_n\delta_n\mathbb E_0[\mathsf S\mathbf1_{C_n}]
+np_n\delta_n^2\mathbb E_0[\mathsf S\mathsf S^t\mathbf1_{C_n}]h
+O_K(np_n\delta_n^3\log(1/q_n))
=\mathcal J_\Sigma h+o_K(1).
\]

The centering lemma makes the first term negligible; the logarithmic second-moment coefficient gives the middle limit; the remainder tends to zero at the stated rate. The proof then applies the independent-sum fourth-moment estimate to centered summands in `eq:v35-centered-fourth`, and only afterward restores the uniformly bounded mean. The three relevant collar-rate identities are displayed. This proves the required compact-uniform fourth moment and quadratic-risk uniform integrability without a higher-moment hypothesis on the product likelihood.

The text explicitly distinguishes a one-observation density-ratio bound from a product-likelihood bound. It also says that each excluded observation contributes zero while the remaining observations stay in the sum. The eight theorem/lemma statements of the chapter are unchanged. The v34 proof of normalized-likelihood tilting, contiguity and quadratic-risk convergence remains active as a separate retained derivation.

## M1, M2, M3 and E1 — preserve the repaired statements

The report closes M1, M2, M3 and E1 at their stated scope. We retain those repairs rather than reopening them or enlarging their claims. Finite likelihood-vector convergence and normalization give both finite-experiment kernels; compact convergence additionally uses the uniform moving-boundary Hellinger modulus and finite-net passage. The count--endpoint theorem continues to observe only the declared laboratory transverse endpoint pairs and the specified counts and stopping information. Normal coordinates, residual times and intermediate collisions are not silently appended. Common domination and domination by a designated reference member remain different assertions.

## I1 — current assembled identity and navigation

Both actual README entries have been replaced by v35 entries; this is not merely another historical copy. They link the active native manuscript, this response, preservation record and current verification document. The reviewed v33 SHA, latest referee SHA, unreviewed v34 predecessor and actual tested assembled source are distinguished. The old entries are retained as `README_PRE_V35.md` at their corresponding levels. The old active main and vector chapter are retained under `history/v34/` by exact blob.

## C2 — execution evidence, not a proposed command

The exact native companion `two_collision.tex` has been compiled locally without source alteration into a seven-page PDF. Its source blob, command, versions, full logs, PDF hash and visual-inspection coverage are recorded in `VERIFICATION_V35.md`. The ordinary and optimized R1 finite diagnostics were actually executed with identical output. The changed vector chapter also passed an isolated syntax check, with its genuinely external references unresolved; that check is not called the complete submission.

The v35 branch-specific workflow archives the complete immutable source and invokes the existing full-graph builder on both native entries, preserving actual logs even on failure. The current verification record gives the actual execution disposition. Neither this workflow definition nor the companion-only success is by itself claimed to close the complete-main requirement. Compilation evidence is kept distinct from mathematical validation and editorial acceptance.

## Preserved scope and significance

The relative boundary law, weighted nonlinear half-line construction, signed all-order contact inverse, single-offset density reconstruction, intrinsic gluing and lattice recovery, moving-ceiling kernels, calibrated physical reconstruction and same-experiment direct-position benchmark remain in the active manuscript. All 36 auxiliary modules remain active. Charged failures, common orientation versus pointwise folding, finite-order stability and the possible non-effectiveness of the compact estimator are retained.

The revision addresses the report through proof completion, coherent source identity and verifiable execution. It adds no unsupported priority claim, acceptance claim, counterexample, or artificial contraction of the mathematical programme. The current verification document states the remaining execution limitations, if any, separately from the scope of the theorems.
