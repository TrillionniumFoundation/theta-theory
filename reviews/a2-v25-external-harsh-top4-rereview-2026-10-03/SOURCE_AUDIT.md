# Source audit for the external A2 v25 rereview

## 1. Reviewed object

Repository: `TrillionniumFoundation/theta-theory`  
Manuscript: Qian Qi, *Reference-free certification from intrinsic boundary laws*  
Directory: `papers/A2-v25-effective-local-recognition`

The reviewed source is frozen by Git object:

- revision branch: `revision/a2-v25-effective-local-recognition-2026-10-03`;
- equivalent alias: `revision/a2-v25-referee-copy-2026-10-03`;
- author commit: `7151ddcd8b29516a8a6f8fa5043b97c49206b3ae`;
- repository tree: `175e6b77020f87ffb5f7d7ceff19e8786b401eb7`;
- mathematical checkpoint: `a5293ca684337b184ba4637cba2c223c684a61ea`;
- commit date: 3 October 2026;
- commit title: `A2 v25: complete effective-recognition revision, source pins and rereview package`.

Both revision aliases resolved to the same author commit. A repository branch search found no `revision/a2-v26...` branch before the review branch was created.

The review branch is

`review/a2-v25-external-harsh-top4-rereview-2026-10-03`.

It was created directly from the author commit and adds files only below

`reviews/a2-v25-external-harsh-top4-rereview-2026-10-03/`.

No author source, prior review, revision branch, retained volume, workflow or unrelated paper is modified.

## 2. Revision chronology

The checkpoint parent is the latest v24 external-review head

`3aeea88879dbba28a7564e3c5787ce293e3a45c8`.

That report reviewed author commit

`f5754f7eacc5b2bde9450de154a4e4c0093b3e23`.

The v25 source pins preserve:

- reviewed v24 tree: `3d729a1fe93e2250cd68494d149fbb6e90b4096e` at `retained/v24`;
- original complete supplement tree: `14b2e5379e5b223bc0bdc823c97fd77c2dca2cda`;
- v24 review commit: `3aeea88879dbba28a7564e3c5787ce293e3a45c8`;
- v24 report blob: `81646493b2011abb8edfa95b4eef795208ef7c0e`.

The chronology is therefore clean: the mathematical checkpoint descends directly from the latest report, and the final author head adds response, ledgers, source bindings, tools and execution evidence.

## 3. Active primary source

The active input order in `main.tex` is:

1. `core/01_setting.tex`;
2. `core/02_fingerprints.tex`;
3. `core/07_effective_fingerprints.tex`;
4. `core/03_local_acquisition.tex`;
5. `core/08_value_probe.tex`;
6. `core/04_inverse_certificate.tex`;
7. `core/05_noisy_stopping.tex`;
8. `core/06_comparison.tex`.

The following v24 active chapters retain their exact Git blobs:

- `core/03_local_acquisition.tex` — `3eed5495efbb84f3270607e7cae87d745fb88cf1`;
- `core/04_inverse_certificate.tex` — `8d6735f47f2937faf10f5224d04b1cbc201ac673`;
- `core/05_noisy_stopping.tex` — `dc2c449e48ef7c667a7dd11f0295b81916ec1fea`.

The new or revised active mathematical inputs are:

- expanded setting and corrected stopping exponent in `core/01_setting.tex`;
- fixed-presentation compactness in `core/02_fingerprints.tex`;
- explicit quantitative recognition in `core/07_effective_fingerprints.tex`;
- value-only local probing in `core/08_value_probe.tex`;
- expanded information comparison in `core/06_comparison.tex`.

## 4. Files inspected

The rereview inspected the following current files in detail:

- `main.tex` and `references.tex`;
- all eight active core inputs;
- `RESPONSE_TO_REFEREES.md`;
- `README.md`;
- `REVISION_STATUS.md`;
- `PROOF_LEDGER.md`;
- `HISTORICAL_DERIVATION_AUDIT.md`;
- `LITERATURE_AUDIT.md`;
- `SOURCE_PINS.json`;
- `PUBLICATION_BINDING.json`;
- `BUILD_QUALIFICATION.md`;
- `tools/calibrate_fingerprint.py`;
- `tools/verify_v25.py`;
- `tools/validate_v25.py` at the theorem/evidence-contract level;
- `verification/local/receipt.json`;
- `.github/workflows/a2-v25-verify.yml`;
- the latest v24 referee report and its machine-readable findings.

