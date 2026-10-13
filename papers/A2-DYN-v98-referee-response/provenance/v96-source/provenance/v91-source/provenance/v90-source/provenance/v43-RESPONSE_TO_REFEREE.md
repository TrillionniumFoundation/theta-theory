# Response to the external referee: A2-DYN revision 43

**Article:** Qian Qi, *Collision records, arithmetic, and raw local inversion in a triangular Lorentz gas*.  
**Controlling report:** v42 external top-four report, `reviews/a2-dyn-v42-external-top4-review-2026-10-08/REFEREE_REPORT.md`.  
**Frozen review commit / blob:** `1d854ffbf468393c80e4f1bb744bfdadbb3e15a8` / `a41ef7c5d55ae4db201176892b286ba99ea84f31`.  
**Author baseline:** `7e155f0fda2a7a5f77a061ed5b54cab5943fb24b`.  
**Revised article:** `papers/A2-DYN-v43-referee-response/main.tex`.

We thank the referee for distinguishing the new finite Morse packet from a full-source raw-density theorem. We retain the title, the actual four-coordinate record, the arithmetic main term, the exact conditioning events and the original pointwise target. This revision takes a different route to the common correction: it uses the complete boundary germs already established by the finite-graph theory, fixes every actual count component before extraction, and proves a summable correction and a coefficient-first pointwise inverse for the entire law. It does not rename the guarded packet as the full source.

## 1. Omitted source and its pointwise role

Modules 92--93 eliminate the omitted source from the new *exact reconstruction*. At a label `(k,m)`, the complete finite graph at cutoff `m` is already the whole component: no larger collision count can contribute to it. Its constructible density includes grazing, singular itinerary and section-decision boundaries through its exact source domain. Every one-sided power--logarithm germ of exponent at most one is subtracted, not just a positive-margin Morse jet. The residual is W21 at that label.

Thus the new identity is `mu=E+Q`, with no positive boundary remainder `r`. Its finite roof inverse has a certified pointwise error on that component. This does not assert that the omitted source of the old guarded construction is small in supremum; it accounts for that source in the new complete germs. The next local-limit estimate is explicitly the full signed correction in Theorem `thm:v43-arithmetic-raw-criterion`, not an L1-to-supremum inference.

## 2. Long-time parameter ledger

The localization has a prescribed mass budget `epsilon_n=(1+n)^(-P-3)`. Each component receives `epsilon_n b_l`, where `b_l` is its exact reference probability. Its coefficients are unchanged and its support alone is reduced. The proof gives total correction mass at most `epsilon_n`, uniform in the radius, and an exponentially controlled count tail.

The reconstruction accuracy is independently set to `delta_n=(1+n)^(-P-3)`. The exact sufficient roof band is

`Lambda_l=max(1,A2_l/(pi delta_n b_l))`,

with null components set to zero. Therefore the sum of labelwise essential-supremum errors is at most `delta_n`. Central labels are all retained by

`L_n=ceil(lambda n+(P+4)/c0 log(2+n))`,

where `lambda>max(c^(-1)+1,a/c0+1)`. Restricting by count creates no tail density at a retained label. The count-tail variation is separately bounded.

This closes the *reconstruction* ledger in terms of actual finite germ budgets. It does not bound those budgets by a polynomial or prove the smallness of the growing-band signed inverse. The distinction is stated immediately after the new corollary, not hidden in metadata.

## 3. Growing bands

The new fixed-band central calculation uses one fixed `B`. The variable `Lambda_l` appears only in an exact coefficientwise reconstruction and its elementary Fourier-tail certificate. It is never substituted into a fixed-band operator estimate. The finite remainder certificate reduces the long-time raw problem to a specific full-source integral with a prescribed truncation error, but does not assert that this integral is already negligible. A quantitative growing-band estimate, or an alternative direct cancellation estimate, is still needed there.

## 4. A convergent common correction

This is the principal new theorem. For each fixed n,R and one bounded finite-record subanalytic weight, Lemma `lem:v43-small-jet-mass` localizes every intrinsic singular jet to any prescribed mass. Theorem `thm:v43-complete-correction` allocates that mass against the actual component probabilities and proves absolute total-variation convergence over all labels. It also proves exact restriction compatibility at every cutoff, an exponential count-tail bound, and a common holomorphic tube for the correction and residual transforms.

