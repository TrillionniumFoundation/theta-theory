# Independent harsh top-four referee report — A2 revision 133

**Manuscript:** *Intrinsic web reconstruction and primary boundary laws for multiplication-failure schemes*  
**Author:** Qian Qi  
**Repository:** TrillionniumFoundation/theta-theory  
**Reviewed revision:** revision/a2-v133-schur-readout-exceptional-fibres-2026-09-23  
**Reviewed head:** bbbb697e852d1ca93b88eb7d3bfe6fbd15f396a7  
**Mathematical/source commit:** 9354051266816a5a63af98cc40a670e92a2d1bad  
**Principal source:** papers/A2-v17-boundary-information-coarsening/article/v133/geometry.tex  
**Controlling previous report:** reviews/a2-v132-independent-harsh-top4-2026-09-23/REFEREE_REPORT.md  
**Controlling previous report commit:** d76f34db1aaa8e196a7b50f4ec04be381d45236e  
**Date:** 23 September 2026

## Status of this report

This is an owner-requested, AI-assisted independent external-referee-style report. It was not commissioned by *Annals of Mathematics*, *Inventiones Mathematicae*, *Journal of the American Mathematical Society*, *Acta Mathematica*, or any other journal, and it must not be represented as a journal-issued referee report or decision.

I reviewed the complete revision-133 manuscript architecture, the response to the revision-132 report, the new universal Schur readout section, the functorial common-projective-transformation lemma, the exceptional-fibre theorem, the inverse-comparison section, the issue matrix, the literature audit, and the source-bound build receipt. I also checked these additions against the precise objections in the revision-132 report.

I do not repeat objections that revision 133 has genuinely repaired.

# Recommendation

## Reject in the present form at a general top-four mathematics journal.

This recommendation is not based on a newly discovered contradiction in the generic reconstruction theorem. On the contrary, revision 133 materially improves the manuscript, and the two proof-level defects singled out in my preceding report have, in my view, been substantially repaired.

The universal coefficient-space argument is now written at the correct representation-theoretic level, before fixing a web, and it does recover a specified left coefficient line rather than merely an isotypic type. The passage from an abstract failure-scheme isomorphism to one common projective transformation on both Pluecker components is now isolated and functorial. The new exceptional-fibre theorem is also a genuine geometric addition rather than a cosmetic rank computation.

The remaining problem is now one of mathematical endpoint and top-four significance.

The full inverse theorem still holds only on the nonempty invariant open \(G_4^{\mathrm{rec}}\). Outside that open, revision 133 classifies fibres of the **two-component invariant**
\[
[w]\longmapsto([Pw],[Qw]),
\]
but explicitly does not classify fibres of the much finer map sending a web to the isomorphism class of its full nonreduced failure scheme. Thus the new exceptional theorem does not yet convert generic reconstruction into an exceptional reconstruction theorem. Moreover, the one explicit positive-dimensional flag-line example lies outside the smooth, basepoint-free geometric locus \(G_4^\circ\), and the manuscript does not determine which exceptional secant, tangent, endpoint, or flag phenomena actually occur inside the geometric locus central to the paper.

At the same time, the directly relevant Ballico 1993 paper remains unread at theorem level. The authors are correct not to fabricate a novelty comparison, but that leaves the historical priority boundary unresolved. Finally, the title and 77-page architecture continue to suggest a broad theory of “primary boundary laws,” while the manuscript itself correctly acknowledges that the complete embedded-primary geometry of the higher \(W_3/W_4\) layers at coranks three and four remains unclassified.

My present assessment is therefore:

- E132.1 is substantially closed.
- E132.2 is substantially closed.
- The generic inverse theorem is now much more convincing.
- The exceptional theorem is mathematically useful but concerns a coarser invariant than the full failure scheme.
- The geometric incidence of the exceptional strata with \(G_4^\circ\) is still largely unknown.
- The historical novelty boundary remains documentary-open.
- The higher-corank primary geometry remains incomplete relative to the breadth suggested by the title and overall architecture.
- The paper is still too diffuse for a general top-four venue in its present form.

