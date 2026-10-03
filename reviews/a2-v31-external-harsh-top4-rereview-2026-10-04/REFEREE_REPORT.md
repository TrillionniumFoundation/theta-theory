# External top-four referee report on A2 v31

**Manuscript:** Qian Qi, *Scalar collision laws and recognition of periodic dispersing billiards*  
**Reviewed revision:** `revision/a2-v31-reciprocal-command-reconstruction-2026-10-04`  
**Equivalent referee-copy alias:** `revision/a2-v31-referee-copy-2026-10-04`  
**Reviewed commit:** `27d109b0eba6a03d453834ef9da9418446ac637d`  
**Reviewed repository tree:** `ff918d19db00fc3aea087a02e6b4481e197c2767`  
**Immediate v30 baseline:** `c01118b11779b6161cc34e311f840e5ab36a019c`  
**Controlling preceding external report:** `6444b57768313ac68978b3ee04a428b4832ccb6e`  
**Manuscript directory:** `papers/A2-v31-reciprocal-command-reconstruction`  
**Date:** 4 October 2026  
**Requested benchmark:** *Annals of Mathematics* / *Acta Mathematica* / *Inventiones Mathematicae* / *Journal of the AMS*  
**Status:** author-requested, AI-assisted referee-style assessment; not a journal decision or a formal proof certificate.

## 1. Recommendation

**Recommendation at the requested four-journal benchmark: reject.**

Version 31 is a genuine mathematical extension of the scalar-collision programme. It does not merely restate the deterministic finite-chain inverse of v29 or the almost-sure cone-stopping theorem of v30. The new section proves that a reciprocal randomized displacement law can recover the obstacle occupation even when no direction has almost-sure positive progress. For centered bounded increments it obtains the explicit mean-exit estimate

\[
\sup_x \mathbb E_x\tau\le
H=\frac{(D+b)^2}{v_*},
\]

a geometric survival tail, monotone Bellman reconstruction, and the physical stability estimate

\[
\|u-\widetilde u\|_\infty
\le H\|(T_\rho-I)(u-\widetilde u)\|_\infty
\]

for two admissible occupations with different unknown zero sets. The paper also gives a fixed-aperture localization and a four-direction finite grid realization with pooled one-bit means and rational interval enclosures.

I found no fatal counterexample to the new mean-exit argument, the different-zero-set comparison, the extension to every nontrivial bounded displacement law, the fixed-aperture killing, or the four-direction finite experiment. I also audited the principal v30 ingredients that entered without an intervening external report: the coupled position/time/angle calibration estimate and the threshold–cluster–hull–smoothing reconstruction. On the hypotheses stated in the manuscript, those arguments are coherent. The negative recommendation is therefore not based on a known false central theorem.

The remaining issue is the level and naturality of the information model. The output of each attempt is one bit, but the experiment is allowed an increasingly fine two-dimensional family of localized spatial commands, a prescribed displacement distribution, the exactly translated reciprocal reverse preparation, calibrated position/time/angle coupling, and the nonstandard convention that attempted solid starts remain in the denominator as zero outcomes. Exact data are two input-output functionals on spatial densities, not two numbers and not an ordinary passive billiard invariant.

The inverse mechanism is mathematically attractive, but its general engines are classical: endpoint cancellation produces a Markov difference, bounded-component geometry supplies finite mean exit, stopped martingales and killed Green operators yield the resolvent bound, and monotone value iteration reconstructs the nonnegative solution. The global table theorem then invokes the retained active-set reconstruction and period-locking machinery under a known positive patch margin and a bounded periodic presentation. In my judgment the combination is serious specialist-journal mathematics, but it does not reach the exceptional conceptual breadth, naturality, or transformation of the subject expected at the four journals named above.

A focused specialist submission centered on the reciprocal scalar inverse and its constructive finite realization could be strong after a fresh human proof review and substantial compression of the cumulative programme. I would not recommend another open-ended revision cycle at the requested top-four benchmark.