The series includes singular boundary germs; it is not limited to positive-margin words. Coalescing roof values are combined before extracting the intrinsic germ. No separation denominator is introduced. The common correction is a localized power--logarithm density of the complete component. We do not identify it with the old unlocalized exponential two-jet word series, whose absolute coefficient summability is not proved here. The measure-level convergence and the remaining pointwise smallness have separate flags and separate theorem statements.

## 5. Arithmetic main term

The new raw criterion uses the radius-uniform evaluated kernel `mathcal L_{m,R}` as its main term. At a fixed radius it specializes to `c mathfrak a_R g_{Omega_R}`, or `mathfrak a_R g_{D_R}` in return normalization. It does not require concrete residues to vanish. A zero residue means an exactly null component and is treated as such. No finite packet is substituted for a prescribed singleton, and no conditional law is attached to a zero denominator.

Theorem `thm:LLT` is retained as the historical unmodulated sufficient criterion. The new arithmetic criterion is the explicitly stated general form appropriate to the actual section. Triviality of the concrete arithmetic factor is not asserted.

## 6. Full roof complement

The new coefficient-first formula includes every roof frequency and every source class at the specified label. Joint integrability of the full mixed transform is not inferred from componentwise integrability. The torus coefficient is taken first, where the count series is absolutely convergent; only then is its roof transform inverted absolutely.

For a fixed `B`, the complete signed correction is exactly `p-K_B*p`, independently of the chosen germ radii. The central term `K_B*p` has the already proved uniform transition expansion. Consequently smallness of the full signed correction is necessary and sufficient for the pointwise arithmetic transition LLT. Its finite-integral version has error at most `delta_n`. We have thereby supplied one exact full-source remainder, but have not proved its central-scale vanishing. All critical and boundary effects remain inside it.

## 7. Independent review

No independent human specialist audit was obtained. `SPECIALIST_AUDIT_MAP.md` specifies the finite-graph, germ, count-summation, inversion-order and arithmetic checks, and retains the inherited anisotropic and geometric verification obligations. The new proof relies on the primary Cluckers--Miller integration/preparation theorem only for the finite component germs already used in module 40. Its primary text was rechecked; no long-time growth estimate is attributed to it.

## 8. Novelty and relation to the historical pipeline

The one-variable constructible preparation theorem, finite component extraction, and the fixed-band arithmetic interval theorem are not claimed new in this revision. The new mathematical step is a count-compatible full-source correction with arbitrary mass allocation, its absolute convergence and exponential moments, followed by an inversion order that does not require joint Fourier L1. This removes the lack of a common complete correction as a measure without claiming the unresolved smallness of that correction. The new arithmetic criterion uses the evaluated transition kernel rather than an unevaluated induced operator hypothesis.

No claim of top-four acceptance or historical priority is derived from these statements. They are offered as a direct advance on the original raw-return problem for the next referee to test.

## 9. Article structure and preservation

The abstract and an article-level full-source route point directly to modules 92--93. The seven inherited principal statements, all 91 old core modules, the bibliography, all inherited diagnostic scripts, all mathematical labels and the compiled A--X synopsis remain. The previous front matter and source records are archived under `provenance/V42_`. No theorem is deleted or silently weakened, and no stationary theorem is called the full raw-return theorem.

## Technical comments

The reconstruction uses `Lambda_l` for the roof bandwidth and leaves `B_m,C_m` for derivative entries. The complete physical source remains normalized by the actual section probability; the inherited Morse coefficient retains `(4 pi c)^(-1)`. At finite jumps the right trace is used; divergent germs are not assigned an artificial finite value. Null label components are zero. Every retained finite packet has n<=L. Preparation budgets retain their real size. Strong phase sources are not asserted to be multipliers; fixed-radius posterior labels and their positive-class bridge remain unchanged. The common all-boundary correction does not imply a prescribed shrinking-interval LLT or a pointwise-roof-conditioned bridge.

The new two-branch workflow must qualify the actual final SHA. A successful run, a generated PDF and finite models are not continuum proof certificates. The final receipts are read back after execution rather than predeclared successful in this response.
