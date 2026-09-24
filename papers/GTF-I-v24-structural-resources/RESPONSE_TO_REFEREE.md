# Response to the seventh external report — General Theta Foundations I, revision 24

**Author:** Qian Qi  
**Date:** 24 September 2026  
**Controlling report:** `reviews/general-theta-foundations-i-v23-external-harsh-top4-r7-2026-09-24/REFEREE_REPORT.md`, frozen at `e34f5eb4fe1b1f03018c6baec2e594ab22766dfb`.  
**Actual reviewed predecessor:** v23 referee-ready commit `e926b783b643b3e7f275a18105528927b76cc97b`; its mathematical source commit is `8a6043aca644043bd805668185eb227468f21170`.  
**New source branch:** `revision/general-theta-foundations-i-v24-structural-resources-2026-09-24`.

## 1. The central objection and the new proof chain

The report recognizes the full-profile all-stochastic characterization, generic strict positivity certificates, compatible noisy recursions, acquired calibration, and the physical interface bridge. Its principal objection is no longer the absence of any converse. It is the absence of a sufficiently substantive resource theorem extracted beyond a fixed finite semialgebraic architecture.

We therefore do not offer a higher-degree SOS computation or another unevaluated consumer. The principal new theorem determines the minimum number of training preparations for the **same positive-noise marked collision task**, over the **entire declared feedback/reset architecture class**, on an explicit high-width segment.

With

`u1 = 4035777 / 10240000`,

`m2 = (12 - 3 sqrt(3)) / 16`,

and `TV(Q,Q*) <= beta`, the theorem proves

`N_c^phys(W,Q) = 2` for every `W >= 12` and `u1 + beta <= c < m2 - beta`.

At the original physical parameters and threshold `c=2/5`, take `beta=1/300`. This gives exactly **two candidate training preparations**, followed by the original **one candidate and one target validation**. The full experiment costs four preparations, not two preparations in total.

The proof has three independent, explicit parts.

1. A dominating-row theorem converts every adaptive feedback training schedule with at most N preparations into a response to N independent all-on observations. Stopping and independent randomization are included. This is an outer-architecture argument, not a certificate for a hand-picked schedule.
2. A posterior-predictive minimax dual supplies an exact rational four-point certificate against every one-preparation auditor, with unlimited memory allowed. The coefficient table is printed in the article; its positive-part sum is u1. The physical exclusion margin is the rational number `78269/30720000`.
3. A deterministic two-preparation selector uses five marked validation events. Its expected ideal score is a polynomial whose uniform minimum is exactly m2. Residual continuation functions compile the selector and both validations into the bit-level profile `(1,2,3,3,4,5,5,10,12,10,10,7,3)`.

The new construction uses the actual mark during validation. It does not estimate an unmarked diagonal-event envelope to high accuracy. This is why the preparation cost can improve while the peak remains twelve. The candidate training marks contain no parameter information and are explicitly discarded. The mark-dependent validation events are legal in the original interface.

This resolves an actual preparation boundary, but it does **not** identify the globally smallest peak width at two preparations. In particular, `(2,12)` is not asserted to be a strictly nondominated point in both coordinates. The exact statement is the value function `N_c^phys(W,Q)=2` for all W at least twelve. The width range 3 through 11 remains to be determined.

## 2. Proof locations

The labels below are stable source identifiers. The executed build generates `evidence/THEOREM_LOCATIONS.json` with final theorem numbers and pages.

