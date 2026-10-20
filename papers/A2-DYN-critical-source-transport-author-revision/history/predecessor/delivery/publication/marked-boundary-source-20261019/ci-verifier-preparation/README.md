# Actual CI artifact verifier for the recovered marked-boundary author revision

`verify_actual_ci_artifact.py` is a new local adaptation of the immutable published B verifier. Its predecessor is the exact file at commit `0933e9b44f5b0fd1d1a624d37ffd881d352496f8`, under `papers/A2-DYN-full-physical-source-author-revision/delivery/publication/full-physical-source-20261019/actual-C2-ci/`, with SHA-256 `e4bbbe2adcba3fc81fc8cd91f2fb2d80144e946c16ea537b7596dbb0b07d01e1`. The old file was copied to a different inode and remains unchanged. This preparation is not claimed to reproduce the bytes or hash of the lost pre-recovery C verifier.

The verifier operates only on explicit actual observations, the downloaded artifact ZIP, exact tested-tree file identities, frozen source files and final local reference receipts. It makes no remote request, executes no code from the archive, and does not extract the archive. It writes only its own result directory. `pdfinfo` is used to inspect the actual PDF bytes independently.

## Exact supported author contract

- Article: `papers/A2-DYN-marked-boundary-source-author-revision`.
- Author branch: `revision/a2-dyn-marked-boundary-source-2026-10-19`.
- Dedicated workflow: `.github/workflows/a2-dyn-marked-boundary-source-20261019.yml`.
- Actual native source: all 59 core bodies 260–318, included exactly once in the complete 69-file TeX closure.
- Actual source-driver AST: 26 declared programs, 52 normal/optimized commands, and all 43 stdout/details byte comparisons.
- Source manifest: schema 5, four inherited identity anchors. The fourth binds all 2,765 files and the exact original `0933` article tree. The helper reconstructs that tree and the full 2,088-file `fdf2603` predecessor tree from the original paths and modes while checking every actual preservation placement.
- Reports: the original 90 indexed bodies plus the distinct original v73 copy at blob `c06ffcf46059987264935f497d8b4e2564571936`.
- Actual CI Python: 3.11, with every frozen requirement pin present in the actual archived environment log.

The manifest digest, mathematical fingerprint, total frozen source count, current label count, new label count, final native page count, PDF identity, CI run and artifact IDs, and all tested commit/tree identities come from actual files or explicit CLI arguments. They are not guessed. In particular, neither the old pre-recovery 195-page draft nor an earlier recovery fingerprint is built into this helper. The final local release reference is supplied explicitly.

The publication labels **C1** and **C2** do not occur as logical requirements of the helper. In the current two-commit plan, the complete scientific C1 is the tested commit. A later C2 may archive the actual C1 evidence with unchanged frozen scientific inputs. The result always reports the actual `--tested-commit`, and never treats that later metadata child as the tested head.

## Exact CLI

Every capitalized value below denotes an actual value or existing path collected by the publisher. Do not run this command with fabricated placeholder receipts.

```bash
python iteration-20261019c-recovery/current-ci/verify_actual_ci_artifact.py \
  --article theta-theory/papers/A2-DYN-marked-boundary-source-author-revision \
  --archive "$ACTUAL_DOWNLOADED_ZIP" \
  --tested-commit "$ACTUAL_TESTED_COMMIT" \
  --tested-article-tree "$ACTUAL_TESTED_ARTICLE_TREE" \
  --tested-root-tree "$ACTUAL_TESTED_ROOT_TREE" \
  --workflow .github/workflows/a2-dyn-marked-boundary-source-20261019.yml \
  --expected-identities "$ACTUAL_TESTED_FILE_IDENTITIES_JSON" \
  --manifest theta-theory/papers/A2-DYN-marked-boundary-source-author-revision/SOURCE_MANIFEST.json \
  --reference-build theta-theory/papers/A2-DYN-marked-boundary-source-author-revision/evidence/current-execution/marked-boundary-source-recovery-final \
  --reference-source "$ACTUAL_FINAL_SOURCE_CHECKS_JSON" \
  --reference-history "$ACTUAL_FINAL_HISTORICAL_REBUILD_RECEIPT_JSON" \
  --observation "$ACTUAL_RUN_JOBS_ARTIFACTS_JSON" \
  --artifact-id "$ACTUAL_ARTIFACT_ID" \
  --job-id "$ACTUAL_JOB_ID" \
  --job-log-identity "$ACTUAL_RAW_JOB_LOG_IDENTITY_JSON" \
  --job-log "$ACTUAL_RAW_JOB_LOG_FILE" \
  --output-dir "$ACTUAL_VERIFICATION_OUTPUT_DIRECTORY"
```

`--manifest` can be omitted only when the manifest is at `article/SOURCE_MANIFEST.json`. `--reference-source` can be omitted only when the actual final source gate is `reference-build/source-checks.json`. The source gate may have run separately after the mathematical/typeset phases; a local `PHASE_all.json` is not required. The actual CI archive **must** contain a successful `build/current/PHASE_all.json` with all three completed phases.

