# A2 v37 — preservation and source delta

The new revision descends from the exact v36 review head `01e772030042ffde9df125c0d40401aee2aabd17`. The first v37 commit is `b0c21cd799bbe4d96bab4a7e1e369d5d7152b294`, tree `bf71bcf4f7db673f7a239702c28558e5b78a960b`.

## Authenticated mathematical-source comparison

The GitHub comparison from the review head to that commit is one commit ahead, zero behind, and reports exactly three changed paths, with **no deleted file**:

| Path | Change |
|---|---|
| `main.tex` under the paper directory | Two revision identifiers changed, 2 added / 2 replaced lines. Abstract, title, date and ordered inputs are identical. |
| `article/23f_single_offset_law_inverse_v26.tex` | E2 statement/reference and proof clarification, 27 added / 10 replaced lines. No theorem or proof is removed. |
| `.github/workflows/a2-v37-native-submission.yml` at repository root | A source-first build/retention workflow, 60 added lines; not evidence of a completed build. |

The ten replaced chapter lines are the insufficient whole-table hypothesis reference and its compressed proof transition. Their replacement states the existing full periodic theorem's hypotheses and explains lattice recovery and all-orbit propagation separately. The remaining chapter is unchanged, and all thirteen labels retain their order.

## Exact preserved pre-edit files

| Current historical path | Original Git blob |
|---|---|
| `history/v36/main.tex` | `8b53acb0785b3b918d129216f172ee3dd73512bc` |
| `history/v36/article/23f_single_offset_law_inverse_v26.tex` | `35f538eea4415951d1572cd9db76fdff429afa0a` |
| Paper `README_PRE_V37.md` | `95b9ca8ec7334fd66c0a56c10846575ba2b27cc0` |
| Repository-root `README_PRE_V37.md` | `54cc54e6e7e300c9107316329b414c18b0c05cdd` |

Historical copies are preservation records, not additional active manuscript inputs. They are not appended to the mathematical article. Previous reports, responses, ledgers and derivation files remain in place.

## Inherited mathematical modules retained

The base-tree update preserves every unlisted path. In particular, the statistical vector proof, likelihood-tilting and original-law moment module, finite-to-compact comparison, count–endpoint argument, signed half-line inverse, analytic continuation, intrinsic gluing, rank-two theorem, signature stability, orientation quotient, moving-ceiling reverse kernel, physical pilot and global reconstruction are not altered.

Selected retained Git blobs identify the dependencies precisely:

| Native source | Git blob |
|---|---|
| `article/18a_vector_boundary_information_v26.tex` | `8ff3ce7334954d6544555e9867a12fa805ca5ea0` |
| `article/18a2_likelihood_tilting_moments_v34.tex` | `b6f74b4d5cbf6e1065af521dc7364dab98445b38` |
| `article/18a1_compact_experiments_v32.tex` | `176e2588344ce0646ed47c09c64f371d6d16a045` |
| `article/23a_signed_endpoint_rigidity_v27.tex` | `0285c90309b8ab88d1ce1ecf8d492ea6d71f268e` |
| `article/23d_rank_two_lattice_recovery_v24.tex` | `5e34a7c034ee8a5de0ae915a2b4c622f0f042b2c` |
| `article/18c1_endpoint_time_deficiency_v25.tex` | `e03e7eb7e450e6c467f898444d8b72b5fddfd093` |
| `article/99_auxiliary_compendium_v19.tex` | `a596f344cd660eeaacc8e4e3eb21a0cb39610a9e` |
| `two_collision.tex` | `df44402b17031525c087d39dfedf8dac3ada611d` |

The main's 52 direct input commands and the auxiliary wrapper's 36 input commands are unchanged. This preservation statement must not be confused with successful recursive retrieval, compilation, or verification of every inherited proof. The local mirror used for the focused checks is partial; the complete source remains in the GitHub revision tree.

## Write scope

The following commit adds current README entries, this preservation record, the point-by-point response, historical audit, exact pre-edit copies and actual limited execution evidence. It does not edit native mathematical source after the source commit identified above. Statistical A1 and the other programme workstreams are untouched. No old branch is deleted or reset, and no merge into `main`, permission change, membership change or branch-protection change is made.

The branch is a new revision for re-review, not an assertion of journal acceptance or complete delivery. Consult [VERIFICATION_V37.md](VERIFICATION_V37.md): C2 remains open.
