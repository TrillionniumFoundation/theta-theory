# Independent referee report on A2, revision 55

**Manuscript:** *Boundary laws and rigidity of periodic dispersing billiards*  
**Author:** Qian Qi  
**Date:** September 15, 2026  
**Requested standard:** the highest general mathematics journals. This is an author-requested, AI-assisted referee-style assessment, not a commissioned journal report, an institutional endorsement, or an editorial decision.

## 1. Recommendation and the object reviewed

**I do not recommend acceptance at the requested highest general-journal level on the present contribution and article-level case. This is not a finding that the principal rigidity theorem is false.** In the mathematical coverage specified here, I identify **no mandatory correction to the v55 expansion of Theorem 23.4**, and **no newly established fatal error in the inherited proof interfaces examined**. The distinction matters: an adverse placement assessment does not justify manufacturing a counterexample, reopening an adequately resolved objection, or requiring an endless succession of additional elementary results.

The reviewed delivery is `revision/a2-v55-review-ready-2026-09-15`, frozen at **`dfc6dea6d361a24223e481048889e34987491466`**. The actual compiled mathematical source is **`3903f5b8a5ffb0d0a69065b1d303c247c06ebf69`**, with manuscript subtree **`8ff45d47f7dd78bc0c0d4ae284dde147a47d87e9`**. The historical directory `papers/A2-v17-boundary-information-coarsening` contains the active v55 manuscript, not a current v17 manuscript. The main article has 283 pages; the two-collision companion has seven. The delivery layer, compiled source, and workflow-preparation commit are not interchangeable identities. [D1]

This assessment freshly examines the complete current Section 23, including the actual-table realization, finite-flight comparison, stopping theorem, and all its new clauses. It also examines the relative half-line/determinant mechanism, the actual-smooth finite-jet factorization, interior-window extraction, the clear-channel skeleton argument, finite-symmetry matching, and the differential-kernel and finite-coordinate arguments. It does **not** constitute a fresh line-by-line certification of every inherited theorem in all 290 pages. In particular, the complete older local-experiment catalogue, full calibrated-acquisition theory, every full-phase event construction, and the companion's mathematics have not received that coverage. The audit ledger makes the boundary explicit. A complete rebuild has broader mechanical coverage than this mathematical audit. [S1–S8, D1]

## 2. Disposition of the two v54 memoranda

The earlier v54 reports are frozen at `1030ca91a96ca1be8ecd0347ecbdac7084cdd8d4` and `67250d08714acf76274e82158f107246f0de7eee`. Both concern mathematical source `2cedae961195f97df802aaa81112d95cd32974e1`. Neither established a mandatory correction to the v54 stopping theorem. Their additional count and bit reductions were useful consequences, not proof that the existing theorem was false. The v55 response represents this history accurately and attributes the overlapping suggestions to both reports. [R1–R3]

| Previous issue or suggestion | Finding in v55 | Disposition |
|---|---|---|
| Uniform-in-cap removal of the terminal mark | One common kernel, exact error under the second alternative, both deficiency directions, and the sharper equal-prior risk bound are supplied. | Correctly incorporated; closed. |
| Exact censored-count risk | The integer likelihood threshold, cemetery decision, and tie convention are present. | Correctly incorporated; closed. |
| Distinguishing count risk from full-record risk | A separate full-overlap formula is printed in the theorem; only an absolute approximation is claimed. | Correct; no conflation found. |
| Finite-intensity bit reduction | A reverse kernel and a two-sided Le Cam comparison are proved, including zero limiting intensity. | Correctly incorporated; closed. |
| Very large caps | The bit can fail while the count succeeds; this is stated and proved rather than hidden. | Correct boundary of the assertion. |
| Realized charge | Count simulation preserves charge; bit simulation is expressly not asserted to do so. | Correct distinction. |
| Earlier Hellinger improvement, direct mean test, waiting-record separation, and cap necessity | Retained with their different hypotheses and observation spaces. | Previously closed points remain closed. |
| Exceptional general-journal significance | Not settled by adding these probability reductions or by successful compilation. | Separate editorial assessment. |

