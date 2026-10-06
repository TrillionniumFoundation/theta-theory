# Response to the latest referee: A2-DYN revision 23

**Article:** Qian Qi, *Collision records, arithmetic, and raw local inversion in a triangular Lorentz gas*  
**Active source:** `papers/A2-DYN-v23-referee-response`  
**Controlling report:** `reviews/a2-dyn-v22-external-top4-review-2026-10-06/REFEREE_REPORT.md`  
**Report commit / blob:** `d21f74a59eed269c4b215c53b85434a3a449c779` / `b5e96b424ca9d73fc1c113142556cc8913281ca7`  
**Reviewed author baseline:** `a656998fee8176316850ef87ac447970d712aae2`  
**Frozen baseline paper tree:** `48ee252fdffc68d779069ce7a6c43ac564f8217f`  
**Date:** 6 October 2026

We thank the referee for identifying the first-order unsmoothing loss, rather than the fixed Taylor degree alone, as the constraint on the preceding fixed-count band. The revision addresses that point with a new damped removal of smoothing and a higher-moment estimate for the actual return clock. The title, physical family, actual section, complete record and raw mixed-density problem remain unchanged. All prior core modules and results are retained, not replaced by a specialist-paper reorganization.

Theorem M is added to the introduction. Its complete proofs appear in `core/48_damped_unsmoothing.tex` and `core/49_wider_fixed_count_band.tex`. The former changes the comparison mechanism; the latter proves a prescribed-count raw annulus, an enlarged marked central theorem, a same-event consequence and an exact weighted raw identity for the new kernel.

## A. Rest of the prescribed-count complement: a sharper unsmoothing mechanism

### A.1. The small residual retains its mass factor in connected sums

The new `lem:small-mass-cumulants` proves that a bounded-BV observable with `L1` norm `O(delta)` has an anchored order-`q` connected-correlation sum at most `C_q delta(1+|log delta|)^(q-1)`. At every tuple the partition formula gives an `O(delta)` bound, while the inherited independent-block argument gives exponential decay in the largest gap. Summing their minimum retains the small factor. The exact translate multiplicity is bounded by the collision length, so there is no artificial boundary error independent of `delta`.

For the centered unsmoothing residual this yields the fourth moment `C[m^2 delta^2 L_delta^2+m delta L_delta^3]`. The lower, single-cumulant term is retained. The proof does not replace this by an independent-increment model.

### A.2. Keep the low-degree correction inside the damped collision word

In `thm:damped-cubic-unsmoothing`, the insertion is smoothed first, while the full exponential still has modulus one; its cost is only `epsilon V_a`. The residual phase is then expanded through degree three. Its fourth-order remainder is controlled by the preceding small-mass moment bound.

The degree-zero through degree-three terms are not bounded by their absolute moments. Instead, each is a finite sum of chronological words of the already damped coarse-scale collision operator, one fine-scale mark and up to three fine-scale residual multipliers. Their collision lengths sum to the full deterministic length even for repeated insertion times and endpoint marks. Each such term is bounded by a fixed polynomial prefactor times `exp(-c m |z|^2)`.

The fine smoothing scale regularizes only the insertions. It never becomes the smoothing scale in the twisted collision operator and therefore does not shrink that operator's analytic domain. This separation is essential. The resulting undamped observable error is quartic rather than linear in the residual sum. The article displays the chronological word and the one-insertion specialization explicitly.

### A.3. A fixed higher moment improves the genuine stopping error

`lem:fixed-even-maximal` derives every fixed even moment from the existing finite-order cumulants and gives its dyadic maximal version. With moment order `2p`, exact visit equivalences give `P(|N_j^+-floor(j/c*)|>b) <= C_p(j+b)^p/b^(2p)`, with the same backward estimate.

In `prop:higher-moment-marked-stopping`, the exceptional event costs only its probability, while the good event uses a deterministic collision-window maximum. The optimizing window is `b=n^((2p+1)/(4p+1))` and the characteristic error is `C_p M_a(1+|v|) n^(-p/(4p+1))`. This is the true two-sided stopping about the actual return mark. It is neither a return-count average nor a deterministic replacement of the mark.

### A.4. Explicit new prescribed-count bound

The concrete choices are coarse scale `delta=n^(-1/5)/4`, fine insertion scale `epsilon=n^(-3)/4`, spectral degree `Q=19` and clock moment order `20` (`p=10`). They are all fixed in advance. The outer rescaled exponent is `1/21`, so the outer physical radius is `2n^(-19/42)`.

The analytic-disk and relative Taylor-remainder margins are `11/210` and `1/7`. The integrated quartic residual margins are `2/105` and `86/105`; the fine-scale replacement margin is `7/6`, and the insertion margin is `59/21`. The slow term is the actual stopping margin `10/41-5/21=5/861`. The logarithmic factors in the fourth moment are absorbed by strict power slack.

Consequently `thm:wider-fixed-count-annulus` proves

`n^2 integral_{2n^(-99/200)<=|z|<=2n^(-19/42)} |Phi_n,R^[k],a(z)| dz <= C[M_a n^(-5/861)+V_a n^(-59/21)]`.

This is an absolute estimate for the full physical transform at the specified `n`, with no annular-volume normalization. The four-dimensional Jacobian exactly cancels `n^2`. The new theorem includes the region beyond the former `2n^(-12/25)` endpoint.

