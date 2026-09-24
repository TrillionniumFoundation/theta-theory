# Sixth Independent External Harsh Referee Report

## General Theta Foundations I: Causal Continuation and Statistical Resource Frontiers — Revision v22

**Author:** Qian Qi  
**Repository:** TrillionniumFoundation/theta-theory  
**Reviewed branch:** `revision/general-theta-foundations-i-v22-referee-ready-2026-09-24`  
**Frozen reviewed branch head:** `88832f95b7dd0b8cc4a3061280a6e31f9fa67319`  
**Canonical source commit recorded by the referee package:** `15f083df26a268534fc5a8cd67717ac165430679`  
**Preserved v21 publication:** `bd5080f15d889ab074d73d4fc9963f83e5759036`  
**Controlling prior external report:** `reviews/general-theta-foundations-i-v20-external-harsh-top4-r5-2026-09-23/REFEREE_REPORT.md` at `14bcfe767940f8cbd196637049524d0b14eaee19`  
**Canonical v22 article:** 81 pages  
**Complete preserved development:** 553 pages, including 472 predecessor pages  
**Review date:** 24 September 2026  
**Requested standard:** Annals of Mathematics / Inventiones Mathematicae / Journal of the AMS / Acta Mathematica  
**Review type:** independent external-referee-style, pipeline-aware harsh review

## Provenance and scope of this report

I reviewed the latest referee-ready v22 source, not an older working revision. The two current v22 branches,
`revision/general-theta-foundations-i-v22-sample-memory-frontier-2026-09-24`
and
`revision/general-theta-foundations-i-v22-referee-ready-2026-09-24`,
are identical at the reviewed head. Relative to the preserved v21 referee-ready publication, v22 is three commits ahead.

For the new mathematical claims I read in particular:

- `sample-memory-frontier.tex`;
- `revelation-profiles.tex`;
- `active-transport.tex`;
- `physical-frontier.tex`;
- `finite-state-confidence.tex`;
- the revised introduction and main theorem;
- the v22 response to the previous referee;
- `RESOURCE_LEDGER.md`, `PROOF_STATUS.json`, `PIPELINE_STATUS.json`, `HISTORY_AUDIT.md`, and `LITERATURE_CROSSWALK.md`.

Because the claimed significance is programmatic, I also re-read the relevant inherited mechanisms rather than treating the v22 additions in isolation: the compatible multicut realization and full-profile value, the weighted and joint residual obstructions, the point-source and overlapping-retention exact examples, the physical full-profile material, the v21 organizing theorem, and the General Theta Foundations blueprint. I also used the repository's own current status of the independent A2 chain, the unresolved historical B4 aggregate, and the scoped C2 transport consumer in evaluating the claimed role of this paper in the eleven-component program.

I did **not** independently re-prove all 553 pages of preserved development. The source-preservation checks, finite diagnostic suites, negative controls, and successful LaTeX build are useful reproducibility evidence, but they are not a substitute for independent proof certification. The v22 package itself says this correctly.

# Recommendation

## Reject in the present form at the requested top-four general-mathematics standard

This conclusion should not be confused with the v20 report.

V22 materially changes the mathematical situation. It would now be inaccurate to summarize the paper as merely classifying a post-training response dictionary at one hand-chosen cut. The manuscript now contains a real full-schedule resource formalism, a finite-horizon response-cover realization with explicit preparation and width budgets, an exact all-stochastic-machine Bayes theorem for a multicut revelation model, an occupation-weighted retained-law perturbation bound, a third preparation/memory regime for the original collision experiment, and finite-state confidence amplification. Several specific requests of the v20 report have therefore been addressed.

The reason I still do not recommend the paper for Annals/Inventiones/JAMS/Acta is different and sharper:

> **V22 has assembled several correct-looking resource statements, but it still does not produce one general invariant, converse, duality, or matched theorem that explains the sample–memory frontier of a nontrivial statistical experiment across the whole causal schedule.**

The exactness and the generality remain split between different theorems.

- The response-cover theorem is broad but is only a constructive upper bound.
- The exact lower-and-upper frontier is for a specially engineered erasure–revelation model in which the unknown parameter is literally revealed on informative observations and the proof reduces to a last-revelation/top-prior-mass counting argument.
- The physical collision family has three attainable resource points but no fixed-sample frontier, no Pareto lower bound, and no exact peak width beyond the inherited interval (3le W_{2/5}^{m phys}le 12).
- The occupation theorem is a standard product-kernel telescoping estimate, useful but not a structural converse.
- The confidence theorem reduces a mean gap to a Bernoulli drift test, but it does not classify the memory required for confidence testing.

