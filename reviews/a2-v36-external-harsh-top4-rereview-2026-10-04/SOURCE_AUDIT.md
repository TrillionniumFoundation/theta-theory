# Source and qualification audit for the external A2 v36 rereview

## 1. Reviewed object

Repository: `TrillionniumFoundation/theta-theory`  
Manuscript: Qian Qi, *Scalar collision laws and recognition of periodic dispersing billiards*  
Reviewed directory: `papers/A2-v36-stationary-boundary`

The reviewed source is identified by Git objects rather than branch chronology:

- revision branch: `revision/a2-v36-stationary-boundary-2026-10-04`;
- referee-copy alias: `revision/a2-v36-referee-copy-2026-10-04`;
- commit: `2559749a038fd2b5ec46d7cc74fdb4bd844b266a`;
- repository tree: `46ad6437731b81ffe439c48fe9ede8b2fbc1d194`;
- active core tree: `18974801d85e6d5760adb71d9ec15fa7da8ede4f`;
- commit title: `Revise A2 with rare pooled queries and unknown-scale reconstruction`.

Both revision names resolved to this same commit. No A2 revision branch later than v36 was found when the review branch was created.

The review branch

`review/a2-v36-external-harsh-top4-rereview-2026-10-04`

was created directly from the reviewed commit. It adds files only under

`reviews/a2-v36-external-harsh-top4-rereview-2026-10-04/`.

No author source, workflow, previous review, retained paper directory or unrelated project is modified.

## 2. Revision chronology

The parent of the v36 author commit is the final v35 external-review head

`985d798e172d38c0a9df2a068fe414b2fd13bcbc`.

That report reviewed the canonical v35 stationary author source

`70c055e1ff090d58ecd61a5644e0fa62a7766f13`.

The v36 `SOURCE_PINS.json` records the following preserved source trees:

| Object | Tree |
|---|---|
| reviewed v35 manuscript | `80780f2590aec6d471985835b1b334774b23675f` |
| controlling v35 review | `2abfbf4ce4d99884c0107bf0caabcf5e70608584` |
| retained v34 manuscript | `66f504938686e4b4920cdf250a92644bd1eae1d9` |

The source chronology is therefore unambiguous: v36 is based on the completed v35 report, not on the earlier divergent v35 footprint sibling.

## 3. Active source inspected

The primary inputs are:

- `main.tex`;
- `references.tex`;
- `core/00_setting.tex`;
- `core/00a_localized_results.tex`;
- `core/00b_resource_overview.tex`;
- `core/00c_stationary_overview.tex`;
- `core/00d_self_calibration_overview.tex`;
- `core/00e_stationary_overview.tex`;
- `core/01_local_queries.tex`;
- `core/02_adaptive_boundary.tex`;
- `core/03_period_recognition.tex`;
- `core/04_information_bound.tex`;
- `core/05_comparison.tex`;
- `core/06_finite_precision.tex`;
- `core/07_sequential_gauge.tex`;
- `core/08_calibration_resolution.tex`;
- `core/09_stationary_jitter.tex`;
- `core/10_unknown_footprint.tex`;
- `core/11_stationary_information.tex`;
- `core/12_rare_stationary.tex`;
- `core/13_unknown_scale.tex`.

The review also inspected:

- `README.md`;
- `RESPONSE_TO_REFEREES.md`;
- `PROOF_LEDGER.md`;
- `HISTORICAL_DERIVATION_AUDIT.md`;
- `LITERATURE_AUDIT.md`;
- `SUBMISSION_MAP.md`;
- `SOURCE_PINS.json`;
- `tools/verify_v36.py`;
- `tools/test_contract_v36.py`;
- `tools/validate_v36.py`;
- `.github/workflows/a2-v36-verify.yml`;
- the complete v35 report and its source audit;
- the exact-SHA workflow run and uploaded receipt.

## 4. Mathematical deltas confirmed

### 4.1 Rare pooled boundary query

The new Section 4 replaces estimation of a small signed reciprocal difference by a one-sided event. Fixed coarse normal data select at most two outward compass candidates. At an exterior target a true maximizing candidate has exactly zero collision probability; at inner depth `e` every selected candidate has probability at least a constant times `e^(gamma+3/2)`. A conjunction of finite batches therefore has query cost

`O(e^-(gamma+3/2) log(1/epsilon))`.

With the retained angular interpolation, this gives the attempted-bit exponent

`((gamma+3/2)s+1)/(s-2)`.

### 4.2 Unknown homothety ratio

The new Section 5 treats physical footprints `A` and `rA`, where only fixed bounds on `r>1` are supplied.

The direct route measures

`Phi_C = integral_E F_1 = t W(C)/2`

from pooled forward bits. If `P_1=C+Q`, `P_2=C+rQ` and `D=P_2-P_1`, then

`a=(W(P_1)-2 Phi_C/t)/W(D)`, `r=1+a^-1`, `Q=aD`, and `C=P_1-aD`.

The denominator is uniformly separated from zero by the footprint inball and scale gap.

