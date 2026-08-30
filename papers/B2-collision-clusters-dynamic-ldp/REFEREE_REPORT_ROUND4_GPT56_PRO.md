# Round-Four Independent Referee Report — GPT-5.6 Pro

**Manuscript:** B2 — *Collision-Marked Trajectory Clusters and Joint Dynamic Large Deviations for Deterministic Hard Spheres*  
**Editorial standard:** *Annals of Mathematics*, *Acta Mathematica*, *Inventiones Mathematicae*, or *Journal of the AMS*  
**Recommendation:** **Reject**  
**Reviewed revision:** `revision/round4-referee-positive-closure-11paper-2026-08-30@cbee394d6ee33db471b63420131314bd05909a0f`  
**Controlling module:** `ROUND3_POSITIVE_CLOSURE.tex`, blob `0efaf76e05ffe1f32c0a19fcd3aa7a9e07ae0715`

## Overall assessment

The revision has corrected the collision orientation, removed the fictitious-new-label interpretation of recollisions, and reorganized the logic so that the grand-canonical marked expansion precedes B1. It also recognizes that a full entropy action requires real-source continuation beyond one small complex chart.

The load-bearing all-contact estimate remains unproved. The purported uniform first-cycle transversality exponent is not justified for arbitrarily deep ancestral chains, and the “forgetful” surgery for later recollisions is incompatible with deterministic scattering because deleting a collision changes every subsequent velocity and contact. The real-source continuation also provides shorter existence times as the source grows, which is insufficient to dualize to the full entropy action on one fixed horizon. Consequently neither the marked pressure nor the claimed good joint LDP has been established.

## Major objections

### 1. The uniform witness exponent does not follow from finitely many local variable types

The first-cycle lemma considers arbitrary connected creation forests and arbitrary ancestral depth. The transverse Jacobian minor is a composition of free-flight and collision derivatives along the exclusive ancestral chains. Although each local variable is of one of finitely many *types*, the composed analytic functions form an infinite family whose degree, oscillation, number of factors, and order of vanishing can grow with the number of labels and collisions.

The proof invokes “the one-dimensional sublevel estimate for a nonzero analytic function” and then chooses one positive exponent `alpha` independent of the label number. Nonzero analyticity alone does not give a uniform Łojasiewicz exponent or uniform lower bound on the analytic norm. A sequence of nonzero analytic minors can vanish to arbitrarily high order.

To obtain a uniform power, the authors would need a quantitative transversality theorem for the full collision genealogy, with constants stable under arbitrary composition. No such theorem is stated or proved.

### 2. The regular witness coarea count is dimensionally unclear

The collision condition imposes that a two-dimensional transverse relative position vanish to radius `epsilon`. The manuscript speaks of “coarea in the scalar/angular witness and the remaining transverse root coordinate” and derives `epsilon^{1-alpha/4}` before weakening it.

The variables, dimensions, and Jacobian determinant are not specified. A scalar witness cannot by itself resolve a two-dimensional disk constraint without another genuinely free coordinate whose conditional density and independence must be controlled. In a general ancestral forest that second coordinate may already be fixed by prior contacts.

The asserted relative activity power is therefore not derived from a valid coarea formula.

### 3. The degenerate strata are not uniformly negligible

Small relative velocity and grazing can be estimated, but the “vanishing analytic minor” sector is treated by the same nonuniform analytic sublevel claim. Simultaneous contacts and changes of chronological cell can accumulate combinatorially with the label number. Absorbing the finite local witness list into `C^k k!` does not control the possible deterioration of the geometric exponent.

The lemma is precisely the new theorem required to extend tree estimates to all actual contacts; it cannot be accepted as a sketch.

### 4. The forgetful surgery for later recollisions is not a valid map of trajectories

After the first cycle contact, the proof says one may “forget” a later contact, identify the adjacent chronological cells, and preserve Gaussian activity because reflection has unit velocity Jacobian.

Deleting a hard-sphere collision does not merely remove a codimension-one face. It changes the two outgoing velocities. All subsequent free flights and collisions of both particles, and potentially of their descendants, change. The original post-collision trajectory is not mapped to a creation-forest trajectory by simply identifying two cells. The multiplicity, Jacobian, and even the terminal state of such a surgery are not controlled.

Unit Jacobian of the reflection map is irrelevant to the fact that the future trajectory is different. A legitimate recollision surgery must rebuild the entire future pseudo-trajectory and quantify all resulting bad sets. The displayed recursion for `Z_{m+1}` is asserted rather than derived from such a map.