## 2. Frozen source and chronology

The two v31 branch names listed above resolve to the same author head

`27d109b0eba6a03d453834ef9da9418446ac637d`

with repository tree

`ff918d19db00fc3aea087a02e6b4481e197c2767`.

Its parent is the complete v30 author revision

`c01118b11779b6161cc34e311f840e5ab36a019c`.

Version 30 in turn follows the latest retrieved external report

`6444b57768313ac68978b3ee04a428b4832ccb6e`,

which reviewed v29 author commit

`b81664d3961cdbad58563f37dcaed03288de199e`.

No separate external v30 review branch was present when this report was frozen. Accordingly, the present rereview covers both the v31 mean-exit extension and the v30 calibration/constructive additions on which it depends.

The complete v30 manuscript is preserved under

`papers/A2-v31-reciprocal-command-reconstruction/retained/v30`

with native tree

`1a6f8f32ec62aec586883e67753b3a72895f875c`.

The nine inherited active core files have retained tree

`315c9c3ec006eadfc66cff72acf9855af29685be`

and are pinned byte-for-byte. The current core tree, including the three new v31 inputs, is

`aa9026847310ecd9205fe631b5ed85aa141b70ed`.

The active mathematical inputs are:

- `core/00_overview.tex`;
- `core/00a_reciprocal_overview.tex`;
- `core/01_reversal.tex`;
- `core/02_local_acquisition.tex`;
- `core/03_periods.tex`;
- `core/04_finite_experiment.tex`;
- `core/05_comparison.tex`;
- `core/06_calibrated_launches.tex`;
- `core/07_constructive_patch.tex`;
- `core/08_hit_functionals.tex`;
- `core/09_mean_exit_inverse.tex`;
- `core/10_pooled_finite_experiment.tex`.

I also inspected the response, proof and literature ledgers, source pins, retained v30 tree, finite reference implementation, local validation summary, exact-SHA workflow, hosted workflow result, and the complete v29 referee report.

The review branch starts directly from the frozen v31 author head and adds files only below

`reviews/a2-v31-external-harsh-top4-rereview-2026-10-04/`.

No manuscript source, author workflow, retained volume, previous report, or unrelated paper is modified.

## 3. Observation model and theorem package

For a displacement \(a\), a commanded attempt starts at \(q\) and records one precisely when the unreflected segment \([q,q+a]\) has a first collision. A start inside the unknown solid and a free miss both produce zero, and both remain in the denominator. If the forward command has density \(f\), the reverse command uses the translated start \(q+a\) and displacement \(-a\).

The retained pointwise identity is

\[
B_a(q)-B_{-a}(q+a)
=\mathbf 1_{\mathcal O}(q+a)-\mathbf 1_{\mathcal O}(q).
\]

For a prescribed displacement law \(\rho\), the reciprocal randomized protocols therefore supply

\[
P_\rho^+(f)-P_\rho^-(f)
=\int f(x)(T_\rho-I)\chi(x)\,dx,
\qquad
T_\rho w(x)=\int w(x+a)\rho(da).
\]

Localized kernel commands yield the forcing

\[
g_\sigma=(T_\rho-I)u_\sigma,
\qquad
u_\sigma=\kappa_\sigma*\chi.
\]

The new question is whether this Markov difference determines \(u_\sigma\) without a supplied zero and without an almost-sure drift cone. The answer is affirmative on the diameter/separation class.

The global finite theorem then specializes to

\[
\rho_\square=\tfrac14
(\delta_{te_1}+\delta_{-te_1}+\delta_{te_2}+\delta_{-te_2}),
\]

implements \(T_{\rho_\square}\) by four exact grid shifts, reconstructs occupation on a fixed enlarged aperture, thresholds and clusters the occupied grid, takes convex hulls, smooths their support functions, and applies the retained finite patch and rational period tests.

