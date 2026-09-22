# General Theta Foundations I — ninth revision

**Causal Experiments, Predictive Quotients, and Resource-Aware Reduction**  
Qian Qi · September 23, 2026

## Read this submission

`paper.pdf` is the canonical article. `complete-development.pdf` contains the same numbered canonical mathematical body followed by the preserved predecessor developments and historical introductions. `main.tex` and `development.tex` are their native LaTeX entry points. No earlier source file has been rewritten or deleted for this revision.

The controlling referee report is the actual v8 decision-spectrum report at commit `1e2ad3c7c5687e9cc9c0e7e0b37e983795f9f4c5`, reviewing the manuscript at `83a887b9212c54e5e09f88821296ccce3d051504`. Its path is `reviews/general-theta-foundations-i-v8-decision-spectrum-harsh-referee-2026-09-23/REFEREE_REPORT.md`. This is not the earlier nominal-v8 report at `fc6d51a...`.

## Mathematical changes

The principal addition is the **controlled common-encoder minimax theorem**, with the encoder fixed across tasks and each task controller fixed across its unknown-parameter rows. Its risk body, support-function dual, controlled continuation partitions and occupancy recursion are proved from the finite instrument. Shared and private randomization are distinguished; a retained design index, including initialization, is charged. A strict two-label example separates their optimal errors.

The same functional gives a maximum-over-tasks quadratic variance formula, a private finite-polynomial A1 formula at unchanged width, and an exponential-moment duality. The least likelihood-saturated predictive quotient is constructed and proved minimal within its stated coordinate class. Rational finite sources have a finite compiler with description, seed, state, workspace and running-time bounds. A noisy Gaussian delayed-query experiment exhibits causal error `S^(-2/d)` for a scalar target whose static query-aware checkpoint error is `S^(-2)`.

The earlier tree, Wasserstein, Gaussian-vector, count and filter results remain available in full. Their existing marks and hypotheses have not been silently strengthened. The new finite controlled converse pursues **Route C** in the report, rather than splitting the manuscript or replacing proofs by closure declarations.

## Referee navigation

`RESPONSE_TO_REFEREE.md` answers every report section. `PROOF_LEDGER.md` identifies each new theorem, its exact assumptions and proof mechanism. `LITERATURE_COMPARISON.md` records the closest prior results and consultation limits. `HISTORY_AUDIT.md` and `PIPELINE_DEPENDENCIES.json` distinguish actual protocol adapters from conditional physical-model interfaces. They do not treat the independent A2 primary algebraic chain as a GTF consequence.

## Rebuild

From a clean repository checkout, with Python 3.12, a TeX installation providing `pdflatex` and the packages used by `papers/GTF-I-v2/legacy/preamble.tex`, and `pdfinfo`:

```sh
python -m pip install -r papers/GTF-I-v9-causal-minimax/requirements.txt
python papers/GTF-I-v9-causal-minimax/build.py
```

The build checks source hashes, runs the v9 diagnostics in ordinary and optimized Python, rejects seven deliberately incorrect variants in both modes, reruns the inherited v1–v8 diagnostics, and compiles both views until references stabilize. It rejects unresolved references, duplicate labels and overfull boxes. It writes an exact-source build receipt, label maps and a source archive under `evidence/`. The archive contains sources, not font files.

`evidence/BUILD_RECEIPT.json` binds the mathematical source commit and exact input hashes. The later publication commit can contain the generated PDFs and evidence without changing those mathematical inputs. `--skip-diagnostics` is available only for explicitly identified typesetting/preservation rebuilds and is recorded as such in the receipt.

These are reproducibility and finite-consistency checks. The analytical proofs are in the manuscript. Neither a build receipt nor a successful workflow certifies novelty, an independent referee's approval, or journal acceptance.
