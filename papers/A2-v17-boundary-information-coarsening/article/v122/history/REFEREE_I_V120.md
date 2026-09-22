# Independent harsh top-four referee report on A2 revision 120

**Manuscript:** *Conductor boundaries and primary structures in multiplication failure*  
**Author:** Qian Qi  
**Repository:** TrillionniumFoundation/theta-theory  
**Reviewed revision branch:** revision/a2-v120-loewy-boundary-primary-2026-09-22  
**Reviewed branch head:** 1a6cae5a90b16d28cbfde3cbbb438e14dd31f474  
**Mathematical-source commit:** cade6b80d8300a2338b43c491c4d4b6bc648f2e4  
**Published PDF/product commit:** 13100ff1c85f77aee0ad28b1cdd459f2efda563c  
**Controlling prior referee report:** b409ec5eb4dfbb75850d90bff69a78604d3a512b  
**This report branch:** review/a2-v120-independent-harsh-top4-2026-09-22  
**Date:** 22 September 2026

## Referee status and scope

This is an owner-requested, AI-assisted external-referee-style assessment. It was not commissioned by *Annals of Mathematics*, *Inventiones Mathematicae*, *Journal of the American Mathematical Society*, *Acta Mathematica*, or any other journal, and it should not be represented as a journal-issued report or editorial decision.

I reviewed the actual v120 mathematical source rather than a stale revision label. I read the new Hilbert-function-(1,2,2) primary-classification section, the conductor-boundary theorem, the quadratic-factor collision family, the codimension-sharpness result, the expanded relative incidence and base-change arguments, the response to the v119 Round-3 report, the dependency map, the literature audit, the build receipts, and the primary-article organization. I also independently recomputed several of the finite polynomial identities that carry the new theorem and checked the source-bound workflow state.

The assessment separates:

1. correctness of the new mathematics;
2. completeness and precision of the proofs;
3. originality and relation to the nearest literature;
4. breadth and conceptual force at a general top-four mathematics journal;
5. manuscript architecture and programmatic role;
6. reproducibility and provenance.

These are not interchangeable.

# Recommendation

## Reject in the present form at a general top-four mathematics journal.

This recommendation is **not** a repetition of the v119 report.

Revision 120 makes real progress and closes most of the concrete v119 objections. In particular, it now does what the previous report explicitly requested: it gives a complete primary classification along the conductor boundary for a natural full Hilbert-function class, proves sharpness of the stabilization bound, expands the relative proofs, and publishes a successful source-bound build. I do not regard E119.2--E119.6 as still open in their old form.

I also did **not** find a fatal counterexample to the new v120 headline theorems in this review.

The remaining negative top-four assessment has a different basis.

First, the nearest historical-source comparison is still unresolved at theorem level. The manuscript itself states that the complete Ballico 1993 text was not obtained and explicitly leaves E119.1 open. For a paper whose significance narrative is a new scheme-theoretic theory of failure loci for multiplication and embeddings, this is not a cosmetic bibliography item. It blocks a reliable top-four originality assessment.

Second, the new “complete” boundary theorem is complete because the chosen class is extremely rigid: over \(\mathbf C\), a local algebra with Hilbert function \((1,2,2)\) reduces to a surjection
\[
\gamma:\operatorname{Sym}^2\mathbf C^2\longrightarrow \mathbf C^2
\]
whose one-dimensional kernel is a binary quadratic, hence has only the square and two-distinct-factor types. The resulting primary geometry is elegant and nontrivial, but it remains a two-type length-five classification. The general cube-zero factorization preceding it is clean, yet it does not itself yield a structural primary theorem for higher embedding dimension, larger quadratic layer, or a varying kernel space. At a general top-four journal, the mathematical burden now shifts from “produce one full boundary classification” to “show that the mechanism scales into a genuinely general theory.”

