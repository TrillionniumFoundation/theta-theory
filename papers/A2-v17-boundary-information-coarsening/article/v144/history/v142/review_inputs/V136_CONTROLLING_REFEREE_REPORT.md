# Referee report on A2 revision 136

## Manuscript and review scope

**Manuscript:** *Intrinsic reconstruction of webs from nonreduced multiplication-failure schemes*  
**Author:** Qian Qi  
**Reviewed revision branch:** revision/a2-v136-functorial-support-reconstruction-2026-09-23  
**Reviewed branch head:** 731729b9e391b507d27994f6db8d71d61cfca577  
**Source commit recorded by the build receipt:** 6827ef5933a66fc920a9cb39737e4597e5561f19  
**Predecessor revision:** revision/a2-v135-structural-support-proof-2026-09-23, base commit 003fb13458c8ed11e2973963493a662f31c700c0  
**Controlling predecessor report recorded by v136:** 9fb3a5b9b27d4f6c6df2f3e557b4fc709c3a546d  
**Companion predecessor report recorded by v136:** 9f246bef692ee715851c4b200041c5cfe76da7d9  
**Review standard:** external-referee-style assessment at the level of a general top-four mathematics journal.

This is an owner-requested, AI-assisted referee-style report, not a journal-commissioned decision. I reviewed the focused v136 proof spine, the new dimension-uniform contraction/support section, the deepest-normal-cone reconstruction argument, the universal Schur readout, the common-projective-transformation descent, the intrinsic residual-colon construction, the literature audit, the response to the two v135 reports, and the source-bound build receipt. I also checked the exact finite-verification script that accompanies the new all-dimensional theorem. The computational evidence is treated as evidence for calculations only, not as a substitute for the written proofs.

## Recommendation

**Reject in the present form at a general top-four journal.**

This recommendation is substantially different in character from the earlier v135 rejection. Revision 136 makes real mathematical progress. I no longer see an obvious representation-theoretic obstruction to the central smooth-locus reconstruction theorem, and I did not find a direct counterexample to the claimed implication

