# Response to the independent referee report on A1 v26

## Submission and review being answered

This revision answers `reviews/a1-english-v26-harsh-independent-2026-09-07/REFEREE_REPORT.md` as committed on `review/a1-english-v26-harsh-independent-2026-09-07` at `19fbf4fe0e7495afd537de73a63670a9cf5616e0`. The reviewed submission is `a2e5d3737085241137211f1cf21393d5bcafa1ce`; its native paper subtree is `899f2124e9e43e11f2e99f0bbba84d7806f34bda`. The report blob is `a1419587213b25dfccab55476416db2b900a6cf0`.

The referee did not identify a fatal counterexample or an unresolved central proof gap in the scalar, graph, selection-capacity, or analytic-phase theorems. The adverse recommendation concerned significance at the requested journal level. We have not recast that editorial assessment as an erroneous mathematical objection, nor marked journal-level significance as mechanically settled by this revision.

The response is to add stronger quantified results and a fully evaluated statistical instance while preserving the existing theorem and proof chain. In particular, the attained confluent flags, full-support prior scope, collision-uniform global covers, all-integer-budget bounds, causal joint-label construction, acquired-dimension caps, graph adaptive converse, first-block selection theorem, separator capacity bound, and analytic collision phases remain in the principal manuscript. The companion source remains present. This is not a replacement of the original results by a smaller conditional paper.

## 1. A rule reused across resolutions: report section 7.3

### The distinction retained

The earlier interval-regret statement compared deterministic orders whose predictive encoders could be redesigned at each resolution. It did not establish a corresponding theorem for a common randomized, history-dependent acquisition rule. We agree with that distinction and do not obtain the stronger assertion merely by relabelling the previous fixed-order result.

A new definition fixes the acquisition law, not just the text of a program. At a fixed calibration the transition functions and independent seed law are fixed across budgets and accuracies. The rule may read its full revealed history, but may not read the requested accuracy, the predictive budget, or a state/output of the resolution-specific predictive encoder. Its encoders and codebooks may be redesigned. The rule is called resolution blind. An algorithm whose acquisition law changes with the number of available labels is not silently placed in this class; the original pointwise graph theorem continues to cover such algorithms at each budget.

### New theorem and proof

`v27/uniform_policy.tex`, Theorem `thm:v27-curve`, proves

    for every calibration a and every fixed resolution-blind rule sigma,
    there exists one order pi(a,sigma), independent of M and of the codebook,
    such that for every integer M >= 1,
    R_sigma,M^(oracle,average) >= c Q_pi(M,a),
    R_pi,M^(charged,maximum) <= C Q_pi(M,a).

The converse is stronger than a claim restricted to an implementable fixed-memory scheduler: it grants the competing scheduler its full history and grants the decoder a finite order prefix. The deterministic upper bound uses the original charged model and one causal joint label.

The new quantifier is justified before any budget is specified. Under the common first-block event, select an order with mass at least beta/v!. Because the acquisition law is fixed, the same order and mass work for every predictive encoder and budget. For a fixed boundary and allocation, apply the unconditional acquired-coordinate density estimate to the M recovered centres before intersecting with the selected trace. A threshold argument gives a lower bound for the expected loss at that single boundary. Maximizing afterwards produces the whole fixed-order profile. No density conditional on an adaptive order is asserted, no decision-region regularity is needed, and no interchange of expectation and maximum is made.

Corollary `cor:v27-bits` also records an explicit additive cost involving beta, the recovery-density constants, the order count, and the Leja-to-volume factorial comparison. It makes the simultaneous bit-curve comparison quantitative. The order is common across budgets; a common nested quantizer across all budgets is not asserted.

### Finite reusable menus and the actual star experiment

`v27/policy_menus.tex` proves deterministic completeness for menus of at most K fixed resolution-blind rules. The menu index is chosen before data are observed, possibly with resolution-dependent mixture weights; conditional member laws remain fixed. Every such adaptive menu is matched, within bounded additive bits at every resolution, by at most K deterministic orders. The reverse construction is causal in the original charged model. Charging the finite configuration index costs at most ceil(log2 K) further bits.

Theorem `thm:v27-menu` and Corollary `cor:v27-menu-regret` characterize the optimal excess over any prescribed accuracy set by a finite order-set minimax functional. Along analytic collision paths, Corollary `cor:v27-contact-menu` identifies its leading coefficient. For the existing positive 24-trial star, Corollary `cor:v27-two-configurations` proves a one-rule interval excess of log2(1/theta)+O(1), and an endpoint-only excess of one half of that leading amount, against the explicitly defined randomized full-history reuse class. Two deterministic configurations remove the leading penalty on every fixed compact positive resolution interval.

This is a positive realization theorem for reusable policy menus as well as a converse. It does not purport to extend a resolution-blind theorem to budget-dependent acquisition laws.

## 2. A complete same-decoder numerical comparison: report section 8.1

`v27/evaluated_model.tex` uses an actual two-vertex, one-edge, two-trial detector experiment, not a nominal Euclidean source. The prior is uniform on [0,1], the positive cells are 1/2+t/4 and 1/2-t/4, and acquisition commands are uniform on [1/4,3/4]^2. The four corner commands form the independently sampled uniform query menu. The completion trial is executed on every run and after every first report.

