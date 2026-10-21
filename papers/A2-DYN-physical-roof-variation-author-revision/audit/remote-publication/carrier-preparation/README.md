# A2-DYN evidence-carrier Git Data preparation

This helper performs local read-only verification and writes request bodies only to a new scratch output directory. It has no network calls, uploads, index writes, commits, or ref updates. The parent author process owns all article changes and publication.

## Fixed source release

- Repository: `TrillionniumFoundation/theta-theory`
- Branch: `revision/a2-dyn-physical-roof-variation-2026-10-21`
- Carrier parent: `6708e30d1e8511e6ed2f4e3a6247c09628bd3ea9`
- Source root tree: `ad34fd91ad2f1c6e594d3bbe437417aba524bf87`
- Source article tree: `4f41b3a98487a1ae0507d40390aca030c5520e19`
- Immutable predecessor tree: `7bcaba2bc1ef7ab393c81a7df84f3e45983c4dfa`
- Workflow blob: `6246879e13fdd5937ebf9c5a9787c24baefb59b5`

Keep these four files together: `prepare_evidence_carrier.py`, `SOURCE_RELEASE_BASELINE.json`, `SOURCE_ROOT_TREE.json`, and `SOURCE_PAPERS_TREE.json`. The default repository directory is recorded in the baseline; `--repo /absolute/path/to/repository` overrides it. The two cached tree receipts are complete nonrecursive GitHub reads and are independently rehashed. No whole-repository recursive inventory is needed.

## Authorized carrier scope

All 130 frozen mathematical/build inputs, `SOURCE_MANIFEST.json`, `CURRENT_SOURCE_ANCHOR.json`, the root workflow, and all 4,393 predecessor files remain unchanged. Existing source-release evidence is immutable. Changes to published outer files are limited to:

- `PUBLICATION_STATUS.json`
- `VALIDATION.md`
- `README.md`
- `HISTORY_PRESERVATION_AUDIT.md`
- `RESPONSE_TO_REFEREE.md`
- `PROOF_DEPENDENCY_LEDGER.md`
- `DELIVERY_MANIFEST.json`

Each original must exist byte-for-byte, with the original mode, under `audit/remote-publication/source-release/`. Other new files are allowed only below `audit/` and `evidence/`. Deletion is forbidden. Existing ignored build/runtime files are excluded using the article's actual Git ignore rules. The final Git Data root request replaces exactly the new article subtree and retains every other path from the fixed source root.

## Run after the final evidence copy

First complete the carrier documentation and copy all intended audit/CI evidence. Record actual observations; a queued run is not a successful run. Any copies of this helper bundle intended for the article must be made before generating the final manifest. The following commands do not themselves edit the article.

```sh
python /workspace/scratch/35c64a3513c5/new-round-carrier/prepare_evidence_carrier.py --prepare-only --output /workspace/scratch/35c64a3513c5/new-round-carrier/carrier-prepare-final
```

An output directory must be new or empty, outside the repository. Prepare-only mode verifies the fixed invariants but tolerates a stale delivery manifest and missing copies of the seven metadata originals. Its `provisional/` requests are explicitly not ready for publication. Inspect `INVARIANTS.json`, `MANIFEST_CHECK.json`, and `DELTA.json`.

The parent author process then installs this run's `DELIVERY_MANIFEST_PROPOSAL.json` as the article's `DELIVERY_MANIFEST.json`. The proposal excludes itself and includes every selected outer file, plus the unchanged dedicated workflow. Do not add or edit evidence after installing it; if anything changes, rerun preparation and reinstall a fresh proposal.

```sh
python /workspace/scratch/35c64a3513c5/new-round-carrier/prepare_evidence_carrier.py --final --output /workspace/scratch/35c64a3513c5/new-round-carrier/carrier-final
```

Final mode requires an exact manifest and all seven original metadata copies. It refuses a stale manifest before emitting any publication payloads. Require exit code 0 and `ready_for_publication: true` in `RESULT.json` and `UPLOAD_INDEX.json`.

## Publication recipe for the parent process

1. Use only the ready final run's `UPLOAD_INDEX.json`. It lists every required new unique blob, payload hash, byte count, conservative connector request size, and expected Git object identity. All source-article and recursively anchored predecessor blobs are already known and reused. Identical bytes across several paths require one upload.
2. Submit `text_tree_batches` to GitHub create-tree without a base tree. Their temporary paths are their blob SHAs; this uploads the text content objects. Verify each returned temporary tree SHA against `expected_git_tree`. Submit `binary_blob_batches` to create-blob and verify each returned SHA against `expected_git_blob`.
3. Submit the sha-only `article_tree` request, verify its exact expected article SHA, then submit the `root_tree` request using the fixed `base_tree`. Verify the root SHA. The root request has exactly one article-subtree entry; it does not include a workflow change.
4. Use `COMMIT_RECIPE.json` only from a ready final run. Its single parent is the published source commit above, and its message contains `[skip ci]`. Read the branch before updating it and require its head to equal the fixed source parent. Update without force. A changed head needs a fresh decision and preparation; do not overwrite it.
5. Preserve actual returned upload, tree, commit, ref, and readback receipts separately. This helper neither asserts that these remote actions happened nor claims any CI outcome.

Request files contain standard REST bodies. For the installed GitHub connector, map tree `tree` to `tree_elements`, map `base_tree` to `base_tree_sha`, and supply `repository_full_name: TrillionniumFoundation/theta-theory`. For blobs pass `content`, `encoding`, and the same repository name. The measured connector envelope reserves another 64 KiB below the 16 MiB request limit. New oversized binaries are reported as `binary_requires_authorized_packaging`; the helper never splits or changes article files. Any separately authorized packaging requires another manifest and final run.

## Output files

- `INVARIANTS.json`: exact frozen-source, workflow, archive, source-original and scope checks.
- `FILES.json`, `BLOBS.json`, `DELTA.json`: current selected files, reuse catalog results, and source-release delta.
- `MANIFEST_CHECK.json`, `DELIVERY_MANIFEST_PROPOSAL.json`: delivery closure and the scratch-only proposal.
- `ARTICLE_TREES.json`: independently computed nested article tree identities.
- `UPLOAD_INDEX.json`, `RESULT.json`: payload inventory, expected article/root trees, and final-readiness status.
- `payloads/`: final request bodies; `provisional/` is used in prepare-only mode.
- `COMMIT_RECIPE.json`: emitted only when final mode is ready.

## Actual helper checks already executed

`PREPARE_ONLY_EXECUTION.json` records the successful preparation on the then-current draft, with all 130 frozen inputs and all 4,393 predecessor files verified. Its provisional counts and tree SHAs apply only to that historical draft.

`FINAL_STALE_REFUSAL_EXECUTION.json` records a real final-mode attempt on 2026-10-21 at 01:42:27–01:42:30 UTC. It exited 2 because the delivery manifest was stale, with zero invariant failures and all seven metadata originals preserved. It emitted neither a payload directory nor a commit recipe. These are helper verification receipts; neither is a CI receipt.
