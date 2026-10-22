# External top-four referee report on A2-DYN revision 30

**Manuscript:** Qian Qi, *Collision records, arithmetic, and raw local inversion in a triangular Lorentz gas*  
**Reviewed author branches:** `revision/a2-dyn-v30-referee-response-2026-10-07`, `revision/a2-dyn-v30-referee-copy-2026-10-07`  
**Reviewed commit:** `a8b400deb4c262bee2978aec3e19cc68aa5439e2`  
**Reviewed repository tree:** `e545ed9ce4ccc3744ddf4aa51f1515b3cfa8af46`  
**Frozen ordinary paper tree:** `7e47c9606ea21b79836319a7fa25d34bdf2a4b3c`  
**Active manuscript directory:** `papers/A2-DYN-v30-referee-response`  
**Last substantive report before this one:** `reviews/a2-dyn-v26-external-top4-review-2026-10-07/REFEREE_REPORT.md`  
**Controlling report commit / blob:** `20337e845157a833fe770687ea98f337788fa586` / `f75e48fa7276be7be654c61afe3cc276ba44d514`  
**Immediate qualified author baseline:** revision 29 at `18c3f14ff7e7275cd7a2955bcbe58bd89ada940f`  
**Qualified revision-29 ordinary paper tree:** `512509ff9d5a3141e3f53183bafe7fba61b4eebb`  
**Date:** 7 October 2026  
**Requested benchmark:** *Annals of Mathematics* / *Acta Mathematica* / *Inventiones Mathematicae* / *Journal of the AMS*  
**Status:** author-requested, AI-assisted referee-style assessment; not a commissioned journal report, an editorial decision, a formal proof certificate, or an independent human billiards-specialist report.

## 1. Recommendation

**Recommendation at the requested four-journal benchmark: reject in the present form.**

Revision 30, together with the previously unreviewed mathematical additions carried by revisions 27--29, is a genuine and substantial advance. The manuscript now proves a coherent mesoscopic conditioning theorem under the actual stationary physical law. Its strongest new conclusion is a functional one: the full physical displacement and collision-fluctuation path, conditioned on exact shrinking endpoint windows at deterministic physical time, converges to a nondegenerate Gaussian bridge. The same limit is obtained under four exact endpoint descriptions on one stationary probability space. The article also proves explicit denominators and selected conditional path laws for a concrete class of fixed multiple-time physical cylinder events.

The new work is not merely a restatement of the earlier functional central limit theorem. It supplies three ingredients that had previously been absent:

1. a joint collision-block Fourier estimate uniform in coalescing and zero-length blocks;
2. conditional tightness after division by a polynomially small endpoint probability;
3. a whole-path coupling on the actual stationary suspension, followed by transfer among the collision, deterministic-return, last-return, and physical endpoint events.

The cumulative revisions 27--29 also establish unsmoothed mesoscopic window probabilities, a signed-window estimate for the common raw correction, the correct equilibrium length biases, actual stationary denominators, and relative symmetric-difference and total-variation estimates between exact physical and return-based events.

I found no decisive counterexample in the six modules that have not previously received a substantive referee report:

- `core/57_unsmoothed_window_remainders.tex`;
- `core/58_relative_physical_windows.tex`;
- `core/59_stationary_collision_band.tex`;
- `core/60_stationary_physical_conditioning.tex`;
- `core/61_multiblock_bridge_windows.tex`;
- `core/62_stationary_window_bridges.tex`.

The endpoint-safe Fourier envelopes treat the three discrete coordinates without assigning a fictitious four-dimensional Lebesgue density to the original law. The projection arguments use a genuine four-dimensional change of variables and a moment truncation rather than taking an illegitimate trace of an integrated Fourier estimate. The stationary section-origin and current-collision biases are correctly distinguished. The multiblock spectral argument handles a short or zero block through adjacent projector differences, rather than through a false lower bound on the shortest block length. The conditional tightness proof pays the rare denominator both on the coarse Fourier grid and below the finest grid. The physical bridge transfer keeps all endpoint events and all path statistics on the same stationary suspension.

These are important accomplishments. In particular, the mesoscopic stationary conditioning pipeline is now substantially complete for the exact window class stated in Theorems T and U.

The negative recommendation nevertheless remains necessary. The manuscript continues to be titled and organized around raw local inversion and an original parameter-uniform raw mixed-density local limit problem which remains unproved. Revision 30 explicitly preserves, rather than closes, the following load-bearing obligations:

- the complete prescribed-return-count complementary Fourier integral;
- the pointwise common signed raw remainder, or an alternative estimate strong enough to replace it;
- the long-time inverse-coarea second-derivative budget at a collision cutoff proportional to the return count;
- the fixed-label and microscopic-time denominator;
- the relative replacement of the original microscopic physical event;
- the corresponding weighted raw theory for the actual downstream indicator class.

Theorem U concerns endpoint half-width `t^(21/50)` in physical coordinates. This is a shrinking standardized, but still mesoscopic, window. It does not prove a local limit at fixed lattice labels or a microscopic time interval. The signed common correction is controlled only after integration over sufficiently large unsmoothed windows; its essential supremum and its absolute integral are not controlled. The wider collision-clock Fourier ball is not a prescribed-return-count complementary estimate. The raw coarea derivative term remains untouched.

