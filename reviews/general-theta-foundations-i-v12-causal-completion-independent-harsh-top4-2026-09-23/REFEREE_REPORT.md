# Independent Harsh Referee Report — General Theta Foundations I, twelfth causal-completion revision

**Manuscript:** *General Theta Foundations I: Causal Experiments, Predictive Quotients, and Resource-Aware Reduction*  
**Author:** Qian Qi  
**Repository:** TrillionniumFoundation/theta-theory  
**Reviewed frozen revision:** revision/general-theta-foundations-i-v12-causal-completion-referee-ready-2026-09-23  
**Reviewed frozen branch HEAD:** a9f8e05640e8bb100178a3216fa6165482ca4676  
**Exact mathematical source checkout recorded by the revision:** 4947abc8b2bdab48b7566df3cf9c1ddcc80b1337  
**PDF/evidence publication commit recorded by the revision:** c7aa49c29801a5b46a4f9c64152db2599acc3f2f  
**Predecessor/fork commit:** b5875ec059e24b328321dcca6d60065cbc3da643  
**Canonical article:** papers/GTF-I-v12-causal-completion/paper.pdf, 92 pages  
**Complete preserved development:** papers/GTF-I-v12-causal-completion/complete-development.pdf, 191 pages  
**Controlling predecessor report:** 8e44610a9826b799f190639cec80c0435f14487c  
**Review date:** 23 September 2026  
**Standard requested:** external-referee standard appropriate to Annals of Mathematics / Inventiones Mathematicae / Journal of the AMS / Acta Mathematica  

**Provenance note.** This is an owner-requested, AI-assisted independent referee-style report. It is not an official report commissioned by any of the named journals.

## Recommendation

**Reject / return in the present form at the requested top-four general-mathematics standard.**

This recommendation should not be read as a claim that the twelfth revision is mathematically unserious. On the contrary, v12 is materially stronger than the tenth revision and, among the General Theta Foundations I revisions I inspected, it makes the clearest attempt to turn the framework into a connected theorem chain rather than a catalogue of interfaces.

I do **not** find a short decisive counterexample to the principal new v12 statements in the source layer I audited: the actual-support exact-cover theorem, the positive risk witness, the summable infinite-horizon compactness/duality theorem, the coherent resource-transport theorem, the finite-rank common-domain memory theorem, the graph-core Galerkin theorem, the width-uniform physical acquisition comparison, or the final certification theorem. Several objections from the v10 report have been answered in substance.

The remaining objection is therefore a more demanding one. After the classical ingredients are subtracted, the present manuscript still does not yet isolate an intrinsic theorem of sufficient novelty, breadth, and inevitability to justify a 92-page top-four article with the title and foundational role claimed. The resource comparison theorem prices a **given** simulator but does not characterize the least resource cost or furnish a resource-deficiency theory. The infinite-horizon theorem still assumes dominated finite-prefix effects and a summable criterion. The exact task theorem is confined to supported restart families with fixed open-loop histories. The hard-sphere consumer is genuinely infinite-dimensional and uses an unbounded generator, but the controls choose observations and do not alter the microscopic flow. The nearest-neighbour priority audit remains explicitly incomplete. And the canonical manuscript has expanded from 64 pages in v10 to 92 pages in v12 rather than resolving the earlier architectural concern by making one theorem visibly dominant.

At a specialist venue, this package could be a serious and potentially publishable contribution after further checking. At Annals / Inventiones / JAMS / Acta scale, I would return it for another structural revision.

---

# 1. Scope of this review

I reviewed the frozen referee snapshot rather than a moving working branch. I inspected in particular:

- GENERAL_THETA_FOUNDATIONS_I_V12_REVIEW_READY.md;
- frontmatter.tex, introduction.tex, and core.tex;
- support-completion.tex;
- infinite-horizon.tex;
- operator-memory.tex;
- resource-certificates.tex;
- the v11 resource-comparison and hard-sphere material incorporated into the v12 core;
- PROOF_LEDGER.md;
- RESPONSE_TO_REFEREE.md;
- LITERATURE_COMPARISON.md;
- HISTORY_AUDIT.md;
- PIPELINE_GRAPH.json;
- the v12 build receipt and remote-build record;
- the controlling v10 independent harsh report and its E10.1–E10.7 requests; and
- the current repository branch landscape relevant to the GTF/A2 dependency claim.

