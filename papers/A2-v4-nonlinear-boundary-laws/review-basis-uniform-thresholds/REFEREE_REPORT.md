# Independent referee report: uniform collision-threshold laws in a periodic Lorentz gas

## Recommendation: reject at the requested top-four-journal level; retain the substantive new theorem

**Review date:** September 9, 2026 (Asia/Singapore).  
**Reviewer:** GPT-6 Astra Pro. This is an independent AI-assisted assessment requested by the repository owner, not a report commissioned by, or a decision of, any journal.  
**Author:** Qian Qi.  
**Main submission:** *Uniform collision-threshold laws and marked response in a periodic Lorentz gas*.  
**Source branch:** `revision/a2-uniform-collision-thresholds-2026-09-09`.  
**Frozen source commit:** `500cf06faccb6eadd6c122abeb63c60a0cb7522e`.  
**Source commit time:** September 8, 2026, 16:53:07 UTC = September 9, 2026, 00:53:07 Singapore time.  
**Previous controlling review:** `50e2bd898e3168d43f1519729a0d88ccbc03946a`.  
**New review branch:** `review/a2-uniform-thresholds-harsh-independent-2026-09-09`.

All manuscript locators below are relative to `papers/A2-uniform-collision-thresholds-v1/` at the frozen commit. The native main entrypoint is `main.tex`, with Sections 1--8. The complete unchanged companion is `two_collision.tex`, Git blob `df44402b17031525c087d39dfedf8dac3ada611d`. The previous report, author response, proof ledger, submission index, and preserved Round 33 A2 chapter were also consulted. Exact source identities and the executed diagnostic boundaries are recorded in `verification.json` alongside this report.

## 1. Editorial assessment

This revision is mathematically different from the seven-page two-collision note previously reviewed. It is no longer legitimate to reject it merely because its count law depends on one roof marginal. The new principal result concerns actual sums of arbitrarily many successive roofs. The paper proves a collision-order-independent onset collar, treats an exponentially small endpoint flux relatively rather than absolutely, and reconstructs a correlated impact record. These are substantive improvements, not changes of terminology.

The strongest part is the combination of the endpoint-localized boundary-value construction with Lemma 4.3. The former prevents constants from growing with itinerary length; the latter prevents an absolute error from overwhelming the exponentially small leading probability. The subsequent Morse integration, smooth additive-source expansion, and residual-time record calculation are coherent consequences. I have not established a fatal error or an in-scope counterexample to Theorems 1.1, 1.2, or 6.1. Independent calculations in initial collision-angle coordinates support the coefficient, and finite nonlinear tests support the relative-twist mechanism.

Nevertheless, I do not recommend publication as an article at the requested top-four level in its present form. The paper develops a precise local hyperbolic calculation for six symmetry copies of one shortest period-two orbit in a one-parameter circular model. The uniformity in orbit length is real, but the applications presently extracted from it do not demonstrate a comparably substantial new dynamical or inverse-geometric consequence. The source summation is, after the uniform local estimate, a geometrically convergent axial series. The multiplier recovery is correct but informationally redundant once the threshold locations are known in this model. The closest existing statistical manifestations of periodic-orbit instability also deserve a more direct comparison.

This is a judgment about the significance established by the submission, not a theorem that a local result or a single model cannot belong in a leading journal. A result of limited formal scope can be profound. Here the manuscript has not made that case sufficiently compelling. Nor is this an instruction to weaken the result, delete proofs, or relabel an unsupported long-time theorem as proved. The new mathematics should be retained. The distinction between a credible specialized result and a persuasive top-four contribution must not be erased in either direction.

## 2. What the revised theorem actually says

The preparation is normalized full phase volume for a unit-speed triangular periodic disk billiard, with radius in a fixed compact interval K contained in (0,1/2). Write

$$g_R=1-2R,\qquad A_R=\sqrt3/2-\pi R^2,\qquad
\lambda_R=2R/A_R,\qquad \chi_R=\operatorname{arcosh}((1-R)/R).$$

Theorem 1.1, `sections/01_results.tex`, label `thm:unweighted`, asserts a positive collar width independent of every integer j at least one, and

