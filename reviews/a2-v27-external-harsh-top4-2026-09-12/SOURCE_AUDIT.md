# Source, coverage, and execution audit — A2 v27

## Identity and selection

Repository: `TrillionniumFoundation/theta-theory` (accessed through the authorized GitHub connector).

Reviewed revision: `revision/a2-v27-observed-type-smooth-jets-top4-2026-09-12`.

Reviewed commit: `17d71b721f0c5b006b52ec3fbe244866221ee93f`.

Reviewed tree: `ef48921175759a1ca7f2435d2215b765b4d17a03`.

Mathematical-source commit: `416124f13f182f8e2d876f93090865f13269c86b`; its tree is `da8779b9c2a7352486931a64252752f3c6eae0b5`.

Prior v26 review tip: `a5b2d4b5a9ed31059e16e5011c8010579d713598`, reviewing manuscript `cefd89084682cc2e31d730eab1a4b8d8eaac0bbe`.

Review branch: `review/a2-v27-external-harsh-top4-2026-09-12`, based directly on the reviewed commit. This report is not a manuscript revision, merge approval, or change to repository administration.

All revision-branch search pages were inspected initially. The A2 revision search was repeated before writing the review branch; it still ended at v27. This selects the latest located revision, not a claim that no unadvertised work exists in arbitrary historical branches.

The GitHub comparison against the prior review tip returned three commits ahead, zero behind, and 20 changed files. The changes include four added mathematical TeX modules, a changed native entry point, navigation and preservation files, verification records, tools, and a workflow. The root README identifies v27. The manuscript directory's historical name, `A2-v17-boundary-information-coarsening`, is not the active revision number.

## How sources were read

The primary source was the immutable GitHub file content, obtained by repository path and commit. Long files were fetched in ranges where necessary. A recursive repository-tree response was too large for full inspection and is **not counted as a completed native source-graph audit**. No claim is made that a response containing a truncated repository tree constituted a complete checkout.

In the table below, `P` means `papers/A2-v17-boundary-information-coarsening`. “Inspected” means text was read and used in this review; it does not mean every dependency of that text was independently recertified.

| Source relative to P | Coverage and use |
|---|---|
| `main.tex` | Complete native entry and abstract; checked active input names and broad organization |
| `article/01_introduction_v27.tex` | Revised introduction, including its final comparison/organization portion fetched separately |
| `article/18f_domination_and_position_comparison_v27.tex` | Complete revised comparison, including a separate read of lines 230–274 |
| `article/23a_signed_endpoint_rigidity_v27.tex` | Lines 1–240, 241–520, and 510–599; weighted inverse, envelope, new functional remainder lemma, homogeneous isolation, block inverse, and completion |
| `article/23g_density_support_distinction_v27.tex` | Complete 54-line support-preserving example and its scope qualification |
| `article/23f_single_offset_law_inverse_v26.tex` | Complete inherited amplitude-free inverse, interior stability, finite-flight error, and global composition |
| `article/23b_intrinsic_multichannel_rigidity_v23.tex` | Lines 1–245: definitions, signature symmetry, gluing classification, orientation sentence, and cycle-holonomy proof; later portions not independently recertified |
| `article/23d_rank_two_lattice_recovery_v24.tex` | Complete metric-free rank-two theorem and its use in global reconstruction |
| `article/23e_signature_stability_v25.tex` | Finite embedding, noisy matching, gluing persistence, and compact inverse-modulus argument in the returned text; no blanket certification of all later text |
| `article/25b_augmented_global_reconstruction_v26.tex` | Separators, finite templates, finite-order physical theorem, and increasing-order/restarted-budget construction, fetched through line 260 |
| `article/18c1_endpoint_time_deficiency_v25.tex` | Complete displayed support and relative-density hypotheses, layer/bulk bounds, both kernels, and projective remark |
| `article/18a_vector_boundary_information_v26.tex` | Lines 1–230: assumptions, collar estimates, support-exclusive mass, common-collar equivalence, and beginning of LAN expansion |
| `article/20_boundary_compatibility.tex` | Lines 1–230: energy-profile factorization, smooth uniqueness, differentiated stability, and beginning of finite-jet identities |
| `article/16_hyperbolic_coordinates.tex` | Lines 1–245: conditional analytic normal-form calculation and start of smooth intrinsic density discussion; nested scalar-linearization file not independently read |
| `article/01b_observation_hierarchy_v23.tex` | Complete observation-hierarchy subsection, used to check the scope of sign and record conventions |
| `article/99_auxiliary_compendium_v19.tex` | Complete 36-input navigation file, not its entire recursively included mathematical contents |
| `preamble.tex` | Complete native preamble, including companion cross-reference declaration |
| `v5/references_v25.tex` | Bibliography text returned, used for attribution and primary-source comparison; not an exhaustive bibliographic audit |
| `RESPONSE_TO_REFEREE_V27.md` | Complete author response |
| `ACTIVE_SOURCE_MANIFEST_V27.md` | Complete source/preservation map, with its explicit limited-audit warning |
| `VERIFICATION_V27.md` | Complete author execution record and limitations |
| `tools/audit_native_sources_v27.py` | Complete literal source scanner; inspected, not run on a full native checkout |

Additional repository-relative reads: root `README.md`; branch/commit metadata; comparison of prior review tip to head; the principal mathematical objections and recommendation in the previous v26 report. The previous report response was lengthy and truncated; this review does not claim to have independently reread every part of it or every preceding review in the archive.

