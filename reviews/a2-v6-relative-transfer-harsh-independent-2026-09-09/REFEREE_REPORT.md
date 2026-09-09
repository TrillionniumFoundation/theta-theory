# Independent referee report on A2 v6
## Relative boundary laws and statistical reconstruction in periodic dispersing billiards

**Recommendation: reject in its present form at the requested top-four general mathematics-journal level.** This is principally an editorial judgment of demonstrated significance, not a finding that the central theorem is false. The new proof chains examined below survive this audit without an identified fatal error. The concrete mathematical and observation-model requests from the preceding reports have, substantially, been answered.

**Date:** September 9, 2026 (Asia/Singapore).  
**Author:** Qian Qi.  
**Reviewer:** GPT-6 Astra Pro. This is an independent AI referee-style assessment requested by the repository owner, not a journal-commissioned report, an editorial decision, a human referee's endorsement, or a formal proof certificate. The preceding reports were consulted; this is not a blinded assessment. The calculations and diagnostic script supplied with this report were developed independently of the author's and earlier referees' diagnostic code.

**Repository:** `TrillionniumFoundation/theta-theory`.  
**Reviewed branch:** `revision/a2-v6-relative-transfer-count-experiments-2026-09-09`.  
**Frozen submission commit:** `4ca186258c92dcbc75accc4eb576e307cc612189`.  
**Frozen root tree:** `526ce687250f81887cd93b8d7444532f07225502`.  
**Commit timestamp:** September 9, 2026, 09:24:22 UTC / 17:24:22 Singapore.  
**Manuscript directory:** `papers/A2-v6-relative-transfer-count-experiments/`.  
**New review branch:** `review/a2-v6-relative-transfer-harsh-independent-2026-09-09`.  
**Review directory:** `reviews/a2-v6-relative-transfer-harsh-independent-2026-09-09/`.

Unless otherwise stated, every source path and LaTeX label below refers to that manuscript directory at the frozen commit. Source labels, not independently unverified PDF page numbers, are the controlling locators. This review adds review material only; it does not amend the author's text.

## 1. Submission identity and the status of the previous objections

There is now a materialized v6 manuscript. It would be incorrect to repeat the preceding report's finding that the branch then called v6 contained only the old manuscript and a review. Three different v6 branch names were inspected. The `relative-laws-calibrated-count-rigidity` branch still pointed to the old review commit `9975aa037d5d9eb1f339b9220f9cd21fb54c0876`. The `relative-locality-count-recovery` branch had an earlier tip, `be05c252d13463c4204e02da86d3fe9a6659f3d1`, whose commit message explicitly described an unverified partial revision. The selected `relative-transfer-count-experiments` branch contains the full revision and has the later inspected tip above. Branch names alone were not used to identify the submission.

The author index identifies mathematical-source commit `17a0d236d4eb70595254abcf107013eef5a9e115`. The frozen tip adds a clean-build record explaining that the companion must be built before the article because of the external-reference auxiliary file. The reported 63-page article and seven-page companion are author build claims; this review did not independently rebuild or inspect those manuscript PDFs.

The controlling historical reports are the report at `9975aa037d5d9eb1f339b9220f9cd21fb54c0876`, under `reviews/a2-v5-statistical-contact-rigidity-harsh-independent-2026-09-09/`, and the subsequent report at `0421836a5868967f90093281c7ca43aab9815a0d`, under `reviews/a2-latest-materialized-second-harsh-2026-09-09/`. Their principal materialized author baseline was v5 commit `1e57d9c024f90f0304e5572c0e320707bab88074`.

| Previous issue | Disposition in the actual v6 |
|---|---|
| SCR-R1: actual versus effective channel curvatures | Answered. Equal facing curvatures are stated next to the scalar geometric inverse, and the effective-curvature formula is printed for the nonsymmetric case. |
| SCR-R2: exact germs, coefficient conditioning, and finite-flight recovery | Answered at the claimed level. `thm:v6-finite-jets` supplies a uniform-in-flight inverse at each fixed jet order. The one-flight/limiting sensitivity comparison is explicit and is not advertised as an infinite-order or minimax theorem. |
| SCR-R3: three physical parameters versus independent area | Answered. `thm:v6-three` proves the constrained physical three-amplitude inverse near the specified circle, while the four-amplitude theorem retains its independent-normalizer interpretation. |
| SCR-R4: raw unlabelled counts versus selected positions | Substantially answered by a new experiment, not merely a disclaimer. `thm:v6-count-only` composes fine calibration, raw-count amplitude estimation, and the coalescing inverse, with its own preparation bound. |
| SCR-R5: relative mechanism and literature | The concrete presentation and bibliographic requests are answered. The introduction centers the relative law, and `thm:v6-transfer` gives a genuine experiment-level consequence. Whether that consequence makes the case for the requested venue convincing remains an editorial question, not an unchanged proof defect. |
| Horizontal versus all-channel preservation | Answered. The channel index is retained in the advertised realization, and the vertical-channel check is included. |
| The earlier unmaterialized-v6 pointer | Closed for this selected branch. It is a historical submission-state finding, not a criticism of this manuscript. |

