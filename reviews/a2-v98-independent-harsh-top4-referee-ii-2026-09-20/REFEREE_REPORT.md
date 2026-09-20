# Independent harsh referee report — A2 revision 98, referee II

**Manuscript:** *Projective polynomial observations: joint spectral atlases and a weight-wall transition*  
**Repository:** TrillionniumFoundation/theta-theory  
**Reviewed manuscript branch:** revision/a2-v98-relative-spectral-atlas-proof-2026-09-20  
**Reviewed exact head:** 72faee076147dbabd3c50a8cd46390f770102a0e  
**Manuscript source commit identified by the authors:** b5691d8d3cc6a62295bfb8b2578be024b5e0c423  
**Principal entrypoint:** papers/A2-v17-boundary-information-coarsening/rigidity_v98.tex  
**Principal source:** papers/A2-v17-boundary-information-coarsening/article/v98/paper.tex  
**Controlling v97 manuscript head:** 5c8b57c655aaec0df76dc3178554de2d1736b076  
**Date:** 2026-09-20  
**Standard applied:** Annals of Mathematics / Acta Mathematica / Inventiones Mathematicae / JAMS level

## 1. Recommendation

**Recommendation: reject in the present form at the level of a top-four general mathematics journal.**

This is not the same report I would have written on revision 97.

Revision 98 is a substantial mathematical response. It does not merely restate the earlier programme. It adds a genuine spreading lemma, a theorem-level relative real-principalization statement, a separate semialgebraic uniform-decay proposition, a quantitative cross-rank inverse, a complete remote tangent-cone proposition, and a sharper quadratic remainder for the remote entrance law. I do not find a fatal algebraic counterexample to the explicit multiplicity formulas, the cubic fibre classification, the local Fisher programmes, or the weight-wall mechanism. Several objections that were serious in revision 97 have been materially answered.

The negative recommendation now rests on three different issues.

First, the broad theorem that is supposed to organize the paper — the finite real spectral atlas in families — still depends on algebraic-geometric and real-semialgebraic interfaces whose proofs are compressed below the standard required for a theorem that is intended to be cited independently. The architecture is plausible; the current text is not yet a reference-grade proof of that architecture.

Second, the effectivity claim is stronger than the algorithmic infrastructure actually specified. The manuscript often knows that a finite construction exists, but a statement that finite algorithms compute all strata, monomial data, leading sets, and algebraic constants requires a more exact computational model and more precise algorithmic citations than are currently provided.

Third, and independently of correctness, the top-four significance case remains underdeveloped. The revised comparison with current Łojasiewicz-exponent literature is much better, and the manuscript correctly concedes finite-max and wall-chamber antecedents. But the object that is now presented as the main new invariant — the joint weighted real initial coefficient set and its root-multiset image — is not compared seriously with the broader literature on semialgebraic or o-minimal preparation, weighted tangent or initial cones, definable metric geometry, and parameterized asymptotics. Without that comparison, it is not yet clear whether the general atlas theorem is a genuinely new structural theorem or a technically competent assembly of established machinery around a new application.

At a specialist-journal standard I would be considerably more positive. At the stated top-four standard, the paper has not yet crossed the bar.

## 2. Source control: what I actually reviewed

The repository contains a branch named revision/a2-v99-joint-invariants-and-remote-entrance-2026-09-20. I did **not** treat the branch name alone as evidence that v99 is a later manuscript.

A direct comparison shows that v99 is exactly one commit ahead of v98 and that the only added file is

reviews/a2-v98-independent-harsh-top4-2026-09-20/REFEREE_REPORT.md.

There is no v99 manuscript source change in that branch. Thus the latest actual paper revision available to this referee is A2 revision 98 at exact head

72faee076147dbabd3c50a8cd46390f770102a0e.

This report is therefore based on the v98 manuscript itself, its v98 response document, the v97 report to which it responds, the exact finite-regression material, and the branch-scoped build metadata. I also checked the current public description of Hà's arXiv:2602.18410 and agree with the manuscript's revised acknowledgement that finite-max, family stability/stratification, and wall-chamber phenomena cannot be advertised as absent antecedents.

