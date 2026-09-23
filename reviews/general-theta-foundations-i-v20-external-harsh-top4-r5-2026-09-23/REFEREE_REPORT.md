# Fifth Independent External Harsh Referee Report

## General Theta Foundations I: Continuation Complexity and Stable Causal Certification — Revision v20

**Author:** Qian Qi  
**Repository:** TrillionniumFoundation/theta-theory  
**Reviewed branch:** revision/general-theta-foundations-i-v20-referee-ready-2026-09-23  
**Frozen reviewed branch head:** b488b2f28bec42a555999070759d715678b87db8  
**Canonical mathematical source commit:** 63d306bb04d9b2b0bfa7d7e09e974c92764bf2d9  
**Reviewed predecessor v19:** 9cf70fe7c8aa289d1be26934451e223364aa06ef  
**Controlling v19 report:** reviews/general-theta-foundations-i-v19-external-harsh-top4-r4-2026-09-23/REFEREE_REPORT.md  
**Canonical article:** 60 pages  
**Complete preserved development:** 400 pages  
**Review date:** 23 September 2026  
**Requested standard:** Annals of Mathematics / Inventiones Mathematicae / Journal of the AMS / Acta Mathematica  
**Review type:** independent external-referee-style, pipeline-aware harsh review

## Provenance and scope

I reviewed the v20 source tree at the frozen referee-ready head, with particular attention to the new decision-continuation spectrum, the weighted finite-valued residual theorem, the sharp one- and two-response values for the marked collision family, the feedback completion, the three-response construction, the 399-sample selector, the exact residual profile, the physical decision-complexity theorem, the three measure/coupling version lemmas, the response to the v19 report, the history audit, the literature crosswalk, and the machine-readable pipeline/proof status.

I compared the new source against the v19 manuscript and the controlling v19 round-four report. The canonical v20 source is ten commits ahead of the frozen v19 manuscript and is not a cosmetic reissue. The build receipt records 60 canonical pages, 400 complete pages, 152,962 finite checks, twelve negative-control executions, and exact predecessor-page preservation. I treat all such checks as reproducibility evidence only, in agreement with the manuscript. The build receipt itself correctly states that the new analytic proofs have not been independently certified and that the all-algorithm peak-memory optimum is not asserted.

I also read the foundation blueprint in foundations/general-theta/General_Theta_Foundations_v0.1.md and its implementation note. That blueprint is important because it states a stronger foundational objective than a single post-training decision dictionary: in particular its G3 program asks for a unified theorem tracking preparation count, persistent memory, calibration error and simulation deficiency through a genuinely online experiment.

# Recommendation

## Reject in the present form at the requested top-four general-mathematics standard

This recommendation is **not** a repetition of the v19 objection.

V20 genuinely repairs the most specific defect identified in the preceding report. The lower bound and the upper construction now concern the same physical family, the same signed validation score, and the same declared training--validation cut. At that cut the manuscript proves a sharp statement: two retained states cannot certify score greater than \(2/5\), while three retained states can. The feedback-row reduction also prevents the most obvious escape through a different validation gate.

That is real mathematical progress.

The remaining top-four problem is more structural. The newly classified quantity is deliberately local to a chosen cut at which all upstream memory is finite but otherwise unrestricted. At that cut, a \(K\)-state machine has at most \(K\) conditional validation responses; conversely, the upper bound may first compute an arbitrarily large empirical object upstream and then retain only the index of one response. Thus the exact quantity \(\kappa_c\) is, mathematically, a response-dictionary/covering complexity of a declared decision interface.

That is a legitimate invariant. It is not yet an end-to-end continuation-memory complexity of the physical certification task.

V20 itself acknowledges this by recording that the all-algorithm peak-memory optimum is not proved. The exact 20,301-state profile is an optimum only for exact implementation of the authors' chosen 399-sample selector, not a lower bound for every successful auditor. Consequently the paper has closed the v19 “same-task at one cut” gap without yet proving the stronger resource theorem that would make the result a compelling first general foundation of the broader program.

At a specialist level the new theorem is interesting. At the requested Annals/Inventiones/JAMS/Acta level, I do not yet see enough structural force, generality, or downstream necessity.

# 1. What v20 genuinely fixes

The revision deserves explicit credit.

