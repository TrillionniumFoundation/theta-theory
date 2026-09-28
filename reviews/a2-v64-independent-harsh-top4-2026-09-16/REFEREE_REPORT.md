# Independent referee report on A2, revision 64

**Manuscript:** *Boundary laws and rigidity of periodic dispersing billiards*  
**Author:** Qian Qi  
**Review date:** September 16, 2026  
**Requested standard:** Annals of Mathematics / Inventiones Mathematicae / Acta Mathematica / Journal of the American Mathematical Society.

This is an author-requested, AI-assisted external-referee-style assessment, not a commissioned journal report, editorial decision, or formal proof certificate. Mathematical correctness, originality, exceptional significance, and reproducibility are separate questions. The author's response and diagnostic records are claims to examine, not substitutes for proofs.

## 1. Recommendation and frozen object

**Recommendation: decline at the requested highest general-journal level on the present exceptional-significance case. No new fatal mathematical error or mandatory core proof repair is established within this round's coverage.** The periodic-itinerary extension is substantive and addresses an actual limitation of the previously reviewed forward mechanism. In particular, it is no longer accurate to describe the relative forward theorem as confined to a normal alternating two-contact orbit.

The six statements in the new Section 8 withstand the scoped examination below. The geometric scaling, chronological transfer normalization, relative determinant comparison, oblique physical time, and nonnormal realization have been examined directly. This conclusion is not a certification of all 448 delivered pages. The adverse placement judgment is reconsidered on the broader theorem, not inherited merely because earlier reports were adverse.

| Object | Frozen identity |
|---|---|
| Actual compiled mathematical source | `ee2380ceb76808dd2969d6b5faaa180737020eff` |
| Reconstructed manuscript subtree | `513b2538cea797cb340e02e69f45543f8b4e9571` |
| Source branch | `revision/a2-v64-referee-response-2026-09-16` |
| Native-products branch | `revision/a2-v64-native-products-35055120579-1` |
| Native-products head used as review parent | `60c5a25a028cafac98d6f40dbc272effc937b29a` |
| Manuscript directory | `papers/A2-v17-boundary-information-coarsening/` |
| Native workflow / attempt / artifact | `35055120579` / `1` / `10429927974` |
| Previous v63 report | `493196e4f6f1d9a46c062df0e3669c3ca26c4fcc` |
| Source reviewed in that report | `f5517519440b897707ddc60deeafba19e86bb5a5` |

At the inspection snapshot, a separately named v64 review-ready branch was not listed; the source and completed native-products branch were available. This report reviews that actual delivery and does not invent a review-ready ref. The source-to-products comparison contains two delivery commits and no changed mathematical input. The principal article has **133 pages**, the full technical manuscript **308 pages**, and the companion **seven pages**. Page references below are to the principal article. [D1]

### Coverage

The complete new module `article/10a_periodic_itinerary_relative_v64.tex`, lines 1–549, and its shared introductory overview were read. This includes all six statements and proofs, not only the response's summary. The current abstracts, principal mechanism statement, response, cover letter, historical audit, dependency ledger, and literature note were examined for consistency. The new module was also fetched at the immutable source; its Git blob `35a9f495313d342f710995be42fafb19eba91160` agrees with the frozen archive. [S1–S7, R2]

This round is not a fresh line-by-line audit of all inherited inverse, global matching/lattice, moving-family, calibration, and statistical proofs. In particular, the entire v59 Banach-space inverse, v60 conditional-continuation proof, earlier finite-chain/full-phase prerequisites, complete finite-experiment catalogue, and companion are not freshly recertified. The entire finite-experiment and position-pilot modules are independently verified byte-identical to the reviewed v63 inputs. That establishes retention, not a new proof of their contents. Mechanical reproduction of every page has a different scope.

## 2. Disposition of the preceding review

| Previous point | Present disposition |
|---|---|
| R62-m1, closed in v63: all-history pilot-grid ceiling | Remains closed. The complete corrected module is unchanged. |
| Published Zelditch comparison and estimator-existence/computation distinction | Retained; no regression was found in the revised framing. |
| R63-E1: demonstrated reach of the relative mechanism | Materially improved. Theorem 8.3 is a forward theorem for selected clear nongrazing periodic itineraries, not merely another alternating example. |
| Complete-germ and calibration-inclusive finite-observation consequences | Retained under their existing alternating-channel and experimental hypotheses. |
| Exceptional significance | Reassessed in Section 6. The broader forward theorem deserves credit, but does not automatically settle placement. |

