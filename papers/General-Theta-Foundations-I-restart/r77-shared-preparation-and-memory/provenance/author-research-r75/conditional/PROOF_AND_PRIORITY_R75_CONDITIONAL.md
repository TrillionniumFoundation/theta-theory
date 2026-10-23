# R75 conditional-memory author research: proof and priority ledger

This is author-side mathematical development and challenge, not a new referee report, formal verification, independent human expert endorsement, or editorial decision. It continues the complete R74 source fixed by the parent revision process. No sealed R74 source was edited.

## Files and theorem map

| File | Statement | New scope and dependencies |
|---|---|---|
| `42-stationary-initialization.tex` | `thm:r75-stationary-initializer` | Exact one-label difference between free-mixture and counted-pure initialization for every finite-command response fixed predictively by a full-support averaged unobserved command; one-label exception explicit. Uses response-function convex elimination; no spectral hypothesis or finite-dimensional minimal-response-space assumption. |
| Same | `cor:r75-stationary-process` | Ordinary stationary, non-i.i.d., finite-alphabet edge-emitting HMMs are a special case. Infinity convention explicit. |
| `43-noisy-conditional-memory.tex` | `lem:r75-noisy-physical` | Full physical validity for every damping and commanded angle; uniform report floors, exact depolarization, stationary predictive preparation, fixed-angle one-dependence, rank three for nonreal positive damping and rank two at zero damping. |
| Same | `lem:r75-full-instrument-bounds` | Productive-cylinder spectral obstruction for every arbitrary-real classical model; one physical polygon invariant under every report branch and all eligible commands. Reuses the inherited Perron normalization and classical stochastic eigenvalue regions. |
| Same | `thm:r75-noisy-memory` | Exact first-sector complete-instrument counts and boundary zero-branch Perron rigidity; exact common all-angle count K(alpha) mixed and K(alpha)+1 pure; explicit zero-damping endpoint 2/3; undamped endpoint inherited from R74. |
| `supplement-r75-conditional.tex` | `thm:r75-stopped-approximation` | A single noisy finite model approximates the undamped instrument uniformly for common randomized adaptive angle/stopping/terminal-measurement policies with bounded target expected calls. Error <= epsilon B/8, counted pure memory pi/4 sqrt(B/delta)+O(1). An upper bound only. |
| Same | Arithmetic lift paragraph | R71 arithmetic envelope, exponents and badly-approximable criterion extend to the complete instrument because the same necessary spectral and sufficient polygon statements hold. No new arithmetic theorem claimed. |

The parent may rename the two main-section files to sections 43/44. Labels above remain stable.

## Load-bearing checks and exact hypotheses

### Initialization

The relevant stationarity equality is on **all future response functions**, not merely on report marginals or on an asserted hidden-state stationary row. With terminal measurements present, the separate equality for every `(word, terminal command, terminal outcome)` includes the empty word. In an arbitrary pure-start realization, this gives `f_o = sum_j Tbar[o,j] f_j`.

If `Tbar[o,o]=1`, nonnegativity and full support of the command distribution force every command to keep label `o` closed, so the response really has a one-label realization. Otherwise the normalized weights `beta_j = Tbar[o,j]/(1-Tbar[o,o])` eliminate `o`. All outcome matrices, including transitions back to `o`, are changed by the same exact formula. Induction verifies every future response from every retained label. This step does not need physical density representatives, observable-rank minimality, irreducibility, or equality of hidden distributions.

Conversely the extra counted label executes the **first actual command** in its entrance row `mu T[a,y]`; it does not generate an unrecorded preliminary sample while pretending its memory is free. Terminal readout at length zero is `mu d[b,z]`. The theorem is for edge-emitting models, matching quantum instruments. It does not silently assert the same count for a different state-emitting model convention.

### Productive cylinder lower