At the requested benchmark these distinctions are decisive. A strong and technically sophisticated conditional bridge theorem does not substitute for the still-open endpoint around which the article's title, raw extraction architecture, and final applications are organized.

The completed results could support a strong specialist paper after independent expert verification and substantial reorganization around the unconditional Gaussian, window, conditioning, and bridge theorems. That is a different editorial proposition from acceptance at the four-journal benchmark for the present raw-local-inversion manuscript.

## 2. Frozen source and revision chronology

The two named revision-30 author branches resolve to the same commit:

`a8b400deb4c262bee2978aec3e19cc68aa5439e2`.

The repository tree at that commit is:

`e545ed9ce4ccc3744ddf4aa51f1515b3cfa8af46`.

The frozen ordinary paper tree is:

`7e47c9606ea21b79836319a7fa25d34bdf2a4b3c`.

The chronology after the last substantive review requires care.

### 2.1. Revision 27

The branch `revision/a2-dyn-v27-referee-response-2026-10-07` ends at staging commit

`a92389dac67efc84364d651bd5614d830a59cd5f`.

That commit transported and checksum-validated ordinary paper tree

`ae335b52f013e3569e4a6b79b899cfc00e26b8e4`,

but was explicitly an immutable-object assembly step, not the final ordinary-source qualification of a complete author revision.

### 2.2. Revision 28

The branch `revision/a2-dyn-v28-referee-response-2026-10-07` points to

`b9b976cd93df7513018f03dea0df5ffe80920e01`.

It preserves the revision-27 ordinary source as a source snapshot. Its own commit message correctly states that the snapshot is source transport rather than mathematical or build qualification.

### 2.3. Revision 29

The first complete and qualified source containing the revision-27 window modules and the new stationary conditioning modules is revision 29 at

`18c3f14ff7e7275cd7a2955bcbe58bd89ada940f`,

with ordinary paper tree

`512509ff9d5a3141e3f53183bafe7fba61b4eebb`.

Its exact-source qualification run `37573116694` completed successfully.

### 2.4. Revision 30

Revision 30 continues from that qualified source. It preserves all sixty inherited core modules, all inherited Python files, all inherited labels, and the bibliography, and adds:

- `core/61_multiblock_bridge_windows.tex`;
- `core/62_stationary_window_bridges.tex`.

Because no substantive A2-DYN review branch after revision 26 was present before this review, the present report evaluates the full cumulative mathematical delta in modules 57--62 rather than treating revisions 27--29 as already refereed.

The present review branch starts directly from the reviewed revision-30 author commit and adds only this report under

`reviews/a2-dyn-v30-external-top4-review-2026-10-07/`.

No manuscript source, author branch, workflow, historical report, or unrelated repository path is modified.

## 3. Source qualification and verification boundary

The exact-source qualification completed successfully on both reviewed author branches:

- response branch run: `37588479611`;
- referee-copy branch run: `37588605973`.

For the response branch, the following steps completed successfully:

- exact checkout at the reviewed SHA;
- archive of the article, baseline, and controlling report;
- installation of native TeX and finite-check dependencies;
- verification of exact source identity;
- normal and optimized finite diagnostics;
- compilation of the complete article;
- rendering of the new proof pages and recording of PDF identity;
- upload of the exact-source qualification artifact.

The response artifact is:

- artifact ID: `11467298248`;
- name: `a2-dyn-v30-a8b400deb4c262bee2978aec3e19cc68aa5439e2`;
- digest: `sha256:6f66f1e843144c57928619d93aa281ac55cf954b6d4c455b8f62f0316297d5f8`.

The verifier records the qualified revision-29 baseline, all baseline and new source hashes, exact main-text edit replay, byte identity of inherited core and Python files, inclusion of all sixty-two modules, retention of all old labels, reference and environment checks, the controlling report blob, and the read-only workflow identity.

The new finite diagnostics test rational exponent identities, fixed residual block powers, trigonometric probe algebra, finite Gaussian bridge calculations, short-block noncommuting words including zero lengths, a bridge covariance determinant, and a common-selector total-variation identity. Negative controls reject, among other errors, identifying distinct short-block projections and attempting to pay the fine-grid denominator with only fourth moments.

These checks are meaningful execution and provenance evidence. They are not proofs of the continuum collision-space estimates, the high-order spectral word bounds, the stationary suspension coupling, the conditional tightness argument, or the full raw local limit theorem.

## 4. Scope of this mathematical review

I have not attempted to re-prove every inherited statement in the sixty-two-module article. The substantive scope is:

1. the six modules added since the last substantive review;
2. their interfaces with the already reviewed covariance, moment, damping, finite-extraction, and cutoff-transport results;
3. the exact source chronology and the claims made in the abstract, theorem synopsis, proof ledger, response to the referee, and publication metadata.

The review distinguishes three levels of conclusion throughout:

- a collision-clock statement on a deterministic number of collisions;
- an actual-return or stationary physical statement on shrinking mesoscopic windows;
- a microscopic raw mixed-density local limit statement.

The first two levels have advanced materially. The third remains open.

