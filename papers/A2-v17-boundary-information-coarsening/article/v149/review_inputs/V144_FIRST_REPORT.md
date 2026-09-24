# Independent harsh referee report — A2 revision 144

## Manuscript and immutable review object

**Manuscript:** *Finite failure schemes and the reconstruction of quadratic pencils*  
**Author:** Qian Qi  
**Revision reviewed:** A2 revision 144  
**Revision branch:** revision/a2-v144-referee-integrated-reconstruction-2026-09-24  
**Immutable mathematical source:** fb4e7c4d00167e422fdb7ee73876a74f6649fb68  
**Immediate mathematical predecessor:** 40ef003998cbeb20f418e1b5e0dcfa9cfef9416d (v143)  
**Controlling earlier referee report:** 3afecca5e65d7fe9c6784020ea6e813122938140  
**Native build run recorded by v144:** 35944289750  
**Review standard:** an external-referee-style assessment at the level of *Annals of Mathematics*, *Acta Mathematica*, *Inventiones Mathematicae*, or *Journal of the AMS*.

This is an owner-requested, AI-assisted independent referee-style report. It is not a journal-commissioned editorial decision.

The exact source SHA above, rather than the movable branch name, is the mathematical object assessed here. The branch also contains source-bound PDFs and build receipts. The recorded v144 objects have 33 pages in the principal article, 102 pages in the supplement, and 130 pages in the complete compilation. The receipt records twenty executed exact/symbolic scripts and 415 current mathematical labels. Those facts are useful provenance and regression evidence; they are not formal verification of the proofs.

I read the principal reconstruction chain in detail: the intrinsic tensor rulings, coefficient principle, all-pencil reconstruction, exact finite-neighbourhood theorem, universal relative neighbourhood, spectral readout and fixed spectral strata, reconstructed critical correspondence, and the new v144 projective critical divisor/ramification section. I also checked the current literature audit, source lock, issue matrix, response to the previous referee, the relevant operator dictionary/Jacobian–Casimir supporting material, and the previous second-v141 report. I independently checked the published formulation of Fevola–Mandelshtam–Sturmfels Conjecture 4.5. I did not formally verify every inherited theorem in the 102-page supplement, and the repository's scripts do not do so either.

## Recommendation

**Reject in the present form for a general top-four mathematics journal, while inviting a genuinely fresh evaluation after the remaining priority and publication-object blockers are resolved.**

This recommendation is narrower than the earlier negative assessments. I do **not** find a new fatal mathematical defect in the main v144 reconstruction–spectral–critical chain. In particular, after a line-by-line audit of the new projective critical divisor argument, I find the finite-flat continuation, the scheme-theoretic elimination of the radial variable, the ramification/Hessian identification, and the length-three collision example internally coherent at the advertised level.

The present top-four blocker is therefore not “the new theorem is false.” It is that the paper still asks an editor and referee to certify a central novelty boundary that the authors themselves correctly mark as unresolved: the closest identified historical failure-locus paper, Ballico 1993, has still not been compared at theorem level. For a manuscript whose flagship object is precisely a nonreduced multiplication-failure scheme, that is not a cosmetic bibliography issue.

A second, now less severe but still important problem is the definition of the publication object. Revision 144 has finally produced a coherent 33-page principal spine, but it still keeps a 102-page supplement containing substantial web, contraction, K3, polar, and boundary theories as fully active parts of the same 130-page submission. Many of those results are not logical inputs to the pencil theorem. A top-four submission cannot simultaneously claim that these theories are merely supporting and require the referee to certify them all as part of one enormous mathematical object without a much sharper scope decision.

The all-rank exterior contraction theorem also still lacks exhaustive map-specific historical clearance. This is no longer fatal to the **pencil** theorem because v144 now correctly demotes it to a supporting web branch, but it remains a problem if the complete submission continues to present that theorem as an independent broad novelty pillar.

## 1. Revision 144 is a real improvement, not an incremental packaging change

The strongest positive change is architectural.

The principal article now has a recognizable theorem chain:

1. an abstract order-d failure neighbourhood recovers the pencil;
2. the first relation space gives a closed immersion of the full pencil parameter scheme;
3. the universal order-d neighbourhood glues and commutes with arbitrary complex base change;
4. on the regular locus, the reconstructed pencil recovers the spectral torsion sheaf and its Fitting incidence schemes;
5. the reconstructed pencil defines the reciprocal critical correspondence;
6. v144 extends the critical scheme from the discriminant-inverted affine picture to a projective finite-flat divisor through critical collisions, with ramification and trace discriminant.

This is materially more convincing than the earlier manuscript architecture, where several theorem clusters competed for top billing. The new Section on the finite flat critical divisor is not an unrelated result appended for prestige: it continues the same spectral/critical chain and resolves a genuine limitation of the earlier affine etale description.

The source/provenance routing is also much cleaner than in the v141 state. CURRENT_REVIEW_ENTRY.md, SOURCE_LOCK_V144.json, ISSUE_MATRIX.json, the response, and the build receipt all identify the same current revision and controlling report. The stale-routing objection in the second v141 report is therefore closed.

## 2. The finite-neighbourhood theorem remains the strongest mathematical core

Let N=binom(n+1,2), p=N-2, and d=n+2p=n^2+2n-4. In graph coordinates near the socle Grassmannian the manuscript obtains the exact homogeneous failure ideal

I_R = (det T) I_p(gamma_R Sym^2 T).

Every generator has degree d. This alone explains why nothing can depend on the pencil below degree d, but it does **not** by itself prove intrinsic reconstruction. The paper now keeps that distinction clear.

The nontrivial part is the passage from the **unmarked abstract finite scheme** Z_R^[d] to the full coefficient datum. The argument proceeds through:

- the intrinsic reduction B;
- the nilradical and its degree-one quotient;
- recovery of the degree-d first-relation kernel from multiplication in the finite scheme;
- reconstruction of the whole homogeneous normal-cone algebra because the ideal is generated in one degree;
- recovery of the determinant cone and its rank-one geometry;
- intrinsic orientation of its two rulings by projective triviality over B;
- constancy of the induced PGL(V)-map because B is connected projective with H^0(O_B)=C;
- ideal quotient by the determinant factor;
- irreducibility of the exterior coefficient representation for pencils;
- exterior duality recovering the Pluecker line of R.

I rechecked the most vulnerable-looking step: whether the finite truncation really contains enough information to reconstruct the complete normal cone. In the present homogeneous one-degree setting, the lemma does what is required. The reduction is B, the nilradical is the truncated zero-section ideal, multiplication recovers the kernel in degree d, and there are no further independent generators. I do not see a hidden use of an ambient marking at this stage.

Likewise, the fixed-coordinate map from Gr(2,Sym^2 V) to the Grassmannian of first relation spaces is genuinely scheme-theoretic. The factorization through the Pluecker embedding, the line-times-fixed-space Grassmannian embedding, and one fixed coefficient inclusion is enough to give a closed immersion and therefore separation of nonreduced parameter schemes.

These are serious results. The exact numerical order d is not, by itself, the conceptual contribution; the conceptual content is that an unmarked finite neighbourhood intrinsically recovers the coefficient line and hence the pencil.

## 3. The universal relative neighbourhood is now at the correct level

The universal theorem is stronger than a fibrewise flat-algebra calculation.

The manuscript works over the pencil Grassmannian P, its relative socle Grassmannian B, and the actual graph neighbourhood. The first relation bundle is constructed by a coordinate-free morphism involving the determinant factors, det(S)^*, and wedge^p Sym^2(U). Locally this is the fixed coefficient inclusion already proved injective. The local degree-d ideals glue under changes of the tautological frame, and quotienting by the (d+1)-st power of the actual zero-section ideal identifies the resulting algebra with the **actual ideal-adic neighbourhood** in the multiplication-failure scheme.

This addresses the relative-gluing concern from the older reviews. The statement also correctly distinguishes the specified relative socle ideal from the absolute nilradical after nonreduced base change.