There already exists a separate v98 review branch in the repository. I read it only after independently auditing the principal theorem chain. The present report is a second external-style assessment, not an endorsement by reference to the earlier review.

## 3. What revision 98 genuinely fixes

The paper should receive credit for real progress.

### 3.1 The former generic-fibre blueprint has become an actual theorem architecture

Revision 97 placed too much weight on a paragraph that effectively said: resolve generically, spread, stratify, and conclude uniformity. Revision 98 replaces that with distinct statements:

- Lemma 3.3: spreading a finite resolution certificate;
- Theorem 3.4: relative real principalization;
- Theorem 4.1: the definable joint initial family;
- Proposition 4.2: semialgebraic decay on strata;
- Theorem 4.3: uniform spectral power law;
- Theorem 4.4: finite real spectral atlas;
- Theorem 5.1: effective algebraic specialization.

This is the correct decomposition.

### 3.2 The literature correction is substantial

The manuscript now explicitly grants classical resolution and principalization, divisor-ratio calculations, Hardt triviality, and the current Hà finite-max / chamber results. In particular it no longer presents the existence of a finite candidate set or wall-chamber structure for scalar Łojasiewicz exponents as a missing antecedent.

That correction materially improves the originality discussion, even though it does not finish it.

### 3.3 The rank-crossing inverse is now load-bearing mathematics rather than expert shorthand

Proposition 7.2 and Lemmas 7.3–7.4 give an actual quantitative mechanism:

1. recover the second-marginal coefficient matrix;
2. obtain a uniform inverse for the competing second channel;
3. place competing component polynomials in a controlled neighbourhood of the affine pencil;
4. isolate the two relevant pencil endpoints by discriminant and depressed-cubic arguments;
5. recover the rank-one coefficient matrices by dual coefficient functionals;
6. recover weights and stochastic channels without dividing by det U.

This directly addresses one of the weakest parts of the prior revision.

### 3.4 The remote tangent cone is now a theorem

Proposition 8.1 is a genuine improvement. It identifies a local Nash chart, records exactly four one-sided directions and seven free directions, proves secant completeness, proves converse feasible realization, handles the component permutation, and supplies exact second-order coefficient identities.

I no longer regard the remote tangent-cone identification itself as a principal objection.

### 3.5 The quadratic entrance remainder is now supported by the local factorization

At the remote simple/double configuration the polynomial coefficients are analytic in the scale parameter even though individual roots split at square-root scale. The exact product identities justify replacing the previous generic O(delta^(3/2)) estimate by

d_rem(delta) = mu_E delta + O(delta^2).

The manuscript also correctly avoids transferring this stronger remainder to unrelated singularities.

### 3.6 The evidence boundary is responsibly stated

The scripts are labelled as finite exact regressions rather than universal proof verification. The response distinguishes a locally compiled principal article from a not-yet-certified exact-head full archive. That is good practice.

These improvements are important because they narrow the remaining dispute: the paper is no longer failing because the explicit calculations are written as hand-waving. It is failing because its broadest general theorem and its significance claim still carry more weight than has been justified.

## 4. Main objection I: Lemma 3.3 is now a central algebraic-geometric theorem, but it is still written as a compressed proof schema

Lemma 3.3 is not a technical aside. Theorem 3.4, and therefore the advertised finite family atlas, rests on it.

The strategy is mathematically sensible: construct a finite certificate over K = k(S), spread every finite piece of data, localize the base until smoothness and normal-crossing conditions persist, arrange base change for the blow-ups, and recurse on the exceptional base.

The problem is not the strategy. The problem is that several genuinely nontrivial specialization statements are still passed over in prose.

### 4.1 A finite diagram should be spread as a finite diagram

The lemma begins with a generic chain

Y_{0,K} ⊃ Y_{1,K} ⊃ ... ⊃ Y_{q,K} = ∅

and projective maps Z_{j,K} → Y_{j,K} that are isomorphisms on specified locally closed differences. The proof says that all equations, inverse maps, and identities involve finitely many coefficients in K and therefore spread after inverting finitely many denominators.

