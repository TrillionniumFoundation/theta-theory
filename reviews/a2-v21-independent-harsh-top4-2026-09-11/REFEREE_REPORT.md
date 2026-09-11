# Independent harsh referee-style report on A2 v21

**Manuscript:** Qian Qi, *Boundary laws, signed contact rigidity, and physical information in dispersing billiards*  
**Review date:** 11 September 2026  
**Requested standard:** *Annals of Mathematics* / *Acta Mathematica* / *Inventiones Mathematicae* / *Journal of the American Mathematical Society*  
**Author revision branch:** `revision/a2-v21-nondominated-lan-registered-transfer-2026-09-11`  
**Immutable revision-branch head reviewed:** `d9f25f78ec43f575e40e6efb404be4e94ef1f3fe`  
**Canonical manuscript-source commit:** `672b159ef204ba75a63ab92a4d52ae3960304337`  
**Immediate predecessor report:** `reviews/a2-v20-independent-harsh-top4-2026-09-11/REFEREE_REPORT.md`  
**Principal active entry point:** `papers/A2-v17-boundary-information-coarsening/main.tex`

This is an author-requested, AI-assisted independent referee-style assessment. It is not a journal-commissioned report and is not an editorial decision by any journal named above. I have reviewed the active v21 source graph rather than treating the revision manifest or response letter as a proof certificate. I have also separated mathematical correctness, proof completeness, statistical experiment formulation, theorem scope, novelty/significance, exposition, and submission readiness.

## 1. Recommendation to the editor

**Recommendation: reject in the present form at the requested top-four level. A further substantially reconstructed manuscript could merit a fresh assessment.**

This recommendation should not be read as a mechanical repetition of the v20 report. V21 makes several serious repairs, and two of the most important v20 objections are, in my view, substantially resolved.

First, the central moving-support statistical theorem no longer writes a nonexistent Radon--Nikodym derivative for the original non-dominated family. The revision explicitly separates support-exclusive mass, introduces a parameter-independent common-collar censoring map, obtains a genuinely dominated representative, proves an explicit vanishing Le Cam comparison, and reserves the literal LAN likelihood expansion for that representative. This is the correct conceptual architecture.

Second, the physical statistical theorem now chooses a mathematically honest model: an anchored registered family in one fixed Euclidean laboratory chart. The observed endpoint coordinates are literal laboratory coordinates under one parameter-independent observation map. Generic contact translations and frame rotations are no longer silently removed; they are acknowledged as additional nuisance directions outside the main anchored theorem.

The quantitative exact-to-ideal Hellinger comparison and the tangent-level finite-design argument are also substantial improvements. I therefore do **not** find it defensible to reject v21 by simply repeating C20-M1 through C20-M4 as if the revision had not addressed them.

My negative recommendation rests on a different set of issues.

1. The all-order signed-jet theorem is now much more informative, and the displayed determinant-one block is internally consistent with the historical linear half-line orbit. However, the proof of the all-order stationary calculus still compresses several nontrivial infinite-dimensional and high-order differentiation steps into assertions that are too short for the theorem's central role. In particular, the derivative-order bookkeeping in the stationary equations is not written carefully enough to justify the claimed arbitrary-order jet dependence, and the weighted inverse, infinite-action differentiation, envelope identity, and highest-degree isolation require a genuinely self-contained argument.
2. The fixed-window statistical theorem is written for same-type `bb` endpoint laws, but the sequence `j_n` is not required to have the parity that produces same-type endpoints. The signed-rigidity section correctly uses an even number of flights; the physical statistical theorem merely states `j_n -> infinity`. For odd `j_n`, the active boundary law has opposite terminal type and the formulas `S_b(u)+S_b(v)`, `U_b`, and `K_{b,d}` are not the declared same-type experiment. This is a concrete theorem-statement defect, not a stylistic preference.
3. The deterministic cap construction has a quantifier problem. The caps are chosen using a compact local set `K`, while the subsequent theorem is phrased as one capped experiment uniform on every compact local set and is then fed into a local asymptotic minimax statement whose local radius is eventually sent to infinity. A single reference-based cap sequence can probably repair this, because the success probabilities are locally comparable, but the order of quantifiers must be made explicit.
4. The phrase “complete stopped transcript” remains too easy to overread. The historical transfer theorem compares a per-preparation **coarsening** consisting of the selected endpoint/residual-time record plus failure, and it explicitly does not compare the full growing collision array. V21 correctly retains failures, designs and stopping times inside that coarsened model, but this is not the complete raw collision history of every bridge. The theorem and headline language should state the observation level without ambiguity.
5. Even if the remaining proof and formulation issues are repaired, I am not yet persuaded that the present local theorem package clears the significance threshold of the four journals named above. The strongest deterministic contribution is a labelled one-channel local inverse from a continuum of signed endpoint-support data. The statistical contribution is a local endpoint-output experiment around a registered channel and deliberately discards a potentially faster waiting-time information channel. Contemporary billiard rigidity literature already contains global marked-length rigidity theorems under significant hypotheses, and more recent enriched marked-length work obtains global isometry conclusions for finite-horizon Sinai billiards. The present data are different and may be locally richer, so this is not a duplication objection. It is a top-four architecture objection: the paper still needs a broader geometric consequence, a universality theorem, or a complete physical limit experiment to make the conceptual payoff commensurate with the requested venue class.
6. The exact canonical source still has no successful native build certificate. The recorded workflow failed before any runner step executed. This is not evidence of a TeX error, but it is not submission verification either.

