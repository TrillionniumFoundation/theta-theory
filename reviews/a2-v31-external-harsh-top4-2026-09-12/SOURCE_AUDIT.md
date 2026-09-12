# A2 v31 review: source and execution audit

## Immutable object

Repository: `TrillionniumFoundation/theta-theory`.
Author branch: `revision/a2-v31-native-complete-build-top4-2026-09-12`.
Source commit: `e1f6304f6069869ac323e7d1a634a619faa4bc32`.
Source tree: `d01225c3db774300fc6f97075d25732be534cc04`.
Prior review head: `3825654904d396c4fd90b7965ff2a1b3e8197c83`.
Review date: September 12, 2026.

The author-branch head was checked twice and remained the source commit above. The other v31 branch, `revision/a2-v31-integrated-native-submission-top4-2026-09-12`, pointed to the old v30 review head during discovery. The authenticated comparison from that prior review head to the reviewed source is ahead by two commits, behind by zero, and has five changed paths with no deleted files. This report is about the pinned source, not a moving branch name.

## Direct source readings

The report's source key gives the paths. Full text was read, using additional source-line requests where a response was truncated, for S2-S14, S16-S17, the workflow and build script in S19, and both README entries in S20. The adaptive section was read through its commit patch and a final source-line request. S13 is the complete *input-list file*, not a complete reading of all 36 files which it includes. Selected portions of the earlier v30 report S15 were read for its findings and final dispositions; it is not adopted as outside certification.

In particular the present review newly concentrates on the vector Gaussian chapter, the explicit Poisson deficiency kernels, count/endpoint scales, physical calibration and global estimation, and two active appendix modules. It is not merely a review of the five-file v31 delta.

Selected authenticated Git blob identities returned with the direct readings:

| Source | Git blob SHA |
|---|---|
| `article/17_adaptive_experiments_v31.tex` | `a3864877e478297153efc6f2779e188cc819bcbd` |
| `article/17a_measurable_physical_coupling_v31.tex` | `93eddb2d5b383c1f31a8190552080ef8fa8602d9` |
| `article/18a_vector_boundary_information_v26.tex` | `352994ee96dec59bcc780bfa5ed6eace46b2025e` |
| `article/18c1_endpoint_time_deficiency_v25.tex` | `e03e7eb7e450e6c467f898444d8b72b5fddfd093` |
| `article/18c_full_endpoint_time_information_v26.tex` | `66aa7c911961b2f9b16c1d2d8cad292c19ba5c66` |
| `article/18d_count_endpoint_multirate_v23.tex` | `04637efc790ace6dba7c9128b89d7f13c4cbb985` |
| `article/18f_domination_and_position_comparison_v27.tex` | `97b115829b5b770c856596bb7c86f3d769483ced` |
| `article/25a_common_observables_v25.tex` | `82df03f99c1d6ac322161381e063d2f107f048ed` |
| `article/23f_single_offset_law_inverse_v26.tex` | `35f538eea4415951d1572cd9db76fdff429afa0a` |
| `article/01_introduction_v27.tex` | `14e5fe4a23f833c6caa581bbe055d0efe73650b6` |
| `article/99_auxiliary_compendium_v19.tex` | `a596f344cd660eeaacc8e4e3eb21a0cb39610a9e` |
| `article/65_envelope_minimax.tex` | `be7952808b26900ffa069c6d3788ca19d0fa1d86` |
| `article/70_comparison.tex` | `1f5e98f69ab12b0c850f81c592a068a2ca921857` |
| `tools/build_submission.py` | `233b6f37ff4912b99793460634983ac9b8da379b` |
| `.github/workflows/a2-v31-native-build.yml` (repository-relative) | `81cde3462d9dd78cb1f6365af9c5ce61a05a3cf8` |

These are connector-returned Git object identities. They are not a claim that the entire manuscript was locally downloaded and independently rehashed.

## Direct repository execution evidence

For source SHA `e1f6304f6069869ac323e7d1a634a619faa4bc32`:

- Actions run: `34695581681`, `A2 v31 complete native submission`.
- Created: `2026-09-12T13:08:16Z`; updated: `2026-09-12T13:08:19Z`.
- Run conclusion: `failure`.
- Job: `103558378093`, `native-build`, conclusion `failure`.
- Job steps: `[]`; runner ID: `0`; runner name: empty.
- Artifact collection: `total_count=0`, `artifacts=[]`.

The build did not execute in that run. No service-level reason is inferred. No LaTeX compilation error was established from these observations. The source commit itself expressly does not assert full-build success. Earlier companion/fixture build claims in the v29 README remain inherited claims, not new v31 execution.

## Independent diagnostics actually executed

The accompanying standard-library script was run locally as:

```sh
python3 independent_checks.py > independent_checks_results.json
python3 -O independent_checks.py > independent_checks_results_optimized.json
cmp independent_checks_results.json independent_checks_results_optimized.json
```

Both final runs exited successfully; the outputs were byte-identical. Only one copy of that output is committed. Checks use explicit exceptions, not removable Python assertions.

Final local SHA-256 identities:

- Script: `22052732750fb0d3b2438a6cdbd6a61a866fb986f1aeed5c20b19b825e4b0dda`.
- Output: `17d86e7040c7253e935b70a3f92094a7a08305a203df5cbee8b8ab26611f1fdb`.

The checks cover three finite overlap/residual couplings (including overlap zero and one), strict TV contraction under a noninjective map, 50 exact rank-one density identities using a nonsymmetric action and both signed anchors, exact Laurent-integral score/collar identities, and twelve rational moving-ceiling examples including the fixed residual-time face.

During diagnostic development an initially guessed bound `k*intensity_error <= 12` failed in the *reviewer's toy model*, whose negative-shift limit is 17. The final script uses the analytically valid bound 20: for negative shift the bound is below 17, for zero shift it is 4, and for positive shift it is below 8 at the tested sizes. This corrected diagnostic-only constant was not a counterexample to the manuscript, which uses an unspecified uniform constant. The final outputs above belong to the corrected, executed script.

The triangular example's normalized common-bulk laws are identical. Its successful check therefore does not verify the general product-bulk estimate. No Monte Carlo experiment or finite check is represented as a proof for the nonlinear billiard family.

## Boundaries of the assessment

Not performed in this round: full local materialization and recursive byte audit of the entire TeX graph; native compilation of the main or companion; manuscript PDF inspection; all-page rendering or typography checks; a line-by-line rederivation of every forward/differentiated-operator estimate, signed contact recursion, analytic continuation/gluing/lattice theorem or all 36 auxiliary inputs; independent rerunning of every inherited author diagnostic; a complete novelty/priority audit of all cited literature.

In particular, the geometric inverse and modulus used by the global estimator remain dependencies, not newly certified conclusions of this statistical construction review. Prior T1/C1 dispositions are retained because no new contrary evidence was established, not because every dependency was reread here.

External sources L1-L3 were checked through primary arXiv HTML or abstract pages. No PDF was inspected. The Finamore-Leguil comparison is tied to version 1 and does not assert later publication status. The comparison does not assert an implication between enriched spectral data and A2's signed channel laws.

## Write scope

The review is an additive package under `reviews/a2-v31-external-harsh-top4-2026-09-12/`, based on the exact reviewed source. It introduces a report, this audit, the independent diagnostic script and its output. It does not revise the manuscript, merge into main, delete historical work, or change repository permissions or protections.
