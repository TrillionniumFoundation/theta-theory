# External top-four referee report on A2-DYN revision 109

**Manuscript:** Qian Qi, *Collision records, arithmetic, and raw local inversion in a triangular Lorentz gas*  
**Reviewed author branches:** `revision/a2-dyn-v109-capacity-abundance-referee-response-2026-10-14`, `revision/a2-dyn-v109-capacity-abundance-referee-copy-2026-10-14`  
**Reviewed author commit:** `ab0ad79b9c101b82c80e33511529588d101a45c0`  
**Reviewed repository tree:** `1d026f3ae6f122cfce8cbe2232dbbfd2ddb2ecaa`  
**Active manuscript directory:** `papers/A2-DYN-v109-referee-response`  
**Active mathematical source:** 261 numbered core modules in the complete packet; revision 109 adds modules 260--261  
**Initial revision-109 source-freeze parent:** `2fa6dbc6e5a7d6677996a3e557975800245617db`  
**Immediate mathematical baseline:** revision 108 author commit `2144665f89362ca80116f1999d99c80875833dcf`  
**Frozen revision-108 paper tree:** `e66a1dec484f419d88c05f12a7e2ec5310430448`  
**Controlling report:** `reviews/a2-dyn-v108-canonical-capacity-external-top4-review-2026-10-14/REFEREE_REPORT.md`  
**Controlling review commit / report blob:** `e863e8c110ffee472b3d10163a129a2bcfe9c0e1` / `5080564a78a192984acc272bc31c7ef8165bda4e`  
**Exact-SHA qualification at review freeze:** response run `38522526482`, queued; referee-copy run `38522538579`, queued  
**Date:** 14 October 2026  
**Requested benchmark:** *Annals of Mathematics* / *Acta Mathematica* / *Inventiones Mathematicae* / *Journal of the AMS*  
**Status:** author-requested, AI-assisted referee-style assessment; not a commissioned journal report, an editorial decision, a formal proof certificate, or an independent human billiards, geometric-measure-theory, probability, o-minimal-geometry, or anisotropic-transfer-operator audit.

## 1. Recommendation

**Recommendation at the requested four-journal benchmark: reject in the present form.**

Revision 109 is a genuine theorem-bearing response to the revision-108 report. It does not add another abstract certificate class and does not merely rename the canonical shortage. Instead, it derives new finite-itinerary optical geometry on the actual Lorentz trajectories, completes one-sided endpoint traces on the inherited physical pairing sheets, distinguishes visited grazing from tangency to an unvisited disk, and pays the complete comparison capacity of the visited-grazing class.

The main new conclusions are the following.

1. The broken-path action has the displayed positive second variation, and stationary elimination gives a uniformly positive reduced endpoint Hessian
   \[
   \lambda_\circ I_2\le D_q^2F\le \Lambda_\circ I_2,
   \qquad
   \lambda_\circ=\frac{9\sqrt{19}}{200},
   \quad
   \Lambda_\circ=\frac{47}{6}.
   \]

2. The endpoint-coordinate density has the exact optical representation
   \[
   \omega=|\partial_{p_0}\alpha_m|^{-1}
   =\frac{|G_{0m}|}{R}
   =\frac{Rc_0c_m}{\mathfrak b_m},
   \]
   where \(\mathfrak b_m\) is the positive \((1,2)\)-entry of the stated free-flight/reflection product.

3. With \(\varrho=47/59\), the manuscript obtains the per-trajectory bounds
   \[
   \omega\le \frac{47}{6}\varrho^{m-1},
   \qquad
   \frac{\omega}{c_j}\le \frac{2209}{72}\varrho^{m-2},
   \]
   and hence
   \[
   \omega I_m\le 500\varrho^{(m-2)_+}.
   \]

4. The Gauss-coordinate differential system gives integrability of \(1/z\) up to both physical ends of every positive-length regular pairing segment. A Schur-complement formula without inverse incidences extends the reduced Hessian continuously when visited incidences tend to zero.

5. The coarea density has finite one-sided endpoint traces and an integrable closed-segment variation bound. If an endpoint limiting trajectory contains an actually visited interior grazing collision, that endpoint trace vanishes and therefore the positive paired minimum on the whole segment is zero.

6. The manuscript correctly distinguishes this from tangency to an unvisited third disk. In the latter case the clearance guard may force \(W^\varepsilon=1\) while all visited incidences and the optical density remain positive, so the endpoint trace need not vanish.

7. The full fixed-window comparison pool can consequently be taken on the complete inherited positive-length physical pairing space. The original source on visited-grazing-ended sheets is zero, but their endpoint-maximum comparison capacity need not be zero. That complete capacity is paid by the original uncut optical volume.

