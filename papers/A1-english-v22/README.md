# A1 English v22 — attainable information geometry

**Author:** Qian Qi. **Date:** 7 September 2026.  
**New branch:** `revision/a1-english-v22-prior-uniform-algebra-2026-09-07`.

This is the complete revised English manuscript responding to the v21 independent referee report at `36910a7c6fd08e5ad2e8e10db7c2d8c71c463de8`, based on the published manuscript `7c44bdccc91667c583b5d5cbcff3f8d9160a57d6`. It is a new revision, not a merge into main and not a replacement of any earlier report or manuscript.

## Reading

`main.pdf` is the complete manuscript; `main.tex` is its source entry point. The monomial main theorem and its principal proof remain intact. A second main-route section, `sections/algebra_multistep.tex`, proves a prior-uniform covariance profile for multistep experiments in bounded finite observation algebras. Seven complete appendices retain the companion proofs and alternative routes. Engineering receipts and the referee response are outside the article.

The current response is `RESPONSE_TO_REFEREE.md`; the historical source map is `HISTORICAL_DERIVATION_MAP_V22.md`; proof dependencies are in `PROOF_LEDGER_V22.md`. Stable theorem labels are used throughout these documents. `REVISION_EDITS_V22.json` records the only two citation-level changes to inherited proofs. All 122 inherited theorem-type statements are retained unchanged.

## Reproduction

From the repository, with Python 3.13, SymPy 1.14, a standard AMS-capable TeX installation, and `pdfinfo` available:

```sh
cd papers/A1-english-v22
python manifest.py
python build.py --prepare-only
python validate.py
```

The immutable sibling directories `A1-english-v21` and `A1-english-v20` are required to independently reconstruct the prior compiled source. A standalone subset that lacks those anchors is not the complete reproduction package. The published workflow artifact includes the necessary siblings.

The validation script runs the inherited v10–v15 and v17–v21 suites and the new v22 suite, performs the normal/optimized comparison, tests mutation rejection, and compiles the full article. It can additionally rerun the pinned v21 referee diagnostics when their source is present in the repository. Receipts report whether this source was available; absence in an older downloaded artifact is never reported as a successful rerun.

## Scope

The new algebra theorem is uniform over priors and covariance rank loss under a bounded multiplication condition. Its observation algebra has a finite observable quotient; this scope is proved, not hidden. The original monomial theorem retains its full fixed-prior collision uniformity. Neither statement concerns unbounded horizons or total arithmetic workspace. These are theorem hypotheses, not grounds for deleting the broader historical program.

`SOURCE_MANIFEST.json`, `PRESERVATION_REPORT.json`, `BUILD_REPORT.json` and `validation/EXECUTION_REPORT.json` distinguish source identity, executed validation and mathematical proofs. A successful build or diagnostic count is not a formal proof certificate or a journal decision.
