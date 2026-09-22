# Independent harsh referee report on A2 revision 118

**Manuscript:** *Conductor strata and nonreduced multiplication failure schemes*  
**Author:** Qian Qi  
**Repository:** TrillionniumFoundation/theta-theory  
**Reviewed revision branch:** revision/a2-v118-higher-defect-nonreduced-generators-2026-09-22  
**Frozen mathematical-source commit:** c87bfdad8d97e68637d269e656b46c4cce85551e  
**Reviewed product head:** 44bfc648ead008896a6981a7302a6d5ab8b21bb8  
**Controlling R117 report:** 2c6f180fa0baf23386e0a46a64abe7503ea65b00  
**Date:** 22 September 2026

## Referee status and scope

This is an owner-requested, AI-assisted external-referee-style assessment. It was not commissioned by *Annals of Mathematics*, *Inventiones Mathematicae*, *Journal of the American Mathematical Society*, *Acta Mathematica*, or any other journal, and it must not be represented as a journal-issued report or editorial decision.

I reviewed the 26-page primary geometry article, the 91-page complete manuscript, the response to R117, the literature audit, the new higher-defect and nonreduced-multigenerator sections, the relevant inherited finite-algebra and conductor arguments, and the source/build receipts. I also rechecked the public primary-source records for the nearest subalgebra/generator literature. The build receipt reports clean LaTeX products and explicitly disclaims proof and priority certification; I treat those receipts only as provenance and reproducibility evidence.

The mathematical source is pinned at c87bfdad8d97e68637d269e656b46c4cce85551e. The later commit 84ea29f752ca223bbcda1eb8d155adc02082dc28 changes only the branch workflow, and 44bfc648ead008896a6981a7302a6d5ab8b21bb8 is the published product head. I therefore assess the mathematics at the frozen source and the delivered PDFs at the product head.

As in R117, I distinguish:

1. whether I found a concrete contradiction;
2. whether the proofs and relative statements are sufficiently formal for publication;
3. whether the work has the originality, conceptual depth, breadth, and demonstrated mathematical importance expected at a general top-four mathematics journal.

These remain different questions.

# Recommendation

## Reject in the present form at a general top-four mathematics journal.

Revision 118 is a genuine and substantial revision. It does not merely repackage v117. It supplies two pieces that R117 explicitly requested:

- a higher-defect conductor/action-rank mechanism, including a codimension-two quotient dichotomy; and
- a nonreduced multigenerator family in arbitrary embedding dimension and nilpotence order, together with a global fat-point transport theorem on projective space.

I did **not** find a fatal counterexample to the new headline statements during this review.

Nevertheless, the new results do not yet change the top-four assessment. The reason is now quite precise. The higher-defect theorem organizes stable images into conductor flags, but it does not classify the full higher-defect nonsurjectivity schemes. The nonreduced multigenerator theorem is exact, but its entire scheme structure collapses to a pure power of a single irreducible Cartier determinant divisor. The higher-dimensional global theorem is a clean triangular monomial transport for one standard fat-point class. These are meaningful advances, but they still stop short of a new general geometry of multiplication failure.

In addition, the nearest-source priority item from R117 remains explicitly unresolved: the complete theorem text of Ballico 1993 has still not been compared theorem by theorem. At a venue where the case rests heavily on novelty of a broad failure-locus package, that is not a minor bibliographic loose end.

# 1. What v118 genuinely accomplishes

A harsh report should not pretend that the revision failed to answer the previous referee.

## 1.1 The higher-defect direction is no longer absent

Theorem  \(\ref{thm:higher-defect-strata}\) introduces a canonical stable generated algebra after unit normalization. On an exact-rank stratum of the stable multiplication map, the image becomes a subalgebra bundle \(E\), and the action of \(E\) on \(B/E\) produces the conductor
\[
J=\ker(E\to \operatorname{End}(B/E)).
\]
The quotient data
\[
C=E/J\subset Q=B/J
\]
is then organized by the exact rank of the action. This is a real structural improvement over the defect-two-only picture of v117.

