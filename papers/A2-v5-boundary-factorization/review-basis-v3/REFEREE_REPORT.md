# Independent referee report: A2 geometric thresholds and observability, revision v3

## Recommendation: reject at the requested top-four mathematics-journal level in its present form

**Review date:** September 9, 2026 (Asia/Singapore).  
**Reviewer:** GPT-6 Astra Pro. This is an independent AI-assisted assessment requested by the repository owner, not a report commissioned by a journal or an actual journal editorial decision.  
**Author:** Qian Qi.  
**Manuscript:** *Uniform collision thresholds and endpoint curvature recovery in periodic dispersing billiards*.  
**Repository:** `TrillionniumFoundation/theta-theory`.  
**Reviewed branch:** `revision/a2-geometric-thresholds-v3-observability-2026-09-09`.  
**Frozen manuscript commit:** `3f8ad0a5b718818a22c0e2e47378d4d6c93473a1`.  
**Manuscript commit time:** September 9, 2026, 00:05:42 UTC, equivalently 08:05:42 Singapore time.  
**Controlling previous report:** commit `fbe11e631e2e8f19eacff804cebbc5496d1fb822`, report blob `1253acf953e8721bf1b9f5e3a8538d42a30271df`.  
**New review branch:** `review/a2-geometric-thresholds-v3-harsh-independent-2026-09-09`.

Unless otherwise indicated, manuscript locators below are relative to `papers/A2-geometric-thresholds-v3-observability/` at the frozen commit. The review branch preserves that commit as its parent and adds review material only. Result labels, rather than an unverified PDF pagination, identify the mathematical statements.

## 1. Executive judgment

This revision is materially better than v2. It removes the near-circle restriction, proves a geometric localization criterion for arbitrary separated positively curved periodic configurations, places the general boundary-value argument before its circular specialization, and proves a quantitative inverse theorem for two genuinely observable endpoint variances. It also realizes the scalar-amplitude ambiguity by actual analytic obstacles with fixed gap and area. These are mathematical additions, not merely changes of terminology.

The main threshold theorem and the two-variance inverse have survived this audit without an identified in-scope counterexample or fatal proof error. In particular, I do not find a missing factor of two, a parity error in the alternating Hessian, an illegitimate replacement of full phase preparation by a transverse law, or a surviving square-root bias in the centered physical variances. The relative determinant argument is the strongest part of the paper. The finite diagnostics supplied with this report support its algebra and the new covariance normalization; they do not certify the continuum theorem.

Nevertheless, I would not recommend this submission for one of the requested four journals. The newly general geometric class still selects a finite collection of isolated normal period-two mechanisms. The additional inverse theorem, once the endpoint Hessian and its physical realization are established, is an explicit two-variable inversion of its diagonal entries. Its useful uniform conditioning does not imply an increasing amount of leading geometric information at increasing collision order. In fact, the entire selected-channel leading count and endpoint-metric hierarchy is already determined by one-flight data; Section 4.1 below makes this precise. The principal technical achievement remains the common nonlinear chart and relative flux estimate, rather than a new hierarchy of independent inverse invariants.

This is an assessment of the depth and significance demonstrated by this particular manuscript, not a theorem that local results or explicit inverse formulas cannot meet a major journal's standard. I have not found a prior result containing the exact theorem, and I do not assert that it is already known. Nor do I deny that the current material could constitute a worthwhile specialist contribution. The report rejects the requested venue-level recommendation, not the validity or mathematical value of every result in the paper.

The previous report explicitly distinguished requests for concrete improvements from a guarantee of eventual acceptance. Those concrete improvements must now be credited. Repeating the old objections unchanged would be an inaccurate review.

## 2. Disposition of the v2 referee requests

