# Response to the thirteenth pipeline-aware referee report

**General Theta Foundations I — Revision 29**  
**Intrinsic Continuation Geometry and Causal Memory**  
24 September 2026

The controlling report is `reviews/general-theta-foundations-i-v28-pipeline-harsh-top4-r13-2026-09-24/REFEREE_REPORT.md`, frozen at `9c8161e9df1b017fa2dfb46218a4fa42f42e9bdd`. Its reviewed v28 head is `cdc749027c5f7a6f66c572ea498cd15e1b1a3391`; its native mathematical source is `0bc3eabddc3c08b8d736cc939937b0cc349e1a89`. The new work branch was created remotely from the controlling report before manuscript publication. The separate pre-existing v29-intrinsic-memory branch is not modified.

The report accepts the positive-noise saddle, Brownian identification, all-fixed-clock memory theorem and support-boundary jump. Its principal objection is that the general capacity field depends on analyst-selected witnesses. This revision changes the mathematical input of the classification: the input is the complete causal response array, and the invariant uses **all** of its normalized residual continuations. A finite geometric completeness condition then supplies both the lower profile and a single compatible upper machine. A growing binary-query experiment separately shows how online positive memory can be linear or exponential despite the same ordinary predictive rank.

The stable labels below refer to the native LaTeX. `evidence/THEOREM_LOCATIONS.json` records the actual numbers and pages in the compiled article. Successful tests do not supply the proofs or settle journal significance.

## 7.1 / Section 5 — from facial certificates to an intrinsic theorem

**Addressed for a finite, decidable completeness class.**

`intrinsic-continuation.tex`, Definition `def:csr29`, uses the entire finite residual set at each charged cut. Two normalized continuations are adjacent when their minimal faces in the polytope of causal arrays intersect. For each connected component, take its affine dimension plus one. The sum is `s_t(C)`; it is determined by the experiment and charged interface, without a supplied witness family or trial program.

Theorem `thm:intrinsic29` proves, for arbitrary stochastic realizations,

```
K_t >= s_t(C).
```

The proof allows internal continuation generators outside the residual hull. A generator used with positive probability must belong to the minimal face of the row it helps represent; it cannot serve two distinct support components. Within a component, affine rank gives the remaining state bound.

For the upper direction, the extreme residuals of every component hull give a single realization with profile `e_t(C)`. A chosen residual's next-action probability is independent of the unread report. Its normalized shift is another actual residual, which is decomposed into the next cut's extreme residuals. These decompositions supply legal stochastic updates **simultaneously**. This is not a splicing of independent cut ranks.

When each component hull is a simplex, `s_t(C)=e_t(C)` at every cut, and the whole minimum profile and peak are exact. The condition is checked by face-intersection feasibility, graph components, affine rank and extreme-point tests. It is not defined as existence of a minimum-size machine. An explicit full-support nonsimplicial square has rank three and needs four states, showing that the test is substantive and not universal.

Corollary `cor:intrinsic-schedule29` replaces the old selected-certificate capacity by the intrinsic field for terminal channels passing this test at every schedule vertex. The same residual restrictions give a compatible realization on the full declared schedule graph. Thus the bottleneck recurrence now optimizes a complete field for that class, not merely certificates discovered by the analyst.

The theorem is finite and effective for explicit rational or real-algebraic arrays. The explicit table may be exponentially large in the horizon; no efficient algorithm for a succinct arbitrary controller is claimed. The theorem is clocked. Additional autonomous shared-row equalities require their own check. Almost-sure partial specifications must be completed or optimized over completions, rather than silently treated as a unique full array.

## 7.2 — adaptive scheduling charged to the same memory

**A general specified-array criterion and exact adaptive-acquisition results are proved; the original fully adaptive collision schedule is not identified with them.**

In the intrinsic theorem, an observation-dependent next action is part of the causal response array. The action's probability cannot depend on the report it precedes, and its persistent protocol information must pass through the charged register. The theorem therefore applies to a specified adaptive array satisfying its geometric test. It does not claim that optimizing over all such arrays reduces to selecting one fixed path.

The growing experiment in `streaming-access.tex` permits the next unread input coordinate to depend on retained observations and randomness. After all coordinates have been acquired, an atomic external query arrives. Every input-dependent acquisition choice and every past random choice must pass through the query-cut state. Therefore every adaptive controller still factors as a single encoder and decoder. The lower bounds in Theorem `thm:access29` apply to all such adaptive schedules, and fixed-order constructions match them. The complete acquisition schedule consequently cannot improve either exact peak regime.

Corollary `cor:barrier29` gives a second adaptive-acquisition/output-order theorem for a specified independent product channel at a preparation barrier. The full labelled output law factors through the retained state, irrespective of output order, and the rank converse matches full retention.

These are exact adaptive resource statements for growing families. They do not assert that every report-dependent collision validation scheduler has peak at least twelve. The v28 twelve-state physical theorem remains an exact result over externally declared clocks, with its original quantifier intact.

## 7.3 — scalable families and exact growth, not another isolated state count

**Addressed by product closure and two exact regimes of one binary-query family.**

Theorem `thm:tensor29` proves closure of the componentwise-simplicial terminal-channel class under independent products. Component graphs multiply; normalized simplex vertices are linearly independent; their tensor products are independent. The exact capacity is multiplicative even against correlated internal generators. This is a theorem for a specified joint product channel, not a general multiplicativity claim for nonnegative rank or minimax scores.

Theorem `thm:access29` uses a binary final answer, while the input length n grows. The specified channel is

