# Referee Report

**Manuscript:** B4 — Nonlinear Kinetic Semigroups  
**Recommendation:** **Reject**  
**Standard applied:** Annals / Acta / Inventiones / JAMS  
**Review target:** pinned eleven-paper clean-main tree, SHA-256 `566335121763abaa7ed8ed2280a3b4345877777e8bedbd80f4eef0a6b48745e2`.

## Overall assessment

The paper attempts to pass from finite deterministic hard-sphere log-Laplace towers to an infinite-dimensional Hamilton–Jacobi semigroup on kinetic densities. The exact conditional tower is a general identity. The kinetic semigroup limit, uniqueness of a mild solution, Markovian closure on the density state, and the microcanonical diagonal limit are not proved.

The paper relies simultaneously on B1’s false ensemble-transfer theorem and B2’s unproved collision-marked cumulant theory. It also invokes the Feng–Kurtz program without supplying any of the generator-convergence, compact-containment, or comparison hypotheses.

## Major objections

### 1. The finite-volume tower is tautological and does not imply a density semigroup

For any probability law and filtration,
\[
\mu^{-1}\log E[e^{\mu F}\mid\mathcal F_s]
\]
satisfies the nonlinear tower. This remains true on the complete history state. It does not show that the empirical density \(f\) is Markov, sufficient, or even an autonomous state at finite \(\varepsilon\).

Passing a history-space tower to a semigroup on densities requires a theorem that all memory not encoded by \(f\) disappears in the Boltzmann–Grad limit, uniformly under the exponential tilts. No such theorem is provided.

### 2. The kinetic Hamilton–Jacobi limit is undefined at the required level

The manuscript states local uniform convergence to the “unique mild solution”
\[
\partial_tU+\mathbb H(f,\delta U/\delta f,0)=0.
\]
It does not define:

- the metric/state space of densities;
- the class of terminal functionals \(\Phi\);
- the meaning of the functional derivative;
- a nonlinear semigroup or mild solution;
- the comparison principle guaranteeing uniqueness;
- the topology of local uniform convergence;
- compact containment/exponential tightness.

A cluster expansion for source functionals may identify a limiting cumulant on a small analytic class. It does not automatically yield a Hamilton–Jacobi semigroup for arbitrary terminal functionals.

### 3. Citing Feng–Kurtz is not verification

The nonlinear-generator approach requires convergence on a separating core, exponential compact containment, well-posedness of the limiting Hamilton–Jacobi equation, and matching initial conditions. The proof checks none of these. “Stability follows” and “local analytic well-posedness gives uniqueness” are placeholders.

The collision-work extension additionally depends on B2’s unproved marked Hamiltonian.

### 4. The preparation–semigroup diagonal limit inherits B1’s false theorem

The proof divides B1’s claimed \(o(\mu_\varepsilon)\) log-Laplace difference by \(\mu_\varepsilon\). But B1’s difference is generally order \(\mu_\varepsilon\) for an allowed source aligned with a conditioned macro observable. No diagonal choice of shrinking windows removes that discrepancy.

Thus the microcanonical kinetic semigroup has not been identified with the fixed-parameter grand-canonical one.

### 5. The “endogenous theta expectation” conflates two distinct choices

A derivative \(I_G'(a)\) is a Lagrange multiplier for preparing the path observable \(G\). Defining
\[
\theta^{-1}\bigl(Q(\theta G+\theta F)-Q(\theta G)\bigr)
\]
then produces an entropic functional with the same scalar by construction. Mechanics does not prove that every terminal work \(F\) must be valued with that parameter. The theorem should distinguish a canonical field from an external certainty-equivalent parameter.

### 6. The Gaussian generator is a formal contraction

The quadratic term
\[
\frac{\theta}{2}Df^\top A Df
\]
is standard for a risk-sensitive diffusion. Deriving it from the hard-sphere nonquadratic semigroup requires an actual central-limit/homogenization scaling, convergence of generators, and control of the exponential tilt. None is present.

### 7. The paper has no independent theorem after dependencies are removed

The exact tower is generic probability; the HJ limit is cited/assumed; the microcanonical transfer is false; the theta calibration is interpretive. This is not a standalone research contribution.

## Editorial recommendation

**Reject.** A valid paper would first construct a precise kinetic nonlinear semigroup and prove generator convergence/comparison on a defined state space. It would then derive, rather than assume, loss of history and the microcanonical constrained pressure.
