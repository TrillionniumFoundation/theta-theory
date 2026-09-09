# A2 v10: observable boundary profiles

**Relative boundary laws and inverse experiments in dispersing billiards**  
Qian Qi — September 10, 2026

This is the revision responding to E1–E4 of the completed-v9 report at `b756f4851669e34c7074ba61b5bcf48689756406`. The mathematical source under review was `33ef794a398b23015651482e93be7667c08d6fad`, not the parallel v9 initialization.

## Reading and building

The full English article is native, directly readable TeX: `main.tex`. All its inputs are present in this directory. The companion entry point is `two_collision.tex`. No restoration command is needed to read or compile either manuscript.

From this directory, with a LaTeX installation including latexmk, and Python with SymPy and mpmath:

```bash
python3 tools/build.py
python3 tools/verify_v10.py
python3 tools/run_all_checks.py
```

The clean build produces `main.pdf` (97 pages) and `two_collision.pdf` (7 pages), with shell escape disabled. `VERIFICATION.json` gives the locally checked PDF identities and diagnostic summaries. Binaries are supplied in the accompanying packet; the Git branch publishes their complete native source and reproducible build instructions, not a claim of already-stored native PDF binaries.

The first verification command needs only this directory. The last command also replays the two original suites in a disposable copy. It reads two hash-pinned historical diagnostic inputs from the unchanged `.publication/a2-v9` in a full repository checkout, or accepts `--v9-source-dir PATH` to an authenticated v9 source folder. The downloadable packet contains that folder as `reference_v9`. This dependency concerns historical diagnostics only, not the manuscript build.

## What changed

Section 10 gives the focused singular-kernel deautoconvolution comparison. Section 11 proves finite-preparation recovery of both complete boundary energy profiles from two oriented even-flight binary experiments. The preparation bound charges unsuccessful preparations and balances finite-bridge bias, scalar noise, derivative regularization and rare-event mass. The information table in Section 1 separates this calibrated labelled experiment from both the exact-family unlabelled four-window experiment and the smooth nuisance envelope.

`RESPONSE_TO_REFEREES.md` answers E1–E4 separately. `PROOF_LEDGER.md` identifies the new statements, dependencies, hypotheses and proof steps. `SOURCE_PINS.json` records the source identity. `history/README.md` distinguishes older delivery records from this revision.

All 168 completed-v9 theorem, lemma, proposition, corollary and proof environments remain byte-identical and in their original input order. The new article has 176 such environments. The prior mathematical sections, appendices and companion are not shortened. All pre-existing repository paths remain on the parent tree; the new revision adds a directory and a root index only.

## Interpretation

The new preparation rate is a sufficient upper bound in its explicitly supplied-calibration experiment, not a minimax or computational-complexity theorem. It reconstructs weighted symmetrized energy profiles, not arbitrary asymmetric boundary graphs. Existing general smooth forward results have not acquired the extra quantitative smoothness assumptions used only for sampling.

The local suites pass in ordinary and optimized Python. Their overlapping finite checks are not independent theorem certifications, and no formal proof assistant, exact nonlinear probability oracle, physical simulation or successful remote CI is claimed. Suitability for the requested journals remains for independent editorial and mathematical assessment.
