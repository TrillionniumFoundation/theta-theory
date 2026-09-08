# Second independent referee assessment of A1 v30

**Manuscript:** *Attainable information, exponent collisions, and adaptive memory*, Qian Qi, September 8, 2026.  
**Repository:** `TrillionniumFoundation/theta-theory`.  
**Controlling submission:** `dc8c1bd475b870cd222627c0cfd6d784363e1728`.  
**Manuscript-bearing parent:** `e7fc18d1f73120527f7a6dfa6f7468b9f20cb435`.  
**Revision branch:** `revision/a1-english-v30-multilevel-minimax-2026-09-08`.  
**Native directory:** `papers/A1-english-v30-multilevel/`.  
**New review branch:** `review/a1-english-v30-harsh-second-independent-2026-09-08`.  
**Requested standard:** Annals of Mathematics, Inventiones Mathematicae, Journal of the American Mathematical Society, or Acta Mathematica.  
**Recommendation:** **Reject at the requested four-journal level.**

This is an owner-requested, AI-assisted referee-style assessment, not a report commissioned by any of the named journals. It is a second examination of the same materialized v30 submission, not an assessment of a nonexistent v31 manuscript. I read the earlier reports, but the mathematical judgments below are not inferred from their recommendations. Independent calculations and their limitations are recorded separately.

## 1. Recommendation to the editor

The revision contains valid-looking, explicitly delimited mathematics and has repaired concrete defects identified previously. I have not established a fatal counterexample to its new named theorems under their printed hypotheses. Nevertheless, I do not recommend publication at the requested level, nor acceptance conditional on a cosmetic revision.

The strongest component remains the collision-uniform attainable-information classification. Its proof connects an executable acquisition model, a uniformly acquired confluent flag, a whole-image covering estimate, and an actual causal update with no reciprocal collision gap. Reducing this component to ordinary dimension counting would be an unfair assessment.

The new statistical network results are considerably less substantial than the paper's overall breadth might suggest. Under conditional regeneration, each currently scored target is determined by a fresh block with a prescribed conditional law. The old state can therefore be overwritten. Once the one-block distortions are known, the network problem is an optimization over a finite convex hull of path-risk vectors. The statistical realization is genuine; the mathematical difficulty of retaining information that will matter later has, however, been removed by the hypotheses rather than characterized by the flow formula.

The general network theorem allows heterogeneous local distortion functions; I do not incorrectly restrict it to the special common-factor example. But the quantitative network-uniform showcase does use a common scalar factor. Its uniform risk-to-certificate ratio follows by exact cancellation of that factor. The unbounded checkpoint penalty is likewise an exact result, but its comparator is an inconsistent collection of checkpoint-specific initial designs, not an admissible competing memory architecture.

These observations do not make the statements false. They limit the significance that can be extracted from them. The submission has not yet supplied a convincing theorem-level account of why the collision classification and the regenerative design results together constitute the exceptional structural advance needed for the requested venues. A complete full-volume publication build also remains unverified. That execution issue is separate from the editorial recommendation and is not evidence of a mathematical error.

## 2. Submission identity, history, and audit scope

The last controlling v30 commit is dated September 8, 2026, 01:07:00 UTC, or 09:07:00 Singapore time. Its parent contains the manuscript addition; the last commit records the native-workflow status.

The branch named `revision/a1-english-v31-causal-compatibility-2026-09-08` was inspected by commit, not accepted at face value. It points to `53810339e445de79a328dd6d41a2eddae2ee663d`, whose change is the preceding v30 referee report. It does not supply a v31 manuscript. The other v30-named branches inspected point to the v29 review or a source-export commit. The revision-branch search was paginated to exhaustion. The manuscript reviewed here is therefore the latest materialized revision located, not the branch with the largest nominal version number.

The v29 report is at `90c7acd0e4efe3280eb1a8faa3c6d9461870c36f`, in `reviews/a1-english-v29-harsh-independent-2026-09-08/REFEREE_REPORT.md`. The existing v30 report is at `53810339e445de79a328dd6d41a2eddae2ee663d`, in `reviews/a1-english-v30-harsh-independent-2026-09-08/REFEREE_REPORT.md`. Both were consulted. Neither is overwritten by this assessment.