```
Pr(B=b | x,j) = (1+b*eta*x_j)/2,   x in {-1,1}^n, j in [n].
```

All conditional probabilities are prescribed. The query is revealed only after acquisition. Its checkpoint memory is the least number of outer-cube points whose convex hull contains the inner cube `[-eta,eta]^n`. The ordinary predictive rank is n+1 for every eta>0.

The exact whole-schedule peak is

```
W_n(eta) = n+1     for 0 < eta <= 1/n^2,
W_n(eta) = 2^n     for 1-1/n < eta <= 1.
```

For n>=2 both regimes include full-support channels. The weak-signal upper proof is not just a final enclosing simplex. It constructs a sequence `P_t` of (t+1)-vertex simplices satisfying `P_t x {-eta,+eta} subset P_(t+1)`. Explicit barycentric stochastic rows achieve the exact minimal profile t+1 after t input bits. The machine stores only a vertex label, not a real vector. All acquisition rows are rational and independent of eta; the specified decoder contains eta.

In the strong-signal regime a disjoint corner-cap argument requires one distinct state generator for each of the 2^n input words. Both peak lower bounds survive adaptive acquisition. Thus the same full-support rank n+1 can equal the causal memory or be exponentially below it. Intermediate eta is not filled with an unsupported formula.

Proposition `prop:access-approx29` additionally distinguishes exact synthesis from approximation: a fair-output one-state channel has row-TV defect eta/2, while any approximation through at most n query states has defect at least eta/(2*sqrt(n)). These are not asserted to be matching approximation bounds.

## 7.4 — a real downstream consumer and the historical pipeline

**The structural theorem has explicit proof consumers; independent historical chains are preserved.**

The marked saddle's five forced rows have canonical support components of sizes 2,1,2 and dimensions 1,0,1. Proposition `prop:marked-csr29` applies the invariant to recover the five-state decision count, including arbitrary stochastic encoders and averaged mark rows. Contact is necessary first: a cheap Bayes tie rule that fails uniform minimax stationarity is not an eligible response. The theorem recasts the formerly selected faces as the complete intrinsic graph of these forced rows.

Theorem `thm:tensor29` gives capacity 5^m for independent products of the specified marked membership-continuation channel. A product output law is explicitly required; additive scores or independent inputs do not alone force it. No all-N minimax equality is inferred.

The new online weak-signal construction also consumes the continuation-shift principle in an essential way. A checkpoint convex factorization alone could not certify its t+1 profile at every prior cut.

The current frozen Round-Seventeen ledger was consulted. Its A2 -> A3 -> A4 -> C2 -> D1 chain and hard-sphere B2/B1/B3/B4/C1/C2/D1 chain keep their own Fourier, LDP, operator-domain, semigroup and optional-projection gates. The present finite-array theorem neither removes those obligations nor rewrites them as consumers by metadata. The report explicitly permits one strong route; this revision pursues intrinsic classification and scalable causal synthesis rather than fabricating a program-wide replacement proof.

## 7.5 / Section 4.6 — theorem-level originality comparison

**The comparison is in the article, not only in a bibliography table.**

`literature-theorems.tex` identifies the precise points of overlap and distinction.

- Heller/Vidyasagar: positive realization is a classical framework, not a new normal form claimed here. Our finite input and geometric completeness test are specified separately.
- Denis–Esposito, Proposition 16 and residual-automaton results: canonical residual generating sets and residual-vertex realization have precedents. Minimality among residual-state automata is distinguished from minimality among all stochastic realizations. The new lower argument permits generators outside the residual hull.
- Gillis–Glineur, Definition 1 and Theorem 1: restricted nonnegative rank and nested polytopes are explicitly distinguished from ordinary rank. The checkpoint cube containment is elementary conditioning; the additional online content is the compatible sequence of enclosing simplices.
- Reusch–Merzenich: incomplete specifications and compatible coverings are relevant at support boundaries. We do not infer a unique full completion from an almost-sure law.
- Random-access coding: Ambainis–Leung–Mancinska–Ozols and the inspected 2026 work of Kondo et al. and Liu are discussed. Private-randomness encoder/decoder factorization is not new. The present task fixes every conditional probability and charges the streaming encoder; it does not assert optimal average or worst-case success for all message sizes.

No exhaustive priority clearance for all realization or filtered-experiment literature is claimed. In particular, Norberg's original proof-level comparison remains distinct. The novelty case rests on the explicitly stated geometric completeness theorem, simultaneous realization and streaming synthesis, not on an assertion that classical ingredients have no predecessors.

## Section 6 / editorial comments — known-target and acquired-target semantics

The abstract, introduction, contact application and resource ledger now all state the convention. Exact five/twelve physical state counts require a specified target and its exact atomic stochastic row. The acquired-target proposition is a finite-counter, finite-precision approximate-score theorem. It does not recover an unknown algebraic tie probability exactly with the same counts. This applies equally to the specified eta in the new query experiment.

The introduction includes a compact mathematical flow diagram and a single theorem spine. The old substantive mathematical body has been moved intact into supporting appendices of the same canonical manuscript; no proof has been replaced by a pointer to a build receipt. All eighteen inherited mathematical modules are byte-identical, and the assembly verifies recovery of the old body. Old repository paths and cumulative volumes remain unchanged. The earlier introduction is retained in those paths and volumes.

The large-N endpoint/localization theorem, physical noise/order results, autonomous testing, quantitative certificates, revelation laws and acquired transport remain available with their original statements. No weak new asymptotic claim is added merely to fill a checklist. Compilation and preservation are delivery checks, not the conceptual answer to the report.