| Previous item | Disposition in v3 |
|---|---|
| GTC-R1: provide a reusable geometric criterion or a substantive observability consequence | Both concrete directions have been implemented. Lemma `lem:g-channels` verifies the criterion from separated positive-curvature geometry; Theorem `thm:v3-tomography` supplies the new observation theorem. The old near-circle scope objection is retired. The importance judgment is reassessed below, not treated as an unchanged defect. |
| GTC-R2: area is not a fourth independent inverse invariant | Addressed explicitly and correctly in `prop:v3-area-coalescence`, including the Fourier area identity and its symmetric dependence on the recovered curvature triple. |
| GTC-R3: coalescence obstructs stable recovery from finite unlabelled amplitude data | The calculation is incorporated. The new stable inverse uses explicitly richer, channel-resolved position data, and includes finite-offset and sampling estimates. This does not solve the original noisy unlabelled problem, but the manuscript does not claim that it does. |
| GTC-R4: realize the product ambiguity and separate general thresholds from the restricted inverse | Addressed by the analytic fixed-area family in `thm:v3-fibers` and by the general unequal-curvature two-variance theorem. Nonminimal own-window selection is kept distinct from ground-onset counts. |
| GTC-R5: attribution, organization, and notation | Substantially addressed. Prony reconstruction and periodic inverse-billiard work are included; the general proof precedes the circular appendices; scalar remainders and endpoint Hessians have different notation. |

No further round should be evaluated as though v3 still lacks these improvements. Conversely, adding the requested examples does not by itself establish the exceptional significance required for the requested venue.

## 3. Audit of the mathematical arguments

### 3.1 Complete-event localization in the enlarged geometric class

**Locator:** `v3/10_geometry_action.tex`, `lem:g-channels`; setup in `v3/00_results.tex`.

The reference configuration has finitely many obstacle representatives and a full-rank lattice. Only finitely many translated pairs can have distance below a fixed bound. Disjoint lifted closures therefore give a positive minimum and a positive gap to pairs outside the reference minimizing set. For a minimizing pair, strict convexity makes its closest displacement and its supporting endpoints unique. In facing graph coordinates, the distance Hessian is

$$\frac1g\begin{pmatrix}1+g\kappa_0&-1\\-1&1+g\kappa_1\end{pmatrix},$$

which is positive definite. Its contacts continue smoothly. A globally shortest segment cannot meet a third obstacle without producing a shorter inter-obstacle distance; local finiteness and disjointness then give positive clearance. These are verified geometric properties, not assumptions that the active event has already localized.

The crucial length-uniform point is also present. Every complete flight has length at least the current minimum gap. A total excess smaller than the common collar bounds each flight's excess separately. The finitely many normal outgoing states are separated, and specular reflection maps a sufficiently short incoming channel into its reverse, not into a different short channel. The same neighborhoods work at each impact. This is an appropriate argument for arbitrary collision order; it does not accumulate a new error constant at every reflection.

The conclusions are local about each fixed configuration, with a compact-family covering interpretation. They are not uniform up to obstacle contact, vanishing curvature, or unbounded higher boundary norms. The manuscript states these restrictions. Infinite horizon elsewhere does not invalidate this short-flight localization.

### 3.2 Alternating Jacobi reduction and the physical multiplier

**Locator:** `v3/10_geometry_action.tex`, `lem:g-jacobi`, `eq:g-effective`, `eq:g-ratio`.

Write

$$c_b=1+g\kappa_b,\qquad c=\sqrt{c_0c_1},\qquad \gamma=\operatorname{arcosh}c,$$

and let $\sigma_i^2=c_{1-(i\bmod2)}$, $D_j=\operatorname{diag}(\sigma_0,\sigma_j)$. The substitution $y_i=\sigma_i z_i$ transforms the whole quadratic action, including its endpoint terms, into the constant-coefficient action. It gives

$$\mathsf H_j=\frac{c\sinh\gamma}{g}D_j^{-1}
\begin{pmatrix}\coth(j\gamma)&-\operatorname{csch}(j\gamma)\\-\operatorname{csch}(j\gamma)&\coth(j\gamma)\end{pmatrix}D_j^{-1}.$$

The endpoint scaling is essential. With it retained, the ratio of the quadratic twist to the square root of the endpoint determinant is exactly $\operatorname{csch}(j\gamma)$ for both parities. At $j=1$ the displayed matrix reduces to the one-flight Hessian above. The two-step transfer trace is $4c_0c_1-2=2\cosh(2\gamma)$, consistently giving the unstable return multiplier $e^{2\gamma}$.

The endpoint eigenvalues remain bounded above and away from zero on the stated compact geometric boxes. The exponentially small object is the mixed endpoint derivative, not the eigenvalue needed to invert the endpoint Morse map. The proof correctly distinguishes them.

### 3.3 The common nonlinear bridge and relative determinant

**Locator:** `v3/10_geometry_action.tex`, `lem:g-relative`, `eq:v3-green`, `eq:v3-cofactor`, `eq:v3-logdet`.

