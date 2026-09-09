# Independent referee report: A2 v5 — statistical contact rigidity

## Recommendation: reject at the requested top-four mathematics-journal level in its present form

**Date:** September 9, 2026 (Asia/Singapore).  
**Reviewer:** GPT-6 Astra Pro. This is an independent AI referee-style assessment requested by the repository owner, not a report commissioned by a journal or an actual editorial decision.  
**Author:** Qian Qi.  
**Title:** *Collision threshold laws and statistical contact rigidity in periodic dispersing billiards*.  
**Repository:** `TrillionniumFoundation/theta-theory`.  
**Reviewed branch:** `revision/a2-v5-statistical-contact-rigidity-2026-09-09`.  
**Frozen manuscript commit:** `1e57d9c024f90f0304e5572c0e320707bab88074`.  
**Commit time:** September 9, 2026, 03:43:02 UTC, or 11:43:02 Singapore time.  
**Frozen root tree:** `70686632d3f0bee18a9f6506b46fc16ceb4c6ee1`.  
**New review branch:** `review/a2-v5-statistical-contact-rigidity-harsh-independent-2026-09-09`.

All manuscript paths and labels below refer to `papers/A2-v5-statistical-contact-rigidity/` at the frozen commit, unless explicitly identified as historical. Source labels, not unverified PDF page numbers, are the controlling locators. The review branch adds review material only; it does not revise the author's manuscript.

The other parallel v5 branch, `revision/a2-v5-boundary-factorization-pairwise-recovery-2026-09-09`, was not selected: its inspected tip `ee879236d0fae1f84c685bef4ff27326403d4b2d` was timestamped 03:00:33 UTC. Its separate mathematical additions are not silently attributed to the later statistical-contact-rigidity manuscript. The selected branch still pointed to the frozen commit when checked again before delivery.

The controlling previous report is at review commit `ec861ecfcdd83a81880c1a9082becc19b0c76977`, path `reviews/a2-v4-nonlinear-boundary-laws-harsh-independent-2026-09-09/REFEREE_REPORT.md`, concerning v4 manuscript `68bbf5b841a66dcc2b85f4d76ce66b1ae8b9782f`. Its preserved copy in the present submission is `review-basis-v4/REFEREE_REPORT.md`.

## 1. Executive assessment

This is a materially stronger paper than v4. It is no longer accurate to describe its nonlinear geometric application as a single fourth-jet example, its unlabelled inverse as only a circular-reference estimate, or its preparation bound as excluding fine timing calibration. The revision has supplied an all-order triangular contact inverse, arbitrary finite-dimensional fixed-leading-data realizations, a positive pairwise inverse through a triple root, and an actual calibration experiment. These are mathematical changes, not merely changes in tone.

The principal new proofs examined here have survived the audit without an identified fatal counterexample. The top-jet diagonal has the correct action and determinant contributions. The four-amplitude map is regular in symmetric polynomial coordinates, and the root-matching step preserves multiplicities. The calibration argument does not evaluate a physical probability at a negative offset, and its fallback rule controls unconditional expected preparation cost even after a failed pilot. The inherited nonlinear relative-factorization proof retains a trace-class factor and is not an absolute-error estimate divided by an exponentially small twist.

Nevertheless, I do not recommend this version for one of the requested four journals. My objection is not that local theorems, elementary final computations, or special symmetry classes are intrinsically unsuitable for such journals. It is that the manuscript still has not made a sufficiently compelling case for the exceptional importance of this particular collection of results. Its genuinely difficult uniform result remains a relative boundary law around isolated alternating normal channels. The geometric rigidity now added is an exact germ determination that also follows from the explicitly computed one-flight nonlinear observation. The coalescence theorem has a genuine model-specific nondegeneracy calculation, but its singular exponent then comes from coefficient-to-root perturbation. The acquisition theorem is a careful local upper bound for a different, channel-resolved observation model. These are valuable results, but they do not automatically combine into a stronger single statistical rigidity theorem.

This report does not identify a previous theorem that contains the complete physical boundary-law statement. Nor does it claim that all the results are routine, false, or incapable of supporting a more important paper. The negative venue recommendation is an editorial assessment, not a mathematical impossibility statement.

Two additional calculations sharpen the assessment rather than merely repeat the old objections. First, the ratio between the limiting and one-flight top-jet diagonals is asymptotic to `(tanh gamma)^m` at jet order `2m`. Thus exact identifiability does not by itself supply a high-order conditioning advantage for the long-bridge datum. Second, in the author's original physical three-parameter family, the first **three** amplitudes already give a local pairwise inverse near the circle with `R=1/4`; the fourth amplitude is useful for the enlarged model with independently unknown area. Full derivations appear in Sections 3 and 4. Neither observation is a counterexample to a correctly restricted theorem.

