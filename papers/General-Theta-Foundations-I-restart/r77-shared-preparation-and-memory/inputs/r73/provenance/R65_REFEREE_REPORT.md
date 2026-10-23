# External Referee Report — *General Theta Foundations I: Acquired Geometry and Causal Resource Transfer*

**Submission:** *General Theta Foundations I: Acquired Geometry and Causal Resource Transfer*  
**Author:** Qian Qi  
**Repository:** `TrillionniumFoundation/theta-theory`  
**Reviewed referee-ready branch:** `referee-ready/general-theta-restart-r65-boundary-memory-2026-10-16`  
**Reviewed exact branch head:** `ee79ca9114f8009d62c056d07381b766645e3fc4`  
**Reviewed branch root tree:** `aa507bdd4bc00a8491f4cf9123e01bef6dfaf768`  
**Ordinary mathematical-source commit:** `0469eb4f852eeea953cb3725d4b34dfdd2bf9d36`  
**Ordinary source root tree:** `a3a633e156cdbfddc8aafa4a03c8245689e56a9e`  
**Complete current paper tree:** `3a0ea744d1e4721f2c47b5e038023becd4da2ce0`  
**Native main PDF:** 34 pages, SHA-256 `a331d07268644a283f8d130eeb6fd21cbdc5288a9d519a607eeeb7a1fad817d4`  
**Current technical supplement:** 67 pages, SHA-256 `2d37747d61aacfb46fcb0f25b5332eddc1ecae7a8615e13d44ad0c64b48f756d`  
**Retained complete R58 companion:** 37 pages, SHA-256 `32e81aa0fc581b4690398c4e57a62114c3c6850a1c8f757fe3f6a8216f067194`  
**Controlling predecessor report:** R64 review commit `0a66ca2ede7835ede2a62fe2363ba5dd3ccd2ed8`, report blob `370ad771cf2e2482beefac866445bd384a161911`  
**Review branch:** `review/general-theta-restart-r65-boundary-memory-external-top4-referee-r65-2026-10-16`  
**Date:** 16 October 2026

This is an author-requested external mathematical assessment deposited in the repository. It is not a commissioned editorial decision of a named journal, a formal proof-assistant certificate, an exhaustive priority certificate, or a claim of acceptance by any journal.

---

## Recommendation

**Reject at the level of the Annals of Mathematics, Inventiones Mathematicae, the Journal of the American Mathematical Society, or Acta Mathematica in the manuscript's present form.**

This is **not a technical-correctness rejection**.

Revision R65 is a genuine and substantial advance over R64. It answers the most important structural question left open in the preceding report: full-history attainment at the least feasible expected-cost boundary does not imply attainment by any finite-state observer, and R65 now gives a necessary-and-sufficient exact-memory criterion on a nontrivial prepared-channel class. The criterion is operationally typed, its least memory is exact, stochastic transitions do not evade it under the stated uniqueness hypothesis, and both positive and negative finite-dimensional quantum realizations are supplied.

The new central chain is coherent:

1. a least-budget identity forces commitment at the first productive herald;
2. compact minimax produces an attained least-favorable measure;
3. nonnegative wordwise decision slack forces the unique Bayes decision at every positive-probability word;
4. exact finite stochastic memory is therefore equivalent to finite residual equivalence of the resulting optimal decision function;
5. the residual index is exactly the least number of live labels;
6. an algebraic rotating qubit has infinite residual index and hence an attained full-history optimum that no finite classical memory can attain;
7. finite memories nevertheless approximate the boundary optimum exponentially at the same expected-cost budget;
8. contraction plus a strict limiting decision gap gives an independent positive realization mechanism;
9. the exact one- versus two-live-label optimum of the noisy qubit is solved globally; and
10. unary rational channels admit a direct precision-synthesis upper bound with separate label, program and working-storage accounts.

In the load-bearing new arguments I checked, I did not find an elementary gap invalidating:

- the first-herald cost identity;
- the reduction of the least-budget problem to a model-independent word distribution and wordwise decision rule;
- compact primal and dual attainment;
- the nonnegative slack identity;
- determinization of an exact stochastic observer under unique least-favorable decisions;
- the finite-index residual characterization and exact live-label count;
- the single-model tied-action criterion;
- the explicit warning that robust ties can require randomization;
- compact attainment at every prescribed finite-memory bound;
- the strict fixed-memory gap when the residual index is infinite;
- the finite distinguishing-depth lower certificate;
- the irrational-rotation qubit obstruction;
- the compact uncertain-polarization extension;
- the upgrade from ultimate to pure periodicity on finite-dimensional unitary orbits;
- the contraction-plus-strict-gap sufficient condition;
- the depolarizing counterexample to contraction alone;
- the exact global two-live-label noisy-qubit formula;
- the one-label and two-label numerical specializations;
- the unary rational-channel prefix construction and its stated bit-complexity upper; or
- the inherited R64 boundary-attainment, complete performed-law, sparse-witness, Bellman, multi-resource, timing and actual-history-transfer results at the level previously reviewed.

