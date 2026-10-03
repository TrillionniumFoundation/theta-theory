# External top-four referee report on A2 v31

**Manuscript:** Qian Qi, *Scalar collision laws and recognition of periodic dispersing billiards*  
**Reviewed revision:** `revision/a2-v31-reciprocal-command-reconstruction-2026-10-04`  
**Equivalent referee-copy alias:** `revision/a2-v31-referee-copy-2026-10-04`  
**Reviewed commit:** `27d109b0eba6a03d453834ef9da9418446ac637d`  
**Reviewed tree:** `ff918d19db00fc3aea087a02e6b4481e197c2767`  
**Immediate v30 baseline:** `c01118b11779b6161cc34e311f840e5ab36a019c`  
**Controlling preceding external report:** `6444b57768313ac68978b3ee04a428b4832ccb6e`  
**Date:** 4 October 2026  
**Requested benchmark:** *Annals of Mathematics* / *Acta Mathematica* / *Inventiones Mathematicae* / *Journal of the AMS*  
**Status:** author-requested, AI-assisted referee-style assessment; not a journal decision or proof certificate.

## 1. Recommendation

**Recommendation at the requested four-journal benchmark: reject.**

Version 31 is a genuine mathematical advance over the previously reviewed scalar-collision manuscript. It removes the v30 almost-sure directional-cone condition from the exact randomized inverse, proves a mean-exit comparison for occupations with different unknown zero sets, localizes the Bellman inverse to one fixed aperture, and supplies a four-direction finite grid implementation with pooled Bernoulli means and rational interval enclosures.

I found no fatal counterexample to the new v31 core. I also audited the principal v30 additions—coupled position/time/angle calibration and the threshold–cluster–hull–smoothing reconstruction—because no separate v30 review branch exists. On the hypotheses stated, those arguments are coherent. The negative recommendation is therefore not based on a known false central theorem.

The obstacle is editorial and conceptual. Although each attempt returns one bit, the controller may choose an increasingly fine two-dimensional family of localized launch densities, prescribe a displacement law, implement an exactly translated reciprocal reverse preparation, improve position/time/angle calibration with the localization scale, and keep attempted solid starts in the denominator as zero outcomes. The exact datum is a pair of functionals on spatial inputs, not two numbers and not an ordinary passive billiard invariant.

The inverse is elegant, but its general engines are classical: reciprocal endpoint cancellation yields a Markov difference, bounded-component geometry gives finite mean exit, a stopped quadratic martingale gives the resolvent bound, and monotone value iteration reconstructs the nonnegative solution. The global table conclusion then invokes strong retained geometric and periodic priors, including a known positive patch margin. This is serious specialist-journal mathematics, but in my judgment it does not reach the exceptional naturality, breadth or conceptual transformation required by the four journals named above.

## 2. Frozen source and review scope

Both v31 revision names resolve to commit

`27d109b0eba6a03d453834ef9da9418446ac637d`

and tree

`ff918d19db00fc3aea087a02e6b4481e197c2767`.

The parent is the complete v30 revision

`c01118b11779b6161cc34e311f840e5ab36a019c`.

The latest preceding external report is v29 commit

`6444b57768313ac68978b3ee04a428b4832ccb6e`,

which reviewed author commit

`b81664d3961cdbad58563f37dcaed03288de199e`.

The complete v30 tree is preserved at `retained/v30` as

`1a6f8f32ec62aec586883e67753b3a72895f875c`.

The nine inherited v30 active-core files are pinned at tree

`315c9c3ec006eadfc66cff72acf9855af29685be`,

and the current core tree is

`aa9026847310ecd9205fe631b5ed85aa141b70ed`.

No v32 branch existed when this review was frozen. The review branch starts directly from the author head and changes only

`reviews/a2-v31-external-harsh-top4-rereview-2026-10-04/`.

## 3. Information model

For a displacement \(a\), the recorded bit is one exactly when a free start at \(q\) has a first collision along the unreflected segment \([q,q+a]\). A solid start and a free miss both produce zero and both remain in the denominator. The reciprocal reverse command starts at \(q+a\) and uses displacement \(-a\).

The fixed-displacement identity is

\[
B_a(q)-B_{-a}(q+a)
=\mathbf1_{\mathcal O}(q+a)-\mathbf1_{\mathcal O}(q).
\]

For a prescribed displacement law \(\rho\), two pooled reciprocal means therefore reveal

\[
P_\rho^+(f)-P_\rho^-(f)
=\int f(x)(T_\rho-I)\chi(x)\,dx,
\qquad
T_\rho w(x)=\int w(x+a)\rho(da).
\]

Translated kernel inputs give

\[
g_\sigma=(T_\rho-I)u_\sigma,
\qquad
u_\sigma=\kappa_\sigma*\chi.
\]

This coupling and the all-attempt normalization are indispensable. Independently randomized reverse starts or conditioning on successful/free preparations would define a different experiment.

## 4. Audit of the mean-exit inverse

### 4.1 Centered laws

