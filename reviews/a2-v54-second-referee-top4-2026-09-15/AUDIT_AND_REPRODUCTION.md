# Audit ledger — second independent review of A2 v54

September 15, 2026. This ledger accompanies `REFEREE_REPORT.md`. Source verification, proof reading, independent finite diagnostics, complete rebuilding and visual inspection are different activities. Their coverage is not interchangeable.

## 1. Frozen identities and noninterference

| Object | Identity |
|---|---|
| Repository | `TrillionniumFoundation/theta-theory` |
| Review-ready branch | `revision/a2-v54-review-ready-2026-09-15` |
| Review-ready commit | `802cb27e731a3a821903a7308cba9d5da29bbf79` |
| Actual compiled mathematical source | `2cedae961195f97df802aaa81112d95cd32974e1` |
| Manuscript directory | `papers/A2-v17-boundary-information-coarsening` |
| Reconstructed manuscript Git subtree | `407b278984b14e57468e727fb56b0fa4163a7207` |
| Distinct workflow preparation commit | `eb6989f624e7417db92140841710c22719cc1cd2` |
| Native run / attempt / artifact | `34934158178` / `1` / `10382712647` |
| Retained-products / attestation commits | `5f168a195d9f04ba8e6b1aa23dbe9a24eeaac6f2` / `47d64975211909c0d30be9050444cab667545e88` |
| Preceding v53 review | `000ce24f65f8381d2180cbd1f080d3d8470c8157` |
| Preceding v53 mathematical source | `42cc62f230473c34d78af1d06b9ca5c2651ae86d` |
| Existing v54 review, preserved | `1030ca91a96ca1be8ecd0347ecbdac7084cdd8d4` |
| New destination branch | `review/a2-v54-second-referee-top4-2026-09-15` |
| New report directory | `reviews/a2-v54-second-referee-top4-2026-09-15` |

The new branch starts at the pinned review-ready commit, not at the default branch or at the other review. Only this new review directory is to be added. No manuscript revision, original review, A1 file, permission, branch protection, default branch or pull-request state is changed by this review.

The existing v54 review was discovered while checking whether the intended branch name was unused. Its opening disposition and Section 5 were then consulted. Its count-only reductions overlap the independently checked formulas here; the report expressly acknowledges this and does not claim priority or use its conclusion as a proof certificate. The present finite diagnostic and rebuild files are separate records, not copies of its reported outputs.

## 2. Proof-reading coverage and source keys

Paths are relative to the manuscript directory at the compiled-source commit. Line numbers refer to the frozen source, not a later rendered Markdown page.

| Key | Path and line coverage | Fresh mathematical examination |
|---|---|---|
| S1 | `article/00_structural_introduction_v48.tex`, 1–365; `main.tex`, 1–165 | Principal theorem hypotheses, actual observation models, finite-channel versus finite-scalar data, experiment interfaces, abstract, attribution and article architecture. Introductory statements are not treated as substitute proofs. |
| S2 | `article/18g_realized_window_information_v53.tex`, 1–595 | Complete Section 23: normalized expansion, actual geometric family, fixed recording profiles, likelihood regimes, strengthened finite-flight corollary, waiting and cap theorem, all their proofs. |
| S3 | `v4/10_boundary_layers.tex`, 1–386 | Nonlinear half-line construction, trace-class amplitudes, gluing, cofactor/determinant normalization and fixed-offset law. Not a fresh audit of every earlier physical event used by this module. |
| S4 | `article/23a_signed_endpoint_rigidity_v27.tex`, proof-focused reading through the final proof and oriented-intrinsic remark (599 lines) | Weighted/envelope mechanism, actual-smooth finite-remainder factorization, last-jet block, finite-order inverse, tangent bound and analytic propagation. No claimed order-uniform conditioning or fresh certification of all externally referenced earlier lemmas. |
| S5 | `article/23q_support_and_interior_windows_v52.tex`, 1–271 | Complete-support centering versus interior extraction, positive visible window, smooth topology, both geometric-fiber inclusions, projected nuisance/table derivative kernel, fixed-window limit and charge restriction. |
| S6 | `article/23m_differential_rigidity_v48.tex`, proof-focused reading across 1–505 | Forward derivative with moving reference, fixed-order jet derivative, analytic variation, local registration, lattice cochain, infinitesimal kernel, finite scalar coordinates and lower Lipschitz proof. |
| S7 | `article/23n_finite_symmetry_v49.tex`, 1–243 | Finite rotation alternatives, local harmonic lift through actual congruences, finite matching and lattice realization tests, converse and circular comparison. The selected-skeleton existence proof in the separate v45 module was not freshly re-audited in full. |
| S8 | `article/23l_calibrated_histograms_v47.tex`, 1–305 | Complete calibrated-histogram interface: offset sensitivity, internal and outer hard-bin crossings, history-uniform bias, capped acquisition comparison and simultaneous choices. Underlying pilot and full quantized-continuation theorems are dependencies, not newly certified in full. |