The negative top-four judgment concerns the **intrinsic reach and external mathematical consequence** of the new theorem. After the least-budget rigidity step, the exact-memory classification becomes a residual automaton theorem for one optimal decision function on a finite alphabet. The physical derivation, robust minimax slack and quantum realization make this combination nontrivial and worthwhile; nevertheless, the current theorem still relies on a specially structured heralded interface with model-independent word probabilities, one globally legal command, a fixed finite decoder dictionary and bounded terminal loss. It is not yet a general invariant for boundary finite-memory attainment in prepared causal experiments.

The rotating-qubit application is elegant and fully physical, but it is designed to realize an irrational unary decision sequence. It does not yet settle a recognized difficult natural problem in quantum statistical decision theory, POMDP control, causal coding, sequential sensing or stochastic shortest-path control. The robust tied case is not classified, the exact intermediate-memory frontier is solved only for one and two live labels in the qubit family, and the computational result is an upper bound for one known unary rational channel rather than a general synthesis theorem.

For a strong specialist journal in stochastic control, sequential decision theory, automata and formal methods, causal coding, mathematical statistics, or mathematical quantum information, my assessment is **favorable after a focused major revision**.

---

## 1. Review object, provenance and pipeline inspected

A fresh complete enumeration of `referee-ready/general-theta-restart-*` immediately before this report identified

```text
referee-ready/general-theta-restart-r65-boundary-memory-2026-10-16
```

as the latest completed `General Theta Foundations I` revision. The continuation page was empty. Existing external review branches ended at R64; no R65 external report was present.

The exact object reviewed is the terminal publication head

```text
ee79ca9114f8009d62c056d07381b766645e3fc4.
```

Its sole parent is the mathematical source commit

```text
0469eb4f852eeea953cb3725d4b34dfdd2bf9d36.
```

The terminal child adds the publication directory and the immutable R64 report object; it does not alter the verified R65 paper subtree.

I reviewed the current theorem article and the current supplement as one paired mathematical submission. The inspection included:

- `main.tex` and `supplement.tex`;
- the complete new `sections/22-boundary-memory.tex`;
- `sections/01-current-overview.tex`;
- the inherited load-bearing `sections/17-primitive-risk.tex`;
- the inherited load-bearing `sections/20-primal-dual.tex`;
- the retained timing theorem in `sections/21-timing-memory.tex`;
- the complete actual-history theorem and proof in `sections/03-main-theorem.tex` and `sections/04-proof.tex`;
- the experiment and observer semantics in `sections/02-experiments.tex`;
- all source references used by the new boundary-memory section;
- `RESPONSE_TO_REFEREE.md`;
- `THEOREM_DEPENDENCIES.json`;
- `THEOREM_INDEX.json`;
- `PROOF_AUDIT.md`;
- `PRESERVATION_MAP.md`;
- `EDITORIAL_LAYOUT.json`;
- `LITERATURE_AND_PRIORITY.md`;
- the current and retained source manifests;
- the complete controlling R64 referee report;
- the local source-bound build receipt;
- the current GitHub Actions status for the exact R65 head; and
- a targeted comparison with absorbing-MDP occupation theory, deterministic/probabilistic/quantum automata, finite-memory POMDP theory and classical minimax.

The current main article is 34 pages. The current supplement is 67 pages. The retained complete R58 companion is 37 pages. The complete R64 source is separately preserved byte-for-byte under `retained/r64-native/`; it is not a hidden substitute for a missing current proof.

I did not independently re-prove every inherited theorem in the full nested historical archive. The R64 results accepted in the preceding review were checked where they remain load-bearing, and the entire new R65 theorem chain was audited directly. Git identity and successful compilation are not fresh mathematical certification of every historical assertion.

---

## 2. Executive mathematical assessment

R64 established the following boundary fact:

```text
the unrestricted full-history constrained optimum is attained
at every feasible finite expected-cost budget,
including the least feasible budget.
```

It correctly did **not** infer that the optimum belongs to a finite-memory class.

R65 now separates three logically different statements:

```text
full-history boundary attainment;

finite-memory density at the same boundary budget;

exact finite-memory attainment.
```

For the prepared heralded-channel class, the first and second always hold under the displayed hypotheses, while the third is governed by a task-specific residual quotient.

This distinction is mathematically important. It rules out two tempting but false implications:

```text
compact full-history attainment
    does not imply finite-state attainment;

contractive physical dynamics
    does not imply eventual constancy of the optimal decision.
```

The new theorem is strongest when read as an exact *boundary implementation theorem*. The least-cost identity removes stopping-time freedom. A robust minimax problem then determines an optimal decision function on all failure words. The residuals of that function, not the full physical state or full predictive quotient, determine the exact implementation memory.

The theorem also supplies a genuine negative phenomenon:

```text
finite-dimensional physical system
+ algebraic primitive channel
+ finite decision dictionary
+ attained bounded-risk optimum
+ exponentially good finite-state approximation

does not imply exact attainment by any finite classical memory.
```

