# Independent harsh referee report on A2 revision 114

Repository: TrillionniumFoundation/theta-theory

Revision branch reviewed: revision/a2-v114-global-residual-singularities-2026-09-22

Frozen revision head reviewed: d58d4ad0546487f4313cf8ed2f05ad9321b54e63

New review branch: review/a2-v114-independent-harsh-top4-2026-09-22

Principal manuscript: papers/A2-v17-boundary-information-coarsening/article/v114/paper.tex

Title: **Residual geometry and singularities of multiplication failure schemes**

Referee standard: a general top-four mathematics journal (Annals of Mathematics / Inventiones Mathematicae / Journal of the AMS / Acta Mathematica level)

Recommendation: **Reject in the present form at a general top-four mathematics journal.**

Revision 114 is a serious and mathematically substantive response to the preceding report. I do not regard it as a cosmetic rewrite, and I do not repeat the v113 objections that have actually been addressed. The new manuscript formulates a polar residual tangent theory for an arbitrary symmetric linear system, derives a global expected-codimension singular-support theorem and residual cotangent-Fitting identities, supplies formal orientation descent, constructs a relative residual determinant divisor, proves the normal-derivative factorization and a simultaneous nonempty wall open, replaces topological phase-monodromy language by an algebraic finite-cover argument, and gives the requested primary decomposition of the rank-two fibre.

Those additions change the character of the paper. The algebraic-geometric core is now much more coherent, and I did not find an immediate counterexample to the new central polar-residual theorem, the Fitting calculation, or the ordinary-double-crossing theorem on its stated dense open locus.

My negative recommendation therefore has a different basis from the previous round. The paper is now closer to a strong specialist algebraic-geometry paper, but in my judgment it still does not clear the bar for a general top-four journal. The main reasons are:

1. the new arbitrary-symmetric-system theorem is formally broad but, in its present form, is primarily a general incidence/cotangent/Fitting mechanism rather than a comparably broad global classification theorem;
2. the difficult global component and wall geometry remains essentially specific to quadratic multiplication of binary subseries;
3. the excess-codimension geometry is still not globally classified beyond maximal-dimensional components and local residual criteria;
4. the higher-product results still classify only a distinguished two-point obstruction family, not the full higher-product failure scheme;
5. the closest historical priority issue explicitly remains unresolved, and the new general polar/Fitting theorem itself now requires a much more serious comparison with the general deformation theory of degeneracy loci;
6. the manuscript still carries a very large inverse/statistical apparatus that is not logically needed for the central algebraic theorem and obscures the paper's identity;
7. at the exact reviewed head, the repository documentation advertises a compiled PDF and source/build receipts that are not present on that head.

The last item is a source-control/provenance defect, not a mathematical counterexample. The first six are the substantive editorial reasons for the recommendation.

## 1. Review scope and exact source boundary

I reviewed the materialized v114 mathematical source at

d58d4ad0546487f4313cf8ed2f05ad9321b54e63.

The review branch was created directly from that commit before writing this report. At the time of finalizing the report, the revision branch and the new review branch were still identical before addition of this report.

This source is a genuine revision of v113. It contains the new general polar section, the explicit orientation-descent section, the relative wall proof package, the reorganized higher-product argument, the priority/application section, the point-by-point response, preservation records and verification code.

There is, however, an important repository-state qualification. At the reviewed head:

- article/v114/paper.pdf is absent;
- article/v114/paper.log is absent;
- article/v114/evidence/SOURCE_RECEIPT.json is absent;
- article/v114/evidence/BUILD_RECEIPT.json is absent.

Yet article/v114/README.md describes paper.pdf as the compiled manuscript and discusses source-bound receipts in evidence/, and the root A2_REVISION_V114_INDEX.md links both paper.pdf and evidence/BUILD_RECEIPT.json.

The workflow explains the mismatch: its first stage materializes and pushes the mathematical source, while a later stage is intended to compile and commit the PDF/evidence. I therefore do **not** infer that the workflow failed. I only record the exact fact relevant to this review: the frozen source head I reviewed does not contain the generated artefacts that its documentation already describes as present.