The nonlinear proof is now sufficiently integrated to be checked directly. The Green kernel has exponential off-diagonal decay. Weights $w_i=\rho^i+\rho^{j-i}$ control the endpoint-forced bridge, and their positive powers have sums bounded independently of $j$. Locality of the gradient remainder and bounded neighboring-weight ratios give a contraction on a common endpoint neighborhood. Strict diagonal dominance gives uniqueness throughout the local contact box, not merely in the contraction ball.

For nonsymmetric graphs the gradient remainder is quadratic, the bridge correction is quadratic in endpoint size, and the action correction begins cubically. The revision uses these orders. Parameter derivatives of the Green kernel create polynomial factors in index distances that are absorbed by a strict exponential margin. The differentiated fixed-point equation has the same uniformly invertible left operator; the induction preserves weighted localization. This is the right replacement for differentiating a long initial-value iterate.

Most importantly,

$$-W_{uv}=\frac{\prod_{i=0}^{j-1}b_i}{\det H_{\rm int}},\qquad b_i=-\ell_{uv}(y_i,y_{i+1}),$$

is used multiplicatively. Tridiagonality and endpoint summability give a trace-norm bound on the interior Hessian perturbation, whereas the reference inverse and its fixed parameter derivatives have bounded operator norm. Consequently the logarithmic determinant series costs the trace norm of the perturbation, not the number of interior variables. Differentiated terms retain a trace-class factor. I do not identify a hidden factor of $j$ invalidating the claimed relative estimate.

The even analytic specialization is consistent with the circular cubic bridge correction and quartic action error. Its use in the appendices avoids requiring a separate proof of the general mechanism there.

### 3.4 Full phase measure, radial cancellation, and marked sources

**Locator:** `v3/20_integration.tex`, `eq:g-full-flux`, `lem:g-radial`, proofs of `thm:g-stability` and `thm:g-marked`.

The section normalization and mean roof give physical flux $ds\,dp/(2\pi A)$. First variation cancels the arclength factor in endpoint coordinates, yielding

$$\frac{-W_{uv}}{2\pi A}\,du\,dv\,dr.$$

Almost-everywhere flight-tube coverage, rather than a finite-horizon upper bound, is what this argument needs. The first residual interval has length $d-(W-jg)$ and is shorter than every preceding roof. The remaining time after the last collision is also smaller than the minimum roof. These facts exclude missing end truncations, including for a selected nonminimal channel at its own onset.

Uniform coercivity places the entire active sublevel inside the common Morse chart. The remaining quadratic integral is

$$\int_{|w|^2<2d}(d-|w|^2/2)\,dw=\pi d^2.$$

It gives precisely $d^2/[2A\sinh(j\gamma)]$ for one orientation. Although a general local amplitude has linear terms, the radial domain and weight annihilate its odd part. This explains why the integrated relative correction is $O(d)$ rather than $O(\sqrt d)$. The smooth-even-function argument supplies every prescribed right derivative using sufficiently many boundary derivatives; no unjustified analyticity assumption on a smooth family is needed.

Subtracting the normal-orbit mark separately at each impact leaves a uniformly summable endpoint-localized deviation. The parity formula for the axial sum and positivity prove necessity as well as sufficiency of the stated real source domain. The source series ranges over different onset windows. It is not an unrestricted pressure or characteristic function, and the paper now says so. The second-derivative interface jump is also consistent with differentiating the positive-part square.

### 3.5 Physical endpoint covariance and the stable inverse

**Locator:** `v3/30_observability.tex`, `prop:v3-metric`, proof of `thm:v3-tomography`; theorem statement in `v3/00_results.tex`.

The conditional endpoint density at leading order is $2(1-|z|^2)/\pi$ on the unit disk. Its second moment is $I_2/6$. Substitution of the Morse inverse therefore gives

$$\mathbb E Y=d\,m_j(d),\qquad \frac{\operatorname{Cov}(Y)}d=\frac13\mathsf H_j^{-1}+d B_j(d).$$

The same parity argument justifies the smooth $O(d)$ matrix remainder. Centering is important: the mean need not vanish for a nonsymmetric obstacle, but it is of order $d$ and its square is of order $d^2$.

