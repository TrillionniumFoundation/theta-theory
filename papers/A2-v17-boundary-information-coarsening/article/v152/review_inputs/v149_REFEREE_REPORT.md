# Independent harsh referee report — A2 revision 149

## Manuscript and review object

**Manuscript:** *Finite failure schemes and the reconstruction of quadratic pencils*  
**Author:** Qian Qi  
**Revision reviewed:** A2 revision 149  
**Revision branch:** revision/a2-v149-intrinsic-pencil-strata-deformations-2026-09-24  
**Source-bound mathematical commit:** 4af97058186974234e2669677818956781a67a08  
**Controlling previous review:** review/a2-v148-independent-harsh-top4-2026-09-24  
**Controlling previous review tip:** dc3a951e26de17e0e69403b1d8cfdfb5e28bc306  
**Principal review object:** papers/A2-v17-boundary-information-coarsening/article/v149/geometry.pdf, 55 pages in the source-bound receipt  
**Separate applications manuscript:** applications.pdf  
**Non-submitted historical archive:** archive-v144.pdf  
**Review standard:** the proof-completeness, originality, conceptual breadth, and exposition standard expected at Annals of Mathematics, Acta Mathematica, Inventiones Mathematicae, or Journal of the AMS.

This is an owner-requested external-referee-style report, not a journal-commissioned editorial decision. I reviewed the v149 principal source, the three new sections, the response to the v148 report, the issue matrix, proof-scope audit, source lock, theorem locator, build receipt, and the v148 controlling referee report. I also rechecked the closest unresolved historical citation by exact title and DOI. The 26 regression scripts and 50 new exact witnesses are treated as finite consistency checks, not as universal proof certificates.

## Recommendation

**Reject in the present form for a top-four general mathematics journal.**

Revision 149 is a substantial mathematical revision. It directly addresses several objections in the v148 report. In particular, the manuscript now goes beyond the full-factor-invariant coefficient class, introduces a relative common-divisor stratum, computes the exact determinant multiplicity of the pencil relation, upgrades the geometric orbit comparison to an explicitly effective quotient-stack comparison, computes normal directions to the pencil locus, and constructs complete families of determinant-radical relations that break both factor symmetries.

I did not find a new fatal counterexample to the principal all-pencil inverse, the moving-family inverse, the actual source-bundle descent, or the eight new v149 results after checking their stated hypotheses and proof interfaces. The new arguments are materially stronger than the v148 additions.

The rejection therefore does **not** rest on claiming the new mathematics is false.

It rests on three top-four-level defects.

First, the closest named failure-locus predecessor, Ballico 1993, remains unexamined at theorem/proof level. The author correctly records this as unresolved. I independently repeated the exact-title and DOI search on September 24, 2026; I found the Wiley record and issue page, but not an accessible complete theorem/proof text. The six comparison axes therefore remain unresolved.

Second, the headline moduli theorem is less independent than the rhetoric suggests. The pencil relation stratum is defined by recovering the determinant root, choosing the appropriate Cauchy summand, imposing the form L tensor F, and then imposing the Pluecker equations. In other words, the stratum is defined scheme-theoretically to be the intrinsic image of the pencil parameter space. Once that definition is made, the quotient-stack equivalence with the pencil quotient is a correct and useful rigidification statement, but much of its force is formal descent and quotient bookkeeping. The corollary transporting every invariant locally closed pencil locus Q to an effective failure stratum is correspondingly formal transport, not a new classification of pencil degenerations.

Third, the common-divisor enlargement is genuine but still not a classification of a naturally occurring broad boundary problem. The exact-gcd locus is explicitly endowed with its reduced locally closed scheme structure, and the determinant-divisor stratum is then a smooth associated bundle over the determinant orbit. This produces a clean ambient deformation space and non-factor-invariant directions, but it does not determine the natural scheme structure of an intrinsic gcd functor, classify all determinant-radical relation spaces, describe the singularities or orbit closures of a natural compactification, or extract a new invariant or theorem about quadratic pencils that was not already encoded by the chosen image conditions.

