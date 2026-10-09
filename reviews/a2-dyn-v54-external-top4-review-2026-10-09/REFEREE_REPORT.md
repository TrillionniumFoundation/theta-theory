# External top-four referee report on A2-DYN revision 54

**Manuscript:** Qian Qi, *Collision records, arithmetic, and raw local inversion in a triangular Lorentz gas*  
**Reviewed author branches:** `revision/a2-dyn-v54-referee-response-2026-10-09`, `revision/a2-dyn-v54-referee-copy-2026-10-09`  
**Reviewed commit:** `63135318e1eadd80341d4d0656a17e8caba60c90`  
**Reviewed repository tree:** `d010dac69e240629a877b9d086a4620b1578cb2c`  
**Ordinary source payload tree:** `6334f8f2e31b35c1f907db28039cd9df0524a63d`  
**Active manuscript directory:** `papers/A2-DYN-v54-referee-response`  
**Active mathematical source:** one hundred sixteen numbered core modules  
**New mathematics since the latest external report:** revision 53 modules 112--114 together with its explicit repairs to modules 110--111, and revision 54 modules 115--116  
**Immediate qualified author baseline:** revision 53, commit `9d3891615c3e09d8e40b7ba8e24d410ee6e9c76d`  
**Frozen revision-53 paper tree:** `95d7b6f3239a487cf83f2690fb8acf84e14f1f86`  
**Controlling external report:** `reviews/a2-dyn-v52-external-top4-review-2026-10-09/REFEREE_REPORT.md`  
**Controlling report commit / blob:** `b487df93e48dbf455b3ed04680c1f7ae3613f45e` / `9f50c9909cc137d67babfd69f6508de2ce3254cf`  
**Date:** 9 October 2026  
**Requested benchmark:** *Annals of Mathematics* / *Acta Mathematica* / *Inventiones Mathematicae* / *Journal of the AMS*  
**Status:** author-requested, AI-assisted referee-style assessment; not a commissioned journal report, an editorial decision, a formal proof certificate, or an independent human billiards/anisotropic-spaces audit.

## 1. Recommendation

**Recommendation at the requested four-journal benchmark: reject in the present form.**

This recommendation should not obscure the substantial progress made after revision 52.

The latest external report had already recognized a common positive path-valued remainder and same-roof bounded-Lipschitz bridge convergence in conditional mean. It nevertheless left two distinct issues open:

1. the scalar positive incidence and clearance remainders had no central-scale essential-height estimate, so the two-sided pointwise raw-density theorem was still missing;
2. several stronger path and likelihood consequences had not yet been proved.

Revision 53 addresses the second category in a serious way. It isolates a reusable signed-measure compactness and positive-remainder transfer principle, retains the factorial dependence in the spectral Cauchy estimates, proves all even pinned increment moments with factorial constants, obtains an exponential moment for the entire pinned collision and actual-return paths under the unchanged exact microscopic event, and upgrades the same-roof bridge from bounded-Lipschitz convergence in mean to every fixed finite Wasserstein order in mean. Conditional covariance kernels and path-maximum moments follow.

Revision 54 returns to the scalar density. It proves a simultaneous finite-count polynomial height bound for the protected source, combines this with the all-margin positive-source mass estimate and the previously established complete exponential height cap, obtains a uniform nontrivial local `L^(1+s)` range for the complete unprotected exact-label density, upgrades both positive physical remainders and the complete scalar/path-valued local law to local roof `L^q`, and proves forward finite-order likelihood, forward relative entropy, and small-order Renyi convergence under an explicit pointwise arithmetic reference floor.

I audited the following new or materially repaired modules:

- `core/110_path_valued_raw_inversion.tex` and `core/111_same_roof_conditional_bridges.tex`, insofar as revision 53 replaced precise notation, Fourier-normalization, domination, compactness, and measurability passages from the revision reviewed at v52;
- `core/112_signed_path_transfer.tex`;
- `core/113_exponential_pinned_moments.tex`;
- `core/114_same_roof_transport.tex`;
- `core/115_uniform_density_integrability.tex`;
- `core/116_strong_raw_likelihood.tex`.

I found no decisive counterexample, source-normalization error, Fourier-sign error, false arithmetic cancellation, collision/return endpoint mismatch, invalid substitution of a collision-count-dependent frequency band into a fixed-band estimate, or illicit inference from finite `L^q` control to essential-supremum control in these additions.

The strongest new scalar conclusions appear internally coherent, subject to the inherited continuum inputs. In particular:

- the superlevel exponent is correctly computed as
  \[
  \frac{1/16}{9}=\frac1{144};
  \]