## 2. Disposition of the previous report and proof audit

### 2.1 The controlling requests have been answered

| Previous request | Disposition in v5 |
|---|---|
| NBL-R1: distinguish nonlinear information from information exclusive to long records | Substantively answered. `prop:v5-one-flight` gives the comparison at every even order; `thm:v5-jets` and `thm:v5-realization` go well beyond the previous one-parameter example. The absence of a strictly increasing information hierarchy is expressly acknowledged. |
| NBL-R2: distinguish a reference-point bound from a nearby pairwise inverse | Answered positively, not just by another obstruction. `thm:v5-pairwise` proves a four-amplitude inverse with multiplicities, and `thm:v5-sharpness` supplies the matching physical cubic path in the whole weighted-sequence topology. |
| NBL-R3: distinguish supplied timing from charged calibration | Answered within an explicit local experiment. `prop:v5-harmonic` records the uncancelled sensitivity, while `lem:v5-calibration` and `thm:v5-self-calibration` charge fine calibration and retain a safe window on all pilot outcomes. The initial coarse bracket remains a supplied assumption, clearly stated. |
| Differentiated operator norms and moving principal poles | Addressed in `v5/15_differentiated_operators.tex`. Derivatives need bounded trace norms, not smallness; parameter differentiation can increase the principal pole order. |
| De Simoi–Kaloshin–Leguil comparison | Added to the bibliography and discussed with its different hypotheses and observation. The old missing-reference objection is closed. |

It would be unfair to retain these matters as unchanged proof defects. Conversely, successful response to a previous referee's requests is not itself a sufficient importance criterion for a top-four recommendation. The present negative assessment must stand on the revised mathematics, not on an ever-growing checklist of corollaries.

### 2.2 Geometry, the uniform bridge, and physical normalization

**Locators:** `v3/10_geometry_action.tex`, `lem:g-channels`, `lem:g-jacobi`, `lem:g-relative`; `v3/20_integration.tex`, `lem:g-radial`, proof of `thm:g-stability`.

The reference geometry is genuinely more general than a near-circular ansatz. Periodicity and separation leave finitely many pairs below any fixed distance bound. Strict convexity gives unique closest support points. Positive curvature gives a positive-definite contact Hessian. A shortest chord cannot meet a third obstacle, and finitely many separated outgoing normal states force successive sufficiently short reflected flights to reverse the same channel. Since every complete flight is at least the minimum gap, a small total excess bounds every individual excess without a collision-order-dependent loss. A nonminimal clear chord is correctly treated as a selected itinerary, not as the complete unlabelled count event at its own onset.

The alternating Jacobi scaling is retained. With `c_b=1+g kappa_b`, `c=sqrt(c_0 c_1)`, and `gamma=arcosh c`, the endpoint Hessian is uniformly positive although its mixed derivative is exponentially small. Those two facts are not confused in the nonlinear inversion. The weighted Green estimate controls stationary coordinates by two summable endpoint layers. The cofactor identity is

$$-W_{uv}=\frac{\prod_i[-\ell_{i,uv}]}{\det H_{\mathrm{int}}}.$$

The logarithm of its normalized version is controlled by the sum of local edge perturbations and a relative determinant. Tridiagonality and endpoint localization give a trace-norm estimate independent of the number of interior sites. The proof does not replace this with a dimension times operator-norm bound.

The first-impact phase density is

$$\frac{-W_{uv}}{2\pi A}\,du\,dv\,dr.$$

The residual interval is shorter than every preceding roof, and the terminal remainder is too short to add a collision. This justifies the full-phase residual-time integral without a finite-horizon assumption. The constructive Morse map uses the positive endpoint Hessian, not the small twist, as its inverse scale. Radial cancellation of odd Taylor terms gives a smooth right function of the offset even for nonsymmetric graphs. I find the physical normalization and the collision-order-uniform remainder argument coherent under the printed hypotheses.

### 2.3 Relative boundary factorization and the limiting probability

**Locators:** `v4/10_boundary_layers.tex`, `lem:v4-halfline`, `thm:v4-factorization`, `thm:v4-law`; `v5/15_differentiated_operators.tex`.

The half-line contraction constructs decaying stationary segments; strict diagonal dominance also gives uniqueness among sufficiently small bounded decaying segments. The action sums and local Hessian perturbations are summable. The half-line determinant amplitude has an explicit logarithmic definition, so there is no unspecified infinite-volume normalization.

The finite-to-half-line comparison is the strongest analytical part of the paper. Gluing the two endpoint layers produces an exponentially small summable residual. Truncating the determinant perturbation to separated end blocks costs trace norm. The compressed finite Green kernels approach the two half-line kernels, while their cross-block entries are exponentially small. Telescoping the logarithmic determinant series preserves one trace-class factor. Fixed derivatives introduce polynomial factors in the series index or bridge length, absorbed by strict exponential margins. The v5 addendum correctly requires smallness only at zeroth order.

