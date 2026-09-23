# Response to the independent v12 referee report

**Manuscript:** General Theta Foundations I: Intrinsic Causal Deficiency and Finite-State Decisions  
**Revision:** v13, 23 September 2026  
**Controlling report:** `a03a574936230aedbe1a8d3f4cb5b1fbd9c8ceb3`, report blob `69fd7069f0902ef6d17790c388fd51322407b7bf`  
**Reviewed v12 head:** `a9f8e05640e8bb100178a3216fa6165482ca4676`  
**New branch:** `revision/general-theta-foundations-i-v13-intrinsic-deficiency-2026-09-23`

We thank the referee for distinguishing the results established in v12 from the remaining structural questions. The revision is organized around an intrinsic optimization over simulators, rather than adding a further parallel family of model interfaces. Its canonical article contains five sections; the entire previous development remains in the complete companion. The discussion below uses stable theorem labels; the build receipt gives the final printed numbers and pages.

## E12.1 — Intrinsic resource-deficiency spectrum

**Response: a new main theorem, with an explicit distinction between a private inverse and a priced convex converse.**

`intrinsic-deficiency.tex` defines the infimum of actual marked feedback error over all task- and parameter-blind causal transducers with prescribed persistent widths. It defines private, hidden-selector, and visible-selector spectra separately. This is an optimization over the simulator itself, not a cost attached to a supplied simulator. Unused states can be added, giving an upward-closed resource set; no unjustified unique coordinatewise minimum is presumed.

Theorem `thm:v13-main` proves attainment for finite experiments, a polynomial characterization of private and fixed-selector feasibility, and the exact hidden-mixture minimax/testing dual. Its simulator columns preserve the common encoder across every parameter, feedback tree and marked event. The converse supplies an actual realization with at most a_K+1 selector values, where a_K is the affine dimension of attainable behavior. If the index must be privately retained, its cost is (a_K+1)K. Composition optimizes both stages and yields the multiplicative-width/additive-error deficiency inequality.

The visible-selector optimization is different. Its objective is max_theta sum_u lambda_u e_theta(q_u), because the feedback test can depend on the revealed selector and the selector remains in the compared law. Its optimized zero set equals the private zero set. By contrast, a hidden mixture can reach zero outside that private zero set. This distinction is proved, not assigned as a convention after convexification.

Proposition `prop:v13-rank` gives a concrete intrinsic slice. A delayed stochastic channel has exact K-state private simulation precisely when its nonnegative rank is at most K. For the n-symbol identity channel the exact private error is 1-1/ceil(n/K), while hidden convexification gives 1-K/n. Their inversions give the minimum required widths at each tolerance. The three-symbol rank-three channel V=(1/2)I+(1/6)11^T has an exact hidden three-mode/two-label realization but positive private two-label deficiency, with an explicit lower bound. Thus an ordinary convex testing dual cannot be claimed to give an unpriced same-width private implementation. The theorem gives a positive priced converse together with the exact private variational problem and signature-dependent zero sets.

## E12.2 — A hard infinite boundary

**Response: a nonsummable average-risk theorem with a proved uniform ergodic mechanism.**

Section `sec:v13-regeneration` treats stationary common finite-register controllers on a standard Borel physical space. Between resets its physical transitions may be deterministic or singular; no common dominating physical transition measure is required. A physically supplied independent reset refreshes the preparation and clears the within-policy register. This is a declared control/resource interface, not an assertion that hidden-plant mixing automatically mixes the retained register.

Theorem `thm:v13-average` constructs the unique invariant law explicitly as a geometric cycle mixture. It proves uniform total-variation contraction, a Cesaro error at most 1/(N eta), and a normalized-discount error at most (1-beta)/(1-beta(1-eta)). These estimates establish actual nonsummable average risks, compact uniform risk images, and attained common-design minimax duality. The exact policy class is stationary finite-register policies with synchronous resets. We do not infer optimality over unrestricted nonstationary policies.

Theorem `thm:v13-cycle` then transfers finite-age marked comparisons to the average criterion. Pointwise-in-age approximation is sufficient because the geometric cycle tail is uniform before optimization; the bound is uniform over every consumer width. An explicit rotation-with-reset example has a nondominated physical transition family. The old summable infinite-horizon theory remains available unchanged in substance and is explicitly identified as summable in its locally annotated heading.

## E12.3 — Endogenous controlled compression

**Response: a new exact characterization for policy-dependent supports and a quantitative lossy relation.**

Section `sec:v13-controlled` starts from a finite controlled history tree with task-dependent stage costs and the full-history Bellman values. The controller knows its task; the shared encoder does not. Different tasks generate different supports. Definition `def:v13-cover` uses task-indexed reachable cells and task-specific actions, but only one initial encoder and one successor update for all tasks. It requires successor closure under the chosen action and actual positive-probability reports, not all hypothetical open-loop controls.

