# Response to the twentieth pipeline-aware referee report

**General Theta Foundations I — Revision 36**  
**Finite Alphabets, Spectral Gaps, and Hidden Memory**  
25 September 2026

Controlling report: `reviews/general-theta-foundations-i-v35-sharp-memory-pipeline-harsh-top4-r20-2026-09-25/REFEREE_REPORT.md`, frozen at `6da551c5b804b683240d5f5631e1c4f5689e21bd`. Reviewed publication: v35 at `aabc0731a0c913f7b9e75e6efc08f7af665bdf23`, native source `0ae43a2180d07bda18384697a33da48d3fc1562a`.

The report accepts the fixed-binary cube-root theorem, identifies a word/product quantifier gap in the representation-valued lemma, and asks for a genuinely finite noncommuting extension and a direct comparison with quantum-automata simulation. This revision addresses those mathematical requests without replacing the original theorem by a weaker conclusion. The new finite-alphabet results have two different geometries: sphere spectral gaps yield a polynomial exponent with a logarithmic order gap, while resonant monomial commands yield a matched cube-root order. A sparse-row implementation theorem separately prices finite-coin control.

The program prefix is retained. The article does not use that prefix, archive volume or revision count as evidence of journal significance. Its actual theorems, external inputs and scope are stated independently. Stable LaTeX labels below resolve to compiled numbers/pages in `evidence/THEOREM_LOCATIONS.json`.

## 11.1 / Section 4 — the word/product gap

**Repaired in the general lemma, with no product-sufficiency restriction.**

`lem:packet` in `word-packets.tex` assumes that the entire packet variable W is independent of sigma(Y,S), and states the endpoint condition as

```
P(S'=r | sigma(Y,S,W)) = T_W(S,r).
```

The product map g(W) may be many-to-one and the kernel T_W may distinguish all words. The proof writes each unnormalised endpoint centroid as the integral of `T_w(s,r) U_(g(w)) z_s`. It then removes the assignment by a pointwise maximum over endpoint directions. Only after that step does it push the word law forward to the product law. This proves the same orbit-distortion inequality for arbitrary full-word kernels.

The independent-word hypothesis would also allow averaging an endpoint kernel over product fibers by disintegration. The previous statement did not display that bridge. The new proof does not rely on leaving it implicit, or on assuming that the wordwise kernels were already constant on the fibers. Equal-product examples are explicitly discussed. Independence of the product *alone* would not suffice, since an identity-product spelling could leak a past variable.

`thm:packet-budget` states freshness relative to the earlier process and all private randomness. Ordered internal transitions compose to a word-dependent kernel, so the theorem now invokes precisely the lemma that was proved. The corrected result applies to noncommuting packets, collisions, the inherited circle construction and the separately defined compact-command application. Invariant directions may make Gamma zero, and that case is explicit rather than excluded by an unstated hypothesis.

## 11.7 / Section 5.4 — a broad finite-generator theorem

**Addressed by a finite spectral-gap criterion with a real command-time charge.**

`thm:spectral` assumes an absolute L2 gap of the fixed finite averaging operator on the complete mean-zero function space of the sphere. It is not a condition only on the defining representation, and density is not substituted for a gap. For m=d-1, it proves

```
c (N/log(N+1))^(m/2) <= W_(N,epsilon) <= W_(N,0) <= C N^(m/2).
```

The scope is fixed d, alphabet, signal and error `epsilon < rho/(2 sqrt(d))`. All competing hidden directions and time-dependent stochastic rows are allowed. The exponent `log W/log N -> m/2` is determined. The logarithmic gap between the two displayed orders is not hidden in a Theta statement.

`lem:mixing` derives uniform mixing for Lipschitz tests from the L2 gap, using the isometric action and sphere ball masses. `lem:finite-distortion` combines it with a quantization lower bound. At endpoint width k, `B_k=O(log(k+1))` *ordinary command slots* are used. This is the explicit difference from treating a fresh Haar matrix as one command. Packet contraction then yields both the peak converse and an occupation bound when widths at other epochs are unrestricted.

`lem:net-upper` constructs a rational stereographic spherical net. It gives an exact sparse convex update for every command, with a common radial shrinkage. The associated vector scale grows geometrically and the final decoder remains bounded. At most d+1 successors are required in a row. Only a vertex index persists; the real vectors specify the read-only program. For rational gate/seed data all atomic rows can be rational. The proof is for every word, not an average distribution.

The spectral gap is a strong analytic condition on a natural class, and its verification is not disguised as elementary. The next theorem gives an explicit fixed finite family to which an existing deep gap theorem applies.