The passage to physical probabilities also contains the necessary argument at `d=0`. Both actions are compared through common Morse coordinates, with uniformly controlled inverse maps and amplitudes. This is not formal differentiation of a moving sharp boundary. The limiting endpoint amplitudes factor, but the probability itself does not: the shared inequality `S_0(u)+S_p(v)+r<d` couples the ends. The scaled bounded-Lipschitz statement avoids an inappropriate total-variation comparison of differently embedded full-record surfaces.

The first-pole calculation is a consequence of the exponentially accurate parity limits. It is not a new statement about pressure or arbitrary long itineraries. The corrected discussion of moving poles is mathematically appropriate. These consequences should be credited at their actual level, without being counted as independent theories.

### 2.4 The all-order contact inverse

**Locator:** `v5/20_contact_rigidity.tex`, `thm:v5-jets`, equations `eq:v5-diagonal` through `eq:v5-amplitude-diagonal`.

The finite-jet argument is essential: a nonzero formal diagonal alone would not prove a triangular inverse. The source gives the required recursive stationary-equation construction and explains why the coefficient of `d^(m-1)` uses the action only through degree `2m` and the amplitude only through degree `2m-2`. The summable differentiated half-line bounds justify the limiting version of this bookkeeping.

At fixed lower jets, variation of `q_(2m)` first changes the one-flight length by

$$\frac{u^{2m}+v^{2m}}{(2m)!}.$$

Substitution of the linear half-line segment `x_i=lambda^i u` in the stationary action gives

$$\partial_{q_{2m}}S^{(2m)}(0)=1+2\sum_{i\ge1}\lambda^{2mi}=\coth(m\gamma).$$

The factor two on interior sites is necessary and present. The first varying local term has zero mixed derivative, so the edge product has no contribution at degree `2m-2`. The determinant contribution comes from the diagonal Hessian variation and the half-line Green diagonal. The change of the stationary segment cannot enter at this degree in the identical-even class. Consequently

$$\partial_{q_{2m}}[u^{2m-2}]B(u)
=-\frac{D_m}{a(2m-2)!},\qquad
D_m=\frac1{e^{2(m-1)\gamma}-1}-\frac1{e^{2m\gamma}-1}.$$

Integration with the residual-time weight, rather than an unweighted conditional disk law, then gives the stated diagonal

$$\partial_{q_{2m}}f_{m-1}
=-\frac{4}{2^m(m+1)(m!)^2a^m}
 \bigl[\coth(m\gamma)+2mD_m\bigr]<0.$$

The affinity in the last jet follows from the degree restriction, not merely from evaluating a derivative at the disk. Nonvanishing gives the recursive inverse at every fixed finite order. Exponentially convergent finite-bridge recovery follows from the differentiated boundary law and the finite-dimensional inverse bound. The author explicitly does not claim a bound uniform in the number of recovered jets.

The analytic continuation corollary is an exact uniqueness assertion in a restricted class. Equality of the analytic contact germs gives equality of the arclength curvature functions and hence, by the common initial frame and Frenet equations, of each participating boundary image. It does not recover an unknown lattice, unseen obstacles, or a noisy global boundary. The proof observes those restrictions.

The realization theorem has a genuine geometric compensator. The support perturbations `sin^(2m)(theta)` fix the support values and curvature radii at the contact normals. The `sin^(2M+2)(theta)` direction corrects area without altering the selected jets. The support-to-graph diagonal `-(2m)!` is nonzero; positivity and clearance persist in a small neighborhood. This is an arbitrary fixed finite-dimensional realization, not a claimed uniformly controlled infinite-dimensional family.

### 2.5 Four amplitudes through coalescence

**Locator:** `v5/40_pairwise_inverse.tex`, `thm:v5-pairwise`, `thm:v5-sharpness`.

The coefficient-space extension is the correct way to cross the triple-root stratum. If `e_1,e_2,e_3` are the elementary symmetric polynomials of the radius deviations, the contour sum involving `p_e'/p_e` extends the observation to a full analytic coefficient neighborhood, including non-real-rooted polynomials. The inverse-function theorem is applied there, and only then restricted to the physical real-rooted set. It is not an inverse theorem for differentiably labelled roots at coalescence.

The Jacobian columns have the correct signs and factors: the symmetric sum contributes `Phi'`, `-Phi''`, and `Phi'''/2`; area contributes `-3 Phi/A_0^2`. Independent symbolic differentiation confirms

