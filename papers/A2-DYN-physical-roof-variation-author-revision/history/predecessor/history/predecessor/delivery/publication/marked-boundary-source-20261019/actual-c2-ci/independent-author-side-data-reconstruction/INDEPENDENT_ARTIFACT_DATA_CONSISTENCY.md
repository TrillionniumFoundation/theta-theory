# Independent author-side consistency and actual execution: C2 artifact data

## Conclusion and exact scope

The separate artifact-data checker was independently read and actually re-executed successfully. Its data conclusions agree with a second reconstruction from the saved raw API responses, original job-log bytes, ZIP members, command receipts, and PDF. This is an author-delivery integrity check, not a referee report, a continuum mathematical proof certificate, or a successful verification of structured workflow completion.

The tested commit is **`efde9fa6c45e7835989b653622a9870e59027530`** (C2), root **`b5d618b8a4b356f8ca07f1c9f1238e35d879ede8`**, article **`b4add0580cc8211223dfa57e6e618e2bf9546d09`**. The actual run is **39281615689**, job **118156848926**, artifact **12201151164**. No future C3 execution or workflow status follows from this report.

The fixed structured API objects used here were observed at approximately **2026-10-19 16:10:07 UTC**. They contain run/job `queued`, null conclusions and an empty job-step array. Those exact objects remain intact. The output explicitly states `workflow_completion_verified=false`, `job_steps_completion_verified=false`, and `synthetic_status_steps_or_timestamps_used=false`. Later API observations, including any change to `in_progress`, are separate timed evidence and do not replace these recorded fields.

## Programs and preserved strict failure

The original strict verifier is byte-identical at SHA-256 **`e44db871d6afaea2aaac23ec836ceb1e57993ecb464afcf884475530b1e7b42f`**. Its actual invocation stopped with exit code **1** at the original completed/success gate, with `RuntimeError: Actual run completed successfully`. The actual stdout is empty; stderr and the complete execution receipt are preserved in the CI packet's `strict-verification-queued-161007/`. No original gate, status, conclusion, timestamp, step, or main function was overwritten.

The inspected separate checker is `verify_actual_artifact_data_only_v2.py`, **30,731 bytes**, SHA-256 **`333214be9f891b8dab1518ad2311899d94f25fe457708e6025678efe8a5a52cd`**. It imports only the hash-pinned original module's parsing and identity helpers, never invokes that module's `main`, never replaces its `require`, and never imports or executes archive code. The actual local re-execution used `PYTHONDONTWRITEBYTECODE=1` and a new output directory. The source uses its own ordinary failing checks for every data condition.

One precision correction was requested during this author pass: the original exact job log begins with a UTF-8 BOM. The first data-checker version's anchored timestamp expression missed the first line and reported the next timestamp. Version 2 accepts the preserved initial BOM when parsing, without altering any log byte. The true first timestamp is **`2026-10-19T15:55:55.6914264Z`**. The complete v1 source, original output and execution remain preserved in the CI agent's packet. The only v1-to-v2 differences are the expression and two explanatory comment lines.

## Actual independent executions

The v2 checker was actually run here from **16:22:46.452903 to 16:22:54.757838 UTC**, exit **0**, with empty stderr. Its full output is in `data-result/ARTIFACT_DATA_ONLY_VERIFICATION.json`; `ACTUAL_EXECUTION.json`, `INVOCATION.json`, `stdout.json` and `stderr.txt` record the actual invocation and returned bytes.

The independently written `check_data_scope_v2.py` was actually run from **16:25:49.929307 to 16:25:50.523427 UTC**, exit **0**, with **366 passing checks**. Its report is `INDEPENDENT_DATA_SCOPE_CHECK.json`; the complete actual second invocation and outputs have the `SCOPE_CHECK_V2_` and `scope-v2.` prefixes. This second program does not import the strict verifier or data checker. It directly reads the original raw responses, ZIP and reports.