The v63 report established no new mandatory core repair. Revision 64 is therefore an extension of an examined mechanism, not a repair of a theorem previously shown false. The author's refusal to count another source-preservation exercise as a new theorem is appropriate. [R1–R2]

## 3. Detailed mathematical assessment

### R64-M1. The oblique Jacobi scaling and orientation are correct

Lemma 8.1, p. 27, starts with actual signed arclength charts and sets

$$x_i=\nu_i s_i,\qquad k_i=L_i^{-1},\qquad m_i=2\kappa_i/\nu_i.$$

The normal cosine is evaluated at the reference collision. The scaling is essential: the unscaled same-end chord Hessian is $\nu_i^2/L_i+\kappa_i\nu_i$, whereas the mixed entry has magnitude $\nu_i\nu_{i+1}/L_i$. Dividing by the endpoint scale factors gives precisely

$$D^2h_i(0,0)=\begin{pmatrix}k_i+m_i/2&-k_i\\-k_i&k_i+m_{i+1}/2\end{pmatrix}.$$

The negative mixed sign is not automatic for a fixed positive boundary orientation. At the initial endpoint the chord has positive outward normal component, at the next endpoint negative component. Alternating the tangent orientations makes their transverse projections have the same sign. Doubling an odd primitive period makes these signed charts return. It is not an assumption that the physical primitive period was even. [S2]

The edge quadratic form is $k_i(x-y)^2+(m_i/2)x^2+(m_{i+1}/2)y^2$. Consequently the interior operator has diagonal surplus $m_i>0$; the periodic Hessian remains coercive with the prescribed endpoint identification. The finite-dimensional persistence argument therefore has an invertible derivative, and the explicit clearance/nongrazing margins keep its continued chords physical. The argument is about a selected marked orbit, including a prescribed deck translate, not the existence of every abstract symbolic word.

No missing normal-cosine factor or sign defect was found. Independent differentiation of actual equilateral and scalene three-disk chords verifies 72 edge-Hessian and momentum configurations. These are checks of finite geometry, not a proof of persistence for every table. [D2]

### R64-M2. The exact twist requires the matrix entry, product order, and endpoint half mass

Lemma 8.2, pp. 27–28, uses

$$Q_i=\begin{pmatrix}1+m_i/k_i&1/k_i\\m_i&1\end{pmatrix},\qquad
\mathcal M_b=Q_{b+P-1}\cdots Q_b.$$

The recurrence in $(x_i,z_i)$ has determinant one. Positivity makes the monodromy trace exceed two. Different starting phases have conjugate monodromies and the same $\chi$, but their $(1,2)$ entries need not agree. Thus the exact prefactor cannot be replaced by a function of the trace alone. The chronological product in the source is the correct one. [S3]

A useful endpoint check is

$$z_0=k_b(x_1-u)-m_bu,\qquad
\partial_u E^{(2)}=-z_0-\frac{m_bu}{2}.$$

The second term records the half mass contributed by the first edge, rather than an artificially imposed exterior reflection equation. Together with

$$v=(\mathcal M_b^n)_{11}u+(\mathcal M_b^n)_{12}z_0,$$

this yields

$$D_{N,b}=\frac1{(\mathcal M_b^n)_{12}}
=\frac{\sinh\chi}{(\mathcal M_b)_{12}\sinh(n\chi)}.$$

The nonlinear cofactor formula follows from the tridiagonal Schur complement. At the reference it is the product of the $k_i$ divided by the Dirichlet interior determinant, not a cyclic determinant. The source keeps these boundary conditions straight. [S3]

The independent exact-rational check compares transfer products with a separately computed Dirichlet continuant in 288 cases, at periods 2, 4, and 6 and all starting phases. It checks the half-mass term and detects changed $(1,2)$ entries in 72 reversed-product controls. This supports the finite algebra; the Cayley–Hamilton argument is the proof for arbitrary repetition count. [D2]