$$\det[f_j^{(k)}(c)]_{j=1,\ldots,4;\,k=0,\ldots,3}
=\frac{12(64c^8+32c^6+116c^4+4c^2+1)}
 {c^4(4c^2-1)^4(2c^2-1)^4}>0.$$

The Rouché argument on the union of disks around the roots correctly retains multiplicities and gives a matching error of order the coefficient error to the power `1/3`. The compact discrepancy-minimization construction supplies a noisy-data estimator without assuming that noisy data lie in the exact image.

The sharpness proof is also appropriately quantified. The physical path has

$$r(s)=(R+36s,R-18s,R-18s),\qquad A(s)=A_0+45\pi s^2/4.$$

The strict exponential margin absorbs the polynomial-in-order derivative bounds, so the upper estimate holds in the whole weighted sequence norm, not just a numerical prefix. Moreover,

$$\Phi_1'''(R)=\frac{3(3g+R)}{\sqrt g\,(g+2R)^{7/2}}>0,$$

$$C_1(s)-C_1(-s)=\frac{11664\Phi_1'''(R)}{A_0}s^3+O(s^5),$$

and the sorted matching distance is `36|s|/(R^2-324s^2)` for sufficiently small `s`. This proves optimality of the pairwise exponent in the specified amplitude topology. It is not a contradiction to the retained circular-reference exponent `1/2`.

### 2.6 Calibration and acquisition

**Locator:** `v5/50_self_calibration.tex`; its dependencies `prop:v3-sampling`, `thm:v3-tomography`, and `prop:v4-timing`.

The harmonic timing derivative is correct. The identity `sum_l omega_l/l=H_m` yields a leading term `-v H_m/h`; extrapolation does not cancel the denominator error. The pilot experiment repairs this by estimating the onset rather than pretending the error is cancelled.

At the positive programmed nodes, square-root probabilities have the form `sqrt(K_j)(z-tau)H_j(z-tau)`. Multiplication of a right Taylor polynomial for `H_j` by `z-tau` gives an approximating polynomial with a simple root. The Lagrange value and derivative estimates control extrapolation back to the bracketing interval. The proof uses no negative-offset physical probability, and the unknown common prefactor does not affect the root.

Waiting for a prescribed number of successes supplies relative probability concentration through the binomial/negative-binomial duality. Fresh preparations are used in the conditional-position stage. The root/fallback convention keeps the pilot estimate in `[-h/2,h/2]`, while the true shift lies in `[-h/4,h/4]`. Thus every second-stage offset is at least `h/4` on every outcome, not merely on the high-probability success event. This is what makes the unconditional expectation bound valid.

The resulting sufficient cost is correctly local: it includes fine calibration but presupposes the initial coarse bracket, fixed channel patches, noiseless recording, and independent full-phase preparations. The constants depend on the fixed extrapolation order. The proof is not a minimax theorem, a global onset-search algorithm, or an argument that successive impacts are independent. Those exclusions are already in the text and are not unresolved errors.

## 3. A new conditioning comparison for the contact inverse

**Relevant locators:** `eq:v5-diagonal`, `eq:v5-one-flight`, `prop:v5-one-flight`.

The revision correctly establishes identical exact identifiability from the limiting and one-flight nonlinear germs in the identical-even class. A sharper comparison can be read directly from its two diagonal formulas. Write

$$D_m^{\infty}=\left|\partial_{q_{2m}}f_{m-1}\right|,
\qquad D_m^{(1)}=\left|\partial_{q_{2m}}f_{1,m-1}\right|.$$

Since `a=sinh(gamma)/g` and `nu_1=g cosh(gamma)/sinh^2(gamma)`, one has `a nu_1=coth(gamma)`. Therefore

$$\boxed{\frac{D_m^{\infty}}{D_m^{(1)}}
=(\tanh\gamma)^m\,[\coth(m\gamma)+2mD_m].} \tag{R1}$$

For each fixed positive `gamma`,

$$\coth(m\gamma)+2mD_m
=1+O_\gamma\bigl(m e^{-2(m-1)\gamma}\bigr),$$

so the ratio in (R1) is asymptotic to `(tanh gamma)^m`. This is not an artifact of using factorial rather than ordinary graph coefficients: the same reparametrization multiplies both diagonals and cancels in the ratio.

For example, at `g=kappa=1`, the ratios for `m=2,3,4,8` are approximately `0.97427858`, `0.66875`, `0.56407637`, and `0.31640630`. At fixed lower jets and equal absolute error in the corresponding coefficient, the inverse diagonal amplification is the reciprocal of this ratio. Thus the limiting datum is asymptotically less sensitive to the highest jet in this precise coefficient comparison.

