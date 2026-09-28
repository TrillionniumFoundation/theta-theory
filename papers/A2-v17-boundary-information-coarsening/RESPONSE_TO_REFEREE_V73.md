# Response to the referee on A2, revision 72

Qian Qi · September 17, 2026

**Manuscript:** *Boundary laws and smooth contact rigidity of periodic dispersing billiards*  
**Revised version:** 73  
**Report addressed:** `reviews/a2-v72-independent-harsh-top4-2026-09-17/REFEREE_REPORT.md`, commit `c6715aff47ad6e8180acfa7ba229fd680e795293`.

We thank the referee for distinguishing the correctness of the examined mathematics from the judgment of exceptional significance. The report finds no new fatal mathematical error and identifies no mandatory repair of the examined core proof. We do not recast that finding as an unresolved lemma, and we do not claim that another version number settles the placement judgment. The two concrete presentation suggestions have been incorporated. More substantially, the revised article identifies the complete invariant of the existing charged local experiment and gives a jointly realizable finite-preparation estimate for it.

The manuscript retains the full scope of revision 72: the general two-known-offset theorem, the symmetric one-known-offset inverse, the unequal-action one-unreported-offset theorem, all actual smooth proofs, the analytic/global branches, the information and acquisition catalogue, and the companion. No theorem has been removed to make the main statement appear more general. Historical derivations and all prior reports remain available. Modified inherited source files have byte-preserved originals under `history/v72-review-baseline/`.

## The mathematical addition

Let `pi_(N,b)` be the success probability on the specified gate, `f_(N,b)` the conditional endpoint density on that gate, `D_(N,b)` the exact reference twist, and `A(T)` the free area of the marked cell. The physical phase-volume formula has the exact finite-flight central identity

\[
 \pi_{N,b}f_{N,b}(0,0)=\frac{D_{N,b}d_b}{2\pi\mathcal A(T)}.
\]

This uses the exact identities `beta_(N,b)(0,0)=1` and `E_(N,b)(0,0)=0`, not a limit approximation. The limiting laws already recover the fixed offsets and the actual contact germs. Their curvatures then determine the Jacobi normalization. Thus success information identifies the free area, which conditioning had canceled. Equivalently, at one phase the scalar `lim pi_(nP,b)/D_(nP,b)` recovers the area together with the limiting laws.

This gives both directions of a classification: equality of the germs of the charged reset records is equivalent to equality of the **actual smooth contact germs, fixed offsets, and free cell area**. Conditional limiting-law germs correspond exactly to the first two components. The remote equal-area completions constructed in the retained locality section are precisely part of the surviving observation fibers. No whole-table determination is inferred.

A separate estimate addresses finite data. Curvature error changes the logarithm of the reference twist by at most `C(1+N)` times that error. The finite estimator uses a countable dense subset of the **realizable finite-record image**, including a log success probability, and selects an actual table–offset pair. Its reported area is the area of that same table. With all `rB` resets charged, the joint profile, offset and logarithmic-area error is bounded by

\[
 C t\log(e/t),\qquad t=(L_B/B)^\beta+\delta^\gamma,
\]

under the explicit class, count, bandwidth and small-error conditions. The returning length depends on the readout floor as well as the budget. The logarithm accounts for the additionally reconstructed area; the earlier profile-and-offset bound is retained without this extra factor. These results are in `article/10h_complete_record_v73.tex`, summarized in `article/00n_record_overview_v73.tex`.

## R72-M1 — Unknown offset and retained marked scale

We accept the report's analysis. The nonzero signed physical momentum remains supplied by the marked polygon, and the offset remains a fixed nuisance constant in a positive interval. Unknown contact heights, curvature, flux factors and numerical offsets are not inserted into the observations. The mark does not disappear merely because the offset is reconstructed. No random drift, inaccurate gate or erroneous success tag is included.

The clock theorem and its proof are retained. The new complete-record theorem uses this identified offset before constructing the area invariant. Its statement does not claim recovery with every physical scale unknown. An exact conditional law still means an entire two-variable distribution, not a single number or trajectory; finite density estimation is addressed separately.

## R72-M2 — Signed anchors and fixed-order stability

The factor separation theorem is retained without changes to its formulas or proof. Signed anchors, their geometric lower bounds, and the distinction between a scalar derivative evaluation and differentiation of an entire reconstructed function are unchanged. The new finite-record estimate uses the same `C^m` action control, then the global positive quadratic inverse, to estimate the curvature vector needed for the normalization.