\[
\widehat D_R \simeq \widehat D_{R'}
\quad\Longrightarrow\quad
R'=gR,\qquad g\in\operatorname{PGL}(V),
\]

on the stated smooth-Jacobian locus.

The two most delicate intrinsic transitions flagged in v135 have also been materially repaired: the manuscript now gives a bundle-theoretic oriented-Segre descent intended to produce one constant projective transformation, and it replaces informal division by a determinant equation with an intrinsic graded colon construction. The new all-dimensional contraction theorem is not a cosmetic significance paragraph; it is a genuine theorem with a written proof.

Nevertheless, I would not recommend acceptance, nor would I classify the remaining work as a routine major revision. Three top-level problems remain.

1. The manuscript itself records that the complete theorem-level comparison with Ballico 1993 is still open, so a close historical priority question has not been cleared.
2. The new all-dimensional theorem generalizes the component-pair recombination mechanism, but not the deepest geometric step of the paper: intrinsic extraction of that component pair from an abstract nonreduced failure scheme. Thus the flagship geometric inverse theorem remains essentially four-dimensional.
3. Because the all-dimensional contraction theorem now carries much of the manuscript's claim to conceptual breadth, its novelty boundary needs a considerably broader theorem-level literature audit than the present comparison with the ambient skew-flattening literature.

In addition, two scheme-theoretic descent steps remain compressed enough that I would require them to be rewritten before treating the main theorem as fully referee-auditable.

## 1. What revision 136 genuinely fixes

The authors should receive credit for responding to the previous reports with mathematics rather than rhetoric.

### 1.1 The direct exterior literature comparison is now correctly delimited

The manuscript now explicitly attributes the ambient exterior-support/enclosing-space formalism and the secant containment to Landsberg--Ottaviani and Sheridan. It no longer presents exterior support, the first skew flattening, or the support bound for a Grassmannian secant as new. The claimed additional content is narrowed to the restriction of contraction to the specified determinant-twisted Jacobian component, the exact kernel by bilinear rank and parity, the induced support table, and the reconstruction consequence.

That is a much more credible novelty statement than the one in v135.

### 1.2 The significance objection received an actual theorem

Section sec:uniform-support introduces, for dim V=n,

\[
j_n:\det V\otimes\operatorname{Sym}^nV
   \longrightarrow \bigwedge^n\operatorname{Sym}^2V
\]

and proves the asserted kernel formula for every nonzero symmetric bilinear form q:

\[
\ker(\iota_q j_n)=
\begin{cases}
\det V\otimes\operatorname{Sym}^n(\operatorname{rad}q),
   &q\text{ singular},\\
0,&q\text{ nondegenerate and }n\text{ odd},\\
\det V\otimes\mathbf C(q^{-1})^{n/2},
   &q\text{ nondegenerate and }n\text{ even}.
\end{cases}
\]

The manuscript then derives the exact support formula and, for n at least four and at least three essential variables, a support gap above 2n. This gives uniqueness of the Grassmannian point on the line determined by the two canonical complementary projections.

I checked the logic of the shear reduction, the cofactor cancellation, the harmonic nonvanishing coefficient, and the support-to-secant implication. I did not find a simple contradiction. The accompanying exact script checks all bilinear ranks for n=2 through 7 and explicitly states that it does not certify the general proof.

### 1.3 The common-g issue is substantially improved

The new oriented relative Segre descent is the right kind of repair. It recognizes that a fibrewise collection of projective transformations is not enough and attempts to prove regularity of the projective-bundle map before invoking projectivity of the Grassmannian base and affineness of PGL. It also tracks the possible line-bundle twist of linear lifts.

Likewise, the revised common-g lemma now uses the normal-cone grading, the oriented ruling, the universal coefficient square, and the residual ideal in a single functorial chain.

### 1.4 Determinant division has been replaced by an invariant operation

The construction

\[
\mathcal J=(\mathcal I:\mathcal D),
\qquad
L=\mathcal D_4,
\qquad
L\otimes\mathcal J_{12}\simeq\mathcal I_{16},
\]

is conceptually the correct replacement for choosing and dividing by a scalar determinant equation. The manuscript also carefully limits the base-change statement: on a nonreduced new base, the determinant ideal is transported rather than recomputed as an absolute reduction. This is the kind of scope discipline a difficult scheme-theoretic inverse argument needs.

## 2. The central four-dimensional proof is now internally coherent enough to deserve serious consideration

The proof architecture is much clearer than it was in earlier revisions.

First, the reduction of the failure scheme is used to recover the Schubert rank strata by iterated reduced singular loci, ending at

\[
\Sigma_0(R)=\operatorname{Gr}(4,S_R).
\]

Second, the normal cone along this deepest stratum has fibre ideal d(T)J_R(T), with reduced determinant hypersurface. Iterating singular loci in the determinant cone recovers the rank-one Segre geometry, and the relative ruling is oriented by distinguishing the projectively trivial P(V)-ruling from the nontrivial projectivization of the tautological bundle.

Third, the nonreduced degree-sixteen ideal is converted by the intrinsic colon into the degree-twelve maximal-minor coefficient module. The universal Cauchy/Schur coefficient map then recovers the two left component lines, with exterior duality identifying them with the two Pluecker components.

Fourth, the Jacobian component has exterior support at least nine as soon as the quartic has at least three essential variables. A sum of two decomposable four-vectors and every tangent vector to Gr(4,10) have support at most eight. This excludes a second point, a doubled point, a pure endpoint, and a whole Grassmannian line on the component pencil. A smooth quartic has four essential variables, so the reconstruction open equals the full smooth-Jacobian locus.

As a mathematical story, this is now coherent. In particular, I do not regard the old v135 objections about the support gap or the informal determinant division as still open in their previous form.

That said, coherence is not yet the same as a top-four acceptance case.

## 3. Blocking issue B136.1: the Ballico 1993 comparison is still explicitly open

The manuscript's own ISSUE_MATRIX.json says:

- all_referee_issues_closed: false;
- Ballico_1993_full_text_obtained: false;
- priority_certified: false.

The literature audit is admirably honest. It records inspection of the publisher's first page of E. Ballico, *On the Failure Locus of Higher Order Properties of Embeddings in Projective Spaces*, Math. Nachr. 163 (1993), 5--13, and explicitly refuses to infer theorem-level nonanticipation from that first page.

That is the correct scholarly stance, but it leaves a real problem for a top-four recommendation.

The present paper is built around a nonreduced multiplication-failure scheme, higher-order failure geometry, Fitting structure, and inverse reconstruction. A historical paper with “failure locus” and higher-order embedding properties in its title is close enough in vocabulary and subject that a referee should not certify novelty while the relevant theorem statements remain unread.

I am not claiming that Ballico anticipated the present result. I am claiming the opposite kind of uncertainty: the current evidence is insufficient to decide.

Before a new top-four submission, I would require the authors to obtain the complete paper through a legitimate library, archive, or interlibrary-loan route and compare exact statements along the six axes they have already identified:

1. parameter spaces;
2. reduced locus versus determinantal/Fitting scheme structure;
3. the varied multiplication or higher-order maps;
4. infinitesimal, nilpotent, colon, or normal-cone data;
5. relative and base-change assertions;
6. inverse or reconstruction results.

The comparison should quote theorem numbers and hypotheses, not merely summarize subject matter. If Ballico is remote from the present theorem, a complete comparison will strengthen the paper. If there is overlap, the paper needs to say exactly where the new contribution begins.

For a general top-four venue, I do not regard an explicitly open priority question of this proximity as a minor editorial matter.

## 4. Blocking issue B136.2: the new all-dimensional theorem does not generalize the deepest geometric mechanism

Revision 136 responds to the previous “four-dimensional accident” criticism by proving a genuine theorem for every n. This is valuable, but the manuscript slightly overstates how much of the original inverse problem has become uniform.

The all-dimensional theorem begins with canonical maps

\[
j_n,\qquad C_n,\qquad
Q_n=\tfrac12j_nC_n,\qquad P_n=1-Q_n
\]

and proves that, on a nonempty open subset of Gr(n,Sym^2 V), the pair of projective component lines

\[
([P_nw],[Q_nw])
\]

determines the original Grassmannian point.

This is a clean inverse statement about a canonically projected Pluecker vector.

It is **not** an all-dimensional theorem saying that an abstract nonreduced multiplication-failure scheme intrinsically recovers those two lines. The manuscript correctly acknowledges this in Remark rem:uniform-versus-intrinsic. The difficult geometric input -- deepest failure stratum, oriented normal cone, residual coefficient readout, and one common projective coordinate transformation -- remains proved only in dimension four.

This distinction matters for significance. The central theorem of the paper is not merely “two projections determine a decomposable vector.” It is that an abstract nonreduced scheme arising from a cube-zero algebra determines the original relation web. The all-dimensional section generalizes the last recombination stage but not the nonreduced-scheme reconstruction stage.

At a specialized journal, the uniform representation-theoretic theorem could be a strong conceptual supplement. At a general top-four journal, I would still want one of the following.

### Route A: a genuinely uniform failure-scheme theorem

Construct the analogue of the multiplication-failure scheme and show, for a class of dimensions or Hilbert functions, that its intrinsic normal-cone data functorially recovers the canonical component pair. The theorem need not be as sharp in every n, but it should generalize the actual geometric mechanism rather than only the final secant exclusion.

### Route B: an abstract structural theorem

Formulate a reusable criterion: for a class of graded Artin algebras or determinantal failure schemes, specify intrinsic hypotheses on the deepest normal cone and its residual coefficient module that force reconstruction of the original relation space. Then show that the (1,4,6) web problem is a significant instance and that at least one genuinely different family also fits the criterion.

### Route C: a major independent geometric consequence

If dimension four is intrinsically exceptional, the paper should connect the theorem to a recognized moduli or Torelli problem strongly enough that the exceptional case itself is a field-level result. The current Reye/K3 discussion is interesting, but the manuscript still reads primarily as a sophisticated internal reconstruction theorem.

Revision 136 has weakened the “isolated plethysm accident” objection. It has not eliminated the gap between a broad linear-algebra mechanism and a broad nonreduced-geometric reconstruction theory.

## 5. Blocking issue B136.3: the novelty audit of the uniform contraction theorem is not yet commensurate with the role that theorem now plays

The v136 literature section correctly compares its support language with Landsberg--Ottaviani and Sheridan. Those are the direct ambient skew-flattening references requested by the previous report.

But the new theorem is stronger and more specialized than an ambient support statement. Its core assertion is an exact formula for the kernel of contraction after restricting to the canonical copy of

\[
\det V\otimes\operatorname{Sym}^nV
\subset
\bigwedge^n\operatorname{Sym}^2V,
\]

including the singular-radical formula and the full-rank parity exception.

Because this theorem is now the principal evidence that the method is not dimension-specific, its historical boundary needs more than a comparison with papers whose stated purpose is exterior subspace varieties.

I would require a theorem-level search and discussion covering the representation-theoretic neighborhood of this map: classical decompositions of exterior powers of symmetric squares, orthogonal harmonic tensors, contraction/interior-product maps on these plethysm components, determinant/Jacobian polarization covariants, and related invariant-theoretic identities. The authors need not prove that no one ever wrote an equivalent formula, which is impossible. They do need to show a serious search of the mathematically closest representation-theoretic sources and explain whether the kernel theorem is:

- genuinely new as stated;
- a known branching or multiplicity-one consequence written in new coordinates;
- or a new geometric use of a standard representation-theoretic fact.

The present audit says, correctly, that the inspected Landsberg--Ottaviani and Sheridan passages do not contain the theorem. That is necessary but not sufficient for a top-four novelty case.

Again, this is not an assertion that the theorem is known. It is a statement that the present manuscript has not yet established the scholarly boundary of the theorem on which its new conceptual breadth depends.

## 6. Serious issue S136.1: the relative Fano scheme of maximal rank-one subspaces needs a complete scheme-theoretic proof

Lemma lem:oriented-segre-descent is the right lemma to prove, but one passage is still too compressed for the amount of weight it carries.

The manuscript states that the relative parameter scheme of maximal n-dimensional linear subspaces contained in the rank-one cone is

\[
(\mathbf P(V)\times B)\ \sqcup\ \mathbf P(\mathcal U^*),
\]

as schemes, not merely on points. It then gives the point classification and a linearized-minor tangent calculation at the two expected families, and concludes that the components have precisely the displayed smooth projective-space scheme structures.

This is plausible and very likely repairable. I am not presenting it as a counterexample. But for the main theorem, “very likely” is not enough.

The authors should explicitly define the relevant closed relative Fano/Grassmann parameter scheme and prove that the two natural morphisms from the displayed projective bundles give an isomorphism onto it. In particular, the proof should make explicit why the tangent calculation rules out:

- nilpotent thickening of either component;
- embedded infinitesimal components;
- additional associated structure over special base points;
- any failure of the claimed identification under base change.

A clean way to do this would be to prove that the two displayed maps are closed immersions, that their images cover every geometric point, and that the local rings of the target have the expected dimension and tangent dimension, hence are regular along those images. If that is the intended argument, it should be written as such rather than left implicit.

This matters because the regular PGL-valued morphism, and therefore the one-common-g conclusion, is built on this relative parameter scheme.

## 7. Serious issue S136.2: make the normal-cone-to-common-g functorial chain completely explicit

The common-g lemma is much improved, but it is still the point at which a skeptical reader will look hardest.

The manuscript should isolate one diagram showing the entire intrinsic chain:

\[
\widehat D_R
\rightsquigarrow
\Sigma_0(R)
\rightsquigarrow
\operatorname{gr}_{\mathcal I}\mathcal O_{\widehat D_R}
\rightsquigarrow
\operatorname{Sym}(\mathcal I/\mathcal I^2)
\rightsquigarrow
\text{rank-one ruling parameter scheme}
\rightsquigarrow
\mathbf P(V)\times\Sigma_0(R)
\rightsquigarrow
g\in\operatorname{PGL}(V).
\]

For every arrow, the manuscript should state precisely what is functorial under an abstract scheme isomorphism, and what is reconstructed only after choosing a local frame. In particular:

- the degree-one vector bundle should be identified before choosing the tensor-factor decomposition;
- the oriented ruling should be shown to reconstruct the left projective factor intrinsically;
- the line-bundle ambiguity of linear lifts should be tracked through the coefficient functors;
- the right-factor change should be visibly confined to the right Cauchy factor;
- the common determinant twist in exterior duality should be shown once in the same diagram.

Most of these ingredients are already present in v136. My objection is auditability, not a detected contradiction. At the top-four level, however, this is the central functorial bridge and should be presented so that there is no opportunity for an unspoken choice of coordinates to enter.

## 8. Serious issue S136.3: the all-dimensional harmonic representation step needs a pinpoint reference or a self-contained lemma

The nondegenerate part of Theorem thm:uniform-contraction uses the harmonic decomposition

\[
\det V\otimes\operatorname{Sym}^nV
=
\bigoplus_t
\det V\otimes \rho^t\mathcal H_{n-2t},
\]

and then uses that the summands are irreducible and pairwise inequivalent for the full orthogonal group, including the disconnected low-dimensional cases. This is exactly what allows nonvanishing on each positive harmonic summand to imply injectivity there and prevents cancellation between summands.

The manuscript discusses the n=2 reflection issue and gives the highest weights for n at least three, but the citation to Fulton--Harris is too broad for this exact full-O_n statement and its determinant twist.

Please either:

1. give a precise theorem/proposition reference for the harmonic decomposition and full orthogonal irreducibility used here, including the n=2 convention; or
2. isolate a short representation lemma and prove exactly the version needed.

The finite exact checks for n up to seven are useful regression tests, but they do not address this infinite-dimensional-in-n representation-theoretic hinge.

I do not currently see evidence that the statement is false. I do think the proof should not ask a referee to reconstruct the full-O_n representation argument from a general textbook citation.

## 9. The manuscript must continue to distinguish reduced support statements from scheme-theoretic statements

Revision 136 is careful here, and that care should be preserved.

The pullback identities for exterior support loci are stated only as identities of reduced closed subvarieties. The manuscript does not claim that the pulled-back skew-flattening minors generate radical ideals or that the scheme-theoretic multiplicities are understood.

That limitation is appropriate. Do not strengthen those statements merely to make the theorem look more scheme-theoretic. The main inverse theorem does not require such a strengthening.

Similarly, the ambient binary-Jacobian obstruction is only a containment of support; it is not a classification of all components of the rank-defect scheme. The current manuscript says this. Keep it.

## 10. The top-four significance case remains underdeveloped even after the uniform theorem

The strongest parts of the paper now form an attractive package:

- intrinsic extraction of two Pluecker components from nonreduced normal-cone data in dimension four;
- an exact contraction/support theorem;
- a support gap excluding secant and tangent recombination;
- separation of the finite web-to-K3 ambiguity.

But the manuscript still spends substantial energy on its own revision history, archival boundary theory, and evidence infrastructure. Those materials are valuable for reproducibility, but they do not themselves establish field-level significance.

For an actual top-four submission, I would ask the authors to state, in mathematical rather than programmatic terms, which established problem is solved and why experts outside this eleven-paper pipeline should care. In particular:

- Is the main result a Torelli theorem for a natural moduli problem?
- Is it the first theorem showing that a nonreduced Fitting failure scheme recovers a defining algebra where the reduced failure locus does not?
- Is it a new general principle for extracting hidden representation components from infinitesimal determinantal structure?
- Does it settle a previously recognized ambiguity in the geometry of webs, Reye congruences, or quartic K3 surfaces?

The paper currently contains pieces of all four narratives. It needs to choose and substantiate one as the primary significance claim.

The new all-n theorem helps, but a general top-four journal will still ask whether the main geometric theorem changes how experts think about a recognized class of inverse or moduli problems, rather than merely solving a technically difficult reconstruction problem designed by the paper itself.

## 11. Reproducibility and computational evidence

The v136 source-bound evidence is unusually disciplined.

The BUILD_RECEIPT records:

- a 30-page focused article;
- a 66-page supplement;
- a 92-page complete archival manuscript;
- a GitHub Actions execution environment and run id 35834394351;
- successful reference, citation, label, source-hash, and PDF-bounds checks;
- eleven exact scripts;
- the new finite contraction checks for n=2 through 7 at every bilinear rank;
- explicit disclosure of what is not machine-certified.

The finite checker also correctly distinguishes modular lower-rank certification from exact exhibited kernels and does not claim to prove the theorem for arbitrary n.

This is good practice.

I did not treat the receipts as formal verification of the structural lemmas. In particular, they do not certify the oriented relative Segre descent, the arbitrary-base colon statement, the full orthogonal representation argument, the historical priority claims, or the intrinsic normal-cone reconstruction. The manuscript itself makes the same distinction.

For a journal submission, the 30-page focused article should remain the primary manuscript. The 92-page archival compilation should not be the object an editor must parse to understand the theorem.

## 12. Further technical and editorial comments

1. The phrase “for every n at least four” should always be attached to the component-pair inverse theorem, not to the abstract failure-scheme reconstruction theorem. The current remark makes this distinction; the abstract and introduction should remain equally precise.

2. The uniform theorem would benefit from one explicit non-diagonal higher-dimensional example. The diagonal web proves nonemptiness, but a second family would make the geometry of the open set less formal and help distinguish the theorem from a single torus-fixed witness plus openness.

3. In the singular contraction proof, the stabilizer argument is elegant. Please state explicitly that the shear subgroup and the B-scaling torus preserve q and that the determinant character only changes the listed weight. These facts are implicit, but they are exactly what validates the invariant-subspace descent.

4. The cofactor-divergence proof is one of the cleanest new arguments in the paper. It deserves to be highlighted as a lemma of independent interest if it is genuinely new, or compared with a classical identity if it is standard.

5. The abstract is currently overloaded with the entire historical architecture of the paper. A top-four abstract should state the main reconstruction theorem, the uniform contraction theorem, and the geometric mechanism, but omit most implementation detail about supplements and residual archives.

6. The paper should retain the explicit statement that Ballico 1993 has not been fully inspected until that comparison is actually completed. Do not convert an unresolved documentary problem into a negative novelty claim.

7. The current treatment of the exact finite checks is appropriately subordinate to proof. Keep it that way.

## 13. Required work before I would support a fresh top-four review

I would require all of the following.

1. **Complete the Ballico 1993 comparison.** Obtain the full article and compare theorem statements, hypotheses, and constructions along the six recorded axes.

2. **Broaden the novelty audit for the all-dimensional kernel theorem.** Compare with the closest classical and modern representation-theoretic literature, not only ambient exterior-subspace references.

3. **Close the conceptual-generalization gap.** Either generalize the intrinsic failure-scheme readout beyond dimension four, formulate a reusable abstract reconstruction criterion with more than one substantive example, or supply a much stronger established-moduli consequence for the four-dimensional theorem.

4. **Strengthen the relative rank-one Fano-scheme lemma.** Prove the scheme-level identification of the two ruling parameter spaces with all nilpotent/embedded possibilities explicitly excluded.

5. **Present the common-g reconstruction as one fully functorial diagram.** Make every passage from an abstract scheme isomorphism to the two recovered coefficient lines transparent and choice-free.

6. **Pin down the orthogonal harmonic representation input.** Add a precise source or a self-contained lemma for the full-O_n irreducibility and multiplicity-free harmonic decomposition actually used.

7. **Keep the focused paper focused.** Submit the 30-page reconstruction article as the main object and keep the long historical/primary-boundary material genuinely supplementary.

8. **Rewrite the significance discussion around an external mathematical problem.** The paper should explain why this theorem matters independently of its internal revision pipeline.

## 14. Final assessment

Revision 136 is a serious improvement. It is the first version I have seen in this line where the central four-dimensional reconstruction proof, the Schur-support obstruction, the common-coordinate issue, and the residual ideal can plausibly be read as one coherent theorem rather than as a collection of partially connected repairs.

I did not find a fatal counterexample to the smooth-locus reconstruction theorem during this pass.

That is not enough for acceptance at a general top-four journal.

The paper still has an explicitly unresolved close historical source, its newly uniform theorem does not yet generalize the intrinsically nonreduced geometric heart of the argument, and the novelty of that uniform theorem has not been audited broadly enough for the role it now plays. In addition, the relative ruling parameter scheme and the normal-cone-to-common-g chain should be rewritten to a standard where a skeptical algebraic geometer can verify every functorial step without reconstructing omitted scheme-theoretic arguments.

My recommendation is therefore **reject in the present form**, with the view that a substantially revised manuscript could merit a fresh external assessment if the priority, conceptual-generalization, and functoriality issues above are genuinely closed. I would not describe the remaining work as minor, and I would not treat the current computational evidence as a substitute for it.
