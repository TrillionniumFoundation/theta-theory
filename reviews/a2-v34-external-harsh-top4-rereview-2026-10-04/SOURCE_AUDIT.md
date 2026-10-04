# Source audit for the external A2 v34 rereview

## 1. Reviewed object

Repository: `TrillionniumFoundation/theta-theory`  
Paper: Qian Qi, *Scalar collision laws and recognition of periodic dispersing billiards*  
Paper directory: `papers/A2-v34-calibration-experiments`

The reviewed source is identified by Git object rather than by branch chronology:

- revision branch: `revision/a2-v34-calibration-experiments-2026-10-04`;
- equivalent referee-copy alias: `revision/a2-v34-referee-copy-2026-10-04`;
- reviewed head: `ed3876b8a82e2c46bc1533457978c15fea1a2114`;
- reviewed repository tree: `26e7db3cd999c260e21d086352864334cc1a38c6`;
- mathematical checkpoint: `477cbff26270b6a04af2c09b9a82d5e804345c46`;
- checkpoint date: 4 October 2026.

Both v34 author branch names resolved to the same reviewed head. No `revision/a2-v35...` branch was present immediately before the review branch was created.

The review branch

`review/a2-v34-external-harsh-top4-rereview-2026-10-04`

was created directly from the reviewed head. It adds files only under

`reviews/a2-v34-external-harsh-top4-rereview-2026-10-04/`.

No author source, revision branch, workflow, previous review, preserved historical tree or unrelated paper was edited.

## 2. Revision chronology

The controlling preceding report is the final v33 review commit

`3d825951afb2c2bd1da258de8648287c046cdc13`

with report blob

`0acfac285985da9babdc8721a87dcef608b4c7d0`.

It reviewed v33 author commit

`245a2bf5d13b72d81ef85b784e9fcb2dd88ca490`.

The v34 mathematical checkpoint `477cbff...` is based directly on that final review head. It introduces the fixed-footprint stationary-jitter inverse, the corrected calibration-converse presentation, the one-article submission architecture, current verification tools and the exact preserved v33 tree.

The final reviewed head is two commits ahead of the mathematical checkpoint. A direct comparison shows changes only to:

- `.github/workflows/a2-v34-verify.yml`;
- one dependency sentence in `papers/A2-v34-calibration-experiments/README.md`;
- `papers/A2-v34-calibration-experiments/verification/CI_ENVIRONMENT.md`.

No active mathematical TeX file, test logic, source pin or archive content changed after the checkpoint.

## 3. Preserved source

The complete reviewed v33 paper is preserved at

`papers/A2-v34-calibration-experiments/archive/v33`

with Git tree

`213cecf77265c5ebea98791a99126b9def5d25f0`.

`SOURCE_PINS.json` records that tree together with:

- controlling v33 review commit `3d825951...`;
- controlling report blob `0acfac...`;
- reviewed v33 author commit `245a2bf...`;
- SHA-256 values for every active v34 mathematical and tool source;
- a one-document journal manifest containing `main.tex`.

The current validation suite checks archive-tree integrity. The journal article does not input the archive. Historical mathematics is therefore retained without being silently imported as a mandatory proof supplement.

## 4. Active files inspected

The audit read the following active article files:

- `main.tex`;
- `references.tex`;
- `core/00_setting.tex`;
- `core/00b_resource_overview.tex`;
- `core/00c_stationary_overview.tex`;
- `core/01_local_queries.tex`;
- `core/02_adaptive_boundary.tex`;
- `core/03_period_recognition.tex`;
- `core/04_information_bound.tex`;
- `core/05_comparison.tex`;
- `core/06_finite_precision.tex`;
- `core/07_sequential_gauge.tex`;
- `core/08_calibration_resolution.tex`;
- `core/09_stationary_jitter.tex`.

The audit also read:

- `RESPONSE_TO_REFEREES.md`;
- `PROOF_LEDGER.md`;
- `HISTORICAL_DERIVATION_AUDIT.md`;
- `LITERATURE_AUDIT.md`;
- `README.md`;
- `SUBMISSION_MAP.md`;
- `SOURCE_PINS.json`;
- `tools/verify_v34.py`;
- `tools/test_contract_v34.py` through its recorded contract results;
- `tools/validate_v34.py` through its source pin and execution contract;
- `verification/local/receipt.json`;
- `.github/workflows/a2-v34-verify.yml`.

