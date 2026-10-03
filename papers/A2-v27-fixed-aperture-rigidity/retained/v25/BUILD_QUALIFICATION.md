# A2 v25 qualification record

## Actual local execution

`verification/local/receipt.json` is the unmodified output of `tools/validate_v25.py --output-dir verification/local`. It records a passed primary-only source-content execution, not a Git checkout. Ordinary and optimized Python produced identical output with 5,490 finite checks. The primary PDF has 22 pages and its final TeX diagnostics list is empty. The source manifest before and after execution agrees.

The seven actual command logs are archived in `verification/local/logs.zip`. Each filename and SHA-256 is listed in the receipt. This archive is execution evidence, not an encoded source-distribution or restoration mechanism. No physical sensor was executed, and no retained-volume compilation was performed locally in this run.

## Current-SHA hosted qualification

`.github/workflows/a2-v25-verify.yml` is a read-only workflow. It checks out the exact triggering SHA, verifies the complete current source manifest and the native retained-v24 and Supplement-S trees, reruns the new checks, and builds the current primary. Full-package mode then calls the unchanged v24 validator from `retained/v24` with its own current-SHA checkout requirements. Its receipt remains nested under its original schema and must report the same current commit, rather than being relabelled as an old run.

This produces the current primary plus the seven declared inherited documents. Raw historical v18 and Supplement-S layout diagnostics remain archived before reversible staging-only layout insertions. The inserts do not change tracked source or mathematical text. The unchanged historical validator documents these exact adjustments. The artifact upload runs even after failure, so a failed gate remains visible.

This file records the qualification mechanism and the actual local result; it does not assert a successful v25 hosted outcome before that run completes. The branch and workflow provide the authoritative current status.

## Historical v24 execution

The controlling referee report confirms that run 37107483439 succeeded at reviewed commit f5754f7eacc5b2bde9450de154a4e4c0093b3e23. The earlier run 37106889506 failed the retained Supplement-S warning gate. Both belong to the unchanged v24 history. Neither is evidence that this v25 commit was built.

All these records concern finite source/build reproducibility, not formal mathematical proof certification or independent editorial review.
