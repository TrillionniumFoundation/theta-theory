# Historical preservation and source availability audit

This is an author source and execution audit for the **global minimizer localization revision**, observed on 18 October 2026. It identifies the mathematical sources actually read and rebuilt, preserves the original evidence without rewriting its claims, and distinguishes those observations from missing transport objects and unsuccessful CI. It is not a new referee report or a mathematical certification by a journal.

The current article continues the complete native A2-DYN main through modules 260–303 and adds modules 304–309. The retained historical supplement supplies the earlier mathematical bodies. The new geometric and original-source results do not by themselves complete the original raw pointwise local limit theorem. The exact dependencies and remaining normalized limit are recorded in [PROOF_LEDGER.md](PROOF_LEDGER.md).

## 1. Frozen author source and controlling review

| Object | Immutable identity | Actual scope |
| --- | --- | --- |
| Latest complete native author main | Commit `fb99e4d67ef74912f6c69b05c9abff3207572e7a`, dated `2026-10-18T04:21:44Z`; repository tree `b27ab3cc197a4ed491fcf85ed7db3658ebbb85ef` | `papers/A2-DYN-summable-physical-source-author-revision`, article tree `5575389060a6ba0ddaa0079be066ae41b107a49c`. The author and paired referee-copy refs resolve to this commit. All 44 native bodies 260–303 and the main's actual input closure are present. A fresh native build produced 127 pages. |
| Exact predecessor snapshot in this packet | [history/predecessor-source](history/predecessor-source) | All 103 actual article files, 1,557,258 bytes, including its old ledgers, manifests, scripts, claims and failed-qualification context. The snapshot is preserved byte for byte; new author corrections are outside it. |
| Controlling A2-DYN report | Report commit `f01482035a0b945b50f1f9c30f30ef35077558dc`; report blob `9c68b0e8b31cd196c732514a29ebd44d95964243` | [v115 controlling report](history/reviews/v115-controlling-report.md), 34,571 bytes, SHA-256 `4d560d8ffde372f67629ea93919bb3e918367502a0fd04e222b1cae17f682b06`. Actual commit time is `2026-10-16T01:13:20Z`. |
| Author source actually examined by that report | Commit `31792379408c5ace2c09284c2eb22d2331023433`; repository tree `008dba443ce2ca29b3e276b1bf05bcf7021011c1` | The report explicitly concerns the v114–v115 development, including modules 270–276. Its criticism is controlling for those sources and unresolved inherited issues. It is not evidence that the referee read modules 277–303 or the new 304–309. |
| Earlier report with still-relevant pressure and shortage issues | Report commit `d7fd0b24314d7341f9a611130bb650371d2d5ef2`; blob `0ad9f500c92db32ea4fc9f6d9ee28630b4484699` | [v112 inherited report](history/reviews/v112-inherited-report.md), 30,434 bytes, SHA-256 `bebed6720dc9def3dfbf3ee4b8c4b72acbe06b5cbd63c1004b66ff54861bb14c`. |

The report describes its author-requested, AI-assisted provenance; the packet does not relabel it as an independent human journal decision. Favorable review material for the companion **A2 geometry** paper is not an A2-DYN referee report. The [report index](audit/reports_index.json), [review status matrix](audit/review_status_matrix.json), and [controlling-report response matrix](audit/CONTROL_REPORT_AND_RESPONSE_MATRIX.md) retain report identities, actual reviewed sources and applicability. They prevent a review of an earlier or different article from silently becoming approval of the current theorem chain.

The native 127-page baseline build and the distinct unsuccessful inherited qualification command are retained in [history/baseline-rebuild-observed](history/baseline-rebuild-observed). A readable and buildable main is established by its actual input closure and execution. This does not establish the availability of every archive entry claimed by its older manifest.

## 2. Repository census and candidate classification

The read-only branch census retrieved 13 nonempty branch pages, containing **1,283 repository branches**, with pages 14–20 empty. There were **420 A2-DYN named refs**: 242 author/revision named refs and 178 review named refs. The author refs led to 127 distinct commit objects; the source inventory examined 113 distinct `papers` trees and 115 distinct A2-DYN article trees across those author heads. The review audit separately retrieved the 90 distinct report texts identified below. Branch aliases and report text counts are different quantities.

