# External top-four referee report on A2 v35

**Manuscript:** Qian Qi, *Scalar collision laws and recognition of periodic dispersing billiards*  
**Reviewed revision:** `revision/a2-v35-self-calibrated-stationary-2026-10-04`  
**Equivalent referee-copy alias:** `revision/a2-v35-self-calibrated-referee-copy-2026-10-04`  
**Reviewed commit:** `70c055e1ff090d58ecd61a5644e0fa62a7766f13`  
**Reviewed repository tree:** `052f994e14452cc42a39ab23c8dae33a468c6495`  
**Controlling preceding report:** `e8ad32bfd0a8641c239c67e9776ba08d3aaab72a`  
**Manuscript directory:** `papers/A2-v35-self-calibrated-stationary`  
**Date:** 4 October 2026  
**Requested benchmark:** *Annals of Mathematics* / *Acta Mathematica* / *Inventiones Mathematicae* / *Journal of the AMS*  
**Status:** author-requested, AI-assisted referee-style assessment; not a journal decision, proof certificate, apparatus validation, or exhaustive priority determination.

## 1. Recommendation

**Recommendation at the requested four-journal benchmark: reject.**

Version 35 is a genuine mathematical advance over the reviewed v34 article. It responds directly to the two most concrete unresolved restrictions in the previous report.

First, the one-scale stationary theorem required the complete support function of the launch footprint as calibrated input. Version 35 replaces this by a two-scale experiment. The same unknown stationary launch mechanism is operated at two known positive homothetic scales, with a known common dilation origin but an unknown convex footprint and unknown density. The two recovered positive-component collections are paired by strict geometric nesting. Two support-function equations then recover both the original obstacle and the unknown footprint.

Second, v34 had no information lower bound specific to a common stationary launch law. Version 35 fixes one known uniform-disk law, uses that same law for every competing table and command, and proves an expected-attempt lower bound by combining a uniform contraction of every collision mean with a conditional binary-channel information inequality. This is not a reformulation of the earlier adversarial calibration nonidentifiability argument.

The revision also makes the two requested local proof repairs: it puts every erosion below an explicit uniform rolling-radius threshold, and it correctly identifies the sixth-order approximation device as a signed numerical kernel rather than a probability density.

On the new v35 core audited in detail, I found no fatal counterexample. The positivity-set identification, cross-scale component matching, two-scale support inversion, finite error propagation, stationary mean-contraction lemma, binary range inequality, stopped mutual-information bound, physical packing and exponent calculation are coherent under their stated hypotheses. Independent finite diagnostics accompanying this report support the displayed algebra and inequalities.

The remaining objection is conceptual and editorial. “Self-calibration” here is relative to a strong calibrated two-scale apparatus: the controller knows the two exact homothetic factors, their common laboratory dilation origin, uniform footprint inball/envelope/curvature/smoothness bounds, the density boundary-mass constants, the compass geometry, a fixed protective aperture, the bounded periodic prior and the positive nonperiod-patch margin needed for uniform finite period decisions. Nominal command positions are refined to a scale that tends to zero with the target accuracy. Manufacture, metrology, scale calibration, apparatus motion and arithmetic bit complexity are not included in the attempted-bit count.

Moreover, the stationary upper and lower powers do not match. For a density bounded below on a fixed footprint, the displayed bracket is

\[
 c\nu^{-(s+1)/(s-2)}
 \le N^*_{\rm stat}(\nu)
 \le C\nu^{-(3s+1)/(s-2)}\log^2(C/\nu),
 \qquad s=6+\beta.
\]

The exponent gap is `2s/(s-2)`. The lower bound proves a genuine polynomial cost of a fixed common spread, but it does not show that the much larger upper power is intrinsic. Consequently the central finite statistical result remains a sufficient construction rather than a sharp minimax theorem.

In my judgment v35 is a serious and potentially strong specialist-journal paper. It is materially stronger than v34 and closes the previous report's most concrete mathematical requests. It does not, however, attain the exceptional naturality, breadth or conceptual transformation expected at the four journals named above. I would not recommend another open-ended revision cycle at that benchmark.

