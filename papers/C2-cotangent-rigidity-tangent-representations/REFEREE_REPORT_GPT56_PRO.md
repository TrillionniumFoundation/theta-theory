# Independent Referee Report — GPT-5.6 Pro

**Manuscript:** C2 — Cotangent Rigidity and Tangent Representations  
**Editorial standard:** *Annals of Mathematics*, *Acta Mathematica*, *Inventiones Mathematicae*, or *JAMS*  
**Recommendation:** **Reject**  
**Review object:** SHA-256-pinned eleven-paper source archive `566335121763abaa7ed8ed2280a3b4345877777e8bedbd80f4eef0a6b48745e2`

## Executive assessment

The paper is a synthesis claiming that one full Liouville path rate generates all finite mechanical contractions, pressure tangents, cotangent quotients, entropic rigidity, likelihood-ratio martingales, diffusion/Girsanov/BSDE representations, and memory compatibility.

The organizing vocabulary is coherent, but the theorem is not. The manuscript changes the underlying physical platform—and therefore the parent probability laws and rate functions—while continuing to speak of contraction from one rate. It also overstates what uniqueness of a phase implies about second differentiability, uses an undefined coboundary quotient, and treats generic martingale/stochastic-calculus identities as consequences of the deterministic path LDP. The entire construction additionally inherits A3 and A4, neither of which proves its load-bearing theorem.

## Major mathematical objections

### 1. The advertised contractions do not come from one parent rate

The examples include a periodic Sinai billiard, an open impact model, a generalized baker map, and proposed heat-bath/augmented platforms. A contraction principle applies to a continuous map from one fixed family of laws and one fixed rate space. Once the physical platform changes, the parent rate changes.

The manuscript itself effectively concedes this by saying that the parent rate depends on the platform. At that point “all contractions of one rate” becomes only a reuse of variational notation. No theorem transfers A3's Sinai path rate to the baker, open-billiard, or heat-bath models.

Even within one platform, collision counts and impact statistics are generally discontinuous at grazing or singular paths. Continuity or exponential approximation of every contraction map must be proved in the selected topology.

### 2. The coboundary quotient is not defined

The relation

\[
F-G=c+U-U\circ\Theta_t
\]

is written without specifying the class of \(U\), whether \(t\) is fixed, the ambient norm/topology, or the closed linear span used in the quotient. The union of coboundary sets over varying times need not be a vector subspace.

A valid cotangent space must quotient by a precisely defined closed linear subspace of an explicitly chosen function space. Otherwise the quotient may fail to be linear or Hausdorff, and all later statements about unique classes are ill-posed.

### 3. A unique maximizing phase does not imply a pressure Hessian

Under suitable compactness and continuity, a unique equilibrium phase may identify a first directional derivative or subgradient. It does not imply twice differentiability, analytic dependence of the phase, or a Green–Kubo formula.

Absolute summability of the covariance at the base phase is not sufficient. One needs differentiable response of the equilibrium law to perturbations, normally supplied by a spectral perturbation theorem on a specified Banach space, together with control of the observable class. The phrase “differentiate the exposed smooth branch” assumes the desired smooth branch.

### 4. The subdifferential is asserted in the wrong/unspecified dual space

On \(C_b\) of a noncompact path space, the Banach dual contains finitely additive functionals, not merely countably additive probability measures. Therefore

\[
\partial Q(\Psi)=\mathcal M(\Psi)
\]

is not automatic. The paper must choose a locally convex topology/function class for which the continuous dual is the desired measure space and prove compactness/tightness of maximizing phases.

Without that work, the subgradient and cotangent identifications are formally suggestive but not rigorous.

### 5. Entropic rigidity is quoted outside a complete hypothesis set

Classification results for strongly time-consistent law-invariant certainty equivalents require precise assumptions: the probability/filtration setting, law invariance or law determination, Fatou/continuity properties, relevance/strict monotonicity, normalization, and the exact form of time consistency. The manuscript substitutes informal prose.

More importantly, even a valid rigidity theorem selects a functional form, not the numerical coefficient. Identifying the exponential coefficient with a mechanical Lagrange multiplier is a calibration convention. The paper alternately acknowledges and suppresses this distinction.

### 6. The likelihood-ratio martingale is generic; the diffusion representation is conditional

For bounded \(F\),

\[
M_t=rac{E[e^F\mid\mathcal F_t]}{E[e^F]}
\]

is a uniformly integrable martingale defining a terminal tilt. This is a general identity and does not require a billiard LDP.

To identify it with a stochastic exponential involving \(\sigma^T Du\), one must already have:

- a proved diffusion contraction;
- Markov sufficiency;
- sufficient regularity of the log-Laplace value;
- a martingale representation theorem in the chosen filtration; and
- Novikov/Kazamaki-type integrability.

The quadratic BSDE similarly needs a specified sign convention, terminal/running data, and a solution class. None follows from A3.

### 7. “Memory compatibility” is only co-location under one law

Constructing Mori–Zwanzig objects, history kernels, and tilted martingales under the same prepared law is bookkeeping. A compatibility theorem would require a commutative diagram or equality relating the operator memory kernel to the nonlinear history generator, with domains and conditional projections. The manuscript proves no such relation.

### 8. The paper inherits the missing A3/A4 interfaces

The full path rate, phase selection, universal pressure, and history generator used throughout are not established in A3/A4. Restating their intended consequences in a synthesis paper cannot close them.

### 9. Mechanical and stochastic tangent levels are conflated

A deterministic path-rate Hessian, a central-limit covariance, a diffusion generator, a Girsanov drift, and a BSDE driver live on different scaling limits and state spaces. The manuscript presents them as successive notational views without proving the limit maps between them. “Typed” labels do not substitute for convergence theorems.

## Dependency assessment

C2 is not an independent closure theorem. Its principal objects are conditional on A3/A4, and several claimed representations additionally require platform-specific diffusion/homogenization results absent from the series.

## Minimum viable reconstruction

Select one physical platform and one representation theorem. Define the primal path space, observable topology, closed coboundary subspace, pressure domain, and dual measure space. Prove first and second differentiability from a concrete spectral theorem. Any diffusion/Girsanov/BSDE corollary must then be derived through a separate proved scaling limit.

## Recommendation

**Reject.** The manuscript is a conceptual survey of desired correspondences, not a theorem. It changes parent models, assumes differentiability, and imports unproved path/history interfaces while advertising a universal closure.
