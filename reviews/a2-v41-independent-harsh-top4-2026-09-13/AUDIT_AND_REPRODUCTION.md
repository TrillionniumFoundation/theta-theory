# A2 v41: source coverage and independent reproduction ledger

## Frozen submission and review scope

Repository: `TrillionniumFoundation/theta-theory`. Reviewed branch: `revision/a2-v41-complete-native-delivery-2026-09-13`. Reviewed commit: `c730a60bbc8af2a4c6e432813c31dccc897828e7`; tree: `1c626923b2623cadd97450d0a93dbaffd564fe34`; commit time: September 13, 2026, 13:11:58 UTC. The head was re-read before publication and was unchanged. The final branch search for `a2-v4` showed v40 and v41 and no v42–v49.

The complete introduction and proof-architecture changes, the cited bibliography entries, the native entry, the controlling relative-law and jet-inverse proofs, the rerooting proof, the common-observable/global-estimation chapters, and the vector/tilting/compact Gaussian arguments listed below were read from the frozen commit. This is a source-based review with an explicit coverage boundary, not a complete-checkout or typeset-manuscript certification.

No native main or companion compilation was performed by this reviewer. No PDF was retrieved or visually inspected. The complete recursive input closure was not materialized or statically linted. No missing glyph, unresolved reference, page count, or layout defect is asserted without that evidence. The many retained auxiliary chapters, the full companion, and every physical flux, localization, stopped-transfer, Poisson, count–endpoint, global gluing, orientation, signature-stability and minimax dependency were not freshly re-proved. Inherited findings retain their historical status and are not described as new executions.

## Immutable source index

All paths below are fixed to the reviewed commit, including the preceding report inherited in that tree. Line ranges refer to native text, not generated PDF pages. The linked theorem labels are the more robust locators.

