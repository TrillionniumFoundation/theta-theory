# Independent harsh referee report on A2 revision 116

**Manuscript:** *Conductor reduction and primary structures of multiplication failure schemes*  
**Repository:** TrillionniumFoundation/theta-theory  
**Reviewed revision branch:** revision/a2-v116-primary-contact-structure-2026-09-22  
**Frozen reviewed head:** fadcfaa11a1939625177eb12e97569b63b7a1a9d  
**Mathematical-source commit recorded by the build receipt:** a02e2d1bfecf9dc2f597e48440257f2d32fc29c4  
**Controlling previous report:** R115 at 1cb4e00c86699247454d21dbec2dcce01a9c6b8b  
**Date:** 22 September 2026

## Referee status and scope

This is an owner-requested, AI-assisted external-referee-style assessment. It is not a report commissioned by Annals of Mathematics, Inventiones Mathematicae, Journal of the American Mathematical Society, Acta Mathematica, or any other journal, and it must not be represented as such.

I reviewed the mathematical source of the primary-contact v116 line, its response to R115, proof audit, literature audit, source/build receipts, and the new conductor/contact sections. I also checked the repository branch topology sufficiently to freeze the object under review. There is a second divergent branch carrying the same version number, revision/a2-v116-higher-product-structure-2026-09-22, whose published head is cbfb78d7451ef9ca9fe694d292fb973f757d9f42. The present report is **not** a review of that divergent manuscript.

I distinguish three questions throughout:

1. whether I found a concrete mathematical contradiction or counterexample;
2. whether the proofs as written meet the standard of a final research article;
3. whether the result is sufficiently new, broad, and important for a general top-four mathematics journal.

These are not the same question.

# Recommendation

## Reject in the present form at a general top-four mathematics journal.

This recommendation is **not** based on a fatal counterexample. Revision 116 is a substantial mathematical improvement over revision 115. In particular, the new conductor reduction and the fixed/moving contact-pencil theorems give a coherent theorem package, and the authors have directly repaired several proof-presentation issues identified in R115.

The reason for rejection is instead that the top-four case is still not established. The new theorem is complete on a carefully engineered but highly structured family, and after the conductor reduction its flagship scheme structure is governed by the power basis of a finite Artin algebra, a confluent Vandermonde/index-form determinant, and a pair-collision normalization. Those are elegant and useful ingredients, but the present paper has not yet shown that their combination produces a structural theorem of the breadth or conceptual depth required for a general top-four venue. The closest historical comparison explicitly remains unresolved, and the manuscript does not yet engage the broader classical literature on primitive elements, index forms, monogenic finite algebras, and discriminant/collision loci at the level required to support its novelty claim.

A strong specialist algebraic-geometry or commutative-algebra submission could be plausible after the scholarly and proof-architecture issues below are repaired. A new top-four attempt would, in my view, require another genuinely structural theorem rather than another layer of exposition, diagnostics, or repository evidence.

# 1. What revision 116 actually adds

The new material is significantly stronger than the v115 hyperplane-only response.

The central chain is now:

- for a length-d divisor D and a generating k-plane A in the restricted series, with n at least 2d-1, the multiplication cokernel for the lifted subseries U_A is identified with the finite-contact multiplication cokernel on D, in families and after arbitrary base change;
- for k=2, a frame converts the finite problem to the power-basis matrix [1,v,...,v^m] in the length-d algebra H^0(O_D);
- for m at least d-1, the zeroth Fitting ideal stabilizes to the determinant of the power basis;
- for D=sum d_i p_i, that determinant is factored exactly into ramification factors with weights binom(d_i,2) and pair-identification factors with weights d_i d_j;
- the resulting fixed-contact divisor receives a complete primary decomposition, corank formula, nilpotency indices, nilradical layers, tangent cones, and singular support;
- after allowing D to move, the total failure divisor is asserted to be integral and to have a smooth finite normalization obtained by marking a scalar length-two subdivisor Z less than or equal to D;
- an explicit differential test is given for singular points of the moving divisor.

