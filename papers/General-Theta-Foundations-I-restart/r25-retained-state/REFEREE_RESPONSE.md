# Response to the external R24 referee report

## Submission and fixed review object

The revised submission retains the title **General Theta Foundations I: Acquired Geometry and Causal Resource Transfer**, by Qian Qi. This response addresses the complete external report at `36422feadc4ccb99aaf12efb33a18bfd44cb3646`, report blob `4cbd264815d33cfda32298429f2775e5b0d8f091`, reviewing R24 at `45cb3e29a131c1c6c2179746d897e7082ed1a762`. The canonical starting point is `18000b21e4bfd89180ccb069e46ac0f21621f34d`. The report did not identify a fatal correctness defect. Its principal objection was that compulsory observer overwrite removed the cross-cycle information problem. We address that objection mathematically rather than changing the subject, weakening the intended foundations program, or claiming acceptance by a journal.

The new article is self-contained for its retained-state theorem. R24 is retained intact as Companion C; its complete predecessors remain B/A/X/W/V/U/T/S. They are provenance and comparison, not hidden premises of the new proof. Exact theorem numbers are also exported from the built auxiliary file. The references below use stable source labels.

## Principal mathematical revision

The main theorem (`thm:main`) replaces compulsory joint reset by a physical fresh preparation **with the observer label retained**. The complete cycle law depends on that label. Its boundary transition P, conditional mean duration d and reward r therefore form a Markov-renewal object, not an iid sequence. The true average is the initial-state-weighted sum of the separate closed-class ratios pi_C r / pi_C d. Pooling numerator and denominator before mixing the classes is incorrect and is explicitly tested by a counterexample.

The program is parameter-independent and stationary. Every action, preparation row, ordinary/end report row and fixed readout is counted in the same M-state interface. No extra cycle counter, retained seed, history tape, posterior register or report-to-readout bypass is supplied.

The quantitative boundary invariant is h(P), the row-sum norm of the group inverse of I-P. On a compact matrix family its uniform boundedness is equivalent to continuity of the Cesaro projection, local constancy of the recurrent rank, and uniform Cesaro convergence for all initial states and bounded rewards (`thm:regularity`). The underlying finite-dimensional matrix identities are classical and credited to Meyer. The new causal theorem uses this criterion to define a closed, common-program recurrence class, allows periodic and multichain boundaries, proves robust attained average risk and finite-model determination, and derives uniform finite-acquisition and discount comparisons. For finite model sets, the unrestricted M-state infimum is the decreasing infimum over these recurrence sublevels; unrestricted attainment is characterized by reaching one finite sublevel. Uniformity as the recurrence bound diverges is not asserted.

The proof pays separately for physical return tails and retained-state recurrence. Its physical-call estimate is `(3 mu_bar (2M+1)H + sum_{s=0}^N a(s))/N`, capped at one. With only conditional entering-label `1+p` moments, the displayed uniform polynomial estimate pays **M K**, not K: summing a supremum over different entering-label lifetime laws must not be silently replaced by the moment of one lifetime. A common stochastic dominating lifetime removes that factor. The queue application has such a domination and receives an independent explicit bound `17/N` and `17(1-beta)`.

The geometry theorem (`thm:geometry`) uses the actual class-weighted occupation measure, not preparation mass. A Q-state retained exploration and J prediction centers per fiber use QJ labels; the joint boundary group inverse is bounded by H+2. Candidate-valid global covers and actual occupation-weighted gains give the upper, and actual small-ball submass gives the lower. Joint-control lower and upper variational curves are stated separately. Their matching rate requires uniform lower witnesses over admissible control and an attaining fixed-size exploration with the stated upper certificates. A fixed-policy example is not promoted to unrestricted optimal control.

A complete scored-cycle defect theorem (`thm:defect`) now also accounts for boundary-class sensitivity through the group inverse of the physical-time-changed matrix. Same-M effective certification is proved in a support-stable graph architecture; arbitrary rounding is not claimed to preserve the recurrence constraint. Primitive classical and quantum comparisons, a forest denominator bound, integer row rounding and an exhaustive table count are supplied.

## Responses to the twelve major requests