All source references below are relative to the controlling native directory. The examination included the three complete new mathematical modules, the active menu correction, `main.tex`, the substantive unified introduction, the response to the referee, the principal rank/confluence/covering/causal-classification proof chain, the explicit risk criteria, and the acquired-law and high-resolution arguments of the evaluated scalar example. Source labels, not unverified PDF theorem numbers, identify results.

This is not a new line-by-line audit of the entire companion, every inherited v25-v29 graph proof, all historical branches, or all eleven papers. In particular, the preceding reports' favorable assessments of components not reexamined here are not converted into fresh verification. No full native two-volume compilation, PDF visual audit, formal proof verification, or exhaustive priority search is claimed.

## 3. Closed objections must remain closed

| Earlier issue | Present disposition |
|---|---|
| Optimized menu excess could allegedly be infinite at a fixed finite graph and calibration | **Closed.** The active passage and its consequence are corrected; the replacement stabilization proof is sound. |
| Statistical realization had only one evaluated checkpoint | **Closed as a factual criticism.** The revision contains multilevel positive experiments. |
| Exactness was only for abstract local path losses | **Resolved on the explicitly regenerative class.** The new equality concerns actual finite-label statistical prediction, not arbitrary posterior dynamics. |
| A favorable event might have exponentially small mass over many stages | **Avoided in the new positive example.** The entire mixed acquired law is retained at every stage. |
| Six chronological introductions in the active article | **Closed at the entry-point level.** There is now one active introduction. Preserved historical files are not themselves an editorial defect. |
| Exceptional mathematical significance of the whole submission | **Not established to my satisfaction.** The reasons are developed below, rather than inferred from the existence of previous negative reports. |
| An executed, current, complete native article-and-companion build | **Still unverified.** Failure with no recorded job steps is not a demonstrated TeX failure. |

The response does not claim that regeneration follows for a shared evolving posterior, that the three loss conventions are uniformly equivalent, or that numerical diagnostics prove the manuscript. Those are important improvements and should not be undone in a more ambitious abstract.

## 4. Examination of the new mathematical statements

### 4.1 Fixed-calibration menu stabilization

**Sources:** `v30/menu_finiteness.tex`; the active insertion in `v27/policy_menus.tex` after `eq:v27-menu-functional`.

The results `thm:v30-menu-finite`, `prop:v30-critical-resolutions`, and `cor:v30-stratum-uniform` survive examination.

At fixed calibration, write x = log2(1/epsilon). After omitting zero volumes, each edge profile is a finite maximum of affine functions with finite intercepts. Expanding a cut sum gives another finite maximum; maximizing over cuts gives the same description for an order profile. Each order is eventually affine. The finite minimum over orders is eventually attained by a lexicographically minimal slope/intercept pair. One such order therefore has bounded excess on the compact initial interval and zero excess thereafter.

The prescribed-menu criterion is also correct: its smallest eventual slope must equal the globally smallest slope. The critical-resolution formula must exclude menus that fail this condition, and the printed formula does. All affine constituents have a fixed ordering between consecutive crossings. On the final interval a slope-optimal excess is constant, so the finite crossing set suffices. No polynomial-time assertion follows from this characterization, and none is printed.

The calibration-uniform corollary requires fixed retained indices and uniformly positive retained volumes. It does not confuse pointwise finiteness with collision-uniform boundedness. I find no reason to reopen E29.1.

### 4.2 Committed routes: exactness with the actual resource convention

**Source:** `v30/multilevel.tex`, `thm:v30-regenerative`.

The equality

$$
\mathcal R_M^{\rm reg}
=\min_{\rho\in\Delta_R}\max_j\sum_r\rho_r d_{rj}(M)
=\max_{\lambda\in\Delta_J}\min_r\sum_j\lambda_jd_{rj}(M)
$$

has the correct quantifiers. Fixing the independent seed fixes the route and the decoder's at most M prediction vectors. Earlier blocks cannot improve the nearest-center lower bound for a fresh current block. Averaging at each checkpoint before taking the maximum is essential, and the proof does so.

