# External top-four referee report on A2 v26

**Manuscript:** Qian Qi, *Collision-generated geometry for reference-free reconstruction*  
**Reviewed revision:** `revision/a2-v26-collision-certification-2026-10-03`  
**Equivalent referee-copy alias:** `revision/a2-v26-referee-copy-2026-10-03`  
**Reviewed commit:** `8c6f1113296c5401258ff052e5ce734fabfb3909`  
**Reviewed tree:** `fafe34398d8373736634b8c045c3063dc4c997cb`  
**Mathematical checkpoint:** `23a0ac311f6864807a3d538f3658ff07d341c269`  
**Controlling preceding report:** `aec09874d30f06dcbac1d1b7858fe96364f9d8d7`  
**Manuscript directory:** `papers/A2-v26-adaptive-recognition`  
**Date:** 3 October 2026  
**Requested benchmark:** *Annals of Mathematics* / *Acta Mathematica* / *Inventiones Mathematicae* / *Journal of the AMS*  
**Status:** author-requested, AI-assisted referee-style assessment; not a journal decision or a formal proof certificate.

## 1. Recommendation

**Recommendation at the requested four-journal benchmark: reject.**

Version 26 is a genuine and substantial mathematical revision. It answers the most serious concrete objection in the v25 report rather than merely relabelling the old information contract. The earlier scheme used arbitrarily accurate local boundary-value, derivative, arclength and distance-to-solid queries and then analytically continued a short contact arc to a complete body. The new primary instead starts from resettable spatial launches and recorded collision positions and times. First-impact point clouds reconstruct complete encountered convex bodies; finite support fingerprints recognize repeated bridge classes; raw proposals are revalidated from fresh clouds at every epoch; and the whole-table certificate is now formulated on a fixed finite-smoothness \(C^{6,\beta}\) class rather than an analytic continuation class.

On the new v26 core audited in detail, I found no fatal counterexample. The first-hit flux minorization, boundary coupon estimate, convex-hull envelope, positive and compensated smoothing bounds, complete-pair fingerprint, normal-root certificate, fresh-cloud revalidation, endpoint histogram error, local action inverse, rational period recovery, completion defect and anytime stopping argument are coherent under the stated numerical priors. The independent finite diagnostics accompanying this report support the displayed algebra and exponent balances. The negative recommendation is therefore not based on a known false central theorem.

The remaining objection is editorial and conceptual. The observation is still unusually rich and purpose-built. The experimenter may reset the dynamics, choose starting positions in prescribed laboratory squares, choose independent directions, request certified collision-position accuracy, launch additional clouds around previously observed contacts and flights, and repeatedly reacquire every retained proposal. The final inverse also observes two growing two-dimensional endpoint histograms per record with an absolute normalization by the free area of the entire unknown periodic cell. These capabilities are mathematically explicit, but they are far stronger than a passive trajectory, a marked length spectrum, collision counts, or a conventional scattering invariant.

The theorem also depends decisively on a compact generic prior: bounded obstacle count and lattice presentations, positive body-area and covolume gaps, positive separation and curvature bounds, pairwise shape separation, quantitative absence of rotations and reflections, a connected uniformly clear short-bridge network, and uniform twist, non-grazing, time-collar and active-window margins. The probabilistic and numerical layer is careful, but once genuine collision clouds and protected records are available, its principal ingredients are classical convex-hull approximation, kernel smoothing, finite separation, rational lattice arithmetic, conditional concentration and coupon bounds.

In my judgment this is serious and potentially strong specialist-journal mathematics. It materially improves the earlier versions and removes both analytic continuation and the deterministic boundary/distance oracle. It does not, however, establish rigidity from a natural standard dynamical invariant or transform the broader rigidity theory at the exceptional level required by the four journals named above. I would encourage a focused specialist submission after a fresh human proof review, completion of the exact-source qualification, and the presentation clarification in Section 8 below. I would not recommend another open-ended revision cycle at the requested top-four benchmark.

## 2. Frozen source and chronology

The two v26 branch names listed above resolve to the same author head

`8c6f1113296c5401258ff052e5ce734fabfb3909`

with repository tree

`fafe34398d8373736634b8c045c3063dc4c997cb`.

The final head is one commit after the mathematical checkpoint