| Result | Source label | What it establishes |
|---|---|---|
| Compatible occupation realization | `prop:realization` | Recalled exact common-row class, including unreachable rows |
| Posterior-predictive statistical dual | `thm:dual` | Exact unrestricted-memory N-preparation value, compact parameter family |
| Dominating-row converse | `thm:outer` | A single upper bound valid over all declared schedules and profiles |
| Finite optimal-prior support | `cor:moments` | At most `(N+2)^2` atoms in the two-parameter product family |
| Sharp physical preparation segment | `thm:physical` | Exact minimum N for all W at least twelve and an interval of c |
| One-preparation rational certificate | `lem:one`, `eq:certificate` | Evaluated all-auditor upper bound, not an existential certificate |
| Two-preparation uniform score | `lem:two`, `eq:poly` | Exact minimum of the specified selector over the continuum |
| Full profile and clock | `lem:profile`, `eq:profile` | Twelve-state peak; five decision states; 75-state phase-tagged realization |
| Causal Bernstein coefficients | `lem:urn` | Shared-row coefficient error at most HS/m |
| Quantitative certification | `thm:quantitative` | Explicit degree, coefficient count, cell count and certified value interval |
| Autonomous noisy theorem | `thm:autonomous` | Classical stationary optimum, explicit dyadic/time upper approximation |
| Raw physical confidence construction | `cor:confidence` | Priced actual-interface upper construction, not a transferred coin lower bound |
| Target-only transport | `prop:transport` | No spurious training-horizon multiplier |

## 3. Responses to requests 24.1–24.10

### 24.1. Name the generic certificate theorem precisely

The article now says **complete semialgebraic certificate hierarchy for a fixed finite architecture**. Proposition `prop:realization` recalls the common-row equations to fix the exact controller class, including zero occupations. It is not advertised as a complete sample–memory theory. The older theorem and its proof remain unchanged in the full companion, with this new interpretive boundary stated in the lead article.

### 24.2. Separate inner and outer optimization

Section 2 defines `V(A)` by optimizing stochastic row parameters within one architecture and `V^out(R)` by taking the supremum over all architectures respecting a resource budget.

The subdivision certificate in Section 5 concerns `V(A)`. It extends to a finite enumerated union by taking maxima of intervals, but it does not silently cover an unbounded union. The dominating-row theorem in Section 3 is a separate uniform reduction that bounds the original physical outer class. The one-preparation certificate and the two-preparation construction are combined only after that reduction is proved.

The response kernel in the statistical dual is unrestricted-memory. Its convexity is not attributed to the fixed-profile controller class. In particular, persistent mixing labels remain charged in the latter class.

### 24.3. Provide quantitative certificate information

Theorem `thm:quantitative` treats arbitrary finite parameter sets, hidden finite execution graphs, controlled rows, arbitrary finite register sizes, and prescribed row identifications. If an execution uses at most H controller rows, each row has at most S destinations, and row r is used at most d_r times, a simplex cell mesh `1/m` gives

`L_m <= V(A) <= U_m <= L_m + HS/m`.

The degree in row block r is d_r; total degree is at most the sum of the d_r. The number of product cells is at most `m^(sum_r s_r)`. A cell row has at most `v_r=s_r*2^(s_r-1)` vertices, giving a coefficient bound `product_r binom(d_r+v_r-1,v_r-1)` per parameter and cell. Rational primitive data give rational certificates. Taking `m >= HS/epsilon` provides a value interval of length at most epsilon.

The coefficient proof conditions independent vertex lists on their counts. It then couples the resulting without-replacement row experiment to one vertex controller. This handles reuse of an autonomous row without replacing it by independently chosen time-indexed rows. The auxiliary conditioned urn is a coefficient representation, not an admissible uncharged-memory algorithm.

This is a **subdivided positive-basis certificate**, not a uniform degree bound for the original global Putinar hierarchy. The number of cells and coefficients can be exponential. We do not claim polynomial-time solution of the general controller problem. Dyadic meshes also quantify an explicit transition-precision approximation; fair-bit execution is a separately priced resource.

### 24.4. Extend beyond binary width two

There are two extensions, and their roles are distinguished.

The finite-architecture quantitative theorem has no width-two or binary-hypothesis restriction. It gives rigorous intervals for controlled and multi-hypothesis finite cases, not a closed K-state minimax recursion. The physical theorem treats a continuous two-parameter noisy candidate family and an outer union of schedules.

The autonomous section gives a W-state noisy class for every W at least two, with a closed stationary minimax infimum and an explicit finite-time dyadic implementation. Its stationary formula is classical Hellman–Cover, not a new claim of priority. It supplies the missing substantive autonomous comparison within the manuscript's resource language but is not the paper's novelty claim. We have not proved a general controlled K-state minimax recursion, and do not replace that problem by a binary calculation.

