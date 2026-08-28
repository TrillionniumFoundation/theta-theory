# Paper V — referee revision v4

**Controlling source:** `main.tex`  
**Controlling bibliography:** `references.bib`  
**Round-four frozen copies:** `main-round4.tex`, `references-round4.bib`

Title: *Tangent-Law Characterization and Stochastic Representations of Theta-Semigroups*.

Build from this directory:

```bash
pdflatex main
bibtex main
pdflatex main
pdflatex main
```

The paper proves terminal-map Fréchet differentiability, an intrinsic
characterization of entropic theta functionals by probability tangents and
covariance curvature, convergence of microscopic deterministic tangent laws,
a genuine Girsanov theorem with Radon--Nikodym density, quadratic and tangent
BSDEs, a path PPDE branch, a pure energy path game, and a stable-volatility
2BSDE branch.

No terminal derivative is assumed, no degenerate derivative limit is inferred
from local uniform convergence, and no nonlinear `Z -> p` inversion is used.
