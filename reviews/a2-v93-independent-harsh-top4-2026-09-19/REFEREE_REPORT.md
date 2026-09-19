# Independent harsh referee report on A2 revision 93

**Review date:** 19 September 2026  
**Repository:** TrillionniumFoundation/theta-theory  
**Reviewed revision branch:** revision/a2-v93-constrained-newton-gauge-2026-09-19  
**Reviewed branch head:** 2832f7a7060217f6c8110688b66b73b9b946d13a  
**Previous revision:** revision/a2-v92-sharp-modulus-and-singular-normal-forms-2026-09-19 at d55c480f8cdf9f1327b4142bf1bb31a315f71b2b  
**Controlling previous report:** reviews/a2-v92-independent-harsh-top4-2026-09-19/REFEREE_REPORT.md at 37e03652f639930f5489dfee09150a7cba3964d7  
**Reviewed manuscript:** *Projective polynomial observations: intrinsic geometry and additive normalization*  
**Author:** Qian Qi

## 1. Recommendation

**Recommendation to the editor: reject in the present form at the stated four-leading-general-mathematics-journal level.**

This recommendation should not be read as a repetition of the v92 report. Revision 93 makes a serious mathematical advance and, in my view, essentially closes the most important positive-rational perturbation question identified as Option B in the previous report.

The new constrained determinant theorem is the right replacement for the insufficient first-order Laurent exposure test. It retains all homogeneous determinant terms, gives a finite Newton-type exponent, pulls the leading root geometry through the local Hellinger metric, and produces a finite variational formula for the leading diameter. The free-normalizer corollary also resolves the specific v92 cancellation problem at fixed data: in the full positive rational experiment the local exponent is controlled by the actual resolvent pole, not by the larger flag-path certificate. The binary refactorization lemma, the pointed-versus-intrinsic fibre distinction, the fixed-margin eta comparison, and the source-provenance repair are all real improvements.

The reason I nevertheless do not recommend the paper at the stated level is now more structural and more concentrated.

The decisive new theorem is exact for an **affine linear numerator slice of the positive rational extension**. It is not yet an invariant of the **nonlinear admissible germ of the original stochastic model**. This distinction is harmless when the first derivative is visible, but it becomes decisive precisely in the regime the paper now wants to classify: when first-order exposure vanishes. At that point the second and higher jets of the stochastic coefficient map can contribute at the same or lower Newton order as the higher homogeneous determinant terms computed on the affine tangent slice. Revision 93 does not prove that the stochastic model can be straightened to the affine slice to the required order, nor does it formulate the Newton invariant for a general analytic or semialgebraic admissible germ.

Thus the paper now has an excellent local theorem for a broader ambient rational experiment, while the hardest intrinsic singularity question in the original stochastic experiment remains unresolved. The binary multi-defect intersection is still completely spectrally nonidentifiable, with a nonzero exact-fibre diameter, and the new affine-slice theorem does not by itself replace the missing identifiable multi-defect normal form.

There are also two technical issues that should be repaired independently of journal level. First, the claimed invariance under arbitrary constant invertible left-right numerator changes does not presently transport the Hellinger/Fisher metric in the statement or proof, even though the leading constant depends on that metric. Second, several “intrinsic” claims are intrinsic only under linear reparametrizations of the affine slice, not under nonlinear changes of the admissible germ.

Revision 93 therefore changes my assessment substantially: the constrained rational perturbation program is now mathematically convincing, but the manuscript still does not have the single model-intrinsic theorem that would make its many layers cohere at a top-four general-journal level.

## 2. Scope of this review

I reviewed the exact branch head 2832f7a7060217f6c8110688b66b73b9b946d13a.

Relative to v92, the v93 branch is three commits ahead and adds the following principal mathematical and review-delivery sources:

- article/v93/constrained_newton.tex;
- article/v93/fibres_and_admissibility.tex;
- article/v93/paper.tex;
- rigidity_v93.tex;
- revisions/a2-v93/RESPONSE_TO_REFEREE.md;
- revisions/a2-v93/SOURCE_MANIFEST.json;
- revisions/a2-v93/verify_a2_v93.py;
- .github/workflows/a2-v93-native.yml;
- the retained v92 referee report;
- A2_REVISION_V93_REVIEW_READY.md.