## 5. Unsmoothed windows and the common signed correction

### 5.1. Endpoint-safe interval envelopes

Module 57 proves the interval majorant and minorant needed for exact, unsmoothed windows. The endpoint treatment is not cosmetic because three coordinates of the record are discrete.

For an interval `I` and angular bandwidth `b`, the manuscript constructs continuous integrable functions satisfying:

```text
L_I <= 1_I <= U_I,
0 <= U_I <= 3,
supp(hat L_I), supp(hat U_I) subset [-b,b],
int U_I = |I| + 2*pi/b,
int L_I = |I| - 2*pi/b.
```

The proof includes either convention at an endpoint. This is necessary for the lattice coordinates and is handled explicitly.

For a box, the lower envelope is not taken to be the product of one-dimensional minorants, which could have the wrong sign. Instead the manuscript uses

```text
L_B = U_B - sum_i E_i product_{j != i} U_j,
E_i = U_i - L_i.
```

The telescoping argument gives the correct lower bound. The total excess is proportional to

```text
|B| sum_i (b_i h_i)^(-1).
```

I find this construction correct for the purpose used here.

### 5.2. Actual unsmoothed window probabilities

For a marked return law and a standardized four-dimensional box with half-widths `h_i`, the article proves an error of the form

```text
C |B| [ E_n(a) + M_a sum_i (b_i h_i)^(-1) ],
```

where the frequency box lies inside the already proved fixed-count region and

```text
E_n(a) = M_a n^(-3/280) sqrt(log(2+n)) + V_a n^(-9/175).
```

The argument integrates the entire bandlimited envelope against the actual mixed lattice-continuous law. It does not assign that law a density with respect to four-dimensional Lebesgue measure.

The comparison between the continuous Gaussian box mass and the mixed counting-times-Lebesgue Gaussian mass explicitly pays the lattice grid error in the first three coordinates. The conditions `b_i <= sqrt(n)/2` and `b_i h_i >= 1` ensure that the grid cells are smaller than the target intervals.

For the original section probability, taking standardized half-widths `n^(-1/25)` and the inherited isotropic bandwidth gives

```text
P{X_n in B} = 16 n^(-4/25) g_D(xi)
              [1 + O(n^(-11/1400) sqrt(log n))].
```

The exponent check is

```text
67/1400 - 1/25 = 11/1400.
```

This is an unsmoothed mesoscopic denominator. It is not a fixed-label local limit.

### 5.3. Averaged common raw correction

The same module proves, for any of the retained cutoffs, a bound of the form

```text
n^2 / m(B) * | integral_B R_chi dm | -> 0.
```

This is more than the cutoff-transport theorem of revision 26, which only controlled the difference `R_chi - R_psi`. Positivity and actual window probabilities now give information about one common correction itself.

The scope, however, is exactly as stated in the manuscript:

- the absolute value is outside the window integral;
- cancellation inside the window is retained;
- no essential-supremum estimate is obtained;
- no absolute integral of the correction is obtained;
- the window side lengths must exceed the reciprocal proved bandwidth.

In particular, the resolution condition cannot hold for a singleton lattice coordinate while the physical bandwidth is `o(sqrt(n))`. The theorem does not imply the microscopic raw local limit theorem.

I regard this distinction as mathematically essential and correctly maintained in revision 30.

## 6. Projection and section-start physical events

### 6.1. Three-dimensional projection from a four-dimensional estimate

Module 58 derives three-dimensional window probabilities for a linear projection of the four-coordinate return record.

The proof does not restrict a four-dimensional `L^1` Fourier estimate to a measure-zero frequency plane. Instead it:

1. extends the projection to a uniformly invertible four-dimensional matrix;
2. changes variables in a genuine four-dimensional frequency integral;
3. truncates the fourth output coordinate at `T=n^(1/400)`;
4. removes that truncation with a fixed sixty-fourth moment.

The main exponent ledger is:

```text
3/280 - 1/400 = 23/2800,
67/1400 - 1/25 = 11/1400,
64/400 - 3/25 = 1/25.
```

The slowest relevant rate in the section-start theorem is `n^(-11/1400) sqrt(log n)`.

The Gaussian envelope error in the discarded coordinate is integrated against Gaussian decay and therefore does not acquire an unnecessary factor `T`. This is an important and correct point.

### 6.2. Maximal return increments and the inverse return clock

The manuscript proves a deterministic return-window maximal estimate by a dyadic decomposition. For a window of `q` return iterates and fixed `p>2`, it obtains an `L^p` bound of order `q^(1/2)` for the maximum centered increment.

The proof uses:

- fixed-moment estimates for deterministic return intervals;
- a union estimate over aligned dyadic intervals;
- Minkowski summation over scales;
- return-map invariance for translated windows.

With a return-index window `q=t^(5/8)` and an error threshold `t^(3/8)`, the two principal probabilities have powers

```text
t^(p/2) q^(-p) = t^(-p/8),
q^(p/2) t^(-3p/8) = t^(-p/16).
```

The unfinished first and final return pieces are treated by the inherited exponential return tail. Independence is not used.

### 6.3. Relative physical event replacement under a section-start law