The author reports that the original three clauses and their proof are retained, with insertions expanding the existing theorem/proof pair rather than creating a new section or theorem number. The source inspected here is consistent with that account. The historical preservation counts in the response are provenance claims, not criteria of importance; this review's independently verified file and build counts are recorded separately. [R3, D1]

## 3. Technical assessment of Section 23

### R55-M1. The geometric probabilities and the mark laws are genuinely different inputs

The realized support family is

$$k_s(\theta)=R+s(\cos4\theta-1),\qquad R=1/10,\qquad s\in[R/128,R/64].$$

Its radius of curvature is `R-s-15s cos(4 theta)`, bounded below by `3R/4`. The integer-translated obstacles are disjoint, and the selected axis channels have common gap `g=4/5` and positive third-obstacle clearance. Different perimeters distinguish the chosen alternatives geometrically. The symmetry argument makes the relevant actual actions even; it does not make them exact quadratic polynomials. [S2, realization proof]

The fixed recording profile on a common collar is proportional to

$$\frac{1}{B_s(u)(d-S_s(u))}.$$

It can be made positive, smooth, and at most one. It is fixed as the window shrinks, but can differ between the two stipulated alternatives. That is legitimate for this two-point construction with nuisance profiles. It is not a sensor that can be programmed from an unrestricted unknown geometry, and the manuscript does not claim that stronger result.

The two contact curvatures are `80/7` and `40/3`; hence

$$\gamma_0=\operatorname{arcosh}(71/7),\qquad
\gamma_1=\operatorname{arcosh}(35/3)>\gamma_0.$$

The relative physical prefactor and the uniform window-mass estimate give

$$p_{i,h}\asymp h^2e^{-\gamma_iJ_h},\qquad
\rho_h=p_{1,h}/p_{0,h}\longrightarrow0.$$

The conditional marks instead satisfy

$$\eta_h=\operatorname{TV}(Q_{0,h},Q_{1,h})
\le C(h^4+\tau^{J_h})\longrightarrow0.$$

No relation between `h` and `tau^J` is needed for this one-stopped-record statement. The acceptance asymptotics cannot be inferred from the normalized marks alone; the proof correctly uses the forward physical probability as well. [S2, equations (23.18), (23.30)–(23.32); S3]

### R55-M2. Uniform count sufficiency and the factor one half in the risk comparison

Suppress `h`. The exact first-acceptance factorization is

$$\Pr_i(W=k,Y\in A)=p_i(1-p_i)^{k-1}Q_i(A).$$

For a cap `b`, write `a_i=1-(1-p_i)^b`. The censored count retains the numerical accepted count or a distinct cemetery outcome. In particular, acceptance at the final preparation is not confused with no acceptance by that preparation.

Projection from the full record to the count is exact. Conversely, retain the count and append an independent mark from `Q_0`, preserving the cemetery symbol. This is one kernel for both alternatives. Under alternative zero it is exact. Under alternative one, disjoint accepted-count components give error exactly

$$\sum_{k=1}^b p_1(1-p_1)^{k-1}\operatorname{TV}(Q_0,Q_1)=a_1\eta_h.$$

Consequently

$$\delta(F^{[b]},C^{[b]})=0,\qquad
\delta(C^{[b]},F^{[b]})\le a_1\eta_h\le\eta_h.$$

The supremum over deterministic caps therefore tends to zero. Summing the infinite geometric series also gives the uncapped comparison. Composing a full-record test with this kernel changes only its alternative-one error. Averaging the two errors proves

$$0\le R_C^*(b)-R_F^*(b)\le\frac12a_1\eta_h.$$

Thus the stated factor one half is justified, not an unsupported sharpening of a generic deficiency bound. The kernel preserves the count, censoring flag, and realized preparation charge pointwise. The estimate is absolute; it is not a relative-risk approximation, a result uniform over unrestricted unknown profiles, or a uniform comparison of arbitrarily many replicated stopped experiments. No such promotion is made in the theorem. [S2, equations (23.22)–(23.23) and proof]

### R55-M3. The integer threshold and the full overlap formula are both correct

For `0<p_1<p_0<1`, the accepted-count likelihood ratio is

$$\frac{p_0}{p_1}\left(\frac{1-p_0}{1-p_1}\right)^{k-1},$$

