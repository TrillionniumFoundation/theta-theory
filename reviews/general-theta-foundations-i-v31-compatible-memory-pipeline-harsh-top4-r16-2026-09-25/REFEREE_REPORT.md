# Referee Report — General Theta Foundations I, Revision 31

**Manuscript:** *General Theta Foundations I: Compatibility of Positive Memory and Online Simplex Synthesis*  
**Repository:** `TrillionniumFoundation/theta-theory`  
**Reviewed branch:** `revision/general-theta-foundations-i-v31-referee-ready-2026-09-25`  
**Reviewed head:** `90dc2c8f0c75e2cfbb95cc61b247ce4d5e216eb9`  
**Native mathematical source recorded by the manuscript:** `ca4982c728168e9e25bc86fe85e0fd7fae455192`  
**Controlling previous report:** `cd793fde91fca07958c6c5bc3989e9c51a17540b`  
**Previous reviewed manuscript:** `a4abeb1c5e0323e5850e7f2446bf96fb1f7d4d8a`  
**Review branch:** `review/general-theta-foundations-i-v31-compatible-memory-pipeline-harsh-top4-r16-2026-09-25`  
**Date:** 25 September 2026

## Recommendation

**Reject at the Annals / Inventiones / JAMS / Acta level.**

This is now a mathematically coherent specialist paper. It is not a four-journal paper, and the distinction should not be blurred by the repository's unusually large historical apparatus.

Revision 31 answers the strongest objections in the fifteenth report more seriously than any preceding revision. It supplies the missing full-support compatibility obstruction; it determines that example's complete two-cut Pareto frontier; it identifies a canonical rank-two no-obstruction class; it proves a same-alphabet online construction for additive encoders; it correctly separates classical cube absorption from the online consequence; it corrects the random-access-code priority boundary; and it internalizes the stochastic-language conventions that were previously left partly external.

I did not find a short fatal error in the principal new proofs. In the exact finite, clocked, atomic stochastic-row model actually stated, the affine-slice argument, the rank-three obstruction, the additive replacement process, the critical-simplex update, and the checkpoint exactification argument are internally coherent. The negative recommendation is therefore **not** based on an allegation that the displayed theorems are false.

The rejection is based on mathematical scale, originality, and relation to the claimed program.

1. The rank-three obstruction is a well-designed constant-size example, not a structural theory. It gives one one-parameter, two-cut family with a one-state incompatibility gap. It does not yield a general obstruction invariant, an asymptotic family, a complexity theorem, an arbitrary-horizon classification, or the solution of a recognized open problem in positive realization.
2. The canonical affine-slice theorem uses the classical invariant-convex-set mechanism in an especially transparent finite-horizon form. The rank-two corollary is essentially the observation that a compact zero- or one-dimensional polytope is a point or an interval, combined with normalized-shift closure. This is useful, but not remotely of four-journal depth.
3. The additive synthesis theorem is an elementary weighted-replacement construction after coordinatewise subtraction of minima. Its simplex consequence is neat, but the proof occupies only the standard affine-barycentric and reservoir-sampling ideas needed to turn a static simplex encoder into a clocked online encoder.
4. The critical cube threshold, the dimensions five and nine, and the checkpoint random-access geometry are prior mathematics. Revision 31 now says so correctly. Once those claims are removed from the novelty account, the new geometric content is the online update formula and an elementary tensor closure.
5. The model remains narrow and permissive: time-varying phase-dependent state sets, an external clock, exact atomic stochastic rows, an uncharged transition table, a fixed acquisition order for the upper construction, and one terminal query. The fair-bit implementation is welcome, but it changes the resource count and assumes a self-paced protocol.
6. The repository-wide Foundations pipeline is not advanced at any of its decisive analytic gates. A2, B4, C2, the eleven-paper aggregate, fully adaptive collision scheduling, all finite query counts, and the sharp second-order streaming problem remain open by the manuscript's own status files.

The appropriate editorial conclusion is therefore straightforward: **the paper may deserve consideration by a specialist journal after substantial repositioning and a broader literature audit, but it should not be revised again under the fiction that it is approaching the level of the four leading general mathematics journals.**