I did not treat successful typesetting, source hashes, finite diagnostics, or branch manifests as proof certificates. The revision itself makes this distinction correctly.

The build record is unusually careful. It binds the mathematical build to source commit 4947abc8b2bdab48b7566df3cf9c1ddcc80b1337, reports 265 inherited and 24 new checked inputs, preserves 607 v11 companion labels, and records 2,285 v12 finite checks with 16 negative-control executions, in addition to rerunning all eleven predecessor diagnostic suites. This is good reproducibility practice. It is not a substitute for proof-level review, and the authors do not present it as one.

I also made a limited external bibliographic check of the closest operator-memory and filtered-experiment antecedents. The arXiv records for Widder–Zimmer–Schilling, *On the generalized Langevin equation and the Mori projection operator technique* (arXiv:2503.20457), and Widder–Schilling, *Generalised Langevin Dynamics: Significance and Limitations of the Projection Operator Formalism* (arXiv:2604.20453), confirm that semigroup well-posedness, finite-rank Mori projection, orthogonal dynamics and domain issues are indeed very close antecedents. The public record for Espen Norberg's 2002 paper *Comparison of Statistical Experiments with Filtered Probability Spaces* also confirms that filtered experiment comparison is a real and directly relevant prior literature. The manuscript itself appropriately says that the full Norberg theorem/proof comparison remains unfinished.

---

# 2. What v12 genuinely fixes

A harsh report should not recycle defects that the authors have actually repaired.

## 2.1 E10.1 is answered in a nontrivial, but still incomplete, way

V10 separated experiment equivalence from finite-register equivalence and left the state-cost multiplier as an implementation caveat. V11 and v12 now promote this into explicit comparison statements.

Theorem 7.6 (thm:v12-transport) gives a prefix-coherent infinite simulator calculus: a simulator of persistent widths K_t and seed bound r composed with a consumer of widths S_t and seed bound q gives widths K_t S_t and seed bound rq. The risk error is the summable weighted prefix error. The public simulator seed is correctly included in the compared joint interface whenever a consumer can read it.

The XOR seed example is exactly the right sanity check. Equality of the unseeded marginal is not enough when the public seed changes the decision content.

Theorem 24.1 then connects this comparison calculus to the positive gap from the exact task theorem. This is a genuine synthesis step: an independently verified comparison bound can certify whether an exact width profile lies on the zero face.

This is substantially better than the v10 situation.

## 2.2 E10.2 is partly answered by a coherent infinite-horizon theorem

Theorem 7.2 does more than let the finite horizon tend to infinity in a scalar value. The policy space is a countable product of compact finite-prefix blocks, the infinite risk map is continuous in C(J) by a uniform summable tail, barycentres are compact in norm, and minimax duality is attained.

The Bernoulli example correctly demonstrates that no common sigma-finite measure need dominate the **complete infinite path laws**, even though every finite prefix lies in the dominated class.

This is a real extension beyond v10.

## 2.3 E10.3 is answered much more convincingly than before

Theorem 4.2 replaces a partition-only, strict-positive-report picture by causally closed compatible covers on the actual support. Overlapping cells are allowed; unsupported successors impose no fictitious constraints; nonunique Bayes-optimal actions are allowed; exact zero excess is unchanged by private or independent public randomization.

The proof mechanism is conceptually clean. Positive supports of randomized retained messages generate compatible cells, and common update rows force successor closure. Conversely a cover gives a deterministic causal machine.

Corollary 4.5 then gives a positive finite witness away from the zero face. The Brier completion recovers the universal marked continuation quotient from a finite pair-separating family in the finite experiment.

This is one of the strongest new pieces in v12.

## 2.4 E10.4 is no longer answered by another finite positive toy model

The operator/microscopic layer is a serious escalation in analytic difficulty.

Theorem 23.1 keeps the domain issue visible: the finite resolved range lies in D(L) intersect D(L*), the orthogonal block is given its actual generator domain, the unresolved initial component appears as forcing, and the full observable reconstruction error is retained.