Several limitations are important. This is a statement about local diagonal sensitivity in coefficient coordinates, not the condition number of an entire triangular inverse, not a minimax comparison of experiments, and not a proof that all long records are statistically inferior under every cost model. Extracting coefficients from noisy probabilities introduces another inverse problem. The manuscript does not claim uniformity in `m`, so (R1) does not refute `thm:v5-jets`.

It does, however, make the importance question more concrete. A new global uniqueness corollary cannot by itself demonstrate that the long-bridge construction unlocks geometric information inaccessible to the finite observation; the paper itself proves the opposite in this class. The significance of the uniform factorization must be explained on its own mathematical merits. I recommend including a short coefficient-sensitivity comparison, rather than leaving the reader to infer a conditioning benefit from the phrase “statistical rigidity.” This request is a benchmark and interpretation request, not a demand to retract the contact theorem.

## 4. The original physical family needs only three amplitudes locally

**Relevant locators:** `v3/40_inverse.tex`, `eq:g-isogap-family`, `eq:v3-area`; `v5/40_pairwise_inverse.tex`, `eq:v5-amplitude-model`.

The four-amplitude theorem is correct for its four-dimensional ambient model with independently unknown `A`. It should not be confused with a minimal-data theorem for the original three-parameter support family. Here is a local sharpening in that physical family.

Fix `R`, hence the known gap `g=1-2R`, and put `x_i=r_i-R`. Let `e_1,e_2,e_3` be their elementary symmetric polynomials. The linear relation between `(alpha,beta,zeta)` and the three radius deviations gives

$$\alpha=\frac{e_1}{108},\qquad
\beta^2+\zeta^2=\frac{e_1^2}{2916}-\frac{e_2}{972}.$$

Substitution into the printed area identity yields

$$\boxed{A(e)=A_0-\frac{\pi R}{54}e_1
+\frac{41\pi}{7776}e_1^2-\frac{5\pi}{432}e_2,
\qquad A_0=\frac{\sqrt3}{2}-\pi R^2.} \tag{R2}$$

Let `M_j(e)` be the same analytic symmetric sum used in the author's contour construction. Consider the **three-dimensional** observation

$$\Psi_3(e)=\bigl(A(e)^{-1}M_j(e)\bigr)_{j=1}^3.$$

Its derivative at zero has rows

