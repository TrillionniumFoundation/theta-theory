# Independent harsh top-four referee report — A2 revision 130

**Manuscript:** *Universal determinant completion, effective Pieri multiplication, and intrinsic primary boundary laws in multiplication failure*  
**Author:** Qian Qi  
**Repository:** TrillionniumFoundation/theta-theory  
**Reviewed revision:** revision/a2-v130-referee-closure-global-primary-2026-09-23  
**Reviewed head:** 472200a5373ce2adc6dacf8d211f02d765ff62f2  
**Controlling previous report:** review/a2-v128-independent-harsh-top4-2026-09-23  
**Principal referee-facing source tree:** papers/A2-v17-boundary-information-coarsening/article/v129/  
**Referee response reviewed:** papers/A2-v17-boundary-information-coarsening/article/v129/RESPONSE_TO_REFEREE_V128.md  
**Build receipt reviewed:** papers/A2-v17-boundary-information-coarsening/article/v129/evidence/BUILD_RECEIPT.json  
**Date:** 23 September 2026

## Status of this report

This is an owner-requested, AI-assisted independent external-referee-style report. It was not commissioned by *Annals of Mathematics*, *Inventiones Mathematicae*, *Journal of the American Mathematical Society*, *Acta Mathematica*, or any other journal, and it must not be represented as a journal-issued report.

I reviewed the revision-130 branch at the head identified above, the self-contained v129 source tree used by that branch, the response to the v128 report, the new bounded principal-colon theorem and universal-primary-finiteness corollary, the relative-assassin argument, the corank-four Cauchy--Pieri repair, the exact generic-slice evidence, the build receipt, and the inherited theorem chain actually compiled by the manuscript. I also checked the precise scope of the Stacks Project results cited in the new relative-assassin proof, in particular Tags 05AS, 0GSJ and 05KR.

# Recommendation

## Reject in the present form at a general top-four mathematics journal.

Revision 130 is the strongest A2 version I have reviewed, and the reason for rejection has changed materially from the v128 report.

The old decisive homological error has been repaired. The manuscript no longer argues that flatness of a final cokernel alone preserves a kernel under base change. The two-short-exact-sequence argument using
\[
0\to I_q\to B\to C_q\to0,
\qquad
0\to K_q\to A\to I_q\to0
\]
is the correct mechanism. The two nontrivial rank-drop support calculations are now performed over the relevant rational function fields, and the corank-four argument now includes right-\(GL(V)\) stability of the ideal and semisimple projection inside the ideal. The source tree is also self-contained and the computational receipt now distinguishes exact algebra from structural proof.

I therefore do **not** repeat the v128 claim that the main family theorem is broken by the four-term Tor mistake, and I do **not** regard the generic \((2,2)\) and \((1,3)\) ruling computations or the missing corank-four invariant projection as open objections.

The remaining difficulty is subtler but still central. Revision 130 promotes a new statement — “universal primary finiteness for symmetric-power quotients” — to the abstract and introduction. That statement depends on a finite geometric-assassin/multiplicity stratification whose proof is still substantially shorter than the theorem it is being asked to support. The cited Stacks results give the correct local ingredients, but the manuscript does not yet prove the exact finite closed-packet theorem, with the asserted constancy of embedded multiplicities, at the level of precision required for a headline theorem.

Even if that relative theorem is repaired, the top-four significance problem remains. The universal determinant identity is elegant, but the new universal corollary is primarily a formal combination of a finite nilpotence bound, flattening, and constructibility. It does not give an explicit universal primary decomposition, an effective stratification, a classification of the generic higher-corank primary supports, or a sharper inverse theorem. The genuinely geometric primary atlas remains concentrated in projection corank two; coranks three and four are still controlled mainly by determinant depth.

For a strong specialist journal I would now regard the manuscript as potentially viable after another serious proof pass and a careful adjustment of scope. For a general top-four journal, I do not yet see either the fully closed relative theorem or the additional conceptual payoff needed to justify the breadth of the present headline claims.

# 1. What revision 130 genuinely fixes

A harsh report should not recycle objections that the authors have actually repaired.

