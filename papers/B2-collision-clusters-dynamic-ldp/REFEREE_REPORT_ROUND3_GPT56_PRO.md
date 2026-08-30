# Round-Three Referee Report — GPT-5.6 Pro

**Manuscript:** B2 — *Collision-Marked Trajectory Clusters and Joint Dynamic Large Deviations for Deterministic Hard Spheres*  
**Editorial standard:** *Annals of Mathematics*, *Acta Mathematica*, *Inventiones Mathematicae*, or *Journal of the AMS*  
**Recommendation:** **Reject**  
**Reviewed revision:** `revision/round3-full-positive-closure-11paper-2026-08-30@6a31720e5b0b6ab156b575f947596f9b66f56efe`  
**Controlling module:** `ROUND3_POSITIVE_CLOSURE.tex`, blob `74c0d4047e5bae2988f677690bc4fafc479826ca`

## Executive assessment

The revision fixes the contact-normal convention, defines the exchange quotient, separates the grand-canonical construction from the later microcanonical conditioning, and explicitly distinguishes creation edges from cycle/recollision contacts. These are necessary corrections.

The main theorem remains unproved. The all-contact cluster bound is inferred from one vaguely specified “first-cycle” tube estimate and then treats all later cycle contacts as if they carried ordinary bounded collision operators and an ordered-time-simplex factorial. In a deterministic trajectory graph, later recollisions are not independent collision integrations; their times and geometries are constrained by the same ancestral variables. The claimed generating bound does not follow.

Independently, the controlling paper proves complex normal convergence only on one small source ball and then claims a full joint LDP with the complete Poisson relative-entropy action. The dual of a small source ball is not that action. Finite-action collision densities require sources `log q` of arbitrarily large norm after regularization. The repository’s own hostile audit identified this exact defect and produced `B2_GLOBAL_SOURCE_LDP.tex`, but that file is not part of the controlling manuscript.

The actual-collision joint LDP is a genuinely new theorem beyond the cited density-only hard-sphere fluctuation/LDP results. It cannot be obtained by saying that the same mechanism applies.

## Improvements relative to the preceding circulation

1. The normal is now chosen as `omega=(x_j-x_i)/epsilon`, so incoming contact is consistently `(v_i-v_j)·omega>0`.
2. Each unordered contact is counted once and the exchange/pre-post quotient is explicit.
3. The construction order `B2 grand canonical -> B1 conditioning -> B2 microcanonical` removes the old formal circularity.
4. The paper no longer pretends that every recollision introduces a new particle label.
5. The desired rate is stated on a weighted density/collision space with an exact weak balance.

These repairs clarify the target. They do not prove it.

## Major mathematical objections

### 1. The “first-cycle geometric gain” is not a theorem at the stated uniformity

The lemma fixes all variables before the first cycle and asserts that one remaining deflection parameter is free and that the recollision condition confines it to a tube with gain `epsilon^alpha`, uniformly in the number of labels and the entire preceding genealogy.

No construction identifies this parameter for every possible first cycle. In a recollision graph, the two ancestral pseudo-trajectories may share several collision variables; the last effective parameter can be degenerate, lie at a grazing or simultaneous-collision singularity, or be constrained by earlier overlap conditions. The proof’s sentence “the last creation or clustering parameter which deflects one ancestral path” is not a measurable partition of the graph class and supplies no Jacobian lower bound.

A rigorous result needs a complete geometric case decomposition, a parametrization of each bad graph, nondegenerate coarea estimates, treatment of small relative velocities and grazing, and summability over the possible ancestral locations. The displayed split at `|v-v_*|=epsilon^{1/4}` is only one ingredient.

### 2. Later cycle contacts do not acquire an ordered-simplex factorial for free

After deleting the first cycle edge, the proof bounds the remaining `c-1` cycle occurrences by

\[
\frac{(CTe^{r+u})^c}{c!}.
\]

This is not justified. Creation collisions have a collision-coarea integration because a new particle position is integrated. A later contact between already connected trajectories generally has no new independent position variable. Its time is a deterministic function or constraint on existing variables, not an independently integrated point in an ordered simplex.

One cannot replace the missing geometric codimension of every later recurrence by the volume of a formal time simplex. The first-cycle gain may make the entire cyclic sector negligible in some established cluster schemes, but proving that requires a graph surgery theorem controlling the residual singular integrations. The manuscript does not provide one.