Thus Route II from the previous report is only partially completed. The manuscript now has a genuine resource theory **interface** and several nontrivial consumers; it still lacks the theorem that makes that interface mathematically unavoidable.

At a strong specialist venue, a carefully focused portion of this material could be defensible. At the requested top-four level, the paper still lacks the structural force, irreducible generality, and downstream necessity expected from a first “General Theta Foundations” paper.

# 1. What v22 genuinely fixes

The revision deserves precise credit before the remaining objections are stated.

1. **Preparation count is now in the theorem, not hidden upstream.**  
   Theorem `thm:v22-tournament` gives a finite-horizon realization with
   [
   N=n(K-1),qquad Wle 3dK(2m+1),
   ]
   while explicitly charging random-bit, event-retention, and validation cuts.

2. **The paper now exhibits an actual sample–width tradeoff rather than only an unrestricted finite-horizon width bound.**  
   The polynomial-horizon absorbing tournament and the inherited constant-width/exponential-horizon block construction are genuinely different attainable resource regimes.

3. **The exact multicut theorem is an optimization over all stochastic machines.**  
   Theorem `thm:v22-revelation` is not an exact-computation theorem for one fixed selector. Its upper bound conditions on the full parameter-independent random table and then applies each future bottleneck.

4. **Cut placement has an exact statistical effect in the solved revelation family.**  
   The inserted/tightened checkpoint formula is a real answer to one of the previous report's objections.

5. **The retained-law perturbation theorem cleanly separates active updates from padded preparations.**  
   This is conceptually useful, and the manuscript correctly refuses to transfer the active-count bound to the entire raw-data transcript.

6. **The physical application now has a third resource point.**  
   The ((320000,1604)) construction is not just a restatement of the ((399,40602)) or astronomically long width-12 constructions.

7. **Confidence is now treated as a separate objective.**  
   The paper no longer leaves the impression that a one-shot expected signed score is automatically a confidence certificate.

8. **The pipeline status remains unusually explicit.**  
   The manuscript does not falsely claim that A2 is derived from GTF-I, that B4 is closed, that the full C2 aggregate is proved, or that the entire eleven-paper program has been certified.

9. **The paper distinguishes clocked and autonomous implementations.**  
   It states explicit autonomous upper bounds rather than silently calling a time-dependent machine autonomous.

10. **The response letter does not falsely claim to have solved the physical fixed-(N) optimum.**  
    The exact erasure–revelation frontier and the collision resource table are kept separate.

These are substantial improvements. They should all survive any future revision.

# 2. Mathematical spot-check: I do not find a short counterexample to the new v22 core

My negative recommendation is not based on a discovered one-line contradiction in the new central lemmas. I record the spot-checks because the distinction matters.

## 2.1 Truncated absorbing comparison

For `lem:v22-walk`, the exponential-martingale argument for hitting the wrong boundary is consistent with
[
Pr(	ext{wrong boundary})le e^{-4	heta m}.
]
The nonabsorbed wrong-sign probability is controlled by the stated Hoeffding term
[
e^{-2n	heta^2}.
]
The exact expected absorption-time expression
[
mathbb E_u	au=
m,rac{	anh(m,operatorname{arctanh}x)}{x},
qquad x=2u-1,
]
with the (x=0) value (m^2), is consistent with the standard gambler's-ruin calculation. I did not find an immediate error in the drift and symmetry arguments.

## 2.2 Finite-horizon response-cover tournament

For `thm:v22-tournament`, the comparison coin
[
rac12+rac{q_j-q_i-h_j^{(r)}(w)+h_i^{(r)}(w)}4
]
is indeed in ([0,1]) and has mean
[
rac12+rac{g_j(b)-g_i(b)}4.
]
The stagewise (4	heta) loss and union bound lead to the advertised form of the score estimate. The separate (2ho) calibration loss and (2^{1-r}) response-rounding loss are consistent with the definitions. The width count is conservative but internally coherent.

The key limitation is not an obvious algebraic mistake; it is that this theorem is one-sided.

## 2.3 Exact revelation frontier

