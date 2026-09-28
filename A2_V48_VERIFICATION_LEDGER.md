# A2 v48 — final verification ledger

September 14, 2026. This ledger concerns the complete author revision responding to the latest v47 report. It distinguishes manuscript content, finite diagnostics, a native build, publication of Git objects, and sampled visual inspection. None of these operational checks constitutes a mathematical proof certificate or a journal acceptance decision.

## Authoritative source and publication

| Object | Pinned identity |
|---|---|
| Latest v47 review head | `757f2ee4e3bf766d2eb56d972e6d2f621b3fd2a6` |
| Actual reviewed v47 mathematical source | `219b39e94b14187561dc3b7e5bdbae49dbd92cc2` |
| Final v48 workflow-preparation commit | `3bc2c620b6f5e56039286d0c8abab730499085e3` |
| **Final v48 mathematical source** | **`fe21046e47a89ec3b3df8493f4d885b087e3ad7f`** |
| Final source subtree | `60d2cc48b3ce645d984724e9aa8ab26014c74522` |
| Native run / attempt | `34852676783` / `1` |
| Native artifact | `10351522484` |
| Artifact ZIP SHA-256 | `bee6a759c375a030a4b9540e23ec887374e01d336706e89302f781639efeab07` |
| Retained product commit verified after push | `3bbeff756c03a9b51362a23e418082ee64852028` |
| Product-attestation head, fetched and verified again | `67b3bf5a5b83b81b0cdcd07d74b19bf5c9569fcf` |

Author branch: `revision/a2-v48-infinitesimal-rigidity-2026-09-14`. Product branch: `revision/a2-v48-native-products-34852676783-1`. The review-ready branch `revision/a2-v48-review-ready-2026-09-14` descends from that product-attestation head and adds only navigation and verification records; it does not amend a compiled TeX input.

Before handoff, the observation squares were made explicitly contact-centered, with closures inside the positive-density region and fixed nonzero scalar anchors, as required by the four-density inverse. The successful earlier build of source `cf3d60fb1f8d4f32bb08b4c7016f0d9a5153b989` in run `34850920287` remains historical evidence, **not the final review target**. The final source above was rebuilt in full after this clarification.

## Complete products

All products below are under [`deliveries/a2-v48/fe21046e47a89ec3b3df8493f4d885b087e3ad7f/`](deliveries/a2-v48/fe21046e47a89ec3b3df8493f4d885b087e3ad7f/), not a sampled-chapter compilation.

| Product | Pages | Bytes | SHA-256 |
|---|---:|---:|---|
| [Main manuscript](deliveries/a2-v48/fe21046e47a89ec3b3df8493f4d885b087e3ad7f/main.pdf) | 255 | 1930660 | `6ca3bc8f50a399d574b7912a5c4390a35eabb0020b50578f2a2b026c23e2a6e4` |
| [Two-collision companion](deliveries/a2-v48/fe21046e47a89ec3b3df8493f4d885b087e3ad7f/two_collision.pdf) | 7 | 333367 | `b9390b0975c41bdef488dade494e9d8f06150e191d563e052ad7b556174e1eb1` |
| [Complete source archive](deliveries/a2-v48/fe21046e47a89ec3b3df8493f4d885b087e3ad7f/native-source.zip) | — | 1781899 | `8e6968aa48d0eca3e0844c80bdab57c2c3d1c727be2dfecb4722477df98b06ff` |

The workflow validates the source snapshot, recursive input graph, both real TeX invocations, and the generated companion auxiliary input imported by the main. Both entries passed. There are no unresolved references, unresolved citations, overfull boxes or missing-glyph failures in the final native logs. The main retains four underfull vertical-box warnings, with badness values 1902, 2608, 10000 and 10000; the companion has no layout warning in its build report. These warnings have not been relabelled as a warning-free build.

The native publication step verified **41 retained artifact files as Git blobs after pushing and fetching the product branch**, then verified them again at the attestation head. [The committed-object attestation](deliveries/a2-v48/fe21046e47a89ec3b3df8493f4d885b087e3ad7f/COMMITTED_OBJECTS_VERIFIED.json) names the earlier retained-product commit it verified; the subsequent head preserves those same artifact blobs. The job log of run `34852676783` records the second fetched-head verification. The attestation concerns content hashes, not a signed-commit or hostile-compiler attestation.

## Preservation and finite diagnostics

The [v48 preservation control](deliveries/a2-v48/fe21046e47a89ec3b3df8493f4d885b087e3ad7f/check_revision_v48-normal.json) checked all **103 inherited active inputs** against the source-matched v47 manifest. **101 remain byte-identical in place**. Exact originals of `main.tex` and `article/01_introduction_v41.tex` are archived in [`history/v47-review-baseline/`](papers/A2-v17-boundary-information-coarsening/history/v47-review-baseline/); only the title/abstract/entry organization and the earlier introduction's section heading were editorially amended. Every inherited mathematical statement and proof remains active, with the inherited input order retained.