The resulting headline bounds are:

\[
\sigma\asymp\nu^{3/2},\qquad
O(\nu^{-3})\ \text{spatial centers},
\]

\[
O\!\left(\nu^{-3}\log\frac{C}{\nu\delta}\right)
\ \text{one-bit attempts},
\qquad
O(\nu^{-6})
\ \text{arithmetic and fixed-kernel evaluations}.
\]

These are sufficient conditional upper bounds with constants depending on all stated priors, including the known patch margin \(\eta\).

## 4. Correctness audit of the reciprocal forcing

The randomized identity is a direct average of the exact fixed-displacement reversal law. The reverse experiment must use the same joint law for \((q,a)\) and start at \(q+a\) with displacement \(-a\). Matching only the marginal direction law or independently resampling an unrelated reverse start would not give the same formula.

The manuscript keeps this coupling explicit. It also keeps the attempted-solid-start normalization explicit. Both are logically essential, not implementation details.

For translated kernel commands, convolution commutes with translation, so the observed mean imbalance is indeed \((T_\rho-I)u_\sigma\). No direction-resolved mean is required after pooling, provided the controller implements the prescribed joint randomization.

I found no defect in this passage from the fixed reversal identity to the pooled Markov forcing.

## 5. Correctness audit of the mean-exit inverse

### 5.1 Centered mean-exit bound

Assume bounded increments, zero mean and second moment \(s_2\ge v_*\). Until the first zero of \(u\), the walk remains inside one containing set because one step is shorter than the separation between distinct sets. If that set has diameter at most \(D\), then at the bounded stopping time \(S=\tau\wedge n\),

\[
|X_S-x|\le D+b.
\]

The process

\[
|X_n-x|^2-ns_2
\]

is a martingale. Bounded optional stopping gives

\[
s_2\,\mathbb E_x(\tau\wedge n)
=\mathbb E_x|X_{\tau\wedge n}-x|^2
\le(D+b)^2.
\]

Monotone convergence yields the claimed expectation bound. Markov's inequality at a block length at least \(2H\), followed by the Markov property, gives the geometric survival tail.

This argument is correct and notably does not require nonsingular covariance. A two-site symmetric walk or a rank-one centered law is allowed.

### 5.2 Bellman reconstruction

With \(g=(T_\rho-I)u\), the iteration

\[
V_0=0,\qquad
V_{n+1}=\max(0,T_\rho V_n-g)
\]

satisfies \(0\le V_n\le V_{n+1}\le u\). If \(e_n=u-V_n\), then on the positive set

\[
e_{n+1}\le T_\rho e_n.
\]

Iteration until the first zero gives

\[
0\le e_n(x)
\le\mathbb E_x\!\left[u(X_n)\mathbf 1_{\{\tau_u>n\}}
\right],
\]

hence the geometric uniform error. Maximum, clipping and a Markov transition are nonexpansive in the supremum norm, so forcing and update errors accumulate at most linearly in the chosen finite depth.

The manuscript correctly warns that iteration depth may not be sent to infinity at fixed forcing error. The theorem is a regularization statement with a bias–error balance, not unconditional convergence of noisy iterates.

### 5.3 Comparison across different unknown zero sets

For two admissible occupations \(u,\widetilde u\), put \(w=u-\widetilde u\) and \(h=(T_\rho-I)w\). Stopping at the first zero of \(u\) gives

\[
w(x)
=\mathbb E_x w(X_S)
-\mathbb E_x\sum_{j<S}h(X_j).
\]

At \(\tau_u\), the terminal difference is \(-\widetilde u\le0\); on survival its positive part is at most one. Letting the truncation grow yields

\[
w(x)\le H\|h\|_\infty.
\]

Interchanging the two occupations gives the reverse inequality. This proves the displayed stability without assuming that their zero sets agree or are known.

