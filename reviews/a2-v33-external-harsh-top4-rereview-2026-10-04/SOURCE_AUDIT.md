# Source audit for the external A2 v33 rereview

## 1. Frozen reviewed object

Repository: `TrillionniumFoundation/theta-theory`  
Paper: Qian Qi, *Scalar collision laws and recognition of periodic dispersing billiards*  
Paper directory: `papers/A2-v33-finite-precision-sequential`

The review is bound to Git objects rather than branch-name chronology:

- revision branch: `revision/a2-v33-finite-precision-sequential-2026-10-04`;
- referee-copy alias: `revision/a2-v33-referee-copy-2026-10-04`;
- reviewed commit: `245a2bf5d13b72d81ef85b784e9fcb2dd88ca490`;
- reviewed repository tree: `98f56b2e1433701e95f0e01e98d26d6dcada1ed8`;
- native paper tree: `213cecf77265c5ebea98791a99126b9def5d25f0`;
- mathematical checkpoint: `a3c4b12d2d56d67a7569e3b239f0bcea8f546ee3`;
- checkpoint tree: `66f981927db72a2179fb6553e1359b95bcd8260b`.

Both v33 branch names resolved to the same reviewed commit. No later A2 revision branch was present when the review was frozen.

The review branch

`review/a2-v33-external-harsh-top4-rereview-2026-10-04`

was created directly from the reviewed author commit. It adds files only under

`reviews/a2-v33-external-harsh-top4-rereview-2026-10-04/`.

No author source, retained source, old review, workflow, revision branch, or unrelated paper is modified.

## 2. Chronology and retained source

The mathematical checkpoint is based directly on the controlling v32 external-review commit

`058d2b7b773038cfa7e43f7f52a3b79fdc4107f6`.

That review assessed v32 author head

`eeb171d4e00242c9813c10e2124556b2cee480d3`

and its report blob is

`e38199da9ea49227f48b94eef8d04b3ee8da871c`.

The exact v32 paper is retained in v33 at

`retained/v32`

with tree

`2a7d949f43dcb7b84d4a85ef8a4436349f615493`.

The six v32 proof chapters remain active in the v33 primary and have original core tree

`b0655672858cd000e2c6d939f681ec47b35eb716`.

The source pins identify the controlling review, v32 tree, active core tree, all new source SHA-256 values, the workflow digest, and a sixteen-document package. The chronology is internally consistent.

## 3. Files inspected

The targeted rereview inspected:

- `main.tex`;
- `core/00_setting.tex`;
- `core/00b_resource_overview.tex`;
- `core/01_local_queries.tex`;
- `core/02_adaptive_boundary.tex`;
- `core/03_period_recognition.tex`;
- `core/04_information_bound.tex`;
- `core/05_comparison.tex`;
- `core/06_finite_precision.tex`;
- `core/07_sequential_gauge.tex`;
- `core/08_calibration_resolution.tex`;
- `RESPONSE_TO_REFEREES.md`;
- `PROOF_LEDGER.md`;
- `LITERATURE_AUDIT.md`;
- `HISTORICAL_DERIVATION_AUDIT.md`;
- `README.md`;
- `SUBMISSION_MAP.md`;
- `SOURCE_PINS.json`;
- `references.tex`;
- `tools/verify_v33.py`;
- `tools/test_contract_v33.py`;
- `tools/validate_v33.py`;
- `verification/local/receipt.json`;
- `.github/workflows/a2-v33-verify.yml`;
- the complete v32 external report and retained v32 source metadata.

The rereview concentrated on the new resource claims and their dependence on the retained v32 reconstruction chain. It did not re-prove every theorem in all nested historical volumes.

## 4. Mathematical delta from v32

The v33 active additions are:

1. `core/00b_resource_overview.tex`: headline statement of digital, sequential, and calibration resources;
2. `core/06_finite_precision.tex`: dyadic controls, rounded bisection, output descriptions, and a conditional numerical-work estimate;
3. `core/07_sequential_gauge.tex`: explicit laboratory gauge, centered packing, prefix-free stopped-word information bound, and expected-attempt lower bound;
4. `core/08_calibration_resolution.tex`: physical common-response coupling and worst-case position-calibration necessity.

The retained v32 upper bound, deterministic-cap lower bound, period recognition, and active-boundary comparison remain active inputs rather than merely archived history.

## 5. Author evidence

The local receipt records:

- 117,772 new finite diagnostics;
- 36 new validation-contract checks;
- 11,647 retained v32 diagnostics;
- 42 retained v32 contract checks;
- identical ordinary and optimized outputs;
- 4,500 geometric starts in the finite common-response control;
- 224 nominal disagreements, split into 104 solid-entry and 120 swept-exit cases;
- a 21-page primary with no final TeX diagnostics;
- source-content execution, not an authenticated checkout;
- no physical sensor execution;
- no formal proof certificate.

The local receipt appropriately does not claim full-package hosted qualification.

## 6. Exact-SHA hosted qualification

Workflow:

`.github/workflows/a2-v33-verify.yml`

Run:

- run ID: `37165176734`;
- head SHA: `245a2bf5d13b72d81ef85b784e9fcb2dd88ca490`;
- status: `completed`;
- conclusion: `success`.

The single job:

- checked out the exact triggering SHA;
- required current and retained entry points;
- installed the declared build dependencies;
- qualified all sixteen documents at that SHA;
- archived native sources and actual evidence;
- uploaded the exact-source result.

Artifact:

- artifact ID: `11289282263`;
- name: `A2-v33-245a2bf5d13b72d81ef85b784e9fcb2dd88ca490`;
- digest: `sha256:da26ab541a269ad47ea4374e4d7035dfdfdfc595507adf45b81190d08a6fff02`.

The hosted qualification is successful. Compilation and finite checks are evidence of reproducibility, not proof certification.

## 7. Independent diagnostics

The review's `verify_review.py` imports no author module. Normal and optimized Python executions were byte-identical, with output SHA-256

`975719daa340fa7bbdaede120c7886872f25aa435ce963f027ee7961dc69bddb`.

The script performs 1,129,071 checks, including:

- reciprocal collision truth tables;
- exact dyadic compass translations;
- rounded bisection width recurrences and mesh floors;
- command-description logarithmic scaling;
- Steiner-centering and calibration exponent algebra;
- prefix-free Kraft and entropy examples;
- expected stopped-word information inequalities;
- one-dimensional swept-set Hausdorff and separation identities;
- a nonvacuous one-dimensional common-response construction;
- adaptive transcript identity under a shared common response;
- retained bounded-denominator and Hermite covolume arithmetic.

The script does not execute a physical apparatus, certify the continuum common-response lemma, perform an independent TeX build, or establish editorial significance.

## 8. Audit conclusion

The source is unambiguously frozen and follows the latest prior report. The reviewed v32 source is preserved exactly, the v33 mathematical delta is active, and exact-SHA all-volume qualification succeeds.

The new mathematical claims are coherent in the stated adversarial active-sensor model. The negative top-four recommendation in `REFEREE_REPORT.md` is an editorial and information-model assessment, not a claim that v33 is a renamed v32 source, that its delivery failed, or that a fatal counterexample was found.
