# Independent harsh referee report — A2 revision 151

## Manuscript and review object

**Manuscript:** *Finite failure schemes and the reconstruction of quadratic pencils*  
**Author:** Qian Qi  
**Revision reviewed:** A2 revision 151  
**Revision branch:** revision/a2-v151-canonical-gcd-boundary-normalization-2026-09-24  
**Source-bound mathematical commit:** e68458a9abba44759177e6fbc5fef75622719b53  
**Controlling prior review:** review/a2-v149-independent-harsh-top4-2026-09-24  
**Controlling prior review tip:** ddcef32b3cf491aacb293e466c393ec4af3caecd  
**Principal review object:** papers/A2-v17-boundary-information-coarsening/article/v151/geometry.pdf, 62 pages in the build receipt  
**Separate applications manuscript:** applications.pdf  
**Non-submitted historical archive:** archive-v144.pdf  
**Review standard:** the proof-completeness, originality, conceptual depth, inevitability, and exposition standard expected at Annals of Mathematics, Acta Mathematica, Inventiones Mathematicae, or Journal of the AMS.

This is an owner-requested independent-referee-style report, not a journal-commissioned editorial decision. I reviewed the v151 principal source, the new canonical-divisor-boundary section, the rigidification section, the common closed pencil specialization, the response to the v149 report, the issue matrix, proof-scope audit, source lock, theorem locator, build receipt, the relative first-relation proposition inherited from v149, and the controlling v149 referee report. I also checked the current bibliography against adjacent factorization/coincident-root literature and rechecked the status of the Ballico 1993 citation. The 27 regression scripts and the new exact finite witnesses are treated as finite consistency checks, never as substitutes for universal proofs.

The branch tip contains a post-source materialization commit adding receipts, PDFs, logs, and provenance artifacts; the source lock binds the mathematical source to e68458a9abba44759177e6fbc5fef75622719b53. I found no later mathematical-source change in that materialization step.

## Recommendation

**Reject in the present form for a top-four general mathematics journal.**

This recommendation is materially different in basis from my v149 recommendation.

Revision 151 has solved a substantial part of the mathematical problem I previously asked the authors to solve. The new degree-prescribed common-divisor incidence is an independently defined scheme-theoretic object, not a reduced structure selected after the fact and not a pencil image cut out by Cauchy and Pluecker equations. The multiplication map from the divisor-incidence space is finite; the manuscript gives explicit equations for its full, possibly nonreduced fibres; it proves that the source is the normalization of the image; and it gives an exact pointwise normality/smoothness criterion. This is genuine new geometry relative to v149. The revised paper also gives a clean universal-property formulation of the two rigidifications and an explicit one-parameter degeneration of every quadratic pencil to a common closed flag orbit.

I do **not** find a new fatal counterexample to Theorem 7.4, the fibre equations, Theorem 15.1, or Theorem 16.1. The core new proofs are substantially more convincing than the reduced-stratum construction in v149.

The remaining negative recommendation is therefore not a disguised correctness objection.

It is a top-four originality/significance objection, sharpened by a literature-positioning problem. The strongest new theorem is broad in parameters but elementary in mechanism: once the multiplication incidence is written down, the normalization result is driven by unique factorization, projectivity plus finite fibres, an explicit multiplication-matrix elimination, and finite-local Nakayama. This is elegant and useful, but the manuscript does not yet place it against the established geometry of factorization loci, coincident-root loci, common-factor/base-point strata, or related singularity calculations. The bibliography for the new boundary theorem consists essentially of Stacks Project infrastructure. In particular, the paper does not discuss the classical and modern coincident-root literature where normalization, local equations, singular loci, and smoothness criteria are already central themes, even though that literature is not identical to the present higher-rank multivariate incidence problem.

At the same time, the closest named failure-locus predecessor, Ballico 1993, remains unread at theorem/proof level. The paper correctly says so. That honesty is preferable to fabricating a priority claim, but a top-four referee cannot certify an exceptional originality claim while both the closest named predecessor and a visibly adjacent factorization/singularity literature remain insufficiently compared.

Thus v151 is a real mathematical advance over v149. It is also, in my view, still short of the level at which a general top-four journal should take responsibility for the originality and breadth claims.

---

