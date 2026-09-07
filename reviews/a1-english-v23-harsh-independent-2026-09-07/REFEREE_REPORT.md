# Referee report on A1 English v23

**Manuscript:** *Attainable information geometry in positive experiments*, Qian Qi.  
**Assessment date:** 7 September 2026.  
**Examined branch:** `revision/a1-english-v23-collision-spine-saturated-proof-2026-09-07`.  
**Immutable submission:** `e7c1111d0ab8fb39e4b213902186db2cdf6d0dea`, directory `papers/A1-english-v23/`.  
**Controlling previous report:** `325e89b9c012830cbd219fec0cff7c52b8e8d321`, `reviews/a1-english-v22-harsh-independent-2026-09-07/REFEREE_REPORT.md`.  
**Previous manuscript identified by the response:** `5f745a863dac637496bd5eb20341f12cecb71ab1`, `papers/A1-english-v22/`.

This is an owner-requested, AI-assisted repository referee assessment at the requested Annals/Inventiones/JAMS/Acta level of scrutiny. It was not commissioned by any journal and does not represent a human referee appointment. Independent diagnostics mean calculations designed and executed in this assessment without importing the author's implementation. They are not formal verification.

## 1. Recommendation

**I do not recommend acceptance at the requested four-journal level. My recommendation is rejection of this submission at that level, on editorial grounds of mathematical significance and proportion, not on a demonstrated false principal theorem.**

The distinction is essential. The specific requests E22.1–E22.4 have received substantial, inspectable responses. I would close those concrete requests rather than reproduce them under new numbers. The collision theorem has a coherent proof route, and the new direct algebra proof survives the checks detailed below. I found no fatal mathematical counterexample or unresolved central proof gap in the audited route. That finding is not a certification of every appendix.

The strongest contribution is the collision-uniform, acquired-dimension-truncated classification for positive sparse monomial experiments. It is not merely a claim about the rank of a Vandermonde matrix. Its acquisition argument and the simultaneous validity of the lower bound, whole-image cover and causal realization deserve credit. The two-parameter example gives a particularly good demonstration of the result's mathematical content.

Nevertheless, my assessment is that the demonstrated advance remains a specialized fixed-horizon classification built from a nontrivial compatibility argument and well-established geometric and approximation mechanisms. The saturated observation-algebra theorem is useful but substantially more elementary geometrically. Taken together, they do not, in my judgment, justify the submitted article's breadth and author-reported 125-page scale at the requested venues. This is a judgment about the weight of the established contribution, not an assertion that the exact theorem was previously published. I have not established such a priority claim.

I am not recommending a nominal “major revision” with an implied promise that another comparison paragraph, another test count, or one more appended theorem will secure acceptance. The concrete previous revision tasks can be completed while a venue-level recommendation remains negative. Conversely, this recommendation is neither a no-go statement about the research program nor a reason to weaken a true theorem.

## 2. Submission identity, scope and evidentiary boundaries

The branch was located through the connected GitHub repository and its head resolved to the immutable submission above. The inspected commit's message identifies v23 as the readable-source revision responding to the v22 report. Source readings were pinned to that SHA rather than to a moving branch.

The mathematical reading concentrated on the principal finite-memory route and the changes that answer the controlling report: the experiment and finite-state definitions; the positive mixed pairing and binomial tangent; the main classification statement; the confluent pairing and thin-rectangle estimate; the Leja flag and actual acquisition argument; the transfer theorem and its monomial verification; the collision consequences; the complete algebra section, new saturation proposition and direct proof; and the nonlinear-filter comparison. The active `main.tex` was inspected to identify the reading route. Source locations below are relative to `papers/A1-english-v23/` and use stable theorem labels.

The prior report and the current response and proof ledger were read as documents to assess, not as proof certificates. In particular, previous claims that an appendix had been checked were not silently promoted into new independent checks in this assessment. This is not a fresh exhaustive audit of the circular, uncertainty, exact-kernel, numerical-construction, mechanical-realization or decision appendices, nor of the complete eleven-paper program.

