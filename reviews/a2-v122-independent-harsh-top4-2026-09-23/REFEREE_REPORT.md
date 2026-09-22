# Independent harsh top-four referee report — A2 revision 122

**Manuscript:** *Ramification and intrinsic primary boundaries in multiplication failure*  
**Author:** Qian Qi  
**Repository:** TrillionniumFoundation/theta-theory  
**Reviewed revision:** revision/a2-v122-intrinsic-primary-k3-boundaries-2026-09-23  
**Reviewed branch head:** 37480f3872b5c9f4ae18731e60a799986114c427  
**Mathematical-source commit:** 790fff70e40ccdbe97d2569792535d6fe6cb6b2a  
**Published-product commit:** 37480f3872b5c9f4ae18731e60a799986114c427  
**v121 base:** 44f6b0bf3bb4f1f8c2a87d84beb61d82194fd5e7  
**Principal journal reading object:** geometry.pdf, 63 pages  
**Date:** 23 September 2026

## Status of this report

This is an owner-requested, AI-assisted external-referee-style report. It was not commissioned by Annals of Mathematics, Inventiones Mathematicae, the Journal of the American Mathematical Society, Acta Mathematica, or another journal, and it should not be represented as a journal-issued report.

I reviewed the v122 mathematical source rather than only the response letter. In particular I read the new relation–ramification section, the intrinsic primary-power section, the recovery theorem, the retained universal determinantal theorem and elliptic family, the dependency map, the literature audit, the v120 Referee-II report and response, and the branch-scoped build and diagnostic evidence.

The standard applied below is the standard of an exceptionally selective general mathematics journal. At that level correctness is only the first threshold. One must also have a theorem of sufficient conceptual scale, a priority position closed against the nearest literature, and a formulation whose natural geometric scope is not obtained by deleting the hardest stratum.

# Recommendation

## Reject in the present form at a general top-four mathematics journal.

This is a materially stronger paper than v120 and v121. I do **not** find a fatal contradiction in the new v122 local algebra. The chain

\[
\text{quadratic relations}
\longrightarrow
\text{finite quadratic morphism}
\longrightarrow
\text{ramification determinant}
\longrightarrow
\mathcal I_D=\mathcal I_\Delta\mathcal I_E
\longrightarrow
\text{intrinsic embedded torsion}
\longrightarrow
\text{recovery of }Y_R
\]

is mathematically coherent under the stated hypotheses. The local model
\[
\mathcal I_D=t(t,f)
\]
survives direct scrutiny, and the displayed ordinary-power decomposition
\[
\mathcal I_D^n
=
\mathcal I_\Delta^n\cap\mathcal I_E^{2n}
\]
is the correct regular-local consequence of that model. The recovery of the embedded support from the annihilator of the nilradical is also real rather than merely set-theoretic.

The reason for rejection is therefore no longer the old v120 criticism that the paper only treats the rigid Hilbert-function \((1,2,2)\) case. Revision 122 genuinely answers that objection by passing to nonempty open classes with Hilbert functions \((1,3,3)\) and \((1,4,6)\), with positive-dimensional algebra-moduli quotients and a K3 case.

The remaining top-four obstacles are more structural:

1. the closest historical failure-locus source, Ballico 1993, is still unread at theorem level by the authors' own audit;
2. the new fixed-tensor theorem is deliberately restricted to the projection-corank-at-most-one open, leaving the first genuinely harder fixed-tensor strata outside the theorem;
3. in the K3 case the paper proves existence of an open algebra class and recovery of each associated abstract K3, but does not prove that the resulting K3s themselves vary in moduli, compute the image in K3 moduli, or recover a polarization, the quadratic map, or the algebra;
4. a substantial part of the determinantal primary architecture is not compared theorem-by-theorem with the classical De Concini–Eisenbud–Procesi / Bruns–Vetter theory of symbolic powers and primary decompositions of determinantal ideals and products;
5. once the local model \(t(t,f)\) is established, several advertised “all powers” conclusions are formal regular-sequence consequences. They are useful, but they do not by themselves supply the missing top-four scale.

In my view v122 has become a serious algebraic-geometry/commutative-algebra paper. It has not yet crossed the threshold for one of the four most selective general mathematics journals.

# 1. What v122 genuinely fixes

A fair harsh report must not recycle objections that the revision has actually solved.

## 1.1 The “no genuine moduli” objection is substantially answered

