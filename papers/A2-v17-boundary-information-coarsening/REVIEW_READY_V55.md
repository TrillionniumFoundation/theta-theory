# A2 revision 55 — final review ledger

September 15, 2026. The complete English revision responds to both v54 referee-style memoranda. This ledger separates manuscript changes, content preservation, native publication, downloaded-source rebuilding and sampled visual review. No operational result is a mathematical certificate or a journal decision.

## Frozen identities

| Object | Identity |
|---|---|
| Latest, second v54 memorandum | `67250d08714acf76274e82158f107246f0de7eee` |
| First v54 memorandum | `1030ca91a96ca1be8ecd0347ecbdac7084cdd8d4` |
| Actual mathematical source reviewed by both | `2cedae961195f97df802aaa81112d95cd32974e1` |
| v55 workflow preparation | `27956302dd20baf623f2881502be7d68ee29e72d` |
| **Actual compiled v55 mathematical source** | **`3903f5b8a5ffb0d0a69065b1d303c247c06ebf69`** |
| Compiled manuscript subtree | `8ff45d47f7dd78bc0c0d4ae284dde147a47d87e9` |
| Native run / attempt / artifact | `34943642385` / `1` / `10385962782` |
| Retained-products commit | `a3654c14fd6126c858c828cdbb9d2ad54eafcc7b` |
| Product-attestation head | `f9613aed7b11e5f94e0d22bbc4e399e4393f8a12` |

Source branch: `revision/a2-v55-stopped-record-reduction-2026-09-15`. Products branch: `revision/a2-v55-native-products-34943642385-1`. Final review branch: `revision/a2-v55-review-ready-2026-09-15`, descending from the product-attestation head with navigation and verification additions only. No compiled TeX input or native PDF is changed by the final review layer.

The new source inherits the second memorandum and copies the first report directory from its frozen commit. Both original review branches are untouched. Both complete report texts and their actual recommendations were read; the second audit ledger was read to identify its proof coverage and overlap with the first. [The response](RESPONSE_TO_REFEREE_V55.md) addresses both. [The historical audit](HISTORICAL_DERIVATION_AUDIT_V55.md) states the dependency-reading limits, and [the primary-record check](LITERATURE_CHECK_V55.md) distinguishes observation scopes without claiming exhaustive priority.

## Mathematical revision and reading map

| Point | Final location |
|---|---|
| Revised abstract and common-measure interpretation | p. 1; existing introduction, pp. 8–9 |
| Unchanged strengthened finite-flight comparison | Corollary 23.3, pp. 106–108 |
| Definitions of full record, censored count and acceptance bit | p. 109, immediately before Theorem 23.4 |
| All original stopping, deficiency, cap-risk and charge conclusions | Theorem 23.4(1)–(3), p. 109; original proof retained on pp. 110–111 |
| Uniform-in-cap count sufficiency and absolute risk error | Theorem 23.4(4), equations (23.22)–(23.23), p. 109 |
| Exact integer count threshold and count-only risk | Equations (23.24)–(23.25), p. 109 |
| Distinct exact full-record overlap identity | Equation (23.26), p. 110 |
| Finite-intensity bit reduction, Bernoulli limit and large-cap boundary | Theorem 23.4(5), equations (23.27)–(23.29), p. 110 |
| Complete new proofs and realized-charge distinction | pp. 111–112 |
| Joint attribution and compiled catalogue | Acknowledgment / Appendix A.1 transition, p. 196; bibliography items [45]–[46], p. 283 |

The count kernel preserves the actual censored count and hence its realized charge. Its error is exactly `a_1(b) eta_h` under alternative one and zero under zero, giving a comparison uniform over all deterministic caps. The full risk is not declared equal to the count-risk formula: it has its own overlap integral, and their difference is bounded in absolute error. The bit kernel instead simulates the full zero-alternative law conditional on acceptance. Its error is at most `a_1(b)`; at finite cap intensity the full experiment converges in Le Cam distance to an explicit Bernoulli pair. At caps satisfying `b_h p_1,h -> infinity`, the bit loses discrimination and its reverse deficiency to the full record tends to one half. Unlike the count kernel, this bit simulation need not preserve realized stopping time.

The count/bit reductions and exact count formula are attributed to the first memorandum and the overlapping check in the second, not represented as two independent contributions. They extend the existing theorem rather than add another theorem or section. The nonlinear relative boundary law, actual-smooth signed inverse, exact/window/geometric and differential theorems, and older quantitative/calibration results keep their original scope. These specified-pair probability conclusions are not a uniform unknown-profile estimator, a new geometric breakthrough or a sensor-independent preparation optimum.

## Complete retained products

The [native delivery](../../deliveries/a2-v55/3903f5b8a5ffb0d0a69065b1d303c247c06ebf69/) contains both full PDFs, a frozen source ZIP, source manifests, native logs and finite diagnostic outputs.

| Product | Pages | Bytes | SHA-256 |
|---|---:|---:|---|
| Main PDF | 283 | 2095080 | `eb55c356dec431ae747c0129852bd65207c874400db9804354e43355aaa6a0e3` |
| Companion PDF | 7 | 333367 | `b9390b0975c41bdef488dade494e9d8f06150e191d563e052ad7b556174e1eb1` |
| Complete source ZIP | — | 2248975 | `050da4a797d5ef0304e5731d56667fb0536c560f409eadb27a49d3f7777cf650` |

