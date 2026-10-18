# General Theta Foundations I — R72 author revision

**Read first:** `main.tex`, the paired `supplement.tex`, `MINIMAL_READING_GUIDE.md` and `RESPONSE_TO_REFEREE.md`. The complete current article continues the genuine R71 mathematics; it is not another referee report. The title and Annals / Acta / Inventiones / JAMS research objective are unchanged.

The new proofs classify finite stochastic realization of compactly reversible responses by finiteness of the observable response group, establish a matching arithmetic memory envelope for two noncommuting commands on shared labels, and determine exact periodic multi-frequency memory by a partition/lcm formula with counted initialization. The entire periodic mixture has an exact one-label leakage increment. Deterministic-transition and stochastic minima can differ (16 versus 105 at orders 3,5,7).

## Source baseline

The actual remote parent is `123d356bfa81b3d5f715591dfe5864ace29610e1`, tree `63f7c6e8a7d45efb07d7bb233f84c0ad34d71253`. Its complete paper subtree `ccea92b801c8f3c587aa60c0960ff3f0a08a5f47` is preserved as `retained/r71-native`. The older archive-local R71 commit and its failure observation predate the later remote source recovery. A branch name pointing to that parent without new source is not a newer manuscript.

The controlling unresolved report remains the repository-deposited R65 report at `358481b21ceeeedb1205ebd30f86982e32a2cb04`, blob `d1ff9c5662390156ee212c82b173e86a21180e84`. It reviews R65 only. Its immutable pointer and scope are in `inputs/review`; the local verifier does not pretend to have hashed a locally absent report body. The previously closed tied/rigidity issues stay inherited rather than repeatedly reopened.

## Rebuild

```sh
python3 -m pip install -r requirements.txt
python3 verify.py --out /tmp/theta-r72-independent --source-commit <actual-checked-out-SHA>
```

Native dependencies are pdfLaTeX, the inherited AMS/LaTeX packages, and Poppler. The verifier checks the current source manifest, every retained tree, the unchanged current theorem bodies, twelve ordinary/optimized diagnostic pairs, native paired references, all theorem-index entries and source immutability. Output must be outside this directory. Exact and floating finite diagnostics are counted separately. Neither a native build nor finite tests certify mathematical novelty, formal proof, independent human approval or editorial acceptance.

The commit/publication/push status is recorded outside this immutable source in the delivery record. No queued, missing or old workflow is a current hosted pass. `ci-workflow.template.yml` is a supplied isolated workflow template, not evidence it has been installed or run.