strictly decreasing in `k`. The cemetery likelihood ratio is below one. The largest accepted count assigned to alternative zero is therefore

$$K_b=\min\left\{b,\left\lfloor1+
\frac{\log(p_0/p_1)}{\log((1-p_1)/(1-p_0))}\right\rfloor\right\}.$$

The two errors of this rule are `(1-p_0)^K_b` and `1-(1-p_1)^K_b`, yielding the printed exact count risk. At an exact tie, either decision has the same risk. There is no missing final-preparation or one-based-index correction. [S2, equations (23.24)–(23.25)]

For the full record, with `q_i=dQ_i/dmu`, the smaller cemetery mass is `(1-p_0)^b`, and half the total overlap is

$$R_F^*(b)=\frac12\left\{(1-p_0)^b+
\sum_{k=1}^b\int\min\bigl(p_0(1-p_0)^{k-1}q_0,
 p_1(1-p_1)^{k-1}q_1\bigr)\,d\mu\right\}.$$

Taking `mu=Q_0+Q_1` makes the identity valid without mutual absolute continuity of the mark laws. The theorem prints this separately and does not mislabel the count formula as the full finite-sample risk. This is an important improvement in interpretability, not the repair of an error established in v54. [S2, equation (23.26)]

### R55-M4. The bit reduction has the right range of validity

The reverse bit kernel sends zero to the cemetery outcome. On one it draws the full stopped record under alternative zero conditional on acceptance by `b`. Under zero the simulation is exact; under one the cemetery mass remains exact and the accepted part has discrepancy at most `a_1`. Projection gives the other direction. This argument requires no closeness of the mark laws. [S2, equation (23.27)]

If `bp_0 -> lambda < infinity`, then `bp_1 -> 0`, `a_0 -> 1-exp(-lambda)`, and `a_1 -> 0`. Comparing the actual bit laws to the limiting Bernoulli pair and composing the kernels gives

$$\Delta_{\rm LC}(F^{[b]},L_\lambda)
\le a_1+\max\{|a_0-(1-e^{-\lambda})|,a_1\}\longrightarrow0.$$

Here the acceptance probabilities of `L_lambda` are `1-exp(-lambda)` and zero. The argument includes `lambda=0`; the limiting experiment is then uninformative. It proves an experiment comparison in both directions, not only convergence of one testing error. [S2, equation (23.28)]

When `bp_1 -> infinity`, both bit laws concentrate on acceptance, while the full/count record still distinguishes the alternatives. Contraction and the triangle inequality give reverse bit-to-full deficiency at least one half asymptotically; the kernel ignoring its input and drawing the equal mixture of the two full laws gives the matching upper bound. The large-cap exception is therefore proved, not merely illustrated. The bit simulation does not preserve the actual stopping count or its physical charge, and the manuscript explicitly says so. [S2, equation (23.29)]

### R55-M5. The original cap and finite-flight assertions remain properly separated

The common cemetery atom and the acceptance event give

$$a_0-a_1\le\operatorname{TV}(F_0^{[b]},F_1^{[b]})\le a_0.$$

They imply optimal equal-prior risk `exp(-lambda)/2` at finite intensity for the full record, not merely for an acceptance-event test. For arbitrary caps, the truncated waiting threshold proves consistency when `bp_0 -> infinity`. A bounded subsequence of `bp_0`, followed by a finite-limit subsequence, proves necessity. The exact tail-sum identity

$$\mathbb E_i\min(W,b)=\frac{1-(1-p_i)^b}{p_i}$$

charges failed preparations. The critical cap scale `p_0^{-1}` is not obtained by replacing an expected stopping time with a deterministic guarantee. [S2, original clauses and proof of Theorem 23.4]

The finite-flight corollary also retains the essential stronger input: a uniform density estimate on a fixed physical interior collar before cropping. The normalization error is `O(h^2 tau^J)`, and both window-area factors cancel in the rescaled density. A common positive floor then yields one-record squared Hellinger error `O(tau^(2J))`, hence product total variation `O(sqrt(n) tau^J)`. The direct bounded-mean test separately needs `tau^J=o(h^4)` and does not approximate the entire growing product. These two arguments must not be conflated; the source does not conflate them. [S2, Corollary 23.3]

The independent exact checks reproduce

