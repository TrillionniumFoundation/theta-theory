# External top-four referee report on A2 v38

**Manuscript:** Qian Qi, *Scalar collision laws and recognition of periodic dispersing billiards*  
**Reviewed revision:** `revision/a2-v38-finite-field-rigidity-2026-10-04`  
**Equivalent referee-copy alias:** `revision/a2-v38-referee-copy-2026-10-04`  
**Reviewed commit:** `a346669928e5147cf2c0ef86c3bc2a455b512d14`  
**Reviewed repository tree:** `3abc9b8fb500c87b125332e7d798a27f72a81a33`  
**Active core tree:** `64cf5f5af705113b494c6f16ad538c413dfbc5e4`  
**Mathematical checkpoint:** `3178349cc91a3f0f0607dd54ab13039e7c999874`  
**Immediate author source:** A2 v37, `02e6a6c799cb00c7dc7304ddfbf7ac885c83ea4d`  
**Controlling preceding report:** `3c6b195c183df2c52e58e25cf59f7e3fcba07fc3`  
**Manuscript directory:** `papers/A2-v38-finite-field-rigidity`  
**Date:** 4 October 2026  
**Requested benchmark:** *Annals of Mathematics* / *Acta Mathematica* / *Inventiones Mathematicae* / *Journal of the AMS*  
**Status:** author-requested, AI-assisted referee-style assessment; not a journal decision, proof certificate, apparatus validation, or exhaustive priority determination.

## 1. Recommendation

**Recommendation at the requested four-journal benchmark: reject.**

Version 38 is the strongest and most conceptually coherent A2 revision I have examined. It contains genuine new mathematics and, importantly, it also activates the substantial v37 additions that had not received a separate external report: a global scalar-to-occupation inverse, exact equality between response and obstacle translation-period groups without a periodicity prior, reconstruction of independently translated homothetic launch supports without component matching, and a stationary minimax theorem with matching polynomial power. Version 38 itself then adds a fixed finite-stencil optimal-stopping representation, arbitrary-data Lipschitz stability with primal--dual certificates, and a direction-free exact rigidity theorem whose scalar normalization is intrinsic perimeter rather than coordinate width.

On the parts audited in detail, I found no fatal counterexample. The global stopping formula, period cancellation, lower support-envelope inverse, translation/period gauge, effective collision-boundary cancellation, Hellinger information bound, shrinking-layer upper construction, killed stopping polytope, finite occupation sampling law, general centered-increment exit argument, and isotropic perimeter deficit are mutually consistent under the stated assumptions. The exact-source workflow also succeeds at the reviewed SHA and preserves the complete active manuscript and evidence.

The negative recommendation is therefore editorial and conceptual rather than a claim that the central theorems are known to be false. The strongest exact datum is a pair of actively controlled scalar response fields on the entire plane, not a passive billiard invariant. The finite theorems remain engineered experiments with prescribed reciprocal joint laws, labelled settings, exact homothety relations, quantitative footprint and boundary-mass priors, arbitrarily precise nominal positions, and, for uniform finite period decisions, a positive nonperiod-patch margin. Once the reciprocal identity has converted the collision sensor into a Poisson/occupation problem, the abstract mechanisms are classical optimal stopping and linear programming, Minkowski support cancellation, Cauchy perimeter, active boundary estimation, and information-theoretic packing. Their integration is technically serious, but in my judgment it does not amount to the exceptional, field-transforming conceptual advance normally required by the four journals named above.

The manuscript is now a credible candidate for a strong specialist journal, and perhaps for a broad journal after a fresh human proof review and substantial editorial compression. At the requested benchmark, however, I would not recommend another open-ended revision cycle.

## 2. Frozen source and chronology

The two v38 revision names listed above resolve to the same author head

`a346669928e5147cf2c0ef86c3bc2a455b512d14`

with repository tree

`3abc9b8fb500c87b125332e7d798a27f72a81a33`.

The final commit changes only the first-page layout in `main.tex`; the mathematical checkpoint is its parent chain beginning at

`3178349cc91a3f0f0607dd54ab13039e7c999874`.

The immediate mathematical base is A2 v37 at