Thus my current view is: **mathematically serious, substantially improved, potentially publishable after further reconstruction, but not yet proved and positioned at Annals/Acta/Inventiones/JAMS standard.**

## 2. Scope of this review

I reviewed the v21 active source graph at the immutable revision head and canonical manuscript-source commit stated above, concentrating on the theorem chain promoted in the title, abstract, and introduction. In particular I inspected:

- `main.tex` and `article/01_introduction_v21.tex`;
- `article/01c_geometric_setup_v18.tex`, especially the channel-centered derivative convention and parity-dependent boundary law;
- `v4/10_boundary_layers.tex`, especially the half-line Green kernel, linear orbit, and nonlinear factorization;
- `v6/10_experiment_transfer.tex`, especially the precise observation space actually compared in total variation;
- `article/17_adaptive_experiments.tex`, especially the stopped-policy coupling and success-weighted budget;
- `article/23a_signed_endpoint_rigidity_v21.tex` in detail;
- `article/18a_vector_boundary_information_v21.tex` in detail;
- `article/18b0_anchored_realization_v21.tex`;
- `article/18b_raw_physical_multirate_v21.tex` in detail;
- the v21 response letter, manifest and verification record as audit aids rather than mathematical authority;
- the exact GitHub Actions evidence attached to the canonical manuscript-source commit.

I also rechecked the significance discussion against current dispersing-billiard rigidity literature, including the 2023 Inventiones marked-length spectral determination of analytic chaotic billiards with symmetry/genericity assumptions, Osterman's 2023 local/global marked-length results for open dispersing billiards, and the 2025 Finamore--Leguil preprint on enriched marked-length rigidity for finite-horizon Sinai billiards. I did **not** find an obvious published duplicate of the specific determinant-one signed endpoint jet mechanism claimed here. The significance concern below is therefore not a claim of plagiarism or known-theorem duplication.

As in any referee report of this scale, I have not machine-reproved every retained historical lemma. I have instead traced the active dependencies that feed the new v21 headline theorems and tested the new arguments at the interfaces where earlier revisions failed.

## 3. What v21 genuinely fixes

### 3.1 The non-dominated likelihood defect of v20 is substantially repaired

The revision correctly starts from

`f_theta = a_theta (w_theta)_+`

and explicitly states that the original local family need not be dominated. The new support-decomposition lemma gives compact-uniform one-observation support-exclusive mass of order

`p_n delta_n^2`,

so the product probability of ever observing a support-exclusive point is `o(1)` at

`n p_n delta_n^2 log(1/delta_n) -> 1`.

More importantly, the revision does not infer from this that a finite-sample likelihood suddenly exists. Instead it chooses

`q_n = delta_n (log(1/delta_n))^(1/4)`

and applies a parameter-independent censoring map which retains observations on the common collar `w_0 >= q_n` and sends the discarded successful observations to an extra atom. On compact local parameter sets all retained densities are mutually positive for large `n`, and the censored family is genuinely dominated.

The claimed comparison

`Delta_LeCam(original product, censored product)
 <= C n p_n q_n^2
 = O((log(1/delta_n))^(-1/2))`

has the right order. The forward kernel is the censoring map itself. A reverse parameter-independent kernel can replace the censoring atom by any fixed point; disagreement is then confined to the event that censoring occurred. This is a legitimate experiment comparison.

I also checked the score scaling. The singular score behaves like `V/w_0`; under the base density `a_0 w_0`, the second moment has the required logarithmic divergence, the third and fourth truncated moments have the printed powers of `q_n`, and the choice of `q_n` is compatible with Lindeberg and quadratic-variation convergence. I do not see the v20 finite-sample Radon--Nikodym error surviving in this formulation.

### 3.2 The fixed laboratory-coordinate model is now mathematically honest

The anchored graphs

`(-psi_0(u),u), (g+psi_1(v),v)`

are imposed in one fixed Euclidean chart with fixed labels, fixed transverse origin, and fixed tangent direction. The raw endpoint map returns literal laboratory `y` coordinates. This is exactly the sort of theorem-level model that the v20 report requested as Route A.

