# Independent referee report on A2, revision 54

**Manuscript:** *Boundary laws and rigidity of periodic dispersing billiards*  
**Author:** Qian Qi  
**Date:** September 15, 2026  
**Requested standard:** the highest general mathematics journals. This is an author-requested, AI-assisted external-referee-style assessment, not a commissioned journal report or an editorial decision.

## 1. Recommendation, reviewed object, and limits of the assessment

**Recommendation: do not accept at the requested highest general-journal level on the present contribution and article-level case.** This recommendation must be separated from the mathematical disposition: **I identify no mandatory correction to the strengthened Corollary 23.3 or the new Theorem 23.4, and no newly established fatal error in the inherited mechanisms inspected here.** The two technical improvements proposed in the v53 report have been implemented with appropriate attribution. The new deterministic-cap theorem withstands scrutiny, including its necessity assertion. Previously closed technical requests remain closed.

The reviewed delivery is `revision/a2-v54-review-ready-2026-09-15`, frozen at `802cb27e731a3a821903a7308cba9d5da29bbf79`. The actual compiled mathematical source is `2cedae961195f97df802aaa81112d95cd32974e1`, with manuscript subtree `407b278984b14e57468e727fb56b0fa4163a7207`. The historical directory `papers/A2-v17-boundary-information-coarsening` contains the active v54 manuscript. The main article has 281 pages and its companion seven. These source and delivery identities are not interchangeable. [D1]

This review examines the complete current Section 23, its preceding realization and likelihood calculation, the v54 response, and the core inherited proof interfaces identified in the accompanying audit ledger. Fresh scrutiny includes the relative half-line/determinant construction, actual-smooth finite-jet inverse, interior-window extraction, selected-channel skeleton, finite-symmetry reconstruction, and differential-kernel argument. It does **not** constitute a fresh line-by-line certification of every older statistical theorem, every full-phase event construction, or the companion. Rebuilding the complete corpus has broader coverage than this mathematical audit; a successful build is not a proof certificate.

Section 5 below supplies additional reviewer-derived reductions of the stopped experiment. They clarify the mathematical content of the new theorem. They are neither counterexamples nor additional conditions imposed as the price of closing this revision.

## 2. Disposition of the preceding report

The preceding report is frozen at `000ce24f65f8381d2180cbd1f080d3d8470c8157` and concerns v53 source `42cc62f230473c34d78af1d06b9ca5c2651ae86d`. It explicitly identified no mandatory correction to that revision's three new statements. Its Hellinger and waiting-count arguments were nonfatal improvements, not findings that the previous claims were false. The present response accurately distinguishes that technical status from the negative placement assessment. [R1, R2]

| Item from v53 | Assessment in v54 |
|---|---|
| R53-Q1: quadratic one-record Hellinger comparison and square-root product bound | Implemented correctly in Corollary 23.3. Closed. |
| R53-Q1: direct finite-flight mean test without approximating a growing product experiment | Implemented separately, with the required mean margin and rate condition. Closed. |
| R53-Q2: retain the first waiting count for the same actual table/profile pair | Implemented, including exact stopping factorization and both deficiency directions. Closed. |
| Expected charge is not a deterministic cap | The new theorem defines the capped experiment and proves its optimal limiting risk and necessary-and-sufficient consistency condition. No defect identified. |
| Actual noncircular realization and fixed profiles | Retained. The actions are not falsely replaced by exact quadratics. |
| Earlier centering, signed units, finite fibers, local smooth versus statistical topology, and attribution distinctions | Retained in the inspected source. Not reopened. |
| Exceptional general-journal significance | An editorial assessment, not a technical checklist that another appended theorem automatically resolves. |

The revision strengthens an existing corollary and adds one theorem in the same section. It does not append another independent introduction or require a new geometric hypothesis for Theorems A and B. The author checker confirms 107 inherited active inputs unchanged in place, four archived originals, and 542 of 544 inherited statement/proof blocks verbatim; the two replaced blocks are precisely the strengthened corollary and its proof. These are provenance facts, not measures of mathematical importance. [R2, D1]

## 3. Corollary 23.3: the improved finite-flight comparison is justified

