# Independent harsh referee report — A2 revision 146

## Manuscript and immutable review object

**Manuscript:** *Finite failure schemes and the reconstruction of quadratic pencils*  
**Author:** Qian Qi  
**Revision reviewed:** A2 revision 146  
**Revision branch:** `revision/a2-v146-referee-proof-completion-2026-09-24`  
**Immutable mathematical source:** `5d5ce834e24b5c7ba80a9ccf2a63b0a449913c5d`  
**Immediate predecessor:** `89edc80cce6fd1801b356313544419d30f377636` (v145)  
**Controlling earlier report recorded by the revision:** `d8376b5dbb47422d93a474add8362d39cf2a68c1`  
**Principal review object:** `papers/A2-v17-boundary-information-coarsening/article/v146/geometry.pdf` (32 pages according to the source-bound receipt)  
**Separate applications manuscript:** `applications.pdf`  
**Non-submitted historical archive:** `archive-v144.pdf`  
**Review standard:** external-referee-style assessment at the level of *Annals of Mathematics*, *Acta Mathematica*, *Inventiones Mathematicae*, or *Journal of the AMS*.

This is an owner-requested independent referee-style review, not a journal-commissioned editorial decision. I reviewed the source-locked v146 principal manuscript and the new proof blocks rather than treating the branch name, response letter, or regression scripts as a substitute for the mathematics. I also checked the v146 source lock, build receipt, issue matrix, response to the v144 reports, the current literature audit, and the controlling earlier report. The receipt records twenty-three successful scripts and successful native builds, but it also correctly states that computation does not certify the proofs or historical priority.

## Recommendation

**Reject in the present form for a general top-four mathematics journal.**

This recommendation is materially different from the v144 rejection. Revision 146 has fixed a substantial part of the former architecture problem, and the new mathematics is not cosmetic. In particular, I do not presently see a fatal counterexample to the new coefficient-support orientation lemma, the unmarked Artin-local inverse, the unrestricted moving-family theorem, or the explicit tangent-identity automorphism kernel. The new local theorem is a genuine strengthening of the previous curve-supported inverse.

The remaining top-four objections are nevertheless decisive.

1. **The closest identified historical predecessor, Ballico 1993, remains unread at theorem level.** The manuscript itself records `Ballico_1993_full_text_comparison_completed=false` and `historical_priority_certified=false`. I independently found the publisher/bibliographic record for E. Ballico, *On the Failure Locus of Higher Order Properties of Embeddings in Projective Spaces*, Math. Nachr. 163 (1993), 5–13, DOI 10.1002/mana.19931630102, but not theorem/proof text sufficient to close the six-axis comparison. I therefore make neither an anticipation claim nor a nonanticipation claim. A top-four novelty claim cannot be certified while the closest named predecessor remains unresolved.
2. **The new single-point Artin theorem is mathematically clean, but its conceptual depth is less than the headline language suggests.** Because there are no relations below degree d and everything above d is killed, an ungraded isomorphism first recovers the tangent space and the degree-d relation subspace. Nonlinear coordinate changes are invisible to that first relation space. The paper's own Proposition `prop:local-automorphisms-v146` makes this explicit: the entire tangent-identity freedom consists of arbitrary higher-order substitutions. Thus the local inverse reduces to a linear orbit-rigidity theorem for the specially engineered subspace K_R, followed by determinant-cone factor recovery, support-rank orientation, and exterior duality. That is a real theorem, but it is not by itself a deep nonlinear local Torelli phenomenon.
3. **Moving the headline to an Artin local algebra creates a new literature obligation that the current audit does not address.** There is a substantial classical and modern literature on isomorphism classes of Artinian local algebras, Macaulay inverse systems, canonical grading, and reduction of local-algebra isomorphism to homogeneous orbit problems. The present theorem need not be anticipated by that literature, but the paper must compare its mechanism to it. For orientation, see for example J. Elias and M. E. Rossi, *Isomorphism classes of short Gorenstein local rings via Macaulay's inverse system* (arXiv:0911.3565) and *Analytic Isomorphisms of compressed local algebras* (arXiv:1207.6919). The current literature section is still organized almost entirely around failure loci and pencils.
4. **The moving-family theorem is potentially the most conceptually important new v146 result, but the actual source-bundle recovery is compressed exactly where a top-four proof should be most invariant.** A projective Segre factorization normally leaves line-bundle twists. The manuscript asserts that after fixing the constant left lift g, the right maps are unique and glue to an actual bundle isomorphism h; it then gives a one-sentence commutant alternative. I believe the argument is salvageable and likely correct because the abstract scheme isomorphism supplies an actual linear normal-bundle map, not merely projective factor data. But this should be isolated as a coordinate-free lemma proving that the actual map kills the line-twist ambiguity. The headline claim “the actual source bundle is recovered” deserves more than a local-frame paragraph.
5. **The top-four significance case is still not demonstrated.** The local theorem strengthens the invariant, but it also exposes how deliberately the invariant has been engineered: the first nonzero relation is precisely a determinant factor times a coefficient module whose left line is dual to the pencil's Pluecker line. The nontrivial content is that the tensor orientation and coefficient line are intrinsic after all markings are erased. To justify a top-four venue, the paper needs either a substantially broader reconstruction principle or a major geometric consequence that genuinely depends on this unmarked mechanism. Accumulating further readouts of a reconstructed pencil will not solve this.

