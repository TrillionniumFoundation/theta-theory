# Independent reconstruction of the actual A2-DYN CI artifact

## Result and scope

**Passed within the explicitly stated artifact scope.** The downloaded GitHub artifact was opened and independently reconstructed. The final audit program completed in both normal and optimized Python, with zero exits and byte-identical result JSON. It does not import or execute the manuscript's validation drivers, and it did not modify the frozen source, any Git ref, or the remote repository.

The final checker evaluated 76,692 explicit artifact conditions in each run. These are identity, receipt, closure, comparison and document conditions; they are not counts of proved mathematical propositions. The complete result is `CI_RECONSTRUCTION_RESULT.json`; the original run-specific results and exact command receipts/logs remain preserved.

CI success and this audit remain auxiliary evidence. The original raw pointwise local limit theorem, full spectral/arithmetic inversion, remaining normalized endpoint/shallow shortage and four-coordinate long-time inverse conclusion are not declared complete.

## Exact artifact and checkout

| Item | Verified or attributed identity |
|---|---|
| Embedded CI checkout SHA | `9bd4ab343bb8a0f78b6a6380ae1f1e80a976d761` |
| GitHub run / job / artifact | `39712256295` / `119606068910` / `12397079374` |
| Downloaded ZIP SHA256 | `6ad292d68d0f16743ad222adfd34b6260b67d50d9c2a0205954bc3ed026e2ac0` |
| Downloaded ZIP bytes | 11,054,196 |
| Published article tree | `1fb3b20b29e3fe447bdae42f0faca0baf4f6b9cc` |
| Extracted files / bytes | 247 / 25,900,932 |

Every extracted file was compared byte for byte with its original ZIP member, after rejecting duplicate or unsafe archive paths. The embedded checkout file equals the published source commit, the build outcome is `success`, and the captured post-run tracked-tree status is empty. The run/job/artifact association and published article-tree identity come from GitHub metadata obtained by the publishing agent; this independent checker verifies the exact ZIP digest and embedded checkout SHA, without claiming a separate remote API query.

## Current source and preserved predecessor

The 140 current mathematical/build inputs were rehashed by bytes, SHA256, Git blob and mode. They total 1,563,890 bytes. The complete source identity is `cecca59e06fc83d0e3bab89e41e347b6c831c50dd78e7603d63377ca4be4feb0`, and the frozen manifest SHA256 is `5745a5abe9bb95de6dc64d53d28e018549c41f330b2895fb3382d9019bb8ae55`. The CI entrypoint hashes and repository workflow mirror match the same local source.

The predecessor is commit `03d651b8709d28d90aa435fc12d608ad9c945e23`, root tree `d65973a6db0eb2c477359d10b43194cc5f99fa2f`, article tree `3010c90e2363dfe1808101a3e992eb02643c28f1`. Its anchored 5,938-path map records 688,244,624 bytes. Independent Git-tree reconstruction from the exact path/mode/blob map yields the recorded article tree, and the 69 available inherited active proof/model files were independently rehashed against their anchored identities.

The complete CI source-gate result is exactly equal to the committed local source-gate result, including the recursive preservation results. **This is not a new independent byte rehash of the entire historical archive.** Those historical source bytes are absent from the current local restored `history/` and are not included in the CI artifact. The successful CI source gate attests its actual checkout checks; this independent reconstruction distinguishes that attestation from the file bytes actually available now. The original preserved Git tree and the current active sources are not conflated.

## Actual mathematical-check execution

| Check class | Independently verified result |
|---|---|
| Programs | 37 |
| Actual normal/optimized command receipts | 74 |
| CI normal versus optimized comparisons | 65 |
| Strict byte comparisons inside CI | 61 |
| CI mathematical JSON comparisons with exact runtime fields excluded | 4 |
| Cross-environment output files compared | 130 |
| Cross-environment files byte-identical | 122 |
| Cross-environment files with disclosed metadata differences | 8 |