`02e6a6c799cb00c7dc7304ddfbf7ac885c83ea4d`,

which itself is based directly on the final v36 review head

`3c6b195c183df2c52e58e25cf59f7e3fcba07fc3`.

That report reviewed v36 author commit

`2559749a038fd2b5ec46d7cc74fdb4bd844b266a`.

Version 38 correctly states that no intervening v37 referee report is being presumed. I therefore treated the v37 global rigidity and minimax additions, together with the new v38 finite-stencil and isotropic additions, as one combined unreviewed mathematical package.

The source pins identify the v37 repository tree

`f640fe628767f4312810f61c1eed2db85eefcc87`

and retained v37 core tree

`12a9e42058be2b228f6855e8fbf296ac97555d52`.

All twenty-four inherited v37 core files remain active, and the new active core tree is

`64cf5f5af705113b494c6f16ad538c413dfbc5e4`.

No A2 revision branch later than v38 existed when this review was frozen. The present review branch starts directly from the reviewed author head and adds files only under

`reviews/a2-v38-external-harsh-top4-rereview-2026-10-04/`.

No manuscript source, author branch, prior report, workflow, retained paper, or unrelated repository path is modified.

## 3. The theorem package

The observation remains one bit per attempted preparation. A bit equals one precisely when a free start has a first collision on a prescribed unreflected segment. A solid start and a free miss both return zero and both remain in the denominator.

For a stationary launch displacement `Z` and a commanded displacement `a`, the forward experiment uses `(x+Z,a)` while the reciprocal reverse experiment uses `(x+Z+a,-a)` with a fresh draw from the same prescribed joint law. If `F` and `R` are the two pooled mean fields, their difference satisfies

\[
        g=F-R=(T-I)v,
        \qquad
        v(x)=\mathbb P\{x+Z\in\mathcal O\}.
\]

The current manuscript has four conceptually distinct layers.

1. **Global exact response rigidity.** For arbitrary locally finite configurations of uniformly bounded, positively separated compact convex obstacles, the full difference field determines the occupation and its positivity components. It also determines the complete translation-period group, without a periodicity prior.
2. **Unknown and unregistered footprints.** Several labelled stationary settings may have independently translated homothetic supports, unknown densities, unknown scale ratios, and no cross-setting obstacle matching. Width or perimeter deficits determine scale; centered support envelopes separate the common obstacle collection from the footprint; the complete geometric fiber is classified.
3. **Sharp finite stationary reconstruction.** On bounded smooth periodic classes, a rare-collision boundary query and physical packing give matching upper and lower polynomial powers for one fixed known disk law, up to one logarithmic factor.
4. **Finite-stencil and isotropic extensions.** Pointwise occupation becomes a fixed finite-dimensional stopping linear program with arbitrary-data stability and certified finite sampling. Exact period rigidity extends from the compass to every known bounded mean-zero displacement law of positive second moment; uniform directions replace directional width by intrinsic perimeter.

These layers use different data and hypotheses. The exact whole-field statements should not be conflated with the finite statistical experiment, and the finite pointwise occupation theorem should not be paraphrased as a finite crystallinity certificate.

## 4. Audit of the global scalar-to-occupation inverse

Let the positive components of the occupation be

\[
        P_C=C+(-A).
\]

They have uniformly bounded diameter and gaps greater than one virtual step. For the compass walk, the first exit time from the containing positive component has uniformly bounded expectation and a geometric tail. The bounded martingale identity gives, for every integrable stopping time,

\[
 -\mathbb E_x\sum_{k<\tau}g(X_k)
        =v(x)-\mathbb E_xv(X_\tau)
        \le v(x).
\]

Immediate stopping attains equality when `v(x)=0`; otherwise the containing-component exit attains equality because the exit point has zero occupation. Hence

\[
 v(x)=\sup_{\tau:\,\mathbb E_x\tau\le H}
       \mathbb E_x\left[-\sum_{k<\tau}g(X_k)\right].
\]

This proves uniqueness and the global Lipschitz estimate in the forcing. The monotone obstacle iteration is the corresponding finite-horizon value iteration, and the exit-tail estimate gives its uniform error. I found this argument sound. It does not require knowing the positive components in advance; they enter only through the attaining rule in the proof.

