# Source audit and reproducibility boundary — A2 v16

## Immutable target

Repository: `TrillionniumFoundation/theta-theory` (private repository, read through the connected GitHub tool).

Author branch: `revision/a2-v16-integrated-submission-2026-09-11`.

Author commit: `bd27ed3208cc869f6c7a6547453a2557bfcd03ed`.

Author root tree: `74e57478462066ee71fd3c7cfd9408c0c36af54e`.

Commit timestamp: 2026-09-11 02:37:39 UTC / 04:37:39 Europe/Amsterdam.

Review branch: `review/a2-v16-independent-harsh-adaptive-experiments-2026-09-11`, created from that exact author commit. No author manuscript, workflow, root index, or previous report is intentionally changed by this review; all new files are confined to this review directory.

The A2 branch inventory was inspected to identify v16. A subsequent search for the v1x A2 branches again returned v16 as the newest numbered author revision in that group. Source reads throughout the review used the immutable commit, not the branch name or the default branch.

## Reading scope

“Full file” below means the returned source file itself was read, sometimes in consecutive line ranges. It does not mean every nested input was read transitively. A review of a proof is not a machine-checked formal proof.

### Full-file source inspection

All paths in this table are below `papers/A2-v16-integrated-submission/`.

| File | Git blob identity | Principal use |
| --- | --- | --- |
| `README.md` | `441587956546cef6e753fdaf6427a52a9a385a18` | Revision scope and explicit pending full-main build |
| `main.tex` | `2364017e6344eb3d41787bb22552abc0039bbb70` | Entry point, abstract, active input list and manuscript organization |
| `RESPONSE_TO_REFEREES.md` | `670f2990c91870c1a85bd3196d10f348265e8637` | Author response, old-comment disposition and scope qualifications |
| `VERIFICATION.json` | `531cfc15c07354da1963bf69ca706b579eed0108` | Separation of reported diagnostics, companion build and pending full main |
| `tools/build_submission.py` | `704d5e5116bb66055d18b0b8560bb748732bb9e5` | Full-native build procedure; read, not executed |
| `article/01a_protocol_scope.tex` | `9e6d73492a699be6344dd3b75d5df130bccf9437` | Current statement of physical adaptive observations |
| `article/17_adaptive_experiments.tex` | `523e31756b940186ac916f1594f048d0e710000c` | Entire new stopped-kernel, physical transfer and pilot argument |
| `article/31_adaptive_critical.tex` | `0d4f9d9f2e1b65afdf7bfbd941dd72f36c4b14f3` | Entire new adaptive common-support and critical-limit argument |
| `article/16c_strict_margin.tex` | `e29a5d25a4ba0db1c82d1888353ece8dacb7a079` | Entire exact mixed-parameter benchmark |
| `v3/10_geometry_action.tex` | `bbfcaa2d01c229ec0147d5305352b536397842ae` | Localization, alternating Jacobi formula, nonlinear bridge, exact cofactor and relative determinant |
| `v3/20_integration.tex` | `56d9767a769591e74397057c6da873bcc584ff2e` | Full-phase measure, uniform Morse integration, threshold and marked consequences |
| `v4/10_boundary_layers.tex` | `892a88e37a24e591fa525013c41910c791e28e73` | Half-lines, trace-class amplitudes, gluing, relative factorization and limiting laws |
| `v6/10_experiment_transfer.tex` | `c7c68620e16fda23fd1942cbfb6e5fdeddeb0077` | Single-preparation relative total variation and its exact observation scope |
| `article/16_hyperbolic_coordinates.tex` | `836f0036c4d2c3ae279086fd013c87eb652ca227` | Analytic benchmark, physical Schur identification and width/profile equivalence; nested input caveat below |
| `article/16a_scalar_linearization.tex` | `f043720b2306b5470c3f2de9cd3ab33efbd296da` | Full scalar product proof and alternating scalar comparison |
| `article/29_two_flight_benchmark.tex` | `07174156a9048407b96c0281b75767b57b897421` | Full independent-contact two-flight inverse and fixed finite-family observation proof |
| `article/21_abel_stability.tex` | `f7d11b05702d7a47599f54c2f75efde5844b7329` | Full Abel norm argument and monomial benchmark |
| `article/28_regularized_observation.tex` | `919ba3c9d9492529d30a9edb862298b34c695096` | Full revised derivative-gain, reconstruction, allocation and plug-in arguments; inherited pilot dependency caveat below |
| `v5/references.tex` | `a519213d39bbb55c9b89099fca2a8e8b40f21eed` | Attribution and closest comparison references |

The repository-root `README.md` was also read at the same author commit, blob `c1434530ccc7fc80512fc1c2b762acc345a19c7a`. Its latest-A2 pointer still names v15. This is the concrete basis for minor finding C16-R2.

### Selected sections or truncated full-file responses

These source locations were read for the stated purposes, but are not represented as exhaustively inspected in their entirety:

- `article/01_introduction.tex`: the contribution hierarchy, geometry, multiplier conventions, principal relative theorem and the beginning of the hyperbolic positioning discussion. A large full-file response was truncated; the unread remainder is not counted as read.
- `article/20_boundary_compatibility.tex`: the definitions, full nonlinear compatibility/Volterra uniqueness proof, full stated profile stability proof, and the finite-jet formulas through most of their proof. The trailing material was not exhaustively read.
- `article/23_two_contact_rigidity.tex`: the complete block formula, its action/amplitude derivation, invertibility proof, recursive inverse and analytic boundary continuation corollary. The last trailing discussion was truncated.
- `article/24_physical_image.tex`, lines 1–235, blob `520455630bf55e5ae07af5ffaffcccfdb4653cea`: the complete support-function realization, finite-fibre corollary, observation statement and initial observation proof. Its later statistical proof was not treated as fully read; the direct two-flight version was read in full instead.
- `v7/10_critical_experiments.tex`: the exact tangent-support theorem, its proof, tangent approximation lemma, physical critical theorem and principal scaling proof. The final generalized-schedule tail was truncated.
- The previous v15 report at `a108adf17c4b9360e340a2d5708b20a375d69283`: its recommendation, old-comment closure, scalar/width benchmark, build scope and diagnostic discussion were read. The entire tail and every companion file were not re-audited.

The nested `article/16b_determinant_transport.tex` was not independently read as a separate full file. The report's scalar/physical conclusions rely on the read scalar lemma, the explicit Schur-concatenation proof and the relative theorem, not on a claim to have inspected that nested file.

The earlier pilot construction in `article/27_profile_calibration.tex` and every retained nuisance/minimax/record-response appendix were not independently re-proved. The new self-calibrated theorem was checked at the level of its complete printed plug-in argument and its stated pilot dependency. Likewise, no full audit of all historical manuscripts or of A1 was performed. The present report is not a new referee report on the entire theta-theory program.

The source's claims of 52 retained old direct inputs and 56 new direct inputs were read as author assertions. This review did not reconstruct and byte-compare the complete v15-to-v16 native input graph. They are not presented as an independently executed retention certificate.

## Directly queried build evidence

The following GitHub REST resources were read through the repository connector for the pinned author SHA:

```text
/repos/TrillionniumFoundation/theta-theory/actions/runs?head_sha=bd27ed3208cc869f6c7a6547453a2557bfcd03ed&per_page=10
/repos/TrillionniumFoundation/theta-theory/actions/runs/34555357324/jobs
/repos/TrillionniumFoundation/theta-theory/actions/runs/34555357324/artifacts
```

Observed run: `34555357324`, `A2 v16 integrated submission`, completed/failure. Observed job: `103126782653`, `source-and-build`, completed/failure, `steps: []`, runner ID `0`. Artifact count: `0`.

These observations do not identify a LaTeX error or an infrastructure cause. They do not establish that build commands executed. The full native main build was not executed locally by this review either. A private-repository clone was not obtained in the local execution environment; authenticated source inspection used the connected GitHub tools. No abbreviated or modified main was built and passed off as the submitted main.

## External comparison actually checked

The external sources were read through web access, not treated as private repository data:

1. De Simoi–Kaloshin–Leguil, arXiv:1905.00890v4: introduction and Section 2 local analytic symplectic normal-form discussion, including the distinction between local dynamics and symmetry-dependent geometric reconstruction. The whole paper was not re-refereed.
2. Eynard-Bontemps–Navas, arXiv:2212.13646v2: introduction's precise scalar regularity distinction. Low-regularity failures were not imported into the smooth setting.
3. Finamore–Leguil, arXiv:2510.18983v1: abstract and version record for the finite-horizon enriched marked-length scope. No claim of full proof inspection.

An attempted fetch of the LPW author-hosted PDF did not yield a usable document in this session. No page-specific claim based on that PDF is made. The sequential coupling calculation is supplied explicitly in the report instead. No external PDF was successfully analyzed; no PDF layout or figure inspection is claimed. The literature work is a scoped comparison, not an exhaustive originality certificate.

## Executed independent diagnostic provenance

Local source file: `verify_review.py`, 10,581 bytes.

Script Git blob: `15c1404aa22afe430c69f1382cb8d75186b439b0`.

Script SHA-256: `0311268b464151d2e498ddd461d5f9c3b5ce0267f34ebf147745b49f8c7bbd9d`.

Each output: 1,052 bytes; SHA-256 `a85cffa174c243a60a51f07abadda1d8e129dab2d4799360afe7b7b1f0d6c3bb`; Git blob `c59ef2cf0a2e6f001ae9b31a53c580f64cd58f6d`.

Both `python verify_review.py` and `python -O verify_review.py` were executed. Byte comparison of their JSON outputs succeeded. The blobs created through GitHub returned exactly the Git blob identities computed locally from the executed source and output bytes. The two output paths intentionally refer to identical bytes.

The checker imports no author scripts, performs no network calls, and has no random test seed. The small integer seed arguments select specified conditional policies; the finite enumeration is deterministic. Mathematical extension to shared independent policy randomization is justified in the report's coupling argument, not misrepresented as an exhaustive numerical test over all randomized policies.

Every check uses exact fractions and an explicit `RuntimeError` on failure. The 461 figure is the number of calls to this explicit check function. Some checks jointly test several related equalities; it is not a count of independent mathematical results.

It is essential to retain the limits of this evidence: finite rational kernels are not billiard trajectories; exact contact-block arithmetic is not a realization theorem; truncated profile inversion is not smooth-function uniqueness; passing finite examples is not an infinite-dimensional proof certificate; and no test in this checker compiles the manuscript.
