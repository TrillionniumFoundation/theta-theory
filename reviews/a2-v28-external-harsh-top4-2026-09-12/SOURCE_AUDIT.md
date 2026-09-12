# A2 v28 independent source and execution audit

## Immutable object

- Repository: `TrillionniumFoundation/theta-theory`.
- Revision branch: `revision/a2-v28-common-orientation-quotient-top4-2026-09-12`.
- Reviewed head: `f5fcd5e319cb4a37bdcbf8d9f9d190786ec7fc7d`.
- Reviewed tree: `a532ddec6150d12e3b3c05dc357a2699295b29ae`.
- Mathematical commit: `6d8f158c60f3636c572daa64779f57c9c9ec757b`.
- Mathematical tree: `768f467572a3a884073e69065d1239825be8f25e`.
- Preceding review tip: `e5a153b1bbb663c4a5e3153c6a7bdedb7fcd5864`.
- New review branch: `review/a2-v28-external-harsh-top4-2026-09-12`.
- Review date: September 12, 2026.

The revision-branch search was paginated, including the older programme branches. The latest named A2 revision located was v28. The v28 commit collection gave the three-commit sequence from the prior review tip. A separate search for `a2-v28` found the revision branch and no pre-existing v28 review branch before this review branch was created. These observations identify the reviewed snapshot; they do not promise that the repository cannot change afterwards.

The comparison from the preceding review tip to the reviewed head returned `ahead`, three commits ahead, zero behind, and no deleted files. The comparison from the mathematical-source commit to the reviewed head returned two commits ahead, zero behind, with only navigation, response, diagnostic-fixture, and verification changes; no mathematical article input changed in that comparison.

## Read sources

All paper-local paths below are relative to `papers/A2-v17-boundary-information-coarsening` at the reviewed head. Hashes are Git blob IDs reported by the connected repository reads, except the locally reproduced script and outputs, whose bytes were independently hashed as described below.

| Source | Git blob | Inspection |
|---|---|---|
| `main.tex` | `7f150377c310e8243b0d99bce4a5eab147cea6ac` | Complete entry and abstract read; direct source wiring inspected, not a recursive native audit |
| `article/23h_global_orientation_quotient_v28.tex` | `d7181d0ce3e7092227b2ff984dab5a4c3a672650` | Complete new subsection: definition, equivariance, classification, stability, folded-record distinction |
| `article/23b_intrinsic_multichannel_rigidity_v28.tex` | `7930d5deac7c53c50aef2e90f90aeb426c10a77d` | Complete section read; final lines separately fetched to avoid response truncation |
| `article/01b_observation_hierarchy_v28.tex` | `b6b5a739939beab02dfbc9b4e9cb077866366116` | Complete section read |
| `article/23f_single_offset_law_inverse_v26.tex` | `35f538eea4415951d1572cd9db76fdff429afa0a` | Complete inverse, off-model stability, finite-flight and global-composition statements read |
| `article/23a_signed_endpoint_rigidity_v27.tex` | `0285c90309b8ab88d1ce1ecf8d492ea6d71f268e` | Complete argument read in overlapping fetches: 1–235, 235–510, and 490 through the end; weighted inverse, functional remainder, envelope, homogeneous block and completion examined |
| `article/23d_rank_two_lattice_recovery_v24.tex` | `5e34a7c034ee8a5de0ae915a2b4c622f0f042b2c` | Complete section read |
| `article/18f_domination_and_position_comparison_v27.tex` | `97b115829b5b770c856596bb7c86f3d769483ced` | Main common-domination proof, dominated/disjoint lemma, full observed-type proof, time-retention remark and examples read; final tail not independently certified |
| `article/01_introduction_v27.tex` | Not separately recorded | Read through the beginning of local information; later tail not treated as a complete fresh reading |
| `article/20_boundary_compatibility.tex` | Not separately recorded | Sampled factorization, smooth Volterra uniqueness, profile stability and finite-jet transformation; not the entire file |
| `tools/check_revision_v28.py` | `8467debd339b36a7c51db0486fb542b28497485b` | Complete script read, exact bytes reproduced, blob verified, and both execution modes run |
| `ACTIVE_SOURCE_MANIFEST_V28.md` | `e410a373f37a55bfd12749caf9b653ce189979f2` | Complete manifest read; statements of other executions remain attributed to the author |
| `RESPONSE_TO_REFEREE_V28.md` | `81c4a2ba1f5837f7a41c198e7e62734d7d64b19e` | Complete response read |
| `VERIFICATION_V28.md` | `3aa3207dd17e64e25c1b9e73de860b0133d4f8c9` | Complete record read; fixture compilation/layout not independently repeated |

Repository-relative sources additionally read: root `README.md` at blob `66ac472cdf9c3aa71bec847482b70976acbee69b`, and `reviews/a2-v27-external-harsh-top4-2026-09-12/REFEREE_REPORT.md` at blob `42fac42b2ebbe89b92da19c06a039c1a6f28a62f`. The latter was read in the initial response and an overlapping fetch of lines 180 through the end, including its C1/C2 requests and verification limits.