This is real progress. It addresses the breadth-versus-depth criticism in R115 much more seriously than another hyperplane refinement would have done.

The manuscript also expands the four hyperplane proofs requested in R115: the plane derivative is made explicit, the residual spanning calculation is written out, the confluent rank-two Hankel radical is isolated, and the equivariant associated-point argument is given precise references. I regard those R115 proof-presentation requests as substantially answered.

# 2. Correctness audit of the new proof spine

I tried to attack the new theorem at the points where a short argument is carrying a large conclusion. I did **not** find a decisive counterexample in the material reviewed.

That statement should not be overread as proof certification. It means that the main reductions are internally plausible after a hostile reading.

## 2.1 Conductor reduction

The basic binary-form multiplication lemma is sound in the stated range: a base-point-free U in V_n contains two coprime degree-n forms, and their syzygy calculation gives U V_t = V_(n+t) for t at least n-1.

The proof of the conductor theorem then uses two separate pieces correctly:

- W_D^2 U_A^(m-2) fills the double-vanishing ideal once 2n-2d is at least n-1;
- H^1(O(n-2d))=0 gives surjectivity from W_D to the first conormal layer, and a unit section of A transports that layer to degree mn.

The local splitting of 0 -> W -> U -> A -> 0 then makes the symmetric-power kernel transparent, and the resulting cokernel comparison is compatible with arbitrary base change because the relevant map is proved to be a surjection of vector bundles.

I therefore do not see an obvious flaw in the conductor reduction as stated.

## 2.2 Fixed-contact determinant and primary weights

Once one is on a frame with A=<a,av>, division by a^m reduces the problem to the Krylov/power-basis matrix [1,v,...,v^m]. Cayley-Hamilton gives stabilization for m at least d-1.

The determinant factorization is also credible. In each local factor C[z_i]/(z_i^(d_i)), the passage from divided derivatives of a polynomial at lambda_i to the coefficients of P(v_i(z_i)) is triangular with diagonal powers of the first jet c_i1. Combining those local determinants with the confluent Vandermonde gives exactly

product_i c_i1^(binom(d_i,2)) times product_(i<j) (lambda_j-lambda_i)^(d_i d_j).

On the framed polynomial chart the factors are distinct prime linear forms. The primary decomposition and absence of embedded primes then follow from unique factorization, and smooth faithful-flat descent can be used to recover the intrinsic statement.

Again, I do not presently have a counterexample.

## 2.3 Coranks and infinitesimal layers

The corank formula is the expected minimal-polynomial computation. The local nilpotency index of v_i-lambda_i is ceil(d_i/e_i); repeated eigenvalues combine by least common multiple, hence by taking the maximum local exponent at each common value. This gives the stated dimension of C[v].

The formula for the nilradical filtration of B/(product f_alpha^(b_alpha)) is also consistent with the colon-ideal calculation in the text. I do not regard this part as a correctness blocker.

## 2.4 Moving divisor and normalization

The incidence with a marked degree-two subdivisor has the local form

g=hq,   v=lambda+h w,

with h monic quadratic. This makes the proposed normalization source visibly smooth on the displayed charts. It is finite over the failure locus because a fixed finite divisor has only finitely many length-two subdivisors. The image is the nonprimitive-element locus: failure of v to generate the finite algebra is equivalent to either identifying two support values or losing the first jet at a multiple support point.

The argument that the hypersurface is generically reduced along its irreducible support, and hence integral, is plausible. The finite birational map from a smooth normal source can therefore be the normalization.

The singular-support criterion derived from the kernel of the normalization differential is also logically plausible, including the Nakayama argument used when there is a unique preimage.

My negative recommendation is therefore not a disguised claim that these results are false.

# 3. The central top-four problem: completeness has been achieved on a designed family, not on a general family

The manuscript repeatedly emphasizes that the contact-pencil family has arbitrarily large codimension. That is true, but it is not the relevant notion of generality.

