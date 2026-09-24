# Eleventh Independent External Harsh Referee Report

## General Theta Foundations I: Saddle Geometry and the Memory of Causal Experiments — Revision 27

**Author:** Qian Qi  
**Repository:** TrillionniumFoundation/theta-theory  
**Reviewed branch:** revision/general-theta-foundations-i-v27-referee-ready-2026-09-24  
**Frozen reviewed branch head:** 7a659e0a2a41cd91f1f6f4ddc3b01c50a77882e3  
**Recorded native mathematical source commit:** d35c9c907b997d667c23f442dfe830dc07c2c568  
**Reviewed predecessor:** revision 26 at 466bfcdcb8b7d594d3924dbfa82b4c6e29368858  
**Controlling prior report:** tenth external report at 6018ed8f31d758b35eacc48079104e5895fc9591  
**Canonical article:** 51 pages  
**Complete mathematical manuscript:** 229 pages  
**Complete preserved development:** 782 pages  
**Review date:** 24 September 2026  
**Requested standard:** Annals of Mathematics / Inventiones Mathematicae / Journal of the AMS / Acta Mathematica  
**Review type:** independent external-referee-style, pipeline-aware harsh review

# Recommendation

## Reject in the present form at the requested top-four general-mathematics standard

Revision 27 is the strongest version of this manuscript that I have examined, and the reason for my negative recommendation has changed again.

The tenth report asked for synthesis rather than another exact table or another layer of certification. Revision 27 does in fact supply synthesis. The new chain

\[
\text{least-favorable saddle face}
\longrightarrow
\text{support contact and stationarity}
\longrightarrow
\text{compatible positive realization}
\longrightarrow
\text{finite-memory obstruction}
\]

is a real organizing principle. It is not merely an expository relabeling of the v26 results. It produces two new sharp memory statements: five states are necessary and sufficient at the post-training decision cut for the two-preparation marked saddle, and twelve states are necessary and sufficient for the whole execution in the candidate-first forward-serial validation schedule. The proof explicitly excludes arbitrary stochastic encoders and continuations rather than only deterministic compilers.

The second new direction is also substantive. For every preparation number, the paper proves convergence of the unrestricted frozen-validation value to the distance from the target to the nearest candidate experiment, localizes every least-favorable prior near the closest-experiment set, computes that set intrinsically for the marked product family, and obtains a quantitative transport bound for symmetric optimizing priors.

I therefore withdraw the central v26 criticism that the paper contains only several exact islands connected by a framework but no structural theorem linking them. Revision 27 now has such a link.

I have also not found a fatal counterexample to the new v27 core in the source-level audit described below. In particular, the positive-realization normal form, the saddle-contact argument on Bayes ties, the five-generator face obstruction, the twelve-generator forward-serial obstruction, the empirical total-variation preparation bound, and the marked closest-experiment calculation appear internally coherent.

The remaining negative recommendation is narrower. At the level of Annals/Inventiones/JAMS/Acta, I do not think the new structural theorem yet has enough mathematical depth or breadth to support the exceptionally strong editorial claim being made.

The exact loss decomposition in the general saddle-realization theorem is algebraically elementary once the least-favorable prior is fixed. The finite-interface matrix-product normal form belongs to a classical positive-realization lineage. The face-packing lemma is a correct but elementary convex-geometric observation. What is genuinely new-looking is the way contact and stationarity on a Bayes-indifferent saddle face are used to force positive generators. That mechanism is elegant. But the present paper demonstrates its sharp power primarily on one specially engineered marked product family, and one of the two flagship whole-execution numbers — twelve — is tied to a declared validation order and to the idealized exact-support geometry.

The all-preparation theorem has wider scope, but its proof is essentially the empirical total-variation estimator plus minimax duality and compactness. It gives a useful endpoint and localization principle, not a sharp asymptotic saddle theory.

Finally, the repository-wide pipeline remains exactly as the authors now state it: the historical A2 chain, the B4 chain, broad C2, and the eleven-paper aggregate are not consequences of the new finite-state theorem. The new proof dependencies are local and genuine, but they do not yet replace any of the hard Fourier/LLT, LDP, semigroup, common-domain, or phase gates recorded in the Round-Seventeen ledger.

Thus the paper has crossed an important threshold: my objection is no longer “there is no synthesis.” My objection is now “the synthesis is mathematically clean and useful, but its genuinely nonformal force has not yet been shown across a class broad enough, or in a flagship physical theorem intrinsic enough, to meet the requested four-journal standard.”

# 1. Provenance and scope of this review

I reviewed the actual v27 referee-ready branch at the frozen head recorded above. The resource-saddle working branch and the referee-ready branch are identical at this head. The native mathematical source is d35c9c9..., and the referee-ready head adds publication artifacts and the review-ready marker.