1. The former auxiliary Bernoulli lower-bound branch is no longer presented as the physical-memory theorem.
2. The decision-continuation spectrum is defined directly on the original compact behavior image.
3. The upper bound for every \(K\)-state decision-cut auditor and the finite-sample empirical-selector construction are proved in the same formalism.
4. The ideal physical product image has exact values
   \[
   \mathfrak V_1=\frac18,\qquad \mathfrak V_2=\frac38.
   \]
5. The physical perturbation bound then rules out two decision-cut states above score \(2/5\).
6. A three-response dictionary and the 399-sample selector give a score strictly above \(2/5\).
7. The feedback lemma addresses row/event continuations rather than silently proving only an all-on open-loop statement.
8. The full residual profile of the chosen selector is computed and the stochastic exact-computation lower bound is written cleanly.
9. The weighted residual theorem now treats finite-valued decisions and nonuniform word weights.
10. The three measure/coupling lemmas materially improve the presentation of the inherited global transport proof.
11. The program map does not fabricate a dependency from the independent A2 chain.
12. The B4 normalized-resolvent defect remains quarantined instead of being renamed as solved.
13. The broader historical C2 claims remain explicitly outside the scoped Gaussian/entropic repair.
14. The manuscript no longer claims that repository preservation is mathematical proof credit.
15. The response letter distinguishes the three-state decision-cut optimum from the sixteen-bit implementation upper bound.

These improvements should be preserved in any future version.

# 2. Mathematical spot-check of the new bridge

I do not find an immediate one-line mathematical contradiction in the principal v20 chain.

For Theorem 4.2, conditioning on the retained state indeed turns any admissible post-cut procedure into a list of at most \(K\) mean responses \(h_m\in[0,1]^\Omega\), giving the envelope upper bound. The empirical selector produces the stated \(n^{-1/2}\) rate; the total-variation estimate and the finite-list Hoeffding bound have the advertised constants.

For Theorem 17.1, the three witness candidates \(b_0,b_1,b_*\) give the displayed pairwise inequalities. They rule out two responses strictly above \(3/8\), while the two fractional responses displayed in the proof attain \(3/8\) using the product constraint. I found no algebraic error in that calculation.

For Lemma 17.3, the minimum of the three deterministic-event payoffs is correctly reduced to the boundary \(\sqrt a+\sqrt c\le1\), and the equality point gives \(\sqrt2-1\).

For Lemma 17.4, the odd-binomial comparison with the fair tail gives the claimed wrong-side probability bound. The bound is loose in one coordinate but valid.

For Theorem 17.5, the residual-key construction is plausible and the counting identities are internally consistent:
\[
r_t=\binom{t+2}{2}\quad(t<200),\qquad
r_t=\binom{402-t}{2}\quad(t\ge200),
\]
with peak \(20301\) at the central cut. The argument that different keys have distinguishing suffixes is the right exact-computation argument.

For Theorem 5.1, the state-overlap inequality and concavity reduction to deterministic labelings are sound as written. In particular, the proof does not make the invalid move of simply declaring a stochastic encoder deterministic.

For the three new transport lemmas, the observation-level density identity, common-path subprobability domination, and marginal-version interpretation remove real ambiguities from v19. I do not regard those three issues as unresolved objections after v20, subject to the usual measure-theoretic polishing discussed below.

This matters for the recommendation: my principal objection is now **not** “the central theorem appears false.” It is that the theorem proved is substantially weaker, more interface-dependent, and less program-defining than the title and requested venue require.

# 3. The new “continuation complexity” is a post-training response-dictionary complexity

Theorem 4.2 is clear enough to reveal exactly what it measures.

At the designated cut:

- all training-dependent data must be compressed into \(M\in[K]\);
- downstream validation may use fresh randomness;
- upstream memory before the cut is finite but unrestricted;
- downstream event storage is counted separately;
- the score depends only on the selected validation response.

Therefore a \(K\)-state lower bound at this cut is equivalent to saying that no list of \(K\) validation responses covers the behavior image above the target score.

The converse is equally revealing. To attain a response list, the machine may estimate the candidate law with a potentially very large histogram upstream, choose the best response, discard the histogram, and retain only its index.

This is why the exact cover formula is so clean.

The clean formula is not a defect. The problem is the foundational interpretation.