---

## 1. Scope of this review

I reviewed the focused revision-31 article and the repository records needed to evaluate both its local mathematics and its place in the larger pipeline. In particular, I examined:

- `papers/GTF-I-v31-compatible-memory/main.tex`;
- `introduction.tex`;
- `affine-sections.tex`;
- `incompatibility.tex`;
- `additive-synthesis.tex`;
- `critical-simplices.tex`;
- `rac-equivalence.tex`;
- `implementation.tex`;
- `conclusion.tex`;
- `references.tex`;
- `RESPONSE_TO_REFEREE.md`;
- `LITERATURE_AUDIT.md`;
- `HISTORY_AUDIT.md`;
- `RESOURCE_LEDGER.md`;
- `PROOF_STATUS.json`;
- `PIPELINE_STATUS.json`;
- `verify.py` and the finite exact-check records;
- the revision-31 build receipt and theorem-location records;
- the complete fifteenth referee report;
- the revision-30 source chain to which the response refers;
- the repository-level `ROUND17_PROOF_DEPENDENCY_LEDGER.md`.

I also compared the revision-30 publication head with the revision-31 referee-ready head. Revision 31 is additive at the repository level: the prior report and the new package are retained, rather than older manuscript material being silently overwritten. This is good provenance practice, but it is not evidence for theorem correctness or journal significance.

The 14-page article is sufficiently self-contained to audit the new local arguments. The 390-page cumulative mathematical manuscript and 943-page development volume are therefore archival records, not necessary proof supplements for the claims under review. I did not treat regression scripts, negative controls, hashes, page comparisons, compilation receipts, or preservation certificates as substitutes for mathematical proof.

---

## 2. What revision 31 genuinely repairs

The revision should receive explicit credit for addressing the previous report rather than evading it.

### 2.1 The missing compatibility phenomenon is now witnessed

Revision 30 had a normal-form feasibility statement but no example showing that separately rank-minimal positive factorizations could fail to coexist in one causal machine. Revision 31 supplies such an example with full support. It also determines the complete feasible two-cut profile region, rather than merely proving that `(3,3)` is impossible.

This is a genuine mathematical improvement. The paper can no longer be dismissed on the ground that its “compatibility obstruction” is only a rephrasing of unknown transition coefficients.

### 2.2 The low-rank positive result is intrinsic

The canonical section

```text
L_t = aff(R_t) intersect P_t
```

is defined from the complete causal array, not by existentially quantifying over a desired realization. The normalized-shift closure is proved directly. When every section is a simplex, its vertices give compatible states at all cuts. This is much cleaner than the revision-30 coherent-enclosure witness.

### 2.3 The cube/simplex priority defect has been corrected

The article now states the absorption-index normalization, credits the universal factor and the known critical dimensions, distinguishes criticality from perfectness, and isolates the online consequence as the possible contribution. The explicit five- and nine-dimensional matrices are used as inputs to the online theorem, not advertised as new simplices.

### 2.4 The random-access-code comparison is now accurate

Revision 31 proves the support-function exactification argument and credits the corresponding cube-containment geometry. It no longer suggests that exact conditional rows alone define a strictly harder checkpoint-cardinality problem than worst-case private-randomness random access coding.

### 2.5 The implementation conventions are materially improved

The article now distinguishes atomic stochastic rows from fair-bit sampling, charges the sampler's phase, current input, old label, and prefix state, and gives an internal definition of a proper stochastic-language automaton. These changes remove several avoidable ambiguities in revision 30.

### 2.6 The response is honest about what remains open

The status files expressly decline to mark the historical analytic gates, all finite query counts, sharp second-order streaming, or fully adaptive collision scheduling as solved. This restraint is appropriate and should be preserved.

These improvements make the paper credible as a local specialist contribution. They do not make it a top-four contribution.

---

## 3. Technical audit of the principal new arguments

### 3.1 Canonical affine sections and the rank-two theorem

