# Independent referee report on A1 v32

**Manuscript:** *Attainable information, exponent collisions, and adaptive memory*, Qian Qi.  
**Date of assessment:** 8 September 2026.  
**Repository:** `TrillionniumFoundation/theta-theory`.  
**Controlling revision branch:** `revision/a1-english-v32-causal-certificates-2026-09-08`.  
**Controlling manuscript commit:** `e712437fe13cf29978715d3f16d825eadb450fea`.  
**Native manuscript directory:** `papers/A1-english-v32-causal-certificates/`.  
**New mathematical module, Git blob:** `db8ae28cff76c143b709dabb8d68e64516c7f6b7`.  
**New review branch:** `review/a1-english-v32-harsh-independent-2026-09-08`.  
**Requested standard:** Annals of Mathematics, Inventiones Mathematicae, Journal of the American Mathematical Society, or Acta Mathematica.  
**Recommendation:** **Reject at the requested four-journal level.**

This is an owner-requested, AI-assisted independent referee-style assessment. It is not a report commissioned by, or an endorsement from, any of the named journals. The recommendation is an editorial judgment about this submission, not a claim that the research program is impossible. The previous reports were consulted to identify the changes and avoid recycling resolved objections; their recommendations were not treated as mathematical evidence.

## 1. Recommendation to the editor

The revision makes a real advance over the version criticized in the preceding report. It now formulates the nonregenerative finite-memory problem with the common transition constraints intact, proves a command-discretization theorem for arbitrary Borel coding kernels, and supplies a valid exhaustive route to two-sided global certificates. The positive delayed-use example compares two admissible schedules and treats private encoder randomization analytically. These are substantive repairs, not merely changes of terminology. [S1, S2]

I have not established a fatal counterexample to the new named statements under their printed hypotheses. In the proof chains examined below, the distinctions between full-history coefficients and decoder information, private randomness and a persistent public seed, mean risk and worst-history risk, and prescribed and state-controlled acquisition are handled correctly. The report should not be read as alleging that the new compatibility theorem secretly assumes regeneration.

Nevertheless, I do not recommend publication at the requested level. The principal publication-bearing mathematics remains the inherited attainable collision classification. The new general machinery is an exact parametrization of finite controllers followed by positive-likelihood perturbation and exhaustive compact approximation. It does not yet reveal a comparably strong new structure of the optimal nonregenerative controller. Its advertised relative accuracy is obtained from a freely chosen discretization precision and the weakest one-dimensional consequence of the old lower bound. The exact delayed-use calculation is worthwhile, but is a two-label finite example under a different charge boundary, not a general description of the original monomial problem's optimal causal organization.

These limitations do not make the results false. They matter to the significance of the package being offered. In particular, the absence of a polynomial-time algorithm is not my objection: a deep structural theorem need not be efficient. My objection is that the new certification layer has not been separated sharply enough from a general exhaustive approximation principle to establish the exceptional additional mathematical content claimed for the combined article. The literature comparison also needs to address closer finite-model and observation-channel approximation results, with the information resources matched explicitly.

A complete current article-and-companion build remains unexecuted in the publication record. That is a separate delivery deficiency, not evidence of a false theorem or a demonstrated TeX failure. Supplying the missing build would not by itself change my editorial recommendation. [S3]

## 2. Submission identity and scope of this examination

The controlling commit is dated 8 September 2026, 04:46:10 UTC, or 12:46:10 Singapore time. It adds a materialized v32 manuscript directory, rather than merely naming a new branch. Its parent is `b9296a7b4736225e72f95cc275c31df220442772`, containing the second independent v30 review. The revision-branch search was followed to an empty final page; the v32 head was checked again before preparing this review for publication. [S4]

The preceding report is `reviews/a1-english-v30-harsh-second-independent-2026-09-08/REFEREE_REPORT.md`. The v32 response identifies that report as controlling. The source-publication record distinguishes the earlier preparation session from the later repository publication. Thus an archived statement that a branch had not yet been created is not evidence that the current v32 branch is missing. [S2, S3]

This examination read the complete new mathematical module, the referee response, the new abstract, positioning and information ledger, the active main entry point, the native build wrapper and its integration helpers, and the principal inherited rank, positivity, attained-flag, covering and causal-classification chain. It also inspected the explicit risk definitions. Source labels are used below instead of theorem numbers inferred from an unbuilt PDF.

