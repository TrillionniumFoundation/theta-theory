# Referee report on A1 English v22

**Manuscript:** *Attainable information geometry in positive experiments*, Qian Qi.  
**Date of assessment:** 7 September 2026.  
**Examined revision:** `revision/a1-english-v22-prior-uniform-algebra-2026-09-07`.  
**Immutable submission:** `5f745a863dac637496bd5eb20341f12cecb71ab1`, `papers/A1-english-v22/`.  
**Previous manuscript:** `7c44bdccc91667c583b5d5cbcff3f8d9160a57d6`.  
**Controlling previous report:** `36910a7c6fd08e5ad2e8e10db7c2d8c71c463de8`, `reviews/a1-english-v21-independent-2026-09-07/REFEREE_REPORT.md`.

This is an owner-requested, AI-assisted technical referee-style assessment, using the requested Annals/Inventiones/JAMS/Acta level of scrutiny. It is not a report commissioned by any of those journals. Independent calculations below mean calculations performed in this review without importing the author's test implementation, not a claim of institutional affiliation or a formal verification certificate.

## 1. Recommendation and its precise meaning

**Recommendation: reject in its present form at the requested four-journal standard.** The principal grounds are the demonstrated significance and the presentation of the contribution, not a discovered contradiction in the central theorems.

The revision makes a genuine mathematical advance over v21: it supplies a second complete multistep classification, with constants uniform over all priors in the stated bounded observation-algebra class. I do not regard this addition as a renamed one-step theorem, an assumption of the desired conclusion, or an iteration that ignores accumulated coding error. The product chart, unconditional acquisition argument and raw-state update together supply the necessary additional reasoning.

I found **no fatal mathematical counterexample in the routes audited here**. In particular, I found no justification for rejecting the new theorem on the grounds of a missing covariance inverse, loss of full support, omitted word probability, or a non-associative redundant coefficient representation. Those would be inaccurate objections to the actual text. Conversely, neither this finding nor successful diagnostics certifies all 129 formal statements in the 120-page article.

My negative editorial judgment is narrower than a claim that the exact results are already in the literature. The manuscript's strongest candidate for a major contribution remains the collision-uniform monomial classification with the acquired-dimensional truncation. The new algebra result is a useful, apparently sound extension of the affine law, but it occupies the saturated finite-observable case, where the covering step reduces to elementary ellipsoid quantization. Its proof does not by itself establish a new general geometric theory of multistep experiments. The manuscript needs a much more discriminating account of what has been proved beyond existing quantization and approximation mechanisms, and why the particular classification has significance commensurate with the requested venue. I have not conducted an exhaustive priority search and do not assert that another paper contains this exact pair of classification laws.

The report therefore separates four categories throughout: corrections already made; mathematical arguments that survived scrutiny; a concrete simplification of the new argument; and remaining editorial or expositional requests. None of the latter is relabeled as a fatal proof gap.

## 2. The submission actually reviewed and the previous objections

The assessment is pinned to the published v22 commit, rather than a moving branch name. The connected GitHub source was compared with the downloaded Actions package. The package digest matched the recorded artifact digest. Four independently recomputed Git blob hashes, including the active main file, the complete new algebra section and the source manifest, matched the pinned repository. All **763** entries of that manifest were checked independently with no mismatch.

An independent recursive expansion of the active TeX input routes, followed by full-block multiset comparison, found 122 theorem/lemma/proposition/corollary statements in v21 and 129 in v22. All 122 inherited statements are unchanged. Of 120 inherited proofs, 118 are unchanged; all 120 match after the two explicitly registered citation-only substitutions. The active v22 route contains 127 proof blocks. These are preservation facts, not measures of mathematical quality.

The disposition of the previous report is as follows.

