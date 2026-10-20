# Independent C1 remote preservation audit

**Result: PASS.** This is a read-only publication-preservation audit of actual GitHub GET responses. It is not a new referee review, a mathematical theorem certificate, or a CI-success claim.

## Immutable target

| Object | Actual Git identity |
|---|---|
| C1 author commit | `409fc85c84a5f239d071b8452da48cb73694365f` |
| C1 repository root | `753cfd8589bc0b7c93942a727ed6925abc214bc2` |
| C1 new article tree | `1c4fe72a8217c590568844d6d69f00e428193049` |
| Sole parent commit | `0933e9b44f5b0fd1d1a624d37ffd881d352496f8` |
| Parent repository root | `dba7d9a6e14d2509291f03cbf269b4ceb78b9549` |

The actual commit object gives the expected root and sole parent. The article is `papers/A2-DYN-marked-boundary-source-author-revision`.

## Complete article identity

The actual recursive article-tree GET is retained at `readbacks/article_recursive.json`. GitHub explicitly returned `truncated: false`. Its 3,739 entries comprise 3,586 blobs and 153 proper subtrees; including the article root gives 154 directory identities.

All 3,586 file paths, object types, modes, Git blob hashes and byte lengths match the independently supplied staged inventory. No file is missing or additional. All 154 directory hashes match that inventory. Each of the 154 tree hashes was also independently recomputed from the actual immediate entries using Git's canonical byte ordering and tree-object framing. Every recomputation agrees with the remote tree identity.

This comparison verifies blob identities and lengths. It does not claim to have downloaded all remote blob bodies again. Their Git identities match the inventory whose stated provenance is actual staged Git blob reads and independent hashing. The exact inventory is retained under `inputs/` with its source path and SHA256 provenance.

## Isolation from all unrelated material

Actual immediate parent/C1 root, papers, `.github` and workflows trees were fetched separately. The huge repository root was never requested recursively. Each of these eight immediate tree hashes was independently reconstructed.

| Tree level | Actual preservation result |
|---|---|
| Repository root | 185 unrelated entries have identical type, mode and SHA; only `papers` and `.github` subtree identities change. No root entry is added or removed. |
| `papers` | All 213 original entries are unchanged; the only addition is the new A2-DYN article tree. |
| `.github` | All three non-workflows entries are unchanged; only the workflows subtree identity changes. |
| `.github/workflows` | All 175 original workflow entries are unchanged; only `a2-dyn-marked-boundary-source-20261019.yml` is added. |

The added workflow has Git blob `56e44c7a4e978494c5dba8df023bef5fc8b7cfa4` and mode `100644`. Because unchanged tree entries retain their exact Git object identities, their complete descendants are preserved. This includes the predecessor A2-DYN source, review material, companion articles and all unrelated papers.

## Actual branch-ref census

Fourteen actual GET pages from the GitHub branches endpoint were preserved, with counts `[100,100,100,100,100,100,100,100,100,100,100,100,96,0]`. There are 1,296 unique observed branch names and no duplicate row. The baseline inventory contains 1,293 branch refs; all remain present with exactly the same commit SHA. The three additions are:

- `revision/a2-dyn-marked-boundary-source-2026-10-19`
- `referee-copy/a2-dyn-marked-boundary-source-2026-10-19`
- `referee-response/a2-dyn-marked-boundary-source-2026-10-19`

All three point to C1 in the retained paginated observations. Three separate actual Git-ref GETs also returned C1. These are observations of moving heads at the recorded collection time, not assertions that their tips remain at C1 after a later C2 or C3 publication. The immutable C1 tree audit remains valid independently of those later heads. This census concerns branch refs, matching the supplied baseline; it does not claim to be a tags inventory.

## Actual evidence and reproducibility

`readbacks/` retains the exact UTF-8 content strings returned by 27 actual GET invocations, with separate request/tool metadata. Request and response timestamps were recorded around the later 23 calls. Per-call timestamps were not captured for the first four calls and are left null; they are not retrospectively fabricated. The saved response bodies and their SHA256 identities are listed in `RAW_RESPONSE_MANIFEST.json`.

`verify_remote_c1.py` verifies the complete saved responses and the exact input inventories. Its actual successful execution is recorded in `VERIFY_PROGRAM_EXECUTION.json`, with genuine stdout/stderr logs. The detailed result is `INDEPENDENT_C1_PUBLICATION_AUDIT.json`. No scientific file, proof index, remote ref, workflow or GitHub object was modified by this audit.

The raw pointwise local limit theorem, four-coordinate inverse and current CI completion are outside this preservation audit. A later workflow result must identify its actual tested commit separately.