### 5. The all-contact exponential ledger therefore does not follow

The theorem's source derivatives and uniform cyclic-sector `epsilon^alpha` gain depend entirely on the two preceding lemmas. Since neither the uniform witness power nor the later-contact surgery is proved, the majorant

\[
\exp\{CTe^{r+u}\}
\]

has no established microscopic basis. In particular, positive collision sources can reward trajectories with repeated recollisions, so this is not a harmless extension of an unmarked tree bound.

### 6. The Hamilton--Jacobi identification assumes the desired factorization

The proof singles out the “last collision” of a limiting connected tree and says the two remaining rooted subtrees are independent. This is true for ideal collision trees after the cyclic sector has been removed. It is not a proof that the deterministic microscopic marked cumulant converges normally to that tree series; that is exactly what the unproved all-contact theorem was meant to establish.

The HJ theorem is therefore downstream of the missing geometric estimate.

### 7. Real-source continuation is not sufficient for a full entropy dual on a fixed horizon

For each source bound `R`, the manuscript produces a time `T_R` satisfying a condition of the form

\[
\Delta e^{CR}\ll1.
\]

Thus `T_R` generally decreases rapidly as `R` grows. A full entropy action for an arbitrary finite-action collision density is obtained by truncating

\[
q=d\Gamma/dA_f
\]

and using sources `log q_M`, whose norm tends to infinity as `M` tends to infinity. To prove the LDP on one fixed time interval `T`, one needs the pressure for all these truncation sources on that same `T`.

The theorem does not provide

\[
\inf_R T_R>0.
\]

Its nested regularity statement only covers sources while the corresponding biased hierarchy remains in a chosen bounded-rate class; it does not show that the truncation sequence needed for an arbitrary finite-entropy path exists on the original horizon.

Consequently the convex dual of the available source domain is not proved to be the full relative-entropy action.

### 8. The “positive collision right inverse” is far too strong for its proof

The manuscript claims a continuous linear map taking every smooth distributional balance defect in a weighted `W^{-1,1}` norm to a signed collision current absolutely continuous with respect to `A_m`, with an `L^infinity` density bound.

A finite incidence matrix on a velocity partition can invert finitely many cell averages. It does not provide an exact right inverse for an infinite-dimensional transport/collision divergence, uniformly under refinement, with the asserted Radon-density estimate. Spatial localization, velocity interpolation, conservation constraints, and compatibility with the nonlinear reference `A_m` all require substantial analysis absent from the proof.

Therefore the balance-preserving regularization lemma, and hence the lower-bound density theorem, is not established.

### 9. Exponential compact containment again uses an unspecified positive velocity source

The containment proof refers to a “positive velocity source” in the cluster theorem. The admissible path-source growth and the exact weighted topology are not specified at this point. A Maxwellian law supports positive quadratic exponential moments only below the Gaussian exponent, not arbitrary weights. The proof must state the precise Lyapunov function and show the biased source remains inside the analytic chart.

### 10. The upper-bound argument is incomplete

Normal convergence for finite collections of sources plus exponential compact containment can support an upper bound only after fixing a convergence-determining dual class and proving the limiting cumulant on that class. The manuscript jumps from source convergence to the full closed-set upper bound and then pointwise dualizes. The topology, density of tests, and exponential approximation of unbounded collision entropy directions are not supplied.

### 11. The microcanonical theorem inherits B1's coefficient gap

Even if the grand-canonical theorem were complete, transfer to the primitive shell uses B1's finite-volume coefficient theorem, which remains unproved. Thus the final prepared joint LDP has two independent open gates.

## Status of previous objections

The orientation and exchange quotient are now correctly stated, and the logical B2-GC -> B1 -> B2-MC order removes the earlier circularity. These are genuine improvements. They do not prove the new all-contact geometry or the full source domain.

## Minimum viable reconstruction

A credible paper should first prove a narrowly scoped theorem: normal convergence of a marked cumulant for actual contacts in one fixed small complex source ball. This requires a complete recollision surgery theorem with explicit genealogical constants.

A full LDP should be deferred until the authors separately prove:

1. real-source pressure on a horizon independent of source truncation;
2. exponential compact containment in a specified topology;
3. a balance-preserving action-dense regularization theorem; and
4. the microscopic lower bound under the biased deterministic law.

## Recommendation

**Reject.** The revision presents a sophisticated blueprint, but its central all-contact estimate and full-LDP lower bound are not proved. These are the paper, not auxiliary details.