The exact period identity is also coherent. Translation covariance gives

\[
 \operatorname{Per}(\mathcal O)
       \subseteq\operatorname{Per}(F,R)
       \subseteq\operatorname{Per}(g).
\]

The stopping inverse commutes with translation, so every period of `g` is a period of `v`. A period of `v` permutes the separated expanded components `C+(-A)`. Cancelling the common laboratory support function of `-A` shows that the same vector permutes the original obstacles. Thus

\[
 \operatorname{Per}(F,R)=\operatorname{Per}(g)
       =\operatorname{Per}(v)=\operatorname{Per}(\mathcal O).
\]

This is a real broadening beyond the prior-relative finite period test. It identifies crystallinity from the **exact active response field**, not from a finite aperture or a passive orbit invariant.

## 5. Audit of unregistered homothetic footprints

At setting `i`, write

\[
        A_i=b_i+\rho_i A_0,
        \qquad s(A_0)=0,
        \qquad \rho_1=1.
\]

The densities at different settings need not be scaled copies. From `g_i` one recovers the collection of expanded components

\[
        \mathcal P_i=\{C+(-A_i)\}.
\]

For any isolated complete expanded component `P=C+(-A_i)`, the integrated forward response measures the coordinate-width sum of `C`. Therefore

\[
 d_i(P)=\mathcal W(P)-\frac2t\int_{E_P}F_i
       =\mathcal W(A_i),
\]

which is independent of the selected obstacle and yields the ratios `rho_i` without cross-setting component matching. This route uses the raw pooled forward mean `F_i`; it is not a difference-only statistic.

The centered support envelope

\[
 L_i(u)=\inf_{P\in\mathcal P_i}p_P^\circ(u).
\]

This takes the form

\[
 L_i(u)=\inf_Cp_C^\circ(u)+\rho_i p_{-A_0}(u).
\]

Hence, for any distinct scale,

\[
 p_{-A_0}=\frac{L_k-L_1}{\rho_k-1}.
\]

This cancellation does not require the infimum to be attained by the same obstacle in each direction or setting. Subtracting the recovered footprint from every expanded support gives the configuration in the frame `O-b_i`.

The claimed ambiguity is also the correct one. Equality of the recovered configurations implies a common translation `h` and, setting by setting, a residual shift in the obstacle period group. Conversely translating the table by `h` and the launch law at setting `i` by `h+pi_i`, with `pi_i` a period, couples the entire binary experiment. Thus the geometric fiber is

\[
 \mathcal O'=\mathcal O+h,
 \qquad
 A_i'=A_i+h+\pi_i,
 \qquad
 \pi_i\in\operatorname{Per}(\mathcal O).
\]

I found no missing shape-matching assumption in this exact argument. The finite periodic version legitimately reintroduces the bounded presentation and positive patch margin for uniform discrete decisions.

## 6. Audit of the stationary minimax theorem

The v37 lower bound is considerably stronger than the earlier response-range lower bound. The load-bearing geometric lemma controls the effective boundary of the collision strip inside a fixed launch disk. The curved boundaries of the sweep and the solid cancel wherever both translated points lie in the disk; only active arcs and the two facets remain. Each active piece of length `ell` forces both collision area and complementary area of order at least `ell^3`. This yields

\[
 L_D(C;t,e)\le K\min\{A,A_c\}^{1/3}.
\]

This holds uniformly in the command direction and length, including lengths tending to zero.

Differentiating a support interpolation then gives

\[
 |P'(\lambda)|
   \le K\varepsilon\min\{P(\lambda),1-P(\lambda)\}^{1/3}.
\]

It therefore implies a squared-Hellinger bound of order `epsilon^(3/2)` for every permitted short command. The manuscript includes the endpoint analysis needed when probabilities approach zero or one.

The accompanying information lemma bounds the mutual information of one Bernoulli observation by the squared Hellinger diameter divided by `ln 2`. Applied conditionally after every adaptive history and combined with the physical support-bump packing, it gives the expected-attempt lower power

