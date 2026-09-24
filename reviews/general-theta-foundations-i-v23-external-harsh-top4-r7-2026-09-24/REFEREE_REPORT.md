# Seventh Independent External Harsh Referee Report

## General Theta Foundations I: Compatible Statistical Experiments and Resource Frontiers — Revision v23

**Author:** Qian Qi  
**Repository:** TrillionniumFoundation/theta-theory  
**Reviewed branch:** revision/general-theta-foundations-i-v23-referee-ready-2026-09-24  
**Frozen reviewed branch head:** e926b783b643b3e7f275a18105528927b76cc97b  
**Canonical source commit recorded by the referee-ready package:** 8a6043aca644043bd805668185eb227468f21170  
**Reviewed predecessor:** revision/general-theta-foundations-i-v22-referee-ready-2026-09-24 at 88832f95b7dd0b8cc4a3061280a6e31f9fa67319  
**Controlling prior external report:** reviews/general-theta-foundations-i-v22-external-harsh-top4-r6-2026-09-24/REFEREE_REPORT.md, recorded by the v23 response at 37ff0991b2764ce2fba14541c6191b26661e000e  
**Canonical article:** 96 pages  
**Complete preserved development:** 649 pages  
**Review date:** 24 September 2026  
**Requested standard:** Annals of Mathematics / Inventiones Mathematicae / Journal of the AMS / Acta Mathematica  
**Review type:** independent external-referee-style, pipeline-aware harsh review

## Provenance and scope

I reviewed the actual latest referee-ready v23 branch. The working branch revision/general-theta-foundations-i-v23-compatible-frontiers-2026-09-24 and the referee-ready branch are identical at the frozen head above. Relative to the v22 referee-ready head, v23 is three commits ahead and adds the compatible-occupation formulation, the polynomial certificate hierarchy, the binary noisy recursions, the exact three-report frontier, the resource-order/calibration layer, and the revised consumer and pipeline material.

I read the v23 response to the sixth report and the new central source files, in particular:

- compatible-occupations.tex;
- binary-noisy-frontiers.tex;
- three-report-frontier.tex;
- acquisition-and-resource-order.tex;
- theta-frontier-consumers.tex;
- the revised introduction and main theorem;
- the v23 proof, pipeline, history, resource, and literature records.

I also re-read the inherited modules directly implicated by the new claims: sample-memory-frontier.tex, physical-frontier.tex, the fixed-profile physical and confidence consumers, the dependency appendices, and the General Theta Foundations blueprint. I used the repository's explicit current status of the independent A2 chain and the unresolved historical B4 and broad C2 targets in judging the programmatic claim.

I did not independently re-prove every theorem in the 649-page preserved development. The build, finite diagnostics, negative controls, source hashes, and preservation checks are useful reproducibility evidence. They are not proof certification or novelty evidence.

I additionally checked the immediate literature boundary around finite-memory testing and polynomial POMDP descriptions. The classical Hellman–Cover finite-memory program is broader historically than a single citation might suggest; the Müller–Montúfar POMDP work already treats polynomial/semialgebraic feasible-frequency descriptions; and a directly relevant 2026 preprint by Managoli and Prabhakaran studies randomized time-invariant finite-state binary testing and obtains matching exponential-in-state upper/lower behavior for a class of adversarial problems. These facts do not refute a v23 theorem, but they raise the bar for the novelty claim attached to the finite-state resource layer.

# Recommendation

## Reject in the present form at the requested top-four general-mathematics standard

This recommendation is materially different from the v22 recommendation.

V23 has crossed two thresholds that the sixth report explicitly asked to see:

1. there is now an exact necessary-and-sufficient description of all stochastic machines for a fixed finite full profile, not merely a constructive upper bound or a residual relaxation; and
2. there is now a genuinely noisy overlapping-support exact class, not only an erasure–revelation model.

Accordingly, several central objections of the sixth report are obsolete and should not be repeated. In particular, it is no longer accurate to say that the manuscript has no general all-machine converse formulation or no nontrivial noisy exact example.

The present rejection rests on a new distinction:

> V23 solves the finite-architecture feasibility problem by an exact semialgebraic encoding and a generic Positivstellensatz hierarchy, but it does not yet extract from that encoding a structural statistical resource theorem of the depth, sharpness, or downstream necessity expected at the requested venues.

The most general converse is formally complete but quantitatively noninformative.  
The most explicit noisy frontier remains extremely small and special.  
The physical collision problem has been embedded into the formal converse but has not acquired a new evaluated lower bound.  
The full sample–memory problem varies the schedule and architecture, while the new exact theorem fixes them.  
The autonomous problem is encoded but not structurally solved.  
The resource tuple is defined but no joint Pareto law is proved.  
The pipeline remains multiple-root, with A2 independent and B4/C2 obligations unresolved.  
The closest finite-memory literature boundary is still not sufficiently settled for a “General Foundations I” paper at top-four level.

