# Paper III — build and circulation notes

Compile with:

```bash
pdflatex main
bibtex main
pdflatex main
pdflatex main
```

The manuscript restates the frozen spectral/coefficient input it needs from
Paper II.  It contains the Doob-selection, martingale--rough, nonautonomous
homogenization, sharp Gaussian rate, dynamic-programming, viscosity-limit, and
theta-semigroup arguments in one file.

The sharp-rate theorem is specifically for full Wasserstein--1 associated with
the declared fractional-Sobolev step-two rough metric.  It must not be quoted
without its range `p>6`, `1/3<eta-1/p`, and `eta<1/2`.
