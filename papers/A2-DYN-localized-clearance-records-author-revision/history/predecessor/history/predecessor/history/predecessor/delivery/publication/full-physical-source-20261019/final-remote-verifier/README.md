# Standalone final publication integrity gate

`verify_final_remote.py` is ready for the actual final metadata commit. Its
preparation includes syntax and CLI checks only. **No C3 verification result is
claimed until the actual C3 commit/ref/tree readbacks are supplied and the
program succeeds.** No additional regression suite, mathematical program or
native build was run during this preparation.

The program performs no API calls and writes only to a selected output directory
outside the article. It has an independent canonical Git tree implementation;
it does not import the transport adapter or execute an article helper.

## Required inputs and checks

The required CLI inputs are actual saved `--readbacks`, a complete `--expected`
file inventory, the planned root `--scope`, the complete `--previous` carrier
inventory, and the actual `--head` and sole `--parent` commit SHAs. All file,
byte, subtree and source-input counts are derived from these inputs.

The gate verifies:

- The actual commit, sole parent, three publication refs, all article files,
  every descendant subtree and article root, and all four repository control
  trees. Every actual file mode/blob/size must equal its frozen expected identity.
  Recursive and control-tree responses must be complete and nontruncated.
- Every repository sibling against the pinned base and planned trees. The only
  allowed repository paths are the isolated current article and its dedicated
  workflow. The actual workflow must match its article-local `ci/` copy.
- Zero deletions from the previous carrier. Existing-file changes are confined
  to `PUBLICATION_STATUS.json`, `PUBLICATION_RECEIPT.json` and
  `REMOTE_TRANSPORT_STATUS.md`; all three must be explicitly excluded by the
  unchanged source manifest. Additions must stay under this iteration's
  publication/source-gate prefixes.
- Every frozen source input's Git blob, SHA256, byte count and mode, the complete
  consecutive native core closure, and the exact mathematical fingerprint from
  root/core TeX and Python tools. The previous/current fingerprints must match.
  The pinned manifest identity is
  `13182b20479bcafcd8a3d53804b9cc610739e5a8ad0fb94f32eed65b4768f997`.

`inputs/SOURCE_MANIFEST.json` is an exact copy of that already published manifest.
Its default use makes the verifier independent of the article filesystem. A
different location can be supplied with `--manifest`; its hash must still match
the same pin. Archiving this copy at a new delivery path reuses its existing Git
blob identity.

## Recommended additional parent and census evidence

Supply `--previous-readbacks` with the actual C2 readbacks. This adds a direct
parent-commit/control-tree linkage check: C2-to-C3 may update only the current
article pointer under `papers` and its root ancestor. The entire `.github` and
workflow trees must be unchanged. Without this optional input the report
explicitly distinguishes the planned/pinned-base sibling check from a direct
actual-parent comparison.

The optional `--old-census` and `--current-all-refs` must be supplied together.
They must contain complete branch lists and ordered, exhausted page receipts.
All existing non-target A2-DYN refs must remain exact. The three authorized new
publication refs may advance to the supplied head. Unrelated ref movements are
listed without attributing them to this publication. Additional new A2-DYN refs
produce an explicit scope observation requiring attribution. Without these
inputs the verifier makes no claim that all old refs were freshly rechecked.

## Invocation after actual C3 readback

Replace `ACTUAL_C3_COMMIT_SHA` and use the actual readback filename:

```sh
python -B iteration-20261019b/final-remote-verification/verify_final_remote.py \
  --readbacks iteration-20261019b/C3_FINAL_REMOTE_READBACKS.json \
  --expected iteration-20261019b/C3_FILE_IDENTITIES.json \
  --scope iteration-20261019b/C3_ROOT_EXPECTED.json \
  --previous iteration-20261019b/C2_FILE_IDENTITIES.json \
  --head ACTUAL_C3_COMMIT_SHA \
  --parent 228ec6a639d4d195a1a8b869a04dae6f49fece0e \
  --previous-readbacks iteration-20261019b/C2_INITIAL_REMOTE_READBACKS.json \
  --output-dir iteration-20261019b/final-remote-verification-results
```

The program archives the exact supplied input bytes with SHA256 identities and
writes complete file/subtree/sibling/frozen-input tables, the fingerprint rows,
the metadata delta and `FINAL_REMOTE_VERIFICATION_RECEIPT.json`.

Any run lookup supplied in the actual readback is preserved as an observation
with its exact head, status and conclusion. The gate does not infer a completed
CI result, borrow the parent's CI success, claim another download of every blob
body, or certify the continuous mathematics. The actual completed C2 CI packet
and the metadata-only final C3 publication remain separately identified.
