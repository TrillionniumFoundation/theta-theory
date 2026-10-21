# A2-DYN complete branch and native-source census

## Method and evidentiary scope

This is an author-revision source audit. The immutable objects were read from the actual repository, rather than inferred from version numbers or earlier conversation claims. The initial `git ls-remote --heads` snapshot contains **1,296 remote refs**. Every head's commit and immediate source/review/workflow trees was inspected. The source census finds **432 A2-DYN-named refs**, representing **216 distinct head commits**. No additional differently named head has an A2-DYN-named article, review, revision or workstream directory in those locations. The workflow census separately records A2/dyn-named workflow blobs; its broader naming filter does not make companion A2 workflows A2-DYN evidence.

The results are stored in `branch-source-index.json`, with each ref's exact commit, root tree, parent identity, subject, scoped article/review trees and workflow blobs. `a2-dyn-tree-dag.json` records every recursively reachable tree entry below the scoped roots. This representation records the complete Git object graph without multiplying identical historical copies. There are **210 scoped root tree variants**, **794 distinct reachable tree objects**, **119 direct author-source tree variants**, and **116 distinct direct main-entrypoint blobs**. The latest repository root expands to 1,716,797 paths, whereas its current article has 3,864 files.

The readback fetched and read **1,595 distinct mathematical TeX, bibliography, program, proof-ledger and referee/response blobs**, totaling **18,705,400 bytes**. Their Git identities, byte counts and newly computed SHA256 hashes are in `source-blob-manifest.json`. The tree graph contains 612 distinct TeX blobs, 575 program blobs, 127 ledger/index blobs, 281 review/response blobs and 192 source-identity blobs under the documented filename classification. Counts describe corpus contents, not independent mathematical results.

`numbered-proof-variants.json` fixes **370 distinct numbered proof-body blobs**, spanning every identifier 1–318. There are 371 filename/blob pairs because one body appears under two names. The inventory preserves variants instead of keeping only the largest module number or latest file spelling.

No `AGENTS.md` occurs in the latest full repository tree or in the recursively inspected A2-DYN source graph. This audit did not modify any checkout, index, branch or remote object reference.

## Complete current author source

| Item | Immutable identity |
|---|---|
| Current complete author head | `6cdd9ae88cd358d524ecb89092361ac1522ba351` |
| Current repository root tree | `49f5bd3917dcedf64a96bd47507c5d6033d43543` |
| Author ref | `revision/a2-dyn-marked-boundary-source-2026-10-19` |
| Matching author-copy refs | `referee-copy/a2-dyn-marked-boundary-source-2026-10-19`; `referee-response/a2-dyn-marked-boundary-source-2026-10-19` |
| Article path | `papers/A2-DYN-marked-boundary-source-author-revision` |
| Article Git tree | `a1d21789f9d7c1be801ff4a54d1befad2a47340f` |
| Main TeX Git blob | `0a4c416c113b60d1505de309f73b5065843d5e8b` |
| Main TeX SHA256 | `1420c43afb2aec30b8801c685e1af6be7e91fe49f9bda2476ee6519453bf8557` |
| Immediate complete author predecessor | `0933e9b44f5b0fd1d1a624d37ffd881d352496f8` |
| Predecessor article tree | `ff4daf7f42d868bd9b41b0b9fe4033489f99bd21` |
| Actual tested marked-boundary source checkout, as identified by its retained execution packet | `efde9fa6c45e7835989b653622a9870e59027530` |

The three current author refs have the same head. The final head is a later evidence-publication descendant, and is not relabeled as the earlier executed CI checkout. The exact current CI packet identifies run 39281615689, job 118156848926 and artifact 12201151164 at the tested checkout above. Its scope must be independently read from that packet or the live service; a later containing commit does not create a new execution.

The current main resolves **69 native TeX inputs**, including all **59 core proof bodies 260–318**. The paper retains the physical model, conditional event and original raw target. The current README and proof ledger explicitly leave the full raw pointwise local limit and four-coordinate inverse theorem unproved. The source is complete and readable; mathematical completeness of the final target is a separate question.

`native-dependency-audit.json` records every literal input edge against its exact article tree. This audit found complete source closure for **117 main-entrypoint variants**. It strips TeX comments and reports dynamic or missing input edges, rather than silently treating them as present. All checked closures have one document class, one document start and one document end after following the dependency graph. This is source-availability verification; actual typesetting is recorded separately by the current revision's build receipts.

