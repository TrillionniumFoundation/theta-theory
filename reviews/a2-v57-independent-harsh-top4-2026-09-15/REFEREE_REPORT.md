# Independent referee report on A2, revision 57

**Manuscript:** *Boundary laws and rigidity of periodic dispersing billiards*  
**Author:** Qian Qi  
**Date:** September 15, 2026  
**Requested standard:** Annals of Mathematics / Inventiones Mathematicae / Acta Mathematica / Journal of the American Mathematical Society.

This is an author-requested, AI-assisted referee-style assessment, not a commissioned journal report or an editorial decision. Its mathematical, reproducibility, and placement judgments are deliberately separated.

## 1. Recommendation and object of review

**Recommendation: do not accept at the requested highest general-journal level on the present case for exceptional mathematical significance.** This recommendation is not a claim that the principal theorem is false. I have not established a fatal error in the core proof interfaces examined below. In particular, the specific dependency correction requested in the preceding report, R56-C1, is now adequately implemented and should be closed.

The present revision is a bounded correction, not another substantial enlargement of the mathematical result. It declares the acquisition-theorem input to Corollary 19.9, clarifies where contact jets agree, and improves the contribution discussion. Those are appropriate responses. It would be unfair to demand a new probability theorem, to repeat the superseded objection that the principal article is an undifferentiated 283-page catalogue, or to turn an adverse significance judgment into an invented algebraic gap.

Nevertheless, closing a dependency-description issue does not reverse the placement judgment. The strongest part of the paper remains the nonlinear relative long-bridge limit and its actual-smooth contact inverse. The recovery of entire analytic images, the registration of finitely many channel frames, and the lattice cochain are important consequences within the stated rich observation model. The revision does not establish a new reduction to a conventional spectral datum, an unrestricted finite-scalar inverse, or a quantitative global reconstruction theory with controlled complexity. It does not claim those stronger results, and I do not require them as corrections. The issue is how much significance the result actually proved carries, rather than whether its stated qualifications can be wished away.

### Frozen identities

The review concerns the following immutable objects, not the historical version number in the directory name:

| Object | Identity |
|---|---|
| Review-ready branch | `revision/a2-v57-review-ready-2026-09-15` |
| Review-ready head | `bd6c4f04cbdf5a306653098c9840dca2b4989e7a` |
| Actual compiled mathematical source | `e39315c1fbb79ce71d1da91186a0d7e99a5ad8d6` |
| Source branch | `revision/a2-v57-explicit-acquisition-dependency-2026-09-15` |
| Manuscript subtree | `1c11e890bdd5a96381b9a803ade7588eff5c04b9` |
| Manuscript directory | `papers/A2-v17-boundary-information-coarsening/` |
| Native workflow / attempt / artifact | `34959437980` / `1` / `10393060381` |

The principal entry `rigidity.tex` has **106 pages**; `main.tex`, the complete technical manuscript, has **283 pages**; `two_collision.tex` has **seven pages**. Unprefixed page references below refer to the principal PDF. An F-prefix denotes a theorem or page in the full technical manuscript. The source-tree identity was independently resolved through GitHub at the compiled commit and reproduced from the downloaded source archive. [D1]

### Coverage

The fresh reading includes the corrected principal statement and application, the two-ended relative determinant argument, the smooth finite-remainder interface, signed density and interior-window extraction, clear-skeleton construction, finite congruence reconstruction, and the moving-family differential argument. It also extends the previous review by examining the physical calibration and direct capped-estimation route in full Sections 46–47, rather than merely checking that Corollary 19.9 cites it. The leading-data comparison family and the internal graph/support conversion were checked as well. [S1–S11]

This is **not** a fresh line-by-line certification of all 396 delivered pages. In particular, the full catalogue of earlier statistical experiments, every prerequisite in the earlier finite-action construction, the complete adaptive transcript-comparison machinery, and the companion's entire mathematics are outside such a certification. The all-page rebuild has much broader mechanical coverage than the mathematical reading. A source manifest does not remove that distinction.

## 2. Disposition of the preceding report