The response and historical derivation audit for v54 were also read. The preceding v53 report was used to identify previously closed issues and the attribution of its optional improvements. The exact frozen main source and native outputs were used for the actual current proofs, not the author response alone.

### Blob identities

| Source | Git blob |
|---|---|
| `main.tex` | `ad3d407d9a60fd6b7baeeeaff7c0837b0c13b435` |
| S1 introduction | `ecb4ddb2c13c2bf573a57e7f72d9ebaa57c2e0f1` |
| S2 | `9d4fe6f11d850c9d955f25cf882feec133751f6b` |
| S3 | `892a88e37a24e591fa525013c41910c791e28e73` |
| S4 | `0285c90309b8ab88d1ce1ecf8d492ea6d71f268e` |
| S5 | `ffbaa8674e5cc1fb9645efe43e96841ae7b2ba8d` |
| S6 | `1eb8db48bd184378ebd10be30c033b91edd8f36d` |
| S7 | `3bc39ac137812340b9426e9f2b7457a39d6e7f91` |
| S8 | `70f30ea4fdd3048bdac04ee0d3febcf40591a341` |

`reproduction.json` also records byte hashes and line counts. Main PDF locations for the changed results are Corollary 23.3, pp. 106–108, and Theorem 23.4, pp. 109–110. The unchanged realization and testing result is Theorem 23.2, pp. 104–106.

No statement that all 281 main pages or all older local statistical experiments have been line-by-line certified is made. The seven-page companion was rebuilt and compared, not independently refereed in full.

## 3. Independent source and artifact verification

The authorized workflow-artifact downloader supplied the actual ZIP. Its size is **4,661,563 bytes** and its SHA-256 is

`d7572bce8b3a9131685f9a76cab47b381e60bf99aaf9c7dd4adf0444e5419610`.

This matches the artifact digest obtained separately with the workflow-run-artifacts action for run 34934158178. The direct generic fetch endpoint for artifact metadata was unsupported; the dedicated artifact action succeeded. Local network access was unavailable; repository access and the binary download were performed through the GitHub connector.

The nested native source was extracted separately from the native output directory. `verify_delivery.py` imports only the Python standard library and does not execute any author code. It checks all **626** frozen source file lengths, SHA-256 hashes and Git blob identities, reconstructs Git trees using the recorded modes and Git tree ordering, and obtains the pinned manuscript subtree. It also verifies the nested source manifest, all **34** build-report evidence files and both PDF products.

The active manifest contains **110 main inputs and one companion input**, 111 in total. Against the archived v53 active manifest, the active path sets agree, **106 main inputs and the one companion input are unchanged in place**, and four altered main-input originals match their archived bytes. The four files are the main entry, structural introduction, Section 23 module, and bibliography. This is an independent file-level audit against the archived baseline, not an independent rerun of the author's 542-of-544 statement/proof-block audit. No author checker was executed for this memorandum.

The verifier was run with ordinary Python and `-O`; outputs agree byte-for-byte. Hashes verify content identity, not a trusted compiler, a cryptographic author signature, or theorem validity.

## 4. Complete independent rebuild and comparisons

From a fresh copy of the extracted source, the companion was compiled before the main. Both commands completed successfully:

```sh
latexmk -norc -pdf -interaction=nonstopmode -halt-on-error -file-line-error -recorder '-pdflatex=pdflatex -no-shell-escape -recorder %O %S' two_collision.tex
latexmk -norc -pdf -interaction=nonstopmode -halt-on-error -file-line-error -recorder '-pdflatex=pdflatex -no-shell-escape -recorder %O %S' main.tex
```

