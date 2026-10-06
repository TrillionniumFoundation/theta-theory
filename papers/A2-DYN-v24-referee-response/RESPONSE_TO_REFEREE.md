# Response to the latest substantive referee: A2-DYN revision 24

**Article:** Qian Qi, *Collision records, arithmetic, and raw local inversion in a triangular Lorentz gas*  
**Active manuscript:** `papers/A2-DYN-v24-referee-response`  
**Controlling report:** `reviews/a2-dyn-v22-external-top4-review-2026-10-06/REFEREE_REPORT.md`  
**Report commit / blob:** `d21f74a59eed269c4b215c53b85434a3a449c779` / `b5e96b424ca9d73fc1c113142556cc8913281ca7`  
**Reviewed v22 source:** `a656998fee8176316850ef87ac447970d712aae2`  
**Recovered v23 paper tree:** `37e6f9a75ad1a6bb4f2c8710494cc50edac9e7c9`  
**Recovery commit on the new branch:** `699f17e6bd75c3c8a741a9f00837ab4654e8c3d1`

We thank the referee for distinguishing a prescribed-count raw integral from averaged or function-defect statements, and for identifying the first-order unsmoothing loss. The complete v23 source had been staged as immutable Git objects but was not attached as an ordinary manuscript at the v23 branch head inspected here. We preserve that exact source on the new v24 branch and continue its mathematics. We do not invent a v23 referee assessment or alter the existing v23 branch.

Relative to the reviewed v22 article, the retained v23 sections replace first-order unsmoothing by a cubic correction inside the damped collision word and control its small-mass fourth-order remainder. The present revision adds a separate multiscale stopping proof and all fixed marked moments, then derives a wider band with the original central error rate. All earlier core modules, theorem statements and bibliography remain. The physical record and the raw mixed-density objective are unchanged.

## A. The prescribed-count complement

### A.1. A new multiscale comparison of the actual clocks

Theorem `thm:multiscale-marked-stopping` proves, for every fixed finite `q>=1`,

`||Z_n,k,R-W_n,k,R||_q <= C_q n^(1/4)`,

with uniformity in the radius and the prescribed mark. Here `Z` is the exact two-sided collision sum obtained by recentering at the actual return, and `W` is its deterministic Kac-scale counterpart. It is not a maximum over all marks inside the expectation.

The difference is localized on disjoint shells of the total clock deviation. The first shell has width `ceil(sqrt(n))`. On a shell of width `L`, a deterministic collision maximum supplies the bound, and Holder's inequality combines it with the actual clock probability. With a fixed integer `p` satisfying `2p>3q/2`, the moderate-shell contribution is at most

`C n^(p-q/2) L^(3q/2-2p)`.

Summing dyadically from `L~sqrt(n)` gives `C_q n^(q/4)` because the shell exponent is strictly negative. The cumulative-return exponential tail handles shells beyond a sufficiently large fixed multiple of `n`. No independence or conditional maximal inequality is assumed. At `q=2`, fourth moments suffice: the moderate contribution is `C sum n/L <= C sqrt(n)`.

Consequently the characteristic stopping error is `C M_a |v| n^(-1/4)`, with exact zero error at `v=0`. This is stronger than optimizing a single global exceptional window, even when the latter uses a high fixed moment.

### A.2. Damped unsmoothing is retained and checked, not replaced by an absolute moment estimate

The recovered `core/48_damped_unsmoothing.tex` retains the degree-zero through degree-three corrections inside full-length damped chronological words. The fine insertion scale is distinct from the coarse twisted-observable scale. Only the fourth-order residual remainder is bounded without damping. Its full small-mass bound includes both `m^2 delta^2 log^2(1/delta)` and `m delta log^3(1/delta)`.

The new proof uses this theorem with fixed spectral degree 19, coarse smoothing `delta=n^(-1/5)/4` and fine insertion smoothing `epsilon=n^(-3)/4`. It does not claim all-order analytic control, replace the genuine return mark, or infer operator decay for the unitary return Koopman operator.

### A.3. A new prescribed-count band without loss of the original central rate

The new outer rescaled exponent is `67/1400`; the physical support radius is `2n^(-633/1400)`. The analytic disk and relative Taylor-remainder margins are `73/1400` and `97/700`. The undamped integrated exponents are

| Error | Decay exponent |
|---|---:|
| Fine mark smoothing | `983/350` |
| Fine residual replacement | `233/200` |
| Paired fourth-order residual | `3/175`, with `log^2 n` |
| Connected fourth-order residual | `143/175`, with `log^3 n` |
| Actual multiscale stopping | `3/280` |

The paired residual has strict power slack `9/1400` over the stopping term. Thus the logarithms there are absorbed. The raw factor `n^2` is exactly cancelled by the four-dimensional change of variables `v=sqrt(n)z`.

Theorem `thm:rate-preserving-annulus` proves the absolute, prescribed-count bound

`n^2 integral_{2n^(-99/200)<=|z|<=2n^(-633/1400)} |Phi_n,R^[k],a(z)| dz <= C[M_a n^(-3/280)+V_a n^(-983/350)]`.

Combining it with the original marked central theorem gives, on the whole rescaled ball of radius `2n^(67/1400)`, the original error

`C[M_a n^(-3/280) sqrt(log(2+n))+V_a n^(-9/175)]`.

This both extends the reviewed v22 radius `2n^(1/50)` and removes its slower central rate `n^(-1/200) sqrt(log n)`. Theorem L and the recovered Theorem M are retained with their original valid bounds. The equality `1/4-5(67/1400)=3/280` explains the selected radius; it is not an optimality or impossibility assertion.