The new class
\[
G_e^\circ\subset \operatorname{Gr}(e,\operatorname{Sym}^2V),
\qquad e=3,4,
\]
is not a finite orbit list.

For
\[
S_R=\operatorname{Sym}^2V/R,
\qquad
B_R=\mathbf C\oplus V\oplus S_R,
\]
the paper proves nonemptiness of the basepoint-free smooth-ramification locus and obtains orbit-dimension deficits at least
\[
1 \quad (e=3), \qquad 9 \quad (e=4).
\]

That is a real response to the v120 criticism. The manuscript should not be reviewed as though it still only contained the two binary-quadratic orbit types of Hilbert function \((1,2,2)\).

## 1.2 The global consequence is no longer merely “transport the finite algebra”

The new recovery theorem is genuinely different from the earlier global-section transport results.

The paper first reconstructs the embedded support \(E_R\) intrinsically from the nonreduced scheme \(D_R\), then uses the graph-bundle description
\[
E_R \sim_{\mathrm{bir}}
Y_R\times \mathbf P^N
\]
and stable-birational cancellation for non-uniruled bases to recover \(Y_R\).

Thus the K3/genus-one conclusion is not obtained by merely embedding a previously known punctual Fitting calculation in projective space.

## 1.3 The primary descent objection is largely closed on the new locus

The new argument does not ask a referee to trust specialization of a universal primary decomposition. The local fixed-tensor calculation produces
\[
\mathcal I_D=(t^2,tf)=t(t,f)
\]
directly, and the global two-stratum lemma globalizes the intrinsic ideals
\[
\mathcal I_\Delta,\qquad \mathcal I_E.
\]

This is a major improvement over a proof that would only identify radicals or associated supports.

## 1.4 The computational and build record is strong

The branch-scoped build is source-bound. The receipt records:

- source commit 790fff70e40ccdbe97d2569792535d6fe6cb6b2a;
- 63 pages for geometry.pdf;
- 130 pages for the complete companion;
- 28 pages for applications.pdf;
- no overfull hboxes in the three products;
- proof certification = false;
- priority certification = false.

The exact diagnostics check the local ordinary-power identities for \(n=1,\ldots,8\), and include explicit rational examples for both \(e=3\) and \(e=4\). The \(e=4\) example is checked chart-by-chart for basepoint-freeness and smoothness of the quartic Jacobian determinant.

These checks are useful audit evidence. They are not being misrepresented as a proof of the general theorem, and no referee should revive the old source-bound-build objection.

# 2. Technical audit of the new relation–ramification chain

I summarize what I checked because my negative recommendation is not based on an invented algebraic failure.

## 2.1 Restriction–contraction identity

For a hyperplane \(H=\ker\alpha\subset V\), the exact sequence
\[
0\to\operatorname{Sym}^2H
\to \operatorname{Sym}^2V
\xrightarrow{c_\alpha} V
\to0
\]
with the correct projective twist is sound in characteristic zero.

The two cokernels
\[
\operatorname{coker}
(\operatorname{Sym}^2H\to S_R)
\quad\text{and}\quad
\operatorname{coker}
(R\xrightarrow{c_\alpha}V)
\]
are indeed the same quotient of \(\operatorname{Sym}^2V\) by
\(R+\operatorname{Sym}^2H\).

The determinant is therefore a degree-\(e\) equation on \(\mathbf P(V^*)\).

## 2.2 Finite quadratic morphism and ramification

If \(R\) is basepoint-free, the associated map
\[
\phi_R:\mathbf P(V^*)\to\mathbf P(R^*)
\]
satisfies
\[
\phi_R^*\mathcal O(1)=\mathcal O(2).
\]
The ampleness argument excludes positive-dimensional fibres; proper plus quasi-finite gives finiteness. The degree
\[
\deg \phi_R=2^{e-1}
\]
is correct.

The Jacobian determinant is the determinant of the contraction matrix up to transpose and units. The radial direction is invertible in the projective tangent calculation, so the determinant defines the ramification Fitting scheme with the stated scheme structure.

I see no defect here.

## 2.3 The basepoint-free / first-order-spanning equivalence

The equivalence
\[
R\text{ basepoint-free}
\Longleftrightarrow
\gamma_R(HV)=S_R \text{ for every }H
\]
is correct.