That conclusion is not a numerical artifact. It excludes arbitrary real transition probabilities and randomized terminal decisions.

---

## 3. Response to the R64 report

R65 is not a cosmetic revision. It answers several principal requests in the R64 report.

| R64 request or concern | R65 assessment |
|---|---|
| Reorganize the cumulative 85-page article | **Substantially resolved.** The current theorem article is 34 pages; the technical inheritance is moved to a paired supplement with an explicit authority map. |
| Compare sparse witnesses with absorbing-MDP geometry | **Resolved at theorem level.** The introduction distinguishes primal occupation-policy mixtures from dual model/preparation witnesses and from implementation labels. |
| Make performed-law compactness a conceptual headline | **Resolved.** The reserve, bounded terminal tail, fixed dictionary and uniform-TV conclusion now appear at the beginning. |
| Give a less engineered substantive application | **Improved materially.** The protected rotating-qubit prediction problem has a primitive instrument, exact boundary cost, exact-memory obstruction, uncertain-preparation extension and exact two-label frontier. |
| Clarify finite-memory attainment at the boundary | **Resolved for prepared heralded channels.** R65 gives a necessary-and-sufficient criterion, positive realizations, negative realizations and density at the same boundary budget. |
| Keep fixed dictionary separate from optimized hard width | **Preserved.** Every new theorem fixes `C`; the hard-width counterexample remains controlling. |
| Do not relabel the timing pumping bound as an exact intermediate curve | **Preserved.** The exact two-label result concerns a different quantum prediction problem. |
| Give honest computational content | **Improved.** A unary rational-channel precision-synthesis theorem is proved; no general efficient robust solver is claimed. |
| Add actual R65 hosted verification | **Not yet complete at this review cutoff.** A head-SHA workflow exists but remains queued with no conclusion. |
| Reduce and type the editorial packet | **Improved but still substantial.** Main, supplement, retained companion, source evidence and historical preservation are now separated. |

The most important response is the resolution of the old boundary-memory gap. R65 does not obtain it by taking the interior completion theorem to zero slack. It uses a different exact rigidity mechanism, as it must.

---

## 4. Audit of the least-budget rigidity identity

### 4.1 Physical interface

At each call:

- a productive herald appears with fixed probability `p`;
- each failure letter `y` appears with probability `q pi_y`;
- a failure applies its declared channel to the protected state;
- a rejected herald leaves the protected state unchanged;
- the controller cannot inspect that state;
- commitment is allowed only on a herald; and
- each call has unit cost.

The word probabilities are independent of the model and controller coins. This hypothesis is strong, but it is explicit and is used exactly where required.

### 4.2 Cost identity

Let `J` be the number of rejected heralds and `tau` the accepted-herald call index. The event that call `i` occurs is predictable and the conditional herald probability is `p`, hence

```text
E sum_{i<=tau} 1_{s_i=s} = p E tau.
```

Exactly one herald is accepted. Every other observed herald is rejected. Therefore

```text
p E tau = 1 + E J.
```

The proof uses monotone summation of nonnegative indicators and does not need an optional-stopping theorem.

It follows that:

```text
N_min = 1/p,
```

and equality is possible precisely when `J=0` almost surely. Thus every boundary-feasible policy commits at the first herald. The remaining history is exactly the preceding failure word.

I found no gap in this reduction.

### 4.3 Why this is load-bearing

The identity does more than simplify notation. It removes every boundary policy that trades extra cost for a better decision after a herald. At the least budget, there is no stopping optimization left. The controller implements a word-to-decision stochastic kernel.

This rigidity is the physical reason automata theory becomes relevant. Without it, residual equivalence of the terminal decision rule would not classify the full boundary policy.

---

## 5. Audit of compact minimax and decision slack

Let

```text
B = product_{w in Y*} Delta(C).
```

This is a compact convex metrizable product. The risk series has a uniform geometric tail bounded by `L q^T`; therefore the payoff is jointly continuous in the plan and model, and bilinear in the plan and a probability measure on the compact model space.

Sion's compact minimax theorem applies and gives

```text
min_b sup_theta R_theta(b)
  = max_mu sum_w lambda(w) min_r ell_mu(w,r).
```

Both the primal plan and a least-favorable measure are attained.

For an attaining measure `mu_*`, any robust optimum `b` satisfies:

```text
average risk under mu_* <= robust value
                       = minimum average risk under mu_*.
```

Hence equality holds. Subtracting the wordwise Bayes minima gives the nonnegative slack decomposition

```text
sum_w lambda(w) sum_r b_w(r)
  [ell_mu*(w,r)-a_mu*(w)] = 0.
```

Every word has strictly positive mass. If the minimizing action is unique at every word, every nonnegative summand must vanish and the robust optimum is the unique deterministic rule

```text
a : Y* -> C.
```

This is the key quantifier. The least-favorable measure is not a Bayesian prior supplied to the observer. It is an offline dual witness proving that every robust optimum must implement the same task decision.

The argument is correct under the declared compactness and continuity assumptions.