## 1. What v151 actually fixes

The v149 report asked for four kinds of strengthening beyond preservation of the existing inverse theory.

### 1.1 A natural scheme structure beyond the reduced exact-gcd locus

This is now substantially addressed.

Section 7 defines the degree-\(g\) divisor incidence on arbitrary complex schemes by a line subbundle
\[
\mathcal L\subset S_g\otimes\mathcal O_T
\]
and a rank-\(r\) relation subbundle
\[
\mathcal K\subset S_D\otimes\mathcal O_T
\]
with the actual bundle-map equation
\[
\mathcal K\to (S_D\otimes\mathcal O_T)/(\mathcal L S_h)=0.
\]
The scheme-theoretic image \(Y_g\) of the multiplication morphism is then canonical.

This is much better than declaring the exact-gcd set reduced and proving that a chosen parameter space maps isomorphically to it. The nonreduced structure at divisor collisions is now part of the geometry being studied.

### 1.2 A theorem describing the boundary rather than only exhibiting transverse directions

This is also substantially addressed.

Theorem 7.4 computes the normalization and gives an exact normal locus. Lemma 7.3 gives full fibre equations, not merely tangent dimensions. The length-three fibre
\[
\operatorname{Spec}\mathbf C[a,b]/(a,b)^2
\]
at \(\langle x^2y,x^2z\rangle\) is exactly the sort of scheme-theoretic phenomenon that v149 had not captured.

### 1.3 A canonical universal property for the quotient operations

This is essentially addressed.

Theorem 15.1 formulates the first-relation map as an fppf gerbe with explicitly identified relative inertia and states the expected universal property for functors killing that inertia. Corollary 15.2 does the same for the right-factor kernel on the pencil side and correctly notes that the descended subgroup need not be a constant group scheme on the base.

The paper is no longer merely “quotienting arrows by convention.”

### 1.4 A non-formal pencil-side consequence

This is addressed literally, although not at a top-four level of depth.

Theorem 16.1 constructs an explicit degeneration of every pencil to the flag pencil \(\langle x_1^2,x_1x_2\rangle\) and proves that its orbit is the unique closed orbit. Corollary 16.2 lifts the degeneration to a finite-flat family of failure algebras.

This is not merely restriction of the effective-stack equivalence to a pre-existing invariant locus. It is an actual orbit-closure statement.

The v151 response therefore deserves credit: the authors did not answer the previous report with cosmetic prose, a larger experiment table, or a renamed version of the same quotient.

---

## 2. Correctness audit of the canonical divisor incidence

Proposition 7.1 is, in my reading, correct.

The key point is that multiplication by a nonzero homogeneous polynomial
\[
S_h\longrightarrow S_D
\]
is injective on every geometric fibre. Hence the tautological multiplication map over \(\mathbf P(S_g)\) has constant rank \(s_h\). Locally a nonzero maximal minor splits it, so its image and cokernel are vector bundles. A rank-\(r\) subbundle contained in that image is therefore the same thing as a rank-\(r\) subbundle of \(S_h\) after tensoring by the divisor line. This gives
\[
\mathscr X_g\simeq \mathbf P(S_g)\times \operatorname{Gr}(r,S_h)
\]
with its full functorial scheme structure.

The finiteness argument is also sound. The source is projective. Over an algebraically closed field a geometric fibre consists of degree-\(g\) divisors of the fixed polynomial \(\gcd(K)\), up to scalar. A polynomial has only finitely many such divisors. Proper plus finite fibres gives a finite morphism.

The integrality of the scheme-theoretic image is not being imposed. On an affine open meeting the image, the coordinate ring of the scheme-theoretic image injects into the coordinate ring of its finite inverse image, which is a domain because the source is integral. Thus \(Y_g\) is integral.

I also agree with the manuscript's scope correction: in several variables, “possesses a divisor of degree \(g\)” is not equivalent to “gcd degree at least \(g\).” This distinction is important and is now stated prominently enough.

I found no correctness blocker here.

---

## 3. The exact fibre equations are a genuine improvement

Lemma 7.3 is one of the strongest pieces of v151.