This is the strongest new statement in v31. I found the stopping argument sound.

### 5.4 General noncentered laws

Any bounded law other than \(\delta_0\) has positive mass in some cone \(a\cdot v\ge\gamma>0\). If \(m\gamma>D\), a block in which all \(m\) increments fall in that cone forces exit from a positive component. The probability of such a block is at least \(p^m\), giving a geometric block tail and mean at most \(m/p^m\).

The conclusion is correct. The constants can be extremely poor when the useful cone has small mass; the manuscript says so. The centered variance bound is therefore the quantitatively meaningful version for the finite compass experiment.

## 6. Fixed-aperture locality

An infinite Bellman iteration could otherwise appear to require forcing on an aperture growing with depth. The manuscript instead kills the transition outside a fixed set \(W\) containing

\[
U+\overline B_{D+b+\varepsilon_0}.
\]

Starting from \(x\in U\), the entire positive component containing \(x\), and every first exit location from that component, lie in \(W\). Consequently the killed transition agrees with the full transition along every path up to the stopping time used in the proof. The Bellman and comparison estimates on \(U\) therefore use only forcing on this fixed enlarged aperture.

This localization is correct. It is important that the boundary convention is killing by zero extension, not periodic wraparound or row renormalization. The supplied interval implementation follows the correct substochastic convention.

## 7. Audit of the finite four-direction experiment

The compass law is centered, has second moment \(t^2\), and has no common positive drift direction. Choosing the grid spacing so that \(t\) is an exact integer number of grid steps makes every transition a finite lookup.

The prior-dependent iteration depth is fixed:

\[
H_*=\frac{(D_0+2\sigma_0+t)^2}{t^2},
\quad
L_*=\lceil2H_*\rceil,
\quad
n_*=6L_*.
\]

The survival contribution at this depth is at most \(2^{-6}=1/64\). The allowed forcing error contributes at most \(1/128\), and the reserved numerical update error contributes another \(1/128\). The total \(1/32\) lies strictly below the \(1/8\) threshold margin used by the hull lemma.

A fixed physical aperture contains \(O(\sigma^{-2})\) grid nodes. Because \(n_*\) is fixed by the prior, each pooled mean needs only a prior-dependent constant accuracy, with a logarithmic confidence factor. Thus the center and attempt counts have the displayed order. The retained hull stage costs \(O(N^2)=O(\sigma^{-4})\), and

\[
\sigma=\nu^{3/2}
\]

turns these into \(\nu^{-3}\), \(\nu^{-6}\), and the support-smoothing error

\[
\sigma^{2/3}=\nu.
\]

The exponent and error-budget calculations are correct.

The rational interval recursion is also valid. Monotonicity places the exact Bellman iterate between the lower and upper recursions. Adding an externally certified survival tail produces a conditional occupation enclosure. The word “conditional” is essential: the interval code does not infer the geometric survival bound, calibration quality, or physical class from the bit data.

## 8. Audit of the inherited v30 additions

### 8.1 Coupled command calibration

The v30 calibration theorem compares nominal and actual segment-hit indicators. A position, duration and angle perturbation changes the swept convex set only inside boundary tubes of radius

\[
r=\ell+\tau+b\alpha.
\]

A packing bound limits the number of physical components contributing in one localized command, and the planar convex tube estimate gives exceptional probability \(O(r/\sigma)\). This includes grazing nominal directions and errors depending on the commanded start.

The proof is coherent under the stipulated coupling. It does not estimate calibration from the observed bits. The finite theorem correctly requires the physical input error to shrink proportionally to \(\sigma/n_*\).

### 8.2 Threshold, hull and support reconstruction

Once the occupation estimate is uniformly within \(1/8\), thresholded grid nodes lie near a unique physical component and all sufficiently eroded interior nodes are retained. Separation prevents graph components from merging different bodies; convex hulls recover each protected component to Hausdorff error \(O(\sigma)\).