The key annihilator identity is
\[
(HV)^\perp=\mathbf C\alpha^2,
\]
so a failure of surjectivity is exactly a common zero of the quadrics in \(R\).

This is an efficient and conceptually useful bridge between the projective morphism and the later block elimination.

## 2.4 Nonemptiness of the admissible open

The incidence counts in Proposition 2.3 are plausible and, at the numerical level, correct.

For fixed \(H\), the restriction
\[
\operatorname{Sym}^2H\to S
\]
is a \(p\times p\) matrix. Corank at least two has codimension four. After adding the \((e-1)\)-dimensional hyperplane parameter, the universal bad locus has dimension
\[
\dim T+e-5<\dim T
\]
precisely for \(e=3,4\).

Likewise, nonsurjectivity of
\[
HV\to S
\]
has codimension \(e\), and the universal incidence has dimension \(\dim T-1\).

This proves that the desired open conditions can meet.

The subsequent use of the universal determinant hypersurface is also reasonable: after the corank-two locus has been removed, the determinant hypersurface in the matrix space is smooth, and the evaluation map is a submersion in the tensor direction.

I do, however, ask for a more formal relative statement in the submitted version; see Major issue M4 below.

## 2.5 Full multiplication Fitting ideal

This is the central local calculation, and it is sound.

Because the augmentation ideal is cube-zero, for every \(m\ge2\) the image of the multiplication map is
\[
\mathbf C\cdot1+K+K^2.
\]

On a frame chart the presentation has the block form
\[
\begin{pmatrix}
1&0&0\\
0&M&0\\
0&A_0&\gamma_R\operatorname{Sym}^2M
\end{pmatrix}.
\]

Every nonzero maximal minor uses the scalar column and all \(e\) linear columns. Hence
\[
\mathcal I_D
=
(\det M)\,
I_p(\gamma_R\operatorname{Sym}^2M).
\]

Near projection corank one, after inverting an \((e-1)\)-minor,
\[
M=\operatorname{diag}(I_{e-1},t).
\]
Writing the quadratic block as
\[
[A,tB,t^2c],
\]
the condition \([A,B]\) surjective gives equality of column modules
\[
\operatorname{im}[A,tB,t^2c]
=
\operatorname{im}[A,tI_p].
\]

Along smooth ramification, \(A\) has corank one, and Schur reduction gives the local ideal
\[
\mathcal I_D=t(t,f).
\]

This is a genuinely scheme-theoretic statement, not a rank-only argument.

## 2.6 Primary decomposition and all ordinary powers

In a regular local ring with parameters \(t,f\),
\[
(t^n)\cap(t,f)^{2n}
=
t^n(t,f)^n.
\]

Thus the displayed global formula
\[
\mathcal I_D^n
=
\mathcal I_\Delta^n
\cap
\mathcal I_E^{2n}
\]
is correct on the stated smooth two-stratum locus.

The nilradical index \(2n\) along \(E\) also follows directly:
\[
t^{2n}\in t^n(t,f)^n,
\qquad
t^{2n-1}\notin t^n(t,f)^n.
\]

The embedded torsion length at the generic point of \(E\),
\[
\frac{n(n+1)}2,
\]
is exactly the length of a two-dimensional regular local ring modulo
\((t,f)^n\).

I do not see an algebraic error in Theorem 3.3.

## 2.7 Intrinsic annihilator

For \(n=1\),
\[
\sqrt{\mathcal I_D}=(t),
\qquad
\mathcal I_D=t(t,f).
\]
Hence the nilradical of \(\mathcal O_D\) is represented by
\[
(t)/t(t,f),
\]
and its annihilator is
\[
(t,f)/t(t,f).
\]

Therefore the annihilator recovers \(E\) with its scheme structure. This is a good invariant and the manuscript is right to distinguish it from a choice of embedded primary component.

## 2.8 Cancellation and K3 birational rigidity

The cancellation statement is correct in substance: for a non-uniruled smooth projective variety, the maximal rationally connected quotient of
\[
Y\times\mathbf P^r
\]
is birational to \(Y\). Therefore stable birationality between two such products forces birationality of the non-uniruled bases.

For smooth genus-one curves, birationality means isomorphism.

For K3 surfaces, a birational map between smooth minimal K3 surfaces is an isomorphism. The supplied two-form/blowup argument is compatible with this standard fact.

