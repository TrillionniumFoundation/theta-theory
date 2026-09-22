# Referee II: harsh external-referee-style report on A2 revision 118

**Manuscript:** *Conductor strata and nonreduced multiplication failure schemes*  
**Author:** Qian Qi  
**Repository:** TrillionniumFoundation/theta-theory  
**Reviewed revision branch:** revision/a2-v118-higher-defect-nonreduced-generators-2026-09-22  
**Reviewed product head:** 44bfc648ead008896a6981a7302a6d5ab8b21bb8  
**Current source receipt:** 84ea29f752ca223bbcda1eb8d155adc02082dc28  
**Earlier identical mathematical-source tree used by the first v118 review:** c87bfdad8d97e68637d269e656b46c4cce85551e  
**Controlling R117 report:** 2c6f180fa0baf23386e0a46a64abe7503ea65b00  
**Date:** 22 September 2026

## Status and independence of this report

This is a second, owner-requested, AI-assisted external-referee-style assessment. It was not commissioned by *Annals of Mathematics*, *Inventiones Mathematicae*, *Journal of the American Mathematical Society*, *Acta Mathematica*, or any other journal, and it must not be represented as a journal-issued referee report or editorial decision.

A first independent v118 review already exists in the repository. I have therefore treated this as a Referee-II re-reading of the current v118 branch rather than overwriting that report. I independently inspected the primary article, the complete-manuscript provenance, the response to R117, the literature audit, the two new mathematical sections, and the relevant inherited finite-algebra and conductor arguments.

There is a small provenance subtlety worth fixing at the outset. The current SOURCE_RECEIPT and BUILD_RECEIPT name 84ea29f752ca223bbcda1eb8d155adc02082dc28 as the source commit, whereas the earlier v118 review froze c87bfdad8d97e68637d269e656b46c4cce85551e as the mathematical-source commit. Direct comparison shows that c87bfdad... to 84ea29f... changes only one workflow line in .github/workflows/a2-v118-build-publish.yml; the mathematical source tree is unchanged. Thus there is no hidden mathematical revision between the two reviews.

The current build receipt reports a 26-page primary article and a 91-page complete manuscript, with no unresolved references, duplicate labels, or overfull boxes. I treat those receipts as provenance and reproducibility evidence only, not as proof or novelty certification.

# Recommendation

## Reject in the present form at a general top-four mathematics journal.

Revision 118 is substantially stronger than v117. In particular, two of the main mathematical requests in R117 have been answered literally:

1. there is now a higher-defect stable-image/conductor/action-rank mechanism, including a complete rank-two quotient-module dichotomy in codimension two; and
2. there is now a nonreduced multigenerator theorem for the entire family
   \[
   B_{e,h}=\mathbb C[z_1,\ldots,z_e]/(z_1,\ldots,z_e)^h
   \]
   in arbitrary embedding dimension and nilpotence order, together with a global transport theorem to order-h fat points in projective space.

I did not find a fatal counterexample to these new headline statements in this review.

The negative recommendation is therefore not based on a discovered contradiction. It is based on the scale of the advance relative to the claimed general-journal level.

The two new mechanisms still stop one conceptual step short of the geometry that would change the top-four assessment:

- the higher-defect result classifies stable generated subalgebras and their conductor quotient flags, but not the full higher-defect zeroth-Fitting nonsurjectivity scheme;
- the fat-point result gives an exact nonreduced multigenerator scheme, but that entire primary structure is a pure power of one classical determinant divisor, governed only by the first-order tangent map;
- the global projective-space theorem is a strong triangular saturation lemma for one homogeneous fat-point class, with its advertised uniform sharpness witnessed at rank one rather than at the flagship rank e+1;
- the two new mechanisms are presented in parallel but are not yet combined into a general primary theory;
- the unrestricted ambient failure geometry remains separate;
- and the nearest-source Ballico 1993 theorem-level comparison is still explicitly open.

For a specialist algebraic-geometry or commutative-algebra venue, the current package is becoming coherent and substantial. For a general top-four journal, I still do not see the theorem that changes the conceptual scale of the subject.

# 1. What v118 genuinely fixes

A harsh report should record real progress rather than recycle objections that have been answered.

## 1.1 E117.4 is closed in the literal sense

