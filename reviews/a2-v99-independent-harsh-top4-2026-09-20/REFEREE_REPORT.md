# Independent harsh referee report on A2 revision 99

**Manuscript:** *Projective polynomial observations: joint spectral invariants and identification walls*  
**Reviewed branch:** revision/a2-v99-joint-invariants-and-remote-entrance-2026-09-20  
**Reviewed exact head:** c49c6d0604f83badf47b32dfdf25dc043b4117ef  
**Principal entrypoint:** papers/A2-v17-boundary-information-coarsening/rigidity_v99.tex  
**Principal article source:** papers/A2-v17-boundary-information-coarsening/article/v99/paper.tex  
**Controlling prior report:** reviews/a2-v98-independent-harsh-top4-2026-09-20/REFEREE_REPORT.md  
**Prior reviewed head:** 72faee076147dbabd3c50a8cd46390f770102a0e  
**Date:** 2026-09-20

## 1. Recommendation

**Recommendation for an Annals / Acta / Inventiones / JAMS-level general mathematics journal: reject in the present form.**

This recommendation is materially different from the recommendation in my report on revision 98.

Revision 99 is not a cosmetic rewrite and it is not another round of renaming old gaps. It makes a serious attempt to close essentially all of the proof-interface objections raised against revision 98. In particular, the manuscript now contains standalone results for Rees-algebra base change, spreading of the full finite stratifying diagram, exact square-slack algebraization, selected real-branch descent, real accessibility, finite support control of semialgebraic orders, an explicit quantifier-elimination route to the spectral outputs, a general finite-fibre remote-entrance theorem, a second-order critical-window theorem, and a complete treatment of the geometric endpoint wall. It also adds the requested example showing that sharp one-coordinate coefficient envelopes do not determine the joint leading spectral diameter.

I therefore no longer regard the paper as failing because its general atlas theorem is merely a blueprint. The appendix is now substantial enough that the earlier criticism would be unfair if repeated unchanged.

I also did not find a direct counterexample to the principal new mathematical statements in revision 99. The fixed-centre joint specialization theorem, the multiplicity theorem inherited from revision 98, the rank-deficient cubic fibre classification, the cross-rank local inverse, the two remote-wall constructions, and the second-order entrance formula all survived the consistency checks I performed on their stated hypotheses and proof logic.

The top-four rejection now rests on a harder and more consequential question: **after the machinery is granted, what is the genuinely new theorem of top-four conceptual depth?**

At present I do not think the manuscript answers that question sharply enough.

The “joint initial fibre” is defined by a weighted rescaling and fixed-centre closure of a semialgebraic graph. Once the optimal weight is known, this construction is very close in spirit to a real constrained weighted tangent cone / initial degeneration. The paper does not yet explain precisely whether its object is a new invariant, a real-inequality version of a standard weighted tangent object, or a convenient representation of an already familiar degeneration. The theorem that its root-image diameter supplies the leading metric constant is useful, but after the limiting set is defined it is also close to a formal consequence of compactness, semialgebraic convergence, and continuity of roots.

The new separation theorem proves that coordinatewise marginal envelopes do not determine the joint set. That is correct, but the example is deliberately built by changing the pairing of two coefficient coordinates on a disconnected union of arcs. It establishes non-productness, not yet a deep obstruction theorem for the actual polynomial observation model.

Similarly, the general remote-entrance theorem is clean and useful, but its hypotheses already assume the hard local geometry: a full polyhedral-cone parametrization, a \(C^2\) observation extension, cone coercivity, and a finite exact fibre. Under those assumptions, the first- and second-order formulas are a constrained metric-projection perturbation calculation. The difficult work is verifying those hypotheses. Revision 99 now verifies them for the two principal walls of one rank-deficient cubic binary family, which is valuable mathematics, but it is still far from a structural classification of remote entrances in the broad semialgebraic theory advertised by the first half of the paper.

Thus revision 99 has largely converted the old correctness/proof-completeness problem into a **novelty, canonicality, and scale-of-the-main-theorem problem**. That is real progress. It does not, in my judgment, yet clear the standard of the four general mathematics journals named above.

There is also a concrete reproducibility defect at the exact reviewed head. The source text says that exact rational data for the new critical examples are “retained with the exact regression,” but the v98-to-v99 diff adds no v99 regression script, no v99 diagnostics record, no v99 revision manifest, and no v99 response package. The workflow directory contains an a2-v98 workflow but no a2-v99 workflow, and there is no GitHub Actions run attached to exact head c49c6d0604f83badf47b32dfdf25dc043b4117ef. This is not a mathematical counterexample, but the claim of retained exact regression is not evidenced in the reviewed branch as it stands.

## 2. Scope of this report

I reviewed the exact branch head

\[
\texttt{c49c6d0604f83badf47b32dfdf25dc043b4117ef}.
\]

Relative to revision 98, revision 99 is two commits ahead and introduces a new v99 article tree containing, among other files,

- foundations.tex;
- real_atlas.tex;
- joint_separation.tex;
- cubic.tex;
- remote_structure.tex;
- geometric_wall.tex;
- critical_examples.tex;
- the new paper.tex and references.tex;

while retaining selected v98 components such as the model, multiplicity theorem, and weight-wall section.

The report treats the current principal article as the object under review. Historical material is used only when the v99 paper imports it or when it is needed to determine whether a prior referee objection was actually answered.

My standard is intentionally severe. A theorem can be correct, useful, and publishable without being a top-four general-journal theorem. Conversely, a negative top-four recommendation is not a claim that the mathematics is wrong.

