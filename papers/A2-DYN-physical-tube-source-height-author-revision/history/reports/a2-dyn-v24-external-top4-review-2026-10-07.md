# External top-four referee report on A2-DYN revision 24

**Manuscript:** Qian Qi, *Collision records, arithmetic, and raw local inversion in a triangular Lorentz gas*  
**Reviewed author branches:** `revision/a2-dyn-v24-referee-response-2026-10-06`, `revision/a2-dyn-v24-referee-copy-2026-10-06`  
**Reviewed commit:** `c1d6940a875f501ee1957204e81772df7b9b39d6`  
**Reviewed repository tree:** `e3fcc090d59fe199649db0eea3e434e00e7aa13a`  
**Frozen ordinary paper tree:** `f15ab9854d022319db374f8ce38f4e6a4273dd84`  
**Active manuscript directory:** `papers/A2-DYN-v24-referee-response`  
**Controlling substantive report:** `reviews/a2-dyn-v22-external-top4-review-2026-10-06/REFEREE_REPORT.md`  
**Controlling report commit / blob:** `d21f74a59eed269c4b215c53b85434a3a449c779` / `b5e96b424ca9d73fc1c113142556cc8913281ca7`  
**Reviewed v22 author commit:** `a656998fee8176316850ef87ac447970d712aae2`  
**Recovered v23 ordinary paper tree:** `37e6f9a75ad1a6bb4f2c8710494cc50edac9e7c9`  
**Date:** 7 October 2026  
**Requested benchmark:** *Annals of Mathematics* / *Acta Mathematica* / *Inventiones Mathematicae* / *Journal of the AMS*  
**Status:** author-requested, AI-assisted referee-style assessment; not a commissioned journal report, an editorial decision, a formal proof certificate, or an independent human billiards-specialist report.

## 1. Recommendation

**Recommendation at the requested four-journal benchmark: reject in the present form.**

Revision 24 is a genuine and substantial mathematical advance. It incorporates the previously unattached revision-23 ordinary source, whose two main additions are a damped finite-order removal of smoothing and a wider fixed-count Fourier band, and then adds a multiscale return-clock comparison, all fixed marked Gaussian moments, and a rate-preserving prescribed-count band.

The principal new fixed-count conclusion is

\[
 n^2\int_{2n^{-99/200}\le |z|\le2n^{-633/1400}}
       |\Phi^{[k],a}_{n,R}(z)|\,dz
 \le C\left(M_a n^{-3/280}+V_a n^{-983/350}\right),
\]

uniformly in the radius, the specified return count, and the position of one actual-return mark. There is no average in the return count and no division by annular volume. Combining this estimate with the inherited marked central theorem gives an integrated Gaussian comparison on

\[
 |v|\le2n^{67/1400}
\]

with the original central error

\[
 C\left(M_a n^{-3/280}\sqrt{\log(2+n)}
       +V_a n^{-9/175}\right).
\]

Revision 24 also proves, for each fixed tensor order, Gaussian polynomial moments of the actual return record with one actual-return insertion, together with a fourth-root stopping comparison and an improved `O(n^{-1/4})` actual covariance/Cesaro identification.

I found no decisive counterexample in the four mathematical modules not previously subjected to a substantive referee report:

- `core/48_damped_unsmoothing.tex`;
- `core/49_wider_fixed_count_band.tex`;
- `core/50_multiscale_stopping.tex`;
- `core/51_rate_preserving_band.tex`.

The small-mass cumulant estimate has the correct logarithmic counting loss. The cubic residual expansion keeps its lower-order corrections inside a fully damped chronological operator word. The multiscale shell calculation gives a genuine `n^(1/4)` comparison without a logarithmic shell loss. The mixed marked-cumulant partition count has the advertised parity. The analytic-radius and Taylor-remainder factors are retained, and the raw four-dimensional Jacobian and kernel exponents are correctly tracked.

These results close meaningful portions of the objections in the revision-22 report. In particular, the paper now proves a substantially wider fixed-count region while preserving the old central rate, rather than trading radius for a slower principal error.

The negative recommendation nevertheless remains necessary. The manuscript continues to be organized around a parameter-uniform raw mixed-density local limit theorem which is not proved. The new physical cutoff is

\[
 2n^{-633/1400},
\]

or rescaled radius `2 n^(67/1400)`. The previously targeted small-frequency endpoint `n^(-2/5)` corresponds to rescaled radius `n^(1/10)`. Thus a nontrivial farther annulus remains, followed by compact nonzero torus/peripheral regions, growing roof frequencies, and the far-roof splice. The exact raw error budget also still contains the long-time second-derivative sum, the new-kernel local extracted-edge correction, and the finite-band residual integral. Weighted versions and the relative replacement of completed-return events by exact physical-time/lattice events remain open.

These are load-bearing mechanisms of the advertised theorem, not presentation details. At the requested benchmark the completed Gaussian, moment, phase, finite-extraction, averaged-orbit, and fixed-count inner-band package is not a substitute for the unproved raw endpoint.

The unconditional results are now unusually substantial for one carefully engineered Lorentz family. A reorganized paper centered on those completed theorems could be a strong specialist contribution after independent expert review. That is a distinct editorial claim from acceptance at the four-journal benchmark for the raw LLT currently organizing the manuscript.

## 2. Frozen source, chronology, and exact qualification

The two named revision-24 author branches resolve to the same commit:

`c1d6940a875f501ee1957204e81772df7b9b39d6`.

The repository tree at this commit is

`e3fcc090d59fe199649db0eea3e434e00e7aa13a`.

The frozen ordinary paper tree is

`f15ab9854d022319db374f8ce38f4e6a4273dd84`.

The chronology requires care. The branch named

`revision/a2-dyn-v23-referee-response-2026-10-06`

ends at assembly commit

`ca2b585c126a0f100d6ab16cb491615f7cd7c770`.

That commit staged immutable objects for ordinary paper tree

`37e6f9a75ad1a6bb4f2c8710494cc50edac9e7c9`,

but did not attach the ordinary manuscript to that branch. Revision 24 recovers that exact source at commit

`699f17e6bd75c3c8a741a9f00837ab4654e8c3d1`

on the new author branch and then continues its mathematics. There is no separately located substantive v23 referee report. I have therefore reviewed the recovered v23 additions together with the v24 additions, rather than treating the v23 modules as previously accepted.

Relative to the recovered v23 source, revision 24 preserves all forty-nine inherited core files, all inherited Python sources, and the bibliography byte-for-byte. It adds:

- `core/50_multiscale_stopping.tex`;
- `core/51_rate_preserving_band.tex`.

Relative to the last substantive review at revision 22, the complete new mathematical set is:

- `core/48_damped_unsmoothing.tex`;
- `core/49_wider_fixed_count_band.tex`;
- `core/50_multiscale_stopping.tex`;
- `core/51_rate_preserving_band.tex`.

Five exact inherited edits affect only `main.tex`; all old mathematical labels remain. The final commit also removes temporary layout and inspection workflows and makes two typography-only repairs without changing the mathematical conclusions.

The source manifest accurately records:

- `all_fixed_marked_moments_proved: true`;
- `quarter_order_stopping_proved: true`;
- `rate_preserving_band_proved: true`;
- `full_fixed_return_complementary_integral_proved: false`;
- `exact_physical_event_replacement_proved: false`;
- `full_raw_LLT_proved: false`.

The exact-source qualification completed successfully on both reviewed branches:

- response branch run `37499198547`;
- referee-copy branch run `37499211798`.

For the response branch, exact checkout, source/report-scope archiving, native TeX and numerical-check installation, normal and optimized verification, complete article build, PDF metadata/render checks, and artifact upload all completed successfully. The response artifact is

`11429162251`,

named

`a2-dyn-v24-c1d6940a875f501ee1957204e81772df7b9b39d6`,

with digest

`sha256:640f2535aef8f25314162c7a5775b9eb1845cf1f3d7a75ac0e1168d2d3cd4841`.

These facts establish exact source identity and successful execution of the declared finite checks and native build. They do not certify the continuum collision-space estimates, the cumulant and multiscale arguments, the missing outer Fourier regions, the long-time raw-density constants, or the full theorem.

The present review branch starts directly from the reviewed author commit and adds only this report under

`reviews/a2-dyn-v24-external-top4-review-2026-10-07/`.

No manuscript source, author branch, workflow, earlier report, or unrelated repository path is modified.

## 3. What revisions 23 and 24 actually prove

Let

\[
 h_R=f_R-\bar G_R\mathbf1_{Y_R^*}
\]

be the bounded centered collision compensation, and write

\[
 C^{[k],a}_{n,R}(v)
 =\int_{Y_R^*} a((F_R^*)^k x)
   e^{iv\cdot(J_{n,R}(x)-n\bar G_R)/\sqrt n}\,d\nu(x).
\]

The corresponding physical-frequency transform is

\[
 \Phi^{[k],a}_{n,R}(z)
 =\int_{Y_R^*} a((F_R^*)^k x)e^{iz\cdot J_{n,R}(x)}\,d\nu(x),
\]

and its absolute value agrees with that of the centered transform under `v=sqrt(n) z`.

The new revisions establish the following unconditional conclusions.

### 3.1 Small-mass cumulants for the smoothing residual

For a bounded-variation observable `u` with

\[
 \|u\|_1=O(\delta),
\]

the manuscript proves at every fixed order `q` that

\[
 \sum_{\mathbf j\in\mathbb Z^{q-1}}
 \left|\operatorname{cum}(u,u\circ T^{j_2},\ldots,u\circ T^{j_q})\right|
 \le C_q\delta(1+|\log\delta|)^{q-1}.
\]

Consequently

\[
 |\operatorname{cum}_q(S_m u)|
 \le C_qm\delta(1+|\log\delta|)^{q-1}.
\]

For centered real `u`, this gives

\[
 \mathbb E|S_m u|^4
 \le C\left[m^2\delta^2(1+|\log\delta|)^2
       +m\delta(1+|\log\delta|)^3\right].
\]

### 3.2 Every fixed even collision moment and deterministic maximum

For every fixed integer `p>=2`, centered bounded-variation collision observables satisfy

\[
 \mathbb E|S_m u|^{2p}
 +\mathbb E\max_{0\le l\le m}|S_lu|^{2p}
 \le C_pm^p.
\]

The theorem is uniform in translated and reversed deterministic intervals and under a bounded initial density. It is a fixed-order result; no all-orders exponential moment is claimed.

### 3.3 Higher-moment clock windows

For each fixed `p>=2`, the actual forward and backward return clocks obey

