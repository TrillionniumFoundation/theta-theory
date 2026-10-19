# Independent verification of the next actual A2-DYN CI artifact

This directory initially contains a verifier and tests of that verifier against the **earlier actually downloaded** physical-tube CI archive. It does not initially contain a successful CI receipt for the new full-physical-source article. Populate any new-run observation only after the corresponding GitHub run exists and has completed.

The standalone program is **verify_actual_ci_artifact.py**. It executes no archive code, performs no network request, extracts no archive member and mutates no article. Its only external inspection command is pdfinfo, reading PDF bytes on standard input. Python's standard library supplies hashing, ZIP CRC checks and JSON processing.

## Required frozen inputs

Pass the complete article, exact published file-identity JSON, exact tested commit and article tree, frozen SOURCE_MANIFEST, final local mathematical/native receipts, final source-gate receipt, final local historical-rebuild receipt, the actual ZIP and fresh GitHub API observation. The expected file list is independently reconstructed as canonical Git trees. Every frozen source byte and every native/tool byte is then compared with the exact tested file identities.

All local reference receipts and the local final PDF/aux must be retained inside the published article and present in the exact expected file list. The local source phase may be separate from the math/typeset execution; use **--reference-source** for that source-checks.json. A local PHASE_all is not required. The actual CI archive **must** contain a passed PHASE_all whose source, math and typeset phases belong to the observed run.

The exact tested root tree is an optional reporting argument. Establish its remote relationship to the article tree with the separate publication readback; this offline verifier does not query GitHub or infer a remote root from a branch name.

## Invocation

Run python verify_actual_ci_artifact.py --help for the complete interface. For the full-physical-source publication, supply these actual values:

| Argument | Required value |
| --- | --- |
| --article | Complete papers/A2-DYN-full-physical-source-author-revision directory |
| --tested-commit | Actual commit read back from the completed dedicated run |
| --tested-article-tree | Article tree read back for that exact tested commit |
| --tested-root-tree | Corresponding repository root tree, if supplied |
| --workflow | .github/workflows/a2-dyn-full-physical-source-20261019.yml |
| --expected-identities | Complete publication file-identity JSON for the tested article tree |
| --manifest | Frozen SOURCE_MANIFEST.json; defaults to the article's file |
| --reference-build | Final evidence/current-execution/full-physical-source-release directory containing mathematical-checks.json, native-typeset.json and native/main.pdf plus main.aux |
| --reference-source | Final source-checks.json, if the source gate is in a separate execution directory |
| --reference-history | Final actual local historical REBUILD_RECEIPT.json, currently the retained execution beginning 20261019T081533713628Z unless a genuinely later rebuild replaces it |
| --archive | Actual downloaded artifact ZIP |
| --observation | JSON containing actual run, jobs and artifacts readbacks |
| --artifact-id | Actual observed artifact ID |
| --job-id | Actual observed successful job ID |
| --job-log-identity | Exact returned job-log identity JSON |
| --job-log | Exact returned UTF-8 job-log bytes, with no appended newline |
| --output-dir | Separate directory for this verification's outputs |

The observation schema uses run, jobs.jobs, and artifacts.artifacts from the purpose-built GitHub readback. The log-identity schema contains job_id, bytes, sha256, exact_returned_utf8_text and file. Archive size/digest, job/run status and checkout head are verified against those observations, rather than hardcoded in the program.

The program derives the mathematical fingerprint, complete program/option contract, numbers of commands and normal/optimized comparisons, active core and TeX counts, native page count and historical document page counts from the frozen article and final local receipts. It does not hardcode the earlier 44-command/164-page version. The historical rebuild must still contain the original complete nine-command, 390-source construction.

## Actual checks

The verifier reads every archive file, checks every CRC and records SHA-256 and Git blob identities. It checks the actual checkout, all three dedicated entrypoint hashes, all mathematical command receipts and log bytes, each normal/optimized stdout and details comparison, complete source anchors, three TeX passes, the actual PDF page count and the native aux identity against the final local aux. PDF byte hashes may differ between local and CI builds, but each actual PDF must match its own recorded bytes/hash and the independently inspected page count.

The fresh historical receipt is selected by actual execution time **after the CI native phase**, not by the largest filename alone. Exactly one such execution is required. All earlier retained historical receipts are listed separately with their own identities. All nine actual commands and outputs and both historical PDF/log products are checked. All post-run changes must be confined to generated build and execution evidence paths.

The verifier also checks that the actual Python environment contains every exact numerical package pin from the frozen requirements file. It uses explicit RuntimeError checks rather than Python assert statements.

## Output files

**CURRENT_CI_ARTIFACT_VERIFICATION.json** contains status, exact_head, article_tree_sha, run_id, job_id, artifact_id, actual artifact digest/size, mathematical_source_sha256, frozen inputs/bytes, command and comparison counts, native pages/PDF/aux, the newly produced historical receipt and the separately preserved earlier receipts. Its success flags concern execution and identity integrity only.

**CURRENT_CI_ARTIFACT_FILE_MANIFEST.json** records every actual ZIP member's bytes, SHA-256 and Git blob identity. **ACTUAL_LOCAL_INPUT_IDENTITIES.json** records the local bytes checked against the tested tree. The caller should also preserve the exact invocation, stdout, stderr and process exit status for reproducibility.

## Verifier validation already completed

The generic program was executed against the actual prior archive from run 39187286448, tested head 8fbc6bd56bd9325600018f1aeb0cb2c2d0d8a4f2 and artifact 12158866926. It successfully rechecked all 1,408 frozen inputs, 98 native/tool inputs, 44 commands, 35 paired outputs, the 164-page native PDF and the fresh 26/883-page historical PDFs. That is a regression test of this verifier, not a new workflow for the current article.

The normal and optimized executions give identical verification results after removing their two execution timestamps. Three integrity-negative checks reject an incorrect tested head, an incorrect article tree and a job log with one extra newline. These actual check receipts are retained in VERIFIER_INTEGRITY_CHECKS.json and verifier-checks/. An initial historical-product JSON shape mismatch, corrected by explicitly checking the three identity fields while validating the recorded product path separately, is retained beneath prior-actual-archive-regression/initial-format-mismatch/.

No successful program run is a proof certificate for continuous geometry, unrestricted pressure, the original shortage limit or the complete raw local limit theorem.
