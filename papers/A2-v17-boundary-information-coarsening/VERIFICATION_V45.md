# A2 v45 verification ledger — source checkpoint

The mathematical baseline is `b229bfa2df2962ea2ebfd0fb2fd11531036d33a6`; the addressed report is `c984b5a5f0dee0e3a9c78264ff7b5136272fec72`. The source branch is `revision/a2-v45-generic-finite-channel-rigidity-2026-09-14`.

The final delivery ledger will distinguish this mathematical source commit from native product and later documentation commits. No GitHub Actions success or fetched-product publication is attested by this source-checkpoint document before it occurs.

The preservation diagnostic checks 97 inherited active manifest entries, the 98-input new main closure, the unchanged companion, and static references. The finite geometry/image diagnostic checks disk skeletons and image-stage algebra, including negative controls. Neither proves the mathematical statements.

Reproduce from a committed checkout by running `tools/check_revision_v45.py` and `tools/check_skeleton_v45.py` in ordinary Python and under `python3 -O -B`, comparing outputs. Run `tools/build_submission.py --output-dir <empty-directory-outside-paper>` for both full native entries. The build freezes committed source, records the companion-generated auxiliary input consumed by the main, disables shell escape, and fails on unresolved references, duplicate labels or missing glyphs.

The v45 workflow publishes only to a new revision products branch. It force-stages the declared delivery subtree, verifies the Git index, pushes, fetches, verifies the actual committed blobs, and records a separate attestation. Native PDFs, source ZIP, raw logs and evidence are retained in Git. A preparation receipt alone is not a publication certificate.

Readable-resolution visual inspection and final hashes/page counts belong to the completed delivery ledger. A successful native build or finite diagnostic does not constitute a full mathematical or editorial acceptance certificate.