The v93 manifest declares 24 active TeX inputs and explicitly requires the inherited proof and bibliography modules to remain active. I read the new theorem and proof modules in full, the new introduction, the response to the referee, the previous v92 report, the inherited common-flag material needed to interpret the new corollaries, and the verification/workflow code.

I treat the Python diagnostics as regression checks only, exactly as the revision itself says. They are not substitutes for universal proofs.

At the time this report was prepared, GitHub Actions run 35438705506 for the exact reviewed head was still **queued**, with no conclusion. The v93 workflow is materially better than the v92 workflow because it triggers on every push to the revision branch and has no restrictive path filter. But a queued run is not evidence of a successful complete build, so I do not record the exact-head native manuscript as remotely verified.

## 3. What revision 93 genuinely fixes

### 3.1 The first-order exposure gap is essentially closed in the affine positive-rational experiment

Theorem “Exact constrained observation modulus” is the central mathematical advance of v93.

For an affine linear perturbation space S, the paper expands

    det(M + E_x) = D + sum_j D_j,

with D_j homogeneous of parameter degree j. At each base root r of multiplicity m_r, it retains every coefficient H_{r,j,a} below order m_r and defines

    alpha_r(S) = min j / (m_r - a).

This is the correct finite Newton-type invariant for the affine slice. It directly answers the main criticism of v92: the first Laurent trace can vanish identically while a higher determinant term moves the spectrum.

The proof is also substantially better than a mere order estimate. It combines:

- injectivity of the local rational observation chart under tau(P)>0;
- the radius-two Fisher ellipsoid induced by the manuscript’s Hellinger convention;
- uniform root localization;
- Newton rescaling on each repeated-root cluster;
- convergence of root multisets rather than labelled roots;
- a finite variational leading diameter over the limiting ellipsoid.

The quadratic-exposure family is a useful and convincing witness that the j=1 Laurent filtration is genuinely insufficient.

I regard this part of the v92 objection as resolved for the experiment that is actually stated.

### 3.2 The cancellation-aware free-normalizer exponent is fixed at a datum

Corollary “Exact exponent with a free monic normalizer” is also an important repair.

The v92 report objected that cancellation information was lost when the normalizer was allowed to vary. Revision 93 now proves, on the full affine rational space S_all, that the exponent at a root is the reciprocal of the true resolvent pole order. Constant rank-one perturbations expose the leading Laurent matrix, and the local rational chart converts coefficient size into Hellinger size.

This is exactly the pointwise statement that v92 did not have.

The manuscript is appropriately careful not to insert the true pole order into the older boundary-uniform common-flag theorem while keeping the old uniform constants. That distinction is mathematically responsible.

### 3.3 The scalar-gauge discussion is now algebraically complete at total homogeneous degree

The scalar interpolation map is used as a linear shear between the total-normalizer coordinates and the zero-sum coordinates. At the level of the complete determinant polynomial, total homogeneous degree is preserved by this invertible linear change of variables.

This is the right way to state cancellation covariance. It is much better than tracking individual triangular paths and hoping that their cancellations survive a gauge change.

### 3.4 The intrinsic/pointed/fibre distinction is repaired

The new fibre section explicitly separates:

1. the intrinsic observation germ;
2. a pointed latent germ at a chosen representative;
3. strata inside the exact fibre.

This directly repairs one of the conceptual defects in the v92 binary discussion. The manuscript no longer treats the repeated common-polynomial representative as an intrinsic label of the observation datum when the exact fibre contains many different multiplicity patterns.

That clarification should be retained.

### 3.5 The binary whole-model perturbation is now properly justified

The analytic stochastic refactorization lemma is exactly the sort of named result requested in the previous report.

The proof identifies the normalized coefficient X = C A^{-1}, uses its simple real spectral projectors, reconstructs rank-one positive coefficient matrices, and then recovers strict weights and stochastic columns. This is a satisfactory local admissibility argument for the displayed binary tangent.

I no longer regard the lower perturbation in the binary theorem as merely an algebraic-pencil construction.

