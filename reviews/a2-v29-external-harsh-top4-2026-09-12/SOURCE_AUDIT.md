# Source and execution audit — A2 v29 independent review

Date: September 12, 2026. Repository: `TrillionniumFoundation/theta-theory`.

## 1. Immutable target and scope

The author revision selected by the repository branch search was `revision/a2-v29-equivariant-density-stability-top4-2026-09-12` at head `b137f2a92943d5491e0239eee193599eaa3728b8`, tree `e3715007ef37041f85739f573904607b376cc304`. The preceding review parent is `5f10927a6399ebec0492b7f87b622ec80a4df631`; the mathematical-source commit is `78852f2ccf828385fd45063c1b58c0d474ddf6c5`.

Authenticated repository comparisons were executed. The head is three commits ahead of the review parent, with no divergence and no removed files. The one commit after the mathematical source changes navigation, responses, diagnostics, and execution evidence, not mathematical TeX sources. These comparisons do not constitute execution of a recursive TeX-input audit.

This review adds only its own files below `reviews/a2-v29-external-harsh-top4-2026-09-12/`. It does not revise the manuscript, delete historical sources, merge into main, rerun workflows, or alter repository settings. The review is author-requested and AI-assisted, not a commissioned journal report.

## 2. Sources read

Below, `P` denotes `papers/A2-v17-boundary-information-coarsening/`. All repository files refer to the immutable reviewed head. “Complete” means the module text was read, including through multiple range requests where necessary; it does not mean that every imported theorem was independently re-proved.

| Source | Reading scope | Git blob returned by the repository |
|---|---|---|
| Root `README.md` | Complete navigation | `eda66be0234cc6c5677c60e8e9878887dc13f103` |
| `P/main.tex` | Complete abstract and active input list; no full recursive materialization | `e8cea2c2b136624c61fa3d3c4629965e31321613` |
| `P/RESPONSE_TO_REFEREE_V29.md` | Complete | `05eaae3b0e1b759f7745256601971cab6312ddf0` |
| Prior v28 report in `reviews/a2-v28-external-harsh-top4-2026-09-12/` | Recommendation, C1/T1 calculations, C2, final disposition, and source key; not represented as a complete historical-repository audit | `dbc4994921b47c13cc4d540ed7245cdba7c86be2` |
| `P/article/23f1_equivariant_density_extension_v29.tex` | Complete new extension, proof, quotient, finite jets, witness | `f90531eae71f43486029a7dd042c249627aa22b8` |
| `P/article/01b_observation_hierarchy_v29.tex` | Complete new hierarchy | `9ff3141c19ec00b669667c0a9226138a2698d234` |
| `P/article/23h_global_orientation_quotient_v29.tex` | Complete, including revised stability corollary | `ac9938ee655b8b63f069a0c79c467d227eca5ab1` |
| `P/article/23f_single_offset_law_inverse_v26.tex` | Complete | `35f538eea4415951d1572cd9db76fdff429afa0a` |
| `P/article/23a_signed_endpoint_rigidity_v27.tex` | Complete module through overlapping range reads; its weighted inverse, envelope, finite remainder and last-jet proofs re-examined | `0285c90309b8ab88d1ce1ecf8d492ea6d71f268e` |
| `P/article/23d_rank_two_lattice_recovery_v24.tex` | Complete metric-free holonomy and lattice-recovery module | `5e34a7c034ee8a5de0ae915a2b4c622f0f042b2c` |
| `P/article/23e_signature_stability_v25.tex` | Complete finite-signature, noisy-match, propagation and compact-modulus module | `62a9df01937f97a33d405426842f25e85b1358b0` |
| `P/article/25a_common_observables_v25.tex` | Complete calibration, observable normalization, continuity and test-implementation module | `82df03f99c1d6ac322161381e063d2f107f048ed` |
| `P/article/25b_augmented_global_reconstruction_v26.tex` | Complete separator, finite estimator, charged policy and budget-indexed global consistency module | `4aff42d3fd3dc88a2bb29e8cafef40e224b51615` |
| `P/article/18c1_endpoint_time_deficiency_v25.tex` | Complete conditional layer/bulk estimates and two-sided kernel construction | `e03e7eb7e450e6c467f898444d8b72b5fddfd093` |
| `P/article/18f_domination_and_position_comparison_v27.tex` | First 240 lines: principal domination, observed-type and matched-time arguments; later examples not fully read | `97b115829b5b770c856596bb7c86f3d769483ced` |
| `P/article/01_introduction_v27.tex` | First 220 lines | `14e5fe4a23f833c6caa581bbe055d0efe73650b6` |
| `P/VERIFICATION_V29.md` | Complete execution record; reported builds were not rerun by this reviewer | `e73b1d950b1e647328c9a233b25aec182d0beb6d` |
| `P/tools/check_revision_v29.py` | Complete; independently materialized, blob-verified and executed | `bd27b08638c9ca2d92f77eb848ac69d24f18fd1f` |
| `P/v5/references_v25.tex` | Bibliography content inspected, including primary sources and explicitly labelled private review provenance | No independent local blob calculation recorded |

