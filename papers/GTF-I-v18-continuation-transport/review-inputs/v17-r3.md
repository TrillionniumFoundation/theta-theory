# Third Independent External Harsh Referee Report

## General Theta Foundations I: Adaptive Testing and Collision-Sensitive Comparison — Revision v17

**Author:** Qian Qi  
**Repository:** TrillionniumFoundation/theta-theory  
**Reviewed branch:** revision/general-theta-foundations-i-v17-intrinsic-adaptive-testing-referee-ready-2026-09-23  
**Frozen referee-base commit:** e5a81e26e9a1b366f5863b00e09d62512f32f5ea  
**Canonical mathematical source identity:** f93ab1a6c8c5255a3398f1884c5af05d65ced73a  
**Final PDF/evidence publication identity:** 978800e2f1d8678291d7a4b1f0dcc4396235f8b5  
**Canonical article:** 59 pages  
**Complete preserved development:** 256 pages  
**Review date:** 23 September 2026  
**Requested venue standard:** Annals of Mathematics / Inventiones Mathematicae / Journal of the AMS / Acta Mathematica  
**Review type:** third independent, external-referee-style, pipeline-aware harsh review

**Provenance and scope.** This is an owner-requested, AI-assisted external-referee-style assessment, not a journal-commissioned report. I reviewed the frozen v17 canonical source architecture, the new adaptive-testing, collision-resource-gap, and optional-stability theorem groups, the proof ledger, response, literature and history audits, the dependency appendix, the v16-to-v17 delta, the two existing v17 harsh reports, and the repository-level eleven-component pipeline material exposed by the revision. I also rechecked selected exact inequalities in the collision proof. Build receipts, diagnostics and repository manifests are treated as reproducibility evidence only; they do not substitute for mathematical proof.

---

# Recommendation

## Reject in the present form at the requested top-four general-mathematics standard

The paper has improved substantially and, in my reading, the principal issue is no longer a simple correctness failure.

I do not find an obvious one-line counterexample to the new headline theorems. The adaptive testing representation is mathematically coherent under its stated information convention; the Bernstein/binomial approximation argument is transparent; the explicit nonlinear certificate is exact; the two-sphere construction genuinely creates the observed transverse signal through collision and loses it when the collision is removed; and the optional-projection estimate supplies a real whole-process stability statement rather than a finite-dimensional convergence slogan.

The paper therefore deserves credit for having moved beyond several weaknesses of earlier revisions.

Nevertheless, at the requested Annals/Inventiones/JAMS/Acta level, the manuscript still falls short for a deeper reason:

> the paper does not yet contain a theorem whose structural force justifies the title and role “General Theta Foundations I.”

The three new v17 headline packages remain parallel:

1. a revealed-candidate adaptive-test representation and an approximation hierarchy on a compact nonconvex behavior image;
2. a carefully engineered two-particle, one-collision physical realization of a finite private/hidden/visible separation;
3. a total-variation/Bayes/maximal-inequality stability theorem for posterior processes under a common latent marginal.

Each is useful. None currently generates the others. None currently classifies the finite-memory resource geometry. None currently survives the hard particle-number or kinetic scaling gates that the repository itself identifies downstream. None currently establishes the historical C2 program. And the repository's primary A2 chain is explicitly recorded as independent rather than as a consumer of the purported first foundational layer.

This is the decisive top-four problem.

The manuscript is now a serious resource-comparison and certification interface. It is not yet a demonstrated first-principles foundation for the eleven-paper program.

I would not recommend another top-four round after local edits. The next revision should add one genuinely organizing theorem, not another exact example, another certificate, or another repository ledger.

---

# 1. What is genuinely improved in v17

The revision answers a number of predecessor objections in a mathematically meaningful way.

- The fixed private behavior image is not silently convexified.
- The new adaptive-test class is independent of the simulator's private randomization.
- The paper distinguishes revealed candidate behavior from hidden runtime information.
- The size bound is expressed in observable affine behavior dimension rather than raw stochastic-row dimension.
- Strict positivity certificates are separated from equality-at-the-boundary questions.
- The physical construction now makes collision mechanics essential to the observed informative signal.
- Private, hidden-selector and visible-selector signatures are separated in one physical model.
- The no-collision regime gives an excellent control experiment.
- The effective-presentation quantifiers are stated uniformly.
- The canonical article is a self-contained source tree.
- The optional-projection result controls an entire posterior process.
- The latent-preserving coupling is correctly identified as a proof device, not as an executable causal simulator.
- The paper does not falsely declare B4 or the full historical C2 program closed.
- The literature section is substantially more careful about classical positivity, minimax, and filtered comparison.

