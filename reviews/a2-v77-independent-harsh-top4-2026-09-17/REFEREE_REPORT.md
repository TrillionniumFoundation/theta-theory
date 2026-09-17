# Independent harsh referee report on nominal A2 revision 77

**Manuscript:** *Boundary laws and smooth contact rigidity of periodic dispersing billiards*  
**Author:** Qian Qi  
**Date:** September 17, 2026  
**Nominal revision branch:** `revision/a2-v77-weighted-action-global-reconstruction-2026-09-17`  
**Nominal revision head inspected:** `ba8e40b92887e2cd8dcc92f3358401aac8c961d2`  
**Head tree:** `61affdf4aa743c761d09c56e88e9048cfc5106e8`  
**Frozen mathematical source identified by the repository:** `d43885eee3d05be2e896a8ac4785f4852c123131`  
**Frozen manuscript subtree recorded by the repository:** `950c448c8e8f19c6181fee26e425a9ac23b7dca9`  
**Comparison branch:** `revision/a2-v76-relative-envelope-2026-09-17`  
**Comparison branch head:** `ba8e40b92887e2cd8dcc92f3358401aac8c961d2`  
**Requested standard:** the level expected of Annals of Mathematics, Inventiones Mathematicae, Acta Mathematica, or the Journal of the American Mathematical Society.

This is an author-requested independent referee-style assessment. It is not a commissioned report from any journal and is not an editorial decision. I apply a deliberately severe general-journal standard and separate (i) version identity, (ii) mathematical correctness of the material actually present, and (iii) significance/placement.

## 1. Recommendation

**I do not recommend acceptance at the requested highest general-journal level, and I do not regard the present `v77` branch as a substantive mathematical revision of v76.**

The first point is not a matter of taste. The nominal v77 branch and the v76 source branch currently resolve to the **same commit SHA** and hence the same repository tree. The head commit itself is a verification/handoff commit whose message is `Record A2 v76 downloaded-product verification and sampled visual inspection`; the verification record identifies revision 76, not a new revision-77 mathematical source. Thus there is no v77 source delta for a referee to credit, reject, or test.

I nevertheless reread the revision-76 material that the nominal v77 branch actually contains, with particular attention to the two additions that were meant to answer the previous significance objection: the separated determinant principle and the phase-weighted actual-function envelope. I do **not** find a fatal mathematical error in those finite-dimensional/finite-phase statements. The problem is more severe from the standpoint of the requested placement: the nominal new revision contributes no new mathematics beyond what was already reviewed in v76, so the previous negative placement conclusion remains unchanged.

The manuscript contains a technically serious local inverse mechanism. What it does not presently contain is a new revision establishing the advertised `weighted-action-global-reconstruction` step, nor a theorem whose scope is commensurate with that branch name. A metadata rename is not a mathematical revision.

## 2. Version identity: the immediate blocker

### R77-B0. There is no revision-77 mathematical source delta

At the time of this review:

- `revision/a2-v77-weighted-action-global-reconstruction-2026-09-17` points to `ba8e40b92887e2cd8dcc92f3358401aac8c961d2`;
- `revision/a2-v76-relative-envelope-2026-09-17` points to the same `ba8e40b92887e2cd8dcc92f3358401aac8c961d2`;
- therefore the two branches have the same complete tree, not merely the same manuscript subtree;
- the head commit records v76 product verification, not v77 mathematics;
- `A2_REVISION_V76_VERIFICATION.md` identifies the frozen mathematical source as `d43885eee3d05be2e896a8ac4785f4852c123131` and explicitly describes the revision as revision 76.

This is a hard reproducibility problem for the review process. A referee cannot infer a new theorem from a branch name. If a revision is intended to answer the v76 report, the source commit must actually diverge from the reviewed v76 object and the response must identify that immutable source.

**Disposition:** until a distinct source commit exists, all v77-specific claims are **not reviewable**. The mathematical object currently reviewable is revision 76.

This does not invalidate the mathematics already present. It does mean that the repository currently overstates revision progress: the branch namespace says v77, while the immutable content says v76.

## 3. Scope of the mathematical rereading

Because the nominal v77 branch is source-identical to v76, I do not pretend that an additional branch name creates a fresh theorem-by-theorem certification of the 375-page full technical manuscript. I reread the parts that control the principal submission and the alleged new structural mechanisms:

- `papers/A2-v17-boundary-information-coarsening/rigidity.tex`;
- `article/00s_principal_abstract_v76.tex`;
- `article/00r_principal_introduction_v76.tex`;
- `journal/core/periodic_relative_v76.tex`;
- `journal/core/periodic_contact_v76.tex`;
- `journal/core/positive_curvature_v76.tex`;
- `article/10d_smooth_contact_rigidity_v68.tex`;
- `article/10k_relative_decoupling_v76.tex`;
- `article/10l_phase_weighted_envelope_v76.tex`;
- `article/10m_conditioning_budget_v76.tex`;
- `RESPONSE_TO_REFEREE_V76.md` and the revision verification record;
- the prior v75 and v76 independent reports as revision-history evidence, not as mathematical authority.

I treat compilation, label reachability, finite fixtures, PDF hashes and artifact checks as integrity evidence only. None of them is a substitute for proof verification.

## 4. Correctness findings on the central mechanism

### R77-C1. The separated determinant proposition is sound as stated under its strong hypotheses

Proposition `prop:v76-determinant` writes

\[
T=D+E,
\]

with `D` block diagonal and `E` block off diagonal. At `t=0`, `(I+D)^{-1}` is block diagonal, hence

\[
\operatorname{tr}((I+D)^{-1}E)=0.
\]

The exact second-variation formula

\[
\log\det(I+D+E)-\log\det(I+D)
 =-\int_0^1(1-t)\operatorname{tr}(R(t)ER(t)E)\,dt
\]

therefore yields the claimed quadratic Hilbert--Schmidt bound, with no matrix-dimension factor, once `||D+tE|| <= q < 1`. The fixed-order parameter-derivative argument is also structurally legitimate: differentiating resolvents introduces bounded operator factors while the two displayed coupling factors remain available for Hilbert--Schmidt pairing.

I do not find a missing dimension factor or an illicit use of a trace-class estimate at this abstract level.

However, this proposition is an abstraction of a mechanism already present in the inherited relative-law proof. Its mathematical correctness should not be confused with independent general-journal significance.

### R77-C2. The phase-weighted envelope calculation is also correct at the algebraic level

For

\[
(A_m z)_b=\widehat a_b^m z_{b+1},
\]

the displayed weights

\[
w_b=\left(\prod_{i=0}^{b-1}\frac{\overline a}{\widehat a_i}\right)^m,
\qquad
\overline a=\left(\prod_i\widehat a_i\right)^{1/r},
\]

satisfy `A_m w = \overline a^m w`, including at the closing phase. Consequently

\[
K_m=6A_m(I-A_m)^{-1}
\]

has Perron eigenvalue

\[
\vartheta_m=\frac{6\overline a^m}{1-\overline a^m}.
\]

Thus the sufficient condition `\overline a^m < 1/7` is a genuine phase-dependent refinement of the worst-phase scalar condition. The paper also correctly pays the norm-equivalence price

\[
\kappa(w)=\frac{\max_b w_b}{\min_b w_b}
\]

when returning to an unweighted norm.

I do not find an algebraic error in this refinement.

### R77-C3. The actual-function step continues to address the flat-function obstruction correctly

The central smooth argument does not infer equality of `C^\infty` functions from equality of all Taylor coefficients. It first identifies finite jets, then integrates the stationary variation along an interpolation between the two **actual** graph representatives and applies a contracted-envelope estimate. For a flat difference `h`, a sufficiently high finite weighted order is chosen only after the contraction margin is fixed; the full action difference is then used again to force `h=0` on a smaller collar.

That logical distinction is important and remains one of the strongest parts of the manuscript.

### R77-C4. The positive quadratic inverse is genuinely global on its positive image

The Schur relation

\[
s_i=k_i+c_i-\frac{k_i^2}{k_i+c_{i+1}+s_{i+1}}
\]

is converted into a strict contraction on the closed positive orthant. This is materially better than an argument based only on local Jacobian nonsingularity. The fixed-point/image criterion and two-point estimate are coherent, and the direct cyclic difference argument gives a second uniqueness check.

I do not find the old local-Jacobian/global-injectivity error here.

### R77-C5. The rare-event normalization is handled in the correct logical order

The relative law removes the exponentially small scalar reference twist before conditioning. In the v76 conditioning corollary, if