These resolutions must remain closed unless a new, specific counterargument is supplied. In particular, the report does not ask the author to solve arbitrary-itinerary dynamics, prove stable global analytic continuation, or establish global minimax optimality merely to satisfy an expanding list of requests.

## 2. Overall assessment

The most substantial analytical result is the collision-order-uniform relative two-boundary law. Its important distinction is between a uniformly positive endpoint Hessian and an exponentially small endpoint twist. Controlling the first does not automatically give relative control of the second. The manuscript actually addresses that distinction, then integrates the correct physical residual-time measure.

V6 now has two coherent consequences that deserve more credit than their v5 predecessors. First, it compares finite and boundary experiments on a common observable space and retains the rare-event mass when failures are restored. Second, it supplies a single, genuinely count-only procedure for the unordered curvature triple, including fine timing calibration. The former is not merely convergence of formal coefficients; the latter is no longer a juxtaposition of an amplitude inverse and an unrelated position-sampling rate.

The finite-flight diagonal is also useful. Its positive endpoint contribution proves that intermediate flight lengths do not produce a hidden zero of a fixed-order inverse Jacobian. The constrained three-amplitude calculation is correct and appropriately local. Neither should be dismissed because an earlier referee suggested its formula; the response gives a proof and the needed quantifiers.

I nevertheless do not recommend publication at the requested venue on the present showing. The difficult relative mechanism is still a local alternating-channel mechanism. The raw-count acquisition theorem uses a fixed finite set of flight numbers, whereas the growing-experiment comparison is a different asymptotic statement. Consequently the strongest new statistical reconstruction theorem is not itself an application requiring the long-bridge limit. This is not a logical inconsistency: the manuscript now says so sufficiently clearly. It does mean that the two advances should not be counted as a single, stronger reconstruction theory whose force comes from increasing record length.

The finite-jet and analytic uniqueness results have the same issue of interpretation. Their exact information is already present in the one-flight nonlinear germ within the identical-even class. The long-bridge law supplies uniformity and a limiting physical description, not additional identifiable contact coordinates in that class. The specialized finite-dimensional coalescence calculation and calibration procedure are valuable, but do not by themselves establish exceptional general mathematical significance.

This is a judgment about the significance case actually presented, not a theorem about the limits of the program. No earlier source found in the targeted comparison below is asserted to contain the complete relative physical law. Locality, symmetry in an inverse application, or an elementary last step is not independently a reason for rejection. The author need not discard correct results or dilute the general forward theorem. The following audit and two additional calculations state precisely what survived and what the results mean.

## 3. Mathematical audit of the principal proof chains

### 3.1 Geometry, stationary segments, and physical normalization

**Locators:** `v3/10_geometry_action.tex`, `lem:g-channels`, `lem:g-jacobi`, `lem:g-relative`; `v3/20_integration.tex`, `lem:g-radial`, proof of `thm:g-stability`.

The shortest-pair reduction is valid for the printed periodic, positively curved configuration, not just for a near-circle perturbation. Bounded obstacle representatives and periodicity leave finitely many candidate short pairs. Strict convexity gives unique closest support points. The distance Hessian is positive definite. A shortest segment cannot encounter a third obstacle first, and its positive clearance persists in small contact neighborhoods.

The uniformity in the number of flights is properly earned: if the sum of the flight excesses is small, every individual excess is small because every complete flight has length at least the minimum gap. Separated outgoing normal states and reflection then force the same alternating channel. There is no successive shrinking of the collar by a factor depending on the flight number. A nonminimal clear channel is treated as a selected itinerary at its own onset, not as the complete count event there.

For unequal facing curvatures, the alternating scaling is retained. With

$$c_b=1+g\kappa_b,\qquad c=\sqrt{c_0c_1},\qquad \gamma=\operatorname{arcosh}c,$$

the endpoint Hessian has uniform positive eigenvalue bounds, while the reference mixed derivative contains the factor $\operatorname{csch}(j\gamma)$. The weighted Green construction controls the stationary segment by two summable endpoint layers. The cofactor identity is

$$-W_{uv}=\frac{\prod_i[-\ell_{i,uv}]}{\det H_{\mathrm{int}}}.$$

Its relative logarithm is controlled by a summable edge product and a trace-class perturbation of the interior Hessian. Tridiagonality and localization bound the sum of matrix entries; the proof does not use the invalid replacement of that estimate by a dimension-dependent operator bound.

The first-impact phase measure is $(-W_{uv})\,du\,dv\,dr/(2\pi A)$. The allowed residual interval is shorter than the preceding roof, and the remaining terminal time cannot accommodate another hit. Thus the residual-time integral is the actual full-phase preparation. The Morse construction inverts the positive endpoint Hessian, not the small twist. Odd terms cancel under the radial integral, giving smooth right offset derivatives without assuming even boundary graphs. I identify no fatal gap in these steps under the stated compact-family hypotheses.