$$\int_{[-1,1]^2}(1/9-z^2w^2)^2\,dz\,dw=224/2025,$$

and the squared Hellinger coefficient `7(a_1^2-a_0^2)^2/(16200d^4)`. This is a finite algebraic check of the expansion constants, not a numerical certificate of the limiting likelihood theorem. [D2]

## 4. Exact stress controls: limitations that are not counterexamples

A small finite example makes the distinctions in the revised theorem concrete. Set `p_0=2/3`, `p_1=1/3`, `b=2`, and take disjoint marks `Q_0=delta_0`, `Q_1=delta_1`. The count distributions, with the cemetery outcome last, are

$$C_0=(2/3,2/9,1/9),\qquad C_1=(1/3,2/9,4/9).$$

There is a likelihood tie at count two. The count risk is `1/3`, whereas the full risk is `1/18`, since accepted marks identify the alternative exactly and only the cemetery mass overlaps. Their difference is

$$5/18=\tfrac12a_1\operatorname{TV}(Q_0,Q_1).$$

Thus the theorem's general finite-probability risk bound can be attained; replacing the full risk by the count formula would be false. The manuscript does not do that. In the same example, the displayed bit kernel gives expected simulated charge `19/12` under alternative one, rather than the actual charge `5/3`. The count kernel preserves the charge. These are exact controls on the probability algebra, **not** a claimed realization by the shrinking-window billiard pair, whose mark distance tends to zero.

The accompanying independently written script checks 8,400 rational finite marked laws, including equal, unequal, and disjoint marks. There are 31 count-threshold tie cases, 5,924 strict finite mark improvements, and 6,720 cases where the displayed bit kernel changes expected charge. The ordinary and optimized-Python outputs agree. Large-cap numerical sequences are labelled illustrations, not proofs of asymptotic convergence. No author checker is imported. These controls support the distinctions above; they do not certify an infinite-dimensional billiard theorem. [D2]

## 5. Re-examination of the principal geometric mechanism

### R55-G1. Relative normalization is a substantive analytical step

The core cannot be dismissed as the cancellation of marginal factors. The reference mixed derivative is exponentially small, of order `1/sinh(j gamma)`. An arbitrary absolute action remainder does not automatically become a vanishing relative twist error after division by that scale.

Theorem 7.2 uses the exact finite cofactor identity, subtracts the reference Hessian, and compares

$$\log b_j=\sum_i\log\{g[-\ell_{uv}(y_i,y_{i+1})]\}
-\log\det(I+G_j\Delta H_j).$$

The nonlinear Hessian perturbation is tridiagonal and localized at the two endpoint layers. Summing those localized entries gives a trace-norm estimate independent of the number of collisions. Truncating the two ends and comparing the finite Green compressions to half-line operators controls the determinant before the small reference twist is removed. The trace-series comparison retains a trace-class difference and a geometric majorant. Fixed powers of the flight length or derivative index are absorbed by a strict exponential margin, not asserted uniformly over every derivative order. [S3, Theorem 7.2 and its proof]

The resulting nonlinear actions and amplitudes live on a flight-independent collar. The common-domain integration in Theorem 7.3 is then taken at fixed positive excess time. It does not replace the nonlinear actions by their Hessians or infer relative control from weak convergence alone. This is the central analytical contribution in the material examined. I have not established a flaw in this mechanism; nor do the finite scripts prove it. [S3, Theorem 7.3]

### R55-G2. The signed jet inverse is not merely formal

Lemma 12.4 handles actual smooth graph pairs with equal finite jets. Interpolating the graphs and differentiating a finite stationary action sum cancels the interior orbit variations. The terminal term is retained until the weighted half-line estimates make it tend to zero. Integrating the finite identity before taking the infinite limit gives a bound of the form

$$|S_b^{[1]}(u)-S_b^{[0]}(u)|
\le\frac{C_M}{1-\rho^{M+1}}|u|^{M+1}.$$

Thus the finite action jet factors through the finite graph jet independently of the actual smooth representative, including flat remainders. Functional smooth bounds enter the argument; a bound on finitely many Taylor coefficients alone is not substituted for them. [S4, Lemma 12.4]