Theorem 23.3 then uses a graph core for the hard-sphere Koopman generator to obtain strong resolvent and locally time-uniform orbit convergence. Theorem 23.4 transfers the L2 observable approximation into a marked report comparison uniform over every finite register profile and feedback design.

This is a genuine infinite-dimensional, unbounded-generator consumer. It is not the kind of finite-state example criticized in the v10 report.

## 2.5 E10.6 is answered honestly

The pipeline is now explicitly a typed graph rather than a fictitious sequential implication chain. The primary algebraic-geometric A2 line is marked independent_not_consumed. The repository order and the word “Foundations” are no longer offered as proof of a dependency.

That is the correct logical representation.

---

# 3. The exact-cover theorem is strong, but its task class remains narrow

I find Theorem 4.2 mathematically plausible in its stated finite setting.

The key zero-excess argument is robust: the excess is a sum of nonnegative entries. If a message has positive probability under two supported histories, every readout action in its support must be optimal for both. A positive common update row sends every actually supported successor into a single next message support. This produces a compatible causal cover.

The public-seed purification is also correctly quantified for finitely many checkpoints and tasks: condition on the independent seed, remove one null set, and freeze a seed value for which all conditional excesses vanish.

The main issue is not correctness. It is the scope of the object being characterized.

The theorem concerns finite restart tasks with fixed open-loop histories and explicitly supplied conditional loss tables. This is an important exact-compression problem, but it is not yet the same as the general controlled decision problem suggested by the broader language of “causal experiments” and “resource-aware reduction.”

In particular:

1. the task family is externally declared;
2. the restart preparation is fixed and strictly positive on the supported histories;
3. the future control word used to define a restart row is open-loop;
4. exactness concerns the zero face, not the general lossy synthesis geometry; and
5. the universal marked quotient appears only after completing the task family by continuation-event predictions.

The manuscript is admirably explicit about these boundaries. The top-four question is whether the exact-cover theorem can be raised from an exact finite restart characterization to a more intrinsic theorem for endogenous controlled decision families.

At present, the answer is not yet yes.

A particularly valuable next result would characterize the minimal causal state for a nontrivial class of **policy-dependent** task families, or prove a quantitative theorem relating the restart cover numbers to the full common-encoder spectrum away from zero.

---

# 4. The infinite-horizon theorem is real, but not yet a general filtered-experiment theorem

Theorem 7.2 is coherent under its stated hypotheses. I do not see a contradiction in the compactness/minimax proof.

However, the new generality must be described precisely.

The theorem assumes:

- standard-Borel report spaces;
- product-dominated L1 loss effects on **every finite prefix**;
- finite control and decision alphabets at each time;
- fixed finite register widths at each time;
- a compact metric row space J; and
- a summable dominating criterion, in the displayed form sum a_t = 1.

The absence of a single dominating measure on the full infinite path is mathematically meaningful. But it does not address the harder nonclosure phenomena of genuinely nondominated finite-prefix strategic measures, nor does it address average cost or other nonsummable criteria.

The Bernoulli example makes this distinction especially clear. It defeats full-path domination because different parameters have disjoint typical sets, yet every finite prefix remains a very regular dominated finite-dimensional experiment. It is therefore a good example of the theorem's infinite-path reach, but not evidence that the theorem has crossed the hard filtered-strategic-measure boundary identified in the v10 report.

Analytically, the new infinite theorem is still assembled from:

- compact weak-star finite-prefix policy blocks;
- countable product compactness;
- uniform summable tails;
- norm continuity into C(J);
- compactness of probability barycentres; and
- classical minimax.

That is a solid argument. For top-four scale, however, I would want either a theorem that survives a genuinely nondominated finite-prefix/strategic-measure regime, or a much sharper claim that the present paper is a dominated-prefix theory with an infinite-time extension.

The manuscript chooses the latter language in several places, but the title and overall architectural reach still invite the former interpretation.

---

# 5. The main remaining structural defect: resource cost is exogenous, not intrinsic

This is the most important issue in the present revision.

The paper now has a **calculus of priced implementations**, but it still lacks an intrinsic resource comparison theory comparable in conceptual force to classical deficiency.

