# Round-Nine Independent Referee Report — GPT-5.6 Pro

**Manuscript:** B4 — *Microcanonical Excess-Pressure Semigroups and Kinetic Theta-Generators*  
**Editorial standard:** *Annals of Mathematics*, *Acta Mathematica*, *Inventiones Mathematicae*, or *Journal of the AMS*  
**Recommendation:** **Reject**  
**Reviewed revision branch:** `revision/round9-referee-positive-closure-11paper-2026-08-31`  
**Payload-host branch head at review lock:** `a8c0c551f5f8614856a9d433e78b2eb92a5dcfa1`  
**Registered round-nine payload SHA-256:** `cf230322211332af59a7883af1b669eeb9b4f7e9f4220fc24712c634bda17716`  
**Reviewed registered source:** `revision/round9-referee-final/B4_LAW_CORE_TRUNCATED_COMPARISON.tex`  
**Reviewed source SHA-256:** `a65a15773f288454ad772fe8936081f9f49f98cbcb3beada728328cd89921817`  

## Evidence boundary

At the review lock, the branch stored the checksum-pinned round-nine payload while the paper-level `main.tex` files still loaded the round-eight modules; the repository publication workflow was queued. I independently verified the payload hash, unpacked it, and ran the repository materializer successfully, producing byte-identical paper-level `ROUND9_POSITIVE_CLOSURE.tex` files. This report therefore reviews the exact registered round-nine theorem text. It does not treat a queued workflow, a clean build, theorem/proof counts, or an internal hostile-regression script as evidence that the mathematical claims are true.

## Executive assessment

The revision correctly removes repeated initial preparation from the transition action, uses a terminal-value sign in the corrector equation, and tries to compare entropy-truncated Hamiltonians before removing the truncation.

The exact finite-state construction remains ill-typed: the manuscript alternates between a semigroup on probability laws and its dual semigroup on observables. The displayed log-Laplace “tower” does not act on the class of functions it is said to act on. The resolvent core and nonlinear generator inherit the same confusion. Independently, the fixed-truncation comparison proof caps the cotangent only by changing the penalty where the derivative is large, which is not legitimate.

## Decisive objections

### 1. The log-Laplace semigroup is ill-typed

The state semigroup
\[
 \mathscr U_\varepsilon(t):\rho\mapsto(\Phi_t)_\#\rho
\]
maps probability laws to probability laws. The paper first calls \(\Phi(\rho)\) an observable on law space. It then defines
\[
 \mathscr V_\varepsilon(t)F(\rho)
 =\mu_\varepsilon^{-1}\log
 \int e^{\mu_\varepsilon F(\eta)}
 \,d(\mathscr U_\varepsilon(t)\rho)(\eta).
\]
Here \(\eta\) is a microscopic state, so \(F\) must be a microscopic-state observable, not a law functional.

If \(F\) is a law functional, \(F(\eta)\) is meaningless. If \(F\) is a microscopic observable, \(\mathscr V_\varepsilon(t)F\) is a functional of the initial law, and composing it as a Markov semigroup on microscopic terminal functions is not the claimed “tower on the complete law state.”

### 2. The resolvent is applied on the wrong side of the semigroup

The manuscript defines
\[
 R_{\lambda,\varepsilon}
 =\lambda\int_0^\infty e^{-\lambda t}\mathscr U_\varepsilon(t)\,dt,
\]
which is a resolvent acting on *states*. It then applies \(R_{\lambda,\varepsilon}\) to observables \(\Phi\) and uses the observable-generator identity
\[
 \mathbb A R_\lambda\Phi=\lambda(R_\lambda\Phi-\Phi).
\]
That identity belongs to the dual Koopman/Markov semigroup on functions. The two semigroups and generators are not identified or even notated separately.

Thus Lemma `r9-b4-core` is not a typed statement.

### 3. Yosida approximation does not prove the announced graph core

Even after replacing \(R_\lambda\) by the observable resolvent, Yosida approximations converge in graph norm only for functions already in the generator domain. Uniform finite-coordinate approximation on a compact set does not imply convergence of generator images. The hard-sphere boundary generator is precisely where ordinary Stone–Weierstrass approximation fails to control traces.

The density of the proposed algebra in the graph domain is therefore unproved.

### 4. The finite-order corrector uses a nonexistent closed order-\(j\) propagator

The BBGKY/ledger hierarchy couples order \(j\) to higher orders. The manuscript introduces an “actual finite triangular generator at order \(j\)” and a backward propagator \(V_{j,\varepsilon}\) without constructing a closed evolution on that level. The asserted \(j!C^jT^{j-1}\) graph bound is the theorem needed to justify the infinite corrector series, not a consequence of its definition.

### 5. Applying the law generator to \(e^{\mu F_\varepsilon}\) does not produce the microscopic nonlinear generator claimed

If the law state evolves deterministically, the generator on law functionals obeys an ordinary chain rule. The large-deviation exponential Hamiltonian arises from the random microscopic empirical process, not from exponentiating a deterministic law evolution unless the state/observable duality and initial-law randomness are handled explicitly.

The paper has not constructed the Markov process whose nonlinear generator is
\[
 \mu^{-1}e^{-\mu F}\mathbb A_\varepsilon e^{\mu F}.
\]

### 6. The fixed-\(M\) comparison penalty leaves the source core

At a doubled maximum,
\[
 |\langle f-g,\phi_j\rangle|=O(\sqrt\eta),
\]
so the derivative coefficient in
\[
 \frac1{2\eta}|\langle f-g,\phi_j\rangle|^2
\]
is \(O(\eta^{-1/2})\), not uniformly bounded. The statement that one can “smoothly saturate” the derivative without changing the penalty near the maximizing pair is unsupported: saturation changes the test exactly when this coefficient is large.

For fixed \(M\), the control ratio \(q\) is bounded, but the Hamiltonian still contains the unbounded doubled cotangent. State continuity estimates must be uniform in that cotangent; none are given.

### 7. Comparison does not pass automatically through entropy truncation

The values \(S^M\) may increase to a variational limit, but viscosity comparison for every truncated Hamiltonian does not imply comparison for the untruncated Hamiltonian. One needs local uniform convergence of Hamiltonians on the relevant test jets, stability of sub/supersolutions, and a proof that balance repair after truncating \(q\) preserves endpoints and incurs vanishing cost.

The short paragraph does not establish these facts.

### 8. The action compactness and lower recovery are imported from unresolved B2

The semigroup law for a correctly additive action is formal. Finiteness, attainment, closed balance, compact sublevels, and a dense recovery class are exactly the unproved B2 LDP interfaces.

## Dependency assessment

B4 cannot be a convergence hub until B2 and B3 are valid. It additionally requires its own correctly typed observable semigroup, graph core, and comparison theorem.

## Required reconstruction

The paper must distinguish:

1. microscopic state process;
2. pushforward semigroup on laws;
3. dual semigroup on microscopic observables;
4. functions on law space; and
5. the nonlinear generator of the empirical process.

After that, a core theorem must be proved on the correct dual generator. Comparison should use a source topology for which diagonal coercivity and Hamiltonian continuity are simultaneously quantitative.

## Recommendation

**Reject.** The exact finite semigroup and resolvent are not typed consistently, so the nonlinear-generator theorem is not defined. The comparison argument also remains incomplete.
