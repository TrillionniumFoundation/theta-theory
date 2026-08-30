# Revision-Round Referee Report — GPT-5.6 Pro

**Manuscript:** A4 — *Exact History Dynamics, Domain-Safe Memory, and Universal Excess Path Pressure*  
**Editorial standard:** *Annals of Mathematics*, *Acta Mathematica*, *Inventiones Mathematicae*, or *Journal of the AMS*  
**Recommendation:** **Reject**  
**Reviewed source:** `main@ae2fdc16bf1ad4a6b58cca6020a7b8b61236e2ad`, manuscript blob `964e23e96bb82caadbfc5993adf305ff12e0d641`  
**Revision provenance:** the repository's available eleven-paper revision ref contains no revised A4 manuscript; the controlling source on `main` is reviewed.

## Overall assessment

The paper combines an exact Yosida-regularized Mori–Zwanzig identity, complete-history Markovization, a conditional log-Laplace tower, an exponential-transform generator, and a proposed short-memory diffusion tangent. The revised exposition is more honest than the initial presentation: it distinguishes the bounded regularized identity from the unbounded orthogonal-dynamics formula and explicitly labels the latter conditional on an ORTH-GEN packet.

That honesty also exposes the editorial difficulty. The unconditional results are generic operator or probability identities. The model-specific Sinai memory theorem, history generator, and Markov tangent are assumed, inherited from A3, or left as formal constructions. Consequently the manuscript does not establish a new Sinai-billiard result of top-journal depth.

## Major objections

### 1. The exact Yosida identity is universal bounded-operator algebra

For a bounded Yosida approximation \(L_\lambda\) and a bounded projection \(P\), the displayed Dyson/Duhamel decomposition is correct. It applies to essentially any strongly continuous group and closed resolved subspace. No billiard singularity, mixing estimate, memory decay, or prepared-phase geometry enters the proof.

The result may be useful as a domain-safe formulation, but its scope must be stated accordingly. Calling it exact coarse dynamics for Liouville-prepared Sinai billiards does not add model-specific content unless the resolved subspace, projection, Liouville domain, and relevant observables are analyzed for that model.

### 2. The classical orthogonal-dynamics theorem assumes the hard part

The packet \(\mathrm{ORTH\mbox{-}GEN}(A)\) assumes that the closure of \(QLQ\) generates the orthogonal semigroup and that the Yosida orthogonal propagators and memory integrands converge uniformly on compact intervals. These are essentially the conclusions needed to pass to the classical formula.

Given these assumptions, dominated convergence is valid. But no nontrivial Sinai observable is shown to satisfy the packet. Thus the manuscript does not prove the unregularized Mori–Zwanzig formula for the advertised billiard setting; it proves a conditional implication.

### 3. Complete-history Markovization is canonical, not a new memory theorem

Any process can be made Markov by retaining its complete past. The manuscript correctly avoids claiming a finite-dimensional Markov state. A rigorous treatment should still specify the history topology, the family of time-indexed transition kernels, measurable concatenation, and stationarity/time homogeneity.

Even after those details are supplied, complete-history Markovization gives no memory decay, no finite-dimensional closure, and no computable kernel. It is exact bookkeeping, not a Sinai-specific theorem.

### 4. The Markov tangent remains conditional and incorrectly transfers an invariance principle

The theorem assumes that the prepared memory kernels concentrate and that the integrated orthogonal forces satisfy a joint invariance principle “verified for the homological currents in v9.” An orthogonal force produced by a chosen projection is not the same observable as the homological current. Its invariance principle does not follow automatically.

The paper does not define a scale-indexed family of resolved equations, the convergence topology, initial-data class, limiting well-posedness, or a stability estimate. The proof consists of convergence of the memory term, assumed convergence of the noise term, and an unstated stability argument. This is a template, not a theorem.

### 5. The universal pressure layer inherits A3's unproved full path LDP

The variational pressure, canonical phase set, random-root limits, and finite-horizon pressure bridge all use the full good physical empirical-path rate from A3. Since A3 has not established that rate, none of the model-specific asymptotic statements can be treated as closed here.

The finite-horizon ratio of partition functions is exact algebra. Its long-horizon identification with a universal pressure and a microscopic phase law is conditional on A3.

### 6. The linear history generator is assumed rather than constructed

The manuscript writes “let \(\mathcal A_\Psi\) be the linear generator of the history process on a core of bounded cylinder functionals.” A regular conditional history kernel does not by itself imply a strongly continuous Feller semigroup on a specified Banach space, nor that bounded cylinders form a core.

The paper must define the state space and function space, prove the semigroup property and strong continuity, identify its domain, and show \(e^\Phi\in D(\mathcal A_\Psi)\). Without this, the exponential-transform formula

\[
e^{-\Phi}\mathcal A_\Psi(e^\Phi)
\]

is conditional notation, not a constructed nonlinear generator.

### 7. The exact nonlinear tower is a generic conditional-expectation identity

The history-space log-Laplace tower is mathematically correct but universal. It does not derive a reduced nonlinear semigroup from billiard mechanics. Renaming the conditional-expectation identity “dynamic pressure” should not be confused with proving an autonomous generator or an HJB equation on a lower-dimensional state.

### 8. The mechanical calibration claim remains too strong

A macro preparation may select a cotangent field conjugate to a constraint. It does not force every terminal work to use that scalar as its certainty-equivalent coefficient. The statement that the scalar is “not free” is true only after an explicit calibrated-ray convention has been imposed. It is not a consequence of the Mori–Zwanzig or path-LDP theory.

### 9. Phase-resolved consistency is bookkeeping

Different maximizing phases can have different conditional kernels, so a phase label is indeed necessary. This is a correct structural observation. It does not prove existence or regularity of those phases, which again depend on A3, and it is not an independent top-journal theorem.

## Status of prior objections

The revision genuinely improves the domain typing of the Mori–Zwanzig discussion and no longer silently writes an unproved \(e^{tQL}\). This closes one expository ambiguity. It does not establish ORTH-GEN, a Sinai-specific memory estimate, a history Feller generator, or the short-memory stochastic limit.

## Required reconstruction

The manuscript should be split. One abstract note could present the Yosida-regularized identity with honest generality. A separate model-specific paper would need to construct the orthogonal semigroup for a fixed projection, quantify memory kernels, build the history semigroup and its core, and prove a homogenization/short-memory theorem for the actual orthogonal force.

## Editorial recommendation

**Reject.** The unconditional mathematics consists of correct general identities; the advertised Sinai-specific memory, generator, and tangent results remain conditional or inherited from an unproved upstream rate theorem.