### 3.6 The fixed-margin eta comparison is now stated correctly

The compact regular equivalence proposition gives two-sided comparability between the exact Fisher condition and eta_d^{-1} on a class with fixed positive margins.

The result is valid as a compactness statement and cleanly avoids the vanishing-cell counterexample. This closes the specific positive compact-class question raised in v92.

I discuss below why I do not view this proposition as a major new theorem.

### 3.7 The provenance contract is substantially improved

The v93 workflow now triggers on every push to the revision branch. The manifest distinguishes the previous review, previous revision, source snapshot, and runtime head. The verifier checks the complete TeX input graph and inherited source identities.

This is a genuine improvement over the v92 path-filter defect.

The remaining issue at review time is operational rather than structural: the exact-head workflow run is still queued and therefore has not yet supplied a successful remote build receipt.

## 4. Major objection I: the new exact invariant is an affine-slice invariant, not yet a stochastic-germ invariant

This is the most important point in the present report.

Theorem “Exact constrained observation modulus” assumes an exact affine coefficient model

    M_x = M + E_x,

where x maps linearly into a fixed real vector space S of polynomial numerator perturbations.

That is a legitimate and useful experiment. It is also exactly the positive rational extension declared in the theorem.

But the original stochastic model does not generally have an affine coefficient germ in its natural parameters. Its numerator coefficients are built from products of channel factors, weights, and component-polynomial coefficients. Near a singular point, the coefficient image has a nonlinear semialgebraic or analytic germ.

Write a local coefficient parametrization schematically as

    M(x) = M + E_1(x) + E_2(x) + E_3(x) + ...,

where E_j is homogeneous of parameter degree j.

Revision 93 computes the full determinant expansion of

    det(M + E_1(x))

when the allowed affine space is identified with the first-order coefficient directions.

That is not the same as the determinant expansion of the actual germ

    det(M + E_1(x) + E_2(x) + ...).

When the first-order determinant exposure is nonzero, the difference may be higher order and irrelevant. But when the first-order exposure vanishes, which is exactly the regime motivating v93, the term obtained by applying the first determinant derivative to E_2(x) can compete with or dominate the quadratic determinant term generated by E_1(x).

In other words, higher determinant degree and higher model-jet degree are different sources of order. The current invariant sees the former on an affine slice; it does not yet see the latter for a curved admissible germ.

A toy scalar mechanism already shows why tangent information alone cannot determine a singular exponent: a coefficient curve of the form c(x)=x^2 has zero first derivative but is not locally constant. Two analytic germs can have the same tangent space and different leading spectral orders. This is not a counterexample to the v93 theorem, because the theorem never claims otherwise. It is a counterexample to using the affine theorem as an intrinsic classification of a nonlinear singular model without an additional straightening or jet theorem.

### What is needed

The natural next theorem is a jet-level constrained Newton principle.

One should compose the determinant with the full admissible analytic or semialgebraic coefficient germ, collect terms by total parameter order after that composition, and define the Newton edge from those composed homogeneous jets. The Hellinger metric must be expanded in the same local model coordinates.

Alternatively, the paper could prove a strong straightening theorem showing that, on the relevant stochastic strata, the coefficient image is analytically equivalent to the affine slice to every order that can contribute to the leading Newton edge.

Without one of these statements, the strongest new theorem in v93 does not yet solve the singular geometry of the model named in the title.

## 5. Major objection II: the hardest intrinsic stochastic singularity remains open

The previous report offered several routes that could materially change the top-four assessment. Revision 93 successfully executes the positive-rational constrained-invariant route.

However, the model-specific multi-defect problem remains where it was.

The binary full-collapse datum still has an exact fibre of positive spectral diameter. Its intrinsic observation modulus does not vanish at the base point. The new fibre section correctly says so.

The nontrivial fractional singular theorem for repeated roots still sits on a stratum where coefficient recovery is regular. The genuinely difficult situation in the original stochastic model would combine, for example:

- tau(P)=0 or channel-rank loss;
- at least one additional algebraic defect;
- an exactly identifiable spectral target, so omega_P(0)=0;
- a nontrivial nonlinear observation modulus generated by the intersecting defects.

