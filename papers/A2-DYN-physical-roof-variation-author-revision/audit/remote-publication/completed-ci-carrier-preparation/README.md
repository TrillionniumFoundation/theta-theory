# A2-DYN completed-CI evidence carrier preparation

This new helper bundle prepares an evidence-only child of the already published pending-CI carrier. It reads the local article and fixed receipts, and writes only to a new scratch output directory. It has no network calls, article edits, index writes, Git object writes, commits, or ref updates. The parent author process owns all metadata changes, CI interpretation, and publication.

## Fixed identities

- Repository: `TrillionniumFoundation/theta-theory`
- Branch: `revision/a2-dyn-physical-roof-variation-2026-10-21`
- Required carrier parent and expected old branch head: `d46ba004ff1ac8d44dab04549daff7e3c0e5f205`
- Mathematical source commit: `6708e30d1e8511e6ed2f4e3a6247c09628bd3ea9`
- Parent root tree: `3ec1a39998cef76f23fc1985a0df78bc0033bf4c`
- Parent papers tree: `e3b1f54549d9933b3d5458f17ed424d17040676c`
- Parent article tree: `2c542d7a279a7bc6fb8ea64dfa372e9bc1dcd9e4`
- Immutable predecessor tree: `7bcaba2bc1ef7ab393c81a7df84f3e45983c4dfa`
- Unchanged workflow blob: `6246879e13fdd5937ebf9c5a9787c24baefb59b5`

The outer baseline comes from the 1,102 entries in the actually published first carrier's `new-round-carrier/carrier-final-stable/FILES.json`; its hash and origin are recorded in `SOURCE_RELEASE_BASELINE.json`. The 130 frozen mathematical/build inputs, source manifest, predecessor anchor and complete predecessor inventory, and workflow retain their original fixed identities. Runtime modification times and encoding classifications are not content identity fields and are omitted from the fixed baseline.

`SOURCE_PARENT_COMMIT.json`, `SOURCE_ROOT_TREE.json`, and `SOURCE_PAPERS_TREE.json` are actual pinned GitHub GET bodies obtained for this bundle; `GITHUB_READ_RECEIPTS.json` records their URLs and observation times. The helper verifies the parent-to-root binding, the parent’s mathematical-source parent, the root-to-papers-to-article bindings, the two complete nonrecursive tree hashes, and the article tree reconstructed from the fixed outer inventory plus immutable predecessor. These receipts do not establish a CI outcome; the parent process supplies actual workflow/run/job evidence separately.

Keep the helper, baseline, and three source receipts together. The default local repository is in the baseline; `--repo /absolute/path` overrides it. No file in the previous helper bundle is changed by this bundle.

## Permitted changes and exact retention

All existing files in the d46 baseline are immutable except the following seven article-root metadata documents:

- `PUBLICATION_STATUS.json`
- `VALIDATION.md`
- `README.md`
- `HISTORY_PRESERVATION_AUDIT.md`
- `RESPONSE_TO_REFEREE.md`
- `PROOF_DEPENDENCY_LEDGER.md`
- `DELIVERY_MANIFEST.json`

Each of these must have an exact byte-and-mode copy under `audit/remote-publication/pending-carrier/` in the final article. The retention path is configurable through `metadata_snapshot_path` in the fixed baseline or the optional `--metadata-snapshot-path` argument; an override must be below `audit/`. The retained versions are compared to **d46**, not to the older 6708 source-release originals. The existing source-release snapshots are independently protected as immutable d46 files.

No existing file may be deleted. All other additions must be inside article `audit/` or `evidence/`. The workflow remains unchanged. The helper excludes `.rsync-tmp` directories at every walk level, the preserved predecessor from the outer inventory, and ignored build/runtime files using the actual Git ignore rules. It verifies the predecessor separately. The final root-tree request replaces exactly this article subtree using the pinned d46 root as its base; all other repository paths are retained.

## Prepare and finalize

Complete the intended evidence copies and seven metadata updates before preparing the manifest. If this bundle is to be archived in the article, copy it before manifest preparation. The following commands perform no article writes:

```sh
python /workspace/scratch/35c64a3513c5/new-round-ci-carrier/prepare_evidence_carrier_stable.py --prepare-only --output /workspace/scratch/35c64a3513c5/new-round-ci-carrier/carrier-prepare
```

Use a new or empty output directory outside the repository and helper root. Prepare-only mode verifies all immutable identities and change restrictions, but permits a stale delivery manifest or missing metadata retention copies. Its `provisional/` bodies are not ready for publication. Inspect `INVARIANTS.json`, `DELTA.json`, and `MANIFEST_CHECK.json`.

The parent author process then installs `DELIVERY_MANIFEST_PROPOSAL.json` as the article-root `DELIVERY_MANIFEST.json`. The proposal excludes itself, covers all selected outer files and the dedicated workflow, and explicitly declares `parent_commit=d46…`, `mathematical_source_commit=6708…`, and the metadata retention path. The final check validates both distinct commit fields. Any later evidence changes require a fresh proposal.

```sh
python /workspace/scratch/35c64a3513c5/new-round-ci-carrier/prepare_evidence_carrier_stable.py --final --output /workspace/scratch/35c64a3513c5/new-round-ci-carrier/carrier-final
```

Final mode requires an exact manifest and all seven exact d46 metadata snapshots. A stale manifest or failed invariant causes refusal before any publication payload is emitted. A final result is usable only with exit code 0 and `ready_for_publication: true`. Its `COMMIT_RECIPE.json` has the sole parent d46, expected old head d46, `force: false`, and message `Record completed A2-DYN source CI evidence [skip ci]`.

## Publication handoff

The parent process reads the branch head again and checks the expected d46 head before publication. A moved branch requires a fresh decision; the helper cannot authorize overwriting it. Use only the ready run's `UPLOAD_INDEX.json`, verify every payload hash and returned Git object SHA, upload the new unique text/binary blobs, create the exact article/root trees, then use the final commit recipe. Existing d46 and predecessor blobs are reused by identity. GitHub connector tree calls map REST `tree` to `tree_elements` and `base_tree` to `base_tree_sha`, with `repository_full_name` supplied separately.

Request sizing preserves the previous stable helper's 16 MiB limit and 64 KiB margin. Oversized new binaries are reported without splitting or modifying article files. The helper records changes during preparation and blocks unstable payloads. It does not claim that remote publication or CI verification occurred merely because preparation succeeded.

## Actual local check

`STALE_MANIFEST_CHECK_EXECUTION.json` and `stale-manifest-check/` preserve the single actual final-mode check performed while preparing this bundle. Its result and identities apply to that observed local snapshot only. It is a check of immutable-file/manifest guards, not a mathematics test, source rebuild, CI run, or publication receipt. No new mathematical verification or compilation is required by this evidence-only helper task.
