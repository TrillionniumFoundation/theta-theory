# Independent harsh top-four referee report — A2 revision 127

**Manuscript:** *Determinantal boundary atlas, nilpotent depth, and polarized reconstruction in multiplication failure*  
**Author:** Qian Qi  
**Repository:** TrillionniumFoundation/theta-theory  
**Reviewed revision:** revision/a2-v127-determinantal-boundary-atlas-2026-09-23  
**Reviewed revision head:** d6c730f8caff71ddbc8208c0bd00cb90138de85a  
**Parent mathematical revision:** revision/a2-v126-global-nilpotent-specialization-2026-09-23  
**Controlling previous report:** review/a2-v126-independent-harsh-top4-2026-09-23  
**Principal source:** papers/A2-v17-boundary-information-coarsening/article/v127/geometry.tex  
**Principal PDF:** papers/A2-v17-boundary-information-coarsening/article/v127/geometry.pdf (46 pages in the source-bound build receipt)  
**Date:** 23 September 2026

## Status of this report

This is an owner-requested, AI-assisted external-referee-style report. It was not commissioned by *Annals of Mathematics*, *Inventiones Mathematicae*, *Journal of the American Mathematical Society*, *Acta Mathematica*, or any other journal, and it must not be represented as a journal-issued report.

I reviewed the v127 source itself, including the new boundary-atlas statements and proofs, the inherited v123/v125/v126 sections actually compiled into the article, the response to the v126 report, the issue matrix, the exact symbolic regressions, the literature audit, and the source-bound build evidence. I do not treat an issue-matrix label such as “addressed” or “closed” as mathematical evidence.

# Recommendation

## Reject in the present form at a general top-four mathematics journal.

Revision 127 is a substantial mathematical advance over revision 126. In particular, the determinant-completion proof
\[
d^5\in J
\]
is elegant, genuinely global, and appears correct. It gives the first uniform finite bound
\[
\widehat{\mathcal N}_R^6=0
\]
across every projection-rank chart. The nine mixed-kernel normal forms at projection corank two also provide a useful geometric organization of the first singular Schubert boundary, and the revision has correctly demoted deformation to the normal cone and flattening stratification to standard background.

Those improvements matter. I would not recycle the v126 objection that the paper merely packages an uncomputed filtration in a Rees algebra.

Nevertheless, the present manuscript is not yet at the standard required for a general top-four journal. The reasons are now sharper.

First, two of the central new proof passages do not yet justify the strength of the corresponding theorems. The corank-four argument shows the relevant representation occurs, but it does not prove that the **specific multiplication map in the coordinate ring** has nonzero projection to the determinant line; a nonzero scalar is being assumed rather than computed. The nine-orbit corank-two table is supported by one integer witness per orbit, but the proof does not establish that the ranks realized at those witnesses are the generic/maximal ranks needed to obtain the asserted coefficient-transverse open.

Second, the “finite associated-prime refinement” is much stronger than what is supplied by the brief appeal to flattening, Fitting ideals, and Noetherian induction. Constancy of Hilbert polynomial is not by itself constancy of fibrewise associated primes, embedded-versus-minimal status, incidences, or generic lengths. The proposition may well be salvageable, but it is not proved at the level stated.

Third, v127 still does not geometrically classify the associated graded object on all exceptional strata. For \(A_H\)-rank drop it gives depth bounds and a finite determinantal decision procedure; at projection corank three it gives an index-five/index-six dichotomy; at projection corank four it gives an exact index. These are important **depth theorems**, but they are not yet the all-boundary description of the schemes \(W_j\), their associated primes, multiplicities, and specialization laws that the preceding referee report requested.

Thus the project has moved from “canonical container without classification” to “real finite-depth structure plus a partially explicit atlas.” That is genuine progress. It is not yet a complete top-four boundary theorem.

# 1. What revision 127 genuinely accomplishes

A harsh report should not obscure the real advances.

## 1.1 The universal fifth determinant power is a strong lemma

On a Schur chart the paper writes
\[
\mathcal I_{\widehat D_R}=dJ,\qquad
J=I_6(\gamma_R\operatorname{Sym}^2M),
\]
where \(M=I_H\oplus T\) and \(d=\det T\).