The author's `BUILD_REPORT.json` records 130 compiled formal statement blocks, 129 proof blocks, a three-pass 125-page build and preservation of the inherited 129 statements and 127 proofs. These are **author-reported receipts inspected in the repository**, not counts or builds independently reproduced here. The current assessment did not independently expand the 772-entry source manifest, recompute the full preservation comparison, rerun the author's suites, or rebuild or visually inspect the PDF. Direct runtime network access failed; authenticated connector text reads remained available and were used. That operational limitation is not a mathematical defect of the submission.

The executed work here is the separate exact-rational diagnostic suite described in Section 8. `REVIEW_SCOPE.json` records the boundaries explicitly.

## 3. Disposition of the controlling requests

| Previous request | What is present in the actual v23 source | Disposition |
|---|---|---|
| E22.1: identify the theorem-level contribution and indispensable proof route | The abstract and `sections/introduction.tex`, especially `sec:contribution-v23`, identify the collision/acquisition/global-cover/causal conjunction. The example `A={0,1,3}`, `(n,m)=(1,2)` distinguishes five raw future directions from two acquired dimensions. The limits of the two experimental classes are explicitly stated. | The concrete expositional request is addressed. This does not settle the separate editorial significance judgment. |
| E22.2: compare directly with nonlinear-filter quantization | `sections/filter_quantization_comparison.tex` compares the compressed object, charged state resource, norm, observation model, upper bounds versus converses, and degeneration uniformity. It includes Pagès–Pham and Pagès–Sagna rather than relying exclusively on more remote approximation literature. | Addressed for the specified comparison. No exhaustive priority conclusion follows. |
| E22.3: disclose saturation and give a direct reduction | The opening of `sections/algebra_multistep.tex` states the finite observable quotient and immediate saturation. `sections/algebra_saturated_geometry.tex` proves the ellipsoid sandwich and gives a complete direct covering, mass and causal argument. `main.tex` includes the former transfer route in the active appendix. | Addressed. The new direct argument is substantive and not merely a new name for the old proof. Byte-for-byte preservation is not independently certified here. |
| E22.4: make the risk criteria and quantifier order local | `def:algebra-risks` explicitly writes both checkpoint infima and both common-filter infima, placing the latter outside the checkpoint maximum and averaging coding randomness before the worst-history supremum. | Corrected. |

There is no justification for claiming that v23 still lacks a second multistep application, still conditions away the selected report word, still interchanges the infimum and maximum, or still hides the finite-algebra quotient. Those would be objections to a different manuscript.

## 4. Principal collision theorem: technical assessment

### 4.1 Physical information and the resource being charged

In `core/02_experiments.tex`, `prop:tests`, equality of future monomial moments is shown to characterize the common future-only experiment. An adaptive future word has fixed commands along that word, so its likelihood remains a product in the stated test space. This is not the same as allowing a continuation to recover an uncharged pre-checkpoint command history. The definition excludes the latter.

`build/operational_model.tex`, `def:finite-state`, charges the complete retained label, allows stage-dependent read-only real data, and does not charge execution time or arithmetic workspace. Query selection occurs after retention. The squared excess loss is therefore the squared discrepancy between conditional physical query probabilities. These conventions are coherent. They are not a total-space or efficient-algorithm theorem, and the report does not reinterpret them as one.

The fixed formal product coefficient matrix remains full-column-rank when two evaluated exponents coincide. Coincidence constrains reachable moment vectors; it does not make the symbolic coefficient matrix singular. The monomial application uses precisely this distinction. An objection based on losing the formal left inverse at a collision would be incorrect.

### 4.2 The acquired dimension is established, not assumed

The decisive locations are `core/03_transversality.tex`, `lem:mixed-moment`, `lem:binomial-tangent`, and `eq:normalized-derivative`.

The mixed determinant identity integrates the product of two generalized Vandermonde determinants. Ordered separated interior intervals have positive mass under a full-support prior even when that prior has no density. This gives strict positivity, not merely nonnegativity.

At the binomial tuple, the polynomials obtained by omitting one factor are independent by evaluation at their distinct negative reciprocal roots. Their product tangent has exactly `n(r-1)+1` distinct monomial directions. The product itself belongs to that tangent. After moment pairing, normalization kills exactly its one-dimensional scaling direction: `v -> v-p e_0(v)` has kernel `span{p}` on the paired image, with `e_0(p)=1`. Thus the lower-dimensional cap is `min{n(r-1), |mA|-1}`.

