# Referee Report — Round 18 (Independent Harsh Review)

**Paper:** B1 — *Microcanonical Preparation and Exponential-Scale Ensemble Transfer for Deterministic Hard Spheres*  
**Version reviewed:** `revision/round17-referee-positive-closure-11paper-2026-09-01@d13b48757f85d9ec1c6998f89c861845094891fa`  
**Controlling source:** `ROUND17_POSITIVE_CLOSURE.tex` (`B1_DIRECT_CANONICAL_COEFFICIENT.tex`)  
**Date:** 1 September 2026  
**Editorial recommendation:** **REJECT**  
**Present mathematical status:** The interacting exact-number Fourier majorant and shell coefficient theorem are not proved.

## 1. Overall assessment

This revision makes a genuine and welcome correction: it works with the positive exact-`N` hard-sphere phase-space integral and does not interpret signed connected polymer activities as independent random components. The intended logical order—grand-canonical B2 pressure, then a B1 coefficient theorem, then microcanonical B2—is also the correct direction in which to avoid an obvious circularity.

The replacement argument nonetheless fails at several essential points. Most decisively, the high-frequency proof uses a number of integrations by parts growing linearly with `N`, whereas the only regularity estimate stated for the interacting conditional density is `C^4`. This is an internal contradiction in the proof. In addition, the canonical saddle, selected-cell decomposition, Fourier decay in position-type directions, shell uniformity, and thermodynamic transfer are not established.

## 2. Decisive mathematical objections

### 2.1. [FATAL] The scaling regime and comparison with an independent one-particle law are not stated rigorously

The proof of `lem:r17-b1-saddle` uses

\[
N\varepsilon^3=O(\varepsilon)
\]

when bounding the forbidden volume. No joint limit relating `N`, `\varepsilon`, the volume, and the Boltzmann–Grad activity is stated in the theorem. In the usual hard-sphere scaling, the excluded volume estimate and the normalization of the exact-`N` ensemble depend on the physical volume and density. The displayed `O(\varepsilon)` cannot be assessed without these definitions.

More importantly, the source `H_N` is a path/contact functional of the deterministic many-particle flow. Conditional on previously exposed initial particles, this source can change discontinuously when a new initial datum creates, removes, or reorders a collision. It is not a bounded product perturbation of independent one-particle kernels. The claim

\[
\left\|N^{-1}D_\lambda^2\log Z_{\varepsilon,N}-D^2q_1(\lambda)\right\|\le C\varepsilon
\]

therefore does not follow from a forbidden-volume estimate plus a grand-canonical connected remainder. A canonical, fixed-`N`, source-differentiated cluster estimate uniform in the conditioning order is required and is not supplied.

### 2.2. [MAJOR, potentially fatal] The global saddle theorem exceeds the inverse-function argument

The theorem asserts a unique real multiplier for every target `a` in a compact subset of the interior one-particle mean image, uniformly in the interacting exact-`N` law and source. A local inverse-function theorem near one multiplier does not prove global surjectivity or uniqueness over the entire compact target set. One needs strict convexity on the full multiplier chart, properness/steepness or boundary behavior of the gradient, and proof that the interacting mean image contains the prescribed compact set.

The constraint vector also includes cell observables `\chi_1,\ldots,\chi_m`. Depending on their definition, these may satisfy an affine relation such as a partition-of-unity constraint. The asserted uniformly positive covariance on all of `\mathbb R^d` is then impossible unless redundant coordinates are removed or the theorem is stated on the appropriate quotient tangent space. No rank condition is given.

Analytic dependence on an infinite-dimensional path/contact source is not obtained from a finite-dimensional inverse-function theorem unless the exact Banach source space and uniform operator derivatives are specified.

### 2.3. [FATAL] Lemma `lem:r17-b1-cell` does not prove the selected-cell structure under an interacting dynamic source

The proof treats sequential cell occupation as if each fresh cell had a uniformly positive success probability conditional on the exterior. Hard-core exclusion alone is velocity independent, but the tilted dynamic source couples particles through their future collision graph. It can strongly alter conditional weights, and a bounded Radon–Nikodym factor on the entire configuration does not yield near-product conditional densities with uniformly controlled mixed derivatives.

The claimed estimate

\[
\|\log R\|_{C^4}\le C\varepsilon n_{\rm sel}
\]

is attributed to the grand-canonical B2 connected bound. The paper never derives a canonical conditional version of this estimate after fixing the exterior and all selected positions. Nor does it specify whether the `C^4` norm includes mixed derivatives across different selected velocities; that distinction is crucial for the later repeated integration by parts.

The exceptional-event statement is also unsupported. An affine-span condition for `C` does not automatically furnish a global full-rank coarea chart whose conditional density has a uniform `W^{d+3,1}` norm after hard-core conditioning and dynamic tilting.

### 2.4. [FATAL, direct internal contradiction] The proof uses `s+cN` derivatives after proving only four

The high-frequency part of `thm:r17-b1-fourier` says that on the typical event one performs `s+cN` integrations by parts, distributed among the selected particles, and obtains

\[
C(1+|u|)^{-s-cN}.
\]

Each integration differentiates the interacting conditional amplitude. Lemma `lem:r17-b1-cell` controls only four derivatives of `\log R`, and the grand-canonical input is stated to have source derivatives through order four. No derivative estimates of order growing with `N` appear anywhere.

