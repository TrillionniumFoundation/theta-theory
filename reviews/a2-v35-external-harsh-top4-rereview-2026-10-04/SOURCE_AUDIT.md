# Source audit for the external A2 v35 rereview

## 1. Reviewed object

Repository: `TrillionniumFoundation/theta-theory`  
Manuscript: Qian Qi, *Scalar collision laws and recognition of periodic dispersing billiards*  
Reviewed directory: `papers/A2-v35-self-calibrated-stationary`

The reviewed object is identified by Git objects rather than by version numbering alone:

- revision branch: `revision/a2-v35-self-calibrated-stationary-2026-10-04`;
- equivalent referee-copy branch: `revision/a2-v35-self-calibrated-referee-copy-2026-10-04`;
- commit: `70c055e1ff090d58ecd61a5644e0fa62a7766f13`;
- repository tree: `052f994e14452cc42a39ab23c8dae33a468c6495`;
- commit date: 4 October 2026;
- commit title: `A2 v35: clarify rolling-radius and signed-kernel proofs`.

Both controlling branch names resolve to that same commit. No `revision/a2-v36...` branch was present when the review was frozen.

The review branch

`review/a2-v35-external-harsh-top4-rereview-2026-10-04`

was created directly from the reviewed commit. It adds files only under

`reviews/a2-v35-external-harsh-top4-rereview-2026-10-04/`.

No manuscript source, author branch, previous review, workflow, historical archive or unrelated paper is modified by this review.

## 2. Which v35 branch is controlling

The repository also contains

`revision/a2-v35-self-calibrated-footprint-2026-10-04`

at commit

`7125ed358a6c3da9fef0cd0011cca0710ad0aab4`.

That branch is a divergent sibling based directly on the v34 review head. It predates the final stationary package and does not contain the controlling latest source. The stationary branch and its referee-copy alias have the later head and include the common-noise lower-bound section and final proof clarifications.

The present report therefore reviews the stationary branch, not the earlier footprint sibling.

## 3. Prior report and revision chronology

The controlling preceding report is the v34 external report:

- branch: `review/a2-v34-external-harsh-top4-rereview-2026-10-04`;
- report commit: `e8ad32bfd0a8641c239c67e9776ba08d3aaab72a`;
- reviewed v34 author commit: `ed3876b8a82e2c46bc1533457978c15fea1a2114`.

Version 35 is based on that report. The final reviewed commit has parent

`53ba5552efea5df04c4e33e30b7d67c815cf3fbf`,

which changes the verification workflow. The final commit itself changes only

`papers/A2-v35-self-calibrated-stationary/core/09_stationary_jitter.tex`

and adds the two proof clarifications requested by the v34 report.

The exact reviewed v34 directory and its v33 archive remain at their original repository paths. Version 35 does not copy them into a new nested tree.

## 4. Active manuscript inputs inspected

The current `main.tex` activates:

- `core/00_setting.tex`;
- `core/00b_resource_overview.tex`;
- `core/00c_stationary_overview.tex`;
- `core/00d_self_calibration_overview.tex`;
- `core/01_local_queries.tex`;
- `core/02_adaptive_boundary.tex`;
- `core/06_finite_precision.tex`;
- `core/03_period_recognition.tex`;
- `core/04_information_bound.tex`;
- `core/07_sequential_gauge.tex`;
- `core/08_calibration_resolution.tex`;
- `core/09_stationary_jitter.tex`;
- `core/10_unknown_footprint.tex`;
- `core/11_stationary_information.tex`;
- `core/05_comparison.tex`;
- `references.tex`.

The audit read the current abstract and theorem statements, the response to referees, proof/history/literature ledgers, README and submission map. It also inspected the v34 report and the source-delivery workflow.

The principal new mathematical inputs are:

1. `core/10_unknown_footprint.tex`, which proves two-scale footprint/table recovery;
2. `core/11_stationary_information.tex`, which proves the common-noise expected-attempt lower bound;
3. the final modifications to `core/09_stationary_jitter.tex`.

## 5. Mathematical deltas confirmed

### 5.1 Unknown footprint recovery

The revision no longer assumes the complete support function of the launch footprint. It assumes two known positive homothetic scale factors and a common known dilation origin, plus uniform footprint bounds. The observed positive components are

`P_{i,C}=C+(-lambda_i K)`.

Strict nesting pairs the scale-one and scale-two components, and a two-by-two support system recovers `K` and `C`.

