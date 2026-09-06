# Current revision validation

`referee_rerun.json` records execution of the unchanged twelve-test referee script; its `pdf_built_or_inspected: false` concerns that diagnostic script, not the separate principal PDF build. `revision_checks.json` records the 27 new finite diagnostics. `build_receipt.json` records the three-pass build of the 22-page principal manuscript and the exact hashes of all 15 build/test source files. `visual_audit.json` records inspection of the rendered principal PDF. `publication_receipt.json` records comparison of those source hashes to actual GitHub tree objects.

All receipts concern this execution, with their stated scopes. Finite tests are not theorem proofs or independent referee acceptance. The corrected foundation companion was not compiled, and the historical eleven-paper author suite was not rerun. Its retained validation files are historical, not these current receipts.

`python build_and_verify.py` regenerates the test receipts and build receipt and writes console logs locally. The recorded PDF binary is supplied with the conversation delivery rather than committed in this directory; its SHA-256 is in the build and visual receipts. A new build can differ in PDF metadata/timestamps without a source change.