Revision 93 still does not provide such a point.

This matters more now, not less, because the manuscript’s introduction presents global additive normalization, exact local constrained geometry, quotient geometry, singular root extraction, and intrinsic fibre geometry as parts of one theory. The new affine rational theorem is a strong ambient result, but it does not yet supply the missing bridge at a singular point of the original stochastic experiment.

For a specialist paper, the separation of experiments is acceptable and clearly stated.

For a leading general journal, I would want the paper’s main new invariant to be applied to the model’s own hardest singularity, or a theorem explaining why the model’s singular germ reduces to the affine rational geometry.

## 6. Major objection III: the left-right invariance claim does not presently transport the Hellinger metric

Theorem “Exact constrained observation modulus” states that constant invertible left and right changes of numerator coordinates give the same result when the normalization functional and allowed space are transported.

The determinant part of this is clear: constant invertible left-right multiplication changes the determinant by a fixed nonzero factor, so the algebraic Newton exponent is preserved.

The leading constant C_S is different. It is defined using the limiting ellipsoid coming from the Hellinger/Fisher metric of the observed probability cells.

An arbitrary invertible left-right transformation of the numerator is not an isometry of that entrywise Hellinger metric. In general it does not even preserve the probability simplex if one treats the transformed entries as new observed cells.

The proof of the theorem addresses the determinant scaling, but it does not prove invariance of the observation ellipsoid under arbitrary invertible left-right changes.

There are two correct ways to formulate the result:

1. treat the transformation as a pure coordinate change and explicitly pull back the observation metric together with the normalization functional and perturbation space; or
2. restrict the invariance claim to transformations that preserve the observed statistical experiment.

As currently written, the algebraic exponent is invariant under the broader transformation, but the metric leading diameter is not justified without an explicit metric transport.

This is a repairable issue, but it concerns the word “exact” and should be fixed.

## 7. Major objection IV: “intrinsic” currently means linear-coordinate intrinsic, not germ intrinsic

The theorem correctly proves invariance under a change of basis in S. The scalar gauge is also an invertible linear change of coefficient coordinates.

That is useful.

But the manuscript repeatedly uses the language of intrinsic geometry, and the new result is not invariant under a general nonlinear reparametrization of an admissible coefficient germ unless the full germ is transformed and the higher jets are retained.

This is closely related to Major Objection I, but it is worth separating the conceptual issue from the missing application.

For an affine vector space, basis invariance is a complete coordinate statement.

For a singular model germ, it is not.

The paper should therefore distinguish at least three notions:

- basis invariance inside a fixed affine coefficient slice;
- invariance under linear gauge shears of that slice;
- invariance of the local observation germ under analytic or semialgebraic reparametrization.

Revision 93 proves the first two, not the third.

The current title and abstract make this distinction easy to miss.

## 8. The free-normalizer pole theorem is strong but much of its algebraic core is classical

The free-normalizer corollary is mathematically useful and closes a real gap in the manuscript.

At the same time, once the full coefficient perturbation space is available, the reciprocal resolvent-pole exponent is close to the classical unstructured multiple-eigenvalue or matrix-polynomial perturbation picture. The genuinely paper-specific content is:

- identifying the correct probability-normalized affine perturbation space;
- proving that the observation map supplies an injective local coefficient chart;
- pulling the sharp root geometry through the Hellinger metric;
- integrating the scalar normalizer with the same coefficient perturbation.

The paper now says many of the underlying perturbation mechanisms are classical, which is good. But the novelty discussion should be even sharper about which part of Corollary v93 is new and which part is the observation-theoretic realization of a classical pole-order fact.

At a top-four journal, the distinction matters. The more general the ambient rational theorem becomes, the more carefully the paper must isolate the genuinely new model geometry.

## 9. The two-scale Newton law is not an intrinsic statistical two-scale theorem

Proposition “Two-scale Newton law” is a correct finite coefficient-box statement as far as I can see.

But the scalar and zero-sum coordinates depend on the interpolation operator I_d. The manuscript itself notes that changing I_d shears the two coordinate groups and that separate coefficient boxes must be transported.