Accordingly, this is a source review of the materialized TeX manuscript, not an independent verification of a committed v114 PDF/build receipt.

## 2. Revision 114 genuinely closes most of the v113 proof-completeness objections

It is important not to review the previous manuscript again.

### 2.1 The orientation-descent objection has been substantially answered

Proposition 5.1 now gives an actual relative orthogonal descent statement. It specifies the orientation double cover for a line-valued even-rank quadratic bundle, describes the two geometric maximal-isotropic families, identifies the determinant character that exchanges them, and treats products of maximal-isotropic factors.

Proposition 5.2 then applies this mechanism to the exceptional incidences using an explicit ordered support/nonzero-weight chart and a function-field nonsquareness argument. The full-rank (7,14,1) case is treated separately through the square class of the Hankel determinant.

This is substantially better than the v113 monodromy shorthand. I no longer regard the mere absence of a formal descent lemma as a blocker.

### 2.2 The relative wall argument is now an actual proof package

The relative residual determinant is no longer introduced fibrewise and then silently globalized. Proposition 7.4 constructs the relevant line bundles and relative Grassmannian product, identifies the determinant section, and proves integrality/reducedness of the resulting Cartier divisor.

Proposition 7.5 supplies the missing normal-bundle statement. In particular, it identifies an invertible plane-normal block and the residual multiplication block on the quotient, so that the determinant of the normal derivative is the residual determinant up to a unit.

Lemma 7.6 then addresses the earlier simultaneous-nonemptiness concern. It does not merely assert that several open conditions are generic separately; it gives an incidence/codimension argument and an affine-lift variation that produces the original corank-one condition simultaneously with the residual corank-one and evaluation-rank conditions.

I regard this as a real closure of one of the most serious v113 proof-completeness complaints.

### 2.3 The higher-product phase descent is now algebraic

The finite splitting cover with coordinates (x,y,t), together with the cyclic and inversion deck transformations, is a much cleaner basis for the dihedral orbit count than the prior loop language.

The proposition also explicitly handles stabilizers: an inversion-fixed relative pattern is not asserted to split merely because the orbit has nontrivial isotropy.

Again, this is a meaningful repair.

### 2.4 The rank-two fibre proposition now has the requested commutative algebra

The explicit primary decomposition

J_c = a intersection b intersection (J_c + m^3)

and the Hilbert-series computation make the embedded-origin statement independently checkable. This is better than relying on a short exact sequence plus small finite diagnostics.

### 2.5 The Stacks citation and scope qualifiers have been cleaned up

The reducedness argument now cites the exact R0 + S1 reducedness lemma. The signed-intersection theorem is explicitly about same-annihilator intersections over the split rank-two base. The excess theorem consistently says maximal-dimensional components.

These are minor individually, but they show that the revision has taken the scope criticisms seriously.

## 3. The new polar residual theorem is mathematically useful, but its present level of generality is not yet the same thing as a general top-four theory

The most important new material is Section 2.

For an arbitrary linear map beta: Sym^m V -> F and a product of Grassmannians, the manuscript defines the plane derivative B, the polar residual source Q = ker(B*), and the residual map tau = mu restricted to Q. The exact tangent sequence

0 -> ker B -> T incidence -> (mu Q)^perp / C ell -> 0

and the resulting formula

dim T incidence = M - a + dim ker tau

are clean and useful. For m=2, the identification of Q with the direct sum of Sym^2(U_nu intersect rad H_ell) gives the binary residual multiplication mechanism a genuinely invariant formulation.

I checked the linear-algebra logic of this theorem. The tangent equation, the solvability condition through the annihilator of Q, the rank count, and the corank-one incidence isomorphism are mutually consistent. I did not find a hidden binary-form hypothesis in the abstract statement.

The problem is not that this theorem is false. The problem is what it accomplishes relative to the venue claim.

At the arbitrary-beta level, the theorem does **not** determine:

- when the maximal-minor scheme has expected codimension;
- its irreducible components;
- its global cycle decomposition beyond the formal determinantal class when applicable;
- the geometry of the annihilator rank strata;
- whether a residual map is itself a multiplication system of the same type;
- a recursive component theorem;
- a wall-crossing theorem;
- a normal-form theorem;
- or a nontrivial family-wide classification for m >= 3.

