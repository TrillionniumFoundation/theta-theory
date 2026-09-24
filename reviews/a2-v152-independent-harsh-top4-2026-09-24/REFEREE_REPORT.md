# Independent harsh referee report — A2 revision 152

## Manuscript and review object

**Manuscript:** *Finite failure schemes and the reconstruction of quadratic pencils*  
**Author:** Qian Qi  
**Revision reviewed:** A2 revision 152  
**Revision branch:** `revision/a2-v152-divisor-conductor-collision-geometry-2026-09-24`  
**Source-bound mathematical commit:** `6919346ef17cf3f599a03e69c722a890fe144fe1`  
**Controlling prior report:** `review/a2-v151-independent-harsh-top4-2026-09-24`  
**Controlling prior-report commit:** `11c9e91135c5e8bb3ee61a067d76286d81a3df7d`  
**Principal review object:** `papers/A2-v17-boundary-information-coarsening/article/v152/geometry.pdf`, 71 pages in the build receipt  
**Separate applications manuscript:** `applications.pdf`  
**Non-submitted historical archive:** `archive-v144.pdf`  
**Review standard:** the proof-completeness, originality, conceptual depth, inevitability, and exposition standard expected at *Annals of Mathematics*, *Acta Mathematica*, *Inventiones Mathematicae*, or *Journal of the AMS*.

This is an owner-requested independent-referee-style report, not a journal-commissioned editorial decision. I read the new v152 conductor/collision sections, the divisor-degree intersection proposition, the common pencil-orbit boundary theorem and its flag-jet lemma, the pure-power normalization-fibre proposition, the revised introduction and abstract, the response to the v151 report, the proof-scope and literature audits, the issue matrix, the theorem locator, the source lock, and the build receipt. I also re-read the controlling v151 report and the inherited normalization and closed-flag-specialization arguments on which the new results depend.

The repository reports 28 successful exact scripts, including 42 new finite checks, together with a clean build and source-preservation audit. I treat these as finite consistency evidence only. They do not prove an all-dimensional formal-local statement, establish historical priority, or decide journal significance. The manuscript and its own audit correctly make the same distinction.

## Recommendation

**Reject in the present form for a top-four general mathematics journal.**

Revision 152 is a genuine and substantial advance over revision 151. It is not a cosmetic response. The authors have added two precise completed-local-ring calculations, computed conductors, depths, Cohen–Macaulay criteria, and singular Fitting data on stated strata, and produced an actual nonnormal point lying in every full first-relation orbit closure of a pencil failure algebra. The new pure-power fibre formula also goes beyond a tangent-space calculation. The literature discussion is markedly better than in v151.

I did **not** find a simple counterexample to Theorem 8.1, Theorem 8.3, Theorem 10.1, Lemma 10.2, or Proposition 10.3. Subject to several proof-compression issues detailed below, the new algebra appears mathematically credible. My negative recommendation is therefore not a disguised correctness rejection.

The top-four problem is scale and structure. Two sharply chosen local models do not yet constitute a singularity theory of the common-divisor image. A reduced set-theoretic formula for intersections does not determine their scheme structures. One common, extremely degenerate point in all `GL(E)` orbit closures does not classify a natural boundary of quadratic pencils, distinguish pencil degeneration types, or reveal the geometry of the orbit closures themselves. The new common point forgets every pencil invariant. It proves nontrivial incidence, but not the promised organizing relation between boundary singularities and the moduli geometry of pencils.

The closest named failure-locus predecessor, Ballico 1993, also remains unavailable at theorem/proof level. The revised primary comparisons are useful and honest, but they remain explicitly bounded rather than an exceptional-novelty certification. Finally, the principal article has grown to 71 pages and 241 labels while carrying several distinct programs: an engineered finite-algebra Torelli theorem, moving-family reconstruction, coefficient recognition, stack rigidification, common-divisor normalization, local singularity theory, orbit degeneration, and spectral consequences. At present the manuscript reads as the cumulative record of a long research pipeline rather than a single inevitable top-four paper.