`23a0ac311f6864807a3d538f3658ff07d341c269`.

A direct Git comparison shows that this last commit adds only `DELIVERY_STATUS.md`, `MATHEMATICAL_SOURCE_PINS.json`, `README.md` and `RESPONSE_TO_REFEREES.md` under the v26 directory. It does not modify the active mathematical source. The source pins identify the retained v25 paper tree as

`c48d900f6596eea1e8df1f729481674fb1bf6175`

and the older complete supplement tree as

`14b2e5379e5b223bc0bdc823c97fd77c2dca2cda`.

The controlling v25 report is pinned at commit

`aec09874d30f06dcbac1d1b7858fe96364f9d8d7`

with report blob

`d826e120dd684da5504f7975c9b1387ea8d38434`.

No `revision/a2-v27...` branch existed when the present review branch was created. The review branch starts directly from the frozen v26 author head and adds files only below

`reviews/a2-v26-external-harsh-top4-rereview-2026-10-03/`.

No author manuscript source, prior report, revision branch, workflow, retained volume or unrelated paper is modified by this review.

The active primary consists of:

- `core/01_setting.tex`;
- `core/02_collision_clouds.tex`;
- `core/03_recognition.tex`;
- `core/04_smooth_certificate.tex`;
- `core/05_sequential.tex`;
- `core/06_comparison.tex`;
- `core/07_compensated_clouds.tex`.

I also inspected the response, source pins, delivery status, current workflow, hosted run and jobs, the v25 report, and the stated literature comparisons.

## 3. Information model and theorem package

The v26 observation has three layers.

1. **Resettable collision acquisition.** The apparatus chooses a position uniformly in a specified square and an independent direction at unit speed. Solid starts are failures. For a free start it records all collision positions and times through a bounded horizon with certified spatial enclosures. Additional bounded-size squares may be placed around contacts and flights already seen.
2. **Collision-generated geometry.** First-hit point clouds, spatial clustering and convex hulls recover complete encountered bodies. Smoothed support functions provide \(C^2\) enclosures. A finite complete-pair support fingerprint recognizes the bridge translation class and coherent transverse sign.
3. **Intrinsic endpoint laws.** For every accepted three-impact return branch, two unconditional endpoint histograms at known absolute times estimate two complete two-dimensional endpoint-arclength subprobability densities. These functions recover the stationary action and the absolute free cell area.

For a clear normal bridge, the local law is

\[
 f_T(s,t)=\frac{-W_{st}(s,t)}{2\pi A}\,(T-W(s,t))_+.
\]

On a strictly active rectangle, two times give

\[
 W=\frac{T_1f_2-T_2f_1}{f_2-f_1},
 \qquad
 A=\frac{(T_2-T_1)(-W_{st})}{2\pi(f_2-f_1)}.
\]

Diagonal derivatives of \(W\) reconstruct the two reflecting arcs. Complete bodies now come from the collision clouds rather than analytic continuation. Reconstructed bodies identify visible types, tree placement gives representatives, and non-tree records give cycle vectors. Their integer span \(\Gamma\) is tested through

\[
 \mathcal D
 =\operatorname{covol}\Gamma-A-\sum_{i\in I}\operatorname{area}(C_i)
 =([\Lambda:\Gamma]-1)\operatorname{covol}\Lambda
   +\sum_{i\notin I}\operatorname{area}(C_i).
\]

The defect vanishes exactly when all types are visible and the cycle subgroup is the full period lattice. The sequential theorem retains every raw proposal, reconstructs its geometry afresh at every epoch, validates all current endpoint laws with fresh samples, and stops only when a component passes the rational and defect tests.

## 4. Collision-cloud reconstruction

### 4.1 First-hit minorization

For a boundary arc \(I\), the proof launches from points a controlled distance along the outward normal and from directions in a fixed cone. In the coordinates \((x,\varphi,r)\mapsto(q,v)\), where \(q=x-rv\), the Jacobian contains \(\cos\varphi\), bounded below on the chosen cone. Positive body separation keeps the launch corridor outside every other obstacle. This gives a lower phase-volume bound proportional to the arclength of \(I\).

Covering a boundary of bounded perimeter by \(O(q^{-1})\) arcs and applying a coupon union bound gives the stated sample size

