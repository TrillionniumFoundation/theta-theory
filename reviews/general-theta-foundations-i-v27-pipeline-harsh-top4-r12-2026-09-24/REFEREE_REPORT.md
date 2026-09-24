# External Referee Report — General Theta Foundations I, Revision 27

**Manuscript:** *General Theta Foundations I: Saddle Geometry and the Memory of Causal Experiments*  
**Revision:** 27, dated 24 September 2026  
**Reviewed branch:** `revision/general-theta-foundations-i-v27-referee-ready-2026-09-24`  
**Reviewed head:** `7a659e0a2a41cd91f1f6f4ddc3b01c50a77882e3`  
**Native source commit recorded by the submission:** `d35c9c907b997d667c23f442dfe830dc07c2c568`  
**Previous controlling report answered by this revision:** r10 at `6018ed8f31d758b35eacc48079104e5895fc9591`  
**Current review:** independent pipeline-aware r12 review  
**Standard applied:** Annals of Mathematics / Inventiones Mathematicae / JAMS / Acta Mathematica level.

## 1. Recommendation

**Reject in the present form at the four-journal level.**

This recommendation is not based on a claim that the new five-state or twelve-state proofs are obviously wrong. I re-read the new saddle-realization module, the exact-memory module, the all-preparation localization module, the marked minimax and two-preparation sources, the physical bridge, the response to the referee, the resource ledger, the proof-status record, and the Round-Seventeen dependency ledger. I do not see a short fatal counterexample to the new v27 mathematical core.

The negative recommendation is instead based on the present depth/breadth balance.

Revision 27 finally contains a genuine synthesis mechanism:

1. an unrestricted minimax saddle exposes a Bayes face;
2. support contact and interior stationarity constrain coordinates that the Bayes objective itself leaves indifferent;
3. those constrained rows are tested for compatible positive causal realization;
4. this produces sharp finite-memory lower bounds in the marked two-preparation model.

That is mathematically meaningful and substantially stronger than merely compiling a particular optimal machine.

However, at the level of the four broad general mathematics journals, the present manuscript still has the following structural limitation:

> where the theorem is general, much of the content is formal convex/positive-realization structure; where the conclusions are sharp and nonformal, they are concentrated in one specially engineered marked product family and one declared serial validation order.

The paper now has a real central idea. It has not yet shown that this idea is broad and deep enough to support the editorial claim implicit in the target venue.

## 2. What revision 27 genuinely accomplishes

I want to separate the real progress from the remaining objections.

### 2.1 The paper now has a coherent conceptual center

The new Section on saddle faces and causal realization is the first place in this project where the unrestricted statistical optimum and the finite-memory implementation problem are connected by one reusable theorem chain.

The paper correctly keeps apart:

- the full-history convex response polytope;
- a nonconvex memory-constrained realization class;
- the exposed Bayes face associated with a least-favorable prior;
- the uniformly optimal subset of that face;
- the positive continuation generators needed to implement a member of that subset.

This resolves a conceptual defect that was present in earlier stages of the project: a Bayes-optimal response under one least-favorable prior cannot simply be selected and then treated as if its arbitrary tie-breaking were minimax-relevant.

The distinction is important and the manuscript explains it clearly.

### 2.2 The five-state result is a real converse

Theorem 14.1 is one of the strongest results in the paper.

The proof no longer says only that a five-event construction exists. It argues that every exact two-preparation minimax solution, after imposing support contact and stationarity, must generate five geometrically distinct response requirements. Three are forced vertices and two lie in disjoint proper faces requiring additional positive generators.

Crucially, the lower bound permits randomized encoders and randomized continuations. The argument is therefore not an artifact of counting deterministic histories.

This is a genuine memory lower bound at the declared post-training cut.

### 2.3 The twelve-state result is also substantially stronger than the earlier compiler count

Theorem 14.3 moves from expected event responses to future-output channels and proves a lower bound from eight deterministic continuation vertices plus four further disjoint-face requirements.

