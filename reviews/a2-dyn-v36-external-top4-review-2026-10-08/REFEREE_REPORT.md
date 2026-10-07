# External top-four referee report on A2-DYN v35 (latest v36 branch alias)

**Manuscript:** Qian Qi, *Collision records, arithmetic, and raw local inversion in a triangular Lorentz gas*  
**Latest visible branches:** `revision/a2-dyn-v36-referee-response-2026-10-08`, `revision/a2-dyn-v36-referee-copy-2026-10-08`  
**Latest visible branch head:** `8bcdf384a36b6bbc86e276b128354dc5766b99e2`  
**Branch-head object:** the existing external report on revision 35, not a new author manuscript  
**Latest actual author branches:** `revision/a2-dyn-v35-referee-response-2026-10-07`, `revision/a2-dyn-v35-referee-copy-2026-10-07`  
**Reviewed mathematical commit:** `fda52bb72045204b50159e8263c05afaa6a9dc58`  
**Reviewed repository tree:** `e25ebf1086ebb693b92faf4c234452a944e4a708`  
**Ordinary source payload tree:** `5979a920272b5ec7999adb37282deca9cb4b6a16`  
**Active manuscript directory:** `papers/A2-DYN-v35-referee-response`  
**Existing v35 report:** `reviews/a2-dyn-v35-external-top4-review-2026-10-07/REFEREE_REPORT.md`  
**Existing v35 report commit:** `8bcdf384a36b6bbc86e276b128354dc5766b99e2`  
**Date:** 8 October 2026  
**Requested benchmark:** *Annals of Mathematics* / *Acta Mathematica* / *Inventiones Mathematicae* / *Journal of the AMS*  
**Status:** author-requested, AI-assisted referee-style assessment; not a commissioned journal report, an editorial decision, a formal proof certificate, or an independent human specialist report.

## 1. Recommendation

**Recommendation at the requested four-journal benchmark: reject in the present form.**

There are two logically distinct reasons for this recommendation.

First, the branches labeled revision 36 do not contain revision-36 mathematics. Both resolve to `8bcdf384a36b6bbc86e276b128354dc5766b99e2`, whose only mathematical-history change relative to the author source is the already landed referee report on revision 35. There is no directory `papers/A2-DYN-v36-referee-response`, no revision-36 source manifest, no revision-36 main manuscript, and no revision-36 qualification workflow. The latest actual mathematical revision is therefore revision 35 at `fda52bb72045204b50159e8263c05afaa6a9dc58`.

Second, an independent supplementary audit of that revision-35 source does not alter the top-four assessment. Revision 35 contains substantial and apparently credible mathematics: it makes the action-weighted collision-space proof far more explicit, replaces the circular phase argument by finite-cover arithmetic, formulates a compact-family physical local principle, and verifies a noncircular oriented-ellipse family. I found no decisive counterexample in the newly added modules. Nevertheless:

1. the four-coordinate raw local limit theorem for the actual return record remains unproved;
2. the completed physical theorem is still specialized relative to the requested venue standard and is substantially organized by existing collision and suspension local-limit frameworks;
3. two load-bearing functional-analytic and finite-cover inputs require sharper theorem-level justification; and
4. no independent billiards/anisotropic-spaces proof audit has occurred.

The revision-36 labels cannot be treated as evidence that any of these issues has been addressed. Editorially, the mathematical submission state is unchanged from revision 35.

## 2. Version identity and chronology

The latest visible response and referee-copy branches both point to

`8bcdf384a36b6bbc86e276b128354dc5766b99e2`.

That commit is titled “Review A2-DYN v35 at the top-four mathematics benchmark.” It adds

`reviews/a2-dyn-v35-external-top4-review-2026-10-07/REFEREE_REPORT.md`

and does not add a revision-36 manuscript.

The actual revision-35 branches both point to

`fda52bb72045204b50159e8263c05afaa6a9dc58`.

That commit adds the complete manuscript directory

`papers/A2-DYN-v35-referee-response`

and the new mathematical modules

- `core/72_action_norm_details.tex`;
- `core/73_rotation_free_arithmetic.tex`;
- `core/74_compact_family_local_principle.tex`;
- `core/75_literature_and_routes.tex`.