- the finite-count error is not integrated to infinity, but only to the inherited exponential height cap;
- the resulting exponent interval
  \[
  1<q<q_*=1+\frac12\min\left\{\frac1{144},\frac\kappa\Gamma\right\}
  \]
  is strictly nonempty;
- interpolation from local `L^1` convergence and a uniform `L^{q_*}` moment is used with the correct powers;
- the forward likelihood theorem retains the pointwise reference floor `G >= d`, rather than replacing it by positive integrated mass;
- forward relative entropy is derived from finite `L^q` likelihood without assuming an essential likelihood bound;
- all exact return, collision, displacement, and roof variables remain unchanged;
- the arithmetic transition kernel is retained uniformly and its fixed-radius residue is never silently set equal to one.

The negative recommendation is nevertheless forced by the principal endpoint which continues to govern the title and the raw-inversion architecture. Revision 54 still does **not** prove

\[
 \sup_{R,n,k}\operatorname*{ess\,sup}_{u\,\text{central}}
 \left|m^2p_{n,R}(k,m,u)
       -\mathcal L_{m,R}(k_1,k_2,u,n)\right|\longrightarrow0.
\]

The positive incidence and clearance remainders may still form arbitrarily narrow upward spikes. The new higher-integrability theorem controls a nonempty finite `L^q` range, and the entropy theorem controls averaged likelihoods, but neither excludes such spikes. The manuscript itself correctly records that the remaining two-sided pointwise law is equivalent to vanishing of the two positive physical essential heights in the ordered limit.

Thus the central situation is now unusually sharp:

- downward microscopic holes below the arithmetic profile have been excluded;
- the full density converges in every local `L^q`, `1 < q < q_*`;
- forward and reverse relative entropies converge on positive-reference windows;
- whole-path conditional laws converge in every finite Wasserstein order in roof mean;
- but positive physical density spikes remain unbounded in essential supremum.

At the requested benchmark, a 357-page article entitled and organized around raw local inversion should either close this final positive-height obstruction or extract a substantially broader theorem whose significance is independent of the unfinished endpoint. Revision 54 does neither yet.

## 2. Frozen source and chronology

Both reviewed author branches resolve to

`63135318e1eadd80341d4d0656a17e8caba60c90`.

The repository tree is

`d010dac69e240629a877b9d086a4620b1578cb2c`.

The active article is

`papers/A2-DYN-v54-referee-response`.

The ordinary source payload tree is

`6334f8f2e31b35c1f907db28039cd9df0524a63d`.

Revision 54 continues the qualified revision-53 author source at

`9d3891615c3e09d8e40b7ba8e24d410ee6e9c76d`.

The intervening lineage commit correctly states that it is only a source freeze and not a completed manuscript. The final reviewed commit adds the complete revision-54 manuscript and qualification workflow. The controlling substantive report remains the revision-52 external report because no separate revision-53 external report was landed before this revision.

This chronology matters. The present review therefore covers all theorem-bearing changes after revision 52, rather than reviewing modules 115--116 in isolation and silently treating revision 53 as independently certified.

The source manifest records:

- all one hundred fourteen revision-53 core modules retained byte-for-byte in revision 54;
- all one hundred forty-seven inherited Python files retained byte-for-byte;
- all inherited mathematical labels, bibliography, compiled appendices, and prior source records retained;
- two new core modules, 115 and 116;
- `full_raw_return_LLT_proved: false`;
- `pointwise_roof_density_LLT_proved: false`;
- `grazing_boundary_pointwise_smallness_proved: false`;
- `clearance_boundary_pointwise_smallness_proved: false`;
- `forward_essential_likelihood_convergence_proved: false`;
- `pointwise_roof_conditioned_bridge_proved: false`;
- `arithmetic_factor_identically_one_proved: false`;
- and `independent_human_review: false`.

The revision-54 exact-source qualification workflows completed successfully on both author refs:

- response branch run `37888494169`;
- referee-copy branch run `37888502141`.

These runs establish source identity, byte preservation, native compilation, finite diagnostic consistency, and label-based rendering at the exact reviewed SHA. They do not certify the continuum billiard geometry, the anisotropic-space estimates, the all-order spectral arguments, or the positive-height endpoint.

The present review branch begins directly from the reviewed author SHA and adds only this report under

`reviews/a2-dyn-v54-external-top4-review-2026-10-09/`.

No author manuscript source, prior review, workflow, historical manuscript, or unrelated repository path is intentionally modified.

## 3. Scope of this review

