# A2 revision 103 — response to the v102 referee report

**Controlling report:** `reviews/a2-v102-independent-harsh-top4-2026-09-20/REFEREE_REPORT.md`, at `8054ae5d5c318b7e59f9ad42545ae27b416bec09`.

**Reviewed v102 head:** `24feb65d770d2db2cd594989d67d4cca280c91ea`.

**Revision branch:** `revision/a2-v103-finite-sheet-metric-quotients-2026-09-20`.

**New principal:** *Finite-sheet metric contact and spectral quotients of polynomial observations*, `papers/A2-v17-boundary-information-coarsening/article/v103/paper.tex`.

**Principal source commit:** `b50fbbe0ce30856bd1b10cd66ab70351fd8f4295`. **Native-build source commit:** `618b0b098654f53e61a782138272349df92d16ad`.

The report's central objection was mathematical depth and unity, rather than a displayed counterexample to v102. This revision supplies a finite-sheet structure theorem with realization, proves that coupled polynomial cancellations produce its sheets, analyzes the native Hellinger quotient family, and classifies the endpoint quotient. It does not replace these tasks with a change of title or a claim of journal readiness. Every previous mathematical source is inherited unchanged; the new principal gives the proofs used for its own conclusions.

## R102.1 — structure of the metric envelope

**Theorem 2.2, pp. 3–4**, treats a finite union of affine residual sheets `c_b + L_b R^{r_b}` avoiding zero. It proves an exact semidefinite lift of the convex upper tensor envelope using positive moment matrices whose final diagonal entries sum to one. The proof also establishes that this particular linear image is closed: full column rank of `[L_b,c_b]` bounds each positive moment matrix by the trace of its image. Closedness is not assumed for arbitrary spectrahedral projections.

For every positive definite metric, the exposed face is exactly the convex hull of the projected residual tensors of the minimizing sheets. This includes ties. The theorem gives a finite semialgebraic active-branch partition, compact-margin Lipschitz dependence, and a polynomial realization of **every** arrangement in its stated affine-sheet class. **Corollary 2.3** proves closure under independent products and handles coupled observation metrics through the same lift.

This structure is not detached from the inverse problem. **Corollary 3.3** proves that the leading residual set on every nonexact opening arc of the coupled weighted family is precisely a finite union of affine sheets. Consequently its entire metric envelope and positive-metric exposed faces are computed by Theorem 2.2. This is the main link between the contact construction and the cancellation theorem.

The general support-reconstruction fact remains **Proposition 2.1**, with its classical separation proof clearly distinguished from the finite-sheet conclusions. The paper does not claim that the convex envelope recovers nonconvex information invisible to all positive-metric minima.

## R102.2 — the native fixed-Hellinger family and probe information

**Theorem 5.1, pp. 10–11**, derives a rational-moment representation for the degree-d binary model. With four probability cells, the full information at a clock has denominator `Delta=q^3 product_e k_e`, and numerator degree at most `7d`. The moment normalization puts the native information family in an affine space of dimension at most `7d`. A finite design has an information-equivalent representation on at most `7d+1` clocks. This is an information-matrix statement, not a claim that compressed clocks retain global identification.

The theorem explicitly differentiates the profiled native form with respect to design weights. Its derivatives are differences of residual-score Gram matrices, and its image dimension is the maximum rank of this rational Jacobian. Two copies give a finite semialgebraic secant description. Thus the native family is analyzed before a sampling criterion is applied.

**Theorem 5.2, pp. 11–12**, proves for a semialgebraic family of dimension s that

    s <= adaptive exact-ray complexity <= fixed exact-ray complexity
      <= min{k(k+1)/2, 2s+1}.

The upper bound is proved with an incidence-dimension argument for **rank-one legal probes**, not arbitrary linear measurements. The adaptive lower bound retains a positive-dimensional semialgebraic set of matrices consistent with the transcript and does not require continuity of the algorithm. For a fixed centre and `2d+1` clocks on an endpoint-free simple-root pattern, at most `4d+1` queries suffice for `k=2d`. This is strictly fewer than polarization's `d(2d+1)` values for `d>=2`. The bound is not labeled sharp in these general patterns.