Theorem thm:fat-primary is not a toy example. It treats every e >= 2 and h >= 3 on the entire ideal-generating (e+1)-plane Grassmannian of the truncated local algebra B_{e,h}. After unit normalization, the stable multiplication map becomes the substitution endomorphism
\[
T_x:B_{e,h}\to B_{e,h},\qquad z_i\mapsto x_i,
\]
and the m-adic filtration gives
\[
\det T_x
=
\prod_{j=1}^{h-1}\det(\operatorname{Sym}^j M)
=
(\det M)^{N},
\qquad
N=\binom{e+h-1}{e+1}.
\]
This is a clean exact calculation over arbitrary coefficient rings.

For e=2 it yields a genuine three-plane theorem for every C[x,y]/(x,y)^h, not merely a single low-length algebra. The low-degree threshold m=h-1 is also genuinely exact by source-rank obstruction.

The previous request for a nonreduced multigenerator family has therefore been answered.

## 1.2 E117.5 is substantially addressed

Theorem thm:higher-defect-strata introduces a canonical stable generated algebra E after unit normalization. On an exact-rank stratum, E is a subalgebra bundle, and its action on M=B/E has kernel equal to the conductor. The resulting quotient flag
\[
C=E/J\subset Q=B/J
\]
retains the specified inclusion into B, the quotient module, and the exact action-rank scheme structure. This is more than a closed-point classification.

The rank-jump example
\[
E=\langle1,sz^2+z^3,z^4\rangle\subset\mathbb C[s][z]/(z^5)
\]
is particularly useful: the exact-rank-one locus is s^2=0, while the conductor rank jumps after specialization. This is a concrete reason the theorem must be stratified scheme-theoretically rather than stated only fibrewise.

## 1.3 The codimension-two theorem is a real structural theorem

When B/E has rank two, the manuscript proves scheme-theoretically that the image of E in End(B/E) has rank at most two. The proof through
\[
\bigwedge^2\mathfrak{sl}_2\longrightarrow\mathfrak{sl}_2
\]
is short but legitimate over the coefficient ring.

The two resulting cases are clean:

- action rank one gives a rank-three quotient with scalar subalgebra;
- action rank two gives a rank-four quotient Q which is rank two over a rank-two algebra C.

This is the correct next-codimension analogue of the rank-two quotient phenomenon in the hyperplane theorem, at least at the level of conductor flags.

## 1.4 The relative formalism is much cleaner

The new finite preliminaries explicitly state that “generating” means ideal/module generation, not generation as a unital algebra. The unit-cover lemma is functorial. The hyperplane cokernel line is written canonically. The moving projective bundle is identified. The manuscript also correctly limits arbitrary-base-change claims for conductors to exact-rank strata and keeps primary-decomposition claims separate from universally base-changing coherent cokernels.

These are meaningful improvements in proof architecture.

# 2. A terminology issue that exposes the precise novelty boundary of the fat-point theorem

The manuscript is correct to define its generating open as ideal generation, not algebra generation. But the distinction is so important in the fat-point theorem that it should be made impossible to miss.

For the local algebra B_{e,h}, an (e+1)-plane A lies in the manuscript's generating open exactly when A contains a unit after base change. After unit normalization one writes
\[
A=\langle1,x_1,\ldots,x_e\rangle
\]
with x_i in the maximal ideal.

The determinant divisor Delta is the locus where the classes of the x_i fail to span m/m^2. By Nakayama, away from Delta the x_i generate m and hence 1,x_1,...,x_e generate B_{e,h} as a unital algebra. Thus the support of the stable multiplication failure scheme is exactly the complement of the minimal algebra-generator locus inside the larger ideal-generating Grassmannian.

This observation sharpens, rather than weakens, the theorem:

> the genuinely new scheme-theoretic information in thm:fat-primary is the multiplicity N of the classical first-order generator determinant, together with its identification as the multiplication Fitting scheme.

But it also places a strict limit on the top-four narrative. The support is a classical determinant failure locus and all higher coefficients of the x_i disappear from the stable ideal. Increasing h does not create new component geometry; it only changes the exponent through the symmetric-power determinant character.

I strongly recommend renaming or repeatedly qualifying the relevant parameter space as the “ideal-generating” or “unit-generating” Grassmannian. Otherwise a reader can easily misread “generating (e+1)-planes” as algebra-generating planes, in which case the existence of a nonempty stable failure divisor looks paradoxical.

