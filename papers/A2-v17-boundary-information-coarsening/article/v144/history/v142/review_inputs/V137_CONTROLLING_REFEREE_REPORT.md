# Independent harsh referee report — A2 revision 137

## Manuscript and review scope

**Manuscript:** *Intrinsic reconstruction from nonreduced failure schemes*  
**Author:** Qian Qi  
**Reviewed revision branch:** `revision/a2-v137-intrinsic-coefficient-torelli-2026-09-23`  
**Source commit recorded by the v137 build receipt:** `45cff45710d6174560a5ec0034d9a7223952bd67`  
**Reviewed predecessor head recorded by v137:** `731729b9e391b507d27994f6db8d71d61cfca577`  
**Controlling predecessor report:** `reviews/a2-v136-independent-harsh-top4-2026-09-23/REFEREE_REPORT.md`, commit `d15c9bcabdfc31070b773e2c8014601e75d4e641`  
**Review standard:** external-referee-style assessment at the level of *Annals of Mathematics*, *Acta Mathematica*, *Inventiones Mathematicae*, or *Journal of the AMS*.

This is an owner-requested, AI-assisted referee-style report, not a journal-commissioned editorial decision.

I reviewed the 37-page principal article source, the new v137 structural coefficient section, the relative rank-one Fano scheme lemma, the common-(g) descent, the full-(O_n) harmonic lemma, the all-dimensional contraction/support theorem, the main four-dimensional web reconstruction argument, the v137 literature audit and response to v136, and the source-bound build receipt. I also checked the mathematical role of the 66-page supplement and the 99-page complete compilation. The v137 build receipt records a successful GitHub Actions run, twelve exact scripts, 292 current mathematical labels with all 274 inherited labels retained, no unresolved references/citations, and successful PDF builds. I treat those checks as reproducibility evidence only, not as proof of the structural theorems or of novelty.

## Recommendation

**Reject in the present form at a general top-four journal.**

This recommendation is no longer driven by the three scheme/representation proof gaps that dominated revision 136. Revision 137 has repaired those points substantially and, in my view, credibly. The remaining obstacles are now more serious in a different sense: the closest historical comparison is still knowingly incomplete, the new “second family” is too engineered to close the conceptual-significance gap by itself, and the paper still has not established a sufficiently compelling external mathematical significance case for a general top-four venue.

I would support a fresh review after those issues are genuinely addressed. I would not describe the present remaining work as minor.

## 1. What revision 137 has genuinely fixed

Three items from the v136 report have moved from blockers to strengths.

### 1.1 The relative rank-one Fano scheme is now proved scheme-theoretically

Lemma `lem:rank-one-fano-scheme` is a real repair, not a rhetorical patch. It defines the relative parameter scheme as the zero scheme of the restricted quadratic rank-one equations on the universal subbundle, proves the two natural projective-bundle maps are closed immersions, classifies geometric points, computes the full Zariski tangent space, and uses the local-dimension/tangent-dimension equality to conclude regularity and reducedness. The final arbitrary-base statement is then obtained by local trivialization and literal base change of the constant model, including nonreduced bases.

This addresses the v136 concern about nilpotent thickening, embedded infinitesimal components, and hidden special-fibre structure. I found no counterexample to the written argument.

A minor exposition improvement would be to say explicitly that the displayed condition (u\wedge A(u)=0) for every (u) polarizes to the full linearization of the quadratic restriction map. The current argument is correct in characteristic zero, but that one sentence would make the tangent calculation completely audit-proof.

### 1.2 The normal-cone-to-common-(g) chain is now explicit

Equation `eq:full-intrinsic-chain` and Lemma `lem:common-g-functoriality` substantially improve the paper. The manuscript now clearly distinguishes:

- the intrinsic deepest stratum;
- the associated graded normal-cone algebra;
- the degree-one conormal bundle before tensor-factor choices;
- the rank-one Fano scheme and the oriented trivial ruling;
- the determinant ideal line;
- the intrinsic residual colon;
- the Cauchy coefficient spaces;
- the final exterior-duality twist.

The line-bundle ambiguity of local lifts is tracked, the right change of frame is confined to the right Cauchy factor, and the common ((\det V)^{-5}) twist is displayed rather than hand-waved. The use of projectivity and (H^0(B,\mathcal O_B)=\mathbf C) to make the resulting (operatorname{PGL}(V))-valued morphism constant is appropriate.