The v27 branch is six commits ahead of the reviewed v26 head. Five of those commits lead to the native mathematical source; the final commit materializes the review-ready artifacts.

I read in full the three new mathematical modules that carry the v27 claims:

- saddle-realization.tex;
- exact-memory.tex;
- preparation-localization.tex.

I also re-read the exact marked and two-preparation material on which they depend:

- marked-minimax.tex;
- two-preparation-saddle.tex;
- two-preparation-family.tex.

For interface and physical scope I re-inspected:

- foundations.tex;
- controlled-memory.tex;
- controlled-dual.tex;
- physical-bridge.tex;
- integer-revelation.tex;
- joint-revelation.tex;
- consumer-transfer.tex;
- introduction.tex.

For provenance, scope, and claimed closure I inspected:

- RESPONSE_TO_REFEREE.md;
- PROOF_STATUS.json;
- PIPELINE_STATUS.json;
- RESOURCE_LEDGER.md;
- HISTORY_AUDIT.md;
- LITERATURE_CROSSWALK.md;
- evidence/BUILD_RECEIPT.json;
- the v27 review-ready marker;
- the General Theta Foundations blueprint;
- the original GTF-I implementation note;
- ROUND17_PROOF_DEPENDENCY_LEDGER.md;
- the complete tenth external report on v26.

I also verified the preservation claim at the Git-object level for ten principal v26 modules: foundations, controlled memory, controlled duality, marked minimax, the two exact two-preparation modules, physical bridge, integer revelation, joint revelation, and the downstream consumer have identical blob SHAs in v26 and v27. This is useful provenance. It is not mathematical evidence in favor of the new theorems.

The build receipt records a clean 51-page article, a 229-page complete manuscript, a 782-page preserved development, no undefined references, normal/optimized agreement, and 36 negative-control executions. I treat these records only as reproducibility and assembly evidence. They are not independent proof verification, novelty clearance, or evidence of top-four significance.

# 2. Disposition of the tenth report

The tenth report deliberately listed several possible routes rather than requiring all of them. Revision 27 pursues three: structural constrained realization, a physical sample-memory converse, and a preparation-number law. This is the correct kind of response. I record the disposition carefully so as not to move the goalposts.

## 2.1 Structural constrained control beyond the routing example

**Substantially resolved.**

Proposition 7.1 of the new module (the exact numbering may shift in the assembled paper) gives a finite-interface positive-realization normal form over all wirings of a declared register profile. The important point is not the product formula by itself. The important point is that generators at different cuts must satisfy common one-step continuation identities, so cutwise nonnegative factorizations cannot be spliced freely.

The saddle-realization theorem then intersects this nonconvex realizability set with the uniformly optimal portion of an exposed Bayes face.

This is precisely the kind of synthesis the previous report requested.

However, there is a distinction between “structural theorem” and “deep structural classification.” The displayed resource-loss identity is an exact identity but is nearly tautological after definitions are made. The positive realization formalism is classical in spirit. The nontrivial new content is the contact-constrained use of the saddle face. I credit that contribution, but I do not think the current general theorem by itself reaches the conceptual depth of a top-four main theorem.

## 2.2 A genuine physical sample-memory converse

**Resolved at the decision cut; resolved for one whole-execution schedule; not resolved intrinsically for the entire validation interface.**

Theorem five-memory proves an exact five-state requirement at the post-training decision cut. This is a genuine converse. It is not the old statement that a particular construction happens to use five event labels.

The theorem allows stochastic encoders, arbitrary upstream memory, adaptive training gates and stopping, independent calibration, and stochastic continuation. The lower bound is extracted from the whole optimal saddle face.

This fully answers the “give me a real memory converse” part of the previous report.

The whole-execution theorem is stronger but narrower: twelve is exact only in the candidate-first forward-serial validation class. The authors state this limitation repeatedly and correctly. Reverse-order and interleaved validation are not solved.

Consequently the paper now has an exact scheduled peak, not an intrinsic order-free peak of the original full interface.

That distinction is no longer a hidden defect. It remains an important limitation on the reach of the flagship memory theorem.

## 2.3 A structural law in preparation number

**Meaningfully resolved at the endpoint/localization level.**

The nearest-experiment theorem applies to every continuous compact family on a finite alphabet. It proves

\[
d_*-\sqrt{(d-1)/N}\le U_N\le d_*,
\qquad U_N\uparrow d_*,
\]

and forces every least-favorable prior to localize near the closest-experiment set.

This is a genuine all-N statement. It is conceptually preferable to an isolated N=3 formula.

