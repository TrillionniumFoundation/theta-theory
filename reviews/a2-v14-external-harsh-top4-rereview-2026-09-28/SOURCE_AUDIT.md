# Source audit for the external A2 v14 rereview

## 1. Reviewed object

Repository: `TrillionniumFoundation/theta-theory`  
Reviewed manuscript: Qian Qi, *Nonlinear boundary laws and two-contact rigidity in dispersing billiards*  
Reviewed directory: `papers/A2-v14-relative-observability-normal-form`

The reviewed revision is identified by Git object, not by branch-name chronology:

- commit: `65b7286080ffae0c4bf8e5d5112fe42f08d82f21`;
- tree: `9c7f29885c4681262de57b7768c33139057cd028`;
- commit date: 28 September 2026;
- commit title: `A2 v14: prove physical normal-form comparison and joint area-jet observability`.

At the time of review, both

- `revision/a2-v14-relative-observability-normal-form-2026-09-28`, and
- `revision/a2-v14-referee-copy-2026-09-28`

resolved to that same commit. No later A2 revision branch was found.

The review branch

`review/a2-v14-external-harsh-top4-rereview-2026-09-28`

was created directly from the reviewed commit. The review adds files only under

`reviews/a2-v14-external-harsh-top4-rereview-2026-09-28/`.

No manuscript source, prior review directory, revision branch, or unrelated paper was edited by this review.

## 2. Frozen prior source and report chain

The v14 tree contains the exact reviewed v13 native manuscript at

`papers/A2-v14-relative-observability-normal-form/history/v13-reviewed`

with tree

`ee946ef91770778839f15c8c35416d401e99ea1c`.

This agrees with the v14 source pins and with the v13 source identity used by the prior reports. The v14 history directory also contains:

- `v13-review-2026-09-10.md`;
- `v13-normal-form-benchmark-2026-09-10.md`;
- `v13-review-2026-09-28.md`.

The latest v13 report is preserved byte-for-byte at blob

`98ce74cd86f0d157cf8dfa3159687bcbd7051ac9`.

The source chronology used in this rereview is therefore:

1. v13 author source `0e54099f079232df233316ae6fe7986fc51b7ea1`;
2. v13 native tree `ee946ef91770778839f15c8c35416d401e99ea1c`;
3. latest v13 review commit `a02d58d2b77e3337f001cf13676c5ff70e1ba97c`;
4. v14 author commit `65b7286080ffae0c4bf8e5d5112fe42f08d82f21`.

The 28 September v13 canonical branch was an alias of the 10 September mathematical source. Version 14 is not such an alias: it contains new active mathematical inputs and a new author commit.

## 3. Files inspected in detail

The rereview read the following current v14 files:

- `main.tex`;
- `article/01_introduction.tex`;
- `article/01a_relative_observability.tex`;
- `article/16_normal_form_comparison.tex`;
- `article/24_physical_image.tex`;
- `article/29_two_flight_benchmark.tex`;
- `article/31_regular_observability.tex`;
- `RESPONSE_TO_REFEREES.md`;
- `PROOF_LEDGER.md`;
- `HISTORICAL_DERIVATION_AUDIT.md`;
- `LITERATURE_VERIFICATION.md`;
- `README.md`;
- `REVISION_STATUS.md`;
- `SOURCE_PINS.json`;
- `VERIFICATION.json`;
- `tools/verify_v14.py`;
- `.github/workflows/a2-v14-verify.yml`.

The rereview also read the retained v13 reports and normal-form benchmark listed above. The new sections were checked against the retained support-function realization and two-flight inverse because those older results are dependencies of the v14 unknown-area theorem.

## 4. Mathematical deltas confirmed

The v14 commit makes the following substantive additions.

### 4.1 Corrected finite-family statement

The abstract no longer says that finite dimension alone implies positive-window observability. The new regular-rank theorem identifies the exact local tangent hypothesis, and the manuscript includes the remote-obstacle zero-rank counterexample.

### 4.2 Analytic normal-form comparator

The new Section 16 contains:

- the mixed-boundary fixed-point equation;
- the exact normalized mixed derivative;
- fixed-box analytic estimates;
- the physical endpoint projection identity;
- the exact origin determinant and reference normalization;
- the product/action limits;
- a nonconstant canonical-shear example;
- identification with the half-line determinant amplitudes;
- an explicit statement of what remains special to the smooth physical theorem.

### 4.3 Unknown-area physical observation

The new Section 31 contains:

- exact-germ versus finite-observation normalization conventions;
- the regular tangent-rank criterion;
- a constant-rank observable quotient;
- a free-area extension of the physical support family;
- a `2M-1` positive two-flight window coordinate theorem;
- confidence and fixed-dimensional minimax risk bounds.

These additions are active inputs of `main.tex`; they are not unattached notes.

## 5. Independent finite diagnostics

The review's `verify_review.py` imports no author module and uses exact rational arithmetic. It checks only finite algebra in the new v14 arguments:

| Group | Checks |
|---|---:|
| shared-intercept window matrix | 60 |
| normal-form mixed derivative | 25 |
| physical projection/shear example | 480 |
| free-area direction | 19 |
| **Total** | **584** |

The checks cover determinant identities and scaling, a singular repeated-node control, the exact implicit derivative formula, the canonical two-form numerator and projected flux, and the sign of the free-area support direction at the disk.

They do not verify the global complex estimates, billiard clearance, source preservation, statistical measurability, retained profile theory, or any journal-level significance judgment.

## 6. Author verification and CI status

The author file `VERIFICATION.json` carefully limits its local claim to:

- 1,588 finite exact algebra checks in normal and optimized Python;
- an isolated eight-page typesetting harness for the new arguments;
- no claimed full-manuscript build in that file.

The exact-source workflow is

`.github/workflows/a2-v14-verify.yml`.

The relevant GitHub Actions run is:

- run ID: `36379170430`;
- head SHA: `65b7286080ffae0c4bf8e5d5112fe42f08d82f21`;
- workflow: `A2 v14 exact-source verification`;
- status at final review check: `queued`;
- conclusion at final review check: `null`.

Accordingly, this audit does not convert the isolated new-section build into a successful full-manuscript build. The queued state is reported as a reproducibility limitation, not as evidence that the mathematics is false.

## 7. Limits of the audit

This was a targeted top-four rereview, not a full formal verification of every inherited statement in a manuscript exceeding one hundred pages. The rereview concentrated on:

1. whether the prior concrete objections were actually answered;
2. whether the new normal-form and physical-projection calculations are coherent;
3. whether the area/contact-jet family is genuinely physical;
4. whether the shared-intercept window design has the claimed rank;
5. whether the corrected package reaches the requested editorial benchmark.

No exhaustive literature or priority search was performed. The cited normal-form comparison was checked at the theorem/mechanism level already frozen in the prior benchmark. No full TeX build was independently completed. No claim is made that the finite diagnostic script is a proof certificate.

## 8. Audit conclusion

The reviewed object is unambiguous and reproducibly pinned. Version 14 is a real mathematical revision and preserves the exact prior source and reports. The new review branch is isolated from the author branches.

The prior quantifier, comparator, normalization, and chronology objections are substantively closed. The remaining negative recommendation in `REFEREE_REPORT.md` is primarily a top-four significance and architecture judgment, not a claim that v14 merely renamed v13 or that the newly audited formulas contain a known fatal error.
