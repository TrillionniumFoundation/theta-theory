# Independent harsh referee report — A2 revision 153, complete materialized article

## Manuscript and review object

**Manuscript:** *Finite failure schemes and the reconstruction of quadratic pencils*  
**Author:** Qian Qi  
**Revision reviewed:** A2 revision 153  
**Revision branch:** `revision/a2-v153-global-incidence-fibre-structure-2026-09-25`  
**Locked branch tip:** `bdaaa980518803bc97e2116e773dae90ee620eec`  
**Source-bound mathematical commit:** `19516986e07e3508e7d13e8a08b66528078a6af7`  
**Controlling prior report:** `reviews/a2-v152-independent-harsh-top4-2026-09-24/REFEREE_REPORT.md`  
**Controlling prior-report commit:** `60f1a3c5f8078c31019dfab249d334d0e717e225`  
**Principal review object:** `papers/A2-v17-boundary-information-coarsening/article/v153/geometry.pdf`, 80 pages  
**Self-contained source:** `papers/A2-v17-boundary-information-coarsening/article/v153/geometry.tex`  
**New mathematical core:** `papers/A2-v17-boundary-information-coarsening/article/v153/new-core.tex`  
**Review standard:** the proof-completeness, originality, conceptual depth, inevitability, and expository standard expected at *Annals of Mathematics*, *Acta Mathematica*, *Inventiones Mathematicae*, or *Journal of the AMS*.

This is an owner-requested independent-referee-style report, not a journal-commissioned editorial decision. I reviewed the current materialized v153 article, not the earlier source-lock shell. The revision branch advanced after the earlier incomplete-submission report: it now contains the complete 80-page article, source-bound build receipts, a response to the v152 report, preservation data, and a new mathematical core. The prior report on the shell tip `2580b639...` was correct for that earlier repository state but is not a review of the article assessed here.

I read the new introduction and abstract, the formal-image lemmas, the binary finite-flat factorization theorem, the squarefree conductor theorem, the simultaneous collision atlas, the all-rank singular Fitting formula, the pure-power reciprocal-fibre theorem, the response to v152, and the build and preservation receipts. I also re-read the inherited normalization, split-conductor, pinch, and common-orbit-boundary arguments on which the new results depend.

The build receipt reports a successful 80-page compilation, 269 labels, no missing predecessor labels, no duplicate labels, preservation of the inherited mathematical blocks, and clean references. The new exact checks are useful consistency evidence. The receipt correctly records that the historical 28 checks were not rerun and that computation does not certify the general proofs. I use the receipts only for source identification and reproducibility, never as a substitute for mathematical review.

## Recommendation

**Reject in the present form for a top-four general mathematics journal.**

Revision 153 is the strongest and most mathematically substantive version of this manuscript that I have reviewed. It genuinely answers many of the concrete technical criticisms in the v152 report. In particular:

- the formal-image and separated-germ steps are now isolated and proved;
- the binary normalization is analyzed on every exact-gcd stratum, not only at one collision;
- the entire squarefree-common-divisor locus receives a uniform completed local model, global conductor formula, full multiple-branch intersection calculus, depth, multiplicity, seminormality, and a Cohen–Macaulay criterion;
- arbitrary simultaneous binary root collisions are represented by a complete incidence atlas;
- the singular Fitting ideal of the generalized pinch model is evaluated in closed form for every rank;
- the pure-power normalization fibre in arbitrary embedding dimension has an explicit minimal relation representation and a complete-intersection classification.

These are real theorems. They are not cosmetic repairs, larger experiment tables, or relabellings of the v152 examples. I found no simple counterexample to the new main statements, and I do not base my recommendation on a concealed correctness objection.

The negative recommendation is instead about mathematical scale, conceptual integration, and the standard of inevitability appropriate to the four general journals named above.

The new global theorem is global only in the binary factorization problem. After ordering the squarefree roots, its local ring is a block coordinate-subspace ring and much of the conductor, depth, multiplicity, and seminormality calculation becomes a controlled Stanley–Reisner computation. This is elegant and useful, but it does not yet yield a comparably global theory for multivariate common-divisor images, nor does it solve a natural compactification or orbit-boundary problem for quadratic pencils.

The simultaneous collision atlas is exact, but it is an incidence presentation by an intersection of kernels. It does not classify the resulting analytic singularities, conductors, homological invariants, or closure relations at arbitrary collisions. The pure-power theorem gives the minimal number and representation type of the defining equations, but leaves most of the commutative algebra of the multivariate fibres—Hilbert functions, lengths, types, resolutions, Betti tables, and Gorenstein behavior—undetermined outside the easiest cases.

