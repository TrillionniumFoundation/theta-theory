# Independent referee report: A2 v4 — nonlinear boundary laws

## Recommendation: reject at the requested top-four mathematics-journal level in its present form

**Date:** September 9, 2026 (Asia/Singapore).  
**Reviewer:** GPT-6 Astra Pro. This is an independent AI-assisted assessment requested by the repository owner. It is not a report commissioned by a journal or an actual editorial decision.  
**Author:** Qian Qi.  
**Manuscript:** *Uniform collision thresholds and nonlinear boundary laws in periodic dispersing billiards*.  
**Repository:** `TrillionniumFoundation/theta-theory`.  
**Reviewed branch:** `revision/a2-v4-nonlinear-boundary-laws-2026-09-09`.  
**Frozen manuscript commit:** `68bbf5b841a66dcc2b85f4d76ce66b1ae8b9782f`.  
**Manuscript commit time:** September 9, 2026, 01:37:56 UTC, or 09:37:56 Singapore time.  
**Frozen tree:** `636e719b596a0775167b033f2ab548d7e29286e5`.  
**Controlling previous report:** `26b05bf0c6483a326d078c99393f4a34434bcc18`, `reviews/a2-geometric-thresholds-v3-harsh-independent-2026-09-09/REFEREE_REPORT.md`.  
**New review branch:** `review/a2-v4-nonlinear-boundary-laws-harsh-independent-2026-09-09`.

Unless otherwise specified, manuscript paths below are relative to `papers/A2-v4-nonlinear-boundary-laws/` at the frozen commit. The report identifies statements by source labels; it does not use an independently verified PDF pagination. The review commit has the frozen manuscript commit as its sole parent and adds review material only.

## 1. Executive assessment

This is a substantive revision, not a cosmetic response to the v3 report. The new finite-to-half-line comparison controls the normalized nonlinear twist, not merely the action. It gives an actual fixed-positive-offset limiting probability and conditional endpoint law. The analytic deformation in Section 6 really preserves area, gap, and both contact curvatures, while changing a nonlinear statistical coefficient. The circular-reference stability and acquisition results also contain positive estimates absent from v3. These additions must be credited before any venue judgment is made.

The principal analytical assertions have survived this source audit without an identified fatal counterexample. I find the relative determinant comparison in `thm:v4-factorization` coherent on the stated compact, positive-curvature, small-contact-box hypotheses. Its use in the physical limiting law is justified by a common Morse construction and radial cancellation. The quartic derivative has the stated sign and normalization. The Jensen-gap stability proof is valid for its expressly stated circular reference, and the extrapolation and waiting-time estimates are valid for the stated independent-preparation experiment with supplied gap and offsets.

Nevertheless, I do not recommend the paper for one of the requested four journals in its present form. The strongest advance is still a local, collision-order-uniform relative-flux construction around isolated normal period-two channels. The new half-line theorem is a real analytical improvement, but the additional consequences do not yet establish the exceptional conceptual reach claimed by the venue ambition. The geometric fiber is a one-parameter fourth-jet separation, and the same parameter is already detected by the one-flight nonlinear coefficient. The pole calculation is a direct consequence of exponentially accurate parity limits. The positive stability theorem measures distance to a single singular reference rather than solving the nearby pairwise inverse problem. The acquisition improvement is fixed-order polynomial extrapolation of an already established smooth expansion, with an exponentially worsening rarity factor.

These observations do not make the theorems false or the half-line analysis redundant. They do limit how many independent advances can reasonably be extracted from the package. An explicit local result can certainly be important enough for a major journal; neither locality nor an elementary final formula is a disqualification. My negative recommendation is the editorial assessment that the particular mechanism and consequences demonstrated here do not yet make that case. I have not found a prior theorem containing the exact full-phase nonlinear statement, and I do not claim that the manuscript is merely a restatement of a cited result.

Three additional calculations support this assessment. For the author's new fixed-leading-data family,

$$\left.\partial_s\mathcal R_1^{(s)}(0)\right|_{s=0}=\frac89,$$

already at one complete flight, whereas the long-bridge limit is $\sqrt3/2$. For the existing coalescing path, comparison of its two noncircular members at $s$ and $-s$ gives

$$\|C(s)-C(-s)\|_a\asymp |s|^3,\qquad
\operatorname{dist}_{\rm match}(\kappa(s),\kappa(-s))\asymp |s|.$$

Thus no uniform pairwise inverse exponent greater than $1/3$ is possible in that sequence topology, although the reference-point exponent $1/2$ is correct. Finally, the first-order timing sensitivity of the stated extrapolated statistic contains the harmonic factor $H_m/h$. Complete derivations appear below. None is being mislabeled as a counterexample to a theorem which the author explicitly did not state.

## 2. Disposition of the controlling v3 requests