Machine-readable inventories are [all-branches.json](history/all-branches.json), [a2dyn-branches.json](history/a2dyn-branches.json), [all-author-head-commits.json](history/all-author-head-commits.json) and [all-author-article-variants.json](history/all-author-article-variants.json). This is an exhaustive census of the observed named heads and their source unions, not a claim to have recovered every unreachable commit, deleted ref, binary artifact or historical run.

Candidate status was determined from source trees and actual main dependencies, not the apparent version number:

| Candidate | Finding |
| --- | --- |
| Summable physical source, `fb99e4d67ef74912f6c69b05c9abff3207572e7a` | The latest actual complete main through 303; selected baseline. Its incomplete archival transport is reported separately below. |
| Sublevel clearance head `796e70b65ec17bccb165e047534ed07dd4b148e0`, theorem commit `d5c81e1e6e9ec8d8bd121372966ad3b012445378` | Genuine standalone progress in 300–301, but not a replacement complete main. Its native results are inherited in the selected later main. |
| Physical-source preparation `ac6a9b5314f5253bea6ff3d4f7bef2103f7fe2a3` and convex-critical preparation `53cce33a8d33db0b95a2375cb0ae33d5e801f437` | Preparation/workflow changes with the unchanged `papers` tree `25bf716fc75c59fa62df39784e4b494fa95122ab`; not new complete mathematical manuscripts. |
| Earlier full main through 291 | Commit `b47b3a86bbd4dda39bf2f0db166626e0102903fd`, article tree `6344849b9ceb592b6b6256de2bfd8c4ae55ae565`; useful actual source predecessor, superseded mathematically by the complete main through 303. |
| Locally claimed global predecessor `612cc64d6b5506981f337ccc019c6478e82b9b61` | Its requested Git object was unavailable in the actual API readback. Its claimed archive or page count is not promoted to a newly reproduced result. Recoverable native proof bodies were obtained from other actual Git objects. |

Further candidate identities and the original retrieval evidence are recorded in [BASELINE_AND_HISTORY_AUDIT.md](BASELINE_AND_HISTORY_AUDIT.md). Original preparation, failed transfer and qualification evidence remains accessible; it is not presented as a successful complete author packet.

## 3. What is preserved, and what each count means

| Retained material | Actual quantity | Index and purpose |
| --- | --- | --- |
| Exact complete predecessor article snapshot | **103 files; 1,557,258 bytes** | [history/predecessor-source](history/predecessor-source); original sources, metadata, historical claims and execution programs preserved unchanged. |
| Active inherited mathematical bodies | **44 files, modules 260–303** | Their current `core/` bytes agree with the predecessor snapshot. The six new mathematical files are additions, not replacements of earlier proofs. |
| Numbered historical mathematical variants | **355 native files; 3,392,932 bytes** | [NUMBERED_NATIVE_VARIANTS.json](history/NUMBERED_NATIVE_VARIANTS.json) and [numbered-variants](history/numbered-variants); every numbered module 1–303 is represented, with distinct observed proof variants retained. |
| Historical main and supplement rebuild closure | **390 original source files: 345 TeX and 45 Python** | [historical-v108/SOURCE_IDENTITY.json](history/historical-v108/SOURCE_IDENTITY.json); includes all 259 core bodies 1–259 and the actual unmodified assembler import closure. |
| Additional historical mathematical/prose variants | **66 distinct native source contents; 902,709 bytes** | [historical-manuscript-variants/SOURCE_MANIFEST.json](history/historical-manuscript-variants/SOURCE_MANIFEST.json); old main, supplement, abstract and bibliography TeX/text omitted from the minimal build closure, including original embedded mathematics. Every alias, source blob and SHA-256 is retained. |
| Retrieved A2-DYN report texts | **90 reports; 3,058,273 bytes** | [history/reports](history/reports) and [audit/reports_index.json](audit/reports_index.json); actual full texts. The two convenient controlling-report copies are duplicates of this collection, not two additional reports. |
| Actual recovery and failure evidence | Original manifests, API responses, compiler commands/logs, failed CI readbacks, source indices | Stored under `history/` and the scoped execution directories identified below. These are evidence categories, not new mathematical results. |

