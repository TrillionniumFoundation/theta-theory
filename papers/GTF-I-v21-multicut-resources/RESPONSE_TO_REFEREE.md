# Response to the fifth independent external referee report

## General Theta Foundations I — Revision v21
### Multicut Continuation Complexity and Stable Causal Certification

**Controlling report:** `reviews/general-theta-foundations-i-v20-external-harsh-top4-r5-2026-09-23/REFEREE_REPORT.md`, commit `14bcfe767940f8cbd196637049524d0b14eaee19`.

**Reviewed predecessor:** `b488b2f28bec42a555999070759d715678b87db8`.

**Revision strategy:** the report's Route II, a general multicut approximate continuation theory, with a constructive end-to-end theorem and a new realization of the same physical certification task. We retain the full previous mathematical development rather than changing the physical target or deleting difficult downstream obligations.

Compiled numbers and pages are in `evidence/THEOREM_LOCATIONS.json`. Every new mathematical claim below has a statement and proof in the manuscript; executed diagnostics are separate reproducibility evidence.

## Principal change

The preceding article restricted one post-training register and allowed unrestricted finite upstream memory. The present article removes that unrestricted training register from its principal realization theorem.

Let κ_c denote the former decision-cut complexity. Define W_c as the least peak retained-state width over the entire training, fresh-random-bit, decision, and validation schedule of every successful finite audit, and W_c^rat as its rational fair-bit subclass. For a fixed finite alphabet of size d, Theorem 7.2 proves

**κ_c ≤ W_c ≤ W_c^rat ≤ 12d κ_c.**

The theorem gives a finite preparation count and explicit precision, random-bit and read-only description costs. Its proof builds a bounded-state tournament from four-state finite-horizon comparisons. It never constructs an empirical histogram and hides it behind a final checkpoint. The external schedule clock is explicitly distinguished from an autonomous implementation and charged in the conversion formula. The classical finite-statistics mechanism is credited to Cover rather than claimed as new.

For the actual collision family, Theorem 22.1 gives a deterministic implementation with at most twelve states throughout bit acquisition and validation. The inherited all-auditor decision obstruction gives the end-to-end lower bound three. Thus **3 ≤ W_phys ≤ 12**, while the 399-training-trial, 40,602-state construction remains as a different preparation–memory regime. The exact integer peak and optimal fixed-sample frontier are not claimed.

## 1. Improvements credited to v20

All fifteen improvements identified in Section 1 of the report are retained. The one- and two-response spectral values, feedback subfamily reduction, three-event construction, exact residual profile of the specified rule, weighted finite-valued overlap theorem, and three transport-version lemmas remain in the canonical article.

The complete v20 organizing theorem is retained in the appendix. The whole 400-page predecessor development is appended without changing its pages. `INHERITANCE.json` identifies unchanged mathematical modules and the sole inherited mathematical source repair. Preservation is not treated as additional proof credit.

## 2. Mathematical spot-checks

We agree with the distinction between the report's positive algebraic assessment and its structural rejection. We did not replace the validated three-candidate inequalities or reissue them as the new principal theorem. The new chain adds a full-profile value and realization theorem, finite bounded-state training, actual randomizer implementations, and confidence guarantees.

The inherited finite diagnostics are rerun, including exact small-word residual enumeration and the 399-sample key counts. New diagnostics compare four-state execution with its exact first-success probability, test precision and capacity accounting, and check the physical two-phase construction. A finite parameter grid is not a substitute for a uniform analytic proof.

## 3. A post-training dictionary is not the full training burden

Theorem 7.2 (`thm:v21-endtoend`) addresses this objection. Its lower bound applies to every successful full-schedule auditor because it must cross the decision cut. Its upper bound is a compatible online machine throughout training and validation, not a histogram-plus-index argument.

Each comparison uses a Bernoulli randomizer whose mean encodes the difference of two response payoffs. A four-state comparison with an indifference band selects the better response except for a prescribed error. A sequential tournament stores only its incumbent and comparison state. The proof tracks comparison regret, calibration, dyadic rounding and failure probability uniformly on the original nonconvex image.

For a K-response list with envelope v, the score is at least v−2^(1−r)−2ρ−4(K−1)θ−2(K−1)δ. Its N=2LR(K−1) training observations and peak at most 12Kd are explicit. This is a constant-factor full-schedule classification for fixed alphabet, not an optimal preparation bound.

## 4. Cut placement and refactorization

Sections 6–7 distinguish the full profile K_t, its peak, and a single decision interface. Theorem 6.1 requires compatible approximate suffix kernels, not independently selected codebooks at successive cuts. Its error accumulates along the actual causal schedule.

Theorem 6.2 gives profile monotonicity, relaxation by dropping charged cuts, finite-precision value bounds, and attainment for a fixed finite experiment. Proposition 6.3 gives holding-cut insertion, observation refinement, simulator-product memory, retained bridge registers, and autonomous-clock conversion. No invariant is claimed independent of its observation and clock model. Once those interfaces are declared, however, the decision cover and end-to-end width are related by a proved uniform factor.