---

## 6. Audit of the residual decision quotient

R65 defines

```text
w equivalent_a v
    iff a(wz)=a(vz) for every continuation z.
```

This is the right residual relation of the output function `a`.

### 6.1 Lower bound on exact memory

If a deterministic machine sends `w` and `v` to the same label, every common continuation follows the same future transition sequence and produces the same output. Thus the two words must be residual equivalent.

Every exact deterministic machine therefore has at least as many reached labels as the residual index.

### 6.2 Stochastic determinization

The nontrivial part is excluding an advantage from stochastic transitions.

For an exact stochastic observer:

- every state reached with positive probability after `w` must decode the unique action `a(w)` with probability one;
- choose one positive-probability successor for each state and failure letter;
- the resulting deterministic path after any word had positive probability in the stochastic machine; and
- its reached state therefore decodes the required action.

This produces a deterministic exact observer with no more labels. The proof does not rely on a false general statement that probabilistic or quantum cutpoint automata recognize only regular languages.

### 6.3 Upper construction and exact count

Residual classes form a right congruence. The transition

```text
[w] --y--> [wy]
```

and decoder `a(w)` therefore give an exact deterministic observer whenever the index is finite.

The least number of live labels is exactly the residual index.

This is mathematically correct. Its scope should remain explicit:

- it is a quotient of one optimal decision function;
- it depends on the fixed dictionary and least-favorable witness;
- it need not preserve other future tests;
- it is not a common unknown-model predictive quotient; and
- it classifies exact boundary implementation only after the herald rigidity reduction.

---

## 7. Ties and randomization

The manuscript correctly treats ties as a separate issue.

### 7.1 Single model

For one prepared model, every wordwise minimizing choice is globally optimal. An exact finite stochastic observer exists precisely when there is a finite-index right congruence whose every class has a nonempty common intersection of optimal-action sets.

This condition is necessary because a reached stochastic state must decode only actions optimal for every word reaching it. It is sufficient by choosing one action in each class intersection.

The minimum class count is the minimum exact live-label count.

### 7.2 Robust models

For a robust family, zero slack under a least-favorable measure is still necessary. It is not sufficient to select an arbitrary tied Bayes action deterministically.

The two-model example with loss vectors `(0,1)` and `(1,0)` is decisive:

- the fair randomized decision has robust value `1/2`;
- both pure decisions are Bayes-tied under the equal least-favorable measure; but
- either deterministic choice has robust loss one.

R65 therefore does not overstate its deterministic residual theorem in the tied robust case.

The absence of a full robust-tie classification is now one of the principal remaining structural gaps.

---

## 8. Fixed-memory attainment and quantitative separation

For fixed `M`, the transition matrices and decoder rows lie in a finite product of compact simplexes. Geometric word tails make the robust risk continuous. Therefore the best `M`-label risk is attained.

If the unique optimal decision function has infinite residual index, equality with the full-history value would produce an exact finite machine, which is impossible. Hence every finite `M` has a strict positive gap.

The prefix construction stores all words shorter than `T` and merges the remaining tail. It remains at cost `1/p` and changes loss only on total mass `q^T`, giving exponentially accurate same-boundary approximants.

The finite distinguishing-depth certificate is also valid:

- there are finitely many deterministic `M`-state output machines;
- each fails at a finite word;
- the maximum first failure depth `H_M` is finite;
- a stochastic machine has a selected positive path of probability at least `M^{-n}`;
- one selected decoder value has probability at least `1/|C|`; and
- the least-favorable slack at the distinguishing word is positive.

This proves the displayed positive lower bound.

The certificate is qualitative and finite, not a sharp asymptotic law. In particular:

- `H_M` is not given by a primitive-data algorithm in the general theorem;
- `gamma_H` may be very small;
- the resulting bound can be extremely weak; and
- no matching lower exponent in `M` is claimed.

Those limitations should remain prominent.

---

## 9. Audit of the rotating-qubit obstruction

The failure channel is conjugation by

```text
U = (1/sqrt(5)) [[2,-1],[1,2]].
```

The corresponding Bloch rotation has

```text
cos(vartheta)=3/5,
sin(vartheta)=4/5.
```

After `n` failures, the Pauli-`Z` audit mean is

```text
c_n = cos(n vartheta).
```

The squared loss of decision `r in {-1,1}` is `2-2 r c_n`, so the unique wordwise optimum is `sign(c_n)`.

### 9.1 Irrationality and nonperiodicity

If `exp(i vartheta)` were a root of unity, then `2 cos(vartheta)=6/5` would be a rational algebraic integer and hence an integer, a contradiction.

Therefore `vartheta/pi` is irrational. No `c_n` vanishes, and every residue subsequence modulo a positive integer is dense on the circle. Each such subsequence visits both cosine signs, so the sign sequence is not ultimately periodic.

A finite deterministic unary output machine has an initial path followed by a cycle; its output is ultimately periodic. The residual index is therefore infinite.