For `thm:v22-revelation`, conditioning on all private randomization to obtain a deterministic machine for the analysis is legitimate because the random table is independent of the unknown parameter and revelation indicators. Given the last revelation time (t), the terminal guess factors through every later charged state, so at most
[
k_t=min(M,K_t,ldots,K_n)
]
parameter values can be correctly represented on that pattern. The top-(k_t) prior-mass upper bound follows. The nested deterministic construction attains the same quantity.

I do not see an immediate flaw in
[
api_1+sum_t w_t P_{k_t}.
]

Again, the objection is the structural simplicity and limited scope of the model, not an apparent false formula.

## 2.4 Occupation-weighted transport

The expansion
[
mu P_1cdots P_T-mu Q_1cdots Q_T
=
sum_t
mu P_1cdots P_{t-1}(P_t-Q_t)Q_{t+1}cdots Q_T
]
gives the stated baseline-occupation TV bound by contraction. The asymmetry is explicit, and the reverse (Q)-weighted bound is also stated. The use in the absorbing tournament is compatible with the fact that after absorption the retained transition is an identity even though padded raw observations still occur.

## 2.5 Physical intermediate regime

The v22 physical proof uses the inherited three-event envelope
[
max(1-a-c,	frac12-a,	frac12-c)
]
and compares (a) and (c) to (1/2) through two absorbing walks. The numerical choice
[
	heta=1/200,quad m=400,quad n=160000
]
gives (4	heta m=2n	heta^2=8), so the displayed error estimate is consistent. I found no immediate arithmetic contradiction in the score (>2/5) conclusion.

## 2.6 Finite-state confidence amplification

For the additional coin
[
Pr(Z=1mid D)=rac12+rac{D-g/2}{4},
]
the null mean is (1/2-g/8) and the alternative mean is at least (1/2+g/8) when (glegamma). The reduction to the absorbing or block comparator is coherent under the stated independent-reset assumptions.

These checks are not a substitute for a line-by-line certification of every proof. They do show why the recommendation below is principally about mathematical scope, novelty, and theorem architecture rather than an obvious fatal local calculation.

# 3. The central v22 problem: exactness and generality live in different models

The paper's main theorem places four results next to one another:

1. a broad response-cover realization;
2. an exact Bayes frontier for revelation experiments;
3. a retained-kernel perturbation estimate;
4. a collision implementation plus confidence consumer.

The manuscript presents these as a statistical resource theory.

What is still missing is a theorem saying that these are manifestations of one mathematical object.

For the broad compact-image problem, define the whole-schedule value
[
mathsf V_{N,mathbf K}(B,Q)
]
or its inherited finite-environment analogue. V22 does not give:

- a dual formula for this value;
- a lower bound matched to the tournament construction;
- a characterization in terms of approximate continuation covers;
- a minimax modulus coupling (N) and the profile (mathbf K);
- a converse showing when the (3dK(2m+1)) scaling is necessary;
- a structural condition under which the response-cover envelope determines the full sample–memory frontier.

The exact theorem is instead proved for a different family with a very special observation channel.

This is the principal gap.

A top-four “foundation” would normally make the exact theorem and the general theorem meet. Here they pass beside one another.

# 4. The response-cover theorem gives an attainable curve, not a sample–memory theory

Theorem `thm:v22-tournament` is constructive and useful. But as a resource theorem it answers only:

> Given a strict finite response cover, how can one implement it with one explicit finite schedule and one explicit memory/error budget?

It does **not** answer:

> Among all causal procedures using (N) preparations and profile (mathbf K), what is the best achievable value, and what feature of (B) controls it?

The paper itself correctly calls its general bounds upper bounds. That qualification is mathematically honest, but editorially decisive.

The v21 point-source family does give a growing exact width example, and the overlapping-retention theorem gives a sharp storage profile for a canonical retention task. I have not ignored them. Their exactness, however, comes from especially transparent structures: one observation identifies a point source exactly, or independent labels must literally be held until later reporting. They do not supply a general converse for noisy statistical learning.

Likewise the v22 revelation model is sharper than those examples in its Bayes formulation, but the unknown parameter is still either revealed exactly or not revealed at all.

What remains absent is a genuinely noisy, overlapping statistical experiment in which the preparation–memory tradeoff is derived from the geometry of the experiment and is matched, even up to universal constants or exponents, by upper and lower bounds.