8. If \(\mathsf R_B^{\rm full}\) is the canonical residual using the complete pool and \(\mathsf R_B^{\rm ng}\) is the residual after removing visited-grazing comparison capacity, then
   \[
   0\le \mathsf R_B^{\rm ng}-\mathsf R_B^{\rm full}
   \le K_BP_{r_B}^{\rm gr},
   \]
   and
   \[
   \mathcal H_M(\mathsf R_B^{\rm ng}-\mathsf R_B^{\rm full})
   \le C_MB^{-95/384}.
   \]

I audited the new article, its model and input statements, modules

- `core/260_optical_jacobi_and_endpoint_trace_completion.tex`;
- `core/261_grazing_capacity_payment_and_nongrazing_shortage.tex`;
- `comparison-scope.tex`;
- `RESPONSE_TO_REFEREE.md`;
- `PROOF_LEDGER.md`;
- `SOURCE_MANIFEST.json`;
- `PUBLICATION_STATUS.json`;
- `VALIDATION.md`;

and the controlling revision-108 report. Within the assumptions actually stated in those files, I found no decisive sign error in the second variation, no reversed optical product, no missing incidence factor in the marked estimate, no invalid positive-part subtraction, no exponent-arithmetic error, no hidden word-count factor, and no illegal exchange of the collision limit with the outer parameter.

The negative recommendation is nevertheless forced by the exact endpoint of the revision. The current final reduction is

\[
\mathcal E_M
\le
\mathcal H_M(\mathsf R_B^{\rm ng})
+C_MB^{-1/384},
\]

where

\[
\mathsf R_B^{\rm ng}(t)
=
\bigl(
\mathsf U_B^{\rm micro}(t)
-K_BP_{r_B}^{\rm ng}(t)
\bigr)_+.
\]

The manuscript proves that the unchanged exact-label raw pointwise assertion is equivalent to

\[
\mathcal H_M(\mathsf R_B^{\rm ng})\longrightarrow0
\qquad
\text{for every fixed }M.
\]

**No theorem establishes this limit.**

The remaining residual includes the full positive weight of the nongrazing microscopic source not paid by the available fixed-window capacity. It can still contain unvisited disk tangencies, nongrazing critical entrances, section-boundary cuts, shrinking flat or short-reach segments, and capacity-deficient sheets. Positivity of every visited endpoint incidence at each fixed collision count does not provide a collision-uniform lower incidence bound. The per-trajectory exponential optical estimate is not a summation theorem over physical trajectories or collision words.

Thus revision 109 completes a real physical component of the scarcity problem, but it does not prove capacity abundance on the remaining physical source. The residual is still the upper pointwise obstruction itself, not a secondary error after the main theorem.

At the requested four-journal benchmark, this is insufficient for acceptance. The new optical and endpoint-trace analysis is technically meaningful, but the paper continues to be organized around a raw pointwise local limit theorem which remains unproved. Nor, in its present specialized form, does the visited-grazing payment constitute a separate theorem of top-four breadth independent of that unfinished endpoint.

## 2. Frozen source and revision chronology

The two reviewed author branches both resolve to

`ab0ad79b9c101b82c80e33511529588d101a45c0`.

The repository tree is

`1d026f3ae6f122cfce8cbe2232dbbfd2ddb2ecaa`.

The active article is

`papers/A2-DYN-v109-referee-response/main.tex`.

The complete revision-108 packet is preserved under

`papers/A2-DYN-v109-referee-response/archive/v108`.

The theorem-bearing revision-109 commit descends from the initial source-freeze commit

`2fa6dbc6e5a7d6677996a3e557975800245617db`.

That initial commit did not contain the present mathematical revision. The theorem-bearing author commit adds the standalone article, modules 260--261, active status and validation files, proof diagnostics, and the exact-checkout build protocol.

The controlling revision-108 review commit is

`e863e8c110ffee472b3d10163a129a2bcfe9c0e1`.

Its report blob is

`5080564a78a192984acc272bc31c7ef8165bda4e`.

The reviewed revision-108 author commit is

`2144665f89362ca80116f1999d99c80875833dcf`.

The revision-109 source manifest declares 259 historical modules and two new modules, for a total of 261 in the complete packet. It accurately keeps the following claims false:

- nongrazing residual-height decay;
- canonical residual-height decay;
- the full raw-return local limit theorem;
- closure of the primary referee request;
- a collision-uniform logarithmic insertion;
- independent reconstruction of the global pairing construction;
- independent human review; and
- formal proof certification.

The present review branch starts directly from the exact author commit and adds only this report under