## 1.1 E128.1 is repaired: colon formation is now handled by the correct exact sequences

The new proof puts
\[
B=A/J,\qquad
C_q=B/f^qB,\qquad
I_q=f^qB,\qquad
K_q=(J:f^q),
\]
and uses
\[
0\longrightarrow I_q\longrightarrow B\longrightarrow C_q\longrightarrow0
\]
and
\[
0\longrightarrow K_q\longrightarrow A\longrightarrow I_q\longrightarrow0.
\]

After finite flattening refinement, \(B\) and \(C_q\) are flat. Hence \(I_q\) is flat. Since \(A\) is flat, the second sequence remains exact after arbitrary base change. Together with flatness of \(B\), this also identifies the base-changed ideal \(J_T\) correctly. The fibre kernel is then
\[
(K_q)_T=(J_T:f_T^q).
\]

This directly addresses the counterexample in the v128 report. I find no recurrence of the old incorrect “flat final cokernel implies kernel commutes with base change” inference.

Subject to the broader stratification issue discussed below, the homological core of the colon-base-change repair is sound.

## 1.2 E128.3 is repaired: the nontrivial rank-drop supports are now certified generically

For the \((a,b)=(2,2)\) slice the manuscript now computes, over the slice function field, the common rank-one factor
\[
u_0u_1
\bigl(
(s+9)u_0^2+(3s+6)u_0u_1-7u_1^2
\bigr)
\]
with discriminant
\[
9s^2+64s+288.
\]

The stated open condition excludes collision with \(u_0u_1=0\) and collision of the two additional roots. Thus the generic four-ruling-line support is no longer inferred from a single integral witness.

For \((a,b)=(1,3)\), the function-field factor
\[
10u_0^2+u_0u_1-4u_1^2
\]
has discriminant \(161\), and the manuscript now records the generic saturation
\[
(\delta,\,
10a^2+ac-4c^2,\,
10ab+ad-4cd,\,
10b^2+bd-4d^2).
\]
The Hilbert-function difference gives the claimed embedded vertex contribution of length three.

The checked-in generic-boundary certificate now reflects these calculations over rational function fields. I regard the specific v128 objection here as closed.

## 1.3 E128.4/M128.1 is substantially repaired: the corank-four projection is now taken inside the ideal

The corank-four argument now separates three ingredients which were conflated in v128:

1. the maximal-minor ideal \(J\) is stable for the right \(GL(V)\)-action;
2. the actual coordinate-ring multiplication from the \((4,4,4,0)\) Cauchy component and the degree-four \((4)\)-component has nonzero \((4,4,4,4)\)-projection;
3. complete reducibility in characteristic zero allows the corresponding isotypic projection to be taken while remaining inside \(J_{16}\).

The manuscript also gives the explicit standard-bitableau model
\[
[123\mid123]^4[4\mid4]^4
\]
and identifies the determinant-four line
\[
\mathbf C(\det T)^4.
\]

This is the right architecture. I no longer regard “projection may leave the ideal” as an open correctness objection.

For a final archival version I would still prefer a slightly more explicit straightening citation identifying the exact coefficient-one formula being used, rather than only a general reference to standard bitableau straightening, but this is no longer a decisive issue.

## 1.4 M128.2 is repaired: the referee-facing source package is now self-contained

The v129 source directory used by revision 130 contains local copies of all inherited proof files, and PROVENANCE_MANIFEST.md records their historical source and Git blob identity.

This is the correct way to preserve provenance without requiring an editor or referee to compile a tree assembled from several historical version directories.

The fact that the directory is still named v129 while the front matter says Revision 130 is cosmetically awkward, but not mathematically important.

## 1.5 The evidence discipline is materially better

BUILD_RECEIPT.json now distinguishes:

- scripts actually executed;
- exact algebraic identities checked by those scripts;
- structural arguments that remain source-level mathematics.

In particular the receipt no longer pretends that a Boolean source-presence check machine-certifies the finite geometric-assassin theorem or the Cauchy--Pieri projection. This is a real improvement in reproducibility and scholarly presentation.

