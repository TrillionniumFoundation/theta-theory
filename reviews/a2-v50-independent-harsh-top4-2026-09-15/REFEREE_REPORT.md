# Independent referee-style report on A2, revision 50

**Manuscript:** *Boundary laws and rigidity of periodic dispersing billiards*, Qian Qi.  
**Assessment date:** September 15, 2026.  
**Requested standard:** the highest-level general mathematics journals.  
**Recommendation:** **Do not accept at that standard on the contribution demonstrated.** This is a contribution and article-level judgment, not a newly established counterexample to the main theorem.

This is an author-requested, AI-assisted referee-style assessment, not a commissioned report or decision of any journal. The mathematical arguments below were checked against frozen source and complete compiled products. Neither earlier favorable checks nor a successful build is treated as a correctness certificate.

## 1. Submission identity and scope

The reviewed delivery is `revision/a2-v50-review-ready-2026-09-15`, frozen at **`9c358bb5792f244bab7b510b36c65c50eab6302a`**. The actual compiled mathematical source is **`49f73409b0cc6cb718fbbe48598fd7f5bc9ddca4`**, under `papers/A2-v17-boundary-information-coarsening`; its historical directory name does not indicate the current revision. The main paper has **263 pages**. The complete, unchanged two-collision companion has **7 pages**. Build provenance and reproducible checks are recorded in `AUDIT_AND_REPRODUCTION.md` and `EVIDENCE.json` beside this report.

The preceding report is the v49 memorandum frozen at `5051b7789a424656a558179922607d8b55061b28`, identified as [R49] in the audit. I read its disposition and the author's response rather than treating its recommendation as binding. Revision 50 adds an attributed noncircular two-realization example and an additional-gap separator, and expands the introduction's explanation of the existing relative-law and actual-smooth inverse arguments. It does **not** supply a new proof of the relative factorization: that proof is inherited. The preservation control confirms that all 518 inherited theorem-style and proof blocks, including 243 proof environments, remain verbatim, with two propositions and two proofs added. [S01, S07, S13]

Fresh technical coverage concentrates on the relative long-bridge law, the actual-smooth signed jet inverse, the four-density inverse, the finite-congruence and differential interfaces, and both new propositions. Selected compact-experiment, quantized-continuation and physical-calibration interfaces were also inspected. The source map states where coverage is selective. I have **not** independently re-proved every statistical limit experiment, minimax assertion, global estimator or appendix theorem, nor every assertion of the companion. All-page build comparison is not all-page mathematical review.

**Principal findings.** The two new propositions survive the geometric checks, including their infinite-lattice clearance claims. The revised introduction now exposes the actual analytic obstruction instead of merely naming it. Fresh examination of the core mechanisms below establishes no new fatal defect. Nevertheless, the additional example and separator do not materially enlarge the central inverse mechanism, and the case for exceptional general-journal significance remains unpersuasive to me. These conclusions must not be merged into the misleading statement that a theorem has been disproved.

## 2. Disposition of the previous review

The revision has responded substantively to the concrete request for a noncircular multiple-realization example. Proposition 19.5 supplies it with attribution and completeness, rather than presenting two sketches without checking the periodic table. Proposition 19.6 goes beyond the suggestion by furnishing an actual clear additional channel. That request is **resolved**; I do not replace it with a demand for another illustrative example. [S07, S13, R49]

The request to foreground the analytic mechanism is also **resolved as an exposition issue**. Equations (1.2)–(1.5), page 5, exhibit the reference scale, normalized cofactor identity, actual-smooth remainder and determinant-one contact block. A reader can now see why an absolute twist estimate would be inadequate and why formal jet algebra would not suffice. Whether these mechanisms justify placement is a different question. [S01]

The finite-fiber, moving-reference and noncircular derivative arguments retain their earlier corrections. I do not reopen objections about extending a broken base symmetry, omitting the moving inverse operator, differentiating a hard histogram projection, ignoring outer cell edges, or confusing preparation trials with successful observations when the current source already addresses those points. Fresh coverage of several of these interfaces is given below. Unreviewed older results are not certified merely because their text is unchanged. [S06, S08–S10]

## 3. Technical assessment of the central inverse

### R50-C1. Relative normalization is essential, and the proof addresses it

**Locations:** Theorem 7.2 and equations (7.9)–(7.12), pages 17–19; introductory equations (1.2)–(1.3), page 5. [S01–S03]

The reference mixed derivative is

$$d_j^0=-W_{j,uv}(0,0)=q_p/\sinh(j\gamma),\qquad p=j\bmod2.$$