\[
 n\gtrsim q^{-1}
 \left\{\log(1+q^{-1})+\log(\alpha^{-1})\right\}.
\]

On the simultaneous event, every true boundary point is within arclength \(q\) of a first-hit observation. With collision localization error \(\varepsilon_x<q/10\), the \(d_0\) separation clusters the points by physical body.

This is a coherent controlled-support tomography argument. It does not require a boundary query. It does require resettable spatial injection and collision localization throughout a square large enough to contain the entire encountered body and a free collar.

### 4.2 Convex hull and positive smoothing

If \(P\) is the convex hull of the localized first-hit points, bounded curvature gives

\[
 d_H(P,C)\le \frac{\kappa_+q^2}{2}+\varepsilon_x.
\]

Equivalently the support functions are uniformly close. Convolution by a positive kernel of width \(h\) gives, through two derivatives,

\[
 \|\widetilde p-p\|_{C^2}
 \le B_3h+C e_qh^{-2}.
\]

Taking \(h\asymp\nu\), \(e_q\asymp\nu^3\), and hence \(q\asymp\nu^{3/2}\), gives \(C^2\) error \(O(\nu)\) with the stated \(O(\nu^{-3/2}\log)\) cloud cost. The algebra is correct.

### 4.3 Compensated smoothing

For the stronger \(C^{6,\beta}\) class, the signed kernel

\[
 K_h=\frac43\phi_h-\frac13\phi_{2h}
\]

has mass one and vanishing second moment. A fourth-order Taylor expansion after two differentiations gives

\[
 \|K_h*p-p\|_{C^2}\le B_6h^4,
\]

while the hull error still contributes \(Ce_qh^{-2}\). The choices

\[
 h\asymp\nu^{1/4},\qquad
 e_q\asymp \nu h^2\asymp\nu^{3/2},\qquad
 q\asymp\nu^{3/4}
\]

give \(O(\nu)\) \(C^2\) accuracy and the improved cloud exponent. The use of six derivatives is exactly what the differentiated fourth-order expansion requires. The signed approximation need not itself be a support function; it is used as an accurate numerical descriptor, while the raw hull retains the geometric enclosure.

## 5. Recognition and local certification

### 5.1 Complete-pair fingerprint

The descriptor places the ordered pair in its common normal-contact frame and samples both complete support functions at a finite uniform angular mesh. Unlike the v25 contact-jet descriptor, this is not attempting to identify an arbitrary smooth body from a short germ. It uses whole-body information obtained from the cloud.

The constants are now quantitative. With

\[
 C_0=3+\frac{9(R_++2D_0)}{\eta},\qquad
 \Delta_0=\min\{1,\sigma/36,\eta/36,d_0/(4C_0)\},
\]

the alignment estimate satisfies \(C_0\Delta_0\le d_0/4\). The type and symmetry margins likewise absorb the centering and rotation losses. A mesh of size \(m\ge64K_0/\Delta_0\) turns nodal agreement into uniform agreement. Same-class noisy descriptors lie below the matching threshold, while distinct classes, including the coherent reversal, stay above it. I found no constant-bookkeeping defect in the final formula.

This is a meaningful improvement over the v25 continuation-sized fingerprint. Its size is polynomial in the declared numerical priors and reciprocal margins. The paper correctly does not turn that statement into an end-to-end bit-complexity theorem.

### 5.2 Normal-root certificate

For two arclength charts at a closest pair, the distance Hessian is

\[
 D''=
 \begin{pmatrix}
 g^{-1}+\kappa_0&-g^{-1}\\
 -g^{-1}&g^{-1}+\kappa_1
 \end{pmatrix}.
\]

Its determinant is
\[
 \frac{\kappa_0+\kappa_1}{g}+\kappa_0\kappa_1>0,
\]
and its quadratic form is bounded below by
\(\min(\kappa_0,\kappa_1)\) times the Euclidean norm squared. The explicit Hessian-Lipschitz bound and contraction test therefore isolate a unique nearby normal root from cloud derivative enclosures. Convex supporting half-planes then identify it as the global shortest segment for those two bodies.

### 5.3 Clearance

The middle-segment clearance test uses the union of cloud hulls, a one-Lipschitz distance function, a spatial mesh, and enclosure errors. This is a valid replacement for the previous distance-to-solid oracle, provided the padded cloud region contains every body capable of entering the tested neighborhood.