That is the kind of result I expected Route II to produce.

# 5. The exact revelation theorem is correct-looking but structurally too special for the advertised role

Theorem `thm:v22-revelation` is the strongest exact v22 statement. Its assumptions are also what make it easy to solve.

At each time the observation is either:

- the exact parameter value (artheta), or
- a common erasure symbol (*).

After the last revelation, all future reports are the same symbol for every parameter. Therefore every future state bottleneck is literally a bound on how many parameter labels can survive. For a known ordered prior, the Bayes upper bound is consequently the mass of the largest (k_t) atoms.

This is a clean theorem. It is also close to a cardinality argument once the last informative time is conditioned upon.

The nested attaining dictionaries are possible because “best (k) hypotheses” means the first (k) prior atoms for every (k). General losses, overlapping channels, state-dependent experiments, and nonnested optimal codebooks immediately destroy this special feature; the manuscript itself says so.

At the requested venue level, the next theorem should be the difficult one:

- a noisy channel with overlapping likelihoods;
- a nontrivial loss matrix;
- a controlled/adaptive experiment;
- a class in which optimal dictionaries are not automatically nested;
- or a dual/dynamic-programming characterization whose compatibility constraints are genuinely active.

Without such a result, the exact formula does not carry enough structural weight to serve as the missing general lower half of the resource theory.

# 6. The exact revelation frontier is exact only in the declared clocked model

This point deserves more prominence because “memory” is central to the title.

The state alphabet after report (t) is allowed to depend on (t), and the attaining transition rule uses the current time-dependent value (k_t). The external clock supplies (t) for free in the headline state profile.

The manuscript is transparent about this convention and gives autonomous conversions elsewhere. I am not accusing it of hiding the clock.

The issue is conceptual:

> an exact (K_t)-profile theorem for a time-inhomogeneous clocked controller is not an exact memory theorem for an autonomous machine.

If the controller must know the epoch internally, the state has to encode the clock or an equivalent phase variable. In state-count units this can multiply the alphabet by the number of epochs. In bit units it adds a logarithmic timing register. Either way, the exact frontier changes.

The same issue is dramatic in the width-12 physical construction: its tiny register is paired with an astronomical schedule. The paper correctly records that the autonomous implementation can be enormous.

Therefore the manuscript has not yet selected one canonical resource notion. It has a vector containing:

- preparation count;
- persistent labels;
- clock/schedule;
- finite transition description;
- fair-bit depth;
- calibration;
- simulation error.

That is a reasonable design. But the headline “exact frontier” optimizes only one projection of that vector while treating time dependence as an external resource.

For a top-four resource theory, I would want either:

1. an autonomous formulation as the primary invariant, with the clocked model as a corollary; or
2. a genuine multi-resource Pareto theorem in which clock/description and persistent memory are optimized jointly.

At present, the ability to trade memory for a very long clock is exhibited but not mathematically classified.

# 7. Description complexity and calibration are accounted for, but not optimized

The v22 resource ledger is careful. The tournament proof records a transition-description size and a fair-bit implementation. The calibration quantities (q_i) are dyadic and have an explicit error (ho).

This is good bookkeeping.

It is not yet a theorem about joint resource optimality.

In particular:

- the full-profile value (mathsf V_{N,mathbf K}) does not constrain transition-description length;
- the exact revelation frontier permits arbitrary time-dependent stochastic kernels in the upper-bound class;
- the general tournament assumes the calibration numbers (q_i) are supplied with the stated accuracy;
- if the target expectations themselves must be experimentally calibrated, the preparations needed to obtain those (q_i) are not derived by the theorem.

None of this invalidates the stated finite model. It does limit the claim that G3 has been solved in a general sense.

The foundation blueprint asks for preparation, persistent memory, precision/calibration, and simulation defect to be propagated through a genuine online experiment. V22 supplies a **conditional finite-model realization** of such a ledger. It does not yet prove a matched theorem for the joint vector of resources.

I recommend changing any program-status wording that suggests G3 itself is closed. “A finite-model G3 realization/consumer” would be accurate; “G3 solved” would not be.

# 8. The physical table is not a frontier

The paper gives the same physical task three attainable points:
[
(399,40602),qquad
(320000,1604),qquad
(12800cdot 2^{400},12),
]
where the coordinates are training preparations and peak labels in the declared clocked model.

