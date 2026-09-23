# Independent harsh top-four referee report — A2 revision 134

**Manuscript:** *Intrinsic reconstruction of webs from nonreduced multiplication-failure schemes*  
**Author:** Qian Qi  
**Repository:** TrillionniumFoundation/theta-theory  
**Reviewed revision:** `revision/a2-v134-global-schur-support-reconstruction-2026-09-23`  
**Reviewed head:** `74b1aa9ffb95557f63e993e428a22e491a1edd0f`  
**Executed source/assembly commit recorded by the manuscript:** `d3494510fad791598c8edaf3ab5c668740c81397`  
**Principal source:** `papers/A2-v17-boundary-information-coarsening/article/v134/geometry.tex`  
**Controlling previous report:** `reviews/a2-v133-independent-harsh-top4-2026-09-23/REFEREE_REPORT.md`  
**Controlling previous report commit:** `a75f534c6694513ae6c493166d1cba1ea56a98fd`  
**Date:** 23 September 2026

## Status of this report

This is an owner-requested, AI-assisted independent external-referee-style report. It was not commissioned by *Annals of Mathematics*, *Inventiones Mathematicae*, *Journal of the American Mathematical Society*, *Acta Mathematica*, or any other journal, and it must not be represented as a journal-issued report or decision.

I reviewed the revision-134 reconstruction spine, including the introduction, deepest-normal-cone reconstruction, the unchanged universal Schur readout and common-projective-transformation arguments, the exceptional-fibre classification, the new contraction-kernel and exterior-support section, the new global rank/ramification section, the response to the revision-133 report, the issue matrix, the build receipt, the literature audit, and the provenance record. I also compared the logical endpoint with the objections in the revision-133 report.

I do not repeat objections that revision 134 has genuinely removed.

# Recommendation

## Reject in the present form at a general top-four mathematics journal, with the important qualification that the central mathematical situation has changed substantially since revision 133.

Revision 134 is not merely another incremental response. The new exterior-support argument appears to remove the principal geometric defect identified in my previous report. In revision 133 the inverse theorem was only established on a further reconstruction open `G_4^{rec}`, and the exceptional-fibre theorem classified ambiguity of the two-component invariant rather than the actual full-scheme inverse problem. Revision 134 proves a much stronger statement: once the Jacobian quartic has at least three essential variables, the Jacobian Schur component has exterior support at least nine, whereas a secant or tangent vector to `Gr(4,Sym^2 V)` has support at most eight. Consequently all nontrivial recombinations are excluded. For a smooth quartic the support is ten, and the manuscript concludes
[
G_4^{rec}=G_4^circ.
]
This converts the generic reconstruction theorem into a reconstruction theorem on the entire smooth basepoint-free Jacobian locus.

On the material I inspected, I did **not** find a direct counterexample to that new argument, nor did I find an explicit logical contradiction in the passage from the support theorem to the smooth-locus inverse theorem. I therefore do not regard the old genericity objection S133.1–S133.3 as an adequate reason to reject revision 134.

The reason I still recommend rejection at the general top-four level is different. The paper now rests its headline theorem on a new and delicate representation-theoretic support theorem whose proof is plausible but too compressed at exactly the points on which the global conclusion depends; the novelty of this new support mechanism is not yet positioned against the relevant classical literature on secant geometry, subspace varieties, supports/ranks of alternating tensors, and plethysm; the Ballico 1993 priority boundary remains explicitly unresolved; and the submission remains an 81-page accumulation in which the reconstruction theorem is surrounded by a large inherited primary-boundary program that is not needed for the new proof.

Thus my present assessment is:

- the principal mathematical objection from revision 133 has been substantially answered;
- the new support argument is the strongest and most interesting part of the paper;
- the smooth-locus inverse theorem is now a serious theorem rather than a generic statement with an unnamed exceptional set;
- I do not currently see a fatal algebraic contradiction in the support argument;
- nevertheless the two most delicate structural steps of the contraction-kernel theorem need a more audit-ready proof;
- the literature audit does not yet cover the mathematical mechanism that actually makes revision 134 new;
- the historically relevant Ballico 1993 paper remains unread at theorem level;
- the 81-page architecture is still not appropriate for the focused theorem the paper now wants to sell.

