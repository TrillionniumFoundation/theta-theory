# Final addendum: sharp enhanced-WIP rate in full rough-path Wasserstein distance

Let `T` be the deterministic shift on the Gaussian product space `(R^d)^Z` and let `xi(omega)=omega_0`.  Let `mathbf W_N` be the canonical step-two lift of the polygonal normalized sum process.

Fix

\[
p>6,
\qquad
\frac13<\eta-\frac1p,
\qquad
\eta<\frac12.
\]

Let `W_1^{eta,p}` denote 1-Wasserstein distance for the inhomogeneous fractional-Sobolev step-two rough-path metric.

## Theorem P3-RWIP-OPTIMAL-WETA-P

There are constants `0<c<=C<infinity` such that

\[
\boxed{
cN^{-(1/2-\eta)}
\le
W_1^{\eta,p}
\bigl(\mathcal L(\mathbf W_N),\mathcal L(\mathbf B)\bigr)
\le
CN^{-(1/2-\eta)}.
}
\]

### Upper bound

Couple the Gaussian increments with Brownian grid increments.  Then `W_N` is exactly the polygonal interpolation of Brownian motion in law.  Brownian-bridge scaling on the mesh, followed by Chen's identity for the second level, gives the upper bound.

### Lower bound

Let `V_N` be the mesh-polygonal path subspace.  The functional

\[
F_N(\mathbf x)=\operatorname{dist}_{W^{\eta,p}}(x^1,V_N)
\]

is 1-Lipschitz for the rough metric and vanishes on `mathbf W_N`.  Independent bridge fluctuations on the middle thirds of the mesh intervals and fractional Poincare scaling yield

\[
\mathbb EF_N(\mathbf B)
\ge cN^{-(1/2-\eta)}.
\]

Kantorovich duality gives the lower bound.

The result is metric-specific.  It does not claim the same exponent for endpoint, Hölder, variation or arbitrary signature metrics.
