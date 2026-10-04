# External top-four referee report on A2 v36

**Manuscript:** Qian Qi, *Scalar collision laws and recognition of periodic dispersing billiards*  
**Reviewed revision:** `revision/a2-v36-stationary-boundary-2026-10-04`  
**Equivalent referee-copy alias:** `revision/a2-v36-referee-copy-2026-10-04`  
**Reviewed commit:** `2559749a038fd2b5ec46d7cc74fdb4bd844b266a`  
**Reviewed repository tree:** `46ad6437731b81ffe439c48fe9ede8b2fbc1d194`  
**Active core tree:** `18974801d85e6d5760adb71d9ec15fa7da8ede4f`  
**Controlling preceding report:** `985d798e172d38c0a9df2a068fe414b2fd13bcbc`  
**Reviewed v35 author source:** `70c055e1ff090d58ecd61a5644e0fa62a7766f13`  
**Manuscript directory:** `papers/A2-v36-stationary-boundary`  
**Date:** 4 October 2026  
**Requested benchmark:** *Annals of Mathematics* / *Acta Mathematica* / *Inventiones Mathematicae* / *Journal of the AMS*  
**Status:** author-requested, AI-assisted referee-style assessment; not a journal decision, proof certificate, apparatus validation, or exhaustive priority determination.

## 1. Recommendation

**Recommendation at the requested four-journal benchmark: reject.**

Version 36 is a genuine and substantial mathematical response to the v35 report. It addresses all of that report's most concrete requests rather than merely restating the information contract.

First, the stationary finite upper bound is materially improved. The retained construction estimated a small signed reciprocal difference and therefore paid the square of the inverse boundary signal. The new argument builds a one-sided rare event directly from the original pooled collision sensor. Fixed coarse geometry identifies at most two outward compass candidates. At an exterior target one candidate has collision probability exactly zero; at inner depth `e` every selected candidate has probability at least a fixed multiple of `e^{gamma+3/2}`. A conjunction over the candidate batches therefore gives an indeterminate-layer boundary query at inverse, rather than squared inverse, signal cost. For `gamma=0`, the displayed upper power falls from `(3s+1)/(s-2)` to `(3s/2+1)/(s-2)`.

Second, the two operating footprints need no longer have a supplied ratio. The manuscript gives two independent normalizations. The first integrates an isolated pooled forward collision mean and recovers a coordinate-width sum of the original obstacle. Together with the two reconstructed positivity supports, this determines the unknown ratio by a stable linear support identity. The second uses only reciprocal differences: a finite killed-walk adjoint recovers the occupation mass, equal to the obstacle area, and a mixed-area quadratic selects the unique physical smaller root.

Third, the revision now charges the additional centers used by the scalar normalization and gives a separate binary description bound for centers, setting labels and repetition counts. Finally, the source-delivery failure identified in v35 has been repaired: the validation tools and source pins are present, and the exact-SHA hosted workflow succeeds and archives its evidence.

On the new v36 core audited in detail, I found no fatal counterexample. The compass-candidate geometry, exterior-zero and interior-positive rare query, integrated-width identity, unknown-ratio support algebra, area-normalized smaller-root argument, finite killed adjoint, error exponents and retained common-noise lower bound are coherent under the hypotheses stated. Independent finite diagnostics accompanying this report support the displayed finite algebra and model inequalities.

The remaining negative judgment is editorial and conceptual. The strongest theorem is still an engineered active input-output result with exact homothety about a supplied common laboratory origin, two labelled operating settings, quantitative footprint and boundary-mass priors, a bounded periodic presentation, a fixed protected aperture, and a known positive nonperiod-patch margin for uniform finite period decisions. The controller uses adaptively chosen real-valued nominal positions at accuracy tending to zero with the requested reconstruction error. The paper now counts their digital descriptions, which is welcome, but manufacture, metrology, homothety certification, travel and arithmetic time remain separate resources.

The stationary minimax problem also remains open. For a known uniform-disk law the new bracket is