I did not attempt to re-prove all one hundred sixteen core modules. The substantive audit concerns the mathematical changes which can alter the revision-52 recommendation:

1. the exact repairs to modules 110--111;
2. signed-measure compactness on continuous path space;
3. the abstract common-positive-remainder path inversion principle;
4. the all-order moving-peak Cauchy bounds;
5. factorial pinned increment moments;
6. the dyadic exponential maximum estimate;
7. transfer to the actual return clock;
8. exponentially weighted physical-defect mass;
9. polynomial-growth path test convergence;
10. finite-order Wasserstein same-roof transport;
11. conditional covariance and path-maximum moments;
12. the fixed-band finite-count positive interval bound for arbitrary roof lengths;
13. the simultaneous all-margin positive-source mass bound;
14. the finite-count protected density-height estimate;
15. the high-density tail principle with an exponential cap;
16. the nonempty higher-integrability range;
17. local `L^q` control of both positive physical remainders;
18. scalar and path-valued local `L^q` limits;
19. forward likelihood, relative entropy, and Renyi convergence;
20. the exact relationship of these results to the still-open essential-height criterion;
21. source identity and qualification evidence.

The inherited revision-52 and earlier continuum chain is treated as a source-pinned baseline, not as independently certified mathematics.

## 4. The revision-53 repairs to modules 110--111

Revision 53 made a small number of explicit replacements in two modules which had been reviewed at revision 52. These are not cosmetic in the sense of source control, but they are mathematically clarifying rather than theorem-changing.

The repaired path-inversion text now:

- states the Fourier convention for the positive two-sinc-square dominator;
- includes the inverse factor `(2 pi)^(-1)`;
- records the compact support and integrability of its Fourier transform;
- distinguishes multiplication by a fixed-band constant from rescaling the Fourier support;
- explicitly records `|sigma_m| <= tau_m` before invoking signed compactness;
- invokes the new signed-measure compactness lemma rather than an informal weak-subsequence statement;
- requires roof-dependent selectors to be jointly Borel;
- states that discrete-prefix constancy is only chartwise and does not cross a physical or section boundary.

The repaired same-roof module distinguishes the deterministic return-clock matrix from the occupation variable and explicitly enlarges the central target bound across a roof interval by `h/sqrt(m)`.

These changes address genuine ambiguity in the old exposition. I found them correct and recommend retaining the exact edit ledger in the permanent source record.

## 5. Tight signed measures on continuous path space

The signed compactness lemma uses four inputs:

- uniformly bounded total variations;
- uniform tightness of the variation measures;
- convergence of total masses;
- convergence of rational-time characteristic cylinders.

For finite signed measures on `C([0,1],R^d)`, this is a legitimate convergence-determining package. Uniform tightness gives subsequential weak compactness of the positive and negative parts, or equivalently of the positive measures `tau_j +/- sigma_j` under the explicit domination `|sigma_j| <= tau_j`. Rational evaluation maps generate the Borel sigma field on continuous path space, and finite-dimensional Fourier uniqueness identifies every subsequential signed limit.

The final passage from weak convergence to bounded-Lipschitz dual convergence uses a compact path set carrying all but a small amount of every variation and a finite equicontinuous net on that compact set. This is the correct topology. The lemma does **not** imply path-space total-variation convergence and does not claim it.

I found no defect in this measure-theoretic step.

## 6. The common-positive-remainder path principle

The abstract transfer theorem separates four hypotheses:

1. fixed-band scalar and cylinder inversion;
2. variation compactness;
3. controlled-source correction;
4. positive local mass of one remainder common to all tests.

This separation is useful. In particular, the positive remainder is a source-derived path measure chosen once; it is not selected independently for each bounded-Lipschitz functional.

The exact identity

\[
 \mathbf P(F)-G\mathsf W(F)-\mathbf R(F)
 =\mathbf A(F)-K_B*\mathbf A(F)
  +K_B*\mathbf P(F)-G\mathsf W(F)-K_B*\mathbf R(F)
\]

is the correct measure-valued analogue of the scalar positive-remainder identity. The fixed-kernel local convolution bound controls the last term after the collision limsup. A countable norming class supplies common roof versions.

For the conditional mean statement, the constant test belongs to the bounded-Lipschitz unit ball, so the scalar mass error is already included in the path-measure norm. The inequality

\[
 P(u)d_{\rm BL}(Q_u,\mathsf W)
 \le 2\|\mathbf P(u)-G(u)\mathsf W\|_{\mathrm{BL}^*}
\]

is valid. The pointwise conditional implication correctly retains the additional scalar positive-height hypothesis and does not derive it from local mass.

