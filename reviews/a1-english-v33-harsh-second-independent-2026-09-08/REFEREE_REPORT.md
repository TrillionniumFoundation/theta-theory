# Second independent referee report on A1 v33

**Manuscript:** *Attainable information, exponent collisions, and finite-state realization*, Qian Qi.  
**Assessment date:** 8 September 2026.  
**Repository:** `TrillionniumFoundation/theta-theory`.  
**Reviewed branch:** `revision/a1-english-v33-moment-controllers-2026-09-08`.  
**Controlling manuscript commit:** `e7dfc3a0e1c8d7a9d3be6b7f52944c5c7c59bb0c`.  
**Controlling tree:** `87ebcf22288819a124b9d1488fdcc0af81a82bd3`.  
**Native manuscript directory:** `papers/A1-english-v33-moment-controllers/`.  
**Preceding v32 report identified by the revision:** `60c5b116a2c002dfd8056a351a87d7014d8c78e1`.  
**This review branch:** `review/a1-english-v33-harsh-second-independent-2026-09-08`.  
**Requested journal standard:** Annals of Mathematics, Inventiones Mathematicae, Journal of the American Mathematical Society, or Acta Mathematica.  
**Recommendation:** **Reject at the requested four-journal level, in its present form.**

This is an owner-requested, AI-assisted independent referee-style assessment, not a report commissioned by any of those journals. “Second independent” distinguishes this new branch from an already existing v33 review branch; that branch is not overwritten. Its report text was not used to derive the conclusions below. The mathematical subject of this assessment is the pinned revision, not the current default branch.

## 1. Recommendation to the editor

The revision is materially better than the manuscript discussed in its controlling v32 report. It now gives an exact representation of the original prescribed-command common-controller problem without full-history optimization variables. It correctly accounts for the shared failure report, proves a suitably restricted purification theorem, derives polyhedral rules for scalarized mean loss, and supplies an analytically solved, genuinely continuous-command instance with a reproducible global certificate. The revised distinction between statistical collision rates and voluntarily chosen numerical accuracy is also correct. These are substantive improvements, not changes of vocabulary. [S1–S4]

**I have not established a fatal counterexample to the new named v33 statements under their printed hypotheses.** In particular, this report does not allege a hidden public seed, an oracle decoder, a substitution of separate checkpoint encoders for a common controller, or an unproved convex minimax exchange. The manuscript explicitly avoids these errors, and its relevant arguments survive the examination described below.

Nevertheless, I do not recommend acceptance, or an invitation to a routine revision, at the requested level. The strongest publication-bearing mathematics remains the inherited collision-uniform classification of the attainable experiment. The new controller layer is useful, but its main mechanisms are a finite-output garbling body, conditional-state propagation in a finite product space, quadratic centroid decoding, finite-function purification, and compact minimization. Its connection with the exceptional collision geometry is predominantly a transfer of the already established risk bounds to an exact variational representation. The revision does not yet establish that the combined article provides a comparably substantial new understanding of optimal causal organization.

This judgment is not based on the absence of a polynomial-time algorithm. A nonconstructive or computationally expensive structural theorem can be outstanding. The issue is what additional mathematical structure has actually been identified, beyond a correct and sometimes economical representation of the optimization problem. Section 5 supplies explicit reductions rather than treating the word “classical” as an argument.

The author has also answered the previous delivery criticism: current source-hashed full-volume build receipts are present, and the original-model arithmetic certificate is independently reproducible. Those matters must not be recycled as unresolved objections. They do not, by themselves, settle significance. The recommendation concerns this submission, not the feasibility or eventual value of the research program.

## 2. Submission identity and scope of the examination

The controlling commit is dated **8 September 2026, 08:19:47 UTC / 16:19:47 Singapore time**. It materializes the v33 directory and identifies the v32 referee response as its parent context. The revision search was followed beyond its returned final set to an empty page. The already existing branch `review/a1-english-v33-harsh-independent-2026-09-08` was detected while choosing a publication destination; this report uses a separate new branch based directly on the reviewed manuscript. [S0]

I read the complete new moment-controller, precision, exact-instance, introduction and comparison modules; the complete active finite-compatibility, command-approximation and certificate module; the risk and finite-state definitions; the main classification statement; and the inherited monomial tangent, mixed/confluent pairing, Newton-flag, thin-rectangle covering and causal-realization proof chain. I also examined the response letter, the current build wrapper, the source/PDF-hash receipt, the session checks, and the exact-arithmetic program. Source labels, rather than independently regenerated theorem numbers, control the references in this report. [S1–S9]