The preceding report is `reviews/a2-v56-independent-harsh-top4-2026-09-15/REFEREE_REPORT.md`, pinned at `4d2916b6963404d65966626196c3da5da04f8756`. It reviewed source `ae0eea2a3368b01a72ab6eaf50bad0cfb50ec8de`, not the present source. The current response and dependency ledger were read against the actual amended text. [R1–R2, S1, S6]

| Previous point | Finding in revision 57 | Disposition |
|---|---|---|
| R56-C1: Corollary 19.9 uses F.47.3 substantively, not merely for comparison | The introduction, the paragraph immediately before the corollary, its statement, its proof, and the current ledger now declare the input and its additional observation assumptions. | **Closed.** |
| Theorem 1.1(3): contact equality versus collar bounds | Equal jets are now explicitly located at the respective anchored contacts; the common collar carries the functional smooth bounds. | **Closed.** No new smooth-germ identification is asserted. |
| Principal-article hierarchy | The separately compiled geometric article is retained; no new stopped-experiment section has been inserted to answer a significance reservation. | The earlier broad organizational objection remains substantially resolved. |
| Exceptional significance | The leading-data comparison is made more concrete, but the mathematical scope of the inverse is unchanged. | Improved explanation; the adverse placement judgment remains an evaluative reservation. |

The current ledger distinguishes eight background/comparison targets from one substantive acquisition-theorem target. Its statements are reading-derived declarations, not consequences of the position of a reference token. This is the appropriate correction to the earlier classification. I do not independently certify every semantic dependency in the manuscript merely because its regression fixtures pass. Nor have I independently recounted the author's 569-of-572 unchanged statement/proof-block claim; it is unnecessary to the mathematical disposition above. [R2]

## 3. Re-examination of the central analytical and geometric interfaces

### R57-M1. Relative normalization is performed before the exponentially small twist is removed

The reference mixed derivative is

$$d_j^0=\frac{\sqrt{a_0a_p}}{\sinh(j\gamma)},\qquad p=j\bmod2.$$

An arbitrary absolute stationary-action estimate cannot be divided by this quantity to obtain the claimed relative theorem. The proof in Theorem 7.2 avoids that invalid operation. It starts with the exact normalized cofactor identity

$$\log b_j=\sum_i\log\{g[-\ell_{uv}(y_i,y_{i+1})]\}-\log\det(I+G_j\Delta H_j).$$

The half-line orbit construction, the finite two-ended gluing, and the Green-operator comparison must be used together. The perturbation of the reference Hessian has summable endpoint-layer weights. Its trace norm is controlled independently of the number of interior sites, rather than estimated by dimension times a crude operator norm. Truncating to the two end blocks removes summable tails. On these blocks the finite Green operator differs from the two half-line operators by exponentially small reflected and cross-end terms. [S2]

The trace-series step has the required stability estimate: for operators of norm at most a fixed number less than one,

$$|\operatorname{tr}(T^m-\widetilde T^m)|\le m q^{m-1}\|T-\widetilde T\|_1.$$

At each separately fixed derivative order, the polynomial factors introduced by differentiation are absorbed using a strict exponential margin. The subsequent normalized integration uses common Morse coordinates and a fixed integration domain. It does not differentiate a moving sharp boundary without justification, and its conditional-law argument does not infer density convergence from weak convergence alone. The scaled endpoint-map difference retains the required vanishing at the origin. [S2]

I have not established an error in this relative interface. It is a substantial part of the paper and should not be dismissed as the displayed determinant formula alone. Conversely, neither the finite algebraic checks nor the successful build proves the weighted orbit estimates or the differentiated trace-class limit.

### R57-M2. Actual smooth finite jets are treated before formal coefficient inversion

Lemma 12.4, pp. 44–45, supplies the necessary passage from actual smooth graphs to finite-jet algebra. Two graph pairs with the same anchored jets through order M and the same gap are interpolated on a common collar. On finite stationary actions, the interior variations cancel. The terminal variation is retained and estimated before the limit is taken. The direct graph perturbation is evaluated along exponentially decaying orbits, and the finite identity is integrated in the interpolation parameter before passing to infinity. This gives

$$|S_b^{[1]}(u)-S_b^{[0]}(u)|\le\frac{C_M}{1-\rho^{M+1}}|u|^{M+1}.$$