The separate anchored-realization proposition also matters. It shows that the finite labelled jet coordinates used statistically can be realized by actual nearby billiard tables via local bump perturbations while preserving strict convexity, disjointness and channel isolation after shrinking the parameter neighborhood. Hence the finite-dimensional statistical model is not merely a formal jet algebra.

The later remark about generic nearby tables is appropriately cautious: moving contact origins and tangent frames produce additional support-velocity terms and are not claimed to leave the anchored information matrix unchanged. This substantially resolves C20-M2, provided the main statistical theorem continues to be advertised as an anchored submodel theorem rather than a generic-table theorem.

### 3.3 The abstract-to-billiard statistical transfer is now quantitative

The new fixed-window reduction gives an explicit support remainder

`r_n = delta_n^2 + delta_n/j_n`

and an `O(delta_n)` regular-amplitude remainder. The general hypersurface Hellinger estimate

`H^2 <= C { epsilon^2 log(e/epsilon) + eta^2 }`

then yields a one-record exact-to-ideal error which is negligible after

`k_n delta_n^2 log(1/delta_n) -> 1`.

The two elementary cases `j_n^{-1} <= delta_n` and `j_n^{-1} > delta_n` are enough to check the support term. This is a real theorem-level improvement over the previous phrase that a likelihood proof was simply “uniform” under perturbation.

### 3.4 The finite-design argument is now tangent-level

The v20 report objected that nonlinear injectivity was being used where derivative injectivity was required. V21 now isolates a finite signed-jet forward map, observes the explicitly invertible leading curvature block, and writes the higher derivative as a block lower-triangular matrix whose new diagonal block is `M_n`. If the determinant-one block formula is valid, the finite-jet differential is indeed an isomorphism. The positive finite design then follows by a standard compactness argument on the unit sphere.

This is the correct structure. The remaining objection is no longer “you appealed to nonlinear rigidity.” It is whether the all-order block formula and its differentiability prerequisites have been proved with the depth required for the role they play.

### 3.5 The endpoint-output versus complete-information distinction is much better

V21 explicitly says that the Gaussian information matrix characterizes the endpoint-output coarsening, not the efficiency of all procedures based on the richer stopped transcript. It also acknowledges that waiting counts may carry additional information through the hyperbolic success exponent. This is an important correction and should be retained.

## 4. Major blocker C21-M1: the all-order signed-jet proof is still too compressed at its hardest point

The signed-endpoint inverse is the most interesting part of the manuscript. I therefore audited the displayed block rather than assuming it was wrong because the result is strong.

The historical half-line formula gives the linear orbit

`x_i^(b)(u) = (sigma_i^(b)/sigma_0^(b)) e^{-i gamma} u + O(u^2 rho^i)`.

With the v21 notation this becomes

- `e^{-i gamma} u` at even sites;
- `rfrak_b e^{-i gamma} u` at odd sites.

If one accepts the envelope reduction, the contribution of the `n`th jet of the starting contact is one copy at the boundary site plus two copies at every interior site of the same type:

`1 + 2 sum_{k>=1} e^{-2 n gamma k} = coth(n gamma)`.

The opposite contact contributes

`2 rfrak_b^n sum_{k>=0} e^{-n gamma(2k+1)}
 = rfrak_b^n csch(n gamma)`.

Since `rfrak_0 rfrak_1 = 1`, the displayed determinant is indeed

`coth^2(n gamma) - csch^2(n gamma) = 1`.

So I do **not** report an algebraic contradiction in `M_n`. The problem is proof closure around this calculation.

### 4.1 The derivative-order bookkeeping in the stationary equations is not written correctly enough

The proof of the stationary-sequence proposition says, in effect, that after differentiating the stationarity equations `k` times in the endpoint variable, the remaining terms contain local graph derivatives of order at most `k`.

But the stationarity equations themselves contain first derivatives of flight lengths, and the flight lengths depend on the boundary graphs. A naive Faà di Bruno count produces one additional derivative of the graph at the equation level. The desired final statement that the **action jet** `S_b^(n)(0)` depends only on graph jets through order `n` can still be true -- and the envelope principle is exactly the mechanism that can remove the apparent derivative shift -- but the manuscript must prove that bookkeeping, not slide over it.

At a minimum the author should write a precise induction distinguishing:

- endpoint derivatives of the stationary orbit;
- derivatives of the stationarity operator;
- derivatives of the stationary action;
- the first variation with respect to a graph-jet coordinate;
- the degree in `u` of each term.

Without that separation, the sentence “all remaining terms contain only ... graph derivatives of order at most `k`” is too strong as printed and does not by itself justify the arbitrary-order triangular dependence.

### 4.2 Uniform invertibility along the nonlinear half-line needs an actual weighted-operator estimate