This is a genuine experiment-side calculation. It would not be legitimate to replace the attainable image by its generally larger affine hull. The inspected proof does not do so. For the introduction's example the positive future exponents are `{1,2,3,4,6}`, but one acquisition has only two available factor coordinates after normalization. The eventual squared-error rate is consequently `M^(-1)`, not `M^(-2/5)`.

### 4.3 Confluence and Leja scales

`build/collision_flags.tex`, `lem:leja-scales`, gives a finite-dimensional triangular comparison, including zero pivots. Greedy maximality bounds the normalized Newton coefficients by one; the leading nonzero triangular block has diagonal entries of absolute value one. The maximal Vandermonde comparison follows by evaluating monic Newton polynomials on arbitrary selected nodes and applying the determinant expansion. No inverse of a zero pivot is required.

The attainment statement needs more than this interpolation calculation. In `lem:newton-attainment`, every initial multiset produces a **complete** Hermite family. The divided-difference functionals are independent on polynomials through the requisite degree; their span is the full collection of evaluations and consecutive derivatives at the selected repeated nodes. The proof is not attempting to infer a Chebyshev property for an arbitrary collection of isolated high derivatives.

`build/analytic_inputs.tex`, `lem:confluent-positive`, supplies the required confluent mixed pairing. The logarithmic factors are bounded at zero because positive nodes stay uniformly away from zero and the constant node occurs with multiplicity one. At the common binomial command tuple the normalized differential has full row rank for every relevant prefix. Compactness over the fixed chamber and the finite set of permutations then supplies the uniform lower singular-value bound.

The probability argument also matters. The square inverse chart includes complementary command coordinates. It integrates a positive-volume neighborhood in those coordinates and includes the all-failure probability. It does not assign positive probability to a frozen command slice. I found no missing density assumption on the prior or omitted report-word factor in this argument.

### 4.4 The cover is of the whole image

The thin-rectangle estimate in `build/analytic_inputs.tex`, `lem:tame-rectangle`, follows from classical component/variation control, not from a newly proved general entropy principle. The primary-source checks in Section 9 support the cited inputs.

Its dimension truncation is properly justified: almost every affine section of codimension larger than the image dimension is empty; for smaller codimension the projected containing rectangle controls the translation volume. The zonotope volume estimate yields products of the largest side lengths. Integer budgets are handled separately when the constant term in the covering count cannot be absorbed.

In `sections/collision_transfer_application.tex`, each fixed-calibration report-word image is rational in command coordinates with positive denominator and bounded degree. Real moment integrals enter as coefficients. They need not be algebraic functions of the calibration for a bounded-format assertion about each command image. The ambient transformation built from the nonzero triangular block has uniformly bounded inverse even at exact collisions; the remaining transformed raw coordinates are zero. I found no coefficient-definability or ambient-invertibility gap here.

### 4.5 Causal implementation does not reread the prefix

`sections/causal_transfer.tex` separates whole-image geometry, actual acquired mass and reachable-state updates. The upper construction updates a reachable representative and then quantizes in the next reachable codebook. The error recurrence retains all preceding quantization errors. The lower bound is imposed on each fixed common filter at every checkpoint under marginals of one exploration law, before taking the outer infimum.

For monomial experiments the raw remaining moments close under multiplication by the next likelihood. The Bayes denominator is bounded below on a segment between reachable posterior moment states because that segment represents a mixture of posteriors. This supplies a gap-independent Lipschitz estimate without a Newton-scale inverse. It is the correct way to use geometrically singular coordinates for analysis without forcing them to carry the recursion.

Independent public coding randomness can be conditioned on; private decoder randomness can be averaged under squared loss. Neither step permits randomness correlated with the acquired history to become an uncharged information channel. Under the stated resource convention the randomized lower argument is valid.

### 4.6 The collision example is stronger evidence than theorem counts

