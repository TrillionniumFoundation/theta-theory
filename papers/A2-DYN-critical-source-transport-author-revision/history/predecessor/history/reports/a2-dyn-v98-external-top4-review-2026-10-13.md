# External top-four referee report on A2-DYN revision 98

**Manuscript:** Qian Qi, *Collision records, arithmetic, and raw local inversion in a triangular Lorentz gas*  
**Reviewed author branches:** `revision/a2-dyn-v98-referee-response-2026-10-13`, `revision/a2-dyn-v98-referee-copy-2026-10-13`  
**Reviewed author commit:** `3727d8bdcf7751f4aaec9b92cf9fa85be1ea0ce2`  
**Reviewed repository tree:** `a08ac4da94bea08a23d9150f53a02d43ac71e459`  
**Active manuscript directory:** `papers/A2-DYN-v98-referee-response`  
**Canonical revision identity:** `a2-dyn-v98-quadratic-gradient-cap-and-paired-traces-2026-10-13`  
**Active mathematical source:** 237 numbered core modules; revision 98 adds modules 235--237  
**Immediate author baseline:** revision 97 at `6dd3149985ff5f6aca9dce9e2c186589df309872`  
**Frozen revision-97 paper tree:** `dea215a65a5b3f3ff51d4448cce551abed75fd1d`  
**Controlling external report:** `reviews/a2-dyn-v97-external-top4-review-2026-10-13/REFEREE_REPORT.md`  
**Controlling report commit / blob:** `5d0d67a3165bc4c97c3e468c91a87cd018b63109` / `a8b4f9dc2b6079adb8b43912f5807a59c3d977b9`  
**Exact-SHA qualification runs:** response `38335505849`, referee-copy `38335514323`; both completed successfully  
**Date:** 13 October 2026  
**Requested benchmark:** *Annals of Mathematics* / *Acta Mathematica* / *Inventiones Mathematicae* / *Journal of the AMS*  
**Status:** author-requested, AI-assisted referee-style assessment; not a commissioned journal report, an editorial decision, a formal proof certificate, or an independent human billiards, geometric-measure-theory, probability, o-minimal-geometry, or anisotropic-transfer-operator audit.

## 1. Recommendation

**Recommendation at the requested four-journal benchmark: reject in the present form.**

Revision 98 is a mathematically substantive response to the revision-97 report. It does not merely restate that report's residual-height obstruction. The three new modules introduce two genuinely new mechanisms.

First, the manuscript maps each regular physical state to the two endpoint momenta through the full gradient
\[
G(q)=\nabla_qF(q)=R(-p_0,p_m)
\]
and uses the uniformly positive endpoint Hessian to obtain a two-dimensional area formula for the complete optical insertion. This gives a quadratic small-gradient cap with an explicit weighted momentum-fiber multiplicity \(\mathcal K_m\). Combining that cap with the inherited \(b^{129/128}\) critical-volume estimate yields a finite-count first inverse-gradient layer cake integrated all the way to \(z=0\), with the complete finite-count error retained.

Second, the manuscript splits the revision-97 residual into a long near-critical component and a genuinely short physical-segment component. The long component is paid by a target-direction loss certificate and the new untruncated insertion. The short component is compared, on the same maximal physical segment, to the minimum of its two original weighted endpoint traces. The target selector is not differentiated and no artificial selector boundary is assigned a trace.

I find no decisive internal sign error, Jacobian reversal, exponent error, missing ramp or selector factor, illegal zero-cutoff exchange, or hidden physical-word multiplier in modules 235--237 at their stated scope. The normalization
\[
d\bar\nu=\frac{\omega}{4\pi c_*}\,dq,
\qquad
D_qG=K,
\]
does give the displayed pushforward density. The positive optical recursion controls each summand \(I_m\omega\) through internal grazing scales. The two-cap layer-cake exponent arithmetic is correct. The low capped clock supplies the claimed density drop on the critical component. The paired-trace comparison is compatible with the retained Borel segment bijection and with arbitrary Borel target selectors.

The recommendation nevertheless remains negative for a fundamental reason: the manuscript's pointwise theorem is still conditional on two independent unproved assertions.