### R64-M3. Uniform Green estimates do not assume the desired endpoint limit

Theorem 8.3, pp. 28–30, derives a Green bound from the actual coercive Jacobi operator. Writing $H^0=A(I-T)$, with $A_{ii}=k_{i-1}+k_i+m_i$, gives $\|T\|_\infty\le q<1$. A path joining indices $i,j$ needs at least $|i-j|$ steps. The walk expansion therefore yields an exponentially decaying kernel. Symmetry supplies the matching column-sum control. For example, the weighted majorant is bounded by

$$\sum_j q^{|i-j|}\rho^{j-i}
\le\frac1{1-q/\rho}+\frac{q\rho}{1-q\rho},\qquad q<\rho<1.$$

Deleting a remote Dirichlet boundary removes only walks reaching it. Such a walk has at least $2N-i-j$ steps before returning from index $i$ to $j$, which gives the stated reflected-kernel estimate. The retained diagonal coefficients do not change. This last point is important; deleting an edge and redefining the diagonal would be a different operator. [S4]

The nonlinear gradient remainder is local, quadratic at zero, and has an $O(r)$ derivative on a small box. The weighted contraction gives the finite bridge and both half-lines on one endpoint collar. Strict convexity supplies uniqueness among all stationary segments remaining in that box. The two-ended bound is

$$|y_i|\le C(|u|\rho^i+|v|\rho^{N-i}).$$

Differentiation leaves the same invertible highest-derivative operator. Lower derivative products remain localized. Family differentiation of the walk/resolvent formula creates only a fixed polynomial loss, absorbed using a strict exponential margin. Thus one slower exponential base may serve every separately fixed differentiation order, while the constants depend on higher norms. This is not an order-uniform smooth estimate. No missing equal-length or normal-incidence premise is used in this part.

### R64-M4. The two-ended trace-class argument controls the relative quantity

The half-line actions are sums of the gauged edges. Their summands and fixed derivatives converge by endpoint localization; the remote terminal variation tends to zero before stationarity is used for the endpoint derivative. Positive edge energy gives positive action Hessians at zero. Gluing the future and past half-lines gives an $\ell^1$ residual of order $N\rho^N$, plus endpoint overwrite errors of the same order. A uniformly bounded inverse of the averaged Hessian then gives the action comparison. [S4]

That action estimate alone would not establish the normalized twist limit. The crucial identity is instead

$$\log\beta_{N,b}=
\sum_{i=0}^{N-1}\log\frac{-\ell_{b+i,12}(y_i,y_{i+1})}{k_{b+i}}
-\log\det(I+G_N\Delta H_N).$$

The exponentially small $D_{N,b}$ has already cancelled exactly. Tridiagonality and localization bound the trace norm of $\Delta H_N$ by the entrywise absolute sum, uniformly in $N$. The argument does not multiply a crude operator-norm error by the number of sites.

The two-end compression retains $r=\lfloor N/3\rfloor$ sites at each end. The removed perturbation tails have exponentially small trace norm. The diagonal Green blocks approach their respective half-line blocks; the off-diagonal blocks have an exponentially long separation. The identity $\det(I+AB)=\det(I+BA)$ is applied after finite support has been introduced, so that the comparison is a genuine finite compression followed by a controlled half-line limit. Finally,

$$|\operatorname{tr}(T^h-\widetilde T^h)|
\le hq_1^{h-1}\|T-\widetilde T\|_1,\qquad \|T\|,\|\widetilde T\|\le q_1<1,$$

controls the logarithm. Fixed differentiated series acquire polynomial factors in $h$, still summable. The forward and backward edge data are not identified by an unproved symmetry. This supplies distinct normalized factors $B_b^-,B_b^+$. [S4]

Within this examination the relative limit is justified, including the stipulated fixed family derivatives. It is not only a formal quadratic calculation. The analytic-family assertion uses a common smaller complex neighborhood of the jointly analytic data; it should not be read as a uniform assertion about unrelated real-analytic tables without common extension control.

### R64-M5. The connected action and scalar linearizer are consequences at the correct scale

Corollary 8.4, pp. 30–31, integrates the exact mixed derivative twice, with oriented integrals on negative intervals. Therefore

