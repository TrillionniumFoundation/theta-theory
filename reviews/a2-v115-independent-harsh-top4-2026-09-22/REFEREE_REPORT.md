# Independent harsh referee report on A2 revision 115

Repository: TrillionniumFoundation/theta-theory

Revision branch reviewed: `revision/a2-v115-intrinsic-residual-germs-2026-09-22`

Frozen revision head reviewed: `acfd3d57e0053e1b03df53020fd8e79e14599c03`

Mathematical source commit identified by the source-bound receipt: `426d112c574f5d3289f6c7d4ecb5f0328ac040b5`

Controlling previous report: R114 at `09869129e16fd43bd2420fa3573a09cd5cbbdff9`

New review branch: `review/a2-v115-independent-harsh-top4-2026-09-22`

Principal journal-facing manuscript: `papers/A2-v17-boundary-information-coarsening/article/v115/geometry.tex`

Complete archival manuscript: `papers/A2-v17-boundary-information-coarsening/article/v115/paper.tex`

Title: **Residual geometry and singularities of multiplication failure schemes**

Referee standard: a general top-four mathematics journal (Annals of Mathematics / Inventiones Mathematicae / Journal of the AMS / Acta Mathematica level)

Recommendation: **Reject in the present form at a general top-four mathematics journal.**

## 1. Executive assessment

Revision 115 is a genuine and substantial mathematical revision. It should not be reviewed as if revision 114 had merely been repackaged. The new manuscript does four things that materially change the previous assessment.

First, it adds an exact local residual-matrix presentation at every multiplication corank, separates the intrinsic normal derivative from the nonlinear residual terms, and records joint relations involving several annihilators. Second, it adds a natural higher-product family — hyperplane subseries of the complete binary series — in which the entire reduced failure support and every corank are determined for every symmetric degree. Third, for degree at least three it proves a scheme-theoretic statement about that family: the secant threefold is the unique reduced component, the evaluation curve is the unique embedded associated subvariety, and the nilpotency index has a lower bound growing with the symmetric degree. Fourth, the source/build defect identified in R114 has been repaired: the frozen revision head now actually contains the generated PDFs, logs and source-bound receipts advertised by the documentation.

These are real advances. In particular, the new hyperplane theorem is substantially better than the old two-point-sector statement, because it excludes every other reduced failure component in that family and supplies nontrivial embedded structure.

Nevertheless, I still do not regard the paper as meeting the standard of a general top-four mathematics journal. The reason is no longer a missing local proof package or a repository inconsistency. The remaining issue is the mathematical level and breadth of the main advance relative to the venue claim.

The manuscript now contains three layers:

1. a very general determinantal/deformation formalism for arbitrary symmetric systems;
2. a deep but specialized quadratic binary classification accumulated over many revisions;
3. one complete higher-product hyperplane family whose proof is largely driven by classical Hankel/secant geometry, elementary binary-monomial propagation, Schur elimination and equivariance.

The first layer is broad but, at its general level, largely formal/classical once the multiplication polar is identified. The second layer is genuinely rich but remains tied to the quadratic binary problem and is still incomplete in the excess regime. The third layer is complete, but is a particularly special parameter family and does not yet provide the broad higher-product classification that would transform the paper into a general theory.

For a strong specialist algebraic-geometry journal, this combination may be significant. At the Annals/Inventiones/JAMS/Acta level, I would expect a substantially stronger synthesis: either a general theorem that transports the component/singularity machinery to a broad class of higher-product systems, or a much deeper scheme-theoretic classification of the natural binary families themselves.

I do not currently see that theorem in revision 115.

## 2. What revision 115 genuinely closes from R114

It is important to distinguish closed objections from persistent ones.

### 2.1 The previous build/source mismatch is closed

R114 froze a source head for which the documentation linked generated artefacts that were not yet present. Revision 115 no longer has that defect.

At the reviewed head `acfd3d57e0053e1b03df53020fd8e79e14599c03`, the repository contains:

- `geometry.pdf`,
- `paper.pdf`,
- `applications.pdf`,
- the corresponding logs and `.fls` files,
- `SOURCE_RECEIPT.json`,
- `BUILD_RECEIPT.json`,
- finite diagnostics and source checks.

The build receipt identifies the mathematical source commit separately from the generated-evidence commit and explicitly says that the build is not proof certification. This is the correct provenance model.

I therefore do not repeat the R114 source-control objection.

### 2.2 The “higher products are only a two-point obstruction family” objection is partially closed