**Theorem 5.3, pp. 12–13**, establishes an exact sharp result in the coupled two-variance pattern. The Hellinger metric, clocks `4,5,6,7,8`, weights `1/5`, second channel, and root locations are all fixed. Only `(alpha_1,u_11,u_12)` vary near the displayed full-rank centre. An exact rational first-jet certificate gives a nonzero three-by-three Jacobian determinant, congruent to **933885 modulo 1000003**. Hence the native image contains an open subset of `Sym_2^{++}`. Its secants contain a neighbourhood of zero. Exactly three ray queries are necessary, even adaptively, and the same lower bound applies to the complete decoded spectral fibre. The three polarization rays attain it. A separate exact design-variation calculation has minor **230039 modulo 1000003**.

Appendix B specifies all scores, the profile matrix, the first-jet arithmetic, and the modular denominators. The checker independently computes the rational base information and checks agreement with its first-jet reduction. These are exact certificates for a particular derivative, not floating-point rank estimates.

The oracle model is explicit: the unknown member is supplied by its ray costs, with the family and pattern known. It is not also supplied by its entire numerical centre law and design, which would allow direct calculation of Q without queries. This remains a deterministic model-information theorem, not an empirical sample-complexity assertion. The general moment and dimension bounds and the sharp native two-variance theorem have their stated scopes; the manuscript does not claim an exact query count for every higher-degree pattern.

## R102.3 — classification after invisible endpoint elimination

**Theorem 6.1, pp. 14–15**, gives a finite necessary-and-sufficient equality test for `G_Q=G_Q'`, allowing different endpoint dimensions. On every full-dimensional intersection of their critical cones, compare the corresponding Schur matrices. Equality on those intersections is necessary by polynomial identity and sufficient by density and continuity.

The value function itself defines canonical finite data: merge equal local quadratic polynomials and retain the closures of their maximal locally quadratic regions. These regions may be unions of polyhedral cones; no unjustified uniqueness of a convex subdivision is asserted. The theorem also characterizes the representable range as

    x^T S x + dist(Tx, L R_+^e)^2,   S>0, L invertible,

and proves the converse positive-definite block construction.

**Theorem 6.2, p. 15**, completely classifies the one-endpoint fibres. Writing `u=b/sqrt(c)`, a mixed-sign u gives a nonquadratic value function that determines A and the oriented vector u. The only invisible parameter is positive endpoint rescaling: the equivalence class has dimension one and has a canonical representative with `c=1`; one endpoint is minimal. For a quadratic value function, the theorem gives exactly both sign families of representations, their maximal fibre dimension `r+1`, and the zero-endpoint minimal representative.

These results go beyond asserting piecewise quadraticity. The all-dimensional equality test and range characterization are complete in their terms, while the full fibre-dimension and minimal-representation classification is proved for one endpoint. It is not silently extended to arbitrary endpoint dimension.

## R102.4 — several variables, competing sheets, and vector cancellation

**Theorem 3.1, p. 5**, proves a relative normal-form estimate for several fast equations, a vector residual, and finitely many feasible inverse sheets. The minimum distance is bounded by `(1 +/- K epsilon_t)` times the smallest Schur norm of the **exact** residual vectors C_b. No positive lower bound on those vectors is imposed. Therefore the estimate remains valid at exact cancellation and on moving paths approaching a wall. The proof supplies localization of every global minimizer and a feasible upper trial, rather than evaluating one selected branch.

**Theorem 3.2, pp. 5–6**, verifies every chart, radius, localization, and small-shear hypothesis for weighted polynomial systems with fast equations `x_i^{m_i}-t eta_i` and a coupled polynomial vector G. The exact branch residuals include all feasible inverse signs; the relative error is `O(t^{nu-1})`, where the smallest slow weighted degree is `nu>1`.