For a strong specialist algebraic-geometry or commutative-algebra venue, this revision is considerably more serious than v151. For one of the four general journals named above, I remain unconvinced.

---

## 1. What revision 152 genuinely adds

The revision answers important portions of the v151 report.

### 1.1 A real conductor calculation

Theorem 8.1 treats a point
\[
K=abL
\]
with two coprime degree-\(g\) divisor choices and gcd-free residual space. Under the stated uniqueness hypothesis for the two degree-\(g\) divisors, it identifies the completed image ring as
\[
\mathbf C[[z_1,\ldots,z_t,x_1,\ldots,x_c,y_1,\ldots,y_c]]/(x_i y_j).
\]
It then computes the conductor, the intrinsic singular Fitting ideal, branch intersection, multiplicity, depth, and exact Cohen–Macaulay criterion. This is the first point in the A2 revision sequence where the paper computes the gluing ring itself rather than only the normalization or one fibre of the normalization.

### 1.2 A ramified collision model

Theorem 8.3 identifies the completed local model at a double binary common root with
\[
A_m=R_m\oplus I t\subset \mathbf C[[u_1,\ldots,u_m,t]],
\qquad \Delta=t^2,
\]
up to a specified smooth factor. The presentation by
\[
u_iw_j-u_jw_i,\qquad w_iw_j-\Delta u_i u_j
\]
is scheme-theoretic, not radicalized. The conductor quotient carries the ramified double cover
\[
\mathbf C[[\Delta]]\longrightarrow \mathbf C[[t]].
\]
The depth and Cohen–Macaulay criterion are exact. This is a natural and useful higher-dimensional generalized pinch model.

### 1.3 An actual connection to failure-algebra orbit closures

Theorem 10.1 no longer leaves the common-divisor boundary beside the pencil problem. It constructs a relation space
\[
K_\infty=a^{g+k_n}L_n
\]
that lies in every full `GL(E)` orbit closure of a pencil first-relation space. The construction is not inferred from a few numerical cases: it uses an osculating filtration of the flag coefficient representation, an adapted basis, and a flat limiting relation subbundle. The full normalization fibre at this point is then described by Proposition 10.3 through reciprocal-polynomial equations.

This literally answers the request for a boundary point reached by genuine failure algebras rather than an unrelated common-factor example.

### 1.4 A materially improved literature discussion

The revised introduction now compares the normalization and singularity mechanisms with Chipalkatti, Kurmann, Hu–Lin–Shao, Ferrand, Abramovich–Olsson–Vistoli, and Fevola–Mandelshtam–Sturmfels. The manuscript carefully distinguishes a single binary form, a tuple of binary forms, an unframed Grassmannian subspace, and a full first-relation orbit. It no longer presents uniqueness plus tangent injectivity, conductor squares, or generic rigidification as new general principles.

These are real improvements. They should be credited without reservation.

---

## 2. Correctness audit of the split-divisor theorem

Theorem 8.1 is plausible and, in its stated range, likely correct. The main ingredients fit together:

1. the normalization has exactly two points above the chosen image point;
2. the tangent maps to the two source branches are surjective, so the source completions are formally embedded branches of the image;
3. over local Artin bases, coprime lifted divisors satisfy
   \[
   (a_A)\cap(b_A)=(a_Ab_A),
   \]
   which identifies the formal branch intersection rather than merely its closed points;
4. the completed image is then a conductor-square fibre product of two smooth branches over their smooth intersection;
5. the displayed local ring and all stated commutative-algebra invariants follow.

The formula
\[
\operatorname{depth}\widehat{\mathcal O}_{Y_g,K}=t+1
\]
is consistent with the exact sequence from the fibre product. The Cohen–Macaulay criterion `c=1`, multiplicity two, conductor `(x,y)`, and singular Fitting ideal `(x,y)^c` also agree with the displayed model.

