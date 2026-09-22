# Independent harsh top-four referee report — A2 revision 128

**Manuscript:** *Universal determinant completion, effective Pieri multiplication, and intrinsic primary boundary laws in multiplication failure*  
**Author:** Qian Qi  
**Repository:** TrillionniumFoundation/theta-theory  
**Reviewed revision:** revision/a2-v128-effective-pieri-relative-primary-atlas-2026-09-23  
**Controlling previous report:** review/a2-v127-independent-harsh-top4-2026-09-23  
**Principal source:** papers/A2-v17-boundary-information-coarsening/article/v128/geometry.tex  
**Referee response reviewed:** papers/A2-v17-boundary-information-coarsening/article/v128/RESPONSE_TO_REFEREE_V127.md  
**Exact-computation source reviewed:** papers/A2-v17-boundary-information-coarsening/article/v128/checks/generic_boundary_atlas.py  
**Build receipt reviewed:** papers/A2-v17-boundary-information-coarsening/article/v128/evidence/BUILD_RECEIPT.json  
**Date:** 23 September 2026

## Status of this report

This is an owner-requested, AI-assisted independent external-referee-style report. It was not commissioned by *Annals of Mathematics*, *Inventiones Mathematicae*, *Journal of the American Mathematical Society*, *Acta Mathematica*, or any other journal, and it must not be represented as a journal-issued report.

I reviewed the v128 source, the response to the v127 report, the new theorem statements and proofs, the generic-slice script and its checked-in certificates, the source-bound build receipt, and the inherited theorem chain actually compiled by geometry.tex. I do not treat ISSUE_MATRIX.json, BUILD_RECEIPT.json, or a response label such as “resolved” as mathematical evidence; they are provenance and workflow records only.

# Recommendation

## Reject in the present form at a general top-four mathematics journal.

Revision 128 is a real improvement over revision 127. The universal symmetric-power determinant-completion theorem is clean and correct in the form stated; the mixed-kernel genericity argument is now genuinely based on rational-function-field calculations rather than on isolated witnesses; the manuscript has a native introduction; and the corank-four proof has moved from bare representation occurrence toward actual multiplication in the matrix coordinate ring.

Nevertheless, I do not think the v127 correctness objections have all been closed. The most serious remaining problem is the proof of base change for the residual colons. The argument currently flattens only the cokernel \(C_j\) and then claims that this makes kernel formation commute with base change. That implication is false in general, and a one-line counterexample exists. Since the finite intrinsic primary-signature refinement is built on that base-change step, a central theorem of v128 is not proved as written.

There are two additional proof-completeness problems. First, the corank-four Pieri repair still omits the invariant-ideal/projection step needed to pass from a product with nonzero \((4,4,4,4)\)-projection to membership of the entire determinant line in the ideal; the theorem is very likely correct, but the written proof is not yet formally closed. Second, the generic pure-block primary table identifies ruling supports for two nontrivial slice families by factoring only the integral base point. The rational-function-field computation certifies the Hilbert functions, but the checked-in script does not certify the generic ruling factor on those two slices. This is repairable, and in fact the same exact setup appears to give the required generic factors, but that calculation needs to be written into the proof and evidence.

Even after those corrections, the higher-corank geometry is still mostly a depth theorem plus an existence-of-finite-stratification theorem rather than an explicit primary classification, and the inverse/moduli consequence has not advanced beyond the inherited polarized-K3 reconstruction. The universal determinant identity is valuable but elementary enough that, by itself, it does not yet supply the conceptual consequence I would expect from a general top-four paper of this length and scope.

# 1. What revision 128 genuinely fixes

A harsh report should separate real progress from unresolved claims.

## 1.1 The universal determinant-completion theorem is a genuine theorem and is proved cleanly

Theorem “Universal symmetric-power determinant completion” states that if
\[
\gamma:\operatorname{Sym}^r V\twoheadrightarrow S,
\qquad
J_{\gamma,r}=I_{\dim S}(\gamma\operatorname{Sym}^r M),
\]
for the generic endomorphism \(M\) of an \(e\)-dimensional space, then
\[
(\det M)^{\binom{e+r-1}{r-1}}\in J_{\gamma,r}.
\]