$$P_j(R,\varepsilon):=\Pr_R(N_{jg_R+\varepsilon}=j+1)
=\frac{3\lambda_R}{2R\sinh(j\chi_R)}\varepsilon^2
[1+\varepsilon h_j(R,\varepsilon)].$$

Every prescribed mixed radius/offset derivative of the normalized remainder is bounded uniformly in j on K. The event is the entire maximal-count event, not an artificially selected transverse ensemble. Its probability vanishes on the negative side of the onset. No constant is claimed uniform as R approaches zero or one half, or as the derivative order tends to infinity.

Theorem 1.2 attaches a smooth additive mark to the outgoing states at all j+1 impacts. If its axial sum is w_{j,e}, the contribution from orientation e is

$$\frac{\lambda_R\varepsilon^2}{4R\sinh(j\chi_R)}
e^{q w_{j,e}(R)}[1+\varepsilon h_{j,e}(R,q,\varepsilon)].$$

For the stated sufficient source range, differentiation of the normalized expression costs only a polynomial in j against a remaining exponential decay. This yields actual summability of the threshold hierarchy. It does not yield a characteristic function or pressure for all itineraries in one fixed long observation window.

Theorem 6.1 identifies the conditional law in a common three-dimensional latent domain, gives uniform expansions of every impact position and time, and controls a fixed finite number of sampling cuts. Theorem 1.2 supplies response for smooth additive collision marks; Theorem 6.1 supplies a record limit and cut-probability convergence. Those are related but distinct assertions.

## 3. Proof audit

### 3.1 Full preparation, residual time, and localization

The stationary normalization in `sections/02_flux.tex`, equations `eq:santalo` and `eq:tails-new`, is correct. Boundary flux has total mass 4 pi R, whereas unit-speed phase volume has total mass 2 pi A_R. The mean roof is A_R/(2R). The counting identity follows from allowable suspension heights and invariance, not independence of consecutive roofs.

The marked first-impact formula in Proposition 2.1 is particularly important. At t=jg_R+epsilon, the residual time is bounded by epsilon, which is smaller than every preceding roof. Thus its integration interval needs no further truncation. A further impact is excluded by the same lower gap. Retaining this residual variable avoids the mistake of shifting a stationary integrand while leaving its mark unshifted. The initial and terminal free-flight pieces are correctly included.

Infinite horizon does not invalidate this argument. The proof uses coverage by flight tubes up to a null set and finite mean roof, not a uniform upper roof bound. The exceptional rational directions are a null subset of the angular variable, and irrational torus lines intersect the disk. No unproved mixing assertion is needed here.

Lemma 3.1 also supplies the necessary global-to-local reduction. Every individual flight has nonnegative excess over g_R. Small total excess therefore forces every flight to be short. The lattice gap between nearest and next-nearest centers, uniqueness of the shortest chord, and angular separation between nearest-neighbor directions force alternation along one pair. Compactness in K gives constants independent of the number of reflections. The no-obstruction and non-grazing conclusions are consequences of this complete-event localization, not additional restrictions on preparation.

The coercivity estimate in `eq:energy-coercive` bounds the sum of squared transverse coordinates by a constant times the total excess. It both excludes other parts of the local chart and prevents an accumulation of interior errors proportional to j. I find no omitted positive-measure itinerary family in the specified collar.

### 3.2 The length-uniform boundary-value calculation

The linearized Dirichlet problem in Lemma 4.1 has interior Hessian

$$H^0_{\rm int}=g_R^{-1}\operatorname{tridiag}(-1,2c_R,-1),
\qquad c_R=(1-R)/R.$$

The displayed Green kernel solves this recurrence and has an exponential off-diagonal bound. The weighted norm with weights rho^i+rho^{j-i}, where exp(-min_K chi_R)<rho<1, makes the local cubic nonlinearity a contraction with a j-independent constant. Strict convexity in the small coordinate box then provides the broader uniqueness statement needed to identify every localized physical orbit with this solution.

The use of a common small complex parameter neighborhood is credible here: the gap and curvature denominators stay separated from zero on the fixed compact radius interval, and the real part of chi retains a positive margin. It supplies fixed-order parameter derivatives of the bridge without differentiating a long unstable initial-value iteration. Summability of the endpoint weights controls the quartic action remainder. These are analytical arguments; the finite tests below are not substitutes for them.

