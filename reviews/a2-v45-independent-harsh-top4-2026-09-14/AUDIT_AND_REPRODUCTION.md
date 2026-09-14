# Audit record and reproduction notes — independent A2 v45 review

Date: September 14, 2026. This record accompanies [REFEREE_REPORT.md](REFEREE_REPORT.md). It distinguishes fresh mathematical examination, previous referee findings, author diagnostic reruns, new independent diagnostics, and native-product verification. None is represented as a formal mathematical certificate.

## 1. Frozen objects and acquisition

Repository: `TrillionniumFoundation/theta-theory`.

The reviewed submission is the head `1e60d66b4826bf6b6f64a342b66857774ac3b420` of `revision/a2-v45-review-ready-2026-09-14`. Its actual compiled mathematical source is `2f064b86b4e071d24ad671f4dc652d7de32a56a4`. The author branch is `revision/a2-v45-generic-finite-channel-rigidity-2026-09-14`; the native-products branch is `revision/a2-v45-native-products-34829418911-1`. Products and fetched-object attestation are at `e10c054655c452b2d3b5edf49e439ab2154772fe`. The final review-ready commit is a navigation/verification documentation commit, not a new mathematical source revision.

GitHub Actions run `34829418911`, attempt 1, supplied source artifact `10341597640` and native artifact `10341144241`. Both were actually downloaded through the connected GitHub artifact API. The former contains the frozen source archive and Git identity/tree records. The latter contains the two PDFs and 37 further source/build/evidence files. The main has 235 pages; the companion has seven.

Let P denote `papers/A2-v17-boundary-information-coarsening/`. Source paths below are relative to P and pinned to the compiled source commit unless otherwise specified. The new module was additionally fetched directly at the source commit: `article/23j_generic_finite_channel_rigidity_v45.tex`, Git blob `d3112bafff22a2185dd7dc898da99f5b205f59cc`.

## 2. Source ledger and actual mathematical coverage

| ID | Source and location | Coverage in this review |
|---|---|---|
| S01 | `reviews/a2-v44-independent-harsh-top4-2026-09-14/REFEREE_REPORT.md`, at `c984b5a5f0dee0e3a9c78264ff7b5136272fec72` | Read the preceding recommendation, issue dispositions, technical findings and editorial reservations. Previous findings are not silently treated as a fresh proof certificate. |
| S02 | Repository `README.md` and P/`RESPONSE_TO_REFEREE_V45.md`, at review-ready commit | Read the current entry and full response; checked the distinction between source, products and documentation identities. |
| S03 | `article/01f_generic_rigidity_overview_v45.tex`, lines 1–64; current main and introductory setup | Read the new overview and its theorem, the native main input structure, and the relevant observation hierarchy and setup. Theorem 1.3 is on p. 8. |
| S04 | `article/23j_generic_finite_channel_rigidity_v45.tex`, lines 1–525 | Full fresh reading of Section 18: finite sublevels, obstruction descent, skeleton, selected locality, graph count, generic asymmetry, determination, harmonic registration and physical corollary. Native pp. 78–85; Lemma 18.1 p. 79, Theorem 18.3 p. 80, Lemma 18.4 p. 81, Proposition 18.6 and Theorem 18.7 p. 82, Proposition 18.8 p. 83, Corollary 18.9 pp. 84–85. |
| S05 | `v3/10_geometry_action.tex`, lines 1–305; `article/01c_geometric_setup_v43.tex`; `article/02_finite_results.tex` | Fresh reading of geometric localization, quadratic Jacobi reduction, weighted finite bridge and cofactor/log-determinant proof; checked the setup and selected versus complete-event distinction. |
| S06 | `v4/10_boundary_layers.tex`, lines 1–386 | Fresh reading of the half-line construction, relative determinant gluing, summable tails and fixed-domain offset argument. Later auxiliary programme claims are not exhaustively recertified. |
| S07 | `article/23a_signed_endpoint_rigidity_v27.tex`, lines 1–598 | Full fresh reading. Particular emphasis on actual smooth interpolation and functional Taylor remainder, lines 298–404, and new-order isolation/block inversion, lines 406–598. Theorem 12.1 begins p. 47. |
| S08 | `article/23f_single_offset_law_inverse_v42.tex`, lines 1–270 | Full fresh reading of interior density cancellation, scalar anchor, finite-flight perturbation and the common-frame global proof. Theorem 13.1 begins p. 54. |
| S09 | `article/23c_analytic_continuation_v23.tex`, lines 1–44 | Read the complete exact analytic-germ globalization argument. Lemma 13.9 is on p. 60. No noisy-continuation theorem is inferred. |
| S10 | `article/23b_intrinsic_multichannel_rigidity_v28.tex`, lines 1–110; `article/23d_rank_two_lattice_recovery_v43.tex`, lines 1–110 | Freshly checked the signature/symmetry equivalence, incidence definitions, rank-two anchoring and metric-free holonomy used in S04/S08. This is targeted dependency inspection, not a fresh audit of every later gluing/classification statement in these modules. |
| S11 | `article/25a_common_observables_v25.tex`, lines 1–266 | Full fresh reading of Section 40: common record, charged onset scan, measurable calibration, same-flight-number error and finite-test implementation. |
| S12 | `article/25b_augmented_global_reconstruction_v26.tex`, lines 1–254 | Full fresh reading of Section 41: mixed onset/law separation, finite template rule, uncapped/capped coupling, fixed-order and budget-indexed consistency. The compact inverse modulus and adaptive transcript transfer are used as displayed dependencies, not entirely rederived here. |
| S13 | `article/29b_direct_position_benchmark_v26.tex`, lines 1–110 | Read the direct contact-jet acquisition proposition and proof through its conclusion; checked the charged-bin probability and Vandermonde interpolation comparison in the same long-even record. |
| S14 | Native artifact, active-source manifest, raw logs, source archive; author `tools/check_revision_v45.py` and `tools/check_skeleton_v45.py`; the new independent script | Execution evidence described in Sections 3–5 below. Author routines and new independent routines are kept distinct. |

