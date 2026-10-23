# External Referee Report — *General Theta Foundations I: Acquired Geometry and Causal Resource Transfer*

**Submission:** *General Theta Foundations I: Acquired Geometry and Causal Resource Transfer*  
**Author:** Qian Qi  
**Repository:** `TrillionniumFoundation/theta-theory`  
**Reviewed referee-ready branch:** `referee-ready/general-theta-restart-r64-primal-dual-risk-2026-10-16`  
**Reviewed exact branch head:** `6ec637d01349ff4525fdc064ab00489442798aaf`  
**Reviewed branch root tree:** `0405bff7f28ce4a9f84150778f067239c83aab6a`  
**Ordinary mathematical-source commit:** `7e397f934457894d1dba961cb126e9aef9023dfc`  
**Ordinary source root tree:** `58697d6a88962611f742b9e0b539603abfde1b0a`  
**Current paper tree:** `2fb9a4d5c12c65bab080e3a5b29b397d34823098`  
**Native main PDF:** 85 pages, SHA-256 `c326f7126d3c58543d650632c141104703979d683356f733888149b7e1112fa1`  
**Current supplement:** 10 pages, SHA-256 `d087df43fedb6aec6b4b6d08f662c082aad4a26430a64a775f558b164bac1903`  
**Retained complete R58 companion:** 37 pages, SHA-256 `32e81aa0fc581b4690398c4e57a62114c3c6850a1c8f757fe3f6a8216f067194`  
**Controlling previously deposited report:** R59 round 3, commit `c39922c242f9bd03d2e0d7f05d6e9b483362e26d`, report blob `eb9e20db36ae1297f4ee13369be8460e786d7546`  
**Review branch:** `review/general-theta-restart-r64-primal-dual-risk-external-top4-referee-r64-2026-10-16`  
**Date:** 16 October 2026

This is an author-requested external mathematical assessment deposited in the repository. It is not a commissioned editorial decision of a named journal, a formal proof-assistant certificate, an exhaustive priority certificate, or a claim of acceptance by any journal.

---

## Recommendation

**Reject at the level of the Annals of Mathematics, Inventiones Mathematicae, the Journal of the American Mathematical Society, or Acta Mathematica in the manuscript's present form.**

This is **not a technical-correctness rejection**.

Revision R64 is a genuine and substantial mathematical advance over the last externally reviewed R59 object and over the intervening R63 author baseline. It responds directly to several important requests in the R59 round-3 report. In particular, it does not merely add another realization or another finite certificate to the earlier geometric route. It adds a distinct optimality layer for the constrained primitive problem:

1. attainment of bounded terminal risk at every feasible expected-cost budget, including the least feasible budget;
2. monotone convergence of reserved finite-prefix problems to the full stopped optimum;
3. an exact resource-price dual for a fixed decoder dictionary;
4. compactness, in uniform total variation, of the complete performed stopped-law family at fixed dictionary and budget;
5. a finite-score decision criterion for exact budget-constrained realization and approximate deficiency;
6. same-budget finite-label density at every strictly interior feasible budget;
7. exact finite spectral cost/risk witnesses with total support at most the affine plan dimension plus one;
8. a common Bellman recursion and a complementary-slackness criterion for every used row;
9. an extension to several simultaneously imposed additive expected resources using one jointly strict fallback; and
10. an exact delayed-release budget curve, exact one-live-label curve, and exact live-state threshold for attaining the unrestricted timing law.

These additions are mathematically coherent. In the load-bearing new arguments I checked, I did not find an elementary gap invalidating:

- compactness of the common infinite-plan set in countable product coordinates;
- the survival bound derived from the positive open-call reserve;
- uniform bounded-loss tail control at the feasibility boundary;
- attainment and right-continuity of the constrained risk frontier;
- fixed-dictionary convexity and the endpoint resource-price dual;
- compactness and convexity of the complete performed stopped-law family in uniform total variation;
- the finite-score separation formula for the exact deficiency;
- the requirement that policies in the finite-score inner problem remain budget-feasible in every model, not only the finite support of the score prior;
- the same-budget finite-label completion and initialization mixture;
- the finite-dimensional active-gradient and normal-cone argument;
- conic compression to at most `k_T+1` total positive cost and risk atoms;
- the use of distinct cost and risk preparations;
- the pure spectral interpretation of active operator constraints;
- the common unnormalized Bellman recursion and its local slack identity;
- the multi-resource supporting-hyperplane argument under one jointly strict fallback and one coercive cost coordinate;
- the distinct-prior and hard-width duality-gap examples;
- the exact unrestricted delayed-release curve;
- the exact one-live-label geometric curve;
- the necessity and sufficiency of `K` live labels for exact attainment at target delay `K`; or
- the positive-cycle pumping lower bound for fewer than `K` live labels.

The new results materially improve the mathematical status of the paper. The negative top-four judgment instead concerns the **conceptual concentration, intrinsic reach, relation to mature constrained-control and occupation-measure theory, natural external consequences, and breadth suggested by the title**.