All 74 actual command arrays were reconstructed, including the `-O`/`-B` modes, the two analytic `--details --output PATH` interfaces, the source-root and manuscript arguments, and output locations. Every command has exit zero, the current source digest, consistent chronology, and a rehashed actual stdout log. The stored 65 comparison entries equal the independently recomputed entries.

The 65 CI comparisons are separate from the 130 local-versus-CI output-file comparisons. Within CI, only `/executed_utc` and `/optimized` are excluded for the stdout and details of `check_all_offset_boundary` and `check_positive_critical_fans`; all other data must match. Across environments, the same normal or optimized mode is compared, so `/optimized` is not excluded. The only allowed changed paths are `/executed_utc` and `/python`, plus `/source` for `check_positive_critical_fans`. That source path must identify the identical SHA-bound `core/322_positive_critical_marked_source.tex` under the respective recorded execution cwd. No arbitrary metadata keys, source hashes, numeric values, bounds or check counts are ignored.

The actual cross-environment Python strings are 3.12.15 with GCC 13.3.0 in CI and 3.12.14 with Clang 22.1.3 in the committed local run. The pinned mathematical/PDF package versions agree. The complete result preserves each of the 130 file identities and each before/after value in the eight changed files.

### Exact changed-file identities

| Output file | Committed local SHA256 | Actual CI SHA256 | Changed JSON pointers |
|---|---|---|---|
| `check_all_offset_boundary-normal.log` | `9814a4351f3813d8455d54fa0308752f8feb85a360a29ddfa4117c86cab896fa` | `a2c98b4675341ff40912b78bd3f60307fe2ac2fcad84604ff09312a0b78d1cba` | `/executed_utc`, `/python` |
| `check_all_offset_boundary-optimized.log` | `62c71bb34c062c2d19cd50397e27a81989cd9480235e93c018ff48a31ab08338` | `ac836f2d7a2e86ad7fd335226194413129f7e20366f8b03d726a5c0f37547833` | `/executed_utc`, `/python` |
| `check_all_offset_boundary-normal.details.json` | `9814a4351f3813d8455d54fa0308752f8feb85a360a29ddfa4117c86cab896fa` | `a2c98b4675341ff40912b78bd3f60307fe2ac2fcad84604ff09312a0b78d1cba` | `/executed_utc`, `/python` |
| `check_all_offset_boundary-optimized.details.json` | `62c71bb34c062c2d19cd50397e27a81989cd9480235e93c018ff48a31ab08338` | `ac836f2d7a2e86ad7fd335226194413129f7e20366f8b03d726a5c0f37547833` | `/executed_utc`, `/python` |
| `check_positive_critical_fans-normal.log` | `e4724d6edf448993e117afacddfb16a41adba6f2af2b45f0d5e81cfb6bf57e74` | `b92db48ab209834dfaea6d3bf1fd72874ef884b56017a85628e2910aeee0e8d9` | `/executed_utc`, `/python`, `/source` |
| `check_positive_critical_fans-optimized.log` | `2fecbca1a292b85061c07b6559a0109398efc0cef5e5fae78499c3f7e24f8149` | `f9608896a51e3cca92c6a4009e4db3a9b7868c2e4b52e60c0bc7ac313fec3980` | `/executed_utc`, `/python`, `/source` |
| `check_positive_critical_fans-normal.details.json` | `e4724d6edf448993e117afacddfb16a41adba6f2af2b45f0d5e81cfb6bf57e74` | `b92db48ab209834dfaea6d3bf1fd72874ef884b56017a85628e2910aeee0e8d9` | `/executed_utc`, `/python`, `/source` |
| `check_positive_critical_fans-optimized.details.json` | `2fecbca1a292b85061c07b6559a0109398efc0cef5e5fae78499c3f7e24f8149` | `f9608896a51e3cca92c6a4009e4db3a9b7868c2e4b52e60c0bc7ac313fec3980` | `/executed_utc`, `/python`, `/source` |