This closes the main auditability objection from v136.

### 1.3 The full orthogonal harmonic input is now self-contained

Lemma `lem:full-orthogonal-harmonics` gives an actual proof for all (n\ge2), including the disconnected (O_2) case. The stabilizer-fixed-vector argument and the reproducing/evaluation orbit argument are a clean way to prove irreducibility for the full compact orthogonal group, and the invariant angular operator separates harmonic degrees. The determinant twist is harmless because it is common.

I would add one sentence making explicit that a complex subspace invariant under (O_n(\mathbf C)) is in particular invariant under (O(n,\mathbf R)), so irreducibility for the compact real subgroup suffices. But this is an exposition point, not a detected mathematical failure.

## 2. Major blocker B137.1: the Ballico 1993 comparison is still open

The manuscript itself correctly states that the complete text of E. Ballico, *On the Failure Locus of Higher Order Properties of Embeddings in Projective Spaces*, Math. Nachr. 163 (1993), 5–13, DOI 10.1002/mana.19931630102, has not been obtained and that the requested six-axis theorem comparison remains unverified.

That is not a cosmetic bibliography issue. “Failure locus”, higher-order embedding properties, degeneracy/failure schemes, and the present paper’s nonreduced Fitting geometry are close enough in subject that a top-four novelty judgment cannot responsibly be made from the title, first page, or later citations. The v137 literature audit handles this honestly, but honesty about an unresolved priority issue does not close the issue.

My own public-source check recovered the bibliographic record and later literature citing the 1993 article, but not theorem text sufficient to resolve the six axes. Therefore I cannot certify that the paper’s claimed conceptual novelty is separated from this closest historical source.

**Required action:** obtain the full article through a lawful library/interlibrary route and compare, theorem by theorem:

1. parameter spaces;
2. reduced versus scheme-theoretic failure loci;
3. the varied multiplication/higher-order map;
4. infinitesimal, nilpotent, colon, or normal-cone data;
5. relative/base-change assertions;
6. inverse or reconstruction conclusions.

Until that is done, I would not support a general top-four submission.

## 3. Major blocker B137.2: the new polar-Fitting family is mathematically valid but conceptually too engineered

Revision 137 answers the v136 request for a second intrinsic family by introducing the block map
[
\Psi_L=
\begin{pmatrix}
\det T&0\\
0&\operatorname{ev}_{L,T}
\end{pmatrix}
]
and the zeroth-Fitting scheme (Z_L).

The proof of Theorem `thm:polar-system-torelli` is clean. In local coordinates the Fitting ideal is exactly
[
I(Z_L)=(\det T)J_L,
]
and the degree-(d) piece of the residual ideal is exactly the Cauchy image
[
(J_L)_d=L\otimes\operatorname{Sym}^d\mathcal U.
]
The zero section is recovered from the iterated singular loci of the determinant hypersurface, the oriented Segre ruling recovers the common projective (V)-factor, and taking the intrinsic colon by the determinant line recovers (J_L), hence (L).

I do not see a correctness problem in that argument.

But as a response to the **conceptual-generalization** objection, this construction is not yet persuasive at the top-four level. The scheme has been designed so that the hidden datum (L) is inserted directly into one block, and the proof then recovers it from the residual coefficient module after dividing out the determinant factor. In other words, the second example shows that the extraction formalism is reusable, but it does not yet demonstrate that a naturally occurring and independently interesting geometric failure scheme unexpectedly remembers coefficients that its reduction forgets.

The distinction matters. A reusable lemma plus a deliberately encoded test family is not the same thing as a new geometric principle with independent force.

**Required action:** either

- give a second naturally occurring family from established geometry/moduli where the failure scheme arises independently of the reconstruction goal and where the nonreduced structure solves a recognized inverse problem; or
- derive a substantial external consequence of the web theorem itself—one that experts would recognize as resolving an existing Torelli/moduli ambiguity.

Without that, v137 closes the formal generalization request but not the significance request that motivated it.

## 4. Major blocker B137.3: the “structural coefficient principle” is currently a criterion, not yet a theory

Theorem `thm:structural-coefficient-reconstruction` is correct in spirit and useful organizationally. However, its hypotheses already contain nearly all the structure needed for the conclusion:

- an intrinsically selected projective base;
- a degree-one bundle presented as (V\otimes\mathcal U^*);
- a determinant-cone reduction with a uniquely oriented trivial ruling;
- a residual factorization (mathcal I=\mathcal D\mathcal J);
- a degree-(m) Cauchy decomposition whose left coefficient spaces are constant over the base.