# 1. What revision 133 genuinely fixes

A harsh report should first distinguish actual repairs from remaining objections.

## 1.1 E132.1 — the coefficient-line readout is now formulated correctly

The new Lemma lem:universal-schur-readout addresses the main technical objection from revision 132.

The manuscript now defines the universal map
\[
\Phi_{V,U}:
\mathcal F(V)^*\otimes\mathcal F(U)
\longrightarrow
\operatorname{Sym}^{12}(V^*\otimes U),
\qquad
\Phi(\beta\otimes\xi)(T)
=
\beta\bigl(\mathcal F(T)\xi\bigr),
\]
where
\[
\mathcal F(X)=\bigwedge^6\operatorname{Sym}^2X.
\]

This is the correct level at which equivariance must be used. The previous proof risked passing too quickly from the occurrence of a \(GL(U)\)-type to identification of a specific line in the left multiplicity factor. Revision 133 explicitly avoids that mistake.

The decomposition
\[
\mathcal F(X)
=
\mathbb S_{(5,4,2,1)}X
\oplus
\mathbb S_{(4,4,4,0)}X
\]
is multiplicity-free, and the Cauchy decomposition of
\[
\operatorname{Sym}^{12}(V^*\otimes U)
\]
is multiplicity-free as a representation of \(GL(V)\times GL(U)\). The manuscript then treats the four source blocks. The off-diagonal blocks cannot occur in the target and therefore vanish; the two diagonal blocks are scalar multiples of the corresponding Cauchy inclusions.

Crucially, nonvanishing of both diagonal blocks is no longer asserted abstractly. Highest-weight vectors are written explicitly and, on a diagonal map \(T\), the two coefficient functions are
\[
t_1^5t_2^4t_3^2t_4
\quad\text{and}\quad
t_1^4t_2^4t_3^4.
\]
Both are nonzero, indeed equal to one at the identity after the chosen normalization.

Only after this universal statement does the manuscript fix \(\beta_R\). The fixed-slice formula
\[
\Phi_{V,U}(\mathbf C\beta_R\otimes\mathcal F(U))
=
\bigoplus_{\lambda}
\mathbf C\beta_{R,\lambda}\otimes\mathbb S_\lambda U
\]
therefore identifies the **specific** left coefficient lines. This is precisely the point that was missing in revision 132.

The exterior-duality lemma also writes the determinant twist explicitly and explains why the same scalar ambiguity affects both components projectively.

I therefore do not repeat E132.1.

## 1.2 E132.2 — the common projective transformation is now isolated

Lemma lem:common-g-functoriality is a serious improvement.

