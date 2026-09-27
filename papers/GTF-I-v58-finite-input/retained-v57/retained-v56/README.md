# General Theta Foundations I — Revision 56

## Clocked Stochastic Realization and Finite Observable Quotients

The main article is `paper.pdf`; readable source is `main.tex` and `sections/`. The controlling v55/r37 report is frozen as `FROZEN_R37_REPORT.md`. `RESPONSE_TO_REFEREE.md` addresses every major and local request. The theorem map appears immediately after the introduction.

The main additions are same-width stationarization under eventual approximate returns, physical-equivariant purification, a complete equality-inclusive clocked finite-quotient classification, exact phasewise limiting minima, a nonabelian spherical width law up to a logarithm, existential-real completeness for finite-group data, and finite-precision/random-bit budgets. The preceding conclusions remain in the article and in an independently buildable native preservation tree.

### Build

With Python 3.11, SymPy 1.14.0, PyMuPDF 1.26.7 and standard TeX Live packages installed, run:

```sh
python build.py --check-isolated
```

The build reruns exact regression suites in normal and optimized Python, builds six documents, verifies all source identities and theorem labels, and rebuilds the portable native archive independently. The expected command can fail; actual success, source commit, page counts and checks are recorded only in `evidence/BUILD_RECEIPT.json` after execution.

### Deliverables

`paper.pdf` is the new article. `PURIFICATION_PREDECESSOR.pdf`, `RADIUS_PREDECESSOR.pdf`, `SCALAR_PREDECESSOR.pdf`, `COMPANION_NOTES.pdf` and `COMPLETE_SUPPLEMENT.pdf` preserve the prior documents. `evidence/CORE_SOURCES.zip` contains readable native source without a repository dependency. `evidence/REFEREE_PACKAGE.zip` includes the PDFs, response and actual qualification records.

`finite_group_formula.py` validates a finite group table and emits a degree-three existential real formula in SMT-LIB form; it does not solve arbitrary formulas. `finite_precision.py` implements rational-to-dyadic row rounding and integer sampling. `check_revision.py` tests these utilities and finite algebraic examples, including noncommuting conventions and failure controls.

Universal mathematical claims are proved in prose, not established by finite regression counts. Independent mathematical and priority review remain separate. No A/B/C/D aggregate closure or journal acceptance is asserted.
