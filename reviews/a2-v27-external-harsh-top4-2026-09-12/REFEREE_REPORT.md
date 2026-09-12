# Independent referee-style report on A2 v27

**Manuscript:** *Boundary laws, intrinsic periodic rigidity, and global physical reconstruction in dispersing billiards*  
**Author:** Qian Qi  
**Revision branch:** `revision/a2-v27-observed-type-smooth-jets-top4-2026-09-12`  
**Reviewed commit:** `17d71b721f0c5b006b52ec3fbe244866221ee93f`  
**Reviewed tree:** `ef48921175759a1ca7f2435d2215b765b4d17a03`  
**Mathematical-source commit:** `416124f13f182f8e2d876f93090865f13269c86b`  
**Previous review:** v26, commit `a5b2d4b5a9ed31059e16e5011c8010579d713598`  
**Native entry:** `papers/A2-v17-boundary-information-coarsening/main.tex`  
**Review branch:** `review/a2-v27-external-harsh-top4-2026-09-12`  
**Date:** September 12, 2026.

This is an author-requested, AI-assisted independent referee-style assessment against the standards sought for Annals of Mathematics, Inventiones Mathematicae, the Journal of the American Mathematical Society, and Acta Mathematica. It is not a commissioned report, an editorial decision, or an assertion of institutional affiliation. It concerns the pinned A2 manuscript, not statistical A1 or the complete theta-theory programme. The accompanying [source audit](SOURCE_AUDIT.md) specifies the material actually inspected and the limits of verification.

## Recommendation

**Revision required before an acceptance recommendation. The principal mathematical objections raised against v26 are satisfactorily repaired in the inspected v27 text. No fresh major mathematical objection to the core inverse has been established by this review.**

That distinction is essential. A harsh referee must not manufacture a replacement objection whenever the author fixes the previous one. The observed-contact error has been corrected in the active proposition and introduction, and the finite-jet argument now treats arbitrary smooth remainders rather than only polynomial coefficient variations. These are substantive repairs, not concessions confined to an author response.

I nevertheless withhold an acceptance recommendation for the submission as delivered. There is still no successful complete native build and recursive reference verification of the assembled submission in the evidence examined. There is also a narrowly scoped mathematical formulation issue in the inherited statement about forgetting transverse signs: a common orientation quotient must not be conflated with pointwise deletion of signs. These outstanding requests are specified in Sections 5 and 6. They do **not** amount to a new counterexample to the main signed inverse, a demand to abandon the programme, or a demand for an unrelated replacement theorem.

The appropriate reading of this recommendation is therefore **minor mathematical clarification plus completion of submission validation**, not a renewed verdict requiring major mathematical reconstruction. The exceptional significance threshold of a particular top-four journal remains a separate judgment. Neither a repaired proof nor a large collection of successful finite checks certifies that threshold.

## 1. Scope and disposition of the preceding report

The branch search located v27 as the latest named A2 revision. The compared head is three commits ahead of the preceding review tip and has no divergence from it. The delta replaces three active mathematical inputs, adds a support-versus-density subsection, updates navigation and provenance, and supplies verification tools and records. The historical mathematical files are preserved. The entry point still includes the auxiliary compendium; this review does not mistake the four changed modules for the complete submission. [S1–S3]

I read the four changed mathematical modules, the full single-offset inverse, the signed half-line and finite-jet proof, and selected substantial inherited dependencies. These include intrinsic gluing and rank-two recovery, finite-signature stability, the explicit two-sided Poisson comparison, and the single-offset global acquisition argument. Other inherited sections were sampled rather than independently recertified in full. In particular, I have not independently checked every theorem in the 36-input auxiliary compendium, every forward relative-law dependency, or the companion manuscript. The audit is deliberately explicit about this distinction.

| v26 issue | Finding in v27 | Disposition |
|---|---|---|
| Position singularity claimed without specifying the observed obstacle | The corrected proposition distinguishes the varying and fixed observed types and defines matched records | Closed in the inspected active statement and proof |
| Infinite Taylor equality used for arbitrary smooth graphs | Finite Taylor remainders and a functional interpolation-envelope lemma are supplied | Closed in the inspected finite-jet argument |
| Stale version navigation and missing current response | The root entry, source manifest, and response identify v27 and its immutable sources | Substantially closed; the manifest is not itself a recursive audit |
| Whole-native compilation and full reference verification | Two observed jobs failed before executing any step | Still open; not a demonstrated TeX error |
| Distinguishing an intrinsic inverse from exact-position sampling | The introduction and inherited inverse keep the observation maps separate | No renewed objection on the inspected statements |
| Prescribed budgets and a diverging minimum flight number | The inherited construction runs the chosen stage afresh | No renewed objection |