$$-\frac{C_{N,b}(u,v)}{D_{N,b}}
=\zeta_b^-(u)\zeta_b^+(v)+O(\tau^N|uv|),\qquad
\zeta_b^\pm(x)=\int_0^xB_b^\pm(t)\,dt.$$

The unnormalized error has the extra factor $D_{N,b}$. Dividing the earlier absolute action error would not yield this conclusion. [S5]

For the stable return, stationary concatenation gives

$$-W_{N+P,b,uv}(u,v)
=[-W_{N,b,12}(w_N(u,v),v)]\,\partial_u w_N(u,v).$$

The joining Hessian is positive. Passing to the limit and using $D_{N+P,b}/D_{N,b}\to e^{-\chi}$ yields

$$B_b^-(T_b^-(u))(T_b^-)'(u)=e^{-\chi}B_b^-(u).$$

Integration supplies the normalized scalar linearizer; reversal supplies the past version. Differentiability at zero gives the stated uniqueness by iterating $h(\lambda x)=\lambda h(x)$. There is no claim of a new general linearization theorem. The argument identifies which geometric amplitude supplies the coordinate. The 24 finite stable-return checks are consistent with this identity but do not prove its limiting assertion. [S5, D2]

### R64-M6. The physical clock is not changed by the action gauge

Theorem 8.5, pp. 31–32, resolves the most immediate danger in extending the normal-channel law. Stationarity tolerates the telescoping linear gauge, but physical residual time does not. Here

$$W_{N,b}=nL+E_{N,b}-p_bu+p_bv,$$

so that

$$t_N-W_{N,b}=d-E_{N,b}+p_bu-p_bv.$$

Using $d-E_{N,b}$ instead would give a different physical experiment at oblique incidence. The manuscript restores the terms before integrating phase volume. [S6]

There is a common positive lower bound on the adjacent free flights near the selected nongrazing orbit. After choosing $d_+$ below that bound and shrinking the endpoint interval using the quadratic action and bounded $p_b$, the available residual $r$ lies in $[d_-/2,3d_+/2]$ and below both adjacent flight lengths. Every split $r=s+(r-s)$ then has exactly the required first and last collisions, up to null boundary cases. The first-collision convention prevents a spurious multiplicity from repetitions of the word.

The coordinate scaling introduces no extra normal-cosine factor into the measure: if $p_s$ is arclength momentum, $x=\nu_b s$ and $\pi=p_s/\nu_b$ give $dx\wedge d\pi=ds\wedge dp_s$. The generating function has $\pi=-W_{N,b,u}$, hence endpoint Jacobian $-W_{N,b,uv}$. Integrating the flux times residual time gives exactly

$$\frac{D_{N,b}}{2\pi A}\,\beta_{N,b}(u,v)
\{d-E_{N,b}(u,v)+p_bu-p_bv\}_+.$$

The fixed positive window gives a positive normalizer floor before division. Thus the success mass is $D_{N,b}Z_{N,b,d}/(2\pi A)\asymp e^{-n\chi}$ and the conditional density converges at the asserted relative rate. This is a selected windowed itinerary, not the complete maximal-count event or its full cap boundary. All-history acquisition costs for a new oblique-channel estimator are not supplied by this forward probability statement, and are not claimed. [S6]

Independent finite chains detect omission of the momentum contribution in all 96 gauge controls. These are negative controls of a wrong formula, not counterexamples to the formula actually printed. [D2]

### R64-M7. The nonnormal realization and normal specialization are genuine

Proposition 8.6, p. 32, uses three unit disks with center separation $5/2$. Their selected contact triangle has side $5/2-\sqrt3$, normal cosine $\sqrt3/2$, and third-disk clearance margin

$$\frac{5\sqrt3}{4}-\frac32>0.$$

The disks themselves have separation margin $1/2$. The surrounding cell is large enough to keep the selected chords away from translated disks. The reference orbit is therefore physical, not just a formal positive Jacobi sequence. Perturbing the contact triangle and placing disk centers behind its interior bisectors gives unequal lengths and incidence angles, with strict margins preserved. The physical primitive period is three; $P=6$ is the oriented period used in the formulas. [S7]