This is the correct level at which to formulate a lower bound if one wants to exclude the objection that the machine could compress an event name into a residual statistic.

The candidate-first hypothesis is explicit. That honesty is important.

### 2.4 The all-N section is structurally useful

Theorem 15.1 gives a preparation-number law that is not merely another finite table. The monotone convergence of (U_N) to the closest-experiment total-variation distance, together with localization of every exact least-favorable prior, gives a legitimate asymptotic perspective on the finite-N calculations.

The marked-family contact calculation is also useful: the closest set is identified explicitly, and the paper derives a quadratic growth inequality from the atom probabilities rather than assuming a metric regularity condition.

These results make the paper more coherent.

## 3. The main four-journal obstacle: the broad theorem is still too close to a formal realization criterion

The central general theorem is Theorem 8.2, the saddle-face realization and exact resource-loss theorem.

Its displayed identity is

[
U-V_{mathbf K}
=
min_{Cinmathcal C_{mathbf K}}
left{
U-ell_*(C)
+
ell_*(C)-min_	heta g_	heta(C)
ight}.
]

As the authors correctly acknowledge, the expression inside braces is identically (U-min_	heta g_	heta(C)). The two-term decomposition is useful organizationally because the summands have different interpretations, but algebraically it is tautological once (mu_*) is fixed.

The remaining general content is:

- exact attainment is equivalent to intersection of the constrained realization set with the uniformly optimal saddle set;
- support contact holds on the support of a least-favorable prior;
- differentiable interior support points satisfy stationarity;
- any retained-state cut induces a common positive factorization through continuation channels.

All of this is correct and useful. But at present it is still much closer to a framework theorem than to a deep classification theorem.

The manuscript does not yet identify an intrinsic realization invariant of the saddle geometry that can be computed or characterized for a broad class without returning to a family-specific face argument.

For example, one would like a theorem of the following flavor:

- define a causal positive-realization number attached directly to the saddle set or its continuation cone;
- prove that it equals minimal exact memory, or sharply bounds it, for a substantial class of causal experiments;
- characterize it by a dual object, a cone invariant, a facial dimension, an order-theoretic obstruction, or a finite certificate that does not require ad hoc enumeration of the family-specific rows.

The present paper instead supplies a general normal form and then a very good special-family argument.

That is a real advance, but not yet the kind of broad theorem I would expect to carry a paper at the named four journals.

## 4. The exact memory theorem is still not intrinsic to the whole causal experiment

The paper itself carefully distinguishes three notions:

1. decision width at the post-training cut;
2. whole-schedule peak in the candidate-first serial class;
3. the minimum whole-schedule peak over all legal validation orders.

Only the first two are solved.

This distinction is not cosmetic.

### 4.1 Five states is a cut complexity, not the full memory complexity

Theorem 14.1 proves the exact minimum at one cut while allowing other cuts to be arbitrarily larger.

This is mathematically legitimate and useful.

But the title foregrounds “the Memory of Causal Experiments,” and the natural intrinsic quantity is the minimum resource profile or peak over the complete legal experiment.

The manuscript has not solved that quantity.

### 4.2 Twelve states is schedule-dependent

Theorem 14.3 assumes that the entire candidate validation is read before any target validation report is read.

The original physical interface does not force that order.

The paper explicitly states that reverse-order and interleaved schedules remain open because the ideal target support can alter the available residual geometry.

This is precisely the unresolved issue a top-level reader will notice: the sharp whole-schedule theorem is not yet a property of the experiment alone; it is a property of a selected schedule class.

I would view a classification of validation-order dependence as a major strengthening.

There are several possibilities, all mathematically interesting:

- twelve remains optimal for every legal order;
- another order lowers the peak;
- several order classes have different sharp peaks;
- the relevant invariant is not a single width but a partially ordered profile.

Any one of these outcomes could deepen the paper substantially.

At present, the intrinsic whole-experiment complexity remains open.