This is **not** a fresh line-by-line verification of all 159 companion pages, all historical branches, or all eleven planned papers. The complete two-volume TeX build and PDF visual inspection were **not independently performed in this assessment**. The cited real-geometric entropy theorem was not reconstructed from its original monograph. The external literature check was targeted, not an exhaustive originality search; the exact theorem-number correspondence of every finite-approximation reference was not independently certified.

The independent executions are narrower and fully specified in Section 7. They test exact identities in concrete experiments and reproduce an analytically justified certificate. They are neither a general proof checker nor a global solution of the multistage optimization problem.

## 3. Disposition of the controlling v32 objections

| Earlier issue | Disposition after examining v33 |
|---|---|
| A chosen relative certificate power was being asked to carry statistical significance. | **Closed as a mathematical/presentation objection.** The arbitrary-precision theorem explicitly separates the chosen accuracy from the full collision profile. |
| Full-history compatibility alone did not identify additional structure. | **Substantially improved, but significance remains disputed.** The coefficient representation genuinely eliminates history-indexed controller variables. Its relation to generic finite-channel and finite-product constructions is analyzed below. |
| Different charging conventions obscured which model was being solved. | **Closed in the examined new main results.** The moment formula and continuum example use the original shared-latent, per-report convention. Block-charged developments are distinguished. |
| The original-model continuum certificate had not been executed. | **Closed.** The author script was replayed from a blob-verified copy, and its output exactly matches the committed receipt. |
| There was no current complete-volume build record. | **Closed as a missing-record objection.** Current receipts record both complete volumes. Their existence is verified; the referee has not independently rebuilt the volumes. |
| The literature comparison needed closer hypotheses and resource accounting. | **Improved.** The discussion now distinguishes action quantization, observation-channel approximation and retained labels. The new implementability body also needs positioning as a decision/garbling body. |

Closing an objection does not require accepting the paper. Conversely, rejecting the paper does not justify denying the repairs. In particular, the one-checkpoint example satisfies the earlier request for an executed original-model example; its limited ability to illuminate multistage optimization is a separate significance issue, not a retroactive failure to meet that request.

## 4. Mathematical examination

### 4.1 The common-failure implementability body

**Location:** `v33/moment_controllers.tex`, `lem:v33-body`, `cor:v33-overlap`, and `eq:v33-support`. [S1]

The body is correctly defined by

$$
A_{kj}=m_k r_{kj}+z_{kj},\qquad
m_k=\int g_k\,d\nu,\qquad
z_{kj}=\int(1-g_k)u_j(g)\,d\nu,
$$

where the accepted-report rows may be chosen separately, but the failure allocation uses one common simplex-valued function. This coupling is not optional: the observed failure report does not disclose its underlying raw cell.

The weak-star argument is adequate. Simplex-valued elements of a finite product of unit balls of $L^\infty(\nu)$ form a weak-star compact convex set, and integration against the finitely many bounded weights is continuous. On the Borel command cube the equivalence classes have measurable representatives, with null-set modifications made in the simplex. The constant accepted-report realization is legitimate because $m_k>0$.

Pointwise maximization gives the exact support function

$$
h_{\mathscr A}(C)=\sum_km_k\max_jC_{kj}
 +\int\max_j\sum_k(1-g_k)C_{kj}\,d\nu.
$$

A smallest-index tie rule is measurable. The compulsory overlap bound also follows directly by placing $\min(1-g_k,1-g_l)u_j$ below both row contributions before summing over $j$. It correctly excludes arbitrary disjoint stochastic rows. The independent finite-command check enumerates all 64 deterministic rules in a two-cell, two-command, two-label instance and verifies this support function for 81 coefficient matrices. This supports that instance; compactness and necessity/sufficiency are established by the analytic argument, not by enumeration.

### 4.2 Conditional occupancies and the exact mean-risk formula

**Location:** `thm:v33-moment-program`, `eq:v33-q-recursion`, `eq:v33-fixed-decoder`, and `eq:v33-baseline`. [S1]

For prescribed independent commands, the recursion

$$
q_{n,j}(t)=\sum_{i,k}q_{n-1,i}(t)k_k^a(t)A_{n,kj}(i)
$$