**Corollary 3.3** identifies the complete leading residual set and its metric envelope along each nonexact semialgebraic path. **Example 3.4** has two fast equations and two coupled residual coordinates, with a union of codimension-two exact walls. **Theorem 3.6** realizes the class by uniformly strictly positive probability observations and derives the Hellinger normalization and its relative error.

The former scalar family and both crossover laws remain in **Corollary 3.5**, with their full earlier derivations preserved in the supporting volume. The new theorem is a proved multivariable class, not a claim that every polynomial stochastic singularity has the stipulated fast normal form. A nonzero equality of leading distance and radius still requires the exact sign or higher-order analysis preserved from the earlier article.

## R102.5 — precise relation to prior literature

The introduction gives a theorem-level separation between inherited machinery and the added conclusions. The primary sources were checked as follows:

| Source | Classical ingredient used | Conclusion not attributed to that ingredient alone |
|---|---|---|
| Boyd–Vandenberghe, *Convex Optimization* (2004) | Separation, positive semidefinite order, Schur minimization | Finite-sheet realization and the exposed-tensor description for the cancellation family |
| Bemporad–Morari–Dua–Pistikopoulos, *Automatica* 38 (2002), Theorem 4 and Corollary 1 | Piecewise-affine optimizer and piecewise-quadratic value for parametric QP | Equality classes, canonical value-function regions, and the complete one-endpoint classification |
| Bochnak–Coste–Roy, *Real Algebraic Geometry* (1998), Chapters 2 and 9 | Semialgebraic dimensions, fibres, and stratification | The native rational-moment family, the fixed-experiment rank witness, and the resulting native query conclusions |
| Lejeune-Jalabert–Teissier, with Risler, arXiv:0803.2369 | Integral closure, arc orders, and real-analytic contact exponents | The positive-metric residual tensor data and cancellation-relative vector coefficients |
| Ha, *An algebraic theory of Lojasiewicz exponents*, arXiv:2602.18410v1 (2026) | Valuative finite-max principles and exponent wall-chamber analysis | Exact canceled vector residuals, positive-metric exposed tensors, and competing inverse-sheet coefficients |
| Bierstone–Milman, *Publ. Math. IHES* 67 (1988), Theorem 0.1 and Corollary 4.9 | Proper real-analytic uniformization and normal crossings | The explicit feasibility-preserving reduction and unit bookkeeping in Appendix A |

The dimension incidence argument is presented with a proof using classical semialgebraic geometry; it is not represented as a newly discovered general dimension theory. The article's native-model contribution is the structure and concrete realizability of the quotient family to which it is applied.

## R102.6 — a proper feasible real presentation, with exact references

**Theorem A.1, p. 16**, supplies an actual existence argument, not an undefined requirement that an appropriate atlas be available. First apply Bierstone–Milman Theorem 0.1 to the compact closed subanalytic feasible set. Properness makes the source compact; removing components with identically zero time still covers the closure of the positive-time image. Next apply their Corollary 4.9 to the single analytic function `t sum_i R_i^2`. This produces normal crossings through a proper surjective real analytic map.

The proof derives monomial factors for time and the residual vector separately. Noncancellation of real squares makes each residual coordinate divisible by the common half-order monomial and leaves a vector unit bounded away from zero. Compact boxes split into real orthants supply finite coverage, uniform unit bounds, and the stated transverse positive-time accessibility. Feasibility is retained through the uniformizing map, not inferred from complex exceptional points.

This is an analytic presentation sufficient for the order computation; it is not mislabeled a Nash map. **Proposition A.2** proves that it computes the intrinsic exponent and metric unit maxima. The exponent formula is identified as classical, while its metric coefficients recover the intrinsically defined envelope.

## R102.7 — explicit whole-model Hausdorff proof

Section 4 now separates the argument into **Lemma 4.1** (exact coefficient inverse and uniform control), **Lemma 4.2** (cluster estimates, score remainder, and feasible root realization), and **Theorem 4.3** (quotient cost and both Hausdorff inclusions).

