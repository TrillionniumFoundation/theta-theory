# History preservation and change isolation

The new revision is based on `e84c06c758bed5b2dc09222ad725cfe0ba0d58dd`. No earlier source, report, derivation, failed attempt, CI file, companion paper or remote historical branch is overwritten. The original 7,102-file localized-clearance article and its nested preserved history remain in their original parent tree. This new directory does not recursively copy that 755 MB tree again.

## Positive preservation checks

1. **Active predecessor proofs:** all 73 native files 260–332, `model.tex`, `inputs.tex` and the remaining active support sources are copied without changes. `audit/INHERITED_ACTIVE_SOURCE_IDENTITIES.json` pins every inherited active source by bytes, Git blob and SHA-256. The predecessor's original main and introduction are also preserved in `history/baseline-active/` while the new main introduces this continuation.
2. **Complete native historical content:** all 660 distinct LaTeX blobs found in the 435-ref scoped census were actually fetched, rehashed and preserved in `history/ALL_660_NATIVE_SOURCE_OBJECTS.tar.gz`. The archive uses content identities as member names and contains 7,303,280 bytes of source before compression. Original paths, commits, names and hashes are recorded in `audit/NATIVE_SOURCE_CONTENT_IDENTITIES.json` and the scoped Git-object census. This is deduplication by identical Git content, not removal of failed mathematical arguments.
3. **Historical analytic proof bodies:** the 40 specifically reconstructed source texts and their canonical identities are additionally preserved in `history/HISTORICAL_ANALYTIC_SOURCE_BODIES.json`. The audit locates the old section multipliers, complete fixed-band arguments, capacity theorem, finite residence result, microscopic equivalence, raw correction identity and real normal-orbit obstruction.
4. **Review evidence:** the controlling report is copied byte-for-byte, with its original Git blob verified. Applicable earlier v112 and v73 reports remain accessible in `history/reviews/`, while the whole scoped report history stays in the frozen Git trees. The 285 report-named blob count is a census of objects, not a representation that every object is a distinct external referee report.
5. **Execution evidence:** the original baseline ledgers/status are preserved separately from the new status. Its successful 74-execution local reproduction, native 255-page build, exact source checks and proof navigation have actual receipts. Earlier failed setup/path attempts and new integration failures are retained with their real causes. Successful earlier GitHub job metadata and the carrier job log are separate from the new branch's CI.
6. **No changed mathematical target:** the original model and analytic-input files are byte-identical, and all old proof bodies remain in the new native closure. Exact labels, physical clock, section/return event, guard, normalization, probability quantifiers and ordered limits are retained. New subsource estimates are declared at their true norms.

The validation program rehashes all inherited active sources and every historical archive member. It also verifies that every core file 260–335 is included exactly once in the native manuscript. The actual compiler recorder is compared against that same source closure.

## Scope of the inventory

The initial complete remote-head collection, A2-DYN normalized ref list, deduplicated tree DAG, direct source-role census, and detailed selection audit are preserved under `audit/`. Named author, referee-copy, response, external-review, research, workflow, publication and ledger paths were traversed in the scoped tree graph. A higher version string without a complete buildable source was not selected. Intermediate source notes and qualification diagnostics are classified by their actual contents. No favorable A2 geometry assessment is counted as A2-DYN review.

The census does not claim to independently reprove every historical page. The current baseline was actually materialized and built. The specific historical analytic dependencies and all new claims received a content-level audit; the remainder is retained and indexed, not certified by filename alone.

## Allowed change set

Only the new article directory and `.github/workflows/a2-dyn-section-multipliers-exact-inversion-20261023.yml` may differ from the parent. The workflow is newly added and restricted to this branch and directory. A machine-readable final diff audit is retained in `evidence/local/CHANGE_SCOPE.json`. Unrelated source trees and every prior path remain identical to the parent. Remote publishing creates the new revision branch and fast-forwards only that branch.

## Failed attempts and their meaning

The first baseline attempt lacked portions of the deliberately sparse historical checkout and the SymPy dependency. The next baseline attempts successfully ran mathematics/typesetting but wrote the proof-navigation output outside the original article root, contrary to that existing script's path contract. The successful final baseline reproduction used the complete materialized source, isolated mathematical environment and an output directory inside the original article. These failures are environment/path failures, not silently discarded mathematical counterexamples.

The first new integration compiled but reported an 18.35 pt overfull equation in native 334. The equation's coordinate declaration was moved to a separate sentence without changing its mathematics. The failure receipt is preserved; final typesetting is validated independently. Any subsequent actual diagnostic is recorded in `VALIDATION_REPORT.md` and the retained execution archive.
