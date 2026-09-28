# External top-four referee report on A2 v14

**Manuscript:** Qian Qi, *Nonlinear boundary laws and two-contact rigidity in dispersing billiards*  
**Reviewed revision:** `revision/a2-v14-relative-observability-normal-form-2026-09-28`  
**Reviewed commit:** `65b7286080ffae0c4bf8e5d5112fe42f08d82f21`  
**Reviewed tree:** `9c7f29885c4681262de57b7768c33139057cd028`  
**Manuscript directory:** `papers/A2-v14-relative-observability-normal-form`  
**Date:** 28 September 2026  
**Requested benchmark:** *Annals of Mathematics* / *Acta Mathematica* / *Inventiones Mathematicae* / *Journal of the AMS*  
**Status:** author-requested, AI-assisted referee-style assessment; not a journal decision or a formal proof certificate.

## 1. Recommendation and executive assessment

**Recommendation at the requested four-journal benchmark: reject.**

This verdict should not be confused with the v13 verdict. Version 14 is a genuine mathematical revision. It corrects the false universal finite-family quantifier, incorporates the previously missing analytic normal-form comparison in physical endpoint coordinates, separates exact-germ normalization from finite noisy calibration, and proves a new physical unknown-area/contact-jet observation theorem. These are substantive responses, not cosmetic changes.

On the portions audited in detail, I found no fatal counterexample to the new normal-form calculation, the regular-rank criterion, the free-area physical construction, or the shared-intercept finite-window design. The earlier two-flight block, relative determinant mechanism, Volterra profile uniqueness, Abel stability, and charged acquisition chain also retain the scope recorded in the previous report; I found no new reason to declare those principal results false.

The negative recommendation is instead editorial and conceptual. Once the closest analytic forward comparator is stated honestly, the qualitative product mechanism is seen to arise from classical local hyperbolic normal form plus the necessary physical projection. The manuscript's additional smooth/Fredholm machinery is technically substantial, but the global mathematical reach remains a selected-channel symmetrized profile, an individually even analytic contact inverse with supplied labelled leading geometry, and regular finite-dimensional statistical consequences. In my judgment this package does not yet produce the exceptional conceptual advance expected at the four journals named above. The extreme length and accreted architecture further obscure rather than strengthen the central theorem.

For a strong specialist journal, after a major restructuring and a fresh full proof review, I would regard the paper as potentially serious. At the requested benchmark, however, the appropriate decision is rejection rather than another indefinite revision cycle.

## 2. Frozen source and revision chronology

The two v14 branch names

- `revision/a2-v14-relative-observability-normal-form-2026-09-28`, and
- `revision/a2-v14-referee-copy-2026-09-28`

resolve to the same author commit `65b7286080ffae0c4bf8e5d5112fe42f08d82f21`. I treated that commit, not a branch label, as the reviewed source.

The complete reviewed v13 native manuscript is preserved inside v14 at

`papers/A2-v14-relative-observability-normal-form/history/v13-reviewed`

with Git tree `ee946ef91770778839f15c8c35416d401e99ea1c`. The v14 response also preserves the 10 September normal-form benchmark and both v13 reports. This is a satisfactory source freeze. The present report is based on the new v14 source, not on the 28 September v13 alias that the previous report correctly identified as containing no new mathematics.

The main active additions are:

1. `article/01a_relative_observability.tex`;
2. `article/16_normal_form_comparison.tex`;
3. `article/31_regular_observability.tex`;
4. revised front matter, response, source ledger, and scoped verification files.

I read these additions against the retained v13 sections governing the two-flight inverse and physical support-function family, in particular `article/24_physical_image.tex` and `article/29_two_flight_benchmark.tex`.

## 3. What v14 genuinely fixes

### 3.1 The false finite-family quantifier is fixed

The v13 abstract said, in effect, that every fixed finite-dimensional family can be observed by positive two-flight windows. That statement was false: a remote-obstacle motion can leave the selected channel laws unchanged. The v14 abstract no longer makes this universal claim.

The new theorem `thm:v14-rank` gives the correct local criterion. At a supplied family and parameter, injectivity of the tangent observation map is equivalent to the existence of finitely many positive-window evaluations with nonsingular derivative, and hence to a local bi-Lipschitz window map. The proof is the finite-dimensional span argument followed by a quantitative inverse-function estimate. The analytic-germ addendum correctly uses the identity theorem to move the criterion between nonempty open subintervals of a connected collar.