For physical positions $Q=q+\mathbf t y\pm\mathbf n\psi(y)$, orthogonality removes a cubic term from the squared displacement, and $\psi(y)^2$ starts at fourth order. Thus the centered Euclidean scalar variance really has the corresponding leading diagonal entry. The observable does not secretly require the unknown contact point or tangent.

For odd $j$, inversion of the endpoint matrix yields

$$(v_{j,0},v_{j,1})=
\frac{g\coth(j\gamma)}{3\sinh\gamma}
\left(\sqrt{c_1/c_0},\sqrt{c_0/c_1}\right).$$

The derivative of $F_j(\gamma)=\coth(j\gamma)/\sinh\gamma$ is strictly negative. On a compact positive gap-curvature box its magnitude has positive lower and finite upper bounds independent of $j$. The geometric mean and ratio of two variances then determine the product and ratio of $c_0,c_1$, without division by an exponentially small covariance. Equal curvatures cause no singularity. The nearest-image reconstruction on a compact box also correctly handles data outside the exact image.

This is a valid improvement over the restricted scalar inverse. It is still a local contact-curvature theorem for a specified selected observation, not shape rigidity or a stable inverse for the same unlabelled amplitudes.

### 3.6 Realized fibers and the sampling estimate

**Locator:** `v3/30_observability.tex`, `thm:v3-fibers`, `prop:v3-sampling`.

The rectangular-lattice construction verifies more than an algebraic change of two curvature jets. The support perturbations have the required zero and first jets at the two horizontal contacts, independently change the two second jets, and admit an area compensator with zero second jets there. Its area derivative is $3\pi/4$, so the analytic implicit-function theorem applies. Positive curvature, separation, and the strict gap to all nonhorizontal pairs persist in a sufficiently small parameter interval.

The resulting family has fixed $g=1$, fixed $A=12-\pi$, and $c_0c_1=4$. Its complete leading ground-count hierarchy is therefore fixed, whereas the ordered variance ratio is $e^{2s}$. The paper correctly avoids asserting equality of finite-offset remainders or of all billiard data. Reversing the oriented channel reverses the endpoint ordering; this is not an unlabelled reconstruction of the sign of an oriented parameter.

The paired-position estimator is unbiased. Coercivity gives a diameter of order $\sqrt d$, so division by $2d$ leaves uniformly bounded summands. The exponential concentration bound follows from independent successful preparations, not independent successive impacts. The expected raw-preparation cost is correctly obtained by dividing the required number of successes by the rare event probability. The paper expressly charges that cost. It would be unfair to report that it forgot the exponentially rare conditioning.

### 3.7 Retained inverse, response, circular results, and companion

**Locators:** `v3/40_inverse.tex`, `v3/50_record_response.tex`, the circular inputs in `main.tex`, `two_collision.tex`, and `history/round33_A2.tex`.

The equal-gap support family has exact, not merely first-order, equal gaps. Odd-index Möbius inversion is absolutely convergent. The ensuing positive finite-exponential-sum recovery handles repeated nodes by rank rather than by inverting a singular three-node Vandermonde matrix. The area formula and the circular first-order cancellation are correct. Exact infinite-data identification is not being represented as finite-noisy-data stability.

The smooth record response uses a maximum norm and operator-norm bounds on the test derivatives, so growing record dimension does not silently change its hypotheses. It differentiates a common parametrization and density, not a total-variation inequality on different physical surfaces. The moving-cut formula includes its boundary term and requires a strict transversality margin. Fixed physical schedules can carry factors $k/d$; the paper does not assert uniform response for arbitrary discontinuous decoders.

The circular normalization, matched-independent-roof exponent comparison, multiplier identity, and Lambert-series interpretation are consistent with the general formulas. I also read the complete fixed-window two-collision companion and the preserved Round 33 arithmetic/Fourier chapter. The former is a separate regular-window calculation; the latter explicitly conditions its Fourier inversion on mechanical estimates not proved here. The current paper does not use those missing long-time estimates as established premises. Their absence is not a counterexample to its onset theorem.

## 4. New substantive assessments

### OBS-R1 — The leading inverse hierarchy saturates at one flight

**Classification: exact information-content calculation and major editorial assessment; not a contradiction of the theorems.**

The manuscript emphasizes recovery at every odd collision order. This is true, but the role of the order-uniform theorem should be separated from the number of independently recoverable quantities.

Fix one oriented selected channel and set

