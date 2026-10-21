# Packaging delta after the visual-archive transport failure

This directory supersedes the complete-article tree and publication payloads in its parent **only for the final packaged release**. The parent plan and all 24 original request bodies remain byte-for-byte unchanged as historical preparation and execution evidence. No remote mutation was issued by this packaging task.

## Ready-to-submit delta

Use `DELTA_UPLOAD_INDEX.json`. It verifies the 21 successful operations in `../API_UPLOAD_STAGE2.json`: ten text-tree batches and eleven binary blobs. The already uploaded workflow blob is also confirmed. Do not re-upload those objects, and do not retry the rejected whole-ZIP blob.

Submit these three object-creation payloads, then the two final tree payloads:

| Payload | Request-body bytes | Expected returned identity |
|---|---:|---|
| `delta/text.json` | 488,627 | tree `d5fe0af9876223fc1b343ece6f0cc8399c79a18b` |
| `delta/part-01.json` | 11,184,847 | blob `8f23966e0814f3e0316d14f722bbfacac8c57ee2` |
| `delta/part-02.json` | 8,094,919 | blob `fdb2fd1b28e8164abba386ac6351e21e1b4f53f0` |
| `delta/article-tree.json` | 146,632 | tree `4f41b3a98487a1ae0507d40390aca030c5520e19` |
| `delta/root-tree.json` | 362 | Bind the actual returned root SHA in the source commit |

The text request creates only five metadata blobs: the exact rebuilt-ZIP ignore rule, revised delivery manifest, revised visual-QA receipt, archive-parts manifest and reassembly instructions. The two binary requests contain the raw archive parts. This is **seven new blobs, 14,916,584 content bytes**; every other required blob has already been uploaded or is anchored in the predecessor.

The exact parent is `4d83de89d16bae7f9e9439dcc80e099b8f8f5c4e`; the parent root is `a1a8677340dfe0bcc3c1be806d6df2c2a200769e`. The root-tree payload modifies only the new article directory and `.github/workflows/a2-dyn-physical-roof-variation-20261021.yml`. The intended branch remains `revision/a2-dyn-physical-roof-variation-2026-10-21`. Commit creation, branch publication and actual CI readback remain with the author agent.

## Byte-exact archive preservation

The original ZIP is retained locally at `audit/pdf-visual-qa/inspected-page-images.zip` and excluded from the selected release by that exact path in the article ignore file. The released replacements are:

| Part | Bytes | SHA256 |
|---|---:|---|
| `inspected-page-images.zip.part01` | 8,388,608 | `412327f5e576f8d3e36763ae3480d6721a8d963608924e900124ddd0510a4ee3` |
| `inspected-page-images.zip.part02` | 6,071,161 | `2553fd1296bc6dcfe969fd4141496e171ca909a94b186b2dbe5f598ec8c6e0ce` |

Their ordered concatenation equals the original **14,459,769-byte** ZIP byte for byte, with SHA256 `40d2b4a0bd42fe071c53020c4a2599f91acebe009f5b92c51d122227565aa9b6`. All 26 ZIP members were read and compared against the existing inspected-image size and SHA256 records. No image or compression stream was changed. `ARCHIVE_PARTS.json` and `REASSEMBLE.md` are inside the released visual-QA directory.

The actual retained connector response was HTTP 400 with the stated message that the MCP request body was invalid or exceeded 16 MiB. The original single-blob request was 19,279,727 bytes. This was a transport-size failure, not an approval rejection. Its exact returned error, original request identity and source-receipt hash are copied into `ARCHIVE_PARTS.json`. Each replacement request body is below the observed limit.

## Final identities and scope checks

The current two-path outer release has **868 files, 97,164,470 bytes and 575 unique blobs**. The delivery manifest declares 867 files and 96,762,786 bytes, excluding its own 401,684 bytes. Its SHA256 is:

`eb4ba488480a7f621a14f3b926794747e94bb8b849927ccd9e0ddbd4e16c0fd4`

The frozen mathematical source manifest remains exactly:

`6a8672fb626e605fe9a93f64187421d953d5259cca3ecca5253cd8f11e42ba86`

Every one of its 130 mathematical/build file identities still matches. The complete predecessor remains the immutable tree `7bcaba2bc1ef7ab393c81a7df84f3e45983c4dfa`. All inherited mathematics, new proof bodies, execution programs, compiled PDFs, build records and prior evidence remain unchanged.

Relative to the previous 865-file plan, exactly three metadata files changed, four files were added, and the one assembled ZIP path was omitted from the published tree. The full ZIP remains on disk. `DELTA.json` identifies every path. Its replacement parts have the same total bytes as the original; the net release-size increase of 7,464 bytes is metadata.

The earlier 218-path staging discrepancy was resolved by the author agent before packaging, as recorded in `../FINAL_STAGED_TREE_READBACK.json`. The checker here sees the expected new packaging changes against that prepackaging index. Root must stage this exact metadata/part delta and remove only the assembled ZIP from the index if committing locally. No source-content discrepancy is implied by those expected differences.

## Supporting outputs

- `PACKAGING_RECEIPT.json`: original/part/archive/image verification.
- `DELTA_UPLOAD_INDEX.json`: actual prior upload receipts, seven remaining blobs, payload hashes and expected returned identities.
- `SUMMARY.json`, `FILES.tsv`, `BLOBS.json`: complete current inventory.
- `CHECKS.json`: exact source/delivery checks and prepackaging-index comparison.
- `DELTA.json`: the narrowly authorized packaging changes.
- `ARTICLE_TREES.json`: all locally computed article subtree identities.
- `upload/`: regenerated full publication plan for reconstruction; use `delta/` for the remaining uploads.
- `before/`: exact original packaging metadata preserved locally.

The final complete article tree `4f41b3a98487a1ae0507d40390aca030c5520e19` was independently verified with read-only Git tree hashing. No claim about branch publication or CI completion is made by this inventory.