For the marked family the paper goes further: it computes the closest set, proves a uniform quadratic-growth inequality, and obtains a W2 convergence bound for symmetric least-favorable priors.

I therefore withdraw the v26 criticism that the exact N=2 calculation has no visible relation to larger preparation numbers.

The remaining limitation is that the general all-N theorem is coarse and elementary. It gives an endpoint law, not the finite-N saddle structure, not a recurrence, not a sharp rate, and not a phase diagram.

## 2.4 A foundations conclusion not already encoded in metric hypotheses

**Resolved in a concrete family, not at broad foundational scale.**

The five-state converse and the marked contact-growth inequality are derived from the experimental coefficients and face geometry rather than an assumed covering exponent, small-ball law, or contraction rate.

This directly answers an important part of the previous criticism.

But the truly intrinsic theorem is presently demonstrated on the marked product family. The paper does not yet derive a comparably sharp resource invariant for a broad class of causal experiments.

## 2.5 A major downstream theorem consuming the foundations layer

**Locally resolved; program-wide status unchanged.**

The new five-state and twelve-state results genuinely depend on the exact U2 saddle and the new contact-realization mechanism. The all-N W2 statement genuinely depends on the localization theorem plus the derived marked contact growth.

These are real proof edges.

However, the historical A2, B4, C2, and eleven-paper aggregate remain independent, exactly as PIPELINE_STATUS.json says. No model-specific gate in the Round-Seventeen principal DAG is closed by the new theorem.

I do not require that an independent paper become a dependency of an entire repository before it can be accepted. But because the manuscript repeatedly frames itself as “Foundations,” program-wide necessity cannot be counted as an accomplished source of significance.

# 3. Source-level mathematical checks

## 3.1 The finite-interface positive normal form is correctly typed

The action-before-report constraint is encoded by

\[
M_t^{a,y}\mathbf 1=p_t(a),
\]

with the action row independent of the unread report. This prevents the most dangerous illegal factorization: allowing the current action to depend on its future observation.

The converse construction from matrices to a controller is also standard and correct-looking: divide the row by the action probability when positive and choose an arbitrary legal transition on a zero row.

The treatment of action or report buffers by splitting at charged cuts is necessary and is stated explicitly.

The common continuation-shift identities are an important addition. They prevent the manuscript from treating separately feasible nonnegative factorizations at successive cuts as if they automatically came from one machine.

I find this formulation clean.

## 3.2 The exact resource-loss identity is correct, but mathematically modest

For a least-favorable prior \(\mu_*\),

\[
\ell_*(C)=\int g_\theta(C)d\mu_*(\theta)\le U
\]

for every unrestricted response, while

\[
\min_\theta g_\theta(C)\le\ell_*(C).
\]

Hence

\[
[U-\ell_*(C)]+[\ell_*(C)-\min_\theta g_\theta(C)]
=U-\min_\theta g_\theta(C).
\]

Minimizing over the constrained compact realization set gives the stated identity.

This is correct. It is also why I would not advertise the identity itself as the main mathematical breakthrough. The content lies in what one can do with the two zero-loss conditions.

The exact-attainment criterion is useful: a constrained profile attains U if and only if its response set intersects the uniformly optimal part of the exposed Bayes face.

## 3.3 Contact and stationarity on Bayes ties are legitimately used

For a response in the saddle set, \(g_\theta(C)-U\) is continuous, nonnegative, and has zero integral under the least-favorable prior. It therefore vanishes on the prior support. At an interior differentiable support point it has zero gradient.

This is elementary complementary-slackness geometry, but it is exactly the condition that was missing if one merely chose an arbitrary Bayes best response.

This point matters. In the U2 example, a Bayes-optimal tie rule can use only three events and still fail minimax optimality. The v27 argument correctly refuses to identify “Bayes optimal under a least-favorable prior” with “uniformly minimax” before imposing support contact.

## 3.4 The face-packing lemma is valid and appropriately stochastic

A vertex of a polytope cannot be expressed as a nontrivial convex combination of other points of that polytope. Therefore every required vertex must occur as a generator.

Likewise, if a convex combination lies in a face, every positive-weight generator lies in that face. If the target row in that face is not in the convex hull of already forced vertices lying in the face, an additional generator is needed.

Pairwise disjoint faces force distinct additional generators.

The lemma is elementary, but importantly it does not assume the generators are deterministic histories. They may be arbitrary stochastic continuation channels. This is what allows the lower bound to exclude stochastic encoders rather than merely deterministic residual machines.

## 3.5 The five-state decision converse survives the obvious Bayes-tie loophole

The proof first uses strict coefficient signs to force the three interior count rows. The only Bayes-indifferent coordinates occur at the two extreme report counts.

