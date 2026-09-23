# Response to the external v19 round-four report

## Frozen inputs and the substantive change

Controlling report: `reviews/general-theta-foundations-i-v19-external-harsh-top4-r4-2026-09-23/REFEREE_REPORT.md`, blob `3c7014121e8490e5883c6ab8bdad530e8b52c853`, at review commit `01679f4eac720dfd256594333e577b5db8145246`.

Reviewed manuscript: v19 at `9cf70fe7c8aa289d1be26934451e223364aa06ef`. All previous revision and review branches remain unchanged.

The decisive objection was that the continuation lower bound and the physical upper construction did not classify the same task. V20 supplies a general operational decision-continuation spectrum, computes its one-state and two-state values on the physical product image, and proves that **exactly three retained states at the specified training--validation cut are necessary and sufficient for uniform physical expected score greater than 2/5**. The impossibility statement quantifies over every finite-training auditor at this interface, including feedback-row selection. The attaining rule is physically executable, with an exact simultaneous trial-cut residual profile and a fully charged bit-level implementation.

This is not a claim that the minimum peak memory over every successful algorithm is sixteen bits. The task-level optimum is at the named cut. The full profile is optimal for exact computation of the specified audit rule. This distinction is part of the theorem statement and proof, not a qualification hidden in a build receipt.

Compiled numbers and pages are generated in `evidence/THEOREM_LOCATIONS.json`. Stable theorem labels are used below.

## Sections 1–3: organizing force, significance, and matched lower/upper statements

The former binary calibration is no longer used as the purported lower-bound branch of the physical certificate. The new organizing theorem is `thm:v20-main`.

`thm:v20-spectrum` defines the intrinsic K-response envelope on the original compact behavior image and proves:

- every K-state continuation after training has worst-case score at most that envelope, whatever finite upstream machine produced the state;
- empirical selection among its K responses approaches the envelope uniformly, with deficit bounded by both sqrt((d-1)/n) and sqrt(2 log(2K)/n);
- the minimum K for a strict score is the least size of a cover by positive-discrepancy response half-spaces;
- the spectrum has a uniform total-variation perturbation bound.

`cor:v20-rows` proves the same classification for the original row-indexed reset interface, with arbitrary row–event continuations and the finite-sample dimension D=sum_j(d_j-1). The upper bound remains valid for adaptive finite training schedules.

`thm:v20-two` computes the ideal physical values V1=1/8 and V2=3/8. Its three-candidate inequality is a task-level obstruction, not a statement about a chosen counter. `lem:v20-feedback` proves that choosing other feedback rows cannot evade the obstruction: an admissible private subfamily realizes every row as a pushforward of its all-on marked law, so every row–event continuation pulls back to a response on that same law. This covers mark-dependent events and stochastic transitions.

`lem:v20-envelope`, `lem:v20-majority`, and `thm:v20-physical` give the upper construction on the same family and same score. The physical perturbation is less than 1/300; hence two states have score less than 3/8+1/300<2/5, whereas the three-state construction has score greater than 0.4032891. The strict comparison is proved with rational inequalities, not decimal sampling.

The new result combines aspects of the report's Routes I and II: an operational classification at a specified cut for general compact behavior images, followed by a matching physical task theorem. It does not claim the stronger unproved statement that a single invariant now solves all simultaneous approximate-width tradeoffs.

## Section 4 and request 19.1: weighted residual obstruction and finite-valued decisions

`thm:v20-weighted` extends exact residual-profile minimality to any finite terminal alphabet in the stochastic implementation model. Distinct exact residuals have disjoint positive state supports; quotient shifts attain all cut widths simultaneously.

For approximate computation, the theorem assigns weights to distinguishing-suffix edges, subject to capacities supplied by the actual word weights. The error is bounded below by the minimum monochromatic edge weight of a K-labeling. The key stochastic step is proved: the sum of weighted state overlaps is concave on the product of encoding simplexes, so its minimum is attained at a deterministic vertex. No general deterministic reduction of an optimal randomized auditor is assumed.

