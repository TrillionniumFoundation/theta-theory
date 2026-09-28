# A2 revision 58 — final review ledger

September 15, 2026. This is the complete revision responding to the v57 memorandum. The strengthened proof, preservation checks, native build, published Git objects and sampled visual inspection are separate records, not a mathematical certificate or a journal decision.

## Frozen review and source

| Object | Identity |
|---|---|
| Addressed v57 report head | `e14138660e716daf60471f3b98e8f1d30cb61a34` |
| Actual reviewed v57 source | `e39315c1fbb79ce71d1da91186a0d7e99a5ad8d6` |
| v58 preparation commit | `fcb6b3b5dabe1c0120ae2ad9ce8ba7917b84d307` |
| **Actual compiled v58 source** | **`92a6d946c98e19c33ebff15997c0116ac158b89d`** |
| Manuscript subtree | `39d14581fd018149f2dcce7c306d04ad8e286c0f` |
| Native run / attempt / artifact | `34969789751` / `1` / `10397425264` |
| Retained-products commit | `485f82166b014deeb5f1aa289bdb570af84dbbba` |
| Product-attestation head | `643a526e66f387224a898bfa21fe2a539e44392d` |

Source branch: `revision/a2-v58-uniform-admissible-blocks-2026-09-15`. Products branch: `revision/a2-v58-native-products-34969789751-1`. Final review entry: `revision/a2-v58-review-ready-2026-09-15`, descending from the verified product head with navigation and verification records only. No compiled TeX input or native PDF is changed in the final entry.

## Mathematical revision and reading map

The latest report closes R56-C1 and the anchored-contact wording and identifies no new mandatory core repair in its stated coverage. The present change responds to its optional R57-M3 refinement inside the original signed-contact proof, without adding an unrelated probability section or narrowing any global theorem.

| Revised or retained point | Final location |
|---|---|
| Existing local theorem strengthened by order-uniform admissible block estimates | Theorem 1.1(3), principal p. 3, equation (1.5) |
| Positive-curvature contraction and the scope of the diagonal bound | Principal introduction, p. 4 |
| Uniform matrices/inverses and exponential approach to identity | Proposition 12.9, principal pp. 48–49; full pp. 50–51 |
| Actual smooth pairs with identical lower jets | Equation (12.32), principal p. 49 |
| Factorial coefficient space and radius gain for the diagonal correction only | Equation (12.33), principal p. 49 |
| Complete finite derivative split into diagonal and strictly lower-triangular terms | Equation (12.36) and following paragraph, principal pp. 49–50 |
| Unchanged declared acquisition-theorem application | Corollary 19.9, principal p. 89; full p. 91 |
| Complete acquisition theorem supplying that application | Full Theorem 47.3, p. 194 |

The new proof uses `r_b = c/c_(1-b) < c` and therefore `r_b exp(-gamma) < (1+exp(-2 gamma))/2`. It bounds the highest-degree matrices and inverses uniformly for all degrees at a positive lower hyperbolic margin, without a separate upper curvature-ratio bound. Both corrections to the identity decay exponentially. The actual-smooth conclusion first invokes the existing functional finite-jet factorization, and the coefficient-space conclusion follows from absolute summation. The constants are not uniform as the hyperbolic margin vanishes.

The finite triangular factorization explicitly prevents substituting a bound on the block diagonal for a bound on the complete nonlinear inverse. Lower-jet couplings, smooth remainder constants, extraction of derivatives from densities and analytic continuation remain separate. The coefficient-radius gain belongs to the diagonal correction, not to the full map. The estimates communicated in the v57 memorandum are attributed at the proof, acknowledgment and both bibliographies. Their consequences are not advertised as independent general inversion principles.

The principal architecture, Theorems A/B and the entire geometric, window, differential, acquisition and statistical corpus are retained. The [response](RESPONSE_TO_REFEREE_V58.md), [historical audit](HISTORICAL_DERIVATION_AUDIT_V58.md), [dependency ledger](journal/DEPENDENCY_LEDGER_V58.md) and [primary-record check](LITERATURE_CHECK_V58.md) state the respective reading and attribution scope.

## Complete native products

The [retained delivery](../../deliveries/a2-v58/92a6d946c98e19c33ebff15997c0116ac158b89d/) contains three full PDFs, the complete source archive, raw native logs, source manifests and paired finite diagnostics.

| Product | Pages | Bytes | SHA-256 |
|---|---:|---:|---|
| Principal article | 109 | 1038456 | `4c18b056f70ec13da0e54a8df0c54866a3403465b3928e8d99688c40a5c4aba4` |
| Full technical manuscript | 285 | 2106845 | `3f358af7dd89910b899aeebe096acf13b355daf016e98aeb5bea59ccdf38507f` |
| Companion | 7 | 333367 | `b9390b0975c41bdef488dade494e9d8f06150e191d563e052ad7b556174e1eb1` |
| Complete source archive | — | 2474791 | `80f92b05972b289abe66e91668dab45a0af1d7b5ab01a1fc89c4a791c2309117` |