## An explicit noncommuting rational alphabet

`thm:rational` uses the five commands I, Rx, Rx inverse, Rz and Rz inverse, where the nontrivial planar rotation blocks are `[[−7,−24],[24,−7]]/25`. These matrices, six seeds, three queries and the signal 1/10 do not depend on the horizon. All conditional probabilities lie in `[9/20,11/20]`.

The SU(2) lifts `(3I−4i sigma_x)/5` and `(3I−4i sigma_z)/5` have algebraic entries. Their eigenphase is irrational because the trace 6/5 is not an algebraic integer. Powers densely fill the two axial tori, whose Lie algebras generate su(2). Bourgain–Gamburd, *A Spectral Gap Theorem in SU(d)*, Theorem 1, therefore gives a gap for the symmetric walk; laziness gives an absolute gap. The sphere is a homogeneous quotient, so its averaging operator inherits that gap.

This proves

```
c_epsilon N/log(N+1) <= W_(N,epsilon) <= W_(N,0) <= C N,
```

while every separate positive minimum is four. There is no uncountable command alphabet, oracle supplying Haar rotations, or assumption that the individual rational-entry angle is badly approximable. The spectral-gap constant is not numerically evaluated. An exact finite bound is expressed in that constant. Finite gate checks do not prove the infinite-dimensional gap.

## A matched finite noncommuting class beyond a full-group character

`thm:monomial` treats finite real-orthogonal commands that permute r complex modes, optionally conjugate them and multiply them by bounded integer powers of one fixed badly approximable phase. With the specified finite seed/query sets and fixed signal, it proves

```
W_(N,epsilon) = Theta(N^(1/3)),    0 <= epsilon < rho/2.
```

The lower bound restricts to an identity/one-mode-rotation sublanguage and uses the corrected packet theorem. The upper works on the *entire* alphabet: a single register retains a mode and a resonant polygon label; permutations, conjugation, two adjacent vertices and an explicitly priced antipodal mixture yield sparse common rows. The latter mixture gives one common radial factor without a dense uniform redraw or an uncharged zero state.

`prop:no-character` supplies an at-most-five-command family generating a dense subgroup of `O(2)^r semidirect S_r`. Its defining real representation is irreducible, and any continuous one-dimensional character is trivial on each rotation torus because conjugation sends that torus to its inverse. Thus this is not obtained by applying the preceding character corollary to the *full* command group. We explicitly acknowledge that the converse uses a cyclic sublanguage and the upper uses monomial structure. We do not claim that all finite noncommuting sets have the same order.

At r=1 and rho=1/10 the original binary theorem is recovered with its original signal, seed set, error range and all-hidden-state quantifier. No earlier result is narrowed to secure the new conclusion.

## 11.2 / Section 6 — quantum-automata simulation and current versions

**The numerical quantum model is written explicitly and the strict-cutpoint boundary is demonstrated on the same family.**

`prop:qubit` gives an exact single-qubit implementation of the rational-gate family. The six seed states have Bloch vectors rho x; the command unitaries are the two fixed lifts and their inverses; the three queries are Pauli measurements. Seed resets and query rotations turn this into a dimension-two general one-way quantum automaton on a finite alphabet, with well-defined semantics on all words and the desired behavior on valid protocol words.

The current Chen–Wu paper is **arXiv:2604.07058v2, 27 August 2026**, with title *The State Cost of Classical Simulation of One-Way General Quantum Finite Automata*. Its Theorem 3.2 gives n^2+1 PFA states for strict-cutpoint language equivalence. Therefore a five-state PFA recognizes each fixed threshold language of this qubit automaton. Its Proposition 3.1 explains why there is no contradiction with our length-dependent width: stochasticization attenuates the deviation from the classical cutpoint by a positive length-dependent factor. Signs are preserved; fixed numerical probabilities and correlation are not.

This comparison is an explicit operational distinction, not the assertion that the 2026 result is about the same exact probability objective. Their asymptotic parameter is quantum dimension; ours is horizon length at fixed quantum dimension. The companion **arXiv:2605.10682v1** is discussed with its measure-once/prepare-test and strict-cutpoint conventions (in particular Theorem 14, Corollary 15 and Theorem 19). Its conclusions are not relabeled as uniform-probability simulation results.