Thus v149 has crossed an important threshold from “recognition inside a designed symmetry class” to “a relative deformation framework containing transverse directions.” It has not, in my view, crossed the much higher threshold to a new organizing theorem of general algebraic geometry.

---

## 1. What revision 149 genuinely adds

The v148 report asked for a conceptual enlargement rather than another example. Revision 149 responds with three new mathematical blocks.

### 1.1 Common-divisor strata and relative first-relation algebras

Lemma 6.1 constructs the locus of r-dimensional degree-D subspaces with exact gcd degree g and identifies the reduced locally closed stratum with

P(S_g(E)) × X_{h,r}(E),

where X is the gcd-free open locus.

Theorem 6.3 specializes this to determinant powers and identifies the determinant-divisor stratum with an associated bundle

GL(E) ×^G X,

hence its quotient by GL(E) with [X/G].

Proposition 6.4 then formulates a relative first-relation algebra on a maximal-lower-Hilbert-function stratum using the normalized multiplication trace, rather than the absolute nilradical, and identifies the tangent-identity substitution kernel before passing to the effective first-relation stack.

This is a real upgrade over the v148 orbit-set statement.

### 1.2 Effective all-pencil moduli

Lemma 13.1 identifies the exact common divisor of the pencil first-relation space as det(T)^(n-1), leaving a primitive degree-(3n-4) residual relation of the form L_R tensor F.

Theorem 13.2 defines the intrinsic pencil relation stratum and proves, after the two explicitly stated ineffective quotients, an equivalence

F_pen^eff ≃ [Gr(2, Sym^2 V) / PGL(V)]

over arbitrary complex parameter schemes. It gives the standard tangent complex and carries singular pencils and infinitesimal families.

Corollary 13.3 transports invariant rank/Fitting and spectral loci, with their scheme structures, through this equivalence.

### 1.3 Transverse directions and fixed-support families

Theorem 14.1 computes the normal space to the pencil locus inside the residual Grassmannian as the direct sum of:

1. non-Pluecker directions;
2. directions breaking the full right multiplicity factor inside the same Cauchy summand; and
3. directions entering other Cauchy summands.

Theorem 14.2 then constructs projective Grassmannians through every pencil whose geometric homogeneous radical remains the determinant ideal and which contain lines leaving both factor-invariant classes.

This genuinely answers the v148 criticism that the ambient space should contain and describe deformations outside the coefficient class.

---

## 2. Correctness audit of the universal gcd lemma

The key map

P(S_g(E)) × X_{h,r}(E) → Gr(r,S_D(E)), ([f],J) ↦ fJ

is well defined because multiplication by a nonzero polynomial is injective. The image of the corresponding projective multiplication map is closed. Removing the higher-gcd images gives the exact-gcd locus set-theoretically.

The differential calculation is also convincing. If

dot(f) j + f dot(j) ∈ fJ

for all j in J, then each irreducible factor of f must divide dot(f), since gcd(J)=1. Equality of degrees leaves only the scalar tangent direction, which vanishes projectively, and then dot(J)=0.

Combined with properness, geometric injectivity, and unramifiedness, this gives a closed immersion onto the chosen reduced target. Since the target is reduced and the closed immersion has the same support, the map is an isomorphism.

I do not see a counterexample to this argument.

There is, however, an important conceptual limitation that should be stated more prominently.

The theorem does **not** discover that some independently defined exact-gcd moduli functor is represented by a reduced scheme. The manuscript first defines Z_g by taking the **reduced locally closed scheme structure** on the exact-gcd set and then proves that this chosen reduced structure is the product above. This is legitimate, but it means that the nonreduced structure of a more intrinsic degeneracy locus has not been classified.

