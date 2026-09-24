# Independent harsh referee report — A2 revision 148

## Manuscript and review object

**Manuscript:** *Finite failure schemes and the reconstruction of quadratic pencils*  
**Author:** Qian Qi  
**Revision reviewed:** A2 revision 148  
**Revision branch:** revision/a2-v148-coefficient-symmetries-moving-pencils-2026-09-24  
**Source-bound mathematical commit recorded by the revision:** 3acb5744f4b820070edb997b3aa38534f4726efe  
**Controlling previous review tip:** 17fb7ba7cab6545f5da6d4fcde5283318bd26725  
**Previous independent report:** reviews/a2-v147-independent-harsh-top4-2026-09-24/REFEREE_REPORT.md  
**Principal review object:** papers/A2-v17-boundary-information-coarsening/article/v148/geometry.pdf, 47 pages in the source-bound build receipt  
**Separate applications manuscript:** applications.pdf  
**Non-submitted historical archive:** archive-v144.pdf  
**Review standard:** the proof-completeness, originality, conceptual breadth, and exposition standard expected by *Annals of Mathematics*, *Acta Mathematica*, *Inventiones Mathematicae*, or *Journal of the AMS*.

This is an owner-requested external-referee-style assessment, not a journal-commissioned editorial decision. I reviewed the v148 principal source tree, the two genuinely new mathematical sections, the response to the v147 report, the issue matrix, source lock, build receipt and literature audit, and I rechecked the inherited moving-pencil and coefficient-descent interfaces on which the new results depend. I treat the 25 regression scripts as finite consistency checks, not as proof certificates.

## Recommendation

**Reject in the present form for a top-four general mathematics journal.**

Revision 148 is a serious and mathematically substantive response to revision 147. It does not merely add prose. The manuscript now gives an intrinsic recognition criterion for the determinant-times-Cauchy coefficient class, an exact proper/full orientation dichotomy, an explicit stabilizer calculation, a global treatment of the transpose ambiguity, and a genuinely pencil-native family in which the equivalence problem for maps P¹ to P¹ is faithfully recovered from unmarked finite thickenings although all fibres and the listed graded bundles are fixed.

I also want to be precise about what I did **not** find. After checking the new arguments against the inherited v146/v147 interfaces, I did not find a new fatal counterexample to the principal local inverse, the moving-pencil inverse, the actual source-bundle descent, the new recognition theorem, or the covering-map construction. The new mathematics appears internally coherent on the class actually defined in the paper.

The top-four rejection is therefore not a disguised claim of mathematical incorrectness. It rests on two different defects.

First, the closest identified failure-locus predecessor, Ballico 1993, remains explicitly unread at theorem/proof level. The manuscript's own v148 audit marks the six-axis comparison unresolved and historical priority uncertified. This fails the most concrete minimum condition of the previous report.

Second, the new v148 structural and covering results, while valid-looking, still do not in my view cross the conceptual threshold of a top-four general journal. The recognition theorem is largely a semisimple representation-theoretic characterization of the class obtained by defining admissibility to mean invariance under one full factor group. The covering theorem is a clean and nontrivial global encoding theorem, but after the v146 moving inverse is granted, its essential new step is to encode a degree-m map by the common factor of the singular pencil (ax+by)H and then recover that common factor. This faithfully transports a classical double-orbit problem into the failure-scheme category; it does not yet reveal a comparably broad new structure of quadratic pencils or their moduli.

Thus v148 has moved the paper again: it is no longer fair to say that the v147 significance objections were ignored. They were addressed literally and intelligently. But the response does not yet turn the article into an Annals/Acta/Inventiones/JAMS-level theorem.

---

## 1. What revision 148 genuinely adds

The v147 report asked for, among other things, two mathematical upgrades:

1. replace the strict-support sufficient criterion by a structural classification or exact ambiguity statement; and
2. provide a consequence native to quadratic pencils, not merely the auxiliary q=1 coefficient example.

Revision 148 supplies both.

The new section **Recognition and the exact ambiguity of coefficient systems** proves:

- recovery of the residual relation J after determinant cancellation;
- an intrinsic test, after the unordered determinant rulings are recovered, for whether J has a one-sided Cauchy coefficient decomposition;
- uniqueness of the coefficient spaces as multiplicity spaces;
- the exact proper-support versus zero/full orientation dichotomy;
- the complete linear stabilizer in both cases;
- the full higher-order automorphism extension for the truncated local algebra;
- the global form of the ruling-exchange ambiguity over a projective reduction; and
- a geometric orbit-set classification for fixed coefficient ranks.

The new section **Covering maps inside one fibre orbit of quadratic pencils** constructs, for every degree-m map f=[a:b] from P¹ to P¹, the moving pencil

R_f = (ax+by) H

inside a fixed two-plane H in V. Every fibre belongs to the same singular-pencil orbit. Nevertheless the associated unmarked order-d failure scheme recovers f up to independent projective transformations of source and target. The paper also computes the complete listed graded vector-bundle data and shows that these depend only on n and m, not on f.

These are real additions, and the response to the previous report correctly distinguishes them from the inherited material.

---

## 2. Correctness audit of the recognition theorem

Theorem thm:recognition-dichotomy-v148 begins with a subspace K in degree D whose generated homogeneous ideal has radical equal to a determinant hypersurface. This intrinsically recovers the determinant line and hence the residual subspace J=K/delta in degree q. Iterated singular loci recover the two unordered tensor rulings.

The paper then calls an ordering **admissible** when J is invariant under the full general linear group on the second tensor factor. For such an ordering, the conclusion

J = direct sum over lambda of L_lambda tensor S_lambda U

is the standard consequence of the Cauchy decomposition, complete reducibility, pairwise nonisomorphism of the right Schur factors, and Schur's lemma. The multiplicity spaces L_lambda are indeed unique and recovered by projection/contraction.

The orientation dichotomy also appears correct. If the reverse ordering is admissible as well, J is invariant under both full factor groups. Each Cauchy summand is irreducible for the product group, so J must be a sum of complete summands. Conversely, a sum of complete summands is invariant under both orderings. Thus a nonzero proper multiplicity space gives a unique admissible orientation, whereas a zero/full pattern gives the transpose ambiguity.

The final determinant-radical implication is likewise credible: at an invertible matrix T, the Schur map S_lambda T is invertible, so a nonzero coefficient covector cannot vanish identically on all invertible matrices; multiplication by the determinant gives exactly the determinant hypersurface as the common zero set. Over C the Nullstellensatz supplies the radical statement.

I therefore do not object to the theorem on correctness grounds.

---

## 3. Why the new “classification” is still narrower than the rhetoric suggests

The mathematical issue is not that Theorem thm:recognition-dichotomy-v148 is false. The issue is what it classifies.

Admissibility is defined to mean invariance under an entire recovered GL(U) factor. Once that symmetry is assumed, the one-sided Cauchy decomposition is essentially the isotypic decomposition of a completely reducible representation. The theorem therefore gives a necessary-and-sufficient characterization of the coefficient construction **inside a class selected by the exact symmetry that forces that construction**.

This is substantially better than the old strict-support sufficient criterion, but it is not yet a classification of the inverse problem posed by arbitrary first relations with determinant radical. It does not characterize which determinant-radical relation spaces acquire the required factor symmetry for intrinsic geometric reasons. It does not classify nearby deformations that leave the determinant radical fixed but break full-factor invariance. It does not describe orbit closures, singularities, deformation directions, or stack structure of the recognized locus. And it explicitly declines to classify arbitrary homogeneous ideals or arbitrary degeneracy schemes.

At a specialized level this is completely legitimate: one defines a natural representation-theoretic subclass and classifies its ambiguity exactly. At a top-four level, however, the paper advertises this as the structural elevation of the inverse theorem. In my view the upgrade remains too close to a reformulation of the designed coefficient class.

A stronger structural theorem would start from a more geometric or deformation-stable hypothesis than “invariant under the full recovered factor group,” and then derive the coefficient form, or it would classify the failure of reconstruction throughout a significantly larger natural stratum.

---

## 4. The exact stabilizer theorem is useful, but mostly closes bookkeeping