Theorem `thm:higher-hyperplane-global` is a real step beyond the old phase-sector theorem. For the natural parameter space of hyperplanes (Usubset H^0(mathbb P^1,mathcal O(n))), it identifies the complete reduced failure locus of
[
operatorname{Sym}^m Ulongrightarrow H^0(mathbb P^1,mathcal O(mn))
]
for all (nge4) and (mge2), determines the corank on the secant and evaluation strata, and gives a global statement on associated points for (mge3).

This is not an artificially chosen arbitrary-(eta) realization and not merely a lower-dimensional obstruction sector. I regard that criticism as genuinely answered for this one family.

What is not closed is the broader higher-product problem on the Grassmannian families that motivated the paper.

### 2.3 The “restricted Fitting data are not exact germs” objection is closed at the level of local equations

The new residual-matrix theorem correctly distinguishes:

- the intrinsic normal derivative,
- its joint polar obstruction,
- the exact Schur residual matrix,
- and the nonlinear terms that survive after first-order elimination.

The corank-one minimal residual presentation and the cubic cusp example make the distinction concrete. The manuscript no longer suggests that tangent/Fitting data alone determine every analytic germ.

This is an important conceptual cleanup.

### 2.4 The geometry/statistics architecture is improved

The 38-page geometry reading copy is a much better journal-facing object than the previous single large manuscript. The 64-page archival version and the separate application copy preserve the long information-recovery program without forcing the reader to treat it as part of the proof of the algebraic results.

I still have reservations about the paper's identity, discussed below, but the structural objection in R114 has been materially reduced.

## 3. The main new hyperplane theorem is interesting, but I do not think it carries a general top-four paper

The decisive new global result is Theorem `thm:higher-hyperplane-global`.

Its statement is attractive:

- the reduced failure locus is always the secant threefold (S_n);
- the multiplication corank is (0) off (S_n), (1) on (S_nsetminus C_n), and (m) on the evaluation curve (C_n);
- the scheme is smooth away from (C_n);
- saturation away from (C_n) gives (I_{S_n});
- for (mge3), the complete associated-point set is ({eta_{S_n},eta_{C_n}});
- powers of a quadratic secant equation yield an unbounded lower bound on the nilpotency index.

This is a clean package. I did not find an immediate counterexample to the statement.

The top-four problem is that the proof, once the correct family is chosen, is comparatively elementary and special.

The support calculation uses the rank-at-most-two Hankel description of quadratic failure. Higher-degree surjectivity is then propagated by a base-point-free pencil argument. The corank calculation is reduced to explicit binary monomial spans on a split secant, a tangent secant and an evaluation hyperplane. Smoothness off the evaluation curve comes from an explicit polar-rank computation. The embedded associated curve is then obtained from the order of Schur minors at an evaluation point, one quadratic equation of the secant variety, and (mathrm{SL}_2)-equivariance.

That is good mathematics, but it does not yet look like the conceptual leap one expects from a general top-four article.

The parameter space is only (mathbb P(V_n^*)), i.e. hyperplanes. The reduced support is the classical secant threefold. The theorem does not classify:

- codimension-(r) subseries for (r>1);
- the higher-product failure scheme on (operatorname{Gr}(c,V_n)) for general (c);
- the analogue for several contacts;
- the full primary ideal along the embedded evaluation curve;
- the exact nilpotency index;
- or higher-contact configurations beyond the hyperplane family.

Thus the paper has moved from “explicit higher-product obstruction sector” to “one complete natural higher-product family.” That is a meaningful improvement, but it is still not a higher-product analogue of the quadratic component theorem.

For a top-four submission, I would expect the hyperplane theorem either to be the first case of a substantially broader structural theorem, or to be strengthened to a much more complete scheme-theoretic classification whose depth clearly exceeds the classical secant/Hankel input.

## 4. The exact residual-germ theorem is useful, but its general part is mostly classical matrix geometry

Section `sec:intrinsic-residual-germs` is mathematically well organized. The distinction between a single-annihilator polar kernel and joint relations in
[
kerleft(operatorname{Hom}(kermu,operatorname{coker}mu)^*
	o T^*Xight)
]
is useful, and the explicit multiplication interpretation has value.

However, the core local normal form
[
widehat{mathcal O}_{D,U}
simeq
mathbb C[[y,x]]/I_ho(L(y)+Psi(y,x))
]
is obtained by standard Schur elimination plus the analytic inverse function theorem. Likewise, the transverse generic-determinantal model is the usual normal form for a map transverse to a rank stratum.