| Previous item | Finding in the actual v22 reading route | Disposition |
|---|---|---|
| E21.1: missing early setup symbols | `sections/introduction.tex` now defines the interval, largest one-step exponent, distinct sumsets, their cardinalities and the zero-step convention before the inherited results use them. | Corrected. |
| E21.2: consequence proofs routed through the alternative appendix | `cor:intrinsic-bits` and `thm:collision-tree` now cite `thm:resolution-main`; the two substitutions agree with `REVISION_EDITS_V22.json`. | Corrected. |
| E21.3: Terao proceedings metadata | The active `references-v22.tex` gives the 20th SWAT, volume 370, article 39. The publisher record confirms the correction [P5]. | Corrected. |
| E21.4: no demonstrated second multistep application | `sections/algebra_multistep.tex` proves a new experiment-level theorem rather than simply restating the transfer hypotheses. | Mathematical response supplied and substantively addressed; journal significance remains an editorial assessment. |

It would be unfair to repeat E21.4 as though v22 contained no second application. It would be equally inappropriate to treat supplying that application as a proof of a favorable publication decision. The author's response itself makes this distinction, and the present report preserves it.

## 3. Audit of the inherited principal route

The principal route was examined at the level of its decisive mechanisms: the physical prediction resource; exact information and the binomial tangent; strict mixed-moment positivity; the acquired collision flags; whole-image covering inputs; the causal transfer theorem; and the monomial verification of its hypotheses. The principal exact-kernel argument and the affine thick-linear comparison were also checked. This is not a claim of a fresh line-by-line audit of every companion appendix or of the complete historical research program.

### 3.1 What the resource actually is

`build/operational_model.tex`, `def:finite-state`, charges the persistent index and disallows an external past-history tape. Current commands and reports are inputs; stage-dependent read-only calibration and transition functions are permitted. The query is revealed only after retention. The loss is the squared excess prediction loss for the physical menu, not Euclidean loss after an inverse-covariance whitening. These choices are mathematically coherent. They are not bounds on total arithmetic workspace, execution time or an unbounded-horizon algorithm.

The distinction between checkpoint encoders and a single causal filter is essential. The latter cannot be justified by repeatedly applying an optimal checkpoint encoder to an unavailable exact history. The inspected transfer proof instead updates a retained reachable representative and requantizes, which is the appropriate construction.

### 3.2 Exact rank and the source of acquired dimension

In `core/03_transversality.tex`, `lem:mixed-moment`, the determinant integral has a nonnegative integrand; ordered interior subintervals have positive mass under a full-support prior. This supplies strict positivity without assuming a prior density.

At the binomial tuple in `lem:binomial-tangent`, the polynomials obtained by omitting one factor are independent by evaluation at the distinct negative reciprocal roots. The tangent exponents listed in that lemma are genuinely distinct: the interior exponent offsets lie strictly between 0 and the largest one-step exponent. Consequently the tangent has dimension `n(r-1)+1`. The product itself lies in it. The normalized derivative removes exactly the one-dimensional direction of that product, rather than an unspecified amount of rank. This justifies the acquired-dimensional cap in the exact law.

These facts matter to the finite-resolution theorem. Replacing the attainable image by its affine hull, or counting formal future coordinates without an acquisition cap, would give an incorrect proof strategy. I did not find that substitution in the present principal route.

### 3.3 Collisions and uniformity

The important claim is uniformity through additive collisions on the specified compact one-step chamber, with the full-support prior fixed. It is not uniformity over all priors in the monomial class.

The Leja/Newton organization in `build/collision_flags.tex` uses complete prefixes. Its bounded triangular comparison and the extension of divided differences through confluence avoid using reciprocal collision gaps as update constants. The acquired-flag argument requires the complete confluent family; a collection of isolated high derivatives would not suffice. The normalization/rank calculation and compactness are used for the required prefix, and the actual exploration argument integrates complementary command neighborhoods rather than assigning mass to one frozen slice.

The whole-image argument is also distinct from this local acquisition argument. For each fixed calibration, the moment map is rational in the command coordinates with positive evidence denominator. Its integral coefficients need not be algebraic functions of the calibration parameter for bounded-format semialgebraic estimates in the command variables to apply. The relevant classical component/variation inputs are identified in the text; the accessible primary sources support the real covering ingredients [P1, P2]. I did not find a basis for a coefficient-algebraicity objection.