An abstract isomorphism
\[
\widehat D_R\simeq\widehat D_{R'}
\]
preserves the intrinsic deepest stratum and its ideal powers, hence induces a grading-preserving isomorphism of the associated graded algebras. The manuscript then uses the intrinsic distinction between the two rank-one tensor rulings to recover the \(V\)-factor projectively.

The key global point is now stated rather than hidden in prose. Once the \(V\)-ruling has been identified, the induced automorphism of the trivial \(\mathbf P(V)\)-bundle defines a morphism
\[
\Sigma_0(R)\longrightarrow PGL(V).
\]
Since \(\Sigma_0(R)\) is connected projective and \(PGL(V)\) is affine, this morphism is constant. Thus one obtains a single \(g\in PGL(V)\), rather than a fibre-dependent family of projective transformations.

At a fibre the tensor map is written as
\[
T\longmapsto gTh^{-1},
\]
and the commutative square for the universal coefficient map shows that \(h\) acts only on the right Schur factor while the same \(g\) acts on both recovered left coefficient lines.

This is the naturality statement needed by the generic inverse theorem. I do not see a reason, from the material inspected, to reopen E132.2.

## 1.3 The new exceptional-fibre theorem is a real theorem

Theorem thm:exceptional-component-fibres is mathematically substantive.

Let
\[
X=\operatorname{Gr}(4,W),\qquad
\pi:X^\times\to
\mathbf P(E_{175})\times\mathbf P(E_{35}),
\qquad
[w]\mapsto([Pw],[Qw]).
\]
For \(A=Pw\), \(B=Qw\), the Pluecker quadrics restrict on the component line to
\[
F(aA+bB)=(b-a)\ell_{F,w}(a,b).
\]
Writing \(H_w\) for the span of these linear forms gives an efficient and exact trichotomy.

If \(\dim H_w=2\), the fibre is one reduced point. If \(\dim H_w=1\), the closed line intersection is a length-two divisor, permitting a genuine secant point, a double point, or a discarded pure endpoint. If \(\dim H_w=0\), the whole line is a Grassmann line determined by a flag
\[
A_3\subset R\subset B_5.
\]

The graph-chart proof of the flag description is clean. The residual point operation on the genuine two-point locus is shown to be a regular involution, and the tangent-degeneracy criterion
\[
Qw_R\in\bigwedge^3R\wedge W
\]
correctly separates infinitesimal degeneracy from a transverse secant pair.

This is considerably better than leaving the exceptional set as an unnamed rank-drop locus.

## 1.4 The manuscript is appropriately cautious about what the theorem does not prove

I regard the explicit scope statements as a strength.

The manuscript repeatedly says that the exceptional theorem concerns the two-component invariant and does **not** assert that equality of the component pair implies an isomorphism of exceptional failure schemes. It also says that it does not compute the irreducible components or codimensions of all exceptional strata and does not claim a complete higher \(W_3/W_4\) embedded-primary atlas.

The build receipt likewise distinguishes exact coordinate checks from structural proofs.

This is good mathematical hygiene. My objections below arise precisely because, once the overclaims have been removed, the remaining endpoint is narrower than the present top-four framing suggests.

# 2. S133.1 — the exceptional theorem classifies a coarse invariant, not exceptional failure-scheme isomorphism fibres

This is now the central mathematical-significance issue.

The headline inverse theorem says that, on \(G_4^{\mathrm{rec}}\), an abstract isomorphism
\[
\widehat D_R\simeq\widehat D_{R'}
\]
forces projective equivalence of the webs.

Outside \(G_4^{\mathrm{rec}}\), the new theorem studies
\[
\pi([w])=([Pw],[Qw]).
\]
The common-\(g\) functoriality lemma shows that an abstract failure-scheme isomorphism forces equality of these two component lines after one projective coordinate change. Hence the fibre of \(\pi\) gives a set of **necessary candidates**.

But revision 133 explicitly stops there.

For a rank-one exceptional line, there may be two distinct decomposable points
\[
[w],\quad [w^\dagger]
\]
with the same projective component pair. The paper does not determine whether
\[
\widehat D_w\simeq\widehat D_{w^\dagger},
\]
whether they are always nonisomorphic, whether an additional intrinsic graded layer separates them, or whether both behaviours occur on different strata.

Likewise, on a flag line, the two-component invariant has a positive-dimensional \(\mathbf G_m\)-fibre, but the paper does not determine the isomorphism classes of the full nonreduced failure schemes along that fibre.

This distinction matters because the paper's most important claim is not “the pair \(([Pw],[Qw])\) is generically injective.” It is that the **abstract full failure scheme** reconstructs the web. Once the generic part has been established, the natural mathematical continuation is to understand the failure locus of that full inverse theorem, not merely the failure locus of one intermediate invariant.

The present exceptional theorem is therefore best viewed as a candidate-reduction theorem.

For a general top-four article whose central new result is an intrinsic inverse theorem, I would expect at least one further decisive result of the following sort:

1. prove that the full failure scheme separates every genuine two-point secant fibre occurring in \(G_4^\circ\); or
2. exhibit and classify actual exceptional pairs of non-projectively-equivalent webs with isomorphic full failure schemes; or
3. identify a second intrinsic invariant of the failure scheme that resolves the residual involution on a dense part of the rank-one exceptional locus; or
4. prove a geometric classification of the actual failure-scheme isomorphism fibres on all codimension-one exceptional strata.

Any of these would turn the new fibre theorem into part of a complete inverse-geometry story.

Without such a result, the paper still has a generic Torelli theorem plus a classification of ambiguity for an auxiliary representation-theoretic invariant.

That is meaningful, but it is not yet the exceptional inverse theorem suggested by the amount of machinery now devoted to the reconstruction section.

# 3. S133.2 — the paper does not show which exceptional fibre types actually occur on the geometric locus \(G_4^\circ\)

This is sharper than the preceding point.

The manuscript's central geometric setting is the open \(G_4^\circ\) of basepoint-free webs with smooth Jacobian quartic. The reconstruction open \(G_4^{\mathrm{rec}}\) is a dense open inside it.

The new exceptional theorem, however, is proved on the larger ambient domain
\[
X^\times\subset\operatorname{Gr}(4,\operatorname{Sym}^2V),
\]
where both Schur projections are nonzero.

For the positive-dimensional flag-line case, the only explicit example is immediately acknowledged to lie **outside** \(G_4^\circ\): the quadrics have a common factor/base point.

I found no corresponding theorem in revision 133 establishing:

- that the rank-one secant locus meets \(G_4^\circ\);
- that the double-point tangent locus meets \(G_4^\circ\);
- that the pure-endpoint rank-one locus meets \(G_4^\circ\);
- that the flag-line locus meets \(G_4^\circ\);
- the codimension of any of these intersections in \(G_4^\circ\);
- or the irreducible invariant components of the exceptional locus inside the geometric family.

This leaves a substantial gap between the ambient representation geometry and the actual geometry of smooth Jacobian webs.

For example, the existence of a \(\mathbf G_m\)-fibre of the component invariant somewhere in \(\operatorname{Gr}(4,10)\) is not, by itself, evidence that positive-dimensional ambiguity occurs in the family on which the K3/Reye interpretation and the full failure-scheme theorem are formulated.

Conversely, it may be that smoothness and basepoint-freeness exclude the most degenerate fibre type. If so, that would be an important theorem and would make the generic inverse result considerably sharper.

At minimum I would ask the authors to determine the incidence of each of the three fibre types with \(G_4^\circ\). A satisfactory top-four-level outcome would give:

- nonemptiness or emptiness;
- expected and actual codimension;
- generic smoothness or singularity of the exceptional strata;
- and an invariant geometric interpretation in terms of the web, its Jacobian K3, its Reye data, or the deepest failure cone.

At present the exceptional theorem is exhaustive only in the ambient component domain, not in the geometric family central to the paper.

# 4. S133.3 — the generic reconstruction theorem is convincing, but its “genericity” should be geometrically explained rather than only certified by two quadrics

The nonemptiness proof of \(G_4^{\mathrm{rec}}\) is logically correct.

An explicit decomposable point \(w_*\) gives two restricted Pluecker quadrics with independent residual linear factors, proving the rank-two condition on a nonempty open of the Grassmannian. Since \(G_4^\circ\) is another nonempty open in an irreducible Grassmannian, the two opens intersect. The manuscript also checks the condition at its independently certified smooth integral witness.

Thus I do not question nonemptiness.

However, once generic reconstruction is elevated to the first theorem in the introduction, the locus
\[
\dim H_w<2
\]
deserves a more conceptual geometric description.

Currently the rank condition is defined by the Pluecker pencil and then analyzed fibrewise. What is missing is an invariant global description of the exceptional locus itself.

Questions that should be addressed include:

- Is the rank-one locus a divisor?
- If not, what is its codimension?
- Is it irreducible?
- Is the double-point locus the ramification divisor of the component map on a suitable normalization?
- Is the genuine secant involution induced by a recognizable classical involution on Reye data?
- Does the exceptional locus map to a special Noether-Lefschetz or automorphism locus in quartic K3 moduli?
- Is the flag-line locus simply disjoint from the smooth-Jacobian locus?

A top-four inverse theorem is substantially more compelling when the failure of reconstruction has a geometric name, rather than only a rank condition on restricted equations.

Revision 133 has taken a useful first step by classifying pointwise fibre shapes. It should now globalize that classification.

# 5. M133.1 — the Ballico 1993 priority comparison remains unresolved

This issue is not mathematical correctness, but it remains important for the significance claim.

The manuscript now has a careful and responsible literature audit.

The authors inspected the relevant modern Reye/Enriques reconstruction results at theorem level and correctly distinguish reconstruction from a Fano-polarized Enriques surface with Reye data from reconstruction from the abstract nonreduced failure scheme. They also inspected the accessible Ballico 1996 paper and identify it as a substantive antecedent for organizing multiplication failure over a Grassmannian.

However, the distinct paper

E. Ballico, *On the Failure Locus of Higher Order Properties of Embeddings in Projective Spaces*, Math. Nachr. 163 (1993), 5–13

remains unavailable to the authors at full-text theorem level.

The manuscript explicitly says that it cannot certify either anticipation or nonanticipation relative to that paper.

I agree completely with the decision not to invent a theorem comparison from metadata. But the consequence is unavoidable: the novelty boundary is still not closed.

This is especially uncomfortable for a general top-four submission because the paper's title, language of “failure schemes,” Grassmannian parameter spaces, and multiplication maps place it close enough in topic that a referee cannot simply ignore the older article.

Before resubmission at this level, the authors should obtain the 1993 text through a library, interlibrary loan, author archive, or other legitimate source and perform an exact theorem-level comparison. The comparison should record:

- the parameter spaces used there;
- whether the failure locus is reduced or carries a scheme/Fitting structure;
- what multiplication maps are varied;
- whether nilpotent or colon layers occur;
- whether relative/base-change statements occur;
- and whether any inverse reconstruction statement is present.

If the 1993 paper is genuinely disjoint from the present theorems, that will strengthen the paper. If it contains a closer antecedent, the manuscript should say so explicitly and recalibrate novelty.

Until this is done, I would not certify the historical novelty case for a top-four journal.

# 6. S133.4 — the phrase “primary boundary laws” still outruns the completed higher-corank primary geometry

Revision 133 is admirably explicit about what is not known.

The complete primary decompositions are for:

- the stated generic corank-two coefficient strata;
- specified collisions;
- quotient-induced benchmark families.

The paper also has global first-support laws and a sharp index-five nilpotence theorem.

But it still does **not** classify, at generic corank-three and corank-four points:

- all associated primes of \(W_3\) and \(W_4\);
- all embedded primary components;
- their generic multiplicities;
- their support varieties;
- or the complete specialization relations across the higher-corank boundary.

The seven-component incidence family is not claimed to be such a primary decomposition, and that disclaimer is correct.

In revision 131 I explicitly allowed a decisive inverse theorem as an alternative route to top-four significance instead of demanding a complete \(W_3/W_4\) atlas. Revision 132 and now revision 133 have chosen that route, so it would be unfair to turn the missing atlas back into a correctness condition.

Nevertheless, the title and architecture still create a scope mismatch.

The paper is called *Intrinsic web reconstruction and primary boundary laws for multiplication-failure schemes*. A reader encountering “primary boundary laws” naturally expects a reasonably complete structural account of the primary geometry on the boundary, especially after 77 pages of residual-colon and coefficient-atlas machinery.

What is actually complete is more selective.

I see two coherent ways forward.

### Route A: make the inverse theorem unquestionably dominant

Retitle and reorganize the paper around intrinsic web reconstruction. Keep only the primary-boundary results needed to build the inverse invariant and to explain the first nonreduced layers. Move the large universal/relative primary machinery and detailed coefficient tables to a companion paper or substantial appendix.

This would produce a conceptually concentrated geometry paper.

### Route B: retain the broad primary-boundary framing

Then compute genuinely new higher-corank primary geometry: at least one complete generic \(W_3/W_4\) primary model at corank three or four, together with a nontrivial specialization theorem connecting it to the lower-corank atlas.

Either route could improve the significance case.

The present manuscript tries to do both programs at once but completes neither at the maximal natural endpoint.

# 7. S133.5 — the 77-page architecture remains too diffuse for the claimed general-journal endpoint

This is not merely stylistic.

The manuscript currently contains at least four substantial programs:

1. intrinsic reconstruction of the web from the full failure scheme;
2. polarized K3/Reye/Torelli analysis;
3. universal determinant-completion and relative primary-stratification technology;
4. extensive explicit corank-two and boundary calculations with exact certificates.

Each program is mathematically related to the others, but their theorem hierarchies are not of equal conceptual importance.

The new reconstruction theorem is now clearly the strongest and most distinctive result. Yet a reader must pass through a large body of universal algebra, atlas calculations, historical comparison, exact certificates, and boundary specializations to understand which statements are genuinely driving the paper and which are support machinery.

A general top-four paper can be long, but length must usually buy conceptual inevitability. Here it still buys a mixture of several different projects.

The introduction has improved by placing reconstruction first. That does not fully solve the architectural problem.

I strongly recommend a more radical concentration:

- state the full inverse theorem and its geometric mechanism as the principal narrative;
- isolate the minimum nilpotent/Fitting input needed for that theorem;
- move the full bounded-principal-colon framework to a companion or appendix unless a genuinely independent conceptual theorem justifies its central placement;
- move most coefficient tables and reproducibility bookkeeping out of the main logical spine;
- keep exact certificates as verification supplements rather than part of the conceptual burden;
- and explain the exceptional inverse geometry before returning to the broader primary program.

The present paper reads as if every technically valid result accumulated through many revisions has been retained. Preservation is useful during a revision process, but an archival paper should be optimized for mathematical necessity, not historical accumulation.

# 8. Technical comments on the new reconstruction section

These are not, at present, rejection-level correctness objections, but they should be addressed in a revision.

## 8.1 State the algebraicity of the rank strata globally

The three cases \(r_w=2,1,0\) are pointwise clear. The manuscript should package them as locally closed algebraic strata of \(X^\times\), defined by the ranks of an explicit morphism of vector bundles obtained by restricting the Pluecker quadrics to the component pencil.

This would make the residual involution an honest morphism on a named algebraic stratum and would prepare the codimension questions above.

## 8.2 Distinguish ambient fibre length from fibre length after deleting endpoints

The theorem correctly states the closed intersection on \(\mathbf P^1\) and then removes pure endpoints to obtain the fibre in \(X^\times\). Because several cases involve an endpoint as the residual zero of \(\ell\), the wording should remain extremely explicit about whether “length two” refers to the closed Grassmannian intersection or the actual fibre of \(\pi\) after endpoint deletion.

The current proof is mathematically readable, but a small table would make this unambiguous.

## 8.3 The tangent criterion should be tied to ramification language

The criterion
\[
Qw_R\in\bigwedge^3R\wedge W
\]
is useful. If the rank-one locus is developed globally, the authors should identify whether the double-point sublocus is exactly the ramification locus of \(\pi\) restricted to the appropriate finite part of the source.

That would turn a local derivative computation into a geometric statement.

## 8.4 The smooth witness deserves a clearer role

The explicit square-web witness proves the ambient reconstruction open nonempty; irreducibility then shows intersection with \(G_4^\circ\). The manuscript additionally verifies the same rank-two condition at the smooth integral witness \(C_*\).

For the final paper, the smooth witness is stronger and conceptually cleaner for the intended geometric locus. I would lead with it if the computation is already exact and independently certified, and relegate the five-coordinate square example to a transparent representation-theoretic illustration.

## 8.5 Keep the machine-verification boundary exactly as it is

The build receipt correctly says that the scripts verify finite coordinate identities but do not certify the structural proofs.

This distinction should be preserved. In particular, the Schur decomposition, normal-cone functoriality, constancy of the common projective transformation, and scheme-theoretic fibre classification are mathematical arguments, not consequences of the Python certificates.

# 9. Comments on the top-four significance case

At this stage I would separate correctness from significance.

### Correctness

I have not identified a new fatal correctness defect in the generic inverse theorem from the material reviewed. The main representation-theoretic and functorial gaps from revision 132 have been addressed in a form that is much closer to an archival proof.

That is real progress.

### Significance

For a general top-four journal, however, the natural question is now:

**What theorem remains after the technical apparatus is stripped away, and how complete is the geometry around that theorem?**

The best answer currently is:

> On a dense invariant open of four-dimensional webs of quadrics with smooth Jacobian, the abstract nonreduced multiplication-failure scheme reconstructs the web up to projective equivalence.

That is an interesting theorem.

But the manuscript then spends substantial additional machinery without yet completing the next natural inverse problem: what happens on the exceptional locus? The new theorem classifies the coarse component-pair fibres but not the actual failure-scheme isomorphism fibres, and it does not yet establish which exceptional types occur in the smooth geometric family.

At the same time, the broad primary-boundary program remains incomplete in the highest residual layers.

Thus the paper currently has one strong generic theorem plus two partially developed surrounding programs.

For a specialized research journal this balance may be entirely reasonable. For a general top-four venue, I would want either a more complete exceptional inverse theorem or a more decisive higher-boundary theorem, together with much sharper architectural concentration and a closed priority audit.

# 10. Required changes before I would support renewed top-four consideration

I would not ask for another accumulation of local lemmas. The next revision should resolve program-level questions.

1. **Close the historical audit.** Obtain and compare Ballico 1993 at theorem level.

2. **Determine the exceptional geometry inside \(G_4^\circ\).** For each rank-two/rank-one/rank-zero fibre type, prove nonemptiness or emptiness in the smooth basepoint-free locus and determine at least the generic codimension.

3. **Go beyond the two-component invariant on the exceptional locus.** Resolve the genuine two-candidate ambiguity for the full failure scheme on a substantial stratum, or exhibit actual exceptional isomorphism pairs. A theorem saying that an additional intrinsic layer breaks the residual involution on a dense rank-one exceptional locus would be a meaningful advance.

4. **Choose a scope.** Either make intrinsic reconstruction the dominant paper and substantially compress/relocate the general primary machinery, or retain the broad primary-boundary title and compute new complete higher-corank \(W_3/W_4\) geometry.

5. **Globalize the exceptional fibre theorem.** Present the rank strata as algebraic loci and relate the double-point locus to ramification of the component map.

6. **Keep the repaired universal readout and common-\(g\) proofs intact.** These should not be shortened back into the forms criticized in revision 132.

# 11. Final assessment

Revision 133 is not a cosmetic rewrite. It repairs the two most important proof-level defects of revision 132 and adds a useful exact theorem describing fibres of the two-component Pluecker invariant.

I therefore regard the generic reconstruction theorem as substantially more mature than in the previous round.

Nevertheless, I would still reject the manuscript in its present form for a general top-four mathematics journal.

The decisive remaining reason is no longer “the coefficient-line proof is incomplete.” It is that the manuscript has not yet reached the natural geometric endpoint created by its own strongest theorem.

The full failure scheme reconstructs the web generically. The next question is the exceptional inverse geometry of the full failure scheme. Revision 133 instead classifies the exceptional fibres of a necessary intermediate invariant, mostly in the ambient Grassmannian, while leaving their incidence with the smooth geometric locus and their actual failure-scheme isomorphism classes open.

Together with the unresolved Ballico 1993 priority comparison, the incomplete higher \(W_3/W_4\) primary atlas, and the still-diffuse 77-page architecture, that is enough for a negative top-four recommendation.

The manuscript is moving in the right mathematical direction. The next revision should be deeper rather than broader.