This is useful evidence that preparation and memory can be traded.

It is not a Pareto frontier.

The paper proves neither:

- that any of these points is Pareto optimal;
- a lower bound on peak width at (N=399);
- a lower bound near (N=320000);
- a lower bound on (N) at width (12);
- an asymptotic law (W(N));
- a nontrivial integrated-memory lower bound;
- a bound for adaptive schedules matching the constructions.

The only unrestricted finite-schedule physical peak statement remains
[
3le W^{m phys}_{2/5}le 12.
]

That interval is valuable, but it also shows how far the current paper is from an exact physical resource theory.

The v20 report asked for an end-to-end physical lower bound or, alternatively, a genuinely general multicut theory. V22 chose the latter route. Because the general lower half is still absent, the unsolved physical frontier becomes important again: there is still no nontrivial noisy family where the new sample–memory upper curve is known to be close to optimal.

# 9. The collision experiment is not a corollary of the exact revelation frontier

A strong unified theory would make the physical theorem an instance of the exact/general abstract theorem after verifying hypotheses.

That does not happen here.

The revelation theorem is independent. The collision theorem uses its own three-event geometry, absorbing comparisons, inherited perturbation estimate, and physical target approximation. The revelation lower bound is explicitly not used as a collision lower bound.

This separation is honest.

It also means the main theorem is a portfolio rather than a hierarchy:

- general upper realization here;
- exact toy/special frontier there;
- physical construction elsewhere.

The paper still lacks the bridge theorem that explains why the same invariant controls all three.

# 10. Confidence amplification is operationally useful but does not solve confidence complexity

The v22 confidence theorem repairs an important semantic problem: expected score and statistical confidence are different objectives.

But the new theorem is essentially an amplifier:

1. assume a base audit with a uniform mean gap;
2. convert its output to a Bernoulli variable with drift;
3. use the same finite-state comparison machinery again.

This gives valid upper bounds.

There is no lower bound on the number of states or preparations required by **any** test achieving prescribed type-I/type-II error. There is no analogue of the exact revelation theorem for confidence testing. There is no proof that the three-state decision optimum survives the change of objective.

Therefore confidence is now a priced consumer, not a classified resource problem.

That is a meaningful improvement in correctness of interpretation; it is not, by itself, a top-four-level new pillar.

# 11. The occupation-weighted perturbation theorem is useful but mathematically standard

Theorem `thm:v22-active` is cleanly stated and appropriately scoped.

Its proof is the standard telescoping identity for a product of Markov kernels followed by TV contraction. The occupation weighting comes from integrating the rowwise defects against the baseline law.

The application to absorbed comparisons is sensible because the machine's retained transition becomes the identity after absorption.

The paper should continue to use this theorem. But it should not rely on it for novelty at the requested venue. Its importance is organizational: it makes the correct quantity visible and prevents raw-preparation counts from being confused with active retained-state perturbations.

The theorem does not establish:

- changing-filtration stability in general;
- a nonlinear robust-control principle;
- a singular perturbation theorem;
- a physical-process result when ignored observations alter future dynamics.

The manuscript already says these things. The editorial consequence is simply that this component cannot supply the missing structural depth.

# 12. The inherited multicut theory is real, but its sharpness problem remains

The v21 material is stronger than the old one-cut narrative and should be credited.

The compatible-realization theorem gives additive causal errors across a profile. The full-profile value
[
V_{N,mathbf K}(B,G)
]
is attained in finite models, is monotone in the profile, and admits finite dyadic/net approximations. The composition proposition correctly prices simulator/controller product states and schedule refinements.

The weighted and joint residual theorems also provide all-stochastic lower-bound templates.

But these results stop short of a sharp theory:

- the compatible continuation theorem is a realization certificate, not an optimality characterization;
- the finite grid/net theorem is a compactness/computability sandwich, not a structural value formula;
- the residual LP is a lower-bound relaxation, not a complete dual;
- the physical specialization of the residual LP does not produce a nontrivial adaptive physical peak lower bound;
- the point-source and interval examples have exactness because their information structure is unusually rigid.

V22 does not close this gap. It adds another solvable rigid family.

Thus the central mathematical opportunity is now very clear: **derive a complete or scaling-sharp dual/converse for a genuinely noisy profile-constrained statistical experiment.**

# 13. Route II from the v20 report is only partially completed

