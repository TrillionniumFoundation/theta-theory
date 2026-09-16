# Independent referee report on A2, revision 61

**Manuscript:** *Boundary laws and rigidity of periodic dispersing billiards*  
**Author:** Qian Qi  
**Date:** September 16, 2026  
**Requested level:** Annals of Mathematics / Inventiones Mathematicae / Acta Mathematica / Journal of the American Mathematical Society.

This is an author-requested, AI-assisted referee-style assessment, not a commissioned journal report, an editorial decision, or a formal proof certificate. The report distinguishes mathematical correctness, the force of the exposition, originality, and exceptional significance. A negative placement judgment is not a statement that the research program should stop.

## 1. Recommendation and frozen submission

**Recommendation: decline at the requested highest general-journal level on the present case for exceptional significance.** The revised exposition is materially better focused and answers the preceding report's request rather than evading it. I nevertheless do not find its affirmative case sufficient for a positive recommendation at that level. This judgment is reconsidered below on the relative/action mechanism itself; it is not inferred from the absence of a new theorem or from an earlier recommendation.

**No new fatal mathematical error is established in the arguments examined in this round.** In particular, the newly emphasized realized comparison has the stated fourth graph jet and nonlinear response, and the finite-flight inverse is supported by its printed fixed-order proof. There is no basis for inventing a corrective theorem simply to keep a revision cycle going. Conversely, the absence of a demonstrated error in this bounded examination is not certification of every assertion in the complete delivery.

| Object | Immutable identity |
|---|---|
| Review-ready branch | `revision/a2-v61-review-ready-2026-09-16` |
| Review-ready head | `774aa34b43f5013dd3a41c8bc6ca5a529466d788` |
| Actual compiled mathematical source | `71e0bd6306f54466728c2e6e781bb0f422c5cfb0` |
| Manuscript subtree reconstructed from frozen source | `ee2d39dbce4dce4d972ec1a281af1df9aaf44d4a` |
| Source branch | `revision/a2-v61-relative-mechanism-2026-09-16` |
| Manuscript directory | `papers/A2-v17-boundary-information-coarsening/` |
| Native workflow / attempt / artifact | `35043311589` / `1` / `10426471183` |

The principal article has **119 pages**, the complete technical manuscript **294 pages**, and the companion **seven pages**. Page references below are to the principal article unless stated otherwise. The source-to-review-ready GitHub comparison contains three delivery commits and no intervening change to compiled mathematical inputs. The revised introduction was also fetched at the compiled commit; its blob is `2d41a5d723b932252283f79b44c53f90f1177575`. [D1]

### What was reviewed afresh

The fresh mathematical examination concentrates on the revised introduction and its actual evidentiary basis: geometric near-onset localization, the finite Jacobi/relative-flux lemma, physical residual-time integration, the half-line and two-ended relative determinant argument, actual-smooth factorization and homogeneous isolation, the single-offset density inverse and its finite-flight consequence, and the full quartic-response/area-preserving-family calculation. The structural headline statements, observation conventions, and current dependency declaration were checked for scope consistency. The author response, cover letter, historical audit, and literature note were read as arguments and provenance, not as proofs. [S1–S7]

This is **not a fresh line-by-line proof audit of all 420 pages**. In particular, the whole global finite-fiber and moving-family proof catalogue, every analytic graph-to-support prerequisite, the complete acquisition/calibration and stopped-experiment theory, and the companion's mathematical argument are not freshly certified here. The v59/v60 analytic inverse modules are unchanged; their earlier scoped assessments are retained as continuity, not represented as a second complete proof verification in this round. All-page mechanical reproduction has a different meaning from this mathematical coverage.

## 2. What revision 61 actually changes

The preceding report is pinned at `396bb28e17ba9944af5ff89a2db601412eeb95ee`; it reviewed source `1a55bfb1102c3eab9cdcd6a292c5ef9070ea14a5`. It established no mandatory new core repair and asked that the importance of the central mechanism be argued directly. [R1]