We continue to credit the older symmetric, known-offset rank-one argument as a predecessor. Neither the revision 72 extension nor the present central area identity is presented as a new general theory of factorization. The substantive new statement concerns the complete physical observation invariant and its actual-table finite reconstruction.

## R72-M3 — Actual smooth contacts and the derivative order

The actual smooth inverse remains the indispensable geometric step. The new observation classification invokes the complete action inverse, including the contracted-visit separation of flat differences; it does not infer equality of smooth functions from equality of Taylor series. The global quadratic identification and signed higher blocks remain in place.

We have made the inherited quantitative condition visible directly in the revision 72 joint stability theorem:

\[
 m\ge3,\qquad 6a^m/(1-a^m)<1,
\]

on the enlarged positive quadratic class. The new finite-record section repeats the same condition. This is a class-dependent sufficient order, not an assertion for every `m>=3`. No uniformity at vanishing hyperbolicity or obliquity, grazing, or changing period is claimed. The stated polynomial alignment precedes the weighted remainder estimate, as before.

## R72-M4 — Obliquity coverage

The first-hit argument and the exceptional self-retracing normal two-contact orbit are retained. Consequently the new oblique complete-record theorem also covers every clear polygon with at least three distinct physical contacts in the stated class. The normal-incidence alternatives have not been removed. The failure of the mixed clock at normal incidence is not advertised as a universal non-identifiability theorem for other observations.

## R72-M5 — Exact finite-flight clock correction

The requested identity is now printed immediately after the limiting clock proposition, in the unnumbered paragraph “The clock before the relative limit”:

\[
 \partial_{uv}\log f_N(0,0)
 =p^2/d^2+D_N/d+\partial_{uv}\log\beta_N(0,0).
\]

The proof differentiates the actual residual and keeps the amplitude term with no sign assertion. Positive floors and the differentiated relative limit give an explicit exponentially small bias bound for the finite plug-in clock, once its mixed derivative is positive. This is attributed to the present report through `A2ReviewV72`; the report is identified as an author-requested AI-assisted memorandum, not a commissioned journal review.

The addition is explanatory, as the referee states: the earlier finite theorem already retained the corresponding forward bias. The new area anchor is different in this respect: it is exact at finite flight count and does not substitute the limiting clock for the finite residual. Its finite estimator nevertheless pays the forward error when identifying contact geometry from finite densities.

## R72-M6 — Realizability, finite preparations and nuisance parameters

The earlier theorem is retained. The new theorem changes the fitted image, rather than attaching an independently estimated scalar to a possibly incompatible reconstructed table. The image is

\[
 \mathcal J_N(T,d)=((f_{N,b}|_Q)_b,\log\pi_{N,b_0})
       \in C^m(Q)^r\times\mathbb R.
\]

A countable dense subset retains an actual representative at every point; the first near-minimizer is measurable. The densities are normalized on `Q_+` and restricted to `Q` **without** renormalizing. The same record supplies both first-success marks and the phase count. A binomial concentration bound controls the logarithmic count; the inherited interior derivative estimator controls the densities. Their events need not be independent. The infinite conditional-mark representation justifies using the first `n` observed successes on the good count event without granting uncharged successes.

The geometric comparison is applied only between the true and selected realizable pairs. Relative twist comparison gives

\[
 |\log(D_N(\widetilde c)/D_N(c))|
 \le C(1+N)\|\widetilde c-c\|,
\]

not a flight-independent bound. The derivative formula proves why this factor can genuinely grow with flight count; it is not offered as a minimax argument. Combining this with the exact central anchor gives the area error. The budget schedule is stopped at the readout floor, avoiding an unnecessary `log B` amplification of a fixed positive readout error. No new preparation group is needed, but no optimal total-sample improvement is claimed. The selector remains an existence result, not an efficient search algorithm. Exact tags, gates and independent resets remain hypotheses.

## R72-E1 — Significance of the combined mechanism

We agree that the strongest case is the combined relative-physical-law and actual-functional-inverse mechanism, not the elementary algebra alone. The revised introduction states the area identity briefly and sends its full proof and statistical use to the new section. It does not count overlapping pages or inherited theorem statements as separate contributions.

The synthesis does more than identify a formal parametrization. Conditioning occurs on an exponentially rare physical event. Relative determinant control prevents normalization from destroying the geometric information. The smooth inverse then identifies actual functions, including differences invisible to every finite jet, without analytic continuation. Finally the charged record recovers the phase-volume scalar that the conditional inverse necessarily omits. Exact locality supplies the reverse implication, so the final object is characterized rather than merely bounded above by a list of recovered coordinates.