I do not regard relative gluing or arbitrary complex base change as an open blocker.

## 4. Spectral reconstruction and fixed-discriminant specializations remain convincing

The spectral sheaf argument is now self-contained enough for the role it plays.

On an affine spectral chart, coker(zA-B) is identified with the finite C[z]-module on which z acts by A^{-1}B. Thus sheaf isomorphism is similarity. The polynomial square-root lemma for an invertible complex operator then supplies the missing bridge from similarity of the self-adjoint operator to simultaneous congruence of the symmetric pair. This is a genuinely complex argument; the manuscript is right not to advertise it as a field-free statement.

The truncated spectral presentation

coker(wI-X) tensor D[w]/(w^a) ≅ coker(X^a)

is also the correct way to package the higher local length data over arbitrary coefficient rings. It makes the scheme-theoretic Fitting incidence loci base-change compatible without diagonalizing and without dividing by eigenvalue differences.

The four-dimensional rank-preserving specialization remains a good stress test. It keeps the full discriminant and every **reduced** rank locus fixed while changing the elementary-divisor partition from (3,1) to (2,2). The qualifier “reduced” is indispensable and is now retained consistently. The flatness asserted is the flatness of the finite neighbourhood family, not of every auxiliary reciprocal curve or the unrestricted full failure scheme.

The fixed-discriminant classification in terms of self-adjoint nilpotent orbits is consistent with the standard orthogonal symmetric-space classification: nilpotent symmetric orbits are indexed by all partitions, and the manuscript uses the classical dominance closure order rather than presenting it as a new classification.

## 5. The v143 critical correspondence is now conceptually connected to the inverse theorem

One of the earlier architectural weaknesses was that the reciprocal-likelihood theorem could look like an independent one-variable exercise placed next to the reconstruction theorem.

Revision 144 improves the connection. The paper now separates three assertions cleanly:

- the unmarked finite neighbourhood recovers the complex pencil;
- the pencil functorially determines its universal score scheme and therefore its critical correspondence;
- additional real definite structure and a specially chosen data open give the all-real etale cover.

That is the correct hierarchy. The finite-failure invariant does not magically infer a real form, definiteness, or a data matrix. Those are extra inputs, and the paper says so.

I independently checked the published Fevola–Mandelshtam–Sturmfels formulation. Their Corollary 4.4 gives reciprocal ML degree 2r-3 for a pencil with r distinct eigenvalues, and Conjecture 4.5 asks for real data producing 2r-3 distinct real critical points. The theorem retained here addresses precisely that existence problem and strengthens it by producing a nonempty open set with nondegenerate, globally labelled real critical sections. This is a legitimate external theorem, not merely a reinterpretation of the internal invariant.

That said, proving a published conjecture does not by itself prove first priority over every later or parallel source. The manuscript appropriately avoids claiming an exhaustive historical search.

## 6. Detailed audit of the new v144 projective critical divisor

This is the main mathematical addition in the present revision.

### 6.1 The correct base open is used

The manuscript fixes split semisimple spectral data with pairwise distinct spectral values alpha_i and a binary polynomial Q_h whose projective roots are simple and disjoint from the spectral poles. Crucially, it does **not** invert the discriminant of the score polynomial G. Hence the base still contains critical-point collisions.

This scope is important. The theorem is not a global statement over arbitrary data matrices or over nonsemisimple spectral data. It is a finite-flat theorem on a specified spectral-data open. The current wording is appropriately explicit about this.

### 6.2 The projective score form is the right invariant object

The one-form

omega = sum_i (n-m_i) d log L_i - n d log Q_h

has total projective weight zero because sum_i(n-m_i)=n(r-1). Writing its numerator as

eta = G(x,y)(x dy - y dx)

therefore produces a binary score form G of degree 2r-3. This is the correct projective replacement for the affine polynomial F whose leading coefficient can vanish and whose degree can drop in a chosen chart.

The affine relation G(1,-t)=-F(t) agrees with the earlier score polynomial.

### 6.3 Disjointness from poles is proved scheme-theoretically enough