This means the bidegree exponent is not, by itself, an intrinsic statement about two independently observed statistical errors.

The paper explicitly says these are coefficient boxes, not independent observation balls. That qualification is essential and should be kept close to every use of the proposition.

I would not advertise this result as a definitive two-scale statistical geometry until a canonical observation-space decomposition is supplied.

The total homogeneous invariant is the genuinely coordinate-stable object here.

## 10. The fixed-margin eta equivalence is useful but essentially a compactness corollary

Proposition “Compact regular equivalence” answers a question from the v92 report, but its proof is mostly:

- both quantities are continuous;
- both are finite and strictly positive;
- the class is compact;
- therefore their ratio has positive finite extrema.

That is correct.

It does not identify quantitative dependence on the margins, a maximal natural regular class, or a structural formula relating eta_d to the Fisher condition.

I therefore regard it as a useful closure lemma, not a major conceptual advance.

This matters only for contribution accounting. The proposition should not carry the same rhetorical weight as the constrained determinant theorem.

## 11. The binary refactorization lemma is a success

I want to record this separately because the previous report was skeptical about the “whole-model” lower perturbation.

The new lemma gives the missing proof.

For a binary pencil with simple real roots, the spectral projectors of C A^{-1} reconstruct rank-one coefficient matrices. Strict positivity and full rank persist locally, and the sums recover strict weights and stochastic columns.

This is the correct local argument.

I have no remaining rejection-level objection to that particular admissibility step.

## 12. Complex-root conventions should be made explicit in the new theorem

The positive rational extension permits complex determinant roots.

The manuscript’s bottleneck formula d_infinity = min over permutations of the maximum absolute root difference naturally extends to complex multisets, and earlier inherited material already uses it for complex roots.

Still, the v93 theorem should state explicitly that its root multisets live in C and that the absolute value is the complex Euclidean modulus. At a real base root, real perturbations may generate conjugate pairs; at a nonreal base root, conjugate clusters are coupled by the real coefficient constraint.

None of this appears to invalidate the proof, but an “exact leading diameter” theorem should make the target metric completely explicit.

## 13. The pointwise cancellation theorem and the uniform flag theorem are still two different theories

Revision 93 is correct to preserve the older common-flag theorem.

The new pointwise rational result says that at a fixed datum the true resolvent pole controls the exact local exponent.

The older global theorem gives a boundary-uniform additive certificate based on a flag and path counts, with constants that remain controlled over a much larger moving class.

These are genuinely different quantifier structures.

The manuscript now explains this better than v92 did.

However, the paper still lacks a theorem describing how the exact pointwise constants degenerate into the uniform path certificate as tau, cell margins, or algebraic separation approach a boundary. Such a theorem is not logically required, but it would provide the conceptual bridge that the current architecture still lacks.

At present the reader must accept two parallel regimes:

- an exact but datum-dependent local theory;
- a less sharp but boundary-uniform global theory.

That is coherent, but not yet unified.

## 14. The manuscript remains too architecturally diffuse for the stated journal target

The active v93 manuscript imports 24 TeX modules accumulated across several revision generations.

The mathematical content now spans at least:

1. scalar normalization identification;
2. endpoint clock complexity;
3. global additive polynomial recovery;
4. quotient charts and exact Fisher geometry;
5. Hellinger observation-ball minimax theory;
6. real-rooted quartic singularity theory;
7. arbitrary closed-model semialgebraic moduli;
8. common-flag matrix-polynomial perturbation bounds;
9. cancellation-aware affine rational Newton geometry;
10. adaptive design and inference statements.

Each layer is legitimate.

The problem is not simply length. The problem is that the paper still has more than one candidate central theorem.

Revision 93 makes the constrained determinant theorem a plausible conceptual center, but that theorem belongs to the positive rational affine extension, whereas much of the statistical and intrinsic singularity theory belongs to the original closed stochastic model.

A top-four paper can be broad if the breadth is forced by one principle. The present manuscript still reads as a highly developed research program compressed into one article.

The decisive next step is not another auxiliary proposition. It is a theorem that makes the new Newton invariant genuinely intrinsic to the stochastic model, or a reorganization in which the rational theorem is clearly the central object and the stochastic results are consequences.

