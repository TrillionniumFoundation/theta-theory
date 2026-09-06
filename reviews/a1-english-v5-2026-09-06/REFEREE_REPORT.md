# Referee report — A1, English revision 5

**Manuscript:** *Finite-Horizon Information States of Calibrated Experiments: Realization, memory–decision laws, and mechanical response*  
**Author named in the submission:** Qian Qi  
**Review date:** 6 September 2026  
**Requested standard:** Annals of Mathematics / Inventiones Mathematicae / Journal of the American Mathematical Society / Acta Mathematica  
**Recommendation:** **REJECT at the requested general-mathematics-journal level in its present form.**

This is an AI-assisted referee-style assessment requested by the repository owner, not a review commissioned by any of the named journals. Independent checking here means fresh examination of the source and independently written finite diagnostics, not an independent human appointment or formal proof verification. The recommendation concerns the submitted manuscript, not the viability of the research program.

## 1. Exact submission and scope

```
repository:        TrillionniumFoundation/theta-theory
revision branch:   revision/a1-english-v5-finite-horizon-decision-law-2026-09-06
submission commit: 20a26285a26cb468206b771c38166fd216283af0
repository tree:   eeeff3c9ab90b5421210f8a12bafa5a1a6a2226f
principal source:  papers/A1-english-v5/main.tex
manuscript tree:   6e96d9e79bdc62bfb221500796400156dda59315
parent review:     58796c768d14c280020d05916feb946db8fb25ab
prior v4 source:   e4b10bf7acebf38dbcfb466b3ee4cf30bb77b381
```

The submission was committed at **2026-09-06 00:03:36 UTC**, or **08:03:36 Singapore time**. Its branch head was checked again before publishing this review and remained the pinned commit. The two earlier, similarly named v4 revision branches are not substituted for this v5 source.

I read `main.tex`, all sixteen numbered section files, both included appendices, and `references.tex`; also the README, response, proof ledger, historical-derivation map, source manifest, and current author diagnostic program. I consulted the controlling v4 report for its mathematical assessment, binary ablation, rank-dependent extension, full-horizon arc argument, and stated requirements. The present assessment covers all **34 principal labels**, with individual dispositions in [CLAIM_AUDIT.md](CLAIM_AUDIT.md).

I did not freshly audit the entire preserved foundation companion, every historical branch, or all eleven papers. Historical preservation is not fresh approval. I did not compile the manuscript, inspect a PDF, run the author’s 50-check program, or rerun the previous referee’s 39-check program. I instead wrote and executed a separate **58-check exact-arithmetic program**: [referee_checks.py](referee_checks.py), with [DIAGNOSTICS.json](DIAGNOSTICS.json). Its general-theorem limitations are stated below. Source identities and execution scope are recorded in [REVIEW_MANIFEST.json](REVIEW_MANIFEST.json).

All manuscript anchors in this report refer to files under `papers/A1-english-v5/` at the pinned submission. Labels, rather than potentially shifting compiled theorem numbers, are the controlling references. The review branch starts from the submission and adds review files only.

## 2. Executive judgment

**The revision has supplied a genuine state–decision connection missing from v4. Nevertheless, the resulting central theorem does not, in my judgment, establish an advance of the depth and consequence required by the requested journals.** These conclusions must be kept separate.

The new finite-horizon quotient is not merely the old full-likelihood count under a new name. The distinction between `qn` and `q min(n,m)` is correctly formulated for the specified observable-future task. The finite-symbol coding theorem includes discontinuous encoders and the declared independent randomization. Its unconditional counterpart uses one fixed exploration experiment and retains the probability of the all-failure prefix. The sign-erasure comparison changes the exponent under the declared common command convention. The separate two-cartridge comparison really has positive information value without an acceptance charge. These are substantive responses, not nonexistent additions that a hostile report may ignore.