I would nevertheless cite the standard maximal-rationally-connected quotient formulation rather than make the elementary paragraph carry the full general cancellation statement by itself.

# 3. Blocker B1 — the Ballico 1993 comparison is still not closed

This remains a top-four threshold issue.

The manuscript itself says:

> the nearest-source comparison with Ballico's higher-order failure-locus article is not completed.

That is the correct scholarly disclosure. It also means the originality case is not ready for a general top-four journal.

The unresolved source is:

E. Ballico, *On the Failure Locus of Higher Order Properties of Embeddings in Projective Spaces*, Math. Nachr. 163 (1993), 5–13, DOI 10.1002/mana.19931630102.

I independently confirmed the bibliographic record. I also inspected the accessible full text of Ballico's 1996 paper *On the failure cycles for the quadratic normality of a projective variety*, Pacific J. Math. 172 (1996), 307–313. That later paper studies multiplication/normality failure on Grassmannian linear sections and explicitly cites the 1993 paper as the preceding failure-locus source.

The 1996 paper does **not** establish that Ballico 1993 anticipates v122. Nor does it establish non-anticipation. It does establish that the inaccessible 1993 paper is not a random title match: it belongs to the same historical failure-locus program and therefore cannot be omitted from the priority audit.

For a specialist submission, one could perhaps complete this comparison during revision.

For a top-four submission, I would not accept a principal novelty claim while the closest named predecessor remains unread at theorem level.

### Required action

Obtain the complete Ballico 1993 paper through a research library, interlibrary loan, author archive, or another lawful source, and add a theorem-by-theorem comparison covering at least:

1. the parameter Grassmannian;
2. complete versus incomplete linear series;
3. the exact multiplication map whose failure is studied;
4. whether the failure locus is reduced, cycle-theoretic, determinantal, Fitting-theoretic, or scheme-theoretic;
5. moving versus fixed finite contacts;
6. embedded/nonreduced structure;
7. conductor or quotient-algebra mechanisms;
8. the relation to higher-order embeddings and jet separation;
9. the global hypotheses and degree ranges.

Until that is done, priority certification should remain false.

# 4. Blocker B2 — the fixed-tensor theorem stops exactly before the higher-corank geometry

The most serious mathematical-scope limitation in v122 is not hidden; it is stated clearly.

The new theorem works on
\[
U_R=
\{K:\operatorname{rank}(K\to V)\ge e-1\}.
\]

The locus
\[
\operatorname{rank}(K\to V)\le e-2
\]
is omitted.

For the local theorem this restriction is natural: on the corank-one divisor there is a single parameter \(t\), the quadratic restriction has at worst corank one on the admissible class, and the failure ideal collapses to
\[
t(t,f).
\]

But this is also exactly why the theorem becomes so clean.

A top-four paper about the scheme of multiplication failure for the fixed algebras \(B_R\) should not leave the first locus where the projection has two-dimensional kernel completely outside the fixed-tensor classification.

The complement has high codimension, but high codimension is not a reason to ignore it in a paper whose novelty is **embedded and associated scheme structure**. Embedded primes are themselves high-codimensional data.

The retained universal theorem does not completely solve this objection. It classifies a generic-tensor first-order-spanning situation before specialization. The manuscript is careful not to claim that an arbitrary fixed tensor inherits that primary decomposition. That caution is mathematically correct, but it leaves the fixed \(B_R\) geometry unresolved on the omitted stratum.

### Why this matters

The phrase “the full failure scheme remembers a K3 surface” is strongest when “full” refers to the natural failure scheme on the whole Grassmannian of unital \(e\)-planes.

At present it means the full Fitting ideal **after restricting to the projection-corank-at-most-one open**.

That is a legitimate theorem. It is not the same theorem.

### Required action for top-four reconsideration

At least one of the following is needed:

1. extend the fixed-tensor primary analysis across projection corank two and describe the new associated supports and nilpotent orders;
2. prove a structural theorem showing that the higher-corank locus is canonically reconstructible from the open failure scheme and introduces no new moduli-relevant information;
3. replace the smooth-ramification hypothesis by a stratified theorem in which higher corank and singular ramification are part of one unified mechanism.

Simply restating that the locus is omitted will not raise the theorem to the required scale.

# 5. Blocker B3 — the K3 case has not yet been shown to vary in K3 moduli

For \(e=4\), the paper proves that the admissible relation spaces have an algebra-orbit dimension deficit at least nine.

