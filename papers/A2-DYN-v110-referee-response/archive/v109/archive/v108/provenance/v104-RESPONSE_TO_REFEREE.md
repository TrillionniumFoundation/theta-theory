# Response to the latest submission-state report and the mathematical report on A2-DYN v102

Author: Qian Qi. Revision: 104, 14 October 2026.

Latest frozen report: `reviews/a2-dyn-v103-submission-state-external-top4-review-2026-10-13/REFEREE_REPORT.md`, blob `952e695da87ea365053f284cff18b819e80a48e4`. Mathematical report: v102, commit `37faf38478a5b561c3aa4a1faf63da378caf8189`, blob `6c6bbd2fc9fd5e6da575ac6db9827448e091af3d`.

Immediate actual author baseline: v103 at `7949b93131806711109c8f126d2a56fe37da7b59`, paper tree `3657fe1eb821ec398484f0487f3a8095dd44deed`. Its theorem-bearing source was added after the submission-state report froze. This revision preserves that source rather than treating its old placeholder as the current manuscript. All prior review texts remain immutable.

We thank the referee for requiring a positive essential-height estimate on the actual endpoint minimum. The new argument compares angular intervals of that same positive measure, instead of introducing another reciprocal-velocity flow. It gives an original-roof bound with integrated trace balance and physical overlap as the only costs. On backward-critical arms a level-width condition controls the incoming trace balance; any shortage of the outgoing trace is paid by the actual uncut optical variation. No lower endpoint speed or pointwise logarithmic trace bound is assumed.

## 1. Actual author source and submission identity — latest report 11.1, 11.8

The packet contains a new article and modules 250–252, its manifest, this response, strict verification tools and a dedicated workflow. It is based on the actual v103 source, not on a relabeled review commit. The two intended new author refs are `revision/a2-dyn-v104-positive-interval-referee-response-2026-10-14` and `revision/a2-dyn-v104-positive-interval-referee-copy-2026-10-14`. Publication remains a separate verifiable action; the packet does not report a placeholder or local file as a remote author commit.

## 2. Complete failure and quantitative recovery — latest report 11.2–11.3; v102 requests 17.1–17.2

Theorem `thm:v104-block` is a finite-count pointwise estimate on the original positive paired measure. A source angular interval is compared with actual trajectories whose roof intervals contain its one-sided roof translates. Integrating their original positive endpoint minima gives an explicit mass ratio. The original selector remains on the starting roof. Summation precedes the pointwise norm and pays a physical overlap bound, never a chamber count.

The exact coefficient alpha=min(1,kappa D/C) splits the original failure into a paid positive part and an unpaid positive deficit. The latter is bounded by (C-kappa D)_+ on the corresponding roof support. Under N kappa <= C epsilon^-1/32, the recovered part has essential height O(B^-1/384). For uniform balance it has O(B^-1/192) height. These are positive-source estimates, not signed differences or local mass bounds.

The complete failure request is advanced but not closed: full physical interval coverage and disappearance of every uncovered or trace-deficient part remain unproved. The final theorem keeps this exact positive remainder. Its equivalence with the original scalar assertion is not offered as a proof of its vanishing.

## 3. Stationary critical corners — latest report 11.4; v102 request 17.3

The retained regular critical trace has the form N_*/Q_*(theta), with lambda <= Q_* <= Lambda. It can be positive, and remains the incoming side of the original minimum. Write the actual outgoing roof as a_*+d+psi(x), d<=delta/2, on a monotone physical arm. Source levels below delta/2 are compared with levels between 2delta and 3delta on that same arm.

Lemma `lem:v104-arm-balance` proves C/D <= Lambda K/(lambda mu log(3/2)) when x psi'/psi <= K on the comparison interval and the average of min(1,f_+/f_-) is at least mu there. The averaged condition permits the outgoing fraction to vanish on positive-measure subsets. No derivative of the positive minimum is used. Finite-order stationary profiles psi~beta x^k are covered with K=k+1 on their actual valid neighborhoods, including k>1 and arbitrarily small source endpoint speed.

Theorem `thm:v104-stationary` therefore gives the entire selected physical-arm height, including every relative source position and approach to a critical entrance. Actual continuation to the comparison levels and the average outgoing fraction remain explicit hypotheses, not claims proved universally by definability.

