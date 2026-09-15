# Independent referee report on A2, revision 56

**Manuscript:** *Boundary laws and rigidity of periodic dispersing billiards*  
**Author:** Qian Qi  
**Date:** September 15, 2026  
**Requested standard:** Annals of Mathematics / Inventiones Mathematicae / Acta Mathematica / Journal of the American Mathematical Society.

This is an author-requested, AI-assisted referee-style assessment. It is not a commissioned journal report, an institutional endorsement, or an editorial decision. The mathematical and placement judgments below are separate from the reproducibility checks.

## 1. Recommendation and exact object of review

**I do not recommend acceptance at the requested highest general-journal level on the present evidence of exceptional significance.** This is not a finding that the central theorem is false. In the proof interfaces examined here, I have not established a fatal error in the relative boundary law, the actual-smooth signed contact inverse, the finite periodic reconstruction, or the differential rigidity argument. The new graph-to-support lemma is correct under its stated local hypotheses.

The article-level judgment must nevertheless be updated rather than copied from the v55 report. Revision 56 has a real principal article, not merely a new abstract attached to the old 283-page manuscript. Its presentation now places the difficult relative normalization and actual-smooth factorization before the periodic consequences. **The former objection that the principal submission gives the ancillary probability catalogue the same structural prominence as the geometric inverse is substantially resolved.** Length reduction alone is not the improvement: the proof hierarchy is materially clearer.

I identify one specific dependency-description correction, **R56-C1**, concerning Corollary 19.9. It is an explicitly external-theorem-dependent consequence, not merely an external comparison. This does not invalidate Theorems 1.1, A or B, and it is not a sufficient reason by itself to reject the paper. I request no new stopped-experiment theorem, no reduction of the principal rigidity statement, and no arbitrary deletion of the retained technical corpus.

The mathematical source reviewed is frozen at:

- source branch: `revision/a2-v56-principal-proof-architecture-2026-09-15`;
- source commit: **`ae0eea2a3368b01a72ab6eaf50bad0cfb50ec8de`**;
- manuscript subtree: **`d554cd4c53737717594a5e30d97978238055bbb2`**;
- manuscript directory: `papers/A2-v17-boundary-information-coarsening/`;
- native product branch: `revision/a2-v56-native-products-34952042203-1`;
- native workflow run: **34952042203**, artifact **10389393610**.

The historical directory name does not identify the current revision. The current principal entry is **`rigidity.tex`, 106 pages**; the full technical entry is **`main.tex`, 283 pages**; the two-collision companion is **seven pages**. Page references in this report refer to the 106-page principal PDF unless expressly prefixed F. Source and artifact identities must not be interchanged. [D1]

The fresh mathematical reading concentrates on the new principal introduction and graph/support appendix, the full two-ended relative-factorization argument, the actual-smooth finite-jet argument, the density and interior-window extraction, the clear-channel skeleton, finite congruence matching, and the moving-family differential and finite-coordinate arguments. I also checked the two-table example's main construction. This is **not** a fresh line-by-line certification of all 396 delivered pages. In particular, the entire statistical-experiment catalogue, the full physical-acquisition theorem used by Corollary 19.9, and the companion's complete mathematics are not certified by this report. A complete rebuild has much broader mechanical coverage than this proof audit. [S1–S10, D1]

## 2. Disposition of the previous report

The addressed v55 report is `reviews/a2-v55-independent-harsh-top4-2026-09-15/REFEREE_REPORT.md`, frozen at **`5015444dc016dec38a7d0f0130b818823bbabd4e`**. It concerned actual mathematical source **`3903f5b8a5ffb0d0a69065b1d303c247c06ebf69`**, not the present source. It identified no mandatory new mathematical correction within its coverage and explicitly warned against an endless sequence of elementary probability additions. Revision 56 correctly does not answer that warning with another stopped-binary-experiment result. [R1–R2]