The exact-memory theorem then excludes every finite stochastic observer, including observers with arbitrary real transition probabilities and randomized terminal readouts.

### 9.2 Values and approximation

The full-history value

```text
V_p = 2 - 2p sum_{n>=0} q^n |c_n|
```

is correct.

The exact one-label value follows from the real part of the cosine resolvent and is

```text
V_{p,1}
 = 2 - 2p(1-3q/5)/(1-6q/5+q^2).
```

At `p=1/2` this is `12/13`.

An `M`-label prefix chain is exact through `n=M-1` and has per-word excess at most four thereafter. The terminal tail mass is `q^M`, proving

```text
0 < V_{p,M}-V_p <= 4q^M.
```

The compact uncertain-polarization family is also correct: for positive polarization the optimal signs are unchanged, risk is worst at the smallest polarization, and that endpoint supplies the least-favorable preparation.

This is a genuine finite-dimensional quantum example, not an externally encoded nonregular string.

---

## 10. Positive exact-memory mechanisms

### 10.1 Finite-dimensional unitary orbits

For a unary unitary orbit with a unique decision at each time, the residual theorem first gives finite memory exactly when the decision sequence is ultimately periodic.

R65 correctly upgrades this to periodicity from time zero. If the eventual period is `r`, compactness of the finite-dimensional unitary torus gives a sequence with

```text
U^(r k_j) -> I.
```

For any fixed early time, the two late states separated by `r` converge to the corresponding early states. Uniqueness among finitely many decisions gives a local strict gap, so eventual periodicity forces equality of the two early decisions.

The least live-label count is the least positive period.

The uniqueness hypothesis is essential. With ties, orbit recurrence need not select a stable output.

### 10.2 Contraction plus a strict limiting decision gap

If all word states converge uniformly to one limiting state and one dictionary value has a strict limiting advantage, trace duality makes that action uniquely optimal beyond a finite depth.

A prefix tree plus one common tail label then gives an exact boundary optimum.

This is an honest positive theorem: the limiting state is an offline certificate, not a runtime oracle.

### 10.3 Why contraction alone is insufficient

For the depolarizing rotating qubit, every nonzero contraction factor preserves the sign of the irrational cosine sequence. The state approaches the maximally mixed state, but the two limiting decisions are tied there. The exact decision continues to alternate at arbitrarily late times, with diminishing advantage.

Thus every finite memory remains strictly suboptimal for every `alpha>0`, although the gap decays geometrically. At `alpha=0`, all positive-length histories are exactly tied and one label is optimal.

This is a useful and conceptually clean counterexample.

---

## 11. Audit of the exact two-live-label frontier

The two-state failure matrix is parameterized by

```text
Q = [[1-a,a],[b,1-b]].
```

Let `lambda=1-a-b` and let `z=a/(a+b)` when `a+b>0`. The expected signed reward vector admits the exact decomposition

```text
v_0 = (1-z)A + zB,
v_1 = z(A-B),

A = p f_c(x),
B = p f_c(x lambda),
x = q alpha.
```

Optimizing randomized decoders is exactly the same as choosing the signs of the two vector entries. Since `v_0>0`, the objective is:

```text
A,                         if B<=A;
A + 2z(B-A),               if B>A.
```

For fixed `lambda`, the largest feasible `z` is:

```text
1,                         lambda>=0;
1/(1-lambda),              lambda<0.
```

The remaining optimization is one-dimensional. The derivative calculations and endpoint clipping in the manuscript cover:

- `x=0`;
- all `0<=c<=1`, including `c=1`;
- all `-1<=c<0`, including degenerate transition endpoints;
- all `0<=alpha<=1`; and
- every `0<p<1`.

I independently checked the piecewise formula against direct numerical optimization over the full square of stochastic transition parameters and randomized decoder values on a broad collection of parameter points. The formulas agree to the expected grid precision.

For the algebraic example `c=3/5`, `p=1/2`, `alpha=1`, the exact values are:

```text
one live label: 12/13;
two live labels: 43/52;
Q = [[2/3,1/3],[0,1]].
```

The second label improves the one-label optimum precisely when `q alpha>1/3`.

This is a substantive exact finite-memory calculation. It should not be described as the intermediate-memory solution of the separate deterministic-release timing problem, and the manuscript correctly avoids that inference.

---

## 12. Audit of the unary rational-channel synthesis theorem

For one known unary rational channel and fixed rational loss dictionary, the algorithm:

1. computes the exact rational states through depth `T-1`;
2. chooses a minimizing dictionary value at each depth;
3. stores a chain of `T` live labels;
4. repeats the final label thereafter; and
5. commits at the first herald.

The policy is exact on all terminal words of length below `T`. The remaining terminal mass is `q^T`, so choosing

```text
L q^T <= epsilon
```

gives risk at most `V+epsilon` at the exact boundary cost `1/p`.

The arithmetic count

```text
O(T(d^4 + m d^2))
```

for dense real-Hermitian superoperator application and loss evaluation is reasonable. With a common denominator, physical coordinate bounds keep numerator lengths linear in `TB`, up to logarithmic dimension factors.