For individual morphisms this is standard. What is used later is stronger:

- the entire locally closed decomposition has the intended fibres;
- the spread inverse maps remain inverse on the correct fibrewise complements;
- no additional fibre component changes the first index j for which a point belongs to Y_j \ Y_{j+1};
- the finite source family still covers every retained fibre point in exactly the way required by Theorem 3.4.

This should be a precise finite-diagram spreading lemma, with hypotheses and conclusions stated in scheme-theoretic language. “All data use finitely many equations” is not a substitute for checking all fibrewise incidence and complement statements.

### 4.2 Reducedness and fibre components cannot remain optional prose

The sentence that reduced structure is immaterial to real points, and that fibrewise reducedness “may also be imposed,” is too loose.

Nilpotents do not alter the real point set. But the next theorem reasons about:

- irreducible and vertical components;
- smooth loci;
- whether a function becomes identically zero on a fibre component;
- the dimension descent of exceptional pieces;
- Zariski density of real smooth points.

Those statements do depend on which reduced schemes and components are being used.

The paper should specify, at every stage, which family is replaced by its reduction, where geometric reducedness is needed, and why component behaviour is stable on the retained base open set.

### 4.3 The blow-up base-change paragraph deserves its own lemma

This is one of the best new pieces of revision 98. The authors correctly avoid the false shortcut “blow-up commutes with arbitrary base change.” They instead invoke generic freeness for the ambient algebra and the associated graded algebra, then use the I-adic exact sequences to control powers of the centre ideal and hence the Rees algebra.

That is the right route.

Precisely because it is right and load-bearing, it should be stated and proved cleanly as a lemma. The paper should explicitly track:

1. the base ring and finite-type hypotheses;
2. flatness of the relevant graded pieces after localization;
3. induction giving flatness of A/I^m;
4. exactness after tensoring to a fibre;
5. identification of the fibre of I^m with the m-th power of the fibre ideal;
6. base change of the Rees algebra;
7. simultaneous localization for the finite sequence of successive centres.

At present all ingredients are present, but the reader must reconstruct the actual theorem being used.

### 4.4 Every removed “bad image” must correspond to an explicitly defined algebraic bad locus

The proof uses Chevalley constructibility correctly in spirit: a constructible image with empty generic fibre cannot be dense, so its closure can be removed.

But the paper groups many distinct failures under “bad loci”:

- source non-smoothness;
- centre non-smoothness over the base;
- wrong normal-crossing ranks or codimensions;
- failure of a chart family to cover;
- failure of an inverse morphism identity;
- loss of invertibility of a declared unit;
- appearance of a fibrewise identically-zero specialization.

Some of these are open rank conditions. Others are coverage or component conditions.

For a theorem intended to establish a finite fibrewise certificate, the paper should write the finite list of bad loci and state why each has empty generic fibre. This is where a plausible spreading argument becomes a reference theorem.

## 5. Main objection II: Theorem 3.4 still hides the decisive real-semialgebraic-to-algebraic interface

Even if Lemma 3.3 is granted, the paper has another problem: it must return from algebraic generic-fibre constructions to the **original real inequality-constrained graph** and produce exactly the real-accessible divisors that govern the metric exponent.

This is more specific to the present paper than the abstract resolution machinery, and it needs a cleaner theorem.

### 5.1 The square-slack lift needs a global compatibility statement

Replacing p ≥ 0 by p = s^2 is set-theoretically exact over the reals. The difficulty begins after algebraic closure, resolution, finite base change, branch selection, and descent.

The theorem needs a statement ensuring that after all those operations:

- every retained source real point projects to the original semialgebraic graph;
- every original real graph point in the required observation neighbourhood is covered;
- no algebraic component created by closure contributes a spurious “accessible” order;
- all strict denominator exclusions, branch inequalities, and stochastic sign constraints survive the descent.

The phrase “retain the original real sign conditions throughout” describes an intention, not yet a formal mechanism.