I nevertheless regard the proof as too compressed at precisely the point where the theorem becomes stronger than a branch-counting statement.

### 2.1 Isolate the formal-image lemma

The manuscript says that surjectivity on cotangent spaces, completeness, and Nakayama imply that the completed source ring is a quotient of the completed ambient/image ring. This is standard, but here it carries considerable weight: it turns each normalization germ into a **closed formal branch** of the image. The authors should state and prove a clean lemma with the exact hypotheses used, including the passage from the ambient Grassmannian to the scheme-theoretic image.

### 2.2 Isolate the two-branch fibre-product lemma

The equality
\[
\widehat{\mathcal O}_{Y_g,K}
 = (R_0/I_a)\times_{R_0/(I_a+I_b)}(R_0/I_b)
\]
uses more than the existence of two normalization points. One needs the completed image to be reduced, the two formal branch ideals to have zero intersection in the completed image, and the Artin-functor computation to identify the scheme-theoretic branch intersection with the proposed smooth factor. These facts are believable in the present excellent finite-type setting, but they should be assembled into one explicit proposition. The current proof makes the conclusion appear nearly formal once the tangent maps are surjective; it is not.

### 2.3 Make the separation of the two normalization germs explicit

The hypothesis says that the only degree-\(g\) divisors are `[a]` and `[b]`. Formal neighbourhoods of these two points in the finite normalization are disjoint, but this separation should be stated before the argument introduces “unique marked lifts” over every local Artin base. This would remove any ambiguity about whether an infinitesimal divisor can move between the two components.

### 2.4 The theorem remains a theorem on one stratum

Even if every proof detail is accepted, Theorem 8.1 describes a highly controlled locus: exactly two coprime divisor choices, no further degree-\(g\) divisors, and gcd-free residual space. It does not determine the conductor where three or more divisor choices meet, where the chosen divisors have a common part, where the residual space has its own gcd, or where several collision types occur simultaneously. This limitation is stated in the paper, but it is central to the significance assessment.

The result is a valuable local normal form. It is not yet a stratified conductor theorem for `Y_g`.

---

## 3. Correctness audit of the binary collision theorem

Theorem 8.3 is also convincing in outline.

The Weierstrass preparation step selects a member with exact order two at the common root. Independent two-jet variations in the Grassmannian provide formal coordinates
\[
a,b,u_i,v_i.
\]
After completing the square, the common-root incidence becomes
\[
\Delta=t^2,\qquad w_i=u_it.
\]
The elimination argument is clean: every class reduces to
\[
p+\sum_i w_i p_i,
\]
and the kernel is controlled by the Koszul first syzygies of the regular sequence `(u_1,\ldots,u_m)`. The finite birational extension to the regular normalization and the conductor calculation are then elementary. The depth computation from `A_m=R_m\oplus I` is also correct-looking.

The following points still deserve revision.

### 3.1 The versality-to-image step should be a formal proposition

The proof says that the independently varying two-jets and Weierstrass division give the entire completed image, rather than an embedded test slice. This is exactly the subtle distinction the earlier reports demanded. It should not be left in two paragraphs of coordinate discussion. The authors should formulate the relevant completed incidence functor and prove that the displayed parameters give an isomorphism of functors, including independence of the chosen frame member `F_0` and changes of Weierstrass coordinate.

### 3.2 The general singular subscheme is not actually simplified

For `m=1`, the paper computes the singular ideal explicitly as
\[
(w,\Delta u,u^2).
\]
For arbitrary `m`, it says that the singular subscheme is defined by the relevant Jacobian minors. That is true, but it is essentially the definition of the Fitting singular scheme applied to the displayed presentation. It is not a structural formula analogous to `(x,y)^c` in Theorem 8.1.

The abstract and introduction should therefore not leave the impression that the intrinsic singular ideal has been explicitly determined in all binary collision ranks. The full ring is determined; the general Fitting ideal is only presented algorithmically.

