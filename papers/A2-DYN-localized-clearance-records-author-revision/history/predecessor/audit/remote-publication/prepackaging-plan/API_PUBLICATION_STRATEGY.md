# A2-DYN frozen publication inventory and Git Data API recipe

Prepared on 2026-10-21 against the final source reported by the author agent. This task made no repository, index, commit, branch, or remote changes. All generated inventory and request bodies are in this scratch directory. This is a publication recipe, not an observation that publication or CI has occurred.

## Frozen identities and exact scope

The only two destination paths are:

1. `papers/A2-DYN-physical-roof-variation-author-revision`
2. `.github/workflows/a2-dyn-physical-roof-variation-20261021.yml`

| Identity | Value |
|---|---|
| Exact commit parent | `4d83de89d16bae7f9e9439dcc80e099b8f8f5c4e` |
| Exact parent root tree | `a1a8677340dfe0bcc3c1be806d6df2c2a200769e` |
| Reused complete predecessor tree | `7bcaba2bc1ef7ab393c81a7df84f3e45983c4dfa` |
| Expected new complete article tree | `1eb038451f1e7e6ba57f999807979c4aa091a4f5` |
| New workflow blob | `6246879e13fdd5937ebf9c5a9787c24baefb59b5` |
| Delivery manifest SHA256 | `7af42e324a6b88a6389f87f464fa74c27bed5260e322a4076541945d8a650981` |
| Mathematical source manifest SHA256 | `6a8672fb626e605fe9a93f64187421d953d5259cca3ecca5253cd8f11e42ba86` |
| Intended new branch | `revision/a2-dyn-physical-roof-variation-2026-10-21` |

The article tree hash was computed from every selected path, Git mode and blob SHA, with the complete predecessor subtree mounted at its immutable tree identity. The root article-tree serialization was independently confirmed with read-only `git hash-object -t tree --stdin`. No archive contents were re-uploaded or rescanned for this task.

## Inventory

The final observed scope has **865 files, 97,157,006 bytes, and 572 distinct Git blobs**. The article itself has 864 outer files and 97,153,103 bytes; the dedicated workflow contributes one further path and 3,903 bytes. Its blob is identical to the retained workflow copy inside the article.

`DELIVERY_MANIFEST.json` excludes itself. Its **864 declared files and 96,756,502 bytes** match the current scope exactly. Adding its own 400,504 bytes gives the totals above. All 130 entries in `SOURCE_MANIFEST.json` also match actual bytes, Git modes, blob SHAs and SHA256 hashes.

| Blob class | Paths | Unique blobs | Unique content bytes |
|---|---:|---:|---:|
| Exactly reusable from predecessor anchor | 394 | 166 | 9,404,514 |
| UTF-8 content not in predecessor anchor | 458 | 394 | 11,723,569 |
| Binary content not in predecessor anchor | 13 | 12 | 48,994,428 |
| Total | 865 | 572 | 70,122,511 |

“Not in predecessor anchor” does not assert that no other historical Git object has the same bytes. It is the conservative upload set established without a repository-wide object census: **406 unique blobs and 60,717,997 bytes**. Repeated normal/optimized mathematical JSON and repeated delivery PDFs need only one blob each.

The immutable predecessor contributes a further 4,393 files and 544,226,975 bytes through one existing subtree pointer. It is already represented in the expected complete article tree; it is excluded only from the outer inventory and upload-size calculation. The complete article therefore contains 5,257 file paths and 641,380,078 bytes including the predecessor.

## Retained evidence, sizes, and reconciliation

The largest new file is `audit/pdf-visual-qa/inspected-page-images.zip`, 14,459,769 bytes. The prior CI artifact ZIP is 10,660,075 bytes. No selected file reaches 100 MiB.

The 86-file expanded `canonical-boundaries/compile-snapshot/` is **intentionally retained**, together with `compile-snapshot.tar.gz`, under the final `COMPILE_SNAPSHOT_STORAGE.json` policy. All 86 expanded files, totalling 3,180,544 bytes, match the tar members by size and SHA256; neither missing nor additional members were found. The snapshot is intermediate execution evidence, not the final native source.

The original preparation inventory already included all 86 expanded files. The increase from 859 files / 82,241,259 bytes to 865 files / 97,157,006 bytes is exactly six added paths and two updated documents. The six additions are the delivery manifest, the snapshot storage receipt, three PDF visual-QA JSON receipts, and the 14,459,769-byte visual-QA ZIP. `PUBLICATION_STATUS.json` and `VALIDATION.md` account for a further 1,419-byte increase. No file was removed. `DELTA.json` records the exact reconciliation.