### 3.2 The relative limit and its derivatives

**Locators:** `v4/10_boundary_layers.tex`, `lem:v4-halfline`, `thm:v4-factorization`, `thm:v4-law`; `v5/15_differentiated_operators.tex`.

The half-line action and edge-product sums are absolutely summable. The amplitude is defined by a relative Fredholm determinant with a specified logarithm, not by an unspecified infinite determinant normalization. The gluing residual has small summable norm; diagonal dominance controls the correction to the finite stationary segment.

For the determinant comparison, the first and last blocks are separated before comparison with half-line Green kernels. The discarded perturbation has exponentially small trace norm. Cross-block Green entries are exponentially small, while each retained block converges to its half-line counterpart. Telescoping powers in the logarithmic determinant retains one trace-class factor. Differentiated factors need bounded norms, not small norms; the v5 addendum states this correctly. Fixed polynomial losses are absorbed by a strict exponential margin.

The probability comparison down to offset zero uses common Morse coordinates and extra endpoint derivatives. It is not formal differentiation of a moving indicator. The actions differ quadratically at zero, an essential fact used again in v6. The limiting density factors before the residual-energy constraint, but the resulting conditional probability is not a product of independent endpoint laws. The first-pole consequences concern different physical windows at different coefficients; they are not pressure statements for all itineraries.

### 3.3 New transfer to physical experiments

**Locator:** `v6/10_experiment_transfer.tex`, `thm:v6-transfer` and its risk corollary.

In scaled endpoint/residual coordinates, the successful subprobabilities have a common scalar prefactor proportional to $d^2[-W_{uv}(0)]$ and densities

$$b_j(\sqrt d\,z)\mathbf1_{\{s\ge0,\ s+E_j(\sqrt d\,z)/d<1\}}$$

and the corresponding boundary expression. Their support lies in a common bounded set. The action estimate with quadratic vanishing gives

$$|E_j(\sqrt d\,z)-E_\partial(\sqrt d\,z)|/d
\le C\tau^j|z|^2.$$

At fixed $z$, the two residual intervals have the same lower endpoint. Their symmetric-difference length is controlled by the difference of their upper endpoints. Integrating this and the amplitude error proves the claimed relative subprobability bound. Dividing by uniformly positive normalized masses gives the conditional total-variation estimate. Adding the failure atom preserves the rare-event factor.

Thus, with $p_{j,d}\asymp d^2e^{-j\gamma}$, the product bound $\min\{1,Cnp_{j,d}\tau^j\}$ follows for raw preparations, while $k$ conditional successes cost $\min\{1,Ck\tau^j\}$. The risk statement for bounded losses follows from total variation. For deterministic physical schedules, one compares at the parameter's actual excess; no supplied unknown gap is thereby smuggled into the estimator.

The same physical embedding at each parameter must be applied to both compared laws. This suffices for the displayed family-wise comparison and common-observation decision rules. It is not a construction of an arbitrary parameter-free simulator, and it does not extend total variation to full embedded growing collision arrays. The manuscript explicitly retains bounded-Lipschitz control for those arrays. Section 4 below independently checks the support mechanism and shows that linear accumulation in the number of successful observations can be sharp.

### 3.4 Contact jets and the finite-flight inverse

**Locators:** `v5/20_contact_rigidity.tex`; `v6/20_finite_jet_stability.tex`, `thm:v6-finite-jets`.

The finite-degree argument is indispensable and present. The coefficient of $d^{m-1}$ uses the stationary action through degree $2m$ and the amplitude through degree $2m-2$. At fixed lower even jets, the first varying local length term is $(u^{2m}+v^{2m})/(2m)!$; it has zero mixed derivative. The action and interior determinant therefore contribute separately, and neither may be dropped.

In the notation of the revision, the finite diagonal is

$$-\partial_{q_{2m}}f_{j,m-1}
=\alpha_m\left(\sum_{i=0}^j w_i\nu_i^m
+4m\sum_{i=1}^{j-1}G_{ii}\nu_i^{m-1}\right),
\qquad \alpha_m=\frac{2}{2^m(m+1)(m!)^2}.$$

Both terms have the displayed sign. The endpoint terms alone give the uniform lower bound $2\alpha_m/a^m$, where $a=\sinh\gamma/g$. The empty interior sum at one flight reproduces the one-flight formula. Summable end layers give the half-line diagonal. Independent exact checks of the finite quadratic forms also give the useful identity

$$\nu_i=\frac{\cosh((j-2i)\gamma)}{a\sinh(j\gamma)}.$$

At each fixed finite order the coefficient dependence can be represented by local polynomial graphs, and the forward derivatives have common bounds on the chosen compact set. Together with the nonzero triangular diagonal this supplies the claimed inverse bounds uniform in $j$. Merely invoking the inverse-function theorem separately for each $j$ would not have sufficed; that is not what the new argument does.