I therefore view v23 as a serious, technically competent, and substantially improved finite statistical resource framework, but not yet as a top-four general-mathematics foundation.

# 1. What v23 genuinely fixes

The revision deserves explicit credit.

### 1.1 A true fixed-protocol necessity/sufficiency statement now exists

Theorem thm:v23-occupation does more than attach a lower-bound relaxation to a controller. For a declared finite schedule and declared register profile, it characterizes exactly the occupation arrays arising from stochastic machines.

The key proportionality equations enforce one common stochastic row across all hidden histories that present the same observable row. The proof also handles zero incoming mass correctly rather than cancelling a quantity that may vanish. This is the right correction to any attempt to optimize separate hidden-history encoders independently.

### 1.2 Shared-row constraints give a legitimate autonomous formulation

The manuscript now distinguishes externally clocked transition tables from shared rows and explains how cross-occurrence compatibility encodes a reused autonomous table. This directly answers the earlier request not to treat an external clock as free autonomous memory.

### 1.3 The all-machine upper side is now mathematically complete for a fixed finite architecture

Theorem thm:v23-dual applies an Archimedean positivity theorem to the compact feasible semialgebraic set. Every strict upper bound can, in principle, be certified at some finite degree. Dyadic controller tables supply constructive lower witnesses converging to the same value.

This is a genuine converse framework. It is not the old weighted-residual relaxation.

### 1.4 The noisy theory is no longer an erasure toy

The Bayesian interval recursion handles binary finite overlapping observations with arbitrary finite losses, priors, finite register profiles, and finite controlled experiment choices.

The minimax receiver-curve recursion handles every finite horizon for uncontrolled binary observations and one-/two-state registers.

The three-report BSC theorem gives exact Bayes and minimax values over all stochastic machines.

### 1.5 V23 exhibits a strict compatibility effect

For profile (2,2,2), a free initial mixture of the complementary Bayesian machines improves the minimax value beyond what any machine of the original profile can attain. This is a clean demonstration that convexifying complete machines can silently add a selector resource.

### 1.6 Calibration acquisition is no longer an oracle

The sampled-calibration theorem actually draws from the target distribution, keeps the entire counter vector in the persistent state, charges fair bits, and carries the calibration state through the subsequent auditor.

### 1.7 The confidence statement now has a matched lower bound in its declared interface

The three-repetition Bernoulli interface is not merely an amplifier with an upper construction. Within that interface, the exact three-report theorem supplies the lower side as well.

### 1.8 The pipeline claims remain disciplined

The current metadata does not claim that:

- A2 is derived from this paper;
- the original B4 aggregate is repaired;
- the broad C2 aggregate is proved;
- the physical fixed-sample Pareto boundary is evaluated;
- the whole eleven-paper program is closed.

This honesty matters. It also determines what significance can legitimately be attributed to the paper.

# 2. Source-level mathematical spot checks

My recommendation is not based on finding an immediate local contradiction in the new v23 core. I record the checks because future revisions should not waste effort “repairing” statements that I am not currently contesting.

## 2.1 Compatible occupation reconstruction

Suppose an observable row r has a positive incoming mass x(theta0,i0,r). Defining the transition probability by f(theta0,i0,r,j)/x(theta0,i0,r) and using the cross-products

f(theta,i,r,j) x(theta',i',r)
=
f(theta',i',r,j) x(theta,i,r)

does recover the same row at every positive incoming mass. At a zero incoming mass, conservation and nonnegativity force every outgoing mass to vanish. If an entire observable row is unreachable, an arbitrary legal row can be inserted without altering the occupation array.

I do not see a zero-boundary defect in this argument.

The same mechanism across identified occurrences is a valid way to encode one reused transition table, provided the row identities themselves represent exactly the charged observable inputs. The manuscript is careful on that point.

## 2.2 Compact semialgebraic feasible set

The occupation coordinates are bounded subprobabilities and the protocol is finite. Adding a redundant ball inequality makes the quadratic module explicitly Archimedean. Encoding equalities by both signs and then collecting their multipliers into an ideal term is consistent with the standard Positivstellensatz setup.

I therefore do not object to the statement that every strict scalar upper bound admits some finite-degree certificate.

## 2.3 Dyadic lower witnesses

Rounding each row of a finite stochastic table to a dyadic simplex and coupling executions until their first row-level discrepancy gives a horizon-dependent total-variation estimate of the advertised additive form. The bound is crude, but it is a legitimate convergence argument for a fixed finite protocol.

## 2.4 Bayesian continuation and interval partitions

For a fixed prior and a clocked finite protocol in which each time-indexed row is encountered at most once, the expected reward is multiaffine in the stochastic row variables. Sequentially replacing rows by simplex vertices yields a deterministic optimum.

