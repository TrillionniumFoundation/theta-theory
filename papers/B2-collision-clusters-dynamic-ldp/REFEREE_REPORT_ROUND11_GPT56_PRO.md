# Independent Referee Report — Round Eleven

**Manuscript:** B2 — Collision Clusters and Dynamic LDP  
**Editorial standard:** *Annals of Mathematics*, *Acta Mathematica*, *Inventiones Mathematicae*, or *JAMS*  
**Recommendation:** **Reject**  
**Reviewed branch:** `revision/round11-referee-positive-closure-11paper-2026-08-31@e81cbf57624d21be23ee9d982a1255c076363761`  
**Reviewed source:** `revision/round11-referee-final/B2_TRACE_AFFINE_FORK_SOURCE_EXHAUSTION.tex` (Git blob `5d98abfe897195203899ea445209592424e43d67`)

## Executive assessment

The Green formula no longer double-weights the normal trace, the true reflected future is retained, and the authors no longer hide depth loss by a QR reset. These are real corrections. The replacement “affine-fork” theorem is nevertheless false for the physical collision dynamics: tangential motion on a contact sphere changes the collision normal, reflected velocities, subsequent flight times, and later collision normals. The final surplus-position map is not a fixed affine map \(A\xi+b\) with depth-independent condition number. The entire recollision gain, source sewing, and LDP remain unsupported.

## Major mathematical objections

### 1. Tangential fork variables do not generate a rigid translated future

At a contact, the relative position is \(arepsilon\omega\). A tangential variation changes \(\omega\). The elastic reflection law

\[
v'=v-((v-v_*)\cdot\omega)\omega
\]

therefore changes at first order through \(D\omega\). All subsequent velocities, collision times, and collision normals change. One cannot translate a descendant subtree rigidly while preserving the creation collision unless the collision normal and outgoing velocities are frozen, which is not the physical hard-sphere map.

Thus the surplus relative position is generally a nonlinear composition of collision maps, not

\[
A(\omega_*)\xi+b
\]

with \(A\) independent of \(\xi\).

### 2. Specular reflection is not orthogonal on the relevant Jacobi fields

The velocity reflection at a fixed normal is orthogonal. The derivative of the billiard collision map with respect to position includes curvature, flight-time, and normal-variation terms. These are precisely the terms responsible for focusing/defocusing and grazing singularities. The proof replaces the derivative of the collision map by the fixed-normal reflection matrix and therefore deletes the difficult Jacobi factors.

### 3. Incoming flux compensates at most the local incidence singularity

Even if one local inverse cosine is integrable against incoming flux, a long genealogy carries products of incidence and collision-derivative factors. The manuscript provides no estimate showing that all earlier and later factors disappear after conditioning at the “youngest fork.” The asserted depth-independent inverse moment is the main theorem and is not proved.

### 4. The first-surplus gain therefore has no basis

The uniform exponent \(\alpha_0\) is obtained entirely from the affine-fork inverse moment. Once that lemma fails, the coarea optimization does not yield a depth-independent \(arepsilon^{\alpha_0}\) factor. The \(C^m\) prefactor cannot absorb a depth-dependent negative power of \(arepsilon\).

### 5. Analytic-radius loss is not controlled under sewing

The one-block theorem works between adjacent analytic label radii. With \(T/h_arepsilon\) blocks, a fixed loss per block exhausts every finite initial radius. The proof says that the loss “sums to a finite amount” but does not show that the loss is \(O(h_arepsilon)\). This is independent of the scalar error estimate.

### 6. The common-refinement argument is incomplete

Two diagonal meshes satisfying

\[
\varepsilon^{\alpha_0}/h_arepsilon\to0
\]

need not possess a uniform common refinement with the same property, particularly when the partitions are not commensurate. Independence of the limit requires a stability estimate for arbitrary partition unions, not the assertion that a common admissible refinement exists.

### 7. The conservative repair theorem is a new unproved PDE theorem

A globally invariant-orthogonal balance defect need not be orthogonal on each energy–momentum shell. The statement that binary collision directions span the full complement shellwise, with a bounded Bogovskii-type right inverse compatible with positivity, pre/post symmetry, traces, and velocity weights, is highly nontrivial. No operator, estimate, or shell geometry is given.

Adding a small Maxwellian background does not automatically dominate a signed correction pointwise or make its relative entropy vanish near zeros and high velocities.

### 8. Local analytic cumulants do not prove the global LDP

Real-source exhaustion requires uniform pressure control on every truncation ball, exponential compact containment, consistency of the duals, and a lower-bound concentration theorem. The manuscript states these conclusions after proving at most a bounded-source short-time expansion. Positive tests detecting singular measures and scaled balance tests lie outside any fixed analytic ball; passing to infinity is not automatic.

### 9. The trace graph theorem is still underspecified

Weak convergence of divergence-measure currents with bounded total variation does not by itself give convergence of all normal traces on a domain with intersecting collision faces. The graph topology, endpoint traces, multiple-collision corners, and analytic hierarchy weights require a complete closedness theorem.

## Status of earlier objections

The normal-trace convention, true-future requirement, and diagonal mesh condition are meaningful repairs. The replacement physical transversality lemma is not valid, and all later theorems depend on it.

## Minimum reconstruction

The authors must derive the full linearized collision map in the proposed fork coordinates and prove an inverse-moment estimate for its actual two-dimensional transverse Jacobian, uniformly after summing genealogies. Only then can the source expansion, conservative recovery, and global LDP be addressed.

## Recommendation

**Reject.** The paper's new root estimate suppresses the normal-dependence of hard-sphere reflections and therefore does not control recollisions in the deterministic dynamics.