I do not reopen the already repaired common-domination, missing-onset-coordinate, cap-conditioning, or finite-signature uniqueness objections. Their corrected mechanisms remain visible in the sources inspected. [S4–S12]

## 2. Observed-contact dichotomy: the correction is mathematically sound

### 2.1 The records are now matched

The active comparison defines a successful scalar record as `(u,v)` and the corresponding position record as `(X_{b,lambda}(u),X_{b,lambda}(v))`. Both delete residual time. Neither retains intermediate impacts or waiting counts. A separate remark retains residual time in **both** records and uses the embedding times the identity. The claims are conditional on successful marks, not statements that preparation failures can be ignored in the unconditional protocol. This resolves the observation-space ambiguity behind the v26 error. [S4, `prop:v27-observed-type-dichotomy`, `rem:v27-matched-time`]

### 2.2 The maximal deficiency proof is stronger than a pairwise argument

The new abstract lemma is correct. Suppose `P_lambda << nu` for a single probability measure, while the target laws have pairwise disjoint measurable full-probability events `A_lambda`, indexed by an uncountable parameter set. For a parameter-independent Markov kernel `K`, all simulated laws satisfy `K P_lambda << K nu`. A probability measure charges at most countably many disjoint measurable sets. Consequently there exists a parameter for which

\[
 (KP_\lambda)(A_\lambda)=0,
 \qquad Q_\lambda(A_\lambda)=1.
\]

With the manuscript's total-variation convention, the worst-case error of every kernel is exactly one. Taking the infimum over kernels preserves one. No integration over an uncountable index set and no parameter-dependent reconstruction kernel is used. [S4, `lem:v27-dominated-disjoint`]

The geometric application supplies the required events. A strictly convex body homothetically dilated about a boundary point has, on every ray entering the body from that point, exactly one further boundary intersection. Distinct positive dilation factors therefore give boundary curves meeting only at the anchor. An arclength-density endpoint has no atom at the anchor. When the first retained endpoint belongs to the varying obstacle, removing that anchor gives the pairwise disjoint full-probability events required by the lemma. The scalar family is dominated on a common bounded transverse box, including after every fixed finite product. Thus

\[
 \delta(\mathsf E_{\rm sc}^{(k)},\mathsf E_{\rm pos}^{(k)})=1,
 \qquad
 \delta(\mathsf E_{\rm pos}^{(k)},\mathsf E_{\rm sc}^{(k)})=0
\]

for every finite `k >= 1`. The same events also exclude a common sigma-finite dominating measure for this position family. This is an exact statistical comparison, not a conclusion extracted from numerical examples.

### 2.3 The fixed-contact case is equally important

When the even design starts at the fixed obstacle, both retained positions lie on one fixed graph. Its graph embedding and transverse projection are parameter-independent inverse maps on the supported boxes. Therefore the matched experiments have Le Cam distance zero. The embedding is allowed to depend on the fixed graph: that graph is a known constant of this particular statistical family, not its unknown parameter.

The density

\[
 f_{\lambda,b}(u,v)=Z_{\lambda,b}^{-1}A_{\lambda,b}(u,v)
                         (d-E_{J,\lambda,b}(u,v))_+
\]

also gives a common positive region. Smooth finite-flight dependence, positive flux, and `E_{J,lambda,b}(0,0)=0` provide a uniform small square with excess below `d/4`. On the fixed graph, its image is a common positive-density region. The position laws are not mutually singular. The disk example is now correctly included as a witness for this case rather than incorrectly assimilated to the varying-endpoint case.

**Disposition:** the previous false-as-written proposition is repaired, and the strengthened dichotomy should be retained. Its scope must remain the stated homothetic family and matched record level. It is not a universal statement about arbitrary position experiments or about reconstruction of an arbitrary analytic boundary from one point.

## 3. Finite smooth remainders: the missing argument is now present

### 3.1 Finite Taylor statements replace an invalid functional equality

The active signed-rigidity section now writes, for each finite order `M`,

\[
 \psi_b(y)=\sum_{n=2}^{M}\frac{q_{b,n}}{n!}y^n+R_{b,M}(y),
 \qquad
 |\partial_y^rR_{b,M}(y)|\le C_M|y|^{M+1-r}.
\]

