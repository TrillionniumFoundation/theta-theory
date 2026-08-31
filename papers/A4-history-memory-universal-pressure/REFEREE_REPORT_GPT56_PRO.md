# Independent Referee Report — GPT-5.6 Pro

**Manuscript:** A4 — History, Memory, and Universal Pressure  
**Editorial standard:** *Annals of Mathematics*, *Acta Mathematica*, *Inventiones Mathematicae*, or *JAMS*  
**Recommendation:** **Reject**  
**Review object:** SHA-256-pinned eleven-paper source archive `566335121763abaa7ed8ed2280a3b4345877777e8bedbd80f4eef0a6b48745e2`

## Executive assessment

The manuscript combines a Yosida-regularized Mori–Zwanzig identity, complete-history Markovization, a conditional log-Laplace tower, a proposed history generator, and a claimed short-memory/diffusion tangent for prepared Sinai billiards. The bounded-operator identity and the conditional-expectation tower are correct general facts. They are not the advertised model-specific theorem.

The nontrivial conclusions are reached in one of three ways: the needed convergence is placed inside an assumption packet; the complete past is retained, making Markovization tautological; or the unproved A3 full path LDP is imported. Consequently the paper proves no Sinai-specific memory decay, no history semigroup with a constructed generator, no Markov tangent, and no universal pressure theorem.

## Major mathematical objections

### 1. The proved Mori–Zwanzig statement is an abstract bounded-operator identity

For a bounded Yosida approximation and a bounded projection, the Dyson/Duhamel calculation gives the displayed decomposition. This fact is model independent. The paper does not analyze a concrete resolved space, conditional projection, singular Liouville generator, or billiard domain.

Calling this “exact coarse dynamics for Sinai billiards” adds interpretation, not mathematics. To earn the model-specific claim, the authors must specify the Hilbert/Banach setting, domains of \(L\), \(QLQ\), and \(PL\), and prove that the relevant observables belong to them.

### 2. The unregularized orthogonal dynamics theorem assumes the difficult conclusion

The packet governing the passage from Yosida approximants assumes that the closure of \(QLQ\) generates the desired orthogonal semigroup and that both propagators and memory integrands converge uniformly on compact time intervals when applied to the observable. Those assumptions are essentially the theorem.

Dominated convergence after assuming the required convergence is formally valid but has no model-specific content. No nontrivial billiard observable is shown to satisfy the packet. The classical orthogonal-dynamics formula therefore remains conditional.

### 3. Complete-history Markovization is canonical and underspecified

Every stochastic process can be made Markov by retaining its entire past. A rigorous construction still requires a Polish history space, a family of kernels \(K_t\), measurable concatenation, stationarity/time homogeneity, and consistency across horizons. These details are not fully specified.

Even after repair, the construction gives no finite-dimensional closure, no memory decay, no computable kernel, and no new theorem about billiards. It merely relocates all non-Markovian information into an infinite-dimensional state.

### 4. The proposed Markov/diffusion tangent is an assumption list, not a theorem

The manuscript assumes concentration of prepared memory kernels and a joint invariance principle for integrated orthogonal forces. It does not define a scale-indexed family of resolved equations, convergence topology, initial-data class, limiting well-posedness, or a stability estimate.

An invariance principle for homological currents does not automatically transfer to an orthogonal force produced by an arbitrary projection. That force is projection dependent and generally a different observable. The required joint limit must be proved.

### 5. The “universal static pressure” is inherited from A3

The variational pressure, phase set, tilt LDP, and random-root conclusions all depend on A3's unproved full good path LDP. The finite-horizon ratio of partition functions is algebraic. Its long-time identification with a universal variational pressure is not.

No amount of conditional-expectation algebra can supply the missing rate function or its effective domain.

### 6. A regular conditional kernel does not automatically have the required generator

A Markov family on histories need not define a strongly continuous Feller semigroup on a chosen Banach space. The paper does not establish:

- the state topology;
- Feller or strong continuity;
- a core of cylinder functions;
- the domain of the generator \(\mathcal A_\Psi\); or
- that \(e^\Phi\) belongs to that domain.

Thus

\[
e^{-\Phi}\mathcal A_\Psi(e^\Phi)
\]

is a formal exponential transform, not a constructed nonlinear generator. The claimed finite-dimensional theta-HJB additionally requires a sufficient statistic, a limiting diffusion generator, and a comparison theorem.

### 7. The nonlinear tower is a generic conditional-expectation identity

The equation

\[
\log E[e^F\mid\mathcal F_r]
=
\log E[\exp(\log E[e^F\mid\mathcal F_s])\mid\mathcal F_r]
\]

holds for every filtered probability space. Renaming it “dynamic pressure” does not derive a new semigroup from billiard mechanics. The manuscript conflates exact bookkeeping at the full-history level with closure on a reduced state.

### 8. Mechanical selection of the entropic coefficient remains unproved

A Lagrange multiplier conjugate to a preparation constraint is not automatically the coefficient of a certainty equivalent for an arbitrary terminal payoff. The paper defines a calibrated ray and reuses the scalar. This is a modeling identification and must be labelled as such.

### 9. Phase labels are bookkeeping, not closure

It is correct that different stationary phases carry different conditional kernels. Retaining a phase label prevents an ill-typed mixture. But existence, selection, and regularity of those phases still depend on A3. The observation does not constitute a theorem of the advertised depth.

## Dependency assessment

A4 cannot be treated as a source of established history generators or universal pressure in C1/C2. Its only unconditional results are general functional-analytic/probabilistic identities. Every model-specific downstream use must be marked conditional on new Sinai-specific theorems.

## Minimum viable reconstruction

The paper should be split. One short abstract note could state the domain-safe Yosida identity with honest scope. A separate paper would need to construct, for a fixed billiard model and fixed projection, the orthogonal semigroup, memory estimates, history Feller semigroup, and a proved homogenization/short-memory limit.

## Recommendation

**Reject.** Correct universal identities are presented as though they close difficult Sinai-specific analytic interfaces. They do not, and the paper has no independent top-journal theorem.