## 3. Executive mathematical diagnosis

Revision 99 has four layers.

1. **A general real-semialgebraic atlas layer.**  
   Resolution/principalization, real algebraization and descent, accessibility, scalar orders, joint weighted specialization, uniform definable asymptotics, and effectivity.

2. **A joint leading-set layer.**  
   The coefficient coordinates are scaled at the common spectral exponent, the fixed-centre positive-radius graph is closed at the weighted limit, and the root-multiset image of this joint limit determines the exact leading spectral diameter.

3. **A concrete binary polynomial layer.**  
   Full-rank multiplicity/boundary laws, rank-deficient cubic exact fibres, quantitative inversion through rank loss, and explicit Fisher-cone constants.

4. **A remote-identification layer.**  
   A general finite-fibre cone entrance theorem, its second-order critical correction, and two explicit cubic walls with different nonidentified-side openings.

The paper is strongest when layers (3) and (4) interact. The distinction between local multiplicity singularity, local conditioning, and global remote identification failure is mathematically clear and conceptually useful.

The paper is weakest in justifying why layer (1), or the abstract formulation of layer (2), is itself a new top-four-level theory rather than a careful assembly of standard real-algebraic/definable tools around a weighted tangent construction.

That is the central issue of this report.

## 4. What revision 99 genuinely fixes from revision 98

The authors deserve explicit credit here. A harsh review should not pretend that the prior objections remain unchanged.

### 4.1 The Rees/base-change gap is substantially repaired

The new lemma “One localization for all powers of an ideal” is the right statement to isolate.

The proof now explains why, after one localization, the associated graded algebra is flat over the base, why the graded pieces are flat, why the quotients \(B/I^n\) become flat, why tensoring preserves the inclusion of \(I^n\), and hence why

\[
I^n\otimes A' \cong (IA')^n
\]

for arbitrary base change after localization. It then passes to the Rees algebra and Relative Proj.

This is a meaningful repair of one of the most technical complaints in the v98 report.

### 4.2 The finite stratifying diagram is now spread as a diagram

Revision 98 moved too quickly from “clear denominators” to a fibrewise certificate. Revision 99 now has a separate finite-diagram lemma. It explicitly retains

- the reduced closed chain;
- the actual successive complements;
- the projective maps;
- both inverse identities;
- finite affine chart coverage;
- flatness;
- geometrically reduced fibres.

The final partition argument on each fibre is also stated.

This is much closer to reference-grade mathematics.

### 4.3 The bad-locus recursion is now auditable

The appendix explicitly lists discarded loci: nondominating components, failures of source/centre smoothness, normal-crossing failures, chart and unit failures, and failures of descended identities. It then explains why each has empty generic fibre, why its constructible image has proper closure, and why recursive reconstruction terminates by base-dimension descent.

This directly addresses a major v98 objection.

### 4.4 Exact real algebraization and descent are no longer slogans

The square-slack lemma now states exact projection onto the original real graph, rather than merely an algebraic relaxation. Strict exclusions and branch conditions are tracked.

The real-descent lemma then handles selected Nash branches, finite algebraic covers, monodromy by base refinement, real surjectivity of the resolved sources, and the finite root-label quotient.

Again, this is a substantial improvement.

### 4.5 Real accessibility now has its own theorem

The new accessibility lemma gives an explicit first-order condition for a divisor to contain an admissible real point away from other divisors, produces a real transversal, and proves that intersections cannot create a smaller order than the minimum divisor ratio.

This is precisely the missing completeness statement requested in the prior report.

### 4.6 The semialgebraic decay proof is now a real argument

The finite-support lemma extracts a finite rational candidate set from polynomial supports of a quantifier-free graph formula and treats specialized zero coefficients and eventual-zero branches.

The proof of the uniform decay proposition then selects a genuinely positive threshold and only takes minima after restricting to compact subsets of a stratum.

The previous objection that a metric power rate was being inferred too quickly from pointwise definable convergence is therefore substantially answered.

### 4.7 Effectivity is much more explicit

For spectral outputs, the paper now gives a credible direct quantifier-elimination route:

- form the maximum functions \(m_H(s)\);
- eliminate their graph formulas;
- extract a finite candidate order list;
- test the candidates by first-order comparability;
- compute the joint initial set;
- adjoin roots;
- express the bottleneck diameter by a finite permutation formula;
- isolate the resulting algebraic number.

This is significantly better than the earlier invocation of an unspecified Puiseux-branch oracle.

I have a residual objection to the stronger claim that the complete geometric atlas certificate is effectively constructible; see Section 10 below. But the scalar/joint spectral output algorithm is now far more convincing.

### 4.8 The requested marginal-separation example is present

Revision 99 constructs two experiments with the same individual coefficient envelopes and the same scalar orders but different leading spectral diameters.

The literal request in R7 of the v98 report has therefore been answered.

My concern is now about the depth of what this example establishes, not about its absence.

### 4.9 The remote-wall request is answered far beyond the literal minimum

Revision 99 adds a general finite-remote-fibre entrance theorem, a second-order critical-window theorem allowing nonunique first-order minimizers, a full geometric endpoint-wall parametrization and score-separation argument, and explicit critical-ray examples.

The old statement that the geometric wall is not completed is no longer true for revision 99.

### 4.10 The main remaining unclosed prior item is reproducibility

Revision 98 had a dedicated exact-head workflow. Revision 99 does not.

That is discussed separately below.

