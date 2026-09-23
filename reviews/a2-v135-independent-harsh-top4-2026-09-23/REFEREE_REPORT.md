# Independent referee report on A2 revision 135

**Manuscript:** *Intrinsic reconstruction of webs from nonreduced multiplication-failure schemes*  
**Author:** Qian Qi  
**Reviewed branch:** \`revision/a2-v135-structural-support-proof-2026-09-23\`  
**Reviewed branch head:** \`003fb13458c8ed11e2973963493a662f31c700c0\`  
**Source commit recorded by the build:** \`390ae3a73f097fdbdc0a84771fd35e155ad79ed8\`  
**Previous controlling report:** \`reviews/a2-v134-independent-harsh-top4-2026-09-23/REFEREE_REPORT.md\`, commit \`a08b157800c27c0f73f0c5c9a52155265ef4f395\`  
**Date of this report:** 23 September 2026

This is an independent owner-requested, AI-assisted mathematical referee report. It is not a decision issued by a journal.

## 1. Recommendation and executive assessment

**Recommendation: reject in present form, with a substantially improved fresh submission worth serious top-four-level reconsideration.**

Revision 135 is a major improvement over revision 134. In particular, it does not merely add more exact certificates around the previous proof. It repairs the two representation-theoretic points that I regarded as the most serious internal proof-presentation defects in the previous report:

1. the singular contraction-kernel argument is now separated into a genuine weight-and-shear descent lemma with the determinant twist and noncancellation treated explicitly; and
2. the nondegenerate scalar-kernel step is now backed by an explicit \(SO_4\) decomposition of \(\bigwedge^3\operatorname{Sym}^2V\), so that the absence of the determinant character is no longer hidden inside a compressed parity argument.

The new 24-page focused reconstruction article is also a much more credible paper than the earlier 80-page accumulation of every boundary calculation. The main proof now has a recognizable spine: intrinsic deepest stratum, oriented normal cone, two-component Schur readout, one common projective coordinate change, exterior-support separation, and reconstruction on the full smooth-Jacobian locus.

After checking the new shear lemma, the \(SO_4\) character calculation, the contraction kernels, the support table, and the secant/tangent exclusion in detail, I did **not** find a counterexample or an evident internal algebraic contradiction in the new v135 repair. The global inverse theorem is now mathematically plausible in a way that it was not several revisions ago.

That is nevertheless not enough for acceptance in a general top-four mathematics journal. The principal remaining blocker has changed. It is now the **scholarly and novelty boundary of the central theorem**, not an obvious missing local calculation. The manuscript itself records that the complete Ballico 1993 paper has still not been read at theorem level and that historical priority is not certified. In addition, the new literature section does not yet engage the most directly relevant skew/exterior subspace-variety and skew-flattening literature. Since the support theorem is now the main new engine of the paper, this omission is material.

I would therefore not recommend acceptance, nor a routine minor revision. The paper needs one more genuinely scholarly revision in which the authors close the relevant historical source, compare the new contraction/support theorem against the direct exterior-tensor literature, and make two subtle intrinsic-functoriality transitions completely audit-ready. If those tasks are completed without shrinking the theorem and without discovering anticipation, the focused reconstruction article could merit a fresh high-level review.

## 2. What revision 135 actually fixes

### 2.1 The singular contraction-kernel proof is now substantially adequate

The new Lemma \`lem:shear-descent\` is the correct kind of repair.

For \(V=A\oplus B\), the manuscript records the actual weights of the \(B\)-scaling torus on
\[
\det V\otimes \operatorname{Sym}^kA\otimes\operatorname{Sym}^{m-k}B,
\]
namely \(\dim(B)+m-k\). These weights are distinct, so an invariant subspace decomposes by \(A\)-degree. This resolves the previous ambiguity about projecting before differentiating.

The derivative argument is also explicit. If
\[
F=\sum_{|\beta|=k}a^\beta f_\beta
\]
and \(f_\beta\neq0\), taking \(\alpha=\beta-e_i\) makes the coefficient of \(a_i\) in \(\partial_A^\alpha F\) exactly \(\beta!f_\beta\). No second degree-\(k\) monomial can contribute to that coefficient. The infinitesimal shear is \(b\partial_{a_j}\), the determinant factor is unchanged under the unipotent shear, and multiplication by \(b^{k-1}\) is injective in \(\operatorname{Sym}B\). This is the missing noncancellation statement from v134.

In the application to the singular bilinear form \(q\), the stabilizer really does contain the stated shears because \(B=\operatorname{rad}(q)\). The manuscript then checks that the degree-one piece
\[
\det V\otimes A\otimes\operatorname{Sym}^3B
\]
is irreducible for the full \(O(A)\times GL(B)\), including the rank-two orthogonal case where the two \(SO_2\) weight lines are exchanged by a reflection. The explicit nonvanishing
\[
4\kappa_q(\epsilon\otimes ab^3)
=(bx_2)\wedge(bx_3)\wedge b^2
\]
then excludes a kernel on the degree-one piece. The shear lemma forces every hypothetical positive-\(A\)-degree kernel vector down to that piece.

This is a real proof, not a computational proxy for one.

### 2.2 The nondegenerate determinant-character step is now auditable

The new Lemma \`lem:orthogonal-exterior-cube\` gives
\[
\begin{aligned}
\bigwedge^3\operatorname{Sym}^2V\simeq{}&
[6,0]\oplus[0,6]\oplus[4,4]\oplus2[4,2]\oplus2[2,4]\\
&\oplus[2,2]\oplus2[2,0]\oplus2[0,2]
\end{aligned}
\]
under \(SL_2\times SL_2\to SO_4\).

The proof expands the skew Cauchy decomposition and records all one-factor \(SL_2\) calculations. The dimension check gives \(120=\binom{10}{3}\), and there is no \([0,0]\) summand. Since the determinant character of \(O_4\) restricts trivially to \(SO_4\), an \(O_4\)-equivariant image of the determinant line would give an \(SO_4\)-fixed vector, which does not exist. This is a much cleaner argument than the earlier exceptional-character paragraph.

The source harmonic decomposition
\[
\det V\otimes\operatorname{Sym}^4V
=
(\det V\otimes\mathcal H_4)
\oplus
(\det V\otimes\rho\mathcal H_2)
\oplus
(\det V\otimes\mathbf C\rho^2)
\]
is then used correctly: the scalar line is killed, and explicit coefficients \(2\) and \(2/3\) prove nonvanishing on the other two irreducible summands.

I regard the v134 objection on this point as closed.

### 2.3 The exact exterior-support table is internally clean

Given the contraction-kernel theorem, Proposition \`prop:exact-schur-support\` is efficient and convincing.

For a quartic with essential-variable space \(H\) of dimension \(d<4\), the annihilating singular bilinear forms are exactly those with \(H\subset\operatorname{rad}(q)\), hence a space of dimension
\[
\dim\operatorname{Sym}^2(V/H)^*
=\frac{(4-d)(5-d)}2.
\]
The support-annihilator identity therefore gives support dimensions
\[
4,\quad7,\quad9
\]
for \(d=1,2,3\).

For \(d=4\), no singular \(q\) annihilates the Schur image. A nondegenerate \(q\) does so exactly for a quadratic square, and projective uniqueness of the square root gives a one-dimensional annihilator in that case. Hence the remaining support values are \(10\) and \(9\).

The smooth-quartic consequence is immediate and is one of the strongest pieces of the paper: a smooth quartic is neither a cone nor a quadratic square, so its Schur component has full exterior support ten.

### 2.4 The secant/tangent obstruction is genuinely effective

The support-eight bound is elementary but decisive. A sum of two decomposable four-vectors uses at most the sum of two four-dimensional supports. A tangent vector in
\[
\bigwedge^3R\wedge W
\]
uses at most \(R\) plus four extra directions. Thus every secant or tangent vector relevant to the component pencil has support at most eight.

If a second decomposable point \(z\) existed on the pencil through \(w_R\), then \(Qw_R\) would be a linear combination of the two decomposable vectors \(w_R,z\), contradicting support at least nine. If the residual point collided with \(w_R\), then \(Qw_R\) would be tangent, giving the same contradiction. A Grassmann line is also tangent. This eliminates the secant, double-point, endpoint, and flag-line alternatives on the smooth family.

This is a much more conceptual global argument than the older finite separating-certificate strategy.

### 2.5 The editorial split is a real improvement

The principal article is now 24 pages according to the source-bound build receipt. The technical companion is 66 pages, and the combined archival object is 86 pages. This is a reasonable response to the previous objection that a top-four submission should not read like a version-control archive.

The main inverse theorem no longer depends on the entire higher-corank primary-boundary program. The supplement can preserve that mathematics without forcing it into the central narrative.

For an actual journal submission I would make the 24-page article the submission object and treat the large companion as a separate supplement or separate paper. The 86-page combined file should remain archival, not editorially primary.

## 3. Audit of the global inverse theorem

I summarize the proof chain because the quality of the paper now depends on this chain rather than on any one coordinate certificate.

### 3.1 Intrinsic deepest stratum

The reduction of the failure scheme is the Schubert determinant divisor. Iterating the reduced singular locus three times recovers
\[
\Sigma_0(R)=\operatorname{Gr}(4,S_R).
\]
The local Schur-complement argument is standard and sufficient for the reduced determinantal stratification.

Near \(K_0\subset S_R\), the transverse normal-cone ideal is
\[
(\det T)\, I_6(\gamma_R\operatorname{Sym}^2T).
\]
Since \(T\) invertible makes \(\gamma_R\operatorname{Sym}^2T\) surjective, the maximal-minor ideal is the unit ideal away from \(\det T=0\). Hence the reduction of the cone is the determinant hypersurface. This part is economical and does not need the much larger boundary atlas.

### 3.2 Orientation of the tensor factors

The rank-one locus of the determinant cone is a relative Segre
\[
\mathbf P(V)\times \mathbf P(\mathcal K_0^*)
\]
over \(\Sigma_0(R)\).

The manuscript distinguishes the two ruling families by projective triviality: the \(\mathbf P(V)\)-ruling is trivial, while \(\mathbf P(\mathcal K_0^*)\) is not, as seen after restricting to a Schubert line where
\[
\mathcal K_0^*|_{\mathbf P^1}
\simeq\mathcal O^{\oplus3}\oplus\mathcal O(1).
\]
This is a clever intrinsic way to remove the matrix-transposition ambiguity.

I accept the geometric idea. I ask for one strengthening of its functorial formulation below in S135.1.

### 3.3 Recovery of the two Pluecker components

Dividing the degree-sixteen cone ideal by the determinant equation recovers the degree-twelve maximal-minor space. The universal map
\[
\Phi_{V,U}:
\bigwedge^6\operatorname{Sym}^2(V)^*
\otimes
\bigwedge^6\operatorname{Sym}^2(U)
\longrightarrow
\operatorname{Sym}^{12}(V^*\otimes U)
\]
is treated before fixing the web, and the multiplicity-free Cauchy decomposition separates the two left coefficient lines. This is the correct way to avoid the old mistake of pretending that a fixed slice is itself a \(GL(V)\)-representation.

The explicit highest-weight nonvanishing check also removes dependence on a numerical web.

Exterior duality then identifies these two coefficient lines with the \(175\)- and \(35\)-dimensional Pluecker components, with a common determinant twist.

### 3.4 One common projective change of coordinates

The \`common-g\` lemma is indispensable: recovering two projective lines independently would not reconstruct a web unless the same projective transformation transports both.

The present proof uses the oriented Segre bundle to obtain an isomorphism of the \(V\)-factor, then argues that the corresponding map
\[
\Sigma_0(R)\longrightarrow PGL(V)
\]
is constant because the source is connected projective and the target affine. Fibrewise the tensor-space isomorphism is \(T\mapsto gTh^{-1}\), and functoriality of \(\Phi\) makes the \(h\)-factor act only on the right Cauchy factors.

This is plausible and I see no immediate contradiction. However, because this is the bridge from an **abstract scheme isomorphism** to a single global \(g\), it still deserves a more intrinsic bundle-level formulation; see S135.1.

### 3.5 Uniqueness on the component pencil

Once both components are transported by the same \(g\), the remaining candidates lie on
\[
\mathbf P(\mathbf C Pw_R\oplus\mathbf C Qw_R).
\]
The support theorem proves that this line meets the Grassmannian in the one reduced point \([w_R]\) throughout the smooth-Jacobian locus. The conclusion
\[
\widehat D_R\simeq\widehat D_{R'}
\Longrightarrow
R'=gR
\]
then follows.

This is the correct architecture for the inverse theorem.

## 4. Blocking issue B135.1: the Ballico 1993 comparison is still open

This is no longer a side remark.

The manuscript itself records

- \`Ballico_1993_full_text_obtained=false\`;
- \`priority_certified=false\`; and
- the six theorem-level comparison axes remain unverified.

The relevant paper is

E. Ballico, *On the Failure Locus of Higher Order Properties of Embeddings in Projective Spaces*, **Mathematische Nachrichten** 163 (1993), 5--13.

The bibliographic existence, journal, year, and page range are not in doubt. What is missing is the mathematical content needed for comparison.

The title and the later failure-locus line of work are close enough to the present subject that a referee for a general top-four journal cannot simply treat the source as permanently inaccessible background. I am **not** asserting that Ballico anticipated the current inverse theorem. I am asserting the opposite kind of epistemic point: until the article has actually been read, neither anticipation nor nonanticipation has been established.

Before this paper is submitted again at this level, the authors should obtain the complete article by a lawful library route and record a theorem-level comparison of at least:

1. the parameter spaces;
2. whether the failure locus is reduced, determinantal, Fitting, or carries further scheme structure;
3. which multiplication maps or higher-order properties vary;
4. whether infinitesimal, nilpotent, colon, or normal-cone structure appears;
5. whether any relative/base-change statement is proved;
6. whether there is any inverse/reconstruction statement from a failure locus.

This is a **blocking scholarly issue**. If the comparison shows no anticipation, say precisely why. If it reveals overlap, rewrite the novelty statement accordingly. A top-four referee should not be asked to certify historical novelty while the manuscript itself identifies the closest old source as unread.

## 5. Blocking issue B135.2: the new support theorem is still not positioned against the closest exterior-tensor literature

Revision 135 improves the literature section, but the comparison is still not centered tightly enough on the actual new engine.

The manuscript cites Landsberg--Weyman on tensor-product subspace varieties and correctly says that this is only methodological context. It also cites Carlini for essential variables and Boralevi for Grassmannian tangents. Those are useful references.

However, there is direct literature on **skew/exterior subspace varieties and skew-flattenings**, which is closer to the present support argument than Segre tensor-product subspace varieties.

At minimum, the revised audit should engage:

- J. M. Landsberg and G. Ottaviani, the Grassmannian/skew-flattening discussion in their work on equations for secant varieties. In the Grassmannian section, the first skew-flattening is used to define
  \[
  \operatorname{Sub}_p(\bigwedge^k W)
  =
  \{[z]:z\in\bigwedge^kW'\text{ for some }\dim W'=p\},
  \]
  with the set-theoretic minors description, and the standard containment
  \[
  \sigma_r(\operatorname{Gr}(k,W))
  \subset
  \operatorname{Sub}_{rk}(\bigwedge^kW).
  \]
- John Sheridan, *Divisor Varieties of Symmetric Products*, **IMRN** 2022, 9830--9863, especially the explicit formulation of the enclosing space of a skew tensor and the associated skew subspace variety as a contraction-rank degeneracy locus.

These references do not by themselves appear to prove the manuscript's specialized theorem
\[
\ker\bigl(
\iota_q\circ j:
\det V\otimes\operatorname{Sym}^4V
\to
\bigwedge^3\operatorname{Sym}^2V
\bigr)
\]
for every rank of \(q\). Nor do they obviously give the exact reduced pullbacks of support \(4,7/8,9\) under the specified Schur embedding. The specialized calculation may therefore be genuinely new.

But that is exactly what must be established by comparison rather than by omission.

The revised literature section should answer, theorem by theorem:

1. Is the embedding
   \[
   \det V\otimes\operatorname{Sym}^4V
   \hookrightarrow
   \bigwedge^4\operatorname{Sym}^2V
   \]
   standard only as a multiplicity-one plethysm summand, or has this specific polarization map been used in prior skew-flattening work?
2. Has the restriction of the first skew-flattening to this Schur summand been decomposed before?
3. Are the kernel dimensions for bilinear ranks \(1,2,3,4\) a known orbit calculation?
4. Are the inverse images of the exterior subspace varieties under this Schur embedding known?
5. Is the exclusion from \(\sigma_2(\operatorname{Gr}(4,10))\) merely an immediate standard corollary once the kernel table is known, or has that incidence already been recorded?
6. What, precisely, is the new theorem after all classical skew-subspace language is stripped away?

I would not require an exhaustive history of all alternating-tensor orbit classifications. I do require the paper to compare against the literature that uses **the same ambient object** \(\bigwedge^4W\) and the same contraction/support rank.

## 6. Serious issue S135.1: make the common-\(g\) step intrinsically bundle-theoretic

I regard Lemma \`lem:common-g-functoriality\` as plausible, but it is still the most conceptually delicate step in the inverse theorem.

The proof presently says that preservation of the projectively trivial ruling yields a morphism
\[
\Sigma_0(R)\to PGL(V),
\]
and then constancy follows from projectivity of the Grassmannian and affineness of \(PGL(V)\).

For a top-four proof I want the preceding sentence expanded. In particular:

- identify the two projective bundles before and after the abstract isomorphism as objects over the induced base isomorphism \(\sigma\);
- explain why the recovered trivial ruling comes with a sufficiently canonical projective trivialization to produce a **regular** \(PGL(V)\)-valued map, rather than merely a fibrewise family of projective isomorphisms;
- track the possibility of tensoring a lifted rank-four bundle by a line bundle on the base;
- state explicitly why such a line-bundle ambiguity has no effect on the projective \(V\)-factor and on the two left Schur coefficient lines;
- only then invoke constancy.

I do not see evidence here for a counterexample. The request is about eliminating a hidden descent/trivialization step at the exact point where the proof converts intrinsic scheme data into one constant coordinate change.

A separate lemma on automorphisms of the oriented relative Segre cone would make this much easier to audit.

## 7. Serious issue S135.2: replace informal “division by the determinant” with an intrinsic ideal-quotient statement

The fibrewise algebra is clear:
\[
I_{\mathscr C_R,16}=d\,(J_R)_{12},
\qquad d=\det T.
\]
Because the polynomial ring is a domain, multiplication by \(d\) is injective.

But the global proof should formulate the recovery of \((J_R)_{12}\) without choosing a scalar equation for \(d\) on every trivialization.

The clean invariant statement is an ideal quotient or a morphism of line-bundle-twisted graded pieces. For example, after identifying the degree-four determinant line of the reduced cone, define the residual degree-twelve piece intrinsically by the appropriate colon
\[
(I_{16}:I_{\mathrm{red},4})
\]
inside the symmetric algebra, or state the equivalent bundle map and prove independence of the local generator.

This matters because the next lemma uses functoriality under an arbitrary scheme isomorphism. Saying that the degree-sixteen ideal is transported and then “dividing by the determinant equation” is mathematically intelligible, but the invariant construction should be written in the language in which the theorem is stated.

Again, I regard this as a repairable exposition/functoriality issue, not evidence that the theorem is false.

## 8. Serious issue S135.3: the principal article should state the novelty boundary in its own language

The 24-page article is now short enough that a reader should not need the 66-page companion to understand what is new.

The introduction currently does a good job separating the main inverse theorem from the technical boundary atlas. I would sharpen the novelty paragraph further:

- classical: Schubert/determinantal singular strata, Grassmann tangents, exterior support/enclosing spaces, first skew-flattening, essential variables, multiplicity-one plethysm;
- specialized/new if the literature audit confirms it: the all-ranks contraction-kernel theorem for the determinant-twisted quartic Schur summand, its exact support table, and the use of that table to prove uniqueness of the component-pencil intersection for every smooth-Jacobian web;
- inherited but essential: intrinsic normal-cone readout and common-\(g\) functoriality;
- companion-only: the extensive primary-boundary and relative-specialization theory.

That is the conceptual theorem statement a general algebraic geometer needs.

## 9. The new reduced support-pullback proposition is useful, but its scheme-theoretic limit must remain explicit

Proposition \`prop:schur-subspace-pullbacks\` is a worthwhile geometric reformulation:
\[
j^{-1}\operatorname{Sub}^{\wedge}_4
=\operatorname{Sub}^{\mathrm{sym}}_1,
\]
\[
j^{-1}\operatorname{Sub}^{\wedge}_{7,8}
=\operatorname{Sub}^{\mathrm{sym}}_2,
\]
and
\[
j^{-1}\operatorname{Sub}^{\wedge}_9
=
\operatorname{Sub}^{\mathrm{sym}}_3\cup\mathcal Q
\]
after reduction.

The manuscript is appropriately careful that these are **reduced** equalities and that it does not claim radicality of pulled-back flattening minors.

That caution is important. The main reconstruction theorem only needs pointwise support and closedness of the support-rank locus, so the lack of a scheme-theoretic equality is not a gap in the main proof.

Do not strengthen the language in a resubmission unless the corresponding ideal-theoretic assertion is actually proved.

## 10. The residual rank-one scheme and Fitting ramification are now handled responsibly

The new residual Cartier-section lemma is a meaningful improvement.

On the nonreduced rank-one determinantal base, the pencil divisor
\[
(b-a)(ca+db)
\]
splits into two effective Cartier sections after inverting \(cd(c+d)\). The proof uses a unimodular coefficient pair, monic degree-one equations over arbitrary coefficient rings, and the Chinese remainder theorem. This is the correct level of scheme-theoretic argument for the claimed base-change compatibility.

Likewise, the phrase “Fitting ramification locus of the quasi-finite part” is much better than language suggesting a global finite flat double cover. The manuscript now says explicitly what is and is not claimed.

These issues from v134 are substantially closed.

## 11. Exact computations and build evidence

The evidence package is unusually disciplined.

The build receipt records:

- 24 pages for the focused article;
- 66 pages for the supplement;
- 86 pages for the combined archival manuscript;
- ten executed exact scripts;
- the \(SO_4\) target dimension and highest weights;
- shear coefficient checks;
- support-table checks;
- source and PDF hashes;
- preservation of inherited source; and
- an explicit list of structural statements that are **not** machine-certified.

This is good practice.

The exact scripts should remain exactly what the manuscript now says they are: finite consistency checks and reproducibility evidence. They do not replace the structural proofs. I saw no attempt in v135 to blur that boundary.

## 12. Technical and editorial comments

### 12.1 The focused article is the right submission object

The 24-page \`geometry.pdf\` is coherent enough to be reviewed as a paper. The 86-page \`complete.pdf\` should not be presented as the main article to a general top-four journal. It is useful as an archival build.

The 66-page supplement contains substantial independent mathematics. Depending on the venue, it may be better as a separate companion article rather than a formal supplement whose length is almost three times the principal paper.

### 12.2 Keep essential-variable space and exterior support terminologically separate

The manuscript has improved this point. Continue to reserve:

- essential-variable space \(H\subset V\) for a quartic; and
- exterior support \(S\subset W=\operatorname{Sym}^2V\) for \(j(f)\).

The numerical jump \(d=1,2,3,4\mapsto s=4,7,9,10\) is much easier to understand when the ambient spaces are never conflated in prose.

### 12.3 Keep the determinant twist visible in every equivariant map that uses \(O_4\)

The present v135 proof is materially better here. The determinant line can be suppressed in projective support counts, but not in the character argument. The current convention is acceptable as long as it remains explicit at the maps where equivariance is used.

### 12.4 Do not weaken the historical disclaimer

The statements that the Ballico comparison is open and that priority is not certified are correct. They should remain until the comparison is completed.

### 12.5 Do not promote the ambient binary-Jacobian containment to a classification

The current corollary only states containment of the support of the rank-defect locus over the binary-quartic boundary. That is supported by the theorem. Equality, irreducible components, radicality, and the complete higher-corank primary atlas are different assertions and are properly not claimed.

## 13. Minimum revision package before another top-four submission

I would require the following before I could recommend acceptance-level consideration.

1. **Obtain and read Ballico 1993 in full.** Add a theorem-level six-axis comparison and revise the historical novelty claims based on what the paper actually says.

2. **Redo the support/secant literature audit in the direct skew/exterior language.** Engage skew-flattenings and exterior subspace varieties, especially the standard inclusion
   \[
   \sigma_r(\operatorname{Gr}(k,W))
   \subset\operatorname{Sub}_{rk}(\bigwedge^kW),
   \]
   and explain exactly what remains new for the embedded \(\det V\otimes\operatorname{Sym}^4V\) summand.

3. **Make the common-\(g\) descent fully intrinsic.** Add a short bundle-level lemma showing how an abstract cone isomorphism preserving the distinguished ruling produces one regular, then constant, projective coordinate change.

4. **Make determinant division intrinsic.** Replace local scalar language by an ideal-quotient or line-bundle-twisted graded construction and state its functoriality.

5. **Keep the 24-page reconstruction paper focused.** Do not pull the historical boundary archive back into the main theorem. Retain the companion as a separate technical object.

6. **Preserve the full scope of the theorem if the proof survives these checks.** I see no mathematical reason in v135 to retreat to a smaller generic open merely for safety. The support argument was introduced precisely to prove the full smooth-locus statement.

7. **Keep finite exact checks subordinate.** They are useful diagnostics and reproducibility evidence, not a substitute for the structural arguments.

## 14. Final assessment

Revision 135 is the strongest A2 version I have reviewed.

The manuscript has now converted the previous two most delicate representation-theoretic pivots into readable proofs. The shear descent is explicit; the \(SO_4\) exterior-cube decomposition is explicit; the contraction-kernel theorem gives a clean support table; and the support-eight secant/tangent bound gives a genuinely conceptual uniqueness mechanism on the entire smooth-Jacobian locus. The 24-page focused article is also a substantial editorial improvement.

I therefore no longer regard the principal problem as “the main theorem has an obvious missing local proof.” The remaining problem is whether the paper has established, to top-four scholarly standards, **what is genuinely new and historically unanticipated**, and whether the abstract-isomorphism-to-common-coordinate transition is written with enough intrinsic precision.

At present the answer to the first question is not yet established: the manuscript openly has not read Ballico 1993, and its support-literature audit still stops short of the closest skew/exterior subspace-variety framework.

For that reason my recommendation remains:

**Reject in present form. Encourage a fresh submission after the Ballico comparison, direct skew-flattening/subspace-variety novelty audit, and the two intrinsic-functoriality clarifications are completed.**

If those tasks are completed favorably, I would regard the focused reconstruction paper as deserving a new serious top-four-level review rather than another incremental certificate round.