The distinct outer Actions ZIP has 4746341 bytes and SHA-256 `848adf607bd34ee8013827a7ab1a7d98cfe88cccfc566fc9948747b603c9a5b6`, matching the dedicated GitHub artifact response.

Both the native and publication jobs completed successfully. The complete companion was compiled before the complete main with shell escape disabled. The unchanged driver checked actual source Git objects, recursive native inputs and the companion auxiliary input imported by the main. The final native main log has three underfull vertical-box notices, with badness 1057, 10000 and 10000. The final scans have no overfull box, unresolved reference/citation or missing glyph in the checked categories. The companion has no corresponding layout notice. This is not described as a warning-free build.

The publication job verified 41 artifact files in the index, pushed and fetched the product branch, verified the committed blobs, committed an attestation and fetched/verified again. The [committed-object record](../../deliveries/a2-v55/3903f5b8a5ffb0d0a69065b1d303c247c06ebf69/COMMITTED_OBJECTS_VERIFIED.json) identifies `a3654c14...`; the later attestation head preserves the artifact bytes. These products are retained Git objects rather than only expiring Actions artifacts. Content verification is not a signed-commit or hostile-compiler attestation.

## Preservation and finite checks

All 111 inherited active inputs remain active in the same relative order. 107 remain byte-identical in place. Exact originals of `main.tex`, the existing structural introduction, the Section 23 module and the main bibliography, plus the baseline active manifest, are archived under `history/v54-review-baseline/`.

The checker finds 544 of 546 inherited statement/proof blocks verbatim. The other two are exactly Theorem 23.4 and its proof with inserted text only: removing the prescribed insertions recovers their old bytes exactly. The inventory is unchanged, including 257 proofs; no theorem number, section or proof environment is added. All inherited labels remain, with 1160 labels in the final graph and no duplicate or unresolved source reference/citation. The complete catalogue remains actively compiled in Appendix A.1.

Five diagnostic families passed in ordinary and optimized Python with identical paired output: `check_revision_v55`, `check_quantized_v46`, `check_adaptive`, `check_revision_v32` and `check_revision_v38`. The new finite controls cover 90 exact capped laws with equal, unequal and disjoint marks, including 30 tie-decision checks and 51 cases with strict finite full-mark improvement. They check simulation error, risk overlap, charge preservation, the finite-intensity comparison and large-cap boundaries. In a finite probability control with `p_0=0.001`, `p_1=0.000001`, and cap one billion, the count threshold is 6912 and its risk is about 0.003940248534, while the bit risk is one half. This is a probability-law control, not an extra billiard realization. Earlier finite controls are retained.

## Downloaded-source rebuild and actual visual coverage

The [separate verifier](../../deliveries/a2-v55/3903f5b8a5ffb0d0a69065b1d303c247c06ebf69/verify_download_v55.py) imports no author code and performs no build or network operation. It verified the outer artifact digest, all 34 native build-evidence entries, all 640 frozen source files by byte count/SHA-256/Git blob identity, the nested manifest, all 111 active inputs and all five diagnostic pairs. It reconstructs the manuscript Git tree from the verified modes and blobs, obtaining `8ff45d47f7dd78bc0c0d4ae284dde147a47d87e9`. No font files are distributed.

Both complete entries were rebuilt from a fresh extraction of the downloaded source with shell escape disabled. All 283 main pages and seven companion pages agree with the native products in extracted text and same-renderer 72-dpi RGB arrays. PDF byte hashes differ, and byte identity is not claimed. No extracted text span lies outside its page. [REBUILD_VERIFICATION_V55.json](../../deliveries/a2-v55/3903f5b8a5ffb0d0a69065b1d303c247c06ebf69/REBUILD_VERIFICATION_V55.json) records the actual hashes, counts and renderer version.

The downloaded author checker was rerun in ordinary and optimized Python. Both outputs agree with one another and with the native v55 diagnostic output. This is an author-code rerun, not a separately designed referee implementation. Commands, successful return codes, final-log hashes and the three retained local underfull notices are in [LOCAL_REPRODUCTION_V55.json](../../deliveries/a2-v55/3903f5b8a5ffb0d0a69065b1d303c247c06ebf69/LOCAL_REPRODUCTION_V55.json).

Sampled visual inspection covered main pages 1, 4, 7–9, 106–113, 196 and 283, and companion pages 1 and 7. It used 108-dpi individual pages and four-page layout sheets; native main page 110 was additionally opened as a Poppler render with longest side 1500 pixels. Inspected main samples match the preflight at 108 dpi. No clipping, text/formula overlap or broken glyph was observed on these pages. The [visual record](../../deliveries/a2-v55/3903f5b8a5ffb0d0a69065b1d303c247c06ebf69/VISUAL_REVIEW_V55.json) distinguishes this sampled coverage from the automatic 290-page comparison. No fresh individual visual or mathematical reading of every page is claimed.

For reproduction, the verifier accepts `--native <evidence-directory>`, optional `--local-build <rebuilt-source-directory>` and optional `--artifact-zip <Actions-ZIP>`, and requires PyMuPDF. Build the complete companion before the main using the commands in the local record, or use `tools/build_submission.py` from a checkout of the pinned source. Run `tools/check_revision_v55.py` with and without `-O` for the author controls. No A1 file, unrelated workstream, default branch, prior report, branch protection or repository permission was changed. The next mathematical review and the nonbinding placement judgment remain separate from all verification results above.