The final recursive graph has **105 distinct inputs** after adding the structural introduction and differential-rigidity section. In the combined main/companion source, all 87 inherited theorem, 70 lemma, 40 proposition, 40 corollary, five definition, 22 remark and **232 proof environments** survive. The new modules add Theorem A, four lemmas, two theorems and seven proofs. There are 1067 active labels, with no duplicate label or unresolved active-source reference in the static control.

Five diagnostic families ran in ordinary and optimized Python with byte-identical outputs: `check_revision_v48`, `check_quantized_v46`, `check_adaptive`, `check_revision_v32` and `check_revision_v38`. The new exact finite controls cover the differentiated four-density and anchor identities, the finite three-harmonic Bezout witness `(6,10,15)`, the non-unimodular gain matrix of determinant six, finite two-by-two jet blocks through degree twelve, and negative controls distinguishing exact injectivity from immersion and detecting an omitted gain-matrix inverse. The v47 cap, hard-cell and charged-calibration controls remain included. These are finite algebra/provenance controls, not an independently realized billiard simulation or certification of the infinite-flight theorem.

## Referee reading map

| Issue or statement | Final location |
|---|---|
| Structural synthesis of exact, infinitesimal and model-local conclusions | Theorem A, p. 4; introduction, pp. 3–6 |
| Parameter differentiation, including moving-support normalization | Lemma 20.1, pp. 89–90 |
| Actual smooth signed contact-jet derivative kernel | Lemma 20.2, pp. 90–91 |
| Analyticity of the support variation, not merely of parameter slices | Lemma 20.3, p. 91 |
| Finite-harmonic differentiable registration and unknown lattice | Lemma 20.4, pp. 91–92 |
| Full-table infinitesimal single-offset rigidity | Theorem 20.5, pp. 92–93 |
| Scalar coordinates on an immersed finite-dimensional model | Theorem 20.6, p. 93 |
| R47-C1: offset and normalizer error | Old Lemma 19.7 → Lemma 21.7, p. 101 |
| R47-C2: internal and outer hard-cell edges | Old Lemma 19.8 → Lemma 21.8, p. 102 |
| R47-C3: pilot conditioning and confidence radius | Old Theorem 19.9 → Theorem 21.9, pp. 102–103 |
| R47-C4: fixed-flight pilot and strict finite budget | Old Corollary 19.10 → Corollary 21.10, pp. 103–104 |

See the [point-by-point response](papers/A2-v17-boundary-information-coarsening/RESPONSE_TO_REFEREE_V48.md) and [historical derivation audit](papers/A2-v17-boundary-information-coarsening/HISTORICAL_DERIVATION_AUDIT_V48.md). In particular, the fixed-contact finite-jet variation bundle in the inherited section is not relabelled as the new whole-table, moving-lattice single-offset kernel theorem. The new finite-dimensional coordinate conclusion is not imposed as a restriction on the inherited infinite-dimensional exact theorem.

## Downloaded artifact and visual coverage

The downloaded Actions ZIP digest agrees with GitHub's artifact digest. The post-download checker verifies the 34 entries in the native build report's evidence manifest, every archived active input's SHA-256 and Git blob identity, and all five ordinary/optimized diagnostic pairs. All 105 active source files also match the separately compiled local preflight source. Using the same PyMuPDF renderer on both PDFs, **all 255 main pages and all seven companion pages agree in extracted text and in their 72-dpi pixel arrays**. No extracted text span lies outside its page. This is a same-renderer parity test, not a second independent rendering-engine test.

Rendered visual inspection covers main pages **1–6, 88–94 and 101–105**, and companion pages **1 and 7**, using individual 108-dpi pages and four-page layout sheets. It includes Theorem A, the complete new differential section and the retained calibration results. The final changed pages were opened after the final native artifact was downloaded; inspected unchanged pages were additionally verified by render equality. No clipping, overlapping text/formulas or broken glyph was found on those pages. **This is sampled visual coverage, not a claim of a fresh page-by-page human review of all 262 pages.** [The explicit visual scope](deliveries/a2-v48/fe21046e47a89ec3b3df8493f4d885b087e3ad7f/VISUAL_REVIEW_SCOPE.json) and [post-download result](deliveries/a2-v48/fe21046e47a89ec3b3df8493f4d885b087e3ad7f/DOWNLOADED_PRODUCTS_VERIFIED.json) are retained separately from the build report, whose own visual-review field correctly says that its script performs none.

The retained [post-download checker](deliveries/a2-v48/fe21046e47a89ec3b3df8493f4d885b087e3ad7f/verify_download_v48.py) can be run with `--evidence <native-delivery-directory>` and, optionally, `--local-build <separately-compiled-source-directory>`. It requires PyMuPDF; it performs no network or repository write. For a fresh native rebuild from a checkout of the final source, the existing `tools/build_submission.py` is the complete-entry driver.

No A1 source, unrelated paper, default branch, historical review, branch protection or collaborator permission was changed. The next independent referee should assess the new derivative-kernel proof and the significance of the revised structural theorem separately from these operational checks.