The abstract theorem is mathematically sound in its stated scope. Its application remains contingent on the inherited path endpoint and variation-dominator estimates.

## 7. All-order spectral derivatives

The factorial derivative lemma correctly extracts the dependence on the differentiation order from one complex circle of radius proportional to `L^(-1/2)`. Cauchy's formula gives

\[
 q!D^qL^{q/2}
\]

times the Gaussian peak or complementary spectral decay. The circle and analytic neighborhood are chosen independently of `q`; this independence is essential and is stated explicitly.

On the nonresonant complement a fixed complex disk yields factorial derivatives with exponential block decay. The argument does not assert any useful dependence on a growing outer roof band.

The principal specialist obligation is to verify that the same local complex charts, projection bounds, and complementary contours really remain uniform over every relevant radius and moving peak. Conditional on the inherited analytic splitting, the Cauchy deduction is correct.

## 8. Factorial pinned increment moments

The three-block derivative represents the exact pinned increment

\[
 \mathsf S_{a+l}-\mathsf S_a-\frac lm\mathsf S_m.
\]

The three centering factors cancel because

\[
 -\frac lm(a+b)+\left(1-\frac lm\right)l=0,
 \qquad a+l+b=m.
\]

Leibniz's multinomial coefficient cancels the three derivative factorials, leaving a global `(2r)!`. The remaining size is controlled by

\[
 \frac lm(\sqrt a+\sqrt b)+\left(1-\frac lm\right)\sqrt l
 \le C\sqrt l.
\]

At least one block has length at least `m/3`, supplying either the four-dimensional Gaussian integral of order `m^(-2)` or an exponentially small complementary factor. This gives

\[
 \int_E\left|\mathsf S_{a+l}-\mathsf S_a-\frac lm\mathsf S_m\right|^{2r}
 d\nu_R^*
 \le (2r)!C_J^{2r}l^r m^{-2}.
\]

The proof uses one fixed positive roof majorant and one fixed spectral band, independent of `r` and `m`. I found the exponent and factorial bookkeeping consistent.

## 9. Exponential moments of the complete pinned path

After normalization by the path scale and by the finite measure

\[
 \lambda=(m^2/h)\mathbf1_E\nu_R^*,
\]

the increment estimate becomes

\[
 \int|\mathcal B(t)-\mathcal B(s)|^q\,d\lambda
 \le q!C_h^q|t-s|^{q/2}
\]

for even `q`. Linear interpolation handles times within one collision grid interval. The maximum of the dyadic increments at level `j` has `L^q` norm bounded by

\[
 (q!)^{1/q}C_h2^{-j(1/2-1/q)}.
\]

For `q >= 4`, the dyadic series is uniformly summable. Minkowski's inequality therefore yields factorial moments of the path supremum, and expansion of the exponential gives a uniform exponential moment without dividing by the rare-event probability.

The exact return-clock identity then bounds the actual-return bridge by the collision bridge on central windows. The occupation coordinate supplies the needed time-change estimate; no independence of the clock and path is assumed.

The argument is coherent. It remains a path-amplitude estimate and says nothing by itself about concentration of scalar roof density.

## 10. Exponentially weighted physical-defect mass

Cauchy--Schwarz combines the unweighted physical local-mass estimate of order `epsilon^(1/16)` with the doubled exponential path moment. The resulting weighted defect estimate is of order

\[
 \varepsilon^{1/32}.
\]

This applies to the original incidence and clearance subsources and does not transport trajectories through a physical seam. It is stronger than their unweighted path-amplitude control, but it is still integrated in the roof variable.

The manuscript correctly refuses to interpret this as a scalar essential-height estimate.

## 11. Polynomial-growth tests and same-roof Wasserstein transport

The growth-upgrade lemma truncates a polynomial-growth path test at radius `R`, paying `R^p` times the mean bounded-Lipschitz error and an exponentially small tail. Choosing `R` proportional to `log(1/e)` gives

\[
 Ce(1+|\log e|^p).
\]

The same structure applies to the unbounded transport cost. Bounded-cost Kantorovich duality controls the truncated metric by bounded-Lipschitz distance, while exponential path moments pay the tail of the supremum metric. No measurable choice of optimal couplings is required because the pointwise infimum estimate is integrated afterwards.

The reference-roof statement correctly requires the stronger domination supplied by a pointwise arithmetic floor. Total variation of the roof laws alone would not transfer an unbounded Wasserstein cost, and the manuscript does not use it for that purpose.