The model a=0,b=x^k,c=1 verifies that all three older capped clocks can be below any positive threshold on a set of positive paired measure, while the interval balance remains bounded. This is a model of the comparison mechanism, not an assertion of a second physical realization or a verified nonempty Lorentz subclass.

### The entire deficient outgoing trace is also paid

Theorem `thm:v104-paid-arms` removes the average outgoing-fraction assumption for these actual critical arms. Let P be the integral of the incoming critical trace on the comparison interval, D the integral of the paired minimum, and E=P-D. The incoming normalization and geometric width ratio give C<=kappa P, hence (C-kappa D)_+<=kappa E. The entire E is bounded by the original weighted trace variation on the same comparison segments.

At an active original roof t, their common incoming roof lies in (t-delta,t), and every comparison interior lies in (t-delta,t+4delta). Disjoint physical angular arms therefore sum their variation with multiplicity one into the actual uncut source v^0 over that single fixed roof window. This proves a finite-count pointwise deficit estimate C kappa (1+epsilon^-1) integral v^0. The resulting deficit height is O(epsilon^3) for a bounded geometric ratio, or O(epsilon^(95/32)) for the permitted growing ratio. Thus poor outgoing trace balance on this critical class is genuinely estimated, not moved into another uncontrolled admission set.

Corollary `cor:v104-whole-arm-recovery` removes the whole selected stationary-critical arm contribution from the old positive three-clock failure. What remains unproved is coverage/height control for the outside source, including insufficient actual angular reach and flat or singular families. The unrestricted original theorem is still not marked complete.

## 4. Summation and comparison convention — latest report 11.5; v102 requests 17.4, 17.6

The new proof does not introduce a Jacobian. It integrates the unchanged density c dtheta du directly. The interval inclusions are stated for almost every pair of source and comparison angles. Fubini identifies the required target interval for an active source roof, and Tonelli performs the complete positive sum. For disjoint physical angular arms the comparison overlap is exactly one. Coincident geometrical faces on distinct incident sheets are never silently identified.

The old pullback covariance remains byte-preserved in the supplement. No inverse Jacobian is deleted from an old formula; the new argument uses a different, explicit integral inequality.

## 5. Schedule, exact data and topology — latest report 11.6

The original epsilon(B)=A_0 B^-1/12 and delta=O(epsilon^4) are unchanged. The new width is r=delta and the comparison collar is 4delta. All balance budgets, physical intervals and overlap bounds are fixed before the collision limit. The leading epsilon power is 1/16 for bounded balance and 1/32 for the larger epsilon^-1/32 budget. The original unaveraged source is on the left; only its positive comparison is averaged.

Exact displacement, occupation, collision count, initial and terminal tests, original smooth guard, source normalization, all arithmetic peaks and zero classes remain unchanged. No neighboring labels are pooled and no point-conditioned law is normalized on a zero class.

## 6. Qualification repair

The actual v103 copy run 38387122726 failed before TeX in `verify_v103.py` with `RuntimeError: inherited core count`. Its nested-directory `git ls-tree -rz <tree>` lacked `--full-tree`, so Git applied the current-directory prefix to the supplied paper tree. The new verifier uses `git ls-tree -rz --full-tree` and checks both Git records and working-copy modes/bytes. A temporary-repository regression reproduces the empty enumeration and verifies the complete enumeration. No inherited file or count assertion is removed to obtain a pass.

The new native archive includes all 249 preceding cores and the complete v103 article; its union with the new article must contain exactly 252 cores. Local staged compilation and remote final-SHA qualification have separate receipts. The failed v103 run and the successful v102 baseline run are not described as qualification of v104.

## 7. Independent review and writing architecture — latest report 11.7 and section 12

No independent human specialist review or formal proof certificate has been obtained. The appendix locates the inherited positive-trace, critical-extension and scalar inputs and the three new proofs. The focused article retains the original problem, gives the new pointwise comparison and stationary-arm proof, and states the precise positive deficit. The complete preceding article and all historical mathematics remain in the technical archive. No alternate topic or lower journal objective is substituted.