The relative point is also important: the manuscript does not merely classify geometric fibres. It keeps the determinantal scheme structure of the action-rank strata and proves base-change compatibility **within** those strata. The rank-jump example
\[
E=\langle 1,\,s z^2+z^3,\,z^4\rangle\subset \mathbb C[s][z]/(z^5)
\]
correctly exhibits a nonreduced rank-one locus \(s^2=0\) and shows why unrestricted conductor formation cannot be expected to commute with specialization.

That example is useful and should remain.

## 1.2 The codimension-two theorem is an honest next-codimension theorem

For a unital subalgebra \(E\subset B\) with \(B/E\) of rank two, the manuscript proves scheme-theoretically that the action has rank at most two. The proof through the isomorphism
\[
\bigwedge^2\mathfrak{sl}_2\longrightarrow\mathfrak{sl}_2
\]
is clean and works over the coefficient ring, not only pointwise.

The two exact-rank strata then have a concrete quotient interpretation:

- rank one: a rank-three quotient with scalar subalgebra;
- rank two: a rank-four quotient \(Q\) which is rank two over a rank-two algebra \(C\).

This is materially better than simply saying that the hyperplane theorem should have a higher-codimension analogue.

## 1.3 The fat-point theorem is a real nonreduced multigenerator calculation

For
\[
B_{e,h}=\mathbb C[z_1,\ldots,z_e]/(z_1,\ldots,z_e)^h,
\qquad
N=\binom{e+h-1}{e+1},
\]
the theorem identifies, on the entire generating \((e+1)\)-plane Grassmannian, the stable zeroth Fitting ideal as
\[
\operatorname{Fitt}_0\operatorname{coker}(\operatorname{Sym}^m\mathcal A\to B_{e,h})
=
\mathcal I_\Delta^N
\qquad (m\ge h-1).
\]

The determinant exponent is not guessed from examples. After a unit-frame normalization, the multiplication problem becomes the substitution endomorphism \(T_x\), and the \(\mathfrak m\)-adic filtration gives
\[
\det T_x
=
\prod_{j=1}^{h-1}\det(\operatorname{Sym}^j M)
=
(\det M)^N.
\]
I find this calculation correct and useful.

For \(e=2\), this indeed gives a three-generator theorem for every \(\mathbb C[x,y]/(x,y)^h\), not a single low-length test algebra. Thus R117's request for a nonreduced multigenerator family has been answered in a literal and nontrivial sense.

## 1.4 The global fat-point transport theorem is stronger than a formal finite-algebra example

Theorem \(\ref{thm:fat-conductor}\) proves a coherent-cokernel comparison for the order-\(h\) fat point in \(\mathbb P^e\) once \(n\ge 2h-1\). The triangular monomial argument is elementary but effective, and the boundary example at \(n=2h-2\) shows that the uniform bound cannot be lowered if it must hold simultaneously over all generating dimensions and all \(m\ge2\).

This does give the finite-algebra calculation an actual global-section consequence.

## 1.5 The relative formalism is cleaner

Several R117 proof-architecture requests are now properly addressed:

- the generating open is defined functorially;
- the hyperplane cokernel line is written canonically;
- the moving projective bundle is identified;
- the relative curve theorem states base-change hypotheses;
- the distinction between universally base-changing coherent cokernels and non-universally base-changing primary decompositions is explicit.

These changes improve the paper and should not be undone.

# 2. The central limitation: the higher-defect theorem is a conductor-stratification theorem, not a classification of higher-defect failure geometry

The title and abstract now place substantial weight on "conductor strata." That is justified.

What is not yet justified is treating this as a general solution of higher-defect multiplication failure.

Theorem \(\ref{thm:higher-defect-strata}\) begins by passing, after the stable degree \(d-1\), to the generated algebra \(E\). On the exact-rank-\(s\) locus of the stable multiplication map, one then studies the action of \(E\) on the quotient \(M=B/E\). The conductor and quotient flag are extracted from that action.