`reviews/a2-dyn-v109-capacity-abundance-external-top4-review-2026-10-14/`.

No author manuscript, author ref, workflow, prior report, historical paper tree, or unrelated repository path is intentionally modified.

## 3. Qualification evidence and its boundary

The dedicated workflow is

`.github/workflows/a2-dyn-v109-source-and-manuscript.yml`.

At the freeze of this report, the exact-SHA runs for the theorem-bearing manuscript were:

- response branch run `38522526482`: `queued`, conclusion `null`;
- referee-copy branch run `38522538579`: `queued`, conclusion `null`.

I therefore do not describe revision 109 as remotely qualified at the review freeze.

The active validation record reports a successful local standalone build of the 12-page current article, stable references, rendered-page inspection, and matching normal/optimized diagnostics. The finite diagnostics cover optical continuants, Schur complements, continuous grazing limits, and positive-part residual inequalities. These are useful implementation checks.

The remote workflow is designed to verify:

1. the exact author SHA and branch ref;
2. the frozen controlling report blob;
3. the original revision-108 packet tree;
4. the exact archived copy of the historical packet;
5. source and claim preservation;
6. normal and optimized numerical diagnostics;
7. native compilation of the current article;
8. native compilation of the complete historical article and supplement;
9. reference stabilization and TeX-log auditing;
10. recorder coverage of all 261 modules; and
11. upload of exact-SHA sources, PDFs, logs, rendered pages, and evidence.

These checks are meaningful source and reproducibility evidence. Even a later successful workflow would not certify:

1. the inherited incident-component pairing-space construction;
2. the one-copy physical multiplicity convention;
3. the common coarea versions over the full exact-label family;
4. the inherited regular-point weighted variation estimate;
5. the fixed-window spectral and pressure averages;
6. the collision-uniform abundance of nongrazing comparison capacity;
7. the global summation of per-trajectory optical estimates;
8. decay of \(\mathsf R_B^{\rm ng}\); or
9. the full exact-label raw pointwise local limit theorem.

The manuscript and active validation summary correctly distinguish software qualification from mathematical certification.

## 4. Scope of this review

The substantive audit concentrates on:

1. the endpoint section cap;
2. the broken-path second variation;
3. stationary elimination and the endpoint Schur complement;
4. the exact optical denominator;
5. the marked single-incidence estimate;
6. the full inherited insertion \(\omega I_m\);
7. the fixed-angle Gauss-coordinate differential equations;
8. integrability of the inverse gradient;
9. the continuous Schur-complement formula at visited grazing;
10. existence of finite one-sided trajectories and clearances;
11. the coarea determinant and trace completion;
12. the closed-segment variation and one-half-Hölder estimate;
13. the distinction between visited grazing and unvisited tangency;
14. the full physical comparison pool;
15. the visited-grazing source/capacity partition;
16. the residual positive-part comparison;
17. the outer exponent arithmetic;
18. the final scalar equivalence; and
19. the precise remaining physical estimate.

The first 259 modules, the original pairing construction, the spectral peak theorem, the pressure estimates, the complete coarea identification, and the earlier scalar reduction are treated as source-pinned inherited inputs. This report does not independently re-prove the complete historical chain.

## 5. The inherited obstruction from revision 108

Revision 108 constructed, at each target roof, the complete admissible fixed-window comparison pool on the then-verified comparison space. It defined

\[
P_r(t)=\int Q_r(t,\theta)p_\vee(\theta)\,d\theta
\]

and allocated the original microscopic source by

\[
V_{r,K}(t)=\min\{U(t),KP_r(t)\},
\qquad
R_{r,K}(t)=(U(t)-KP_r(t))_+.
\]

That construction solved the measurable-selection and overlap problem within its declared scalar certificate class. It did not prove that the pool had enough capacity, uniformly in collision count, to pay the microscopic source.

The revision-108 report therefore asked for a genuine Lorentz-specific scarcity or capacity-abundance theorem in the required limit order. It also identified endpoint-trace completion, singular extensions, and the distinction between source weight and comparison capacity as load-bearing physical issues.

Revision 109 responds to those points in the correct direction. It does not infer abundance from finite-count exhaustion. It proves a physical endpoint theorem and removes one entire physical class from the unresolved capacity question.

## 6. Endpoint section cap

The section test is uniformly separated from grazing at the initial and terminal collisions. The only section centers with tangential coordinate exceeding \(1/2\) in magnitude have coordinate

\[
\frac{2q_R}{1+q_R^2},
\qquad
q_R<\frac{53}{100}.
\]

The manuscript verifies