### R54-M1. The area cancellation is essential and is actually present

The argument starts from a uniform density estimate on one fixed physical interior square, before the recording window shrinks. Let `f_{s,J}` and `f_s` be the finite and limiting successful endpoint densities and let `w_s` be the product of the two fixed recording probabilities. The source supplies

$$\|f_{s,J}-f_s\|_\infty\le C\tau^J,$$

with positive upper and lower bounds on the fixed collar. The relevant normalizers satisfy

$$A_{s,J}(h)=\int_{(-h,h)^2}w_sf_{s,J}\asymp h^2,
\qquad |A_{s,J}(h)-A_{s,\infty}(h)|\le Ch^2\tau^J.$$

In the rescaled quotient

$$q_{s,J,h}(z,w)=\frac{h^2w_s(hz,hw)f_{s,J}(hz,hw)}{A_{s,J}(h)},$$

the two area factors cancel. Thus the claimed supremum-norm error is `C tau^J`, not `C tau^J/h^2`. This is stronger input than pointwise weak convergence for each fixed window. The proof uses that input and does not interchange the shrinking-window and long-flight limits without control. [S2, lines 320–346; S3]

After decreasing the fixed collar and increasing the minimum flight, both rescaled densities have a common lower bound `m>0`. With the manuscript's convention `H^2(P,Q)=integral(sqrt(p)-sqrt(q))^2`,

$$H^2(P,Q)=\int\frac{(p-q)^2}{(\sqrt p+\sqrt q)^2}
\le\frac1{4m}\int(p-q)^2
\le m^{-1}\|p-q\|_\infty^2,$$

because the rescaled square has area four. Hence the one-record bound is `C tau^(2J)`. Affinity tensorization gives a product squared Hellinger bound `C n tau^(2J)`, and `TV <= H` yields

$$\operatorname{TV}\left(\bigotimes_{k=1}^nQ_{s,J,h}^{(k)},
                         \bigotimes_{k=1}^nQ_{s,h}^{(k)}\right)
\le\min\{1,C\sqrt n\,\tau^J\}.$$

The fixed allocation among the four labels causes no problem. Uniform bounds on expectations of tests pass to the infimum defining the optimal equal-prior risk. Therefore `n tau^(2J) -> 0` suffices to transfer the whole binary testing experiment. The former stronger sufficient condition remains a valid consequence. [S2, lines 346–368]

### R54-M2. The direct test and full-experiment comparison are not conflated

For the bounded statistic `F(z,w)=1/9-z^2w^2`, the ideal means differ by

$$D_h=c_0h^4+O(h^6)>0.$$

Each finite-flight mean differs from the corresponding ideal mean by `O(tau^J)`. Under `tau^J=o(h^4)`, the ideal midpoint remains on the correct side of each finite-flight mean at distance at least `D_h/4`. Since the range length of `F` is one, the bounded-variable exponential inequality gives