This is a useful organization of the stable image. But it is not a primary decomposition, component classification, singularity theorem, or even an equation theorem for the whole nonsurjectivity locus in codimension \(r>1\).

The manuscript itself correctly exposes this limitation in Proposition \(\ref{prop:extreme-corank}\): for \(r>1\), the unital-subalgebra scheme is the **extreme-corank** Fitting locus
\[
V\!\left(\operatorname{Fitt}_{r-1}\operatorname{coker}(\operatorname{Sym}^m W\to B)\right),
\]
not the whole zeroth-Fitting nonsurjectivity scheme.

That distinction is mathematically crucial and, in my view, decisive for the venue assessment.

The higher-defect theorem tells us how to parameterize the points where the stable image itself is a specified subalgebra and how its conductor action stratifies. It does **not** tell us what the full multiplication-failure scheme looks like when the image has intermediate corank, how its irreducible components meet, what nilpotent structure lies on those strata, or how the different conductor ranks interact inside one ambient failure scheme.

For a top-four paper, I would expect the new conductor flag to be the input to such a theorem, not the endpoint.

# 3. The codimension-two quotient dichotomy is elegant, but it remains a low-rank action theorem

The codimension-two result is probably the cleanest new conceptual theorem in v118.

It is also very special.

Its decisive algebra is the fact that commuting trace-zero \(2\times2\) matrices span at most one line because
\[
\bigwedge^2\mathfrak{sl}_2\to\mathfrak{sl}_2
\]
is an isomorphism. This forces only two action-rank possibilities and produces the rank-three/rank-four quotient dichotomy.

That mechanism does not yet suggest a comparable classification when \(B/E\) has rank three or more. In higher rank, commuting subalgebras of matrix algebras have a substantially richer geometry, and the action-rank stratification alone is not close to a classification.

Thus the theorem should be sold as a complete **rank-two quotient-module case**, not as evidence that a general higher-defect quotient theory has already been achieved.

There is also a second limitation. Even in codimension two, the theorem classifies the conductor quotient flags attached to a unital subalgebra \(E\). It does not classify the full codimension-two multiplication failure scheme on the generating Grassmannian. Those are different tasks.

A next revision should make this distinction impossible to miss in the abstract and introduction.

# 4. The nonreduced multigenerator theorem answers R117 formally, but it chooses the geometrically easiest possible nonreduced structure

This is the strongest reason why the top-four recommendation does not change.

Theorem \(\ref{thm:fat-primary}\) is exact. But after unit normalization, the entire stable failure scheme is controlled by one determinant:
\[
\det T_x=(\det M)^N.
\]
Consequently the scheme is simply
\[
N\Delta
\]
where \(\Delta\) is an irreducible Cartier determinant divisor.

Once this identity is established, almost all of the advertised primary structure is automatic:

- every ordinary power is primary;
- there is one associated prime;
- there are no embedded associated points;
- the nilpotency index is the exponent;
- the generic transverse length is the exponent.

These are consequences of taking a power of a prime Cartier divisor in a regular ambient scheme.

So the theorem gives a genuine nonreduced family, but its nonreducedness is **pure multiplicity along one divisor**. It does not exhibit the harder phenomena that make nonreduced multigenerator failure geometry interesting:

- multiple primary components;
- embedded primes;
- non-Cartier nilpotent structure;
- collisions of conductor strata;
- nontrivial normalization;
- interaction between tangent-rank degeneration and higher-order coefficients;
- or a primary structure not already forced by one determinant character.

This matters because R117 did not merely ask for any nonreduced example. It asked for evidence that the multigenerator theory continues beyond the reduced Haiman-diagonal situation into genuinely new finite-algebra geometry.

v118 technically meets that request. It does not yet meet its conceptual ambition.

# 5. The higher coefficients disappear from the fat-point determinant, which is both the strength and the limitation of the theorem

A revealing feature of the proof is that the determinant depends only on the linear coefficient matrix \(M\). All higher coefficients of the \(x_i\) are irrelevant to \(\det T_x\).

This is a beautiful filtration calculation.

