# Response to the fifth independent external referee report

## General Theta Foundations I — revision v22
### Causal Continuation and Statistical Resource Frontiers

**Controlling report:** `reviews/general-theta-foundations-i-v20-external-harsh-top4-r5-2026-09-23/REFEREE_REPORT.md`, frozen at `14bcfe767940f8cbd196637049524d0b14eaee19`.

**Manuscript reviewed by that report:** v20, `b488b2f28bec42a555999070759d715678b87db8`.

**Actual starting point of this revision:** the already-published v21 package, `bd5080f15d889ab074d73d4fc9963f83e5759036`, not an older manuscript. V21's source commit was `6dafe7b7c2f40902ea506f9509b86b5c1de67c97`. No v21 referee report was found among the inspected General Theta branches. The v20 report remains the controlling report; v21's previous response is treated as existing work, not as new v22 results.

We follow the report's Route II: full-schedule statistical resource theory. We retain the original physical task and all predecessor mathematical modules. The new article leads with fixed-preparation realizations, an exact all-cut statistical frontier, and active-update transport. The previous unrestricted-horizon theorem remains in the article with its proof dependencies. The separate complete-development PDF includes every page of the 472-page v21 companion, with text and raster identity checked by the build.

## Principal change beyond v21

V21 proved `κ_c ≤ W_c ≤ W_c^rat ≤ 12dκ_c` with an explicitly priced clock, but its bounded-width learner could require exponential preparation length. It also introduced compatible approximate profiles, joint residual budgets, and confidence tests. We do not re-present these as new discoveries.

V22 adds five proved modules:

1. **Finite-horizon preparation–width realizations.** Theorem `thm:v22-tournament` uses an absorbing comparison, with `N=n(K−1)`, peak at most `3dK(2m+1)`, and score loss
   `2^(1−r)+2ρ+4(K−1)θ+2(K−1)[exp(−4θm)+exp(−2nθ²)]`.
   Taking `m=ceil(log(2/δ)/(4θ))`, `n=ceil(log(2/δ)/(2θ²))` gives polynomial preparation length. All comparison bits and validation-event storage are counted. The original constant-width/exponential-horizon realization is preserved as a distinct resource pair.
2. **An exact all-algorithm multicut statistical frontier.** Theorem `thm:v22-revelation` solves the Bayes decision problem for erasure–revelation experiments under arbitrary priors, reveal schedules, and state profiles. With `k_t=min(M,K_t,…,K_n)`, last-revelation weights `w_t`, no-revelation probability `a`, and ordered prior mass `P_k`, the exact value is `aπ_1+Σ_t w_t P_(k_t)`. The upper bound includes every stochastic machine; one compatible deterministic machine attains it. Corollaries invert the formula for preparation count and peak width and give the exact cost of inserting a checkpoint. This is a statistical optimum over all rules, not exact computation of a specified selector.
3. **Occupation-weighted perturbation.** Theorem `thm:v22-active` prices the induced retained transition defects along the actual baseline execution. Absorbed updates contribute zero even when the raw training source changes. The bound is for the retained/output law, not the entire padded raw-data transcript; scheduled preparations remain charged. The absorbing-time formula supplies an explicit active-call bound.
4. **A third same-family physical regime.** Theorem `thm:v22-physical` gives 320,000 training trials, peak width 1,604, decision width three and a score strictly greater than 2/5, in the original positive-noise collision family. Both the 399-trial/40,602-state and the very long 12-state constructions remain intact. These are attainable resource points, not an assertion that the exact physical fixed-sample frontier has been solved.
5. **Finite-state confidence amplification.** Theorem `thm:v22-confidence` gives a polynomial-horizon growing-counter amplifier and a constant-register long-clock amplifier, with prescribed type-I and type-II errors. These coexist with the inherited signed-sum and train-once confidence theorems.

Compiled theorem numbers and pages are in `evidence/THEOREM_LOCATIONS.json`. The analytic proofs are in the English article. Finite checks and successful compilation are reproducibility evidence, not independent mathematical certification.

## 1. Improvements credited to v20

All fifteen improvements in Section 1 of the report are retained. In particular the original nonconvex behavior image, exact one- and two-response values, feedback-row reduction, three-response envelope, 399-sample rule, its exact residual profile, weighted finite-valued obstruction, and three measure/coupling version lemmas remain in the canonical mathematical source. No lower bound is moved to an auxiliary Bernoulli task and then relabeled as physical.

