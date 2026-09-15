# A2 revision 54 — final review ledger

September 15, 2026. This ledger identifies the complete English revision responding to the latest v53 memorandum. Mathematical changes, source preservation, native publication, local reproduction and sampled layout inspection are separate records. None constitutes a journal decision or a proof certificate.

## Frozen identities and full products

| Object | Identity |
|---|---|
| Addressed v53 review head | `000ce24f65f8381d2180cbd1f080d3d8470c8157` |
| Actual reviewed v53 source | `42cc62f230473c34d78af1d06b9ca5c2651ae86d` |
| v54 workflow preparation | `eb6989f624e7417db92140841710c22719cc1cd2` |
| **Actual compiled v54 mathematical source** | **`2cedae961195f97df802aaa81112d95cd32974e1`** |
| Compiled manuscript subtree | `407b278984b14e57468e727fb56b0fa4163a7207` |
| Native run / attempt / artifact | `34934158178` / `1` / `10382712647` |
| Retained-products commit | `5f168a195d9f04ba8e6b1aa23dbe9a24eeaac6f2` |
| Product-attestation head | `47d64975211909c0d30be9050444cab667545e88` |

Source branch: `revision/a2-v54-stopped-window-experiments-2026-09-15`. Products branch: `revision/a2-v54-native-products-34934158178-1`. Final review entry: `revision/a2-v54-review-ready-2026-09-15`, descending from the verified products and adding only navigation and post-download records. No compiled mathematical input or native product changes in this final layer.

The [complete retained delivery](../../deliveries/a2-v54/2cedae961195f97df802aaa81112d95cd32974e1/) contains both PDFs, full frozen source, manifests, native logs and paired diagnostics.

| Product | Pages | Bytes | SHA-256 |
|---|---:|---:|---|
| Main PDF | 281 | 2080784 | `393f471cc623d446fdec58b3c05fabc5f3bfc4b620f9194950523dfe601d0552` |
| Companion PDF | 7 | 333367 | `b9390b0975c41bdef488dade494e9d8f06150e191d563e052ad7b556174e1eb1` |
| Complete source ZIP | — | 2178095 | `46e5ca2a859424e3362baae1747551d3e54a8c5e67c3bac8788ba536f3c9b4f6` |

The outer Actions ZIP is a distinct object: 4661563 bytes, SHA-256 `d7572bce8b3a9131685f9a76cab47b381e60bf99aaf9c7dd4adf0444e5419610`, matching GitHub's artifact digest.

## Mathematical changes and referee reading map

The complete v53 report and audit ledger were read, including their continuations. The report identified no mandatory new theorem correction. The revision strengthens the finite-flight interface and completes the comparison of records in the same Section 23; it does not manufacture an error in the previously accepted reasoning or append an unrelated section.

| Point | Final location |
|---|---|
| Revised account of conditional marks, waiting records and capped acquisition | Existing introduction, p. 8 |
| Original realized nonlinear pair and attained successful-record scale | Lemma 23.1 and Theorem 23.2, pp. 103–106, unchanged |
| Uniform density bound, quadratic Hellinger error and square-root product comparison | Strengthened Corollary 23.3, pp. 106–108; equations (23.12)–(23.15) |
| Direct finite-flight moment-test bound without full-product approximation | Corollary 23.3 and proof, pp. 107–108 |
| Unchanged accepted mass and expected n-success charge | Equation (23.16), p. 107; proof, p. 108 |
| First-acceptance experiment and binary deficiency convention | Subsection 23.4, p. 108 |
| Waiting/mark separation, reverse deficiency one half, deterministic-cap risk and charge | Theorem 23.4, pp. 109–110; equations (23.18)–(23.25) |
| Attribution and retained compiled catalogue | Acknowledgments / Appendix A.1 transition, p. 194; bibliography item [44], p. 281 |

The corollary improves the product bound from `C n tau^J` to `C sqrt(n) tau^J`, and its sufficient condition to `n tau^(2J) -> 0`. The original condition and bound are expressly retained as weaker consequences. The direct mean test instead needs `tau^J=o(h^4)` and gives an exponential risk bound directly, without requiring the full growing products to be close.

Theorem 23.4 uses the same actual two-table/profile alternatives. Their acceptance probabilities satisfy `p_i asymp h^2 exp(-gamma_i J_h)` with `gamma_1>gamma_0`. It proves the reviewer-supplied reverse binary deficiency limit and develops the deterministic-cap conclusion: optimal equal-prior error tends to `exp(-lambda)/2` when `b_h p_0 -> lambda < infinity`; consistency is possible exactly when `b_h p_0 -> infinity`. The shared no-acceptance atom supplies both sides of the finite-cap total-variation bound. Expected stopped charge is obtained by a tail sum, not by treating an uncapped expectation as a deterministic guarantee. Tests concern the specified pair; no uniform unknown-profile estimator or universal charged inverse complexity is asserted.

The Hellinger and first-waiting-record contributions are attributed to the v53 memorandum. The deterministic-cap risk is proved here. Theorems A/B, the original h^(-8) mark-scale theorem, window extraction, geometric fibers, unknown-lattice and differential rigidity, and the older quantitative/calibration theory retain their conclusions and assumptions. See [the response](RESPONSE_TO_REFEREE_V54.md), [historical audit](HISTORICAL_DERIVATION_AUDIT_V54.md), and [primary-record check](LITERATURE_CHECK_V54.md).

## Preservation and finite checks