The first is the new spectral-capacity condition
\[
\tag{SC}
m^6\mathcal K_m\theta_{B_*}^{\,2m}\longrightarrow0
\]
along an unbounded sequence of fixed auxiliary bands. Fixed-count definability proves only \(\mathcal K_m<\infty\) for each \(m\). It gives no collision-asymptotic growth rate. The manuscript correctly does not identify the stable-Jacobian pressure sums in the cited billiard literature with this endpoint-momentum-fiber multiplicity.

The second is decay of the positive paired short-trace height. Even under (SC), the final scalar reduction contains
\[
\mathcal H_M\!\left(T_{\mathsf S}^{\varepsilon(B)}\right),
\]
where \(T_{\mathsf S}\) is the minimum of two nonnegative physical endpoint traces on each selected short segment. No estimate forcing this quantity to zero is proved. It is not the Jordan positive part of the projected signed current, and it may retain precisely the nongrazing short-segment concentration capable of supporting a pointwise upper spike.

Thus revision 98 proves an important finite-count cap, a conditional critical-height theorem, and a complete paired-trace reduction. It does not prove the unrestricted upper pointwise half, the full exact-label raw local limit theorem, or the unrestricted downstream point-conditioned laws. At the requested benchmark, the central organizing theorem must be established rather than reduced to an unverified capacity condition and a second unestimated positive trace source.

## 2. Frozen source and chronology

Both reviewed author refs resolve to
\[
\texttt{3727d8bdcf7751f4aaec9b92cf9fa85be1ea0ce2},
\]
with tree
\[
\texttt{a08ac4da94bea08a23d9150f53a02d43ac71e459}.
\]

The active packet is
\[
\texttt{papers/A2-DYN-v98-referee-response}.
\]

The source manifest identifies revision 97 at
\[
\texttt{6dd3149985ff5f6aca9dce9e2c186589df309872},
\]
with frozen paper tree
\[
\texttt{dea215a65a5b3f3ff51d4448cce551abed75fd1d}.
\]

The revision-98 author commit descends directly from the controlling revision-97 review commit
\[
\texttt{5d0d67a3165bc4c97c3e468c91a87cd018b63109}.
\]

It preserves 234 inherited cores and adds exactly:

- `core/235_quadratic_gradient_cap_and_uncut_insertion.tex`;
- `core/236_disjoint_residuals_and_critical_height_certificate.tex`;
- `core/237_paired_physical_traces_and_scalar_reduction.tex`.

The comparison from the controlling review commit to the author commit contains one author commit. The revision is packaged in a new v98 directory and a new v98 qualification workflow. No preceding paper packet, review report, author branch, or historical source path is overwritten by the reviewed commit.

The source manifest and response also correct provenance identifiers that were stated differently in the frozen revision-97 report header. The frozen report remains unchanged. I use the source-pinned v98 identifiers above; this metadata correction has no bearing on the two unresolved mathematical conditions.

The present review branches start from the exact author SHA and add only this report under
`reviews/a2-dyn-v98-external-top4-review-2026-10-13/`.

## 3. Qualification evidence and its boundary

The exact-SHA workflow is
`.github/workflows/a2-dyn-v98-qualification.yml`.

At the final review freeze:

- run `38335505849` on `revision/a2-dyn-v98-referee-response-2026-10-13` completed with `success`;
- run `38335514323` on `revision/a2-dyn-v98-referee-copy-2026-10-13` completed with `success`.

The author commit reports a ten-page focused article, an 809-page archive, recorder coverage of all 237 cores, 7,380 new exact finite fixtures, and agreement between ordinary and optimized runs. The validation contract pins the preceding source and report, verifies inherited bytes and modes, builds the article and archive, checks recorder coverage, stabilizes references, and inspects page geometry.

This is useful and unusually careful source evidence. It establishes reproducible assembly, exact source identity, and the tested finite algebraic relations. It does not verify:

- the continuum endpoint-momentum area formula on every singular limiting configuration;
- the asymptotic growth of \(\mathcal K_m\);
- condition (SC);
- the inherited spectral estimates;
- the complete Borel/coarea disintegrations;
- the positive scalar remainder;
- decay of the paired short-trace height; or
- the unrestricted pointwise theorem.

The report therefore treats the successful workflows as qualification evidence, not as mathematical certification.

## 4. Scope of this audit

The complete archive contains 237 core modules. I have not independently reconstructed every historical spectral and geometric theorem. The substantive audit concentrates on:

1. the requests made in the revision-97 external report;
2. the exact endpoint-angle and endpoint-momentum conventions;
3. the Hessian and area-formula normalization;
4. the definition and fixed-count finiteness of \(\mathcal K_m\);
5. the positive optical recursion used to bound \(I_m\omega\);
6. the two-positive-cap layer cake down to zero gradient;
7. the precise exponent and limit order in the uncut insertion estimate;
8. the disjoint critical/short residual partition;
9. the low-clock density-loss certificate at the target roof;
10. target-direction multiplicity-one transport;
11. the two-ended physical trace comparison;
12. the role of grazing and critical endpoint traces;
13. arbitrary Borel target selectors;
14. the conditional scalar reduction and outer parameter schedule;
15. the logical status of (SC) and the paired trace;
16. source preservation and remote qualification; and
17. completeness and significance at the requested top-four standard.

The endpoint Hessian theorem, physical angular measure, optical recursion, inherited critical-volume estimate, maximal-segment Borel parametrization, per-sheet trace theorem, revision-97 running-compression reduction, and positive scalar remainder are treated as source-pinned inputs. I checked their interfaces with modules 235--237 but do not claim an independent re-proof of the entire historical chain.

## 5. What revision 98 adds

### 5.1. A physical two-dimensional gradient cap

On a regular word the manuscript uses endpoint angles
\[
q=(\alpha_0,\alpha_m),\qquad
G(q)=R(-p_0,p_m),\qquad
K=D_q^2F.
\]

The retained endpoint theorem gives
\[
\lambda_\circ I_2\le K\le\Lambda_\circ I_2.
\]
The physical area form is
\[
d\bar\nu=\frac{\omega}{4\pi c_*}\,dq.
\]

Consequently the pushforward of the complete optical insertion by \(G\) has density
\[
D_{m,R,n,k}(v)
=
\sum_{x\in\Pi^{\rm reg}:G(x)=v}
\frac{I_m(x)\omega(x)}
     {4\pi c_*\det K(x)}.
\]

The manuscript defines
\[
\mathcal K_m
=
1+\pi\sup_{R,n,k}
\operatorname*{ess\,sup}_{|v|<b_0}D_{m,R,n,k}(v).
\]

This gives, at every fixed count,
\[
\int_Ju_b(t)\,dt\le\mathcal K_m b^2,
\]
where \(u_b\) is the complete \(I_m\)-weighted source restricted to \(z=|G|<b\).

This is a genuine improvement over the preceding one-dimensional or positive-cutoff estimates. It controls the entire mass in a two-dimensional gradient disk and is independent of the roof interval \(J\).

### 5.2. Why the fixed-count cap is legitimate

The optical normalization is
\[
\omega=\frac{Rc_0c_m}{y_m},
\]
with the positive continuant recursion for \(y_m\). Positivity gives
\[
y_m
\ge
\tau_-\prod_{i=1}^{m-1}
\left(1+\frac{v_*}{c_i}\right),
\qquad
v_*=\frac{2\tau_-}{R_+}.
\]

Because
\[
I_m=1+\sum_{i=1}^{m-1}\frac{q_0^{d_i}}{c_i},
\qquad
\sum_iq_0^{d_i}\le\frac{2q_0}{1-q_0},
\]
each weighted summand \(I_m\omega\) stays uniformly bounded through internal grazing and in fact carries the displayed product decay. The lower Hessian bound controls \((\det K)^{-1}\).

At fixed \(m\), the finite-horizon physical graph has finitely many lifted itineraries, and the regular fibers of the local diffeomorphism \(G\) are finite in the relevant definable family. Thus \(\mathcal K_m<\infty\) at each count.

I regard this fixed-count conclusion as coherent. It is important, however, not to confuse it with an asymptotic estimate. The argument produces
\[
\mathcal K_m
\le
1+C N_m(1+v_*)^{-(m-1)}
\]
for a fixed-count fiber-cardinality bound \(N_m\). No bound on the growth of \(N_m\), and hence no useful collision-asymptotic bound on \(\mathcal K_m\), is proved.

### 5.3. The complete two-cap layer cake

Let
\[
w_b(t)\,dt
=
F_\#\!\left(I_mz^{-1}\mathbf1_{\{0<z<b\}}\bar\nu\right).
\]