The unchanged-module manifest distinguishes literal source inheritance from modified introduction, front matter, bibliography and input order. The v21 organizing theorem is retained in an appendix; its complete previous introduction is preserved verbatim in `history/` and in the appended predecessor PDF.

## 2. Mathematical spot-checks

We preserve the proofs credited by the report instead of manufacturing a new answer to an already-closed v19 objection. New checks compare the absorbing transition law against explicit word enumeration and its hitting-time difference equation, and compare the exact revelation frontier against independent exhaustive finite-machine optimization. The latter enumerates transition tables and optimizes terminal decoding without using the frontier formula in the optimizer. The proof for all stochastic machines is separate: condition on a parameter-independent random table, impose every remaining bottleneck, then integrate. This is not an unjustified deterministic reduction of a minimax objective.

## 3. The decision dictionary is not the training burden

The main text now explicitly defines the fixed-preparation full-profile value `V_(N,K-profile)` alongside κ and unrestricted-horizon W. Theorem `thm:v22-tournament` constrains every training cut. It is not an empirical histogram followed by a small final index. Its register contains the incumbent, absorbing counter, current observed symbol and fair-bit sampler state when necessary. The finite description and autonomous clock conversion are stated in the proof.

The inherited `κ≤W≤12dκ` theorem remains valid and useful, but it is no longer the only general resource statement. The exact revelation theorem makes the fixed-schedule all-algorithm optimization explicit on a growing family.

## 4. Cut placement and refactorization

V21's profile monotonicity, compatible suffix realization, holding-cut insertion, simulator-product register and clock conversion remain. V22 adds an exact statistical transformation law: changing the profile loses `Σ_t w_t(P_(k_t)−P_(k_tilde_t))`. A newly inserted holding cut H after time s replaces the effective width by `min(k_t,H)` only for revelations at or before s. Later acquisition is not incorrectly constrained by an earlier bottleneck.

For example, M=4, three half-probability reveals and profile (4,1,4) have exact uniform-prior success 5/8, whereas charging only a four-state terminal cut gives 29/32. Thus checkpoint placement changes the actual optimum, and the theorem computes how.

## 5. All-algorithm physical peak memory

The universal physical lower bound three and full-schedule upper bound twelve from v21 are retained. V22 adds a polynomial-horizon intermediate construction, not a false claim that 1,604 or 40,602 is a lower bound for every successful auditor. The table in Corollary `cor:v22-physical-regimes` explicitly distinguishes all-auditor lower bounds, construction upper bounds and the chosen selector's exact residual count.

The exact integer physical peak in [3,12] and the optimal fixed-N adaptive physical frontier are still not asserted. The revision's exact matched result is the all-cut revelation theorem, within the general finite statistical theory. This implements Route II rather than claiming that three unmatched physical integers complete Route I.

## 6. Exact computation versus statistical success

Theorem `thm:v22-revelation` optimizes Bayes success over every statistical rule under the full profile. It does not fix a desired word function and then minimize its automaton. Randomized encoders and decoders are included in the upper bound. Arbitrary nonuniform priors retain actual probability mass, and the attaining nested machine is profile-compatible.

The uniform-prior specialization is `[a_n+K(1−a_n)]/M`, with `a_n=(1−q)^n`. Its inversion includes unattainable boundary cases: for 0<q<1 a nontrivial success K/M is approached but not achieved at any finite n. The exact result is Bayesian; the article does not falsely promote the asymmetric attaining machine to a minimax optimizer by giving it a free persistent permutation.

## 7. Expected score versus confidence

The existing type-I/type-II theorems remain. V22 further transforms an independent base-audit score D into a dyadic Bernoulli variable of probability `1/2+(D−g/2)/4`, where a known dyadic g is at most the uniform alternative mean margin. Its null and alternative means are separated from one-half by g/8. Applying the absorbing or block comparator yields genuine testing guarantees, with every base reset, score value, coin bit and amplifier state charged.

For the original physical expected-score margin, g=3/8 is legal and the extra coin needs at most six fair bits. The optimal three-state expected-witness dictionary is not claimed as the state optimum of this different binary test.