Assume \(|a|\le b\), \(\mathbb E a=0\), and \(\mathbb E|a|^2\ge v_*>0\). Before hitting \(\{u=0\}\), the walk stays inside one positive component because the step bound is smaller than the component separation. If that component has diameter at most \(D\), then for \(S=\tau\wedge n\),

\[
|X_S-x|\le D+b.
\]

The stopped martingale

\[
|X_n-x|^2-n\mathbb E|a|^2
\]

gives

\[
\mathbb E_x\tau\le
H=\frac{(D+b)^2}{v_*}.
\]

Markov's inequality at a block length at least \(2H\), followed by the Markov property, yields the geometric survival tail. This proof is correct and does not require nonsingular covariance or a common drift direction.

### 4.2 Bellman reconstruction

With \(g=(T_\rho-I)u\), define

\[
V_0=0,\qquad
V_{n+1}=\max(0,T_\rho V_n-g).
\]

Then \(0\le V_n\le V_{n+1}\le u\). If \(e_n=u-V_n\), then on the positive set \(e_{n+1}\le T_\rho e_n\), so

\[
0\le u(x)-V_n(x)
\le\mathbb E_x\!\left[
u(X_n)\mathbf1_{\{\tau_u>n\}}
\right].
\]

The geometric exit tail therefore gives uniform convergence. Forcing and update errors accumulate at most linearly in the finite iteration depth. The manuscript correctly treats depth as a regularization parameter rather than sending it to infinity at fixed noise.

### 4.3 Different unknown zero sets

For two admissible occupations \(u,\widetilde u\), put \(w=u-\widetilde u\) and \(h=(T_\rho-I)w\). Stop at the first zero of \(u\). At the stopping time the terminal value is \(-\widetilde u\le0\); on survival its positive part is at most one. The stopped representation gives

\[
w(x)\le H\|h\|_\infty.
\]

Interchanging \(u\) and \(\widetilde u\) gives

\[
\|u-\widetilde u\|_\infty
\le
H\|(T_\rho-I)(u-\widetilde u)\|_\infty.
\]

This is the strongest new v31 statement, and I found the argument sound.

### 4.4 General noncentered laws

Any bounded law other than \(\delta_0\) has positive mass \(p\) in some cone \(a\cdot v\ge\gamma>0\). A block of \(m\) such increments, with \(m\gamma>D\), forces exit from a positive component. Hence the survival tail is bounded by

\[
(1-p^m)^{\lfloor n/m\rfloor}
\]

and the mean exit time by \(m/p^m\). The conclusion is correct, although these constants may be extremely poor. The centered bound is the quantitatively relevant one for the finite compass protocol.

## 5. Fixed-aperture locality

The manuscript kills the transition outside one prior-controlled set \(W\) containing

\[
U+\overline B_{D+b+\varepsilon_0}.
\]

Starting from \(U\), the complete positive component and its first exit location lie in \(W\). Thus the killed and full transitions agree along every path up to the stopping time used by the Bellman and comparison proofs. The finite algorithm correctly uses zero extension: it neither wraps periodically nor renormalizes a boundary row.

This closes a real implementation issue. An iteration with large depth does not require an aperture growing with depth.

## 6. Finite four-direction realization

The compass law

\[
\rho_\square=\tfrac14(
\delta_{te_1}+\delta_{-te_1}+
\delta_{te_2}+\delta_{-te_2})
\]

is centered, has second moment \(t^2\), and has no common positive drift direction. A grid spacing chosen so that \(t\) is an exact integer number of mesh steps turns its transition into four finite lookups.

With

\[
H_*=\frac{(D_0+2\sigma_0+t)^2}{t^2},
\quad
L_*=\lceil2H_*\rceil,
\quad
n_*=6L_*,
\]

the survival error is at most \(1/64\). The allowed forcing error contributes at most \(1/128\), and the reserved numerical update error another \(1/128\), for total occupation error \(1/32<1/8\).

A fixed aperture has \(O(\sigma^{-2})\) command centers. Since \(n_*\) is fixed by the prior, Hoeffding sampling gives the stated logarithmic factor. The hull computation costs \(O(\sigma^{-4})\). With

\[
\sigma\asymp\nu^{3/2},
\]

the theorem obtains

\[
O(\nu^{-3})\ \text{centers},\qquad
O\!\left(\nu^{-3}\log\frac{C}{\nu\delta}\right)
\ \text{attempts},
\qquad
O(\nu^{-6})\ \text{arithmetic},
\]

while compensated support smoothing gives \(\sigma^{2/3}=O(\nu)\) in \(C^2\). These calculations are consistent.

The exact rational interval code encloses the Bellman iterate once forcing intervals are supplied. Adding a certified survival tail gives a conditional occupation enclosure. It does not infer the physical class, reciprocal coupling, calibration or survival bound from the bits themselves.

## 7. Inherited v30 material

No separate v30 external report branch exists, so I also examined the two principal inherited additions.

First, the command-calibration theorem confines changes of the swept-set and solid-start indicators to convex boundary tubes of radius

\[
r=\ell+\tau+b\alpha.
\]

