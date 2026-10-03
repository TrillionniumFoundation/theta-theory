# Source audit for the external A2 v29 rereview

## 1. Reviewed object

Repository: `TrillionniumFoundation/theta-theory`  
Manuscript: Qian Qi, *Scalar collision laws and recognition of periodic dispersing billiards*  
Manuscript directory: `papers/A2-v29-scalar-collision-tomography`

The reviewed source is identified by Git object rather than branch chronology:

- revision branch: `revision/a2-v29-scalar-collision-tomography-2026-10-03`;
- equivalent referee-copy alias: `revision/a2-v29-referee-copy-2026-10-03`;
- author commit: `b81664d3961cdbad58563f37dcaed03288de199e`;
- repository tree: `7957f3778b73ff4948090bce5338df8de0b2de0c`;
- mathematical checkpoint: `44c2b6bd6caf8946384ade3576a079c4e237bbd9`;
- commit date: 3 October 2026.

Both v29 aliases resolved to the same author commit. A search immediately before branch creation found no `revision/a2-v30...` branch.

The review branch

`review/a2-v29-external-harsh-top4-rereview-2026-10-03`

was created directly from the author commit. The review writes only below

`reviews/a2-v29-external-harsh-top4-rereview-2026-10-03/`.

No author manuscript, author workflow, revision branch, preceding review, retained volume or unrelated paper is changed by this review.

## 2. Revision chronology

The mathematical checkpoint has parent

`a067c123c5702decb4b7146cf57961a65afe5c88`,

the external v28 review head. That report reviewed v28 author source

`3ac2df58d175010f338dd6ae8af84158c1590d20`.

The v29 source pins preserve the complete reviewed v28 paper under

`papers/A2-v29-scalar-collision-tomography/retained/v28`

with native tree

`b17c9c051f3e279d6f7610e3d1c5e56d0733216a`.

Thus the author chronology is clean: the scalar revision responds to the latest frozen v28 report, and the retained supplement is a source snapshot rather than a rewritten dependency.

## 3. Active source inspected

The review read the current primary source:

- `main.tex`;
- `core/01_reversal.tex`;
- `core/02_local_acquisition.tex`;
- `core/03_periods.tex`;
- `core/04_finite_experiment.tex`;
- `core/05_comparison.tex`;
- `references.tex`.

It also inspected:

- `README.md`;
- `RESPONSE_TO_REFEREES.md`;
- `PROOF_LEDGER.md`;
- `LITERATURE_AUDIT.md`;
- `SOURCE_PINS.json`;
- `verification/local/receipt.json`;
- `tools/verify_v29.py` through its recorded scope and receipt;
- `.github/workflows/a2-v29-verify.yml`;
- the exact-SHA workflow run and jobs;
- the controlling v28 referee report.

The active primary is self-contained for the scalar reversal, chain inverse, finite acquisition and period-recognition route. Supplement P preserves the preceding multi-volume programme, but this review did not re-prove every inherited theorem in that archive.

## 4. Mathematical delta confirmed

Version 29 makes the following substantive changes relative to the v28 theorem emphasized by the preceding report.

### 4.1 Scalar output replaces impact-position output

The new observation records only whether a commanded attempted launch collides before one fixed horizon. No impact position, impact angle or collision time is returned. A solid attempted start and a free miss both return zero.

The command side is correspondingly stronger: the observer chooses localized spatial input laws and two exactly opposed collimated directions. The command center, spatial mask, direction and horizon are known.

### 4.2 Exact reversal balance

The new theorem proves

`B_a(q)-B_{-a}(q+a)=chi(q+a)-chi(q)`

for every closed obstacle set. Its integrated form identifies the finite difference of occupation from two spatial input-output functionals. Multiple interior intersections cancel; no small-time limit is used.

### 4.3 Bounded zero-witness inverse

A finite minimum of telescoping sums reconstructs a nonnegative function from one directional finite difference when every prescribed chain contains a zero. Diameter and component-separation priors supply that zero condition for both the indicator and compactly mollified occupation.