The covariance and path-maximum moment corollaries follow from `W_2` or higher-order coupling estimates and the uniform exponential moments. I found no logical defect in these transport upgrades.

## 12. Fixed-band finite-count window estimates in revision 54

Revision 54 fixes one auxiliary roof band `B_circ` once and for all. On each moving peak chart, the four-frequency Gaussian integral has size `m^(-2)`; complementary powers decay exponentially. A positive band-limited interval majorant has mass `h+O(B_circ^(-1))` and Fourier supremum bounded by that mass.

This yields the finite-count estimate

\[
 m^2\nu_R^*\{K_n=k,N_n=m,T_n\in I\}
 \le C(1+h)(1+m^2\rho^{m/2})
\]

for every interval length `h > 0`. This is a genuine finite inequality, not a fixed-window limit used at a shrinking window.

The guard complement is bounded by the union of section, incidence, and clearance strips over all depths. The width-uniform marked local estimates give the leading sum

\[
 C(1+h)\varepsilon^{1/16},
\]

and summing the width-independent finite-count errors before taking any limit gives

\[
 C(1+h)m^3\rho^{m/2}.
\]

The clearance of flight `j` remains observed at collision `j+1`, while occupation remains half-open at times `0,...,m-1`. The source enlargement pays the section factor `1/c` once.

Subject to the inherited moving-peak and marked-strip estimates, this finite-count window argument is internally consistent.

## 13. The polynomial protected height

The protected source is divided into high-gradient and low-gradient parts.

For the high-gradient part, the flow duration has size

\[
 h'_\varepsilon\asymp\varepsilon^9.
\]

The finite window inequality is divided by that duration, producing the explicit height loss

\[
 C\varepsilon^{-9}(1+m^2\rho^{m/2}).
\]

The inverse short-window length is paid; it is not discarded.

For the low-gradient part, each point is completed to an `epsilon/2`-protected normal critical center. The corresponding roof collar has width

\[
 r_\varepsilon\asymp\varepsilon^6.
\]

The inherited mass and density comparison for disjoint collars converts a sum of critical Jacobian coefficients into an unmarked probability on a roof window of that width. The resulting `epsilon^(-6)` bound is smaller than the high-gradient budget.

The load-bearing continuum questions are:

- global same-label injectivity of the protected flow box;
- the exact relative-Jacobian bound on that box;
- completion of every low-gradient point to a protected normal critical center;
- inclusion of its roof in the stated collar;
- disjointness and single charging of the collars;
- preservation of the original exact labels and section normalization.

The text addresses these points through inherited modules, but they require specialist checking. I did not find an internal contradiction in the new deduction.

## 14. The high-density tail principle

The abstract tail lemma assumes an exact positive split

\[
 P_m=A_{m,\varepsilon}+B_{m,\varepsilon},
\]

with

\[
 \|A_{m,\varepsilon}\|_\infty\le C_A\varepsilon^{-K},
 \qquad
 \int B_{m,\varepsilon}\le C_I(\varepsilon^\alpha+e^{-\kappa m}).
\]

At density level `L`, choosing

\[
 \varepsilon=(2C_A/L)^{1/K}
\]

makes `A <= L/2`. Hence on `{P > L}` one has `B >= P/2`, and

\[
 \int_{\{P>L\}}P
 \le C\left(L^{-\alpha/K}+e^{-\kappa m}\right).
\]

For the billiard application, `K=9` and `alpha=1/16`, giving `alpha/K=1/144`.

The exponentially small error cannot be integrated over all levels. Revision 54 correctly truncates the layer-cake integral at the complete finite-count height cap

\[
 \|P_m\|_\infty\le C_He^{\Gamma m}.
\]

The error contribution is then bounded by

\[
 e^{-\kappa m}e^{s\Gamma m},
\]

which is uniformly bounded and tends to zero when `s Gamma < kappa`. Thus every

\[
 0<s<\min\{1/144,\kappa/\Gamma\}
\]

is admissible. The manuscript chooses a strict interior exponent.

This is the correct way to obtain a genuine, nonempty higher-integrability range from the finite-count estimates. A family of separate fixed-`epsilon` limsups would not suffice, and the manuscript does not use such an invalid argument.

## 15. Uniform higher integrability

Applying the tail principle on an arbitrary translated interval yields

\[
 \int_{I_t\cap\{P>L\}}P
 \le C(1+h)(L^{-1/144}+e^{-\kappa m})
\]

and a uniform local `L^{q_*}` bound for the complete original normalized density.