The theorem correctly separates:

- persistent live-label count;
- transition/readout table length;
- rational working storage;
- primitive and dictionary input encoding;
- herald-rate dependence; and
- output-program storage.

The polynomial precision claim requires the herald rate bounded away from zero. It is not polynomial uniformly as `p` tends to zero, and it is not a matching complexity lower bound.

The result is a useful constructive upper for a narrow input class. It does not solve robust continuum-model synthesis, residual-index decidability for general channels, or exact-memory minimization.

---

## 13. Inherited R64 optimality theory

The R64 report found no fatal gap in:

- boundary attainment;
- right-continuity of the constrained frontier;
- performed-law compactness in uniform total variation;
- complete bounded-score separation;
- the fixed-dictionary resource-price dual;
- sparse physical cost/risk witnesses;
- the common Bellman recursion and rowwise slack;
- multi-resource completion;
- the hard-width duality-gap example; or
- the delayed-release memory threshold.

R65 preserves these proofs and reorganizes them. I checked the preservation map and the current compilation graph. The accepted mathematical bodies remain current inputs, with cross-document references rebuilt. The new boundary-memory theorem is not used to weaken their assumptions or to retroactively claim finite-memory attainment in the full R64 interface.

The editorial restructuring is a real improvement. The theorem article now has a recognizable center. The supplement, however, remains 67 pages and contains many independent lines. A journal submission must make clear which results are necessary for the theorem article and which are preserved programme infrastructure.

---

## 14. Literature and priority positioning

### 14.1 Absorbing MDPs

The new comparison with Piunovskiy--Zhang and Dufour--Prieto-Rumeau is appropriate.

Their finite extreme occupation measures and finite mixtures of deterministic stationary policies are primal objects in an observed-state MDP. R64's `k_T+1` atoms are dual model/preparation witnesses. Neither count is an implementation-memory bound for a controller that does not observe the underlying state.

R65 states this distinction correctly.

### 14.2 Classical residual equivalence

The exact finite-index theorem belongs directly in the Rabin--Scott / Moore--Myhill--Nerode tradition of residual equivalence and minimal finite-state output machines.

R65 acknowledges residual-function automata, but the native comparison should be more direct. The new part is not that finite residual index characterizes finite deterministic realization. The new part is the physical and decision-theoretic derivation of one uniquely forced robust output function at the least cost, plus the proof that exact stochastic realization collapses to deterministic realization because every positive word and every wrong action has positive decision slack.

This distinction should be stated in the theorem introduction, not left mainly to the response and priority ledger.

### 14.3 Probabilistic and quantum automata

Probabilistic automata with isolated cutpoints can often be reduced to regular behavior, while nonisolated cutpoints can generate nonregular stochastic languages. Unary quantum finite automata likewise use rotation and periodicity mechanisms.

R65's determinization is not a general cutpoint theorem. It relies on exact zero slack and unique minimizing decisions at every word. The rotating-qubit construction uses an established irrational-rotation mechanism but gives it a new paid prediction interpretation and an exact bounded-risk statement.

The paper should compare these quantifiers explicitly.

### 14.4 Finite-memory POMDP theory

Finite-memory controller problems for POMDPs range from positive approximation theorems under filter stability to hard or undecidable exact quantitative questions.

R65's result avoids those general difficulties because:

- the failure word distribution is state and model independent;
- there is one globally legal command;
- the least budget forces one stopping rule;
- the physical state is never used to choose an action; and
- only the terminal decision must be implemented.

This is a virtue for exact analysis, but it is also a scope limitation. The paper should not suggest that the residual quotient is a general finite-memory POMDP criterion.

---

## 15. Pipeline and reproducibility assessment

The source-bound local receipt reports:

- exact source commit `0469eb4f852eeea953cb3725d4b34dfdd2bf9d36`;
- exact source root tree `a3a633e156cdbfddc8aafa4a03c8245689e56a9e`;
- exact paper tree `3a0ea744d1e4721f2c47b5e038023becd4da2ce0`;
- 1,748 verified source files;
- 111 verified theorem entries;
- 10,190 finite diagnostics;
- 7,956 exact checks;
- 2,234 floating probes;
- identity of ordinary and optimized Python output;
- three LaTeX passes for each current document; and
- byte-identical repeated builds of all three PDFs.

These are useful source-integrity, finite-algebra and reproducibility controls.

At the cutoff for this report, GitHub Actions run

```text
38861581555
```

for the exact head SHA

```text
ee79ca9114f8009d62c056d07381b766645e3fc4
```

exists but remains **queued**, with no conclusion. The repository correctly says that the local source-bound receipt and older runs do not constitute a passed R65 hosted verification.

This is not a mathematical proof defect. The final handoff should be updated when the actual head-SHA workflow reaches a terminal state. Until then, language such as “hosted verification passed” would be inaccurate.

Finite diagnostics, compilation, source hashes and repeated PDF identity do not prove the continuum theorems, novelty, priority or journal significance.

