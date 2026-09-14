# Audit and reproduction record — independent review of A2 v44

September 14, 2026. This record accompanies [REFEREE_REPORT.md](REFEREE_REPORT.md). It distinguishes inspected source, independently executed checks, author attestations and editorial judgment.

## 1. Exact object selection

Repository: `TrillionniumFoundation/theta-theory`.

The current root README identifies `revision/a2-v44-review-ready-2026-09-14`, whose examined tip is `606664116fa839488d73f1b28fecb5bc3dd0e5dd`. Its tree is `d002598b81cb6513292853bfcb02968af6983fe7`. The mathematical source actually used by the native build is `b229bfa2df2962ea2ebfd0fb2fd11531036d33a6`, not the later documentation-only commit. The products/attestation commit is `fbcf3175f0a13ec3c8508ff16b6deb6d5da2d4d9`.

An authenticated source-to-review-ready commit comparison was read. It reports three descendant commits, no changes to active mathematical TeX, and additions of delivery products plus current documentation. Thus the source archive is the mathematical submission advertised at the examined latest tip; the old source-checkpoint verification ledger is not mistaken for the current delivery ledger.

The prior report is `reviews/a2-v43-independent-harsh-top4-2026-09-14/REFEREE_REPORT.md`, originally committed at `6f7de242000a7db2bf473276b8e1792104c7cd42`. It reviewed v43 source `22d9b930a426cdb2c62984a5a3e5875e95e05e79` and products `edd95683ee57965ff8cd82cee1462a478d06ae39`. Its findings were consulted as history, not copied as fresh verification.

## 2. Source key used in the report