Every subseries in the new family contains the full conductor space W_D. Equivalently, after quotienting by W_D, the problem is deliberately forced into a two-dimensional generating subspace of a length-d finite algebra. The theorem is therefore complete on the relative family

A in Gr(2,H^0(O_D(n)))^circ,
U_A = res_D^(-1)(A),

not on an unrestricted Grassmannian of subseries of V_n.

This distinction is mathematically substantial. The family is broad in d and in the contact multiplicities, but it is structurally adapted to the reduction that makes the classification possible. Its codimension d-2 can go to infinity simply because the conductor quotient has fixed rank two while d grows.

I do not object to studying such a family. It is natural and interesting. I object to using “arbitrarily large codimension” as a surrogate for a general higher-product classification.

At top-four level, the question is whether the new result reveals a mechanism that governs multiplication failure beyond the locus engineered to admit finite-contact reduction. Revision 116 does not yet show that.

# 4. After conductor reduction, the flagship classification is close to classical primitive-element and discriminant geometry

The manuscript is commendably explicit that power bases, Vandermonde determinants, confluent Vandermonde identities, Fitting ideals, and discriminant identities are classical.

That disclosure sharpens the significance question.

Once Theorem thm:conductor-reduction is granted, the k=2 classification is the geometry of when an element v of a length-d commutative Artin algebra generates that algebra. The stable determinant is the determinant of the power basis

1,v,...,v^(d-1).

Its factorization is an index-form/confluent-Vandermonde computation. Its support is the nonprimitive-element locus. Its normalization marks the elementary obstruction of a scalar length-two quotient. The identity

disc(chi_v)=disc(g) Delta(g,v)^2

makes the discriminant character of the construction especially explicit.

None of this means the theorem is already in the literature in the exact relative multiplication language. I have not established that, and the manuscript has not established it either.

It does mean that the novelty burden is much higher than the current literature section acknowledges.

A top-four submission needs a theorem-level comparison not only with the failure-locus papers already cited, but also with the classical and modern literature on:

- primitive elements and monogenic finite algebras;
- index forms and determinants of power bases;
- discriminant hypersurfaces and their normalizations;
- collision/branch incidences for unordered configurations;
- universal finite algebras and the non-generator locus;
- conductor and Fitting descriptions of finite-algebra multiplication.

The present paper compares carefully with determinantal singularities and selected failure-locus papers, but it does not yet persuade me that the new fixed/moving contact package is conceptually beyond a relative geometric packaging of this classical structure.

For a specialist paper, a clean relative packaging may itself be worthwhile. For a top-four paper, it needs either a much stronger novelty comparison or a theorem whose content is not essentially forced once the finite-algebra reduction is known.

# 5. The unresolved Ballico 1993 comparison is still a publication blocker

The literature audit is unusually honest about this issue. It says that the theorem pages of E. Ballico, *On the Failure Locus of Higher Order Properties of Embeddings in Projective Spaces*, Mathematische Nachrichten 163 (1993), 5–13, DOI 10.1002/mana.19931630102, were not obtained and that the theorem-level comparison remains undetermined.

I independently checked the publisher metadata during this review. Wiley confirms the article, author, volume, pages, year, and DOI. In the source-access environment available for this review, the nominal PDF/ePDF route redirects to the article/abstract interface rather than delivering the theorem pages. I therefore also cannot responsibly state whether the paper anticipates, overlaps, or is disjoint from the present contact theorem.

That is exactly the problem.

For an incremental specialist result, an inaccessible old paper can sometimes be resolved during editorial revision. For a submission whose top-four case depends heavily on having found a new global failure-scheme structure, the nearest historical result cannot remain a blank row in the novelty table.

The manuscript correctly says that failed source access is not evidence of originality. The editorial consequence is that the originality claim is not ready for a top-four decision.

The authors need to obtain the paper through a library, interlibrary loan, author archive, scanned volume, or another legitimate source and compare the actual theorem statements.

# 6. The conductor theorem itself is useful, but its current range looks technically sufficient rather than conceptually sharp

The uniform hypothesis n >= 2d-1 is exactly what makes both of the elementary cohomological/multiplication steps go through.