## 15. Statistical layer: still strong, but not yet integrated with the new v93 theorem

My positive assessment of the v92 statistical results remains.

The regular Fisher covariance, finite-permutation quotient at cross-component collisions, exact Hellinger-ball bridge, arbitrary-point minimax equivalence, and repeated-root quartic profile are among the stronger parts of the manuscript.

What v93 does not yet provide is a statistical theorem for the new constrained Newton edge beyond the local deterministic Hellinger modulus itself.

For example, one could combine the exact affine rational modulus with the existing two-point minimax machinery to state the exact local risk exponent and, where possible, the leading decision constant on the rational experiment. More importantly, one could do the same after composing the Newton construction with an actual stochastic singular germ.

That would make the new theorem interact with the paper’s statistical half instead of sitting next to it.

This is not a correctness objection. It is another sign that the manuscript has not yet found its final conceptual compression.

## 16. Reproducibility and exact-head audit

### 16.1 The v92 workflow-trigger defect is repaired

The v93 workflow triggers on every push to revision/a2-v93-constrained-newton-gauge-2026-09-19.

There is no paths filter that can silently exclude a manuscript-only or manifest-only change.

This is the right design.

### 16.2 The manifest fields are much clearer

The v93 manifest distinguishes:

- previous_review_commit;
- previous_revision_head;
- revision_source_commit;
- revision_source_tree;
- a runtime revision_head policy.

This is substantially clearer than the ambiguous v92 provenance fields.

### 16.3 The verifier checks the complete active graph

The verifier recursively resolves the TeX input graph and requires exact equality with the manifest’s active_tex set. It also checks inherited identities and rejects modifications or removals relative to the controlling review commit.

This is a meaningful source-preservation audit.

### 16.4 The exact-head native run is not yet completed

At the time of review, Actions run 35438705506 for head 2832f7a7060217f6c8110688b66b73b9b946d13a is still queued with no conclusion.

Therefore I do not certify:

- successful complete TeX compilation at the reviewed head;
- absence of unresolved references in the remote build;
- absence of overfull boxes in the remote build;
- successful execution of the exact source audit at the reviewed head;
- existence of the promised exact-head artifact.

This is a status statement, not evidence of a failing workflow.

The report should be updated if a completed run is later used as part of a delivery claim.

## 17. Smaller mathematical and expository comments

### 17.1 Clarify the neighbourhood in omega_P^S

The affine rational modulus is local because x is restricted to a sufficiently small coefficient neighbourhood. Put that restriction directly into the formal definition of the competitor set, not only in the preceding prose.

Otherwise a reader may wonder whether remote exact fibres of the rational parametrization can enter the Hellinger ball.

### 17.2 Separate algebraic invariance from metric invariance

The determinant exponent is invariant under more transformations than the Hellinger leading constant.

State these as separate assertions.

### 17.3 The notation H_e M is easy to misread

The symbol looks like multiplication by a scalar interpolation polynomial, but it denotes an interpolation operator applied to e(T_j)P_j.

A notation such as G_e or T_P(e) would reduce ambiguity.

### 17.4 State the complex bottleneck metric explicitly

As noted above, the inherited formula extends naturally, but the new theorem should say so.

### 17.5 Explain the relation between alpha=infinity and local determinant rigidity

The proof is short and correct in spirit: every perturbed determinant retains all base roots with their full multiplicities and has the same degree. A one-sentence algebraic lemma before the theorem would make the conclusion easier to parse.

### 17.6 Do not let the compact eta proposition look deeper than it is

Its value is closure of a comparison question, not a new mechanism. The exposition should reflect that.

### 17.7 Fix the diagnostic assertion message

In verify_a2_v93.py, the invisible-first-variation test checks that h/g is analytic at zero, but the failure message says “first variation has pole.” The test condition is the intended one; the message is backwards.

This is minor but easy to fix.

### 17.8 Be precise about which positive rational perturbations remain stochastic

The quadratic-exposure family correctly does not claim stochastic factorization of its alternatives. Keep that distinction visible whenever the example is summarized.

### 17.9 The new abstract is much better, but still dense

