# A2 v5: relative boundary factorization and collision thresholds

**Qian Qi — September 9, 2026.**

The complete English article is **Relative boundary factorization and collision thresholds in periodic dispersing billiards**. The native entry is [`main.tex`](main.tex). The new revision is prepared for an independent referee; it is not a journal decision or a formal-verification certificate.

## Main results

Theorem 5.1 proves relative two-boundary factorization for spatially varying uniformly convex scalar twist chains, without periodicity. Theorem 6.3 converts its billiard specialization into a full-phase, fixed-offset limiting law. Theorem 13.1 proves a sharp pairwise one-third-Hölder inverse from four unlabelled threshold amplitudes near a three-curvature collision. Theorem 10.3 uses the measured first residual time to remove the inverse-offset factor from the calibration sensitivity of a curvature estimator. The previous circular-reference one-half exponent and all previous mathematical results are retained.

## Read and reproduce

- [`RESPONSE_TO_REFEREE_V5.md`](RESPONSE_TO_REFEREE_V5.md): point-by-point response to NBL-R1, NBL-R2, NBL-R3, and the secondary requests.
- [`PROOF_LEDGER_V5.md`](PROOF_LEDGER_V5.md): hypotheses, proof dependencies, and the scope of the new assertions.
- [`SUBMISSION_INDEX.md`](SUBMISSION_INDEX.md): theorem locators and historical preservation.
- [`verification-v5/VALIDATION_SUMMARY.json`](verification-v5/VALIDATION_SUMMARY.json): executed build, diagnostic, and visual-inspection receipts.

From this directory:

```sh
python build.py
python v5/verify_revision.py > verification-v5/REVISION_CHECKS.json
python -O v5/verify_revision.py > verification-v5/REVISION_CHECKS.optimized.json
cmp verification-v5/REVISION_CHECKS.json verification-v5/REVISION_CHECKS.optimized.json
```

The build requires Python and a standard TeX installation with `pdflatex`. Visual inspection used PyMuPDF. The diagnostics use NumPy, SciPy, SymPy, and mpmath. The completed local native build produced a 55-page article and the unchanged 7-page `two_collision.tex` companion. Compiled PDFs are supplied with the conversation's native archive; the GitHub source build regenerates them. Cross-environment PDF byte identity is not promised.

## Frozen basis and preservation

The controlling review is commit `ec861ecfcdd83a81880c1a9082becc19b0c76977`, at `reviews/a2-v4-nonlinear-boundary-laws-harsh-independent-2026-09-09/REFEREE_REPORT.md`. Its reviewed manuscript is commit `68bbf5b841a66dcc2b85f4d76ce66b1ae8b9782f`, directory `papers/A2-v4-nonlinear-boundary-laws`.

This directory is a new native revision. The original `v2`, `v3`, `v4`, `sections`, companion, historical derivations, and previous response letters remain present. Every one of the 176 labels in the formerly active v4 article remains active in v5. The old publication entry points are preserved under `history/v4-publication`. The original repository directories and review reports are not overwritten. This branch is not a merge into `main`.