The manuscript explicitly says that this bound is sufficient and does not claim necessity.

That is acceptable for a supporting lemma. It is less satisfying if the conductor reduction is meant to be one of the paper's principal structural theorems.

The natural questions are not addressed:

- Is 2d-1 sharp for all generating A?
- What is the true threshold as a function of d, k, and m?
- What fails below the threshold: the double-vanishing step, the first normal layer, or only uniformity over the parameter space?
- Can the cokernel comparison hold under weaker regularity hypotheses?
- Is there a cohomological criterion on a general curve or general projective variety that recovers the same reduction?
- Can one characterize exactly when W_D U_A^(m-1)=H^0(I_D(mn))?

A general theorem in terms of regularity/conductor conditions, with P^1 as a sharp corollary, would be much closer to a structural result. The current theorem is elegant, but it is strongly tailored to the binary-form setting.

# 7. The arbitrary-k statement stops exactly where the hard geometry begins

The conductor theorem is stated for arbitrary generating k-planes A. The complete scheme classification is then given only for k=2.

For k=2, the finite multiplication map is controlled by one element v and one minimal polynomial. This is the most monogenic case possible.

For k at least 3, the finite-algebra problem becomes genuinely multigenerator. The failure scheme is no longer the determinant of a single power basis, and the collision geometry should become much richer.

This is precisely where a top-four version of the paper could become transformative.

At present the arbitrary-k theorem transports the problem but does not solve it. The flagship “complete” theorem therefore remains a rank-two quotient theorem.

A substantial k>=3 classification, even in one robust range, would do far more for the significance of the paper than additional diagnostics or refinements of the k=2 primary weights.

# 8. The primary decomposition on multiplicity strata needs a more explicit descent lemma

I am not asserting that Corollary cor:contact-multiplicity-strata is false. I think the stated descent is likely correct.

However, the proof is too compressed relative to the strength of the conclusion.

On the labelled finite etale cover, the factors T_i and E_ij are distinct smooth divisors and the equation is a product of powers. Downstairs, components in the same symmetric-group orbit are identified. When equal multiplicities occur, a single irreducible component downstairs can have several labelled branches upstairs, and those branches meet along braid-type collision loci.

The report should not pass over the following points in one paragraph:

1. the reduced orbit union upstairs is exactly the pullback of a **prime Cartier divisor** downstairs;
2. the indicated power of that downstairs prime pulls back to the product/intersection of the corresponding branch powers upstairs;
3. the stated intersection of powered downstairs prime ideals equals the descended failure ideal;
4. embedded associated primes cannot appear under the quotient/descent;
5. these claims remain valid at intersections of several branches and not only generically.

Faithful flatness checks equality once the correct downstairs ideals are identified, but it does not by itself identify the orbit union with a power of a single prime Cartier ideal.

For a headline theorem claiming complete primary structure on every multiplicity stratum, I would require a standalone descent lemma, preferably formulated for a finite etale Galois cover of a regular base with an invariant weighted hyperplane arrangement.

This is a proof-architecture request, not a detected counterexample.

# 9. The moving normalization theorem is elegant, but the paper must identify what is new relative to classical discriminant incidence geometry

The local normalization formula

g=hq,
v=lambda+h w

is very clean.

It is also exactly the kind of pair-collision incidence one expects for a discriminant/nonprimitive-element hypersurface.

The manuscript should therefore compare the normalization theorem to the established geometry of discriminant hypersurfaces, branch divisors, index forms, and configuration-space quotients.

The current proof demonstrates the theorem internally. It does not establish that the theorem is a new geometric phenomenon.

The strongest genuinely paper-specific content appears to be the fact that the original multiplication-failure Fitting scheme is transported to this finite-algebra discriminant scheme **as a coherent cokernel after arbitrary base change**. That is the part I would emphasize. The normalization and weighted fixed fibres should then be positioned with an exact account of which aspects are classical consequences of the index-form model and which aspects are new consequences in the multiplication problem.

