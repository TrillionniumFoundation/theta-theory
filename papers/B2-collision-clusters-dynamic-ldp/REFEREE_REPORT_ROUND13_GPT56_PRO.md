# Independent Referee Report — Round 13

**Manuscript:** B2 — *Collision Clusters and Dynamic LDP*  
**Reviewed branch:** `revision/round13-referee-positive-closure-11paper-2026-09-01`  
**Reviewed commit:** `5c8b71e67d62d4a63c53a5a59e7a10f1ccc0f688`  
**Reviewed tree:** `586de2e3cf8c547ca3cbfbc0cb0daba2fd05af59`  
**Controlling module:** `ROUND13_POSITIVE_CLOSURE.tex`  
**Registered module SHA-256:** `cfdf26027356a63216f77307173ded483c1e3a4006a07cd5869834c5a27d5880`  
**Editorial standard:** *Annals of Mathematics*, *Acta Mathematica*, *Inventiones Mathematicae*, or *JAMS*  
**Recommendation:** **Reject**

## Executive assessment

Round 13 correctly stops trying to sew a vanishing time mesh from an unproved blockwise cyclic modulus. It instead proposes a fixed-horizon dominated-convergence argument over complete genealogies, retains the true reflected future, and allows the analytic sublevel exponent to depend on the genealogy. Those are genuine conceptual improvements.

The new proof still fails at its two load-bearing interfaces. The trace norm calls `gamma^-` a normal-flux measure and then multiplies it by `v·n` a second time. More seriously, invertibility of the full symplectic collision differential does not imply that the projection of two root Jacobi fields onto the two transverse position coordinates is nondegenerate. A symplectic map can send an entire position plane into momentum directions. The argument offered for nonidentical minors is therefore invalid, so the dominated-convergence removal of all recollisions has no pointwise input. The full LDP lower bound then assumes rather than proves the required exposed controlled trajectories.

## Decisive objections

### 1. The trace norm double-counts the normal flux

The manuscript defines `gamma_k^-` as an incoming **normal-flux measure**. Its Green identity pairs this measure directly with

\[
 \phi^+-\phi^-.
\]

That convention is correct: the factor `V_k·n` is already contained in the normal trace. The graph norm, however, contains

\[
 \|v\cdot n\,\gamma_k^-\|_w.
\]

This multiplies the flux by the normal velocity a second time. Near grazing it changes the topology by an extra vanishing factor and no longer controls the trace appearing in the Green formula.

If `gamma^-` is instead intended to be an unweighted boundary density, then the Green identity is missing the flux factor. Both interpretations cannot be true simultaneously. The closed graph and all subsequent contact estimates depend on choosing one convention consistently.

### 2. Symplectic invertibility does not prove a nonzero transverse position minor

The key lemma argues that the full collision/free-flight derivative is invertible symplectic and concludes that the two-dimensional map

\[
 \xi\longmapsto
 \Pi^\perp(q_a-q_b)
\]

cannot have identically vanishing determinant.

This inference is false. An invertible symplectic transformation can map a two-dimensional position-variation plane entirely into momentum directions. The standard symplectic rotation

\[
 (q,p)\mapsto(p,-q)
\]

is the elementary example: it is invertible and symplectic, while the final position projection vanishes on the initial momentum-zero position plane at the corresponding conjugate time.

Thus independence of the two Jacobi fields in full phase space does not imply independence of their transverse **position** components at the surplus time. The kernel direction may also vary with the chronological variables, so a pointwise rank defect does not backward-propagate as one fixed field tangent to both roots.

A model-specific nonfocusing/conjugate-point theorem for every regular genealogy is required. It is not supplied.

### 3. The fixed-genealogy analytic sublevel estimate has no established nonzero function

Quantitative analytic sublevel theory applies only after one proves that a specified determinant minor is not identically zero on each homogeneous chart. The proof merely asserts that some unspecified minor is nonzero at a regular point. It does not identify the variables, the minor, or a configuration at which its value is nonzero.