The rereview also checked the hosted workflow run and job attached to the exact author SHA.

## 5. Mathematical deltas confirmed

### 5.1 Fixed-presentation compactness

The new Lemma 2.1 keeps redundant bounded lattice presentations rather than selecting a discontinuous reduced basis. It provides a compact topology for bodies, centers, lattice matrices and finite bridge labels, and explains representative and basis relabelling.

### 5.2 Explicit recognition constants

Section 3 supplies:

- an explicit interpolation/three-circles continuation modulus;
- local graph-to-support conversion;
- full-pair Hausdorff control;
- quantitative shape, symmetry and physical-copy locking;
- a computable jet order and threshold;
- a finite value-grid fingerprint with reversal implemented by permutation.

### 5.3 Value-only local sensor

Section 5 supplies:

- deterministic finite-difference enclosures;
- a uniform `C^2` chart approximation from height values;
- interval contraction for the normal point;
- the retained clearance mesh;
- canonical graph conversion;
- certified arclength quadrature;
- value-query cost and corrected expected-work conditions.

### 5.4 Corrected tail exponent

The main theorem now quantifies over a chosen `a >= 6`. Generic expected probe work uses `a > 4+s`; the value-query specialization uses `a > 5+3s_v`. The earlier fixed-`a=6` inconsistency is closed.

## 6. Author evidence

The local source-content receipt records:

- 5,490 finite checks;
- ordinary/optimized Python identity;
- a 22-page primary PDF;
- no final TeX diagnostics;
- unchanged source manifest;
- `execution_kind: source_content_not_git_checkout`;
- `scope: primary_only`;
- no physical sensor execution;
- no formal proof certificate.

The supplied symbolic calibration example has:

- `J = 516`;
- `m0 = 27`;
- `P = 27 * 2^519`;
- `E_* = 76 * 2^(-P)`;
- `N = 2^P`;
- no expanded fingerprint coordinates.

This evidence is appropriately scoped. It illustrates finite symbolic computability and the extreme size of the constants; it does not execute the sensor or prove the uniform theorem by enumeration.

## 7. Hosted exact-source qualification

Workflow:

`.github/workflows/a2-v25-verify.yml`

The workflow uses read-only permissions, checks out `${{ github.sha }}`, disables persisted credentials, validates with

`tools/validate_v25.py --all-volumes --require-checkout`,

and archives current receipts, raw diagnostics, delivered PDFs, source pins, publication binding and the nested v24 requalification.

Exact reviewed-head run:

- run ID: `37111917413`;
- head SHA: `7151ddcd8b29516a8a6f8fa5043b97c49206b3ae`;
- status: `completed`;
- conclusion: `success`.

The job records success for:

1. exact triggering-SHA checkout;
2. mathematical build dependency installation;
3. current-source and all-declared-volume validation;
4. evidence and PDF archival.

Thus source qualification is not a negative finding in the referee report.

## 8. Independent review diagnostics

The review's `verify_review.py` imports no author module and uses the Python standard library. It performs 29,326 checks in ordinary and optimized mode. The groups cover:

- explicit interpolation and chain-of-disks algebra;
- continuation-threshold cancellation;
- geometric support and copy-locking margins;
- symbolic jet and value-grid budgets;
- registry error bands;
- deterministic first/second differences;
- arclength integrand control;
- corrected cost summability;
- retained rational subgroup and completion-defect algebra;
- relative-contact translation invariance.

The checks do not certify compactness, analytic identity continuation, interval root certification, physical acquisition, literature priority or the multi-volume proof programme.

## 9. Scope and limits

This was a targeted external rereview of the new v25 mathematics, its dependencies and the requested top-four significance. It was not:

- a formal proof assistant verification;
- an execution of a physical billiard sensor;
- an exhaustive priority search;
- a reproof of every retained theorem from v4 through v24;
- a journal editorial decision.

The verdict in `REFEREE_REPORT.md` distinguishes mathematical correctness from the strength and naturality of the information model.