The theorem keeps every exact label and has no source guard. The exponent `q_*>1` may be extremely close to one because it depends on one fixed-band decay rate and the complete exponential height constant. The lack of a numerical lower bound does not invalidate the theorem, but it limits its quantitative and editorial force.

The conclusion is higher integrability, not essential boundedness. The manuscript states this distinction correctly.

## 16. Positive physical remainders in local `L^q`

Each positive physical remainder satisfies

\[
 0\le B_\varepsilon\le P.
\]

Its local `L^1` mass is of order

\[
 \varepsilon^{1/16}+e^{-\kappa m},
\]

while its `L^{q_*}` moment is bounded by that of `P`. The interpolation exponent

\[
 \theta_q=\frac{q_*-q}{q_*-1}
\]

satisfies

\[
 q=\theta_q+q_*(1-\theta_q).
\]

Hence

\[
 \int B_\varepsilon^q
 \le C(1+h)
       (\varepsilon^{1/16}+e^{-\kappa m})^{\theta_q}.
\]

The same estimate applies separately to incidence and clearance and, by Radon--Nikodym domination, to arbitrary bounded source insertions.

Minkowski's integral inequality gives a local `L^q` convolution bound with the scale-invariant `L^1` norm of the reconstruction kernel. No reconstruction band depending on the collision count enters a spectral theorem.

The interpolation and convolution steps are correct.

## 17. The complete scalar and path-valued local `L^q` laws

The scalar error already converges uniformly in translated local `L^1` windows. The transition kernel is uniformly bounded, and the complete density has a uniform local `L^{q_*}` moment. Interpolation therefore gives local `L^q` convergence for every `1<q<q_*`.

For the path-valued error, the bounded-Lipschitz dual norm is bounded by

\[
 \|\mathbf P-G\mathsf W\|_{\mathrm{BL}^*}
 \le P+|G|.
\]

Its local `L^1` norm tends to zero by the revision-52/53 path-valued theorem, and its `L^{q_*}` moment is bounded by the scalar estimate. The same interpolation gives the path-dual roof `L^q` law. The actual-return version uses the inherited roof-integrated time-change transfer on its central target class.

This is a genuine strengthening of the topology in the roof coordinate. It remains bounded-Lipschitz, rather than total variation, in the path coordinate.

## 18. Forward likelihood and entropy

On a fixed window where

\[
 G(u)\ge d>0
\]

almost everywhere, define the true and reference conditional roof laws from the same exact event. Their likelihood ratio is

\[
 r(u)=\frac{H P(u)}{F G(u)},
 \qquad F=\int_I P,\quad H=\int_I G.
\]

The local law gives `F-H -> 0`, while the reference floor gives `F,H` uniform positive lower bounds. Since `G` is also uniformly bounded,

\[
 \int|r-1|^q\,dQ
 \le C_{d,h,q}
 \left(\int_I|P-G|^q+|F-H|^q\right).
\]

The local `L^q` theorem therefore proves likelihood convergence for every `1<q<q_*`.

For Renyi order `s<q_*`, `L^s` convergence of `r` to one gives convergence of `\int r^s dQ` to one. For relative entropy, the inequality

\[
 0\le x\log x-x+1\le C_q|x-1|^q,
 \qquad 1<q<2,
\]

is applicable because the constructed `q_*` is strictly below two. Integration and `\int(r-1)dQ=0` prove forward relative-entropy convergence.

This closes one item explicitly listed as open in the revision-52 report. It does not prove an essential likelihood bound and does not assign a reference law to a zero arithmetic class.

## 19. What has and has not been closed since revision 52

The combined revision-53/54 changes close several real issues:

- the path numerator is controlled in a common measure-valued topology rather than separately for each test;
- the signed path inverse has a rigorous compactness principle;
- all pinned increment orders have explicit factorial constants;
- the complete pinned paths have exponential moments under the microscopic source;
- same-roof bridges converge in every fixed finite Wasserstein order in conditional roof mean;
- the complete raw density has a nontrivial higher-integrability range;
- both positive physical remainders vanish in stronger local `L^q` norms;
- the scalar and path-valued raw laws hold in local roof `L^q`;
- forward likelihood and forward entropy converge under a pointwise arithmetic floor.

The principal raw endpoint is nevertheless unchanged:

\[
 \lim_{B\to\infty}\limsup_{m\to\infty}
 \|m^2b_{\rm inc}^{\varepsilon(B),1}\|_{\infty,M}=0,
\]

and

\[
 \lim_{B\to\infty}\limsup_{m\to\infty}
 \|m^2b_{\rm clr}^{\varepsilon(B),1}\|_{\infty,M}=0
\]

