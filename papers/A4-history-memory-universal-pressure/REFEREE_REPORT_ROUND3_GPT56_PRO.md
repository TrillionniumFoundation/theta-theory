# Round-Three Referee Report — GPT-5.6 Pro

**Manuscript:** A4 — *Exact History Dynamics, Domain-Safe Memory, and Universal Excess Path Pressure*  
**Editorial standard:** *Annals of Mathematics*, *Acta Mathematica*, *Inventiones Mathematicae*, or *Journal of the AMS*  
**Recommendation:** **Reject**  
**Reviewed revision:** `revision/round3-full-positive-closure-11paper-2026-08-30@6a31720e5b0b6ab156b575f947596f9b66f56efe`  
**Controlling module:** `ROUND3_POSITIVE_CLOSURE.tex`, blob `52c09286c7e018f87a17acc5f96ea2271044199b`

## Executive assessment

The manuscript has moved in a mathematically healthier direction. It abandons the formal semigroup `e^{tQLQ}` as a primitive object, defines memory through a compressed Koopman resolvent, recognizes complete history as the exact state, and attempts to distinguish a general Ray realization from a quantitatively mixing spectral phase.

Nevertheless, the active paper contains two direct errors. First, it asserts uniform-norm strong continuity of a Feller semigroup on the Ray completion for every stationary prepared law; right continuity of sample paths does not imply such uniform convergence on all bounded continuous functions. The repository’s own hostile audit corrected this to bounded-strict continuity in a separate file, but that correction is not included in the controlling manuscript. Second, the normalized Feynman–Kac log transform used in the paper does not satisfy the claimed nonlinear tower unless the normalizing function is multiplicative or a Doob normalization is performed. This is an elementary algebraic failure in one of the headline theorems.

The more ambitious claims—exponentially decaying memory after adjoining pole modes and a joint rough diffusion tangent—remain sketches resting on A2 and A3, whose load-bearing theorems are not established.

## Improvements relative to the preceding circulation

1. The exact memory identity no longer assumes that `QLQ` generates a semigroup.
2. The resolved projection and the prepared `L²` space are typed explicitly.
3. The paper attempts a general measurable history realization and a stronger regularity theorem only on spectral phases.
4. It formulates a compressed-resolvent transfer function that is a legitimate algebraic object in finite resolved dimension.

These are real improvements and could support a focused abstract paper after the errors below are corrected.

## Major mathematical objections

### 1. The general Ray theorem claims the wrong topology

The active theorem states that for every stationary prepared law, the Ray completion carries a strongly continuous Feller contraction semigroup, and its proof says that right continuity of paths gives

\[
P_tF\to F
\]

uniformly on the closure of the Ray algebra.

This implication is false in general. A right process on a noncompact Polish state space can be Feller without its semigroup being strongly continuous in the sup norm on all of `C_b`. Pointwise or compact-uniform convergence does not become global uniform convergence merely because the operators are contractions.

The repository’s internal hostile audit identified this exact issue. The separate file

```text
revision/round3-rereview/A4_RAY_FELLER.tex
```

replaces the general claim by strong continuity in the bounded-strict topology and reserves norm-strong continuity for the exposed spectral `BUC` phase. That replacement is not input by the active `main.tex`. The controlling theorem is therefore the version already rejected by the internal audit.

### 2. The normalized Feynman–Kac transform does not have the asserted tower

The paper defines the linear Feynman–Kac semigroup

\[
P_t^\Psi F(h)
=E_h\left[e^{\int_0^t\Psi(H_s)ds}F(H_t)\right]
\]

and then

\[
\mathcal E_t^\Psi F
=\log P_t^\Psi(e^F)-\log P_t^\Psi1.
\]

In general,

\[
\begin{aligned}
\mathcal E_s^\Psi(\mathcal E_t^\Psi F)
&=\log P_s^\Psi\left(
\frac{P_t^\Psi(e^F)}{P_t^\Psi1}
\right)-\log P_s^\Psi1,
\end{aligned}
\]

which is not

\[
\log P_{s+t}^\Psi(e^F)-\log P_{s+t}^\Psi1.
\]

The denominator `P_t^Psi 1` is state dependent and sits inside the outer semigroup. Thus the claimed exact nonlinear tower is false.