The effective Hessian in Lemma 4.2 is

$$H_{j,R}=\frac{\sinh\chi_R}{g_R}
\begin{pmatrix}\coth(j\chi_R)&-\operatorname{csch}(j\chi_R)\\
-\operatorname{csch}(j\chi_R)&\coth(j\chi_R)\end{pmatrix}.$$

Its determinant and the eigenvalue bounds are consistent. In particular, its nondegeneracy does not deteriorate with j even though its off-diagonal entry is exponentially small.

### 3.3 Relative flux: the critical estimate is actually present

It would be a serious error to use an absolute estimate of the form W_uv=-d_j^0+O(u^2+v^2), because d_j^0 decays exponentially. The manuscript does not make that error.

Lemma 4.3 uses the exact tridiagonal corner-cofactor identity

$$-W_{uv}=\frac{\prod_{i=0}^{j-1}b_i}{\det H_{\rm int}},
\qquad b_i=-\ell_{uv}(y_i,y_{i+1}).$$

Both the sum of one-flight logarithmic errors and the trace norm of the perturbation H_int-H_int^0 are O(u^2+v^2), independently of dimension. The uniformly bounded inverse of H_int^0 then controls the logarithm of the determinant ratio without multiplying the error by j. This yields a relative positive analytic amplitude with uniform fixed-order derivatives. The trace-norm argument is a genuine answer to the potentially fatal loss of relative accuracy.

The first-variation calculation in Proposition 4.4 gives the normalized physical measure

$$d\nu=\frac{-W_{uv}}{4\pi R}\,du\,dv.$$

The nonzero twist also gives injectivity at fixed initial endpoint. This is not merely a formal change of variables detached from the physical billiard: the preceding localization and uniqueness arguments identify the segment with the true successive first hits.

### 3.4 Threshold integration, smooth sources, and jumps

The even Morse construction in Lemma 5.1 is valid for the two-dimensional endpoint action. Its matrix-square-root construction gives an odd local inverse with uniform bounds. Coercivity ensures that the entire active sublevel is represented, so there is no hidden chart-boundary term.

The residual-time integral contributes one additional power of epsilon. Explicitly,

$$\int_{|w|^2<2\varepsilon}(\varepsilon-|w|^2/2)\,dw
=\pi\varepsilon^2.$$

Together with the normalized flux and six orientations, this gives precisely the printed coefficient, including the factors R and lambda_R. The source-free remainder has an even analytic expansion. For a merely smooth mark, the paper correctly switches to finite-order Taylor calculus rather than claiming analyticity of that mark.

The sum of mark deviations from the axial values has bounded derivatives because each deviation is localized at the endpoints of the bridge and these localization weights sum uniformly. Odd terms vanish in the symmetric integral. This explains why the integrated marked normalizer has an O(epsilon) relative remainder although a general source-weighted conditional density has only O(sqrt(epsilon)) deviation. The manuscript expressly makes this distinction.

The polynomial losses in j from radius and source differentiation are consistent with differentiating csch(j chi_R) and the axial source factor. The sufficient exponential margin in Theorem 1.2 is therefore adequate. Radius differentiation at fixed physical time is also correctly distinguished from differentiation at fixed onset offset: the operator becomes partial_R+2j partial_epsilon. The second-derivative jumps 2C_j in time and 8j^2 C_j in radius have the correct normalization and sign.

### 3.5 Joint record and sampling cuts

In `sections/06_records.tex`, the common domain is

$$\mathcal U=\{(z,\eta):|z|<1,\ 0<\eta<1-|z|^2\},
\qquad d\mathsf m=(2/\pi)\mathbf1_{\mathcal U}\,dz\,d\eta.$$

Its volume is pi/2. The exact density in these coordinates is proportional to a_j(sqrt(2 epsilon)z), giving the stated O(epsilon) total-variation bound. The identity that the quadratic flight excesses sum to |z|^2 agrees with the endpoint action. Summing the endpoint-decaying errors gives the uniform time expansion. Direct reflection confirms the signs of the initial incoming and final outgoing transverse velocity formulas.