### 3.3 The higher-collision hierarchy is absent

A double root is the first collision. The paper does not treat triple common roots, collisions of several clusters, mixed multivariate divisor overlap, or closure relations among these local types. For a specialist paper, one exact binary collision model is meaningful. For a top-four singularity theory, it is only the first case.

---

## 4. Proposition 9.1 is correct but modest

The common-part formula for
\[
(Y_a\cap Y_b)_{\mathrm{red}}
\]
is a useful organizational statement. Its proof by unique factorization and proper images is sound at the level claimed.

But the reduction is doing nearly all the work. The proposition does not calculate the scheme-theoretic intersection, embedded components, multiplicities, conductor interaction, or tangent cones. It does not determine when the components `M_j` are distinct, how they meet, or their closure order. In several variables, even the incidence of factor degrees can be subtle because divisor degrees are not an interval for a general polynomial.

Thus Proposition 9.1 should not be counted as a “divisor-poset stratification theorem.” It is a finite description of the underlying reduced intersection set. The two local models supply full scheme structure on two special loci, but no global bridge between the reduced formula and those local thickenings is proved.

There is also a small statement-level correction. The sentence asserting that at `K=a_0^mL` the positive divisor degrees are exactly `{1,\ldots,m}` is valid only when `a_0` is a linear form, as in the later boundary theorem. This hypothesis should be written in Proposition 9.1 itself.

---

## 5. The common ramified boundary theorem

Theorem 10.1 is the most important new integration result in v152. I find the basic construction credible.

For nonzero `\tau`, multiplying adapted basis vectors by the nonzero scalars `\tau^{-d_j}` does not change their span. At `\tau=0`, the associated-graded initial forms remain independent. Thus the adapted columns define a flat rank-`r` limit of the primitive coefficient space. Multiplication by the determinant power then gives a flat family of first-relation spaces, and truncation at degree `D` gives a finite locally free family of algebras. The exact highest osculating degree is three in dimension three and four in higher dimension, according to the explicit flag-coordinate calculation.

The two-stage orbit argument is also logically valid if the inherited closed-flag specialization is accepted:

1. every pencil relation orbit closure contains the flag-pencil relation point;
2. the flag-pencil relation orbit closure contains `K_\infty`;
3. hence every pencil relation orbit closure contains `K_\infty`.

This is a nontrivial theorem. It should remain in the paper.

It does not, however, have the scale that the words “universal boundary” can suggest.

### 5.1 The acting group is enormous

The orbit closure is taken under
\[
\operatorname{GL}(E),\qquad E=V^*\otimes U,
\]
acting on the entire cotangent space. This is much larger than the congruence group governing quadratic pencils. The first-relation inverse shows that a general orbit point still represents an isomorphic unmarked algebra, so this is a legitimate intrinsic operation. But it also makes a common degeneration far easier to obtain than a common degeneration in the pencil Grassmannian or in a natural compactification of pencil moduli.

The theorem should be advertised as a statement about **full first-relation coordinate-change orbit closures**, not as a classification of the boundary of quadratic pencils.

### 5.2 The point is common, not canonical

The displayed `K_\infty` depends on a standard flag pencil, a chosen scalar direction `a`, a complement `B_{11}=0`, and an adapted basis of the osculating filtration. Different choices produce conjugate or related limits. What is intrinsic is the containment of an appropriate orbit, or the existence of a common boundary type, not a coordinate-free distinguished point of a moduli problem.

The manuscript mostly says “explicitly constructed common point,” which is defensible. Phrases such as “canonical operation,” “intrinsic boundary point,” or “universal point” should be used with much greater discipline unless an actual universal property or choice-independent orbit is proved.

### 5.3 The theorem destroys rather than organizes pencil invariants