\[
\frac{2(53/100)}{1+(53/100)^2}+rac1{200}<rac9{10}.
\]

Hence on the closure of the original section tests

\[
|p_0|,|p_m|\le\frac9{10},
\qquad
c_0,c_m\ge\frac{\sqrt{19}}{10}.
\]

This is a direct geometric estimate and supplies a genuine uniform endpoint lower incidence without introducing an interior incidence cutoff.

I found no numerical or logical error in this step.

## 7. Second variation and reduced endpoint Hessian

For an actual fixed collision itinerary, the manuscript writes

\[
D^2S[\xi,\xi]
=
R\left(c_0\xi_0^2+c_m\xi_m^2
+2\sum_{i=1}^{m-1}c_i\xi_i^2\right)
+
R^2\sum_{i=0}^{m-1}
\frac{(c_i\xi_i+c_{i+1}\xi_{i+1})^2}{\tau_i}.
\]

The signs are consistent with the chosen actual orientation of the circular boundaries and the specular relations at departure and arrival. Every displayed term is nonnegative.

Letting \(H=D^2S\), eliminating the stationary interior variables gives

\[
G
=H_{EE}-H_{EI}H_{II}^{-1}H_{IE},
\]

and the variational characterization

\[
\eta^{\mathsf T}G\eta
=
\min_\zeta
(\eta,\zeta)^{\mathsf T}H(\eta,\zeta).
\]

The explicit endpoint diagonal terms yield

\[
G\ge R\operatorname{diag}(c_0,c_m).
\]

The endpoint section cap then gives the uniform lower bound. Choosing zero interior variation gives the upper bound by the endpoint block. The constant \(47/6\) is conservative but compatible with

\[
R_++\frac{2R_+^2}{\tau_-}=rac{47}{6}.
\]

I found no decisive defect in this reduction. A specialist should nevertheless check the boundary-orientation convention and the second derivative of each flight directly, because all later sign and positivity statements depend on this formula.

## 8. Exact optical denominator and marked incidence

The manuscript introduces

\[
\mathsf S(s)=
\begin{pmatrix}1&s\\0&1\end{pmatrix},
\qquad
\mathsf C(\kappa)=
\begin{pmatrix}1&0\\\kappa&1\end{pmatrix},
\qquad
\kappa_i=\frac{2}{Rc_i},
\]

and

\[
\mathsf M_m
=
\mathsf S(\tau_{m-1})\mathsf C(\kappa_{m-1})
\cdots
\mathsf S(\tau_1)\mathsf C(\kappa_1)
\mathsf S(\tau_0).
\]

The exact identity

\[
\mathfrak b_m=(\mathsf M_m)_{12}
=\prod_i\tau_i\det J
\]

is consistent with the tridiagonal continuant obtained from the interior Hessian. It gives

\[
\omega
=|\partial_{p_0}\alpha_m|^{-1}
=rac{|G_{0m}|}{R}
=rac{Rc_0c_m}{\mathfrak b_m}.
\]

All matrix entries are nonnegative. Each interior reflection increases the top component of a positive second column by at least the factor

\[
1+\frac{2\tau_-}{R_+}=rac{59}{47}.
\]

This yields

\[
\mathfrak b_m\ge\tau_-\left(\frac{59}{47}\right)^{m-1}
\]

and therefore the first optical bound.

For a marked collision \(j\), the coefficient of \(\kappa_j\) splits into positive left and right continuants. The resulting estimate

\[
\mathfrak b_m
\ge
\kappa_j\tau_-^2\left(\frac{59}{47}\right)^{m-2}
\]

implies

\[
\frac{\omega}{c_j}
\le
\frac{R_+^2}{2\tau_-^2}
\left(\frac{47}{59}\right)^{m-2}
=
\frac{2209}{72}
\left(\frac{47}{59}\right)^{m-2}.
\]

The summation

\[
\sum_{j=1}^{m-1}q_0^{d_j}
\le
\frac{2q_0}{1-q_0}
=rac{47}{3}
\]

then gives the stated bound

\[
\omega I_m\le500\varrho^{(m-2)_+}.
\]

I found the constants and exponent arithmetic consistent. The manuscript also makes the essential restraint explicit: this is a per-trajectory estimate, not a theorem controlling the sum over all collision words or physical sheets. That restraint is mathematically necessary.

## 9. Fixed-angle Gauss coordinates and inverse-gradient integrability

On a constant-angle pairing segment,

\[
\nabla F(q)=ze,
\]

so differentiating in \(z\) gives

\[
\frac{dq}{dz}=G^{-1}e,
\qquad
\frac{du}{dz}=z e^{\mathsf T}G^{-1}e.
\]

