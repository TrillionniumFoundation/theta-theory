# A2 revision 50 — final review ledger

September 15, 2026. The complete English revision responds to the latest v49 memorandum. This record separates the mathematical changes from content preservation, native builds, publication and sampled layout inspection. It does not constitute a proof certificate or an editorial decision.

## Pinned review, source and publication

| Object | Identity |
|---|---|
| Latest v49 report head | `5051b7789a424656a558179922607d8b55061b28` |
| Actual mathematical source reviewed there | `a003c1c69585f09f0b8fcc9fe03eb330cd6d57b7` |
| v50 workflow preparation | `17fb13a1ee1af533fdd5cbff5a43f28657d7149d` |
| **Actual compiled v50 mathematical source** | **`49f73409b0cc6cb718fbbe48598fd7f5bc9ddca4`** |
| Compiled manuscript subtree | `aef336df33a8754390f74e02f1fd855045095661` |
| Native run / attempt / artifact | `34908647982` / `1` / `10373213966` |
| Retained-product commit | `26bcd8debc3cd04542e8da0624cb82b07a1e0663` |
| Product-attestation head | `d46dd93d2068a8cd950dc4604ebf505cea522ca7` |

Author branch: `revision/a2-v50-relative-core-two-branch-2026-09-15`. Product branch: `revision/a2-v50-native-products-34908647982-1`. The final entry is `revision/a2-v50-review-ready-2026-09-15`, descending from the product-attestation head with navigation and post-download verification only. The actual compiled TeX inputs and native products are not changed by that final entry.

The addressed report and reproduction record are in `reviews/a2-v49-independent-harsh-top4-2026-09-15/` at the pinned head. Both were read completely. The [response](RESPONSE_TO_REFEREE_V50.md) treats the unfavorable placement assessment as an editorial evaluation, not an invented mathematical gap. The [historical audit](HISTORICAL_DERIVATION_AUDIT_V50.md) states the actual dependency-reading scope. The [primary literature check](LITERATURE_CHECK_V50.md) is version-pinned and observation-specific, not an exhaustive priority assertion.

## Mathematical reading map

| Revision or retained interface | Final location |
|---|---|
| Complete unchanged structural statement | Theorem A, p. 4 |
| Exponentially small reference and normalized determinant obstruction | Introduction, equations (1.2)–(1.3), p. 5 |
| Actual smooth remainder and finite signed contact block | Introduction, equations (1.4)–(1.5), pp. 5–6; full inherited proofs remain in Parts I and the auxiliary material |
| Noncircular two-table fiber, with all-lattice geometry and complete filtering | Proposition 19.5, pp. 82–83 |
| Additional marked gap separating those two realizations | Proposition 19.6, p. 83 |
| Unchanged moving-reference and normalization argument | Lemma 20.1, beginning p. 84 |
| Unchanged noncircular derivative kernel and model-local coordinates | Theorems 20.5–20.6, pp. 88–89 |
| Unchanged hard-category calibration | Lemmas 38.7–38.8, p. 151; Theorem 38.9, pp. 152–153; Corollary 38.10, pp. 153–154 |

The C4 example suggested by the referee is attributed in the proposition, acknowledgment and bibliography. It has exactly two realizations with different marked Gram forms, although each local derivative has only the common Euclidean kernel. The extra-gap proposition is proved here for that example. It establishes clearance of the actual closest segment through a radius-tube bound, rather than presuming it lies on the center segment. It does not add a channel hypothesis to Theorem A or claim a universal branch selector.

The proof architecture established in v49 is retained. Part I follows the relative law, signed smooth inverse, analytic images and periodic registration in dependency order; Part II treats local information; Part III treats finite-resolution and physical acquisition. The complete detailed catalogue remains actively compiled in Appendix A.1. No second introduction is reinserted into the core proof.

## Complete native products

The [source-matched delivery](../../deliveries/a2-v50/49f73409b0cc6cb718fbbe48598fd7f5bc9ddca4/) contains both full PDFs, the complete frozen source ZIP, manifests, raw native logs and paired diagnostic outputs.

| Product | Pages | Bytes | SHA-256 |
|---|---:|---:|---|
| Main PDF | 263 | 1971486 | `cd907cac027839c11f89bfccbbad069ad961cd5e0d21499f03028606d7619112` |
| Companion PDF | 7 | 333367 | `b9390b0975c41bdef488dade494e9d8f06150e191d563e052ad7b556174e1eb1` |
| Complete source ZIP | — | 1914215 | `a7e395201f892bb7fc0754b964ab01b9d7be4ab047cd6ad658e22317b17ea272` |

The outer Actions ZIP is a different object: 4289286 bytes, SHA-256 `6ec009358e8dfcd3910fd369a377bcb2c9d26215afdb4ec0142599835a563a96`, matching the GitHub artifact digest.