Third, the global projective realization proves that the two length-five primary schemes occur in actual section-multiplication problems, but it is a transport theorem for zero-dimensional schemes. It does not convert the local classification into a comparably broad theorem about global failure loci on positive-dimensional varieties, nor into a global component/normalization theorem for a moving family of algebras. This is a legitimate application, but not yet a top-four-level amplification of the classification.

Fourth, the complete 111-page manuscript remains an accumulation of several historically distinct programs. The 44-page primary geometry article is much more coherent and is the edition I would regard as the serious journal object. The full manuscript, by the authors' own dependency map, retains polar, wall, residual, orientation, higher-product and statistical material that is not logically needed by the new finite-algebra core. Preservation is a valid repository policy; it is not a substitute for editorial concentration in a submitted article.

The result is now a substantial and potentially publishable algebraic-geometry/commutative-algebra paper. I do not yet see a demonstrated case for one of the four most selective general mathematics journals.

# 1. What v120 genuinely fixes

A harsh report should give the revision full credit where it has answered the previous referee.

## 1.1 E119.2 is materially answered: the boundary is now computed, not merely presented

The v119 report distinguished a presentation of the full codimension-two Fitting scheme from a classification of its geometry along the extreme-corank locus \(T\).

Revision 120 now supplies such a classification for every complex local algebra with Hilbert function \((1,2,2)\). The theorem gives explicit primary decompositions, all associated primes, embedded surfaces, the possible embedded point, generic multiplicity, nilradical index, the reduced normal divisor, and the position of conductor strata.

This is exactly the kind of boundary theorem the prior report requested.

## 1.2 E119.3 is answered in a natural complete class, not by another isolated example

The previous connected family
\[
B_h=\mathbf C[x,y]/(x^2,xy,y^h)
\]
showed embedded associated primes and unbounded nilpotent complexity but did not yield a general conductor-to-primary theorem.

Revision 120 replaces “one more example” by a complete theorem for a specified Hilbert-function class. That is a qualitative improvement.

The class is small, and I return to that issue below, but it is a class theorem.

## 1.3 E119.4 is closed: the stabilization bound is proved sharp

For every \(r\ge1\) and \(k\ge2\), the paper constructs
\[
B=\mathbf C[z,\epsilon_1,\ldots,\epsilon_{k-2}]
 /(z^{r+2},z\epsilon_i,\epsilon_i\epsilon_j)
\]
with
\[
W=\operatorname{Span}(1,z,\epsilon_1,\ldots,\epsilon_{k-2})
\]
and
\[
W^r\ne W^{r+1}=B.
\]

The basis calculation is immediate and correct. Thus the universal \(r+1\) bound is sharp simultaneously in every codimension and every prescribed generating rank at least two.

The manuscript also now correctly separates the elementary field-level length count from the genuinely relative coefficient-ring theorem.

## 1.4 E119.5 is closed as a delivery issue

The previous v119 review found that the canonical build failed because a required inherited verifier was absent.

That criticism no longer applies.

Workflow run 35738068605, “A2 v120 source-bound build and publish,” ran from mathematical-source commit cade6b80d8300a2338b43c491c4d4b6bc648f2e4 and completed successfully. The branch contains source/product receipts and the PDFs were published in commit 13100ff1c85f77aee0ad28b1cdd459f2efda563c.

The repository correctly says that this is reproducibility evidence, not proof or priority certification.

## 1.5 E119.6 is substantially closed

The rank-two incidence fibre is now proved by a full functor-of-points construction rather than the earlier phrase “check after trivializing.” The relative cohomology section also spells out the locally split restriction sequence, the vanishing of higher direct images in the required range, and the arbitrary-base-change argument.

I did not find a fatal defect in those additions.

## 1.6 E119.7 is closed as a documentation request

The dependency map now says exactly what is and is not logically used.

In particular, it candidly states that the finite-algebra/conductor-boundary core is self-contained, uses no unstated theorem from A1, and has not yet been verified as an invoked input of any specific A3--D1 manuscript.

That is the correct thing to say. It resolves the documentation issue, though it creates a separate programmatic question discussed below.