The Hessian bounds imply

\[
2\lambda_\circ
\le
\frac{d(z^2)}{du}
\le
2\Lambda_\circ.
\]

Thus \(z\) is strictly increasing with the roof coordinate, the endpoint limits of \(q\) exist in a chosen angular lift, and

\[
\int_a^b\frac{du}{z}
\le
\lambda_\circ^{-1}(z_b-z_a)
\le
\lambda_\circ^{-1}
\min\left\{
\sqrt2R_+,
\sqrt{2\Lambda_\circ(b-a)}
\right\}.
\]

This correctly shows that a critical endpoint of a positive-length segment can occur only at the incoming end.

The derivation is short but coherent. It is one of the strongest additions in revision 109 because it provides the endpoint integrability actually needed by the inherited weighted variation inequality.

## 10. Continuous Schur complement at visited grazing

The interior Hessian can be factored through

\[
Z=2I+RC_I^{1/2}L_{II}C_I^{1/2}\ge2I.
\]

The reduced Hessian becomes

\[
\begin{aligned}
G={}&RC_E+R^2C_EL_{EE}C_E\\
&-R^3C_EL_{EI}C_I^{1/2}Z^{-1}
C_I^{1/2}L_{IE}C_E.
\end{aligned}
\]

This formula contains no inverse power of an interior incidence. Since \(Z^{-1}\) stays uniformly bounded, it extends continuously when one or several visited incidences tend to zero. The order bounds pass to the limit.

The marked optical estimate further gives \(G_{0m}\to0\) if at least one visited interior incidence tends to zero.

I found this argument internally consistent. It avoids the common error of trying to pass to grazing through a formula containing \(C_I^{-1}\). Independent specialist reconstruction should verify the matrix factorization and the correspondence between the limiting fixed itinerary and the relevant physical endpoint.

## 11. Existence of endpoint trajectories and clearances

The manuscript argues one-sidedly from the actual event. The endpoint initial angle and momentum converge. For each designated next disk, the flight quadratic has a continuous entry root up to tangency; the positive finite-horizon flight lower bound prevents collapse. Specular reflection is continuous at tangency. Induction over the finite itinerary therefore gives limits for all visited collision points, velocities, flight lengths, and incidences.

Third-disk clearances also have limits because only finitely many lattice disks can approach a finite-horizon flight and the distance to each is continuous.

This is a plausible and economical endpoint argument. It does not continue a forbidden itinerary past a physical boundary. The most delicate cases are simultaneous endpoint events: a visited grazing together with a third-disk tangency, a section boundary, or another itinerary boundary. The one-sided nature of the construction appears sufficient, but this is a point that should be checked by a human billiards specialist against the precise inherited definition of maximal physical pairing segments.

## 12. Coarea trace completion

The coarea determinant is

\[
\chi
=
\det D_q(F,\arg\nabla F)
=
e^{\perp\mathsf T}Ge^\perp
\ge\lambda_\circ.
\]

Thus

\[
f^\varepsilon
=
\frac{\omega W^\varepsilon}{4\pi c_*\chi}
\]

has finite one-sided limits once the finite trajectory, \(G\), \(\omega\), and the guard variables have one-sided limits.

The inherited regular-point inequality is

\[
|\partial_u f^\varepsilon|
\le
C(1+\varepsilon^{-1})AI_m/z.
\]

The new marked optical estimate bounds \(AI_m\) uniformly on each finite trajectory by a constant times \(\varrho^{(m-2)_+}\), while the Gauss-coordinate lemma makes \(1/z\) integrable. Consequently the derivative has an integrable majorant on the closed segment.

Local absolute continuity on compact regular subsegments, the proved endpoint limits, and the integrable derivative bound yield the closed-segment estimate

\[
|f^\varepsilon(b-)-f^\varepsilon(a+)|
\le
C(1+\varepsilon^{-1})
\int_a^b AI_m/z\,du.
\]

The same calculation gives the one-half-Hölder estimate

\[
|f^\varepsilon(v)-f^\varepsilon(u)|
\le
C(1+\varepsilon^{-1})
\varrho^{(m-2)_+}|v-u|^{1/2}.
\]

Within the inherited regular-point derivative input, this endpoint passage is coherent. It is not an independent reconstruction of the global pairing model or of the regular-point derivative estimate, and the article accurately says so.

## 13. Visited grazing and unvisited tangency

This distinction is essential and is handled correctly in the new text.

If a limiting trajectory contains an actually visited interior grazing collision, then some \(c_j\to0\). The marked estimate gives

\[
\omega\le Cc_j\varrho^{m-2}\longrightarrow0.
\]