For attainment, the controller reads the current block, stores its nearest-center index, and discards the old label. Stage-dependent codebooks are parts of one fixed program, not additional persistent states. Compactness gives minimizing codebooks and a minimizing initial route law. The dual is finite convex separation. The publicly announced route and shared independent seed are explicit resources. The optional RM-label charged-route construction is only an upper bound for a different convention.

This is a correct resolution of a specified statistical design problem. It is not an identification of the local block optimum with the cost of maintaining a nonregenerative posterior.

### 4.3 Predictable networks

**Source:** `v30/predictable_networks.tex`, `thm:v30-predictable-exact`.

The decisive hypothesis is conditional, not merely marginal: after conditioning on the entire pre-acquisition history, the independent seed, and the selected vertex w, the block still has law P_w, and its current query vector is q_w(H_w). This gives

$$
\mathbb E[L_j\mid\mathcal H_j^-,w]\ge d_w(M).
$$

Integrating yields a linear occupation cost x_w d_w(M). Expected arc incidences of an adaptive schedule form one common unit flow. Conversely, an initial random path and fresh reset quantizers attain the costs of a minimizing flow. The shortest-path dual is justified because this particular flow polytope has no additional node caps. That conclusion must not be transferred unchanged to the older capacitated relaxation.

The proof actually establishes that full-history adaptive scheduling does not improve the optimum over the appropriate open-loop randomized path design in this class. That is informative, but it is quite different from an adaptivity gain. The J+1 path-support bound is true. The previous report already observed that an optimal exposed face gives a J-path sharpening; I do not present that observation as a new defect or new finding.

For `prop:v30-predictable-bound`, conditional layer cake gives the linear cost x_w times the integral of 1-c_w. The inequality phi_w(z) <= z phi_w(1), followed by grouping a path decomposition by its first vertex, gives the correct comparison with the earlier anchored relaxation. This uses the unit terminal capacities stipulated here. The ordering Gamma_pred >= Gamma_pre >= Gamma has the right direction.

### 4.4 Positive realization, atoms, and constants

**Sources:** `v27/evaluated_model.tex`; `thm:v30-positive-realization`, `lem:v30-atom-capacity`, `thm:v30-controlled-gap`, `cor:v30-checkpoint-gap`, and `cor:v30-network-gap`.

The acquired measure is not an assumed uniform statistic. Its two atom masses are 5/16 and 3/16. The failure component has mass 1/2 and density bounded by 26 on [10/21,14/27]. The retained failure evidence in the change of variables is essential. The displayed density, evidence, posterior means, and query isometry were examined; the continuous mass was independently integrated with exact rational antiderivatives.

Projection of arbitrary decoder vectors onto the affine query line, followed by clipping, justifies the exact one-block reduction. It is not enough to check centers already on that line, and the proof does not make that mistake. With readout gain s, the distortion is s squared times D_M(nu)/128.

The atom-aware small-ball function is

$$
c_w(t)=\min\{1,1/2+b_w\sqrt t\},\qquad b_w=2HLM/s_w,
\quad H=26,\quad L^2=128.
$$

Its integrated cost is

$$
\phi_w(x)=\frac{(x-1/2)_+^3}{3b_w^2},\qquad
\phi_w(1)=\frac{s_w^2}{8306688M^2}.
$$

The arithmetic identity 96 times 26 squared times 128 = 8306688 and the all-budget factor 8306688/64800 < 129 were independently checked. The midpoint covering bound uses the whole support hull of length 4/45, so it does not forget the atoms. The scalar high-resolution proof handles a continuous density and finitely many atoms correctly by a lower submeasure bound and a finite allocation of atom centers for the upper bound.

The exact network ratio is

$$
\frac{\mathcal R_{\mathscr D,M}^{\rm reg}}{\Gamma_{\rm pred}}
=\frac{8306688}{128}M^2D_M(\nu).
$$

This identity explains its uniformity over finite networks, horizons, and positive gains. The scalar limit formula is supported by the printed quantization proof. The published decimal enclosure in (4.05,4.06) was read in the source and preceding report; its integer-root enclosure was not independently regenerated in this second assessment. It should not be listed as a newly executed check here.

