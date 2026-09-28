# Source and execution audit — A2 v36 independent referee-style review

Date: September 13, 2026. This audit separates retrieved source, mathematical examination, author-reported evidence, and newly executed diagnostics. It is not a full native-build certificate.

## 1. Fixed identities and source convention

Repository: `TrillionniumFoundation/theta-theory` (private, accessed through the authorized GitHub connector).

- Reviewed branch: `revision/a2-v36-complete-native-delivery-top4-2026-09-13`.
- Reviewed commit: `0802bfa20533feff55bf5620d39d6399d5e778f5`.
- Reviewed tree: `8a3872f8f341644ef206b019f3308ed9babd40ac`.
- Commit timestamp: `2026-09-13T02:04:07Z`, equivalent to 04:04:07 Europe/Amsterdam.
- Exact previously reviewed v35 submission: `1c50ef04fc2863b4744b5312b539cb68265054f3`.
- New review branch: `review/a2-v36-external-harsh-top4-2026-09-13`.
- Native manuscript prefix, denoted **P/** below: `papers/A2-v17-boundary-information-coarsening/`.

Every current-source path below is pinned to the reviewed commit. Its canonical source URL is `https://github.com/TrillionniumFoundation/theta-theory/blob/0802bfa20533feff55bf5620d39d6399d5e778f5/` followed by the exact repository path, with **P/** expanded as above. References use theorem labels and source ranges, not unverified PDF page numbers.

## 2. Source keys and actual inspection coverage

| Key | Source and examined scope |
|---|---|
| S1 | Commit metadata, main source **P/main.tex**, and authenticated v35-to-v36 comparison. Main entry read in full; delta checked at the changed-file and displayed patch level. |
| S2 | Root `README.md`; **P/README.md**; **P/VERIFICATION_V35.md**; previous v35 referee report. Both current README contents and the inherited execution ledger read in full. The preceding report was used to establish previous dispositions, not as a substitute for fresh proof examination. |
| S3 | **P/article/18a_vector_boundary_information_v26.tex**, source lines 100–560: support-exclusive mass, common-collar representative, LAN proof, finite likelihood normalization/coupling, vector Gaussian theorem, and in-place alternative mean/fourth-moment repair. This range does not constitute a fresh audit of every earlier hypothesis/collar lemma or later section of that file. |
| S4 | **P/article/18a2_likelihood_tilting_moments_v34.tex**, read in full, including all thirteen new explanatory lines and the full tilting, contiguity, original-law moment, and quadratic-risk argument. |
| S5 | **P/article/18a1_compact_experiments_v32.tex**, read in full: finite-net lemma, compact vector theorem, fixed-window corollary and scope remark. The external physical reduction and stopped-transfer dependencies cited there were not all rederived. |
| S6 | **P/article/23f_single_offset_law_inverse_v26.tex**, read in full: four-density identity, stability, finite-flight consequence, global theorem and observation-scope qualification. E2 concerns item 3 of `thm:v26-single-offset-global`. |
| S7 | **P/article/23a_signed_endpoint_rigidity_v27.tex**, lines 1–460: stated determinant-one inverse, support and leading geometry, weighted Green inverse, envelope limit, smooth finite-remainder factorization and homogeneous isolation. The final continuation of the chapter was not read in full in this round. The site multiplicity/geometric-series calculation was independently derived and checked, not presented as a fresh complete audit of every inherited forward-law input. |
| S8 | **P/article/23b_intrinsic_multichannel_rigidity_v28.tex**, inspected across the main response and an overlapping tail read from line 250 to the end; **P/article/23d_rank_two_lattice_recovery_v24.tex**, read in full. Signature-symmetry, gluing, cycle telescoping, rank-two lattice recovery and the full periodic hypothesis statement were examined. |
| S9 | **P/article/23e_signature_stability_v25.tex**, inspected through the finite-signature embedding, noisy matching, gluing persistence and compact inverse-modulus argument. The returned text truncated during the latter proof; any remaining tail is outside this round's fresh coverage. |
| S10 | **P/article/23h_global_orientation_quotient_v29.tex**, lines 1–230: common reflection, lattice sectors, equivariance, classification and stability discussion. The final folded-data discussion and the separate off-model transported-anchor module were not fully rederived. |
| S11 | **P/article/18c1_endpoint_time_deficiency_v25.tex**, read in full: all displayed hypotheses, layer/bulk/corner estimates, forward and reverse kernels, and projective tail remark. Examination establishes the abstract implication under these hypotheses; the complete physical anchored-realization chain was not independently rederived. |
| S12 | **P/article/25a_common_observables_v25.tex**, lines 1–230; **P/article/25b_augmented_global_reconstruction_v26.tex**, lines 1–235. Acquisition spaces, physical localization, scan, pilot, fixed-offset separators, finite-template rule, cap/concentration ordering and global diagonal construction were examined. The final tails and every physical transfer dependency were not freshly audited. |
| S13 | **P/article/01_introduction_v27.tex**, main returned text plus overlapping read from line 270 through the end; **P/v5/references_v25.tex**, bibliography inspected for cited comparison sources. The direct-position benchmark is evaluated here as an explicitly stated comparison, not as a newly rederived complete chapter. |
| C1 | Exact workflow source `.github/workflows/a2-v36-native-build.yml`; latest pinned run metadata; latest run jobs; latest run artifact list. See the exact evidence below. |
| D1 | Newly executed `diagnostics.py` and `diagnostics.json` in this review directory. These are independent finite checks, not imported results from v35. |

Selected exact Git blob identities returned by the connector:

| Path under P/ | Git blob SHA |
|---|---|
| `main.tex` | `8b53acb0785b3b918d129216f172ee3dd73512bc` |
| `article/18a_vector_boundary_information_v26.tex` | `8ff3ce7334954d6544555e9867a12fa805ca5ea0` |
| `article/18a2_likelihood_tilting_moments_v34.tex` | `b6f74b4d5cbf6e1065af521dc7364dab98445b38` |
| `article/18a1_compact_experiments_v32.tex` | `176e2588344ce0646ed47c09c64f371d6d16a045` |
| `article/23f_single_offset_law_inverse_v26.tex` | `35f538eea4415951d1572cd9db76fdff429afa0a` |
| `article/23a_signed_endpoint_rigidity_v27.tex` | `0285c90309b8ab88d1ce1ecf8d492ea6d71f268e` |
| `article/23b_intrinsic_multichannel_rigidity_v28.tex` | `7930d5deac7c53c50aef2e90f90aeb426c10a77d` |
| `article/23d_rank_two_lattice_recovery_v24.tex` | `5e34a7c034ee8a5de0ae915a2b4c622f0f042b2c` |
| `article/23h_global_orientation_quotient_v29.tex` | `ac9938ee655b8b63f069a0c79c467d227eca5ab1` |
| `article/18c1_endpoint_time_deficiency_v25.tex` | `e03e7eb7e450e6c467f898444d8b72b5fddfd093` |
| `article/25a_common_observables_v25.tex` | `82df03f99c1d6ac322161381e063d2f107f048ed` |
| `article/25b_augmented_global_reconstruction_v26.tex` | `4aff42d3fd3dc88a2bb29e8cafef40e224b51615` |
| `VERIFICATION_V35.md` | `cb5ddd37d744e65f1108e4d5da4692fb1a915909` |

Root README blob: `54cc54e6e7e300c9107316329b414c18b0c05cdd`. Paper README blob: `95b9ca8ec7334fd66c0a56c10846575ba2b27cc0`. Previous v35 report blob: `86702a9b2484b9389156fdf3498a35c7c247f8db`.

## 3. Authenticated revision delta

Compare endpoint:

`https://api.github.com/repos/TrillionniumFoundation/theta-theory/compare/1c50ef04fc2863b4744b5312b539cb68265054f3...0802bfa20533feff55bf5620d39d6399d5e778f5`

Returned relation: ahead by 4 commits, behind by 0, seven changed files, no deletion.

| Changed repository path | Status | Added / removed lines |
|---|---|---|
| `.github/workflows/a2-v36-native-build.yml` | Added | 62 / 0 |
| **P/**`article/18a2_likelihood_tilting_moments_v34.tex` | Modified | 13 / 0 |
| **P/**`main.tex` | Modified | 2 / 2 |
| `reviews/a2-v35-external-harsh-top4-2026-09-13/REFEREE_REPORT.md` | Added | 273 / 0 |
| `reviews/a2-v35-external-harsh-top4-2026-09-13/SOURCE_AUDIT.md` | Added | 181 / 0 |
| `reviews/a2-v35-external-harsh-top4-2026-09-13/diagnostics.json` | Added | 154 / 0 |
| `reviews/a2-v35-external-harsh-top4-2026-09-13/diagnostics.py` | Added | 202 / 0 |

The comparison preserves the manuscript's direct inputs and abstract. It adds no native PDF or source-archive product and no v36 verification ledger. A read of **P/VERIFICATION_V36.md** returned 404; that isolated path check is not described as an exhaustive search for every possible external product location. The inherited v35 ledger explicitly does not certify the complete main.

## 4. C1: exact hosted execution evidence

Read endpoints:

- `https://api.github.com/repos/TrillionniumFoundation/theta-theory/actions/runs?branch=revision%2Fa2-v36-complete-native-delivery-top4-2026-09-13&per_page=5`
- `https://api.github.com/repos/TrillionniumFoundation/theta-theory/actions/runs/34732106624/jobs`
- `https://api.github.com/repos/TrillionniumFoundation/theta-theory/actions/runs/34732106624/artifacts`

Filtered observations transcribed from the authenticated responses:

```json
{
  "run_id": 34732106624,
  "head_sha": "0802bfa20533feff55bf5620d39d6399d5e778f5",
  "run_number": 3,
  "status": "completed",
  "conclusion": "failure",
  "job_id": 103656672543,
  "job_name": "complete-native",
  "started_at": "2026-09-13T02:04:09Z",
  "completed_at": "2026-09-13T02:04:12Z",
  "steps": [],
  "runner_id": 0,
  "runner_name": "",
  "artifact_total_count": 0,
  "artifacts": []
}
```

The branch run listing showed three runs. The report's exact job and artifact conclusion concerns the latest pinned run above; it does not claim an individual job/artifact inspection of all earlier runs. An attempt to access check-run annotations was rejected by the connector endpoint allowlist. No runner-failure cause was established. No workflow was dispatched or rerun by this review, and no setting, permission, or protection was changed.

The new workflow is a source-first build-and-retention configuration. Its presence does not show that its checkout, archive, TeX installation, compilation, hash, or upload steps ran. The existing ledger's companion and isolated chapter builds are author-reported predecessor evidence, not newly reproduced evidence.

## 5. D1: newly executed independent diagnostics

Commands actually executed locally:

```sh
python diagnostics.py > diagnostics.json
python -O diagnostics.py > diagnostics.optimized.json
cmp diagnostics.json diagnostics.optimized.json
sha256sum diagnostics.py diagnostics.json
```

Both Python executions and the byte comparison succeeded. Environment: Python **3.13.5**, NumPy **2.3.5**, SciPy **1.17.0**. The committed JSON is the ordinary output; the optimized output is identical and is not duplicated in the repository. Checks use explicit exceptions, not Python assertions, so optimization does not disable them.

SHA-256:

- `diagnostics.py`: `b0794bb7ddbe26503898c56df07b1fdf3fa37d2a230196804ce2b01f670e93bc`.
- `diagnostics.json`: `3849a226b037bc14b24b25aab2cfa8bf316bf1ffa0d32889ce871eb44d37cd11`.

Six finite families were executed:

1. Signed asymmetric four-density inversion on 31 points. Maximum action error below `9.8e-16`; amplitude error below `3.2e-15`.
2. Ninety last-jet blocks, orders 3–32 over three positive geometries, plus leading geometry recovery. Maximum displayed algebraic error below `4.5e-16`.
3. Four nonlinear finite stationary solves, 64 flights, two starting types and endpoint signs, with asymmetric cubic/quartic graphs. Maximum stationarity residual `3.0682921481339775e-17`; maximum symmetrized envelope discrepancy `4.763849426048239e-7`, below the declared `2e-6` tolerance. This is a finite truncation and finite-endpoint approximation, not an exact equality test for the infinite theorem.
4. Lattice and common-reflection identities with nonunimodular marked cycle determinant six, including a perturbation-norm bound. Maximum identity error below `2.3e-16`.
5. Twelve explicit moving-ceiling layer cases with `k` equal to 64, 256, 1024, 4096 and local displacements -1, 0, 0.8. Exact radial formulas include the endpoint/residual corner and compare full intensity variation, not just total mass. The radial probability model is not asserted to be a billiard realization.
6. Original-alternative truncated means in a linearly vanishing radial density with information 2, over four logarithmic scales and four local parameters. The evaluation uses a stable algebraic expression; exponential underflow at logarithmic scale 1024 removes negligible terms and is explicitly documented in the code. This is not an exact integer-sample construction or an independent proof of uniform moment bounds for the general theorem.

The diagnostics read no repository source and have no network activity. Therefore they are not source-preservation tests, do not count or validate the complete input graph, and cannot establish that every active proof was examined. They are independent consistency checks of specified formulas and examples.

## 6. Primary literature scope check

The following primary-source abstract/metadata pages were consulted online. No complete literature PDF was inspected and no full-paper priority audit is claimed.

- **L1:** J. De Simoi, V. Kaloshin, M. Leguil, *Marked Length Spectral determination of analytic chaotic billiards with axial symmetries*. `https://arxiv.org/abs/1905.00890v4`. The current abstract page identifies v4 and the related Inventiones publication. Used only for the stated open-billiard observation map and symmetry/genericity scope.
- **L2:** D. Finamore, M. Leguil, *A CAT(0)-approach to the marked length spectral rigidity of Sinai billiards*. `https://arxiv.org/abs/2510.18983v1`, October 21, 2025. Used for the enriched marked-length and finite-horizon Sinai scope.
- **L3:** A. Meister, M. Reiß, *Asymptotic Equivalence for Nonparametric Regression with Non-Regular Errors*. `https://arxiv.org/abs/1101.5248v1`, January 27, 2011. Used for the existence of a prior Poisson boundary-experiment equivalence in a different observation model.

Private manuscript passages were not submitted to web search. These external references support only the bounded comparisons made in the report; they do not independently verify the repository's theorems.

## 7. Limitations and write scope

No full native main or companion was compiled, no assembled PDF was obtained or inspected, and no complete audit of all auxiliary inputs was performed in this round. The fresh examination does not cover every relative-law determinant estimate, every flux integration, every count–endpoint or stopped-transfer proof, the full direct-position benchmark, every analytic realization bundle, or every appendix. Favorable findings are confined to the described arguments and their stated dependencies.

The review is designed as an additive commit based on the exact reviewed tree, under a new review branch, containing this audit, the report, and the two diagnostic files. It does not revise the author's mathematical sources, merge into `main`, remove historical work, change branch protections, or modify membership and permissions. Successful Git delivery of this report is distinct from the unverified native delivery of the author's assembled manuscript.
