# A2 v22 — reference-free certified recovery

Qian Qi · 29 September 2026

**Primary:** *Intrinsic marked boundary laws and rigidity of periodic dispersing billiards*, `main.tex` (17 pages in the actual local build).

**Controlling report:** v21, `b263abc35b2aacb038185d66c5cb13f488d3fe93`. **Reviewed author:** `5ab3be483386dab1b2f53575f47dbf7aebd92bd3`. This revision does not respond to the older v18 report under a new version number.

## Main result and reading route

Theorem 1.2 and Section 3 certify completeness of an arbitrary connected observed component from

`covol(Gamma) - A - sum(visible obstacle areas)`.

The defect is the sum of missing-obstacle area and the nonnegative period-index defect. Zero therefore proves both coverage and full period generation; neither is assumed. The common absolute phase normalization includes hidden bodies and must not be replaced by success-conditioned probabilities.

Theorem 1.3 and Section 4 give a reference-free noisy certificate on explicit bounded analytic/generic physical classes. Shape clustering identifies incidence without known edge-key neighborhoods. Bounded-denominator reconstruction identifies the integer group before any coverage-dependent area calibration. A positive body-area/covolume gap then gives a correct decision and a whole-table estimate. Arbitrary omissions can prevent acceptance but do not create false acceptance in the model.

Section 5 gives the finite-histogram rate, repeated-inspection control and Theorem 5.3's sharp N^{-1/2} hidden-area testing scale in an actual fixed-window physical subexperiment. This is not a whole-table minimax or count-only theorem. Section 6 retains the geometry-aware scanner as one sufficient producer, not an unmarked-trajectory algorithm. The sensor still consists of two density functions or two growing histograms with local marks and absolute normalization.

## Preservation

`retained/v21` is the entire exact reviewed paper tree `a13f1cabd3bc11214bc92ecb6fb49ea51fde87bb`, including its original source history and Supplements R and S. No earlier manuscript, review path or unrelated paper is edited. `core/02_local.tex` is the exact retained intrinsic local proof. `SUPPLEMENT_MAP.md` identifies every volume; `RESPONSE_TO_REFEREES.md` answers each numbered issue in the latest report.

## Reproduction

Requirements: Python 3.10+, NumPy, SciPy, latexmk, LaTeX with amsart/Latin Modern/microtype, and Poppler pdfinfo.

```sh
python3 tools/validate_v22.py
# Exact checkout with the complete retained tree:
python3 tools/validate_v22.py --all-volumes --require-checkout
```

The actual local run passed **5,110 new finite checks and 3,635 selected retained local checks**, with identical normal and optimized output. Its 90 nonlinear stationary-ray curvature comparisons had maximum absolute error `1.2312545871751013e-08`. The primary built to 17 pages with no final TeX warnings, unresolved references or overfull/underfull boxes. All pages were visually inspected.

The local run is **source-content execution, not an authenticated Git checkout**. It did not build retained volumes. The receipt keeps commit/run fields null, records actual commands/exits/hashes and verifies unchanged mathematical/tool sources. The separate read-only workflow checks out its exact triggering SHA, verifies source pins and the preserved native tree, reruns the new and retained suites and builds all five entry documents. Its existence or a queued state is not a hosted pass; consult the actual run for its result.

`tools/certificate.py` implements only the finite conditional arithmetic/decision stage after genuine cycle and area estimates are supplied. Its floating diagnostics are not interval-certified analytic geometry. Finite checks and compilation do not certify every proof, establish priority or constitute a journal decision. The original title, billiard topic and requested Annals/Acta/Inventiones/JAMS target are retained.