### 4.4 Finite scalar patch acquisition

A deterministic two-dimensional grid of localized kernel commands reconstructs occupation averages with error independent of the kernel scale once the scalar means are controlled. Erosion inclusions and a rolling-ball argument convert their uniform comparison into matched component geometry. A compensated smoothing estimate converts Hausdorff error into support-function `C^2` error.

### 4.5 Retained period theorem under the new sensor

The primary reproduces the v28 two-sided central-patch period criterion, protected generating list, patch-margin classification and rational locking. The new contribution is the scalar route to the physical patch on which those retained arguments operate.

## 5. Source bindings

`SOURCE_PINS.json` binds:

- every new core TeX file;
- `main.tex` and `references.tex`;
- `tools/test_contract.py`;
- `tools/validate_v29.py`;
- `tools/verify_v29.py`;
- the workflow digest;
- the v28 retained tree;
- the mathematical checkpoint and controlling report.

The author commit is unsigned at the GitHub level. This is a repository-signature fact, not a mathematical defect.

## 6. Author local evidence

The local receipt records:

- execution kind: `source_content`;
- scope: `primary_only`;
- source commit and GitHub run fields: null;
- 18,945 finite mathematical/source checks;
- 19 validation-contract checks;
- identical ordinary and optimized Python output;
- a warning-free twelve-page primary build;
- unchanged pinned sources during validation;
- no physical sensor execution;
- no formal proof certificate;
- no local full-package qualification.

This is correctly scoped local evidence. It is not represented as an authenticated checkout or as a rebuild of the retained eleven documents.

## 7. Hosted exact-source qualification

The workflow

`.github/workflows/a2-v29-verify.yml`

checks out the exact triggering SHA without persistent credentials, verifies the current and retained entry points, installs the mathematical environment, runs

`tools/validate_v29.py --all-volumes --require-checkout --expected-commit "$GITHUB_SHA"`,

archives exact sources and actual evidence, and uploads the results even on failure.

For the reviewed commit, GitHub Actions run

`37133211373`

reported:

- status: `completed`;
- conclusion: `success`;
- head SHA: `b81664d3961cdbad58563f37dcaed03288de199e`.

The job record reports successful completion of:

1. exact triggering-source checkout;
2. current and retained entry-point checks;
3. environment installation;
4. all twelve declared document qualifications;
5. source/evidence archival;
6. artifact upload.

Accordingly, this review records the exact-SHA twelve-document delivery as successful. Compilation and finite checks are reproducibility evidence, not mathematical proof certification.

## 8. Independent review diagnostics

The review's `verify_review.py` imports no author module. Ordinary and optimized Python output are identical. The script performs 306,117 successful exact integer/rational checks covering finite instances of:

- reversal balance;
- weighted probability balance;
- finite-chain inversion and deterministic noise amplification;
- geometric zero witnesses;
- grid and smoothing constants;
- two-sided motif period tests;
- patch-margin threshold arithmetic;
- determinant and bounded-denominator lattice identities.

The script does not build TeX, execute a physical apparatus, certify the compactness/continuum arguments, determine priority, or formally verify the retained programme.

## 9. Audit limits

This was a targeted external rereview of the v29 mathematical delta and the dependencies needed by its main theorem. It is not:

- a formal proof verification;
- an exhaustive priority search;
- a physical feasibility certification;
- a re-proof of every retained theorem;
- a journal editorial decision.

The correctness conclusion is therefore appropriately limited: no fatal counterexample was found in the audited v29 core, and the finite diagnostics support the displayed algebra, but they do not replace expert line-by-line proof review.

## 10. Source-audit conclusion

The reviewed object is unambiguous, source-pinned and chronologically based on the latest frozen report. The v28 source is preserved exactly, the scalar primary is active and self-contained for its main route, and the exact-SHA twelve-document qualification succeeds. The negative top-four recommendation in `REFEREE_REPORT.md` is a mathematical-significance and information-model judgment, not a claim that v29 is a branch alias, a failed delivery, or known to contain a fatal central error.