The theorem does **not** classify:

- the minimum peak state count over the full online training schedule;
- the minimum number of bits needed by every successful audit;
- the preparation-memory tradeoff;
- the sample-memory tradeoff;
- the transition-description complexity;
- the memory needed when the cut is moved earlier;
- the memory needed for a high-confidence certificate rather than an expected-score game.

In other words, \(\kappa_c\) classifies the number of post-training continuation labels, not the whole causal computational burden of learning which continuation to use.

For a paper titled “General Theta Foundations I,” that distinction is now the central editorial issue.

# 4. Cut placement is doing substantial mathematical work

The manuscript calls \(\mathfrak V_K(B,Q)\) a continuation invariant of the marked decision interface. The final words are essential: **of the interface**.

If one moves the charged cut:

- before sufficient statistics have been accumulated,
- before a large empirical histogram has been reduced,
- after the event has already been chosen,
- or after part of validation,

the required state count can change drastically.

This makes the invariant useful but protocol-relative.

A genuinely foundational continuation-complexity theory should explain how the complexity transforms under natural refactorizations of the same experiment. At minimum I would expect monotonicity, composition, or a profile theorem that treats the complete sequence of charged cuts and does not allow the decisive upstream computation to disappear behind a single checkpoint.

The current exact three-state theorem is partly an exact theorem about **where the authors decided to place the checkpoint**.

That is much weaker than saying the physical task itself has intrinsic three-state complexity.

The text is careful not to make the latter statement literally, but the title, introduction, and programmatic role still draw conceptual benefit from it.

# 5. The physical task still has no matched all-algorithm peak-memory lower bound

This is the most important remaining mathematical gap.

The paper proves two different exact statements:

1. every successful auditor needs at least three states at the final training/validation cut;
2. the authors' selected exact rule has a peak trial-cut width \(20301\), and a bitwise implementation uses at most \(40602\) states.

What is **not** proved is any nontrivial lower bound on
\[
\inf_{\mathcal A:\ \text{score}>2/5}
\ \max_t |\mathsf{State}_t(\mathcal A)|.
\]

The infimum here is over all successful finite-reset auditors, not just exact implementations of the chosen three-event majority selector.

The distinction is not cosmetic. A different approximate auditor could in principle use a different training statistic, different stopping structure, randomized compression, or a different response dictionary while still ending with three states. The theorem gives no lower bound such as \(n^\alpha\), \(c\sqrt n\), \(\log n\), or even a constant above three for the peak width of all such procedures.

Thus the previous request for a “physical memory lower bound” has been answered only after narrowing the word “memory” to one selected interface.

That is an acceptable response to a local theorem request. It is not yet the end-to-end resource theorem suggested by the broader program.

# 6. The exact residual profile is for exact computation of one rule, not for the physical statistical task

Theorem 17.5 is mathematically useful. It gives a clean residual quotient and a simultaneous exact-width profile.

But it solves the automata problem
\[
\text{exactly compute this specified 399-sample event-selection function}.
\]

The physical objective is instead
\[
\text{obtain worst-case expected score}>2/5.
\]

These are different optimization problems.

Exact computation may require many residual classes even when approximate computation with small statistical regret can be much more compressed. The paper explicitly acknowledges this, but then the 20,301 and sixteen-bit numbers cannot serve as evidence that the physical task itself has comparable memory complexity.

A top-four resource theorem would connect the statistical margin to approximate residual complexity and prove a lower bound for all rules achieving that margin.

The weighted theorem is an obvious tool for attempting this. V20 does not yet carry out that program on the physical family.

# 7. “Certification” is an expected-score notion, not a confidence guarantee

The reset-audit score is the expectation of one signed event difference after training, using one candidate validation and one target validation.

That is a coherent decision-theoretic objective.

It is not, by itself:

- a confidence statement;
- a uniformly valid test with specified type-I/type-II errors;
- a confidence sequence;
- a sequential stopping guarantee;
- a probability-\(1-\alpha\) certificate that the candidate family is separated.

The manuscript says this explicitly, which is good.

But the word “certification,” especially in a foundational theorem, naturally suggests a stronger operational conclusion than expected payoff. The three-state classification could change substantially when the output must include a statistically reliable decision rather than maximize a one-shot expected signed score.