The analytic-boundary conclusion remains exact germ uniqueness in the identical-even class. Analytic continuation of the arclength curvature function and the common initial frame identify participating boundary images, not an unknown lattice or unseen obstacles. Finite-dimensional area-compensated realizations are legitimate. Their preserved leading hierarchy is the selected horizontal one. The sensitivity ratio asymptotic to $(\tanh\gamma)^m$ concerns one diagonal with lower jets fixed, not the full inverse condition number or a statistical comparison of all experiments.

### 3.5 Unlabelled amplitudes through coalescence

**Locators:** `v3/40_inverse.tex`; `v4/40_coalescence.tex`; `v5/40_pairwise_inverse.tex`; `v6/30_three_amplitudes.tex`.

The symmetric coefficient extension is the correct way to handle repeated roots. The contour formula for the sum of the three analytic node functions extends to a full coefficient neighborhood. The inverse-function theorem is applied there, before restriction to the real-rooted physical subset. The subsequent root matching counts multiplicities; the disk-union Rouché argument does not assume separable labelled roots.

The four-function Wronskian and all twelve entries of the physical three-amplitude derivative table have been independently recomputed. The physical area constraint is

$$A(R,e)=\frac{\sqrt3}{2}-\pi R^2-\frac{\pi R}{54}e_1
+\frac{41\pi}{7776}e_1^2-\frac{5\pi}{432}e_2.$$

At $R=1/4$, its three-amplitude determinant is indeed

$$-\frac{2\sqrt2(15804720A_0+64253\pi)}{72930375A_0^4}\ne0,
\qquad A_0=\frac{\sqrt3}{2}-\frac\pi{16}.$$

Adding the observed spacing uses the first row $(-2,0,0,0)$ for $g=1-2R$. This supports the joint local coefficient, area, and curvature estimates. The result is near that reference radius, not a global three-amplitude theorem throughout the family.

The physical path $r(s)=(R+36s,R-18s,R-18s)$ has even area and opposite-side amplitude difference of cubic order. Its matching curvature distance is linear in $|s|$. This proves sharpness of the pairwise one-third exponent in the stated amplitude topology. It does not contradict the one-half exponent for distance to the circular reference. Equal facing curvatures are necessary for interpreting each scalar inverse parameter as an actual curvature; otherwise only the printed effective curvature is recovered.

### 3.6 Fine calibration and genuinely count-only acquisition

**Locators:** `v5/50_self_calibration.tex`; `v6/40_count_only_acquisition.tex`, `thm:v6-count-only`.

The selected-position and count-only procedures are now genuinely separate. For fixed $j\le J$, the count probability has the form $p_j(d)=d^2(C_j+dB_j(d))$. Estimating $p_j(d)/d^2$ from Bernoulli trials incurs noise of order $(nh^2)^{-1/2}$, not $n^{-1/2}$. Fixed-order extrapolation gives bias $O_m(h^m)$.

The pilot uses the simple zero of the square root of the onset probability. Interpolation is performed at positive physical offsets; a Taylor polynomial is evaluated near the zero, not an unphysical negative-offset probability. Its common positive normalizer cancels. Negative-binomial waiting estimates provide the relative probability accuracy at the stated cost.

The root-or-zero fallback is important. It keeps the estimated shift in its prescribed interval on every pilot outcome. With $L=J+1$, the second-stage actual offsets are bounded below by $(L-3J/4)h>0$, including after a failed pilot. This establishes finite unconditional expected cost, rather than just a cost conditional on a successful preliminary estimate.

Fresh second-stage preparations remain independent conditional on the entire pilot. The shift error produces normalized probability error of order $|\widehat g-g|/h$; extrapolation does not cancel this timing sensitivity. The pilot's $O_m(h^{m+1})$ gap error therefore suffices. The resulting amplitude error $O_m(h^m)$ feeds the positive coalescing inverse and gives matching curvature error $O_m(h^{m/3})$.

Accordingly the sufficient raw-preparation order

$$C_m\varepsilon^{-(6+6/m)}\log(C_m/\eta)$$

is supported for fixed $m$, fixed $J=3$ or $4$, the stipulated local compact family, noiseless recording, and the supplied coarse bracket. It includes fine calibration. The initial bracket $|g-g_0|\le h/4$ still shrinks with the requested accuracy and is not acquired in this bound. The text says this; it is a limitation of the stated experiment, not a concealed error. No conclusion uniform in $m$, nor an optimized minimax exponent six, follows by formally sending $m$ to infinity.

### 3.7 Retained record, circular, and companion arguments

**Locators:** `v3/30_observability.tex`, `v3/50_record_response.tex`; the circular appendix sources; `two_collision.tex`.