The abstract now distinguishes fixed-datum exact geometry from uniform flag bounds. That is an improvement. It still contains too many theorem families for a general-journal reader to identify the single conceptual novelty immediately.

## 18. What would change my recommendation

A further revision could materially change my recommendation if it proves one definitive bridge theorem rather than adding another independent module.

The strongest route would be:

### Option 1: a jet-level constrained Newton theorem for the actual admissible germ

Let the admissible coefficient map be analytic or semialgebraic rather than affine. Compose the full determinant with its homogeneous jets, define the exact Newton exponent from the composed germ, pull the result through the observation Hellinger metric, and prove a leading root-multiset variational law.

Then apply the theorem to an actual singular point of the stochastic model where:

- coefficient recovery is singular;
- at least one other defect is present;
- the exact spectral fibre is a singleton;
- the resulting intrinsic modulus has a nontrivial fractional exponent.

That would connect the strongest v93 idea directly to the hardest remaining model-specific problem.

### Option 2: an analytic straightening theorem

Prove that, on the relevant stochastic singular stratum, the coefficient-image germ is analytically equivalent to an affine slice up to every order that can affect the leading Newton edge. Then the current v93 theorem would become genuinely intrinsic to that stratum.

### Option 3: a single unified local-to-uniform degeneration theorem

Relate the datum-dependent exact Newton constant and true pole order to the boundary-uniform additive flag certificate as the regular margins degenerate. Such a theorem would not by itself solve the nonlinear stochastic-germ issue, but it would substantially strengthen the conceptual unity of the paper.

In all cases, the left-right metric invariance statement should be repaired, and the exact-head native build should have a completed successful receipt before the revision is presented as fully audited.

## 19. What I would regard as publishable now

Ignoring the stated top-four target, I regard v93 as a strong and serious specialist-level contribution.

The following package is now especially convincing:

1. projective scalar-normalizer identification;
2. observable joint-projector recovery;
3. additive global inverse stability;
4. exact regular quotient/Fisher geometry;
5. arbitrary-point Hellinger modulus and minimax equivalence;
6. profiled quartic repeated-root geometry;
7. common-flag uniform perturbation bounds;
8. exact constrained Newton geometry on affine positive-rational slices;
9. cancellation-aware free-normalizer local exponents.

That is a substantial body of mathematics.

My negative recommendation is therefore about the standard and architecture of a four-leading-general-mathematics-journal submission, not about the absence of technical results.

## 20. Final assessment

Revision 93 is the strongest A2 revision I have reviewed in this sequence.

It does not merely patch exposition. It supplies the theorem that the v92 report explicitly identified as the natural completion of the constrained-exposure program. The quadratic-exposure example demonstrates why that theorem is needed, the free-normalizer corollary repairs the cancellation gap, and the proof gives an exact leading metric object rather than only a Hölder order.

I therefore consider the following v92 objections substantially resolved:

- first-order Laurent exposure is no longer treated as a classification;
- cancellation-aware local sharpness survives a free monic normalizer at a fixed datum;
- the binary algebraic lower direction is now proved stochastic;
- the intrinsic-versus-pointed fibre language is repaired;
- eta_d has a positive fixed-margin comparison theorem;
- the provenance/workflow design is substantially cleaner.

The remaining top-four obstacle is different.

The paper’s new exact invariant is exact on an affine positive-rational coefficient slice, while the original stochastic model has a nonlinear admissible germ. At singular points where first-order exposure disappears, higher jets of that germ can alter the leading Newton order. The manuscript does not yet prove a germ-level invariant or a straightening theorem, and it still does not compute a genuinely intersecting but spectrally identifiable singularity of the original stochastic model.

Accordingly, the paper now contains a convincing solution to a hard ambient perturbation problem, but not yet the model-intrinsic unification that would make the entire manuscript feel inevitable at the stated general-journal level.

For that reason my recommendation remains **reject at the four-leading-general-mathematics-journal level in the present form**, with a materially more positive mathematical assessment than in v92.

---

*This is an owner-requested independent external-referee-style assessment of the repository manuscript. It is not a journal-commissioned report and does not represent an editorial decision.*
