# Audit scope, sources, and reproduction — A2 v48

This record accompanies [REFEREE_REPORT.md](REFEREE_REPORT.md). It distinguishes source inspection, mathematical deductions, finite diagnostics, complete compilation, and sampled visual inspection. None of the operational checks certifies a mathematical theorem.

## 1. Frozen objects

Repository: `TrillionniumFoundation/theta-theory`. Reviewed branch: `revision/a2-v48-review-ready-2026-09-14`, frozen at `5babd4cd1515b7f64488d997d89d0860a4eff96c`. The compiled mathematical source is `fe21046e47a89ec3b3df8493f4d885b087e3ad7f`, with source subtree `60d2cc48b3ce645d984724e9aa8ab26014c74522`. These are different identifiers and are not used interchangeably.

Native run 34852676783, attempt 1, artifact 10351522484 was downloaded through the authorized GitHub connector. The downloaded Actions ZIP SHA-256 is `bee6a759c375a030a4b9540e23ec887374e01d336706e89302f781639efeab07`, matching the author ledger. The earlier native run 34850920287 is superseded and was not the final review object.

The GitHub comparison from the compiled source to the review-ready snapshot is ahead by three commits and changes navigation and delivery records, not compiled TeX sources. The independent report branch starts from the pinned review-ready snapshot. No author manuscript, default branch, historical report, branch protection, permission, or unrelated research source is edited by this review.

The preceding report is `reviews/a2-v47-independent-harsh-top4-2026-09-14/REFEREE_REPORT.md`, frozen at `757f2ee4e3bf766d2eb56d972e6d2f621b3fd2a6`. Its actual reviewed mathematical source is `219b39e94b14187561dc3b7e5bdbae49dbd92cc2`, not the v47 workflow-preparation commit.

## 2. Manuscript source index

All relative source paths below have prefix `papers/A2-v17-boundary-information-coarsening/` at the compiled source commit, unless another root is stated. Labels and page numbers were checked against the final native auxiliary file. A path's older revision suffix does not imply an inactive input.

| ID | Source and reading scope |
|---|---|
| S01 | `article/00_structural_introduction_v48.tex`: complete new introduction; Theorem A, p. 4. |
| S02 | `article/23m_differential_rigidity_v48.tex`: all 432 lines; Lemmas 20.1–20.4 and Theorems 20.5–20.6, pp. 89–93. |
| S03 | `main.tex`, the recursive active input graph, and the retained `article/01_introduction_v41.tex` entry: organization and preservation. |
| S04 | `article/23f_single_offset_law_inverse_v42.tex`: four-density inverse, anchor, leading curvature inverse, and fixed-order stability; Theorem 14.1, p. 58. |
| S05 | `article/23a_signed_endpoint_rigidity_v27.tex`: weighted half-line inverse, finite terminal-envelope estimates, smooth finite-jet factorization and contact blocks; Lemmas 13.2–13.5, pp. 52–55, and the surrounding finite-order recursion. |
| S06 | `v4/10_boundary_layers.tex`: half-line action, trace-class amplitude, gluing and relative factorization at the parameter-differentiation interface; in particular lines 90–116 and 185–249. Also the formulation of the relative-law input in `article/01c_geometric_setup_v43.tex`. Not a new certification of every operator theorem. |
| S07 | `article/16_hyperbolic_coordinates.tex`: the mixed-boundary normal-form formulation and the distinction between a physical amplitude and the linear multiplier, at the dependency interface used by the local inverse. |
| S08 | `article/23j_generic_finite_channel_rigidity_v45.tex`: complete selected-channel construction, asymmetry and cochain proof; Theorem 19.3, p. 83; Proposition 19.5, p. 85; Theorem 19.7, p. 86; Proposition 19.8, p. 87. |
| S09 | `article/23c_analytic_continuation_v23.tex` and `article/23k_quantized_law_stability_v46.tex`: qualitative continuation, the finite graph-to-support conversion and the distinction from conditional noisy inversion. This round does not independently recertify every quantitative modulus. |
| S10 | `article/23l_calibrated_histograms_v47.tex`: complete unchanged module, 305 lines; Lemmas 21.7–21.8, Theorem 21.9, Corollary 21.10, pp. 101–104. Its pilot/statistical dependencies retain the preceding review's separate coverage. |
| S11 | `article/25c_analytic_variation_bundles_v25.tex`: the earlier fixed-contact finite-jet bundle and finite positive designs, Section 45, p. 175 onward; compared with the new moving-table kernel theorem. |
| S12 | `RESPONSE_TO_REFEREE_V48.md`, `HISTORICAL_DERIVATION_AUDIT_V48.md`, the archived v47 baseline, `tools/check_revision_v48.py`; repository-root `README.md`, `A2_V48_VERIFICATION_LEDGER.md`; and the native artifact manifests and logs. These are provenance and response records, not substitutes for proof. |

The new introduction's Git blob is `2f2e36d3848dea62154753c58542c3485d7f2889`; the differential section's blob is `5a46865e2e9534f4f30b9c2910a140e68845f734`; the main entry's blob is `d9c7f9f486ad7b3b1800bab4ae2f00b55270c0cf`. The independent artifact checker verifies SHA-256 and Git blob identities for every one of the 105 active source files, not just these three.

The report does not claim a fresh line-by-line proof audit of all inherited LAN, Poisson, deficiency, deconvolution, transfer-operator, auxiliary or companion results. The optional noncircular local strengthening and the circular-lattice control in Section 4 of the report are referee deductions with arguments supplied there, not falsely attributed manuscript claims.

