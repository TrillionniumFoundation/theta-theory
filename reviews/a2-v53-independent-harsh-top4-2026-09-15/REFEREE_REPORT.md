# Independent referee report on A2, revision 53

**Manuscript:** *Boundary laws and rigidity of periodic dispersing billiards*  
**Author:** Qian Qi  
**Date:** September 15, 2026  
**Assessment requested:** stringent external-referee-style review at the highest general mathematics journal level. This is an author-requested, AI-assisted assessment, not a commissioned report or a decision of any journal.

## 1. Recommendation and scope

**Recommendation: do not accept at the requested highest general-journal level on the present contribution and article-level case.** This is an editorial recommendation, not a finding that the main rigidity theorem is false. In the proof coverage specified below, I identify **no newly established fatal error and no mandatory correction to the three new mathematical statements**. The new realization and testing calculation survive scrutiny. The finite-flight condition is sufficient but unnecessarily strong; a sharper comparison follows from the same hypotheses. A separate calculation below makes the distinction between conditional marks and retained waiting counts especially pronounced for the very pair constructed in this revision.

The reviewed object is A2 v53, not the historical A1 manuscript on the repository's default branch. The frozen review-ready commit is `da8d788ee1ba5a34c7430ccca805ae9524bcca88`, on `revision/a2-v53-review-ready-2026-09-15`. The compiled mathematical source is `42cc62f230473c34d78af1d06b9ca5c2651ae86d`, with manuscript subtree `6153e28c29bd54c2d45f6466d3c3c3bf6dd09942`. These identities are not interchangeable. The main manuscript has 278 pages; the two-collision companion has seven. [D1]

I read the complete new Section 23, the response to the v52 report, the structural introduction, the window inverse, and the principal inherited proof modules identified in the audit ledger. Fresh checks include the half-line/relative determinant mechanism, actual-smooth finite-jet factorization, signed density extraction, selected-channel skeleton, finite noncircular matching, lattice recovery, and differential-kernel interfaces. This is **not** a fresh line-by-line certification of every theorem in all three parts, every older statistical experiment, or the companion. Complete-source rebuilding and page comparison have much broader coverage than this mathematical audit and must not be confused with it. Source keys, exact paths, line ranges and blob identities are in [the audit ledger](AUDIT_AND_REPRODUCTION.md) and `reproduction.json`.

The report's technical additions in Sections 4 and 5 are reviewer-derived consequences, with proofs, rather than attributed manuscript results. They are not new demands imposed retroactively on the preceding revision.

## 2. What revision 53 actually changes

The inherited structural conclusions are substantial: selected signed same-type endpoint laws at known positive offsets recover nonlinear actions; the signed contact inverse recovers finite graph jets; analyticity propagates the resulting germs to complete obstacle images; finite noncircular symmetry leaves finitely many global matching alternatives; two independent marked cycle gains recover the lattice. The infinitesimal theorem removes the geometric derivative kernel modulo one common proper Euclidean motion, and finite scalar coordinates follow only after restricting to an immersed finite-dimensional model. [S1, S3–S9]

Revision 53 adds a specific quantitative complement to this chain. It realizes the preceding referee's functional small-window benchmark using actual noncircular analytic periodic obstacles, proves an attained two-point successful-record scale with a critical likelihood limit, and transfers that experiment to finite flights. The fixed profiles are chosen on a common collar before the observation window shrinks. The actions are actual nonlinear actions; exact quadratics are not asserted. This is a genuine improvement over a purely functional example. [S2, R2]

The relationship to the preceding report is as follows.

| Previous point | Assessment in v53 |
|---|---|
| Complete-support centering and attribution | Remains addressed. The centering result is not relabelled as the full inverse or as a smooth-noise estimate. |
| Interior cropping must not secretly reveal the cap boundary | Remains addressed. The known window is strictly interior and must retain both critical lines. |
| Local smooth regularity is not uniform statistical stability | Correct distinction retained. The new shrinking-window calculation illustrates rather than contradicts it. |
| Exact geometric fibers require both inclusions | Both inclusions remain present; the nuisance projection is not a claim to identify every profile. |
| Functional quadratic benchmark had no proved geometric realization or matching test | The new explicit family and Theorem 23.2 supply those two additions, within a specified two-point nuisance experiment. |
| A common measure must explain the different observation models | The explanation is retained and made more concrete. It does not identify those experiments with one another. |
| Highest-journal significance | A separate judgment, not a compliance item that becomes resolved by appending another theorem. |

