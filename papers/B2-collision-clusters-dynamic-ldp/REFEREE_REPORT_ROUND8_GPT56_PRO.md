# Round-Eight Independent Referee Report — GPT-5.6 Pro

**Manuscript:** B2 — *Collision Clusters and a Dynamic Large-Deviation Principle for Deterministic Hard Spheres*  
**Editorial standard:** *Annals of Mathematics*, *Acta Mathematica*, *Inventiones Mathematicae*, or *Journal of the AMS*  
**Recommendation:** **Reject**  
**Reviewed revision branch:** `revision/round8-referee-positive-closure-11paper-2026-08-31`  
**Reviewed branch head:** `ad2b5106678b29b7d9ffb3824f61ddbd141ac4b8`  
**Reviewed tree:** `00d7ef9edcddda26fc88962e206677f9b399bebe`  
**Active controlling module:** `ROUND8_POSITIVE_CLOSURE.tex`, blob `366d8f0ba31f0efe8fee0f60d43c3bec3f01394b`

## Executive assessment

Round eight abandons the previous fiction that an arbitrary interior measure and an arbitrary boundary flux form a kinetic state. It also stops using QR coordinate resets as though they could erase physical Jacobi losses. These are correct responses to the last report.

The replacement still does not establish the actual-contact LDP. The declared graph completion is built from `L1` interior densities with `L1` transport derivatives, yet the theorem says that a collision-time boundary Dirac belongs to that completion; this is incompatible with the norm. The depth-independent Jacobi estimate is asserted from unstable monotonicity without proving that the chosen fork variables are admissible physical variations or that transverse two-volume survives projections to the future contact coordinate. The source-sewing estimate is not uniform over vanishing meshes. Most decisively, the regularization theorem invokes a compact symmetry group that would have to smooth arbitrary velocity/path laws while preserving momentum, energy, the collision manifold, and conjugating the full hard-sphere flow; no such group exists.

## Genuine repairs recognized

The following round-eight directions are appropriate:

- kinetic trace compatibility is encoded by a closed graph rather than independent coordinates;
- actual reflected futures are retained;
- physical Jacobi fields replace coordinate-normalization rhetoric;
- low-angle and short-gap bad sets are separated from the good coarea set;
- GC is placed upstream of B1 and MC;
- the lower-bound regularization is required to preserve balance exactly.

## Major mathematical objections

### 1. Boundary Dirac traces do not belong to the declared graph completion

The level space is the closure of smooth densities in the norm

\[
\|g\|_{L^1_w}+\|Tg\|_{L^1_w}+
\|\gamma^-g\|_{\mathcal M_w}.
\]

A Cauchy sequence in the first two terms converges to an `L1` interior density with an `L1` transport derivative. A point mass in the tangential boundary variables cannot be obtained while the interior approximants remain Cauchy in `L1`; concentrating a tangential mollifier to a Dirac has no `L1` limit. Concentrating in the normal direction instead creates a distributional transport derivative rather than an `L1` derivative.

Thus the sentence “approximating a collision trace by incoming thin layers shows that its Dirac limit belongs to the graph closure” is false for this norm. One needs an interior measure-valued transport space, not an `L1` graph with an independently measure-valued trace.

### 2. Lumer–Phillips is invoked without a generator theorem

The proof does not establish density of the domain, dissipativity of the full triangular creation/reflection operator, or the range condition for one resolvent value. A positive Neumann series for a formal boundary renewal is not by itself the Lumer–Phillips theorem.

The bound for `B_{k,k+1}` also ignores the geometry and velocity weights of the collision kernel. Factorial label weights control combinatorics, but not grazing trace losses or the compatibility of creation with the `Tg` graph coordinate.

### 3. The “youngest fork” variations are not shown to be admissible chronological variables

At a true creation collision, independently translating the two outgoing child clusters immediately after the fork generally breaks continuity with the pre-collisional parent trajectory and the contact constraint. Such translations are not automatically coordinates of the original initial-data/collision-time integral.

