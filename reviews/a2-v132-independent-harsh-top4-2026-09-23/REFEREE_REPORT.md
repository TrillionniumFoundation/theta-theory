# Independent harsh top-four referee report — A2 revision 132

**Manuscript:** *Intrinsic web reconstruction and primary boundary laws for multiplication-failure schemes*  
**Author:** Qian Qi  
**Repository:** TrillionniumFoundation/theta-theory  
**Reviewed revision:** revision/a2-v132-galois-descent-higher-residual-2026-09-23  
**Reviewed head:** 6d8fcb430efa95624a15aa684cfccab79c793350  
**Mathematical source commit:** 422fb0a8e74e9bc987cc66db873f2a700f7c1471  
**Principal referee-facing source:** papers/A2-v17-boundary-information-coarsening/article/v132/geometry.tex  
**Controlling previous report:** reviews/a2-v131-independent-harsh-top4-2026-09-23/REFEREE_REPORT.md  
**Date:** 23 September 2026

## Status of this report

This is an owner-requested, AI-assisted independent external-referee-style report. It was not commissioned by *Annals of Mathematics*, *Inventiones Mathematicae*, *Journal of the American Mathematical Society*, *Acta Mathematica*, or any other journal, and it must not be represented as a journal-issued report.

I reviewed the complete revision-132 source architecture, the point-by-point response to the revision-131 report, the new packet-descent section, the new intrinsic-web-reconstruction section, the relative primary-stratification machinery into which the descent argument is inserted, the moduli/Reye comparison, the literature audit, and the source-bound build receipt. I also checked the logical role of the exact arithmetic witnesses in the reconstruction theorem and compared the revised claims with the specific objections in the revision-131 report.

The present report deliberately does **not** repeat objections that revision 132 has genuinely repaired.

# Recommendation

## Reject in the present form at a general top-four mathematics journal.

This is nevertheless a materially different judgment from the rejection of revision 131.

Revision 132 closes the principal descent defect identified in the preceding report in a mathematically serious way. It also supplies the inverse-theorem alternative explicitly requested there: on a nonempty invariant open, the full nonreduced failure scheme is claimed to reconstruct the original relation web, rather than only its polarized Jacobian K3 surface. These are not cosmetic additions.

I therefore no longer regard the manuscript as blocked by the old “finite images descend packets” sentence, and I no longer regard the inverse problem as stopping at the K3.

The remaining concern is more concentrated. The new generic reconstruction theorem has become the natural headline result, but the representation-theoretic coefficient-space readout on which it rests is still written one lemma too tersely for a top-four archival proof. The underlying statement looks plausible and is very likely repairable, but the exact universal equivariant map and its restriction to the two Schur summands must be written explicitly. At present the proof moves too quickly from “a nonzero equivariant coefficient map is injective” to the much stronger identification of the **particular left coefficient line** determined by the web.

In addition, the manuscript itself records an unfinished priority audit for Ballico (1993). I agree with the authors’ refusal to invent a theorem comparison from metadata, but a general top-four submission cannot permanently leave a directly relevant historical paper unread while asking the referee to certify the novelty boundary.

Finally, even after the new inverse theorem, there remains a structural mismatch between the breadth suggested by “primary boundary laws” and the actual state of the higher residual layers: the paper still does not classify the full embedded primary geometry of the third and fourth layers at coranks three and four. This is no longer, by itself, a fatal objection because revision 132 chose the inverse-theorem route allowed by the previous report. It does, however, matter for scope, title, and the top-four significance case.

My present view is therefore:

- the old central correctness blocker E131.1 is substantially closed;
- the old inverse-ambiguity objection S131.3 is materially closed on a dense open;
- the main new theorem is genuinely interesting;
- one proof-level readout step still needs to be made fully explicit;
- the historical novelty boundary is not yet closed;
- and the 71-page architecture still needs sharper conceptual concentration for a general top-four venue.

# 1. What revision 132 genuinely fixes

A fair referee should first record what has changed.