For \(z>0\),
\[
z^{-1}\mathbf1_{\{z<b\}}
=
b^{-1}\mathbf1_{\{z<b\}}
+
\int_0^b v^{-2}\mathbf1_{\{z<v\}}\,dv.
\]

The inherited critical-volume estimate has a leading cap of order \(v^\alpha\), \(\alpha=129/128\), and a finite-count spectral remainder of order \(E v^{1/2}\). The new area formula supplies the second cap \(Hv^2\), with
\[
E=C_{B_*}(1+B_*|J|)m^2\theta_{B_*}^{m},
\qquad
H=m^2\mathcal K_m.
\]

The elementary bound
\[
b^{-1}\min(Eb^{1/2},Hb^2)
+
\int_0^b v^{-2}\min(Ev^{1/2},Hv^2)\,dv
\le
3\min\{Hb,E^{2/3}H^{1/3}\}
\]
is correct. It yields
\[
\begin{split}
m^2\int_Jw_b
\le{}&
C b^{1/128}(|J|+B_*^{-1})\\
&+
C\min\!\left\{
m^2\mathcal K_m b,\,
C_{B_*}^{2/3}(1+B_*|J|)^{2/3}
m^2(\mathcal K_m\theta_{B_*}^{2m})^{1/3}
\right\}.
\end{split}
\]

This is the central unconditional theorem of revision 98. It is a real finite-count zero-cutoff estimate. The previous square-root spectral remainder is not integrated to zero without a second cap.

The phrase “integrable to zero” should always be read as “integrable down to zero gradient at fixed count,” not as “the resulting charge vanishes.”

### 5.4. What condition (SC) actually supplies

If
\[
m^6\mathcal K_m\theta_{B_*}^{2m}\to0,
\]
then
\[
m^2(\mathcal K_m\theta_{B_*}^{2m})^{1/3}
=
(m^6\mathcal K_m\theta_{B_*}^{2m})^{1/3}
\to0.
\]

After taking the collision limit at each fixed auxiliary band and then enlarging an unbounded qualifying band sequence, the manuscript obtains
\[
\limsup_m\sup_{R,n,k}\sup_{|J|=L}
m^2\int_Jw_b
\le
CLb^{1/128}.
\]

Adding the fixed positive-gradient complement gives a collision-normalized fixed-width estimate for
\[
v^0(t)\,dt=F_\#(I_mz^{-1}\bar\nu).
\]

The deduction is correct conditional on (SC). The point is not a defect in the exponent arithmetic. The point is that (SC) is a new substantive dynamical theorem which is not proved.

Fixed-count definable finiteness cannot be used to infer (SC). Nor can one choose a collision-dependent \(b=b_m\) to exploit the first term \(m^2\mathcal K_mb\), because the pointwise theorem requires each geometric width to be fixed during the collision limit.

## 6. The critical residual

### 6.1. Disjoint partition

With
\[
d=2qr,
\]
the manuscript defines
\[
\mathsf S=Y\cap\{\ell\le3d\},
\qquad
\mathsf C=Y\cap\{\ell>3d\}.
\]

The overlap between short residence and near-critical support is assigned to \(\mathsf S\). This is a disjoint partition of the original revision-97 residual, not a replacement source.

For a target in \(\mathsf C\), the retained support information implies
\[
\tau^-\le2d,\qquad z<a,\qquad\tau^+>d.
\]
Thus the full forward interval \([0,d]\) lies in the original exact event.

### 6.2. The low-clock density loss

The capped clock satisfies \(c_r(x)<q\), and \(d=2qr\). If the physical angular density stayed at least one half of its target value throughout \([0,d]\), then this forward interval alone would contribute at least
\[
\frac{d}{2r}=q
\]
to the clock, a contradiction. Hence there is an \(s\in(0,d)\) with
\[
A(\Phi_sx)<\frac12A(x).
\]

Therefore
\[
\frac12A(x)
\le
\int_0^d|\partial_uA(\Phi_ux)|\,du
\le
C\int_0^d
A(\Phi_ux)\frac{I_m(\Phi_ux)}{z(\Phi_ux)}\,du.
\]

Radial growth gives
\[
z(\Phi_ux)<b,
\qquad
b=(a^2+2\Lambda_\circ d)^{1/2}.
\]