The manuscript now acknowledges this explicitly and cites determinantal-singularity literature. That correction is welcome. It also makes the novelty issue sharper.

At the arbitrary-system level, the new theorem is not that every determinantal germ has such a residual matrix; that is classical. The paper-specific content is:

- the identification of the intrinsic derivative with the multiplication polar;
- the organization of joint annihilator relations in that language;
- the residual interpretation in the quadratic binary case;
- and the way these local equations are tied to the global binary classification.

That is a coherent framework. I do not think, by itself, it is a top-four theorem.

The current presentation occasionally still gives the general formalism more rhetorical weight than its novelty justifies. For example, “exact residual equations at every multiplication corank” sounds like a new classification theorem, whereas the exact local matrix presentation is largely the standard local geometry of rank loci expressed in the chosen multiplication coordinates.

The paper should continue to distinguish “new multiplication-specific identification” from “classical matrix normal form” at every stage.

## 5. The closest historical-priority problem remains unresolved, and this is now a serious publication blocker

The manuscript is commendably explicit that the Ballico 1993 comparison remains incomplete.

That honesty does not remove the problem.

The current paper's main subject is a failure locus for varying subseries and higher-order multiplication properties. The cited Ballico paper is titled *On the Failure Locus of Higher Order Properties of Embeddings in Projective Spaces*. The authors have inspected bibliographic and first-page material but have not obtained and compared the theorem statements.

For an ordinary specialist submission, one might resolve this during revision.

For a claimed general top-four result, I do not think the manuscript can be evaluated responsibly without a theorem-by-theorem comparison with the closest historical source the authors themselves have identified.

The burden is especially high because several ingredients of the new theorem are classical:

- rational normal curve secants;
- low-rank Hankel/catalecticant geometry;
- normal-generation/failure mechanisms;
- determinantal singularity normal forms;
- Fitting ideals;
- Schur complements;
- equivariant arguments.

I am not asserting that Ballico 1993 contains Theorem `thm:higher-hyperplane-global`. I have not established that. The problem is exactly that the manuscript also has not established the contrary.

The literature audit therefore remains insufficient for top-four editorial judgment.

A future version needs a nearest-result table at theorem level, including at least:

1. the exact parameter space in each prior theorem;
2. whether the subseries vary;
3. the symmetric degree (m);
4. whether the result is set-theoretic or scheme-theoretic;
5. whether coranks are classified;
6. whether associated primes/embedded structure are determined;
7. and which part of the present theorem is genuinely not implied by the prior result.

Without this, the novelty claim cannot be assessed at the level required by the venue.

## 6. The excess-codimension quadratic problem is still globally incomplete

Revision 115 preserves the strong quadratic binary results from v114. It does not complete the excess regime.

When (b<a), the manuscript still determines the maximal-dimensional components but not the entire irreducible/associated-prime structure of the maximal-minor scheme.

The unresolved questions include:

- all lower-dimensional components;
- all embedded associated primes;
- a global primary decomposition;
- attachment of smaller annihilator strata;
- and a recursive structure theorem for the complete excess scheme.

The new hyperplane family shows that the authors can prove a complete associated-point theorem in one excess family. That actually makes the remaining gap in the main quadratic family more visible.

The paper repeatedly emphasizes “global residual geometry,” “components in all dimensions,” and a general residual mechanism. At top-four level, the natural expectation is that the principal family itself should have a comparably complete global scheme-theoretic description, not only its maximal-dimensional components in the excess range.

The present manuscript is careful in the fine print, but the overall conceptual framing still outruns the classification actually proved.

## 7. The higher-product story remains split between breadth and depth

The paper now has three higher-product statements of very different character.

### 7.1 Arbitrary symmetric systems

The polar tangent sequence and intrinsic normal derivative apply to arbitrary
[
eta:operatorname{Sym}^m V	o F.
]
This is broad, but mainly formal.

### 7.2 Two-point higher-product sectors

The older explicit phase-sector theorem gives concrete geometry, but the paper correctly does not identify those sectors with the complete failure scheme.

### 7.3 Hyperplane subseries

The new theorem gives a complete global support/corank/associated-point statement, but only for codimension-one subseries.

What is still missing is a theorem that is both broad and deep.

For example, a genuinely transformative next result would give verifiable hypotheses on a family of subseries under which the polar residual construction recursively controls:

- components;
- expected versus excess codimension;
- singular support;
- embedded associated structure;
- and higher-product wall phenomena.

