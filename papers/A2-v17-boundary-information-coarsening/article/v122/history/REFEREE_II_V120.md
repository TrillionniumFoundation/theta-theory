# Referee II — harsh external top-four review of A2 revision 120

**Manuscript:** *Conductor boundaries and primary structures in multiplication failure*  
**Author:** Qian Qi  
**Repository:** TrillionniumFoundation/theta-theory  
**Reviewed revision:** revision/a2-v120-loewy-boundary-primary-2026-09-22  
**Reviewed branch head:** 1a6cae5a90b16d28cbfde3cbbb438e14dd31f474  
**Mathematical-source commit:** cade6b80d8300a2338b43c491c4d4b6bc648f2e4  
**Published product commit:** 13100ff1c85f77aee0ad28b1cdd459f2efda563c  
**Source-bound workflow run:** 35738068605  
**Controlling v119 review:** b409ec5eb4dfbb75850d90bff69a78604d3a512b  
**Referee-II branch:** review/a2-v120-referee-ii-harsh-top4-2026-09-22  
**Date:** 22 September 2026

## Status of this report

This is an owner-requested, AI-assisted external-referee-style report. It was not commissioned by Annals of Mathematics, Inventiones Mathematicae, the Journal of the American Mathematical Society, Acta Mathematica, or another journal, and it should not be represented as a journal-issued report.

This is a second independent review of revision 120. I reviewed the revision itself, not merely the earlier referee response. I inspected the new Loewy-boundary primary classification, the cube-zero factorization, the conductor-kernel theorem, the collision family, the sharpness construction, the expanded relative incidence and cohomology arguments, the dependency map, the literature audit, and the source/product receipts. I also stress-tested the algebra underlying the headline decompositions.

The standard applied here is the standard of an exceptionally selective general mathematics journal: correctness is necessary but not sufficient. The central question is whether the paper establishes a sufficiently broad, conceptually unavoidable theorem whose originality has been placed securely against the nearest literature.

# Recommendation

## Reject in the present form at a general top-four mathematics journal.

Revision 120 is mathematically much stronger than revision 119. I do not find a fatal contradiction in the new headline results, and I regard most of the concrete v119 repair requests as genuinely answered. The previous reproducibility defect is fixed. The conductor boundary is no longer represented only by equations or examples: the paper now gives a full primary decomposition for a natural Hilbert-function class. The stabilization bound is proved sharp. The relative arguments are substantially more explicit.

The reason for a negative top-four recommendation has therefore changed.

The present obstacle is not a missing local calculation. It is that the paper's deepest new classification is still confined to the first rigid nontrivial Loewy case, Hilbert function \((1,2,2)\), where over \(\mathbf C\) the problem reduces to two binary-quadratic orbit types. The general cube-zero formula preceding that classification is elegant but elementary at the level of maximal minors. It has not yet been converted into a structural primary theorem for a class with genuine moduli. At the same time, the nearest historical failure-locus source, Ballico 1993, remains unread at theorem level by the authors' own audit. These two facts prevent a reliable top-four significance claim.

I would regard the focused geometry article as a serious specialist-journal paper after literature closure and proof polishing. I do not regard the current revision as an Annals/Inventiones/JAMS/Acta-level result.

# 1. What revision 120 has genuinely accomplished

A harsh review should not recycle objections that the revision has already solved.

The new revision adds four substantive advances.

First, for a split cube-zero augmentation
\[
B=\mathcal O\oplus V\oplus S_2,\qquad
\mathfrak m^3=0,
\]
it derives the universal factorization
\[
\mathcal I_D=(\det M)\,
I_q\!\left(\gamma\operatorname{Sym}^2 M\right).
\]
This is an identity of the full Fitting ideal on the frame cover, not merely a radical statement.

Second, it completely analyzes the two complex local algebra types with Hilbert function \((1,2,2)\), producing embedded associated strata on the conductor boundary and an exact nilpotent structure.

Third, it proves that the codimension-\(r\) stabilization degree \(r+1\) is a sharp universal bound for every prescribed generating rank at least two.

Fourth, it repairs the relative functorial details and the source-bound build. Workflow run 35738068605 completed successfully from the pinned mathematical-source commit and produced the three advertised reading editions.

These are real improvements.

