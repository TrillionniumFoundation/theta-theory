# Independent Referee Report — GPT-5.6 Pro

**Manuscript:** B4 — Nonlinear Kinetic Semigroups  
**Editorial standard:** *Annals of Mathematics*, *Acta Mathematica*, *Inventiones Mathematicae*, or *JAMS*  
**Recommendation:** **Reject**  
**Review object:** SHA-256-pinned eleven-paper source archive `566335121763abaa7ed8ed2280a3b4345877777e8bedbd80f4eef0a6b48745e2`

## Executive assessment

The paper seeks to pass from exact finite hard-sphere conditional log-Laplace towers to an infinite-dimensional Hamilton–Jacobi semigroup on kinetic densities, then identify a microcanonical diagonal limit, an endogenous-theta expectation, and a Gaussian risk-sensitive contraction.

The exact tower is a universal conditional-expectation identity. It does not prove that the empirical density is a Markov sufficient state, that microscopic history disappears under exponential tilts, or that an infinite-dimensional nonlinear semigroup exists. The limiting HJ equation is not defined on a complete state/function space and no generator-convergence, compact-containment, or comparison theorem is established. The proposed microcanonical identification also relies directly on B1's false fixed-saddle transfer, while the collision-work extension relies on B2's unproved marked theory.

## Major mathematical objections

### 1. A full-history tower does not imply an autonomous density semigroup

For any filtered probability space,

\[
\frac1\mu\log E[e^{\mu F}\mid\mathcal F_s]
\]

satisfies a nonlinear tower. If the state is the complete history, this produces a tautological Markov representation. At finite \(\varepsilon\), the empirical one-particle density generally does not determine all recollision and correlation information.

Passing from the history state to a density-only semigroup requires a loss-of-memory theorem uniform under the relevant exponential tilts. The paper proves no such theorem. It simply changes state spaces between the exact identity and the limiting equation.

### 2. The limiting Hamilton–Jacobi problem is not mathematically specified

The manuscript announces local uniform convergence to a “unique mild solution” of

\[
\partial_t U+\mathbb H\!\left(f,\frac{\delta U}{\delta f},0\right)=0.
\]

It does not define:

- the metric state space of densities;
- the admissible moment/velocity weights;
- the class of terminal functionals;
- the functional derivative or test-function core;
- the nonlinear semigroup and meaning of mild solution;
- the topology of local uniform convergence;
- compact containment/exponential tightness; or
- a comparison principle.

Without these data, “unique mild solution” is not a theorem statement.

### 3. Invoking the Feng–Kurtz program does not verify its hypotheses

A nonlinear-generator method requires convergence on a separating core, exponential compact containment, identification of upper and lower Hamiltonians, and well-posedness/comparison for the limiting HJ equation. The manuscript checks none of these.

A short-time cluster expansion for analytic sources may identify a local cumulant. It does not automatically give semigroup convergence for arbitrary terminal functionals or a global large-deviation principle. Statements such as “stability completes the argument” merely rename the missing analysis.

### 4. The microcanonical diagonal limit is invalid because B1's error is extensive

The proof divides the claimed microcanonical/canonical log-Laplace difference by \(\mu_\varepsilon\). B1 asserts that the numerator is \(o(\mu_\varepsilon)\), but for an allowed time-zero source aligned with a conditioned macro observable the difference is order \(\mu_\varepsilon\).

No diagonal choice of shrinking windows removes a nonzero limiting convexity gap. Therefore the prepared microcanonical semigroup has not been identified with the fixed-parameter grand-canonical semigroup.

The correct limiting object must retain a source-dependent constrained saddle.

### 5. The collision-work semigroup depends on B2

The collision-source Hamiltonian and its dynamic action are not established by the current marked cluster/LDP paper. B4 cannot treat them as a proved generator merely because their formal expression is natural.

### 6. The theta “derivation” conflates conjugate preparation and valuation

A derivative \(I_G'(a)\) is the canonical field enforcing a prepared value of an observable \(G\). Defining

\[
\theta^{-1}\bigl(Q(\theta G+\theta F)-Q(\theta G)\bigr)
\]

with the same scalar creates an entropic functional by construction. It does not prove that mechanics forces the coefficient used to value an arbitrary \(F\). The paper must distinguish a mechanically conjugate field from an externally chosen certainty-equivalent parameter.

### 7. The Gaussian generator is a formal expansion, not a hard-sphere limit

The quadratic risk-sensitive diffusion term is standard once a diffusion and its covariance are given. Deriving it from the nonquadratic hard-sphere semigroup requires a central-limit/homogenization scaling, convergence of the nonlinear generators, control of tilted likelihood ratios, and a comparison theorem for the limiting PDE.

No such scaling theorem is proved. Formal second-order expansion of a candidate Hamiltonian is not enough.

### 8. There is no independent theorem after dependencies are removed

The finite tower is generic probability. The density closure is assumed. The HJ convergence is not constructed. The microcanonical transfer is false. The collision extension is conditional on B2. The theta identification is interpretive. What remains cannot support a standalone top-journal paper.

## Dependency assessment

B4 is a convergence hub built on B1 and B2. Since those inputs fail, B4 cannot be repaired locally. Moreover, even with corrected inputs, the paper would still need an independent infinite-dimensional semigroup/comparison theorem.

## Minimum viable reconstruction

A viable paper should first define a weighted density state space and a nonlinear semigroup on a separating class of cylinder functionals, prove upper/lower generator convergence and compact containment, and establish comparison for the limiting HJ equation. Microcanonical preparation must enter through a constrained source-dependent pressure, not a fixed-saddle replacement.

## Recommendation

**Reject.** The exact history tower is tautological, while the claimed density semigroup, HJ limit, microcanonical transfer, and Gaussian contraction are unproved or false under the stated inputs.
