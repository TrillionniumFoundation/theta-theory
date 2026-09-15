# Audit ledger and independent reproduction — A2 v55

**Date:** September 15, 2026.  
**Purpose:** evidence for the accompanying author-requested, AI-assisted referee-style report. This ledger distinguishes source identity, mathematical reading, finite diagnostics, rebuilding, and visual inspection. None is substituted for the others.

## 1. Frozen objects and version selection

| Object | Identity |
|---|---|
| Repository | `TrillionniumFoundation/theta-theory` |
| Reviewed revision | A2 v55 |
| Reviewed ready branch | `revision/a2-v55-review-ready-2026-09-15` |
| Reviewed ready head | `dfc6dea6d361a24223e481048889e34987491466` |
| Ready-head repository tree | `613d71698a8aa98d1b5f06c157af8d16b11d528f` |
| Actual compiled mathematical source | `3903f5b8a5ffb0d0a69065b1d303c247c06ebf69` |
| Active manuscript directory | `papers/A2-v17-boundary-information-coarsening` |
| Reconstructed manuscript subtree | `8ff45d47f7dd78bc0c0d4ae284dde147a47d87e9` |
| Author branch | `revision/a2-v55-stopped-record-reduction-2026-09-15` |
| Native workflow run / attempt | `34943642385` / `1` |
| Downloaded native artifact | `10385962782` |
| Native products branch | `revision/a2-v55-native-products-34943642385-1` |
| Products-attestation head | `f9613aed7b11e5f94e0d22bbc4e399e4393f8a12` |
| Workflow-preparation commit, not mathematical source | `27956302dd20baf623f2881502be7d68ee29e72d` |
| Prior first v54 report head | `1030ca91a96ca1be8ecd0347ecbdac7084cdd8d4` |
| Prior second v54 report head | `67250d08714acf76274e82158f107246f0de7eee` |
| Mathematical source reviewed by both v54 reports | `2cedae961195f97df802aaa81112d95cd32974e1` |

The revision-branch inventory was paginated, and the current v55 README and actual entry files were fetched through the connected GitHub API. A subsequent search found the three v55 author/products/ready branches and no v56 branch; no v55 review branch of this name existed at that check. This selects a frozen object for review, not a claim that branches cannot change later.

The GitHub comparison from the compiled source to the ready head is three commits ahead. Its changed paths are the repository entry, delivery/evidence files, and `REVIEW_READY_V55.md`; it does not change an active compiled TeX input. No default-branch A1 manuscript was substituted for the current A2.

## 2. Mathematical reading coverage

Paths below are relative to the active manuscript directory at the compiled source. Page labels refer to the downloaded main PDF and its native auxiliary labels, not to a newly renumbered draft.

| Source or interface | What was examined | Limit of the claim |
|---|---|---|
| `main.tex`; `article/00_structural_introduction_v48.tex` | Complete entry, principal theorem statements and proof map, stated observations, revised stopped-record interpretation, current literature distinctions | Not a proof of every theorem named in the introduction |
| `RESPONSE_TO_REFEREE_V55.md`; both v54 reports | Current point-by-point response and the prior recommendations/technical dispositions relevant to it | Prior reviewers' findings are not treated as fresh proof certificates |
| `article/18g_realized_window_information_v53.tex` | Complete 747-line current Section 23: actual noncircular realization, fixed recording profiles, expansion constants, critical and attained testing scales, Corollary 23.3, all five clauses and full proof of Theorem 23.4 | Fresh principal focus; finite computations do not replace limiting arguments |
| `v4/10_boundary_layers.tex` | Weighted half-line construction, localized perturbations, cofactor normalization, trace-norm and determinant comparisons, fixed-offset law and sublevel integration; Theorems 7.2–7.3 start on pp. 19 and 21 | Selected core analytical audit, not a line-by-line re-certification of every supporting estimate in every older module |
| `article/23a_signed_endpoint_rigidity_v27.tex` | Actual-smooth finite-jet factorization, finite terminal cancellation, functional regularity requirements, signed last-jet block and finite-order interpretation; Lemma 12.4 starts on p. 46 | No uniform infinite-order inverse bound is inferred; not a complete re-audit of all surrounding finite-flight statements |
| `article/23q_support_and_interior_windows_v52.tex` | Interior origin lines, anchored interaction extraction, smooth local extension, exact-fiber inclusions, and the stated nuisance/visibility restrictions | No total-variation-to-smooth inverse or unknown-window calibration is certified |
| `article/23j_generic_finite_channel_rigidity_v45.tex` | Clear-pair descending path construction, marked spanning-tree/two-gain selection, local persistence and selected-channel scope; Theorem 19.3 starts on p. 84 | Not a new exhaustive audit of every generic-asymmetry and realization statement in that file |
| `article/23n_finite_symmetry_v49.tex` | Finite rotation groups, local nonzero-harmonic alignment, incidence enumeration, actual gain-matrix inversion, candidate compatibility, both fiber inclusions, and circular comparison; Theorem 20.3 starts on p. 90 | Does not assume finite symmetry persists under a variation; does not numerically decide arbitrary analytic-image equalities |
| `article/23m_differential_rigidity_v48.tex` | Common-strip variation, moving reference and cap normalizer derivatives, fixed-order contact kernel, analytic propagation, local alignment, lattice derivative, finite scalar coordinates; Theorems 21.5–21.6 start on p. 99 | Finite-dimensional scalar-coordinate conclusion not promoted to the whole analytic class |