At the base orbit the Jacobi inverse is explicit and bounded on the weighted space. The proof then says that after shrinking the common box, the operator obtained by linearizing along the nonlinear stationary orbit retains a uniform inverse bound.

This is plausible, but for the all-order theorem it should be a lemma with a norm estimate. One needs to show that the nonlinear Hessian perturbation is small in the operator norm appropriate to `X_rho`, not merely quote positivity or the base Green function. The weighted Banach-space estimate is what justifies repeated implicit differentiation with constants controlled on compact finite-jet sets.

A top-four proof should state something of the form

`|| H_b(u,q) - H_b(0,q_2) ||_{X_rho -> X_rho} <= C |u|`

(or the correct variant) and then apply a Neumann-series or quantitative implicit-function argument. At present the proof gives the right picture but not enough of the operator mechanics.

### 4.3 Differentiating the infinite stationary action and the envelope identity needs a full tail argument

The manuscript states that the differentiated action sums are absolutely convergent by weighted bounds and that the tail boundary term tends to zero. For a first derivative this is believable. The theorem, however, uses arbitrary fixed endpoint order and graph-jet variations, and the key conclusion is that orbit variation makes no degree-`n` contribution.

The paper should prove uniform summability after the relevant mixed derivatives, identify the finite-truncation boundary term, and show that it tends to zero in the same topology used for the jet calculation. This is especially important because the claimed all-order formula is supposed to be reusable independently of the inverse conclusion.

### 4.4 The highest-degree isolation deserves a precise homogeneous expansion

The proof says that differentiating a flight length with respect to an `n`th graph jet has leading homogeneous term `y^n/n!` or `z^n/n!`, that the linear orbit depends only on the quadratic geometry, and that nonlinear orbit terms cannot change the degree-`n` coefficient.

This is probably the right mechanism, but it should be written as an explicit homogeneous expansion with an error of degree at least `n+1`, including the effect of the factor “horizontal separation divided by flight length.” The signs and contact labels should be fixed once. The statement that lower nonlinear orbit terms “cannot change that degree” should be a lemma or a displayed degree count, not a sentence carrying the entire arbitrary-order induction.

### 4.5 Why this remains a major blocker

If the paper only claimed a third- or fourth-order reconstruction, the above could be treated as a request for exposition. The paper instead claims **every finite jet at arbitrary order**, uses that claim to prove tangent injectivity in every finite jet model, and then feeds that tangent injectivity into the positive-definite statistical design theorem. The all-order calculus is therefore a load-bearing theorem, not an appendix detail.

I am not saying the formula is false. I am saying the proof is still below the completeness standard appropriate to the strength and centrality of the claim.

### Required repair for C21-M1

Promote the all-order stationary calculus into a genuinely self-contained theorem package. It should include:

1. a quantitative weighted implicit-function theorem for the nonlinear half-line stationarity operator;
2. the exact derivative-order induction in endpoint and graph variables;
3. uniform summability of the differentiated stationary action;
4. a finite-truncation proof of the envelope identity and tail cancellation;
5. a homogeneous-degree lemma isolating the first appearance of `q_{b,n}`;
6. the two geometric sums with all multiplicities and signs;
7. quantitative smoothness and lower-singular-value bounds for the finite-jet forward map on compact positive sets.

This would strengthen, not weaken, the paper.

## 5. Major blocker C21-M2: the same-type statistical theorem is missing the necessary flight-parity hypothesis

This is the clearest concrete theorem-statement defect I found in v21.

The signed-rigidity section correctly says that for a same-type endpoint experiment one uses an **even number of flights** with first and last impacts of type `b`. The historical relative law is also parity dependent: if `p = j mod 2`, the limiting action is

`S_0(u) + S_p(v)`

in the chosen orientation.

The v21 physical statistical section nevertheless fixes same-type designs `(b,d)` and uses the defining function

`w_{b,d}(u,v) = d - S_b(u) - S_b(v)`,

then introduces only the condition

`j_n -> infinity`.

No condition `j_n in 2N` (or the equivalent parity requirement for the chosen orientation) is printed in the fixed-window reduction, the batch-rate assumptions, or the final endpoint Gaussian theorem.

For an odd number of alternating flights, the terminal contact type is not the same as the initial type. Then the limiting endpoint action is mixed, and the same-type formulas for `w_{b,d}`, the support velocity, and `K_{b,d}` are not the experiment described by the itinerary.

This is easy to repair, but it is not optional. A theorem about a physical billiard experiment must specify an itinerary that actually produces the observation law being analyzed.

### Required repair for C21-M2

Either:

- impose `j_n` even throughout the same-type physical theorem; or
- formulate the statistical theorem with an explicit terminal parity `p_n=j_n mod 2` and use the mixed actions/amplitudes/information matrices appropriate to that parity.