An absolute error of order $\vartheta^j$ becomes, after division by this reference, an error of order $(\vartheta e^\gamma)^j$. Its decay does not follow from $\vartheta<1$. The new introductory calculation is therefore relevant, not rhetorical.

The actual proof normalizes before comparing. The finite tridiagonal cofactor formula gives

$$\log b_j=\sum_{i=0}^{j-1}\log\{g[-\ell_{i\bmod2,uv}(y_i,y_{i+1})]\}-\log\det(I+G_j\Delta H_j).$$

The infinite-volume cancellation is encoded in the subtracted Hessian. Endpoint localization makes its entries absolutely summable, hence trace class; a dimension times an unweighted operator-norm estimate would not do the same job. The half-line determinant is defined by a convergent trace series with operator norm below $1/2$ on the chosen collar.

I checked the finite-to-half-line argument rather than accepting the determinant notation as a proof. The glued left and right half-line segments have residual bounded in $\ell^1$ by a polynomial in $j$ times $\rho^j$. Strict diagonal dominance gives uniform inverse bounds. Fixed-order differentiated residual equations retain the same principal inverse and introduce only fixed polynomial losses. In the determinant comparison, retaining two blocks of length $\lfloor j/3\rfloor$ gives a trace-norm tail estimate from entrywise localization. The finite Green kernel has exponentially small reflected terms on each retained block, and exponentially small coupling between the blocks. Telescoping trace powers then retains one trace-norm factor and summable operator-norm powers. These are the necessary mechanisms for a relative conclusion.

The fixed-domain sublevel integration is a separate step: it carries the relative amplitude and action limits into the physical endpoint law at a fixed positive excess. That order of limits retains the nonlinear action rather than replacing it by its quadratic jet. The conditional cap still couples the two endpoints; factorization of the amplitude is not independence of the conditional endpoints.

The independent script checks the asymmetric alternating reference and normalized cofactor identity exactly for lengths 1 through 10, and includes an absolute-only negative control. These finite matrix checks are diagnostic, not a proof of the uniform infinite-flight estimates. My positive finding about the latter rests on the argument just examined, within its local and fixed-derivative-order hypotheses.

**Finding:** no newly established relative-normalization gap. The substantive work is localization and controlled passage to the boundary law, not the cofactor identity by itself.

### R50-C2. The signed inverse is an inverse of actual smooth jets

**Locations:** Lemma 12.4, page 44; Proposition 12.6, page 46; Theorem 13.1, page 48. [S04–S05]

On a positive interior square the same-type density has the form

$$f(u,v)=Z^{-1}B(u)B(v)\{d-S(u)-S(v)\}.$$

Writing

$$R(u,v)=\frac{f(u,v)f(0,0)}{f(u,0)f(0,v)},\qquad t(u)=\frac{S(u)}{d-S(u)},$$

gives $1-R(u,v)=t(u)t(v)$. A single nonzero anchor $a$ determines the positive scalar $q=\sqrt{1-R(a,a)}$, after which $t(u)=(1-R(u,a))/q$ and $S=dt/(1+t)$. Both the unknown amplitude and the normalizing constant cancel. There is no pointwise square root through the action minimum, and no loss of the odd signed terms. Continuous interior densities make these evaluations meaningful for the exact law. This is not an assertion that pointwise densities are directly measured from a finite sample.

The less elementary issue is whether the resulting action jets determine the jets of actual graph functions, rather than just a formal model. Lemma 12.4 addresses precisely this issue. For two local graph pairs with the same gap and the same jets through order $M$, interpolate the actual local graphs. Their quadratic half-line reference is common. At fixed endpoints,

$$\partial_t\ell_t(y,z)=\frac{h_t(y,z)}{\ell_t(y,z)}\{\Delta\psi_0(y)+\Delta\psi_1(z)\}.$$

Taylor remainder bounds and weighted orbit decay make the sum bounded by a constant times $|u|^{M+1}\sum_i\rho^{(M+1)i}$. The finite stationary envelope must first retain its terminal term. That term tends to zero with the required fixed derivatives. Integrating the finite identity in the interpolation parameter before passing to the limit proves

$$|S_b^{[1]}(u)-S_b^{[0]}(u)|\le\frac{C_M}{1-\rho^{M+1}}|u|^{M+1}.$$

No globally realized interpolation of periodic tables is needed for this local statement. The constants require functional smooth bounds; bounds on finitely many jet values alone are insufficient. The lemma states this restriction. Flat smooth differences imply equality of all finite action jets, not equality of arbitrary smooth germs. Analyticity enters later, when a germ determines an entire obstacle image.