The previous report expressly identified no mandatory theorem correction and did not request a further theorem as the price of closing its bounded requests. The response acknowledges that fact. I keep those requests closed. Neither this review nor a future revision should turn an editorial disagreement into an endless list of invented mathematical gaps. [R1, R2]

## 3. Detailed examination of the new results

### R53-M1. Lemma 23.1: normalization and the leading information coefficient

Put $a_i=S_i''(0)$ and $\Delta=a_1^2-a_0^2$. Evenness and the stated $C^4$ control give

$$S_i(hz)=\tfrac12a_i h^2z^2+O(h^4),\qquad
 t_i(hz)=\frac{a_i}{2d}h^2z^2+O(h^4),$$

uniformly on the fixed rescaled interval. The density is

$$q_{i,h}(z,w)=\frac{1-t_i(hz)t_i(hw)}{4-I_i(h)^2},\qquad
 I_i(h)=\int_{-1}^1t_i(hz)\,dz.$$

Expanding the denominator is essential. With $F(z,w)=1/9-z^2w^2$ it yields

$$q_{i,h}=\frac14+\frac{a_i^2}{16d^2}h^4F+O(h^6),\qquad
 \int F=0,\quad \int F^2=\frac{224}{2025}.$$

The integrals here use Lebesgue measure on $[-1,1]^2$. Since the limiting density is $1/4$, the leading difference of square roots equals the leading difference of densities. Thus, under the manuscript's convention $H^2=\int(\sqrt p-\sqrt q)^2$,

$$H^2(Q_{0,h},Q_{1,h})=
 \frac{7\Delta^2}{16200d^4}h^8+O(h^{10}).$$

The omitted higher action terms first affect the density remainder at order $h^6$, and hence the squared Hellinger remainder at order $h^{10}$. They do not have to vanish. Distinct positive $a_i$ give a nonzero leading contrast and $\operatorname{TV}(Q_{0,h},Q_{1,h})=\Theta(h^4)$. The constants are for the specified pair; no uniform positive separation over coalescing alternatives is being proved.

The moments also agree:

$$\mathbb E_iF=\frac{14a_i^2}{2025d^2}h^4+O(h^6),\qquad
 \operatorname{Var}_i(F)=\frac{56}{2025}+O(h^4).$$

**Assessment:** the expansion, convention and constants are correct in this audit. In particular, there is no missing factor of two in the Hellinger or subsequent likelihood coefficient. The independent script detects the incorrect coefficient obtained by omitting the window normalizer. Its synthetic quartic-action checks corroborate the expansion but are not a numerical proof of billiard realization. [S2, D2]

### R53-M2. Theorem 23.2: the geometric realization is not a formal substitution

For $R=1/10$, $s\in[R/128,R/64]$ and

$$k_s(\theta)=R+s(\cos4\theta-1),$$

the curvature radius is

$$k_s+k_s''=R-s-15s\cos4\theta\ge R-16s\ge3R/4.$$

The support is at most $R$, so the body lies in the radius-$R$ disk. Its integer translates are disjoint. At both axis contacts the support value is $R$ and its first derivative vanishes, giving the common gap $g=1-2R=4/5$. Every third lattice center has distance at least one from the relevant unit axis segment; containment in radius-$R$ disks gives a strictly positive third-obstacle clearance. These are all-lattice arguments, not the output of a finite collision simulation. They supply common local gates and collars. A global finite-horizon assertion is neither needed nor established here.

The quarter-turn symmetry identifies horizontal and vertical channels; the appropriate reflections identify the two contact types and make their actions even. Half-line uniqueness transfers these geometric symmetries to the actual actions. Noncongruence follows, for example, from the perimeter $2\pi(R-s)$, which varies with $s$. The contact curvature and half-line Hessian satisfy