\[
 \nu_R^*\{|N^\pm_{j,R}-m_j|>b\}
 \le C_p\frac{(j+b)^p}{b^{2p}}.
\]

The recovered v23 proof optimizes one global window and obtains stopping exponent

\[
 s_p=\frac{p}{4p+1}.
\]

Revision 24 subsequently improves the stopping comparison by summing over deviation scales and obtains the limiting fourth-root rate without sending `p` to infinity.

### 3.4 Damped cubic removal of smoothing

For a deterministic marked two-sided collision interval of length `m`, the recovered v23 theorem proves

\[
 \begin{aligned}
 |I^a_{r,s,R}(z)|\le{}&
 CM_a\epsilon^{-8}(1+m|z|)^3e^{-cm|z|^2}
 +C\epsilon V_a\\
 &+CM_a\epsilon(1+m|z|)^3\\
 &+CM_a|z|^4\left[m^2\delta^2L_\delta^2
                    +m\delta L_\delta^3\right],
 \end{aligned}
\]

on the stated real-frequency damping domain, where `delta` is the coarse smoothing scale and `epsilon` is used only for the insertion and finitely many residual factors.

The degrees zero through three of the residual phase remain inside chronological words whose twisted power lengths sum to the full deterministic interval. Only the fourth-order Taylor remainder is estimated without damping.

### 3.5 The recovered v23 wider fixed-count band

With fixed spectral degree `Q=19`, clock moment order `2p=20`, coarse scale

\[
 \delta=\frac14n^{-1/5},
\]

and fine scale

\[
 \epsilon=\frac14n^{-3},
\]

the recovered source proves at every prescribed count

\[
 n^2\int_{2n^{-99/200}\le|z|\le2n^{-19/42}}
       |\Phi^{[k],a}_{n,R}(z)|\,dz
 \le C\left(M_an^{-5/861}+V_an^{-59/21}\right).
\]

Equivalently the rescaled outer radius is `2 n^(1/21)`.

### 3.6 Fourth-root multiscale stopping

Revision 24 defines the total forward/backward clock deviation

\[
 D_{n,k,R}=|N^-_{k,R}-m_k|+|N^+_{n-k,R}-m_{n-k}|.
\]

It combines a polynomial fixed-moment bound for moderate deviations with an exponential cumulative-return bound for far deviations. Decomposing into dyadic shells beginning at `sqrt(n)` gives, for every fixed real `q>=1`,

\[
 \|Z_{n,k,R}-W_{n,k,R}\|_q\le C_q n^{1/4},
\]

and

\[
 \|Z_{n,k,R}\|_q+\|W_{n,k,R}\|_q\le C_q\sqrt n.
\]

The associated marked characteristic-function comparison is

\[
 \left|C^{[k],a}_{n,R}(v)
 -\int a(y)e^{iv\cdot W_{n,k,R}(y)/\sqrt n}\,d\nu(y)\right|
 \le CM_a|v|n^{-1/4}.
\]

The right side vanishes at `v=0`.

### 3.7 All fixed marked Gaussian moments

For each fixed integer `d>=1`, revision 24 proves

\[
 \left\|
 \int_{Y_R^*}a((F_R^*)^kx)
 \left(\frac{U_{n,R}(x)}{\sqrt n}\right)^{\otimes d}\,d\nu(x)
 -\alpha_a\mathcal G_d(D_R)
 \right\|
 \le C_d\left[M_an^{-1/4}+(M_a+V_a)n^{-\rho_d}\right],
\]

where

\[
 \rho_d=\begin{cases}
 1/2,&d\text{ odd},\\
 1,&d\text{ even}.
 \end{cases}
\]

The actual normalized covariance and its induced Cesaro expression therefore converge at rate `O(n^(-1/4))`. Absolute summability of the induced correlation series is not claimed.

### 3.8 Rate-preserving fixed-count band

Revision 24 chooses

\[
 \varepsilon_\natural=\frac{67}{1400},
 \qquad
 V_n^\natural=n^{67/1400},
 \qquad
 B_n^\natural=n^{-633/1400}.
\]

It proves the prescribed-count raw estimate

\[
 n^2\int_{2n^{-99/200}\le|z|\le2B_n^\natural}
       |\Phi^{[k],a}_{n,R}(z)|\,dz
 \le C\left(M_an^{-3/280}+V_an^{-983/350}\right),
\]

and the wider central comparison

\[
 \int_{|v|\le2V_n^\natural}
 |C^{[k],a}_{n,R}(v)-\alpha_a e^{-v^{\mathsf T}D_Rv/2}|\,dv
 \le C\left(M_an^{-3/280}\sqrt{\log(2+n)}
             +V_an^{-9/175}\right).
\]

### 3.9 Exact weighted raw identity at the new cutoff

For marked insertions which satisfy both the bounded-variation hypotheses of the Fourier theorem and the finite-record admissibility required by the structural extraction, revision 24 writes an exact raw decomposition with kernel

\[
 K_n^\natural=\mathcal F^{-1}\chi(\cdot/B_n^\natural).
\]

The corresponding error budget retains explicitly:

- the new-kernel local extracted-edge correction;
- the finite-band edge-subtracted residual integral;
- the far-roof term containing the actual second-derivative sum `A_2(n,L_n,R,w)`;
- the high-count convolution correction;
- the Gaussian tail outside the new central ball.

The theorem does not suppress the unresolved quantities.

## 4. Audit of the small-mass cumulant estimate