These are not cosmetic gains. They should be preserved.

The rejection below should therefore not be read as “v17 did not answer v16.” It did answer much of v16. The remaining bar is now a structural one.

---

# 2. The first headline theorem is a representation theorem, not yet a causal-resource duality theory

The paper defines, for a compact behavior image \(B\) and affine event discrepancies \(f_i\),

\[
F(b)=\max_i f_i(b), \qquad \delta=\min_{b\in B}F(b).
\]

An adaptive test is a continuous map

\[
\kappa:B\to\Delta_m,
\]

chosen before the candidate but evaluated at the fully revealed candidate behavior \(b\). Its score is

\[
G(b,\kappa)=\sum_i\kappa_i(b)f_i(b).
\]

Theorem v17-dual proves

\[
\delta
=
\sup_{\kappa\in C(B,\Delta_m)}
\min_{b\in B}G(b,\kappa)
=
\min_{\mu\in\mathcal P(B)}
\sup_{\kappa}
\int_B G(b,\kappa)\,d\mu(b).
\]

The theorem is correct under the stated rules. But the proof reveals why its structural content is limited.

The continuous tester can pre-program an approximate pointwise argmax of the finite family \(f_i\). A partition of unity on the open sets

\[
U_i=\{b:f_i(b)>F(b)-\eta\}
\]

gives a continuous \(\kappa\) with

\[
F(b)-\eta<G(b,\kappa)\le F(b).
\]

The measure side then satisfies

\[
\sup_\kappa\int G\,d\mu
=
\int F\,d\mu,
\]

and minimization over \(\mu\) collapses to a point mass at a minimizer of \(F\).

Thus the “duality” is not exposing a hidden polar object of finite-memory causal behavior. It is encoding pointwise selection after the candidate law is revealed.

That distinction matters greatly.

A genuine resource-sensitive duality theorem would make the dual class itself carry nontrivial operational restrictions. Examples include:

- tester-side finite memory;
- partial rather than full law revelation;
- causal continuation constraints;
- a common-information filtration restriction;
- a resource gauge or norm whose polar has an operational meaning;
- a separation theorem in which both primal and dual obey matched information budgets;
- a continuation-state or predictive-state invariant that determines the separating class.

The current theorem is better described as a **revealed-behavior adaptive-test representation**.

I strongly recommend either proving a truly constrained causal/resource duality or renaming the result so that the partition-of-unity mechanism is not asked to carry more conceptual weight than it has.

---

# 3. The behavior-dimension hierarchy is useful, but “intrinsic” remains relative and one-sided

Theorem v17-degree is, in my view, the strongest new finite quantitative statement.

After quotienting directions invisible to the discrepancy family, the paper works in observable affine dimension \(a\) with event-norm diameter \(R\). Tensor Bernstein tests give

\[
0\le \delta-d_n\le \frac{4Ra}{\sqrt n},
\]

with at most

\[
(n+1)^a
\]

occupied coefficients, and the moment-side minimizer can be supported on at most

\[
(n+2)^a
\]

points.

The proof is clean. The binomial smoothing estimate is the expected one, and the moment support reduction is a direct finite-dimensional Carathéodory argument.

This is a real improvement over a row-coordinate hierarchy.

However, the theorem is still not an intrinsic complexity theory of finite-memory comparison.

The word “intrinsic” currently means intrinsic to the chosen observable discrepancy image after quotienting directions annihilated by the chosen event family. It does not mean invariant under all equivalent task descriptions, all mark refinements, all information signatures, or all presentations of the same operational resource class.

The manuscript itself correctly states what is missing:

- no bit-complexity bound for finding the chart;
- no complexity bound for describing the feasible nonconvex set;
- no algorithmic bound for minimizing the test score on that set;
- no coefficient-height bound for the resulting rational separator;
- no lower bound on required degree;
- no lower bound on support;
- no sharpness result;
- no characterization of minimal degree by causal-state complexity;
- no width/horizon dichotomy;
- no polynomial-time claim.

At a normal specialist-journal level, this can be a strong theorem. At a top-four “Foundations I” level, it is one half of the theorem one wants.