The corresponding finite differentiability bound is stated. No equality of a smooth function with a convergent infinite Taylor series is asserted. More importantly, this is accompanied by an actual proof that the finite action jet is independent of the remaining smooth function. [S5, `eq:v22-general-contact-jets`, `lem:v27-smooth-jet-factorization`]

### 3.2 The interpolation proof treats the function, not merely its coordinates

Let two graph pairs have the same gap and the same graph jets through order `M`. Interpolate their graphs linearly. On a common small interval, the anchors and strict convexity persist; the equal quadratic jets leave the quadratic half-line operator fixed. The weighted inverse supplies

\[
 |x_i^{(b,t)}(u)|\le C|u|\rho^i,
 \qquad 0<\rho<1,
\]

uniformly in the interpolation parameter. This is a local graph argument. It does not require every interpolated graph pair to extend to a globally admissible periodic table.

For one flight, at fixed endpoints,

\[
 \partial_t\ell_{r,t}(y,z)
 =\frac{h_{r,t}(y,z)}{\ell_{r,t}(y,z)}
       \bigl(\Delta\psi_r(y)+\Delta\psi_{1-r}(z)\bigr).
\]

The factor lies between zero and one; equality of the graph jets bounds the bracket by `C_M(|y|^{M+1}+|z|^{M+1})`. Differentiating a **finite** truncation cancels every interior orbit variation by stationarity. The fixed initial endpoint contributes nothing. The terminal term tends to zero as the product of two weighted decaying factors.

Integrating the finite identity in `t` before sending the truncation length to infinity is the correct justification. The summable direct-variation majorant yields

\[
 |S_b^{[1]}(u)-S_b^{[0]}(u)|
 \le \frac{C_M}{1-\rho^{M+1}}|u|^{M+1}.
\]

Since the actions are `C^M`, their derivatives at zero through order `M` agree. This closes the logical gap between polynomial jet-coordinate differentiation and arbitrary smooth remainders. I find no need to restrict this finite-jet conclusion to analytic contacts.

The uniformity statement is also appropriately delimited. Functional graph-norm bounds and positive geometric margins are required. A bounded list of coefficients alone is not used to assert uniform bounds for arbitrary smooth representatives. Polynomial representatives with cutoffs are introduced only after representative independence has been established. The flat perturbation example correctly illustrates equality of every finite jet without equality of the smooth functions.

### 3.3 The determinant-one recursion survives the repair

The last-jet block follows from the exact envelope formula and homogeneous degree isolation. A new graph coefficient of order `n` enters at endpoint degree `n`; nonlinear orbit corrections raise that degree. The linear orbit has even coefficients `exp(-i gamma)` and odd coefficients `r_b exp(-i gamma)`. Counting the starting boundary site once and interior sites twice gives

\[
 1+2\sum_{k\ge1}e^{-2n\gamma k}=\coth(n\gamma),
 \qquad
 2\mathfrak r_b^n\sum_{k\ge0}e^{-n\gamma(2k+1)}
       =\mathfrak r_b^n\operatorname{csch}(n\gamma).
\]

The product `r_0 r_1=1` then gives determinant one. Affine dependence on the new jet follows because the degree-`n` coefficient uses only the quadratic linearized orbit. The leading curvature inversion and these successive blocks form an invertible finite block-triangular differential.

This proves a **fixed-order** inverse on compact positive finite-jet sets. It does not supply an order-independent infinite-dimensional condition number, and the revised introduction correctly declines to infer one. Analytic continuation enters only after the contact jets have been recovered; it is not used to justify the smooth finite-jet calculation.

**Disposition:** R2 is closed in the inspected revised proof. This review does not turn that conclusion into an independent certification of every inherited forward estimate used to define the action.

## 4. Main dependency chain and mathematical contribution

### 4.1 The amplitude-free one-offset inverse

For the interior density

\[
 f(u,v)=Z^{-1}B(u)B(v)(d-S(u)-S(v)),
 \qquad t(u)=\frac{S(u)}{d-S(u)},
\]

the four-density ratio satisfies

\[
 R_f(u,v)=\frac{f(u,v)f(0,0)}{f(u,0)f(0,v)},
 \qquad 1-R_f(u,v)=t(u)t(v).
\]

A fixed nonzero anchor has `t(a)>0`, so it determines `t(u)` and hence `S(u)`. The manuscript correctly distinguishes a density's uniquely determined continuous version from point values directly supplied by finite observations. It also avoids differentiating a square root at the degenerate action minimum: only the scalar anchor root is used. The fixed-interior `C^M` stability argument follows from positive denominators and the elementary product and reciprocal estimates. [S6]