Given a fixed suffix, the value of sending a posterior atom to a suffix state is affine in the scalar binary posterior. The upper envelope of finitely many affine functions has interval cells. Thus the interval-partition conclusion is consistent with the classical likelihood-ratio quantizer mechanism.

I do not find an immediate gap in the stated binary, conditionally independent, clocked setting.

## 2.5 Receiver-curve minimax recursion

For a binary summary of a finite binary experiment, replacing it by a receiver-curve point at the same false-positive coordinate gives a Blackwell-dominating binary experiment. Conditional independence of the next report permits tensoring the dominating prefix with the next observation. This supports the induction used in thm:v23-minimax-recursion.

The restriction to uncontrolled observations and one-/two-state registers is doing real work. The manuscript acknowledges this.

## 2.6 Three-report BSC formulas

I checked the algebra around the middle-register reduction and the balanced threshold.

For the canonical edge quantizer with parameter w, the factor

p^2 (1-p)^2 (1-2p) (1-2w)^2

has the required sign for 0<p<1/2 and 0<=w<=1/2.

The balanced randomization

a(w)=2(1-2w)/(3-2w)

lies in [0,1], and the displayed derivative of R(w) has the correct sign on the same interval. The factorized gap from w=0 is nonnegative there. Substitution at w=0 yields the stated minimax value 1-p+d(p)/3.

I do not see an arithmetic counterexample to the headline three-report formulas.

## 2.7 Sampled calibration

The Hoeffding/union-bound calculation gives the stated M of order rho^{-2} log(K/beta). The register count (M+1)^K is conservative but correctly exposes the price of retaining all counters. The expected-score loss of 2 beta on the bad calibration event is consistent with a score in [-1,1].

## 2.8 Confidence interface

Once the audit output is deliberately converted to the declared Bernoulli interface, monotone coupling does place the least favorable alternative at the endpoint used in the BSC theorem. The manuscript also states the important limitation: a richer physical auditor is not constrained by this coin-interface lower bound.

These checks support the central conclusion of this report: the remaining problem is principally structural depth, novelty, sharpness, and foundational necessity, not a one-line algebraic failure in the new v23 modules.

# 3. The central issue: “complete converse” now means generic semialgebraic completeness

The phrase “complete full-profile converse” sounds stronger than the mathematical increment actually delivered.

For a fixed finite schedule and fixed finite row architecture, the controller is already described by finitely many stochastic-row parameters. Its expected payoff is a polynomial or rational expression obtained by multiplying finitely many transition probabilities. One can therefore view the feasible controller/payoff set directly as a compact semialgebraic image.

V23 instead introduces occupation variables and rank-one proportionality equations. This is useful because:

- it exposes hidden-history compatibility explicitly;
- it gives a zero-safe reconstruction theorem;
- it aligns with flow-based formulations;
- it makes relaxations and shared-row constraints transparent.

But after that exact finite-dimensional encoding is available, the existence of a convergent sum-of-squares hierarchy for strict upper bounds is inherited from general real algebraic geometry. Putinar supplies the completeness mechanism. Powers supplies the rational variant. The manuscript says this honestly.

The top-four question is therefore not whether the hierarchy is correct. It is:

> What new statistical mathematics is obtained from this hierarchy that was not already implicit in “finite stochastic controller + polynomial constraints + generic positivity theorem”?

At present the answer is not strong enough.

The paper proves no architecture-independent dual object, no explicit degree bound tied to memory, no finite exactness criterion, no rank theorem for the hierarchy, no structural description of extremal certificates, no asymptotic certificate complexity, and no general closed form for the value.

Thus “complete” is logical completeness for strict polynomial upper certification, not a complete statistical theory of the resource frontier.

That distinction should be central to the paper rather than left as a caveat after the theorem.

# 4. The occupation theorem is useful, but its novelty boundary is narrow

The proportionality equations are mathematically natural conditional-independence constraints. They express that the conditional distribution of the next observer choice depends only on the observable row and not on the hidden environment/history.

This rank-one/minor mechanism is not new in itself. The manuscript now cites Müller–Montúfar and correctly notes that polynomial feasible-frequency descriptions and vanishing minors already occur in POMDP optimization.

The finite-horizon theorem adds several real features:

- changing register alphabets;
- explicit cross-environment rows;
- zero-occupation reconstruction;
- shared rows for autonomous reuse;
- a finite full-profile interpretation.

These are worthwhile.

But for a top-four general-mathematics contribution, a repackaging/generalization of conditional-independence minors should lead to a theorem whose consequence is unexpectedly strong. In v23, the strongest generic consequence is still the black-box Positivstellensatz hierarchy.

I would want at least one of the following before treating this as the central theorem of a top-four paper:

1. a canonical minimal set of compatibility equations with a nontrivial algebraic-geometric classification;
2. a bounded-degree or finite-convergence theorem controlled by protocol width/tree structure;
3. an explicit dual whose variables have statistical meaning rather than generic SOS multipliers;
4. a decomposition theorem showing when profile optimization factors, and exactly when it does not;
5. a sharp asymptotic consequence for a broad noisy class.