Accordingly, I identify the mathematical object by Git SHA and call it A2-DYN revision 35. The current revision-36 branch names are aliases for a review commit, not a mathematical revision. A subsequent author response should not cite them as a new theorem-bearing source.

The present review branch starts from the alias head so that the existing v35 report is preserved. It adds only this submission-state and supplementary referee report. No author source, prior report, workflow, historical manuscript, or unrelated path is intentionally modified.

## 3. Source qualification and verification boundary

The exact-SHA revision-35 qualification workflow completed successfully on both actual author branches:

- response run `37640998381`;
- referee-copy run `37641024948`.

The source manifest records:

- revision `35`;
- active directory `papers/A2-DYN-v35-referee-response`;
- source payload tree `5979a920272b5ec7999adb37282deca9cb4b6a16`;
- seventy inherited core files and seventy-nine inherited Python scripts preserved, subject to the declared module-70 correction;
- all inherited labels and the compiled A--X synopsis retained;
- `full_raw_return_LLT_proved: false`;
- `common_pointwise_return_correction_proved: false`;
- `full_return_complement_proved: false`;
- `independent_human_review: false`.

These source and execution checks are meaningful. They establish the exact source, successful native typesetting, consistency of finite diagnostics, and agreement of ordinary and optimized executions. They do not prove the continuum partition estimates, weighted Lasota--Yorke bounds, strong-space faithfulness, mixing of finite covers, peripheral spectral exclusion, compact-family uniformity, endpoint local-measure passage, or the resulting local theorem.

The v36 alias branches have no separate revision-36 qualification run because there is no revision-36 manuscript to qualify.

## 4. Scope of this supplementary audit

I concentrated on the additions and the points most likely to change the revision-34 assessment:

1. the explicit weak, strong-stable, and unstable norms;
2. the fixed-complexity preceding-flight multiplier;
3. the geometric Jacobian and length sums;
4. the accumulated action bounds on homogeneous and matched curves;
5. the block/equivalent-norm argument;
6. faithfulness of the strong completion and physical representation of peripheral vectors;
7. the rotation-free phase theorem;
8. the use of mixing on finite lattice covers;
9. covariance nondegeneracy and compact-parameter spectral uniformity;
10. the positive-envelope endpoint local limit;
11. the corrected varying-test Portmanteau step;
12. the oriented-ellipse verification;
13. the relation to prior local-limit theory; and
14. the separation between the completed physical theorem and the incomplete raw-return theorem.

The many inherited Gaussian, functional, marked, raw-edge, cutoff, window, and bridge statements are treated as the source-pinned baseline claimed by the packet. This report does not independently re-certify every theorem in the full article.

## 5. The action-weighted collision norms

Module 72 now gives a coherent density convention and explicit norms. The printed choices

\[
p=\frac1{12},\qquad q=\frac1{24},\qquad
\varsigma=\frac18,\qquad \zeta=\frac14,
\qquad 0<\gamma\le\frac1{100}
\]

satisfy the displayed strict inequalities. I found no arithmetic inconsistency in those choices.

The preceding-flight observable is placed on the image side of the transfer operator. Its partition is required to have, uniformly in each homogeneity strip:

- finitely many simply connected pieces;
- uniformly bounded intersections with stable curves;
- an `O(epsilon)` stable-length estimate near partition boundaries; and
- a common piecewise one-half-Hölder bound.

This is the correct type of fixed-complexity hypothesis for the cited piecewise multiplier result. The manuscript also correctly excludes refinements whose complexity grows with the orbit length.

The complex exponential and all fixed derivatives are controlled in the multiplier algebra on compact complex frequency sets. This gives a plausible analytic realization of the exact unsmoothed displacement--roof collision twist. A specialist should still compare the manuscript’s exponent conventions and closure spaces line by line with the pinned version of the Demers--Pène--Zhang multiplier lemma.

## 6. Geometric sums and the stable inequality

The revision improves the previous proof by listing the unweighted inverse-curve sums before the phase is inserted. In particular it keeps visible:

- the total stable-Jacobian sum;
- the length-weighted interpolation sum;
- the never-long growth-lemma sum; and
- the inverse-Jacobian power sum used by the unstable estimate.

The exact action identity

\[
d\tau=T^*\vartheta-\vartheta,
\qquad \vartheta=\sin\varphi\,dr,
\]