Once these hypotheses are available, the common-(g) conclusion is a fairly formal consequence of the Segre preserver and Cauchy functoriality.

That is valuable, but the paper presently oversells it as evidence for a broad new reconstruction mechanism. What would make this a genuine principle is a theorem explaining when hypotheses (i)–(iii) arise from intrinsic geometry, or a nontrivial classification of failure schemes for which they hold. At present the difficult work is still instance-specific: proving the web normal cone has exactly the stated residual module, or building the polar example so that it does by construction.

I recommend reframing this as a **reconstruction criterion** unless and until a broader structural theorem is proved.

## 5. Major blocker B137.4: the top-four significance case remains unresolved

The main four-dimensional theorem is now mathematically much more credible:

> for every basepoint-free four-dimensional web with smooth Jacobian quartic, the abstract nonreduced multiplication-failure scheme determines the web up to projective equivalence.

That is a serious theorem.

What is still missing is a convincing answer to: **which recognized external problem does this solve?**

The paper says several different things:

- it is a Torelli theorem for nonreduced failure schemes;
- it separates the finite ambiguity of a polarized Jacobian K3;
- it reconstructs hidden Pluecker components from infinitesimal determinantal structure;
- it gives a general coefficient readout principle;
- it relates webs, Reye congruences, and Enriques data.

These are not equivalent significance narratives. A top-four paper should identify the primary one and document its status in the literature.

The present “finite web-to-K3 packet” discussion is mathematically useful, but the paper does not yet show that this finite ambiguity was a recognized outstanding problem rather than an ambiguity created by the paper’s own chosen invariant. Likewise, the polar-Fitting construction does not by itself establish a field-level conceptual breakthrough.

A strong revision should formulate one explicit external theorem of the form:

- a previously studied moduli map is generically finite/noninjective, and the new failure-scheme invariant is the first natural invariant that resolves its fibres; or
- a known Torelli-type problem for webs/Reye congruences/Enriques data is settled; or
- a recognized class of nonreduced degeneracy schemes is shown to carry coefficients invisible to all reduced degeneracy data.

The paper is closest to being compelling when it focuses on the first of these, but the historical/moduli case is not yet developed to that standard.

## 6. Major blocker B137.5: the all-dimensional contraction theorem still needs a broader exact novelty audit

Theorem `thm:uniform-contraction` is one of the strongest pieces of v137. The written proof is coherent:

- singular kernels are reduced to the radical by shear descent;
- the nondegenerate even-dimensional scalar line is produced by the cofactor/Piola cancellation;
- every positive harmonic summand is shown nonzero by an explicit coefficient computation;
- full-(O_n) irreducibility prevents hidden cancellation.

The resulting support formula and the (>2n) secant/tangent gap are clean.

The literature audit is improved: it now separates classical exterior-symmetric plethysm (Cheng–Wang), Fischer/harmonic decomposition (De Bie–Eelbode–Roels), Piola cancellation (Kupferman–Shachar), and skew-flattening support (Landsberg–Ottaviani/Sheridan) from the map-specific kernel calculation.

That is the right structure. But for a result that is now carrying much of the paper’s broad significance, the audit is still too local. The key novelty claim is not the occurrence of the representation but the exact rank-dependent kernel of
[
\iota_q\circ j_n: \det V\otimes\operatorname{Sym}^nV
\longrightarrow \bigwedge^{n-1}\operatorname{Sym}^2V
]
for every rank of (q), together with the even-dimensional quadratic-power exception. Before presenting this as a principal broad theorem, the authors should compare it with classical invariant theory, transvectants/contractions of symmetric powers, orthogonal branching, and known descriptions of the Jacobian/polarization embedding.

I do not currently have evidence that the theorem is anticipated. I also do not think the present audit is sufficient to certify that it is not.

## 7. The main web reconstruction proof is now plausible, but a few local clarifications would improve auditability

I did not find a fatal defect in the v137 main proof. In particular:

- the deepest stratum is recovered by iterated reduced singular loci;
- the normal cone keeps the full homogeneous ideal, not only the reduction;
- the determinant line and residual colon are intrinsic;
- the universal Schur coefficient map separates the two left coefficient lines;
- the common-(g) lemma prevents independent coordinate changes on the two components;
- the Jacobian component has exterior support (\ge9) for at least three essential variables;
- secant and tangent vectors of the Grassmannian have support (\le8);
- the component pencil therefore has one reduced decomposable point on the smooth locus.