This issue is central because the paper itself correctly insists that complex or algebraic divisors are not enough: the exponent must be attained by a real admissible arc.

### 5.2 Passage from a Nash stratum to an integral algebraic base needs auditable label bookkeeping

The proof passes from a Nash stratum to the smooth real locus of a Zariski closure and then to an integral algebraic component. Root labels can require finite algebraic base covers.

This is plausible, but Theorem 3.4 claims a fixed finite chart collection, fixed integer orders, and fixed accessibility flags. The paper should therefore track:

- which real Nash branch of the algebraic cover is selected;
- how nonreal and conjugate branches are discarded;
- how monodromy of root and component labels is killed or quotiented;
- how order data descend when several algebraic sheets represent one original parameter;
- why the permutation quotient preserves the joint initial family, not merely the scalar exponent.

The current descent paragraph is too short for the strength of the conclusion.

### 5.3 Zero specializations and vertical components should be theoremized rather than bundled into one induction paragraph

Revision 98 rightly recognizes that a function nonzero generically can become identically zero on a special fibre and that new vertical components can appear. The proposed remedy is to add all such parameter values to an exceptional algebraic set and rerun the construction by dimension induction.

Again, the architecture is reasonable.

But the finiteness of the entire atlas depends on this induction. The paper should distinguish at least the loci where:

- a new vertical component appears;
- a declared unit loses invertibility;
- a nonzero function becomes fibrewise zero on a component;
- the chart family stops covering;
- the real-accessibility condition changes.

Each locus should be shown to lie in a proper algebraic or semialgebraic subset with strict dimension descent. Right now this is asserted globally rather than proved case by case.

### 5.4 Real accessibility deserves a standalone lemma

The real-accessibility condition is mathematically important:

a recorded divisor must have a real point away from the other divisors and a real admissible transversal along which G > 0.

The proof says this is first-order and that an inverse étale chart then gives the transversal. That should be isolated as its own lemma, including:

- the exact first-order formula;
- the square-slack constraints;
- persistence in the intended real branch;
- existence of the G > 0 side;
- completeness: every scalar order that can be realized by a real degeneration is no smaller than one of the recorded divisor ratios.

Corollary 3.6 uses this completeness, not merely existence of some real divisors.

## 6. Main objection III: the uniform semialgebraic asymptotics are plausible but under-proved relative to their role

Proposition 4.2 is a good response to the earlier criticism that Hardt triviality does not imply a power-rate estimate.

The proposition states that a semialgebraic e(theta,t) tending pointwise to zero admits, after finite Nash stratification, a positive rational power nu and a positive continuous threshold with

e(theta,t) ≤ t^nu.

The proof has the right ingredients:

- quantifier elimination;
- a finite polynomial list;
- one-variable algebraic branches;
- Newton/Puiseux slopes from finite supports;
- semialgebraic choice;
- a compact-subset minimum for the threshold.

I believe a rigorous theorem of this type is true.

My objection is that the proof, as written, is still one level too informal for the amount of work it performs. In particular, the passage from an arbitrary quantifier-free Boolean formula for a single-valued graph to finitely many algebraic branches with a uniform finite slope list should either be:

- cited to a precise semialgebraic preparation / Puiseux theorem in families; or
- proved by an explicit cell decomposition and branch-selection argument.

The sentence that a one-dimensional graph “must lie on a zero of one of the remaining polynomials” is a useful observation, but it is not by itself a family preparation theorem.

The authors should not infer from this criticism that the theorem is false. My point is the opposite: this is standard-enough tame geometry that a precise theorem should exist, and a top-four paper should either invoke it exactly or prove the needed version cleanly.

## 7. Main objection IV: Theorem 5.1 overstates “effective” relative to the specified algorithmic infrastructure

The direct semialgebraic-max route is a strong improvement.

For a fixed algebraic input, defining

m_H(s) = max { H(x) : x in Gamma, G(x) ≤ s }

by a first-order formula, applying real quantifier elimination, and then extracting the eventual Puiseux order is a credible finite procedure. Likewise, after the rational exponent is known, the joint leading set and bottleneck diameter are definable by finite formulas, so exact algebraic output is believable in principle.