telescopes along every regular branch. Since the lattice itinerary is constant on a branch, the accumulated displacement--roof phase has a branchwise Lipschitz bound independent of the number of collisions.

For the strong stable norm, the proof subtracts the average of the pulled-back terminal test rather than the average of the entire weighted test. The contracting difference retains the stable factor, while the noncontracting derivative of the phase is charged to the weak norm through the most-recent-long-ancestor decomposition. This is the correct structural arrangement. It avoids the common error of putting an iterate-independent phase derivative into the contracting strong coefficient.

The displayed length normalizations are consistent with this decomposition. I found no immediate missing exponential word-count factor in the written stable estimate.

## 7. Matched connectors and the unstable inequality

The matched pieces are inherited from the unweighted collision construction. A connector that encounters an intermediate singularity is placed in the unmatched family. On a genuinely matched pair, the two endpoints have the same lattice itinerary, and the telescoping action identity controls the difference of roof sums by the endpoint connector lengths.

After including the trimming displacement, the manuscript obtains

\[
\|w_m^{(1)}-w_m^{(2)}\|_{C^q}
\le C_B\epsilon^{1-q}.
\]

The unstable estimate then separates:

- unmatched pieces, paid by the usual small-length exponent;
- the old graph/test difference;
- the old Jacobian difference; and
- the new phase-weight difference.

All of the printed error exponents remain strictly above `gamma`. The stable cross coefficient is retained as `C_B C_3^m`; it is not incorrectly replaced by an iterate-independent constant.

For a fixed band, the block length is chosen first. Only after that finite choice is the coefficient of the unstable seminorm chosen so that the block inequality contracts in an equivalent norm. This order is correct and does not imply any useful control as the Fourier band grows.

The most important specialist check remains whether every connector called matched is regular through every intermediate iterate and whether every required singularity or homogeneity cut is already present in the imported partition. The manuscript states this condition; the finite diagnostics cannot establish it.

## 8. A functional-analytic point that still needs clarification

The revision tries to prove that the strong anisotropic completion is faithfully represented as a space of distributions. This is necessary: an abstract peripheral vector cannot simply be declared to be a measurable phase.

The transverse-averaging argument is a reasonable route. It shows that a stable-curve pairing can be approximated by a global smooth test pairing, with the unstable seminorm controlling transverse displacement. Endpoint trimming and approximation by curves with strict cone margins are also discussed.

However, the final sentence of the proof reads, in substance, that every weak-norm pairing vanishes and then concludes `h=0` because the inclusion of the strong completion into the weak completion is injective. Read literally, that invokes the injectivity which the lemma is intended to establish.

This should be repaired in one of two explicit ways:

1. conclude directly that every strong-stable pairing vanishes and therefore `||h||_s=0`, and that every matched-pair difference vanishes and therefore `||h||_u=0`; or
2. cite an independently established injective embedding of the strong completion into distributions or into the weak completion.

The surrounding argument appears capable of supporting the first repair, so I do not identify a counterexample. But the current logical endpoint is too compressed for a load-bearing lemma at this level.

## 9. Peripheral vectors as bounded physical phases

Once faithfulness is supplied, the remaining peripheral-density construction is plausible.

Power boundedness removes nontrivial Jordan blocks on the unit circle. Cesàro averages of twisted images of a bounded smooth density converge in the strong space to the finite-rank spectral projection. Every summand is also an actual bounded physical density with a common `L-infinity` bound. A weak-star limit therefore gives a bounded measurable density `q`.

The manuscript then passes the eigen-equation through the physical weighted-composition operator by weak-star continuity, rather than evaluating a discontinuous observable on an abstract anisotropic vector. Ergodicity makes the modulus constant, and normalization gives a circle-valued phase.

This is a genuine improvement over an argument that merely asserts regularity of an approximate spectral vector. Subject to the faithfulness clarification, I found no immediate contradiction in this construction.

## 10. Rotation-free arithmetic

Module 73 removes the roof phase by measurable stable and unstable holonomy. Around sufficiently small regular product rectangles it obtains

\[
\exp\left(ib\int_Q d\vartheta\right)=1.
\]

Since `d vartheta` is nonvanishing away from grazing and such rectangles have arbitrarily small positive area, this forces `b=0`.