For a sample near the kth normal impact time, the cut has derivative one in eta. The strip estimate controls mismatch probability uniformly in j for a fixed number of samples. This is a valid way to retain an interface; it does not discard the interface by differentiating only away from collisions.

Two presentation clarifications remain worthwhile. The total-variation assertion concerns the common, parameter-dependent coordinates (z,eta), not total variation between arbitrary physical record measures supported on different embedded surfaces. Also, a record with j+1 coordinates should be equipped with an explicit metric when uniform bounds for Lipschitz tests are asserted. A supremum metric is consistent with the displayed uniform coordinate errors; an unnormalized Euclidean metric on a growing record can introduce a square-root dimension factor. Neither observation refutes the formulas as printed.

### 3.6 Consequences and the retained companion

The independent-roof comparison is mathematically sound. The one-roof excess density is 3/sqrt(g_R)+O(u). Integrating j independent such excesses with a residual-time factor over a simplex gives an epsilon^(j+1) onset with coefficient

$$\frac{\lambda_R}{(j+1)!}\left(\frac3{\sqrt{g_R}}\right)^j.$$

For j at least two this differs from the true quadratic onset. This directly disproves any suggestion that the revised hierarchy still uses only the one-roof marginal. At the same time, the reason for the quadratic exponent is transparent: the actual orbit segment is determined by a two-dimensional collision state, not j independent roofs.

The period-two multiplier, coefficient ratios, and Lambert-series calculation in Corollary 7.2 are correct consequences of the recurrence. The manuscript correctly says that this coefficient-generating series is not a pressure or a fixed-window count generating function. Its meromorphic poles must not subsequently be called transfer-operator resonances without a new argument.

The unchanged companion retains its correct distinction between expected count and event probability, its regular terminal-level argument, and its coarea contribution to the second derivative. The new main supplies the previously requested nonempty terminal-level witness. I found no reason to reverse the earlier favorable assessment of that companion's narrowly scoped theorem.

## 4. Principal publication objections

### UCT-R1 — Substantial uniform local analysis, but an insufficiently demonstrated top-four contribution

**Severity: major editorial objection, not an established mathematical contradiction.**

The new result goes beyond fixed-j Morse integration; dismissing it as that alone would be unfair. Nevertheless, the complete event is localized to one normal period-two mechanism and its symmetry copies. No competition between different shortest mechanisms, transition between minimizing itinerary types, or stability under noncircular geometric deformations is established. The two-dimensional action and its relative twist are the mathematical center; the later source summation, renewal comparison, and record cuts are mostly consequences of that center.

The paper should explain what new principle is exposed by this calculation and substantiate that explanation with a theorem or consequence commensurate with the requested level. One possible route is a structurally stable threshold theorem for a genuinely broader family of convex scatterers, with actual verification of minimizer selection, nondegeneracy, relative flux, and moving physical tests. Another is a substantial new consequence already within the circular model that is not determined by its known one-parameter geometry. These are possible directions, not a demand that every good paper be more general or that all eleven planned papers be solved simultaneously.

Adding more sources, higher derivative indices, or a longer list of finite checks does not by itself resolve this objection. Those enlargements must supply mathematical information beyond the already proved uniform local estimate.

### UCT-R2 — The instability application is informationally weak in the stated model

**Severity: major objection to the contribution claimed for the application; the corollary itself is correct.**

In the specified unit-speed, unit-lattice-spacing circular family, the spacing of the threshold locations already determines the radius:

$$R=(1-g_R)/2,\qquad c_R=(1+g_R)/(1-g_R).$$

It consequently determines exp(2 arcosh(c_R)), the multiplier recovered by the coefficient ratios. Thus the inverse statement is an alternative statistical encoding, not an additional recovery of an unknown geometric degree of freedom once the physical thresholds are observed.

There is a second concrete limitation. Define a_0=0 and a_j=1/C_j for j at least one. The exact coefficient formula gives

$$a_{j+1}=2c_Ra_j-a_{j-1}.$$

The entire unweighted coefficient hierarchy is therefore generated by a second-order recurrence in this model. Its infinitely many coefficients or meromorphic poles do not amount to infinitely many independent pieces of dynamical information.