At cut `t`, the manuscript takes the affine span `A_t` of the normalized actual residual arrays and intersects it with the full causal polytope `P_t`. If `G` is in this intersection and has positive next-action probability, restriction to an action/report pair and normalization give

```text
G^{a,y} = sum_h [c_h p_{R_h}(a) / p_G(a)] R_h^{a,y}.
```

The coefficients may be signed, but they sum to one; validity and nonnegativity come from `G in P_t`. Thus the shifted array lies in the next residual affine span and in the next causal polytope. This argument is correct in the declared complete finite-interface model.

If `L_t` is a simplex, its vertices can be used as the cut-`t` states. Their action probabilities and barycentric decompositions of shifted continuations define the stochastic rows. Backward induction then recovers the specified array. The affine dimension gives the matching lower bound.

I see no hidden appeal to residual-state realizations in this proof. The chosen vertices may lie outside the residual hull, as they should. Zero-probability action rows are harmless because they are unreachable under the corresponding state continuation.

The rank-two conclusion is also correct: a nonempty compact section of affine dimension zero or one is a point or a segment, hence a simplex.

There are, however, two important qualifications.

First, this is a **clocked finite-horizon realization with cut-dependent state sets and rows**. It is not an autonomous positive realization with one fixed transition architecture. Converting it into an autonomous phase-tagged machine generally counts the union of the phase state sets, not their maximum.

Second, the mechanism is the standard invariant-convex-set construction of positive realization in finite form. The article cites Heller and Vidyasagar at a high level, but it does not provide a theorem-by-theorem comparison showing that the precise complete-array statement, rather than only its notation, is new. At top-four level, a general citation to classical antecedents is insufficient.

### 3.2 The full-support rank-three obstruction

The example specifies five two-dimensional terminal mean vectors after the command:

```text
(h,h), (h,-h), (-h,0), (-h/2,h x_1/4), (-h/2,h x_2/4),
9/10 <= h <= 1.
```

The four first-cut residuals form an affine square in the last two free coordinates, so the normalized residual rank is three. The second-cut residuals contain three affinely independent points, so that rank is also three.

The two upper constructions are explicit and check correctly.

- For profile `(3,4)`, the parent triangle with free-coordinate vertices

  ```text
  (-a,-a), (3a,-a), (-a,3a),  a=h/4,
  ```

  contains the four input corners with the displayed barycentric weights. The second register uses the four corners of the outer square.

- For profile `(4,3)`, the first register retains `x`, and every command-conditioned mean is represented in the triangle with vertices

  ```text
  h(1,1), h(1,-1), h(-1,0).
  ```

  The displayed weights reproduce all five columns and are nonnegative.

The lower bound against `(3,3)` is also coherent. Three first-cut generators containing the residual square must have the same affine plane as that square, so their free coordinate pairs must contain `[-a,a]^2`. Three second-cut decoder vectors form a triangle containing the first three fixed points. The forced-triangle lemma bounds every point in its vertical section at first coordinate `-h/2` by

```text
|y| <= beta(1-h) < h/2.
```

Every shifted first-cut generator must lie in that same decoder triangle, so all three parent free-coordinate vertices lie in a square of half-width strictly less than `h/2=2a`. The trace lemma says that a triangle contained in a square of half-width `b` cannot contain `[-a,a]^2` unless `b>=2a`. This gives the contradiction.

The constants are consistent. At `h=9/10`, the strict margin is positive, and all terminal probabilities lie in `[1/20,19/20]`. For `h<1`, the array has full support. The proof permits arbitrary legal stochastic state continuations; it does not assume that internal states are residuals.

I therefore do not identify a mathematical error in Theorem `thm:obstruction`.

The significance problem is different. The example is deliberately engineered from two triangles and one square. It has two memory cuts, a fixed order, constant alphabets, and a gap of one state. No parameter makes the incompatibility gap grow. No theorem classifies which rank-three sections are compatible. No obstruction invariant is extracted from the example. No hardness result is proved. The phrase “the first possible maximum cut rank” is correct only in this narrow finite clocked model and should not be allowed to suggest a broad positive-realization phase transition.

### 3.3 Additive encoders and weighted replacement

