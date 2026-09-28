# Independent A2 v64 audit ledger

Review date: September 16, 2026. This ledger accompanies `REFEREE_REPORT.md`; it is not a proof certificate or commissioned journal decision.

## 1. Frozen provenance

Repository: `TrillionniumFoundation/theta-theory`.

| Item | Identity |
|---|---|
| Actual compiled source | `ee2380ceb76808dd2969d6b5faaa180737020eff` |
| Source repository tree | `576dd214e3f826d6dd475f17975b62f8f2970e4a` |
| Independently reconstructed manuscript subtree | `513b2538cea797cb340e02e69f45543f8b4e9571` |
| Native-products head / review parent | `60c5a25a028cafac98d6f40dbc272effc937b29a` |
| Products repository tree | `729975d4664acc9e0e3e19aad478b5b677bfcf37` |
| Native workflow / attempt / artifact | `35055120579` / `1` / `10429927974` |
| Workflow preparation head, not compiled source | `b16c81f48829b33ba0d8c88458eba7afbd242977` |
| Previous review | `493196e4f6f1d9a46c062df0e3669c3ca26c4fcc` |
| Previous mathematical source | `f5517519440b897707ddc60deeafba19e86bb5a5` |

The native artifact SHA-256 is `5d77b2174e56fd5021c0384f4b9811add1b7ba79b2f975ad8ce2678f65b57aa6`. The frozen `native-source.zip` SHA-256 is `18c017f35d30eb6792a27ba8ed8b0ba8011937598d5a1c470168397c216ee720`.

The available v64 refs at the inspection snapshot were the source branch `revision/a2-v64-referee-response-2026-09-16` and products branch `revision/a2-v64-native-products-35055120579-1`. A separately named review-ready ref was not listed. The review is based on the completed native products, not a fictitious review-ready layer. The authenticated source-to-products GitHub comparison found two delivery commits, with no alteration of compiled mathematical inputs. The new module was also fetched at the immutable source; its Git blob `35a9f495313d342f710995be42fafb19eba91160` matches the archive.

The verifier reconstructs the manuscript subtree, not the entire repository tree. Repository-tree values above come from GitHub commit records. Matching hashes do not authenticate authorship or prove mathematics.

## 2. Mathematical and literature coverage

The complete 549-line new module `article/10a_periodic_itinerary_relative_v64.tex` and new mechanism overview were examined. The review follows all six statements: geometric oblique Jacobi coefficients and persistence; exact chronological transfer/cofactor normalization; finite and half-line Green estimates, nonlinear gluing and relative determinants; connected transmission and scalar stable coordinates; restored physical endpoint momenta and phase-volume normalization; and the three-disk realization and normal specialization. Source-line and printed-page locators are given in S1–S7 of the report.

Current framing, the response, cover letter, historical audit and dependency declaration were checked against that mathematical scope. The inherited v63 ceiling correction remains closed. The complete finite-experiment and position-pilot modules are byte-identical, but their retention is not a fresh proof audit.

Not freshly certified in their entirety: the earlier finite-chain/full-phase prerequisites, the complete v59 Banach-space inverse, v60 continuation construction, all global matching/lattice and differential proofs, the full calibration/statistical catalogue, and the companion. No line-by-line certification of all 448 delivered pages is claimed.

The targeted new primary-source checks concern Bolotin–Treschev's discrete Hill formula and the periodic-word homoclinic asymptotics of Bálint–De Simoi–Kaloshin–Leguil. They distinguish cyclic from Dirichlet determinants and marked-length data from controlled endpoint laws. They do not establish redundancy, first priority, or an information ordering. The Hill-formula theorem/orientation page was viewed by PDF screenshot. The second paper's parsed PDF text was read; screenshot attempts failed, so successful image inspection of that external PDF is not claimed. Retained spectral comparisons were not all re-audited as full external proofs.

## 3. Independent delivery and baseline checks

`verify_delivery.py` is reused from the preceding independent review. It imports no author checker. It verifies lengths, SHA-256 values and Git blob identities, reconstructs a Git subtree using recorded modes, checks active-input manifests and native evidence, and optionally rebuilds and compares the complete PDFs.

Actual verification: **800 frozen source files**, **129 distinct active inputs**, **45 evidence entries**. The per-entry active counts are 118 main, 50 principal and one companion; shared inputs explain the smaller union.

`compare_baseline.py` is adapted to the v63 baseline and verifies both frozen manifests. It found all **784 inherited paths retained**, **779 unchanged**, and five modified paths with exact originals under `history/v63-review-baseline/`. All 127 inherited active paths remain; the two new shared v64 modules make 129. The complete finite-experiment module, its five statement bodies, and the complete position pilot are unchanged. This is a byte/mode and syntactic comparison, not a semantic theorem census.