The manuscript already disclaims stronger inverse rigidity than marked-length-spectrum results. That disclaimer is appropriate, but it does not itself make the application substantial. A stronger inverse motivation would require an explicitly identified uncertainty not already resolved by the threshold locations, and a theorem showing that amplitudes resolve it. The present corollary should remain, but it cannot bear much of the top-four significance argument.

### UCT-R3 — The originality discussion misses a closer statistical comparator

**Severity: major literature-positioning objection; not a demonstrated priority collision.**

The comparisons with stationary Palm theory, Hill-type formulas, and marked length spectra are useful. However, statistical detection of periodic-orbit instability is already developed in rare-event theory for hyperbolic systems with singularities. Carney, Nicol, and Zhang [4] prove compound-Poisson and extreme-value results near periodic points, including Sinai billiard maps with finite or infinite horizon, with the relevant index determined by the derivative of the map. That is closer to the statistical motivation of Corollary 7.2 than comparison only with labeled periodic lengths.

The comparison must distinguish the present physical maximal-count onset, its collision-order-uniform collar, and its radius/source derivatives from rare visits to shrinking neighborhoods in a long observation sequence. I am not claiming that [4] contains Theorem 1.1 or its exact coefficient. The point is that a different observable is not, by itself, a sufficient originality argument for the asserted significance. The precise extra theorem must be identified against the nearest mechanisms, not only against obviously different operator or inverse-data problems.

The search used here is targeted, not an exhaustive proof of priority or non-priority. It does not justify asserting that the exact uniform threshold theorem was already known.

### UCT-R4 — Keep full-record limits separate from full-record response

**Severity: scope and topology clarification; not a finding that Theorem 1.2 is false.**

Theorem 1.2 gives derivatives for a specified smooth additive-source functional. Theorem 6.1 gives total-variation control in latent coordinates, path reconstruction, and convergence of a finite set of cut probabilities. These do not automatically give all-order radius derivatives for arbitrary bounded record tests, arbitrary discontinuous decoders, or fixed physical sampling schedules across all relevant parameter interfaces.

A simple scope example makes the logical distinction exact. The auxiliary Bernoulli family

$$p_\varepsilon(r)=\tfrac12+\varepsilon\sin(r/\varepsilon^2)$$

has total-variation distance at most epsilon from Bernoulli(1/2), while p'_epsilon(0)=1/epsilon. This is not a billiard counterexample. It shows why small total-variation error alone cannot be differentiated. In the present paper, any stronger decoder-response conclusion would require its own differentiated moving-domain estimate; the strip estimate proves convergence, not all those derivatives.

State the test class and record metric explicitly, and keep the broad phrase “marked response” attached to the result actually proved. Do not delete the useful complete-record theorem or promote its O(epsilon) limit to an unproved response theorem.

## 5. An additional analytical check: the axial source range

The paper's bound q_0 F_*<min_K chi_R is sufficient, but not the intrinsic pointwise summability condition of its own threshold series. This is a refinement available from the printed theorem, not a correctness objection.

Let a_e=f_R(x_e) and define the pair average bar f_e=(a_e+a_{-e})/2. Exact counting of even and odd indices gives

$$w_{j,e}=(j+1)\bar f_e+
\mathbf1_{\{j\ \mathrm{even}\}}(a_e-a_{-e})/2.$$

For fixed R and real q, the parity correction is bounded independently of j. On a sufficiently small collar, the positive relative amplitudes are bounded above and below, and csch(j chi_R) is comparable to exp(-j chi_R). Consequently the normalized series over j converges precisely when

$$\max_e q\bar f_e<\chi_R.$$

At equality there is a nondecaying positive contribution, and beyond equality one contribution grows. The same conclusion applies to the normalized right limit at epsilon=0. On compact parameter/source sets strictly inside this domain, the differentiated series remains uniformly convergent because only polynomial losses in j occur.

This refinement would make the source statement more natural. It also clarifies the extent of the present summability: the governing rates are the axial pair averages and one normal-orbit exponent, not a pressure obtained by summing the full billiard itinerary space. That latter object would require different estimates.