At every intermediate roof the same-event forward map is injective and the selected target ancestors form a subfamily of the original exact fiber. Thus
\[
\mathsf C^\varepsilon(t)
\le
C_0\int_t^{t+d}w_b(u)\,du.
\]

This is a target-height certificate, not an integral over starting roofs. I find the direction of transport and the clock arithmetic consistent.

### 6.3. Conditional critical height

Under (SC),
\[
\limsup_m\sup_{R,n,k}
m^2\|\mathsf C^\varepsilon\|_\infty
\le
Cd\,b^{1/128}.
\]

For
\[
q=\frac18,\qquad a=\sqrt{qr},\qquad d=2qr,
\]
one has \(b\asymp\sqrt{qr}\), hence
\[
d\,b^{1/128}
\asymp
(qr)^{257/256}.
\]

The exponent \(257/256\) is correct. Without (SC), the manuscript retains only the corresponding fixed-positive-gradient statement and the complete finite-count cutoff error. It does not claim unconditional critical recovery.

## 7. The short physical segments

### 7.1. Same-segment paired traces

For a maximal segment \(\sigma\), let
\[
f_\sigma^\varepsilon(u)
=
A_\sigma(u)W^\varepsilon(\Psi_\sigma(u)),
\]
and let \(f_\sigma^-\), \(f_\sigma^+\) be its two original one-sided endpoint traces.

For a Borel target selector \(H\) supported on segments of length at most \(\delta\), revision 98 defines
\[
T_H^\varepsilon(t)
=
\int_{\{a_\sigma<t<b_\sigma\}}
\mathbf1_H(\Psi_\sigma(t))
\min\{f_\sigma^-,f_\sigma^+\}\,d\sigma.
\]

The minimum is taken on the same physical segment. It is not moved through projection and is not identified with a Jordan positive part.

### 7.2. Complete comparison error

Since
\[
I_m\ge1,
\]
the retained angular-density and guard derivative bounds give
\[
|\partial_uf_\sigma^\varepsilon|
\le
C A_\sigma\frac{I_m}{z}
+
C\varepsilon^{-1}A_\sigma\frac1z
\le
C(1+\varepsilon^{-1})
A_\sigma\frac{I_m}{z}.
\]

For any interior point of the segment,
\[
\left|
f_\sigma^\varepsilon(u)
-
\min\{f_\sigma^-,f_\sigma^+\}
\right|
\le
\int_{a_\sigma}^{b_\sigma}
|\partial_vf_\sigma^\varepsilon(v)|\,dv.
\]

The target selector is held at the target roof. It is not differentiated. Because the segment length is at most \(\delta\), every joining interval lies inside \((t-\delta,t+\delta)\). The Borel maximal-segment parametrization counts every physical interior point once even with this target-dependent Borel selection. Thus
\[
|R_H^\varepsilon(t)-T_H^\varepsilon(t)|
\le
C(1+\varepsilon^{-1})
\int_{t-\delta}^{t+\delta}v^0(u)\,du.
\]

I regard this comparison as internally coherent, conditional only on the inherited segment and trace theorems.

### 7.3. Grazing and critical ends

If an internal incidence vanishes at either physical endpoint, the retained optical theorem gives zero weighted trace there. The minimum is then zero, and under (SC) the entire selected grazing-ended short source has height
\[
O((1+\varepsilon^{-1})\delta).
\]

A backward critical endpoint is different: its one-sided weighted trace need not vanish. Revision 98 preserves this distinction. It does not use zero original area to delete a directional critical trace.

### 7.4. The unresolved positive trace

For short segments whose two relevant endpoint traces are nonzero, the term
\[
T_{\mathsf S}^\varepsilon
\]
remains. It is nonnegative and is not controlled by the signed projected cancellation proved in earlier revisions.

No estimate of the form
\[
\mathcal H_M(T_{\mathsf S}^\varepsilon)
\le
C_M\varepsilon^{-Q}\delta^\beta,
\qquad \beta>0,
\]
or any comparable vanishing bound is proved.

This is not a merely expository omission. A family of very short nongrazing segments can carry small total roof mass while retaining large endpoint-trace height at exceptional roofs. The paired comparison shows exactly where such a concentration would live; it does not exclude it.