Most importantly, the connection back to pencils remains one common information-destroying point in every full `GL(E)` first-relation orbit closure. It does not distinguish pencil degeneration types, recover Segre data from boundary type, describe a nontrivial portion of an orbit-closure poset, or construct a natural compactification of the pencil-failure moduli problem. The common limit is a legitimate incidence theorem; it is not yet an organizing boundary theory for the motivating moduli problem.

The closest named failure-locus predecessor, Ballico 1993, remains unavailable at theorem/proof level. The manuscript is appropriately honest about this, but a top-four referee still cannot certify exceptional historical originality while that comparison remains open. The article is also still 80 pages with 269 labels and a large inherited appendix architecture. Reordering the pipeline is an improvement, but it is not the same as producing one sharply focused general-journal paper.

For a strong specialist venue in algebraic geometry, commutative algebra, or invariant theory, v153 is a serious candidate after further proof polishing and literature positioning. For *Annals*, *Acta*, *Inventiones*, or *JAMS*, I remain unconvinced.

---

## 1. What v153 genuinely fixes

### 1.1 Formal images are no longer handled by prose shorthand

Lemma `lem:formal-image-v153` isolates the completed scheme-theoretic image of a finite morphism. It records the kernel-intersection formula after completion, reducedness of the completed image, the implication from cotangent surjectivity to surjectivity of complete local rings, the two-branch fibre product, and separation of formal normalization germs.

This is a material improvement. In v152, these steps were plausible but compressed exactly where the split-conductor theorem became stronger than a branch-counting statement. The new lemma makes the logical dependence visible and removes the appearance that a tangent calculation alone determines an image intersection.

Lemma `lem:coprime-lifts-v153` likewise supplies the Artin-base identity

\[
(a)\cap(b)=(ab)
\]

for coprime lifted forms, together with flatness of the relevant graded quotients. It also gives the direct numerical estimate

\[
c\ge (r-1)(s_g-1)\ge1,
\]

which is preferable to inferring positivity only after the two-branch picture has already been asserted.

These corrections substantially close points 1–4 of the v152 report.

### 1.2 The binary normalization is treated on every exact-gcd stratum

Theorem `thm:binary-fibres-v153` is one of the strongest genuinely new pieces of the revision.

On the binary exact-common-divisor-degree-
\(s\) stratum, the normalization map becomes the base change of

\[
\mathbf P(S_g)\times\mathbf P(S_{s-g})\longrightarrow\mathbf P(S_s),
\qquad (f,H)\longmapsto fH.
\]

The manuscript proves that this map is finite locally free of degree
\(\binom{s}{g}\), and it describes the complete scheme fibre at an arbitrary root partition. The fibre decomposes into products of tensor products of reciprocal Artin complete intersections

\[
H_{a,b}=\mathbf C[q_1,\ldots,q_k]/(c_{l+1},\ldots,c_{l+k}).
\]

The length, weighted Hilbert series, socle weight, total cluster length, and partition closure order are then computed uniformly.

This is no longer one double-root example. It is a clean theorem over an entire stratification, and the finite-flat degree is geometrically meaningful.

### 1.3 The squarefree locus now has an actual conductor theory

Theorem `thm:squarefree-v153` directly answers the strongest mathematical demand in the v152 report on a substantial natural class.

For binary relations with squarefree common divisor of degree \(s\), it identifies the completed local ring with the block monomial model

\[
\mathbf C[[z,u_{ij}]]/J_{s-g+1}.
\]

The normalization branches are indexed by degree-\(g\) subsets of the roots. Every multiple branch intersection is computed scheme-theoretically. The conductor is

\[
J_{s-g}/J_{s-g+1},
\]

and globally on the squarefree open it is the ideal of the next divisor-degree image:

\[
\mathfrak c_{Y_g}|_{\mathcal U}
 =\mathcal I_{Y_{g+1}/Y_g}|_{\mathcal U}.
\]

The theorem also gives seminormality, depth, multiplicity, a Hilbert series, and the exact Cohen–Macaulay cases.

This is a real global structural theorem within the binary problem. The previous criticism that the paper had only two isolated local models is obsolete for v153.

### 1.4 The collision discussion is upgraded from a slice to an incidence atlas