Theorem 7.6 begins with a simulator already given to the theorem, carrying state cost K_t, seed cost r, and prefix errors epsilon_t. It then proves how these costs compose with a consumer.

That is useful, but the difficult resource question is left outside the theorem:

> Given two causal marked experiments E and F, what is the least state-cost profile K, seed cost r, and error epsilon for which such a simulation exists?

The current theory does not give:

- an intrinsic resource-deficiency quantity;
- a variational or dual characterization of the least K or least epsilon at fixed K;
- a criterion for when K_t = 1 is possible;
- a converse turning risk-body inequalities into a simulator with controlled state cost;
- a completeness theorem for the proposed comparison preorder; or
- a canonical minimal-cost composition invariant.

The manuscript explicitly disclaims a constrained inverse randomization theorem. That is mathematically responsible, but it leaves the central resource quantity exogenous.

The final certification theorem therefore remains a **stability theorem conditional on an independently verified comparison**. It does not solve the resource comparison problem itself.

This matters because the title is *Resource-Aware Reduction*. A top-four foundation in this direction should, in my view, make the resource cost an intrinsic object of the theory, rather than a label carried by an externally supplied simulator.

The most promising next step would be to define something like a cost-indexed causal deficiency
[
  delta_K(E,F)
]
or a state/seed spectrum of deficiencies, prove its composition law, identify its zero set, and derive a decision-theoretic dual characterization under a significant class of experiments. The present product-state theorem would then become the implementation half of a genuinely new invariant.

Without that step, the current “resource-aware comparison” is still closer to a careful implementation calculus than to a new comparison theory.

---

# 6. The finite-seed theorem is useful, but exact public convexification remains idealized

Corollary 7.3 improves the situation substantially. A compact private risk image in C(J) is uniformly equicontinuous; an h-net of the row space and Carathéodory give a finite mixture with at most N(J,h)+1 private policies, and the mixture index can be stored by multiplying the register width.

This has two virtues:

1. the number of policies is independent of truncation horizon at fixed accuracy;
2. the private storage price is explicit.

Still, the exact ideal-public body is the convex hull generated by an arbitrary probability on the full compact policy space K. That public object may contain unbounded information about a policy in an infinite product.

The paper is honest about this and does not call the ideal seed a finite register. Good.

But it means that exact ideal-public duality and finite-resource implementability remain different layers. A stronger resource theory would characterize the approximation rate N(J,h), or replace the metric covering argument by a dimension/entropy theorem intrinsic to the experiment family.

As written, the finite-seed result is a clean compactness corollary rather than a new resource-complexity theorem.

---

# 7. The operator-memory theorem is carefully stated, but its novelty is mainly in the interface

Theorem 23.1 is better written than many informal Mori–Zwanzig derivations because it does not write an undefined exponential of QLQ and does not erase the initial orthogonal component.

The proof via a bounded off-diagonal perturbation is plausible:

- PH is finite-dimensional and lies in D(L) intersect D(L*);
- PL extends boundedly;
- the off-diagonal block is bounded;
- subtracting it block-diagonalizes the generator domain;
- dissipativity gives the orthogonal contraction semigroup; and
- variation of constants yields the Volterra equation.

In the skew-adjoint case the sign B = -C* and K(0) = -C*C are correctly kept.

However, this is precisely the area where recent literature already supplies close semigroup/domain treatments. The external arXiv records for Widder–Zimmer–Schilling and Widder–Schilling confirm that orthogonal dynamics generated by the projected operator, bounded-perturbation arguments, skew-adjoint unitary cases, and domain subtleties are existing results.

The manuscript credits them and does not claim discovery of the Mori identity. That is correct.

Consequently the top-four novelty cannot reside in Theorem 23.1 by itself. It must reside in the connection from the operator approximation to the finite-register decision invariant.

That connection is interesting, but it is still one application of a comparison bound rather than a theorem changing the operator theory itself.

---

# 8. The hard-sphere consumer is genuine, but still passive and model-scoped

Theorem 23.3 and Theorem 23.4 are a substantial improvement over the model-scoped finite examples criticized in v10.