## 8. The conditional scalar reduction

Retain
\[
\varepsilon(B)=A_0B^{-1/12},
\qquad
q=\frac18,
\qquad
r=c\varepsilon(B)^4,
\qquad
a=\sqrt{qr},
\qquad
\delta=6qr.
\]

Under (SC), revision 98 proves
\[
\mathcal E_M
\le
\mathcal H_M(T_{\mathsf S}^{\varepsilon(B)})
+
C_MB^{-1/192}
+
C(qr)^{257/256}
+
C(1+\varepsilon(B)^{-1})qr.
\]

The scale arithmetic is correct:
\[
(qr)^{257/256}=O(\varepsilon^{257/64}),
\]
and
\[
(1+\varepsilon^{-1})qr=O(\varepsilon^3).
\]

All geometric widths and auxiliary bands are fixed before their collision limits, and the reconstruction parameter \(B\) is outermost. The limit order is therefore legal.

The theorem also gives, under (SC), an equivalence between the original scalar endpoint and decay of the paired trace along this schedule. This equivalence does not prove either assertion. It identifies the final positive short-segment obstruction once the spectral-capacity problem is solved.

## 9. Response to the revision-97 report

### 9.1. Residual essential height

**Substantially advanced, but not closed.**

The manuscript now has a complete finite-count inverse-gradient estimate down to \(z=0\), and it converts the long critical residual to the corresponding local insertion. The collision-normalized height conclusion requires the unverified condition (SC). The short paired trace remains unestimated.

### 9.2. Separation of mechanisms

**Addressed.**

The residual is split disjointly into long near-critical and genuinely short components. Their proofs use different geometric mechanisms, as requested.

### 9.3. Near-critical entrance and target capacity

**Advanced conditionally.**

The two-dimensional endpoint-momentum area formula and target-direction loss certificate are genuine new tools. They isolate the required transverse quantity as \(\mathcal K_m\). The necessary asymptotic capacity bound is not supplied.

### 9.4. Genuinely short residence

**Advanced to a complete comparison, but not closed.**

The manuscript compares the target source to both original physical endpoint traces on the same segment and pays the full comparison error by \(v^0\). Grazing-ended segments are conditionally controlled. Positive paired traces on nongrazing short segments remain.

### 9.5. Large height implies mass, capacity, or persistence

**Partly addressed.**

For the critical component, a large target density forces a definite density loss over a full forward interval and hence a local inverse-gradient volume cost. For the short component, the conclusion stops at a boundary trace rather than a vanishing capacity estimate.

### 9.6. Signed projection

**Handled correctly at the stated scope.**

Revision 98 does not replace the inherited projected signed forcing by an uncontrolled sum of positive sheetwise growth terms. The paired trace is explicitly a separate positive comparator, not a claimed signed cancellation.

### 9.7. Explicit scales and limit order

**Addressed.**

The \(q,r,a,\delta,\varepsilon(B)\) schedule and all exponents are stated explicitly. The auxiliary band and collision limits remain in the correct order.

### 9.8. Downstream laws

**Handled correctly.**

No unrestricted roof kernel, denominator, likelihood, entropy, path total variation, or arithmetic-zero-class conditional law is promoted.

### 9.9. Independent specialist verification

**Not supplied.**

Successful source qualification and finite fixtures do not replace independent reconstruction of the spectral chain, area formula, optical multiplicity, Borel disintegration, critical certificate, or paired-trace argument.

Revision 98 is therefore a serious and positive response to the preceding report, but it remains an incomplete response to the primary theorem request.

## 10. Exact theorem-bearing contribution of revision 98

Subject to the inherited inputs, I regard the following as the genuine contribution of this revision:

1. an endpoint-momentum area formula for the complete \(I_m\)-weighted physical source;
2. a quadratic small-gradient cap with explicit weighted fiber multiplicity \(\mathcal K_m\);
3. uniform control of each \(I_m\omega\) summand through every internal grazing scale;
4. fixed-count finiteness of the uncut \(I_m/z\) source;
5. a complete two-cap layer-cake estimate with the spectral error integrated down to zero gradient;
6. a disjoint decomposition of the revision-97 residual into critical and short physical mechanisms;
7. a target-height critical loss certificate with no positive initial-gradient cutoff;
8. the conditional critical height \(C(qr)^{257/256}\);
9. a complete two-ended original weighted trace comparison for arbitrary Borel target selectors;
10. conditional recovery of every grazing-ended short component;
11. an explicit conditional scalar reduction to the positive paired short trace; and
12. a precise identification of the new weighted multiplicity problem separate from the remaining short-trace problem.

