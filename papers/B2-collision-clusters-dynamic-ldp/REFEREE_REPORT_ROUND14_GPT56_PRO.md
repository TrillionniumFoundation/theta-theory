# Independent Referee Report — Round 14

**Manuscript:** B2 — *Collision Clusters and Dynamic LDP*  
**Reviewed branch:** `revision/round14-referee-positive-closure-11paper-2026-09-01`  
**Reviewed commit:** `dd9dbcb891076b7dbfe388bd8543d8342ba103c0`  
**Reviewed tree:** `c4492f8891e065201af70e68e6764ff5975f2137`  
**Controlling module:** `ROUND14_POSITIVE_CLOSURE.tex`  
**Registered module SHA-256:** `2dbb7caa64f22c6ce252a3bbfa6365f3843eaab5be9aa6a0f269f10cf039b2b6`  
**Editorial standard:** *Annals of Mathematics*, *Acta Mathematica*, *Inventiones Mathematicae*, or *JAMS*  
**Recommendation:** **Reject**

## Executive assessment

Round 14 makes a sensible strategic change: it treats the full fixed horizon in one trajectory expansion, uses one normal-flux trace, and allows the analytic sublevel exponent to depend on the genealogy before summing by dominated convergence. These are preferable to the earlier false blockwise and depth-uniform claims.

The core deterministic recollision lemma is still not proved. Its pseudo-orbit removes the first surplus contact equation while retaining the reflection and all later dynamics, an impossible combination away from the contact set. The witness configuration does not establish a nonzero transverse-position minor for an arbitrary genealogy. The lower-bound “Hodge repair” also derives positivity from an `L2` solution without any pointwise control. Consequently neither the marked pressure nor the full LDP is established.

## Decisive objections

### 1. The first-surplus pseudo-orbit is not a defined physical trajectory

The paper says:

> Remove only the first surplus-contact equation, not its reflection or future trajectory.

After the contact constraint is removed, the two particles generally do not satisfy

\[
|x_a(t_*)-x_b(t_*)|=\varepsilon.
\]

There is then no physical collision at `t_*`, no collision normal determined by their relative position, and no specular reflection to apply. One cannot simultaneously vary off the contact manifold and retain the same physical reflection/future orbit.

A legitimate coarea argument must define an unconstrained map up to the prospective contact time and evaluate the contact function there. The post-contact dynamics can only be introduced on the zero set, or through a carefully constructed extension whose derivatives are shown not to affect the tube estimate. The manuscript does neither.

### 2. The claimed leading Jacobi block does not follow from the chosen variables

The proof varies two tangential components of a creation normal and writes the surplus-position derivative as

\[
-2gL I_{\omega^\perp}+O(\delta).
\]

But changing that normal while satisfying all earlier creation constraints also changes:

- the creation point and time;
- both outgoing velocities;
- every later collision time and normal;
- the endpoint at which the final free flight starts; and
- potentially the ordering of the prescribed genealogy.

Those contributions are not `O(delta)` merely because later contacts are placed in a short interval. The implicit-function derivatives of the constraints can be large near grazing or near multiple contacts. No quantitative chart estimate is given.

### 3. The witness configuration is not shown to exist for every genealogy

For an arbitrary fixed ordered graph the proof asks that all subsequent creation contacts occur in a short interval, remain regular, and leave a final free flight of length `L`. Hard-sphere exclusion, bounded velocities, the prescribed incidence order, and pre-existing labels can make such a configuration impossible.

The argument “choose normals and velocities generically” is not a realization theorem. A nonidentically-zero analytic minor must be exhibited on the actual nonempty parameter domain of each genealogy, not on a formally imagined collision sequence.

### 4. Symplectic invertibility still does not prove the required position rank

The full collision/free-flight differential may be invertible and symplectic while the projection of two Jacobi fields onto the two transverse position coordinates at `t_*` has rank zero or one. The elementary map `(q,p) -> (p,-q)` demonstrates the logical gap.