$$\kappa_s=(R-16s)^{-1},\qquad a_s^2=\kappa_s^2+2\kappa_s/g.$$

At the endpoints of the parameter interval,

$$a_0^2=\frac{7800}{49},\qquad a_1^2=\frac{1900}{9},\qquad
 \Delta=\frac{22900}{441}.$$

I also checked the quadratic coefficient directly by summing the quadratic flight energy along the decaying linear half-line orbit. It agrees with the displayed Hessian formula. This finite calculation is a cross-check of the coefficient, not a replacement for the nonlinear half-line construction. [S2, S3, D2]

The recording choice

$$e_s(u)=\frac{c_*}{B_s(u)(d-S_s(u))}$$

is admissible on one fixed sufficiently small collar, with a common sufficiently small $c_*>0$ and a smooth positive extension bounded by one. The resulting profiles need not become smaller as $h$ decreases. Cancellation with the full limiting density indeed gives the normalized $q_{s,h}$ in the lemma. The source is careful that these profiles may differ between the two nuisance alternatives. They are not a table-independent programmable sensor constructed from an unknown table. That is a restriction on the experiment, not a flaw in this existential two-point construction.

**Assessment:** the stated realization survives. Rejecting it because generic actions have higher coefficients, because the examples have symmetry, or because the ambient array need not have finite horizon would misread the theorem.

### R53-M3. The testing regimes and the meaning of attainment

Writing $r_h=(q_{1,h}-q_{0,h})/q_{0,h}$ gives

$$\|r_h\|_\infty=O(h^4),\qquad \mathbb E_0r_h=0,\qquad
 \mathbb E_0r_h^2=\mathcal J h^8+O(h^{10}),\qquad
 \mathcal J=\frac{7\Delta^2}{4050d^4}.$$

The cubic log-likelihood remainder is $O(h^{12})$ per record. When $nh^8\to\lambda\in(0,\infty)$, both $nh^{10}$ and $nh^{12}$ vanish. Bounded triangular-array increments justify the normal limits with means $\mp\lambda\mathcal J/2$ and variance $\lambda\mathcal J$. The likelihood-ratio threshold is a continuity point of both limits, so the optimal equal-prior error tends to $\Phi(-\sqrt{\lambda\mathcal J}/2)$. The subcritical conclusion follows from affinity tensorization.

For the upper bound, $F$ has range length one. The exact two means differ by a positive constant times $h^4$; the midpoint test therefore has error at most $\exp(-cnh^8)$. Moreover, the square of the leading mean contrast divided by the limiting variance is precisely $\mathcal J h^8$, so the same test attains the critical limit. The constants depend on the specified positive two-point contrast; they are not uniform over the unrestricted nuisance class.

**Assessment:** all three regimes are supported. The adjective “attained” is justified for the specified two-point successful-record problem. It is not a uniform minimax theorem over arbitrary geometries and separate profiles, not an estimator for an unknown infinite-dimensional nuisance, and not a lower bound in total preparations. The manuscript expressly preserves these distinctions. [S2]

### R53-M4. Corollary 23.3: uniform cropping and the mass calculation

The inherited relative theorem supplies a uniform density error on a fixed physical interior square, not merely weak convergence separately for each window. Multiplication by the fixed bounded recording weight and integration over a window of area $4h^2$ give an unnormalized integral error $O(h^2\tau^J)$ and normalizers comparable to $h^2$. In the rescaled quotient those area factors cancel. Therefore

$$\|q_{s,J,h}-q_{s,h}\|_\infty\le C\tau^J$$

is justified uniformly in small $h$. A generic total-variation conditioning inequality would lose information here and produce an unnecessary inverse-area factor. The source correctly avoids that loss.

Telescoping products gives the stated sufficient condition $n\tau^J\to0$. The source also retains the additive finite-flight error rather than claiming an unqualified exponential testing bound. Finally,

$$r_{s,\infty}(h)=\frac{c_*^2h^2}{dZ_s}\{4-I_s(h)^2\},\qquad
 r_{s,J}(h)\asymp h^2,$$

follows by direct substitution. Repeating independent preparations to obtain $n$ accepted records costs expectation $n/(\pi_{s,J}r_{s,J}(h))$. An expected waiting-time identity is not a deterministic preparation-cap guarantee.