At present these layers are not separated sharply enough for a top-four novelty assessment.

# 10. The singular-support criterion is useful but not, by itself, a top-four leap

Proposition prop:moving-singular-test is one of the more attractive new results. It gives an explicit condition at collisions, rather than only on the reduced-support locus.

The proof via the normalization differential and the equations

h divides q r,
w r mod h is constant

is concise and appears plausible.

However, this is a local criterion for singularity of the specific discriminant hypersurface already described by the normalization. It enriches the k=2 model; it does not broaden the model.

For a top-four submission I would want to know whether this criterion is an instance of a more general deformation theorem, perhaps one that survives for k>=3 or for higher-dimensional conductor quotients. Otherwise it remains a fine structural calculation inside the same monogenic geometry.

# 11. The paper still contains several different papers under one cover

Revision 116 improves the ordering: the new conductor/contact theorem is placed first.

Nevertheless, the complete manuscript still carries:

- the new conductor/contact-pencil theory;
- the older quadratic binary component theorem;
- polar residual tangent theory;
- exact residual matrix germs;
- all-dimensional quadratic component optimization;
- wall geometry;
- two-point higher-product sectors;
- the hyperplane theorem;
- information-recovery/statistical appendices.

The build receipt records a 74-page complete manuscript, a 48-page geometry copy, and a 27-page application copy.

Preservation of old theorems is useful for repository history. It is not automatically good journal architecture.

The new contact theorem does not logically require the older quadratic classification, and the older quadratic classification does not become stronger because it sits next to the contact theorem. The result is still an accreted research program rather than a single mathematically inevitable paper.

A top-four paper should make it immediately clear which theorem is the reason for publication and why the surrounding material is indispensable to that theorem.

If the new contact theorem is the flagship, I would strongly consider a dedicated paper centered on conductor reduction, finite-contact failure schemes, and the moving normalization, with only the minimum residual framework needed for comparison.

# 12. The old incomplete problems remain incomplete

Revision 116 correctly does **not** claim to have solved the old quadratic excess associated-prime problem or the exact primary structure of the old hyperplane scheme.

That honesty is good.

It also means that the previous incompleteness has not disappeared; the paper has moved sideways to a new complete family.

This can be a valid research strategy. It does not automatically answer the top-four objection that the most general-looking families in the article are not fully classified.

In particular:

- the b<a quadratic excess regime still lacks a complete global associated-prime/primary classification;
- the hyperplane theorem still gives only a lower bound for the embedded evaluation-curve nilpotency rather than the exact primary ideal;
- the arbitrary-beta polar theory remains primarily a deformation formalism rather than a global classification.

The new contact family is complete, but it does not unify these older families.

# 13. “Arbitrarily large codimension” should not be used as a significance proxy

The abstract and response emphasize that contact pencils produce subseries of arbitrarily large codimension d-2.

This is formally correct.

But the complexity of the quotient remains two-dimensional. The classification becomes possible because every such subseries contains W_D and is represented by a pencil in the finite quotient.

Thus the parameter d increases the amount of contact data while keeping the algebraic generator problem monogenic.

A reader could otherwise come away with the impression that the paper solves a genuinely high-rank arbitrary-codimension multiplication problem. It does not.

I recommend rewriting the significance language around the actual content:

> a uniform family of conductor-containing subseries with unbounded ambient codimension but rank-two finite quotient.

That statement is accurate and still interesting.

# 14. Repository identity is currently unsuitable for a formal submission

There are two divergent branches both labelled A2 v116:

- revision/a2-v116-higher-product-structure-2026-09-22, published head cbfb78d7451ef9ca9fe694d292fb973f757d9f42;
- revision/a2-v116-primary-contact-structure-2026-09-22, reviewed here at head fadcfaa11a1939625177eb12e97569b63b7a1a9d.

They diverge from the same R115 review base and contain different mathematical centers.

This is not merely cosmetic. A referee, editor, or later reader who is told to inspect “A2 v116” does not have a unique object.