It also means that the stable failure divisor is, scheme-theoretically, just the pullback of the classical determinant hypersurface under the tangent map
\[
K\to\mathfrak m/\mathfrak m^2,
\]
with a fixed multiplicity \(N\).

Thus the arbitrarily large nilpotence order \(h\) changes the exponent but does not create a new support, new component, or new singularity type beyond the generic determinantal hypersurface. The singular locus is again the standard rank-\(\le e-2\) determinant singularity.

For a specialist result, that rigidity is attractive. For a general top-four claim, it weakens the assertion that arbitrary embedding dimension and nilpotence order have produced a genuinely new geometric regime.

The next step should be a family in which the higher jets actually affect the primary geometry.

# 6. The global fat-point transport is clean but primarily a saturation/combinatorics theorem

Theorem \(\ref{thm:fat-conductor}\) is well organized. Its proof reduces the global kernel-filling problem to the fact that the integer intervals
\[
[jh,jn]
\]
have no gaps once \(n\ge2h-1\), and then uses a triangular monomial basis.

I find no problem with this argument.

But its conceptual content should be assessed accurately. The passage to arbitrary projective dimension does not introduce new higher-dimensional projective geometry. The support is one standard fat point, coordinates reduce the calculation to monomial degree intervals, and the proof is a triangular basis argument.

In other words, the theorem is a strong **transport lemma**, not a new classification theorem on projective varieties.

At a top-four level I would want the transport mechanism to survive for a broader and geometrically variable class of zero-dimensional schemes—mixed fat points, unions, non-monomial local schemes, local complete intersections, or another class where the regularity problem itself becomes nontrivial—and then to produce a new global failure theorem.

# 7. The two main v118 additions remain largely parallel rather than forming one new theory

The response to R117 presents v118 as addressing both higher-defect quotient mechanisms and nonreduced multigenerator geometry.

Both claims are true.

But the paper does not yet make the two mechanisms interact in a way that produces a new theorem.

The higher-defect section gives conductor flags for general finite algebras and a complete rank-two quotient-module case. The fat-point section gives a special family whose stable failure ideal is a determinant power. The latter is not derived as a deep application of the conductor-stratification theorem; it is solved directly by the \(\mathfrak m\)-adic substitution determinant.

This matters for the paper's conceptual unity. At present the article contains two successful exact mechanisms:

1. stable-image/conductor stratification;
2. tangent-determinant rigidity for a homogeneous truncated local algebra.

A top-four case would be much stronger if the first mechanism actually predicted and controlled the second, or if together they yielded a classification in a substantially broader class.

# 8. The nearest-source priority problem is still open, and this remains a top-four blocker

The authors continue to state honestly that E117.1 is open.

That is the correct scholarly position.

The public Wiley record confirms that E. Ballico's paper *On the Failure Locus of Higher Order Properties of Embeddings in Projective Spaces* appeared in *Mathematische Nachrichten* 163 (1993), pages 5--13. In this review session, as in the manuscript's audit, the complete theorem text was not available through the public route I could inspect. I therefore cannot certify overlap or non-overlap.

The correct conclusion is not that the present results are anticipated. It is also not that they are new.

It is that the nearest historical comparison is incomplete.

At a specialist journal, that gap might be resolved during revision. At a general top-four journal, where the significance case depends on presenting a broad new failure-scheme package, I would not recommend acceptance while the nearest-source comparison remains unresolved.

No amount of build provenance or exact finite diagnostics substitutes for this literature obligation.

# 9. The broader subalgebra/generator literature raises the novelty burden further

The expanded v118 literature section is materially better than the v117 discussion.

The paper now explicitly acknowledges:

- field-level classifications of maximal subalgebras;
- projective varieties of subalgebras and their vanishing ideals;
- the classical generator and polygenerator schemes described by minors;
- standard Hilbert and nested-Hilbert constructions;
- the classical faithful-action viewpoint;
- the classical symmetric-power determinant identity.

That honesty should be retained.

It also sharpens the question: what is the irreducible new conceptual statement that remains after those inputs are removed?