is correct. Conditional on the latent parameter and preceding label, the current command still has its prescribed law. Integrating the observed report and update produces precisely one implementable matrix for each time-state pair. Conversely, the one-step lemma supplies a transition kernel for every chosen matrix, and induction realizes the entire common controller. The functions $q$ are an offline description of its law, not an extra retained state.

The important loss identity uses conditional independence of the latent parameter and retained state given the complete command-report history. A fixed history contributes its latent likelihood times a state-path weight that does not depend on the latent parameter. Summing state paths preserves this factorization. Therefore

$$
\mathbb E[p_{nq}(H_n)d_{nq}(S_n)]
 =\mathbb E[H_{nq}(t)d_{nq}(S_n)]
 =\sum_i b_{niq}d_{nq}(i).
$$

This is what justifies the stated baseline-plus-quadratic formula; it is not an invocation of sufficiency of the retained label. Completing squares gives the conditional centroids. Since each decoder entry belongs to one checkpoint, centroid choices minimize the checkpoint losses simultaneously, while the transition variables remain common to all checkpoints.

The zero-occupancy extension is valid: $0\le b\le w$ implies $0\le b^2/w\le w$. Thus the objective extends continuously to $w=0$ and attains its minimum on the finite product of implementability bodies. The prior-moment degree bound is also correct. A degree-$n$ occupancy multiplied by a future product of degree $N-n$ uses moments only through degree $N$; squaring an already evaluated moment does not require moments through degree $2N$.

The baseline still contains an integral over commands and a sum over report words. The manuscript says so. Accordingly, “no history-indexed controller variables” is justified, whereas “the whole computation has polynomial cost” would not be. The printed theorem does not make the latter claim. Our three-stage diagnostic independently verifies the occupancy polynomials and the fixed-decoder loss identity against complete history enumeration.

### 4.3 Purification

**Location:** `lem:v33-purification` and `thm:v33-pure`. [S1]

The finite-function purification proof is valid. At a nonvertex extreme point of the constrained simplex-valued function set, two coordinates are bounded below on a positive-measure set. Splitting that set into more pieces than the number of moment constraints gives a nonzero bounded perturbation annihilating all of them. Opposite perturbations contradict extremality. Atomlessness is used exactly at the splitting step.

Applying this argument separately to each accepted report with weight $g_k$, and to failure with all weights $1-g_k$, preserves every entry of the same implementability matrix. Induction then preserves the conditional occupancy laws for every latent parameter, and the fixed-decoder identity preserves the whole vector of **unconditional** checkpoint risks.

The scope restrictions are essential and correctly printed. Atomlessness belongs to the command law, not the latent prior. The result does not preserve the risk of every individual history, does not imply equality of worst-history optima, does not eliminate a persistent seed indexing different decoder programs, and does not assert jointly measurable purification of an arbitrary calibration-indexed family. No counterexample to these stronger claims is needed, because the manuscript does not make them.

The mechanism is classical finite-function purification, explicitly acknowledged by the author. The relevant comparison is not merely informal deterministic-policy intuition; see [L1, L2]. Its recursive application here is a valid consequence of the coefficient reduction.

### 4.4 Polyhedral scalarized policies

**Location:** `thm:v33-polyhedral`. [S1]

The proof starts from a **global** minimizer, freezes its decoders and all but one time-state matrix, and observes that each path encounters that matrix only once. The resulting objective is affine in that matrix. The support formula therefore supplies a constant accepted-report choice and an affine-comparison failure choice. Replacing the row cannot improve below the global minimum, so it preserves global optimality. Repeating the replacement retains the asserted form of earlier rows.

There is no local-to-global optimization fallacy here. Nor is atomlessness required: pointwise selection attains the linear support problem even for atomic commands. Lexicographic assignment on affine ties should be understood as the partition convention on the polyhedral boundaries.

The theorem is, however, for a fixed nonnegative scalarization of checkpoint mean losses. It does not show that an optimum of the maximum-checkpoint objective is exposed by some scalarization, nor that its deterministic purification can be chosen polyhedral. The manuscript explicitly acknowledges this distinction. It is a limit of the structural conclusion, not a demonstrated error.

### 4.5 Collision transfer

**Location:** `thm:v33-collision`. [S1]