The proof combines two bounds for an anchored joint cumulant of the smoothing residual:

1. a time-independent `O(delta)` bound obtained by placing the anchored factor in one block of every partition term and using its `L1` norm;
2. an exponential-in-diameter bound inherited from finite-product decoupling and independent-block cumulant cancellation.

For anchored tuples of diameter at most `J`, the count is polynomial of degree `q-1`; for larger diameter, the exponential estimate is summable. Choosing `J` proportional to `1+|log delta|` yields

\[
 C_q\delta(1+|\log\delta|)^{q-1}.
\]

The exact finite-interval multiplicity is at most `m`, giving the stated cumulant bound without introducing a smoothing-independent boundary term. At orders two and four, the identity

\[
 \mathbb E X^4=\operatorname{cum}_4(X)+3\operatorname{cum}_2(X)^2
\]

then gives the paired and connected residual contributions appearing later.

I found this argument coherent. It does not assume independence of residual blocks or analyticity of the unsmoothed twist.

A specialist should nevertheless check that the finite-product decoupling estimate used in the diameter bound is available with the required uniform constants on every local collision space and for repeated times. The manuscript addresses repeated times as zero-length powers, and I found no contradiction in that treatment.

## 5. Audit of fixed even moments and deterministic maxima

The proof first uses the finite moment-cumulant identity for `S_m u`. Since the observable is centered, singleton blocks vanish. Every remaining partition of `2p` indices has at most `p` blocks, while each fixed-order cumulant is `O(m)`. Thus

\[
 \mathbb E|S_m u|^{2p}=O(m^p).
\]

For the maximum, the manuscript enlarges to a dyadic interval and writes every prefix as a union of at most one aligned interval at each scale. At scale length `l`, the expectation of the maximum `2p`th power over the aligned intervals is bounded by

\[
 C(M/l)l^p.
\]

Minkowski's inequality over scales then gives an `L^(2p)` maximum norm of order `sqrt(M)` because

\[
 \sum_j2^{-j(p-1)/(2p)}<\infty
\]

for `p>1`.

Translation, reversal, vector components, and a bounded initial density are handled without introducing an induced mixing assumption. I found no exponent or normalization error here.

## 6. Audit of damped cubic unsmoothing

The central improvement over revision 22 is methodological. The earlier first-order unsmoothing estimate took the absolute value of the whole residual phase before applying spectral damping. The recovered v23 proof instead writes

\[
 e^{iX}=1+iX-\frac{X^2}{2}-\frac{iX^3}{6}+\mathcal R_4(X),
 \qquad |\mathcal R_4(X)|\le |X|^4/24,
\]

with

\[
 X=|z|S_mu,
 \qquad
 u=\xi\cdot(h_R-h_{R,\delta}).
\]

The fourth-order remainder is bounded by the small-mass fourth moment. For degrees one through three, every residual factor is smoothed at the fine scale and retained as a multiplier inside the coarse twisted word. After sorting the residual times together with the actual-return mark, the nonnegative twisted power lengths sum to the full deterministic interval `m`. The real-frequency damping therefore contributes

\[
 e^{-cm|z|^2}
\]

to every corrected term.

The worst multiplier cost is `epsilon^(-8)`, corresponding to the mark plus three residual factors. Summing the ordered time tuples gives the factor `(1+m|z|)^3`. Replacing original residual factors by their fine smoothing costs

\[
 C M_a\epsilon(1+m|z|)^3,
\]

while insertion smoothing costs `C epsilon V_a`.

This separation of scales is essential. The fine scale does not define a new twisted operator and does not enter the analytic damping domain. Repeated insertion times become zero-length powers, while endpoint marks are treated by the same word.

I found no decisive algebraic or scaling flaw in this argument. Its load-bearing inherited input is the compatibility of the local collision distribution spaces, smooth multipliers, and the uniform real-frequency power bound under a chronological product with up to four multipliers. Independent anisotropic-operator review should check this composition carefully.

## 7. Audit of the recovered v23 wider band

With

\[
 Q=19,\quad p=10,\quad
 \delta=\frac14n^{-1/5},\quad
 \epsilon=\frac14n^{-3},\quad
 |v|\le2n^{1/21},
\]

the two damping-domain quantities are

\[
 |z|\delta^{-2}=O(n^{-11/210}),
 \qquad
 |z|^{18}\delta^{-40}=O(n^{-1/7}).
\]

After the four-dimensional change of variables, the principal undamped losses have decay exponents

\[
 \frac{59}{21},\quad
 \frac76,\quad
 \frac{2}{105},\quad
 \frac{86}{105},\quad
 \frac5{861}.
\]

The slowest term is the higher-moment stopping error `n^(-5/861)`. The paired fourth-order residual has strictly larger power margin, so its logarithmic square is absorbed.

The resulting theorem is valid and useful, but revision 24 supersedes its principal central-rate budget by replacing the single-window stopping optimization with the multiscale comparison. The recovered theorem remains a separate valid statement and a useful consistency check on the proof architecture.

## 8. Audit of the multiscale return-clock comparison

The manuscript proves two bounds for the total clock deviation `D`:

\[
 \nu_R^*(D>b)
 \le C_p\frac{(n+b)^p}{b^{2p}},
\]

and

\[
 \nu_R^*(D>b)
 \le C_pe^{a_0n-c_0b}.
\]

