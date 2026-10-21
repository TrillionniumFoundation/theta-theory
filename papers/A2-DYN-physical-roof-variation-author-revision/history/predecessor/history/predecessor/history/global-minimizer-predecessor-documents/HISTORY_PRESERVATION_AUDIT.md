# History preservation audit

## 1. Status and evidentiary boundary

This revision preserves the original A2-DYN source record and extends its native mathematical chain. It does not certify the final raw pointwise local limit theorem. The current dependency account is [PROOF_LEDGER.md](PROOF_LEDGER.md); the controlling-report response is [RESPONSE_TO_REFEREE.md](RESPONSE_TO_REFEREE.md).

A workspace-maintenance event removed the local working files during the first remote transport attempt. The original frozen transport inventory survived in session storage. It is preserved, without redefining its file identities, at [history/PRE_MAINTENANCE_TRANSPORT_INVENTORY.json](history/PRE_MAINTENANCE_TRANSPORT_INVENTORY.json). Original source bytes were recovered from immutable Git objects and the saved original author snapshot. Newly reconstructed metadata, proof text and current execution evidence are identified as such. An old hash in that inventory is evidence of a formerly inventoried artifact; it is not a claim that a lost raw log has been recovered.

The exact pre-maintenance version of this audit is retained at [history/pre-maintenance-author-documents/HISTORY_PRESERVATION_AUDIT.md](history/pre-maintenance-author-documents/HISTORY_PRESERVATION_AUDIT.md). It has 22,127 bytes and SHA-256 `d728bd749d4b6be3646f08c1bfaba8835a56ad13c00c905422122abf566473f2`. Its descriptions of earlier local executions remain historical statements. This current audit supersedes those statements for the availability and identity of current files and logs.

This document distinguishes:

1. immutable original mathematical sources and reports recovered with exact byte, SHA-256 and Git-blob checks;
2. fresh API readbacks of fixed remote commits and trees, which substantiate source identities but are not asserted to reproduce the serialization of lost API responses;
3. reconstructed author documents and source-control utilities, checked again after reconstruction;
4. current actual executions, including failed attempts, with their real command receipts;
5. missing historical objects and lost execution artifacts, which are not replaced by invented evidence.

## 2. Fixed baseline and controlling report

The baseline is the actual complete native author manuscript at commit `fb99e4d67ef74912f6c69b05c9abff3207572e7a`, authored at 2026-10-18T04:21:44Z, in `papers/A2-DYN-summable-physical-source-author-revision`. Its repository root tree is `b27ab3cc197a4ed491fcf85ed7db3658ebbb85ef` and its article tree is `5575389060a6ba0ddaa0079be066ae41b107a49c`. The author and matching referee-copy refs resolve to the same source identity. Its actual directory has 103 files, including the 44 native modules 260–303. Its earlier observed native build was 127 pages. That historical observation is kept distinct from the newly executed 147-page current manuscript and the fresh 26/883-page historical rebuild below.

The controlling A2-DYN report is the v115 report committed as `f01482035a0b945b50f1f9c30f30ef35077558dc`, with report blob `9c68b0e8b31cd196c732514a29ebd44d95964243` and SHA-256 `4d560d8ffde372f67629ea93919bb3e918367502a0fd04e222b1cae17f682b06`. The commit time is 2026-10-16T01:13:20Z. It explicitly reviews author commit `31792379408c5ace2c09284c2eb22d2331023433`, whose repository root tree is `008dba443ce2ca29b3e276b1bf05bcf7021011c1`. Its direct scope is that author version, including the v114/v115 additions through module 276. It is not an external review of modules 277–309 or of this reconstruction.

The report is retained at [history/reviews/v115-controlling-report.md](history/reviews/v115-controlling-report.md). The inherited v112 report is retained at [history/reviews/v112-inherited-report.md](history/reviews/v112-inherited-report.md); its blob is `0ad9f500c92db32ea4fc9f6d9ee28630b4484699` and SHA-256 is `bebed6720dc9def3dfbf3ee4b8c4b72acbe06b5cbd63c1004b66ff54861bb14c`. These reports are author-requested, AI-assisted external-review records. They are not journal acceptance decisions or independent human reconstructions of the later dynamical inputs. A favorable review of the companion A2 geometry paper is not an A2-DYN report.