# 2. Decisive proof-completeness issue E130.1 — the finite geometric-assassin packet theorem is still not proved at the claimed strength

The new Lemma “Finite geometric-assassin stratification” is the logical bridge from the corrected colon-base-change argument to the universal headline conclusion.

Its conclusion is strong. After finite locally closed stratification it asserts finitely many closed packets
\[
Z_\nu\subset X
\]
such that for **every geometric fibre**
\[
\operatorname{Ass}(\mathcal F_{\bar s})
=
\bigcup_\nu
\{\text{generic points of irreducible components of }(Z_\nu)_{\bar s}\},
\]
with geometric splitting allowed, and after further refinement it claims constant incidence and minimal-versus-embedded status.

The cited Stacks results are relevant, but they do not by themselves state this packet theorem.

### What the cited results actually provide

Tag 05AS gives the relative assassin formalism and its behaviour under field extension/base change.

Tag 0GSJ is powerful: for the closure \(Y\) of a known relative associated point, under flatness the generic points of irreducible components of fibres of \(Y\to S\) remain relative associated points. This is exactly the correct tool for preventing a tracked generic packet from producing false generic components.

Tag 05KR proves constructibility of the locus
\[
\{s\in S:
\operatorname{Ass}(\mathcal F_s)\subset U_s\}
\]
for a **fixed open** \(U\subset X\).

These ingredients strongly suggest that the desired finite stratification is true in the finite-presentation setting. But the manuscript still makes a nontrivial leap when it says:

> Applying this to a finite affine cover adapted to the closures just constructed, and intersecting the resulting constructible conditions, gives a dense constructible locus on which the generic packets exhaust the geometric fibrewise assassin.

That sentence is not a proof of the reverse inclusion.

The problem is that “all associated points lie in a specified open set” and “all associated points are precisely the generic points of the fibres of these specified closed packets” are different assertions. A fixed open-neighbourhood containment condition does not automatically exclude:

- a new embedded associated point appearing inside the same closed support packet but away from its fibrewise generic points;
- an additional associated specialization lying in an intersection of tracked packet closures;
- a new fibrewise associated point that lies in every chosen open neighbourhood of a tracked closure but is not a generic point of a component of that closure.

The proof says that a finite affine cover can be chosen “adapted” to the closures, but it never defines the resulting opens or proves that the 05KR conditions are equivalent to exact exhaustion by the listed packet generic points.

This is precisely where the new theorem becomes stronger than the cited constructibility statement.

### Why this matters

The universal corollary does not merely need persistence of known associated points. It needs **exhaustion** of all fibrewise associated points by a fixed finite list of packet closures on each final stratum.

Without that reverse inclusion, the manuscript has established a robust family of tracked associated supports, but not the exact primary signature claimed in Theorem \(\ref{thm:bounded-principal-colon-stratification}\), Proposition \(\ref{prop:associated-prime-refinement}\), the abstract, and the universal corollary.

### Required repair

I would require a self-contained proposition whose proof explicitly separates the two inclusions.

On an irreducible base stratum:

1. list the associated points \(\xi_1,\ldots,\xi_m\) of the geometric generic fibre;
2. after finite extension if needed, take their Galois packets and scheme-theoretic closures \(Z_i\);
3. shrink so that the relevant closures and \(\mathcal F\) satisfy the hypotheses needed for 0GSJ; this gives
   \[
   \{\text{generic points of components of }(Z_i)_{\bar s}\}
   \subset
   \operatorname{Ass}(\mathcal F_{\bar s});
   \]
4. prove the reverse inclusion on a nonempty open of the base by an explicit constructible condition.

The last step is the missing one. One possible route is to spread a finite prime/cyclic filtration of the generic fibre and use universal injectivity after flattening of the successive cokernels. Another is to give an exact reduction from “there exists an untracked associated point” to a finite list of 05KR-type open-containment conditions. But the finite list and the equivalence have to be written down.

After that generic-open result is proved, Noetherian induction on the complement can legitimately add new packets and terminate.

I would also state the geometric base-change step explicitly using the associated-point description under extension of residue fields rather than leave “packets may split geometrically” as prose.

