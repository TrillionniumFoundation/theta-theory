# Final addendum: genuine path-dependent pure game, PPDE and BSDE

Let a deterministic Gaussian Bernoulli shift generate the slow limit

\[
dX_t=(u_t+v_t)dt+dW_t.
\]

The maximizer and minimizer use noncompact real controls with instantaneous Hamiltonian

\[
p(u+v)-\frac\mu2u^2+rac\nu2v^2,
\qquad \mu,\nu>0.
\]

Its unique pure saddle is

\[
u^*(p)=\frac p\mu,
\qquad
v^*(p)=-\frac p\nu,
\]

and the optimized Hamiltonian is

\[
H(p)=cp^2,
\qquad
c=\frac1{2\mu}-\frac1{2\nu}.
\]

Choose the genuinely path-dependent bounded terminal functional

\[
\Phi(\omega)
=\tanh\left(
\int_{T-\delta}^{T}\omega_sds
+\max_{T-\delta\le s\le T}\omega_s
\right).
\]

For `c!=0`, set `theta=2c` and define

\[
U(t,\omega)
=\frac1\theta\log\mathbb E\left[
\exp\left(
\theta\Phi(\omega\otimes_t(\omega_t+W_\cdot-W_t))
\right)
\right].
\]

For `c=0`, use the linear conditional expectation.

## Theorem P5-PATH-ACTUAL

The tower property gives an exact path-space DPP.  Smooth cylindrical approximation and functional Ito calculus give

\[
\partial_tU
+\frac12\partial_{\omega\omega}^2U
+c|\partial_\omega U|^2=0,
\qquad
U(T,\omega)=\Phi(\omega).
\]

The Cole-Hopf transform `V=e^{theta U}` reduces the equation to the linear path-dependent heat equation and gives comparison in the bounded class.  The same value is represented by the quadratic BSDE

\[
Y_t=\Phi(X_{[0,T]})
+\int_t^Tc|Z_s|^2ds
-\int_t^TZ_s\,dW_s.
\]

The bounded terminal functional makes the exponential representation finite and selects the unique bounded solution.

This is an actual path-dependent value, not merely a finite-dimensional Markov payoff written in path notation.  It may be coupled to the actual weighted noncompact filter through any bounded posterior path statistic.

## Export

```text
P5-PATH-ACTUAL
```