Theorem `thm:atlas-v153` treats an arbitrary binary root partition

\[
\gcd(K)=\prod_i\ell_i^{s_i}
\]

and writes every normalization branch through factor variables
\(A_i,B'_i,U_{ij}\). The completed image is the precise intersection of the kernels of the branch maps. The construction is formulated over local Artin bases and is declared independent, up to isomorphism of the completed incidence diagram, of the frame and local root coordinates.

This is the right formal object. It covers higher and simultaneous collisions without pretending that a selected transverse family is the whole local image.

### 1.5 The generalized pinch singular ideal is actually evaluated

Theorem `thm:fitting-v153` gives the all-rank formula

\[
\operatorname{Fitt}_{m+1}\Omega_{A_m/\mathbf C}
=(I^{m+1}+\Delta I^m)\oplus I^m t
=I^{m-1}(I^2,(w),\Delta I).
\]

This closes a concrete deficiency of v152. The singular ideal is no longer left as “the relevant Jacobian minors.” The proof exhibits generating minors and uses equivariance to span the complete symmetric-power pieces. The distinction between the nonreduced Fitting ideal and its conductor radical is retained.

### 1.6 The pure-power fibre now has structural commutative algebra

Theorem `thm:reciprocal-structure-v153` computes the embedding dimension, the exact minimal number of equations, and the equivariant minimal relation module

\[
\mathcal I/\mathfrak n\mathcal I
\simeq
\bigoplus_{j=g+1}^{g+k}(\operatorname{Sym}^jW)^*.
\]

It follows that the fibre is a complete intersection exactly in the binary case \(\dim W=1\). The theorem also identifies the truncated-symmetric-algebra case \(k=1\), and the actual ternary-pencil limiting fibre is shown to have 44 variables but 9867 minimal scalar equations.

This is exactly the kind of structural information that v152 lacked. The 9867 count is not confused with a length or embedding dimension.

### 1.7 The paper's scope language is more responsible

The new introduction explicitly distinguishes the full `GL(E)` first-relation coordinate-change orbit from the `PGL(V)` congruence orbit of pencils. It records the two-stage specialization, removes the claim that the common limiting point is a coordinate-free canonical moduli point, and organizes the abstract around two theorem packages rather than a catalogue of infrastructure.

These changes are not merely cosmetic. They make the actual content easier to evaluate at its correct level.

---

## 2. Correctness audit of the formal-image and binary finite-flat arguments

I did not find a correctness blocker in this part, but several arguments should be expanded or cited more precisely before publication.

### 2.1 The complete-local surjectivity argument is credible

The proof of Lemma `lem:formal-image-v153` uses surjectivity on cotangent spaces, successive lifting on associated graded pieces, and completeness to obtain a surjection

\[
R\longrightarrow B_i.
\]

With the common residue field \(\mathbf C\), Noetherian completeness, and continuity understood, this is a standard complete-local argument. The manuscript should state these hypotheses explicitly in the lemma, because cotangent surjectivity without the complete local setting would not be enough.

The use of excellence to obtain reduced completions is also appropriate over finite-type complex rings. A precise citation would improve the presentation.

### 2.2 The finite-flat factorization morphism uses miracle flatness correctly

The binary factorization map is finite between smooth varieties of the same dimension. At a source point, the local ring is Cohen–Macaulay and finite over the regular target local ring. The target parameters form a system of parameters in the source and hence a regular sequence. The local flatness criterion then gives flatness.

This is the right mechanism. It should be named as a finite/miracle-flatness argument and supplied with a standard reference, rather than left as a one-sentence local calculation in a theorem carrying substantial weight.

### 2.3 The base-change description needs its scheme structure kept visible

The key statement is not merely that a degree-\(g\) divisor of \(K=GL\) is a divisor of \(G\) on closed points. The manuscript correctly uses a residual member coprime to \(G\) and Artin-base cancellation to identify the incidence functors. That is the necessary scheme-theoretic step.

The final version should make especially clear how the gcd-free residual open is used uniformly after base change, and why the chosen coprime member can be selected locally in the relevant topology. The current proof is convincing over the completed/local setting, but the descent from the local choice to the stated global base-change description is terse.

### 2.4 The reciprocal cluster algebra is classical and correctly scoped

For a single root cluster, the reciprocal equations form a homogeneous system of parameters in the weighted polynomial ring; hence they are a regular sequence. The Hilbert-series and length formulas follow. Tensor decomposition across coprime clusters is justified by Hensel factorization over Artin bases.

I agree with the manuscript's revised novelty language: the reciprocal complete intersections themselves are classical. The geometric contribution is their appearance as the full normalization fibres of the unframed Grassmannian divisor image and the uniform finite-flat theorem over the exact-gcd stratum.

---

## 3. Audit of the squarefree conductor theorem

The squarefree theorem is mathematically credible and significantly stronger than the v152 local models.

### 3.1 The completed local ring is the expected coordinate-subspace arrangement

After choosing ordered roots, a marked degree-\(g\) divisor selects a subset \(A\) of the \(s\) roots. The corresponding branch equations set the blocks indexed by \(A\) to zero. Thus

\[
\bigcap_{|A|=g}I_A=J_{s-g+1}
\]

because a monomial belongs to every branch ideal exactly when its block support meets every \(g\)-subset, equivalently when it uses at least \(s-g+1\) blocks.

This combinatorial identity is correct and gives the full scheme structure, not only the union of its components.

### 3.2 The multiple-intersection formula follows from sums of coordinate ideals

For any collection of branches, the sum of their ideals is the ideal of the union of their selected root sets. Hence all multiple intersections are smooth coordinate subspaces with the stated dimension. This really does answer the previous request for intersections of three or more branches on the squarefree binary locus.

### 3.3 The conductor formula is convincing

On a branch \(A\), the conductor consists of functions vanishing along every gluing with another branch. The product of the blocks outside \(A\) is precisely what is forced. Globally this yields \(J_t/J_{t+1}\), and the same local coordinates identify the next divisor-degree image with \(J_t\).

The resulting equality

\[
\mathfrak c_{Y_g}|_{\mathcal U}
=\mathcal I_{Y_{g+1}/Y_g}|_{\mathcal U}
\]

is a clean theorem. The use of faithful flatness of completion to globalize the ideal equality is legitimate, although the paper should explicitly state that both coherent ideals are being compared stalkwise on the squarefree open.

### 3.4 Seminormality and depth are plausible but deserve standard references

The ring is an equalizer of its normalization branches with compatibility on coordinate intersections. The coefficient-by-monomial argument explains why pairwise compatibility suffices in this distributive coordinate-ideal setting. The square-and-cube criterion then yields seminormality.

The depth computation is a standard Stanley–Reisner/Koszul-homology calculation for a block-support skeleton. The manuscript supplies an argument, but the proof is effectively a version of Hochster's formula after collapsing each block. A primary citation to the Stanley–Reisner or coordinate-subspace-arrangement literature is needed. At present the bibliography is detailed on coincident roots and factorization, but surprisingly thin on the exact combinatorial commutative algebra used for the strongest new global theorem.

### 3.5 The theorem's limitation is equally clear

The global conductor formula is proved on the binary squarefree-common-divisor open. It does not determine the conductor on the collision strata, in the multivariate divisor image, or on an orbit closure of pencil first relations. The collision atlas gives a presentation there, but not a corresponding closed conductor theorem.

This limitation does not diminish the correctness of the squarefree theorem. It does matter for the top-four significance assessment.

---

## 4. Audit of the simultaneous collision atlas

The collision atlas is the correct universal local incidence object for the binary problem, but its mathematical payoff is less complete than the rhetoric “all collisions” might initially suggest.

### 4.1 The versal coordinates are credible

The interpolation map to the sum of root-jet spaces is surjective, and the Grassmannian tangent space can independently vary the relevant jets. Weierstrass preparation and division then give a triangular change to the polynomial and remainder coordinates. This supports the claim that the displayed variables form formal ambient coordinates rather than parameters on a selected slice.

### 4.2 The branch rings represent the marked divisor functors

For a distribution \(\alpha=(a_i)\), the equations

\[
P_i=A_iB_i',\qquad R_{ij}=A_iU_{ij}
\]

are exactly the equations for a marked divisor over an Artin base. Monicity gives uniqueness of quotient data. The factor coefficients are integral over the product coefficients, so the branch map is finite. The completed-image lemma then supplies

\[
\widehat{\mathcal O}_{Y_g,K}
=T/\bigcap_\alpha\ker(T\to B_\alpha).
\]

I find this convincing as an incidence presentation.

### 4.3 The atlas is not yet a classification of collision singularities

The theorem does not simplify the intersection of kernels into local normal forms for arbitrary partitions. It does not compute the conductor, depth, multiplicity, type, seminormalization, or minimal resolution in those cases. It also does not describe which collision types lie in the closure of which singularity strata beyond the elementary root-partition order.

Thus “all collisions” means that every collision has an exact formal incidence presentation. It does not mean that the singularities have been classified. This distinction should remain explicit in the abstract and conclusion.

---

## 5. Audit of the all-rank Fitting formula

Theorem `thm:fitting-v153` is a useful exact calculation.

The dimension count gives the correct size of Jacobian minors. After substitution into the normalization, minors without the \(\Delta\) column acquire the required positive \(t\)-order, while those using the \(\Delta\) column have one additional \(u\)-factor. The displayed rows and columns produce representatives of

\[
I^m t,\qquad \Delta I^m,\qquad I^{m+1}.
\]

Simultaneous linear changes of \(u\) and \(w\), together with the fact that powers of linear forms span the symmetric powers in characteristic zero, generate the full indicated modules.

I do not see a counterexample to the formula. For publication, however, the manuscript should spell out the equivariance group and explain why the chosen minors transform through the full symmetric-power representations, rather than simply saying that the ideal is invariant. This is a proof-polishing request, not a fatal objection.

The theorem is also correctly scoped: it computes one important family of collision singular ideals. It does not compute the singular schemes of all rings in the general collision atlas.

---

## 6. Audit of the reciprocal-fibre theorem

This theorem supplies a sharp and easily stated structural invariant.

### 6.1 The embedding dimension count is correct

Because \(g\ge k\), the defining reciprocal coefficients have no linear terms in the variables parameterizing

\[
Q_i\in\operatorname{Sym}^iW.
\]

The presentation is therefore minimal at the level of variables, giving

\[
\operatorname{edim}F_{g,k}(W)=\binom{d+k}{k}-1.
\]

### 6.2 The relation-module argument is plausible

For each weight \(j\), the coefficient space gives a `GL(W)`-equivariant map

\[
(\operatorname{Sym}^jW)^*
\longrightarrow \mathcal I/\mathfrak n\mathcal I.
\]

Specialization to a one-dimensional subspace shows that the map is nonzero because the corresponding binary reciprocal relation is minimal. Irreducibility then gives injectivity. Different weights cannot cancel, and the selected equations generate the ideal, so the direct-sum formula follows.

The paper should isolate the specialization lemma: under the specialization to one coordinate, membership in \(\mathfrak n\mathcal I\) maps to membership in the specialized variable ideal times the specialized relation ideal. This is true for the stated homomorphism, but the logical step is important enough to state rather than leave implicit.

### 6.3 The complete-intersection classification follows

For \(d\ge2\), the number of minimal equations is strictly larger than the number of variables. Since the fibre is zero-dimensional, a complete intersection in a minimal regular local presentation would require equality. The binary case is a regular sequence. Hence complete intersection occurs exactly when \(d=1\).

The special case \(k=1\) is also correct: the coefficients of \(Q_1^{g+1}\) generate all degree-\(g+1\) monomials, yielding the truncated symmetric algebra.

### 6.4 The theorem leaves a large structural problem open

For \(d>1\) and \(k>1\), the manuscript does not compute:

- the length or Hilbert function;
- the Cohen–Macaulay type;
- a Gorenstein criterion;
- the graded or local Betti table;
- a minimal free resolution;
- primary decomposition or associated primes of related non-Artin families;
- representation stability as \(g,k,d\) vary.

The minimal relation module is valuable, but for a top-four claim it looks like the beginning of the multivariate reciprocal-fibre theory, not its culmination.

---

## 7. The connection to quadratic pencils remains the central conceptual weakness

Revision 153 materially improves the independent geometry of the divisor image. It does not yet make that geometry organize the motivating pencil problem.

### 7.1 The acting group is too large for the common limit to remember pencil geometry

The point constructed in every orbit closure is common under the full `GL(E)` action on all cotangent variables. This is much larger than the congruence group `PGL(V)` acting on pencils. The manuscript now says this clearly.

The common point therefore demonstrates that the natural first-relation boundary is actually reached by genuine failure algebras. That is worthwhile. But the point is deliberately information-destroying: every pencil reaches the same extreme boundary.

### 7.2 No degeneration type is read from the boundary type

The paper still does not prove a theorem of the form

\[
\text{pencil degeneration invariant}
\quad\Longleftrightarrow\quad
\text{divisor-collision or conductor invariant}.
\]

It does not distinguish regular from singular pencils, or different Segre types, through distinct boundary singularities. The inherited inverse can recover the pencil before degeneration, but the new boundary geometry does not classify what happens to that recovered object along natural compactifying families.

### 7.3 No meaningful part of the orbit-closure geometry is classified

For the orbit closures \(Z_R\), the manuscript does not determine dimensions, irreducible components, generic stabilizers, normality, singular loci, boundary divisors, closure relations, or normalization. It gives one common point and its normalization fibre.

A single common point is not a nontrivial portion of an orbit-poset classification.

### 7.4 There is still no natural compactification theorem

The paper does not construct a compactification of the effective pencil-failure stack on which the failure functor extends with geometrically meaningful boundary strata. Nor does it identify \(Y_g\) or an orbit closure with a previously central compactification whose geometry was unknown.

This is the missing bridge between the technically impressive inverse theorem and the now-substantial divisor singularity theory.

---

## 8. Top-four originality and significance

### 8.1 The squarefree theorem is global but combinatorially elementary after root ordering

Once the common roots are ordered, the completed image is a union of coordinate subspaces. The conductor and branch-intersection formulas follow from a block-support monomial ideal; the depth calculation is Stanley–Reisner topology.

There is nothing wrong with an elementary mechanism. A theorem with an elementary proof can be exceptional. But then its statement should solve a problem of unmistakable prior importance or unlock consequences much broader than the calculation itself.

Here the theorem is broad in parameters but narrow in ambient geometry: binary forms, squarefree common divisor, and one family of Grassmannian subspace images. The paper does not yet derive a major external consequence from the block model.

### 8.2 The collision atlas is exact but still mostly a presentation theorem

Writing a singularity as an intersection of branch kernels is useful. For a general-journal contribution, one expects the presentation to lead to a classification, a resolution, a new singularity property, intersection theory, topology, or a moduli consequence. Most of those steps remain open.

### 8.3 The main inverse invariant remains deliberately information-bearing

The unmarked local-algebra theorem is striking in formulation, and the proof that the pencil can be recovered after forgetting grading, coordinates, tensor factors, and nonlinear automorphisms is nontrivial.

Nevertheless, the failure algebra is engineered so that its first nontrivial relation contains the pencil coefficient data. The achievement is intrinsic recovery of that designed encoding. This differs from showing that a standard independently central invariant unexpectedly has Torelli power.

The new divisor geometry makes the relation space less ad hoc, but it has not yet established that the failure invariant is inevitable in a classical geometric problem.

### 8.4 The historical originality audit is still incomplete

The manuscript correctly preserves the limitation concerning Ballico 1993. It does not fabricate a theorem-level comparison or infer nonanticipation from lack of access.

That is responsible scholarship. It also leaves the broad historical claim unresolved. For a specialist submission, this limitation can be disclosed and bounded. For a top-four originality certification centered on a “failure-locus to reconstruction” program, the closest named failure-locus predecessor remaining unread is still a material problem.

### 8.5 The new combinatorial literature positioning is insufficient

The paper now cites the classical reciprocal quotient through Grinberg and retains the factorization/conductor comparisons. It should also compare the squarefree block ring with the established literature on Stanley–Reisner rings, coordinate-subspace arrangements, subspace-arrangement conductors, seminormal unions, and skeleton ideals.

The current proof independently derives what it needs, but originality is not established merely by reproving a combinatorial commutative-algebra calculation inside new notation. The manuscript must identify which part of the block model, conductor equality, and homological formula is genuinely new for this geometric image.

---

## 9. Architecture and exposition

The revision improves the reading order, but the underlying architectural problem remains.

The principal PDF is now 80 pages and contains 269 labels. It retains at least the following programs:

1. sharp reconstruction of every quadratic pencil;
2. one-point ungraded local-algebra reconstruction;
3. Grassmannian and curve-supported reconstruction;
4. moving-family and source-bundle recovery;
5. general Schur-coefficient reconstruction;
6. image recognition and nonlinear automorphism kernels;
7. covering-map reconstruction;
8. stack rigidification;
9. canonical divisor-incidence normalization;
10. split and collision singularity models;
11. global binary finite-flat normalization fibres;
12. squarefree conductor and branch stratification;
13. arbitrary binary collision atlases;
14. pure-power fibre commutative algebra;
15. common first-relation orbit degeneration;
16. spectral specialization and fixed-strata results.

Moving many inherited arguments to appendices does not make them conceptually subordinate when the article continues to advertise and preserve them as part of the submission.

I strongly recommend splitting the project into at least two papers:

- a reconstruction paper centered on the sharp unmarked inverse and its relative/local forms;
- a divisor-image paper centered on normalization, conductors, binary collision geometry, and reciprocal fibres.

A third, more specialized paper may be appropriate for the stack, covering-map, and spectral extensions.

The present article still feels like the audited cumulative output of a research pipeline. The top general journals publish long papers, but usually because one central theorem requires a long proof—not because every successful extension has been retained in one submission.

---

## 10. Specific technical and expository points

These should be addressed even for a specialist submission.

1. **State the complete-local hypotheses in Lemma `lem:formal-image-v153`.** Include locality, common residue field, continuity, and Noetherian completeness in the cotangent-surjectivity assertion.

2. **Cite analytic unramifiedness of excellent reduced local rings.** The reduced-completion step is standard but load-bearing.

3. **Name and cite miracle flatness.** The finite-flat factorization theorem should not hide its main flatness input in a sentence about systems of parameters.

4. **Clarify local selection of a residual member coprime to the gcd.** Explain the topology and descent used in the base-change theorem.

5. **Separate weighted grading from maximal-ideal grading throughout.** The reciprocal Hilbert series is weighted; several readers will otherwise infer an ordinary local Hilbert function.

6. **Give a formal Hensel product lemma for root clusters.** The tensor-product decomposition of full scheme fibres deserves a separately reusable statement.

7. **Cite the partition-stratum closure order.** The root-merging assertion is correct but should be linked to the standard symmetric-product stratification literature.

8. **State the coherent-ideal globalization argument for the conductor.** Make explicit that equality after completion at every squarefree point implies equality of the coherent ideals.

9. **Isolate the equalizer description of the block arrangement.** Pairwise compatibility is sufficient here because of the coordinate monomial structure; this is not true for arbitrary unions without hypotheses.

10. **Cite Hochster/Stanley–Reisner machinery.** The depth proof is effectively a standard multigraded Betti calculation even though a self-contained argument is included.

11. **Explain the relation between the block ideal and known skeleton or transversal ideals.** This is essential for novelty positioning.

12. **Do not call the collision atlas a classification.** It is an exact incidence presentation; the local isomorphism types remain largely unsimplified.

13. **Expand the finiteness proof for the branch maps in the atlas.** Record explicitly which factor coefficients are integral and which quotient coefficients are polynomial functions after monic division.

14. **Make coordinate-independence functorial.** The current final paragraph is plausible; a short proposition on representability and uniqueness of the completed incidence functor would be cleaner.

15. **Spell out the equivariance in the Fitting calculation.** Identify the acting general linear group and the representations spanned by the displayed minors.

16. **Isolate the specialization lemma in the reciprocal proof.** State why membership in `nI` specializes to membership in the binary variable ideal times the binary relation ideal.

17. **Do not let 9867 substitute for geometry.** The dramatic equation count is informative, but a large number is not by itself a structural consequence.

18. **Add at least one invariant beyond minimal generators for multivariate reciprocal fibres.** A Hilbert function, type, first nontrivial syzygy representation, or resolution pattern would materially deepen the theorem.

19. **Keep the full `GL(E)` versus `PGL(V)` distinction in every summary.** The revised introduction does this well; later references to “pencil orbit boundary” should be equally explicit.

20. **Keep the two-stage specialization visible.** No single uniform one-parameter subgroup is proved for all starting pencils.

21. **Complete or sharply bound the Ballico comparison.** The limitation must remain in the submitted article until resolved.

22. **Do not imply regression certification from the v153 receipt.** The receipt honestly says that the historical 28 checks were not rerun; summaries should preserve that qualification.

23. **Separate reproducibility infrastructure from the mathematical narrative.** Source hashes and nondeletion manifests belong in the repository, not in the significance case.

24. **Split the submission.** Reordering alone has not solved the scale problem.

---

## 11. Scorecard against the v152 report

### 11.1 Formal branch and completed-image rigor

**Closed.**

The formal-image lemma, separated completed germs, Artin cancellation, and direct codimension estimate address the earlier proof-compression concerns.

### 11.2 General all-rank singular Fitting ideal

**Closed for the generalized double-root pinch model.**

The ideal is explicitly evaluated. This does not compute singular schemes for every collision atlas ring.

### 11.3 A global conductor and branch theorem

**Materially closed on the entire binary squarefree-common-divisor locus.**

This is a substantial advance. The multivariate and collided-root conductors remain open.

### 11.4 Scheme-theoretic multiple intersections

**Closed for all normalization branches on the binary squarefree locus, and for nested binary divisor-degree images.**

The general multivariate divisor-poset intersection problem remains open.

### 11.5 Arbitrary higher root collisions

**Addressed at the level of an exact completed incidence atlas.**

A classification of the resulting singularities and their invariants is not supplied.

### 11.6 Structural theory of reciprocal fibres

**Materially addressed but not completed.**

The minimal relation representation and complete-intersection classification are real structural results. Most higher homological and numerical invariants in the multivariate case remain unknown.

### 11.7 Integration with actual pencil degenerations

**Still conceptually incomplete.**

The common point is reached by genuine failure algebras, but it does not organize distinct pencil degeneration types or classify orbit boundaries.

### 11.8 A nontrivial orbit-closure or compactification theorem

**Open.**

No substantial part of the `GL(E)` orbit-closure geometry or a natural compactification of the effective pencil-failure moduli problem is determined.

### 11.9 Literature and historical priority

**Improved but open.**

The reciprocal algebra now has a primary comparison. The combinatorial arrangement literature needs attention, and Ballico 1993 remains documentary-open.

### 11.10 Architecture

**Improved in order, unresolved in scope.**

The abstract is better and the two principal packages are visible. The 80-page article still contains too many independent theorem programs.

---

## 12. Conditions for another top-four evaluation

I would not recommend another top-four round triggered by one more collision model, a longer exact-check suite, a larger explicit equation count, or another reordering of the same inherited blocks.

A serious future top-four case should do at least one of the following at unmistakably global scale:

1. **Multivariate divisor-image geometry.** Determine a conductor/branch stratification, local normal forms, or a canonical semiresolution for a genuinely multivariate class substantially larger than the split locus.

2. **Collision singularity classification.** Convert the binary incidence atlas into closed formulas for conductors, depth, type, Betti tables, seminormalization, and closure relations for all root partitions.

3. **A natural compactification.** Construct a compactification of the effective pencil-failure moduli problem on which the failure functor extends, and identify boundary strata with geometric pencil invariants.

4. **Orbit-closure geometry.** Classify a nontrivial portion of the full first-relation orbit-closure poset or determine normalization and singularities of a meaningful family of orbit closures.

5. **Boundary detection of pencil data.** Relate Segre or congruence degeneration types to intrinsic conductor/collision types in the first-relation boundary.

6. **Deep reciprocal-fibre algebra.** Determine the Hilbert functions, types, resolutions, or representation-stable syzygies of the multivariate pure-power fibres, with consequences beyond the constructed example.

The historical and adjacent-literature comparisons must also be completed to the level appropriate for the resulting theorem. Finally, the submission should be separated into coherent papers rather than continuing to accrete all prior programs.

---

## 13. Final assessment

Revision 153 deserves substantial credit. It is not an incomplete shell, not a cosmetic response, and not merely proof engineering. It contains a genuine global binary conductor theorem, a uniform finite-flat factorization theorem, exact all-collision incidence charts, an evaluated singular Fitting ideal, and a structural theorem on multivariate reciprocal fibres.

I therefore withdraw, for this materialized article, the earlier procedural conclusion that v153 lacked a review object. A complete review object now exists, and it contains serious new mathematics.

I nevertheless recommend rejection at the stated top-four level.

The strongest new global theorem becomes a coordinate-subspace/Stanley–Reisner calculation after ordering binary roots. The arbitrary-collision result is a presentation rather than a singularity classification. The multivariate fibre theorem stops at minimal generators and complete-intersection failure. The connection to pencils remains a common extreme collapse under the very large full coordinate-change group, not a moduli boundary theorem. The closest named historical comparison remains incomplete, and the article continues to combine too many independent programs in one 80-page submission.

The appropriate decision for *Annals*, *Acta*, *Inventiones*, or *JAMS* is therefore:

**Reject in the present form.**

After splitting the manuscript, strengthening the literature comparison, and polishing the formal arguments, I would regard the divisor-geometry component and the reconstruction component as credible candidates for strong specialist journals. A future top-four case would require a qualitatively new global theorem connecting the divisor singularities to the natural geometry of quadratic-pencil moduli—not another incremental closure of the current issue list.
