# Revision-Round Referee Report — GPT-5.6 Pro

**Manuscript:** C2 — *Path-Space Cotangent Rigidity, Universal Contractions, and Tangent Representations*  
**Editorial standard:** *Annals of Mathematics*, *Acta Mathematica*, *Inventiones Mathematicae*, or *Journal of the AMS*  
**Recommendation:** **Reject**  
**Reviewed source:** `main@ae2fdc16bf1ad4a6b58cca6020a7b8b61236e2ad`, manuscript blob `7c573e1c23ebc409c892b4815b9b3510ce9b78e8`  
**Revision provenance:** no revised C2 manuscript is materialized on the repository's discoverable eleven-paper revision ref; the controlling `main` source is reviewed.

## Overall assessment

The manuscript attempts to synthesize the single-particle path-LDP papers into a universal cotangent and representation theory. It combines contraction principles, path coboundaries, pressure derivatives, entropic rigidity, likelihood-ratio martingales, Girsanov and BSDE formulas, and compatibility with Mori–Zwanzig memory.

Several individual observations are standard and correct when their hypotheses hold. The synthesis theorem is not. The paper changes physical platforms and parent rate functions while continuing to advertise contractions of one full rate; it assumes pressure smoothness from uniqueness; it uses an undefined coboundary quotient and an unspecified dual space; and it presents generic martingale or diffusion identities as consequences of the deterministic Sinai path rate. The whole paper also inherits the unproved A3/A4 interfaces.

## Major objections

### 1. The “universal contractions” are not contractions of one rate

A contraction principle applies to a continuous map from one fixed family of probability laws and one fixed rate space. The paper lists:

- the periodic Sinai platform;
- an open-billiard impact model;
- a generalized baker map with Lebesgue branch law; and
- augmented heat-bath or energy-transfer systems.

The proof explicitly says that “the parent rate changes with the physical platform.” Once the parent changes, the result is not a contraction theorem from one rate; it is a statement that similar variational notation can be reused on different models.

The abstract and final closure theorem should not claim that one Liouville empirical-path rate produces all these theories. At most, each platform may have its own rate and its own separately proved contractions.

### 2. Continuity of the asserted mechanical contractions is not proved

Even on a fixed billiard platform, collision counts, impact frequencies, and singular path statistics are generally discontinuous at grazing or multiple-collision trajectories. The theorem assumes a continuous affine map \(C\), but it does not verify that the listed observables define such maps in the physical path topology.

A contraction theorem for these observables requires either continuity on the finite-rate support or an exponentially good approximation. Merely listing the observable does not satisfy the contraction principle.

### 3. The coboundary quotient remains undefined

The proposition uses

\[
F-G=c+U-U\circ\Theta_t
\]

without specifying the function class for \(U\), whether \(t\) is fixed, the topology of closure, or the closed linear span. The union over varying times need not be a linear subspace.

A genuine cotangent quotient must be defined as a quotient of an explicit locally convex function space by a precisely specified closed linear subspace. Otherwise the quotient may fail to be a vector space or Hausdorff, and phrases such as “the same cotangent direction” have no mathematical meaning.

### 4. A unique maximizing phase does not imply a pressure Hessian

Under compactness and continuity, a unique maximizer may identify a first directional derivative or subgradient. It does not imply twice differentiability, smooth dependence of the phase, or a Green–Kubo covariance formula.

Absolute convergence of the covariance integral at the base law is not enough. One needs differentiable response of the equilibrium law under perturbations, normally obtained from a spectral perturbation theorem on a specified Banach space, with control of the path-potential class. The proof's instruction to “differentiate the variational pressure on its exposed smooth branch” assumes the smooth branch that the theorem is supposed to establish.

### 5. The subdifferential identification uses an unspecified and potentially wrong dual

The paper writes

\[
\partial Q_R(\Psi)=\mathcal M(\Psi)
\]

for a pressure on bounded continuous functions over a noncompact path space. In the Banach dual of \(C_b\), finitely additive functionals can appear; the continuous dual is not automatically the space of countably additive probability measures.

To identify subgradients with path laws, the paper must choose a topology/function space whose dual is the desired measure class and prove tightness/compactness of maximizing phases. This functional-analytic step is absent.

### 6. Entropic rigidity does not mechanically determine the coefficient

The manuscript now correctly states that the axioms do not determine \(artheta\) and that other values are external valuation parameters. That is an improvement. The subsequent “first-principles branch” still identifies \(artheta=	heta\) merely because terminal work is measured in dual units on a calibrated ray.

Units ensure dimensional compatibility, not equality of parameters. The equality remains an additional modeling calibration. It is not derived from the rigidity theorem or the mechanical path LDP.

### 7. The likelihood-ratio martingale is generic; Girsanov and BSDE require a separate diffusion theorem

For bounded \(F\),

\[
M_t=
\frac{E[e^F\mid\mathcal F_t]}{E e^F}
\]

is a uniformly integrable martingale. This is a universal conditional-expectation identity and does not require an empirical-path LDP.

To identify it with

\[
\mathcal E\left(\int\theta\sigma^T Du\,dW\right)
\]

one must first prove a scalar diffusion contraction, Markov sufficiency, regularity of \(u\), a martingale representation in the selected filtration, and Novikov/Kazamaki-type integrability. The quadratic BSDE also needs a terminal/running-data class and a well-posed solution space. None follows from A3's deterministic path-rate statement.

### 8. “Memory compatibility” is only common construction under one law

The paper observes that the regularized Mori–Zwanzig family, history kernel, and tilted martingale are all built under the same prepared law. This is bookkeeping. It does not prove an identity relating the operator memory kernel to the nonlinear history generator or likelihood-ratio tangent.

A compatibility theorem should state a commutative diagram or equality with domains, projections, and conditional operators. The current proof merely says that the objects share a probability law.

### 9. The final closure theorem inherits A3 and A4

The full physical path rate, phase laws, history generator, and short-memory diffusion used here are not established in A3/A4. A synthesis paper cannot close those interfaces by repeating their intended consequences.

### 10. The manuscript conflates distinct tangent levels

A pressure Hessian, a central-limit covariance, a diffusion generator, a Girsanov density, and a BSDE driver live on different state spaces and scaling limits. The paper places them in one chain without proving the convergence maps between those levels. “Tangent representation” is not a substitute for a theorem.

## Status of prior objections

The revision more clearly admits platform changes and says that diffusion/BSDE formulas require a justified contraction. These are welcome truth-boundary improvements. They simultaneously confirm that the advertised “one rate” and “universal representation” claims are not established. The coboundary, differentiability, and dual-space problems remain unchanged.

## Required reconstruction

Choose one physical platform and one central theorem. Define the path-potential space, closed coboundary subspace, pressure domain, and dual measure topology. Prove first and second differentiability from a concrete spectral theorem. Any diffusion, Girsanov, or BSDE representation must then be derived through a separate scaling-limit theorem.

## Editorial recommendation

**Reject.** The paper is a conceptual map of desired correspondences across different models and limits, not a proved universal cotangent theorem.