## Incomplete names, generated sources and historical distinctions

The direct article trees for `papers/A2-DYN-v50-referee-response` (`58818bc4835ad9d7d689017174e1d8d6bb51809a`) and `papers/A2-DYN-clearance-jacobi-2026-10-15` (`4d30e4984ba0eda27927ee622a22a5cb18a44c55`) do not contain `main.tex`. They are not substituted for a complete native article.

Some branch names advertise a version without introducing a same-numbered article directory. `author-branch-name-exceptions.json` records these cases with exact refs and commits. A naming exception is not itself a finding of mathematical incompleteness: for example the v114 author alias points to the complete, differently named clearance-roof article. The actual source graph determines the classification.

Historical v73 uses `build/v72-body.tex` and `build/v72-frontmatter.tex`. These are generated before typesetting by its retained `tools/verify_v73.py`, Git blob `1527443926aa2690af2b79a3703c3c7965324bc9`, called from its exact `build.sh`. The generator reads the retained v72 main, preserves all 159 inherited core inputs in their order, and constructs both files. The source audit independently executed that extraction algorithm and followed the resulting input edges. These two generated paths are therefore not confused with an incomplete transfer. Historical v108 likewise uses a short main wrapper whose included preamble and body form one complete native document.

The controlling A2-DYN report remains the actual v115 report at commit `f01482035a0b945b50f1f9c30f30ef35077558dc`, report blob `9c68b0e8b31cd196c732514a29ebd44d95964243`. It expressly examines author commit `31792379408c5ace2c09284c2eb22d2331023433` and the native chain through 276. It does not directly review the later 277–318 continuation. Favorable assessments of the separate A2 geometry paper and successful qualification workflows have no enlarged review scope.

## Independent preservation verification

The four current preservation anchors were independently compared with the actual latest article tree. A placement passes only if the recorded original Git blob exists at its stated preservation path. Where the original article tree is specified completely, its entire path/mode/blob map was also compared with the anchor's original map. SHA256 was additionally checked for every covered blob included in the freshly read mathematical source corpus.

| Anchor | Checked placements | Additional exact original-tree check | Result |
|---|---:|---|---|
| `FULL_PHYSICAL_SOURCE_ANCHOR.json` | 2,765 | All 2,765 original files equal tree `ff4daf7f42d868bd9b41b0b9fe4033489f99bd21` | Passed |
| `PHYSICAL_TUBE_SOURCE_ANCHOR.json` | 2,088 | All 2,088 original files equal tree `f5c90ecd279dd116330c5d90fa31cae2b0d6f61e` | Passed |
| `GLOBAL_MINIMIZER_NATIVE_SOURCE_ANCHOR.json` | 74 | Stated native-source and author-document placements | Passed |
| `IMMUTABLE_SOURCE_ANCHOR.json` | 1,048 | Stated older frozen-source placements | Passed |

Groups overlap and are not added to create an inflated count of unique preserved files. `independent-anchor-verification.json` records the actual zero-failure result. In particular all **56 predecessor core bodies 260–315** remain byte-identical. The only additional core files are 316, 317 and 318; every predecessor body is still reached by the current main.

The early physical geometry, periodic and arithmetic arguments, spectral and conditioning interfaces, old proof attempts, original reports and execution evidence are retained in the immutable source graph and the current article's history. Retained historical statements keep their original conditions and later correction records. Preservation alone does not convert an unresolved interface into a theorem.

## Isolation requirement for the new continuation

Start the new revision's repository tree from the exact current head above. Add a new article directory containing the complete current native inputs, current author exposition and genuinely new proofs. Preserve the entire preceding article under a separate immutable history placement or Git subtree with the exact tree identity above. Add only its dedicated workflow if needed. The final Git delta must have no deletions or modifications to any pre-existing article, review, companion, unrelated workflow or repository-root file. A final scope check should compare the complete old-path map against the new tree and bind the local and CI receipts to the source checkout that actually ran them.

This audit makes no continuum theorem-certification or journal-acceptance claim. It provides a reconstructible source baseline and preservation evidence for the continuing author revision.