`build/collision_consequences.tex`, `cor:two-parameter`, is worth emphasizing. For `A={0,1,2+u,3+v}`, the nine positive two-fold formal sums form six separated groups with three internal gaps `|u|`, `|v-u|`, `|v-2u|`. The largest two gaps are comparable. This makes the seven-dimensional risk branch redundant and leaves the displayed six-, eight- and nine-dimensional regimes.

The exact peak ranks 6, 8 and 9 at the intersection, along a nontrivial collision line and off the lines are consistent. Along `u=theta`, `v=theta+theta^k`, the two budget crossover orders are `theta^(-6)` and `theta^(-(8k-2))`; substituting them gives regret orders `theta^2` and `theta^(2k)`. The calculations in Section 8 check the exponent arithmetic and representative collision strata independently. Arbitrary finite contact order here is genuinely different from imposing one simple gap, although it remains a fixed-horizon theorem.

## 5. New saturated algebra proof: detailed assessment

### 5.1 Saturation and support loss

`prop:algebra-saturation` combines the whole-history identity

`v_n = m + Sigma theta_n`

with a bounded coefficient range and an actual inverse acquisition patch to obtain

`m + Sigma(r B_d) subset S_n subset m + Sigma(R B_d)`.

This proves relative dimension `rank(Sigma)` at every positive checkpoint, including zero rank. The qualitative statement that this rank equals the number of positive-mass observable parts minus one follows from independence of the evaluation rows of the finite function algebra. The possibly ill-conditioned indicator coefficients are not used in quantitative constants.

Thus the theorem really is prior-uniform across support loss under the stated bounded multiplication assumptions. But acquisition saturates immediately: it is not a second proof of delayed acquisition of a growing collision flag. The revised source now makes this distinction properly.

### 5.2 Integer covers and arbitrary prediction centers

The direct grid proof in `sections/algebra_saturated_geometry.tex` covers the containing covariance ellipsoid, discards empty cells and chooses reachable representatives. For `M>=2`, choosing the radius constant to make the nonconstant covering terms at most `M/2` leaves at most `1+M/2<=M` cells. For `M=1`, the prior mean is reachable by zero commands. The zero-rank case is treated separately. There is no asymptotic-only gap in the stated all-integer-budget conclusion.

For the converse the dominated coefficient ball is rotated, a fixed cube is retained, and its first coordinate prefixes are projected before multiplication by the covariance eigenvalues. The dominated mass is independent of those eigenvalues. The volume exclusion estimate accommodates arbitrary decoder centers, not just reachable ones. Converting arbitrary predictions to raw-mean centers and discarding the constant-query error is legitimate.

The physical factor is exactly

`2^(-2(N-n)) delta^2/(d+1)`

times squared raw-mean distance. The semiaxes are covariance eigenvalues, not their square roots. The argument does not conceal a whitening operation.

### 5.3 The actual law and the raw update

The complete acquisition lemma in `sections/algebra_multistep.tex` uses the all-positive word. With later commands zero, the first-command coefficient map is `z/(1+m^t z)`, whose derivative at zero is the identity. Bounded multiplication coefficients and positive evidence make the inverse construction uniform over priors. A positive-volume neighborhood of the later commands is then integrated.

The density includes `(2 delta)^(-nd) 2^(-n) Z_n`. This is the joint command-and-word law. Neither support degeneracy nor a redundant feature representation invalidates it: the coefficient coordinate is used on histories and is not claimed to be uniquely determined by the raw mean.

The raw update is the stated Bayes quotient with denominator at least `3/4` on posterior mixture segments. Extending a realizing history proves reachability of its update. Hence codebook re-quantization produces a genuine common causal filter. The local risk definitions and the order of the lower-bound argument agree.

### 5.4 An independent scalar calculation

Here is a useful check not taken from the author's test implementation. Take the two-point latent space, `f=tau 1_{1}`, prior mass `p`, one acquisition and one future query. Let `m=tau p` and `Sigma=tau^2 p(1-p)`. Conditional on command `u` and report `y`,

`v-m = y u Sigma/(1+y u m)`.

The actual report probability is `(1+y u m)/2`. Therefore

`E[(v-m)^2 | u] = Sigma^2 u^2/(1-u^2 m^2)`.

For the uniform command on `[-delta,delta]`, the optimal one-label predictor is the prior predictor, by total expectation. With the paper's two-element physical query menu, its exact risk satisfies