### 3.4 Causal transfer and exact kernels

The transfer hypotheses separate whole-image geometry, mass under one actual exploration law, and reachable-state Lipschitz updates. The lower argument applies to fixed codebook randomness and can then be averaged; it does not permit the exploration distribution to change after selecting a difficult checkpoint. The upper argument uses the recurrence `e_n <= L e_(n-1) + delta_n`, with stage-specific codebooks. Positive evidence and multiplication of remaining tests supply the raw update in the monomial application. No discarded command history is required.

For the principal exact-kernel route in `sections/kernel_feasibility.tex` and `sections/exact_kernels.tex`, I checked the separation-based full-support feasibility step, the local constrained moment chart, and the use of the maximal nonzero minor of the quotient multiplication pencil. The latter is essential: a vanishing common intersection of moving kernels would not prove the existence of one zero kernel. The local positive-density perturbation argument and the polynomial-grid witness retain the annihilation equations and address exact kernel realization, not merely containment. The text explicitly treats the zero-rank and zero-chart-dimension cases. I found no reason to resurrect a containment-versus-exactness objection to this version.

## 4. The new algebra theorem: detailed assessment

All locators in this section refer to `papers/A1-english-v22/sections/algebra_multistep.tex` at the pinned commit. Its complete 437-line argument was examined.

### 4.1 Hypotheses and quantifiers

Lines 11–38 assume bounded continuous generators, specified bounded multiplication coefficients, a fixed command cube, a fixed finite horizon and a prior known during each run. The constants may depend on `d, B, delta, N`, but not on the particular prior or positive covariance eigenvalues. Redundancy, support loss and covariance rank loss are explicitly allowed. These are strong hypotheses, but they are printed hypotheses rather than omissions.

Lines 40–55 construct the actual delayed query menu. With `s=N-n`, its probabilities are `2^(-s)` and `2^(-s)(1+delta f_i)`. Thus the squared physical prediction distance between two raw means is exactly

`2^(-2s) delta^2 /(d+1) * ||v-w||^2`.

The covariance eigenvalues, not their square roots, are the semiaxes of the reachable raw-mean variation. This distinction is preserved in the statement and examples.

### 4.2 Every history, including redundant presentations

`lem:algebra-product-chart`, lines 120–163, represents the unscaled likelihood product by `a_n+b_n^t f`. A fixed left-to-right coefficient multiplication rule is sufficient. It need not be associative as a rule on redundant coefficients, since its evaluation is the associative pointwise product. The exact identity coefficient also makes zero later commands harmless.

The integration identity

`v_n = m + Sigma b_n / (a_n+b_n^t m)`

is correct. The bounded bilinear coefficient rule and the evidence bounds give a uniform radius for `theta_n=b_n/Z_n`. These controls are before any diagonalization and do not use a lower covariance eigenvalue. They concern the complete reachable set, not just a regular patch. This is the right starting point for prior-uniformity.

### 4.3 Actual mass, not a conditional or zero-measure substitute

`lem:algebra-acquired-density`, lines 169–233, is the decisive additional step. On the all-positive word, with the first command `z` and later commands `w`, the coefficient coordinate at `w=0` is exactly `z/(1+m^t z)`. Its derivative at the origin is the identity. The bounded multiplication coefficients and positive evidence give the uniform derivative control used in the inverse argument.

The proof integrates over a positive-volume set of complementary commands. Its lower density includes `(2 delta)^(-nd) 2^(-n) Z_n`, the unconditional command-and-word density. It therefore does not replace a rare selected word by a probability-one event, and it does not assign positive mass to the slice `w=0`. The zero-dimensional complementary volume convention handles `n=1`. The constants may deteriorate with the fixed horizon; the theorem does not claim otherwise.

Singular `Sigma` causes no difficulty here: `theta_n` is a geometric history coordinate, not an additional retained state or a uniquely identifiable coordinate of the raw mean. Rotating its ball and projecting before multiplying by the positive eigenvalues gives the required prefix mass at each nonzero rank.