$$a_j=\lim_{d\downarrow0}d^{-2}\Pr(E_{j,e}(d))=\frac1{2A\sinh(j\gamma)}.$$

At $j=1$, the two limiting physical variances are simply

$$(v_{1,0},v_{1,1})=\frac{g}{3(c_0c_1-1)}(c_1,c_0). \tag{R1}$$

At known $g$, these already determine the ordered pair $(c_0,c_1)$. Indeed, with $P=3\sqrt{v_{1,0}v_{1,1}}/g$, one has $P=c/(c^2-1)$, and hence

$$c=\frac{1+\sqrt{1+4P^2}}{2P},\qquad
\frac{c_0}{c_1}=\frac{v_{1,1}}{v_{1,0}}.$$

Consequently every odd-order variance pair satisfies

$$v_{j,b}=v_{1,b}\frac{\coth(j\gamma)}{\coth\gamma},\qquad b=0,1, \tag{R2}$$

and every leading probability coefficient satisfies

$$a_j=a_1\frac{\sinh\gamma}{\sinh(j\gamma)}. \tag{R3}$$

If the normalizer is also to be identified, $a_1$ gives $A=[2a_1\sinh\gamma]^{-1}$. The complete leading endpoint matrix at either parity is likewise determined by the displayed Jacobi formula once $g,c_0,c_1$ are known. Thus the selected-channel leading count and endpoint-metric hierarchy factors through the four scalar data $(g,a_1,v_{1,0},v_{1,1})$. Without count amplitudes, all odd variance pairs factor through $(g,v_{1,0},v_{1,1})$.

These statements concern one selected channel and leading coefficients only. They do not assert that two unlabelled amplitudes identify a multichannel configuration, that higher boundary jets are determined, or that finite-offset laws are fixed by these data. They also do not make the long-bridge probability theorem redundant: a common collar, relative remainder, and differentiated bounds at arbitrary order are much stronger than a one-flight asymptotic.

They do, however, show why the inverse consequence has less depth than the phrase “at every odd collision order” might suggest. There is no accumulation of new leading inverse coordinates with collision order. Once physical covariance is linked to the inverse Hessian, the reconstruction itself is a two-dimensional algebraic calculation. The uniformity preserves access to the same contact data at long order; it does not supply a progressively richer leading geometric hierarchy.

The main significance case must therefore rest on the relative nonlinear calculus and a demonstrably substantial consequence of it. The additional admissible shapes, the elementary inverse map, and its repeated availability at many orders should not be counted as three separate deep advances. The manuscript acknowledges much of this mechanism, but its current organizing conclusion still does not persuade me that the technical achievement reaches the requested venue threshold.

**Requested disposition:** state the saturation identities near the inverse discussion and make an explicit case for what collision-order uniformity accomplishes beyond preservation of those same leading data. This is not a request to delete the correct uniform theorem or to add an unsupported global rigidity claim.

### OBS-R2 — Infinite absolute-amplitude data retain the coalescence degeneracy

**Classification: a strengthened analytical limitation, proved here in a specified topology; not a falsity finding.**

The manuscript establishes first-order loss for every fixed finite amplitude vector. The same loss persists for the whole sequence in a range of natural exponentially weighted absolute-error norms. Making this explicit would prevent “exact infinite identification” from being mistaken for removal of the instability by simply observing larger orders.

Use the paper's admissible path with fixed $R$, $\alpha=\zeta=0$, $\beta=s$. Its radii are $R+36s,R-18s,R-18s$, and

$$C_j(s)=\frac{\Phi_j(R+36s)+2\Phi_j(R-18s)}{A(s)},\quad
\Phi_j(r)=\operatorname{csch}\!\left(j\operatorname{arcosh}(1+g/r)\right),$$

where $A(s)=A(0)+45\pi s^2/4$. Choose a sufficiently small closed admissible interval $|s|\le s_0$, and let $\gamma_->0$ be a lower bound for all three corresponding exponents on that interval. For any fixed $0\le a<\gamma_-$, equip amplitude differences with

$$\|\Delta C\|_a=\sup_{j\ge1}e^{aj}|\Delta C_j|.$$

Differentiating $\operatorname{csch}(j\gamma)=2e^{-j\gamma}/(1-e^{-2j\gamma})$ twice, with the radius and area functions ranging over a compact positive interval, gives