# 2. Audit of the new quadratic-layer factorization

The cleanest new structural statement is
\[
\mathcal I_D=(\det M)\,I_q(\gamma\operatorname{Sym}^2M)
\]
for a cube-zero augmentation ideal.

I find this theorem correct as stated in the split locally free setting.

## 2.1 The block-minor argument is sound

With
\[
B=\mathcal O\oplus V\oplus S_2,\qquad \mathfrak m^3=0,
\]
and a framed \(e\)-plane
\[
K\longrightarrow V\oplus S_2,\qquad
\begin{pmatrix}M\\H\end{pmatrix},
\]
the image of every symmetric power of degree at least two is
\[
\mathcal O\cdot1+K+K^2.
\]

The presentation matrix has the block form
\[
\begin{pmatrix}
1&0&0\\
0&M&0\\
0&H&\gamma\operatorname{Sym}^2M
\end{pmatrix}.
\]

Because the quadratic columns have no \(V\)-row entries, every nonzero maximal minor must take all \(e\) middle columns. Expansion therefore contributes \(\det M\), leaving a \(q\times q\) minor of the quadratic block. The \(H\)-variables do not produce extra maximal minors.

This is a genuine identity of ideals before taking radicals.

## 2.2 “Arbitrary base change” is acceptable here, but the exact hypothesis should remain visible

The theorem is strongest and cleanest for an augmented locally free algebra with locally free layers and \(S_2(V\oplus S_2)=0\). In that formulation the polynomial identity plainly survives coefficient substitution and base change.

The prose should not allow a reader to confuse this with an arbitrary family of Artin algebras in which the Loewy layers fail to be locally free or no compatible splitting is available. The manuscript mostly avoids that overstatement; retain this discipline.

# 3. Audit of the Hilbert-function-(1,2,2) classification

## 3.1 The reduction to two algebra types is correct

For a complex local algebra with Hilbert function \((1,2,2)\),
\[
\dim \mathfrak m/\mathfrak m^2=2,\qquad
\dim \mathfrak m^2=2,\qquad
\mathfrak m^3=0.
\]

The multiplication tensor is a surjection
\[
\gamma:\operatorname{Sym}^2V\to S_2,
\]
so its kernel is one-dimensional. A nonzero binary quadratic over \(\mathbf C\) is either a square or a product of two distinct linear factors.

Thus the two isomorphism types used in the paper are the right ones:
\[
B_{\rm sq}=\mathbf C[x,y]/((x,y)^3,y^2),
\qquad
B_{\rm tf}=\mathbf C[x,y]/((x,y)^3,xy).
\]

No hidden cubic extension coefficient remains because \(\mathfrak m^3=0\).

## 3.2 The explicit minors check out

On the frame cover
\[
M=\begin{pmatrix}a&c\\ b&d\end{pmatrix},
\qquad \delta=ad-bc,
\]
the paper writes
\[
L_{\rm sq}=
\begin{pmatrix}
a^2&2ac&c^2\\
ab&ad+bc&cd
\end{pmatrix},
\]
and
\[
L_{\rm tf}=
\begin{pmatrix}
a^2&2ac&c^2\\
b^2&2bd&d^2
\end{pmatrix}.
\]

I independently recomputed the \(2\times2\) minors. They are, up to units,
\[
\delta(a^2,ac,c^2)
\]
in the square case and
\[
\delta(ab,ad+bc,cd)
\]
in the two-factor case.

After the additional \(\det M=\delta\) factor from the linear layer, the stated full failure ideals
\[
I_{\rm sq}=\delta^2P^2,\qquad
I_{\rm tf}=\delta^2J
\]
follow.

This is not merely a numerical diagnostic: it is the correct algebraic reduction of the Fitting ideal.

# 4. Audit of the primary decompositions

I found no fatal error in the two displayed decompositions.

## 4.1 Square type

With \(P=(a,c)\), the manuscript claims
\[
\delta^2P^2=(\delta^2)\cap P^4.
\]

