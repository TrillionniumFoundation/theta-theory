# Source audit for the external A2-DYN review

## 1. Reviewed object

Repository: `TrillionniumFoundation/theta-theory`  
Manuscript: Qian Qi, *Collision records, arithmetic, and raw local inversion in a triangular Lorentz gas*  
Reviewed directory: `papers/A2-DYN-v4-quantitative-periods-and-clock`

The latest A2-DYN branch visible at the time of review was

`revision/a2-dyn-v5-raw-llt-referee-response-2026-10-05`.

It is an exact alias of

`revision/a2-dyn-v4-referee-response-2026-10-05`.

Both resolve to:

- commit: `f0c2f6c9044a9e76e487329dbf7791f865ee7b8c`;
- repository tree: `73ded33d0d53feb57d526bf55d3797012535f6dd`;
- active core tree: `37509bf72fe8b9e28a7831b2b87fb56a5cff9913`.

The mathematical parent is:

- commit: `12a7c04eaf9754de356a69dfc1ec4ae09ba605b8`;
- commit title: `A2-DYN v4: quantitative period separation and uniform mechanical clock`.

The final author commit adds response, audit, validation, and exact-source qualification material and states that the mathematical core is unchanged. The review therefore identifies the source by Git object and treats the v5 branch name as an alias of the v4 manuscript.

The review branch

`review/a2-dyn-v4-external-top4-review-2026-10-05`

was created directly from the reviewed author head. Review files are confined to

`reviews/a2-dyn-v4-external-top4-review-2026-10-05/`.

No manuscript source, author revision branch, workflow, earlier paper, or unrelated path is edited.

## 2. Report-discovery boundary

Searches for branches and paths containing `a2-dyn` found author and referee-copy revision branches but no external A2-DYN review branch. The source audit in the manuscript records the same boundary and explains that the available v1 specialist handoff explicitly disclaims independent review.

The repository contains an external top-four acceptance report for A2-GEOM v43. That report was inspected only to verify that its title, source, and scope are different. It was not used as a controlling A2-DYN report.

This is therefore the first located external referee-style report on the A2-DYN manuscript. The inability to find a differently named or inaccessible report is not represented as a mathematical theorem.

## 3. Lineage

The immediate dynamics lineage used by the review is:

1. A2-DYN v1 baseline: `36f1365041de95ca478739a1e2984734c72f95aa`;
2. A2-DYN v3 baseline: `55ab80ed1a4f11b58ce9a88c365b0cea2e2ce191`;
3. v4 mathematical checkpoint: `12a7c04eaf9754de356a69dfc1ec4ae09ba605b8`;
4. v4 final/source-qualified head and v5 alias: `f0c2f6c9044a9e76e487329dbf7791f865ee7b8c`.

The source audit reports that all twenty-eight v3 proof bodies and all seventy-eight v3 labels remain active. The v4 source contains thirty-seven proof bodies and one hundred seven labels. New proofs are concentrated in the quantitative-period and uniform-clock additions; the earlier proof-bearing core files are retained byte-for-byte.

## 4. Files inspected

The review read the complete active article, including:

- `main.tex`;
- `core/01_interfaces.tex`;
- `core/02_physical_records.tex`;
- `core/03_periodic_geometry.tex`;
- `core/04_raw_edges.tex`;
- `core/05_residual_inversion.tex`;
- `core/06_downstream.tex`;
- `core/07_realization.tex`;
- `core/08_joint_arithmetic.tex`;
- `core/09_localized_inversion.tex`;
- `core/10_exact_clock.tex`;
- `core/11_return_stability.tex`;
- `core/12_quantitative_periods.tex`;
- `core/13_uniform_physical_clock.tex`;
- `references.tex`.

It also read:

- `README.md`;
- `RESPONSE_TO_REVIEW_ITEMS.md`;
- `PROOF_LEDGER.md`;
- `LITERATURE_AUDIT.md`;
- `SOURCE_AUDIT.md`;
- `VALIDATION.md`;
- `.github/workflows/a2-dyn-v4-qualification.yml`;
- the finite diagnostic scripts under `tools/`;
- the downloaded exact-SHA workflow artifact.

## 5. Mathematical deltas confirmed

The new v4 mathematical material contains the following substantive additions.

### 5.1 Quantitative excursion geometry