Since \(W^\varepsilon\le1\) and \(\chi\ge\lambda_\circ\), the corresponding endpoint trace is zero. The paired density on the whole segment is the minimum of the two endpoint traces, so it is identically zero on that segment.

This conclusion is not based on declaring the grazing set measure zero. It is a pointwise statement about the original positive endpoint minimum.

By contrast, tangency of a flight to an unvisited third disk makes the relevant clearance zero and can force \(W^\varepsilon=1\), but it need not make any visited incidence vanish. The optical density can therefore stay positive. These sheets must remain in the source, and revision 109 retains them.

The report agrees with this distinction.

## 14. The full physical comparison pool

Revision 109 now takes

\[
\Theta_{\rm ad}=\Theta_{\rm phys}
\]

for all positive-length maximal regular pairing segments of the original exact event. The endpoint trace theorem supplies the previously missing finite traces and variation inequality on this inherited pairing space.

For fixed \(0<r<\Delta\), the deterministic orientation rule defines a Borel pool indicator \(Q_r\le1\). With

\[
P_r=D_r+E_r,
\]

the paired-minimum part satisfies

\[
D_r(t)
\le
\frac1r
\int_{t-r}^{t+r}
\mathsf T_\Delta^\varepsilon(u)\,du.
\]

The endpoint-difference part satisfies

\[
E_r(t)
\le
C(1+\varepsilon^{-1})
\int_{t-\Delta}^{t+\Delta}v^0(u)\,du.
\]

Hence

\[
P_r(t)
\le
\frac1r
\int_{t-r}^{t+r}
\mathsf T_\Delta^\varepsilon(u)\,du
+
C(1+\varepsilon^{-1})
\int_{t-\Delta}^{t+\Delta}v^0(u)\,du.
\]

This is the same finite-count capacity estimate as in revision 108, now on the complete inherited positive-length comparison space rather than a space restricted by unverified endpoint traces.

The conclusion remains conditional on the inherited global Borel pairing construction, one-copy multiplicity convention, common coarea versions, and averaged analytic estimates. Revision 109 has completed the local endpoint regularity needed to use those inputs; it has not independently re-proved the global inputs.

## 15. Zero grazing source and paid grazing capacity

Let \(\Gamma\) be the set of pairing segments whose limiting finite itinerary has a visited interior incidence equal to zero at at least one endpoint. The endpoint incidence limits are Borel, so \(\Gamma\) is Borel.

On \(\Gamma\),

\[
c^\varepsilon=0.
\]

Thus every original selected paired source on \(\Gamma\) is exactly zero at finite count.

However,

\[
p_\vee=e_\partial
\]

on this class, and the comparison capacity need not vanish. The completed variation estimate yields

\[
P_r^{\rm gr}(t)
\le
C(1+\varepsilon^{-1})
\int_{t-\Delta}^{t+\Delta}v^0(u)\,du.
\]

After the complete one-copy physical sum and the inherited fixed-window volume estimate,

\[
\mathcal H_M(KP_r^{\rm gr})
\le
CK(1+\varepsilon^{-1})\Delta.
\]

This is a genuine physical payment of the entire visited-grazing comparison capacity. It neither deletes that capacity nor confuses zero source weight with zero endpoint envelope.

## 16. Residual comparison and exponent audit

Revision 109 chooses

\[
h_B=\frac{\delta(B)}2,
\qquad
r_B=\frac{\delta(B)}8,
\qquad
\Delta_B=8\delta(B),
\qquad
K_B=\max\{1,\varepsilon(B)^{-1/32}\}.
\]

All of these quantities are fixed from the outer parameter before the collision limit.

Since

\[
P_{r_B}=P_{r_B}^{\rm ng}+P_{r_B}^{\rm gr},
\]

the elementary positive-part inequality gives

\[
0
\le
\mathsf R_B^{\rm ng}-\mathsf R_B^{\rm full}
\le
K_BP_{r_B}^{\rm gr}.
\]

With \(\Delta_B=O(\varepsilon^4)\) and \(K_B=O(\varepsilon^{-1/32})\),

\[
K_B(1+\varepsilon^{-1})\Delta_B
=O(\varepsilon^{95/32}).
\]

Because \(\varepsilon(B)=A_0B^{-1/12}\), this becomes

\[
O(B^{-95/384}).
\]

The exponent arithmetic is correct.

The accepted complete-pool source has height

\[
O\left(
\varepsilon^{-1/32}
\{\varepsilon^{1/16}+O(\varepsilon^3)\}
\right)
=O(\varepsilon^{1/32})
=O(B^{-1/384}).
\]

Substitution into the inherited scalar reduction gives