The central R64 optimality theorems work on a common finitely branching interface with a positive conditional call-cost floor, bounded terminal loss, compact decisions, and—where spectral finite witnesses are invoked—a compact continuous finite-dimensional primitive family, a fixed finite horizon and a fixed decoder dictionary. These are meaningful and reasonably broad hypotheses for the declared stopped experiment, but they do not yet yield an intrinsic classification of general prepared causal experiments. Nor do they solve a recognized difficult natural problem in stochastic control, sequential decision theory, causal coding, selective prediction, or quantum statistics.

The delayed-release theorem is exact and useful as a semantic test of complete stopped-law comparison. It remains a deliberately minimal one-command timing experiment. It demonstrates a real temporal memory obstruction, but it does not by itself supply the external mathematical consequence normally expected at a top-four general-mathematics journal.

For a strong specialist journal in stochastic control, mathematical statistics, sequential decision theory, information theory, constrained Markov decision processes, causal coding, or mathematical quantum information, my assessment is **favorable after a focused major revision**.

---

## 1. Review object, provenance, and pipeline inspected

A fresh complete branch enumeration immediately before this report identified

```text
referee-ready/general-theta-restart-r64-primal-dual-risk-2026-10-16
```

as the latest completed `General Theta Foundations I` referee-ready revision. The continuation page was empty. Existing external review branches stopped at R59 round 3; no R64 review branch was present.

The exact reviewed object is the terminal source-bound head

```text
6ec637d01349ff4525fdc064ab00489442798aaf.
```

Its sole parent is the mathematical source commit

```text
7e397f934457894d1dba961cb126e9aef9023dfc.
```

The final child changes no mathematical source. Relative to the source commit, it adds only:

```text
papers/General-Theta-Foundations-I-restart/r64-primal-dual-risk-publication/LOCAL_BUILD_RECEIPT.json
papers/General-Theta-Foundations-I-restart/r64-primal-dual-risk-publication/README.md
```

The current paper tree continues the genuine R63 source commit

```text
2bb08a6323fb0198e8ba93a4870b74304431fedc
```

and preserves the complete R63 paper tree under `retained/r63-native/`. The R59 reports are pinned as independent review inputs rather than merged into the author lineage.

The mathematical packet directly relevant to this review contains:

- the current 85-page main manuscript;
- the current 10-page technical supplement; and
- the complete retained 37-page R58 companion.

I treated the 85-page main manuscript as the editorial object. The supplement was used to audit the explicit common Bellman recursion, slack identity, conic compression and boundary-compactness qualifications. The retained companion was used only for provenance and for older exact-stopping and calibration semantics; it is not a hidden premise of the new R64 theorems.

The inspection included:

- `main.tex` and its full current section order;
- `sections/17-primitive-risk.tex` and `sections/19-compact-risk.tex`, on which the R64 completion results depend;
- all of `sections/20-primal-dual.tex`;
- all of `sections/21-timing-memory.tex`;
- the new quantifier and literature discussion in `sections/01d-decision-order.tex`;
- the current scope appendix;
- `supplement-primal-dual.tex`;
- `RESPONSE_TO_REFEREE.md`;
- `THEOREM_MAP.md`, `PROOF_AUDIT.md`, `PRESERVATION_MAP.md`, `LITERATURE_AND_PRIORITY.md`, and the hierarchical source manifest;
- the complete R59 round-3 report and the author's point-by-point response;
- the current references and the relation between R64 and the retained R63/R62/R61 lines; and
- the source-bound build record and current GitHub Actions status.

I did not independently re-prove every inherited theorem in all 85 pages, every result in every nested retained paper, or every independent realization branch. Inherited results were checked where they are load-bearing for the R64 completion, and the new R64 theorem chain was audited directly. Preservation and source identity are not fresh mathematical certification of every historical claim.

---

## 2. Executive assessment of the R64 mathematical architecture

R64 now contains two conceptually distinct routes.

### 2.1 Geometric transfer route

The earlier route derives a resource curve from an actual-history lower witness and one common all-model upper program. Its central quantifiers remain:

```text
there exists one lower operating witness
    valid against every competitor, reached history and legal command;

there exists one common upper program
    valid in every model and after every surviving history.
```

This route remains certificate driven. R64 preserves its actual-history comparison, finite-width task defects, singular geometry, common hazard construction, memory typing and classical/quantum realizations.

### 2.2 Primitive constrained-optimum route

The newer route starts directly from the raw finite action/report instruments and a common sequence-form plan. It first derives an all-state fallback from the absence of dark subspaces, then approximates the robust constrained risk on finite model families and compact uncertainty classes. R64 completes this route by proving optimality, not merely approximation:

- the full bounded-risk frontier is closed at the least feasible budget;
- fixed-dictionary plans form a compact convex decision class;
- complete stopped laws form a compact convex family in uniform total variation;
- exact complete-law deficiency is characterized by finite bounded score tests;
- fixed-dictionary risk has an exact resource-price dual;
- compact finite prefix problems have finite active spectral witnesses;
- one backward recursion evaluates the witness objective; and
- finite-label strategies approximate the full stopped optimum at the same interior budget.

This is a real mathematical response to the R59 request for a fuller decision comparison and an optimality side to the previous sufficient constructions.

