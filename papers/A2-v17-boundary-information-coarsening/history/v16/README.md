# A2 v16 — integrated submission and adaptive physical experiments

**Nonlinear boundary laws and two-contact rigidity in dispersing billiards**  
Qian Qi · English revision · September 11, 2026

This is the complete native manuscript tree, not a shortened replacement. It is based on the A2 v15 author tree at `627c16b951994fa65acfbf3a621d0e4306131db3` and responds to the independent report at `a108adf17c4b9360e340a2d5708b20a375d69283`. Both existing author and review directories remain untouched elsewhere in the repository. The overwritten v15 entry point and submission metadata are additionally retained in `history/v15/`.

## Reading and contribution order

The principal result is the uniform nonlinear relative physical boundary law on a nonshrinking collar, including every fixed mixed geometric and offset derivative. The scalar linearization is classical; the paper proves its identification with the physical determinant amplitude. Independent two-contact jet inversion, the two-flight benchmark, and full symmetrized profile recovery are distinct conclusions. Full-profile acquisition retains its sufficient, rather than minimax, interpretation.

The revision adds complete proofs for adaptive stopped physical experiments (`article/17_adaptive_experiments.tex`), an exact common-history overlap functional and its critical limit (`article/31_adaptive_critical.tex`), and the referee's exact strict-margin benchmark (`article/16c_strict_margin.tex`). The previously proved fixed-schedule experiment transfer is moved into the main argument, without alteration.

All 52 direct inputs of the v15 entry point remain active; four inputs are added. No theorem, proof, auxiliary application, companion manuscript, or historical source is removed. The main text reduces serial review chronology; detailed responses and source identities remain outside the mathematical narrative.

## Entry points and validation

`main.tex` is the full article. `two_collision.tex` is its full source-pinned companion and must be compiled first because the article imports its labels.

From a checkout of this revision:

```sh
python3 papers/A2-v16-integrated-submission/tools/build_submission.py \
  --output-dir /tmp/a2-v16-complete-build
```

The script requires Python 3.10+, `latexmk`, `pdflatex`, and `pdfinfo`. It checks the entire active input graph, runs exact finite diagnostics in ordinary and optimized Python, builds both complete documents without shell escape, and writes the source manifest, final logs, PDFs, page counts, hashes, and structured build report. Missing inputs or unresolved citations/references cause failure; no appendix is silently omitted.

The executed local finite diagnostics passed, with identical ordinary/optimized output. The exact original companion has also been compiled locally (7 pages). At this source-publication checkpoint, **the full native main build has not yet been verified**; C15-1 is not claimed closed. See `VERIFICATION.json` for the actual evidence rather than interpreting an installed workflow as a successful run.

`RESPONSE_TO_REFEREES.md`, `COVER_LETTER.md`, `PROOF_LEDGER.md`, and `HISTORICAL_DERIVATION_AUDIT.md` explain the revision. They do not claim that the independent referee has withdrawn the significance recommendation, or that numerical checks certify the mathematical proofs.