**S01 — Identity and deltas.** [Reviewed commit](https://github.com/TrillionniumFoundation/theta-theory/commit/c730a60bbc8af2a4c6e432813c31dccc897828e7); [v40 submission to v41 comparison](https://github.com/TrillionniumFoundation/theta-theory/compare/070aa946fb28001916ad1bbd3503afa5f6cae3b3...c730a60bbc8af2a4c6e432813c31dccc897828e7); [last author commit comparison](https://github.com/TrillionniumFoundation/theta-theory/compare/d7098a403dc3f3b4fd910f64b3cbfe2d12d56ec9...c730a60bbc8af2a4c6e432813c31dccc897828e7). Exact connector comparisons returned three additional commits/eleven paths for the first comparison and one commit/five paths for the second. No additional proof-file changes are inferred.

**S02 — New introduction.** [article/01_introduction_v41.tex](https://github.com/TrillionniumFoundation/theta-theory/blob/c730a60bbc8af2a4c6e432813c31dccc897828e7/papers/A2-v17-boundary-information-coarsening/article/01_introduction_v41.tex), all 385 lines. Blob `94e056a79877b6a9087534a61627ca4838deb775`. Locators: `thm:v26-intro-rigidity`, `thm:v26-intro-physical`, the related-inverse-problems subsection and its Florio–Leguil footnote.

**S03 — Architecture and bibliography.** [article/01d_proof_architecture_v41.tex](https://github.com/TrillionniumFoundation/theta-theory/blob/c730a60bbc8af2a4c6e432813c31dccc897828e7/papers/A2-v17-boundary-information-coarsening/article/01d_proof_architecture_v41.tex), all 76 lines, blob `8272dc991e74b2c33c38a0106a1da088ce6017ab`; [v5/references_v41.tex](https://github.com/TrillionniumFoundation/theta-theory/blob/c730a60bbc8af2a4c6e432813c31dccc897828e7/papers/A2-v17-boundary-information-coarsening/v5/references_v41.tex), cited entries and final bibliography closure, blob `47919210678a16c61ee0cd27ccbad4ff5782cc09`. Bibliographic versions were checked against L1–L4; no claim to verification of every bibliography entry is made.

**S04 — Current navigation.** [Root README](https://github.com/TrillionniumFoundation/theta-theory/blob/c730a60bbc8af2a4c6e432813c31dccc897828e7/README.md), blob `3dea5fd278c24291822aaaa49feb6781d28898fc`; [paper README](https://github.com/TrillionniumFoundation/theta-theory/blob/c730a60bbc8af2a4c6e432813c31dccc897828e7/papers/A2-v17-boundary-information-coarsening/README.md), blob `dd02e43f8ceb40631e87ad4dfcd3b12a76453383`. Both were read in full and explicitly identify v38.

**S05 — Preceding independent report.** [v40 REFEREE_REPORT.md](https://github.com/TrillionniumFoundation/theta-theory/blob/c730a60bbc8af2a4c6e432813c31dccc897828e7/reviews/a2-v40-independent-harsh-top4-2026-09-13/REFEREE_REPORT.md), blob `345b655b1bedf4d088938af67c9154a9d46da032`. The retrieved opening, mathematical discussion, and final delivery/literature/disposition sections establish the outstanding requests and prior coverage. Its own code and execution records were not rerun in this review.

**S06 — Relative half-line law.** [v4/10_boundary_layers.tex](https://github.com/TrillionniumFoundation/theta-theory/blob/c730a60bbc8af2a4c6e432813c31dccc897828e7/papers/A2-v17-boundary-information-coarsening/v4/10_boundary_layers.tex), read through EOF in two chunks, blob `892a88e37a24e591fa525013c41910c791e28e73`. Locators: `lem:v4-halfline`, `thm:v4-factorization`, `thm:v4-law`. Fresh inspection covered weighted decay, trace norm, gluing, determinant comparison, and fixed-domain integration; it did not recursively re-prove every cited earlier finite-flight lemma.

**S07 — Finite smooth-jet inverse.** [article/23a_signed_endpoint_rigidity_v27.tex](https://github.com/TrillionniumFoundation/theta-theory/blob/c730a60bbc8af2a4c6e432813c31dccc897828e7/papers/A2-v17-boundary-information-coarsening/article/23a_signed_endpoint_rigidity_v27.tex), read through EOF in three chunks, blob `0285c90309b8ab88d1ce1ecf8d492ea6d71f268e`. Locators: `lem:v22-weighted-inverse`, `lem:v22-envelope`, `lem:v27-smooth-jet-factorization`, `lem:v22-homogeneous-isolation`, `prop:v22-last-jet-block`, `prop:v22-tangent-jet-isomorphism`.

**S08 — Single-offset density inverse.** [article/23f_single_offset_law_inverse_v26.tex](https://github.com/TrillionniumFoundation/theta-theory/blob/c730a60bbc8af2a4c6e432813c31dccc897828e7/papers/A2-v17-boundary-information-coarsening/article/23f_single_offset_law_inverse_v26.tex), complete chapter, blob `63ed36efd417cd23e6f869952627719de00e6ef7`. Locators: `thm:v26-density-inverse`, `prop:v26-density-stability`, `cor:v26-finite-flight-inverse`, `thm:v26-single-offset-global`.

**S09 — Rerooting.** [article/23b1_signature_rigid_rerooting_v40.tex](https://github.com/TrillionniumFoundation/theta-theory/blob/c730a60bbc8af2a4c6e432813c31dccc897828e7/papers/A2-v17-boundary-information-coarsening/article/23b1_signature_rigid_rerooting_v40.tex), all 66 lines, blob `a658cbed21f80dd1b79b97e0c026b2127833a239`. `lem:v40-signature-rigid-rerooting` and its composition paragraph were directly checked. The referenced complete analytic-signature classification was not freshly reconstructed in full here.

**S10 — Charged observable calibration.** [article/25a_common_observables_v25.tex](https://github.com/TrillionniumFoundation/theta-theory/blob/c730a60bbc8af2a4c6e432813c31dccc897828e7/papers/A2-v17-boundary-information-coarsening/article/25a_common_observables_v25.tex), read through EOF, including the final test-implementation proof, blob `82df03f99c1d6ac322161381e063d2f107f048ed`. Locators: `lem:v25-physical-localization`, `thm:v25-observable-calibration`, `prop:v25-test-implementation` and the common Borel record spaces.

**S11 — Global physical estimator.** [article/25b_augmented_global_reconstruction_v26.tex](https://github.com/TrillionniumFoundation/theta-theory/blob/c730a60bbc8af2a4c6e432813c31dccc897828e7/papers/A2-v17-boundary-information-coarsening/article/25b_augmented_global_reconstruction_v26.tex), complete argument through its final scope paragraph. Locators: `lem:v26-single-offset-separators`, `thm:v26-fixed-order-physical`, `thm:v26-global-physical-reconstruction`. The separately cited compact global modulus and stopped-transfer theorem are dependencies, not newly certified by this chapter-level audit.

**S12 — Vector boundary information.** [article/18a_vector_boundary_information_v26.tex](https://github.com/TrillionniumFoundation/theta-theory/blob/c730a60bbc8af2a4c6e432813c31dccc897828e7/papers/A2-v17-boundary-information-coarsening/article/18a_vector_boundary_information_v26.tex), read through EOF in three chunks, blob `6db9136e31c0e94bc09eddc5f261eab1b25be3ba`. Locators: common-collar equivalence, uniform LAN, finite-likelihood experiments, `thm:v22-vector-boundary-gaussian`, v35-labelled alternative-mean/fourth-moment equations, and `lem:v22-hypersurface-stability`.

**S13 — Compact-experiment upgrade.** [article/18a1_compact_experiments_v32.tex](https://github.com/TrillionniumFoundation/theta-theory/blob/c730a60bbc8af2a4c6e432813c31dccc897828e7/papers/A2-v17-boundary-information-coarsening/article/18a1_compact_experiments_v32.tex), complete chapter, blob `176e2588344ce0646ed47c09c64f371d6d16a045`. Freshly checked: `lem:v32-finite-net`, `thm:v32-compact-vector`. The physical corollary was read, but its earlier fixed-window reduction and transfer dependencies were not exhaustively re-audited.

**S14 — Exact-head build metadata.** [Head-filtered runs](https://api.github.com/repos/TrillionniumFoundation/theta-theory/actions/runs?head_sha=c730a60bbc8af2a4c6e432813c31dccc897828e7&per_page=10); [run](https://github.com/TrillionniumFoundation/theta-theory/actions/runs/34759179999); [jobs API](https://api.github.com/repos/TrillionniumFoundation/theta-theory/actions/runs/34759179999/jobs); [artifacts API](https://api.github.com/repos/TrillionniumFoundation/theta-theory/actions/runs/34759179999/artifacts). These were actual connector reads. The metadata extraction below is not a TeX log.

**S15 — Likelihood tilting and original-law moments.** [article/18a2_likelihood_tilting_moments_v34.tex](https://github.com/TrillionniumFoundation/theta-theory/blob/c730a60bbc8af2a4c6e432813c31dccc897828e7/papers/A2-v17-boundary-information-coarsening/article/18a2_likelihood_tilting_moments_v34.tex), complete subsection, blob `b6f74b4d5cbf6e1065af521dc7364dab98445b38`. Locator: `prop:v34-tilting-moments`. The v35-labelled equations it cites are explicitly present in S12; they are not a demonstrated dangling-reference defect.

**S16 — Native entry and retained structure.** [main.tex](https://github.com/TrillionniumFoundation/theta-theory/blob/c730a60bbc8af2a4c6e432813c31dccc897828e7/papers/A2-v17-boundary-information-coarsening/main.tex), complete entry, blob `1a7a0e4aeba4fda2bdccd54894cd0c7869caa400`. The input list, abstract, acknowledgments and bibliography target were read. Reading this list does not mean every listed input was fetched or a recursive build was validated.

## Actual delivery metadata

| Field | Retrieved value |
|---|---|
| Exact-head query count | 1 workflow run |
| Run ID / workflow | `34759179999` / `A2 v41 complete native delivery` |
| Event / head | `push` / reviewed `c730a60...` |
| Created / updated | `2026-09-13T13:12:19Z` / `2026-09-13T13:12:22Z` |
| Run conclusion | `failure` |
| Job | `103728806195`, name `native`, conclusion `failure` |
| Executed step list | `[]` |
| Runner ID / name | `0` / empty string |
| Artifacts | `total_count: 0`, `artifacts: []` |

No billing explanation, infrastructure diagnosis or TeX error is inferred. The observed run is not an executed compiler test. The ledger makes no universal assertion about builds performed elsewhere that were not retrieved.

## Bounded primary-source literature check

**L1.** J. De Simoi, V. Kaloshin and M. Leguil, *Marked Length Spectral determination of analytic chaotic billiards with axial symmetries*, [arXiv:1905.00890v4](https://arxiv.org/abs/1905.00890v4), related [publication DOI](https://doi.org/10.1007/s00222-023-01191-8). The checked record concerns analytic open billiards, non-eclipse, and symmetry/genericity assumptions for marked-length geometric determination.

**L2.** A. Florio and M. Leguil, *Smooth conjugacy classes of 3D Axiom A flows*, [arXiv:2010.04120v5](https://arxiv.org/abs/2010.04120v5), June 3, 2021. The abstract and version notice distinguish the retained smooth-conjugacy result from the removed spectral-rigidity assertion affected by Proposition 3.1. The v41 comparison now respects that distinction.

**L3.** D. Finamore and M. Leguil, *A CAT(0)-approach to the marked length spectral rigidity of Sinai billiards*, [arXiv:2510.18983v1](https://arxiv.org/abs/2510.18983v1), October 21, 2025. The stated finite-horizon Sinai theorem uses an enriched marked length spectrum. No reduction between that observation map and A2's channel laws was established in this review.

**L4.** A. Meister and M. Reiss, *Asymptotic Equivalence for Nonparametric Regression with Non-Regular Errors*, [arXiv:1101.5248v1](https://arxiv.org/abs/1101.5248v1), January 27, 2011. The checked record gives equivalence with Poisson point processes encoding a target curve in their intensity support. It is a precedent for the general boundary-experiment phenomenon, not a proof or refutation of the specific billiard transfer results.

Primary records were checked on September 13, 2026. This was not an exhaustive bibliography or novelty audit, and no external paper's proof was fully re-certified.

## Independently executed controls

The companion [independent_checks.py](independent_checks.py) imports no manuscript code and uses explicit exceptions rather than removable assertions. [RESULTS.json](RESULTS.json) is its full normal stdout; optimized stdout was byte-identical. [EXECUTION.json](EXECUTION.json) contains the actual commands, timestamps, environment versions, return codes and hashes. Both runs exited zero and had empty stderr.

Reproduce from this directory with Python, NumPy and SciPy installed:

```sh
python independent_checks.py > normal.json
python -O independent_checks.py > optimized.json
cmp normal.json optimized.json
```

The recorded environment used Python 3.13.5, NumPy 2.3.5 and SciPy 1.17.0. The actual executable was `/opt/pyvenv/bin/python`. Floating-point text can differ across library/platform versions; such a formatting difference is not by itself a theorem failure.

The controls have four separate scopes. Exact rational algebra checks 361 pair identities and 38 action/amplitude inversions for an asymmetric action and nonconstant amplitude. The nonlinear control solves 96 finite stationary problems using 96 edges, two starting types, three curvature/gap configurations, four endpoint values and degrees three through six; it evaluates the direct envelope coefficients, rather than substituting only the proposed linear orbit. A deliberately swapped asymmetric contact coefficient is rejected. The radial density model evaluates exact collar and score-moment expressions at four logarithmic scales; its sample-size quantity is a continuous scaling proxy, not a simulated integer-sample experiment. Finally, 2,352 support comparisons validate a support-preserving gauge while detecting its changed density invariant; this is a negative control against a support-only shortcut.

No control establishes an infinite half-line limit, uniformity over a compact class, analytic continuation, periodic-table realizability, a Markov-kernel deficiency theorem, or a TeX build. The count of passing tests is not a completeness percentage. `EXECUTION.json` also records an initial development guard triggered by an inadequately large collar scale for a negative local alternative. The final scales satisfy the guard. That correction belongs to the diagnostic, not to the manuscript.

SHA-256 of the executed script: `6901c5416287ef04cad4521acda58b47153015e99afc0fd1bcb232c59d93c12f`.

SHA-256 of each full stdout and of `RESULTS.json`: `f0a0d2d69d4c61b6da4ad62f828214a8624d2cebca8712dcd4193e4e755aa682`.

## Publication boundary

This package adds only independent review documents and diagnostic evidence under a new `reviews/a2-v41-independent-harsh-top4-2026-09-13/` directory on a new review branch. It does not revise the manuscript, change its claims, merge into the default branch, or modify repository permissions or workflow configuration. The author can answer the report in a later revision while retaining this source-pinned review unchanged.
