# Normative technical appendices — referee revision v4

The following appendices are part of the formal-review package.  They expand
proofs that would otherwise make the five controlling `main.tex` files
unreasonably dense.  A theorem invoked from an appendix has the same review
status as a theorem in the main manuscript; these files are not informal
scratch notes.

## Paper I

```text
paper-I-bilateral-response/technical-appendix-v4.tex
```

Contents:

- reflection equations on a bi-infinite itinerary;
- uniform inverse of the billiard Jacobi operator;
- analytic implicit-function theorem on a weighted sequence space;
- Hölder dependence on symbolic itineraries;
- analytic Ruelle operators on one fixed space;
- normal convergence of arbitrary-source susceptibilities;
- periodic-orbit non-coboundary certificate.

## Paper II

```text
paper-II-pressure-diffusion/technical-appendix-v4.tex
```

Contents:

- scalar/quotient block inverse;
- weighted unit-circle convexity;
- Diophantine imaginary-axis gap;
- two-case extension to a right half-strip;
- parameter-derivative resolvent words;
- uniform temporal-shear cancellation and Dolgopyat block;
- all-primitive-direction triangular-lattice proof.

## Paper III

```text
paper-III-rough-theta/technical-appendix-v4.tex
paper-III-rough-theta/physical-clock-appendix-v4.tex
```

Contents:

- exact conditional disintegration for endogenous parameters;
- tensorization to arbitrary finite dimension;
- canonical geometric second-level identity;
- first- and second-level BDG estimates;
- lifted martingale identification;
- state-dependent bracket Riemann sums;
- uniform pointwise HJB consistency;
- controlled consistency and forward theta-independence;
- random roof-clock martingale decomposition;
- inverse-clock convergence;
- physical-time SDE/RDE time change;
- branch-dependent semi-Markov theta recursion;
- exact match with the pressure-root covariance and the nonlattice roof.

## Paper IV

```text
paper-IV-filtering-games/technical-appendix-v4.tex
```

Contents:

- Bayes normalization in the declared TV convention;
- refresh--autoregressive contraction and Lyapunov drift;
- posterior moment ball;
- strategy-tree slow convolution;
- constrained strongly monotone saddle variational inequality;
- coercive optimizer localization;
- common lower/upper consistency;
- viscosity convergence;
- feedback verification by stable smooth approximation.

## Paper V

```text
paper-V-representations/technical-appendix-v4.tex
```

Contents:

- probability-valued replicator ODE;
- total-variation uniqueness;
- static and dynamic tangent characterization;
- weak convergence under bounded exponential tilting;
- microscopic tangent-kernel convergence;
- bounded density martingale and stochastic logarithm;
- Novikov and BMO routes;
- true Girsanov law;
- tangent PDE/BSDE equivalence;
- path tower and stable-volatility DPP/minimality.

## Build commands

From each paper directory:

```bash
latexmk -pdf -interaction=nonstopmode -halt-on-error technical-appendix-v4.tex
```

For Paper III also run:

```bash
latexmk -pdf -interaction=nonstopmode -halt-on-error physical-clock-appendix-v4.tex
```

From the repository root, the updated series Makefile exposes:

```bash
make -C papers/referee-ready appendices
```

## Review boundary

The appendices are intended for line-by-line formal review.  Their presence
does not certify the proofs.  The structural verifier checks that all six
appendices exist, are substantial, have balanced LaTeX environments, and do
not contain superseded dependency shortcuts.