---

## 3. Response to the R59 round-3 report

R64 is not a cosmetic revision. It addresses several major R59 criticisms with new mathematical statements.

| R59 concern | R64 assessment |
|---|---|
| The manuscript needed an actual new source revision rather than another report | **Resolved.** R64 is a new source commit continuing R63. |
| Full decision comparison was missing | **Substantially resolved at fixed dictionary and paid budget.** The complete performed stopped-law theorem uses all bounded measurable scores and yields exact deficiency. It is not an ancillary quantum-channel theorem. |
| The geometric theorem was certificate driven | **Not removed, but complemented.** The primitive route optimizes the constrained risk directly from raw finite instruments. |
| Boundary optimality was unclear | **Resolved for bounded terminal loss.** The full plan optimum is attained at every feasible finite budget, including the least one. |
| Finite certificates did not characterize optimality | **Resolved for compact finite prefix problems.** Sparse active spectral witnesses and a Bellman slack identity are necessary and sufficient. |
| A natural application was requested | **Improved.** Delayed release gives an exact budget curve and exact live-state threshold, but it remains a purposefully minimal timing model. |
| Computational claims needed stronger content | **Improved but not closed.** The finite witness has an exact backward evaluation; general efficient global synthesis and matching complexity lower bounds remain open. |
| Cost and risk adversaries could be conflated | **Resolved explicitly.** R64 permits separate preparations and gives an exact counterexample to a forced common prior. |
| Hard output width was being treated too much like a convex cost | **Resolved explicitly.** R64 proves a strict hard-width Lagrange gap. |
| A common unknown-model quotient was absent | **Still open.** The predictive quotient remains fixed-law and separately scoped. |
| A recognized difficult external application was absent | **Still open.** The timing theorem is exact but not a resolution of a standard open problem. |
| The editorial packet was too sprawling | **Not resolved.** The current main article is 85 pages, plus a 10-page supplement and retained companion. |

The most important positive change is that the paper no longer relies only on the exactness of a supplied geometric comparator. The primitive constrained problem now has its own compactness, decision-order and finite optimality theory.

---

## 4. Audit of boundary attainment

### 4.1 Common-plan compactness

The full common-plan space is a closed subset of a countable product of intervals, defined by sequence-form flow equalities. Because the action/report tree is countable and finitely branching, this product is compact and metrizable.

The cost-constrained set is not obtained by claiming continuity of full expected cost. Instead, it is defined by all finite reserved constraints

```text
C_{theta,T} + c_* S_{theta,T} <= N
```

for every model and depth. Each such condition depends on finitely many plan coordinates and is closed. Their intersection is therefore compact.

This distinction is mathematically important. Bounded expected stopping cost does not in general give a uniformly vanishing expected remaining-cost tail. R64 does not make that false assertion.

### 4.2 Positive floor and uniform terminal tails

The proof uses the open-call reserve and monotonicity of survival to obtain

```text
C_T + c_* S_T >= c_* [1 + T S_T].
```

Consequently

```text
S_T <= min{1,(N/c_* - 1)/T}.
```

The omitted bounded terminal loss is therefore uniformly at most `L` times this survival mass. This is sufficient for uniform convergence of terminal risk, although it is not sufficient for compactness of full occupation measures or continuity of total expected cost.

The proof correctly keeps those conclusions separate.

### 4.3 Attainment at the least feasible budget

The finite-prefix reserve conditions also imply properness of every point in the compact intersection. Nonnegative partial costs increase to the total cost, so monotone convergence yields the actual budget.

Choosing feasible budgets decreasing to their infimum and using the same compact finite-intersection mechanism proves feasibility at the least finite budget. Thus the boundary optimum is genuinely attained in the unrestricted common-plan class.

The manuscript correctly declines to infer finite-memory attainment at that boundary.

### 4.4 Boundary convergence

The reserved finite values increase with the depth. Restricting a later feasible plan preserves the earlier reserve and cannot increase accumulated nonnegative terminal loss.

Conversely, optimizers along increasing depths have a coordinatewise convergent subsequence. Every fixed earlier reserve survives in the limit, and the uniform bounded-loss tail identifies the limiting full risk. This proves

```text
q_{C,T}(N) -> R_C(N),
q_{m,T}(N) -> R_m(N)
```

from below at every feasible budget.

I found no gap in this argument under the declared common finite-branching and bounded-loss hypotheses.

---

## 5. Audit of the resource-price dual

For a fixed dictionary, behavioral mixing remains inside the same dictionary class. Worst expected cost and worst risk are convex functionals of the mixed plan, so the constrained value `R_C(N)` is convex and nonincreasing on its feasible ray.

An interior supporting line therefore gives the exact scalar dual

```text
R_C(N)
 = sup_{lambda >= 0} inf_P
   { worst-risk(P) + lambda [worst-cost(P)-N] }.
```

The proof correctly distinguishes this scalar resource multiplier from a model prior. The robust cost and risk maxima remain separate.

At a strictly interior budget, a known strict fallback bounds the multiplier by

```text
lambda <= L/(N-kappa).
```