### 5.2 Common stationary-noise lower bound

The revision fixes one known uniform-disk law, shared across tables and commands. A mean-contraction lemma gives an `O(h^s)` response range on a physical packing. A conditional binary-range inequality and stopped chain rule convert this into the expected-attempt power

`nu^(-(s+1)/(s-2))`.

This is distinct from the earlier adversarial implementation-map converse.

### 5.3 Requested proof clarifications

The final commit places every erosion below explicit uniform rolling radii. It also identifies the sixth-order approximation kernel as signed and displays coefficients that cancel the second, fourth and sixth moments of an even base kernel.

## 6. Repository-delivery audit

### 6.1 README claims

The README states that a local run:

- built a 36-page warning-free primary;
- passed 4,254 current finite diagnostics;
- passed 19 current validation-contract checks;
- reran 5,886 v34 diagnostics and 21 v34 contract checks;
- can be reproduced with `tools/validate_v35.py`.

### 6.2 Files present at the reviewed head

The reviewed v35 paper directory contains the manuscript, ledgers and maps. It does not contain:

- a `tools/` directory;
- `tools/validate_v35.py`;
- the current finite diagnostic program named by the README;
- a `verification/` receipt tree;
- a `SOURCE_PINS.json` manifest.

A direct contents request for the advertised tools path returns `404 Not Found`, and the recursive reviewed tree contains no v35 validation path. The README's local evidence is therefore not reproducible from the reviewed branch as delivered.

### 6.3 Workflow at the reviewed head

The workflow is

`.github/workflows/a2-v35-verify.yml`.

It performs only:

1. exact-triggering-SHA checkout;
2. TeX and PDF-tool installation;
3. primary `latexmk` build plus a log grep;
4. an exact-SHA/status check if the build succeeds.

It does not execute the validation commands claimed by the README, rerun v34 diagnostics, check source pins, generate a receipt, archive logs or upload failure evidence.

### 6.4 Actual hosted result

The exact-head run is:

- run ID: `37177203228`;
- workflow: `A2 v35 manuscript qualification`;
- head SHA: `70c055e1ff090d58ecd61a5644e0fa62a7766f13`;
- status: `completed`;
- conclusion: `failure`.

Job details show:

- checkout: success;
- dependency installation: success;
- `Build primary manuscript`: failure;
- `Bind exact source commit`: skipped.

The run contains zero uploaded artifacts. Because no failure artifact or log bundle was retained, this audit does not infer a more specific failure cause from the workflow metadata alone.

The current source is therefore **not exact-head build-qualified**.

## 7. Independent finite diagnostics

The review's `verify_review.py` imports no author module and uses only the Python standard library. Ordinary and optimized executions are byte-identical. It records 555,419 successful checks.

The finite groups cover:

- two-scale support identities and perturbation bounds;
- disk-model scale nesting and radius recovery;
- scaled density lower-bound algebra;
- signed-kernel moment cancellation;
- circular lens and weighted boundary-mass powers;
- finite Bernoulli information-range comparisons;
- stopped information-budget algebra;
- exact killed-chain exit times and Green perturbation bounds;
- stationary upper/lower exponent identities;
- parallel-area controls.

These diagnostics do not build the TeX source, certify the physical apparatus, prove the continuum compactness/interpolation arguments or authenticate author evidence.

## 8. Limits of this audit

This is a targeted top-four rereview. It concentrated on:

1. whether the v34 objections were actually answered;
2. whether the new two-scale inverse is algebraically and geometrically coherent;
3. whether the stationary lower bound uses one common noise law and handles adaptive stopping correctly;
4. whether the finite exponents follow from the displayed constructions;
5. whether the source package supports its reproducibility claims;
6. whether the corrected contribution reaches the requested editorial benchmark.

No exhaustive priority search was performed. The audit did not re-prove every inherited theorem in the long A2 programme, execute a collision apparatus or complete an independent TeX build.

## 9. Audit conclusion

The reviewed mathematical source is unambiguously pinned. Version 35 is a substantive response to v34. The two-scale support inverse and common-stationary-noise lower bound are real additions, and no fatal error was found in their audited core.

The final repository delivery is materially weaker than the mathematical package described by its README: the cited validators and receipts are absent, and the only exact-head workflow failed its primary build without retaining artifacts.

The negative top-four recommendation in `REFEREE_REPORT.md` rests primarily on the information model, strong calibration/prior contract and unresolved rate gap. The failed source qualification is a separate submission-readiness defect.