The later timestamp of the present branch is enough for me to identify the owner's latest revision in this review session. It is **not** an acceptable long-term versioning rule for a journal submission.

Before any external submission, the authors should:

1. give the two lines different version numbers;
2. declare one immutable submission head;
3. provide a one-page manifest identifying the mathematical-source commit and generated-PDF commit;
4. avoid reusing the same version label for divergent mathematical manuscripts.

The present report is pinned to fadcfaa11a1939625177eb12e97569b63b7a1a9d precisely to remove that ambiguity.

# 15. The verification package is good repository practice, but it does not alter the mathematical recommendation

The build/source records are much better than in early revisions. The reviewed branch records:

- the mathematical-source commit separately from the generated build commit;
- three successful PDF builds with no undefined references or duplicate labels;
- source preservation hashes;
- inherited diagnostic reruns;
- new finite checks for conductor ranks, determinant identities, normalization examples, and colon exponents.

The repository also repeatedly states that these are not proof certification.

I agree.

These checks are valuable for reproducibility and regression control. They do not increase the novelty of the theorem and they cannot validate universal algebraic-geometric claims.

I therefore treat the engineering/provenance side as satisfactory for review, aside from the duplicate-v116 identity problem.

# 16. What would materially change the top-four assessment

More polishing will not change my recommendation. Another genuinely structural theorem could.

I see several possible routes.

## Route A: leave the conductor-containing locus

Prove a higher-product component or primary-structure theorem on a substantial open class in an unrestricted Grassmannian Gr(c,V_n), rather than on subseries forced to contain W_D.

This would demonstrate that the contact theorem captures a mechanism of the ambient multiplication problem rather than a complete model family.

## Route B: solve a multigenerator finite-contact problem

Use the arbitrary-k conductor theorem to classify a nontrivial k>=3 family of finite-contact multiplication failure schemes, including components and scheme structure.

This would move the theory beyond the power-basis/minimal-polynomial case.

## Route C: formulate a general conductor/regularity theorem

Replace the numerical P^1 bound by a structural condition on a projective variety, curve, or line bundle that guarantees coherent-cokernel reduction to a finite contact scheme.

Then prove that the resulting finite-contact geometry has consequences in more than one genuinely different family.

## Route D: complete one of the old principal schemes

Give a complete associated-prime or primary theorem in the unrestricted quadratic excess regime, or determine the exact embedded primary structure of the hyperplane family.

Either would strengthen the global claim of the existing paper.

## Route E: turn the moving contact theorem into a broader discriminant theorem

Develop the universal non-generator locus for finite algebras in a way that contains the current pair-collision normalization as the rank-two case and produces new geometry for higher generator rank or more general finite algebras.

That could convert what currently looks like a classical discriminant incidence into a new structural theory.

I would not require all of these. I would require at least one advance of this kind before reconsidering the work at a general top-four venue.

# 17. Mandatory revisions independent of venue

Even for a specialist submission, I would require the following.

### E116.1 — Freeze a unique manuscript identity

Rename or renumber the divergent v116 branches and identify one immutable submission head.

### E116.2 — Complete the Ballico 1993 theorem-level comparison

Obtain the actual theorem pages and provide a result-by-result comparison. Do not infer originality from failed access.

### E116.3 — Add the missing primitive-element/index-form/discriminant literature audit

The new flagship theorem should be compared with the literature naturally suggested by the power-basis determinant and discriminant identity, not only with prior “failure locus” papers.

### E116.4 — Isolate and prove the etale descent lemma for primary components

Give a precise lemma covering orbit components, powers, intersections, associated primes, and braid intersections on the multiplicity strata.

### E116.5 — State the exact novelty boundary of the moving normalization

Separate what follows formally from the classical index-form/discriminant model from what is genuinely new because of the multiplication-cokernel transport.

### E116.6 — Reframe the scope language

Make explicit, already in the abstract and first theorem paragraph, that the complete classification is for conductor-containing subseries with rank-two finite quotient. “Arbitrarily large codimension” should not be allowed to suggest unrestricted high-rank generality.