The source comparison confirms the author's description of this revision. All **739 inherited frozen paths** remain; **736 are byte-identical**. The only changed inherited files are the manuscript README and the two entry files, `main.tex` and `rigidity.tex`. The old principal introduction remains byte-identical in place. A new introduction replaces it in the active input graph, and both mathematical environments in the old introduction occur verbatim in the replacement. The structural theorem input and the other proof modules are retained. These are byte-level findings, not a semantic census of independent results. [D1]

The principal opening now distinguishes long flight number at fixed positive excess from a small-excess quadratic truncation, states why the relative twist is necessary, connects the limiting law to the existing finite-flight inverse, and gives a concrete realized separation from leading data. The cover letter no longer asks the reader to count continuation, matching, and lattice algebra as unrelated breakthroughs. This is a substantive improvement in presentation even though the mathematical claims have not changed. [S1, R2]

| Earlier issue | Disposition |
|---|---|
| Complete analytic inverse versus only diagonal blocks | The stronger result is retained; no regression is found. |
| Conditional real-observation consequence from v60 | Retained at its actual strength, with analytic prior and radius loss. |
| Same-disc stability from weak real data | Still not claimed; this is not an outstanding defect. |
| Explicit acquisition input and fixed observation conventions | Retained; closed corrections are not reopened. |
| Mechanism-centered significance case | Now explicitly and credibly presented, but not persuasive enough for the placement requested, in this reviewer's judgment. |

A revision can legitimately be expository. The absence of a new theorem is neither the reason for the adverse recommendation nor grounds for alleging that the response was nonresponsive.

## 3. Re-examination of the relative/action mechanism

### R61-M1. The forward law comes from a physical phase measure, not an assumed endpoint density

The finite model uses the exact flight length

$$\ell_b(u,v)=\sqrt{(g+\psi_b(u)+\psi_{1-b}(v))^2+(v-u)^2}.$$

The localization argument uses separation of lifted obstacles, uniqueness of the closest segment, positive clearance, and the separation of distinct normal outgoing states. Near a ground onset, every complete flight must be short; specular reflection then forces repeated reversal of one channel. The same localization applies to a selected clear nonminimal channel only for its selected itinerary, not for the complete count event. This distinction is printed and matters. [S2]

The quadratic endpoint Hessian is uniformly positive even though its off-diagonal twist tends to zero. The alternating Jacobi transformation and Schur complement give

$$d_j^0=\frac{\sqrt{a_0a_p}}{\sinh(j\gamma)},\qquad p=j\bmod2.$$

The nonlinear bridge is constructed using a weighted Green inverse and local remainders. Strict diagonal dominance supplies uniqueness on the small contact box and bounds independent of the number of interior sites. This is a controlled local hyperbolic problem, not an analysis across arbitrary grazing singularities. [S2]

The first-impact change of variables gives

$$d\mu=\frac{-W_{j,uv}}{2\pi A}\,du\,dv\,dr.$$

The boundary arclength factor cancels against the generating-function momentum derivative. At excess $d<g_*$ the allowed first residual time is smaller than the preceding roof, and another complete roof cannot fit after the last impact. Integrating $r$ therefore gives the positive-part weight, rather than an arbitrary substitute ensemble. The normalization is the phase-volume normalization; finite horizon is not silently inserted as an assumption. These observations support the stated physical interpretation. [S2]

### R61-M2. Exact cofactor normalization is the substantive relative estimate

For the finite stationary segment, the tridiagonal Schur complement yields

$$-W_{j,uv}=\frac{\prod_{i=0}^{j-1}[-\ell_{i,uv}]}{\det H_{\rm int}},$$

with the empty determinant equal to one when $j=1$. Consequently

$$\log b_j=\sum_i\log\{g[-\ell_{i,uv}]\}-\log\det(I+G_j\Delta H_j),\qquad b_j=-W_{j,uv}/d_j^0.$$

This exact identity is used before the limit. An absolute action estimate alone would not justify dividing its error by $d_j^0$. The revised introduction now makes the distinction appropriately explicit. [S1–S3]