At minimum the title and abstract should distinguish “expected-score certification” from statistical certification in the usual high-confidence sense. A stronger paper would show how continuation complexity changes when confidence is imposed.

# 8. The general spectrum theorem is mathematically clean but structurally elementary

The core proof of Theorem 4.2 consists of:

1. conditioning on a \(K\)-valued retained state;
2. obtaining \(K\) conditional validation responses;
3. bounding a convex combination by their maximum;
4. estimating those \(K\) response payoffs empirically;
5. using compactness and a finite-class concentration bound.

The half-space-cover characterization is then almost a restatement of the strict envelope condition.

Again, this is correct mathematics.

At the requested venue level, however, the general theorem needs a stronger reason to exist as a foundational result. As presently stated, the difficult geometry is pushed into the chosen compact set \(B\), while the classification itself is a finite response-dictionary cover plus empirical model selection.

A genuinely stronger continuation theory might include, for example:

- a multi-cut resource profile;
- an approximate residual invariant with sharp upper and lower bounds;
- sequential or adaptive validation;
- a composition/tensorization theorem for spectra;
- infinite or continuous observation alphabets under nontrivial compactness assumptions;
- communication-style or information-style lower bounds that constrain the training phase as well as the final index;
- a theorem coupling sample size and memory rather than allowing unrestricted upstream memory;
- a sharp minimax theorem for a nontrivial class of behavior images.

Without such an extension, I do not regard Theorem 4.2 by itself as top-four-level general mathematics.

# 9. The physical three-response calculation is sharp but small-scale

The physical application has attractive internal coherence:

- two labeled hard spheres;
- one nongrazing collision;
- a prepared impact--mark correlation;
- two acquired report bits;
- a fair terminal mark;
- fixed positive Gaussian noise;
- one compact collision-parameter interval;
- three validation events.

The collision/no-collision control remains conceptually strong.

But the new exact state classification is ultimately a three-response covering calculation on a two-parameter product image. The geometry needed for the \(2\)-versus-\(3\) result is captured by three witness candidates and three simple events.

That is an elegant example. It is still far from:

- a many-particle interaction;
- a collision network;
- a kinetic scaling;
- a singular-noise limit;
- an unknown-calibration problem;
- a nontrivial phase transition in the response spectrum;
- a high-dimensional family where the continuation number exhibits new asymptotic geometry.

The physical realization therefore supports the theorem; it does not elevate the theorem to a general physical-complexity theory.

# 10. The no-training-factor stability is special to the blind source

Theorem 17.6 obtains a particularly clean perturbation statement when \(d\) changes because the private candidate training law is unchanged and only the physical target changes.

This is useful.

It should not be read as a general stability principle for learned auditors.

The inherited reset-transport theorem already records that perturbing training laws can produce a training-count factor through product coupling. In the current physical family \(\alpha=0\), so that difficulty disappears.

Thus the statement “there is no multiplier equal to the number of training trials” is a property of this source-invariant perturbation, not a general theorem saying learned causal certificates are stable without sample-size amplification.

For the broader G3 resource-transfer goal, the difficult case is precisely when the source behavior, calibration, or acquisition law changes and training itself must be transported.

# 11. The weighted residual theorem is promising but is not yet the missing statistical-memory theorem

Theorem 5.1 is one of the more interesting new additions.

The use of weighted distinguishing suffixes and state-distribution overlaps produces a legitimate distribution-sensitive obstruction. The concavity argument correctly avoids an unjustified deterministic reduction.

But the current theorem remains a flexible lower-bound template, not a sharp classification.

The manuscript does not provide:

- a dual characterization of the best weighted obstruction;
- a general sharpness theorem;
- asymptotics of the obstruction under product measures;
- a physical-family lower bound for all approximate successful auditors;
- an equivalence with a known graph/information quantity;
- a theorem showing when randomization strictly changes approximate width.

The most natural next step is to use this machinery to attack the all-algorithm peak-memory problem identified above. Until that is done, the weighted theorem is adjacent to the principal physical classification rather than the theorem that closes its remaining resource gap.

# 12. The feedback completion is useful, but the row-indexed statement should be formalized more cleanly

Theorem 17.6 writes
\[
\kappa_{2/5}(B,Q_{d,\sigma})=3
\]
using the one-row spectrum notation, and then invokes Lemma 17.2 to say that feedback-row selection cannot improve the two-state bound in the full interface.

