# Round-Eight Independent Referee Report — GPT-5.6 Pro

**Manuscript:** C2 — *Cotangent Rigidity and Tangent Representations Across Deterministic Platforms*  
**Editorial standard:** *Annals of Mathematics*, *Acta Mathematica*, *Inventiones Mathematicae*, or *Journal of the AMS*  
**Recommendation:** **Reject**  
**Reviewed revision branch:** `revision/round8-referee-positive-closure-11paper-2026-08-31`  
**Reviewed branch head:** `ad2b5106678b29b7d9ffb3824f61ddbd141ac4b8`  
**Reviewed tree:** `00d7ef9edcddda26fc88962e206677f9b399bebe`  
**Active controlling module:** `ROUND8_POSITIVE_CLOSURE.tex`, blob `a53588607aff0ad3b5264bb4240dbc1855b9cfe0`

## Executive assessment

Round eight fixes several typing errors. The coboundary null set is now a closed linear span, constants are separated from integral equivalence, and source response is placed on a common transfer space rather than an `L2` trivialization by Radon–Nikodym derivatives between mutually singular Gibbs measures.

The revised theorem still fails. The Kato ODE is applied as though spectral projectors were differentiable bounded operators on one Banach space, whereas the upstream moving-singularity theory loses regularity from a strong space to a weak space. More fundamentally, the projector `P_eta` is introduced as the isolated spectral projector of the Ruelle operator and is then used as the Mori–Zwanzig resolved projection. A spectral projector commutes with the generator, so its compressed resolvent has zero memory. If `P_eta` instead denotes a physically chosen resolved observable subspace, it is not the Riesz projector governed by the Kato equation. The paper conflates these two different projections.

## Genuine repairs recognized

The following changes should be retained:

- `N_int` is explicitly a closed linear span;
- constants are included only in the pressure-null space;
- infinite-volume mutual absolute continuity is no longer assumed;
- finite-time likelihood cocycles are used where they are well defined;
- the causal memory sign is correct;
- nonlinear contractions are handled by test pullback rather than a fictitious linear adjoint.

## Major mathematical objections

### 1. The invariant-integral theorem is conditional on an unproved separator estimate

The converse direction assumes that every Hahn–Banach separating weighted functional satisfies

\[
\sup_{T\ge1}\frac1T\int_0^T
\int W\circ\Theta_t\,d|\mu|\,dt<\infty.
\]

This is a property of the arbitrary signed separator produced by Hahn–Banach, not merely of physical probability phases. The manuscript does not derive it from the A3 or B2 rate-moment bounds. Those bounds concern finite-rate positive laws, whereas the separator may be signed and need not lie in a rate sublevel.

The theorem is therefore a conditional functional-analytic statement, not an established platform result.

### 2. The Kato ODE is not typed on the upstream strong/weak scale

The paper assumes that