On a multiplication-minor chart, the quotient coefficients are forced by an invertible \(s_h\times s_h\) block \(M_{A_0}(f(u))\). The complementary equations
\[
C_{B_0}-M_{B_0}(f(u))M_{A_0}(f(u))^{-1}C_{A_0}=0
\]
therefore describe the entire scheme fibre, without taking a radical.

This point matters. In v149 the discussion of gcd strata could still be read mainly on geometric points plus tangent spaces. V151 now records higher nilpotents and can distinguish:

- one reduced divisor lift;
- several reduced divisor lifts;
- one geometric lift with a ramified/nonreduced fibre.

The tangent-kernel formula is also convincing. If \(K=fJ\), \(H=\gcd(J)\), and \(c=\gcd(f,H)\), then the condition
\[
f\mid \dot f\,j\quad\text{for all }j\in J
\]
is equivalent valuation-by-valuation to \(f\mid \dot f\,H\). Writing \(f=cf_1\), \(H=cH_1\), with \(\gcd(f_1,H_1)=1\), forces
\[
\dot f=f_1 w,\qquad w\in S_{\deg c}.
\]
Modding out the projective scalar direction gives
\[
S_{\deg c}/\mathbf Cc.
\]

The exact scripts check representative instances of this formula and the length-three example, but the proof itself is algebraic and does not depend on those scripts.

Again, I do not find a fatal defect.

---

## 4. The normalization theorem is correct-looking, but its mechanism must be assessed at the right scale

Theorem 7.4 is the main new theorem of the revision.

The proof that \(\nu_g\) is birational uses the dense open where the residual subspace is gcd-free. On that open the full gcd has degree exactly \(g\), so there is one degree-\(g\) divisor, namely the gcd itself. Lemma 7.3 gives zero fibre tangent space.

The local Nakayama step is worth checking carefully, because it is doing real work.

Let \(A\) be the local ring of \(Y_g\) and \(B\) the finite algebra of the inverse image. Since the fibre is a single reduced point,
\[
B/\mathfrak m_A B\simeq \mathbf C,
\]
and the image of \(A\) already supplies that copy of \(\mathbf C\). Hence
\[
(B/A)/\mathfrak m_A(B/A)=0.
\]
Nakayama gives \(B=A\). This is stronger than set-theoretic injectivity and is exactly what is needed.

Since the source is smooth and integral, finite birationality makes it the normalization.

The same argument yields the pointwise normality criterion. A normal point forces the normalization to be locally an isomorphism, hence one reduced point in the normalization fibre. Conversely, a unique divisor with zero overlap makes the entire fibre a single reduced point, so the same finite-local argument makes the normalization an isomorphism near that point.

The additional statement “normal if and only if smooth” is also justified **in this specific situation**: if \(Y_g\) is normal at the point, the normalization is locally an isomorphism there, and the normalization source is smooth. The manuscript does not make the false general claim that normal varieties are smooth.

I therefore regard the theorem as mathematically credible.

But the top-four significance question is different.

Once the incidence has been chosen, the proof is built from:

1. unique factorization of polynomials;
2. constant-rank multiplication;
3. projectivity and finite fibres;
4. explicit block elimination;
5. a valuation computation;
6. Nakayama's lemma.

There is elegance in the fact that these elementary ingredients produce a uniform theorem for all \(e,g,h,r\). There is not yet a commensurate structural payoff. The paper does not determine the conductor, the scheme-theoretic singular locus, branch intersection multiplicities, local analytic types beyond selected fibres, Cohen–Macaulayness, rational singularities, canonical class, or a stratified resolution. Nor does it identify \(Y_g\) with a previously important compactification whose geometry was unknown.

A theorem can of course be top-four-worthy with an elementary proof. But in that case the statement usually has to solve a problem of unmistakable prior importance or reveal a principle whose reach is much broader than the construction that proves it. The present manuscript has not yet made that case.

---

## 5. The examples are correct and well chosen, but they do not substitute for a singularity theory

The example
\[
K=\langle x^2y,x^2z\rangle
\]
with \(g=1\) is useful. In the chart \(f=x+ay+bz\), substitution produces the ideal
\[
(a^2,ab,b^2),
\]
giving a length-three fibre with two-dimensional tangent space.