Theorem thm:exact-coefficient-stabilizer-v148 computes

- (G_L x GL(U))/G_m in the proper-support case; and
- ((GL_n x GL_n)/G_m) semidirect C_2 in the nonzero zero/full case.

The proof is the expected combination of:

1. preservation of the determinant radical;
2. the determinant/Segre linear-preserver theorem;
3. unique orientation in the proper-support case;
4. preservation of the multiplicity spaces on the left; and
5. arbitrary action on the full right factors.

The added Milne reference is appropriate for the quotient-to-closed-image step. The characteristic-zero reducedness/smoothness argument makes the passage from equality on complex points to equality of the closed subgroup schemes credible.

I regard this as a successful repair of the categorical precision requested in the previous report.

But it should not be oversold as an independent top-four-scale theorem. Once the recognition theorem and the classical determinant-preserver result are fixed, the stabilizer formula is close to the formal normalizer calculation one should expect.

The same applies to the extension by the universal higher-order substitution group. It is important for honesty about ungraded automorphisms, and the paper is right to keep it. It does not materially change the conceptual breadth of the main inverse theorem.

---

## 5. The global zero/full ambiguity is a good technical completion

Proposition prop:full-global-ambiguity-v148 addresses a point that earlier versions would have left ambiguous: if every active coefficient module is full, then locally the two matrix factors can be exchanged. The proposition shows that even in this case the abstract finite scheme still recovers the actual source-bundle isomorphism class, while a global exchange exists precisely when the source projective bundle is trivial, equivalently when the source bundle is a common line twist of a trivial rank-n bundle.

The proof uses the actual normal-bundle map rather than only projective bundle data. This is exactly the right use of the v147 commutant/actual-factor descent mechanism.

I do not see a correctness blocker in this argument.

It is, however, again a completion of the ambiguity analysis of the designed class, not a new geometric phenomenon of comparable scale to the main claims in a top-four paper.

---

## 6. The orbit-set corollary is intentionally weaker than a moduli theorem

Corollary cor:intrinsic-orbits-v148 identifies three sets of geometric orbits:

- coefficient Grassmannian data modulo PGL(V);
- recognized first-relation spaces modulo GL(n²); and
- the corresponding ungraded Artin algebras up to isomorphism.

This is a useful summary of the reconstruction statement.

The manuscript is commendably explicit that this is **not** an equivalence of moduli stacks, not a statement about nonreduced parameter bases, and not a deformation theorem. That caveat is correct and should remain.

But it also identifies the limitation. A genuine moduli-theoretic enhancement — for example, a comparison of quotient stacks on a natural open/stratified locus, a deformation-theoretic equivalence, or a description of orbit closures and singular stabilizer jumps — would materially deepen the result. The present orbit-set bijection does not.

For a top-four significance case, the distinction matters.

---

## 7. Correctness audit of the covering-map theorem

The new pencil-native theorem is the strongest addition in v148.

Fix H=<x,y> and a degree-m map f=[a:b]. The pencil bundle

R_f=(ax+by)H

has rank two because multiplication by the nonzero linear form ax+by is injective on H. Every fibre is equivalent to <x²,xy>, so the family is genuinely locally isotrivial in the pencil-orbit sense.

The bundle calculations are also coherent. In Sym²H, the two columns have Pluecker coordinates (a²,ab,b²). The exact sequence

0 -> O(-2m) -> O³ -> O(m)² -> 0

is justified by the displayed syzygy matrix; its maximal minors have no common zero. This yields the claimed quotient bundle and then the top nilradical graded piece after taking the fixed complement to the full Cauchy subspace. The rank formulas are consistent with the relation bundle having rank M.

The decisive equivalence

Y_f isomorphic to Y_f' iff f' = alpha composed with f composed with sigma

uses the inherited unrestricted moving-pencil inverse. Once that theorem supplies a **single constant** g in GL(V) carrying the entire moving pencil family to the other, the new argument extracts the common factor ell from the two-dimensional space ell H. Dividing by that common factor recovers H. Hence g preserves H and induces one alpha in PGL(H), while the reduction isomorphism supplies sigma. The converse is immediate by extending a lift of alpha from H to V.