The estimate depends on functional smooth bounds and positive geometric margins. Bounds on a list of Taylor coefficients alone would not establish it. Flat smooth remainders do not defeat the finite-order conclusion, but equality of all smooth jets is not promoted to equality of arbitrary smooth boundary germs. The global image step uses analyticity separately. The amended wording of Theorem 1.1 now respects this distinction. [S1, S3]

At degree n the highest new graph coefficients enter through

$$M_n=\begin{pmatrix}\coth(n\gamma)&r_0^n\operatorname{csch}(n\gamma)\\r_1^n\operatorname{csch}(n\gamma)&\coth(n\gamma)\end{pmatrix},\qquad r_0r_1=1.$$

The endpoint occurs once and each interior contact twice in the envelope sum. The resulting geometric series give the displayed block and its determinant one. Odd coefficients remain signed. The actual-smooth argument, not the matrix identity in isolation, justifies applying this recursion to genuine boundaries. [S3]

### R57-M3. A useful refinement: the admissible last-jet blocks themselves are uniformly bounded in order

The earlier caution that determinant one alone does not imply good conditioning is correct. It should not be read as evidence that these particular geometrically admissible blocks must become badly conditioned. There is a simple stronger bound available from the hypotheses.

Put t = exp(-gamma), c = cosh(gamma), and c_b = 1 + g kappa_b > 1. Since c squared equals c_0 c_1 and r_b equals the square root of c_b/c_(1-b),

$$r_b<c,\qquad r_bt<ct=\frac{1+t^2}{2}<1.$$

Therefore

$$M_n=\frac1{1-t^{2n}}\begin{pmatrix}1+t^{2n}&2(r_0t)^n\\2(r_1t)^n&1+t^{2n}\end{pmatrix}.$$

Its inverse has the same diagonal entries and the negatives of the off-diagonal entries. For n at least three,

$$\max\{\|M_n\|_\infty,\|M_n^{-1}\|_\infty\}\le\frac{3+t^6}{1-t^6}.$$

Writing q = (1+t squared)/2 also gives

$$\|M_n-I\|_\infty\le\frac{4q^n}{1-t^6}.$$

These bounds are uniform on a class with gamma bounded below by a positive constant. This is a referee observation following directly from the printed geometric parameters, not a necessary correction and not an additional claim attributed to the author. The independent script checks 750 admissible rational blocks at orders 3 through 32, including the explicit inverse and endpoint/interior multiplicities. The argument above, rather than that finite sample, establishes the general bound. [S1, S3, D2]

Crucially, this does **not** supply a uniformly bounded inverse for the complete nonlinear triangular jet map. The lower-order remainders, their derivatives, the norms used to encode analytic data, and analytic continuation remain separate issues. The manuscript is right not to infer an all-order noisy reconstruction theorem from determinant one. The present observation simply locates that caution more accurately: it need not be blamed on these isolated two-by-two last-jet blocks.

### R57-M4. Density extraction and window centering preserve the stated information, not an unstated stronger experiment

The single-offset inverse uses

$$1-\frac{f(u,v)f(0,0)}{f(u,0)f(0,v)}=t(u)t(v),\qquad t=\frac{S}{d-S}.$$

A fixed nonzero anchor chooses a positive scalar normalization. Solving for S preserves both signs of the transverse coordinate. There is no differentiation of a pointwise square root at the degenerate minimum. The local stability argument uses positive density and anchor margins in a fixed differentiable topology; it does not turn total variation into control of high derivatives. Independent polynomial controls with a nonzero cubic coefficient reproduce the inverse and its odd derivative exactly, but are not claimed to be realized billiard laws. [S4, D2]

For the cropped window, the mixed logarithmic derivative is

$$\partial_{xy}\log p(x,y)=-\frac{S'(x-\xi)S'(y-\eta)}{[d-S(x-\xi)-S(y-\eta)]^2}.$$

Under the printed hypotheses, the unique vertical and horizontal zero lines identify the origins. The proof uses no unobserved cap boundary. It does require that both origins lie inside the window, that the relevant minimum be nondegenerate, that denominators remain positive, and that the chosen slices and anchors have margins. The local extension loses the explicitly stated derivatives when taking mixed log derivatives and translating the recovered origins. None of this identifies arbitrary unknown coordinate changes or unknown physical units. [S4]