The use of the hard-sphere Koopman generator makes the analytic state space infinite-dimensional and the generator unbounded. The graph-core argument is an appropriate way to justify the Galerkin limit.

The physical comparison proof also addresses a real subtlety: an L2 bound on the initial density need not persist as a bounded posterior density under feedback. The proof avoids this by integrating the first-mismatch contribution under the original marginal and using a uniform sum over the finitely many possible controls. This is the right direction.

But the consumer remains restricted in a way that matters for the advertised downstream force:

> the controls select observations; they do not change the microscopic flow.

Thus the result is a width-uniform theorem for **passive sensing of a fixed hard-sphere dynamics** with Gaussian noisy observables. It is not a theorem about controlled hard-sphere dynamics, not a nonlinear kinetic control theorem, and not a Boltzmann–Grad decision limit.

The manuscript explicitly states these limitations. Again, that honesty is a strength.

The pipeline graph correspondingly marks the v12 B4 edge only as a “verified_microscopic_linear_consumer” and states that the nonlinear kinetic action-sublevel closure remains open.

For a top-four foundation, I would want one of two stronger outcomes:

- a downstream theorem in which the control actually changes the physical dynamics and the resource comparison survives; or
- closure of one of the historically hard A4/B4/C2 targets that the repository originally motivated.

At present, the hard consumer demonstrates that GTF can interact with a nontrivial infinite-dimensional model, but not yet that GTF unlocks a previously inaccessible hard theorem.

---

# 9. The pipeline audit is honest — and therefore weakens the strongest foundational reading

PIPELINE_GRAPH.json is one of the most useful documents in the revision because it prevents rhetorical overclaiming.

It records:

- A1: verified protocol adapter;
- A2: verified protocol adapter, with the primary chain independent and not consumed;
- A3: conditional interface only;
- A4: model-scoped consumer plus an operator-domain v12 edge;
- B1–B3: conditional interfaces;
- B4: model-scoped and microscopic linear consumers, with the nonlinear historical target open;
- C1: model-scoped consumer;
- C2: conditional interface plus operator-domain edge;
- D1: model-scoped consumer.

Most importantly, for **every one of the eleven components**, the field full_historical_target_closed_by_v12 is false.

This is not a criticism of the bookkeeping; it is exactly the correct bookkeeping.

But it means the pipeline does not yet support the strongest interpretation of “General Theta Foundations I” as a theorem from which the eleven-paper research program follows.

The revision now says the program is a typed graph with adapters, consumers and independent lines. That is much more credible. It also changes the editorial story: GTF is a general comparison framework connected to several models, not the mathematical foundation from which the entire program is derived.

There is also a freshness point. The v12 graph freezes the independent primary A2 observation at v127. The current branch survey already contains later A2 branches v128, v129 and v130. This does not invalidate a frozen audit. It does demonstrate that the graph is a historical snapshot rather than a live dependency proof.

The next revision should either:

1. treat the pipeline material as historical motivation and move it largely out of the canonical article; or
2. provide a mechanically refreshed dependency appendix while keeping the theorem-level claims independent of branch chronology.

Repository motion should not be part of the mathematical burden of a top-four paper.

---

# 10. The nearest-neighbour priority audit remains unfinished

This is still a serious editorial blocker at the requested standard.

The manuscript explicitly says that the full theorem/proof text of Norberg's filtered-experiment paper was not obtained and that the original incomplete/partial-machine minimization literature has not been audited to proof-level closure.

That is not a reason to accuse the paper of plagiarism or false attribution. The authors correctly avoid claiming novelty for the cover device itself.

But the remaining claimed novelty is a connection among:

- filtered/causal comparison;
- finite retained state;
- shared/common encoders;
- risk-body convexification;
- exact task covers;
- automata/predictive-state equivalence; and
- resource-costed simulation.

When the novelty is a **connection of established theories**, the nearest-neighbour theorem comparison becomes especially important. One cannot establish top-four originality merely by showing that each ingredient is classical and then asserting that their conjunction is new.

The external bibliographic record confirms that Norberg's paper is indeed about comparison of statistical experiments with filtered probability spaces. Until that paper and the closest finite-memory/common-information/partial-machine theorems are compared statement-by-statement, I would not sign off on the originality claim at Annals / Inventiones / JAMS / Acta level.

