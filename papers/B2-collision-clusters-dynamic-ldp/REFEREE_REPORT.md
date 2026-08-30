# Referee Report

**Manuscript:** B2 — Collision Clusters and Dynamic LDP  
**Recommendation:** **Reject**  
**Standard applied:** Annals / Acta / Inventiones / JAMS  
**Review target:** pinned eleven-paper clean-main tree, SHA-256 `566335121763abaa7ed8ed2280a3b4345877777e8bedbd80f4eef0a6b48745e2`.

## Overall assessment

The manuscript attempts a genuinely nontrivial extension of the hard-sphere Boltzmann–Grad theory: it adds an empirical measure of actual binary collisions to the particle-path observable, asserts a source-decorated real-trajectory cluster expansion, and derives a joint density/collision-flow LDP with Poisson relative-entropy action.

The cited Annals hard-sphere work proves short-time fluctuation and large-deviation results for the empirical density under regularity assumptions. A joint LDP for the actual collision point process is not obtained merely by attaching a factor to every tree edge. The present manuscript provides no proof of the new combinatorics, topology, exponential tightness, or lower bound. The result is therefore not established.

## Major objections

### 1. “Put \(e^\psi\) on every created edge” does not represent all actual collisions without proof

Real hard-sphere trajectories contain collision trees, recollisions, overlaps, and correlations between collision marks and the entire trajectory history. The empirical collision measure counts actual collisions, including events that are not simply independent creation edges in a limiting Boltzmann tree.

The manuscript states that recollision and overlap graphs remain in the same negligible class after adding bounded collision weights. This is precisely what must be proved. Positive collision sources favor trajectories with many collisions and can alter the summability constants and the relative importance of exceptional graphs. A one-line replacement \(T\mapsto T e^{C\|\psi\|}\) is not a derivation of the marked cluster norm.

A valid proof must define the marked polymers, show how every microscopic collision contributes exactly once with the chosen orientation, and re-establish all geometric recollision estimates uniformly in the source ball.

### 2. There is a sign/orientation inconsistency in the collision mark

With the manuscript’s convention
\[
\omega=(x_i-x_j)/\varepsilon,
\]
an incoming contact satisfies
\[
(v_i-v_j)\cdot\omega<0,
\]
because the interparticle distance is decreasing. The text labels incoming collisions by a positive dot product while later using \(((v-v_*)\cdot\omega)_+\). One can choose the opposite normal convention, but then the collision rule and exact balance must be rewritten consistently. For an empirical measure of unordered collisions, the quotient by particle exchange and normal reversal must also be specified.

This affects the claimed exact microscopic balance and the reference intensity \(A_f\).

### 3. Analytic convergence of cumulants is not a path-space LDP

Even if the marked log-Laplace functional converged analytically for a local source class, the joint LDP would still require:

- a precise topology for density paths and collision measures;
- exponential tightness at speed \(\mu_\varepsilon\);
- identification of all finite-dimensional Hamiltonians;
- a comparison principle or exposed-trajectory argument;
- local upper and lower bounds with controllable approximation;
- treatment of singular collision measures and boundary points of the source domain.

The proof says these follow by “the same mechanism” as the density-only theorem. That is not acceptable for a new observable whose topology and dual variable are different.

### 4. The relative-entropy action is only a formal convex dual at this stage

The identity
\[
\sup_\lambda\{q\lambda-a(e^\lambda-1)\}=a\ell(q/a)
\]
is elementary. It does not prove that deterministic hard-sphere collision counts have an asymptotically Poissonian local cost conditional on a density path.

The weak kinetic balance is necessary but may not be sufficient to characterize the closure of feasible microscopic collision flows. Exchange symmetry, pre/post-collisional involution, conservation constraints, integrability in velocity, and compatibility with the chosen incoming orientation all require inclusion in the state space and rate domain.

### 5. The initial-rate statement is incomplete and inherits B1’s false transfer

Conditioning on finitely many moments does not make all off-minimizer empirical initial measures infinitely costly. The conditional initial empirical measure should have a nontrivial relative-entropy rate on the constraint set, with zero only at the information projection. The manuscript does not define this rate fully.

More importantly, it invokes B1’s fixed-parameter microcanonical-to-grand-canonical log-Laplace transfer, which is false for arbitrary extensive sources. Thus even a correct grand-canonical marked LDP would not yield the stated microcanonical theorem.

### 6. The lower bound is the difficult part and is absent

The statement is restricted to a “regular biased-solution class,” but neither that class nor the controllability/invertibility of the tilted kinetic equation is defined. To prove a local lower bound one must construct microscopic tilts approximating a prescribed \((f,\gamma)\), control the Radon–Nikodym cost, and show concentration under the tilted deterministic dynamics. The manuscript merely cites formal Hamilton–Jacobi duality.

## Editorial recommendation

**Reject.** The collision-marked extension may be an interesting research direction, but the manuscript presently contains a proposed formula and a proof outline, not a theorem. It also depends on the false B1 preparation transfer.
