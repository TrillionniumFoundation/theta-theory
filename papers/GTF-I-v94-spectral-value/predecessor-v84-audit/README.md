# General Theta Foundations I — Revision 84

## Finite-Use Geometry and Learning of Ordered Quantum Measurements

This revision responds to both latest R53 reports on completed v83 at `58cbb2608fa65f1fba1b5d56ab1fd55dfd9dacd7`. The reports are frozen verbatim. The requested four-leading-general-journal objective, measurement topic, complete historical proof corpus and independent structural article are retained.

## Main mathematical response

The new support span is `W_E=sum_j P_j H_d P_j`, where `P_j=supp(E_j)`. It is a real linear span, not generally an algebra or the span of the effects. The new results prove:

- a bijective parameterization of the whole covariance kernel, including singular and zero effects, with dimension `d²-dim(W_E)+sum_j(d-rank(E_j))²`;
- the exact criterion `i[G,E] in Ran(C_E)` iff `G in W_E`;
- matching finite-angle actual trace-distance orders on every fixed unitary orbit: zero when stationary, `min(1,sqrt(N)|t|)` inside the support span, and `min(1,N|t|)` outside it;
- a common known-pair recovery construction with explicit error `4m t² ||G||op²`, using the actual classical output and an external reference, not the inaccessible environment;
- regularized data processing when a public probability-weight covariance is transported through the same stochastic output channel, with equality for reversible label splitting; and
- exact polynomial rational support-span decisions and generator projection.

The existing metrological Hamiltonian-not-in-Kraus-span criterion and Knill–Laflamme correction principle are credited to prior work. The new submission supplies its covariance-support identification and a written finite-angle trace-error proof. Orbit constants depend on E,G. No complete arbitrary-pair boundary metric, full-boundary entropy, growing-k minimax equality, or general efficient control/dictionary synthesis is asserted.

## Reading objects

| Entry | Purpose |
|---|---|
| `quantitative.tex` / `paper.pdf` | Focused primary: covariance, supports, finite-angle orbits, transported ridge, balanced learning consequences |
| `supplement.tex` / `BINARY_SUPPLEMENT.pdf` | Entire retained binary auxiliary proof corpus with current-source cross-references |
| `structural.tex` / `STRUCTURAL_PAPER.pdf` | Unchanged independently complete structural article |
| `main.tex` / `COMPLETE_REVISION.pdf` | Complete preservation edition with all previous sections still active |
| `RESPONSE_TO_REFEREE.md` | 15 required items, 30 detailed comments, 28 gates and 10 risks |
| `PROOF_AUDIT.md` | Complete support, recovery, finite-angle and regularization accounting |
| `LITERATURE_AUDIT.md` | Direct primary-source comparisons; unavailable newest full text expressly identified |
| `evidence/JOURNAL_PACKAGE.zip` | Standalone primary, binary supplement and separate structural source graphs |
| `evidence/RESEARCH_PACKAGE.zip` | Complete native proof corpus, four PDFs and fresh evidence |

## Reproduction

```sh
python build_revision.py --check-source
python support_check.py
python support_geometry.py examples/support-bb84.json > support-certificate.json
python support_geometry.py examples/support-bb84.json --verify support-certificate.json
python build_revision.py --isolated          # actual committed native source
python build_revision.py --verify-published # exact published or metadata-only final head
```

The builder runs all 21 prior exact suites anew and the support suite under ordinary and optimized Python. The new suite has 280 positive checks and 18 negative controls. It includes a nonprojective BB84 exact symbolic recovery example. Finite tests do not prove the continuum theorem and are not physical executions. Source-qualified, isolated, standalone and exact-final-head receipts are separate.

Every predecessor mathematical section is byte-identical. The baseline contains 495 native files and 856/363/116 complete/quantitative/structural labels. The quantitative conservation check uses the explicit union of the current primary and supplement, emits every relocated label and verifies its destination. There is no deleted proof hidden by a shorter article. Changed entry/audit/build files retain exact originals under `predecessor-v83-audit/`; earlier revision directories and review branches are untouched.

Independent human priority assessment, signature status and the newest covariant-learning full-text comparison are not represented as completed. The five independent A/B/C/D aggregate flags remain false. Current receipts govern current build status, not earlier successes.