Until this is done, the central new family theorem is not proved at the strength in which it is advertised.

# 3. Decisive proof-completeness issue E130.2 — constancy of embedded multiplicities needs a relative construction, not only “spread the torsion module”

The same lemma asserts constancy of
\[
\mu_p(\mathcal F_{\bar s})
=
\operatorname{length}
H^0_{p\mathcal O_{X_{\bar s},p}}
(\mathcal F_{\bar s,p})
\]
along every tracked associated packet.

At a fixed associated point this is a perfectly sensible finite length. The problem is the family argument.

The proof says:

> Choose \(n\) with \(p^nT_p=0\), spread both the packet ideal and the finite torsion module after shrinking, and filter it by the powers of that ideal. The successive quotients are finite modules on the packet. Generic freeness makes their generic ranks constant after shrinking, and the sum of those ranks is exactly the displayed length.

This is plausible as a roadmap, but it skips the step that identifies the spread-out finite module with the **fibrewise local torsion**
\[
H^0_{p_s}(\mathcal F_{s,p_s})
\]
for every generic point \(p_s\) of the packet fibres.

Spreading a finite submodule from the generic localization gives a coherent model after shrinking. It does not automatically show that no additional \(I_{Z}\)-power torsion appears after specialization, or that the spread-out module commutes with the relevant localization and fibre operation.

That is exactly the phenomenon whose constancy the theorem is trying to prove.

### Required repair

A clean proof should introduce an actual coherent relative module, for example
\[
T_n=(0:_{\mathcal F}\mathcal I_Z^n)
\]
for a fixed sufficiently large \(n\), and then prove after shrinking that:

1. localization of \(T_n\) at the generic points of the packet fibres equals the entire local \(H^0\)-torsion;
2. this equality remains valid on the chosen base stratum;
3. the finite filtration
   \[
   T_n\supset \mathcal I_ZT_n\supset\cdots
   \]
   has coherent graded quotients whose generic ranks on \(Z\) are constant after flattening;
4. those ranks compute the desired fibrewise lengths, including after geometric base extension.

Equivalent arguments using a relative primary filtration or a local Hilbert function would also be acceptable.

At present, the manuscript has the right invariant and the right heuristic mechanism, but not yet a proof that the invariant is constant in the asserted family.

This gap propagates directly to the “constant embedded multiplicities” clause of the bounded principal-colon theorem and therefore to the new universal corollary.

# 4. Major formulation issue M130.1 — the universal corollary claims conclusions that are not literally “exactly the four clauses” of the theorem

The new Corollary “Universal primary finiteness for symmetric-power quotients” states, after finite stratification of the surjection parameter space, constant:

- associated-support packets;
- minimal/embedded incidence;
- embedded multiplicities;
- Hilbert polynomials;
- multiplication ranks.

Its proof ends:

> All stated conclusions are exactly the four clauses of that theorem.

That is not literally correct.

The bounded principal-colon theorem as stated does not mention a grading or a Hilbert polynomial. It says the \(M_q\) are flat and that a **prescribed finite collection** of maps may be included so their relevant modules are flat and fibre ranks commute with base change.

For the universal symmetric-power family these additional conclusions are probably recoverable, but they need to be stated correctly.

### Required repair

Specify the standard grading on the \(\operatorname{End}(V)\)-coordinate algebra and either:

- prove that flatness of the graded \(M_q\) makes every finite-degree graded piece locally free after the chosen finite refinement and hence fixes the Hilbert function/polynomial; or
- pass to the corresponding projective sheaves and invoke the standard Hilbert-polynomial flatness statement.

Likewise, explicitly define the finite family of natural multiplication maps whose ranks are being asserted constant. The general theorem allows an arbitrary prescribed finite family, but the corollary should name the family relevant to the claimed “primary complexity.”

This is not the deepest problem in the manuscript, but because the corollary is now abstract-level material, the statement should not be stronger or less precise than the theorem it cites.

# 5. Structural/top-four issue S130.1 — “universal primary finiteness” is mostly a formal finiteness theorem, not a universal primary classification

