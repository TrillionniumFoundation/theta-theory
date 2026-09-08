# Independent referee report on A1 English v30: multilevel minimax revision

**Manuscript:** *Attainable information, exponent collisions, and adaptive memory*, Qian Qi, 8 September 2026.  
**Repository:** TrillionniumFoundation/theta-theory.  
**Reviewed branch:** `revision/a1-english-v30-multilevel-minimax-2026-09-08`.  
**Controlling submission:** `dc8c1bd475b870cd222627c0cfd6d784363e1728`.  
**Submission timestamp:** 8 September 2026, 01:07:00 UTC / 09:07:00 Singapore time.  
**Manuscript-bearing parent:** `e7fc18d1f73120527f7a6dfa6f7468b9f20cb435`.  
**Native directory:** `papers/A1-english-v30-multilevel/`.  
**Review branch:** `review/a1-english-v30-harsh-independent-2026-09-08`.  
**Requested standard:** Annals of Mathematics, Inventiones Mathematicae, Journal of the American Mathematical Society, or Acta Mathematica.  
**Recommendation:** **Reject at the requested four-journal level.**

This is an owner-requested, AI-assisted independent referee-style assessment. It is not a report commissioned by, or written on behalf of, any of the named journals. Mathematical correctness, editorial significance, finite computational checks, and successful typesetting are separate questions throughout this report.

## 1. Assessment for the editor

This revision makes real progress against the preceding report. The incorrect assertion about infinite optimized menu excess at a fixed calibration has been corrected in the active source and replaced by a valid stabilization theorem. The submission now contains actual multilevel statistical realizations, not merely abstract assignments of losses to paths. The predictable-acquisition theorem goes beyond the initial-anchor constraint and includes branching, recombination, and history-dependent scheduling in its converse. The positive examples retain the complete acquired distribution, including its atoms, and avoid a favorable event whose probability decays exponentially with the horizon. The active article now has one consolidated introduction rather than six chronological introductions.

A report which simply repeated that none of these repairs had been made would be inaccurate. I regard those specific objections as repaired, or, where appropriate, repaired on the explicitly stated regenerative class.

I have not found a fatal counterexample to the eleven new named statements under their printed hypotheses. Their principal inequalities, constants, minimax directions, and information conventions survive the examination below. In particular, I do not characterize the exact statistical flow theorem as false merely because its hypotheses are restrictive. Nor do I characterize a workflow failure without recorded steps as a mathematical or TeX compilation failure.

My negative recommendation is nevertheless firm for this submission at the requested level. The principal new exact theorem assumes that the information needed at the current checkpoint is entirely contained in a fresh block whose conditional law is unaffected by the past. Consequently the retained state may be discarded and rebuilt at every checkpoint. Once the one-block quantization costs are supplied, the remaining problem is the minimization of the maximum coordinate over a finite convex hull of path-cost vectors. This is a valid statistical realization, but the realization removes, rather than resolves, the cross-time posterior-compression constraint that would make a general causal-memory classification difficult.

The strongest numerical uniformity claim is similarly a consequence of exact factorization: the network design factor cancels from the ratio of risk to certificate. The unbounded checkpoint penalty is a genuine realized penalty, but it is a penalty for relaxing a common design decision into incompatible checkpoint-specific decisions. It is not a separation between admissible memory architectures, an adaptivity advantage, or a new obstruction to maintaining an evolving posterior. The manuscript usually states these distinctions correctly. Correct delimitation is necessary; it does not itself establish exceptional significance.

The inherited collision-uniform acquisition and causal-compression theorem remains the most substantial mathematical spine in the material examined. It should not be dismissed as a statement about ambient dimension alone. However, the new regenerative appendage does not establish a new consequence for that nonregenerative spine, and the submission still does not adequately substantiate why the combined package is a contribution of the exceptional depth or reach warranting the requested venues. This is an assessment of the present mathematical contribution, not a claim that the research program cannot produce such a contribution.

## 2. Submission identity and scope of this review