The additive theorem is correct. Coordinatewise subtraction of the scalar minima produces

```text
lambda(x) = w_0 q_0 + sum_i w_i q_i(x_i),
```

where the `w_i` are input-independent nonnegative masses. The update that retains the old label with probability `W_{t-1}/W_t` and otherwise redraws from `q_t(x_t)` has exactly the required running mixture law. It uses no stored selector indicating which summand generated the current label.

The argument works under every **externally prescribed** permutation. It does not construct an input-dependent adaptive acquisition policy, and it does not remove the external clock. If `W_{t-1}=0`, the “dummy” label should explicitly be chosen from the existing `m` labels to avoid even the appearance of an uncounted extra state; this is easily repaired.

The simplex corollary is also valid. With exactly `r` affinely independent generators, barycentric coordinates are affine functions of the channel vector. If the channel is additive in product coordinates, those coordinates are additive stochastic encoders and the replacement theorem applies.

For the binary-query cube, `n+1` decoder points enclosing a full-dimensional contracted cube necessarily form a simplex. Thus a checkpoint optimum of `n+1` states has an online fixed-order realization with the same peak, and the checkpoint lower bound applies to adaptive acquisition as well.

Again, correctness is not the issue. The construction is mathematically elementary. It is a weighted reservoir/mixture replacement scheme after a one-line nonnegative decomposition. The manuscript does not provide a serious theorem-level comparison with online mixture sampling, weighted reservoir sampling, sequential categorical sampling, or related finite-state constructions. Without such a comparison, the paper has not established that the general additive theorem is new in substance rather than in terminology.

### 3.4 Critical simplices and non-Hadamard dimensions

At the critical signal `eta=1/n`, equality in the trace inequalities forces the barycentric identities

```text
a_s = 1/(n+1) = ||b_s||_1/n,
sum_s |b_{s,i}| = 1,
sum_s b_{s,i} = 0.
```

The local distributions

```text
q_i(s|x_i) = |b_{s,i}| + b_{s,i} x_i
```

are therefore probability vectors. Averaging them through the replacement update yields the barycentric encoder of `x/n`. This proof is correct and does not require Hadamard orthogonality.

The displayed dimension-five and dimension-nine matrices have the claimed role: they are classical critical simplices whose inverse barycentric data supply rational online rows. The resulting six- and ten-state online realizations are legitimate consequences.

The normalized tensor proposition is also algebraically correct. Under Kronecker products, the uniform first inverse row and unit absolute column sums multiply, and the remaining augmented columns stay in the cube.

But almost all of the geometric depth here is inherited. The critical factor, the seed simplices, and the distinction between critical and perfect simplices are classical. The new online formula follows immediately from the additive theorem. The tensor closure is elementary Kronecker algebra. These are useful corollaries, not four-journal geometric advances.

### 3.5 Checkpoint exactification and random-access coding

The support-function proof is sound. If a fixed decoder dictionary achieves worst-case signed margin at least `eta`, then for every direction `u`, choosing the input corner with signs matching `u` gives

```text
h_{conv D}(u) >= eta ||u||_1.
```

This is exactly the support function inequality for containment of `eta[-1,1]^n`. Containment gives an exact convex representation of every target `eta x` after changing only the encoder. Hence worst-case success and exact conditional synthesis have the same minimum checkpoint alphabet in the stated private-randomness model.

Revision 31 correctly treats this as a translation of existing random-access geometry, not a new exponent or a new static cardinality problem. That correction is important. It also removes a large portion of the novelty rhetoric available to earlier revisions.

### 3.6 Finite fair-bit implementation

The rejection sampler for a rational row of denominator `D_rho` is standard and correct. A `b_rho`-bit proposal is accepted with probability greater than one half; no trial counter is needed because rejection returns to the prefix-tree root. The expected bit count is less than `2b_rho`.

The stated state bound is generous but valid once phase, old label, current input, prefix nodes, ready states, and terminal states are included.