## 6. Disposition of the previous report and the historical programme

| Previous item | Disposition in this revision |
|---|---|
| TC-R1: only a regular one-roof calculation | The mathematical limitation is substantially overcome by the uniform multi-flight theorem. The old reason cannot simply be repeated. The top-four significance question remains, for the reasons stated in UCT-R1. |
| TC-R2: no genuine multi-history or uniform/summable control | Addressed for the extremal threshold hierarchy, including correlated marks and an entire reconstructed record. Not addressed for unrestricted long records or arbitrary decoder derivatives, which the current main does not claim. |
| TC-R3: no bridge to the original A2 root theorem | Still not proved, but now explicitly and correctly separated in the submission index and Section 8.3. This is a programme-status issue, not a valid sole veto on a separately scoped theorem. |
| TC-R4: insufficient originality comparison | Improved substantially; the closest periodic rare-event/statistical-instability comparison and the weight of the inverse application remain inadequate. |
| Terminal-level witness and source preservation | The witness is supplied in Section 7.3; the complete old companion remains the same Git blob. |

The preserved `history/round33_A2.tex` proves an arithmetic separation estimate and a conditional Fourier-inversion budget. It does not establish the required model-level stable-curve operators, source-dependent high-frequency estimates, or integrated central Edgeworth remainder. The latest main does not silently claim those inputs. Statistical A1 v36 is not imported as a substitute.

It would be wrong to say that the new source series closes the historical unrestricted local-limit programme. It would also be wrong to require that entire programme as a condition for taking the new, explicitly different theorem seriously. The present rejection recommendation rests on the submitted article's demonstrated contribution, not on a demand to solve a different theorem.

## 7. Independent verification

The accompanying `diagnostics.py` imports no repository code and uses no network access. The final version passed **125 of 125** named checks in ordinary Python and in Python with optimization enabled. The complete generated JSON outputs were byte-identical. The counts comprise **43 exact-rational checks, 2 elementary symbolic scope checks, and 80 non-interval numerical checks**. The output hash and environment are recorded in `verification.json`; full output can be regenerated with the supplied script.

The exact checks use scalar rational Schur elimination and the Chebyshev recurrence for j through 128. They verify the effective Hessian, its determinant, and the product/cofactor twist identity at four rational radii. These are identities at finitely many inputs, not a computer proof of the arbitrary-j theorem.

The independent physical calculation begins in the original initial collision angles, not the author's endpoint integral. It compares positive incoming intersections with a finite triangular-lattice patch, selects the first hit, and reflects the ray mechanically. High-precision differentiation at the normal segment computes the Hessian K_j of the actual total flight length in these coordinates. The checked identity is

$$\sqrt{\det K_j}=R\sinh(j\chi_R).$$

Since the angular section density at the normal state is 1/(4 pi), this reproduces C_j=3 lambda_R/(2 sqrt(det K_j)) without importing the author's endpoint Jacobian. Sixteen radius/order combinations were tested. The finite patch and local normal calculations are not a simulation of the full equilibrium billiard flow.

Nonlinear boundary-value tests separately check the reflection residual, positive relative twist, and two-amplitude quadratic scaling for j up to 128. They stress the relative estimate at large j, where an absolute estimate would be uninformative.

Finally, direct collision-angle quadrature at R=0.46 gives the following ratios. The denominator is the theorem's C_j epsilon^2, not a fitted coefficient.

| j | Number of impacts | epsilon=0.0001 | epsilon=0.00001 |
|---|---:|---:|---:|
| 1 | 2 | 0.999369099908 | 0.999936862198 |
| 2 | 3 | 0.999604406664 | 0.999960425777 |
| 3 | 4 | 0.999658353574 | 0.999965826002 |

A non-even smooth mark f(phi)=cos(phi)^2+(1/2)sin(phi), with source q=0.1, was also integrated along the actual reflected record. Dividing by C_j epsilon^2 exp(0.1(j+1)), the ratios for j=3 are 0.999582501163 and 0.999958234242 at the two displayed offsets. These calculations support the leading marked coefficient and cancellation scale; they do not test every smooth source or every parameter derivative.