The inverse proof displays the second-marginal divisibility calculation and its Bezout step. The cluster proof bounds sums by `O(t)`, repeated centred displacements by `O(sqrt(t))`, and one-sided endpoint displacements by `O(t)`. It constructs prescribed retained variances and endpoint sums exactly. The final proof gives the two radial factors and explains why they preserve cone boundaries. Finally compactness and exact identification exclude all unseen whole-model components.

The rates remain `O(sqrt(t))` in the repeated regime and `O(t)` in the linear regime, uniformly on compact fixed-pattern strata with the specified strict margins. No cross-stratum continuity of the marking is assumed. This expands and organizes the proof; it does not weaken the prior whole-model conclusion.

## R102.8 — executed checks, native pipeline, and the evidence boundary

The new **18-page principal** was compiled locally with native pdfLaTeX/latexmk, both directly and through its repository wrapper. The two rendered outputs agree page by page. All pages were rendered and visually inspected through contact sheets, with enlarged checks of the title page, rank-certificate page, real-presentation proof, and arithmetic appendix. The final logs have no undefined references or citations, multiply-defined labels, overfull or underfull boxes, or LaTeX warnings. The principal source, exact checker, and native builder blobs were read back from GitHub and match their local bytes.

`EXACT_DIAGNOSTICS.json` records the executed rational and finite-field rank certificates, the independent base-information cross-check, probability normalization and positivity, eight coupled polynomial substitutions, twelve endpoint-rescaling checks, and the affine projection and moment identities. `LOCAL_VALIDATION.json` records the exact source and PDF hashes and the scope of local validation. None of this is advertised as formal verification of the universal proofs.

The branch-scoped workflow was triggered at **618b0b098654f53e61a782138272349df92d16ad**, run **35504308437**. Its builder recursively rebuilds available PDF-source dependencies using the inherited literal dependency walker, binds source bytes to the triggering commit, verifies the addition-only diff, checks all native logs, and distinguishes hashed binary-only dependencies. Native recorder inputs add styles and other repository-local dependencies to the manifest. The workflow publishes a durable receipt and four volume targets on this branch only after successful execution and a source-drift check.

**At this response's preparation, that full-graph run was queued. The full archival graph has not been executed locally, and no v103 full-graph success is claimed. R102.8's full-runtime evidence requirement therefore remains pending the actual successful receipt.** A workflow definition, an old v98 artifact, and this local principal receipt are not substitutes. The authoritative full-build evidence, once produced, is `revisions/a2-v103/native/RUNTIME_RECEIPT.json` with `status=native_passed`, together with its source head and output hashes.

## Full preservation and referee entrypoints

| Volume | Entrypoint in `papers/A2-v17-boundary-information-coarsening/` | Content |
|---|---|---|
| Principal | `rigidity_v103.tex` | New self-contained article |
| Supporting | `rigidity_v103_supporting.tex` | Complete v102 principal, unchanged |
| Archive | `rigidity_v103_archive.tex` | Complete v102 principal and its complete inherited mathematical record |
| Complete | `rigidity_v103_complete.tex` | v103 principal followed once by the full archive |

The supporting article is already inside the archive and is not inserted twice. `CONTENT_PRESERVATION.md` maps the earlier arguments to these volumes. The source comparison against the controlling review contains only additions; no previous manuscript, review, derivation, or other branch is edited. Subsequent documentation-only commits do not change the compiled principal or the native trigger's mathematical sources.

For the new mathematical argument, read Theorems **2.2, 3.1, 3.2**, Corollary **3.3**, Theorems **4.3, 5.1–5.3, 6.1–6.2**, and **A.1**, with their proofs. Appendix B supplies the finite native-rank certificate; the complete historical record remains available for every retained earlier result. Mathematical significance and suitability for a top-four journal remain questions for the next independent referee, not conclusions of the build system or this response.