The branch names were checked against their actual commits. Three branches carry a v30 name. The causal-realization branch points to the v29 review commit `90c7acd0e4efe3280eb1a8faa3c6d9461870c36f`; the causal-compatibility branch points to an earlier source-export commit `907c7ef44ef6d7109c42fcd66b1343b5f972feb2`. Neither is the controlling multilevel revision. The multilevel branch remained at the submission identified above on the final pre-publication check; the complete A1 revision-branch search was paginated to exhaustion.

The preceding report is [the v29 independent report](https://github.com/TrillionniumFoundation/theta-theory/blob/90c7acd0e4efe3280eb1a8faa3c6d9461870c36f/reviews/a1-english-v29-harsh-independent-2026-09-08/REFEREE_REPORT.md), which assessed `610233410ff6600e76167fad98a3f610faa6191b`. The current response and proof ledger were read against that report, not taken as independent evidence of correctness.

Unless otherwise specified, source paths and theorem labels below refer to the controlling submission. The [native entry point](https://github.com/TrillionniumFoundation/theta-theory/blob/dc8c1bd475b870cd222627c0cfd6d784363e1728/papers/A1-english-v30-multilevel/main.tex) identifies the active modules. I use source labels rather than unverified PDF theorem numbers.

The examination covered all three new mathematical modules in full; the active menu corrections; the substantive unified introduction and entry-point structure; the full principal transversality, confluent-flag, analytic-input, and direct causal-classification modules; the full acquired-law and high-resolution arguments in the evaluated scalar example; the occupation module; and the initial-information definitions and dual proof. The current response, proof ledger, README, and CI receipt were also read. This is not a renewed line-by-line audit of every v25-v28 proof, the entire companion volume, or all eleven papers. Earlier favorable assessments of those unreaudited components are not silently converted into fresh verification here.

No full native two-volume build or PDF visual audit was executed in this review. The independent arithmetic and finite-model computations are specified in Section 11. No exhaustive literature-priority search or formal proof certificate is claimed.

## 3. Disposition of the preceding objections

| Earlier concern | Disposition in v30 |
|---|---|
| E29.1: optimized menu excess allegedly infinite at fixed finite graph and calibration | **Closed.** The active text is corrected and the new stabilization proof is valid. |
| Exactness established only for abstract local path data | **Resolved on the stated regenerative class.** The new theorem concerns actual finite-label statistical prediction; no general nonregenerative realization follows. |
| Evaluated statistical showcase has only one checkpoint | **Closed as a factual objection.** There is now an explicit-protocol multilevel family with matching common-design primal and dual. |
| Event mass may deteriorate exponentially across checkpoints | **Avoided in the new family.** The atom-aware capacity uses the whole probability space. |
| Six cumulative introductions | **Closed at the active-entry-point level.** `main.tex` now uses `v30/introduction.tex`; preservation of historical introductions outside that entry point is not a defect. |
| A demonstrated exceptional structural contribution | **Still not established to my satisfaction.** Sections 8-10 explain why, without denying the repairs above. |
| Complete current native two-volume build | **Still unverified.** The live job metadata confirms failure without recorded execution steps; it does not identify a TeX error. |

Previously closed comments should remain closed. I do not request deletion of valid collision results or the companion material to obtain a cleaner verdict.

## 4. The new statements: correctness disposition

The following table records the specific outcome of the present examination, not universal certification.

| Source label | Disposition and decisive qualification |
|---|---|
| `thm:v30-menu-finite` | Valid finite-envelope stabilization argument; calibration fixed. |
| `prop:v30-critical-resolutions` | Valid finite crossing-set formula; excessive-slope menus must be excluded. |
| `cor:v30-stratum-uniform` | Valid with fixed retained index sets and uniform positive volume bounds. |
| `thm:v30-regenerative` | Exact statistical minimax supported; route chosen before data, fresh sufficient blocks, public route descriptor. |
| `thm:v30-positive-realization` | Projection and clipping give the exact full-law reduction; attenuation changes the scored readout, not acquisition. |
| `lem:v30-atom-capacity` | Atom mass, recovery norm, cubic integral, and constant checked. |
| `thm:v30-controlled-gap` | Correct on committed routes; the uniformity is exact cancellation of a common positive design factor. |
| `cor:v30-checkpoint-gap` | Exact ratio supported; comparator uses incompatible checkpoint-specific route laws. |
| `thm:v30-predictable-exact` | Conditional lower bound and reset upper construction supported; no posterior information persists in the current target beyond the fresh block. |
| `prop:v30-predictable-bound` | Conditional layer cake and anchored-flow comparison have the correct directions; terminal capacities equal one. |
| `cor:v30-network-gap` | Correct specialization under conditional regeneration and the stated public-descriptor convention. |

### 4.1 Fixed-calibration finiteness is actually repaired

In `v27/policy_menus.tex`, immediately after `eq:v27-menu-functional`, the active source now inputs `v30/menu_finiteness.tex`. The false infinity sentence is replaced, and `cor:v27-menu-regret` explicitly distinguishes pointwise finiteness from deterioration along collision calibrations.

Put x = log2(1/epsilon). At fixed calibration, after omitting zero-volume branches, each edge cost is a maximum of finitely many affine functions with finite intercepts. Each cut sum and each order profile is again such a maximum. Every order is eventually affine, with slope

$$
D_\pi=\frac12\max_j\sum_{e\in\delta(S_j^\pi)}d_e.
$$

Among finitely many eventual affine profiles, a lexicographically minimal slope/intercept pair is minimal beyond a finite common threshold. Its order has zero excess thereafter and bounded excess on the remaining compact interval. Thus the optimized menu excess is finite even over the whole accuracy interval (0,1]. A prescribed menu has finite excess exactly when its smallest eventual slope is globally minimal.

The critical-resolution proposition is also sound. Expanding all cut sums produces finitely many affine constituents. Their nonnegative pairwise crossings, together with zero, partition the half-line into intervals on which every relevant maximum and minimum is affine. A slope-optimal menu has constant excess on the final interval; all finite-interval extrema occur at endpoints. The proof does not claim an efficient algorithm, nor does it treat arbitrarily small positive volumes as uniformly bounded below.

### 4.2 The committed-route statistical equality

In `v30/multilevel.tex`, `thm:v30-regenerative` gives

$$
\mathcal R_M^{\rm reg}
=\min_{\rho\in\Delta_R}\max_j\sum_r\rho_r d_{rj}(M)
=\max_{\lambda\in\Delta_J}\min_r\sum_j\lambda_jd_{rj}(M).
$$

Conditioning on the complete independent seed fixes the route and the decoder's at most M prediction vectors at a checkpoint. A label assignment, even one using earlier blocks, cannot beat the nearest of those vectors for the current block. The block retains its prescribed law under that conditioning. Averaging first at each checkpoint and taking the maximum afterwards proves the required lower bound. There is no illicit exchange of maximum and expectation.

The upper construction is a legitimate single controller: at every stage it reads the fresh block, selects its nearest center in the stage/route codebook, and overwrites the old label. The same label alphabet is reused; neither the old history nor earlier outputs are read back. Compactness gives optimal codebooks and a minimizing route law. The finite convex-hull separation argument gives the dual. These observations support the theorem exactly as stated.

The route is public by definition. The optional RM-state charged-route construction is an upper bound for a different problem, not an asserted equality. This resource convention is restrictive but not hidden.

### 4.3 Predictable networks and the stronger conditional information

For `thm:v30-predictable-exact`, conditioning immediately before acquisition, including the chosen vertex and seed, leaves the current block with law P_w. Hence

$$
\mathbb E[L_j\mid\mathcal H_j^-,w]\ge d_w(M),\qquad
\mathbb E L_j\ge\sum_{w\in\mathscr V_j}x_wd_w(M).
$$

An adaptive scheduler's expected arc incidences form a unit flow. Conversely, an optimal flow is realizable by an initial mixture of deterministic paths, with a fresh nearest-center reset at each visited node. This proves the exact value, including the full-history scheduling converse. It also proves a substantive limitation of what the theorem is saying: data-dependent scheduling has no advantage over an appropriate open-loop randomized path design in this class.

The displayed shortest-path dual is legitimate because the flow polytope in this theorem has no additional node restrictions. It should not be transplanted without modification into the earlier capacitated occupation problem. The manuscript explicitly retains that distinction.

For `prop:v30-predictable-bound`, conditional layer cake yields the linear occupation cost x_w ell_w, where ell_w is the integral of 1-c_w. Convexity and phi_w(0)=0 imply phi_w(z) <= z phi_w(1). Grouping a path decomposition by first vertex constructs feasible anchored mixtures and proves Gamma_pred >= Gamma_pre. The older Jensen argument gives Gamma_pre >= Gamma. This is the correct direction at both comparisons.

A minor sharpening is available: the J+1 path support bound can be replaced by J. An optimal risk vector lies on the exposed minimizing face for an optimal nonzero checkpoint dual vector. Only minimizing path vectors are needed, and their affine hull has dimension at most J-1. Caratheodory reduction on that face gives at most J paths. The printed J+1 bound is true, not an error, and improving it would not change the recommendation.

## 5. Independent multilevel witness for strict predictable improvement

It is useful to exhibit a statistical example in which the new predictable refinement does more than the initial anchor. This witness is derived here from the printed positive-block construction; it is not a counterexample to the submission.

Take two levels. The first level has a forced vertex u. The second has two alternatives a and b, with arcs from u to both and then to the sink. Use independent copies of the full positive acquired law at every vertex. Let s_u=delta in (0,1], and s_a=s_b=1. Put

$$
C_M=\frac1{8306688M^2}.
$$

The first-level cost in both earlier occupation problems is necessarily delta^2 C_M. Splitting the second-level occupation equally gives phi_a(1/2)=phi_b(1/2)=0. There is only one initial anchor. Consequently

$$
\Gamma=\Gamma_{\rm pre}=\delta^2 C_M.
$$

In the predictable problem, the second-level cost is C_M for every split, because it is linear in occupation and both local unit costs equal C_M. Therefore

$$
\Gamma_{\rm pred}=C_M,\qquad
\frac{\Gamma_{\rm pred}}{\Gamma_{\rm pre}}=\delta^{-2}.
$$

The actual risk is D_M(nu)/128, since the design factor is one. Thus an arbitrarily large strict improvement occurs within actual positive regenerative experiments, even with a forced initial vertex. The finite diagnostics check this witness at several rational gains and budgets. The general identities above follow from the displayed formulas, not from the samples.

This strengthens the favorable correctness assessment. It also precisely identifies the gain: conditioning before a fresh second acquisition prevents the earlier relaxation from diluting its atom-aware small-ball cost through a fractional occupation.

## 6. Full-law quantization, constants, and the multilevel penalty

### 6.1 The acquired measure and its atoms

The evaluated model in `v27/evaluated_model.tex` was reread rather than replacing the acquired statistic by an assumed uniform variable. The two accepted reports have masses 5/16 and 3/16 and posterior means 8/15 and 4/9. The failure component has mass 1/2, support [10/21,14/27], and density bounded by 26. Its rational density and the signs of its derivatives on either side of the peak agree with the stated change of variables and retained failure evidence.

The query isometry is

$$
\|q(z)-q(z')\|_q^2=(z-z')^2/128.
$$

Orthogonal projection onto the affine query line and scalar clipping justify the exact reduction for arbitrary decoder centers, not merely centers already lying on the attainable image. Attenuation by s changes the one-block distortion to s^2 D_M(nu)/128. It does not justify forgetting the atoms or modifying their acquired probabilities.

### 6.2 The atom-aware integration and the finite-budget factor

With b=2HLM/s, H=26, and L^2=128, the capacity is min(1,1/2+b sqrt(t)). Direct integration gives

$$
\phi(x)=\frac{(x-1/2)_+^3}{3b^2},\qquad
\phi(1)=\frac1{24b^2}=\frac{s^2}{8306688M^2}.
$$

The denominator is exactly 96 times 26^2 times 128. The atom term is a valid upper bound even when the two atoms cannot both be perfectly represented by a very small codebook. Such looseness does not invalidate a lower certificate.

The full support has diameter 4/45. An M-cell uniform midpoint quantizer on its convex hull gives D_M(nu) <= 4/(2025M^2), including the atoms. Hence

$$
\frac{\mathcal R_{\mathscr D,M}^{\rm reg}}{\Gamma_{\rm pred}}
=\frac{8306688}{128}M^2D_M(\nu)
\le\frac{8306688}{64800}<129.
$$

This all-budget upper factor is supported. It is a coarse bound, not a sharp finite-budget constant. The displayed exact all-budget identity still contains the variational quantity D_M(nu); it is not a closed-form evaluation of the optimal scalar codebook for each M.

### 6.3 Independent enclosure of the asymptotic coefficient

The self-contained scalar high-resolution proof correctly handles the continuous submeasure and finitely many atoms separately. The lower argument uses the number of intersections between Voronoi intervals and a fixed partition; the upper argument allocates centers according to upper density sums and reserves finitely many atom centers. It yields

$$
\kappa_{\rm ex}=\frac1{1536}\left(\int f(z)^{1/3}\,dz\right)^3.
$$

Independent monotone endpoint sums with 8,192 subintervals on each side and integer cube-root scale 10^12 give the following outward-rounded enclosure:

$$
4.0574997475
<8306688\kappa_{\rm ex}
<4.0595506343.
$$

The exact rational endpoints are in `INDEPENDENT_CHECKS.json`. This supports the printed interval (4.05,4.06). The graph-uniform convergence follows because the exact ratio has no graph, horizon, or gain parameter left; it does not require an additional exchange of a network limit with a scalar quantization limit.

### 6.4 What the consistency penalty compares

For diagonal gains one and off-diagonal gains 1/J, the risk-design matrix has diagonal one and off-diagonal 1/J^2. Under route law rho, checkpoint j costs

$$
J^{-2}+(1-J^{-2})\rho_j.
$$

Uniform rho minimizes its maximum, and uniform checkpoint weights give the matching dual. Thus V=1/J+1/J^2-1/J^3. Separate checkpoint-specific route laws give 1/J^2, and the ratio is exactly J+1-1/J. These calculations were checked with exact primal/dual vertex enumeration for J=2 through 5 and explicit rational witnesses through J=64.

This is a real positive statistical family, not an abstract path-loss fabrication. Nevertheless the divergent ratio is generated by incompatible design choices together with prescribed attenuation of the loss. Dividing each node's loss by its positive gain squared makes every node's scalar task identical; then the design factor is one and the corresponding common-versus-separate design gap disappears. That normalization changes the objective, so it is not a refutation. It explains why the example alone cannot establish a general memory or adaptivity separation.

## 7. The inherited collision and causal-memory spine

The core proof examined here contains more than dimension counting. `core/03_transversality.tex` constructs an attainable binomial product tangent of dimension n(r-1)+1. Its exponent blocks are disjoint because the interior one-step exponents lie strictly between zero and D. Strict mixed-moment positivity holds for every fixed full-support prior, including singular priors. Evidence normalization loses exactly the constant direction, giving the acquired rank rather than the dimension of an arbitrary future test space.

In `text/collision_flags.tex`, formal labels are retained through additive coincidences. Complete Hermite prefixes, not isolated high derivatives, are used in the confluent pairing. The positive exponent lower bound controls logarithmic derivatives at zero. Finite label permutations and compactness make the acquired differential uniformly surjective. The lower-measure argument adds kernel coordinates and integrates them after an inverse chart; it does not place positive probability on a frozen null slice. The failure evidence remains in the subprobability law.

The Leja factorization has bounded triangular inverse on the nonzero block; zero pivots are omitted rather than inverted. Prefix products compare with maximal determinant volumes with a finite factorial cost. The global covering argument in `text/analytic_inputs.tex` is applied to the entire attainable rational command image, with prior integrals as arbitrary real coefficients. It does not assume the prior's moments depend semialgebraically on calibration.

The raw update in `text/collision_direct.tex` has a denominator that is a genuine positive report probability, including on a segment between two reachable vectors through its posterior-mixture interpretation. Its Lipschitz bound does not divide by an exponent gap. Updating and requantizing reachable representatives gives a single causal filter, with preceding errors retained in a finite-horizon recurrence. The converse uses the same exploration law at all checkpoints before taking the infimum over controllers.

No new gap was identified in this route in the present examination. Its constants remain dependent on the fixed prior, experiment, and horizon; the code may depend on the known calibration and budget. The operational resource is persistent labels, not total computation or temporary workspace. The new network theorem should not be used to erase these qualifications or to claim that this inherited nonregenerative geometry has received an exact flow characterization.

## 8. A sharp scope test: actual memory compatibility outside regeneration

The following elementary problem isolates the information constraint removed by regeneration. It is a scope witness, explicitly not a counterexample to any printed v30 theorem.

Two independent fair bits B1 and B2 are revealed together before the first compression. There are two scoring checkpoints. No further data or score feedback reaches the controller between them; earlier outputs cannot be read back. The respective true conditional query means are

$$
q_1=1/4+B_1/2,\qquad q_2=1/4+B_2/2.
$$

A score can be realized by a Bernoulli outcome with that mean, observed only by the evaluator. Means are strictly between zero and one. The controller retains two labels and may use an independent public seed. The stage-two transition has no new observation.

A separate encoder designed only for checkpoint j stores B_j and has zero excess. A common causal controller cannot achieve both zero risks. Conditional on the public seed, its two labels induce at most two reconstruction vectors for the four corners of the square {1/4,3/4}^2. For fixed centers, random assignments cannot improve the sum of squared distances over nearest-center assignments. It therefore suffices to examine the partitions into at most two cells and use each cell's centroid.

There are three nontrivial partition types up to symmetry. An adjacent two-versus-two split has total mean squared error 1/16; a singleton-versus-three split has 1/12; a diagonal two-versus-two split has 1/8. A single cell also has 1/8. Thus every seedwise controller has sum of checkpoint risks at least 1/16. Averaging seeds and taking the maximum gives a lower bound 1/32. A fair independent seed choosing whether to store B1 or B2 attains risk 1/32 at each checkpoint. Hence

$$
\inf_{\text{one two-label causal controller}}\max_j\mathbb E L_j=1/32,
\qquad
\max_j\inf_{\text{separate checkpoint encoder}}\mathbb E L_j=0.
$$

The diagnostic enumerates all sixteen binary assignments and verifies these values. The argument also covers randomized encoders by the nearest-center reduction and averaging the independent seed.

At stage two the target depends on information from the old block, not on a newly revealed sufficient block. Precisely this feature violates v30's conditional-regeneration/current-sufficiency hypothesis. The example shows why that hypothesis is substantive. The fresh-block reset theorem is not an approximate solution to this compatibility problem: outside its domain, the zero local cost would miss a strictly positive common-controller risk.

## 9. Why the new results do not change the venue recommendation

### S30.1: the realization is separable after the imposed regeneration

The exact reduction can be summarized without any small-ball machinery. First solve each one-block M-center problem. Next assign its optimal cost to the corresponding vertex. Finally minimize the maximum checkpoint cost over the convex hull of deterministic path vectors. The reset construction implements those local optima simultaneously because no current prediction requires discarded past information.

The introduction of an actual statistical protocol is a genuine response to v29, but the protocol has been chosen so that the difficult compatibility requirement disappears. Short proofs can certainly establish deep results; proof length is not the objection. The objection is that no consequence has been shown in which this exactness controls an evolving posterior or a genuinely competing cross-stage allocation of retained information.

### S30.2: network uniformity is scalar factorization, not a new uniform stability mechanism

Both the true risk and the predictable certificate are the same positive network factor multiplied by a scalar quantity. Their ratio is consequently independent of every network parameter. This is useful and correct, including for varying finite networks, but it does not demonstrate a graph-uniform control of correlated acquisition, a graph-uniform comparison for the original tensor-only loss, or uniform error propagation for an evolving shared posterior.

The manuscript's separation of the original tensor, augmented local-and-tensor, and attenuated regenerative losses is now explicit. I accept that separation. I do not accept a breadth-of-application inference obtained simply by placing these three different tasks under one headline.

### S30.3: an inadmissible comparator does not establish an operational separation

The J+1-1/J family answers the earlier request for a multilevel statistical witness, and the answer deserves credit. But the relaxed comparator is allowed to choose a different initially committed route for each checkpoint. The construction demonstrates the cost of that inconsistency, not superiority over a legitimate competing controller class. The manuscript says so; the remaining problem is editorial weight, not honesty of the statement.

For a stronger significance case, a result should identify what is newly learned about an actual observation-and-memory problem after every compared procedure is placed under a common information, loss, and acquisition convention. Another large ratio to a deliberately weaker local certificate would not by itself answer that question.

### S30.4: the mathematical center of the article remains insufficiently resolved

Consolidating the introduction was necessary and has been done. The remaining issue is not the presence of historical files. It is whether the collision-geometric theorem and the regenerative network theorem constitute one consequential structural advance, rather than two results connected mainly by vocabulary and a general interest in finite labels.

The current exact regenerative value does not use the collision-uniform attainable flags. Conversely, the inherited nonregenerative graph and collision theorems do not acquire a new sharp characterization from the regenerative minimax formula. The paper needs to identify and substantiate its leading mathematical advance, with precise comparisons to the closest results and a consequence that makes that advance consequential. A longer list of valid specializations is not a substitute for this task.

These are grounds for my negative editorial recommendation, not assertions that the eleven new statements are false. I would not recommend acceptance conditional merely on correcting prose, sharpening J+1 to J, or obtaining a clean build.

## 10. Concrete requirements for a substantive reconsideration

**R30.1 — Contribution and comparison.** State which theorem is intended to carry the publication case. Compare its hypotheses and conclusion against the nearest relevant acquisition/quantization and occupation-measure results. Separate the nonstandard attainable collision argument from classical finite convex separation. A generic bibliography or a claim that the entire conjunction is new is not enough; equally, the referee has not established that an external paper already contains the whole conjunction.

**R30.2 — Consequential statistical content.** Demonstrate a consequence in which the retained-information constraint does mathematical work beyond independent current-block quantization and preassigned loss balancing. This may be a substantial consequence of the existing collision spine, a justified extension with nontrivial cross-time information, or another comparably strong result within a clearly stated model. This is an explanation of the significance deficit, not a demand to prove an unrelated general theorem as a repair of a false claim, and not a promise of acceptance after one additional theorem.

**R30.3 — Preserve the distinctions.** Keep the three loss conventions, public versus charged descriptors, fixed-calibration versus collision-uniform quantifiers, maximum of expectations versus expectation of a maximum, and common versus separately optimized acquisition laws explicit. The response currently gets these distinctions largely right. Do not discard them in a more ambitious abstract.

**R30.4 — Native publication package.** Supply an executed full native article-and-companion build at a pinned commit, with resolved cross-volume references and inspected output, before describing the whole submission as publication-ready. The present proof packet and arithmetic receipt are narrower deliverables. No deletion of mathematical content is requested to accomplish this.

## 11. Executed independent checks and build evidence

`independent_checks.py` was written separately from the author implementation after reading the mathematical source. It uses the Python standard library, exact fractions and integer arithmetic, and explicit exceptions rather than removable assertions. It was run with ordinary Python and with `python -O`; the JSON outputs were byte-identical.

The executed script's SHA-256 is

`f97ab68e2867e2e0876fa0f5ec21bf7d102c4bc4e22c8b90b78554219101b840`.

The accompanying JSON's SHA-256 is

`0751d33ac7ff3ff50dc146732567fe61ca2c3c976d46844e7e016239e2370cfa`.

There were **49,401 finite checks**, of which **49,156** were endpoint-density and integer-root operations for the scalar enclosure. That count is not a measure of theorem coverage. The remaining diagnostics include exact finite-game primal/dual vertex enumeration, branching/recombining path occupations, fresh-block selection and anticipatory-selection negative controls, atom-aware integration, menu stabilization, the full acquired continuous mass, physical query constants, the strict predictable-refinement witness, and the nonregenerative two-bit scope witness. Decimal fields are display-only; the mathematical enclosures are rational.

The tests do not certify all priors, all calibration limits, measurable scheduler classes, global inverse charts, real-geometric covering theorems, arbitrary codebooks, or all companion results. The analytic reasoning in this report, rather than a test count, supports the corresponding judgments. The author's historical diagnostic suites were not rerun.

The native CI status was independently checked through the live [job record](https://github.com/TrillionniumFoundation/theta-theory/actions/runs/34175506178/job/101903965773). It reports the manuscript-bearing commit `e7fc18d1f73120527f7a6dfa6f7468b9f20cb435`, conclusion `failure`, an empty steps array, and runner identifier zero. This matches `CI_EXECUTION_V30.json`. The cause is not established by those fields. There is no observed TeX failure from which to infer a manuscript error, and no successful full-build evidence from that run.

The author's ten-page new-results compilation and 50,790-check suite remain author-reported, narrower execution records. They were not independently reexecuted here. The present review does not claim a complete native compilation, PDF visual inspection, or byte-by-byte preservation audit of every inherited proof body.

## 12. Targeted primary-source positioning

The following checks support limited contextual and bibliographic statements, not an exhaustive priority verdict.

**[P1] R. T. Rockafellar.** *Minimax Theorems and Conjugate Saddle-Functions*, Mathematica Scandinavica 14 (1964), 151-173, DOI 10.7146/math.scand.a-10714. The [journal record](https://journals.msp.org/mscand/article/view/2592) verifies the reference. The finite separation proof actually needed in v30 is printed in the manuscript and was examined directly. This citation is not evidence that Rockafellar proved the submitted statistical theorem.

**[P2] Xianping Guo, Yonghui Huang, and Yi Zhang.** *Constrained Continuous-Time Markov Decision Processes on the Finite Horizon*, Applied Mathematics and Optimization 75 (2017), 317-341, DOI 10.1007/s00245-016-9352-6. The [author-deposited university record](https://livrepository.liverpool.ac.uk/3001778/) describes occupation measures, deterministic-policy extreme performance vectors, and finite mixtures of deterministic policies. Its model and hypotheses differ from A1. It establishes that occupation-based convexification and finite-mixture attainment are an established control-theoretic methodology, not that it subsumes the collision theorem or the precise v30 experiment.

**[P3] Yifan Zhang and Joe Kileel.** *Covering Number of Real Algebraic Varieties and Beyond: Improved Bounds and Applications*, [arXiv:2311.05116](https://arxiv.org/abs/2311.05116). The authors' research record concerns covering bounds for algebraic varieties, polynomial images, and semialgebraic sets with controlled format. This supports the placement of the covering input within existing real-geometric work. I assessed the thin-rectangle specialization from the manuscript's section/projection argument; I do not claim a fresh page-by-page verification of every externally cited entropy theorem.

The manuscript need not deny its use of classical tools. It needs a more persuasive explanation of the new consequence obtained from them and from its nonstandard attainable-geometry component.

## 13. Final recommendation

**Reject at the requested four-journal level.** The present manuscript has repaired the concrete v29 mathematical misstatement and has supplied legitimate new statistical realization results. No demonstrated fatal counterexample to those new statements is asserted in this report. Nevertheless, the exact new network theory is a separable regenerative design problem, and the current package has not established the exceptional structural consequence required to reverse the earlier editorial assessment.

This is not a recommendation for cosmetic minor revision. Nor is it a reason to erase valid mathematics, revive closed objections, or treat the research direction as impossible. A reconsideration would have to rest on a materially stronger contribution case, supported by mathematics under clearly controlled operational conventions and by a complete native submission package.