The first route is much cleaner and is fully compatible with the present signed-rigidity design.

The author should also check every use of `k_n tau^{j_n}` and every success-probability asymptotic after the parity convention is fixed, although no difficulty is apparent there.

## 6. Major blocker C21-M3: the deterministic-cap construction has an unresolved order-of-quantifiers issue

The physical theorem wants one sequence of capped experiments which is locally valid uniformly on compact parameter sets. The text says, however, that the deterministic cap `N_{n,l}` is chosen so that

`inf_{z in K} N_{n,l} p^partial_{n,l}(z) >= 2 k_{n,l}`

for a compact set `K`. The resulting cap-failure probability is then exponentially small uniformly on `K`.

This is fine **for a fixed K-dependent experiment**. The subsequent theorem is phrased as a single capped endpoint-output experiment which is uniformly valid on every compact local set, and the minimax discussion ultimately considers larger and larger local balls. Those are different quantifiers.

I believe the intended repair is straightforward. Because `j_n delta_n -> 0`, the local success probabilities should be uniformly comparable to the reference success probability on every fixed compact set. The author can therefore choose one reference-based cap, for example with a fixed safety factor relative to `p_{n,l}(0)`, and prove that for each fixed compact `K` the inequality above holds for all sufficiently large `n`. Then the cap sequence is independent of `K` and the compact-uniform theorem has the correct logical form.

But this should be done explicitly. The current phrasing allows the experiment itself to change when the compact set in the theorem changes.

### Required repair for C21-M3

Print the cap sequence before quantifying over compact local sets, and prove a statement of the form

`for every fixed compact K, for all large n,
 inf_{z in K} N_{n,l} p_{n,l}(z) >= c k_{n,l}`

with the same `N_{n,l}` for all `K`. Then restate the uniform theorem and local minimax conclusion with the corrected quantifier order.

## 7. Major scope issue C21-M4: “complete stopped transcript” is complete only after a nontrivial per-preparation coarsening

The historical transfer theorem `v6/10_experiment_transfer.tex` is admirably explicit on this point. Its per-preparation law retains the selected endpoint/residual-time record plus a failure atom, and it says that this is **a coarsening of a raw physical record**. It later emphasizes that the full growing collision array lies on an embedded surface and that no total-variation comparison of distinct full arrays is asserted.

The adaptive theorem then builds a stopped transcript from those per-preparation kernels. Within that model, it retains every design, every success or failure record, and the stopping time. That is a legitimate “complete stopped transcript” **of the coarsened endpoint-record experiment**.

V21 sometimes uses language such as “complete actual finite-bridge stopped transcript” and “raw endpoint records.” A careful reader can reconstruct the intended meaning, but the headline phrase is stronger than the underlying comparison if it is read as the complete collision history of every attempted bridge.

This matters because the paper also emphasizes “physical information.” A full collision array may carry information that has been discarded before the v6 comparison even starts, just as waiting counts may carry information discarded by the later endpoint-output coarsening.

### Required repair for C21-M4

Choose unambiguous terminology, for example:

- “complete stopped transcript of the endpoint/residual-time coarsened preparation experiment”; or
- “complete stopped acquisition transcript at the declared record level.”

Then define the record space once in the main theorem. Do not call the v16/v21 comparison a total-variation theorem for the full raw collision array unless such a theorem is actually proved.

This is partly a terminology issue, but at the requested venue it is also a theorem-scope issue: the statistical experiment is the mathematical object, and changing its sigma-field changes the meaning of an information statement.

## 8. The non-dominated Gaussian theorem is now plausible, but its Le Cam claims should be sharpened

I regard the v21 statistical reconstruction as a major improvement, not a remaining fatal error. Still, several statements should be tightened before publication.

### 8.1 Distinguish three levels of convergence

The manuscript uses all of the following ideas:

- a uniform LAN expansion for the dominated representative;
- asymptotic equivalence between original and censored experiments on compact local sets;
- convergence of fixed finite subexperiments to a Gaussian shift;
- compact-local estimator convergence;
- a local asymptotic minimax lower bound over Euclidean balls.

These statements are related but not identical. The proof currently moves between them very quickly. The author should cite or state one precise LAN-to-limit-experiment theorem with the exact uniformity assumptions being used, and then separately invoke the appropriate local asymptotic minimax theorem.

In particular, “every fixed finite local subexperiment converges in Le Cam distance” is not literally the same statement as convergence of the entire continuum-indexed compact experiment. The latter may be available from the compact-uniform likelihood expansion, but then it should be stated and proved at that level rather than inferred by wording.

### 8.2 Singular information matrices should be formulated on the identifiable quotient

