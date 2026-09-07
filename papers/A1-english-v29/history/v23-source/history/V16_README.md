# A1 — English revision 16

**Attainable information geometry in positive experiments**  
Qian Qi · 7 September 2026

This is the complete English manuscript responding to the v15 referee report, not only a response letter or a proposed revision. Its basis is submission `e1d0ff2ef04a8641ac77923b664c4d3e8386f212`; the controlling review is `d89bc35dc5d50240c8ae3c82aa251437dcc2165a` on `review/a1-english-v15-harsh-referee-2026-09-07`. The new destination is `revision/a1-english-v16-referee-response-2026-09-07`.

## Reading entry points

`main.pdf` is the full manuscript and `main.tex` its source entry point. `RESPONSE_TO_REFEREE.md` answers E15.1, E15.2 and the limited editorial requests. `PROOF_LEDGER.md` gives the stable labels and proof dependencies.

The revision develops a theorem- and resource-level comparison with Bayesian Fourier filtering, places the two acquisition–observation coordinate chains side by side, and sharpens the mathematical case for the full collision-uniform, past-limited resolution invariant. The abstract and circular theorem's surrounding text keep fixed horizon, known contrast, read-only program and persistent-label conventions visible. No new theorem is claimed just to increase the result count.

All 84 complete v15 proofs and all 87 complete named theorem statements remain verbatim in the compiled paper. The monomial classification, general positive-history criterion, circular theorem, all ambiguity-width orders, exact-prefix and common-name results, and full numerical construction/precision/resource/contract appendices are retained. The previous expository files and their verification records are archived under `history/V15_*`.

## Reproduction

From this directory:

```sh
python3 manifest.py
python3 validate.py
```

The driver executes the six inherited author suites (68,481 assertions) and a three-pass `pdflatex` build. `python3 build.py --prepare-only` expands the complete source and checks preservation without requiring TeX. Python 3.13, the packages in `main.tex`, and `pdfinfo` suffice for the full validation.

From a complete repository checkout, `python3 validate.py --prior-review` also reruns the pinned v15 referee script (1,800 exact assertions). It is a regression run of existing independent-review diagnostics, not a new independent review of v16. Each execution generates current receipts in `validation/`; old receipts are not reused. `SOURCE_MANIFEST.json` hashes text and code; `V15_PRESERVATION_MANIFEST.json` and the generated preservation report identify complete statements and proofs. These are integrity checks, not proof-assistant certificates or evidence of journal-level importance.

## Scope

The monomial theorem retains arbitrary fixed full-support priors and uniformity over compact one-step exponent chambers containing arbitrary future additive collisions. The circular theorem retains Haar prior, exactly known contrast and a fixed finite horizon, with uniformity in label budget and contrast on the proved small interval. At zero contrast its physical state is constant. The effective numerical compiler is for the monomial model, not the circle.

The manuscript is submitted for further mathematical review. Neither the repository's referee-style report nor this response is commissioned by Annals, Inventiones, JAMS or Acta, and no editorial acceptance or exhaustive priority determination is asserted.