At each degree `n>=3`, the last-jet block has diagonal `coth(n gamma)` and off-diagonal entries `r_0^n csch(n gamma)` and `r_1^n csch(n gamma)`, where `r_0 r_1=1`. Its determinant is one. Subtracting the lower-order contribution gives the finite signed inverse, including odd orders. This does not yield an order-independent conditioning bound, and equality of all smooth jets is not equality of arbitrary smooth germs. The whole-image conclusion subsequently uses analyticity. Those distinctions are preserved. [S4]

### R55-G3. Interior-window recovery uses explicit visibility and topology

On a positive rectangular window containing both origins, the mixed logarithmic derivative is

$$\partial_{xy}\log p(x,y)
=-\frac{S'(x-\xi)S'(y-\eta)}{[d-S(x-\xi)-S(y-\eta)]^2}.$$

Separate positive recording factors cancel. The unique vertical and horizontal zero lines locate the origins under the stated window and single-critical-point conditions. An anchored four-density ratio then extracts `t(u)t(v)`, where `t=S/(d-S)`. A nonzero scalar anchor determines its positive normalization; inversion recovers the signed action without taking a pointwise square root at the minimum. [S5]

This genuinely avoids using an unobserved cap boundary. It does not avoid the need for visible origins, known signed physical units, positive denominators, and nondegenerate anchors. The local smooth extension is in a positive `C^(m+3)` density neighborhood with margins, not in unrestricted total variation. The finite-fiber argument checks both inclusions, and the nuisance-kernel argument concerns the stipulated analytic variation. I find no basis here for reopening the already resolved centering objection. [S5]

### R55-G4. The selected skeleton and finite symmetry argument survive a direct check

The clear-channel construction does not assume that every closest pair is unobstructed. If another obstacle meets a closest segment, the two replacement gaps have total length no greater than the original and each is smaller by a uniform positive separation. The finite descending induction yields a path in the clear-pair graph. Projecting selected paths between representatives and their two marked deck translates gives a finite connected graph whose cycle gains generate the deck group. A spanning tree and two independent gains then give the stated `N+1` architecture. This graph argument is not incorrectly interpreted as one physical billiard itinerary. [S6, Theorem 19.3]

The persistence argument uses the positive closest-contact Hessian, selected-channel clearance, and only finitely many relevant lattice translates locally. Two independent gains need not be a unimodular basis. The reconstruction correctly uses the actual fixed matrix inverse

$$L=(v_1\ v_2)M^{-1},$$

rather than silently replacing `M` by the identity. [S6–S7]

For a noncircular analytic obstacle, the proper symmetry group is finite. Enumerating incidence congruences therefore gives finitely many candidate placements. Each candidate is separately checked for positive lattice orientation, disjoint lifted obstacles, clear selected contacts, and compatible images. These geometric conditions do not follow merely from solving the cochain equations. The finite translate bound depends on the smallest singular value of the candidate lattice. This is an exact function-valued finite-branch inverse, not a decision procedure for arbitrary finite-precision data. [S7, Theorem 20.3]

### R55-G5. The differential conclusion is proved, not inferred from injectivity

The differentiability lemma explicitly includes the derivative of the moving reference inverse,

$$\dot G=-G\dot H^0G,$$

and the subtracted Hessian derivative. The nondecaying reference terms cancel before summation; the remaining terms are trace-norm summable. The moving-cap normalizer is differentiated using the positive-part integral and dominated convergence off a regular level set. No unaccounted boundary Dirac term is inserted. [S8]

The zero-law-derivative argument differentiates the amplitude-free inverse at each fixed order, obtains zero contact-jet derivatives, and then applies analyticity to the parameter derivative itself. The common-strip hypothesis is essential for that step. At a finitely symmetric noncircular base table, a nonzero harmonic supplies a local alignment branch along the actual family; the proof does not assume the finite symmetry survives a symmetry-breaking variation. The lattice cochain eliminates the remaining relative-frame variation. [S7–S8, Theorem 21.5]

Finally, the scalar-coordinate theorem selects a basis from separating gap and test-expectation derivatives on an immersed finite-dimensional model. The inverse function theorem and a uniform closeness estimate to the base Jacobian give local bi-Lipschitz coordinates. This is not a fixed finite scalar vector recovering all analytic tables. The manuscript explicitly limits the conclusion to the stipulated model. [S8, Theorem 21.6]