Every `Z_R` contains the same point. Consequently this point cannot distinguish regular from singular pencils, Segre data, discriminant type, stabilizer, or any of the moduli recovered by the finite algebra. The result shows that the larger boundary is nontrivially reached, but it does not explain **which** boundary types correspond to **which** pencil degenerations.

The v151 report asked for a relation of the form
\[
\text{pencil degeneration type}
\longleftrightarrow
\text{normalization/collision type}.
\]
V152 proves instead that all types share one extreme degeneration. This is a literal response to the request for integration, but it is much weaker as geometry.

### 5.4 There is no geometry of `Z_R`

The paper does not determine the dimension, irreducible components, normalization, singularities, generic boundary, or orbit poset of `Z_R`. It does not compare `Z_R` and `Z_{R'}` for inequivalent pencils, describe their intersection beyond one point, or show whether `K_\infty` is generic in any natural component. It does not identify the intersection of all orbit closures or prove that the constructed orbit is the unique common closed orbit in the larger relation Grassmannian.

Without such information, Theorem 10.1 is an elegant degeneration lemma, not a compactification theorem.

### 5.5 The flatness argument should be made scheme-theoretically explicit

The proof says that a matrix with constant fibre rank has locally split image over the affine line. Here the relevant conclusion is true, but the manuscript should display a nonvanishing maximal minor near every point, or invoke the precise constant-rank criterion for a map of vector bundles. This is especially important because the adapted columns were divided by different powers of `\tau`.

Similarly, the statement that every nonzero fibre is the flag failure algebra should explicitly note that the diagonal rescaling of an adapted relation basis leaves the relation subspace unchanged for `\tau\neq0`.

### 5.6 The flag-jet lemma needs a clearer representation-theoretic anchor

For `n\ge4`, one quartic coordinate proves that order four occurs, and the affine flag formula proves that no coordinate has degree above four. To conclude that no nonzero linear combination has higher vanishing order, the proof invokes linear independence of the coefficient functions. The underlying reason is that the orbit of the highest-weight vector spans the irreducible representation. This should be cited to a precise earlier lemma or stated directly. As written, “the coordinates are linearly independent by the coefficient-span statement” is too compressed for the hinge of the all-dimensional theorem.

---

## 6. The pure-power normalization fibre

Proposition 10.3 is a useful strengthening. It gives the full Artin fibre, not only its tangent space, through the reciprocal recurrence
\[
c_j=-\sum_{i=1}^kq_ic_{j-i}
\]
and the equations
\[
c_{g+1}=\cdots=c_{g+k}=0.
\]
The cancellation of a residual member coprime to `a` over local Artin bases is the right mechanism. The tangent dimension
\[
\dim \operatorname{Sym}^k(E)-1
\]
follows because the defining equations have no linear terms when `g\ge k`.

A sentence near the end of the proof is grammatically and mathematically misleading. It says, immediately after discussing the equations, “Their number is
\(
\sum_{i=1}^k\dim\operatorname{Sym}^iW
\).” This is the number of coefficient **variables** in the `q_i`, not the number of scalar equations in the coefficients of `c_{g+1},\ldots,c_{g+k}`. The sentence must be corrected.

More importantly for significance, the proposition stops at a presentation and embedding dimension. It does not compute the fibre length, Hilbert function, socle, Gorenstein property, complete-intersection status, irreducible decomposition of its tangent cone, or asymptotics in `g,k,e`. In the dimension-three example, “embedding dimension forty-four” sounds dramatic, but an embedding dimension alone is not a geometric classification.

A top-four version of this result would need to extract a structural invariant or a uniform theorem from the reciprocal ideal, not merely write down its generators.

---

## 7. The new results remain local slices, not a global singularity theory

The central geometric object `Y_g` now has:

- a smooth normalization;
- an exact pointwise normality criterion;
- full normalization-fibre equations;
- one split two-branch local model;
- one binary double-root collision model;
- a reduced formula for pairwise divisor-degree intersections;
- one extreme pure-power ramification fibre.