## 5. Main objection I: the paper has not established that the “joint initial fibre” is a new canonical object rather than a weighted tangent/initial degeneration under another name

This is now the most important conceptual issue.

The paper fixes the exponent \(\alpha=p/q\), introduces the weighted substitutions

\[
R=\varepsilon^q U,\qquad
c_{r,a}=\varepsilon^{p(m_r-a)}V_{r,a},
\]

holds the centre parameter fixed, and takes the real closure as \(\varepsilon\downarrow0\). The coefficient projection of the resulting limit is \(\mathcal C_0\).

This is a natural and useful construction.

But structurally it looks very close to a weighted tangent cone, weighted initial degeneration, or a real constrained version of a deformation-to-the-normal-cone/Rees construction applied to the observation graph with anisotropic coordinate weights.

The paper currently does not settle the relationship.

That omission matters because the article repeatedly asks the “joint invariant” to carry the novelty that scalar resolution theory does not carry.

### 5.1 Theorem 4.1 contains two mathematically different claims that should be separated

The first claim is substantive:

> the correct anisotropically scaled positive-radius graph has a nonempty compact fixed-centre limit with all real inequality relations retained.

The second claim is much more formal:

> the leading spectral constant is the diameter of the root image of that limit.

Once Hausdorff convergence of the scaled coefficient image is known, continuity of the finite-degree root-multiset map and continuity of diameter under Hausdorff convergence do most of the second job.

A top-four paper needs to identify exactly where the new geometry enters. At present the definition and its formal consequences are somewhat conflated.

### 5.2 “Joint” is not yet a structural theorem

The paper correctly emphasizes that \(\mathcal C_0\) is not a Cartesian product of its scalar coordinate projections.

But an arbitrary joint set is not determined by its coordinate projections. That fact alone is not a new geometric principle.

The paper needs a theorem about the structure of \(\mathcal C_0\), not only a theorem saying that one should retain \(\mathcal C_0\).

Examples of the sort of result that would change my assessment include:

- an intrinsic universal property for the fixed-centre weighted degeneration;
- a comparison theorem with a weighted normal cone or initial ideal construction;
- a functoriality/invariance theorem under changes of semialgebraic presentation;
- a finite set of algebraic data from which the joint set, not merely its scalar orders, can be reconstructed;
- a nontrivial constraint/classification theorem for the possible joint leading sets in the polynomial observation model;
- a theorem showing that the joint set detects a phenomenon invisible to a substantially richer scalar valuative invariant than coordinatewise envelopes.

I am not prescribing one exact route. I am saying that the present paper names the object and proves it computes the constant, but has not yet exposed a new structural law governing the object.

### 5.3 The literature comparison is too narrow for this claim

The bibliography is extremely short for a paper whose first half ranges across resolution, real algebraic geometry, definable asymptotics, weighted degenerations, metric tangent behavior, and algorithmic geometry.

The current comparison with Hà is responsible as far as scalar Łojasiewicz exponents and finite candidate sets are concerned. But it is not enough to position the joint weighted limit itself.

The paper should compare its construction with the relevant languages of

- weighted tangent and normal cones;
- initial degenerations and Rees/deformation constructions;
- real/semialgebraic tangent geometry;
- definable metric tangent limits.

I am deliberately not asserting that one of those literatures already contains the exact fixed-centre real-inequality object. The point is that, without the comparison, the reader cannot tell whether the paper has discovered a new invariant or repackaged a standard weighted degeneration in coordinates adapted to the application.

At a specialist venue this could be repaired in exposition. At a top-four venue it is part of the originality proof.

## 6. Main objection II: the new separation theorem proves non-productness, but not yet a deep insufficiency theorem for the scalar atlas

Theorem “Separation from marginal scalar data” is correct and useful.

The two experiments have labels

\[
\mathcal E_A=\{(1,-1),(2,-4)\},\qquad
\mathcal E_B=\{(1,-4),(2,-1)\},
\]

so the individual ranges of \(c_1\) and \(c_0\) agree, while the pairing differs. The resulting root-image diameters differ.

This is a clean construction.

It is also exactly the kind of construction one would expect whenever a nonlinear function of two coordinates depends on their coupling and one keeps only the two marginal ranges.

### 6.1 The example is deliberately external to the main binary observation model

The source is a disjoint union of two intervals with an extra discrete label. That is allowed by the general semialgebraic framework, but it avoids most of the geometry that makes the concrete polynomial observation model difficult.

Consequently the example proves the logical statement

> separate sharp coordinate envelopes do not determine a joint nonlinear image.

It does not prove

> the scalar atlas obtainable from the actual polynomial observation geometry fundamentally fails to determine the new joint invariant.

Those are different significance claims.

### 6.2 The paper itself admits the gap

The introduction carefully says that the example does not show irrecoverability from “every possible scalar function of all the coefficients.”

That disclaimer is correct and should remain.

But once that disclaimer is made, the top-four novelty burden is still open.

### 6.3 A stronger theorem is needed

A much more compelling result would hold within the paper's principal binary polynomial experiment and would keep fixed a richer set of scalar data, for example:

- the full list of divisor orders for all coefficient functions;
- all one-coordinate sharp value functions;
- perhaps a natural class of scalar valuative combinations;

while producing genuinely different joint leading root geometry.

An alternative would be a theorem characterizing exactly which scalar data suffice to reconstruct the joint object and which do not.

Either would turn the current example from an illustration into a structural result.

As written, the separation theorem answers the prior referee request literally but does not by itself elevate the general atlas to a top-four contribution.