The proof chooses
\[
G=(\gamma_R,\rho):
\operatorname{Sym}^2V
\xrightarrow{\sim}
S_R\oplus K
\]
and applies Laplace expansion to
\[
\det(G\operatorname{Sym}^2M).
\]
Since
\[
\det(\operatorname{Sym}^2M)=(\det M)^5=d^5,
\]
every term in the expansion contains a \(6\times6\) minor of
\(\gamma_R\operatorname{Sym}^2M\). Hence \(d^5\in J\).

This is concise, conceptual, and independent of the detailed rank pattern of \(A_H\), \(B_H\), and \(C_H\). It materially improves the global picture.

The consequence
\[
N^6=0
\]
for the local nilradical follows immediately from
\(\mathcal I_{\widehat D_R}=dJ\).

I regard this as one of the strongest new statements in v127.

## 1.2 The multiplication law of the graded nilpotent algebra is clarified

The identification
\[
N^j/N^{j+1}
\simeq
\mathcal L^{\otimes j}\otimes\mathcal O_{W_j}
\]
was already present through the residual-colon formalism. Revision 127 now spells out that the product is induced by the quotient multiplication
\[
\mathcal O_{W_i}\otimes
\mathcal O_{W_j}
\longrightarrow
\mathcal O_{W_{i+j}}.
\]

The local containment
\[
(J:d^{i-1})+(J:d^{j-1})
\subset
(J:d^{i+j-1})
\]
is the relevant algebra, and the class of \(1\otimes1\) maps to the generator in the next layer. Subject to the inherited residual-colon formula, this is a clean and useful observation.

It removes one datum from the classification problem: once the \(W_j\) are actually known, no extra scalar multiplication constants remain to be chosen.

## 1.3 The mixed-kernel orbit organization is useful

For \(A_H\) injective at projection corank two, the paper organizes
\[
\beta_H:H\otimes W\to E_H,\qquad
\dim H=\dim W=2,\quad \dim E_H=3,
\]
by the projective position of \(\mathbf P(\ker\beta_H)\) relative to the Segre quadric.

The resulting nine types are natural:

- rank three, kernel point off the Segre;
- rank three, kernel point on the Segre;
- rank two, secant kernel line;
- rank two, tangent kernel line;
- the two inequivalent ruling lines;
- rank one with dual tensor of rank two;
- rank one with dual tensor of rank one;
- the zero mixed map.

Keeping the two ruling families separate is mathematically meaningful because the nilpotent behaviour differs.

This is much better than treating “failure of mixed regularity” as one undifferentiated exceptional set.

## 1.4 The contact symbol survives without mixed regularity

The lemma proving that modulo \((\delta)\) the residual minors are generated by
\[
h_H(u)\operatorname{Sym}^4(\mathbf C_v^2)
\]
under the Segre factorization \(T=uv^t\) is a useful extension of the earlier mixed-regular analysis.

It identifies the first graded symbol at every \(A_H\)-injective corank-two point, including mixed-rank drops.

## 1.5 The manuscript now handles the standard geometry honestly

Revision 127 explicitly states that:

- the extended Rees algebra is standard;
- deformation to the normal cone is standard;
- flattening stratification is standard.

It cites Fulton and the Stacks Project accordingly.

This resolves the novelty-positioning criticism of revision 126.

# 2. Decisive correctness issue E127.1 — the corank-four membership \(d^4\in J\) is not yet proved

The theorem at projection corank four asserts
\[
d^3\notin J,\qquad d^4\in J.
\]

I find the exclusion \(d^3\notin J\) plausible and well motivated by
\[
\bigwedge^6\operatorname{Sym}^2V
=
\mathbb S_{(5,4,2,1)}V
\oplus
\mathbb S_{(4,4,4,0)}V,
\]
which contains no determinant-cube representation.

The second half is more delicate.

The proof correctly identifies the
\(\mathbb S_{(4,4,4,0)}V\)-component of the degree-twelve minors with the dual, up to determinant twist, of the Jacobian-quartic component. Smoothness of the Jacobian quartic ensures that this component of the degree-twelve generator space is nonzero.