I would support a fresh top-four review only after the novelty boundary and the conceptual scope are closed. I would not ask the author to weaken the all-pencil theorem or retreat to generic pencils.

---

## 1. What v146 genuinely fixes

The revision should receive credit for answering several serious objections from the preceding reports.

First, the publication object is now intelligible. The principal submission is the 32-page `geometry.pdf`; the likelihood/critical material is a separate applications manuscript; the 130-page object is explicitly a non-submitted archive. This substantially resolves the earlier objection that one referee was being asked to certify several research programs under one title.

Second, the new coefficient-support argument removes the artificial dependence on a nontrivial source projective bundle. The earlier geometric orientation used the fact that among the two rank-one rulings only the V-ruling was projectively trivial. Revision 146 adds an intrinsic local discriminator: in the relevant multiplicity-one Cauchy summand the residual module has support ranks (1,M), whereas transposition gives (M,1). Since M>1, transposition is impossible. This is a clean and useful observation.

Third, the local theorem really does remove all positive-dimensional support. The invariant is now a single unmarked finite-dimensional local algebra

    A_R^[d] = C[t_ij] / ((det T) I_p(gamma_R Sym^2 T) + m^(d+1)),

with no grading, matrix coordinates, tensor factors, or chosen generators supplied to the isomorphism. The ungraded statement is stronger than the earlier Schubert-line realization.

Fourth, the explicit automorphism kernel is a useful honesty check rather than decoration. The theorem does not falsely identify all local-algebra automorphisms with pencil stabilizers. The huge tangent-identity group explains exactly how much coordinate freedom the inverse ignores.

These are substantive improvements, not presentational changes.

---

## 2. Hostile audit of the new coefficient-support orientation

The key lemma is `lem:coefficient-orientation-v146` in `parts/32-local-inverse-v146.tex`. Its structure is sound.

After the determinant cone is recovered, any linear preserver of the rank-one cone is of left-right type or left-right followed by transposition. In a multiplicity-one Cauchy summand the residual coefficient subspace has the form

    L tensor S_lambda(U)  subset  S_lambda(V)^* tensor S_lambda(U),

with support ranks `(dim L, dim S_lambda U)`. Separate changes of the two tensor factors preserve these ranks; transposition exchanges them. For pencils the exterior representation F(H)=wedge^(N-2) Sym^2(H) is irreducible and the left coefficient space is a line, so the ranks are `(1,M)` with `M=binom(N,2)>1`. Hence the transposed alternative cannot land in another pencil coefficient module of the same type.