At the least feasible budget the value identity remains exact by approaching from the interior and using right-continuity; a finite multiplier need not attain the supremum. This qualification is necessary and is stated.

The manuscript also correctly refuses to extend convexity to the union over freely optimized width-`m` dictionaries. Mixing two dictionaries can double the set of terminal numerical values.

---

## 6. Audit of the complete stopped-law comparison

### 6.1 The compared object

The outcome space records:

- the complete terminal action--report word;
- the committed value from the actual fixed dictionary; and
- the prospective physical audit outcome.

Thus the law records stopping and raw visible history, not merely the terminal audit marginal. This is the right object for distinguishing the delayed-release controllers later in the paper.

### 6.2 Uniform-TV compactness

At a fixed depth there are finitely many terminal words and output indices. Their law contributions are fixed physical audit measures multiplied by common sequence weights. Total variation of the finite contribution is bounded by the sum of absolute changes in those weights, independently of the model.

The omitted tails of any two budget-feasible plans have uniformly small probability mass by the positive cost floor. Therefore convergence of the finitely many prefix coordinates gives uniform-in-model total-variation convergence of complete stopped laws.

The image of the compact plan set is consequently compact. Linearity in the sequence weights gives convexity.

This is a compactness result for bounded performed probability laws. It is not compactness of occupation measures and does not claim continuity of unbounded expected duration.

### 6.3 Finite-score dual

For equal-mass laws, total variation is the supremum of the positive signed event difference. The manuscript considers the affine functionals

```text
P_theta^P(A) - T_theta(A).
```

If a level below the deficiency were simultaneously attainable against every such functional, the corresponding closed subsets of the compact plan set would have a common point. Their total intersection is empty; compactness reduces this to finitely many tests. Separating the attainable finite test-vector set from a lower orthant gives nonnegative weights. Grouping by model produces:

- a finitely supported model probability; and
- one finite-valued score in `[0,1]` for each supported model.

This proves the reverse inequality in the displayed finite-score formula.

The critical quantifier is retained: the plan minimizing the weighted finite score remains feasible under the budget in **every** model, not only in the support of the finite score prior.

Zero deficiency gives exact realization because the minimum distance is attained.

### 6.4 Same-budget finite-label density

A depth-`T` prefix of an arbitrary feasible plan is completed by the real common fallback on open paths. Coupling the original and completed runs shows that their complete laws differ only on the event that the original plan remains open at that depth.

The completion may exceed the target budget by a controlled amount. Mixing once, before the first physical call, with the strict fallback restores the original budget. This changes the complete law by at most the mixing probability.

The resulting finite-label strategy counts:

- the finite prefix tree;
- the fallback roles; and
- the initial branch role.

No persistent uncounted seed is used.

The density statement is correctly restricted to strictly interior feasible budgets, where the common fallback has strict slack.

---

## 7. Audit of sparse primal--dual witnesses

### 7.1 Finite compact prefix problem

At a fixed horizon and dictionary, the common sequence plans form a finite polytope. Each robust cost or loss constraint is the maximum of a compact family of affine functions indexed by a model and a unit preparation vector.

The strict feasible prefix supplies Slater-type budget slack. A supporting line of the finite budget-value function yields a nonnegative resource multiplier and complementary slackness.

### 7.2 Active gradients and the normal cone

At an optimal plan, directional derivatives of the maxima are maxima of active affine gradients. If the sum of the active risk-gradient hull and the weighted active cost-gradient hull missed the negative normal cone, a feasible tangent direction would strictly decrease the scalarized objective.

Because the feasible set is a polytope, every tangent direction can be realized by a sufficiently short feasible step. The resulting contradiction gives an active convex combination satisfying the stationarity condition.

This is a standard but valid finite-dimensional argument.

### 7.3 The `k_T+1` support bound

In affine plan coordinates of dimension `k_T`, the proof augments each risk gradient by `1` and each cost gradient by `0`. The stationarity vector with total risk mass one lies in their conic hull in dimension `k_T+1`.

Conic dependence elimination reduces the positive support to at most `k_T+1` total risk and cost atoms, preserving:

- stationarity;
- risk mass one;
- activity at the chosen optimum; and
- nonnegativity.

The new total cost multiplier mass need not equal the pre-compression mass; evaluating at the strict fallback supplies the required bound afterward. This point is correctly explained in the supplement.

### 7.4 Pure spectral atoms

Operator constraints are tested against unit vectors. At an active positive semidefinite inequality, zero quadratic form implies annihilation of the vector. Thus the active preparations may be taken pure and are eigenvectors of the active reserved-cost or risk operator.

Cost and risk atoms may lie in different models and different preparations. R64 supplies a concrete two-model example showing that forcing them to share one adversarial prior gives a strict lower dual value.

### 7.5 Sharpness

The one-call simplex example has affine plan dimension `k` and robust loss `max_i x_i`. Its optimal dual requires all `k+1` active risk atoms. This demonstrates sharpness of the support count within a physical finite experiment rather than only in an abstract cone.

I found this sharpness argument correct.

---

## 8. Audit of the common Bellman certificate

