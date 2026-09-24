# Independent harsh referee report — A2 revision 147

## Manuscript and review object

**Manuscript:** *Finite failure schemes and the reconstruction of quadratic pencils*  
**Author:** Qian Qi  
**Revision reviewed:** A2 revision 147  
**Revision branch:** revision/a2-v147-intrinsic-family-descent-2026-09-24  
**Review branch:** review/a2-v147-independent-harsh-top4-2026-09-24  
**Source-bound mathematical commit recorded by the revision:** ee87f9979de6b6d40038daab9f8cf336fa0b3007  
**Immediate predecessor reviewed:** revision/a2-v146-referee-proof-completion-2026-09-24  
**Controlling v146 report:** reviews/a2-v146-independent-harsh-top4-2026-09-24/REFEREE_REPORT.md  
**Principal review object:** papers/A2-v17-boundary-information-coarsening/article/v147/geometry.pdf, 39 pages in the source-bound build receipt  
**Separate applications manuscript:** applications.pdf  
**Non-submitted historical archive:** archive-v144.pdf  
**Review standard:** external-referee-style assessment at the level of *Annals of Mathematics*, *Acta Mathematica*, *Inventiones Mathematicae*, or *Journal of the AMS*.

This is an owner-requested independent referee-style review, not a journal-commissioned editorial decision. I reviewed the principal v147 source, the two new structural sections, the response to the v146 report, the issue matrix, the source-bound build receipt, the literature audit, and the retained local/moving-pencil arguments. I treated the regression scripts as consistency checks, not as proof certificates.

## Recommendation

**Reject in the present form for a general top-four mathematics journal.**

This recommendation should not be misread as saying that v147 failed mathematically. On the contrary, revision 147 materially closes most of the proof-architecture objections in my v146 report. The new first-relation proposition is the right abstraction; the actual-factor descent lemma supplies the missing global bundle argument; the local automorphism statement is now honestly formulated at the affine group-scheme level; the determinant-preserver input has been isolated; and the new moving-coefficient theorem produces a genuinely global, unmarked reconstruction statement with a nontrivial separating example.

I did not find a new fatal counterexample to the principal all-pencil reconstruction chain, the ungraded local inverse, the actual source-bundle descent, or the new isotrivial-family example.

The reason I still recommend rejection at top-four level is different. The closest identified 1993 failure-locus predecessor remains unresolved at theorem/proof level by the manuscript's own audit, so the novelty boundary is still documentary-open. More importantly, the new general coefficient theorem, while useful and apparently correct, still reads as a reconstruction theorem for a deliberately encoded determinant-times-Cauchy class rather than as a structural theorem of sufficiently broad independent consequence. The q=1 isotrivial example demonstrates that the family theorem is not fibrewise tautology, but it does not yet transform the paper into a top-four contribution.

In short: v147 has largely moved the paper from “proof architecture not yet finished” to “mathematically coherent but significance/priority threshold still not cleared.”

---

## 1. What v147 genuinely fixes

The v146 report required seven substantive items before a fresh top-four evaluation:

1. isolate the general first-relation/truncation principle;
2. give an invariant proof of actual source-bundle descent;
3. clarify the category of the automorphism sequence;
4. isolate or precisely cite the determinant-cone linear-preserver theorem;
5. position the Artin-local formulation against inverse-system/canonical-grading literature;
6. close Ballico 1993 at theorem/proof level;
7. reframe the significance case around the moving/unmarked mechanism rather than theorem count.

Revision 147 completes items 1–5 to a meaningful degree. Item 6 is explicitly still open. Item 7 is improved but, in my view, not completed at top-four level.

That distinction matters. I would no longer reject this version for the same mathematical reasons as v146. The present rejection is principally about unresolved historical priority and the scale of the conceptual payoff.

---

## 2. The first-relation orbit proposition is the correct abstraction

Proposition prop:first-relation-orbit-v147 considers

A(K) = Sym(E) / ((K) + m^(d+1))

with K contained in Sym^d(E), and observes intrinsically that

E = n/n^2,

K = ker[ Sym^d(n/n^2) -> n^d ].

This is elementary but exactly the right elementary statement. The proof correctly uses the fact that changing one lift by n^2 moves a d-fold product into n^(d+1), which vanishes. It also correctly identifies all higher-order changes of generators with substitutions x -> a(x)+u(x), where u has order at least two.