### 4.4 Causality and the choice of metric

`lem:algebra-update`, lines 235–259, gives the Bayes quotient in raw moments. On a segment between posterior moment states the evidence denominator is at least `3/4`; the numerator and its derivatives are controlled by the fixed coefficient bounds. The update is therefore uniformly Lipschitz in the physical raw-mean metric, even when covariance is singular.

A codebook representative is itself reachable. Extending a realizing history by the current allowed command and report proves that its updated representative remains reachable. This is stronger than merely having a Lipschitz map on a formal coordinate box and is exactly what the causal construction needs. The proof in lines 261–302 uses the physical query map, orthogonal diagonalization and the previously established acquisition mass consistently.

### 4.5 Quotients, attenuation and inverse curves

`prop:finite-observable-quotient`, lines 308–339, is correct and important. Polynomial annihilation makes each generator finite-valued; separating products yield the indicators of the joint-value fibers. Hence `W` is all functions on a finite clopen partition, with at most `d+1` parts. The author explicitly discloses this. The qualitative indicator construction can have ill-conditioned coefficients, but these are not used in the quantitative proof. It would be wrong to insert those denominators into the theorem's uniform constants.

`cor:algebra-attenuation`, lines 341–396, correctly distinguishes the exact all-prior covariance formula from the attenuation-only comparison requiring positive lower bounds on all prior weights, including the residual atom. In the two-channel example, the determinant is `tau_1^2 tau_2^2 / 27`, and the two risk branches and crossover have the stated powers. As a simple independent scale check, with one feature `f=tau 1_{1}` and prior mass `p`, `Sigma=tau^2 p(1-p)`. The raw posterior variation is of this covariance order, so the squared risk has a `tau^4` factor, not `tau^2`. This supports the printed law; it is not a counterexample to it.

`cor:algebra-operational-inverse`, lines 398–429, has the required integer-budget argument. For a positive `lambda_l`, the witness `M_0=V_l/lambda_l^l` is at least one; rounding upward costs at most a factor two. If the rank is below `l`, the infimum vanishes by the large-budget decay. The claim concerns comparison up to constants from the entire infinite budget curve, not exact recovery from finitely many noisy observations. I found no inversion error under that interpretation.

## 5. A sharper explanation of what the new geometry does

The following reduction is an independent mathematical observation about the printed hypotheses, not a proposed weakening of them.

Put `k=rank(Sigma)` and `S_n={v_n(h)}`. The product chart gives

`S_n subset m + Sigma (R B_d)`.

The acquisition proof supplies every point of a fixed ball in the coefficient coordinate on an actual command patch, so also

`m + Sigma (r B_d) subset S_n`.

Consequently the dimension of the reachable raw state is **exactly `k` at every checkpoint `n>=1`**. In this class there is no further history-length-dependent acquired-dimension cap below covariance rank: the first acquisition already reaches a full relative-dimensional patch. For a fixed observable quotient, `k` is the number of its positive-mass parts minus one. Indeed, the evaluation vectors `(1,f)` on the distinct parts have independent rows because their span contains every partition indicator; a positive-weight covariance has precisely the affine dimension of those vectors. Rank drops therefore reflect support loss or a degeneration that changes the observable features, not a delayed acquisition of additional directions.

This also gives a direct proof of the covering part without semialgebraic geometry. After an orthogonal rotation, cover the containing ellipsoid by a rectangular grid. For every positive radius,

`N(S_n,epsilon) <= product_(i=1)^k (1+C_d R lambda_i/epsilon)`

`                 <= C'_d sum_(l=0)^k V_l (R/epsilon)^l`,

where `V_0=1` and dimensional constants absorb the rectangular grid's Euclidean diameter. Empty cells can be discarded and surviving centers moved into `S_n`, at a fixed enlargement of radius. The argument applies to any subset of the containing ellipsoid; no bound on its algebraic complexity is needed.

