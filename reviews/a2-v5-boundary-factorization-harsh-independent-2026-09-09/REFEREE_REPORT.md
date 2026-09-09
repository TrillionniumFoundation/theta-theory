# Independent referee report: A2 v5 — relative boundary factorization

## Recommendation: reject at the requested top-four mathematics-journal level in its present form

**Date:** September 9, 2026 (Asia/Singapore).  
**Reviewer:** GPT-6 Astra Pro. This is an independent AI-assisted assessment requested by the repository owner, not a journal-commissioned report or an actual editorial decision.  
**Author:** Qian Qi.  
**Manuscript:** *Relative boundary factorization and collision thresholds in periodic dispersing billiards*.  
**Repository:** `TrillionniumFoundation/theta-theory`.  
**Reviewed branch:** `revision/a2-v5-boundary-factorization-pairwise-recovery-2026-09-09`.  
**Frozen manuscript commit:** `ee879236d0fae1f84c685bef4ff27326403d4b2d`.  
**Frozen tree:** `2eb4741cfe031839d447bc74939bf0975379ac8f`.  
**Manuscript commit time:** September 9, 2026, 03:00:33 UTC, or 11:00:33 Singapore time.  
**Controlling previous review:** `ec861ecfcdd83a81880c1a9082becc19b0c76977`, reviewing manuscript `68bbf5b841a66dcc2b85f4d76ce66b1ae8b9782f`.  
**New review branch:** `review/a2-v5-boundary-factorization-harsh-independent-2026-09-09`.

Unless stated otherwise, source paths below are relative to `papers/A2-v5-boundary-factorization/` at the frozen commit. Labels, not independently verified PDF pagination, identify the mathematical statements. The review commit has the frozen manuscript as its sole parent and adds review material only.

## 1. Executive assessment

This revision makes three genuine advances over the reviewed v4 submission. The relative factorization is now formulated for a nonperiodic sequence of uniformly diagonally dominant scalar twist actions. The formerly missing positive pairwise inverse is proved, with a sharp one-third exponent and four direct limiting amplitudes. The residual-time statistic is a genuinely different observation that removes the inverse-offset factor from the stated timing error. These developments answer the substance of the previous NBL requests. They cannot fairly be described as cosmetic changes, an unchanged circular-reference result, or another repetition of an obstruction.

My audit identifies no fatal mathematical counterexample to Theorems 5.1, 6.3, 10.3, or 13.1 under their printed hypotheses. In particular, the relative determinant argument does not divide an uncontrolled action error by an exponentially small flux; the inverse does not assume separated roots; the area enlargement is not an illicit extra physical parameter; and the ratio estimator does not assume independence between its numerator and denominator. These are important positive findings, not an acceptance certificate.

I nevertheless do not recommend this version for the requested journals. The new central result is a careful uniform construction for a strongly coercive one-dimensional local variational system. Its billiard consequence is an exact physical law near isolated normal channels, not an analysis of unrestricted long records. The other two new theorems are concrete applications of, respectively, a nonsingular symmetric-coordinate observation map followed by cubic root matching, and a smooth ratio followed by fixed-order extrapolation and concentration. They are useful results. In my judgment, the manuscript has not yet made a sufficiently compelling case that this particular combination changes the understanding of a major problem or introduces a method of exceptional reach.

This judgment is about the mathematical significance demonstrated by the actual results, not an alleged obligation to prove global rigidity, remove every convexity hypothesis, or solve the earlier Fourier programme. Local results can be major results; elementary final formulas can encode deep work. Here the difficulty that is genuinely resolved is the relative normalization of a long bridge on one common neighborhood. The presentation now identifies it clearly, but the additional inverse and acquisition conclusions do not establish independent breakthroughs commensurate with the journal ambition. Simply adding more such consequences would not resolve this assessment.

I also give a constructive refinement that helps separate the content of the inverse result from its packaging: near the physical member with $R=1/4$, the first **three** amplitudes already admit a sharp pairwise one-third inverse and Lipschitz area recovery. The relevant physical three-dimensional Jacobian is explicitly nonzero; a proof is given in Section 6 of this report. This is not a counterexample to four-amplitude sufficiency, and the manuscript does not claim that four is minimal. It is not a new condition for acceptance.

## 2. Disposition of the previous referee requests