Let their mark-averaged values be a and b. Contact at the two reflected supporting parameters gives a=b. Stationarity at the support point then gives the unique common value \(t_\gamma\in(0,1)\).

Thus the five mark-averaged rows are

\[
(t,0,1,1),\quad
(1,0,1,1),\quad
(1,1,1,1),\quad
(1,1,0,1),\quad
(1,1,0,t).
\]

Three are distinct cube vertices. The first and last lie in two disjoint faces and are not the already forced vertex in their respective face. The face-packing lemma therefore gives \(K\ge5\).

The lower-bound passage from the original adaptive audit to the common-garbling subfamily is also correctly one-directional: an audit attaining the unrestricted physical upper value must attain that value on the subfamily. Averaging over independent training marks preserves a K-generator factorization.

I do not see the earlier loophole “you only counted the states of a selected deterministic optimizer.”

The matching five-event construction closes the decision-cut count.

## 3.6 The uniform four-state gap is a compactness theorem, not an effective estimate

The relaxed K=4 encoder/decoder spaces are compact and fixed over the compact gamma interval. Their optimum is continuous in gamma. Since the exact five-state theorem gives a pointwise strict deficit, the minimum gap on the interval is positive.

This argument is sound.

But \(\delta_*\) is existential. The manuscript correctly does not pretend otherwise.

This matters for the physical-noise statement. The Gaussian target perturbation tends to zero uniformly, so sufficiently small nonzero noise preserves a strict separation from the four-state class. The paper does not certify the old full noise range from this argument.

I approve the restraint.

## 3.7 The twelve-state forward-serial converse is much stronger than the old compiler count, but schedule-specific

At the cut after the candidate's second report and before its mark, the proof considers actual future-output channels, not only scalar response means.

Eight forced histories give eight distinct deterministic channel vertices. Four extreme-count rows give four genuinely mixed channels lying in four pairwise disjoint faces. Each of these faces contains exactly one of the already forced vertices, and the mixed row is not that vertex because \(0<t<1\).

Therefore four additional generators are required beyond the eight vertices.

This is a legitimate positive-factorization obstruction and gives twelve.

The proof also addresses a subtle potential cheat: an event label need not remain stored after a smaller residual becomes sufficient. The lower bound is phrased on the actual continuation channel, so it does not count stale labels.

The main limitation is explicit in the theorem itself. The geometry is evaluated at a candidate-first cut. If target validation is read first, the target's support restrictions can change the residual geometry. The theorem therefore does not determine the least whole-schedule peak over all legal validation orders.

For the requested top-four standard, this remaining order dependence is substantial. The five-state theorem is intrinsic to the decision cut; the twelve-state theorem is not yet intrinsic to the experiment as a whole.

## 3.8 The nearest-experiment preparation theorem has the stated constant

Let \(\widehat P\) be the empirical law of N training reports and choose the event maximizing \(Q-\widehat P\). Comparing it with an event maximizing \(Q-P_\theta\) loses at most \(2\operatorname{TV}(\widehat P,P_\theta)\).

For a d-atom law,

\[
E\,\operatorname{TV}(\widehat P,P)^2
\le\frac{d-1}{4N}.
\]

Hence

\[
2E\,\operatorname{TV}(\widehat P,P)
\le\sqrt{(d-1)/N}.
\]

This gives the common parameter-independent lower rule.

The upper bound \(U_N\le d_*\) follows by evaluating at a closest candidate parameter. Monotonicity follows by ignoring an extra training observation.

For a least-favorable prior, integrating the common lower rule and using \(U_N\le d_*\) yields the displayed average excess bound. Compactness and continuity then imply support localization of all weak limits.

I find this theorem correct.

I also regard it as conceptually modest. It is a useful minimax corollary of finite-alphabet empirical estimation rather than a new asymptotic decision-theory technology.

## 3.9 The marked closest-experiment calculation appears internally consistent

The common mass of target and candidate reduces to \(\psi(a)+\psi(c)\) with \(a=(1-p)(1-q)\) and \(c=pq\). On the reflected half of the square, the AM-GM reduction correctly pushes the maximum to the diagonal.

The comparison of the relevant piecewise endpoints isolates

\[
s_\gamma=\sqrt{(1+\gamma)/2}
\]

and its reflection.

The claimed value

\[
d_\gamma=2s_\gamma-1-\gamma/2
\]

is consistent with that overlap calculation.

The proof of the uniform quadratic lower bound is deliberately conservative. It combines a linear diagonal deficit with the off-diagonal loss \((p-q)^2/4\), then converts them to Euclidean squared distance. I found no constant-direction error in the displayed \(7/2300\) bound.