One sentence should be clarified. The text removes “endpoint collars shorter than \(\min(d_0/8,g/4)\)” and then says that the remaining middle segment is at distance at least \(c_0/2\) from “the solid,” while the collars are handled by facing supports and \(d_0\). If “the solid” in the middle claim includes the two endpoint bodies, an upper bound on the collar length cannot imply a \(c_0/2\) distance from them: along the outward normal of a disk, that distance is exactly the removed collar length. The intended and mathematically natural interpretation is that the \(c_0\) clearance test concerns other bodies, with the two endpoint bodies treated separately by support half-planes. That exclusion should be stated explicitly, or the collar length should be chosen with an additional lower bound compatible with the claimed tube radius. I regard this as a presentation/constant clarification, not a counterexample to the protected-bridge theorem.

## 6. Smooth inverse and completion certificate

The two-time quotient recovers \(W\) and \(A\) with a locally Lipschitz \(C^2\) bound under the displayed denominator, twist, activity and geometry margins. The diagonal Schur-complement formulas recover source and target curvature and the nearest-foot speed. Frenet integration then reconstructs the local arcs.

The global step no longer analytically continues those arcs. It clusters the independently reconstructed complete cloud bodies under the \(C^2\) type gap. A spanning tree places representatives; non-tree edges produce approximate lattice cycle vectors. Bounded vectors and a positive covolume lower bound yield a finite denominator bound for the coordinates relative to an independent pair. Rational separation recovers these coordinates exactly at sufficiently small continuous error, and Hermite reduction gives the subgroup before the area test is used.

The order of operations remains important: the arithmetic subgroup is recovered before the completion identity calibrates anything. The defect is nonnegative and has a uniform positive gap on incomplete components because either the subgroup index is at least two or a missing body has area at least \(a_0\). Omissions and repetitions cannot create a false positive. I found no defect in this retained chain.

## 7. Sequential validation and resource accounting

At every epoch the method rebuilds all geometric decisions from fresh clouds. This prevents one erroneous early statistical name from becoming permanent. Conditional on the proposal history, the current finite list is fixed before the new validation samples. The cloud confidence allowances and endpoint concentration bounds therefore combine by iterated conditioning and summable error spending.

The endpoint cell error includes both laboratory-square bias and coordinate-registration error:

\[
 C\{h\sqrt{r_N}+r_N+\tau_L+\nu h\}.
\]

After division by cell area and two differentiations, the density error is

\[
 C\{h^\beta+\sqrt{r_N}h^{-3}
        +(r_N+\tau_L)h^{-4}+\nu h^{-3}\}.
\]

The choices
\[
 h=r_N^{1/(2\beta+6)},\qquad
 L\gtrsim h^{-(\beta+4)},\qquad
 \nu\lesssim r_N^{1/2}=h^{\beta+3}
\]
balance all displayed terms. No derivative estimate is improperly inferred directly from total variation.

The protected return volume gives every missing witness record a uniform conditional hazard. A finite saturated witness follows from short-clear-bridge connectivity and the proper-divisor reduction of a finite-index cycle subgroup. The coupon tail and the current-epoch validation error give the stated stopping tail. The launch exponents follow from at most \(O(k^3)\) fresh cloud calls at epoch \(k\), multiplied by the cloud cost and summed over epochs. The condition \(a>11/2\) is correctly compatible with the theorem's choice \(a\ge6\).

These are valid resource accounts for the declared launch model. They are not end-to-end complexity bounds. Position-localization bit cost, numerical geometry, analytic or smooth fitting, apparatus travel and setup remain separate. The largest laboratory square grows with the target accuracy. A single passive orbit is not covered.

## 8. Corrections and qualifications required before submission