`delta^4 Sigma^2/24 <= R_av(1) <= delta^4 Sigma^2/[24(1-delta^2 m^2)]`.

This confirms the covariance-squared scale, including the fourth power of attenuation and vanishing prior mass. It also shows why substituting a second moment or a square-root covariance scale would be wrong. It supports the printed theorem rather than contradicting it.

## 6. What the results do and do not establish

The mathematical contribution should be evaluated at the quantifiers actually proved. The monomial theorem fixes a full-support prior, a finite horizon, a positive detector and a compact strictly ordered one-step chamber; it is uniform in additive collisions and integer budgets. The algebra theorem has stronger prior uniformity but a finite observable quotient and bounded multiplication closure. Neither theorem is asserted to cover every positive detector, nor does their conjunction supply one theorem uniform simultaneously over unrestricted priors and all monomial geometries.

The fixed-prior restriction in the monomial statement is mathematically substantial, not merely a technical wording choice. For example, let `mu_epsilon=(1-epsilon)delta_0+epsilon Uniform[0,1]`. Every positive epsilon gives full support. For a fixed positive experiment and fixed horizon, each nonconstant posterior monomial moment is at most `epsilon kappa^(-n)` at checkpoint n. The prior itself is reachable through constant failure commands. One retained prior representative therefore has worst-history squared physical prediction error `O(epsilon^2)`. In contrast, the formal profile at `M=1` contains `V_1=1`. A positive lower comparison constant cannot be uniform over this prior family. This confirms a restriction already disclosed in the theorem; it is not a newly discovered counterexample to it.

Likewise, finite-horizon error accumulation and lower evidence bounds can deteriorate with the horizon. A fixed real-valued codebook program does not imply a uniformly efficient construction or a total computational-space bound. The manuscript now acknowledges these distinctions, and they must remain in any assessment of its implications.

The right originality question is consequently whether the particular collision-uniform experimental classification, especially simultaneous acquisition of all complete prefixes, constitutes an advance of exceptional mathematical weight. It is not whether the paper invented Newton interpolation, total positivity, ellipsoid quantization or stability-based propagation. The source now correctly credits those mechanisms. The present literature checks do not prove that the exact classification is known, but they do explain why the transfer and saturated covering components should not be counted as separate major conceptual breakthroughs.

## 7. Editorial judgment and finite recommendations

**E23.1 — Venue-level significance; blocking for my recommendation, not a proof defect.** The paper now explains its contribution more accurately. My remaining negative assessment is not that the explanation is absent. It is that the established specialized classification and its elementary saturated companion do not, on the evidence examined, carry the exceptional depth and proportion I would require for the requested four-journal submission. An intelligent synthesis can be mathematically valuable without meeting that particular publication threshold. Reasonable specialists may weigh the central collision result differently; this report does not manufacture an objective priority obstruction to settle that judgment.

**E23.2 — Article architecture; nonfatal and not an instruction to delete mathematics.** The active route is much better organized than an undifferentiated archive. Nevertheless, the independent exact-kernel, uncertainty, mechanical, decision and implementation developments have different hypotheses and are not indispensable to the principal collision proof. Their preservation is valuable; their presence in the same large article does not automatically strengthen the principal theorem's significance. A submission-focused core and separately organized complete companions could retain all mathematics while improving proportion. This is a presentation recommendation, not a demand to erase inherited proofs, and by itself would not reverse E23.1.

**E23.3 — Put the strongest existing example to work; optional exposition.** The two-parameter collision example communicates more than the new collision-free five-coordinate/two-dimension illustration alone. A brief early reference to its 6/8/9 ranks and separated crossover orders would make the actual multiscale content easier to assess. The example already exists and is proved; no additional theorem or extension of hypotheses is requested.

There is **no new mandatory list of alleged fatal mathematical defects** in this report. In particular, I do not request an unbounded-horizon theorem, all-prior monomial uniformity, a third application, or another general transfer theorem as a moving condition for closing E22.1–E22.4. Those requests would change the problem rather than fairly assess this revision. The author need not answer an editorial disagreement by weakening correct results or appending unrelated results.

