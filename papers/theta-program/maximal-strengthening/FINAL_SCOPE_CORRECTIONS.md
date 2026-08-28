# Final scope corrections for maximal strengthening

**Latest-wins over every broader reading in this directory.**

## 1. Radial Sinai U3

`S-RADIAL-U3` proves the following actual objects:

- the invariant-density/projector jets through order three;
- the completely assembled differentiated-invariance sources and their reduced-resolvent images at the base parameter;
- the leading eigenvalue and spectral projector for constant-plus-coboundary twists.

It does **not** assert parameter differentiability of the full reduced resolvent `R_a` on arbitrary source directions.  From

\[
L_{a,q}=e^{qc(a)}M_{e^{-qg_a}}L_aM_{e^{qg_a}}
\]

one obtains exact conjugacy of the twisted eigendata, but a derivative of the full reduced resolvent still requires a parameter derivative of `R_a`.  That stronger object remains governed by the graded Paper-I packet.

Accordingly the canonical token is interpreted as

```text
P1-SINAI-RADIAL-U3
= ACTUAL_NONCONJUGATE_PROJECTOR_SOURCE_U3
  + ACTUAL_COHOMOLOGICAL_TWISTED_EIGENDATA_U_INFINITY
```

and not as generic noncoboundary operator U3.

## 2. High-frequency BDL

The actual unconditional moving-family result is `HF-SIMILARITY-BDL`, based on the exact scaling identity

\[
(z-A_a)^{-1}=s(a)C_a(s(a)z-A_0)^{-1}C_a^{-1}.
\]

For a nonconjugate moving family, high-frequency parameter derivatives are conditional on the complete graded generator-symbol packet.  Compactness of the geometric family alone does not create those derivatives.

## 3. Optimal rough-WIP rate

The controlling optimal-rate result is `OPT-RWIP-GAUSS`:

```text
system: deterministic Gaussian Bernoulli shift
distance: full W_1 for the fractional-Sobolev step-two rough-path metric
safe range: p>6, 1/3 < eta-1/p, eta<1/2
sharp rate: N^{-(1/2-eta)}
```

Any earlier claim phrased only in a Stein/Dirichlet test class is superseded by this standard-Wasserstein theorem.  No claim is made that the same exponent is optimal in every Hölder, variation, endpoint, or signature metric.

## 4. Pure Isaacs

The general compact theorem is an equivalence:

```text
pure saddle exists  <=>  H_minus = H_plus.
```

There is no unconditional pure saddle for arbitrary games.  The positive noncompact theorem requires the stated strong concave-convex/coercive structure.

## 5. Weighted/path actualization

The exact actual witnesses are:

- a Gaussian noncompact hidden state with one-step prediction forgetting;
- a deterministic Gaussian shift producing the slow Brownian limit;
- the quadratic noncompact pure game with explicit saddle;
- the bounded genuinely path-dependent terminal functional and its entropic PPDE/BSDE solution.

Claims for arbitrary weighted filters, arbitrary path-dependent Isaacs equations, or arbitrary unbounded terminal data remain packetized theorems, not consequences of this example.
