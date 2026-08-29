# Referee Report

**Manuscript:** C2 — Cotangent Rigidity and Tangent Representations  
**Recommendation:** **Reject**  
**Standard applied:** Annals / Acta / Inventiones / JAMS  
**Review target:** pinned eleven-paper clean-main tree, SHA-256 `566335121763abaa7ed8ed2280a3b4345877777e8bedbd80f4eef0a6b48745e2`.

## Overall assessment

The manuscript is a synthesis paper claiming that one full Liouville path rate yields all mechanical contractions, pressure tangents, entropic rigidity, likelihood-ratio martingales, Girsanov/BSDE representations, and memory compatibility.

Several components are standard when their hypotheses hold. The manuscript neither establishes those hypotheses nor maintains a single parent rate across the advertised platforms. It also overstates differentiability of convex pressure and the mechanical determination of an entropic parameter.

## Major objections

### 1. “All finite mechanical contractions” is not a theorem about one rate

A contraction principle applies to continuous maps from one fixed probability model/rate space. The list includes:

- the periodic Sinai platform;
- an open-billiard impact model;
- a generalized baker map with Lebesgue symbolic law;
- proposed augmented heat-bath models.

The proof admits that “the parent rate changes with the physical platform.” Once the parent rate changes, this is not a contraction of one rate; it is only reuse of the same variational vocabulary. Items involving v6 and v7 therefore do not follow from A3’s Liouville path rate.

Continuity of each claimed observable map must also be proved in the selected path topology. Collision counts and impact statistics are generally discontinuous at grazing/singular trajectories.

### 2. The coboundary quotient is underspecified

The proposition uses \(F-G=c+U-U\circ\Theta_t\) without specifying the class of \(U\), whether \(t\) is fixed, or the closed linear span used in the quotient. As noted in A3, the union over varying times need not be a linear subspace.

For invariant measures a correctly defined time coboundary has zero mean, and its integrated finite-horizon contribution is a boundary term. That standard fact does not validate the manuscript’s undefined quotient.

### 3. Unique maximizing phase does not imply the stated second derivative

A unique maximizer can yield a first directional derivative of a convex pressure under compactness/continuity assumptions. It does not by itself yield twice differentiability or a Green–Kubo covariance formula.

Absolute convergence of the covariance series at the base phase is not sufficient. One needs differentiable dependence of the equilibrium law on the potential—typically a spectral perturbation theorem on an appropriate Banach space—and control of the observable class. The proof’s phrase “differentiate the variational pressure on its exposed smooth branch” assumes the result.

### 4. The subdifferential identification needs the correct dual space

On \(C_b\) over a noncompact path space, the Banach dual contains finitely additive functionals, not only countably additive probability measures. The equality
\[
\partial Q(\Psi)=\mathcal M(\Psi)
\]
therefore requires a carefully chosen locally convex topology/function class and compactness theorem. It is not automatic from a variational formula.

### 5. Entropic rigidity is quoted outside its precise hypotheses

Kupper–Schachermayer-type rigidity results require specific assumptions on the probability/filtration structure, law invariance or law determination, continuity/Fatou properties, relevance, and strong time consistency. The manuscript replaces these by informal prose.

More importantly, even if exponential utility is the only admissible nonlinear certainty equivalent, its parameter is not fixed by the mechanical Lagrange multiplier. The paper itself says the axioms do not choose \(\vartheta\), then declares \(\vartheta=\theta\) on a “calibrated” ray. That equality is a calibration convention, not a consequence of the rigidity theorem or Liouville dynamics.

### 6. The likelihood-ratio martingale is elementary; the diffusion representation is conditional

For bounded \(F\),
\[
M_t=\frac{E[e^F\mid\mathcal F_t]}{E[e^F]}
\]
is indeed a uniformly integrable martingale and defines a terminal tilt. This is a general probability identity.

To identify it with
\[
\mathcal E\!\left(\int\theta\sigma^\top Du\,dW\right)
\]
one must already have a Markov diffusion contraction, a sufficiently smooth log-Laplace value \(u\), martingale representation, and integrability such as Novikov/Kazamaki. The quadratic BSDE likewise needs terminal/running-data assumptions and a specified sign convention. None follows from the deterministic billiard path rate.

### 7. “Memory compatibility” proves no equality

Saying that Mori–Zwanzig operators, history kernels, and tilted martingales are constructed under the same prepared law is bookkeeping. It does not prove that the operator memory kernel equals, determines, or is recoverable from the nonlinear history generator. A genuine compatibility theorem would state a commutative diagram or an identity with domains and conditional projections.

### 8. The entire paper inherits A3 and A4

The full path rate, phase law, history generator, and short-memory contraction used here are not established in those papers. C2 cannot close the series by restating them.

## Editorial recommendation

**Reject.** The manuscript is a conceptual survey of desired relations, not a proved cotangent-rigidity theorem. It should not be submitted independently unless one central representation result is formulated on a single platform and proved with complete functional-analytic hypotheses.