**I found no new blocking counterexample to the principal mathematical statements under their printed model restrictions and the future-only common-continuation interpretation of operational equivalence.** This is a source-level assessment, not a guarantee that no error remains. In particular, the review does not reject because `q min(n,m)` is false, because all-failure histories were silently discarded, because the random-coding lower bound assumes continuous encoders, or because the zero-cost gain is actually the old cost-saving gap.

The decisive issue is what remains after the standard mechanisms are separated from the application. The central calculation uses an open family in the entire univariate polynomial space, a polynomial-product differential, a positive Gram pairing between two nested polynomial spaces, and squared-error quantization on a finite-dimensional prediction set. The calibrated detector supplies a particularly transparent full-rank matrix. This is a coherent and useful construction. The manuscript does not yet show a sufficiently substantial structural obstruction, classification, or operational consequence beyond that saturated finite-dimensional setting.

There are also important limits to the performance narrative. The bit theorem is a **single-checkpoint, fixed-horizon, high-resolution coding theorem**, not a finite-memory online controller theorem. Its main score predicts an exponentially rare all-failure event; a zero-memory predictor already has an exponentially small absolute regret bound as the future horizon grows. Its sign comparison uses each experiment’s own Bayes baseline; it is not a finite-memory advantage theorem for the richer detector. The author largely declares these restrictions honestly. They are not hidden counterexamples, but they substantially limit what the main result demonstrates.

The recommendation is rejection, rather than a routine revision invitation, because a materially different judgment would require a stronger central result, not another corrected identity or a larger count of retained theorems. This is not a request to abandon the model, reduce the target, or manufacture a many-collision problem outside the paper’s scope.

## 3. What v5 has actually resolved

| Previous substantive concern | V5 disposition | Assessment |
|---|---|---|
| Unrestricted functional gates make attainable rank too unconstrained | Fixed four-symbol detector and four-entry lookup cube | A real restriction of the controller interface; exact cube-image calculation is correct. |
| Full-likelihood dimension does not identify future decision requirements | Operational quotient, probe span, and causal shrinking moments | Addressed for the specified observable-future task, not arbitrary hidden-parameter losses. |
| Continuous exact dimension gives no finite-bit consequence | Matching finite-symbol bounds and a separate continuous-state obstruction | Addressed in the checkpoint model, including declared randomized codes. |
| Conditional worst-command lower bounds may not describe one experiment | Independent uniform-command exploration and subprobability minorization | Addressed; continuous command randomness and its storage convention are explicit. |
| Old adaptive witness survives removal of the mark | Same-protocol sign erasure changes the new exponent | The old objection does not invalidate this new theorem. |
| A positive benefit should not merely save acceptance cost | Exact uncensored two-cartridge prediction gain | Addressed; its mechanism is conditional-variance improvement, not adaptive control. |
| Rank-r and all-stage arcs were already available to the referee | Incorporated with attribution | Correct consolidation; not an independent answer to the significance objection. |
| Four-journal-level central advance | Still not established | This is the decisive editorial judgment, not an allegation that the requested additions are absent. |

The previous report asked for a restriction–geometry–decision connection. V5 supplies one. It would be moving the goalposts to deny that fact. The remaining question is the strength of the supplied connection, evaluated below on its own merits.

## 4. Audit of the new proof chain

### 4.1 Finite calibration: correct, explicit, and still an ideal exact-coordinate realization

**Anchors:** `sections/12_calibrated_rank.tex`, `thm:calibrated-rank`, `eq:four-cells`, `eq:finite-failure`.

The probabilities are

\[
k_\partial=\pi R^2/a_0,\quad k_0=1-\pi R^2/a_0-2TR/a_0,
\quad k_\pm=TR/a_0\pm2T\epsilon R^3/(\pi a_0).
\]

They sum to one and remain positive under the stated bounds. The four power-coefficient columns have determinant of absolute value `4 T^2 epsilon / a0^3`. The failure family is exactly the image of the rejection-probability cube under this matrix. The displayed inverse command realizes a neighborhood of the constant half-failure polynomial with one command independent of the unknown radius. Erasing the sign before comparison removes the cubic direction and leaves the full quadratic space. The shared four-factor menu spans the required spaces in both devices.