The complete v33 referee report and its source chronology were used to distinguish newly answered objections from inherited conclusions.

## 5. Mathematical delta confirmed

The new active mathematical input is principally `core/09_stationary_jitter.tex`, together with the revised overview/comparison and explicit qualifications in the calibration chapter.

The v34 delta establishes:

1. reciprocal forcing for one unknown stationary additive launch density on a known compact footprint;
2. exact support recovery through the positivity set of the blurred occupation;
3. Minkowski support subtraction without density deconvolution;
4. a uniform near-boundary mass lower bound of order `e^(gamma+3/2)`;
5. a density-independent inverse modulus for two different nuisance densities;
6. a fixed-aperture Green bound for high-accuracy noisy Bellman iterates;
7. an indeterminate-layer local query with cost `e^(-(2gamma+3))` up to logarithms;
8. a finite whole-table reconstruction theorem with the stated polynomial attempted-bit upper bound;
9. a no-positive-resolution-floor corollary for fixed uniform-disk launch noise in this calibrated model.

The revised calibration-converse chapter also implements the v33 report's requested explicit uncertainty quantifiers and closed-set boundary convention.

## 6. Author evidence

The local receipt records source-content execution, not an authenticated Git checkout. It reports:

- 5,886 v34 finite mathematical/source checks;
- 21 v34 validation-contract checks;
- ordinary/optimized output identity;
- successful reruns of the retained v33 and v32 suites;
- a 28-page primary build;
- no final TeX diagnostics;
- no physical sensor execution;
- no formal proof certificate.

The receipt's stated scope is

`primary_and_archive_integrity_not_historical_volume_rebuilds`.

The retained check counts overlap earlier suites and are not treated as independent proof counts by this review.

## 7. Hosted exact-SHA qualification

The final workflow is

`.github/workflows/a2-v34-verify.yml`.

The exact-head run is:

- run ID: `37174046426`;
- head SHA: `ed3876b8a82e2c46bc1533457978c15fea1a2114`;
- status: `completed`;
- conclusion: `success`.

The job successfully:

1. checked out exactly the triggering commit;
2. installed and preflighted `mpmath`, NumPy, SciPy and Shapely together with the TeX environment;
3. qualified current proofs and archive integrity;
4. bound the actual source and execution outputs;
5. uploaded the evidence artifact.

The artifact is:

- artifact ID: `11292677471`;
- artifact name: `A2-v34-ed3876b8a82e2c46bc1533457978c15fea1a2114`;
- digest: `sha256:8117e6340d009ea5bc956fb97083d6e8070495fc0b1112a119e0efa9fe94ca86`.

Two earlier runs failed because the retained suites required numerical dependencies not yet installed. The failures and artifacts are preserved. The successful final run is therefore not a relabelling of either failure.

## 8. Independent finite diagnostics

The review's `verify_review.py` imports no author module. Ordinary and optimized execution produced byte-identical JSON output.

It performs 89,669 finite checks, using exact integer or rational arithmetic except for finite binary-logarithm budget comparisons. The groups cover:

- reciprocal bit identities;
- stationary translation and one-dimensional support controls;
- exact finite support addition/subtraction and centering;
- rolling-disk lens rectangles and exponent identities;
- finite killed-lattice Bellman and Green bounds;
- query thresholds and error allocations;
- robust bisection under an indeterminate layer;
- stationary upper-bound exponent balances;
- rational period/subgroup arithmetic;
- finite binary-cap controls.

Hashes:

- review script SHA-256: `b616e1e1637518c74fddc266945d21f4a5a4ce88ced607e6052d45aa25d8aa03`;
- ordinary/optimized output SHA-256: `f90f091b63e9f11face815dbb127f91de163633ebbc9a9442cfbd24b1723af6e`;
- result's internal canonical SHA-256 field: `5548c39f39c2e83ae10b0398a81039807f431b41871543e8e8a9746aa5414412`.

These checks do not certify the continuum lens argument, the full physical class, the apparatus, the TeX source, the entire historical programme, literature priority or journal significance.

## 9. Audit limits

This was a targeted external rereview of the newest mathematical delta and the proof chain on which it depends. It was not a formal reproof of every theorem in the preserved multi-generation archive.

No physical collision instrument was executed. No independent TeX build was performed by the review script; the exact-SHA author workflow supplies build evidence. No exhaustive literature or priority search was performed.

The source object, revision chronology, preservation boundary and final workflow result are nevertheless unambiguous and reproducibly pinned.