However Theorem 5.1 claims more than this fixed-centre numerical output. It says that in parameter families the corresponding strata and formulas are effectively describable, and the proof also presents a constructive geometric route through reduced decomposition, resolution/principalization, spreading, accessibility testing, and recursive exceptional-set handling.

For this level of claim the paper must specify:

- the coefficient field and its effective representation at every stage;
- exact algorithms or references for constructive characteristic-zero resolution/principalization in the required representation;
- how finite étale charts and inverse maps are represented;
- how vertical-component and fibrewise-zero conditions are decided;
- how the recursive base stratification is encoded and terminated;
- how branch labels and real accessibility are represented in the output.

Saying that ideal arithmetic, localization, generic flatness, and elimination “can be performed by finite algebraic calculations” is not enough for a theorem whose conclusion is algorithmic.

There are two clean solutions.

**Option A:** weaken Theorem 5.1 to an existence/definability theorem and retain the direct real-elimination algorithm only for the fixed algebraic spectral output that is actually specified.

**Option B:** retain the strong effectivity theorem but add a formal computational model and exact constructive references for every transformation.

The present version lies between these two standards.

## 8. Main objection V: the top-four originality comparison is still too narrow

The manuscript has fixed one important literature problem: it now compares honestly with current scalar Łojasiewicz theory. That is necessary but not sufficient.

The central claimed new object is no longer the scalar exponent. It is the simultaneous weighted real leading coefficient set

C_0(theta),

followed by its root-multiset image and exact bottleneck diameter.

Conceptually, this is a weighted initial/tangent object of a definable graph at an exact fibre, with real inequality constraints retained, followed by a nonlinear but definable root map.

The relevant novelty question is therefore broader than:

“Does existing Łojasiewicz theory already give the scalar exponent?”

The paper must also ask:

- What is already known about weighted tangent cones or initial sets of semialgebraic/definable germs?
- What uniformity is already supplied by semialgebraic or o-minimal preparation?
- What Hausdorff convergence of definable rescalings is standard?
- What part of the joint coefficient relation survives that is not already a standard weighted tangent-cone construction?
- Is the exact root-multiset diameter theorem new because of a genuinely new geometric invariant, or is it an application of a standard definable tangent object to a particular polynomial-root map?

At present the bibliography contains excellent classical real algebraic references for elimination and Hardt triviality and a current scalar Łojasiewicz comparison, but it does not delimit this broader novelty boundary.

For a specialist paper, a new synthesis and a sharp application can be enough. For Annals/Acta/Inventiones/JAMS, the paper needs to explain why the organizing invariant itself changes the subject, rather than merely packages standard tame-geometric machinery efficiently.

## 9. Theorem 4.1 is potentially the conceptual centre, but the manuscript has not isolated its genuinely new content

Theorem 4.1 is one of the strongest conceptual statements in the paper.

It does something important that independent scalar coefficient envelopes cannot do: it takes the simultaneous feasible weighted limit, retains relations between coefficients and inequality faces, maps the joint set to root multisets, and computes the exact leading diameter.

I agree with the manuscript that a Cartesian product of separately optimized coefficient envelopes would generally lose information.

But the theorem currently mixes two kinds of content:

1. tame-geometric consequences of definability and compactness;
2. the genuinely model-independent invariant the authors want to introduce.

The fixed-centre Hausdorff convergence argument is plausible:

- scalar orders bound the rescaled coordinates;
- every sequence has definable compact subsequential limits;
- the closure formula identifies the outer limit;
- semialgebraic monotonicity controls the distance to the positive-radius sections;
- finite nets give Hausdorff convergence;
- root continuity transfers the limit;
- cluster separation localizes bottleneck matchings.

What I do not yet see is a theorem statement that makes clear which part of this package is not already a standard fact about a suitably defined weighted tangent set.

If the authors want this to be the main conceptual theorem, they should formulate it so that a reader can identify the new invariant and the new assertion in one page, independently of the very large relative-resolution infrastructure.