The previous report proposed:

> Develop an invariant that tracks approximate continuation classes across an entire causal schedule, with explicit sample-memory tradeoffs, persistent-randomness accounting, and composition laws. Prove upper and lower bounds for a nontrivial class of compact behavior images and recover the collision theorem as a true corollary.

V21 and v22 collectively now provide much of the first sentence:

- full profiles;
- compatible continuations;
- clock and randomization accounting;
- composition;
- finite-horizon upper bounds;
- confidence consumers.

What remains missing is the second sentence in its difficult form.

The exact lower-and-upper theorem is not for a broad class of compact behavior images. It is for an erasure–revelation experiment whose informative observation equals the parameter itself.

The collision theorem is not recovered as a corollary of that exact theory.

Therefore it would be premature for the response letter to describe Route II as complete. It has become a serious research direction, but its main converse theorem is still open.

# 14. The General Theta Foundations blueprint sets a stronger target than v22 achieves

The foundation blueprint distinguishes several layers and explicitly warns against declaring a universal memory/error law without matching lower bounds and real experimental hypotheses.

Its G3 objective is not merely to list four resource parameters. It asks for a unified resource–precision–statistical-error theorem in a genuinely online experiment, with quantities defined in one appropriate feature metric and with the difficult lower-bound interactions handled rather than assumed away.

V22 advances G3 in an important way:

- finite preparation count;
- persistent finite labels;
- dyadic implementation precision;
- calibration error;
- simulation/source perturbation;
- confidence-level output.

But the theorem does not yet provide a **unified matched frontier** for these quantities.

The blueprint's proposed first foundation also centers on causal experiments, predictive quotients, executable reduction, and attainable resolution. V22's dominant new material is a finite-state statistical resource layer. The broader predictive-quotient architecture appears mainly through inherited modules and program maps.

This is not necessarily a defect if the paper is retitled as the statistical-resource branch. It is a problem if the paper's significance depends on being the universal first-principles root of the entire program.

# 15. The pipeline remains multiple-root and contains known unresolved obligations

The repository's current pipeline status is commendably honest.

It says, in effect:

- the primary A2 geometric chain is independent;
- the historical B4 normalized-resolvent aggregate is not certified;
- the broader C2 rigidity aggregate is not certified;
- the finite Gaussian/entropic consumer is scoped;
- the full eleven-component program is not closed.

I agree.

This has a direct consequence for the title “General Theta Foundations I.”

The paper cannot obtain top-four-level significance merely by standing at the front of the repository. The actual dependency graph still has multiple roots. A2 does not essentially consume GTF-I. B4 remains a blocker. C2 has a bounded consumer rather than its full historical theorem.

There are two coherent programmatic choices:

### A. Make GTF-I genuinely foundational

Prove a theorem that a major downstream branch needs in an essential way and verify its hypotheses in that branch.

### B. Present GTF-I as one foundation module

Then narrow the title and narrative to the causal/statistical resource program and judge the paper on that mathematics alone.

V22 is still mathematically closer to B.

# 16. The unresolved B4 defect remains important to any global program claim

The history audit correctly records that the historical normalized linear difference identity fails on nonzero constants and that the current paper does not use it to claim range, compactness, comparison, or corrector results.

This is the right scholarly response.

But it also means the broader kinetic branch is not downstream evidence for the foundational theorem. It remains an unresolved mathematical target.

No amount of source preservation or resource bookkeeping can substitute for that missing theorem.

# 17. A2 independence remains decisive

The paper correctly refuses to manufacture an artificial dependency from the primary A2 geometric chain.

That is preferable to a false unification.

But it means that one of the program's most substantial geometric roots still does not require the new sample–memory theory.

For a top-four first-foundation narrative, I would expect at least one major nontrivial A2 result to be re-derived or sharpened through a GTF theorem in a way that is not merely notational. Alternatively, the program should openly adopt a multiple-root architecture and stop drawing significance from a single-root story.

# 18. The closest literature boundary is still not settled enough for this venue

The v22 literature crosswalk improves the Weisshaupt comparison and is appropriately cautious about Norberg.

The unresolved point remains serious:

- the original Norberg proof-level comparison is incomplete;
- the priority status of the exact revelation specialization has not been exhaustively checked;
- the ingredients overlap with classical finite-memory testing, finite-state learning, automata/residual methods, quantization, and filtered comparison of experiments.