\[
w_N=c\,d_N\,\beta_N r_N,
\]

the scalar `d_N` cancels exactly from the conditional law. The proof compares `\beta_N r_N` to its limit rather than dividing an absolute approximation error by a rare success probability. This is the correct mechanism.

These correctness findings are positive. They do not change the placement conclusion below.

## 5. Major mathematical and editorial concerns

### R77-M1. The manuscript still proves a highly marked local inverse theorem, not a global reconstruction theorem

The principal theorem assumes a supplied clear nongrazing periodic polygon, supplied contact points and tangent/normal frames, phase labels, a closing translation, exact itinerary/gate selection, and phase-resolved endpoint laws. With two prescribed positive offsets it reconstructs the **visited smooth contact germs**. The manuscript itself correctly says that unvisited boundary arcs remain free and even constructs equal-area remote completions.

This is a legitimate inverse problem. It is not whole-table reconstruction, unmarked orbit reconstruction, or global rigidity from conventional scattering/spectral data.

The nominal branch name `weighted-action-global-reconstruction` therefore has no theorem-level counterpart in the source currently present. A top-journal referee must judge the theorem, not the branch label. On the theorem actually written, the scope objection from v75/v76 remains.

### R77-M2. The revision-specific determinant abstraction remains too close to the inherited proof to carry the placement case

The useful insight is that an off-diagonal trace must cross between the two end spaces twice, producing a quadratic coupling. But the current proposition is a finite-matrix lemma under deliberately strong assumptions:

- a common operator-norm margin below one along the full segment;
- uniform trace-class control of the diagonal blocks and their parameter derivatives;
- Hilbert--Schmidt smallness of the coupling and all fixed derivatives;
- separately supplied convergence of the two diagonal determinants.

The billiard application paragraph then says that the inherited Green/gluing proof supplies these hypotheses.

For a specialist proof this is acceptable. For the claimed conceptual elevation, it is not enough. The manuscript still lacks a fully exposed billiard corollary mapping every abstract hypothesis to a concrete estimate with rates, and it lacks a genuinely independent application showing that the proposition is more than a repackaging of the argument from which it was extracted.

A stronger revision would either:

1. prove an infinite-dimensional trace-ideal theorem with a natural hypothesis class and at least one non-billiard consequence; or
2. make the finite-dimensional theorem an explicit reusable engine with two genuinely distinct mathematical applications.

The current source does neither.

### R77-M3. The phase-weighted refinement is a tradeoff, not a uniform conditioning improvement

The geometric-mean threshold can reduce the required differentiability order. But the weight ratios satisfy

\[
\frac{w_{b+1}}{w_b}=
\left(\frac{\overline a}{\widehat a_b}\right)^m,
\]

so strong phase heterogeneity can make `\kappa(w)` extremely large. The finite-jet alignment constants and observation floors remain as well.

The manuscript mostly acknowledges this. The point remains important for significance: the refinement improves one sufficient threshold while potentially worsening another constant. The non-geometric fixture showing order `3` versus `19` demonstrates the algebraic possibility of threshold improvement; it does **not** demonstrate a realized billiard family with a comparably improved practical inverse.

At a top general-journal standard, this is a useful quantitative refinement, not a decisive new theorem by itself.

### R77-M4. The main conceptual theorem has not been enlarged since the negative v76 placement report

The data model, target, and principal uniqueness theorem are unchanged. The new v76 material reorganizes and sharpens the mechanism, but it does not remove a major exact-information interface or enlarge the spatial target.

A revision capable of changing the placement judgment would need a substantive mathematical delta of one of the following kinds:

- reconstruction from materially less marked data;
- a natural uncalibrated/unknown-interface formulation that removes one of the exact marks now assumed;
- a genuinely global smooth rigidity conclusion under natural observations;
- or an abstract inverse principle with consequences well outside the billiard application.

The nominal v77 branch currently provides **none** of these, because it provides no mathematical delta at all.

### R77-M5. The finite-preparation result remains a conditional consequence, not a second independent breakthrough

The sampling theorem is built on a bounded class with fixed geometric margins, exact gate/itinerary tags, independent normalized Liouville resets, bounded post-acceptance sensor error, finite-flight control, and an actual-table selection mechanism. The rarity exponent and smoothing exponent are correctly exposed.