This is a respectable package. It is not yet a classification of the singularities of `Y_g`.

The missing cases are not peripheral. They include:

- more than two degree-`g` divisors;
- overlapping divisors with nontrivial common part;
- residual gcds;
- simultaneous split and ramified choices;
- higher root collisions;
- multivariate collisions not reducible to a binary root chart;
- intersections of three or more degree images;
- closure relations among all these loci;
- generic singularities of each component of the nonnormal locus;
- global conductor and branch subschemes;
- Serre, Du Bois, rational, seminormal, or related singularity properties;
- canonical or intersection-theoretic data;
- a resolution or semiresolution with geometric consequences.

Theorems 8.1 and 8.3 are excellent test cases for such a theory. They are not the theory itself.

The manuscript should either prove a global theorem that organizes these cases or narrow its rhetoric and submit the local models as a specialist contribution.

---

## 8. The top-four originality problem remains unresolved

### 8.1 The Ballico 1993 comparison is still open

The authors are commendably explicit that they did not obtain the full theorem/proof text of Ballico's 1993 paper and do not make a negative anticipation claim. That is the correct scholarly posture.

It is also incompatible with asking a top-four referee to certify exceptional originality for a broad “failure scheme to intrinsic reconstruction” program. The closest named predecessor remains known only from metadata and an opening page. The six comparison axes requested in the prior reports therefore remain unresolved on that source:

- precise failure object;
- retention of nonreduced structure;
- infinitesimal order;
- family and base hypotheses;
- forgotten markings;
- inverse or reconstruction conclusions.

A publisher-access failure is not evidence of anticipation, but neither is it evidence of novelty. For a specialist venue, the authors can state the limitation and proceed. For a top-four originality case, this remains a serious block.

### 8.2 The new literature section is bounded, not exhaustive

The comparisons with coincident-root loci, tuple common-factor strata, conductor squares, rigidification, and regular pencils are useful. They demonstrate awareness of several adjacent theories and correct earlier overstatement.

They do not yet establish that the particular generalized pinch models, conductor powers, divisor-incidence intersections, or reciprocal-fibre ideals are unknown in the broader literature on factorization schemes, subspace varieties, resultants/subresultants, multiple-point schemes, finite birational images, and orbit closures of representations. The manuscript itself labels the audit bounded. A bounded audit is not enough to support an exceptional priority claim.

### 8.3 The main inverse invariant remains highly engineered

The inherited headline is striking: an unmarked, ungraded finite local algebra at a sharp order recovers every quadratic pencil. The paper has done serious work to show that coordinate changes, nonlinear automorphisms, tensor-factor ambiguity, and moving bundles do not destroy the encoded coefficient line.

Nevertheless, the failure algebra is intentionally constructed so that its first nontrivial relation contains the pencil data. The achievement is proving that the encoding remains intrinsic after forgetting all markings. This is genuine mathematics. It is not yet the discovery that a standard, independently central invariant unexpectedly has Torelli power.

The new boundary sections improve this situation by giving the relation space independent geometry. But until that geometry solves a recognized global problem or produces a natural compactification/classification theorem, the paper still feels built around a faithful encoding whose complexity is justified internally rather than by an external mathematical necessity.

---

## 9. Architecture and exposition

The source/provenance discipline is unusually strong. The build receipt, source hashes, preservation checks, theorem locator, and distinction between computation and proof are all exemplary research-engineering practices.

They should remain invisible to the significance argument.

The principal article now contains too many partially independent narratives:

1. sharp finite reconstruction of pencils;
2. a one-point local-algebra inverse;
3. moving-family and source-bundle recovery;
4. general Schur-coefficient reconstruction;
5. exact image recognition and nonlinear stabilizers;
6. covering-map reconstruction;
7. stack rigidification;
8. common-divisor normalization;
9. conductor and collision singularities;
10. a universal relation-orbit degeneration;
11. spectral specializations and fixed strata.

