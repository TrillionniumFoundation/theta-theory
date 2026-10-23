# Actual source, mathematics and typesetting validation

## Outcome and exact tested source

The final sealed-source local validation passed. It executed on 2026-10-23T07:27:50.801763+00:00 through 2026-10-23T07:28:06.516858+00:00. The active native source SHA256 is `d4a67e23d0559b777f7b03fec588639c71229ce534ed767f4f903bcefacf377b`. The content manifest SHA256 is `17fbcc69943372afdc78fe15f03d313479aa0f0c309a0dd8093af3e837ac66cc`. The complete executed commands, exit codes, timestamps and log hashes are in evidence/local/run/.

The actual PDF has **283 pages**, from **90 native inputs and 78 core proof files**, with **1205 unique labels**. Its SHA256 is `7ebe5c18b3be9bfcc852fd8300556e424960516639e4e97ee1faf15d4119fc89`. Every compiler-recorded native input agrees with the recursively checked main-file closure. The proof navigation table agrees with the final compiled index.

## Completed checks

| Verification | Actual result | Interpretation |
| --- | --- | --- |
| Sealed content manifest | All 217 included non-evidence files match bytes, Git blob and SHA256; exact file set verified | Content identity |
| Immediate predecessor | All 158 materialized files preserved; 85 of 87 active native files and every one of 76 core proofs byte-identical | Historical preservation |
| Portable source census | 8 provenance groups pass; 435 old A2-DYN refs unchanged in the 436-ref frozen census | Correct baseline and review scope |
| Git object reconstruction | 950 historical and 19 fresh tree hashes, all 660 native bodies and 120 historical main entries verified | Real object identity, not proof validity |
| Inherited mathematics programs | Four programs pass with their original exact/symbolic/finite-example scopes | No new credit for inherited results |
| New physical-SBV program | 29 exact symbolic/rational checks pass | Pushforward examples, signed grouping, coarea factors and exceptional-radius control |
| New jump-spectrum program | 42 exact/symbolic/high-precision controls pass | Fourier signs, full-torus normalization, sinc cross terms, finite-band inequality and normalization |
| Native typesetting | Three passes, actual recorder and text extraction pass | Complete readable native manuscript |
| Visual inspection | 21 selected pages, including every new proof page; no observed layout defect | Scope recorded in FINAL_VISUAL_QA.json |

There are no undefined references, duplicate labels, missing characters or overfull hbox/vbox diagnostics. Two amsmath compatibility warnings for foreign primitive commands also occur in the predecessor; their exact messages are recorded in PUBLICATION_STATUS.json. They are not hidden under a claim of a warning-free build.

## Mathematics checked in the written proof

The author reconstruction independently checks the complete physical first-hit graph, fixed-radius boundary construction, finite geometric support, monotone side Jacobian, turning-point integrability, constant-roof atoms, increasing-roof boundary signs, critical sector factor, one conditioning factor, all-label variation, complex signed cancellation, differentiated Fourier sign, complete torus measure, every sinc cross term, Cauchy–Schwarz finite-band bound, central cutoff derivative, the original m^2 normalization, and the inherited zero-clearance fan transfer. These derivations are in NEW_MATHEMATICAL_CHECKS.md, the proof ledger, internal challenge records and full native proofs.

The source hypotheses of Coste were verified from indexed primary theorem text. Four earlier primary PDFs were downloaded and hashed again. The failed full Coste PDF retrieval is separately recorded, not misreported as a completed byte-level verification.

## Actual failures, corrections and historical evidence

The selected predecessor was independently rebuilt to 271 pages with its four programs. Its first environment attempt lacked mpmath; exact failure and successful rerun archives are retained under evidence/baseline/. The two earliest physical-SBV program attempts lacked SymPy before its checks began; the corrected isolated-environment execution is recorded in audit/physical_sbv_execution.json. The portable census verifier corrected an invalid implementation assumption about selected versus complete tree entries, then passed both a relocated self-contained execution and a mutated-ref rejection control; its actual receipt is audit/CURRENT_CENSUS_EXECUTION.json.

The geometric proof was corrected to take closures fiberwise at fixed radius. Constant-roof regular side atoms and same-label signed coincidences are retained. A central analytical roof cutoff is justified by its explicit product decomposition. All these are proof clarifications documented in audit/INTERNAL_PROOF_CHALLENGE.md. The first integrated native manuscript already compiled; its original receipts are retained separately in evidence/preliminary/.

## Remote publication and CI

The source was actually pushed to `revision/a2-dyn-physical-roof-jump-spectrum-2026-10-23` at commit `1cd52fd00675f10f08182f670a42fbbf9e0d1a96`, with parent `d6c3c6754fb3a1b4ad3eea8e6dcc51642e312b28`. The repository tree is `d78e8ff51de5a63497d576a3e67214389d9bad30` and the new article tree is `2505b6ec3d4153d71e1b3bda0e2cfe2bd4d0131f`. All 285 remote article blobs match the exact local publication plan. GitHub's comparison contains exactly 286 added files: this new article and its dedicated workflow, with zero modified or deleted files.

The structural tree comparison preserves every one of 218 previous paper entries and 180 previous workflow entries. All 1307 refs present immediately before publication were unchanged at the post-source observation. One additional unrelated general-theta branch appeared concurrently with this new revision branch; it is recorded and preserved. The earlier census-to-prepublication observation likewise preserved the initial 1306 refs, with one unrelated concurrent addition. These observations do not claim that no other author was working in the repository.

At 2026-10-23 07:52:05 UTC, the workflow for the exact source commit was **queued**, with conclusion `None`. Its actual run is [39920538196](https://github.com/TrillionniumFoundation/theta-theory/actions/runs/39920538196); 1 job and 0 artifacts were reported. A queued job with no completed steps is not a passed validation. The exact run, job and artifact API records are retained under evidence/github/. The predecessor's queued runs do not qualify this revision.

The metadata carrier containing this receipt changes only publication metadata and evidence, leaving the sealed source and its 283-page validated PDF unchanged. Its own workflow status must be observed separately and is not inferred from the source run. No unobserved remote success is claimed. SOURCE_PUBLICATION_RECEIPT.json, SOURCE_TREE_SCOPE.json, SOURCE_COMPARE_FILES.json and POST_SOURCE_REF_DELTA.json record the actual publication and preservation checks.

## Mathematical completion status

The complete physical SBV and marked jump-spectrum statements have full author proofs with their explicit inherited assumptions. The final original shortage and the alternative complete normalized local derivative-charge condition remain open. The necessary jump-energy condition is not asserted sufficient; neither smooth narrow concentration nor positive-source remainder is declared automatically small. The full raw pointwise local limit and full four-coordinate inverse are not asserted complete. No finite program, visual check, compilation or CI outcome is independent expert certification of those unclosed dynamical assertions.