The full 90 distinct retrieved A2-DYN reports are retained in `history/reports/`, with the audit copies in `audit/reports/`. The two named controlling/inherited copies are duplicate placements of reports already counted in those 90. They do not increase the count to 92. The unresolved historical requests and applicability ranges are recorded in [audit/CONTROL_REPORT_AND_RESPONSE_MATRIX.md](audit/CONTROL_REPORT_AND_RESPONSE_MATRIX.md).

## 3. Immutable preservation anchor and actual inventory

[history/IMMUTABLE_SOURCE_ANCHOR.json](history/IMMUTABLE_SOURCE_ANCHOR.json) binds the original frozen transport identities. Its SHA-256 is `bc93f16657c09a87a469ab8275cdf966082fa64131f517dbb308c6f70db17177`. The source verifier checks this literal identity before trusting the per-file entries; a newly calculated hash of altered source cannot silently replace the anchor.

| Anchored group | Actual placements | Original bytes | Scope |
|---|---:|---:|---|
| Predecessor snapshot | 103 | 1,557,258 | All actual files of the fixed summable-source author directory, unchanged |
| Numbered native variants | 355 | 3,392,932 | Distinct native source contents bearing module numbers 1–303, including historical alternatives |
| Historical build sources | 390 | 3,221,429 | Complete native v108 build closure: 345 TeX and 45 Python files |
| Additional historical manuscript variants | 66 | 902,709 | Distinct old main, supplement, abstract, bibliography and related mathematical text not already present by content |
| Distinct historical reports | 90 | 3,058,273 | Complete retrieved report text, without counting duplicate audit or named-control copies |
| Active inherited core | 44 | 442,771 | Exact inherited modules 260–303 in the active current source |

These groups overlap in mathematical content and sometimes duplicate the same Git blob at different paths. Their placement counts are not numbers of independent theorems or disjoint discoveries. The anchor's checks cover 1,048 designated placements, including 1,004 historical placements and 44 active inherited core placements.

The known-Git restoration receipt is [audit/recovery/KNOWN_GIT_BLOB_RESTORE.json](audit/recovery/KNOWN_GIT_BLOB_RESTORE.json). It records 699 distinct known Git blobs restored at 1,178 original frozen placements with zero missing objects and zero byte, SHA-256 or Git-blob differences. The original 103-file snapshot was also available as saved full strings and was restored against its original identities. This statement concerns the native bytes actually checked; it does not claim that every newly authored document, generated PDF, execution log or original API serialization survived.

The exact source identities and current placements are indexed in [SOURCE_IDENTITIES.json](SOURCE_IDENTITIES.json), [history/PREDECESSOR_SOURCE_IDENTITY.json](history/PREDECESSOR_SOURCE_IDENTITY.json), [history/historical-v108/SOURCE_IDENTITY.json](history/historical-v108/SOURCE_IDENTITY.json), [history/NUMBERED_NATIVE_VARIANTS.json](history/NUMBERED_NATIVE_VARIANTS.json) and [history/historical-manuscript-variants/SOURCE_MANIFEST.json](history/historical-manuscript-variants/SOURCE_MANIFEST.json). Those indices are explicit post-maintenance reconstructions, not claimed byte-identical restorations of lost index serializations.

## 4. Exhaustive ref and native-variant reconciliation

The fresh branch readback covers 1,283 repository refs, of which 420 are A2-DYN-related. The 242 author/revision refs resolve to 127 distinct author heads. The source reconstruction read the actual immutable metadata of all 127 commits, their 127 root trees, 113 papers trees, 115 A2-DYN article trees and 111 distinct core trees. These are direct nonrecursive Git-tree reads, retained in the `audit/recovery/AUTHOR_*_READBACK_20261018_*.json` files. Nonrecursive reads were used after an oversized recursive response failed; failure of that response was not evidence that the referenced native source did not exist.

Every one of the frozen 355 numbered variants now has an actual original module number and at least one fixed-tree source witness. All 355 original native contents are present; none was inferred by thematic similarity or by renumbering a later proof. The source-index reconstruction receipt is [history/SOURCE_INDEX_RECONSTRUCTION.json](history/SOURCE_INDEX_RECONSTRUCTION.json).