Both the native and publication jobs succeeded. The native driver read the frozen Git source, built the complete companion first and complete main second with shell escape disabled, and verified their recursive native inputs. The main retains three underfull vertical-box notices, all with badness 10000. There are no overfull boxes, unresolved references/citations or missing-glyph failures. The companion has no corresponding layout notice. Both restricted builds have the expected epstopdf warning that shell escape is disabled.

The publication step verified 41 artifact files in the Git index, pushed the product branch, fetched and verified the committed blobs, committed the attestation, and fetched/verified again. The committed-object record identifies `26bcd8de...`; the later product-attestation head preserves its artifact bytes. This is content verification, not a signed-commit or hostile-compiler attestation. Products are retained Git objects rather than only expiring Actions artifacts.

## Preservation and finite controls

All **106 inherited active inputs** remain active and in the same relative order. **103 are byte-identical in place**. Exact originals of the three amended inputs are archived in `history/v49-review-baseline/`: `main.tex`, `article/00_structural_introduction_v48.tex` and `v5/references_v43.tex`. The amendments concern metadata, additive explanation, the new input and attribution.

The v50 control verifies all **518 inherited theorem-style statement and proof blocks verbatim**, not only the environment totals. All **243 inherited proof environments** survive. One new active module adds two propositions and two proofs, giving **107 active inputs** and **1096 labels**, with no duplicate label or unresolved source reference/citation. In particular, Theorem A, the finite-fiber and noncircular differential proofs, and the quantitative and calibration modules retain their exact statement/proof bodies and hypothesis boundaries.

Five diagnostic families ran in ordinary and optimized Python with identical paired outputs: `check_revision_v50`, `check_quantized_v46`, `check_adaptive`, `check_revision_v32` and `check_revision_v38`. The new controls check the explicit convexity and gap values, determinant-sign filtering, marked Gram forms, symbolic all-lattice determinant identities and the extra-channel margins. A negative control detects nonzero support derivatives at the additional center directions, excluding a radial closest-point shortcut. The old v49/v48/v47 finite controls remain included. These are finite algebra/provenance checks, not an infinite-flight certificate or a numerical reconstruction of an arbitrary table.

## Downloaded-source rebuild and sampled visual scope

The separate download checker verified all **34 build-report evidence entries**, all **567 frozen source files**, all **107 active input identities** and all five diagnostic output pairs. It checked byte lengths, SHA-256 and Git blob identities and verified that no font files were distributed. Every active source also agrees with the earlier local preflight source. The result is [DOWNLOAD_VERIFICATION_V50.json](../../deliveries/a2-v50/49f73409b0cc6cb718fbbe48598fd7f5bc9ddca4/DOWNLOAD_VERIFICATION_V50.json).

The downloaded source was then rebuilt in a fresh extracted directory, again companion first with shell escape disabled. Both complete builds succeeded. The v50 author control was rerun in ordinary and optimized Python and matched both the paired output and the native output byte-for-byte. This is explicitly an author-code rerun, not a separately designed referee implementation. Commands, return codes, final-log hashes and warnings are recorded in [LOCAL_REPRODUCTION_V50.json](../../deliveries/a2-v50/49f73409b0cc6cb718fbbe48598fd7f5bc9ddca4/LOCAL_REPRODUCTION_V50.json).

All **263 main pages and seven companion pages** agree with both the preflight and the downloaded-source rebuild in extracted text and same-renderer 72-dpi RGB pixels. No extracted text span lies outside its page. PDF byte streams differ; byte-identical PDF reproduction is not claimed. The fresh comparison is recorded in [REBUILD_VERIFICATION_V50.json](../../deliveries/a2-v50/49f73409b0cc6cb718fbbe48598fd7f5bc9ddca4/REBUILD_VERIFICATION_V50.json).

Sampled visual inspection covered main pages **1, 3–7, 81–84, 150–154, 177 and 263**, and companion pages **1 and 7**, through 108-dpi individual pages and layout sheets. Main pages 82–83 were additionally inspected as 120-dpi Poppler renders; the native Poppler rendering of page 83 was opened after download. Inspected preflight samples match the native samples at 108 dpi. No clipping, text/formula overlap or broken glyph was found on the listed pages. This is not a claim of individual visual inspection or mathematical review of all 270 pages. See [VISUAL_REVIEW_V50.json](../../deliveries/a2-v50/49f73409b0cc6cb718fbbe48598fd7f5bc9ddca4/VISUAL_REVIEW_V50.json).

The retained `verify_download_v50.py` accepts `--native`, optional `--local-build`, and optional `--artifact-zip` with `--artifact-sha256`; it requires PyMuPDF and performs no network or repository writes. Its operational checks do not replace the written geometry, the relative-operator estimates or independent refereeing.

No A1 source, unrelated paper, historical review, default branch, branch protection or collaborator permission was modified. The next referee should assess the central relative/smooth inverse and the complete two-branch geometry separately from these operational records.