I do not see a genericity loophole here. The argument does not depend on regularity of the pencil, discriminant simplicity, or a rank condition on the pencil. It is a representation-theoretic statement about the coefficient subspace. Line twists also do not alter contraction ranks.

One point should nevertheless be strengthened in exposition: the manuscript currently proves the determinant-cone preserver alternatives by restricting to decomposable tensors and using projective linearity. Since this dichotomy is now central to the strongest theorem, it would be preferable to isolate the exact linear-preserver lemma, state its field and dimension hypotheses, and cite the classical preserver result if one is being reproved. The present proof is plausible, but a top-four paper should make the classification input impossible to miss.

---

## 3. The ungraded local inverse appears correct, but its mechanism should be stated more candidly

Theorem `thm:artin-local-inverse-v146` says

    A_R^[d] isomorphic to A_R'^[d]  iff  R'=(Sym^2 g)R.

The proof relies on the intrinsic maximal ideal n. Since there are no relations below degree d, one recovers the tangent space `n/n^2` and the kernel

    K_R = ker[ Sym^d(n/n^2) -> n^d ].

This is indeed intrinsic under an ungraded algebra isomorphism. A nonlinear change of minimal generators has the form `x -> linear(x) + terms of order >=2`; when substituted into a degree-d relation, its nonlinear contribution begins in degree d+1 and is zero in the truncation. Therefore the ungraded isomorphism acts on K_R only through its tangent linear map.

From K_R one forms the homogeneous ideal it generates. Its radical is the determinant ideal: off `det T=0`, T is invertible, hence `gamma_R Sym^2 T` is surjective and at least one maximal minor is nonzero. Determinant cancellation then recovers the residual coefficient module. The support-rank lemma orients the tensor factors; exterior duality recovers the Pluecker line of R.

I do not see a circular use of the original matrix coordinates after the tangent space has been recovered. Nor do I see a hidden regular-pencil hypothesis.

However, the proof also shows that the apparently nonlinear statement is much closer to a linear orbit problem than the introduction admits. In fact v146 should formulate the following general principle explicitly: for a vector space E and a degree-d subspace K of Sym^d E with no lower relations, the algebra

    Sym(E)/(K + m^(d+1))

remembers K up to the tangent GL(E)-action, while all tangent-identity coordinate changes form a universal unipotent kernel. The pencil theorem is then the nontrivial assertion that the GL(E)-orbit of K_R determines the GL(V)-orbit of R.

Stating this general lemma would improve the paper in two ways. It would clarify exactly what is difficult, and it would force an honest comparison with the classical theory of isomorphisms of Artin local algebras rather than presenting the ungraded formulation as if the truncation itself created a new nonlinear rigidity phenomenon.

---

## 4. The local automorphism proposition is plausible, but its category should be cleaned up

Proposition `prop:local-automorphisms-v146` claims a split exact sequence

    1 -> U_R -> Aut_C(A_R^[d]) -> (G_R x GL(U))/C^* -> 1,

and identifies U_R, after choosing degree-one generators, with all substitutions

    x_i -> x_i + u_i,   u_i in n^2.

The algebraic argument is persuasive. Every defining relation has degree d, so the substitution changes it only in degree at least d+1; these terms vanish. Conversely a tangent-identity endomorphism of a finite filtered local algebra is invertible. Thus there are no hidden equations on the u_i. Since `dim n^2 = length(A)-1-n^2`, the affine-space dimension is correct.

Still, the statement mixes levels: the sequence is introduced as one of “complex automorphism groups,” while U_R is called a unipotent algebraic group and its underlying variety is identified. A top-four version should say explicitly whether the full sequence is meant in the category of algebraic groups / automorphism group schemes, or only on C-points with an independently exhibited algebraic structure on the kernel. If the stronger algebraic-group statement is intended, prove representability and that the quotient/splitting maps are morphisms. If only the abstract-group statement is intended, say so and avoid letting the geometric language suggest more.