# 3. The fat-point theorem is exact, but its nonreduced geometry is a pure Cartier thickening

This is the principal significance limitation of v118.

The theorem proves
\[
\operatorname{Fitt}_0\operatorname{coker}(\operatorname{Sym}^m\mathcal A\to B_{e,h})
=
\mathcal I_\Delta^N.
\]

Once Delta is known to be an integral Cartier divisor on a smooth ambient scheme, essentially all of the advertised primary structure follows formally:

- there is one associated prime;
- every power is primary;
- there are no embedded associated points;
- the nilradical index is N;
- the generic transverse length is N;
- the q-th ordinary power is I_Delta^{Nq}.

This is valid mathematics. But it is the easiest possible kind of nonreduced primary structure: a single smooth-in-codimension-one determinantal support with pure multiplicity.

The earlier R117 request was motivated by the hope that a genuinely multigenerator nonreduced theory would expose geometry unavailable in the reduced Haiman diagonal model. The present family does leave Haiman and it does have arbitrary embedding dimension, but the new nonreduced structure contains no interaction among several associated primes, no embedded component, no higher-jet-dependent primary component, and no collision of conductor strata.

The manuscript itself already contains a small noncurvilinear hyperplane chart with an embedded associated point:
\[
(ab,b^2)=(b)\cap(a,b)^2.
\]
Ironically, that small example displays a more difficult primary phenomenon than the flagship fat-point theorem. What is missing is a systematic multigenerator theorem of comparable complexity.

At a top-four level I would want the next theorem after thm:fat-primary to break the pure-Cartier-power regime.

# 4. The higher-defect theorem is a classification of stable-image conductor flags, not of the full failure scheme

Theorem thm:higher-defect-strata is useful, but its output must be described with precision.

After the stable degree, the multiplication image is an invertible E-module L^m inside B, where E is the generated algebra. The theorem then stratifies the action of E on M=B/E and extracts the conductor quotient flag C subset Q.

This organizes the stable image. It does not classify the whole nonsurjectivity geometry for codimension r>1.

Proposition prop:extreme-corank makes the distinction explicit. For a unital codimension-r plane W, the subalgebra condition is the extreme-corank locus
\[
V\!\left(\operatorname{Fitt}_{r-1}
  \operatorname{coker}(\operatorname{Sym}^m W\to B)\right).
\]
For r>1 this is not the same as the zeroth-Fitting failure locus.

Thus the new quotient flags currently describe one special determinantal stratum of the multiplication problem: the locus where the image collapses all the way to the original codimension-r subspace as a subalgebra. They do not determine:

- the components of the full Fitt_0 locus;
- intermediate corank strata;
- their generic primary structures;
- singularities where action rank changes;
- or how conductor flags control closures and intersections in the ambient Grassmannian.

For a general-journal paper, the conductor flag should become the engine for one of these geometric theorems. At present it is mainly a structural reparameterization.

# 5. The codimension-two quotient dichotomy is elegant but remains low-rank linear algebra until it controls geometry

The codimension-two theorem is probably the best conceptual addition in v118.

Its mechanism, however, is intrinsically 2-by-2. Commuting trace-zero two-by-two matrices are proportional because the bracket map on sl_2 is an isomorphism. That forces only two action-rank possibilities.

Nothing comparable is yet proved for rank(B/E) >= 3, where commuting subalgebras of matrix algebras have much richer families. More importantly, even in rank two the theorem is not yet turned into a classification of the full codimension-two multiplication failure scheme.

The natural next step is therefore not another abstract action-rank stratum. It is a theorem saying what the rank-three/rank-four quotient dichotomy actually does to Fitt_0:

- Which components occur?
- What are their dimensions?
- What are the generic coranks?
- Is one quotient mechanism a boundary of the other?
- What nilpotent structure appears on their intersection?
- Is the s^2=0 rank-jump example the local model of a systematic boundary phenomenon?

Until such questions are answered, the codimension-two theorem remains an attractive local structural lemma rather than a new global geometry.

# 6. The two v118 advances do not yet interact

This is, in my view, the deepest architectural weakness of the revision.

The higher-defect theory produces stable generated algebras, conductor flags, and action-rank strata.

The fat-point theory produces a determinant power from a filtered substitution endomorphism.