The arbitrary-beta theorem therefore provides a deformation-theoretic envelope around the specialized classification; it does not yet transport the hard classification to a broad new class.

The paper itself is candid about this, especially for higher powers. That candor is good. But it also means that the earlier request for a genuinely general theorem is only partly answered.

A general top-four paper could justify this architecture in one of two ways.

**First route: prove a structural theorem with nontrivial geometric consequences beyond the model.** For example, give verifiable hypotheses on beta, its annihilator strata and the polar residual systems under which component formation, residual recursion, expected codimension and wall singularities follow. Then show at least one substantial non-binary or m >= 3 family satisfying those hypotheses.

**Second route: make the binary quadratic classification the unapologetic main theorem.** In that case the polar formalism should be presented as the invariant mechanism explaining the classification, not as evidence that a comparably complete arbitrary-symmetric theory has already been achieved.

At present the manuscript tries to claim the conceptual benefit of the first route while most of the deep geometric content remains on the second.

## 4. The global singular-support theorem is a strong organizational result, but its novelty burden is now much higher than the manuscript acknowledges

Theorem 2.2 states, under pure expected codimension, that the reduced singular support is exactly the union of:

- original multiplication corank at least two;
- original corank one with noninjective polar residual map.

On a constant-rank polar stratum in the corank-one locus, it further identifies all relevant cotangent Fitting ideals with minors of tau.

The index count in the Fitting formula is internally consistent: after splitting the invertible plane-derivative block, the residual presentation has precisely the advertised minor size. The statement that a corank-at-least-two point is singular is also consistent with the Schur chart: the local maximal-minor generators have no linear terms there, so the Zariski tangent space is the full ambient tangent space while expected codimension is positive.

The manuscript then gives the all-corank Schur-Jacobian presentation of the singular scheme. Again, I do not see an immediate mathematical contradiction.

But there is a major top-four novelty issue.

Much of the proof consists of:

- differentiating a determinantal incidence;
- splitting an invertible block;
- using a cotangent presentation;
- using invariance and base change of Fitting ideals;
- using Schur-complement equations;
- applying the Jacobian/Fitting description of a singular scheme.

Those are classical pieces of determinantal/deformation theory. The manuscript itself correctly says that cotangent presentations, Fitting calculus, Schur elimination and determinantal resolutions are standard.

Once Theorem 2.2 becomes the claimed conceptual generalization, the literature audit must therefore compare it not only with papers about binary forms, secants and normal generation, but also with the general literature on tangent/conormal spaces, degeneracy loci, determinantal singularities and Fitting stratifications.

The present literature section does not do this.

I am not asserting that an identical theorem already exists. I have not established that. I am saying that a theorem whose proof is this formal has a particularly high burden of demonstrating what is genuinely new:

- Is the novelty the definition of Q?
- The identification of Q for quadratic multiplication?
- The global support formula?
- The exact Fitting-index recursion?
- The application to varying subseries?
- Or a combination of these?

A top-four manuscript needs that answer explicitly and with nearest prior theorems, not only with references to the algebraic tools used in the proof.

Without this comparison, I cannot treat Theorem 2.2 itself as the missing top-four conceptual leap merely because it is stated for arbitrary beta.

## 5. “Global singularities” still means global support and global equations, not a global classification of singularity types

The title and abstract are much better aligned with the paper than in earlier versions, but they still invite a stronger reading than what is actually proved.

The manuscript now has three distinct levels of singularity information.

### 5.1 Global expected-codimension support

Theorem 2.2 gives a global set-theoretic characterization of the singular support under the pure expected-codimension hypothesis. This is a genuine global theorem.

### 5.2 Global local-equation machinery

The Schur-Jacobian formula gives an exact open-chart presentation of the singular scheme at every original corank. This is also global in the sense of covering the failure scheme.

### 5.3 Residual determinantal identification only on specific corank-one strata

The elegant residual-minor description of the Fitting ideals is pulled back to constant-rank polar strata inside the corank-one locus. At higher original corank, or through changes of polar rank, the paper falls back on the full Schur-Jacobian equations.