A coordinate-free description of U_R would also help. The chosen-generator parametrization is convenient, but the intrinsic object is a space of higher-order corrections to a minimal lifting of the tangent space. This matters because the theorem is being sold as unmarked.

---

## 5. The moving-family theorem is stronger than the local theorem in the direction that matters

Theorem `thm:unrestricted-moving-v146` removes the source-projectivization restriction from `thm:moving-reconstruction-v146`. The resulting assertion is genuinely global: an abstract finite scheme over an unspecified smooth connected projective reduction recovers the base, the constant left vector space up to one constant transformation, the actual rank-n source bundle, and the varying rank-two pencil subbundle.

The first steps are convincing. The nilradical recovers the reduction and conormal bundle. The degree-d multiplication kernel reconstructs the homogeneous cone. Its determinant reduction recovers the two unordered rank-one rulings. Coefficient-support asymmetry orients them. Because the left ruling is a trivial projective bundle and the base is connected projective, the induced map to PGL_n is constant.

The delicate point is the passage from projective factor data to an actual source-bundle isomorphism. In general, an isomorphism of projective bundles determines a vector bundle only up to tensoring by a line bundle. The manuscript says that after fixing one constant linear lift g, local right maps are unique and glue; alternatively, removing g makes the actual normal-bundle map commute with End(V), so the commutant is the right-factor homomorphism bundle.

I believe the second sentence contains the correct reason, but it should be promoted to a formal lemma. One should state and prove, globally, that an actual bundle isomorphism

    V tensor U_1^*  ->  V tensor U_2^*

whose induced Segre action is the identity on the V-projective factor lies in `id_V tensor Isom(U_1^*,U_2^*)`, after fixing the constant lift. This is exactly what kills the line twist. The current local-gluing paragraph is too compressed relative to the strength of the conclusion.

This is not presently a counterexample; it is a demand that the most delicate global descent step be written at the same standard as the headline theorem.

---

## 6. Uniform sharpness is correct, but it is not the significance argument

The order

    d = n^2 + 2n - 4

is the first degree in which the defining ideal contributes. Consequently every truncation below d is independent of R, while order d recovers R. This proves the smallest **uniform** reconstruction order. The manuscript now uses that phrase consistently, which is correct.

But the number d itself is not a deep threshold phenomenon: it is forced by the degree of the determinant factor plus the maximal minors. The mathematical content is the orbit rigidity of the first relation space. The paper should resist presenting the integer d as an independent source of conceptual depth.

---

## 7. The old publication-object objection is substantially resolved

I withdraw the strongest form of the v144 objection that the referee is being asked to certify a 130-page multi-program submission. Revision 146 now declares:

- `geometry.pdf` as the principal paper;
- `applications.pdf` as a separate manuscript;
- `archive-v144.pdf` as a non-submitted research archive.

The principal source is internally closed and does not require the archive to establish its main theorem. This is the correct direction.

I would keep the spectral consequences in the principal paper only insofar as they illuminate information recovered by the inverse. They should remain consequences, not co-equal headline claims. The separate applications manuscript should remain separate.

---

## 8. Ballico 1993 remains a non-negotiable novelty blocker

The current `LITERATURE_AUDIT_V146.md` is intellectually honest: every theorem-text cell for Ballico 1993 says, in effect, “not obtained; no content inferred.” That is better than inventing a comparison, but it does not solve the problem.

I independently verified the bibliographic existence of the 1993 article through the publisher/indexing record. I was not able, from the accessible material, to inspect the theorem/proof text needed to answer the manuscript's own six comparison questions. I therefore do not know whether the 1993 paper contains only support-level failure loci, retains nonreduced/Fitting structure, treats infinitesimal neighborhoods, has a relative construction, or proves any inverse recovery statement.

For an ordinary specialized journal, one might allow the author to state a narrow novelty claim conditioned on what has actually been checked. For a top-four submission whose title and central construction are explicitly about a failure scheme, leaving the closest identified failure-locus paper unresolved is not acceptable.