$$\text{error}\le\exp(-nD_h^2/8)\le\exp(-c'nh^8).$$

This conclusion applies directly under the finite-flight laws. It does not need a small total-variation distance between the entire growing products. This distinction matters particularly when `nh^8` diverges. The manuscript states it correctly rather than deleting the product-approximation error without justification. Its logarithmic even-flight choice with coefficient `(4+epsilon)/|log tau|` is sufficient for the required mean condition; no optimal geometric convergence exponent is established or claimed. [S2, lines 369–405]

The normalization and information constants inherited from v53 also check out. Writing `a_i=S_i''(0)` and `Delta=a_1^2-a_0^2`, the expansion is

$$q_{i,h}=\frac14+\frac{a_i^2}{16d^2}h^4F+O(h^6),
\qquad \int F^2=\frac{224}{2025},$$

and therefore

$$H^2(Q_{0,h},Q_{1,h})=
\frac{7\Delta^2}{16200d^4}h^8+O(h^{10}).$$

Even `C^4` actions suffice for the displayed remainders. Higher nonlinear terms enter the density remainder; they need not vanish. The likelihood coefficient is four times the leading squared Hellinger coefficient under this convention. The exact rational checks in the independent script agree. The critical Gaussian likelihood limit and bounded-mean attainment concern this specified two-point experiment, not a uniform estimator over arbitrary recording profiles. [S2, lines 18–263; D2]

**Disposition of R54-M1–M2:** no mandatory correction identified. Both parts of R53-Q1 are closed.

## 4. Theorem 23.4: actual rarity, stopping, and deterministic caps

### R54-M3. These are actual table probabilities, not freely chosen geometric parameters

The noncircular support family is

$$k_s(\theta)=R+s(\cos4\theta-1),\quad R=1/10,
\quad s\in[R/128,R/64].$$

Its radius of curvature is `R-s-15s cos(4theta) >= 3R/4`. Each obstacle lies in the radius-`R` disk, and the selected axis pairs have the common gap `g=4/5` and positive all-lattice third-obstacle clearance. The perimeter varies with `s`, so the two endpoints are not merely different descriptions of congruent tables. Reflections and quarter-turn symmetry legitimately make the selected actual half-line actions even and identical across the relevant labels. No finite-horizon assertion is needed for these selected channels. [S2, lines 95–181]

The recording choice

$$e_s(u)=\frac{c_*}{B_s(u)(d-S_s(u))}$$

is made on one fixed collar, with a common sufficiently small `c_*` and a positive smooth extension bounded by one. It is fixed as `h` shrinks. It may differ between the specified alternatives. That is legitimate for this existential two-point nuisance construction; it is not a table-independent sensor computable without knowing an unknown geometry. The source preserves this restriction. [S2, lines 182–202]

At the two endpoints, `kappa_0=80/7` and `kappa_1=40/3`. Thus

$$\gamma_0=\operatorname{arcosh}(71/7),\qquad
\gamma_1=\operatorname{arcosh}(35/3)>\gamma_0.$$

The relative physical law supplies `pi_{i,J} asymp exp(-gamma_i J)`, and the crop fraction is uniformly comparable to `h^2`. Consequently

$$p_{i,h}\asymp h^2e^{-\gamma_iJ_h},\qquad
\rho_h=p_{1,h}/p_{0,h}\longrightarrow0.$$

The common gap does not force the two hyperbolic exponents to coincide. Conversely, the inference above genuinely depends on the forward physical prefactor and uniform crop estimate; it cannot be deduced from the normalized mark law alone. [S2, lines 382–388 and 416–595; S3]

### R54-M4. The full and coarsened records belong to the same acquisition

For independent preparations, first acceptance gives the exact identity

$$\Pr_i(W=k,Y\in A)=(1-p_i)^{k-1}p_iQ_i(A).$$

Thus the waiting count and terminal mark are independent within each alternative, and deleting `W` gives exactly the finite-flight accepted mark. The comparison is not between unrelated acquisition policies. Failed preparations retain only their acceptance/failure symbols; richer failed-shot measurements are excluded by the experiment's definition. [S2, lines 406–595]

The accepted marks obey `TV(Q_0,Q_1) <= C(h^4+tau^J) -> 0`. In contrast, with

$$m_h=\lceil(p_0p_1)^{-1/2}\rceil,$$

the count threshold has errors at most `exp(-rho_h^(-1/2))` and `sqrt(rho_h)+p_1`. They both vanish without a relation between `h` and `tau^J` beyond their separate convergence to zero.

The deficiency argument has both required directions. Projection gives `delta(F,E)=0`. Contraction and the triangle inequality give

$$\delta(E,F)\ge
\tfrac12\{\operatorname{TV}(F_0,F_1)-\operatorname{TV}(E_0,E_1)\}.$$

The right side tends to one half. A kernel ignoring its input and returning the equal mixture of the two full laws gives the matching upper bound. Dependence of that kernel on the two specified hypotheses is allowed; dependence on the unknown generating alternative is not. The stated kernel respects this distinction. [S2, equations (23.18)–(23.24)]

### R54-M5. The cap theorem proves optimality, not just a convenient upper bound

Let `a_i=1-(1-p_i)^b`. For sufficiently small `h`, `p_1<p_0`, so `a_1<=a_0`. The capped full laws share a cemetery atom of mass at least `1-a_0`. Testing the occurrence of any acceptance and bounding by that common atom give

$$a_0-a_1\le\operatorname{TV}(F_0^{[b]},F_1^{[b]})\le a_0.$$

These inequalities hold for arbitrary terminal mark laws. In particular they do not assume that the marks are exactly identical. If `bp_0 -> lambda < infinity`, then `bp_1=rho bp_0 -> 0`, `a_0 -> 1-exp(-lambda)`, and `a_1 -> 0`. The two bounds squeeze the optimal equal-prior error to

$$R_h^*(b_h)\longrightarrow\tfrac12e^{-\lambda}.$$

This establishes the lower bound for the full capped record, not merely the performance of the acceptance-event test. That event test attains the limit. [S2, equation (23.25) and following proof]

For unrestricted cap sequences with `bp_0 -> infinity`, the observable threshold `min(b,m_h)` has `p_0 min(b,m_h) -> infinity` and `p_1 min(b,m_h) -> 0`. It is measurable even when the observed outcome is the cemetery symbol. This proves sufficiency. If `bp_0` does not diverge, a bounded subsequence has a further subsequence converging to a finite `lambda`, on which the optimal risk has a positive limit. This proves necessity.

The manuscript does **not** incorrectly use the any-acceptance bit for every supercritical cap. At extremely large caps with `bp_1 -> infinity`, that bit becomes uninformative; the truncated waiting threshold still works. The independent negative control illustrates this distinction. Finally,

$$\mathbb E_i\min(W,b)=\sum_{k=0}^{b-1}(1-p_i)^k
=\frac{1-(1-p_i)^b}{p_i}$$

charges every failed preparation before stopping. The critical deterministic-cap order `p_0^(-1) asymp h^(-2)exp(gamma_0 J)` follows from the risk criterion, not from turning an expected waiting time into a deterministic bound. It is specific to this stopped binary experiment. [S2, lines 548–595; D2]

**Disposition of R54-M3–M5:** R53-Q2 is closed. The new cap extension requires no mandatory correction identified here.

## 5. Independent reductions: what the stopped theorem adds, and what it does not

The following consequences are useful for assessing the new theorem's mathematical reach. They are reviewer derivations from its specified experiment, not attributed manuscript statements or new revision requirements.

### R54-Q1. For any deterministic cap, the terminal mark is asymptotically dispensable

Let `C_h^[b]` retain only the waiting count when acceptance occurs by `b`, and the cemetery symbol otherwise. Let `F_h^[b]` be the manuscript's full capped record. Write `eta_h=TV(Q_{0,h},Q_{1,h})`.

Deleting the mark gives `delta(F^[b],C^[b])=0` exactly. In the opposite direction, use a single parameter-independent kernel which preserves the count and, on acceptance, appends an independent mark drawn from `Q_{0,h}`. Under alternative zero the simulated full law is exact. Under alternative one its total-variation error is exactly `a_{1,h} eta_h`: each accepted-count component has the same conditional mark discrepancy, and the cemetery component has none. Hence

$$\delta(C_h^{[b]},F_h^{[b]})\le a_{1,h}\eta_h\le\eta_h\longrightarrow0,$$

**uniformly over all deterministic cap choices**. The same construction works without a cap, with upper bound `eta_h`. It also gives the equal-prior risk comparison

$$0\le R_C^*(b)-R_F^*(b)\le\tfrac12a_{1,h}\eta_h.$$

This is a Le Cam comparison of the stated two-point experiments. It neither supplies an unrestricted unknown-profile kernel nor gives a relative-error approximation when the optimal risks themselves are very small. In particular, the bound must not be converted without further estimates into an exact asymptotic ratio of vanishing risks.

The conclusion is informative: the stopped experiment's asymptotic discrimination is already present in the waiting count. The terminal action-sensitive mark, which was essential to the conditional-window discussion, adds asymptotically negligible information in this binary comparison.

### R54-Q2. At finite cap intensity, even one acceptance bit suffices asymptotically

When `bp_0 -> lambda < infinity`, let `B=1{W<=b}`. To simulate the full capped record from this bit, send `B=0` to the cemetery symbol and, on `B=1`, draw the full record conditional on acceptance under alternative zero. Again the simulation is exact under zero. Its error under one is at most `a_1 -> 0`, regardless of the difference between the accepted mark laws.

Thus the full capped experiment is asymptotically equivalent to the binary experiment whose success probabilities tend to `1-exp(-lambda)` under zero and zero under one. The limiting risk `exp(-lambda)/2` is the corresponding elementary binary risk. The geometric work is in realizing the acceptance probabilities and identifying their exponents, not in this final common-atom calculation. This observation confirms, rather than contradicts, the manuscript's cap formula.

The finite-intensity restriction is important. The bit reduction need not be informative at arbitrarily large caps. In the independent finite diagnostic with `p_0=10^(-3)`, `p_1=10^(-6)`, and `b=10^9`, the any-acceptance bit has risk approximately `1/2`, while the optimal count risk is approximately `0.00394025`. These parameters are a finite distribution check, not an additional billiard realization. [D2]

### R54-Q3. The count-only capped Bayes risk has an exact finite formula

For `0<p_1<p_0<1`, the accepted-count likelihood ratio

$$\frac{p_0}{p_1}\left(\frac{1-p_0}{1-p_1}\right)^{k-1}$$

strictly decreases with `k`; the cemetery likelihood ratio is less than one. Define `K` to be the largest integer `k<=b` for which the displayed ratio is at least one. Equivalently, with either convention at a tie,

$$K=\min\left\{b,\left\lfloor
1+\frac{\log(p_0/p_1)}{\log((1-p_1)/(1-p_0))}
\right\rfloor\right\}.$$

The likelihood-ratio test chooses zero for accepted counts up to `K`, and one otherwise. Therefore

$$R_C^*(b)=\tfrac12\{(1-p_0)^K+1-(1-p_1)^K\}.$$

This formula and R54-Q1 provide a direct finite comparison with the full capped law. Exact rational enumeration checks the formula, common-atom bounds, simulation-kernel error, and charge identity in the independent script. The formula is not a claim to solve a general optimal physical acquisition problem: the flight design and the two alternative profiles have already been stipulated.

**Disposition of R54-Q1–Q3:** additional analysis supporting the evaluation, not requested additions to the article. Appending these observations would not by itself resolve the placement reservation below.

## 6. Fresh scrutiny of the inherited mechanism

### R54-M6. The relative nonlinear law remains the central analytical contribution

The reference twist has size `q_p/sinh(j gamma)`. An absolute action estimate alone does not control its normalization. The inspected proof instead uses the exact cofactor/log-determinant identity, summable tridiagonal perturbations of the half-line reference Hessian, and a trace-norm comparison of two separated endpoint blocks. The glued stationary orbit has an exponentially small residual; diagonal dominance controls its correction. The trace-power telescoping retains a trace-norm factor and a geometric operator-norm factor rather than paying for the total number of collision sites. Fixed differentiated orders use strict exponential margins. This supports a nonlinear fixed-positive-offset law rather than only a quadratic curvature approximation. [S3]

These are serious analytical steps. Dismissing the whole paper as elementary odds-ratio manipulation would misidentify its hardest argument. I found no new relative-normalization gap in this inspected module. That finding is bounded by the stated proof coverage and does not newly certify every earlier physical event construction used by it.

### R54-M7. The action inverse is an actual-smooth finite-jet argument

The source retains a finite stationary envelope identity, including its terminal term, before taking the half-line limit. Interpolating two graph pairs with the same `M`-jet and using the exponential orbit bound gives

$$|S_b^{[1]}(u)-S_b^{[0]}(u)|
\le\frac{C_M}{1-\rho^{M+1}}|u|^{M+1}.$$

Only after this actual-remainder estimate does the proof use the last-jet block

$$M_n=\begin{pmatrix}
\coth(n\gamma)&r_0^n\operatorname{csch}(n\gamma)\\
r_1^n\operatorname{csch}(n\gamma)&\coth(n\gamma)
\end{pmatrix},\qquad r_0r_1=1,\qquad\det M_n=1.$$

Boundary visits count once and interior visits twice. Nonlinear orbit corrections contribute at higher endpoint degree. The inverse is triangular at each fixed finite order; determinant one does not imply order-uniform conditioning. Equality of entire boundary images later uses analyticity, not equality of arbitrary smooth germs with the same Taylor series. The signed odd jets remain present. [S4]

### R54-M8. Window, matching, and differential interfaces preserve their hypotheses

For an interior recorded window, the zero fibers of

$$\partial_x\partial_y\log p
=-\frac{S'(x-\xi)S'(y-\eta)}
{[d-S(x-\xi)-S(y-\eta)]^2}$$

identify the origins only because both critical lines remain visible. A nonzero scalar anchor fixes the action scale. The local inverse is in finite smooth norms, with root extraction, translated restrictions, and positive denominators; it is not an inverse from total variation to derivatives. Both inclusions of the geometric fiber are supplied, and the joint nuisance/table derivative statement concerns the projected table kernel, not identification of all nuisance profiles. [S5]

The selected skeleton follows from obstruction descent and two independent deck cycles. Its `N+1` count is for that connected two-cycle architecture. Finite-symmetry matching enumerates proper incidence congruences, propagates rotations, and uses the actual gain-matrix inverse in `L=(v_1 v_2)M^(-1)`. The matrix need not be unimodular. Retained candidates still undergo shape, separation, determinant, and channel-clearance tests. The converse direction verifies that a compatible candidate produces the same normalized laws; phase-volume normalization cancels. This is an exact function-valued reconstruction, not a finite-precision decision procedure. [S6, S7]

The differential proof does not infer immersion from injectivity. It differentiates the moving reference through `dot G=-G dot H^0 G`, controls trace-class derivatives, and justifies the moving-cap normalizer by dominated convergence away from a measure-zero regular level. The variation itself is analytic because of the common-strip family hypothesis. Finite-symmetry registration follows the actual local angular branch, including possible symmetry breaking. Finally, finite-dimensionality enters only when selecting finitely many scalar test derivatives; the local lower Lipschitz estimate compares the derivative with one fixed invertible matrix on a convex ball. [S8]

**Disposition of R54-M6–M8:** no new fatal defect established in the inspected chain. No broader certificate for all inherited experiments is claimed.

## 7. Literature, significance, and article-level judgment

### R54-E1. Judge the strongest theorem, but also the actual observations supplied

The combination of a relative physical boundary law with an actual-smooth signed inverse is the strongest contribution. The unknown lattice, finite global symmetry alternatives, and common-strip differential result are meaningful consequences. They deserve evaluation as a coherent inverse-dynamical theorem, not as an accumulation of isolated statistical exercises. [S1, S3–S8]

Nevertheless the theorem is supplied selected obstacle/channel/deck marks, physical signed transverse conventions, gaps, known offsets, and exact local function-valued probability laws. The window extension additionally requires visibility of the critical lines. The design is not learned from an unmarked trajectory. The finite-coordinate result is model-local and does not turn the full analytic-class datum into a universal finite observation vector. These are legitimate hypotheses, but they matter substantially when assessing the informational and conceptual reach of the theorem. The manuscript now states these distinctions explicitly; the objection is not a missing disclaimer.

My judgment is that this is a substantial specialized contribution whose demonstrated reach does not yet make a sufficiently compelling case for exceptional placement in the requested general-journal tier. I do not claim that a rich datum makes a rigidity theorem trivial, that the result is known, or that another editor could not weigh its significance differently. The recommendation is a judgment of the contribution established under these observations, not a proof of impossibility of further progress.

### R54-E2. The stopped-window extension completes an interpretation, not a second geometric breakthrough

Revision 54 is technically successful. It sharpens a sufficient finite-flight rate and completes the preparation accounting for a realized binary example. However, once the physical success probabilities have different exponents, its new cap risk follows from a common atom and geometric waiting. R54-Q1–Q3 make this separation especially explicit: the terminal mark is asymptotically unnecessary, and at finite cap intensity even a single acceptance bit captures the limit.

This does not diminish the actual geometric realization or the importance of charging failures. It does limit the weight that the added theorem can carry in a top-level significance argument. The construction fixes the two alternative-dependent profiles and the flight design. It is neither an unrestricted-nuisance estimator nor an optimal end-to-end preparation theorem across designs. The author correctly avoids those claims. Thus the new theorem resolves the earlier technical suggestions without independently resolving the earlier publication reservation.

### R54-E3. The common measure links the parts, but does not equate their experiments

The unnormalized relative boundary measure genuinely links exact rigidity, coarsening, and acquisition. The introduction now identifies that link and distinguishes the observation models. The point is not an arbitrary page limit: 281 pages are not a mathematical error. It is whether the full treatment delivers a general consequence commensurate with its scale. The exact law inverse, model-local scalar coordinates, specified-pair likelihood limits, finite-histogram inverse, and richer calibration sensor still require different premises. The later quantitative acquisition theory is not a corollary with the same observation model as Theorem A. [S1]

I remain unpersuaded that the combined article, on this showing, demonstrates the exceptional synthesis required for the requested placement. Preservation of every historical block is valuable for provenance but cannot substitute for an article-level argument. I do not mandate deleting proved material, weakening the central theorem, splitting the paper, or adding yet another tailored theorem. Those are research and editorial choices, not outstanding mathematical corrections in this report.

### Targeted primary-source check

Osius's association framework treats odds ratios with unrestricted marginals; the manuscript credits this background rather than presenting the cancellation as a new general principle. That literature does not by itself supply the billiard relative limit or signed geometric inverse. [L1]

The spectral comparisons use different observations. Finamore–Leguil concern enriched marked length data for finite-horizon Sinai billiards; De Simoi–Kaloshin–Leguil concern analytic open billiards under non-eclipse and symmetry/genericity hypotheses. No reduction between their spectral data and the selected boundary-law datum is established here, so the comparison does not prove either redundancy or a strict strengthening. Florio–Leguil's fifth-version notice records removal of an erroneous geometric spectral-rigidity assertion; the present manuscript does not rely on that removed assertion. [L2–L4]

These checks concern primary bibliographic records, stated scopes, and attribution. They are not a fresh proof audit of the cited external papers or an exhaustive novelty search.

## 8. Reproduction and final disposition

The authorized workflow artifact was downloaded and its SHA-256 matched to GitHub's run-artifact metadata. All 626 frozen source files were checked by byte count, SHA-256, and Git blob identity. Reconstructing their manuscript tree gives `407b278984b14e57468e727fb56b0fa4163a7207`. All 111 distinct active inputs and 34 native evidence files matched the manifests. [D1]

Both complete entries were independently rebuilt, companion first, with shell escape disabled. Every one of the 288 pages matched its native counterpart in extracted text and 72-dpi RGB arrays under the same PyMuPDF renderer. PDF byte identity is not claimed. Direct visual inspection was limited to main pages 107, 109, and 110; the inspected mathematical text was legible, with no observed clipping on those pages. The main rebuild retained four underfull-vbox notices. Both final rebuild logs also contained the expected `epstopdf` warning that shell escape was disabled. No overfull-box or unresolved-reference/citation warning was found in the final log scans. [D1]

The author checker under ordinary and optimized Python produced identical outputs matching the retained native result. The independent reviewer script imports no author code; its ordinary and optimized outputs also agree. Its exact rational checks, finite probability controls, and numerical limiting examples support the displayed calculations but do not prove the billiard realization or certify the infinite-dimensional arguments. The written proofs, not the diagnostics, carry those claims. [D2]

**Final disposition:** the strengthened corollary and new stopping/cap theorem survive this review. R53-Q1 and R53-Q2 are closed, and no additional mathematical result is requested merely to continue the revision loop. I nevertheless **do not recommend acceptance at the requested highest general mathematics journal level**, for the contribution and synthesis reasons stated above. This is not a finding that Theorems A or B are false, not a full proof certificate, and not a claim that further research is impossible.

Source keys [S1]–[S8], revision records [R1]–[R2], reproduction evidence [D1]–[D2], and primary references [L1]–[L4] are specified with paths, line ranges, and immutable identities in [AUDIT_AND_REPRODUCTION.md](AUDIT_AND_REPRODUCTION.md).