The comparison with **Lumbreras–Ma–Thompson–Gu, arXiv:2608.19779v1**, is restored. Its Theorems 28–30 concern stationary repeated-history value/decision error and exact qutrit modeling. Our finite-horizon classical lower bound permits new, nonstationary machines and tests numerical terminal laws. The adjacent September symmetry paper **Chen, arXiv:2609.01451v1** is also considered; its behavioral-rank and strict-cutpoint memory questions are separated from numerical row accuracy. No first quantum/classical memory separation or exhaustive priority certification is claimed.

`LITERATURE_AUDIT.md` records precise inspected versions and theorem locations. The direct manuscripts, not summaries alone, were consulted for these comparisons.

## 11.4–11.6 / resource and compact-input distinctions

All new main alphabets are finite and fixed before the horizon is chosen. The inherited all-SO(d) theorem stays in the supporting article as a different model. The formal model paragraph states Borel dependence for that compact-input comparison, and gives the finite-triangulation argument for a Borel convex choice. It is not used to create a hidden infinite command alphabet in the new theorems.

The primary measure is explicitly nonuniform clocked stochastic branching-program width, with free epoch, horizon, row table, arithmetic and atomic real sampling. Available labels, including padding, are counted. Positive-probability counts are only usable under the actual proof test law. The command matrices of the upper constructions can be common across epochs, but the selected state alphabet and final decoder depend on N. One terminal coordinate query is requested, not jointly independent answers to all coordinates.

`thm:compiler` gives additional implementation content without conflating it with atomic exactness. A categorical row with at most L successors is sampled through a binary tree. Rounded dyadic comparisons retain the old label, current input, tree node and bit position, not the entire random-bit prefix. This gives O(K log(N/delta)) labels and controlled uniform output error. Every input is processed to a ready boundary in a self-paced interface. There is no free microstep clock or free retained input. Irrational rows are not sampled exactly; finite tables are nonuniform program data. For fixed positive tolerance the two classes retain leading label-bit coefficients 1/3 and (d−1)/2, with O(log log N) uncertainty. This is not a uniform-space theorem.

## Actual error, independent pipeline gates and preservation

The spectral-gap proof gives a lower bound on the true minimum terminal row error for each peak profile. It does not use a sum of local deficiencies as though errors could not cancel. The earlier accumulated-local-certificate result is retained with its proper one-sided interpretation. Weighted packet interval choices depend on the proposed public profile, never on its private random trajectory. An exact-angle arithmetic oracle or interval-sign representation would be required to compute general cyclic weights; no efficient algorithm for arbitrary exact real angles is asserted.

The current frozen Round-Seventeen ledger and the relevant v32–v35 source chain were consulted. The finite-alphabet theorems do not discharge unrelated branchwise Fourier/LLT, stopped-LDP, nonlinear-semigroup, operator-domain or optional-projection gates. The new qubit probability consequence and finite-alphabet width laws are actual proof consequences here, not fabricated A2/B4/C2 dependencies. The general adaptive collision problem, noisy-tag composition and all-irrational classification remain distinct research objectives.

The full v35 article remains byte-identical as `supporting-results.pdf`. Its cumulative mathematical and development volumes are appended unchanged after the new article and a divider. The small referee package excludes those large archives. All earlier repository paths remain unchanged. No proof is replaced by a test receipt, and no archival page count is used as significance evidence.

## Disposition of the specific points

The full-word lemma, sigma-field condition and invariant-direction case address points 1–3. Wordwise test-law selection, endpoint versus initialization counts and available versus positive-mass labels address 4–7. Horizon-dependent common rows and the floor-removal meaning of strict finite inequalities address 8–9. The nonuniform label-bit and finite-coin definitions address 10 and the implementation concerns. The quantum/world-model model comparison addresses 11–12. Borel table and triangulation conventions address 13–16. Constants are fixed-class rather than uniform in d, addressing 17. Public-profile selection, actual-error semantics and computational input qualifications address 18–21. Probabilistic ordered-program terminology and the distinction between fresh row coins and a publicly shared seed address 22–24. The inherited angular appendix is not in the new novelty claim, addressing 25. The individual rational-entry angle is not classified, addressing 26. Raw-suffix storage is explicitly bounded by `(d+1)|A|^l` in the selected-cut proof, addressing 27. Internal pipeline labels stay out of the mathematical conclusion, and no test/revision count establishes significance, addressing 28–29. Independent expert priority assessment requested in 30 has not been obtained and is not claimed.

The new article contains complete proofs of the word-level correction, finite spectral-gap width and occupation estimates, rational sparse upper construction, explicit five-gate application, noncommuting monomial matched law and finite-coin compiler. It invokes the stated external spectral-gap theorem. Finite regressions and compilation support reproducibility; independent correctness and priority remain matters for the next review.