For the referee's first-command rectangle, requiring only the first failure gives beta=35/1024. The failure-weighted acquired-mean subprobability has a directly derived density bound H=177957/20480. Recovery from the actual four-query vector has squared operator norm 128. The resulting conditional capacity constant obeys

    C^2 = 1013398203168/30625.

Both internal subset vertices are included in the separator. Integrating its actual capacity profile gives the all-budget risk certificate

    [1071875/12452637120528384] M^(-2).

The old comparison event additionally requires the completion failure. After completion commands are integrated, that condition multiplies the entire selected-coordinate subprobability by one half. Thus beta and H both halve, H/beta and the recovery norm remain unchanged, the node capacities are identical, and the complete risk certificate halves. This proves a factor-two improvement with the same decoder and all constants accounted for. It is not an inference from the event-mass ratio alone.

The new calculation does not assert that the rectangle is a uniform inverse chart from the general regular-box construction. Its weighted density is calculated directly. Nor are constants transferred from a finite-prefix oracle decoder to the stricter separator decoder.

## 3. The exact optimum is distinguished from the certificate

The same section derives the full acquired-mean law: two atoms of masses 5/16 and 3/16 at 8/15 and 4/9, plus an explicit continuous failure component of mass 1/2. Projection onto the actual query line gives the exact finite-M reduction of average excess to scalar quantization, with metric factor 1/128. Independent randomized initial orders or decoder seeds cannot improve this infimum.

A self-contained proof of the classical one-dimensional high-resolution formula, including finitely many atoms, yields the sharp average coefficient

    kappa_ex = (integral f(z)^(1/3) dz)^3 / 1536,

approximately 4.886e-7. The separator coefficient is approximately 8.608e-11. Thus the fully evaluated separator certificate remains conservative by a factor of approximately 5.68e3. The paper states this difference explicitly. It does not advertise the generic separator lower bound as an exact minimax constant, or equate the average and maximum-tape optima. The general scalar quantization lemma is identified as classical; the acquired law and the complete comparison are derived for this experiment.

## 4. Decoder and conclusion scopes: report section 8.4

The new introduction contains a compact table separating four claims:

1. The pointwise graph law permits the acquisition rule to vary with budget and its converse permits a finite-prefix decoder.
2. The quantitative separator certificate uses the original label and visited-set query descriptor, without that extra prefix.
3. Whole-curve domination fixes the acquisition law across resolutions and allows the larger oracle information only in the converse.
4. A finite menu fixes its conditional member laws and selects a finite index before tapes are observed.

The manuscript also distinguishes quantitative all-budget comparisons, bounded-additive-bit conclusions, contact-order leading coefficients, and the sharp constant of the particular two-trial average-risk problem. Uniform constants are for the fixed graph experiment; no growing-graph uniformity, dependent-edge extension, or exact finite-calibration switching threshold is claimed.

## 5. Historical derivations and preservation

The construction continues the shared-label resource model and independently capped attained blocks already developed in the v10 scheduling material, including its distinction between overlap and unconstrained serial acquisition. The earlier result that a fixed serial schedule suffices when arbitrary serialization is available is not withdrawn. Graph acquisition constraints and resolution reuse are additional questions, not counterexamples to that result.

The v25 graph proof supplies the fixed-order causal construction and the unconditional regular-box input. The v26 revision supplies first-block evidence selection, visited-set capacities and analytic phase notation. Every one of those active inputs remains in `main.tex`. The new directory is a repository-native source overlay; the complete v26 source remains at its original path in the same branch. `build_v27.py` materializes it and overlays the new source. No history, companion proof, review report, old branch or existing source file is deleted or overwritten.

The citation, proof-ledger and genuine-negative-control matters E25.1--E25.3 that the referee regarded as closed are not reopened as newly repaired defects. The reviewed bibliography is retained and one classical quantization source is appended.

## 6. Verification and what is not certified

The new mathematical proofs are in the manuscript. Arithmetic tests are supporting checks, not substitutes for the proofs. `diagnostics_v27.py` checks rational Bayes identities, the full mixed-law mass and first moment, the query metric, every factor of the separator comparison, all 24 star orders and the finite affine arrangement for menus of size at most two. It also constructs a rational monotone-sum enclosure of the sharp coefficient using integer cube-root bounds. The checks use explicit exceptions rather than Python assert, so optimized execution does not erase them.

Native two-volume compilation and PDF visual inspection must be distinguished from these arithmetic checks. The revision supplies a build/materialization command that records its own actual execution status and refuses to certify unresolved references. No native two-volume or visual-layout pass is inferred from an isolated arithmetic run, an earlier revision's log, or the referee's diagnostic counts. `NATIVE_SOURCE_RECORD.json` and the proof ledger define the source and verification scopes.

The new theorems address the stated mathematical scope and quantitative-example requests. Whether their conjunction has the significance required for the four target journals remains an external editorial judgment. This response does not represent that judgment as an acceptance decision.