For exact three-dimensional endpoint windows of standardized half-width `t^(-1/25)`, hence physical half-width `t^(23/50)`, the manuscript proves:

```text
P(A_t) = 8 t^(-3/25) g_V(xi)
         [1 + O(t^(-11/1400) sqrt(log t))]
```

for the deterministic-return, last-return, and deterministic-physical-time events.

The coupling error is `t^(-1/8)` after normalization. Relative to the window half-width, the boundary-shell ratio is

```text
t^(-1/8) / t^(-1/25) = t^(-17/200),
```

which is faster than the Fourier-envelope error. The exceptional probability also remains negligible after division by the proved denominator.

The resulting symmetric-difference and conditional total-variation estimates are genuine relative event-replacement statements for this section-start mesoscopic class.

They are not statements about fixed lattice labels or the microscopic time event in the raw theorem.

## 7. Stationary collision windows and physical conditioning

### 7.1. Wider deterministic-collision Fourier band

Module 59 exploits a real structural distinction: a deterministic collision interval has no return-clock stopping error.

For bounded-BV initial collision data it proves an isotropic integrated Gaussian comparison through rescaled radius

```text
C m^(9/100),
```

or physical collision frequency `C m^(-41/100)`, with error

```text
C m^(-3/280) sqrt(log m).
```

On the central ball the inherited six-term expansion gives the slow exponent `3/280`.

On the outer collision annulus the proof uses fixed choices

```text
P = 40,
Q = 29,
delta = m^(-19/100)/4,
epsilon = m^(-50)/4.
```

The residual Taylor degree is 79, distinct from the spectral degree 29. The two analytic margins are

```text
1/2 - 9/100 - 2(19/100) = 3/100,
28(1/2 - 9/100) - 2(19/100)30 = 2/25.
```

The largest residual-moment exponent is `-1/25`. Its strict margin over the retained central rate is

```text
1/25 - 3/280 = 41/1400.
```

All nonsingleton block counts, including the connected `b=1` term, are retained. The expansion orders are fixed before `m` varies.

I find the exponent accounting coherent. The conclusion must nevertheless remain labeled a collision-clock theorem. It is not the missing prescribed-return-count complement.

### 7.2. Projected collision windows

Using the wider collision band, a true four-dimensional envelope argument, a fourth-coordinate truncation `T=m^(1/400)`, and a fixed 128th moment, the manuscript proves three-dimensional exact collision-window probabilities with standardized half-widths `m^(-2/25)`.

The relevant powers are:

```text
3/280 - 1/400 = 23/2800,
9/100 - 2/25 = 1/100,
128/400 - 6/25 = 2/25.
```

The resulting relative error is

```text
m^(-23/2800) sqrt(log m).
```

The bounded-BV initial density assumption includes the actual outgoing-collision marginal of the stationary flow.

### 7.3. Correct stationary length biases

Module 60 distinguishes two different equilibrium biases.

In the return suspension, the preceding section state has density proportional to the full return roof. That density need not be bounded-BV.

After decomposing an excursion into collision flights, the current outgoing collision has density

```text
sigma_R = tau_R / mean(tau_R)
```

relative to collision measure. This density has uniform supremum and BV bounds.

The proof uses the exact tower identity and the normalization

```text
mean(return roof) = mean(collision roof) / c_*.
```

The unbounded return-roof bias is transferred only through its exponential and `L^2` controls, not by silently assigning it collision-BV regularity.

This distinction is correct and necessary.

### 7.4. Four endpoint descriptions on one stationary space

The manuscript places the collision reference, deterministic-return reference, last completed return, and actual physical observation on one stationary suspension. It does not resample an independent section point.

A uniform coupling gives standardized error `O(t^(-1/8))` outside an arbitrarily high inverse-polynomial exceptional probability. Initial age, initial partial return, and final partial return are retained.

For endpoint half-width `t^(-2/25)` in standardized coordinates, or physical half-width `t^(21/50)`, all four events have denominator

```text
8 t^(-6/25) g_V(xi)
[1 + O(t^(-23/2800) sqrt(log t))].
```

The Gaussian shell error from the coupling has relative power

```text
t^(-1/8) / t^(-2/25) = t^(-9/200),
```

which is faster than the Fourier-envelope rate.

The conditional initial laws of the four events are close in total variation. This proves a meaningful stationary relative-replacement theorem for the exact mesoscopic windows stated in the paper.

## 8. Joint collision blocks and shrinking endpoint windows

Module 61 is the main new analytic input of revision 30.

### 8.1. Uniformity in block boundaries

Fix a finite number of consecutive collision blocks with lengths `m_l`, where some lengths may be zero and the boundaries may coalesce. The block frequencies are allowed to grow as `m^(1/200)`. The endpoint frequency is integrated through radius `C m^(9/100)`.

The theorem proves an integrated comparison between the actual chronological product and the Gaussian block product with error

```text
C m^(-3/280) sqrt(log m).
```

The constants may depend on the fixed number of blocks but not on their lengths or locations.

This is the correct uniformity for the later conditional tightness argument.

### 8.2. Short and zero blocks

A common error in a multiblock spectral proof would be to claim exponential decay from the shortest block. Revision 30 does not do this.