For a specialist paper, a careful but incomplete historical comparison can sometimes be acceptable.

For a paper claiming a new general foundation at the Annals/Inventiones/JAMS/Acta level, the novelty boundary must be theorem-level clear.

In particular, the final literature section should explain precisely which theorem is not implied by:

- classical finite-memory hypothesis testing;
- time-dependent finite statistics;
- filtered Blackwell/Le Cam comparison;
- residual/Nerode state minimization;
- finite-alphabet quantized inference;
- standard Markov-kernel perturbation/telescoping.

The current paper often says correctly that an ingredient is classical, but the **joint mathematical increment** is still described more clearly in engineering/resource-language than in an impossibility/equivalence theorem that isolates new mathematics.

# 19. The main article is still a cumulative repository artifact rather than one inevitable theorem chain

The canonical article is now 81 pages. It contains a large inherited architecture:

- deficiency;
- continuation theory;
- operational precision;
- multicut resources;
- clocked learning;
- new sample–memory realization;
- exact revelation;
- active transport;
- weighted/joint residuals;
- streaming/nonlinear/adaptive testing;
- physical complexity;
- microscopic and Gaussian transport;
- confidence;
- compressed certificates;
- phase machines;
- historical organizing theorems;
- dependency maps.

The complete development is 553 pages.

Preservation is useful for the repository. It is not a journal-design principle.

The v22 genuinely new mathematical core is concentrated in a handful of short modules. The article should either:

1. strengthen those modules until the inherited machinery becomes a necessary proof chain; or
2. split the material into a focused paper on causal statistical resource frontiers and companions for transport/physical applications/history.

At present, the reader has to carry a large amount of historical machinery to reach results whose sharpest new exact theorem is a relatively elementary revelation model.

That imbalance works against the requested venue.

# 20. Reproducibility evidence is excellent, but it has reached diminishing returns

The package records hundreds of thousands of finite checks, negative controls, source hashes, theorem locations, and page-preservation comparisons.

This is good practice.

It should no longer be a major revision axis.

The next meaningful progress will not come from:

- another larger diagnostic count;
- another branch generation;
- another exact source-preservation manifest;
- another small improvement of the 320000/1604 constants.

The mathematical bottleneck is a converse/frontier theorem.

The report would be unchanged if the diagnostic count doubled tomorrow.

# 21. Technical requests for any next revision

These are secondary to the structural objections, but they matter.

## 21.1 Promote the clock model into theorem notation

Every headline frontier should visibly indicate whether it is:

- externally clocked/time-inhomogeneous;
- autonomous;
- or part of a multi-resource vector with clock length.

Do not leave this only in prose after the theorem.

## 21.2 Define the resource partial order explicitly

The paper now has preparations, state width, bit width, clock length, description length, random-bit depth, calibration precision, and transport error. State exactly when one implementation dominates another.

Then say which Pareto boundary is actually proved.

## 21.3 Separate calibration input from calibration acquisition

If (q_i) are exogenously known approximations of target response means, state that as data. If they must be learned from physical target preparations, charge those preparations and prove the corresponding theorem.

## 21.4 Give a nontrivial lower bound paired with `thm:v22-tournament`

Even a scaling-sharp lower bound on a restricted but noisy class would materially improve the paper. The lower bound should constrain all stochastic causal machines, not exact implementations of a chosen selector.

## 21.5 Strengthen the revelation class

A meaningful next step would permit overlapping noisy reports or a general loss matrix so that the compatibility problem cannot be solved by nested top-prior sets automatically.

## 21.6 Turn the physical resource table into a theorem about a frontier

For example, prove a lower bound (W(N)) on an interval of (N), or a lower bound on (N) at fixed (W), for the same collision task and all admissible auditors.

## 21.7 Keep the active transport theorem scoped

Do not present it as changing-filtration or general physical-process stability. Its current caveat is correct.

## 21.8 Do not call inherited exact-computation residual profiles statistical frontiers

The source mostly avoids this mistake. Continue to distinguish exact function computation, Bayes regret, minimax score, and confidence testing.

## 21.9 Complete the literature audit before a top-four resubmission

The Norberg gap and the priority boundary around the revelation model should be closed as far as reasonably possible.

## 21.10 Reduce the canonical article