\[
        \nu^{-(3s/2+1)/(s-2)}.
\]

The shrinking-layer rare-collision construction attains the same polynomial power for the fixed pooled compass, with one logarithmic factor. The lower controller class is strictly more informative: it permits arbitrary adaptive directions and arbitrarily short commands. Thus the sandwich

\[
 c\nu^{-q_0}
 \le N^*_{\rm short}(\nu,\delta)
 \le N^*_{\rm pool}(\nu,\delta)
 \le C\nu^{-q_0}\log\frac{C}{\nu\delta}.
\]

This is logically consistent and identifies the polynomial minimax exponent on the stated known-disk experiment.

This proof is delicate. In particular, the uniform effective-boundary estimate as the command length tends to zero, the moving-boundary derivative formula, and the reduction to one common indexed component family are the places where a human specialist should concentrate a fresh proof review. I found no finite counterexample or internal contradiction, but the repository checks are not substitutes for that analysis.

The scope must remain explicit. The matching statement is for a fixed known uniform-disk law, a near-circular physical packing contained in one bounded smooth class, fixed confidence, centered `C^2` loss, and worst-case expected attempt cost. It does not identify sharp logarithms, sharp confidence dependence, or the exponent for every boundary-decaying density.

## 7. Audit of the finite-stencil inverse

Version 38 fixes a square stencil

\[
 S=\{-K,\ldots,K\}^2,
 \qquad K=\left\lceil\frac{D+\Delta}{t}\right\rceil.
\]

Let `Q` be the substochastic killed compass matrix, and let

\[
 G=(I-Q)^{-1},
 \qquad
 \mathcal M_o=\{m\ge0:(I-Q^{\mathsf T})m\le e_o\}.
\]

The proof correctly interprets `m` as a continuation-visit measure. Writing the slack as the stopping mass gives flow conservation. Conversely, the statewise continuation probability `m_z/(m_z+s_z)` realizes every feasible vector; transience follows because the continuation transition matrix is dominated by the killed walk. Nonnegative Green multiplication yields coordinate and total-mass bounds, hence compactness.

Linear-program duality gives

\[
 \mathcal V(f)=\max_{m\in\mathcal M_o}(-f^{\mathsf T}m)
 =\min\{u_o:u\ge0,(I-Q)u\ge-f\}.
\]

The corresponding Bellman form is

\[
        u=\max\{0,Qu-f\}.
\]

For physical forcing `f_x(z)=g(x+tz)`, every killed stopping payoff is at most `v(x)`. The first exit from the target's containing positive component occurs before exit from the square because the whole component lies within coordinate distance `Kt`; this rule attains equality. Other positive components may touch the computational boundary, but their nonnegative terminal occupation only lowers arbitrary stopping payoffs. Therefore no unobserved physical zero-boundary oracle has been inserted.

The arbitrary-data stability

\[
 |\mathcal V(f)-\mathcal V(\widetilde f)|
 \le\sum_zG_{oz}|f_z-\widetilde f_z|
 \le h_o\|f-\widetilde f\|_\infty.
\]

This is a direct consequence of the common feasible polytope and is a useful strengthening over a horizon-dependent error accumulation.

The finite sampling theorem is also correctly scoped. It estimates two raw means at each of `M` fixed sites, uses Hoeffding and the Green mass to control the forcing vector, and reserves numerical error for a rational primal--dual gap. The result estimates **one occupation value** to accuracy `epsilon` using `O(epsilon^{-2}log(1/delta))` attempted bits at a prior-dependent fixed site set. It does not turn finitely many values into a whole-field period or crystallinity certificate.

## 8. Audit of general and isotropic command laws

Let `mu` be a known bounded displacement law with

\[
        \int a\,d\mu(a)=0,
        \qquad
        \int|a|^2d\mu(a)>0.
\]

The reciprocal balance gives `g_mu=(T_mu-I)v`. The process

\[
 |X_n-x|^2-n\sigma_\mu^2
\]

is a martingale. Bounded obstacle diameter and bounded jumps give a uniform expected exit time from the containing positive component. No invertibility of the covariance is needed; a nontrivial centered law supported on a line still exits a bounded component in finite expected time. The same stopping argument and support cancellation therefore yield the complete period group.