This is more constrained than v4’s arbitrary measurable angular gate. The controller does not see the impact coordinate, the prepared seed, or the discarded angle. The fixed internal threshold is sufficient; no arbitrary inverse-CDF family is required for this theorem.

Nevertheless, the detector still reads an internally exact coordinate satisfying `|z|=R`. Its fixed threshold then generates a prescribed parameter-dependent bit. This is a legitimate ideal apparatus assumption, not circular use of a parameter supplied to the controller. It also means that the realization theorem is a finite calibration calculation, not a lower bound on physical measurement complexity or a characterization of unavoidable mechanical information. The manuscript should continue to avoid those broader interpretations.

### 4.2 The finite-horizon quotient and causal profile are sound

**Anchors:** `sections/13_decision_horizon.tex`, `lem:probe-span`, `thm:decision-quotient`, `thm:causal-horizon`.

The physically executed all-failure probes span `P_(qm)` because an open subset of `P_q` spans `P_q`, and products of `m` such factors span all monomials through degree `qm`. Each probe is a realizable event; only the selected sequence is executed.

For a common continuation rule applied to future histories, every realized future word has a likelihood polynomial of degree at most `qm`. Equality of the corresponding posterior moments therefore gives equality of the future law. Conversely, equality of all continuation laws includes the spanning probes. This proves both directions, not merely sufficiency of a convenient moment list.

The dimension computation is particularly clean. Put `a=qn`, `b=qm`, and

\[
E_a=\{Q\in\mathcal P_a:\pi_0Q=0\}.
\]

The prediction derivative is the pairing `Q -> (pi_0(H_j Q))_j`. For `b>=a`, its kernel is zero because a kernel element is orthogonal to itself. For `b<a`, restriction to `E_b` is injective, while the constant test removes one of the `b+1` possible test coordinates. Its rank is consequently `min(a,b)`. Full support, not existence of a prior density, supplies the positive polynomial Gram form.

The coprime-factor submersion gives an attainable open posterior patch. Composing local sections and using invariance of domain gives a genuine continuous-state lower bound. Coefficients or moments give the global upper representation. The argument does not confuse an affine-hull count with an attained local dimension.

The shrinking recursion

\[
M'_j=\frac{\sum_{i=0}^q f_iM_{i+j}}{\sum_{i=0}^q f_iM_i},
\qquad j\le q(m-1),
\]

uses only the old moments through `qm`. The coefficient-to-moment changeover needs prior moments through `qN`; the stated tent profile follows. It is an exact-real, posterior-dependent state statement. Additional task memory for a payoff referring to past reports is not erased, and an arbitrary hidden-parameter terminal loss is not covered by this smaller quotient.

### 4.3 The randomized finite-code lower bounds do not contain the usual side-information loophole

**Anchors:** `sections/14_memory_risk.tex`, `lem:score-metric`, `thm:memory-rate`, `thm:average-memory-rate`, `thm:continuous-regret`.

The Brier excess is exactly `s^(-1)||a-p||^2`. Revealing the query after encoding is essential and is stated. The attainable ball is obtained from the previously proved submersion, not postulated as a generic property of all posterior sets. The quantitative inverse-function argument using a smallest singular value and a derivative-variation bound is valid.

The upper bound is an ordinary grid in the prediction affine plane. The lower bound is also correct: after fixing a fresh public seed, conditional-mean decoder outputs give at most `M` centers. Private encoder randomization cannot beat the nearest center. Projection to the affine plane reduces distance, and the union-of-balls volume bound gives

\[
\mathbb E\min_i\|X-z_i\|^2
\ge \frac{d}{d+2}\rho^2M^{-2/d}.
\]

Averaging the independent seed preserves this lower bound. This is not a deterministic-only argument disguised as a randomized-code theorem. A past command-generation seed is explicitly charged, so it cannot act as an uncounted historical tape.

