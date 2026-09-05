# A1 English revision 3.0 — operational closure

**Principal submission:** [main.tex](main.tex), a self-contained 22-page manuscript with seven sections, two appendices and all proofs. **Start the re-review with [RESPONSE_TO_REFEREE.md](RESPONSE_TO_REFEREE.md).**

This revision adds an actual collision-coordinate detector, a counted parameter-independent preparation, an exact positive likelihood state with a matching continuous-state dimension lower bound, and an attained control problem for the full acceptance interval. It does not substitute a no-go conclusion for the previous program.

## Review lineage

Controlling review branch: `review/a1-english-v2-harsh-referee-2026-09-05`.
Review commit: `40be02de7479712d866a575c4b0b9ec930699282`.
New branch: `revision/a1-english-v3-operational-closure-2026-09-05`.
First source publication: `19fc74bcfcdad1e8b6daf28e6444929d423c542f`.

The frozen reviewed source stays at `reviews/a1-english-v2-2026-09-05/source/`. The complete inherited foundation is also published as ordinary files in [foundations/](foundations/), with M1–M3 corrected in place and historical validation clearly marked. Its twenty sections and four appendices are not replaced by the shorter principal manuscript. The principal manuscript contains the new contribution and independently proves every model input it uses.

## Main mathematical additions

The same apparatus has raw numerator densities `pi R^2`, `a0-pi R^2-2TR`, and `2TR(1+epsilon R^2 cos(y-theta))`, divided by the constant cell area `a0`. Both placement failure and censoring consume a cartridge. Firmware uses the measured collision coordinate, not the unknown radius.

At budget n the entire likelihood has an exact normalized positive Bernstein vector of length `3n+1`; the update takes O(n) arithmetic given the one-step coefficients. A coprime-factor argument gives the matching `3n` lower bound for continuous exact likelihood states across the full command family. Four moments specify the censored likelihood; those moments plus one continuation integral form the exact five-dimensional Bellman feasible body. This is not a five-number representation of the entire accepted-report kernel. Measurable gates in `[0,1]` attain the ideal optimum, and finite lookup gates with finite command menus approach it uniformly at each fixed budget.

## Contents and verification

[PROOF_LEDGER.md](PROOF_LEDGER.md) gives statement labels, actual PDF start pages and proof dependencies. [HISTORICAL_DERIVATION_MAP.md](HISTORICAL_DERIVATION_MAP.md) records actual source reuse. [validation/](validation/) contains separate test, build, visual and publication receipts.

From this directory, with Python, pdflatex and pdfinfo installed:

```bash
python -m pip install -r requirements.txt
python build_and_verify.py
```

The PDF is produced at `build/main.pdf`. The script runs the unchanged referee diagnostics and new revision diagnostics, then performs three LaTeX passes. It checks labels, undefined references and overfull diagnostics. It does not build the foundation companion or run the historical eleven-paper author suite.

Recorded execution: **12 original referee diagnostics + 27 new diagnostics passed; 22 PDF pages; 13 proof-bearing entries; zero unresolved label/TeX diagnostics.** These are finite diagnostics, not proof-assistant verification or an independent referee acceptance. The corrected foundation companion is source-complete but was not compiled in this execution. The built principal PDF is also supplied with the conversation delivery; a binary PDF is not stored in this repository directory.
