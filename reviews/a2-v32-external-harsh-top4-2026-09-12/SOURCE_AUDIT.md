# Source and execution audit — A2 v32 independent review

This audit accompanies [REFEREE_REPORT.md](REFEREE_REPORT.md). It records what was read, what was independently checked, and what was not executed. It is not a proof certificate.

## Immutable target and scope

Repository: `TrillionniumFoundation/theta-theory`. Author branch: `revision/a2-v32-compact-lecam-native-submission-top4-2026-09-12`.

Reviewed submission: [`a4fe5c11f18070fc03d878ba683e014b48e921af`](https://github.com/TrillionniumFoundation/theta-theory/commit/a4fe5c11f18070fc03d878ba683e014b48e921af). Tree: `2968770619cd9be6e2692ada43bbe1ad34d13bae`. Mathematical-source commit: `35fd4ccef1b5785692de512635f7240a4df0d641`. Review parent: `9edd5f48d91b74d09718149de6e2c3550c375f20`.

All manuscript paths below are relative to `papers/A2-v17-boundary-information-coarsening/` at the reviewed submission unless stated otherwise. The historical directory name does not identify the current revision number. Source references use actual labels and paths; JSON-wrapper line numbers are not manuscript line numbers.

The branch search returned the revision branches in two pages, including A2 v32. The authenticated commit collection established the actual ancestry rather than inferring freshness from a branch name alone. The comparison against the v31 review head returned ahead_by=2, behind_by=0, and nineteen changed paths with no deleted file. The review does not purport to cover any manuscript subsequently committed after the pinned SHA.

## Source key and coverage

| Key | Source | Examination in this round |
|---|---|---|
| S1 | Authenticated branch search, author-branch commit collection, and comparison `9edd5f48...a4fe5c11` | Version discovery, ancestry and nineteen-path change inventory |
| S2 | Repository-root `README.md`; manuscript `README.md`, `main.tex`, `article/01_introduction_v27.tex` | Complete entries and introduction read; active claims and input structure checked |
| S3 | `RESPONSE_TO_REFEREE_V32.md`, `VERIFICATION_V32.md`; repository-relative `reviews/a2-v31-external-harsh-top4-2026-09-12/REFEREE_REPORT.md` | Current response and verification record read completely; predecessor's principal findings and required response examined, not every source underlying that report |
| S4 | `article/18a1_compact_experiments_v32.tex` | Complete 160-line section read and independently checked: finite-net lemma, uniform Hellinger modulus, singular Gaussian range, fixed-window transfer |
| S5 | `article/18d_count_endpoint_multirate_v32.tex` | Complete 272-line section read and independently checked: Taylor budget, geometric/NB score, waiting comparison, compact product kernels, caps and transfer |
| S6 | `article/18a_vector_boundary_information_v26.tex` | Complete chapter read across overlapping ranges; collar estimates, censoring, LAN, contiguity, quotient Gaussian formulation and support stability examined |
| S7 | `article/18b_raw_physical_multirate_v22.tex` | Record hierarchy, anchored model, exact/ideal reduction, finite design, reference cap, local Gaussian theorem, stopped transfer and pilot corollary examined; final generic-nearby-table discussion was not fully audited |
| S8 | `article/15_operator_comparison.tex` | Complete section read; Dirichlet cofactor, trace-log transport and normalized Morse integration proofs checked |
| S9 | `v4/10_boundary_layers.tex` | Half-line construction, amplitude definition, two-boundary factorization and physical limiting-law proof read and checked; tied-onset and pole statements read through their concluding argument; earlier finite-bridge inputs were not rederived in full |
| S10 | `article/23a_signed_endpoint_rigidity_v27.tex` | Complete chapter read and independently checked: weighted inverse, finite-truncation envelope, smooth remainder factorization, homogeneous isolation, last-jet block and fixed-order inverse |
| S11 | `article/23f_single_offset_law_inverse_v26.tex` | Complete chapter read; exact cancellation, off-model fixed-anchor stability and finite-flight normalization checked; global conclusion examined as a composition, not a fresh proof of every gluing dependency |
| S12 | `article/99_auxiliary_compendium_v19.tex`; `v5/references_v25.tex`; `article/20_boundary_compatibility.tex` | All thirty-six compendium inputs inventoried, not all their proofs reviewed; relevant bibliography entries read; compatibility chapter's first 230 lines spot-checked, not its entire remaining content |
| S13 | Actions run `34701204570`, job `103573170687`, and artifact collection | Direct authenticated execution metadata checked; precise snapshot below |

Additionally, `tools/check_revision_v32.py` was read in full to distinguish the author's diagnostic scope from this review's independent diagnostics. It was not rerun as an authenticated copy in this round. The author's reported fixture, compiler version, hashes and utility-regression results are treated as author records, not as fresh executions by this reviewer.

### Retrieved Git blob identities

These are file-content identities returned by authenticated file reads, not locally reconstructed hashes of all manuscript files.

| Path | Git blob SHA |
|---|---|
| Repository-root `README.md` | `f971281eac847ad2078bd8122672b95bd43707f1` |
| `README.md` | `a5dc1d9bef6bf3e49ae57e771b0c7ffc10b49c30` |
| `main.tex` | `98741811e33425cb4104c1409a26114da8800af1` |
| `RESPONSE_TO_REFEREE_V32.md` | `06b7dd416989a8eacdb66973eee4e9f563fb9911` |
| `VERIFICATION_V32.md` | `8a4aa69d0fd10faabbba6bd3c3c7461fa5447b36` |
| `article/18a1_compact_experiments_v32.tex` | `176e2588344ce0646ed47c09c64f371d6d16a045` |
| `article/18d_count_endpoint_multirate_v32.tex` | `8f84b43e8c8634036cb682453b007136d8f6d673` |
| `article/18a_vector_boundary_information_v26.tex` | `352994ee96dec59bcc780bfa5ed6eace46b2025e` |
| `article/18b_raw_physical_multirate_v22.tex` | `5231860fae5ae8ae88bdcbd5242b65f59f573a82` |
| `article/01_introduction_v27.tex` | `14e5fe4a23f833c6caa581bbe055d0efe73650b6` |
| `article/15_operator_comparison.tex` | `886adb2d68e105723f41f6554eeec59391cab44c` |
| `v4/10_boundary_layers.tex` | `892a88e37a24e591fa525013c41910c791e28e73` |
| `article/23a_signed_endpoint_rigidity_v27.tex` | `0285c90309b8ab88d1ce1ecf8d492ea6d71f268e` |
| `article/23f_single_offset_law_inverse_v26.tex` | `35f538eea4415951d1572cd9db76fdff429afa0a` |
| `article/99_auxiliary_compendium_v19.tex` | `a596f344cd660eeaacc8e4e3eb21a0cb39610a9e` |
| `tools/check_revision_v32.py` | `63758b58bb3e89f7d83bdd9656c66536f77811be` |

## Authenticated native-build snapshot

[Run](https://github.com/TrillionniumFoundation/theta-theory/actions/runs/34701204570): `34701204570`, name `A2 v32 complete native submission`, head SHA exactly `a4fe5c11f18070fc03d878ba683e014b48e921af`, attempt 1, status `completed`, conclusion `failure`.

[Job](https://github.com/TrillionniumFoundation/theta-theory/actions/runs/34701204570/job/103573170687): `103573170687`, name `native-build`, conclusion `failure`, `steps: []`, `runner_id: 0`, empty runner name. Created and started at `2026-09-12T15:06:04Z`; completed at `2026-09-12T15:06:06Z`.

The artifact collection returned exactly `{"total_count":0,"artifacts":[]}`. No job step or native PDF is inferred from an intended workflow. A request for check-run annotations was rejected by the connector endpoint allowlist; the service-level reason for the pre-execution failure was not determined. There is no basis here to diagnose a LaTeX error, billing problem or quota problem.

The environment used for the independent diagnostics did not contain a repository checkout. A direct container Git network probe could not resolve the configured network proxy. Manuscript review therefore used authenticated connector file reads. No complete native build was executed locally. No manuscript PDF, companion PDF, fixture PDF or external research-paper PDF was inspected in this round. No PDF page count or full-native product hash is asserted.

## Independently executed diagnostics

Files: [diagnostics.py](diagnostics.py), [diagnostics.json](diagnostics.json). Executed with Python **3.13.5** on September 12, 2026:

```sh
python3 diagnostics.py > diagnostics.json
python3 -O diagnostics.py > diagnostics.optimized.json
cmp diagnostics.json diagnostics.optimized.json
```

Both runs completed successfully and their outputs were byte-identical. Explicit exceptions keep every check active under optimization. The redundant optimized output is not separately committed.

SHA-256 of `diagnostics.py`: `0e8656deb092927d5a1c1918bd0923bf26caa2326104ccfc1d0cb2b7166d4f30`.

SHA-256 of `diagnostics.json`: `94442d5ef2a874dcb9c36b32dab332b3719ea27a86b3412ed95a6e3522a11f03`.

The checks cover eight exact rational score identities; the geometric affinity 12/13 and four negative-binomial powers; thirty finite log-probability Hellinger comparisons; six closed-form triangular moving-boundary examples; exact last-jet determinant and site-multiplicity identities at orders 3 through 20; the four-density inverse on five signed points with asymmetric action and amplitude; and four illustrative compatible rate choices.

The compact-spike example illustrates why finite restrictions alone are insufficient. Its infinite-index conclusion is proved in the report; the finite rational minimax check is only a diagnostic. It is expressly not a counterexample to the v32 theorem. The triangular model is an abstract density example, not a constructed billiard. Decimal arithmetic is used for numerical checks, not certified interval bounds. Rate values are illustrative, not numerical proofs of convergence. Determinant checks do not establish that an arbitrary nonlinear action has the claimed filtration; that point is addressed by the source proof examination.

## Boundaries of the review

No complete independent rederivation is claimed for every finite stationary/flux foundation, all mixed-derivative operator sources, global analytic gluing and finite-signature stability, charged global calibration and reconstruction, off-model orientation equivariance, the complete Poisson reverse-kernel proof, the native companion, or all thirty-six active appendix inputs. This review does not silently reuse earlier positive assessments as fresh proof certification.

The external literature check is limited to primary arXiv abstract and version metadata for the three references L1–L3 in the report. It establishes the stated comparison of observation problems, not an exhaustive novelty or priority result.

Only new files in this review directory are to be committed. The review branch is based on the pinned submission. Manuscripts, historical reports, workflow definitions, repository permissions, protections and existing branch refs are not altered by this review.
