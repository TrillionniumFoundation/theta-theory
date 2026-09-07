# A1 — English revision 17

**Attainable information geometry in positive experiments**  
Qian Qi · 7 September 2026

This is the complete revision responding to the v16 referee report at `0ef7e8bd90c0767b7fdc0f2bd175548242e39cec`, on branch `revision/a1-english-v17-referee-response-2026-09-07`.

## Reading order

Read `main.pdf` for the full English manuscript, `RESPONSE_TO_REFEREE.md` for the point-by-point response, and `HISTORICAL_DERIVATION_MAP.md` for the exact source basis. The new section `sections/operational_reconstruction.tex` proves that the complete integer-budget optimal-regret curve recovers every past-attainable exterior-volume order and characterizes uniform comparison of the curves. Both model specializations are proved. The command domain is explicitly continuous.

All 84 v16 proof blocks and all 87 named theorem/lemma/proposition/corollary statements remain unchanged in the compiled expansion. Earlier exact information, collision geometry, circular law, directional ambiguity, common-name, effective implementation, sequential value and common-risk results remain complete. The revision adds four named results and their four proofs; it does not replace the original forward classification by an abstract hypothesis.

## Reproduction

From this directory:

```sh
python manifest.py
python validate.py
```

From a full repository checkout, the pinned previous referee's mathematical regression suite can also be rerun:

```sh
python validate.py --prior-review
```

Python 3.13, `pdflatex`, the LaTeX packages used by `main.tex`, and `pdfinfo` are required. `python build.py --prepare-only` checks preservation and assembles `build/expanded.tex` without typesetting. No shell escape is enabled.

`SOURCE_MANIFEST.json` binds current text, source code and retained historical records. `BUILD_REPORT.json`, `PRESERVATION_REPORT.json` and `validation/EXECUTION_REPORT.json` report actual execution. They are not proof-assistant certificates or editorial recommendations. PDF and visual-inspection receipts identify the exact artifact inspected; no receipt for v16 is reused as evidence for v17.

The intrinsic finite-state resource is a persistent alphabet of cardinality at most `M`; known model data, the clock and a fixed program are read-only. Continuous command inputs are not a finite command alphabet. The circular result is fixed-horizon and known-contrast; the effective numerical compiler is for the monomial model. These resource conventions are also stated in the manuscript.