The proof is exactly the right one. Choose a complementary quotient \(\rho\) so that
\[
G=(\gamma,\rho):\operatorname{Sym}^rV\longrightarrow S\oplus K
\]
is an isomorphism. Then
\[
\det(G\operatorname{Sym}^rM)
=
\det(G)(\det M)^{\binom{e+r-1}{r-1}},
\]
and Laplace expansion along the \(\dim S\) rows belonging to \(\gamma\) puts every summand in the maximal-minor ideal of \(\gamma\operatorname{Sym}^rM\). The square case gives sharpness in the stated universal class.

This is conceptually cleaner than treating \(d^5\in J\) as an isolated identity for the \((1,4,6)\) model.

I find no correctness issue here.

## 1.2 The mixed-kernel genericity objection from v127 is substantially resolved

Theorem “Generic slice certification for the mixed-kernel atlas” is the right kind of repair to E127.2.

For the secant, tangent, and \(H\)-ruling rows, the paper now:

1. computes the infinitesimal stabilizer action on the nine-dimensional quadratic-block space;
2. adjoins explicit transverse coordinate directions whose differential completes the tangent rank to nine;
3. computes successive residual colons over \(\mathbf Q(s_i)\), not only at an integer point;
4. records the generic initial ideals and the denominator divisors on which they can change.

For the four rows with open stabilizer orbit in the quadratic-block space, the integral calculation is legitimately generic because the orbit itself is open.

This is a substantial mathematical improvement over the v127 witness argument.

## 1.3 The corank-three rank-drop passage is now conceptually organized

Lemma “Functorial symbol containment under mixed-rank drop” is a useful repair to M127.1. Writing the residual symbols as images of natural alternating maps and observing that lowering mixed rank factors through a quotient of the source is the right mechanism for showing that a missing right-\(GL(W)\) constituent cannot be created by rank degeneration.

The later Littlewood–Richardson exclusion of \((3,3,3)\) is therefore no longer resting on a vague semicontinuity sentence.

I would still welcome a slightly more explicit statement of the group action used on the coordinate ring, but I no longer regard the old v127 complaint as a decisive issue.

## 1.4 The manuscript architecture is improved

Revision 128 has a new abstract, introduction, and theorem hierarchy. It no longer asks the reader to interpret a v125 introduction as if it described the current theorem package.

The principal driver still imports inherited proof files from v123, v125, and v126, which I discuss below as a source-architecture issue, but the mathematical narrative is now much more coherent.

# 2. Decisive correctness issue E128.1 — colon formation is not shown to commute with base change

This is the most important issue in the present revision.

Proposition “Finite intrinsic primary-signature refinement” asserts, after a finite locally closed refinement, that every residual colon
\[
K_j=(J:d^{j-1})
\]
commutes with base change.

The proof introduces
\[
0\longrightarrow K_j\longrightarrow P_S
\xrightarrow{\ d^{j-1}\ }
P_S/J
\longrightarrow C_j\longrightarrow 0,
\]
with
\[
C_j=P_S/(J,d^{j-1}),
\]
then says:

> By generic flatness … every \(C_j\) is flat over the base. Tensoring the exact sequence with a residue field is then left exact at \(P_S\): \(\operatorname{Tor}_1^S(C_j,k(s))=0\). Hence \((K_j)_s=(J_s:d_s^{j-1})\).

That inference is not valid.

A four-term exact sequence cannot be treated as though vanishing of \(\operatorname{Tor}_1\) of the final cokernel automatically preserves the kernel of the original map.

A minimal counterexample is already enough:

- let the base be \(R=k[t]\);
- take the map
  \[
  R\longrightarrow R/(t)
  \]
  given by the quotient;
- its cokernel is \(0\), hence flat over \(R\);
- its kernel is \((t)\).

After base change to \(k=R/(t)\),
\[
(t)\otimes_R k\cong k,
\]
but the base-changed map
\[
k\longrightarrow k
\]
is the identity and has zero kernel.

Thus “cokernel flat” does not imply “kernel commutes with base change,” even with a flat free source.

The same homological issue is present in the manuscript’s sequence.

### Required repair

