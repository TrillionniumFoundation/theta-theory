# General Theta Foundations I — Revision 76 referee entry

## Finite-Use Geometry of Ordered Binary Quantum Measurements

This revision responds to the v75/r49 reports and retains the general mathematics journal objective. The complete matrix effect body is treated in every fixed finite input dimension; a separate theorem gives a common learner for every unknown biased qubit effect. All inherited proofs and their original hypotheses are retained.

Native source: `a107cd1a0f7ec4e356e807f5f49c7ab998553552`.
Predecessor: `16b78c8edef566300ea21300908854ad83455879`.
Controlling external report: `4de14a3fe5c271c77de64e410e1bd67fa2e7dce8`; pipeline audit: `8ee073109d5911c6526ff81314bede13bafe9f6c`.

## Manuscripts

| Artifact | Pages | Role |
|---|---:|---|
| [Focused quantitative paper](papers/GTF-I-v76-matrix-effect-geometry/paper.pdf) | 69 | New core theorems first; complete supporting proofs in appendices |
| [Structural companion](papers/GTF-I-v76-matrix-effect-geometry/STRUCTURAL_PAPER.pdf) | 41 | Separately complete inherited structural theory |
| [Complete research edition](papers/GTF-I-v76-matrix-effect-geometry/COMPLETE_REVISION.pdf) | 174 | Historical mathematical development and all additions |

[Point-by-point response](papers/GTF-I-v76-matrix-effect-geometry/RESPONSE_TO_REFEREE.md) covers R01–R20 and D01–D36. [Written-proof audit](papers/GTF-I-v76-matrix-effect-geometry/PROOF_AUDIT.md), [literature comparison](papers/GTF-I-v76-matrix-effect-geometry/LITERATURE_AUDIT.md), and [independent rereview brief](papers/GTF-I-v76-matrix-effect-geometry/INDEPENDENT_REVIEW_BRIEF.md) identify the exact claims and their proof and priority questions.

## Three mathematical additions

1. **All-dimensional matrix geometry.** For `M=(E+F)/2`, `H=F-E`, and `V=M(I-M)`, the intrinsic Sylvester modulus `Q_N^2=N <H,(L_V+R_V+N^-1 Id)^-1 H>` satisfies `min(1,Q_N)/(8192d) <= d_N^na <= d_N <= min(2,8Q_N)` for every pair and horizon, including all ranks and spectral multiplicities. The metric uses unhalved final trace norm with arbitrary retained references, common feedback, and bounded public stopping.
2. **Full-body entropy.** For each fixed `d`, all `N>=1`, and `0<delta<=delta_d`, the covering number is comparable to `N^(d^2/2) log(N+2)^floor(d/2) delta^(-d^2)`. Uniform measure bounds for actual operational balls include every singular boundary point. A signed-prefix spectral integral and matching nested endpoint boxes give the logarithmic multiplicity. Rational legal centres attain the same order.
3. **Common unknown-qubit learning.** One data-dependent experiment learns bias, contrast, and direction with error `delta` in future-`N` adaptive distance and failure at most `eta`, using and requiring order `N delta^-2 log(1/eta)` training calls. Every entangled block has at most `N` calls. Random GHZ signs remove bias, observed amplitudes select the noise scale, and fresh endpoint samples finish the estimate. Rational rounding and the retained exact code give an optimal-order reusable word without more calls.

Learning and the implemented joint codec have qubit scope; the matrix geometry and rational covering existence have arbitrary fixed-dimension scope. Payload, training calls, classical arithmetic, workspace, and physical hardware remain separately accounted for.

## Locations in the focused PDF

| Source label | Statement | Page |
|---|---|---:|
| `thm:matrixmetric76` | 2.1 | 3 |
| `lem:matrixpath76` | 2.2 | 4 |
| `cor:matrixadaptivity76` | 2.3 | 6 |
| `lem:matrixspectral76` | 2.4 | 7 |
| `lem:matrixlocal76` | 2.5 | 7 |
| `lem:matrixball76` | 3.2 | 8 |
| `prop:matrixvolume76` | 3.3 | 10 |
| `thm:matrixcover76` | 3.1 | 8 |
| `thm:commonlearn76` | 4.1 | 12 |
| `cor:learncode76` | 4.6 | 18 |

## Reproduction and preservation

The native build and its isolated reconstruction passed 14 exact suites in ordinary and optimized Python with identical results. Every page was checked, and the isolated build reproduced page text and rasters. The separate journal-package reconstruction also passed. There are no unresolved references/citations or overfull/underfull boxes.

All 266 predecessor native files are pinned; all 557 prior complete-edition mathematical labels remain in the active graph, now containing 658 labels. The 296 native files include 52 byte-identical inherited sections, three new proof sections, added primary references, and the native geometry figure.

[Build receipt](papers/GTF-I-v76-matrix-effect-geometry/evidence/BUILD_RECEIPT.json), [source hashes](papers/GTF-I-v76-matrix-effect-geometry/evidence/SOURCE_HASHES.json), [theorem locations](papers/GTF-I-v76-matrix-effect-geometry/evidence/THEOREM_LOCATIONS.json), [package hashes](papers/GTF-I-v76-matrix-effect-geometry/evidence/PACKAGE_MANIFEST.json), and [journal rebuild receipt](papers/GTF-I-v76-matrix-effect-geometry/evidence/JOURNAL_REBUILD_RECEIPT.json) identify the actual submitted materials.

[Journal package](papers/GTF-I-v76-matrix-effect-geometry/evidence/JOURNAL_PACKAGE.zip) contains both focused articles, active sources, response, literature material, and its independent verifier. [Research package](papers/GTF-I-v76-matrix-effect-geometry/evidence/RESEARCH_PACKAGE.zip) includes the complete edition and exact tools. [Native source package](papers/GTF-I-v76-matrix-effect-geometry/evidence/NATIVE_SOURCE.zip) is independently reconstructible.

The publication is a direct child of the native-source commit. The workflow `GTF-I v76 exact-head read-only reconstruction` verifies the actual submitted publication SHA and attaches final-head and independent journal receipts to that run. The referee-ready alias is assigned after that run succeeds. This entry does not substitute an earlier successful run for the submitted object.

Work branch: `revision/general-theta-foundations-i-v76-r49-response-2026-10-04`.
Native-source branch: `revision/general-theta-foundations-i-v76-native-source-2026-10-04`.
Referee-ready branch: `revision/general-theta-foundations-i-v76-referee-ready-2026-10-04`.

The unchanged A/B/C/D analytic obligations are recorded in the [history and pipeline audit](papers/GTF-I-v76-matrix-effect-geometry/HISTORY_AND_PIPELINE_AUDIT.md). Finite computation and source reconstruction do not replace the written mathematical proofs, an independent human priority opinion, or a human authorship signature. The revision supplies concrete additional theorems and review materials; editorial acceptance remains for the referee and editor.