### Material not freshly certified in full

The older adaptive/LAN/Poisson/position/count experiment catalogue, the complete quantized and calibrated-histogram reconstruction theory, all pilot bounds, every full-phase event construction, every auxiliary compendium proof, the complete two-table example, and the companion's mathematics were not all freshly audited line by line. The report discusses the richer acquisition sensor only at the scope stated in the current introduction/response. The build covers their inclusion, not their mathematical correctness.

The author response reports 111 inherited active inputs, 107 byte-identical inherited inputs in place, and 544 of 546 inherited statement/proof blocks verbatim with the other two expanded by insertions. This review independently verifies the current 111 active inputs and full frozen tree. It does **not** present the author's historical block-count checker as a new independent block-by-block preservation proof.

## 3. Independent finite checks

`check_stopped_experiment.py` was written for this review and imports no author checker. Its finite-law calculations use `fractions.Fraction`, with explicit exceptions rather than removable Python assertions. The log-threshold expression is numerically compared only away from floating-point ties; ties themselves and either tie decision are checked by exact rational likelihoods.

The grid uses all distinct interior rational probabilities with denominators 3, 4, 5, and 7, every ordered pair with `p_1<p_0`, caps 1, 2, 3, 7, and 12, and all ordered pairs of four two-point mark distributions. It checks 8,400 finite marked laws. Checks include probability normalization; monotone count thresholds; exact count and full risks; the cemetery decision; the exact count simulation error; the half-factor risk bound; both displayed reverse simulation constructions; stopped charges; count-charge preservation; and cases where bit simulation changes charge.

The output records 31 count-tie cases, 5,924 strict finite mark improvements, and 6,720 changed expected charges for the specified bit kernel. The case digest is `2a50a99204d5a621cdb8a39670b8c1d5efd9db1eb07ada2eaf0623c0f856143f`. The script additionally checks exact Section 23 information constants and nine algebraic signed-jet determinant controls. The large-cap floating-point sequences are explicitly illustrations, not simulated billiard trajectories or proofs of a limiting theorem.

Run:

```sh
python check_stopped_experiment.py > checks-normal.json
python -O check_stopped_experiment.py > checks-optimized.json
cmp checks-normal.json checks-optimized.json
```

Both runs were executed and their outputs were byte-identical. `INDEPENDENT_CHECKS.json` retains that output. The script's lower-bound count of 100,800 checks counts only twelve finite-law requirements per marked case; further threshold and algebraic checks are additional. This bookkeeping is not a measure of mathematical depth.

The disjoint-mark finite control in report Section 4 is exact probability algebra. It is not asserted to belong to the actual shrinking-window table family, for which the two mark laws approach one another.

## 4. Artifact extraction, hashes, and full rebuild

The connected GitHub action downloaded artifact `10385962782` to a local ZIP. That artifact was extracted; its `native-source.zip` was separately extracted. The latter contains the manifest plus the 640-file `source/` tree. The rebuild used a separate working copy of that source, not the author's existing generated files as an allegedly new compilation.

`verify_delivery.py` independently:

1. Checks each of the 640 frozen source files against its byte length, SHA-256, and Git blob hash.
2. Reconstructs the Git subtree recursively, including Git directory sort semantics and file modes, and compares it to the declared source subtree.
3. Checks all 111 distinct active input hashes from the active manifest.
4. Checks byte lengths and hashes of 34 native evidence files listed in the build report.
5. Compares the complete rebuilt PDFs against the native PDFs, page by page, using extracted text and a common renderer at 72-dpi RGB.