# 2. Stress test of the quadratic-layer factorization

Let \(K\) be the framed non-scalar part of a unital \((e+1)\)-plane and write its map into
\[
V\oplus S_2
\]
as
\[
\begin{pmatrix}M\\H\end{pmatrix}.
\]
Because \(\mathfrak m^3=0\), every multiplication image in symmetric degree \(m\ge2\) is
\[
\mathcal O\cdot 1+K+K^2.
\]
A presentation can therefore be written in block form as
\[
\begin{pmatrix}
1&0&0\\
0&M&0\\
0&H&\gamma\operatorname{Sym}^2M
\end{pmatrix}.
\]

Every nonzero maximal minor must use the scalar column and all \(e\) columns meeting the \(V\)-rows. Expansion then contributes \(\det M\), leaving a \(q\times q\) minor of the quadratic block. The \(H\)-variables do not create additional maximal minors.

I find this argument sound under the stated split locally-free hypotheses. It is also genuinely scheme-theoretic: no radical or rank-stratum reduction is used.

The paper should keep those hypotheses visible. The formula should not be advertised as a theorem for arbitrary degenerating families of local Artin algebras whose Loewy layers may fail to remain locally free.

# 3. The \((1,2,2)\) reduction is correct — and also explains the top-four limitation

For a complex local algebra with Hilbert function \((1,2,2)\),
\[
\dim V=2,\qquad \dim S_2=2,\qquad \mathfrak m^3=0.
\]
Hence
\[
\gamma:\operatorname{Sym}^2V\to S_2
\]
is a surjection with one-dimensional kernel. A nonzero binary quadratic over \(\mathbf C\) has exactly two orbit types relevant here: a double linear factor or two distinct linear factors.

Thus the two algebras
\[
B_{\rm sq}=\mathbf C[x,y]/((x,y)^3,y^2)
\]
and
\[
B_{\rm tf}=\mathbf C[x,y]/((x,y)^3,xy)
\]
do exhaust the class.

This is mathematically clean. But it also makes the conceptual limitation transparent: the "complete classification" is ultimately the complete analysis of two isomorphism types. There is no positive-dimensional moduli problem left inside this Hilbert-function stratum.

That is entirely acceptable for a specialist paper. It is a serious obstacle for a paper whose principal significance claim targets one of the four most selective general mathematics journals.

# 4. The explicit primary calculations survive direct checking

Put
\[
M=\begin{pmatrix}a&c\\ b&d\end{pmatrix},
\qquad
\delta=ad-bc,
\qquad
P=(a,c),\quad Q=(b,d).
\]

For the square type, the quadratic matrix is
\[
\begin{pmatrix}
a^2&2ac&c^2\\
ab&ad+bc&cd
\end{pmatrix}.
\]
Its \(2\times2\) minors are, up to units,
\[
\delta(a^2,ac,c^2)=\delta P^2.
\]
After the additional linear-layer determinant factor,
\[
I_{\rm sq}=\delta^2P^2.
\]

The decomposition
\[
\delta^2P^2=(\delta^2)\cap P^4
\]
is consistent with the \(P\)-adic order of \(\delta\), which is one.

For the two-factor type, the quadratic matrix is
\[
\begin{pmatrix}
a^2&2ac&c^2\\
b^2&2bd&d^2
\end{pmatrix},
\]
whose minors yield
\[
\delta J,\qquad
J=(ab,ad+bc,cd).
\]
Thus
\[
I_{\rm tf}=\delta^2J.
\]

The decomposition through
\[
J=P\cap Q\cap Q_0
\]
with
\[
Q_0=J+P^2+Q^2
\]
is compatible with the displayed quotient basis and annihilator calculation. The subsequent component
\[
Q_*=\delta^2Q_0+\mathfrak n^7
\]
is \(\mathfrak n\)-primary and the colon calculation used in the manuscript produces the claimed intersection
\[
I_{\rm tf}
=(\delta^2)\cap P^3\cap Q^3\cap Q_*.
\]

I found no fatal error in the associated-prime list
\[
\{(\delta),P,Q,\mathfrak n\}.
\]

Likewise, the exact nilradical index four follows from
\[
I=\delta^2J',\qquad
\delta\notin J',\qquad
\delta^2\in J',
\]
so that
\[
\delta^4\in I,\qquad \delta^3\notin I.
\]