remain unproved.

These are positive-source estimates. There is no remaining possibility that an unidentified signed cancellation will close the theorem automatically. The new `L^q` bounds make the potential spikes rarer in an integral sense, but do not bound their height.

## 20. Why finite `L^q` and entropy do not finish the theorem

A uniformly bounded `L^{1+s}` family can have arbitrarily high spikes of sufficiently small width. Forward and reverse relative entropy may both tend to zero while the essential supremum of the likelihood ratio diverges. Revision 54 gives an explicit abstract example illustrating this topology distinction.

Consequently none of the following follows from the new theorems:

- two-sided pointwise raw-density convergence;
- forward essential likelihood convergence;
- uniform same-roof bridge convergence at every positive-reference roof;
- an externally prescribed exceptional-roof statement;
- pointwise suppression of incidence spikes;
- pointwise suppression of clearance spikes.

The manuscript is correct not to claim these implications.

## 21. Arithmetic modulation

At fixed radius the exact-index main term remains

\[
 c\,\mathfrak a_R(k,n,m)g_{\Omega_R}(Z),
\]

or its equivalent `D_R` normalization. Uniformly in the radius it remains the finite transition kernel `\mathcal L_{m,R}` with moving damped branches.

Revision 54 does not prove that the actual section phase masses are uniform, so it does not prove that every arithmetic factor equals one. This is not a defect in the theorems as currently stated: the arithmetic factor is part of the correct result. It does mean that an unmodulated radius-uniform singleton theorem remains unavailable unless the zero-residue criterion is separately verified.

A final paper should either embrace the arithmetic transition kernel as intrinsic in its principal theorem or prove the concrete zero-residue specialization. It should not alternate editorially between these two endpoints.

## 22. Generality and top-four significance

The combined results are substantial within the specialized program. The conjunction of exact return and collision indices, arithmetic residues, complete raw roof density, all-depth physical-source decomposition, path-valued inversion, same-roof conditional transport, higher density integrability, and two-directed entropy control is technically impressive.

However, the hardest inputs remain specific to one triangular finite-horizon Lorentz family:

- the particular moving section;
- image-side incidence and clearance geometry;
- the protected flow boxes and critical collars;
- the local collision Banach spaces;
- the full occupation-torus peripheral analysis;
- the exact finite resonance structure;
- the all-depth decision and physical-source decomposition.

The abstract signed-measure, tail-integration, interpolation, and entropy principles are useful, but they are comparatively elementary once these model-specific inputs are available. Revision 54 does not add a second independent singular-hyperbolic application or formulate a general theorem whose hypotheses are verified in several distinct systems.

At a strong specialist dynamics/probability journal, the local `L^q` density law, same-roof Wasserstein bridges, and entropy conclusions could form a significant paper if the proof chain withstands expert scrutiny and is presented in a focused architecture. At the requested four-journal benchmark, the combination of model specificity, extraordinary length, lack of independent specialist verification, and the still-open pointwise endpoint weighs decisively against acceptance.

## 23. Independent specialist verification

No independent human specialist audit has been obtained. The following points deserve line-by-line checking by experts in dispersing billiards and anisotropic transfer operators:

1. the complete fixed-band moving-peak decomposition on the full occupation torus;
2. uniform complex neighborhoods and contours for all derivative orders;
3. tight positive dominators for signed path inverses;
4. protected endpoint influence for the entire path;
5. chartwise constancy of displacement and occupation prefixes;
6. the physical thin-layer multiplier through all homogeneity strips;
7. width- and mark-uniform local upper bounds;
8. the exact all-depth source partition;
9. the protected flow-box duration of order `epsilon^9`;
10. relative Jacobian bounds and global same-label injectivity;
11. near-critical completion at scale `epsilon^3`;
12. critical collar width and mass-density comparison at scale `epsilon^6`;
13. disjointness and one-time charging of collars;
14. the inherited complete exponential density cap;
15. exact normalization by the section mass `c`;
16. half-open occupation conventions at the terminal collision;
17. the actual return-clock transformation;
18. uniformity of the pointwise arithmetic reference floor through parameter transitions.

The source verifier, finite diagnostics, native build, and rendered theorem pages are valuable regression evidence, but not substitutes for this audit.

## 24. Required mathematical changes before another top-four review

A subsequent revision seeking the same benchmark should address the following.

1. **Control the positive incidence height.**  
   Prove central-scale essential-supremum smallness of the complete first-incidence physical remainder, uniformly in the exact labels and radius.

2. **Control the positive clearance height.**  
   Prove the corresponding estimate for the competing-hit clearance remainder without continuing an orbit through a physical seam.