Only after this filtration is established is it legitimate to use the last-jet matrix

$$M_n=\begin{pmatrix}\coth(n\gamma)&r_0^n\operatorname{csch}(n\gamma)\\r_1^n\operatorname{csch}(n\gamma)&\coth(n\gamma)\end{pmatrix},\qquad r_0r_1=1.$$

A boundary occurrence is counted once and each interior occurrence twice. The geometric sums give $\det M_n=1$. The proof's degree bookkeeping prevents an orbit derivative from silently importing a higher graph jet into the degree being recovered. My script checks the determinant and the boundary multiplicity for orders 3 through 12, with a deliberately incorrect multiplicity as a negative control.

**Finding:** the actual-smooth remainder is a genuine prerequisite and is present. A criticism that the paper merely inverts a formal series would not accurately describe this source. No order-uniform or whole-class noisy inverse follows from these finite-order calculations, and none is being credited here.

### R50-C3. Finite global ambiguity and local differential injectivity are compatible

**Locations:** Theorem 19.3, page 80; Section 20, including Theorems 20.5–20.6. [S06, S08]

For a centered noncircular support function, at least one harmonic of order $k\ge2$ is nonzero. Proper symmetries must annihilate the phases of all such harmonics; their order is the gcd of these indices. A finite subset already realizes that gcd. Thus congruences between two recovered copies form a finite set, not a preferred global phase.

The reconstruction propagates rotations on a tree of incident channels, checks all other occurrences, and only then solves the center cochain. The formula $L=(v_1\ v_2)M^{-1}$ uses the actual invertible integer gain matrix, not an assumed unimodular one. Geometric acceptance tests remain necessary. Every realization produces an assignment, and every accepted assignment places the full ordered channel pairs correctly. The conditional law is preserved because its global phase-volume constant cancels. This establishes the two required directions; finite enumeration by itself would establish neither.

For derivatives, the actual continuous congruence family chooses a local logarithmic branch through the base alignment. It is not necessary that every symmetry at the base extend after symmetry breaking. A nonzero harmonic controls the local angular derivative. The moving-reference derivative also correctly retains

$$\dot G=-G\dot H^0G,\qquad \dot T=\dot G\Delta H+G\dot{\Delta H}.$$

The reference subtraction precedes the trace-class assertion. The derivative of the cap normalizer is included; the first derivative of its positive part is justified away from a measure-zero regular level. Interior density differentiability is not extended without argument across the moving cap boundary. The independent noncommuting finite-matrix control detects a nonzero error when the $\dot G$ term is deliberately omitted.

The differentiated four-density inverse retains its scalar-anchor correction. The contact recursion retains derivatives of both its lower-order term and its coefficient matrix. Analyticity of the variation follows from the common-strip $C^1$ family hypothesis, not merely analyticity of each slice. These facts, followed by registration and the lattice cochain, supply a derivative-kernel proof; nonlinear injectivity alone would not supply one.

Finally, finite-dimensional duality selects actual gap or smooth interior expectation observables. The lower Lipschitz estimate is obtained on a sufficiently small convex parameter ball by comparison with the fixed invertible derivative at the base. It is not inferred just from pointwise nonsingularity.

**Finding:** no new defect in these checked interfaces. The local scalar coordinate theorem remains model- and base-dependent; it is not a global finite-dimensional encoding of the analytic class.

## 4. The genuinely new propositions

### R50-C4. Proposition 19.5 has exactly the announced two realizations

**Location:** pages 82–83; S07, lines 12–123.

Let $a=2^{-1/2}$, $R=101/1000$, and

$$h(\theta)=1/10+\cos(4\theta)/1000,\qquad L_\pm=\begin{pmatrix}1&\pm a\\0&a\end{pmatrix}.$$

The support has curvature radius at least $17/200$, center zero and proper symmetry group exactly $C_4$. Since $K$ lies in the radius-$R$ disk and the least eigenvalue of either marked Gram matrix is $1-a$, every nonzero lattice mark has center displacement at least $\sqrt{1-a}>2R$. This establishes separation of the entire periodic configuration, not a finite plotted patch.

For the selected unit center segments, $h'$ vanishes at the contact normals. The gaps are therefore $399/500$ and $401/500$. Every third center off a selected line has perpendicular distance at least $a$; every nonincident center on it is at least one from the segment. Consequently the third obstacles remain at distance at least $a-R>3/5$. The selected physical channels and common small collars exist.

