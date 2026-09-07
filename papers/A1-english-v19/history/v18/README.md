# A1 English v18 — structural classification

**Title:** *Attainable information geometry in positive experiments*  
**Author:** Qian Qi  
**Revision date:** 7 September 2026  
**Branch:** `revision/a1-english-v18-structural-classification-2026-09-07`

This is the complete revised manuscript, not a supplement replacing its predecessor. The entry point is `main.tex`; the compiled manuscript is `main.pdf` when accompanied by a successful current `validation/EXECUTION_REPORT.json`. The preceding submission is pinned at `1f3838d89a5820b853d1e4b78194293b23e70bd2`, and the controlling v17 report is pinned at `a2adb648c08b3c9e803e916f533605203963ee35`.

## Mathematical additions

Three sections add eleven complete named results and eleven proofs.

- `sections/structural_classification.tex`: exact augmented-moment-rank classification of checkpoint and causal memory exponents for positive command-polynomial finite experiments on arbitrary compact metric latent spaces, for every actual prior; polynomial rank strata in the finite prior moment body, including exceptional full-support priors.
- `sections/affine_geometry.tex`: uniform full resolution profile for the whole positive affine acquisition class. The physical acquisition–query cross-covariance supplies the scales; the proof derives its reachable image and unconditional mass, including evidence, through every covariance rank loss.
- `sections/universal_attainment.tex`: necessary and sufficient paired-determinant sign criterion for full acquisition rank under every full-support prior in the square pairing regime, with a matched-space consequence on arbitrary compact latent spaces.

The original collision-uniform monomial theorem, circular double attenuation, operational inverse, uncertainty geometry, decision results, and complete finite numerical constructions are retained. The three new sections do not replace the multi-step results with a one-step assertion. General polynomial experiments receive an exact exponent classification, not a claimed universal anisotropic profile across all degenerations.

## Review and provenance

Read `RESPONSE_TO_REFEREE.md` for the response to E17.1, `PROOF_LEDGER.md` for the new proof dependencies, and `HISTORICAL_DERIVATION_MAP.md` for the inherited arguments used. Original administrative records and the original v17 entry point and preparer are archived under `history/`. The original `papers/A1-english-v17/` directory and all review materials remain unchanged.

`build.py` reconstructs the v17 compiled source using its unchanged, Git-blob-pinned preparer. It then checks inclusion of all 88 preceding complete proof blocks, all 91 preceding complete statement blocks, and all preceding labels in the actual expanded v18 source. The expected v18 totals are 99 proofs and 102 statements. Counts become executed evidence only in a successful current preservation/build receipt; they are not proof certificates.

## Reproduction

With Python 3.10 or later, `pdflatex`, the standard AMS/Latin Modern/mathrsfs packages, and `pdfinfo` installed, run:

```sh
python manifest.py --write
python validate.py
```

For source-preservation checks without typesetting, use `python build.py --prepare-only`. For just the new exact diagnostics, use `python tests/verify_v18.py validation/V18_STRUCTURAL_DIAGNOSTICS.json`.

The complete validation runs the unchanged v10–v15 and v17 author suites, the new exact rational diagnostics, and three LaTeX passes. The authoritative current execution receipt is `validation/EXECUTION_REPORT.json`; earlier receipts are archival records, not executions of v18. Finite diagnostics, source identity, and clean typesetting do not constitute formal verification or a journal recommendation. No claim is made that an editorial significance judgment has already been reversed.