One clean repair is to split the four-term sequence into
\[
0\to K_j\to P_S\to I_j\to0,
\qquad
0\to I_j\to P_S/J\to C_j\to0,
\]
and refine the base so that enough of these modules are flat.

For example, if both \(P_S/J\) and \(C_j\) are flat over the stratum, then \(I_j\) is flat. Since \(P_S\) is flat, the first short exact sequence then remains exact after arbitrary base change, and the desired equality of the fibre kernel with the fibre colon follows.

Equivalent repairs are possible by flattening the two-term complex or by directly flattening the image module.

But some additional flatness input is necessary.

Until this is fixed, the first clause of Proposition \(\ref{prop:associated-prime-refinement}\) is unproved, and all later claims that depend on fibrewise identification of the colon layers do not yet follow.

This is not an editorial nicety. It is a correctness issue in the central family theorem of v128.

# 3. Decisive proof-completeness issue E128.2 — the relative-assassin refinement still needs a precise constructibility theorem

Suppose E128.1 is repaired so that the fibre modules really are the intended colon quotients.

The rest of the proof of Proposition \(\ref{prop:associated-prime-refinement}\) is plausible in strategy, but it remains too compressed for the strength of the conclusion.

The paper cites:

- Stacks Project, Tag 05AS, for the relative assassin;
- Tags 0GSF/0GSJ, for flat modules and persistence of relative associated points;
- Tag 05L2, for specialization in the purity discussion.

These are relevant references. In particular, Tag 0GSJ gives a useful statement about generic points of fibres of the closure of an existing relative associated point under flatness, and Tag 05L2 gives a specialization result.

However, the proof then uses the additional assertion

> The locus on which an additional fibrewise associated point occurs is constructible.

That assertion is exactly one of the nontrivial steps needed to make the Noetherian-induction argument finite. It is not proved in the manuscript, and it is not supplied merely by citing the definition of relative assassin or the persistence lemma.

There is a much closer Stacks reference available: the relative-assassin constructibility results in Section 37.25, for example Lemma 37.25.5, Tag 05KR, control constructible loci defined by containment of fibrewise associated points in a prescribed open set.

### Required repair

The paper should formulate a precise finite-stratification lemma with hypotheses matching its situation—finite presentation, Noetherian base, flatness of the relevant module—and derive the claimed finite list of fibrewise associated supports from an explicit constructibility result such as Section 37.25.

It should also be explicit about geometric fibres. If a closure \(Z_{j,\nu}\) acquires geometrically reducible fibres, the theorem should explain how the geometric generic points are tracked and how the refinement fixes the data that are claimed constant.

Likewise, the last paragraph on “generic length” is plausible, but the finite filtration and generic-freeness step should be stated at the actual localizations used in the theorem rather than summarized in one sentence.

I do not currently see a counterexample to the desired finite stratification. My objection is that the proof as written is shorter than the theorem it claims to prove.

Because E128.1 already breaks the base-change identification, E128.2 is logically downstream; both should be repaired together.

# 4. Decisive proof-completeness issue E128.3 — two generic rank-drop primary supports are inferred from special base points

Theorem “Generic primary signatures for every \(A_H\)-rank-drop type” is one of the central new claims of v128.

The rational-function-field calculations in checks/generic_boundary_atlas.py do certify the generic Hilbert functions on the chosen transverse slices.

But the geometric support identification in the proof is made differently. The text says:

> To identify the positive-dimensional supports, pull the layer ideals back to the rank-one parametrization \(T=uv^t\). At integral base points the common binary factors are …

and then lists the factors that produce the ruling divisors.

For rank types whose quadratic-block orbit is already open, this is harmless: the base point lies in an open orbit and the support type is transported by the stabilizer.

The problem occurs for the rows with genuinely nontrivial transverse slices, most notably
\[
(a,b)=(2,2)
\quad\text{and}\quad
(a,b)=(1,3).
\]

In these cases a factorization at one integral point does not, by itself, prove the generic support type along the rational-function-field slice. Constant Hilbert function is not enough: distinct reduced ruling lines, colliding ruling lines, and a nonreduced divisor can share the same Hilbert polynomial in suitable families.