For a zero power, the complementary part is interpreted as

```text
N(z)^0 = I - Pi(z).
```

The term containing only complementary factors is controlled by the total collision length, since the positive block lengths sum to `m`.

Every other nonprincipal term contains an adjacent mixed factor. The manuscript rewrites, for example,

```text
N(z)^l Pi(w) = N(z)^l [Pi(w) - Pi(z)].
```

The reversed ordering is treated similarly. The projector difference provides the small factor even when `l=0`.

This resolves the zero-length-block interface without assuming a positive lower bound on any `m_l/m`.

### 8.3. Principal term and observable smoothing

On the small central ball, the product of principal eigenvalues gives the weighted Gaussian logarithm. Mixed spectral terms, the initial-density smoothing, the observable smoothing, and the covariance replacement are controlled with the same six power budgets as in the deterministic-collision theorem.

The allowed path frequencies are smaller than or equal to `m^(1/200)`, so they do not enlarge the slow central exponent.

### 8.4. High-order annular argument

On the outer collision annulus, every segment frequency is comparable to the endpoint frequency because

```text
|v| >= 2 m^(1/200),
max_l |u_l| <= m^(1/200).
```

Consequently

```text
sum_l m_l |v+u_l|^2 / m >= c |v|^2.
```

The corrected residual monomials form chronological words with a fixed number of smooth multipliers. The power lengths in each block sum to that block's length, and the total is `m`. Thus the product retains genuine Gaussian damping in the integrated endpoint frequency.

The fixed orders remain `P=40`, `Q=29`. The largest residual-moment power remains `-1/25`, with margin `41/1400` over `3/280`.

I find the argument internally coherent, subject to independent specialist checking of the inherited anisotropic collision norms and the fixed high-order multiplier constants.

### 8.5. Oscillatory endpoint conditioning

The block characteristic function is then conditioned on an exact three-dimensional shrinking endpoint window.

Because the numerator is complex, positivity cannot directly sandwich it between endpoint majorants and minorants. The manuscript instead uses the modulus-one bound on the oscillatory weight:

```text
|E[W(1_B - U_B)]| <= E[U_B - 1_B] <= E[U_B - L_B].
```

The same domination is used on the Gaussian side. This correctly reduces the oscillatory envelope replacement to the already controlled unweighted excess.

The fourth output coordinate is removed by a fixed 128th moment, and the true denominator is supplied by the projected collision-window theorem.

The resulting conditional block characteristic differs from the Gaussian-bridge increment formula by

```text
C m^(-23/2800) sqrt(log m),
```

uniformly in coalescing block boundaries and in test frequencies through `m^(1/200)`.

The center replacement inside the endpoint box costs

```text
m^(-2/25) m^(1/200) = m^(-3/40),
```

which is faster than the displayed Fourier rate.

## 9. Conditional collision and physical bridge limits

### 9.1. Finite-dimensional distributions

For a fixed finite list of times, the uniform block characteristic theorem gives the Gaussian bridge increment law. Rounding a fixed time to a collision index changes the normalized path by `O(m^(-1/2))`, since the collision observable is bounded.

This part is standard once the multiblock theorem is available.

### 9.2. Conditional increment tails from trigonometric probes

The manuscript does not infer tightness from finite-dimensional convergence.

It introduces a nonnegative trigonometric tail test

```text
F_p(x) = integral_0^1 (1 - cos(ux))^p du,
```

which is bounded below away from zero for `|x| >= 1` and above by `C|x|^(2p)`.

With `p=4`, the conditional block characteristic estimate gives, for an increment of relative length `Delta`,

```text
P{|increment| > a | endpoint window}
<= C a^(-8) Delta^4 + C epsilon_m.
```

The Gaussian bridge increment has eighth moment `O(Delta^4)`, including the bounded mean term.

### 9.3. Coarse dyadic grid

The proof uses levels through

```text
J_m = floor(log_2(m)/200)
```

and thresholds `a_j = epsilon 2^(-j/8)`.

The largest trigonometric probe frequency is of order

```text
m^(1/1600),
```

strictly inside the permitted `m^(1/200)` budget.

After the union over all adjacent increments, the Gaussian part is summable and the Fourier error becomes

```text
2^(J_m) epsilon_m
= O(m^(-9/2800) sqrt(log m)),
```

using

```text
23/2800 - 1/200 = 9/2800.
```

### 9.4. Motion below the finest grid

The motion within the finest cells is treated separately with a fixed 128th maximal moment.

There are `2^(J_m)` cells. The unconditional normalized 128th moment in one cell is `O(2^(-64 J_m))`. After the union over cells and division by the endpoint probability `m^(-6/25)`, the exponent is

```text
63/200 - 6/25 = 3/40.
```

Thus the fine-grid conditional probability tends to zero. This is the correct place to pay the rare denominator. Fourth moments would not suffice, and the manuscript's negative diagnostic correctly records this.

The coarse and fine estimates establish conditional tightness in continuous path space.

### 9.5. Uniformity in the covariance and endpoint

The proof of uniform bounded-Lipschitz convergence uses a compact-parameter subsequence argument. The endpoint centers remain bounded and the covariance matrices lie in a compact set of uniformly positive matrices. The comparison bridge laws vary continuously under a common Brownian coupling.