The conditional metric uses the physical residual-time weight and gives $\operatorname{Cov}(Y)/d=H^{-1}/3+O(d)$. The odd-flight two-variance inverse does not divide by an exponentially small covariance. Paired independent successful preparations estimate centered physical variances; successive impacts are not assumed independent. The realized scalar fiber has fixed gap and area while changing the endpoint curvatures, and therefore supplies a genuine geometric check of the effective-curvature distinction.

The record-response argument specifies the maximum norm on growing arrays and differentiated smooth tests. A sampling interface has an explicit boundary term and a positive margin. The margin is nonempty on the stated small latent support; fixed physical schedules can carry the printed factors of $k/d$. It would be wrong to infer arbitrary decoder response from a convergence estimate, but the source does not do so.

The circular appendix consistently specializes the general Hessian and flux calculation. The independent-roof comparison uses a product density on a simplex and has exponent $j+1$, unlike the correlated physical exponent two. The Lambert-series continuation refers to onset coefficients from different windows, not fixed-window pressure.

The companion's stationary tail identity is derived without renewal assumptions. Its window is below twice the minimum intercollision gap, while remaining above the one-flight onset. The complete short-flight region is uniformly transverse. A critical point on the terminal level would force the normal chord of length $1-2R<T$, a contradiction. Flattening that regular level justifies its smooth response and Bell-polynomial moving-level formulas. The explicit positive-measure witness and negative roof derivative support strict two-collision response. This companion is a separate fixed-window calculation, not an imported long-time theorem.

## 4. Additional referee calculation: an exact total-variation benchmark

This calculation is new to the present report. It concerns the **quadratic right-limit successful experiments**, not exact nonlinear positive-offset probabilities. It provides a sharp test of the mechanism in `thm:v6-transfer`.

Take identical facing curvatures, write $a=\sinh\gamma/g$, and use the scaled endpoint/residual coordinates $(Y,s)$. The finite quadratic conditional law has constant density $a/\pi$ on

$$D_j=\{s\ge0:\ s+\tfrac12Y^{\mathsf T}H_jY<1\},\qquad
H_j=a\begin{pmatrix}\coth(j\gamma)&-\operatorname{csch}(j\gamma)\\
-\operatorname{csch}(j\gamma)&\coth(j\gamma)\end{pmatrix}.$$

The boundary law has the same constant density on $D_\infty$, obtained by replacing $H_j$ by $aI$. Indeed both determinants equal $a^2$, and both domains have volume $\pi/a$.

Set $u=e^{-j\gamma}$ and $\lambda=\tanh(j\gamma/2)=(1-u)/(1+u)$. After an orthogonal change of endpoints and a common rescaling, each residual-time section compares the unit disk with the equal-area ellipse

$$\lambda x^2+\lambda^{-1}y^2<1.$$

The crossing angle in a quadrant is $\theta_0=\arctan\sqrt\lambda$. Polar integration gives the disk/ellipse intersection area

$$2\left[\theta_0+\int_{\theta_0}^{\pi/2}
\frac{d\theta}{\lambda\cos^2\theta+\lambda^{-1}\sin^2\theta}\right]
=4\theta_0.$$

The common scaling of every section makes the same overlap fraction hold for the three-dimensional domains. With total variation defined as $\sup_B|P(B)-Q(B)|$, the exact result is therefore

$$\boxed{\delta_j:=\|\Pi_j^{(0)}-\Pi_\infty^{(0)}\|_{\mathrm{TV}}
=1-\frac4\pi\arctan\sqrt{\tanh(j\gamma/2)}
=\frac2\pi\arcsin(e^{-j\gamma}).} \tag{TV1}$$

In particular $\delta_j=(2/\pi)e^{-j\gamma}+O(e^{-3j\gamma})$. The superscript denotes the quadratic right-limit model. These are not the same as the finite and infinite nonlinear experiments at fixed positive $d$.

There is a further exact conclusion. The two densities are equal on their common support and zero off their respective supports. Their product densities have precisely the same property. Thus, for $k$ independent successful records,

$$\boxed{\| (\Pi_j^{(0)})^{\otimes k}-(\Pi_\infty^{(0)})^{\otimes k}\|_{\mathrm{TV}}
=1-(1-\delta_j)^k.} \tag{TV2}$$

Consequently, as $j\to\infty$, convergence holds exactly when $k e^{-j\gamma}\to0$. When $k e^{-j\gamma}\to b\in(0,\infty)$, the distance tends to $1-e^{-2b/\pi}$. A blanket square-root-in-$k$ accumulation estimate would be false for these moving-support laws.

Restoring a common failure atom and the common leading success probability

$$p_j^{(0)}(d)=\frac{d^2}{2A\sinh(j\gamma)}$$

gives an equally exact tangent-experiment identity, for sufficiently small $d$ so this mass is at most one:

$$\boxed{\| (P_j^{(0)})^{\otimes n}-(P_\partial^{(0)})^{\otimes n}\|_{\mathrm{TV}}
=1-(1-p_j^{(0)}(d)\delta_j)^n.} \tag{TV3}$$

