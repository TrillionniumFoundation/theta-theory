# Final addendum: actual fully nonlinear path-dependent volatility branch

Let the deterministic Gaussian Bernoulli shift supply i.i.d. standard normal increments.  At slow step `k`, a controller chooses

\[
\alpha_k\in[\underline\sigma,\overline\sigma],
\qquad 0<\underline\sigma<\overline\sigma,
\]

and the deterministic-fast approximation is

\[
X_{k+1}^{\varepsilon}
=X_k^{\varepsilon}+\varepsilon\alpha_k\xi_k,
\qquad k\varepsilon^2\le T.
\tag{1}
\]

Predictable-characteristic convergence gives the weak limit

\[
X_t=x+\int_0^t\alpha_s\,dW_s.
\tag{2}
\]

For a bounded uniformly continuous genuine path payoff `Phi`, define

\[
\mathcal E^G_{t,T}[\Phi](\omega)
=\sup_{\alpha\in\mathcal A_{[t,T]}}
\mathbb E\left[
\Phi\left(\omega\otimes_t
\left(\omega_t+\int_t^\cdot\alpha_s dW_s\right)
\right)
\right].
\tag{3}
\]

## Theorem P5-PATH-2BSDE-ACTUAL

The family of volatility laws in (3) is stable under conditioning and concatenation.  Hence (3) satisfies the path-space dynamic programming principle.  Its path-dependent viscosity equation is

\[
\partial_tU+G(\partial_{\omega\omega}^2U)=0,
\qquad
G(\Gamma)=\frac12\sup_{a\in[\underline\sigma^2,\overline\sigma^2]}a\Gamma,
\tag{4}
\]

with terminal condition `Phi`.

On the canonical path space, let `P` range over the nondominated laws whose quadratic-variation density lies in
`[underline_sigma^2,overline_sigma^2]`.  The value admits the second-order BSDE form

\[
Y_t=\Phi
-\int_t^TZ_s\,dB_s
+K_T^{P}-K_t^{P},
\qquad P\text{-a.s. for every }P,
\tag{5}
\]

where `K^P` is nondecreasing and the usual minimality condition selects the smallest process dominating all conditional expectations.  Explicitly,

\[
Y_t
=\operatorname*{ess\,sup}_{P'\in\mathcal P(t,P)}
E^{P'}[\Phi\mid\mathcal F_t],
\qquad P\text{-a.s.}
\tag{6}
\]

which is exactly (3).  Equation (6), rather than a single dominated martingale law, is the actual representation.

For smooth cylindrical terminal data, functional Ito's formula verifies (4) directly.  Uniform approximation by cylindrical functionals and the stability of the nonlinear expectation extend the result to bounded uniformly continuous path payoffs.

## Scope

This actualizes the fully nonlinear path/2BSDE branch.  It is separate from the entropic pure drift game, which actualizes the nonconvex-gradient PPDE and quadratic BSDE branch.  Their product with the exact weighted noncompact filter gives a single deterministic-fast platform carrying all declared weighted/path representation types.
