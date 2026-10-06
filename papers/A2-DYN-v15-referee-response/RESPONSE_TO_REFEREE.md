# Response to the referee: A2-DYN revision 15

**Article:** Qian Qi, *Collision records, arithmetic, and raw local inversion in a triangular Lorentz gas*  
**Active source:** `papers/A2-DYN-v15-referee-response`  
**Controlling report:** `reviews/a2-dyn-v14-external-top4-review-2026-10-06/REFEREE_REPORT.md`  
**Report commit / blob:** `43d797ce65ad5e4cf92f874a6656c9cd0af9d572` / `197a42fbe2c815860423fa405f10e96cbe82e3d4`  
**Reviewed author baseline:** `cac1a5f9ece9a8a63e69fcfb2156768337790034`  
**Date:** 6 October 2026

We thank the referee for separating the established joint nondegeneracy theorem from the quantitative mechanisms still needed for raw inversion. This revision addresses that distinction with new estimates for approximate collision phases and complex function vectors. It retains the title, physical family, actual return section, joint record and original raw mixed-density endpoint. None of the inherited theorem modules is removed. The new results appear as Theorem F and are proved in the two new sections following joint nondegeneracy.

## A. From qualitative arithmetic to quantitative phase defects

The preceding exact-phase theorem determined the roof and constant phases but did not determine every spatial circle phase. Nor did it provide a defect comparison for approximate vectors. Revision 15 adds the following proof chain.

### A.1. Complete spatial circle arithmetic

`thm:complete-physical-phase` proves that the only measurable circle solution of

`q o T_R = exp(i(u.kappa_R+s+t tau_R)) q`

has `u in 2 pi Z^2`, `s in 2 pi Z`, `t=0`, and constant q. The inherited theorem first removes t and s. At t=0 the stable and unstable holonomy formulas make q constant on a positive-measure product set. Ergodic saturation then places its range in a countable orbit of the lattice character. This gives a measurable lift to `Z^2/L`, where L is the character kernel. A proper integer subgroup has a nontrivial finite quotient character. That character produces a mean-zero unit-modulus invariant on an actual finite physical cover, contradicting its ergodicity.

This handles irrational u as well as rational u. It does not assume a measurable logarithm with finite moments, evaluate a phase on a periodic orbit, or replace the real billiard by an independent-sheet model.

`lem:finite-return-witnesses` next proves the existence of finitely many positive-measure first-return cells of an auxiliary product set whose displacement/count records generate `Z^3`. A proper return subgroup would produce an excluded exact phase by extension along the genuine first-return tower. This finite witness lemma is used quantitatively, with each cell's actual positive mass retained in the constants. The auxiliary product set is not substituted for the paper's record section.

### A.2. Finite-time approximate holonomy

`lem:finite-holonomy-defect` replaces the limiting holonomy argument by the explicit bound

`C_P [m d + H epsilon + (epsilon^(-1)+abs(t)) theta_P^m]`,

where d is the physical one-step L1 phase defect, H bounds BV, and m is a deterministic collision count. Both pair marginals are the normalized restriction of collision probability; their domination controls every accumulated defect. The backwards argument retains the same sign as the forward holonomy. No invariance of the pair probability is claimed.

The measure-class density is handled rather than suppressed. The new formulas state the stable and unstable conditional pair densities exactly. The proof truncates the finite Radon–Nikodym derivatives to compare reference triple products with those pair probabilities. The tail discarded in each comparison is explicit. No bounded density or inverse-density assumption is added to the inherited geometric input.

### A.3. Logarithmic separation on a fixed compact band

For a roof band bounded away from zero, choose a positive-measure family of four-corner quadrilaterals with action bounded above and below. The area obstruction, after the density truncation, bounds the integrated sum of four approximate holonomy errors from below. Choosing `epsilon=c/H` and `m=ceil(c_1+c_2 log H)` yields `d >= c/(1+log H)`.

For small roof frequency, `lem:almost-constant-product-phase` makes q approximately constant on the product set. The finite return witnesses then bound every lattice/count character by the phase defect, the endpoint error and the small roof term. Their integer generating identities cover compact nonzero spatial frequencies even when s=t=0. This proves `thm:compact-log-phase-defect` on every fixed compact subset of `T^3 x R` excluding the origin, at each fixed radius.

The constants are selected before q and H. Their dependencies are specified: product-set mass and contraction; density-tail cutoffs; the positive action witness and its mass; the finite return records, their cell probabilities and integer generating coefficients. A numerical billiard witness or a uniform bound as the frequency band changes is not asserted.

### A.4. Complex-vector reconstruction without a lower modulus

`thm:compact-vector-defect` supplies the comparison missing from a purely qualitative phase argument, on an explicit function class. Normalize `||f||_2=1`, assume `||f||_infinity+||f||_BV<=H`, and write a=|f|. The one-step complex defect epsilon controls the invariance defect of a. Collision correlations give

`Var(a) <= C H^2 exp(-gamma m) + sqrt(Var(a)) m epsilon`.

A BV coarea level between 1/4 and 1/2 produces a unit-modulus q with controlled BV and `||q-f||_2 <= 3 ||a-1||_2`, including zeros of f. The function is never divided by its modulus at zero. The resulting comparison is

`d(q) <= epsilon + C(eta+m epsilon)`.