I find this uniformity argument adequate.

## 10. Whole physical path on the stationary suspension

### 10.1. Pathwise physical-to-collision coupling

The manuscript upgrades the one-time coupling to a supremum-norm comparison of the physical polygon and the deterministic collision polygon.

It applies the stationary one-time coupling at the integer physical times from `t^(1/4)` to `t` and at the terminal time. A union bound with a sufficiently high fixed moment gives an arbitrarily high inverse-polynomial exceptional probability.

For earlier times, deterministic bounded-speed and positive-minimum-flight estimates give an error smaller than the common `t^(3/8)` unnormalized threshold.

The deterministic collision index at physical grid time `k/t` differs by only a bounded amount from the reference index for physical length `k`. Between neighboring grid points both paths make only a uniformly bounded unnormalized increment.

After division by `sqrt(t)`, the pathwise error is `O(t^(-1/8))`.

Under endpoint conditioning, the exceptional probability is divided by the already proved probability `t^(-6/25)` and remains negligible.

### 10.2. Stationary physical bridge

Under the collision endpoint event, the collision bridge theorem applies with the actual stationary outgoing-collision density

```text
sigma_R = tau_R / mean(tau_R).
```

The covariance is

```text
C_t = (m/t) B_R Gamma_R B_R^T = V_R + O(t^(-1)).
```

The physical path replaces the collision polygon through the whole-path coupling.

The other endpoint events are transferred by the total-variation comparison already proved in Theorem T. Pushforward under the same physical-path map cannot increase total variation.

The result is therefore a genuine functional conditional limit for all four exact endpoint descriptions:

```text
physical path | endpoint event
    -> Gaussian bridge with endpoint xi and covariance V_R.
```

The return-conditioned path remains the actual physical path on the original stationary suspension. The section origin and elapsed age are not resampled.

## 11. Path-weighted and multiple-time selectors

### 11.1. Fixed bounded continuous path weights

For a fixed bounded continuous nonnegative path functional `F`, uniform weak convergence and uniform tightness give

```text
E[F(path) 1_A]
= endpoint mass * [E F(bridge) + o(1)].
```

If the bridge expectation has a positive uniform lower bound, the corresponding reweighted conditional path law converges to the `F`-weighted bridge law.

This is a valid theorem for fixed `F`. The manuscript correctly does not claim a uniform result for arbitrary changing rare path weights.

### 11.2. Concrete multiple-time physical cylinder events

For fixed distinct interior times and fixed bounded boxes with nonempty interiors, the exact event is formed from the actual physical observations at those times.

The denominator is

```text
8 t^(-6/25) g_V(xi) b_R(xi; s, D) [1+o(1)],
```

where `b_R` is the finite-dimensional Gaussian bridge box probability. Its covariance blocks are

```text
[min(s_l,s_k) - s_l s_k] V_R.
```

The scalar bridge covariance at distinct interior times is positive definite, and uniform ellipticity of `V_R` gives uniform positivity after tensoring with the spatial covariance. Each fixed box contains a compact subbox of its interior, so the Gaussian density yields a positive uniform lower bound for bounded endpoints.

The cylinder boundary has zero probability under the limiting bridge. The actual physical observations differ from the polygon values by `O(t^(-1/2))`, so enlargement and contraction of the fixed boxes transfers the weak convergence to the exact indicator.

Intersecting two endpoint events with the same cylinder event can only reduce their symmetric difference. Dividing by the newly proved cylinder denominator preserves the conditional total-variation rate.

This closes the additional-denominator assumption for a concrete and nontrivial class of multiple-time selectors.

## 12. What revisions 27--30 close relative to the revision-26 report

The cumulative revisions close or substantially advance several items from the last report.

### 12.1. Mesoscopic denominators

The article now proves actual unsmoothed denominators at:

- a prescribed return count under the section law;
- a deterministic physical time under the section-start law;
- a deterministic physical time under the true stationary law.

These are not merely smoothed probabilities.

### 12.2. Relative physical-event replacement

For the stated mesoscopic endpoint windows, physical, last-return, deterministic-return, and collision-reference events are compared on one probability space. Their relative symmetric differences and conditional total-variation distances tend to zero at explicit rates.

Thus the earlier criticism that only an absolute clock error was available no longer applies to this window class.

### 12.3. Conditional functional limit

Revision 30 identifies the common conditioned path law as a Gaussian bridge and proves conditional tightness. This is a substantive theorem not contained in the preceding event-comparison statements.

### 12.4. Concrete path-selector denominators

Fixed multiple-time physical box selectors now have explicit positive denominators and selected bridge limits. The additional weighted denominator is proved rather than assumed for this class.

### 12.5. Information about the common raw correction

The common correction is now controlled after signed integration over sufficiently resolved unsmoothed windows. This is a genuine advance beyond cutoff transport.

It is still not a pointwise raw correction estimate.

## 13. Remaining obstruction I: the full prescribed-return complement

The deterministic collision theorem reaches a full isotropic rescaled radius `m^(9/100)`. This is valuable for stationary window probabilities because it avoids return stopping.