## Recorded native Git blobs

The following identities were returned with file content or corroborated by the active manifest. These are source identifiers, not build certificates.

| Source | Git blob |
|---|---|
| `P/main.tex` | `2133039c3a220a923b232db9f1c5a5661938773c` |
| `P/article/01_introduction_v27.tex` | `14e5fe4a23f833c6caa581bbe055d0efe73650b6` |
| `P/article/18f_domination_and_position_comparison_v27.tex` | `97b115829b5b770c856596bb7c86f3d769483ced` |
| `P/article/23a_signed_endpoint_rigidity_v27.tex` | `0285c90309b8ab88d1ce1ecf8d492ea6d71f268e` |
| `P/article/23g_density_support_distinction_v27.tex` | `94064ab1f9be56218d30db5de736a85cec427694` |
| `P/article/23f_single_offset_law_inverse_v26.tex` | `35f538eea4415951d1572cd9db76fdff429afa0a` |
| `P/article/23b_intrinsic_multichannel_rigidity_v23.tex` | `0146f25a95d9cdb92cb09f4b6916d4d153cedeaf` |
| `P/article/23d_rank_two_lattice_recovery_v24.tex` | `5e34a7c034ee8a5de0ae915a2b4c622f0f042b2c` |
| `P/article/18c1_endpoint_time_deficiency_v25.tex` | `e03e7eb7e450e6c467f898444d8b72b5fddfd093` |
| `P/article/18a_vector_boundary_information_v26.tex` | `352994ee96dec59bcc780bfa5ed6eace46b2025e` |
| `P/article/99_auxiliary_compendium_v19.tex` | `a596f344cd660eeaacc8e4e3eb21a0cb39610a9e` |
| `P/preamble.tex` | `7e0de97c08dd2e12187193aff89f3ca4712f430f` |
| `P/tools/audit_native_sources_v27.py` | `304a8eb8aed7a2e0ea1ac2944afec1f34ed5e359` |
| `P/VERIFICATION_V27.md` | `4fa14ad2d91a92273e997bf70b661f6cce144113` |

The manifest reports 48 direct native main inputs versus 47 previously and 36 direct auxiliary inputs. Those figures describe navigation. This review did not independently execute the complete recursive reference scanner or hash every native input on a local checkout.

## Live build evidence

A live GET of the workflow-run collection for the revision branch returned `total_count=2`.

| Run | Source commit | Observed conclusion |
|---|---|---|
| `34674173652` | `416124f13f182f8e2d876f93090865f13269c86b` | Failure in the run collection; its pre-step details are also recorded by the author |
| `34674631142` | `852bfc5981f067b0ad0f701137fbb819f56c2479` | Failure; job details independently read |

The second run's job response contained exactly one job, `103502162490`, with `steps=[]`, `runner_id=0`, an empty runner name, and completion at `2026-09-12T05:04:09Z`. This independently verifies that the observed job executed no listed steps. No underlying account or scheduling cause was established.

The author record states that the first job likewise had no executed steps. That particular first-job detail was not independently re-fetched in this review. Neither attempted run is described here as an executed TeX compilation. The branch collection contained no successful complete build and no run at the final evidence-only reviewed head. There was no download or visual inspection of full native PDFs in this review.

A source-pinned successful complete local build would be acceptable evidence; GitHub Actions itself is not mandatory.

## Independent execution

The file `independent_checks.py` was written specifically for this review and run with Python 3.13.5 in both ordinary and optimized modes. It uses only the standard library and explicit exceptions rather than removable assertions.

Executed commands:

```sh
python independent_checks.py > independent_checks.json
python -O independent_checks.py > independent_checks_optimized.json
cmp independent_checks.json independent_checks_optimized.json
```

The commands completed successfully, and the outputs were byte-identical. The committed ordinary result is sufficient to reproduce the comparison; optimized output can be regenerated by the command above.

Script SHA-256: `8261dbe6869bb91ea9d527047d21b7f05d3d7ff466e2c357725082689d0bd85b`.

There are 1,952 checks, mostly finite rational grid instances. The result JSON separates their groups. Exact rational arithmetic checks finite algebraic identities. The floating-point part checks nine leading-geometry inversions and 12 finite 28-flight Dirichlet-bridge envelope examples. The latter use two starting types, endpoint values -0.12 and 0.08, and graph-perturbation degrees 3, 4, and 5. Their parameter integrals use a 12-panel Simpson rule.

The script does not establish convexity on an entire continuum from a grid, infinite-tail convergence from finite bridges, or uncountable statistical deficiency from finite support analogues. Those arguments are assessed analytically in the report. The script also does not run the author's 884 checks, certify the primary literature, compile TeX, inspect PDFs, or verify mathematical proofs formally.

## Primary-literature coverage

Primary arXiv abstract/version pages were checked for `1905.00890v4` (De Simoi–Kaloshin–Leguil), `2510.18983v1` (Finamore–Leguil), and `1101.5248v1` (Meister–Reiß). The comparison is limited to their declared observations, settings, and stated conclusions. It is not a full-paper rereading, exhaustive current-literature search, or priority certification for the contact-jet formula.

## Review write scope

Only files under `reviews/a2-v27-external-harsh-top4-2026-09-12/` are intended to be added on the new review branch: the report, this audit, the independent script, and its executed result. No paper source, previous review, workflow, branch protection, membership, or permission is changed. No merge to `main` is requested or performed. The final review commit is reported after the write and read-back verification; the review source commit above remains the immutable manuscript under assessment.