| Previous request | Disposition in v5 |
|---|---|
| NBL-R1: distinguish nonlinear information from information appearing only at long collision order | **Addressed.** Proposition `prop:v5-one-flight` records the derivative $8/9$ already at one complete flight, alongside the limiting $\sqrt3/2$. The introduction expressly disclaims a strictly increasing hierarchy of inverse coordinates. Theorem `thm:v5-chain-factorization` also supplies an actual reusable nonperiodic formulation, not merely a request for one. |
| NBL-R2: distinguish a circular-reference estimate from a nearby pairwise inverse | **Addressed, with a positive new theorem.** `thm:v5-pairwise` proves four-amplitude pairwise recovery, including multiplicities, and its sharp exponent $1/3$. The old reference-point $1/2$ theorems retain their correct scope. |
| NBL-R3: account for physical-window calibration and the harmonic sensitivity | **Addressed, with an additional-data improvement.** `prop:v5-harmonic` proves the coefficient $-v_{j,b}H_m/h$. `thm:v5-residual-recovery` changes the normalizer using observed first residual times and improves the sufficient calibration scale. Supplied-gap and preparation qualifications remain explicit. |
| Separate bounded Green derivatives from trace-class perturbation derivatives | **Addressed.** `eq:v5-operator-trace-bounds` and the added norm display in `v5/20_boundary_layers.tex` make the required distinction. |
| Clarify moving poles and add the De Simoi–Kaloshin–Leguil comparison | **Addressed.** `cor:v4-poles` distinguishes undifferentiated simple poles from parameter derivatives. `v5/references.tex` and the comparison section include the Inventiones article with the relevant hypothesis distinctions. |

There is no outstanding NBL correctness request that should simply be copied into another negative report. The remaining recommendations below concern attribution, mathematical emphasis, and the significance of the revised submission. They do not retrospectively convert the previous requests into promises of acceptance.

## 3. Audit of the main analytical chain

### 3.1 Geometry and physical preparation

**Locators:** `v3/10_geometry_action.tex`, `lem:g-channels`, `lem:g-jacobi`, `lem:g-relative`; `v3/20_integration.tex`, `lem:g-radial`.

The ground-onset localization is derived from the periodic geometry. Only finitely many lifted obstacle pairs can lie below a fixed distance bound. Strict convexity makes a minimizing normal chord unique. Its distance Hessian is positive definite. A third obstacle cannot intersect a globally shortest chord without giving a shorter gap, and the relevant clearance persists under the local parameter perturbations. Separation of the finitely many outgoing normal states forces reversal of consecutive sufficiently short flights. Because every complete flight is at least the minimum gap, a bound on total excess controls each flight without accumulating a factor of the collision order.

The distinction between a whole ground-onset event and a selected nonminimal itinerary is maintained. A nonminimal channel is not assumed to remain visible in the unselected ground collar at arbitrary order. The construction neither requires congruent obstacles nor imports finite horizon. These are not surviving defects.

The alternating quadratic calculation also checks out. Writing $c_b=1+g\kappa_b$, $c=\sqrt{c_0c_1}$, $\gamma=\operatorname{arcosh}c$, $\sigma_i=\sqrt{c_{1-(i\bmod2)}}$, and $D_j=\operatorname{diag}(\sigma_0,\sigma_j)$, the endpoint Hessian is

$$
\mathsf H_j=\frac{c\sinh\gamma}{g}D_j^{-1}
\begin{pmatrix}\coth(j\gamma)&-\operatorname{csch}(j\gamma)\\
-\operatorname{csch}(j\gamma)&\coth(j\gamma)\end{pmatrix}D_j^{-1}.
$$

At $j=1$ it is $g^{-1}\left(\begin{smallmatrix}c_0&-1\\-1&c_1\end{smallmatrix}\right)$. The ratio of the negative mixed derivative to the square root of the determinant is $\operatorname{csch}(j\gamma)$ for both parities. Uniform endpoint coercivity is not confused with uniform size of that exponentially small mixed derivative.

The equilibrium preparation factor is present. In first-impact endpoint coordinates the measure is

$$
\frac{-W_{uv}}{2\pi A}\,du\,dv\,dr.
$$

The residual interval is $0<r<d-(W-jg)$ and lies below every preceding roof on the chosen collar. Nor can a further roof fit after the last impact. Thus the full-phase law, rather than an initial distribution on a transverse section, is actually being integrated. The common Morse construction and radial cancellation justify smooth right extensions in $d$; the proof does not obtain them by formally differentiating an indicator. The result is the correctly normalized channel probability $d^2[1+d\mathcal R_j(d)]/[2A\sinh(j\gamma)]$.

### 3.2 The nonperiodic chain theorem

**Locator:** `v5/10_twist_chains.tex`, `thm:v5-chain-factorization` (Theorem 5.1).

The theorem is correctly stronger than the alternating billiard calculation. The actions may vary without periodicity or convergence at infinity. The zero configuration is stationary for every edge, the twists have positive upper and lower bounds, and each edge Hessian has a fixed diagonal-dominance margin. Uniform bounds on every fixed derivative order include the allowed finite-dimensional parameters.

The basic inverse estimates follow from $H=D-B$ and $\|D^{-1}B\|_\infty\le q<1$. A nearest-neighbor path needs at least $|i-k|$ steps to join sites $i,k$. A finite-to-half-line difference needs a path reaching the missing boundary and returning. These facts justify the displayed exponential kernels. Symmetry transfers the bounded inverse from $\ell^\infty$ to $\ell^1$; positivity also gives the appropriate $\ell^2$ operator. Fixed parameter derivatives insert bounded band matrices, and polynomial factors in path lengths can be absorbed using a strict exponential margin.