That distinction is mathematically sound and explicitly stated.

But it means the paper still does **not** classify:

- all analytic or formal singularity types;
- normalization of the whole failure scheme;
- conductor data globally;
- incidence-image identifications at higher corank;
- all intersections created by multiple annihilators;
- or the local branches through every colliding-support point.

The node theorem remains a dense-open theorem on one distinguished wall divisor.

There is nothing wrong with stopping there. The issue is editorial positioning. “Global residual singularities” should not be used rhetorically as if every singular germ has been reduced to a smaller multiplication failure germ. The theorem gives a global singular-support criterion plus residual Fitting descriptions on specified strata. That is substantial, but it is a more precise and narrower claim.

## 6. The excess-codimension regime remains unfinished at the same global level as the expected-codimension regime

Proposition 2.5 is useful. It shows that the same cotangent calculation continues to produce an exact Fitting formula on a corank-one constant-rank stratum even when expected codimension fails. It also gives the correct tangent criterion once the actual local dimension is known.

This is not, however, a global classification of the excess scheme.

The all-dimensional component theorem still says, when b < a, only that the maximal-dimensional components are the signed secant components, with one additional exceptional component at (5,7,1).

It does not determine:

- every smaller irreducible component;
- the global associated primes of the maximal-minor ideal;
- embedded components;
- equidimensionality failures away from the maximal components;
- how lower-dimensional annihilator strata attach to the maximal components;
- or a recursive decomposition of the complete excess scheme.

The manuscript is careful not to claim those results. I credit that precision.

But this is exactly why the phrase “components in all dimensions” and the broader global-geometric framing still feel stronger than the actual excess theorem. The dimensions of the **parameters** range over all c,k,L; the component classification itself is not complete in the excess regime.

For a specialist paper, that may be a perfectly reasonable boundary. For a top-four paper selling a global classification mechanism, it is a substantive unfinished part of the story.

## 7. Higher symmetric powers remain an obstruction-family theorem, not a higher-product analogue of the main classification

The revision has improved the proof of the phase-sector theorem, but not its mathematical scope.

For m >= 2, the manuscript classifies the reduced incidence of a distinguished family of two-point annihilators and obtains the dihedral orbit count

N_{m,L} = (m^{L-1} + gcd(m,2)^{L-1}) / 2.

It proves irreducibility and rationality of the corresponding image closures and obtains a residual tangent/smoothness formula on those sectors.

Those are legitimate results.

The manuscript also says explicitly that these sectors are **not** asserted to be all components of the higher-product failure scheme and that the full higher-product failure codimension is not determined.

That disclaimer is exactly right. It also prevents the higher-product section from carrying the burden of a genuine m >= 3 generalization of the quadratic component theorem.

In other words, the arbitrary-beta polar theorem is broad but formal, while the explicit m >= 3 geometry is concrete but partial. The manuscript still lacks a theorem that is both broad **and** comparably deep to the quadratic binary classification.

That is the central conceptual reason I still do not see a general top-four paper.

## 8. The wall theorem is now one of the strongest parts of the paper

I want to separate the remaining global-scope criticism from the correctness of the new wall proof.

The relative determinant line, the affine torsor, the normal-bundle factorization and the simultaneous-open lemma now give a much more convincing route to the local equation uv = 0.

The logic is coherent:

1. the signed incidence is smooth;
2. the residual determinant cuts an integral reduced divisor in it;
3. the normal derivative drops rank exactly along that divisor;
4. on the corank-one open, all but one normal equation are eliminated;
5. the remaining equation factors as uG;
6. simple vanishing of G along the residual divisor gives a transverse coordinate v = G;
7. hence the analytic equation is uv = 0.

This is exactly the level of organization I wanted in the previous report.

I therefore do **not** regard the generic node theorem as a current rejection-level proof gap.

The remaining limitation is one of scope: the theorem still describes a nonempty dense open of one wall divisor, not the entire wall or every multiple-annihilator/collision germ. The new Fitting theorem records tangent-excess strata beyond that open, but a Fitting stratification is not itself a classification of analytic types.