This is not a fresh line-by-line verification of every companion proof, all inherited graph modules, every historical branch, or all eleven planned papers. The general real-geometric entropy theorem cited by the manuscript was not independently reconstructed from its original monograph. The full native two-volume source was not compiled or visually inspected in this assessment. The accompanying computations are independent finite diagnostics, not executions of the authors' scripts and not a formal verification of the continuum results.

## 3. Disposition of the preceding objections

| Question inherited from the v30 assessment | Disposition in this review |
|---|---|
| Does the new analysis address only conditionally regenerative blocks? | **Closed as a factual criticism.** The new compatibility and approximation results concern a shared latent parameter and one common finite-state controller. |
| Are separately optimized checkpoint encoders substituted for a common transducer? | **Closed for the new finite formulation.** The common-row equations explicitly prevent that substitution. |
| Is the timing comparator inadmissible, or does its denominator vanish identically? | **Closed for the new delayed-use example.** Both schedules are admitted, and the just-in-time risk is positive for every printed parameter value. |
| Are a persistent public seed and private transition coins conflated? | **Closed in the examined v32 statements.** The unseeded class and the enlarged seeded class are distinguished. |
| Does the earlier fixed-calibration menu-finiteness objection need to be raised again? | **No.** This review does not allege a regression, nor convert an inherited repair into a newly executed verification. |
| Has exceptional significance at the requested venue level been established? | **Not to this referee's satisfaction.** The reasons are theorem-specific and given in Section 6. |
| Is there a current complete native build and visual record? | **Still open.** A standalone new-results packet and historical receipts are not the complete publication object. |

These dispositions should constrain the next round. Repeating an obsolete objection after its mathematical premise has been removed would not be a rigorous review. [S1–S3]

## 4. Examination of the new mathematics

### 4.1 Exact finite compatibility and conditional centroids

**Locations:** `thm:v32-finite`, `eq:v32-action-rows`, `eq:v32-compatible`, `eq:v32-posterior-factorization`, and `prop:v32-centroids` in [S1].

The finite representation correctly retains the causal restriction. With command probabilities a_t(c|i), joint command/update rows b_t(c,j|i,x), and joint history-state masses alpha_h(i), the conditions are

\[
\sum_c a_t(c\mid i)=1,\qquad
\sum_j b_t(c,j\mid i,x)=a_t(c\mid i)
\]

for every report x, and

\[
\alpha_{hcx}(j)
=r_x(h,c)\sum_i\alpha_h(i)b_{t+1}(c,j\mid i,x).
\]

Requiring the same a-row for every possible report enforces selection before observation. Requiring the same b-row for all histories arriving at state i is the finite-memory constraint. Neither condition follows merely from conservation of total flow.

The nontrivial point in the state-controlled version is the posterior factorization. Conditional on the observed command/report history h, the latent parameter and retained state have law

\[
\frac{L_h(\vartheta)\mu(d\vartheta)}{Z_h}\,K_h(i).
\]

A command selected using the retained state and fresh private randomness reweights only K_h. Its report multiplies only the latent factor. The subsequent state update again changes only the finite-state factor. This proves the induction and justifies the coefficient r_x(h,c), including when the controller affects acquisition. It does not give a posterior oracle to the decoder.

The converse realization by selecting c and then sampling b/a is valid; zero a forces the corresponding b entries to vanish. Closed bounded row simplices, decoder cubes and recursively determined occupancies give compactness. Thus the minimum is attained. The claim of a finite polynomial optimization with fixed real coefficients is correct and does not imply convexity or effective access to arbitrary real coefficients.

For fixed rows, completing the square gives the printed centroids. Each decoder coordinate belongs to one checkpoint, so these choices minimize all checkpoint mean risks simultaneously. The perspective term extends continuously at zero occupancy because its numerator is bounded by the square of its denominator. This is not a worst-history centroid rule, and the manuscript does not assert one.

**Assessment:** the finite equivalence survives examination. The independent diagnostic verifies its recurrence and latent-state factorization against direct enumeration for a three-stage state-controlled rational experiment. This is evidence for that finite instance, not the proof of the theorem.

### 4.2 Positive-likelihood perturbation and command discretization