The dual-number example correctly shows that fibrewise gcd degree is insufficient. It does not by itself establish that the reduced stratum chosen in Lemma 6.1 is the uniquely natural scheme structure for the broader deformation problem.

This distinction is not a correctness defect. It is important for evaluating how much moduli-theoretic content the theorem carries.

I would also ask for a more explicit reference or sentence justifying the passage from geometric-point injectivity plus the tangent calculation to the precise radicial/unramified hypotheses used in the cited closed-immersion criterion. The intended argument is standard in this characteristic-zero finite-type setting, and I do not regard this as a blocker, but a top-level journal proof should leave no ambiguity at this point.

---

## 3. The determinant-divisor stack theorem is clean but largely built into the stratum

Theorem 6.3 is formally strong and, under the stated definition, correct-looking.

The power map on projective spaces is a closed immersion in characteristic zero. The determinant orbit is the homogeneous space GL(E)/G. Pulling back the universal gcd decomposition along that orbit leaves an unrestricted gcd-free residual subspace. The associated-bundle description and quotient-stack identity then follow by descent.

The tangent complex

[Lie(G) → Hom(J,S_h(E)/J)]

is the standard quotient-stack tangent complex.

What the theorem does **not** do is classify an independently given determinant-radical moduli problem. The determinant-divisor stratum is defined by requiring the exact common divisor line to lie in the determinant-power orbit. Once this is imposed, the residual parameter is deliberately unrestricted. Smoothness then follows because the residual space is an open Grassmannian and G is smooth.

This is useful and honest geometry. It should not be advertised as if a difficult singular moduli space had unexpectedly become smooth. The smoothness is a consequence of the chosen locally closed stratum.

The manuscript mostly respects this boundary, but the abstract-level language “the effective first-relation stack is an explicit smooth quotient” can easily be read as stronger than the construction warrants.

---

## 4. The relative first-relation proposition is a good technical upgrade

Proposition 6.4 is one of the better pieces of v149.

The normalized trace augmentation is an intrinsic way to separate the scalar summand over a nonreduced base. Under the stated Hilbert-function hypotheses, lifting generators of E=N/N^2 gives a surjection from the truncated symmetric algebra. Any relation of least degree below D would contradict the assumed associated-graded isomorphisms. Since N^(D+1)=0, the remaining kernel is exactly the degree-D relation bundle.

Changing generator lifts by N^2 does not change a product of D generators modulo N^(D+1), so the degree-D first relation is intrinsic. The tangent-identity substitutions form the expected smooth affine scheme on Hom(E,N^2), with nonadditive composition law.

I agree with the manuscript that this closes a real gap left by a geometric-point orbit classification.

The main limitation is again scope: the proposition assumes the maximal-lower-Hilbert-function stratum and multiplicativity of the normalized trace. Arbitrary finite-flat deformations of the local algebras are not being classified. The paper states this caveat, and it should remain visible wherever the stack theorem is summarized.

---

## 5. Correctness audit of the exact pencil multiplicity

Lemma 13.1 is a meaningful and apparently correct calculation.

The exterior-duality identity gives the determinant twist

∧^(N-2) Sym^2 H ≃ (det H)^(n-2) ⊗ S_mu H

with mu=(3,...,3,2,0). Including the extra determinant in the failure ideal gives the total factor det(T)^(n-1).

The residual gcd argument is also sound in outline. The right group preserves the coefficient space, so any common divisor has right-invariant zero divisor. Right multiplication is transitive on the invertible locus, hence a proper invariant divisor cannot meet that open orbit. Therefore any divisor is supported on det=0 and is a power of the irreducible determinant.

The rank-(n-1) test excludes an extra determinant factor because S_mu has length n-1 and hence remains nonzero on an appropriate rank-(n-1) map. Irreducibility under the left group ensures that for every nonzero beta some left translate gives a nonvanishing coefficient.

I do not find a fatal defect in this proof.