This resolves an important conceptual problem in v146. The ungraded local theorem is no longer presented as though the truncation itself creates mysterious nonlinear rigidity. The truncation kills higher-order corrections; the genuinely nontrivial pencil statement is the orbit-rigidity assertion that the unrestricted GL(E)-orbit of K_R still determines the GL(V)-orbit of R.

That is a much more candid and mathematically useful formulation.

I also agree with the manuscript's distinction from Elias–Rossi. Their canonical-grading results remove lower-degree inverse-system terms in special Gorenstein classes. Here the algebra is already homogeneous, the relevant socle behaviour is different, and the issue is the orbit of a top-degree relation space. The revised inverse-system paragraph is appropriately modest and no longer overstates the novelty of “ungraded versus graded.”

---

## 3. The affine automorphism group-scheme formulation is now credible

Proposition prop:first-relation-group-v147 substantially improves the categorical precision.

Representing Aut(A(K)) as the closed subgroup of GL(A) cut out by f(1)=1 and f(xy)=f(x)f(y) is standard and sufficient. The normalized regular-trace identity

tr(M_z) = length(A) · epsilon(z)

is a clean way to recover the augmentation functorially after extension to an arbitrary commutative complex algebra. Because the base is a C-algebra, division by the length is harmless. This avoids the earlier confusion between an augmentation ideal and an absolute nilradical after scalar extension.

The kernel parametrization by Hom(E,n^2), together with the unitriangular realization, justifies the unipotent claim. The warning that the affine-space parametrization is not an additive group law is important and correct.

The pencil corollary then identifies the quotient with the left-right stabilizer modulo diagonal scalars. The argument that equality on complex points upgrades to equality of smooth closed subgroup schemes in characteristic zero is reasonable here: the relevant groups are smooth/reduced, and the image is a closed algebraic subgroup.

I would still prefer a reference for the final algebraic-group quotient/isomorphism step, but I do not regard this as a present correctness blocker.

---

## 4. The actual-factor descent lemma closes the most delicate v146 gap

Lemma lem:actual-factor-descent-v147 is the strongest proof-level improvement in this revision.

The v146 moving-family theorem claimed recovery of the actual right vector bundle, not merely its projectivization. That conclusion is delicate because projective-bundle isomorphisms permit line twists. V147 now uses the datum that actually exists: the normal-bundle isomorphism itself.

After a constant lift of the recovered left PGL transformation is removed, the bundle map

V tensor A_1 -> V tensor A_2

preserves every left ruling. Checking the rulings generated by basis vectors kills the off-diagonal blocks; checking v_i+v_j forces all diagonal blocks to agree. Reducedness of the base promotes fibrewise vanishing to vanishing of bundle morphisms. The resulting map commutes with End(V), and the commutant sheaf is exactly Hom(A_1,A_2).

This is the right argument. It produces a global section directly, rather than gluing projective local lifts and hoping a line twist disappears.

I do not presently see a hidden extra marking here. The actual normal map comes from the intrinsic conormal quotient n/n^2 of the unmarked finite scheme. The projective left factor is first recovered from the determinant cone, then shown constant because the reduced base is connected projective and PGL(V) is affine. Choosing one constant linear lift introduces only the expected common scalar ambiguity.

This part of the revision should be retained.

---

## 5. The determinant-preserver input is now stated at the right level

Lemma lem:linear-preserver-v147 isolates the exact square, invertible, complex-linear hypothesis needed by the paper.

The proof by iterating reduced singular loci from the determinant hypersurface to the rank-one cone is standard and adequate. The maximal linear spaces in the Segre cone give the two rulings, and the resulting automorphism is left-right or transpose-left-right. The reference to Marcus–Moyls is appropriate, and the manuscript no longer leaves this classification buried inside a later support-rank argument.

This was a real exposition weakness in v146 and is now fixed.

---

## 6. The general moving-coefficient theorem appears internally coherent

Theorem thm:general-moving-coefficients-v147 is the main new conceptual claim.

The setup is:

- a smooth connected projective complex base B;
- a constant left n-space V;
- a rank-n source bundle U;
- coefficient subbundles L_lambda inside S_lambda(V^*) tensor O_B;
- the degree-q residual module J_q given by the multiplicity-one Cauchy decomposition;
- a first relation bundle K = determinant · J_q in degree D=n+q;
- the finite truncation through order D.