\[
\mathcal E_M
\le
\mathcal H_M(\mathsf R_B^{\rm ng})
+C_MB^{-1/384}.
\]

I found no defect in this positive decomposition or its order of limits.

## 17. The exact remaining obstruction

The remaining estimate is

\[
\lim_{B\to\infty}
\limsup_{m\to\infty}
\sup_{R,n,k}
 m^2
\esssup_{t\in\mathcal C_{m,R,n,k}(M)}
\bigl(
\mathsf U_{B,m}^{\rm micro}(t)
-K_BP_{r_B,m}^{\rm ng}(t)
\bigr)_+
=0.
\]

Revision 109 does not prove this estimate.

The unresolved nongrazing class can contain:

- unvisited third-disk tangencies;
- nongrazing critical incoming endpoints;
- section-boundary cuts with positive traces;
- shrinking flat segments;
- true short-reach segments;
- pairs with positive but collision-count-dependent small incidences;
- sources whose available fixed-window endpoint envelope is deficient;
- physical configurations for which the inherited average bounds do not yield the required pointwise abundance.

At each fixed collision count, all visited endpoint incidences on this class are positive. Their infimum may nevertheless tend to zero with the count. No uniform lower incidence follows.

The per-trajectory bound

\[
\omega I_m\le500\varrho^{(m-2)_+}
\]

cannot simply be summed over collision words. No weighted complexity or pressure theorem for this new use is proved in revision 109. The manuscript correctly refuses to make that inference.

The finite-count fact that every positive-length segment contains a sufficiently small window is also insufficient, because \(r_B\) must be fixed before the collision limsup.

Therefore the governing raw pointwise theorem remains open within the manuscript.

## 18. Top-four significance

The optical and endpoint-trace calculations are nontrivial and useful. In particular, the continuous Schur-complement formula and the exact distinction between visited grazing and unvisited tangency clarify a genuine technical obstruction in the preceding revisions.

Nevertheless, the requested benchmark is not met.

First, the paper's organizing theorem remains unproved. The final residual limit is explicitly equivalent to the desired upper pointwise law.

Second, the new theorem removes one physical component whose original paired source is already zero, although its comparison capacity must be paid. This is important for the correctness of the canonical allocation, but it does not yet control the positive nongrazing source which carries the remaining theorem.

Third, the result remains highly specialized to one finite-horizon triangular Lorentz family, one section, one guard, one exact-label event, and a long inherited analytic pipeline. Revision 109 does not extract a general theorem about endpoint traces or capacity scarcity for a broad class of singular hyperbolic systems.

Fourth, the continuum proof chain still relies on 259 inherited modules and several load-bearing inputs which have not received an independent human specialist audit.

Accordingly, the new material strengthens the project but does not justify publication in *Annals*, *Acta*, *Inventiones*, or *JAMS* in its present form.

## 19. Major mathematical requirements for a further revision

A further revision capable of changing the recommendation must do at least one of the following.

### Route A: prove nongrazing capacity abundance

Prove directly, in the prescribed order of limits,

\[
\mathcal H_M
\left(
(\mathsf U_B^{\rm micro}-K_BP_{r_B}^{\rm ng})_+
\right)
\longrightarrow0.
\]

This requires a physical theorem showing that the complete nongrazing pool has sufficient fixed-window capacity after the full physical sum, uniformly in collision count, radius, and exact labels.

### Route B: prove a genuine microscopic insertion

Establish a collision-uniform inverse-residence or logarithmic insertion on the original microscopic source, with constants independent of \(B,m,R,n,k\), strong enough to force its ordered essential height to vanish.

The earlier conditional criteria are not substitutes for this estimate.

### Route C: decompose and pay every nongrazing class

Give an exhaustive Borel classification of the remaining nongrazing microscopic source and prove a summable pointwise-height bound for each class. This must include unvisited tangencies, nongrazing critical endpoints, section cuts, flat or short-reach segments, and capacity-deficient families.

A list of local certificates is insufficient unless their complements are proved small in the target essential-height topology.

### Route D: prove a new weighted-complexity theorem

If the per-trajectory exponential optical estimate is intended to control the remaining source, prove a physical weighted-summation or pressure theorem which compensates for collision-word growth and remains compatible with the exact labels and target roof.

The present manuscript explicitly does not contain such a theorem.

## 20. Specialist audit targets

Before any positive publication recommendation, an independent billiards and transfer-operator audit should reconstruct at least the following points.