The earlier apparent disagreement with the predecessor's claim of 343 native variants through module 291 has been resolved by real source recovery:

- an initial collection contained 339 variants, including modules 300 and 301 but omitting modules 292–299;
- six distinct v36 alternatives for modules 72, 74, 76, 77, 78 and 79 were recovered from commit `273cb245f2371efb9352086c29be6ef511885c61`, article tree `63141f93769d39defe2ad22affddad54dda2641d` and core tree `77bbe8f2292edb7e4ac067b9be8b42321d68a825`;
- removing the two post-291 modules from that initial count gives 339 + 6 - 2 = 343 variants through 291;
- the twelve subsequent modules 292–303 give 355 in total.

The six recovered alternative Git blobs are `b30ef1826ad93a91df2ed1c631db49bdd698b627`, `909715849241633076a4f9d4403be6bc3ea53797`, `10cebf9aeb2d0e92d7d0a25f171d0c4199368aa1`, `41e42eb8a43c9dd2edf9237692bf0cb1ef3e0110`, `2b5e8aad64ace54227760338f54ea20fa390c20a` and `4165ba9ef70910c155ad81b4c3541c7014956aa0`. Their actual variant/module mapping is in the numbered manifest.

The 66 additional historical manuscript contents retain all source aliases observed in the fixed v108 root, core, appendix and provenance readbacks. These are preserved as one original byte sequence per distinct content, with explicit aliases and immutable URLs. The manifest does not claim exhaustive enumeration of every recursively nested duplicate alias. All 66 distinct original contents themselves are present and independently hash checked. Alternative main texts and failed or superseded mathematical approaches are not silently merged into the active proof chain.

## 5. Genuine historical build closure and current execution

The recovered historical native source is taken from `papers/A2-DYN-v108-referee-response` in the fixed baseline repository tree. The article tree is `e66a1dec484f419d88c05f12a7e2ec5310430448`; its native core tree is `abc9ef989a20f32f7611d4060d65d51d3afd7732`. All canonical core modules 1–259 are preserved. The 259 core files alone contain 2,428,191 bytes. The complete build closure is the anchored 390-file native set.

The scoped helper [history/historical-v108/rebuild_history.py](history/historical-v108/rebuild_history.py) was reconstructed after the maintenance event. Its immutable 390-file source table has SHA-256 `27573612967769a36d9571798369d80ed26a82cddb861a076378078dbc3f4a04`. It checks those source identities before running the unchanged original `tools/assemble_v105.py`. The resulting full supplement source has SHA-256 `f48c2d14e8647a40a585626075fa9aa959a819fcb081bc9b027049f8bea7da37`.

The helper compiles the supplement before the main manuscript because the original main uses external supplement labels. It then compiles each document three times and records the real commands, return codes, logs, output identities and page counts. Its added wrapper does not replace the historical mathematical source or change the original assembler.

Three post-maintenance attempts are preserved:

| Attempt directory under `evidence/current-execution/historical-recovery/` | Actual outcome |
|---|---|
| `20261018T163843666122Z/` | Original assembler failed because SymPy was unavailable; the actual failure receipt and command output are retained |
| `20261018T164212275266Z/` | All nine commands returned zero and pages were 26/883, but compiling main before supplement left unresolved external references; `POST_EXECUTION_QUALITY_ASSESSMENT.json` rejects this as the clean final build |
| `20261018T164336583551Z/` | Correct supplement-then-main order; all nine commands returned zero; 26-page main and 883-page supplement; no unresolved references, xr dependency warnings, overfull boxes or missing-glyph diagnostics |

The accepted clean receipt is [evidence/current-execution/historical-recovery/20261018T164336583551Z/REBUILD_RECEIPT.json](evidence/current-execution/historical-recovery/20261018T164336583551Z/REBUILD_RECEIPT.json). It was executed with Python 3.12.14 and the restored SymPy 1.14.0 / mpmath 1.3.0 environment. That runtime is distinguished from the Python version specified for remote CI.