The proof then observes that
\[
\mathbb S_{(4,4,4,0)}V
\simeq
(\det V)^4\otimes(\operatorname{Sym}^4V)^*
\]
and that an equivariant pairing
\[
\mathbb S_{(4,4,4,0)}V
\otimes
\operatorname{Sym}^4V
\longrightarrow
(\det V)^4
\]
exists and is unique up to scalar.

The missing step is the one that matters:

> the existence of this abstract equivariant map does not by itself prove that the **actual polynomial multiplication map**
> \[
> J_{12}\otimes \mathbf C[\operatorname{End}(V)]_4
> \longrightarrow
> \mathbf C[\operatorname{End}(V)]_{16}
> \]
> has a nonzero component on that determinant line.

The text says that one may “choose a degree-four matrix coefficient whose \(\operatorname{Sym}^4V\)-component pairs nontrivially” and concludes that multiplication has nonzero determinant projection. That conclusion requires proving that the scalar by which the coordinate-ring multiplication realizes the relevant Pieri/Cauchy map is nonzero for the specific copy of
\(\mathbb S_{(4,4,4,0)}V\) contained in the minor ideal.

Representation occurrence is necessary, not sufficient, for this particular nonvanishing.

The current regression script verifies the character decomposition only. It does not verify \(d^4\in J\) for a concrete smooth web, let alone supply a symbolic identity valid uniformly.

### Required repair

Any one of the following would close the gap:

1. give a full two-sided \(GL(V)\times GL(V)\) Cauchy/Pieri calculation and prove that the multiplication structure constant is nonzero;

2. give an explicit highest-weight-vector computation showing that the product has nonzero \(d^4\) coefficient;

3. produce an explicit covariant identity expressing \(d^4\) as a polynomial combination of the \(6\)-minors, with coefficients depending algebraically on the Jacobian-quartic covariant, and prove the coefficient is nonzero on \(G_4^\circ\);

4. reduce the claim to one exact web for which both smoothness and \(d^4\in J\) are independently certified, together with an invariant argument showing the relevant scalar is universal and nonzero.

Until this is supplied, I would not regard the exact corank-four nilpotency index as established.

# 3. Decisive correctness issue E127.2 — one witness per orbit does not establish the claimed generic table

The central corank-two theorem states exact nilpotency indices and Hilbert functions on a “coefficient-transverse open” of each of the nine mixed-kernel orbit types.

For seven new orbit types, the proof chooses one integer quadratic block \(\chi\), computes colons at that point, and then says that the associated coefficient matrices have maximal rank there. From this it concludes that the same ranks hold on a nonempty Zariski-open set.

There are two distinct facts here:

1. an explicit witness proves that the displayed algebra occurs somewhere;
2. to conclude that it is the generic algebra on an open subset of the entire orbit family, one must prove that the relevant ranks at the witness are the generic/maximal ranks.

The second fact is asserted, not demonstrated.

A matrix rank is lower semicontinuous. A single witness of rank \(r\) proves generic rank is at least \(r\), not that it equals \(r\). Likewise, a Hilbert function at one fibre can be special.

The definition of the “coefficient-transverse open” does not repair this. If the witness realizes a nonmaximal rank pattern, its constant-rank locus can be merely locally closed rather than open in the coefficient space.

### Required repair

For every row in the nine-orbit table, the authors should give one of:

- symbolic upper bounds showing the witness realizes the maximum possible ranks;
- explicit nonzero maximal minors together with dimension bounds ruling out higher rank;
- a Gröbner basis over the rational function field of the orbit parameters;
- or a universal module calculation giving the generic Hilbert series.

The open conditions should then be written explicitly enough that the reader can see what is being excluded.

This is not a cosmetic request. The generic Hilbert table is one of the principal new theorems of v127.

# 4. Decisive correctness issue E127.3 — the associated-prime refinement proposition is underproved

Proposition “Finite associated-prime refinement” asserts that after a finite locally closed refinement:

1. every graded module \(\mathcal M_j\) is flat with constant Hilbert polynomial;
2. there are finitely many relative closed supports whose fibrewise generic points are **exactly** the associated primes of every geometric fibre;
3. dimensions, minimal-versus-embedded status, incidences, and generic lengths are constant;
4. multiplication cokernels are flat, hence multiplication ranks are constant.

The proof consists essentially of:

- coefficient matrices have polynomial entries;
- rank conditions give determinantal strata;
- flatten the finitely presented modules;
- further use Fitting ideals and Noetherian induction.

That is not enough for the proposition as written.

Generic flatness controls Hilbert polynomials. It does not automatically make the set of associated primes of every fibre constant. Embedded associated primes can appear or disappear under specialization even in flat families. Their fibrewise behaviour requires a precise relative-associated-points argument or a more explicit finite presentation, and generic lengths require their own flatness or primary-data control.

There is also a base-change subtlety in the colon construction. The ideal
\[
(J:d^{j-1})
\]
is presented as a kernel. Formation of a kernel does not commute with arbitrary base change unless appropriate flatness hypotheses have first been imposed on the relevant cokernel. The manuscript reverses this logic too quickly.

### Required repair

The authors should either:

- replace the proposition by the weaker statement actually needed later, namely a finite stratification with constant ranks/Hilbert polynomials and determinant-membership data; or

- prove the full fibrewise associated-prime statement carefully, with precise references or a self-contained construction controlling relative \(\operatorname{Ass}\), embedded components, and generic lengths.

At present the proposition is doing substantial conceptual work in converting a finite algorithm into a “geometric classification,” but its proof is only a sketch.

# 5. Decisive structural issue E127.4 — depth classification is not yet graded-boundary classification

The response to v126 marks the exceptional rank strata as addressed or closed. That is too strong.

## 5.1 \(A_H\)-rank drop at projection corank two

The proposition proves the lower bound
\[
k\ge
6-a-\left\lfloor\frac b2\right\rfloor,
\qquad
k=\min\{j:d^j\in J\},
\]
and combines it with \(k\le5\).

This is useful. In the extreme type \((a,b)=(0,3)\), it indeed forces \(k=5\), hence nilpotency index six.

But for most rank-drop rows the theorem gives a list of possible values of \(k\), separated by Macaulay rank conditions.

It does **not** identify:

- the schemes \(W_1,\ldots,W_5\);
- their radicals;
- their minimal and embedded components;
- their multiplicities;
- the contact interpretation of those components;
- or their incidence with the known mixed-kernel strata.

Calling this a finite “atlas” is acceptable algorithmically. Calling it the requested geometric classification is premature.

## 5.2 Projection corank three

The theorem proves only
\[
d^3\notin J,\qquad d^5\in J,
\]
so that the nilpotency index is five or six depending on \(d^4\in J\).

That is a sharp depth dichotomy.

But the schemes
\[
W_1,W_2,W_3,W_4,W_5
\]
are not identified geometrically, and neither are their associated primes or multiplicities.

Thus v126 E126.2 is closed only at the level of **depth**, not at the level of the associated graded boundary geometry.

## 5.3 Projection corank four

Even granting the intended proof of \(d^4\in J\), the result computes an exact nilpotency index.

It does not compute the intermediate graded supports.

Again, exact depth is significant, but it is not a full classification of the special fibre.

# 6. Decisive structural issue E127.5 — actual specialization laws between rank strata are still missing

The v126 report specifically distinguished two kinds of specialization:

- the Rees parameter, which deforms a fixed nonreduced scheme to the normal cone of its reduction;
- variation in the **rank/moduli variables**, which moves a mixed-regular point into a rank-drop or higher-corank boundary.

Revision 127 now says that coefficient collisions are recorded by determinantal specialization and that a finite flattening refinement exists.

This is true as an organizational statement.

It is not yet the requested boundary-control theorem.

What remains absent is a theorem describing what happens along an actual DVR or one-parameter degeneration such as:

- mixed-regular rank two \(\rightsquigarrow\) tangent kernel line;
- secant line \(\rightsquigarrow\) ruling line;
- \(A_H\)-injective \(\rightsquigarrow\) \(A_H\)-rank drop;
- projection corank two \(\rightsquigarrow\) projection corank three;
- projection corank three \(\rightsquigarrow\) projection corank four.