The two-ended proof glues left and right half-lines, controls the stationary residual in a summable norm, and retains blocks of size $\lfloor j/3\rfloor$ at the two ends. Tridiagonal localization gives a trace-norm bound for the discarded perturbation. Remote reflections and cross-end Green blocks are exponentially small; fixed differentiation orders introduce only fixed polynomial factors. The determinant comparison then uses

$$|\operatorname{tr}(T^m-\widetilde T^m)|\le m q^{m-1}\|T-\widetilde T\|_1,\qquad \|T\|,\|\widetilde T\|\le q<1.$$

Thus the logarithmic series is controlled by a trace-class factor, not by multiplying the chain length by a crude operator bound. Sending the end blocks to their half-line limits supplies $B_0(u)B_p(v)$. The subsequent common-domain Morse integration justifies fixed-order offset derivatives at zero; it is not differentiation through an uncontrolled moving cutoff. [S3]

I find no new fatal error in this interface. The 48 exact finite cofactor controls in the audit are useful algebraic checks, but do not prove the infinite-dimensional or differentiated convergence statements. The printed gluing and trace-norm argument is what carries those assertions. [D2]

### R61-M3. The smooth inverse is more than a formal Taylor recursion

The actual-smooth factorization interpolates graph functions with equal anchored jets through order $M$, not merely a list of formal coefficients. Differentiating a finite stationary sum leaves the direct graph variation and one terminal orbit term. The latter is estimated and removed only after its decay is established. The direct variation is bounded by the $(M+1)$st power of a geometrically decaying contact coordinate. Integration in the interpolation parameter gives

$$|S_b^{[1]}(u)-S_b^{[0]}(u)|\le\frac{C_M}{1-\rho^{M+1}}|u|^{M+1}.$$

The needed functional smooth bounds are explicit. They are not inferred from bounded Taylor coefficients. The local interpolation need not be globally realized as a family of periodic tables to establish this local jet identity. [S4]

Only after this factorization does the homogeneous calculation isolate a new contact degree. At leading degree the initial visit is counted once and each internal visit twice, giving

$$M_n=\begin{pmatrix}\coth(n\gamma)&\mathfrak r_0^n\operatorname{csch}(n\gamma)\\\mathfrak r_1^n\operatorname{csch}(n\gamma)&\coth(n\gamma)\end{pmatrix},\qquad \det M_n=1.$$

Nonlinear corrections to the orbit enter at higher endpoint degree, including for odd variations. Flat smooth perturbations illustrate why equality of all jets is not equality of arbitrary smooth germs, but do not contradict this finite-order statement. The source preserves that distinction. [S4]

The later full analytic inverse and conditional real-observation theorem strengthen the outcome in their stated additional topologies. Their hypotheses are not retrospectively imposed on the earlier smooth theorem, nor are they used to assert that all smooth remainder constants are uniform in order. The rewritten abstract does not introduce such a claim. [S1, S7]

### R61-M4. The highlighted finite-flight inverse is valid in the declared strong real norm

Corollary 13.3, p. 61, is an existing result, now given a more visible role. On a fixed positive interior square,

$$f_{j,b,d}=Z_j^{-1}b_j(d-E_j),\qquad f_{b,d}=Z^{-1}B_b(u)B_b(v)(d-S_b(u)-S_b(v)).$$

The relative theorem controls the numerators in $C^M$. On the whole common box, the Lipschitz property of $x\mapsto x_+$ controls the normalizing integral in $C^0$; this denominator has a positive lower bound at fixed $d$. No high derivatives of a sharp boundary are needed to obtain the interior $C^M$ density estimate. [S5]

The four-density inverse is locally Lipschitz in that norm under positive density and nonzero anchor margins. It is defined on sufficiently small nearby functions even if they are not exact factorized laws. After extraction, subtracting the zeroth and first action Taylor terms is a bounded projection and does not alter the Hessian or higher coefficients. Leading-curvature inversion and finitely many triangular steps then yield

