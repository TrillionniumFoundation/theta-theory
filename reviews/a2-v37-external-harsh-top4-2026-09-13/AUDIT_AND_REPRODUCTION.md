# A2 v37: source coverage, evidence, and reproduction ledger

Review date: September 13, 2026. Read this with [REFEREE_REPORT.md](REFEREE_REPORT.md).

## 1. Frozen object and citation convention

All manuscript source links in this ledger resolve to submission commit **`6c311aa389e3af833f06f14ae98de7bfc28c1327`**, not to a moving branch. The Git tree is `c7285e6882fa0b4c09922ca4f4a9c63b402ac1af`. The native mathematical source was introduced by `b0c21cd799bbe4d96bab4a7e1e369d5d7152b294`; the later commit supplies further evidence and documentation. The fixed manuscript root is `papers/A2-v17-boundary-information-coarsening/`.

The report uses source keys rather than PDF page numbers because the complete native PDF was not built or inspected in this review. A positive assessment is restricted to the arguments actually examined. A cited dependency is not automatically a freshly verified theorem.

## 2. Primary repository sources and coverage

**[S0] Version selection and comparison.** The current author branch was read through GitHub, its exact ref was resolved, and the review-history comparison was checked. [Submission commit](https://github.com/TrillionniumFoundation/theta-theory/commit/6c311aa389e3af833f06f14ae98de7bfc28c1327). [Comparison to the preceding review commit](https://github.com/TrillionniumFoundation/theta-theory/compare/01e772030042ffde9df125c0d40401aee2aabd17...6c311aa389e3af833f06f14ae98de7bfc28c1327). Result: two commits ahead, no commits behind, 19 changed paths. No newest-PR heuristic was used as a substitute for the actual manuscript branch.

**[S1] Submission navigation, entry, and author execution claims.** [Root README](https://github.com/TrillionniumFoundation/theta-theory/blob/6c311aa389e3af833f06f14ae98de7bfc28c1327/README.md); [paper README](https://github.com/TrillionniumFoundation/theta-theory/blob/6c311aa389e3af833f06f14ae98de7bfc28c1327/papers/A2-v17-boundary-information-coarsening/README.md); [main.tex](https://github.com/TrillionniumFoundation/theta-theory/blob/6c311aa389e3af833f06f14ae98de7bfc28c1327/papers/A2-v17-boundary-information-coarsening/main.tex); [response](https://github.com/TrillionniumFoundation/theta-theory/blob/6c311aa389e3af833f06f14ae98de7bfc28c1327/papers/A2-v17-boundary-information-coarsening/RESPONSE_TO_REFEREE_V37.md); [verification ledger](https://github.com/TrillionniumFoundation/theta-theory/blob/6c311aa389e3af833f06f14ae98de7bfc28c1327/papers/A2-v17-boundary-information-coarsening/VERIFICATION_V37.md). These were read directly. Main Git blob: `c67badf42e0e6d1c30c73a54c19918ffe7508621`. The author's companion execution, eight diagnostic families, and companion PDF inspection remain author-reported; this referee did not rerun that suite or retrieve the earlier conversation attachment.

**[S2] Single-offset inverse and the edited E2 theorem.** [23f_single_offset_law_inverse_v26.tex](https://github.com/TrillionniumFoundation/theta-theory/blob/6c311aa389e3af833f06f14ae98de7bfc28c1327/papers/A2-v17-boundary-information-coarsening/article/23f_single_offset_law_inverse_v26.tex). Entire chapter examined, including stability, finite-flight inversion, and the revised full-table statement and proof. Blob: `63ed36efd417cd23e6f869952627719de00e6ef7`.

**[S3] Signed contact inverse.** [23a_signed_endpoint_rigidity_v27.tex](https://github.com/TrillionniumFoundation/theta-theory/blob/6c311aa389e3af833f06f14ae98de7bfc28c1327/papers/A2-v17-boundary-information-coarsening/article/23a_signed_endpoint_rigidity_v27.tex). Entire chapter obtained in contiguous ranges and examined: weighted inverse, envelope, smooth finite-jet factorization, homogeneous isolation, multiplicities, tangent isomorphism, and completion. Blob: `0285c90309b8ab88d1ce1ecf8d492ea6d71f268e`.

**[S4] Metric-free lattice recovery.** [23d_rank_two_lattice_recovery_v24.tex](https://github.com/TrillionniumFoundation/theta-theory/blob/6c311aa389e3af833f06f14ae98de7bfc28c1327/papers/A2-v17-boundary-information-coarsening/article/23d_rank_two_lattice_recovery_v24.tex). Entire chapter examined, particularly the distinction between lattice determination and full-table propagation. Blob: `5e34a7c034ee8a5de0ae915a2b4c622f0f042b2c`. The full intrinsic-gluing and finite-signature-stability chapters are dependencies, not newly certified in their entirety by this round.

**[S5] Moving-support likelihoods and moments.** [18a_vector_boundary_information_v26.tex](https://github.com/TrillionniumFoundation/theta-theory/blob/6c311aa389e3af833f06f14ae98de7bfc28c1327/papers/A2-v17-boundary-information-coarsening/article/18a_vector_boundary_information_v26.tex), blob `8ff3ce7334954d6544555e9867a12fa805ca5ea0`; [18a2_likelihood_tilting_moments_v34.tex](https://github.com/TrillionniumFoundation/theta-theory/blob/6c311aa389e3af833f06f14ae98de7bfc28c1327/papers/A2-v17-boundary-information-coarsening/article/18a2_likelihood_tilting_moments_v34.tex), blob `b6f74b4d5cbf6e1065af521dc7364dab98445b38`. Both were examined, including the tail of the vector chapter containing the original-alternative mean, centered fourth moments, and Hellinger stability. The classical local asymptotic minimax theorem is used as a cited external theorem, not re-proved here.

**[S6] Compact local experiments.** [18a1_compact_experiments_v32.tex](https://github.com/TrillionniumFoundation/theta-theory/blob/6c311aa389e3af833f06f14ae98de7bfc28c1327/papers/A2-v17-boundary-information-coarsening/article/18a1_compact_experiments_v32.tex). Entire chapter examined. Blob: `176e2588344ce0646ed47c09c64f371d6d16a045`. The proof's use of the separate fixed-window reduction is checked at the dependency interface, not a fresh line-by-line audit of every source of that reduction.

**[S7] Count–endpoint multirate experiment.** [18d_count_endpoint_multirate_v32.tex](https://github.com/TrillionniumFoundation/theta-theory/blob/6c311aa389e3af833f06f14ae98de7bfc28c1327/papers/A2-v17-boundary-information-coarsening/article/18d_count_endpoint_multirate_v32.tex). The chapter, including its final cap and finite-transfer paragraphs, was examined. Blob: `6014dec05ec24fe67a2d59062ea94e96d0518f0f`. The stopped-transfer theorem invoked there remains an upstream dependency rather than a complete new audit of the adaptive-experiment chapter.

**[S8] Common observations and global physical estimator.** [25a_common_observables_v25.tex](https://github.com/TrillionniumFoundation/theta-theory/blob/6c311aa389e3af833f06f14ae98de7bfc28c1327/papers/A2-v17-boundary-information-coarsening/article/25a_common_observables_v25.tex), blob `82df03f99c1d6ac322161381e063d2f107f048ed`; [25b_augmented_global_reconstruction_v26.tex](https://github.com/TrillionniumFoundation/theta-theory/blob/6c311aa389e3af833f06f14ae98de7bfc28c1327/papers/A2-v17-boundary-information-coarsening/article/25b_augmented_global_reconstruction_v26.tex). The observation map, localization argument, grid pilot, bounded-test implementation, finite-template proof, caps, and budget-indexed diagonalization were examined. Their use of the relative law and compact inverse modulus is explicit; this is not a new proof of every upstream analytic-class theorem.

**[S9] Principal relative theorem and operator interfaces.** [01c_geometric_setup_v18.tex](https://github.com/TrillionniumFoundation/theta-theory/blob/6c311aa389e3af833f06f14ae98de7bfc28c1327/papers/A2-v17-boundary-information-coarsening/article/01c_geometric_setup_v18.tex), blob `c070f628f3ffbc58b5219ae37e82e0b3aa758847`; [15_operator_comparison.tex](https://github.com/TrillionniumFoundation/theta-theory/blob/6c311aa389e3af833f06f14ae98de7bfc28c1327/papers/A2-v17-boundary-information-coarsening/article/15_operator_comparison.tex), blob `886adb2d68e105723f41f6554eeec59391cab44c`. Both examined. The cofactor, trace-log continuity, and Morse-domain arguments were checked; the complete finite-bridge and differentiated separated-block sources were not independently reconstructed in this round.

**[S10] Exposition and prior-art claims.** [01_introduction_v27.tex](https://github.com/TrillionniumFoundation/theta-theory/blob/6c311aa389e3af833f06f14ae98de7bfc28c1327/papers/A2-v17-boundary-information-coarsening/article/01_introduction_v27.tex), blob `4bf96b3ad9f77c0671a7142e8f4baad3db3f560b`; [references_v25.tex](https://github.com/TrillionniumFoundation/theta-theory/blob/6c311aa389e3af833f06f14ae98de7bfc28c1327/papers/A2-v17-boundary-information-coarsening/v5/references_v25.tex). The introductory theorem summaries and the complete related-work paragraph were checked against the cited primary works below. The bibliography was inspected for the relevant entries; this was not an exhaustive bibliographic or priority search. The direct-position benchmark and the Poisson comparison were examined at the level of the introductory statements, not newly re-proved from their complete chapters.

**[S11] Preceding report.** [v36 referee report](https://github.com/TrillionniumFoundation/theta-theory/blob/01e772030042ffde9df125c0d40401aee2aabd17/reviews/a2-v36-external-harsh-top4-2026-09-13/REFEREE_REPORT.md). The prior dispositions and supporting mathematical discussion used in this review were consulted. The current findings do not rely on counting previous reports as independent journal endorsements.

**[B1] Build driver.** [tools/build_submission.py](https://github.com/TrillionniumFoundation/theta-theory/blob/6c311aa389e3af833f06f14ae98de7bfc28c1327/papers/A2-v17-boundary-information-coarsening/tools/build_submission.py). Entire source read and materialized. Git blob verified locally as `029e9e96537df18a032d36de55e449e262be87c4`, SHA-256 `0bae306311226ea0966eb9fd1ea141ebeb0ffcd8062cccbc5b851aed24cc3184`, 8,388 bytes. The retained [fixture](fixtures/build_submission.py) is byte-identical to this source. It is imported for isolated mocked unit tests, not executed as the native submission builder.

## 3. Independently queried hosted evidence

**[C1]** [Run 34735598451](https://github.com/TrillionniumFoundation/theta-theory/actions/runs/34735598451), [job 103666347616](https://github.com/TrillionniumFoundation/theta-theory/actions/runs/34735598451/job/103666347616). GitHub's authenticated API returned:

```json
{
  "run_id": 34735598451,
  "head_sha": "b0c21cd799bbe4d96bab4a7e1e369d5d7152b294",
  "status": "completed",
  "conclusion": "failure",
  "job_id": 103666347616,
  "steps": [],
  "runner_id": 0,
  "runner_name": "",
  "artifact_total_count": 0,
  "artifacts": []
}
```

This is a selected-field transcription of independently read run, jobs, and artifacts responses, not an assertion that it is GitHub's raw combined JSON response. The reason for failure was not established. No evidence of TeX execution was inferred. This ledger does not claim that every workflow run on every repository branch was inspected.

## 4. Primary external literature checked

**[L1]** J. De Simoi, V. Kaloshin, M. Leguil, *Marked Length Spectral determination of analytic chaotic billiards with axial symmetries*, [arXiv:1905.00890v4](https://arxiv.org/abs/1905.00890v4), related publication DOI `10.1007/s00222-023-01191-8`. The arXiv abstract and publication metadata were checked for the stated geometric class and hypotheses. This review does not purport to re-referee that paper.

**[L2]** D. Finamore, M. Leguil, *A CAT(0)-approach to the marked length spectral rigidity of Sinai billiards*, [arXiv:2510.18983v1](https://arxiv.org/abs/2510.18983v1), October 21, 2025. The version history, abstract, and [HTML introduction/Theorem A](https://arxiv.org/html/2510.18983v1) were consulted. The comparison retains the distinction between enriched and ordinary marked length spectra. The checked arXiv record listed v1; no later version or new journal publication is asserted.

**[L3]** A. Meister, M. Reiß, *Asymptotic Equivalence for Nonparametric Regression with Non-Regular Errors*, [arXiv:1101.5248v1](https://arxiv.org/abs/1101.5248v1). The abstract was checked for the nonregular regression to Poisson-boundary equivalence. The report uses it only for that narrow precedent, not for an unproved transfer to the present billiard model.

These sources were consulted on September 13, 2026. The public literature comparison is bounded, not an exhaustive novelty certificate. No PDF was analyzed in the external-literature step; the accessible HTML/abstract sources were used.

## 5. Fresh diagnostics and exact reproduction

**[D1]** [reviewer_checks.py](reviewer_checks.py), [ordinary JSON](evidence/diagnostics.normal.json), [optimized JSON](evidence/diagnostics.optimized.json), [execution ledger](evidence/execution.json).

From this review directory, using Python 3.10 or later and the standard library:

```sh
python reviewer_checks.py > /tmp/a2-v37-review.normal.json
python -O reviewer_checks.py > /tmp/a2-v37-review.optimized.json
cmp /tmp/a2-v37-review.normal.json /tmp/a2-v37-review.optimized.json
```

The included driver fixture must retain its recorded Git blob. Alternatively, `--driver /path/to/the/pinned/tools/build_submission.py` selects another copy; the script rejects it unless its bytes match that same blob. This protects the provenance test itself from silently testing a later driver version.

| Family | Final observed result | What it does not certify |
|---|---|---|
| Signed density | 648 exact-rational density pairs passed | Geometric realization, sample density estimation, derivative stability on all classes |
| Last-jet blocks | 48 geometry/order pairs passed; maximum determinant discrepancy `2.1E-74` at 75-digit working precision | Infinite-dimensional nonlinear inversion or uniform-in-order conditioning |
| Lattice/gauge | Determinant-six marked basis; four-vertex rooted propagation; an uncovered fifth vertex detected | Analytic signature matching or billiard admissibility |
| Pilot grid | 432 exact two-type success-time combinations passed | Rare-event mass lower bound or simulated physical acquisition |
| Count information | 25 geometric-affinity comparisons and 27 negative-binomial derivative cases passed | A numerical proof of a central limit theorem or deficiency convergence |
| Compatible rates | Five integer-budget examples with the displayed error budgets decreasing | Necessity or optimality of the sufficient rate hypotheses |
| Provenance | Matched control plus two expected weaknesses reproduced | A successful native build, source tampering in an actual author run, or a mathematical counterexample |

The finalized ordinary and optimized commands and `cmp` each exited zero. Both outputs have SHA-256 `4c322709006b0b3e626891bd53847cf5f08d9a0a3ca9b3a61b2fc5dd992b6cb1`; stderr was empty. Python version: 3.13.5. Reviewer-script SHA-256: `fb85440f84f052dc6f4e1ff45be1279d4fb508c9bd480b359f5e8cdb9b2d4a66`.

The provenance fixtures mock both external processes and create only temporary mock products. They do not establish that the ordinary clean-build path spontaneously creates divergent inputs. They establish that the inspected metadata routine does not reject or faithfully describe the tested divergent state, and does not reject a missing recorder. All mock products are discarded; no mock PDF is supplied as manuscript evidence. No repository source is changed by these fixtures.

During development, an initial exact-rational test promoted an integer zero to floating-point arithmetic. That reviewer-harness defect was corrected before the finalized recorded runs. It is not reported as a manuscript defect. The execution ledger records this distinction.

## 6. What was not executed

A network clone from the local runtime failed at DNS resolution, so the local materialized files were not a complete checkout. GitHub source reads succeeded through the authorized connector. The one build-driver file used in executable fixtures was separately verified by its Git blob, as recorded above.

No native main or companion build and no actual manuscript-PDF inspection was performed by this reviewer. The inherited author diagnostics, nonlinear 64-flight examples, and earlier companion PDF rendering were not replayed here. The following full-checkout procedure is therefore a **future reproduction instruction, not an executed success**:

```sh
git checkout --detach 6c311aa389e3af833f06f14ae98de7bfc28c1327
git rev-parse HEAD
git rev-parse HEAD^{tree}
git status --porcelain=v1
python3 papers/A2-v17-boundary-information-coarsening/tools/build_submission.py \
  --output-dir /tmp/a2-v37-complete-native
```

The output must be outside the manuscript tree. The source should be clean or explicitly frozen as a content-addressed snapshot. The unmodified driver's green status alone is insufficient to close R37-V1; verify actual compilation bytes and recorder coverage independently or correct the driver in a new author revision. Then inspect the real assembled documents and record the coverage honestly. No shortened manuscript or isolated chapter should be substituted for the native entry.