The introduction tries to summarize all of them and repeatedly explains what is not being claimed. This is evidence that the article has exceeded a coherent narrative scale.

I strongly recommend splitting the project. One paper could focus on the sharp unmarked reconstruction theorem and its relative/local variants. A second could develop the common-divisor image, conductor, collision singularities, and orbit-boundary geometry. At present each program weakens the exposition of the other. The singularity theory appears halfway through an inverse-theorem paper, while the inverse theorem is repeatedly interrupted by stack and boundary infrastructure.

A top-four paper can be long, but its length should come from one deep theorem and its unavoidable proof, not from preserving every successful branch of a research pipeline in one submission.

---

## 10. Specific technical and expository corrections

These points should be addressed even for a specialist submission.

1. **Formal branch lemma.** State a precise lemma converting cotangent surjectivity into a closed immersion of completed source germs into the completed scheme-theoretic image.

2. **Completed-image fibre product.** Prove in one place that the completed image is reduced and equals the fibre product of the two completed branch images over their Artin-functor intersection.

3. **Separated normalization germs.** Explain why the two marked divisor lifts remain in disjoint formal components over all local Artin bases.

4. **Numerical codimension.** Give a direct numerical or geometric explanation that `c\ge1` under the split theorem's hypotheses, rather than only an argument by contradiction after the branch picture has been asserted.

5. **Binary versality.** Formulate the Weierstrass/two-jet computation as an isomorphism of completed incidence functors and record its independence from the chosen frame and local root coordinate.

6. **General singular ideal.** Either compute the Jacobian-minor ideal of `A_m` in a structural closed form or temper the claim that the singular scheme has been “determined” for arbitrary `m`.

7. **Power divisor hypothesis.** In Proposition 9.1, explicitly state that `a_0` is linear before claiming that all positive divisor degrees are `1,\ldots,m`.

8. **Reduced intersection rhetoric.** Consistently call Proposition 9.1 a reduced-support formula, not a scheme-theoretic intersection theorem.

9. **Orbit group distinction.** Every statement about `Z_R` should visibly say `GL(E)` first-relation orbit closure and contrast it with the `PGL(V)` congruence orbit of pencils.

10. **Choice dependence of `K_\infty`.** Replace “canonical point” language by a statement about a common orbit or explicitly prove choice independence at the appropriate level.

11. **Two-stage nature.** Keep prominent that a general pencil reaches `K_\infty` by two specializations, not by one uniform one-parameter subgroup. The current proof is honest about this; the introduction should be equally precise.

12. **Flat relation subbundle.** Exhibit the maximal-minor/constant-rank argument over `\mathbf A^1` after the basis vectors are divided by different powers of `\tau`.

13. **Flag coefficient span.** Cite the exact representation-theoretic result ensuring that no nonzero linear combination of the coefficient functions vanishes to order above four.

14. **Reciprocal-fibre wording.** Correct “their number” to “the number of coefficient variables” in Proposition 10.3.

15. **Pure-power invariants.** Compute at least basic invariants of the reciprocal ideal, or explain why the presentation itself is the intended endpoint.

16. **Abstract scope.** The abstract currently compresses the all-pencil inverse, moving families, two singularity models, a common orbit boundary, rigidification, transverse families, coverings, and spectral data into one paragraph. It should identify at most two principal theorem packages.

17. **Terminology.** Reserve “universal” for an actual universal property or make clear that it means only “common to every orbit closure.” Reserve “intrinsic” for choice-independent objects, not a construction after a standard flag and coordinate have been fixed.

18. **Literature status.** The Ballico limitation must remain in the submitted article, not only in repository audits, unless the comparison is completed.

19. **Computational evidence.** Do not cite passing scripts in support of theorem validity in the article. The repository can retain them for reproducibility.

20. **Submission decomposition.** Decide whether this is primarily an inverse theorem paper or a common-divisor singularity paper. The present compromise obscures both contributions.

---