### E116.7 — Decide the article identity

Either make the contact theorem the paper and move historically accumulated independent material elsewhere, or explain a non-rhetorical theorem-level dependency that makes the quadratic, polar, hyperplane, and contact theories one paper.

### E116.8 — Clarify the status of the threshold n >= 2d-1

At minimum, provide examples showing what can fail below the bound. Preferably formulate the sharp or structural hypothesis.

# 18. Smaller mathematical and expository requests

1. In the contact-main theorem, state explicitly in the headline theorem what happens for 2 <= m < d-1: the zeroth Fitting ideal is zero and the entire parameter space is the failure scheme. This avoids making “every degree” sound as if every degree has a nontrivial divisor classification.

2. When descending components from the labelled cover, distinguish irreducibility from smoothness and geometric unibranchedness at every use, not only in one sentence at the end of the corollary.

3. The phrase “complete primary decomposition” should always carry its base in the same sentence: fixed D, or a fixed multiplicity stratum, or the moving total divisor. The paper contains several different schemes whose primary behavior is very different.

4. The discriminant identity deserves to appear earlier in the conceptual discussion because it makes the classical algebraic nature of the stable determinant transparent.

5. The paper should explain whether Delta(g,v) is literally the classical index form in the chosen monogenic presentation and, if terminology differs, why.

6. The singularity criterion should be accompanied by a few systematically classified collision types, not only one worked d=4 example, if it is intended as a major theorem rather than an effective test.

7. The geometry article should contain a compact dependency diagram. The current complete manuscript still requires the reader to distinguish new contact theorems from inherited quadratic/hyperplane theorems scattered over many sections.

8. Keep the applications logically separate. Revision 116 does this better than earlier versions; it should remain that way.

# 19. Assessment relative to R115

R115 asked for a stronger mathematical center. Revision 116 has supplied one.

I therefore withdraw the specific R115 criticism that the paper has only a broad formalism plus one complete hyperplane family.

The current paper now has a complete nontrivial family with unbounded ambient codimension, exact primary weights, moving collisions, and a normalization theorem.

However, the new result exposes a different issue: the complete family becomes a rank-two finite-algebra primitive-element problem after a relatively short conductor reduction. The stronger the authors make the exact power-basis/discriminant description, the more important it becomes to establish which part of that description is genuinely new and which part is classical finite-algebra/discriminant geometry transported into the multiplication setting.

Thus the objection has changed. It is no longer “the paper has no complete higher-product family.” It is now “the complete family is not yet shown to carry top-four-level novelty beyond its reduction to a classical algebraic model.”

That is meaningful progress, but not closure.

# 20. Final recommendation

Revision 116 is the strongest version of this A2 line that I have reviewed. The conductor reduction is clean, the fixed-contact primary formula is exact, the moving normalization is elegant, the previous hyperplane proof gaps have been expanded, and the repository evidence is unusually careful.

I nevertheless recommend **rejection in the present form at a general top-four mathematics journal**.

The decisive reasons are:

- the complete theorem is confined to conductor-containing subseries with rank-two finite quotient;
- after reduction, the main scheme is governed by classical-looking power-basis/index-form and discriminant geometry;
- the manuscript does not yet contain the literature comparison needed to establish novelty of that package;
- the nearest historical Ballico 1993 comparison remains explicitly unresolved;
- the arbitrary-k reduction is not followed by a genuinely multigenerator classification;
- the old unrestricted quadratic and hyperplane primary problems remain incomplete;
- the multiplicity-stratum primary descent deserves a standalone rigorous lemma;
- and the repository currently contains two divergent manuscripts both called v116.

I found no fatal counterexample to the new main theorem in this review. My recommendation is therefore a judgment about venue-level novelty, breadth, conceptual depth, scholarly priority, and final proof architecture—not a claim that the central statements are false.

A specialist submission could become compelling after E116.1–E116.8 are addressed. A renewed top-four submission should add one genuinely structural theorem of the kind listed in Section 16, not merely another round of local refinements or verification receipts.