A substantially shorter, reconstruction-centered manuscript with the two proof bottlenecks expanded and the relevant priority/novelty questions closed could merit fresh consideration. I would not recommend acceptance of the present version.

# 1. What revision 134 genuinely fixes

A harsh report should distinguish successful repairs from unresolved issues.

## 1.1 S133.1 — the paper no longer needs an exceptional full-scheme classification on the smooth locus

The previous report emphasized that revision 133 classified fibres of the intermediate map
[
[w]longmapsto([Pw],[Qw])
]
but did not classify isomorphism fibres of the full nonreduced failure scheme outside `G_4^{rec}`.

Revision 134 changes the problem rather than evading it. The new Theorem `thm:global-schur-recombination` claims that all rank-one and rank-zero component-pencil phenomena are absent as soon as the Jacobian quartic has at least three essential variables. Smooth quartics have four essential variables. Therefore on `G_4^circ` there is no residual two-point or positive-dimensional component fibre whose full failure scheme still needs to be compared.

If the support theorem is correct, this is a legitimate and stronger resolution of S133.1.

I therefore do **not** repeat the demand that the authors classify exceptional full-scheme isomorphism fibres inside `G_4^circ`: revision 134 proves that there are no such component ambiguities there.

## 1.2 S133.2 — incidence of the exceptional fibre types with `G_4^circ` is now answered by emptiness

The previous report asked whether the secant, tangent/double, endpoint, and flag-line strata actually meet the smooth geometric family.

Revision 134 answers this cleanly. The support bound forces the rank-two case on all of `G_4^circ`; the other rows of the component-fibre table have empty intersection with the smooth locus. This is stronger than supplying codimensions for exceptional strata: there are no such strata in the family under consideration.

Subject to the correctness of the support theorem, S133.2 is closed.

## 1.3 S133.3 — the former genericity condition has acquired an invariant boundary interpretation

The corollary `cor:exceptional-binary-jacobian` places the ambient rank-defect locus over quartics with at most two essential variables, equivalently over the rank-at-most-two first-catalecticant subspace variety. The manuscript correctly states containment rather than equality and does not invent an irreducible-component classification of the whole ambient boundary.

This is the geometric explanation that was missing in revision 133. In particular, the paper no longer presents the reconstruction condition as a mysterious pair of separating restricted Pluecker quadrics.

I regard S133.3 as substantially closed on the geometric family.

## 1.4 E132.1 and E132.2 should not be reopened without new evidence

The universal coefficient-space argument and the common-projective-transformation lemma are retained byte-for-byte from the material that revision 133 specifically repaired. I checked that revision 134 still uses them in the same role: the normal cone recovers two specified projective Schur component lines, and an abstract failure-scheme isomorphism transports both through one common element of `PGL(V)`.

I found no new reason in revision 134 to reopen those two earlier proof defects.

# 2. The new contraction-kernel theorem is the real mathematical hinge

The entire upgrade from a generic inverse theorem to the global smooth-locus theorem now passes through
[
kappa_q(f)=iota_qj(f),
]
where
[
j:det Votimesoperatorname{Sym}^4V
longrightarrow
igwedge^4operatorname{Sym}^2V
]
is the polarized Jacobian Schur embedding.

This is the correct place for a referee to be severe. The finite exact calculations recorded in `REVISION134_EXACT.json` are useful sanity checks, but the build receipt itself correctly says that the stabilizer-shear argument, orthogonal irreducibility, support classification, and global reconstruction are not machine-certified proofs.

I agree with that limitation. The structural proof must stand on its own.

## 2.1 The singular-`q` shear argument is elegant but too compressed