The unconditional result makes a further legitimate step. Uniform continuous commands and the all-failure evidence give a positive-density joint measure in command space. A local submersion chart, integration over complementary coordinates, and the retained evidence yield a positive subprobability minorization on the prediction ball. This proves an unconditional lower bound for one fixed experiment. It does not assign positive probability to an individual exact real command. The finite-alphabet alternative, where an exact finite history code eventually exists, is expressly distinguished.

The Borsuk–Ulam assertion is separate and valid for a deterministic continuous real encoder. It is not used to impose continuity on finite-bit codes. These distinctions are strengths of the revised argument.

### 4.4 The bit-value and all-stage-arc results are correct under their stated restrictions

**Anchors:** `sections/15_mark_value.tex`, `thm:zero-cost-gain`; `sections/16_all_stage_arcs.tex`, `thm:all-stage-arcs`.

Conditional on a first hit, the prior becomes `R pi_0 / mu_1`. The next placement-failure probability and first sign probability are

\[
h(R)=\pi R^2/a_0,\qquad c(R)=1/2+\epsilon R^2/\pi.
\]

Their covariance under the hit posterior is `epsilon v/a0`. The squared-loss improvement from the binary observation is its squared covariance divided by `cbar(1-cbar)`. Multiplying by the first-hit probability gives exactly the printed formula. Full support on a nondegenerate positive interval makes the variance strictly positive. Both experiments consume two uncensored cartridges, so this is not the old acceptance-cost mechanism.

For the full circular detector, freezing an optimal failure continuation turns the gate comparison into a linear pointwise problem. The accepted continuation is convex in the cosine coordinate, whereas the frozen failure term is affine. Their comparison yields at most two collision arcs. The Borel construction uses the already selected feedback and finite chronological integration, rather than an unjustified measurable selection on a space of policies. Tagwise current accepted reward is indispensable. The result is a boundary-count theorem, not an algorithmic complexity theorem. Its attribution to the previous report is appropriate.

## 5. Decisive limitations of the central contribution

### E1. The exact formula is a saturated polynomial-space calculation, not yet a broader structural theory

The step specific to the main theorem is the rank of a Gram pairing between nested full polynomial spaces after an open-product attainability argument. This is appreciably stronger than merely storing coefficients. It is nevertheless a short finite-dimensional argument once the previous product-rank lemma is available.

A separate elementary family makes the generality and the limitation transparent. On `t in [0,1]`, put `z(t)=1/4+t/2` and

\[
k_j(t)=\binom qj z(t)^j(1-z(t))^{q-j},\qquad j=0,\ldots,q.
\]

These are strictly positive normalized categorical probabilities and form a basis of `P_q`. Their lookup failure family has interior, so the whole new quotient and coding theorem applies without any Lorentz mechanics. This is not a counterexample, and the manuscript itself states a general polynomial theorem. It identifies what the theorem’s mathematical engine actually is: full polynomial saturation plus a definite pairing.

An application need not be unique to mechanics to be important. The objection is not that another realization exists. It is that neither the general theorem nor this particular realization currently exhibits a difficult structural phenomenon beyond this saturation mechanism. Section 7 below gives an explicit sparse-space example showing where genuinely different geometry already begins.

### E2. Sharp checkpoint coding is not a sharp finite-memory sequential decision law

The encoder is allowed to have the entire exact prefix available before compressing once. The decoder then announces one forecast before the selected probe is executed. The codebook, query table, exact calibration, and exact prefix processing are outside the charged memory resource. Those conventions are legitimate and mostly explicit.

They do not establish matching rates for an `M`-state controller that must update after every observation, cannot retain a full-precision prefix, and must choose future interventions from its evolving finite memory. The causal exact-real theorem does not fill this gap: quantizing that recursion repeatedly introduces additional errors, and the current theorem gives neither a matching streaming construction nor a matching streaming lower bound.