Round 14 adds the term `-2gL I`, but without controlling all constraint and intervening-collision derivatives this does not establish the position minor. The central fixed-genealogy sublevel theorem remains unproved.

### 5. Weak trace compactness does not exclude concentration on corners

The Green theorem says multiple-contact intersections have zero simple-flux mass and that this property is preserved under weak graph convergence. A sequence of codimension-one flux measures with uniformly bounded total mass can concentrate onto a codimension-two intersection. Codimension alone does not prevent such a weak limit.

To retain only simple traces, the paper needs a uniform nonconcentration estimate near grazing and multiple-contact strata. Otherwise the graph closure must include independent corner traces and compatibility conditions.

### 6. The global genealogy majorant is asserted without controlling velocity integration

The displayed majorant contains

\[
e^{C\sum_i|v_i|^2}.
\]

Its integrability against the Maxwellian activity requires an explicit margin between `C` and the inverse-temperature weight, stable under all bounded complex sources and derivatives. No such inequality is stated. The combinatorial claim that the sum over all labels and surplus contacts is finite also needs the exact label/activity factors, not only the time-simplex denominator.

### 7. The Hamiltonian derivation is conditional on the missing cycle theorem

Deleting the last creation contact of a limiting tree can produce two subtrees, but the deterministic microscopic expansion converges to that tree series only after the cyclic sector has been controlled. Since the Jacobi/tube argument is not proved, the marked pressure and every `psi` derivative remain formal.

### 8. The exposed-pair theorem does not construct bounded sources for every stated pair

Given a smooth balanced pair with bounded positive `q`, the formula

\[
\psi=\log q-\Delta p
\]

is algebraic. The paper additionally claims that a bounded smooth `p` solving the relevant backward adjoint equation exists and that the microscopic tilted law concentrates exponentially. This requires a well-posed adjoint problem, source-domain bounds, strict convexity on the full balanced quotient, and convergence of the tilted cluster expansion. These properties are asserted, not proved.

### 9. The kinetic Hodge repair does not preserve positivity

Lax–Milgram gives an `L2`-type solution `r` with control of

\[
\int|\Delta r|^2dA_f.
\]

It does not give an `L-infinity` lower bound for `Delta r`. The paper then says that adding a vanishing Maxwellian background makes

\[
q+\Delta r>0.
\]

An arbitrarily small positive background cannot dominate an unbounded negative part of an `L2` correction. Positivity of the repaired collision measure is therefore not established. Without positivity, it is not a valid contact intensity and its Poisson entropy is not defined.

### 10. The repair is not shown to have vanishing entropy cost

Even if positivity were restored by clipping, the entropy

\[
\int\ell(q+\Delta r)dA_f
\]

is sensitive to large positive and near-zero values. `L2` convergence plus the phrase “Orlicz equi-integrability” does not prove convergence of this entropy. A quantitative truncation, positivity margin, and de la Vallée-Poussin estimate are needed.

### 11. The full LDP is not obtained from bounded analytic sources alone

The upper bound requires exponential tightness in the weighted trace-graph topology. The lower bound requires a dense family of actual microscopic tilted laws. Both are delegated to the unproved trace/Jacobi/repair lemmas. Monotone truncation of `log q` gives a pointwise convex conjugate; it does not manufacture deterministic hard-sphere recovery.

## Dependency assessment

B2-GC remains the first open gate in the hard-sphere chain. B1 has no justified trajectory-polymer coefficient expansion; B3 has no microscopic covariance theorem; B4 has no limiting action/semigroup input; and C1/C2/D1 remain downstream.

## Required reconstruction

A credible submission must first prove a standalone fixed-horizon theorem:

1. a legitimate pre-contact map and coarea tube estimate;
2. an actual realization/nonfocusing theorem for each genealogy class;
3. a summable global majorant with velocity margins;
4. a closed trace space including or excluding corner concentration by proof; and
5. a positive entropy-stable recovery construction.

## Recommendation

**Reject.** The strategic fixed-horizon reorganization is useful, but the principal recollision and lower-recovery theorems remain invalid or unproved.