For each finite risk or cost atom, the proof propagates the corresponding unnormalized physical state along every raw action--report word. Controller probabilities are not multiplied into these analytic states.

The backward recursion then uses:

- weighted immediate physical costs at pre-call nodes;
- weighted terminal score at productive reports;
- continuation value after rejection; and
- the actual one-call reserve at open depth-`T` leaves.

The common action is minimized against the sum of all atom contributions. Nothing in this recursion reveals the operating model to the runtime controller; the atom states are offline coefficients used to design one common tree.

Subtracting the recursively minimal value from a randomized plan produces nonnegative local row slacks. Sequence-form flow equalities telescope all internal value terms. Equality at the root holds exactly when every positively used alternative has zero local slack.

The manuscript correctly emphasizes that a deterministic tree minimizing the scalarized dual need not satisfy the original individual robust constraints. A complete certificate needs both:

1. primal feasibility in every model; and
2. equality with the sparse dual witness.

---

## 9. Audit of simultaneous expected resources

R64 extends the finite certificate to finitely many additive nonnegative expected resources. The statement requires:

- one resource with a positive per-call floor, to force properness and control survival;
- upper bounds on the other additive one-step costs; and
- one common fallback strictly below all resource budgets simultaneously.

The vector epigraph is closed and convex at the finite level. A supporting hyperplane has nonnegative resource coefficients. Strict joint feasibility forces a positive coefficient on risk, allowing normalization of the risk mass to one.

All active cost gradients, regardless of resource index, are augmented by zero. Risk gradients are augmented by one. The same conic compression therefore yields at most `k_T+1` total atoms, independent of the number of additive expected-resource coordinates.

Completion of a finite optimizer may exceed several budgets by different amounts. Choosing the completed plan with the minimum of the individual safe mixing probabilities restores every budget simultaneously.

The proof correctly states that separate fallbacks, one safe for each resource, are insufficient. The same physically executable fallback must be jointly safe.

Hard output cardinality, program bits and scratch space are not relabeled as additive expected costs. This is an important and correct limitation.

---

## 10. Audit of the hard-width and distinct-witness counterexamples

### 10.1 Separate cost and risk witnesses

The two-model one-call example has robust cost active in model 1 and robust risk active in model 2. The true optimum at budget `3/2` is `1/2`.

Forcing both atom lists to use the same prior gives

```text
3/2 - sqrt(2) < 1/2.
```

The algebra is correct. This example rules out an attractive but invalid reduction of robust constraints to one scalar least-favorable prior.

### 10.2 Hard dictionary width

The width-one value

```text
R_1(N)=min{1/2,2-N}
```

is attained and right-continuous but nonconvex. The scalar Lagrange envelope coincides with the width-two value

```text
R_2(N)=(2-N)/2.
```

At budget `3/2`, the relaxation has gap `1/4`. The randomized implementation producing the envelope uses different terminal values on the cheap and expensive branches and therefore genuinely has width two.

This is a correct warning that an initial behavioral randomization cannot be treated as a free convexification of a hard decoder dictionary.

---

## 11. Audit of the delayed-release timing theorem

### 11.1 Complete-law objective

The physical device has one stateless command and emits the same report on every unit-cost call. The terminal output and audit are constant. Only the stopping time distinguishes strategies.

For target commitment at call `K`, total-variation discrepancy is

```text
1 - Pr(tau=K).
```

This is invisible in the constant output marginal but visible in the complete stopped law. The example therefore genuinely illustrates the value of Theorem 5.3.

### 11.2 Unrestricted budget curve

For `s=Pr(tau=K)`, positivity of the stopping time gives

```text
E tau >= 1 + (K-1)s.
```

Hence the largest possible target mass is

```text
min{1,(N-1)/(K-1)}.
```

It is attained by committing at call one with the remaining probability and otherwise traversing a deterministic length-`K` chain. This proves

```text
Delta_{N,infinity}(K)=(K-N)_+/(K-1).
```

### 11.3 Exact one-live-label curve

With one live label, the halt probability is one constant `p`; the stopping time is geometric. The budget requires `p>=1/N`, and the target mass is

```text
p(1-p)^(K-1).
```

Its maximizer over the feasible interval is `p=1/min{N,K}`, giving the stated exact curve.

### 11.4 Exact attainment threshold

A positive length-`K` live-label path with fewer than `K` labels repeats a state. Pumping the repeated cycle once produces an additional longer stopping path. One of the length-`K` paths has probability at least

```text
s/M^(K-1).
```

The cycle product is at least that path probability, so the pumped path has probability at least

```text
s^2/M^(2K-2).
```

This gives the normalization and mean inequalities in the theorem and forces a strict gap whenever `M<K` and `N>1`.

A deterministic `K`-phase chain attains the unrestricted curve. Therefore `K` live labels are necessary and sufficient. Event stopping can reuse the final live label; state stopping needs one additional terminal label.

The manuscript does not claim a sharp closed form for every intermediate `M`, and the pumping inequality is correctly labeled as a quantitative obstruction rather than an exact curve.

---

## 12. Relation to neighboring theory