Likewise, \(xy\langle x,z\rangle\) gives two reduced divisor lifts, whereas
\[
x(x^2+yz)\langle y,z\rangle
\]
has a higher gcd degree but one transverse divisor lift and is normal.

These examples demonstrate that three naive proxies fail:

- gcd degree alone;
- number of geometric divisor choices alone;
- tangent dimension alone without the full fibre.

This is good exposition.

For a top-four paper, however, the next step should be a theorem organizing these examples into a stratified singularity picture. At present the examples illustrate the criterion rather than exposing a new hierarchy of singularities.

---

## 6. The first-relation algebra boundary is legitimate, but its scope is narrower than the abstract rhetoric can suggest

Corollary 7.8 transports the common-divisor boundary to the maximal-lower-Hilbert-function first-relation algebra stratum.

The inherited Proposition 6.4 is important here. Under the stated trace, nilpotence, local-freeness, and associated-graded hypotheses, a local splitting of
\[
\mathcal N\to\mathcal N/\mathcal N^2
\]
gives a surjection from the truncated symmetric algebra. A relation with a nonzero term of least degree \(<D\) would contradict the assumed associated-graded isomorphisms. Since the truncation stops at degree \(D\), the kernel is exactly the degree-\(D\) relation bundle. This justifies the local homogeneous presentation used by the v151 rigidification theorem.

Thus I do not object to the algebra-stack statement on its stated stratum.

The limitation is substantial, however. This is not a moduli theorem for arbitrary finite-flat local algebras or arbitrary smoothings of the failure algebra. The Hilbert-function stratum is deliberately chosen so that the first relation is the only relation before truncation. The paper says this correctly in the proof-scope audit and in the corollary.

The abstract phrase “a canonical boundary for the first-relation algebra stack” should therefore always be read with this stratum condition attached. I would prefer it to be attached even more explicitly in the abstract or first-page summary.

---

## 7. The rigidification theorem repairs the categorical presentation, but it is not a new source of top-four novelty

Theorem 15.1 is a good cleanup of a real issue in v149.

The relative inertia is identified as the substitution group inducing the identity on \(\mathcal N/\mathcal N^2\). Its underlying local scheme is \(\operatorname{Hom}(\mathcal E,\mathcal N^2)\), but the manuscript correctly refuses to replace the actual substitution law by addition. Normality follows intrinsically from being the kernel of the map to the linear first-relation automorphism group.

The descent proof of the universal property is also the right argument: local lifts differ by the killed inertia; the triple-overlap failure lies in the same inertia; hence a functor killing that inertia acquires honest descent data. Natural transformations descend as well.

Corollary 15.2 similarly identifies the right-factor subgroup as a conjugation-associated \(\operatorname{GL}(U)\)-bundle over a torsor, rather than pretending it is globally constant.

I do not see a serious correctness objection.

But this is standard rigidification technology applied carefully to the present stack. The paper itself acknowledges this and cites the Stacks Project guide. At final-submission level I would strongly prefer a primary citation to the appropriate rigidification literature, with the manuscript proving only the particular identification of its subgroup stack and the hypotheses needed here.

The universal property is valuable because it prevents an overstatement. It should not be counted as one of the principal originality pillars.

---

## 8. The common closed pencil orbit theorem is believable and useful, but elementary

Theorem 16.1 says every quadratic pencil degenerates to
\[
\langle x_1^2,x_1x_2\rangle
\]
and that the orbit of these flag pencils is the unique closed \(\operatorname{PGL}(V)\)-orbit in
\[
\operatorname{Gr}(2,\operatorname{Sym}^2V).
\]

The explicit proof is convincing.

For independent quadrics \(q_0,q_1\), the rational function \(q_1/q_0\) is nonconstant. In characteristic zero its differential is nonzero somewhere on the open set where \(q_0\neq0\). After subtracting a scalar multiple of \(q_0\) from \(q_1\), one gets coordinates with nonzero \(x_1^2\) coefficient in \(q_0\), zero \(x_1^2\) coefficient in \(q_1\), and nonzero \(x_1x_2\) coefficient in \(q_1\).

The one-parameter subgroup with weights \(0,1,2,\ldots,2\) then gives polynomial rescaled generators and the required limit. Independence survives at \(t=0\), so the family really defines a subbundle over the whole affine line.