The cylinder mode is `alpha exp(i theta)/8`, while every entry of the productive zero-branch core is bounded by a constant times `8^{-n}`. Thus its spectral radius is at most 1/8. Normalize an irreducible block containing the observed complex mode, then radially contract its stochastic normalization with a stationary rank-one matrix. This proves `alpha exp(i theta) in K_M` for arbitrary HMMs without a false global Perron-vector assumption on reducible matrices.

At a first-sector boundary, strict monotonicity excludes smaller sizes at least three, and Hankel rank excludes one/two states. The carrying block must use all M labels. Its spectral radius must equal 1/8, so the classical equality case yields a lazy directed cycle after diagonal similarity. No assertion that the similarity is scalar, or that the other outcome matrices are uniquely determined, is made.

### Simultaneous physical upper

The polygon is made of actual pure qubit states, with one vertex equal to the reset state. It works for branch zero if `alpha exp(i theta)` lies in the polygon. Branch one resets to that fixed vertex. The normalized branch-two output has Euclidean Bloch norm at most `5/11`, strictly below every regular q-gon inradius for q>=3. A single dictionary and common terminal decoder therefore work for every commanded angle satisfying the condition, including arbitrary adaptive command selection. The universal upper uses the whole disk of radius alpha; it is not a separate controller selected after each complete experiment.

The R68 uniform-interior theorem does not already supply this example: branch one always prepares a pure state, and every positive word consisting only of ones still prepares it at any block length. Both the one-step and fixed-block every-posterior interior hypotheses fail. The new positive construction exploits simultaneous branch geometry. Fixed-angle stationarity/one-dependence is not ascribed to arbitrary feedback-controlled visible records; a policy can introduce its own temporal correlations.

The lower attaining the universal upper is witnessed by one nonreal phase: any nonreal angle when K=3, or theta=pi/(K-1) when K>3. At the exact ceiling boundary alpha=cos(pi/K), the K-gon still contains the closed disk. At alpha=0 the angle disappears entirely: the two explicit diagonal states and rational 2x2 matrices give an exact complete-instrument realization, and a 2x2 word Hankel minor is exactly 2^-19. Stationarity then charges the third pure-start label.

### Stopped approximation

The two changed report branches have opposite differences `epsilon(D-Ad_U)/8`. For a positive qubit operator X, `||D(X)-Ad_U(X)||_1 <= tr X`; hence the flagged one-call trace distance is at most `epsilon tr(X)/8`. The constant assumes the stated single qubit and no entangled external quantum register.

In the hybrid telescoping term for call t+1, the prefix is always the undamped target and the suffix always the damped system. Thus the local error is weighted by the **target** continuation probability. The sum is epsilon times the target truncated expected cost divided by eight. Every future common policy step and terminal POVM contracts the Hermitian trace norm. Merging unfinished histories at horizon H and then increasing H proves the infinite stopped-record assertion, including the nontermination atom.

The expected-cost bound is imposed on the target. Total variation does not bound an unbounded stopping-time expectation of the approximation. The approximate process can have nontermination probability up to the error bound. A deterministic horizon removes that possibility. The construction supplies no matching generic approximation lower and no unknown-model learning guarantee. External policy labels, real coefficient encodings and exact sampling costs are separate accounts. B=0 is handled explicitly by a no-call one-label decoder.

## Primary literature inspected in this author pass

### Monras and Winter

Primary full text inspected: Alex Monras and Andreas Winter, *Quantum learning of classical stochastic processes: The Completely-Positive Realization Problem*, arXiv:1412.3634v1, 11 December 2014; journal version J. Math. Phys. 57, 015219 (2016), DOI 10.1063/1.4936935.