| Accepted output | Bytes | SHA-256 |
|---|---:|---|
| Historical main PDF, 26 pages | 529,089 | `c1a2e4c7b58c0a9cef417cff17e4016860bd1a4c40ec87e96cd6d3cdb3e57ad2` |
| Historical main TeX log | 26,917 | `044b497293c1fd364ab15a169b7b4585f4c64127eace2e5cf22abb3179a06ff2` |
| Historical supplement PDF, 883 pages | 5,714,968 | `c39d7f8bb1d3174224a0fc440a984921ae4daa4a786d8fb3c163a4d45d2f2d18` |
| Historical supplement TeX log | 52,723 | `0245fe25a97465454501d8b237e0c68a4ff8b3127e085f5a654133a60b7145bb` |

The historical main retains the original amsmath advisory about a foreign `\\over`; it is disclosed rather than removed by changing the original proof text. The accepted supplement has no such diagnostic. The PDFs and real execution records are deliverables; their successful construction is evidence of readable native proof bodies, not a substitute for mathematical validity.

Earlier pre-maintenance 26/883-page executions and the predecessor 127-page execution were also observed. Their old output identities remain in the frozen inventory and in the preserved prior audit where recorded. Raw bytes that were lost are not recreated under the old log filenames. The new accepted receipt above is a new execution with its own hashes.

## 6. Preservation of new and inherited mathematics

The active modules 260–303 are exact copies of the fixed baseline sources. The current revision adds modules 304–309. The original geometry, physical collision trajectories, clock, section/return events, joint return/displacement/collision labels, arithmetic factors, conditional measures and four-coordinate raw inversion objective remain the objects of the paper.

The new work includes the global-minimizer boundary-load estimates, the exact physical clock and phase bookkeeping, conditional comparison-cost bounds, the extension to all relevant third-obstacle centres, a uniform exponential localization theorem for every global minimizer, and an explicit Borel source decomposition that includes the genuine section collars. The exact statements, constants, measures, quantifiers and remaining hypotheses are in the complete English native proof bodies and [PROOF_LEDGER.md](PROOF_LEDGER.md).

The workspace recovery did not provide a byte-identical copy of every newly authored TeX file or author document. The proof reconstruction is disclosed in [MATHEMATICAL_AUDIT.md](MATHEMATICAL_AUDIT.md) and the current validation records. In particular, reconstructed module 304 makes the feasibility scope of the interior variational inequality explicit; this is the scope used by module 307's arbitrary-feasible budget. Actual restored/reconstructed label names are used. The current six new bodies have 94 labels, rather than an invented restoration of the earlier 104-label count.

The current active source closure contains 59 source files, including all 50 core modules 260–309. The reconstructed proof index reports 691 current labels and verifies the source/auxiliary/PDF destinations. That derived navigation is recalculated from the actual final typeset manuscript. Its count is not a proof of the analytic inputs. The current author manuscript's observed new build is 147 pages; [VALIDATION.md](VALIDATION.md) and the final actual receipts govern its final output identity.

The new uniform exponential localization closes a finite-depth geometric defect that the earlier polynomial localization did not close. The explicit Borel source decomposition controls a stated total-variation exceptional source exponentially, uniformly over the specified original geometries and collision words. Conditional density-cost estimates use the same original full roof and explicitly inherit the named pressure hypothesis where required. None of these statements automatically supplies the supremum of microscopic conditional return densities, the unresolved normalized positive-source remainder, the full Fourier estimate or the long-time inverse Jacobian control.

The final raw pointwise local limit theorem therefore remains unproved. No TV bound is silently promoted to a pointwise density bound; no shortened roof replaces the original roof in a conditional law; no average limit replaces the requested supremum; no unproved interchange of ordered limits is made. The exact minimum closure conditions are retained in the ledger and the response.

## 7. Missing historical archive claims and active packaging replacements

The predecessor's manifest lists 982 entries. In the actual 103-file baseline directory, 101 of those listed entries exist with matching content; 881 are absent, and two actual files are outside that listed set. The absent entries include the claimed archival packaging. The actual current native mathematical closure does not require pretending that those missing archive objects exist.