This proves that the algebras \(B_R\) have genuine moduli.

It does **not** prove that the ramification K3 surfaces
\[
Y_R\subset\mathbf P^3
\]
have genuine moduli inside this family.

The map
\[
R \longmapsto [Y_R]
\]
to the moduli of quartic K3 surfaces may have positive-dimensional fibres. The paper does not compute its differential, image dimension, generic fibre, degree, or even prove nonconstancy of the abstract K3 isomorphism class.

For \(e=3\) this problem is handled much better: the Hesse subfamily has an explicit nonconstant \(j\)-invariant. Thus the manuscript actually proves that the embedded failure schemes vary through nonisomorphic genus-one curves.

There is no comparable result for \(e=4\).

The diagnostics contain one explicit smooth quartic example. That proves non-vacuity, not non-isotriviality.

### Why this matters for the headline

The most striking advertised statement is that a multiplication-failure scheme “recovers a K3 surface.”

For top-four significance I would want to know that this is not a single abstract K3 type repeated over a large family of unrelated algebras.

### Required action

Produce at least a one-parameter family \(R_t\in G_4^\circ\) and prove that the polarized quartics \(Y_{R_t}\) are nonisomorphic for general \(t\). Better would be a calculation of the dimension of the image of
\[
G_4^\circ/\operatorname{PGL}(V)
\longrightarrow
\mathcal M_{\mathrm{quartic\ K3}}.
\]

A period-theoretic, invariant-theoretic, or infinitesimal deformation calculation would all be acceptable.

Without such a result, the K3 part is a beautiful existence-and-recovery statement but not yet a moduli theorem.

# 6. Blocker B4 — the determinantal primary literature comparison is not adequate

The retained weighted determinantal theorem is not a routine side lemma. It is one of the manuscript's principal structural claims.

The paper proves, for a generic \(q\times p\) matrix \(A\),
\[
F
=
t\sum_{i=0}^{q}t^{q-i}I_i(A)
=
(t)\cap
\bigcap_{j=1}^{q}
(t,I_j(A))^{(q-j+2)}.
\]

The proof is convincing as written.

The originality positioning is not.

There is a classical literature specifically on symbolic powers, products and primary decompositions of determinantal ideals. In particular:

- C. De Concini, D. Eisenbud and C. Procesi, *Young Diagrams and Determinantal Varieties*, Invent. Math. 56 (1980), 129–165, includes products of determinantal ideals, symbolic powers, and order of vanishing;
- W. Bruns and U. Vetter, *Determinantal Rings*, includes chapters on powers of maximal-minor ideals and primary decomposition and explicitly attributes the symbolic-power and product decompositions to the De Concini–Eisenbud–Procesi theory.

The v122 bibliography cites modern generic-determinantal normality and height results, but I do not see a direct theorem-level comparison explaining how the weighted formula above differs from, specializes, or can be derived from the classical determinantal primary-decomposition machinery.

I am **not** asserting that Theorem \(\ref{thm:weighted-primary}\) is contained in those sources. The presence of the extra scalar \(t\) and the special matrix \([A,tI]\) may produce a genuinely useful new weighted degeneration.

But at top-four level the authors must make that distinction themselves and prove the precise novelty boundary.

### Required action

Add a dedicated comparison that answers:

1. Is \(F=tI_q([A,tI_q])\) an instance, flat degeneration, Rees specialization, or initial ideal of a classical product of determinantal ideals?
2. Can the displayed symbolic-power intersection be obtained directly from the De Concini–Eisenbud–Procesi \(\gamma\)-functions/order formulas?
3. If not, what property of the repeated scalar \(t\) makes the theorem genuinely different?
4. Which part is new: the ideal identity, irredundancy, exact nilpotency orders, the geometric interpretation, or only the application to multiplication failure?

A top-four originality claim cannot leave this at the level of “generic determinantal normality is classical.”

# 7. Major issue M1 — the K3 recovery is elegant but currently soft

