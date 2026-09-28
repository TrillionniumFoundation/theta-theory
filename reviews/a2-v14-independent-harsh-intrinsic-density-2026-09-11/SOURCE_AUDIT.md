# Source, scope, and verification audit — A2 v14

**Review date:** 11 September 2026.

## Frozen source chain

Repository: `TrillionniumFoundation/theta-theory`.

- Author branch: `revision/a2-v14-intrinsic-boundary-normal-form-2026-09-10`.
- Reviewed author commit: `e136929b120912586266fb78e0ae7b3c9d43bfd6` (commit timestamp 2026-09-10 08:37:28 UTC).
- Root tree: `235b06d8ed42d9697ef983367683bc97947f2dad`.
- Manuscript directory: `papers/A2-v14-intrinsic-boundary-normal-form`.
- Parent / latest primary v13 review: `b3f0ad5843782c221651c9189fc156d20865cab1`.
- Author version reviewed by that parent: `0e54099f079232df233316ae6fe7986fc51b7ea1`.

The repository's A2 branches were searched at the start of the review; v14 was the highest materialized A2 author revision returned. The v14 branch was searched again before the review write. Its author source was read by immutable commit, not by a moving default branch. The report does not silently substitute an earlier version of the paper.

## Direct reading

All paths in the table are relative to the frozen manuscript directory unless marked otherwise. Git blob identities pin the actual source, not a paraphrase of an earlier report. The table is a reading-scope record, not a claim that every argument was formally verified.

| Source | Inspected content | Frozen Git blob SHA |
| --- | --- | --- |
| `main.tex` | Full abstract, active-input structure, acknowledgments and contribution scope | `cf90db9a5d217de54c3389f409de034e0f7330e5` |
| `README.md` | Full reading/build map; build and retention figures treated as author claims | `0c3e40e50c71b2f15404112895d4a8bf77384974` |
| `RESPONSE_TO_REFEREES.md` | Full response to both v13 reports and explicit preservation/verification qualifications | `663aa026a5bd4fb83cf4d5f8364187bab1f35d76` |
| `article/01_introduction.tex` | Full introduction, main theorem, family restrictions, forward and spectral comparisons | `907daec5fbc1478423e46a75d311719aa8dfc4db` |
| `article/16_hyperbolic_coordinates.tex` | Complete new analytic comparison, smooth cocycle theorem, width corollary and their proofs | `14210a28d78baadb7e6d750c813c4e4aa31a0eee` |
| `article/20_boundary_compatibility.tex` | Lines 1–270: profile definition, physical convolution identity, complete smooth uniqueness, stability and beginning of finite-jet discussion | `a6292a952053187e872a2d69f7ce1540ee382c07` |
| `article/21_abel_stability.tex` | Full Abel transform, two-sided inverse, nullspace, mixed bound and monomial comparison | `f7d11b05702d7a47599f54c2f75efde5844b7329` |
| `article/23_two_contact_rigidity.tex` | Limiting independent-contact block, action/amplitude variations, recursion and analytic continuation proof | `49d0468658a5b219d5a51720714ffb3194e1110a` |
| `article/24_physical_image.tex` | Physical support-function realization and finite-window theorem/proof, including adaptive lower bound | `520455630bf55e5ae07af5ffaffcccfdb4653cea` |
| `article/27_profile_calibration.tex` | Lines 1–270: plug-in error mechanism and complete charged calibration lemma/proof; not a fresh audit of the remaining older acquisition theorem | `c2aedf2d3c08d545373fbdd26c3f3577956a1c2c` |
| `article/28_regularized_observation.tex` | Full two-derivative gain, reconstruction, acquisition, conditional modulus and improved self-calibrated theorem/proof | `919ba3c9d9492529d30a9edb862298b34c695096` |
| `article/29_two_flight_benchmark.tex` | Full finite inverse, exact-germ clarification, coordinate comparison and direct two-flight experiment | `07174156a9048407b96c0281b75767b57b897421` |
| Repository-root `README.md` | Current A2 navigation and preservation wording | `50b7223a3a1edb251701d699fc5154732495d6e7` |