The committed script reflects this distinction. Its rational-function-field routine certifies the Hilbert data, but the function rank_one_binary_factors later resets to the numerical \(C\)-matrices and extracts the common factor only over \(\mathbf Q\).

Thus the checked-in computational evidence does not actually certify the generic ruling factor for the nontrivial slices.

### The encouraging part

This looks immediately repairable rather than false.

Running the same exact algebra over the slice field gives, for the one-parameter \((2,2)\) slice, a common rank-one factor which is, up to a nonzero scalar,
\[
u_0u_1\Bigl(
(s+9)u_0^2+(3s+6)u_0u_1-7u_1^2
\Bigr).
\]
The quadratic discriminant is
\[
9s^2+64s+288,
\]
which is not the zero polynomial. Hence the generic fibre indeed consists of four distinct ruling lines.

For the \((1,3)\) slice, the corresponding generic factor remains, up to scalar,
\[
10u_0^2+u_0u_1-4u_1^2,
\]
whose discriminant is \(161\neq0\). Thus the generic two-line support is likewise plausible.

These are precisely the calculations that should appear in the manuscript and in the certificate.

### Required repair

Replace “at integral base points” by an actual factor calculation over the same rational-function fields used for the generic Gröbner bases, and record the discriminant/noncollision divisor.

Then compute the saturation quotient over that generic field when an embedded vertex module is claimed.

Once this is done, I expect the generic rank-drop primary table to become much more convincing.

# 5. Major proof issue M128.1 — the corank-four \(d^4\in J\) argument still skips the invariant-projection step

Revision 128 correctly identifies the weakness in v127: abstract occurrence of
\[
\mathbb S_{(4,4,4,0)}
\]
and
\[
\operatorname{Sym}^4V
\]
does not by itself prove that actual coordinate-ring multiplication reaches the determinant line.

Lemma “Effective Cauchy–Pieri multiplication in the matrix ring” is therefore the right repair. It invokes standard bideterminants and says that straightening the product of a \(\lambda=(4,4,4,0)\) bideterminant with a row-shaped \(\mu=(4)\) bideterminant contains the \(\nu=(4,4,4,4)\) bideterminant with coefficient one.

This is substantially better than v127.

However, the final theorem still makes one unspoken step.

The proof produces an element of the ideal \(J_{16}\) whose \(\nu\)-projection is nonzero and then concludes:

> The product belongs to the ideal \(J\), so its nonzero \(\nu\)-projection shows that this line meets \(J\) nontrivially. Hence the generator itself belongs to the ideal.

For that implication one must know that the relevant degree piece \(J_{16}\) is stable under the group whose semisimple decomposition is being used, so that the projection onto the irreducible \(\nu\)-summand stays inside \(J_{16}\).

This stability is expected: right multiplication \(T\mapsto Tg\) acts through \(\operatorname{Sym}^2g\) on the source columns, and the maximal-minor ideal is stable. Over characteristic zero the degree piece is completely reducible. Since the \((4,4,4,4)\) right type is one-dimensional, a nonzero intersection then indeed contains the entire determinant line.

But this argument should be stated.

There is a second presentation issue in the Pieri lemma itself. “Multiply a standard \(\lambda\)-bideterminant by the row-shaped \(\mu\)-bideterminant which fills the fourth row” is plausible to a specialist, but for the central repair to the previous referee objection I would prefer one explicit choice of bitableaux/highest-weight vectors and the one-line straightening identity showing the coefficient is nonzero.

The current script does not independently check this structure constant; its “effective_pieri_horizontal_four_strip” test only checks that \(\nu/\lambda\) is a horizontal four-strip. That checks the Littlewood–Richardson combinatorics, not the actual coordinate-ring multiplication coefficient.

### Required repair

Add:

1. a lemma stating the right \(GL(V)\)-stability of each \(J_m\);
2. the complete-reducibility/projection argument;
3. an explicit bideterminant or highest-weight product with nonzero \(\nu\)-coefficient.

I regard this as a repairable proof-completeness issue rather than evidence that \(d^4\in J\) is false.

# 6. Structural issue S128.1 — higher corank is still depth plus abstract finite stratification, not an explicit primary atlas

Revision 128 now handles the wording more honestly than revision 127.