The identification of the limiting orbit with \(\operatorname{Fl}(1,2;V)\) is also natural: one recovers the line \(\ell\) as the common factor and the plane \(H\) after division.

This theorem supplies the non-formal pencil-side consequence requested in v149.

But it is not deep enough to carry the top-four significance case. Conceptually it is a highest-weight degeneration inside the projectivization of \(\bigwedge^2\operatorname{Sym}^2V\), and the manuscript itself calls the mechanism elementary projective representation theory. The theorem should be compared with the standard representation-theoretic description of closed orbits in projective irreducible representations, and with the existing orbit/stratification literature on pencils of quadrics.

The failure-algebra lift in Corollary 16.2 is a legitimate consequence of the exact-multiplicity construction. It shows compatibility of the inverse apparatus with a concrete degeneration. It does not classify orbit-closure adjacency among quadratic pencils, and the manuscript correctly disclaims such a classification.

---

## 9. The paper has finally crossed the v149 conceptual boundary, but the new boundary theorem is not yet integrated with the pencil boundary geometry

This is, to me, the most important structural criticism after the literature problem.

The new \(Y_g\) is a large, natural space of arbitrary degree-\(g\) divisorial first relations. That is good.

The pencil relation locus is a much smaller locus obtained by additional determinant, Cauchy, factor-rank, and Pluecker conditions.

The paper now has two distinct geometric stories:

1. a general divisor-incidence normalization theorem for arbitrary relation spaces;
2. a highly structured inverse theorem for quadratic pencils.

What is still missing is a theorem showing that the singularity theory of the first story controls a genuinely natural compactification or boundary problem in the second story.

Every pencil lies in the exact-gcd open of the canonical divisor boundary. But the paper does not classify which components or strata of \(Y_g\setminus U_g\) are actually reached by natural degenerations of pencil failure relations, which divisor collisions correspond to Segre-symbol degenerations, or how the normalization branches encode orbit-closure adjacency of pencils.

Theorem 16.1 gives one common degeneration, but it stays inside the exact pencil locus and keeps the exact divisor \(\delta^{n-1}\). It therefore does not use the genuinely singular part of \(Y_g\).

This leaves the new boundary theorem and the old pencil inverse standing beside each other rather than fusing into a single organizing theorem.

For a specialized paper this is entirely acceptable. For a top-four general journal, this missing integration is costly. The strongest new general theorem does not yet solve the strongest natural boundary problem of the motivating class.

---

## 10. The Ballico 1993 comparison remains open and cannot be waved away at this level

The manuscript identifies the following predecessor:

E. Ballico, “On the Failure Locus of Higher Order Properties of Embeddings in Projective Spaces,” *Mathematische Nachrichten* 163 (1993), 5–13, DOI 10.1002/mana.19931630102.

The v151 literature audit says the complete theorem/proof text was not obtained. The Wiley volume record confirms the article metadata and pages, but the current audit still does not supply the full theorem/proof text.

The manuscript is commendably explicit that it does not know whether Ballico anticipates any of the relevant mechanisms.

That is the correct scholarly response to incomplete access.

It is not enough for a top-four originality certification.

The six comparison axes previously requested remain unanswered on the Ballico side:

- exact failure object;
- retention of nonreduced structure;
- infinitesimal order;
- family/base hypotheses;
- forgotten markings;
- inverse/reconstruction conclusions.

This gap is now more consequential, not less, because v151 asks the reader to regard “failure scheme \(\to\) intrinsic relation \(\to\) reconstruction” as part of a broad conceptual package. A named paper explicitly about failure loci cannot remain at metadata level.

I would not reject an ordinary specialized paper solely because one old article was temporarily difficult to obtain. I would reject a top-four originality case that asks the referee to certify exceptional novelty while its closest named predecessor remains unexamined.

---

## 11. The literature audit for the new boundary theorem is too narrow

This is a new concern specific to v151.

The bibliography added for the common-divisor theorem cites general Stacks Project results on finiteness, scheme-theoretic image, normalization, and rigidification. Those are appropriate technical references. They are not a literature comparison for the geometric object being introduced.

At minimum, the authors should compare their theorem with the classical/modern literature on factorization and coincident-root loci.

Two obvious adjacent references are:

- J. V. Chipalkatti, “On equations defining Coincident Root loci,” *Journal of Algebra* 267 (2003), 246–271, DOI 10.1016/S0021-8693(03)00336-3.
- S. Kurmann, “Some remarks on equations defining coincident root loci,” *Journal of Algebra* 352 (2012), 223–231, DOI 10.1016/j.jalgebra.2011.10.045, arXiv:1108.4532.

Kurmann's abstract explicitly discusses the normalization of a coincident-root locus, local generators for the fibre product with its normalization, a singular-locus description, and a smoothness criterion.

These papers concern binary forms and prescribed root multiplicities, not the present space of \(r\)-planes of multivariate forms with a common factor. I am **not** claiming they anticipate Theorem 7.4.

That distinction is exactly why a comparison is necessary.

The present paper must explain what changes when one passes:

- from one binary form to an \(r\)-dimensional subspace of multivariate forms;
- from a prescribed root-partition/factorization type to a degree-prescribed common factor;
- from the classical factorization normalization to the Grassmannian incidence;
- from singular-locus statements there to the exact unique-divisor/coprime-residual criterion here.

There is also a broader literature on common-factor/base-point strata in compactifications of spaces of maps and on resultant/subresultant conditions. I do not require the authors to cite every computational-gcd paper. I do require them to demonstrate that they know where their \(Y_g\) sits in the existing geometry of factorization loci.

The current sentence that focused searches did not reveal an exact primary theorem is not an adequate top-four novelty analysis.

---

## 12. The existing pencils-of-quadrics literature still needs a sharper comparison for the new orbit statement

The manuscript already cites Fevola–Mandelshtam–Sturmfels, *Pencils of quadrics: old and new* (2021), which reviews classification by Segre symbols and studies strata in the Grassmannian.

V151's new closed-orbit theorem should be positioned explicitly against that classical stratification picture.

The paper should answer, at minimum:

1. How does the flag orbit \(\ell H\) appear in the Segre-symbol or singular-pencil classification?
2. Is uniqueness of this closed congruence orbit already implicit or explicit in the standard representation-theoretic/orbit literature?
3. What is genuinely new: the orbit theorem itself, the elementary proof, or only the lift to the failure-algebra family?
4. Which orbit-closure relations remain unclassified by the present theorem?

The current text is admirably cautious in not calling the highest-weight specialization a new classification. That caution should be backed by an actual reference comparison.

---

## 13. The strongest inherited inverse theorems remain impressive, but their role in the top-four case is still difficult to evaluate

I do not retract the positive correctness comments from the v149 report concerning the inherited all-pencil inverse, moving-family inverse, exact determinant multiplicity, coefficient-support asymmetry, and transverse families.

V151 preserves those results and the build receipt records preservation of the inherited mathematical blocks.

The central inverse statement remains striking in formulation:

an unmarked, ungraded finite algebra of a sharp truncation order recovers every complex quadratic pencil up to \(\operatorname{PGL}(V)\).

The moving version also claims recovery of a varying pencil, one constant left transformation, and the actual source bundle.

These are the claims with the greatest potential to justify a very strong journal.

But their significance is still mediated by two issues.

First, the failure algebra is a deliberately engineered high-order object whose first nontrivial relation is constructed to encode the pencil coefficient data. The paper has worked hard to show that the encoding survives forgetting coordinates, gradings, tensor factors, and nonlinear automorphisms. That is real mathematics. It is still different from discovering that a standard independently important invariant unexpectedly has Torelli power.

Second, the new v151 boundary theorem does not yet show that this inverse mechanism reorganizes a classical geometric problem outside the constructed failure-algebra framework.

A top-four paper needs the reader to feel that the theorem was mathematically inevitable once discovered, not merely that an elaborate invariant can be proved faithful after enough intrinsic reconstruction machinery.

V151 moves in the right direction, but has not fully crossed that line.

---

## 14. The source/provenance engineering is excellent and should remain secondary

The build receipt is unusually disciplined:

- 62-page principal article;
- 27 successful regression scripts;
- 40 new exact checks;
- resolved references and labels;
- no overfull boxes;
- source hashes;
- preservation checks for inherited mathematics;
- theorem locators;
- explicit separation of proof from finite computational evidence;
- explicit statement that historical priority is not certified.