\[
 c\nu^{-(s+1)/(s-2)}
 \le N^*_{\rm stat}(\nu)
 \le C\nu^{-(3s/2+1)/(s-2)}\log^2(C/\nu).
\]

The exponent gap `s/(2(s-2))` is much smaller than before, but it is still a genuine polynomial gap. The paper does not show that the rare-query upper exponent is necessary, nor does it identify the stationary minimax exponent.

In my judgment this is serious and potentially strong specialist-journal mathematics. Version 36 is materially stronger than v35, and the source package is now professionally qualified. It nevertheless remains below the exceptional naturality, breadth and conceptual transformation expected at the four journals named above. I would not recommend another open-ended revision cycle at that benchmark.

## 2. Frozen source and chronology

Both v36 revision names resolve to the same author head

`2559749a038fd2b5ec46d7cc74fdb4bd844b266a`

with repository tree

`46ad6437731b81ffe439c48fe9ede8b2fbc1d194`.

The head is based directly on the final v35 external-review commit

`985d798e172d38c0a9df2a068fe414b2fd13bcbc`,

which reviewed v35 author commit

`70c055e1ff090d58ecd61a5644e0fa62a7766f13`.

The source manifest pins the reviewed v35 manuscript tree

`80780f2590aec6d471985835b1b334774b23675f`,

the controlling v35 review tree

`2abfbf4ce4d99884c0107bf0caabcf5e70608584`,

and the retained v34 tree

`66f504938686e4b4920cdf250a92644bd1eae1d9`.

No A2 revision branch later than v36 existed when this report was frozen. The review branch starts directly from the v36 author head and adds files only under

`reviews/a2-v36-external-harsh-top4-rereview-2026-10-04/`.

No manuscript source, author revision branch, prior report, workflow, retained paper or unrelated project is modified.

The active primary consists of `main.tex`, `references.tex`, and nineteen core inputs. The genuinely new mathematical inputs relative to v35 are primarily:

- `core/00e_stationary_overview.tex`;
- `core/12_rare_stationary.tex`;
- `core/13_unknown_scale.tex`;
- the concluding update to `core/11_stationary_information.tex`;
- the expanded comparison and resource account.

I also inspected the response to referees, proof/history/literature ledgers, source pins, validator and diagnostic programs, exact-SHA workflow, hosted run, uploaded receipt and the complete v35 report.

## 3. Information model and theorem package

Each attempted command returns one bit. It is one exactly when a free start has a first collision on the prescribed unreflected segment. A solid start and a free miss both return zero and both remain in the denominator.

At a stationary setting, a forward preparation at nominal center `x` starts at `x+Z` and uses an independently drawn compass displacement. Its reciprocal reverse preparation starts at `x+Z+a` and uses `-a`, with a fresh draw from the same nominal joint law. Only pooled means are observed; neither the launch realization, free-start status nor direction is returned.

The two labelled settings use physical footprints `A` and `rA`. The first footprint and the ratio `r` are unknown, while

\[
        1+g_*\le r\le R_*.
\]

Exact homothety about a fixed laboratory origin, uniform footprint geometry and a lower boundary-mass condition are supplied. The result reconstructs the first physical footprint and the ratio; it does not assign an artificial scale to a latent parameter body.

The new theorem package has three principal parts.

1. A rare-collision boundary query reconstructs the positivity supports with attempted-bit exponent
   \[
   \frac{(\gamma+3/2)s+1}{s-2},\qquad s=6+\beta.
   \]
2. An integrated pooled forward mean determines the ratio and footprint at an additional `O(nu^{-2})` attempted-bit and center cost, lower order in observations but not in center count.
3. An independent area normalization recovers the ratio from reciprocal differences alone, under a weaker separation condition.

The retained period theorem then acts on the recovered original bodies. Uniform finite decisions still use the known positive patch margin; exact and pointwise eventual statements remain separate.

## 4. Audit of the rare pooled boundary query

### 4.1 Coarse normal information