**Locations:** `lem:v32-perturbation`, `thm:v32-grid`, and `cor:v32-controlled` in [S1].

The perturbation estimate uses positivity in the right place. For commands at sup-norm distance at most delta, the report distributions conditional on the latent parameter have total variation distance at most delta. Along the command segment, the likelihood-product score has absolute value at most t delta/kappa. Differentiating a bounded fixed future expectation as a covariance then gives

\[
|p_{tq}(h)-p_{tq}(Q_\delta h)|\le t\delta/\kappa.
\]

The future likelihood is fixed and does not read a discarded command prefix. This restriction is essential and is printed. There is no differentiation through an arbitrary coding rule, and no division by a difference of exponents.

The lifted finite experiment is an effective way to handle discontinuous Borel transitions. Commands are still drawn from the original cube, but reports use the likelihood at the cell representative. Conditional on a cell, the within-cell command can be integrated out of the update kernel in the prescribed independent-command model. The resulting stochastic row is implemented by fresh private coins. It is not a retained location seed.

Coupling the reports and then changing the target gives the mean comparison

\[
|V^{\rm av}_{\delta,M}(a)-\mathfrak R^{a,\rm av}_{M,N}|
\le T(1+2/\kappa)\delta.
\]

The bound does not count the number of labels, which explains its uniformity in M. For worst-history risk, the lower inequality follows from restriction to representatives and the upper inequality from rounding, with error 2T delta/kappa. The risk definition uses a supremum over all admitted histories, not an essential supremum. Consequently restriction to finitely many representatives is legitimate despite their zero mass under a continuous command law. Coding expectation remains inside that supremum. [S5]

The state-controlled corollary also has the right direction. Finite commands are a subclass of continuous commands. For the reverse approximation, integrate the continuous command/update kernel over a cell conditional on the previous state and use the likelihood depending only on its representative. Coupling until the first report discrepancy bounds the change of the induced law. The old exploration-law collision lower bound is not transferred to this optimized acquisition problem.

**Assessment:** I find no missing continuity assumption on the coding kernels and no concealed change of memory resource in these arguments. The finite-horizon, uniform-positive-likelihood hypotheses are doing substantial work; the result should not be paraphrased as an unrestricted approximation theorem for partially observed control.

### 4.3 Rational controller nets and two-sided global certificates

**Locations:** `lem:v32-controller-net` and `thm:v32-certificates` in [S1].

Rounding the first M-1 entries of a stochastic row down to multiples of 1/b and putting the residual mass in its last entry gives total variation error at most (M-1)/b. Coupling at a fixed history and rounding decoder values gives

\[
E_{M,b}=\frac{T(M-1)+2}{b}.
\]

The finite net is a subset of admissible common controllers. Its best value W is therefore no smaller than V, while approximation of a finite optimizer gives W-V at most E. The same argument applies to both printed risk criteria.

Suppose each controller has an objective enclosure [ell_F,u_F] of width at most tau. Taking the minimum of all lower endpoints and the minimum of all upper endpoints gives u-ell at most tau: use a controller attaining the smallest lower endpoint. Combining this with the controller-net error and the command-grid comparison gives the stated mean and worst-history intervals, including the different one-sided command errors. A controller attaining the smallest upper endpoint gives an actual implementing upper certificate.

The lower endpoint requires the complete finite net, or a replacement argument rigorously covering it. A few feasible controllers cannot supply it. The manuscript explicitly says this. I therefore do not criticize the theorem as if it were a local nonlinear solver masquerading as a global optimum.

The effective-access qualification is also correct. The relevant monomial coefficients use moments with formal degree at most N, even though the final risk expression squares already evaluated numbers. Evidence denominators are bounded below by kappa to the appropriate power. Certified access to the finitely many moments and fixed coefficients therefore permits interval refinement. Full support alone does not imply that the prior moments are computable. The theorem makes a conditional finite-oracle assertion, not an algorithm for every abstract prior.

**Assessment:** the certificate construction is mathematically coherent. Its significance and the extent to which it has been instantiated are separate questions addressed below.

### 4.4 Relative certification across collisions

**Location:** `cor:v32-relative` in [S1].

The printed inference is valid. With command radius at most M^{-3}, b=M^4 and objective-enclosure width at most M^{-3}, the absolute interval width is O(M^{-3}). The inherited classification implies