The checker verifies the downloaded content against its manifests and reconstructs its content identity; the GitHub pinned entry/source reads and source-to-ready comparison establish the reviewed repository context. This should not be described as a cryptographic proof of mathematical correctness or of an unsigned author's identity.

The two complete entries were rebuilt with shell escape disabled, using the following command in the separate source working directory, once for each entry:

```sh
latexmk -norc -pdf -interaction=nonstopmode -halt-on-error \
  -file-line-error -recorder \
  '-pdflatex=pdflatex -no-shell-escape -recorder %O %S' two_collision.tex
latexmk -norc -pdf -interaction=nonstopmode -halt-on-error \
  -file-line-error -recorder \
  '-pdflatex=pdflatex -no-shell-escape -recorder %O %S' main.tex
```

Both commands completed successfully. The verified comparisons are:

| Entry | Pages | Matching extracted-text pages | Matching same-renderer RGB pages |
|---|---:|---:|---:|
| Main | 283 | 283 | 283 |
| Two-collision companion | 7 | 7 | 7 |

Renderer: PyMuPDF 1.26.7, one point per pixel, RGB without alpha. PDF bytes differ after rebuilding and byte identity is not claimed. Cross-renderer or arbitrary-platform pixel identity is also not claimed.

Native SHA-256 identities:

```text
native-source.zip  050da4a797d5ef0304e5731d56667fb0536c560f409eadb27a49d3f7777cf650
main.pdf           eb55c356dec431ae747c0129852bd65207c874400db9804354e43355aaa6a0e3
two_collision.pdf  b9390b0975c41bdef488dade494e9d8f06150e191d563e052ad7b556174e1eb1
```

`DELIVERY_VERIFICATION.json` also records the rebuilt PDF hashes. For replication after downloading the pinned artifact and rebuilding:

```sh
python verify_delivery.py EXTRACTED_NATIVE_DIR EXTRACTED_SOURCE_DIR REBUILD_DIR \
  > delivery-verification.json
```

`EXTRACTED_SOURCE_DIR` is the `source` child of the extracted native source ZIP. The script requires PyMuPDF in addition to the Python standard library. Rebuilt byte hashes can vary with build metadata; the meaningful required comparisons performed by the script are content and same-renderer page equality against the native products.

### Warnings and actual visual coverage

The local final main log contains three underfull-vbox notices: one of badness 1057 and two of badness 10000. The companion final log has no notices captured by the checker's warning scan. No missing-character, overfull-box, or LaTeX reference warning was captured by that scan. These are log observations, not a claim that no typography could ever be improved.

Actual visual inspection was performed on main pages **1, 109, 110, 111, 112, and 283**, and companion pages **1 and 7**, using four rendered contact sheets. The displayed material was readable and no clipping was observed in those samples. The dense abstract and long theorem were visible. All other pages received computational text/render comparison, not individual visual inspection. No all-page visual approval is claimed.

## 5. Targeted literature verification

The report's literature comparison is deliberately narrow. Primary records were checked on September 15, 2026. For Finamore–Leguil, the PDF was opened and printed pages 4 and 5 were viewed as screenshots to inspect the enriched-data definition and Theorem A. For De Simoi–Kaloshin–Leguil and Osius, the checked material establishes bibliographic and abstract-level scope, not a complete rereading of their proofs.

The comparison does not claim equivalence between enriched marked lengths, ordinary periodic-orbit marked lengths, and the manuscript's function-valued boundary-law datum. It does not claim a complete priority search or that the central theorem is already in one of those papers. It also does not treat a prior AI-assisted memorandum as a journal endorsement.

## 6. Repository write scope

The intended deposit is the new branch `review/a2-v55-independent-harsh-top4-2026-09-15`, based on the frozen ready head. Only the following six new paths in this review directory are part of the deposit:

```text
REFEREE_REPORT.md
AUDIT_AND_REPRODUCTION.md
check_stopped_experiment.py
INDEPENDENT_CHECKS.json
verify_delivery.py
DELIVERY_VERIFICATION.json
```

No mathematical source, native product, older report, author revision branch, default branch, repository permission, or branch-protection setting is part of this change. A branch/commit comparison should be used to verify this scope after publication. This ledger does not claim that a future GitHub write succeeded before the connector returns and the published tree is read back.
