# Appendix A — Actual noncompact path evaluation

This appendix is normative for `P5-PATH-ACTUAL`.  The full construction is

```text
../../maximal-strengthening/WEIGHTED_NONCOMPACT_PATH_ACTUALIZATION.md
```

## A.1 Deterministic-fast origin

The fast product system consists of the four-branch moving-seam map, a
countable full-branch innovation map, and a two-sided deterministic Bernoulli
shift supplying iid observation uniforms.  Its weighted filter is actual and
geometrically stable.

The stationary filtered observable has centered sums of order `N^(1/2)`, so
under slow scaling

\[
\epsilon^2\sum_{n<O(\epsilon^{-2})}
[H(\pi_n)-\bar m]=O_{L^2}(\epsilon).
\]

Only the stationary average enters the limiting delay drift.

## A.2 Genuine path state

The slow state is the segment

\[
X_{t+\cdot}\in C([-\delta,0];\mathbb R^d),
\]

and the payoff depends on an integral and a maximum over the entire terminal
window.  It cannot be reduced to the present endpoint.

## A.3 Segment equation

Let `S` be the horizontal shift generator and let `partial_0` denote the
vertical derivative at the present endpoint.  Under the unique pure feedback
saddle, the value satisfies

\[
\partial_tV+\mathcal SV
+b_*\cdot\partial_0V
+\frac12\operatorname{Tr}(a\partial_{00}^2V)
+\ell_*=0.
\]

The segment DPP and comparison identify the unique value in the declared
growth class.

## A.4 BSDE representation

The forward stochastic delay equation and the saddle-reduced Lipschitz driver
give

\[
Y_t=\Phi(X_{T+\cdot})
+\int_t^Tf(s,X_{s+\cdot},Y_s,Z_s)ds
-\int_t^TZ_s\,dB_s,
\]

with `V(t,omega)=Y_t^(t,omega)`.

This is a genuinely path-dependent actual branch.  It is downstream of the
homogenized segment DPP and is not used to derive it.