E10.5 is therefore not closed.

---

# 11. The article is still too omnibus for its current central theorem

This is the main presentation issue.

The v10 report said that if no single unifying theorem were added, the canonical article should be reduced. V12 does add more synthesis. But it also expands the canonical paper:

- v10 canonical article: 64 pages;
- v11 canonical article: 78 pages;
- v12 canonical article: 92 pages.

The complete development grows to 191 pages.

The v12 core still imports, among other things:

- the decision spectrum;
- finite and conditional duality;
- marked quotients;
- task completion;
- exact synthesis and complexity boundaries;
- common-membership separation;
- controlled minimax;
- a variational principle;
- finite compilation;
- delayed Gaussian exponents;
- projection/precision results;
- several model consumers;
- hard-sphere graph-core analysis;
- operator memory;
- resource certificates;
- predictive trees;
- measure geometry; and
- sequential Gaussian consequences.

This is an impressive research program, but it is not yet one inevitable top-four article.

The new theorem spine is clearer than before:
[
	ext{exact support cover}
	o
	ext{positive gap}
	o
	ext{costed comparison}
	o
	ext{physical approximation}
	o
	ext{certificate}.
]
That could support a strong focused paper.

The problem is that the canonical article still carries many inherited theories whose logical role in that spine is secondary. The result is that the reader must referee a framework, a complexity theory, a stochastic-team compactness theorem, a collection of examples, an operator-memory section, and a hard-sphere approximation theorem in one submission.

For a top-four general journal this breadth raises, rather than lowers, the burden of novelty.

I would strongly encourage a canonical article organized around one of the following:

**Option A: Resource comparison and exact task spectra.**  
Keep the resource-costed comparison, actual-support cover theorem, positive witness, infinite summable risk body, and certificate. Move most model-specific and historical material to companions.

**Option B: Microscopic approximation as a resource theorem.**  
Make the main theorem a genuinely new resource-deficiency invariant, then use hard spheres as the flagship realization. Keep only the minimum finite-state theory needed to state that invariant.

The present 92-page compromise still reads as a carefully curated compendium.

---

# 12. Detailed technical comments

## 12.1 Theorem 4.2: distinguish task exactness from experiment equivalence every time it is summarized

The exact cover theorem is about preserving a declared restart decision family. Only after completing the Brier tests by a separating family of continuation events does one recover the universal marked quotient.

The abstract and introduction are mostly careful about this. The distinction should remain explicit in every high-level summary and table.

## 12.2 Corollary 4.5: the positive gap is a finite-table witness, not a uniform robustness theorem

The constant alpha gamma depends on the least positive restart weight and the least positive entry regret. It can be arbitrarily small under perturbation of the task table or preparation.

This is sufficient for the certification theorem but should not be described as a uniform margin of the model class.

## 12.3 Corollary 4.7: compactness gives existence, not an effective infeasibility witness

The finite-prefix criterion is a clean inverse-limit statement. It gives no computable time at which an infeasible infinite problem must fail.

The manuscript says this. Keep that warning prominent if the result is used algorithmically elsewhere.

## 12.4 Theorem 7.2: the infinite horizon is summable, not average-cost

The phrase “infinite-horizon” is correct, but readers in control will naturally ask about average cost, Cesaro criteria, or invariant strategic measures. None is covered.

I would put “summable infinite-horizon criteria” in the theorem title or immediately adjacent headline.

## 12.5 Corollary 7.3: the finite-seed price hides row-space metric entropy

The policy count is independent of truncation horizon but depends on N(J,h). In high-dimensional or nonparametric row spaces this can be extremely large.

A top-four-strength improvement would give an intrinsic entropy/dimension bound for an important class, not merely the abstract covering number.

## 12.6 Theorem 7.6: define an intrinsic optimal cost profile

The theorem should be viewed as the composition lemma for a future deficiency spectrum. The current K_t and r are inputs. The missing object is the infimum over simulators and its decision-theoretic characterization.

This is the most important mathematical request in this report.

## 12.7 Theorem 23.1: make the source of differentiability explicit

The theorem states that x(t)=P U(t)f is continuously differentiable for every f in H, even though U(t)f need not be differentiable for general f outside D(L).