## 7. Main objection III: the general remote-entrance theorem is elegant, but most of the difficult geometry sits in its hypotheses

Theorem “Remote entrance for regular corners” assumes:

- a finite exact fibre;
- a full relative neighbourhood of each remote point parametrized by a closed convex polyhedral cone;
- a Nash homeomorphism onto that neighbourhood;
- a \(C^2\) extension of the observation embedding;
- cone coercivity of the first derivative;
- positive first-order separation \(\mu_j>0\).

Under those hypotheses, localization gives \(z=O(\delta)\), the rescaled minimization converges to a metric projection onto \(J_jK_j\), and the entrance distance is

\[
d_j(\delta)=\mu_j\delta+O(\delta^2).
\]

The second-order theorem then expands the squared norm and minimizes the first correction over the first-order minimizer set.

I find this argument plausible, and I specifically checked the nonunique-minimizer issue. The fact that the residual \(J_jv-b\) is common on \(M_j\) follows from uniqueness of the metric projection onto the closed convex cone \(J_jK_j\), even if its preimage under \(J_j\) is not unique. The stated formula is consistent with that geometry.

My objection is not that the theorem is false.

My objection is that the theorem is presented as a broad structural extension while its hypotheses already encode the regular-corner structure that makes the perturbation calculation work.

### 7.1 The hard theorem is verification of the hypotheses

For the weight wall, the paper does real work to construct the exact cone chart and prove score separation.

For the geometric endpoint wall, it again does real work to construct the ordered endpoint-root chart and prove that the centre direction lies outside the remote score cone.

Those are the deep parts.

The abstract theorem does not classify when such a chart exists.

### 7.2 A top-four version should say something genuinely structural about singular models

Examples of a stronger result would be:

- a theorem deriving the cone-chart/coercivity hypotheses from checkable algebraic conditions on a broad class of rank-deficient polynomial mixture models;
- a stratification theorem for finite exact fibres showing that regular remote entrances are generically of this type;
- a classification of possible first entrance exponents when the remote chart is not regular;
- a theorem treating intersections of the \(B\)- and \(E\)-walls or higher-rank/higher-multiplicity remote components.

At present the paper has a general perturbation lemma plus two highly worked cubic verifications.

That is good mathematics. I do not regard it as a general theory of identification-wall entrances yet.

### 7.3 The variational-analysis comparison is missing

The remote theorem is, mathematically, a sensitivity theorem for distance from a moving point to the image of a constrained set, with a second-order expansion.

The paper should compare it with standard perturbation/sensitivity and variational-analysis results for polyhedral cones, metric projections, constrained nonlinear programs, and second-order value-function expansions.

Again, I am not claiming that a standard theorem immediately gives the exact formula under the paper's chosen parametrization. I am saying that the novelty cannot be assessed without that comparison.

The current bibliography does not attempt it.

## 8. Main objection IV: the breadth of the abstract theory and the breadth of the demonstrated new phenomena remain mismatched

The general atlas theorem is formulated for arbitrary fixed-format compact semialgebraic families of probability maps and polynomial targets.

The concrete theorems that exhibit nontrivial spectral geometry concern a much narrower model:

- two components;
- binary stochastic channels;
- fixed polynomial degree;
- exterior clock observations;
- full-rank coprime centres for the complete multiplicity theorem;
- one rank-deficient cubic family for the exact nonidentification and wall analysis.

There is nothing wrong with a narrow model theorem.

The problem is rhetorical and structural: the first half of the paper asks the reader to absorb a large general resolution/definability apparatus, while the second half demonstrates the sharp new phenomena in one quite specific family.

The paper still has not shown that the full generality of the atlas is essential to the principal explicit discoveries.

### 8.1 The multiplicity theorem does not need the full general atlas for its proof

The full-rank coefficient inverse, root coordinates, Fisher projection, and direct Taylor expansions already give the explicit leading sets and constants.

### 8.2 The cubic walls are also proved directly

The exact fibre is analyzed by the affine pencil. The local inverse is proved by second-marginal recovery and robust pencil isolation. The remote walls are handled by explicit local charts and score separation.

These are strong direct arguments.

### 8.3 The paper therefore risks having two articles superposed

One article is about a general real spectral atlas built from resolution and definability.

The other is about explicit singular inverse geometry in a binary polynomial observation model.

Revision 99 connects them conceptually, but the connection is not yet strong enough to make the union automatically greater than either paper separately.

For a top-four journal, the authors should either prove a theorem where the general atlas machinery yields a genuinely new conclusion not accessible by the direct model analysis, or sharply reorganize the paper so that the general apparatus is subordinate to the concrete discovery.

## 9. Detailed assessment of the general relative real-atlas proof

Because this was the central weakness of revision 98, I record my current view in detail.

### 9.1 Rees algebra lemma

The new proof is credible.

The key move is to apply generic freeness to the finite-type algebra and its associated graded algebra, then use flatness of the graded pieces and the \(I\)-adic exact sequences to show flatness of \(B/I^n\) for all \(n\). That is the right way to justify arbitrary base change of all powers after one localization.

I do not currently see a fatal gap here.

### 9.2 Finite-diagram spreading

The explicit use of a finite-presentation limit result to descend objects, inverse maps, and identities on the actual complements is a considerable improvement.

The later imposition of flatness and geometrically reduced fibres addresses the component concern from the prior report.

Again, I do not currently see a direct contradiction.

### 9.3 Exceptional sets