The constant-rank observable-quotient corollary is also correct in its stated local form. It does not confuse regular local factorization with global identifiability or with statistical sufficiency. The remote-obstacle example is now presented as a zero-rank direction for the selected information set, which is the right interpretation.

This closes the principal statement error from v13.

### 3.2 The closest analytic forward comparator is now present

Section 16 starts from the supplied analytic canonical normal form

\[
N(s,p)=(\Delta(sp)s,\Delta(sp)^{-1}p),\qquad \Delta(0)=\lambda\in(0,1).
\]

For the mixed boundary conditions it derives

\[
I=st\Delta(I)^n,\qquad p_0=t\Delta(I)^n,\qquad
T_n=\left.\frac{\partial p_0}{\partial t}\right|_s
 =\frac{\Delta(I)^n}{1-nI\Delta'(I)/\Delta(I)}.
\]

The proof estimates the normalized expression before differentiating, uses a fixed complex bidisk and Cauchy bounds, and therefore avoids the invalid operation of dividing an uncontrolled absolute error by an exponentially small twist. This is the correct relative argument.

The physical endpoint projection is not skipped. With the mixed-to-physical map `Phi_n`, the symplectic two-form gives the exact identity

\[
|W_{n,uv}|=\left|\frac{T_n}{\det D\Phi_n}\right|.
\]

The common physical-box inversion, the exact origin determinant, the product limit, and the action-gradient limit are all supplied. The normalized factors are inverse projection Jacobians of the stable and unstable axes. Applying this and the half-line determinant theorem to the same analytic physical problem identifies the two normalized factors by uniqueness of the limit and their value one normalization.

This is the comparison the previous report requested. It also sharpens the novelty statement in the correct direction: the existence of an analytic nonlinear relative product is not, by itself, new; the manuscript's increment lies in the directly geometric smooth construction, common-box differentiated estimates, first-hit channel localization, residual-time integration, and the later inverse/observation results.

I found no fatal algebraic or analytic defect in this comparator. The independent finite checks accompanying this report verify the displayed implicit derivative and the nontrivial canonical-shear projection identity on exact rational grids. Those checks are diagnostics, not a substitute for the proof.

### 3.3 Exact normalization and finite noisy observation are separated

Version 14 now distinguishes three different operations:

1. taking normalized exact germs as mathematical input;
2. extracting the common leading coefficient from a raw exact germ by a limit at zero;
3. estimating unknown area from finitely many positive noisy windows on a specified physical family.

This is the distinction missing in v13. Equation `eq:v14-exact-area` correctly recovers the area from exact germ data once the labelled leading geometry is supplied, while explicitly noting that this limiting operation is not a finite statistical procedure.

### 3.4 The unknown-area extension is a real physical theorem

The free-area proposition keeps the coefficient of `sin^(2M+2)(theta)` free in the existing support-function construction. This perturbation does not change the selected support values, curvatures, or graph jets through order `2M`. Its area derivative is

\[
\partial_\zeta A=-\int_0^{2\pi}(h+h'')\sin^{2M+2}\theta\,d\theta<0,
\]

so the old triangular support-to-contact Jacobian combines with the area direction to give local physical coordinates

\[
(A,q_2,\ldots,q_M).
\]

This is compatible with the retained fixed-area theorem. It does not merely append a formal scalar parameter to a jet model.

The subsequent observation theorem uses `M` positive windows in one orientation and `M-1` in the other. In the coordinates

\[
(\alpha,\alpha\xi_{0,1},\ldots,\alpha\xi_{0,n},
          \alpha\xi_{1,1},\ldots,\alpha\xi_{1,n}),
\qquad n=M-1,
\]

there is a shared constant coefficient. The resulting `2n+1` by `2n+1` nodal matrix is invertible: the first block forces a degree-`n` polynomial to vanish at `n+1` nodes, and the second block then has the additional root at zero. Its inverse has the expected `h^{-n}` scaling, while the differentiated Taylor remainder is `O(h^{n+1})`; after preconditioning the perturbation is `O(h)`. This establishes a nonsingular Jacobian for fixed sufficiently small positive `h`.

Returning to raw probabilities uses only known row factors `(ih)^2`; it does not insert the unknown area. The local bi-Lipschitz conclusion and the fixed-dimensional `N^{-1}` risk bounds then follow by standard arguments. The lower bound correctly permits adaptivity only among the stated fixed windows and uses actual physical alternatives in the constructed family.

I found this theorem sound in its stated fixed-`M`, supplied-family, supplied-labelled-geometry scope.

## 4. Technical qualifications and minor corrections

The following points do not overturn the audited theorems, but they should be corrected in any revised presentation.

### 4.1 State the same-section chart convention behind the exact reference flux

After the physical projection proposition, the manuscript specializes to “the same physical section at both ends” and writes the reference normalization using `U_s(0,0)U_p(0,0)`. The intended identification of the right chart derivatives with the corresponding entries of the left chart is recoverable from context, but it should be stated explicitly, including the orientation/sign convention. The general formula with `U_s V_t-\lambda^{2n}U_pV_q` is the invariant statement and should remain primary.

### 4.2 Keep fixed derivative order and fixed jet order visible

The normal-form estimates are for each fixed `C^k` order, and the finite-window conditioning constants may deteriorate rapidly with `M`. The manuscript does say this, but the abstract and theorem summaries should make the fixed-order nature visually unavoidable. Nothing here is uniform in growing jet order.

### 4.3 Clarify the probability-margin sentence

In the area-window proof, once positive nodes and a compact parameter ball have been fixed, strict positivity and an upper bound below one should be deduced directly from continuity and compactness. The phrase “after decreasing the collar if necessary” is potentially confusing after the window design has already been selected. This is a presentation issue, not a substantive obstruction.

### 4.4 Do not overstate minimality

The `2M-1` count is minimal for a differentiable locally bi-Lipschitz coordinate map built from scalar window means on this `2M-1` dimensional family. It is not a universal information-theoretic minimum over arbitrary experiments, derivatives, sequential stopping rules with other observations, or singular inverse maps. The theorem itself includes the proper qualification; the abstract and response should preserve it exactly.

### 4.5 Full-source build evidence remains incomplete at review time

The author's scoped `VERIFICATION.json` appropriately claims only finite algebra and an isolated eight-page build. The exact-source GitHub Actions run `36379170430` for commit `65b7286080ffae0c4bf8e5d5112fe42f08d82f21` remained `queued` with no conclusion when this report was finalized. I therefore do not record an independent successful full-manuscript build. This is a reproducibility item to close, not the mathematical basis for the top-four rejection.

## 5. Remaining top-four significance objections

### 5.1 The forward product mechanism is no longer a standalone novelty claim

The new comparison does exactly what it should, but it changes the editorial balance. It shows that, in the analytic setting with supplied normalizing charts, the relative product and its stable/unstable interpretation follow from classical local hyperbolic structure plus physical projection. The manuscript's smooth half-line determinant proof is stronger in hypotheses and uniformity, and its geometric execution is nontrivial. Nevertheless, the conceptual phenomenon is not newly discovered here.

To justify a top-four venue, the smooth extension would need to be shown to unlock a broader principle or consequence commensurate with the technical investment. At present it feeds a selected-channel invariant and the later scoped inverse problems, but not a new global rigidity theorem or a general structural classification.

### 5.2 The inverse target remains restricted

For arbitrary smooth contacts the recovered object is the complete **symmetrized energy profile** associated with one selected channel. It is not the pair of individual boundary germs, not the whole billiard table, and not a global isometry class.

The explicit contact recovery theorem is stronger geometrically but assumes individually even analytic contacts, supplied labels, supplied gap, and supplied separate curvatures. Equal curvatures are handled, which is a genuine technical achievement, but asymmetry and natural global data remain outside the theorem.

These restrictions are now stated honestly. They are not correctness defects. They do, however, limit the mathematical reach at the requested editorial level.

### 5.3 The finite statistical results are consequences of local invertibility

The physical realization and two-flight block are the real geometric content. Once a finite-dimensional physical mean map is locally bi-Lipschitz with fixed positive probability margins, `N^{-1}` squared risk and `epsilon^{-2}` confidence cost are regular parametric consequences. The new regular-rank theorem is essentially finite-dimensional duality plus the inverse function theorem. The shared-intercept design is elegant, but it does not create a new statistical regime.

The infinite-dimensional profile experiment is more delicate, yet the manuscript offers a sufficient preparation bound under supplied smoothness and convergence certificates, not an optimal minimax theorem with matching lower bounds for the physical model. Thus neither statistical component independently supplies the missing top-four-level conceptual leap.

### 5.4 The manuscript lacks a single dominant theorem

The paper now contains several substantial but only partially unified projects:

- a smooth relative determinant law;
- a symmetrized-profile inverse and compatibility identity;
- an even analytic two-contact jet inverse;
- a support-function physical image;
- finite-dimensional two-flight experiments;
- an Abel-regularized smooth-profile acquisition scheme;
- extensive auxiliary, calibration, minimax, and historical material.

The result is an accreted manuscript rather than a sharply organized argument around one theorem whose consequences transform the subject. The main mathematical contribution is difficult to identify without reconstructing many rounds of referee history.

### 5.5 The revision history is too prominent in the mathematical article

The long acknowledgments catalogue successive AI referee memoranda and the provenance of individual calculations. Provenance should be retained in repository records, but a journal article should present a coherent mathematical narrative independent of its revision history. The present architecture repeatedly interrupts theorem exposition with distinctions inherited from prior objections. This is valuable for auditability and poor for a final top-tier paper.

## 6. What would materially strengthen a future submission

A credible resubmission should first be reorganized, not merely enlarged.

1. **Separate the projects.** A natural division is a geometry/dynamics paper centered on the smooth relative law and profile invariant, and a second paper on explicit even-contact inversion and physical/statistical observation. The current appendix ecosystem is too large for a single conceptual arc.
2. **State one central theorem early.** The introduction should specify exactly what is new after the analytic normal-form comparator, with the comparator stated before global inverse-spectral comparisons.
3. **Move provenance out of the article.** Keep source pins, report chronology, and AI-assistance records in a supplementary repository ledger; reduce the main acknowledgments to ordinary mathematical attribution.
4. **Close the reproducibility loop.** Record a successful exact-source full build and resolve any resulting references or layout failures.
5. **Pursue one broader mathematical consequence.** Examples of a genuinely material upgrade would be an asymmetric contact inverse, a natural whole-table rigidity consequence, a parameter-uniform smooth normal-form theorem that reveals a new structural equivalence, or a sharp infinite-dimensional physical experiment. I do not require all of these, and I am not prescribing an unrelated theorem; the point is that rewriting alone will not bridge the present top-four significance gap.
6. **Reduce theorem proliferation.** Elementary rank and parametric-risk consequences should be compressed so that the genuinely new geometric arguments carry the exposition.

## 7. Independent diagnostics and limits of this review

The accompanying `verify_review.py` imports no author code. In exact rational arithmetic it performs 584 checks:

- 60 shared-intercept nodal determinant, scaling, nonuniform-node, and singular-node checks;
- 25 mixed-boundary implicit-derivative checks;
- 480 canonical-shear physical-projection checks;
- 19 free-area direction sign checks.

Normal Python execution produced the accompanying `verification.json` summary. These checks support only the finite algebra of the new v14 arguments. They do not certify the complex-analytic estimates, global billiard geometry, retained profile theory, statistical measurability, or the complete source build.

I did not attempt an exhaustive priority search. The literature comparison here is limited to the closest mechanism already identified in the frozen v13 benchmark and to the theorem-level distinctions made by the manuscript. I also do not claim to have re-proved every inherited lemma in a manuscript of this size.

## 8. Final verdict

**Response to the previous reports:** substantively successful. The false quantifier, missing forward comparator, area-normalization ambiguity, and source chronology have been addressed.

**Mathematical audit:** no fatal counterexample found in the new v14 core or in the previously audited principal chain; several minor presentation clarifications remain.

**Editorial assessment:** the corrected paper is technically serious but still too restricted, diffuse, and incrementally assembled for the exceptional conceptual threshold of *Annals*, *Acta*, *Inventiones*, or *JAMS*.

**Recommendation: reject at the requested top-four benchmark.**