| Previous reservation | Finding in v56 | Disposition |
|---|---|---|
| R55-E1: put the main analytical mechanism ahead of ancillary probability reductions | Theorem 1.1 now leads, with a proof map to the relative determinant and actual-smooth arguments. | Substantially addressed. Renumbering is not presented as a new independent theorem. |
| R55-E2: explain the strength of the observation | Signed coordinates, known positive offsets, selected marked channels, retained gaps, function-valued laws, analyticity and model-local finite coordinates are separated. | Scope is accurately disclosed. Importance remains an evaluative question, not a hidden-hypothesis objection. |
| R55-E3: principal-article hierarchy | A separately compiled 106-page geometric article is provided while the full corpus remains available. | The old organizational objection should not be repeated unchanged. R56-C1 is the narrower remaining dependency issue. |
| R55-M1–M5: stopped-record distinctions | No new theorem in that direction is claimed here. | No reopening on the basis of reorganization; no fresh certification of the entire older probability material is implied. |
| R55-G1–G5: geometric proof interfaces | The selected interfaces have been re-examined, with an internal graph/support conversion now supplied. | No new fatal defect established in this coverage. |

The preservation claims in the response concern provenance. They do not establish importance or mathematical correctness. This audit independently checks the current frozen tree and active sources; it does not claim to have independently recounted every v55-to-v56 theorem/proof block merely because the author provides preservation counts. [R2, D1]

## 3. Mathematical assessment of the principal mechanism

### R56-M1. The relative determinant argument addresses the genuinely dangerous scale

The reference mixed derivative is exponentially small:

$$d_j^0=\frac{\sqrt{a_0a_p}}{\sinh(j\gamma)},\qquad p=j\bmod 2.$$

It would be wrong to derive the claimed relative limit by taking an arbitrary absolute stationary-action error and dividing by this quantity. That is not the argument printed in Theorem 7.2, beginning on p. 17. The proof first uses the exact normalized cofactor identity

$$\log b_j=\sum_i\log\{g[-\ell_{uv}(y_i,y_{i+1})]\}-\log\det(I+G_j\Delta H_j).$$

The perturbation of the reference tridiagonal Hessian is localized at the two endpoint layers. Summing its entries gives a trace-norm bound independent of the bridge length; a crude operator estimate multiplied by the number of collisions is not substituted. The finite Green operator is then compared on the two end compressions with the corresponding half-line operators. Tail removal, the remote reflected terms, and the interaction between the two ends are controlled before the small reference twist is eliminated. [S2]

The determinant comparison uses a trace-class difference and a geometric majorant. In particular, for operators of norm below a fixed number less than one, the trace-series difference retains a bound of the form

$$|\operatorname{tr}(T^m-\widetilde T^m)|\le m q^{m-1}\|T-\widetilde T\|_1.$$

At any separately fixed derivative order, polynomial factors can be absorbed by a strict exponential margin. This does not yield a bound uniform over every derivative order, and Theorem 1.1 expressly does not assert one. The weighted orbit construction, endpoint gluing, and compressed determinant comparison have to be read together; the determinant formula alone would not prove the theorem. [S1–S2]

The fixed-offset law in Theorem 7.3 uses the full-phase flux formula and common-domain integration. It retains nonlinear half-line actions on a flight-independent collar. It does not infer density convergence merely from weak convergence or replace the nonlinear actions with their Hessians. The selected-channel locality argument also distinguishes a channel's own gap from the smallest gap of the whole table. These are substantive features of the argument. I have not established a flaw at this interface. [S2, S6]

### R56-M2. The signed inverse is an inverse for actual smooth finite jets, not just formal series

Lemma 12.4, pp. 44–45, is necessary to justify the eventual coefficient inversion. Two actual smooth graph pairs with the same gap and the same graph jets through order M are interpolated. On a finite stationary action sum, differentiation cancels the interior orbit variations. The terminal contribution is retained and estimated before the infinite limit is taken. The direct variation of each flight is bounded by the order-M+1 graph remainder evaluated along an exponentially decaying orbit. Integrating the finite identity first gives

$$|S_b^{[1]}(u)-S_b^{[0]}(u)|\le \frac{C_M}{1-\rho^{M+1}}|u|^{M+1}.$$

The assumptions involve functional smooth bounds, positive curvature and gap margins, not just bounds on a finite list of Taylor coefficients. Flat smooth remainders therefore do not invalidate the finite-jet statement. Conversely, this argument does not identify arbitrary smooth boundary germs from equality of all Taylor coefficients; the later global image argument uses analyticity. [S3]