Without such a development, the occupation theorem is a good exact formulation, not yet a deep general invariant.

# 5. The SOS hierarchy gives no quantitative resource law

The theorem proves

V = inf_d U_d.

It does not prove any useful relationship between d and:

- horizon;
- number of hidden histories;
- number of environments;
- register width;
- number of actions;
- desired accuracy;
- distance to the boundary;
- conditioning of the experimental kernels.

This matters because the physical and statistical claims are resource claims.

For the compact-family extension, one first chooses a finite kernel net and then, for that enlarged finite polynomial problem, eventually chooses a certificate degree. As the net is refined, the required degree may grow without any stated control. The theorem therefore establishes consistency in an iterated limit, not a quantitative converse.

Similarly, the dyadic lower approximation has an error proportional to the number of row occurrences. On long schedules the required bit precision must grow with the schedule if one wants a fixed global tolerance.

There is nothing wrong with these facts. They simply show what the theorem is: a completeness statement for a fixed finite problem, not a sample–memory scaling theorem.

The paper currently asks a generic real-algebraic hierarchy to carry much of the weight of the word “frontier.” It cannot do that without quantitative extraction.

# 6. Fixed protocol is not the same object as the physical sample–memory frontier

This is the most important unresolved mathematical distinction after v23.

The occupation theorem fixes:

- a finite schedule sigma;
- the location of every cut;
- the allowed observable rows;
- a register alphabet at each cut;
- the permitted experimental operations.

Then it optimizes all stochastic transition tables inside that architecture.

The physical sample–memory problem asks a different question. It compares algorithms that may use different:

- numbers of preparations;
- phase structures;
- stopping/absorption patterns;
- placements of cuts;
- random-bit implementations;
- clocks;
- register profiles;
- descriptions.

The three physical constructions in the manuscript do not share one fixed schedule. They are different architectures.

Therefore the statement

“every fixed physical profile has an all-auditor SOS converse”

does not by itself produce a lower bound on the union of all algorithms with N preparations and peak width W.

The paper has solved the inner optimization over transition probabilities of a declared architecture. It has not solved the outer optimization over architectures/schedules that defines the sample–memory complexity problem.

This is why the physical table remains only a table of attainable points.

# 7. The physical “converse procedure” has not yet produced a physical converse theorem

V23 says that the physical reset/collision protocols live in the same occupation class and that any certified dual applies to every auditor of the same declared full profile.

That is correct as an interface statement.

But no new nontrivial dual certificate is actually produced for the collision task.

The inherited physical knowledge remains, essentially:

- three explicit attainable sample/width points;
- a decision-row obstruction giving the lower bound three;
- the unrestricted clocked finite-horizon interval 3 <= W_phys <= 12.

V23 does not derive:

- a lower bound on width at N=399;
- a lower bound near N=320000;
- a lower bound on N at width 12;
- a function W(N);
- an asymptotic exponent;
- an integrated-state lower bound;
- a certificate excluding a qualitatively different schedule.

Thus the phrase “all-auditor converse procedure” should not be mistaken for “all-auditor physical lower bound.”

At the requested venue level, this difference is decisive.

# 8. The noisy exact theory is a real advance, but it remains narrow

The v23 noisy results are substantially better than the v22 erasure model.

Nevertheless the structural theorem landscape is still limited.

## 8.1 Bayesian result

The Bayesian interval theorem is for binary hidden parameter, conditionally independent finite reports, clocked finite profiles, and finite controlled experiment choices.

The interval structure is a classical one-dimensional likelihood-ratio phenomenon. The real v23 contribution is compatibility across the whole profile and the explicit reconstruction.

This is useful but not yet a broad new theory of finite-memory Bayesian experiments.

## 8.2 Minimax result

The arbitrary-horizon minimax recursion is restricted to:

- binary parameter;
- uncontrolled reports;
- conditional independence;
- every register of size one or two.

It is exact, but it is essentially an iteration in the Blackwell order of binary experiments through receiver curves.

The hard cases that the generic occupation theorem can encode but the structural theory does not solve include:

- registers of size K>=3 over long horizons;
- controlled/adaptive experiment selection in minimax form;
- multiple hypotheses;
- reused autonomous rows;
- compound/robust environment classes;
- nonproduct report processes.

A top-four paper should explain a phenomenon that persists when at least some of these restrictions are relaxed.

# 9. The three-report BSC frontier is elegant, but too small to carry the paper

Theorem thm:v23-bsc is the cleanest theorem in the new manuscript.

It gives a strict and exactly quantified memory effect in a genuinely noisy model. It separates Bayes and minimax values and exhibits the cost of an unpriced selector.

I regard this as the strongest new concrete result in v23.

