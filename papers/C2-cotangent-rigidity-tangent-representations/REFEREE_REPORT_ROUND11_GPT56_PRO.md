# Independent Referee Report — Round Eleven

**Manuscript:** C2 — Cotangent Rigidity and Tangent Representations  
**Editorial standard:** *Annals of Mathematics*, *Acta Mathematica*, *Inventiones Mathematicae*, or *JAMS*  
**Recommendation:** **Reject**  
**Reviewed branch:** `revision/round11-referee-positive-closure-11paper-2026-08-31@e81cbf57624d21be23ee9d982a1255c076363761`  
**Reviewed source:** `revision/round11-referee-final/C2_FULL_PRESSURE_FUNCTIONAL_EIGENBUNDLE.tex` (Git blob `6d33212e23602c08d4e6872f2d3e8f86e0b3ba66`)

## Executive assessment

The manuscript correctly distinguishes equality of one scalar pressure from equality of the full perturbed pressure functional, avoids infinite-path Radon–Nikodym trivializations, and separates spectral and resolved projections. These are genuine improvements.

The principal functional-analytic claims remain ill-typed or unproved. The dual of a quotient vector space cannot be a set of probability measures; the platform-wide Livšic step is unavailable for the hard-sphere process; and a finite-dimensional Riesz frame does not transport the graph domain of the full unbounded Doob generator. The memory and optional-projection theorems therefore do not follow.

## Major mathematical objections

### 1. The stated continuous dual is not a vector space

The continuous dual of

\[
\mathscr A_W/\mathscr N_{\rm inv}
\]

is a vector space. The theorem identifies it with “the compactly generated set of invariant Radon probabilities.” Probability measures are not closed under scalar multiplication or subtraction. The correct dual object, if the topology is chosen appropriately, is a space of invariant signed Radon measures; probabilities form only a normalized positive slice.

This is a basic typing error in the headline cotangent theorem.

### 2. The weighted Hahn–Banach/Cesàro argument lacks its topology theorem

On a noncompact weighted strict topology, one must prove that every continuous separator is countably additive, that its time averages remain uniformly weighted-tight, and that the limit preserves the pairing. The claimed Lyapunov estimate “for every Dirac initial state” is not established by A1/A2/B2, and the Jordan parts of a limiting functional require a precise invariant signed-measure representation.

### 3. Full-pressure rigidity requires a platform Livšic theorem

For a mixing finite-state subshift, equality of equilibrium Gibbs measures for Hölder potentials can imply a constant-plus-coboundary relation. The manuscript applies this conclusion across all platforms, including the hard-sphere/Boltzmann path law. No periodic-orbit Livšic theorem or Markov Poisson-range theorem is proved there.

Differentiating the perturbation identity may identify the same equilibrium linear functional. It does not by itself turn the potential difference into a pathwise temporal coboundary in the declared source norm.

### 4. The finite Riesz frame does not transport the full generator domain

The frame \(e_i(\eta)=\Pi_\eta v_i\) only trivializes the finite-dimensional leading spectral range. It provides no conjugacy of the complementary infinite-dimensional transfer space or of the unbounded Doob generator \(L_\eta^D\). Nevertheless the memory proof states that a common graph domain follows after conjugation by that finite frame.

A finite matrix acting on a Riesz eigenspace cannot identify the graph domains of the full generators.

### 5. Regularity loss remains relevant to the projector derivatives

Avoiding Picard iteration is sensible, but higher derivatives of \(\Pi_\eta\) still consume strong regularity. The theorem must specify, for every order, the source and target levels and prove that the finite-frame Gram matrices and dual pairings are differentiable there. “Fresh strong regularity” is not a fixed bundle theorem.

### 6. The resolved Hilbert bundle is assumed nondegenerate

A finite family of physical observables can become linearly dependent modulo constants, conservation laws, or phase null directions. Positivity of a correlation Gram matrix does not give a uniform lower eigenvalue. The chart on which \(R_\eta\) is differentiable must be constructed after quotienting all null modes, not merely declared regular.

### 7. The memory derivative still requires an unproved unbounded-operator perturbation theorem

Differentiating

\[
(z-L_\eta^D)^{-1}
\]

requires a common domain or a graph-bounded derivative \(DL_\eta^D\). Correlation differentiability alone does not supply either. Descriptor modes and Smith–McMillan language do not fix the domain problem.

### 8. The optional-projection theorem is much stronger than the stated inputs

Stable convergence of finite-history likelihood martingales and their optional projections requires convergence of filtrations/conditional kernels, uniform integrability of the likelihoods, and joint convergence with the driving martingale. Identifying the limit as a Girsanov exponential additionally needs a martingale representation theorem and admissibility. A quadratic BSDE needs a specified driver, terminal condition, and solution class.

A4 does not prove these interfaces in the current revision.

### 9. The contraction chain rule is correct but not novel enough to carry the paper

The exact source identity and ordinary state chain rule are useful typing corrections. They are elementary once the domains are separated and do not compensate for the missing rigidity, eigenbundle, and stochastic-representation theorems.

## Status of earlier objections

The scalar-pressure counterexample is explicitly addressed, and the finite spectral frame avoids the previous impossible Kato evolution on one regularity-losing Banach space. The replacement theorems still overreach from a finite eigenspace to an infinite generator and from equilibrium equality to platform-wide cohomology.

## Minimum reconstruction

Choose one platform and one fixed transfer/graph space. Prove the signed-measure duality, the appropriate zero-variance/cohomology theorem, and a graph-resolvent perturbation theorem there. The Girsanov/BSDE layer should be a separate corollary after a proved diffusion-filtration limit.

## Recommendation

**Reject.** Several typing repairs are correct, but the central cotangent dual, cohomology, memory, and stochastic representation theorems remain unproved or incorrectly formulated.