It does not prove the corresponding statement for the actual prescribed return record.

The raw return-count problem still needs a fixed-count complementary estimate covering, in one compatible argument:

- the balanced small-frequency directions outside the retained isotropic, box, and adaptive-cross domains;
- compact nonzero lattice and collision-count torus frequencies;
- all relevant peripheral return phases;
- growing roof frequencies;
- the far roof-frequency tail;
- strict splicing of these regimes with the actual constants and weight losses.

The multiblock theorem also lives on deterministic collision intervals. It is an input to the bridge theorem, not a substitute for the missing prescribed-return transform.

The source manifest and publication metadata correctly continue to record that the full fixed-return complementary integral and the full raw LLT are not proved.

## 14. Remaining obstruction II: the pointwise common signed raw remainder

Revision 26 established that changing among three cutoffs changes the combined signed correction by a vanishing amount.

Module 57 now shows that one common correction has a vanishing signed average over sufficiently large unsmoothed windows.

What the raw density theorem requires is stronger. A representative target remains

```text
n^2 ||R_chi^{a,L_n}||_{L^infinity(W_n)} -> 0,
```

or an alternative statement that directly yields the same pointwise raw conclusion.

The current signed-window estimate permits cancellation inside the window. It cannot be localized to a singleton lattice coordinate or a microscopic time interval at the available bandwidth.

Nor does it imply either of the isolated absolute estimates:

- smallness of the extracted-edge correction;
- smallness of the absolute complementary residual integral.

The manuscript is correct not to make those inferences.

This common pointwise remainder is now a cleaner blocker than before: cutoff transport has shown that the issue is intrinsic rather than an artifact of which low-frequency kernel is chosen.

## 15. Remaining obstruction III: long-time raw-density preparation

The exact finite-count extraction proves constructible power-logarithm subtraction and an absolutely invertible residual for each fixed finite packet.

The full theorem still requires a uniform estimate at a linear count cutoff. In the notation of the manuscript, the unresolved quantity includes

```text
A_2(n,L_n,R,w)
= sum_ell || partial_t^2 r_{n,R}^{w,L_n}(ell,.) ||_1,
L_n proportional to n.
```

A useful bound must control the growth of:

- regular and singular cells;
- prepared exponents and their distance from critical thresholds;
- germ radii;
- power-log coefficients and logarithmic degrees;
- critical-value coalescence;
- inverse-coarea Jacobians;
- regular-interval derivative integrals;
- the dependence on the parameter, the count, and the actual weight.

The new fixed high moments, collision bands, and conditional bridge arguments do not estimate these inverse-coarea derivatives. They cannot replace the long-time raw preparation theorem.

An alternative direct estimate that bypasses `A_2` would be acceptable, but no such replacement is proved in revision 30.

## 16. Remaining obstruction IV: the microscopic physical event

Theorems T and U use standardized endpoint half-width `t^(-2/25)`, hence physical half-width

```text
t^(1/2-2/25) = t^(21/50).
```

The section-start result uses an even larger physical half-width `t^(23/50)`.

These windows shrink on the central-limit scale and are mathematically nontrivial. They are nevertheless far from:

- fixed lattice labels;
- a microscopic or fixed-width time window;
- the exact denominator required by the original raw mixed-density application.

The concrete cylinder selectors add fixed interior path restrictions, but the terminal endpoint remains mesoscopic.

The original microscopic application still needs:

1. a weighted raw local asymptotic for the actual indicator class;
2. the corresponding exact denominator;
3. a relative comparison of completed-return and physical events at that denominator scale;
4. compatibility with the full prescribed-return Fourier complement and the common pointwise remainder.

Revision 30 explicitly leaves these tasks open.

## 17. Remaining obstruction V: breadth at the requested benchmark

Even if the completed mesoscopic results are accepted as correct, the article remains an exceptionally long and highly system-specific construction for one triangular Lorentz family.

For a four-journal paper, one would normally expect at least one of the following:

- completion of the advertised raw endpoint;
- a general principle extracted and proved for a broad class of hyperbolic systems, with this billiard family as a substantial application;
- several genuinely different applications demonstrating that the compensation, fixed-order damping, adaptive Fourier geometry, and conditional bridge mechanism form a reusable theory.

The current article contains many useful mechanisms, but their general scope is not yet isolated at that level. The combination of an unproved organizing endpoint and a single-family realization remains an editorial obstacle at the requested benchmark.

## 18. Required work before a further top-four submission

A further submission pursuing the same raw endpoint should, in my view, proceed in the following order.

### 18.1. Complete the prescribed-return Fourier complement

The first task is a single quantitative theorem covering all remaining fixed-count frequency regimes, including balanced directions, compact nonzero torus frequencies, peripheral return phases, and growing and far roof frequencies.

The deterministic-collision band should be used as an input, but the return-clock loss and the actual return record must be handled rather than bypassed.

### 18.2. Prove the common pointwise raw correction

The cutoff-transport and signed-window theorems suggest that a direct estimate of the combined correction may be sharper than separate absolute edge and residual bounds.

A successful theorem must nevertheless operate at the microscopic raw scale. A signed average over a mesoscopic box is insufficient.