## 2. Frozen source and chronology

The final stationary revision and its referee-copy alias both resolve to

`70c055e1ff090d58ecd61a5644e0fa62a7766f13`

with repository tree

`052f994e14452cc42a39ab23c8dae33a468c6495`.

The final commit changes only `core/09_stationary_jitter.tex`, adding the rolling-radius and signed-kernel clarifications requested by the v34 report. Its parent is `53ba5552efea5df04c4e33e30b7d67c815cf3fbf`, which changes the v35 workflow but not the mathematical source.

The branch

`revision/a2-v35-self-calibrated-footprint-2026-10-04`

is a divergent sibling based directly on the v34 review head. It resolves to the earlier commit `7125ed358a6c3da9fef0cd0011cca0710ad0aab4` and does not contain the final stationary package reviewed here. The stationary revision is therefore the controlling latest A2 object.

The controlling preceding report is the v34 review at

`e8ad32bfd0a8641c239c67e9776ba08d3aaab72a`,

which reviewed author commit

`ed3876b8a82e2c46bc1533457978c15fea1a2114`.

No A2 revision branch later than v35 existed when the present review was frozen. The review branch starts directly from the final v35 author head and adds files only under

`reviews/a2-v35-external-harsh-top4-rereview-2026-10-04/`.

No manuscript source, author revision branch, previous report, workflow, archive or unrelated paper is modified.

The active article consists of `main.tex`, `references.tex`, and fifteen core inputs. The genuinely new mathematical inputs relative to v34 are principally

- `core/00d_self_calibration_overview.tex`;
- `core/10_unknown_footprint.tex`;
- `core/11_stationary_information.tex`;

with the two local proof clarifications in `core/09_stationary_jitter.tex`. I also inspected the response, proof/history/literature ledgers, README, submission map, v34 report, workflow definition, hosted run and repository tree.

## 3. Information model and theorem package

One attempted command returns one bit. For nominal center `x`, displacement `a` and stationary launch error `Z`, the forward command starts at `x+Z` and the reciprocal reverse command starts at `x+Z+a` with displacement `-a`. Solid starts and free misses both return zero and remain in the denominator. Only pooled collision means are used.

For one fixed launch scale the reciprocal identity recovers the forcing

\[
 g=(T-I)v,
 \qquad
 v(x)=\int j(z)\mathbf1_{\mathcal O}(x+z)\,dz.
\]

The positive components of `v` are the interiors of

\[
 P_C=C+(-K).
\]

The killed-walk inverse reconstructs `v`; active boundary search reconstructs the expanded bodies; subtracting the known support of `-K` gives the original obstacles. This is the retained v34 result.

Version 35 instead uses two known scales `0<lambda_1<lambda_2` of one unknown footprint `K`, with one stationary density `j` on the unscaled footprint. At scale `lambda_i` the positive components are

\[
 P_{i,C}=C+(-\lambda_iK).
\]

The new exact inverse and finite theorem recover both `K` and the table. The article then gives a separate stationary-noise lower bound under one fixed known uniform-disk law and arbitrary adaptive short commands.

The result remains an active input-output theorem. The exact data are controlled mean functionals; the finite data are adaptively selected Bernoulli responses. It is not a passive count, marked-length or spectral invariant.

## 4. Audit of the two-scale footprint inverse

### 4.1 Positivity sets at each scale

The density is positive almost everywhere in the footprint interior, with the quantitative lower bound

\[
 j(z)\ge b_0\operatorname{dist}(z,\partial K)^\gamma.
\]

Consequently a blurred occupation is positive exactly when a translated footprint and an obstacle have positive-area intersection. This identifies its positive components as the interiors of `C+(-lambda_i K)`. The strict separation condition

\[
 t+2\lambda_2R_K<d_0
\]

keeps different expanded bodies more than one compass step apart, so the retained stopped inverse applies at both scales.

The scaling of the density lower bound is correct:

\[
 j_i(z)=\lambda_i^{-2}j(z/\lambda_i)
 \ge b_0\lambda_i^{-(\gamma+2)}
       \operatorname{dist}(z,\partial(\lambda_iK))^\gamma.
\]

Thus the finite query constants can be chosen uniformly from the stated priors without evaluating the unknown density.

### 4.2 Cross-scale matching

Convexity gives

\[
 \lambda_2K=\lambda_1K+(\lambda_2-\lambda_1)K.
\]

Since `K` contains `r_K` times the unit disk,

\[
 P_{1,C}+(\lambda_2-\lambda_1)r_K\overline B
 \subset P_{2,C}.
\]

This is a strict, shape-independent nesting margin. It pairs every small-scale expanded body with a unique large-scale expanded body without labels, asymmetry or pairwise noncongruence. At finite error the Steiner point of the small estimate remains inside exactly the corresponding large estimate once the Hausdorff error is below fixed fractions of the nesting and intercomponent margins.

I found this matching argument sound. It is stronger and cleaner than matching by approximate congruence.

### 4.3 Linear support separation

For a matched pair,

\[
 p_{P_{i,C}}^{\rm lab}
 =p_C^{\rm lab}+\lambda_i p_{-K}^{\rm lab}.
\]

The two equations give

\[
 p_{-K}^{\rm lab}
 =\frac{p_{P_{2,C}}^{\rm lab}-p_{P_{1,C}}^{\rm lab}}
        {\lambda_2-\lambda_1},
\]

\[
 p_C^{\rm lab}
 =\frac{\lambda_2p_{P_{1,C}}^{\rm lab}
       -\lambda_1p_{P_{2,C}}^{\rm lab}}
        {\lambda_2-\lambda_1}.
\]

These formulas are exact. Their condition number is controlled by the fixed positive scale gap. They recover the laboratory position of a noncentered footprint because the common dilation origin is supplied; no hidden mean-zero convention is used.

For finite reconstructions, the manuscript averages the separate footprint estimates to enforce one common output footprint. Averaging does not improve the worst-case rate, but it cannot enlarge the maximum error. The positive curvature-radius margins ensure that the recovered support differences are genuine strictly convex bodies for sufficiently small error, rather than formal differences of noisy sets.

### 4.4 Error propagation and period recognition

At each scale the fixed-jitter query reconstructs the expanded supports with supremum error `O(h^s)` and `C^2` error `O(h^{s-2})`. Applying the fixed two-by-two linear inverse preserves these orders, up to a scale-gap constant. The protected-patch period tests are then applied to the recovered original obstacles, not to the blurred bodies.

This distinction matters: the footprint need not have the table's period structure. The manuscript handles it correctly. Under the known positive patch margin and bounded-denominator priors, the primitive orbit count and exact rational relations lock, while Euclidean period coordinates remain estimates.

## 5. Audit of the stationary information lower bound

### 5.1 Uniform contraction of every command mean

For matched convex bodies at Hausdorff distance `epsilon`, both the solids and their segment sweeps have symmetric-difference area `O(epsilon)` by parallel-body estimates. A compact launch density bounded by `J` therefore changes any short-command success probability by at most `C J epsilon`, uniformly in the nominal center and direction.

The physical packing has pairwise `C^2` separation of order `h^{s-2}` but total Hausdorff diameter only `O(h^s)`. Hence every permitted Bernoulli response probability varies across the entire packing by at most

\[
 d_h=O(h^s).
\]

This estimate remains true after any adaptive history because conditioning only restricts the set of possible parameters.

### 5.2 Information in one contracted Bernoulli response

If all conditional success probabilities lie in `[a,b]`, the manuscript proves

\[
 I(V;Y)\le b-a
\]

in bits. The proof couples `Y` to an independent uniform threshold. Outside an interval of length `b-a`, the output is parameter-independent; inside, its entropy is at most one bit. This avoids any artificial division by `a(1-a)` and remains valid when probabilities approach zero or one.

The inequality is elementary and correct.

### 5.3 Adaptive stopping

At every active history the possible response means have range at most `d_h`. Padding the transcript after stopping and applying the conditional chain rule gives