Alternatively, the authors could prove a full (mge3) component theorem on a nontrivial Grassmannian (operatorname{Gr}(c,V_n)) with (c<n).

Without such a result, the paper remains a sophisticated collection of one formal general mechanism plus several highly developed model calculations.

That is not the same as a general theory.

## 8. The scheme-theoretic part of the hyperplane theorem should go further if it is to be the flagship result

The associated-point argument is elegant. It uses:

1. regularity away from the evaluation curve;
2. saturation to the reduced secant ideal;
3. a secant equation with quadratic initial term at an evaluation point;
4. the fact that the maximal-minor ideal starts in order at least (m);
5. equivariance to eliminate closed embedded associated points.

This proves a real theorem.

But the natural commutative-algebra questions remain unanswered:

- What is the (I_{C_n})-primary component?
- Is the nilpotency index exactly (lceil m/2ceil), or larger?
- What is the associated graded algebra along (C_n)?
- Is the transverse structure constant along the curve?
- Can one identify the Rees or normal cone?
- How do the higher maximal minors generate the embedded structure?
- Is there a representation-theoretic decomposition of the successive nilradical quotients?

The present result gives only a lower bound from one quadratic element.

For a specialist paper, that may be a satisfying theorem. If this is supposed to be the new global result that lifts the work to top-four level, it feels like the beginning of the scheme-theoretic classification rather than its end.

## 9. Several proofs are plausible but too compressed at the exact points on which the flagship theorem depends

I do not presently have a counterexample to the new hyperplane theorem. I do, however, think several arguments are underwritten for a paper aiming at this venue.

### 9.1 Rank of the plane derivative

In Lemma `lem:hyperplane-residual-smoothness`, the key sentence is that the graph variables “can be varied independently,” so the plane derivative has rank (n).

That is believable in the chosen split and tangent normal forms, but it should be written as an explicit matrix computation. The smoothness of the whole scheme on (S_nsetminus C_n) depends on this rank being exactly (n) at every such point.

At the tangent secants especially, I would prefer to see the source quotient, a chosen basis, the graph directions and the resulting polar pairing written out explicitly.

### 9.2 Residual image equality

The equality
[
W^2U^{m-2}=g^2V_{mn-4}
]
in the split case is compressed into a reference to the propagation lemma. This is probably correct, but the iteration and base-point-free hypotheses should be made explicit in the proof rather than left as a one-line assertion.

Likewise, the tangent claim that products with at least two (W)-factors span precisely exponents (4,dots,mn) deserves a clean semigroup lemma.

### 9.3 Rank-two Hankel classification

The proof of the global support invokes the fact that every rank-two Hankel form is associated with a length-two divisor and has the stated radical. This is standard in this context, but it is a decisive global input.

A top-four version should either state and prove the precise catalecticant lemma in the section or cite an exact theorem that includes the tangent/nonreduced length-two case.

### 9.4 Associated points

The final associated-point argument is concise and appears logically sound, but it uses several commutative-algebra facts in rapid succession: finiteness of associated points of a coherent sheaf, equivariance of the associated set, minimal points of the support of a nonzero coherent submodule, and containment of associated points of a submodule in those of the ambient module.

Given that this is one of the headline new conclusions, I recommend isolating this as a lemma with precise references.

These are not the main reason for my rejection recommendation. They are proof-presentation issues that should be fixed irrespective of venue.

## 10. The manuscript is still carrying too much historical accretion for its current central theorem

The geometry-only copy is a substantial improvement. Even so, the core article still contains a long succession of results developed over many revision rounds:

- general polar tangent theory;
- exact residual matrix germs;
- global quadratic geometry;
- residual calculus;
- orientation descent;
- all-dimensional component optimization;
- wall geometry;
- higher-product two-point sectors;
- the new hyperplane theorem;
- prior-work comparison;
- and an application bridge.

Individually these are relevant, but the main narrative is still not as sharp as it could be.

If the hyperplane theorem is now the flagship new response to R114, the paper should decide what the actual main theorem is.

There are at least three possible papers hiding here:

1. a quadratic binary failure-scheme classification paper;
2. a general polar/deformation formalism paper;
3. a higher-product hyperplane/embedded-structure paper.

The current manuscript attempts to make all three reinforce one another. At present I think they dilute one another instead.

A top-four paper usually has one central mathematical inevitability: after reading the introduction, one understands what the main object is, what the main theorem settles, and why the theorem changes the subject.