The residual displacement and constant collision phase are encoded in the integer cocycle

\[
(\kappa,1)\in\mathbb Z^3.
\]

If the phase kernel is proper, a finite character modulo a prime gives a function on a finite lattice cover. When the constant-step coefficient is nonzero, this function has a nontrivial unit-modulus eigenvalue. When it is zero, the sheet average makes it a nonconstant invariant function. Mixing excludes the first case and ergodicity the second.

The finite-character algebra is coherent and genuinely eliminates the circular rotation argument. The manuscript also correctly emphasizes that the constant step `1` is not the discontinuous section occupation used in the four-coordinate actual-return problem.

## 11. Finite-cover mixing is a theorem-level hypothesis

The finite-cover phase argument depends essentially on mixing of every relevant finite lattice cover. The general compact-family statement currently places connectedness of the free region, standard finite-horizon geometry, product rectangles, and finite-cover mixing under one paragraph of “uniform table geometry.”

This should be decomposed more carefully.

Connectedness of the configuration space should not be used as an unexplained synonym for mixing or for absence of a finite cyclic component of the collision map. For the general theorem, mixing of each finite cover should be stated as an explicit independent hypothesis. For the oriented-ellipse application, the paper should cite the exact theorem establishing Bernoulli or mixing behavior on those finite covers, together with the assumptions which rule out periodic decomposition.

I found no concrete counterexample for the stated triangular ellipse family. The point is therefore a required proof citation and hypothesis clarification, not a demonstrated falsehood. It is nevertheless load-bearing because the constant-step character is excluded by mixing, not merely by base-map ergodicity.

## 12. Covariance and compact-family spectral uniformity

The covariance argument is coherent at the formal level. Exponential correlation summability gives a Green--Kubo matrix. If a direction has zero asymptotic variance, boundedness of the scalar partial sums and Cesàro averaging produce an `L^2` coboundary. Exponentiation for every real scalar turns that coboundary into a phase equation. Rotation-free rigidity then forces the direction to be zero.

Finite-lag continuity plus a uniform summable tail gives covariance continuity. Compactness supplies a common positive lower eigenvalue.

For each fixed frequency band, the weighted inequalities provide power boundedness and quasi-compactness. Strong-to-weak parameter continuity and peripheral exclusion yield a uniform spectral gap on compact sets avoiding zero. Near zero, analytic perturbation identifies the Hessian of the simple eigenvalue with the collision covariance.

The proof correctly refuses to claim uniform control of these constants as the band tends to infinity.

The general theorem would be easier to reuse and audit if the following were listed as separate assumptions rather than bundled together:

- local common collision spaces;
- uniform unweighted growth and distortion estimates;
- the preceding-flight multiplier partition;
- the action identity and matched-connector regularity;
- finite-cover mixing;
- strong-to-weak parameter continuity;
- observation-cell regularity; and
- continuity of the stationary normalizations.

## 13. Positive envelopes and the order of limits

The local theorem uses a mathematically sound order of limits.

For a time test with fixed compact Fourier support, torus orthogonality and the exact endpoint transfer pairing reduce the problem to the fixed-band collision spectrum. The noncentral compact region is exponentially suppressed; the central region gives the Gaussian after rescaling.

A sharp interval is then placed between positive Beurling--Selberg lower and upper envelopes. Because the source weight is nonnegative, the inequalities survive multiplication by the actual trajectory measure. The proof first lets the collision count tend to infinity for each fixed band and only afterwards lets the band grow.

This avoids substituting a polynomially or exponentially increasing cutoff into a spectral estimate whose constants were proved only for a fixed band. The later choice `B=m^(P+3/2)` is used only in the explicit source-smoothing estimate after the microscopic denominator has already been proved.

I found no misuse of a growing frequency cutoff in the stated argument.

## 14. Endpoint measures and the corrected Portmanteau step

Revision 35 identifies and repairs a real statement/proof mismatch inherited from revision 34.

For parameter-dependent endpoint overlap tests, pointwise convergence outside a small open set is not enough. The exceptional neighborhoods must have closures of small limiting measure and null boundary so that Portmanteau controls the limsup of their source masses. Uniform convergence on the complement and a uniform local mass bound then complete the varying-test passage.