This result must remain separate from the atomic-row theorems. It assumes a self-paced protocol in which the environment waits for a ready boundary; it charges a state factor depending essentially on the denominator; and it still treats the row table and cumulative-sum lookup as program data. It is not a proof that the atomic optimum survives implementation.

### 3.7 Probabilistic residual automata

The new definition resolves the previous normalization ambiguity. In the finite language example, query-phase residuals are the extreme corners of an affine cube. A residual state language supported on the remaining two-symbol words must be one of those query-phase residuals, so extremality forces `2^n` residual states. The phase-tagged reservoir construction supplies the polynomial unrestricted-positive realization.

The proof is credible in the stated proper-automaton convention. It remains an inherited illustrative separation rather than a new central theorem of revision 31.

---

## 4. The compatibility obstruction is real, but it is not yet a theory

The strongest new item is Theorem `thm:obstruction`. It deserves publication-level attention. It does not carry the weight assigned to it by the Foundations branding.

A top-four structural result would normally do more than exhibit one constant-size failure. For example, one might expect at least one of the following:

1. a computable invariant characterizing compatibility on a broad natural class;
2. a family with an unbounded gap between separate and simultaneous positive ranks;
3. an arbitrary-horizon obstruction theorem;
4. a complexity classification for deciding a prescribed state profile;
5. a topological, combinatorial, or convex-geometric obstruction stable under natural operations;
6. a connection resolving a recognized open question in hidden Markov or positive realization theory;
7. a classification of rank-three sections, rather than one rank-three counterexample.

Revision 31 provides none of these. It proves that the first obstruction can occur at rank three, in the sense that rank at most two is automatically compatible and a particular rank-three array is not. That is a sharp threshold for the **existence of some counterexample**, not a classification of the rank-three regime.

The exact Pareto frontier `(3,4),(4,3)` is elegant, but its proof is tightly tied to the chosen coordinates. The forced-triangle estimate has not been elevated into a reusable obstruction calculus. The example therefore answers the fifteenth report's minimum request; it does not satisfy the much higher standard of a general-journal centerpiece.

A fair description is:

> Revision 31 proves a clean first example of causal incompatibility between individually minimal positive factorizations and identifies a low-rank class where incompatibility cannot occur.

That would be a respectable specialist abstract. It is not “General Theta Foundations.”

---

## 5. The positive-realization novelty boundary remains underdeveloped

The article's bibliography is far too small for the breadth of its claims. It moves among finite-horizon causal arrays, positive realization, invariant convex sets, stochastic automata, residual automata, nonnegative rank, cube absorption, random-access coding, and streaming memory with roughly ten references.

The paper acknowledges classical invariant-cone and residual mechanisms, but the comparison remains generic. The authors should answer precise questions.

- Is the canonical section `aff(R_t) intersect P_t` a known minimal invariant polytope construction in finite-horizon positive realization under another name?
- Is simultaneous realization by vertices of shift-invariant sections already implicit in standard realization proofs?
- Is the rank-two consequence known for two-dimensional cones or interval-valued normalized sections?
- How does the two-cut profile problem relate to sequential nonnegative factorizations, switched positive systems, controlled hidden Markov realizations, and finite-state transducer minimization?
- Are there known examples of incompatible local nonnegative factorizations in adjacent literatures?
- What decision problem is genuinely new here, and what is its computational complexity?

The current audit says that an exhaustive review of the classical sources has not been completed. That admission is honest, but it is disqualifying for a top-four originality claim. A paper cannot span several mature subjects, offer only a handful of citations, and shift the burden of priority clearance to future referees.

The same problem applies to the additive theorem. The weighted replacement update is sufficiently elementary that independent rediscovery is highly plausible. The authors need a serious comparison with existing reservoir and online-mixture constructions before calling it a new general synthesis principle.

---

## 6. The online simplex theorem has limited scope

The strongest positive online statement is

```text
K_n(eta)=n+1
iff W_n^fo(eta)=n+1
iff W_n^ad(eta)=n+1.
```

Within the definitions used, this is correct. Its scope is much narrower than a casual reading suggests.