Revision 115 is much closer to that than earlier versions, but it still reads as an exceptionally elaborate research program compressed into one article.

## 11. The information-recovery application should not be used to raise the algebraic-geometric significance claim

The revised architecture correctly says that the application appendices are not assumptions in the algebraic proofs.

I agree with that separation.

The information-recovery interpretation may motivate the multiplication map, but it does not increase the algebraic novelty of the geometric theorems. The top-four case has to be made entirely on the mathematics of the failure schemes.

Accordingly, the strongest version of this paper should be evaluated as an algebraic-geometry paper first. If the algebraic theorem is not independently at the required level, the size of the downstream application program does not change the venue assessment.

## 12. Verification and repository evidence

The repository hygiene in v115 is substantially improved.

The source checks report:

- 19 reviewed v114 TeX files verified;
- 13 active files byte-identical to v114;
- 136 old theorem/lemma/proposition/corollary/proof environments retained;
- 169 old labels preserved;
- 25 old bibliography keys preserved;
- root/nested-path regression tests passing.

The build receipt reports three compiled PDFs with zero undefined references and zero duplicate labels.

These facts are useful for provenance and for confirming that the revision did not silently delete earlier proofs.

They are not evidence for the universal mathematical statements, and the repository correctly says so.

I therefore regard the engineering/provenance side of this revision as satisfactory for review purposes.

## 13. What would materially change my top-four assessment

This is not a request for more polishing. A new top-four submission would need a stronger mathematical center.

At least one of the following would materially change the assessment.

### Route A: a genuinely general higher-product classification theorem

Prove a theorem for a substantial class of (mge3) subseries — not only hyperplanes and not only a two-point obstruction family — that determines components, codimensions and singular/embedded structure.

The theorem should use the polar residual mechanism in an essential way, not merely as a local tangent calculation.

### Route B: complete the principal quadratic excess scheme

Determine all components and associated primes in the (b<a) regime, not only maximal-dimensional components, and explain the global attachment of the lower-dimensional strata.

A full primary/associated-prime theorem for the main binary family would make the word “global” much more convincing.

### Route C: fully classify the embedded hyperplane structure

Determine the actual primary ideal along the evaluation curve, the exact nilpotency index and the successive infinitesimal layers, preferably in a representation-theoretic form uniform in (m) and (n).

This could turn the current hyperplane theorem from a striking first structural result into a substantial scheme-theoretic classification.

### Route D: establish a new structural recursion theorem

Give checkable hypotheses under which the polar residual system recursively controls not only tangent excess but the global failure scheme — components, walls, embedded structure and higher coranks — and verify those hypotheses in more than one nontrivial natural family.

Any of these routes would address the current breadth-versus-depth problem.

## 14. Mandatory scholarly revisions independent of venue

Even for a specialist submission, I would require the following before publication.

1. Complete the theorem-level comparison with Ballico 1993 and any other nearest failure-locus results it points to.
2. Expand the proof of the plane-derivative rank and residual-image calculations in the hyperplane theorem.
3. Isolate the associated-point argument with precise commutative-algebra references.
4. State exactly which parts of the residual-germ section are classical determinantal normal form and which are multiplication-specific.
5. Continue reducing claims such as “global theory” when the theorem proved is only for one parameter family.
6. Keep the geometry article independent of the statistical appendices at the level of proof dependencies and exposition.

## 15. Final recommendation

Revision 115 is mathematically stronger than revision 114 and answers several of the previous report's concrete objections. The new higher-product hyperplane theorem is a genuine theorem, the exact residual-germ section is a useful conceptual cleanup, and the repository provenance is now reviewable.

I do not, however, think these improvements cross the threshold for a general top-four mathematics journal.

The new general local theory is too close to classical determinantal deformation theory at its broadest level; the deepest global classification remains specialized to quadratic binary subseries; the new complete higher-product result is confined to hyperplanes; the principal excess scheme is still not fully classified; the flagship embedded-structure theorem stops before the primary structure; and the nearest historical-priority comparison remains explicitly unresolved.

My recommendation is therefore:

**Reject in the present form at a general top-four mathematics journal.**

This recommendation is not based on a detected fatal counterexample. It is based on the combination of venue-level novelty, breadth, completeness and priority burden. I would view the paper much more favorably as a specialist algebraic-geometry submission after the literature comparison and the proof expansions listed above, or as the basis for a new top-four attempt after one of the stronger structural routes in Section 13 is actually proved.