For singular `q`, the manuscript decomposes
[
V=Aoplus B,qquad B=operatorname{rad}(q),
]
observes invariance under `O(A,q)	imes GL(B)`, the `B`-scaling torus, and shears
[
amapsto a+L(a),qquad bmapsto b,
]
and proves nonvanishing on
[
Aotimesoperatorname{Sym}^3B.
]
It then argues that any kernel vector with positive `A`-degree can be pushed by infinitesimal shears to a nonzero kernel vector in that degree-one summand, a contradiction.

The idea is credible. The presentation is not yet adequate for a theorem carrying the entire global inverse result.

The sentence

> “Some mixed derivative of order (k-1) of a nonzero polynomial of (A)-degree (k) is nonzero. Applying the corresponding shears produces a nonzero kernel vector in (Aotimesoperatorname{Sym}^3B); multiplication by (b^{k-1}) cannot annihilate it.”

compresses several points that should be separated:

1. why the chosen iterated Lie-algebra operators cannot cancel across the (operatorname{Sym}^kAotimesoperatorname{Sym}^{4-k}B) component;
2. how one chooses the `B` directions when (dim B>1);
3. why the resulting vector is nonzero in the relevant associated graded piece;
4. how the determinant twist behaves under the stabilizer action;
5. why the argument covers every singular rank uniformly, including the low-dimensional `A` cases.

None of these looks impossible, and the exact canonical-rank computations strongly support the stated kernel dimensions. But a top-four proof should not make the reader reconstruct the Lie-algebra filtration argument.

**Required repair:** isolate a standalone “shear descent” lemma for (operatorname{Sym}^4(Aoplus B)), prove it at the level of the `B`-weight filtration, and then invoke it in the contraction-kernel theorem. This would convert a clever paragraph into an audit-ready proof.

## 2.2 The nondegenerate-`q` scalar-kernel step deserves a representation-theoretic proof, not only a bespoke parity argument

For nondegenerate `q`, the manuscript uses
[
operatorname{Sym}^4V
=
mathcal H_4oplus homathcal H_2oplusmathbf Cho^2,
]
with the three summands irreducible and pairwise nonisomorphic, checks nonvanishing on the first two, and proves (kappa_q(ho^2)=0).

The nonvanishing checks are explicit and convincing. The delicate point is the claim that the relevant determinant character does not occur in
[
igwedge^3operatorname{Sym}^2V.
]
The manuscript gives a direct reflection/parity/infinitesimal-rotation argument. I do not see an immediate contradiction in it, but this is exactly the kind of one-paragraph exceptional-character calculation that is difficult to audit inside an already long paper.

Because the theorem is now the hinge of the entire submission, I would require one of the following:

- an explicit `O_4` or `SO_4timesmathbf Z/2` decomposition of (igwedge^3operatorname{Sym}^2V) showing that the determinant character is absent;
- an equivalent highest-weight computation with the determinant twist tracked explicitly;
- or a fully expanded coordinate lemma that makes every symmetry constraint and every remaining basis vector visible.

The current argument may well be correct. My objection is not “the scalar kernel is false”; it is that a general top-four reader should not have to trust an unusually compressed representation-theoretic exclusion at the point where the main theorem becomes global.

## 2.3 Once the contraction-kernel theorem is accepted, the support table is exceptionally clean

The formula
[
s(z)=10-dim{qin W^*:iota_qz=0}
]
is the natural support-annihilator identity.

Given the contraction-kernel theorem, the stated support values
[
4, 7, 9, 10
]
according to essential-variable dimension, with the nondegenerate quadratic-square exception of support nine, follow efficiently. The smooth-quartic conclusion is particularly transparent: fewer than four essential variables give a cone, and a quadratic square is nonreduced, so a smooth quartic has support ten.

This part is one of the strongest pieces of the revised paper.

## 2.4 The secant/tangent obstruction is simple and decisive

The lemma that a sum of two decomposable four-vectors is supported on at most eight ambient directions, and that a tangent vector in
[
igwedge^3Rwedge W
]
is likewise supported on at most eight directions, is elementary but exactly the right observation.

