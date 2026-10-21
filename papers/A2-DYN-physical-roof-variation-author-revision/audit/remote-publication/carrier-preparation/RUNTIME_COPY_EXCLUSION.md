# Publication-helper runtime-copy correction

The original helper and its original hash-bound bundle are preserved unchanged. The first root final-mode run refused the stale manifest with zero source/archive/workflow invariant failures. Its exact `MANIFEST_CHECK` and `RESULT` are retained here. The proposal had briefly included four runtime copy-stage files that had disappeared by the second inventory. No publication payloads or commit recipe were emitted.

`prepare_evidence_carrier_stable.py` differs in one directory-walk condition only: it excludes the filesystem synchronizer's transient `.rsync-tmp` directories at every depth. Every published source inventory path and every immutable predecessor anchor path was checked first; none uses this directory name. This excludes no archived or published source file. The helper continues to check all 130 frozen inputs, all 4,393 predecessor files, original metadata versions, source manifest, workflow, complete intended outer-file inventory and final tree identity. No mathematical source was changed.

The exact one-line diff is `RUNTIME_COPY_EXCLUSION.diff`. The original helper bundle manifest binds the original program; the complete final delivery manifest separately binds this corrected program and this note.
