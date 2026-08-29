# Deterministic first-principles to theta-expectation: closure report

## Controlling theorem chain

\[
\text{area-preserving deterministic map}
\to
\text{Lebesgue physical measure}
\to
\text{mechanical current LDP}
\to
\theta=I'(a)
\to
\text{microcanonical/canonical equivalence}
\to
\text{deterministic driven map}
\to
\text{physical diffusion}
\to
\text{excess-pressure DPP}
\to
\text{physical theta-HJB}.
\]

## Exact formulas

Base current preparation:

\[
a_0=2/5,\qquad w(a_0)=(1/10,1/5,3/10,2/5).
\]

Rate and conjugate parameter:

\[
I(a)=\frac{1+a}{2}\log\frac{1+a}{7/5}
+\frac{1-a}{2}\log\frac{1-a}{3/5},
\]

\[
\theta(a)=I'(a)=\frac12\log\frac{3(1+a)}{7(1-a)}.
\]

Collision and physical coefficients:

\[
C(a)=\operatorname{diag}(1-a,6(1+a)),\qquad
\bar\tau(a)=\frac{3-a}{2},
\]

\[
A_{\rm phys}(a)=C(a)/\bar\tau(a).
\]

Physical theta-HJB:

\[
-u_t=c+b\cdot Du+\frac1{2\bar\tau(a)}C(a):D^2u
+\frac{\theta(a)}{2\bar\tau(a)}Du^TC(a)Du.
\]

## New tools

1. Quantitative finite-window microcanonical equivalence.
2. Exact deterministic driven-map realization of the canonical path tilt.
3. Canonical excess-pressure identity for theta-expectation.
4. Exponential random-horizon replacement in physical time.
5. Risk-sensitive saddle-envelope theorem with optimizer-response correction.
6. Direct cash-additive certainty-equivalent rigidity theorem.

## Honest boundary

The macro current `a` is a preparation condition.  A deterministic equation
alone cannot select which atypical macro current an experimenter prepares.
Once `a` is fixed, however, the probability law, conjugate theta, driven map,
stochastic limit, and nonlinear expectation are all determined in this model.

The package is internally closed in this exact full-cover collision scope and
awaits independent specialist review.