## 3. Primary literature records

These primary records were checked on September 14, 2026. The comparison is targeted, not an exhaustive priority search.

**L1.** D. Finamore and M. Leguil, *A CAT(0)-approach to the marked length spectral rigidity of Sinai billiards*, arXiv:2510.18983v1, submitted October 21, 2025. [Primary record](https://arxiv.org/abs/2510.18983v1). The current record has v1 and concerns enriched marked length data for finite-horizon Sinai billiards. The enriched-spectrum definition and the PDF's printed page 4 were inspected. No reduction to or from the present boundary-law datum is asserted.

**L2.** A. Florio and M. Leguil, *Smooth conjugacy classes of 3D Axiom A flows*, arXiv:2010.04120v5, June 3, 2021. [Versioned primary record](https://arxiv.org/abs/2010.04120v5). The version comment explicitly records the removal of the earlier geometric spectral-rigidity assertion affected by Proposition 3.1; the dynamical conclusions are distinct.

**L3.** J. De Simoi, V. Kaloshin and M. Leguil, *Marked Length Spectral determination of analytic chaotic billiards with axial symmetries*, arXiv:1905.00890v4, August 17, 2022. [Versioned primary record](https://arxiv.org/abs/1905.00890v4). The announced theorem concerns analytic open billiards with non-eclipse, symmetry and genericity assumptions, and marked length data. It is not identified with the endpoint-law inverse.

**L4.** L. N. Trefethen, *Quantifying the ill-conditioning of analytic continuation*, BIT 60 (2020), 901–915, DOI 10.1007/s10543-020-00802-7. [Author publication record](https://people.maths.ox.ac.uk/trefethen/papers.html) and [Oxford institutional record](https://ora.ox.ac.uk/objects/uuid%3A0e4de186-e63c-4ec3-bc1c-4b6af4fe012b). This is context for the distinction between exact analytic uniqueness and conditional stability, not a substitute for the manuscript's internal proof.

## 4. Reproduction

Extract the final Actions artifact into `NATIVE`, then extract its `native-source.zip` into a fresh directory. The nested `source/` directory is denoted `SOURCE` below. Paths are placeholders for local directories, not extra repository branches. The review used Python 3.13.5, SymPy 1.14.0 and PyMuPDF 1.26.7.

Run the author's preservation and finite checks from the extracted source:

```sh
cd SOURCE
python tools/check_revision_v48.py > author-normal.json
python -O tools/check_revision_v48.py > author-optimized.json
cmp author-normal.json author-optimized.json
```

Both runs succeeded with identical output. They report 103 inherited active inputs, 101 identical in place, two archived originals with deterministic editorial amendments, 105 final inputs and 232 inherited proof environments retained. The included finite v47 calibration controls remain active. These counts do not measure correctness or novelty.

Rebuild both complete entries, companion first because its generated auxiliary data are used by the main:

```sh
latexmk -norc -pdf -interaction=nonstopmode -halt-on-error -file-line-error -recorder \
  '-pdflatex=pdflatex -no-shell-escape -recorder %O %S' two_collision.tex
latexmk -norc -pdf -interaction=nonstopmode -halt-on-error -file-line-error -recorder \
  '-pdflatex=pdflatex -no-shell-escape -recorder %O %S' main.tex
```

Both commands completed successfully in this review. From the review directory, run:

```sh
python independent_checks.py > checks-normal.json
python -O independent_checks.py > checks-optimized.json
cmp checks-normal.json checks-optimized.json
python verify_artifact.py --native-root NATIVE --source-root SOURCE \
  --local-build SOURCE > artifact-audit.json
```

The finite diagnostic outputs were identical and passed; the recorded result is [INDEPENDENT_CHECKS.json](INDEPENDENT_CHECKS.json). They test the differentiated density/anchor identities with varying amplitude, moving-cap normalization, geometric-series contact blocks through order 16, harmonic registration, a non-unimodular cochain and the circular-table lattice identities. Negative controls detect a wrong anchor sign, omitted normalization derivative and omitted gain inverse. The script uses explicit exceptions, not assertions disabled by `-O`. Functional cap and synthetic cochain tests are not misrepresented as billiard realizations.

[ARTIFACT_AUDIT.json](ARTIFACT_AUDIT.json) records 34 native evidence files and all 105 active input identities verified. Native product hashes are:

| Product | SHA-256 |
|---|---|
| Main PDF | `6ca3bc8f50a399d574b7912a5c4390a35eabb0020b50578f2a2b026c23e2a6e4` |
| Companion PDF | `b9390b0975c41bdef488dade494e9d8f06150e191d563e052ad7b556174e1eb1` |
| Native source ZIP | `8e6968aa48d0eca3e0844c80bdab57c2c3d1c727be2dfecb4722477df98b06ff` |

Every page of the independently rebuilt 255-page main and seven-page companion matches the native PDF in extracted text and 100-dpi RGB raster arrays using PyMuPDF. The rebuilt PDF byte hashes differ; no byte-identity or second-rendering-engine claim is made. The local final main log retains four underfull boxes, zero overfull boxes and no unresolved-reference/citation warning. The companion has no such layout warnings.

Direct visual inspection covered main pages **4, 89–94** and companion pages **1, 7**. These include Theorem A and the complete new differential section. More pages were rendered or text-searched, but that is not counted as direct visual inspection. All-page automated parity is not all-page human reading, and neither is mathematical certification.