In addition, `v4/10_boundary_layers.tex` was directly read through the half-line construction, relative determinant definition, and complete two-boundary factorization proof. The displayed beginning of its physical-law subsection was read, but the full inherited localization/integration and collision-record appendix chain was not re-audited line by line. All references to those dependencies in the report retain that distinction.

The latest v13 report was read at `reviews/a2-v13-independent-harsh-normal-form-2026-09-10/REFEREE_REPORT.md`, commit `b3f0ad5843782c221651c9189fc156d20865cab1`, blob `aeac44587b699bca47ee608547e70195bce2f3b8`. Its mathematical assessment is contextual evidence, not a substitute for reading the v14 arguments. The earlier same-version report is addressed through the exact-germ and navigation issues explicitly quoted in the v14 response; this review does not claim to have freshly audited every file on that earlier branch.

## External primary sources

Versioned HTML texts were inspected on 11 September 2026:

1. De Simoi–Kaloshin–Leguil, [arXiv:1905.00890v4](https://arxiv.org/html/1905.00890v4): local analytic hyperbolic normal form and the distinction from global geometric symmetry assumptions.
2. Eynard-Bontemps–Navas, [arXiv:2212.13646v2](https://arxiv.org/html/2212.13646v2): the introductory statement of the classical smooth scalar linearization regime and its distinction from low-regularity failures.

These uses do not attribute A2's physical probability theorem to either paper. The scalar product construction and the width example in the companion note are supplied as independent calculations. No complete priority survey or fresh verification of the other inverse-spectral papers in A2's bibliography is claimed. No external PDF was analyzed in this review.

## Executed local diagnostics

The reviewer wrote `verify_review.py`. It imports no author or previous-referee module. The actual commands were equivalent to:

```sh
python3 verify_review.py --output diagnostics.normal.json
python3 -O verify_review.py --output diagnostics.optimized.json
cmp diagnostics.normal.json diagnostics.optimized.json
```

Both executions passed 3,216 explicit checks, and `cmp` succeeded. `verification.json` is the ordinary-run output, byte-identical to the optimized-run output. The environment reported Python 3.13.5, NumPy 2.3.5, and SciPy 1.17.0.

The exact suite has 2,208 checks. The local Euclidean suite has 1,008 checks, three graph models, 24 half-line endpoint/orientation cases, 64-flight truncations, and finite bridge lengths 4, 5, 8, 9, 12, 13, 20 and 21. Repeated diagnostic operations are counted as checks, not as independent theorems, statistical replications, or formal proof obligations.

- SHA-256 of `verify_review.py`: `06b60b73a82c9c4e6e9c8b7b4090421868b5b8a7c2d43e3cf5d0a6d69a71f242`.
- SHA-256 of `verification.json`: `3120cc2c89a2eb48351e5bb4562648914214ed4ea23ddb751faeb42cc544323b`.

Rational identities are exact within their specified models. Floating values are not interval-certified, and the infinite half-line is truncated. Local Euclidean contact patches are not a global periodic table or a billiard trajectory simulation. The code does not estimate actual success probabilities. The abstract width shears are not asserted to be physically realizable.

## Activities not performed

No author diagnostic suite or previous-referee diagnostic suite was rerun. The manuscript and companion were not compiled. No remote CI was run. No complete source-retention multiset or every inherited formal block was independently checked. No claim is made that all 129 author-reported pages or all appendix statements have been newly certified. A successful finite diagnostic is not evidence of journal-level significance.

## Repository write boundary

The review is to be added only under `reviews/a2-v14-independent-harsh-intrinsic-density-2026-09-11`, on a new branch based on the frozen author commit. Its files are the report, scalar/width companion, this source audit, diagnostic source, recorded diagnostic output, and a reading/reproduction README. Existing manuscripts, root navigation, previous review reports, branch protections, and repository permissions are outside the write set. No merge, deletion, or force-push is part of this review.