### 24.5. Give an actual physical upper certificate

The one-preparation coefficient table is printed in equation `eq:certificate`. It uses the actual admissible private candidates with `p=q` equal to `1/8`, `1/5`, `4/5`, and `7/8`, and prior weights `1/16`, `7/16`, `7/16`, and `1/16`. All entries have common denominator 40960000. Their positive-part sum is exactly `4035777/10240000`.

For the physical target this gives a worst-case score at most `u1+1/300 < 2/5`, even with unlimited memory, arbitrary legal feedback, stopping before the sample cap and independent randomization. Off-diagonal target coefficients for the ideal law are nonpositive, so restricting the displayed table to its four supported atoms does not omit a favorable response coordinate.

The finite measure is a certificate against fixed candidates. Its mixture is not itself declared a legal private simulator, and the parameter is not resampled between preparations. We do not assert that this four-point certificate computes the exact optimal one-preparation score. A certified upper strictly below the target threshold is what the matched preparation theorem requires.

### 24.6. Explain exhaustion of the physical architecture class

The physical class is the same row-event training/validation task as in the predecessor: independent reset preparations, current feedback gates, a selected row-event before the fresh validations, and all persistent buffers and selectors charged. It is not the class of arbitrary statistics permitted to reselect a validation event after looking at the validation data.

For the adversarial subfamily used in the converse, every feedback row is the parameter-independent pushforward `(x1,x2,w) -> (x1,g(x1)x2,w)` of the all-on law. Pre-generating N all-on draws therefore simulates every adaptive schedule with at most N preparations. Pulling back the selected validation response gives a member of the response box in the dual. This proves the upper certificate for the union over architectures, rather than enumerating a sample of schedules.

For achievability, every private candidate in the original class has the specified all-on product law, and the deterministic construction uses only this legal row. Thus the upper and lower results concern the same original task. The parameter-independent target calibration allowed in the converse cannot reveal the private parameter and can be absorbed into its independent seed; the construction needs none.

### 24.7. Give an autonomous exact theorem

For independent binary reports with parameters p and 1-p, let `r=(1-p)/p` and use W time-invariant states. In the common irreducible induced-chain class, the stationary minimax infimum is

`1/(1+r^(W-1))`.

The proof bounds the oscillation of stationary likelihood ratios by a Markov-chain-tree argument and applies an elementary likelihood-range lemma. The matching limiting birth-death construction is given explicitly. For dyadic `epsilon=2^(-b)`, its time-n error is bounded by

`1/(1+r^(W-1)) + epsilon*(W-2) + exp(-(p*epsilon/2)^(W-1)*floor(n/(W-1)))`.

The denominator of each transition probability divides `2^(b+1)`. A sequential fair-bit implementation and its extra register states are stated separately. The stationary lower bound is expressly not a finite-horizon lower bound. We attribute the optimum to Hellman and Cover and do not misrepresent it as an original solution.

The physical construction additionally has an exact finite execution with an explicit 75-state autonomous phase-tagged implementation; this is recorded as a clock-cost implementation, not substituted for the autonomous noisy theorem.

### 24.8. Complete the current literature audit

We added and compared Managoli–Prabhakaran, `arXiv:2605.12063v1`, posted 12 May 2026. Their model concerns randomized time-invariant finite-state binary testing against adaptively chosen distributions; its asymptotic error criterion and adversarial parameter dynamics are not identified with our finite reset signed-score task. The manuscript acknowledges their matching state exponents and exact subclass results. It does not derive novelty from their absence.

The finite-memory comparison now explicitly includes Hellman–Cover (1970), their 1971 randomization paper, Flower–Hellman (1972), and Cover–Freedman–Hellman (1976). The stationary formula in our article is attributed accordingly. The author-maintained Stanford bibliography was used to verify the original metadata, including R. A. Flower's initials.