The negative recommendation is therefore not based on a discovered algebraic contradiction.

# 5. The global primary statement is not yet written at the same level of rigor as the affine computation

This is the most important proof-quality criticism I have of the new theorem.

The affine-frame calculation is explicit. The passage from that calculation to a complete primary decomposition on the Grassmannian is considerably more compressed.

The paper says, in effect, that:

- the components survive polynomial extension by \(H\) and localization;
- the supports \(P,Q,\mathfrak n\) have intrinsic meanings;
- \(J,Q_0,Q_*\) may be constructed from invariant ideal sheaves;
- the frame morphism is smooth and faithfully flat;
- regular fibres introduce no new associated primes;
- alternatively, the result may be checked on standard Grassmannian charts.

This is plausible, and I do not claim it is false. But the word **complete** is being carried by this paragraph.

For a top-four proof I would require a dedicated global descent lemma that explicitly states and proves:

1. which ideal sheaves on \(X=\operatorname{Gr}(2,\mathfrak m)\) pull back to \(P,Q,\mathfrak n,J,Q_0,Q_*\);
2. the descended intersection equality;
3. irredundancy after descent;
4. the global set of associated points;
5. the precise canonical content of the decomposition when an embedded primary component itself is not canonical.

The current text says that \(Q_*\) is a specified primary representative rather than a canonical embedded primary component. That distinction matters. A "complete primary classification" should clearly separate canonical invariants of the scheme from one convenient noncanonical primary decomposition.

# 6. The conductor-kernel theorem is a genuine structural improvement

On the exact tangent-rank-one locus the manuscript introduces
\[
L=\operatorname{im}(K\to V),\qquad
H_0=K\cap S_2
\]
and proves that the subalgebra condition is exactly
\[
\gamma(\operatorname{Sym}^2L)\subset H_0.
\]

It then identifies
\[
\operatorname{cond}_B(W)
=
\ker\!\left[
K\to\operatorname{Hom}(V,S_2/H_0)
\right].
\]

This is the right mechanism: the conductor is not inferred merely from numerical rank, and the quadratic relation controls which embedded surfaces lie in the subalgebra boundary.

The square and two-factor cases are then read off correctly from the images of multiplication by the relevant factor lines.

This is the strongest conceptual part of v120.

The limitation is again breadth. Because \(\ker\gamma\) is a single binary quadratic, the geometry of factor lines is completely rigid. The manuscript does not yet tell us what replaces this mechanism when \(\ker\gamma\) is a higher-dimensional linear system of quadrics.

# 7. The collision family is useful but not a substitute for a moduli theorem

The family
\[
\mathcal B_\tau
=
\mathbf C[\tau,x,y]/((x,y)^3,y^2-\tau xy)
\]
is finite free of rank five. Its quadratic relation moves from a double factor at \(\tau=0\) to distinct factors for \(\tau\ne0\).

The stated Fitting ideal
\[
\delta^2\bigl(
a(a+\tau b),\,
2ac+\tau(ad+bc),\,
c(c+\tau d)
\bigr)
\]
is compatible with direct minor computation.

This is a good deformation connecting the two orbit types.

But the family does not create a new moduli problem: it simply interpolates the only two isomorphism types in the class. The paper is appropriately cautious not to assert flatness of the failure family or specialization of a chosen primary decomposition.

# 8. The sharpness theorem closes the old issue but is not itself a high-end novelty driver

For every \(r\ge1\) and \(k\ge2\), the construction
\[
B=
\mathbf C[z,\epsilon_1,\ldots,\epsilon_{k-2}]
/
(z^{r+2},z\epsilon_i,\epsilon_i\epsilon_j)
\]
with
\[
W=\operatorname{Span}(1,z,\epsilon_1,\ldots,\epsilon_{k-2})
\]
has
\[
W^r\ne W^{r+1}=B.
\]

The proof is immediate from the basis
\[
1,z,\ldots,z^j,\epsilon_1,\ldots,\epsilon_{k-2}
\]
of \(W^j\).

This correctly establishes optimality of the universal \(r+1\) bound.