The compensated support convolution differentiates the kernel rather than the polygon. With the true \(C^6\) support bound,

\[
\|J_h*p_H-p_C\|_{C^2}
\le C(eh^{-2}+h^4),
\]

and \(h=e^{1/6}\) gives \(Ce^{2/3}\). Positivity of the true curvature radius then makes the smoothed result a genuine strictly convex body for small error.

I found no fatal flaw in these inherited arguments. Their reliance on curvature, \(C^6\), separation, a protective aperture and certified kernel evaluation remains substantial.

## 9. Technical qualifications for any resubmission

### 9.1 Keep the exact and finite theorems separate

The theorem for a general bounded displacement law is an exact functional statement on all translated spatial commands. The finite implementation is proved only for a four-atom compass law with exact grid shifts. A continuous law is not silently replaced by finite quadrature. This distinction is already present and should remain adjacent to every summary.

### 9.2 Display the prior dependence of constants

For the compass law, \(H_*\), \(L_*\), \(n_*\), the per-mean sample constant and the calibration tolerance depend on \(D_0/t\) and the other geometric priors. Big-\(O\) notation in \(\nu\) hides this dependence. For a general noncentered law, \(m/p^m\) may be enormous. These are legitimate fixed-class constants, but the article should not invite a class-uniform computational interpretation.

### 9.3 Rational certification is conditional

Exact rational intervals certify the finite algebra once forcing intervals and a survival bound are supplied. They do not certify the physical reciprocal coupling, the class priors, the patch margin, or the smooth geometric stage. The current implementation states this correctly.

### 9.4 The positive patch margin remains an input

Uniform finite recovery of primitive periods uses a known \(\eta>0\). With unknown margin, only the retained pointwise eventual statement is available. Version 31 does not turn that margin into a data-driven finite stopping certificate.

### 9.5 Rational relations are not exact Euclidean geometry

The discrete bounded-denominator relations are recovered exactly after geometric acceptance. The real generator vectors and basis coordinates remain estimates. The manuscript states this distinction and should preserve it in the abstract and theorem captions.

### 9.6 “Collision law” requires the complete command contract

A reader could otherwise interpret the result as passive one-bit collision counting. Every headline must keep together:

- localized commanded spatial densities;
- the displacement controller;
- translated reciprocal reverse starts;
- all-attempt normalization including solid starts;
- calibration that improves with localization scale;
- known command centers and horizons.

Without this contract, the reversal forcing is not the same observable.

## 10. Remaining top-four significance objections

### 10.1 The controlled input carries most of the spatial localization

The per-attempt output is one bit, but the experiment uses \(O(\nu^{-3})\) known spatial command centers. The exact datum is a pair of linear functionals on spatial densities. This is a meaningful output/input trade, not a reduction to a natural scalar invariant of an uncontrolled billiard flow.

### 10.2 The new analytic engine is classical potential theory

The mean-exit estimate, killed Green norm, stopped comparison and Bellman iteration are elegant in this setting, but they are standard martingale and dynamic-programming mechanisms. The manuscript credits them. The novelty is their coupling to the reciprocal collision forcing and the physical class, not a new general theory of random walks or value iteration.

### 10.3 Periodicity is recognized inside a strongly bounded periodic class

The theorem assumes a bounded periodic presentation and a known finite aperture containing the necessary motifs. It recognizes the full period group of a table already known to belong to that class. It does not infer crystallinity from an arbitrary aperiodic configuration or discover periodicity from passive data.

### 10.4 Strong geometric priors drive the finite theorem

The conclusion depends on component diameter and separation, curvature and \(C^6\) bounds, bounded presentation data, a known positive nonperiod patch margin, a fixed protective aperture, reciprocal calibration, and certified numerical primitives. These assumptions are not inferred from the bit record.

### 10.5 No statistical optimality theorem is proved