## 5. The physical positive-noise result remains qualitatively weaker than the ideal sharp theorem

The paper proves a sharp five-state decision count and a sharp candidate-first peak of twelve for the ideal marked target.

For the positive-noise physical model, the persistence statement is weaker.

Corollary 14.2 obtains a uniform positive four-state gap by compactness. The physical perturbation estimate then implies that the strict separation survives for sufficiently small positive noise.

This is correct.

But the actual threshold depends on an unevaluated (delta_*). The theorem does not show:

- exact decision width five for every sufficiently small nonzero noise;
- exact forward-serial peak twelve for every sufficiently small nonzero noise;
- a robust face-packing classification under perturbation;
- a numerical range of physical noise for which the exact counts remain sharp.

In other words, the physical theorem presently gives a persistence of strict suboptimality for width four, not a robust classification of the exact memory number.

This matters because the ideal target has support zeros that play a visible role in the face structure.

A top-level strengthening would either:

1. prove structural stability of the exact realization number under a quantitative perturbation condition, or
2. compute how the minimal positive-realization number changes once the support becomes full.

That would turn the physical discussion from a continuity corollary into a theorem about robust causal memory.

## 6. The all-preparation theorem is a useful endpoint law, not yet a sharp asymptotic theory

Theorem 15.1 gives

[
d_*-sqrt{rac{|Omega|-1}{N}}
le U_Nle d_*,
]

together with

[
int (d(	heta)-d_*),dmu_N(	heta)
lesssim N^{-1/2}.
]

With quadratic growth this yields an (N^{-1/4})-scale Wasserstein localization bound for symmetric minimizing priors in the marked family.

These statements are useful, and they answer the demand for a law in (N).

But they do not yet explain the fine finite-N saddle structure.

The paper still does not determine, in any broad sense:

- the support size of least-favorable priors as a function of (N);
- whether the two-point contact set controls the exact finite-N support;
- a first nontrivial asymptotic correction to (U_N);
- a matching lower coefficient;
- a local asymptotic normal or moderate-deviation description;
- a phase transition in the optimizer;
- a recursion or variational equation that explains the exact (N=1,2) formulas from the large-N geometry.

The current estimate comes from an empirical total-variation approximation argument plus growth of the distance function. That is a clean general device, but it is not a deep asymptotic saddle theory.

For a specialist paper, this is enough to give context.

For the four journals under consideration, I would want a sharper theorem that reveals new structure rather than only endpoint convergence and localization.

## 7. The pipeline audit is responsible, but it also shows the present theorem is not yet a foundational root of the full program

I examined the Round-Seventeen dependency ledger and the v27 pipeline status.

The historical chains remain:

[
A2	o A3	o A4	o C2	o D1,
]

and

[
B2	ext{-}GC	o B1	o B2	ext{-}MC	o B3	o B4	o C1/C2	o D1,
]

with A1 independent.

Revision 27 adds genuine local dependencies:

- exact (U_2) (	o) saddle contact rigidity;
- contact rigidity (	o) five-state decision converse;
- contact rigidity + output continuation faces (	o) forward-serial twelve-state converse;
- all-N excess (	o) closest-experiment localization;
- marked overlap geometry (	o) quadratic growth;
- localization + growth + symmetry (	o) Wasserstein convergence.

These are real proof edges.

The paper is also commendably explicit that:

- historical A2 remains independent;
- historical B4 aggregate closure is false;
- broad C2 aggregate closure is false;
- the eleven-paper program is not closed by this finite-state theorem.

This transparency should be preserved.

But it also limits the force of the word “Foundations.”

The major downstream obligations in the repository remain analytically independent:

- A2 still requires its branchwise Fourier/LLT and physical integration-by-parts work;
- A3 still requires stopped-LDP and entropy machinery;
- A4 still requires global-kernel and forced-memory operator arguments;
- B3 still requires Gaussian/Mosco analysis;
- B4 still requires Nisio resolvents, m-dissipativity, graph-core arguments, and nonlinear Trotter–Kato;
- C2 still requires weighted strict duality, form/operator compression, and optional-projection analysis;
- D1 still requires labelled-phase and typed contraction arguments.