Cancellation of separate recording factors identifies the normalized interaction, not the discarded probability mass. Multiplying those factors by small constants can preserve the conditional law while reducing the number of observed successes. Thus a conditional-law inverse alone cannot provide a uniform preparation budget. This is why the additional acquisition theorem in Corollary 19.9 matters mathematically, not merely bibliographically.

### R57-M5. Finite periodic reconstruction and infinitesimal rigidity have different uses of analyticity and symmetry

The clear-skeleton construction in Theorem 19.3 is valid at the interface checked. A blocked closest segment is replaced by two shorter gaps whose sum is no larger than the original gap. Uniform positive separation makes the induction terminate. The resulting object is a graph path, not a physical specular itinerary. Paths to all obstacle representatives and two marked deck translates give a finite quotient graph whose cycle gains have rank two. A spanning tree and two additional edges yield the N+1 design. Positive contact Hessians and a finite-translate bound justify local persistence; infinitely many third-obstacle clearances are not silently assumed to persist. [S6]

For noncircular analytic obstacles, the finite symmetry group gives finitely many incidence congruences. Theorem 20.3 enumerates these choices and then checks complete incidence consistency, nonsingularity and orientation of the lattice, disjointness, and selected-channel clearance. The cochain reconstructs

$$L=(v_1\ v_2)M^{-1}$$

with the actual real-invertible integer gain matrix M. It need not be unimodular. Solving those displacement equations without the separate admissibility checks would not prove the fiber theorem; the printed proof includes the checks and both directions of the reconstruction. It is a finite-branch inverse of exact function-valued observations, not an algorithm for deciding analytic shape equality from arbitrary finite-precision input. [S6–S7]

The differential theorem does not infer immersion from exact injectivity. The common holomorphic strip makes the parameter variation analytic. Moving-reference differentiation includes both the derivative of the reference Green operator and the derivative of the subtracted Hessian; the nondecaying reference terms cancel before trace-class summation. The positive-part normalizer is differentiated with its regular boundary level treated correctly. Zero density variation gives zero action and graph-jet variation at each fixed order. The internal graph/support lemma and the identity theorem then eliminate the entire channel-frame shape variation. [S8–S9]

At a finitely symmetric base table, registration follows the actual local angular branch. It does not assume that a symmetry of the base obstacle survives a symmetry-breaking perturbation. The cochain then eliminates relative placement and lattice variation. The remaining kernel is precisely the common infinitesimal proper Euclidean motion stated in Theorem 21.5. Theorem 21.6 selects finitely many test differentials only after tangent separation on a fixed finite-dimensional immersed model. Its lower Lipschitz bound uses closeness to one invertible base Jacobian on a convex ball, not pointwise nonsingularity alone. [S7–S9]

I found no new fatal defect in these interfaces. The resulting distinctions are essential: finite ambiguity is not global uniqueness; exact analytic propagation is not stable continuation on an unrestricted class; and model-local finite coordinates are not one universal finite observation vector.

## 4. Expanded audit of the acquisition input

### R57-A1. Corollary 19.9 now verifies the correct conditional application

The corrected paragraph and proof on p. 87 explicitly import Theorem F.47.3. The corollary concerns a compact analytic family in **one persistent properly asymmetric skeleton neighborhood**, with the cited uniform analytic, chart and physical-record assumptions. It does not cover all noncircular finite-ambiguity families indiscriminately, nor choose one common design across unrelated skeleton neighborhoods. [S6, S10–S11]

The geometric design checks are appropriate. The finite incidence and signature-rigid matching persist on that neighborhood. The two marked gains form a fixed invertible M. Since the lattice L ranges over a compact nonsingular family, the smallest singular value of LM has a positive minimum. This supplies the holonomy margin without supplying an unknown Euclidean lattice vector. The finite-signature and compact-inverse results provide the geometric inverse used by the acquisition theorem. Its sensor and preparation assumptions remain additional assumptions, not conclusions of exact injectivity. [S5–S6]