### 3. The all-contact derivative bound is therefore unsupported

The theorem claims normal convergence after any number of collision-source derivatives and identifies each derivative with an actual-contact factorial moment. Positive collision sources exponentially reward trajectories with many contacts, including recollisions. Without a valid all-cycle bound, there is no source-uniform majorant and no justification for termwise differentiation.

Marking every microscopic contact in the definition is not equivalent to proving that the marked cluster expansion converges.

### 4. A local complex source ball cannot yield the full entropy action

The controlling cluster theorem works only for `||(h,psi)|| <= r0`. The joint LDP theorem then dualizes over arbitrary collision densities and writes

\[
\int\ell(d\Gamma/dA_f)dA_f.
\]

For a regular pair with

\[
q=d\Gamma/dA_f,
\]

the exposing collision source is `log q` up to a gauge. Even when `q` is bounded above and below, its bound can be arbitrarily large across the finite-action domain. Approximating a general finite-entropy `q` by truncations `q_M` makes `||log q_M||` diverge.

The convex dual of pressure known only on a fixed small ball is a truncated support function, not the full Poisson entropy. The upper bound and lower bound both fail outside the local mean image.

### 5. The repository contains an unincorporated attempted repair

The internal hostile audit correctly demanded real-source continuation on every bounded source set and balance-preserving regularization. The branch contains

```text
revision/round3-rereview/B2_GLOBAL_SOURCE_LDP.tex
```

which proposes blockwise continuation and a collision right inverse. `main.tex` does not input it, and the active `ROUND3_POSITIVE_CLOSURE.tex` retains the small-ball proof. Therefore the publication candidate has not even materialized its own proposed response.

Moreover, the separate repair file contains several major new assertions—uniform conditional hierarchy charts, a positive collision right inverse, and action-dense regularization—that would themselves require full proofs.

### 6. The microscopic lower bound is not constructed

The proof says: tilt the initial activity and every actual contact by `(p,psi)`, observe that the first derivative is the target biased law, and use the second derivative plus compact containment for concentration.

For deterministic trajectories, this requires an exact normalized path-space change of measure and a theorem that the source-decorated finite system concentrates at the desired density/collision pair. Analyticity of a limiting cumulant near one source gives finite-dimensional moments; it does not automatically prove path-space exponential concentration, uniqueness of the biased hierarchy, or the lower bound in the weighted topology.

The asserted backward equation for `p`, regular recovery path, and compensating transport correction are not defined or estimated.

### 7. Exponential compact containment is only sketched

A positive velocity source controls a Gaussian-compatible quadratic weight locally, and a positive constant collision source controls total contact count if the marked pressure exists. To obtain compactness in the weighted path/collision space, one still needs:

- uniform velocity-tail estimates under the source family;
- a closed modulus-of-continuity criterion for density paths;
- tightness of collision locations and velocities;
- control of endpoint layers; and
- closure of exchange and pre/post symmetries.

The short proof does not establish these properties.

### 8. The Hamilton–Jacobi identification is asserted by tree rhetoric

“Remove the last collision and obtain two independent rooted subtrees” describes the formal Boltzmann tree recursion. It does not prove a unique analytic mild solution on a defined scale of Banach spaces, nor the differentiability required for the covariance hierarchy. The function spaces, loss of velocity weight, Picard norm, and time of existence are not stated with sufficient precision.

### 9. The microcanonical theorem inherits B1’s missing coefficient theorem

Even if the grand-canonical joint LDP were proved, the final transfer uses B1’s source-uniform shell coefficient. B1’s current safe-box proof has the wrong Boltzmann–Grad scaling. Thus the microcanonical rate is not available.

### 10. The cited literature does not contain the announced extension

The established short-time hard-sphere fluctuation/LDP and real-trajectory cluster results provide indispensable background for empirical particle distributions. The present paper adds the empirical measure of every actual collision and claims a full joint LDP and source-normal convergence. That is a new load-bearing theorem; it must be proved here rather than described as the “same mechanism.”

## Editorial recommendation

**Reject.** A potentially important paper lies in the actual-collision marked extension, but the current proof does not control the deterministic recollision graph and cannot derive a global entropy action from a local source chart. A viable reconstruction must first prove a source-uniform all-contact cluster theorem with a rigorous graph surgery, then extend real pressures to every bounded source required by entropy duality, and finally construct the weighted path-space lower bound. Only after that should B1 conditioning and the microcanonical joint LDP be added.