The next version must obtain the paper by library/interlibrary means if necessary and record theorem numbers, hypotheses, defining maps, scheme structures, family/base-change scope, and any inverse conclusions. Metadata is not enough.

---

## 9. A new prior-art audit is now required for the Artin-local formulation

V146's strongest slogan is no longer merely “one Schubert line suffices” but “one unmarked Artin local algebra suffices.” That change broadens the relevant literature.

The paper should compare its local mechanism with at least the following traditions:

- Macaulay inverse systems and apolar descriptions of Artinian algebras;
- classification of isomorphism classes of Artinian Gorenstein/level local rings;
- canonical-grading results in which analytic isomorphism classes reduce to homogeneous data;
- automorphism groups of truncated local algebras and homogeneous ideals;
- linear preservers of determinantal and Segre varieties.

Elias–Rossi's work on short Gorenstein local rings is not being cited here as anticipation: their hypotheses and objects are different. It is being cited because it demonstrates that “ungraded local algebra isomorphism reduces to a homogeneous projective orbit problem” is an established conceptual pattern. V146 must explain what is new in its much higher socle-degree, non-Gorenstein, specially structured setting.

Without that comparison, the new headline has outrun the literature review.

---

## 10. Top-four significance remains the central unresolved question

The paper has a valid-looking mathematical spine:

    abstract finite local/family scheme
        -> tangent/conormal bundle
        -> first degree-d relation space
        -> determinant cone
        -> tensor rulings
        -> orientation by coefficient-support asymmetry
        -> residual coefficient line
        -> Pluecker plane R.

This is elegant. But elegance is not the same as top-four significance.

In fixed coordinates the coefficient line is deliberately built from the quotient volume associated with R, and exterior duality sends it back to the Pluecker line of R. The main difficulty is erasing and then intrinsically recovering the markings. V146 solves that difficulty more completely than v144. What it does not yet show is why this mechanism changes the way one thinks about a broad class of inverse problems.

The structural coefficient theorem is the right seed, but it still reads mainly as a criterion tailored to the present determinant/Cauchy setup. For a top-four paper I would want at least one of the following:

1. a general theorem classifying when first nonzero relation modules of nonreduced degeneracy loci recover their defining data;
2. a moduli-level consequence that is genuinely nonformal after the unmarked quotient;
3. a new geometric theorem for natural objects whose proof essentially requires the unmarked reconstruction and is not simply a readout once R is known;
4. a conceptual bridge to a major existing theory of Artin algebras, determinantal singularities, or inverse systems that makes this construction a new instance of a broader phenomenon.

The current moving-family theorem is the most promising candidate for such a bridge. It should be developed conceptually rather than followed by another long sequence of special-purpose consequences.

---

## 11. The regression evidence is useful but has exactly the right limited status

The source-bound receipt records twenty-three successful scripts, native PDFs, preserved predecessor bytes, unique labels, resolved references, and no overfull boxes. This is excellent research engineering.

I emphasize, however, that the scripts do not verify:

- the universal coefficient-support lemma;
- the global source-bundle descent;
- the classification of all determinant-cone linear preservers;
- the theorem-level priority comparison;
- the top-four significance claim.

The v146 README and receipt themselves acknowledge this, so I do not regard the computational evidence as misleading. It should remain in this modest role.

---

## 12. Specific mathematical and expository revisions I would require

### 12.1 Isolate the general first-relation/truncation lemma

State a standalone proposition describing isomorphisms of algebras `Sym(E)/(K+m^(d+1))` when K has pure degree d: extraction of K from multiplication, action through the tangent GL(E), and the tangent-identity unipotent kernel. This will make the local inverse transparent and place the novelty where it belongs: the orbit rigidity of K_R.

### 12.2 Give a coordinate-free global factor-recovery lemma

Formalize the commutant argument that removes the line-bundle ambiguity and recovers the actual source bundle in the moving theorem. Do not leave the strongest global conclusion resting on “the local maps therefore agree on overlaps.”