The manuscript also correctly says that the field-level dimension argument is not claimed as new. The more interesting statement is the relative equality of image submodules over coefficient rings.

That distinction should remain central. The sharpness example is valuable closure, not a top-four centerpiece.

# 9. The relative proofs are now adequate in outline

The new relative-cohomology section materially improves the paper.

The finite locally free family gives locally free pushforwards for the restricted line bundles. Fibre regularity supplies the necessary \(H^1\)-vanishing. Surjectivity follows by Nakayama, the kernel is locally free because the quotient is locally free, and the locally split sequence survives arbitrary pullback.

The multiplication-kernel map is then a morphism of vector bundles whose coherent cokernel vanishes on every geometric fibre. This gives global surjectivity and preserves it under pullback.

I do not see a reason to carry the old E119.6 objection forward.

The authors should nevertheless cite the exact cohomology-and-base-change statements at the places where they are used. In a paper making arbitrary nonreduced base change part of the advertised result, every transition from fibre regularity to a global vector-bundle statement should be traceable to a precise theorem or a complete direct argument.

# 10. The source-bound build issue is closed

The previous referee found a genuine failure caused by a missing inherited verifier.

That criticism is obsolete for v120.

The current branch contains the inherited verifier, the canonical workflow completed successfully, and the build receipts bind the source commit, product commit, diagnostic digest and PDF hashes.

The repository correctly marks
proof certification = false
and
priority certification = false.

No further review round should use the old broken-build issue as a rejection reason unless the branch changes again.

# 11. The unresolved Ballico comparison remains a top-four blocker

The manuscript's own literature audit states that the complete theorem text of

E. Ballico, *On the Failure Locus of Higher Order Properties of Embeddings in Projective Spaces*, Math. Nachr. 163 (1993), 5–13,

was not obtained.

The audit therefore leaves the closest theorem-level comparison unverified.

That is the responsible scholarly position. It is also incompatible with a confident top-four originality claim.

The paper studies scheme-theoretic failure of multiplication/embedding behavior, including incomplete linear series, finite contacts, nonreduced structure, and global transport. A historical article whose title explicitly concerns failure loci of higher-order embedding properties is too close to leave at metadata level.

I make neither of the following claims:

- that Ballico anticipates v120;
- that Ballico does not anticipate v120.

The point is precisely that the current record does not establish either conclusion.

For a specialist submission, an editor may allow the comparison to be completed during revision. For a general top-four submission, I consider the missing comparison a threshold issue.

# 12. The central top-four problem is now mathematical scale, not mathematical closure

The v120 response can reasonably say that E119.2 and E119.3 were answered.

That does not mean the top-four significance objection has disappeared.

The new class theorem is still the smallest case in which the quadratic layer has nontrivial relation geometry:
\[
\dim V=2,\qquad
\dim S_2=2,\qquad
\dim\ker\gamma=1.
\]

The projective parameter controlling the relation is a single binary quadratic, and its orbit stratification is finite.

A general theory should reveal what survives when the relation space itself has geometry.

Examples of a materially stronger direction include:

- cube-zero algebras with fixed Hilbert function \((1,e,q)\) for \(e\ge3\);
- nets or higher-dimensional systems of quadrics;
- a theorem describing minimal and embedded associated primes in terms of determinantal/discriminantal strata of \(\ker\gamma\);
- a uniform conductor-primary theorem over a positive-dimensional moduli stratum;
- or an intrinsic classification of boundary components for a family in which factor geometry actually varies.

The present factorization theorem is exactly the piece from which such a theory ought to start.

At present the manuscript proves the first complete nontrivial case, not the general phenomenon.

# 13. "Complete primary decomposition in length five" overstates the scope

The theorem title should be changed.

Not every length-five complex local algebra has Hilbert function \((1,2,2)\). The theorem classifies the multiplication-failure primary structure for the length-five \((1,2,2)\) class.

The title should say so explicitly.

A suitable formulation would be:

**Complete primary decomposition for Hilbert function \((1,2,2)\)**

or

**Primary decomposition for the length-five \((1,2,2)\) class**.

The abstract should likewise prefer "unital three-planes" or an equivalent precise phrase over "three generators" when the parameter space is a Grassmannian of three-dimensional subspaces rather than an ordered generating triple.