Rotation by $\pi/2$ identifies the second ordered pair in the two tables and preserves the signed convention. The first ordered pair is identical. Thus both same-type conditional laws agree. The argument does not assert equality of successful-preparation frequencies.

Completeness uses the previously established inverse. In the root gauge, the second displacement can only be $(a,a),(-a,a),(-a,-a),(a,-a)$. Their determinants are $a,a,-a,-a$. The first two have already passed separation and clearance; the latter two are excluded by $GL^+(2,\mathbb R)$. The identity gain matrix leaves no placement freedom. The surviving marked Gram forms differ, and changing the integer basis is not permitted for this marked datum.

**Finding:** the two-element fiber is established in the announced class. It illustrates nonsharpness of the general product bound, not a contradiction to that bound or to the derivative theorem. Its origin in [R49] is properly acknowledged.

### R50-C5. Proposition 19.6 checks the actual segment, not an invalid radial surrogate

**Location:** page 83; S07, lines 128–177.

For the additional mark $(1,1)$ the center lengths are $\ell_\pm=\sqrt{2\pm\sqrt2}$. The radius bounds give $\ell_\pm-2R\le g_\pm\le\ell_\pm+2R$, hence $g_+>1>g_-$. To make these distances valid clear channels, the proof also checks every third lattice obstacle.

For arbitrary integer $(m,n)$,

$$\det(L_\pm(1,1),L_\pm(m,n))=a(n-m).$$

The off-line distance is therefore at least $a/\ell_\pm$; the on-line nonincident distance is at least $\ell_\pm$. The common center-segment bound $c_*=a/\ell_+$ exceeds $2R$. Every segment between points of the two bodies is within the radius-$R$ tube of their center segment, so every third obstacle is at least $c_*-2R>0$ from the actual closest segment.

This last distinction matters. At the new center directions $\pi/8$ and $3\pi/8$, one has respectively $h'=-1/250$ and $h'=1/250$. The radial shortcut used legitimately for the original two channels is not available here. The submitted tube proof does not use that shortcut and survives this check.

A further deterministic consequence, derived here only as a control, is useful for interpreting the example. Set

$$t_*=(\ell_++\ell_-)/2,\qquad \epsilon_*=(\ell_+-\ell_--4R)/2>0.$$

Then $g_+\ge t_*+\epsilon_*$ and $g_-\le t_*-\epsilon_*$. Thus an additional-gap measurement with absolute error strictly below $\epsilon_*\approx0.3391961$ distinguishes the two members by threshold $t_*\approx1.306563$. The actual-segment clearance bound is approximately $0.1806834$. This is a control on the **original exact two-point fiber**, not a theorem about perturbations of the original laws, universal branch selection, or sample complexity. Its absence from the manuscript is not a defect or a new revision requirement.

**Finding:** the separator is correct in its example-specific scope. It is a useful addition, but not an additional general inverse mechanism.

## 5. Statistical and observational boundaries

The exact theorem observes finitely many channels but function-valued laws. It also supplies the selected design, deck marks, signs, known offsets and gaps. Recovering unknown channel registration and the marked lattice from this record is nontrivial; nevertheless this is not recovery from $N+1$ scalar measurements or from an unmarked collision record. The current theorem does not claim those stronger interpretations. [S01, S05–S06]

The quantized theorem imposes analytic, density, geometric and harmonic-registration margins beyond the noncircular exact theorem. I inspected the stated conditions and the finite-jet/analytic-continuation interface; the prescribed order of choosing the jet order and then the accuracy is important. The hard-category calibration argument separately controls inner and outer cell edges by displacement tubes, retains the amplified gap error at the chosen final flight length, and conditions on a richer planar-position pilot. Its successful-observation and preparation budgets must remain distinct. These qualifications survive in the current source. They cannot be silently removed by invoking exact injectivity. [S09–S10]

I also checked the compact finite-net upgrade: a single kernel chosen for a finite net can be extended by total-variation contraction and the stated uniform modulus. That step does not by itself prove the upstream finite-experiment convergence or any arbitrary noncompact uniformity. My assessment here is limited to the upgrade and its hypotheses. [S11]

The signed one-flight benchmark is an important internal comparison. With its different, mixed-endpoint support record varying over time, the one-flight length function directly recovers the facing graphs. It shows why the long-flight restriction matters to the present observation problem. It is not a reduction of the fixed-offset same-type density experiment to that benchmark, nor a counterexample to the boundary-law theorem. The manuscript explicitly distinguishes these records. [S12]

## 6. Primary literature and the highest-journal judgment