The nonlinear construction uses a weighted space in which convolution with those kernels is uniformly bounded. The local gradient remainder is quadratic and has small derivative on a small weighted ball. Differentiating the fixed-point equation leaves the same invertible operator on the highest derivative. Uniqueness in the whole small coordinate box follows separately from the averaged Hessian. Thus existence is not being asserted only for a length-dependent contraction ball. Action summability, the endpoint first variation, and the lower convexity bound for the half-line actions have the necessary justification.

The gluing argument controls an $\ell^1$ residual and then an $\ell^1$ correction. The opposite-end products, endpoint overwrites, and truncated tails all have exponential separation. Their fixed derivatives remain summable. Zero value and first endpoint differential at the origin give the additional quadratic vanishing of the action error.

The decisive step is the exact cofactor identity

$$
-\mathcal W_{m,n,uv}
=\frac{\prod_{i=m}^{n-1}[-L_{i,uv}(x_i,x_{i+1})]}{\det H_I}.
$$

Normalizing this identity at zero produces the logarithmic edge sum minus a relative logarithmic determinant. The perturbation $\Delta H_I$ has uniformly summable entries, hence uniformly bounded trace norm; its small undifferentiated norm is $O(|u|+|v|)$. Derivatives of the reference Green operator need only bounded operator norm. Every product derivative of $G_I\Delta H_I$ retains a trace-class factor. This is the correct way to avoid a factor equal to the number of interior sites.

The two retained boundary blocks have size $\lfloor(n-m)/3\rfloor$. Removing the middle perturbation costs trace norm, not an extensive operator-norm estimate. The compressed finite Green matrix approaches the direct sum of the two half-line compressions, including its off-diagonal blocks. The trace-log comparison follows from