The manuscript now distinguishes algebraic exceptional loci, which are handled by dimension descent, from full-dimensional real chamber changes in accessibility flags, which are handled by real quantifier elimination.

This distinction is important and correct in spirit.

### 9.4 Square-slack exactness

The statement that the real square-slack lifts project exactly to the original relatively closed graph is now explicit. The proof also explains why denominator exclusions are not blindly replaced by unbounded reciprocal coordinates on nonclosed pieces.

This is much better.

### 9.5 Real branch descent

The finite algebraic cover / selected Nash section argument is plausible. The paper also correctly treats root-label permutations equivariantly at the level of the whole joint relation rather than independently permuting scalar coordinates.

That answers a subtle prior concern.

### 9.6 Accessibility

The monomial weighted-average argument correctly explains why an arc through an intersection of normal-crossing divisors cannot have a smaller ratio than the minimum of the contributing single-divisor ratios.

The transversal construction at a real accessible divisor is also appropriate.

### 9.7 Bottom line on the atlas proof

I no longer recommend rejection because “the relative theorem is only a sketch.”

If the paper were being judged solely on whether it has upgraded the v98 blueprint to a serious proof, my answer would be yes.

The remaining question is whether this carefully assembled theorem is new and deep enough, rather than whether the authors have finally written down the assembly.

## 10. Detailed assessment of effectivity

The effectivity section now contains two conceptually different algorithms.

### 10.1 The direct spectral-output algorithm is credible

The maximum-function route is the strongest part.

For algebraic input, the graph of

\[
m_H(s)=\max\{H(x):G(x)\le s\}
\]

is first-order definable with attained maxima. Quantifier elimination gives a finite polynomial support. The finite-support lemma converts possible asymptotic orders into a finite rational list. Candidate exponents are then tested by first-order formulas.

After \(\alpha\) is selected, the joint initial fibre and its root image are again first-order definable, and the bottleneck diameter can be expressed with a finite permutation disjunction.

This is a genuine finite algorithm in the ordinary real-algebraic sense, although no complexity bound is claimed.

### 10.2 The geometric-certificate enumeration is much less satisfactory as a headline theorem

The appendix then says, in effect: enumerate all finite algebraic diagrams and semialgebraic partitions in increasing encoding length and verify them until the existence proof guarantees that one passes.

This is a legitimate computability strategy in principle.

But if the theorem is going to advertise “effective construction” of the geometric atlas, the computational model needs to be stated much more carefully:

- exact encoding of algebraic bases and their irreducible components;
- exact encoding of rational-function-field extensions;
- exact representation of projective maps and successive blowups;
- decidability of every proposed certificate condition in that encoding;
- how lower-dimensional recursive bases are enumerated and identified;
- how finite real branch selections are represented canonically enough for the verification search.

The paper gestures at all of these, but the result remains closer to an existence-by-effective-enumeration argument than to a usable constructive theorem.

My recommendation is simple: **do not make geometric-certificate effectivity part of the top-level novelty claim.** Keep the direct spectral QE algorithm, which is already interesting and much cleaner, and state the certificate enumeration as a supplementary computability observation unless a full computational algebraic-geometry formalization is intended.

## 11. Detailed assessment of the joint fixed-centre theorem

The fixed-centre formula is a good correction to an earlier conceptual ambiguity.