## 3.10 The symmetric-prior W2 conclusion is justified, but not sharp asymptotics

The Bayes objective is convex in the prior and invariant under simultaneous complementation. Averaging a least-favorable prior with its reflected image therefore gives a symmetric least-favorable prior.

Pushing such a prior to a nearest point of the two-point contact set gives the equal two-point law by symmetry. The expected squared transport cost is bounded by the second moment of the distance to the contact set. Taking square roots gives the stated \(N^{-1/4}\)-scale W2 bound.

This is correct under the preceding growth inequality.

It is not a statement that \(N^{-1/4}\) is the true rate, nor that finite-N least-favorable priors are two-point. The manuscript states both limitations.

# 4. The central remaining top-four objection: the general theorem is broad where it is formal, and sharp where it is narrow

This is the key editorial issue for me.

Revision 27 now has a unifying sentence that is mathematically meaningful:

> an unrestricted saddle exposes a face; uniform contact restricts the Bayes-indifferent coordinates; finite memory asks whether that restricted face admits a compatible positive realization.

I like this point.

But the strongest general statements and the strongest sharp statements live at different levels.

At the general level:

- every fixed finite causal controller has a positive matrix-product realization;
- exact constrained attainment is intersection with the uniformly optimal saddle set;
- support contact and differentiable stationarity hold;
- a face obstruction gives a state lower bound.

The first item is a finite-state realization principle with classical antecedents. The second is the exact-attainment condition written in the natural geometry. The third is complementary slackness plus first-order optimality. The fourth is elementary convex geometry.

The combination is useful and, to my knowledge from this review, nontrivially deployed. But the paper does not yet provide a general classification of the minimal compatible realization of a saddle face, a computable invariant that equals memory for a broad class, a duality theorem for the nonconvex realization number, or a theorem identifying a large family in which contact data determine memory sharply.

At the sharp level:

- decision width is exactly five;
- forward-serial whole peak is exactly twelve;
- the marked closest set is exactly two points.

These are excellent exact results. But they belong to one marked Bernoulli product family with a specially structured target and a narrow two-preparation saddle.

This asymmetry is the main reason I remain negative at the four-journal level.

The paper has found a bridge. It has not yet shown that the bridge carries enough mathematical traffic.

# 5. The flagship memory theorem is still not an intrinsic whole-experiment complexity theorem

Revision 27 makes a decisive improvement over v26: it turns the number five from “our construction uses five event labels” into “every exact decision-cut implementation needs five states.”

That is an important theorem.

The number twelve is likewise no longer merely an upper bound in the declared forward serial schedule.

However, three distinctions remain.

## 5.1 Decision width versus whole-schedule peak

The exact five-state theorem allows other cuts to be arbitrarily large. It is a theorem about one causal cut.

That is perfectly legitimate, but readers should not conflate it with the minimum total memory of an exact physical audit.

## 5.2 Candidate-first serial versus arbitrary legal validation order

The exact twelve-state theorem assumes candidate validation is completely read before target validation begins.

The original interface does not force that order.

The paper is honest about this, but it means twelve is a property of a scheduled protocol class, not yet of the underlying experiment independently of scheduling.

For a paper whose title foregrounds “the Memory of Causal Experiments,” the order-free question is mathematically natural and currently unresolved.

## 5.3 Ideal exact support versus nonzero physical noise

The twelve-state proof uses exact continuation vertices and faces arising from the ideal marked target's support pattern.

The paper proves persistence of a strict four-state decision gap for sufficiently small positive target perturbation. It does not prove that exact decision width remains five, or that the whole forward-serial optimum remains twelve, for a nonzero-noise physical collision target.

Again, the manuscript does not falsely claim this.

But this is precisely why I would not yet regard the physical side as a complete intrinsic memory theorem.

A top-four strengthening would determine the order-free peak, classify the effect of validation order, or prove a robust version of the realization obstruction under positive physical perturbations with matching constructions.

# 6. The all-preparation theorem is useful synthesis, but it is not yet a deep N-asymptotic saddle theory

The v26 report asked for a law in N rather than another finite-N table. Revision 27 answers in the right direction.

The value endpoint

\[
U_N\to \min_\theta \operatorname{TV}(Q,P_\theta)
\]

is conceptually natural: with many candidate training samples one can identify the candidate experiment well enough to choose a nearly optimal separating event.

The new contribution is to turn the same common rule into a statement about every least-favorable prior.

That is a useful observation.

Still, the current theorem does not explain the exact one- and two-preparation saddles at the level one might hope.

It does not give:

- the support cardinality of a finite-N least-favorable prior;
- a recurrence or variational equation in N;
- a phase transition in the optimal event alphabet;
- a sharp correction to \(d_*\);
- a matching lower asymptotic coefficient;
- a central-limit or local asymptotic description of the prior;
- a classification of when the closest-experiment set controls the finite-N saddle geometry.

For the marked family, the W2 upper rate follows from a coarse \(N^{-1/2}\) value deficit plus quadratic growth. It is a localization bound, not a sharp fluctuation theorem.

I therefore credit this section as synthesis, but not as the theorem that elevates the paper to the requested editorial level.

# 7. The repository pipeline: genuine local proof edges, no fabricated global closure

I reviewed the current pipeline in the context the authors requested.

The Round-Seventeen ledger retains two principal historical chains:

\[
A2\to A3\to A4\to C2\to D1,
\]

and

\[
B2\text{-}GC\to B1\to B2\text{-}MC\to B3\to B4\to C1/C2\to D1,
\]

with A1 recorded as an independent root.

The paper-specific v27 pipeline correctly records the new local edges:

- exact U2 to saddle contact rigidity;
- contact rigidity to exact five-state decision memory;
- contact rigidity plus continuation faces to exact forward-serial peak twelve;
- all-N prior excess to closest-experiment localization;
- marked overlap geometry to intrinsic quadratic growth;
- localization plus growth plus symmetry to W2 convergence.

These are real mathematical dependencies.

Equally important, v27 explicitly records:

- historical A2 independent = true;
- historical B4 aggregate closed = false;
- broad C2 aggregate closed = false;
- eleven-paper closure = false.

This is the correct scientific posture.

The new finite positive-realization theorem does not replace:

- A2's branchwise Fourier/LLT and physical integration-by-parts obligations;
- A3's stopped LDP and entropy obligations;
- A4's global kernel and forced-memory operator obligations;
- B3's Gaussian/Mosco obligations;
- B4's Nisio-resolvent, m-dissipativity, graph-core, and Trotter-Kato obligations;
- C2's weighted strict dual and common-domain form/operator obligations;
- D1's labelled-phase and typed contraction obligations.

Therefore the cumulative repository cannot be used as evidence that GTF-I has already become an indispensable theorem root of the complete program.

This is not a criticism of correctness. It is a restriction on the significance claim.

# 8. Novelty and literature boundaries

The v27 literature discussion is substantially more responsible than the early history of this project.

The manuscript explicitly acknowledges classical positive stochastic realization and invariant-cone ideas through Heller and Vidyasagar, and it separates nonnegative rank from ordinary linear rank with the Gillis–Glineur reference. It does not claim the positive matrix-product representation itself as an invention.

That is important, because the finite-interface normal form should not carry the novelty claim by itself.

The plausible novelty-bearing point is more specific:

> minimax support contact and stationarity can determine Bayes-indifferent response coordinates, and those determined rows can create a sharp positive-realization obstruction to exact causal memory.

That is a sufficiently precise claim to be auditable.

I have not found, in the material reviewed here, a source that obviously subsumes the exact five- and twelve-state conclusions. I also have not performed a complete priority audit across the stochastic-realization, filtered-experiment, finite-memory testing, and imperfect-recall literatures.

The manuscript itself acknowledges that its proof-level comparison with Norberg's filtered-experiment theory remains incomplete.

At an ordinary specialist-journal threshold, that unresolved boundary would not by itself be fatal if the theorem were clearly differentiated.

At the requested top-four threshold, I would want the authors to sharpen the theorem-level novelty statement further: exactly what general realization quantity or principle is new beyond classical positive realization plus standard minimax contact?

# 9. Presentation and theorem hierarchy

Revision 27 is more coherent than v26, but the canonical article has grown from 40 to 51 pages and still carries a large inherited theorem inventory.

The new title is better than the old title because the actual center of gravity is now saddle geometry and memory.

Even so, the paper still has two partially competing identities:

1. a general foundations paper about causal experiments, predictive quotients, transport, and resource accounting;
2. an exact minimax/memory paper centered on one marked family and its saddle face.

The new realization section genuinely connects them, but the article would be stronger if the hierarchy were made even more ruthless.

My preference would be:

- state one general saddle-realization theorem as the conceptual center;
- state the exact five-state and twelve-state results immediately as the principal consequences;
- state the all-N localization theorem as the second consequence;
- demote inherited revelation models, old deterministic precursor constants, and nonessential historical machinery unless they are directly needed for those theorems.

The 782-page preserved development is valuable archival material. It should have essentially zero weight in the editorial argument for the 51-page article.

The best parts of v27 are the new 27-specific proofs, not the preservation volume.

# 10. Specific requests for a future top-four version

I would not ask for all of the following. One sufficiently strong advance could change the assessment.