Writing `e(M)=max_(1<=l<=k)(V_l/M)^(1/l)`, this yields a reachable `M`-point cover of radius at most `C e(M)`. To include all integer budgets, first choose the constant for `M` above a fixed dimensional threshold, so the constant term and the geometric sum fit inside `M`; for the finitely many smaller budgets, use one reachable representative and `e(M)>=lambda_1/M`. When `k=0`, one point is exact.

For the converse, rotate the dominated coefficient ball and project onto any first `l` positive eigenvectors. A fixed-mass uniform rectangle of widths proportional to `lambda_1,...,lambda_l` is dominated by the actual acquisition distribution. At radius `c(V_l/M)^(1/l)`, `M` balls cover at most half of that component's volume, for a sufficiently small fixed `c`. The remaining component gives squared loss at least a constant times `(V_l/M)^(2/l)`. This is a lower bound for arbitrary codebook centers; fixing and then averaging independent coding randomness preserves it. Taking the maximum over `l` yields the profile.

Finally, the raw update gives `e_n<=L e_(n-1)+C e(M_n)`. Starting from the exact prior mean and iterating gives the displayed convolution and the fixed-horizon maximum law. Thus the new theorem can also be obtained from the manuscript's existing thick-linear geometry (`lem:v18-thick-linear`), the genuinely new whole-history/mass verifications, and the raw update.

This derivation explains both the value and the limit of the new application. Its prior-uniform acquisition and causal verifications are real content. Its covering step is the saturated ellipsoid case, not a second example requiring the difficult acquired-dimensional truncation of the monomial theorem. The finite quotient does not make uniformity through degenerating feature coordinates vacuous, but it substantially qualifies the generality one might otherwise infer from the phrase “arbitrary compact latent space.”

## 6. Remaining objections and finite requests

### E22.1 — Contribution case at the requested journal level

**Severity: editorial, decisive for the present recommendation; not a theorem-level contradiction.**

The paper now has two multistep applications. That is an answered mathematical request, not evidence by itself of a four-journal contribution. The editor still needs a concise account of which central phenomenon cannot be recovered from known finite-dimensional quantization tools and what mathematical reach the collision classification has beyond the calibrated finite-horizon setting.

The response should distinguish the genuinely delicate monomial acquisition/collision step from the more elementary transfer and saturated covariance mechanisms. The current accumulation of exact rank, quantization, algebra, kernel, inverse-profile, uncertainty and implementation results does not automatically form one comparably deep classification. The author's explicit caveats are welcome, but caveats are not a substitute for a compelling contribution argument.

**Requested response:** provide a theorem-level account of the irreducible new contribution, identifying the exact hypotheses and conclusions not furnished by the closest existing results. Do not answer by adding more theorem counts, renaming an existing mechanism, or asserting that all previously listed requests have therefore proved significance. This request does not mandate a further new theorem or an unrestricted generalization, and compliance is not a promise of acceptance.

### E22.2 — The comparison should include nonlinear-filter quantization itself

**Severity: substantial positioning/attribution request; no established priority violation.**

The active text contains comparisons with approximate information states, finite MDP approximations and finite-window policies. It does not cite Pagès–Pham or Pagès–Sagna. For a paper whose new centerpiece is a finite-horizon causal filtering approximation built from quantization and stability, those are materially closer mechanisms than a discussion confined to finite-window sufficiency.

Pagès–Pham [P3] is specifically about quantization for nonlinear filtering with discrete-time observations. The accessible Section 6 and Theorem 6.3 of Pagès–Sagna [P4] give normalized-filter error bounds controlled by accumulated quantization errors, under explicit regularity and integrability assumptions. This supports the need for comparison, not a claim that their theorem proves the present optimal finite-label law.

**Requested response:** compare the compressed object, charged resource, observation model, physical prediction norm, upper versus matching lower bounds, and uniformity under rank/prior degeneration. Quantizing hidden states and propagating a probability vector is not automatically the same resource as retaining one of `M` posterior labels. Likewise, a regularity-dependent filtering upper bound is not automatically a matching all-prior covariance classification. Spell out these differences instead of either ignoring the literature or declaring the new theorem subsumed without a reduction. I have inspected the accessible filtering theorem, not the inaccessible full publisher text of [P3], and make no stronger priority claim.

