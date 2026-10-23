# Independent source-provenance findings for the continued author revision

## Baseline decision

Continue the actual complete R78 native mathematical source at commit `e0377beea364e456af2301f5e4fec98fe343cbcb`, repository tree `f17e457a57a2a7f14d1fe4996258dde167ea678f`, paper directory `papers/General-Theta-Foundations-I-restart/r78-reset-memory-frontier`, paper subtree `072a5a8c7b251964c0f5ba8c1c109d88a93302ee`. Its direct parent is R77 publication commit `300807bad3eb00ad8e1975ae9ff1ea1971a333db`; R77 source is `18b76a739898d2734c4f5bfcb609db0786cd4c11`, subtree `c48519790add40e3c67aa245aa8e5ee1fcc47de6`.

The R78 source is a real, readable 694-file manuscript/supplement/companion and evidence packet, not an empty branch or a partial transfer. Its complete source seal was independently executed and passed: manifest SHA-256 `b7da627688f49b12046a63dff12a59e9bcdfd51bdd5eb2875cc64d193b9bb6c1`. The retained proof-body checks cover 235 predecessor statement labels, 59 prior current proof files, all 622 R77 predecessor files (601 at the same path and 21 archived explicitly), and all 34 R58 companion files. The companion tree is `007a1d7d5f5b880c670fc6f47a812ebd476bfb00`.

**A source/publication distinction matters.** At this snapshot R78 is a source commit only. No R78 publication child or sibling publication directory is deposited. R78 README/START_HERE contains prospective links and page counts for that missing publication. Those links must not be reported as actual published PDFs or a completed strict run. The latest deposited publication is R77. The parent revision task subsequently completed a fresh strict native build of these exact sources at 2026-10-23T07:00:38Z: all 27 diagnostic suites passed, the native main/supplement/companion compiled to 45/190/37 pages, and the receipt declares and verifies source commit `e0377beea364e456af2301f5e4fec98fe343cbcb`. The actual receipt is retained as `R78_FRESH_NATIVE_BUILD_RECEIPT.json`; this is a local native build, not a previously deposited R78 publication or hosted CI run.

## Controlling and historical reports

The latest applicable deposited substantive report is R65 at `358481b21ceeeedb1205ebd30f86982e32a2cb04`, original path `GENERAL_THETA_FOUNDATIONS_I_RESTART_R65_BOUNDARY_MEMORY_EXTERNAL_REFEREE_REPORT_R65.md`. Its Git blob is `d1ff9c5662390156ee212c82b173e86a21180e84`; SHA-256 is `8c7d45d762736009fda667621fdf5019fa934f5f45f39364c747f837e6d7343c`; its length is 45,974 bytes. These values were checked by reading the file at its original commit, not by trusting copied metadata.

The report assesses R65 source `0469eb4f852eeea953cb3725d4b34dfdd2bf9d36`, publication `ee79ca9114f8009d62c056d07381b766645e3fc4`, and paper subtree `3a0ea744d1e4721f2c47b5e038023becd4da2ce0`. It did not assess R66–R78. Substantive intervening author answers must be inherited; R65 controls its genuinely surviving concerns, not an artificial reopening of all fifty comments. No new independent review of R77 or R78 is present.

Fresh original-commit reads also authenticated:

| Report | Commit | SHA-256 |
|---|---|---|
| Original-paper v94/R62 | `58581d5a6391642fb0849f8c8bb49c8c0c20b63c` | `e03df5d0b8a5ddbd4b9d2f889435ce71477710b1291a2d35326fb5a260958b29` |
| Restart R59 round 3 | `c39922c242f9bd03d2e0d7f05d6e9b483362e26d` | `42781c496f741c20fd5acb88c0fc1640db9478780abbb39e891202779fbae306` |
| Restart R64 | `0a66ca2ede7835ede2a62fe2363ba5dd3ccd2ed8` | `fbabcc131fb448f737fb71a13d93e509e8ff2be191a75649e19cccedb55a465f` |

The v96/R63-named review branch is still the author-verification head `e38f757ee13158c315e9328c961eb84e3e9a000d`, with no distinct R63 report. The R71 proof-clarification head `ecc9b7b26acc4000527295a6dc1755bfffd2f1b4` is an older-line patch whose valid clarifications are already inherited. Pipeline audits, author-team challenges, copies of old reports, workflow records and A1/A2 reports do not become new General Theta independent reviews. Human identity or a commissioned editorial origin is not established merely by a report's filename.

## Full current graph and historical text census