## 10.1 Give a broad realization-complexity theorem, not only the exact-attainment tautology

The current theorem tells us that exact attainment is intersection of a constrained realization set with a saddle set.

A stronger theorem would identify a nontrivial invariant of the saddle face — for example a causal positive-realization number, a compatible cone complexity, or a dual obstruction — and prove that it equals or sharply controls minimal memory over a broad class of interfaces.

Ideally this invariant would be computable or characterizable without enumerating a chosen finite machine.

Such a theorem would make “saddle geometry determines memory” a general mathematical theory rather than a powerful proof strategy demonstrated on one family.

## 10.2 Determine the whole-schedule memory independently of validation order, or classify the order dependence

The most direct physical strengthening is to solve the minimum peak over all legal validation schedules for the two-preparation marked experiment.

If the optimum differs by order, classify it.

If twelve remains optimal, prove it without the candidate-first assumption.

Either outcome would be mathematically more intrinsic than the current scheduled theorem.

A robust positive-noise version would strengthen the physical interpretation further.

## 10.3 Sharpen the all-N law enough to explain finite-N structure

An exact N=3 table is not what I mean.

A useful advance would be a theorem on the support or scaling of least-favorable priors, a sharp expansion of \(U_N\), a phase law for optimal response geometry, or a class of experiment families in which the limiting contact set controls finite-N saddles in a quantitative way.

The current endpoint/localization theorem is too easy to be the principal asymptotic theorem of a top-four paper.

## 10.4 Establish a theorem-level novelty boundary around positive realization

The manuscript should isolate, in one formal statement, which part is classical realization and which part is new saddle-constrained realization.

A proof-level comparison with the nearest filtered-experiment and finite-memory testing frameworks would substantially strengthen the originality case.

## 10.5 A repository-wide consumer would help, but it is not mandatory

If a future A2/B4/C2 theorem genuinely uses the new realization theorem in place of an independent argument, that would increase the force of “Foundations.”

But I would not make this a condition for acceptance if the intrinsic theorem in GTF-I becomes sufficiently strong.

# 11. What I would not ask the authors to do

To avoid an endless review loop, I explicitly would not ask for:

- more build receipts;
- more preservation pages;
- another finite exact table without a structural consequence;
- another restatement of A0–A5;
- another local metadata dependency;
- another proof that a chosen five-event implementation fits in memory;
- another example where adaptive sensing beats open-loop sensing;
- another explanation that positive realization is not ordinary rank.

Revision 27 has moved beyond those issues.

The next useful step is theorem depth, not infrastructure.

# 12. Editorial assessment by component

### Saddle-face realization theorem

**Assessment:** conceptually useful and correctly organized. The exact loss identity is elementary; the novelty lies in imposing uniform contact on the exposed Bayes face before testing positive realizability.

### Outer positive normal form

**Assessment:** clean and important for avoiding illegal report-dependent actions and incompatible cutwise factorizations. Closely related to classical finite-state stochastic realization ideas; not by itself a top-four novelty claim.

### Face-packing lemma

**Assessment:** correct, reusable, and appropriately stochastic. Mathematically elementary.

### Exact five-state decision memory

**Assessment:** one of the strongest results in the paper. Sharp, nontrivial, and robust against arbitrary stochastic encoding at the declared cut. It is a decision-cut theorem, not a full-profile theorem.

### Exact forward-serial peak twelve

**Assessment:** strong and substantially better than v26. The proof counts continuation channels rather than stale event labels. The candidate-first schedule is essential to the current argument, and arbitrary validation order remains open.

### Uniform four-state gap

**Assessment:** correct compactness consequence. Non-effective. Gives only an existential positive-noise persistence threshold.

### All-N nearest-experiment limit

**Assessment:** correct and useful. Broad but based on an elementary empirical-TV argument; not a sharp asymptotic theory.

### Least-favorable-prior localization

**Assessment:** a good consequence of the common empirical rule. The marked W2 conclusion is clean but rate-wise coarse.

### Intrinsic marked contact geometry

**Assessment:** explicit and well matched to the new theme. A meaningful family-specific theorem derived from the experiment rather than an imposed metric hypothesis.

### Prepared foundations and causal transport

**Assessment:** remain careful and useful. They supply the legal interface in which the new memory theorem is meaningful. Most underlying mechanisms remain classical or conditional as already acknowledged.

### Pipeline integration

**Assessment:** transparent, non-circular, and appropriately modest. New local proof edges are genuine. Major historical A2/B4/C2 chains remain independent.

### Literature positioning

**Assessment:** responsible. The remaining issue is not obvious misattribution but incomplete proof-level delimitation of the exact new general principle.

# 13. Final assessment

Revision 27 deserves substantially more credit than revision 26.

