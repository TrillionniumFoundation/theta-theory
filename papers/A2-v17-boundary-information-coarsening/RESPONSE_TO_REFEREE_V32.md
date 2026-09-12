# Author response to the independent A2 v31 referee-style report

**Article:** *Boundary laws, intrinsic periodic rigidity, and global physical reconstruction in dispersing billiards*  
**Revision:** A2 v32, September 12, 2026  
**Review:** `reviews/a2-v31-external-harsh-top4-2026-09-12/REFEREE_REPORT.md` at `9edd5f48d91b74d09718149de6e2c3550c375f20`  
**Reviewed manuscript:** `e1f6304f6069869ac323e7d1a634a619faa4bc32`  
**Mathematical revision:** `35fd4ccef1b5785692de512635f7240a4df0d641`

We thank the referee for separating the mathematical integration from the unresolved verification requirement. We preserve the article's geometric scope, observation spaces, complete auxiliary proofs and prior corrections. The response does not treat a finite diagnostic, source inventory or unexecuted workflow as a full native build.

## E1. State the convergence mode and remove revision-era mathematical prose

**Response: a stronger, explicitly proved compact-experiment statement is now active.** We did not change “uniformly on compact parameter sets” into a finite-parameter-only conclusion.

The new section `article/18a1_compact_experiments_v32.tex` contains:

- `lem:v32-finite-net`: finite-subexperiment convergence plus asymptotic uniform total-variation continuity implies compact-indexed two-sided Le Cam convergence. The proof fixes a finite net before taking the sample-size limit and uses one parameter-independent kernel in each direction. Net selection is an error estimate, not unknown-parameter information passed to a simulator.
- `thm:v32-compact-vector`: the existing support-stability estimate yields a product Hellinger modulus bounded by `C s^2(1+log(1/s))`. Gaussian continuity and the finite-net lemma prove the compact conclusion for the original moving-support family. Singular information is handled on its identifiable range, including the zero-dimensional case.
- `cor:v32-compact-fixed-window`: independent batches, the historical exact/ideal reduction, common reference caps and the stopped comparison transfer this stronger conclusion to the declared physical endpoint-output experiment.

The active count chapter is `article/18d_count_endpoint_multirate_v32.tex`. It preserves the stable labels of the predecessor, which remains present but is no longer input by the main. The revised `thm:v23-count-endpoint-joint` explicitly asserts `Delta(E_boundary,K,G_K)->0` and `Delta(E_finite,K,G_K)->0` for every fixed compact local set. The information remains `1 direct-sum K_H`, and the original fast, slow and gap scales are unchanged.

The proof does not infer this assertion merely from joint LAN. It supplies an exact geometric-waiting Hellinger bound, compares the true negative-binomial batches to the ideal count-only family, proves compact convergence of that family, and independently removes the fast displacement from the endpoint factor. Uniform compact convergence of the endpoint factor follows from the new corollary. Product comparison precedes the cap correction, and the success-weighted stopped finite-bridge error is then added. Mixed fast/slow Taylor terms are explicitly controlled in the count-score lemma.

The chapter no longer calls a matrix “the v22 matrix” or an experiment “the v22 experiment.” Scientific prose uses direct theorem and equation references. Historical filenames and stable labels remain for reproducibility.

No new geometric restriction is introduced to obtain this result. The anchored finite contact-jet model, fixed positive design, common regular collar, critical scale, even diverging flight sequence and rate conditions are the same hypotheses already used by the preceding theorem chain. Compact local equivalence is not presented as a uniform statement on the entire unbounded parameter space or the infinite-dimensional class of tables.

## I1. One current revision identity

**Response: corrected.** Both principal README entries now identify v32 and point to the active native main, this response, the preservation record and the execution record. The new branch descends from the actual v31 review head, not from the misleading old branch name discussed by the referee. The mathematical-source SHA and the full build-attempt SHA are distinguished rather than conflated.

The native main identifies revision 32 in its source and PDF metadata. It inputs the compact-experiment section and the revised count chapter. Its three scientific parts, companion reference, complete auxiliary compendium and bibliography remain active. Previous entry files are preserved by exact Git blob.

## C2. Complete native-main and companion verification

**Response: not claimed closed by a source commit or isolated test.** `VERIFICATION_V32.md` is the execution record. It separates actual local diagnostics, the isolated changed-section syntax check, the build-utility regression, and the complete native workflow.

The complete workflow archives the full immutable manuscript tree before installing TeX, runs the inherited and new finite diagnostics, audits the literal native source graphs, and invokes the builder on both `two_collision.tex` and `main.tex`. The builder now preserves available PDF/log/auxiliary products even when LaTeX fails, attempts the main after a companion failure, and records commands, versions, source hashes, actual recorder inputs and per-entry status. Source graphics are not discarded merely because they have PDF extensions. This repairs an evidence-retention weakness in the old failure path, but is not itself a successful build.

The acceptance condition remains the referee's: executed complete native main and companion, resolved references and citations, retained logs and immutable product identities, followed by inspection of the complete PDFs. An unstarted hosted job, the five-page isolated fixture or a synthetic regression of the build utility does not meet that condition. The execution record is updated with the actual attempt rather than assuming it succeeds.

## Correct distinctions explicitly preserved

The same-parameter measurable physical coupling and its success-weighted stopped comparison are unchanged. They are not used as unknown-parameter reconstruction kernels. Common domination is not confused with domination by the reference member; endpoint likelihoods still use the common-collar representative. The count--endpoint theorem concerns its declared coarsening, not complete raw histories. Caps are added after exact uncapped factorization, and all preparations remain charged.

The four-density signed inverse, transported-anchor off-model stability, common-orientation quotient, observed-contact qualification in the position/scalar comparison, charged pilot and onset coordinate, analytic finite-signature reconstruction, direct-position benchmark and smooth-envelope caveat remain in place. The finite-net lemma and the geometric-waiting bound are elementary supporting arguments, not claims of a new general statistical principle. The article's main geometric significance remains the relative nonlinear boundary law and the all-order unsymmetrized contact inverse with their intrinsic reconstruction consequences.

The present changes address a precise proof and integration request. They are neither an unrelated expansion of the programme nor a claim that all inherited proofs have been independently re-certified in this round. No manuscript or review source is deleted.