### New finite auxiliary diagnostics

| Source-bound diagnostic | Actual finite checks in each mode |
|---|---:|
| `check_all_label_likelihood.py` | 74,071 |
| `check_localized_clearance_transport.py` | 1,478,574 |
| `check_marked_weak_operator.py` | 28,388 |

These counts and outputs are actual source-bound finite arithmetic/symbolic diagnostics. They do not certify continuous geometry, all physical collision words, inherited pressure estimates, or limiting theorems.

## Native manuscript and actual navigation

The three actual current pdflatex passes, pdfinfo call and navigation command have verified zero-exit receipts and unchanged raw logs. The compiler recorder contains exactly the declared 84 native TeX files. All 73 core bodies 260–332 occur once; numerical order is not imposed because the actual main manuscript introduces core 287 early and places retained appendices later. There are 1,125 unique source labels, 1,125 matching auxiliary records and 1,125 verified actual PDF named destinations. All 1,567 reference occurrences resolve to 807 distinct referenced labels, and all active citation keys resolve.

The actual current PDF has 255 pages. All six new core bodies 327–332 occur in the full article and contribute 94 labels. The CI auxiliary file is byte-identical to the committed local auxiliary file. All stable proof-index fields, including complete label entries, source lines, input edges, actual page mappings and the seven observed auxiliary-page offsets, match the committed local index exactly. The seven offsets were checked against the actual PDF destination page and the statement heading on that page.

| Label | Auxiliary page | Actual PDF page |
|---|---:|---:|
| `cor:dc-unique` | 39 | 40 |
| `prop:el-logomega` | 74 | 75 |
| `thm:gr-jets` | 79 | 80 |
| `thm:at-height` | 137 | 138 |
| `cor:nm-moments` | 158 | 159 |
| `thm:rbv-height` | 197 | 198 |
| `cor:v110-holder-constant` | 248 | 249 |

No final-log undefined references/citations, multiply defined labels, overfull boxes, missing characters or TeX fatal errors were found. The inherited amsmath advisories about `\atopwithdelims` and `\over` are recorded, not hidden.

## Historical original rebuild

The actual historical execution contains one original `tools/assemble_v105.py` invocation, six pdflatex passes and two pdfinfo calls. All nine actual stdout files, both final TeX logs and both actual PDF byte identities match their receipts and the wrapper summary. The rebuilt historical main and supplement contain 26 and 883 pages, respectively.

The CI historical rebuild records 390 checked source files. Its generated supplement identity agrees exactly with the committed local receipt: 280,165 bytes, SHA256 `f48c2d14e8647a40a585626075fa9aa959a819fcb081bc9b027049f8bea7da37`. The generated TeX bytes are not included in this artifact; agreement of these receipt identities is not represented as an independent hash of unavailable generated source. The historical repository-wide gate was explicitly not executed.

The local historical PDFs were found at their correct committed `delivery/historical-main.pdf` and `delivery/historical-supplement.pdf` paths. Their actual bytes match the local receipts. The execution-evidence folder alone does not contain those PDFs; no missing-file conclusion is based on that narrower directory.

## Actual PDF comparison and binary identity limits

For all 1,164 page pairs across the current 255-page manuscript, historical 26-page main and historical 883-page supplement, the independently read extracted text, media/crop boxes and decompressed page-content bytes are exactly equal between local and CI. The page text hashes and both content-stream hashes for every page are retained in the complete result. This is the verified document-content comparison; it is not a claim that independently built PDF files are byte-identical.