The finite-flight argument controls the normalization integral as well as the unnormalized density. The estimate uses a fixed positive offset and an interior square, not an unjustified inference of high derivative control from total variation. The separate onset gap is retained. I found no contradiction in these inspected statements or in their composition with the repaired finite-jet inverse.

### 4.2 The new support example has the right, limited force

The transformation

\[
 \phi_\epsilon(s)=s+\epsilon s(1-s)(s-1/2),
 \qquad \widetilde S(u)=\phi_\epsilon(u^2),
\]

is increasing on `[0,1]`, obeys `phi(1-s)=1-phi(s)`, and gives a strictly convex action for the stated parameter interval. Consequently it preserves the one-offset support while changing the four-density invariant. The printed lower bound for the transformed second derivative is positive. [S7]

This is a valid distinction in the **functional action-density class**. It is not a constructed pair of physical billiard tables with identical unsigned or support-only data. The author now states that limitation expressly. It would be incorrect for either author or referee to promote this toy comparison into an unproved physical nonidentifiability theorem.

### 4.3 Intrinsic gluing and finite signatures

The fixed-Gram formulation and the later metric-free rank-two formulation are not inconsistent: the latter explicitly strengthens the former. Two independent marked deck displacements need only form a real basis, not a primitive integer basis, for `L=VM^{-1}` to recover the Euclidean realization. The nontrivial geometric inputs are the recovered complete framed curve images and their unique signature matches; the final matrix identity is not by itself a deep rigidity theorem. [S8–S9]

The finite-signature result does not simply assert that one scalar curvature value has a unique nearby match. It obtains a finite vector immersion using analytic nonconstancy and compactness, then finite-coordinate separation of distant pairs using the absence of orientation-preserving symmetries on transition obstacles. The noisy matching proof requires a `C^2` perturbation and proves strict convexity of the squared residual near the true point. These are the mechanisms needed for the stated uniqueness.

The subsequent compact inverse modulus is logically different. Continuous injection of the compact class gives a uniformly continuous inverse; this supplies a non-effective finite-data consistency argument. It does not provide a well-conditioned unrestricted analytic continuation algorithm. The source keeps these assertions separate. I found no new defect in the portions of this chain inspected. [S10]

### 4.4 Statistical information and physical acquisition

The two-sided moving-ceiling comparison explicitly includes the `O(k^{-1})` **relative** density perturbation on the common bulk. Its reverse kernel reconstructs the layer, supplies reference bulk observations, and randomizes their order. The layer, corner and bulk estimates have distinct roles; trace convergence alone is not being used to deduce product equivalence. [S11]

The scalar common-collar construction also correctly distinguishes common domination of the original family from domination by one reference member. The finite-strip Poisson envelope gives a common dominating probability measure. A support-exclusive event relative to one member does not contradict that fact. The vector LAN section was inspected through its collar construction and the beginning of the expansion; the uninspected remainder is not certified here. [S4, S13]

In the global construction, the final flight number is selected **before** pilot accuracy, gaps enter the separating moment map, and concentration is applied to an uncapped success sequence with cap failure added separately. The budget-indexed policy runs the selected stage afresh. These choices avoid the historical errors they were introduced to repair. The successful transverse tests do not by themselves make the initial unregistered position experiment identical to the intrinsic law experiment; the pilot remains part of its charged acquisition. [S12]

### 4.5 Significance at the requested journal level

The strongest candidate contribution is the combined geometry-specific statement: a sufficiently uniform nonlinear boundary law, its signed all-order contact inverse, and the sharply specified law-valued observation map. The elementary density cancellation is useful, but the journal-level mathematical burden lies in the uniform forward estimates and the contact inversion, not in presenting the cancellation alone as a new general principle.

Analytic continuation, compactness-based inverse continuity, matrix recovery of a lattice from known holonomies, and Poissonization are not independently sufficient claims of exceptional novelty. The manuscript's introduction largely recognizes this. Its comparison with marked-length rigidity explicitly refrains from claiming an unproved inclusion between data maps. The cited marked-length works use different observations and hypotheses, and the cited nonregular-regression work already supplies a Poisson-equivalence precedent. [L1–L3; S14]

The primary-source literature check conducted for this report supports these distinctions. It is **not an exhaustive priority search**, and reading the available abstracts does not establish that no earlier theorem has the same contact-jet block. I make no such priority certificate. I also do not demand a new flagship theorem merely because this revision satisfactorily fixes the previous two defects.