\[
\mathfrak R^{a,\rm av}_{M,N}\ge c\Xi_N(M,a)\ge cM^{-2},
\]

since the first determinant volume equals one. The worst-history risk is no smaller. Dividing gives the claimed O(M^{-1}) relative width uniformly in calibration. The absolute approximation was established independently, so this is not a circular proof.

This correct inference should not be confused with a new sharp collision-dependent rate. The certificate uses only the M^{-2} floor at the final step, not the higher determinant volumes or the detailed changes of attainable dimension. Section 6.1 makes this limitation precise.

### 4.5 The exact unseeded delayed-use law

**Location:** `thm:v32-delayed` in [S1].

The positive latent/report construction yields the centered targets Y_j=gamma X_j+e U_j, with independent symmetric report signs. The acquisition likelihoods are at least 1/4, and the readout probabilities have the stated positive bound. Both schedules acquire the same reports once and score one selected query. Importantly, the complete block is available during an update; memory is charged at block boundaries. The manuscript explicitly distinguishes this from the per-report convention of the scalar monomial theorem. [S6]

The single-current-target quantization argument gives V_jit=e^2 for 0<e<=gamma/2. For the early schedule, subsequent private transitions without new information cannot improve on decoding from the first retained label. Jensen's inequality justifies this reduction.

For a randomized binary encoder Q, put p=E Q and v_j=E(Y_j Q). Centroid decoding gives explained variance v_j^2/[p(1-p)]. Reflections permit nonnegative correlations. Averaging Q with its coordinate-swapped version preserves p and increases the smaller squared correlation. This is a private randomized encoder with fixed new centroid decoders; it is not a convex mixture of decoder programs indexed by a free public seed.

At fixed p, the remaining maximization is an upper-tail problem for Y_1+Y_2. On each interval between successive tail masses, its numerator has form A+sp. The derivative of (A+sp)^2/[p(1-p)] has the sign of (s+2A)p-A when the numerator is nonzero. Hence no interior strict maximum is lost by checking the tail endpoints. The two surviving endpoint candidates are the four-word and six-word symmetric tails, and both are deterministic encoders. This supports the full private-randomization conclusion

\[
V_{\rm early}(e)=\gamma^2+e^2-
\max\{\gamma^2/3,(2\gamma+e)^2/15\}.
\]

The branch crossing e=(sqrt(5)-2)gamma lies inside the parameter interval. The early value tends to 2gamma^2/3, whereas V_jit tends to zero. Thus the unbounded ratio is genuine, with a positive denominator for every allowed e.

A persistent public coin that chooses which large sign to retain gives each checkpoint risk gamma^2/2+e^2. This is strictly below the unseeded value throughout the stated range, since the maximum explained variance in the unseeded formula is at most 5gamma^2/12. This is a useful resource-separation check, not a counterexample to the unseeded theorem. The manuscript correctly treats the public-seed construction as belonging to a different decision problem.

**Assessment:** the formula survives examination. Independent exact enumeration checks all 32,768 unordered deterministic binary partitions at seven rational parameter ratios, including a boundary control at e=0. The proof for arbitrary stochastic encoders and all real parameter values remains the analytic symmetrization and tail argument, not those finite checks.

## 5. The inherited geometric theorem remains the strongest component

The revision should not be assessed as though its only mathematics were the new finite optimization. I reexamined the principal scalar chain. [S7–S10]

The binomial tangent has n(r-1)+1 distinct monomial directions. Strict mixed-moment positivity supplies the required rectangular rank for every fixed full-support prior, including a singular one. Because the product itself belongs to the tangent, normalization removes exactly one direction. This establishes attainable rank, rather than inferring it from the dimension of an ambient test space.

The complete Hermite-prefix argument in the attained Newton-flag lemma is important. Arbitrarily selected high derivatives would not support the same positivity conclusion. Positive lower bounds on future exponents control logarithmic functions at zero. Continuity, compactness and the finite set of formal-label permutations give uniform surjectivity through collisions. The positive-mass step augments the output map with kernel coordinates and integrates over those coordinates; it does not assign positive measure to a frozen slice.