| Actual PDF | Pages | Committed local SHA256 | Actual CI SHA256 |
|---|---:|---|---|
| Current native manuscript | 255 | `60b08184ad7bfa001aae76deb98d99062212cc647723a8e096485e89861df6f5` | `5e4b98d8bd52942865dd6914bd5abec90bb2d2d242d1661f259baebe25d3b249` |
| Historical main | 26 | `d3fdacb4a020f165014f8790a184ae6d59aea5b95e48acd603a051b546c15688` | `adf2cc75a28d40efccbd25711ebcaf588528907d196783c3e44721aebda5efd0` |
| Historical supplement | 883 | `57b406b6642c94e79193f75c125e4c7820fe2ba4e7c6e46d05040936420e0bf6` | `8f1756c56b3317e5127b5483ce6743467d1b1cbdd1aa221dbae5bb5ddf91c12d` |

Observed PDF metadata differences are `/CreationDate` and `/ModDate`. The exact observed trailer identifiers also differ:

| Actual PDF | Committed local trailer `/ID` (hex) | Actual CI trailer `/ID` (hex) |
|---|---|---|
| Current native manuscript | `["4df73403f7f01e6bc4508d710ca852be", "4df73403f7f01e6bc4508d710ca852be"]` | `["feed73532a89b5ca64a28f3ae94501b0", "feed73532a89b5ca64a28f3ae94501b0"]` |
| Historical main | `["e3b96a802bc8d3c6a9091b98433b4397", "e3b96a802bc8d3c6a9091b98433b4397"]` | `["788624ce55db5ae74f8ad3b5883e5435", "788624ce55db5ae74f8ad3b5883e5435"]` |
| Historical supplement | `["1f3bf520afcf89515e65a44422d93504", "1f3bf520afcf89515e65a44422d93504"]` | `["d11282ab3e7182bd3861a34d4ae12809", "d11282ab3e7182bd3861a34d4ae12809"]` |

The exact date values and both ID arrays are retained. All PDF binary differences have not been exhaustively classified; byte-size and SHA differences are not silently treated as byte identity, and the report does not infer complete PDF-object equality from the page comparisons.

## Independent-checker execution and retained development

Final checker SHA256: `844fa02c86588c32413024515f87cda17a9a33b1602af95d0787cd7758d320dc`. Final normal and optimized result SHA256: `ee9e417ed0f6cb6902d60e71860b7efb80def8cd8bf24919165999cd28167e85`. `NORMAL_OPTIMIZED_EQUIVALENCE.json` binds the two real command receipts, exit codes and raw-log hashes to the byte-identical results.

The initial independent-checker attempts are retained, including source snapshots, actual failed receipts/logs and partial results. Three reader-schema adaptations were needed: distinct references versus total occurrences, the individual checker success strings (`PASS_AUXILIARY_ONLY`/`pass`) versus the aggregate driver string (`passed`), and TeX's stdout line-wrap inside the word `pages`. These were errors in the new independent reader, not changes to the frozen source or failures of the actual CI artifact. The first successful normal/optimized pair is also preserved. Final refinements record actual trailer IDs, enforce page-content equality and use the committed local receipt cwd for a portable source-path comparison. See `AUDIT_DEVELOPMENT_NOTES.md`.

No source, historical proof body, referee record, workflow, remote ref or external result was changed by this independent artifact reconstruction. The final proof/dependency ledger, full native proof statements and current mathematical status remain the authority for which billiard assertions are conditional and which original closure inputs remain open.

## Reproduction

Use Python with pypdf 6.10.0. Extract the preserved original ZIP into a separate audit directory, preserving all member names. Point `--article-root` at the published article source and committed local evidence; point `--artifact-root` at the directory containing `current/` and `current-history/`. The result must be written beside the independent checker. The checker reads inputs only and never imports the repository validation drivers.

```sh
python -B verify_ci_artifact.py \
  --article-root /path/to/theta-theory/papers/A2-DYN-localized-clearance-records-author-revision \
  --artifact-root /path/to/extracted-artifact \
  --archive /path/to/A2_DYN_CI_39712256295.zip \
  --output /path/beside/checker/independent-result.json
```

Add `-O` before `-B` for the optimized invocation. The supplied normal/optimized receipts are records of the actual executions, not mock output or proposed CI.