## 5. Required clarification C1: specify the orientation quotient

**Location:** `article/23b_intrinsic_multichannel_rigidity_v23.tex`, final sentence of `thm:v23-intrinsic-table-rigidity`.  
**Classification:** a narrowly scoped ambiguity in an inherited auxiliary formulation; not a counterexample to the main theorem, which retains signed transverse data.

The sentence asserting that, when every transverse sign is simultaneously forgotten, the corresponding statement is modulo `E(2)` needs an explicit data-map definition. Two operations must not be identified.

A **single common reversal of orientation for the entire signed datum** is a quotient by one two-element group. On that interpretation, equality in the quotient means equality of two representatives either directly or after one common reflection. Applying the signed classification to those representatives gives the corresponding globally reflected classification. This is the short argument the author should state if it is the intended meaning.

By contrast, **pointwise deletion of observed signs**, such as replacing `(u,v)` by `(|u|,|v|)`, is a statistical coarsening. For a continuous density its interior pushforward on the positive quadrant is

\[
 f_{\rm abs}(a,b)
   =f(a,b)+f(-a,b)+f(a,-b)+f(-a,-b).
\]

This is not a choice between two globally reflected signed density versions. Independent orientation quotients for separate channel records constitute yet another operation. The signed four-density proof does not automatically invert either of those coarsenings. The observation-hierarchy subsection does not define an unsigned quotient resolving this distinction.

**Requested action:** define precisely the single global orientation action and prove the quotient sentence for it. If the intended claim instead concerns folded endpoint observations or independent channel sign erasures, supply the corresponding identifiability argument and its symmetry hypotheses. Do not rely on the signed theorem alone.

I have not constructed a physical analytic-table counterexample to every possible interpretation of the sentence. Accordingly this is not classified as a demonstrated false theorem. It is a request to make the quantifier and observation map unambiguous. No weakening or deletion of the signed flagship theorem follows from it.

## 6. Required completion C2: provide the assembled native submission

The v27 verification record is unusually explicit about its own limits, which is welcome. It reports a changed-module fixture, a changed-source check, and finite mathematical diagnostics without calling them a complete native build. A live workflow read during this review confirmed two listed attempts. The newer job had `steps=[]`, `runner_id=0`, and conclusion `failure`; it never executed checkout or TeX. [S15]

The two listed runs are `34674173652` at mathematical commit `416124f13f182f8e2d876f93090865f13269c86b` and `34674631142` at documentation/tool commit `852bfc5981f067b0ad0f701137fbb819f56c2479`. The latest reviewed head is an evidence-only successor. I do not describe either run as a successful build of that head. Nor do I infer a TeX failure, a billing problem, or another scheduling cause from an empty step list.

A complete submission-level resolution requires one coherent package tied to an immutable source snapshot: the recursive native input closure for **both** entry points; an executed reference/citation audit including the prefixed companion references; actual engine logs and versions for the complete builds; the resulting complete PDFs with hashes and page metadata; and review of unresolved references, missing glyphs and layout defects. Mathematical-source identity must be demonstrated if the execution commit differs only in documentation or review files.

This may be produced by a clean local build or another functioning environment. A particular hosted runner, permissions change, or repeated failed workflow is not a mathematical requirement. An independently reported clean whole-native build is the missing evidence; another script promising to perform it is not.

The 16-page changed-module fixture is not the complete article. The existence of the source manifest does not establish the absence of unresolved inherited references. Conversely, the absence of build evidence does not refute a theorem. The request concerns the availability and integrity of the assembled submission, not proof by compilation.

No arbitrary deletion of auxiliary mathematics is required. The complete main and companion inputs, the corrected active versions, and historical sources should remain traceable. I have not compiled or visually inspected the full native PDFs during this review and do not certify their typography or full cross-reference graph.

## 7. Independent diagnostics and their evidentiary value

The accompanying [independent script](independent_checks.py) was written for this review and executed with ordinary Python and `python -O`. Both executions produced byte-identical output. The [result record](independent_checks.json) includes its SHA-256 and the reviewed commit.

The 1,952 checks comprise exact rational instances of the rank-one density identity, fixed-anchor inversion, determinant and inverse blocks, support-preserving transformation identities, finite geometric remainder sums, and finite disjoint-support analogues, together with floating-point leading-geometry and nonlinear finite-bridge envelope checks. Most cases are inexpensive grid identities; their count is not a measure of theorem coverage.