For the higher-defect theorem, the answer appears to be the organization of the specified inclusion \(E\subset B\), quotient \(B/E\), conductor, and exact action-rank scheme into a functorial quotient flag.

For the fat-point theorem, the answer is the exact exponent of the tangent determinant in the stable multiplication Fitting ideal and the global section transport.

Those are real contributions. The paper has not yet demonstrated that either has the breadth or downstream consequences expected from a general top-four paper.

I am **not** claiming that these precise theorems are already in the cited literature. I am saying that the current paper still carries the burden of showing why its refinements fundamentally change the subject rather than sharpen known subalgebra/generator geometry.

# 10. The unrestricted ambient problems still remain outside the new flagship theorems

The complete 91-page manuscript preserves the broader quadratic, polar, wall, and unrestricted hyperplane developments.

That archival preservation is useful, but it also shows the remaining boundary.

The new v118 flagship theorems do not solve the unrestricted ambient Grassmannian problems that motivated much of the earlier program. They instead give exact structure on:

- stable-image exact-rank strata;
- extreme-corank subalgebra loci;
- hyperplanes;
- reduced three-plane contacts;
- and one homogeneous truncated-local-algebra family.

There is nothing wrong with specializing to tractable families. But a general top-four paper needs one result whose significance is not primarily "a complete family inside a harder unresolved ambient theory."

I still do not see that theorem.

# 11. Proof-level and statement-level revisions required independently of venue

I found no fatal contradiction, but I would require the following cleanup even for a specialist-journal version.

## 11.1 State the scope of the higher-defect theorem in the abstract with the same precision as Proposition \(\ref{prop:extreme-corank}\)

The phrase "in codimension two the controlling quotients have rank three or four" can be read too broadly.

The theorem concerns conductor quotient flags of the **stable generated subalgebra on exact-rank strata**. It does not say that every point of the codimension-two nonsurjectivity scheme is classified by one of two quotient types.

The abstract should say this directly.

## 11.2 Make the quotient-flag functor completely explicit

In Theorem \(\ref{thm:higher-defect-strata}\), the phrase "flags \(B\twoheadrightarrow Q\supset C\)" should specify in the theorem statement itself that:

- \(Q\) is a quotient **algebra** of \(B\);
- \(C\) is a unital subalgebra;
- \(Q/C\) is locally free of the indicated rank;
- the action map is the specified split subbundle injection.

The proof uses all of these properties. The statement should not look module-theoretic.

## 11.3 Isolate the relative cyclic-vector argument in the codimension-two theorem

The passage from a rank-two subalgebra \(C\subset\operatorname{End}(M)\) to \(M\) being locally free of rank one over \(C\) is correct on the exact-rank-two stratum, but it is important enough to deserve a short lemma.

State the open cover on which a cyclic vector exists, prove that the determinant defining cyclicity is invertible there, and record compatibility with base change. This will make the relative quotient-tower statement easier to verify.

## 11.4 Identify the fat determinant divisor globally as a standard Schubert divisor

The proof currently argues on a frame cover that the linear coefficient matrix is generic and its determinant is irreducible, then descends integrality.

A cleaner global proof is available: the map
\[
K\to\mathfrak m/\mathfrak m^2
\]
is the universal projection of an \(e\)-plane, and the vanishing of its determinant is the pullback of the standard Schubert divisor on \(\operatorname{Gr}(e,\mathfrak m)\). State this identification and use the known irreducibility/primality of that divisor.

That would make the global primary argument visibly coordinate-free.

## 11.5 Clarify the low-degree meaning of the zero Fitting ideal

For \(m<h-1\), the theorem states that the zeroth Fitting ideal is zero.

Since the failure scheme is defined by that ideal, this means the failure scheme is **all of \(X\)**, not empty. Say this explicitly. The current statement is algebraically correct but easy to misread.

## 11.6 Make the moving-fat-point relative parameter space canonical

The corollary says that coordinate charts give the relative determinant Schubert divisor with free higher-jet parameters and concludes that the total divisor is integral.