At projection corank two, the paper gives genuinely geometric generic primary signatures.

At projection corank three, however, the explicit theorem remains
\[
d^3\notin J,\qquad d^5\in J,
\]
with the binary choice \(d^4\in J\) determining depth five versus six.

At projection corank four, the explicit theorem is
\[
d^3\notin J,\qquad d^4\in J,
\]
hence exact depth five.

The general primary-signature proposition says that after finite refinement the fibrewise associated supports, generic lengths, and multiplication ranks become constant. That is an existence/constructibility theorem. It does not identify those supports geometrically on the generic corank-three and corank-four strata.

Thus E127.4 is improved but not fully closed in the sense in which the previous report posed it.

For a paper advertising “intrinsic primary boundary laws,” the natural remaining theorem would identify at least the generic \(W_j\) supports and associated primes at corank three and four, not merely prove that some finite stratification exists on which they are constant.

I would accept a narrower paper that explicitly declares the higher-corank result to be a depth theorem. I would also accept a broader paper that computes the higher-corank generic primary signatures. The present text sits between these two positions.

# 7. Structural issue S128.2 — the specialization theorem still stops before the higher-corank boundary

The explicit corank-two orbit-closure families are useful.

The manuscript now realizes:

- off-Segre point to on-Segre point;
- secant line to tangent line;
- secant line to either ruling;
- tangent line to dual-rank-two;
- either ruling to dual-rank-one;
- either rank-one type to the zero mixed map.

It also gives one \(A_H\)-injective to \(A_H\)-rank-drop family.

These are real specialization laws and should be kept.

But the v127 report also asked for the higher-rank adjacency:
\[
\text{projection corank }2
\rightsquigarrow
3
\rightsquigarrow
4.
\]
Revision 128 still does not track \(W_j\), associated supports, or multiplicities across those degenerations.

This matters because the strongest geometric discontinuities may occur precisely when the size of the Schur complement changes.

I therefore regard E127.5 as substantially advanced, not closed globally.

# 8. Structural issue S128.3 — the inverse problem remains unchanged

The inherited polarized reconstruction theorem remains, in my view, the conceptual center of the paper:

the abstract nonreduced failure scheme determines the polarized quartic K3 surface.

That is strong.

But v128 still does not prove that the deeper primary signature distinguishes two members of the finite Torelli packet, reduces the generic degree of the inverse map, determines the web, or determines the Reye/Enriques datum.

The response candidly acknowledges this and chooses the alternative route of broadening the determinant theorem.

That is mathematically legitimate. It does not, however, mean that the inverse side has advanced.

The introduction should continue to distinguish clearly between:

- reconstruction of the polarized K3;
- additional intrinsic boundary invariants;
- and actual reconstruction of the original multiplication tensor.

Those are not the same theorem.

# 9. Top-four significance issue S128.4 — the universal theorem is broad, but its present consequence is not yet commensurate with the venue claim

The new theorem
\[
(\det M)^{\binom{e+r-1}{r-1}}
\in I_{\dim S}(\gamma\operatorname{Sym}^r M)
\]
is elegant and general.

But its proof is one Laplace-completion argument once the complementary quotient is chosen.

That is not a criticism of the theorem’s correctness; simple proofs of broad facts can be excellent mathematics.

The editorial issue is what the theorem does for the rest of this manuscript.

At present, the general theorem gives a universal nilpotence bound after specialization to the \((1,4,6)\) model. Most of the detailed geometry remains specific to that model and is established by a long finite atlas of colon computations. The higher-corank primary geometry is not explicitly classified, and the inverse/moduli map is not sharpened.

For a specialist algebraic-geometry or determinantal-geometry journal, the current package could become quite compelling after the correctness repairs.

For a general top-four journal, I would still want one further conceptual consequence, for example:

- a sharp determinant exponent for a genuinely broad class of non-isomorphic quotients \(\gamma\), not only sharpness in the square-isomorphism extreme;
- a general theorem identifying the nilpotent Fitting layers with ramification or discriminant data beyond the \((1,4,6)\) case;
- a higher-corank primary classification with a uniform representation-theoretic mechanism;
- or a theorem showing that the deeper nilpotent boundary strictly improves the inverse problem.