This is an exact response-field theorem. When `mu` has continuous support, it does not imply that finitely many mean samples evaluate `T_mu` or its stopping functional exactly. The manuscript states this distinction.

For directions uniform on the circle, the integrated collision strip at one direction has area `t` times the transverse width. Cauchy's perimeter formula gives

\[
 \int_{E_P}F_{i,\mu}(x)\,dx
       =\frac t\pi\mathcal L(C).
\]

Since planar perimeter is additive under Minkowski addition,

\[
 d_i^{\rm iso}(P)
   =\mathcal L(P)-\frac\pi t\int_{E_P}F_{i,\mu}
   =\mathcal L(A_i).
\]

This identifies scale ratios without a preferred laboratory axis. The same centered support-envelope argument then recovers the footprint and configurations, with the same translation/period gauge.

The normalization and registration algebra are sound. The route requires the raw forward mean as well as the reciprocal difference; only the occupation/period inverse itself is difference-only. No finite isotropic minimax theorem is proved, and none should be inferred from the exact result.

## 9. Qualifications and revisions required for publication

The following points do not overturn the audited theorem package, but they should be made visually unavoidable in any journal submission.

### 9.1 Exact full fields are a very rich active datum

The global rigidity theorem assumes `F` and `R`, or `g`, at every nominal center on the plane. It is a whole-field active response theorem. Calling the output a scalar field does not make the information low-dimensional. The finite-stencil theorem is pointwise and does not by itself provide a finite global acquisition theorem for the period group.

### 9.2 Keep raw means and reciprocal differences distinct

The stopping inverse and exact period theorem use `g=F-R`. Width and perimeter deficits use `F` itself. The area-normalized calibration route is difference-only. Abstract, introduction, theorem summaries, and future comparisons should preserve these distinctions exactly.

### 9.3 Separate exact and finite period results

Exact response-period equality needs no periodicity prior. Uniform finite recovery of a primitive lattice still uses a bounded periodic presentation and a known positive nonperiod-patch margin. The finite nonperiodic-cloud theorem instead assumes that a known bounded aperture captures every component. None is a finite, prior-free test for an arbitrary unknown infinite configuration.

### 9.4 The finite-stencil theorem is pointwise

Its fixed number of sites depends on the prior ratio `(D+Delta)/t`, and its physical aperture also needs a coarse footprint-location bound. Repeating it over a growing target set incurs the corresponding sum of batch costs. It should not be advertised as a finite sufficient statistic for the entire response field.

### 9.5 The minimax statement has a precise comparator

The matching polynomial power concerns a known uniform disk, fixed positive radius range, one near-circle packing inside a bounded smooth class, centered `C^2` loss, fixed confidence, and expected attempts. The upper and lower command classes differ in the favorable direction, which is legitimate. The remaining logarithm and confidence dependence are unresolved.

### 9.6 Homothety remains an apparatus assumption

The origins and ratios are reconstructed, but labelled settings and exact positive homothety of their supports are assumed. The per-setting stationary densities may differ, which is a strength. Physical certification, manufacture, travel, and metrology are outside the attempted-bit and digital-description counts.

### 9.7 The article is still accreted

The seventy-one-page primary contains global exact rigidity, blind footprint registration, active smooth reconstruction, sharp minimax analysis, finite stopping linear programs, isotropic commands, and the complete historical localized/calibration chain. The reordering is much better than in earlier revisions, but the paper still reads as several substantial articles accumulated into one source. A focused journal version should identify one dominant theorem package and move older self-contained programmes to separately citable papers or appendices of genuinely subordinate status.

## 10. Top-four significance assessment

The current paper deserves substantially more credit than the earlier A2 revisions. In particular:

- equality of the full response and obstacle period groups without a periodicity prior is clean and broad within the active-field model;
- the lower centered-support envelope avoids cross-setting component matching in a nontrivial way;
- the Hellinger cancellation closes the polynomial stationary rate gap on the stated disk experiment;
- the finite stopping polytope gives a useful robust and certifiable local inverse;
- the isotropic perimeter normalization removes the arbitrary coordinate-width choice.

