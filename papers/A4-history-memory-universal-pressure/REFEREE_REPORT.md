# Referee Report

**Manuscript:** A4 — History, Memory, and Universal Pressure  
**Recommendation:** **Reject**  
**Standard applied:** Annals / Acta / Inventiones / JAMS  
**Review target:** pinned eleven-paper clean-main tree, SHA-256 `566335121763abaa7ed8ed2280a3b4345877777e8bedbd80f4eef0a6b48745e2`.

## Overall assessment

The manuscript combines two themes: a Yosida-regularized Mori–Zwanzig identity and a conditional log-Laplace semigroup on complete histories. The bounded-operator identity and the conditional-expectation tower are standard and essentially correct. They do not prove the advertised Sinai-billiard memory theory, nonlinear generator, or Markov/diffusion tangent.

The paper’s main conclusions are obtained by either (i) assuming the desired convergence in a named packet, (ii) using the tautological fact that the complete past Markovizes any stationary process, or (iii) inheriting the unproved full path LDP from A3. This is not top-journal-level closure.

## Major objections

### 1. The only fully proved memory identity is an abstract bounded-operator identity

For bounded \(L_\lambda\), the Dyson identity indeed gives the displayed regularized decomposition. This holds for any strongly continuous group and any bounded projection. No billiard-specific geometry, mixing, memory estimate, or prepared-phase analysis enters.

The result may be a useful domain-safe observation, but its novelty and scope must be stated honestly. Calling it an exact coarse dynamics theorem for Sinai billiards adds no content unless the resolved subspace, conditional projection, and relevant operator domains are analysed for that model.

### 2. The unregularized theorem assumes its conclusion

The packet `ORTH-GEN(A)` assumes that the closure of \(QLQ\) generates the orthogonal semigroup and that the Yosida propagators and memory integrands converge uniformly on compact time intervals when applied to \(A\). Those are precisely the difficult assertions needed to pass to the classical formula.

The proof then invokes dominated convergence. This is logically valid but mathematically tautological. No manuscript in this series verifies `ORTH-GEN(A)` for a nontrivial billiard observable. The paper must not advertise the classical orthogonal dynamics as established.

### 3. Complete-history Markovization is standard and underspecified

Any process can be Markovized by retaining its complete past. The theorem should specify a Polish topology on the infinite-past path space, a family of transition kernels \(K_t\) rather than a single unspecified “next-segment” kernel, measurability of concatenation, and the time-homogeneous property under stationarity.

Even after these details are supplied, this is a canonical construction, not a new memory theorem. It gives no finite-dimensional closure, decay of memory, or computable kernel.

### 4. The “Markov tangent” theorem is not a theorem

The statement assumes that the prepared memory kernels concentrate and that the integrated orthogonal forces satisfy the needed joint invariance principle. It does not define a scale-indexed family of resolved equations, the topology of convergence, initial-data class, well-posedness, or stability estimate. The proof consists of “the first term converges, the noise converges, stability completes the limit.”

Moreover, an invariance principle for homological currents does not automatically apply to an orthogonal force created by a chosen projection. The latter is a different observable with a projection-dependent dynamics. The manuscript has not proved the claimed v9 diffusion tangent.

### 5. The universal static pressure inherits A3’s unproved rate function

The variational pressure, tilt LDP, phase set, and random-root statements all rely on A3’s full good empirical-path LDP. Since that theorem is not established, none of these are available here. The exact finite-horizon ratio of partition functions is algebraic; its long-horizon identification with a universal excess pressure is not.

### 6. Existence of a history generator is assumed without a Feller/semigroup theorem

A regular conditional history kernel gives a Markov family. It does not imply that its transition operators form a strongly continuous Feller semigroup on a specified Banach space, that bounded cylinder functions form a core, or that \(e^\Phi\) lies in the generator domain.

Accordingly,
\[
e^{-\Phi}\mathcal A_\Psi(e^\Phi)
\]
is only a formal exponential transform until the linear semigroup, state space, domain, and core are constructed. The sentence that finite-dimensional contraction “gives” a theta-HJB also requires a proved sufficient statistic, a limiting diffusion generator, and an HJB comparison/regularity theorem.

### 7. The dynamic tower is conditional expectation, not a derived billiard semigroup

The tower law
\[
\log E[e^F\mid\mathcal F_r]
=\log E[\exp(\log E[e^F\mid\mathcal F_s])\mid\mathcal F_r]
\]
is a general identity. The discrete recursion is likewise the standard log-Laplace recursion once a kernel is given. No new universal nonlinear dynamics is produced by renaming this identity “pressure.”

### 8. Mechanical calibration of the entropic parameter remains unproved

As in A1, a Lagrange multiplier conjugate to a prepared path constraint does not force an agent’s or terminal functional’s entropic parameter. The paper defines a calibrated ray and then uses the same scalar in the log-Laplace transform. That is a convention, not a consequence of Liouville mechanics.

### 9. Phase-resolved consistency is a bookkeeping observation

Each chosen stationary phase has its own conditional laws. The need to retain a phase label is correct, but it is not a theorem of comparable depth to the claims in the abstract. Existence and selection of those phases remain dependent on A3.

## Editorial recommendation

**Reject.** The paper contains correct general identities but no proved Sinai-specific memory, generator, homogenization, or universal-pressure theorem. A new submission should separate an abstract functional-analytic note from any genuinely model-specific result and prove the latter independently.