This proof is short because the hard global descent is inherited, not because it is circular. I do not see a hidden fibrewise choice reintroduced in the v148 step.

The explicit pair z³ and z³+z is also correctly separated by ramification indices, and the n=3 numerical rank identities are consistent.

So again: this is not where I find a fatal correctness defect.

---

## 8. Why the covering theorem still falls short of the top-four significance threshold

The theorem is an elegant **faithful encoding** result.

But the geometry of the encoded family is deliberately chosen so that the varying datum is the common linear factor ell_f itself. Once the inherited moving inverse recovers the entire pencil subbundle up to one constant left transformation, recovering f from ell_f H is close to unique-factor extraction in a polynomial ring.

In other words, v148 shows that the global finite thickening remembers more than:

- the isomorphism class of each fibre;
- the conormal bundle;
- the first-relation bundle;
- the pencil and quotient bundles; and
- the listed associated graded vector bundles.

That is a meaningful global-rigidity phenomenon.

What it does **not** yet do is solve a natural pre-existing geometric problem about moving quadratic pencils that was not built into the encoding. The theorem does not classify a natural moduli space of pencil degenerations. It does not derive a new invariant of regular pencils. It does not reveal an unexpected boundary structure, compactification, deformation theory, or Torelli phenomenon for a standard moduli problem. It takes an arbitrary rational self-map of P¹, inserts it into a common-factor pencil family, and proves the resulting finite scheme faithfully remembers the inserted map.

This distinction is editorially decisive at the top-four level.

A faithful functor from a familiar equivalence problem into a highly structured class of finite schemes can be quite interesting. But without a deeper intrinsic characterization of the image or a new geometric theorem about that image, the construction remains closer to universality/encoding than to a new organizing theorem of algebraic geometry.

The fact that all fibres lie in one singular orbit is a strength as a demonstration that fibrewise classification is insufficient. It is also a warning about significance: the construction exploits an intentionally degenerate common-factor orbit rather than discovering rigidity in a naturally occurring family of general pencils.

---

## 9. The inherited v146/v147 proof chain remains the real engine

The new covering theorem depends critically on the inherited statement that an abstract isomorphism of the finite total schemes yields:

- the isomorphism of reduced bases;
- one constant left transformation;
- an actual source-bundle isomorphism; and
- equality of the moving pencil subbundles under those data.

I rechecked the relevant v146/v147 source path rather than treating that interface as a black box.

The inherited proof recovers the first relation from multiplication in the nilradical, generates the homogeneous cone, takes its determinant radical, recovers the unordered rank-one rulings, orients them using asymmetric coefficient support, uses projectivity to force the left PGL map to be constant, and then uses the actual normal-bundle map plus the commutant lemma to recover the right vector bundle without a line twist.

Revision 147 already repaired the weakest part of that chain: the actual-factor descent. I still do not see a new contradiction introduced by v148.

This matters for the referee conclusion. The rejection is not based on pretending that the new result is unsupported. The inherited engine is substantial. The question is whether the new output obtained from that engine is broad and conceptually unexpected enough for one of the four general journals.

I do not think it is.

---

## 10. The “smallest uniform order” remains an engineered sharpness statement

The paper continues to emphasize the threshold

d = n² + 2n - 4

for quadratic pencils.

The lower-order independence statement is correct in the presented construction because the defining first relations occur exactly in degree d. The order-d inverse is therefore uniformly sharp for this particular finite-thickening functor.

This is useful and should be retained.

But the numerical threshold should not be made to carry more conceptual weight than it has. Its sharpness is largely forced by the chosen degree of the determinant-times-minor relation. The deep content is the orbit rigidity of the first relation after all markings are forgotten, not the mere existence of a number d below which the deliberately delayed relations vanish.

The v148 introduction mostly understands this distinction, but the abstract and presentation still invite a reader to treat the threshold itself as a major geometric depth phenomenon. I would continue to subordinate the number to the reconstruction mechanism.

---

## 11. Ballico 1993 remains an unresolved top-four blocker

This point is unchanged and should not be softened.

The v148 literature audit states that the complete theorem/proof text of:

E. Ballico, *On the Failure Locus of Higher Order Properties of Embeddings in Projective Spaces*, Mathematische Nachrichten 163 (1993), 5–13

has still not been obtained.

The audit consequently leaves unresolved, on the Ballico side:

- the exact underlying objects;
- whether the failure locus is treated with nonreduced scheme structure;
- the infinitesimal order retained;
- the relative hypotheses;
- what data are forgotten in the isomorphism problem; and
- whether any inverse reconstruction conclusion appears.

The manuscript is commendably honest: it explicitly marks historical priority uncertified and does not claim nonanticipation.

That honesty does not close the issue.

For a top-four submission centered on nonreduced failure schemes, the closest named predecessor in the failure-locus literature cannot remain unexamined at theorem/proof level. The referee cannot establish novelty by inference from a title, metadata, opening page, or failed download attempts. Nor can regression scripts or an internally new theorem settle an external priority comparison.

This is not a demand for ceremonial bibliography. It is a basic condition for assessing originality at the level claimed.

A future top-four resubmission should not return before the full article has been obtained through a legitimate library/document-delivery route or equivalent and compared theorem by theorem.

---

## 12. Novelty relative to the classical ingredients is still not sharply enough isolated

The manuscript now correctly disclaims novelty for:

- the Cauchy decomposition;
- complete reducibility;
- determinant/Segre preservers;
- Pluecker reconstruction;
- common-factor extraction;
- projective linear algebra; and
- basic Artin truncation observations.

That is an improvement.

The genuinely new-looking synthesis is:

unmarked finite scheme  
-> first relation  
-> determinant cone  
-> unordered tensor rulings  
-> orientation from residual representation  
-> one constant left map over a proper base  
-> actual right bundle from the normal map  
-> coefficient or pencil recovery.

This spine is mathematically interesting.

But the paper still needs a more convincing answer to: **what general phenomenon does this synthesis reveal beyond the specially manufactured determinant-times-Cauchy relation?**

V148 answers with “it recognizes exactly the factor-invariant subclass and can encode the full equivalence problem for covers P¹ to P¹.” That is progress, but for a top-four paper it remains an answer about the expressive power of the construction rather than a theorem organizing a broad pre-existing geometric landscape.

A specialized algebraic-geometry or commutative-algebra venue may well value precisely that inverse construction. The general-journal threshold is higher.

---

## 13. Reproducibility and source discipline are excellent, but editorially orthogonal

The v148 source lock records the mathematical source commit and the controlling prior review. The build receipt records a 47-page principal article, 25 successful regression scripts, preservation of all inherited mathematical blocks, resolved labels/references, and source hashes.

This is unusually strong research engineering.

The paper also draws the right evidentiary boundary: the receipt explicitly says that the computation does not certify universal proofs, historical priority, or journal acceptance.

I agree completely.

Accordingly, the successful build and finite exact checks increase confidence in formulas and examples, but they do not change the decision on originality and top-four significance.

---

## 14. Minor editorial and documentary issues

These are not reasons for rejection, but they should be cleaned up.

1. The separate applications driver still contains a PDF title identifying it as “A2 revision 146” although the v148 source tree is dated September 24, 2026. Since applications.pdf is explicitly separate from the principal article, this is minor, but it is avoidable version drift.

2. The principal article is now 47 pages and carries several generations of theorem labels and inherited section names. The source preservation strategy is excellent for provenance, but a submission copy should read like one paper rather than an archaeological record of 148 iterations. Historical version suffixes are useful internally; they are distracting in a final journal manuscript.

3. The introduction spends substantial space explaining the genealogy of previous repairs. A final submission should state the conceptual theorem architecture directly and move revision-history explanations to a response letter.

4. The distinction between “classification of the recognized class” and “classification of all determinant-radical first relations” should be visible already in the abstract-level rhetoric, not only in later caveats.

---

## 15. What revision 148 successfully closes from the previous report

For clarity, I would record the previous minimum conditions as follows.

### 15.1 Full Ballico 1993 theorem/proof comparison

**Not closed.** The manuscript itself marks this documentary item open.

