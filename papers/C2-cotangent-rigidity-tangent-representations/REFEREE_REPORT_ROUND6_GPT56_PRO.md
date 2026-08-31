# Round-Six Independent Referee Report — GPT-5.6 Pro

**Manuscript:** C2 — *Cotangent Rigidity and Tangent Representations Across Deterministic Platforms*  
**Editorial standard:** *Annals of Mathematics*, *Acta Mathematica*, *Inventiones Mathematicae*, or *Journal of the AMS*  
**Recommendation:** **Reject**  
**Reviewed revision branch:** `revision/round6-referee-positive-closure-11paper-2026-08-31`  
**Reviewed branch head:** `fb2ccfafab262f31f5b6f960df23e31258a59223`  
**Reviewed tree:** `2d3992ea12cfd513359a5f204bb1c2ae027bc7c4`  
**Active controlling module:** `ROUND6_POSITIVE_CLOSURE.tex`, blob `fd64714a6ebedf8dea791caf84bb1bc2132e52cf`

## Editorial summary

The finite likelihood is now correctly written as a complete-history conditional-expectation martingale, and the pressure tangent/memory formula is at least placed in one Doob Hilbert space with one orthogonal projection. Those are real improvements in typing.

The paper nevertheless contains an explicit false theorem: its cotangent null space includes constants, yet it claims that quotient-equivalent potentials have the same integral under every invariant probability. Potentials differing by `1` are quotient-equivalent but their integrals differ by `1`. The optional-projection theorem also depends entirely on A4's impossible convergence of deterministic complete-history Dirac kernels to a nondegenerate diffusion kernel. Platform coercivity and source-response commutation are assumed rather than proved. The manuscript therefore does not establish the announced cross-platform rigidity.

## Major mathematical objections

### 1. The cotangent characterization is false because constants are quotiented out

The paper defines

\[
\mathscr N_W=
\overline{\operatorname{span}}
\left(
\mathbb R\mathbf1+
\{U-U\circ\Theta_t\}
\right).
\]

Thus `F` and `F+1` represent the same quotient class in

\[
\mathscr A_W/\mathscr N_W.
\]

`thm:r6-c2-cotangent` then states that two potentials have the same integral under every invariant finite-weight phase if and only if they have the same quotient class. But for every invariant probability `nu`,

\[
\nu(F+1)-\nu(F)=1.
\]

This is a direct counterexample to the theorem as written.

One may quotient coboundaries when characterizing equality of integrals, or quotient constants and coboundaries when characterizing equilibrium phases/pressure modulo additive constants. These are different equivalence relations. The manuscript conflates them. The Hahn–Banach proof also relies on a separator annihilating constants and hence cannot establish literal equality of probability integrals.

### 2. Averaging a separator over rational time shifts is not justified

Even after correcting the constant issue, the converse proof says that a continuous signed separator can be averaged over rational time shifts to produce an invariant signed Radon functional. No averaging scheme, compactness theorem, or invariant mean is supplied. The rational-time group is infinite and noncompact; simple Cesàro averages require a Følner sequence and weak-star compactness in a dual space compatible with the weighted topology.

The dual of the dynamically Hölder algebra `mathscr A_W` is not automatically the weighted Radon measure space used earlier for `C_{W,0}`. A Hahn–Banach functional on the Hölder norm may be a distribution. Thus the claimed invariant Radon separator and its Jordan decomposition do not follow from the argument given.

A valid Livšic/annihilator theorem needs model-specific periodic-orbit separation or a proved dual characterization, not this abstract averaging paragraph.

### 3. The platform coercivity hypothesis is not a proved interface

The manuscript assumes

\[
I_\alpha(\nu)
\ge a_\alpha\nu(W_\alpha)-b_\alpha
\]

for every platform. A1 has not established a good path LDP or rate at all. A3's recurrent–defect rate and goodness are precisely disputed in the A3 report. B2's hard-sphere good rate is not proved, and its source domain does not establish the claimed Maxwellian exhaustion.

The phrase “for hard spheres this is read ... by lower-semicontinuous exhaustion” is not a proof of a rate–moment inequality. Without coercivity, the pressure may be infinite on the advertised weighted source ball, maximizing phases need not be compact, and the strict subdifferential theorem has no platform input.

C2 is therefore conditional on the strongest unproved conclusions of the preceding papers rather than a theorem derived from them.

### 4. The optional-projection convergence inherits the A4 Dirac-kernel contradiction

C2 explicitly says that A4 provides uniform convergence of complete-history kernels. In A4, however, the history contains the full graph-completed deterministic suspension state. Given that state, the future is deterministic and the conditional kernel is a Dirac measure. A sequence of Dirac measures cannot converge weakly to a nondegenerate Brownian rough-diffusion law.

Consequently the proof of `thm:r6-c2-optional` has no valid conditional-kernel input. Localization to a compact history set does not alter determinism. Stable convergence after multiplication by an initial-history variable is even stronger and cannot repair the contradiction.