## 6. Why the highest-journal recommendation remains negative

### R55-E1. The new probability reductions clarify an example, not a second major inverse theorem

The new clauses are valid and useful. Once the two actual success probabilities and the two conditional mark laws are available, however, their proofs are geometric-series, likelihood-ratio, overlap, and Markov-kernel arguments for a two-point experiment. Their difficulty and reach should not be confused with the relative nonlinear billiard construction that supplies those inputs. The author now says this plainly and credits the earlier suggestions; that is a substantive improvement in exposition, not a new reason to reject the mathematics.

I nevertheless do not find that these additions change the article's case for exceptional general-journal significance. Another correct consequence of the same stopped binary experiment would not, by itself, change that judgment. This report therefore does not demand another such consequence as the price of closing the revision.

### R55-E2. The observation map is rich and specialized; finite channels do not mean finite information

The principal theorem uses complete function-valued limiting endpoint laws, marked selected channels, signed physical coordinates, separately retained gaps, and analytic continuation. It recovers a genuinely geometric object, including an unknown marked lattice, and its relative/smooth inverse deserves serious consideration. But the small number of channel labels is not a small finite collection of numerical observations. Likewise, the exact continuation argument is not an unrestricted stable inverse from noisy data. The finite-resolution results require separate quantitative assumptions. These are not hidden defects; they are central to evaluating what problem has been solved. [S1, S5–S8]

A targeted primary-source comparison confirms that the neighboring spectral-rigidity problems have different observations. Finamore and Leguil's Theorem A concerns **enriched** marked length data for finite-horizon smooth Sinai billiards; its definition uses lengths arising from closed geodesics in the auxiliary construction, and should not be replaced by ordinary periodic-orbit marked lengths. De Simoi, Kaloshin, and Leguil treat analytic open billiards with non-eclipse, symmetry, and genericity restrictions. No reduction between either observation map and the present boundary-law datum is established in this report. Their existence therefore does not prove the manuscript redundant, and the manuscript's theorem does not automatically solve their problems. The current introduction correctly distinguishes them. [L1–L2, S1]

The cancellation of separate marginal factors belongs to the established association/odds-ratio framework; the manuscript already attributes that background to Osius. It is the geometric relative limit and signed smooth inverse, rather than the association identity alone, that must carry the originality case. I have not performed an exhaustive priority survey and do not claim one. [L3, S1–S2]

My adverse recommendation is that the present combination of a specialized exact-law inverse and its many observation-specific consequences does not yet persuade me of the exceptional breadth or conceptual impact required for the requested placement. This is an evaluative judgment, not a theorem of nonpublishability and not a claim that the central analysis is elementary.

### R55-E3. Article-level integration has improved, but accumulation is not a substitute for hierarchy

The three-part organization and the common unnormalized boundary measure provide a genuine organizing principle. I do not repeat an obsolete objection that the manuscript has no proof order or no common object. The author has also distinguished the minimal law datum, cropped records, successful marks, waiting records, and the richer calibration pilot. [S1, R3]

Nevertheless, a 283-page main article plus companion asks the reader to absorb a large catalogue of distinct observation models. The inverse at exact function-valued data, the finite-dimensional expectation coordinates, the specially realized two-point nuisance experiment, and the richer-sensor finite acquisition procedure do not become one equally general theorem by sharing a forward measure. In particular, the same-flight pilot described in the introduction uses additional planar-position, timing, and outcome information; it is not calibration from the minimal transverse histograms alone. I have not freshly certified the entire pilot theory, and its title or successful build cannot substitute for that audit. [S1, D1]

Length alone is not my ground for rejection, and no arbitrary deletion of valid mathematical content is requested. The unresolved issue is the article-level case for the importance of its principal mechanism relative to the weight assigned to ancillary consequences. The current v55 expansion improves the interpretation of one such consequence; it does not resolve that editorial reservation.

## 7. Final disposition and verification

**Mandatory new mathematical corrections identified in this review: none within the stated coverage.** The newly expanded stopping theorem is technically satisfactory under its printed assumptions. The previously closed requests remain closed. This assessment must not be converted into a certificate that every inherited result has been independently verified, or into an assertion that the paper has no possible error.