### 15.2 Structural classification and exact ambiguity

**Partially closed in a mathematically valid but narrower sense.** The exact ambiguity of the full-factor-invariant coefficient class is now classified. What remains missing for top-four significance is a broader structural theorem not defined by the very symmetry that enforces the decomposition.

### 15.3 Pencil-native global consequence

**Closed literally.** The P¹-cover construction is genuinely inside the quadratic-pencil family, all fibres lie in one pencil orbit, and the total unmarked scheme recovers the cover equivalence class.

### 15.4 Sharpen the theorem-level synthesis beyond classical ingredients

**Improved but not closed at top-four level.** The synthesis is clearer; its independent geometric reach remains too narrow.

### 15.5 Preserve the all-pencil, local, singular, and actual-descent gains

**Closed.** I found no retreat from those results.

### 15.6 Keep the publication object disciplined

**Closed.** geometry.pdf remains the principal article; applications and archive are separate.

This is a much stronger response than a cosmetic revision. The remaining rejection should therefore be understood as a threshold judgment, not as repetition of objections that v148 actually fixed.

---

## 16. Minimum conditions for another top-four evaluation

I would not recommend another top-four round merely for another layer of examples or certificates. A genuinely new evaluation should be triggered by a conceptual enlargement.

### 16.1 Close the historical comparison completely

Obtain the full Ballico 1993 paper and make a theorem/proof-level comparison. Give exact theorem numbers, hypotheses, scheme structures, infinitesimal orders, relative statements, and any inverse conclusions.

### 16.2 Go beyond factor-invariance as the definition of the recognized class

Either classify a substantially larger natural family of determinant-radical first relations, or derive the factor-invariance condition from geometric hypotheses that do not already encode the desired one-sided Cauchy structure.

A deformation-theoretic or orbit-closure analysis would be one meaningful route.

### 16.3 Replace faithful encoding by an independent geometric consequence

The next major theorem should say something new about a natural moduli or degeneration problem for quadratic pencils, rather than insert an arbitrary external moduli problem into a common-factor family and recover the inserted datum.

Examples of the required level would include a genuine Torelli-type statement for a natural compactification, a classification of a broad boundary stratum, a deformation-equivalence theorem for the finite failure functor, or an intrinsic moduli comparison with new consequences on either side.

### 16.4 If moduli language is used, upgrade the set-theoretic orbit statement

A quotient-set bijection is not a moduli theorem. If the paper wants the recognition result to carry moduli-theoretic weight, address stabilizers in families, infinitesimal deformations, and the relevant quotient-stack or coarse-moduli structure on a natural locus.

### 16.5 Preserve the hard-won proof architecture

Do not weaken the all-pencil inverse to generic pencils, do not drop singular pencils, do not retreat from ungraded local algebras, and do not replace actual source-bundle recovery by projective recovery. These are among the paper's strongest mathematical achievements.

---

## 17. Final assessment

Revision 148 is mathematically stronger than revision 147.

The author has supplied an exact proper/full ambiguity analysis of the coefficient systems and a genuine quadratic-pencil family whose total unmarked failure scheme remembers an entire covering map while its individual fibres and listed additive bundle invariants do not. The stabilizer and line-twist analyses are more precise, the group-scheme reference is now appropriate, and the inherited actual-factor descent remains intact. I do not identify a new fatal proof error in these additions.

Nevertheless, the paper is still not ready for *Annals*, *Acta*, *Inventiones*, or *JAMS*.

The closest named predecessor remains unresolved at theorem/proof level, so the priority boundary is not closed. More importantly, the new “structural classification” is still a classification of a class selected by full-factor symmetry, and the new covering theorem is still a faithful engineered encoding whose decisive extraction becomes elementary once the powerful inherited moving inverse is granted. These are worthwhile results, but they do not yet produce the breadth, inevitability, or independent geometric consequence expected of a top-four general-journal article.

My present view is that the manuscript has evolved into a potentially strong specialized paper with unusually careful proof engineering and provenance. To justify another top-four evaluation, it needs a new conceptual theorem, not another round of local repair.

**Recommendation: reject in the present form for a top-four general mathematics journal.**