The manifest states that the main entry has 49 direct inputs and that the active auxiliary compendium has 36 direct inputs. The current entry visibly retains that compendium. Those counts and retained pointers are not represented as this reviewer's executed complete recursive source closure. The companion mathematics, all auxiliary inputs, the entire relative-law dependency chain, all local-information proofs, and all global-estimator proofs were not independently recertified in full.

## Independently executed diagnostics

Environment: Python 3.13.5. Both scripts were run in ordinary and optimized modes and their outputs compared byte-for-byte with `cmp`. All four executions completed successfully.

### Author script rerun

The retrieved UTF-8 script was reproduced locally without mathematical or code changes. Before execution, `git hash-object` gave exactly:

`8467debd339b36a7c51db0486fb542b28497485b`.

Its SHA-256 is:

`d5f1b366689e8773ddc5a0ddc25be7d1105fd5a8dd1e6da22fc44b23444b5c65`.

The rerun produced 883 exact finite checks and the byte-identical output committed here as `author_checks_reproduced.json`. Its Git blob is `8edbf8a22284816c1dc555c026dd962068fbb3bd`, identical to the author's pinned result. Its SHA-256 is `29f06040b8ee0cdf3da8183354598c94d6f9c01390b920144afde729a24ae5bc`.

From a complete checkout at the reviewed source, the commands are:

```sh
python papers/A2-v17-boundary-information-coarsening/tools/check_revision_v28.py > author-normal.json
python -O papers/A2-v17-boundary-information-coarsening/tools/check_revision_v28.py > author-optimized.json
cmp author-normal.json author-optimized.json
```

Only this script was independently rerun. The author's changed-source audit, revised-module typesetting, v27 suite, and historical referee suites were not rerun.

### New independent script

`independent_checks.py` uses only the Python standard library, exact rational arithmetic, and explicit exceptions. Its SHA-256 is:

`23bef28fc24772ce1cd72d3b97007f927c98b1bdeff23ba2646ae319ffe2e2a4`.

Its Git blob is `a035b3a40b86f9b8b1a74bd6a2c58c25bbcb0ac8`. It produced 1,784 checks, including the fixed-anchor off-model nonequivariance witness. `independent_checks.json` has Git blob `66ee040fba7977ad9a11613c4a12a6b363e6abeb` and SHA-256 `5a566cfa1accc0b59628f46e1cf33d020846f30ace3bea9777f73da8b55e6ab2`.

Run from this review directory:

```sh
python independent_checks.py > independent-normal.json
python -O independent_checks.py > independent-optimized.json
cmp independent-normal.json independent-optimized.json
```

The square-root comparison in T1 is checked with exact squares and verified positive branches, not floating-point approximations. The witness is a functional-density example and is not labelled a physical billiard-table counterexample. A transported-anchor identity is checked separately. The analytic proof and its exact scope are in Section 3 of `REFEREE_REPORT.md`.

The finite grids do not establish convergence of the infinite half-line, any full statistical deficiency limit, or completeness of the native source graph. Their counts must not be used as a theorem-coverage percentage.

## Live workflow evidence

A connected read of the revision-branch run collection returned two runs. Separate job reads confirmed both:

- Run `34677164341`, job `103508962672`, source `6d8f158c60f3636c572daa64779f57c9c9ec757b`, completed September 12, 2026 at 06:03:58 UTC.
- Run `34677568860`, job `103510063039`, source `c6827750cc595d058a1786aa818a57d52266cfdc`, completed September 12, 2026 at 06:13:29 UTC.

Both had status `completed`, conclusion `failure`, `steps=[]`, runner ID `0`, and an empty runner name. See `ci_observations.json`. No checkout or TeX step ran. No failure cause is inferred. No workflow was dispatched or rerun by this reviewer, and no repository permissions were changed.

The author-reported eight-page fixture, its hashes, and its ten unresolved-reference occurrences were read in the verification record. They are not this reviewer's independent PDF or log inspection. No complete native PDF was compiled, rendered, or visually inspected here, and no PDF page references are invented in the report.

## External literature scope

On September 12, 2026, web search and direct arXiv abstract-page reads checked:

- `arXiv:1905.00890v4`: De Simoi–Kaloshin–Leguil, marked-length determination under symmetry/genericity assumptions; abstract and version metadata only.
- `arXiv:2510.18983v1`: Finamore–Leguil, enriched marked length spectrum for finite-horizon Sinai billiards; abstract and version metadata only.
- `arXiv:1101.5248v1`: Meister–Reiß, nonregular regression-to-Poisson equivalence; abstract and version metadata only.

The comparison uses primary sources. It is not exhaustive priority research and does not claim a full reading of these papers or an implication between their observation maps and A2's.

## Publication boundary

This review branch starts from the exact reviewed revision head. The new package adds only the report, this audit, the new diagnostic source/result, the reproduced author result, and normalized workflow observations under its new review directory. It does not modify mathematical manuscript files, delete historical material, merge into `main`, change an existing review branch, or alter repository governance. A review commit is not an endorsement or a journal decision.