For the J-route diagonal/off-diagonal gain family, uniform row and column strategies give matching primal and dual values 1/J + 1/J^2 - 1/J^3. Dividing by the separate-checkpoint value 1/J^2 gives J+1-1/J. This exact algebra was independently checked. The comparison is a common-design consistency penalty, not a separation between two admitted causal memory classes.

## 5. The inherited collision theorem deserves a more precise publication case

**Sources:** `core/03_transversality.tex`, `text/analytic_inputs.tex`, `text/collision_flags.tex`, `text/collision_direct.tex`, and `text/main_classification.tex`.

The rank calculation constructs an attainable binomial tangent with n(r-1)+1 distinct monomials. The separation of interior one-step exponents from the endpoints makes the exponent blocks disjoint. Strict mixed-moment positivity then applies for every fixed full-support prior, including a singular prior. Evidence normalization removes exactly one direction. This is an acquisition theorem, not simply a statement about the dimension of an ambient future test space.

The confluent proof uses complete Hermite prefixes. Arbitrarily selected high derivatives would not justify the same positivity argument. The positive lower bound on future exponents controls logarithmic derivatives at zero. Compactness and finitely many formal-label permutations give uniform surjectivity. The acquired-law minorization completes the derivative by kernel coordinates and integrates those coordinates after the inverse chart. It does not attach positive mass to a frozen slice of measure zero.

The Leja construction separates small scales from a uniformly bounded triangular coordinate change. Its prefix-volume inequality remains meaningful at exact coincidences, with zero pivots never inverted. Independent rational tests included repeated-node configurations, but these tests are only checks of the finite algebra, not a proof of the uniform acquired-measure statement.

The covering argument is also more careful than an informal local chart argument. The command image is a bounded-format semialgebraic set at fixed calibration, even though the prior moment coefficients need not be algebraic functions of calibration. The affine-section component bound and the real entropy inequality yield a sum of rectangle-volume products only up to the image dimension. The integer-budget step treats small M separately and moves centers onto the attainable set. The externally cited general real-geometric entropy input was not reproved from its original monograph in this review; the submitted specialization was checked for its hypotheses and logical use.

Finally, the causal construction updates raw remaining moments. A segment joining two reachable vectors has a posterior-mixture interpretation, so the Bayes denominator remains a positive report probability. The Lipschitz constant does not divide by a collision gap. Reachable representatives remain reachable after an actual report update. The accumulated errors are retained in a finite-horizon recurrence. The lower argument uses one common exploration law before minimizing over filters.

I did not identify a new defect in this examined chain. Its constants are nevertheless for a fixed experiment, prior, and horizon. Known calibration and budget-dependent code design are allowed. Its resource is persistent labels, not total arithmetic space, numerical bit precision, or computational complexity. None of those qualifications is a flaw when stated; all matter to the significance comparison.

The general regenerative theorem could of course take monomial blocks as its local inputs. Thus it would be too strong to say there is no possible mathematical connection between the two components. What has not been shown is a consequential new control of their nonregenerative causal interaction. Substitution of independently solved blocks into a design program is not that interaction.

## 6. A stronger scope control: positive local costs do not encode causal compatibility

The earlier v30 report gave a two-bit example with zero separate-checkpoint costs. The following extension removes the zero-denominator feature and makes the acquisition likelihoods uniformly positive. It is a diagnostic of the boundary of the new realization principle, **not a counterexample to a printed v30 theorem** and not an assertion that the scalar monomial theorem covers this example.

### 6.1 Two positive Bayesian experiments with the same current-target marginals

Let A1,A2,C1,C2 be independent fair signs in {-1,1}. Observe each sign through an independent binary channel with probability 3/4 of reporting it correctly. Denote the corresponding reports by X1,X2,U1,U2. Every complete acquisition-word likelihood, conditional on any latent word, is at least 1/256. The four reports are independent fair signs, and the posterior expectations of the latent signs are their corresponding reports divided by two.

Fix 0 < epsilon <= 1/16. At checkpoint j the scored Bernoulli event has latent conditional mean

$$
\frac12+\frac14 A_j+2\epsilon C_j.
$$

This number lies in [1/8,7/8]. Its full-history mean, once the relevant reports have been acquired, is

$$
q_j=\frac12+\frac18 X_j+\epsilon U_j.
$$

