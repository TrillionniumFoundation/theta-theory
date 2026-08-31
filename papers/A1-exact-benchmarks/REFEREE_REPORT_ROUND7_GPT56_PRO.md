# Round-Seven Independent Referee Report — GPT-5.6 Pro

**Manuscript:** A1 — Exact Benchmarks  
**Editorial standard:** *Annals of Mathematics*, *Acta Mathematica*, *Inventiones Mathematicae*, or *Journal of the AMS*  
**Recommendation:** **Reject**  
**Reviewed revision:** `revision/round7-referee-positive-closure-11paper-2026-08-31@b1e3d17f59ca9bb1a04d4ac9157f10dc333f9607`  
**Controlling module:** `ROUND7_POSITIVE_CLOSURE.tex`, blob `3abe8fb4302352d2d905ab3e014c4d66fdb83c6f`

## Executive assessment

Round seven makes two real improvements. It replaces the one-seam section by a proposed two-coordinate germ completion, and it no longer invokes an isotropic Hölder spectral gap for an invertible baker map. The full-port work layer also removes the previous positive-measure collar defect, and the mechanical/valuation identification is now correctly stated as conditional on equality of likelihood cocycles.

The central return map is nevertheless not well defined on the declared cell complex. The anisotropic transfer theorem is then built on the wrong partition, and the autonomous Hamiltonian realization is asserted through mutually incompatible support requirements. Even after those defects were repaired, the corrected Bernoulli benchmark would not meet a top-four novelty threshold.

## Major mathematical objections

### 1. The declared biseam complex omits the preimage seams of the next-port partition

The cells are only

\[
I_i\times J_k.
\]

On such a cell the physical formula

\[
Q_i(q)=\frac{q-s_{i-1}}{p_i},\qquad P_i(p)=t_{i-1}+p_ip
\]

is affine, but the target vertical label \(j\) changes whenever

\[
Q_i(q)=s_j,
\qquad	ext{i.e.}\qquad
q=s_{i-1}+p_i s_j.
\]

These lines are generally interior to \(I_i\times J_k\); they are not among the source seams \(q=s_\ell\). At such a source point the target has two oriented vertical germs, while the source point carries no side label relative to this new preimage seam. Thus the instruction “take the unique oriented germ” is false: there are two possible target germs and no datum selecting one.

Consequently \(F_a\) is not a single-valued stratum-preserving map on the announced 16-cell complex. The source partition must be refined by all branch preimages of every vertical seam. Once this is done, further iterated preimages appear in the transfer/current calculus. The present finite biseam complex does not contain them.

### 2. The anisotropic spectral packet is built on the same incomplete partition

The proof repeatedly says that \(F_a\) is affine on every closed cell and that differentiating the finite cell indicators produces all required face and corner currents. Because the next-port preimage seams are missing, both statements are false. Pullback creates discontinuities on internal lines not represented in \(\mathcal C_1\), so the proposed operator does not preserve the displayed cell/trace space.

There are further unresolved functional-analytic issues:

- the Fourier \(\ell^1\) norms are introduced cellwise without boundary extension conventions compatible with nonperiodic affine restrictions;
- the “zero unstable average” subspace used in the Lasota–Yorke estimate is not defined or shown invariant;
- the compact embedding with negative stable regularity and independent current coordinates is asserted rather than proved;
- simplicity of the peripheral spectrum is inferred from the symbolic full graph without proving that the physical quotient of the proposed current space has no additional peripheral distributions; and
- the Keller–Liverani iteration requires a fixed compatible scale, while the domain/codomain losses and moving-cell identifications are not formulated as one perturbation theorem.

This is the load-bearing theorem of the revision. A two-paragraph Fourier heuristic is not a proof of an anisotropic spectral theory with moving polyhedral currents.

### 3. The autonomous suspension uses incompatible disjoint-support claims

The text asks for four exact symplectic isotopies supported in pairwise disjoint Darboux collars, one for each source branch, and then sums their Hamiltonians. But a baker branch carries an entire vertical strip onto a horizontal strip that crosses the source collars of the other branches. A Hamiltonian diffeomorphism compactly supported in a source collar cannot transport its points outside that support while remaining the identity outside it. If the collars are enlarged to contain both source and target, they are no longer pairwise disjoint.

The statement that a “relative Moser correction” fixes this does not solve the support obstruction. Moser’s method adjusts symplectic forms; it does not automatically realize a prescribed global return map, with exact return time and flat matching jets, by four noninteracting compactly supported Hamiltonians. No actual Hamiltonians, collars, or gluing maps are supplied.

### 4. The physical response claim remains far stronger than the construction

Even after refining the section, an all-order physical response theorem must control the full iterated singularity partition generated by the invertible map, not only the original vertical/horizontal seams. It must also identify the physical invariant distribution, prove its spectral gap on a precise anisotropic space, and establish boundedness of every shape derivative and saltation current. The present “finite incidence types” argument does not address the dynamically generated cuts.

### 5. The corrected content remains below the top-four threshold

The symbolic factor is a deliberately engineered Bernoulli shift. Its pressure, conditioning, canonical tilt, and response are standard and explicitly solvable. A rigorous Hamiltonian realization and a careful response note could be useful, but the paper would still be a benchmark construction rather than a theorem of the depth expected by the four journals.

## Required reconstruction

A valid revision must first refine the graph completion by all one-step preimage seams and prove that the resulting map is a genuine bijection. It must then construct a real anisotropic Banach scale invariant under the complete transfer operator, including dynamically generated currents, and supply an explicit global Hamiltonian suspension rather than a support-incompatible existence paragraph. The calibration theorem should remain expressly conditional.

## Recommendation

**Reject.** The proposed return map is not well defined on its declared biseam complex; the spectral and Hamiltonian theorems therefore lack a mathematical object on which to operate. Correctly reconstructed benchmark content would still not reach a top-four novelty standard.