## 10. The explicit multiplicity theorem is substantially more convincing than the general atlas theorem

Theorem 6.2 treats the full-rank binary model at fixed degree with arbitrary root multiplicities and endpoint/interior patterns. Within that scope it is a useful theorem.

The derivation is transparent:

- the full-rank coefficient inverse reduces the observation geometry to coefficient/root geometry;
- repeated interior roots create square-root splitting coordinates;
- endpoint roots are one-sided and remain linear;
- the order-t score produces a finite Fisher cone;
- a radial contraction realizes the complete leading set;
- the ordered-cluster diameter is computed exactly.

I do not see a fatal defect in the formulas

omega_theta(t) = C(theta) sqrt(t) + O_H(t)

for repeated interior clusters or in the linear law when no interior root is repeated.

The scope should remain exactly as currently stated: fixed degree, two components, binary stochastic channels, coprime component polynomials, strict positive invertible channels, strict weights, at least 2d+1 exterior clocks, and the entire closed-model competitor class.

This theorem is not an unrestricted singularity classification. The revision is now appropriately careful about that.

At top-four level, however, the theorem is still an explicit theorem in a very structured finite-dimensional model. Its significance depends heavily on the general theory around it.

## 11. The cubic fibre classification and rank-crossing inverse are now serious pieces of the paper

Theorem 7.1 gives a complete exact fibre for the chosen cubic family. I find the pencil reduction and discriminant geometry convincing.

The rank-crossing local inverse is also much improved. In particular, the proof no longer hides a determinant division through det U = 0. The second marginal provides the stable rank-two object; the perturbed pencil is isolated quantitatively; coefficient functionals recover rank-one matrices; stochastic parameters then follow from row/column sums.

I would still recommend that final publication make the constants easier to audit and perhaps separate the depressed-cubic absorption estimate into a named technical lemma, but this is exposition, not a reason for rejection.

The distinction between:

- exact identification,
- root-multiplicity singularity,
- and local Fisher conditioning

is one of the strongest conceptual features of the explicit part of the paper.

## 12. The weight-wall theorem is the strongest model-specific result

Theorem 8.4 is, in my view, the most interesting concrete theorem in the manuscript.

At the wall:

- the base local Fisher constant remains finite and positive;
- a remote exact component exists at a positive spectral distance;
- its observation distance from the identified-side centre is linear in delta with positive coefficient mu_E;
- below the threshold the whole-model modulus is governed by the local square-root law;
- above the threshold it jumps to the remote spectral scale;
- on the nonidentified side the remote exact interval opens at a square-root root scale.

This cleanly separates loss of identification from local conditioning.

Revision 98 also correctly handles the critical ray conservatively: first-order asymptotics alone do not determine the sign there.

I regard the quadratic entrance remainder as plausible because the exact local polynomial chart displays the second-order coefficient error.

If this paper were narrowed around the fixed-centre joint invariant plus the explicit multiplicity/cubic/wall results, I would regard it as much closer to a strong specialized paper.

## 13. The centre-known statistical corollary is secondary and should remain secondary

The statistical corollary is explicitly centre-known and local. That calibration is important. It does not establish unknown-centre adaptation, honest confidence regions across the wall, or a general minimax theorem for the entire family.

I have no major objection to retaining it as an illustration.

I would not advertise it as an independent statistical contribution of the same depth as the algebraic and spectral theorems.

## 14. Reproducibility status at the reviewed head

At the time of this report, the exact reviewed head is

72faee076147dbabd3c50a8cd46390f770102a0e.

The branch-scoped workflow “A2 v98 exact-head manuscript and archive” has run id 35483001933. At the time I checked it, the status was still **pending** and the conclusion was null.

Therefore I record the following:

- the repository contains a sensible exact-head build/audit workflow;
- the response reports a successful local principal build;
- the finite exact regression record is appropriately scoped;
- I do **not** certify a completed exact-head remote principal/archive/complete build from this report.

A later successful CI receipt would close this reproducibility item. It would not alter the mathematical recommendation above.

## 15. Disposition of the principal v97 requests