The physical pilot records planar endpoint positions, with the two types of a channel expressed in one channel sensor frame, together with clock and preparation outcomes. Different channels need not already be registered. The later estimator can discard longitudinal coordinates and residual information; that does not turn the calibration into an endpoint-histogram-only observation. Fixed gates and selected channel labels are part of the design. There is no uncharged discovery of arbitrary unmarked channels. [S10]

I find the revised dependency statement accurate. There is no demonstrated path from this downstream corollary into the examined proofs of Theorems 1.1, A or B. Calling the input substantive therefore does not establish circularity in the geometric theorem. **R56-C1 is closed.**

### R57-A2. The pilot and capped estimator avoid two common stopping/calibration mistakes

The direct physical acquisition route in full Sections 46–47 deserves more than a reference scan. Its near-onset localization and positive lower success mass are used for an explicit finite pilot grid. The lower mass has the form

$$p_*(j,h)=c h^2e^{-j\gamma_+}.$$

Each type is tested at a finite grid of physical times. A grid point with excess in [h,2h] exists uniformly over the gap interval, and the per-point preparation cap controls the probability of missing it. A recorded earlier success still has nonnegative excess because a j-flight record cannot occur at a time below jg. Consequently the good pilot controls both the gap error multiplied by j and the contact-frame error. All unsuccessful preparations count toward its deterministic cap. [S10]

A particularly important ordering is printed in the fixed-order estimator proof, F. p. 192. First choose the finite separating tests and the sample target k, then the final even flight number J, and only then the pilot resolution h. The pilot itself runs at j = J. The proof therefore controls J times the gap error for the very flight number subsequently used. It does not calibrate at a short flight and then amplify an uncontrolled gap error by choosing a much longer bridge afterward. [S11]

Conditional on a good pilot history, the fresh designs are fixed and observable. The empirical concentration argument is applied to the successful marks in the **uncapped** fresh success sequence. A cap failure event is added separately. It is not assumed that conditioning on completion before the cap preserves independent identically distributed marks. This is the correct way to handle the stopping rule.

With D design groups, R bounded tests and success lower bound p_0, the printed choices include

$$k\ge8c^{-2}\log(8R/\delta),\qquad B=\left\lceil\frac{2k+8\log(8D/\delta)}{p_0}\right\rceil.$$

The binomial lower-tail bound controls the union of cap failures by delta/8, while the bounded-test concentration bound is at most delta/4. Adding the pilot contribution still leaves the asserted risk budget. Tests sharing samples need not be independent for this union bound. The finite library is selected from a compact separating observation map; its existence is not advertised as an effective computational construction. [S11]

This reading supports the direct physical risk argument used by the application. The additional complete-transcript comparison invokes earlier machinery, including F.25.3; I have not freshly certified all of that machinery in this report. The direct physical concentration proof does not need to identify an unknown centering map with an observable kernel in order to establish the displayed estimation bound. The distinction is visible in the source and should remain visible in claims about what this audit certifies.

### R57-A3. Prescribed budgets are an existence result, not a complexity estimate

The increasing-order construction selects a finite jet resolution and a small finite-order error using the compact inverse modulus. Each stage has a finite deterministic cap. Taking the running maximum of those caps and choosing the largest affordable stage gives a policy under each prescribed preparation budget. The policy executes that stage afresh; it does not claim that all previous stages can also be executed within the same cap. The minimum even flight number can tend to infinity while the error tends to zero. [S5, S11]

This is a legitimate uniform consistency mechanism under the imported compactness, analyticity, observation and margin hypotheses. The separation constants, compact inverse moduli, template library and small success probabilities can be extremely unfavorable and are not given an effective general complexity bound. No minimax rate or unrestricted stable analytic continuation follows. Those limits are not a flaw in the theorem as stated. They prevent the acquisition corollary from being used rhetorically as a stronger finite-information reconstruction result than it is.

## 5. The leading-data comparison is real, but its logical reach is limited

The revised introduction uses an existing analytic family to make its information claim concrete. This is an improvement over merely asserting that nonlinear laws contain higher jets. For

$$h_{s,z}(\theta)=1+s\sin^4\theta+z\sin^6\theta,$$