At degree n, the highest new graph jets enter through

$$M_n=\begin{pmatrix}
\coth(n\gamma)&r_0^n\operatorname{csch}(n\gamma)\\
r_1^n\operatorname{csch}(n\gamma)&\coth(n\gamma)
\end{pmatrix},\qquad r_0r_1=1.$$

The endpoint multiplicity is one and interior multiplicity is two. Summing the linear half-line orbit contributions gives the displayed diagonal and off-diagonal entries, and

$$\det M_n=\coth^2(n\gamma)-\operatorname{csch}^2(n\gamma)=1.$$

Subtracting the lower-order remainder therefore gives an invertible triangular block at each finite order, including odd signed coefficients. Determinant one alone does not imply uniformly good conditioning as n grows. The source keeps the fixed-order qualification. Independent exact checks of 90 rational blocks reproduce the determinant, inverse and geometric-series multiplicities; these finite checks do not prove the smooth remainder estimate. [S3, D2]

A minor wording improvement is available in Theorem 1.1(3): specify that the graph jets agree **at the anchored contact**, whereas the common collar is where the functional bounds hold. The detailed Lemma 12.4 already has the intended meaning. I do not regard this wording as a substantive mathematical gap. [S1, S3]

### R56-M3. The new graph/support appendix supplies the needed local interface

Lemma A.1.1 on p. 99 is the genuinely new local proof interface in this revision. For a boundary graph $(-\psi(y),y)$ with $\psi''(0)=\kappa>0$, it uses

$$\psi'(y(p))=p,\qquad H(p)=-\psi(y(p))+py(p),\qquad H'(p)=y(p),$$

and

$$h(\theta)=\cos\theta\,H(\tan\theta).$$

The coefficient of degree k in the inverse y(p) needs the graph derivatives only through order k+1. Integrating H'=y then shows that the support jet through order m needs the graph jet only through order m. A naive differentiation of the unsimplified composition can obscure this finite-order property; the stationary identity makes it explicit. The implicit function theorem supplies the actual-smooth and parameter-dependent interpretation. [S4]

With $q_n=\psi^{(n)}(0)$, an independent finite calculation gives