This matters because the title and broader control framework suggest a stronger operational synthesis than the new coding result actually proves. A focused checkpoint theorem may be valuable, but its contribution must be judged as such. The report does not require an online theorem as a missing hypothesis of the printed result.

### E3. The score is nondegenerate at each fixed checkpoint but degenerates rapidly with the future horizon

This limitation admits an elementary bound, not merely a qualitative warning.

**Referee deduction: zero-memory absolute-regret bound.** Suppose every factor in the probe menu satisfies `0<F<=u<1`. Every all-failure probe has `H_j<=u^m`, and therefore `p_j<=u^m` for every posterior. A decoder that stores no history and always forecasts zero has

\[
\mathcal R(0,p)=\frac1s\sum_jp_j^2\le u^{2m}.
\]

For the general bounded gate class one can take `u=1-eta`. For the particular shared menu one has the sharper bound `u=c+delta`, because every raw cell probability is at most one. This holds for every prefix, hence for worst-history and unconditional regret alike.

Consequently,

\[
\mathcal R_M^*\le\min\{4dM^{-2/d},(c+\delta)^{2m}\}
\]

for the shared-menu problem. With `c=1/2`, `delta=1/8`, and `m=20`, the second bound is `(5/8)^40 < 10^(-8)`, already with `M=1`. The inequality is checked exactly in the accompanying program.

This does **not** contradict the manuscript’s theorem: the theorem takes coding resolution to infinity with the detector, prior, `n`, and `m` fixed. Its constants are expressly not uniform in the horizon. It does show that the displayed coefficient `q min(n,m)/2` in the bit asymptotic cannot be interpreted as a horizon-uniform demand for useful memory at a fixed absolute tolerance. A growing formal dimension and an already negligible zero-memory regret can coexist in precisely the submitted task.

The manuscript should display this bound near its main performance statement. More importantly for significance, it does not yet establish a nondegenerate joint memory–horizon law. Replacing the task or rescaling its loss would change the problem and would require its own stated resource and payoff conventions.

### E4. The sign comparison is a structural ablation, not a finite-budget superiority theorem

The common command convention, number of cartridges, query index set, and loss formula are genuinely shared. However, the event probabilities differ between the two apparatuses, and each regret is measured against that apparatus’s own full-history Bayes forecaster. A larger dimension means that matching the richer forecaster can require more bits. It does not establish which apparatus gives the smaller total Bayes risk at the same finite bit budget.

Nor is the uncensored two-cartridge gain a theorem resolving that finite-memory comparison: it uses free history memory and a different prediction target. The two results correctly expose two aspects of the same bit, but their juxtaposition does not prove a single sharp law for the operational value of that bit under a memory constraint.

An independent exact enclosure also puts the stated positive-gain example in scale. For a uniform prior on `[9/20,47/100]` and `T=epsilon=1/20`,

\[
v=\frac{529}{18750000},\qquad
5.637602588099328\times10^{-13}
<\Delta_{\rm bit}
<5.637602588099330\times10^{-13}.
\]

Smallness is not a defect in a strict mathematical inequality, and the author does not promise a large universal gain. The calculation does prevent this witness from carrying an unstated claim of substantial finite-resolution benefit. Exact rank remains full for every positive amplitude, while the gain tends to zero quadratically as the amplitude tends to zero. The current theorem does not quantify the transition between formal dimension and useful prediction accuracy.

## 6. The inherited framework does not cure these limitations by accumulation

The full positive filter, boundary-complete Bellman theorem, fixed-controller response, and normalized smooth surrogate remain useful and appear correct under their assumptions. Their preservation is appropriate. The thirty-four-label count is not itself evidence for a central breakthrough.

The response theorem concerns a fixed parameter-independent feedback rule, not differentiation through an optimizing policy. The smooth-surrogate theorem controls complete-policy values and transfer regret, not exact rank under arbitrary nonpolynomial perturbation, derivative convergence, or a vanishing rare-history posterior error. The paper correctly makes these distinctions.