**Recommendation at the requested level: do not accept on the present significance and article-level case.** I do not condition that judgment on shrinking the principal rigidity theorem, deleting valid history, solving an unrelated stronger inverse problem, or appending another elementary probability theorem. A future assessment should evaluate the substantive relative/smooth inverse and any genuinely changed article-level case, not merely count revisions or successful finite tests.

The native artifact was downloaded, all 640 frozen source files and 111 active inputs were hash-checked, and the source subtree was reconstructed. Thirty-four native evidence files were independently checked. Both complete entries were rebuilt from the downloaded source. All 283 main pages and seven companion pages agree with the native products in extracted text and same-renderer 72-dpi RGB arrays. PDF byte identity is **not** claimed. Eight specified pages were actually inspected visually; the all-page computational comparison is not described as all-page visual review. The main rebuild retains three underfull-vbox notices. These facts and the independent finite controls are recorded in the accompanying ledger and JSON files. They establish delivery reproducibility, not mathematical correctness or journal significance. [D1–D2]

## References and audit keys

All S-keys refer to the compiled source `3903f5b8a5ffb0d0a69065b1d303c247c06ebf69`, under `papers/A2-v17-boundary-information-coarsening/`. Full reading coverage and limitations are in `AUDIT_AND_REPRODUCTION.md`.

- **S1:** `main.tex`; `article/00_structural_introduction_v48.tex`.
- **S2:** `article/18g_realized_window_information_v53.tex`, complete current Section 23, especially Corollary 23.3 and Theorem 23.4, the latter on pp. 109–112.
- **S3:** `v4/10_boundary_layers.tex`, Theorems 7.2 and 7.3, beginning on pp. 19 and 21.
- **S4:** `article/23a_signed_endpoint_rigidity_v27.tex`, especially Lemma 12.4, beginning on p. 46, and the signed last-jet block.
- **S5:** `article/23q_support_and_interior_windows_v52.tex`, origin extraction, smooth extension, and exact-fiber arguments.
- **S6:** `article/23j_generic_finite_channel_rigidity_v45.tex`, especially Theorem 19.3, beginning on p. 84.
- **S7:** `article/23n_finite_symmetry_v49.tex`, especially local alignment and Theorem 20.3, beginning on p. 90.
- **S8:** `article/23m_differential_rigidity_v48.tex`, especially Theorems 21.5 and 21.6, beginning on p. 99.
- **R1:** `reviews/a2-v54-independent-harsh-top4-2026-09-15/REFEREE_REPORT.md`, at report head `1030ca91a96ca1be8ecd0347ecbdac7084cdd8d4`.
- **R2:** `reviews/a2-v54-second-referee-top4-2026-09-15/REFEREE_REPORT.md`, at report head `67250d08714acf76274e82158f107246f0de7eee`.
- **R3:** `RESPONSE_TO_REFEREE_V55.md`, in the active manuscript directory at the reviewed ready head.
- **D1:** `AUDIT_AND_REPRODUCTION.md`, `verify_delivery.py`, and `DELIVERY_VERIFICATION.json`, in this review directory.
- **D2:** `check_stopped_experiment.py` and `INDEPENDENT_CHECKS.json`, in this review directory.
- **L1:** A. Finamore and M. Leguil, *A CAT(0)-approach to the marked length spectral rigidity of Sinai billiards*, arXiv:2510.18983v1, October 21, 2025. The primary record, definition of enriched marked data, and Theorem A on printed pp. 4–5 were checked on September 15, 2026. No claim of full proof review is made.
- **L2:** J. De Simoi, V. Kaloshin, and M. Leguil, *Marked Length Spectral determination of analytic chaotic billiards with axial symmetries*, arXiv:1905.00890v4, August 17, 2022; DOI 10.1007/s00222-023-01191-8. Primary bibliographic/abstract scope checked on September 15, 2026; not a full proof review.
- **L3:** G. Osius, *Asymptotic inference for semiparametric association models*, Annals of Statistics 37 (2009), 459–489; arXiv:0903.0702; DOI 10.1214/07-AOS572. Primary record and stated association-model scope checked on September 15, 2026.