The fixed-$M$ compactness argument is sound. On the compact calibration chamber, positive one-step exponents remain bounded away from zero, so the cell functions are jointly continuous including at latent value zero. The polynomial occupancies, their moments, and the positive-evidence baseline are jointly continuous. The perspective extension handles vanishing label masses. Minimization occurs on one compact domain independent of calibration.

Substitution of a minimizer at the limiting calibration gives the upper-limit inequality; a convergent subsequence of minimizers gives the lower-limit inequality and optimality of its limit. The finite recursion then yields uniform-in-latent-parameter convergence of the conditional state probabilities. This is convergence of the stated laws, not of particular Borel transition partitions.

The final comparison with $\Xi_N$ is obtained by combining the exact value formula with the inherited collision theorem. It does not independently rederive that profile from the moment optimization. The author correctly separates fixed-$M$ continuity from the uniform-in-$M$ comparison. No sharp leading constant or optimizer convergence rate is asserted.

### 4.6 Finite compatibility and arbitrary precision

**Locations:** `v33/finite_compatibility.tex` and `v33/precision.tex`. [S2]

The finite formulation retains one common row for every history arriving at the same time-state pair. In the state-controlled extension, the command-before-report constraint is explicitly enforced. The posterior factorization used in the coefficients remains valid: conditioning on a selected command reweights the conditional state factor, while the next report updates the latent likelihood factor. This does not give the decoder a posterior oracle.

The lifted-command approximation also handles arbitrary Borel transitions correctly. It first replaces likelihoods by cellwise-constant likelihoods on the **same** continuous command space; only then does it average the within-cell update. It does not claim total-variation convergence of continuous command measures to finitely supported measures. For worst-history risk, restriction to representative histories is legitimate because the criterion uses a supremum over all admitted histories, not an essential supremum.

Rational row rounding gives total variation error at most $(M-1)/b$ per transition; decoder rounding contributes $2/b$. Thus the printed error $[T(M-1)+2]/b$ is consistent. The lower certificate requires every member of the finite net, or a rigorous replacement covering it; evaluation of a few candidate controllers is not substituted for coverage.

For $s>2$, choosing $\delta\le M^{-s}$, $b=\lceil M^{s+1}\rceil$ and enclosure width $\tau\le M^{-s}$ gives absolute width $O(M^{-s})$. Dividing first by $c\Xi_N$ and then using its $M^{-2}$ floor gives relative width $O(M^{2-s})$. The net cardinality is explicitly stated. This is correct arbitrary-precision certification, not a newly discovered statistical exponent. The earlier criticism on this point is answered.

### 4.7 The exact continuous-command example

**Location:** `v33/exact_instance.tex`, `thm:v33-exact-example` and `cor:v33-enclosure`. [S3]

The example uses a uniform full-support prior, positive affine detector cells, a genuine two-dimensional continuous command cube, and one compression after one acquisition report. Its two future likelihoods form an attainable basis, although one query is constant.

Let $a_*=1/240$ and center the nonconstant prediction at $1/2$. The acquired variable $Y$ has atoms of mass $1/4$ at each of $\pm a_*$, and a symmetric central component of mass $1/2$ contained in $[-a_*/10,a_*/10]$. The failure component includes the evidence weight $(u+v)/2$. Omitting that weight would change the second moment; the proof does not omit it.

For an arbitrary stochastic binary encoder, conditionalization on $Y$ preserves its output mass $p$ and correlation $v=\mathbb E(YQ)$. Centroid decoding explains $v^2/[p(1-p)]$. Symmetry and label complementation reduce the bound to $p\le1/2$, $v\ge0$. For $p\le1/4$ the atom bound suffices. For $p=1/4+s$, an upper-tail argument and the central support bound give the displayed positive margin $37s/400$. Thus the maximum explained variance is exactly $a_*^2/3$, attained by retaining whether accepted cell 1 occurred.

This proves optimality over **all** admitted Borel stochastic encoders. It is not a grid-search assertion. The resulting risk

$$
\mathfrak R_{2,2}^{\mathrm{av}}
 =a_*^2\left(\frac1{12}+\frac{J_*}{4}\right),\qquad
J_*=\mathbb E\frac{(U-V)^2}{U+V},
$$

and the reported decoders check out. The nonnegative geometric series supplies the rational enclosure. Its global lower coverage rests on the analytic upper-tail proof, not on the arithmetic script. The independent replay and separate integration check agree with the claimed endpoints.