| Previous request | Disposition in v4 |
|---|---|
| OBS-R1: state the leading-data saturation and demonstrate what the nonlinear uniform calculus adds | The saturation is now explicit in `prop:v4-saturation`. Theorems `thm:v4-factorization` and `thm:v4-law` supply genuinely nonlinear long-bridge conclusions, and `thm:v4-jet-fiber` separates the nonlinear observation from the entire leading metric. The concrete request is addressed. The significance of the resulting package must be assessed afresh, not treated as an unchanged missing theorem. |
| OBS-R2: identify a topology for the whole sequence and avoid confusing exact inversion with conditioning | `thm:v4-sequence-stability` incorporates the strict exponential margin and the sequence-level quadratic cancellation. `thm:v4-radial-stability` adds a matching positive estimate at the circular reference. This is more than merely repeating the old obstruction. Its reference-point scope is explicit. |
| OBS-R3: state accuracy versus raw-preparation cost and account for physical-window calibration | `thm:v4-acquisition` gives fixed-order bias cancellation, expected and high-probability costs, and a sufficient accuracy exponent. `prop:v4-timing` propagates the actual offset error. The independent-preparation and known-gap qualifications remain visible. The request is addressed. |

The earlier objections concerning a near-circle-only geometric setup, an allegedly independent fourth area parameter, an unrealized algebraic curvature fiber, or a missing full-phase preparation factor are not grounds for rejecting this version. Those matters were already addressed in v3 and remain addressed.

A further assessment should not consist of increasing the number of requested elementary corollaries after each successful revision. The present recommendation concerns the mathematical importance demonstrated by the revised central theorem, not failure to satisfy an old checklist. Sections 4–6 below identify the exact remaining distinctions; they are not a promise that inserting three more formulas would produce acceptance.

## 3. Audit of the mathematical arguments

### 3.1 Geometry, the alternating Hessian, and the inherited nonlinear chart

**Locators:** `v3/10_geometry_action.tex`, `lem:g-channels`, `lem:g-jacobi`, `lem:g-relative`.

The geometric localization is established from the periodic positive-curvature configuration rather than imposed as an ansatz. Local finiteness leaves only finitely many obstacle pairs below a fixed length bound. Strict convexity gives unique support endpoints for a minimizing displacement; the endpoint distance Hessian is positive definite. A globally shortest chord cannot meet a third obstacle, since its initial portion would produce a smaller gap. The finitely many short outgoing states are separated, and specular reflection forces reversal within a common neighborhood. Since every complete flight is at least the minimal gap, a small total excess bounds each individual excess without accumulating a factor of the collision order.

This proves localization of the complete ground-onset event. A clear nonminimal chord is correctly treated only as a selected local itinerary at its own onset. The proof does not claim that its probability remains visible in the ground collar at arbitrarily large order. Neither finite horizon nor congruence of the obstacles is smuggled into the general argument.

The alternating reduction retains the necessary endpoint scaling. With $c_b=1+g\kappa_b$, $c=\sqrt{c_0c_1}$, $\gamma=\operatorname{arcosh}c$, $\sigma_i^2=c_{1-(i\bmod2)}$, and $D_j=\operatorname{diag}(\sigma_0,\sigma_j)$, the endpoint Hessian is

$$\mathsf H_j=\frac{c\sinh\gamma}{g}D_j^{-1}
\begin{pmatrix}\coth(j\gamma)&-\operatorname{csch}(j\gamma)\\
-\operatorname{csch}(j\gamma)&\coth(j\gamma)\end{pmatrix}D_j^{-1}.$$

Its determinant and mixed derivative give the exact ratio $\operatorname{csch}(j\gamma)$ for both parities. At $j=1$ this reduces to $g^{-1}\begin{pmatrix}c_0&-1\\-1&c_1\end{pmatrix}$. The small mixed derivative is not confused with the uniformly positive eigenvalues used for endpoint inversion.

The weighted Green estimate and local nonlinear contraction supply a common finite-bridge chart. Cubic action errors, rather than quartic ones, are used for general nonsymmetric graphs. The trace-norm estimate for the tridiagonal interior perturbation is the essential step: endpoint localization controls the sum of entries independently of matrix size. The logarithmic determinant keeps at least one trace-class factor after differentiation. The proof does not use a dimension times operator-norm estimate that would destroy uniformity.

### 3.2 Half-line segments and the boundary determinant

**Locator:** `v4/10_boundary_layers.tex`, `lem:v4-halfline`, `eq:v4-half-green` through `eq:v4-half-amplitude`.

The half-line Green kernel has the correct conjugating factors:

$$G_{ik}^{(b)}=\frac{g\sigma_i^{(b)}\sigma_k^{(b)}}{2c\sinh\gamma}
\left(e^{-\gamma|i-k|}-e^{-\gamma(i+k)}\right).$$

It is the Dirichlet inverse for the alternating interior Hessian. The chosen weighted space has a strict exponential margin. The contraction constructs a decaying half-line solution, while diagonal dominance establishes uniqueness among all sufficiently small bounded decaying solutions, not only inside the original contraction ball.

Summability justifies the action $S_b$. First variation leaves the initial boundary term and gives

$$a_b=S_b''(0)=\frac{c\sinh\gamma}{g c_{1-b}}>0.$$