But it is still a three-sample calculation with one nontrivial middle bottleneck.

The theorem does not determine:

- the n-report value for general width K;
- the asymptotic error exponent as n grows with fixed memory;
- the minimum memory needed for a target finite-horizon risk;
- controlled observation design;
- an autonomous analogue;
- a multi-hypothesis analogue;
- a profile scaling law.

The arbitrary-horizon receiver recursion is an exact representation, but it does not convert the three-report formula into a larger solved class.

For a specialized information/statistics venue, this exact example plus the finite-profile framework may be attractive. For Annals/Inventiones/JAMS/Acta, it is not enough.

# 10. The strict mixing gap is conceptually correct but must be positioned against prior finite-memory randomization results

The d(p)/6 gap is a useful warning: convexifying whole machines can introduce a persistent selector.

However finite-memory learning has a long literature on when randomization saves states and on differences between time-invariant and time-varying finite-memory devices. Hellman and Cover's program includes, among other items, “On Memory Saved by Randomization,” finite-time finite-memory testing, and time-invariant finite-memory hypothesis testing.

V23 cites the foundational Hellman–Cover papers, but the exact novelty boundary of the selector-cost theorem is not yet sharp enough.

The manuscript should answer a theorem-level question:

> Is the three-report gap a new incompatibility theorem, or a particularly transparent finite-horizon instance of an already-known randomization/memory phenomenon?

A supplied analytic proof does not settle priority.

# 11. A directly relevant 2026 literature item is missing from the current bibliography

As of the revision date, Managoli and Prabhakaran, “Memory Constrained Adversarial Hypothesis Testing,” arXiv:2605.12063 (May 2026), studies randomized time-invariant finite-state binary hypothesis testing and derives upper and lower bounds on minimax asymptotic error as a function of the number of states, with matching exponential behavior and exact matching for a class of problems.

This paper is not in the current v23 bibliography.

I am not claiming that it contains thm:v23-bsc, the finite full-profile occupation theorem, or the same finite-horizon objective. The models differ.

It is nevertheless directly relevant to the editorial claim that v23 provides a new general theory of memory-constrained minimax statistical testing. A top-four resubmission should compare:

- finite-horizon clocked versus time-invariant autonomous memory;
- exact finite-profile values versus asymptotic state exponents;
- adversarial/compound versus fixed product environments;
- the role of randomization.

The literature crosswalk should be updated accordingly.

# 12. The clocked/autonomous distinction is encoded, not solved

The earlier report asked for the clock to become part of theorem notation. V23 does this.

Theorem thm:v23-occupation can also impose shared-row equations for an autonomous controller. Thus the autonomous feasible set is, in principle, exactly encoded.

What is still missing is a substantive autonomous theorem.

The explicit Bayesian and minimax recursions are clocked. The three-report BSC theorem is clocked at its declared atomic update times. The long physical constructions exploit predetermined phases.

There is no autonomous analogue giving a closed or scaling-sharp frontier for a nontrivial noisy class.

Thus the earlier conceptual problem has not disappeared; it has been correctly typed.

That is progress in correctness, not yet a solution in mathematics.

# 13. The resource tuple is defined, but the joint resource problem is not classified

The new tuple records candidate preparations, target preparations, register profile, bit precision, description length, and clock/autonomous status.

This is the right bookkeeping.

Proposition thm/proposition v23-resource-order then observes that with finite caps the feasible class is finite, so one may maximize over it; with unrestricted real stochastic rows on a fixed finite architecture, the occupation/SOS theorem applies.

This is logically exact but mathematically close to tautological.

The difficult resource question is not whether a finite search space has a maximum.

It is to prove a nontrivial relation among the coordinates.

For example:

- how many states can be traded for one bit of transition precision?
- how does target calibration memory change the optimal candidate-sample count?
- how does description length constrain a long external clock?
- what is the Pareto boundary between N and W for a noisy family?
- when does autonomous reuse compensate for clock description?

V23 defines the coordinates but proves no general tradeoff theorem among them.

# 14. Calibration is now honestly priced, but the price is not optimized

The sampled-calibration theorem is a useful correction to the earlier implicit read-only calibration.

Its retained state cost (M+1)^K is, however, only one explicit construction. The paper does not show that retaining the complete counter vector is necessary, nor that the rho^{-2} sample rate and exponential-in-K state count form any joint optimum.

Therefore calibration has moved from “unpriced input” to “priced consumer.” It has not become a classified resource frontier.

This distinction should remain explicit.

# 15. The confidence theorem is exact only after a deliberate interface restriction

The confidence corollary is now matched for the declared Bernoulli interface.

That is a genuine improvement.

But the manuscript itself correctly states that a raw physical auditor with access to richer outputs is not lower-bounded by the coin-interface result. To transfer the lower bound to a physical subfamily, the relevant endpoint experiment must actually occur or be obtained by a certified limit.

