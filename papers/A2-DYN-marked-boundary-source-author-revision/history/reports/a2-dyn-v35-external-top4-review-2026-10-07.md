# External top-four referee report on A2-DYN revision 35

**Manuscript:** Qian Qi, *Collision records, arithmetic, and raw local inversion in a triangular Lorentz gas*  
**Reviewed branches:** `revision/a2-dyn-v35-referee-response-2026-10-07`, `revision/a2-dyn-v35-referee-copy-2026-10-07`  
**Reviewed commit:** `fda52bb72045204b50159e8263c05afaa6a9dc58`  
**Repository tree:** `e25ebf1086ebb693b92faf4c234452a944e4a708`  
**Ordinary source payload tree:** `5979a920272b5ec7999adb37282deca9cb4b6a16`  
**Active directory:** `papers/A2-DYN-v35-referee-response`  
**New modules:** `72_action_norm_details.tex`, `73_rotation_free_arithmetic.tex`, `74_compact_family_local_principle.tex`, `75_literature_and_routes.tex`  
**Controlling report:** `reviews/a2-dyn-v34-external-top4-review-2026-10-07/REFEREE_REPORT.md`  
**Controlling report commit / blob:** `b4ea180550cd805fba88019e52d0b1a54ca8eef1` / `776a78aaecf82ea2dc92cd661e49c8bddf58e522`  
**Date:** 7 October 2026  
**Benchmark:** *Annals of Mathematics* / *Acta Mathematica* / *Inventiones Mathematicae* / *Journal of the AMS*  
**Status:** author-requested, AI-assisted referee-style assessment; not a commissioned journal report, editorial decision, formal proof certificate, or independent human specialist report.

## 1. Recommendation

**Reject in the present form at the requested four-journal benchmark.**

Revision 35 is a genuine and substantial revision. It expands the action-weighted collision-space proof, supplies a physical representation of peripheral vectors, replaces the circular symmetry argument by finite-cover arithmetic, formulates a compact-family local principle, and verifies that principle for all oriented ellipses whose two semiaxes lie in `[0.45,0.47]`.

The revision also corrects a real scope mismatch in module 70: the varying-test Portmanteau statement now requires exceptional open neighborhoods whose closures have small limiting measure and null boundary, which is the hypothesis actually used in the proof.

On the new material I found no decisive counterexample, no inconsistent clock normalization, no lost cell correction, no misuse of a growing Fourier bandwidth inside a fixed-band spectral estimate, and no obvious algebraic failure in the finite-character argument. The strict norm exponents are compatible, and the block/equivalent-norm choices are made in the correct order.

The negative top-four recommendation rests instead on four broader points.

1. The article still presents the raw four-coordinate local limit theorem for the actual return record
   \[
   J_{n,R}=(K_{n,R},N_{n,R},T_{n,R})
   \]
   as an organizing target. Its common pointwise correction and full return-frequency complement remain unproved. The new collision theorem contains neither accumulated section occupation nor the unbounded induced-return record.

2. The compact-family physical theorem is substantial, but its novelty relative to existing Lorentz-process local limits, endpoint mixing local limits for deformed billiards, and suspension-flow local central limit theory is still too specialized for the requested benchmark. The new package is primarily an action-weighted roof verification, rotation-free arithmetic, compact-parameter uniformity, an ellipse application, and posterior total-variation comparison.

3. The most difficult continuum steps still require an independent billiards/anisotropic-spaces audit. Source qualification and finite diagnostics cannot certify them.

4. The paper remains a hybrid of a completed three-coordinate physical theorem and an incomplete four-coordinate raw-return program. The new Part I route is a major improvement, but a seventy-five-module article should have one unmistakably completed principal endpoint.

Subject to specialist verification, the stationary compact-family theorem appears credible and potentially publishable in a strong dynamics/probability venue. The combined article does not yet meet the standard of the four journals named above.

## 2. Frozen source and qualification

Both author branches resolve to

`fda52bb72045204b50159e8263c05afaa6a9dc58`.