3. **Complete the two-sided arithmetic raw theorem.**  
   Combine the two positive-height estimates with the existing transition kernel and positive-remainder representation.

4. **Deduce the unconditional uniform same-roof bridge.**  
   Once scalar height is controlled, carry out the already isolated path-measure implication on every positive-reference central set.

5. **Resolve the final arithmetic presentation.**  
   Either prove the concrete zero-residue criterion or state the arithmetic factor and transition kernel as permanent parts of the principal theorem.

6. **Obtain independent specialist review.**  
   In particular, the physical multipliers, protected critical geometry, full occupation spectrum, moving peaks, and all-depth source decomposition require external human verification.

7. **Extract a broader theorem.**  
   Formulate a reusable singular-hyperbolic result linking transverse positive boundary layers, polynomial protected height, an exponential complete cap, local `L^q` raw laws, and same-roof conditional transport; verify it in more than one genuinely different system if top-four breadth is sought.

8. **Reduce the submission burden.**  
   Present the shortest complete proof route to one principal endpoint. Historical pipelines, duplicated theorem hierarchies, validation ledgers, and unfinished alternative endpoints should not dominate the journal article.

9. **Sharpen the novelty comparison.**  
   Explain theorem by theorem what is not available from existing Lorentz-process, billiard mixing-local-limit, and suspension local-limit frameworks after their hypotheses are checked.

## 25. Technical and presentation comments

1. Keep the auxiliary spectral band, reconstruction band, protection scale, density level, and collision count visibly distinct.
2. State whenever an estimate is finite in `m`, rather than a limsup for each fixed scale.
3. Keep the inverse short-window length in every protected flow-box estimate.
4. Do not allow the auxiliary band to depend on the density level or collision count.
5. Preserve the exact exponent calculation `(1/16)/9 = 1/144`.
6. Keep the exponential error term in the superlevel estimate until it has been integrated to the complete height cap.
7. State the dependence of `q_*` on `kappa/Gamma`; do not advertise a universal numerical exponent.
8. Preserve the distinction between local roof `L^q` and essential supremum.
9. Preserve the distinction between bounded-Lipschitz path dual norm and path-space total variation.
10. Keep the original exact-label source normalization and pay `1/c` only when enlarging to the ambient collision source.
11. Preserve the clearance mark at collision `j+1` and the occupation interval `0,...,m-1`.
12. State central-target enlargement across a roof window explicitly.
13. Keep signed `G` in unnormalized raw laws and positive `G` only under an explicit reference floor in likelihood statements.
14. Do not transfer unbounded transport costs from true to reference roof law using total variation alone.
15. Preserve the pointwise reference-floor hypothesis in every forward likelihood or reference-Wasserstein theorem.
16. Do not infer forward essential likelihood from forward relative entropy.
17. Do not infer physical scalar height from exponential path moments.
18. Keep the common positive path remainder independent of the chosen test.
19. Retain the countable norming-class and common-null-set constructions.
20. Explain in the main text, not only metadata, why the higher-integrability theorem does not close the pointwise raw endpoint.
21. Consider moving source-verification and finite-test detail to a reproducibility supplement.
22. Reduce duplication between historical leading theorems and the current principal results.

## 26. Final assessment

Revisions 53 and 54 are genuine theorem-bearing advances over the last externally reviewed source.

Revision 53 supplies a sound signed-measure compactness mechanism, a common positive path remainder, factorial all-order pinned moments, exponential complete-path moments, polynomial-growth path laws, finite-order same-roof Wasserstein convergence, and conditional moment consequences.

Revision 54 supplies a simultaneous finite-count protected-height budget, a correctly truncated high-density tail argument, a strictly nonempty higher-integrability range for the complete original exact-label density, local roof `L^q` convergence of scalar and path-valued raw laws, local `L^q` control of both positive physical remainders, and forward likelihood, relative-entropy, and small-order Renyi convergence under the correct pointwise arithmetic floor.

I found no decisive error in these new deductions within their declared scope, subject to the inherited continuum inputs and the specialist verification obligations listed above.

The manuscript nevertheless remains short of the endpoint which continues to organize its title and proof architecture. Positive incidence and clearance spikes have not been excluded in essential supremum; hence the two-sided pointwise arithmetic raw-density theorem, forward essential likelihood, and unconditional uniform same-roof bridge remain open.

The new finite-norm and entropy theorems make the remaining obstruction narrower and more explicit. They do not remove it.

**Final recommendation: reject in the present form at the requested four-journal benchmark.**