---

## 16. Main reasons the top-four recommendation remains negative

### 16.1 The exact criterion is derived on a special heralded interface

The theorem assumes:

- one globally legal command;
- a model-independent productive probability;
- a finite failure alphabet with model-independent positive probabilities;
- state-independent word mass;
- a fixed finite decision dictionary;
- bounded terminal loss;
- and no observation of the protected state.

These assumptions create a clean exact boundary problem. They also remove most of the feedback and control structure that makes general finite-memory causal decision problems difficult.

### 16.2 After rigidity, the classification is classical in form

Once first-herald commitment is forced and the unique robust decision function is derived, the least-memory statement is the minimal residual automaton theorem for that function.

The paper's contribution is the derivation and robust stochastic determinization, not the residual theorem itself. The current title and framing should reflect that narrower center.

### 16.3 The tied robust case remains open

R65 correctly shows that robust ties can require randomization. It does not give a necessary-and-sufficient finite stochastic-memory criterion in the tied robust case.

That is precisely the setting in which probabilistic automata can exhibit behavior not captured by deterministic residual classes. A complete robust-tie theorem would materially broaden the result.

### 16.4 The natural application is still constructed around the mechanism

The rotating qubit is physically legitimate, algebraic and noncommutative. It is also chosen so that the optimal sign sequence is generated by an irrational rotation.

The example verifies the theorem sharply, but it does not yet solve an independently recognized quantum prediction, discrimination or feedback-control problem. The uncertain-polarization extension improves robustness but does not change that assessment.

### 16.5 The intermediate-memory theory is incomplete

The paper gives:

- the unrestricted full-history optimum;
- the exact one-label optimum;
- the exact two-label optimum;
- strict nonattainment for every finite label bound; and
- an exponential prefix upper.

It does not determine the optimal `M`-label risk for general `M`, its sharp asymptotics, or a matching lower rate. The finite distinguishing-depth certificate is not such a rate.

### 16.6 The computational theorem is one-sided and narrow

The rational-channel algorithm is a constructive approximation upper. It does not decide finite residual index, find a minimal exact observer, prove hardness, or give matching program/precision/workspace lower bounds.

### 16.7 The complete programme remains much broader than the theorem article

The current main article is more concentrated, but the title still suggests a general foundation for acquired geometry and causal resource transfer. R65 supplies one exact boundary-memory invariant for one prepared-channel class, not a general classification.

---

## 17. Major revision requests

### 17.1 Make the exact boundary-memory theorem the sole mathematical headline

The abstract and introduction should distinguish three layers in one compact display:

```text
general performed-law boundary attainment;

heralded-channel exact-memory criterion;

quantum obstruction and positive finite-memory mechanisms.
```

The geometric and timing routes should remain clearly complementary rather than coequal headlines.

### 17.2 Add a direct Moore/Myhill--Nerode comparison

State explicitly:

- classical residual equivalence already characterizes minimal deterministic output machines;
- R65 derives the output function from a physical minimax problem;
- exact zero slack and uniqueness eliminate any stochastic advantage;
- the residual quotient is task and dictionary specific; and
- it is not the full predictive quotient.

### 17.3 Develop the robust tied case

A major strengthening would give a necessary-and-sufficient criterion for exact finite stochastic memory when a least-favorable measure has tied wordwise actions.

At minimum, formulate the problem as a finite-state realization of a family of admissible decoder simplexes and identify what replaces the deterministic residual congruence.

### 17.4 Broaden the herald model

The next mathematically meaningful extension is not another example. It is to allow at least one of:

- model-dependent failure probabilities;
- state-dependent herald probabilities;
- several legal commands;
- command-dependent channel words;
- or a nontrivial stopping choice at the boundary.

The theorem should identify which part of the residual criterion survives and what new sufficient statistic replaces the raw failure word.

### 17.5 Obtain a sharp `M`-memory law

For the noisy qubit, prove either:

- an exact formula for general `M`;
- a matching asymptotic for `V_{p,alpha,M}-V_{p,alpha}`;
- or a nontrivial lower exponent matching the prefix upper.

The present finite-depth bound proves positivity but does not describe the frontier.

### 17.6 Connect the quantum example to an external problem

A stronger application would arise from a standard quantum task whose finite classical-memory optimum was previously unknown, such as:

- repeated heralded state prediction under a prescribed instrument;
- a reference-frame tracking task;
- a quantum finite-state feedback protocol; or
- a constrained sequential discrimination problem with a natural audit.

The current qubit should remain as the exact core example, but it should not carry the whole external-impact claim.

### 17.7 Strengthen computational content

For unary rational channels, investigate:

- decidability or complexity of finite residual index;
- minimal exact-memory synthesis when the index is finite;
- hardness of the `M`-label optimum;
- certificate size for strict nonattainment;
- or matching precision/program lower bounds.

### 17.8 Close the hosted verification record

Read back the actual terminal status of run `38861581555` and append the resulting head-SHA receipt. Do not label a queued run as a pass.