The first follows from fixed even moments of the visit count and a union bound for the forward and backward clocks. The second uses the cumulative-return tail and actual-return invariance to identify the backward clock marginal; no independence is used.

For a deterministic deviation width `L`, a sum of four fixed prefix/suffix maxima bounds the pathwise difference whenever `D<=L`. Its `2p`th moment is `O(L^p)`. On a shell `L/2<D<=L`, Holder's inequality gives

\[
 C_{p,q}L^{q/2}\nu_R^*(D>L/2)^{1-q/(2p)}.
\]

For moderate shells `L<=An`, this becomes

\[
 C n^{p-q/2}L^{3q/2-2p}.
\]

Starting at `L` of order `sqrt(n)`, the first term is exactly of order `n^(q/4)`. Choosing `p` so that

\[
 2p>\frac{3q}{2}
\]

makes the dyadic shell series geometric. Far shells are summable by the exponential bound. Taking the `q`th root yields

\[
 \|Z-W\|_q=O(n^{1/4}).
\]

For `q=2`, one may take `p=2`, and the moderate contribution is

\[
 C\sum_j n/L_j=O(\sqrt n),
\]

as claimed.

I found the shell exponents and the absence of a logarithmic shell loss correct. The proof is also careful not to place a maximum over all mark locations inside the expectation: the estimate is uniform in a prescribed mark.

Points for specialist verification are the pathwise localization of the two-sided difference by the four deterministic maxima, including windows crossing collision time zero, and the use of the cumulative-return tail on the unbounded far shells. The text states both mechanisms explicitly, and I found no decisive gap.

## 9. Audit of all fixed marked Gaussian moments

For a real direction `xi`, the deterministic collision sum is handled by cumulants. A mixed cumulant containing one centered mark `a-alpha` and `j` copies of the centered collision observable has exponential diameter decay and is absolutely summable over the other anchored time indices. Thus the cumulant involving the marked factor and the interval sum is bounded independently of interval length.

In the finite moment-partition expansion:

- the block containing the centered mark must contain at least one collision factor;
- every other nonzero block contains at least two collision factors because the observable is centered.

There are therefore at most

\[
 \left\lfloor\frac{d-1}{2}\right\rfloor
\]

remaining blocks that can contribute a factor of interval length. For the unweighted moment, pair partitions give the Gaussian term in even degree; every covariance correction or nonpair partition reduces the power of `m` by at least one. In odd degree, at most `(d-1)/2` nonzero blocks occur and the Gaussian moment vanishes.

This gives the deterministic parity rates

\[
 m^{-1/2}\quad\text{for odd }d,
 \qquad
 m^{-1}\quad\text{for even }d.
\]

The actual stopping replacement is bounded using

\[
 \|x^{\otimes d}-y^{\otimes d}\|
 \le C_d|x-y|(|x|+|y|)^{d-1}
\]

and Holder's inequality, together with the fourth-root comparison and fixed `d`th moments. After normalization the stopping loss is `O(n^(-1/4))`.

The normalization is coherent:

\[
 m_k+m_{n-k}=n/c_*+O(1),
 \qquad
 D_R=c_*^{-1}\Gamma_R.
\]

The theorem therefore identifies every fixed marked tensor moment with the Gaussian tensor moment. At degree two it improves the actual covariance and exact Cesaro identity from the prior `n^(-1/6)` rate to `n^(-1/4)`.

I found no decisive combinatorial or normalization error. The theorem is explicitly fixed-order; constants may depend on `d`, and no moment-determinacy or growing-degree conclusion is inferred. The mixed-cumulant extension to heterogeneous observables is load-bearing and should be checked by an independent specialist, particularly with a discontinuous section-supported mark handled through bounded variation.

## 10. Audit of the rate-preserving frequency balance

Revision 24 chooses

\[
 \varepsilon_\natural=\frac{67}{1400}.
\]

The corresponding physical exponent is

\[
 \frac12-\varepsilon_\natural=rac{633}{1400}.
\]

With coarse smoothing `delta=n^(-1/5)/4`, fine smoothing `epsilon=n^(-3)/4`, and spectral degree nineteen, the two damping-domain margins are

\[
 \frac{73}{1400}
 \quad\text{and}\quad
 \frac{97}{700}.
\]

After integration over the four-dimensional rescaled ball, the nondamped errors have decay exponents:

| Term | Decay exponent |
|---|---:|
| fine insertion smoothing | `983/350` |
| fine residual replacement | `233/200` |
| paired fourth-order residual | `3/175`, with `log^2 n` |
| connected fourth-order residual | `143/175`, with `log^3 n` |
| multiscale stopping | `3/280` |

The identity

\[
 \frac14-5\frac{67}{1400}=rac3{280}
\]

selects the new radius at which the stopping contribution preserves the inherited central power. The paired residual exponent exceeds `3/280` by

\[
 \frac{9}{1400},
\]

which is sufficient to absorb its logarithmic square.

The raw factor `n^2` is exactly canceled by the four-dimensional Jacobian under `v=sqrt(n) z`. The damped polynomial term is exponentially small on the annulus because its rescaled inner radius is `n^(1/200)`, so the damping exponent begins at order `n^(1/100)`.

I independently checked these rational exponents and found them correct.

The result improves revision 22 in two distinct ways:

1. it extends the fixed-count radius from rescaled exponent `1/50` to `67/1400`;
2. it restores the original principal central rate rather than retaining the slower `n^(-1/200)` rate of revision 22 or the `n^(-5/861)` rate of the recovered v23 theorem.

The manuscript correctly states that this balance is not an optimality theorem. It also correctly states that it does not reach the target rescaled exponent `1/10`.

## 11. Audit of same-event conditioning and marked moments

For a marked-state event with probability `p_n` and zero-extension variation `V_n`, the wider-band comparison is divided by the exact same probability appearing in the numerator. No event is replaced and no independence of return observations is assumed.

The preserved central-rate budget is

\[
 \beta<\frac3{280},
 \qquad
 \beta+\kappa<\frac9{175},
\]

when

\[
 p_n\ge cn^{-\beta},
 \qquad
 V_n\le Cn^\kappa.
\]

The moment theorem separately permits the broader fixed-moment requirements

\[
 \beta<\frac14,
 \qquad
 \beta+\kappa<\rho_d.
\]

For convergence of every fixed polynomial moment and the conditional covariance, the stated common condition

\[
 \beta<\frac14,
 \qquad
 \beta+\kappa<\frac12
\]

is sufficient. These are same-event statements, not relative comparisons between completed-return and physical-time events.

The manuscript also keeps the insertion classes distinct. The Fourier and moment theorems require bounded variation. The exact finite-count raw extraction additionally requires finite-record subanalytic admissibility. Arbitrary `L2` weights from the averaged theorem, logarithmic return-window events, and exact physical observation indicators are not silently identified with this intersection class.

## 12. Audit of the new-kernel raw identity

The physical cutoff is

\[
 B_n^\natural=n^{-633/1400}.
\]

The exact raw decomposition uses the corresponding kernel in every term. In particular, the local edge correction is defined anew as

\[
 \mathcal E^{\natural,a,L}_{n,k,R,A}
 =\operatorname*{ess\,sup}_{\mathcal W_{n,R,A}}
 |e^{a,L}-K_n^\natural*E^{a,L}|.
\]

It is not imported from either earlier cutoff.

For the high-count measure, the kernel scale gives

\[
 n^2(B_n^\natural)^4=n^{67/350},
 \qquad
 nB_n^\natural=n^{767/1400}.
\]

Hence the count-separated convolution is bounded by

\[
 C_J n^{67/350-767J/1400},
\]

and can be made smaller than any prescribed inverse power by selecting the fixed Schwartz order `J`.

The omitted Gaussian frequencies begin at rescaled radius `n^(67/1400)` and contribute

\[
 Ce^{-cn^{67/700}}.
\]

The remaining exact raw terms are

\[
 n^2\mathcal E^{\natural,a,L_n}_{n,k,R,A},
\]

\[
 (2\pi)^{-4}n^2\mathcal C^{\natural,a,L_n}_{n,k,R}(B),
\]

and

\[
 \frac{n^2}{\pi B}A_2(n,L_n,R,w_{n,k,R}).
\]

The manuscript retains their true `n`, parameter, weight, and kernel dependence and interprets the inequality in the extended reals if the local edge quantity has not been bounded. This is the correct level of honesty.

## 13. What revision 24 closes from the preceding report

Revision 24 materially closes or improves the following points.

### 13.1 The first-order unsmoothing bottleneck

Lower residual orders are no longer estimated absolutely before damping. The cubic correction keeps them inside the full damped collision word, leaving only a small-mass fourth-order remainder.

### 13.2 The single-window stopping loss

The stopping comparison is no longer optimized through one global exceptional window. Multiscale shells yield the fourth-root rate in every fixed finite `L^q` norm and eliminate the slower `p/(4p+1)` principal rate.

### 13.3 The prescribed-count Fourier radius and principal rate

The fixed-count region is extended to rescaled exponent `67/1400`, and the old `n^(-3/280) sqrt(log n)` central rate is preserved.

### 13.4 Fixed marked polynomial moments

The paper now proves every fixed marked Gaussian tensor moment, not only moments through degree four, and improves actual covariance/Cesaro convergence.

### 13.5 Weighted exact raw bookkeeping

The wider central estimate is inserted into an exact marked raw identity with the matching kernel, while all unresolved terms remain visible.

These are significant achievements. They do not, however, close the remaining raw theorem.

## 14. Remaining fixed-count complementary-frequency problem

The new outer physical radius is

\[
 n^{-633/1400}\approx n^{-0.45214}.
\]

The previously targeted small-frequency regime reaches

\[
 n^{-2/5}=n^{-0.4}.
\]

Equivalently, the proved rescaled radius is

\[
 n^{67/1400}\approx n^{0.04786},
\]

while the contemplated endpoint is

\[
 n^{1/10}.
\]

The remaining gap in the rescaled exponent is

\[
 \frac1{10}-\frac{67}{1400}=rac{73}{1400}>0.
\]

The manuscript still needs a fixed-count estimate for:

1. the farther small annulus from the new cutoff toward `n^(-2/5)`;
2. compact nonzero lattice/count torus frequencies;
3. the relevant full peripheral return phases;
4. growing roof frequencies;
5. the transition to the far-roof derivative estimate;
6. a strict common splice with all actual constants and weight losses.

The averaged direct-orbit theorem, cyclic arc bounds, exterior Abel estimate, and fixed-test-frequency spectral Cauchy law do not supply the missing fixed-count integral. The local compressed-resolvent route retains its displayed scale incompatibility. The present finite-order scheme itself is only a sufficient method and is not claimed to reach the target endpoint.