This exact multiplicity is one of the stronger genuinely mathematical additions in v149. It sharpens the previous “one determinant factor” recovery mechanism and is not merely notational.

---

## 6. The all-pencil stack equivalence is correct-looking but partly tautological

The central theorem deserves the closest editorial scrutiny.

The manuscript defines the pencil relation stratum by the following scheme-theoretic conditions after recovering the determinant root and tensor rulings:

- the primitive residual relation lies in the designated Cauchy summand;
- it has the special form L tensor F;
- L satisfies the Pluecker equations.

These are precisely the equations defining the closed image of the pencil Grassmannian inside the residual relation Grassmannian, together with its transpose copy.

The proof then identifies the ordered residual locus with the pencil Grassmannian, combines the two orderings as the induced G-space G ×^{G°} P, and quotients by G to get [P/G°]. The exact sequence

1 → GL(U) → G° → PGL(V) → 1

then removes the ineffective right factor. Proposition 6.4 removes the nonlinear tangent-identity substitution kernel. After stackification one obtains [P/PGL(V)].

I believe this calculation is correct.

But it is crucial to state what has and has not been proved.

The theorem does **not** begin with a pre-existing natural moduli stack of finite algebras and unexpectedly identify it with the pencil stack. It first restricts to a relation stratum cut out by the precise Cauchy and Pluecker image equations, then rigidifies away the automorphisms known to be invisible to the pencil, and obtains the pencil quotient.

That is a legitimate and useful scheme-level enhancement of the orbit theorem. It is also much closer to “the intrinsic image is equivalent to the source after removing the known kernel” than to an independent Torelli theorem for a naturally defined compactification.

The word **effective** is therefore essential. It must never disappear from the theorem's high-level summaries.

The original algebra stack is not [Gr/PGL]. The paper correctly acknowledges this in Remark 13.4. The nonlinear substitution automorphisms and the full right factor are genuine automorphisms that are deliberately removed.

---

## 7. The deformation statement is stronger than v148, but not an independent deformation classification

The tangent complex

[pgl(V) → Hom(R,Sym^2V/R)]

is exactly what one expects from the quotient stack [Gr/PGL]. The smoothness and stack dimension n-3 are correct.

Likewise, once the equivalence of effective quotient stacks is established, compatible lifting over small Artinian extensions is a formal consequence of smoothness of the Grassmannian and the group.

This is a real improvement over the v148 orbit-set corollary.

However, the manuscript should not present the deformation result as though a new obstruction theory of quadratic pencils had been derived from the finite failure algebras. The deformation theory is transported from the standard smooth pencil quotient through the image equivalence.

The direction of conceptual novelty is therefore:

finite failure algebra retains the standard pencil deformation groupoid after specified rigidifications,

not:

finite failure algebra reveals a new deformation theory of pencils.

That distinction matters for a top-four significance claim.

---

## 8. Corollary 13.3 is almost entirely formal transport

The corollary says that every PGL(V)-invariant locally closed subscheme Q of the pencil Grassmannian gives a corresponding intrinsic effective failure stratum [Q/PGL(V)], preserving its equations and specializations.

This is true once Theorem 13.2 is granted.

But it should not be counted as an independent geometric consequence of the construction. The result simply restricts an equivariant closed immersion and its inverse to Q.

In particular, the statement that rank-incidence and spectral Fitting loci are retained does not classify those loci, determine their components, singularities, closures, or adjacency relations. It says that whatever scheme structure they already have on the pencil side is faithfully copied to the effective failure side.

This is useful functoriality. It is not a new theorem about the geometry of those degenerations.

This point is central to the top-four assessment. The v148 report asked for a consequence saying something new about a natural moduli or degeneration problem for quadratic pencils. V149 now gives a genuine moduli **comparison**, but the displayed specialization consequences remain transported structure rather than new structure.

---

## 9. The transverse normal-space calculation is clean and worthwhile

Theorem 14.1 is one of the clearest new results.

