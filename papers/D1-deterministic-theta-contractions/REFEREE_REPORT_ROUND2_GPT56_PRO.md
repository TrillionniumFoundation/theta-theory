# Revision-Round Referee Report — GPT-5.6 Pro

**Manuscript:** D1 — *Rigidity and Universal Contractions of Hard-Sphere Kinetic Cotangents*  
**Editorial standard:** *Annals of Mathematics*, *Acta Mathematica*, *Inventiones Mathematicae*, or *Journal of the AMS*  
**Recommendation:** **Reject; remove as a standalone paper**  
**Reviewed source:** `main@ae2fdc16bf1ad4a6b58cca6020a7b8b61236e2ad`, manuscript blob `72e6d6729e9fa0cb36356e6fdbad189191bba9c6`  
**Revision provenance:** no revised D1 manuscript is materialized on the repository's discoverable eleven-paper revision ref; the controlling `main` source is reviewed.

## Overall assessment

D1 is intended as the closure paper for the hard-sphere half of the series. It asserts that one path pressure has the biased Boltzmann law as first derivative, the fluctuating Boltzmann covariance as Hessian, the dynamic action as convex dual, and Girsanov/BSDE formulas as Gaussian contractions.

The first theorem remains incorrectly normalized or, at minimum, fatally underspecified. The proof says to differentiate a normalized finite-volume exponential tilt, for which the second derivative is the large-deviation speed times covariance, not ordinary covariance. The remaining claims depend on the false or unproved B1–B4/C1 chain and add no independent proof. D1 should not exist as a standalone submission until those upstream theorems are established.

## Major objections

### 1. The pressure Hessian formula omits the large-deviation speed

For a finite-volume scaled pressure

\[
Q_\varepsilon(\Theta)
=
\frac1{\mu_\varepsilon}
\log E\exp\{\mu_\varepsilon\Theta\},
\]

one obtains

\[
DQ_\varepsilon(\Theta)[F]
=E_{\Theta,\varepsilon}[F],
\]

but

\[
D^2Q_\varepsilon(\Theta)[F,G]
=
\mu_\varepsilon\,
\operatorname{Cov}_{\Theta,\varepsilon}(F,G).
\]

The manuscript states

\[
D^2Q_T(\Theta)[F,G]
=
\operatorname{Cov}_{\mathbb P^\Theta}(F,G)
\]

and says this follows by differentiating the normalized finite-volume tilt and passing to the limit. These formulas are not compatible unless \(F,G\) have been rescaled by \(\mu_\varepsilon^{-1/2}\), or “covariance” is explicitly defined as the limiting asymptotic covariance per unit speed. Neither convention is stated.

The correct Hessian is the covariance of the \(\sqrt{\mu_\varepsilon}\)-fluctuation field, not the ordinary covariance of an unscaled macroscopic observable under a limiting law. This normalization is central to the claimed fluctuating-Boltzmann identification.

### 2. Uniform source analyticity is asserted, not proved

Passing first and second finite-volume derivatives through the Boltzmann–Grad limit requires convergence on a source neighborhood and uniform derivative bounds, typically including complex analyticity or strong real estimates. B2 has not proved the collision-source-decorated cumulant convergence needed for this step.

The phrase “pass to the limit using uniform source analyticity” imports the conclusion of the missing marked-cluster theorem. Exposedness or uniqueness of a phase does not supply a Hessian.

### 3. The closure chain is broken at every load-bearing stage

The final theorem says to combine the deterministic microcanonical path law, collision-marked LDP, cotangent geometry, nonlinear semigroup, controlled typing, and tangent contractions. But:

- B1's fixed-\(f_a^0\) transfer is false for an allowed time-zero source;
- B2 does not prove the actual-collision marked cluster expansion or local lower bound;
- B3's unique \((p,\psi)\) cotangent is destroyed by an unquotiented representation gauge;
- B4 does not construct the density-state nonlinear semigroup or comparison theorem;
- C1's final Isaacs equation solves an adaptive game rather than the declared one-time preparation game.

A synthesis theorem cannot turn invalid inputs into a closed theory.

### 4. Entropic rigidity still does not identify the mechanical coefficient

The paper correctly says that the axioms do not determine the numerical value of \(	heta\). It then says that mechanical preparation fixes the coefficient because the path I-projection identifies a multiplier. This identifies a conjugate preparation field, not necessarily the coefficient of a certainty equivalent for arbitrary terminal work.

The equality is a calibrated modeling choice. It is not a theorem of entropic rigidity or hard-sphere mechanics.

### 5. The listed “universal contractions” are separate models and limits

A tagged-particle Brownian limit requires a specific near-equilibrium scaling and invariance principle. A heat-bath energy-transfer ray requires an augmented mechanical model. Freezing all but one particle does not automatically turn the Boltzmann–Grad gas into a Sinai billiard or baker map.

The manuscript labels some of these as typed limiting models, which is appropriate, but then includes them in the same closure theorem without proving the limiting maps. Similar notation does not make them contractions of one theorem.

### 6. The Girsanov and BSDE statements are generic diffusion facts

For an already given diffusion and admissible drift, the stochastic exponential and quadratic BSDE are standard. To call them the Gaussian tangent of the deterministic hard-sphere likelihood ratio, the paper must prove joint convergence of:

- the finite-particle fluctuation field;
- the canonical likelihood-ratio martingales;
- their quadratic variations; and
- the tilted laws,

with uniform integrability and identification of the limiting Cameron–Martin drift. None of this is shown.

The filtration, integrability assumptions, terminal data, regularity of the value function, and BSDE solution class are also unspecified.

### 7. The rate/action/Hessian triangle is stated across incompatible levels

The convex dual of a path pressure, its local Hessian, and the covariance of a Gaussian fluctuation can be related under differentiability, exponential tightness, and a valid local quadratic expansion on one state space and scaling. D1 moves between microscopic path measures, kinetic densities, collision flows, tagged diffusions, and heat-bath rays without proving the transitions.

A diagram of intended relations is not a closure theorem.

### 8. There is no independent theorem in D1

After correcting normalization and deleting inherited claims, D1 is a short summary of the intended B-series hierarchy. It proves no new estimate, compactness theorem, convergence result, or functional-analytic statement. A top journal will not accept a closure paper whose dependencies remain open and whose main displayed formula is incorrect.

## Status of prior objections

The manuscript now emphasizes that long-time source-decorated LDPs and adaptive collision control are not claimed. This truth boundary is appropriate. It does not fix the Hessian normalization or the upstream theorem failures. The decisive prior objections remain unchanged.

## Required reconstruction

D1 should be removed as a standalone paper. After a correct constrained preparation theorem, actual-collision LDP, full-gauge cotangent theorem, kinetic semigroup, and fluctuation convergence are proved, a correctly normalized hierarchy can appear as a theorem or roadmap section in the principal paper. The notation must distinguish ordinary covariance from asymptotic covariance per unit large-deviation speed.

## Editorial recommendation

**Reject; remove as a standalone paper.** The headline tangent hierarchy is incorrectly normalized, the stochastic representations are not derived from hard spheres, and the paper contributes no proof capable of closing the broken dependency chain.