The resulting contradiction is strong:

- a second decomposable point on the component pencil would express `Qw_R` as a linear combination of two decomposable four-vectors;
- a double point or flag-line case would put `Qw_R` in the tangent space;
- but the Jacobian Schur component of a quartic with at least three essential variables has support at least nine.

This is the conceptual core of revision 134. It is far preferable to another finite separating certificate.

# 3. The smooth-locus inverse theorem is now logically much stronger

Assuming the two accepted ingredients from revision 133 and the new support theorem, the proof of
[
widehat D_Rsimeqwidehat D_{R'}
quadLongrightarrowquad
R'=gR
]
for all `R,R'in G_4^circ` is logically coherent.

The chain is:

1. the deepest Schubert stratum is intrinsic;
2. the normal cone recovers the degree-sixteen ideal;
3. division by the determinant equation recovers the degree-twelve maximal-minor space;
4. the universal Schur readout recovers the two specified projective component lines;
5. the ruling argument and functoriality give one common projective transformation on both components;
6. the support theorem shows that the component pencil meets the Grassmannian at exactly one reduced point throughout the smooth locus;
7. therefore the web is recovered.

This is the correct architecture for the inverse theorem.

The revision-133 report criticized the fact that the paper stopped after step 5 on an exceptional locus. Revision 134 now supplies a genuine step 6.

I therefore consider the main mathematical endpoint materially improved.

# 4. The new global rank and ramification section is useful, but its terminology and scheme structure should be tightened

The bundle morphism
[
ho:
mathcal I_{mathrm{Pl},2}otimesmathcal O_{X^	imes}
longrightarrow
mathcal K
]
with rank-two target is a natural globalization of the pencil calculation. Defining rank-one and rank-zero determinantal loci by minors and entries is appropriate.

The local residual-section construction also matches the fibre classification.

I have three requests.

## 4.1 State explicitly the precise category in which the residual involution is defined

The manuscript says that on the rank-one finite stratum, after deleting endpoints and the diagonal, the residual operation is a regular fixed-point-free involution and argues that the degree-two divisor splits as two disjoint sections even over a nonreduced base.

That is a worthwhile scheme-theoretic statement. It deserves a short lemma spelling out the base, the open subscheme, and the two Cartier sections. At present it is embedded in a long proposition with several other claims.

## 4.2 Be more careful with “ramification scheme”

The paper defines the ramification scheme as
[
operatorname{Fitt}_0Omega_{X^	imes/Y}.
]
This is a reasonable convention for the locus where the morphism fails to be unramified, but (pi) is not being presented as a global finite flat double cover. The text already warns against that interpretation; the terminology should be made equally explicit at first use.

I suggest “the Fitting ramification locus of the quasi-finite part” unless a standard reference is supplied for the exact convention used.

## 4.3 Separate the clean smooth-locus conclusion from ambient boundary geometry

The important conclusion for the main theorem is simply that this Fitting ramification locus is empty on `G_4^circ`. The ambient binary-Jacobian boundary may have complicated determinantal structure. Since the paper does not classify that structure, it should resist giving the ambient rank section more prominence than is needed for the inverse theorem.

# 5. The largest scholarly gap has shifted: the new support theorem itself is not literature-positioned

Revision 134's literature audit is careful about the Reye/Enriques comparison and about the inaccessible Ballico 1993 paper. That is good. But the paper's genuinely new mathematical engine is now elsewhere.

The upgrade from revision 133 to revision 134 rests on:

- the specific equivariant embedding
  [
  det Votimesoperatorname{Sym}^4V
  hookrightarrow
  igwedge^4operatorname{Sym}^2V;
  ]
- its contraction kernels against symmetric bilinear forms;
- the exact exterior-support table;
- and the exclusion of the secant and tangent varieties of (operatorname{Gr}(4,10)) by support.

The present audit does not give a serious theorem-level comparison with the classical literature on:

- secant and tangent varieties of Grassmannians;
- subspace varieties and support varieties for alternating tensors;
- ranks and orbit stratifications in exterior powers;
- plethysm/decomposition of (igwedge^4operatorname{Sym}^2V);
- catalecticants and essential-variable/subspace varieties of quartics;
- or existing representation-theoretic descriptions of the (mathbb S_{(5,1,1,1)}V) component.

For a general top-four paper this matters. The paper can prove its lemma from scratch and still need to explain whether the lemma is new, standard in another language, or a special case of a known orbit/support theorem.

**S134.1 — required novelty audit.** Before another top-four submission, add a theorem-level comparison centered on the contraction-kernel/support theorem itself. The audit should say which exact statement is new and which part is a repackaging of classical representation or secant geometry.

At present the manuscript gives the strongest novelty language to precisely the result whose external mathematical positioning is thinnest.

# 6. M133.1 remains open: Ballico 1993 cannot be treated as a permanently deferred footnote

The authors continue to be admirably explicit that they have not obtained the complete text of

E. Ballico, *On the Failure Locus of Higher Order Properties of Embeddings in Projective Spaces*, Math. Nachr. 163 (1993), 5–13.

I agree that no theorem-level claim should be fabricated from metadata.

But this does not make the issue disappear. The manuscript still uses “failure schemes,” multiplication maps, Grassmannian parameter spaces, Fitting structure, and inverse reconstruction as part of its novelty boundary. The older paper is close enough in title and historical line that a top-four referee needs to know what it actually proves.

The accessible 1996 Ballico paper on failure cycles for quadratic normality itself works with Grassmannians and multiplication maps and treats the 1993 work as part of the same failure-locus program. That does not show anticipation of the present theorem, but it reinforces that the 1993 text is not safely irrelevant.

**M134.1 — unresolved documentary blocker.** Obtain the paper through a library, interlibrary loan, author archive, or other legitimate source and compare exact theorem statements. The comparison should record at least:

1. parameter spaces;
2. reduced locus versus scheme/Fitting structure;
3. the multiplication maps being varied;
4. nilpotent, colon, or infinitesimal layers if any;
5. relative/base-change statements;
6. any inverse or reconstruction statement.

Until this is done, I would not support a claim of historically settled top-four novelty.

# 7. The paper is still editorially overgrown

The revision changes the title and moves the inverse theorem earlier. That is an improvement. But the build receipt records an 81-page paper with 30 compiled inputs and 219 inherited mathematical labels. The branch deliberately retains essentially the entire previous primary-boundary program.

That is a version-control achievement, not an editorial argument.

The new main theorem depends on a much smaller spine:

- relation/Fitting setup;
- intrinsic deepest stratum and normal cone;
- universal Schur readout;
- common-`g` functoriality;
- exceptional component-pencil classification;
- contraction-kernel/exterior-support theorem;
- smooth-locus reconstruction;
- polarized-K3 comparison and a concise classical-data discussion.

The large corank-two tables, higher boundary specializations, relative primary filtrations, determinant-completion certificates, and extensive exact-coordinate appendices are interesting, but the current revision itself repeatedly says that they are not hypotheses of the support argument and do not constitute a complete higher-corank embedded-primary atlas.

That admission should have an editorial consequence.

**S134.2 — required architectural decision.** For a top-four resubmission I strongly recommend splitting the material:

- a focused paper on intrinsic reconstruction from the full nonreduced failure scheme, containing the support theorem and only the boundary machinery logically needed for it;
- a companion paper for the detailed primary-boundary, collision, and relative-specialization program.

If the authors insist on one 81-page article, they need a convincing mathematical reason why the retained appendices are part of one theorem rather than the history of how the theorem was found.

“Preserving every inherited result” is not such a reason.

# 8. Exact computation is used responsibly, but it should remain subordinate

The revision-134 receipt is unusually careful about the boundary between computation and proof. It records:

- all 35 polarization columns;
- the canonical contraction ranks for bilinear forms of ranks 1–4;
- harmonic nonvanishing coefficients;
- support representatives of dimensions 4, 7, 9, 10, 9;
- a smooth witness of support ten;
- sharp support-eight secant/tangent examples.

It also explicitly lists the structural statements that are **not** machine-certified.

This is good practice and should be retained.

The manuscript should not, however, use the presence of exact canonical-rank checks as a substitute for expanding the two delicate structural steps identified in Sections 2.1–2.2 above. Those checks establish consistency with the theorem, not the theorem for arbitrary `q`.

# 9. Technical comments

## 9.1 Clarify the status of the equality `G_4^{rec}=G_4^circ`

The proof says that the determinantal complement has no geometric points and hence is empty, giving equality as open subschemes. Over (mathbf C) and for the reduced geometric locus this is fine, but the manuscript should state explicitly which scheme structures are being used on `G_4^circ` and the rank-defect locus. This is a small clarification, not a substantive objection.

## 9.2 Track determinant twists consistently in the support section

The text often says “with the determinant factor understood.” That is harmless for projective support dimensions but less harmless inside equivariance arguments. Since the nondegenerate proof invokes the determinant character of `O_4`, the twist should be written explicitly at least once in every representation-theoretic map used there.

## 9.3 Separate support of a vector from essential variables of a quartic in the prose

The distinction is mathematically clear in the formulas but occasionally compressed in exposition. The quartic has an essential-variable space in `V`; its image `j(f)` has an exterior support in `Sym^2V`. The numerical jump (4,7,9,10) is more striking if these two spaces are consistently named.

## 9.4 The abstract should not make the ambient obstruction sound classified

The abstract says the ambient exceptional locus lies over binary quartics and that its rank stratification and ramification scheme are described. The body is more precise: the rank-defect support is **contained** in the inverse image of the binary-quartic subspace variety, and no equality or irreducible-component classification is claimed. The abstract should preserve that distinction.

## 9.5 Preserve the explicit disclaimer about the exact certificates

The current sentence that finite coordinate checks do not formally verify the written structural proofs is exactly right. Do not weaken it.

# 10. What I would require before a new top-four submission

I would regard the following as the minimum serious revision package.

1. **Expand the singular contraction-kernel proof.** Add a self-contained shear-filtration lemma and remove the current one-paragraph descent through `A`-degree.

2. **Replace or supplement the nondegenerate determinant-character paragraph with an explicit representation decomposition.** Make the absence of the determinant character in (igwedge^3operatorname{Sym}^2V) immediately checkable.

3. **Perform a literature audit focused on the new support theorem and Grassmann secant geometry.** The current novelty audit is aimed mainly at the older failure-locus and Reye/K3 story, not at the new argument that now carries the paper.

4. **Obtain and read Ballico 1993 at theorem level.** Keep the present caution until this is done.

5. **Split or radically shorten the manuscript.** Present the reconstruction theorem as a coherent article rather than as the latest layer of a version-preservation archive.

6. **Keep the exact scripts and provenance package as supplementary verification rather than narrative bulk.**

7. **Retain the current scope discipline.** Do not reintroduce claims of a complete higher-corank `W_3/W_4` primary atlas unless that program is actually completed.

# Final assessment

Revision 134 is the first version in this sequence for which I regard the central inverse theorem as having a plausible global geometric endpoint on the full smooth Jacobian locus. The exterior-support obstruction is a real conceptual advance over the separating-certificate strategy of earlier versions, and it appears to resolve the most serious mathematical-significance criticism in the revision-133 report.

That is not yet enough for acceptance at a general top-four journal.

The new theorem is now important enough that its two delicate representation-theoretic pivots must be written at a standard where an expert can audit them without reconstructing omitted arguments; its novelty must be compared with the literature actually closest to the support/secant mechanism; the historically relevant 1993 failure-locus paper must be read rather than indefinitely bracketed; and the paper should be rebuilt around its new core instead of carrying the entire 81-page inherited boundary program.

**Recommendation: reject in present form. A substantially shorter, proof-expanded, literature-closed reconstruction paper could warrant a fresh top-four-level review.**