The \(P\)-adic order of \(\delta=ad-bc\) is one in the associated graded domain
\[
\mathbf C[b,d][a,c],
\]
so
\[
(P^t:\delta^u)=P^{\max(t-u,0)}.
\]

The intersection identity and its power version
\[
I_{\rm sq}^j=(\delta^{2j})\cap P^{4j}
\]
follow.

The embedded prime \(P\) is therefore real, not an artefact of taking a slice.

## 4.2 Two-factor type

Let
\[
J=(ab,ad+bc,cd),
\]
\[
Q_0=J+P^2+Q^2,\qquad P=(a,c),\quad Q=(b,d),
\]
and
\[
Q_*=\delta^2Q_0+\mathfrak n^7.
\]

The manuscript first proves
\[
J=P\cap Q\cap Q_0.
\]

I independently checked the key ideal equality by elimination/Groebner reduction. The triple intersection has the same Groebner basis as \(J\). I also checked
\[
\delta\notin J,\qquad \delta^2\in J,
\]
with
\[
\delta^2=(ad+bc)^2-4ab\,cd.
\]

These are the right identities for the subsequent embedded-prime analysis.

The displayed decomposition
\[
I_{\rm tf}
=(\delta^2)\cap P^3\cap Q^3\cap Q_*
\]
is compatible with the colon computations in the proof. The use of
\[
(Q_*:\delta^2)=Q_0
\]
and the \(\mathfrak n\)-primary nature of \(Q_*\) is coherent.

Within this review I found no counterexample to
\[
\operatorname{Ass}(R/I_{\rm tf})
=\{(\delta),P,Q,\mathfrak n\}.
\]

## 4.3 The nilradical index four is supported by the equations

In both cases
\[
I=\delta^2J',
\qquad
\delta\notin J',
\qquad
\delta^2\in J'.
\]

Hence
\[
\delta^4\in I,\qquad \delta^3\notin I,
\]
while the radical is \((\delta)\). The exact nilpotency index four is therefore justified.

## 4.4 The descent paragraph should be upgraded from a referee-comfort argument to a formal lemma

This is not a discovered counterexample, but the current proof becomes too compressed precisely where the theorem moves from an affine frame ring to a global statement on the Grassmannian.

The text says that:

- the decompositions survive polynomial extension and localization;
- the ideals \(P,Q\) have intrinsic descriptions;
- \(J\), \(Q_0\), and \(Q_*\) can be built from invariant ideal sheaves;
- the frame map is a smooth faithfully flat torsor with regular fibres;
- no new associated primes appear;
- alternatively, standard Grassmannian charts give the same equations.

For an ordinary paper this may be enough. For a theorem advertised as a **complete global primary classification**, it deserves a named descent lemma.

In particular, I recommend that the paper explicitly prove:

1. the global ideal sheaves corresponding to \(P,Q,\mathfrak n\);
2. the global equality of the displayed intersections after descent;
3. the irredundancy of the descended components;
4. the asserted associated-point set on \(X\), rather than only after pullback to the frame torsor.

The intrinsic descriptions strongly suggest the result is correct. The issue is proof completeness at the exact point carrying the word “complete.”

# 5. The conductor-boundary theorem is a real theorem, not decoration

The formula
\[
\operatorname{cond}_B(W)=
\ker\left(
K\to\operatorname{Hom}(V,S_2/H_0)
\right)
\]
on the exact rank-one locus is natural and useful.

The proof correctly exploits \(S_2\mathfrak m=0\). Closure of \(W\) is equivalent to
\[
\gamma(\operatorname{Sym}^2L)\subset H_0,
\]
and conductor membership of \(k\in K\) is equivalent to
\[
\gamma(\bar k,V)\subset H_0.
\]

The square and two-factor cases then identify the action-rank jumps on the embedded surfaces explicitly.

This is exactly the kind of mechanism the v119 report asked the authors to connect to primary structure.