For the 12 finite stationary-envelope cases, the largest absolute discrepancy between the action difference and the numerically integrated direct envelope variation was approximately `4.99e-18`, and the largest stationarity residual was approximately `4.86e-17`. These are floating-point diagnostics with fixed Dirichlet endpoints and finite bridge length, **not** certified interval estimates or a computational proof of the infinite half-line limit. The rigorous infinite-tail reasoning is the analytic argument discussed in Section 3.

The finite disjoint-support examples likewise do not prove the uncountable deficiency-one lemma; its proof is the measure-theoretic countability argument. The author's 884-case suite and historical suites were not rerun in this review. Their recorded results must remain attributed to their respective executions. No native build or proof-assistant verification was performed by the independent script.

## 8. Bounded requests for the next submission

The next response should address C1 by defining the orientation quotient in the active theorem and should address C2 by supplying an actually executed, source-pinned complete native submission. Preserve the observed-type dichotomy and functional smooth-remainder proof. Keep conditional successful-law statements, full charged transcripts, exact-position benchmarks, and intrinsic signed law data distinct in any further editing.

No fresh mathematical counterexample to the core signed inverse was found in this revision-focused audit. That fact must not be inflated into a claim that every inherited theorem has been independently recertified or that a top-four journal would accept the paper. Equally, it must not be suppressed to maintain the appearance of harshness. The prior two mathematical objections are closed on their merits; the remaining requests above are specific and finite.

## Source key

All repository source references below are relative to `papers/A2-v17-boundary-information-coarsening` at reviewed commit `17d71b721f0c5b006b52ec3fbe244866221ee93f`, unless expressly identified otherwise. The accompanying audit gives inspected ranges and source blobs where recorded. Stable theorem labels, rather than invented PDF page numbers, identify mathematical locations.

- **S1:** `main.tex`; repository root `README.md`; `ACTIVE_SOURCE_MANIFEST_V27.md`.
- **S2:** `RESPONSE_TO_REFEREE_V27.md`.
- **S3:** `reviews/a2-v26-external-harsh-top4-2026-09-12/REFEREE_REPORT.md`, repository-relative; compare of preceding review tip with reviewed head.
- **S4:** `article/18f_domination_and_position_comparison_v27.tex`.
- **S5:** `article/23a_signed_endpoint_rigidity_v27.tex`.
- **S6:** `article/23f_single_offset_law_inverse_v26.tex`.
- **S7:** `article/23g_density_support_distinction_v27.tex`.
- **S8:** `article/23b_intrinsic_multichannel_rigidity_v23.tex`.
- **S9:** `article/23d_rank_two_lattice_recovery_v24.tex`.
- **S10:** `article/23e_signature_stability_v25.tex`.
- **S11:** `article/18c1_endpoint_time_deficiency_v25.tex`.
- **S12:** `article/25b_augmented_global_reconstruction_v26.tex`.
- **S13:** `article/18a_vector_boundary_information_v26.tex`.
- **S14:** `article/01_introduction_v27.tex`; `article/16_hyperbolic_coordinates.tex`; `v5/references_v25.tex`.
- **S15:** `VERIFICATION_V27.md`; live GitHub Actions run collection for the revision branch; run `34674631142`, job `103502162490`.
- **S16:** `article/01b_observation_hierarchy_v23.tex`; `article/20_boundary_compatibility.tex`; `article/99_auxiliary_compendium_v19.tex`; `preamble.tex`; `tools/audit_native_sources_v27.py`.

### Primary literature checked for the limited comparison

**L1.** J. De Simoi, V. Kaloshin and M. Leguil, *Marked Length Spectral determination of analytic chaotic billiards with axial symmetries*, arXiv:1905.00890v4; published in Inventiones Mathematicae 233 (2023), 829–901, DOI `10.1007/s00222-023-01191-8`. The arXiv abstract and version metadata were checked; this review does not claim a new line-by-line review of that paper.

**L2.** D. Finamore and M. Leguil, *A CAT(0)-approach to the marked length spectral rigidity of Sinai billiards*, arXiv:2510.18983v1, submitted October 21, 2025. The checked abstract states a rigidity result for the enriched marked length spectrum of finite-horizon Sinai billiards.

**L3.** A. Meister and M. Reiß, *Asymptotic Equivalence for Nonparametric Regression with Non-Regular Errors*, arXiv:1101.5248v1, submitted January 27, 2011. The checked abstract describes equivalence to Poisson experiments for its nonregular regression setting. It is a precedent for the type of limiting experiment, not a theorem about the billiard observation map in A2.