This is mathematically useful because it connects the deterministic inverse to a concrete experimental protocol. But it should not be counted as an independent broad statistical inverse theorem. It is a consequence of the deterministic mechanism under a strongly specified design.

The conditioning section is commendably explicit about this and should remain so.

### R77-M6. Repository verification is unusually detailed but cannot substitute for mathematical novelty

The manuscript infrastructure records source preservation, active labels, native products, PDF hashes, finite algebraic fixtures, and visual checks. This is good engineering. It is not mathematical evidence that a top-four placement objection has been answered.

The current versioning problem illustrates the danger: the repository can have excellent verification of v76 while simultaneously exposing a v77 branch with no new source. The distinction between integrity and revision content must be kept strict.

## 6. What the nominal v77 would have needed to contain

The branch name suggests a planned response involving a weighted action or a global reconstruction principle. No such new revision is present. For a genuine revision 77 I would expect, at minimum, the following items to be immutable in the branch itself:

1. **A distinct mathematical source commit** diverging from `ba8e40b92887e2cd8dcc92f3358401aac8c961d2`, with the source SHA identified in a revision ledger.
2. **A response to the v76 referee report** mapping each issue to exact theorem/section changes and explicitly stating which objections are correctness issues and which are placement/significance issues.
3. **A theorem-level statement matching any `global reconstruction` claim.** If the result remains local contact-germ determination, the branch/revision language should say so.
4. **An explicit instantiation of the two-end determinant abstraction** in the billiard setting, listing the end blocks, middle deletion, trace-norm and Hilbert--Schmidt rates, operator margin, and parameter-derivative losses.
5. **A principled treatment of the phase-weight tradeoff.** If the geometric-mean refinement is advertised as important, exhibit a geometrically realizable class where it changes the usable regularity/conditioning regime, or explain clearly why the abstract criterion is the main contribution even without such an example.
6. **A stronger significance bridge.** Either broaden the inverse theorem or demonstrate that the extracted mechanism solves another natural problem not reducible to the present marked periodic-orbit setup.

Without these, another branch number would amount to revision bookkeeping rather than mathematical progress.

## 7. Specific editorial comments

1. The symbol `D_N` in Proposition `prop:v76-determinant` denotes a block-diagonal operator, while `D_{N,b}` elsewhere denotes the scalar reference twist. The text warns the reader, but the collision remains avoidable and should be removed.
2. The abstract's phrase `phase-weighted envelope estimate replaces a worst-phase sufficient order criterion` is accurate only as a sufficient-order statement. The unweighted condition number cost should remain visible wherever this refinement is highlighted.
3. The principal introduction correctly states that the result concerns supplied marks and visited contact germs. Preserve that precision. Do not let future branch names or summary prose silently upgrade the theorem to whole-boundary reconstruction.
4. The determinant abstraction would read more convincingly if followed immediately by a named billiard corollary, rather than a prose application paragraph.
5. The source directory name `A2-v17-boundary-information-coarsening` is historical. At the present revision depth, immutable commit identifiers are essential; version numbers in paths are no longer reliable provenance on their own.
6. A revision branch must not be created before its mathematical source delta is committed and then left pointing at the previous revision. That practice makes branch discovery unreliable for referees and automation.

## 8. Final assessment

The mathematical core I rechecked is serious. In particular, I find no fatal error in the relative determinant cancellation, the positive quadratic inverse, the signed finite-jet route, or the actual-function envelope. Revision 76's phase-weighted refinement is also mathematically coherent.

But the requested standard is not `technically correct and extensively verified`. It is exceptional mathematical significance in a form whose central theorem and conceptual advance are immediately legible at a general level.

On the object actually present in the repository, the strongest result remains a carefully marked **local** smooth-contact inverse theorem. The two v76 abstractions improve its architecture and quantitative understanding, but they do not establish a new general principle of comparable reach, and the nominal v77 branch adds no mathematics whatsoever.

**Recommendation: do not accept at the requested top-four general-journal level in the present form. Do not treat the current v77 branch as a completed revision. A renewed review should begin only from a genuinely distinct, immutable mathematical source commit.**

This is a negative placement recommendation and a version-integrity objection. It is **not** a claim that the examined central theorem has been disproved, and it is **not** an instruction to delete the technical programme. The appropriate response is substantive mathematics plus clean revision provenance, not downscaling by omission and not another metadata-only branch.