**Assessment:** no invalid exchange of limits or normalization error is identified. The product bound is, however, not the best bound supplied by these hypotheses. [S2, S3, S5]

## 4. R53-Q1: a sharper finite-flight transfer under the same hypotheses

This is a nonfatal sharpening of Corollary 23.3, not a counterexample. After decreasing $h_0$ and increasing $J_0$, all relevant rescaled densities are bounded below by a common $m>0$. Consequently,

$$H^2(Q_{s,J,h},Q_{s,h})
 =\int\frac{(q_{s,J,h}-q_{s,h})^2}
 {(\sqrt{q_{s,J,h}}+\sqrt{q_{s,h}})^2}
 \le C\tau^{2J}.$$

For $n$ independent records, including a fixed allocation among the displayed channels, affinity tensorization and $\operatorname{TV}\le H$ yield

$$\operatorname{TV}\left(\bigotimes_{k=1}^n Q_{s,J,h}^{(k)},
                         \bigotimes_{k=1}^n Q_{s,h}^{(k)}\right)
 \le C\sqrt n\,\tau^J.$$

Thus **$n\tau^{2J}\to0$ suffices** to transfer the entire testing experiment in total variation. The displayed upper error can correspondingly be improved to

$$\exp(-cnh^8)+C\sqrt n\,\tau^J.$$

At the critical scale $nh^8\asymp1$, this comparison needs $\tau^J=o(h^4)$ rather than the manuscript's stronger $\tau^J=o(h^8)$. This changes a sufficient logarithmic flight-length coefficient. It does not identify an optimal geometric convergence exponent or an optimal preparation complexity.

For the supercritical mean test one can do better still than a product comparison. Since $F$ is bounded, each finite-flight mean differs from its ideal mean by $O(\tau^J)$. If $\tau^J=o(h^4)$, the ideal exact midpoint remains at distance at least $c'h^4$ from each finite-flight mean. Applying the same bounded-variable inequality directly under the finite-flight laws gives error $\exp(-c''nh^8)$ for sufficiently small $h$. This conclusion for one fixed statistic does not require approximating the full $n$-record experiment and should not be conflated with the preceding product-distance statement.

**Disposition:** optional mathematical improvement, with the proof now supplied. The existing stronger sufficient condition is correct. It is not a mandatory repair and is not a reason by itself to reject the manuscript. [Reviewer derivation from S2; finite affinity controls in D2.]

## 5. R53-Q2: waiting counts strongly distinguish this actual pair

The last paragraph of the new corollary correctly says that waiting counts may retain information absent from conditional marks. For this particular constructed pair one can replace “may” by a precise asymptotic separation.

Keep one channel and the two specified profiles, fix the admissible positive $d$, and let $J_h$ be even with $J_h\to\infty$. For the symmetric contact pair,

$$\gamma_i=\operatorname{arcosh}(1+g\kappa_i),\qquad
 \gamma_1>\gamma_0>0.$$

The relative fixed-offset law gives $\pi_{i,J}\asymp e^{-\gamma_iJ}$ with positive fixed constants, while the corollary gives $r_{i,J}(h)\asymp h^2$ uniformly. Hence the accepted probability per preparation,

$$p_i(h)=\pi_{i,J_h}r_{i,J_h}(h),$$

satisfies

$$\rho_h:=p_1(h)/p_0(h)\asymp
 e^{-(\gamma_1-\gamma_0)J_h}\longrightarrow0.$$

This uses the actual two billiard tables; the gap being unchanged does not make their escape exponents equal. [S2, S3]

Let $W$ be the number of independent preparations up to and including the first accepted record. Under alternative $i$, $W$ has geometric parameter $p_i$. Set

$$m_h=\left\lceil(p_0p_1)^{-1/2}\right\rceil,$$

and choose alternative zero when $W\le m_h$, otherwise alternative one. Then

$$\Pr_0(W>m_h)\le e^{-p_0m_h}\le e^{-\rho_h^{-1/2}},$$

$$\Pr_1(W\le m_h)\le m_hp_1\le\sqrt{\rho_h}+p_1.$$