Lemma `lem:v13-regret` gives the exact occupation formula for excess risk. Theorem `thm:v13-endogenous` proves that an exact common design exists if and only if the corresponding reachable compatible cover exists; private and independent seeded randomization do not enlarge the zero face. The proof fixes entire time-indexed row tables simultaneously across tasks and uses nonnegative Bellman regrets, not a claim that every positive minimax optimum is deterministic.

The same theorem gives a positive finite-table infeasibility witness and an approximate-cover upper bound. Equation `eq:v13-lossy` identifies the hidden-selector lossy common-risk optimization, with the selector priced if privately stored. Corollary `cor:v13-certificate` ties the cover face to intrinsic stateless deficiency and a stable decision threshold. The example with an optimal rest action and an unused probe branch shows that this is not merely the earlier restart theorem with different notation.

## E12.4 — Active physical control or a hard historical closure

**Response: the active-control alternative is implemented and proved; it is not relabeled as the other alternative.**

The new physical model applies an orthogonal intervention to particle velocities and then runs the actual hard-sphere flow. Choosing identity versus velocity reversal changes the subsequent positions on a positive-measure collision-free set. Thus the actions change microscopic dynamics; they do not only select an observable of a fixed path.

Lemma `lem:v13-words` proves controlled-word convergence for graph-core Galerkin approximations followed by projected intervention operators. The interventions need not preserve the generator domain. The proof uses bounded compositions and stable graph-core resolvent approximation, with a precise citation to Trotter's original Theorem 5.2 and a self-contained contraction argument.

Theorem `thm:v13-active` constructs an actual noisy observation experiment from the finite-dimensional matrices. It preserves the actual initial physical mark through its joint push-forward, not by an independent marginal resampling. Its comparison bound sums over controlled words under the original L2-bounded preparation; it does not assume feedback preserves posterior L2 bounds. The result is two-sided and stateless at the report interface and therefore uniform over every consumer width and independent exposed seed.

Corollary `cor:v13-active-average` combines this active microscopic construction with the new regenerative theorem. The approximate physical vector dimension is separate from consumer label cardinality. All particle numbers, action alphabets and noise levels are fixed in the assertions. We do not claim that this proves the historical nonlinear B4 action-sublevel corrector, a Boltzmann–Grad limit, or the A4 left-strip spectral estimates. Those targets and their source files are retained as distinct mathematical tasks. This response takes the referee's active physical-control route, rather than claiming the historical alternatives have also been completed.

## E12.5 — Original-source nearest-neighbour comparison

**Response: theorem-level comparison strengthened, but this request is not fully closed.**

The common-information original was inspected at Theorem 3 and Corollary 5, including the no-common-information finite-memory specialization. Its dynamic program is explicitly credited. Trotter's original Theorem 5.2 and proof passage were obtained and visually inspected. The domain-conscious Mori paper was reread at its semigroup construction and Theorem 2.5 context. The article does not claim novelty for any of those ingredients.

Fresh retrieval attempts at the Norberg DOI/publisher PDF, its national-library preprint record, and the Paull–Unger original IEEE PDF/record did not yield accessible full texts. The Norberg author abstract and bibliographic record were available; the IEEE record identified the original but the full-text endpoint failed. We therefore cannot honestly mark their proof-level comparison complete. `LITERATURE_COMPARISON.md` distinguishes retrieved theorem text from metadata/abstract and gives the exact unresolved questions. No invented theorem numbering, quotation, or assertion of absence from an unread original has been substituted.

The v13 contribution is stated positively as the exact signature-indexed theorem proved here. Priority of that entire conjunction remains for independent scholarly comparison. This unresolved priority audit is a substantive remaining review item, not hidden by successful compilation or a comparison table.

## E12.6 — Frozen dependency graph and freshness

**Response: separated mathematical structure from remote branch observation.**

`PIPELINE_GRAPH.json` preserves all eleven historical components and all inherited proof/adapter records. New proof edges have explicit labels and hypotheses. It does not infer sequential dependence from A1/A2/etc. names. The primary algebraic-geometric A2 line remains an independent branch of the mathematical graph; its decision adapters are separately typed.

`REPOSITORY_SNAPSHOT.json` records the fresh remote observations. The branch named `revision/a2-v131-relative-primary-filtrations-2026-09-23` was observed at `57c70a882150cc6e44d85ad6f68043b7327d8a10`. Importantly, that commit is the v130 referee report, not a materialized v131 article. The putative v131 geometry entry was absent; the actual v129 geometry entry used by v130 was read and its blob recorded. The snapshot therefore does not mistake a newer branch name for a newer completed theorem.

The build checks graph identities and label existence. It does not certify a theorem dependency merely because a JSON edge is well formed.