\[
 I(V;Z,U_0)\le d_h\,\mathbb E\mathsf T.
\]

Fano's inequality for the disjoint accuracy sets yields

\[
 d_h\frac1M\sum_v\mathbb E_v\mathsf T
 \ge (1-\delta)\log_2M-h_2(\delta).
\]

Continuous command coordinates, batch sizes and the stopping time do not form an extra table-dependent channel: conditional on the independent controller seed they are functions of the preceding binary transcript. The proof correctly treats expected stopping time rather than silently replacing it by a deterministic cap.

### 5.4 Packing and exponent

The support-bump family has

\[
 \log_2 M\asymp h^{-1},
 \qquad
 \text{C}^2\text{ separation}\asymp h^{s-2},
 \qquad
 d_h\asymp h^s.
\]

Taking `h` proportional to `nu^{1/(s-2)}` gives

\[
 \mathbb E\mathsf T
 \gtrsim h^{-(s+1)}
 =\nu^{-(s+1)/(s-2)}.
\]

The same known uniform-disk law is used for every table. The result even allows the controller to know the lattice, species and laboratory frame and to select short directions, arbitrary-precision centers and a scale in a fixed interval bounded away from zero. This is a genuine common-noise lower bound.

It is not a matching lower bound for the stated upper construction. The paper says so explicitly.

## 6. The two inherited proof clarifications

### 6.1 Rolling radii

The final source chooses uniform rolling radii for `C`, `K` and their Minkowski sum, and places `e_0` below all of them and below the fixed collar depth. The subsequent erosion identities are therefore invoked in their valid range. This closes the v34 presentation objection.

### 6.2 Signed approximation kernel

The coefficients

\[
 \frac85,-\frac45,\frac8{35},-\frac1{35}
\]

on dilation scales `1,2,3,4` have total mass one and cancel the second, fourth and sixth moments of an even base kernel. Odd moments vanish by evenness. The resulting device is necessarily signed, and the final source now says so. This closes the second requested clarification.

## 7. Qualifications required in any resubmission

### 7.1 Qualify “self-calibration” at every headline occurrence

The theorem removes an entire footprint support-function oracle. It does not infer the scale factors, common dilation origin, exact homothety, density lower-bound constants, footprint regularity class, compass geometry or nominal coordinate system from collision bits. A more precise phrase would be “two-scale blind footprint recovery under calibrated homothety.”

### 7.2 Keep control precision separate from observed bits

The attempted-bit bound does not price the binary description or physical production of nominal centers at scale `O(nu^{s/(s-2)})`, exact homothetic scaling, apparatus travel, or metrology. These are legitimate separate resources, but the distinction must remain adjacent to every complexity statement.

### 7.3 Do not present the stationary exponent as sharp

For `gamma=0`, the upper power is `(3s+1)/(s-2)` and the lower power is `(s+1)/(s-2)`. The gap is large. The result establishes a stationary-noise information penalty and a constructive upper bound, not a stationary minimax rate.

### 7.4 Preserve the precise lower-bound scope

The stationary converse concerns a fixed nondegenerate physical subclass, a deterministic laboratory-frame gauge, bounded short commands, one known bounded density and a worst-case expected-attempt criterion. It does not cover unbounded command lengths, observed launch positions, analog outputs, scales tending to zero, or every restricted subclass.

### 7.5 Period recognition remains prior-relative

Uniform finite decisions require the bounded periodic presentation and known positive nonperiod-patch margin. Without that margin the paper retains only pointwise eventual decisions. The theorem does not infer crystallinity from an arbitrary configuration.

## 8. Source and qualification defect at the reviewed head

The final exact-head workflow run is

`37177203228`

for SHA

`70c055e1ff090d58ecd61a5644e0fa62a7766f13`.

It completed with conclusion **failure**. Checkout and dependency installation succeeded; the `Build primary manuscript` step failed, and the source-binding step was skipped. The run uploaded no artifact.

