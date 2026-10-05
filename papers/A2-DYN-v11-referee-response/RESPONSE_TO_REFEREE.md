# Response to the referee on A2-DYN revision 10

**Article:** Qian Qi, *Collision records, arithmetic, and raw local inversion in a triangular Lorentz gas*  
**Revised manuscript:** `papers/A2-DYN-v11-referee-response/main.tex`  
**Controlling report:** `reviews/a2-dyn-v10-external-top4-review-2026-10-06/REFEREE_REPORT.md`  
**Review commit / report blob:** `a42dc1401007f9f8025c916106884e09d7d864f0` / `e6732df7a22bc7e161ac4650e74e9fdce80d52b3`  
**Reviewed author commit:** `3e45e41b5be6ef636944f67dce529fdc9fd4fcc9`  
**Date:** 6 October 2026

We thank the referee for separating the integrated central theorem from the remaining requirements of raw inversion. The revision keeps the original title, physical family, four-coordinate deterministic return record and raw mixed-density endpoint. It does not replace the manuscript with a paper on a different problem. All twenty-seven mathematical core files of the reviewed version remain included and byte-identical. The following additions are part of the full article, not a response-only supplement.

## Principal new result

Theorem C and Theorem 22.5 extend the integrated central estimate to a weight placed at **any one of the actual returns**, uniformly in the mark index `0<=k<=n`. For a complex function a supported in the section, let `M_a=||a||_infinity`, `V_a=||a||_BV`, and `alpha_a=integral a dnu`. The marked measure assigns weight `a((F_R^*)^k x)` to the original n-return record. Its centered transform obeys

`integral_{|v|<=2 n^(1/200)} |C^[k],a_n,R(v)-alpha_a exp(-v^T D_R v/2)| dv`

`<= C [M_a n^(-3/280) sqrt(log(2+n)) + V_a n^(-9/175)]`.

The endpoints are the initial and terminal weights. Every intermediate sequence of marks is allowed, including one that approaches either endpoint. The estimate also permits an insertion variation norm growing as `O(n^kappa)`, `kappa<9/175`, when the supremum norm is bounded. This growth assertion was not a consequence of the uniform bounded-BV insertion class stated in revision 10.

The proof changes the origin of the actual orbit to the marked return. The record becomes an exactly compensated backward collision sum plus a forward collision sum, with the insertion at the new origin. Both parts are evaluated by forward collision operators, with the insertion as a middle multiplier. Separate treatments of two long blocks, a short block, and a zero block make the estimate uniform in the mark. No time-reversal invariance of the section, induced mixing, independent excursions, or regularity of a long induced composition is assumed.

Corollary 22.6 derives the central estimate under an unchanged marked-return-state event, retaining its exact probability denominator. This is a state-event result, not a substitution of a completed-return event for an exact final lattice event. Appendix C adds the requested definition-by-definition collision norm source map.

## Essential requests in Section 16

### 1. Uniform covariance nondegeneracy

The covariance remains the actual continuous matrix `D_R=c_*^-1 Gamma_R` established in the earlier compensation argument. It is positive semidefinite. The new proof does not require an inverse covariance or silently assume a positive lower eigenvalue.

We retain the distinction between an L2 coboundary identity and a representative that can be evaluated on selected periodic points. Changing the orbit origin is an almost-everywhere identity and does not provide the latter representative. The existing rigidity references have regularity and singularity hypotheses that have not been checked for the hard section indicator here. Consequently this revision does not claim to close the periodic-evaluable regularity or uniform positive-definiteness step. Positive definiteness remains explicitly required at raw Gaussian density inversion.

### 2. The whole complementary-frequency integral

The new marked theorem retains exactly the physical central radius `n^-99/200`. It does not reach the old `n^-2/5` threshold. The conclusion paragraph of Section 22 repeats that the intervening annulus, compact nonzero frequencies and large roof frequencies require estimates independent of the new central proof.

