# General Theta Foundations I — Revision 42

**Alphabet Dynamics and Calibrated Numerical Memory**  
Qian Qi · 26 September 2026

Controlling independent r27: `fdc5acf7e7913dcfc379f5f19d5c97ab21306496`. Reviewed v41 publication: `08773b2705c5ac92716df5daf42a54f3b61bca34`, native v41 source `282bc34bbbeaa56a2ec36c6daf438e545dcfeb37`. This package is additive on `revision/general-theta-foundations-i-v42-canonical-gap-calibration-2026-09-26`. The pre-existing `v42-alphabet-calibration` branch is not modified.

[English article](paper.pdf) · [Native source](main.tex) · [Response to r27](RESPONSE_TO_REFEREE.md) · [Theorem locations](evidence/THEOREM_LOCATIONS.json) · [Executed receipt](evidence/BUILD_RECEIPT.json)

[Compact referee package](evidence/REFEREE_PACKAGE.zip) · [Standalone core sources](evidence/CORE_SOURCES.zip)

## Principal mathematical results

For a fixed r-angle planar command alphabet with an identity letter and the dual badly approximable bound `||m.alpha|| >= b*||m||_1^(-r)`, the exact and fixed-small-error label widths are

```
W_(N,epsilon) = Theta(N^(r/(2r+1))).
```

This is an all-hidden-state converse and an exact common-row upper realization. Every optimized finite-block gap is zero. The same law holds after adding reflection. Explicit examples use `alpha_i = 2^(i/(r+1))`, with the proved dual constant `(2/9)^r`. These angles give computable-real, not asserted algebraic, rotation matrices. Dimension, alphabet, signal and error are fixed. The error range is `epsilon < rho/(2 sqrt(2))`, with `0<rho<=1/10`. The r=1 mechanism is inherited; the multi-angle hierarchy is proved in the current article.

Optimized law gaps are attained alphabet invariants. A finite-block positive gap is equivalent to spectral radius below one for the uniform one-step Koopman average modulo invariant functions. A rational two-letter SO(3) example has zero optimized one-step gap and positive two-step gap, giving linear numerical width. Its positive block gap uses a qualitative external algebraic expansion theorem, not a finite numerical estimate.

Query calibration is an exact rank-constrained projection optimization. Algebraic data admit finite quantifier elimination; a convex SDP relaxation has an explicit dual. The main examples have computed values, including a primal/dual certificate for the two-copy calibration `c^2=1/6`. General query frames admit reconstruction cone programs and perturbation bounds. This is finite calibration, not decidability of infinite-dimensional gap positivity.

Finite component labels are charged by an explicit cocycle compiler. Finite group actions have a finite orbit-tracking upper bound. Metric quotient-equivalence and even the same effective circle action do not alone determine numerical width.

## Reproduction

Use Python 3.12 with SymPy 1.14.0, mpmath, PyMuPDF 1.26.7 and LaTeX providing AMS, Latin Modern, mathrsfs, geometry, microtype, booktabs, mathtools, needspace and hyperref. The full inherited regression build additionally uses NumPy 2.3.5 and SciPy 1.17.0.

```sh
python papers/GTF-I-v42-canonical-gap-calibration/verify.py
python -O papers/GTF-I-v42-canonical-gap-calibration/verify.py
python papers/GTF-I-v42-canonical-gap-calibration/build.py --core-only
python papers/GTF-I-v42-canonical-gap-calibration/build.py
```

The core source ZIP extracts to one package. From its parent run `python GTF-I-v42-canonical-gap-calibration/build.py --core-only`. The full source ZIP includes the pinned predecessor PDFs and verification inputs. No standalone font files are distributed. The workflow commits native sources first, builds that source commit, independently rebuilds the core ZIP, and publishes the artifacts without force to the new work and ready branches.

## Preservation and scope

[Unchanged v41 supporting article](supporting-results.pdf) · [Complete mathematical archive](complete-manuscript.pdf) · [Complete development archive](complete-development.pdf) · [Full rebuilding sources](evidence/SUBMISSION_SOURCES.zip)

All older sources, PDFs, review paths and other work branches remain unchanged. Three inherited analytic modules are byte-identical in the current core; the entire v41 article and cumulative volumes are retained. The compact referee package excludes the large archives.

No all-alphabet classification, numerical general spectral-gap algorithm, sharp finite integer optimum, uniform vanishing-signal theorem, free-bit implementation, autonomous anytime theorem or unrelated analytic pipeline closure is asserted. The optional original-page LPS audit remains as recorded in the predecessor. The matched nongapped law has a precise Diophantine hypothesis. The geometric, spectral and convex ingredients are explicitly credited. Executed checks support reproducibility, not independent proof or priority certification.