The important limitation is scope: the theorem succeeds because the entire quadratic relation is one binary quadratic. It does not yet give a general rule that starts from a higher-dimensional kernel of
\[
\operatorname{Sym}^2V\to S_2
\]
and predicts the associated primes of the multiplication-failure scheme.

That next step is where I think the top-four-level mathematics would have to lie.

# 6. The collision family is correctly chosen and computed

The family
\[
\mathcal B_\tau=
\mathbf C[\tau,x,y]/((x,y)^3,y^2-\tau xy)
\]
is finite free of rank five, with basis
\[
1,x,y,x^2,xy.
\]

The paper claims the full failure ideal
\[
\delta^2
\bigl(
a(a+\tau b),
\,2ac+\tau(ad+bc),
\,c(c+\tau d)
\bigr).
\]

I independently recomputed the relevant minors and obtained exactly the stated three factors, each multiplied by \(\delta\), before the additional linear-layer \(\delta\).

Thus the \(\tau=0\) fibre is the square type and every nonzero fibre is the two-factor type.

The paper is also appropriately cautious: it does not assert flatness of the failure schemes or specialization-compatibility of a chosen embedded primary component.

# 7. Sharpness and algebra length

The sharpness proposition is correct and useful.

The authors have also improved the literature positioning by explicitly saying that the field-level dimension bound is classical and that the new content of the stabilization theorem is relative equality of submodules over a coefficient ring, with the corresponding Fitting-ideal stability.

This closes the main defect from v119.

However, a top-four submission still needs a sharper theorem-level comparison with the algebra-length literature, not merely bibliography. The paper need not prove that every earlier length result is irrelevant; it should say exactly which hypotheses and conclusions differ.

# 8. Relative cohomology and arbitrary base change

The expanded proof is materially better than v119.

For a finite locally free family \(q:\mathcal Z\to S\), the sheaf \(\mathcal O_{\mathcal Z}(t)\) is invertible over \(\mathcal Z\), hence its finite pushforward is locally free. The uniform fibre regularity bound gives the required \(H^1\)-vanishing, fibrewise surjectivity of
\[
p_*\mathcal O(t)\to q_*\mathcal O_{\mathcal Z}(t),
\]
and therefore global surjectivity by Nakayama. The kernel is locally free because the quotient is locally free, so the sequence locally splits.

The later fibrewise-surjective bundle map used to fill the multiplication kernel has finitely presented cokernel; vanishing on every geometric fibre forces the cokernel to vanish.

I found no fatal issue here.

The independent check of Sidman's regularity theorem also supports the use
\[
\operatorname{reg}(I^2)\le2\operatorname{reg}(I)
\]
for a zero-dimensional scheme: Theorem 1.8 bounds the regularity of a product when the corresponding schemes intersect in a finite set.

# 9. Reproducibility is no longer a negative point

This deserves an explicit correction to the record.

The v119 report criticized a real broken dependency. The v120 branch repaired it.

The source-bound workflow completed successfully, the receipts bind the mathematical source and product commits, and the three reading editions were produced.

I therefore do **not** carry E119.5 forward.

More diagnostics are not what this manuscript needs next.

# 10. First remaining top-four blocker: the nearest-source priority problem is still open

This is E119.1, and it remains the most serious nonmathematical blocker.

The source is:

E. Ballico, *On the Failure Locus of Higher Order Properties of Embeddings in Projective Spaces*, *Mathematische Nachrichten* 163 (1993), 5--13, DOI 10.1002/mana.19931630102.

The current audit correctly states that complete theorem text was not obtained. My own public-source check likewise recovered the bibliographic record and publisher page but not enough theorem text to perform the requested comparison.

Therefore the only responsible conclusion remains:

- I do not claim that Ballico anticipates v120.
- I do not certify that it does not.

That uncertainty is acceptable in an internal research pipeline. It is not acceptable as the final originality basis of a submission to a general top-four journal whose central narrative is a new theory of failure loci.

The paper should obtain the article through a library, author copy, interlibrary loan, or another lawful full-text source and compare it theorem by theorem.