the area derivatives at the disk are 3 pi/4 and 5 pi/8. The area-preserving implicit curve has derivative z'(0) = -6/5. On the fixed rectangular lattice, the construction keeps gap, free area, both contact curvatures, and all the specified leading endpoint covariance/count data fixed. Its fourth contact jet is

$$q_s=3-24s.$$

At gamma = arcosh(2) and a = sqrt(3), the printed quartic formula gives

$$\left.\frac{d}{ds}\mathcal R_\infty^{(s)}(0)\right|_{s=0}=\frac{\sqrt3}{2}.$$

The independent finite controls reproduce the area derivatives and this coefficient. The action inverse also shows why differing contact jets must produce differing fixed-offset signed conditional laws. [S12, D2]

The example demonstrates information absent from the **leading quadratic threshold record**. It does not demonstrate equality of complete marked length spectra, equality of all other billiard observations, or a reduction between previously studied inverse data and the present law-valued data. The manuscript now says this explicitly. The disk at the base of this local comparison is not a counterexample to a global theorem whose noncircularity hypothesis excludes it. The example should be credited for its actual purpose, neither dismissed nor inflated.

## 6. Originality and significance at the requested level

### R57-E1. The analytical mechanism, not the number of consequences, must carry the placement case

The principal article has a genuine mathematical architecture. The relative normalized long-bridge limit makes nonlinear information survive a singular asymptotic normalization, and the smooth finite-remainder argument justifies using that information on actual boundaries. These are the most persuasive parts. The current review has not shown them to be false, and I do not claim that a displayed identity or a short summary makes their proofs elementary.

The later steps have different conceptual weight. Once the special density is available, cancellation of separate factors is an association calculation. Once all analytic contact jets have been recovered, the identity theorem propagates the local image. Once the images are known, finite congruence matching and the lattice displacement equations are finite geometric operations. Once the data derivative separates the tangent space of an immersed finite-dimensional model, selecting a basis of scalar test differentials is linear algebra followed by the inverse function theorem. These consequences strengthen the result, but counting them as equally independent major innovations would exaggerate the significance case. [S2–S9]

The analysis is centered on selected alternating clear-channel bridges with a controlled one-dimensional chain of collision variables. The global table conclusion uses deliberately marked, signed, physically scaled, function-valued laws, together with gaps and analytic continuation. The observations are rich enough to recover complete local action germs. The unknown lattice and inter-channel placement are genuinely reconstructed; however, a finite number of channel labels is not a finite amount of scalar information. The physical consistency theorem has additional acquisition hypotheses and non-effective compactness constants. These are not concealed defects, but they are material to judging the reach of the theorem. [S1, S6–S11]

My adverse recommendation therefore rests on the current case for the breadth, originality and impact of this particular relative/smooth inverse, not on an alleged failure to format a reference or prove an unrelated stronger theorem. The revision improves accuracy and positioning, but it does not persuade me that the result has the exceptional significance required for the requested placement. Another specialist may reasonably judge its central mechanism more highly. This is an evaluative conclusion, not a theorem that the work cannot merit such a journal.

### R57-E2. Primary-source comparison must not manufacture either priority or redundancy

The targeted literature check was refreshed from primary records. It supports careful distinctions, not a comprehensive priority conclusion.

Finamore and Leguil's *A CAT(0)-approach to the marked length spectral rigidity of Sinai billiards*, arXiv:2510.18983v1, treats finite-horizon Sinai billiards with **enriched** marked length data. The enriched datum and Theorem A were checked on printed pp. 4–5. It must not be represented as using only ordinary marked periodic-orbit lengths. No reduction between that enriched datum and the present conditional endpoint-law datum has been established here. [L1]

De Simoi, Kaloshin and Leguil's analytic open-billiard result uses non-eclipse and its stated symmetry/genericity restrictions with marked length data. Its observation map and geometric class differ from the present periodic-law setting. Its existence does not prove the present theorem redundant, and the present theorem does not automatically solve that inverse problem. The primary abstract/record, rather than its complete proof, was checked for this comparison. [L2]