The Leja argument separates the small pivot scales from a uniformly bounded triangular change of coordinates. Its determinant-product comparison remains meaningful at repeated nodes, where zero pivots are never inverted. The covering proof concerns the entire attainable image: bounded-format semialgebraic descriptions permit arbitrary real prior-moment coefficients at each fixed calibration. The affine-section component and entropy bounds produce the dimension-truncated products of rectangle widths. Small integer budgets and moving centers onto the attainable set are handled explicitly. The specialization was checked; the original external entropy theorem remains an external input, not a theorem newly verified here.

Finally, the causal construction updates raw remaining moments. The denominator on a segment between reachable states is a report probability under a posterior mixture and stays positive. This gives a collision-gap-independent Lipschitz bound. Updating a reachable representative and quantizing it in the next reachable image gives one actual transducer, with errors propagated through a fixed finite horizon.

I did not identify a new defect in this examined chain. Its acquired-measure and causal content should not be dismissed as ordinary dimension counting or as a theorem about Vandermonde matrices alone. Conversely, these arguments have constants for a fixed prior, experiment and horizon, and permit known calibration and read-only real-valued programs. They are not finite-bit arithmetic complexity results or horizon-uniform bounds.

The inherited theorem already shows that, for a fixed experiment and horizon, the common-filter risk has the same order as the maximum checkpoint profile, uniformly in calibration and M. It would therefore be inaccurate to say that the paper has no quantitative causal comparison at all. What the new certification layer does not add is a sharper structural description of that comparison or of the optimizing controller.

## 6. Major reservations and requirements for a substantive revision

### R32.1 — The relative-certificate rate is a tunable precision statement

**Type:** significance and positioning; not a false-theorem allegation.

The manuscript chooses delta=M^{-3}, b=M^4 and tau=M^{-3}. The same argument gives a family of arbitrarily faster displayed rates. For any fixed integer k>2, choose

\[
\delta\le M^{-k},\qquad b=M^{k+1},\qquad\tau\le M^{-k}.
\]

Then E_{M,b}, the command error and the evaluation width are O(M^{-k}). Dividing by the same lower bound cM^{-2} gives relative width O(M^{2-k}). No new collision geometry is used to make this change. The extra accuracy is purchased by enlarging the finite exhaustive problem and refining coefficient evaluations.

This observation does not contradict the stated corollary, which claims neither optimality nor efficiency. It identifies its mathematical role: a consequence of absolute approximability plus a positive polynomial risk floor. Any family satisfying the corresponding perturbation hypotheses and floor would admit the same inference. The higher determinant volumes are not needed for this particular relative conclusion.

**Required revision:** state the free precision/error tradeoff directly, and distinguish it from an intrinsic asymptotic law. Explain which additional result, if any, uses the full collision profile to characterize causal organization, sharp constants or a nontrivial resource tradeoff. The choice k=3 must not carry the rhetorical weight of a new critical exponent.

### R32.2 — An exact controller representation is not yet a structural solution

**Type:** major contribution assessment.

The compatibility equations are necessary and sufficient and genuinely repair the earlier causal omission. They nonetheless retain a variable for every finite history and state. For command-alphabet size C and report-alphabet size X, the number of length-t histories is (CX)^t. The formulation does not eliminate that tree by identifying a new sufficient finite structural invariant.

The size of the literal rational table net makes the nature of the certification explicit. With Q_t queries at checkpoint t, its number of table assignments is

\[
\binom{b+M-1}{M-1}^{TMCX}
(b+1)^{M\sum_t Q_t}.
\]

This counts all rows, including ones irrelevant to particular reachable states; pruning may reduce it. It is the direct product of rational transition-row simplices and decoder grids, not a bound exploiting monomial geometry. The command discretization can itself require many representatives before this enumeration begins.

There is nothing invalid about an exhaustive construction. Nor is a polynomial bound a necessary condition for publication in pure mathematics. But exact representability by a large nonconvex program, together with an elementary net approximation, should not be treated as equivalent in depth to a structural classification of the optimum. The paper already cites the finite-controller nonlinear-programming precedent of Amato, Bernstein and Zilberstein, appropriately. [L1]

**Required revision:** distinguish representation, approximation, global certification and structural classification in the hierarchy of claims. To justify the proposed prominence of the new layer, provide a consequential structural result in the original shared-latent model, or make a substantially more precise case that the existing acquired collision theorem alone bears the requested publication significance. Examples of a meaningful strengthening include a sharp causal comparison beyond unspecified fixed-horizon constants or a theorem identifying how optimal retained information changes through collisions. These are illustrations of the missing kind of conclusion, not a demand to solve a particular newly imposed problem.

