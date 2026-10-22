# Actual execution evidence

The five execution bundles preserve actual stdout/stderr logs, per-command receipts, details JSON, compiler logs and recorders, and generated files. EVIDENCE_INDEX.json records every archived path, byte count and SHA-256 and each bundle hash. Every bundle was reopened and all entries verified byte for byte before the uncompressed working copy was removed. Extract a bundle into a fresh directory with the standard tar -xzf command.

- baseline-reconstruction.tar.gz retains the successful 195-page baseline build and source verification, the initial missing-dependency failures and the complete successful pinned rerun.
- historical-reconstruction.tar.gz retains the first separate original 390-file historical reconstruction.
- preliminary-typeset-321.tar.gz is a real but intermediate 207-page build through 321; it is not final-322 verification.
- current-execution.tar.gz is the final frozen native source, 62-command mathematical and 211-page typesetting execution.
- current-history-execution.tar.gz is the second real historical reconstruction through the new isolated wrapper used by the dedicated CI.

The uncompressed top-level summaries are exact copies of the corresponding final execution records. Standalone final PDFs are in ../compiled/. The actual command receipts retain their original execution paths and timestamps. No output is rewritten to look as if it ran from its archive location.

Finite computation and successful typesetting do not certify continuous physical geometry or the unclosed full raw local limit theorem. Current GitHub Actions evidence is recorded separately once a real run has completed.

Loose copies of earlier baseline and historical execution records, when present, retain their original scope. The indexed bundles bind the exact complete executions described above; a duplicate loose copy is not a new run.