## 1.1 E131.1 — packet descent is now addressed by an actual ideal-level construction

The new Section 09e is a real response to the previous report.

In characteristic zero the manuscript no longer says merely that finite images “descend the packets.” It constructs, on a finite Galois splitting cover,
\[
 I'_O=\bigcap_{i\in O}P_i
\]
for a complete orbit and gives the semilinear Galois action as a descent datum. The two pullbacks on the double overlap are identified componentwise, and composition of group elements supplies the cocycle on the triple overlap. The equivariant inclusion
\[
 I'_O\hookrightarrow B
\]
is then descended by effective fpqc descent.

That is the right object and the right theorem.

The fibre argument is also materially better. The exact sequence
\[
0\longrightarrow B/I'_O
\longrightarrow \bigoplus_{i\in O}B/P_i
\longrightarrow C_O\longrightarrow0
\]
is flattened so that the diagonal injection survives arbitrary base change. Thus the intersection identity is actually preserved on fibres. Together with geometrically integral prime fibres and the inherited noncontainment witnesses, this gives the intended reduced orbit of components upstairs, and the torsor over an algebraically closed field identifies that computation with the downstairs geometric fibre.

I therefore regard the characteristic-zero descent objection from revision 131 as closed in substance.

## 1.2 The arbitrary-characteristic packet construction matches the theorem actually stated

The second construction is also better calibrated than the old proof.