### 4.8 The inherited classification that still carries the paper

**Locations:** `text/main_classification.tex`, `core/03_transversality.tex`, `text/analytic_inputs.tex`, `text/collision_flags.tex`, and `text/collision_direct.tex`. [S5–S8]

The attained geometry is materially stronger than a dimension count for an arbitrary posterior family. The binomial-factor construction identifies an actual monomial tangent of dimension $n(r-1)+1$ inside feasible acquisition commands. Strict mixed-moment positivity pairs it with the required future tests for a fixed full-support prior, including singular priors. Normalization removes exactly one direction. The confluent argument uses complete multiplicity blocks, which is important at collisions.

The finite Leja ordering gives uniformly conditioned raw-to-scaled coordinates on the nonzero block, with zero pivots handled without division. Maximal Vandermonde volumes are comparable to products of initial scales. The uniform acquired chart includes the all-failure evidence and gives a positive-mass minorization, not merely a geometric image with no probability attached.

The covering argument treats prior integrals and node values as real coefficients of bounded-format semialgebraic sets. It does not require semialgebraic dependence on calibration. Conditional on the cited real entropy input, the projected-rectangle argument and the separate small-integer-budget step support the claimed covering radius. The causal upper bound uses reachable raw representatives and positive-evidence quotient updates; it does not propagate unstable divided differences or retain an uncharged history tape. Finally, checkpoint lower laws are prefixes of one common exploration law.

I did not find a contradiction in this audited dependency chain. I also do not regard these observations as a substitute for a specialist assessment of the core theorem's originality in attainable information geometry and collision-dependent quantization. That core deserves to be judged on its own mathematical content. Adding certification precision or generic compact-control consequences should not be used as a proxy for such an assessment.

## 5. Decisive reservations about significance

### 5.1 The exact body has a direct finite-experiment interpretation

For each raw cell $k$, define a probability measure on the observed command-report space by

$$
Q_k(dg,dx)=\nu(dg)\bigl[g_k\delta_k(dx)+(1-g_k)\delta_\dagger(dx)\bigr].
$$

Then the body in Section 8 is exactly

$$
\mathscr A_M(\nu)=\left\{A:\ A_{kj}=\int U(j\mid g,x)\,Q_k(dg,dx)\right\}.
$$

This is a finite-output postprocessing, or garbling, body of the finite family $(Q_k)$. Its support function follows by maximizing a linear decision payoff pointwise. The positive row overlap reflects the common failure component. These statements are an explicit reduction of the printed definition, not a claim that an earlier article contains A1 verbatim.

The reduction explains both the value and the limit of the new lemma. It is an exact and useful experiment-specific feasibility description, but compact convexity, the support formula, and deterministic linear optimizers are not independent deep phenomena. A serious novelty comparison should identify what remains after this reduction. The present finite-approximation comparison is improved, but does not itself answer that question. Finite-controller nonlinear programming and finite-function purification already have direct precedents [L1–L3]; the manuscript cites such antecedents, so lack of all attribution is not the objection.

### 5.2 The new moment layer is largely independent of monomial collision geometry

The following observation is useful in evaluating the claimed synthesis.

**Generic finite-detector reduction.** Replace the latent interval by any probability space, and replace the monomial detector by any finite family of measurable nonnegative cells $k_1,\ldots,k_J$ summing to one. Retain independent prescribed commands, the same accepted/failure observation mechanism, a fixed finite horizon, and future likelihoods that are polynomials in those cells of the indicated remaining degree. With the same positive-evidence condition where used, the implementability body, occupancy recursion, exact mean-risk formula, and moment-degree bound remain valid.

**Proof.** The observed law conditional on a raw cell is precisely $Q_k$, independently of how the function $k_k$ is represented. Integrating the state update gives the same recursion. Repeated substitution makes each occupancy a homogeneous degree-$n$ polynomial in the cells. Integrating it alone or multiplied by a remaining-degree query uses finitely many cell-product moments of degree at most $N$. Conditional independence given the complete history and completion of the square give the identical risk expression. Compactness and the bound $b^2/w\le w$ give attainment. None of these steps invokes ordered exponents, a Chebyshev system, tangent transversality, or additive collisions. The purification and scalarized support arguments likewise depend on the observation measures, not on monomial identities. This proves the observation.

