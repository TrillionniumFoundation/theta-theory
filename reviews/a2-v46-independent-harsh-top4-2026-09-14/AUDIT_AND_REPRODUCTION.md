# Audit and reproduction record — A2 revision 46

This record accompanies [REFEREE_REPORT.md](REFEREE_REPORT.md). Its purpose is to separate mathematical review, finite diagnostics, delivery verification, and inherited findings. None of these records is a formal mathematical certificate.

## 1. Pinned objects and source catalogue

The reviewed entry is commit `b48685189554e594d81baa6be9c72fd7ec873975` on `revision/a2-v46-review-ready-2026-09-14`. The mathematical source actually compiled is `ab99196fadc20682c1ee44d6bb433a788c7274ab`. Workflow preparation commit `44457d01bfb809b07c5e22b92e7200c146005bb6` is a different object. First native products were committed at `266f1d4076617c1396ee3c03b33d216dff1b7985`; the subsequent author-attestation commit is `7c6da872a279f3109839fdb82f28e123d002aaa8`.

For S02–S08, paths are relative to `papers/A2-v17-boundary-information-coarsening/` at the actual compiled source commit unless otherwise specified. Native page references use the final 243-page main. Source line references are one-based physical TeX lines.

| ID | Source | Coverage and use |
|---|---|---|
| S01 | Root `README.md`; paper `REVIEW_READY_V46.md` and `RESPONSE_TO_REFEREE_V46.md`, at the reviewed entry commit | Full entry and response read. Establishes source/product distinction, addressed report and claimed scope. Author execution claims were not accepted as independently repeated checks merely by reading them. |
| S02 | `main.tex`; `article/01g_quantized_reconstruction_overview_v46.tex`; introduction/proof-architecture modules | Full new introductory theorem and main input structure read; introductory motivation and proof architecture examined. Theorem 1.4 is on pp. 9–10. |
| S03 | `article/23k_quantized_law_stability_v46.tex` | Entire new section read, including all four lemmas, Theorem 19.5, finite accuracy prescription, Corollary 19.6, selection and charged-cap discussion. Section 19 is on pp. 86–93. |
| S04 | `article/23a_signed_endpoint_rigidity_v27.tex` | Weighted half-line/finite-envelope mechanisms and homogeneous blocks examined; the functional finite-remainder proof, lines 298–404, freshly read in full. Section 12; Lemma 12.4 starts on p. 51. This is not a renewed audit of every relative determinant estimate elsewhere in the corpus. |
| S05 | `article/23f_single_offset_law_inverse_v42.tex` | Four-density cancellation, nonzero anchor, two-point interior stability and finite-flight normalization interface examined, particularly lines 1–230. Used for the finite action-jet estimate. |
| S06 | `article/23j_generic_finite_channel_rigidity_v45.tex` | Clear-skeleton construction, asymmetry argument, generic theorem, common-frame paragraph and cochain formula examined. Section 18, pp. 79–86; corrected backtrack wording occurs in Theorem 18.7. This does not independently re-referee every older analytic-continuation/signature theorem referenced there. |
| S07 | `article/25a_common_observables_v25.tex` | Specifically examined the same-final-flight pilot clarification and observable normalization/test transfer, lines 184–266, including TV continuity and the bounded-Lipschitz test hypothesis. The implementation proposition is on p. 159. |
| S08 | `article/25b_augmented_global_reconstruction_v26.tex` | Specifically examined lines 130–173: choose final J first; choose pilot accuracy second; use fresh success sequences and separate cap failure. This is a targeted calibration-interface audit, not a new complete audit of Part III. |
| S09 | `reviews/a2-v45-independent-harsh-top4-2026-09-14/REFEREE_REPORT.md` at `0614a20bbba6312830b5523b806ddc726a6333f1` | Previous findings and adverse editorial recommendation read, including the explicit warning against an indefinitely expanding proof-repair checklist. Prior findings are distinguished from current fresh checking. |
| S10 | Native artifact `10345480046` from Actions run `34838199154`, attempt 1 | Archive downloaded; evidence and active sources checked; both manuscripts independently rebuilt; every native/rebuilt page compared. See below. |

Pinned mathematical source directory: <https://github.com/TrillionniumFoundation/theta-theory/tree/ab99196fadc20682c1ee44d6bb433a788c7274ab/papers/A2-v17-boundary-information-coarsening>.

Pinned review-ready entry: <https://github.com/TrillionniumFoundation/theta-theory/tree/b48685189554e594d81baa6be9c72fd7ec873975>.

The previous report's compiled source was `2f064b86b4e071d24ad671f4dc652d7de32a56a4`. The current preservation script compares against its recorded baseline; it does not turn every preserved proof into a freshly verified proof.

## 2. Primary literature checked on September 14, 2026

**L1.** Lloyd N. Trefethen, *Quantifying the ill-conditioning of analytic continuation*, arXiv:1908.11097v1. Primary record: <https://arxiv.org/abs/1908.11097>. The record describes conditional continuation under a complex-domain bound and severe strip/channel conditioning. Used for context and attribution, not as a proof of the manuscript's constants.

**L2.** Douglas Finamore and Martin Leguil, *A CAT(0)-approach to the marked length spectral rigidity of Sinai billiards*, arXiv:2510.18983v1. Primary record: <https://arxiv.org/abs/2510.18983>. Its stated input is an enriched marked length spectrum for finite-horizon Sinai billiards. No identification of that observation with the present endpoint laws was inferred.

**L3.** Anna Florio and Martin Leguil, *Smooth conjugacy classes of 3D Axiom A flows*, arXiv:2010.04120v5. Primary record: <https://arxiv.org/abs/2010.04120v5>. The version notice reports the removal of an earlier geometric spectral-rigidity result after an error, while dynamical results remain. Used only to check this version-sensitive distinction.