Therefore the confidence theorem does not establish a physical confidence-memory frontier.

It establishes a solved downstream interface.

This is worth keeping, but it should not be counted twice: once as an exact noisy theorem and again as independent evidence that the physical resource theory is sharp.

# 16. The compact-family extension is a consistency statement, not an effective general theorem

Corollary cor:v23-compact is useful for typing continuous kernel families into the finite framework.

But its content is:

1. approximate the compact family by a finite net;
2. solve or upper-certify the finite net problem;
3. pay a telescoping total-variation error;
4. send net mesh, row precision, and certificate degree through suitable limits.

No effective net is guaranteed for an arbitrary presentation, and no uniform certificate degree is given.

Consequently the compact theorem does not provide a computable general invariant of compact statistical experiments.

It provides a mathematically valid approximation route when additional effective structure is supplied.

Again, this is a useful interface but not the missing top-four theorem.

# 17. The General Theta Foundations blueprint still asks for a different first foundation

The repository blueprint is unusually clear about what the first general foundation should accomplish.

Its recommended first-paper chain is:

real experiment
→ future predictive quotient
→ causal simulation
→ finite-resource attainable resolution.

It explicitly says that merely restating existing categorical/statistical comparison mechanisms and quantization identities is not enough, and asks for a substantive theorem deriving online finite-budget behavior from the original experiment with matching upper/lower control.

V23 has moved decisively toward a finite-protocol statistical resource paper:

- controller occupation arrays;
- semialgebraic feasibility;
- finite-memory binary decisions;
- finite precision/calibration;
- fixed-profile consumers.

That is a legitimate research direction.

It is not yet the same as the blueprint's first-principles predictive-quotient foundation.

The discrepancy creates an editorial choice.

### Option A: keep the “General Theta Foundations I” title

Then the paper should prove an essential theorem connecting the finite-resource structure to the predictive quotient / attained information layer and to a major downstream mathematical branch.

### Option B: judge v23 as a finite-resource paper

Then narrow the foundational narrative and title and let the occupation/noisy frontier mathematics stand on its own.

At present the paper wants the breadth of A and has mathematics closer to B.

# 18. The pipeline is still multiple-root

The v23 pipeline records this correctly.

The primary A2 geometric chain remains independent.

The original B4 aggregate remains unresolved because the normalized linear resolvent difference used historically fails on constants, and the new finite-state theorem does not establish the missing range, compactness, control-transfer, or corrector results.

The broad C2 strict-dual/form/rigidity/optional-projection aggregate is also not proved by the bounded Gaussian or finite-confidence consumers.

Therefore downstream program size cannot be used as evidence that thm:v23-occupation is foundationally necessary.

There is still no major program theorem for which the new compatible occupation machinery is an indispensable mathematical step.

This was Route D in the previous report. It remains open.

# 19. A2 independence remains a programmatic obstacle to the “first root” narrative

The repository does the right thing by not fabricating an arrow from GTF-I to A2.

But the consequence is unavoidable.

One of the program's strongest geometric strands does not consume the new theory.

For a paper called General Theta Foundations I at top-four level, I would expect one of two things:

- a theorem that actually subsumes and sharpens a major A2 statement after its hypotheses are verified; or
- an explicit multiple-root program architecture in which this paper is no longer presented as the universal first root.

V23 currently acknowledges the mathematical fact but has not fully adjusted the editorial narrative.

# 20. The unresolved B4 and C2 obligations remain important

The history audit correctly states that v23 does not repair them.

That is the right mathematical behavior.

It also means the large preserved kinetic/operator architecture cannot be counted as an application of the new theorem.

A 649-page preserved development with unresolved major historical branches is not evidence of closure. It is evidence of a large active program.

A top-four referee must judge the 96-page current article on the irreducible mathematics it proves now.

# 21. The paper remains too cumulative

The new central chain is now much clearer than in v22:

occupation realization
→ polynomial upper certificates
→ noisy binary recursions
→ exact three-report frontier
→ calibration and consumers.

That chain could support a focused paper.

Instead, the canonical article still includes approximately thirty-five inherited mathematical modules, historical organizing theorems, multiple physical/transport developments, residual relaxations, phase machines, and pipeline appendices.

The result is 96 pages, with a 649-page complete development.

Preservation is valuable in the repository. It is not automatically good journal architecture.

The current exposition makes it difficult to tell which lemmas are mathematically necessary for the new theorem and which are present because earlier rounds promised never to delete historical material.

A top-four submission should be an inevitable proof architecture, not a lossless repository snapshot.

I strongly recommend moving most inherited but nonessential developments to companions while keeping all repository history intact.

# 22. The diagnostics have reached diminishing returns

The v23 package advertises more than 260,000 finite checks, negative controls, theorem locations, source hashes, and preserved-page comparisons.

This is exemplary reproducibility practice.

It does not affect my recommendation.