This generality is a virtue, not a counterexample. It also shows that most of the new layer is a generic finite-detector construction. The special collision geometry enters through evaluation of coefficients, continuity under the selected parameterization, and substitution of the previously proved comparison with $\Xi_N$. The paper needs a sharper statement of what mathematical interaction, rather than coexistence, the combined theory delivers.

### 5.3 The principal minimax controller remains variationally specified

The history elimination is genuine. The representation uses finitely many one-step entries and polynomially many formal occupancy coefficients in the horizon for fixed $J$. But the principal maximum-checkpoint optimum is still given as a nonconvex minimum over those entries. Purification preserves this value without identifying the optimizing partition, while the polyhedral theorem applies to a different, scalarized objective.

Neither fact is a defect in the stated theorems. They limit the assertion that the revision has classified optimal common-controller organization. There is no derived description of active checkpoint tradeoffs, collision-induced changes of optimal transition structure, or a quantified causal compatibility cost in a nontrivial multistage instance of this same model. Such a result would strengthen the proposed synthesis; it is not logically required to make the existing formulas true. I would not prescribe an arbitrary new theorem as an endless condition of acceptance. The editorial question is whether the current contribution, accurately delimited, meets the requested threshold. In my judgment it does not.

### 5.4 Compact collision transfer is not a second collision classification

The fixed-domain continuity theorem is a correct compact minimization argument. Its all-budget risk conclusion imports the inherited classification. It does not show how optimizing controllers bifurcate, select labels, or reorganize at a collision. The author now avoids claiming convergence rates or sharp constants; that is good mathematical discipline. Nonetheless, the additional theorem should be presented with weight proportionate to what it establishes, rather than serving as the principal evidence that the exact optimization layer adds a new collision theory.

### 5.5 The executed example is conclusive but structurally small

The continuous-command example is fully legitimate and globally solved. Its precision is genuine. However, $N=2$ means one acquisition and one compression, and only one scalar target contributes loss. The controller ignores the command and isolates one separated atom. There is no competition between checkpoint objectives and no need to reconcile different future uses of an intermediate state.

It therefore validates the original protocol and certificate arithmetic, but is not evidence that the new multistage moment formulation resolves the causal coupling that motivated its introduction. The distinction should be stated without devaluing the example or pretending that continuum optimization was not actually solved.

## 6. Priorities for a substantive revision

The immediate priority is an honest contribution hierarchy, not another layer of validation terminology. The inherited attainable collision theorem should be stated as the principal result, with its closest geometric and statistical antecedents compared at the level of hypotheses and conclusions. The coefficient description should be presented as an exact finite-detector realization theorem, and its genuinely new experiment-specific content isolated from the garbling, forward-recursion, centroid, purification and compactness mechanisms described above.

A useful next mathematical target would connect the coefficient optimization to a genuinely multistage phenomenon in the original per-report model: for example, an exact compatibility cost between two checkpoint objectives, or a collision-dependent change of an optimal controller characterized on a nontrivial parameter family. This is a direction that would address the present significance concern, **not** a claim that every such result is necessary, sufficient, or guaranteed to secure acceptance. Merely increasing a numerical certificate exponent cannot address it.

The main article should also maintain the following distinctions throughout: prescribed versus controller-selected acquisition; mean versus worst-history risk; private coins versus a persistent decoder-indexing seed; fixed-$M$ continuity versus all-budget estimates; representation size versus coefficient evaluation versus global solution cost. The v33 statements mostly do this already. These distinctions should be retained, not weakened in response to a demand for a more impressive abstract.

No deletion of the historical proofs is requested. Their preservation is compatible with a focused submission and a separately organized companion. Nor is an efficiency theorem, a density assumption on the prior, calibration-blind coding, or a reduction of the horizon demanded as a repair of a false statement. No such false statement has been established here.

## 7. Reproducibility and evidentiary limits

### 7.1 Exact replay of the author's certificate

The fetched `v33/certify_instance.py` was copied locally and checked against its Git blob identity:

- Git blob: `36d5f623f4452d55ed79e606d095a7db8a865d91`.
- Source SHA-256: `c7796f9440cbd2e48a0ad41a79d1517deef17054f87f6af04233a2c81b588172`.
- Output SHA-256: `a297123da52c971a86e36b0517d0eb6b345231660c753e8572f644eb4b2aafb4`.