$$\operatorname{error}(j^M\psi_0,j^M\psi_1)\le C_M(\tau^j+\epsilon+\epsilon_g).$$

This argument does connect finite-flight observations to the geometric inverse. It does not provide $C^M$ density estimation from a finite sample without further assumptions, does not make $C_M$ independent of $M$, and does not bound a charged preparation budget. Those are not omitted conclusions that should be imputed to the corollary. [S5]

## 4. The realized information separation

### R61-M5. The area constraint and fourth graph jet check out

Theorem A.4.2, pp. 117–118, uses

$$h_{s,z}(\theta)=1+s\sin^4\theta+z\sin^6\theta.$$

An independent expansion of the support-area formula gives the exact polynomial

$$\frac{\mathcal A(h_{s,z})}{\pi}=1+\frac34s+\frac58z-\frac{45}{128}s^2-\frac{105}{128}sz-\frac{525}{1024}z^2.$$

Hence the area constraint defines an analytic branch with $z(0)=0$ and $z'(0)=-6/5$. The derivative in the $z$ direction is nonzero. This verifies the constraint beyond checking only an asserted tangent vector. [S6, D2]

At the horizontal contacts, the height and its first two perturbation jets vanish. The support points and curvature radii therefore remain those of the unit disk. Eliminating the normal-angle parameter from the support parametrization gives

$$\psi(y)=\frac{y^2}{2r(0)}+\frac{3r(0)-r''(0)}{24r(0)^4}y^4+O(y^6).$$

Here $r(0)=1$ and $r''(0)=24s$, so the fourth graph derivative is exactly $q_s=3-24s$. The area-correcting $\sin^6$ term does not change this fourth jet. Smallness preserves positive curvature and the strict gap separating horizontal ground channels from the other pairs. Thus this is an actual local family of periodic tables, not a formal density perturbation. [S6]

The claim of identical leading data is scoped to the horizontal ground-onset experiment: $g=1$, free area $12-\pi$, and both contact curvatures stay fixed, so the leading endpoint Hessians and count amplitudes at every flight number stay fixed. It is not an assertion that every possible channel measurement, all finite-offset probabilities, or a complete marked length spectrum is identical. The surrounding theorem makes that scope available; it should remain explicit in summaries.

### R61-M6. The determinant contribution is indispensable to the quoted response

For identical even contact graphs, write

$$S(u)=au^2/2+t_4u^4/24+O(u^6),\qquad B(u)=1+\beta u^2+O(u^4).$$

The stationary envelope gives the quartic action derivative

$$\partial_q t_4=1+2\sum_{i\ge1}e^{-4i\gamma}=\coth(2\gamma).$$

At quadratic endpoint degree, the direct mixed-edge term has no $q$ contribution. The Hessian variation is diagonal, however, so the relative determinant contributes

$$\partial_q\beta=-\sum_{i\ge1}G_{ii}e^{-2i\gamma}=-\frac1{4a\sinh(2\gamma)}.$$

Both contributions enter the normalized positive-part integral:

$$\mathcal R_\infty(0)=\frac{2\beta}{3a}-\frac{t_4}{12a^2},\qquad \partial_q\mathcal R_\infty(0)=-\frac{\cosh(2\gamma)+2}{12a^2\sinh(2\gamma)}.$$

The residual weight vanishes on the boundary, so its first variation produces the displayed interior quartic integral without a boundary contribution. Higher even graph degrees do not enter this first offset coefficient. These are the steps checked in Proposition A.4.1, p. 116. [S6]

At $g=\kappa=1$, one has $a=\sqrt3$, $\cosh(2\gamma)=7$, and $\sinh(2\gamma)=4\sqrt3$. Thus

$$\partial_q\mathcal R_\infty(0)=-\frac{\sqrt3}{48},\qquad \frac{d}{ds}\mathcal R_\infty^{(s)}(0)\bigg|_{s=0}=\frac{\sqrt3}{2}.$$