The exact martingale lemma remains true, but convergence of optional projections is a separate quenched/conditional theorem that is not established.

### 5. The limiting filtration is changed without proof

The finite likelihood conditions on `mathcal F_t^{hist}`, the resolved-history filtration. The limit is written as conditioning on `mathcal F_t^X`. Passing conditional expectations through weak convergence requires convergence of filtrations or conditional kernels. Ordinary/stable path convergence does not imply

\[
E[Y_\varepsilon\mid\mathcal F_t^\varepsilon]
\to E[Y\mid\mathcal F_t].
\]

Information can be lost or retained in the limit. This is precisely why the invalid A4 conditional theorem was introduced. Without a correct version, identifying the limiting martingale with the diffusion optional projection is unjustified.

### 6. The Girsanov/BSDE theorem is a standard conditional corollary, not a microscopic result

Under the additional assumptions of a uniformly elliptic diffusion with bounded `C_b^3` coefficients, the exponential transform and Girsanov formula are standard. They do not validate the preceding microscopic likelihood convergence. The manuscript also defines `nu(t,x)` but then uses `u(t,x)`, a minor notation error revealing that this subsection is not integrated carefully with the earlier construction.

More substantively, an A4 rough homogenization limit need not be uniformly elliptic or possess the classical bounded `C^{1,2}` solution assumed. The theorem is therefore a separate smooth-diffusion statement under new hypotheses, not a representation established for the deterministic platforms in general.

### 7. The pressure-tangent/memory formula is valid only at fixed Doob data

For one fixed semigroup `P_tilde^Psi`, differentiating the entropic transform in the terminal payoff at zero indeed gives `P_tilde_t^Psi`. The Laplace-compressed resolvent formula is then formal but correctly typed.

The theorem goes further and states that “source differentiation on either side gives the same Duhamel insertion.” If the source changes the exposed potential `Psi`, then all of the following depend on the source:

- the eigenvalue and eigenfunction defining the Doob transform;
- the invariant measure `nu_Psi^D` and hence the Hilbert inner product;
- the generator `L_D`;
- the resolved subspace after identification; and
- the orthogonal projection `P_D`.

Differentiating only

\[
e^{t(L_D+\eta V)}
\]

misses derivatives of the conjugating eigenfunction, invariant density, pairing, and projection. The simple Duhamel formula proves commutation for a bounded additive perturbation in a fixed Hilbert realization, not the full source-response diagram claimed.

### 8. The compressed inverse and memory domain are not analyzed

The formula

\[
[P_D(z-L_D)^{-1}P_D]^{-1}
\]

requires invertibility of the finite compressed resolvent on the chosen domain. The paper does not state that domain, discuss transmission zeros, or invoke A4's proposed augmentation here. Even for `Re z>0`, a proof of strict accretivity on the compressed range is needed for a general Markov contraction that is not self-adjoint.

The assertion that A4's Volterra theorem applies directly also needs `V subset D(L_D^2)` and sufficient regularity for all source derivatives. The later memory-response claim exceeds those assumptions.

### 9. The contraction functor overstates derivative commutation

The exact finite-volume identity for a continuous linear observable is correct. First and second derivative commutation, however, requires a local analytic pressure chart on the pulled-back source and uniform derivative convergence. Such charts are unavailable for A1's physical current, unproved for A2/A3, and disputed for B2/B3.

For nonlinear admitted maps or exponentially good approximations, there is no adjoint `C^*` and no general pressure-derivative chain rule of the form stated. The theorem should distinguish linear finite-dimensional observables from nonlinear contractions.

### 10. Cross-platform synthesis remains bookkeeping rather than rigidity

The coproduct correctly prevents accidental identification of different platforms, but then most universal conclusions are componentwise restatements of standard contraction, Fenchel, Doob, and Girsanov facts. No nontrivial microscopic scaling map between Sinai and hard-sphere systems is constructed. Once the unproved component inputs are removed, there is no top-four-level cross-platform theorem left.

## Required reconstruction

A viable revision must:

1. separate equality-of-integrals modulo coboundaries from pressure equivalence modulo constants;
2. prove a genuine invariant-measure annihilator theorem in the declared weighted algebra;
3. derive, rather than assume, rate–moment coercivity for each valid platform;
4. replace the invalid complete-history conditional theorem by a filtration-compatible coarse-history result;
5. analyze convergence of optional projections and filtrations explicitly;
6. restrict memory commutation to fixed Doob data or differentiate the eigenfunction, invariant measure, and projection correctly; and
7. state derivative contraction only for maps and source charts for which a chain rule is actually proved.

## Recommendation

**Reject.** The exact martingale and fixed-Hilbert Doob formula are useful corrections, but the cotangent theorem is explicitly false because constants are quotiented out, optional-projection convergence rests on the impossible A4 conditional kernel, and platform coercivity is assumed. The paper remains a collection of conditional formal correspondences rather than a proved rigidity theorem.