Normal and `python -O` execution produced byte-identical output. The output hash equals the hash recorded in the author's committed `SESSION_CHECKS.json`. The verified rational interval is

$$
L=\frac{18108150189130829}{12454041600000000000000},\qquad
U=\frac{150901251576091}{103783680000000000000},\qquad
U-L=\frac1{136857600000000000000}.
$$

The copied source and replay result are included in this review directory. This replay verifies arithmetic execution and its provenance; global coverage still rests on the analytic theorem examined in Section 4.7.

### 7.2 Independent three-stage and support-function checks

`audit/independent_checks.py` uses standard-library exact rational arithmetic and checks that remain active under Python optimization. Its normal and optimized outputs agree. **101 checks pass.**

The multistage instance has one shared uniform latent parameter, two positive affine detector cells, two labels, and three acquisition stages. It uses an explicitly specified **atomic prescribed command law**, admissible in the general Section 8 formulation. Complete enumeration produces 6, 36 and 216 command-report histories at the three checkpoints. Their directly computed risks agree exactly with the occupancy-polynomial and centroid identities. The future menus contain 8, 4 and 2 ordered failure-factor products respectively. These are checks of one specified common controller, not globally optimal risks.

A separate enumeration of all 64 deterministic one-step rules tests 81 support functionals and gives minimum row overlap $17/60$ for its selected command law. It excludes the disjoint-row identity matrix. This finite atomic calculation does not test atomless purification.

A separately derived series calculation reproduces the continuum certificate. As an additional diagnostic, changing variables to sum and difference yields

$$
J_*=\frac{100}{3}\left[
\int_{9/10}^{1}\frac{(s-9/10)^3}{s}\,ds+
\int_{1}^{11/10}\frac{(11/10-s)^3}{s}\,ds
\right].
$$

Its logarithmic antiderivative, evaluated at high decimal precision, gives risk approximately $1.453997888455008\times10^{-6}$, inside the rational interval. This decimal cross-check is explicitly **not** a formally directed interval proof.

### 7.3 Full-volume build record

The committed receipt records six successful compiler invocations, current hashes of 79 active TeX inputs, no unresolved-reference or overfull-box entries, and generated main/companion PDF hashes. The session record reports 35 main pages and 159 companion pages, and describes the author's contact-sheet and selected enlarged-page inspection. The build wrapper compiles both actual entrypoints and checks cross-volume label convergence; it is not merely a short theorem-packet builder. [S9]

These are author execution records that were inspected, not a build performed by this referee. The distinction is explicit in the accompanying audit manifest. There is no claimed GitHub Actions pass, formal proof-assistant verification, independent full-PDF proofread, or exhaustive general-controller-net computation in this assessment.

## 8. Source ledger

All native paths below are relative to `papers/A1-english-v33-moment-controllers/` at the controlling manuscript commit, unless otherwise indicated. The stated Git blobs identify the exact versions examined.