An independent scalene realization has lengths approximately $(0.82327,0.68217,0.81649)$ and normal cosines $(0.90937,0.84386,0.83898)$, with positive separation and third-disk clearance. This verifies that the numerical audit is not restricted to commuting identical one-step matrices. [D2]

For the normal two-contact specialization, $\operatorname{tr}(Q_{b+1}Q_b)=2\cosh(2\gamma)$ and $(Q_{b+1}Q_b)_{12}=2gc_{1-b}$. Substitution gives $D_{2n,b}=a_b/\sinh(2n\gamma)$. The change from arclength to the transverse graph chart contributes the ordinary endpoint Jacobians to the amplitude. Thus no normalization discrepancy with the retained alternating result is introduced. [S7]

## 4. Scope: what is broader, and what is not

The new theorem broadens the **forward relative mechanism** to fixed selected nongrazing periodic itineraries. The exact two-contact inverse still uses alternating geometry. The abstract, introduction and last paragraph of Section 8 state this distinction. It would be wrong to summarize v64 either as still only a normal-pair forward theorem or as a proved arbitrary-itinerary geometric inverse. [S1, S7]

Uniformity is over the stipulated compact marked class with fixed oriented period and positive geometric margins. It is not uniformity as the period becomes unbounded, incidence becomes grazing, curvature vanishes, or clearance disappears. The endpoint interval also depends on the positive offset range. These are declared hypotheses, not newly discovered hidden gaps.

Likewise the inherited complete-germ analytic and finite-preparation results retain their priors, smaller radii, realizable-law fitting, sensor conventions and preparation charges. The new forward law neither supplies a new global quantitative continuation/matching theorem nor silently changes their observation model. The source comparison confirms retention of the entire corrected finite-experiment and physical-pilot modules. This review does not reissue their previous assessments as fresh proof certifications. [S8, D1]

## 5. Primary-literature context most relevant to this extension

The new extension deserves comparison with discrete variational and hyperbolic billiard asymptotics, not only with inverse spectral titles. Two targeted primary checks are particularly useful.

**Bolotin–Treschev.** Their discrete Hill formula relates periodic action Hessians, mixed derivative factors and monodromy, and discusses orientation, including odd billiard periods. Theorem 2.1 and the adjacent orientation discussion were checked on printed p. 12. This supports treating transfer/Hessian/orientation technology as established context. Their cyclic determinant formula is not the present Dirichlet corner cofactor, however, and it does not by itself prove the nonlinear two-end conditional law. No redundancy of Theorem 8.3 follows merely from citing Hill's formula. [L1]

**Bálint–De Simoi–Kaloshin–Leguil.** In their non-eclipsing open-billiard setting, Theorem D gives exponentially small length asymptotics for periodic orbits shadowing general periodic words; Corollary E recovers marked Lyapunov data. Their statement section and introductory scope were checked. This is relevant context for general-period orbit shadowing and the extension beyond period two. The present datum is instead a fixed-window, endpoint-varying physical law with separately fixed derivative estimates. Neither a reduction between the observations nor equivalence of the theorem statements is established here. [L2]

These comparisons are not allegations of missing hypotheses, an exhaustive priority search, or a proof that the principal theorem is already known. They are more directly informative about the new mechanism than a tally of manuscript results. A bibliography-only revision would not resolve the significance reservation below. The retained v63 spectral comparisons have not been subjected to another complete primary-paper audit in this round.

## 6. Exceptional significance: the actual remaining objection

### R64-E1. The old reach objection must be updated

Revision 64 is not another arithmetic amendment. It shows that unequal flights, oblique incidence and distinct future/past tails do not destroy the relative mechanism. The geometric Jacobi reduction, physical gauge restoration, and realized nonnormal family are real additions. The earlier unqualified characterization of the forward theorem as confined to a normal alternating channel must be retired.

Nevertheless I remain unconvinced by the requested highest-general-journal placement. The extension places the mechanism in a larger but still uniformly coercive scalar discrete variational setting. Once the geometric scaling has produced a positive diagonal surplus, the proof proceeds through a nearest-neighbor resolvent expansion, a uniformly contractive local boundary-value problem, summable endpoint perturbations and trace-series continuity. These are effective and carefully matched tools. The new period-dependent coefficients do not introduce a qualitatively different analytical obstruction in that proof.