This supports the manuscript's use of expected successes, rather than raw sample size alone, in its transfer bound. It does **not** prove that the particular slower rate $\tau$ furnished by the nonlinear block proof is optimal. Nor does it permit interchanging arbitrary growing-sample and small-offset limits without additional error estimates. The identities are exact in the explicitly defined tangent experiments and sufficient for the stated benchmark.

## 5. Additional referee calculation: a lower bound for the specified count design

The manuscript correctly declines a global minimax claim. There is nevertheless a useful lower bound in the actual physical family, which clarifies why a cubic inverse obstruction cannot simply be removed by more precise algebra.

Fix $R=1/4$, hence $g=1/2$, and put $\alpha=0$. Allow $(\beta,\zeta)$ to vary in the printed support family. Rotating the triangular lattice and the whole prepared billiard through $\pi/3$ preserves the unlabelled count law. On $(\beta,\zeta)$ this acts as a rotation through $2\pi/3$, up to choice of sign. No nonzero real linear functional is invariant under that action.

For fixed $j\le J$ and $0<d\le d_*$, write

$$p_{j,d}(\beta,\zeta)=\Pr_{\beta,\zeta}(N_{jg+d}\ge j+1).$$

The normalized function $p_{j,d}/d^2$ is smooth with uniformly bounded third parameter derivatives by the forward theorem. Its derivative in $(\beta,\zeta)$ vanishes at zero by rotation invariance. Along the two alternatives $(\beta,\zeta)=(s,0)$ and $(-s,0)$, Taylor's theorem therefore yields

$$|p_{j,d}(s)-p_{j,d}(-s)|\le C_Jd^2|s|^3,
\qquad c_Jd^2\le p_{j,d}(\pm s)\le C_Jd^2<\tfrac12. \tag{LB1}$$

The cubic upper bound here is for actual finite-offset count probabilities, not only their leading amplitudes. It follows from the full parameter-smooth physical law and the symmetry; no simulated dynamics or interpolation of a finite amplitude prefix is needed.

For Bernoulli probabilities $p,q\in(0,1)$, the elementary bound

$$D_{\mathrm{KL}}(\operatorname{Ber}(p)\Vert\operatorname{Ber}(q))
\le\frac{(p-q)^2}{q(1-q)}$$

follows from $\log x\le x-1$. Hence one query at $(j,d)$ has divergence at most $C_J d^2s^6$. For independent predetermined Bernoulli queries at $(j_i,d_i)$, additivity gives

$$D_{\mathrm{KL}}(\mathsf P_s\Vert\mathsf P_{-s})
\le C_Js^6\sum_i d_i^2. \tag{LB2}$$

The two curvature multisets have matching distance comparable to $|s|$. A reconstruction within less than half that distance induces a test of the two alternatives. Pinsker's inequality and the elementary two-point testing bound then imply a worst-case expected matching error at least

$$c_J\left(\sum_i d_i^2\right)^{-1/6} \tag{LB3}$$

for sufficiently large budgets, with the alternatives chosen inside the fixed local family. Equivalently, constant-confidence curvature accuracy $\varepsilon$ requires $\sum_i d_i^2\ge c\varepsilon^{-6}$, with constants adjusted for the chosen confidence below one half.

For a design confined to $d_i\le C_mh$, this requires

$$n\ge c_mh^{-2}\varepsilon^{-6}. \tag{LB4}$$

This conclusion also extends to a stopped, adaptive Bernoulli procedure whose queries stay in the same collar on every history and whose worst-case expected number of queries is at most $N$. Conditional on any common observed history, the chosen query is the same in the two experiments. The chain rule bounds its conditional divergence by $C_mh^2s^6$. Apply the bound to the first $M$ queries, including a stop symbol, then let $M\to\infty$; the resulting divergence is at most $C_mh^2s^6\mathbb E_sT$. The same two-point argument gives $N\ge c_mh^{-2}\varepsilon^{-6}$. A deterministic supplied bracket centered at the common true gap makes this a subexperiment of the local setup; allowing the gap to be unknown cannot make this two-point test easier.

With the manuscript's fixed-order choice $h\asymp\varepsilon^{3/m}$, (LB4) has order $\varepsilon^{-(6+6/m)}$. Thus its stochastic/coalescence power has a matching obstruction **within this shrinking-offset, bounded-flight-number, Bernoulli-query design**, apart from confidence logarithms and constants. The pilot's clipped windows satisfy the required all-history offset bound at the two alternatives.

This is not a global minimax theorem over all count observations or all experimental schedules. It does not rule out using nonshrinking offsets, other flight numbers, the complete values of lower collision counts, physical positions, stronger analytic information, or another treatment of nuisance functions. It does not justify sending $m$ to infinity with uncontrolled constants. The lower bound strengthens the interpretation of the printed procedure at its actual scale; it must not be used to enlarge the theorem's quantifiers.

## 6. Remaining editorial requirements and limits of the recommendation