The abstract theorem allows `J_Sigma` to be singular and then writes a Gaussian shift with the “usual interpretation on the range.” This is understandable but too informal for a theorem which otherwise emphasizes exact experiment structure. State the identifiable subspace or quotient explicitly, and formulate testing and minimax conclusions there. The physical finite-design theorem later obtains positive definiteness, so this issue is mainly one of abstract theorem precision.

### 8.3 The local estimator is a reference-model statistic

The central-sequence estimator uses the score and information matrix at the reference geometry. This is standard in a local experiment, but the introduction should keep it clearly distinct from a globally implementable estimator with unknown reference geometry. The paper is already mostly disciplined about this point; one sentence in the theorem statement would remove possible overinterpretation.

These are not reasons, by themselves, to reject a repaired manuscript. They are part of what is needed to make the statistical component top-journal clean.

## 9. Anchored realization is a legitimate submodel, but it should not be rhetorically inflated into generic-table inference

The anchored-realization proposition is a good addition. It makes clear that finite labelled jets can be varied independently by actual smooth local billiard perturbations while preserving the channel.

The resulting statistical theorem, however, remains a theorem for a specially registered finite-dimensional local family. It is **not** a theorem saying that an arbitrary nearby billiard table can be observed in a common contact frame for free. V21 itself now acknowledges this and writes the first-order frame-motion term for generic families.

That discipline should be maintained everywhere, especially in the abstract, title discussion, and significance claims. Phrases such as “unknown contact geometry at rate delta_n” should be read as “unknown coordinates in the chosen finite-dimensional anchored contact-jet model.” If the author wants a theorem for generic nearby tables, the nuisance registration directions and their information geometry must be included in the theorem, not only mentioned in a final subsection.

The charged-registration-pilot criterion is a useful observation, but at present it is only a scale criterion, not a full generic-table equivalence theorem.

## 10. Statistical resource accounting is honest, but the current minimax result is not a full physical efficiency theorem

V21 deserves credit for explicitly charging failed preparations and for refusing to call waiting counts ancillary. This is important because the success probability contains the exponentially sensitive long-bridge factor.

But this honesty also reveals the limited scope of the current Gaussian minimax theorem. The local rate

`delta_n` for anchored shape and `delta_n/j_n` for gap

is a rate in the number of **successful endpoint records** at the chosen critical moving-support scale. The expected number of raw preparations is exponentially larger in `j_n`, and the complete stopped experiment may contain a different, possibly faster, information channel in the waiting counts.

There is nothing mathematically wrong with analyzing the endpoint-output coarsening. But at top-four level, the paper should not let the phrase “physical information” suggest that the complete resource-constrained physical experiment has been asymptotically characterized. The most interesting future theorem may in fact be the joint multiscale limit experiment for

`(waiting counts, endpoint marks)`

under an explicit raw-preparation budget.

Such a theorem could materially strengthen the paper's conceptual significance.

## 11. Top-four significance assessment

Even assuming all correctness issues are fixed, I am not yet persuaded that the current theorem architecture is strong enough for the four journals named in the review request.

### 11.1 What is genuinely interesting

The most attractive deterministic mechanism is the signed endpoint support recovering the unsymmetrized half-line actions, followed by an all-order triangular jet reconstruction with determinant-one diagonal blocks. I did not find an obvious direct duplicate of this mechanism in the literature I checked.

The coupling of that inverse theorem to the same boundary law that governs a nonregular endpoint experiment is also conceptually appealing. The paper is strongest when it shows that one nonlinear boundary structure simultaneously controls:

1. the relative long-bridge asymptotic;
2. local labelled geometric reconstruction;
3. the singular information geometry of endpoint observations.

That is a coherent theme.

### 11.2 Why the present consequence still feels too local for the requested venue class

The deterministic inverse uses a continuum of signed endpoint-support data from a single selected labelled channel and concludes local recovery of the two participating contact germs. It does not assemble channels into a table-level rigidity theorem.

By contrast, current marked/enriched-length rigidity results in the area obtain global geometric conclusions from global orbit data under their respective assumptions. These are not directly comparable information sets: the present endpoint law is locally richer in collision coordinates, while marked-length data are globally organized and spectrally natural. I therefore do not claim that those theorems subsume the present one.

But the comparison matters editorially. A top-four paper normally needs either a theorem of comparable geometric reach, or a new mechanism whose conceptual consequences clearly reorganize the subject. At present the determinant-one local inverse is elegant, but the manuscript does not yet extract a multi-channel/global rigidity consequence from it.

### 11.3 The statistical component is not, by itself, the top-four significance engine

Moving-support experiments, nonregular endpoint rates, Le Cam comparison, Gaussian local experiments, and local minimax theory have substantial classical antecedents. V21 appropriately does not claim otherwise. The novel part is the billiard-specific support velocity/information matrix and its coupling to the geometric inverse.

That is useful, but because the analyzed physical output is deliberately coarsened and locally registered, I do not think the statistics alone raises the manuscript to the requested venue class.