Unless stated otherwise, paths below are relative to `papers/A2-v17-boundary-information-coarsening/` at the [frozen compiled source](https://github.com/TrillionniumFoundation/theta-theory/tree/b229bfa2df2962ea2ebfd0fb2fd11531036d33a6/papers/A2-v17-boundary-information-coarsening). Line numbers are one-based physical source lines. Page numbers come from the downloaded native v44 main and its generated label map, not an older revision.

| Key | Source and location | Use and review scope |
|---|---|---|
| S01 | [Current root README at the review-ready tip](https://github.com/TrillionniumFoundation/theta-theory/blob/606664116fa839488d73f1b28fecb5bc3dd0e5dd/README.md); Git ref/commit metadata; source-to-tip comparison | Revision selection, delivery identity, unchanged active mathematical source |
| S02 | `RESPONSE_TO_REFEREE_V44.md`; [completed VERIFICATION_V44.md at the review-ready tip](https://github.com/TrillionniumFoundation/theta-theory/blob/606664116fa839488d73f1b28fecb5bc3dd0e5dd/papers/A2-v17-boundary-information-coarsening/VERIFICATION_V44.md); preceding v43 report | Author claims and previous-issue disposition; author execution statements remain attributed as such unless independently repeated below |
| S03 | `main.tex`; `article/01_introduction_v41.tex`, lines 1–385; `article/01d_proof_architecture_v41.tex`; `article/01e_realization_overview_v44.tex`; `article/01c_geometric_setup_v43.tex` | Active architecture, theorem hierarchy, precise observation model and novelty comparisons |
| S04 | `v3/10_geometry_action.tex`, lines 1–305, especially 158–305; Lemmas 4.1, 5.1 and 5.2, pp. 15–19 | Fresh scrutiny of localization, weighted bridge and relative determinant mechanism |
| S05 | `v4/10_boundary_layers.tex`, especially lines 1–327; `v3/20_integration.tex`; Theorems 7.2–7.3 and radial integration, pp. 19–25 | Fresh scrutiny of half-line factorization, trace-norm block comparison and fixed-domain integration; not a separate recertification of every later complete-event application |
| S06 | `article/23a_signed_endpoint_rigidity_v27.tex`, theorem statement and lines 132–559; Theorem 12.1, Lemmas 12.2–12.5, Propositions 12.6–12.7, pp. 46–53 | Fresh examination of weighted inverse, truncation/envelope tails, smooth finite remainders, homogeneous isolation and finite triangular inverse |
| S07 | `article/23f_single_offset_law_inverse_v42.tex`, lines 1–270; Theorem 13.1, Corollary 13.3 and Theorem 13.4, pp. 53–56 | Density algebra, stability topology, finite-flight normalization and common-frame composition |
| S08 | `article/23b1_signature_rigid_rerooting_v40.tex`, lines 1–66; `article/23d_rank_two_lattice_recovery_v43.tex`, lines 1–164; Lemma 14.11 and Theorems 15.3–15.4, pp. 63, 67–69; `article/23e_signature_stability_v25.tex` | Dependency examination of retained gluing/stability safeguards; earlier report also consulted. Not represented as a new proof of every global gluing or stability result |
| S09 | `article/23i_nonsymmetric_periodic_realization_v44.tex`, all 404 lines; Section 17, pp. 72–77 | Full fresh scrutiny of Theorem 17.1, Proposition 17.2, Corollary 17.3 and Proposition 17.4, including all-translate clearance, symmetry, registration and analytic perturbations |
| S10 | `article/18c1_endpoint_time_deficiency_v43.tex`, all 194 lines; Lemma 30.1 and Theorem 30.2, pp. 117–120 | Fresh full examination of the stated two-sided comparison: layer, normalized bulk, corner, forward/reverse kernels and count exceptions |
| S11 | `article/18a1_compact_experiments_v32.tex`; inherited likelihood, moment, count-product and adaptive-transfer inputs in Part II | Architecture and historical-review context only. No claim that this report independently rederives every LAN, quadratic-loss or Gaussian-product dependency |
| S12 | `article/25a_common_observables_v25.tex`, especially lines 1–192; Lemma 39.1 and Theorem 39.2, pp. 141–144 | Fresh pilot/acquisition examination: common record spaces, witness mass, onset scan, final-flight calibration, measurability and charged failures |
| S13 | `article/25b_augmented_global_reconstruction_v26.tex`, lines 1–254; Lemma 40.1 and Theorems 40.2–40.3, pp. 144–148 | Fresh examination of finite separation, capped concentration, template rule and fresh-stage budget indexing, conditional on the stated compact inverse inputs |
| S14 | `article/29b_direct_position_benchmark_v26.tex`; Proposition 21.1, pp. 86–88; comparison in S03 | Same-experiment benchmark used in the significance assessment; no assertion that the two observation spaces are equivalent |
| S15 | Native Actions artifact, manifests, native PDFs and logs; authenticated delivery-tree entries; independent rebuild and page parity | Provenance and execution, detailed in Sections 3–5 below |
| S16 | [independent_checks.py](independent_checks.py), [CHECK_RESULTS.json](CHECK_RESULTS.json), [BUILD_VERIFICATION.json](BUILD_VERIFICATION.json) | Independently authored finite diagnostics and execution summary; no mathematical certification inferred |

The source audit is targeted and substantial, not a line-by-line certification of all 228 pages or every inherited theorem-style environment. The companion was obtained, rebuilt and visually surveyed; its complete mathematical proof was not freshly recertified. Favorable findings in the previous review are not automatically promoted to independent results of this round.

## 3. Native retrieval and identities

The authenticated Actions API identified run `34820671440`, attempt 1, with native artifact `10338197591`, named `a2-v44-native-b229bfa2df2962ea2ebfd0fb2fd11531036d33a6-1`. The connector's artifact-download action supplied the actual ZIP bytes. Its inner `native-source.zip` supplied the complete buildable paper source. Direct local GitHub cloning was unavailable and is not claimed as evidence.

| Downloaded product | Pages | Bytes | SHA-256 | Computed Git blob SHA-1 |
|---|---:|---:|---|---|
| `main.pdf` | 228 | 1775792 | `88928386ef8436bb3fd79b7f1ddee3c0d00a620c189833b5d14afc7a0f8b64fe` | `716628d0449622b8aff53a9df88301ec6e5137e4` |
| `two_collision.pdf` | 7 | 333367 | `b9390b0975c41bdef488dade494e9d8f06150e191d563e052ad7b556174e1eb1` | `dae9697f40bcac775d7dd6aa26144af0181adc75` |
| Inner `native-source.zip` | — | 1549844 | `1b65df642d26973b9de895ebe9fe411c53300e3615f3d439fd94e749a6c8d879` | `74fc24215033e673b92ef219f0250978b80bc98a` |

The 97 active-manifest entries (96 for main, one for companion) were checked against the extracted source using SHA-256 and Git-blob hashing, with no mismatches. These are recorded active inputs, not a mathematical theorem count.

The current delivery directory is `deliveries/a2-v44/b229bfa2df2962ea2ebfd0fb2fd11531036d33a6/`; its Git subtree is `af969940cdd519fcfbc3aa10d4a9986fe0bdd631`. The authenticated tree response contains the main PDF and source archive with the exact computed blob identities above, as well as actual raw native auxiliary/log entries. The source-to-tip comparison separately lists both current and repaired-old PDFs and their native auxiliary files as additions.

The current ledger attributes verification of 41 artifact/evidence files and 37 repaired v43 artifact files to the author's publication job. This referee inspected the delivered evidence and matching key Git objects, but did not independently re-download and compare all 78 files byte by byte. The full-count claims remain attributed to the author's attestations. That limitation does not revive the disproven claim that the present complete manuscript is unavailable.

## 4. Independent native rebuild and layout comparison

The complete extracted source was copied to a separate directory. These commands were actually executed there, in this order:

```sh
latexmk -norc -pdf -interaction=nonstopmode -halt-on-error -file-line-error -recorder \
  '-pdflatex=pdflatex -no-shell-escape -recorder %O %S' two_collision.tex
latexmk -norc -pdf -interaction=nonstopmode -halt-on-error -file-line-error -recorder \
  '-pdflatex=pdflatex -no-shell-escape -recorder %O %S' main.tex
```

Both returned zero. Rebuilt page counts are 7 and 228. Different PDF metadata/bytes are not treated as failure; byte identity between the independent rebuild and hosted PDFs is not asserted.

For every corresponding page, PyMuPDF `get_text()` was compared directly, and RGB raster bytes were compared using `get_pixmap(matrix=fitz.Matrix(1,1), alpha=False)`, i.e. 72 dpi. There were **zero text mismatches and zero raster mismatches across all 235 pages**. The final rebuilt main log has no TeX error, no unresolved-reference message and no overfull box; it has four underfull vertical boxes. The companion has none of those four categories. Shell escape was disabled; no literally warning-free claim is made.

This comparison establishes equality of the tested text and raster representations, not equality at every resolution, correctness of every formula, or an all-page visual certificate.

## 5. Actual visual coverage

Readable-resolution visual examination of main pages **48, 49, 50, 53, 54, 55, 72, 73, 74, 75, 76 and 77** was performed from rendered native pages. This covers the finite-remainder/anchor arguments and the entire newly added Section 17. All seven companion pages were examined together in an overview sheet. No clipping, missing formula material or overlap was identified in these inspected pages.

Other selected main pages were rendered but are not counted here as inspected merely because image files were created. All-page 72-dpi parity is separately reported in Section 4 and does not enlarge the readable-resolution inspection list.

## 6. Reproducing the new finite diagnostics

Run from this review directory, with Python 3, NumPy and SciPy installed:

```sh
python independent_checks.py > rerun.json
python -O independent_checks.py > rerun-optimized.json
cmp rerun.json rerun-optimized.json
```

Both modes were actually executed during the review and produced byte-identical output in that environment. The implementation uses explicit runtime checks, not assertions that disappear under optimization. Floating-point last digits can differ across library/platform builds; the numerical tolerances, not cross-platform textual identity, are the intended reproducibility criterion.

The script independently constructs 128 parameter cases, including amplitude endpoints, small operator-norm lattice perturbations, translations and analytic support perturbations with modes 4, 7 and 11. It solves 512 nonlinear contact equations, checks the contact displacement vectors, independently poses the four pairs of complete support images, and recovers lattice Gram matrices by Fourier registration. The registration function never receives the generating matrix. It also tests a corrupted fourth-channel cycle and a deliberately vanishing third Fourier coefficient, and separately checks the scalar-anchor inverse on a non-even action with an unknown nonconstant amplitude.

The smallest tested gap is approximately 4.59474; this is a finite-sample observation, not the proof of the uniform 4.3 lower bound. The all-translate clearance and analytic-neighborhood assertions are addressed by the source proof examination. No finite sampling is claimed to establish them.

Most importantly, this script starts at complete support images for its registration tests. It does **not** estimate a density from physical preparations, reconstruct all jets numerically, or execute analytic continuation. Both the script and its results mark `mathematical_certification` as false.

## 7. Primary literature checked

The following sources were consulted for the limited comparisons in Section 7 of the report. This is not an exhaustive novelty or priority audit.

**L1.** Anna Florio and Martin Leguil, *Smooth conjugacy classes of 3D Axiom A flows*, [arXiv:2010.04120v5](https://arxiv.org/abs/2010.04120v5), revised June 3, 2021. The version notice and retained smooth-conjugacy claim were checked. The v5 revision notice explicitly removes the earlier geometric spectral-rigidity assertion affected by Proposition 3.1.

**L2.** Jacopo De Simoi, Vadim Kaloshin and Martin Leguil, *Marked Length Spectral determination of analytic chaotic billiards with axial symmetries*, [arXiv:1905.00890v4](https://arxiv.org/html/1905.00890v4), August 17, 2022. The abstract, introduction and stated geometry/observation hypotheses were checked, including the open-billiard non-eclipse setting and symmetry/genericity qualifications. Its full proof was not independently refereed here.

**L3.** Douglas Finamore and Martin Leguil, *A CAT(0)-approach to the marked length spectral rigidity of Sinai billiards*, [arXiv:2510.18983v1](https://arxiv.org/abs/2510.18983v1), October 21, 2025. The stated finite-horizon and enriched-marked-length observation qualifications were checked. No reduction between that observation map and A2's channel-law data is asserted.

**L4.** Alexander Meister and Markus Reiß, *Asymptotic Equivalence for Nonparametric Regression with Non-Regular Errors*, [arXiv:1101.5248](https://arxiv.org/abs/1101.5248). The stated Poisson boundary-experiment equivalence was checked as background for the limited priority comparison. It is not cited as an existing proof of A2's billiard-specific inverse.

## 8. Meaning of the recommendation and repository scope

The report's adverse recommendation concerns editorial significance at the requested level. It does not label an unproved counterexample as a fact. The concrete previous realization and current delivery/navigation issues are closed on the stated evidence. No new mathematical obstruction is manufactured to justify an indefinite technical revision cycle.

This review is intended to be committed on a new `review/a2-v44-independent-harsh-top4-2026-09-14` branch based on `606664116fa839488d73f1b28fecb5bc3dd0e5dd`. Only this new review directory is added. The manuscript, author branches, historical reports, native deliveries and default branch are not modified. The final commit identity is supplied by Git after publication and is not fabricated inside a pre-commit receipt.