Revision 130 was clearly designed to answer S128.4: the previous report asked for a genuinely broader consequence of the determinant-completion theorem.

The new corollary is a legitimate response in the sense that it is broader than the \((1,4,6)\) model. But its actual content needs to be judged carefully.

The determinant-completion identity provides
\[
d^N\in J_{\mathrm{univ}},
\qquad
N=\binom{e+r-1}{r-1}.
\]
This truncates the colon tower to finitely many residual colons
\[
(J_{\mathrm{univ}}:d^q),\qquad 0\le q<N.
\]

Once the list is finite, generic flatness/flattening and constructibility of associated-point behaviour are standard mechanisms for obtaining some finite locally closed stratification on which a finite collection of invariants is constant.

What the corollary **does not** currently provide is:

- an explicit description of the strata;
- an effective bound on their number or degree;
- an explicit primary decomposition on the universal family;
- a representation-theoretic classification of the possible associated-support packets;
- an explicit list of packet geometries;
- a canonical or equivariant stratification;
- a sharp determinant exponent for a broad non-square class of quotient maps;
- or a geometric interpretation of the higher layers outside the special A2 model.

Thus “finite primary complexity” should not be read as “the primary structure has been classified.” The theorem gives a finite **constructible associated-support/multiplicity stratification**, assuming E130.1/E130.2 are supplied. It does not give a universal primary atlas in the sense in which the corank-two tables do.

This distinction is especially important because no actual family of primary components \(Q_i\) is constructed in the universal theorem. The data being tracked are associated supports, incidences, selected generic lengths, Hilbert data, and multiplication ranks. Those are valuable primary invariants, but they are not themselves a primary decomposition.

### Top-four consequence

The new corollary therefore does not yet solve the significance problem identified in v128. It turns the determinant bound into a broad finiteness principle, but the proof mechanism is largely formal once the bound is known.

For a general top-four journal I would still want a more structural consequence, for example one of the following:

- classify the possible generic primary packets for a nontrivial infinite family of \((e,r,s)\), rather than only prove some finite stratification exists;
- determine the sharp determinant exponent for a broad class of non-isomorphic quotient maps \(\gamma\);
- identify the residual layers with a geometric discriminant/ramification construction beyond \((1,4,6)\);
- prove a uniform representation-theoretic formula for the higher-corank primary supports;
- or show that the deeper nilpotent data resolves or strictly reduces the finite ambiguity in the inverse problem.

The present universal corollary is useful scaffolding for such a theorem. I do not think it is yet the missing top-four theorem by itself.

# 6. Structural issue S130.2 — higher corank is still depth, not an explicit primary boundary atlas

Revision 130 does not close the main geometric issue from S128.1.

At projection corank two, the paper now has genuinely detailed primary geometry: explicit generic signatures, ruling-line supports, vertex-primary contributions, generic function-field certificates, and orbit specialization laws.

At projection corank three the explicit theorem remains
\[
d^3\notin J,\qquad d^5\in J,
\]
with the single membership condition
\[
d^4\in J
\]
separating the two possible determinant depths.

At projection corank four it proves
\[
d^3\notin J,\qquad d^4\in J,
\]
hence exact depth five.

The new bounded principal-colon theorem says that, after some finite refinement, the associated-support packets and multiplicities are constant. It still does **not** say what the generic packets actually are on the corank-three and corank-four strata.

This matters for the current title and abstract. “Intrinsic primary boundary laws” naturally suggests that the boundary primary geometry has been described. In the strongest new higher-corank sections, however, the geometry is still encoded by an existence stratification and a determinant-depth invariant.

There are two coherent ways to resolve this.

### Route A — broaden the mathematics

Compute at least the generic \(W_j\), associated primes/supports, and generic lengths at projection coranks three and four, with a mechanism that explains the pattern rather than a long witness list.

This would make the phrase “primary boundary atlas” genuinely global.

### Route B — narrow the interpretation, not the results

Keep the current theorems, but state explicitly that the paper gives:

- a complete generic primary atlas at projection corank two;
- exact determinant-depth results at coranks three and four;
- and an abstract finite stratification theorem for their remaining primary invariants.

The present wording repeatedly turns the third item into a substitute for the first. For a top-four submission I would not make that substitution.

# 7. Structural issue S130.3 — the explicit specialization laws still do not traverse projection corank \(2\to3\to4\)

The corank-two specialization table is a real strength of the paper. It gives actual one-parameter families realizing:

- off-Segre to on-Segre;
- secant to tangent;
- secant to either ruling;
- tangent to dual-rank-two;
- ruling to dual-rank-one;
- rank-one types to the zero mixed map.

The manuscript also gives a pure-block rank-drop family.

But the global boundary has another direction: the projection corank itself changes. The previous report explicitly asked for the adjacency
\[
2\rightsquigarrow3\rightsquigarrow4
\]
together with the behaviour of the intrinsic graded pieces.

Revision 130 still does not compute those specializations.

The new relative theorem says that on each final stratum the objects commute with arbitrary base change. That is not the same as describing what happens when a one-parameter family crosses from one stratum to another — exactly where associated supports can merge, acquire embedded structure, or change dimension.

For a paper whose stated theme is boundary laws, this cross-corank specialization remains one of the most natural missing geometric theorems.

# 8. Structural issue S130.4 — the inverse problem is unchanged

I continue to regard the polarized reconstruction theorem as the most conceptually attractive part of the paper:

> the abstract nonreduced multiplication-failure scheme determines the polarized quartic K3 surface.

Revision 130 preserves this theorem, as it should.

But the deeper primary data still do not:

- recover the original relation web;
- determine the Reye/Enriques datum;
- prove generic injectivity of the web-to-K3 map;
- compute the finite degree of that map;
- or distinguish members of the remaining finite Torelli packet.

The manuscript is commendably careful not to claim generic injectivity. The new global finiteness corollary is presented as the alternative conceptual advance.

That is legitimate, but it means the inverse side of the paper has not advanced since the previous review. For top-four significance, a theorem showing that the newly computed nilpotent layers strictly sharpen the inverse problem would be much more compelling than another noncanonical finiteness stratification.

# 9. Major terminology issue M130.2 — “primary” should be used with more precision in the universal statements

The explicit corank-two tables really do contain primary-geometric information: associated supports, saturations, embedded vertex modules, and in several rows concrete primary behaviour.

The universal theorem is different. It constructs no primary decomposition
\[
I=Q_1\cap\cdots\cap Q_m
\]
and no flat family of primary ideals \(Q_i\).

It tracks:

- residual colon modules;
- associated-support packets;
- minimal/embedded incidence;
- local torsion lengths;
- Hilbert data;
- and multiplication ranks.

Calling this a “primary signature” is defensible if the term is explicitly defined as this package of invariants. Calling the resulting noncanonical flattening/assassin stratification a “universal primary stratification” without qualification risks suggesting that primary components themselves have been spread out and classified.

I recommend that the paper reserve “primary decomposition/primary atlas” for places where actual component structure is determined, and use a phrase such as

> finite associated-support and multiplicity stratification

for the general theorem unless a relative primary-decomposition theorem is really proved.

This is not merely stylistic. It affects how much mathematical content the new global consequence appears to claim.

# 10. The corank-four proof is no longer a blocker, but the decisive straightening coefficient should be made completely audit-ready

As noted in Section 1.3, I now accept the architecture of the corank-four \(d^4\in J\) proof.

Still, this is a point on which two consecutive referee rounds have had to focus, and it should be made impossible to misunderstand.

The sentence
\[
[123\mid123]^4[4\mid4]^4
=
[1234\mid1234]^4+
\sum_{\tau\ne\nu}c_\tau B_\tau
\]
with coefficient one on the determinant-four standard bitableau is the decisive concrete nonvanishing.

For a final version I would either:

- give the exact standard-bitableau straightening rule that produces this coefficient, with the precise proposition/theorem number in De Concini--Eisenbud--Procesi; or
- include a short self-contained straightening calculation.

The BUILD_RECEIPT correctly labels this as structural proof rather than machine certification. I agree with that evidence discipline.