Omitting the determinant-amplitude contribution would instead give $7\sqrt3/18$. The independent symbolic control distinguishes these values. The finite-chain coefficient formula was also evaluated through exact rational Jacobi/Schur algebra in 21 cases, including the empty-interior case, with its limiting coefficient checked. These finite controls support normalization, not a general proof of the long-bridge limit. [D2]

Two logically different observations must not be conflated. The nonzero derivative of $\mathcal R_\infty$ proves variation of the scalar normalized probability $\mathcal F^{(s)}(d)$ for sufficiently small positive $d$. Variation of a scalar unconditioned mass alone would not prove variation of a conditional endpoint law. The revised introduction supplies the separate reason for the latter: different fourth contact jets, the signed action inverse, and the one-offset law inverse. That is the appropriate argument. [S1, S5–S6]

This realized comparison is a genuine illustration of the mechanism, not an example that invalidates the main rigidity theorem. It demonstrates information beyond the leading truncation of the same experiment. It does not establish a hierarchy relative to other inverse data.

## 5. Significance after the expository revision

### R61-E1. The affirmative case is now coherent, but still does not support my positive recommendation

The best case for the paper is now clearly visible. It starts from a physically defined rare-event ensemble, retains nonlinear endpoint actions in a relative long-bridge limit, proves that those actions have an actual-smooth geometric inverse, and uses the recovered images to reconstruct an unregistered periodic table. Long-flight conditioning is not being replaced by a Gaussian approximation, and the unknown lattice and channel poses are not supplied as metric answers. The realized family makes the loss in the leading approximation concrete. These points deserve credit. [S1–S7]

The remaining question is whether the depth and reach of this particular mechanism are exceptional enough for the requested general journals. My answer remains negative on the present submission, for more specific reasons than its length or its use of rich observations.

The analytical construction is confined to small collars of deliberately selected alternating clear channels. There, strict convexity and a positive gap give a uniformly diagonally dominant nearest-neighbor variational problem. The hardest estimate is a carefully organized relative determinant limit for two localized ends. The subsequent jet isolation exploits the stationary envelope and geometric visit sums. These arguments are substantive, but the exposition does not show that they overcome a comparably broad obstruction elsewhere in billiard dynamics or substantially change an established inverse-data regime. This is a judgment about the demonstrated mathematical reach of the proved mechanism, not a demand to solve a different problem as a correctness repair.

The realized separation strengthens the interpretation of that mechanism, but the comparison is between a leading quadratic record and a nonlinear function-valued record within the same specially designed experiment. A change in higher jets while lower jets and area are fixed is not, by itself, an exceptional inverse phenomenon. The actual accomplishment is showing that the long-bridge law retains and recovers those higher jets. The support-family computation confirms this accomplishment; it does not constitute an independent second major advance.

The global conclusions are genuine and should not be called supplied geometry. Nevertheless, once complete local analytic images have been recovered, much of the remaining route is analytic propagation, finite incidence congruence matching, and reconstruction from marked translation cycles. The differential and finite-coordinate conclusions have their additional model hypotheses. The v60 conditional stability result is useful but remains local, prior-dependent, and distinct from acquisition. The cover letter now acknowledges these dependencies, which improves accuracy but does not automatically change their significance.

I therefore regard the revision as a successful clarification of a mathematically coherent contribution, not as a convincing answer to the strongest general-journal importance question. Another specialist might value the relative/action mechanism more highly. I do not claim redundancy, lack of novelty, or universal agreement with this placement judgment. The reason for declining is not that no new theorem was appended in v61.

### R61-E2. Further nominal repair iterations would misdescribe this report

The requested mechanism-centered reorganization has been carried out. I do not request another introduction rewrite merely because the placement recommendation remains adverse. Nor do I ask for ordinary marked-length rigidity, unmarked channel discovery, or unrestricted finite-scalar global recovery as corrections to the stated theorems. These are different inverse problems.

The introduction still repeats several distinctions between diagonal and full inversion, analytic and smooth categories, and exact laws and samples. Some of that repetition could be compressed in a final editorial pass, with no loss of hypotheses or proofs. This is a minor expository observation, not a barrier whose repair would secure acceptance. Arbitrary deletion of mathematical material is not requested.