## E12.7 — One focused canonical article without erasing the development

**Response: the canonical article has been reorganized, not expanded by another parallel block of twenty pages.**

The canonical manuscript has five sections centered on intrinsic deficiency and its endogenous/active consumers. It includes complete proofs of its stated new results and the classical graph-core argument it actually uses. Its source is `main.tex`.

The complete companion starts with precisely those same sections and then includes the entire v12 canonical mathematical core and the earlier bodies v12 preserved. Every original source file in the 290-entry inherited closure remains byte-identical. All predecessor companion labels are checked during the build. The only changes to predecessor text occur in two new local annotated copies, and the exact additions/heading adjustment are documented. Nothing is deleted from the repository or silently dropped from the full development. The former Gaussian, filtering, nonfinite duality, marked quotient, synthesis, operator-memory, and pipeline material therefore remains available for review without competing with the new main theorem in the canonical article.

## E12.8 — The theorem-sized remainder after classical ingredients

**Response: stated as a precise mathematical conjunction, not a universal priority assertion.**

The finite minimax interchange, Caratheodory reduction, Bellman telescoping, nonnegative factorization, geometric regeneration, and stable semigroup convergence are classical tools. They are not the claimed remainder.

The statement to evaluate is Theorem `thm:v13-main` with Proposition `prop:v13-rank` and its consumers: for a common task/parameter-blind causal transducer, the optimal marked feedback error at specified persistent resources has an exact hidden testing converse with an explicit state price; exposing the selector changes the variational problem and forces the private zero set; the optimized resource spectra compose and transport endogenous common decisions. The active microscopic corollary supplies a nonfinite physical realization of that before-optimization transport, including a nonsummable criterion.

The rank-three example exhibits the phenomenon rather than leaving it at framework terminology. It makes clear which conclusion cannot be obtained by merely forgetting the resource signature in ordinary convex comparison. Whether the exact conjunction has the scale and priority required by the requested journals remains a referee question. We submit the proofs and precise comparison category, not a self-issued acceptance judgment.

## Specific technical comments 12.1–12.12

| Comment | Action in v13 |
|---|---|
| 12.1 Task exactness versus experiment equivalence | The endogenous theorem concerns its declared Bellman tasks. The intrinsic deficiency theorem separately tests the full actual marked transcript. No identification is made without decision completion. The earlier continuation-event completion is retained in the companion. |
| 12.2 Finite margin | The new witness explicitly depends on least positive initial/transition probabilities and Bellman regret. A remark states that it need not remain positive uniformly under model perturbation. |
| 12.3 Infinite-prefix effectiveness | The manuscript explicitly distinguishes compact inverse-limit existence from a computable infeasibility horizon. No bound on a first failing prefix is asserted. |
| 12.4 Summable heading | A local annotated copy changes the old heading to “Summable infinite-horizon common-encoder duality,” preserving its label and proof. The original file is unchanged. |
| 12.5 Seed dimension | Proposition `prop:v13-dimension` replaces row covering numbers by a finite-rank approximation of the attainable risk image. Exact affine dimension m gives m+1 designs; approximation error eta gives uniform risk error 2 eta. |
| 12.6 Intrinsic cost | The simulator itself is optimized in each deficiency definition; the delayed-channel formulas invert to exact least state budgets. |
| 12.7 Differentiability | The preserved memory proof now explicitly says the projected derivative comes from its bounded block integral formula, not differentiation of an arbitrary full orbit outside D(L). |
| 12.8 Semigroup priority | Trotter 1958, Theorem 5.2, p. 902, is cited both in the new graph-core proof and in the locally annotated predecessor proof. |
| 12.9 Width uniformity | Fixed particle number, action alphabet, step size, positive noise, and observable family are stated. There is no uniformity claim in growing physical alphabets or kinetic/noiseless limits. |
| 12.10 Row dependence | New and annotated physical statements specify that the preparation and losses vary; flow, interventions, noises, observable presentation, and actual mark channel stay fixed unless additional continuity is verified. |
| 12.11 Passive scope | The retained passive theorem begins with an explicit fixed-flow scope sentence. The new active theorem is separate and does not claim a nonlinear kinetic limit. |
| 12.12 Evidence rhetoric | Diagnostic counts and hashes are confined to source/evidence documents and the build receipt, not used as mathematical proof arguments in the article. |

## Submission status

The new finite and analytic arguments are offered for independent scrutiny under their stated hypotheses. The original-source comparison in E12.5 remains incomplete; the unrestricted historical kinetic and spectral targets remain separately recorded. These limitations are not used to discard the ambitious research program, change old statements in place, or represent engineering checks as proof. The new revision supplies the optimized comparison theorem and its new consumers, with the entire prior development preserved.
