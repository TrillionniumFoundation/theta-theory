# Read-only audit of the published A2-DYN source commit

**Audit date:** 20 October 2026 UTC. **Result:** the published source has the declared immutable identities, exact historical preservation, complete native source closure and correct isolation. One concrete explanatory-text substitution defect was found in `VALIDATION.md`; it does not affect any mathematical, native TeX or build input. Minor response and evidence-locator clarifications are listed below.

This audit reads the immutable Git objects at the source commit, rather than treating a changing working directory or later evidence commit as the tested source. It does not rerun the mathematics, compiler or GitHub Actions, and it is not a referee report or a continuum-proof certificate. All output was written outside the repository, in the scratch post-publication audit directory. No Git ref, index, repository file or remote state was changed.

## 1. Exact published identity and complete change scope

| Object | Verified identity |
|---|---|
| Source commit | `86c947eccea6029258d9a362624866a475118a66` |
| Exact parent | `6cdd9ae88cd358d524ecb89092361ac1522ba351` |
| Source repository tree | `4624f0eef13e655c39d6313f6779e6c72a86870e` |
| New article tree | `6830d79a554645422869c3531715f1a32161ce20` |
| New article | `papers/A2-DYN-critical-source-transport-author-revision` |
| Preserved predecessor subtree | `a1d21789f9d7c1be801ff4a54d1befad2a47340f` |
| Dedicated workflow Git blob | `34745bb3a225516e1d101519f87c08e42e45e85c` |

The full recursive parent-to-source Git delta contains **4,369 additions and zero modifications, deletions, renames or other statuses**. Exactly 4,368 added files belong to the new article. The sole other addition is `.github/workflows/a2-dyn-critical-source-transport-20261020.yml`. Thus every previously existing repository path retains its original Git identity. This comparison concerns the source commit's content; the separate remote-ref census and eventual CI evidence remain their own records.

The dedicated workflow and its frozen article-local mirror are the **same Git blob**. Its push trigger names the requested revision branch and only the new article/workflow paths. This source audit makes no claim that a workflow declaration itself constitutes an executed run.

## 2. Exact preservation and manifest checks

The new `history/predecessor` tree is exactly the complete original article tree at the stated parent. Every one of its **3,864 paths, modes and Git blob identities** matches the separately fixed anchor. The anchor's declared size is **485,851,107 bytes**. Its original-path map also independently reconstructs the same Git tree. This readback verifies preservation through exact Git object identity and the independently pinned original SHA-256 map; it does not claim to have newly rehashed all historical bytes a second time.

The **61 active inherited files**—all 59 core bodies 260–318 plus `model.tex` and `inputs.tex`—retain the original archived blobs and modes. The four older preservation-anchor documents retain their original SHA-256 identities. All **91 distinct original report bodies**, identified by the **178-ref review map**, have their declared exact original-blob placements in the published archive.

The controlling report copy is the actual report blob `9c68b0e8b31cd196c732514a29ebd44d95964243`, SHA-256 `4d560d8ffde372f67629ea93919bb3e918367502a0fd04e222b1cae17f682b06`. The current documents consistently identify its report commit `f01482035a0b945b50f1f9c30f30ef35077558dc`, explicit reviewed source `31792379408c5ace2c09284c2eb22d2331023433`, and direct scope through native 276. No favorable A2 geometry report is attributed to A2-DYN.

Every **123-entry** frozen source-manifest record matches the actual published path, mode, byte count, Git blob and SHA-256. The canonical mathematical-source digest uses 122 mathematical/build files; the additional manifest entry is the dedicated workflow mirror. Every **503-entry** delivery-manifest record matches the published bytes and SHA-256, and its path set is exactly all 504 nonhistorical article files except the delivery manifest itself.

| Fixed file or digest | SHA-256 |
|---|---|
| `CURRENT_SOURCE_ANCHOR.json` | `e49c3b8d9002cc2e431a4e7b846490a5a9f347f47fa236a1c609146f16bcfe1b` |
| `SOURCE_MANIFEST.json` | `775943e1aa70d53e725956c8ab9eb01edb710c555b89cdcc5f1f9064d463f6c1` |
| Canonical mathematical source | `cbe6dac9cab2bf80dd73119aaeda4d9f3122b42898807a4d0b6ac869eaecbc82` |
| `main.tex` | `73e0365b10bd86cda608c5b4e7853d4b4d3dd4595211f36defba8496e5d1b04c` |
| Published `compiled/main.pdf` | `8eb1f67c250590ee5dc6c78994f710743ad5bf2f442c5071f7c0d60671235efb` |
| Source-commit `DELIVERY_MANIFEST.json` | `7d2a8e6a4ff7d1274f0d8f9e78ddea0eaa0e87c8c084a7f5ac4d640b14409ebf` |