The proof justifies the statement through the block variation-of-constants formula with bounded A and B, not by differentiating U(t)f directly. I believe the argument is sound, but this subtle point deserves one explicit sentence in the theorem proof because a reader may otherwise suspect an unbounded-generator domain mistake.

## 12.8 Theorem 23.3: cite the precise approximation theorem even though a proof is supplied

The graph-core resolvent-to-semigroup argument is classical. The in-text Gamma/Euler proof is useful, but the paper should still give a precise Trotter–Kato / strong-resolvent reference and state exactly which hypotheses are being re-proved.

This will make the novelty boundary cleaner.

## 12.9 Theorem 23.4: “uniform over all finite width profiles” is correct only because the comparison precedes optimization

This is an important and good point. The manuscript should emphasize that the uniformity is over consumer state widths for a **fixed physical acquisition family**. It is not uniform over an expanding action alphabet, vanishing noise levels, particle number, or a Boltzmann–Grad scaling.

## 12.10 Corollary 23.5: state the row dependence exhaustively

The proof controls row continuity through L1-continuity of the initial density and uniform continuity of bounded row losses. If future versions allow the parameter row to alter the flow, observation functions, noise law, or mark channel, those dependencies will need separate continuity hypotheses.

The current physical setup appears fixed outside the preparation/loss row; say so explicitly in the corollary.

## 12.11 The hard-sphere section should not carry historical kinetic implications by proximity

The manuscript already says that the B4 nonlinear kinetic corrector and Boltzmann–Grad limit are not proved. The section ordering nevertheless places microscopic Koopman convergence near broader kinetic language.

I would keep an explicit boxed or italic scope statement at the start of the section: fixed physical flow, passive observation control, no particle-number uniformity, no kinetic limit.

## 12.12 Build and finite diagnostics should remain outside the theorem narrative

The current separation is mostly good. Do not expand the article with more diagnostic counts. The repository can carry those receipts.

The next advance should be mathematical, not another layer of manifests.

---

# 13. Status of the prior E10.1–E10.7 requests

## E10.1 — Resource-aware comparison theorem

**Partially closed.**

There is now a coherent costed implementation/composition theorem and a certificate theorem. What remains missing is an intrinsic optimal state-cost/deficiency invariant and a converse/dual characterization.

## E10.2 — Broaden nonfinite theory or narrow the claim

**Partially closed.**

The paper reaches infinite time without full-path domination, but remains within dominated finite prefixes and summable criteria. This is materially broader than v10 but still far from arbitrary filtered strategic measures or average cost.

## E10.3 — Connect universal minimality to task-specific compression

**Substantially improved, not fully closed.**

The actual-support cover theorem exactly characterizes zero-excess task-specific widths and completion recovers the universal marked quotient. The remaining gap is endogenous controlled task families and quantitative lossy comparison away from zero.

## E10.4 — Add a genuinely hard historical consumer

**Partially closed.**

The unbounded hard-sphere Koopman/Galerkin/observation consumer is genuinely nontrivial. But it is passive observation of a fixed flow and does not close the historically hard nonlinear kinetic or Sinai spectral targets.

## E10.5 — Close nearest-neighbour theorem comparison

**Open.**

The manuscript itself records the unresolved Norberg and partial-machine source audits.

## E10.6 — Decide A2 and eleven-paper logical status

**Closed as a bookkeeping issue.**

The architecture is now explicitly a typed dependency graph; the primary A2 chain is independent.

This answer is logically correct but reduces the force of the claim that GTF is the foundational theorem source for the entire program.

## E10.7 — Reduce the canonical paper if no single unifying theorem is added

**Not closed.**

A stronger theorem spine has been added, but the canonical article has grown to 92 pages and remains architecturally broad. I do not yet see one theorem whose proof makes all imported sections necessary.

---

# 14. What I would require for a top-four reconsideration

I would not ask for v13 to be another accumulation of local lemmas. The next revision should make a structural choice.

## E12.1 — Define and characterize an intrinsic resource-deficiency spectrum

For marked causal experiments E and F, define the least simulation error at a prescribed persistent-state/seed cost, or equivalently the least state cost at a prescribed error.

