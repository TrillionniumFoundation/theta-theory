# Technical note: verification of the actual entropic path game

Consider

\[
dX_s=(u_s+v_s)ds+dW_s
\]

with payoff to the maximizer

\[
J_{t,\omega}(u,v)
=\mathbb E\left[
\Phi(X_{[0,T]})
+\int_t^T
\left(-\frac\mu2u_s^2+\frac\nu2v_s^2\right)ds
\right].
\tag{1}
\]

Controls are progressively measurable with finite quadratic energy.  Let

\[
c=\frac1{2\mu}-\frac1{2\nu}
\]

and let `U` be the bounded path value defined by the entropic formula in `FINAL_ADDENDUM_ENTROPIC_PATH_ACTUAL.md`.

## Theorem V-ENTROPIC-GAME-VERIFY

The lower and upper values of (1) coincide with `U`.  In every smooth cylindrical approximation the saddle feedback is

\[
u_s^*=\frac{\partial_\omega U(s,X)}{\mu},
\qquad
v_s^*=-\frac{\partial_\omega U(s,X)}{\nu}.
\tag{2}
\]

### Proof

Write `p=partial_omega U`.  Functional Ito's formula and

\[
\partial_tU+\frac12\partial_{\omega\omega}^2U+cp^2=0
\]

give a drift contribution

\[
-cp^2+p(u+v).
\]

Adding the running payoff and completing squares yields

\[
\begin{aligned}
&-cp^2+pu+pv-\frac\mu2u^2+\frac\nu2v^2\\
&\qquad
=-\frac\mu2\left(u-\frac p\mu\right)^2
 +\frac\nu2\left(v+\frac p\nu\right)^2.
\end{aligned}
\tag{3}
\]

For arbitrary `u`, choosing `v=v*` makes (3) nonpositive.  For arbitrary `v`, choosing `u=u*` makes it nonnegative.  Integrating, localizing the martingale and using the bounded terminal condition proves

\[
J(u,v^*)\le U(t,\omega)\le J(u^*,v).
\]

Thus `(u*,v*)` is a pure saddle and both game values equal `U`.

For a bounded uniformly continuous path payoff, approximate it uniformly by smooth cylindrical functionals.  The exponential formula is stable under uniform approximation; the values and the completed-square inequalities pass to the limit.  This supplies the actual path-space game verification without assuming classical differentiability of the final payoff.

## Consequences

- the pure saddle is not merely a pointwise Hamiltonian certificate;
- the path DPP, PPDE, entropic evaluation and quadratic BSDE describe the same actual value;
- the argument remains valid for negative `c` because the bounded terminal payoff keeps the exponential transform finite.