The half-line Hessian perturbation is trace class, including the fixed mixed derivatives used later. The logarithmic edge product is summable. The determinant denominator in $B_b$ has an explicit convergent logarithmic series with $\|G^{(b)}\Delta H_b\|<1/2$. Thus there is no undefined determinant normalization or arbitrary infinite-volume factor. The analytic claim is confined to jointly analytic families; smooth families are not treated as analytic by default.

For readability, the source could state once, before the differentiated determinant comparisons, the operator-norm and trace-norm bounds for the first finitely many derivatives of both arguments. The ingredients are already present. I regard this as an exposition improvement, not a missing mathematical premise.

### 3.3 Relative two-boundary factorization

**Locator:** `thm:v4-factorization` and its proof.

The action and relative twist must be audited separately. The proof does so. Gluing a left half-line to the reversed right half-line produces a local residual with summable norm bounded by a polynomial in $j$ times an exponential. Endpoint overwrites are also exponentially small. The averaged interior Hessian is symmetric and uniformly diagonally dominant, giving both an $\ell^\infty$ and an $\ell^1$ inverse bound. The differentiated correction estimates therefore remain independent of the number of interior variables, up to polynomial factors absorbed by a strict exponential margin.

For the twist, the cofactor identity is used multiplicatively:

$$\log b_j=\sum_{i=0}^{j-1}\log\bigl(g[-\ell_{i\bmod2,uv}]\bigr)
-\log\det(I+G_j\Delta H_j).$$

Truncating the perturbation to the two end blocks costs trace norm, not an extensive operator-norm error. The finite Green matrix, compressed to those blocks, approaches the direct sum of the two half-line compressions; its cross-block term has an exponential separation factor. The trace-norm Lipschitz estimate for the logarithmic determinant then justifies the comparison. It is important that the author actually provides this step: convergence of $W_j-jg$ alone would not imply convergence after division by the exponentially small reference twist.

The same rate $\tau<1$ may be chosen slower than the underlying exponential rates; arbitrary fixed derivative orders change the constants, not the need for a new contact box at every $j$. The proof's zero value and zero first differential for the action difference give the additional quadratic endpoint vanishing needed at small offset. I find no surviving parity error, missing interior determinant, or unabsorbed dimension factor in this argument.

### 3.4 Physical fixed-offset law and the first poles

**Locators:** `v3/20_integration.tex`; `thm:v4-law`, `cor:v4-weights`, `cor:v4-poles`.

The full-phase measure is

$$\frac{-W_{uv}}{2\pi A}\,du\,dv\,dr.$$

The allowed residual interval is shorter than every preceding roof; the remaining terminal time is also too short to add an impact. This remains valid for the selected nonminimal itinerary at its own onset. The physical integral therefore has the stated normalization, not a transverse initial ensemble substituted for equilibrium preparation.

At parity $p$, $d_j^0=\sqrt{a_0a_p}/\sinh(j\gamma)$. Hence the exact normalized probability is

$$F_j(d)=\frac{\sqrt{a_0a_p}}{\pi d^2}
\int(d-E_j)_+b_j\,du\,dv.$$

The comparison down to $d=0$ is properly conducted through common Morse coordinates. The inverse coordinate maps depend smoothly on uniformly positive actions, their difference vanishes at zero, and radial integration removes odd Taylor terms. This justifies the right-smooth offset derivatives of the normalized integral. It is not an unsupported differentiation of a moving indicator.

The limiting conditional density factors in its amplitudes but not as a probability measure: the common inequality $S_0(u)+S_p(v)+r<d$ couples the ends. The bounded-Lipschitz comparison of scaled coordinates follows from a common latent density and a coupling of nearby coordinate maps. A total-variation comparison of different embedded full-record surfaces is not claimed.

The pole formula is also correct. Exponential convergence of the even and odd coefficients implies a holomorphic remainder past the first convergence circle. The positive residue has the stated negative sign, and the negative pole is removable precisely when the two parity functions agree. However, this is an elementary analytic consequence of the factorization, not a separate pressure or dynamical-zeta theorem. The manuscript correctly says that its coefficients use different physical windows.

A minor clarification is appropriate: derivatives with respect to a parameter that moves $\gamma$ can raise the order of the principal poles. The assertion about the same smaller holomorphic domains should not be read as saying that all differentiated series still have simple poles. The displayed decomposition already provides the correct interpretation by differentiating its principal term.

### 3.5 Fourth-jet sensitivity and the realized geometric fiber

**Locator:** `v4/20_nonlinear_information.tex`, `prop:v4-quartic`, `thm:v4-jet-fiber`.

The coefficient computation is correct. On the linear half-line $x_i=\lambda^i u$, the quartic jet enters the broken action as $q(x_i^4+x_{i+1}^4)/24$. Stationarity prevents the cubic trajectory correction from altering the quartic stationary action. Consequently

$$\partial_q t=1+2\sum_{i\ge1}\lambda^{4i}=\coth(2\gamma).$$

The same pure fourth powers have no quadratic mixed-edge contribution. The interior diagonal Hessian variation is $q\lambda^{2i}u^2$, and $G_{ii}=(1-\lambda^{2i})/(2a)$ gives