### 11.4 What would materially strengthen the top-four case

Any one of the following could change my assessment:

- a multi-channel theorem assembling signed local inverses into a global or table-level rigidity statement;
- a coordinate-free version of the local inverse with an intrinsic geometric interpretation of the odd jets;
- a joint limit experiment for the complete declared physical transcript, including waiting-time information and an explicit raw-cost normalization;
- a universality theorem showing that the boundary-law / determinant-one inverse mechanism applies to a significantly broader class of hyperbolic scattering systems;
- a genuinely new global consequence for marked/enriched orbit data derived from the local boundary law.

I would not demand all of these. I do think the present paper needs at least one comparably strong conceptual payoff if the target remains Annals/Acta/Inventiones/JAMS.

## 12. Native build and submission readiness

The repository's verification record is appropriately cautious. I checked the exact canonical manuscript-source commit `672b159ef204ba75a63ab92a4d52ae3960304337`.

The workflow **“A2 v21 complete native build”** exists and a run was created for that exact source. Its conclusion is `failure`, but the recorded job executed no runner steps. The rerun has the same zero-step failure mode. There is therefore:

- no evidence from this workflow of a LaTeX compilation error;
- no evidence that checkout, dependency installation, LaTeX, bibliography, diagnostics, or artifact upload actually ran;
- no successful native-build certificate for the canonical source.

The two later commits on the revision branch add only the root-level manifest and verification record and do not modify the manuscript source. They have no workflow run of their own, which is mathematically irrelevant but confirms that the canonical source run is the only build evidence to assess.

Before any real submission, the exact canonical source should be built in a runner that actually executes. Cross-references, bibliography, labels, warnings and the final PDF should be checked from one frozen submission tree.

The persistent directory name `A2-v17-boundary-information-coarsening` is also unnecessary source-version friction for a v21 submission. Historical provenance can remain in the repository while the submission itself is frozen into one canonical directory or release artifact.

## 13. Status of the v20 blockers after v21

My assessment is:

| Previous issue | V21 status | Referee assessment |
|---|---|---|
| R20-1 non-dominated vector likelihood | **substantially repaired** | common-collar dominated representative and explicit Le Cam comparison are the right fix |
| R20-2 common physical coordinates | **repaired for the anchored submodel** | fixed laboratory chart and parameter-independent endpoint map are now explicit; generic tables remain outside the theorem |
| R20-3 quantitative abstract-to-billiard transfer | **substantially repaired** | explicit support/amplitude remainders and Hellinger product control are now present |
| R20-4 tangent-level finite design | **repaired in structure** | depends on the all-order tangent map, whose proof still needs expansion |
| R20-5 standalone all-order signed-jet proof | **improved but not closed at top-four proof standard** | displayed block checks out algebraically, but the infinite-dimensional/high-order proof remains too compressed |
| R20-6 endpoint-output vs richer transcript | **substantially repaired** | efficiency claim is correctly limited; observation-level terminology still needs tightening |
| R20-7 successful canonical build | **unresolved** | workflow never executed a runner step |

This table is important. V21 should not be judged as though the author ignored the previous report. The remaining rejection is based on the new state of the manuscript.

## 14. New required repairs before another top-four review

### R21-1. Fully close the all-order signed-jet calculus

Provide a self-contained weighted-operator and high-order differentiation proof, including exact derivative-order bookkeeping, uniform inversion, differentiated infinite-action convergence, the envelope limit, and homogeneous-degree isolation.

### R21-2. Fix the physical itinerary/parity in the statistical theorem

Impose even `j_n` for same-type endpoint designs, or rewrite the theorem with terminal parity and mixed actions. Audit all formulas after the choice is made.

### R21-3. Fix the cap quantifiers

Choose one cap sequence independent of the compact local set and prove eventual compact-uniform adequacy, or explicitly state that the experiments are `K`-dependent and modify every subsequent limit accordingly. The former is preferable.

### R21-4. Define the observation sigma-field exactly at every transfer step

Distinguish the full raw collision history, the endpoint/residual-time per-preparation coarsening, the stopped transcript built from that coarsening, and the final endpoint-output experiment. Do not use “complete raw transcript” across these different levels.

### R21-5. State the precise Le Cam/LAN/minimax theorem being invoked

Separate dominated uniform LAN, asymptotic equivalence, compact experiment convergence, finite-subexperiment convergence, contiguity and local asymptotic minimax. Formulate singular information on the identifiable subspace.

### R21-6. Strengthen the conceptual consequence if the target remains top-four

The mathematics may become publishable without this item at a strong specialist journal, but the requested venue class needs a more compelling structural consequence: global/multi-channel rigidity, coordinate-free geometry, a complete physical limit experiment, or a broader universality theorem.

