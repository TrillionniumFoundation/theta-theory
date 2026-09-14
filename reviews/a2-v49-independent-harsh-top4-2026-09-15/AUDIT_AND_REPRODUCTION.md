# Audit trail and reproduction — A2 v49 independent review

This record accompanies `REFEREE_REPORT.md`, dated September 15, 2026. It separates evidence acquisition, fresh mathematical coverage, finite diagnostics, build reproduction and sampled visual inspection. None is represented as certification of the entire manuscript.

## Frozen objects

Repository: `TrillionniumFoundation/theta-theory`. The latest revision branches were searched in two pages, including author, native-product and review-ready variants. The selected complete latest delivery was `revision/a2-v49-review-ready-2026-09-14`, snapshot `c1cc5b54811d0886d68c189a87c3972506bc3d6d`. Its actual mathematical source is `a003c1c69585f09f0b8fcc9fe03eb330cd6d57b7`, not the workflow-preparation commit `f4211c6bc149bb8818f4db52fadbd87822a88971`.

The authorized GitHub connector downloaded Actions artifact `10355118804` from run `34862659773`, attempt 1. The archive contains both complete PDFs and `native-source.zip`; the latter contains 551 frozen source files. The compiled source-to-ready comparison is three commits ahead and changes delivery/navigation records, not the mathematical TeX source. The delivered-product directory at the review-ready snapshot has Git tree `a70bf6a0994de5ee2318cfe3cc465f7133255f92`.

The preceding v48 report was fetched from review head `a512f70ca77d711bd6c9ee61988f1e8dd4dba790`; it reviewed mathematical source `fe21046e47a89ec3b3df8493f4d885b087e3ad7f`. Its continuation through the final disposition was also read, rather than relying on the truncated initial tool response. The v49 response and historical audit were checked against the active sources, not used as proof substitutes.

## Source index

Unless stated otherwise, paths below are relative to `papers/A2-v17-boundary-information-coarsening/` at the pinned mathematical source. The directory name is historical. Source line numbers are one-based. Git blob identities were computed from the downloaded bytes and checked in the manifest verification.

| ID | Source and fresh coverage | Git blob SHA |
|---|---|---|
| S01 | `article/00_structural_introduction_v48.tex`, complete 219 lines; especially Theorem A, lines 27–115, main p. 4. | `80f03a17f249c93ae58cc2abc036d25edb79c445` |
| S02 | `article/23n_finite_symmetry_v49.tex`, complete 243 lines, main pp. 78–81. Congruences 14–48; local branch 50–85; finite fiber 89–182; circular control 192–243. | `3bc39ac137812340b9426e9f2b7457a39d6e7f91` |
| S03 | `article/23m_differential_rigidity_v48.tex`, complete 505 lines, main pp. 81–87. Forward regularity 60–180; density/jet inverse 184–240; analytic variation 242–274; registration 278–377; kernel 379–421; coordinates 425–505. | `1eb8db48bd184378ebd10be30c033b91edd8f36d` |
| S04 | `article/23f_single_offset_law_inverse_v42.tex`, density cancellation, anchor and finite-order interface, lines 1–174, within Section 13, pp. 47–54. Not a fresh audit of every later finite-flight consequence. | `aea44fc8ed3273174a225b143d3fdf5b5c9b5a19` |
| S05 | `article/23a_signed_endpoint_rigidity_v27.tex`, weighted inverse, envelope, functional remainder and last-jet block, lines 154–599, within Section 12, pp. 40–47. | `0285c90309b8ab88d1ce1ecf8d492ea6d71f268e` |
| S06 | `article/23c_analytic_continuation_v23.tex`, complete registered-germ argument, together with the distinct support-variation argument in S03. | `62dff1c3eb8d55816756a386a6005bebe446d1c6` |
| S07 | `v4/10_boundary_layers.tex`, half-line amplitude, relative gluing and trace-series interface, especially lines 35–290; Section 7, pp. 15–20. Review scope is the interface used by S03, not certification of every physical-law estimate. | `892a88e37a24e591fa525013c41910c791e28e73` |
| S08 | `article/23j_generic_finite_channel_rigidity_v45.tex`, clear-connection descent and skeleton selection, lines 1–175; Section 18, pp. 71–78. The complete new cochain proof is audited in S02/S03. | `18e7e152e6296716232cd289570cfb7f4642712d` |
| S09 | `article/23k_quantized_law_stability_v46.tex`, quantified-class hypotheses and finite-order interface, lines 1–220; source preservation checked for the complete module. Not a new end-to-end proof audit of its statistical consequences. | `6f507c272f9f69b996872926141aed5df984655b` |
| S10 | `article/23l_calibrated_histograms_v47.tex`, hypothesis boundary and offset/cell interface, together with the preceding report's disposition; complete module verified unchanged. Now results 38.7–38.10. No claim of re-proving the entire pilot theorem in this round. | `70f30ea4fdd3048bdac04ee0d3febcf40591a341` |