That is an acceptable theorem boundary; it simply should be reflected in the top-level significance claim.

## 9. Priority remains a formal blocker, now in two directions

### 9.1 Ballico 1993 remains explicitly unresolved

The manuscript's own literature audit states that the theorem-level comparison with E. Ballico, “On the Failure Locus of Higher Order Properties of Embeddings in Projective Spaces,” Math. Nachr. 163 (1993), 5–13, remains unverified because the necessary theorem pages were not obtained.

The revision has made progress: it inspected the actual first page and correctly refuses to infer nonoverlap from a title or first-page description.

That is responsible scholarship.

It is still not closure.

The burden is especially significant because “failure locus,” higher-order embedding properties and incomplete spaces of sections are close enough to the present topic that a general top-four referee cannot simply assume the principal novelty boundary.

I am not claiming that Ballico 1993 contains the v114 component theorem, residual singularity theorem or wall node. I have not verified that, and neither has the manuscript.

That uncertainty itself is the blocker.

### 9.2 The new arbitrary-beta theorem creates a second priority obligation

The literature audit is still organized mostly around normal generation, binary forms, Hankel determinantal geometry and secant failure.

But Theorems 2.1 and 2.2 are stated as general theorems about arbitrary symmetric linear systems and determinantal failure schemes. Their nearest literature is therefore not exhausted by the older projective-normality papers.

A revised priority section should compare the new theorem, theorem by theorem, with the nearest general results on:

- singular loci of determinantal and degeneracy loci;
- tangent and conormal descriptions of rank-drop loci;
- incidence resolutions of determinantal schemes;
- Fitting ideals of cotangent modules;
- singularity stratifications induced by kernels/cokernels of bundle maps;
- symmetric or isotropic degeneracy loci where relevant.

The manuscript should say exactly which step is new after these general theories are taken into account.

Until that is done, the general theorem cannot simultaneously be the paper's main novelty argument and remain largely unpositioned against its natural general literature.

## 10. The paper is still carrying too many logically independent programs

The reorganization is an improvement. The article now starts with multiplication failure and the polar residual theorem, and the short information-recovery application comes after the algebraic geometry.

But the manuscript still retains in its appendices a very large collection of:

- exact contact geometry;
- native realization;
- boundary experiments;
- finite-precision score compression;
- Poisson/Gaussian comparisons;
- finite-sample estimation;
- inverse-programming complements;
- and other statistical constructions inherited from the earlier versions.

The preservation policy is understandable from a revision-history perspective. It is not necessarily a good publication architecture.

The main algebraic theorems do not depend on these appendices. The manuscript itself says so.

A general top-four paper should make its conceptual spine unmistakable. Here the strongest spine is now:

polar residual deformation -> binary component theorem -> residual wall -> singularity/Fitting structure.

The full statistical/native program is better treated as:

- a companion paper;
- a separate application paper;
- or a much shorter final section containing only the minimum needed to demonstrate why the geometry matters.

Keeping all of it in the same submission increases length and cognitive load without strengthening the proof of the central geometry.

## 11. The repository's evidence claims should match the exact reviewed head

This is not a reason by itself to reject a theorem, but it is a publication-readiness issue.

At d58d4ad0546487f4313cf8ed2f05ad9321b54e63 the readable source exists, but the files advertised as generated build evidence do not.

A future submission-ready revision should ensure that:

1. the README does not describe a compiled PDF as present before it is committed;
2. the root index does not link nonexistent evidence;
3. the source receipt identifies the exact mathematical source;
4. the PDF receipt identifies the exact PDF generated from that source;
5. source-only and evidence-only commits are clearly distinguished;
6. the final journal-facing manuscript is generated from the same reviewed source.

The workflow is designed to achieve this. The exact reviewed head simply had not yet reached that state.

I have not treated successful finite diagnostics, when present, as proof of any universal theorem. The repository itself correctly warns against doing so.

## 12. Specific mathematical points that I checked and do not currently treat as blockers

To make clear where this review has moved relative to v113, the following are **not** current rejection-level objections.

### 12.1 The polar tangent dimension formula