All five actual published execution bundles were reopened without extracting into the repository. Their complete **492 indexed member files** match the declared paths, sizes and hashes. This verifies that the execution evidence was actually published intact; it does not repeat or strengthen the results recorded by those executions.

## 3. Native closure and final explanatory scope

The source checker was read from the pinned source commit and its native-closure routine was run against a scratch extraction of those same mathematical files. It resolves **74 native TeX files**, with all **63 core bodies 260–322 included exactly once**, **959 unique labels**, **668 references**, no unresolved references, and one complete document structure. The declared manifest graph matches the actual resolved graph. This is source-closure verification, distinct from the preserved actual compiler-recorder verification.

The final `main.tex`, revision introduction, README, response, proof ledger, mathematical audit, literature audit, source-identity document and history audit were read. The regular all-offset boundary result, positive-capacity threshold result, and leading positive-visited critical-fan result retain their separate mathematical scope. In particular, the final exposition correctly recognizes the all-mark leading positive-visited fan payment after 322 while retaining the distinct visited-grazing traces, nonleading coarea remainders, original same-roof shortage, full pressure, spectral/arithmetic/conditional inputs and raw inverse endpoint. No complete raw pointwise LLT or full four-coordinate inverse theorem is asserted.

All **19 explicit relative Markdown links** in the inspected root Markdown documents resolve in the immutable published tree. The native TeX references also resolve as stated above. The separately preserved baseline failure classification still reports 34 missing-Sympy import failures in the initial run, and 52 successful commands in the pinned rerun at the same baseline mathematical digest. The actual command logs remain bound by the published evidence index. No old mathematical program was rerun for this audit.

## 4. Concrete explanatory findings for the evidence carrier

1. **`VALIDATION.md`, line 5:** a prose-template substitution changed the intended filename `SOURCE_MANIFEST.json` into `SOURCE_775943e1aa70d53e725956c8ab9eb01edb710c555b89cdcc5f1f9064d463f6c1.json`. That latter filename does not exist. The actual manifest exists, has the correct identity, and passed all checks above.
2. **`VALIDATION.md`, lines 11 and 44:** the same substitution mechanism replaced occurrences of the word `PDF` with the full main-PDF hash. The published text therefore contains phrases such as `Final main <hash> SHA-256` and `Standalone <hash>s`. Restore the word `PDF`/`PDFs` while retaining the actual digest in the digest field. This is prose corruption, not a changed PDF or mathematical source.
3. **Response 18.2:** qualify “precisely \(l-2\) intervening collisions” with “for \(l\ge2\),” and mention the separately handled one-hit case if desired. Native 319 and the mathematical audit already make this distinction correctly; the response summary currently omits the qualifier.
4. **Detailed-audit locators:** the mathematical audit opening and the proof ledger's final audit paragraph cite only `audit/mathematical-reconstruction/`. The detailed independent reconstructions for 319 and 320 are retained at `audit/current-census/319_RECONSTRUCTION.md` and `audit/current-census/320_RECONSTRUCTION.md`. The two bare primary-literature JSON filenames in the literature audit are at `audit/current-census/literature/PRIMARY_SOURCE_READBACK.json` and `audit/current-census/literature/THEOREM_LOCATORS.json`. Adding these explicit paths would make the already-present evidence easier to locate.

The parent authoring process was informed of the confirmed substitution defect and the minor precision/locator items. The source commit remains immutable; any correction belongs to a separately identified evidence/documentation carrier. That carrier must retain the frozen mathematical source identity and must refresh its own delivery manifest if its explanatory files change.

## 5. CI scope at this immutable source commit

The source-commit publication record explicitly describes preparation before remote execution; it does not contain a successful new-run claim. The parent process reported that dedicated run **39424256218** was queued when delegating this audit. This audit does **not** determine that run's eventual state. The source SHA, the actually executed CI checkout, its outcome/artifacts and a later carrier commit must remain separately identified. Present-tense CI wording in the response should be read with those actual status records and made concrete by the carrier once the run is inspected.

## Machine-readable supporting output

The scratch audit contains `git-scope.json`, the complete added-path list, the pinned article-tree inventory, `source-identity-verification.json`, `published-native-closure.json`, `relative-document-links.json`, the verified nonhistorical file identities and `verify_published_source.py`. The source-identity verification completed with **zero errors**. These are author-side preservation and consistency records with the limited scope stated above.