There is no quantified drifting parameter \(\theta'\). This matters.

The proof strategy for Hausdorff convergence is also reasonable:

- scalar order control bounds the scaled coefficients;
- the fixed-centre closure defines all subsequential outer limits;
- semialgebraicity and one-variable monotonicity remove subsequence dependence;
- compact finite nets give the inner inclusion;
- continuity of the root map transfers the limit to root multisets;
- cluster separation prevents cross-cluster optimal matching.

I did not find a contradiction in this argument.

My concern, as emphasized above, is not correctness. It is whether defining the correct weighted tangent object and then taking its diameter is by itself the conceptual theorem the paper claims it to be.

## 12. Detailed assessment of the multiplicity theorem

The revision 99 article imports the v98 multiplicity theorem essentially unchanged.

My prior assessment still stands.

For a repeated interior cluster, an order-\(\sqrt t\) zero-sum root splitting produces order-\(t\) second symmetric coefficient variation, giving the square-root spectral exponent. Endpoint one-sidedness forces linear root scale because the signed sum controls the individual displacements.

The projected Fisher program and

\[
C(\theta)
=
\max_j
2\sqrt{\frac{m_j-1}{m_j}}\,
\kappa_j^{-1/4}
\]

are consistent with the ordered zero-sum cluster diameter.

The coefficient-order formula

\[
\beta_1=1,\qquad
\beta_k=k/2
\]

for repeated interior clusters, and \(\beta_k=k\) at endpoints, is also consistent with the stated realizing arcs.

I do not base the present negative recommendation on a claim that this theorem is algebraically wrong.

The limitation remains scope: fixed degree, two components, full-rank positive channels, coprime component polynomials, binary outputs, and exterior clocks.

The manuscript now states that scope responsibly.

## 13. Detailed assessment of the cubic exact fibre and cross-rank inverse

Revision 99 improves the exposition of the second-marginal matrix dimensions and singular-value convention, which was a minor request in the v98 report.

The exact fibre theorem remains one of the strongest parts of the paper.

At rank one in the first channel, the second marginal forces competitors into the affine pencil

\[
h_c=(1-c)f+cg.
\]

The discriminant and root-location analysis then identifies the feasible real-rooted pencil interval, while the weight floor produces the second wall.

The inverse through rank loss is also persuasive:

- recover the normalizer and second marginal;
- use the second marginal to prove the competing second channel remains invertible;
- place competing component polynomials within \(O(\delta)\) of the affine pencil;
- use separate robust estimates near \(c=0\) and \(c=1\);
- recover stochastic parameters with dual coefficient functionals rather than division by \(\det U\).

This is exactly the sort of model-specific analysis that has genuine depth.

I found no direct contradiction in these arguments.

## 14. Detailed assessment of the general second-order entrance coefficient

The second-order theorem deserves credit.

A possible danger in nonunique first-order minimization is that second-order movement of the minimizer could alter the correction through an unaccounted \(Jw\) term. The paper avoids the essential ambiguity because the first-order image point is the unique Euclidean projection of \(b\) onto the closed convex cone \(JK\); hence the residual is common to all preimages in \(M\). The minimization of the first perturbative correction over \(M\) is therefore the natural value-function coefficient.

The proof based on

\[
f_\delta(v)
=
\|Jv-b\|^2
+
2\delta\langle Jv-b,Q(v,v)-c\rangle
+
o(\delta)
\]

on a compact localization is plausible.

I would still ask the authors to compare this theorem to existing second-order sensitivity results in variational analysis, but I do not presently claim the formula is wrong.

## 15. Detailed assessment of the geometric endpoint wall

This is the most important genuinely new completion in revision 99.

The endpoint parametrization uses ordered root coordinates

\[
d_1\le d_2\le0
\]

rather than recycling the interior variance cone. That is the correct geometry.

The score-separation proof also has a clear mechanism. Equality with the base wall-crossing derivative would force the derivative of the remote double-root pencil to move the endpoint double root outward, producing

\[
d_1+d_2=2\dot b>0,
\]

which contradicts endpoint feasibility.

This is a convincing first-order obstruction.

The theorem then gives

\[
d_{{\rm rem},B}(\delta)
=
\mu_B\delta+k_B\delta^2+o(\delta^2)
\]

and separates the local square-root scale below entrance from the positive remote spectral distance above entrance.

The contrast with the weight wall is conceptually useful:

- weight-wall feasible pencil length opens linearly on the nonidentified side and can produce a square-root spectral opening;
- endpoint-wall feasible pencil length opens quadratically, while the exact whole-model spectral diameter remains \(D-r\).

I regard this contrast as publishable mathematics.

The issue is again breadth: two explicit walls in one cubic family do not yet amount to a general classification of identification walls.

## 16. The critical examples are useful, but their claimed exact regression is not actually retained at the reviewed head

The new critical_examples.tex gives very sharp rational isolating intervals for \(\mu_B\), \(k_B\), and \(k_E\), and says:

> “The rational values of \(\mu^2\), \(\mu k\), the Gram data and isolating intervals are retained with the exact regression.”

At the reviewed exact head, I cannot verify that repository claim.

The v98-to-v99 file diff adds the v99 TeX sources and the prior referee report. It does **not** add:

- scripts/verify_a2_v99_math.py;
- revisions/a2-v99/EXACT_DIAGNOSTICS.json;
- an equivalent v99 regression record under another obvious v99 path;
- a v99 source manifest or runtime receipt.

A recursive path audit of the exact head finds the v99 article tree and entrypoints, but no v99 diagnostics package.

Therefore the finite decimal intervals in the new examples are presently assertions in the manuscript, not repository-backed exact regressions of the kind revision 98 had begun to establish.

This is straightforward to fix, but it should be fixed before the examples are advertised as retained exact arithmetic.

## 17. Reproducibility status at the exact reviewed head

The reviewed exact head is

\[
\texttt{c49c6d0604f83badf47b32dfdf25dc043b4117ef}.
\]

At this head:

- there is no .github/workflows/a2-v99.yml;
- the latest version-specific A2 workflow is a2-v98.yml;
- that v98 workflow is triggered on the v98 revision branch and does not certify v99;
- there is no GitHub Actions run whose head SHA is the reviewed v99 commit;
- there is no v99 runtime receipt or exact-head build manifest visible in the new revision diff.

Accordingly, I do **not** certify that rigidity_v99.tex, rigidity_v99_archive.tex, and rigidity_v99_complete.tex have been built successfully from the reviewed exact head in remote CI.

This is not a reason to reject a mathematical theorem.

It is, however, a real defect in the repository's claimed review discipline, especially because revision 98 explicitly made exact-head reproducibility part of its response.

A revision that adds more than two thousand lines of proof and new exact numerical examples should not regress on exact-head build evidence.

## 18. Disposition of the revision-98 referee requests

My assessment is now:

### R1. Reference-grade spreading theorem

**Substantially answered.**

The Rees lemma, finite-diagram lemma, explicit bad-locus construction, and completion proof materially close this request.

### R2. Formal real algebraization and descent

**Substantially answered.**

The square-slack and real-descent lemmas now track the actual real graph, selected branches, and finite label quotient.

### R3. Zero specializations and vertical components

**Substantially answered.**

The source-component zero flags and explicit exceptional recursion are now visible.

### R4. Standalone real-accessibility lemma

**Answered.**

Revision 99 has exactly such a lemma.

### R5. Full semialgebraic decay argument

**Answered at the level I requested.**

The finite-support lemma plus positive-threshold selection is a real proof rather than an appeal to Hardt triviality.

### R6. Formalize or narrow effectivity

**Partly answered.**

The direct spectral-output algorithm is substantially convincing. The stronger geometric-certificate enumeration remains too informal to carry headline weight.

### R7. Demonstrate information beyond scalar marginals

**Literally answered, conceptually only partly answered.**

The new example separates marginal envelopes from the joint diameter. It does not yet establish a deep insufficiency result for the scalar atlas in the principal model.

### R8. Broaden the remote-wall theorem or narrow framing

**Strongly answered at the literal level.**

There is now a general regular-corner entrance theorem, a second-order theorem, and a complete geometric wall.

The remaining question is whether the general theorem is deep enough under its strong hypotheses to support the broad framing.

### R9. Preserve exact-head successful CI evidence

**Not answered for v99.**

There is no v99 exact-head workflow/run/receipt at the reviewed commit.

This matrix is important. Revision 99 should not be reviewed as though it were revision 98. Most of the old technical requests have genuinely been closed.

## 19. Why I still do not recommend top-four acceptance after so many repairs

A sequence of referee repairs can make a manuscript correct without making its central theorem sufficiently consequential for a top-four general journal.

That is the situation I see here.

The manuscript has now become much better at proving the following meta-statement:

> semialgebraic singular inverse problems admit finite stratified asymptotic descriptions, and the correct leading spectral constant is obtained from a joint weighted limit rather than coordinatewise scalar bounds.

I believe this is useful.

But the individual ingredients divide into two categories.

### 19.1 General ingredients close to established machinery

- resolution/principalization;
- monomial valuation ratios;
- semialgebraic stratification;
- quantifier elimination;
- Hardt triviality;
- algebraic/Puiseux one-variable asymptotics;
- finite-dimensional algebraic optimization.

Revision 99 now handles their interfaces much better, but careful assembly is not automatically a new central theorem of the strongest general-journal class.

### 19.2 Distinctive ingredients that remain narrow

- the explicit jointly constrained spectral leading set;
- the full-rank binary multiplicity constants;
- the cubic exact-fibre classification;
- the two identification walls;
- the remote-versus-local scale transition.

These are the parts I find most original.

They remain concentrated in a specific finite-dimensional polynomial experiment.

The missing step is a theorem that turns the distinctive phenomena into a broad mathematical principle.

## 20. What would change my assessment

I see three coherent routes.

### Route A: make the joint weighted degeneration a genuine new invariant theorem

Do not merely define \(\mathcal C_0\) and compute its diameter.

Prove a theorem explaining its canonical geometric status.

For example, identify it with an intrinsic weighted normal/tangent object of the real constrained graph and derive nontrivial consequences from that identification that are not available from scalar valuation data.

Then establish functoriality or invariance properties that make it a reusable object beyond this paper.

### Route B: build a real theory of remote identification walls

Use the general entrance theorem as a starting lemma, not the endpoint.

Prove a structural theorem telling the reader when a singular inverse problem has a regular polyhedral remote entrance, what happens when that regularity fails, and how entrance exponents/critical corrections stratify in families.

The two cubic walls could then become model examples of a genuinely general wall theory.

### Route C: make this a focused explicit paper

Reduce the general atlas infrastructure to the minimum needed for the application and center the manuscript on:

1. the binary polynomial observation model;
2. the multiplicity law;
3. the complete cubic fibre;
4. the cross-rank inverse;
5. the local Fisher normal form;
6. the weight wall;
7. the geometric endpoint wall;
8. the general metric-projection lemma as supporting machinery;
9. the contrast between multiplicity crossover and remote identification loss.

This would be a strong, coherent paper even if it abandoned the claim of founding a general finite spectral-atlas theory.

For a top-four venue, Route A or B would be more persuasive. For a broader high-level journal, Route C may be the cleanest article.

## 21. Specific revisions required before I would reconsider at the same journal class

### R1. Identify the joint initial fibre relative to standard weighted tangent/initial constructions

Give a precise comparison theorem, not merely a paragraph of analogy.

If the object is genuinely different because of fixed-centre real inequalities, explain exactly where and prove the distinction.

### R2. Add a nontrivial structural theorem for the joint object

The theorem should say more than “the limit exists and its root-image diameter is the constant.”

Provide canonicality, functoriality, classification, reconstruction, or another mathematically substantive property.

### R3. Strengthen the scalar-separation result inside the principal observation model

Preferably keep the full scalar divisor/order atlas, or a substantially richer scalar data set than coordinate projections, fixed while changing the joint spectral leading set.

### R4. Reposition the general remote-entrance theorem against variational analysis

Either show that the theorem materially exceeds standard sensitivity/value-function results under comparable hypotheses, or cite the standard result and move the novelty to the algebraic verification of its hypotheses.

### R5. Broaden the wall theory or narrow the claims

Treat a structural class beyond the one cubic family, or explicitly frame the wall theorems as complete analysis of that family rather than as evidence of a general classification.

### R6. Narrow the geometric effectivity claim

Keep the direct quantifier-elimination algorithm for spectral outputs.

Unless the authors want to formalize the entire certificate-encoding model, demote exhaustive geometric-certificate enumeration from the main theorem.

### R7. Add v99 exact diagnostics

The new critical examples need a committed exact-arithmetic record reproducing:

- \(\mu_B^2\);
- \(\mu_Bk_B\);
- the projected Gram data;
- KKT signs;
- isolating intervals;
- the corresponding weight-wall \(k_E\) data.

The manuscript's statement that these are “retained with the exact regression” should become literally true.

### R8. Restore exact-head CI

Add a v99 workflow that compiles the principal/archive/complete v99 entrypoints from the reviewed head and reruns all v99-specific exact diagnostics.

Preserve the runtime receipt and source-input graph.

### R9. Add a v99 response/manifest package

Revision 99 is a direct response to a detailed v98 review. A point-by-point response explaining which old objections were closed and where would materially improve auditability.

### R10. Expand the literature positioning

The paper needs a serious comparison with the mathematical literatures nearest to

- weighted tangent/initial degeneration;
- real and definable tangent geometry;
- sensitivity and variational analysis for constrained distance/value functions;
- singular inverse problems with nonidentification.

A ten-item bibliography is not adequate to establish priority and conceptual novelty for claims this broad.

## 22. Editorial and expository comments

The exposition is much more disciplined than in early versions of this project, but revision 99 is becoming conceptually overloaded.

Several recommendations:

- Make the distinction between “scalar order theorem,” “joint weighted limit theorem,” and “model-specific Fisher normal form” visible in the section architecture.
- Do not call the joint limit new merely because it is joint; explain its relation to established tangent constructions.
- Keep the excellent warning that Hardt triviality gives topology, not a metric rate.
- Keep the warning that no general leading set is claimed to be quadratic.
- Keep the distinction between local and whole-model moduli explicit.
- Keep the statement that the separation theorem concerns marginal scalar data and does not rule out recovery from arbitrary scalar functions.
- Keep the fixed-degree/full-rank/coprime/binary qualifiers every time the multiplicity theorem is summarized.
- Keep the statement that the remote theorem is not a classification of all rank-deficient singularities.
- Do not use the very large explicit Fisher constants as evidence of universality; they are examples of conditioning.
- Separate theorem statements from repository-validation statements. Exact arithmetic in an example is mathematics; the fact that a script reproduces it is evidence, not part of the theorem.
- Consider moving the complete geometric-certificate effectivity search out of the main proof narrative unless it becomes a central contribution.

## 23. Correctness assessment

My present view is substantially more favorable than for revision 98.

### General atlas

The proof interfaces are now serious. I do not have a counterexample to the stated relative real-principalization or uniform-definable-asymptotic conclusions.

### Joint leading set

The fixed-centre construction and Hausdorff/root-image argument appear mathematically consistent.

### Multiplicity theorem

I found no new contradiction in the imported full-rank multiplicity formulas.

### Cubic exact fibre

The affine-pencil classification remains convincing.

### Cross-rank inverse

The new dimensional conventions and robust endpoint estimates make the argument easier to audit. I do not see a determinant-division failure hidden in the proof.

### Remote entrance

The first- and second-order general formulas are plausible under the stated regular-corner hypotheses.

### Geometric wall

The endpoint cone and outward-speed obstruction are convincing.

Therefore my recommendation is **not** a correctness rejection based on an identified false theorem.

## 24. Originality assessment

The paper's strongest original-looking ideas are:

1. retaining the full jointly constrained weighted coefficient limit before applying the root map;
2. distinguishing multiplicity singularity from global remote identification failure;
3. the explicit exact-fibre and two-wall geometry of the rank-deficient cubic model.

The weakest originality claim is the idea that finite stratification + rational exponent + Nash leading coefficient + effective algebraic description is itself a new theory. Much of that package is what one expects after resolution and semialgebraic definability once the correct object has been identified.

The authors should therefore stop asking the infrastructure to carry the paper's originality and make the genuinely new object/phenomenon mathematically stronger.

## 25. Depth assessment

The direct cubic analysis has real depth.

The real-algebraic appendix is technically substantial, but much of its depth lies in correctly combining known tools.

The remote perturbation theorem is elegant but elementary relative to the difficulty encoded in its chart/coercivity hypotheses.

A top-four paper needs one more conceptual theorem connecting these layers.

## 26. Breadth assessment

The framework is extremely broad.

The demonstrated nontrivial phenomena remain narrow.

That breadth mismatch is now a more important weakness than proof completeness.

## 27. Reproducibility assessment

The repository discipline improved markedly in revision 98 and regressed in revision 99.

At the exact reviewed head:

- no v99 workflow;
- no exact-head Actions run;
- no v99 diagnostics package;
- no v99 response package;
- no v99 runtime receipt;
- no visible committed exact regression supporting the newly quoted critical intervals.

This should be fixed irrespective of venue.

## 28. Final assessment

Revision 99 is the first version in this A2 line for which I would say that the authors have largely paid the technical debt identified by the prior report.

That is a significant achievement.

The consequence is that the paper can now be judged on the question that technical gaps previously obscured:

> Is the central mathematical discovery, after standard real-algebraic and definable machinery is granted, sufficiently canonical, deep, and broad for a top-four general mathematics journal?

My answer is still no.

The joint weighted set is useful, but its relation to standard weighted tangent/initial geometry is not established. The new separation theorem proves a marginal-versus-joint distinction by a relatively elementary pairing construction. The general remote theorem is a clean perturbation result under strong regular-corner assumptions; the hard verification is completed only for two walls of one cubic binary family. The broad finite-atlas machinery is now much more believable, but the distinctively new structural mathematics has not expanded to the same breadth.

I therefore recommend **rejection in the present form** at the stated journal class.

I would, however, explicitly encourage a further revision or a restructured submission. Unlike the revision-98 report, I am not asking the authors to finish a missing proof architecture. I am asking them to decide what the new theory actually is and prove a theorem that makes that answer unavoidable.

A successful next revision should not add more infrastructure. It should sharpen the conceptual center.