The proof idea is reasonable: on the selected private subfamily, every row/event continuation pulls back to a response on the all-on marked law.

For publication, however, the exact full-interface optimum should be given its own notation—say \(\kappa^{\rm rows}_{2/5}\)—and both inequalities should be stated and proved directly for that object. The current presentation moves between one-row \(\kappa\) and the full row-indexed operational claim in prose.

I do not currently treat this as a fatal mathematical error. It is exactly the sort of quantifier/interface ambiguity that a paper about typed causal resources should eliminate completely.

# 13. The general operational converse uses arbitrary real response probabilities

The spectrum optimizes over all \(h\in[0,1]^\Omega\). Every such vector is represented as the mean response of a randomized event.

For the abstract expected-score theorem this is fine.

For a resource-aware operational interpretation, however, arbitrary real probabilities have description and implementation costs. The physical theorem avoids this issue by using deterministic rational events, but the general converse does not.

If the paper wants \(\mathfrak V_K\) to be a computational/physical resource invariant rather than only a decision-theoretic value, it should add a rational finite-support approximation theorem: given a strict margin, approximate the optimal response list by explicitly implementable rational randomization while tracking any additional state, random-bit, or description cost.

Otherwise “\(K\) states suffice” in the general theorem hides unlimited precision in the post-cut randomizer.

# 14. The transport repair is now technically better, but its scope remains narrow

The three new lemmas answer the v19 technical requests well.

In particular:

- the observation-level Radon--Nikodym derivative is now explicit;
- the common-path subprobability domination is written as a lemma;
- the coupled stochastic integrals are interpreted through marginal measurable versions rather than a false Brownian claim in the joined filtration.

This substantially improves the proof chain.

But the underlying global consumer still assumes:

- common latent preparation;
- bounded signals;
- fixed strictly positive Gaussian noise;
- equivalent laws;
- bounded scalar entropic terminal transform;
- the specific quadratic entropic structure.

This remains a scoped C2 repair. It is not a general changing-filtration or cotangent-rigidity theorem.

The pipeline status says this correctly. The main article should continue to resist any broader wording.

# 15. The pipeline is honest, and that honesty limits the foundational claim

The namespaced program map is a significant improvement in scholarly discipline.

It records that:

- the primary A2 geometric chain is independent and not consumed;
- the B4 historical normalized-resolvent identity is defective and the aggregate B4 program is not certified;
- the broader historical C2 strict-dual/form-response/rigidity program is not certified;
- the present C2 result is a bounded Gaussian/entropic scoped consumer;
- the full eleven-component program is not certified by GTF-I.

I agree with these status statements.

But they have an editorial consequence.

The repository does **not** presently support the interpretation that this paper is the unique first-principles root from which the eleven-paper theta-theory program follows.

The foundation blueprint itself was more nuanced: it proposed a shared typed foundation and identified G1--G4 as substantial research goals. In particular G3 asks for a unified resource--precision--statistical-error theorem with preparation count, persistent labels, calibration error and simulation deficiency tracked together.

V20's exact three-state post-training decision dictionary is a useful result inside that agenda. It is not yet G3.

Nor does v20 close G1, G2, or G4 in their general forms.

Accordingly, one of two programmatic positions should be adopted without ambiguity:

### Position A: a genuinely universal first foundation

Then prove theorem-level dependencies from major presently independent branches and a resource theorem that survives beyond the chosen decision cut.

### Position B: the root of the causal comparison/certification branch

Then the current mathematics is much easier to defend, but the title and program description should say exactly that.

At present the manuscript is mathematically closer to Position B.

# 16. The unresolved B4 defect remains relevant to any “whole pipeline” claim

The history audit correctly tests the historical normalized nonlinear resolvent identity on constants and finds that the displayed formula fails.

V20 also records a correctly typed conditional nonlinear identity under already established graph and resolvent hypotheses.

That is the right response.

But the conditional identity does not prove:

- range;
- comparison;
- compact action sublevels;
- the kinetic corrector;
- the historical nonlinear semigroup aggregate.

Therefore B4 remains an actual program blocker, not merely a documentation item.