## 8. Structural force of the general theory

The main theorem now connects fixed-preparation realization, exact all-algorithm profile optimization, and occupation-weighted transfer. The exact frontier permits arbitrary profile bottlenecks, nonuniform prior masses, nonidentical reveal probabilities and growing parameter alphabet. It supplies both necessity and an explicitly compatible simultaneous attainment theorem.

The proof relies on the particular revelation structure, especially nested optimal label sets. We do not infer that every general loss or observation channel has the same formula. The general compatible-continuation and residual results remain the framework outside that solved class. Classical finite-state testing, concentration and martingale arguments are credited rather than claimed as newly invented.

## 9. Scale of the physical application

The original two-sphere, nongrazing, marked, positive-Gaussian-noise model is unchanged. No many-particle or zero-noise claim is inserted without proof. V22 changes the end-to-end training implementation and derives confidence consumers for the same task. The exact growing revelation class is a statistical example, not misrepresented as a many-particle limit.

## 10. Stability with changed training laws

The general Nα bound is retained. The new occupation bound also applies when α>0: the terminal incumbent-law error is at most `α E A`, where A counts active comparison updates. The expected score has a factor two, plus the two validation-law defects. The comparison hitting-time bound is at most `min(n,m²)`, with the sharper formula and gap-dependent bound in Lemma `lem:v22-walk`.

This does not give the complete raw-data law an active-count bound. Ignored reports still change that law, and all scheduled trials still count as preparations. For non-reset physical processes, forgetting an observation may not erase its future physical effect; the theorem requires the actual induced transition kernels or a sufficient analysis state. The unchanged blind source in the moving-collision theorem remains the special case α=0.

## 11. Weighted residuals and joint lower bounds

The weighted finite-valued and shared-capacity multicut theorems remain in full. Their actual-word-probability physical specialization is preserved with its fixed-schedule qualification. The new exact frontier provides a separate sharp weighted statistical example: a remaining k-label bottleneck permits at most the sum of the k largest prior atoms on each last-revelation event. Compatibility is achieved by nested labels, not by independently optimizing each cut.

We do not claim the weighted residual LP is a complete dual for all adaptive finite-memory statistical problems. Nor do we claim a new adaptive physical lower bound above three. These distinctions are stated rather than obscured by an exact count for one selector.

## 12. Full feedback-row notation

The explicit `κ_c^rows` definition and direct physical equality in `physical-full-profile.tex` are preserved byte for byte. The new physical theorem uses that same original row–event interface and cites its feedback-uniform obstruction. It does not substitute one-row notation for an unrestricted feedback conclusion.

## 13. Rational operational approximation

Dyadic row and response approximation, finite fair-bit samplers, actual nested-event retention and finite descriptions remain. The new tournament states the comparison probability explicitly and charges its r+2 fair bits, observed-symbol buffer and sampler state. Its calibration constants are known dyadic numbers; the unknown candidate parameter never appears in the transition description. For arbitrary prescribed dyadic calibration the precision can be enlarged.

The physical intermediate construction is deterministic and needs no such randomizer. The confidence amplifier uses a separate explicitly dyadic coin. Irrational boundary attainment is not used to claim an exact finite program.

## 14. Transport repair and the continuous-time consumer

The three version lemmas and the common-preparation Gaussian/entropic proof remain unchanged. The new finite retained-law transport theorem has its own hypotheses and proof; it is not used to certify the broader changing-filtration, cotangent or rigidity program. Bounded signals, positive noise, common latent preparation and the bounded scalar entropic terminal structure remain the stated conditions of the continuous-time consumer.

## 15. Foundation blueprint and G3

The inspected foundation blueprint distinguishes positive experimental kernels, preparation, causal policies, actual acquired laws, and separately priced labels, calibration, clock and description. Its G3 objective concerns a unified resource–precision–statistical-error theorem, not a claim that a finite decision dictionary solves all dynamics.

The new proof chain gives a finite controlled-experiment realization of these quantities: Theorem `thm:v22-tournament` supplies finite preparation and memory budgets; its dyadic implementation supplies precision and calibration; Theorem `thm:v22-active` supplies simulation/source perturbation; Theorem `thm:v22-confidence` supplies statistical error. The exact frontier gives a matched optimization in a nonconstant family. General singular limits and the other foundation goals retain their original targets.