Its equal-prior error tends to zero. On the other hand, a single accepted endpoint mark, after discarding $W$, has law $Q_{i,J_h,h}$ and

$$\operatorname{TV}(Q_{0,J_h,h},Q_{1,J_h,h})
 \le C\tau^{J_h}+O(h^4)\longrightarrow0.$$

Its optimal equal-prior error tends to $1/2$. The comparison is between the same repeat-to-first-success acquisition transcript and its coarsening, not two arbitrary unrelated sensors.

There is also a precise binary deficiency formulation. Let $\mathcal E_h$ retain only the mark and $\mathcal F_h$ retain $(W,\text{mark})$. Define deficiency using the infimum, over Markov kernels, of the maximum total-variation error over these two alternatives. Discarding $W$ gives $\delta(\mathcal F_h,\mathcal E_h)=0$. For any kernel $K$ in the other direction, contraction and the triangle inequality give

$$\operatorname{TV}(F_{0,h},F_{1,h})
 \le 2\max_i\operatorname{TV}(KE_{i,h},F_{i,h})
       +\operatorname{TV}(E_{0,h},E_{1,h}).$$

The first pairwise distance tends to one and the last to zero, so $\liminf\delta(\mathcal E_h,\mathcal F_h)\ge1/2$. The kernel ignoring its input and returning the equal mixture of the two $F$ laws gives the reverse bound $\delta\le1/2$. Therefore

$$\delta(\mathcal E_h,\mathcal F_h)\longrightarrow\frac12.$$

This calculation does **not** say that one waiting count is inexpensive: its expected preparation cost is $1/p_i$, which can be very large. The test is for the two specified alternatives, just as the manuscript's mark test is. It proves neither a universal waiting-count estimator nor a deterministic-budget advantage of a claimed order.

**Disposition:** a concrete consequence of the supplied model and a useful interpretation test, not a contradiction of the manuscript. The author explicitly excludes transporting the conditional lower bound to this richer record. The result emphasizes why the new $h^{-8}$ scale cannot be advertised as the physical inverse problem's general preparation complexity. It also supplies a sharper comparison on one actual geometric family without demanding another appended manuscript section. [Reviewer derivation; finite waiting-time controls in D2.]

## 6. Fresh checks of the inherited rigidity mechanism

### R53-M5. The nonlinear relative law remains the principal forward achievement

The reference twist is exponentially small, $d_j^0=q_p/\sinh(j\gamma)$. An arbitrary absolute action remainder would not control the normalized amplitude. The source instead uses the exact cofactor identity

$$\log b_j=\sum_i\log\{g[-\ell_{i,uv}(y_i,y_{i+1})]\}
            -\log\det(I+G_j\Delta H_j).$$

The half-line perturbation is trace class by summing localized tridiagonal entries. Gluing the two half-lines gives an exponentially small residual with polynomial flight-length factors; diagonal dominance controls the correction. Retaining two separated endpoint blocks and comparing the compressed reference Green kernels produces a relative determinant estimate. The trace-series telescoping retains one trace-norm factor, rather than multiplying an unweighted operator estimate by the number of sites. Fixed-order differentiated estimates retain exponential margins. The fixed-offset integral then keeps the nonlinear actions instead of collapsing to the quadratic model. [S3]

These are substantive analytical steps. I found no new relative-normalization gap in their inspected argument. At the same time, this audit does not newly certify every earlier full-phase event construction used by that argument; its fresh proof coverage is explicitly recorded.

### R53-M6. The action-to-contact inverse is not merely formal

For two smooth graph pairs agreeing through degree $M$, the interpolation and finite envelope identity control the actual action difference by

$$|S_b^{[1]}(u)-S_b^{[0]}(u)|
 \le\frac{C_M}{1-\rho^{M+1}}|u|^{M+1}.$$

The endpoint term at a finite truncation is retained until it tends to zero. Thus the finite action jet is independent of the choice of smooth representative. Only after that step is the last-jet block used:

$$M_n=\begin{pmatrix}
 \coth(n\gamma)&r_0^n\operatorname{csch}(n\gamma)\\
 r_1^n\operatorname{csch}(n\gamma)&\coth(n\gamma)
 \end{pmatrix},\qquad r_0r_1=1,\quad\det M_n=1.$$

Boundary visits count once and interior visits twice. The triangular inverse is at each fixed order, with functional smooth bounds. It does not prove order-uniform conditioning or equality of arbitrary smooth germs with the same Taylor series. The later equality of complete boundary images uses analyticity. The signed odd terms remain in the inverse. [S4, S5]

### R53-M7. Window, global and differential interfaces retain their actual hypotheses

On the positive window, the mixed logarithmic derivative is

$$\partial_x\partial_y\log p
 =-\frac{S'(x-\xi)S'(y-\eta)}
 {[d-S(x-\xi)-S(y-\eta)]^2}.$$

Its unique zero fibers locate the origins because both critical lines are retained and the action is strictly convex. A nonzero scalar anchor then fixes the action scale. The local smooth extension uses simple-root extraction, translated restrictions and positive denominators; it is not a total-variation-to-derivatives inverse. Both geometric fiber inclusions and the projected joint nuisance/table kernel remain explicit. [S6]

For the selected skeleton, obstruction descent gives a finite path of clear pairs; quotienting suitable paths produces two independent cycle gains. Their gain matrix need not be unimodular. The finite noncircular reconstruction propagates only finitely many incidence rotations and then uses $L=(v_1\ v_2)M^{-1}$. It subsequently tests shape consistency, determinant, all relevant separation and channel clearance. It does not infer realizability merely from dimension counting. The local angular lift follows the actual congruence branch, including symmetry breaking; finite rotations are not continuous infinitesimal ambiguities. [S7, S8]

The differential argument includes the moving reference,

$$\dot G=-G\dot H^0G,\quad
 \dot{\Delta H}=\dot H-\dot H^0,\quad
 \dot{(G\Delta H)}=\dot G\Delta H+G\dot{\Delta H}.$$

It justifies the moving-cap normalizer and makes the variation itself analytic through the common-strip assumption. Exact nonlinear injectivity is not used as a substitute for a derivative-kernel proof. Finite-dimensionality enters only when selecting a basis of scalar test derivatives; the local lower Lipschitz estimate compares the derivative to one fixed invertible matrix on a convex ball. [S9]

These interfaces withstand the stated scrutiny. The richer pilot/histogram acquisition theory retains additional sensors and quantitative margins; this review does not promote its introductory description into a fresh certification of all its proofs.

## 7. Literature, significance and the publication recommendation

The targeted primary-source check supports the manuscript's distinction between the inherited odds-ratio algebra and billiard reconstruction. Osius's association framework treats odds ratios while leaving marginals unrestricted. The manuscript credits that background; its relative dynamical limit and signed geometric inverse are not thereby shown to be prior results. Conversely, the cancellation itself should not be counted as a new general association principle. [L1]

The spectral-rigidity comparators use different observations. Finamore–Leguil concern enriched marked length data for finite-horizon Sinai billiards; De Simoi–Kaloshin–Leguil concern analytic open billiards with axial symmetries and additional hypotheses. No reduction from those data to these conditional boundary laws, or conversely, is established in the inspected manuscript. Florio–Leguil's fifth version explicitly records removal of an erroneous geometric spectral-rigidity assertion while retaining dynamical results; the present manuscript does not rely on that removed assertion. These checks concern the primary bibliographic records and stated scopes, not a complete re-review of those external proofs or an exhaustive priority search. [L2–L4]

**R53-E1 — The main contribution deserves to be judged on its strongest mechanism, but the information supplied remains highly structured.** The relative physical law followed by the actual-smooth signed inverse is the strongest mathematical contribution. It should not be dismissed as elementary cross-ratio manipulation. However, the global inverse is supplied selected obstacle and deck marks, signed physical transverse conventions, gaps, known offsets, and exact function-valued local laws. In the window version both critical lines must remain visible. The $N+1$ count is the size of a selected connected two-cycle design, not the number of scalar data or successful preparations. The model-local finite-coordinate conclusion does not remove these distinctions.