Choosing `eta` proportional to `(1+log H)^(-1)` and `m=O(1+log H)` proves the normalized complex-vector lower bound `c/(1+log H)^2`. Polynomially growing BV budgets therefore cannot support polynomially small defects on a fixed compact nonzero band at a fixed radius.

### A.5. Parameter-uniform compact separation

`thm:uniform-compact-bv-separation` separately proves a positive infimum over the entire radius interval when H and the compact band are fixed. The proof uses BV compactness, L2 convergence from the supremum bound, persistence of regular collision roots, and an explicit smooth-approximation inequality for compositions with the varying maps. An exact limiting complex vector has invariant modulus and is therefore a forbidden circle phase.

This uniformity statement is not conflated with a uniform logarithmic rate for growing H. Product-set constants have not been assumed continuous or uniform in R.

### A.6. The remaining complementary-transform work

The new estimates are for actual bounded-BV collision functions. They are not a claimed realization of the unbounded induced twist on anisotropic distributions. A proposed operator proof must still construct the map from its approximate vectors to this function class, control its regularity and normalize the defect in the required norm. The compact-band constants must also be controlled in the shrinking annulus and growing roof regimes before they can enter an integrated splice.

Accordingly, the complete complement beginning at physical radius `2 n^(-99/200)` (rescaled `2 n^(1/200)`) is not declared estimated. The new theorem supplies a quantitative phase-reconstruction step, not a relabeling of Gaussian decay as physical Fourier decay.

## B. Complete raw branch decomposition

The original raw-edge, localized inversion and absolute residual-sum statements remain in full. The source still requires every critical, grazing, competing-root and image-boundary contribution, extraction of every nonintegrable jump, and actual return-count growth in the second-derivative sum. The new BV estimates concern collision functions, not inverse-coarea densities. They do not establish the missing global branch extraction or local edge error. Those requirements retain their roles in the same raw density theorem.

## C. Weighted exact conditioning

Initial and single-marked central and moment theorems remain intact, with the same restricted-collision normalization and unchanged event probabilities. The new compact collision defect theorem does not make a terminal lattice/time indicator or a multiple-time path functional admissible automatically. Weighted complementary and edge bounds, correct local denominator lower bounds and relative event replacement remain requirements for the exact physical observation. No event or denominator has been changed.

## D. Independent specialist review

The qualitative Young product input remains the same. New measure-theoretic details explicitly specify the conditional pair densities and the density truncations; new algebra specifies the countable lift and finite-cover invariant. The only appended bibliography item is Ambrosio–Fusco–Pallara for the classical BV chain, product and coarea rules used in radial truncation. Independent expert verification of the continuum proofs has not been obtained or inferred from CI.

## E. Article scope

The manuscript remains on its original raw mixed-density problem. The proof architecture is extended in place by Theorem F, rather than replacing the topic or removing the unresolved analytical mechanisms. The completed nondegeneracy and new quantitative function-space steps are retained as inputs to that endpoint.

## Presentation comments 1–14

1. Immediately after Theorem E, the introduction now states that every later use of D_R may use its stronger uniform positive definiteness.
2. Product coordinates are explicit: fixing u gives a stable leaf; fixing s gives an unstable leaf.
3. The densities of both conditional pair probabilities and both marginal densities are displayed in `eq:explicit-conditional-pair-densities`; the new defect proof spells out the Radon–Nikodym truncations.
4. The four corners are ordered `x00 -> x01 -> x11 -> x10 -> x00`, with the stable/unstable edge orientations stated beside the Stokes calculation.
5. Both the retained exact and new approximate proofs explain the identical holonomy sign.
6. The finite-cover paragraphs identify the unchanged planar disk array and flight bound, connected punctured-torus free domain, strict convexity, and the rectangular Euclidean cover.
7. The two- and three-rotation products remain separate and unchanged.
8. Exact phase rigidity, bounded-BV quantitative defects and anisotropic approximate-spectrum control are distinguished explicitly.
9. Both physical and rescaled cutoffs are now printed beside the inherited raw, localized and growing-band inversion statements; general older cutoffs retain their own hypotheses.
10. Gaussian and physical-transform tails continue to be different quantities.
11. Every inherited induced Green–Kubo conclusion retains the qualifier Cesaro.
12. The new finite covers, like the old one, are physical Euclidean billiards.
13. All changes to inherited TeX, including the appended reference, are exact replayable edits.
14. The metadata distinguishes author proofs, finite diagnostics, native builds and independent review. No journal or formal-proof certification is claimed.

## Source qualification

All 33 old core modules and all old theorem/equation labels remain. Two core sections are added. Twenty-eight inherited core files and every inherited Python diagnostic are byte-identical. Five inherited core files, main.tex and references.tex have exactly replayed edits. The old bibliography entries are all retained, with AFP appended. The source verifier checks the actual hashes and replays every edit from the frozen author baseline.

New finite checks cover non-product pair marginals and density truncation, four-corner cancellation, finite integer witness identities, finite-cover signs, the modulus quadratic bound, radial truncation including zeros, and logarithmic smoothing budgets. They are not a computation of actual billiard return witnesses or a certificate of continuum geometry. The exact-SHA build runs the inherited checks as well, in normal and optimized modes, typesets the complete ordinary-source article, and emits a run-bound receipt. No future execution result is predeclared successful in this response.