These are not bookkeeping changes. They add new singular-transport geometry. Their present logical status, however, is conditional and reductive rather than a completed raw local limit theorem.

## 11. Claims that remain unproved

The manuscript correctly leaves unproved:

- condition (SC);
- any collision-asymptotic growth bound for \(\mathcal K_m\);
- an appropriate growth bound for the fiber cardinalities \(N_m\);
- a comparison between \(\mathcal K_m\) and an existing stable-Jacobian pressure sum;
- unconditional collision-normalized control of \(v^0\);
- unconditional critical-residual essential-height decay;
- positive paired short-trace height decay;
- full residual-height decay;
- unconditional upper-spike persistence;
- the upper pointwise half of the exact-label raw local limit;
- the unrestricted pointwise exact-label raw local limit theorem;
- unrestricted same-roof point-conditioned kernel convergence;
- forward essential-likelihood convergence;
- path-space total variation or relative entropy convergence;
- unrestricted normalization on zero arithmetic classes;
- independent human specialist approval; and
- a formal proof certificate.

The active publication-status and proof-ledger files represent these boundaries accurately.

## 12. What a successful next revision must prove

### 12.1. Prove or eliminate the spectral-capacity condition

The next revision must derive a collision-asymptotic estimate for the actual weighted momentum-fiber multiplicity. A sufficient statement is
\[
\limsup_{m\to\infty}\frac1m\log\mathcal K_m
<
-2\log\theta_{B_*}
\]
for an unbounded sequence of admissible fixed bands, with enough margin to absorb the polynomial factor \(m^6\).

One possible route is to quantify the number and weight of endpoint-momentum preimages by a pressure or transfer-operator theorem formulated for the same fibers and the same optical weight. A purely symbolic word count is not enough. If a stable-Jacobian pressure estimate is used, the manuscript must prove a comparison theorem from that partition sum to
\[
\sum_{G(x)=v}\frac{I_m(x)\omega(x)}{\det K(x)}
\]
uniformly in the exact labels and endpoint momentum \(v\).

Another possible route is a direct current or operator estimate which avoids \(\mathcal K_m\) altogether and controls the uncut inverse-gradient insertion in the needed pointwise topology.

Fixed-count o-minimal finiteness is not an acceptable substitute for either route.

### 12.2. Prove decay of the paired short trace

Independently of (SC), the next revision must control
\[
T_{\mathsf S}^\varepsilon(t)
=
\int_{\mathsf S(t)}
\min\{f_\sigma^-,f_\sigma^+\}\,d\sigma
\]
in normalized essential height.

A sufficient theorem would be
\[
\mathcal H_M(T_{\mathsf S}^\varepsilon)
\le
C_M\varepsilon^{-Q}\delta^\beta
\]
for some finite \(Q\) and \(\beta>0\), or an equivalent estimate that vanishes under the retained outer schedule.

Potential mechanisms include:

- a two-sided physical boundary-current estimate retaining cancellation before positive projection;
- a reversible first-entry/last-exit pairing on the same short segment;
- a Carleson or capacity estimate for short nongrazing endpoint traces;
- a theorem forcing one endpoint trace to be small whenever total residence is short;
- a transverse coarea estimate for the paired boundary map; or
- a direct projected estimate which proves that the positive minimum overcounts by a controllably small amount.

A bound for the integrated trace mass alone is insufficient. The theorem must exclude concentration at exceptional roofs.

### 12.3. Keep the two obligations separate

Proving (SC) closes the critical and comparison-error terms, but not the positive paired trace. Proving paired-trace decay without an uncut inverse-gradient estimate does not close the critical certificate. The final proof must state and discharge both obligations rather than combining them into an unnamed “capacity condition.”

### 12.4. Complete the scalar theorem with the retained schedule