## 15. Remaining long-time raw-density estimates

The finite-count structural extraction is complete for every fixed packet. At the linear cutoff

\[
 L_n\asymp n,
\]

the raw theorem still requires a radius-uniform growth estimate for

\[
 A_2(n,L_n,R,w)
 =\sum_\ell
 \|\partial_t^2 r^{w,L_n}_{n,R}(\ell,\cdot)\|_1.
\]

Fixed-packet finiteness does not control:

- the number of singular cells;
- prepared rational exponents and their distance from threshold values;
- germ radii;
- power-logarithm coefficients;
- logarithmic degrees;
- coalescing critical values;
- inverse-coarea Jacobians;
- regular-interval derivative integrals;
- the dependence on the radius and the weight class.

The new collision cumulant and stopping estimates concern bounded collision observables. They do not estimate these pushforward-density derivatives.

A second unresolved term is the new-kernel local edge correction

\[
 n^2\mathcal E^{\natural,a,L_n}_{n,k,R,A}.
\]

The exact extraction includes every finite-packet singularity, but the manuscript has not shown that the combined extracted density minus its convolution is negligible on the actual central windows at the new scale.

The finite-band residual integral must also be bounded jointly with the far-roof choice `B`. All three terms need compatible estimates, not independent qualitative finiteness statements.

## 16. Weighted raw theory and exact physical conditioning

The same-event marked theorems are valuable, but the final physical conditioning application remains incomplete.

It still requires:

- the full weighted fixed-count complementary integral for the actual downstream indicator class;
- a weighted long-time `A_2` estimate;
- a weighted local edge estimate;
- a raw-scale asymptotic lower bound for the identical exact denominator;
- a relative comparison between the completed-return event and the exact physical-time/lattice observation event.

An absolute unfinished-return error, even one with strong moments, cannot be discarded under a rare exact lattice constraint without a relative event estimate. The new multiscale theorem compares clocks in `L^q`; it does not perform this event replacement.

The manuscript correctly preserves the distinctions among:

- a single bounded-BV actual-return mark;
- an arbitrary `L2` weight in a return-count average;
- a logarithmic window of actual-return observations;
- a finite-record subanalytic weight for raw extraction;
- an exact physical-time/lattice event.

A future proof must identify an insertion class stable under every required raw operation or prove separate estimates for the actual physical class.

## 17. Top-four significance assessment

The manuscript now contains a large unconditional body of mathematics:

- Gaussian and functional limits for an actual unbounded return record;
- growing central and fixed-count Fourier bands;
- initial, terminal, intermediate, and logarithmic-window observations;
- all fixed marked Gaussian moments;
- actual covariance convergence;
- uniform joint nondegeneracy;
- complete measurable phase arithmetic;
- quantitative collision and return defects;
- exact peripheral phase lifting;
- finite-rank compression and an explicit diagnosis of its scale boundary;
- complete structural finite-count raw extraction;
- exact count-localized raw identities;
- direct uncompressed averaged-orbit and cyclic spectral estimates;
- damped cubic unsmoothing and rate-preserving fixed-count cancellation.

Several ideas are independently interesting. The bounded collision compensation, measurable phase rigidity, actual tower lifts, observed-count localization, and damped finite-order unsmoothing are particularly notable.

At the requested four-journal standard, however, the paper is still organized around a raw mixed-density LLT whose decisive outer and density estimates remain open. The manuscript is also tied to one highly engineered triangular Lorentz family. It has not yet extracted a broad theorem with multiple substantially different applications that could replace completion of the advertised endpoint as the source of top-four breadth.

I therefore do not regard revision 24 as meeting the closure and breadth threshold of *Annals*, *Acta*, *Inventiones*, or *JAMS*.

A specialist-paper reorganization around the unconditional results could be compelling, especially after independent billiards and anisotropic-operator review. If the authors retain the current raw-LLT organization, the remaining estimates must be proved rather than left as exact interfaces.

## 18. Required work before another top-four review

### A. Close the full fixed-count Fourier complement

Prove an integrated estimate for the actual full-law or edge-subtracted residual transform from the new cutoff through:

- the farther small annulus;
- compact nonzero torus frequencies;
- the relevant full return peripheral phases;
- growing roof frequencies;
- the far-roof splice.

The estimate must hold at the specified return count and with the raw normalization. Averaged coefficients, function defects, finite matrices, or cyclic-vector arc masses are not substitutes.

### B. Prove uniform long-time finite-count preparation bounds

Quantify the finite-count constructible extraction when `L_n` is proportional to `n`. Bound the complete second-derivative sum with its true dependence on the radius, count, singular cells, germ data, and admissible weight.

### C. Bound the new-kernel local edge correction

Prove that

\[
 n^2\mathcal E^{\natural,a,L_n}_{n,k,R,A}\to0
\]

on the actual central windows for the required unweighted and weighted classes. The estimate must use the new kernel rather than an earlier cutoff.

### D. Complete the weighted raw denominator theory

For the downstream observation class, prove weighted versions of the full complement, derivative budget, and local edge estimate, together with the exact raw denominator asymptotic.

### E. Prove relative physical-event replacement

Compare the completed-return event with the exact physical-time/lattice event at the scale of the true rare-event probability. Preserve the exact lattice coordinate and continuous window; do not infer the comparison from an absolute stopping or unfinished-block estimate.