There are standard correct alternatives:

- use the unnormalized logarithmic semigroup `F -> log P_t^Psi(e^F)`;
- construct a normalized Doob semigroup using a positive eigenfunction and eigenvalue; or
- use two-parameter finite-horizon conditional canonical operators whose normalization is consistent with the remaining horizon.

The current theorem uses none of these.

### 3. The nonlinear generator formula is consequently not the generator of a semigroup

Because the normalized family above is not a semigroup, its derivative

\[
e^{-F}\mathcal A_\Psi(e^F)-\mathcal A_\Psi1
\]

cannot be advertised as the generator of an exact nonlinear semigroup. It is the first-order derivative of a normalized family at zero time, but the Hille–Yosida/dynamic programming interpretation does not follow.

The later C2 repair file uses a normalized Doob transition semigroup, illustrating the missing construction. That repair is not reflected in A4’s active theorem.

### 4. The inverse-Laplace existence statement is underproved

The finite-dimensional compressed resolvent

\[
G(z)=P(z-L)^{-1}P
\]

is strictly accretive for `Re z>0`, so its invertibility there is plausible. The paper then defines

\[
\widehat K(z)=zP-PLP-G(z)^{-1}
\]

and infers from `O(1/z)` in sectors the existence of a unique causal locally integrable operator-valued distribution.

Analyticity and one asymptotic bound do not by themselves establish the boundary growth and Hardy/Paley–Wiener conditions required for a locally integrable kernel. At most they suggest a causal distribution of finite order. The class, topology, and inversion theorem must be stated precisely.

### 5. “Adjoining pole modes” is not a proved realization theorem

The memory-decay theorem says that poles of `G^{-1}` are zeros of `det G`, that their residue ranges can be added to the resolved space, and that after finitely many such enlargements the memory kernel decays exponentially.

This is not established. A zero of a compressed transfer function is not automatically a Koopman resonant state that can be represented by adjoining its residue range. The residue of `G^{-1}` already maps inside the resolved finite-dimensional space. One needs a state-space realization or a Schur-complement theorem identifying actual hidden modes in the full Hilbert space and proving that enlargement removes the zeros rather than creating new ones.

The claim that the procedure terminates after finitely many steps in a half-strip is therefore unsupported.

### 6. The spectral correlation expansion is imported from an unproved A2 theorem

The proof asserts that every entry of `C(t)=PU_tP` is a finite sum of resonant exponentials plus an exponentially decaying remainder. A2 concerns a collision transfer operator and a proposed vector/roof high-frequency theorem; it does not, in its current proof, establish the complete meromorphic suspension-flow resolvent expansion used here. Since A2’s temporal packet is itself not proved in the controlling source, the memory continuation and decay theorem have no established input.

### 7. The rough diffusion tangent lacks a defined scaling problem

The theorem states joint rough-path convergence of additive observables, every compressed-memory coordinate, resolved slow dynamics, and nonlinear semigroups. The manuscript does not define:

- the scale-indexed slow equation;
- its initial data and solution topology;
- how the compressed-memory coordinates enter that equation;
- a stability estimate for the vanishing-memory limit; or
- the class on which nonlinear semigroup convergence is uniform.

A martingale–coboundary decomposition for `g` alone does not automatically yield all these joint conclusions.

### 8. The paper depends on A3’s invalid full path LDP

The long-time pressure identity invokes A3’s good physical empirical-path rate and Varadhan’s lemma. A3’s active proof fails because of the one-big-excursion obstruction. The static pressure and phase conclusions in A4 therefore remain conditional.

### 9. The controlling manuscript is not standalone

The active paper is only a preamble and one input module. It assumes the prepared path laws, graph completion, A2 spectral objects, A3 rate, and several weights without reconstructing them as definitions or precise cross-paper theorem references.

## Editorial recommendation

**Reject.** The compressed-resolvent construction is the strongest idea in the revision and may deserve a separate, carefully scoped functional-analytic paper. The current manuscript must first incorporate the bounded-strict Ray theorem, replace the false normalized Feynman–Kac tower by a genuine Doob or two-parameter construction, state a valid inverse-Laplace theorem, and prove any memory-decay realization. The Sinai diffusion and universal-pressure layers should remain absent until A2 and A3 are independently established.