The proof has a clear intrinsic sequence:

1. the nilradical recovers B and the conormal bundle;
2. multiplication recovers K;
3. the homogeneous ideal generated by K has radical equal to the determinant ideal;
4. successive singular loci recover the two matrix rulings;
5. support-rank asymmetry orients them;
6. projectivity makes the left projective transformation constant;
7. the actual normal map plus the commutant lemma recovers the right bundle without a line twist;
8. contraction in each Cauchy summand recovers the coefficient subbundle.

I checked the most obvious failure points.

The radical argument is valid under the stated hypotheses: away from det=0 the matrix is invertible, and any nonzero coefficient subspace produces at least one nonzero residual coefficient. Hence the common zero set of determinant times residual coefficients is exactly the determinant hypersurface. On affine charts over C, equality of closed points gives equality of radicals, and the determinant hypersurface is reduced over the smooth base.

The orientation argument also works. In a lambda-summand the residual coefficient space has factor-support ranks (r_lambda,m_lambda). A transposition exchanges them. Because at least one support satisfies 0<r_lambda<m_lambda, the transposed type cannot equal the prescribed target type in that summand.

The coefficient recovery after orientation is likewise natural: the right Schur factor is full, so contraction against its full dual leaves exactly L_lambda.

I therefore do not have a proof-level objection to the theorem as presently stated.

---

## 7. But this “general theorem” is still a sufficient reconstruction package, not a classification principle

This is where the top-four significance problem now concentrates.

The theorem assumes a highly structured class in which the unknown data are inserted directly as coefficient subbundles L_lambda inside multiplicity-one Cauchy summands and then multiplied by the determinant. Once the first relation K is intrinsically recovered, a large fraction of the inverse is forced by the way the input was encoded.

The genuinely nonformal parts are:

- recovering the matrix tensor factors from the determinant cone;
- orienting those factors from asymmetric coefficient supports;
- obtaining an actual bundle map rather than a projective bundle;
- forcing one constant left transformation over the whole projective base.

Those are good ideas. But the current theorem does not classify when a first-relation module determines its coefficient data. It gives one strong sufficient condition.

For a top-four paper I would expect a sharper structural result along at least one of the following lines:

- characterize the full normalizer/stabilizer of a general multiplicity-one coefficient system;
- give necessary and sufficient conditions for transpose or other accidental symmetries to destroy reconstruction;
- classify the ambiguity when every support is symmetric or full;
- formulate a moduli-level quotient in which the reconstruction theorem becomes an intrinsic statement about an open or stratified class of relation modules, rather than a theorem about one hand-built family of ideals.

The strict-support hypothesis is effective, but at present it is a convenient asymmetry certificate, not a structural classification of the inverse problem.

This is not a correctness complaint. It is a significance complaint.

---

## 8. The isotrivial rank-712 example is valid and useful, but it is not yet the decisive global consequence

Example ex:isotrivial-covers-v147 is a good addition.

For B=P^1, V=C^3, U=O^3, q=1 and a rank-one coefficient line, the two columns

(s^3,t^3,0)^t

and

(s^3+s t^2,t^3,0)^t

define two O(-3) subbundles. Their fibre algebras are all isomorphic because GL(V) is transitive on nonzero coefficient lines. The underlying nilradical graded vector bundles agree: the top quotient calculation gives O^489 plus O(3)^3 in both cases. Yet the total schemes are distinguished by the reconstructed maps z^3 and z^3+z, whose ramification partitions differ.

The ramification comparison is sound. z^3 has two points of index three. z^3+z has two finite simple critical points of index two and infinity of index three. Independent source and target projective transformations preserve those ramification data.

This example successfully proves that the global theorem contains information not visible in fibrewise algebra isomorphism classes or in the underlying graded vector bundles.

However, the example belongs to the q=1 general coefficient theorem, not to the quadratic-pencil theorem that gives the paper its title and main narrative. It is therefore an internal witness for the general mechanism rather than a new geometric consequence about pencils of quadrics.

For top-four significance I would want one of two stronger outcomes:

- a pencil-native pair of moving families whose fibres and natural graded bundle invariants agree but whose unmarked thickenings are separated only by the global reconstruction; or
- an independent geometric theorem about a natural moduli/family problem whose proof essentially uses the unmarked coefficient descent.

The present rank-712 example is mathematically legitimate but still feels engineered to demonstrate the theorem.