### F. Obtain independent specialist review

At minimum, independent experts should examine:

- the local collision-space chronological product with repeated and endpoint multipliers;
- the small-mass cumulant and fixed even maximal arguments;
- the two-sided dyadic-shell clock comparison;
- the mixed marked-cumulant summability and parity count;
- the finite spectral-jet and real-frequency damping inputs;
- the complete finite-count constructible preparation;
- the future outer-frequency and local-edge estimates.

### G. Reorganize if the raw endpoint is not completed

If the remaining raw estimates are not supplied, present the completed Gaussian, moment, phase, fixed-count central-band, and finite-extraction theorems as the actual main results. The raw LLT should then be separated as a precise future theorem or conditional interface.

## 19. Presentation and technical comments

1. Keep the v23 chronology explicit. The existing v23 branch contains an assembly commit, not the attached ordinary manuscript; future readers should not infer a missing referee decision.
2. State the final ordinary paper tree and controlling report near the source manifest and response, as the current revision does.
3. In the multiscale stopping theorem, retain the distinction between uniformity in a prescribed mark and an expectation of a maximum over all marks.
4. Keep the two clock-tail bounds separate. The polynomial bound handles moderate shells; the exponential estimate is only invoked after the threshold exceeds a sufficiently large fixed multiple of `n`.
5. State explicitly that `p` in the shell proof is selected after the fixed desired `q`; no constants are uniform as moment order grows.
6. In the mixed marked-moment proof, expand one representative heterogeneous cumulant comparison in full. This would make the extension from identical collision factors easier to audit.
7. Retain the parity definition of `rho_d` beside every all-moment statement.
8. Continue to distinguish collision covariance absolute summability from the induced Cesaro identity; no absolute induced Green--Kubo series is proved.
9. Keep the coarse smoothing scale, fine insertion scale, spectral degree, clock moment order, and residual Taylor degree notationally separate. They play different roles.
10. Beside every wider-band theorem, display both the physical and rescaled radii.
11. Do not describe the new band as the full annulus. Its rescaled endpoint is `67/1400`, not `1/10`.
12. Keep the old sharper small-ball theorem as a separate statement rather than replacing it by the wider-band result.
13. In the raw theorem, define the edge correction with the active kernel immediately before use. The current revision correctly recomputes it.
14. Keep the finite-record subanalytic requirement distinct from bounded variation and arbitrary `L2` weights.
15. State that the local edge term may be unbounded before germ estimates; this prevents a structural identity from being mistaken for a proved asymptotic.
16. Retain the exact count-separation exponents for the new kernel.
17. Do not use the spectral Cauchy limit at test frequency growing with `n` without a separate uniform theorem.
18. Record explicitly that successful CI establishes source/build execution, not the continuum proof.
19. The article is now very long. A dependency chart separating unconditional theorems, raw interfaces, and remaining assumptions would materially help readers.
20. A final top-four submission should include an independent expert statement or a detailed source map for every external billiard/anisotropic theorem used in the load-bearing chain.

## 20. Verification boundary

I reviewed the frozen revision-24 source identity, the controlling revision-22 report, the recovered v23 source history, the four new mathematical modules, the proof ledger, source manifest, response, input maps, validation record, branch identities, and exact GitHub Actions results.

I checked the principal algebra and exponent balances independently, including:

- the small-mass cumulant logarithmic power;
- the dyadic maximal-moment summation;
- the higher-moment clock exponent;
- the multiscale shell exponent `3q/2-2p`;
- the fourth-root stopping scale;
- the parity count in marked moments;
- the damping-domain margins `73/1400` and `97/700`;
- the five integrated error exponents in the rate-preserving band;
- the four-dimensional raw Jacobian;
- the new-kernel count-separation powers.

I did not independently reconstruct every inherited singularity estimate, reproduce the full anisotropic collision-space theory, formally verify the constructible preparation, or certify every proof in the  revision history. I also did not establish any of the remaining outer-frequency, long-time derivative, local-edge, or physical-event estimates.

Finite diagnostics and native TeX checks can verify source identity, finite algebra, exponent arithmetic, and build reproducibility. They cannot prove hyperbolic product structure, collision-space spectral estimates, continuum cumulant bounds, constructible uniformity, the full complementary integral, or journal acceptance.

This report is therefore a mathematical and editorial referee assessment at the requested standard, not a formal proof certificate.

## 21. Final conclusion

Revision 24 makes substantial and credible progress. The recovered v23 argument repairs the first-order unsmoothing bottleneck by retaining a cubic correction inside fully damped chronological words. The new multiscale proof gives fourth-root stopping, the all-moment theorem extends Gaussian moment identification to every fixed marked tensor degree, and the rate-preserving band pushes the prescribed-count raw region outward while retaining the inherited central rate.

I found no decisive counterexample in these new proof chains. The source is frozen coherently and the exact qualification succeeds on both author branches.

Nevertheless, the full fixed-count complement, the long-time finite-count second-derivative budget, the new-kernel local edge correction, the weighted raw denominator theory, and exact physical-event replacement remain unproved. These are central pieces of the raw mixed-density local limit theorem around which the article is organized.

For those reasons I recommend rejection at the requested top-four benchmark in the present form, while recognizing revision 24 as a major mathematical advance and a potentially strong specialist contribution after independent expert verification and suitable reorganization.