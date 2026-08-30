# Referee Report

**Manuscript:** D1 — Deterministic Theta Contractions  
**Recommendation:** **Reject**  
**Standard applied:** Annals / Acta / Inventiones / JAMS  
**Review target:** pinned eleven-paper clean-main tree, SHA-256 `566335121763abaa7ed8ed2280a3b4345877777e8bedbd80f4eef0a6b48745e2`.

## Overall assessment

This final paper claims to close the deterministic hard-sphere hierarchy by identifying the first derivative of path pressure with the biased Boltzmann law, the Hessian with fluctuating Boltzmann covariance, the convex dual with the dynamic action, and Gaussian contractions with Girsanov/BSDE formulas.

The first displayed “pressure tangent hierarchy” has a basic scaling error. The remaining claims are either inherited from unproved earlier papers or are generic stochastic-calculus statements not derived from hard spheres.

## Major objections

### 1. The second-derivative formula misses the large-deviation speed

For a finite-volume scaled pressure
\[
Q_\varepsilon(\Theta)
=\frac1{\mu_\varepsilon}
\log E\exp\{\mu_\varepsilon\Theta\},
\]
differentiation gives
\[
DQ_\varepsilon(\Theta)[F]=E_{\Theta,\varepsilon}[F],
\]
but
\[
D^2Q_\varepsilon(\Theta)[F,G]
=\mu_\varepsilon\,
\operatorname{Cov}_{\Theta,\varepsilon}(F,G).
\]

The manuscript writes the Hessian as the unscaled covariance. That is dimensionally and mathematically wrong unless the symbols \(F,G\) have been rescaled in an unstated way. In the Boltzmann–Grad limit, the Hessian is an asymptotic covariance per unit speed, or equivalently the covariance of the \(\sqrt{\mu_\varepsilon}\)-fluctuation field—not the ordinary covariance of macroscopic observables under a limiting law.

This missing factor is central because the paper uses the Hessian to identify the fluctuating Boltzmann equation.

### 2. “Exposed phase” is insufficient for second differentiability

An exposed/unique phase may give a first subgradient. It does not imply analyticity or a Hessian. Passing finite-volume derivatives through the Boltzmann–Grad limit requires uniform derivative bounds and convergence of tilted cumulants on a complex/source neighborhood. Those are not proved for the collision-marked theory.

### 3. The deterministic hierarchy depends on false or unproved inputs

- B1’s microcanonical fixed-parameter log-Laplace transfer is false.
- B2’s actual-collision marked LDP is unproved.
- B3’s unique cotangent theorem is false as stated.
- B4’s kinetic nonlinear semigroup is not constructed.
- C1’s controlled closure is inconsistent.

A final “combine the preceding papers” proof cannot repair these defects.

### 4. Entropic rigidity again does not mechanically fix the parameter

The classification of certain law-invariant strongly time-consistent certainty equivalents, under precise assumptions, selects an affine/exponential form. It does not identify the exponential coefficient with a kinetic Lagrange multiplier. The paper’s “calibrated” equality is a modelling choice.

### 5. The listed “universal contractions” are not contractions of one theorem

Brownian tagged-particle limits require a separate near-equilibrium scaling and theorem. Heat-bath energy exchange requires a different mechanical platform. “Freezing all but one particle” is not a contraction of the Boltzmann–Grad \(N\)-particle LDP and does not produce a Sinai billiard or baker map without a new limiting construction.

The paper correctly labels some as “typed limiting models,” but then includes them in a closure theorem without proving the limits.

### 6. The Girsanov and BSDE theorem is disconnected from hard-sphere dynamics

For a given diffusion and an admissible drift tilt, the stochastic exponential and quadratic BSDE are standard. To call this the Gaussian tangent of the kinetic canonical likelihood ratio, the authors must prove convergence of the finite hard-sphere likelihood ratios jointly with the fluctuation field, identify the limiting Cameron–Martin drift, and establish uniform integrability.

No such likelihood-ratio convergence theorem appears. Boundedness/integrability of \(u\), the filtration, terminal data, and the BSDE solution class are also unspecified.

### 7. There is no independent final theorem

After correcting the covariance scale and removing unsupported contractions, D1 is a short summary of earlier intended results. A closure paper cannot be accepted when it adds no proof and the dependencies are open.

## Editorial recommendation

**Reject.** The headline derivative hierarchy is incorrectly normalized, and the claimed deterministic-to-diffusive representations are not derived. The paper should be deleted as a standalone submission; a corrected hierarchy diagram could appear in an introduction after the underlying theorems are actually proved.