### 18.3. Close or bypass the long-time coarea derivative budget

Either prove a usable uniform `A_2` estimate at `L_n proportional to n`, with all geometric constants tracked, or replace the far-roof integration-by-parts mechanism by another argument that yields the required raw tail.

### 18.4. Establish the microscopic weighted denominator and event replacement

The actual downstream indicator class must be shown to lie in the intersection of the Fourier and finite-record admissibility classes needed by the proof, or a new interface must be constructed.

The exact microscopic denominator and its relative physical-event replacement must then be proved on the same probability space.

### 18.5. Obtain independent specialist verification

Before another four-journal review, the following interfaces should receive independent scrutiny from a billiards / anisotropic-operator specialist:

- the Demers--Zhang common-space identifications and multiplier bounds;
- the fixed high-order words with up to eighty smooth insertions;
- the multiblock principal/complementary decomposition with zero blocks;
- the stationary suspension normalization and physical-clock coupling;
- the finite-record constructible extraction near collision singularities;
- the eventual long-time raw-density estimate.

The repository diagnostics are not a substitute for this review.

## 19. Presentation and organization comments

1. The chronology should continue to distinguish the revision-27 staging commit, the revision-28 snapshot, the qualified revision-29 source, and the present revision-30 source.

2. The abstract now correctly states that the pointwise common remainder, full complement, long-time preparation, and microscopic exact-event application remain open. This boundary must remain prominent.

3. Theorem U should always be described as a stationary mesoscopic endpoint-window bridge theorem. The physical half-width `t^(21/50)` should remain visible whenever the result is summarized.

4. The deterministic-collision Fourier ball should not be described as a prescribed-return-count complement. Revision 30 currently observes this distinction.

5. The common signed-window estimate should always display that the absolute value is outside the integral.

6. The manuscript should keep the three notions separate: cutoff-transition smallness, signed-window smallness of one correction, and pointwise raw smallness.

7. The fixed number of blocks and fixed expansion orders should remain explicit in the multiblock theorem. No uniformity in growing block number or growing residual degree has been proved.

8. In the tightness proof, the two denominator payments should remain separately visible: the accumulated Fourier error above the finest mesh and the 128th-moment estimate below it.

9. The distinction between the unbounded section-origin roof bias and the bounded-BV outgoing-collision bias is essential and should not be compressed into a generic phrase such as “stationary density.”

10. The cylinder-selector theorem should retain “fixed distinct interior times” and “fixed bounded boxes with nonempty interiors.” Arbitrary changing rare selectors are outside its scope.

11. The article now has a very large main-theorem list. A journal version would benefit from grouping the results into a smaller number of conceptual theorems and moving provenance and source-ledger material out of the mathematical narrative.

12. The raw endpoint should have one explicit ledger listing exactly which terms in the final inversion identity are proved small and which remain open. The current proof ledger is helpful but should be tied directly to the final displayed raw formula.

13. Execution evidence, source qualification, and mathematical proof status should continue to be separated. The present metadata does this correctly.

## 20. Correctness assessment

Subject to the inherited collision-space and geometric inputs, I regard the new chain as mathematically plausible and substantially more complete than the version reviewed at revision 26.

In particular:

- the interval and box envelopes are used correctly;
- the mixed lattice-continuous Gaussian normalization is tracked;
- the projection does not use an invalid Fourier trace;
- the stationary length biases are distinguished correctly;
- the collision endpoint denominator pays the discarded coordinate by a sufficiently high fixed moment;
- the multiblock proof handles zero lengths by projection differences;
- the annular damping uses the total collision length;
- the oscillatory envelope replacement uses the modulus-one bound rather than positivity of the numerator;
- the conditional tightness pays the rare endpoint probability;
- the physical path is coupled on the same stationary suspension;
- the fixed cylinder denominator has a genuine uniform Gaussian lower bound.

I did not locate a decisive counterexample or a clear algebraic inconsistency in modules 57--62.

This assessment is not a formal verification. The high-order continuum spectral estimates and the physical-clock coupling are sufficiently intricate that independent expert checking remains necessary.

## 21. Final editorial assessment

Revision 30 closes a real mathematical gap: it upgrades stationary endpoint event comparison to a conditioned functional Gaussian-bridge limit and proves explicit denominators for a concrete multiple-time path class.

It also consolidates the cumulative revisions 27--29 into a coherent mesoscopic conditioning theory:

- actual unsmoothed windows;
- signed-window control of the common correction;
- section-start event replacement;
- equilibrium collision and return biases;
- stationary physical denominators;
- conditional total-variation comparison;
- collision and physical Gaussian bridges;
- concrete path-selector denominators.

These results are substantial and deserve serious specialist attention.

They do not, however, prove the full raw mixed-density local limit theorem named and architected by the manuscript. The prescribed-return complement, pointwise common remainder, long-time coarea derivative control, and microscopic exact physical-event application remain central mathematical theorems rather than peripheral cleanup.

For that reason my recommendation at the requested four-journal benchmark remains:

**reject in the present form.**

A future top-four submission should return only after the raw endpoint is genuinely closed or after the completed mechanisms have been extracted into a broad theorem with multiple substantive applications.