| Report request | Revision and exact boundary |
|---|---|
| 11.1 Put compulsory observer reset in the headline | Replaced by a retained-state central theorem. Physical preparation remains prescribed and paid. Retained observer information is not erased. The old compulsory-reset result remains accurately identified in Companion C. |
| 11.2 Compare finite-memory long-run POMDP theory | The introduction and comparison section distinguish fixed M and recurrence certificates from the approximation results of Chatterjee--Saona--Ziliotto and Venel--Ziliotto. Their results are not claimed as corollaries or special cases. |
| 11.3 Compare restart and intermittent observation | The cited restart preprint and published intermittent-observation paper are compared by information pattern, objective and memory class. A physical boundary, a chosen restart, intermittent full observation, and a reset of the observer are not equated. |
| 11.4 Separate average optimization from fixed-exploration geometry | Main theorem part (v) and the geometry section give explicit lower/upper control envelopes and additional conditions for matching. The abstract and comparison table retain this distinction. |
| 11.5 Stationary implementation | Every required phase variable is either currently visible or charged in the controller label. The QJ product, state-only readout timing and boundary lift H+2 are proved. |
| 11.6 Operational return envelope | `prop:drift` gives a killed-kernel Lyapunov inequality uniform in every physical state and legal action, and a positive-dual quantum version. It covers endogenous termination, not only an independent clock. |
| 11.7 Domination versus nondomination | Finite-history product domination remains explicit. Zeros, common singular references and rank changes are allowed. The direct holding theorem has arbitrary preparation families, but is not used to infer general nondominated adaptive compactness. |
| 11.8 Effective inputs and constants | All input certificates remain listed. The controlled busy-period theorem derives them from raw transitions and gives numerical constants 17/N and 17(1-beta) uniformly over the declared M=2 architecture. The compiler is exhaustive, not an efficiency claim. |
| 11.9 Natural application | Controlled, partially observed queue busy periods have natural physical regeneration, unbounded workload, endogenous return, and no observer reset. We prove a fixed-memory robust theorem there. We do not claim that this settles a previously recognized open queue-control problem or that a journal has certified its impact. |
| 11.10 Finite-model novelty | The finite-intersection argument is explicitly standard. The work is the common Borel-program topology, retained-state regularity, and uniform physical-time passage. |
| 11.11 Complexity | The revealing-POMDP complexity preprint is cited. The support-stable forest bound makes finite evaluation explicit, but no efficient general synthesis or optimal complexity classification is claimed. |
| 11.12 Foundations scope | The title and mother problem remain. The abstract immediately identifies physical regeneration with retained state, the recurrence certificate, and conditional geometric matching. Unrestricted nonregenerative theory is not claimed. |

## Two independent raw realizations and singular content

`thm:queue` derives the general hypotheses from controlled nearest-neighbor workload kernels with upward probability bounded strictly below one half. A uniform exponential Lyapunov function works for all history-adaptive actions. No finite belief dimension is assumed for that unbounded physical model. A finite hidden-load factor supplies a separate geometric task, explicitly not the full queue predictive quotient.

`thm:quantum` derives the same exact/effective hypotheses from unnormalized positive instruments and a dual drift inequality. Noncommuting alive/jump Kraus operators have state-dependent survival, visible terminal flags, real audit back-action and rank changes. The observer is classical and fully counted; the physical quantum system is not free quantum observer memory.

`prop:endogenous` verifies actual acquired geometry in both finite hidden and noncommuting quantum classes with state-dependent returns. Alive normalized updates can expand: with survival values between .09 and .10, the all-candidate bound is 20/9, greater than one, but survival-weighted squared gains are summable. The actual fresh-load submeasure has positive physical-time mass, and the continuous quantum stratum retains its true mixture weight. Singular holding laws, actual length bias, common Cantor/countable references and rank strata are retained as substantive theorems.

## A correction required by retained information

The old joint sharpness experiment used a fixed hidden bit that was sometimes revealed on short cycles. With retained state, an observer can remember that bit after a reveal. We do **not** transfer that lower bound to the new interface. The new attained joint law (`thm:joint`) uses a fresh physical bit each cycle, but keeps the inaccessible calibration sign fixed across the path. It proves the lower against every retained M-state observer and an upper with `3 floor(M/3)` labels. The complete-cycle deficiency is exactly e/2 in the stated task-preserving simulator class: the true audit wire is environment-owned, its value cannot be fabricated, and the virtual bit must be issued before later acquisitions. Without that audit compatibility, a different unrestricted simulation problem could have zero deficiency. This distinction is part of the theorem, not a hidden convention.

The resulting selected slice is `M^{-2/d}+delta^2+epsilon^{p/(1+p)}` after bounded-loss normalization. It does not constitute a matched full region for program length, scratch space, planning time and minimum simulator state. Finite-N comparisons are signed approximation bounds, not an invented positive acquisition penalty.

## Technical and provenance requests

The accompanying `REFEREE_COMMENT_CONCORDANCE.md` addresses all thirty numbered technical comments. The appendix expands cycle timing, measurable density construction, first-load occupation weights, nonexpansive finite-horizon counting, explicit queue moments and informationally complete singular values. The published 2025 Yüksel history-space article and directly adjacent primary literature are cited (the author spelling in the article is typeset correctly).

All ordinary manuscript sources, auxiliary proofs, audits and the source manifest are bound before building. Build and finite regression receipts are separate from mathematical proofs. The previous corrected R24 calibration normalization and its superseded earlier build remain historical facts; the new manuscript uses the full `diam(K)^2+5` normalization. Neither original R24 proofs nor old review, realization or archive branches are overwritten.

## Remaining mathematical questions

The revision closes the forced-observer-overwrite limitation for physical regeneration under a near-necessary **cost-universal boundary regularity** certificate, not for all nonreset partially observed experiments without assumptions. It does not prove a necessary-and-sufficient recursive geometry classification, general nondominated adaptive controller compactness, uniformity across unbounded recurrence degeneration, efficient synthesis, or a full multi-resource lower region. For an infinite model family a single controller need not have a uniform finite boundary constant. The conditional matching control hypotheses are not automatically verified by either fixed-exploration example. These are genuine remaining questions, not changes of topic or substitutes for the proofs supplied here.

Independent correctness, priority, and general-journal significance remain for external assessment. No finite check, workflow run, branch name or reproducible PDF is presented as a proof certificate or an editorial decision.
