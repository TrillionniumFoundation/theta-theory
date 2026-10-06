# Response to the substantive referee: A2-DYN revision 13

**Article:** Qian Qi, *Collision records, arithmetic, and raw local inversion in a triangular Lorentz gas*  
**Revised source:** `papers/A2-DYN-v13-referee-response`  
**Controlling report:** `reviews/a2-dyn-v11-substantive-top4-review-2026-10-06/REFEREE_REPORT.md`  
**Report commit:** `fd84da57359a3ad2fefed532b0b5094ab8c6e436`  
**Reviewed v11 source:** `dfacd56110f80a9621671028d2aa0a5782659055`  
**Immediate v12 baseline:** `13b088e47bfbe8d46313b00bb97bc92a235a2376`

We thank the referee for distinguishing the marked central theorem from the raw density endpoint and for identifying the exact-source defects. Revision 12 supplied the repaired source packet. Revision 13 adds a new proof of moment identification for the same physical record. It retains the title, family, raw mixed-density target, periodic geometry, exact critical-edge subtraction, inversion statements, and all inherited theorem-level content. It does not substitute a different topic or a different conditioning event.

## A. Exact source and native build

The immediate baseline has a successful exact-source workflow: run `37399143352`, event SHA `13b088e47bfbe8d46313b00bb97bc92a235a2376`, artifact `11384359352`, archive digest `sha256:064604c3ed2aab67292133b5d52aa8abe98c5970f0a4f0b3dd24f2e62d063714`. This is evidence for v12 only. It is not used as evidence that v13 passed.

Of the 29 v12 core files, 28 are byte-identical in v13. The remaining file, `core/15_exponential_returns.tex`, differs by exactly the deletion of a stray plus after `\end{proof}`. This is an explicit typesetting repair, not an unreported preservation claim. All inherited Python diagnostics and the bibliography are unchanged. The new manifest records the actual source hashes. The new workflow checks the event SHA and clean source, runs the diagnostics normally and with `-O`, builds the full article, and emits the PDF hash and exact run ID dynamically. The failed v11 packet is not rewritten.

## B. Covariance: a new actual-moment theorem

The new section `sec:unsmoothed-moments` resolves a distinction left explicit in the earlier proof: a weak Gaussian covariance had not yet been identified with the limit of the actual normalized second moments.

The proof has six steps, all in the article.

1. `lem:bv-finite-product` smooths two to four bounded-variation factors at a scale chosen from a single deterministic collision gap. The chronological operator word costs at most `epsilon^(-2q)`; balancing this against the smoothing error gives exponential finite-product decoupling. No variation norm of a long pullback is used.
2. `prop:unsmoothed-fourth` splits ordered four-point functions at each of their three gaps. The paired term sums to `O(m^2)` and the connected remainder to `O(m)`. A dyadic `L4` argument gives a maximal fourth-moment bound with no logarithmic loss.
3. `lem:fourth-clock-window` applies that bound to the section visit count. Its actual forward/backward clock probability is `O((j+b)^2/b^4)`.
4. `thm:marked-L2-stopping` uses the existing cumulative-return exponential tail to control the unbounded stopped sum on exceptional events. With `b=n^(2/3)` it proves an `L2` normalized stopping error `O(n^(-1/6))`, uniformly in the mark and radius.
5. `lem:quadratic-collision-insertion` sums centered three-point correlations. The correction from a single insertion at any deterministic collision origin is `O(M_a+V_a)` even for the quadratic moment.
6. `thm:marked-quadratic-moments` transfers this estimate to the actual return mark. In particular, `n^(-1) E[U_n tensor U_n] = D_R + O(n^(-1/6))` uniformly in the physical parameter. Theorem D states this conclusion in the introduction.

The induced Green--Kubo expression now converges with the actual Cesaro lag weights, at the same rate. Absolute convergence of the induced series is not assumed or asserted. Thus the covariance identification does not depend on a new induced-mixing theorem.

This advance does not by itself prove a positive lower eigenvalue bound. The referee's periodic-representative objection remains valid: an `L2` transfer function is not evaluated at a periodic point. The explicit rank and coercivity results are retained, and no periodic regularity conclusion is smuggled into the new moment argument.

## C. Complementary frequencies

The fourth-moment clock window also improves the marked characteristic stopping comparison to `O(M_a(1+|v|)n^(-2/9))`, by taking `b=n^(5/9)`. On the inherited four-dimensional central ball its integrated stopping terms decay faster than `n^(-3/280)`. The new proof therefore preserves, and strengthens a component of, the established marked band.

This does not estimate the transform itself throughout the complement. The physical radius is still `2n^(-99/200)`, not `n^(-2/5)`. The intervening annulus, nonzero torus frequencies, growing roof frequencies, and far tail remain explicitly required by the same raw inversion theorem. No gap is hidden by changing the cutoff variable.

## D. Complete raw branch sum

The raw edge, localized inversion, and absolute residual-sum sections are retained. The new fourth moments are moments of a collision sum, not variation estimates for inverse-coarea densities. They cannot replace extraction of every nonintegrable critical/singular jump or control the total second-derivative sum. Those obligations remain stated for the original full measure, with its actual return-count dependence.

## E. Marked conditioning and exact physical events

`cor:marked-conditional-moments` adds first, second, and covariance limits under exactly the same single marked-state event as `cor:marked-state-conditioning`. If the event probability is at least `c n^(-beta)` and its indicator variation is at most `C n^kappa`, the second moment converges when `beta<1/6` and `beta+kappa<1`; the mean and conditional covariance converge when `beta<1/6` and `beta+kappa<1/2`. In particular the entire event class of the earlier central theorem satisfies these moment conclusions.

The numerator uses the exact same indicator and the denominator is its exact invariant probability. No rare-event replacement is performed. A multiple-time path event or an exact final lattice/time constraint is not declared to belong to this insertion class. The weighted complementary integrals, raw edge estimates, and relative event-replacement estimate needed for the full physical conditioning application remain separate.

## F. Source imports and independent review

The new proof uses the already stated collision-space spectral splitting, smooth multiplier bound, mean-preserving BV approximation, and cumulative-return tail. The existing source-to-norm appendix remains intact. It introduces no additional external regularity theorem and no spectral gap for the induced map. The finite diagnostics check algebra, source identity, and finite models, not continuum billiard estimates. Independent specialist review has not been obtained in this author revision.

## Presentation comments 1--10

Theorems C and D both state the unnormalized restricted-collision convention; the normalized probability is obtained with `a=s_R`. The separated supremum/variation bounds remain primary. Backward-clock endpoints and empty intervals are defined before use. Terminal-state insertions, path events, and exact physical observations remain distinguished. The article assumes no induced mixing. Both cutoff scales are displayed. The identity-notice report is not described as mathematical acceptance; the publication metadata makes no journal or proof-certification claim. Dynamic build receipts, rather than assertions in prose, identify the exact successful run and PDF.

The new revision is offered for a further substantive review of the added moment and stopping proofs together with the retained raw-density program.