The current positive-realization theory does not subsume these gates.

That is not a correctness problem.

It is a significance problem if the manuscript is presented as the foundational theorem of the entire pipeline.

At present I would describe GTF-I as a strong local foundations paper for the causal-memory/minimax branch of the project, not as a mathematical root from which the complete repository program follows.

## 8. Novelty boundary: the manuscript is much more careful, but the general theorem still needs a sharper originality statement

The literature crosswalk is improved.

The paper explicitly credits:

- classical stochastic realization and invariant-cone ideas;
- HMM realization theory;
- nonnegative-rank geometry;
- Blackwell comparison;
- convex minimax;
- belief-state dynamic programming;
- adaptive sensing;
- finite-memory testing;
- mixed/behavioral distinctions under imperfect recall.

This is appropriate.

The likely novelty is narrower:

> support contact and stationarity in a minimax saddle can determine Bayes-indifferent coordinates, and those determined coordinates can force additional positive causal generators.

That is a plausible and interesting contribution.

However, the manuscript still needs a theorem-level statement clarifying exactly which part of this mechanism is new relative to the closest positive-realization and filtered-experiment frameworks.

At present the reader is left to infer the novelty from the combination of classical ingredients.

For a top-four journal, I would want the paper to state and defend a general principle that cannot be summarized merely as:

1. take a least-favorable prior;
2. use equality at support points;
3. use first-order stationarity;
4. inspect a positive factorization.

The special marked-family conclusion is nontrivial. The general novelty boundary remains less sharp.

## 9. A specific technical issue of exposition: the theorem hierarchy still overstates the role of the “exact resource loss” identity

I do not regard this as a mathematical error, but I would change the presentation.

Theorem 8.2 combines two very different levels of content:

- a tautological loss decomposition;
- a nontrivial realization/contact criterion.

The first displayed identity receives prominent billing as “exact resource loss,” but the proof immediately notes that the expression equals (U-min_	heta g_	heta(C)).

This risks making the theorem look deeper algebraically than it is.

I recommend separating the statement into:

1. a short proposition giving the decomposition and its interpretation;
2. the actual realization theorem, whose substantive claims are exact attainment, support contact, stationarity, and cut-channel positive factorization.

This would sharpen the manuscript and make the novelty easier to evaluate.

## 10. Another technical issue of scope: compactness gives strict loss, but not an informative quantitative modulus

Several conclusions use the same compactness pattern:

- nonintersection of a compact constrained class with the saddle set implies strict loss;
- pointwise positive gaps over a compact bias interval imply a uniform positive gap.

These are valid.

But the resulting quantities are existential.

For example, the four-state ideal loss (delta_*) is not evaluated.

This has consequences:

- the physical noise threshold is unknown;
- the robustness strength of the memory obstruction is unknown;
- the gap cannot yet be compared to finite-precision implementation errors;
- the theorem does not expose which geometric separation controls the loss.

A stronger general theory would quantify the gap using, for example, distance from the saddle face to the positive-realization variety, a Hoffman-type error bound, a facial angle, or another explicit condition number.

Such a theorem would materially increase the depth of the general result.

## 11. The paper remains overpacked

The canonical article is now 51 pages.

The strongest story is:

1. saddle-constrained positive realization;
2. exact decision memory five;
3. exact candidate-first peak twelve;
4. all-N contact localization.

That is already enough for a substantial paper.

The article also carries a large amount of inherited machinery:

- predictive quotient foundations;
- controlled-memory dynamic programming;
- informative routing;
- exact one-preparation and two-preparation values;
- physical scattering construction;
- integer revelation;
- joint revelation;
- quantitative positivity;
- autonomous finite-memory comparisons;
- transported consumers.

Some of these are necessary to make the interface self-contained.

Others dilute the main result.

