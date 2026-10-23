# R76 baseline and verifier-port evidence

This directory records the new author-revision baseline audit. It is not an
external referee report or a mathematical approval. The controlling source
is R75 commit `bc2952aa9a9695fe9985d491a4156b8975024285`, delivered at
`2c103f924720435700e947cc8df31b8b648f61e9`; the substantive deposited report
remains R65 at `358481b21ceeeedb1205ebd30f86982e32a2cb04`.

Start with `BASELINE_LOCK_R76.json` and `BASELINE_AUDIT_R76.md`.
`BASELINE_CONTENT_AUTHENTICATION.json` checks every source/publication
file, native-input closure, readable PDF and pinned dependency.
`R75_RECEIVED_VERIFICATION.json` and `R75_ARCHIVE_RESTORATION.json` record
the actually executed prior-publication receiver/restore checks; they do
not claim a fresh mathematical build or a new R76 success.

`REMOTE_HEADS.tsv`, `CURRENT_REFS.json`, `ALL_HEAD_COMMIT_IDENTITIES.json`,
`REF_DELTA_R76.json`, `NEWLY_REACHABLE_COMMITS_R76.json` and
`REVIEW_BRANCH_RECHECK.json` bind the all-head retrieval, inspected ancestry
and inherited report identities. The two new branches relative to the
R75 starting snapshot are the completed R75 branch and a separate A2-DYN
branch. Other-paper changes are classified without importing their claims.

`full-scan/` contains the complete fresh 6,664-object text inventory,
versioned path/commit mappings, scoped raw history, lexical issue lines and
read/hash/decode receipts. `scan_theta_history.py` is the exact inherited
scanner executed for this pass. `materialize_history_cache.py` records
construction of an isolated audit object cache from authenticated original
bytes; no manuscript checkout refs, index or files were changed by it.
`authenticate_baseline.py` records the independent baseline byte checks.
Their absolute workspace paths describe the actual execution environment
and can be adapted for a new audit.

The complete 26,648,059-byte historical corpus is supplied as a publication
archive rather than embedded again inside this source folder. Its SHA-256
is `492d79c1c8cb350d5f8fb19aaa6d73a0670f0144f677d4e14641801424b887e4`.
`BASELINE_LOCK_R76.json` and `full-scan/HISTORICAL_TEXT_INDEX.json.gz`
authenticate all members. Original R75 archive identity records and the
entire predecessor provenance remain unchanged elsewhere in this source.

`refresh_preservation.py` regenerates the complete 386-file R75 retention
map after every changed old file has been byte-preserved under
`inputs/r75/`. It does not seal the new source or fabricate missing bytes.
The new sealer separately fixes the old manifest hash and compares every
retained path/byte identity; strict verification additionally checks the
actual immutable predecessor Git tree.

`VERIFIER_PORT_PREFLIGHT_R76.json` is an early static port check: syntax,
all twenty inherited diagnostic source identities, absence of removable
Python assertions in those scripts, 59 protected proof/support bodies,
the original supplement suffix, the independent R58 tree and all 209
inherited indexed statements. At that recorded stage the current theorem
count is intentionally unset and the three new suite names are provisional.
The final source must fix the actual count and full inventory before a
strict execution can pass. This early receipt is retained as development
evidence and does not override the later source-bound build receipt.