No finite grid certifies a continuum stochastic theorem unless it is part of an analytic proof, and the manuscript itself says so. No source hash certifies novelty. No rendering comparison supplies a physical lower bound.

The next revision should not optimize the number of diagnostics.

The next revision needs a mathematical theorem.

# 23. What has replaced the old v22 central objection?

The sixth report said:

- the broad theorem was only an upper construction;
- the exact theorem was only an erasure–revelation model;
- there was no complete full-profile converse;
- the noisy class was missing.

V23 has answered those points.

The new central objection is more demanding:

> The exact general converse is generic semialgebraic completeness for a fixed finite architecture, while the non-generic statistical consequences extracted from it are still too narrow. The manuscript has not yet found the invariant, quantitative duality, or scaling law that makes the general encoding mathematically deep.

This is the key sentence for the next revision.

Do not answer it by adding another finite example.

Do not answer it by increasing the SOS degree in a computation.

Do not answer it by adding another pipeline consumer with no lower bound.

Extract structure.

# 24. Specific technical requests

These are secondary to the structural recommendation but should be addressed.

## 24.1 Rename the generic theorem more precisely

“Complete full-profile certificates” is logically defensible, but the surrounding prose should repeatedly say:

“complete semialgebraic certificate hierarchy for a fixed finite architecture.”

This prevents readers from hearing “complete sample–memory theory.”

## 24.2 Separate inner and outer optimization

Define explicitly:

- inner value: optimize stochastic row parameters on one schedule/architecture;
- outer value: optimize over all schedules/architectures satisfying a global resource budget.

Then state which theorem solves which level.

The physical sample–memory frontier is an outer problem.

## 24.3 Give quantitative information on the certificate hierarchy

Even a restricted theorem would help.

Examples:

- a degree bound on a tree protocol;
- finite convergence under a nondegeneracy condition;
- an explicit low-degree dual for binary registers;
- a bound depending on horizon and width;
- exactness of a first relaxation for a meaningful subclass.

Without this, the hierarchy is too black-box.

## 24.4 Extend the structural noisy theory beyond binary width two

A meaningful next target is one of:

- K-state minimax recursion for a nontrivial K>=3 class;
- controlled binary minimax observations;
- multi-hypothesis interval/polytope recursion;
- autonomous reused-row noisy testing;
- asymptotic fixed-memory error exponent.

## 24.5 Produce one actual physical upper certificate

Do not merely say that one exists eventually.

For a concrete physical sample count and width, give an explicit certified upper bound that rules out a better score for every auditor of that declared class.

Better still, optimize over a family of schedules and derive a true N–W lower curve.

## 24.6 Clarify whether the physical architecture class is exhaustive

If the headline physical quantity permits arbitrary finite causal auditors, explain how a fixed-schedule certificate contributes to a lower bound for that union.

If it does not, do not call the fixed-schedule result a physical frontier.

## 24.7 Give one autonomous exact theorem

Shared-row equations are not enough. Solve a nontrivial autonomous noisy class or obtain a scaling law.

## 24.8 Complete the current literature audit

At minimum add and compare the 2026 memory-constrained adversarial hypothesis-testing work, and expand the older finite-memory randomization literature around Hellman–Cover.

The Norberg proof-level gap should still be closed if reasonably possible.

## 24.9 Reduce the journal manuscript

Retain the full source history in the repository. That requirement is compatible with a much shorter canonical paper.

The main article should contain only modules that are actually used to prove or interpret the central theorem.

## 24.10 Keep the existing scope caveats

The manuscript is strongest when it says exactly what is not proved:

- no physical fixed-N Pareto law;
- no uniform SOS degree;
- no generic tournament optimality;
- no clocked/autonomous equality;
- no B4/C2 closure;
- no eleven-paper closure.

Do not remove these caveats in an attempt to strengthen the presentation.

# 25. What theorem would change my recommendation?

I would reconsider after one of the following.

## Route A: quantitative structural duality

Starting from the occupation equations, derive an explicit statistical dual or a bounded-degree hierarchy for a broad noisy class. The result should expose a recognizable invariant of the experiment and yield nontrivial lower bounds without solving a generic polynomial optimization problem from scratch.

## Route B: a scaling law for noisy finite memory

Solve a family whose horizon tends to infinity or whose register width varies. For example, obtain matching upper and lower error/resource scaling for an n-report noisy class under a full causal profile, preferably including an autonomous version.

This would turn the three-report example into the first member of a theory rather than the principal solved case.

## Route C: a physical sample–memory theorem

For the existing collision family, prove a nontrivial all-auditor lower bound coupling training preparations and persistent memory over a family of schedules, and match it by a construction up to constants or exponents.

An explicit certified physical Pareto segment would substantially change the editorial assessment.

## Route D: an essential downstream theorem

Prove a major A2, B4, C2, or other program theorem that genuinely uses the compatible-resource structure in an indispensable way.