### R32.3 — The closest approximation literature is not yet adequately compared

**Type:** major scholarly positioning; no claim of established duplication.

The comparisons with quantization of prescribed measures, clustered Vandermonde matrices, zero-delay communication coding and finite-controller nonlinear programming are relevant. They do not exhaust the nearest literature for the new approximation theorem. [S11]

Saldi, Yüksel and Linder study quantized-action approximations under weak continuity. In the version checked here, their Theorem 3.2 gives convergence of discounted optimal values uniformly on compact state sets, and the paper discusses partially observed models through their belief-state reduction. This is a closer approximation precedent than a general reference to quantization alone. It is not automatically a result about a decoder whose entire persistent state consists of M labels. [L2]

The same authors also study finite observation/action approximations in decentralized stochastic control and near-optimal quantized policies for static and dynamic teams. The abstract establishes the relevance of that comparison; this review has not audited all of that paper's hypotheses and proofs and does not assert that it subsumes the present theorem. [L3]

Yüksel and Linder examine optimal-cost continuity in observation channels under total variation, setwise and weak convergence, primarily but not exclusively in single-stage problems. This is directly relevant to locating the positive-likelihood coupling argument. Their framework must not be declared equivalent to the v32 finite-memory constraint without checking the permitted information at every decision. [L4]

**Required revision:** give a theorem-level comparison separating horizon, retained state, available history, randomness, continuity assumptions, discretized object, risk criterion and uniformity. Identify exactly which existing result can be specialized, which cannot, and what new proof is needed for the uniform-in-M Borel-controller statement. I have not established prior publication of the exact v32 theorem; the objection is an insufficiently resolved novelty case, not plagiarism or a proved priority failure.

### R32.4 — The delayed-use calculation does not yet unify the principal models

**Type:** scope and significance.

The example succeeds as a positive, admissible timing separation and as an exact unseeded two-label calculation. Those improvements must be credited. But the early encoder reads all four reports in one block before compression, whereas the scalar monomial theorem charges memory after every report. Both schedules in the example obey the same block-charge rule; the issue is not internal unfairness between them. The issue is the limit of what this example demonstrates about the principal per-report, full-future-query model. [S1, S6]

Similarly, the state-controlled corollary is a different design objective with an induced acquisition law. Its explicit disclaimer concerning the prescribed-exploration lower bound is correct. The regenerative graph theorems use additional public descriptors or seed access and conditional regeneration. A common abstract label such as adaptive memory does not turn these different decision problems into one theorem.

**Required revision:** retain the exact ledger, and supply a mathematical dependency map distinguishing consequences within one model from comparisons between models. A strong application to the original per-report monomial experiment would carry more weight than another isolated finite example. Historical preservation is not itself an editorial defect; however, preserving all derivations does not require that every model receive equal prominence in the active research article.

### R32.5 — Separate proved certificate existence from executed certification and publication readiness

**Type:** reproducibility and delivery, not a proof gap in the existence theorem.

The response properly records that the complete general controller net was not enumerated. The independent checks accompanying this report do not enumerate it either. Thus neither the author's finite examples nor this report's diagnostics constitute an executed two-sided certificate for a nontrivial original continuous monomial instance. This is not a contradiction: the theorem is an existence and finite-oracle construction. [S1, S2]

**Required revision:** clearly label mathematical certificates, diagnostic tests and actual executed enclosures as different artifacts. A small fully specified original-model instance with certified lower and upper endpoints, the implementing controller and a complete coverage argument would make the construction inspectable. It is not necessary to run the impossibly large literal net at every budget to validate a mathematical theorem; the point is to demonstrate what is and is not operationally delivered.

Separately, build the complete `main.tex` and `companions.tex` pair from a pinned commit, record the engine and commands, stabilize cross-volume references, inspect both final PDFs, and attach a current receipt. The supplied builder has appropriate checks for unresolved references and explicitly records that its script does not perform visual inspection. Reading that code is not executing it. Neither this referee nor the source-publication record establishes a current native build. A successful earlier packet compilation does not close this obligation. [S3, S12]

## 7. Independent calculations and their exact scope