The missing half is a lower-bound or classification theorem.

For example:

1. prove that the \(\varepsilon^{-2}\) degree dependence is unavoidable in a natural family;
2. prove exponential dependence on behavior dimension is unavoidable;
3. relate minimal separating degree to private-state or continuation-state complexity;
4. classify behavior images with uniformly bounded-degree separators;
5. establish a complexity dichotomy in horizon or width;
6. prove a canonical finite-state invariant controlling both upper and lower test complexity.

Without such a theorem, the hierarchy remains a good approximation scheme rather than a new structural theory.

---

# 4. The chart-effectiveness statement needs a more explicit algorithmic theorem if it is to carry computational significance

Lemma v17-chart states that for a rational polynomial image of a product of simplexes, a rational bounded chart can be found effectively.

The proof invokes density and real quantifier elimination.

This is plausible, but the current statement compresses several distinct tasks:

- determining the observable quotient dimension;
- representing the quotient rationally;
- locating an affine basis;
- deciding that a candidate determinant exceeds half the true maximum determinant;
- controlling the relation between exact real-algebraic data and rational samples;
- transporting the resulting chart into the later rational certificate procedure.

The manuscript explicitly disclaims bit complexity, which is appropriate.

But if “effective” is to be more than a computability label, the authors should state a separate algorithmic proposition with exact input and output encodings.

In particular, the paper should say whether the dimension \(a\) is part of the input or computed, how the annihilator quotient is represented, and how the determinant comparison is reduced to a first-order real formula.

This is not a fatal proof objection. It is a place where the current computational language is stronger than the operational detail supplied.

---

# 5. The exact nonlinear witness is excellent as an example, but it does not resolve the structural gap

Proposition v17-smallcertificate is one of the cleanest parts of the manuscript.

For the width-one two-report example, the paper gives three behavior-dependent weights built from

\[
J(t)=3t^2-2t^3,
\]

then transforms the score using

\[
a=(p+q-1)^2,\qquad b=(p-q)^2,
\]

obtains a nonnegative derivative decomposition, and finishes with an exact positive degree-16 Bernstein coefficient list.

This is unusually transparent and reproducible.

It convincingly demonstrates that constant affine tests can miss a positive private deficiency that a nonlinear revealed-behavior test detects.

The problem is significance, not correctness.

The example does not yet answer:

- what the minimal degree is;
- whether the cubic choice is in any sense canonical;
- whether there is a general finite-memory analogue;
- whether small certificates characterize any operational class;
- whether the coefficient height can be controlled intrinsically;
- whether a matching lower bound exists.

Keep the example. Do not ask it to serve as evidence for a general complexity theory.

---

# 6. The collision section is a genuine physical improvement, but the information separation is still planted at preparation level

The new hard-sphere construction is substantially more convincing than the earlier collective benchmark.

The preparation encodes:

- \(B\) in the sign of the transverse impact orientation;
- \(W\) in the sign of the longitudinal center-of-mass velocity.

The collision then creates a tagged transverse velocity whose sign reveals \(B\). The no-collision regime removes that signal.

This is a real interaction/no-interaction contrast.

I independently rechecked the decisive rational lower estimate in the scattering proof:

\[
-\frac{3}{200}
+
\frac{1443}{1000}\frac{87}{220}
=
\frac{122241}{220000}
>
\frac12.
\]

The Gaussian tail transfer used to get the \(1/300\) physical discrepancy is also consistent with the stated bounds.

The resulting private/hidden/visible separation is therefore not merely nominal.

However, the paper should be even more explicit about where the resource gap originates.

The \(B\)-\(W\) correlation is already present in the preparation law. The collision does not create the correlation. It converts the pre-existing \(B\) variable into an observable collision-generated signal.

Likewise, the hidden-selector advantage is fundamentally the finite-information fact that a persistent hidden bit can correlate two emissions without being charged to the width-one private register.

The mechanics physically realize the finite marked experiment. They do not generate a new many-body memory principle.

This distinction is central for top-four significance.

The theorem has:

- two labeled spheres;
- one isolated nongrazing collision;
- no recollision graph;
- no many-particle limit;
- no particle-number-uniform estimate;
- no Boltzmann-Grad limit;
- no nonlinear kinetic semigroup;
- no large-deviation action;
- no hierarchy corrector;
- no mechanical feedback force.

The paper says most of this correctly.