$$\sup_{|s|\le s_0}|C_j''(s)|\le B(1+j)^2e^{-j\gamma_-}. \tag{R4}$$

The already established identity $C_j'(0)=0$ then gives, by Taylor's integral remainder,

$$\|C(s)-C(0)\|_a\le B_a s^2. \tag{R5}$$

Indeed, the supremum of $(1+j)^2e^{-(\gamma_--a)j}$ is finite. On the other hand, the matching distance of the curvature multiset from the circular triple is bounded below by $b|s|$. A locally Hölder inverse of exponent $\theta>1/2$ in this data norm would imply

$$b|s|\le L\|C(s)-C(0)\|_a^\theta\le L B_a^\theta|s|^{2\theta},$$

which is impossible as $s\to0$ through nonzero values. The same upper-bound argument applies to finite weighted sequence norms with a strict exponential margin.

This does not disprove exact injectivity. It does not establish a matching one-half-Hölder upper stability theorem, and it is not a statement about every conceivable relative-error topology. It is a precise limitation of the retained unlabelled inverse under the stated absolute-amplitude noise model, even when every order is included.

The new position observation resolves a different problem. Its Lipschitz result is genuine precisely because it retains a channel label and two endpoint statistics discarded by the scalar datum. This is not an algebraic regularization of the same observation.

**Requested disposition:** keep the different data spaces separate, and either incorporate this sequence-level strengthening or explicitly explain why the paper elects to discuss only finite vectors. A full solution of all noisy multichannel inverse problems is not being made a prerequisite for correctness of the current theorem.

### OBS-R3 — Conditional conditioning is not the experimental accuracy-cost relation

**Classification: quantitative interpretation of the stated estimator and its hypotheses; not an omitted-cost accusation or a minimax lower bound.**

Proposition `prop:v3-sampling` correctly gives error at most

$$C\left[d+\sqrt{\log(4/\eta)/K}\right]$$

after $2K$ independent successes, at confidence $1-\eta$, with expected raw-preparation cost comparable to $K d^{-2}e^{j\gamma}$. To make this particular guarantee of order $\epsilon$, choose $d$ proportional to $\epsilon$ and $K$ proportional to $\epsilon^{-2}\log(4/\eta)$. The resulting sufficient expected cost scales as

$$e^{j\gamma}\epsilon^{-4}\log(4/\eta). \tag{R6}$$

This is a consequence for the proposed stop-after-success experiment, not an optimality result and not by itself a fixed-budget high-probability bound on the number of raw preparations. Better estimators, bias cancellation using multiple offsets, or other measurements are not ruled out. Equation (R6) simply states the actual accuracy-cost meaning of the given proposition.

Together with (R2), it also shows that the manuscript has not established a statistical advantage of using high collision order for these leading contact parameters. The conditional inverse remains well conditioned while the acquisition cost worsens exponentially. That distinction is already acknowledged; its explicit accuracy dependence should accompany any claim of practical or quantitative observability.

There is a related reason to retain the known-offset qualification prominently. Suppose the programmed window is $t=j\widehat g+d_0$, but $g=\widehat g+\Delta g$. The actual offset is $d=d_0-j\Delta g$. If the observed physical variance is normalized by $d_0$ rather than the unknown $d$, its leading value is multiplied by $d/d_0$. In the regime $|j\Delta g|\le d_0/2$, this introduces an error of order $j|\Delta g|/d_0$, in addition to the finite-offset bias. To preserve an order-$d_0$ bias by this direct normalization, accuracy $|\Delta g|=O(d_0^2/j)$ is sufficient. The manuscript explicitly does not promise a cost-free timing change; the calculation explains why that caveat matters.

**Requested disposition:** state an accuracy-cost corollary such as (R6), retain the known-gap/window and independent-preparation assumptions, and do not equate uniform conditional inverse constants with uniform experimental efficiency. These clarifications do not invalidate the theorem as printed.

## 5. Literature and priority assessment

The updated comparisons are substantially appropriate. The targeted primary-source check in this review did not identify a theorem already containing the exact full-phase, collision-order-uniform onset law and two-variance realization here. This is not an exhaustive priority certificate.

Bolotin and Treschev [1] provide the relevant classical variational Hessian/monodromy framework. That background does not by itself supply the relative nonlinear flux estimates proved in this manuscript. Bálint, De Simoi, Kaloshin and Leguil [2] recover period-two curvature information and periodic Lyapunov data from marked lengths in an open three-obstacle setting. Their data and ambient class differ from the conditional variance experiment.

