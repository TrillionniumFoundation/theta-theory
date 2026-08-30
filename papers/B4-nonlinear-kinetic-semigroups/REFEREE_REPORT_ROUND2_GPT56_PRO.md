# Revision-Round Referee Report — GPT-5.6 Pro

**Manuscript:** B4 — *Microcanonical Excess-Pressure Semigroups and Kinetic Theta-Generators*  
**Editorial standard:** *Annals of Mathematics*, *Acta Mathematica*, *Inventiones Mathematicae*, or *Journal of the AMS*  
**Recommendation:** **Reject**  
**Reviewed source:** `main@ae2fdc16bf1ad4a6b58cca6020a7b8b61236e2ad`, manuscript blob `3d009bd5925a904931cfaa0d267da261bab2d865`  
**Revision provenance:** no revised B4 manuscript is present on the repository's discoverable eleven-paper revision ref; the controlling `main` source is reviewed.

## Overall assessment

The manuscript aims to derive an infinite-dimensional nonlinear kinetic semigroup from finite deterministic hard-sphere path laws. It starts from an exact complete-history conditional log-Laplace tower, invokes a source-decorated Boltzmann–Grad cumulant limit, claims convergence to a kinetic Hamilton–Jacobi equation, passes microcanonical preparation through a diagonal limit, and then extracts scalar theta and Gaussian diffusion contractions.

The exact tower is correct but tautological. It does not imply density-state Markov closure. The limiting HJ problem is not defined at the level needed for a theorem, and the proof invokes the nonlinear-generator method without verifying its hypotheses. The microcanonical diagonal theorem directly imports B1's false fixed-saddle transfer, while the collision-work extension imports B2's unproved marked Hamiltonian. The paper therefore has no established independent theorem.

## Major objections

### 1. The microscopic tower is a general conditional-expectation identity

For any filtered probability law,

\[
\mu^{-1}\log E[e^{\mu F}\mid\mathcal F_s]
\]

satisfies the nonlinear tower. Retaining the complete conditional history produces an exact sufficient state by construction. This does not show that the empirical density \(f\) is Markov, autonomous, or sufficient at finite \(arepsilon\), nor that the history collapses to \(f\) under exponential tilts.

The paper changes from a complete-history state in the exact proposition to a density state in the limiting HJ equation without proving a uniform loss-of-memory or propagation-of-chaos theorem on the exponentially tilted source class.

### 2. The limiting Hamilton–Jacobi problem is not defined

The theorem asserts locally uniform convergence to a unique mild solution of

\[
\partial_tU+
\mathbb H\left(f,\frac{\delta U}{\delta f},0\right)=0.
\]

The manuscript does not define:

- the metric state space of densities;
- velocity/moment weights and compact-containment sets;
- the terminal-functional class;
- the functional derivative and test-function core;
- the nonlinear semigroup or meaning of mild solution;
- the topology of local uniform convergence;
- boundary conditions; or
- a comparison principle giving uniqueness.

Without these objects, the displayed equation is a formal target, not a theorem.

### 3. The nonlinear-generator framework is cited, not implemented

A Feng–Kurtz-type argument requires convergence of upper and lower nonlinear generators on a separating core, exponential compact containment, approximation of test functions, and comparison for the limiting HJ equation. None of these is checked.

A local analytic cluster expansion may identify cumulants for a small source class. It does not automatically yield semigroup convergence for arbitrary terminal functionals or a full viscosity/mild-solution theory. The phrases “stability follows” and “local analytic well-posedness gives uniqueness” merely name the missing analysis.

### 4. The preparation–semigroup diagonal limit is invalid

The proof invokes B1's assertion that microcanonical and fixed-\(f_a^0\) grand-canonical log-Laplace functionals differ by \(o(\mu_\varepsilon)\). For an allowed time-zero source aligned with a conditioned macro observable, the difference is order \(\mu_\varepsilon\). Dividing by \(\mu_\varepsilon\) leaves a nonzero limit.

No choice of shrinking windows or diagonal sequence removes this convexity gap. The limiting microcanonical nonlinear value must retain a source-dependent constrained saddle. Consequently the diagonal theorem, and every closure theorem using it, is false as stated.

### 5. The collision-work extension depends on B2's unproved theorem

The extended Hamiltonian with a collision source is not established by the current real-trajectory cluster paper. B4 cannot treat it as a proved nonlinear generator merely because it has the expected kinetic form. Topology, source-uniform recollision estimates, and the microscopic lower bound remain missing upstream.

### 6. The “endogenous theta expectation” is a calibration, not a mechanical necessity

A rate derivative \(I_G'(a)\) is the canonical field conjugate to a prepared observable \(G\). The paper then defines

\[
\theta^{-1}\{Q(\theta G+\theta F)-Q(\theta G)\}
\]

using the same scalar. This creates a calibrated entropic functional. It does not prove that every terminal work \(F\) must be valued with that coefficient. The distinction between a preparation field and a preference/valuation parameter remains essential.

### 7. The Gaussian generator is a formal contraction

The quadratic risk-sensitive diffusion generator is standard once a limiting diffusion, covariance, and smooth value function are already available. Deriving it from the hard-sphere nonquadratic semigroup requires a central-limit/homogenization scaling, convergence of likelihood ratios, uniform generator estimates, and comparison for the limiting PDE.

The manuscript states none of these results. A formal Taylor expansion of the collision exponential is not a deterministic hard-sphere diffusion theorem.

### 8. The references do not establish the exact theorem stated here

The cited deterministic hard-sphere results concern specific short-time empirical-measure fluctuation/LDP settings. The current paper claims an infinite-dimensional nonlinear semigroup on prepared conditional laws, with collision work and a microcanonical diagonal. Those additional state-space, preparation, and comparison results must be proved in this manuscript or imported through exact matching theorems. They are not.

### 9. No independent contribution remains after dependencies are removed

The finite tower is generic probability. The density closure is unproved. The HJ semigroup is undefined. The microcanonical transfer is false. The collision extension is conditional. The theta identification is interpretive. The Gaussian contraction is formal. This cannot support a standalone top-journal submission.

## Status of prior objections

The manuscript is careful not to declare finite conditioned laws Markov and identifies complete history as the exact state. This is a valid correction. The missing step is precisely the theorem from complete history to density-state kinetic semigroup, which remains absent. The B1 counterexample continues to invalidate the diagonal limit.

## Required reconstruction

A viable paper must first define a weighted density state space and nonlinear semigroup, prove microscopic upper/lower generator convergence and exponential compact containment, and establish a comparison principle for the limiting HJ equation. Microcanonical preparation must enter through a source-dependent constrained pressure. Collision work and Gaussian contractions should be added only after their separate microscopic convergence theorems exist.

## Editorial recommendation

**Reject.** The exact history tower is tautological, while every model-specific semigroup, preparation, collision, and Gaussian conclusion remains unproved or depends on a false upstream theorem.