### 17.9 Further reduce the editorial dependency surface

The 34-page main article is a major improvement. The 67-page supplement still contains many independent lines. The journal submission should specify a minimal theorem-dependency subset and move purely historical preservation outside the submitted mathematical packet.

### 17.10 Keep memory notions distinct in every abbreviated statement

Every summary should distinguish:

- live labels;
- decoder values;
- event-stopped total labels;
- state-stopped terminal labels;
- program-table bits;
- working storage;
- protected quantum state; and
- full-history mathematical information.

---

## 18. Technical comments

1. Every abbreviated statement of the boundary-memory theorem should retain the fixed dictionary `C`.
2. The model-independent word probabilities are a theorem hypothesis, not merely notation.
3. The first compulsory call is included in `1/p`.
4. A separately executed audit cost must continue to be added to all budgets.
5. The least-favorable measure is an offline witness, not a Bayesian input to the controller.
6. The unique-action assumption is wordwise under one attaining least-favorable measure.
7. Strictly positive word masses are used to pass from zero expected slack to zero slack at every word.
8. The residual relation is a right congruence of the optimal decision function, not of the full channel state.
9. “Least live-label count” should be followed immediately by the event/state total-label conventions.
10. Unreachable stochastic rows may be completed arbitrarily, but they should not be counted in a claimed minimal reached machine.
11. The stochastic determinization proof depends on selecting positive successors; zero-probability edges cannot be used.
12. The robust tied example should remain adjacent to every informal determinization claim.
13. `H_M` exists by finiteness but is not automatically computable from continuum primitive data.
14. The quantitative gap should not be advertised as a sharp memory-risk law.
15. The irrational-rotation proof uses the fact that `6/5` cannot be a rational algebraic integer.
16. The statement that no cosine is zero should retain its root-of-unity implication.
17. The uncertain-polarization result requires `eta>0`; at `eta=0` uniqueness fails.
18. Pure periodicity on a unitary orbit requires uniqueness at every orbit time.
19. The contraction theorem requires one common limiting state and one strict limiting decision gap.
20. The depolarizing example demonstrates that a positive contraction factor alone is insufficient.
21. In the two-state calculation, state and row conventions for `Q` should be stated where the formula first appears.
22. The two-label theorem optimizes decoder expectations in `[-1,1]`, hence includes randomized terminal decisions.
23. The endpoint cases `x=0`, `c=1` and `c=-1` should remain explicit.
24. The threshold `q alpha>1/3` belongs only to the displayed `c=3/5` family.
25. The exact two-label theorem is not the unresolved intermediate phase-type timing frontier.
26. The rational algorithm assumes exact rational primitive entries and fixed dictionary losses.
27. The polynomial precision claim requires a herald-rate lower bound.
28. Dictionary and primitive encoding lengths are additional program inputs.
29. The arithmetic upper uses a dense `d^2`-coordinate superoperator representation; sparse structure may improve it but is not assumed.
30. The output program table is distinct from transient rational working storage.
31. The local build receipt is source-bound but is not a proof of theorem truth.
32. The R65 GitHub Actions run was queued at the review cutoff.
33. Cross-document references require the main and supplement PDFs to be kept together.
34. Preservation of the complete R64 tree is provenance, not re-review.
35. The historical branch-name scan is not a fresh SHA and proof audit of every historical theorem.
36. The complete performed-law theorem continues to compare bounded scores, not unbounded remaining duration.
37. Fixed-dictionary convexity must not be extended to optimized hard width.
38. Sparse `k_T+1` atoms remain dual physical witnesses, not primal finite-memory states.
39. The protected qubit is part of the experiment and is not observer-owned quantum memory.
40. The scope statement should continue to list general boundary finite-memory density and robust tied classification as open.

---

## 19. What would materially change the top-four assessment

Any one of the following would substantially alter the editorial evaluation:

1. an intrinsic exact-memory criterion beyond model-independent herald words;
2. a complete robust-tie stochastic-memory classification;
3. a sharp general-`M` memory-risk frontier for the quantum orbit;
4. a solution of a recognized natural quantum/POMDP/causal-coding problem using the new invariant;
5. a general decidability or complexity theorem for boundary exact memory; or
6. a unified theorem connecting performed-law compactness, boundary residual memory and acquired geometry without separately supplied certificate classes.

Additional examples, more repository evidence or more historical preservation would not by themselves change the mathematical assessment.

---

## Final recommendation

R65 is a serious and technically credible revision. It resolves the preceding report's most important open structural point on a clearly declared class. The least-budget identity, robust zero-slack theorem, residual decision quotient, finite-dimensional quantum nonattainment and exact two-label calculation form a coherent specialist paper.

I nevertheless recommend **rejection at the top-four general-mathematics level in the present form**, because the exact classification remains tied to a specially engineered heralded interface and reduces, after the physical rigidity step, to classical residual automata of one optimal task. The paper has not yet produced the broader intrinsic classification or external consequence suggested by its title.

For a strong specialist journal, I would view a focused revision favorably.