Historical preservation can remain in the repository and companion material. The journal manuscript should contain only the dependencies needed to prove and interpret its main theorem.

# 22. What theorem would change my recommendation?

I would not change the recommendation because of another local construction. I would reconsider after one of the following.

## Route A: a genuine general converse for the full-profile value

Define a class of noisy finite experiments broad enough to include a nontrivial physical or geometric example and prove upper and lower bounds for
[
V_{N,mathbf K}(B,G)
]
in terms of one continuation/resource invariant, with matching scaling in (N), (mathbf K), and approximation error.

A complete dual formula would be especially compelling.

## Route B: an exact or scaling-matched physical sample–memory frontier

For the existing collision family, prove a nontrivial all-auditor lower bound coupling preparations and peak memory, and match it by a construction up to constants or exponents.

This would transform the current three resource points into a physical complexity theorem.

## Route C: a genuinely nontrivial exact multicut statistical class

Extend the revelation theorem to overlapping noisy channels, nonnested optimal codebooks, or controlled observation kernels, and solve the compatibility problem rather than assuming the structure that trivializes it.

Then recover at least one existing theta model as a theorem-level corollary.

## Route D: an essential downstream consumer

Prove a major A2, B4, C2, or other program theorem whose proof genuinely uses the GTF causal/resource structure and cannot be replaced by a routine direct argument.

This would give the “Foundations” title concrete mathematical force.

# 23. Final assessment

V22 is a serious improvement over v20.

It is now incorrect to say that the manuscript only studies a final decision cut with unlimited upstream memory. The inherited v21 multicut formalism and the new v22 finite-horizon tournament really do price training cuts. The exact revelation theorem really does optimize over all stochastic machines in its declared model. The confidence and active-transport modules repair real operational ambiguities.

The new question is whether these advances have crossed the threshold from **a collection of explicit finite-resource constructions and examples** to **a general mathematical theory of causal statistical resource frontiers**.

In my judgment, they have not.

The most general theorem is not sharp.  
The sharpest theorem is not general.  
The physical theorem is not a frontier.  
The clocked exactness is not autonomous exactness.  
The pipeline is not single-root.  
The closest literature boundary is still incomplete.  
The 81-page architecture is broader than the new irreducible mathematics.

This is precisely the kind of manuscript for which another round of local repairs can make the package larger without changing the editorial conclusion. The next revision must add a theorem that links the existing pieces at the level of necessity, not another implementation point.

**Recommendation:** **reject in the present form at the requested Annals/Inventiones/JAMS/Acta standard.** A fundamentally strengthened resubmission should center on a matched sample–memory converse/frontier for a genuinely noisy class, an all-auditor physical Pareto law, or an essential downstream theorem. Until then, I would describe the work as a sophisticated causal finite-resource framework with several correct-looking exact and constructive examples, not yet a top-four general-mathematics foundation.

---

## Referee checklist

- Latest v22 referee-ready branch and frozen head explicitly identified.
- v22 work branch and referee-ready branch verified identical.
- v21 publication treated as the actual baseline.
- v20 fifth external report used as the prior controlling critique.
- New v22 tournament, revelation, active-transport, physical, and confidence modules inspected.
- No immediate one-line contradiction found in the principal new claims during source-level spot-check.
- Full-schedule resource accounting credited as a genuine advance.
- Exact revelation theorem recognized as all-stochastic within its stated model.
- General response-cover theorem recognized as an upper realization, not a matched frontier.
- Physical ((N,W)) rows recognized as attainable points, not a Pareto frontier.
- External-clock dependence distinguished from autonomous memory.
- Description/calibration bookkeeping distinguished from joint resource optimality.
- Confidence upper bounds distinguished from confidence-memory optimality.
- Occupation-weighted transport recognized as a scoped retained-law theorem.
- v21 point-source and overlapping-retention exact families taken into account rather than misattributed to v22.
- Weighted/joint residual bounds treated as lower-bound templates, not a complete dual.
- A2 primary chain recognized as independent.
- Historical B4 aggregate recognized as unresolved.
- Broad C2 aggregate not treated as closed.
- Full eleven-component pipeline not treated as certified.
- Norberg proof-level literature comparison recognized as incomplete.
- Build/diagnostic evidence treated as reproducibility, not proof.
- Principal remaining objection classified as lack of a general matched converse/frontier and foundational necessity, not as the obsolete “single post-training cut only” objection.