Nevertheless, the conceptual reach remains bounded by the observation model. The exact rigidity starts from continuum active response fields. The finite global conclusions require strong smoothness, separation, aperture, homothety, and period margins. The main engines after the reciprocal reduction are recognizable instances of classical stopped Poisson inversion, occupation-measure linear programming, mathematical morphology, convex support/perimeter identities, active boundary estimation, and metric-entropy/information bounds. The manuscript combines them with care and introduces collision-specific geometric arguments, especially in the rare-query and Hellinger estimates, but it does not yet alter the general understanding of billiard rigidity or inverse dynamics at the level expected by *Annals*, *Acta*, *Inventiones*, or *JAMS*.

Most notably, the result is not a rigidity theorem from a standard passive dynamical invariant such as a marked length spectrum, scattering relation, count germ, or trajectory law. Nor is the finite active experiment a universal reconstruction theorem without strong apparatus and compact-class priors. These are legitimate scopes, not correctness defects, but they govern the editorial decision.

## 11. Source qualification and reproducibility

The exact-head GitHub Actions run is

- run ID: `37188797187`;
- workflow: `A2 v38 exact-source manuscript qualification`;
- head SHA: `a346669928e5147cf2c0ef86c3bc2a455b512d14`;
- status: `completed`;
- conclusion: `success`.

Checkout, environment installation, exact-source qualification, complete-primary build, and artifact upload all succeeded. The uploaded artifact is

- artifact ID: `11297913971`;
- digest: `sha256:2296e44f9640d20d8ecb7f5f9efc9e67de826e10af74604be212ae280ed9d085`.

The receipt records:

- exact commit qualified: true;
- 71-page primary;
- 29 active TeX files;
- 265 labels;
- 66 proof environments;
- 1,796 current v38 finite checks, including all 512 deterministic stopping policies of the diagnostic model;
- 606,502 retained v37 finite checks;
- no final layout findings;
- primary PDF SHA-256 `711054010f4c7ce16f58abefa19c2ff380969df5d6c213744b0d635b1895f4c5`.

These are strong source and finite-model receipts. They are not formal proof certification or physical-sensor validation.

## 12. Independent diagnostics and limits of this review

The accompanying `verify_review.py` imports no author code and uses only the Python standard library. Ordinary and optimized executions are byte-identical, with output SHA-256

`0a3174f1ce669cd03bf564e28b2466730231dedba16a58ecc8066c81d270473b`.

It records 931,220 successful checks covering:

- all 512 deterministic stopping policies of a `3 x 3` killed compass model;
- exact flow feasibility, Green budgets, Bellman/primal equality, and arbitrary-data stability;
- a nonzero physical occupation on the computational boundary;
- bounded mean-zero increment laws with singular one-dimensional covariance;
- unlabeled centered-support envelope cancellation with changing minimizers;
- width and isotropic perimeter deficits under translated homothetic supports;
- Bernoulli Hellinger-capacity inequalities;
- stationary exponent identities and finite-sampling concentration algebra.

These checks support only finite algebra and finite models. They do not certify the continuum effective-boundary estimate, the complete infinite-configuration envelope, physical realizability of controls, the full TeX proof chain, or editorial priority. I did not conduct an exhaustive literature search, and I did not re-prove every inherited A2 lemma.

## 13. Final verdict

**Response to the controlling v36 report:** substantively successful. The current source contains the global exact period theorem, unregistered footprint inverse, matching stationary polynomial power, explicit control accounting, robust fixed-stencil evaluation, and isotropic normalization.

**Mathematical audit:** no fatal counterexample found in the new v37/v38 core; several delicate continuum steps merit independent human proof review; the theorem scopes must remain exact.

**Source delivery:** successful exact-SHA qualification with archived evidence.

**Editorial assessment:** technically serious and potentially strong for a specialist or broad field journal, but the active continuum data, engineered apparatus, strong finite priors, classical abstract engines, and accreted architecture leave it below the exceptional conceptual threshold of the requested four journals.

**Recommendation: reject at the Annals / Acta / Inventiones / JAMS benchmark.**