$$\frac1{A_0}\left(
\Phi_j'(R)+\frac{\pi R}{18A_0}\Phi_j(R),\;
-\Phi_j''(R)+\frac{5\pi}{144A_0}\Phi_j(R),\;
\frac12\Phi_j'''(R)\right). \tag{R3}$$

At the admissible physical reference `R=1/4`, `g=1/2`, direct differentiation gives

$$\boxed{\det D\Psi_3(0)
=-\frac{2\sqrt2\,(15804720A_0+64253\pi)}
 {72930375A_0^4}\ne0,
\qquad A_0=\frac{\sqrt3}{2}-\frac\pi{16}>0.} \tag{R4}$$

For reproducibility, the derivatives of the first three `Phi_j` at this reference, divided by `sqrt(2)`, are

| j | Phi_j | Phi_j' | Phi_j'' | Phi_j''' |
|---:|---:|---:|---:|---:|
| 1 | 1/4 | 3/4 | -5/4 | 21/4 |
| 2 | 1/24 | 17/72 | 35/216 | -491/216 |
| 3 | 1/140 | 297/4900 | 36243/171500 | -4458537/6002500 |

Insertion of this table into (R3) gives (R4); its sign follows from positive `A_0` and `pi`, not from a floating determinant. Its numerical value is approximately `-2.079860474347108`.

The analytic inverse-function theorem now gives locally Lipschitz recovery of `(e_1,e_2,e_3)` from `(C_1,C_2,C_3)`. Restrict to the real-rooted physical parameter set and apply the same multiplicity-preserving root estimate as in the manuscript. On a sufficiently small neighborhood of this physical circle,

$$|A-\widetilde A|\le C\delta_3,
\qquad \operatorname{dist}_{\rm match}(\kappa,\widetilde\kappa)
\le C\delta_3^{1/3},
\qquad \delta_3=\max_{1\le j\le3}|C_j-\widetilde C_j|. \tag{R5}$$

The same physical two-sided path has a nonzero cubic first-amplitude difference, so the exponent remains sharp there. This calculation establishes a local result near the specified radius, not a global assertion for every radius in `(0,1/2)`.

The conclusion is not that the fourth-amplitude theorem is false or useless. Its additional content is robustness to an **independent area nuisance parameter**, which is a legitimate stronger observation model. But the introduction to the section should not suggest that a fourth amplitude is intrinsically needed to solve the physical three-parameter problem. The manuscript already says area is constrained in that family; the calculation above makes the consequence explicit. It would improve the paper to distinguish physical three-parameter identifiability from ambient four-parameter robustness, rather than count them as the same advance.

## 5. Remaining issues in statement, data model, and importance

### 5.1 State the equal-facing-curvature restriction in the abstract

The abstract says that for three unlabelled equal-gap channels the first four amplitudes recover the area and curvature multiset. Read literally together with the general nonsymmetric setup, this is too broad. For a general channel the scalar leading coefficients depend on

$$c_e=\sqrt{(1+g\kappa_{e,0})(1+g\kappa_{e,1})},$$

not on its two actual curvatures separately. At `g=1`, the family

$$\kappa_0(s)=2e^s-1,\qquad \kappa_1(s)=2e^{-s}-1$$

has constant `c_e=2` while its curvatures vary. This is not only a formal algebraic ambiguity: the inherited `thm:v3-fibers` realizes the phenomenon with fixed gap and area in actual periodic obstacles.

The four-node-function model uses `c=1+g/r`. Its interpretation as an actual curvature `1/r` requires equal curvatures at the two ends of each channel, as in the centrally symmetric physical family. Without that restriction it recovers effective channel parameters, not all the actual endpoint curvatures. The formal inverse theorem specifies its model and is not invalidated by this observation. The abstract's final statement that additional inverse assumptions are given separately helps, but does not replace naming this decisive assumption next to the curvature claim.

A suitable correction is: “For three unlabelled equal-gap channels with equal facing curvatures in each channel, ...”. Alternatively, use “effective channel parameters” for the broader interpretation. This is a precise hypothesis/observable correction, not a request to weaken a theorem that was actually proved.

### 5.2 Do not concatenate different inverse and sampling theorems

Four exact leading amplitudes, a whole normalized probability germ, and a finite set of raw collision records are different observations. The paper is usually careful about this, but the chain of applications can still leave an unwarranted impression that one final preparation bound covers the whole rigidity package.

The jet theorem has fixed finite-jet Lipschitz bounds in coefficient coordinates; it does not bound extracting those coefficients from noisy probability values or performing analytic continuation. The pairwise theorem assumes deterministic errors in leading onset coefficients. The self-calibrated acquisition theorem estimates two curvatures from positions in a **selected** channel. It does not estimate an unlabelled coalescing triple from count data alone at that same rate. Its coarse bracket is supplied, not acquired. Each theorem is valid with its own quantifiers, but their rates cannot simply be transferred between these observations.

A basic count-only calculation illustrates the distinction without invoking a new impossibility claim. For fixed flight numbers `j=1,...,4`, known common gap, and a compact equal-gap physical family, write

$$p_j(d)=d^2[C_j+dB_j(d)].$$

At a positive offset `d`, an empirical probability from `n` independent preparations has

$$\operatorname{Var}\!\left(\frac{\widehat p_j(d)}{d^2}\right)
=\frac{p_j(d)(1-p_j(d))}{nd^4}\le\frac{C}{nd^2}. \tag{R6}$$

Use fixed-order extrapolation at `d=lh`, `l=1,...,m`. The differentiated threshold law supplies bias `O_m(h^m)`. Bernoulli concentration supplies a stochastic term of order

$$C_m\left[\sqrt{\frac{\log(C_m/\eta)}{nh^2}}
+\frac{\log(C_m/\eta)}{nh^2}\right].$$

Taking `h` of order `delta^(1/m)` and `n` of order `delta^(-2-2/m) log(C_m/eta)` suffices for amplitude error `delta`. Composing with the printed pairwise `1/3` estimate gives the elementary sufficient count-only curvature-accuracy order

$$C_m\varepsilon^{-(6+6/m)}\log(C_m/\eta). \tag{R7}$$

The fixed number of flight orders and offsets is absorbed in `C_m`. This is a baseline upper bound with **known gap**, not a minimax rate, not a charged unknown-gap experiment, and not a claim that better methods are impossible. The purpose is to show why the selected-position rate `epsilon^(-2-2/m)` cannot simply be read as the count-only coalescence rate. Including a data-model table, or a carefully qualified corollary of this type, would clarify the connection. Its absence is not a surviving failure of NBL-R3, which the revision has answered for the stated selected-channel experiment.

### 5.3 The significance argument must be about the central mechanism

The strongest coherent main chain is: geometric localization, a common nonlinear bridge, relative two-boundary determinant factorization, and the normalized physical law. The all-order contact inverse is a meaningful application, but its one-flight counterpart must remain adjacent to it. The four-amplitude result is a finite analytic observation-map theorem with a specific nonzero Wronskian. The calibration result is a valid statistical use of quadratic onset vanishing. The manuscript should explain why this combination changes the understanding of the subject, rather than rely on the number of different application headings.

The selected paper's uniform chain remains alternating and locally attached to period-two normal channels. That is a scope description, not a defect: the paper does not assert an arbitrary-itinerary theorem. A wider transfer principle, a consequential application essentially using the uniform relative law, or a convincing resolution of a recognized obstruction could support a stronger importance case. None is imposed here as a mandatory extra theorem, and no particular enlargement is promised to produce acceptance. A proof of exceptional depth or a sufficiently important local result could also suffice. What is missing from the current presentation is a persuasive case of that kind for the actual result proved.

The new realization and pairwise estimates deserve more credit than the corresponding v4 examples. They nevertheless do not remove the need for this importance argument. Treating a repaired counterexample, a nonzero Jacobian, or a polynomial extrapolation identity as an additional independent conceptual breakthrough would exaggerate the revision.

### 5.4 A closer spectral-jet comparison is needed

The addition of De Simoi–Kaloshin–Leguil is appropriate and resolves the previous bibliographic request. Their marked-length determination theorem has a different datum, an open no-eclipse configuration, and symmetry/genericity assumptions [3]. It should not be claimed to imply this paper's statistical law.

The new all-order analytic contact determination also makes the comparison with Zelditch's work on analytic domains pertinent [1]. That paper uses localized wave-trace expansions near periodic billiard orbits to obtain spectral determination in symmetry classes. The observations and geometric setting differ from the current normalized probabilities, so no direct containment or equivalence is asserted. Nevertheless, an article whose main new application is recovery of analytic boundary data through successive coefficients should discuss this closely related coefficient-to-geometry strategy, not compare only with marked lengths. The relevant question is which part of the present coefficient extraction and nonvanishing mechanism is new for its statistical datum, and which part is the familiar passage from successively recovered local data to analytic uniqueness.

Hill-type determinant identities [2] explain an important predecessor structure but do not by themselves establish the relative physical-flux limit here. Prony-type accuracy work [4] is relevant to the coalescence observation, but the manuscript correctly uses a model-specific Wronskian and an elementary root estimate rather than claiming a new general Prony theory.

These are targeted primary-source comparisons. This review inspected primary abstract/bibliographic pages, not every proof in these papers, and does not issue an exhaustive priority certificate. A missing citation is not evidence that the principal theorem is already known, nor a stand-alone reason for the negative venue judgment.

## 6. Concrete disposition requested from the author

| ID | Classification | Required disposition |
|---|---|---|
| SCR-R1 | Statement/observable correction | Put the equal-facing-curvature assumption next to the abstract's actual-curvature multiset claim, or use effective channel parameters. Preserve the more general forward theorem. |
| SCR-R2 | Conditioning and interpretation | Explain the difference between exact germ uniqueness, fixed finite-jet inversion, and noisy geometric recovery. Address the diagonal comparison (R1), without promoting it to an unsupported minimax statement. |
| SCR-R3 | Observation-model clarification | Distinguish the physical constrained-area family from the ambient independent-area model. The four-amplitude theorem is valid; (R2)–(R5) show why four should not be advertised as intrinsically required in the physical family. |
| SCR-R4 | Statistical scope and exposition | Keep the unlabelled amplitude inverse separate from the selected-position acquisition rate. A data-model comparison or a qualified baseline such as (R6)–(R7) would make the distinction explicit. Do not hide the supplied coarse bracket. |
| SCR-R5 | Principal editorial issue | Recast the importance argument around the relative boundary-law mechanism and its actual consequences; add the relevant analytic spectral-jet comparison with accurate hypotheses. More formulas or diagnostics alone do not settle this issue. |

SCR-R1 is a concrete correction to the headline formulation. SCR-R2 through SCR-R4 are substantive interpretation and model-separation requests supported by explicit calculations, not fatal counterexamples to the restricted statements. SCR-R5 is the main reason I withhold a top-four recommendation. I do not request arbitrary deletion of correct results, abandonment of the program, or an unsupported reduction of the general forward setting to the symmetry assumptions of one inverse application. Historical derivations can and should remain available.

## 7. Independent diagnostics and limits of this review

The accompanying `independent_diagnostics.py` imports no repository code and makes no network calls. It completed **104 of 104 named checks**, both normally and under `python -O`, with byte-identical JSON output within the executed environment. There are **85 exact identities** and **19 ordinary floating, non-interval comparisons**. Explicit failure exceptions are used; correctness checks do not disappear under Python optimization.

The exact identities include the four-function Wronskian, the first-amplitude third radius derivative, the physical two-sided cubic multiplier, the support-function area from its Fourier coefficients, the symmetric area formula (R2), the three-amplitude Jacobian (R4), the disk moments and action diagonal constants through several fixed orders, and the extrapolation/harmonic identities through order ten. These are finite checks of formulas, not independent proofs of the entire infinite-order or operator statements.

The nonlinear quadrature checks the actual one-flight length and mixed-derivative flux for local graphs `psi_q(y)=y^2/2+q y^(2m)/(2m)!` at `q=0`. It differentiates the full residual-time integral, solving the actual radial sublevel boundary. It does not merely evaluate the claimed diagonal formula. With 96 angular directions and 32 radial Gauss nodes, selected results are:

| Jet | Predicted coefficient derivative | Estimate at d=0.004 | Estimate at d=0.00025 |
|---:|---:|---:|---:|
| q4 | -0.0370370370370 | -0.0369929025176 | -0.0370342725275 |
| q6 | -0.00102880658436 | -0.00102819079488 | -0.00102876800998 |
| q8 | -0.0000171467764060 | -0.0000171467832695 | -0.0000171467764331 |
| q10 | -0.000000190519737845 | -0.000000190634594284 | -0.000000190526919903 |

An intermediate offset `d=0.001` is also recorded by the script. These comparisons support the finite-order normalization and signs, but ordinary quadrature is not an interval certificate. The local polynomial graphs in this check are not a simulation of an entire area-compensated periodic billiard. No continuum theorem is inferred from a test count.

Executed environment: Python 3.13.5, NumPy 2.3.5, SciPy 1.17.0, SymPy 1.14.0. The executed script SHA-256 is `5efd14dba0b73bcd843e782c13ff0adb18ca7219dace8ca5a3737f1fa373a29d`. The full generated diagnostic JSON has SHA-256 `ef6278e7b01d505b207b64b43ec280768dcb51e286501c9d0e3651eebaabbe52`. `VERIFICATION.json` records the commands, key outputs, source pins, and limitations. The script regenerates the detailed JSON; cross-version floating-point byte identity is not promised.

The source audit covered the complete new v5 mathematical chapters, their introduction and comparison, the v3 geometric/relative-flux and physical-integration foundations, the conditional-variance and realized-leading-fiber arguments, the v4 boundary-factorization and acquisition arguments, the relevant physical unlabelled-family and area formulas, the response letter and proof ledger, and the controlling v4 report's assessment and requests. This is a focused independent re-review of the revised main chain, not a claim to have re-proved every active appendix or every historical branch. The unchanged circular appendices, moving-cut record sections, two-collision companion, and Round 33 chapter were not separately re-audited in this round.

I did not rerun the author's 175-check suite, rebuild or inspect manuscript PDFs, certify remote CI, use interval arithmetic, run a proof assistant, or audit every cited external proof. The author's build and delivery claims are not represented as my own executed build. No inference about mathematical correctness is drawn from whether a workflow is green, pending, or unavailable.

## 8. Final recommendation

The author has substantially and successfully answered the controlling mathematical requests. The relative nonlinear boundary law remains the central achievement; the new all-order contact inverse, finite geometric realization, pairwise coalescence estimate, and locally charged calibration strengthen the paper. I identify no fatal error in the central proofs examined here.

My recommendation nevertheless remains **reject at the requested top-four mathematics-journal level in the present form**, principally because the manuscript has not yet demonstrated the exceptional importance of its specialized central mechanism and the exact inverse consequences now attached to it. This is not a verdict that the theorems are false, that the revision is cosmetic, or that the research program cannot progress. The concrete corrections and comparisons above should be addressed independently of that editorial judgment. No claim of journal acceptance, formal proof certification, or completion of unreviewed historical work is made.

## Primary references consulted

[1] S. Zelditch, *Inverse spectral problem for analytic domains, II: Z2-symmetric domains*, Annals of Mathematics 170 (2009), 205–269. DOI: 10.4007/annals.2009.170.205. Primary publisher abstract and bibliographic record: https://annals.math.princeton.edu/2009/170-1/p06.

[2] S. Bolotin and D. Treschev, *Hill's formula*, Russian Mathematical Surveys 65 (2010), no. 2. DOI: 10.1070/RM2010v065n02ABEH004671. Primary abstract: https://arxiv.org/abs/1006.1532.

[3] J. De Simoi, V. Kaloshin and M. Leguil, *Marked Length Spectral determination of analytic chaotic billiards with axial symmetries*, Inventiones Mathematicae 233 (2023), 829–901. DOI: 10.1007/s00222-023-01191-8. Primary abstract and revision metadata: https://arxiv.org/abs/1905.00890. Institutional bibliographic record: https://research-explorer.ista.ac.at/record/12877.

[4] D. Batenkov and Y. Yomdin, *On the accuracy of solving confluent Prony systems*, SIAM Journal on Applied Mathematics 73 (2013), no. 1, 134–154. DOI: 10.1137/110836584. Primary abstract and bibliographic record: https://arxiv.org/abs/1106.1137.
