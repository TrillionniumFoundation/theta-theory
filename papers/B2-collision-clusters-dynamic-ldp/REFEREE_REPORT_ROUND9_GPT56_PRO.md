# Round-Nine Independent Referee Report — GPT-5.6 Pro

**Manuscript:** B2 — *Collision-Marked Trajectory Clusters and Joint Dynamic Large Deviations for Deterministic Hard Spheres*  
**Editorial standard:** *Annals of Mathematics*, *Acta Mathematica*, *Inventiones Mathematicae*, or *Journal of the AMS*  
**Recommendation:** **Reject**  
**Reviewed revision branch:** `revision/round9-referee-positive-closure-11paper-2026-08-31`  
**Payload-host branch head at review lock:** `a8c0c551f5f8614856a9d433e78b2eb92a5dcfa1`  
**Registered round-nine payload SHA-256:** `cf230322211332af59a7883af1b669eeb9b4f7e9f4220fc24712c634bda17716`  
**Reviewed registered source:** `revision/round9-referee-final/B2_TRACE_JACOBI_SEWING_LDP.tex`  
**Reviewed source SHA-256:** `09900b878c679267de02fb6fe8a23cbebb2f66644b24eb4c17e0ec00ca6b0766`  

## Evidence boundary

At the review lock, the branch stored the checksum-pinned round-nine payload while the paper-level `main.tex` files still loaded the round-eight modules; the repository publication workflow was queued. I independently verified the payload hash, unpacked it, and ran the repository materializer successfully, producing byte-identical paper-level `ROUND9_POSITIVE_CLOSURE.tex` files. This report therefore reviews the exact registered round-nine theorem text. It does not treat a queued workflow, a clean build, theorem/proof counts, or an internal hostile-regression script as evidence that the mathematical claims are true.

## Executive assessment

The paper now attempts to place boundary traces in a closed transport graph, keeps the true reflected future after a surplus contact, and scales the one-block error linearly in the block length. These changes address real defects.

The central deterministic theorem remains unproved. The trace is not consistently typed in the Green identity, the claimed inverse-Jacobi moment estimate is unsupported for the semi-dispersing hard-sphere geometry, and the finite-cell repair does not establish a dense lower-bound class. The final joint LDP is still a formal kinetic answer rather than a consequence of the microscopic dynamics.

## Major objections

### 1. The Green identity double-counts the normal flux

The manuscript defines \(\gamma^-_{k,ij}\) as the incoming normal trace of the divergence-measure current
\[
 \mathcal J_k=(g_k,v_1g_k,\ldots,v_kg_k).
\]
A normal trace is already the measure \(\mathcal J_k\cdot n\). The Green formula should pair a test directly with that trace. Instead the theorem writes
\[
 \int_{\Gamma_{ij}}\phi\,(V_k\cdot n_{ij})\,d\gamma_{k,ij},
\]
multiplying by the normal velocity a second time.

If \(\gamma\) is intended to be an unweighted boundary density, it is not the normal trace claimed in the definition. The state space, norm, reflection map, and creation operator depend on which convention is used. The theorem is ill-typed as written.

### 2. The time variable in the divergence-measure state is not specified

A level state is introduced as a measure on the instantaneous phase domain, but the current contains a time component and the test formula includes \(\partial_t\phi\). A space-time transport current and a time-slice state are different objects. The paper does not define the topology in which normal traces at collision faces and time slices coexist or prove that the semigroup maps the graph into itself.

### 3. The flux-weighted Jacobi lemma is the missing hard-sphere theorem

The map from all fork variables to a three-dimensional relative position is rectangular, so the notation
\[
 \wedge^2J_m^{-1}
\]
is undefined until a two-dimensional submap and a measurable choice of minor are specified.

More substantively, hard-sphere collision cylinders are semi-dispersing and possess neutral directions. Positivity of a curvature form does not imply an inverse-moment bound
\[
 \int |\wedge^2J_m^{-1}|^p\,d\mathfrak f_m
 \le C^m\delta^{-C}
\]
with a \(\delta\)-exponent independent of depth. Each near-grazing conversion can introduce an inverse cosine; the incoming flux compensates at most a specific power and does not automatically make the product integrable for arbitrary \(p\).

The proof gives no recurrence, exterior-power calculation, or selection of admissible chronological variables. It is a research program compressed into one paragraph.

### 4. The first-surplus coarea estimate does not follow from the lemma as stated

An \(L^p\) bound on an inverse Jacobian must be combined with a precise coarea/Hölder argument, dimensional exponents, multiplicity control, and a lower-dimensional contact tube. None is given. The treatment of the bad set likewise assumes independent one-event integration despite correlations imposed by the entire chronology.

Therefore the depth-uniform \(\varepsilon^\alpha\) gain—the root of B2-GC—has not been proved.

### 5. The boundary-renewal hierarchy lacks an \(\varepsilon\)-uniform operator theorem

The estimate
\[
 \|B_{k,k+1}G_{k+1}\|\le C(k+1)\|G_{k+1}\|
\]
must include the collision-surface scaling, velocity weights, grazing traces, and creation compatibility. The text simply declares that one velocity-weight loss pays for grazing. No domain, dissipativity, or resolvent theorem is supplied for the triangular operator.

### 6. The one-block noncyclic error is asserted without a geometric derivation

The term \(h^2\varepsilon^\eta\) is exactly what makes sewing work, but the proof only says that unmatched boundary/end pieces have two event integrations. Two time integrals do not by themselves produce a power of \(\varepsilon\). A complete Boltzmann–Grad change of variables and uniform trace estimate are required.

### 7. The conservative finite-cell repair is not established

For an arbitrary finite discretization, the range of the transport/contact incidence matrix need not equal the full orthogonal complement of mass, momentum, and energy. There may be disconnected cells, inaccessible collision pairs, boundary constraints, and mesh-dependent small singular values.

Even if the algebraic defect lies in the range, the norm of a right inverse can diverge as the mesh is refined. The signed correction may then be larger than the positive background, and its entropy cost need not vanish. No quantitative controllability estimate is provided.

### 8. The lower-bound proof assumes exposure and concentration

A smooth positive feasible path is not automatically exposed by finitely many bounded sources. Solving the inverse kinetic Hamilton equations, proving the finite-volume tilted law concentrates on the target, and controlling recollisions under that tilt are the hard parts of the deterministic lower bound. They are asserted rather than proved.

### 9. Compact containment is not derived

Moment and total-contact exponential estimates do not alone give a Skorokhod modulus for the density/contact path. The Green identity controls only a chosen test class and requires uniform integrability of the collision kernel. The good-rate claim is unsupported.

## Dependency assessment

B2-GC is the first hard-sphere gate. Until the compatible trace semigroup and depth-uniform first-surplus estimate are proved, B1 has no full complex pressure input and B3/B4/C1/D1 have no microscopic density–actual-contact LDP.

## Required reconstruction

The paper should focus on one theorem: an \(\varepsilon\)-uniform marked real-trajectory cluster expansion on a rigorously constructed transport/trace domain. It must give the actual Jacobi/coarea estimate with all exponents and then a source-uniform lower-bound construction. The global LDP should follow only after these pieces exist.

## Recommendation

**Reject.** The central geometric and functional-analytic estimates remain assertions, and the final Poisson-entropy action is not derived from deterministic hard spheres.