---

## 9. The all-pencil local theorem remains one of the strongest parts

Theorem thm:artin-local-inverse-v146 survives the v147 audit.

The point-local algebra has no relations below degree d. Therefore an ungraded algebra isomorphism recovers the tangent space and first degree-d relation kernel. Higher generator corrections disappear above the truncation. The homogeneous cone generated by K_R recovers the determinant geometry; coefficient-support ranks orient the factors; exterior duality recovers the pencil plane.

The statement continues to hold for singular pencils; I found no place where regularity is silently reintroduced.

The “smallest uniform order” formulation is also correct. Lower truncations are independent of R because the defining relations first occur in degree d. The integer d is therefore sharp uniformly.

I repeat one conceptual caution from v146: the numerical threshold is not, by itself, the source of depth. It is the degree of the deliberately constructed first relation. The substantive theorem is the orbit rigidity of K_R after all markings are forgotten.

V147 now says this much more clearly.

---

## 10. The closest identified failure-locus predecessor remains unresolved

This remains the most concrete external blocker.

The v147 literature audit records that for Ballico's 1993 paper

*On the Failure Locus of Higher Order Properties of Embeddings in Projective Spaces*, Math. Nachr. 163 (1993), 5–13,

the first page has been inspected, but pages 6–13 and the complete theorem/proof text have not been obtained. The manuscript accordingly leaves all theorem-level cells involving nonreduced structure, infinitesimal order, relative constructions, and inverse conclusions unresolved.

I independently rechecked the publicly accessible publisher record and issue listing on September 24, 2026. They verify the bibliographic data and expose a first-page/PDF entry, but I still did not obtain theorem/proof text sufficient to close the six-axis comparison.

This does not mean that Ballico 1993 anticipates the present inverse theorem. It means the opposite conclusion is also not yet justified.

For a specialized journal, an author can sometimes proceed with a carefully limited novelty claim while an obscure predecessor remains hard to access. For a top-four submission whose title and central object are explicitly a failure scheme, the closest named failure-locus predecessor cannot remain a question mark in the final novelty case.

The next version must obtain the complete article through a library, author contact, document-delivery service, or another legitimate route and compare actual theorem statements and proofs.

No amount of additional internal regression evidence substitutes for this.

---

## 11. The revised Artin-local literature positioning is much better

V147 now cites and discusses:

- Elias–Rossi on short Gorenstein local rings;
- Elias–Rossi on compressed local algebras;
- Marcus–Moyls on tensor-product/rank-one preservers;
- the characteristic-zero smoothness input for algebraic groups.

This is a substantial improvement over v146.

The paper now clearly says:

- it is not proving a general canonical-grading theorem;
- its algebras are not in the cited short Gorenstein classes;
- the inverse-system formula is classical;
- nonlinear higher-order changes form a universal kernel;
- the new problem is the special orbit rigidity of the determinantal coefficient relation.

That is the correct intellectual boundary.

I would nevertheless broaden the literature discussion around the new global theorem itself. Once the paper advertises “unmarked descent for moving coefficient spaces,” the relevant comparison is no longer only Artin inverse systems. The author should explain how this result sits relative to standard automorphisms of determinantal/Segre varieties, descent from projective bundles to vector bundles, and invariant-theoretic reconstruction from multiplicity-free or multiplicity-one modules. At present these ingredients are used correctly but are not synthesized into a convincing statement of what is conceptually new about their combination.

---

## 12. The publication object is now disciplined

The 39-page geometry.pdf is a credible principal object. The 10-page applications manuscript is separate. The 130-page historical archive is explicitly non-submitted.

I no longer have the publication-object objection that applied to much earlier versions.

The principal paper is still dense, but its internal structure is coherent:

- introduction;
- general first relations;
- tensor-ruling foundations;
- coefficient descent;
- fixed pencil inverse;
- finite neighbourhoods;
- curve and moving-family theorems;
- local inverse;
- spectral consequences.

The applications and archive should remain separate.

---

## 13. The computational/reproducibility layer is strong but does not change the referee standard

The v147 build receipt records twenty-four successful scripts, resolved references, unique labels, no overfull boxes, source preservation, and three native PDFs. This is unusually careful research engineering.

The manuscript itself correctly states that these checks do not prove:

- the universal geometric arguments;
- the global descent theorem;
- historical priority;
- top-four significance.