Write down the relative bundle over \(\mathbb P^e\), its Grassmannian, and the determinant line map. Then integrality and Cartier structure should be proved from that relative construction rather than inferred primarily from coordinate charts and fibre descriptions.

## 11.7 Keep the computational receipts out of the logical burden of proof

The current text already says that the exact symbolic regressions are not proof certification. Keep it that way.

The finite checks are useful provenance. They should not grow into a second argument for theorem validity or significance.

# 12. Disposition of the R117 mandatory items

My assessment is:

| R117 item | v118 status | Referee assessment |
|---|---|---|
| E117.1 Ballico 1993 theorem-level comparison | **open** | still a real priority blocker |
| E117.2 broader novelty audit for universal hyperplane result | improved, not exhaustively closed | the new audit is useful, but the top-four novelty burden remains |
| E117.3 state the three-plane/Haiman novelty boundary | closed | v118 now does this correctly |
| E117.4 nonreduced multigenerator theorem | formally closed | the fat-point family is genuine, but geometrically it is a pure Cartier power |
| E117.5 higher-defect mechanism | substantially addressed | conductor flags and codimension two are real advances, but not a full failure-scheme theory |
| E117.6 formalize relative constructions | substantially closed | only the cleanups in Section 11 remain |
| E117.7 preserve primary-article architecture | closed | the 26-page article remains coherent |

A future referee should not recycle E117.3, E117.6, or E117.7 as though nothing changed. The main new issue is that the two successful responses to E117.4--E117.5 are still structurally narrower than the top-four narrative suggests.

# 13. New mandatory revisions arising from v118

## E118.1 — Close the Ballico 1993 comparison

Obtain the complete article and give a theorem-by-theorem comparison.

The comparison should explicitly cover:

- failure loci versus Fitting schemes;
- fixed versus moving finite contacts;
- higher-order multiplication or osculating failure;
- conductor transport;
- quotient/Hilbert incidences;
- and whether nonreduced scheme structure appears in Ballico's formulation.

Until this is done, do not make a broad priority claim.

## E118.2 — Separate conductor-stratum classification from full failure-scheme classification

Rewrite the abstract, introduction, and theorem roadmap so that readers cannot confuse:

- classification of stable-image/conductor flags;
- the extreme-corank subalgebra Fitting locus;
- and the full zeroth-Fitting nonsurjectivity scheme.

For \(r>1\), these are not the same object.

## E118.3 — Prove a theorem on the full codimension-two failure scheme

This is the most natural next mathematical step.

Use the new rank-three/rank-four quotient dichotomy to say something nontrivial about the **whole** codimension-two multiplication failure scheme, not only the unital-subalgebra/extreme-corank locus.

For example, determine components, generic coranks, primary structure, singularities, or a dense-open normal form.

Without such a theorem, the quotient flag remains a structural reparameterization rather than a completed failure theory.

## E118.4 — Move beyond pure Cartier-power nonreducedness

Produce a multigenerator family in which the nonreduced scheme is not just \(\mathcal I_\Delta^N\) for one prime Cartier divisor.

A convincing target would exhibit at least one of:

- several associated primes;
- an embedded component;
- a non-Cartier primary component;
- collision of distinct conductor strata;
- higher-jet dependence of the defining ideal;
- or a primary decomposition not forced by a determinant character.

The paper already has an embedded hyperplane chart in a small noncurvilinear algebra. The missing step is a **systematic multigenerator theorem** of that complexity.

## E118.5 — Make the higher-defect and nonreduced mechanisms interact

At present they are parallel developments.

A stronger paper would use the conductor flag to predict, organize, or prove the primary geometry of a family such as the truncated local algebras, and then extend that mechanism beyond them.

This would turn two exact calculations into one theory.

## E118.6 — Broaden the global transport beyond a single homogeneous fat point

The dimension-independent bound \(n\ge2h-1\) is useful, but the proof is monomial.

Extend the transport to a geometrically variable class where the regularity problem is nontrivial: mixed fat points, unions, nonmonomial zero-dimensional schemes, curvilinear/noncurvilinear mixtures, or another natural family.