The two-word, one-state example has exact weighted error min(p,1-p), for every 0<p<1. With unit word weights it gives exact total error one, attaining the earlier (r-K)/(r-1) bound at r=2, K=1. `cor:v20-bayes` converts the weighted obstruction into finite-action audit regret under arbitrary priors and explicit Bayes margins. The prior is used only as a lower-bound device; it is not granted to a private candidate.

## Section 5 and request 19.2: odd-sample uniqueness and even ties

The paragraph following `cor:v20-bayes` makes the equality argument explicit. When every word has a strictly positive gap between the best and second-best action, attaining the Bayes value forces zero error on every word. This is the step needed in the odd full-support Bernoulli experiment.

At even sample size, balanced-count words have zero likelihood gap. Different outputs on those words can attain the same value. The article therefore does not identify value attainment with exact computation of one prescribed tie rule, nor transplant the odd-sample profile to that setting without a separate argument.

The complete prior binary theorem and proof remain in `streaming-complexity.tex` unchanged.

## Sections 6–7 and requests 19.3–19.4: a same-task lower bound and an actual state machine

The former nineteen-bit bound remains explicitly an implementation upper bound. Its full proof is unchanged in `compressed-certificate.tex`. The added `phase-machines.tex` gives its exact phase-state transitions: partial transcript buffers, clipped updates, all four threshold comparisons including ties, event formation, candidate validation, target validation and final score. It proves the 504,008 maximum by phase-indexed injections into one alphabet, not a vague appeal to label reuse.

The new rule is different: count 00 and 11 over 399 informative samples, select the opposite singleton event if a strict sample majority occurs, and otherwise select the diagonal event. Its expected regret is controlled by the elementary odd-binomial tail bound proved in `lem:v20-majority`. One of the two true probabilities is at most 1/4, so only one term pays the worst threshold-regret constant.

`thm:v20-profile` computes the exact residual keys. The two profile pieces are binom(t+2,2) for t<200 and binom(402-t,2) for t>=200, through t=399. They peak at 20,301 at t=200. Distinct residuals remain distinct for the complete signed-score function: a common validation suffix separates any two different event labels. Thus this is not merely an event-name encoding count.

The deterministic quotient transition table is defined by lexicographic representatives, with representative independence proved through residual shifts. A first-bit buffer gives at most 40,602 states. Marks are discarded during training. Event and candidate-score registers are retained during validation; their states are counted. The free clock carries phase and trial number, never data-dependent history. The optional 400th training trial is ignored; the rule consequently fits the same 402-trial budget as v19, or can be run with 401 total trials by omitting that redundant slot.

The new lower bound applies to every auditor at the designated cut. The 20,301 profile is exact for this particular rule. The paper does not confuse these two quantifier orders.

## Sections 8–9 and request 19.5: explicit change-of-measure and coupling lemmas

The inherited bounded global entropic theorem remains unchanged and is preceded by three fully proved lemmas in `transport-versions.tex`:

1. `lem:v20-tilt`: on the observation sigma-field F, dP_F/dP^g_F = E_{P^g}[c/g | F] = c/E_P[g | F], with both density directions bounded by exp(2 gamma). This justifies returning the integrated coefficient estimate to the original observation law.
2. `lem:v20-diagonal`: the common-path subprobability measure of any coupling is dominated by both marginals. This is the precise reason a same-path marginal estimate bounds the equality-event contribution.
3. `lem:v20-integrals`: Borel continuous-path versions of the marginal stochastic integrals can be defined through their own BSDE identities and pulled back to an arbitrary coupling. No innovation is declared Brownian in the joined filtration.