Osius's association-model work provides established context for separating marginal distributions from association information. This justifies treating marginal cancellation as background rather than as a new general statistical principle. It does not prove the manuscript's billiard realization, relative estimate, or smooth contact inverse. [L3]

Florio and Leguil's version-5 record explicitly removes a geometric open-billiard spectral-rigidity conclusion affected by a mistake while retaining and improving dynamical conclusions. The manuscript's version-specific distinction is appropriate. An obsolete geometric assertion must not be cited as an established theorem. [L4]

This is a limited primary-source comparison, not an exhaustive priority search or a review of the complete proofs of these works. I make no categorical first-priority claim and no claim that the principal boundary-law theorem is already known. A meaningful placement assessment should engage the actual relative/smooth mechanism rather than compare incompatible data maps by title alone.

## 7. Required disposition and limits of further revision

**Specific correction requested in the preceding report:** R56-C1 is closed. The anchored-jet wording is also closed.

**New mandatory core mathematical repair established by this review:** none within the stated coverage. This is a report of what the audit established, not a certification of every theorem in either manuscript.

**New mathematical observation:** R57-M3 supplies a stronger bound for the isolated admissible last-jet blocks. Incorporating it is optional. It is not a precondition for closing R56-C1 and does not create a new all-order inverse theorem.

**Recommendation at the requested journal level:** do not accept on the present exceptional-significance case. I do not recommend another repair-only round as though one more dependency sentence, build certificate, elementary stopping lemma, or version number would resolve that judgment. No arbitrary reduction of the theorem or deletion of the retained corpus is requested. A subsequent substantive assessment should focus on the relative/smooth inverse and its mathematical significance, with already closed points left closed unless a precise new defect is demonstrated.

## 8. Independent reproduction and audit limitations

The downloaded native artifact has SHA-256

`45b4a5525012e4323fc5940b61304c949b7f2a968cfa5bf597a2dd97cfe80186`.

The independent verifier checked all **679 frozen source files**, including byte lengths, SHA-256 values and Git blob identities, and reconstructed the manuscript subtree specified above. The active manifests contain 110 main inputs, 41 principal inputs, and one companion input, with **120 distinct paths** in their union. All 45 build-report evidence entries were checked. The frozen-source count includes historical and ancillary files; it is not a count of independent mathematical inputs or theorems. [D1]

Fresh complete builds used shell escape disabled and compiled the companion, full manuscript and principal entry in that order. All **396 pages** agree with their native counterparts in extracted text and same-renderer 72-dpi RGB arrays. The rebuilt PDFs are **not byte-identical**. There are no recorded undefined-reference, undefined-citation, missing-glyph, overfull-box or LaTeX-error matches in the checked logs. One principal and three full-manuscript underfull-box notices remain. [D1]

Actual visual inspection covered principal pp. **3, 19, 44, 87 and 99**, and full p. **192**. No clipping or unreadable formula was observed on those pages. Computational all-page agreement is not described as all-page human-style visual inspection.

The independent finite script checks admissible last-jet blocks, signed four-density recovery and mixed log derivatives, the fourth graph/support coefficient, the leading-data family's area derivatives and quartic coefficient, a nonunimodular lattice control, and 30 onset-grid configurations. Ordinary and optimized-Python runs give identical output. No author's mathematical checker is imported. These finite controls do not prove trace-class limits, arbitrary-order smooth factorization, analytic continuation, probability inequalities, or global rigidity. [D2]

## Sources and reproducibility keys

All S-keys refer to the actual compiled source `e39315c1fbb79ce71d1da91186a0d7e99a5ad8d6`, beneath `papers/A2-v17-boundary-information-coarsening/`. The immutable source root is:

https://github.com/TrillionniumFoundation/theta-theory/tree/e39315c1fbb79ce71d1da91186a0d7e99a5ad8d6/papers/A2-v17-boundary-information-coarsening