$$\partial_q\beta=-\frac{1}{4a\sinh(2\gamma)}.$$

The residual-time moments yield

$$\mathcal R_\infty(0)=\frac{2\beta}{3a}-\frac{t}{12a^2},\qquad
\partial_q\mathcal R_\infty(0)=-\frac{\cosh(2\gamma)+2}{12a^2\sinh(2\gamma)}.$$

The support-function construction is also genuine. The compensator has nonzero area derivative $5\pi/8$ while leaving the fourth contact jet unchanged. Area, horizontal gap, and both contact curvatures remain fixed exactly. The local graph has $q_s=3-24s$. At $g=\kappa=1$, substitution gives the claimed derivative $\sqrt3/2$. A small parameter interval preserves positive curvature, clearance, and the gap to nonhorizontal translates. Higher graph jets cannot contribute to this first offset coefficient.

The result is a valid distinction between leading data and nonlinear data. It is not arbitrary shape recovery; the inverse-function theorem reconstructs one supplied family parameter. The author states that limitation. Section 4 explains a further limitation of the example's role in the importance argument.

### 3.6 Endpoint observations, coalescence, acquisition, and retained material

**Locators:** `v3/30_observability.tex`, `v3/40_inverse.tex`, `v4/30_saturation_acquisition.tex`, `v4/40_coalescence.tex`, `v3/50_record_response.tex`.

The inherited covariance identity is correctly centered: $\operatorname{Cov}(Y)/d=\mathsf H_j^{-1}/3+O(d)$. In the Euclidean physical position, orthogonality of tangent and normal removes the cubic term in the squared displacement. Thus the observable scalar variances do not require supplying the unknown contact point or tangent. The odd-order two-variance inverse remains uniformly Lipschitz on the stated compact boxes without division by the small off-diagonal covariance.

The exact unlabelled inverse is correctly separated from quantitative stability. The odd-index Möbius transform is absolutely convergent. Positive finite-exponential-sum recovery handles repeated nodes through Hankel rank and multiplicities. The Fourier support-function area formula makes the area a symmetric function of the three recovered radii, not a fourth independent coordinate.

The new statistic $J$ is a Jensen gap for $f(x)=x^2/(4-x^2)$ with uniformly positive weights. Its comparison with weighted variance proves the two-sided circular-reference estimate. The second derivative bound $|C_j''(s)|\le B(1+j)^2e^{-j\gamma_-}$ supplies the whole-sequence quadratic estimate with $a<\gamma_-$. These arguments prove exactly the claimed reference-point sharpness. They do not prove pairwise one-half-Hölder stability, and the source explicitly refrains from claiming it.

The extrapolation weights cancel the first $m-1$ powers of the offset. Uniform smoothness of the variance expansion, rather than an uncontrolled length-dependent remainder, justifies the resulting bias. The paired successful records are independent because the raw preparations are independent. Their normalized summands are bounded. The binomial lower-tail argument gives a simultaneous high-probability bound on waiting time and estimation error by a union bound; independence between those two final events is unnecessary.

The cost $e^{j\gamma}\epsilon^{-(2+2/m)}$ times the stated logarithm is a sufficient cost for this procedure at fixed $m$. It is not a minimax result, an assertion uniform as $m\to\infty$, or an advantage of increasing collision order. The programmed-window error is correctly propagated through both the offset denominator and the supplied-gap inverse. A separate cost for learning an unknown gap is not included in that conditional experiment.

The record-response section uses a maximum norm and dimension-independent operator norms of test derivatives. Its moving-cut formula retains the boundary term and states the transversality margin. It does not infer parameter differentiability from a total-variation estimate for a discontinuous decoder. The circular appendices retain their consistent even-parity improvements, the independent-roof comparison, and the distinction between onset series and a fixed-window count generating function.

The two-collision companion has a separate regular-window argument. Its positive gap, complete short-flight transversality, regular terminal level, moving-level formulas, and explicit positivity witness remain consistent with the main onset calculation. The preserved Round 33 chapter is a conditional Fourier compiler; the main paper does not establish its full mechanical frequency hypotheses. I have not treated that separate program as a false theorem being asserted in v4.

## 4. NBL-R1 — What the new geometric fiber does and does not show

**Classification:** a new exact calculation relevant to significance and presentation; not a falsity finding.

The previous leading-data saturation argument has now been incorporated. The new fiber genuinely goes beyond that leading hierarchy. But it is important not to substitute a different implicit comparison: nonlinear information versus leading information is not the same as long-record information versus information available at one flight.

For identical even graphs, retain the paper's notation

$$F_j(d)=1+d\mathcal R_j(0)+O(d^2).$$

At $j=1$, there are no interior variables and no interior determinant. The quadratic Hessian is

$$\mathsf H_1=\frac1g\begin{pmatrix}c&-1\\-1&c\end{pmatrix},\qquad
(\mathsf H_1^{-1})_{00}=(\mathsf H_1^{-1})_{11}
=\frac{gc}{c^2-1}=:v.$$