The text names the use of each lemma in `thm:v19-global`. Bounded signals, common preparation, fixed positive noise, and the actual observation-measurable terminal certainty equivalent remain explicit mathematical hypotheses. The physical theorem discharges them on its moving-collision family.

## Sections 10–11: genuine physical mechanism and the no-collision control

The manuscript retains two labeled spheres, one nongrazing collision, and the full-dimensional prepared impact–mark law. The collision transduces a prepared impact variable into the transverse detector signal. Changing contact distance changes the collision time and the actual microscopic trajectory.

The no-collision result d<=2/5 and vanishing private/hidden/visible deficiencies appears in the organizing theorem and the physical composition theorem. It is not relegated to repository metadata. No many-particle limit is inferred from a two-particle estimate.

## Sections 12–15 and request 19.6: the eleven-paper program and historical proof obligations

The article contains a one-page namespaced program map in `sec:v20-program`. The exact inherited machine-readable graph is retained in `PIPELINE_STATUS.json`; current theorem dependencies are additional typed edges.

The original B4 and C2 Round17 blobs were read directly at the recorded frozen commit. The B4 displayed normalized difference identity fails on constants and is not used here. We do not replace it by a linear resolvent formula and call the nonlinear kinetic theorem repaired. `HISTORY_AUDIT.md` records the correctly typed nonlinear resolvent identity that a separate repair would have to establish from an already justified graph/range theorem; it is not credited as a physical B4 closure.

The current C2 consumer is the proved bounded common-preparation Gaussian/entropic chain. The historical strict-dual, form-response, rigidity and aggregate claims are not certified by it. Their source files and targets remain intact.

The primary A2 geometric chain remains independent. We do not invent a dependency to make an eleven-paper linear narrative appear complete. The foundational program is retained with its actual proof graph; GTF-I supplies the causal comparison/certification root and a concrete physical consumer. This is a theorem-level architectural statement, not a change in the program's research ambition.

## Section 16: literature crosswalk and what remains unverified

`LITERATURE_CROSSWALK.md` gives all eight requested comparison axes for the current theorem: deficiency, filtered operator class, adaptation, persistent-state accounting, private/visible randomization, convexification, necessity/sufficiency, and proof mechanism. It distinguishes the current claims from classical positive-cone realization and deterministic residual minimization.

The original Norberg full text was not obtained from the publisher or the located library record. Consequently we cannot honestly fill the Norberg theorem/proof column with verified theorem numbers or absence claims. This publication-level task remains explicitly unverified. The response is not to assert priority on the basis of an abstract, or to label the gap closed. The current paper makes its new contribution through explicit statements and proofs without claiming that filtration or randomization comparison itself originates here.

## Sections 17–18: reproduction and article structure

The canonical article is a complete integrated English manuscript, not a short addendum replacing the old paper. Sixteen mathematical input modules are inherited byte for byte. All predecessor pages are preserved in the complete-development companion and checked individually for text and raster equality. The canonical dependency table connects the new response spectrum, same-family physical lower bound, three-event construction, exact residual profile and microscopic transport.

Diagnostics exhaust small finite input words, verify residual quotients and shifts, check exact response inequalities and rational margins, and preserve the former clipping map. Normal and optimized Python runs must agree, and deliberately corrupted variants must fail. These are supplementary checks, not proof certification and not evidence of journal acceptance.

## Sections 19–21: disposition and next independent review

Every request 19.1–19.6 has a corresponding manuscript statement, proof, implementation table, or program map as detailed above. The substantive structural response is a matched **decision-cut** classification for the exact physical score, with a general operational spectrum and full implementation profile. The stronger optimization of peak memory across all possible successful rules is not claimed. The original Norberg proof-level comparison remains unverified. All new analytic arguments await independent scrutiny.

The next referee can focus on the three-candidate response obstruction, the feedback completion, the odd-binomial regret estimate, the residual-key count, and the interface quantifiers. These are the mathematical steps on which the new bridge stands; the build system cannot settle them.