But the fat-point primary theorem is not derived from the conductor-stratum machinery in any substantive sense. Conversely, the conductor-stratum machinery is not used to predict the exponent N, associated primes, or singularities of the fat-point family.

They are two parallel exact arguments placed in one article.

A stronger theory would make one mechanism explain the other. For example:

- identify the conductor/action-rank geometry along successive rank strata of Delta;
- show how the quotient flag changes as the tangent matrix M drops rank;
- derive primary exponents from conductor data rather than from a standalone symmetric-power determinant character;
- or extend the fat-point calculation to a class where several conductor flags meet and the primary decomposition records that meeting.

That synthesis would be much more persuasive as a general theory of multiplication failure.

# 7. The global fat-point transport is useful, but its “sharpness” is not sharp for the flagship family

Theorem thm:fat-conductor proves the uniform bound n >= 2h-1 for every generating dimension k and every m >= 2. The proof by triangular monomial columns is clean, and the counterexample at n=2h-2 is correct for the uniform statement.

However, the boundary counterexample takes A=<1>, i.e. k=1.

The flagship nonreduced application uses k=e+1.

Therefore the manuscript has **not** shown that n >= 2h-1 is the optimal conductor threshold for the actual family used in cor:global-fat-primary. It has shown only that no smaller bound works uniformly across all k.

The text does explicitly say “no rank-specific sharpness is asserted,” which is mathematically responsible. But this also means that “sharp uniformly over generating ranks” should not carry much significance weight for the e+1-plane theorem.

There is an obvious research opportunity here. The P^1 theory has a rank-dependent sharp threshold n >= 2d-k. A genuinely higher-dimensional analogue, with a threshold depending on e,h,k and a matching obstruction, would make the global conductor theorem much deeper than the present monomial filling lemma.

# 8. The global theorem is still tied to one maximally homogeneous local algebra

The order-h fat point is an excellent test case because its associated graded algebra is the full truncated symmetric algebra. That is exactly why the substitution determinant becomes
\[
\prod_j\det(\operatorname{Sym}^jM).
\]

But this homogeneity is doing almost all the work.

The paper does not yet treat:

- mixed fat points;
- unions of fat points;
- nonhomogeneous Artin quotients;
- local algebras with relations in intermediate degree;
- non-Gorenstein deformations with varying Hilbert function;
- or a family in which the associated graded algebra itself varies.

A transport theorem for one of these classes would test whether the present method is robust or whether it is specific to the most symmetric truncated polynomial algebra.

For top-four significance, robustness matters more than enlarging e and h inside the same homogeneous model.

# 9. The nearest-source priority blocker remains open

E117.1 is still explicitly open in the manuscript, response, identity, and build receipt.

I independently retried the public Wiley route for E. Ballico, *On the Failure Locus of Higher Order Properties of Embeddings in Projective Spaces*, Math. Nachr. 163 (1993), 5–13, DOI 10.1002/mana.19931630102. The bibliographic record and references are publicly visible, but the PDF route redirected to the abstract/metadata page in this review session. I therefore do not have the theorem pages needed for a theorem-by-theorem comparison.

The only responsible conclusion is the manuscript's own conclusion: inaccessible full text is not evidence of novelty.

At a specialist venue, an editor might allow this comparison to be completed during review. At a general top-four venue, where the paper's case depends on a broad new package of failure-locus geometry, I would regard the unresolved nearest-source comparison as a hard originality blocker.

The expanded comparisons with maximal-subalgebra varieties, generator schemes, index forms, and Haiman are useful. They do not remove E117.1.

# 10. The novelty boundary of the fat-point result should be stated even more sharply

The manuscript already acknowledges that the symmetric-power determinant identity is classical linear algebra and that polygenerator opens are classical.

The sharpest honest novelty statement appears to be:

1. the support Delta is the minimal-algebra-generator determinant inside the larger ideal-generating Grassmannian;
2. the multiplication Fitting scheme is not merely Delta but the exact thickening N Delta;
3. the exponent N is computed by the filtered substitution determinant;
4. the same Fitting thickening is transported to global section multiplication on P^e in an explicit uniform degree range.

That is a clean contribution.

The paper should not allow phrases such as “complete nonreduced multigenerator geometry in arbitrary embedding dimension” to suggest that arbitrary nonreduced multigenerator algebras are classified. Only one highly symmetric local algebra family is.