Under these observations, the later global steps exploit complete analytic continuation and finite congruence compatibility. That is legitimate rigidity, but its strength cannot be evaluated as though it recovered a table from a short unmarked trajectory or a finite vector of arbitrary noisy observations. In my judgment, the manuscript demonstrates a serious specialized inverse-dynamical result without yet making a sufficiently compelling case for exceptional general-journal significance. This is a weighting of the demonstrated contribution and supplied data, not a proof that the result is known or a prediction that no editor could weigh it differently.

**R53-E2 — The new information example strengthens the paper but does not transform its central difficulty.** The actual realization is useful and the critical testing calculation is correct. Once the normalized interaction has been arranged by the explicit alternative-dependent profiles, the $h^4$ density contrast, $h^8$ squared distance, bounded-statistic test and Gaussian critical limit follow from Taylor expansion and tensorization. The extension makes a previous limitation geometric and quantitative; it does not solve a uniform unknown-nuisance estimation problem or an end-to-end charged acquisition problem. Sections 4 and 5 above further delimit that return: the full-experiment finite-flight comparison is nonsharp, while the discarded waiting record distinguishes the same alternatives very strongly.

Neither observation makes the theorem false. They do affect how much broad inferential content should be assigned to the new example. It is a worthwhile consequence of the central relative law, not, in my assessment, a second breakthrough that independently settles the preceding placement reservation.

**R53-E3 — A common forward object is not automatically a single article-level theorem.** The unnormalized boundary measure genuinely links the three parts. Nevertheless exact law-valued rigidity, interior smooth inversion, model-local scalar coordinates, specified two-point testing, and acquisition with a richer calibration sensor remain different experiments with different hypotheses. The introduction now says so clearly. The issue is not a missing disclaimer or an arbitrary numerical page limit. It is whether their combined treatment produces a general consequence commensurate with the scale and requested placement. I remain unpersuaded on the present showing.

Preserving the inherited 538 statement/proof blocks is valuable provenance discipline; it is not cumulative evidence of journal-level impact. Nor should a negative placement judgment be answered automatically by adding one more narrowly tailored result. No deletion of proved material, weakening of theorems, or new unrequested mathematical target is mandated by this report. The publication decision and any further research direction should be separated from the closure of concrete technical requests.

## 8. Reproduction and final disposition

The authorized GitHub workflow artifact was downloaded and its SHA-256 matched against GitHub's artifact digest. All 612 frozen files were checked by byte count, SHA-256 and Git blob identity. Reconstructing the source tree gives `6153e28c29bd54c2d45f6466d3c3c3bf6dd09942`, also identified by GitHub for the manuscript directory at the compiled-source commit. All 111 active inputs and 34 native evidence files match their manifests. [D1]

Both complete entries were independently rebuilt, companion first, with shell escape disabled. All 285 pages match the native products in extracted text and in 72-dpi RGB arrays under the same PyMuPDF renderer. PDF byte identity is not claimed. Direct visual inspection was limited to main pages 103–107. The final main log has four underfull-box notices; the final scans found no overfull box or unresolved reference/citation. The companion final log has no such warnings. These facts concern reproduction, not theorem validity. [D1]

The author checker was rerun under ordinary and optimized Python, producing identical outputs matching the native retained result. Its preservation component finds 107 inherited active inputs unchanged in place, three archived originals, and all 538 inherited statement/proof blocks, including 253 proofs, retained. The reviewer-written checker imports no author code and also produces identical ordinary/optimized outputs. Its exact rational, synthetic quartic, affinity and waiting-time controls are finite diagnostics; the proofs and their limitations are the arguments in this report. [D2]

**Final disposition.** Revision 53 positively answers the geometric-realization limitation of the earlier functional benchmark and proves the stated attained two-point mark scale. Its new lemma, theorem and corollary require no mandatory mathematical correction identified here. The finite-flight sharpening and retained-count comparison are nonfatal, explicit reviewer contributions. The bounded requests previously closed remain closed. Nevertheless, **I do not recommend acceptance at the requested highest general mathematics journal level**, for the contribution and synthesis reasons above. This conclusion is neither a full mathematical certificate nor a claim that further progress is impossible.