$$
|\operatorname{tr}(T^s-(T')^s)|\le s q_1^{s-1}\|T-T'\|_1,
\qquad \|T\|,\|T'\|\le q_1<1.
$$

The differentiated series remains summable after its fixed polynomial factors. This establishes relative amplitude factorization independently of the action estimate. There is no identified missing determinant factor or unabsorbed volume factor.

The choice of one endpoint box and one slower rate for all fixed derivative orders is credible under the stated uniform smoothness hypotheses: derivative orders change constants and polynomial factors, not the underlying locality or spectral gap. The analytic assertion is restricted to uniformly holomorphic extensions. Finally, the nonperiodic statement compares an interval with its own endpoint-dependent half-lines. It correctly does not assert a single site-independent limiting law.

### 3.3 From factorization to a nonlinear physical law

**Locator:** `v5/20_boundary_layers.tex`, `thm:v4-factorization`, `thm:v4-law` (Theorems 6.2 and 6.3).

The explicit half-line Hessian and alternating Green kernel agree with the finite Dirichlet limit. Their boundary curvatures are $a_b=c\sinh\gamma/(g c_{1-b})$. At parity $p$, $d_j^0=\sqrt{a_0a_p}/\sinh(j\gamma)$, yielding

$$
F_j(d)=\frac{\sqrt{a_0a_p}}{\pi d^2}
\int(d-E_j)_+b_j\,du\,dv.
$$

Convergence down to $d=0$ requires more than convergence of integrands away from the moving boundary. The paper supplies the needed common Morse-coordinate comparison. The inverse maps vanish at zero, their difference is $O(\tau^j|w|)$, and fixed-order differences of transformed amplitudes are controlled. Radial integration eliminates odd powers of $\sqrt d$, giving the stated smooth normalized convergence.

For the conditional laws, comparison takes place first on the common latent domain. Coupling the nearby latent densities and nearby scaled endpoint maps proves a bounded-Lipschitz estimate. The resulting limiting density contains the common constraint $S_0(u)+S_p(v)+r<d$; it is not a product probability. The manuscript explicitly retains this coupling. It also avoids an unjustified total-variation comparison of full records lying on different embedded surfaces.

The first-pole corollary is correct but should count as a consequence, not an additional spectral theory. Exponentially accurate parity limits produce a rational principal part and a larger holomorphic disk for the remainder. Parameter derivatives moving $\gamma$ can raise the principal pole order, as now stated. The coefficients use different physical windows, so this is not an unrestricted fixed-window dynamical zeta function.

### 3.4 Nonlinear information and inherited records

**Locators:** `v5/30_nonlinear_information.tex`; `v3/30_observability.tex`; `v3/50_record_response.tex`.

The fourth-jet computation retains both the stationary-action contribution and the relative determinant contribution. At equal even contacts it gives

$$
\partial_q\mathcal R_\infty(0)
=-\frac{\cosh(2\gamma)+2}{12a^2\sinh(2\gamma)}.
$$

The support-function compensator preserves area without changing the relevant fourth contact jet. The family is therefore geometric, not merely formal. Its first-offset response is $\sqrt3/2$ in the half-line limit and $8/9$ at one complete flight. The author now draws exactly the correct conclusion: nonlinear observations distinguish data invisible to the whole leading hierarchy, but this parameter does not first appear at long order.

The centered Euclidean endpoint variances eliminate the unknown contact location and have leading values equal to the diagonal entries of $\mathsf H_j^{-1}/3$. For odd $j$ their product and ratio give a uniformly conditioned inverse for the two curvatures on compact positive boxes. This does not divide by the exponentially small off-diagonal covariance. The asymmetric fixed-area scalar fiber is realized by the displayed support functions and is separated by those variances.

The record-response section specifies maximum-norm arrays and bounded operator norms for test derivatives. This prevents hidden dimension factors. The moving-cut formula includes its boundary term and imposes explicit margins from the other latent boundaries. Fixed physical schedules are allowed to incur factors of $k/d$; no general uniform differentiated response is inferred from weak convergence alone. I found no new contradiction in these inherited dependencies.

## 4. Audit of the two new quantitative results

### 4.1 Four-amplitude pairwise inversion

**Locator:** `v5/50_pairwise_inverse.tex`, `thm:v5-pairwise`, `lem:v5-jacobian`, `lem:v5-roots` (Theorem 13.1 and Lemmas 13.2–13.3).

The use of elementary symmetric coordinates is mathematically appropriate. The contour formula with $P_e'/P_e$ supplies an analytic extension through multiple roots and counts multiplicities. The temporary independent variable $q=A^{-1}$ is an observation-map device; restricting its local inverse back to the actual physical family is legitimate. There is no dimension-count error.

For $f_j(c)=\operatorname{csch}(j\operatorname{arcosh}c)$, the collision differential has columns $(3f_j,qf_j',-qf_j'',qf_j'''/2)$. The printed determinant is

$$
-\frac{18q^3(64c^8+32c^6+116c^4+4c^2+1)}
{(c^2-1)^2c^4(4c^2-1)^4(2c^2-1)^4}.
$$

I independently recomputed its rational Wronskian reduction exactly. The expression is correct and nonzero for $c>1,q>0$. The subsequent convex-neighborhood argument controls the differential relative to one invertible matrix and integrates along line segments. It therefore supplies a pairwise Lipschitz coefficient inverse, not merely pointwise local invertibility with uncontrolled constants.

The root estimate also addresses the relevant issue. A union of disks around the roots of the first cubic has boundary distance at least the chosen radius from every root. Rouché counting on its components preserves multiplicity, and a component formed from at most three disks has controlled diameter. This gives a matching estimate, not merely Hausdorff proximity. The cubic-root exponent is then transported to the physical curvatures. Projection by minimum discrepancy onto a compact physical image is a valid finite-noisy-coefficient reconstruction.

The sharpness path is an actual support-function path. Its radii are $(R+36s,R-18s,R-18s)$, and its area is even in $s$. The first-order numerator cancels. Since

$$
\Phi_1'''(r)=\frac{3(3g+r)}{\sqrt g\,(g+2r)^{7/2}}>0,
$$

one obtains the nonzero cubic coefficient $11664\Phi_1'''(R)/A_*$ in $C_1(s)-C_1(-s)$. Sorted matching gives $36s/(R^2-324s^2)$ for small positive $s$. The bound on third derivatives of the sequence, with a strict exponential margin, supplies the whole-sequence upper estimate; a finite prefix calculation alone would not. Thus attainability and sharpness are both established for the stated pairwise problem.

The result is not a general theory of singular Prony inversion. Once the specific analytic observation has an invertible coefficient differential, the exponent is the familiar loss in recovering three colliding roots. The new work is the verification for these four particular probability amplitudes and its realization in the billiard family. This is a narrower but real contribution. The manuscript's existing citation to regular confluent-Prony conditioning should be supplemented by the collision/Vieta comparison discussed in Section 7 below.

### 4.2 Residual normalization, sampling, and calibration

**Locator:** `v5/40_residual_calibration.tex`, `prop:v5-harmonic`, `lem:v5-residual`, `thm:v5-residual-recovery` (Proposition 10.1, Lemma 10.2, Theorem 10.3).

The harmonic sensitivity calculation is exact. The Richardson weights satisfy $\sum_l\omega_l/l=H_m$, so the old programmed-offset population statistic has derivative $-v_{j,b}H_m/h+O_m(1)$. Extrapolation does not remove that leading inverse-offset factor.

The new normalizer does remove it by changing the data. On the common latent domain, the mean residual fraction at zero is $1/3$. Radial smoothness therefore gives $D_j(d)=3\mathbb E r/d=1+O(d)$ with a uniform positive lower bound. The ratio $T_{j,b}(d)=\operatorname{Var}(Q_b)/(3\mathbb E r)$ has the same leading variance and a uniformly bounded offset derivative. This is a ratio of population means, not the potentially singular mean of a quantity involving $1/r$.

At actual offset $d_l=lh-\tau$, the normalized sample means have expectations $s_lV_{j,b}(d_l)$ and $s_lD_j(d_l)$, where $s_l=d_l/(lh)\in[1/2,3/2]$. Their common scale cancels. Both types of summands are uniformly bounded by geometric coercivity and $r<d_l$. Concentration and a union bound do not require numerator-denominator independence within a window. The true denominator is at least $1/4$, and the stated sample-size condition makes the clipping inactive on the good event. The ratio map is then uniformly Lipschitz.

Fixed-order polynomial cancellation and the bounded offset derivative produce $h^m+|\tau|$ deterministic error. The joint gap-variance inverse contributes the separate $|\Delta g|$ term. Hence

$$
C_m\left[h^m+\sqrt{\frac{\log(C_m/\eta)}K}
+j|\Delta g|+|\Delta g|\right]
$$

is supported by the proof. Waiting for independent successful preparations has the stated expectation and binomial tail bound, since success probability is comparable to $(lh)^2e^{-j\gamma}$. The simultaneous high-probability claim needs only a union bound, not independence of the error and waiting-time events.

This is a correct procedure-specific improvement. It is not joint unknown-gap estimation, a sensor-noise theorem, or a minimax bound. The author says so. Those exclusions must not be recycled as false-claim allegations. They do mean that this theorem supplies a controlled calibration refinement, rather than an independently comprehensive statistical inverse theory.

## 5. Why the venue recommendation remains negative

### BF-R1 — The central theorem needs a sharper importance argument, not a broader adjective

Theorem 5.1 is a real generalization from an alternating medium to a spatially varying one. Its strength is a common nonlinear chart together with relative, differentiated, exponentially accurate boundary separation. The proof resolves the normalization problem correctly. Nevertheless, the permitted medium remains scalar, nearest-neighbor, locally pinned at a known stationary configuration, and uniformly coercive with a fixed positive margin. The difficulty is not nonuniform hyperbolicity, global orbit selection, or degeneration of the Jacobi operator. The nonperiodic coefficients do not remove these strong simplifying features.

The response to v4 asked for a reusable formulation as one possible way to clarify significance, and the author has supplied it. I do not now redefine that request to mean a theorem for all hyperbolic systems. My judgment is instead that the reusable formulation actually proved still lies within a particularly tractable localization mechanism, while its demonstrated applications remain the same normal-channel laws. The revised article needs to establish why this precise uniform statement matters beyond being a technically stronger version of a finite-segment calculation. Repeating that the statement is relative, all-order, or nonperiodic is not by itself that argument.

The comparison should separate the established inverse-decay and trace-determinant tools from the particular nonlinear full-phase synthesis. Demko–Moss–Smith and the trace-ideal framework of Simon are relevant analytical antecedents [3–4]; Hill-type variational identities are already appropriately acknowledged [2]. None of these citations, by itself, proves that Theorem 5.1 or its physical consequence is already known. I make no such assertion.

A useful algebraic observation illustrates why the printed hypotheses should remain presented as sufficient local conditions, not as an intrinsic characterization. For a bounded sequence $a_i$, replace

$$
L_i(u,v)\quad\hbox{by}\quad
\widetilde L_i(u,v)=L_i(u,v)+\tfrac12a_i u^2-\tfrac12a_{i+1}v^2.
$$

Interior stationary equations, interior Hessians, and mixed twists are unchanged. Finite actions change only by the endpoint term. The half-line actions change by $+a_m u^2/2$ and $-a_n v^2/2$, respectively; their amplitudes are unchanged. Thus the factorization differences themselves are invariant under this operation, although edgewise diagonal dominance need not be.

For example, $L(u,v)=u^2+v^2-uv$ satisfies the hypotheses. Taking every $a_i=5/4$ gives $\widetilde L_{vv}=3/4<|\widetilde L_{uv}|=1$, while its interior Hessian is still the matrix with diagonal $4$ and adjacent entries $-1$. The half-line second derivatives become $\sqrt3\pm5/4$, both positive. This elementary example does not refute the theorem. It demonstrates that its convenient edge normalization is more restrictive than the invariant boundary-separation mechanism. A brief observation of this kind would sharpen the conceptual formulation; a new general theorem is not demanded here.

### BF-R2 — Count the new inverse and acquisition results at their actual depth

Theorem 13.1 is the positive result missing from the earlier package. Theorem 10.3 genuinely improves calibration sensitivity with an additional observable. Both should remain. Their proofs also show why they do not independently transform the significance assessment: the singular exponent is supplied by cubic coefficient-to-root inversion once an explicit finite Jacobian is nonsingular; the acquisition estimate follows from a smooth ratio, classical extrapolation, bounded-variable concentration, and the previously established geometric success probability.

Neither statement depends essentially on the new nonperiodic factorization theorem. The pairwise inverse uses the leading amplitude formula. The acquisition theorem uses the uniform smooth finite-bridge expansion and the leading variance inverse. The genuinely long-bridge result is Theorem 6.3. A main-results narrative should reflect this dependency structure rather than allow several different senses of “uniform,” “sharp,” and “recovery” to suggest a single larger theorem.

The exponent $1/3$ is sharp. The number four is sufficient, not claimed minimal. Section 6 below shows concretely that these are different questions. The author should preserve that distinction; proving minimality or generalizing the refinement to every $R$ is not a required repair.

### BF-R3 — Preserve the data model and remove cumulative duplication from the main argument

Four limiting coefficients with an absolute error bound are not four raw physical count observations. Conversely, the residual-normalized estimator uses selected positions and times, not merely unlabelled amplitudes. The manuscript already distinguishes these experiments. That distinction should remain immediately visible wherever the results are summarized, particularly because the coefficient inverse and the preparation theorem do not combine into a proved end-to-end acquisition theorem for unlabelled curvature triples.

The leading-data saturation and the one-flight fourth-jet comparison are also already correct. Long collision order preserves access to the same leading contact parameters at an exponentially increasing preparation cost; it supplies a limiting nonlinear law, not a demonstrated advantage for learning those parameters. This is a scope assessment, not an information-theoretic impossibility theorem for every conceivable experiment.

Finally, the active article gives both the abstract proof of boundary factorization and a lengthy second proof of nearly the same gluing and determinant comparison in the alternating case. Preserving historical derivations does not require the main narrative to prove the same mechanism twice. A general theorem, explicit billiard identification of its constants, and physical limiting law would make the conceptual dependency easier to judge. The exact old derivations and circular calculations can remain available without being counted as independent contributions. Page count, label preservation, and diagnostic counts have no bearing on the editorial significance of the result.

These three comments are not a new checklist of mandatory research achievements. BF-R1 is the controlling importance objection; BF-R2 and BF-R3 explain why the ancillary results and cumulative organization do not overcome it. Correcting citations or adding the optional calculation below would not by itself reverse the recommendation.

## 6. An independent refinement: three physical amplitudes near $R=1/4$

This section supplies a mathematical observation of the present referee, not an alleged error in Theorem 13.1. It keeps the same physical family and takes its dependent area seriously.

Let $z_r=\kappa_r^{-1}-R$ be the three radius shifts, and let $E_1,E_2,E_3$ be their elementary symmetric functions. The support-function formulas give

$$
\alpha=\frac{E_1}{108},\qquad
\beta^2+\zeta^2=\frac{E_1^2}{2916}-\frac{E_2}{972}.
$$

Substituting into `eq:v3-area` yields the exact physical identity

$$
A(E)=A_* -\frac{\pi R}{54}E_1
+\frac{41\pi}{7776}E_1^2-\frac{5\pi}{432}E_2,
\qquad A_* =\frac{\sqrt3}{2}-\pi R^2. \tag{R1}
$$

In particular, area has no independent fourth coordinate here. At fixed $g=1-2R$, put

$$
\phi_j(r)=\operatorname{csch}\!\left(j\operatorname{arcosh}(1+g/r)\right),
\qquad \mathcal C_j(E)=\frac{\sum_{r=0}^2\phi_j(R+z_r)}{A(E)}.
$$

The same contour/Newton-sum argument used in the manuscript makes $\mathcal C_j$ analytic in a full coefficient neighborhood of $E=0$. For $j=1,2,3$, its differential has row

$$
\frac1{A_*}\left(
\phi_j'(R)+\frac{\pi R}{18A_*}\phi_j(R),\;
-\phi_j''(R)+\frac{5\pi}{144A_*}\phi_j(R),\;
\frac{\phi_j'''(R)}2\right). \tag{R2}
$$

The primes here differentiate radius while holding $g$ fixed; substituting $g=1-2R$ is done only after that differentiation. This distinction matters in the calculation.

At $R=1/4$, $g=1/2$, direct exact algebra gives

$$
\det D(\mathcal C_1,\mathcal C_2,\mathcal C_3)(0)
=-\frac{4(15804720 A_*+64253\pi)}
{72930375\sqrt2\,A_*^4}<0,
\qquad A_* =\frac{\sqrt3}{2}-\frac\pi{16}. \tag{R3}
$$

For a reproducible reduction, write $\phi_j(r)=h(r)p_j(r)$, where

$$
h(r)=\frac{r}{\sqrt{g(g+2r)}},\quad
p_1=1,\quad p_2=\frac1{2(1+g/r)},\quad
p_3=\frac1{4(1+g/r)^2-1}.
$$

If $\phi_j^{(k)}=h d_{j,k}$, then $d_{j,0}=p_j$ and

$$
d_{j,k+1}=d_{j,k}'+\left(\frac1r-\frac1{g+2r}\right)d_{j,k}.
$$

Three iterations reduce (R2) to rational functions, with $h(1/4)=1/(2\sqrt2)$. Expansion of the resulting $3\times3$ determinant gives (R3). The accompanying script verifies this equality symbolically and independently evaluates the derivative matrix at 70-digit precision, giving approximately $-2.07986047434710822848$.

By continuity of the differential on a small convex coefficient ball, (R3) gives a pairwise Lipschitz inverse for $(E_1,E_2,E_3)$ from these first three amplitudes. Apply the manuscript's multiplicity-preserving cubic root estimate to recover the radii, and then the locally Lipschitz reciprocal map to recover the curvatures. Formula (R1) gives Lipschitz area recovery. Consequently, on a sufficiently small physical neighborhood at this fixed $R$,

$$
\operatorname{dist}_{\rm match}(\kappa,\widetilde\kappa)
\le C\max_{1\le j\le3}|C_j-\widetilde C_j|^{1/3},
\qquad
|A-\widetilde A|\le C\max_{1\le j\le3}|C_j-\widetilde C_j|. \tag{R4}
$$

Compact-image minimum-discrepancy reconstruction gives the analogous noisy-coefficient guarantee. The physical $s,-s$ path used in the manuscript has a nonzero cubic discrepancy already in $C_1$ and only cubic discrepancies in every fixed finite coefficient. Its matching distance is linear. Thus the exponent in (R4) is sharp as well.

The statement is deliberately local at $R=1/4$. This report does not assert the same three-amplitude determinant is nonzero for every $R\in(0,1/2)$, does not claim a minimal-data theorem, and does not invalidate the author's uniform-in-$c>1$ four-coordinate Jacobian. The refinement is useful precisely because it separates an exponent statement, an observation-count statement, and an auxiliary-coordinate choice.

## 7. Literature and attribution

The new singular inverse should be compared with Batenkov–Yomdin's *Geometry and Singularities of the Prony mapping* [1], not only their earlier regular confluent-conditioning result. Their primary abstract explicitly discusses colliding nodes, coefficient/root geometry, and the Vieta map. That makes it a relevant antecedent for the organizing principle in Section 13. It does not establish that the specific four billiard amplitudes or the physical sharpness path are covered by their theorem. The proper attribution is to the singular-coordinate framework, while identifying the author's explicit probability-map verification as the concrete contribution.

The comparison with Bolotin–Treschev [2] is already appropriately qualified. Their variational setting relates action Hessians and dynamics, but that alone does not establish the uniform normalized full-phase probability law. Likewise, inverse-decay and trace-ideal references [3–4] identify background tools, not an exact antecedent for the whole nonlinear theorem. The active bibliography does not currently include [1], [3], or [4]. A precise comparison would improve attribution; their mere addition would not settle originality or importance.

The newly added De Simoi–Kaloshin–Leguil paper [5] concerns marked-length determination in an analytic open-billiard class with non-eclipse, symmetry, and genericity hypotheses. Its stronger geometric conclusion comes from different data under different assumptions. The manuscript now says this correctly. It would be inappropriate either to ignore that antecedent or to pretend that it directly subsumes the present equilibrium threshold observation.

This was a targeted primary-source abstract and bibliographic check, not a full-proof audit of all comparison articles and not an exhaustive priority search. I found no verified theorem that contains the complete stated nonlinear threshold law. Absence of such a finding is neither a novelty certificate nor a reason to label the result already known.

## 8. Independent diagnostics, reproducibility, and audit limits

The accompanying `independent_diagnostics.py` imports no repository code and makes no network calls. Its final version passes **48 named checks**, both normally and with `python -O`; the generated JSON files are byte-identical in the recorded environment. The suite has **29 exact symbolic checks, 14 ordinary floating non-interval checks, and 5 high-precision non-interval checks**. Failure conditions use explicit exceptions rather than removable assertions. `VERIFICATION.json` records hashes and commands; `DIAGNOSTICS.json` records the complete results.

The exact checks include the four-amplitude Wronskian, the collision determinant, the radius third derivative, matching and cubic factors, the one-flight and half-line jet coefficients, residual moments, Richardson and harmonic identities through order eight, (R1), and the independent physical determinant (R3). The two elementary coboundary checks concern algebraic telescoping only.

For the nonlinear test I used the nonperiodic chain

$$
L_i(u,v)=\frac{b_i}2(v-u)^2+\frac{a_i}2u^2+
\frac{\widetilde a_i}2v^2+\frac{k_i}6(u^3+0.7v^3)
+\frac{t_i}{24}(u^4+v^4)+\chi_i u^2v^2,
$$

with bounded trigonometric coefficients specified in the script. On $|u|,|v|\le0.1$ their elementary coefficient bounds give a negative twist and positive row margins. Newton solves use the actual local action; the logarithmic relative twist is computed from its cofactor product and reference-normalized Hessian determinant. The endpoint values are $u=0.05$, $v=-0.04$. The comparison uses two length-96 finite approximations to the appropriate half-lines, retaining the actual site indices. A length-64 comparison checks truncation consistency, not the infinite limit.

Selected results for left site $m=3$ are:

| Length | Action factorization discrepancy | Logarithmic relative-twist discrepancy |
|---:|---:|---:|
| 4 | $4.580\times10^{-5}$ | $3.535\times10^{-8}$ |
| 8 | $3.466\times10^{-7}$ | $9.336\times10^{-8}$ |
| 12 | $2.677\times10^{-9}$ | $1.684\times10^{-9}$ |
| 16 | $1.890\times10^{-11}$ | $1.528\times10^{-11}$ |
| 24 | $9.266\times10^{-16}$ | $1.331\times10^{-15}$ |

The nonmonotonic first two twist discrepancies are retained. An exploratory test demanding a hundred-fold drop between lengths 4 and 12 failed because the length-4 discrepancy has an early cancellation. No theorem asserts monotonicity of these errors, so that inappropriate test was removed rather than treating it as a mathematical counterexample. The final suite tests stationary residuals, long finite-boundary agreement, and cutoff consistency; it does not fit or certify an exponential rate. Values near $10^{-15}$ are at the floating-point floor. A second starting site, $m=17$, is also included.

For the geometric sharpness path, 70-digit calculations use the first 128 coefficients, $R=1/4$, and sequence weight $a=0.4$. As $s$ decreases from $10^{-4}$ to $10^{-5}$, the weighted prefix discrepancy divided by $s^3$ changes from approximately $192927.47$ to $192919.07$, while the matching curvature distance divided by $s$ approaches $576$. These computations support the algebraic normalization. The infinite-sequence assertion rests on the written derivative bound, not on a prefix computation.

The recorded environment is Python 3.13.5, NumPy 2.3.5, SciPy 1.17.0, SymPy 1.14.0, and mpmath 1.3.0. High precision does not mean interval arithmetic, and symbolic checks of identities do not certify the analytic existence or uniformity assertions.

The source audit covered all five new mathematical v5 sections, the comparison and bibliography, the introduction's main statements, the active general v3 geometry/integration/observability/inverse/record-response foundations, both active v4 acquisition and coalescence sections, the response letter and proof ledger, and the controlling report's substantive requests. The unchanged circular appendices, original two-collision companion, and every historical branch were not independently re-audited in full in this review. No blanket certification of those materials is intended.

I did not rebuild or inspect the manuscript PDFs, replay the author's 141-, 411-, 328-, 257-, or 252-check suites, replay the previous referee's 81-check suite, run remote CI, simulate the full equilibrium billiard, or use a formal proof assistant. The author's reported 55-page article and 7-page companion build are not my executed build. Preservation counts and author validation receipts are not used as premises of the mathematical assessment.

## 9. Final disposition

The preceding review's NBL requests have received substantive answers. The core relative determinant construction, sharp pairwise inverse, and residual-normalized calibration improvement survive this audit without an identified fatal defect. A future report should not revive objections already answered, accuse the author of treating area as an independent physical coordinate, or describe a correct reference-point theorem as a false pairwise theorem.

The remaining negative recommendation is an editorial assessment of significance. The manuscript contains a coherent and technically careful local relative-flux theory, accompanied by explicit finite-dimensional inverse and sampling consequences. I am not persuaded that the demonstrated reach and consequences of that theory justify the requested exceptional venue level. Additional elementary corollaries, another validation count, or the three-amplitude refinement in this report would not alone supply that case.

**Final recommendation: reject at the requested top-four level in its present form, on importance and positioning rather than an established fatal mathematical counterexample. Retain and credit the substantive mathematical progress. Do not convert this recommendation into an unsupported assertion that the principal theorems are false, wholly contained in the cited literature, or incapable of further development.**

## Primary references and bibliographic entry points

[1] D. Batenkov and Y. Yomdin, *Geometry and Singularities of the Prony mapping*, Journal of Singularities **10** (2014), 1–25. DOI: 10.5427/jsing.2014.10a. Primary abstract inspected: https://arxiv.org/abs/1301.1336. Publication metadata also checked against the authors' institutional publication record. The comparison above uses the collision/Vieta scope, not an unverified theorem-containment claim.

[2] S. Bolotin and D. Treschev, *Hill's formula*, Russian Mathematical Surveys **65** (2010), 191–257. DOI: 10.1070/RM2010v065n02ABEH004671. Primary abstract inspected: https://arxiv.org/abs/1006.1532.

[3] S. Demko, W. F. Moss and P. W. Smith, *Decay rates for inverses of band matrices*, Mathematics of Computation **43** (1984), 491–499. Publisher bibliographic entry: https://www.ams.org/mcom/1984-43-168/S0025-5718-1984-0758197-9/. The indexed metadata were consulted; direct publisher access was restricted. No full-proof comparison with this article is claimed.

[4] B. Simon, *Trace Ideals and Their Applications*, second edition, Mathematical Surveys and Monographs **120**, American Mathematical Society, 2005. Publisher metadata: https://www.ams.org/books/surv/120. Author bibliography confirming the edition: https://www.math.caltech.edu/simon/biblio.html. This is a background reference for the trace-ideal framework, not a claim to have checked a specific theorem encompassing the manuscript.

[5] J. De Simoi, V. Kaloshin and M. Leguil, *Marked Length Spectral determination of analytic chaotic billiards with axial symmetries*, Inventiones Mathematicae **233** (2023), 829–901. DOI: 10.1007/s00222-023-01191-8. Primary abstract and version metadata inspected: https://arxiv.org/abs/1905.00890. This comparison is now present in the manuscript and is not an outstanding omission.