At present the universal determinant theorem broadens the algebra, but the paper’s deepest geometric consequence is still inherited from the specialized quartic-K3 reconstruction.

# 10. Computational evidence: useful, but the receipt overstates what is actually certified

The computational posture is much better than in early revisions, and the exact rational-function-field calculations are appropriate evidence for finite algebra.

The script checks:

- stabilizer tangent ranks;
- transverse slice completion;
- residual colons over rational function fields;
- first determinant powers;
- Hilbert functions and leading monomials;
- selected rank-one factors at numerical base points.

That is valuable.

However, several Boolean fields in BUILD_RECEIPT.json should not be read as theorem certification.

In particular:

- effective_pieri_proof=true is a source-presence/build check; the script only verifies the horizontal-four-strip combinatorics;
- relative_assassin_proof=true is likewise a source check, and cannot detect the base-change error in E128.1;
- rankdrop_primary_table=true does not mean the generic ruling supports on the nontrivial slices were computed over the rational function field.

I recommend that future evidence receipts distinguish:

- source present;
- script executed;
- exact algebraic identity checked;
- theorem depends on structural proof only.

The manuscript itself mostly respects this distinction, but the evidence labels are easy to overread.

# 11. Source architecture issue M128.2 — the “native v128 article” is still assembled from several historical versions

The introduction is native v128, which closes the main expository objection from v127.

But geometry.tex still compiles the final article by importing files from:

- v123;
- v125;
- v126;
- and v128.

This is excellent for provenance but not ideal as a final journal source package.

A referee can follow it because the repository preserves all versions. An editor or production system receiving only the final article tree would have a more fragile dependency graph.

For a final submission I would either:

- materialize a self-contained v128 source tree with the inherited files copied byte-for-byte and a provenance manifest recording their origin; or
- provide a generated, immutable submission tree that resolves every historical include.

This is not a mathematical objection.

# 12. Documentary issue M128.3 — Ballico 1993 remains unresolved, although the paper handles it responsibly

The manuscript continues to state that the complete 1993 Ballico article has not been checked against the current theorem package.

That is the correct scholarly posture.

I do not treat this as a correctness objection because no current theorem depends on an unverified historical nonanticipation claim.

But before making any strong priority claim in a top-four submission, the full paper should be read theorem by theorem and the comparison recorded precisely.

# 13. Minor presentation issues

A few points should be corrected in any next version.

1. In the introduction’s Boundary structure theorem, item 6 currently contains
   \[
   d^3\notin J,qquad d^4\in J.
   \]
   The missing backslash before qquad is an obvious source typo.

2. The phrase “the unique \((4,4,4,4)\)-line” should specify the relevant left/right Cauchy action when first used. In the full matrix coordinate ring the Cauchy summand is naturally a tensor of left and right Schur factors; the one-dimensional conclusion follows because both factors are determinant powers.

3. When the paper says a finite primary-signature refinement is “intrinsic,” it should continue to distinguish the intrinsic fibrewise output from the noncanonical finite stratification used to make it locally constant. The present wording is mostly careful, but a few sentences still invite the stronger reading.

# 14. Status of the v127 issues after v128

My assessment is as follows.

## E127.1 — corank-four \(d^4\in J\)

**Substantially repaired, but not formally closed.**

The paper now uses actual Cauchy–Pieri multiplication rather than representation occurrence alone. Add the invariant-ideal projection step and an explicit bideterminant/highest-weight product.

## E127.2 — genericity of the nine mixed-kernel rows

**Closed for the mixed-kernel table.**

The transverse-slice and rational-function-field Gröbner argument is the correct repair.

## E127.3 — associated-prime refinement and colon base change

**Not closed.**

The key kernel/base-change inference is false as stated. After fixing that, the finite associated-point stratification needs a precise constructibility theorem.

## E127.4 — geometric graded data beyond depth

**Closed generically at corank two; still open geometrically at higher corank.**

The corank-two mixed and pure-block tables are a major improvement, subject to E128.3 for two slice families. Corank three and four remain primarily depth statements.

## E127.5 — actual specialization laws

**Substantially advanced at corank two; open across the higher-corank boundary.**