The readout probabilities and acquisition likelihoods are uniformly positive throughout the family. Predictions are evaluated at a selected checkpoint in a separate run of the same controller, as in a maximum-of-checkpoint-expectations criterion. A scored query outcome is not a later input, earlier outputs cannot be read back, and the clock carries no data. This convention rules out an accidental score-feedback storage channel.

In the **fresh schedule**, (X1,U1) is acquired at the first checkpoint and the independent pair (X2,U2) at the second. In the **delayed-use schedule**, all four reports are acquired before the first compression; between checkpoints only an independent uninformative report is supplied. Both schedules use M=2 retained labels, an independent public seed, and the same two current-target marginal laws. The descriptor is a fixed stage number, not a data-dependent side channel.

At either checkpoint, a separately optimized full-history two-center code has distortion

$$
d_1(2)=d_2(2)=\epsilon^2>0.
$$

To verify this, put a=1/8. The four centered target values are -a-epsilon, -a+epsilon, a-epsilon, a+epsilon, each with probability 1/4. Grouping by the sign X gives distortion epsilon squared. In one dimension a nearest-center partition is contiguous. A singleton-versus-three partition has distortion (2/3)(a^2-a epsilon+epsilon^2), which is at least epsilon squared for epsilon <= a/2. The one-center choice is worse. These exhaust the relevant cuts.

The fresh schedule is regenerative, and reset encoding therefore gives exactly epsilon squared for the common-controller risk. The one-path local-distortion flow expression is also epsilon squared for either collection of these marginal data.

### 6.2 An analytic lower bound for delayed use

Write R_del for the delayed-use common-controller risk. Then

$$
\frac1{128}\le R_{\rm del}\le\frac1{128}+\epsilon^2.
$$

For the lower bound, grant both encoder and decoder the nuisance pair (U1,U2) for free. This is a relaxation. Conditional on that pair and the independent seed, subtract its known offsets. The two targets now form the four equiprobable corners (a X1,a X2) of a square, with a=1/8. A two-label controller, with no later informative observation, provides at most two reconstruction vectors. Optimized cell centroids suffice for squared loss; randomized assignments cannot improve the nearest-center sum of losses.

The unordered partitions of the four corners have the following minimum total squared errors. An adjacent two-versus-two partition gives a^2; a singleton-versus-three partition gives 4a^2/3; a diagonal partition or a single cell gives 2a^2. Thus the sum of checkpoint risks is at least a^2 even in the relaxed problem. Averaging the independent seed and taking the larger checkpoint risk gives a^2/2 = 1/128.

For the upper bound, a fair independent seed selects which of X1 or X2 to retain. At its associated checkpoint predict 1/2 + X_j/8; at the other predict 1/2. Ignore both nuisance reports. At each fixed checkpoint the averaged risk is a^2/2 + epsilon^2. No past output or uncharged data-dependent descriptor is used.

Consequently,

$$
\frac{R_{\rm del}}{\max_j d_j(2)}\ge\frac1{128\epsilon^2}\longrightarrow\infty.
$$

This analytic conclusion does not depend on a numerical test or on the exhaustive certificate below. Both local costs are strictly positive. Uniformly positive likelihoods and readout probabilities do not restore a multiplicative realization bound from current-target marginal distortions alone.

### 6.3 Exact finite certificate and reproducible values

The accompanying script further evaluates all 32,768 unordered partitions of the sixteen equiprobable report words into at most two cells. Symmetry under exchange of the two coordinates makes half the minimum sum of distortions the exact randomized maximum-checkpoint optimum: symmetrize an optimal partition with its coordinate-swapped copy by an independent public seed.

The resulting exact values are:

| epsilon | Local/fresh-schedule risk | Delayed-use risk | Ratio |
|---|---:|---:|---:|
| 1/16 | 1/256 | 3/256 | 3 |
| 1/32 | 1/1024 | 9/1024 | 9 |
| 1/64 | 1/4096 | 33/4096 | 33 |
| 1/128 | 1/16384 | 129/16384 | 129 |

There is also a finite integer certificate for the parameter-uniform identity R_del = 1/128 + epsilon squared over the whole stated epsilon interval. Here are the exact mathematical conditions checked, so the computational scope is explicit.