Distributing the integrations among different variables does not solve the problem: mixed derivatives of the interaction factor are still generated, and even repeated differentiation in one variable requires corresponding smoothness. A `C^4` density cannot support `O(N)` integrations by parts. This alone invalidates the global Fourier majorant and every theorem depending on it.

### 2.5. [FATAL] Velocity integration cannot control all Fourier directions of the declared constraint vector

The constraint vector is

\[
C=(v,|v|^2/2,\chi_1,\ldots,\chi_m).
\]

The cell observables `\chi_j` are position variables. A Fourier vector dominated by the `\chi` coordinates has phase derivative zero in every velocity coordinate. The claim that for every unit direction there is a velocity coordinate `\xi` with

\[
|\partial_\xi(e\cdot C)|\ge c_*
\]

is therefore false unless the `\chi_j` themselves depend on velocity or the Fourier domain is restricted. The manuscript calls the `U_j` “velocity-position boxes” but later integrates only selected velocities and states that hard-core exclusion is velocity independent.

Position integration by parts would create hard-core boundary terms and moving cell-boundary terms, which are precisely the difficult parts. No such analysis is given. Consequently the compact-annulus damping and high-frequency decay do not cover all directions in `\mathbb R^d`.

### 2.6. [FATAL] The exceptional-event regularity is weaker than the decay exponent required by the theorem

The exceptional event is assigned a conditional density with `W^{d+3,1}` regularity. The theorem demands a tail exponent `s>d+4`. Standard Fourier decay obtained by integration by parts is limited by the available Sobolev derivatives. `W^{d+3,1}` does not justify arbitrary `s>d+4`; it does not even provide the number of derivatives explicitly used in the display. This mismatch is independent of the `C^4` contradiction on the typical event.

### 2.7. [MAJOR] The central and compact-frequency estimates are not derived for the dependent canonical law

Uniform covariance bounds and a fourth-cumulant estimate can yield Gaussian decay on a sufficiently small neighborhood, but the proof does not establish the required cumulant bounds for the exact interacting law uniformly in `N`, `\varepsilon`, source, and saddle. On a fixed compact annulus, integrating one selected velocity at a time gives a factor less than one only under a uniform conditional nonlattice estimate for every residual Fourier direction. Dependence through `R` and the position-only directions prevent the claimed simple product argument.

The phrase “absorbing the `C\varepsilon N` interaction factor into the exponent” additionally requires a specified regime and a strict inequality between the independent damping rate and the interaction error. Neither is quantified.

### 2.8. [FATAL] The geometric shell theorem is overclaimed

The proof of `thm:r17-b1-coefficient` applies a Gaussian smoothing argument to an arbitrary family of domains with uniformly `C^2` boundary, bounded Gaussian perimeter, and inradius satisfying `\sqrt N\rho_\varepsilon\to\infty`. Several issues remain:

1. the Fourier theorem needed for the density approximation is unproved;
2. the displayed boundary error contains a corrupted factor `h_\varepsilon/\rho_\varepsilon` without a derivation from the stated perimeter bound;
3. multiplicative relative error is not uniform when the Gaussian mass of the shell tends to zero faster than the absolute inversion error;
4. arbitrary translated or anisotropic shells can leave the central regime where the cumulant expansion is valid;
5. the claim that “point boxes” follow is false for continuous constraint coordinates: exact points have probability zero and have no positive inradius.

The theorem must distinguish lattice from continuous coordinates, central from moderate/large-deviation targets, and absolute from relative error regimes.

### 2.9. [FATAL] The pressure limit and microcanonical transfer are assumed rather than extracted

The notation `Q^N(H,\lambda)` is introduced as “the exact-number limiting pressure obtained from the grand-canonical B2-GC pressure by coefficient extraction.” That extraction is the principal theorem that B1 is supposed to prove. The manuscript does not establish the thermodynamic limit, uniformity in the source, equivalence of coefficient and saddle asymptotics, or interchange of source derivatives with the limit.

Even with a central shell coefficient, passage to the exact microcanonical pressure requires precise normalization and conditioning windows, and the Schur-complement Hessian formula requires differentiability of the limiting saddle. These are not consequences of the preceding five-page outline.

## 3. Dependency consequences

B1 is downstream of B2-GC and upstream of B2-MC. Its coefficient theorem is also used by B3 and C1. Because the full Fourier majorant and shell theorem fail, the microcanonical transfer claimed in B2, the constrained covariance in B3, and the prepared observation kernels in C1 are unavailable.

## 4. Minimum requirements for reconsideration

A future submission would need:

1. a complete statement of the hard-sphere scaling and exact canonical ensemble;
2. a canonical source-dependent cluster/conditional-density theorem, not an appeal to a grand-canonical remainder;
3. a rank-correct saddle theorem on the true constraint space;
4. a Fourier decomposition handling both velocity and position constraints, including hard-core boundary terms;
5. derivative bounds compatible with the actual number of integrations by parts—either analytic/Gevrey estimates or a different high-frequency strategy;
6. a mixed lattice/continuous local coefficient theorem with precise window regimes and relative-error hypotheses;
7. a rigorous source-uniform coefficient extraction and thermodynamic saddle limit.

## 5. Recommendation

**Reject.** The positive exact-`N` reformulation is the correct conceptual direction, but the proof contains a direct regularity contradiction (`C^4` versus `O(N)` integrations by parts) and does not control position-type Fourier directions. The local coefficient and microcanonical transfer results are therefore not established.