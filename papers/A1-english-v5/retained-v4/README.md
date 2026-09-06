# A1 — English revision 4.0

**Author:** Qian Qi. **Edition date:** 6 September 2026.

Principal manuscript: `main.tex`, with all inputs under `sections/` and `references.tex`.

Revision branch: `revision/a1-english-v4-structural-control-robustness-2026-09-06`.

## Read this edition

This revision responds to `reviews/a1-english-v3-2026-09-05/REFEREE_REPORT.md` at review commit `574f2315a136d8b401644d8a3eeeb93c87887010`. The reviewed manuscript is submission `025a9b3fdfd9ffa86e6ae2924f8b5e5b1b58ddd6`, A1 tree `ec09fa385c5fdcc5f2aece59a6b7f0806bfbb8ea`. The review and previous manuscript remain unchanged. This directory is a new edition, not an overwrite of either source.

The manuscript contains the complete inherited principal proof chain plus the following strengthening:

* An exact coefficient-Gram criterion, explicit common-gate right inverse, quantified same-degree perturbation margin, and sharp intrinsic degree-q state dimension.
* Optimal Borel endpoint policies, an explicit last-cartridge solution with at most two collision acceptance arcs, and finite endpoint-lookup value bounds.
* Positive normalized physically implemented surrogates for smooth detector families, with explicit degree–regret bounds and the original flag masses unchanged.
* A strictly positive adaptive advantage over **every** nonadaptive Borel-gate controller, not just a sampled menu. The final example has nonzero-amplitude modes and a full-support prior; its certified gap exceeds **11/10000**.

The old 13 principal proof-bearing labels remain. The current M1 smooth-readout qualification and M2 intrinsic-dimension wording are corrected; the biased-entropy, two-density-trace, transported-preparation, rare-failure, and fixed-controller qualifications remain. `RESPONSE_TO_REFEREE.md` identifies the exact changes and `PROOF_LEDGER.md` maps the statements and dependencies.

## Build and reproduce

From this directory, with Python, SymPy, PyMuPDF, and a TeX installation supplying `latexmk`, `pdflatex`, and the packages in `main.tex`:

```bash
python build_and_verify.py
# Optional page renders for visual inspection:
python build_and_verify.py --render
# Exact adaptive comparison alone:
python tests/certify_adaptive.py
```

The current principal build is **35 pages**. The final PDF is generated as `main.pdf`; it is not required as an opaque prebuilt dependency. A compiled PDF accompanies the conversation delivery. Ordinary LaTeX source, executable diagnostics, and the exact interval certificate are stored directly in this branch.

`validation/V4_CHECKS.json` records **24/24 newly executed checks**, with kinds and limitations. `validation/ADAPTIVE_CERTIFICATE.json` includes all 64 nonadaptive vertex pairs, all eight adaptive first-gate values, and the continuation comparisons. The finite enumeration covers the full comparator only because the manuscript proves the nominal all-Borel reduction and the full-cubic uniform transfer. The script never uses floating-point comparisons for those inequalities.

`validation/V4_BUILD.json` records the current PDF digest, page count, source digests, compiler information, and layout/reference checks. `validation/V4_VISUAL_REVIEW.md` distinguishes the actual visual inspection from automated checks. No proof-assistant verification or independent referee approval is asserted.

## Preservation and historical receipts

`foundations/` is inherited by its exact Git tree `833389dfccd571f989f6143ac44b7de0d0626e69`. It contains the complete corrected v3 foundation companion, including the whole-equilibrium Lorentz calculation. The current principal Appendix A supplies the sharpened report-manifold/ambient-dimension qualification and explicit outer-boundary flux convention; read it alongside the historical companion.

Other inherited tests, validation files, and status text belong to their dated v3 or earlier editions. Their 39 author checks, 20 current-referee checks, 12 earlier-referee checks, and prior PDF builds are **not** added to the v4 execution count and were not re-executed by this v4 suite. The foundation companion was preserved, not rebuilt in this execution. `HISTORICAL_DERIVATION_MAP.md` describes the historical sources actually consulted.

The principal-only source archive supplied with the conversation builds independently; it does not bundle the historical companion, which remains available in the repository. The next review should examine the new class theorem, the two-arc and lookup arguments, the normalization of the physical surrogate, and especially the scope of the full-class adaptive comparison.