For the marked measures, that paragraph states the complete conditional inversion requirements: a uniform positive lower covariance bound, an extracted measure with mixed density, residual transform in `L1(T^3 x R)`, the full complementary integral of order `o(n^-2)`, and the local edge conditions. If these hold and the proved marked central error tends to zero, the retained exact inversion proof applies. Neither residual integrability nor the complementary estimate is attributed to the new theorem.

### 3. Actual high-frequency operator mechanism

Lemma 22.4 proves an exact marked **collision** pairing,

`ell(L_z^s M_(a_delta) L_z^r nu)`.

It uses the already established smooth collision operator on the local distribution spaces. The mark is a smooth multiplier after ordinary coordinate smoothing; no unbounded induced twist has been inserted into the same space without proof. The negative collision indices in the trajectory formula are eliminated by invariance before using the operator.

This supplies a rigorous operator mechanism for the new weighted central theorem. It does not supply the requested high-frequency Fredholm, phase reconstruction or resolvent estimates. The physical renewal compatibility and earlier phase-separation results remain included, with their original scope.

### 4. Global raw branch decomposition

No critical word, competing-root contribution or singular boundary is removed from the stated raw problem. The new insertion norm is variation in the original collision cylinder, including its section boundary. It is not a norm of a many-return coarea density.

Recentring a marked trajectory does not estimate inverse Jacobians or second distributional derivatives of the pushed-forward roof density. The complete n-dependent critical/singular residual sum and extracted-edge bounds therefore remain to be established. The manuscript does not infer them from the two-sided counting identity or from bounded initial-coordinate variation.

### 5. Strict frequency splice

The new central calculation exposes every additional error caused by the middle multiplier and the two-sided stopping. With the inherited choices `U_n=n^(1/200)` and `delta_n=(1/4)n^-1/14`, the insertion-smoothing term is

`V_a delta_n U_n^4 = (1/4)V_a n^-9/175`.

The supremum-weighted margins are `3/280`, `29/700`, `53/280`, `51/1400`, `9/50`, `7/40`, `19/40` and `97/100`. Short blocks are cut at a stated logarithmic threshold, making the complementary spectral powers negligible. The four-dimensional frequency-volume factors are included before choosing these margins.

These are actual inequalities for the central proof. They are not a surrogate for the missing intermediate/outer splice. No unverified spectral or branch-growth constant is assigned a favorable numerical value. The outer splice remains a separate requirement.

### 6. Weighted theory for conditioning

This request is advanced in three specific ways. First, the central integral now permits a terminal or an arbitrary single intermediate return-state insertion, not only an initial insertion. Second, its separate BV term permits controlled variation growth. Third, Corollary 22.6 gives an exact relative central error under the same marked-state event.

For `A={x:(F_R^*)^k x in E}`, invariance gives `nu_R^*(A)=nu(E)/c_*`. The conditional transform is exactly the marked transform divided by `nu(E)`. Thus its integrated error is bounded by

`C [n^-3/280 sqrt(log(2+n)) + ||1_E||_BV n^-9/175] / nu(E)`.

In particular a lower probability bound `c n^-beta` and BV growth `O(n^kappa)` suffice when `beta<3/280` and `beta+kappa<9/175`.

The limits of this advance are stated next to the result. A product of separated return-state factors is not one insertion at one mark. A final lattice or flight-time constraint depends on the record and is not generally a state set of this class. Complementary and edge bounds are still needed for a weighted **raw** local theorem. Accordingly the manuscript calls the new result a marked central-integral theorem, not a completed weighted local limit or an exactly conditioned physical-time bridge.

### 7. Independent specialist proof review

No independent human specialist endorsement has been obtained. The local-space identification remains a load-bearing mathematical import. Appendix C now maps the relative-density convention, weak, stable and unstable norms, exponent restrictions, mass functional and complementary powers to their exact locations in Demers–Zhang. The new marked pairing is derived in full rather than treated as a consequence of a generic mixing statement.

The source preservation checks, finite exact identities, native build and selected rendered-page inspection make the article easier to review; they are not independent continuum proof certification. No journal decision is represented by this delivery.

## Presentation and technical comments in Section 17

### 1. Collision and section normalizations