The complete-invariant theorem is a consequence of that synthesis, not an independent claim of a new universal inverse method. Its finite reconstruction also exposes a genuinely relevant interface: error in a recovered curvature changes an exponentially rare normalization by a flight-length factor. Retaining this factor, and fitting the entire realizable record, is necessary to make the added geometric conclusion statistically coherent.

These are reasons for considering the combined result at the requested general-journal level. They do not mathematically compel an editorial recommendation. We preserve the target and the proved scope without declaring the significance reservation “closed” by fiat.

## R72-E2 — Rich data and the exact determined object

We agree with the report's description of the data. The observation is local, phase-resolved and marked; the finite experiment has a charged reset budget and differentiated priors. The revised statement does not disguise those features.

The new classification answers a question internal to this observation: exactly which geometric equivalence class does its complete record determine? The answer distinguishes local shape from a global volume scalar and from unobserved remote shape. Success information is neither redundant nor equivalent to an exterior scattering record. This is a positive determination theorem with an exact converse, not a retreat to a smaller contact class. Nontrivial equal-area remote completions show that the recovered object is the entire invariant of the specified experiment, rather than a casually selected subset of potentially observable parameters.

The rate is still sufficient and class-dependent. The added logarithmic factor is stated openly and applies to the enlarged output, while the previously established profile-and-offset estimate remains available. We make no assertion of optimality or efficient computation.

## R72-E3 — No manufactured repair checklist

We have not relabeled unreset trajectories, noisy tags, minimax optimality, an unmarked polygon or whole-table smooth determination as missing hypotheses to be “closed.” The new work uses the existing success/failure record and its physical normalization. It is a relevant consequence, not a mandatory repair the referee supposedly demanded.

The corrected planar comparison is retained unchanged. The article is not claimed to dominate the corrected travelling-time theorem, ordinary marked-length results, or enriched marked-length results on their different data. No additional hypothesis removal from those theorems is asserted. All valid prior scope remains present.

## Presentation suggestions and R72-D1–D4

**Presentation.** Both suggested clarifications are implemented at their mathematical point of use. The new overview theorem is in the introduction; full statements and proofs occupy the new section immediately after the single-law section. The revision number is metadata, not part of the mathematical title. The full technical entry and companion remain available alongside the principal article.

**D1, examined mathematics.** We report what was checked, not a blanket certificate for every retained proof. The new arguments and their operative physical, smooth, quadratic, statistical and locality interfaces were re-examined. The later analytic continuation, full global registration and lattice arguments, moving-family material, older catalogue and companion have been preserved and built but have not undergone a new complete independent line-by-line proof audit in this revision.

**D2, revision response.** The original unreported-offset improvement and its signed-anchor stability are retained. The present response adds the complete charged invariant, the exact area anchor, relative normalization stability and joint actual-table estimation. It does not claim these additions retroactively answer an unmentioned fatal error.

**D3, requested placement.** We request reassessment of the combined mathematical contribution. Acceptance and exceptional significance remain matters for independent editorial and referee judgment. The target has not been lowered, nor is acceptance represented as guaranteed by compilation or finite tests.

**D4, delivery and preservation.** New source and native-product branches isolate this revision. No existing branch, report, permission or default-branch setting is changed. The final reading entry records the actual source commit, native products, preservation verification, mathematical diagnostic scope, and visual inspection performed. It distinguishes a successfully executed build from proof certification; previous reviewers' or authors' work is not silently adopted as fresh work here.

## Locations for the next reading

- `article/10g_uncalibrated_single_law_v72.tex`: exact finite clock paragraph and explicit weighted-order condition; original separation, rigidity and sampling statements retained.
- `article/10h_complete_record_v73.tex`: phase-volume anchor, complete observation fibers, logarithmic twist derivative, finite-record stability, jointly realizable estimator, budget/readout schedule; all proofs included.
- `article/00n_record_overview_v73.tex`: introductory complete-invariant theorem and mechanism.
- `journal/DEPENDENCY_LEDGER_V73.md`: supplied, observed and reconstructed quantities; exact/limiting/finite interfaces.
- `HISTORICAL_DERIVATION_AUDIT_V73.md`, `LITERATURE_CHECK_V73.md`: source lineage and precisely bounded literature check.
- `tools/check_revision_v73.py`: independently written finite algebra, transfer, normalization-negative-control and budget diagnostics, active with and without Python optimization.