All **111 inherited active inputs** remain active, in the same relative order. **107 are byte-identical in place**. Four exact originals and the baseline active manifest are archived in `history/v53-review-baseline/`: `main.tex`, the existing structural introduction, the realized-window module, and the main bibliography.

The checker verifies **542 of the 544 inherited statement/proof blocks verbatim**. The two exceptions are exactly Corollary 23.3 and its proof, strengthened in place. Their original bytes are archived and every former conclusion remains a consequence. They are not incorrectly labelled byte-identical. The original inventory includes 256 proofs; 255 remain verbatim, one is strengthened, and one new theorem-proof is added. The final graph still has 111 inputs and has 1152 labels, with no duplicate label or unresolved source reference/citation. The entire old catalogue remains actively compiled in Appendix A.1. The companion is unchanged.

Five diagnostic families passed in ordinary and optimized Python with identical paired output: `check_revision_v54`, `check_quantized_v46`, `check_adaptive`, `check_revision_v32`, and `check_revision_v38`. The new finite controls test positive-density Hellinger order, affinity tensorization, the strict improvement of the joint flight condition, the direct-test margin, normalized capped laws with unequal marks, common-cemetery bounds, exact expected capped charge and the mixture-kernel upper bound. Negative controls detect loss of the density floor, an off-by-one waiting convention and failure of the any-acceptance test when the cap is too large for that particular statistic. Earlier finite v53–v47 controls are retained. These are finite distribution/algebra checks, not a proof of the infinite-flight construction.

## Native publication and downloaded-source reproduction

Both native and publication jobs succeeded. The unchanged native driver compiles the complete companion first and then the complete main with shell escape disabled, using the actual frozen Git source. It checks all recursive native inputs and the companion auxiliary input imported by the main. Native final scans found no overfull box, unresolved reference/citation or missing glyph. The main retains **four underfull vertical-box notices**, with badness 1057, 10000, 10000 and 10000; the companion has no corresponding layout notice. We do not call this a warning-free build.

The publication job verified 41 artifact files in the Git index, pushed and fetched the product branch, verified its committed blobs, committed an attestation and fetched/verified again. The [committed-object record](../../deliveries/a2-v54/2cedae961195f97df802aaa81112d95cd32974e1/COMMITTED_OBJECTS_VERIFIED.json) names the retained-products commit; the subsequent attestation head retains the same artifact bytes. Products are stored Git objects, not only expiring workflow artifacts. This is content verification, not signed-commit or hostile-compiler attestation.

The separate [download verifier](../../deliveries/a2-v54/2cedae961195f97df802aaa81112d95cd32974e1/verify_download_v54.py) checked the outer artifact digest, all 34 build-report evidence files, all **626 frozen source files**, all 111 active identities, the nested source manifest and all five diagnostic pairs. It reconstructs the Git source tree from the verified file modes and blob hashes and obtains `407b278984b14e57468e727fb56b0fa4163a7207`. No font files are distributed.

Both complete entries were rebuilt from a fresh extraction of the downloaded source. All **281 main pages and seven companion pages** agree with the native products in extracted text and same-renderer 72-dpi RGB arrays. The separately compiled preflight also agrees. Native and rebuilt PDF byte hashes differ; byte-identical reproduction is not claimed. No extracted text span lies outside its page. The result is [REBUILD_VERIFICATION_V54.json](../../deliveries/a2-v54/2cedae961195f97df802aaa81112d95cd32974e1/REBUILD_VERIFICATION_V54.json).

The downloaded author checker was rerun in both Python modes and agrees with the native result byte-for-byte. This is an author-code rerun, not a separately designed referee implementation. [LOCAL_REPRODUCTION_V54.json](../../deliveries/a2-v54/2cedae961195f97df802aaa81112d95cd32974e1/LOCAL_REPRODUCTION_V54.json) records commands, return codes, final log hashes, warnings and the local harness interruption: both builds had completed, the optimized checker was rerun separately, and all final comparisons passed. Local restricted-shell builds also emit the expected epstopdf notice that shell escape is not enabled.

## Sampled visual scope and reproduction

Visual inspection covered main pages **1, 7–8, 106–110, 194 and 281**, and companion pages **1 and 7**, at 108 dpi using individual pages and one bibliography/companion sheet. Native main pages **109–110** were additionally inspected with Poppler at a longest-side resolution of 1440 pixels. The inspected preflight and native sample arrays agree at 108 dpi. No clipping, text/formula overlap or broken glyph was found on those pages. [VISUAL_REVIEW_V54.json](../../deliveries/a2-v54/2cedae961195f97df802aaa81112d95cd32974e1/VISUAL_REVIEW_V54.json) records this scope separately from the automated comparisons. There is no claim of individual visual or mathematical review of all 288 pages.

To reproduce, extract the complete source and build `two_collision.tex` before `main.tex` with the restricted-shell latexmk commands in the local record, or use `tools/build_submission.py` from a checkout of the pinned source. Run `tools/check_revision_v54.py` with and without `-O`. The independent-of-author-code download verifier requires PyMuPDF and accepts `--native`, optional `--local-build`, and optional `--artifact-zip`; it performs no network or repository write and no mathematical-code execution.

No A1 source, unrelated workstream, prior report, default branch, branch protection or collaborator permission was changed. The next referee should assess the strengthened finite-flight proof, the exact charged binary experiment and the principal relative/smooth inverse separately from these operational checks and from the nonbinding editorial recommendation.