These categories overlap in source content. In particular, the 355 variants contain canonical bodies also present in the 390-file build closure; the 103-file snapshot contains the 44 inherited active bodies; controlling report copies occur within the 90-report set. The counts must not be added and described as distinct theorems or independent sources.

All 66 added source contents were independently rehashed after integration and matched their fetched native Git blob and SHA-256 identities. They address a concrete completeness issue: a minimal compiler input closure need not retain every historically distinct main or supplement, and some of those files contain mathematics directly rather than through a numbered input. They are preserved separately with exact bytes and aliases, without silently importing an obsolete statement into the current main. The broader fetched scaffold manifest is retained at [SCAFFOLD_SOURCE_MANIFEST.json](history/historical-v108/SCAFFOLD_SOURCE_MANIFEST.json).

## 4. Reconciliation of the numbered historical variants

The earlier claimed total of 343 numbered variants through 291 was not accepted on trust. The first reconstruction found 339 numbered variants, including 300–301 but excluding 292–299. An exhaustive comparison of actual author-head core trees located six otherwise missing v36 variants: modules **72, 74, 76, 77, 78 and 79** in commit `273cb245f2371efb9352086c29be6ef511885c61`, article `papers/A2-DYN-v36-referee-response`, article tree `63141f93769d39defe2ad22affddad54dda2641d`, core tree `77bbe8f2292edb7e4ac067b9be8b42321d68a825`.

The recovered blobs are respectively `b30ef1826ad93a91df2ed1c631db49bdd698b627`, `909715849241633076a4f9d4403be6bc3ea53797`, `10cebf9aeb2d0e92d7d0a25f171d0c4199368aa1`, `41e42eb8a43c9dd2edf9237692bf0cb1ef3e0110`, `2b5e8aad64ace54227760338f54ea20fa390c20a` and `4165ba9ef70910c155ad81b4c3541c7014956aa0`.

Thus the observed native count is **339 + 6 − 2 = 343 variants through 291**, followed by the 12 actual modules 292–303, giving **355**. The source index verifies each byte sequence. This reconciles the numbered-source claim by retrieving the missing mathematical objects. It does not validate the bytes, membership, or completeness of an unavailable ZIP archive, and it does not assert that all historical unnumbered prose was included in the initial 343; the additional 66-source collection addresses that separate scope.

## 5. Reconstructed native historical main and supplement

The earlier canonical source was recovered from actual commit `fb99e4d67ef74912f6c69b05c9abff3207572e7a`, where `papers/A2-DYN-v108-referee-response` remains available as article tree `e66a1dec484f419d88c05f12a7e2ec5310430448`, with core tree `abc9ef989a20f32f7611d4060d65d51d3afd7732`. All **259 numbered core files**, totaling **2,428,191 bytes**, are present without an index gap.

The retained 390-file input/import closure supports the original main and supplementary assembler without changing their mathematical text or the 45 original Python dependencies. The new scoped [rebuild_history.py](history/historical-v108/rebuild_history.py) checks source identities and runs this closure; it does not pretend to execute every old repository gate. After assembly, all 301 reachable TeX inputs exist. The generated supplementary TeX has SHA-256 `f48c2d14e8647a40a585626075fa9aa959a819fcb081bc9b027049f8bea7da37`.

Two independent local builds were performed. The first source-recovery build produced a 26-page main and an 883-page supplement; original commands and compiler output are retained in [historical-v108/evidence/source-recovery](history/historical-v108/evidence/source-recovery). Earlier assembly attempts failed because SymPy was unavailable in the attempted Python environments. Those failures remain in [LOCAL_RECOVERY_FAILURES.json](history/LOCAL_RECOVERY_FAILURES.json). Supplying the actual isolated SymPy 1.14.0 and mpmath 1.3.0 dependencies allowed the unchanged assembler to execute successfully. These recovery failures are not erased or turned into a successful old whole-repository gate.