The fourth-jet variation of the action is $(u^4+v_{\rm end}^4)/24$; here $v_{\rm end}$ denotes the second endpoint coordinate, distinct from the scalar variance factor $v$. Its mixed derivative vanishes, so there is no quadratic amplitude variation from this jet. Radial integration of the quartic action term gives

$$\partial_q\mathcal R_1(0)=-\frac1{24}(v^2+v^2)
=-\frac{g^2c^2}{12(c^2-1)^2}. \tag{N1}$$

This can also be checked directly by setting $j=1$ in `eq:v4-finite-quartic`; the empty interior sum is essential. At the author's fixed-area family, $g=1$, $c=2$, and $q_s'= -24$. Thus

$$\partial_q\mathcal R_1(0)=-\frac1{27},\qquad
\left.\partial_s\mathcal R_1^{(s)}(0)\right|_{s=0}=\frac89. \tag{N2}$$

The normalized one-flight probability consequently has nonzero parameter derivative $(8/9)d+O(d^2)$ at every sufficiently small positive offset. Area compensation does not change this calculation: the area and contact Hessian are fixed, and higher jets cannot enter the first offset coefficient. One complete flight means two impacts in the paper's convention, not one impact.

For comparison, the proved long-bridge value is $\sqrt3/2$. The independent finite calculations give $0.888888888889$ at $j=1$, $0.861111111111$ at $j=2$, and values approaching $0.866025403784$ at large $j$. There is no contradiction; the coefficient need not be monotone in $j$.

The correct conclusion is therefore that nonlinear physical data distinguish obstacles which all leading statistics fail to distinguish. This explicit example does not show that taking long records reveals a parameter inaccessible to one-flight nonlinear data. The paper does not explicitly assert that stronger proposition, so (N2) is not a refutation of `thm:v4-jet-fiber`.

**Requested response:** state this one-flight comparison alongside the fiber and identify the actual additional content of the long-bridge theorem: existence, relative factorization, and uniform smooth convergence of its limiting physical law. Do not describe the fiber itself as evidence of a strictly growing inverse-information hierarchy in collision order. A genuinely long-record-only inverse separation would be a different and stronger result, but it is not being demanded as a condition for correctness of the theorem already printed.

For the venue assessment, the distinction matters. The long-bridge construction cannot borrow all of its importance from an example whose distinguishing parameter is detected by the elementary finite calculation (N1). Its importance must be defended on its own analytical content or a further substantive application, rather than by counting the same leading-versus-nonlinear separation twice.

## 5. NBL-R2 — The pairwise singularity is cubic, despite quadratic radial stability

**Classification:** an additional analytical limitation within the author's actual geometric family. It strengthens the reason for the existing reference-point qualification; it does not contradict that qualified theorem.

Use exactly the coalescing path in `prop:v3-area-coalescence` and `thm:v4-sequence-stability`: $R$ is fixed, $\alpha=\zeta=0$, and $\beta=s$. Its radii are

$$r(s)=(R+36s,R-18s,R-18s),$$

and its free area is the even function $A(s)=A_0+45\pi s^2/4$. Both signs of sufficiently small $s$ are admissible convex billiards with the same gap. Put

$$\Phi_j(r)=\operatorname{csch}\!\left(j\operatorname{arcosh}(1+g/r)\right),\qquad
C_j(s)=\frac{\Phi_j(R+36s)+2\Phi_j(R-18s)}{A(s)}.$$

The cancellation $C_j'(0)=0$ is already in the paper. On a sufficiently small compact interval, differentiating once more than in the v4 proof gives

$$\sup_{|s|\le s_*}|C_j'''(s)|\le B(1+j)^3e^{-j\gamma_-}. \tag{N3}$$

Indeed, the radius-to-exponent map and $A^{-1}$ have bounded derivatives through order three, and each derivative of $2e^{-j\gamma}/(1-e^{-2j\gamma})$ contributes at most one additional polynomial factor in $j$. The denominator stays uniformly separated from zero.

Taylor expansion of $C_j(s)$ and $C_j(-s)$ through degree two cancels the constant and quadratic terms by subtraction; the linear term is zero. Therefore, for every fixed $0\le a<\gamma_-$,

$$\|C(s)-C(-s)\|_a\le B_a|s|^3,
\qquad \|D\|_a=\sup_{j\ge1}e^{aj}|D_j|. \tag{N4}$$

This is an infinite-sequence estimate, not a finite-prefix observation. The strict exponential margin absorbs $(1+j)^3$.

The cubic order is nonzero already in the first amplitude. One has

$$\Phi_1(r)=\frac{r}{\sqrt{g(g+2r)}},\qquad
\Phi_1'''(r)=\frac{3(3g+r)}{\sqrt g\,(g+2r)^{7/2}}>0.$$

Since $36^3+2(-18)^3=34992$, evenness of $A(s)$ and the zero first derivative give