No amount of additional computer verification can substitute for this.

# 11. Second top-four blocker: the new “complete” theorem is still mathematically small in moduli

The phrase “complete primary classification” is true at the stated Hilbert function.

The question is what this completeness means conceptually.

For Hilbert function \((1,2,2)\), the multiplication tensor is governed by a single point of
\[
\mathbf P(\operatorname{Sym}^2\mathbf C^2),
\]
modulo \(\operatorname{GL}_2\). There are only two nonzero orbit types relevant here: a double root and two distinct roots.

So the complete classification is, at its core, a complete analysis of two algebra types.

That is not a criticism of correctness. It is a criticism of **generality relative to the journal standard being targeted**.

The theorem would become much more compelling if the paper moved from the two-orbit binary-quadratic situation to a statement such as:

- arbitrary cube-zero local algebras with fixed \((e,q)\);
- embedding dimension three with a varying net of quadrics;
- a structural theorem expressing associated primes of the failure scheme through degeneracy strata of \(\gamma\);
- a theorem relating factorization type or the projective geometry of \(\ker\gamma\) to embedded primary components;
- or a natural class with positive-dimensional moduli in which the conductor-primary mechanism is uniform.

The current factorization theorem is the obvious gateway to such a result. At present, the paper stops just after passing through the first nontrivial gateway.

# 12. The title “Complete primary decomposition in length five” is too broad

This is a formal but important scope issue.

Not every length-five complex local algebra has Hilbert function \((1,2,2)\). The theorem is not a classification of multiplication-failure primary geometry for all length-five local algebras.

The surrounding text is accurate, but the theorem title “Complete primary decomposition in length five” can be read as claiming exactly that.

Rename it to something like:

**Complete primary decomposition for Hilbert function \((1,2,2)\)**

or

**Complete primary decomposition for the length-five \((1,2,2)\) class**.

At this level, theorem titles should carry their scope without relying on a preceding paragraph.

# 13. The projective realization is valid but does not yet create a broad global theorem

The two local algebras are realized by zero-dimensional schemes in \(\mathbf P^2\), and the regularity-controlled transport theorem carries their full Fitting schemes to section multiplication.

This is a legitimate and useful global realization.

But it should not be oversold.

The result does not classify failure loci on positive-dimensional varieties. It does not give a component theorem in a moduli space of zero-dimensional schemes. It does not show that the primary types control a broad global enumerative or birational phenomenon. It shows that the local schemes occur as genuine global section-multiplication failure.

For a specialist paper, that is enough.

For a top-four significance case, I would want the local primary classification to force a new global theorem whose content cannot be summarized as “the same finite-algebra Fitting ideal is transported under a regularity bound.”

# 14. Manuscript architecture: the primary article is plausible; the 111-page complete manuscript is not the right submission object

The repository now contains:

- a 44-page primary geometry article;
- a 111-page complete manuscript;
- a 28-page applications edition.

The primary article has a coherent chain:
\[
\text{stabilization}
\to
\text{codimension-two Fitting presentation}
\to
\text{conductor incidence}
\to
\text{primary boundary classification}
\to
\text{global transport}.
\]

That is a defensible article.

The complete manuscript, by contrast, intentionally preserves extensive polar, residual, wall, orientation, higher-product, contact and statistical material that the dependency map itself says is not prerequisite to the finite-algebra core.

Repository preservation and journal exposition are different objectives.

I would strongly advise treating the primary geometry article as the actual submission object and the complete manuscript as an archival or companion document unless a future theorem genuinely reconnects the two halves.

This is not a request to delete mathematics from the repository.

It is a request to decide what paper is actually being submitted.

# 15. The theta-theory pipeline label no longer supplies significance by itself

The dependency map is admirably candid:

- the current finite-algebra core uses no unstated A1 theorem;
- no specific current A3--D1 paper was verified as already invoking the v120 results;
- retained historical sections are not logical prerequisites.

As a standalone paper, this is fine.