R64 credits the main classical tools: convex separation, semi-infinite programming, Carathéodory-type compression, strategic-policy compactness, Blackwell comparison, quantum randomization, reject-option selection, functional representation and phase-type distributions.

The priority discussion should nevertheless be sharpened in one additional direction.

### 12.1 Absorbing MDP occupation measures and finite mixtures

Recent work on absorbing Markov decision processes proves:

- compactness results for occupation measures under uniform absorption and continuity hypotheses;
- characterization of finite extreme occupation measures by deterministic stationary strategies; and
- sufficiency of mixtures of at most `J+1` deterministic stationary occupation measures for constrained total-reward problems with `J` constraints.

More recent geometric work studies faces, affine hulls and minimal finite-mixture order for uniformly absorbing MDP occupation measures.

R64's theorem is not a restatement of those results. Its sparse atoms are **dual model/preparation witnesses**, not a mixture decomposition of the primal controller. Its plan space is a common history-dependent finite tree shared across unknown models, its open-call reserve is explicit, and its same-budget completion is operational. Conversely, the MDP occupation-measure results concern a broader state/action control formalism and give structural primal policy conclusions that R64 does not claim.

This difference should be stated directly. At present the bibliography cites compactness of absorbing MDP occupation measures but does not sufficiently compare the `k_T+1` witness theorem with the recent extreme-point and finite-mixture literature.

### 12.2 Complete stopped-law comparison

The complete-score theorem is appropriately placed in the Blackwell--Le Cam tradition. Its distinctive object is a constrained family of **performed stopped laws** with a protected audit and a uniform physical budget.

The paper should state even more explicitly that:

- it is not a channel randomization theorem with arbitrary ancillary inputs;
- it is conditional on a fixed actual decoder dictionary;
- it does not convert total-variation closeness into control of unbounded duration; and
- its finite-score witnesses are separation witnesses for one budget-feasible law family, not a finite universal basis of all decision problems.

### 12.3 Phase-type timing

Aldous--Shepp and the phase-type literature optimize different variability criteria. R64's exact total-variation target mass and exact autonomous-state threshold are distinct and, as far as I can determine, not immediate corollaries of the cited continuous-time result.

The manuscript correctly avoids an earliest-priority claim for general phase-type timing.

---

## 13. Pipeline and reproducibility assessment

The source-bound local verifier reports:

- 868 source files verified;
- all three R59 report blobs verified;
- 3,313 finite diagnostics;
- 2,537 exact checks;
- 776 floating checks;
- 285 checks added specifically for R64;
- equality of ordinary and optimized Python output;
- two byte-identical builds of the final PDFs and extracted texts; and
- successful native construction of the 85-page main, 10-page supplement and 37-page retained companion.

These are useful source-integrity and finite-arithmetic controls.

However, no GitHub Actions workflow run is presently attached to either:

```text
referee-ready/general-theta-restart-r64-primal-dual-risk-2026-10-16
```

or the mathematical source SHA

```text
7e397f934457894d1dba961cb126e9aef9023dfc.
```

The repository itself correctly says that the local source-bound receipt does not establish hosted success. This absence is not a mathematical proof defect, but the final handoff should not be described as independently hosted verification until an actual run at the relevant SHA is complete and read back.

Finite diagnostics, native compilation, source hashes and repeated PDF identity do not prove the continuum theorems, mathematical novelty or journal significance.

---

## 14. Main reasons the top-four recommendation remains negative

### 14.1 The strongest R64 theorems are an exact closure of a declared finite-branching interface, not a new general invariant

The boundary and complete-law theorems are broad within their interface. Their conceptual inputs remain:

- common finite branching;
- finite legal actions at every node;
- a positive conditional cost floor;
- bounded terminal loss;
- compact decisions; and
- a fixed dictionary for the total-variation comparison.

The paper does not identify an intrinsic invariant characterizing when an arbitrary prepared causal experiment admits the earlier geometric profile or a common finite-resource simulator.

### 14.2 Much of the new proof technology is classical convex analysis

The new mathematical work lies in fitting compact product plans, open-call reserves, performed stopped laws, separate robust witnesses, Bellman slack and same-budget completion together correctly.

That synthesis is useful and nontrivial. Supporting hyperplanes, finite-support semi-infinite duality, conic compression, convex separation and dynamic programming themselves are mature. The paper has not yet shown that their present assembly produces a conceptual consequence of sufficiently broad reach for a top-four general journal.

### 14.3 The natural application remains purpose built

Delayed release is a clean test case with a real complete-law obstruction. It is also designed to isolate a deterministic timing target on a one-command device.

The paper still does not derive a previously unknown optimal finite-resource law for a standard problem in selective prediction, active sensing, robust causal coding, POMDP control or quantum statistical comparison.

### 14.4 Computational closure is incomplete

The Bellman recursion evaluates a supplied finite witness. Semialgebraic elimination terminates on supplied exact primitive data. Neither result is a practically meaningful complexity theorem for global synthesis.

No matching lower region is proved for program description, arithmetic precision, workspace, execution time or minimal simulator state.

### 14.5 The manuscript is not sufficiently concentrated