The source manifest identifies the ordinary payload tree as

`5979a920272b5ec7999adb37282deca9cb4b6a16`.

Seventy inherited core files and all seventy-nine inherited Python files are reported byte-identical. Module 70 receives exactly the two declared statement/proof-alignment replacements recorded in `INHERITED_EDITS.json`; the former source is retained under provenance. The bibliography now gives the published Demers--Pène--Zhang citation while retaining the arXiv numbering convention used in the text.

The exact-SHA qualification workflow completed successfully on both branches:

- response run `37640998381`;
- referee-copy run `37641024948`.

These runs establish source identity, successful finite diagnostics, and native typesetting. They do not prove the multiplier partition, weighted Lasota--Yorke estimates, matched-connector regularity, strong-space faithfulness, finite-cover mixing, compact-frequency spectral gap, endpoint local-measure passage, or the local theorem.

## 3. Scope of the mathematical audit

The substantive audit concentrates on:

- the three collision norms and exponent choices;
- the preceding-flight piecewise multiplier;
- the normalized Jacobian and length sums;
- the action estimate on stable pieces and matched connectors;
- the block equivalent-norm argument;
- faithfulness of the strong completion and the physical peripheral-density construction;
- measurable holonomy and finite-cover phase rigidity;
- covariance nondegeneracy;
- the compact-family fixed-band local principle;
- the corrected varying-test argument;
- the oriented-ellipse verification; and
- the distinction between the physical theorem and the still-open raw-return theorem.

The many inherited Gaussian, functional, raw-edge, window, bridge, and cutoff results are treated as the qualified baseline claimed by the author packet, not as independently re-certified here.

## 4. Norms, multipliers, and exponent choices

Module 72 states the weak, strong stable, and unstable norms in a common density convention. The choices

\[
p=1/12,\quad q=1/24,\quad \varsigma=1/8,
\quad \zeta=1/4,\quad 0<\gamma\le1/100
\]

satisfy the displayed strict inequalities. I found no arithmetic inconsistency in them.

The preceding-flight observable is required to have a fixed finite regularity partition in each homogeneity strip, a bounded stable-curve intersection count, an `O(epsilon)` boundary-neighborhood estimate, and a common piecewise one-half-Hölder bound. These are the appropriate hypotheses for the cited multiplier criterion. The text correctly rules out a partition whose complexity grows with the orbit length.

The complex exponential and its fixed derivatives are estimated in the multiplier algebra, giving analytic dependence on compact complex frequency sets. A specialist should still check the exact correspondence between the manuscript's exponents and the conventions in the pinned version of Demers--Pène--Zhang.

## 5. Action weights and the stable inequality

The manuscript records the unweighted inverse-curve sums with their length factors before inserting the phase. The interpolation giving the never-long estimate is consistent with those sums.

The identity

\[
d\tau=T^*\vartheta-\vartheta,
\qquad \vartheta=\sin\varphi\,dr,
\]

telescopes on every regular branch. Since the lattice label is constant on that branch, the accumulated displacement--roof phase has a Lipschitz bound independent of the number of collisions.

For the strong stable norm, the proof subtracts the average of the pulled-back terminal test, not the average of the weighted test. The contracting test difference retains `Lambda^{-qm}`, while the noncontracting phase derivative is paid by the weak term through the last-long-ancestor decomposition. This is the correct structure and avoids placing a nondecaying phase derivative in the leading strong coefficient.

Revision 35 has substantially answered the revision-34 request to expose the normalized length and Jacobian sums.

## 6. Matched connectors and the unstable inequality

The matched inverse pieces use the regular unstable-cone connectors from the unweighted collision proof. A connector meeting an intermediate singularity is assigned to the unmatched family. Matched endpoints therefore have the same lattice itinerary, and the action identity gives a roof-sum difference of order `epsilon`.

After charging the trimming cost, interpolation yields

\[
\|w_m^{(1)}-w_m^{(2)}\|_{C^q}
\le C_B\epsilon^{1-q}.
\]