For such degenerations one wants to know which \(W_j\) specialize to which components, where embedded components are born, whether lengths jump, and how the primary structure degenerates.

A finite stratification says that such data are constructible after refinement. It does not tell the reader the closure relations or the actual specialization laws.

For a paper whose title advertises a “boundary atlas,” this is a material omission.

# 7. Major issue M127.1 — the corank-three representation argument should be made fully explicit

The proof of \(d^3\notin J\) at projection corank three is plausible, and I do not currently have a counterexample.

However, the sentence

> every rank drop gives a subrepresentation of this case and cannot create a determinant representation that was absent before

is too compressed for a central theorem.

Because the actual generator spaces depend on the coefficient tensor, the authors should spell out the rank-drop cases or give a precise functorial containment of the corresponding symbol spaces.

The displayed \(GL_3\) decompositions are checked by the regression script, which is useful, but the theorem should not ask the reader to infer the passage from those universal character identities to every coefficient degeneration.

This is likely repairable with a short but explicit representation-theoretic lemma.

# 8. Major issue M127.2 — the “canonical finite atlas” is not canonical in the same sense as the nilpotent filtration

The nilradical, its powers, the annihilator schemes, and the \(W_j\) are intrinsic to the abstract failure scheme.

By contrast, the Macaulay valuation atlas is built from:

- a Schur chart;
- a choice of coordinates;
- a displayed generating set of maximal minors;
- monomial bases of homogeneous pieces;
- and subsequent flattening refinements.

The membership condition \(d^k\in J\) is invariant, and the final nilpotency index is intrinsic. But the particular finite matrix stratification is not obviously canonical under changes of chart or generating set.

The manuscript occasionally uses “canonical determinantal valuation strata” in a way that blurs this distinction.

The authors should distinguish:

- intrinsic invariants: the schemes \(W_j\), nilpotency index, multiplication in \(\operatorname{gr}_N\);
- coordinate-dependent computational strata: chosen Macaulay rank conditions used to compute those invariants.

If an intrinsic globalization of the rank conditions exists, it should be stated as a theorem and proved.

# 9. Major issue M127.3 — the inverse problem has not yet materially advanced

The polarized reconstruction theorem inherited from v123 remains, in my view, the conceptual high point of the paper.

Revision 127 observes that the higher \(W_j\), depth jumps, and orbit types are intrinsic and therefore refine the finite Torelli packet.

That observation is correct.

But no theorem proves that these additional invariants:

- reduce the generic degree;
- separate any two previously indistinguishable points;
- determine the web;
- determine the Reye/Enriques structure;
- or compute the monodromy group.

Thus the inverse problem remains generically finite rather than solved.

I agree with the authors' decision not to claim generic injectivity. But then the new boundary atlas should not be presented as if it has already advanced the inverse problem beyond providing possible future invariants.

A meaningful next theorem would show that one of the new graded layers actually distinguishes members of the finite packet.

# 10. Major issue M127.4 — the manuscript architecture is now a palimpsest rather than an integrated article

The compiled v127 source imports:

- the v125 introduction;
- v123 relation/Fitting/reconstruction/moduli sections;
- the v126 depth section;
- v125 boundary sections;
- new v127 atlas/proof sections.

This preservation strategy is useful for revision history, but it is no longer good journal exposition.

The inherited v125 introduction still says that the purpose is to understand “the first two layers” and “the first failure of the mixed-regular hypothesis.” Revision 127, however, claims a global depth-six cutoff, nine mixed-kernel types, rank-drop strata, and corank-three/four results.

Likewise, the older introduction calls the residual-colon formulas “the all-corank structure theorem,” language that the v126 referee already criticized and that the new v127 section partly corrects.

A top-four submission should read as one article, not as successive revision layers pasted together.

### Required editorial repair

Rewrite the introduction, theorem hierarchy, and proof roadmap natively for v127.

The logical order should be approximately:

1. intrinsic reconstruction theorem;
2. universal Fitting/residual factorization;
3. uniform determinant-power bound;
4. explicit corank-two orbit atlas;
5. rank-drop and higher-corank depth theorems;
6. precise limits of the geometric classification;
7. standard DNC as packaging;
8. moduli/inverse consequences;
9. classical and priority comparison.

Historical preservation belongs in Git, not in the reader-facing theorem narrative.

# 11. Major issue M127.5 — the top-four significance case is still not established

Subtract the standard or classical ingredients:

- Schubert/Fitting determinantal formalism;
- Reye and nodal-Enriques geometry;
- the nine-dimensional classical moduli background;
- Rees/deformation to the normal cone;
- flattening stratification;
- formal generic-finite/finite-etale reductions.

The manuscript-specific core is now stronger than in v126:

- polarized quartic-K3 reconstruction from a nonreduced failure scheme;
- residual-colon control of the nilpotent filtration;
- the global \(d^5\) determinant-power bound;
- explicit collision primary laws;
- the first decomposable-kernel wall;
- the nine mixed-kernel normal-form program;
- higher-corank depth constraints.

This is a serious body of mathematics.

The remaining top-four problem is breadth and conceptual consequence.

The \(d^5\) theorem is, at heart, a very clean determinant-completion identity for a surjection
\[
\operatorname{Sym}^2\mathbf C^4\to\mathbf C^6.
\]
The nine-orbit table and Macaulay atlas are intricate finite-dimensional determinantal algebra for the single Hilbert function \((1,4,6)\).

To justify a general top-four venue, the paper should extract a principle that survives the particular dimensions, or derive a striking global consequence from the atlas.

Examples of an adequate strengthening would include:

- a general determinant-power theorem for \((1,e,\binom e2)\) or a broader class of cube-zero algebras, with sharp exponents;
- a general theorem connecting nilpotent Fitting layers to ramification geometry;
- a full reconstruction theorem for the original multiplication tensor/web, not only its quartic K3;
- or a complete intrinsic classification of the boundary graded algebra with a nontrivial moduli consequence.

At present the paper looks much stronger as a specialist algebraic-geometry/determinantal-geometry paper than as a general top-four paper.

# 12. Ballico 1993 remains a documentary boundary

The manuscript now handles this correctly.

It cites:

E. Ballico, “On the failure locus of higher order properties of embeddings in projective spaces,” *Mathematische Nachrichten* 163 (1993), 5–13.

The v127 literature audit explicitly says that the complete theorem text was not obtained and that no anticipation or nonanticipation claim is inferred from metadata.

That is responsible scholarship.

It does not, however, make the priority question disappear for a top-four editorial decision. Before making strong historical novelty claims about “failure loci” with higher-order scheme structure, the complete predecessor should be read theorem by theorem.

I therefore keep this as an open documentary requirement, but not as a mathematical objection to the truth of the v127 theorems.

# 13. Computational evidence

The computational posture is mostly appropriate.

The v127 regression script:

- reproduces selected normal-form colon computations;
- checks the reported Hilbert prefixes at the chosen witnesses;
- verifies the \(GL_4\) character identity for
  \(\bigwedge^6\operatorname{Sym}^2\mathbf C^4\);
- verifies the printed \(GL_3\) exterior-symmetric-square character identities;
- checks \(J=(\delta^3)\) in the zero mixed-map witness.

The certificate correctly labels itself:

> “exact symbolic regression, not theorem certification”.

That wording should be retained.

In particular, the existing script does **not** certify:

- the genericity/maximal-rank claim for each mixed-kernel orbit;
- the corank-four membership \(d^4\in J\) for the universal family;
- the full associated-prime refinement;
- or the geometric content of the higher-corank \(W_j\).

I would not respond to this report merely by adding more random finite witnesses. The missing steps are structural.

# 14. Status of the v126 requests after v127

For clarity, my assessment is:

## E126.1 — determine the special fibre, not merely construct it

**Partially addressed, not closed.**

The uniform finite-depth theorem and explicit corank-two generic atlas are real advances. The full \(W_j\)-geometry on rank-drop/corank-three/corank-four strata remains unspecified.

