# Audit scope, immutable sources, and reproduction

This ledger accompanies [REFEREE_REPORT.md](REFEREE_REPORT.md). It distinguishes current-source examination, inherited dispositions, author-reported executions, and computations actually performed for this review. None of these categories is a universal correctness certificate.

## 1. Frozen submission and branch discipline

Repository: `TrillionniumFoundation/theta-theory`.

Reviewed branch: `revision/a2-v38-source-pinned-native-referee-response-2026-09-13`.

Reviewed commit: `7b506becac7fc51dc1ea4f5ab407389d1208b07a`; repository tree: `ff91a3fba7ae4ffd7506669198c738805e40cf33`.

Review branch: `review/a2-v38-external-harsh-top4-2026-09-13`, created directly from that submission. The review adds only files beneath `reviews/a2-v38-external-harsh-top4-2026-09-13/`. It does not alter native manuscripts, author responses, prior reviews, the default branch, repository permissions, or branch protections.

All manuscript paths below are relative to `papers/A2-v17-boundary-information-coarsening/` unless explicitly stated otherwise. Each source link uses the frozen commit, not a moving branch. The reviewed directory's historical name is not a claim that the current paper is version 17.

## 2. Source inventory and actual read coverage

| Key | Frozen source | Coverage and use |
|---|---|---|
| S00 | [Previous report](https://github.com/TrillionniumFoundation/theta-theory/blob/7b506becac7fc51dc1ea4f5ab407389d1208b07a/reviews/a2-v37-external-harsh-top4-2026-09-13/REFEREE_REPORT.md), [revision comparison](https://github.com/TrillionniumFoundation/theta-theory/compare/377efa79597776e75e3cc1d399c1986edd097aaf...7b506becac7fc51dc1ea4f5ab407389d1208b07a) | Prior recommendation, dispositions, provenance counterexample, coverage qualifications, and next-submission conditions; current compact compare response enumerated all 29 changed paths. Historical conclusions are not treated as new independent proof checks. |
| S01 | [Root README](https://github.com/TrillionniumFoundation/theta-theory/blob/7b506becac7fc51dc1ea4f5ab407389d1208b07a/README.md), [manuscript README](https://github.com/TrillionniumFoundation/theta-theory/blob/7b506becac7fc51dc1ea4f5ab407389d1208b07a/papers/A2-v17-boundary-information-coarsening/README.md), [response](https://github.com/TrillionniumFoundation/theta-theory/blob/7b506becac7fc51dc1ea4f5ab407389d1208b07a/papers/A2-v17-boundary-information-coarsening/RESPONSE_TO_REFEREE_V38.md), [historical audit](https://github.com/TrillionniumFoundation/theta-theory/blob/7b506becac7fc51dc1ea4f5ab407389d1208b07a/papers/A2-v17-boundary-information-coarsening/HISTORICAL_DERIVATION_AUDIT_V38.md) | Full navigation, response, and historical-audit documents; versions, claimed repairs, explicit open C2, and preservation claims. |
| S02 | [article/01_introduction_v27.tex](https://github.com/TrillionniumFoundation/theta-theory/blob/7b506becac7fc51dc1ea4f5ab407389d1208b07a/papers/A2-v17-boundary-information-coarsening/article/01_introduction_v27.tex) | Principal inverse and physical theorems, observation-level distinctions, revised anchoring wording, comparison and organization. Not every line of the intervening local-information summary was separately re-fetched. |
| S03 | [main.tex](https://github.com/TrillionniumFoundation/theta-theory/blob/7b506becac7fc51dc1ea4f5ab407389d1208b07a/papers/A2-v17-boundary-information-coarsening/main.tex), [article/01c_geometric_setup_v18.tex](https://github.com/TrillionniumFoundation/theta-theory/blob/7b506becac7fc51dc1ea4f5ab407389d1208b07a/papers/A2-v17-boundary-information-coarsening/article/01c_geometric_setup_v18.tex) | Complete entry and formal principal relative theorem; centered derivative convention and stated dependencies. Reading an input list is not reading all its inputs. |
| S04 | [v3/10_geometry_action.tex](https://github.com/TrillionniumFoundation/theta-theory/blob/7b506becac7fc51dc1ea4f5ab407389d1208b07a/papers/A2-v17-boundary-information-coarsening/v3/10_geometry_action.tex) | Localization, quadratic reduction, Green kernel, weighted nonlinear bridge, cofactor and differentiated relative determinant proofs. |
| S05 | [v4/10_boundary_layers.tex](https://github.com/TrillionniumFoundation/theta-theory/blob/7b506becac7fc51dc1ea4f5ab407389d1208b07a/papers/A2-v17-boundary-information-coarsening/v4/10_boundary_layers.tex) | Half-line construction, two-block relative factorization, physical-law proof, and final corollaries. Other upstream flux/Morse modules were not all independently re-derived. |
| S06 | [article/23f_single_offset_law_inverse_v26.tex](https://github.com/TrillionniumFoundation/theta-theory/blob/7b506becac7fc51dc1ea4f5ab407389d1208b07a/papers/A2-v17-boundary-information-coarsening/article/23f_single_offset_law_inverse_v26.tex) | Full density inverse, stability, finite-flight normalization and jet reconstruction, and detailed periodic composition. |
| S07 | [article/23a_signed_endpoint_rigidity_v27.tex](https://github.com/TrillionniumFoundation/theta-theory/blob/7b506becac7fc51dc1ea4f5ab407389d1208b07a/papers/A2-v17-boundary-information-coarsening/article/23a_signed_endpoint_rigidity_v27.tex) | Full module through completion: weighted inverse, truncation envelope, smooth finite remainders, homogeneous isolation, determinant-one blocks, tangent inverse, and analytic conclusion. |
| S08 | [article/23e_signature_stability_v25.tex](https://github.com/TrillionniumFoundation/theta-theory/blob/7b506becac7fc51dc1ea4f5ab407389d1208b07a/papers/A2-v17-boundary-information-coarsening/article/23e_signature_stability_v25.tex) | Finite embedding and noisy-matching proofs, gluing persistence, and compact-modulus construction. The separate general gluing-space and orientation-quotient chapters were not freshly audited in full. |
| S09 | [article/18a_vector_boundary_information_v26.tex](https://github.com/TrillionniumFoundation/theta-theory/blob/7b506becac7fc51dc1ea4f5ab407389d1208b07a/papers/A2-v17-boundary-information-coarsening/article/18a_vector_boundary_information_v26.tex) | Model, collar estimates, reference-dominated censoring, LAN, revised contiguity, finite likelihood lemma, main Gaussian statement, and beginning of the original-alternative expansion. The full original-law moment proof was checked independently in S10. |
| S10 | [article/18a2_likelihood_tilting_moments_v34.tex](https://github.com/TrillionniumFoundation/theta-theory/blob/7b506becac7fc51dc1ea4f5ab407389d1208b07a/papers/A2-v17-boundary-information-coarsening/article/18a2_likelihood_tilting_moments_v34.tex) | Full noncircular tilting, both contiguity directions, original-alternative mean/fourth moments, and compact-local quadratic risk. |
| S11 | [article/18c1_endpoint_time_deficiency_v25.tex](https://github.com/TrillionniumFoundation/theta-theory/blob/7b506becac7fc51dc1ea4f5ab407389d1208b07a/papers/A2-v17-boundary-information-coarsening/article/18c1_endpoint_time_deficiency_v25.tex) | Full abstract layer/bulk/corner estimates, explicit forward/reverse kernels, exception handling, finite-batch qualification, and projective tail interpretation. Not a re-audit of every upstream application. |
| S12 | [article/25a_common_observables_v25.tex](https://github.com/TrillionniumFoundation/theta-theory/blob/7b506becac7fc51dc1ea4f5ab407389d1208b07a/papers/A2-v17-boundary-information-coarsening/article/25a_common_observables_v25.tex) | Acquisition spaces, full localization/charged scan/calibration argument, observable normalization and continuity, and the finite-test comparison. The later complete global-estimator chain is not certified afresh. |
| S13 | [tools/source_provenance.py](https://github.com/TrillionniumFoundation/theta-theory/blob/7b506becac7fc51dc1ea4f5ab407389d1208b07a/papers/A2-v17-boundary-information-coarsening/tools/source_provenance.py) | Full source read; exact bytes materialized and hash-verified; recorder and recursive-graph controls independently executed. Freeze/archive routines were read but not exercised as a full Git-snapshot CLI integration in this review. |
| S14 | [tools/build_submission.py](https://github.com/TrillionniumFoundation/theta-theory/blob/7b506becac7fc51dc1ea4f5ab407389d1208b07a/papers/A2-v17-boundary-information-coarsening/tools/build_submission.py) | Full driver source read; call placement, source freeze, diagnostics, companion-to-main auxiliary transfer, and failure reporting examined. No execution of this full driver by this referee. |
| S15 | [VERIFICATION_V38.md](https://github.com/TrillionniumFoundation/theta-theory/blob/7b506becac7fc51dc1ea4f5ab407389d1208b07a/papers/A2-v17-boundary-information-coarsening/VERIFICATION_V38.md), [hosted job](https://github.com/TrillionniumFoundation/theta-theory/actions/runs/34743133630/job/103686134246) | Full author ledger; independent GitHub GET of jobs and artifact endpoints. Author's tests, companion PDF and inspection remain attributed to the author. |
| S16 | [article/65_envelope_minimax.tex](https://github.com/TrillionniumFoundation/theta-theory/blob/7b506becac7fc51dc1ea4f5ab407389d1208b07a/papers/A2-v17-boundary-information-coarsening/article/65_envelope_minimax.tex) | Full appendix section read for consistency of the envelope-versus-physical distinction and development-history wording. Its preceding upper-bound theorem was not independently reconstructed. |
| S17 | [article/99_auxiliary_compendium_v19.tex](https://github.com/TrillionniumFoundation/theta-theory/blob/7b506becac7fc51dc1ea4f5ab407389d1208b07a/papers/A2-v17-boundary-information-coarsening/article/99_auxiliary_compendium_v19.tex) | Full 36-input wrapper read for scope. This is not full coverage of 36 auxiliary modules. |

Selected returned blob identities are retained for unambiguous file-level reference:

| Path | Git blob SHA |
|---|---|
| `article/01_introduction_v27.tex` | `aa13f32d24145d40d3f611dfe4083e3fe305e9c6` |
| `article/01c_geometric_setup_v18.tex` | `c070f628f3ffbc58b5219ae37e82e0b3aa758847` |
| `v3/10_geometry_action.tex` | `bbfcaa2d01c229ec0147d5305352b536397842ae` |
| `v4/10_boundary_layers.tex` | `892a88e37a24e591fa525013c41910c791e28e73` |
| `article/23f_single_offset_law_inverse_v26.tex` | `63ed36efd417cd23e6f869952627719de00e6ef7` |
| `article/23a_signed_endpoint_rigidity_v27.tex` | `0285c90309b8ab88d1ce1ecf8d492ea6d71f268e` |
| `article/18a_vector_boundary_information_v26.tex` | `6db9136e31c0e94bc09eddc5f261eab1b25be3ba` |
| `article/18a2_likelihood_tilting_moments_v34.tex` | `b6f74b4d5cbf6e1065af521dc7364dab98445b38` |
| `article/18c1_endpoint_time_deficiency_v25.tex` | `e03e7eb7e450e6c467f898444d8b72b5fddfd093` |
| `tools/source_provenance.py` | `d944aac5604f123795f5c744c2042176c353b981` |
| `tools/build_submission.py` | `faa4310cb5fe41f2869f3d840b760a4a6ea381f3` |
| `article/65_envelope_minimax.tex` | `be7952808b26900ffa069c6d3788ca19d0fa1d86` |

These are identities of fetched files, not a claim that every listed file was materialized locally. Only the provenance fixture below was recovered byte-for-byte for independent module execution.

## 3. D1: independently executed diagnostic package

Files: [diagnostics.py](diagnostics.py), [exact verifier fixture](fixtures/source_provenance.py), [normal output](evidence/diagnostics.normal.json), [optimized output](evidence/diagnostics.optimized.json), and [execution ledger](evidence/execution.json).

The fixture is the author's unchanged source-provenance module, retained here as a test dependency rather than installed as a modification to the author's build tooling. Its 12,975 bytes have Git blob `d944aac5604f123795f5c744c2042176c353b981` and SHA-256 `495061bf4962dd07f2e7b551a1488c9c9e09769a8e7ea4cda353f06bc8a47739`. The test checks both before importing it.

The independent diagnostic program has 15,186 bytes and SHA-256 `ebacd3294048d763882506526022c665f4936cf48fa4b8f4a59e70b1d0ffab63`.

Run from this review directory, with Python and NumPy available:

```sh
OPENBLAS_NUM_THREADS=1 python -B diagnostics.py > /tmp/a2-v38-review.normal.json
OPENBLAS_NUM_THREADS=1 python -B -O diagnostics.py > /tmp/a2-v38-review.optimized.json
cmp /tmp/a2-v38-review.normal.json /tmp/a2-v38-review.optimized.json
```

Executed environment: Python 3.13.5, NumPy 2.3.5. Both return codes were zero, both stderr streams were empty, and the output bytes were identical. The retained output has 4,010 bytes and SHA-256 `fb558b857dc429d77b349d8018cead07d218a599649f8986126d5ef86967abce`. Floating-point digits can vary across numerical-library platforms; the explicit tolerances, rather than cross-platform output hashes, are the numerical acceptance conditions. The fixture's source hashes must always match exactly.

| Family | Actual scope | What it does not establish |
|---|---|---|
| Provenance: 23 controls | Matching bytes, missing/empty recorder, PWD, native/recursive coverage, altered bytes, missing source, unexplained inputs, symlinks, approved/unapproved external paths, producer-bound auxiliary files, source/generated overlap, current outputs, duplicate input lines, static-input comment/dynamic handling. | No native TeX execution; no full-CLI integration; no malicious-toolchain attestation; no independent rerun of the author's 41-test script. |
| Quadratic Jacobi: 21 cases | Unequal curvatures, both parities, lengths 1 through 21; explicit Green versus matrix inverse, Schur endpoint Hessian, cofactor twist. | Not the nonlinear or infinite half-line theorem. |
| Nonlinear local flights | Two asymmetric graph pairs by starting type; signed endpoints; 8/16/24-flight relative log amplitudes versus 64-flight half-line approximations; finite cubic-envelope derivatives. | No global periodic-table realization, certified interval calculation, or proof at arbitrary flight length/derivative order. |
| Density and jet blocks | 121 exact rational signed-density pairs and 12 finite determinant-one blocks. | No statistical density estimator, analytic continuation guarantee, or infinite-order condition bound. |
| Poisson layer/corner | Explicit normalized radial probability model at four sample sizes; finite mass and corner budgets. | No billiard-realizability claim or proof of the full abstract kernel theorem. |

The exact fixture functions operate on real temporary files. No successful TeX process or PDF product is mocked into this review's execution record. Explicit exceptions remain active under `python -O`.

## 4. Hosted execution evidence and native build limits

The reviewer independently read these GitHub endpoints on September 13, 2026:

- `GET /repos/TrillionniumFoundation/theta-theory/actions/runs/34743133630/jobs`
- `GET /repos/TrillionniumFoundation/theta-theory/actions/runs/34743133630/artifacts`

They returned one completed failed job, ID `103686134246`, head SHA `7d34d96a7c2dd974ab3725e009bbb584d3228114`, an empty step list, runner ID zero, and zero artifacts. A compact transcription is retained in [evidence/hosted-status.json](evidence/hosted-status.json). It is identified as an extraction from the responses, not a signed raw API archive. No cause of failure is inferred.

The author ledger reports a genuine seven-page companion build and visual inspection, plus a miniature two-entry integration fixture. The previous conversation's raw companion attachment was not independently retrieved here. The reviewer did not build or inspect either native PDF. No complete native repository checkout was materialized locally. Installed compiler availability is not a compilation result.

## 5. Primary literature records checked

The review checked the following primary abstracts/metadata and the manuscript's corresponding comparison paragraph, not the full PDF proofs. This is a bounded comparison of observation maps, not an exhaustive novelty survey.

**L1.** J. De Simoi, V. Kaloshin, M. Leguil, *Marked Length Spectral determination of analytic chaotic billiards with axial symmetries*. [arXiv:1905.00890](https://arxiv.org/abs/1905.00890). Analytic open dispersing billiards under the stated non-eclipse, symmetry, and genericity assumptions; marked-length data. The inspected record lists the revised version of August 17, 2022.

**L2.** D. Finamore, M. Leguil, *A CAT(0)-approach to the marked length spectral rigidity of Sinai billiards*. [arXiv:2510.18983](https://arxiv.org/abs/2510.18983). October 21, 2025 record; finite-horizon Sinai billiards and enriched marked length spectrum. No equivalence to the present signed conditional-law datum is inferred.

**L3.** A. Meister, M. Reiss, *Asymptotic Equivalence for Nonparametric Regression with Non-Regular Errors*. [arXiv:1101.5248](https://arxiv.org/abs/1101.5248). Earlier nonregular regression/Poisson experiment equivalence. The report uses this only to delimit the claim that a Poisson boundary experiment is itself a new general principle.

## 6. Explicit nonclaims

No journal commissioned this report. No universal correctness, novelty, acceptance, complete-main-build, or visual-inspection certificate is issued. No new fatal mathematical counterexample is asserted. Previous accepted repairs are not reopened without current evidence, but neither are unexamined inherited chapters silently certified. All final recommendations are those of this bounded independent referee-style assessment.
