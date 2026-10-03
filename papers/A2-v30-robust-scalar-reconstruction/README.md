# A2 v30 — robust scalar reconstruction

Qian Qi · 3 October 2026

**Primary article:** *Scalar collision laws and recognition of periodic dispersing billiards*, `main.tex`. The controlling report is the latest v29 report at `6444b57768313ac68978b3ee04a428b4832ccb6e`; the reviewed author head is `b81664d3961cdbad58563f37dcaed03288de199e`. The current title, controlled-collision topic and requested Annals/Acta/Inventiones/JAMS target are retained.

## Referee route

The unnumbered Main theorem states the one-bit output, all-attempt denominator (solid starts and free misses both zero), spatial command complexity, known patch margin, calibration scale and arithmetic model together. The five reviewed core chapters remain active and byte-identical. The substantive additions are:

- **Theorem 5.2:** a coupled position/timing/angle bias bound `C(ell + tau + b alpha)/sigma`, including grazing commands. The error may depend on the nominal start. Calibration must be independently established; it is not measured by the bit.
- **Theorem 5.3:** a stopped averaging inverse for known randomized displacement laws. The translated reverse start is coupled to its sampled displacement. A geometric cone condition gives exact recovery in a bounded number of steps and mean-error amplification at most that number. This is an exact functional theorem; arbitrary continuous averaging is not silently declared a finite quadrature algorithm.
- **Lemma 6.1, Proposition 6.2 and Theorem 6.3:** a finite threshold/cluster/hull reconstruction from the original fixed-horizon scalar commands, followed by support smoothing and finite period tests. No search over an infinite-dimensional physical class is used in this new theorem. On the known-margin class it gives conditional C2 error O(nu), O(nu^-3 log(C/(nu delta))) attempts and a conservative O(nu^-6) arithmetic/fixed-kernel evaluation bound. Neither minimax optimality nor Turing bit complexity is asserted.
- **Proposition 8.1:** the exact endpoint-excluded capacity-functional identity, followed by comparisons with mathematical morphology, X-ray probing and wedge probing in their respective information categories.

The original existence selector in Theorem 4.1 remains explicitly existence-based. Known positive nonperiod patch margin eta and a bounded periodic presentation remain necessary inputs to the uniform global conclusion. Exact rational period relations are not exact Euclidean coordinates. The uniformly prepared analytic count-germ question is not identified with this active spatial-input experiment.

## Preservation and submission volumes

`retained/v29` is the exact entire reviewed paper tree `82df1b0fc48b734fa49412fccc72ff6983635e22`, including its nested v28 and earlier history. All five reviewed core files additionally remain active, unchanged, in this primary. `SUBMISSION_MAP.md` distinguishes the current primary, the retained twelve-document package, and the historically named Supplement P. Existing repository papers, reports, workflows and revision branches are not rewritten.

The new full-package driver declares **13 documents**: this primary plus the exact twelve-document v29 package. It delegates the unchanged v29 validator at the current checkout SHA and rejects an incomplete or historical receipt. Preservation is not a claim that those documents were rebuilt in a primary-only run.

## Actual local evidence

`python3 tools/validate_v30.py --output-dir verification/local` passed **6,800 finite mathematical/source checks and 34 validation-contract checks**, with identical normal and optimized Python output. The checks include rational stopped-recursion and perturbation identities, the necessary stopping counterexample, endpoint conventions, bounded-denominator recovery, sampled coupled capsule geometry, adversarial threshold grids and numerical polygon smoothing. The numerical capsule diagnostic uses 108,000 finite configurations; those configurations are not counted as 108,000 independent theorems or formal checks.

The **19-page** primary compiled with no final TeX warning, undefined reference, overfull or underfull box. All pages were rendered for layout inspection. The mathematical and tool source manifest remained unchanged during the qualification run. The local receipt identifies **source-content execution**, with no authenticated checkout SHA or hosted run substituted. It does not rebuild the twelve retained documents and does not claim a hosted full-package result.

The workflow `.github/workflows/a2-v30-verify.yml` is read-only. It checks out its exact triggering SHA, verifies the retained native tree, runs the current and inherited diagnostics, builds all thirteen declared documents and archives actual receipts/logs/PDFs, including failures. A queued or defined workflow is not a pass; its actual run supplies that result. The v29 report's successful twelve-document run is recognized as historical evidence for v29, not borrowed for v30.

## Reproduction

Requirements: Python 3.10+, NumPy, SciPy, latexmk, TeX Live LaTeX extras/recommended fonts, and Poppler pdfinfo.

```sh
python3 tools/validate_v30.py
# In the actual revision checkout, including the retained subtree:
python3 tools/validate_v30.py --all-volumes --require-checkout --expected-commit "$(git rev-parse HEAD)"
```

`tools/reconstruct_scalar.py` exposes finite chain inversion, finite-state Bellman inversion, threshold clusters, convex hulls and bounded-denominator recovery, and a JSON CLI for the chain/hull stages. It is a floating-point reference implementation, **not an interval-certified complete period pipeline or a physical sensor**. The mathematical finite-arithmetic construction specifies where numerical enclosures are required.

Finite diagnostics and compilation do not certify the continuum proofs, validate apparatus calibration, establish literature priority or constitute a journal decision.