The original Norberg proof-level gap was pursued through the publisher DOI record and the Norwegian library record. The accessible materials did not supply the full original proof. **That part remains incomplete.** We do not claim absence of overlap, exhaustive priority clearance, or a proof-level comparison based only on metadata. The explicit new proofs do not rely on an assertion that Norberg's results fail to cover a certain category.

Müller–Montúfar's polynomial feasible-frequency approach, classical minimax duality and Putinar's theorem remain acknowledged. The statistical minimax interchange and the use of a positive polynomial basis are not separately claimed as novel general principles.

### 24.9. Focus the journal article without deleting the development

The new main article follows one proof chain: the experimental/controller model, the architecture-free dual, the sharp physical preparation segment, quantitative compatible certificates, autonomous resource accounting, and the physical confidence/transport consequences. It does not begin with a long sequence of historical organizing theorems.

No older manuscript path is edited or deleted. The complete mathematical manuscript appends the entire 96-page v23 article to the new article. The complete development appends the entire 649-page v23 volume. The build checks every appended predecessor page for equal extracted text and raster samples, and records source hashes. The full old proof modules, historical derivation graph, references and qualification statements remain in the repository and the source package.

The focused article is therefore not the only deliverable. The paired full volumes preserve all earlier mathematical material; the distinction is editorial organization, not removal of scope or silent replacement of difficult proofs.

### 24.10. Preserve accurate scope qualifications

The caveat that no physical fixed-sample result is evaluated must now be updated, rather than repeated incorrectly: the preparation boundary for W at least twelve **is evaluated**. The complete W=3 through 11 boundary, the least peak width at two preparations, and the optimal score for two preparations are **not evaluated**.

The paper still does not prove a uniform global SOS degree bound, generic tournament optimality, equality of clocked and autonomous resources, a universal controlled K-state recursion, B4/C2 aggregate closure, or eleven-paper closure. The dyadic autonomous upper bound is not an optimal joint time–precision tradeoff. The raw physical confidence construction is not a confidence lower frontier. Preservation and successful checks are not independent proof certification.

## 4. The historical pipeline and the first-principles root

The source audit used the actual v23 modules and their preserved historical material, not a replacement by an older A1 draft. The General Theta Foundations blueprint fixes positive experimental kernels, causal observation, actual preparation, executable tests and charged simulation states before introducing derived geometry or resource invariants.

The new dual follows this order. Actual independent preparations generate likelihoods. These produce a posterior and its validation-predictive distribution. The test quotient yields total variation and a prior certificate. On the constructive side, the event selector's future residual functions form an observation-shift-closed quotient, so its register labels are executable causal states. The marked physical experiment is then a concrete consumer with a matching converse.

The A2 primary geometric route remains independent. The original B4 aggregate still needs its own control transfer, nonlinear resolvent/range and compactness hypotheses and proofs. The broader C2 form, rigidity and optional-projection program is not certified by a finite-state confidence theorem. We preserve those targets and their derivations instead of reducing them to the claims proved here.

The old odd-sample majority width theorem, the ideal marked separation value derived in the v17 material, and the three-response decision invariant are not relabeled as new v24 results. The shortened marked preparation construction and its matching all-architecture exclusion are the specific physical additions.

## 5. Reproducibility and the requested next review

`verify.py` checks the rational table, positive-part sum, exact polynomial identity, derivative certificate, full residual transition quotient, all 4096 input words and selected rational autonomous stationary laws. It also tests a genuinely reused stochastic row in the positive-basis representation. Deliberately incorrect certificate, selector, polynomial, profile, shared-row and stationary-law controls must fail in both ordinary and optimized Python.

The build reruns the inherited v23 diagnostics, preserves every old module and both old PDF volumes, compiles the article and records actual page counts, hashes and theorem locations. The receipt explicitly separates finite checks from analytic proofs and priority assessment.

The principal mathematical request for the next referee is to examine the outer dominating-row reduction, the one-preparation coefficient certificate, the continuum polynomial minimization and the twelve-state validation compilation. The report's broader editorial threshold remains for the referee to assess; it is not treated as satisfied merely because the files compile or a new version number exists.