## 8. Executed independent diagnostics

`independent_diagnostics.py` uses only the Python standard library and exact `fractions.Fraction` arithmetic. It completed **3,878 checks**, with byte-identical JSON receipts under ordinary Python and `python -O`. The script contains explicit exception-based checks; optimization does not disable them. Its SHA-256 is recorded in `DIAGNOSTICS.json`.

The diagnostics include 16 formal-node multisets; 36 binomial acquisition models and 144 selected node orderings; exact repeated-node Newton identities; Leja monotonicity, zero pivots and maximal determinant inequalities; confluent mixed-pairing and normalized-prefix ranks; six two-parameter collision calibrations; 25 finite-algebra models, 200 complete report histories and 600 prefixes; raw Bayes versus coefficient updates; covariance/support ranks; physical squared-loss scaling; unconditional word-probability partition; integer inverse witnesses; seven contact orders; and causal accumulation identities.

For the uniform prior, the independent identity

`integral_0^1 t^a [b_1,...,b_j](b -> t^b) dt = (-1)^(j-1)/product_i(a+1+b_i)`

allows the mixed and normalized differential calculations to remain exact at repeated nodes. There is no floating-point rank threshold. Negative controls distinguish omitted normalization, second moments in place of covariance, the wrong attenuation scale, replacing a selected word's probability by one, swapping infimum and maximum, and retaining only the last stage's error.

These counts are an execution description, not a measure of theorem depth or a certificate. Finite examples do not prove uniform positive density, global covering estimates, optimal-code lower bounds, all-prior assertions or arbitrary real-parameter limits. The algebra diagnostics use indicator presentations and do not exhaust redundant, non-associative coefficient rules. Those analytical and scope distinctions are assessed from the source rather than inferred from successful tests.

## 9. Primary-source checks

**[P1]** Y. Zhang and J. Kileel, *Covering Number of Real Algebraic Varieties and Beyond: Improved Bounds and Applications*, arXiv:2311.05116v4, especially Lemma 2.18. The bounded-format semialgebraic regularity input is classical relative to the submission; it does not itself supply actual acquisition mass or the experimental lower bound. https://arxiv.org/html/2311.05116v4

**[P2]** G. Comte and I. Halupczok, *Motivic Vitushkin invariants*, arXiv:2206.15412v2. Only the introductory real Vitushkin-variation and entropy background is relevant to the submitted thin-rectangle argument. No nonarchimedean theorem is used to justify the real covering step. https://arxiv.org/html/2206.15412v2

**[P3]** G. Pagès and H. Pham, *Optimal quantization methods for nonlinear filtering with discrete-time observations*, Bernoulli 11(5), 893–932 (2005), DOI `10.3150/bj/1130077599`. The publisher search record and bibliographic/topic information were checked. The publisher full-text page did not return usable article text; no full-text inspection is claimed. https://doi.org/10.3150/bj/1130077599

**[P4]** G. Pagès and A. Sagna, *Improved error bounds for quantization based numerical schemes for BSDE and nonlinear filtering*, arXiv:1510.01048v3, Section 6, Theorem 6.3 and Remark 6.4. The inspected result bounds squared normalized-filter error by a weighted sum of squared signal-quantization errors, with normalization factors and explicit hypotheses. It supports the manuscript's acknowledgement of established error-propagation mechanisms, but does not identify a signal grid cardinality with the number of complete retained posterior labels. https://arxiv.org/html/1510.01048v3

This is a targeted primary-source comparison, not an exhaustive survey proving originality or lack of originality. No figure or PDF analysis was used; the accessible HTML mathematical text was examined.

## 10. Final assessment

The revision has done the requested mathematical and expositional work on the concrete v22 comments. The principal collision route and the new direct saturated-algebra proof survived this assessment's central analytic checks and independent finite diagnostics. A harsh review should record that rather than invent a fatal gap.

My venue recommendation remains negative because I do not judge the established contribution, in the submitted scale and architecture, sufficient for the requested four-journal standard. That is the actual remaining disagreement. It is not a concealed claim that the core results are false, that an old objection remains unanswered, or that the research direction cannot be advanced. All mathematical confidence statements remain bounded by the explicit source and execution scope above.