The fresh snapshot contains **1,307 remote branch heads**, **873 distinct head commits**, and **2,711 ancestor commits**. The earlier number 1,308 from `for-each-ref` included the symbolic local `origin/HEAD`; it is not a remote branch. Every distinct head commit payload was read and SHA-1 authenticated. Relative to the frozen R78 pre-source census of 1,306 refs, the only addition is the R78 author branch and source commit. No old ref moved or disappeared. All 132 General Theta review refs remain unchanged.

The current full-history raw-diff traversal identifies **1,057 scoped changing commits**, **175,967 scoped versioned paths**, and **7,201 distinct text blobs**. All 7,201 were actually read, decoded and authenticated, totaling **112,371,368 bytes**. Of these, 7,137 historical blobs (108,165,876 bytes) were streamed from the retained, hash-pinned archive parts/deltas without extracting a second corpus; 64 new R78 source blobs supplied the remaining text. There are no new report candidates, no missing archive members, no duplicate archive members, and no hash mismatches. Four legacy LaTeX logs are decoded by byte-preserving Latin-1 as previously indexed; original bytes remain the hash authority.

The scope is every snapshotted remote head and its ancestors, selecting General Theta/GTF-I versioned text plus shared shallow repository governance, pipeline, audit, review, response and dependency records. This is source retrieval and identity authentication, with lexical issue indexing. It is not a claim to have independently re-proved every historical theorem or to have obtained independent human review.

All twelve central historical mathematical dependency identities were rechecked against actual commit trees. Their selected manuscript/manifest blob hashes were matched against the freshly reauthenticated corpus. This covers R72–R76, the original v96 line, the R58 companion and the separate TR-OMG/TR-OMD sources.

## Concrete audit artifacts

`provenance_current/` contains:

- `CURRENT_REFS.json`, `REF_DELTA_FROM_R78.json`, `ALL_HEAD_COMMIT_IDENTITIES.json.gz`, and `ALL_ANCESTOR_COMMITS.txt`.
- `CURRENT_CENSUS_RECEIPT.json`, `CURRENT_HISTORICAL_TEXT_INDEX.json.gz`, `HISTORICAL_BLOB_VERSIONS.json.gz`, `NEW_TEXT_INDEX.json.gz`, `NEW_ISSUE_LINES.json.gz`, and `NEW_REPORT_CANDIDATES.json`.
- `HISTORICAL_ARCHIVE_AUTHENTICATION.json`, `R78_SOURCE_SEAL_CHECK.json`, and `R78_SOURCE_AUTHENTICATION.json`.
- `CONTROLLING_AND_HISTORICAL_REPORTS.json`, exact four original report bodies in `reports/`, and `HISTORICAL_DEPENDENCIES_RECHECK.json`.
- `refresh_census.py`, a read-only reproducer taking explicit repository, source-root, ref-snapshot, archive-receipt and output arguments.
- `ALL_HEAD_CONTENT_CATALOG.json.gz` and `HEAD_CONTENT_CATALOG_RECEIPT.json`: the completed tree-level catalog covers every one of the 873 distinct heads and 1,307 refs. Actual General Theta content appears at 372 heads reached by 527 refs. The catalog maps every ref to native entrypoint identities, report blob identities and actual tip file deltas; it does not infer source completeness or review independence from a filename.

The archive authentication can be reproduced with the unchanged R78 `provenance/r78-audit/verify_history_r78.py`. The census can then be reproduced by supplying the exact source directory and fixed ref snapshot to `refresh_census.py`. The new portable `verify_current_history.py` additionally authenticates the exact 64-blob `HISTORICAL_TEXT_DELTA_R79.tar.gz` and all 873 raw Git head-commit payloads without Git or network access; it checks the extension from 7,137 retained to 7,201 current indexed text blobs. Run the inherited R78 checker and the new checker together to authenticate all 7,201 payloads in a fresh run. `CURRENT_HISTORY_MANIFEST.json` pins the new archive, indexes, snapshot and raw commit-object pack. Neither checker changes a branch, commits files, pushes remotely, or extracts archive paths. The optional new-checker receipt must be outside the source directory.

## Surviving scientific concerns, without reopening valid closures

R78 already provides the complete finite-memory reset frontier, same-command-row deterministic report update, semidefinite failure-effect coverage, exact action-cover model formulas, and continuity of strict resource gaps. These are the mathematical starting point, not a requested new rebranding of R65's special sign example.

The original general-M squared-sign decision-risk frontier remains a separate unresolved problem. The unrestricted-decoder stopped-response log-log lower versus logarithmic upper gap also remains separate. Nonreset or optional-stopping general control, independent timing, and A1/A2 or larger Theta goals are not completed by a reset theorem. An author revision should strengthen the actual current theorem chain while keeping these distinctions and all valid prior proofs intact. No byte authentication, native build, finite diagnostic or internally authored challenge resolves the journal-level significance question by itself.