### A.4. Exact boundary of the new result

The theorem is for the full physical transform at the specified `n`, with one actual-return insertion. It is neither volume-normalized nor averaged over return counts. It does not control the entire complement. The farther small-frequency annulus beyond `2n^(-633/1400)`, compact nonzero torus and peripheral return frequencies, growing roof frequencies and the final roof splice still require fixed-count estimates. The previously contemplated physical endpoint `n^(-2/5)` is not included by a change of notation.

## B. Long-time raw extraction

The full finite-count constructible extraction is retained. The new clock and cumulant bounds do not control preparation exponents, germ radii, coefficients, coalescing critical values, inverse-coarea Jacobians or second derivatives when the count cutoff is proportional to `n`. The actual quantity `A_2(n,L_n,R,w)` remains in the raw estimate. Fixed-packet finiteness is not asserted to be a uniform long-time bound.

## C. The local edge correction is recomputed

The new kernel is `K_n^natural`, with physical scale `B_n^natural=n^(-633/1400)`. The edge term is defined anew as

`ess sup |e^(a,L_n)-K_n^natural*E^(a,L_n)|`.

It is not taken from either earlier cutoff. Corollary `cor:rate-preserving-raw-budget` gives the exact four-term decomposition and raw inequality. The Gaussian tail is `C M_a exp(-c n^(67/700))`. Count separation gives `C M_a n^(67/350-767J/1400)`, hence every fixed inverse power after choosing the Schwartz order `J`.

The finite-band residual integral and the far-roof term `n^2 A_2/(pi B)` remain alongside the kernel-dependent local edge correction. The inequality keeps its extended-real interpretation until the latter is bounded. No cancellation between an extracted density and its convolution is lost by splitting them apart.

## D. Marked moments and weighted raw theory

Theorem `thm:all-marked-gaussian-moments` is a second substantive addition. A single centered mark in a mixed cumulant is anchored at collision time zero. The inherited finite-order decoupling gives a summable bound over all remaining time indices, independently of the deterministic interval length. In the finite moment partition, the block containing that mark must contain at least one collision factor; all other nonzero blocks have at least two factors. This gives the correct parity-sensitive deterministic moment error.

The multiscale stopping theorem transfers it to the actual return record. For every fixed tensor order `d>=1`, the marked moment differs from its Gaussian moment by at most

`C_d[M_a n^(-1/4)+(M_a+V_a)n^(-rho_d)]`,

where `rho_d=1/2` for odd `d` and `rho_d=1` for even `d`. The normalized actual covariance and its exact induced Cesaro expression therefore converge at `n^(-1/4)`, improving the earlier `n^(-1/6)` identification. No convergence of the unweighted induced correlation series without Cesaro weights is claimed.

The same-event corollary divides by the unchanged exact probability. In particular, the original marked-band probability budget `beta<3/280`, `beta+kappa<9/175` now holds on the wider band, and every fixed conditional polynomial moment converges as well. The polynomial-moment theorem alone permits `beta<1/4`, `beta+kappa<1/2` for all fixed moments and covariance, with the stated parity refinement for a single even moment.

For the weighted raw identity, the insertion must additionally satisfy the finite-record admissibility required by the structural extraction. Arbitrary BV functions, finite-record subanalytic weights, logarithmic return windows and exact physical indicators are not identified with one another. The full weighted complement, derivative sum, edge smallness and raw denominator asymptotic are still the quantitative requirements for the downstream application.

## E. Exact physical-event replacement

No completed-return event is replaced by a physical-time/lattice observation. The new conditional results use the identical indicator and exact denominator throughout. They do not turn an absolute unfinished-return error into a relative rare-event estimate. That required comparison remains present in the original application.

## F. Independent review and presentation

The new proof imports no additional continuum theorem. Its inputs are the retained fixed-order collision cumulants, collision maximal moments, exact backward and forward clock identities, cumulative-return tail, marked recentering, and damped unsmoothing. The next referee should check the unbounded dyadic-shell sum, its Holder exponents and exponential far shells, the mixed anchored cumulants, the parity-dependent partition count and tensor polarization, and the new frequency and kernel exponents.

All fifteen presentation comments are addressed by retaining the explicit finite-order caveats, fixed-smoothing order of limits, true Taylor remainder, full chronological words, separate supremum/variation losses, both frequency scales, event classes, physical-versus-Gaussian tail distinction, and exact inherited-edit accounting. The new Theorem N is additional; Theorems A--M and all of their proofs remain in the article.

## Source and execution history

The v23 branch inspected at task start contained only the assembly commit `ca2b585c126a0f100d6ab16cb491615f7cd7c770`. Assembly run `37490787605` had created the immutable paper tree listed above. The new branch first attached that exact tree at `699f17e6bd75c3c8a741a9f00837ab4654e8c3d1`, leaving the v23 branch unchanged. The first audit run `37491888772` stopped because the audit environment lacked NumPy; it is not counted as successful qualification. The dependency was then added without changing the mathematical baseline.

All 49 recovered core modules, every inherited Python script and the bibliography are byte-identical in v24. Five exact edits occur only in `main.tex`. The new manifest is computed from the actual ordinary source, not a hand-copied hash list. The final read-only qualification checks the exact event SHA, normal and optimized finite regressions, inherited diagnostics and complete native TeX. Its dynamic receipt, not a prediction in this response, records the actual successful source and PDF. Execution checks are not formal proof certification or independent human review.
