# R80 baseline and historical-content audit

Begin with `BASELINE_SELECTION.md` and `BASELINE_LOCK_CURRENT.json` for the
actual complete R79 source/publication and controlling R65 report identities.
`REFEREE_CARRY_FORWARD_MATRIX.md` separates all ten major and forty technical
R65 requests from the inherited historical obligations. It is an author-side
issue analysis, not a new referee report.

The current source selection is independently supported by the exact remote
source/publication trees, all 806/23 local file authentications, source-seal and
publication-integrity executions, and checks of the three baseline PDFs'
hashes, page counts and first-two-page text readability. Those records do not
claim a newly executed R79 native compilation or full visual inspection.

`CURRENT_REFS.json` and `BRANCH_PAGINATION_CHECK.json` agree on all 1,309 remote
branches. `REF_DELTA_FROM_R79.json` shows the two added branches and unchanged
old refs. `NEW_COMMIT_IDENTITIES.json`, `NEW_COMMIT_PAYLOADS.json.gz` and
`NEW_A2_SCOPE_COMPARISON.json` cover all four additional ancestor commits and
the unrelated A2-DYN changes. Every current head's raw commit identity is
authenticated using the inherited raw-head pack plus this minimal extension.

Both inherited portable history verifiers were actually run in this audit.
`RETAINED_R78_HISTORY_RECHECK.json` authenticates 7,137 historical text payloads;
`RETAINED_R79_HISTORY_RECHECK.json` authenticates 64 more. The present minimal
`HISTORICAL_TEXT_DELTA_CURRENT.tar.gz` adds 72 distinct current predecessor
texts, 3,786,951 uncompressed bytes. The complete current index has 7,273
distinct text blobs, containing 116,158,319 bytes. No complete old archive is
duplicated here.

To authenticate the entire historical payload chain from the delivered source,
run all three checkers with the current source directory as `--source-root`:

```bash
python3 provenance/r78-audit/verify_history_r78.py --source-root .
python3 provenance/r79-audit/verify_current_history.py --source-root .
python3 provenance/r80-audit/verify_current_history.py --source-root .
```

Optional `--receipt` paths must be outside the source. Each checker streams
archives without extracting members. The new checker uses only Python's
standard library, delivered files and the pinned `CURRENT_HISTORY_MANIFEST`;
it requires no local Git cache, original workspace or network. The separate
`refresh_current_census.py` is the read-only Git/complete-source delta scanner
used to produce the census; it is not needed for portable authentication.

`CONTROLLING_AND_HISTORICAL_REPORTS_RECHECK.json` records fresh original-SHA
remote reads of four report bodies. `HISTORICAL_DEPENDENCIES_RECHECK.json`
records twelve central source/dependency checks and 21 selected file hashes.
The fresh R65 workflow readback is successful only for its own historical SHA;
R79 source/publication hosted queries both returned zero runs. No R80 execution
result is anticipated by this audit.

The full declared scope is frozen branch/ancestor traversal, relevant payload
retrieval/authentication, decoding, lexical issue indexing and content-based
source/report selection. It is not a claim of newly re-proving every archived
theorem, formal verification, independent human endorsement, comprehensive
priority clearance or editorial acceptance.