The accompanying `independent_checks.py` was written for this review. It uses Python's standard-library `fractions.Fraction`, explicit exceptions rather than assertions, and no network or third-party numerical solver. The actual environment was Python 3.13.5. The following commands were executed successfully in the review environment, using the corresponding local paths:

```bash
python independent_checks.py > INDEPENDENT_CHECKS.json
python -O independent_checks.py > INDEPENDENT_CHECKS.optimized.json
cmp INDEPENDENT_CHECKS.json INDEPENDENT_CHECKS.optimized.json
```

Both runs exited successfully and produced byte-identical JSON. The optimized duplicate need not be stored twice; its identity is recorded in `AUDIT_RECORD.json`.

The checks cover 168 exact history-state equalities against direct latent/state-path enumeration in a three-stage, two-state, two-command, two-report controlled experiment. They also check the posterior factorization and occupancy normalization. One command row has zero probability for one state at one stage. There are no globally zero-mass histories in that particular diagnostic, so it should not be advertised as a test of all unreachable-history cases.

There are 420 exact posterior-perturbation comparisons for a positive three-cell monomial detector with the uniform prior on [0,1]. Calibration pairs include (1,199/100), (1,2), (1,201/100), (1,3) and (2,3); the list includes exact and nearby additive-collision configurations. Rational-exponent moments are integrated exactly as 1/(1+lambda). The command perturbation is 1/60 and the conservative likelihood lower bound is 1/16. These tests check the printed inequality for the chosen histories, not a continuum of calibrations.

For the delayed experiment, all 32,768 unordered deterministic binary partitions, including the constant encoder, are tested at e/gamma equal to 0, 1/8, 1/5, 2/9, 1/4, 1/3 and 1/2. The first is a boundary diagnostic outside the theorem's strict e>0 assumption. The computed optima agree with the formula and the tail-endpoint calculation. The extra sum-of-explained-variances statistic is only a finite-parameter benchmark. It is not presented as an additional proved all-parameter theorem. Twelve rational stochastic-row examples check the rounding bound.

The script SHA-256 is `a99fe77d3f23f5717453fd4cfcddaa7f1c2d88fcbbf600cc1db98bae6e929b93`. The output SHA-256 is `02fe852d41847d3500ba5151b93158231f2df099bd3c9fc59a9f3a877fe8ff01`. The pinned manuscript commit and proof blob are embedded in the output. No floating-point optimizer, formal proof assistant, complete manuscript build, author-script rerun or exhaustive literature certification is claimed.

## 8. Final assessment

The v32 author has answered important earlier objections correctly. This is a materially better submission than one offering only a regenerative flow formula as a substitute for general causal memory. Its new finite compatibility theorem, perturbation argument and exact delayed-use calculation should be preserved.

The recommendation remains rejection at the four-journal level because the new layer has not yet established the claimed level of structural significance, the closest approximation literature has not been adequately resolved, and the relation among the several active decision problems remains more a carefully qualified collection than a compelling new unified theorem. The missing complete build is an additional, independently remediable issue.

A further revision should not respond merely by adding another version number, more diagnostics, a finer exhaustive grid, or a stronger adjective in the abstract. It should make the publication-bearing theorem unmistakable, establish its relation to the nearest prior results, and distinguish genuine new structure from representation and exhaustive approximation. Correctly closing the concrete issues in this report would permit a fresh assessment; it would not amount to a promise of acceptance at any particular journal.

## Source map and primary literature

All manuscript references below are pinned to the controlling commit, not a moving branch. The theorem labels in the body identify the relevant passages.