- It addresses only the **minimum full-dimensional alphabet**, namely `n+1` states.
- It relies on the checkpoint codebook being a simplex. It says nothing comparable for larger nonsimplicial dictionaries.
- It controls the peak number of labels in a clocked machine, not the sum of phase-tagged autonomous states.
- It gives a fixed-order upper construction. Equality for the adaptive optimum follows by sandwiching, not from a new adaptive policy.
- It does not determine the optimal state count for general finite `(n,eta)`.
- It does not determine the varying-signal regime.
- It does not give a second-order law.
- It does not give an efficient procedure for constructing general optimal codebooks.
- It does not charge program description, transition-table access, or arithmetic complexity.

The dimensions five and nine are attractive examples precisely because the static simplices already exist. They do not show that the paper can discover new critical dimensions or new absorption geometry.

The tensor family is explicit, but it is generated by a basic closure operation from known seeds. It does not resolve the general critical-dimension problem and should not be presented as if it materially changes that landscape.

---

## 7. The resource model is legitimate but should not be marketed as ordinary streaming complexity

The primary state count is the number of persistent labels at a cut. The machine additionally receives substantial free structure:

- an externally declared time index;
- cut-dependent transition rows;
- exact atomic stochastic sampling;
- an uncharged program and transition table;
- no charge for row-construction time or arithmetic;
- a fixed prescribed acquisition order for the constructive theorem;
- a single query supplied only after acquisition;
- no requirement that one autonomous state set be reused across phases.

There is nothing mathematically illegitimate about this model. It belongs naturally to finite positive realization. It is not the standard computational meaning of a streaming algorithm with a succinct update rule.

The finite-coin proposition makes the distinction clearer rather than eliminating it. Its sampler uses more states, depends on rational denominators, and assumes a self-paced interface. For general real algebraic or irrational rows, no finite fair-bit implementation theorem is provided. For the old exponential codebooks, program description and construction remain uncharged.

The title and abstract now say “atomic stochastic-row model,” which is an improvement. Nevertheless, the word “online” must consistently be read in this specialized transducer sense. Claims of broader streaming-memory significance should be reduced.

---

## 8. Pipeline assessment

The repository-wide proof dependency ledger has two long analytic chains:

```text
A2 -> A3 -> A4 -> C2 -> D1
```

and

```text
B2-GC -> B1 -> B2-MC -> B3 -> B4 -> C1/C2 -> D1.
```

Their gates involve branchwise Fourier and local-limit theory, stopped large deviations, global kernels, nonlinear semigroups, graph cores, filtering regularity, optional projection, and typed contraction. The finite positive-realization theorems in revision 31 do not discharge any of those obligations.

The manuscript's own `PIPELINE_STATUS.json` correctly records as false:

- `historical_A2_replaced`;
- `B4_aggregate_closed`;
- `C2_aggregate_closed`;
- `eleven_paper_aggregate_closed`;
- `fully_adaptive_collision_solved`;
- `all_finite_query_counts_solved`;
- `sharp_second_order_streaming_solved`.

That is the decisive pipeline fact. Revision 31 is a local side result in positive realization and online query encoding. It is not a bridge theorem for the main analytic DAG.

The 390-page and 943-page cumulative volumes preserve history. They do not magnify the novelty of the 14-page article. Indeed, including them in a normal journal submission would make the paper harder to evaluate and would create the misleading impression that the referee is responsible for certifying a thousand-page repository history.

The repository engineering is unusually careful. The mathematics must still stand on the focused article alone, and for the new claims it largely does. That is exactly why the cumulative volumes should be excluded from the editorial case.

---

## 9. Editorial assessment of the focused article

The reduction from the earlier sprawling manuscripts to a 14-page paper is a major improvement. The current article has a visible theorem spine:

1. canonical affine sections;
2. a rank-two positive result;
3. a rank-three incompatibility example;
4. additive online synthesis;
5. critical-simplex corollaries;
6. checkpoint exactification;
7. implementation conventions.

That structure should be retained.

However, the paper still tries to carry too many inherited results and programmatic associations. The residual-automaton separation, previous entropy theorem, prior block construction, historical collision models, and aggregate pipeline discussion dilute the central contribution. They are not needed to prove the new theorem pair.