Put k=1/(8 epsilon) >= 2. For a nonconstant partition cell of size n, let Sx1,Sx2,Su1,Su2 be the sums of its four report signs. The explained sum of squared centered target coordinates, after division by epsilon squared, is

$$
\frac{(kSx1+Su1)^2+(kSx2+Su2)^2}{n(16-n)}.
$$

Its being at most k squared is equivalent to P(k) >= 0, where

$$
\begin{aligned}
P(k)&=Ak^2+Bk+C,\\
A&=n(16-n)-Sx1^2-Sx2^2,\\
B&=-2(Sx1Su1+Sx2Su2),\\
C&=-Su1^2-Su2^2.
\end{aligned}
$$

The script exhausts the 32,767 nonconstant unordered cells and verifies, using integers, A >= 0, P(2) >= 0, and P'(2) >= 0. These imply P(k) >= 0 for every real k >= 2. The partition by X1 attains the explained variance k squared. The centered total variance is 2(k squared + 1), so the minimum total distortion is epsilon squared times (k squared + 2). Symmetrization gives the claimed identity.

This is an exhaustive computational certificate for this sixteen-atom control, not a formal verification of A1. The simpler analytic lower and upper bounds already suffice for the unbounded-ratio conclusion.

### 6.4 What this control does, and does not, establish

The two schedules have identical currently scored marginal laws, identical positive local distortions, and the same unique-path cost optimization, but different causal risks. Their acquisition timing and future information differ. In the delayed-use schedule, the second target depends on discarded past data rather than on a fresh sufficient block; it violates the printed regeneration hypothesis. Therefore it does not contradict `thm:v30-predictable-exact` or its 129 bound.

It also does not defeat the manuscript's full-future-test-space approach. If the first checkpoint is tested against all relevant future continuations, the information geometry includes both later-relevant coordinates, and the local object changes. That is precisely why the inherited attainable-future-information spine is more substantive than a flow of current-block distortions alone.

This control sharpens the earlier report's boundary test. It does not create a new demand that the authors solve every nonregenerative problem, and solving this small example alone would not establish a four-journal contribution. Its role is to prevent a general causal-compatibility claim from being supported only by local marginal costs, positivity, and flow feasibility.

## 7. Remaining publication-level objections

### S2.1 — The exact realization solves a separable problem

The general new theorem consists of local quantization, convexification of path risks, and an attaining reset implementation. The statistical implementation deserves credit; its existence is made possible by current-block sufficiency and conditional regeneration. No result is shown in which a locally optimal code must preserve a competing direction for a later target, or in which the flow constraints alone encode such preservation.

The objection is not that a short proof cannot be deep. It is that the central new exactness does not resolve the causal information constraint that motivates the broader discussion. Section 6 supplies a stable mathematical boundary for this objection with strictly positive costs, rather than an impression based on theorem names.

### S2.2 — The quantitative uniformity claim is narrower than a uniform memory theory

In the positive-block application, true risk and certificate carry exactly the same design factor. Their ratio is therefore scalar. This is valid even when the finite graph or positive gains vary with M. It does not establish uniform error propagation of a shared posterior, a uniform bound for correlated acquisitions, or equivalence of tensor-only and local-plus-tensor loss as graph size grows.

The source now states these distinctions correctly. I am not requesting that they be deleted, weakened, or concealed. I am asking that the publication case not count several differently weighted tasks as one demonstrated operational generalization.

### S2.3 — The divergent comparison is not between two admissible competitors

The J+1-1/J result supplies the requested multilevel positive example, but the separate-checkpoint procedure uses incompatible initial route choices. The result is a common-design penalty. It does not demonstrate that adaptive scheduling beats an admissible open-loop design, that one finite-memory architecture beats another, or that cross-time posterior compression has been characterized.

A further increase of a ratio against the author's own relaxed certificate would not by itself strengthen the editorial case. The paper needs to articulate which legitimate statistical decision problem becomes substantially better understood because of its main theorem, with information, query timing, loss, and memory charged on the same terms.

### S2.4 — Novelty must be located theorem by theorem