The corrected module states this stronger condition. The one-flight cell geometry is used to provide closed neighborhoods of grazing, singular, tangency, vertex-crossing, and cell-boundary sets with arbitrarily small limiting measure.

This correction is substantive and should remain visible in every theorem-level summary. It does not weaken the physical local theorem, but it shows why source identity and finite diagnostics alone are not enough to validate the continuum passage.

## 15. The oriented-ellipse application

The ellipse family is

\[
O_{a,b,\theta}
=\operatorname{Rot}_\theta\operatorname{diag}(a,b)B(0,1),
\qquad a,b\in[0.45,0.47].
\]

Every obstacle contains the radius-`0.45` disk and is contained in the radius-`0.47` disk. This gives a uniform positive inter-obstacle gap and transfers a common finite-horizon bound from the smaller circular obstacles. The printed curvature formula gives uniform positive lower and upper curvature bounds, and normalized arclength changes have common regularity bounds.

The candidate preceding-flight length is obtained from a quadratic equation with a denominator bounded away from zero. The square-root discriminant gives one-half-Hölder regularity at tangencies. Finite candidate lists and semialgebraic chart decompositions provide a plausible route to uniform finite complexity of the one-step singularity partition.

The circular locus `a=b` makes the orientation parameter redundant but does not make the table geometry singular. The covariance argument is parameter-compact and does not require a smooth inverse for that redundant parametrization.

Subject to the finite-cover mixing citation and the specialist audit of the partition/transversality statements, the noncircular verification is internally coherent.

## 16. The completed physical theorem

The stationary physical theorem concerns

\[
\{W_\lambda(t)=k,\ C_\lambda(t)=m\}
\]

at a deterministic physical time under the stationary suspension law.

The exact initial-age integration retains both initial and terminal cell offsets. The endpoint local measure evaluates the resulting finite sum of interval overlaps. The total unweighted overlap amplitude is the square of the mean roof, while the stationary source contributes the reciprocal mean roof. The clock change gives

\[
\det\mathcal V_\lambda
=\bar\tau_\lambda^{-5}\det\Sigma_\lambda.
\]

The normalization is consistent.

For the stated regular endpoint selectors, Fubini factorizes the amplitude into the product of the two stationary means. A positive selected denominator is asserted only when this product is uniformly positive.

The positive finite-band likelihood has an unnormalized source error of order `B^{-1}`. Division by the independently established `t^{-3/2}` denominator gives normalized total-variation error `O(m^{-P})` at `B=m^(P+3/2)`. Total variation then controls every bounded posterior test on the unchanged trajectory space.

The manuscript correctly does not infer a Gaussian amplitude for an arbitrary path-dependent selector from this posterior comparison.

## 17. Prior art and the significance question

The new literature section is more accurate than earlier versions. It acknowledges that:

- planar Lorentz-process local limits are classical;
- endpoint factors and geometric perturbations already occur in billiard mixing local-limit theory;
- the fixed-parameter physical conclusion belongs to suspension local-limit theory once the relevant joint observable, arithmetic group, and endpoint data are verified; and
- recording collision count does not by itself create a new arithmetic group, since it is a suspension reward up to bounded endpoint corrections.

The remaining contribution is a specific package:

1. an action-weighted norm calculation for the unsmoothed roof;
2. a rotation-free finite-cover phase argument;
3. compact-parameter uniformity;
4. a verified oriented-ellipse family; and
5. normalized source-level posterior comparison after a microscopic denominator is proved.

This is meaningful mathematics. In my judgment it does not yet provide a convincing top-four significance case. The compact-family theorem is still tied to finite-horizon periodic dispersing billiards with the standard collision anisotropic framework, one-flight observation geometry, and mixing finite covers. The ellipse application broadens the circular family but remains one closely related class.

A materially stronger top-four case would require at least one of the following:

- completion of the original four-coordinate raw-return theorem;
- a genuinely general action-weighted local-limit theorem for a wider class of singular hyperbolic systems, with several independent applications; or
- a sharp new phenomenon not already organized by existing collision and suspension local-limit frameworks.

## 18. The four-coordinate raw-return theorem remains open

The article retains as an organizing problem the actual return record

\[
J_{n,R}=(K_{n,R},N_{n,R},T_{n,R}),
\]

with three lattice coordinates and one raw continuous roof coordinate.

The completed physical theorem uses the bounded collision observable