### E22.3 — Explain the saturated geometry before deploying the general machinery

**Severity: proof architecture and mathematical exposition; the existing proof is not invalid.**

Lines 278–279 explicitly apply the transfer theorem with `p_n=q_n=d`. Section 5 of this report shows why a direct ellipsoid argument suffices. The new section should state near its theorem that its reachable dimension saturates after the first observation and that the observable quotient is finite. Both facts clarify its relationship to the monomial result. The finite-quotient fact is already proved later; the request is to make its consequences visible when the theorem's scope is first assessed.

**Requested response:** add a short saturated-geometry explanation and either give the direct thick-linear reduction or identify it as an alternative proof. Retaining the uniform transfer route is reasonable, but do not leave the reader to infer that this application needs every geometric ingredient used in the monomial case. The complete proofs and historical sources can remain available; arbitrary deletion of mathematical content is not requested.

The 120-page article would also benefit from separating the indispensable proof spine from independent developments and alternative derivations. The existing appendices are an improvement, but preservation of an archive and the composition of a journal article are different tasks. A proof can be retained in full without occupying the same narrative position as a central new theorem.

### E22.4 — Correct the local reference for the risk criteria

**Severity: minor and local.**

At `sections/algebra_multistep.tex`, lines 57–62, the two checkpoint risk criteria are attributed to `def:finite-state`. That definition specifies the transducer resource, not the two named variational infima. The surrounding article supplies the intended interpretation, so I do not regard this as an ambiguity sufficient to invalidate the theorem.

**Requested response:** point to the actual risk definitions or write the infimum conventions locally: expected loss under the fixed exploration law for the average criterion, supremum over feasible histories with coding randomness averaged for the worst-history criterion, and an infimum over one common causal filter outside the maximum over checkpoints for the multistage criterion. Preserve the distinction between `inf max_n` and `max_n inf`. No change to the theorem's mathematical scope is needed.

## 7. Executed checks and their limits

The review did not accept a successful repository badge as a mathematical certificate. The following operations were performed in this review session.

**Source identity and preservation.** The outer Actions package SHA-256 is `8d8778819a61487c464bf37ac8624524c3346ebac69058d622d12f237f37dc79`. Four Git blob identities and all 763 current manifest entries were independently checked. Active-source block comparison independently recovered the 122 unchanged statements, 118 unchanged proofs and two citation-only changes described above.

**Author v22 tests, actually rerun.** `tests/verify_v22.py` completed with 244 experiment cases and **38,454 checks**. It was executed normally and under `python -O`; the receipts were byte-identical. These are rerun author diagnostics, not independently designed tests.

**New independent diagnostics.** The accompanying `independent_diagnostics.py` uses only exact `fractions.Fraction` arithmetic and the Python standard library. It imports no manuscript implementation. It completed **13,884 checks** over 50 models, 400 full report histories and 1,200 checked prefixes. Fifteen models had genuinely non-associative coefficient multiplication while representing associative pointwise products. Tests include redundant and constant generators, support-boundary and rare-atom priors, zero/unequal detector channels, direct latent Bayes versus coefficient charts and raw updates, physical query scaling, covariance/support-affine ranks, report-word probability partition, selected Jacobian identities and integer inverse witnesses. Explicit negative controls distinguish omitted normalization, a second-moment substitution and the wrong covariance scale. Normal and optimized execution produced identical receipts. The exact script hash is in `DIAGNOSTICS.json`.

These finite checks do not prove uniform density, covering estimates, optimal coding lower bounds or correctness for all real parameters. Those claims were assessed analytically in the sections above.