- **S1:** [Complete new proof module](https://github.com/TrillionniumFoundation/theta-theory/blob/e712437fe13cf29978715d3f16d825eadb450fea/papers/A1-english-v32-causal-certificates/v32/new_results.tex).
- **S2:** [Response to the controlling referee report](https://github.com/TrillionniumFoundation/theta-theory/blob/e712437fe13cf29978715d3f16d825eadb450fea/papers/A1-english-v32-causal-certificates/RESPONSE_TO_REFEREE.md).
- **S3:** [Current source-publication record](https://github.com/TrillionniumFoundation/theta-theory/blob/e712437fe13cf29978715d3f16d825eadb450fea/papers/A1-english-v32-causal-certificates/revision-v32/SOURCE_PUBLICATION.json) and [current README](https://github.com/TrillionniumFoundation/theta-theory/blob/e712437fe13cf29978715d3f16d825eadb450fea/papers/A1-english-v32-causal-certificates/README.md).
- **S4:** [Controlling commit](https://github.com/TrillionniumFoundation/theta-theory/commit/e712437fe13cf29978715d3f16d825eadb450fea).
- **S5:** [Persistent-state definition](https://github.com/TrillionniumFoundation/theta-theory/blob/e712437fe13cf29978715d3f16d825eadb450fea/papers/A1-english-v32-causal-certificates/text/operational_model.tex) and [risk quantifiers](https://github.com/TrillionniumFoundation/theta-theory/blob/e712437fe13cf29978715d3f16d825eadb450fea/papers/A1-english-v32-causal-certificates/risk_criteria.tex).
- **S6:** [Information and resource ledger](https://github.com/TrillionniumFoundation/theta-theory/blob/e712437fe13cf29978715d3f16d825eadb450fea/papers/A1-english-v32-causal-certificates/v32/model_ledger.tex).
- **S7:** [Attainable transversality](https://github.com/TrillionniumFoundation/theta-theory/blob/e712437fe13cf29978715d3f16d825eadb450fea/papers/A1-english-v32-causal-certificates/core/03_transversality.tex).
- **S8:** [Confluent positivity and whole-image covering input](https://github.com/TrillionniumFoundation/theta-theory/blob/e712437fe13cf29978715d3f16d825eadb450fea/papers/A1-english-v32-causal-certificates/text/analytic_inputs.tex).
- **S9:** [Collision scales and attainable Newton flags](https://github.com/TrillionniumFoundation/theta-theory/blob/e712437fe13cf29978715d3f16d825eadb450fea/papers/A1-english-v32-causal-certificates/text/collision_flags.tex).
- **S10:** [Checkpoint and causal classification proofs](https://github.com/TrillionniumFoundation/theta-theory/blob/e712437fe13cf29978715d3f16d825eadb450fea/papers/A1-english-v32-causal-certificates/text/collision_direct.tex) and [leading theorem](https://github.com/TrillionniumFoundation/theta-theory/blob/e712437fe13cf29978715d3f16d825eadb450fea/papers/A1-english-v32-causal-certificates/text/main_classification.tex).
- **S11:** [Theorem-level positioning](https://github.com/TrillionniumFoundation/theta-theory/blob/e712437fe13cf29978715d3f16d825eadb450fea/papers/A1-english-v32-causal-certificates/v32/positioning.tex).
- **S12:** [Native two-volume builder](https://github.com/TrillionniumFoundation/theta-theory/blob/e712437fe13cf29978715d3f16d825eadb450fea/papers/A1-english-v32-causal-certificates/revision-v32/build_native.py).

**L1.** C. Amato, D. S. Bernstein and S. Zilberstein, *Optimizing fixed-size stochastic controllers for POMDPs and decentralized POMDPs*, Autonomous Agents and Multi-Agent Systems (2010), [publisher record and abstract](https://link.springer.com/article/10.1007/s10458-009-9103-z). Used for the finite-controller nonlinear-optimization precedent, not an assertion of identical objectives or resources.

**L2.** N. Saldi, S. Yüksel and T. Linder, *Near Optimality of Quantized Policies in Stochastic Control Under Weak Continuity Conditions*, [arXiv:1410.6985v2, full HTML](https://arxiv.org/html/1410.6985v2), especially Theorem 3.2 and the partially observed application. Used for a specific finite-action approximation comparison, not as a theorem automatically imposing the present finite-memory constraint.

**L3.** N. Saldi, S. Yüksel and T. Linder, *Finite Model Approximations and Asymptotic Optimality of Quantized Policies in Decentralized Stochastic Control*, [arXiv:1511.04657](https://arxiv.org/abs/1511.04657). The abstract was checked for relevance; a complete theorem-by-theorem subsumption audit was not performed.

**L4.** S. Yüksel and T. Linder, *Optimization and Convergence of Observation Channels in Stochastic Control*, SIAM Journal on Control and Optimization, [DOI 10.1137/100808976](https://epubs.siam.org/doi/10.1137/100808976). Used for the observation-channel continuity comparison with its published scope qualifications.