The local reference mathematical, native, source and historical receipts must reside inside the tested article and be present in the exact tested file inventory. Their bytes are checked against that inventory. For the historical input, pass the actual final local `REBUILD_RECEIPT.json`; do not reuse a prior run's receipt merely because it is present in an inherited archive.

## Input JSON shapes

The expected tested file inventory is an actual complete article inventory:

```text
{
  "article_tree_sha": ACTUAL_40_HEX_ARTICLE_TREE,
  "subtree_hashes": { RELATIVE_DIRECTORY: ACTUAL_40_HEX_TREE, ... },
  "files": [
    {"path": RELATIVE_PATH, "bytes": ACTUAL_SIZE,
     "sha256": ACTUAL_SHA256, "sha": ACTUAL_GIT_BLOB,
     "mode": "100644" OR "100755", "type": "blob"}, ...
  ]
}
```

`subtree_hashes` is optional; when supplied every value is checked. The complete `files` array always reconstructs the tested article tree independently. Every frozen input and each separately accessed reference or predecessor-placement file is then read and matched by byte size, SHA-256, Git blob and current Git file mode.

The observation object retains actual parsed GitHub API data:

```text
{"run": ACTUAL_ACTIONS_RUN_OBJECT,
 "jobs": {"total_count": ACTUAL_COUNT, "jobs": [ACTUAL_JOB_OBJECT, ...]},
 "artifacts": {"total_count": ACTUAL_COUNT, "artifacts": [ACTUAL_ARTIFACT_OBJECT, ...]}}
```

Use the real run endpoint, `/actions/runs/{id}/jobs?per_page=100`, and `/actions/runs/{id}/artifacts?per_page=100`; read all pages if the collection exceeds one page. Preserve the original fetch responses separately. The verifier requires the actual dedicated push event, author branch, exact tested head, completed successful run and job, all successful steps, complete collections, and an unexpired artifact for the same run and head. The ZIP bytes must match the advertised size and digest.

The job-log identity must contain the actual `job_id`, `bytes`, `sha256`, `exact_returned_utf8_text: true`, and the saved log filename. Encode precisely the returned UTF-8 log text. Do not add or remove a terminal newline.

## What successful verification establishes

The verifier reads every ZIP member, verifies its CRC, rejects duplicate or unsafe paths and symbolic links, and creates a complete byte manifest. It then checks actual checkout SHA, build outcome, the three dedicated entrypoint hashes, all frozen inputs, all four immutable anchors, actual source and native reference closure, every mathematical command and individual command receipt, every normal/optimized pair, and every native command and its individual receipt. It independently reads the actual PDFs, checks three TeX passes and PDF/aux identities, and requires the same final page count and aux bytes as the supplied final local reference.

The current CI historical rebuild is selected by its actual start time **after the current native phase ends**. Exactly one such rebuild must occur within the current run, with nine commands, 390 historical source inputs, both actual historical PDFs and their logs. All earlier archived historical receipts are listed separately. No old historical receipt is substituted for the current actual one.

The helper also verifies that the actual post-run working-tree changes are confined to generated build/history outputs. It retains actual warnings from the current native and historical logs without converting a successful build into a mathematical certificate.

Successful output files are:

- `CURRENT_CI_ARTIFACT_VERIFICATION.json`: actual run/head/artifact, source/anchor/reference checks, all command counts and times, actual PDF identities, current historical receipt and explicit scope limits.
- `CURRENT_CI_ARTIFACT_FILE_MANIFEST.json`: every actual ZIP member by path, size, SHA-256 and Git blob.
- `ACTUAL_LOCAL_INPUT_IDENTITIES.json`: every actually read local source/reference/anchor placement checked against the tested tree.

The first output additionally exposes `manifest_schema: 5`, `immutable_anchor_count: 4`, `distinct_original_reports_with_recovered_copy: 91`, `recovered_v73_report_sha256`, `author_contract`, and the actual native/new-body label counts. A successful result describes only the observed tested commit. The caller must separately preserve the actual commit/root/ref readback connecting these supplied tree identities to the remote Git objects.

## Preparation status

`VERIFIER_PREPARATION_RECEIPT.json` records the actual preparation checks: syntax, equal normal/optimized CLI help, and an independent read of the current 59-core/69-TeX/26-program source contract. At that check the article still carried the inherited schema-4 manifest; it was correctly rejected as an unfrozen C source. No actual C archive was verified in that preparation.

The recorded local preparation interpreter is distinct from the required actual CI Python 3.11 environment. The source uses Python 3.11 syntax and standard-library interfaces. The eventual archived CI environment must itself prove the required version and package pins. These preparation checks, the later CI, and any finite mathematical diagnostics are auxiliary evidence, not a proof of the complete continuous Lorentz-gas local limit theorem.