All three entries were rebuilt from a clean copy of the frozen manuscript, regenerating auxiliary files in companion/full/principal order, with shell escape disabled. All **448 pages** match the native PDFs in extracted text and same-renderer 72-dpi RGB arrays. PDF bytes differ. The final logs contain three full-manuscript and two principal underfull notices, none in the companion. No undefined-reference/citation, missing-character, overfull-box or LaTeX-error pattern was found. Exact commands and PDF hashes are retained in `AUDIT_RESULTS.json`.

Actual visual inspection covered principal pages **27, 30, 31 and 32**, rendered at **108 dpi**. No clipping or unreadable formula was observed on those pages. Other generated images are not counted as inspected. All-page computational comparison is not all-page visual inspection.

The author's own preservation/mathematical checker was not rerun. Verifying its retained output's hash does not amount to rerunning it or endorsing its mathematical claims.

## 4. Independent mathematical diagnostics

`independent_checks.py` uses Python, NumPy and SciPy, imports no author code, and uses explicit checks rather than removable assertions. It independently derives edge gradients/Hessians from disk parametrizations and solves finite stationary chains. Its exact rational calculations compute the Dirichlet determinant by continuants separately from transfer multiplication.

The executed checks comprise 288 exact transfer/continuant identities, 18 phase-trace families, 288 endpoint-half-mass negative controls, 72 noncommuting product-order controls, 72 physical edge-Hessian/momentum cases, 24 two-ended configurations at 6/12/18/24 flights compared to 48-flight proxies, 24 finite stable-return amplitude identities, and 96 restored-gauge negative controls. Both equilateral and scalene three-disk geometries satisfy the tested reflection, separation and third-disk clearance conditions.

The largest 24-flight relative factorization discrepancy against the finite proxy is `2.842170943040401e-14`; the largest stable-return discrepancy is `1.7319479184152442e-14`; the largest recorded stationarity residual is `9.992007221626409e-16`. These are floating-point finite-chain diagnostics, not certified error bounds to an infinite orbit. Periodic translated obstacles are handled in the manuscript's geometric argument, not exhaustively enumerated by this local diagnostic.

Normal and optimized runs emit byte-identical full JSON in this environment. Its SHA-256 is `e2c51c672f6df9743e3eabf7fdeddd3859a5a13dde1098eb26d1c7c5e009d404`. Floating-point last digits and output hashes may differ on another numerical toolchain. The full per-configuration output is in the accompanying audit archive; the committed results summarize it.

These tests do not prove arbitrary-order smooth/family estimates, trace-class convergence, analytic inversion, a global geometric inverse, or statistical rates. Negative controls test deliberately incorrect formulas, not the formulas actually printed.

## 5. Reproduction

Requirements: Python 3, NumPy, SciPy, PyMuPDF, and a TeX installation with `latexmk` and the manuscript's packages. Obtain native workflow artifacts 10429927974 (current) and 10428569064 (baseline). Extract the current artifact to `$WORK/artifact/`, then extract its `native-source.zip` to `$WORK/source/`, yielding `source/SOURCE_MANIFEST.json` and `source/source/`. Start with no existing `$WORK/rebuild/` directory.

From this review directory:

```sh
python verify_delivery.py "$WORK"
python verify_delivery.py "$WORK" --build two_collision
python verify_delivery.py "$WORK" --build main
python verify_delivery.py "$WORK" --build rigidity
python verify_delivery.py "$WORK" --compare
python compare_baseline.py /path/to/a2-v63-native-products.zip /path/to/a2-v64-native-products.zip > SOURCE_DIFF.json
python independent_checks.py > INDEPENDENT_CHECKS.json
python -O independent_checks.py > INDEPENDENT_CHECKS_OPTIMIZED.json
cmp INDEPENDENT_CHECKS.json INDEPENDENT_CHECKS_OPTIMIZED.json
```

The verifier writes `REPRODUCTION_RESULTS.json` and retained fresh-build outputs in the work directory. It does not download a moving branch, make network requests, or treat author-supplied checks as independent proof verification. Source/evidence manifests remain available in the pinned native delivery.

## 6. Review-only changes

The review branch starts at the pinned products head. The only intended additions are the report, this ledger, results, and three reproducibility scripts under `reviews/a2-v64-independent-harsh-top4-2026-09-16/`. Manuscript source, historical reviews, native deliveries, default-branch refs and permissions are not changed. No PR approval, merge, commissioned journal decision or acceptance certificate is implied.