\[
[P_\eta',P_\eta]
\]

is a bounded operator on one common Banach space. In the moving billiard and shape-response constructions, parameter differentiation creates boundary currents and loses regularity: derivatives act from a strong space to a weaker space. A projector derivative need not map the strong space to itself.

Standard Kato parallel transport cannot be applied without either a no-loss common domain or a scale-valued connection with carefully controlled products. Neither is constructed. The one-line operator ODE ignores the principal domain issue of the series.

### 3. The paper conflates a spectral projector with a resolved-memory projector

The common-bundle subsection defines `P_eta` as the isolated Riesz spectral projector of the source-dependent Ruelle operator. The memory subsection then sets

\[
C_\eta(z)=P_\eta(z-L_\eta)^{-1}P_\eta
\]

and treats `P_eta` as the finite resolved projection of a compressed-memory problem.

For a spectral projector,

\[
P_\eta L_\eta=L_\eta P_\eta,
\]

so the resolved and unresolved subspaces are invariant and

\[
P_\eta L_\eta(I-P_\eta)=0.
\]

Consequently the Mori–Zwanzig memory kernel on that spectral subspace is identically zero. In the rank-one leading eigenspace,

\[
C_\eta(z)=(z-\lambda_\eta)^{-1}P_\eta
\]

and

\[
zP_\eta-A_\eta-C_\eta(z)^{-1}=0.
\]

This is not A4's nontrivial memory compression onto selected physical observables.

If `P_eta` is intended to be an arbitrary resolved-observable projection, it is not an isolated spectral projector and the Kato commutator equation does not apply. The central memory theorem is therefore either trivial or ill-typed.

### 4. Kato transport of the leading eigenspace does not transport the full Doob dynamics

Transporting the one-dimensional right eigenfunction range does not identify the full transfer Banach spaces, the dual eigenfunctional, multiplication operators, or an arbitrary finite resolved observable subspace. The Doob operator acts on the entire space, not only on the leading eigenspace.

The statement that finite-time likelihood derivatives “implement the same derivative” needs an intertwining theorem on the whole operator family, not just Kato transport of `Ran P_eta`.

### 5. The causal-memory derivative is formally correct but attached to the wrong object

The differentiation rule

\[
\nabla K=z\nabla P-\nabla A+
C^{-1}(\nabla C)C^{-1}
\]

is an algebraic identity when all operators share domains and `C` is invertible. Those assumptions are not proved. More importantly, because `P_eta` is spectral, the memory itself is zero and the formula has no connection to the physical memory theorem advertised by the paper.

### 6. Optional-projection convergence inherits A4's unresolved quenched theorem

The exact conditional-expectation martingale is correct. Passing it to a diffusion optional projection requires convergence of conditional kernels/filtrations, not merely path convergence. The proof cites A4's uniform quenched theorem, which is not established and whose memory/transfer inputs remain invalid.

No independent tightness or filtration-convergence argument is supplied here.

### 7. The finite-time/common-reference statement needs fixed support

The proof says that all finite-cylinder source laws have positive densities relative to one kernel. This holds for bounded potential changes on a fixed transition support. It can fail if geometry, controls, or platform changes create or remove admissible branches. The paper must restrict the statement to a fixed support chart and track zeros at its boundary.

### 8. The contraction theorem is elementary and does not close the platform interfaces

The identities

\[
Q_Y(\phi)=Q_X(\phi\circ\mathcal C)
\]

and

\[
I_Y(y)=\inf_{\mathcal C(x)=y}I_X(x)
\]

are the ordinary Laplace and contraction principles. They are correct when the upstream LDP and source domains exist. They do not prove any cross-platform scaling theorem, and they cannot compensate for the missing A3/B2 path rates.

### 9. Standalone novelty remains insufficient

After the invalid memory identification is removed, the unconditional content is a standard coboundary quotient under a strong averaging hypothesis, Kato perturbation of an isolated projector, an exact conditional-expectation martingale, and the contraction principle. This is not a standalone top-four theorem.

## Dependency assessment

C2 remains downstream of A2/A3/A4 and B2/B3. Its optional projection and memory claims cannot be used in D1. The exact history likelihood is valid, but every nontrivial limiting representation remains conditional.

## Required reconstruction

The paper must separate three objects:

1. the leading spectral projector used to normalize a Gibbs/Doob phase;
2. the arbitrary finite resolved-observable projection used in memory compression; and
3. the scale-valued connection needed when parameter derivatives lose regularity.

A valid covariant memory theorem must transport the full generator, invariant pairing, and resolved projection on a common domain. The invariant-separator theorem must also prove, rather than assume, the required weighted Cesàro compactness for its Hahn–Banach separators.

## Recommendation

**Reject.** The RN-trivialization error is repaired, but the manuscript now identifies the Ruelle spectral projector with the Mori–Zwanzig resolved projection. On the former the memory is identically zero; on the latter the Kato theorem used in the proof is unavailable.