At each spectral pole L_i=0 the logarithmic residue is n-m_i, and at each root of Q_h it is -n. These are nonzero in characteristic zero. Since all poles are simple and disjoint on the chosen base, G does not vanish at a pole in any geometric fibre.

The manuscript then uses the fact that a nonempty intersection would have a geometric point in some fibre. There is no hidden “nilpotent-only intersection with empty support” to worry about: a nonempty scheme has nonempty underlying topological support. I therefore accept the scheme-disjointness step.

### 6.4 The finite-flat argument survives nonreduced bases

At a point of the base, one chooses a constant rational point of P^1 outside the finite zero set of the fibre of G. Because every residue field has characteristic zero, it contains the prime field Q, and there are infinitely many such rational points. After shrinking the base, evaluation of G at that point is a unit. A constant projective coordinate change sends it to infinity, and G becomes a degree-(2r-3) polynomial with unit leading coefficient.

The local critical algebra is therefore monic and free on 1,t,...,t^(2r-4). These opens cover the base, giving finite local freeness of degree 2r-3. This is an elementary and adequate argument. It also explains why flatness is robust through collisions.

A small exposition improvement would be to spell out the “prime-field rational point” sentence just given. As written, “such a point exists since the residue field has characteristic zero” is correct but slightly compressed.

### 6.5 The identification with the original two-score scheme is stronger than a point count

The proof next writes K=lambda K_0(t). The radial score is

(-n lambda + U_0)/lambda^2,

so the critical ring imposes lambda=U_0/n and makes U_0 a unit. Eliminating lambda from the tangential score gives exactly omega. Since the projective divisor is already disjoint from D_h Q_h, every denominator used in the elimination is a unit on the critical algebra.

This gives inverse coordinate-ring maps, not just a bijection on closed points. The radial reconstruction

K = (U(K_0)/n) K_0

is invariant under rescaling K_0 and therefore glues across projective charts. I find this part of the proof particularly important because it closes the most obvious loophole: a projective score divisor could otherwise have acquired spurious nilpotent structure or omitted an affine chart.

I do not see such a gap here.

## 7. Ramification, Hessian degeneracy, and trace discriminant

The local monic presentation A=O[t]/(g) gives