The targeted primary-source check was repeated on September 15, 2026. Finamore–Leguil's current arXiv record is v1 and concerns finite-horizon Sinai billiards, an enriched marked length spectrum and an isometry conclusion [L1]. De Simoi–Kaloshin–Leguil's v4 concerns analytic open billiards under non-eclipse, symmetry and genericity assumptions [L2]. Florio–Leguil's v5 explicitly records removal of an earlier geometric spectral-rigidity assertion affected by an error, while retaining dynamical conjugacy results [L3]. The present manuscript does not use that removed assertion as a premise.

These are different observations and theorem classes. I have not proved an information reduction in either direction and have not conducted an exhaustive priority search. It would be unjustified either to call the present signed-law inverse already proved by these papers or to advertise it as automatically removing their assumptions. The revision's observation-specific comparison is appropriately qualified.

**R50-E1 — Contribution.** The most substantial achievement remains the chain from relative long-bridge boundary laws through an amplitude-free signed inverse to actual contact jets. Analytic continuation, finite congruence enumeration, the lattice cochain and local scalar selection turn that local inverse into an attractive structural result. The first part cannot fairly be dismissed as elementary algebra. Conversely, the last steps do not each constitute a separate major conceptual advance merely because they enlarge the list of consequences.

The revised exposition makes the best existing case for the paper substantially easier to evaluate. I nevertheless remain unconvinced that the demonstrated advance has the exceptional breadth or conceptual force needed for the requested general-journal placement. Its exact reconstruction uses a deliberately selected, contact-centered, function-valued observation carrying fine local information; the broader acquisition claims retain separate sensor and conditioning assumptions. This is an assessment of the mathematical return under that observation, not an objection that such an observation is illegitimate. The paper convincingly explains retention of nonlinear geometry in the prescribed long-flight regime. In my assessment it does not make an equally convincing case that this achievement and its consequences warrant the highest-level general-journal treatment sought here.

**R50-E2 — Article-level synthesis.** The 263-page submission combines exact rigidity, several local statistical experiments, finite-resolution continuation and physical calibration. The dependency reorganization is a real improvement. Still, collecting these results into one source-matched corpus does not itself establish that their joint conceptual contribution exceeds that of the central inverse. The new two-branch example clarifies the theorem sharply but does not resolve that editorial issue. No universal page limit is being imposed, and I am not requesting deletion of valid proofs or reduction of the theorem's scope.

These are expressly judgment calls. An editor or another specialist may assess the contribution differently. I do not present them as formal obstructions, guaranteed journal outcomes, or a mandate to prove some unspecified stronger theorem. In particular, it would be a moving target to demand a routine new consequence after each successful response to a concrete request.

## 7. Reproduction, preservation and final disposition

The complete native artifact was downloaded through the authorized GitHub connection. All 567 source files were checked for size, SHA-256 and Git blob identity. Reconstructing the Git directory objects from them yields the advertised source subtree `aef336df33a8754390f74e02f1fd855045095661`, independently matched to the repository's pinned source directory. All 107 active source records match. Both complete entries were rebuilt with shell escape disabled, companion first. [D1]

All 270 rebuilt pages match their native counterparts in extracted text and in 72-dpi RGB pixel arrays under the same PyMuPDF renderer. Rebuilt PDF byte hashes differ; byte-identical PDF reproduction is **not** claimed. Direct visual inspection covered main pages 5, 18, 44, 46, 82 and 83, and companion pages 1 and 7. The main log has three underfull boxes and no overfull box or unresolved-reference/citation warning. Both logs contain the expected disabled-shell-escape warning. [D1]

The author's v50 preservation/control suite and the independent finite controls both pass in ordinary Python and under `python -O`, with identical output within each pair. The independent tests cover finite reference twists and cofactors, contact multiplicities, moving-reference differentiation, amplitude cancellation with odd signed action terms, and the new lattice geometry. Their explicit negative controls detect the deliberately invalid shortcuts. None certifies an infinite-dimensional estimate or an unreviewed theorem. [D1]

**Final disposition:** the concrete v49 exposition/example requests are resolved, the v50 additions survive the fresh technical checks, and complete source-matched delivery is independently reproduced. I report **no newly established fatal theorem error in this coverage**. I nevertheless **do not recommend acceptance at the requested highest-level general mathematics journal standard**, for the contribution and synthesis reasons in Section 6. This is not a recommendation to weaken the valid statements, repeatedly append illustrative material, or manufacture an algebraic patch for an editorial disagreement. No manuscript source is modified by this review.