I agree with that limitation.

The code and receipts increase confidence that the intended finite examples and formulas are internally consistent. They do not replace proof or literature comparison.

---

## 14. What remains genuinely impressive

A harsh report should still identify what is working.

The paper now has a clean mathematical spine:

unmarked finite scheme  
→ intrinsic reduction and conormal bundle  
→ first relation space  
→ determinant cone  
→ tensor rulings  
→ orientation from support asymmetry  
→ actual factor descent  
→ coefficient subbundle  
→ quadratic pencil.

The local theorem shows that no positive-dimensional base is needed to recover a constant pencil. The moving theorem shows that fibrewise local classification is not enough for families. The isotrivial example makes that distinction concrete. The automorphism kernel honestly records all higher-order coordinate freedom that the first relation does not see.

This is a serious piece of mathematics. My rejection is not based on finding the construction empty or inconsistent.

The remaining question is whether this mechanism has been pushed far enough beyond its engineered model to justify a place in one of the four general journals.

At present I do not think it has.

---

## 15. Minimum conditions for another top-four review

I would regard a successor to v147 as ready for a genuinely fresh top-four evaluation only if it does the following.

### 15.1 Close Ballico 1993 completely

Obtain and read the complete theorem/proof text. Record exact theorem numbers, hypotheses, scheme structures, infinitesimal orders, relative statements, and whether any inverse reconstruction appears.

### 15.2 Turn the general coefficient theorem into a structural classification, or clearly limit the ambition

The present strict-support condition is a sufficient orientation criterion. A stronger paper would identify the exact ambiguity group of coefficient systems and characterize when reconstruction fails or becomes nonunique.

### 15.3 Supply a consequence native to quadratic pencils that uses the global theorem essentially

The q=1 rank-712 example is useful but not pencil-native. Give a moving-pencil phenomenon that cannot be reduced to separate fibrewise reconstruction and is invisible to the natural graded-bundle data, or derive an independent moduli/geometric consequence.

### 15.4 Sharpen the novelty statement around the combination of ingredients

Explain what is new beyond:

- classical inverse-system correspondence;
- standard determinant/Segre preserver theory;
- projective-to-linear factor descent once an actual tensor map is known;
- direct coefficient recovery from a multiplicity-one Cauchy summand.

The novelty should be a theorem-level synthesis, not merely the fact that these tools can be assembled for the present ideal.

### 15.5 Preserve the mathematical gains of v147

Do not retreat to generic pencils, do not drop singular pencils, do not remove the local inverse, and do not weaken actual bundle descent to projective-bundle recovery. Those are among the strongest features of the manuscript.

### 15.6 Keep the publication object disciplined

Continue to submit geometry.pdf as the sole principal article, with applications and the historical archive separate.

---

## 16. Final assessment

Revision 147 is a substantial and successful response to the mathematical part of the v146 report.

The general first-relation proposition clarifies the local algebra mechanism. The automorphism functor is now represented in the correct category. The determinant-preserver theorem is isolated. Most importantly, the actual-factor descent lemma supplies the invariant global proof that v146 lacked. The new coefficient-descent theorem is coherent, and the isotrivial example convincingly shows that the family reconstruction contains information not visible in individual fibres or in the underlying graded vector bundles.

I found no new fatal proof-level defect in those additions.

Nevertheless, I would not recommend publication in *Annals*, *Acta*, *Inventiones*, or *JAMS* in the present form.

The first reason is objective and documentary: the closest identified 1993 failure-locus predecessor remains unread at theorem/proof level, so the novelty boundary is explicitly open.

The second reason is editorial and mathematical: the new “general” theorem is still a sufficient inverse theorem for a specially encoded determinant-times-Cauchy class. It does not yet classify the inverse problem, and its strongest new separating example is engineered in the q=1 auxiliary class rather than in the quadratic-pencil setting that motivates the article.

The paper is now much closer to a strong specialized-geometry/algebra paper than it was in v146. It may even be correct in essentially all of its principal mathematical claims. But top-four acceptance requires a broader conceptual consequence or classification theorem, together with a closed novelty record.

**Recommendation: reject in the present form at top-four level; invite a genuinely new evaluation only after the historical comparison is closed and the global coefficient-descent mechanism is elevated from a sufficient construction-specific inverse to a broader structural result or a major pencil-native geometric consequence.**