# 14. The projective realization is correct but too close to transport

For the two punctual length-five schemes in \(\mathbf P^2\), the paper uses regularity three and the conductor transport theorem to realize the same Fitting schemes as genuine global section-multiplication failures for \(n\ge5\).

This is a valid application.

It does not yet demonstrate that the embedded primary structure controls a broad global geometric phenomenon. The global conclusion is essentially that the finite-algebra coherent cokernel is reproduced by global sections once the kernel-filling theorem applies.

For a top-four case, I would want one global result where the primary boundary geometry changes a geometric classification, a moduli boundary, a component structure, a normalization problem, an enumerative statement, or another phenomenon not already contained in the finite algebra after transport.

# 15. The full 111-page manuscript is not the correct journal object

The repository's build receipt records a 44-page geometry article, a 111-page complete manuscript, and a 28-page applications document.

The 44-page article has a coherent theorem chain:
\[
\text{relative stabilization}
\Longrightarrow
\text{codimension-two presentation}
\Longrightarrow
\text{conductor incidence}
\Longrightarrow
\text{primary boundary classification}
\Longrightarrow
\text{global transport}.
\]

The 111-page manuscript deliberately retains large amounts of historical polar, residual, wall, orientation, contact, higher-product and statistical material that the dependency map itself declares nonessential to the new core.

This is reasonable archival practice and poor submission architecture.

I would not ask the repository to delete old mathematics. I would ask the authors to stop treating preservation and journal exposition as the same objective.

Unless a future structural theorem reconnects those sections logically, the focused geometry article should be the submitted paper and the long complete manuscript should remain an archival companion.

# 16. The current A2 label is historical rather than logically demonstrated

The dependency map explicitly says:

- the present finite-algebra core has no unstated dependence on A1;
- no particular current A3–D1 manuscript has been verified as using the v120 results;
- the retained historical sections are not premises of the new core.

That is honest and mathematically harmless for a standalone paper.

It also means that the designation "A2" does not currently contribute to the paper's significance. The logical second step in a theory program has not been demonstrated at theorem level.

There are two clean choices.

Either present this as a self-contained algebraic-geometry/commutative-algebra article whose A2 label is merely repository history.

Or give an explicit theorem dependency:
\[
\text{named A1 theorem}
\Longrightarrow
\text{named A2 hypothesis/result}
\Longrightarrow
\text{named downstream theorem},
\]
with the hypotheses checked.

Anything in between is narrative rather than mathematical dependency.

# 17. Disposition of the previous mandatory items

| Previous item | v120 status | Referee-II assessment |
|---|---|---|
| E119.1 Ballico theorem-level comparison | Open | Still a top-four originality blocker |
| E119.2 boundary theorem along \(T\) | Closed for a complete natural class | Substantive mathematical progress |
| E119.3 conductor-to-primary beyond one \(B_h\) family | Closed at the requested next step | Now a class theorem, but the class remains rigid |
| E119.4 sharpness of \(r+1\) | Closed | Correct explicit family for all \(r,k\) |
| E119.5 reproducible source-bound build | Closed | Workflow green |
| E119.6 relative/base-change detail | Substantially closed | No old blocker remains |
| E119.7 pipeline dependency note | Closed as documentation | It now reveals the absence of a demonstrated chain dependency |

A future report should not recycle E119.2–E119.7 as unresolved defects.

# 18. Mandatory revisions from Referee II

## RII-120.1 — Complete the nearest-source comparison

Obtain the complete Ballico 1993 article through a lawful library or author-access route and prepare a theorem-by-theorem comparison covering:

- the definition and scheme structure of the failure locus;
- incomplete versus complete linear series;
- fixed versus moving finite contacts;
- multiplication maps versus higher-order embedding/osculating properties;
- quotient-algebra/Hilbert constructions;
- conductor or residual mechanisms;
- nonreduced and embedded-primary structure;
- and global degree/regularity assumptions.

The conclusion may be positive, negative, or mixed. What is not acceptable for the target venue is leaving the nearest source unread while making a global originality claim.

## RII-120.2 — Extend the primary mechanism to a positive-moduli class

The next theorem should not be another isolated length-five example.