This is a coherent proof architecture.

I nevertheless recommend the following local improvements before another external review.

1. In `lem:rank-one-fano-scheme`, explicitly polarize (u\wedge A(u)=0) to the full bilinear linearization of the restricted quadratic map.
2. In `lem:full-orthogonal-harmonics`, add the one-line compact-real-to-complex-group irreducibility implication.
3. In Theorem `thm:polar-system-torelli`, display the local (2\times N) matrix for (\Psi_L) once, so that the equality (operatorname{Fitt}_0\operatorname{coker}\Psi_L=(\det T)J_L) is literally visible.
4. In the main theorem, keep the distinction between reduced support identities and scheme-theoretic identities exactly as written. Do not strengthen those claims for rhetorical symmetry.

These are not rejection-level mathematical objections.

## 8. The paper should be more careful with the word “Torelli” for the polar example

For a single equation (L=\mathbf C f), Theorem `thm:polar-system-torelli` does produce a scheme-valued invariant that separates projective classes of (f). But this is an auxiliary scheme built from a block map that contains the coefficient evaluation of (f) by definition.

Calling this a Torelli theorem is formally defensible, but it invites a stronger geometric interpretation than the construction currently merits. In conventional usage, a Torelli theorem is persuasive because the recovered object is a natural invariant already of independent geometric interest.

I suggest either motivating (Z_L) independently—e.g. as a natural degeneracy construction arising elsewhere—or using more neutral language such as “coefficient reconstruction from a polar Fitting scheme.”

## 9. Reproducibility is excellent and should remain subordinate to mathematics

The source-bound evidence is unusually disciplined. The principal article is now 37 pages rather than forcing an editor through the 99-page archive, and the supplement is genuinely separated. The build receipt explicitly distinguishes machine-checked identities/build integrity from unverified general proofs and historical priority.

That is good practice.

For an actual journal submission, however, the response history, version infrastructure, source hashes, and build narrative should stay out of the mathematical foreground. The article should read as a finished paper, not as the visible endpoint of 137 revision rounds. The current v137 article is much closer to this goal than earlier versions, but a final submission should remove the remaining programmatic language that is not mathematically necessary.

## 10. Required work before I would support a fresh top-four review

I would require all of the following.

1. **Complete the Ballico 1993 theorem-level comparison.** This remains nonnegotiable for novelty assessment.
2. **Broaden the exact novelty audit of the all-dimensional contraction theorem.** Compare the map-specific kernel formula, not merely the surrounding representation machinery.
3. **Replace or strengthen the second example.** The polar-Fitting family is a valid proof-of-concept, but it is too deliberately coefficient-encoded to carry the conceptual-generalization burden alone.
4. **Choose one external significance narrative and prove it.** Preferably formulate a recognized Torelli/moduli problem for webs/K3/Reye/Enriques geometry that the new invariant actually resolves.
5. **Reframe the structural theorem as a criterion unless a wider natural class is proved.**
6. **Make the few local proof clarifications listed in Section 7.**
7. **Keep the 37-page article as the submission object.** The supplement and archival compilation should remain supporting material.
8. **Do not convert unresolved literature questions into negative novelty claims.** The current honesty on this point should be preserved.

## 11. Final assessment

Revision 137 is a substantive mathematical improvement over revision 136. The scheme-level Fano argument, the common-coordinate descent, and the full orthogonal harmonic lemma now meet the standard I asked for in the previous report. The central four-dimensional reconstruction theorem is no longer blocked, in my reading, by an obvious local proof defect.

That is not enough for a general top-four journal.

The remaining difficulty is now the one such journals care about most: whether the theorem is both historically new and conceptually important enough to justify the venue. The closest historical failure-locus source is still unread at theorem level. The new arbitrary-dimensional polar family is mathematically correct but too engineered to establish, by itself, that the nonreduced reconstruction mechanism is a broad natural phenomenon. The all-dimensional contraction theorem is promising, but its exact novelty has not yet been audited at the depth appropriate for a principal significance claim.

Accordingly, my recommendation is **reject in the present form**, with a materially more positive mathematical assessment than for v136. If the priority comparison, natural second application, and external significance case are closed, this manuscript would merit a genuinely fresh referee round rather than another incremental rereview.