For transparency, a preliminary version of the referee's own harness imposed an unjustified absolute cap of 5000 on a radius-dependent normalized quadratic coefficient. It failed near R=0.49, where the coefficient was about -7315 and the relative twist remained positive, approximately 0.98978. The theorem permits constants depending on K. This was a test-design error, not a manuscript counterexample. The final harness removes that arbitrary cap and instead tests positivity, mechanical consistency, and two-scale behavior. The final checks and their limits, rather than the discarded cap, are the evidence reported here.

No interval arithmetic, formal proof assistant, exhaustive continuum check, complete author-suite replay, manuscript PDF rebuild, visual PDF inspection, or remote CI execution was performed in this review. The author's 14+7-page build and 411-test account are author-reported evidence, not independently reproduced achievements of this referee. The mathematical assessment rests primarily on the source arguments. Finite agreement is corroboration, not proof or journal acceptance.

## 8. What a further submission should establish

A further submission should preserve the new theorem and present a reason for its significance that survives the information-redundancy and closest-literature comparisons above. A structurally broader geometric result or a genuinely new consequence within the present model could supply such a reason. Merely renaming the coefficient series as a spectral object would not.

Within the present argument, explicit record metrics and response test classes would remove avoidable ambiguity. A statement of the sharper axial source domain would be useful, although the conservative bound is already correct. The primary literature comparison should identify precisely which uniformity and differentiated physical observable are absent from the closest prior results.

The report does not require deletion of the old companion, inflation of the claim to unrestricted long time, or a numerical demonstration in place of analysis. Nor does it promise that completing any checklist would determine a journal's decision. The central issue is a mathematical contribution persuasive enough for the level requested.

## 9. Primary literature consulted

[1] J. Marklof, *Entry and return times for semi-flows*, Nonlinearity 30 (2017), 810--824. [Primary preprint](https://arxiv.org/abs/1605.02715). Stationary/Palm background; not the present uniform billiard geometry.

[2] S. V. Bolotin and D. V. Treschev, *Hill's formula*, Russian Mathematical Surveys 65 (2010), 191--257. [Primary preprint](https://arxiv.org/abs/1006.1532). Action-Hessian/monodromy context; the manuscript correctly does not claim a new general Hill formula.

[3] P. Balint, J. De Simoi, V. Kaloshin, and M. Leguil, *Marked length spectrum, homoclinic orbits and the geometry of open dispersing billiards*, Communications in Mathematical Physics 374 (2020), 1531--1575. [Primary preprint](https://arxiv.org/abs/1809.08947). Different inverse data and a different billiard family.

[4] M. Carney, M. Nicol, and H.-K. Zhang, *Compound Poisson law for hitting times to periodic orbits in two-dimensional hyperbolic systems*, arXiv:1709.00530, submitted September 2, 2017; journal DOI 10.1007/s10955-017-1893-9. [Primary preprint](https://arxiv.org/abs/1709.00530). Relevant statistical manifestation of periodic-orbit instability; not asserted to subsume the present physical onset theorem.

[5] M. F. Demers and H.-K. Zhang, *A functional analytic approach to perturbations of the Lorentz gas*, Communications in Mathematical Physics 324 (2013), 767--830. [Primary preprint](https://arxiv.org/abs/1210.1261). Perturbative operator comparison, not an automatic all-order record-response theorem.

[6] M. Demers, I. Melbourne, and M. Nicol, *Martingale approximations and anisotropic Banach spaces with an application to the time-one map of a Lorentz gas*, Nonlinearity 33 (2020), 4095--4113. [Primary preprint](https://arxiv.org/abs/1901.00131). Typical-orbit statistical limit laws, not the source-differentiated raw local Edgeworth theorem required by the historical A2 target.

## Final disposition

**Reject at the requested top-four-journal level as presented.** The latest revision contains a genuine, substantively stronger multi-collision theorem, and this review has not established a fatal error in its stated regime. The old one-roof and no-uniformity objections must be retired for that regime. The unresolved issue is whether the now credible local uniform analysis has been developed into a research contribution of the requested significance; the present applications and comparison do not establish that case. Preserve the theorem, its complete proofs, the companion, and the explicit separation from the historical long-time programme.
