# A1 English v20 — exact kernels and collision-uniform causal geometry

**Manuscript:** *Attainable information geometry in positive experiments*, Qian Qi.

**Controlling report:** `reviews/a1-english-v19-independent-2026-09-07/REFEREE_REPORT.md` at `59018a3231abb551d93947929f7e9bf0e3ddcd9e`.

**Reviewed source:** `01abeb689b203ea871b88495d16a826bb4942e16`, `papers/A1-english-v19/`.

**Revision branch:** `revision/a1-english-v20-exact-kernels-and-causal-geometry-2026-09-07`.

## Reading the submission

`main.pdf` is the complete English manuscript, not a supplement. `main.tex` is its source entry point. The introduction now begins with the collision-uniform checkpoint and causal memory law. Its next subsection separates actual acquisition mass, the whole-image anisotropic cover, and causal compatibility. Table `tab:scope` compares the hypotheses, uniformities, and resource conventions of the theorem families. The body follows that mathematical order rather than the chronology of revisions.

The exact-kernel section, `sections/exact_kernels.tex`, answers E19.1 by proving the stronger assertion rather than changing the name of the old containment theorem. Annihilation feasibility is a positive-cone condition on the product space. Exact realization is equivalent to full column rank of its quotient multiplication pencil. Full-support witnesses can be chosen by arbitrarily small continuous positive density perturbations. A multiplication closure identifies forced directions, and a positive balanced-block family gives an explicit polynomial-root classification, including the referee's eight-point counterexample and exact positive alternatives.

The abstract and contribution statement distinguish these experiment-level conclusions from the elementary separation, Fourier, and determinantal inputs. The significance of the combined conclusions remains for independent mathematical assessment; neither test counts nor the number of statements is offered as a criterion for journal acceptance.

## Response and provenance

`RESPONSE_TO_REFEREE.md` addresses E19.1, E19.2, and the report's organizational obligations. `PROOF_LEDGER_V20.md` records the new dependencies. `HISTORICAL_DERIVATION_MAP_V20.md` identifies the historical arguments used. `LITERATURE_VERIFICATION_V20.md` records the primary-source comparisons. Older maps and response letters are historical documents, not current assertions of scope.

The complete v19 snapshot is retained under `history/v19/`, anchored by source-manifest Git blob `eb846da7fe3e036ebe31c91ecac7b39c52cb3900`. Every one of its 109 compiled proof blocks and 112 theorem/lemma/proposition/corollary blocks remains byte-identical in the new compilation. Five new statement/proof pairs are added. The two documented inherited prose edits leave every formal block unchanged. All other inherited mathematical sources are unchanged. The original v17 manifest additionally anchors the inverse theorem independently of the new manifest.

## Reproduction

Use Python 3.13, SymPy 1.14.0, pdfLaTeX with AMS/Latin Modern/microtype/booktabs/hyperref, and `pdfinfo`.

```sh
python -m pip install sympy==1.14.0
python manifest.py
python build.py --prepare-only
python validate.py
```

`validate.py` runs ten inherited/current diagnostic suites, actually corrupts and restores the inherited inverse proof to test standalone rejection, and builds the full PDF in three passes. `validation/EXECUTION_REPORT.json`, `PRESERVATION_REPORT.json`, and `BUILD_REPORT.json` are execution receipts. They report what ran, not formal proof verification or an independent referee endorsement. The v20 suite checks quotient identities, local density charts, forced kernels, the eight-point regression, exact block witnesses, physical prediction ranks, and edge cases.

This revision is owner-requested and AI-assisted. It does not assert that a journal has commissioned or accepted the manuscript or this response.