The authors took the previous report's central request seriously. They did not merely add one more certificate or one more special exact value. They found a real mathematical mechanism linking an unrestricted minimax saddle to constrained causal memory.

The key achievement is the recognition that Bayes indifference is not free. If a Bayes coefficient vanishes, a minimax optimizer still has to touch the value at every supporting parameter. Those contact equations, and stationarity at interior support, can determine the tied response. Once determined, the response may require additional positive continuation generators. In the marked two-preparation experiment this mechanism yields an exact five-state decision converse and, after lifting to future-output channels, an exact twelve-state forward-serial converse.

That is a coherent theorem story.

The all-preparation localization result also gives the exact finite-N work a genuine limiting context.

I have not found a fatal mathematical gap in these new arguments during this review.

Nevertheless, my recommendation at the specifically requested Annals/Inventiones/JAMS/Acta level remains negative.

The reason is now concentrated:

- the broad realization theorem is exact but much of its algebra and convex geometry is formal or classical;
- the sharp nonformal consequences are concentrated in one marked product family;
- the exact whole-execution number twelve is schedule-specific and not yet intrinsic to all legal validation orders;
- the positive-noise physical model has only a weaker existential persistence statement, not the same sharp five/twelve classification;
- the all-N theorem is an endpoint/localization bound rather than a sharp saddle asymptotic;
- the main historical A2/B4/C2 pipeline remains mathematically independent.

For a strong specialist venue, I would regard v27 as a serious and potentially publishable paper after ordinary polishing and a careful novelty audit.

For the four general journals named by the authors, I still do not see a theorem of sufficiently broad nonformal reach to justify acceptance.

Thus my recommendation is:

## **Reject in the present form at Annals/Inventiones/JAMS/Acta.**

This rejection should not be read as “the paper still lacks the synthesis requested in the tenth report.” It no longer does.

It should be read as: **the synthesis is now real, but the current general theorem is not yet deep enough where it is broad, and the current deep exact consequences are not yet broad enough where they are sharp.**

That is the remaining top-four obstacle.

---

## Referee checklist

- Latest General Theta Foundations I revision verified as v27.
- Referee-ready and resource-saddle v27 branches verified identical at head 7a659e0a2a41cd91f1f6f4ddc3b01c50a77882e3.
- Native mathematical source commit recorded as d35c9c907b997d667c23f442dfe830dc07c2c568.
- Reviewed predecessor v26 head recorded as 466bfcdcb8b7d594d3924dbfa82b4c6e29368858.
- Controlling tenth review recorded at 6018ed8f31d758b35eacc48079104e5895fc9591.
- Canonical 51-page article inspected.
- saddle-realization.tex inspected in full.
- exact-memory.tex inspected in full.
- preparation-localization.tex inspected in full.
- exact marked one-preparation and two-preparation family sources re-inspected.
- foundations, controlled-memory, controlled-dual, physical bridge, integer revelation, joint revelation, and consumer source context re-inspected.
- Response, proof status, pipeline status, resource ledger, history audit, literature crosswalk, and build receipt inspected.
- General Theta Foundations blueprint and implementation note inspected.
- Round-Seventeen proof-dependency ledger inspected.
- Ten principal inherited v26 mathematical modules verified blob-identical in v27.
- Positive action-before-report normalization checked.
- Common continuation-shift compatibility checked.
- Exact resource-loss identity checked.
- Support-contact and stationarity argument checked.
- Face-packing argument checked for stochastic-generator scope.
- Five-state decision converse checked for Bayes-tie and mark-averaging loopholes.
- Uniform four-state gap checked as a compactness consequence.
- Twelve-state forward-serial argument checked at the continuation-channel level.
- Candidate-first schedule limitation retained.
- Arbitrary validation-order peak not inferred.
- Positive-noise exact five/twelve classification not inferred.
- Finite-alphabet empirical-TV constant in the all-N theorem checked.
- Least-favorable-prior excess/localization deduction checked.
- Marked closest-experiment calculation and quadratic-growth route inspected.
- Symmetric-prior W2 transport argument inspected.
- Build and regression evidence treated as reproducibility evidence only.
- Historical A2 independence retained.
- Historical B4/C2 and eleven-paper closure not inferred.
- No fatal counterexample found in the new v27 mathematical core during this review.
- v26 objection “no structural synthesis theorem” withdrawn.
- v26 objection “no genuine physical memory converse” withdrawn at the decision cut and within the declared forward-serial schedule.
- v26 objection “no structural preparation-number law” withdrawn at the endpoint/localization level.
- Final negative recommendation based on top-four-level depth, breadth, intrinsicness, and novelty reach rather than a claimed elementary proof failure.