S11 comprises `main.tex`, `RESPONSE_TO_REFEREE_V49.md`, `HISTORICAL_DERIVATION_AUDIT_V49.md`, the current reference/acknowledgment text, root `README.md`, and `REVIEW_READY_V49.md`. The last two navigation files are read at the review-ready snapshot. The compiled catalogue is in Appendix A.1 starting at main p. 173. S12 comprises the complete native artifact, both source manifests, the native build report, author preservation controls, the GitHub source-to-ready comparison and published delivery-tree metadata, and the independent reproduction records in this directory.

## Primary literature checked

These are targeted comparisons, not an exhaustive priority audit. The records were accessed during this review; version histories and the correction notice, not search-result snippets alone, were inspected. No conclusion that the observation maps are equivalent was drawn.

**L1.** D. Finamore and M. Leguil, *A CAT(0)-approach to the marked length spectral rigidity of Sinai billiards*, arXiv:2510.18983. The current record lists v1, October 21, 2025. The abstract and introductory theorem context concern an enriched marked length spectrum for finite-horizon Sinai billiards. The primary PDF was also viewed by web screenshots on its first and third pages. Primary record: `https://arxiv.org/abs/2510.18983`.

**L2.** J. De Simoi, V. Kaloshin and M. Leguil, *Marked Length Spectral determination of analytic chaotic billiards with axial symmetries*, arXiv:1905.00890. The current record lists v4, August 17, 2022; the analytic open-billiard setting has the stated symmetry/genericity and non-eclipse hypotheses. Journal DOI: `10.1007/s00222-023-01191-8`. Primary record: `https://arxiv.org/abs/1905.00890`.

**L3.** A. Florio and M. Leguil, *Smooth conjugacy classes of 3D Axiom A flows*, arXiv:2010.04120v5, June 3, 2021. The version record explicitly removes an earlier geometric spectral-rigidity assertion affected by an error while retaining the dynamical conjugacy results. Primary record: `https://arxiv.org/abs/2010.04120v5`.

**L4.** L. N. Trefethen, *Quantifying the ill-conditioning of analytic continuation*, BIT Numerical Mathematics 60 (2020), 901–915. Publisher record and DOI: `10.1007/s10543-020-00802-7`. Used only to distinguish qualitative analytic uniqueness from quantitative stable continuation, not as a purported contradiction to the kernel theorem. Primary record: `https://link.springer.com/article/10.1007/s10543-020-00802-7`.

## Independent reproduction performed

The full artifact and source ZIP were extracted locally. All 551 source entries were checked for length, SHA-256 and Git blob hash against the frozen manifest. The union of the two active source graphs contains 106 distinct files; their active-manifest hashes were checked. The two native PDFs and source ZIP match their recorded SHA-256 values and the following published Git blobs:

| Product | Published Git blob | SHA-256 |
|---|---|---|
| Main PDF | `4900f50528b68d3a3bca6d6c577f9891d37d0170` | `1e074789890d453072412ced9b34dba5a5b0bba204f49f6d5b44c71947e58c36` |
| Companion PDF | `dae9697f40bcac775d7dd6aa26144af0181adc75` | `b9390b0975c41bdef488dade494e9d8f06150e191d563e052ad7b556174e1eb1` |
| Source ZIP | `727da9834157e6f5f13ae70fe24c7c5e497855ce` | `4d3af0129a17f7194d97310f755e95a6796ed67d9a2d1a87777602b75d14675d` |

In the extracted `source/` directory, the complete entries were built, companion first, with:

```sh
latexmk -norc -pdf -interaction=nonstopmode -halt-on-error -file-line-error -recorder \
  '-pdflatex=pdflatex -no-shell-escape -recorder %O %S' two_collision.tex
latexmk -norc -pdf -interaction=nonstopmode -halt-on-error -file-line-error -recorder \
  '-pdflatex=pdflatex -no-shell-escape -recorder %O %S' main.tex
python tools/check_revision_v49.py > author-check-normal.json
python -O tools/check_revision_v49.py > author-check-optimized.json
cmp author-check-normal.json author-check-optimized.json
```

Both builds succeeded and the paired preservation results agree. The author control verifies 105 inherited active inputs, 100 unchanged in place, exact archives of the five amended originals, preservation of the inherited labels and 239 combined proof environments, and addition of four proof environments. These syntactic checks do not decide mathematical correctness.

PyMuPDF 1.26.7 compared corresponding pages using `page.get_text()` and `page.get_pixmap(matrix=fitz.Matrix(1,1), alpha=False)`. Dimensions and complete RGB byte arrays were compared on all 259 main pages and all seven companion pages. There were no text or pixel mismatches. The local rebuilt PDF hashes differ from the native ones; the hashes and warnings are recorded in `REPRODUCTION_RESULTS.json`.

Sampled visual inspection, using locally rendered images, covered main pages 4, 79, 80, 82, 86 and 173 and companion pages 1 and 7. The samples were legible without observed clipping. Additional pages were rendered but are not counted as visually inspected. The three main underfull-vbox warnings and the intentional shell-escape-disabled epstopdf warnings are disclosed rather than suppressed. The full-page parity check does not imply all-page visual or mathematical reading.

## Independent finite controls and their limits

From this review directory:

```sh
python independent_checks.py > checks-normal.json
python -O independent_checks.py > checks-optimized.json
cmp checks-normal.json checks-optimized.json
```

Requires SymPy; the executed version was 1.14.0. Both runs passed with identical output, retained as `independent_checks.json`. The code uses explicit exceptions so that `-O` cannot remove the checks.

The controls test the C4 noncircular two-branch example, curvature and clearance inequalities, determinant-sign filtering, a noncommuting three-by-three moving-reference derivative, destruction of a base half-turn symmetry, four-density nuisance cancellation and scalar-anchor differentiation, and a three-obstacle cochain with determinant-six gain matrix. Negative controls detect omitting the orientation filter, omitting the Green-operator derivative, changing the anchor sign, and omitting the integer gain inverse.

The exact all-lattice separation/clearance and two-branch completeness arguments are printed in Section 4 of the report. The script checks their explicit identities and inequalities; it is not a sampled substitute for those geometric arguments. Its finite matrix check is not an infinite-operator certificate. It does not reconstruct an arbitrary table, simulate the full billiard acquisition protocol, or certify the unreviewed statistical results.

## Mutation scope

The new review branch starts from the pinned review-ready snapshot. Only a new review directory is added. The author revision branches, main manuscript, companion, existing reports, A1 workstream, default branch, branch protections and repository permissions are not changed by this review. The recommendation is an author-requested referee-style assessment, not an actual editorial decision.