A local packing bound and planar convex tube estimate give bias \(O(r/\sigma)\), including grazing nominal commands and start-dependent bounded errors. This is coherent under the stipulated coupling, but calibration is an input resource, not something estimated from the collision bits.

Second, thresholding a uniformly accurate occupation grid separates components; connected clusters and convex hulls recover protected bodies to \(O(\sigma)\) Hausdorff error. The compensated convolution estimate

\[
\|J_h*p_H-p_C\|_{C^2}
\le C(eh^{-2}+h^4)
\]

with \(h=e^{1/6}\) yields \(Ce^{2/3}\). Positivity of the true curvature radius makes the smoothed output a genuine strictly convex body. I found no fatal flaw in this route under the stated curvature, \(C^6\), separation and aperture assumptions.

## 8. Necessary qualifications

The following distinctions must remain explicit in any journal version.

1. **Exact versus finite.** The theorem for an arbitrary bounded displacement law is an exact functional statement over translated spatial inputs. The finite implementation is proved for a four-atom law; a continuous law is not silently discretized.

2. **Prior-dependent constants.** \(H_*,L_*,n_*\), sample constants and calibration tolerances depend on the full geometric prior. For a general noncentered law, \(m/p^m\) can be enormous.

3. **Conditional intervals.** Rational enclosures certify finite algebra conditional on forcing and survival bounds; they do not certify the apparatus or geometry.

4. **Known patch margin.** Uniform finite period locking still requires a known positive \(\eta\). Unknown margin gives only the retained pointwise eventual statement.

5. **Exact discrete relations versus real geometry.** Bounded-denominator relations are recovered exactly after locking; Euclidean generator coordinates and the period basis remain estimates.

6. **Complete sensor contract.** “Scalar collision law” must always be accompanied by localized commands, prescribed displacements, translated reciprocal starts, all-attempt normalization and scale-dependent calibration.

## 9. Top-four significance assessment

The finite output alphabet does not make this a low-information passive inverse problem. Spatial localization is carried by \(O(\nu^{-3})\) known command centers. The exact datum is a pair of linear input-output functionals.

The new probabilistic engine is classical potential theory and dynamic programming. Its use here is clean and useful, but it does not establish a new general random-walk or Bellman principle.

The global theorem assumes a bounded periodic presentation, strong component and smoothness bounds, a fixed protective aperture, calibrated reciprocal commands and a known patch margin. It recognizes periods within that class; it does not infer crystallinity from an arbitrary configuration.

The displayed rates are sufficient upper bounds. There is no matching lower bound, minimax theorem, or information-order comparison with the retained position-output or uniform-launch experiments.

Finally, the work does not establish rigidity from passive unmarked trajectories, uniformly prepared counts, marked lengths, spectra or exact analytic count germs. The manuscript correctly disclaims these statements, but those disclaimers also delimit the theorem's reach at a top-four benchmark.

## 10. Literature and provenance

Matheron's capacity-functional framework and Molchanov's random-set theory already place hit probabilities and swept-set morphology in a classical setting. X-ray and wedge-probing papers study richer outputs but confirm the established active-probing context.

Lawler–Limic provide the standard killed Green and random-walk potential theory. Bertsekas treats proper finite-expected-termination policies and value-iteration behavior. The manuscript now credits these mechanisms and does not claim them as abstract novelties.

I did not find in this focused audit a cited theorem containing the complete combination of endpoint-excluded reciprocal collision forcing, different-zero-set stability, fixed-aperture finite realization and periodic reconstruction. That synthesis is meaningful, but this was not an exhaustive priority search.

A future version should compare the finite statistical theorem with binary active level-set or set-boundary estimation. Without a lower bound, the \(\nu^{-3}\) order should not be presented as statistically sharp.

## 11. Verification and source qualification

The author's local evidence records 8,513 finite mathematical/source checks, 49 validation-contract checks, ordinary/optimized agreement and a warning-free 26-page primary. It explicitly reports no physical sensor execution and no formal proof certificate.

The exact-source hosted workflow, run `37140328128`, checked out the reviewed SHA, qualified all fourteen declared documents, archived the evidence and uploaded the artifact. Every workflow step succeeded. Source delivery is therefore not a basis for the rejection.

The accompanying independent `verify_review.py` imports no author code and performs 91,316 exact integer/rational checks of finite-state mean exits, Green row sums, Bellman tails, different-zero-set comparison, rational intervals, fixed-aperture killing, compass shifts, pooled reversal and exponent balances. Ordinary and optimized executions agree. These checks are diagnostics, not a continuum proof or editorial certificate.

## 12. Final verdict

**Response to the concrete mathematical objections:** substantively successful. Version 31 removes the almost-sure drift-cone restriction and gives a genuine finite pooled realization.

**Correctness audit:** no fatal counterexample found in the new v31 core or the principal inherited v30 additions examined here.

**Editorial assessment:** a rigorous and interesting active inverse problem under a highly controlled spatial-input contract and strong physical priors, built from classical potential/Bellman mechanisms.

**Recommendation: reject at the requested Annals/Acta/Inventiones/JAMS benchmark.** A focused specialist-journal submission could be strong after fresh human proof review and compression around the reciprocal scalar inverse.