Fresh proof coverage centers on the new Section 18 and its local deterministic and physical-estimation dependencies. The inherited LAN, Poisson deficiency, alternative-moment, adaptive-transfer, deconvolution and count-information results were not all freshly recertified. The companion was rebuilt and compared, but no fresh complete mathematical referee review of it is claimed. No claim of an exhaustive historical-repository or literature audit is made.

## 3. Independent rebuilding and product comparison

The frozen source was extracted and copied into a separate build directory. Both complete native entries were built, companion first, using:

```sh
latexmk -norc -pdf -interaction=nonstopmode -halt-on-error -file-line-error \
  -recorder '-pdflatex=pdflatex -no-shell-escape -recorder %O %S' two_collision.tex
latexmk -norc -pdf -interaction=nonstopmode -halt-on-error -file-line-error \
  -recorder '-pdflatex=pdflatex -no-shell-escape -recorder %O %S' main.tex
```

Both commands returned zero. For each of the 99 entries in the active-source manifest, the extracted source's SHA-256 and Git blob identities were checked, and the separate-build copy was compared byte for byte. All 99 entries passed. This is a comparison to the downloaded active manifest, not an independent remote fetch of all 99 source blobs.

The two PDFs were compared page by page using PyMuPDF text extraction and RGB rendering at `fitz.Matrix(1,1)`, with alpha disabled. All 235 main pages and all seven companion pages matched in extracted text, raster dimensions and raster bytes. PDF bytes themselves differ, so no byte-identical-build claim is made. This comparison does not establish equivalence at every resolution or correctness of every formula.

Both main logs have six underfull notices, zero overfull notices, zero `LaTeX Warning` occurrences and zero `undefined`/`multiply defined` occurrences. Both companion logs have zero occurrences of these notices. Readable-resolution visual inspection in this review covered main pages 79–85 at approximately 115 dpi. Merely rendering or comparing all other pages is not counted as visual inspection.

The following downloaded bytes were hashed independently:

| File | Bytes | Git blob identity |
|---|---:|---|
| `main.pdf` | 1819269 | `e60ebd822e8c830e9bfcfb448533500204bcdba9` |
| `two_collision.pdf` | 333367 | `dae9697f40bcac775d7dd6aa26144af0181adc75` |
| `native-source.zip` | 1599819 | `6e618e1512f523dfbbdb9cb5ff1f6e77659d4560` |
| `main.log` | 33006 | `1141fafed98fb043b2a144e9796ddf635bd1bc2a` |
| `two_collision.log` | 24664 | `c29f642e47be3f588691f73352c495b8044fe62f` |

SHA-256 identities of the two PDFs and source archive are respectively:

```text
main.pdf
cd097ca221cb6e1ca8d1259adbda7dbd3a9837fbe30bc82bc3d995b6500e4c9c

two_collision.pdf
b9390b0975c41bdef488dade494e9d8f06150e191d563e052ad7b556174e1eb1

native-source.zip
c62a107a203351f83c466935574fbb509138f2c0506f0fbaa8f508418a51d1d0
```

The retained delivery directory was inspected through the Git tree API at the review-ready commit:

`deliveries/a2-v45/2f064b86b4e071d24ad671f4dc652d7de32a56a4/`

Its tree identity is `5fd2f3a05f6ef7ac1391490a839f74e05b1c4fae`. The main PDF, source archive and raw-log blob identities above match the inspected tree entries. The companion bytes were independently hashed; the complete companion blob identity is recorded above. The author's all-39-object fetched-retention attestation is distinct from this review's targeted remote-tree/byte checks. The report does not claim a separate independent remote re-fetch of every retained object.

## 4. Author-code reruns

The following author routines were run in ordinary and optimized Python, with the outputs compared:

```sh
python tools/check_revision_v45.py > preservation-normal.json
python -O tools/check_revision_v45.py > preservation-optimized.json
cmp preservation-normal.json preservation-optimized.json
python tools/check_skeleton_v45.py > skeleton-normal.json
python -O tools/check_skeleton_v45.py > skeleton-optimized.json
cmp skeleton-normal.json skeleton-optimized.json
```

Both comparisons matched. The preservation routine reports 97 verified baseline entries, 98 main inputs and one companion input, 216 retained theorem-style environments, 22 retained remarks and ten added theorem-style environments. This is a rerun against its pinned baseline records; it is not a new remote verification of every historical v44 blob or a proof check of those environments.

The author's skeleton routine reports 18 disk tables, 301 clear candidates, 73 independently posed image cases, a determinant-six test, and negative controls including tangential obstruction and vanishing anchors. These finite diagnostics are credited as author tests rerun here, not described as newly authored independent verification.

## 5. New independent diagnostics

The accompanying `independent_checks.py` is a separate implementation using only the Python standard library and importing no author diagnostic. Execute:

```sh
python independent_checks.py > CHECK_RESULTS.json
python -O independent_checks.py > optimized.json
cmp CHECK_RESULTS.json optimized.json
```

Both executions actually completed and their JSON outputs were identical. Assertions are implemented as explicit checked exceptions, so optimization does not remove them.

The inverse routine receives abstract recovered image coefficients, centers, incidence labels and deck marks. It does not receive the generating lattice. Its 240 cases include independently posed channel images, nonzero tree labels, arbitrary integer changes of obstacle representatives, one-obstacle loops, and nonunimodular cycle matrices. The modes-four-and-nine cases use the Bezout identity `-2*4+9=1`; they check the rotation mechanism beyond the explicit modes-two-and-three locus without purporting to implement generic analytic continuation. Random image configurations are not asserted to be geometrically admissible billiard tables.

A deterministic unit-disk example separately treats a tangential third-body contact as an obstruction and checks the descent inequality. Another independent calculation checks the positive scalar-anchor density cancellation for a non-even action and a nonconstant unknown amplitude. Rank-one, disconnected, zero-anchor and reflected-image controls are rejected. Full results are in `CHECK_RESULTS.json`.

No diagnostic estimates an empirical law, recovers arbitrarily high jets, performs noisy analytic continuation, verifies all translates of a random billiard, or proves Theorem 18.7. Finite algebraic checks complement the source audit; they cannot replace it.

## 6. Primary literature checked

The following primary sources were checked online during this review. These are limited observation-map and version comparisons, not an exhaustive priority search or a full independent referee review of each external paper.

**L1.** J. De Simoi, V. Kaloshin and M. Leguil, *Marked Length Spectral determination of analytic chaotic billiards with axial symmetries*, arXiv:1905.00890; Inventiones Mathematicae 233 (2023), 829–901. The checked description concerns analytic open dispersing billiards, marked length data, symmetry and genericity assumptions.  
Source: https://arxiv.org/abs/1905.00890  
DOI: https://doi.org/10.1007/s00222-023-01191-8

**L2.** O. Finamore and M. Leguil, *A CAT(0)-approach to the marked length spectral rigidity of Sinai billiards*, arXiv:2510.18983, v1 submitted October 21, 2025, as displayed by the checked version history. The abstract and Theorem A concern finite-horizon Sinai billiards and enriched marked length data. The definition on PDF p. 4 and theorem context on p. 5 were consulted; the definition page was also viewed as a PDF screenshot. No identification of that data map with selected endpoint-law data is made.  
Sources: https://arxiv.org/abs/2510.18983 and https://arxiv.org/pdf/2510.18983

**L3.** A. Florio and M. Leguil, *Smooth conjugacy classes of 3D Axiom A flows*, arXiv:2010.04120. The checked version history shows v5, June 3, 2021, and an explicit notice withdrawing the earlier geometric billiard assertion affected by an error while retaining dynamical conjugacy conclusions. The manuscript's version-sensitive treatment is not reopened as a defect.  
Source: https://arxiv.org/abs/2010.04120

**L4.** A. Meister and M. Reiß, *Asymptotic Equivalence for Nonparametric Regression with Non-Regular Errors*, arXiv:1101.5248. The checked abstract describes equivalence to two independent Poisson point processes whose support boundaries encode the regression function. This supports the limited observation that the general Poisson-boundary-experiment principle predates this manuscript, not a claim that the present billiard comparison follows from it.  
Source: https://arxiv.org/abs/1101.5248

## 7. Scope of the repository operation

This review is deposited on a new review branch descending from the frozen review-ready commit. Its deliverables are the report, this audit record, the independent diagnostic source and its executed results. The requested operation does not call for changing the mathematical manuscript, overwriting an earlier review, merging to the default branch, or changing repository permissions. Final branch/commit identities are supplied in the delivery message after the writes and read-back checks.