1. **Clarify endpoint bodies in the clearance statement.** State explicitly that the middle-segment \(c_0/2\) test excludes the two bodies defining the bridge and that their contribution is handled by the facing-support collar argument; otherwise add a collar lower bound consistent with the claimed tube radius.
2. **Keep the complete sensor contract in every headline statement.** “Collision data” here means controlled resettable launch positions, independent directions, bounded-time collision positions and times, certified localization, auxiliary full-body clouds, fresh repeated validation, and two endpoint histograms. It is not generic unmarked orbit data.
3. **Keep smooth-class priors adjacent to the global conclusion.** Shape separation, asymmetry, area/covolume gaps, bounded lattice presentations and the protected clear-bridge network are structural inputs, not consequences of collision sampling.
4. **Do not describe launch exponents as end-to-end complexity.** The manuscript currently gives the necessary caveat; it should remain in the abstract, theorem summary and any submission letter.
5. **Complete exact-source qualification.** The remote branch does not contain `tools/verify_v26.py` or `tools/validate_v26.py`. The successful hosted run archived the source but skipped both tool installation and all-volume qualification. A formal submission should contain the driver and an actual exact-SHA full-package pass.

## 9. Literature and novelty assessment

The closest existing literatures have different data.

- Boundary and lens rigidity recover a metric from boundary distance or lens relations. The Euclidean billiard table here is unknown through reflecting bodies, and its local data are actively prepared collision clouds plus endpoint laws.
- Obstacle travelling-time rigidity uses exterior endpoint/travel-time sets. Version 26 instead uses internal resettable launch positions, collision localization, selected return laws and absolute phase-volume normalization.
- Random convex-body approximation studies convex hulls of random interior or boundary points, often under uniform sampling. The v26 first-hit cloud has a different distribution, but the proof needs only a uniform lower mass on each short boundary arc; its coupon/Hausdorff mechanism belongs naturally to this classical approximation framework.
- The marked-length and count-only billiard problems remain distinct. Version 26 neither reduces its sensor to those invariants nor proves the unresolved exact analytic count-only statement.

The genuinely new package is the integration of a collision-generated whole-body enclosure, a quantitative complete-pair classifier, the intrinsic density/action inverse, arithmetic period recovery, the nonnegative completion defect and anytime revalidation. That integration is substantial. The individual mechanisms are mostly recognizable, and the final theorem remains tied to a highly controlled experiment and a strongly separated compact class. This is why my correctness assessment is positive while my four-journal significance assessment is negative.

## 10. Reproducibility and evidence

The author records a local source-content execution with:

- 7,453 finite assertions;
- identical ordinary and optimized Python output;
- an 18-page primary build;
- no final TeX diagnostics.

The delivery note correctly says that this local execution was not an authenticated Git checkout and did not rebuild the retained volumes.

The exact-head GitHub Actions run `37118534591` completed with conclusion `success`, but its semantics must not be overstated. It checked out the exact triggering commit and archived the native source. Because `tools/validate_v26.py` is absent, both “Install build tools when qualification driver is present” and “Qualify exact source and all declared volumes” were skipped. The workflow then wrote a source-archive-only status with `full_package_qualified: false` and uploaded it. Thus there is a successful source-archiving run, not a successful v26 full-package qualification.

My independent `verify_review.py` imports no author code. In ordinary and optimized Python it produced identical output and completed 199,456 checks of finite algebra, including:

- the normal-distance Hessian and curvature lower bound;
- first-hit coupon and square-preparation inequalities;
- positive and compensated smoothing balances;
- fingerprint alignment constants and registry bands;
- translation invariance of relative contacts;
- rational cycle coordinates, common denominators, Hermite indices and covolumes;
- completion-defect identities and positive gaps;
- histogram exponents, hazard bounds and epoch resource sums.

The script also records the endpoint-collar interpretation issue. These checks are not a proof certificate, a physical apparatus execution, a uniform class verification, a TeX build, or a priority search.

## 11. Final verdict

Version 26 successfully addresses the central v25 access objection. It replaces deterministic boundary and distance queries by counted collision launches, replaces short-arc analytic continuation by direct whole-body clouds, replaces analytic regularity by a fixed \(C^{6,\beta}\) class, and supplies a quantitative finite fingerprint. No fatal counterexample was found in the new core.

The result remains a conditional rigidity and certification theorem for a strong active collision-tomography experiment on a strongly separated compact class. It does not derive whole-table rigidity from a standard passive or spectral billiard invariant, and its conceptual ingredients, while skillfully assembled, do not in my judgment cross the exceptional threshold of *Annals*, *Acta*, *Inventiones* or *JAMS*.

**Recommendation: reject at the requested top-four benchmark.** A focused specialist-journal submission could be strong after a fresh human proof review, the clearance clarification and an exact-source full-package qualification.
