# Source audit for the external A2 v31 rereview

## 1. Frozen reviewed object

Repository: `TrillionniumFoundation/theta-theory`  
Paper: Qian Qi, *Scalar collision laws and recognition of periodic dispersing billiards*  
Paper directory: `papers/A2-v31-reciprocal-command-reconstruction`

The reviewed revision is identified by Git objects:

- branch: `revision/a2-v31-reciprocal-command-reconstruction-2026-10-04`;
- equivalent alias: `revision/a2-v31-referee-copy-2026-10-04`;
- commit: `27d109b0eba6a03d453834ef9da9418446ac637d`;
- repository tree: `ff918d19db00fc3aea087a02e6b4481e197c2767`;
- parent v30 commit: `c01118b11779b6161cc34e311f840e5ab36a019c`.

Both v31 branch names resolved to the same commit when this audit was frozen. A search of all `revision/a2-v*` branches found no v32 revision.

The review branch

`review/a2-v31-external-harsh-top4-rereview-2026-10-04`

was created directly from the reviewed author commit. It adds files only under

`reviews/a2-v31-external-harsh-top4-rereview-2026-10-04/`.

No author manuscript source, workflow, retained volume, old report, revision branch, or unrelated paper is changed by this review.

## 2. Revision chronology

The latest controlling external report available before v31 is:

- branch: `review/a2-v29-external-harsh-top4-rereview-2026-10-03`;
- commit: `6444b57768313ac68978b3ee04a428b4832ccb6e`;
- report blob: `d5e4be543ceb354341e01897fda83532707b1481`;
- reviewed v29 author commit: `b81664d3961cdbad58563f37dcaed03288de199e`.

Version 30 was committed at

`c01118b11779b6161cc34e311f840e5ab36a019c`

directly on top of the v29 report. No separate `review/a2-v30...` branch was present. Version 31 has that v30 commit as its parent. The present review therefore includes a targeted audit of the v30 calibration and constructive-reconstruction additions as well as the new v31 mean-exit material.

The exact complete v30 manuscript is preserved at

`papers/A2-v31-reciprocal-command-reconstruction/retained/v30`

with tree

`1a6f8f32ec62aec586883e67753b3a72895f875c`.

The retained nine-file v30 active core has tree

`315c9c3ec006eadfc66cff72acf9855af29685be`.

The current core, after adding the v31 inputs, has tree

`aa9026847310ecd9205fe631b5ed85aa141b70ed`.

## 3. Current active mathematical inputs

The current `main.tex` actively includes:

1. `core/00_overview.tex`;
2. `core/00a_reciprocal_overview.tex`;
3. `core/01_reversal.tex`;
4. `core/02_local_acquisition.tex`;
5. `core/03_periods.tex`;
6. `core/04_finite_experiment.tex`;
7. `core/06_calibrated_launches.tex`;
8. `core/07_constructive_patch.tex`;
9. `core/05_comparison.tex`;
10. `core/08_hit_functionals.tex`;
11. `core/09_mean_exit_inverse.tex`;
12. `core/10_pooled_finite_experiment.tex`;
13. `references.tex`.

The principal new v31 files are:

- `core/00a_reciprocal_overview.tex`;
- `core/09_mean_exit_inverse.tex`;
- `core/10_pooled_finite_experiment.tex`;
- `tools/reciprocal_intervals.py`;
- `tools/verify_v31.py`;
- `tools/test_v31_contract.py`;
- `tools/validate_v31.py`.

The source-pin file records SHA-256 values for all current mathematical and tool sources, the workflow hash, the retained v30 tree, and the nine inherited active core hashes.

## 4. Files inspected

The review read the current:

- `main.tex`;
- `core/00_overview.tex`;
- `core/00a_reciprocal_overview.tex`;
- `core/01_reversal.tex`;
- `core/02_local_acquisition.tex`;
- `core/03_periods.tex`;
- `core/04_finite_experiment.tex`;
- `core/05_comparison.tex`;
- `core/06_calibrated_launches.tex`;
- `core/07_constructive_patch.tex`;
- `core/08_hit_functionals.tex`;
- `core/09_mean_exit_inverse.tex`;
- `core/10_pooled_finite_experiment.tex`;
- `RESPONSE_TO_REFEREES.md`;
- `PROOF_LEDGER.md`;
- `LITERATURE_AUDIT.md`;
- `HISTORICAL_DERIVATION_AUDIT.md`;
- `README.md`;
- `SUBMISSION_MAP.md`;
- `SOURCE_PINS.json`;
- `references.tex`;
- `tools/reciprocal_intervals.py`;
- `tools/verify_v31.py`;
- `verification/local/summary.json`;
- `.github/workflows/a2-v31-verify.yml`.