- **[S0]** Revision branch/commit metadata: `e7dfc3a0e1c8d7a9d3be6b7f52944c5c7c59bb0c`; tree `87ebcf22288819a124b9d1488fdcc0af81a82bd3`. Prior report: `reviews/a1-english-v32-harsh-independent-2026-09-08/REFEREE_REPORT.md` at `60c5b116a2c002dfd8056a351a87d7014d8c78e1`, consulted for the controlling objections, not adopted as evidence of correctness.
- **[S1]** `v33/moment_controllers.tex`, blob `e15db79f462b9d8395cc4368296f4d0f10d6a48c`: one-step body, exact formula, purification, scalarized polyhedral realization, collision continuity. Entire module read.
- **[S2]** `v33/finite_compatibility.tex`, blob `6254d766c1469292dbc1125a1eea3fd42de571de`; `v33/precision.tex`, blob `f54e913c2e7e0e0f4db2a5572ded6b53ec431479`. Entire active modules read.
- **[S3]** `v33/exact_instance.tex`, blob `8c79906419c9974425fcd0c65d7c6a18eb5dd4a0`; `v33/certify_instance.py`, blob `36d5f623f4452d55ed79e606d095a7db8a865d91`. Entire sources read; script independently replayed.
- **[S4]** `v33/introduction.tex`, blob `a572397e9cadf48ec5924b922fbfa3cdecc7194b`; `v33/comparison.tex`, blob `9e1902dc7ca3b10a2281d7d7587b604dad37b68f`; `RESPONSE_TO_REFEREE_V33.md`, blob `d9d5f043742d08b5cbcc3fcdf85a1535de2d5f1c`; `main.tex`, blob `e18b822681cef140a3cab51d926133f020eb6255`.
- **[S5]** `risk_criteria.tex`, blob `da5403fdde6bed138d33b252d52d75e4255c8528`; `text/operational_model.tex`, blob `62b00087d3000d1a6303b7f65479047172a851e2`; `text/main_classification.tex`, blob `307a694dacddee85104212dfa51a222053ee1769`.
- **[S6]** `core/03_transversality.tex`, blob `6395724ba2c4bed3ead19178a1cfe8206f9a3824`: mixed positivity, attainable tangent, normalized rank, continuous-state causal attainment.
- **[S7]** `text/analytic_inputs.tex`, blob `92c431918df8894dbab4e2bef267a1b3d086370c`; `text/collision_flags.tex`, blob `558972ba3ad6f42ca1f782b80fed4b7ef9a87fe8`: confluent pairing, entropy input, Leja conditioning and acquired flag minorization.
- **[S8]** `text/collision_direct.tex`, blob `12db8bce89cd0a731cb3bc5c383c3c70699ced60`: checkpoint classification and one common causal transducer.
- **[S9]** `v33/build_revision.py`, blob `5ea3dc605f19c166af74b38b0e6f8bf9288285c6`; `verification-v33/BUILD_RECEIPT.json`, blob `045b34c4a0f7b2a3d479b91cfbfac81f9cca4b06`; `verification-v33/SESSION_CHECKS.json`, blob `0a83fc21f351c02ab20b6d5bf3bf1805ef2e2975`; `README.md`, blob `3ab7da655fe062c1591cb01bf241c1d845edbaa8`.

### Targeted external comparisons

**[L1]** M. Ali Khan, Kali P. Rath and Yeneng Sun, “The Dvoretzky–Wald–Wolfowitz theorem and purification in atomless finite-action games,” *International Journal of Game Theory* **34** (2006), 91–104. DOI: [10.1007/s00182-005-0004-3](https://doi.org/10.1007/s00182-005-0004-3). The publisher abstract explicitly identifies elimination of randomization preserving integrals for finite action spaces and finitely many atomless measures. It supports the purification comparison, not a claim of prior publication of A1's whole controller theorem.

**[L2]** Eugene A. Feinberg and Alexey B. Piunovskiy, “On Strongly Equivalent Nonrandomized Transition Probabilities,” *Theory of Probability and Its Applications* **54** (2010), 300–307. DOI: [10.1137/S0040585X97984255](https://doi.org/10.1137/S0040585X97984255). The publisher abstract describes nonrandomized transition probabilities preserving integrals of finitely many functions with respect to finitely many atomless measures. The comparison here is to that finite-integral mechanism; no unqualified extension to infinitely many moment constraints is inferred.

**[L3]** Christopher Amato, Daniel S. Bernstein and Shlomo Zilberstein, “Optimizing Memory-Bounded Controllers for Decentralized POMDPs,” *Proceedings of UAI 2007*, 1–8; later repository copy [arXiv:1206.5258](https://arxiv.org/abs/1206.5258). The primary abstract formulates fixed-size stochastic-controller optimization as nonlinear programming and discusses local optimization. The model differs from A1; this is a direct antecedent for the optimization paradigm, not an identification of the two information structures or a claim of an efficient global solution.

The manuscript itself supplies the finite-approximation references discussed in its Section 13. The comparisons above supplement that discussion. No assertion is made that a targeted search proves exhaustive absence or presence of prior art for the inherited collision classification.

## 9. Final assessment

The revision makes real repairs and contains a coherent new finite-moment representation. Its exact original-model continuum certificate survives both analytic examination and independent arithmetic replay. The principal new statements examined here should not be dismissed as false merely because the publication recommendation is negative.

My recommendation remains **rejection at the requested four-journal level**. The decisive reservation is the gap between a correct collection of realization, purification, approximation and compactness results and a demonstrated exceptional structural advance in the optimal common-controller problem. The inherited attainable collision theorem remains the center of mathematical gravity. A future submission should make its originality and significance persuasive on their own terms and make the controller layer's added interaction with that geometry precise, rather than trying to turn proof volume, certificate precision, or a successful build into evidence of journal-level depth.