This does not invalidate Theorem 17.6. It does invalidate any suggestion that the current GTF paper has already closed the broader dynamical pipeline.

# 17. A2 independence is still decisive for the “first foundation” narrative

The current A2 primary geometric chain is explicitly independent.

That fact should not be hidden by inventing an interface arrow, and v20 correctly refuses to do so.

But an independent major first-principles chain means the global program currently has multiple roots.

A top-four foundation paper can certainly be one root among several. What it cannot do is derive significance from being the single universal root while the proof graph itself says otherwise.

A nonartificial A2 consumer of the GTF formalism—or an explicit multiple-root architecture—would resolve this tension.

# 18. The nearest filtered-comparison literature remains insufficiently audited

The literature crosswalk is more honest than many submissions: it explicitly says the original Norberg proof was not obtained and makes no theorem-level absence claim.

That honesty should be preserved.

It also means the publication-level novelty comparison is incomplete.

The closest historical literature already concerns comparison of statistical experiments on filtered probability spaces, successive actions, and risk-based deficiency. For a paper whose conceptual center is resource-aware filtered comparison and decision continuations, a theorem/page-level comparison is not optional at the requested venue.

The final version should compare at least:

- exact operator class;
- admissible adaptation;
- where randomization enters;
- whether persistent memory is represented;
- risk/deficiency equivalences;
- necessity and sufficiency directions;
- finite versus general state spaces;
- whether the decision rules already factor through finite response lists;
- the precise new content of the present \(K\)-response spectrum.

The same precision is needed for residual/Nerode and finite-state statistical decision mechanisms. It is not enough to say those mechanisms are classical while leaving the novelty boundary qualitative.

# 19. The canonical article still carries too many generations of architecture

The 60-page article contains:

- intrinsic marked deficiency;
- exact causal realization;
- decision-continuation spectra;
- weighted residual obstructions;
- reset minimax;
- binary streaming;
- nonlinear testing;
- adaptive hierarchy;
- rational charts;
- collision resource gaps;
- optional stability;
- Gaussian transport;
- coupled-version lemmas;
- global entropic transport;
- microscopic composition;
- physical decision complexity;
- the older compressed certificate;
- phase machines;
- the eleven-paper dependency map.

The source-preserving companion is useful for history.

The journal article should be organized around one unavoidable theorem chain.

At present the new top-level decision theorem is conceptually simpler than the amount of inherited architecture around it. This makes the paper feel like a cumulative repository artifact rather than a mathematically inevitable article.

Two viable editorial routes are:

1. focus the paper tightly on continuation dictionaries, weighted approximate residuals, and physical finite-memory testing, with the transport material moved to a companion; or
2. strengthen the continuation theory enough that all these modules become essential consequences of one genuinely general theorem.

# 20. Technical and presentation requests

These are secondary to the structural issues above, but they should be fixed in any next revision.

## 20.1 Define the full feedback-row complexity explicitly

Introduce the row-indexed analogue of \(\kappa_c\), state its exact value for the physical task, and avoid using one-row notation for a full-interface conclusion.

## 20.2 Add rational operational approximation to the general spectrum

For strict margins, show how arbitrary optimal real responses can be approximated by finite rational randomization and state exactly what randomness/description resources are charged.

## 20.3 Give transformation rules under moving or splitting a cut

A resource theory based on checkpoints needs at least monotonicity or comparison statements under natural interface refinements.

## 20.4 Convert the weighted residual theorem into a physical all-algorithm lower bound

Use actual training-word probabilities and score margins to lower-bound the peak or integrated memory of every auditor achieving score \(>2/5\). Even a scaling-correct nonsharp bound would be much more important than further improvement of constants in the present selector.

## 20.5 Add a confidence-level version of certification

State and analyze a version with prescribed error probability or confidence. Explain whether the three-response dictionary remains optimal and how repeated validations affect state complexity.

## 20.6 Complete the theorem-level literature audit

The Norberg gap is publication-level, not cosmetic. Resolve it before making a priority or top-four novelty case.

## 20.7 Correct the apparent source corruption in the weighted-capacity formula

In weighted-residuals.tex, the capacity condition contains the token sequence “{m or}” between the two word-equality alternatives. The build succeeds, but the source should be checked against the intended logical “or” and the rendered equation. A foundational paper should not leave an ambiguous mathematical condition in the source.