This materially improves auditability.

It should not enter the mathematical significance calculus.

A top-four referee should be able to remove the entire provenance directory and reach essentially the same judgment from the manuscript and primary references.

The paper itself mostly understands this. I recommend keeping the infrastructure in the repository while making the submitted article even more ruthlessly theorem-centered.

---

## 15. Specific technical and expository points to address

### 15.1 Cite primary rigidification literature

The Stacks Project guide is useful, but a theorem whose title is “First-relation rigidification” should cite the primary source appropriate to normal, possibly noncentral subgroup rigidification. The manuscript can still give its direct proof.

### 15.2 Separate “normalization of the image” from “classification of the boundary”

Theorem 7.4 solves the former completely. It does not solve the latter. The introduction is already more careful than earlier revisions, but phrases such as “the divisorial boundary” can still sound classificatory. I would use “normalization and normal locus of the degree-\(g\) common-divisor image” more often.

### 15.3 Give the scheme-theoretic singular locus, if feasible

Since normality equals smoothness here, the theorem determines the **set** of singular points by the divisor-choice/overlap criterion. It would be valuable to state whether the manuscript determines the singular locus as a scheme, not only its support. This would connect more directly to the classical factorization-locus literature.

### 15.4 Clarify how divisor-degree strata intersect

A point may lie in several \(Y_a\) for different \(a\). The current examples show this phenomenon indirectly. A systematic description of inclusions/intersections among the \(Y_a\) would make the boundary geometry much more useful.

### 15.5 Explain the conductor/branch structure

The normalization fibre already separates multiple divisor choices from overlap ramification. The next natural invariant is the conductor. Even partial results would deepen the theorem significantly.

### 15.6 Do not count the rigidification theorem as an independent headline innovation

It is important infrastructure and corrects a conceptual weakness. It is standard stack technology once the subgroup is identified.

### 15.7 Do not count the unique closed orbit by itself as a major classification theorem

Its value in this paper is the compatible finite-flat failure-algebra specialization. The underlying orbit statement should be presented and cited at the appropriate classical/representation-theoretic scale.

### 15.8 Tighten the abstract's algebra-stack phrase

“Canonical boundary for the first-relation algebra stack” should explicitly signal the maximal-lower-Hilbert-function stratum, because outside it the relative first-relation proposition is not claimed.

---

## 16. What v151 closes from the v149 minimum conditions

For the record, I assess the previous conditions as follows.

### 16.1 Finish the Ballico 1993 comparison

**Not closed.**

The manuscript correctly leaves it documentary-open. This remains a serious originality obstacle at the requested journal level.

### 16.2 Replace the reduced exact-gcd stratum by an intrinsic moduli problem or justify universality

**Closed in a mathematically substantive sense.**

The incidence functor is intrinsic, represented over arbitrary bases, and its scheme-theoretic image carries real nonreduced boundary information. The full normalization fibre is computed locally without radicalizing.

This is the biggest improvement in v151.

### 16.3 Produce a non-formal geometric consequence on the pencil side

**Closed literally, but only modestly at the significance level.**

The common closed specialization is an actual orbit-closure theorem and is lifted to failure algebras. It is not formal restriction of the stack equivalence. It is nevertheless elementary and far short of an orbit-closure classification or compactification theorem.

### 16.4 Clarify the effective stack by a canonical universal property

**Closed.**

The two subgroup stacks and their universal properties are now described carefully, including the twisted right-factor group over torsors.

### 16.5 Preserve the v149 strengthening

**Closed by source comparison and build evidence.**

I found no retreat from the exact determinant multiplicity, nonreduced-base arguments, all-pencil singular case, moving bundle recovery, or transverse families.

### 16.6 Produce a top-four-scale independent geometric theorem

**Partially closed, but not enough.**

Theorem 7.4 is now genuinely independent of the pencil image and is the first revision in this sequence where I would call the new boundary theorem a standalone algebraic-geometric result.

I still do not think its present depth, literature positioning, or integration with the pencil problem reaches the general top-four threshold.

---

## 17. Minimum conditions for another top-four evaluation

I would not recommend another top-four review round triggered only by more examples, more exact scripts, or another formal refinement of the quotient stacks.