The retained adaptive example remains a valid full-class acceptance-cost comparison. Its nominal optimizer uses only no collision versus its complement, and its gap is

\[
(1-s)\{z_lq_l(1-q_l)+2z_uq_u(1-q_u)\}.
\]

V5 now explicitly separates that mechanism from the new sign results. This closes a misleading interpretation rather than making the old theorem false. I examined the written all-Borel reduction and transfer proof, but did not independently recertify its entire numerical table in this review. The previous referee’s numerical execution must not be reported as a new one.

The main paper still combines two detector interfaces, two notions of information state, an exact-real causal algorithm, a checkpoint coding theorem, a separate free-memory prediction gain, a multiplicative-cost control example, and mechanical response appendices. These pieces have legitimate links, but the reader must not have to infer a stronger unified performance theorem that is never stated. A clearer organization should preserve proofs and historical material while making the actual central claim unmistakable.

## 7. A referee-derived sparse-space example: one-step rank is not the future decision dimension

This is a new deduction for this review, **not a counterexample to the printed full-`P_q` theorem and not a claim of literature priority**. It indicates a structural issue that the full-rank calculation avoids. In particular, the already credited formula `n(r-1)` for full-likelihood products cannot simply be converted into `(r-1)min(n,m)` for future decisions.

Let

\[
W=\operatorname{span}\{1,t^2,t^5\},\qquad t\in[0,1],
\]

with the uniform prior. It has a positive normalized three-cell realization:

\[
k_1=\tfrac13+\tfrac1{12}t^2,\quad
k_2=\tfrac13+\tfrac1{12}t^5,\quad
k_3=\tfrac13-\tfrac1{12}(t^2+t^5).
\]

The third cell is at least `1/6`; the cells are independent and sum to one. Lookup rejection probabilities in `[1/4,3/4]^3` therefore give relative interior in `W` around the constant `1/2`.

Take three all-failure factors `F_i/2`, where

\[
F_i=1+a_it^2+b_it^5,\qquad
(a_1,b_1,a_2,b_2,a_3,b_3)=\tfrac1{1000}(1,2,3,4,5,6).
\]

They are exactly implemented by rejection vectors

\[
\left(\tfrac12+4a_i-2b_i,\;
\tfrac12-2a_i+4b_i,\;
\tfrac12-2a_i-2b_i\right),
\]

all strictly inside the permitted cube. Thus this is an attainable example, not an arbitrary polynomial perturbation outside a calibrated experiment.

For two future trials,

\[
W^2=\operatorname{span}\{1,t^2,t^4,t^5,t^7,t^{10}\}.
\]

Products of attainable failure factors span this space. Every accepted or rejected two-step word, including feedback choices along that word, also belongs to it. The future operational quotient is therefore determined by the five nonconstant moments with exponents `2,4,5,7,10`; its global dimension is at most five.

Write `P=F_1 F_2 F_3`, `Z=int_0^1 P(t)dt`, and

\[
p_j=\frac{\int_0^1t^jP(t)dt}{Z},\qquad j\in\{2,4,5,7,10\}.
\]

For each parameter variation `V=t^h product_(k != i) F_k`, `h in {2,5}`, the derivative is

\[
D_Vp_j=\frac{Z\int_0^1t^jV(t)dt
-(\int_0^1t^jP(t)dt)(\int_0^1V(t)dt)}{Z^2}.
\]

Exact integration uses only `int_0^1 t^k dt=1/(k+1)`. At the displayed attainable tuple, the determinant of the first five columns, ordered `(a_1,b_1,a_2,b_2,a_3)`, is

\[
-\frac{149355957460881864071474244699533159667968750000000000000}
{321006326403084606311224880739213913091275853342726956011747270080699228465818648617},
\]

which is nonzero. The formula, rational evaluation, actual gate realization, and rank check are reproduced by the accompanying independent program.