$$C_1(s)-C_1(-s)=\frac{11664\Phi_1'''(R)}{A_0}s^3+O(s^5). \tag{N5}$$

Thus the norm in (N4) is also bounded below by a positive multiple of $|s|^3$.

The curvature multisets at the two signs are not permutations of one another. Sorting realizes optimal maximum-distance matching in one dimension. For sufficiently small positive $s$, the middle matched pair gives

$$\operatorname{dist}_{\rm match}(\kappa(s),\kappa(-s))
=\frac{36s}{R^2-324s^2}
=\frac{36}{R^2}s+O(s^3). \tag{N6}$$

The negative case follows by symmetry. If a uniform pairwise inverse of exponent $\theta>1/3$ held throughout the neighborhood in the same data norm, (N4) and (N6) would imply $b|s|\le L B_a^\theta|s|^{3\theta}$ for arbitrarily small nonzero $s$, an impossibility.

In particular, the two statements

$$\operatorname{dist}_{\rm match}(\kappa,\kappa_*)\le C\|C-C^*\|_a^{1/2}$$

and

$$\operatorname{dist}_{\rm match}(\kappa,\widetilde\kappa)
\le C\|C-\widetilde C\|_a^{1/2}$$

have substantially different content. The first is the correct v4 theorem; the second is false even along this two-sided path. Equations (N3)–(N6) do not establish an attainable pairwise $1/3$ inverse for the entire neighborhood. They establish an upper limit on any possible uniform pairwise exponent, and an exact cubic example.

**Requested response:** retain the reference-point qualification wherever the sharp exponent is summarized, and preferably include the two-sided-path distinction. Do not describe the radial theorem as a solution of general nearby noisy multichannel recovery. The manuscript already avoids the latter claim; this calculation explains why the qualification is mathematical rather than merely cautious wording. Solving the full pairwise inverse problem was not an unfulfilled demand in OBS-R2 and is not retroactively made one here.

## 6. NBL-R3 — Extrapolation does not cancel the leading timing sensitivity

**Classification:** a quantitative sharpening for the specified estimator, not a minimax lower bound or a missing-cost accusation.

The fixed-order acquisition theorem is valid, including its raw-preparation cost. Its improvement concerns cancellation of powers of a correctly calibrated offset. It does not cancel the error arising from normalization by an incorrect physical offset.

Let $\tau=j\Delta g$ and write $V(d)$ for either normalized physical endpoint variance. The expectation of the extrapolated statistic when denominators use the programmed offsets is

$$\widehat v_{\rm pop}^{[m]}(\tau)
=\sum_{l=1}^m\omega_l\left(1-\frac{\tau}{lh}\right)V(lh-\tau),
\qquad \omega_l=(-1)^{l-1}\binom ml.$$

Differentiation at $\tau=0$ gives

$$\left.\partial_\tau\widehat v_{\rm pop}^{[m]}\right|_0
=-\sum_{l=1}^m\omega_l\left[\frac{V(lh)}{lh}+V'(lh)\right].$$

Since $V(d)=v+O(d)$ with bounded derivative,

$$\left.\partial_\tau\widehat v_{\rm pop}^{[m]}\right|_0
=-\frac{vH_m}{h}+O_m(1),\qquad H_m=\sum_{l=1}^m\frac1l. \tag{N7}$$

Here the exact identity is

$$\sum_{l=1}^m\frac{\omega_l}{l}
=\int_0^1\frac{1-(1-x)^m}{x}\,dx=H_m.$$

Thus the leading $j\Delta g/h$ sensitivity survives extrapolation with a nonzero coefficient. The extra ordinary gap error in the inverse is only of order $|\Delta g|$ and does not generally remove it. This supports the scale $|\Delta g|=O_m(h^{m+1}/j)$ used in the paper for preserving an order-$h^m$ deterministic bias by this normalization rule.

This is a local sensitivity statement for this specific statistic. It does not rule out joint gap estimation, a different estimator, a calibrated external instrument, or cancellation in specially chosen data. It is not a lower bound on every possible experiment. Similarly, the sufficient preparation cost is not a minimax rate, and extrapolation constants are not uniform as $m\to\infty$.

**Requested response:** keep the known-gap assumption next to the accuracy-cost statement, and distinguish preparations used to acquire conditional positions from any separate calibration experiment. Formula (N7) would make the printed timing estimate more informative, but its absence is not a defect invalidating `prop:v4-timing`.

## 7. Novelty, organization, and the requested journal level

### 7.1 What should be treated as the central contribution

The genuine new core is the combination of a small common nonlinear Dirichlet chart, an exponentially accurate relative two-boundary determinant factorization, and its full-phase fixed-offset probability law. The first-pole statement, tied-channel weights, and the fourth-jet scalar example are consequences of that core with different amounts of additional work. They should not be presented as three additional theories of long-time statistics, spectral geometry, and noisy inversion.

The manuscript already makes many of the right qualifications. Those qualifications should not be turned into accusations of claims it never made. They nevertheless leave an importance question. The analysis remains attached to isolated local normal channels, and the concrete inverse gain displayed is one scalar jet parameter. The analytic work is careful, but the applications do not yet reveal a comparably substantial new principle or a problem whose resolution depends in an essential way on this particular uniform nonlinear construction.

A stronger importance case need not be global shape rigidity, an unrestricted limit theorem, or a larger pile of estimates. It could rest on a genuinely reusable formulation of the boundary-factorization mechanism, a nontrivial consequence unavailable from the existing finite calculations, or an exceptionally compelling explanation of why the present uniform statement itself settles a recognized difficulty. These are examples of what an importance argument would need to establish, not mandatory new theorems or a promise of a favorable recommendation. Unsupported enlargement of the claims would make the paper worse.

### 7.2 Primary-literature comparison

The targeted primary-source check supports the broad distinctions now made in `v4/60_comparison.tex`.

Bolotin–Treschev [1] place action Hessians and monodromy determinants in the general discrete-Lagrangian setting. Their primary abstract does not establish the exact relative physical-flux limit claimed here. It would be unfair to dismiss the latter simply by citing Hill's formula.

Bálint–De Simoi–Kaloshin–Leguil [2] recover period-two curvature information and periodic Lyapunov exponents from marked lengths of open dispersing billiards. That is a different datum and geometric setting. Osterman [3] recovers analytic dynamical information near a homoclinic orbit, and the remaining scatterer when two are supplied, from marked length data. His normal-form and asymptotic-series method is a relevant antecedent for nonlinear jets, not a proof of the statistical law in this manuscript.

A particularly relevant comparison missing from the active bibliography is De Simoi–Kaloshin–Leguil [4], which proves marked-length determination of analytic chaotic billiards under symmetry and genericity hypotheses and appeared in *Inventiones Mathematicae*. It should be discussed when situating a higher-jet inverse statement at the requested venue level. Its stronger geometric conclusion does not subsume the present observation, and its additional assumptions must not be suppressed. This is a bibliographic and positioning request, not an accusation of plagiarism or evidence that the new theorem is already known.

This review inspected the cited primary abstract/introduction pages and bibliographic records, not the full proofs of every comparison paper. It did not find an exact antecedent for the complete claimed nonlinear threshold law. This is a targeted check, not an exhaustive priority certificate. No inference from the absence of a search result is used as a proof of novelty.

### 7.3 Exposition and cumulative architecture

The paper now has an identifiable nonlinear center, but still reads partly as the accumulated record of successive referee replies. The presentation repeatedly re-establishes why each older result remains valid and what it does not claim. That is useful in the response letter, but it competes with the mathematical narrative of a research article.

The general threshold theorem, the relative factorization, and the physical limiting law should form one clearly stated main chain. The leading-data saturation and the exact nonlinear example should delimit its information content immediately. The radial inverse and acquisition estimates should be presented as ancillary results, not compensatory claims of separate depth. The circular appendix can retain explicit calculations without repeating the general mechanism as though it were another independent contribution.

No arbitrary deletion of correct results or historical derivations is requested. The repository can preserve them all. Reorganizing what the main article emphasizes is different from retracting mathematics. Neither the number of pages, the number of theorem environments, nor the number of finite diagnostics is evidence of exceptional importance.

## 8. Independent diagnostics and the boundary of this audit

The accompanying `independent_diagnostics.py` was written for this review. It imports no repository code and makes no network calls. Its final version completed **81 of 81 named checks** both normally and under `python -O`; the two JSON outputs were byte-identical. Failure conditions use explicit exceptions, not removable Python assertions.

There are **52 exact**, **25 ordinary floating non-interval**, and **4 high-precision non-interval** checks. The exact group includes direct rational Schur complements for three equal/unequal curvature pairs at lengths 1 through 9, the one-flight derivative, the half-line coefficient, the third radius derivative, Jensen's derivative, and extrapolation and harmonic identities through order 10. The counts describe finite diagnostics, not independently verified theorems.

For the nonlinear check, a Newton solution of the actual local length action is compared with two length-160 approximations to half-line segments. One case has $g=0.4$, curvatures $(1.3,2.1)$, cubic jets $(0.7,-0.9)$, and quartic jets $(3,4)$; another has identical even graphs. Endpoints are $u=0.035$ and $v=-0.027$. The cofactor product and interior LDL determinant compute the relative twist without replacing it by the asserted limit. Selected asymmetric results are:

| Length j | Absolute action-factorization discrepancy | Absolute logarithmic relative-twist discrepancy |
|---:|---:|---:|
| 4 | 7.046e-5 | 8.623e-4 |
| 8 | 8.447e-7 | 1.486e-5 |
| 12 | 1.025e-8 | 2.375e-7 |
| 20 | 1.510e-12 | 5.186e-11 |

The very long finite comparisons reach floating-point cancellation in the determinant calculation. They must not be interpreted as proving an exponential rate beyond that numerical floor. A finite half-line cutoff is not an infinite-operator certificate, and the tests sample only two local graph pairs rather than the whole geometric class.

An independent one-flight quadrature solves the actual radial sublevel boundary and integrates the mixed-derivative flux with its residual-time weight. It uses the local graphs $\psi_s(y)=y^2/2+(3-24s)y^4/24$, which have the relevant fourth-jet variation; it is not a simulation of the full area-compensated global support family. Symmetric differences with parameter step $10^{-4}$ give estimates of $\partial_s\mathcal R_1(0)$ approaching $8/9$:

| Offset d | Estimated first-coefficient shape derivative |
|---:|---:|
| 0.002 | 0.887261685234 |
| 0.001 | 0.888074681571 |
| 0.0005 | 0.888481637151 |

At $d=0.001$, refinement from 96 angular directions and 32 radial nodes to 192 and 48 changes the normalized unperturbed probability by approximately $3.66\times10^{-15}$. This checks numerical consistency, not rigorous quadrature error.

For (N4), high-precision computations use only the first 128 coefficients, $R=1/4$, sequence weight $a=0.4$, and 70 decimal digits. As $s$ decreases from $10^{-4}$ to $10^{-5}$, the weighted prefix discrepancy divided by $s^3$ is approximately $192927.47$ to $192919.07$, while the matching curvature distance divided by $s$ approaches $576$. The infinite-sequence statement rests on (N3), not on that prefix.

The executed environment was Python 3.13.5, NumPy 2.3.5, SciPy 1.17.0, SymPy 1.14.0, and mpmath 1.3.0. The script's Git blob is `2d40e01f32b1464ea8212c0779c0625a8f24b338`; its SHA-256 is `12512e19fc67709671dee1f1e0d643ef2974a761ac4874f010fae20e91ee77fe`. The full generated JSON has SHA-256 `7bae8609c91d37d5b3f82c064e2a07e3a4f3e90328ff2217e267ee186629b26d`. `VERIFICATION.json` records the execution commands, selected outputs, and limitations. The script regenerates the full output; cross-version floating-point byte identity is not promised.

The source audit covered the new v4 mathematical sections, their active v3 foundations, the active circular mathematical appendices, the two-collision companion, the current response and proof ledger, the controlling v3 report's mathematical requests, and the preserved Round 33 chapter. This is not an audit of every historical branch. I did not replay the author's 252-, 257-, 328-, or 411-check suites or the former referee's 594-check suite. I did not rebuild or inspect manuscript PDFs, run remote CI, use interval arithmetic or a formal proof assistant, or simulate the full equilibrium billiard. The author's reported 44-page article and 7-page companion build is not presented as my own executed build. No claim of continuum correctness is inferred from the finite test count.

## 9. Required disposition and final recommendation

A response should address NBL-R1, NBL-R2, and NBL-R3 separately, recognizing their classifications. NBL-R1 asks for a correct comparison between leading, nonlinear, and genuinely long-record information. NBL-R2 asks that the circular-reference estimate not be promoted to a pairwise inverse and supplies an explicit cubic reason. NBL-R3 sharpens the dependence of the specified estimator on physical calibration. The literature and pole-derivative clarifications are secondary requests.

All three controlling OBS requests have received substantive answers. It would be inaccurate to report otherwise. In particular, the half-line determinant and the positive circular-reference estimate are mathematical progress, not rhetorical substitutions. Conversely, inserting the present report's additional calculations, adding further verification receipts, or increasing manuscript length would not by itself reverse the venue recommendation.

The strongest part of the submission is a careful nonlinear relative-flux analysis. The weakest part of its case for the requested journals is the gap between that specialized analytical achievement and the importance of the concrete inverse and statistical consequences used to advertise it. I do not identify a fatal error in the principal theorems, but I remain unconvinced that the present paper reaches the exceptional level of significance required for the requested recommendation.

**Final disposition: reject at the requested top-four level in its present form, on importance and positioning rather than an established fatal mathematical counterexample. Preserve and credit the proved nonlinear progress; do not replace this judgment with an unsupported claim that the main theorem is false, already known, or incapable of further development.**

## Primary references consulted

[1] S. Bolotin and D. Treschev, *Hill's formula*, Russian Mathematical Surveys 65 (2010), 191–257. DOI: 10.1070/RM2010v065n02ABEH004671. Primary abstract inspected: https://arxiv.org/abs/1006.1532.

[2] P. Bálint, J. De Simoi, V. Kaloshin and M. Leguil, *Marked Length Spectrum, homoclinic orbits and the geometry of open dispersing billiards*, Communications in Mathematical Physics 374 (2020), 1531–1575. DOI: 10.1007/s00220-019-03448-x. Primary abstract inspected: https://arxiv.org/abs/1809.08947.

[3] O. V. Osterman, *On length spectrum rigidity of dispersing billiard systems*, Journal of Modern Dynamics 19 (2023), 847–878. DOI: 10.3934/jmd.2023025. Publisher abstract/introduction inspected: https://www.aimsciences.org/article/doi/10.3934/jmd.2023025. Primary preprint: https://arxiv.org/abs/2208.12244.

[4] J. De Simoi, V. Kaloshin and M. Leguil, *Marked Length Spectral determination of analytic chaotic billiards with axial symmetries*, Inventiones Mathematicae 233 (2023), 829–901. DOI: 10.1007/s00222-023-01191-8. Primary abstract and revision metadata inspected: https://arxiv.org/abs/1905.00890v4. Institutional bibliographic record inspected: https://research-explorer.ista.ac.at/record/12877.