The fixed-accuracy preliminary stage reconstructs an expanded component well enough to produce an interior center, isolated radial brackets and a rational normal approximation satisfying

\[
        |\widehat n-n|\le 1/32
\]

throughout a fixed tubular neighborhood of each bracket. Positive rolling radius makes the normal map Lipschitz in that neighborhood. This stage has prior-dependent finite cost and is independent of the target accuracy.

The candidate set

\[
 V(\widehat n)=\left\{v\in\{\pm e_1,\pm e_2\}:
 \widehat n\cdot v\ge \max_w\widehat n\cdot w-\tfrac14\right\}
\]

contains every true maximizer of `n dot v`, including a tie, contains at most two vertices, and every selected vertex satisfies `n dot v>3/8`. I found the constants consistent.

### 4.2 Exterior zero

For a target in the isolated bracket neighborhood, shift the nominal center to `y+tv` for every selected candidate. If the target is exterior, choose a true maximizing vertex `v_*`, which is among the candidates. Support addition and symmetry of the compass imply

\[
 n\cdot(y+tv_*+z+utw)>p_C(n)
\]

for every launch offset `z`, every random compass direction `w`, and every point `u` on the attempted segment. Hence this candidate has collision probability exactly zero. The stronger design margin

\[
       D_*+2t+d_c<d_0
\]

excludes every other obstacle. The conjunction is therefore deterministically zero.

This is a genuine one-sided event, not an inference from a small difference of two noisy means.

### 4.3 Interior positive probability

At inner normal depth at least `e`, the boundary-mass lemma gives

\[
        \mathbb P\{y+Z\in C\}\ge c e^{\gamma+3/2}=:b_e.
\]

For every selected candidate the shifted start is free. On the independent events `y+Z in C` and compass direction `-v`, the attempted segment ends in `C`, so its pooled collision probability is at least `b_e/4`. A batch of order

\[
        b_e^{-1}\log(1/\varepsilon)
\]

therefore marks the candidate positive with the required confidence. A union bound over at most two candidates proves the proposition.

The statement is correctly local: the target lies in an isolated bracket neighborhood for one expanded component. It should not be paraphrased as a global membership oracle at arbitrary laboratory points.

### 4.4 Rate calculation

Take angular spacing

\[
 h\asymp\nu^{1/(s-2)},\qquad e\asymp h^s.
\]

There are `O(h^{-1} log(1/h))` boundary tests, each costing `O(e^{-(gamma+3/2)})` up to confidence logarithms. This gives

\[
 N_\nu\lesssim
 \nu^{-((\gamma+3/2)s+1)/(s-2)}
 \operatorname{polylog}(1/\nu,1/\delta).
\]

The exponent algebra is correct. For `gamma=0`, subtraction of the retained lower power gives exactly `s/(2(s-2))`.

## 5. Audit of the unknown-ratio inverse

### 5.1 Integrated collision width

For one displacement `a=tv`, the segment sweep `S_a(C)=C+[-a,0]` differs from `C` by a strip of length `t` over each nonempty transverse slice. Cavalieri's formula gives

\[
 |S_a(C)|-|C|
 =t\{p_C(v^\perp)+p_C(-v^\perp)\}.
\]

Under the stronger separation condition, the response support of one complete expanded component can be isolated in a bounded domain `E`. Tonelli's theorem and normalization of the unknown launch density then yield

\[
 \Phi_C:=\int_EF_1(x)\,dx
   =\frac t2\mathcal W(C),
\]

where `W(C)` is the sum of the two coordinate widths. No density symmetry, smoothness, upper bound or evaluation oracle is used.

It is important that this route uses the pooled forward mean `F_1`, in addition to the reciprocal differences used to reconstruct the positivity supports. The phrase “two reciprocal mean pairs suffice” is correct only if the two raw pooled means in each pair remain available; the difference alone does not contain this width integral.

### 5.2 Linear support inversion

Put

\[
 P_1=C+Q,\qquad P_2=C+rQ,\qquad D=P_2-P_1=(r-1)Q,
\]