An independent route uses only reciprocal differences. The occupation component mass is the obstacle area. A finite killed-walk adjoint estimates that mass, and the mixed-area quadratic selects the unique physical smaller root.

### 4.3 Resource accounting

The finite theorem charges the `O(nu^-2)` attempts and center occurrences used by the scalar normalization. It also bounds the binary description length of nominal centers, setting labels and repetition counts. Physical manufacture, travel, metrology and arithmetic running time remain explicitly outside that measure.

### 4.4 Source-delivery repair

Unlike the reviewed v35 branch, the v36 branch contains its validator, diagnostics, contract tests and source manifest. The exact-head workflow runs all of them, builds the primary, writes a receipt and uploads success or failure evidence.

## 5. Author exact-source qualification

The hosted workflow is

`.github/workflows/a2-v36-verify.yml`.

The exact reviewed-head run is:

- run ID: `37180013120`;
- head SHA: `2559749a038fd2b5ec46d7cc74fdb4bd844b266a`;
- status: `completed`;
- conclusion: `success`.

Every job step succeeded:

1. exact triggering-SHA checkout;
2. build-environment installation;
3. source and finite-diagnostic qualification;
4. evidence binding;
5. artifact upload.

The uploaded artifact is:

- artifact ID: `11294633094`;
- name: `A2-v36-2559749a038fd2b5ec46d7cc74fdb4bd844b266a-1`;
- digest: `sha256:afa632c67d3529454b3d218d3e5d7b37ee073310754aecd66fd07037b6a593ee`.

The artifact was downloaded and its receipt inspected. The receipt records:

- `status: passed`;
- `exact_commit_qualified: true`;
- 571,613 mathematical finite checks;
- 66 validation-contract checks;
- ordinary/optimized equality for both programs;
- a 48-page primary;
- no final TeX diagnostics;
- exact source archives and hashes;
- retention of all 117 reviewed labels;
- byte-identical preservation of all 33 reviewed proof bodies;
- 46 current formal blocks and 43 current proof bodies.

The primary PDF SHA-256 is

`65f9846c4d32e147dad944c8e9690ec3afb232a3266ae706d0f304cd4dfcf200`.

The journal-source ZIP SHA-256 is

`968a549ac44ed13285dcfe874e592f1cf137faa108321328e5a674f2b30f7ee5`.

This source delivery is adequate for review. Compilation and finite checks remain distinct from proof certification.

## 6. Independent diagnostics

The review's `verify_review.py` imports no author module and uses only the Python standard library. It was executed under ordinary Python and `python -O`; the output files were byte-identical with SHA-256

`f2da54a08b67b3282108f7b9237a8323433b0e01ebf2fb7fb805f2f9c5c35817`.

It records 515,081 successful checks. Principal groups include:

| Group | Checks |
|---|---:|
| compass unit/normal/candidate geometry | 19,768 |
| rare exterior support-plane cases | 10,800 |
| rare interior witness cases | 1,944 |
| direct width/scale/support identities | 460,800 |
| mixed-area root and support recovery | 15,000 |
| disk scale-nesting models | 5,120 |
| killed-adjoint identities | 96 |
| binary information-range inequalities | 784 |
| signed-kernel moments | 7 |
| exponent identities | 182 |
| scaled-density algebra | 360 |
| parallel-area controls | 60 |

The checks exercise:

- retention of support-maximizing compass candidates;
- exterior-zero support-plane inequalities;
- interior free starts and collision witnesses;
- translation-invariant coordinate-width recovery;
- direct and mixed-area scale formulas;
- rejection of the nonphysical larger quadratic root;
- finite symmetric killed-chain adjoint identities;
- binary mutual-information range bounds;
- the new and retained exponent calculations.

They do not certify:

- the continuum cap-mass lemma;
- the uniform coarse-normal construction;
- the complete adaptive statistical experiment;
- a physical apparatus;
- the TeX build;
- every inherited theorem;
- the editorial recommendation.

## 7. Scope and limitations of the audit

This was a targeted rereview at the requested top-four benchmark. It concentrated on:

1. whether v36 actually answers the v35 rate, calibration, accounting and source-delivery objections;
2. whether the one-sided rare query is valid for the original pooled sensor;
3. whether the direct and area-normalized scale inverses are algebraically and geometrically coherent;
4. whether the finite theorem charges its additional observations and controls;
5. whether the corrected package reaches the requested editorial threshold.

The review did not formally verify the continuum manuscript or repeat every historical proof. No physical experiment was executed. The literature audit was focused rather than exhaustive.

## 8. Audit conclusion

The reviewed source is reproducibly pinned and exact-head qualified. Version 36 is a real mathematical revision based on the latest completed report. The new rare-query and unknown-ratio arguments are active in the primary and not unattached notes.

No fatal counterexample was found in the new core. The remaining rejection in `REFEREE_REPORT.md` is a top-four significance and information-model judgment, not a claim that the v36 delivery is merely a renamed source, fails to build, or contains a known false central theorem.