The review also read the complete v29 referee report and the retained v30 proof/source ledgers relevant to the inherited additions.

## 5. Mathematical deltas confirmed

Version 31 makes the following active additions.

### 5.1 Mean-exit inversion

For bounded centered displacement laws with positive second moment, the manuscript proves:

- a diameter-to-variance uniform mean-exit bound;
- a geometric survival tail;
- monotone Bellman reconstruction;
- a finite-depth forcing/update error bound;
- a comparison between two admissible occupations with different zero sets.

### 5.2 General bounded nontrivial laws

The manuscript derives a positive-probability escape cone from any bounded law other than `delta_0`, giving a geometric block tail and finite mean exit. This removes the v30 requirement that every realized displacement make progress in one common direction.

### 5.3 Fixed-aperture localization

The Bellman and stopped-comparison proofs are localized to one prior-controlled aperture with killed zero extension. The manuscript explicitly excludes periodic wraparound and renormalized boundary rows.

### 5.4 Finite pooled-direction implementation

For the four-atom compass law, the manuscript gives:

- exact grid shifts;
- two pooled Bernoulli means per spatial center;
- fixed prior-dependent Bellman depth;
- rational forcing and occupation intervals;
- the displayed command, attempt, calibration and arithmetic bounds.

These additions are active inputs of `main.tex`, not unattached notes.

## 6. Audit of inherited v30 material

Because no separate v30 external report was found, the present rereview also inspected:

- the grazing-uniform coupled calibration theorem;
- the finite stopped inverse under an almost-sure cone;
- threshold clustering and convex-hull recovery;
- compensated support smoothing;
- the constructive period-locking route;
- capacity-functional and active-probing comparisons.

No fatal counterexample was found in this targeted audit. The current report records the strong hypotheses and editorial limitations rather than treating those inherited additions as previously refereed.

## 7. Author evidence

The committed local summary reports:

- execution kind: source-content execution;
- scope: primary only;
- 8,513 finite mathematical/source checks;
- 49 validation-contract checks;
- ordinary/optimized agreement;
- a 26-page primary;
- no final TeX diagnostics;
- no physical sensor execution;
- no formal proof certificate;
- no local full-package qualification claim.

This local evidence is correctly scoped.

## 8. Hosted exact-source qualification

The read-only workflow is:

`.github/workflows/a2-v31-verify.yml`.

For the reviewed head:

- run ID: `37140328128`;
- head SHA: `27d109b0eba6a03d453834ef9da9418446ac637d`;
- status: `completed`;
- conclusion: `success`.

The job record shows successful completion of:

1. exact triggering-source checkout;
2. current and retained entry-point checks;
3. environment installation;
4. qualification of all fourteen declared documents at the exact SHA;
5. source/evidence archival;
6. artifact upload.

Accordingly, this review does not use a source-delivery failure as part of its negative recommendation.

## 9. Independent diagnostics

The review's `verify_review.py` imports no author code and uses exact integer and rational arithmetic. Ordinary and optimized Python runs produce the same JSON output.

It performs 91,316 checks covering finite-state instances of:

- centered mean exit;
- Green row sums;
- Bellman monotonicity and survival tails;
- unknown-zero-set stability;
- forcing-error accumulation;
- rational interval enclosure;
- fixed-aperture killing;
- compass grid shifts;
- pooled reciprocal reversal;
- noncentered cone exit;
- finite-experiment error budgets and exponents;
- total-variation transition-law calibration.

These checks do not certify the continuum theorem, compactness, apparatus calibration, support smoothing, patch margin, source priority, or editorial significance.

## 10. Source-audit conclusion

The reviewed source is unambiguous, pinned and reproducibly qualified. Version 31 is a real mathematical revision. Its new core has been examined against both the current source and the unreviewed v30 baseline.

The report's negative recommendation is a top-four significance and information-model judgment, not a claim that the latest branch is stale, that v31 merely renames v30, or that the hosted exact-source package failed.