Carney, Nicol and Zhang [3] treat periodic-point extreme-value and compound-Poisson limits for billiard maps, with a dynamically adapted metric and derivative-dependent clustering. The long-observation shrinking-target regime is not the present maximal-count onset experiment. I checked their primary HTML statements of Theorems 1 and 2 and the finite/infinite-horizon application discussion; this supports, rather than overturns, the distinction now made by the manuscript.

Batenkov and Yomdin [4] are an appropriate source for the Prony reconstruction and local regular-point conditioning context. Their local analysis exposes node-separation dependence; it does not give a uniformly regular inverse at colliding nodes for the unlabelled observation. I checked the local-accuracy discussion in the primary HTML rendering. That rendering uses sequential theorem numbering, so this review does not claim an additional PDF verification of the manuscript's precise theorem-number locator.

Finamore and Leguil [5], in the version pinned by the manuscript, prove an isometry conclusion for diffeomorphic finite-horizon Sinai tables with the same enriched marked length spectrum. The enriched datum includes limits from approximating geodesic flows. I checked Theorem A and the defining introductory discussion. Their conclusion is global and their datum different. The present theorem permits infinite horizon but only recovers local contact curvatures from another observation. Neither result should be presented as automatically supplying or subsuming the other.

Thus the previous attribution omissions are not valid grounds for rejecting v3 unchanged. The remaining objection is the mathematical importance demonstrated after the classical mechanisms and the genuinely new uniform estimates have been separated.

## 6. Independent diagnostics and limits of this audit

The accompanying `diagnostics.py` was written for this review, imports no repository code, and makes no network calls. It completed **594 of 594** named checks in ordinary Python and under `python -O`. The generated JSON outputs were byte-identical. Explicit conditions, not removable Python assertions, determine failure.

The checks comprise **288 exact-rational**, **23 exact-symbolic**, **277 ordinary non-interval numerical**, and **6 high-precision non-interval numerical** checks. Exact rational elimination tests four alternating-curvature inputs at lengths 1 through 12 and 31, 32, 63, 64, 127, 128. It compares Schur complements, positivity, relative twist, parity, and the one-flight saturation identities. The inverse diagnostics include equal and unequal curvatures and odd lengths through 1025. The smallest sampled Jacobian singular value is approximately 0.0097734; this is a finite-sample diagnostic, not a certified infimum on the theorem's compact boxes.

Symbolic checks verify the support jets, their Fourier representations, and the area-compensator derivative. Numerical fiber samples verify the implicit area correction and evaluate curvature radii at 4096 angles; this sampling does not replace the analytic openness argument. High-precision amplitude calculations test a finite prefix of the weighted coalescence behavior. The infinite-sequence conclusion in Section 4.2 rests on (R4), not on that finite prefix.

For an independent nonlinear check, the program integrates the exact one-flight sublevel using

$$\psi_b(y)=\kappa_b y^2/2+a_b y^3/6+b_b y^4/24,$$

with $g=0.4$, curvatures $(1.3,2.1)$, cubic jets $(0.7,-0.9)$, and quartic jets $(3,4)$. It solves the radial sublevel boundary, includes the exact mixed-derivative flux and residual-time weight, and computes the centered two-dimensional physical position variances. It does not substitute the predicted covariance as the integration density. The predicted limits are approximately $(0.136539032354,0.112793113684)$.

| Offset d | Probability divided by its leading term | First physical variance divided by d | Last physical variance divided by d |
|---|---:|---:|---:|
| 0.001 | 0.998547343032 | 0.136527414085 | 0.112778256399 |
| 0.0003 | 0.999563695650 | 0.136535547576 | 0.112788655346 |
| 0.0001 | 0.999854516824 | 0.136537870828 | 0.112791627461 |
| 0.00003 | 0.999956349963 | 0.136538683903 | 0.112792667805 |

The corresponding variance biases divided by $d$ approach approximately $-0.011615$ and $-0.014863$. Coarse and refined quadratures agree within the explicit diagnostic tolerance. These are local one-flight, non-interval calculations, not a simulation of the complete equilibrium billiard or a nonlinear arbitrary-length proof.