## 20.8 State the exact scope of the no-training-factor perturbation in the theorem summary

Make explicit in the headline statement that the candidate training law is unchanged by the moving-collision parameter. Otherwise readers may incorrectly infer a general sample-count-free stability result.

# 21. What would change my top-four recommendation

Another round of smaller constants, more finite diagnostics, another exact event dictionary, or further repository bookkeeping would not change the recommendation.

One of the following could.

## Route I: End-to-end physical memory complexity

Define a full resource objective, for example the minimum over all successful auditors of the maximum retained-state width across training, decision, and validation cuts.

Prove a nontrivial lower bound for the actual collision family and a matching or scaling-matching construction.

This would turn the current three-state checkpoint theorem into one component of a genuine physical complexity theorem.

## Route II: General multi-cut approximate continuation theory

Develop an invariant that tracks approximate continuation classes across an entire causal schedule, with explicit sample-memory tradeoffs, persistent-randomness accounting, and composition laws.

Prove upper and lower bounds for a nontrivial class of compact behavior images and recover the collision theorem as a true corollary.

This would be substantially more general than a response cover at one decision cut.

## Route III: A major downstream theorem that essentially consumes GTF

Prove that a mathematically substantial downstream component—an important A2, B4, C2, or other major program theorem—cannot be obtained without the GTF continuation/resource structure, and prove that consumer under its real model hypotheses.

A bounded Gaussian scoped consumer is useful but not sufficient for the whole foundation narrative.

## Route IV: Singular or high-dimensional physical scaling

Show a nontrivial asymptotic law for continuation complexity under growing particle number, collision-network depth, vanishing observation noise, unknown calibration, or another genuinely singular/high-dimensional regime, with matched resource bounds.

Any of these routes would create structural mathematics beyond the present finite response dictionary.

# 22. Final assessment

V20 is a serious and substantially improved revision.

I regard the following new claims as mathematically plausible after the present source-level inspection:

- the operational \(K\)-response envelope at a declared decision cut;
- the exact \(1/8\) and \(3/8\) values for the first two responses on the ideal product image;
- the feedback reduction on the selected private subfamily;
- the three-response envelope and 399-sample expected-score construction;
- the exact residual profile of that chosen rule;
- the weighted finite-valued overlap obstruction;
- the three measure/coupling clarification lemmas.

The revision therefore **does close the narrow v19 same-task/same-cut objection**.

But the stronger foundational question remains open:

> Does one intrinsic resource notion classify the end-to-end cost of learning, retaining, and executing a successful physical certificate across the whole causal schedule, and does that resource structure become essential for the larger theta-theory pipeline?

V20 does not yet prove that.

Its exact answer is instead:

> at one designated post-training decision cut, the physical task needs exactly three conditional validation responses; one particular successful selector has a separately computed exact implementation profile.

That is a worthwhile theorem. I do not consider it sufficient, by itself or together with the still-partial pipeline, for the requested Annals/Inventiones/JAMS/Acta standard under the title “General Theta Foundations I.”

**Recommendation:** reject in the present form at the requested top-four general-mathematics standard. A fundamentally strengthened resubmission should target end-to-end resource complexity, a genuinely general multi-cut continuation theory, or an essential major downstream consumer rather than another local refinement of the current decision-cut calculation.

---

## Referee checklist

- Latest referee-ready v20 branch and frozen head explicitly identified.
- v19 controlling report compared against the substantive v20 response.
- No obvious one-line counterexample found in the inspected new spectrum, two-state obstruction, three-response construction, residual profile, weighted overlap theorem, or version lemmas.
- V20 credited with closing the narrow same-task decision-cut objection.
- Build/diagnostic evidence treated as reproducibility, not proof.
- All-algorithm peak-memory optimality recognized as unproved.
- Expected-score certification distinguished from confidence certification.
- Decision-cut complexity distinguished from end-to-end online memory.
- A2 primary chain recognized as independent.
- Historical B4 defect recognized as unresolved and not consumed.
- Historical broad C2 aggregate not treated as closed.
- Full eleven-paper pipeline not treated as certified.
- Original Norberg proof-level crosswalk recognized as unresolved.
- Principal remaining objection classified as structural/significance/general-resource scope, not a recycled v19 complaint.