The current main article is 85 pages and contains many substantial but partly independent lines: primitive risk, compact uncertainty, primal--dual risk, timing memory, geometric task transfer, width defects, zero spectra, synthesis, finite memory, continuation, reset control, detector memory, acquired geometry, realizations, composition and quotient appendices.

The new R64 mathematical center occupies a comparatively small part of this cumulative article. For general-journal evaluation, the paper needs a more concentrated theorem narrative. Historical preservation can remain in the repository without requiring the submitted main article to carry every prior line at equal editorial weight.

### 14.6 The title still exceeds the current intrinsic scope

R64 advances the Foundations programme, but it does not provide a foundation-wide necessary-and-sufficient classification of acquired geometry and causal resource transfer. The title can be retained only with a substantially clearer statement that the present article proves two scoped routes rather than completing the whole programme.

---

## 15. Major revision requests

### 15.1 Rebuild the editorial center around the R64 results

The main paper should be reorganized around four statements:

1. boundary attainment;
2. complete performed-law comparison;
3. sparse primal--dual witnesses and Bellman equality; and
4. the delayed-release memory theorem.

The geometric route should either be summarized as an independently proved companion line or integrated only where it is logically needed. An 85-page accumulation of all previous lines obscures the genuinely new contribution.

### 15.2 Compare the sparse certificate directly with constrained absorbing-MDP geometry

Add theorem-level comparison with:

- extreme occupation measures in absorbing MDPs;
- `J+1` deterministic-policy mixture theorems for constrained total reward; and
- recent face/minimal-mixture results for uniformly absorbing MDPs.

State precisely why R64's `k_T+1` objects are dual physical model/preparation witnesses rather than primal policies, and identify what operational conclusions are new.

### 15.3 Make the performed-law compactness theorem the conceptual headline

The present abstract lists many results. The paper should isolate the exact new compactness mechanism:

```text
positive open-call reserve
+ bounded terminal law
+ fixed dictionary
=> compact budget-feasible performed stopped-law family in uniform TV.
```

Explain why this is different from strategic-measure compactness and from occupation-measure compactness.

### 15.4 Give one substantial external application

Apply the complete-score or sparse-dual theorem to a problem whose optimal finite-resource frontier was not designed into the example. Suitable directions include:

- a standard stochastic shortest-path model with unknown fixed dynamics;
- a selective-prediction problem with paid sequential features;
- a causal coding problem with a hard output alphabet and expected delay;
- a natural quantum stopping/discrimination task; or
- a robust sensing problem with a nontrivial model continuum.

The delayed-release theorem should remain, but it should not carry the entire natural-application burden.

### 15.5 Clarify what remains unknown at the boundary

State together:

- primal full-history attainment holds at the least feasible budget;
- finite-label density currently requires strict interior slack;
- the endpoint multiplier may diverge; and
- finite-memory attainment at the boundary is not proved.

A theorem or counterexample on boundary finite-label attainment would materially sharpen the paper.

### 15.6 Separate fixed-dictionary and optimized-width duality throughout

Every abbreviated statement of the resource-price or complete-score theorem should say “fixed dictionary.” The hard-width counterexample should be referenced immediately whenever a reader might otherwise infer convexity or a Lagrange theorem for optimized width.

### 15.7 Strengthen the timing application only by proving more mathematics

The most natural next step is an exact intermediate-`M` curve or a sharp asymptotic regime for phase-type timing under the expected-call constraint. More packaging around the current pumping estimate would not change the editorial assessment.

### 15.8 State computational claims as certificate evaluation, not global efficiency

The Bellman recursion is an exact evaluator of a finite witness. Real-algebraic elimination is a terminating existence procedure. Neither is a polynomial-time solver for the full robust problem.

A stronger computational claim requires either:

- a complexity upper for a natural finite input class; or
- a nontrivial lower bound for synthesis, certificate size, precision or memory.

### 15.9 Add an actual R64 hosted rebuild or keep the delivery label local

The current source-bound local rebuild is useful and honest. A final publication handoff should append an actual completed workflow run at the R64 source or final head before using language such as “hosted independent verification.”

### 15.10 Reduce the submitted packet

The journal object should distinguish:

- the current theorem article;
- the current technical supplement;
- the retained companion; and
- repository provenance/evidence.

Preservation is valuable, but it should not make the editorial object appear to require a cumulative history archive for comprehension.

---

## 16. Technical comments