# 11. The primary article is coherent, but the 91-page complete manuscript should not be the submission identity

The 26-page geometry article has a coherent spine:

- conductor transport;
- finite generating opens;
- rank-two quotient geometry;
- higher-defect conductor flags;
- reduced and nonreduced multigenerator families;
- primary contact calculations;
- literature boundaries.

That is a real improvement.

The 91-page complete manuscript retains many independent developments for archival continuity. That may be useful in the repository, but it weakens the identity of a journal submission.

For any serious submission, I would submit the primary article and keep the complete manuscript as supplementary or historical material unless an editor specifically requests it.

# 12. Proof and presentation requests independent of venue

I did not find a fatal proof error, but several points should be made more canonical.

## 12.1 Rename the generating open in the fat-point section

As explained above, “generating” here means ideal/module generating, not algebra generating. Use “ideal-generating,” “unit-generating,” or an equally explicit qualifier throughout the fat-point theorem and abstract.

Then state directly that Delta is the complement of the algebra-generating locus.

## 12.2 Identify Delta globally as a standard determinantal/Schubert divisor

The proof establishes irreducibility on a frame cover using the generic determinant. It would be cleaner to identify Delta intrinsically through the map
\[
K\to(\mathfrak m/\mathfrak m^2)\otimes\mathcal O_X
\]
as the determinant degeneracy divisor and compute its line bundle/class.

This would make primeness and the geometry of its singular strata visibly coordinate-free.

## 12.3 State explicitly that Fitt_0=0 for m<h-1 means the failure scheme is all of X

The algebra is correct, but the geometric meaning is easy to misread.

## 12.4 Make the relative moving-fat-point parameter space canonical

For moving p in P^e, write the relative jet algebra bundle, the relative Grassmannian, the augmentation kernel, and the determinant line map. Then prove integrality/Cartier structure of the total Delta from that relative construction.

## 12.5 Separate current-source provenance from workflow provenance

The current receipts name 84ea29f... as source commit, while the first v118 review used c87bfdad...; the source trees are mathematically identical and the only intervening change is workflow-only.

This is harmless, but future receipts should distinguish “commit containing the frozen source tree” from “commit that last changed mathematical source” so referees do not need to reconstruct that distinction manually.

## 12.6 Keep computational regressions auxiliary

The symbolic tests and build receipts are useful. They should remain evidence of reproducibility, not part of the logical proof burden.

# 13. Disposition of the R117 items

| R117 item | v118 status | Referee-II assessment |
|---|---|---|
| E117.1 Ballico 1993 theorem-level comparison | **OPEN** | still a hard originality blocker at top-four level |
| E117.2 broader novelty audit for universal hyperplane theorem | improved | useful bounded audit, not an exhaustive novelty certificate |
| E117.3 Haiman novelty boundary | closed | correctly attributed and scoped |
| E117.4 nonreduced multigenerator theorem | closed literally | real theorem, but pure determinant-power geometry |
| E117.5 higher-defect mechanism | substantially closed | real conductor/action-rank theory, not yet full Fitt_0 geometry |
| E117.6 relative formalization | substantially closed | only canonical-presentation cleanups remain |
| E117.7 primary-article architecture | closed | 26-page article is coherent |

A next review should not pretend that E117.3, E117.4, or E117.5 received no response. The correct criticism is that the responses are mathematically real but not yet broad enough to change the venue-level significance judgment.

# 14. New mandatory items from Referee II

## E118-II.1 — Complete the Ballico 1993 theorem-level audit

Obtain the full article and compare hypotheses and conclusions theorem by theorem with:

- fixed and moving failure loci;
- higher-order multiplication;
- finite-contact conductor transport;
- quotient/Hilbert incidences;
- and nonreduced Fitting structures.

Do not infer non-overlap from inaccessible text.

## E118-II.2 — Prove geometry for the full codimension-two Fitt_0 failure scheme

Use the rank-three/rank-four quotient dichotomy to determine a substantial part of the actual nonsurjectivity scheme, not only the extreme-corank subalgebra locus.

A convincing theorem should give components, dimensions, generic coranks, closure relations, or primary structure.

## E118-II.3 — Leave the pure-Cartier-power regime

Produce a systematic multigenerator family whose failure scheme has at least one genuinely harder primary phenomenon:

- multiple associated primes;
- an embedded component;
- non-Cartier primary support;
- higher-jet-dependent equations;
- or collision of distinct conductor strata.

The small B=C[x,y]/(x^2,y^2) hyperplane chart shows that such behavior exists. The missing contribution is a theorem, not an example.

## E118-II.4 — Make conductor strata predict primary geometry

Integrate the two new v118 mechanisms. Use action-rank/conductor data to explain or compute primary exponents and associated primes in a nontrivial family.

Without this bridge, the paper remains a collection of exact but parallel mechanisms.

## E118-II.5 — Determine a rank-specific higher-dimensional conductor threshold

For the flagship k=e+1 fat-point family, either improve n>=2h-1 or prove it sharp.

More ambitiously, develop a rank-dependent threshold analogous to n>=2d-k on P^1.

## E118-II.6 — Extend global transport beyond the standard homogeneous fat point

Treat a family with genuinely variable local algebra: mixed fat points, unions, nonhomogeneous Artin quotients, or another natural higher-dimensional zero-scheme class.

## E118-II.7 — Tighten novelty language around Delta

State explicitly that Delta is the classical first-order algebra-generator determinant and that the new content is the exact multiplication thickening, exponent, and global transport.

# 15. What would change the top-four assessment

More values of e and h, more build receipts, or more finite symbolic checks will not change this recommendation.

Nor will a larger exponent N: that still gives the same determinant support.

A materially different general-journal case would need at least one theorem of the following scale:

1. **Full codimension-two multiplication-failure geometry** derived from the quotient dichotomy.
2. **Higher-rank conductor geometry** for rank(B/E)>=3 with actual equations/components, not only exact-rank flags.
3. **A non-Cartier multigenerator primary theorem** with embedded or interacting associated components.
4. **A rank-sensitive global conductor theorem** in projective dimension e>=2 with a genuinely sharp threshold for the flagship family.
5. **A variable higher-dimensional zero-scheme transport theorem** whose geometry is not monomially homogeneous.
6. **A bridge to the unrestricted ambient Grassmannian**, showing that the finite conductor mechanisms control a major component or dense open of the original failure problem.

One strong result of this kind could change the scale of the paper.

# 16. Correctness assessment

Within the scope of this re-reading, I found no fatal counterexample to the following v118 claims:

- total-degree stabilization at degree d-1 after unit normalization;
- independence of stable Fitting ideals;
- construction of the exact-rank conductor flags;
- base-change compatibility within exact-rank strata;
- the scheme-theoretic rank-at-most-two statement in codimension two;
- the rank-three/rank-four quotient dichotomy;
- the nonreduced action-rank example s^2=0;
- the substitution presentation for B_{e,h};
- the determinant exponent N=binom(e+h-1,e+1);
- the pure-primary power I_Delta^N;
- the exact stable threshold m=h-1;
- the global saturation bound n>=2h-1;
- or the boundary failure at n=2h-2 for the uniform-in-k statement.

This is not proof certification. It records only that the negative recommendation is not based on a discovered contradiction in the new headline mathematics.

# 17. Final assessment

Revision 118 is a serious improvement and should not be judged as if it were v117.

It now contains:

- a genuine higher-defect stable-image/conductor stratification;
- an exact codimension-two quotient-module dichotomy;
- a nonreduced action-rank jump;
- an arbitrary-(e,h) multigenerator theorem for truncated local algebras;
- an exact determinant multiplicity;
- a global fat-point transport theorem on P^e;
- cleaner relative statements;
- and a coherent 26-page primary article.

Nevertheless, my recommendation remains **rejection in the present form at a general top-four mathematics journal**.

The decisive reason is not correctness. It is that the new mechanisms still describe comparatively tractable boundary cases of the broader geometry:

- stable conductor flags instead of the full higher-defect Fitt_0 scheme;
- a 2-by-2 action dichotomy instead of higher-rank quotient geometry;
- a pure determinant thickening instead of genuinely interacting nonreduced multigenerator components;
- one maximally homogeneous fat-point algebra instead of a variable higher-dimensional class;
- a uniform global threshold whose sharpness is witnessed outside the flagship rank;
- and an unresolved nearest-source priority comparison.

The strongest next revision would not enlarge the present catalogue. It would make the conductor flags, primary structure, and global transport interact in one theorem that controls a genuinely harder multiplication-failure scheme.