No new fatal proof defect is asserted in the audited principal chain. The following are concrete requests for presentation and assessment, not a demand to prove a new global theorem.

**V6-R1: Give the observation and asymptotic structure in one compact statement.** The introduction now distinguishes the data correctly, but a reader must still combine several sections to see which parameters vary. A table should contrast: long-bridge endpoint/residual transfer with growing sample size; fixed-order contact coefficients with varying flight length; fixed-$J$ raw-count acquisition with decreasing offset; and selected-position acquisition at odd $j$. List supplied information, unknowns, error topology, cost, and the exact variable in which constants are uniform. This would prevent a reader from incorrectly using the selected-position rate for count-only coalescence or the transfer theorem for full embedded records.

**V6-R2: Explain the statistical content without an unsupported optimality slogan.** Sections 4 and 5 of this report give two possible benchmarks: support mismatch can force linear product accumulation, and cubic physical indistinguishability obstructs the shrinking-offset Bernoulli design. The author need not adopt these precise lemmas. An alternative argument could serve the same interpretive purpose. What should not appear is a claim of optimized exponent six from fixed-$m$ bounds, a Gaussian square-root accumulation principle for these support-changing laws, or global minimax optimality inferred from amplitude sharpness alone. Those claims are not presently made and must remain absent unless separately proved.

**V6-R3: Make the importance case about the actual relative theorem.** The count-only theorem is now a coherent and correct application of differentiated finite-threshold laws, but it uses only $J=3$ or $4$. The analytic germ inverse is also present at one flight. These facts should be stated alongside, rather than far from, the motivation for the long-bridge construction. The key contribution left to defend is the uniform relative physical law and the genuinely growing-experiment comparison. Explain what that mechanism teaches beyond an assembly of valid local consequences. No particular enlargement is imposed as an acceptance condition, and no result is promised acceptance merely by satisfying this presentation request.

**V6-R4: Keep reproducibility evidence separate from proof and priority.** The source pins and build instructions are useful. Author diagnostics, reviewer diagnostics, rendered-page counts, and remote CI are different claims. Use actual observed evidence for each. For compact discrepancy minimization, specifying a Borel measurable tie-breaking selection would make the estimator convention fully explicit; continuity on compact metric parameter sets supplies standard measurable-selection machinery, so this is a formalization request, not an identified obstruction to the stated bounds.

My adverse venue recommendation should not be repackaged as “the theorems are wrong,” “the revision ignored the referee,” or “this line of research is impossible.” Equally, the lack of a fatal error and the completion of a checklist are not an affirmative top-four recommendation. The significance judgment remains less mechanically verifiable than the determinant and probability calculations; that uncertainty is intrinsic to this part of the report.

## 7. Targeted comparison with primary literature

The comparison is targeted, not an exhaustive originality search. Primary records and selected source passages were checked; no claim is made to have reverified every proof of the cited works.

Bolotin and Treschev's Hill-formula work [1] relates action Hessians and monodromy in discrete and continuous Lagrangian systems. It supplies predecessor structure for the determinant mechanism. It does not, on the material inspected, substitute for the collision-order-uniform relative nonlinear flux estimate and physical residual-time integration proved here.

Zelditch's analytic-domain work [2] extracts boundary information from localized wave-trace coefficients near periodic billiard orbits, using oscillatory boundary integrals and stationary-phase analysis in specified symmetry and nondegeneracy classes. The published theorem's additional hypotheses matter; it should not be summarized as arbitrary analytic-domain rigidity from a single symmetry. The current positive phase-volume probability is a different datum. The v6 comparison acknowledges both the related coefficient-to-boundary strategy and the difference in observation. No containment or equivalence of the two inverse theorems is asserted.

De Simoi, Kaloshin and Leguil [3] consider marked-length determination for analytic chaotic open billiards with axial symmetry and genericity assumptions. Finamore and Leguil's pinned v1 preprint [4] concerns an enriched marked length spectrum and finite-horizon Sinai billiards. These are distinct table-determination problems. The present contact reconstruction does not replace their global observations; conversely, their statements are not evidence that the normalized onset theorem is already known.

Batenkov and Yomdin [5] study local accuracy and the geometry of confluent Prony systems. The manuscript's specific hyperbolic-sine Wronskian and physically realized coalescence path have to be checked on their own. Its coefficient-to-root exponent is not a new universal root-perturbation theorem. The new count experiment adds physical acquisition and timing costs, which are not supplied by an exact Prony identification theorem alone.

## 8. Executed verification and review boundaries

The accompanying `independent_checks.py` completed **190 named checks: 162 exact symbolic/rational checks and 28 ordinary floating-point checks**. It ran normally and with `python -O`; the JSON outputs were byte-identical in the executed environment. Explicit exceptions, not optimization-removable assertions, enforce the checks. The script imports no repository or earlier referee diagnostic code and makes no network calls.

