# Round-Seven Independent Referee Report — GPT-5.6 Pro

**Manuscript:** B2 — Collision Clusters and Dynamic Large Deviations  
**Editorial standard:** *Annals of Mathematics*, *Acta Mathematica*, *Inventiones Mathematicae*, or *Journal of the AMS*  
**Recommendation:** **Reject**  
**Reviewed revision:** `revision/round7-referee-positive-closure-11paper-2026-08-31@b1e3d17f59ca9bb1a04d4ac9157f10dc333f9607`  
**Controlling module:** `ROUND7_POSITIVE_CLOSURE.tex`, blob `544c517699ef734e7df4357afe249036b4d40b22`

## Executive assessment

Round seven addresses two genuine objections: it no longer treats an arbitrary interior \(L^1\) density as having a uniformly bounded boundary collision rate, and it no longer deletes the deterministic future after the first surplus contact. Boundary states are promoted to measures and the intended recollision estimate is reorganized around a youngest separating fork.

The new proof does not close the microscopic theorem. The measure–trace state is not a well-defined kinetic trace domain, and a QR reparametrization cannot remove the accumulated singular values of the physical Jacobi cocycle while preserving the integration measure. The claimed depth-independent Gramian is therefore unsupported. The regularization and full LDP lower bound are also stated at the level of a program rather than proved.

## Major mathematical objections

### 1. The measure–trace hierarchy does not define compatible transport states

A level state is declared to be an arbitrary pair

\[
(g_k,\gamma_k^-)
\]

of an interior finite measure and an incoming boundary finite measure. For a genuine transport solution, the incoming trace is not an independent coordinate: it must be the kinetic trace of the interior/outgoing evolution and satisfy compatibility at reflections, corners, and creation boundaries. An arbitrary finite interior measure has no boundary trace, while an arbitrary boundary atom need not be the trace of any admissible interior state.

The norm imposes tangential BV only on the absolutely continuous part and then says grazing losses are absorbed by total variation. Differentiating reflected traces near grazing can create singular measures with nonintegrable coefficients; total variation alone does not close the transport generator. No Green formula, trace theorem, closed generator domain, or compatibility condition is supplied.

Thus \(U_k(t)\), \(B_{k,k+1}\), and the claimed positive semigroup on the announced Banach space have not been constructed. The estimate

\[
\|B_{k,k+1}G_{k+1}\|_k\le C(k+1)\|G_{k+1}\|_{k+1}
\]

is precisely a difficult hard-sphere trace estimate, not a consequence of factorial weights.

### 2. A frame reset cannot erase physical depth deterioration for free

The physical derivative from ancestral impact variables to a later relative position is a product of linearized free flights and scattering maps. Repeated non-grazing maps with condition number \(C\delta^{-C}\) may have smallest singular value of order \(\delta^{Cm}\).

Changing coordinates by QR at every event does not alter this physical singular value. If the reset rescales a shrinking direction to unit size, the inverse scaling appears in the complementary variables or in the Jacobian of the change of integration variables. A symplectic transformation can have determinant one while possessing exponentially large and small singular values. Unit determinant is therefore not a uniform condition-number estimate.

The proof claims both that the reset orthonormalizes the relevant coordinate and that the change of chronological variables has Jacobian one, then discards the complementary scaling. That is the missing cost. No explicit canonical transformation of the full integration variables is given, and no bound proves that conditional coarea measures are unchanged. The conclusion

\[
\lambda_{\min}\mathcal G_{ab}\ge c\delta^C
\]

independent of depth does not follow.

### 3. The youngest fork controls initial separation, not all later focusing

Even if relative root translations or fork impact variables span the transverse plane at the separating event, subsequent collisions can focus those variations before the proposed surplus contact. The backward-covector argument must multiply the inverse scattering matrices along the entire exclusive paths. Calling the intermediate bases “reset frames” does not remove that multiplication.

The manuscript therefore has no depth-uniform first-surplus gain. Without it, the all-depth cyclic-sector sum and the \(O(arepsilon^{\alpha_0})\) elimination of recollisions remain open.

### 4. The fixed-horizon source sewing assumes the one-block theorem it needs to prove

The estimate

\[
\|\mathcal S_{h,arepsilon}^H-\mathcal S_h^H\|
\le C_R(harepsilon^\eta+arepsilon^{\alpha_0})
\]

is announced after invoking “the usual noncyclic Boltzmann–Grad change of variables.” For actual-contact sources on a measure-valued trace hierarchy, this is a new operator convergence theorem. It must control all source derivatives, boundary atoms, grazing pieces, and reached trace radii. No derivation is supplied.

The iterated limit “fix \(h\), send \(arepsilon	o0\), then \(h	o0\)” also does not by itself give one partition-independent pressure semigroup unless consistency and stability as the mesh changes are proved.

### 5. The proposed exact regularization is not defined

A “velocity-space Ornstein–Uhlenbeck heat projected onto the collision invariants” is not specified. Ordinary Ornstein–Uhlenbeck evolution does not preserve exact total energy and momentum. Brownian motion on each energy–momentum shell is a different degenerate operator and does not commute automatically with the nonlinear map \(f\mapsto A_f\) or with the full transport/contact balance.

Likewise, a Kac collision semigroup on a shell acts on velocity laws, not directly on an arbitrary density–contact pair in such a way that the weak balance defect remains exactly zero. The assertion that the product semigroup commutes with balance is the theorem; it is not proved. Entropy contraction of separate Markov operators does not imply convergence of the perspective action relative to the changing nonlinear reference \(A_{f_h}\).

### 6. The grand-canonical lower bound is not obtained from local projected curvature

Differentiability and positive variance on a regular finite-dimensional chart yield a lower bound near the chart's exposed mean. They do not prove that every smooth positive feasible pair is exposed by a bounded source, nor that the projective pressure is available on all source sizes required by the regularization. The claimed full LDP lower bound compresses these missing constructions into “solve the finite projected exposing equations.”

## Dependency assessment

B2-GC remains the first hard-sphere gate. B1 cannot use its marked pressure as proved input, and B2-MC, B3, B4, C1/C2, and D1 remain conditional. The dependency diagram in the repository does not change this mathematical order.

## Required reconstruction

Construct a genuine compatible kinetic trace space and semigroup, prove a recollision estimate whose physical singular-value loss is summable jointly in depth and \(arepsilon\), and give a complete source-uniform one-block operator theorem. A balance-preserving smoothing theorem must be formulated and proved for the actual nonlinear density/contact action before it can support the LDP lower bound.

## Recommendation

**Reject.** The revision removes an invalid boundary-layer estimate and the collision-deletion surgery, but replaces them with an unproved trace semigroup and a coordinate-reset argument that does not control the physical Jacobi cocycle.