\[
(\kappa_1,\kappa_2,\tau-\bar\tau)
\]

at a prescribed physical collision count. The finite-cover arithmetic adjoins the constant step `1`; it does not insert the discontinuous section occupation `1_{Y^*}` into the collision twist. The action estimate does not realize the unbounded induced-return observable.

Accordingly, the following remain unproved:

- the common pointwise correction for the raw return measure;
- the full return-frequency complement;
- the unconditional four-coordinate raw mixed-density LLT;
- arbitrary selected-path Gaussian amplitudes; and
- a general microscopic conditional path bridge for the inherited return pipeline.

These are central requirements of Part II. They are not editorial details and are not consequences of the new ellipse theorem.

## 19. Architecture and submission strategy

The two-part structure is an improvement. A reader can now follow the completed physical theorem through the literature comparison, norm details, arithmetic, compact-family principle, and detailed circular proof before entering the return pipeline.

The article nevertheless remains a very large hybrid submission. Part I contains a completed three-coordinate stationary physical theorem. Part II retains a long, incomplete four-coordinate raw-return program. The title continues to emphasize collision records and raw local inversion, while the strongest completed theorem is the compact-family stationary physical local law.

For a specialist or high-level dynamics/probability submission, the authors should choose one unmistakable principal endpoint:

- either complete the raw-return theorem and retain the unified article; or
- make the compact-family physical theorem the primary self-contained paper and move the unfinished raw-return programme to a clearly separate sequel or technical companion.

This is not a recommendation to delete mathematics. It is a recommendation to align the submitted theorem, title, abstract, proof route, and editorial claim.

## 20. Required changes before another top-four review

A genuinely new revision should address the following matters.

1. **Land an actual new mathematical source.** The next revision branch must point to an author commit containing a new manuscript directory or explicit in-place source changes. A review commit must not be relabeled as a theorem-bearing revision.
2. **Repair the strong-space faithfulness endpoint.** Prove directly that the stable and unstable seminorms vanish, or cite an independent injective embedding theorem. Do not finish the proof by assuming injectivity of the inclusion under construction.
3. **State finite-cover mixing explicitly.** Separate it from connectedness and provide the exact theorem or aperiodicity argument for the oriented-ellipse covers.
4. **Complete or separate the raw-return theorem.** The common pointwise correction and full return complement must either be proved in the present paper or identified as belonging to a separate future article whose incompleteness does not govern the current submission.
5. **Strengthen the generality/significance case.** Formulate the action-family mechanism at a level that clearly exceeds the existing fixed-table and suspension local-limit frameworks, and demonstrate it beyond one near-circular obstacle family.
6. **Obtain an independent specialist audit.** The multiplier partition, matched connectors, weighted Lasota--Yorke estimates, peripheral-density construction, finite-cover arithmetic, and endpoint local-measure passage should be read by experts in dispersing billiards and anisotropic transfer operators.
7. **Preserve the corrected Portmanteau hypothesis.** Every compact-family and selected-endpoint statement must retain the closed-exceptional-neighborhood and null-boundary conditions actually used by the proof.
8. **Normalize version metadata.** Branch names, manuscript dates, active directories, source manifests, qualification workflows, and referee-copy branches must identify the same mathematical revision and Git SHA.

## 21. Final assessment

Revision 35 is a substantial mathematical advance over revision 34. It makes the weighted collision proof auditable, removes rotational symmetry from the arithmetic, proves a compact-family physical local principle, and verifies a noncircular ellipse family. I found no decisive counterexample in the new modules.

Subject to specialist verification and the two clarifications above, the completed stationary physical theorem appears credible and potentially suitable for a strong dynamics or probability journal.

At the requested *Annals* / *Acta* / *Inventiones* / *JAMS* benchmark, however, the combined manuscript is not ready. Its original raw-return endpoint remains incomplete; its completed theorem has not yet been shown to have the breadth or independent significance expected at that level; and the load-bearing functional-analytic proof has not received independent expert verification.

The latest branches labeled revision 36 do not alter this assessment because they contain no new revision-36 mathematics. They are aliases for the existing revision-35 review commit. A new editorial assessment should begin only after a genuinely new author SHA is landed.

**Final recommendation: reject in the present form at the requested four-journal benchmark.**