This would give the word “Foundations” concrete force.

# 26. Editorial assessment by component

For clarity:

### Compatible occupation theorem
**Assessment:** correct-looking, useful, exact, but conceptually close to finite conditional-independence/semialgebraic controller formulations. Needs deeper consequences.

### Positivstellensatz certificate theorem
**Assessment:** correct-looking as a generic completeness application; not by itself a new statistical duality of top-four depth.

### Binary Bayesian recursion
**Assessment:** clean synthesis of likelihood-ratio quantization with whole-profile compatibility. Likely publishable mathematical content, but not enough alone.

### Binary-register minimax recursion
**Assessment:** more interesting structurally; exact for arbitrary finite horizons in its restricted class. Needs extension or asymptotic extraction.

### Three-report BSC frontier
**Assessment:** elegant and convincing local theorem. Too small to carry the full foundational claim.

### Calibration theorem
**Assessment:** operationally important accounting theorem; not a matched resource result.

### Physical consumer
**Assessment:** correct typing/interface advance; does not yet produce a physical lower frontier.

### Confidence consumer
**Assessment:** exact in a declared reduced interface; appropriately scoped; not a raw physical confidence lower bound.

### Pipeline
**Assessment:** honest, multiple-root, unresolved in B4/C2, A2 independent. Cannot currently amplify the paper's foundational significance.

# 27. Final assessment

V23 is the strongest version of this manuscript I have reviewed.

The authors did not evade the sixth report. They added exactly the kinds of objects that report requested: a full-profile all-machine characterization, a complete upper-certificate mechanism, an overlapping-noise exact class, explicit selector incompatibility, acquired calibration, and a fixed-profile bridge to the physical protocols.

That progress should be recognized.

But the new theory stops one level before the top-four contribution.

The occupation formulation tells us exactly which finite stochastic controllers are feasible.  
The Positivstellensatz tells us that strict scalar upper bounds are eventually certifiable.  
The binary recursions solve a narrow class.  
The three-report theorem gives one elegant exact frontier.  
The physical bridge says the same machinery can be applied.

What is still absent is the theorem that makes this architecture unavoidable:

- a quantitative invariant;
- a scaling-sharp converse;
- an explicit broad noisy dual;
- a physical Pareto law;
- or an indispensable downstream consequence.

The revision has moved from “portfolio without a converse” to “exact finite semialgebraic framework without a sufficiently deep extracted resource theorem.”

That is a substantial improvement. It is also still below the requested Annals/Inventiones/JAMS/Acta threshold.

**Recommendation: reject in the present form at the requested top-four general-mathematics standard.**

I would encourage a mathematically focused resubmission after the framework is used to prove one genuinely sharp theorem beyond fixed-architecture generic certification.

---

## Referee checklist

- Latest v23 referee-ready branch frozen at e926b783b643b3e7f275a18105528927b76cc97b.
- v23 working and referee-ready branches verified identical.
- v22 referee-ready head 88832f95b7dd0b8cc4a3061280a6e31f9fa67319 used as the actual predecessor.
- Sixth external report treated as the controlling prior critique.
- New occupation, SOS, binary noisy, three-report, resource-order, calibration, confidence, and physical-consumer modules inspected.
- No immediate one-line contradiction found in the new core during source-level spot checks.
- Old criticism “no general all-machine converse” explicitly withdrawn.
- Old criticism “exactness only in erasure–revelation” explicitly withdrawn.
- Fixed-architecture semialgebraic completeness distinguished from structural/statistical duality.
- Generic Putinar completeness distinguished from quantitative degree/rate information.
- Inner fixed-schedule optimization distinguished from outer schedule/architecture resource optimization.
- Physical all-auditor certificate procedure distinguished from an evaluated physical lower bound.
- Three physical resource rows still treated as attainable points, not a Pareto frontier.
- Binary noisy exact theorems credited and their actual restrictions recorded.
- Clocked and autonomous formulations distinguished; absence of a substantive autonomous exact noisy theorem noted.
- Calibration acquisition credited; lack of calibration-memory optimality noted.
- Confidence lower bound credited only at its declared Bernoulli interface.
- A2 primary geometric chain recognized as independent.
- Historical B4 aggregate recognized as unresolved.
- Broad C2 aggregate recognized as unresolved.
- Full eleven-component program not treated as closed.
- Müller–Montúfar semialgebraic POMDP prior art taken into account.
- Classical Hellman–Cover finite-memory testing/randomization program taken into account.
- 2026 Managoli–Prabhakaran memory-constrained adversarial testing flagged for the literature audit, without asserting theorem identity.
- Norberg proof-level comparison recognized as incomplete.
- Build/diagnostic evidence treated as reproducibility rather than proof or novelty.
- Principal remaining objection classified as insufficient quantitative/structural extraction from the exact finite semialgebraic framework, not as the obsolete lack of any converse.