I do not presently regard this as a reason to reject on correctness, but a top-four final proof should not require the referee to reconstruct the key coefficient from a broad citation.

# 11. Computational evidence — now appropriately scoped

The computational part is one of the better developed aspects of the current revision.

The exact scripts and certificates cover, among other things:

- the generic transverse-slice Gröbner calculations;
- determinant-depth witness regressions;
- the generic \((2,2)\) factor and discriminant;
- the generic \((1,3)\) factor, saturation and length-three quotient;
- corank-two exact checks;
- selected representation-character regressions.

The revised build receipt explicitly says that the following remain structural proof only:

- bounded principal-colon base change;
- finite geometric-assassin stratification;
- coordinate-ring Cauchy--Pieri projection.

That is exactly the right distinction.

I therefore have no objection to the use of exact symbolic computation in the current paper. My objections E130.1 and E130.2 concern the parts that the evidence receipt itself correctly identifies as non-computational.

# 12. Documentary/priority issue M130.3 — the Ballico boundary is responsibly stated but still needs a final literature audit

The manuscript cites Ballico’s 1993 paper and avoids claiming theorem-level nonanticipation without having a complete comparison.

That is responsible and should be preserved.

However, a top-four novelty assessment ultimately cannot leave a directly relevant historical paper at the level of a documentary placeholder. Before a serious submission, the author should obtain the full text and prepare a theorem-by-theorem comparison explaining exactly what is classical and exactly what is new.

The same principle applies to the classical Reye-congruence/K3 material: the manuscript now distinguishes the classical nine-dimensional moduli count from its own inverse statement, which is good, but the final introduction should make the novelty boundary maximally explicit.

This is not a correctness objection. It is part of the editorial significance assessment.

# 13. Minor presentation and architecture comments

1. The branch is revision 130 but the complete source tree remains under article/v129. This is understandable historically, yet for a final immutable submission I would materialize an article/v130 directory so that the source path, front-matter version and build receipt agree.

2. The universal corollary uses \(S\) both in the general relative-algebra discussion and as the target vector space of \(\gamma:\operatorname{Sym}^rV\twoheadrightarrow S\). The notation is survivable, but unnecessary ambiguity in the most general theorem should be removed.

3. The phrase “all stated conclusions are exactly the four clauses” in the universal corollary should be replaced even if M130.1 is repaired, because the Hilbert-polynomial conclusion is an additional graded consequence.

4. The introduction should distinguish “arbitrary base change **within a final stratum**” from specialization **across** strata. Several current sentences are easy to read as if the former solved the latter.

5. The abstract is now carrying four logically different layers of result: universal determinant completion, relative finite stratification, explicit corank-two classification, and K3 reconstruction. I would shorten it after the theorem hierarchy is final so that the strongest proved geometric consequence is more visible.

6. The self-contained source/provenance solution is good. Keep the manifest, but do not require historical branch knowledge for the final journal package.

# 14. Status of the v128 issues after revision 130

## E128.1 — colon formation and base change

**Closed.**

The two-short-exact-sequence argument fixes the previous mathematical error.

## E128.2 — finite associated-point stratification

**Partially closed, but replaced by E130.1/E130.2.**

The paper now cites the correct constructibility result and formulates geometric packets. The remaining problem is no longer “missing citation.” It is that the manuscript has not supplied the additional argument turning those ingredients into the exact packet-exhaustion and constant-multiplicity theorem it states.

## E128.3 — generic ruling factors on rank-drop slices

**Closed.**

The relevant factors and discriminants are now computed over the correct rational function fields, and the \((1,3)\) saturation quotient is checked generically.

## E128.4 / M128.1 — corank-four ideal membership

**Closed in substance.**

Right-\(GL(V)\) ideal stability, semisimple projection and an explicit Cauchy--Pieri nonvanishing are now all present. I retain only the auditability comment in Section 10.

## E128.5 — higher-corank primary geometry

**Not closed geometrically.**

The paper now has a stronger abstract finite-stratification theorem, but it still does not identify the generic primary supports at coranks three and four.