Exact checks include the three-amplitude derivative table and determinant, the symmetric physical area constraint, the four-function Wronskian, finite Green-metric identities and uniform diagonal lower bounds at rational values of $e^{-\gamma}$, one-flight reductions, extrapolation and harmonic identities, the all-outcome window margin, the order-three rotation, and the physical cubic amplitude coefficient. Numerical checks include independent polar integration of the disk/ellipse overlap, the product-support identity, and sample instances of the Bernoulli divergence inequality.

These checks do not simulate a global billiard and do not certify an infinite-dimensional contraction or an all-order theorem. In particular, the proofs of (TV1)–(TV3) and (LB1)–(LB4), rather than the number of checks, justify the report's new calculations. Ordinary quadrature is not interval arithmetic.

Executed environment: Python 3.13.5, SymPy 1.14.0, SciPy 1.17.0. Script SHA-256: `921f238ad09f8db7cce9ea315eef9d9a50d5f49279637ceba9264c9a4a726855`. Normal and optimized complete diagnostic JSON SHA-256: `3e5f0b63b7c88806e7be92de556d49930a1051b4bbf9757838a776238f0b3f2e`. Cross-version byte identity is not promised. `VERIFICATION.json` records commands, source identity, counts, hashes, and nonclaims.

The direct source review covered all five new v6 introduction/application files, the active geometric/relative/integration foundations, the half-line and differentiated determinant proofs, contact jets and realization, the variance and calibration arguments, the constrained and ambient amplitude inverses, the retained general record-response section, the circular appendix calculations, and the two-collision companion's mathematical argument. Historical review conclusions were checked against the actual revised statements, not accepted as proof certifications.

The archival Round 33 program, inactive historical manuscript trees, every other revision branch, and every external cited proof were not re-audited. The author's validation suite was not rerun. No manuscript PDF was compiled or visually inspected, no remote CI was certified, and no formal proof assistant was run. The manuscript page counts are reported by its author, not independently verified here. These limits are not mathematical counterexamples; they delimit what this report has actually checked.

## 9. Final disposition

This is a real, substantive v6 response. The actual/effective-curvature distinction is repaired; finite-flight fixed-order inversion is proved; the physical three-amplitude reconstruction is correctly delimited; and the count-only acquisition theorem includes an actual fine-calibration experiment. The relative boundary law now has a meaningful common-observation experiment comparison. The new calculations above support two of its statistical interpretations while preserving their proper scope.

I find no fatal error in the audited central proof chains. I nonetheless withhold the requested top-four recommendation because the manuscript still has not made a sufficiently compelling case for the exceptional significance of its particular uniform relative mechanism and its collection of applications. This is an editorial rejection of the present submission, not an instruction to delete correct mathematics, lower the general forward assumptions, or abandon the research program. A subsequent manuscript should be assessed on its exact committed mathematics, without recycling the now-resolved objections.

## References and frozen source links

[1] S. Bolotin and D. Treschev, *Hill's formula*, Russian Mathematical Surveys 65 (2010), 191–257. DOI: 10.1070/RM2010v065n02ABEH004671. Primary author record: https://arxiv.org/abs/1006.1532.

[2] S. Zelditch, *Inverse spectral problem for analytic domains, II: Z2-symmetric domains*, Annals of Mathematics 170 (2009), 205–269. DOI: 10.4007/annals.2009.170.205. Publisher: https://annals.math.princeton.edu/2009/170-1/p06.

[3] J. De Simoi, V. Kaloshin and M. Leguil, *Marked length spectral determination of analytic chaotic billiards with axial symmetries*, Inventiones Mathematicae 233 (2023), 829–901. DOI: 10.1007/s00222-023-01191-8. Primary author record: https://arxiv.org/abs/1905.00890.

[4] D. Finamore and M. Leguil, *A CAT(0)-approach to the marked length spectral rigidity of Sinai billiards*, arXiv:2510.18983v1, October 21, 2025. Pinned version: https://arxiv.org/html/2510.18983v1. This citation does not assert that v1 is the latest version or a published journal article.

[5] D. Batenkov and Y. Yomdin, *On the accuracy of solving confluent Prony systems*, SIAM Journal on Applied Mathematics 73 (2013), 134–154. DOI: 10.1137/110836584. Primary author record: https://arxiv.org/abs/1106.1137.

Frozen manuscript: https://github.com/TrillionniumFoundation/theta-theory/tree/4ca186258c92dcbc75accc4eb576e307cc612189/papers/A2-v6-relative-transfer-count-experiments.

First controlling report: https://github.com/TrillionniumFoundation/theta-theory/blob/9975aa037d5d9eb1f339b9220f9cd21fb54c0876/reviews/a2-v5-statistical-contact-rigidity-harsh-independent-2026-09-09/REFEREE_REPORT.md.

Second controlling report: https://github.com/TrillionniumFoundation/theta-theory/blob/0421836a5868967f90093281c7ca43aab9815a0d/reviews/a2-latest-materialized-second-harsh-2026-09-09/REFEREE_REPORT.md.