My recommendation is not to delete the theorem. It is to stop using it as evidence that the hard kinetic part of the program is close to closure.

It is an excellent finite physical realization theorem.

It is not yet a cross-scale theorem.

---

# 7. The no-collision control is one of the strongest conceptual points and should be elevated

For \(d\le 2/5\), the detector remains identically zero and the target reports are pure independent noise. All three deficiencies then vanish.

This is a very good control experiment.

It directly demonstrates that the informative report is collision-created rather than a disguised conserved-mode readout.

I would move this contrast closer to the principal theorem statement and figure/table summary.

The current paper has many technical modules. The no-collision control is one of the few places where the conceptual mechanism is immediately visible.

It should carry more of the exposition.

---

# 8. The optional-projection theorem is mathematically useful, but its hypotheses are much stronger than the historical C2 problem

Theorem v17-optional assumes:

- equivalent joint laws \(P,Q\);
- the same latent marginal;
- a common canonical observation path space;
- bounded latent observables for the basic estimate.

The proof uses:

- the density martingale;
- Bayes' formula;
- weak \(L^1\) maximal inequalities;
- latent-conditional maximal coupling.

The resulting bound

\[
E_Q\sup_{t\le T}|M_t^P-M_t^Q|^2
\le 80\,\|P-Q\|_{\rm TV}
\]

and the latent-preserving coupled bound with constant \(84\) are legitimate and useful.

The physical specialization then keeps one fixed invariant hard-sphere flow and one fixed latent initial state, while changing the observation function from \(h\) to \(h_n\). Girsanov/KL and Pinsker convert \(L^2(\mu)\) approximation of \(h\) into joint total-variation convergence.

This closes a real scoped problem.

But it is not the historical C2 problem in full generality.

The hard C2 regime concerns some combination of:

- changing microscopic processes;
- changing likelihood processes;
- changing coarse filtrations;
- stochastic-exponential limits;
- Girsanov limits;
- BSDE limits;
- strict duality;
- covariant form response;
- memory response;
- rigidity.

The v17 theorem keeps the latent state space and microscopic flow fixed and varies only the observation map in its concrete specialization.

Therefore the phrase “microscopic changing-filtration limit” is technically defensible but potentially misleading.

I recommend language such as:

> whole-process posterior convergence for a fixed microscopic flow under varying observation maps.

That is already a good theorem.

There is no need to let the abstract suggest the full historical C2 bridge has been crossed.

---

# 9. A deeper limitation: total variation is doing nearly all of the conditional-law work

The optional-projection theorem is presented as a downstream conditional-law input.

But the actual mechanism is that small joint total variation controls posterior martingales.

This has two implications.

First, the theorem is robust and portable.

Second, its difficulty is located upstream: one must actually prove small joint total variation in the microscopic approximation under consideration.

In the Gaussian-observation specialization, that is supplied by a very favorable setup:

- deterministic bounded drifts conditional on the same latent state;
- common noise variance;
- fixed time horizon;
- a common invariant reference measure;
- \(L^2\) approximation of the observation function.

This is far easier than the historical kinetic and changing-path situations.

So the theorem should be positioned as a **TV-to-posterior stability principle**, with one concrete microscopic verification, rather than as a general solution to changing-filtration limits.

Again, the result is worth keeping. The framing should become sharper.

---

# 10. The three headline packages do not yet compose into one theorem

This is the central mathematical organization problem.

The adaptive-test theorem does not use the collision theorem.

The collision theorem does not use the optional-projection theorem.

The optional-projection theorem does not use the adaptive-test hierarchy.

The dependency appendix explicitly confirms this near-independence.

As a result, the paper currently reads like three strong neighboring modules:

- nonconvex finite behavior verification;
- collision-sensitive finite resource separation;
- posterior-process stability.

A top-four paper titled “Foundations I” needs a theorem that turns these modules into one mechanism.

A natural target would be a theorem of the following form.

> Under explicit microscopic geometric, observation, and effective-presentation hypotheses, an interacting system induces a finite-resource nonconvex behavior image; the intrinsic adaptive hierarchy certifies a strictly positive private/hidden/visible resource gap with controlled degree and support; and that certified gap is stable under a stated microscopic or filtration limit.

Such a theorem would make the present sections indispensable to one another.

At present they are additive.

This is the single most important revision target.

---

# 11. The manuscript still does not prove that it is foundational to the eleven-component program

The repository history records an eleven-component graph:

A1, A2, A3, A4, B1, B2, B3, B4, C1, C2, D1.

The current history audit also records that the primary A2 algebraic-geometric chain remains independent.

This creates an unavoidable editorial and mathematical question:

> in what precise theorem-level sense is GTF-I the first general foundation of the whole program?

A paper does not become foundational because it appears first in a repository, because later files cite its terminology, or because it provides a convenient comparison interface.

One of the following must be true.

### Option A: GTF-I is genuinely foundational

Then the paper should prove an essential consumer theorem showing that a major downstream chain cannot be formulated or proved without the GTF invariant, comparison theorem, or resource object.

### Option B: GTF-I is an interface/certification layer

Then the title, abstract and programmatic positioning should say so.

The current state sits uncomfortably between these options.

The paper is strongest when read as an interface theorem.

It is weakest when read as a universal first-principles foundation.

---

# 12. The repository pipeline has a theorem-status governance problem

The second v17 review already identified a serious issue: historical files with “positive closure” language coexist with current GTF metadata that leaves full-target closure flags false.

This is not a Git hygiene detail. It is a mathematical ontology issue.

For every downstream theorem, the program needs an authoritative status such as:

- proved and current;
- proved but conditional;
- proof gap open;
- superseded;
- narrowed;
- repaired by another theorem;
- historical draft only;
- independently reviewed;
- not independently reviewed.

Branch names are not theorem status.

File names containing “closure” are not theorem status.

A typed dependency graph that verifies labels and hashes is not theorem status.

The program should maintain a theorem-level status ledger with exact statement identity and supersession relations.

This is especially important for C2, where the new v17 optional-projection theorem is presented as repairing a weakness in an older changing-filtration argument.

If the older theorem survives, explain why.

If it does not, mark it superseded or narrowed.

A top-four paper cannot rely on a repository in which contradictory closure semantics remain simultaneously live.

---

# 13. The proof ledger is useful, but the canonical article still contains too many historical layers for a first read

The 59-page canonical article is far better than the 256-page preserved development.

Still, it carries a large accumulated theorem stack from v13-v16 in addition to the three v17 headline branches.

This creates two editorial problems.

First, the reader must distinguish:

- inherited foundational definitions;
- inherited theorems still needed for v17;
- historical strengthening;
- new v17 results;
- pipeline interfaces.

Second, the main mathematical contribution becomes hard to summarize in one theorem chain.

I recommend a stricter canonical cut.

The journal-facing article should contain only:

1. the minimum resource-comparison formalism needed for the new theorem;
2. one principal structural theorem;
3. the physical realization;
4. the stability/limit theorem if it actually composes with the principal result;
5. a concise dependency appendix.

Everything else should move to a companion or supplement.

The archive can preserve history. The article should preserve focus.

---

# 14. Literature: the nearest filtered-comparison boundary remains insufficiently closed

The manuscript has improved substantially in its treatment of:

- Blackwell/Le Cam;
- Sion;
- Bernstein/Handelman/Schmüdgen hierarchy work;
- Weisshaupt.

The unresolved Norberg original-text audit remains important.

I do not assert that Norberg contains the present finite-state resource theory.

But the conceptual center of the paper is filtered/causal comparison under information constraints.

At the requested venue, the closest historical filtered-comparison result must be compared at the level of:

- exact deficiency definition;
- filtration/adaptation convention;
- operator class;
- randomization structure;
- persistent information;
- convexity closure;
- necessity/sufficiency theorem;
- proof mechanism.

Until that crosswalk is complete, the novelty boundary remains less secure than it should be.

This is not the main reason for rejection, but it remains a publication-level requirement.

---

# 15. What I would regard as a genuinely top-four-level next theorem

The paper now has enough machinery. It does not need another local patch.

It needs one theorem of substantially greater organizing force.

I see three viable routes.

## Route I — Intrinsic continuation-state classification

Define a canonical continuation-state or predictive-state object for marked causal experiments with finite persistent resources.

Then prove:

1. private/hidden/visible behavior classes can be characterized in that object;
2. exact zero deficiency has a structural factorization criterion;
3. positive deficiency admits a genuinely resource-constrained dual/separation theorem;
4. minimal tester complexity is quantitatively related to continuation-state complexity;
5. at least one lower bound matches the upper theory.

This would turn the finite comparison part into a real foundation.

## Route II — Unified microscopic-to-certificate theorem