All **281 main pages and seven companion pages** match their native counterparts in extracted text and in the raw RGB arrays rendered at 72 dpi by the same PyMuPDF renderer. No text or pixel mismatch page was found. The renderer version tuple was `('1.26.7', '1.26.12', None)`.

| Product | Native SHA-256 | Rebuilt SHA-256 |
|---|---|---|
| Main | `393f471cc623d446fdec58b3c05fabc5f3bfc4b620f9194950523dfe601d0552` | `8ffad61a2879ce74d34fca759e9c588de5d8da3e27abd45d620f127efcf5ea05` |
| Companion | `b9390b0975c41bdef488dade494e9d8f06150e191d563e052ad7b556174e1eb1` | `a7d42357ce51290ee495ab922445dbbae1d7380a7e7d6a073e95444084061d10` |

The differing byte hashes are stated explicitly. No byte-identical PDF reproduction is claimed. Final-log scans retained four main underfull vertical-box notices, of badness 1057, 10000, 10000 and 10000. No overfull box, undefined reference/citation or missing-glyph diagnostic was found in the scanned categories. The companion had no corresponding warning. This is not a claim that every possible engine/package warning was absent.

Direct visual inspection was confined to native main pages **107, 109 and 110**, at 108 dpi. Those pages showed no clipping or formula overlap. Other sample images were rendered but are not counted as visually reviewed. All-page automated pixel comparison is not all-page visual or mathematical inspection. No OCR was used.

Native PDFs and source already remain in the manuscript delivery. They are not duplicated by this review. Local rebuild transcript hashes are in `reproduction.json`; the transcripts and rendered pages are not added to the repository. No font files are distributed.

## 5. Independent finite controls and reproduction commands

`independent_checks.py` imports no author code. Its ordinary and optimized outputs are identical, with SHA-256

`37165ca35176a7672bde9cf0bf6194d5c8f8a08d8a8a8a3e1995dd2611a59e63`.

Thirty exact rational capped laws use unequal marks to check normalization, the common-cemetery sandwich, the exact censored-count likelihood threshold, the full/count risk comparison, the simulation-kernel error and the expected capped charge. Further controls verify the window interaction integral and leading Hellinger coefficient, the actual quadratic curvature contrast, positive-floor quadratic Hellinger order, affinity tensorization, and a joint scaling which satisfies the new but not the old product condition. Floating finite-cap examples approach the stated limiting risks.

Negative controls remove the positive density floor and take an excessively large cap for the any-acceptance statistic. They detect invalid extensions of the arguments; the manuscript does not make those invalid extensions. The checks use explicit guards rather than optimization-sensitive assertions. Finite distribution controls are not a simulation or proof of the nonlinear billiard realization.

After extracting the native artifact to `NATIVE_DIR` and its nested source ZIP to a directory with `SOURCE_DIR=.../source` and sibling `SOURCE_MANIFEST.json`, run:

```sh
python verify_delivery.py NATIVE_DIR SOURCE_DIR > delivery-normal.json
python -O verify_delivery.py NATIVE_DIR SOURCE_DIR > delivery-optimized.json
cmp delivery-normal.json delivery-optimized.json
python independent_checks.py > checks-normal.json
python -O independent_checks.py > checks-optimized.json
cmp checks-normal.json checks-optimized.json
```

The deposited `reproduction.json` records the identities, verifier results, rebuild results, source hashes, executed command templates, visual scope and limitations. `independent_checks.json` is the actual normal-mode output, not hand-constructed expected output.

## 6. Primary literature scope

On September 15, 2026 the official arXiv records for `0903.0702v1`, `2510.18983v1`, `1905.00890v4` and `2010.04120v5` were checked. The Finamore–Leguil primary PDF was additionally inspected at its Theorem A on printed p. 5. These checks support the observation-model and version-specific comparisons in the report. They do not constitute an exhaustive literature review, a proof of novelty, or a complete verification of the cited external proofs.

The report's editorial recommendation is distinct from each verification result above. Correctly closed technical points remain closed; adding another elementary consequence is not made a condition of mathematical closure.