## 5. All-algorithm physical peak memory

The new physical construction constrains every acquisition epoch. The first block phase tests the 00 probability; the second, when needed, tests the 11 probability. A latched first-phase event is explicitly retained. Training uses at most five completed-trial states and ten bit-acquisition states; validation uses at most twelve. Training marks are read and discarded according to the declared schedule.

The lower bound three applies to every successful auditor in the full feedback-row interface by the retained two-state obstruction. Combining it with the new construction proves 3≤W_phys≤12 for the same physical family and threshold 2/5.

The concrete twelve-state schedule uses 12,800·2^400 training preparations. This enormous cost is displayed in the theorem and resource ledger, not hidden in “finite.” It demonstrates bounded-state end-to-end realization under the inherited clock model, not a practical replacement. The exact integer peak in [3,12] and an optimal fixed-N frontier remain unclaimed. This is Route II, not a purported completion of Route I with unmatched integers.

## 6. Exact selector computation versus statistical success

The exact 20,301-state trial-cut profile still concerns the old specified selector alone. Its 40,602-state bitwise implementation remains the smaller-preparation alternative. The new peak construction achieves the same expected-score objective without exactly computing that selector, illustrating the distinction by a proved alternative.

Theorem 9.1 applies shared residual budgets to approximate finite-action decisions. Its physical specialization inserts actual marked training-word probabilities and permits every stochastic selector on a fixed all-on schedule. We do not substitute these fixed-schedule likelihoods for controller-dependent adaptive likelihoods.

## 7. Expected score versus confidence

Section 23 defines two different testing tasks. Theorem 23.1 repeats the whole audit independently, retains a signed-score sum, and bounds both type-I error under equality and type-II error over fixed alternatives by exp(−Jγ²/8). Width is at most W(2J+1), and preparation count is J(n+2).

For the retained physical audit γ=2/5 is valid, so J≥50 log(1/α) suffices. Theorem 23.2 instead trains once with a high-probability conditional witness margin, then repeats validation. Its type-II bound is 2δ+exp(−mγ_0²/8), with a charged witness label and accumulator. These are actual error guarantees, not interpretations of one signed pair. The three-state expected-witness optimum is not asserted for the different binary testing task.

## 8. Structural force of the general theorem

The principal chain is no longer only a half-space cover and empirical selection. It includes compatible approximation across all cuts, a full profile value for finite controlled experiments, and a constructive comparison of the cover with bounded end-to-end width.

Theorem 9.2 gives growing compact point-source images with exact response spectra and linear end-to-end upper and lower bounds. Theorem 9.3 gives a simultaneous product profile for overlapping retention obligations and an approximate stochastic-decoding lower bound. These test growing and simultaneous memory constraints. They are mathematical classes, not claims of high-dimensional hard-sphere scaling. Infinite observation alphabets are not silently included.

## 9. Scale of the physical example

We retain the nongrazing two-sphere collision, marked preparation, fixed positive Gaussian noise, and no-collision control. No many-particle, vanishing-noise or kinetic limit has been substituted for a proof. V21 adds full-schedule realization and confidence consumers on the actual original family. Its general structural result supplies bounded-state training for every strict finite response cover; the abstract growth examples remain distinct from unproved physical asymptotics.

## 10. Source-preserving stability

Corollary 7.3 displays 2 min(1,Nα), together with candidate and target validation errors. The physical theorem explicitly states that changing the collision parameter leaves the blind candidate training law unchanged; only there is α=0.

The confidence section distinguishes transporting a conditional mean margin from transporting the entire repeated-data law. It does not assign a one-sample total-variation bound to an m-sample law. Coupling full data sets counts all affected calls.

## 11. Weighted residuals and statistical memory

Theorem 9.1 imposes a common complete-word capacity across cuts, preventing one word's regret from being counted repeatedly. The sum of monochromatic-edge minima bounds weighted error for every compatible stochastic machine. Optimizing weights on fixed distinguishing graphs is a finite linear program.

The physical specialization uses its genuine marked product likelihood and priors supported on feasible (p,q), not mixtures reclassified as private simulators. It covers all stochastic event selectors on the prescribed schedule. We do not claim complete LP duality or a new numerical adaptive physical lower bound above three. The general lower comparison is κ_c≤W_c; the substantive new side is bounded-state realization for every compact finite-alphabet image.

## 12. Full feedback-row notation

Section 22 explicitly defines κ_c^rows. Theorem 22.1 states κ_(2/5)^rows=3 directly for the full physical interface, using the feedback-uniform lower bound and an admissible all-on construction. Its full-schedule width is separately bounded. One-row κ remains where the interface really has one row; arbitrary tests on products of validation rows are not treated as a row–event continuation.

## 13. Rational operational approximation

Section 5 proves dyadic row approximation and a fair-bit sampler with at most 2s−1 labels at every depth. A Bernoulli sampler uses at most three labels instead of a persistent exact real uniform variable. The depth-supplying clock is declared.