Once both estimates are available, the manuscript should substitute them into
\[
\mathcal E_M
\le
\mathcal H_M(T_{\mathsf S}^{\varepsilon(B)})
+
C_MB^{-1/192}
+
C(qr)^{257/256}
+
C(1+\varepsilon^{-1})qr
\]
and verify every exponent with
\[
r=c\varepsilon(B)^4,\qquad q=\frac18,\qquad \delta=6qr.
\]

Only then should the upper pointwise theorem be marked proved and combined with the retained lower law.

### 12.5. Promote downstream laws only after scalar closure

No additional reciprocal, posterior, entropy, or path-space theorem can replace the missing scalar upper estimate. Downstream point-conditioned conclusions should remain at their currently proved finite-roof-norm scope until the scalar theorem is actually closed.

### 12.6. Obtain independent specialist verification

A submission of this breadth requires independent reconstruction of at least:

- the four-record spectral theorem and its finite-peak input;
- the endpoint Hessian and physical area normalization;
- the positive optical recurrence and \(I_m\omega\) estimate;
- the definable physical graph and fiber multiplicity;
- the Borel maximal-segment disintegration;
- the critical-volume and positive scalar inputs;
- the low-clock target certificate; and
- the paired physical trace theorem.

## 13. Exposition and architecture

The focused article is clearer than the complete archive and is commendably explicit about its conditional status. The following points should remain visible in any subsequent version.

1. Replace the phrase “integrable to zero” by “integrable down to zero gradient” wherever there is any risk of confusing integrability with vanishing.
2. State (SC) next to every result that uses it, not only in the source manifest.
3. Keep fixed-count finiteness of \(\mathcal K_m\) separate from collision-asymptotic capacity.
4. Display the complete finite-count error before every conditional collision-limit consequence.
5. Do not describe the stable-Jacobian pressure theorem as controlling \(\mathcal K_m\) without an explicit comparison.
6. Keep the paired endpoint minimum distinct from the Jordan positive part of a projected signed current.
7. Continue to distinguish a grazing trace, which vanishes, from a backward critical trace, which may not.
8. State that successful exact-SHA qualification verifies source identity and finite fixtures, not (SC) or the continuum theorems.
9. Keep provenance corrections separate from mathematical claims.
10. The principal theorem narrative should not require the reader to infer which of hundreds of archived statements are current claim authorities.

These are not substitutes for the two missing estimates, but they are important for a publishable presentation.

## 14. Significance and venue assessment

Revision 98 contains a stronger mathematical advance than a mere conditional reformulation. The endpoint-momentum area formula and the two-cap zero-gradient layer cake are potentially reusable tools for singular transport problems with a finite-count geometric cap and a separate spectral cap. The target-density loss certificate is a clean way to convert a low occupation clock into a local source cost. The same-segment paired-trace theorem also identifies the exact boundary object left by genuinely short physical residence.

If the weighted multiplicity estimate and paired-trace height theorem can both be proved and independently verified, the resulting pointwise inversion theorem could be a substantial contribution to dispersing billiards and local limit theory.

At the requested four-journal benchmark, however, the present paper remains incomplete in two independent directions. The first missing statement is a new global spectral-capacity theorem; the second is a pointwise boundary-trace deconcentration theorem. Neither follows from the finite fixtures or from fixed-count definability. Even granting the first, the second remains capable of carrying the full upper obstruction.

The completed results may already support a strong specialized article if reorganized around the unconditional finite-count cap and conditional transport architecture. That would be a different publication claim. The current manuscript retains the unrestricted pointwise raw local limit theorem as its governing objective, and that objective is not proved.

## 15. Final recommendation

Revision 98 responds seriously to the revision-97 report. It establishes a valid physical two-dimensional gradient cap, integrates the first inverse-gradient layer cake down to zero at fixed count with the complete error, separates the critical and short residual mechanisms, proves a target-direction critical certificate, and derives a complete two-ended physical trace comparison.

I found no decisive internal error in modules 235--237 at their stated finite-count and conditional scope, subject to the inherited inputs.

Nevertheless, condition (SC) is unverified, no collision-asymptotic bound for the weighted gradient multiplicity is proved, and the positive paired short-trace height is not shown to vanish. The full residual height, scalar upper endpoint, unrestricted pointwise exact-label raw local limit theorem, and downstream unrestricted laws therefore remain unproved.

**I recommend rejection in the present form at the requested Annals/Acta/Inventiones/JAMS benchmark.**