The initial second-reconstruction program used the wrong ancestor count in one local input path and failed before reading its first checker input. That actual failure and original program are retained in `check_data_scope.py`, `SCOPE_CHECK_EXECUTION.json` and `scope.stderr.txt`. The corrected version changes only `HERE.parents[3]` to `HERE.parents[2]`. No condition was weakened and no input or result was edited to achieve the subsequent pass.

The independently generated v2 data report and the CI agent's v2 data report agree on **every field except the two execution-clock fields** `started_utc` and `finished_utc`. Complete archive-member identity lists and checked-local-input lists are retained in `data-result/`.

## What the actual bytes establish

| Object | Actual checked scope |
|---|---|
| Downloaded artifact | 11,125,810 bytes; SHA-256 `3dd55cb52656fea0ec950367067a4a27a6ad08ebed77fd5ee0b4400d7f7ae604`; advertised API digest and size agree |
| ZIP members | 249 unique files; every member read, CRC checked, and SHA-256/Git blob identity recomputed |
| Expected source | Complete C2 staged inventory of 3,596 files and 156 directory hashes reconstructed |
| Frozen source | Schema 5, 1,837 source files, 139,367,900 bytes, all four immutable anchors preserved |
| Actual local inputs read by v2 | 2,935 unique checked source/reference files; byte identity and mode tied to the tested inventory |
| Mathematical/native input set | 107 native/tool files; fingerprint `ee0bd027bf5b4263ea5c6eebfb8ffe2d24c8fa0b21d1187f0967bfcaf0a221a5` |
| Native source graph | 59 complete core bodies, 69 reachable TeX files, 897 labels, 86 labels in the new bodies |
| Mathematical execution records | All 52 distinct required command receipts, declared arguments, exit codes 0, actual output sizes and hashes |
| Normal/optimized comparisons | All 43 declared pairs independently compared as actual bytes |
| Native execution records | Four command receipts: three actual `pdflatex` passes and one actual PDF inspection |
| Current native PDF | Independently read as 195 pages; 1,659,306 bytes; SHA-256 `b54be63ba6088a96f957e8736227cf61a18a5bbf7b28613254e263207a87ead2` |
| Native auxiliary file | SHA-256 `ca813cb5f7103352269d49f2f67b30d33464d8fae19a4676db87228253a3a914`, identical to the actual final local build's auxiliary file |
| Historical rebuild | One actual fresh post-native receipt, 9 commands, 390 historical source files, complete 26-page main and 883-page supplement PDFs |
| Original reports | 90 original retained report files plus the distinct original v73 report, each tied to exact source identities |

The current CI PDF is identified by its own exact bytes. No claim is made that it is byte-identical to the earlier local PDF; the actual auxiliary file, page count and tested source identities agree. The checker does not extract the archive or execute any code from it.

The exact job log runs from **15:55:55.6914264 to 15:59:35.0330612 UTC**. The archived source/math/native phase is **15:57:49.505755–15:59:02.429940 UTC**; the fresh historical rebuild is **15:59:02.472998–15:59:27.781466 UTC**. These intervals were checked against the actual log timestamps. They are not fabricated API job-step timestamps. The report explicitly leaves `phase_within_structured_run_update_interval_verified=false` because the fixed structured response has not supplied an adequate completion interval.

## Evidence lineage and publication limits

The second reconstruction checked the raw binary API response and parsed-object identities for both run and jobs, then compared all parsed objects to the assembled observation. It separately reconstructed the artifact object from its original actual GET record. The original job-log response text encodes to exactly the saved log bytes, including the BOM and absence of an appended newline. The strict failure record and outputs match their saved identities.

All work here is confined to this new scratch audit directory. Existing C1/C2 audit directories, scientific source, workflow, frozen manifest, original CI program and CI packet outputs were not edited. The preparation of a final Git verifier is separately identified as preparation. Neither this actual C2 artifact-data report nor the verifier's existence proves that C3 has been published, that any later head has run CI, or that the complete raw pointwise local-limit theorem has been proved.

The original full workflow verifier's completed/success requirement remains the requirement for a full successful CI verification. If a later authoritative actual response satisfies it, that response and a separate strict execution must be retained as new evidence; the observations and failures in this packet remain historical facts.
