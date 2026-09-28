# A2 v45 — completed native delivery and verification

## Exact identities

| Role | Identity |
|---|---|
| Addressed independent v44 report | `c984b5a5f0dee0e3a9c78264ff7b5136272fec72` |
| Compiled v44 mathematical baseline | `b229bfa2df2962ea2ebfd0fb2fd11531036d33a6` |
| Actual compiled v45 source | `2f064b86b4e071d24ad671f4dc652d7de32a56a4` |
| v45 repository source tree | `5ebb00d9c56eb65948f81bd2403f40bc85e32758` |
| v45 paper source subtree | `b60d6f03d9c6c882a811d67c331640f82848bbcc` |
| Native and publication Actions run | `34829418911`, attempt 1; both jobs completed successfully |
| Retained native artifact | `10341144241` |
| First published products commit | `5633e0553305dad7ab8f390b30ed64be83ef7791` |
| Products plus fetched-object attestation | `e10c054655c452b2d3b5edf49e439ab2154772fe` |
| Separate local native-validation commit | `51ef9d3d8ea1fc1a479ce11cece360aeb6861593`; local only, not a GitHub source identity |

The review-ready branch is `revision/a2-v45-review-ready-2026-09-14`. Its final navigation commit descends from the products/attestation commit and changes documentation only. It is not falsely designated as the source from which the PDFs were compiled. The author branch is `revision/a2-v45-generic-finite-channel-rigidity-2026-09-14`; the products branch is `revision/a2-v45-native-products-34829418911-1`.

## Actual native products

All paths below are relative to `deliveries/a2-v45/2f064b86b4e071d24ad671f4dc652d7de32a56a4/`.

| Product | Extent | SHA-256 |
|---|---|---|
| `main.pdf` | 235 pages; 1,819,269 bytes | `cd097ca221cb6e1ca8d1259adbda7dbd3a9837fbe30bc82bc3d995b6500e4c9c` |
| `two_collision.pdf` | 7 pages; 333,367 bytes | `b9390b0975c41bdef488dade494e9d8f06150e191d563e052ad7b556174e1eb1` |
| `native-source.zip` | 1,599,819 bytes | `c62a107a203351f83c466935574fbb509138f2c0506f0fbaa8f508418a51d1d0` |

The companion PDF is byte-identical to the retained v44 companion. The article is the full native main, not a summary PDF. The main compiled its 98 recursive native source inputs, the bibliography, and the separately produced companion auxiliary input; the companion has its own unchanged native entry. All 99 active manifest entries match the separate local build by byte count, Git blob ID and SHA-256. The local full source archive differs in documentation/checkpoint context and has a different Git identity; no claim of complete archive equality is made.

Both hosted entries compiled successfully with the preserved `build_submission.py`, which freezes committed Git bytes, checks each compilation copy, disables shell escape, records actual native inputs and verifies the companion-generated auxiliary file consumed by the main. No unresolved reference or citation, duplicate label/destination, missing glyph, or overfull box occurred. The hosted main has six underfull vertical-box notices; the companion has none of these notices. The local toolchain additionally warns that shell escape is disabled, as intended.

## Source preservation and finite diagnostics

`check_revision_v45.py` verified every one of the 97 v44 active manifest entries, using the exact archived old main for its old identity. All 216 inherited theorem/lemma/proposition/corollary/definition environments and all 22 inherited remarks remain active; 10 theorem-style environments are added. The previous direct input order is unchanged. The native source graph and static reference/citation checks pass.

`check_skeleton_v45.py` passed on 18 periodic disk tables with 301 clear candidate edges and on 73 independently posed complete-image reconstruction cases. Negative controls reject third-body tangency, disconnected graphs, rank-one gains, a tree without deck cycles, and zero harmonic anchors. A gain matrix of determinant 6 tests nonunimodular reconstruction. Hosted maximal residuals are approximately `5.69e-15` for the lattice, `5.78e-15` for centers and `1.14e-13` for the Gram form. These are finite floating-point diagnostics, not a proof, a billiard-law simulation, or an empirical-law-to-infinite-jet inverse. Cross-platform residuals need not be byte-identical.

Both v45 diagnostics produced byte-identical ordinary/optimized JSON within each execution environment. The inherited native driver also passed its adaptive finite algebra, v32 diagnostics and all 41 v38 provenance regression cases in ordinary and optimized Python. Those v38 regression fixtures explicitly mock TeX in their unit tests; they are distinct from the actual complete TeX builds recorded above.

## Publication verification

The publication job copied the actual native artifact into the declared delivery subtree, force-staged only that subtree, verified its Git index, committed and pushed it to a new products branch, then fetched that branch and verified the actual committed blobs. It committed `COMMITTED_OBJECTS_VERIFIED.json` separately, pushed again, fetched again and reverified all promised files. Both jobs and the final fetch/verify step passed in Actions run `34829418911`.

The committed attestation identifies the first products commit `5633e0553305dad7ab8f390b30ed64be83ef7791` and **39 artifact/evidence files**, including both PDFs, source ZIP, raw native logs, recorders, generated auxiliary products, manifests and diagnostics. The final products head `e10c054655c452b2d3b5edf49e439ab2154772fe` adds the attestation without changing those 39 files. A source-tree comparison shows no mathematical source change between the author commit and the products commits. This attestation is an executed Git-object integrity record within the Git/toolchain trust boundary, not an independent mathematical certificate or a cryptographic author signature.

## Visual examination and cross-build comparison

The downloaded hosted PDFs were compared page by page with the separate local native build. **All 235 main pages and all seven companion pages have identical extracted text and identical 72-dpi rendered pixels**. The PDFs are not claimed byte-identical across the different compilation environments. The executed parity result is retained in `LOCAL_COMPARISON_V45.json`.

Readable-resolution rendered examination covered main pages **1, 8, 9 and 78–85**, including the complete new Section 18, its interface with the retained realization and following section, the introductory theorem and the abstract. No clipped formula, overlap, broken glyph or unresolved reference was observed on those pages. All seven companion pages received a contact-sheet overview. These scopes are deliberately distinguished: this is not a readable-resolution inspection or a new mathematical audit of every inherited page.

The new statements appear as introductory Theorem 1.3 and Section 18: Lemmas 18.1–18.2, Theorem 18.3, Lemma 18.4, Propositions 18.5–18.6, Theorem 18.7, Proposition 18.8 and Corollary 18.9. The main generic determination theorem is 18.7 on pages 82–83; the full new section spans pages 78–85.

## Reproduction and scope

Check out the actual compiled source commit above. Run `python3 -B papers/A2-v17-boundary-information-coarsening/tools/check_revision_v45.py` and `check_skeleton_v45.py`, repeat with `python3 -O -B`, and compare outputs. With the native TeX toolchain installed, run `tools/build_submission.py --output-dir <empty-directory-outside-paper>`. The workflow file records the exact commands and pinned action versions. The preserved source-checkpoint ledger is under `history/v45-source-checkpoint/`.

The complete paper, response and all historical mathematical materials remain available. Compilation, source identity, finite diagnostics and visual checks do not settle general-journal significance, establish exhaustive priority, or replace the next independent mathematical review.