The nested-event realization stores the actual event through validation, not just an unimplemented mean vector. Random bits, labels and read-only thresholds are recorded separately. Section 7 applies these samplers to training comparisons and gives description sizes. Strict margins absorb approximation; exact irrational boundary attainment is not asserted.

## 14. Scope of transport repair

The existing common-path domination, observation-level density and marginal integral-version lemmas remain intact. The global consumer retains its bounded common preparation, positive Gaussian noise and scalar bounded entropic hypotheses. The new finite multicut transfer theorem does not promote this scoped continuous-time consumer to a general changing-filtration or cotangent-rigidity theorem.

## 15. Foundation blueprint and G3

G3 asks for preparation, labels, calibration and simulation error in one online theorem. Sections 5–7 provide these for finite controlled experiments and concretely for the bounded-state cover realization. The ledger shows which quantities grow when memory is held fixed.

The proof graph remains multiple-root and typed. GTF supplies shared experimental structure and actual finite model theorems, not an assertion that all eleven historical papers follow from a single already-proved root. General G1, G2 and G4 remain targets; no unrestricted singular-rate form of G3 is claimed.

## 16. Historical B4 defect

The original normalized nonlinear resolvent identity was inspected directly and fails on constants. The appendix retains the correctly typed conditional graph-resolvent identity with its hypotheses. This does not certify kinetic range, compactness, comparison, graph-domain correctors or nonlinear-semigroup convergence. Original B4 targets and documents remain preserved rather than removed or renamed as settled.

## 17. A2 independence

The primary A2 chain remains independent; no artificial theorem dependency is inserted. Historical and primary A1/A2 namespaces remain distinct in the preserved graph. The blueprint describes typed interfaces and model-specific obligations. A future A2 consumer must genuinely invoke a GTF result under its own hypotheses.

## 18. Nearest literature

The original Cover article was inspected at the relevant theorem and clock discussion, and its classical mechanism is credited. Filtered definitions, compactness and randomization in Weisshaupt's 2002 report were checked against the controller class. Inherited residual/Nerode and finite-state references remain.

The original Norberg proof text was not obtained through the available publisher/preprint routes. The requested definitive theorem/page comparison therefore remains incomplete. No absence, uniqueness or priority claim is based on that unavailable text. This remaining publication-level task is recorded in `LITERATURE_CROSSWALK.md` and `PROOF_STATUS.json`; compilation cannot resolve it.

## 19. Article organization and retention

The introduction states the end-to-end theorem first. Causal realization, rational precision, full-profile transfer, bounded-state selection and joint lower bounds form the leading chain. The physical section then gives the full-profile and confidence consumers. The historical dependency map and former organizing theorem are in the appendix.

No prior mathematical proof module is removed from the canonical article. The full historical exposition remains in the appended 400 pages. Page count is not offered as mathematical significance.

## 20. Technical requests

| Item | Location | Result and boundary |
|---|---|---|
| 20.1 Feedback-row complexity | Section 22, Theorem 22.1 | κ^rows defined; physical equality and full peak distinguished |
| 20.2 Rational approximation | Section 5; Theorem 7.2 | Dyadic rows, nested events, fair-bit cuts, finite descriptions |
| 20.3 Moving/splitting cuts | Theorems 6.1–6.2; Proposition 6.3 | Compatible approximation, profile monotonicity, refinement, product states, clocks |
| 20.4 Physical all-algorithm lower bound | Theorem 9.1 specialization; Theorem 22.1 | Actual-weight fixed-schedule bound; universal lower three and full-schedule upper twelve; exact adaptive fixed-N frontier not claimed |
| 20.5 Confidence | Theorems 23.1–23.2 | Type-I/type-II bounds; reset and accumulator costs |
| 20.6 Literature audit | LITERATURE_CROSSWALK.md | Cover/Weisshaupt checked; original Norberg proof comparison incomplete |
| 20.7 Capacity corruption | weighted-residuals.tex | Malformed disjunction replaced by `\text{or}`; before/after hashes recorded |
| 20.8 Training-factor scope | Corollary 7.3; Section 22 | Nα term retained generally; zero only for unchanged training law |

## 21. Structural route selected

The revision selects Route II: constructive whole-schedule comparison, full-profile approximation/composition, joint error budgets, growing images, and a same-family physical corollary. It is not a further optimization of the 399-sample constant. Route I's exact physical peak, Route III's major kinetic closure and Route IV's singular physical asymptotics are not asserted. Their targets remain intact.

## 22. Final statement

V21 supplies written proofs of a general finite-alphabet relation between decision and end-to-end continuation complexity; a compatible approximation/precision calculus; finite preparation and description costs; a twelve-state full physical realization; and two confidence guarantees. It retains the old exact rule profile and historical program.

The receipt reports executed diagnostics, negative controls, typesetting and preservation checks, not independent analytic certification. The exact physical peak and optimal sample-memory frontier remain unclaimed, and the original Norberg proof-level audit remains incomplete. The new statements and their proofs are submitted for substantive external review, not presented as an already-changed top-four recommendation.