The inverse function theorem on this five-coordinate slice supplies an attainable open prediction patch with a local section. Invariance of domain gives the lower continuous-state bound, and the five moments give the global upper bound. Thus the exact observable-future continuous dimension in this example with `n=3,m=2` is **five**, whereas `(r-1)min(n,m)` with `r=3` would give **four**. The same finite-probe squared-loss construction then has fixed-checkpoint coding exponent `2/5` by the volume and grid arguments, not `2/4`.

The point is not to demand that the author append this example as another theorem and announce closure. For a general fixed factor space `W`, the relevant object is the pairing of the normalized-product tangent space with the future test space `W^m`. Its rank depends on multiplication geometry and the prior pairing, not just the dimension of `W`. The full polynomial case collapses this issue to nested spaces and a definite Gram form. A substantive characterization beyond that collapse could constitute a different central result; the elementary example above is only evidence of the distinction, not such a characterization.

## 8. Definition and presentation points requiring attention

**P1. Specify the input domain of a common continuation policy.** The quotient theorem is correct when the same continuation rule is applied to future observations, with identical external task data. The definition should say this explicitly. It cannot mean the same arbitrary full-history policy evaluated at two different original prefixes while retaining those prefixes outside the state.

For example, two one-step all-failure histories with different constant gates have the same unchanged posterior. A full-history rule that repeats the first gate makes their next censoring probabilities different. Under that reading the claimed equivalence would fail even though the posteriors agree. The source’s references to two posterior densities and a common future task support the intended future-only reading; I treat this as a quantifier clarification, not a blocking counterexample to that intended theorem.

**P2. Separate posterior state from task state in summaries as carefully as in the definitions.** The tent profile does not absorb an arbitrary reward’s dependence on past observations. The source acknowledges this, but the abstract-level phrase “state required for finite future decisions” is broader than the proved posterior-dependent statement without that qualification.

**P3. Distinguish sharp exponent from sharp distortion constant.** The bounds match the power of `M`, not the optimal leading constant or a uniform finite-resolution law over priors, amplitudes, and horizons. The explicit attainable-ball recipe is a checkable local bound, not a reported physically sized codebook or a uniformly conditioned inverse.

**P4. Remove stale review-relative wording from the integrated mathematical narrative.** Appendix A still describes a “current English-v3 report”; other retained passages refer to the “current referee report” when their attribution belongs to an older round. Use stable source identities or ordinary mathematical remarks. This is a presentation repair, not grounds for deleting proofs or provenance from the repository.

**P5. Keep the two detector comparisons distinct.** Erasure before comparator evaluation is an intervention on the apparatus and changes how the same four-entry command is interpreted. It is not automatically the same as postprocessing an already censored five-symbol report. The manuscript’s convention is explicit and valid; summaries should not silently replace it with a stronger experiment-ordering assertion.

## 9. Literature comparison and originality boundaries

The following are targeted primary-source comparisons, not an exhaustive priority search. No claim is made that one earlier source proves this entire manuscript.

**[L1] Predictive representations.** The primary NIPS 2001 proceedings record for *Predictive Representations of State* describes multi-step action-conditional predictions as states. This supports the manuscript’s attribution of the representation principle. It does not establish the present attainable nonlinear quotient or its exact `q min(n,m)` formula. Record inspected: <https://papers.nips.cc/paper_files/paper/2001/hash/1e4d36177d71bbb3558e43af9577d70e-Abstract.html>.

**[L2] Quantization.** Graf and Luschgy, *Foundations of Quantization for Probability Distributions*, Lecture Notes in Mathematics 1730, Springer, 2000, is the appropriate standard comparison for finite-dimensional squared-error coding. The review does not attribute the exponent mechanism to A1. Publisher record: <https://link.springer.com/book/10.1007/BFb0103945>. The primary record for Graf, Luschgy and Pagès, *Distortion mismatch in the quantization of probability measures*, also documents established asymptotic quantization-rate questions: <https://arxiv.org/abs/math/0602381>. The present report’s lower-bound audit rests on the written volume proof, not on an unverified assertion that a cited theorem has identical randomization quantifiers.