The outer Actions ZIP is different from the nested source ZIP: 6063342 bytes, SHA-256 `4a3d7c6eaed1f4b927b0a05efe94b675a03c4463c4809da81238100dcfc2a868`, matching GitHub's artifact digest.

All three native builds and the publication job succeeded. The unchanged engine compiles companion, full technical manuscript and principal article in that order from the frozen Git source, with shell escape disabled. Imported companion/full auxiliary files are checked against their producer's source and native products. No old full-manuscript auxiliary file supplies the principal references.

The final native reports contain no unresolved-reference/citation, overfull-box or missing-glyph failure. The principal retains two underfull-vbox notices (badness 2600 and 1057); the full manuscript retains three (1057, 10000, 10000); the companion has none. Local restricted-shell builds additionally emit the expected epstopdf shell-escape-disabled notice. The build is not described as warning-free.

The publication job verified 52 artifact files from the index, pushed and fetched the product branch, checked its committed blobs, committed an attestation, then fetched and checked again. The attestation names the retained-products commit; the later attestation head keeps the same artifact bytes. This verifies content, not signed commits or a hostile compiler. The complete products are Git objects, not only expiring Actions artifacts.

## Preservation and finite diagnostics

All 120 inherited active paths remain in the original three entry graphs; one shared input raises their union to 121. Entry counts are 111 main, 42 principal and one companion, with overlaps. Of the inherited paths, 113 remain byte-identical in place. Seven exact amended-file originals and the v57 native manifest are archived under `history/v57-review-baseline/`.

All 572 inherited statement/proof blocks remain present. Of these, 570 are verbatim; the only two amended blocks are the strengthened Theorem 1.1 and its proof map. The 270 inherited proof blocks include one amended proof map; one proposition/proof pair is added. Counts are per source path, including shared display copies, not independent theorem counts. All old labels survive. Static checks found no duplicate active label or missing reference/citation in any entry.

Five diagnostic families passed under ordinary and optimized Python with identical paired output: `check_revision_v58`, `check_quantized_v46`, `check_adaptive`, `check_revision_v32`, `check_revision_v38`. The new exact controls test 1330 admissible rational blocks at degrees 3–40, both uniform row-sum bounds, exponential identity approach, endpoint/interior multiplicities, fixed-lower-jet algebra and finite-support factorial coefficient norms. Negative controls distinguish inadmissible determinant-one matrices, wrong endpoint multiplicity, the radius gain of a correction rather than the identity part, and growing inverses of abstract triangular maps with identity diagonals. These finite comparisons do not simulate a billiard or prove the general smooth and infinite-flight arguments.

The current dependency map retains eight background/comparison targets and one substantive acquisition-theorem input across 14 literal occurrences. Statement-only imports and misclassification fixtures remain checked. Role declarations result from reading, not from the position of reference tokens, and the tests are not semantic proof certificates.

## Post-download reproduction and actual visual scope

The separate verifier imports no author checking code. It verified the outer digest, all 45 declared build-report evidence entries, all 699 frozen source files and all 121 active identities. It reconstructed the Git manuscript tree from modes and blob hashes, obtaining `39d14581fd018149f2dcce7c306d04ad8e286c0f`, also resolved independently by the GitHub tree endpoint. It found no standalone font files in the source distribution.

Three complete builds from a fresh extraction of the downloaded source succeeded. All 109 principal, 285 full and seven companion pages — **401 pages** — agree with the native PDFs in extracted text and same-renderer 72-dpi RGB arrays. The separately compiled preflight agrees as well. Native and rebuilt PDF byte hashes differ; byte identity and cross-renderer invariance are not claimed. No extracted text span lies outside its page. The author checker was rerun in both Python modes and matches the native output; that is an author-code rerun, not an independently designed mathematical checker.

Direct visual inspection covered principal pp. **3, 4, 48–50** and full p. **51** at 108 dpi. Principal preflight samples were compared with the downloaded native samples; all agree. Native principal p. **49** was additionally opened as a Poppler render with longest side 1440 pixels. The new proof and its transition are legible without observed clipping, overlapping formulas or broken glyphs on these pages. This is sampled layout inspection, not a visual or mathematical review of every delivered page. The companion was rebuilt and compared on all pages but not freshly inspected visually in this round.

`LOCAL_REPRODUCTION_V58.json`, `REBUILD_VERIFICATION_V58.json`, `VISUAL_REVIEW_V58.json` and the portable `verify_delivery_v58.py` are retained in the delivery directory. The verifier requires PyMuPDF and accepts `--native`, `--source-commit`, `--source-tree`, optional `--rebuild`, optional `--preflight`, and optional `--artifact` with its `--artifact-sha256`. It performs no compilation, network request or mathematical-code execution. Rebuild the three TeX entries in dependency order using the restricted-shell commands in the local record; run the author checker with and without `-O` separately.

A1, unrelated papers, past reports, the default branch and repository permissions were not changed. The remaining significance assessment concerns the relative/smooth inverse and its mathematical reach, not the count of preserved files or successful workflow runs.