## 6. Primary literature and scope

The targeted check was refreshed using primary records. Finamore–Leguil's finite-horizon Sinai theorem uses an enriched marked length datum. Its definition and Theorem A were checked on printed pp. 4–5, including the distinction between the enriched lengths and actual periodic billiard lengths. De Simoi–Kaloshin–Leguil treats analytic open billiards with non-eclipse and the stated symmetry/genericity assumptions. Neither comparison establishes a reduction to or from the present conditional endpoint-law observation. [L1–L2]

Osius supplies association-model context for eliminating marginal factors, not the billiard relative determinant or contact inverse. Trefethen supplies context for conditional analytic continuation under a complex-domain bound, not the specific billiard mechanism. Florio–Leguil's version-5 correction removes an affected geometric open-billiard spectral-rigidity assertion while retaining dynamical conclusions; the removed claim is not available as a theorem to use against or within this manuscript. [L3–L5]

These checks are not an exhaustive priority investigation or proof audits of the cited papers. No claim that the manuscript is already known, and no first-priority assertion, follows from them. The revised literature discussion respects these limits.

## 7. Disposition for the next step

**R61-D1 — Correctness within coverage:** no new mandatory core repair or realized counterexample is established. The emphasized finite-flight inverse and nonlinear comparison withstand this examination. This is not a certificate for the entire corpus.

**R61-D2 — Response to the previous report:** the mechanism-centered presentation request has been addressed. It should not be marked unaddressed solely because this reviewer remains unconvinced about placement.

**R61-D3 — Preserve the scope:** retain the selected marked observation model, the distinction between complete laws and finite scalar samples, fixed-order real estimates versus analytic all-order estimates, global matching alternatives, and the substantive acquisition dependency. The current rewrite does not remove these qualifications.

**R61-D4 — Editorial recommendation:** decline at the requested level on the present significance case. A further assessment should be an independent judgment of the central mathematical contribution, not an exercise in manufacturing another technical gap or declaring this judgment closed by an extra lemma or build receipt.

## 8. Independent reproduction and limits

The downloaded native artifact has SHA-256 `8a08c96bbaaae1a9fc15c4f292bb899c0b7cfab25ac286b6e696eafd699e8b56`. The verifier checked the lengths, SHA-256 values, and Git blob identities of **753 frozen files**, reconstructed the manuscript subtree above, checked **123 distinct active inputs**, and verified **45 build-report evidence entries**. Active path counts are 113 full, 44 principal, and one companion, with overlaps. The separate comparison with the v60 archive gives the preservation findings in Section 2. [D1]

Fresh builds used regenerated auxiliary files, in companion/full/principal order, with shell escape disabled. All **420 pages** match the native PDFs in extracted text and same-renderer 72-dpi RGB arrays. PDF bytes differ. Final logs contain one principal and three full-manuscript underfull notices, none in the companion, and no match for undefined references/citations, missing characters, overfull boxes, or LaTeX errors. Actual visual inspection covered principal pp. **4, 8, 116, and 117** at 108 dpi; no clipping or unreadable mathematical expression was observed on these pages. All-page computational parity is not all-page visual inspection. [D1]

The independent mathematical script imports no author checker. It verifies the exact support-area polynomial and graph jet, the quartic action/amplitude response and an omitted-amplitude negative control, 48 exact tridiagonal cofactor cases, and 21 finite Jacobi/quartic coefficient cases. Normal and optimized Python emit identical JSON. These checks do not certify arbitrary-order smooth factorization, a Banach-space inverse, trace-class convergence, global continuation, or statistical risk bounds. The author's own preservation/checker program was not rerun; source identities were checked independently. [D2]

## Source keys