The displayed command, attempt and arithmetic orders are sufficient upper bounds for this design. There is no matching lower bound, no minimax theorem over the physical class, and no comparison in an information order with the position-output or uniform-launch experiments. The exponent therefore cannot carry the editorial significance by itself.

### 10.6 The natural passive inverse problems remain open

The paper does not prove rigidity from a uniformly prepared collision count, a passive unmarked trajectory, a marked-length spectrum, a spectral invariant, or exact analytic count germs. It correctly disclaims those conclusions. Those disclaimers also identify the limited reach of the present theorem at a top-four benchmark.

## 11. Literature assessment

The manuscript now correctly places its hit/no-hit functionals in the capacity-functional and mathematical-morphology tradition of Matheron and Molchanov. It also distinguishes its Bernoulli response from X-ray and wedge probes, whose outputs contain lengths or contact geometry.

For v31, the relevant random-walk and dynamic-programming tools are likewise classical. Lawler and Limic provide the standard Green-function and potential-theoretic setting for killed random walks. Bertsekas treats proper policies, finite expected termination and value-iteration subtleties in stochastic shortest-path problems. The manuscript does not claim those general principles as new.

I did not find, in this focused audit, a cited theorem that directly contains the complete combination of endpoint-excluded reciprocal collision forcing, unknown-zero-set occupation comparison and periodic obstacle reconstruction. That is a meaningful synthesis. This was not an exhaustive priority search, and absence from this audit is not a priority certificate.

A revised literature section should additionally connect the finite grid theorem to statistical active level-set or set-boundary estimation. The models differ, but that is the natural place to discuss whether the \(O(\nu^{-3})\) center/attempt order is merely sufficient or has any information-theoretic significance.

## 12. Reproducibility and independent diagnostics

The author's local source-content evidence records:

- 8,513 finite mathematical/source checks;
- 49 validation-contract checks;
- identical ordinary and optimized Python output;
- a warning-free 26-page primary build;
- no physical sensor execution;
- no formal proof certificate;
- no local full-package qualification claim.

The exact-source hosted workflow for the reviewed head is run `37140328128`. It checked out the exact triggering SHA, required current and retained entry points, qualified all fourteen declared documents, archived evidence, and uploaded the result. Every workflow step concluded successfully.

The accompanying `verify_review.py` imports no author code. Using exact integer and rational arithmetic, it performs 91,316 checks covering:

- exact mean exit times and the diameter–variance bound;
- killed Green positivity and row-sum identities;
- Bellman monotonicity, survival errors and geometric tails;
- comparison of occupations with different zero sets;
- forcing-error accumulation and rational interval enclosures;
- fixed-aperture agreement and killed compass transitions;
- pooled reciprocal reversal;
- positive-probability cone bounds;
- centered laws with no common drift direction;
- finite error and exponent balances;
- total-variation operator calibration.

Ordinary and optimized Python executions agree. These diagnostics support finite algebra only. They do not prove the continuum compactness, smoothing, calibration, period-margin, or apparatus assumptions and are not an editorial certificate.

## 13. Final verdict

**Response to the preceding concrete objections:** substantively successful. Version 31 removes the almost-sure drift-cone restriction, supplies a fixed-aperture finite pooled implementation, makes calibration and conditional interval certification explicit, and retains the exact-source package reproducibly.

**Mathematical audit:** no fatal counterexample found in the new v31 core or in the principal inherited v30 additions examined here. The scope and prior dependence must remain explicit.

**Editorial assessment:** the result is a rigorous and interesting active inverse problem for a highly controlled spatial-input collision experiment. Its central probabilistic machinery is classical, its global theorem is strongly prior-relative, and it does not reach a natural passive billiard invariant or a broad rigidity principle.

**Recommendation: reject at the requested Annals/Acta/Inventiones/JAMS benchmark.** A focused specialist-journal submission could be strong after fresh human proof review and compression around the reciprocal scalar inverse.