Theorem 4.2 says that an abstract isomorphism
\[
D_R\simeq D_{R'}
\]
implies
\[
Y_R\simeq Y_{R'}.
\]

The proof has two stages:

1. recover \(E_R\) as the annihilator scheme of the nilradical;
2. use the fact that \(E_R\) is a vector bundle over \(Y_R\times\mathbf P^{p-1}\), hence stably birational to \(Y_R\), and cancel projective-space factors.

This is correct and elegant.

But once the embedded support has been found, the K3 recovery is a stable-birational argument rather than a new Torelli-type mechanism.

The theorem does **not** recover:

- the quartic polarization;
- the embedding \(Y_R\subset\mathbf P^3\);
- the degree-eight quadratic map \(\phi_R\);
- the relation space \(R\);
- the local algebra \(B_R\);
- or even a finite set of possible \(R\)'s from \(D_R\).

The manuscript is commendably explicit about these limits.

For a specialist journal, this exact level of recovery may be a satisfying theorem.

For Annals/Inventiones/JAMS/Acta, I would want the reconstruction mechanism to carry more of the original geometry.

### Stronger directions

Any one of the following would substantially improve the case:

- recover the polarized K3 \((Y_R,\mathcal O_{Y_R}(1))\);
- recover \(\phi_R\) up to projective equivalence;
- prove generic finite-to-one reconstruction of \(R\) or \(B_R\);
- identify a canonical line bundle or projective model on \(Y_R\) directly inside the failure scheme;
- produce a period or Torelli invariant extracted from the embedded torsion.

# 8. Major issue M2 — the “all powers” theorem should not carry disproportionate novelty weight

Once
\[
\mathcal I_D=t(t,f)
\]
is known with \(t,f\) regular parameters, the formula
\[
\mathcal I_D^n
=
(t^n)\cap(t,f)^{2n}
\]
and the torsion length
\[
n(n+1)/2
\]
are short regular-local calculations.

They are worth recording because they make the nonreduced structure completely explicit.

They should not be presented as a second independent source of conceptual depth comparable to the relation–ramification identification.

The true theorem is the production of the local normal form from the multiplication tensor and the proof that its second parameter is the intrinsic ramification equation.

I recommend compressing the ordinary-power results into a corollary package unless a future revision extends them to a genuinely more complicated singular or higher-corank setting.

# 9. Major issue M3 — the manuscript needs a theorem-level comparison with classical linear systems of quadrics

The v122 literature section correctly credits:

- the Jacobian criterion;
- adjunction;
- projective-bundle cohomology;
- the Hesse invariant;
- standard K3 non-uniruledness.

That is not yet a literature review of the geometric construction being used.

The geometry of nets/webs/linear systems of quadrics, associated determinant or discriminant hypersurfaces, and quartic geometry is classical and remains an active subject.

The paper need not prove that all of this literature is directly overlapping. It must, however, tell the reader where its construction sits relative to that body of work.

The contribution being claimed is not “quartic K3 surfaces exist” or “a Jacobian determinant gives ramification.” It is the bridge from a quadratic relation tensor to the **embedded primary structure of a multiplication-failure scheme** and then to intrinsic recovery.

That bridge will look much stronger if the classical part is fenced off with precise theorem references rather than a short paragraph of ingredient citations.

### Required comparison

I would expect a subsection distinguishing at least:

1. classical discriminants/ramification of linear systems of quadrics;
2. classical symmetroid/determinantal quartic constructions;
3. finite endomorphisms or morphisms of projective space given by quadrics;
4. the manuscript's new Fitting ideal on the Grassmannian of unital planes;
5. the embedded associated component and its intrinsic annihilator;
6. the resulting reconstruction statement.

# 10. Major issue M4 — Proposition 2.3 should be rewritten as a clean relative-geometric lemma

I believe the nonemptiness argument can be made correct, but at present too much is compressed into one paragraph.

The proof moves through the following facts:

- a universal corank-two incidence has codimension four;
- a universal first-order-spanning failure incidence has codimension \(e\);
- their proper projections are proper closed subsets;
- the determinant is not identically zero;
- the total universal determinant hypersurface is smooth after deleting the corank-two locus;
- the generic fibre is geometrically regular;
- properness lets one delete the image of the nonsmooth locus;
- the construction descends from surjective tensors to kernels in the Grassmannian.

Each step is standard. Together they are the existence theorem supporting the whole K3 family.

For a top-four paper, I would isolate this as a proposition about the universal family with the maps and dimensions explicitly displayed.

In particular, state clearly:

1. the parameter spaces before and after quotienting by frames of \(S\);
2. why the universal determinant divisor is relative Cartier;
3. why it is flat over the chosen parameter open;
4. why the nonsmooth-fibre locus has proper closed image;
5. why every condition depends only on the kernel \(R\).

This is proof architecture, not a new mathematical obstacle.

# 11. Major issue M5 — the global definition of the intrinsic torsion should be formalized

Theorem 3.3 defines \(\mathcal T_n\) as “the kernel of localization of \(\mathcal O_{D^{[n]}}\) at its unique minimal associated point.”

On the current irreducible support this has the intended meaning: it is the maximal coherent subsheaf supported away from the minimal point, and locally it is
\[
(t^n)/t^n(t,f)^n.
\]

I would nevertheless prefer a coordinate-free sheaf definition, for example as the torsion subsheaf relative to the integral reduction \(n\Delta\), or as the kernel of the canonical map to the pushforward from the generic point / suitable dense open.

Then prove coherently that
\[
\operatorname{Ann}(\mathcal T_n)
\]
defines \(E^{[n]}\).

This matters because “intrinsic recovery” is the strongest conceptual claim of the paper. Its defining module should not look affine or ad hoc.

# 12. Major issue M6 — the relative flatness statement deserves a precise base-change lemma

The relative proof is plausible.

If \(\mathcal E\hookrightarrow\mathcal U\) is a relative regular immersion of codimension two, then
\[
\mathcal I_{\mathcal E}^j/\mathcal I_{\mathcal E}^{j+1}
\simeq
\operatorname{Sym}^j
(\mathcal I_{\mathcal E}/\mathcal I_{\mathcal E}^2),
\]
so the ordinary thickenings are flat over the parameter base. The same is true for the principal thickenings \(n\boldsymbol\Delta\).

The exact sequence
\[
0\to
\mathcal O_{\mathcal E^{[n]}}(-n\Delta)
\to
\mathcal O_{\mathcal D^{[n]}}
\to
\mathcal O_{n\Delta}
\to0
\]
then remains exact after arbitrary base change because the right term is flat.

This should be stated as a lemma with the exact Tor argument.

The current proof is likely sufficient for a specialist reader, but the paper makes arbitrary base change part of the advertised structure, so the formal mechanism deserves one clean reusable statement.

# 13. Major issue M7 — put the explicit \(e=4\) witness in the paper, not only in diagnostics

The diagnostic file contains an explicit rational four-dimensional relation system for \(e=4\), with a quartic Jacobian determinant checked on all four affine charts to be smooth and basepoint-free.

This is valuable.

A reader of the 63-page geometry article should not need to inspect JSON evidence to see a concrete K3 member.

Include one explicit \(R\) in the manuscript, perhaps in an example immediately after Proposition 2.3, and record:

- the four quadrics;
- the Jacobian quartic;
- a short certificate of basepoint-freeness;
- a short certificate of smoothness.

The general proof should remain the proof. The example should serve as a transparent non-vacuity witness and a benchmark for future computations.

# 14. Major issue M8 — prove or cite stable-birational cancellation in its natural language

Lemma 4.1 is correct in the cases needed.

However, the statement
\[
Y\times\mathbf P^r \dashrightarrow
Y'\times\mathbf P^{r'}
\quad\Rightarrow\quad
Y\dashrightarrow Y'
\]
for non-uniruled \(Y,Y'\) is naturally a statement about the maximal rationally connected quotient.

A top-four submission should cite that framework.

The current elementary argument says that a dominant rational map must be constant on general projective-space fibres, because otherwise the target would be covered by rational curves. This is the right idea, but it deserves either:

- a precise lemma proving that the images of those fibres cover a dense open and therefore make the target uniruled; or
- a standard MRC citation and a one-line application.

The K3-specific birational-to-isomorphic conclusion is classical and can also be cited, with the supplied two-form argument retained if desired.

# 15. Major issue M9 — the \(e=3\) and \(e=4\) stories are presently asymmetric

The \(e=3\) case has:

- a nonempty open class;
- an explicit Hesse family;
- a nonconstant \(j\)-invariant;
- nonisomorphic input algebras;
- nonisomorphic full failure schemes.

The \(e=4\) case has:

- a nonempty open class;
- one explicit smooth diagnostic example;
- abstract K3 recovery for each member;
- no proven variation of the K3 isomorphism class.

This asymmetry should be visible in the abstract and introduction.

At present the phrase “a smooth genus-one curve or a K3 surface” makes the two cases sound parallel. They are parallel at the local primary-structure level, but not yet at the moduli level.

# 16. Expository issue — the principal article is still carrying too much inherited machinery

The repository separation is responsible:

- geometry.pdf is the principal article;
- paper.pdf is the complete archival companion;
- applications.pdf is separate.

That is an improvement over treating the 130-page complete version as the submission.

Still, geometry.pdf is now 63 pages and its core input list retains a large amount of v120/v121 machinery after the new v122 theorem chain.

The v122 theorem itself is conceptually much cleaner than the historical path that produced it.

I recommend that the submitted article be reorganized around four blocks:

1. relation tensors and ramification;
2. the multiplication Fitting normal form;
3. intrinsic embedded torsion and reconstruction;
4. only the retained results actually needed to explain scope or applications.

No mathematical material needs to be deleted from the repository. The long historical development can remain in the archival companion.

A top-four paper should read as the shortest inevitable proof of its main theorem, not as a chronological record of every obstacle previously solved.

# 17. Minor and local points

## 17.1 Clarify “full failure scheme”

Whenever this phrase appears, append “on the projection-corank-at-most-one open” until the whole Grassmannian theorem is proved.

## 17.2 Separate algebra moduli from K3 moduli

The orbit-dimension deficit is an algebra-moduli statement. It is not a lower bound for the dimension of the image in K3 moduli.

Do not let the prose blur those two statements.

## 17.3 Make the role of ordinary powers explicit

The current text already says that the \(n\)-th powers are powers of the failure ideal, not new multiplication degrees. Keep that warning prominent.

## 17.4 State the reduction-independent invariant first

For the recovery theorem, the intrinsic object is the nilradical and its annihilator. Lead with this before discussing a chosen primary decomposition.

## 17.5 Cite the classical determinantal sources where symbolic order is used

The proof of the weighted theorem is self-contained, but the surrounding discussion should acknowledge the classical symbolic-order and product-primary-decomposition framework, not only generic normality.

## 17.6 Do not call the build a proof certificate

The repository already avoids this mistake. Preserve the explicit false certification flags.

# 18. What I would require for top-four reconsideration

I would not ask for another round of cosmetic strengthening. The next revision should answer structural questions.

A credible top-four resubmission would need the following package.

### E122.1 — close the nearest-source audit

Read Ballico 1993 in full and add the theorem-level crosswalk. Also compare the weighted determinantal theorem with De Concini–Eisenbud–Procesi and Bruns–Vetter.

### E122.2 — remove the designed-open limitation or explain it structurally

Give a fixed-tensor theorem on the projection-corank-two locus, or a general stratified theorem that includes it.

### E122.3 — prove genuine K3 variation

Show that the family \(R\mapsto Y_R\) is non-isotrivial for \(e=4\), preferably with a moduli-image dimension calculation.

### E122.4 — strengthen the reconstruction output

Recover at least a polarization, the quadratic map, or the relation tensor up to finite ambiguity; alternatively prove a comparably strong theorem for singular ramification/higher corank.

### E122.5 — consolidate the proof architecture

State the relative smoothness/flatness and intrinsic torsion mechanisms as clean global lemmas, cite MRC cancellation, and put an explicit \(e=4\) example in the article.

If E122.1–E122.4 are not pursued, I would recommend repositioning the paper as a strong specialist contribution rather than continuing to add formal corollaries of the two-parameter local model.

# 19. Final assessment

Revision 122 is not a failed revision.

It successfully repairs the most important mathematical-scale criticism of revision 120: the theory now reaches a positive-dimensional family of cube-zero algebras, including Hilbert function \((1,4,6)\), and it extracts an honest global K3 object from a nonreduced multiplication-failure scheme.

The central equations survive direct checking. I found no reason to call the new theorem false.

But a top-four decision turns on more than local correctness.

The paper still does not know its nearest historical predecessor at theorem level; it has not closed its determinantal priority boundary; its fixed-tensor classification omits the first higher-corank stratum; and its K3 result has not yet been shown to produce a genuinely varying K3-moduli family or to reconstruct the richer polarized/quadratic data from which the K3 arose.

Those are not editorial details.

They are exactly the remaining questions that decide whether this is a strong specialized theorem package or a theorem of the conceptual breadth expected by Annals/Inventiones/JAMS/Acta.

**Recommendation: reject in the present form at a general top-four mathematics journal, while encouraging a mathematically substantive revision rather than further cosmetic expansion.**