Omega_{A/O} = A dt/(g' dt),

so the ramification Fitting ideal is (g').

In the local score coordinates (lambda,t), the radial Hessian entry is a unit after imposing the radial score. The Schur-complement factor is the derivative of the eliminated tangential score. Because that score is a unit times g, its derivative modulo (g) is a unit times g'. Thus the determinant of the full score Hessian generates the same ideal as Fitt_0 Omega.

This is the right scheme-theoretic statement. At a critical scheme, second-derivative correction terms under coordinate change are multiples of first derivatives and hence vanish in the critical quotient; the determinant changes by a square of a Jacobian unit. The paper states the corresponding invariant conclusion, though adding this one sentence explicitly would improve the proof for readers sensitive to nilpotents.

The trace-discriminant assertion is also standard and correctly scoped. For a monic algebra the determinant of the trace pairing is the polynomial discriminant, and projective coordinate changes only alter the binary discriminant by a unit. The paper explicitly does **not** identify the trace-discriminant divisor with an arbitrarily scheme-theoretic image of the ramification scheme. That caveat should remain.

I found no mathematical reason to reject this theorem in its present local-algebra form.

## 8. The triple collision is a useful nontrivial test

For

A=I_3, B=diag(-1,0,1),
S_c=diag((1+c)/2,-c,(1+c)/2),

the manuscript obtains

D(t)=t(t^2-1), Q(t)=t^2+c,
F(t)=-(6c+4)t^2+2c.

The projective cubic is

Fhat(T,Z)=-(6c+4)T^2 Z+2c Z^3.

At c=-2/3 this becomes a nonzero scalar times Z^3, so the critical divisor is a length-three scheme supported at the projective direction Z=0. In the local coordinate u=Z/T the algebra is C[u]/(u^3). The radial reconstruction sends the reduced direction to I_3/3. The binary cubic discriminant is a unit times c(3c+2)^3, and c is a unit on the stated base, giving the claimed trace-discriminant multiplicity.

I independently recomputed these identities and found them consistent.

This example is more than decorative: it confirms that the projective family is genuinely retaining nonreduced collision structure rather than merely compactifying a generic root count.

## 9. The principal article is now much more coherent, but the complete submission is still overextended

The principal article has improved substantially. A 33-page article centered on the inverse theorem and its spectral/critical continuation is a plausible object for serious evaluation.

The problem is that the repository still defines the complete mathematical submission as a 130-page object with a 102-page supplement. The supplement retains, with full proofs, theorem clusters on:

- four-dimensional webs;
- an all-rank exterior contraction operator and exact Jacobian–Casimir identities;
- polarized and polar constructions;
- K3-related geometry;
- large boundary and primary-structure atlases;
- further global and degeneration results.

The build receipt says 282 inherited mathematical blocks remain active. That is not a technical appendix in the ordinary sense. It is several substantial research programs attached to one principal paper.

This creates a top-four reviewability problem even if every statement is correct. If those results are independent of the principal pencil theorem, the referee should not be forced to certify them as part of the same submission merely because the repository preserves them. If they are logically necessary, the principal article should say exactly where they enter; at present, it correctly says many of them do **not** enter.

My recommendation is not to delete mathematics. It is to make a publication-object decision:

- either split the independent web/operator/K3/boundary clusters into companion papers or a clearly non-submitted research archive;
- or provide a convincing theorem-level reason why they are one theorem package and give the referee a realistic dependency map.

Revision 144 has fixed the **principal narrative** more than the **complete-submission scope**.

## 10. Ballico 1993 remains the decisive top-four blocker

The manuscript itself identifies the directly relevant source:

E. Ballico, *On the Failure Locus of Higher Order Properties of Embeddings in Projective Spaces*, Math. Nachr. 163 (1993), 5–13, DOI 10.1002/mana.19931630102.

The v144 literature audit is appropriately honest: the complete theorem text has not been obtained, and the six requested comparison axes remain “full text required.” The 1996 Ballico paper is separately inspected and compared, but it cannot substitute for the 1993 paper.

I independently confirmed the 1993 bibliographic record, but I did not obtain its theorem/proof text through the accessible publisher route used in this review. I therefore make neither an anticipation nor a nonanticipation claim.

For this manuscript, that uncertainty is not peripheral.

The headline theorem reconstructs a quadratic pencil from the nonreduced infinitesimal structure of a multiplication-**failure scheme**. The closest already-identified predecessor has “Failure Locus of Higher Order Properties” in its title. A general top-four journal should not be asked to certify that the central inverse/failure construction crosses a major novelty threshold before the closest known historical source has actually been read.

The required comparison should be theorem-level and should state, for Ballico 1993:

1. the parameter space being varied;
2. the exact multiplication/evaluation map;
3. whether the construction is set-theoretic, reduced, Fitting-theoretic, or fully scheme-theoretic;
4. whether nonreduced infinitesimal neighbourhoods or nilpotents are retained;
5. whether any relative/base-change statement is proved;
6. whether any inverse/reconstruction theorem recovers the original linear system or map.

The paper should give theorem numbers, hypotheses, and conclusions, not a title-level or citation-chain inference.

If the 1993 paper has no inverse theorem, no unmarked reconstruction, and no comparable nilpotent neighbourhood statement, that will materially strengthen the present paper's top-four case. If it does contain a closer construction, the novelty statement must be redrawn around the exact additional step proved here. Either outcome is better than leaving the comparison open.

Until that work is done, I would not recommend acceptance.

## 11. The contraction theorem's historical status is still open, but its editorial role has improved

The supplement retains the all-dimensional operator

kappa_{n,q}=iota_q j_n

and proves a precise kernel theorem, a mixed Jacobian–contraction identity, an angular-Casimir composite, and singular values under a specified metric.

Revision 144/v143 has improved the literature positioning substantially. The equality-level operator dictionary now separates:

- classical harmonic decomposition;
- classical multiplication/differentiation adjunctions;
- representation decompositions of exterior powers of Sym^2;
- the exact normalized exterior map used here.

The paper also explicitly says that the inspected sources do not establish exhaustive historical priority for the restricted operator identity.

That honesty matters.

For the **principal pencil reconstruction theorem**, I no longer regard this unresolved operator-priority question as a fatal blocker, because the manuscript now clearly states that the contraction theorem is a supporting theorem for the web branch and is not an input to the pencil proof.

However, if the complete 130-page submission continues to treat the all-rank operator theorem as an independent broad novelty claim, then the map-specific historical comparison still needs to be completed. The authors cannot have it both ways: a result cannot be simultaneously “only a supporting calculation, irrelevant to the main theorem” when asked about priority and “a major all-dimensional novelty pillar” when arguing significance.

The current principal article mostly avoids that inconsistency. The complete submission still needs a scope decision.

## 12. Build evidence is excellent engineering, not mathematical certification

The v144 source discipline is strong.

The repository records:

- the immutable mathematical source SHA;
- byte-identical inherited mathematical files;
- preservation of inherited theorem/proof/equation blocks;
- three native PDFs;
- twenty executed scripts;
- source and predecessor hashes;
- no duplicate labels or unresolved references in the recorded builds;
- exact regression checks for the newly added projective algebra.

This is unusually careful and makes the manuscript much easier to audit.

It proves none of the following:

- that every one of the 415 labelled mathematical assertions is correct;
- that the intrinsic reconstruction has no conceptual gap outside the tested identities;
- that historical priority is closed;
- that the paper meets a top-four significance threshold.

The current README and receipt explicitly acknowledge this limitation. That language should remain.

## 13. Specific comments that should be addressed even if the main blockers are closed

### 13.1 State the projective-critical base open every time the theorem is summarized

The v144 finite-flat critical divisor requires split semisimple spectral data, pairwise distinct spectral poles, simple projective roots of Q_h, and disjointness between those roots and the poles.

The important strength is that the **score discriminant is not inverted**, so critical collisions remain. The theorem should never be abbreviated to “the critical scheme is finite flat for arbitrary data.”

### 13.2 Keep regularity separate from the all-pencil inverse theorem

The finite reconstruction theorem includes singular pencils. Spectral torsion and the reciprocal critical correspondence require regularity, and the v144 projective divisor uses a still smaller split-semisimple data open. These domains are correctly separated in the current source and must remain so in abstracts and talks.

### 13.3 Keep framed families separate from unmarked moduli claims

The abstract order-d reconstruction is unmarked. The parameter closed immersion, universal classifying map, and certain relative constructions use a fixed tensor presentation or a framed first-relation family. The paper repeatedly disclaims an equivalence of unmarked moduli stacks. Do not weaken those disclaimers.

### 13.4 Clarify the coordinate invariance of the Hessian ideal in the nonreduced setting

The proof is essentially correct, but one sentence should note that at the critical quotient the terms involving first derivatives vanish, so the Hessian transforms by J^t H J and its determinant by a square of a unit. This would remove an avoidable referee question.

### 13.5 Slightly expand the rational-point step in the finite-flat proof

Explain that a characteristic-zero residue field contains Q, so a nonzero degree-(2r-3) binary form cannot vanish at every Q-rational point of P^1. This makes the existence of the constant section completely transparent.

### 13.6 Do not call regression checks “exact proofs”

“Exact regression” is good language for symbolic identities and finite computations. It should not be allowed to blur into “formal verification” of a geometric proof. The current source lock is appropriately cautious.

## 14. Status of the major objections from the second v141 report

My present assessment is:

### Closed or substantially closed

**Native source/review routing:** closed. The current source lock and canonical review entry are coherent.

**Relative gluing of actual finite neighbourhoods:** closed at the advertised level.

**Spectral sheaf/similarity and polynomial square roots:** closed.

**Scheme-theoretic spectral readout:** closed at the advertised level.

**Real reciprocal-likelihood existence theorem:** mathematically substantive and properly connected to the reconstructed critical correspondence.

**Principal-paper architecture:** substantially improved. The 33-page main article now has one recognizable spine.

**Critical collisions:** v144 adds a genuine theorem, not merely a rewritten generic root count.

### Still open

**Ballico 1993 theorem-level comparison:** open and still blocking for a top-four novelty certification.

**Exact historical priority of the broad contraction theorem:** still open if that theorem remains a submission-level novelty pillar.

**Definition of the complete publication object:** still open. A 102-page supplement of largely independent active theories is not solved merely by moving it behind an appendix boundary.

### Not currently an open blocker

I do **not** presently identify a new proof-level counterexample to the main v144 finite-flat critical-divisor theorem. That statement should not be misread as a formal certification of all 130 pages.

## 15. Minimum conditions for a fresh top-four evaluation

Before I would support a fresh accept/reject review on the merits rather than another cleanup round, I would require the following.

1. **Obtain and compare Ballico 1993 at theorem level.** This is the most important item. The comparison must use the actual text and answer the six axes listed above.

2. **Freeze the publication object.** Decide whether the 102-page web/operator/K3/boundary supplement is actually part of the submitted paper. Preserve the mathematics, but move logically independent research clusters to companion papers or clearly non-submitted archival material unless there is a compelling unified theorem reason to keep them.

3. **Resolve the rhetorical status of the contraction theorem.** If it is a major novelty claim, complete the map-specific historical comparison. If it is only a supporting theorem for the web branch, keep it out of the principal significance argument.

4. **Retain the v144 principal hierarchy.** The finite unmarked reconstruction theorem should remain the central theorem; universal spectral readout and the projective critical divisor should remain the main continuations.

5. **Keep the sharp scope qualifiers.** All pencils versus regular pencils; split semisimple data versus arbitrary data; reduced rank loci versus full Fitting schemes; complex reconstruction versus supplied real definite structure; unmarked objects versus framed families.

6. **Preserve immutable review routing.** Future mathematical changes should occur on a new revision branch with a new source lock, rather than moving the reviewed v144 object.

7. **Add the two small proof clarifications above.** The characteristic-zero rational-point argument and the Hessian coordinate-change argument should be explicit.

I do **not** request weakening the main theorem, deleting the nonreduced structure, or retreating to a generic-only result. The correct next step is to close the external novelty evidence and define a reviewable publication object while preserving the mathematical spine.

## 16. Final assessment

Revision 144 is the strongest A2 revision I have seen in this repository.

The main inverse theorem remains substantial: the manuscript claims, and gives a serious intrinsic proof, that one exact finite neighbourhood of a nonreduced multiplication-failure scheme reconstructs every quadratic pencil, while every lower order is universal. The relative version is now genuinely glued. The spectral sheaf and its Fitting data are recovered scheme-theoretically. The reciprocal critical correspondence is functorially attached to the reconstructed pencil. The new v144 section then supplies a projective finite-flat continuation through critical collisions, identifies ramification with Hessian degeneracy, identifies the trace discriminant, and exhibits a nonreduced length-three fibre in a fixed pencil.

I found the new v144 local algebra coherent and did not find a fatal new mathematical error in the principal chain.

Nevertheless, I would still recommend **rejection in the present form at a general top-four journal**.

The reason is now sharply identifiable. The manuscript has not yet closed the theorem-level comparison with the closest known 1993 failure-locus predecessor, so its central novelty boundary cannot responsibly be certified. At the same time, the complete submission remains far larger than its now-coherent principal narrative because a 102-page collection of independent theorem clusters is still treated as active submission mathematics.

If the Ballico 1993 comparison comes out favorably, the complete publication object is rationalized, and the contraction theorem is given a historically defensible role, I would regard the next version as deserving a genuinely fresh top-four evaluation. That future evaluation should not begin from the presumption that the paper is false: the current main spine has crossed the threshold from “ambitious but structurally unreviewable” to “mathematically serious, with a concrete external novelty blocker and a scope problem.”

Until those blockers are closed, however, I would not recommend acceptance.