1. The sign and endpoint convention in the second variation of the broken-path action.
2. The exact relation between the endpoint Hessian mixed entry and \(|\partial_{p_0}\alpha_m|^{-1}\).
3. The continuant identity \(\mathfrak b_m=\prod_i\tau_i\det J\).
4. The marked factorization at a chosen interior collision.
5. Uniformity of the constants in the radius interval.
6. The continuous Schur-complement formula with multiple simultaneous visited grazings.
7. One-sided endpoint limits at simultaneous physical boundaries.
8. Local absolute continuity of the guard and clearance minimum on regular subsegments.
9. Passage from the inherited regular derivative inequality to closed-segment absolute continuity.
10. The global Borel incident-component pairing construction.
11. Multiplicity one in the physical coarea sum.
12. Common roof versions for all positive restrictions at fixed exact labels.
13. The full-pool Borel partition and the visited-grazing class \(\Gamma\).
14. The identification of the complete grazing capacity with the original uncut volume payment.
15. The historical necessity direction used to claim equivalence with the raw pointwise theorem.
16. The inherited spectral/pressure averages and their stated width independence.

Software diagnostics cannot certify these continuum assertions.

## 21. Requested clarifications and presentation revisions

The current exposition is substantially clearer than the accumulated shell used in revision 108. I nevertheless recommend the following changes in any further submission.

1. State in the introduction, before the main positive results, the exact residual limit which remains unproved.
2. Avoid using “capacity abundance” without the qualifier “visited-grazing component” in prose, since abundance on the nongrazing source is the missing theorem.
3. Keep the distinction between zero original source and nonzero comparison capacity prominent.
4. State explicitly whether the constant in the one-half-Hölder estimate is uniform over all fixed-count sheets and which inherited constants it uses.
5. Add a short matrix derivation of the corner cofactor identity, rather than referring only to successive determinant expansion.
6. State the one-sided endpoint-limit lemma separately for simultaneous boundary mechanisms.
7. Explain explicitly that \(\Gamma\) can include several grazing incidences and that the proof remains unchanged.
8. Preserve the statement that unvisited third-disk tangencies are retained with their original positive weight.
9. Keep the scalar roofwise allocation distinguished from an individual-sheet coupling.
10. Update the active validation record only from actual completed exact-SHA runs; do not infer success from the workflow definition.
11. Continue to preserve the controlling report's freeze-time CI status even if the jobs later succeed.
12. Do not promote denominator, likelihood, or unrestricted conditional-law conclusions before the scalar residual is closed.

## 22. What revision 109 has resolved

For clarity, the following objections from the preceding report have been materially advanced or resolved within the stated inputs.

- The comparison space is no longer restricted by an unspecified endpoint-trace exclusion.
- The finite one-sided endpoint traces are proved on the inherited positive-length pairing segments.
- The weighted endpoint variation has an integrable passage to the physical ends.
- The optical density at visited grazing is controlled without an incidence cutoff.
- The difference between visited grazing and unvisited tangency is stated correctly.
- The original source on visited-grazing-ended segments is proved exactly zero.
- The full comparison capacity of those segments is retained and paid.
- The full-versus-nongrazing residual difference has a quantitative ordered-height bound.
- The quantifier order is kept explicit.
- The manuscript does not misrepresent finite-count exhaustion or per-trajectory decay as the remaining theorem.

These are substantial improvements.

## 23. What revision 109 has not resolved

The following central matters remain open in the manuscript.

- Decay of the nongrazing canonical residual.
- Decay of the complete canonical residual.
- The full raw-return pointwise local limit theorem.
- A collision-uniform microscopic logarithmic or inverse-residence insertion.
- A weighted summation theorem for the new optical estimate.
- A complete physical scarcity theorem for unvisited tangencies, critical ends, section cuts, flat sheets, and short-reach sheets.
- An independent reconstruction of the global pairing and coarea model.
- Independent human specialist verification.
- Formal proof certification.

The source manifest and publication-status file record these boundaries accurately.

## 24. Final recommendation

Revision 109 makes genuine and technically credible progress. Within its stated inherited inputs, I found no decisive error in the new optical denominator, marked-incidence estimate, Gauss-coordinate integrability, continuous Schur complement, endpoint trace completion, visited-grazing source identity, grazing-capacity payment, or residual exponent calculation.

The revision nevertheless leaves the exact remaining theorem as

\[
\mathcal H_M(\mathsf R_B^{\rm ng})\to0,
\]

and proves no estimate implying it. The paper's principal raw pointwise local limit theorem is therefore still unproved.

**Recommendation at the requested top-four mathematics benchmark: reject in the present form.**

A materially different assessment would require a collision-uniform theorem closing the nongrazing microscopic shortage, or a new general theorem of independent top-four scope whose validity and significance do not depend on that unfinished endpoint.
