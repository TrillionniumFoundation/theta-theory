# R74 provenance inventory

Current control and selection records are `BASELINE_LOCK.json`, `BASELINE_AUDIT.md`, `BASELINE_SOURCE_IDENTITIES.json`, `BASELINE_REFRESH_RECEIPT.json`, `CURRENT_SCAN_RECEIPT.json`, `CURRENT_REFS.json`, `ALL_CURRENT_HEAD_METADATA.json`, `NEW_COMMITS.json`, `NEW_TEXT_OBJECTS.json` and `REFEREE_STATUS_AT_BASELINE.md`.

`current-full-scan/` is the fresh 20 October full scoped ancestry inventory, decoded text index, issue-line index and Git diff occurrences. Its exact receipt and the separate corpus identity are explained in `../SOURCE_PROVENANCE.md`. `refresh_baseline.py` records the current incremental comparison. The predecessor scanner and classifier are preserved under `../inputs/r73/provenance/` with their original scope. The final remote delivery refresh belongs in the publication evidence because it occurs after source sealing.

`R65_REFEREE_REPORT.md`, `R65_REPORT_COMMIT.json` and `R65_HOSTED_TERMINAL_RECEIPT.json` are exact historical controlling evidence. The terminal CI success belongs only to the stated R65 SHA. `PINNED_INDEPENDENT_TREES.json` fixes original companion locations. `CURRENT_RETAINED_BODY_IDENTITIES.json`, `SUPPLEMENT_SUFFIX_IDENTITY.json` and `R73_FILE_PRESERVATION.json` bind retained bytes, with current strict checks implemented by `verify.py` and `seal_source.py`.

`R74_PROOF_DEPENDENCIES.json` is the current twelve-statement detailed addendum. `author-research/` retains derivations, separately assigned AI challenges, exact finite diagnostic outputs and development snapshots. Its `superseded/` subdirectory contains the duplicated R68 restatement and weaker dictionary lower, neither included in the active manuscript. Development records preserve the conclusions and hashes true at their stated cutoff; current main source, corrected dependency map and final build receipt control the delivered edition.

Older R73 control objects, branch inventories, delivery receipts, reconstruction notes and proof challenges remain under `../inputs/r73/`. They are neither erased nor treated as fresh R74 evidence. No source inventory, AI challenge, historical CI receipt or PDF build is a human referee report, formal proof or editorial decision.

Some redundant old top-level provenance copies are also retained. The exact path list is `R73_FILE_PRESERVATION.json` under `historical_provenance_archival_locations`; these are historical R73 evidence only. The explicitly named current records and `current-full-scan/` above control R74. Their presence does not make an old scan or receipt current.