That observation does not make the result false, useless, or already known. It explains why I regard this revision as a substantial extension of one mechanism rather than an independent new level of difficulty. The exact physical normalization and actual-smooth inverse remain the parts on which the strongest significance claim must rest. The classical determinant and hyperbolic asymptotic contexts in Section 5 make it especially important to identify the contribution of their particular combination with endpoint-law reconstruction, rather than count each standard final step as another major innovation.

The new general-period theorem is forward; the geometric inverse and all global/finite-budget reconstruction consequences remain tied to the earlier alternating-channel structure. This is correctly stated and is not a correctness defect. It does mean that broadening the forward domain has not simultaneously established a new inverse for that broader domain. An exceptional-significance judgment must evaluate the actual division of labor, not infer the stronger inverse from the scope of the new forward theorem.

My recommendation is therefore adverse on the present case for depth and mathematical impact, after acknowledging the extension. It is not a categorical objection to local periodic-orbit arguments, rich function-valued data, or long papers, and it is not supported by an allegation of priority that the search has not established. Another specialist may reasonably evaluate the combined relative/action mechanism more favorably.

### R64-E2. No artificial repair condition

I do not require a grazing theorem, a period-uniform theorem, arbitrary-itinerary inversion, an unmarked spectral theorem or minimax optimality as a correction to the stated results. Those are different possible research questions, not demonstrated gaps here. Nor do I request arbitrary deletion of the inherited mathematical corpus or another small auxiliary proposition to manufacture a repair cycle.

A further editorial assessment should address the strongest actual contribution: the now broader physical relative law together with the valid two-contact inverse and its consequences. The author has already distinguished standard tools from the claimed geometric mechanism. The unresolved matter is whether that mechanism merits the proposed exceptional placement, not whether a further build certificate can be produced.

## 7. Disposition codes

**R64-D1 — New mathematics:** no mandatory core repair or fatal counterexample is established in the complete new Section 8 within this scoped review. The six new statements withstand the examination above; this is not a certificate for every inherited theorem.

**R64-D2 — Updated scope:** retire the unqualified normal-two-periodic-only objection to the forward law. Preserve the distinction between the general periodic forward theorem and the alternating-contact inverse.

**R64-D3 — Physical conventions:** retain signed/scaled charts, the chronological monodromy entry, endpoint half masses, restored physical momenta, fixed positive windows, and charged acceptance normalization. These features are correctly implemented, not outstanding repair requests.

**R64-D4 — Placement:** decline at the requested highest general-journal level on the current exceptional-significance case. Do not present this as an unresolved arithmetic error, an established lack of novelty, or a request for another nominal correction-only round.

## 8. Independent reproduction and evidence limits

The downloaded v64 native artifact has SHA-256

`5d77b2174e56fd5021c0384f4b9811add1b7ba79b2f975ad8ce2678f65b57aa6`.

Independent verification checks file lengths, SHA-256 values and Git blob identities for **800 frozen files**, reconstructs the manuscript subtree using the recorded modes, checks **129 distinct active inputs**, and verifies **45 native build-report evidence entries**. The active counts are 118 full, 50 principal and one companion. The independent v63 comparison finds all 784 inherited source paths retained: 779 byte-identical, five modified with byte-exact originals archived. All 127 inherited active paths remain; the two new shared modules make 129. Source counting is not a census of distinct theorems. [D1]

Fresh builds with shell escape disabled and regenerated auxiliaries succeeded for all three entries. All **448 pages** match the native PDFs in extracted text and same-renderer **72-dpi RGB arrays**. PDF bytes differ. Final logs contain three full-manuscript and two principal underfull-box notices, none in the companion; no undefined-reference/citation, missing-character, overfull-box or LaTeX-error pattern was found. Actual visual inspection covered principal pp. **27, 30, 31 and 32** at **108 dpi**; no clipping or unreadable formula was observed there. All-page computational parity is not all-page visual inspection. [D1]