The underlying intrinsic-gluing and analytic-continuation files were not separately reread in full in this review. Their relevant identities and uses were examined in the active orientation, signed-rigidity and rank-two modules. The original forward relative-law and adaptive-transfer constructions, every LAN or multirate proof, the entire auxiliary compendium, and the companion mathematics were not recertified line by line. Conclusions in the report are correspondingly module-specific and conditional on explicitly identified dependencies.

## 3. Actual diagnostic executions

Execution environment: Python 3.13.5. Only standard-library exact rational arithmetic was used in the two suites. Both use explicit exceptions rather than removable Python assertions.

### Author suite reproduced

The local reproduction of `P/tools/check_revision_v29.py` has 5,945 bytes, the repository Git blob listed above, and SHA-256:

`efa21131f44d3af8a5740f96f78b0c0ae3d3bb4c16819dc3dabaff9446e3a458`.

It was run in ordinary and optimized modes. Both completed successfully, passed 12,443 checks, and produced byte-identical output. The retained reproduction is `author_checks_reproduced.json`; the original script remains available in the inherited manuscript source tree.

### Independent reviewer suite

`independent_checks.py` was separately written and executed. Its SHA-256 is:

`57344b44ad5e6a562996c66d78aaa984b428b8f8dba3c1e33991a95298fc05db`.

Both ordinary and optimized runs completed successfully, passed 5,033 checks, and produced byte-identical output. The retained output is `independent_checks.json`. Its families and exact scope are printed in that file. In particular, the moving-ceiling checks concern a normalized toy model, not an execution of the full billiard asymptotic argument.

Reproduction commands from an authorized checkout of this review branch are:

```sh
P=papers/A2-v17-boundary-information-coarsening
R=reviews/a2-v29-external-harsh-top4-2026-09-12
OUT=$(mktemp -d)
python3 "$P/tools/check_revision_v29.py" > "$OUT/author-normal.json"
python3 -O "$P/tools/check_revision_v29.py" > "$OUT/author-optimized.json"
cmp "$OUT/author-normal.json" "$OUT/author-optimized.json"
python3 "$R/independent_checks.py" > "$OUT/reviewer-normal.json"
python3 -O "$R/independent_checks.py" > "$OUT/reviewer-optimized.json"
cmp "$OUT/reviewer-normal.json" "$OUT/reviewer-optimized.json"
```

The independent output records the Python version, so that field can differ on another interpreter version. Normal-versus-optimized equality on one environment does not depend on suppressing a failed check. Test counts are finite identity counts, not a measure of mathematical theorem coverage.

## 4. Live CI observations and author-reported native evidence

The author-branch Actions run collection returned two runs. Their job collections were separately read from authenticated endpoints. The selected fields are preserved in `ci_observations.json`.

Both jobs completed with conclusion `failure`, empty `steps`, runner ID zero and an empty runner name. Therefore neither inspected hosted job executed source checkout, tests, source auditing or TeX. No infrastructure cause was established. No workflow rerun or administrative change was made.

The author's verification record reports a seven-page native companion PDF with SHA-256 `98dfd9a5a9792edce676d61e7f872c7f29a2e9d401bb37fa0cf6b06bac8b4748`, plus complete encoded logs and an independent ten-page selected-module fixture. This reviewer read the record but did not decode all companion logs, rebuild either native entry, or inspect either PDF. The fixture is not a full native-main build. Its unresolved references to omitted modules are not automatically unresolved references in the complete main.

C2 therefore remains open. The review does not claim a failed TeX compilation; it records the absence of the required successful complete-native verification in the inspected evidence.

## 5. Literature scope

The arXiv abstract and version-metadata pages for `1905.00890`, `2510.18983`, and `1101.5248` were consulted on September 12, 2026. Only the limited comparisons stated in the report are drawn from them. Their full papers were not read or theorem-audited for this review, and no exhaustive novelty search or later publication-status claim is made.

## 6. What this package does not certify

This package is not a full repository checkout, a recursive submission source scanner, a native-main build certificate, a proof-assistant certificate, a full-PDF visual inspection, a proof of arbitrary density realizability, or a journal acceptance decision. The review reports resolved points, outstanding evidence, and the limitations of its own inspection separately. It adds no restriction to an exact theorem merely to preserve a negative verdict.