## Local staging discrepancy

The read-only scoped index check observed 647 staged outer paths, leaving **218 selected retained evidence paths absent from the index**. The missing paths include logs, PDFs and auxiliary compilation files. Exact-path `git check-ignore --no-index -v` found no ignore rule for the sampled missing paths. No staged path had a content or mode mismatch.

This discrepancy does not alter the complete API request bodies: `upload/article-tree.json` includes every intended file. A direct Git commit must first stage the missing evidence paths and verify the resulting article tree. The exact missing path list is in `CHECKS.json`. This report must not be represented as a fully matching local index until that observation is superseded by a later check.

## Request bodies and order

`UPLOAD_INDEX.json` is the authoritative list of payload files and their SHA256 identities. It also records every expected returned blob or intermediate tree SHA. All request bodies are already materialized under `upload/`; no further text encoding or shell interpolation is necessary.

1. Create the 394 distinct new UTF-8 blobs using the ten unattached content-tree bodies `upload/text-01.json` through `upload/text-10.json`. Their temporary paths are blob SHAs. These trees carry no branch or commit attachment. Compare each returned tree SHA with `UPLOAD_INDEX.json`. Total JSON size is 12,658,468 bytes. The preferred batching size is 1 MiB; three single-file batches exceed it, the largest being 2,970,830 bytes. This size is an operational choice, not an asserted API limit.
2. Create the twelve distinct binary blobs using `upload/blob-01.json` through `upload/blob-12.json`. These are standard base64 blob request bodies, totalling 65,326,340 JSON bytes. Compare every returned SHA with the expected content identity. Existing predecessor blobs need no create call.
3. Submit `upload/article-tree.json` to create the complete article tree. It has 865 entries: 864 outer article files plus the existing `history/predecessor` tree entry. The compact body is 146,229 bytes. Require the returned SHA to equal `1eb038451f1e7e6ba57f999807979c4aa091a4f5`.
4. Submit `upload/root-tree.json`. Its base is the exact parent root, and its only two updates are the new article subtree and dedicated workflow. The body is 362 bytes. Do not add nested modifications underneath the mounted immutable predecessor.
5. The author agent creates a commit with the returned root tree and the sole exact parent above, then creates the authorized new branch at that commit. Preserve returned API receipts. This inventory does not perform those actions.
6. Read back the commit, new branch, article-tree SHA, workflow blob, and `history/predecessor` tree pointer. Use non-recursive subtree reads when inspecting the large parent repository. Read back the resulting actual CI state separately; successful object creation is not a CI result.

GitHub documents content-based tree entries, existing-object SHA entries, and `base_tree` preservation in [REST API endpoints for Git trees](https://docs.github.com/en/rest/git/trees). It warns that a recursive tree response can be truncated beyond 100,000 entries or 7 MB; subtree reads avoid depending on a whole-repository recursive response. The [Git blobs API](https://docs.github.com/en/rest/git/blobs) documents UTF-8 and base64 content encodings. These primary documentation pages were checked on 2026-10-21. Their retrieval limits are not treated as tree-creation payload limits.

## Small output names

| File | Purpose |
|---|---|
| `SUMMARY.json` | Frozen counts, anchor identities and checks |
| `FILES.tsv` / `FILES.json` | Every selected path, mode, byte size, Git blob and SHA256 |
| `BLOBS.json` | Unique blobs, predecessor reuse and all aliases |
| `ARTICLE_TREES.json` | Bottom-up article subtree identities |
| `UPLOAD_INDEX.json` | Exact request bodies, payload hashes and expected API results |
| `CHECKS.json` | Source/delivery identity checks and observed staging discrepancy |
| `DELTA.json` | Exact change from the initial preparation inventory |
| `COMPILE_SNAPSHOT_DUPLICATION_CHECK.json` | Exact expanded/tar member comparison |
| `STAGED_EVIDENCE_READBACK.json` | Scoped read-only ignore/index followup |
| `upload/` | Ten text-tree bodies, twelve binary-blob bodies, article-tree and root-tree bodies |

Earlier preparation files are retained under `preparation-010254/`. Any later source, documentation, evidence or manifest change requires regenerating the inventory and payloads before using their frozen hashes. The complete upload plan and all current results are confined to scratch; this agent has made no remote mutation.