The paper must derive the two transverse controls from actual impact normal, time, and root variables and compute the Jacobian of that transformation. Declaring two root translations at every youngest fork skips the main geometric issue, especially for ancestor–descendant lineages.

### 4. Unstable monotonicity does not prove the claimed projected two-volume bound

Positive curvature controls an unstable Lagrangian graph in full phase space. The first-surplus coarea map uses the projection of two Jacobi fields to a particular pair's relative position at a later collision. Full phase-space expansion does not automatically give a lower bound for that projected exterior area.

The manuscript says “apply the same calculation to the second exterior power,” but no exterior-power mirror formula or lower bound is proved. Neutral directions of hard-sphere collision cylinders and changes in which particles collide can rotate the unstable plane relative to the final contact projection. A determinant-one/symplectic property does not control the smallest projected singular value.

### 5. The bad-set estimate and the depth-independent Gramian are unsupported

The theorem claims one exponent `C` independent of ancestral depth and one bad-set exponent `alpha`. The proof performs no induction through the many-particle scattering cocycle and gives no uniform chart atlas at multiple and near-grazing contacts. These constants are precisely the quantities needed to make the sum over all genealogies converge; they cannot be left inside the theorem statement.

### 6. The source-sewing theorem overstates the one-block estimate

The one-block error contains a term independent of the block length:

\[
C_R(h\varepsilon^\eta+\varepsilon^\eta).
\]

For `T/h` blocks, telescoping gives a contribution of order

\[
T\varepsilon^\eta/h.
\]

This does not vanish uniformly over partitions whose mesh tends to zero jointly with `epsilon`. The proof actually takes the iterated limit “fix `h`, send `epsilon` to zero, then send `h` to zero.” That is weaker than the theorem's claimed uniformity and does not define a partition-independent semigroup without an additional stability/rate argument.

### 7. The compact smoothing group does not exist

The regularization theorem postulates a compact group generated by spatial translations and “small canonical velocity transformations” which simultaneously:

- preserve total momentum and energy;
- preserve every hard-sphere collision manifold;
- conjugate the complete hard-sphere flow and contact current; and
- smooth every noninvariant direction.

The genuine continuous symmetries are global Euclidean motions, permutations, time translation, and Galilean transformations with the usual changes in conserved quantities. They do not form a compact group acting transitively enough to smooth arbitrary velocity distributions on fixed momentum–energy shells while conjugating all free flights and collisions.

A Kac collision process or projected heat flow is a stochastic regularizer, not a symmetry conjugacy of the deterministic path law. The displayed exact balance-preserving smoothing therefore has no construction.

### 8. The full LDP lower bound is reduced to slogans

Even if the pressure existed, “solve the finite projected exposing equations” does not establish concentration of the deterministic microscopic law under the exact tilt. The proof needs a source-uniform second-derivative estimate, a unique regular tilted kinetic path, and a microscopic lower-bound construction. The regularization lemma intended to extend the result is itself invalid.

### 9. Exponential tightness and contact compactness are not proved in the controlling module

The final theorem invokes exponential tightness without deriving velocity tails, contact-mass tails, or a time-modulus estimate in the new graph-trace topology. These properties do not follow solely from the formal semigroup bound.

## Dependency assessment

B2-GC remains the first open hard-sphere interface. B1 cannot use a completed source-decorated pressure, and B3/B4/C1/C2/D1 cannot use actual-contact action, covariance, graph semigroups, or lower-bound tilts from this paper.

## Required reconstruction

A credible B2 paper must:

1. construct a compatible measure-valued kinetic trace space that genuinely contains stopping-contact states;
2. prove the boundary-renewal generator and its source perturbations;
3. derive fork controls from actual chronological variables;
4. establish a projected Jacobi determinant summable jointly in depth and `epsilon`;
5. prove a block error compatible with the intended sewing limit; and
6. replace the nonexistent symmetry smoothing by a rigorously balance-preserving approximation theorem on the kinetic action.

## Recommendation

**Reject.** The paper responds to the correct objections, but its new trace domain excludes the boundary states it claims to contain, the uniform recollision geometry is not proved, and the regularization mechanism is based on a nonexistent dynamical symmetry group.