### 12.3 Clarify the category of the automorphism exact sequences

Say explicitly whether the sequences are sequences of abstract groups of C-points or algebraic groups/group schemes. Prove the stronger statement if intended.

### 12.4 Expand the determinant-preserver input

Either cite a precise linear-preserver theorem or isolate the proof that a linear isomorphism carrying the determinant cone to itself is left-right or transpose-left-right. The support-rank orientation theorem depends on this classification.

### 12.5 Add an Artin-local literature section

Compare to inverse systems, canonical grading, analytic isomorphism, and automorphism-group results. Explain why the present algebra is not merely another canonically graded short algebra and what the determinantal coefficient structure adds.

### 12.6 Close Ballico 1993

This remains mandatory. No amount of additional internal strengthening substitutes for reading the closest named predecessor.

### 12.7 Keep all scope distinctions

Continue to separate: all-pencil reconstruction; regular-pencil spectral consequences; marked relative base change; split semisimple critical applications; real definite likelihood statements. Do not compress them into one unconditional slogan.

---

## 13. What I would *not* ask the author to do

I would not recommend weakening the theorem to generic pencils, deleting singular pencils, discarding nilpotent structure, retreating from the single-point statement, or suppressing the moving-family theorem. Those would make the paper less interesting and would not address the real objections.

I also would not ask for more theorem accumulation. V146 already has enough results. The next gains must come from conceptual compression, literature closure, and a sharper explanation of why the unmarked mechanism matters.

---

## 14. Minimum conditions for a fresh top-four evaluation

I would regard a new version as ready for a genuinely fresh top-four review only if it does all of the following:

1. obtains and compares Ballico 1993 at theorem/proof level;
2. positions the Artin-local inverse against the inverse-system / Artin-algebra isomorphism literature;
3. recasts the local theorem through a general first-relation orbit lemma, making clear that nonlinear coordinate freedom is the universal unipotent kernel rather than the source of rigidity;
4. gives a fully invariant proof of actual source-bundle recovery in the moving-family theorem;
5. clarifies the algebraic-group status of the automorphism sequences;
6. makes the moving-family reconstruction, rather than theorem count, the principal significance case;
7. keeps `geometry.pdf` as the sole principal object and the applications/archive separate;
8. preserves the present all-pencil scope and the correct “smallest uniform order” formulation;
9. issues a new immutable source lock after any mathematical change.

---

## 15. Final assessment

Revision 146 is a serious improvement and, on the mathematics I audited, the strongest A2 version so far.

The new coefficient-support asymmetry is simple but effective. It removes the transpose ambiguity without a positive-dimensional base. The resulting unmarked Artin-local theorem appears internally coherent: the maximal ideal gives the tangent space, multiplication recovers the first degree-d relation kernel, the homogeneous cone recovers the determinant geometry, support ranks orient the factors, and exterior duality returns the pencil. The moving-family theorem extends this to a genuinely global reconstruction problem, and the explicit unipotent automorphism kernel correctly exposes the higher-order freedom that the invariant does not see.

I did not find a new fatal proof-level defect in that chain.

That is still not enough for one of the four general mathematics journals. The local theorem is, after the truncation is unpacked, an orbit-rigidity theorem for a deliberately constructed first relation space; the paper has not yet situated that fact against the mature Artin-local/inverse-system literature. The moving-family theorem is more conceptually promising but deserves a more invariant descent proof. Most importantly, the closest identified historical failure-locus predecessor from 1993 remains unexamined at theorem level, so the central novelty boundary is still open by the manuscript's own records.

Accordingly my recommendation remains **reject in the present form at top-four level**. If the historical comparison is closed favorably, the Artin-local literature boundary is handled seriously, and the paper is reframed around the moving/unmarked reconstruction mechanism rather than the number of consequences, I would regard a subsequent version as deserving a new review rather than as exhausted by the current rejection.