Execution used Python 3.13.5, NumPy 2.3.5, SciPy 1.17.0, and SymPy 1.14.0. The script's Git blob is `2debdcf5a89683734c161ab25e452fc1fd4c95e4`; its SHA-256 is `aae78c0c4344eb35394392939c3fd00145fbd0c8d5e81c8f316a44ecc26a1c14`. The full output has SHA-256 `a6d4394ee03a0266e2ad980e90e413ee79a714298a57139db978b8a5a0932624`. The committed `verification.json` records the commands, environment, counts, selected numerical output, and limitations. Running the script regenerates all named checks. Cross-version floating-point byte identity is not promised.

I read the active mathematical source closure of `main.tex`, the complete two-collision companion, the controlling review, the current response, the author validation summary, and the preserved Round 33 chapter. I did not independently replay the author's 257-, 328-, or 411-check suites or the prior referee's 241-check suite. I did not rebuild or inspect the manuscript PDFs, run remote CI, perform an interval proof, use a formal proof assistant, or audit every historical source branch. The author's 31-page plus 7-page build claim is not presented as my own executed build. None of these unperformed tasks is concealed by the independent test count.

## 7. Required response and final recommendation

A further response should address OBS-R1, OBS-R2, and OBS-R3 separately, distinguishing an exact calculation from a correction to a false statement and both from editorial judgment. It should identify what new information is present in each observation, what is already determined at one flight, and what collision-order uniformity adds analytically. It should also state the acquisition model alongside the inverse stability statement.

No arbitrary deletion of established mathematics is requested. No unsupported long-time theorem, global rigidity claim, or general noisy-data assertion should be added merely to make the paper sound broader. In particular, the original Fourier programme is not a substitute for a proved consequence of the current theorem. Conversely, the saturation and cost calculations above should not be used to retract a correct uniform result: they calibrate its information content and interpretation.

The manuscript has successfully answered most concrete requests from the previous report. My remaining negative recommendation is therefore not based on an uncorrected algebraic gap. It is based on the limited conceptual reach of the additional inverse result relative to the central local relative-flux construction. Merely adding (R1)–(R6), more verification records, or more theorem labels would clarify the article but would not, by itself, reverse that judgment. A successful importance argument would have to explain why the existing uniform mechanism, or a genuinely deeper proved consequence of it, merits the requested general-journal prominence. This is not a demand for any particular unproved extension or a promise of acceptance after another checklist.

**Final disposition: reject at the requested top-four level in the present form. Substantial mathematical progress is credited; no fatal counterexample to the principal threshold or two-variance theorem has been established in this review.**

## Primary references consulted

[1] S. Bolotin and D. Treschev, *Hill's formula*, Russian Mathematical Surveys 65 (2010), 191–257. DOI: 10.1070/RM2010v065n02ABEH004671. Primary abstract inspected: https://arxiv.org/abs/1006.1532.

[2] P. Bálint, J. De Simoi, V. Kaloshin and M. Leguil, *Marked Length Spectrum, homoclinic orbits and the geometry of open dispersing billiards*, Communications in Mathematical Physics 374 (2020), 1531–1575. DOI: 10.1007/s00220-019-03448-x. Primary abstract inspected: https://arxiv.org/abs/1809.08947.

[3] M. Carney, M. Nicol and H.-K. Zhang, *Compound Poisson law for hitting times to periodic orbits in two-dimensional hyperbolic systems*, Journal of Statistical Physics 169 (2017), 804–823. DOI: 10.1007/s10955-017-1893-9. Primary text consulted: https://arxiv.org/html/1709.00530v1, Theorems 1–2 and the application discussion. Rendering dates are not treated as new research-publication dates.

[4] D. Batenkov and Y. Yomdin, *On the accuracy of solving confluent Prony systems*, SIAM Journal on Applied Mathematics 73 (2013), 134–154. DOI: 10.1137/110836584. Primary text consulted: https://arxiv.org/html/1106.1137v3, introduction and Section 4; bibliographic version checked at https://arxiv.org/abs/1106.1137.

[5] D. Finamore and M. Leguil, *A CAT(0)-approach to the marked length spectral rigidity of Sinai billiards*, arXiv:2510.18983v1, October 21, 2025. Primary text consulted: https://arxiv.org/html/2510.18983v1, enriched-spectrum definition and Theorem A. The arXiv version history was checked; no later journal-publication claim is made.