and `a=(r-1)^{-1}`. Additivity of coordinate widths gives

\[
 a=\frac{\mathcal W(P_1)-2\Phi_C/t}{\mathcal W(D)},
 \quad r=1+a^{-1},
 \quad p_Q=a p_D,
 \quad p_C=p_{P_1}-a p_D.
\]

The denominator is uniformly bounded below by the scale gap and footprint inball. Support and scalar-measurement errors therefore propagate linearly, and the curvature margins make the recovered functions physical support functions. The formulas retain laboratory first harmonics and hence the physical placement.

### 5.3 Finite scalar measurement and control count

Sampling a nominal center uniformly in `E` and recording one pooled forward bit gives a bounded unbiased estimator of `Phi_C`. Hoeffding gives `O(m^{-2} log(1/epsilon))` attempts for error `m`. The finite-grid bias argument conditions on the launch displacement and counts cells meeting boundaries of convex bodies and segment sweeps; it does not require a density modulus or upper bound.

With `m=O(nu)`, this adds `O(nu^{-2})` attempts and nominal-center occurrences. The observation cost is lower order because the rare-query exponent exceeds two. The center count, however, contains a visible `nu^{-2}` term and should not be summarized solely by the one-dimensional boundary-query count. The manuscript's separate digital-description bound correctly includes it.

### 5.4 Area normalization from reciprocal differences alone

For the first-setting occupation component,

\[
 M_C=\int v_{1,C}=|C|.
\]

This follows directly from Fubini and normalization of the launch density. With `D=P_2-P_1` and `P_1=C+aD`, the mixed-area identity gives

\[
 M_C=|P_1|-2aV(P_1,D)+a^2|D|.
\]

The discriminant is

\[
 V(P_1,D)^2-|D|(|P_1|-M_C)=V(C,D)^2>0.
\]

The true value is the smaller root. The larger root would make the mixed area of the putative remainder with `D` negative and therefore cannot be physical. Uniform inballs give a discriminant margin and stable root selection.

The finite adjoint is also coherent. On a coarse dyadic domain `E`, let

\[
 w_E=(I-T^E)^{-1}\mathbf1.
\]

Symmetry of the killed compass operator gives

\[
       \int_E w_Eg_1=-\int_Ev_{1,C}=-M_C.
\]

The proposed weighted forward-minus-reverse bit is bounded, and the finite midpoint bias again follows from convex boundary-cell estimates uniformly over the unknown launch density.

## 6. Qualifications required in a journal version

### 6.1 Distinguish raw mean pairs from reciprocal differences

The direct width route requires `F_1`; the area route works from `(g_1,g_2)` alone. Abstract, introduction and theorem summaries should maintain this distinction exactly.

### 6.2 Keep the rare query local

Its deterministic exterior zero is proved for points in a protected tubular neighborhood of a bracket associated with one complete expanded component, under the stronger separation margin. It is not a global zero-test for arbitrary centers.

### 6.3 Define command-center counting consistently

The integrated measurement samples `O(nu^{-2})` center occurrences. The paper should use one term consistently for distinct spatial sites, randomized center commands, and repetitions, or give separate counts. The current formulas are mathematically usable but the prose occasionally permits these notions to blur.

### 6.4 State the strengthened design condition prominently

The faster query requires `2t+D_*<d_0`, stronger than the retained signed-query condition. This is an acceptable design choice, but every headline comparison of the two rates should display the changed admissible design class.

### 6.5 Self-calibration remains calibrated homothety

The ratio is learned. Exact homothety, setting labels, common origin, quantitative scale-gap bounds and physical realization of the settings are supplied. An unknown common unscaled offset produces the stated translation gauge. The term “self-calibration” should remain accompanied by these qualifications.

### 6.6 The upper and lower criteria differ in details

The upper theorem gives a deterministic high-probability attempt bound for an unknown density class and uses a fixed pooled compass design. The lower theorem concerns worst-case expected attempts on a fixed uniform-disk subclass and permits a more informative direction-controlled design. The comparison of powers is informative and legitimate, but it is not yet a matched minimax theorem.