For a top-level submission, I would substantially reduce the visible theorem inventory and move more retained development to companion material.

The 782-page preserved development is useful as an archive and reproducibility record, but it should carry essentially no editorial weight.

The paper should be judged by the 51-page canonical theorem chain.

## 12. What would materially change my assessment

I would not require all of the following. One or two sufficiently strong advances could change the paper's level.

### 12.1 Solve the order-free whole-schedule memory problem

Determine the minimum peak over all legal validation schedules for the marked two-preparation experiment.

If different orders produce different sharp peaks, classify them.

This would convert the present schedule-specific theorem into an intrinsic causal complexity result.

### 12.2 Prove a robust exact positive-noise memory classification

Show that the exact five-state or twelve-state number survives on a nontrivial full-support physical neighborhood, with an explicit quantitative criterion.

A theorem explaining when positive-realization numbers are stable under perturbation would be especially valuable.

### 12.3 Replace the framework theorem by a genuine realization-complexity theorem

Introduce an intrinsic invariant of the uniformly optimal saddle set and prove that it controls or equals minimal causal memory over a broad class.

This would make the paper a general theory rather than a framework plus one sharp example.

### 12.4 Develop a sharp large-N saddle asymptotic

Go beyond (U_N	o d_*) and localization.

A first correction term, a support law for least-favorable priors, or a finite-N-to-contact-set classification would substantially deepen the asymptotic part.

### 12.5 Demonstrate a mathematically essential downstream use

A future A2/B4/C2 theorem that genuinely uses the saddle-realization theorem in place of an independent argument would strengthen the claim that this is “Foundations.”

This is not mandatory if the intrinsic theorem becomes strong enough, but at present such a consumer would help.

## 13. What I would not ask for

I would not ask for:

- more build receipts;
- more source hashes;
- more preservation metadata;
- another finite exact value with no structural consequence;
- another regression table;
- another restatement of the same compactness argument;
- another chosen-machine upper bound;
- another example of adaptive sensing outperforming open-loop sensing.

The project has enough infrastructure.

The next step, if the authors continue toward the four-journal level, should be deeper mathematics rather than more packaging.

## 14. Detailed assessment of the principal new components

### Proposition 8.1: outer normal form and compatible continuations

This is clean and useful.

The action-before-report normalization is important and correctly prevents illegal dependence on an unread report. The common one-step shift identities also correctly prevent the mistake of independently factorizing each cut.

The proposition provides the right finite-interface realization language.

Its basic mathematical content is nevertheless close to classical stochastic realization plus explicit causal typing.

### Theorem 8.2: saddle-face realization and exact resource loss

The support-contact and stationarity consequences are useful.

The exact-attainment characterization is the correct bridge between minimax optimality and constrained realization.

The displayed loss decomposition itself is formal.

The theorem is a strong organizing result, but not yet a deep general classification theorem.

### Lemma 8.4: vertex and face packing

Correct and reusable.

It is elementary convex geometry.

Its strength comes from applying it to the right forced continuation rows.

### Theorem 14.1: exact decision memory five

A strong theorem.

The use of contact and stationarity to determine the Bayes-indifferent extreme rows is the key nontrivial step.

The stochastic-generator lower bound is appropriately stronger than deterministic state counting.

The scope is exactly the post-training decision cut.

### Corollary 14.2: strict four-state gap

Correct by compactness once Theorem 14.1 is established.

Non-effective.

The physical persistence conclusion is therefore existential.

### Theorem 14.3: sharp forward serial peak twelve

Also a strong theorem.

The lower bound is formulated at the level of future-output channels, which is the right way to avoid overcounting event labels.

The unresolved validation-order dependence remains the main limitation.

### Theorem 15.1: nearest-experiment limit and least-favorable-prior localization

Broad and useful.

The empirical-TV ingredient is elementary.

The localization conclusion is a good synthesis.

Not yet a sharp finite-N asymptotic theory.

### Theorem 15.2 and Corollary 15.3: marked contact geometry and prior limit