A specialist submission would be stronger if it were honestly presented as a paper about **compatible positive realizations of finite causal arrays**, with the query-channel simplex theorem as an application. The title “General Theta Foundations I” has no mathematical meaning visible from the focused paper and suggests a foundational status that the results do not possess.

The current title is therefore not merely grandiose; it actively impedes accurate classification by editors and readers.

---

## 10. Minimum changes for a credible specialist submission

These changes are not a route to top-four acceptance. They are the minimum needed for a fair specialist review.

### 10.1 Reposition and retitle the paper

Remove “General Theta Foundations I.” Use a title that names the actual problem, such as compatible positive realization of finite causal arrays or online realization of simplex encoders. The abstract should lead with the two-cut obstruction and the rank-two theorem, not the repository program.

### 10.2 Give a complete theorem-level literature map

The authors must compare the canonical-section theorem and the incompatibility example with positive realization, invariant cones/polytopes, hidden Markov realization, probabilistic automata, sequential nonnegative factorization, and controlled finite-state transducers.

The additive update must be compared with weighted reservoir and online-mixture sampling. A vague statement that classical antecedents exist is not enough.

### 10.3 Formalize the machine model in one definition

State explicitly:

- the finite horizon and alphabets;
- the order of action and report;
- whether reports are adversarial/external rather than probabilistic;
- the state set at each cut;
- initialization, action, update, and terminal rows;
- the role of the external clock;
- the treatment of zero-probability rows;
- what buffers are charged;
- whether “state count” means available or reachable labels;
- the distinction between clocked and autonomous realization.

At present these conventions are recoverable, but they are distributed through prose.

### 10.4 Separate new theorems from inherited material

The 14-page article should identify, in a single contribution table, which statements are:

- new in revision 31;
- inherited from revision 30;
- classical external inputs;
- immediate corollaries;
- implementation lemmas.

The static critical simplices and random-access checkpoint equivalence must remain explicitly classified as prior mathematics.

### 10.5 Either deepen the compatibility theory or reduce the claims

A substantially stronger paper could develop:

- an unbounded incompatibility-gap family;
- a multi-cut hierarchy;
- a classification of rank-three sections;
- a decision-complexity theorem;
- a robust obstruction invariant;
- natural closure operations preserving or amplifying incompatibility.

Without such a development, the paper should present the example as a first counterexample, not as a foundational classification.

### 10.6 Remove the cumulative volumes from the submission package

Retain them in the repository if desired, but do not ask an editor to treat 390- and 943-page compilations as part of the paper under review. The focused source, proofs, response, and a modest reproducibility supplement are sufficient.

### 10.7 Obtain an independent priority audit

The repository's own status says independent review is incomplete. That is appropriate. Before publication claims are sharpened, someone familiar with classical positive systems and probabilistic automata should independently assess the novelty boundary.

---

## 11. Specific major and minor points