The claimed local predecessor commit `612cc64d6b5506981f337ccc019c6478e82b9b61`, claimed article tree `13c34c68b38097c02f50a17b74d9dab6027cc373`, claimed root tree `fed4bbd067ef9423649952ecb837b9a6fc423d56`, archive-index blob `244d6d0f0d3cbcce11955bcf18c2b38a7fdb14fd`, original archive blob `486d012476e251af0cf9bb2d93c70c095cbc3a56` and later CI archive blob `c4041625d60e0dc93792206ca2ce3dd925bb4084` are not treated as recovered source. Earlier API probes returned not-found responses for the specified unavailable objects. Where the old raw response was lost, the present account is explicitly the retained historical observation, not a fabricated fresh response.

The current package instead carries the actual original source bytes, the complete restored 1–259 historical build and all 355 numbered variants. [history/summable-manifest-missing.json](history/summable-manifest-missing.json) reconstructs the missing-entry accounting directly from the preserved original manifest and actual source identities.

The pre-maintenance packaging correction moved nine old active placements into the preserved original snapshot. The post-maintenance delivered state is more precisely described as seven obsolete active mapping or qualification/publishing entry points absent from the current active package, plus two inert historical workflow copies restored under `ci/` by the exact known-Git recovery. These two copies are retained for traceability; they are not active repository workflows. The seven removed active paths and the two retained copies, with their original source identities, are listed in [history/ACTIVE_PACKAGING_REPLACEMENTS.json](history/ACTIVE_PACKAGING_REPLACEMENTS.json). Every original remains in `history/predecessor-source/`. No mathematical proof body was removed by this packaging correction. The original repository workflows, source versions, historic publication instructions, old manifests and failure claims remain preserved. The predecessor's missing-archive qualification entry point does not govern the new complete native-source build.

## 8. CI, publication and current package verification

Fresh baseline workflow and CI observations are recorded in [history/BASELINE_WORKFLOW_READBACK.json](history/BASELINE_WORKFLOW_READBACK.json) and [audit/CI_AND_PUBLICATION_AUDIT.md](audit/CI_AND_PUBLICATION_AUDIT.md). An uploaded artifact, a successful preparation workflow, a skipped qualification step or an incomplete workflow is not evidence of a qualified manuscript. A run with a successful top-level status but skipped mathematical installation and qualification is described with those actual skipped jobs.

The latest source baseline has an observed failed historical qualification run. The workflow file's existence and successful source retrieval are not represented as a successful build or as a mathematical result. The final new-branch CI status is determined by the actual run readbacks attached by the publishing agent. This audit does not announce a future or unobserved run as complete.

The source helper [tools/package_source_manifest.py](tools/package_source_manifest.py) verifies every anchored original placement before freezing or verifying current source. It uses explicit exceptions, so optimized Python does not disable the checks. It checks actual file bytes, SHA-256, Git-blob hashes, exact source membership and the native TeX input closure. Historical files named `SOURCE_MANIFEST.json` or `PUBLICATION_STATUS.json` remain ordinary preserved source entries; the root-only exclusions do not hide them.

The root `SOURCE_MANIFEST.json` excludes itself, its checksum, current execution outputs, build directories, transient synchronization files, the derived `PROOF_INDEX.json`, and the entire derived `delivery/` subtree. This prevents PDF timestamps or publication receipts from creating a source-freeze cycle. The complete remote transport inventory still includes the actual delivered proof index, PDFs, receipts and other designated output blobs. Exclusion from the source-input manifest is not omission from the delivered revision.

The utility's real positive and negative checks are retained under `evidence/current-execution/manifest-reconstruction/`. Failed fixture attempts, including transient synchronization interference and a disk-full failure in redundant disposable test staging, are not silently recast as successful current mathematics. Those structural test fixtures are reproducible copies and were not native originals.

## 9. Final preservation conclusion

The actual original A2-DYN mathematical source and all 90 retrieved reports are retained with immutable identities. The formerly missing six v36 alternatives and the 66 additional historical manuscript contents are genuinely recovered. All 355 numbered native variants are supported by fixed-tree witnesses, and the complete 390-file historical native build has been freshly executed in its delivered path.

This revision does not claim recovery of missing historical archives, lost raw execution bytes, unobserved CI success or a completed raw local limit theorem. Newly reconstructed documents and utilities are explicitly distinguished from exact original source. The remaining analytic and dynamical closure conditions are recorded alongside the completed new geometric arguments, so subsequent author work can continue from the actual proof chain and its exact evidentiary limits.