### R21-7. Produce a real canonical build

Run the exact frozen manuscript source through a functioning runner and archive the successful PDF/build diagnostics. A zero-step workflow failure is neither a pass nor a manuscript failure.

## 15. Smaller mathematical and presentation comments

1. State the parity convention near the first definition of a `bb` design, not only deep in the inverse section.
2. In the abstract non-dominated theorem, define the Hellinger convention used. Constants are immaterial asymptotically, but a fixed convention avoids ambiguity in product bounds.
3. When saying the censored family is dominated by the null censored law, explicitly note that the null `partial` atom has positive mass; this is true because the null collar mass is positive.
4. The reverse kernel in the censoring comparison is parameter independent; it would help to say this explicitly because that is what makes it a valid deficiency bound.
5. The sentence claiming compact-uniform contiguity from “the same argument applied to bounded local sequences” is too short. State the precise lemma.
6. If `J_Sigma` is singular, replace informal inverse-square-root notation by a projection/pseudoinverse formulation.
7. In the Hellinger stability lemma, state whether the support functions have been normalized by a common positive factor or whether the constant is invariant under such changes; the information matrix already has the correct invariance.
8. In the fixed-window reduction, identify explicitly which derivatives are taken at fixed laboratory time and which historical `S_b` derivatives were constructed in channel-centered coordinates. The algebra in v21 appears to account for the gap derivative through the `delta_n/j_n` remainder, but the convention switch is important enough to deserve one displayed sentence.
9. The finite positive design is existential and may depend on the finite jet order `M`. The revision says this correctly. Preserve that qualification in the abstract and any future summary.
10. The finite design will generally also depend on the reference geometry. This is normal for a local experiment, but should be stated if an implementation interpretation is offered.
11. The endpoint-output central-sequence estimator is a local reference-model estimator. Avoid presenting it as an adaptive global reconstruction algorithm.
12. The anchored-realization proof should state exactly how `u_*` is chosen relative to the region on which the bump cutoff equals one, so that the printed graph family is literally of the displayed form on the whole statistical patch.
13. The gap variation by a cut-off normal displacement is harmless for a local smooth family, but if the two selected patches lie on the same connected obstacle, say explicitly that global embeddedness is preserved after shrinking the parameter ball. The present clearance argument strongly suggests this.
14. For the analytic continuation conclusion, distinguish equality of parametrized graph germs, equality of boundary images in the registered frame, and global obstacle identification. The current theorem says “boundary images,” which is safer than claiming a global parametrization; keep it that way.
15. The phrase “physical onset determines the gap” is deterministic. In statistical statements keep onset estimation cost separate, as v21 mostly does.
16. The pilot-centered equivalence is correctly restricted to the post-pilot endpoint-output sigma-field. This restriction should not be dropped in summaries.
17. The complete stopped transcript may contain additional information even after the per-preparation endpoint coarsening because the success/failure sequence remains. The full raw collision record may contain still more. These are two different enrichments.
18. The source graph is historically rich but editorially difficult. A journal referee should not need response letters and version manifests to identify the active theorem. Freeze a clean source tree for the next review.
19. The acknowledgement of AI-assisted independent memoranda is transparent. Keep it factual and separate from mathematical authority.
20. A shorter proof dependency map inside the manuscript would help. The present article spans many retained historical modules whose version names obscure which results are logically essential.

## 16. Final editorial assessment

V21 is the first version in this sequence for which I would say that the central non-dominated statistical architecture is **conceptually credible**. The v20 Radon--Nikodym defect has been addressed in the right way; the laboratory-coordinate problem has been resolved by choosing a genuine anchored physical submodel; the exact-to-ideal comparison is quantitative; the finite-design argument is now tangent-level; and the manuscript is appropriately cautious about endpoint-output efficiency versus richer transcripts.

The signed determinant-one mechanism also survives a direct sanity check: the linear orbit and the displayed geometric sums are mutually consistent, and I found no elementary sign or determinant contradiction.

That makes the remaining problems more, not less, important. The all-order signed-jet theorem is now the mathematical centerpiece and must be proved with full high-order weighted-operator bookkeeping. The physical statistical theorem must specify the correct itinerary parity. The cap sequence must have the correct order of quantifiers. The observation sigma-fields must be named exactly. And after those repairs, the paper still needs a stronger argument for why this local one-channel/endpoint-output package belongs in the very small class of papers accepted by Annals, Acta, Inventiones or JAMS.

Accordingly I recommend **rejection in the present form at the requested top-four level**, with the explicit qualification that this is not a dismissal of the program. A version that (i) fully closes the all-order proof, (ii) repairs the theorem-level statistical formulation, (iii) freezes a verified canonical build, and (iv) extracts a substantially broader geometric or complete-experiment consequence would be different enough that I would regard a fresh review as mathematically justified.