A theorem of this kind could give the global side independent interest.

## E118.7 — Complete the formal cleanups in Section 11

These are not top-four significance issues, but they should be resolved before any final specialist submission.

# 14. What would materially change the top-four assessment

Another round of source receipts, finite substitution checks, or larger values of \(e\) and \(h\) will not change my recommendation.

Nor will merely increasing the exponent \(N\): the geometry remains a powered determinant divisor.

A renewed general top-four case would require a theorem that changes the scale of the subject. Examples include:

1. **Full codimension-two failure geometry.** Use the quotient-tower theorem to classify a substantial part of the zeroth-Fitting nonsurjectivity scheme.

2. **Higher-rank conductor geometry.** For \(B/E\) of rank at least three, replace the action-rank stratification by a moduli/primary theorem with actual equations and component structure.

3. **Non-Cartier multigenerator primary structure.** Produce a broad nonreduced family with embedded or multiple associated components and prove its exact primary decomposition.

4. **A global theorem beyond monomial fat points.** Establish a conductor transport on a genuinely variable higher-dimensional zero-scheme family and derive new projective geometry from it.

5. **A bridge to the unrestricted ambient Grassmannian.** Show that the finite quotient/conductor mechanisms control a dense open or a major component of the original unrestricted failure problem.

Any one of these, if sufficiently strong, could alter the significance assessment.

# 15. Correctness assessment of the new v118 mathematics

Within the scope of this review, I found no fatal counterexample to:

- stable degree truncation at \(d-1\) after unit normalization;
- independence of stable Fitting ideals;
- construction of the conductor action-rank strata;
- the quotient-flag equivalence on exact-rank strata;
- the scheme-theoretic rank-at-most-two statement for codimension two;
- the rank-three/rank-four quotient dichotomy;
- the nonreduced rank-jump example \(s^2=0\);
- the substitution presentation for \(B_{e,h}\);
- the determinant exponent \(N=\binom{e+h-1}{e+1}\);
- the primary-power description of the universal fat-point family;
- the stable threshold \(m=h-1\);
- the global saturation bound \(n\ge2h-1\);
- or the boundary obstruction at \(n=2h-2\).

This is **not** proof certification. It means that my negative recommendation is not based on a discovered contradiction in these new statements.

The negative recommendation is instead about the scale and novelty of what the correct statements presently achieve.

# 16. Final recommendation

Revision 118 is stronger than revision 117.

It has:

- a genuine higher-defect conductor stratification;
- a complete codimension-two quotient-module dichotomy;
- an explicit nonreduced rank-jump scheme;
- a uniform nonreduced multigenerator theorem for truncated local algebras;
- an exact determinant exponent in arbitrary embedding dimension and nilpotence order;
- a sharp uniform fat-point transport on \(\mathbb P^e\);
- cleaner relative formulations;
- and a coherent 26-page primary article.

These are substantive advances.

Nevertheless, I recommend **rejection in the present form at a general top-four mathematics journal**.

The decisive reasons are now:

- the higher-defect theorem classifies stable-image conductor flags, not the full higher-defect failure scheme;
- the codimension-two theorem is a special rank-two quotient-module action result and has not yet been converted into full codimension-two failure geometry;
- the new nonreduced multigenerator family is scheme-theoretically only a pure power of one irreducible determinant divisor;
- its higher-order coefficients do not affect the stable failure ideal;
- the projective-space transport is a strong monomial saturation lemma rather than a new higher-dimensional geometric classification;
- the two new mechanisms remain largely parallel instead of combining into a general theory;
- the unrestricted ambient problems remain separate;
- and the nearest Ballico 1993 theorem-level priority comparison is still unresolved.

A strong specialist paper is increasingly visible, and the v118 primary article is much closer to a coherent specialist submission than earlier versions. But a renewed top-four submission should be driven by a new structural theorem of the kind listed in Sections 13--14, not by another enlargement of the same exact-diagnostics package.