The new mathematical diagnostic imports no author code. It checks 288 exact transfer/continuant identities, 18 phase-trace families, endpoint-half-mass and noncommuting-order controls, 72 actual edge geometries, 24 two-ended configurations, 24 finite stable-return identities and 96 physical-gauge negative controls. It uses equilateral and scalene three-disk geometries. At 24 flights, the largest numerical relative factorization discrepancy against the stated finite long-chain proxy is below $3\times10^{-14}$; the largest stable-return discrepancy is below $2\times10^{-14}$. These are floating-point finite diagnostics with a finite proxy, not rigorous bounds on the infinite limit. [D2]

Normal and optimized Python produce identical output in this environment. The author's own preservation/mathematical checker was not rerun. The delivery verifier is reused from the prior independent review, and the baseline comparator is adapted to v63; neither is presented as newly invented mathematics. No finite test proves arbitrary-order family differentiation, trace-class convergence, a complete inverse, or global statistical reconstruction.

## Source keys

All S-keys refer to actual source `ee2380ceb76808dd2969d6b5faaa180737020eff` under `papers/A2-v17-boundary-information-coarsening/`. [Immutable source root](https://github.com/TrillionniumFoundation/theta-theory/tree/ee2380ceb76808dd2969d6b5faaa180737020eff/papers/A2-v17-boundary-information-coarsening).

- **S1:** `rigidity.tex`, `main.tex`, both active introductions, and `article/00e_periodic_mechanism_overview_v64.tex`; current claims and distinction between forward and inverse scope.
- **S2:** `article/10a_periodic_itinerary_relative_v64.tex`, lines 14–94; Lemma 8.1, p. 27.
- **S3:** Same module, lines 96–150; Lemma 8.2, pp. 27–28, equations (8.3)–(8.5).
- **S4:** Same module, lines 152–344; Theorem 8.3 and full proof, pp. 28–30.
- **S5:** Same module, lines 346–411; Corollary 8.4, pp. 30–31.
- **S6:** Same module, lines 413–494; Theorem 8.5, pp. 31–32.
- **S7:** Same module, lines 496–549; Proposition 8.6, p. 32, and specialization/scope discussion, p. 33.
- **S8:** `article/23f2_finite_experiment_analytic_inverse_v62.tex` and `article/25a_common_observables_v25.tex`, independently byte-checked against v63; `journal/DEPENDENCY_LEDGER_V64.md`. Retained inputs, not newly certified complete proofs.
- **R1:** [v63 report](https://github.com/TrillionniumFoundation/theta-theory/blob/493196e4f6f1d9a46c062df0e3669c3ca26c4fcc/reviews/a2-v63-independent-harsh-top4-2026-09-16/REFEREE_REPORT.md), especially its scope, closed corrections and significance assessment.
- **R2:** `RESPONSE_TO_REFEREE_V64.md`, `COVER_LETTER_V64.md`, `HISTORICAL_DERIVATION_AUDIT_V64.md`, and `LITERATURE_CHECK_V64.md`; author-side claims and provenance, not proof substitutes.
- **D1:** `AUDIT_LEDGER.md`, `AUDIT_RESULTS.json`, `verify_delivery.py`, `compare_baseline.py` in this review directory; native artifacts 10429927974 and 10428569064; immutable source-to-products comparison.
- **D2:** `independent_checks.py` and its actual results summarized in `AUDIT_RESULTS.json`; complete emitted outputs and fresh-build logs are in the accompanying audit archive.
- **L1:** Sergey Bolotin and Dmitry Treschev, *Hill's formula*, [arXiv:1006.1532v1](https://arxiv.org/abs/1006.1532v1), especially Sections 2.1–2.3 and Theorem 2.1, printed p. 12. Theorem/orientation page inspected as a PDF screenshot.
- **L2:** Péter Bálint, Jacopo De Simoi, Vadim Kaloshin and Martin Leguil, *Marked Length Spectrum, homoclinic orbits and the geometry of open dispersing billiards*, [arXiv:1809.08947v3](https://arxiv.org/abs/1809.08947v3), especially introductory scope and Theorem D/Corollary E, printed pp. 8–9. Primary PDF text checked; screenshot retrieval failed and is not claimed as completed.

Primary-literature checks were made on September 16, 2026. They are targeted statement/context checks, not full external-paper proof audits or an exhaustive novelty investigation.