The unstable estimate separately pays the unmatched `epsilon^varsigma` term, the old graph/test and Jacobian errors, and the new weight difference. Every exponent is strictly larger than `gamma`. The stable cross coefficient remains `C_B C_3^m`; it is not incorrectly replaced by an iterate-independent constant.

For a fixed band, the block length is chosen first, and only then is the coefficient of the unstable norm chosen to absorb the finite cross term. This order is correct.

An independent specialist should verify directly that every connector declared matched remains regular through all intermediate iterates, that all singularity and homogeneity cuts belong to the old partition, and that the weighted matching preserves the imported Jacobian estimates.

## 7. Strong-space faithfulness and peripheral densities

The transverse-averaging argument in module 72 is a plausible way to recover stable-curve pairings from global smooth tests. It addresses a genuine gap in any argument that treats an abstract anisotropic vector as automatically physical.

The final presentation should make the logical endpoint fully explicit. The transverse averaging should be stated as proving directly that all `C^q` stable pairings vanish and hence that both strong seminorms vanish. Alternatively, the text should cite a previously established injective embedding of the strong completion into distributions. The current sentence invoking an injective strong-to-weak inclusion can be read as assuming the point under proof.

The peripheral-density construction itself is sensible. Cesaro averages of twisted images of a bounded smooth density remain uniformly bounded in `L^infinity`; a weak-star limit represents the spectral projection on smooth global tests. The eigen-equation is passed through the physical weighted-composition operator, not by applying a discontinuous test to an abstract distribution. Ergodicity then makes the nonzero modulus constant.

Subject to the faithfulness clarification, I found no immediate contradiction in this step.

## 8. Rotation-free phase rigidity

Module 73 removes the roof frequency by measurable stable/unstable holonomy. Multiplying the leaf relations around arbitrarily small product rectangles gives

\[
\exp\left(ib\int_Q d\vartheta\right)=1.
\]

Since `d vartheta` is nonzero away from grazing, this forces `b=0`.

The remaining displacement and constant collision phase are encoded in the cocycle `(kappa,1)` in `Z^3`. If its kernel is proper, a finite character gives a function on a finite lattice cover which is either a nontrivial unit-modulus eigenfunction or a nonconstant invariant function. Mixing excludes the former and ergodicity the latter.

The algebra is coherent and genuinely removes reliance on rotations of a circular obstacle. The theorem also correctly distinguishes the constant collision step from the discontinuous section occupation in the actual-return problem.

## 9. Finite-cover mixing is a load-bearing input

The general theorem uses mixing of every relevant finite lattice cover. The ellipse application says that connectedness of the free region and standard finite-horizon dispersing theory provide this conclusion.

This needs a more precise statement and citation.

Connectedness alone should not be used as shorthand for the exclusion of every finite cyclic component of the collision map. The author should either:

1. state mixing of each finite cover as an explicit independent hypothesis and cite the exact Bernoulli/mixing theorem verifying it for the ellipse covers; or
2. give a short geometric aperiodicity argument for those covers.

This point is substantive because the nonzero constant-step character is excluded by mixing, not merely by ergodicity. I did not find a counterexample in the triangular ellipse family, so I regard this as a required clarification rather than a demonstrated failure.

## 10. Covariance and compact-family spectrum

The zero-variance argument is coherent. Exponential covariance summability makes the partial sums of a zero-variance scalar observable bounded in `L^2`; Cesaro averaging supplies a coboundary, and exponentiation produces a phase equation for every real scalar. Rotation-free rigidity then forces the direction to vanish.

For each fixed frequency band, the weighted inequalities give power boundedness and quasi-compactness. Strong-to-weak continuity and peripheral exclusion give a uniform spectral gap on compact sets avoiding zero. Near zero, analytic perturbation identifies the quadratic term with the Green--Kubo covariance.

The proof does not claim any useful control of the constants as the band grows. The local theorem freezes the band, takes the collision count to infinity, and enlarges the band only through positive interval envelopes. This order of limits is correct.