## 11. Scorecard against the v151 minimum conditions

### 11.1 Complete the Ballico comparison

**Open.**

The authors document the access failure and avoid fabrication. The theorem-level comparison is still unavailable.

### 11.2 Add a real factorization-locus literature section

**Substantially improved, but bounded.**

The paper now discusses several primary sources with theorem-level distinctions. This closes the most obvious omission, but not a top-four priority audit.

### 11.3 Deepen the geometry of `Y_g`

**Partially and materially addressed.**

The split and binary-collision models are real structural results. They compute conductors, depth, and Cohen–Macaulayness on stated strata. They do not supply a global conductor, singularity stratification, or resolution.

### 11.4 Integrate the boundary with actual pencil degenerations

**Literally addressed, conceptually incomplete.**

The common point `K_\infty` lies in every first-relation orbit closure and comes from a finite-flat failure-algebra family. This is genuine integration. It does not relate distinct pencil degeneration types to distinct boundary types and therefore does not organize the pencil geometry.

### 11.5 Classify orbit closures or replace the closed-orbit theorem as the main payoff

**Not closed at top-four scale.**

The new common ramified point replaces the elementary closed flag orbit as the principal degeneration result, but no nontrivial part of the orbit-closure poset or geometry of `Z_R` is classified.

### 11.6 Compress standard infrastructure

**Improved in ordering, not solved in architecture.**

The new geometry appears earlier and AOV is cited. The article remains overloaded with standard and project-specific infrastructure.

---

## 12. Conditions for any further top-four evaluation

I would not recommend another top-four review round triggered by more finite checks, another isolated collision example, a larger explicit fibre, or another formal refinement of the rigidification stack.

A serious new round should contain at least one theorem of unmistakably global scale. Examples include:

- a complete conductor and branch stratification of `Y_g` on a natural large class, with closure relations and local normal forms;
- a canonical semiresolution or resolution with consequences for singularity type, canonical class, intersection theory, or topology;
- a scheme-theoretic divisor-poset intersection theorem, not only a reduced support formula;
- a classification of a substantial part of the `GL(E)` orbit-boundary poset for pencil first relations;
- a theorem recovering or predicting Segre/pencil degeneration data from boundary collision type;
- a natural compactification of the effective pencil-failure moduli problem on which the failure functor extends and whose boundary has geometric meaning;
- a structural theorem about the reciprocal-fibre algebras, beyond their presentation and tangent dimension.

The historical comparison with Ballico 1993 must also be completed through a legitimate source, or the paper must abandon any broad priority implication for the failure-locus program. Finally, the submission should be reorganized around one principal theorem package rather than preserving the whole pipeline in one article.

---

## 13. Final assessment

Revision 152 deserves substantial credit. The authors responded to the strongest mathematical objections in v151 with actual theorems. The split-conductor calculation and generalized pinch model are meaningful commutative algebra. The common orbit-boundary theorem genuinely links the divisor collision geometry to failure algebras. The pure-power fibre presentation is exact rather than heuristic. The literature and scope statements are more responsible.

I therefore reject any description of v152 as mere proof engineering, metadata, or cosmetic revision. It contains new mathematics.

I also do not think that the manuscript has reached the threshold of *Annals*, *Acta*, *Inventiones*, or *JAMS*. The new singularity results are local slices of a much larger boundary. The orbit theorem supplies one common information-destroying degeneration under a very large coordinate-change group, not a boundary classification or compactification of pencils. The closest named historical comparison remains incomplete. The inherited inverse is technically impressive but still organized around a deliberately information-bearing failure algebra. The article's breadth now works against conceptual inevitability.

The appropriate editorial decision at the stated level is therefore:

**Reject in the present form for a top-four general mathematics journal.**

I would regard the paper, after major restructuring and completion of the literature comparison, as a credible candidate for a strong specialist venue. A future top-four case would require a new global structural theorem, not another incremental closure of the current issue matrix.