## E127.6 — broader theorem

**Closed in a meaningful sense.**

The universal symmetric-power determinant-completion theorem is genuinely broader than the \((1,4,6)\) case.

## E127.7 — integrated article

**Largely closed at the narrative level.**

The source tree is still historically assembled, but the article now has a native v128 front end and theorem hierarchy.

## E127.8 / documentary boundary

**Still open by design.**

Ballico 1993 remains unavailable in the verified corpus; the cautious wording is appropriate.

## M127.1 — corank-three rank drops

**Substantially closed.**

The functorial-symbol lemma supplies the missing mechanism.

## M127.2 — intrinsic versus presentation atlas

**Closed conceptually.**

The distinction is now explicit.

## M127.3 — inverse problem

**Not closed, and the authors no longer claim otherwise.**

## M127.4 — architecture

**Substantially improved.**

## M127.5 — significance breadth

**Improved, not fully resolved for a general top-four venue.**

# 15. What I would require before another top-four review

The next revision should prioritize proof closure over adding another layer of terminology.

## E128.1 — repair colon base change

Flatten enough of the two-term complex to make
\[
(J:d^{j-1})\otimes k(s)
=
(J_s:d_s^{j-1})
\]
a theorem, not an inference from flatness of the final cokernel alone.

Then re-run the relative-assassin argument on the genuinely identified fibre modules.

## E128.2 — prove the finite associated-point stratification with an exact reference

Use an appropriate constructibility theorem for relative associated points, such as the results in Stacks Section 37.25, and spell out the passage to geometric fibres, embedded/minimal status, incidence, and generic length.

## E128.3 — certify the generic ruling factors on the rank-drop slices

Compute the rank-one common factors over the same rational-function fields as the Gröbner bases, record their discriminants, and compute the generic saturation quotient when an embedded vertex is claimed.

The \((2,2)\) and \((1,3)\) rows are the important ones.

## E128.4 — finish the corank-four ideal-membership proof formally

State the group stability of \(J_m\), the semisimple projection argument, and one explicit nonzero bideterminant/highest-weight multiplication.

## E128.5 — decide how much higher-corank geometry the paper wants to claim

Either compute generic primary signatures at corank three and four, or narrow the global “boundary atlas / primary boundary laws” language so that the explicit classification claim is visibly corank-two and the higher-corank theorem is visibly a depth theorem.

## E128.6 — add one genuinely global consequence

For a renewed general top-four submission, I would look for a consequence that connects the universal determinant theorem and the specialized boundary geometry, or a theorem showing that the deeper intrinsic layers improve the inverse problem.

# 16. Final assessment

Revision 128 is stronger than revision 127 in exactly the directions a serious referee requested.

The universal determinant-completion theorem is a real conceptual generalization. The mixed-kernel genericity proof has been upgraded from isolated witnesses to rational-function-field geometry. The corank-two primary tables are now much closer to a genuine atlas. The corank-four argument is aimed at the correct multiplication map. The article is substantially better organized.

I therefore do not repeat the earlier criticism that the project is merely a formal Rees-algebra packaging of uncomputed data.

But the central relative-family theorem still contains a false homological inference: flatness of the final cokernel does not, by itself, make the colon kernel commute with base change. Because the associated-prime refinement and its claimed intrinsic family interpretation depend on that step, the manuscript cannot be accepted as written.

There are also two smaller but genuine proof-completeness gaps: the generic ruling factors for nontrivial pure-block slices are proved only at integral base points in the text/evidence, and the corank-four Pieri argument omits the invariant-ideal projection step.

My overall view is therefore:

> **Revision 128 has converted most of the v127 objections into repairable, sharply localized proof obligations, but one of those obligations—base change for the colon tower—still breaks a central theorem as currently written. The paper is mathematically substantial, but it is not yet at the correctness and conceptual-consequence threshold of a general top-four journal.**

**Recommendation: reject in the present form at a general top-four mathematics journal. A further revision is worth reviewing if it first repairs the colon/base-change theorem, makes the relative-associated-point stratification fully precise, certifies the generic pure-block support factors over the slice fields, and formally closes the corank-four ideal-membership argument.**