The optical action for the zero-winding excursion family is written exactly. The Hessian has uniform bounds, its inverse has explicit off-diagonal decay, and the minimizing heights have two-sided estimates. These yield two-sided bounds on consecutive excess-length increments.

### 5.2 Quantitative periodic phase separation

Logarithmic-length periods are selected as a function of roof frequency. Their consecutive excess increments produce an explicit negative-power lower bound on a periodic phase discrepancy. An approximate-phase corollary is stated for continuous unit-modulus phases near the selected periodic states.

### 5.3 Fixed-return parameter continuity

For each fixed number of induced returns, the raw mixed density and first moments are shown to vary continuously with the radius after branchwise removal of singular and critical neighborhoods.

### 5.4 Parameter-uniform first-order clock

A compact subadditive argument upgrades pointwise ergodic convergence to uniform convergence in the parameter. Uniform integrability controls maximal return blocks, and renewal inversion transfers the result to physical time and to the stationary length-biased law.

The paper also preserves the earlier joint arithmetic, raw edge, exact subtraction, local inversion, and downstream conditional interfaces.

## 6. Exact-source workflow

The exact-source workflow is

`.github/workflows/a2-dyn-v4-qualification.yml`.

Its trigger names the v4 branch only. Since the latest v5 branch is an exact alias of the same commit, the workflow run nevertheless qualifies the reviewed bytes by SHA.

The successful run is:

- run ID: `37253620285`;
- head SHA: `f0c2f6c9044a9e76e487329dbf7791f865ee7b8c`;
- status: `completed`;
- conclusion: `success`.

All job stages succeeded:

1. exact event-source checkout;
2. native TeX dependency installation;
3. source/finite checks and complete manuscript build;
4. source-bound artifact upload.

Artifact metadata:

- artifact ID: `11321513463`;
- name: `a2-dyn-v4-f0c2f6c9044a9e76e487329dbf7791f865ee7b8c`;
- digest: `sha256:a7948de353a64a1221acfae8ef7da81d05e9496856fc8d7c24b19d5d3393819f`.

## 7. Artifact audit

The downloaded artifact contains:

- `main.pdf`;
- `main.log`;
- `remote-build.json`;
- `v4-audit.json` and optimized output;
- retained v1 and v2 finite outputs;
- winding and excursion certificates.

`remote-build.json` records:

- reviewed head SHA: `f0c2f6c9044a9e76e487329dbf7791f865ee7b8c`;
- core tree: `37509bf72fe8b9e28a7831b2b87fb56a5cff9913`;
- native build: passed;
- source and finite checks: passed;
- PDF SHA-256: `e331e99dc9ee15afe415642497edf4a9d8fd3ab6bd7bd4d0d889a15125a0c1da`;
- full raw LLT verified: false;
- independent human review: false.

The current source audit reports 437 checks, eighteen finite excursion samples, fifteen certified increment pairs, thirty-seven active proofs, and one hundred seven labels. The retained v1 and v2 suites report 686 and 4,881 checks respectively. These are finite evidence, not continuum certification.

## 8. Independent review diagnostics

The review's `verify_review.py` imports no author code and uses only the Python standard library. Normal and optimized executions are byte-identical at SHA-256

`e67223c611df7ed74a1383b803b92fdd3ee5033f01a31bcbd205dc096a51efd8`.

It records 471,556 checks of finite exact algebra and finite/high-precision models. The checked groups include:

- the four-record determinant and five-dimensional augmented determinant;
- quantitative phase-exponent bookkeeping;
- alternating Hessian and edge coefficients;
- one-sided Fourier tails;
- Kac and collision-rate formulas;
- length-bias transfer inequalities;
- renewal inversion;
- frequency splice feasibility;
- compact-subadditive block estimates.

The diagnostics do not certify the continuum optical action, branchwise coarea, measurable cohomology, transfer operators, covariance, all-branch residual sum, or full raw LLT.

## 9. Audit conclusion

The reviewed object is unambiguous by Git SHA and source-qualified. The latest v5 branch is not a later mathematical manuscript; it is an alias of the v4 head. No fatal finite-algebra contradiction was found, and no source-build defect is used as the basis of the recommendation.

The negative recommendation in `REFEREE_REPORT.md` is a top-four completion and significance judgment. It recognizes the proved modules while treating the operator, covariance, global residual, and square-root clock obligations as genuinely unfinished.