Prove nontrivial composition and zero-set properties, and obtain a decision-theoretic dual or converse under a significant class.

The present Theorem 7.6 should become a corollary of that invariant, not the endpoint.

## E12.2 — Push the infinite theory across a genuinely hard boundary

Either:

- allow a significant nondominated finite-prefix / strategic-measure class;
- treat an average-cost or nonsummable criterion with a real compactness/ergodicity issue; or
- explicitly narrow the paper's central claim to dominated finite-prefix summable theory.

The Bernoulli full-path singularity example alone is not enough to settle this.

## E12.3 — Extend exact causal compression beyond fixed open-loop restart tasks

Give a theorem for a meaningful endogenous controlled task family, or derive a quantitative relation between the actual-support cover profile and the lossy common-encoder spectrum.

This would make the task theorem feel intrinsic rather than test-family dependent.

## E12.4 — Make one downstream consumer genuinely transformative

Either let controls alter the microscopic dynamics and carry the comparison through, or close one difficult historical A4/B4/C2 theorem that was previously unavailable.

A passive noisy-observation theorem for a fixed flow is a good application, but not yet enough to demonstrate the advertised downstream force.

## E12.5 — Finish the nearest-neighbour theorem audit

Obtain and compare the full Norberg filtered-experiment result at theorem/proof level.

Do the same for the closest partial-machine compatible-cover/minimization sources, finite-memory control results, and common-information formulations.

The final novelty statement should survive after those exact comparisons.

## E12.6 — Separate frozen pipeline history from mathematical dependency

The current repository has A2 branches beyond the v127 observation frozen into the v12 graph. A frozen graph is fine, but it should not be presented as live program closure.

Keep theorem dependency static and mathematically explicit; keep repository freshness in a separate audit artifact.

## E12.7 — Rebuild the canonical article around one dominant theorem

Do not add another 15–30 pages.

Either focus on resource deficiency + exact spectra + certification, or focus on a resource comparison theorem with one hard physical realization.

The 191-page development can preserve every historical result without forcing the journal article to carry them all.

## E12.8 — State the contribution that remains after all classical ingredients are removed

The paper already credits weak-star compactness, Blackwell/Le Cam comparison, convex minimax, Carathéodory, weighted-automaton equivalence, partial-machine covers, finite-rank Mori projection, graph-core resolvent approximation and hard-sphere flow theory.

The next manuscript should be able to state, in one theorem-sized sentence, what remains that is both new and deep.

At present that remainder is a resource-sensitive connection among these ingredients. I do not yet think the connection has been sharpened into a theorem of top-four scale.

---

# 15. Final assessment

Revision 12 is a serious advance over revision 10.

The actual-support cover theorem is conceptually cleaner than the previous strict-positive task completion. The infinite-time theorem is a genuine coherent extension rather than a finite-horizon relabeling. The public-seed interface issue is handled correctly. The common-domain operator treatment avoids obvious Mori-domain mistakes. The hard-sphere application is genuinely infinite-dimensional. The pipeline audit is much more honest than a sequential-paper narrative.

For those reasons, I would **not** reject v12 on the ground that it lacks substantive mathematics or that its new central statements are obviously false.

I would nevertheless return it at the requested Annals / Inventiones / JAMS / Acta standard for four decisive reasons:

1. **The resource cost is not yet intrinsic.** The theory composes a supplied K-state simulator but does not characterize the least K or give a resource-deficiency duality.
2. **The nonfinite theorem remains analytically restricted.** It uses dominated finite prefixes and summable criteria; the hardest filtered/strategic-measure and average-cost boundaries remain outside.
3. **The downstream force remains model-scoped.** The hard-sphere consumer is real but passive, and no full historical target in the eleven-component graph is marked closed by v12.
4. **Novelty and architecture are not yet settled at top-four scale.** The nearest-neighbour priority audit is unfinished, while the canonical paper has expanded to 92 pages and still contains many mathematically parallel inherited layers.

The next decisive version should therefore be **smaller in architecture and deeper in invariant content**, not larger in inventory.

**Recommendation: reject / return for major structural revision at the requested top-four general-mathematics standard.**