These are checks of named primary records and their stated results/version notices, not new complete referee audits of those papers or an exhaustive literature search. No claim of proven priority or of one observation model subsuming another is made.

## 3. Native artifact and independent rebuild

Artifact retrieval used the authenticated GitHub Actions artifact-download action, not an inaccessible repository-web PDF preview. The ZIP was extracted with path containment checks. Its nested `native-source.zip` supplied a complete source directory. A separate copy, rather than the original native product directory, was used for rebuilding.

Verified SHA-256 identities:

| Object | SHA-256 |
|---|---|
| Downloaded Actions artifact ZIP | `7d8f457382bbaabcb4cccf5590fd1ee37c6edce4374aa2c32636dd99461c72a2` |
| Native main PDF | `f93a998816b1d6f149393a1c93ec111f1f6310a95c0b00269eea691731584075` |
| Native companion PDF | `b9390b0975c41bdef488dade494e9d8f06150e191d563e052ad7b556174e1eb1` |
| Nested native source ZIP | `95ddd9f96f8c24f2feecf951bacb0da0061b13bc903f5dd330d8e6be7ff4f9dc` |
| Native build report | `3323ed19eedf4ac8ac21cfe5f3de919d51a46d8cdd248bf2e7033ff5ff99ec80` |

All **34 evidence-file identities** listed in the native build report were checked locally. All **101 active source identities** matched the extracted source and the separate rebuild source. This report does **not** claim that the author's separate 41-object Git-blob attestation was independently repeated against GitHub's blob API.

Run from the extracted paper root, companion first:

```sh
latexmk -norc -pdf -interaction=nonstopmode -halt-on-error -file-line-error -recorder \
  '-pdflatex=pdflatex -no-shell-escape -recorder %O %S' two_collision.tex
latexmk -norc -pdf -interaction=nonstopmode -halt-on-error -file-line-error -recorder \
  '-pdflatex=pdflatex -no-shell-escape -recorder %O %S' main.tex
```

Both builds returned zero. The main has 243 pages and the companion seven. MuPDF 1.26.7 was used for pagewise extraction and raster comparison under Python 3.13.5. All **250 pages** have identical extracted text and identical 72-dpi raster pixels between the downloaded native and separate rebuilt versions. The PDF byte streams are different; the separate hashes appear in `CHECK_RESULTS.json`.

The main log has five underfull notices, zero overfull notices and no unresolved citation/reference. The companion has none of these notices. These results establish reproducibility of the inspected source/product pair, not correctness of the mathematics.

Readable-resolution visual inspection actually covered main pages **88–93**, using rendered images at 1.4 pixels per point. Other pages were rendered or mechanically compared but are not described as individually visually reviewed. No OCR was used. No fresh mathematical review of the complete companion is claimed.

## 4. Referee implementation versus author-code reruns

The included `independent_checks.py` imports no author diagnostic. Its dependencies are Python 3 and SymPy; it uses exact symbolic algebra for the cubic/quartic Bellman identities and deterministic seeds for floating phase tests. Verification decisions use explicit exceptions and remain active under optimized Python.

```sh
python independent_checks.py > independent.json
python -O independent_checks.py > independent-opt.json
cmp independent.json independent-opt.json
```

These commands were executed successfully. The JSON is identical. The script SHA-256 is `168b248dc0154100c1008db30681d93a382e597c4e023bd57a84ef914689a745`.

The exact Bellman test uses gap 1, curvatures 1/2 and 1/24, action curvatures 9/10 and 5/8, and half-line slopes 3/5 and 5/12. The cubic and quartic graph coefficients remain symbolic. It verifies the stated leading blocks, determinant one and the actual lower-remainder inverse. Suppressing the quartic lower remainder fails. The 300 phase checks include {2,3}, {4,9} and {6,10,15}. The latter witness has gcd one without any coprime pair.

The histogram aliasing and quadratic-cap offset calculations are functional diagnostics. They are not claimed to be periodic billiard tables. The illustrative sufficient jet-order calculation is not a lower bound on the inverse problem, a statistical impossibility result, or a class instantiated by a physical table.

The following **author implementations** were also inspected and rerun from the frozen paper source, under ordinary and optimized Python:

```sh
python tools/check_revision_v46.py
python -O tools/check_revision_v46.py
python tools/check_quantized_v46.py
python -O tools/check_quantized_v46.py
```

Each normal/optimized output pair is identical. The preservation rerun reports 99 baseline entries, 95 byte-identical active files, four modified active originals archived, 100 current main inputs, one companion input, and retention of 226 theorem-style environments, 22 remarks and 466 mathematical environment blocks. Seven theorem-style environments are added. The author's finite-series rerun has 24 cases of 64 flights through order six, with maximum coefficient error about 4.45e-16, and 240 phase checks. These outputs remain labelled as author-code reruns even when an embedded author description uses the word independent.

`CHECK_RESULTS.json` records both categories separately. No script verifies all smooth remainders, all infinite-orbit estimates, all global realizability assumptions, or every theorem in the manuscript.

## 5. Scope exclusions and repository changes

Fresh coverage is defined in the source table above. In particular, there was no new full line-by-line audit of all retained relative-operator estimates, LAN and Poisson experiments, deconvolution statements, all appendices, the companion, A1, or the wider eleven-paper program. The report neither certifies nor refutes those unrefreshed results by inference from build success.

The new review branch was created from the exact reviewed entry commit. Only new review files are added under `reviews/a2-v46-independent-harsh-top4-2026-09-14/`. The author manuscript, historical reviews and native products are not edited; no default-branch merge, forced ref update, permission change or administrative action is part of this review.