Clean family-specific results.

The explicit quadratic growth estimate is valuable.

The Wasserstein rate is a consequence of a coarse excess bound and should not be oversold as an asymptotic fluctuation theorem.

## 15. Pipeline verdict

I regard the repository-level accounting in v27 as scientifically responsible.

The manuscript does not falsely claim that finite-state positive realization closes the operator, LDP, semigroup, or phase-analysis obligations elsewhere in the project.

The local dependency edges are real.

The broad historical closure claims are withheld.

This is exactly the correct posture.

However, the same pipeline audit shows that the current paper's reach is local relative to the full program.

That weakens, rather than strengthens, the argument for four-journal foundational status.

## 16. Final verdict

Revision 27 is the strongest version of General Theta Foundations I that I have seen in this repository lineage.

The project has crossed an important threshold: it now contains a theorem mechanism that genuinely explains why an unrestricted minimax saddle can force causal memory.

The five-state result is not merely a compiler count.

The twelve-state candidate-first result is not merely an implementation profile.

The least-favorable-prior localization is not merely another finite-N table.

Those are substantial improvements.

Nevertheless, at the level of Annals / Inventiones / JAMS / Acta, I remain negative.

The remaining obstacle is no longer “the paper is only infrastructure.”

The obstacle is more precise:

> the paper's broad statements are not yet mathematically deep enough where they are general, while its deepest sharp statements are not yet intrinsic and broad enough where they are exact.

In particular:

- the general realization theorem remains framework-level;
- the exact full peak is schedule-specific;
- sharp robustness under nonzero physical noise is unresolved;
- the large-N theorem is endpoint/localization rather than a sharp saddle asymptotic;
- the major A2/B4/C2 pipeline remains mathematically independent;
- the novelty boundary of the general principle is still not isolated at theorem level.

Accordingly:

## **Recommendation: Reject in the present form at the four-journal level.**

I would, however, regard the current mathematical core as potentially suitable for a strong specialist venue after a careful condensation and novelty audit.

---

## Referee checklist

- Repository confirmed as `TrillionniumFoundation/theta-theory`.
- Latest General Theta Foundations I revision branch verified as v27; no v28/v29 branch found in the connected repository at review time.
- Reviewed `revision/general-theta-foundations-i-v27-referee-ready-2026-09-24`.
- Reviewed head `7a659e0a2a41cd91f1f6f4ddc3b01c50a77882e3`.
- Compared v26 and v27; v27 is six commits ahead of the v26 referee-ready base and contains the new saddle-memory and all-N material.
- Read the 51-page canonical article source.
- Read `saddle-realization.tex`.
- Read `exact-memory.tex`.
- Read `preparation-localization.tex`.
- Re-inspected marked minimax, two-preparation, controlled-memory, and physical-bridge context.
- Read the v27 response to the controlling r10 referee report.
- Read `PROOF_STATUS.json`, `PIPELINE_STATUS.json`, `RESOURCE_LEDGER.md`, `HISTORY_AUDIT.md`, and `LITERATURE_CROSSWALK.md`.
- Read the Round-Seventeen proof-dependency ledger.
- Checked that v27 itself does not claim all-validation-order peak optimality.
- Checked that v27 itself does not claim a numerical four-state gap.
- Checked that v27 itself does not claim sharp large-N rates.
- Checked that v27 itself does not claim historical B4/C2 or eleven-paper closure.
- No short fatal counterexample found to the new five-state decision converse.
- No short fatal counterexample found to the candidate-first twelve-state continuation-channel converse.
- Four-state persistence under physical noise remains existential because the ideal gap is not quantified.
- Whole-schedule peak over arbitrary validation orders remains open.
- Broad positive-realization framework remains mathematically distinct from the independent A2/B4/C2 analytical gates.
- Final negative recommendation is based on top-four depth, breadth, intrinsicness, quantitative strength, and novelty reach, not on an asserted elementary proof failure.