1. **Define the clocked machine formally.** The paper currently defines the causal array more carefully than the realizing machine.
2. **Clarify cut-dependent states.** “A single machine” may be misread as one autonomous state set; the theorem uses phase-dependent vertices and rows.
3. **Qualify the rank-three threshold.** It is the first rank at which this paper exhibits a counterexample, not a general phase transition in positive realization.
4. **Clarify “separately admit three states.”** This means each lower bound is attained in a joint machine whose other cut may use four states; it is not merely an amputated static factorization.
5. **State the profile convention.** Explain whether padded or unreachable labels count when taking the upward closure of the feasible region.
6. **Keep the full-support endpoint precise.** Full support holds for `9/10 <= h < 1`; the endpoint `h=1` has deterministic terminal rows.
7. **Choose the zero-prefix dummy from `[m]`.** This avoids an apparent extra state in Theorem `thm:additive`.
8. **Do not call the fixed-order construction adaptive.** The adaptive equality at `n+1` is obtained by a lower-bound sandwich.
9. **Define `K_n`, `W_n^fo`, and `W_n^ad` in full.** The introductory table is not a substitute for optimization definitions with all resource conventions.
10. **State the `n=1` output convention.** The phrase “a final binary output requires no more than `n+1` labels” meets equality at `n=1`; the counting convention should be explicit.
11. **Separate static and online theorem names.** Titles should make clear when a statement is a classical inclusion and when it is the new implementation.
12. **Reduce the tensor proposition's rhetoric.** It is an elementary closure of normalized augmented matrices, not a new general theory of critical simplices.
13. **Expand the positive-realization bibliography.** The current list cannot support the claimed breadth.
14. **Expand the online-sampling bibliography.** The additive replacement mechanism needs direct comparison with existing sampling constructions.
15. **Do not count verification volume as evidence of significance.** Millions of finite checks would still not prove a universal theorem or establish novelty.
16. **Keep the fair-bit model separate.** The self-paced implementation and the atomic-row optimum are different resources.
17. **State table-lookup assumptions.** The finite sampler counts control states but not the storage or computation of cumulative row tables.
18. **Do not imply efficient construction.** The article gives explicit rows for rational critical families, not a general efficient optimizer for checkpoint dictionaries.
19. **Remove references to “complete preserved development” from the mathematical sales pitch.** Preservation is archival, not a theorem.
20. **Shorten the conclusion's pipeline discussion.** A focused paper should not require the reader to understand A2/B4/C2 labels to know what was proved.
21. **Distinguish ordinary rank, affine rank, nonnegative rank, and state complexity in a formal diagram.** The prose has improved, but the terminology remains easy to conflate.
22. **State whether all vertices of `L_t` are algorithmically enumerated or merely existential.** The explicit-array setting permits finite enumeration, but output size can be exponential.
23. **Avoid complexity language without an input model.** “Decidable” and “computable” require a representation and bit-complexity convention.
24. **Keep prior entropy results outside the novelty summary.** They are not new to revision 31 and their leading exponent is classical.
25. **Do not use the repository's revision history as external validation.** Fifteen internal review cycles are provenance, not peer review.

---

## 12. Scorecard

| Criterion | Assessment |
|---|---|
| Correctness in the stated model | The main new proofs appear coherent; no short fatal counterexample found |
| Originality | A genuine new-looking finite obstruction and useful online corollary, but the classical boundary is broad and incompletely audited |
| Mathematical depth | Moderate for a specialist paper; far below four-journal level |
| Generality | Narrow finite-horizon, clocked, atomic-row model; constant-size obstruction |
| Quantitative strength | No unbounded gap, no second-order law, no general finite counts, no complexity result |
| Pipeline impact | Essentially none on the principal A/B/C/D analytic gates |
| Presentation | Substantially improved and focused, though the branding and auxiliary package remain disproportionate |
| Reproducibility engineering | Strong, but not evidence of proof or significance |
| Editorial recommendation | Reject at top-four level; consider only after specialist repositioning |

---

## 13. Final assessment

Revision 31 is the first version of this project that I would describe without qualification as containing a coherent, focused mathematical paper. The authors have supplied the counterexample that the preceding report demanded, and they have corrected several priority and modeling defects. The rank-three profile theorem is nontrivial and appears correct. The additive online construction is clean. The article is readable without reconstructing the entire repository.

That positive judgment should not be confused with a recommendation for a leading general journal.

The central obstruction remains a small bespoke example. The low-rank theorem is a simple consequence of a classical invariant-section mechanism. The online simplex transfer is an elementary affine-mixture construction. The static geometry and checkpoint coding results are inherited. The computational model is permissive. The main repository pipeline remains open at every difficult analytic gate.

Put bluntly: **the repository has successfully converted a missing example into a respectable local theorem; it has not converted that theorem into a foundational theory.** The thousand-page preserved history does not change that assessment.

My recommendation is therefore final at the stated editorial level:

**Reject for Annals of Mathematics, Inventiones Mathematicae, Journal of the AMS, or Acta Mathematica.**

A substantially retitled and literature-complete version, stripped of the Foundations framing and presented as a specialist contribution to positive realization and finite stochastic transducers, could merit a fresh evaluation elsewhere.