The reviewed workflow no longer executes the validation commands claimed in the README. It installs TeX, builds the primary, greps the log and checks the checkout SHA. The reviewed paper tree contains neither the referenced `tools/validate_v35.py` route nor a current verification receipt or source-pin manifest. Thus the README's claimed local counts and build result are not independently reproducible from this branch as delivered.

This is a real submission-readiness defect. It is not evidence that the new theorems are false, and it is not the mathematical basis for the top-four rejection. A resubmission should restore a fail-closed source manifest, include the current diagnostics actually cited by the README, retain logs and artifacts on failure, and obtain a successful exact-head build.

## 9. Top-four significance assessment

The revision's strongest contribution is the combination of three layers:

1. reciprocal collision means reconstruct a blurred occupation;
2. two homothetic positivity supports separate an unknown convex footprint from the obstacles;
3. a common-noise contraction and stopped binary-information argument gives a stationary expected-cost lower bound.

This is a meaningful synthesis in the stated collision experiment. The abstract mechanisms are nevertheless classical in character: Minkowski support addition, strict nesting, a two-by-two linear inverse, rolling-body overlap, killed random-walk potentials, active line search, smooth interpolation and binary entropy bounds.

The observation remains highly engineered. Exact homothetic scaling and a common laboratory origin substitute for the removed footprint-function oracle. Strong physical priors and a known period margin drive the global conclusion. The result does not produce rigidity from a standard dynamical invariant, and the central stationary statistical rate remains unresolved by a wide polynomial gap.

For these reasons I do not regard the manuscript as reaching the conceptual threshold of *Annals*, *Acta*, *Inventiones* or *JAMS*. The work can nonetheless form a strong specialist paper if presented as a conditional active inverse problem rather than as a natural rigidity theorem.

## 10. What would materially strengthen a future submission

1. **Close or substantially narrow the stationary exponent gap.** A matching lower bound for the boundary-mass regime, or a new upper construction approaching `(s+1)/(s-2)`, would change the editorial balance.
2. **Reduce the homothety oracle.** Identifying an unknown scale ratio or common dilation origin from the bits, or proving a sharp one-scale nonidentifiability theorem, would clarify the intrinsic information threshold.
3. **Price additional control resources.** A joint sample/input-precision or metrology complexity theorem would make the finite information statement more natural.
4. **Separate the principal paper from the programme archive.** The best focused paper is the stationary support inverse, two-scale footprint separation and common-noise lower bound. Earlier experiments can remain available without carrying equal narrative weight.
5. **Repair exact-source delivery.** The current failed build and missing validation route should be closed before any submission.

## 11. Independent diagnostics and limits

The accompanying `verify_review.py` imports no author code and uses only the Python standard library. Ordinary and optimized execution produced byte-identical output. It performs 555,419 checks covering:

- exact two-scale footprint/body identities and perturbation bounds;
- disk-model nesting and radius recovery;
- scaled density exponents;
- signed-kernel mass and moment cancellation;
- circular lens `d^{3/2}` scaling and weighted cap powers;
- 548,090 finite Bernoulli information-range comparisons;
- stopped information-budget algebra;
- exact killed-chain mean exits and Green perturbation bounds;
- stationary upper/lower exponent identities;
- parallel-area symmetric-difference controls.

These checks do not certify the continuum compactness arguments, physical apparatus, adaptive measurability in all generality, TeX build, literature priority or the retained multi-volume programme. I did not perform an exhaustive literature search or re-prove every inherited theorem.

## 12. Final verdict

**Response to the v34 report:** substantively successful. The footprint-function oracle is removed under calibrated two-scale homothety; a genuine common-stationary-noise expected-attempt lower bound is proved; and both requested proof clarifications are supplied.

**Mathematical audit:** no fatal counterexample found in the new v35 core. The two-scale inverse and stationary lower-bound chains are coherent under the stated assumptions.

**Source qualification:** unresolved and currently failed at the exact reviewed head; the advertised validation route is absent from the delivered tree.

**Editorial assessment:** strong conditional active-inverse mathematics, but too engineered, prior-dependent and statistically nonsharp for the requested four-journal benchmark.

**Recommendation: reject at the requested top-four benchmark.**