The authors' response matrix is useful, but “supplied” should not be confused with “referee-closed.” My disposition is as follows.

### Substantially closed

- current Hà comparison, including acknowledgement of finite-candidate and wall-chamber antecedents;
- explicit scope of the multiplicity theorem;
- quantitative cross-rank inverse;
- remote tangent-cone completeness and converse realization;
- separation of local and whole-model modulus;
- evidence discipline for finite symbolic checks;
- stronger remote entrance remainder in the stated simple/double chart.

### Materially improved but not closed at top-four proof standard

- spreading the generic resolution certificate over a parameter base;
- real-semialgebraic descent from algebraic lifts;
- vertical/special component recursion;
- completeness of real-accessibility flags;
- uniform family asymptotics;
- the strong family-effectivity assertion.

### New top-four issue exposed by the successful revision

- the paper now has enough infrastructure that the central originality question can no longer be postponed. The manuscript must explain what is genuinely new about the joint weighted initial spectral object relative to broader tame/weighted tangent geometry, not only relative to scalar Łojasiewicz exponent formulas.

## 16. Required mathematical revisions before I would reconsider the paper at this level

I would require all of the following.

1. **Rewrite Lemma 3.3 as a precise finite-diagram spreading theorem.**  
   State the finite-type base hypotheses, reductions, locally closed pieces, inverse isomorphisms, relative smoothness, normal crossings, and fibrewise conclusions in one exact proposition.

2. **Extract the blow-up base-change argument as a separate algebraic lemma.**  
   Prove the associated-graded / I-adic / Rees base-change chain in a form that can be cited later.

3. **Split Theorem 3.4 into algebraic coverage and real admissibility.**  
   One theorem should produce the fibrewise algebraic monomial cover; a second should prove descent to the original semialgebraic graph and completeness of the real-accessible order list.

4. **Give a standalone real-accessibility lemma.**  
   It should include the first-order condition, real transversal construction, square-slack compatibility, and the completeness statement needed by Corollary 3.6.

5. **Make the exceptional-set induction auditable.**  
   List the exceptional phenomena individually and show strict base-dimension descent for each.

6. **Replace the informal family-Puiseux step by a precise preparation theorem or a full cell proof.**  
   Proposition 4.2 should be a theorem a reader can cite without reconstructing the missing definable-preparation details.

7. **Calibrate Theorem 5.1.**  
   Either provide a formal computational model plus constructive references for the entire family algorithm, or weaken the theorem to the exact effectivity that the elimination route actually proves.

8. **Broaden the novelty comparison.**  
   Compare the joint weighted initial set with semialgebraic/o-minimal tangent and preparation constructions, not only with scalar valuation formulas. State explicitly what invariant or theorem is new after all standard tame-geometric machinery is granted.

9. **Reorganize the introduction around one principal new theorem.**  
   At present the paper alternates between a very general atlas theorem and a highly explicit binary stochastic experiment. A top-four reader should be able to state the one main new theorem and why it matters without reciting the entire dependency graph.

10. **Preserve a successful exact-head CI receipt before calling the full repository product reproducibly built.**  
    This is not a mathematical theorem issue, but it should be closed before final archival claims.

## 17. Two coherent publication routes

### Route A: finish the general theorem at reference level

If the authors keep the current title and general framing, I would expect a theorem approximately of this strength to become the unmistakable centre:

> After a finite semialgebraic stratification of a fixed-format compact real algebraic family, the observation graph admits a fibrewise proper real-accessible weighted monomial model with fixed combinatorial order data; the associated joint weighted initial spectral sets form a definable compact family; their root-multiset diameters give the exact leading modulus with compact-uniform power remainder.

To justify a top-four submission, the authors would then need to show that this theorem is genuinely new relative to existing resolution, tame preparation, and weighted tangent-cone machinery, not merely derivable by chaining them.

The explicit multiplicity and wall theorems would become strong applications of that general theorem.

### Route B: narrow to the distinctive mathematics already proved most convincingly

A more conservative paper could centre on:

- fixed-centre joint constrained weighted specialization;
- exact root-multiset leading diameter;
- full-rank arbitrary-multiplicity/boundary laws in the binary experiment;
- complete rank-deficient cubic fibre;
- quantitative local inverse through the rank locus;
- local Fisher normal form;
- remote weight-wall entrance transition.

The parameter-family atlas and strong algorithmic theorem could then be deferred until their foundational interfaces are fully formalized.

This would reduce formal breadth but substantially increase proof density and sharpen the originality claim.

## 18. Editorial comments

These are secondary to the mathematical issues above.

- Keep the distinction between exact target fibre, parameter fibre, and root-multiset image explicit everywhere.
- Keep local modulus and whole-model modulus visibly separate in theorem statements.
- Keep the warning that the critical ray t = mu_E delta is not decided by the first-order coefficient.
- Keep the geometric wall B = 0 labelled as a remark rather than a second completed entrance theorem.
- Do not use “effective” as a synonym for “definable” or “finite in principle.”
- When a theorem uses a standard deep result, cite the exact applicable form rather than the general subject.
- The discussion of Hà v2 is now much better; preserve that scholarly calibration.
- Add literature around definable/semialgebraic preparation and weighted tangent/metric geometry if the joint initial set remains the main invariant.
- The huge numerical Fisher constants are acceptable as exact examples, but they should remain illustrations rather than evidence for a general singular mechanism.
- A concise dependency diagram is useful, but it should not substitute for theorem hypotheses.

## 19. Final assessment by category

### Correctness

For the explicit finite-dimensional theorems, I found no fatal counterexample in revision 98. The multiplicity law, cubic fibre, cross-rank inverse, remote tangent cone, and weight-wall mechanism are internally coherent and substantially better proved than in the previous revision.

For the general family atlas, my concern is proof completeness and exact applicability of infrastructure, not a concrete counterexample.

### Originality

The joint constrained leading set and remote-fibre entrance mechanism are the most distinctive ideas.

The scalar order and finite chamber language are not sufficient originality claims; the manuscript now acknowledges this.

The novelty of the general weighted initial-set theorem relative to broader semialgebraic/o-minimal tangent geometry remains insufficiently documented.

### Depth

The explicit wall calculation and the quantitative rank-crossing inverse have real depth.

The general atlas theorem would have greater depth if the family-resolution and real-descent interfaces were themselves completed as precise results.

### Breadth

The paper is broad, perhaps too broad for 26 pages. It moves from general real algebraic resolution and effectivity to detailed stochastic polynomial inverse problems. Breadth is valuable only if the central theorem unifies these parts at full proof strength.

### Exposition

Substantially improved. The principal article is much easier to audit than earlier complete-volume versions.

The remaining difficulty is no longer gross organization; it is that several deep interfaces are compressed into dense paragraphs.

### Reproducibility

The source discipline is good. The exact-head remote workflow was still pending when checked, so full remote build certification is not recorded here.

## 20. Bottom line

Revision 98 is a meaningful advance and should not be evaluated as if it were revision 97 with cosmetic edits.

The authors have repaired the explicit rank-crossing and remote-wall parts to a degree that I regard as mathematically serious. They have also moved the general family programme from a slogan to a plausible theorem architecture.

But “plausible architecture” is not the standard for a top-four general mathematics journal when the architecture itself is the principal theorem.

The broad atlas still relies on under-theoremized specialization, real-descent, accessibility, and uniform-preparation interfaces. The effectivity claim still exceeds the level of algorithmic specification. And, once those technical matters are set aside, the manuscript has not yet established that its general weighted initial-set formalism is new enough relative to the broader tame-geometric literature to support an Annals/Acta/Inventiones/JAMS-level significance claim.

I therefore recommend **rejection in the present form**, while strongly distinguishing this from a claim that the explicit new mathematics is wrong.

I would encourage a future submission only after one of two nonlocal changes: either complete and position the general real spectral atlas as a genuine reference theorem, or narrow the paper around the fixed-centre joint invariant and the explicit multiplicity/cubic/weight-wall mathematics that revision 98 now proves most convincingly.