**[L3] Sequential approximate information states.** Subramanian, Sinha, Seraj and Mahajan, *Approximate Information State for Approximate Planning and Reinforcement Learning in Partially Observed Systems*, JMLR 23(12), 2022, formulates recursively updated information states and approximate dynamic programming with bounded policy loss. This is relevant to distinguishing checkpoint compression from sequential approximate control; it is not a prior proof of the submitted polynomial dimension or coding lower bound. Primary journal abstract inspected: <https://jmlr.org/papers/v23/20-1165.html>.

**[L4] Comparison of experiments.** Blackwell, *Equivalent Comparisons of Experiments*, Annals of Mathematical Statistics 24 (1953), 265–272, DOI `10.1214/aoms/1177729032`, is appropriate background for information value. The submitted exact covariance calculation supplies its own strictness proof and should be assessed as such. The full original article was not used as a substitute for checking that calculation. Primary publication record: <https://projecteuclid.org/journals/annals-of-mathematical-statistics/volume-24/issue-2/Equivalent-Comparisons-of-Experiments/10.1214/aoms/1177729032.short>.

The bibliography is substantially more candid than a presentation claiming predictive states, quantization, or conditional variance as newly invented. Correct attribution, however, leaves the burden of identifying a sufficiently strong original result. A synthesis can meet that burden, but merely observing that the ingredients are now linked is not enough at the requested level.

## 10. What would materially change the assessment

A further manuscript should identify one central result that remains mathematically substantial after the elementary saturation calculation and classical squared-error coding mechanism are removed. Within the present finite-budget setting, a structural description of nonsaturated attainable test spaces and their operational quotients, or a nondegenerate finite-resolution performance theorem genuinely coupling attainable geometry to an evolving constrained state, would address the issues identified here. These are illustrations of the missing strength, not a requirement to solve every listed extension and not a promise of acceptance for appending another result.

The next response should explicitly confront the zero-memory horizon bound and distinguish the two Bayes baselines in the sign experiment. It should not defend a fixed-checkpoint theorem by suggesting that it already proves online control complexity. Nor should it answer the sparse-space example with only another formal degree count.

The existing proofs, retained failure probabilities, positive likelihood representation, common-policy comparisons, and precise apparatus assumptions should remain available. What needs to change is the force of the main theorem and the accuracy of the synthesis, not the amount of archived mathematics.

## 11. Execution record and final recommendation

The independently written program completed **58/58 exact checks**, using Python 3.13.5 and SymPy 1.14.0. Its SHA-256 is

```
692237c585d79a31cc5050b05082b97091d31c34464066f211c8876427cfcd65
```

The checks include physical calibration identities, separate positive categorical probe spans, asymmetric centered-Gram ranks, coprime product derivatives, shrinking-moment identities, Brier and volume constants, an exactly feasible sparse-space rank-five example, a rational outward enclosure of the physical uniform-prior gain, and the zero-memory tolerance example. They import no author test code. The categorical examples are explicitly separate experiments, not replacements of pi or sqrt(3) in the physical device.

The all-budget statements, topological lower bounds, randomized-coding quantifiers, submersion minorization, geometric collision coverage, and Borel-control arguments are assessed through their analytic proofs. Finite diagnostics do not certify these statements. The author’s prior execution counts and the previous referee’s table checks have not been relabeled as current execution. No LaTeX compilation, PDF inspection, proof-assistant certificate, or exhaustive priority verification is claimed.

**Final recommendation: reject at the requested four-journal level.** V5 is a real mathematical improvement over v4 and appears internally sound in its declared setting. The objection is that its strongest new claim remains a fixed-checkpoint saturation-and-quantization result with a deliberately constructed scoring task, while the manuscript has not yet established the broader structural or nondegenerate operational consequence needed to make that result a compelling major advance. This is a substantive negative assessment of the present submission, not a no-go judgment on further development.