Symmetric genealogies, near-conjugate flights, and changes of collision ordering can make different minors vanish on different charts. Without a finite chartwise selection and a measurable majorant, the constants `C_G` and `beta_G` are not defined inputs to the dominated-convergence sum.

### 4. The factorial majorant does not by itself dominate the constrained surplus tube

The displayed majorant counts source-decorated chronological contact graphs before imposing the small two-dimensional surplus-position tube. To use it as a dominating function after the Jacobi change of variables, one must prove that all inverse Jacobians, grazing factors, singular chart partitions, and later reflected contacts are bounded by that same absolute activity.

The proof says that normal flux “sums homogeneity strips,” but it does not show a genealogy-independent integrable bound for the inverse coordinate changes introduced in the transversality step. Dominated convergence cannot be invoked until this domination is proved on the actual common measure space.

### 5. The fixed-horizon pressure theorem uses a limiting semigroup not yet constructed

The local connected series is available only on a source-dependent short interval. To extend it, the paper composes finite-volume Feynman–Kac operators and invokes uniqueness of a limiting mild Hamilton–Jacobi equation. The state space, terminal-function class, nonlinear semigroup, and comparison/uniqueness theorem are not defined here; B4 later claims to construct them using B2.

This is a dependency loop unless B2 proves its own complete Picard semigroup theorem on a specified Banach space. The sentence “decomposing a tree at its last contact gives Picard uniqueness” is not such a theorem.

### 6. The lower-bound recovery assumes exposure of every regular target

For a smooth positive balanced pair the proof writes

\[
 \psi_n=\log q_n-\Delta p_n
\]

and says that this defines the microscopic tilted law. Existence of a bounded `p_n` solving the adjoint/exposing equations is not proved. A smooth finite-action point need not be an exposed point of the full infinite-dimensional rate, and the balance multiplier may fail to exist in the declared source space.

The subsequent “diagonal truncation” cannot replace:

- construction of a dense exposed class;
- concentration under each microscopic tilted law;
- uniform recollision estimates under those tilts; and
- entropy convergence after restoring exact balance.

These are the difficult parts of the deterministic lower bound.

### 7. The controlled Boltzmann approximation is circularly specified

The proof proposes to approximate a target `(f,Gamma)` by choosing `q_n` and then solving the controlled Boltzmann equation with activity `q_n A_{f_n}`. The unknown solution `f_n` occurs inside its own reference intensity. To conclude `f_n -> f`, one needs a stability theorem showing that the chosen coefficients approximate the target equation in the precise weighted trace topology. No such theorem or estimate is stated.

### 8. The claimed full LDP does not follow from local analytic pressure alone

Even pressure convergence on every bounded real-source ball, if proved, gives convex dual upper bounds. A full good LDP on the trace-graph path space additionally requires exponential tightness, a separating dual algebra compatible with the topology, and a lower bound for all finite-action points. The paper asserts all three in one paragraph.

The actual-contact coordinate and singular trace topology make these requirements substantially stronger than the standard finite-dimensional Gärtner–Ellis theorem.

## Genuine improvements recognized

The use of one incoming flux convention, the fixed-horizon global genealogy strategy, the true reflected future, and genealogy-dependent analytic exponents are the correct directions. The paper should retain them after repairing the trace and transversality theorems.

## Dependency assessment

B2-GC remains the first hard-sphere gate. B1's primitive shell, B3's Gaussian field, B4's Nisio semigroup, and C1/C2/D1 all depend on the all-contact pressure and full joint LDP. None is certified while the Jacobi and recovery arguments remain open.

## Required reconstruction

A viable paper should focus on a single theorem: a complete fixed-horizon marked trajectory expansion with a rigorously selected nondegenerate physical minor and a common integrable genealogy majorant. Only after that should the authors state a precise exposed-class lower bound and then a full LDP.

## Recommendation

**Reject.** The global summation strategy is more credible than the previous block sewing, but the physical transversality proof uses an invalid symplectic-projection inference, the trace space is internally inconsistent, and the LDP lower bound is assumed rather than established.