For a contraction \(\mathfrak q\subset A_K\), the manuscript forms the schematic closure ideal
\[
 Q=\ker(A\to A_K/\mathfrak q)
\]
on the original ring. On a finite splitting cover it proves, after clearing denominators,
\[
 (I')^n\subset QB\subset I',
 \qquad I'=\bigcap_iP_i.
\]
After flattening the diagonal intersection sequence, every geometric fibre satisfies
\[
 \sqrt{(QB)_{\Omega}}
 =
 \bigcap_i(P_i)_{\Omega}.
\]

This is exactly the level of information required by the final “support packet” theorem: the generic points of the geometric irreducible components are the associated points. The theorem does **not** assert that every packet in positive characteristic is geometrically reduced, nor that individually labelled primary components descend canonically.

The distinction is important. The present proof uses the finite cover to identify the geometric components, while the packet ideal itself is constructed downstairs. That is compatible with the actual statement of the bounded principal-colon stratification.

I therefore do not repeat the old complaint that the arbitrary-characteristic theorem is secretly only a theorem after a splitting cover.

## 1.3 The downstairs torsion module is now an actual relative object

Proposition prop:descended-packet-torsion gives the correct mechanism.

On the generic fibre it takes
\[
T_K=H^0_{I_K}(M_K),\qquad Q_K=M_K/T_K
\]
and chooses
\[
h_K\in I_K
\]
outside every associated prime of \(Q_K\). After spreading
\[
0\to T\to M\to Q\to0
\]
and the injection \(h:Q\to Q\), flattening the relevant cokernels preserves these injections under arbitrary base change.

Then an \(I\)-power-torsion element of a fibre maps to an \(h\)-power-torsion element of \(Q\), hence to zero. This proves that the spread submodule is the entire fibrewise local torsion module, not merely a generic candidate.

This is the right answer to the multiplicity part of E131.1.

## 1.4 S131.3 — the inverse problem no longer stops at the K3

The new theorem thm:generic-intrinsic-web is the most important mathematical change in revision 132.

The argument uses the actual nonreduced normal cone along the deepest intrinsic Schubert stratum. It does not merely recycle the first-layer K3 reconstruction.

The claimed chain is:

\[
\widehat D_R
\Longrightarrow
\Sigma_0(R)
\Longrightarrow
C_{\Sigma_0(R)/\widehat D_R}
\Longrightarrow
([Pw_R],[Qw_R])
\Longrightarrow
[w_R]
\Longrightarrow
R.
\]

The first arrow is intrinsic because three reduced singular-locus iterations recover \(\Sigma_0(R)\). The normal cone is then an intrinsic graded object.

The fibre equation
\[
\Spec \mathbf C[t_{ij}]/(d(T)J_R(T))
\]
retains the degree-twelve residual maximal-minor space after dividing the degree-sixteen ideal by the recovered determinant. This is genuinely more information than the polarized quartic alone.

The global ruling argument is also conceptually useful. A single square determinant cone admits transposition, but the two relative families of maximal \(\mathbf P^3\)'s are
\[
\mathbf P(V)\times\Sigma_0(R)
\quad\text{and}\quad
\mathbf P(\mathcal K_0^*).
\]
The first is projectively trivial and the second is not: on a Schubert line,
\[
\mathcal K_0^*
\simeq
\mathcal O^{\oplus3}\oplus\mathcal O(1),
\]
whose determinant degree obstructs projective triviality. This gives an intrinsic way to orient the tensor factors.

That is a substantive geometric idea, not a numerical accident.

## 1.5 The reduced one-point Pluecker witness is exact and relevant

The explicit witness is also well chosen.

For
\[
w_*=e_{1,5,8,10}
\]
the Jacobian covariant gives an exact projector onto the 35-dimensional summand, with
\[
CC^*=48\,\mathrm{id}.
\]
The displayed formula for \(Qw_*\) is then exact.

On the pencil \(aPw_*+bQw_*\), two Pluecker quadrics restrict to
\[
-\frac29(b-a)(b+2a),
\qquad
-\frac49(b-a)^2.
\]
After removing the common factor \(b-a\), the residual linear forms have no common projective zero. Thus the restricted ideal sheaf is \((b-a)\), and the Grassmannian intersection is the single reduced point \([w_*]\).

This is stronger than merely observing a unique point numerically.

The additional exact calculation at the independently certified smooth witness \(C_*\) is useful corroboration, although the irreducibility/open-intersection argument already proves nonemptiness of the reconstruction open inside \(G_4^\circ\).

## 1.6 The source discipline remains strong

The revision-132 build receipt records a 71-page compiled manuscript, no undefined references or citations, no LaTeX errors, local source inputs, source hashes, inherited-label preservation, and execution of the exact scripts.

More importantly, it explicitly lists the structural arguments that are **not** machine certified:

- effective Galois ideal descent;
- power-certified packets;
- downstairs torsion and length arguments;
- intrinsic deepest-stratum/ruling arguments;
- the Cauchy coefficient-space readout;
- generic web reconstruction.

That is the correct epistemic boundary.

I have no objection to the use of exact symbolic computation in the paper in its present role.

# 2. E132.1 — the two-component coefficient readout needs one more full representation-theoretic lemma

This is the main proof-level issue in revision 132.

The crucial assertion appears in Lemma lem:plucker-component-readout.

Let \(U=K_0\). The maximal minors of
\[
\gamma_R\operatorname{Sym}^2T:
\operatorname{Sym}^2U\longrightarrow S_R
\]
are the coefficients of the natural polynomial map obtained by pairing
\[
\beta_R\in
\left(\bigwedge^6\operatorname{Sym}^2V\right)^*
\]
with
\[
\bigwedge^6\operatorname{Sym}^2T.
\]

The manuscript uses the decompositions
\[
\bigwedge^6\operatorname{Sym}^2U
=
\mathbb S_{(5,4,2,1)}U
\oplus
\mathbb S_{(4,4,4,0)}U
\]
and
\[
\operatorname{Sym}^{12}(V^*\otimes U)
=
\bigoplus_{\lambda\vdash12}
\mathbb S_\lambda V^*\otimes\mathbb S_\lambda U.
\]

It then concludes
\[
(J_R)_{12}
=
\bigoplus_{\lambda\in\{(5,4,2,1),(4,4,4,0)\}}
\mathbf C\beta_{R,\lambda}\otimes\mathbb S_\lambda U.
\tag{2.1}
\]

Equation (2.1) is exactly what makes the inverse theorem work: the ideal must identify the **specific coefficient line**
\[
[\beta_{R,\lambda}]
\subset\mathbf P(\mathbb S_\lambda V^*),
\]
not merely the occurrence of the two representation types.

The present proof says, in effect, that the coefficient map is equivariant, nonzero, and injective because its source is irreducible. That is very close to the right argument, but it conflates two levels unless the universal map is written explicitly.

The clean proof should define the natural \(GL(V)\times GL(U)\)-equivariant map
\[
\Phi:
\left(\bigwedge^6\operatorname{Sym}^2V\right)^*
\otimes
\bigwedge^6\operatorname{Sym}^2U
\longrightarrow
\operatorname{Sym}^{12}(V^*\otimes U)
\]
by
\[
\Phi(\beta\otimes\xi)(T)
=
\beta\!\left(
(\bigwedge^6\operatorname{Sym}^2T)(\xi)
\right).
\tag{2.2}
\]

Then one should decompose both source and target and prove, for each of the two relevant partitions \(\lambda\), that
\[
\Phi_\lambda:
\mathbb S_\lambda V^*
\otimes
\mathbb S_\lambda U
\longrightarrow
\mathbb S_\lambda V^*
\otimes
\mathbb S_\lambda U
\]
is a **nonzero scalar multiple of the canonical Cauchy inclusion/identity** under the chosen identifications.

Multiplicity one and Schur's lemma then imply this immediately once nonvanishing is established.

Only after this universal statement has been proved may one fix \(\beta_R\) and conclude that its slice has image
\[
\mathbf C\beta_{R,\lambda}\otimes\mathbb S_\lambda U.
\]

Why am I insisting on this?

Because the fixed-\(\beta_R\) slice itself is not a \(GL(V)\)-subrepresentation. There are many \(GL(U)\)-submodules isomorphic to \(\mathbb S_\lambda U\) inside
\[
\mathbb S_\lambda V^*\otimes\mathbb S_\lambda U,
\]
parametrized precisely by lines in the left factor. The inverse theorem needs to know **which** line occurs.

The manuscript's intended universal equivariance argument almost certainly gives the desired answer, but it should be written as the universal map (2.2), followed by the multiplicity-one statement and an explicit nonvanishing check for both summands.

At top-four level, this is not a stylistic request. It sits at the exact point where a degree-twelve ideal is promoted from “it contains these two Schur types” to “it recovers the original web's two projective Pluecker components.”

### Required repair for E132.1

I would ask for a standalone lemma proving:

1. the precise source and target of \(\Phi\), including all dual and determinant twists;
2. the two Schur decompositions with the conventions used in the rest of the paper;
3. multiplicity one of each relevant \(GL(V)\times GL(U)\)-type in the target;
4. nonvanishing of \(\Phi_\lambda\) for each of the two partitions;
5. the scalar-identity conclusion by Schur's lemma;
6. the fixed-\(\beta_R\) corollary giving exactly (2.1);
7. compatibility of the two recovered coefficient lines with the exterior-duality identification of \(\beta_R\) with the Pluecker vector \(w_R\).

The exact script can check chosen coordinates, but this lemma should be a written proof independent of the script.

# 3. E132.2 — the final functorial passage from an abstract scheme isomorphism to one common \(g\in PGL(V)\) should be isolated

I do not currently see a counterexample to the final step of thm:generic-intrinsic-web. The ingredients appear to be present.

Nevertheless, the proof is compressed at another point where a general top-four referee will want a commuting diagram rather than prose.

An abstract isomorphism
\[
\widehat D_R\simeq\widehat D_{R'}
\]
intrinsically identifies the reductions and therefore the deepest strata. It should then induce, functorially, an isomorphism of the **graded** normal cones over the induced base isomorphism
\[
\Sigma_0(R)\simeq\Sigma_0(R').
\]

After the trivial/nontrivial ruling distinction, a fibrewise linear map preserving the two Segre rulings has the form
\[
g\otimes h.
\]
The reconstruction theorem needs the induced action on the degree-twelve Cauchy pieces to send **both** recovered left coefficient lines by the same \(g\), while the \(h\)-action is confined to the \(U\)-factor.

This is what the manuscript says informally, and it is the expected naturality statement. But since this is the bridge from an abstract scheme isomorphism to projective equivalence of relation webs, I recommend promoting it to a formal lemma.

The lemma should state that:

- the isomorphism of pairs induces a grading-preserving normal-cone isomorphism;
- the oriented rank-one ruling determines the \(V\)-factor projectively;
- the degree-twelve readout is natural for that tensor-product map;
- hence the two projective coefficient lines transform under the same \(g\in PGL(V)\);
- no extension of the original isomorphism to the ambient Grassmannian is being used.

I regard this as a proof-closure request, not evidence that the theorem is false.

# 4. S132.1 — the generic reconstruction theorem is strong, but the exceptional reconstruction locus is still a black box

The reconstruction open is defined by
\[
Pw_R\ne0,\qquad Qw_R\ne0,\qquad
\dim\langle\ell_{F,R}\rangle=2.
\]

The manuscript proves that this is nonempty and open. Since the Grassmannian is irreducible, it follows that it meets the smooth Jacobian locus. This is logically sufficient for a generic theorem.

For a general top-four paper, however, the exceptional locus is now mathematically important enough that merely naming it by a rank condition is unsatisfactory.

The theorem has changed the conceptual endpoint of the paper. The natural next questions are therefore intrinsic:

- What is the codimension of the complement of \(G_4^{\mathrm{rec}}\)?
- Is there a divisorial component?
- What are its irreducible invariant pieces?
- Does failure of the rank-two Pluecker condition correspond to a classical geometric feature of the web, the Reye congruence, the Enriques involution, or the Jacobian quartic?
- When the pencil contains a second decomposable point, what geometric relation holds between the two webs?
- Can the residual ambiguity on the exceptional locus be classified rather than merely acknowledged?

The current exact witness proves generic uniqueness, but it does not yet explain the geometry of failure of uniqueness.

I would not make a full classification of the exceptional locus a correctness condition. I would, however, expect at least a first geometric theorem about it if the authors want the inverse theorem to carry the entire top-four significance case.

# 5. S132.2 — the higher \(W_3/W_4\) primary geometry remains incomplete

Revision 132 is commendably explicit about this limitation.

The paper still does not give, at generic corank-three and corank-four points, a complete classification of:

- all associated primes of the third and fourth residual layers;
- all embedded primary components;
- their generic multiplicities;
- their support varieties;
- and their specialization through the \(2\to3\to4\) incidence family.

The seven-component family remains a theorem about the pulled-back incidence resolution, not a primary decomposition of the complete higher residual failure scheme.

The sharp exponent-five theorem tells us the length of the nilpotent tower. It does not identify the transverse geometry of every higher layer.

In revision 131 I said that the authors could answer the top-four significance issue either by computing genuinely higher residual geometry **or** by supplying a decisive inverse theorem. Revision 132 has chosen the second route, so it would be unfair now to declare the missing full \(W_3/W_4\) atlas an automatic rejection criterion.

But the scope must be calibrated accordingly.

If the complete higher primary atlas remains outside the paper, the title, abstract, and introduction should make unmistakably clear that the “primary boundary laws” are:

- complete in the corank-two atlas and in specified universal/quotient-induced families;
- global for the first two minimal supports and the nilpotency bound;
- but not a complete embedded-primary classification of all higher-corank residual layers.

The manuscript mostly says this already, but the overall 71-page architecture still encourages a stronger impression than the theorem list actually supports.

# 6. M132.1 — the Ballico 1993 priority audit remains unfinished and is not optional at final submission

The authors handle this responsibly.

The literature audit states that the full theorem text of Ballico's 1993 paper was not obtained and explicitly refuses to infer anticipation or non-anticipation from a title, DOI page, first page, or reference list.

I independently found the same bibliographic record for:

E. Ballico, *On the Failure Locus of Higher Order Properties of Embeddings in Projective Spaces*, Math. Nachr. 163 (1993), 5–13, DOI 10.1002/mana.19931630102.

The readily surfaced publisher material confirms the article and metadata, but this does not substitute for reading the theorem text.

This is exactly the correct scholarly caution.

However, it cannot be the final state of a submission to a general top-four journal.

The paper makes a central contribution in a subject explicitly called “failure loci,” and it cites a directly relevant article with essentially that phrase in the title. A referee cannot certify the novelty boundary while a theorem-level comparison is knowingly absent.

Before resubmission I would require either:

1. acquisition of the full Ballico 1993 text and a precise theorem-by-theorem comparison; or
2. documentary evidence strong enough to establish that the article is genuinely unavailable to the authors and a correspondingly conservative novelty statement, together with a broader historical comparison that makes clear what is and is not being claimed.

The first route is strongly preferable.

The comparison should address at least:

- the parameter space on which the failure locus is formed;
- whether the failure locus is set-theoretic or scheme-theoretic;
- the use, if any, of Fitting structures;
- higher nilpotent layers;
- residual/colon structures;
- family/base-change statements;
- and any reconstruction or inverse theorem.

# 7. M132.2 — the universal primary-stratification theorem needs a clearer novelty boundary

The bounded principal-colon primary stratification theorem is useful. It carefully avoids several common base-change mistakes:

- it flattens the image \(I_q=f^qB\) before using kernel base change;
- it constructs actual primary models on a splitting cover;
- it proves exhaustion by the diagonal injection into primary quotients;
- it uses coherent torsion modules for multiplicities;
- it descends support packets rather than pretending labelled primary decompositions are canonical.

These are all mathematically worthwhile.

But much of the mechanism is built from generic freeness, flattening, Noetherian induction, relative associated-point technology, and finite exact diagrams.

For a top-four paper, the authors should distinguish more sharply between:

- the genuinely new theorem;
- a strong but systematic packaging of standard relative algebra;
- and technical infrastructure needed for the special geometric application.

At present phrases such as “a bounded principal power converts the a priori infinite primary problem into a finite, base-change-compatible invariant” sound broader than the paper's actual conceptual novelty has been compared against.

I suggest a short theorem-positioning subsection that answers:

- Which exact output is absent from standard flattening/relative-assassin results?
- Is the novelty the simultaneous colon tower?
- Is it the combination with packet multiplicities?
- Is it arbitrary-base-change compatibility after finite stratification?
- Or is this theorem mainly infrastructure, with the real novelty lying in the determinant-completion and reconstruction results?

My own reading is that the top-four case should rest on the geometry and inverse theorem, not on presenting the relative-primary machinery as an independent foundational breakthrough unless a substantially broader literature comparison supports that claim.

# 8. The classical Reye/Enriques boundary is handled more carefully, but the new theorem should be compared against the classical inverse geometry more directly

Revision 132 does a good job separating the classical nine-dimensional Reye family from the exact rank computation used for the present K3 map.

The manuscript explicitly says that
\[
24-15=9
\]
is not a novelty claim, and it cites classical and modern Reye/Enriques sources.

That is appropriate.

Now that the paper claims generic reconstruction of the original web, however, the novelty comparison should be upgraded from a dimension comparison to an **inverse-problem comparison**.

The final version should state explicitly which of the following are classical and which are new:

- reconstruction of a web from a Reye congruence, when available;
- reconstruction of Reye/Enriques data from the web;
- reconstruction of the Steinerian/Jacobian surface from the web;
- reconstruction of the web from the polarized quartic alone;
- and reconstruction of the web from the full nonreduced multiplication-failure scheme.

The new theorem may well remain distinct from all classical statements because its input is the abstract nonreduced failure scheme and its mechanism is the deepest normal cone. But the distinction should be established by comparison, not left implicit.

# 9. The exact arithmetic evidence is good, but the headline theorem should not need the reader to trust a script

The new exact script checks substantial finite algebra:

- the \(35\times210\) Jacobian matrix;
- \(CC^*=48I\);
- the rank-35 projector;
- all sixteen \(\mathfrak{gl}_4\) matrix-unit equivariance identities;
- the five-coordinate Pluecker witness;
- the two restricted quadrics;
- and the same separation condition at the smooth integral witness.

This is valuable evidence.

The paper is also correct to say that none of this machine-certifies the structural proof.

For the final version, the printed proof should contain enough exact information that the nonemptiness witness can be checked by hand in principle:

- the five nonzero Pluecker coordinates;
- the projector formula;
- the two named quadratic Pluecker relations;
- their restrictions;
- and the argument that their saturation gives \((b-a)\).

Revision 132 already contains most of this.

The remaining script-heavy step is the smooth witness \(C_*\), which is only corroborative. That is acceptable.

# 10. The paper has become conceptually stronger, but it is still too encyclopedic for its main theorem hierarchy

The 71-page length is not itself an objection. Long top-four papers exist because some arguments genuinely require them.

The issue is hierarchy.

Revision 132 now has a plausible central story:

\[
\text{multiplication failure}
\to
\text{intrinsic nilpotent filtration}
\to
\text{polarized K3}
\to
\text{deepest normal cone}
\to
\text{full web}.
\]

That story is substantially cleaner than the historical sequence by which the paper was developed.

The final manuscript should be reorganized around it.

At present the reader must traverse:

- determinant completion;
- the K3 reconstruction;
- nine-dimensional moduli;
- a large corank-two atlas;
- multiple exact certificates;
- relative primary specialization;
- a universal stratification theorem;
- cross-corank incidence geometry;
- quotient-induced families;
- sharp global laws;
- and only then the deepest-cone inverse theorem.

Much of this is valuable, but not all of it deserves equal narrative weight.

For a top-four submission I would strongly consider:

1. moving extensive certificate tables and reproducibility details to an appendix or companion data note;
2. compressing historical revision-response material out of the mathematical narrative;
3. presenting the inverse theorem much earlier;
4. making the universal relative theorem a clearly labelled tool unless its independent novelty is defended;
5. separating complete theorems from exploratory atlas material that is not used in the final inverse theorem.

The paper should read like one inevitable argument, not the accumulated record of 132 revision stages.

# 11. Status of the revision-131 issues after revision 132

## E131.1 — descent of closed packets

**Substantially closed.**

The characteristic-zero orbit ideal now carries an explicit descent datum and cocycle.

The arbitrary-characteristic construction works at the support-packet level actually required by the theorem.

The local torsion module is constructed downstairs.

I do not repeat E131.1.

## S131.1 — complete higher-corank primary atlas

**Still open, explicitly not claimed.**

The manuscript has not computed the full embedded primary geometry of \(W_3\) and \(W_4\) at coranks three and four.

This is now a scope/significance issue rather than the unique missing path to a stronger paper.

## S131.2 — cross-corank family versus actual failure-scheme primary structure

**Still only partially closed.**

The incidence family remains distinct from a complete higher residual primary specialization theorem.

Again, the new inverse theorem reduces the urgency of this point but does not make the distinction disappear.

## S131.3 — inverse ambiguity

**Materially closed on a dense open, subject to E132.1/E132.2 proof completion.**

This is the largest advance in revision 132.

The full scheme is now claimed to recover the web generically, and the finite Torelli packet is separated after restricting to an open.

I no longer list “the inverse theorem stops at the K3” as an objection.

## M131.1 — Ballico 1993

**Still open.**

The authors disclose the limitation correctly, but the priority audit is unfinished.

## M131.2 — stale theorem hierarchy

**Closed.**

The article now consistently states the sharp index-five result on the smooth Jacobian open and removes the old revision-number prose from the mathematical narrative.

# 12. What I would require before another general top-four review

I would not recommend another top-four-style review after only copyediting.

A genuinely review-ready successor should do the following.

## E132.1 — write the universal Schur/Cauchy readout completely

Introduce the universal coefficient map (2.2), decompose it, prove it is a nonzero scalar on each relevant irreducible block, and derive the fixed-\(\beta_R\) coefficient-line formula as a corollary.

This is the most important proof request.

## E132.2 — isolate the normal-cone functoriality and common-\(g\) step

Give a formal lemma showing that an abstract failure-scheme isomorphism induces the oriented tensor map \(g\otimes h\) on a normal-cone fibre and that both recovered Pluecker components transform by the same \(g\).

## M132.1 — close the historical priority audit

Obtain and compare Ballico 1993 in full if at all possible, and expand the classical inverse-problem comparison now that web reconstruction is a headline theorem.

## S132.1 — explain at least one geometric feature of the exceptional reconstruction locus

A full classification is not mandatory, but the paper should say more than “the rank condition fails.” Codimension, an invariant divisor, a classical interpretation, or a classification of the second decomposable point would all materially strengthen the result.

## S132.2 — calibrate the primary-boundary scope

Either add a genuinely higher \(W_3/W_4\) theorem, or make the title/abstract/theorem hierarchy unmistakably reflect that the complete embedded primary atlas is only available in the stated lower-corank and benchmark families.

## Editorial concentration

Rebuild the paper around the reconstruction chain and demote technical infrastructure that is not part of the conceptual spine.

# 13. Top-four significance assessment

Revision 132 is the first version of this A2 project for which I think the paper has a credible single theorem around which a broad mathematical case can be made.

The generic intrinsic reconstruction theorem does something conceptually stronger than the earlier revisions:

- it uses the **abstract** nonreduced scheme;
- it finds an intrinsic deepest stratum without an ambient marking;
- it extracts a relative tensor orientation;
- it reads two representation-theoretic components from the actual nonreduced ideal;
- and it uses their Pluecker recombination to recover the original web.

That is a coherent geometric mechanism.

The difficulty is that a general top-four journal does not judge only whether a mechanism is clever. It also asks whether the theorem is completely proved, historically situated, and conceptually broad enough to justify a long and technically elaborate paper.

At present:

- the key representation-theoretic readout needs one more formal proof layer;
- the historical priority boundary is knowingly incomplete;
- the exceptional reconstruction locus is unexplained;
- and the higher primary atlas remains incomplete despite the breadth of the paper.

These points keep me below the acceptance threshold.

For a strong specialist journal, after the readout/functoriality repair and the literature audit, I would regard the paper much more favorably than I did revision 131.

For a general top-four journal, I would want the repaired inverse theorem to be presented as the unmistakable centerpiece and accompanied by a sharper explanation of either its exceptional locus or its relation to the classical inverse geometry of webs and Reye congruences.

# 14. Final assessment

Revision 132 is a substantial advance.

The previous central descent objection has been met with an actual ideal-level fpqc/Galois construction in characteristic zero and a correctly scoped power-certified packet construction in arbitrary characteristic. The coherent torsion argument is now downstairs. The new deepest-normal-cone theorem gives a serious answer to the inverse problem and, if fully justified, generically separates the finite Torelli packet.

I therefore withdraw the two strongest criticisms from revision 131:

1. I no longer claim that the relative packet theorem lacks any descent mechanism on the original base.
2. I no longer claim that the inverse theorem stops at the polarized K3.

The present rejection is based on a narrower set of issues.

The main mathematical request is to make the Schur/Cauchy coefficient readout fully explicit at the universal equivariant level and to formalize its functorial use under an abstract scheme isomorphism.

The main scholarly request is to finish the historical priority audit, especially Ballico 1993 and the inverse-problem comparison with classical web/Reye geometry.

The main structural request is to make the 71-page paper read as a focused reconstruction theorem with supporting machinery rather than as an encyclopedic accumulation of boundary calculations whose highest residual layers are still not completely classified.

My recommendation is therefore:

**Reject in the present form at a general top-four mathematics journal.**

I would encourage a further, targeted revision. Unlike several earlier rounds, the required next step is no longer “find a missing major theorem.” The paper now has a plausible headline theorem. The task is to close its most delicate representation-theoretic proof step, complete the novelty audit, and reorganize the manuscript so that the mathematical contribution is as sharp as the underlying idea.