Section 22 begins with `nu(Y_R^*)=c_*` and `nu_R^*=c_*^-1 nu|_(Y_R^*)`. The new introduction states that the original probability corresponds to `a=s_R`. The marked measure is written relative to nu, and its mass is `alpha_a`, independent of the mark by invariance.

### 2. Complex amplitude and measure

A paragraph immediately following Theorem B now states explicitly that the insertion and its amplitude may be complex, and that the resulting pushforward is a finite complex measure rather than a probability law. Theorem C and Section 22 use the same convention.

### 3. Rescaled versus physical frequencies

The variables in Theorem C and the definition of the marked transform are rescaled v. The physical frequency remains `omega=v/sqrt(n)`. The final scope paragraph records the unchanged physical exponent `-99/200`.

### 4. The BV condition in finite-dimensional smoothing

The final reviewed correction in the earlier product corollary is retained byte for byte. The new theorem does not discard variation control: it states its exact cost as `V_a n^-9/175`. Supremum control alone is sufficient for exceptional clock events and bounded short exponents, not for the full unsmoothing passage.

### 5. The old cutoff is not reached

Neither the introduction nor the new proof describes the band as reaching `n^-2/5`. The new mark and norm-growth extensions use the same central band as revision 10.

### 6. Semidefinite and definite covariance

All three introductory theorems retain the positive-semidefinite covariance convention. The marked central estimate is valid even at a singular covariance. Raw density inversion is quoted only with its additional uniform positive-definiteness hypothesis.

### 7. All raw-inversion hypotheses

The end of Section 22 explicitly lists residual L1 integrability, the whole complementary-tail condition, the local extracted-edge conditions and the positive covariance lower bound. The marked central result is not presented as automatically supplying these conditions.

### 8. Terminology for weighted local limits

The new results are named central-integral estimates. The conditional marked raw-inversion application is identified as conditional. No statement that only controls the central integral is labeled a proved weighted raw local limit theorem.

### 9. Exact source table for collision norms

Appendix C gives the requested short table, distinguishing the location of a source definition from a deduction made in the present article. It maps weak, stable and unstable norms to (3.11)–(3.13), the relative-density convention to Section 3.2 and the Section 3.3 footnote, mass to Lemma 3.4, and complementary powers to Theorem 2.1(3). The existing smooth multiplier proof is cited separately instead of attributing an unproved induced multiplier theorem to the source.

### 10. The object whose variation is bounded

The new norm definition explicitly refers to the original collision coordinates and includes the section boundary. Both the appendix and the new section distinguish this first variation from second derivatives of the raw pushed-forward density.

### 11. Cutoff notation

The additional short-block threshold is `q_n`; the band radius is `U_n` and the smoothing scale is `delta_n`. The insertion is a, so it is not also used as a cutoff sequence.

### 12. Version and build prose

Version chronology, source hashes, preservation checks and publication status are in supporting files. The article contains mathematical statements, proofs and source citations. No repository checkpoint narrative interrupts the new proof.

## Delivery, preservation and verification

The complete manuscript typesets to 75 pages and includes 29 core files, 98 proof environments and 289 labels. All 27 inherited core files and 14 inherited diagnostic scripts are byte-identical. Normal and optimized Python diagnostics agree. New finite checks cover 26,880 exact two-sided marked compensation cases, 243 chronological operator pairings and 165 misplaced-mark negative controls, as well as every stated rational exponent margin. These finite examples verify algebraic ordering, not the continuum spectral hypotheses.

This revision has been prepared and validated locally. The available GitHub connection in this execution supplies read operations but no mutation operation, and direct Git network access failed. The remote v11 response ref observed during the work still pointed to the frozen review baseline. No new remote author commit or v11 Actions success is asserted. An add-only patch and a guarded, non-forcing publication script accompany the source, so that publication can use the intended review parent without replacing unrelated repository content.

The main raw-density problem is unchanged. The present revision advances the marked central and relative state-event analysis; it does not declare the covariance, global residual, complementary-frequency or exact-record conditioning work complete.