For a nontrivial interacting microscopic class, prove in one theorem chain:

1. a resource-sensitive finite behavior image;
2. a collision- or interaction-generated gap;
3. an intrinsic adaptive certificate of the gap;
4. a quantitative stability theorem;
5. persistence of the gap under a genuinely changing microscopic limit.

This would unify the three v17 modules.

## Route III — Close one hard downstream gate completely

Choose B4 or C2 and prove one genuinely hard theorem at the scale the repository itself declares difficult.

For example:

- particle-number-uniform recollision/corrector control leading to a nonlinear semigroup statement;
- or a true changing-microscopic-path optional-projection/Girsanov/BSDE theorem.

Then prove that the GTF comparison architecture is essential in transferring that theorem to the operational resource question.

This would demonstrate program-level significance.

Any one of these routes would materially change my recommendation.

---

# 16. Required revisions before another top-four-level review

I recommend the following as hard requirements rather than optional suggestions.

## E17-R3.1 — State the true role of the adaptive representation

Either:

- prove a genuinely constrained causal/resource duality,

or:

- rename the theorem to make the revealed-candidate mechanism explicit.

The present word “duality” is mathematically legal but conceptually too strong for the role currently proved.

## E17-R3.2 — Add an intrinsic lower bound or classification theorem

At least one nontrivial lower-bound theorem is needed for:

- adaptive test degree;
- support size;
- coefficient height;
- width/horizon complexity;
- continuation-state complexity;
- or bounded-degree separability.

## E17-R3.3 — Make chart effectiveness fully formal

Give a precise input/output algorithmic theorem for:

- quotient dimension;
- rational basis;
- determinant test;
- rational chart;
- certificate pullback.

No polynomial-time claim is required, but the computability statement should be exact.

## E17-R3.4 — Prove one composition theorem joining the three v17 modules

Do not leave adaptive testing, collision realization and optional projection as parallel sections.

Prove a theorem in which each is used essentially.

## E17-R3.5 — Reframe the physical result at its actual scale

Keep the two-sphere theorem and the no-collision control.

But make explicit in the main theorem summary that:

- the \(B\)-\(W\) correlation is prepared;
- collision transduces \(B\) into an observable signal;
- the result is fixed-particle and single-collision;
- geometric similarity is not kinetic scaling.

## E17-R3.6 — Reframe the optional-projection theorem as TV-to-posterior stability

State prominently that the physical specialization uses:

- one fixed microscopic flow;
- one common latent state;
- varying observation maps;
- fixed positive Gaussian noise.

Do not let this be confused with the full historical changing-microscopic-path C2 problem.

## E17-R3.7 — Resolve theorem-status conflicts in the pipeline

Create one authoritative theorem-status ledger with fields for:

- statement identity;
- source commit;
- current/superseded/narrowed/conditional status;
- proof status;
- review status;
- upstream dependencies;
- downstream consumers;
- supersedes/repaired_by relations.

## E17-R3.8 — Demonstrate actual foundational consumption

Either show that a principal downstream chain essentially uses GTF-I, or narrow the “Foundations” framing to an interface/certification role.

A2 being explicitly independent is a serious signal that the present universal-foundation narrative is not yet proved.

## E17-R3.9 — Complete the Norberg proof-level crosswalk

This remains necessary for novelty positioning.

## E17-R3.10 — Reduce the canonical theorem stack

The 59-page article should become one theorem spine, not a compressed monograph chapter.

Move inherited or parallel material out unless it is used in the main proof chain.

## E17-R3.11 — Add theorem-level novelty subtraction

For each principal theorem, state exactly:

- classical input;
- inherited GTF input;
- new statement;
- new proof step;
- new consequence.

This will make the significance claim auditable.

## E17-R3.12 — Do not treat repository verification as mathematical evidence

Keep the excellent build, hash, manifest and diagnostic infrastructure.

But separate it visually and rhetorically from theorem validation.

A successful workflow can establish reproducibility. It cannot increase the truth probability of an analytic lemma in the way a proof does.

---

# 17. Specific theorem-level comments

1. In Theorem v17-dual, state explicitly that the partition-of-unity identity works for any compact \(B\) with continuous \(f_i\); finite causal structure enters only through the chosen behavior image.

2. The probability-measure side is minimized by a point mass. This should be said in the theorem discussion, not buried in the proof. It makes the nature of the representation transparent.