At J=L tensor F, the tangent space to the residual Grassmannian decomposes as

Hom(L,A/L) tensor End(F)  plus  Hom(L tensor F,H_other).

The tangent to P(A) tensor F is the scalar End(F) direction. Splitting End(F)=C·I plus sl(F) produces the second transverse mode.

The normal to the Pluecker Grassmannian inside P(∧^2W) is

Hom(∧^2R, ∧^2(W/R)),

which gives the first transverse mode. The other Cauchy summands give the third.

The group orbit tangent lies inside the pencil tangent, so the same normal quotient survives after passing to the effective quotient stack.

This is a correct and conceptually useful answer to the v148 criticism that factor-invariant recognition did not describe nearby directions leaving the class.

The limitation is that this is still a first-order normal-space calculation inside a deliberately smooth ambient residual Grassmannian. It does not determine orbit closures, singularities of a natural boundary, versal deformation equations of the unrigidified algebra stack, or which transverse directions preserve stronger geometric properties beyond the selected common-divisor condition.

That is enough for a specialized paper. It is not yet a broad boundary theory.

---

## 10. The fixed-support Grassmannians genuinely leave both symmetry classes

Theorem 14.2 is also substantive.

The evaluation map from the invertible locus modulo scalars to P(J*) has image closure of dimension at most n^2-1. Since M>n^2 for n≥3, a general n^2-plane B in J can be chosen with annihilator missing that image. A second open condition gives gcd(B)=1. Hence every M-plane J' containing B has no common zero on the invertible locus and has gcd one.

Therefore the common zero set of det^(n-1) J' is exactly the determinant hypersurface, so the homogeneous radical is (det). The universal family remains finite flat in the prescribed truncated Hilbert stratum.

The explicit projective line obtained by replacing one vector j0 by j0+t eta, with eta in a different Cauchy summand, indeed breaks both full factor symmetries for t nonzero. The Cauchy projection detects this immediately.

I do not see a correctness blocker.

This theorem successfully proves that the new ambient stratum is not merely a reparametrization of the old coefficient class.

But it still falls short of classifying the ambient determinant-radical relations. In fact, the construction emphasizes how enormous that ambient space is. The theorem gives complete subfamilies through every pencil and one explicit symmetry-breaking line, not a geometric classification of the boundary or a natural moduli compactification.

---

## 11. The unresolved Ballico 1993 comparison remains a serious originality problem

The manuscript's literature audit is admirably explicit.

The paper is:

E. Ballico, “On the Failure Locus of Higher Order Properties of Embeddings in Projective Spaces,” Mathematische Nachrichten 163 (1993), 5–13, DOI 10.1002/mana.19931630102.

The v149 audit states that the complete theorem/proof text was not obtained. I independently repeated the exact-title and DOI search. The Wiley landing page and issue entry are available, but the complete theorem/proof text was not exposed through the accessible material I could inspect.

Accordingly, the following remain unverified on the predecessor side:

- the exact objects studied;
- whether nonreduced scheme structure is retained;
- which infinitesimal orders are considered;
- the relative/family hypotheses;
- what markings or ambient data are forgotten;
- whether any inverse reconstruction conclusion appears.

The author correctly refuses to infer nonanticipation from metadata or a first page.

For an ordinary specialized submission, an editor might decide that the present theorem statements are sufficiently distinct to proceed while the literature search continues. For a top-four claim centered on failure loci and infinitesimal reconstruction, I do not think this is acceptable. The closest identified predecessor cannot remain unread at theorem/proof level while the manuscript asks the referee to certify a very high originality threshold.

This remains the clearest concrete item that v149 has not closed.

---

## 12. Why v149 still does not clear the top-four significance threshold

The manuscript's strongest conceptual spine is now:

unmarked finite algebra  
→ intrinsic first relation  
→ exact common divisor  
→ determinant tensor geometry  
→ pencil image equations  
→ effective quotient stack  
→ standard pencil deformation groupoid  
plus transverse directions in a larger determinant-divisor stratum.