## E126.2 — exceptional rank strata

**Substantially advanced, not closed.**

Mixed-kernel rank drops are now organized; \(A_H\)-rank drops have sharp depth bounds; corank three and four have depth theorems. But depth is not a primary/graded-support classification.

## E126.3 — specialization laws between rank strata

**Still open.**

Finite flattening/refinement is not the same as an explicit degeneration theorem with closure relations and specialization of components.

## E126.4 — Ballico 1993

**Open documentary issue, honestly disclosed.**

## E126.5 — advance the inverse problem

**Not closed.**

The new invariants are candidates for separating the finite packet; no separation theorem is proved.

## E126.6 — reframe DNC as standard

**Closed.**

The citations and novelty positioning are now appropriate.

# 15. What I would require for top-four reconsideration

The next revision should not simply add another layer of terminology around the same finite algorithm.

## E127.1 — close the corank-four proof

Prove the nonzero multiplication coefficient giving
\[
d^4\in J
\]
by an explicit representation-theoretic or polynomial identity.

This is a correctness requirement.

## E127.2 — prove genericity of the nine-orbit table

For each mixed-kernel orbit, prove that the displayed witness realizes the generic ranks/Hilbert series, or replace the theorem by a finite locally closed stratification that honestly records multiple possible Hilbert types within an orbit.

This is also a correctness requirement.

## E127.3 — either prove or weaken the associated-prime refinement proposition

Do not use generic flatness as shorthand for constant fibrewise embedded-prime structure.

Give a precise theorem controlling relative associated points, or state only what the available flattening argument actually proves.

## E127.4 — turn depth data into geometric graded data

At the \(A_H\)-rank-drop, corank-three, and corank-four strata, identify enough of the \(W_j\) to justify the phrase “boundary atlas” geometrically.

At minimum, determine radicals, dimensions, and associated supports of every nonzero layer on the generic stratum of each rank type.

## E127.5 — give actual degeneration/specialization laws

Write explicit one-parameter degenerations between adjacent orbit/rank strata and track the \(W_j\), multiplicities, and embedded components.

A closure-poset theorem for the atlas would already be a substantial improvement.

## E127.6 — extract a broader theorem or decisive inverse consequence

Either generalize the determinant-power mechanism beyond the single \((1,4,6)\) case or prove that the deeper nilpotent algebra recovers strictly more moduli data than the polarized K3 alone.

## E127.7 — integrate the article

Rewrite the introduction and theorem hierarchy around v127 rather than importing the v125 narrative verbatim.

## E127.8 — complete the Ballico comparison before strong priority claims

Obtain and read the full 1993 article. Keep the present cautious wording until then.

# 16. Final assessment

Revision 127 is the strongest A2 revision I have reviewed in this sequence.

The main positive change is that the paper now contains a real global theorem beyond the standard Rees formalism:
\[
d^5\in J,\qquad
\widehat{\mathcal N}_R^6=0.
\]
It also has a substantially better geometric organization of the corank-two exceptional set and a credible program for converting the residual-colon tower into finite determinantal data.

I do not find a counterexample to the global \(d^5\) theorem, to the inherited polarized reconstruction theorem, or to the mixed-regular collision algebra.

But a general top-four journal cannot accept the strongest new conclusions on the basis of representation occurrence where a multiplication nonvanishing is missing, or on the basis of one witness where genericity has not been proved. Nor does a finite flattening stratification by itself constitute the advertised all-boundary geometric classification.

The correct description of the present state is therefore:

> **Revision 127 has replaced the purely formal global container of v126 by a genuine uniform depth theorem and a partially explicit finite atlas, but the atlas is not yet proved or geometrically resolved at the level required for the manuscript's strongest claims.**

The paper has crossed an important threshold from formal organization to substantive boundary algebra. It has not yet crossed the threshold to a complete, integrated, top-four-level structure theorem.

**Recommendation: reject in the present form at a general top-four mathematics journal. Reconsideration would require closing the corank-four nonvanishing and mixed-kernel genericity gaps, proving or weakening the relative-associated-prime theorem, and replacing the remaining depth-only strata by an actual geometric/specialization classification.**