The compact-family theorem would be more reusable if common collision spaces, finite-cover mixing, preceding-flight multipliers, action regularity, observation geometry, and parameter continuity were listed as separate hypotheses rather than bundled into “uniform table geometry.”

## 11. Endpoint measures and the corrected Portmanteau step

Revision 35 correctly strengthens the varying-test hypothesis. The exceptional open neighborhoods must have closures of small limiting measure and null boundary. Portmanteau then controls the source mass of the closed exceptional set, while uniform convergence handles its complement.

Small measure of an arbitrary open set alone would not have justified the previous limsup argument. The correction is mathematically real and should be retained in every synopsis of the theorem.

The one-flight overlap tests satisfy the stronger condition through closed neighborhoods of finitely many grazing, singular, tangency, vertex-crossing, and cell-boundary curves.

## 12. The oriented-ellipse family

Every ellipse in the stated family contains the radius-`0.45` disk and is contained in the radius-`0.47` disk. This gives uniform separation, a common finite horizon, uniform curvature bounds, common `C^3` boundary bounds, and a fixed finite candidate set.

The quadratic backward entry root has a denominator uniformly separated from zero, and the square root gives one-half-Hölder regularity up to tangency. A fixed-complexity semialgebraic decomposition in rational trigonometric charts is a reasonable mechanism for obtaining finitely many monotone backward-singularity arcs. Stable/unstable transversality then gives the intersection and boundary-neighborhood estimates.

The change to normalized arclength is uniformly smooth and monotone, so the finite-complexity and transversality estimates should survive it. The circular locus makes the orientation parameter redundant but does not singularize the geometry.

Subject to the finite-cover mixing clarification, the ellipse verification is plausible and internally consistent.

## 13. Physical normalization and posterior comparison

The endpoint local measure evaluates the exact flight-age overlap with both cell offsets retained. The total overlap amplitude is `bar_tau^2`, and the stationary source contributes `1/bar_tau`. The physical clock change gives

\[
\det\mathcal V_\lambda
=\bar\tau_\lambda^{-5}\det\Sigma_\lambda.
\]

This normalization is consistent.

Regular endpoint selectors give the product of stationary means. A positive selected denominator is claimed only when that product is uniformly positive. The text correctly refuses to infer an arbitrary path-selector Gaussian amplitude from posterior total-variation approximation.

The normalized posterior comparison uses only the explicit `O(B^{-1})` source-smoothing error and the independently proved `t^{-3/2}` denominator. Choosing `B=m^{P+3/2}` after the local theorem does not invoke a growing-band spectral estimate.

## 14. Prior art and significance

Module 75 improves the literature discussion substantially. It acknowledges that a fixed-table cell local limit is not new, endpoint factors and geometric perturbations already occur in billiard local-limit theory, and the fixed-parameter physical conclusion belongs to suspension local-limit theory once the relevant joint observable and arithmetic group have been verified.

The manuscript now narrows its novelty claim to the action-weighted roof calculation, rotation-free finite-cover arithmetic, compact-family uniformity, noncircular verification, and normalized source comparison.

In my judgment, this is substantial but not yet broad enough for the requested four-journal benchmark. The compact-family theorem remains tailored to finite-horizon periodic dispersing billiards with standard collision anisotropic spaces, one-flight observations, and mixing finite covers.

A stronger top-four case would require at least one of:

- completion of the original raw four-coordinate return theorem;
- a general action-weighted local-limit theorem for a broad class of singular hyperbolic systems with several nontrivial applications; or
- a new sharp phenomenon not already organized by existing collision and suspension local-limit frameworks.

## 15. The raw-return theorem remains open

The finite-cover arithmetic adjoins the constant integer collision step. It does not insert accumulated section occupation into the collision twist. The compact-family action estimate does not realize the unbounded induced-return observable.

Consequently the following remain unproved in the submitted article:

- the common pointwise correction for the raw return measure;
- the full return-frequency complement;
- the complete raw four-coordinate mixed-density LLT;
- arbitrary selected-path Gaussian amplitudes; and
- the general microscopic conditional path bridge suggested by the inherited pipeline.

These are central analytical requirements of Part II, not minor editorial omissions.

## 16. Architecture

The new two-part organization is a major improvement. A reader can reach the physical theorem through modules 75, 72, 73, and 74, followed by the detailed modules 69--71.

Nevertheless the article still combines a completed compact-family physical theorem with an incomplete raw-return program. At the requested benchmark, this weakens the main theorem rather than strengthening it.

A publication version should either complete the raw-return theorem or present the compact-family physical theorem as the actual endpoint and move the raw-return program to a separate sequel. This is not a request to delete valid mathematics; it is a request to align the article with a completed principal theorem.

## 17. Required changes for any positive reconsideration at the requested benchmark

1. Resolve the principal endpoint: complete the raw-return LLT or submit the compact-family physical theorem as a separate completed paper.
2. Obtain an independent specialist audit of the weighted norms, matched connectors, strong-space faithfulness, peripheral density, finite-cover mixing, and varying endpoint tests.
3. State and verify finite-cover mixing precisely.
4. Make the strong-space faithfulness conclusion noncircular.
5. Pin exact references for every normalized Jacobian/length sum and matching estimate in the conventions used.
6. State the compact-family theorem with reusable, separated hypotheses.
7. Strengthen the theorem-level novelty comparison and provide applications beyond the ellipse family if claiming a general principle of top-four breadth.
8. Streamline the journal manuscript around a small number of principal results while preserving provenance in the repository.

## 18. Technical comments

1. Keep the dependence of the equivalent norm on the fixed band visible.
2. Retain the statement that no growing-band spectral constant is controlled.
3. State explicitly which sign in the ellipse quadratic gives the first admissible backward entry and how the current obstacle's zero root is removed.
4. Explain that the semialgebraic partition is built before passing to normalized arclength.
5. Note explicitly that orientation is redundant but harmless at the circular locus.
6. Point every use of “regular endpoint selector” to the null-boundary and closed-exceptional-neighborhood conditions.
7. Fix the total-variation convention, including any factor `1/2`.
8. Do not imply a polynomial convergence rate for the compact-family LLT; the theorem gives qualitative `o(1)`.
9. Keep the distinction between arbitrary bounded posterior tests and regular selector Gaussian amplitudes.
10. Keep the published DPZ citation together with the note that the lemma numbering follows the pinned arXiv version.
11. Distinguish local common Banach spaces from one global Banach space over the compact family.
12. State separately where mixing and where only ergodicity are used in the finite-cover character proof.
13. Retain the count-as-suspension-reward identity because it prevents an exaggerated novelty claim for the count coordinate.
14. Do not call the physical singleton theorem the full raw local theorem while the four-coordinate return theorem remains open.

## 19. Final assessment

Revision 35 closes several legitimate objections to revision 34:

- the weighted norm calculation is substantially expanded;
- the peripheral vector is connected to a bounded physical phase;
- the arithmetic no longer uses circle rotations;
- the theorem is formulated on a compact family;
- a noncircular oriented-ellipse family is verified;
- the varying-test statement is corrected;
- the prior-art discussion is much more accurate; and
- both author branches have successful exact-SHA qualification runs.

I found no demonstrated fatal error in the new stationary theorem.

That does not justify acceptance at the requested benchmark. The original raw-return theorem remains incomplete, the completed physical theorem is still specialized relative to existing local-limit frameworks, the load-bearing continuum proof lacks an independent specialist audit, and the article combines two different local-limit projects at excessive scale.

**Final recommendation: reject in the present form at the requested top-four benchmark.**

A shorter paper centered on the compact-family physical theorem could be a serious candidate for a strong dynamics/probability journal after specialist verification. A future submission that also closes the raw four-coordinate return correction and complement would warrant a fundamentally different top-four assessment.