The second build was executed from the **final integrated article path**, starting at `2026-10-18T05:08:05.954149Z`, using the scoped rebuild command and the supplied isolated `PYTHONPATH`. It checked all 390 original sources and ran nine actual commands: the assembler, six `pdflatex` passes, and two PDF inspections. All nine returned exit code zero. The result is recorded in [FINAL_PATH_REBUILD.json](evidence/current-execution/historical-final-path/FINAL_PATH_REBUILD.json), alongside the actual command receipts and compiler output.

| Final-path document | Pages / PDF bytes | PDF SHA-256 | Final log SHA-256 |
| --- | --- | --- | --- |
| Historical main | **26 / 529,089** | `2ff3dc40866e57112415853b033808cc6529bb970334ac7a5352f7333b40a80a` | `772e9162dd7e5477c4c1940735128f7301b268847a0035a4aeefe49c161b1129` |
| Historical supplement | **883 / 5,714,968** | `291a224e4068360df0bde99d33f647319f155e4b05a5013372526566e1f7db87` | `cae09ba1245be1e9c9d525b321e6b32dbef93acd84e22613bab65f524f460904` |

The PDFs are generated under `history/historical-v108/build/`; logs and receipts retain the observed artifact identities even when regenerable build outputs are excluded from the source manifest. The supplement had no recorded undefined-reference, overfull, missing-glyph or LaTeX/package warning diagnostics. The historical main retains the original `amsmath` advisory concerning `\over`. The first and second PDF hashes differ; this audit claims identical verified source bodies and actual independent compilation, not a bit-reproducible PDF build.

The **26-page main and 883-page supplement are historical documents**. The 127-page build above belongs to the selected predecessor main through 303. Current main page counts, current proof checks and current CI are reported by their own actual receipts in [VALIDATION.md](VALIDATION.md); these distinct executions must not be conflated.

## 6. Missing transport objects and the inherited manifest discrepancy

The selected predecessor article tree actually contains **103 blobs**. Its inherited source manifest lists **982 entries**: **101 listed files are present with matching bytes, and 881 listed entries are absent from that article tree**. The two other actual files fall outside that inherited listed set. The complete native main input closure is present, but the larger transport manifest is not thereby satisfied. [summable-manifest-missing.json](history/summable-manifest-missing.json) preserves the absent paths and their claimed identities.

Actual API readbacks in [missing-archive-api-readback.json](history/missing-archive-api-readback.json) returned unavailable-object responses for the claimed local predecessor commit `612cc64d6b5506981f337ccc019c6478e82b9b61`, archive-index blob `244d6d0f0d3cbcce11955bcf18c2b38a7fdb14fd`, original archive blob `486d012476e251af0cf9bb2d93c70c095cbc3a56`, and later CI archive blob `c4041625d60e0dc93792206ca2ce3dd925bb4084`. The corresponding old claimed trees, checksums and sizes remain in the retained predecessor manifests. The audit does not invent downloadable objects from those claims or attribute actual rebuilt pages to that unavailable local commit.

Native recovery establishes availability of the explicitly indexed mathematical sources independently of those missing archives. It does **not** recreate the unavailable archive byte for byte, prove every old archive member recovered, or validate a historical claim of 91 archived reports. The actual retrieved report collection is 90; its observed membership and source coverage are documented separately.

The previous version of this audit, with its original claims and provenance, remains unchanged inside `history/predecessor-source/`. This current audit corrects the present evidentiary status without removing the older record.

## 7. CI and packaging evidence

The actual historical run readbacks are retained in [HISTORICAL_CI_ACTUAL_READBACK.json](history/HISTORICAL_CI_ACTUAL_READBACK.json). At the observed read time, the relevant runs were:

| Actual run | Head / last update | Observed status |
| --- | --- | --- |
| [39017578483](https://github.com/TrillionniumFoundation/theta-theory/actions/runs/39017578483) | `d5c81e1e6e9ec8d8bd121372966ad3b012445378`; `2026-10-17T08:52:28Z` | Completed, **failure** |
| [38919903130](https://github.com/TrillionniumFoundation/theta-theory/actions/runs/38919903130) | `b47b3a86bbd4dda39bf2f0db166626e0102903fd`; `2026-10-16T18:38:55Z` | Completed, **failure** |
| [39096822675](https://github.com/TrillionniumFoundation/theta-theory/actions/runs/39096822675) | `fb99e4d67ef74912f6c69b05c9abff3207572e7a`; `2026-10-18T04:46:12Z` | Completed, **failure** |

For the summable-source run, actual job `117584906141` completed setup, checkout and dependency installation, then failed exact-source qualification. The top-level log identifies the `source_phase` / inherited `qualify_revision.py verify` invocation and its child log path; it does not expose enough child output to assert a more specific causal error. The independently observed 881-file discrepancy is therefore recorded as a source-availability finding, not invented as the complete explanation of that job failure. Artifact upload success is not qualification success. Actual job metadata and logs are preserved in `history/SUMMABLE_FAILED_CI_*`.

The inherited workflow `.github/workflows/a2-dyn-summable-physical-source-20261017.yml` was actually read at blob `ecf886dd9bc0f6ecfee7aa8205785cf8fe93883f`; its readback is retained in [BASELINE_WORKFLOW_READBACK.json](history/BASELINE_WORKFLOW_READBACK.json). Its older full-archive gate cannot be reused unchanged as verification of the present source package.

Nine obsolete predecessor packaging, mapping and publication entry points were removed **only from the new active placement**, after exact copies were verified in the immutable 103-file predecessor snapshot. [ACTIVE_PACKAGING_REPLACEMENTS.json](history/ACTIVE_PACKAGING_REPLACEMENTS.json) records every original path, preserved path, SHA-256 and reason. No original mathematical body was removed by this packaging correction. The new scoped build and source-verification entry points have their own receipts; simulated tests, local compilation and workflow creation are not descriptions of a completed remote run. The actual publication and current CI status must be taken from the current exact-commit execution records.

## 8. Literature, dependency and historical-review traceability

Historical references, theorem variants, failed mechanisms and old response documents are retained in their original contexts. The review audit indexes the 90 full reports and their 356 extracted request sections; extraction is a navigation aid, not a statement that every mathematical request has been solved. Current responses state which issues are resolved by retained or new proofs, which deductions are conditional, and which final implications remain open.

The supplementary historical source census also checks bibliography definition and citation coverage, retaining aliases and the original companion-paper references. Bibliographic key resolution is distinct from theorem applicability. The current [LITERATURE_AUDIT.md](LITERATURE_AUDIT.md) and the primary-source recheck notes identify which external theorems were actually reread, with their relevant spaces, hypotheses and quantifiers. The audit does not claim that every external work in the historical bibliography has newly received an independent full reconstruction, or that a companion paper's review validates A2-DYN's dynamical input.

## 9. Isolation, reuse and mathematical status

All assembly described here is confined to `papers/A2-DYN-global-minimizer-localization-author-revision`, together with the dedicated current workflow managed for this revision branch. Existing author versions, review branches, the A2 companion and unrelated repository papers are retained. [HISTORY_INTEGRATION_RECEIPT.json](history/HISTORY_INTEGRATION_RECEIPT.json) records the initial verified integration; the subsequent 66-source addition and full-report collection have their own exact manifests. [REUSABLE_GIT_BLOBS.json](REUSABLE_GIT_BLOBS.json) supplies 747 verified original-blob placements from the initial integration, with final repository paths, so existing immutable blobs can be reused. That count is not an exhaustive count of all subsequently added package files.

Source identity, native compilation, mathematical deduction and remote publication have separate scopes. Preservation protects the exact old proof bodies and evidence, including unsuccessful attempts. The current proof ledger explains the new uniform exponential localization of every global minimum, the explicit Borel exceptional source on original physical records, its exponential total-mass estimate, and the precise conditional density payments. It also retains the unresolved normalized shortage, spectral and full raw inversion implications. No historical archive claim, finite computation or successful compile is used to replace those remaining proofs.