There is real attained-geometry content in the scalar theorem. There is also a large amount of established quantization, total positivity, real-geometric covering, finite minimax, and occupation-measure methodology. The submission should state the precise new implication obtained from this combination and compare hypotheses and conclusions with the nearest relevant results. Merely declaring the full package novel does not do that work.

Conversely, this referee has not established that an existing paper contains the complete A1 theorem. A vague assertion of prior art would be as inadequate as a vague claim of novelty. The targeted comparisons in Section 9 are deliberately limited.

### S2.5 — A preserved source archive is not yet a finished submission

The active-introduction problem is repaired. The unresolved issue is the hierarchy of the mathematics and the readiness of the complete publication object, not the existence of historical source files. The manuscript needs a clear leading theorem and an economical explanation of how its subsequent developments depend on it. Preserving complete derivations is compatible with that requirement; deletion of valid content is not requested.

## 8. Requirements for a substantive reconsideration

**R2.1 — Identify the publication-bearing advance.** State which theorem carries the submission and what it adds beyond its closest predecessors. Give a hypothesis-and-conclusion comparison rather than a generic bibliography. Keep the genuinely attained collision result distinct from the elementary finite convexification it may feed into.

**R2.2 — Make the operational consequence consequential.** Either substantiate a strong consequence of the existing collision spine, or demonstrate a comparably significant interaction in a clearly specified model where retained information has nontrivial future value. This explains the present significance deficit; it is not a demand for a universal theorem as a repair of a false statement, and it is not a promise of acceptance after any single addition.

**R2.3 — Preserve a model ledger.** At every principal result make explicit: data seen before selection; data available at decoding; public descriptors and seed access; whether scores can feed future updates; the point where memory is charged; the order of maximum, expectation, and infimum; and whether the target is a current query or the entire relevant future family. The current source gets most of these distinctions right. A compact ledger would prevent an expansive introduction from outrunning them.

**R2.4 — Keep prior repairs closed and supply the complete publication build.** Preserve the fixed-calibration correction and the distinctions among the original tensor, mixed, and attenuated regenerative tasks. Supply an executed native article-and-companion build at a pinned commit, with cross-volume references resolved and output inspected. Neither additional check counts nor a clean build alone would reverse the editorial recommendation.

## 9. Targeted primary-source positioning

These are contextual comparisons, not an exhaustive priority determination or a claim that any cited work subsumes A1.

**[P1] S. Graf and H. Luschgy, *Foundations of Quantization for Probability Distributions*, Lecture Notes in Mathematics 1730, Springer, 2000; DOI 10.1007/BFb0103945.** The publisher record identifies the general and asymptotic quantization theory relevant to the one-block distortion and its high-resolution constant. The submitted acquired positive mixture and its geometry still require their own analysis. The elementary high-resolution argument actually printed in A1 was examined directly.

**[P2] R. G. Wood, T. Linder, and S. Yüksel, *Optimal Zero Delay Coding of Markov Sources: Stationary and Finite Memory Codes*, arXiv:1606.09135, revised April 5, 2017.** The authors' record treats sequential coding through stochastic control, including structural optimality results for finite-state Markov sources. It is a relevant comparison for causal coding claims. A transmitted-symbol alphabet and decoder-accessible communication history are not automatically the same resource as A1's persistent-label transducer. Any claimed reduction must establish that correspondence; this review does not assume it.

**[P3] D. Batenkov, B. Diederichs, G. Goldman, and Y. Yomdin, *The spectral properties of Vandermonde matrices with clustered nodes*, arXiv:1909.01927, revised July 24, 2020.** This research concerns clustered-node Vandermonde spectral and conditioning estimates. It is relevant to separating collision linear algebra from A1's attainable nonlinear statistical image. It does not by itself establish the acquired-mass statement, the fixed-prior positive experiment, or the causal finite-label realization in A1. Those differences should be made into a precise contribution argument, not ignored in either direction.

The arXiv abstracts and the Springer bibliographic record were checked. No page-by-page audit of these external works or theorem-by-theorem equivalence proof is claimed. The finite convex-hull separation used in v30 is assessed from its printed proof; its correctness does not depend on assigning novelty to linear-programming duality.

## 10. Executed diagnostics and reproducibility limits