This is mathematically coherent and substantially richer than v148.

The remaining question is not whether the chain works. It is what new general principle it establishes.

At present I see three limitations.

### 12.1 The ambient stratum is chosen to be easy

The exact-gcd locus is given the reduced locally closed structure that makes the universal multiplication map an isomorphism. The determinant-divisor locus is then an associated bundle over a homogeneous orbit. Smoothness is consequently built into the setup.

This is a useful coordinate-free parameter space, but not the resolution of a pre-existing singular moduli problem.

### 12.2 The pencil stratum is defined by the pencil image equations

The effective stack equivalence is therefore an exact image/rigidification theorem. It is not an independent identification of a naturally defined algebraic compactification with the pencil stack.

The distinction is especially visible in Corollary 13.3: every invariant pencil locus is retained simply because the equivalence restricts.

### 12.3 The new transverse theory is local or existential rather than classificatory

The normal-space decomposition is first order. The fixed-support Grassmannians exhibit many complete transverse families. Neither result classifies which determinant-radical relations arise, how their orbit closures meet the pencil locus, what the singularity theory of a natural boundary is, or whether the finite failure functor resolves or contracts meaningful strata of a standard pencil compactification.

A top-four version would need one theorem of that scale: a boundary classification, a genuinely new compactification/Torelli statement, a nontrivial deformation-equivalence theorem for a pre-existing natural moduli problem, or an unexpected geometric consequence on the pencil side that is not simply transported through an equivalence whose image was defined by the pencil equations.

---

## 13. The sharp order remains secondary

The sharp uniform order

d=n^2+2n-4

should remain in the paper, but the v149 presentation is right to make it secondary to the inverse and moduli mechanisms.

The lower-order independence is engineered by the first relation appearing in degree d. The deep part is the rigidity of the first relation after all markings are forgotten, not the numerical threshold itself.

The current abstract is better than earlier versions in this respect, although the threshold still occupies more rhetorical space than I would give it in a final general-journal submission.

---

## 14. Reproducibility and proof engineering are excellent, but not a substitute for theorem breadth

The v149 receipt records:

- a 55-page principal article;
- 26 successful regression scripts;
- 50 new exact witnesses;
- preservation of all v148 principal mathematical blocks;
- resolved references and labels;
- source hashes;
- a source-bound commit;
- and explicit statements that computation does not certify universal proofs, historical priority, or journal acceptance.

This is unusually disciplined.

It materially increases confidence that formulas, labels, dimensions, and examples have not drifted between revisions.

It does not alter the main editorial question. Top-four significance is not earned by provenance infrastructure, however good that infrastructure may be.

The manuscript itself understands this. The referee report should preserve the same distinction.

---

## 15. What v149 closes from the v148 report

For clarity, I would record the previous minimum conditions as follows.

### 15.1 Full Ballico 1993 theorem/proof comparison

**Not closed.** The documentary gap is explicitly preserved.

### 15.2 Go beyond full-factor-invariance

**Closed mathematically in a meaningful sense.** The common-divisor stratum and the fixed-support families genuinely contain relations that are invariant under neither full factor group.

This is one of the strongest improvements in v149.

### 15.3 Provide a native pencil moduli/deformation consequence

**Closed literally and technically.** There is now an all-pencil effective quotient-stack equivalence over arbitrary complex parameter schemes, including singular pencils and infinitesimal families.

However, much of this theorem is an image/rigidification equivalence for a stratum defined by the pencil's own Cauchy and Pluecker equations. It therefore closes the requested categorical upgrade more strongly than it closes the requested significance upgrade.

### 15.4 Address stabilizers and nonreduced bases

**Closed on the specified Hilbert and relation strata.** The nonlinear substitution kernel and ineffective right factor are explicitly retained before quotient, and the scheme-level arguments do not substitute geometric fibres for equations over nonreduced bases.