- **S1:** `rigidity.tex`; `journal/00_principal_introduction_v56.tex`; `journal/01_structural_statements_v56.tex`. In particular Theorem 1.1, pp. 2–3, and its proof map.
- **S2:** `v4/10_boundary_layers.tex`, especially the half-line construction, two-ended normalized determinant comparison and fixed-offset law proof; Theorems 7.2–7.3, pp. 17–20. The earlier finite-action inputs are not all freshly certified here.
- **S3:** `article/23a_signed_endpoint_rigidity_v27.tex`, including the finite envelope and smooth finite-jet factorization, and the signed last-jet calculation; Lemma 12.4, pp. 44–45, and Proposition 12.6.
- **S4:** `article/23f_single_offset_law_inverse_v42.tex`, especially Theorem 13.1 and fixed-order stability; `journal/shared/23q_support_and_interior_windows_v52.tex`, lines 57–166, Theorem 14.6, pp. 60–61.
- **S5:** `article/23e_signature_stability_v25.tex`, finite analytic signature and compact-inverse statements and their use by the acquisition construction. The full noisy-registration catalogue is not separately certified.
- **S6:** `article/23j_generic_finite_channel_rigidity_v45.tex`, lines 1–221 for clear skeletons, and lines 492–544 for the corrected acquisition paragraph, Corollary 19.9 and proof; principal p. 87, full p. 89.
- **S7:** `article/23n_finite_symmetry_v49.tex`, finite congruences, local alignment and the complete finite-fiber reconstruction; Theorem 20.3, pp. 89–90. The separate two-table construction is not freshly certified in this report.
- **S8:** `article/23m_differential_rigidity_v48.tex`, moving-reference and density differentiation, local kernel, analytic propagation, registration, and Theorems 21.5–21.6, pp. 97–99.
- **S9:** `journal/02_graph_support_v56.tex`, Lemma A.1.1 and its proof, pp. 99–100.
- **S10:** `article/25a_common_observables_v25.tex`, common record space, localization, finite pilot, observable normalization and finite-test implementation; full Section 46, including Theorem F.46.2.
- **S11:** `article/25b_augmented_global_reconstruction_v26.tex`, finite separators and template estimator, direct capped physical risk proof, and increasing-order budget construction; full Section 47, Theorems F.47.2–F.47.3, pp. 191–193. Its references to earlier complete-transcript transfer are not a fresh certification of those earlier proofs.
- **S12:** `v4/20_nonlinear_information.tex`, the quartic derivative and area-preserving leading-data comparison, especially lines 23–94 and 116–195.
- **R1:** The v56 report at `4d2916b6963404d65966626196c3da5da04f8756`, path specified in Section 2.
- **R2:** `RESPONSE_TO_REFEREE_V57.md`; `HISTORICAL_DERIVATION_AUDIT_V57.md`; `journal/DEPENDENCY_LEDGER_V57.md`; current review-ready README. The latter is pinned at the review-ready head; the mathematical files are pinned at the compiled source.
- **D1:** `AUDIT_AND_REPRODUCTION.md`, `verify_delivery.py` and `DELIVERY_VERIFICATION.json` in this review directory.
- **D2:** `check_local_mechanisms.py` and `INDEPENDENT_CHECKS.json` in this review directory.
- **L1:** D. Finamore and M. Leguil, *A CAT(0)-approach to the marked length spectral rigidity of Sinai billiards*, arXiv:2510.18983v1, October 21, 2025. https://arxiv.org/abs/2510.18983 . Primary record and enriched datum/Theorem A on printed pp. 4–5 checked September 15, 2026.
- **L2:** J. De Simoi, V. Kaloshin and M. Leguil, *Marked Length Spectral determination of analytic chaotic billiards with axial symmetries*, arXiv:1905.00890v4, August 17, 2022; DOI 10.1007/s00222-023-01191-8. https://arxiv.org/abs/1905.00890 . Primary record/abstract scope checked September 15, 2026.
- **L3:** G. Osius, *Asymptotic inference for semiparametric association models*, Annals of Statistics 37 (2009), 459–489; DOI 10.1214/07-AOS572. https://arxiv.org/abs/0903.0702 . Primary record/association-model scope checked September 15, 2026.
- **L4:** A. Florio and M. Leguil, *Smooth conjugacy classes of 3D Axiom A flows*, arXiv:2010.04120v5, June 3, 2021. https://arxiv.org/abs/2010.04120v5 . The version-specific correction statement and dynamical/geometric distinction were checked September 15, 2026.