## 16. Historical B4 defect

We re-inspected the original `ROUND17_POSITIVE_CLOSURE.tex` at `c04845b6613208406703695c9c184ae461f95805`, including the normalized nonlinear resolvent, range/comparison and corrector claims. The displayed linear difference formula fails on nonzero constants. The retained conditional graph identity is not credited with proving kinetic range, compact action sublevels, comparison or the hierarchy corrector. No current theorem consumes the defective aggregate. The original target and text are not deleted.

## 17. A2 and the multiple-root architecture

The namespaced historical graph and appendix retain the independent primary A2 chain. V22 adds no artificial dependency from it to GTF. A genuine future consumer would have to invoke a GTF theorem under its own model assumptions. The current paper contributes a causal/statistical foundation within the preserved multi-root program; it does not certify all eleven historical aggregate theorems by declaration.

## 18. Closest literature

The original Weisshaupt report was revisited at its title page, filtered-operator definition, Lemma 1 and Theorem 5. We correct the erroneous title in v21's companion literature audit; the article's bibliography already had the correct title. The comparison now also notes that the report's variation norm for probability differences is twice the event-supremum total variation used here.

Cover's clocked finite-statistics mechanism remains explicitly credited. Hoeffding and Hellman–Cover bibliographic entries are added, without making newly verified theorem-level claims about every result in those works.

The original Norberg proof text still could not be obtained from the publisher/old Oslo route. The definitive proof-by-proof crosswalk requested by the report is **not completed**. `LITERATURE_CROSSWALK.md` records the precise source-access boundary; no priority, uniqueness, or claim that Norberg lacks a particular feature depends on this absence. This is a remaining publication-level task, not something compilation can solve.

## 19. Article organization and retention

The new introduction states the fixed-preparation and exact multicut results first. The leading proof chain contains marked comparison, continuations, response covers, rational precision, compatible profiles, both training regimes, the exact frontier and active transport. Physical and confidence theorems consume that chain. Earlier organizing statements and the namespaced dependency map are in appendices.

Every predecessor mathematical module is retained in the canonical article. The old introduction's organizing theorem and proof remain; its complete prose is additionally archived verbatim. No predecessor repository path is modified or deleted. The complete-development companion preserves all 472 old pages, rather than treating preservation as extra proof credit.

## 20. Technical requests — disposition

| Report item | Disposition in v22 |
|---|---|
| 20.1 Row-indexed feedback complexity | Explicit v21 definition and proof retained; new physical result uses the same interface. |
| 20.2 Rational implementation | Existing dyadic theorem retained; r+2 comparison bits and separate confidence coin fully priced. |
| 20.3 Moving or splitting a cut | Existing compatible calculus retained; exact all-cut frontier now computes checkpoint sensitivity. |
| 20.4 Physical all-algorithm lower bound | Universal lower three retained; new intermediate construction. Exact adaptive fixed-N physical lower frontier remains unproved. Exact all-algorithm matched theorem supplied for the revelation class under Route II. |
| 20.5 Confidence | Existing error theorems retained; two finite-state amplifiers and their costs added. |
| 20.6 Literature | Weisshaupt title and norm convention corrected; original Norberg proof comparison remains incomplete. |
| 20.7 Malformed disjunction | V21's repaired `\text{or}` source is inherited unchanged and hash-verified. |
| 20.8 Training-factor scope | Nα bound preserved; new active-state bound has explicit reset/kernel hypotheses and does not apply to the full raw-data transcript. |

## 21. Route to a stronger resubmission

The revision develops Route II rather than claiming that a smaller constant or more diagnostics change the venue decision. Its exact multicut theorem is genuinely optimized over all stochastic rules in its stated statistical class, and its general construction makes preparation length explicit. The physical family remains an essential implementation consumer. The exact physical peak, singular many-particle extensions and full kinetic downstream closure remain substantive research targets, not relabeled as solved.

## 22. Final statement

V22 submits additional analytic proofs, an integrated English article, a full historical companion, and a reproducible evidence package. It does not claim independent proof certification or a changed journal recommendation. The remaining Norberg proof audit and exact physical fixed-sample frontier are explicitly identified. All earlier mathematical targets are preserved, while the actual results and their resource assumptions are sharpened for the next external review.