### 15.5 Preserve the hard-won all-pencil and moving inverse

**Closed.** I found no retreat from singular pencils, ungraded algebras, actual source-bundle recovery, or the one-constant-left-map moving theorem.

### 15.6 Produce a top-four-scale independent geometric theorem

**Still not closed.** The new results are substantial, but the central stack and specialization statements remain too close to exact image recognition and formal transport to carry the entire top-four significance case.

---

## 16. Minimum conditions for another top-four evaluation

I would not recommend another top-four review round triggered only by more examples, more computational certificates, or another refinement of the same image equivalence.

A genuinely new round should contain at least the following.

### 16.1 Finish the Ballico 1993 comparison

Obtain the complete article through a legitimate library or document-delivery route and compare theorem by theorem. Give exact theorem numbers, hypotheses, scheme structures, infinitesimal orders, relative statements, forgotten data, and inverse conclusions.

If the paper is unavailable even through institutional channels, document that effort and reframe all historical claims so the novelty case does not depend on an unverified negative statement.

### 16.2 Replace the reduced exact-gcd stratum by a more intrinsic moduli problem, or justify its universality

Either represent a natural exact-common-divisor functor with its genuine scheme structure, or explain why the reduced stratum is the correct canonical moduli object for the deformation theory being claimed.

A result describing nonreduced structure along gcd jumps would be substantially stronger.

### 16.3 Produce a non-formal geometric consequence on the pencil side

The next theorem should not merely restrict the equivalence to a pre-existing invariant locus.

Examples of the appropriate scale would be:

- a classification of a natural boundary stratum or orbit-closure adjacency;
- a new Torelli statement for a standard compactification;
- a description of singularities or normalization of a natural pencil moduli closure;
- a new deformation/obstruction theorem not already equivalent to the smooth Grassmannian quotient;
- or a geometric invariant extracted from the failure algebra that solves an existing pencil problem.

### 16.4 Clarify the status of the effective stack

Use standard rigidification language if possible and state exactly which subgroup stack is removed at each stage. The present quotient-of-morphisms description is understandable, but a canonical universal property would make the result easier to compare with standard moduli constructions.

Most importantly, never conflate the effective stack with the unrigidified algebra stack.

### 16.5 Preserve the successful v149 mathematics

Do not weaken the exact det^(n-1) multiplicity theorem, the nonreduced-base scheme arguments, the all-pencil singular case, the actual source-bundle descent, or the transverse families. These are genuine gains.

---

## 17. Final assessment

Revision 149 is the strongest A2 revision I have reviewed in this sequence.

It answers the previous report with new mathematics rather than cosmetic editing. The universal common-divisor construction, exact pencil multiplicity, relative first-relation algebra, effective stack comparison, normal-space decomposition, and fixed-support symmetry-breaking families form a coherent package. I do not identify a new fatal proof error in those additions.

The paper is therefore no longer well described as merely an engineered encoding theorem with representation-theoretic recognition. It now contains an actual relative deformation framework.

Nevertheless, I still would not recommend it for Annals, Acta, Inventiones, or JAMS in the present form.

The unresolved Ballico 1993 comparison prevents a clean top-level originality assessment against the closest named predecessor. More importantly, the new moduli theorem obtains the standard pencil quotient after restricting to a stratum defined by the pencil image equations and then rigidifying precisely the known ineffective automorphisms. The specialization corollaries are formal restrictions of that equivalence, and the broader common-divisor stratum is a deliberately smooth reduced parameter space rather than a classification of a natural singular boundary problem.

Those results are mathematically serious and potentially strong for a specialized algebraic-geometry or commutative-algebra venue. They do not yet have the independent geometric breadth, inevitability, or organizing force I would expect from a top-four general mathematics paper.

**Recommendation: reject in the present form for a top-four general mathematics journal.**