$$h''(0)=\kappa^{-1},\qquad h'''(0)=-q_3\kappa^{-3},$$

$$h^{(4)}(0)=2\kappa^{-1}-q_4\kappa^{-4}+3q_3^2\kappa^{-5}.$$

The check through degree six contains no higher graph derivative than the requested support order. These are controls on the local formula, not a replacement for the lemma's proof for arbitrary fixed order. Reversing the second outward normal together with the positively oriented tangent gives the known factor $(-1)^n$ on its graph coefficients; it does not introduce an unobserved relative pose. [S4, D2]

This appendix properly removes the differential image proof's need to import quantitative statistical hypotheses merely to use a local coordinate conversion. It is an elementary geometric lemma, not a new general principle of convex geometry. The manuscript accurately describes it that way. [R2, S4]

### R56-M4. Law inversion and interior windows preserve signs and state the observation honestly

On a centered positive square, the four-density ratio satisfies

$$1-\frac{f(u,v)f(0,0)}{f(u,0)f(0,v)}=t(u)t(v),\qquad t=\frac{S}{d-S}.$$

A nonzero scalar anchor determines the positive normalization of t; inversion gives $S=dt/(1+t)$. This avoids an unjustified pointwise square root at the minimum, and it preserves odd coefficients in the signed coordinate. Separate positive marginal recording factors cancel. An independently chosen polynomial control with a nonzero cubic term recovers its third derivative exactly; it is not asserted to be a realized billiard law. [S5, D2]

The interior-window theorem, Theorem 14.6 beginning on p. 60, does not secretly use the unobserved cap boundary. Under its hypotheses,

$$\partial_{xy}\log p(x,y)
=-\frac{S'(x-\xi)S'(y-\eta)}{[d-S(x-\xi)-S(y-\eta)]^2}.$$

The visible vertical and horizontal zero lines locate the origins. The argument requires both origins to lie in the window, a unique nondegenerate minimum on the relevant action interval, positive denominators and usable anchors. The local smooth extraction takes place in the stated strong density topology with margins. It is not a total-variation-to-derivatives theorem, an unknown-unit calibration theorem, or a recovery result from the fixed rectangular support alone. Those stronger assertions should not be attributed to the manuscript. [S5]

The exact-fiber and differentiated-nuisance conclusions also have to be separated from acquisition cost. Multiplying the two recording factors by a small positive constant can leave the conditional law unchanged while reducing acceptance mass. No uniform physical preparation budget follows from the normalized-law inverse without additional information. The source preserves this distinction. The full acquisition theory therefore remains a separate theorem, which matters for R56-C1 below. [S5–S6]

### R56-M5. The finite skeleton and finite-fiber construction do not supply the lattice covertly

Theorem 19.3, p. 82, does not assume that every closest pair is clear. If a third body meets a closest segment, the two replacement gaps have total length at most the original gap, and each is shorter by a uniform positive separation. Induction yields a finite path of clear pairs. This is a graph path, not a physical specular itinerary and not a claim about its travel time. [S6]

Projecting paths to all obstacle representatives and to two marked deck translates gives a finite connected quotient graph with rank-two cycle gains. A spanning tree and two additional edges yield the N+1 architecture. The contact Hessian is positive definite, and finitely many selected clearances persist; bounds using the smallest singular value of the lattice reduce the potentially relevant translated obstacles to a finite set. This correctly supplies local persistence rather than assuming infinitely many clearances automatically remain positive. [S6]

The two integer gains need not form a unimodular basis. With their matrix M and recovered translations $v_1,v_2$, the reconstruction uses

$$L=(v_1\ v_2)M^{-1},$$

not an unannounced identification M=I. A simple exact control with determinant-six M confirms the distinction. This is a check of the cochain formula, not an additional billiard realization. [S6–S7, D2]

For a noncircular analytic obstacle, its proper symmetry group is finite. Theorem 20.3 enumerates finitely many incidence congruences, reconstructs candidate placements and lattices, and separately checks admissibility: positive lattice orientation, disjoint lifted bodies, clear selected channels, and consistency of incident images. Solving the finite displacement equations alone would not establish these geometric properties. The proof accounts for both directions of the fiber classification. [S7]

The noncircular two-table construction illustrates an actual discrete ambiguity, while the circular comparison concerns a continuous ambiguity outside the noncircular hypothesis. These are not counterexamples to the stated finite-fiber or differential theorem. The N+1 count is minimal for the specified connected two-cycle mechanism, not an information-theoretic lower bound for every possible inverse observation. Complete endpoint laws remain infinite-dimensional data. [S6–S8]

### R56-M6. The differential theorem does not infer immersion from exact injectivity

The common-strip hypothesis is doing real work. The derivative of an analytic support family must itself be analytic for the identity theorem to eliminate a variation from its vanishing contact jets. Individual analyticity of each parameter slice, without the stipulated family control, would not justify that step. [S9]

The forward differentiation includes the moving reference inverse,

$$\dot G=-G\dot H^0G,$$

as well as the derivative of the subtracted Hessian. Nondecaying reference terms cancel before the trace-class summation. The normalizing integral is differentiated in positive-part form; dominated convergence off its regular boundary level gives the derivative without an artificial boundary Dirac term. [S9]

Zero density variation gives zero action and graph-jet variation at each fixed order. The internal graph/support lemma and analytic identity theorem then give zero entire channel-frame shape variation. At a finitely symmetric base table, an actual local angular branch is selected along the family; the proof does not assume that the base symmetry survives a symmetry-breaking perturbation. The cochain then eliminates relative placement and lattice variation. Thus the remaining kernel has the stated common Euclidean form

$$\dot h_i(\theta)=a\cdot n(\theta)-\omega h_i'(\theta),\qquad \dot L=\omega J L.$$

These steps substantiate Theorem 21.5, p. 97. [S4, S7, S9]

For Theorem 21.6, finite-dimensionality enters only after the full derivative separates tangent vectors. Selecting a basis from the gap and test-expectation differentials and applying the inverse function theorem gives local coordinates on the immersed model. The lower Lipschitz estimate uses uniform closeness to the base Jacobian on a convex ball, not pointwise nonsingularity alone. This is a valid model-local consequence, not a fixed finite measurement vector reconstructing the whole analytic class. [S9]

## 4. R56-C1: semantic dependence is not decided by the location of a reference label

The native products have no unresolved-reference failure, and the F-prefix convention is visible. The narrower problem is the classification of those references in the response and proof-independence narrative. The response describes nine external references as comparisons and reports that no full-only label occurs inside a principal proof environment. It also correctly disclaims a semantic proof certificate from this static check. The present example explains why that disclaimer is necessary. [R2, S10]

**Corollary 19.9, p. 87**, `article/23j_generic_finite_channel_rigidity_v45.tex`, lines 493–515, assumes the uniform analytic, chart and physical-record conventions of **Theorem F.47.3**. Its conclusion applies that theorem to the persistent N+1 design. Its proof invokes the finite-signature and compact-inverse arguments followed by the charged pilot and capped fresh-stage estimator. Those are substantive inputs from the full technical manuscript. They are not constructed in this principal proof merely because the label to F.47.3 is placed in the corollary's statement rather than between the proof delimiters. [S6, S10]

The corollary is a legitimate conditional application of an external theorem; citing such a theorem is not itself an error. Nor is the dependency hidden from a careful reader of p. 87. The correction is to the broader description: **this item is an external-theorem-dependent corollary, not just a comparison reference.** A syntax-only checker cannot establish that every printed proof is mathematically independent of the full manuscript.

For the next revision, identify this item explicitly in the dependency ledger and near the statement. A suitable clarification is that the principal geometric theorems have their supporting proofs internally, while Corollary 19.9 additionally uses F.47.3 and its observation/acquisition assumptions. The proof can then be read as a verification of that external theorem's design hypotheses. Full duplication of the acquisition proof is not required, and deletion of the corollary or of the wider corpus is not required.

I found no path from this physical-acquisition consequence back into the examined proofs of Theorems 1.1, A or B. Consequently this is **not** a demonstrated circularity in the central rigidity theorem. It is a concrete correction to the proof-dependency claim and to the classification of what is self-contained. It should neither be ignored nor inflated into a fatal mathematical objection.

## 5. Originality and significance at the requested level

### 5.1 What should carry the paper's case

The strongest material is the relative nonlinear long-bridge law coupled to the actual-smooth signed inverse. The new introduction now makes that case in an intelligible order. The finite skeleton, analytic globalization, finite symmetry bookkeeping and differential kernel give consequential geometric conclusions; they are not merely a list of unrelated probability calculations. I therefore withdraw the old, broader organizational criticism insofar as it described the entire submission as an undifferentiated 283-page catalogue. [S1–S9]

At the same time, the components have different levels of difficulty and originality. Once the special density form is available, eliminating separate marginal factors is an association identity. Once full analytic boundary images are recovered, Fourier congruence matching and the lattice cochain are comparatively direct finite operations. Once tangent vectors are separated, the finite-dimensional coordinate selection is linear algebra and the inverse function theorem. The article's exceptional-significance case should not be based on assigning the same conceptual weight to all these consequences as to the relative normalization and smooth remainder mechanism.

This is a distinction in the architecture of the proof, not a claim that the central analysis is elementary or that applications of standard tools lack value. The current exposition itself makes many of these distinctions correctly. The new graph/support appendix improves the independence of the proof, but its addition does not by itself enlarge the underlying inverse problem solved.

### 5.2 What the observation does and does not establish

The complete periodic conclusion uses selected marked clear channels, signed physical endpoint coordinates, known positive excess times, separately retained gaps, complete function-valued conditional laws, and analytic continuation. The unknown Euclidean lattice and inter-channel placement are genuinely recovered rather than supplied. Noncircularity and proper asymmetry have distinct roles in finite ambiguity and uniqueness. These are substantial conclusions within the specified observation model. [S1, S6–S9]

A finite number of channel labels is not a finite amount of scalar information. Local exact analytic determination is also not unrestricted stable reconstruction from weakly accurate measurements. The finite-dimensional scalar-coordinate theorem and the separately conditioned physical-acquisition theory do not erase these distinctions. They answer different, explicitly qualified questions. [S1, S5, S9]

None of these facts is a defect merely because the observation is rich. A rich-data inverse theorem can be important. My reservation is that the present text and the limited primary-source comparison still do not persuade me that this particular inverse and mechanism have the exceptional depth or impact warranting the requested placement. That is a referee's evaluative judgment, not a mathematical theorem about publishability, and it could reasonably receive a different assessment from another specialist.

### 5.3 Primary-source comparison and its limits

Finamore and Leguil's *A CAT(0)-approach to the marked length spectral rigidity of Sinai billiards*, arXiv:2510.18983v1, concerns finite-horizon Sinai billiards and **enriched** marked length data. Its primary record and the enriched datum/Theorem A were checked. It must not be described as a theorem using only ordinary periodic-orbit marked lengths. No reduction between that datum and the present conditional boundary-law observation has been established here. [L1]

De Simoi, Kaloshin and Leguil's analytic open-billiard result, arXiv:1905.00890v4, works with non-eclipse and stated symmetry/genericity restrictions and marked length data. Its assumptions and observation map differ from those of this periodic-law manuscript. The existence of that work does not prove the current theorem redundant; the current theorem does not automatically solve its inverse problem either. [L2]

Osius's association-model work explains why unknown marginal distributions and an odds-ratio description must be distinguished. It supports assigning the marginal-cancellation identity to established background rather than treating cancellation alone as the new geometric theorem. The nonlinear billiard realization and smooth inverse require separate analysis. [L3]

The version history of Florio and Leguil's arXiv:2010.04120v5 explicitly records removal of a geometric spectral-rigidity conclusion affected by an error, while retaining and improving dynamical conclusions. The current manuscript's version-specific distinction is appropriate; it should not cite an obsolete geometric assertion as an established theorem. [L4]

This is a targeted primary-source check, not an exhaustive priority survey or a proof review of all four cited works. I make no claim that the central boundary-law theorem is already in the literature, and no categorical claim of first priority. Strengthening the contribution explanation is a matter of mathematical comparison and exposition, not a demand to solve an unrelated stronger problem as the price of closing an old objection.

## 6. Required disposition and next-review criteria

**Specific correction identified:** R56-C1, the classification and explicit declaration of the external acquisition-theorem dependency of Corollary 19.9. The anchored-jet wording in Theorem 1.1 is a minor clarification, not a new proof requirement.

**New mandatory core mathematical repair established by this review:** none within the stated coverage. This statement does not certify every theorem in the principal article, much less all results in the full manuscript. It records what this audit did and did not establish.

**Recommendation at the requested journal level:** do not accept on the present exceptional-significance case. The formerly broad article-hierarchy objection is substantially resolved. The remaining adverse placement judgment should not be disguised as an algebraic error, a missing probability corollary, or an assertion that a specialized exact-law theorem is automatically unimportant.

For a subsequent review, the meaningful object is the principal relative/smooth inverse and its changed substantive presentation. Counting another revision, adding a further consequence of the stopped two-point experiment, or obtaining another clean build should not be treated as progress on that editorial question. Conversely, an adequately closed mathematical point should remain closed unless a precise new defect is demonstrated.

## 7. Independent verification and limitations

The downloaded artifact SHA-256 is

`32fa3e4c3235a648a3ee8a96a1c0b122cd76ff0d2a366070f40e154991ce006a`.

The audit independently verified the bytes, SHA-256 and Git blob hashes of **662 frozen source files**, reconstructed the Git manuscript subtree, and obtained the pinned subtree identity above. Active source inputs are **110 for main**, **41 for rigidity**, and **one for the companion**, with **120 distinct sources in their union**. Main plus the separately compiled companion account for the familiar 111-source full delivery; imported generated auxiliary files should not be counted as new mathematical sources. [D1]

All three entries were rebuilt from the extracted source with shell escape disabled. The 106 principal pages, 283 full-manuscript pages and seven companion pages agree with their native counterparts in extracted text and in same-renderer 72-dpi RGB arrays: **396 pages compared, no mismatching pages**. The rebuilt PDFs are **not byte-identical** to the native PDFs. Four principal pages—2, 44, 87 and 99—were actually inspected visually. All-page computational equality is not described as all-page human-style visual inspection. [D1]

The independent finite script checks graph/support coefficients through degree six, 90 exact rational last-jet matrices, signed four-density recovery, the mixed log derivative and a nonunimodular lattice control. Ordinary and optimized-Python runs give identical output. No author's checker is imported. These are finite diagnostic controls and do not certify trace-class limits, arbitrary-order smooth factorization, analytic continuation, or global rigidity. [D2]

## Source and audit keys

All S-keys refer to the frozen source **`ae0eea2a3368b01a72ab6eaf50bad0cfb50ec8de`** beneath `papers/A2-v17-boundary-information-coarsening/`. The immutable source root is:

https://github.com/TrillionniumFoundation/theta-theory/tree/ae0eea2a3368b01a72ab6eaf50bad0cfb50ec8de/papers/A2-v17-boundary-information-coarsening

- **S1:** `rigidity.tex`; `journal/00_principal_introduction_v56.tex`; `journal/01_structural_statements_v56.tex`; `article/00b_interaction_overview_v51.tex`.
- **S2:** `v4/10_boundary_layers.tex`; `v3/10_geometry_action.tex`; `v3/20_integration.tex`; principal Theorems 7.2–7.3 and their finite-bridge/integration inputs.
- **S3:** `article/23a_signed_endpoint_rigidity_v27.tex`, especially Lemmas 12.3–12.4 and Proposition 12.6.
- **S4:** `journal/02_graph_support_v56.tex`, Lemma A.1.1.
- **S5:** `article/23f_single_offset_law_inverse_v42.tex`; `journal/shared/23q_support_and_interior_windows_v52.tex`.
- **S6:** `article/23j_generic_finite_channel_rigidity_v45.tex`, especially Theorems 19.3 and 19.7 and Corollary 19.9.
- **S7:** `article/23n_finite_symmetry_v49.tex`, including the actual local angular lift and Theorem 20.3.
- **S8:** `article/23o_two_branch_example_v50.tex`, main two-table construction and completeness argument. Its auxiliary extra-gap consequence is not used to justify the principal theorem in this report.
- **S9:** `article/23m_differential_rigidity_v48.tex`, especially Theorems 21.5–21.6; the graph/support formula is supplied internally by S4.
- **S10:** `journal/full_reference_routes_v56.tex`; `RESPONSE_TO_REFEREE_V56.md`; native principal p. 87. These identify the semantic distinction in R56-C1.
- **R1:** v55 report at `5015444dc016dec38a7d0f0130b818823bbabd4e`, path specified in Section 2.
- **R2:** `RESPONSE_TO_REFEREE_V56.md` at the reviewed source commit.
- **D1:** `AUDIT_AND_REPRODUCTION.md`, `verify_delivery.py`, and `DELIVERY_VERIFICATION.json` in this review directory.
- **D2:** `check_local_mechanisms.py` and `INDEPENDENT_CHECKS.json` in this review directory.
- **L1:** D. Finamore and M. Leguil, *A CAT(0)-approach to the marked length spectral rigidity of Sinai billiards*, arXiv:2510.18983v1, October 21, 2025. https://arxiv.org/abs/2510.18983 ; enriched datum and Theorem A on printed pp. 4–5 of the primary PDF. Checked September 15, 2026.
- **L2:** J. De Simoi, V. Kaloshin and M. Leguil, *Marked Length Spectral determination of analytic chaotic billiards with axial symmetries*, arXiv:1905.00890v4, August 17, 2022; DOI 10.1007/s00222-023-01191-8. https://arxiv.org/abs/1905.00890 . Primary record/abstract scope checked September 15, 2026.
- **L3:** G. Osius, *Asymptotic inference for semiparametric association models*, Annals of Statistics 37 (2009), 459–489; DOI 10.1214/07-AOS572. https://arxiv.org/abs/0903.0702 . Primary record/association-model scope checked September 15, 2026.
- **L4:** A. Florio and M. Leguil, *Smooth conjugacy classes of 3D Axiom A flows*, arXiv:2010.04120v5, June 3, 2021. https://arxiv.org/abs/2010.04120 . Primary record and version-correction statement checked September 15, 2026.