The accompanying `independent_checks.py` was written independently of the author's implementation. It uses the Python standard library, exact rational arithmetic, integer comparisons, and explicit exceptions rather than removable assertions. It was executed under normal Python and under `python -O`; the JSON outputs were byte-identical.

Script SHA-256:

`bffb8c8474b8dedc2fa128782dcc2aed0e20d4f74b38e255ac70398dde6f82ce`

`INDEPENDENT_CHECKS.json` SHA-256:

`633367c48ed6609b411f12f8205abb5980104a6f26cdb7209dbdde62f057984b`

The checks include positive acquisition likelihoods and posterior identities for the new control; all two-cell partitions at four rational parameters; the separate integer certificate over all real k >= 2 for that control; exact acquired continuous mass; atom-aware constants; matching symmetric-design primal and dual values for J=2 through 16; and 126 rational five-node multisets, including collisions, for the Leja prefix-volume inequalities. The JSON separates these families. Counts are not a measure of manuscript correctness.

The control's exhaustive certificate is genuinely finite and algebraic. It does not certify arbitrary real-geometric images, all priors, uniform inverse charts, measurable scheduling classes, global covering, or every inherited theorem. The uniform analytic bound in Section 6.2 is deliberately available independently of the certificate. The author's historical diagnostic suites were not rerun.

The live native job record was inspected: run `34175506178`, job `101903965773`, manuscript-bearing SHA `e7fc18d1f73120527f7a6dfa6f7468b9f20cb435`, conclusion `failure`, empty `steps`, and runner identifier zero. These fields establish neither a successful TeX build nor a TeX error. The failure cause is not determined here. The author's ten-page new-results packet is a narrower reported build, not a full native two-volume build; it was not independently reexecuted in this review.

No workflows, branch protections, manuscripts, prior reviews, or main-branch files are changed by this review. Only a new review directory is added on the new branch.

## 11. Source fingerprint ledger

The following blob identities were returned for the controlling submission. They identify the principal evidence rather than claiming an exhaustive preservation audit.

| Source | Git blob SHA |
|---|---|
| `main.tex` | `f9fe30cf113b659f8ff7f1fb17ec0e23ffc3892c` |
| `v30/menu_finiteness.tex` | `1094ac4b19b09dc84b4b507a376a601430f81710` |
| `v30/multilevel.tex` | `78ccdf5a2939d9d0807c82c277c3ced84eafb305` |
| `v30/predictable_networks.tex` | `b48912ab940a9c1c947e7e6a93143f845158fc49` |
| `v27/policy_menus.tex` | `82cb58f0327dad01c8b15f45ac390ac23f0d78c4` |
| `core/03_transversality.tex` | `6395724ba2c4bed3ead19178a1cfe8206f9a3824` |
| `text/analytic_inputs.tex` | `92c431918df8894dbab4e2bef267a1b3d086370c` |
| `text/collision_flags.tex` | `558972ba3ad6f42ca1f782b80fed4b7ef9a87fe8` |
| `text/collision_direct.tex` | `12db8bce89cd0a731cb3bc5c383c3c70699ced60` |
| `text/main_classification.tex` | `307a694dacddee85104212dfa51a222053ee1769` |
| `risk_criteria.tex` | `da5403fdde6bed138d33b252d52d75e4255c8528` |
| `RESPONSE_TO_REFEREE.md` | `3a553a3096695f8345c5072051a669480df1aa96` |

## 12. Final verdict

**Reject at the requested four-journal level.** The concrete fixed-calibration error has been repaired, and the new regenerative statistical equalities should not be dismissed as false. The remaining negative judgment concerns the depth and unity of the demonstrated advance: the exact new network theory can reset away past information, its strongest uniform quantitative example factorizes, and its divergent comparison is against incompatible local designs.

The strengthened positive-risk control shows why those qualifications are substantive without claiming a counterexample outside the theorems' hypotheses. The collision-uniform attained-information theorem remains the most promising publication-bearing component, but the present manuscript has not yet made a sufficiently persuasive case for the exceptional significance of the combined submission. This recommendation concerns the work now supplied; it is not a judgment that the research direction is impossible, a demand to erase valid derivations, or a substitute for evaluating future substantive mathematics.