As “A2” in a logically ordered theta-theory program, it means the position is presently nominal rather than demonstrated by theorem dependency.

The paper should not use the program label as part of its top-four significance case unless the project can show an actual theorem interface:

\[
\text{A1 theorem}
\Longrightarrow
\text{A2 hypothesis or construction}
\Longrightarrow
\text{A3 theorem}.
\]

Otherwise, submit the finite-algebra paper on its own merits.

# 16. What v120 should not do next

The repository has already accumulated many review/revision rounds. The next response should not be:

- another isolated primary example;
- more finite diagnostics;
- a larger table of exact substitutions;
- another build receipt;
- another restatement of the same \((1,2,2)\) classification;
- or another round of preserving every historical section inside the principal submission.

Those actions would increase volume without answering the remaining significance question.

# 17. Mandatory revisions arising from v120

## E120.1 — Close the Ballico 1993 comparison

Obtain the complete article and produce a theorem-level comparison covering at least:

- the definition of the failure locus;
- scheme structure versus reduced support/cycles;
- incomplete linear series;
- higher-order embedding or osculating conditions versus multiplication maps;
- moving versus fixed finite contacts;
- quotient-algebra or Hilbert-scheme constructions;
- conductor/residual mechanisms;
- nonreduced and embedded-primary structure;
- and degree/regularity hypotheses.

If the comparison reveals anticipation, revise the novelty claims accordingly. If it does not, say exactly why.

This is a documentary requirement, not a request to force a positive originality conclusion.

## E120.2 — Generalize the conductor-primary theorem to a class with genuine moduli

Use the quadratic-layer factorization as the starting point.

A top-four-level next theorem should explain primary structure for a class substantially larger than the two binary-quadratic orbit types. For example:

- higher embedding dimension;
- larger quadratic layer;
- varying nets/systems of quadrics;
- or another natural positive-moduli class.

The desired output is a structural rule relating algebraic data of \(\gamma\) or \(\ker\gamma\) to minimal/embedded associated primes, multiplicities, and conductor strata.

This is the main mathematical requirement.

## E120.3 — Turn the local classification into a stronger global consequence

The current zero-dimensional projective realization is correct but mainly transports the local Fitting scheme.

A stronger result could be:

- a family theorem over a moduli space of finite schemes;
- a component/normalization statement for a global failure locus;
- a degeneration theorem showing how primary strata control global boundary geometry;
- or a positive-dimensional geometric application in which the embedded primary structure has an observable consequence.

The goal is not “more applications”; it is one application whose theorem-level content demonstrates why the primary classification matters globally.

## E120.4 — Promote the frame-to-Grassmannian descent to an explicit lemma

Give a formal global proof of the descended primary decomposition and associated points.

Do not leave the most global part of the theorem resting on the sentence that regular fibres introduce no new associated primes plus an unexpanded “alternatively, standard charts” remark.

This is a proof-quality requirement, not an assertion that the current result is false.

## E120.5 — Calibrate titles and scope

At minimum:

- rename “Complete primary decomposition in length five” to specify Hilbert function \((1,2,2)\);
- keep the distinction among arbitrary finite algebras, cube-zero algebras, and the \((1,2,2)\) class visible in the abstract and theorem roadmap;
- avoid using “complete” without the class qualifier.

## E120.6 — Choose the actual journal manuscript

Use the coherent primary geometry article as the main submission unless a future result makes the historical full manuscript logically unified.

The complete 111-page archive may remain in the repository without being the principal journal object.

## E120.7 — Demonstrate or de-emphasize the A2 pipeline role

Either:

- identify a concrete A1 input and a concrete downstream theorem using the new A2 output, with hypotheses checked;

or

- present this as a self-contained algebraic-geometry paper and treat “A2” as repository history rather than part of the mathematical significance claim.

# 18. Disposition of the v119 mandatory items

