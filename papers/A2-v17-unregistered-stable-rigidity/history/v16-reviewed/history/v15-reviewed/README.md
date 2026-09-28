# A2 v15 — asymmetric two-contact rigidity

**Author:** Qian Qi. **Date:** 28 September 2026.

The primary article is `main.tex`: *Nonlinear boundary laws and asymmetric two-contact rigidity in dispersing billiards*. The revision responds to the frozen v14 report on review commit `a8e432bd27c21485a4babc268006314a5c7186c5`. It introduces an all-degree asymmetric contact inverse, rather than changing the venue target or relabelling the analytic forward product as new.

## Manuscripts

`main.tex` is a 13-page, theorem-led article with the complete new inverse and observation proofs. `complete/main.tex` is the 133-page complete geometric proof and auxiliary-experiment volume. `complete/two_collision.tex` is the retained 7-page auxiliary article; build it before the complete volume because of external references. Page counts refer to the executed local qualification recorded in `VERIFICATION.json`, not to an unexecuted workflow.

The primary theorem recovers the two contacts' jets of every degree from two oriented two-flight probability germs and two signed transverse endpoint first-moment germs, at supplied labelled gap, separate curvatures, and axis orientation. Unknown area comes from the common leading probability coefficient. The signed moment is additional information: this is not an asymmetric inverse from count-only data. Analytic germs determine the two participating analytic boundary images; unvisited obstacles and arbitrary smooth germs are not inferred from Taylor jets.

At each fixed order, a support-function construction realizes independent odd and even jets with fixed area or free area. Positive-window scalar means are local coordinates on these supplied physical families. A precisely specified binary compression, which does not reveal the original mark or compression seed, has the regular parametric risk order. Its lower bound is not asserted for the uncompressed endpoint experiment.

## Preservation and source identity

`history/v14-reviewed` is the exact native v14 tree `5506d189c55aff9b2e67dc9bfee9602615e0909a`, including its historical derivations. All 312 inherited files are present in `complete`; 309 are byte-identical. The three edited files are its front matter (`main.tex`), the same-section chart convention (`article/16_normal_form_comparison.tex`), and the fixed-window probability-margin paragraph (`article/31_regular_observability.tex`). All 54 original top-level TeX inputs remain in their original order. The complete volume retains 116 proof environments. The historical acknowledgments are also preserved verbatim in `V14_ACKNOWLEDGMENTS_PRESERVED.tex`.

The metadata inside `complete/` and `history/` originated in earlier revisions. They are historical records, not v15 qualification claims. Current entry points are this README, `RESPONSE_TO_REFEREES.md`, `PROOF_LEDGER.md`, `PROVENANCE.md`, `SOURCE_PINS.json`, and `VERIFICATION.json`.

## Reproduction

Install Python 3.10 or later, `latexmk`, a LaTeX installation providing `amsart`, `lmodern`, `microtype`, `mathtools`, `xr-hyper`, and `hyperref`, and Poppler's `pdfinfo`. On Ubuntu the required TeX packages are `texlive-latex-extra` and `texlive-fonts-recommended`.

From this directory run:

```sh
PYTHONDONTWRITEBYTECODE=1 python3 tools/run_validation.py
```

The command checks the frozen source tree, preservation and dependency closure, runs 2,747 new exact rational diagnostics and 1,588 retained algebraic diagnostics in both normal and optimized Python, forces all three complete builds, rejects final TeX warnings/undefined references/overfull boxes, verifies that mathematical sources were unchanged, and writes its actual commands, exit codes, hashes and receipt to `verification/current/`. It never repairs or pushes source. The GitHub workflow has read-only contents permission and records the actual triggering commit and tree in its artifact.

Finite checks, successful compilation and source hashes are reproducibility evidence, not formal mathematical proof certificates or a journal decision. The human author must review the new all-degree argument and references before submission. The requested Annals/Acta/Inventiones/JAMS benchmark has not been replaced by a specialist-journal target.