## 7. Top-four significance assessment

The revision significantly improves the paper's mathematical balance. It no longer leaves the earlier large stationary upper exponent untouched, it learns a previously supplied scale ratio, and it closes the source-delivery defect. These are substantial achievements.

Nevertheless, the observation remains highly engineered. The scalar output alphabet does not by itself make the experiment a natural low-information billiard invariant: localization, setting selection, exact reciprocal joint laws, precise nominal positions and exact homothetic operation carry substantial control information. The paper now prices digital descriptions, but that does not price physical calibration or metrology.

The main engines after the sensor-specific reductions are established ones: active line search and smooth interpolation, inverse-probability detection of a rare informative event, Minkowski support addition, mixed-area algebra, killed Green identities and information-chain bounds. Their combination in this collision model is meaningful. I do not see, however, a new general inverse-geometric principle or rigidity theorem of the breadth expected at the four named journals.

The global conclusion also remains prior-relative. It assumes periodicity in a bounded presentation and uses a known positive patch margin for uniform finite period decisions. It does not infer crystallinity from an arbitrary configuration and does not derive rigidity from passive trajectories, count germs, marked lengths or spectra.

Finally, the stationary exponent remains unresolved. Closing the current polynomial gap, or proving a genuinely different natural-data rigidity theorem, would materially change the editorial assessment. Further refinements of the same apparatus-relative upper construction, by themselves, are unlikely to do so.

## 8. Literature positioning

The manuscript now compares the finite reconstruction to active smooth-boundary estimation, the rare-event principle to informative abstention, the nuisance-footprint problem to noisy convex-support estimation, and its digital control account to query-precision work. These are the right information categories.

The closest cited works do not contain the complete combination of pooled collision commands, one-sided geometric rare events, blind homothetic footprint separation and periodic reconstruction. Conversely, the manuscript correctly does not claim novelty for bisection, interpolation, binomial detection, Minkowski addition, mixed area, Green identities or entropy chain rules.

The literature audit is focused rather than exhaustive. No priority conclusion should be drawn from it.

## 9. Verification and source qualification

The exact-source workflow run `37180013120` is bound to the reviewed SHA. Exact checkout, finite diagnostics, contract tests, primary build, evidence binding and artifact upload all succeeded. The uploaded artifact is `11294633094`, digest

`sha256:afa632c67d3529454b3d218d3e5d7b37ee073310754aecd66fd07037b6a593ee`.

Its receipt records:

- 571,613 author finite diagnostics, with ordinary and optimized output identical;
- 66 validation-contract checks, again identical in ordinary and optimized modes;
- a warning-free 48-page primary;
- exact-commit qualification of `2559749a038fd2b5ec46d7cc74fdb4bd844b266a`;
- byte-identical preservation of all 33 reviewed v35 proof bodies and retention of all 117 reviewed labels.

The independent `verify_review.py` accompanying this report imports no author code and uses only the Python standard library. Ordinary and optimized executions are byte-identical. It performs 515,081 finite checks of candidate geometry, support-plane rare-event models, direct width calibration, mixed-area root selection, killed-adjoint mass identities, scale nesting, binary-range information bounds, signed-kernel moments, rate algebra and parallel-area controls.

Neither suite is a proof certificate or physical experiment. I did not re-prove every inherited theorem in the long A2 programme, and I did not perform an exhaustive literature search.

## 10. Final verdict

**Response to the v35 report:** substantively successful. The rate gap is substantially narrowed, the scale ratio is learned, control descriptions are charged, the stationary results lead the narrative, and source qualification is repaired.

**Mathematical audit:** no fatal counterexample found in the new v36 core; several scope and terminology qualifications should remain explicit.

**Editorial assessment:** strong specialist-journal potential after fresh human proof review and focused editing, but insufficient naturality, universality and conceptual reach for *Annals*, *Acta*, *Inventiones* or *JAMS*.

**Recommendation: reject at the requested top-four benchmark.**