### A.5. General range and the remainder of the task

`prop:damped-unsmoothing-band-range` proves a nonempty fixed-order construction for every rescaled exponent `1/200<epsilon<1/20`, instead of the preceding `epsilon<1/42`. The proof supplies the simultaneous inequalities on the coarse scale, the fixed clock moment and the fixed spectral degree. Constants are not claimed uniform in the moment order.

This does not yet reach the physical `n^(-2/5)` endpoint (rescaled exponent `1/10`). The remaining farther small annulus, compact nonzero torus frequencies, all required peripheral phases and growing roof frequencies still require prescribed-count control. The new theorem is not presented as the entire complement, and no averaged-orbit or Cauchy-limit statement is substituted for it.

## B. Long-time finite-count extraction

The full structural extraction in file 40 is retained verbatim. The new small-mass cumulant estimates concern bounded collision observables; they do not bound prepared germ radii, coefficients, exponent gaps, logarithmic degrees, coalescing critical values or inverse-coarea second derivatives at `L_n` proportional to `n`. The actual `A_2(n,L_n,R,w)` remains in the raw budget without an asserted long-time bound.

The new weighted identity retains this exact quantity for the actual marked weight. A usable far-roof cutoff must still be chosen together with the finite-band estimate, rather than inferred merely from fixed-packet finiteness.

## C. Local edge correction for the new kernel

The new physical cutoff is `B_n^sharp=n^(-19/42)`, with support radius `2B_n^sharp`. The correction is defined afresh as `e^{a,L_n}-K_n^sharp*E^{a,L_n}`. It is not transferred from the v22 kernel and is not split in a way that loses possible cancellation.

`thm:sharp-weighted-raw-inversion` gives the exact identity and the corresponding raw inequality. The Gaussian tail is `C M_a exp(-c n^(2/21))`. Count separation gives `C M_a n^(4/21-23J/42)`, hence every fixed inverse power after choosing the Schwartz order `J`. The local-edge term is kept as a mixed essential supremum and the inequality remains extended-real until that term is estimated. All singular and image-boundary jets from the finite extraction remain included.

## D. Weighted raw theory

The new Fourier theorem allows a single BV insertion at any actual return and keeps the separated `M_a,V_a` costs. For the structural weighted extraction we require, additionally, finite-record subanalytic admissibility as defined in the inherited paper. The weight under the normalized section probability is exactly `w=c* a o F^k`; this yields the original marked measure under the restricted collision measure, with mass `alpha_a`. For `a=s_R`, the weight is one.

This explicitly identifies a common class for which the stronger central estimate, exact finite extraction and new raw identity all hold. It does not identify every BV function with a subanalytic function or every multiple-time event with a one-mark event. The weighted outer complement, derivative budget, local edge smallness and raw denominator asymptotic remain the stated quantitative tasks.

The same-event corollary on the new band divides by the exact unchanged probability. A sufficient regime is `beta<5/861` and `beta+kappa<9/175`, improving the former probability exponent `1/200` while retaining the earlier variation budget. No denominator is changed.

## E. Exact physical-event replacement

No completed-return event is exchanged for a physical-time/lattice observation in this revision. The required relative error under a rare exact constraint is not deduced from an absolute unfinished-return probability. That part of the original application remains explicitly present, with the same event and denominator to be proved.

## F. Independent specialist review

The new arguments requiring specialist checking are the small-mass anchored cumulant sum, the cubic correction with a separate fine multiplier scale, the full-length chronological damping at repeated and endpoint insertion times, the fixed twentieth-moment clock estimate, and the weighted raw normalization. The inherited collision-space and finite-extraction imports remain load-bearing. No new external continuum theorem is invoked; the existing cumulant reference remains background rather than a substitute for the printed finite-order proof. Independent human specialist review is not claimed.

## Presentation comments 1--15

Theorem L retains its inner-annulus label and original estimate. Theorem M states both new cutoffs, and the old sharper central rate remains visible. Fixed-order constants and the order of limits of the inherited spectral jet are unchanged. Its smoothing-dependent Taylor remainder is retained exactly. The new proof displays a chronological word with the mark between collision powers and explicitly handles one insertion, repeated times and endpoint marks. Real smoothed collision damping is not identified with decay of the unitary return operator.

Supremum and variation losses stay separate. The numerical ranges `1/42`, `1/20` and the remaining target `1/10` are compared explicitly. One-mark events, logarithmic return-window events and exact physical observations remain distinct. The new raw edge correction is kernel-dependent. Fixed-packet finiteness is not called uniform long-time control. The source manifest and dynamic build receipt keep execution evidence separate from mathematical proof status. All prior core files, scripts, bibliography entries and labels are preserved.

## Exact source qualification

The new branches start at the latest v22 review commit and retain its report. All 47 inherited mathematical core files are byte-identical; the only inherited mathematical-source edits are five precisely replayable changes in `main.tex`. All inherited Python scripts and the bibliography are unchanged. New finite regressions test the clock and smoothing exponents, exact moment--cumulant identities through order twenty, small Bernoulli residual identities, chronological products on a nonreversible finite-state chain, and a Taylor remainder. These tests are not continuum proofs. The full article is committed as ordinary source and is checked and compiled at an exact SHA by a read-only workflow. The dynamic receipt records the actual run, source and PDF hashes; no future execution is predeclared successful here.