All S-keys refer to source `71e0bd6306f54466728c2e6e781bb0f422c5cfb0` under the manuscript directory in Section 1. [Immutable source root](https://github.com/TrillionniumFoundation/theta-theory/tree/71e0bd6306f54466728c2e6e781bb0f422c5cfb0/papers/A2-v17-boundary-information-coarsening).

- **S1:** `rigidity.tex`; `main.tex`; `journal/00_principal_introduction_v61.tex`, lines 1–410. Revised abstracts and principal pp. 2–9, especially finite-flight discussion p. 4 and realized comparison p. 8.
- **S2:** `v3/10_geometry_action.tex`, geometric localization, Jacobi reduction and the nonlinear relative-flux lemma; `v3/20_integration.tex`, lines 1–91, physical measure and common-domain integration. Further marked and threshold-interface corollaries are not necessary to the new emphasis.
- **S3:** `v4/10_boundary_layers.tex`, especially lines 1–326. Half-lines, relative factorization, and the physical limiting law; Theorems 7.2–7.3, pp. 20–22.
- **S4:** `article/23a_signed_endpoint_rigidity_v27.tex`, especially the weighted inverse, finite envelope, actual-smooth factorization and homogeneous isolation, lines 130–473, together with the printed signed block statement. This is not an assertion of a new complete audit of every downstream continuation proof.
- **S5:** `article/23f_single_offset_law_inverse_v42.tex`, lines 1–174. Density-ratio inverse, fixed-order stability, and Corollary 13.3, p. 61.
- **S6:** `v4/20_nonlinear_information.tex`, lines 1–195. Proposition A.4.1, p. 116, finite coefficient formula p. 117, and Theorem A.4.2, pp. 117–118.
- **S7:** `journal/01_structural_statements_v56.tex`; `article/00b_interaction_overview_v51.tex`; `journal/DEPENDENCY_LEDGER_V61.md` and its retained v60 declaration. The analytic inverse files `article/23a2_analytic_contact_inverse_v59.tex` and `article/23a3_conditional_observation_inverse_v60.tex` are byte-identical to the reviewed baseline. The global/analytic/statistical proofs are not all freshly recertified here.
- **R1:** [Prior v60 report](https://github.com/TrillionniumFoundation/theta-theory/blob/396bb28e17ba9944af5ff89a2db601412eeb95ee/reviews/a2-v60-independent-harsh-top4-2026-09-16/REFEREE_REPORT.md).
- **R2:** `RESPONSE_TO_REFEREE_V61.md`, `COVER_LETTER_V61.md`, `HISTORICAL_DERIVATION_AUDIT_V61.md`, and `LITERATURE_CHECK_V61.md` at the compiled source. These are author-side arguments and provenance.
- **D1:** `AUDIT_LEDGER.md`, `AUDIT_RESULTS.json`, and `verify_delivery.py` in this review directory; downloaded native artifact 10426471183; GitHub source-to-review-ready comparison.
- **D2:** `independent_checks.py` in this review directory. Full emitted output and fresh build logs accompany the downloadable audit package. The code and summarized exact results are also retained in the branch.
- **L1:** Douglas Finamore and Martin Leguil, *A CAT(0)-approach to the marked length spectral rigidity of Sinai billiards*, [arXiv:2510.18983](https://arxiv.org/abs/2510.18983), definition and Theorem A on pp. 4–5.
- **L2:** Jacopo De Simoi, Vadim Kaloshin and Martin Leguil, *Marked Length Spectral determination of analytic chaotic billiards with axial symmetries*, [arXiv:1905.00890v4](https://arxiv.org/abs/1905.00890v4), related DOI 10.1007/s00222-023-01191-8.
- **L3:** Gerhard Osius, *Asymptotic inference for semiparametric association models*, [arXiv:0903.0702](https://arxiv.org/abs/0903.0702), Annals of Statistics 37 (2009), 459–489.
- **L4:** Lloyd N. Trefethen, *Quantifying the ill-conditioning of analytic continuation*, [arXiv:1908.11097](https://arxiv.org/abs/1908.11097).
- **L5:** Anna Florio and Martin Leguil, *Smooth conjugacy classes of 3D Axiom A flows*, [arXiv:2010.04120v5](https://arxiv.org/abs/2010.04120v5), including the correction notice.