## E128.6 / S128.4 — genuinely global consequence

**Formally advanced, not closed at top-four significance level.**

The new universal corollary is a real theorem-level consequence if E130.1/E130.2 are completed. It is nevertheless a nonexplicit finiteness result and does not yet supply the structural classification or geometric consequence I was asking for.

## S128.2 — specialization across the boundary

**Still partial.**

The corank-two orbit degenerations are retained and useful. The projection-corank \(2\to3\to4\) specialization remains untreated.

## S128.3 — inverse problem

**Unchanged.**

The K3 is reconstructed; the original multiplication tensor/web is not.

## M128.2 — source architecture

**Closed.**

The referee-facing tree is self-contained with provenance manifest.

## M128.3 — Ballico 1993

**Still documentary-open, responsibly handled.**

# 15. What I would require before another top-four review

I would not request another top-four-style review merely after cosmetic revision. The next round should close a small number of mathematically decisive items.

## E130.1 — prove the finite geometric-assassin packet theorem exactly

Give a proof of both inclusions in the fibrewise associated-point equality, with explicit use of the chosen constructible loci and a complete Noetherian-induction argument.

Do not leave “adapted finite affine cover” as the step that performs the main logical work.

## E130.2 — make embedded multiplicity a genuinely relative invariant on each packet

Construct the coherent relative torsion module or equivalent filtration whose fibrewise generic lengths are the claimed multiplicities, and prove the necessary base-change/specialization statement.

## M130.1 — repair the universal corollary statement

State the grading, Hilbert invariant and finite collection of multiplication maps precisely, then derive them from the general theorem rather than saying they are literally already among its clauses.

## S130.1 — either compute higher-corank primary geometry or narrow the global atlas language

A general top-four paper should not advertise a global primary atlas when the actual explicit primary geometry ends at corank two.

The stronger option is to determine generic \(W_j\) and associated supports at coranks three and four.

## S130.2 — extract a nonformal consequence from the universal determinant theorem

The current universal finiteness principle is useful but largely formal after the exponent bound. Add a theorem that classifies, sharpens, or geometrically interprets the universal family in a way not supplied by generic flattening/constructibility alone.

## S130.3 — add at least one global boundary specialization or inverse consequence

Either compute the intrinsic graded degeneration across projection corank \(2\to3\to4\), or show that the deeper nilpotent signature reduces the inverse ambiguity.

Either direction would connect the long boundary algebra to a genuinely global geometric theorem.

## M130.3 — finish the literature audit

Read the full Ballico 1993 paper and record a precise novelty comparison before making final priority claims.

# 16. Final assessment

Revision 130 is a serious improvement.

The most important positive conclusion of this report is that the previous elementary counterexample to the colon-base-change proof no longer applies. The generic rank-drop support calculations are now performed at the correct generic points, the corank-four ideal-membership argument has the missing representation-theoretic projection mechanism, the source package is self-contained, and the computational evidence is presented with much better epistemic discipline.

I therefore regard the current manuscript as mathematically substantially stronger than revision 128.

I nevertheless do not recommend it for a general top-four journal in its present form.

The new headline consequence rests on a finite geometric-assassin and embedded-multiplicity theorem whose proof still compresses the hardest step into a constructibility sentence that does not, as written, yield the exact packet theorem claimed. That is the main proof-completeness blocker.

After that is repaired, the editorial problem remains: the universal determinant theorem plus noncanonical finite stratification is broad but largely formal, while the detailed new geometry remains concentrated in the specialized corank-two atlas. Coranks three and four are still primarily depth theorems, the cross-corank specialization is not computed, and the deeper nilpotent data do not yet sharpen the inverse problem.

My recommendation is therefore:

**Reject in the present form at a general top-four mathematics journal.**

I would encourage a further revision if it does two things simultaneously: first, fully proves the relative packet/multiplicity theorem at the strength advertised; second, converts the universal determinant bound or the higher-corank boundary into one genuinely explicit global geometric theorem. Without the second step, the manuscript may become a strong specialist paper, but I do not yet see the case for the present top-four scope.