3. The finite-level hierarchy is the genuinely nontrivial part of the adaptive section. Promote it over the infinite-dimensional identity.

4. Do not call the \(4Ra/\sqrt n\) rate sharp without a lower bound.

5. The Carathéodory support theorem is existential. Do not let “support bound” be read as an efficient algorithm.

6. Clarify whether observable quotient dimension is computable directly from the rational row presentation and provide the exact procedure.

7. Preserve the small exact certificate. It is pedagogically strong.

8. In the collision theorem, the phrase “collision-generated information” is acceptable only if immediately clarified to mean “collision-generated observable of a preparation variable,” not generation of the \(B\)-\(W\) correlation itself.

9. Preserve the no-collision control as a highlighted corollary.

10. Preserve the distinction between acquisition gate and mechanical control.

11. The physical presentation theorem is constructive only at fixed positive \(\sigma_0\) on compact parameter sets. Keep this scope next to every uniform-computability claim.

12. In the optional theorem, the common latent marginal is essential. Put it in the theorem title or first sentence of every downstream use.

13. The output-law equivalence assumption is also essential. Do not imply the TV theorem directly covers singular limits.

14. The physical optional-projection theorem is strongest as a fixed-flow observation-approximation result. Present it that way.

15. The phrase “discharges a sufficient conditional-law hypothesis” is appropriate. “Closes C2” would not be.

16. The dependency appendix should contain a graphical canonical theorem DAG for the 59-page paper only.

17. Every inherited theorem in that DAG should be marked “inherited” in the margin or theorem header.

18. Every v17 theorem should be marked “new in v17” in the internal proof ledger.

19. The reader should not have to consult the 256-page development to learn whether a theorem is new.

20. The paper should explicitly distinguish “foundation for a resource-comparison interface” from “foundation for the entire theta-theory program.”

---

# 18. Positive aspects worth preserving

Despite the rejection, I want to record the following strengths clearly.

1. The manuscript is unusually careful about information-pattern semantics.

2. It no longer uses hidden convexification as if it were free private randomization.

3. The private/hidden/visible distinction is mathematically meaningful and well motivated.

4. The behavior-dimension quotient is a better invariant than raw row count.

5. The small nonlinear witness is exact and checkable.

6. The collision/no-collision comparison is conceptually strong.

7. The physical bounds are explicit.

8. The effective-presentation section avoids unsupported “computable in principle” language.

9. The optional-projection theorem gives an actual supremum-in-time estimate.

10. The coupling is not misrepresented as executable.

11. The manuscript now clearly separates fixed-particle statements from kinetic limits.

12. The clean standalone source tree is publication-quality infrastructure.

13. The literature section now subtracts substantial classical machinery rather than claiming it.

14. The response to previous referees is unusually explicit about what remains open.

15. The repository preserves historical material without deleting inconvenient earlier targets.

All of these are strengths.

The requested venue still demands a more organizing theorem.

---

# 19. Final assessment

General Theta Foundations I v17 is a serious and substantially improved mathematical manuscript.

Its new finite comparison results are coherent. Its physical example is no longer a decorative mechanics wrapper. Its posterior-process theorem is a real mathematical statement. Its reproducibility and source-governance practices are unusually careful.

But the paper is still missing the theorem that would make these strengths add up to a top-four foundational contribution.

At present:

- the adaptive representation is too close to pointwise revealed-law selection to count as a deep new duality theory;
- the quantitative hierarchy has only upper bounds;
- the collision theorem is fixed-particle and single-collision;
- the optional-projection theorem works through strong joint-TV hypotheses on a fixed latent flow;
- the three new modules are not composed;
- the primary A2 chain is not shown to depend on GTF-I;
- the hard B4/C2 gates remain outside the proved scope;
- the nearest filtered-comparison priority boundary remains incompletely audited;
- and the repository still needs authoritative theorem-level supersession/status semantics.

Therefore:

## Recommendation: Reject in the present form at the requested top-four venue.

I would support a new serious review only after the manuscript adds a theorem that either:

1. classifies finite-memory resource geometry intrinsically and gives both upper and lower complexity structure; or
2. composes the adaptive, physical and optional-projection modules into a single cross-scale theorem; or
3. closes one of the hard downstream B4/C2 gates in a way that essentially consumes the GTF architecture.

Anything materially weaker is likely to produce another long revision without changing the top-four conclusion.