| v119 item | v120 status | Current assessment |
|---|---|---|
| E119.1 Ballico theorem-level comparison | **Open** | Still a top-four originality blocker |
| E119.2 boundary theorem for the full scheme | **Closed in a natural complete class** | The \((1,2,2)\) primary theorem is a real answer |
| E119.3 generalize conductor-to-primary beyond \(B_h\) | **Closed at the requested next level** | Complete Hilbert-function class, though still small |
| E119.4 sharpness/status of \(r+1\) | **Closed mathematically** | Explicit sharp family for every \(r,k\) |
| E119.5 reproducible build | **Closed** | Source-bound workflow succeeded |
| E119.6 relative representability/base change | **Substantially closed** | Expanded functorial and cohomological proofs |
| E119.7 pipeline note | **Closed as documentation** | Dependency map is explicit and appropriately cautious |

A future referee should not recycle E119.2--E119.7 as though v120 did not exist.

# 19. Correctness assessment of the v120 delta

Within the scope of this review, I found no fatal counterexample to the new claims that:

- the full Fitting ideal factors as
  \[
  (\det M)I_q(\gamma\operatorname{Sym}^2M)
  \]
  for the stated cube-zero split setting;
- the two Hilbert-function-\((1,2,2)\) algebra types exhaust the complex case;
- the square and two-factor quadratic minors are the stated ideals;
- the square primary decomposition and its power formula hold;
- \(J=P\cap Q\cap Q_0\) in the two-factor case;
- the two-factor associated primes are \((\delta),P,Q,\mathfrak n\);
- the reduced support is the determinant divisor with the stated singular point;
- the nilradical has exact index four;
- the conductor-kernel formula holds on the exact rank-one locus;
- the factor lines locate the stated embedded surfaces;
- the \(\tau\)-family realizes the collision between the two types;
- the codimension stabilization bound is sharp for every \(r\) and \(k\ge2\);
- the expanded rank-two incidence-fibre functor is represented by \(\operatorname{Spec}C\);
- or the relative kernel-filling argument is compatible with arbitrary base change under the stated hypotheses.

This is not proof certification. It means my negative recommendation is not based on a discovered contradiction in the new mathematical core.

# 20. What would materially change the top-four assessment

A materially stronger case would have four ingredients.

1. **Priority closure.** The nearest historical source is actually read and compared.

2. **A structural primary theorem beyond binary quadratics.** The cube-zero factorization is turned into a theorem for a positive-moduli class.

3. **A consequence whose scale matches the structural theorem.** The local embedded-primary geometry drives a genuinely new global or moduli statement.

4. **A focused submission architecture.** The reader sees one main theorem chain rather than the entire history of the research program.

If those are achieved, the paper would no longer read as a very sophisticated complete calculation at the first nontrivial Loewy boundary. It would read as a general theory whose smallest case is the v120 classification.

# 21. Final recommendation

I recommend **rejection in the present form at a general top-four mathematics journal**.

This is a stronger manuscript than v119.

The new primary decomposition is not cosmetic. The conductor-boundary theorem is real. The sharpness theorem is real. The relative proof gap has been substantially repaired. The build is now green. The authors have responded to the previous referee in substance rather than by narrowing claims or hiding unresolved items.

The reason for rejection is therefore no longer lack of a full boundary theorem or lack of reproducibility.

The remaining issue is whether the mathematical advance is broad and historically established enough for the target venue.

At present:

- the nearest historical failure-locus source remains unread at theorem level;
- the complete new primary theorem is confined to the two isomorphism types of the \((1,2,2)\) class;
- the general cube-zero factorization has not yet been converted into a correspondingly general primary-geometry theorem;
- the global realization transports the local example rather than amplifying it into a broad global classification;
- and the full manuscript remains less focused than the primary geometry article.

I would take the 44-page primary geometry article seriously as a specialist-journal submission after priority closure and proof-polish.

For an Annals/Inventiones/JAMS/Acta-level resubmission, I would require E120.1--E120.4 in substance, especially the structural extension in E120.2. That is the point at which the work could plausibly cross from “complete and elegant first nontrivial classification” to “general theory.”