**Build.** A separate `python build.py` completed with three `pdflatex` passes and shell escape disabled. It produced 120 pages, with zero undefined-reference or overfull warnings in the build report. The locally rebuilt PDF SHA-256 is `f094fcab855408fa538453a6e7f4eed6ecc0a0798092237fcbb7384c4f856ef3`. This is a local build receipt, not a claim that the PDF is byte-identical to the author's PDF. No visual page-by-page PDF inspection was performed; this is a source-based mathematical review.

**Incomplete full-suite attempt, explicitly disclosed.** The full `python validate.py` run hit the review environment's 200-second execution limit during v12. The local progress receipt records completed v10 and v11 suites with 7,904 and 8,207 checks respectively, but no completed local full-suite receipt. I therefore do not claim to have rerun all 171,221 checks reported by the author's original package, nor all inherited referee diagnostics. The timeout is not evidence of a mathematical failure. The targeted v22 run and the separate full build described above did complete.

`REVIEW_SCOPE.json` records the source identities, preservation method, execution boundaries and exclusions. In particular, this report is not an exhaustive certification of the effective-construction, uncertainty, circular or decision appendices; not an exhaustive historical-archive audit; and not a proof of priority relative to all published literature.

## 8. Primary-source checks

The following sources were used for specific external checks, not as a substitute for reading the submitted proofs. Their relevance is deliberately limited.

**[P1]** Y. Zhang and J. Kileel, *Covering Number of Real Algebraic Varieties and Beyond: Improved Bounds and Applications*, arXiv:2311.05116v4. The accessible Section 2, particularly Lemma 2.18, records bounded-format semialgebraic regularity/component control. The needed classical input should not be confused with a new contribution of the submitted paper. https://arxiv.org/html/2311.05116v4

**[P2]** G. Comte and I. Halupczok, *Motivic Vitushkin invariants*, arXiv:2206.15412v2. The introductory real formulas (4)–(5) recall Vitushkin variations and the real metric-entropy inequality. Only that real background is used here, not the paper's nonarchimedean theorem. https://arxiv.org/html/2206.15412v2

**[P3]** G. Pagès and H. Pham, *Optimal quantization methods for nonlinear filtering with discrete-time observations*, Bernoulli 11(5), 893–932 (2005), DOI `10.3150/bj/1130077599`. Bibliographic/topic comparison only; no claim of full publisher-text inspection. https://doi.org/10.3150/bj/1130077599

**[P4]** G. Pagès and A. Sagna, *Improved error bounds for quantization based numerical schemes for BSDE and nonlinear filtering*, arXiv:1510.01048v3, Section 6, especially Theorem 6.3 and Remark 6.4. Used for the concrete comparison with accumulated quantization errors in normalized nonlinear filtering, not to assert equivalence of resource models or matching converses. https://arxiv.org/html/1510.01048v3

**[P5]** T. Terao, *Faster Approximate Linear Matroid Intersection*, 20th Scandinavian Symposium on Algorithm Theory (SWAT 2026), LIPIcs 370, article 39, 39:1–39:19. Publisher record verifies the corrected metadata. https://drops.dagstuhl.de/entities/document/10.4230/LIPIcs.SWAT.2026.39

## 9. Final assessment

The revision should receive credit for answering the previous concrete requests, preserving the inherited mathematics and proving a real prior-uniform multistep statement. A harsh report must not erase those facts to produce a more dramatic verdict.

Nevertheless, I would not recommend acceptance, or a merely cosmetic revision leading to acceptance, at the requested four-journal standard on the present evidence. The new algebra theorem survives the checks made here, but its finite observable quotient and immediate acquisition saturation substantially narrow what it demonstrates about general multistep geometry. The principal collision theorem remains the central contribution requiring a convincing theorem-level significance and literature comparison. The exact-kernel and other companion developments have their own hypotheses and should not be counted as automatic evidence that one universal classification has been proved.

The appropriate next response is to address E22.1–E22.4 directly, with the finite mathematical distinctions and comparisons specified above. This report does not demand an endless sequence of appended theorems, does not require weakening the existing true statements, and does not turn an editorial judgment into a nonexistent mathematical obstruction. All correctness conclusions remain bounded by the explicit scope of this review.
