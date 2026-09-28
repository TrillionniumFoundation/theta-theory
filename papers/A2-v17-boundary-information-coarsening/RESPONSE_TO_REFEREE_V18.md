# A2 v18 — point-by-point response to the 11 September 2026 referee report

**Revision branch:** `revision/a2-v18-integrated-boundary-information-2026-09-11`  
**Referee branch:** `review/a2-v17-independent-harsh-boundary-information-2026-09-11`  
**Reviewed author head:** `106836283ebe3fabee0479df8976d24f6dbe0bf6`  
**Referee report commit:** `d713b345ed58b8949cafa430954c5a82e1d159fd`

This revision treats the report as a mathematical and editorial audit, not as a request to weaken the established theorem chain.  No retained theorem is withdrawn merely to simplify the paper.  The revision instead (i) corrects the one genuine scope defect, (ii) rebuilds the active abstract/introduction around the common geometric–information mechanism, (iii) broadens the nonregular-support literature audit, and (iv) supplies a branch-specific native-build workflow.  The old v17 source files are retained in the repository for comparison; the active entry point selects the revised v18 front matter and boundary-information proof.

## C17-M1 — scope of support-exclusive negligibility

**Referee point.**  In `thm:v17-boundary-information`, the sentence asserting that support-exclusive observations are negligible was grammatically exposed to the `b=+infinity` regime, although the proof uses `np t^2 -> 0`, which follows only from a finite information scale.

**Revision.**  Corrected without weakening the supercritical theorem.  The active theorem now makes three scopes explicit:

1. the total-variation transition holds for `b in [0,+infinity]`;
2. the Gaussian log-likelihood statement is asserted for `0<b<+infinity`;
3. support-exclusive negligibility is asserted only for `b<+infinity`.

For `b=+infinity`, the manuscript now expressly states that no support-exclusivity conclusion is needed or claimed.  The proof of `TV -> 1` uses the multiplicative Hellinger affinity exactly as in v17.  Thus the strongest supercritical conclusion is preserved, while the false implication `np t^2 log(1/|t|)->infinity => np t^2->0` is nowhere used.

**Active source:** `papers/A2-v17-boundary-information-coarsening/article/18_boundary_information_v18.tex`.

## C17-E1 — significance and what is genuinely new

**Referee point.**  The v17 response risked presenting the logarithmic moving-boundary rate itself as the conceptual novelty, although the one-dimensional linearly vanishing moving-endpoint phenomenon is classical.  The report also asked what billiard-specific obstruction is actually solved.

**Revision.**  The active abstract and introduction no longer claim novelty for the existence of nonregular normal limits.  They organize the paper around a single mechanism:

`relative Jacobi determinant law -> residual-time integration -> linearly vanishing moving support -> intrinsic boundary information -> observation-dependent critical experiment`.

The revised text isolates four pieces that are proved here and are not attributed to the classical one-dimensional rate phenomenon:

- the invariant hypersurface coefficient
  `I_Sigma = integral_Sigma a_0 v^2/|grad w_0| d sigma`;
- the independently thinned simple-experiment limit with a retained failure atom;
- the exact determinant-one billiard whitening, which gives `I_Sigma=1` for unequal contact curvatures and either parity;
- the physical three-level observation hierarchy: complete records have the erasure scale `q_j`, endpoint-only records have the Gaussian scale `q_j^2 log(1/q_j)`, and success bits lose the tangent shape information exactly.

The central billiard-specific obstruction is now stated directly: **coarsening and the long-bridge limit do not commute at the level of the local experiment**.  Contracting the complete-record TV estimate does not recover the endpoint critical law.  The endpoint law has to be recomputed after physical residual-time integration, and the physical positive-offset transfer has to be controlled at the smaller `r_j` scale.

This is a sharpening of the mathematical thesis, not an assertion that an editorial threshold is mechanically satisfied.

**Active sources:** `main.tex`, `article/01_introduction_v18.tex`, `article/18_boundary_information_v18.tex`, retained `article/19_endpoint_critical.tex`.

## C17-E2 — nonregular moving-support literature

**Referee point.**  v17 only verified the official abstract of Smith (1985), which was too narrow a literature basis for an aggressive originality statement.

**Revision.**  The manuscript now positions the boundary-information theorem against a broader verified chain:

- M. Akahira (1975), two papers on location estimation in nonregular cases;
- I. A. Ibragimov and R. Z. Has'minskii, *Statistical Estimation: Asymptotic Theory*, including the classification of singularities;
- R. L. Smith (1985), explicitly identifying the linearly vanishing (`alpha=2`) moving-endpoint case as asymptotically normal at a different rate;
- K. Hirano and J. R. Porter (2003), parameter-dependent support treated through limits of experiments and local asymptotic minimax efficiency.

The revised introduction and boundary-information section make a negative priority statement: the paper **does not claim** priority for parameter-dependent support, the `alpha=2` rate change, or nonregular normality.  The originality claim is restricted to the multidimensional intrinsic coefficient and its particular physical realization/observation hierarchy proved in this manuscript.

**Active bibliography:** `v5/references_v18.tex`.  
**Audit record:** `LITERATURE_VERIFICATION_V18.md`.

## C17-E3 — contribution hierarchy / dossier problem

**Referee point.**  The v17 active entry point contained sixty direct inputs and the introduction still foregrounded the older acquisition program, while the response letter treated boundary information as the significance answer.  The paper therefore read as an accumulating dossier.

**Revision.**  The active front matter has been rebuilt rather than incrementally patched.

The revised title is **“Boundary laws, information loss, and two-contact rigidity in dispersing billiards.”**  The abstract now presents two linked main chains:

1. the nonlinear relative boundary law and its geometric/profile consequences;
2. the observation-dependent information transition generated by residual-time coarsening.

The active introduction is replaced by `article/01_introduction_v18.tex`.  It begins with the determinant normalization shared by both chains, places the boundary-information theorem and the strict observation hierarchy before the acquisition material, and explicitly subordinates the older calibration/acquisition/adaptive modules to the principal forward structure.  The mathematical modules themselves remain active; no theorem is deleted merely for presentation.

Part II is retitled **“Boundary information and observation-dependent transitions”** and begins with the general information theorem and billiard endpoint experiment before Abel stability and regularized profile observation.  The appendix retains all historical auxiliary proof chains.

The previous introduction remains in the repository unchanged for provenance, but is no longer the active introduction.  This preserves content while giving the submission a single readable theorem hierarchy.

## C17-R1 — complete native build

**Referee point.**  The v17 workflow run failed before a runner executed any step; therefore no successful full native build was established.

**Revision.**  A branch-specific workflow is added at `.github/workflows/a2-v18-native-build.yml`.  It is configured to trigger on the v18 revision branch and to:

1. retain the exact source commit and a source archive;
2. install a native TeX toolchain;
3. run the existing `tools/build_submission.py`, which builds the original companion before the complete article;
4. run the boundary diagnostics in ordinary and optimized Python modes and compare the outputs;
5. retain the complete build artifacts even on failure.

A workflow execution is evidence only if GitHub assigns a runner and the steps complete successfully.  This response does not convert a queued or infrastructure-level failure into a mathematical build certificate.  `VERIFICATION_V18.json` records the distinction.

## Preserved historical theorem chain

The v18 revision keeps the historical dependencies identified in the v17 derivation audit:

- `v3/10_geometry_action.tex` and `v3/20_integration.tex`: stationary action, Jacobi Hessian, physical mixed derivative and residual-time measure;
- `v4/10_boundary_layers.tex`: half-line actions/amplitudes and relative factorization;
- `v6/10_experiment_transfer.tex`: physical transfer with the failure atom retained;
- `v7/10_critical_experiments.tex`: exact tangent laws, determinant whitening and complete-record erasure profile;
- `article/30_supercritical.tex`: fixed-critical-subsample supercritical transfer;
- `article/16_hyperbolic_coordinates.tex` and the scalar/determinant transport modules: intrinsic identification of the boundary density;
- `article/23_two_contact_rigidity.tex`, `article/29_two_flight_benchmark.tex` and the profile inverse modules: the independent geometric consequences under their printed hypotheses.

No inference from finite diagnostics to these analytic theorems is made.

## Net result

The revision answers the report by tightening scope and strengthening architecture, not by retreating from proved results.  The `b=+infinity` TV conclusion remains intact; the endpoint critical law remains sharp; the physical transfer and three-level observation hierarchy remain intact; and all prior geometric/profile/finite-jet modules remain in the source tree.  What changes is the precision of the theorem scope, the literature attribution, and the hierarchy by which the reader encounters the results.