1. Every short statement of Theorem 5.1 should retain the positive conditional cost floor and bounded terminal loss.
2. Keep the distinction between the compact plan topology and continuity of total expected cost explicit.
3. The survival bound uses the reserve after the depth-`T` decision; the cutoff is not a declaration of success.
4. State the exact convention for whether the first compulsory call is included in `C_T` whenever the theorem is reused.
5. At the least feasible budget, primal attainment does not imply a finite Lagrange multiplier.
6. `R_C` is convex only for a fixed actual dictionary, including its repeated entries.
7. Optimizing over compact `D^m` gives attainment, not convexity of `R_m`.
8. The complete stopped-law outcome must continue to include raw stopping history and commitment, not only the future audit marginal.
9. The target law family is data on the same outcome space; it is not an executable oracle.
10. In the complete-score formula, repeat that the inner policy satisfies every model budget.
11. Finite-valued score tests suffice by separation; they are not claimed to be a fixed universal finite test list.
12. Total variation controls bounded law scores, not unbounded expected stopping cost.
13. Same-budget finite-label density requires one common fallback with strict slack.
14. The initial completion/fallback mixture must continue to count the surviving branch role.
15. At zero deficiency, exact realization follows from attainment; without compactness only approximate realization would follow.
16. The sparse atoms depend on the horizon, dictionary and chosen optimal plan; they are not one horizon-independent least-favorable prior.
17. `k_T` is the affine dimension after eliminating flow equalities, not the raw number of tree variables.
18. Cost and risk preparations may differ and should not be merged for notational convenience.
19. A dual-minimizing Bellman tree is not automatically primal feasible.
20. Complementary slackness requires activity of every positive atom at the primal optimum.
21. For multiple resources, one jointly strict fallback is essential.
22. Only one resource must be coercive, but every noncoercive resource still needs an additive bounded one-step accounting.
23. Program size, workspace and dictionary width are not additive expected resources by terminology alone.
24. The hard-width counterexample uses a bounded general loss, not a squared-loss realization; retain that distinction.
25. In the timing theorem, `N` is an expected-call budget and may be nonintegral, while `K` and label counts are integers.
26. Event stopping and state stopping have different total-label conventions; retain both in every corollary.
27. The one-live-label law assumes one time-homogeneous reused halt probability and no report that reveals elapsed time.
28. The pumping proof relies on a repeated positive-probability live path; zero-probability paths need no conditioning.
29. A physical clock, phase-valued report or persistent external seed changes the timing interface.
30. The delayed-release terminal marginal is constant; the theorem is about complete laws.
31. The compact primitive spectral witness theorem is finite-dimensional and fixed-horizon; do not export its support count to the full infinite plan without the approximation theorem.
32. Pure preparation witnesses are proof objects, not observer-owned quantum memory.
33. The R59 report is not an external review of R63 or R64; maintain that provenance distinction.
34. The source-bound local rebuild should not be described as an R64 GitHub Actions success.
35. The 3,313 finite checks support algebra and examples but do not certify the continuum compactness and separation arguments.
36. The references should add the recent extreme-occupation-measure and finite-mixture absorbing-MDP results.
37. The current main article should make its page-85 scope separation visible before the theorem inventory.
38. Historical corrected statements should remain clearly distinguished from superseded formulations in retained copies.
39. The fixed-law predictive quotient remains fixed-law; none of the new duality results supplies a common unknown-model quotient.
40. The paper should continue to state that top-four significance and priority remain independent judgments.

---

## 17. Directions that could materially change the top-four assessment

Any one of the following would significantly strengthen the case:

1. **Intrinsic classification:** a near-necessary experiment-level criterion for when the geometric profile or complete-law simulator exists.
2. **Natural hard application:** a new exact finite-resource law for an externally recognized problem rather than an interface designed to exhibit the theorem.
3. **Boundary memory theorem:** finite-label attainment or a sharp obstruction at the least feasible cost.
4. **Nonconvex dictionary theory:** an exact dual or intrinsic relaxation theorem for optimized hard output width.
5. **Efficient synthesis:** a non-exhaustive algorithm with proved complexity for a natural finite input class.
6. **Matched computational resources:** lower bounds coupling persistent labels with program bits, precision, workspace or execution time.
7. **Uniform unknown-model predictive realization:** one executable quotient across a nontrivial changing-support family.
8. **Broader performed-law compactness:** extension beyond common finite branching while preserving the paid stopping and same-budget conclusions.
9. **Sharper timing theory:** the exact intermediate-memory curve or an externally motivated phase-type application.
10. **Direct bridge to constrained MDP geometry:** a theorem showing when the sparse dual witnesses imply, or are implied by, a finite primal policy mixture in an absorbing control model.

These are mathematical routes. Additional preservation maps, diagnostics or review branches would not substitute for them.

---

## 18. Final assessment

R64 is the first revision in this line that supplies a convincing optimality layer for the primitive constrained-risk route. The boundary theorem, complete performed-law comparison, exact fixed-dictionary resource dual, sparse physical witness theorem and Bellman slack identity form a coherent mathematical package. The delayed-release theorem gives a clean exact demonstration that complete stopped laws and persistent temporal state can matter even when terminal outputs are identical.

I did not identify a fatal proof defect in the R64 center under its stated hypotheses. The paper is technically serious and substantially stronger than the last externally reviewed R59 object.

I also do not find a sufficient basis for a positive top-four recommendation. The new theory remains a carefully engineered closure of a declared finite-branching stopped-control interface, built largely from classical compactness, separation, semi-infinite duality and dynamic programming. It has not yet produced a broad intrinsic classification or a major natural external consequence. The cumulative 85-page presentation further obscures the central advance.

**Recommendation:** reject at the top-four general-mathematics level in the present form; favorable consideration by a strong specialist journal after a focused major revision.