- URL: https://arxiv.org/html/1412.3634v1
- Inspected Definition 1 (stationary quasi-realizations), Definition 5 (positive realizations with stationary initial row), Theorem 6 (invariant polyhedral-cone criterion), Lemma 7 and Example 2 (group invariance obstruction), and Appendix A's proof of the order-unit statement.
- These establish the classical positive-realization and stationary-cone framework. The current convex elimination belongs to that framework and is not presented as invention of it. The inspected passages do not state the present controlled exact free-start/pure-start minimum comparison. This limited inspection is not a worldwide novelty clearance.
- The inherited bibliography key `MonrasWinter14` refers to the TQC 2014 conference version, DOI 10.4230/LIPIcs.TQC.2014.99. The expanded full text above is the 2016 journal article; the parent should retain that distinction if citing an exact theorem number from it.

### Fanizza, Lumbreras and Winter

Primary publisher full text inspected: Marco Fanizza, Josep Lumbreras and Andreas Winter, *Quantum Theory in Finite Dimension Cannot Explain Every General Process with Finite Memory*, Communications in Mathematical Physics 405, article 50 (2024), DOI 10.1007/s00220-023-04913-4.

- URL: https://link.springer.com/article/10.1007/s00220-023-04913-4
- Inspected Section 2.3, Theorem 2 and Section 4.2, including the cylinder generating-function argument and normalization by the maximal positive eigenvalue.
- Section 2.3 credits the FRDN noncommensurate-phase obstruction and commensurate minimum dimensions, referring to Fox--Rubin (1968) and Dharmadhikari--Nadkarni (1970). Theorem 2 already gives inverse-square-root noise dependence in a worst-phase classical-memory lower bound for another noisy quantum process. Neither mechanism nor exponent is claimed first here.
- Current additional scope: explicit matching full-instrument upper and lower for the stated exactly-depolarizing uniformly positive qubit family; the same dictionary for all commanded angles; exact initialization accounting; endpoint and bounded-cost stopped-law implementation. Its sector formula is inherited R69 classical stochastic geometry, not new spectral geometry.

### Ohta

Primary author full text inspected: Yoshito Ohta, *On the Realization of Hidden Markov Models and Tensor Decomposition*, arXiv:2008.11487v1, 26 August 2020.

- URL: https://arxiv.org/html/2008.11487v1
- Inspected formulation in Section 2 and the conclusion in Section 5. It treats stationary state-emitting HMMs, reachable/null subspaces, and tensor reductions yielding a minimal quasi-realization. Its conclusion explicitly retains the minimum positive-state issue in a deterministic-observation class.
- The new results are exact constructions and lower bounds for specified models and an initialization relation. They do not identify arbitrary hidden models from data or solve the unrestricted minimum HMM realization problem.

### Heller original access limit

The original Heller (1965) DOI is already correctly retained in R74: 10.1214/aoms/1177700000. A fresh attempt to open the Project Euclid full-text page through the available web tool failed. Accordingly this pass does not claim to have reread its original proof; its positive-realization antecedence is retained and the modern primary exposition above was inspected.

## Diagnostics actually executed

`diagnostics_r75_conditional.py` ran successfully in ordinary mode and under Python `-O`. Its JSON reports are byte-identical. It performs 2,078 checks, all with exact rational arithmetic and no floating probes:

| Group | Checks | What was actually exercised |
|---|---:|---|
| Controlled stationary elimination | 697 | Two-command nonmemoryless fixture; initializer with positive self-return; full-support averaged identity; elimination restores the two-state core; finite command/report words and terminal readouts. |
| Zero-damping two-state endpoint | 373 | Explicit rational branch matrices, rank-one aggregate, physical state intertwining, finite word states, exact Hankel minor. |
| Complete noisy instrument polygon | 966 | Rational four-gon first-sector boundary; simultaneous multiple rational angle commands at stronger damping; all branch state identities, finite command/report words, lazy-cycle zero branch and rank-three minor. |
| Stopped-law perturbation | 42 | Exact pure-qubit one-call constant and capped adaptive stopping with terminal measurement, including randomized command policies. |

Finite checks corroborate these displayed data. Universal quantifiers, continuum angle families, optimality over arbitrary HMMs, infinite-horizon limits and novelty still rest on the written mathematical arguments and require subsequent referee assessment.