Use the cube-zero factorization to prove a structural statement for a class in which the quadratic relation space has nontrivial moduli. The theorem should predict minimal/embedded associated primes, multiplicities, or conductor strata from intrinsic data of
\[
\gamma:\operatorname{Sym}^2V\to S_2
\]
or its kernel.

This is the main mathematical requirement for a renewed top-four case.

## RII-120.3 — State and prove the global descent theorem explicitly

Promote the frame-to-Grassmannian argument to a named lemma/proposition.

Specify the global ideal sheaves, their pullbacks, the intersection equality, irredundancy, associated points, and which embedded primary components are canonical or noncanonical.

Do not let the strongest global wording of the paper depend on an abbreviated descent paragraph.

## RII-120.4 — Produce one genuinely global consequence of the primary structure

Go beyond reproducing the finite Fitting scheme in global sections.

A strong response would derive a new component, degeneration, moduli, normalization, or positive-dimensional geometric theorem whose proof actually needs the embedded primary structure.

## RII-120.5 — Calibrate "complete" claims to the exact class

Rename the length-five theorem and revise the abstract so that every use of "complete" carries the qualifier Hilbert function \((1,2,2)\), unless a later theorem expands the class.

Also distinguish a Grassmannian of unital three-planes from an ordered triple of generators.

## RII-120.6 — Submit the focused article, not the archival accumulation

Treat the 44-page geometry paper as the primary journal object unless new mathematics makes the 111-page manuscript logically unified.

Preserve the longer source in the repository if desired; do not require a journal reader to reconstruct the paper's actual theorem chain from historical layers.

## RII-120.7 — Either prove the A2 pipeline role or de-emphasize it

Identify concrete theorem-level upstream and downstream dependencies, or present the article as standalone.

The repository label alone should not be used as evidence of importance.

# 19. What would change my assessment

I would reconsider a general top-four case if the next version had all of the following.

1. **Priority closure:** the nearest historical failure-locus theorem is actually compared.

2. **Structural enlargement:** the \((1,2,2)\) calculation appears as the smallest case of a theorem for a class with genuine moduli.

3. **Global consequence:** the new primary structure forces a theorem beyond finite-algebra transport.

4. **Intrinsic proof closure:** the global primary decomposition and associated points are proved directly on the Grassmannian, with canonical versus noncanonical data clearly separated.

5. **Editorial focus:** the principal manuscript presents one theorem chain rather than the entire history of the project.

More exact checks, more workflow receipts, or more isolated examples would not materially change this assessment.

# 20. Correctness assessment

Within the scope of this review I found no fatal counterexample to the following v120 claims:

- the quadratic-layer Fitting factorization under the stated cube-zero split hypotheses;
- exhaustion of the complex \((1,2,2)\) class by the square and two-factor types;
- the displayed square and two-factor minor ideals;
- the square primary decomposition and its power formula;
- the two-factor decomposition and associated-prime set;
- normality of the reduced determinant divisor;
- exact nilradical index four;
- the conductor-kernel formula on the exact rank-one locus;
- the stated placement of factor surfaces and the extreme-corank point;
- the quadratic-factor collision family;
- sharpness of the \(r+1\) stabilization bound for every \(r\) and prescribed \(k\ge2\);
- the expanded rank-two incidence-fibre functor;
- or the relative kernel-filling/base-change mechanism under the stated regularity hypotheses.

This is not proof certification. It means only that my recommendation is based on top-four originality, scale, proof presentation at the global descent step, and manuscript architecture rather than on a discovered contradiction.

# Final assessment

Revision 120 is the strongest A2 version I have examined in this lineage. It has crossed an important threshold: the paper now contains a coherent algebraic-geometric core and a real conductor-boundary theorem.

It has not crossed the threshold to a top-four general-journal paper.

The decisive gap is no longer "finish the computation." The decisive gap is "show the general phenomenon."

At present the manuscript gives a complete and elegant analysis of the first rigid nontrivial Loewy class, supported by a correct general block-minor factorization and a sound transport mechanism. That is substantial mathematics. It is not yet a broad structural theory of multiplication-failure primary geometry.

**Recommendation: reject in the present form for Annals/Inventiones/JAMS/Acta-level consideration; encourage a focused specialist submission after priority closure, or a substantially more general revision driven by RII-120.2 and RII-120.4.**