A serious next round should contain most of the following.

### 17.1 Complete the Ballico comparison

Obtain the full 1993 article through a legitimate institutional library, document-delivery service, interlibrary loan, or author/archive source and compare theorem by theorem.

Record exact theorem numbers, hypotheses, scheme structures, infinitesimal orders, relative statements, forgotten data, and inverse conclusions.

If it truly cannot be obtained after documented institutional efforts, say so and build the novelty case without any negative claim about what it does not contain.

### 17.2 Add a real factorization-locus literature section

Compare Theorem 7.4 with coincident-root/factorization-locus normalization and singularity results, at minimum explaining the relation to Chipalkatti 2003 and Kurmann 2012 and why the multivariate \(r\)-plane problem is different.

Also survey the common-factor/base-point and resultant/subresultant literature sufficiently to rule out an already standard normalization theorem in a different language.

### 17.3 Deepen the geometry of \(Y_g\)

A top-four-strength continuation would ideally prove at least one genuinely structural result beyond normalization and the set-theoretic normal locus, for example:

- the conductor and branch locus;
- the scheme-theoretic singular locus;
- local analytic or étale normal forms for divisor collisions;
- Cohen–Macaulay, rational, Du Bois, or related singularity properties;
- a stratification by divisor posets with closure and intersection formulas;
- a canonical resolution with geometric consequences;
- or intersection-theoretic invariants not formal from the product normalization.

The specific choice is less important than the presence of a theorem that reveals structure not already visible from the finite parametrization.

### 17.4 Integrate the common-divisor boundary with actual pencil degenerations

Determine which strata of \(Y_g\setminus U_g\) occur as limits of natural pencil failure relations when determinant geometry is allowed to degenerate, and relate them to standard pencil invariants such as Segre data or orbit closures.

A theorem of the form

“pencil degeneration type \(\leftrightarrow\) normalization-branch/collision type of the intrinsic first-relation boundary”

would be far more compelling than having the two theories adjacent.

### 17.5 Either classify orbit closures or stop using the closed-orbit theorem as the main pencil-side payoff

The unique closed orbit is a useful anchor. A real geometric advance would be a nontrivial portion of the orbit-closure poset, singularities of orbit closures, or a natural compactification on which the failure functor has a geometric meaning.

### 17.6 Compress standard infrastructure in the article

Keep the rigorous proof of the particular subgroup identifications, but cite standard rigidification technology and move generic categorical rehearsal out of the conceptual foreground.

The reader should see the genuinely new geometry before the proof-engineering infrastructure.

---

## 18. Final assessment

Revision 151 is the first A2 revision in this review sequence that materially answers the strongest mathematical criticism of v149.

The canonical common-divisor image \(Y_g\) is not a disguised pencil image. Its normalization theorem is real algebraic geometry. The full nonreduced fibre equations and exact normality criterion are useful. The two rigidifications now have a defensible universal meaning. The common flag degeneration is an honest pencil-side geometric statement rather than formal transport.

I therefore no longer accept the criticism that the manuscript has **only** engineered image recognition plus quotient bookkeeping.

That criticism would be obsolete for v151.

Nevertheless, I would still reject the paper in its present form for Annals, Acta, Inventiones, or JAMS.

The reason is that the new standalone theorem is not yet situated convincingly in the factorization/singularity literature, while the closest named failure-locus predecessor remains unread at theorem level. The theorem's proof is elegant but uses elementary incidence, UFD, finite-morphism, elimination, and Nakayama mechanisms, and the paper has not extracted from it a correspondingly deep singularity theory or a new natural compactification theorem. The pencil-side closed orbit is useful but elementary; the rigidifications are standard technology; and the deepest new boundary geometry has not yet been tied to a classification of natural degenerations of quadratic pencils.

This leaves a paper with substantial, credible mathematics and unusually strong internal auditability, but without the level of demonstrated novelty, structural depth, and integration that I would demand from a top-four general mathematics journal.

**Recommendation: reject in the present form for a top-four general mathematics journal.**

I would, however, regard v151 as a much more serious candidate for a strong specialist algebraic-geometry/commutative-algebra venue than v149, provided the literature comparison is completed and the central claims are positioned at their correct level.