The rank algebra is consistent. If h = dim Q, then rank B = e - h, and the residual map accounts for exactly the remaining annihilator-direction compatibility equations. The stated dimension M - a + dim ker tau follows.

### 12.2 The corank-one incidence isomorphism

On an invertible (p-1)-minor chart, the normalized annihilator is uniquely solved and the remaining equations are the Schur row. This is enough for the scheme-level local identification used by the Fitting argument.

### 12.3 The corank-at-least-two singularity assertion under expected codimension

After Schur elimination, the rho-minors of a matrix vanishing at the point have no linear terms for rho >= 2. Therefore the tangent space is ambient. With positive expected codimension, the point is singular.

### 12.4 The primary decomposition of the fixed rank-two fibre

The degree-two mixed relations and vanishing of mixed cubics support the stated decomposition and Hilbert series. I do not presently see the former associated-prime objection surviving v114.

### 12.5 The generic node reduction

With the new relative divisor, normal-block factorization and nonempty-open lemma in place, the implicit-function reduction to uv = 0 is now sufficiently explicit for me not to list it as an unresolved proof architecture issue.

These observations are not certifications of every line. They explain why the recommendation is no longer driven by a suspected elementary mathematical failure.

## 13. What would materially change my top-four assessment

Another revision should not consist of a new layer of local patching around the same theorems. The paper has already repaired most of those proof-architecture problems.

What is needed now is a change in conceptual closure.

### A. Establish the novelty boundary of the general theorem

Provide a theorem-by-theorem comparison with the general determinantal/degeneracy-locus deformation literature. State exactly which part of the polar tangent/Fitting package is new.

Separately, complete the theorem-level comparison with Ballico 1993 and the nearest projective-normality/subseries literature.

### B. Make the general theorem generate new geometry outside the binary quadratic model

A convincing route would be a structural theorem whose hypotheses imply some combination of:

- expected codimension;
- component recursion;
- residual singularity recursion;
- wall formation;
- or normal forms.

Then work out at least one substantial non-binary or m >= 3 example.

Merely observing that any section-multiplication map can be inserted into beta is not enough; the theorem should produce nontrivial information in that setting.

### C. Either finish the excess geometry or narrow the global classification claim

If the authors want an “all dimensions/global failure scheme” classification, determine the smaller components and associated-prime structure in the excess regime, or prove a recursive theorem that controls them.

If they do not want to solve that problem, narrow the title and principal claims to the expected-codimension classification plus maximal excess components.

### D. Refocus the paper

Move the long statistical/native development into a companion article or sharply compress it to a genuine application section.

A cleaner algebraic paper would make the current strongest results easier to recognize and evaluate.

### E. Close the build/provenance loop before treating the branch as submission-ready

Commit the generated PDF and exact source/build receipts, or remove claims that they already exist.

## 14. Final recommendation

Revision 114 is a substantially stronger manuscript than revision 113.

It has done the hard work of converting several previously plausible arguments into actual propositions with identifiable hypotheses and proofs. The general polar residual formulation is useful. The expected-codimension singular-support and Fitting theorem gives the paper a cleaner conceptual center. The wall proof is now organized in a way that can be independently checked. The orientation and phase-descent issues have been treated seriously.

For those reasons, I would no longer characterize the manuscript as being blocked mainly by local proof gaps.

I nevertheless recommend **Reject in the present form at a general top-four mathematics journal**.

The decisive issue is now the mismatch between the breadth of the venue-level claim and the depth of the genuinely general theorem. The hard global classification remains a special binary quadratic result; the arbitrary-symmetric theorem is principally a deformation/Fitting framework; the higher-product geometry is partial; the excess scheme is not globally classified; and the historical/general novelty boundary is not yet certifiable.

This is a much more mature and potentially publishable research paper than the earlier revisions. But for Annals/Inventiones/JAMS/Acta level, the next advance must be conceptual rather than another round of technical patching: either turn the polar residual mechanism into a general structural theory with new consequences beyond the model case, or present the binary quadratic classification as a sharply focused specialist theorem with a fully audited priority boundary and a substantially cleaner article architecture.
