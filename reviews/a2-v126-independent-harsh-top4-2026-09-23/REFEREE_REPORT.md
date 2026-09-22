# Independent harsh top-four referee report — A2 revision 126

**Manuscript:** *Canonical nilpotent specialization, stratified contact algebra, and polarized reconstruction in multiplication failure*  
**Author:** Qian Qi  
**Repository:** TrillionniumFoundation/theta-theory  
**Reviewed revision:** revision/a2-v126-global-nilpotent-specialization-2026-09-23  
**Reviewed revision head:** 2566944ed07c77a58b2025fd212b2a70396a6e87  
**Parent mathematical revision:** revision/a2-v125-stratified-nilpotent-contact-boundary-2026-09-23  
**Controlling previous report:** review/a2-v124-independent-harsh-top4-2026-09-23  
**Principal source:** papers/A2-v17-boundary-information-coarsening/article/v126/geometry.tex  
**Principal PDF:** papers/A2-v17-boundary-information-coarsening/article/v126/geometry.pdf (36 pages according to the v126 build receipt)  
**Date:** 23 September 2026

## Status of this report

This is an owner-requested, AI-assisted external-referee-style report. It was not commissioned by *Annals of Mathematics*, *Inventiones Mathematicae*, *Journal of the American Mathematical Society*, *Acta Mathematica*, or any other journal, and it must not be represented as a journal-issued report.

I reviewed the revision-126 source itself, not merely the response letter, issue matrix, build receipt, or generated PDF. I also checked the inherited v123 and v125 proof blocks that form the actual article, the controlling revision-124 referee report, and the branch-scoped exact-computation evidence. I did not treat issue-matrix labels such as “resolved” as evidence.

# Recommendation

## Reject in the present form at a general top-four mathematics journal.

Revision 126 is mathematically stronger than revision 124, but the decisive new mathematics is largely in revision 125 rather than in the revision-126 centerpiece.

Revision 125 proves a useful global residual-colon description of the nilpotent filtration and materially advances the rank-two boundary analysis. It proves that the fixed vertex component remains genuinely primary through the mixed-regular contact-collision boundary, treats the containment case \(h_H\equiv0\), and computes the first transverse decomposable mixed-kernel wall. Those are real improvements and should not be recycled as unresolved objections.

The new mathematical centerpiece of revision 126 is the extended Rees algebra of the nilradical
\[
\mathscr R_{\mathcal N}
=
\mathcal O_{\widehat D}[t,\mathcal N t^{-1}]
\subset
\mathcal O_{\widehat D}[t,t^{-1}],
\]
which gives a flat family with generic fibre \(\widehat D\) and special fibre
\[
\operatorname{Spec}_{\widehat\Delta}
\operatorname{gr}_{\mathcal N}\mathcal O_{\widehat D}
=
C_{\widehat\Delta/\widehat D}.
\]

I agree with this construction and with the flatness argument. The problem is not that the theorem is false.

The problem is that this is the standard deformation-to-the-normal-cone/Rees construction for a closed immersion, applied to the intrinsic nilradical. It canonically packages the filtration already described in v125, but it does not geometrically determine the unknown graded pieces on the higher-corank and rank-drop strata. The revision therefore turns an incompletely classified filtration into one canonical family and then treats the existence of that family as if it were the missing all-boundary structure theorem.

For the paper's top-four claim, the distinction is decisive:

> **A deformation to the normal cone packages a filtration; it does not compute the filtration.**

The controlling v124 report's Option C did not ask merely for the existence of a Rees algebra. It contemplated a Rees/normal-cone replacement whose graded pieces are identified on explicit Schubert/contact strata and whose specialization controls every boundary. Revision 126 supplies the universal formal mechanism but still does not identify the schemes \(W_j\) on the major exceptional loci that motivated the objection.

Accordingly, I do not accept the v126 issue matrix's labels “resolved-by-global-rees-option-C” for E124.1 or “resolved-by-specialization” for E124.2 as top-four-level mathematical closure.

# 1. What has genuinely improved since revision 124

A fair report must separate the substantial v125 advances from the comparatively formal v126 addition.

## 1.1 The global residual-colon filtration is useful

Revision 125 proves on the whole Grassmannian that
\[
\mathcal I_{\widehat D}
=
\mathcal I_{\widehat\Delta}\,
\mathcal J^{\mathrm{res}},
\qquad
\mathcal J^{\mathrm{res}}
=
(\mathcal I_{\widehat D}:\mathcal I_{\widehat\Delta}),
\]
and, for \(j\ge1\),
\[
\operatorname{Ann}_{\mathcal O_{\widehat D}}(\mathcal N^j)
=
\frac{
(\mathcal J^{\mathrm{res}}:
 \mathcal I_{\widehat\Delta}^{\,j-1})
}{
\mathcal I_{\widehat D}
}.
\]

With
\[
W_j=
V_{\widehat\Delta}\!\left(
(\mathcal J^{\mathrm{res}}:
 \mathcal I_{\widehat\Delta}^{\,j-1})
+\mathcal I_{\widehat\Delta}
\right)
\]
and
\[
\mathcal L=
\mathcal I_{\widehat\Delta}/
\mathcal I_{\widehat\Delta}^{\,2},
\]
the paper obtains
\[
\mathcal N^j/\mathcal N^{j+1}
\simeq
\mathcal L^{\otimes j}\otimes\mathcal O_{W_j}.
\]

Locally, if the Schubert equation is \(d=\det T\) and
\(\mathcal I_{\widehat D}=dJ\), this becomes
\[
\operatorname{Ann}(N^j)=(J:d^{j-1})/(dJ),
\qquad
N^j/N^{j+1}
\simeq
A/\bigl((d)+(J:d^{j-1})\bigr).
\]

This is an exact and useful reduction of the nilpotent filtration to a tower of residual colons. It is genuinely stronger than the revision-124 presentation-only statement.

But the theorem itself correctly says what remains: one must identify the colon schemes \(W_j\) geometrically on the successive rank strata. That is still the principal structural problem.

## 1.2 The repeated-contact primary structure is now substantially stronger

On the mixed-regular projection-corank-two locus, v125 proves
\[
J=I_H\cap\mathfrak m^3
\]
and
\[
\mathcal I_{\widehat D}
=
\delta I_H\cap\mathfrak m^5.
\]

This is important. It means the earlier concern that \(\mathfrak m^5\) had merely been written globally as an ideal, without proving that it remains an actual primary component across contact collision, has been answered on the stated mixed-regular locus.

The local repeated-contact law
\[
(\delta^2,\delta q^e,q^{e+1})
\]
is also a genuine scheme-theoretic refinement, not merely a statement about colliding roots of the contact quartic.

I therefore withdraw the old E124.3 objection in its original form.

## 1.3 The containment case is no longer hidden inside the quartic discriminant

The separate formula
\[
\mathcal I_{\widehat D}
=
\delta^2\mathfrak m
=
(\delta^2)\cap\mathfrak m^5
\]
when \(h_H\equiv0\), together with the identification of the containment locus with the finite reduced Fano scheme of lines on the smooth quartic, is a useful correction.

The manuscript now correctly distinguishes:

- a nonzero quartic with repeated roots;
- and the identically zero quartic, where the contact morphism is no longer finite.

That is exactly the scope correction requested by the prior report.

## 1.4 The first decomposable mixed-kernel wall is a real boundary theorem

The theorem
\[
(J_{\mathrm{dec}}:\delta)
=
(c,d,a^2,ab,b^2)
\]
shows that the second intrinsic-depth support becomes a length-three nonreduced thickening at the transverse decomposable-kernel wall.

This is the kind of theorem the earlier report requested: it extracts actual scheme structure from an exceptional boundary, rather than merely rewriting the universal maximal-minor formula.

The difficulty is that it is only the first such wall.

## 1.5 The paper now distinguishes “presentation” from “structure”

The v125 source explicitly warns that the all-corank block formula is a presentation theorem, whereas associated-prime, collision, and nilpotent-filtration statements require separate hypotheses.

That distinction is mathematically correct and improves the paper.

Revision 126 should preserve it consistently. At present the abstract and response matrix partially undo this gain by giving the standard Rees family more structural force than has been computed.

# 2. Correctness audit of the revision-126 Rees theorem

## 2.1 The local construction is correct

Let \(A\) be the coordinate ring of an affine open of \(\widehat D\), and let \(N\) be its nilradical. The algebra
\[
\mathscr R_N=A[t,Nt^{-1}]
\subset A[t,t^{-1}]
\]
is well defined.

The nilradical and its powers commute with localization, so these local algebras glue.

Because \(\mathscr R_N\) sits inside \(A[t,t^{-1}]\), a nonzero element of \(\mathbf C[t]\) acts injectively. Thus \(\mathscr R_N\) is torsion-free as a \(\mathbf C[t]\)-module. Since \(\mathbf C[t]\) is a PID, torsion-free modules are flat. Therefore the family is flat over \(\mathbb A^1\).

After inverting \(t\),
\[
\mathscr R_N[t^{-1}]
=
A[t,t^{-1}],
\]
so the family is trivial over \(\mathbb G_m\).

Modulo \(t\),
\[
\mathscr R_N/(t)
\simeq
\bigoplus_{j\ge0}N^j/N^{j+1}
=
\operatorname{gr}_N A.
\]

Since \(N\) is the ideal of the reduction \(\widehat\Delta=(\widehat D)_{\mathrm{red}}\) inside \(\widehat D\), the special fibre is exactly the normal cone
\[
C_{\widehat\Delta/\widehat D}.
\]

An abstract scheme isomorphism preserves the nilradical, so the construction is functorial under abstract isomorphisms.

I do not find a mathematical contradiction in this proof.

## 2.2 The construction is standard, not a new general theorem

The article should cite the classical deformation-to-the-normal-cone construction explicitly.

For a closed immersion defined by an ideal \(I\), the graded algebra
\[
\bigoplus_{n\ge0}I^n/I^{n+1}
\]
defines the normal cone, and the extended Rees algebra supplies the standard deformation from the original scheme to that cone.

Appropriate classical references include:

- William Fulton, *Intersection Theory*, Chapter 5, §5.1, “Deformation to the Normal Cone”;
- the Stacks Project, normal cone and associated graded construction, Tag 062Z and surrounding material.

The manuscript-specific contribution is not the existence of the family. It is whatever the authors can determine about \(N\), its powers, the schemes \(W_j\), and the multiplication structure in the associated graded algebra.

That distinction is essential for novelty.

## 2.3 Forming the Rees family does not add the missing higher-corank geometry

Revision 125 already gives
\[
\operatorname{gr}_N\mathcal O_{\widehat D}
\simeq
\mathcal O_{\widehat\Delta}
\oplus
\bigoplus_{j\ge1}
\mathcal L^{\otimes j}\otimes\mathcal O_{W_j}.
\]

Revision 126 observes that this graded algebra is the special fibre of a canonical flat family.

The unknown geometry has not disappeared. It is still concentrated in the unknown \(W_j\)'s and in the multiplication maps among the graded pieces on the exceptional strata.

The Rees construction therefore provides a canonical container, not the missing classification.

# 3. Decisive blocker E126.1 — Option C has been met formally, not substantively

The v124 report explicitly allowed a global Rees/normal-cone route instead of an exhaustive primary-decomposition table.

But the intended theorem had two parts:

1. produce an intrinsic graded/Rees object;
2. identify its graded pieces on explicit Schubert/contact strata and prove that the specialization controls the actual boundary geometry.

Revision 126 establishes the first part.

It establishes the second part only on:

- projection corank one;
- the mixed-regular rank-two locus;
- mixed-regular repeated-contact collisions;
- the mixed-regular containment case;
- and the first transverse decomposable mixed-kernel wall.

The statement in the response letter that every projection corank and rank-drop locus lies in one global special fibre is formally true but does not answer the structural question.

Every point must lie in the normal cone of the reduction once that normal cone is formed. The hard issue is what the cone is at that point.

### Required closure

A top-four revision should geometrically determine the \(W_j\) and their multiplicative maps on a canonical stratification.

For each relevant stratum it should state:

- which \(W_j\) are nonempty;
- their radicals and scheme structures;
- their dimensions and multiplicities;
- the nilpotency index;
- the associated primes of the failure scheme;
- and the multiplication maps
  \[
  (N^i/N^{i+1})\otimes(N^j/N^{j+1})
  \longrightarrow
  N^{i+j}/N^{i+j+1}.
  \]

That would turn the Rees object into a genuine all-boundary structure theorem.

# 4. Decisive blocker E126.2 — major exceptional strata remain uncomputed

The manuscript still does not classify the loci on which the mixed-regular hypotheses fail, except for one transverse decomposable-kernel wall.

## 4.1 Rank drop of \(A_H\)

The mixed-regular theorem assumes that
\[
A_H:\operatorname{Sym}^2H\to S_R
\]
is injective.

When this rank drops, the elimination leading to the standard residual matrix changes. The manuscript does not compute the residual ideal, associated primes, nilpotency index, or \(W_j\)'s there.

The Rees construction does not change this.

## 4.2 Rank drop of the mixed map

The theorem also assumes that
\[
\overline B_H:
H\otimes(V/H)\to S_R/\operatorname{im}A_H
\]
is surjective with one-dimensional kernel.

The paper computes the transition from a rank-two generator of that one-dimensional kernel to a decomposable generator.

It does not classify:

- failure of surjectivity;
- kernel dimension greater than one;
- intersections of those rank conditions with contact collisions;
- or nontransverse versions of the decomposable wall.

Those are natural places for new embedded components and larger nilpotency indices to appear.

## 4.3 Projection corank three

The all-corank block formula is valid, but the paper does not identify the special-fibre strata, associated primes, nilpotency depth, or local Hilbert functions.

Thus “corank three lies in the same Rees family” is only a formal statement.

## 4.4 Projection corank four

The same objection applies at projection rank zero.

The manuscript supplies an exact block presentation but no structure theorem for the corresponding residual scheme.

## 4.5 Deeper nilpotent layers remain formal

The colon formula gives
\[
\text{nilpotency index}
=
1+\min\{k\ge0:d^k\in J\}
\]
on a Schur chart.

That is useful, but outside the computed loci the minimum is not determined.

A theorem advertised as global nilpotent specialization should not leave the depth on the deepest strata as an unspecified ideal-membership problem.

# 5. Decisive blocker E126.3 — the headline scope is overstated

The abstract says:

> “Across the first singular Schubert boundary we compute that special fibre explicitly.”

This is too broad.

What is explicitly computed is a substantial but proper subset of that boundary:

- mixed-regular rank two;
- its contact-collision strata;
- the containment case;
- and one transverse decomposable mixed-kernel wall.

The first singular Schubert boundary also contains the \(A_H\)-rank-drop and mixed-rank-drop loci and other exceptional kernels.

The response letter similarly uses the existence of one Rees family to mark E124.1 and E124.2 resolved.

The correct top-level wording would be something like:

> the Rees construction canonically places every projection-rank stratum in one deformation; the graded geometry is determined completely on corank one and on the specified mixed-regular and first-wall portions of corank two.

That is an accurate and still meaningful theorem.

# 6. Decisive blocker E126.4 — Ballico 1993 remains an unresolved priority boundary

The manuscript handles this limitation responsibly.

The bibliography identifies:

E. Ballico, *On the Failure Locus of Higher Order Properties of Embeddings in Projective Spaces*, *Mathematische Nachrichten* **163** (1993), 5–13, DOI 10.1002/mana.19931630102.

The response records that the currently available Wiley endpoint supplies metadata and first-page access but not the complete theorem text. It does not manufacture a non-anticipation claim from metadata.

That is correct scholarly practice.

It does not, however, close the priority problem for a top-four journal.

The earlier title and historical line are close enough to the present “failure scheme” framework that the complete predecessor should be read before the journal is asked to certify exceptional novelty.

This is not an assertion that Ballico anticipates the paper. Without the theorem text I cannot responsibly make that assertion.

The point is that the present record is insufficient to certify the opposite assertion either.

### Required action

Obtain the complete 1993 article through a research library, interlibrary loan, author archive, or direct author contact and compare theorem by theorem:

- the definition of the failure locus;
- the parameter Grassmannian;
- the multiplication/evaluation map;
- whether scheme structure is retained;
- whether Fitting ideals appear;
- whether embedded or nonreduced components are studied;
- whether higher-order failure produces a filtration or normal cone;
- and whether geometric data are reconstructed from the failure object.

Until then I would not sign off on the historical-priority portion of a top-four report.

# 7. Major issue M126.1 — the Torelli monodromy theorem is largely formal

Revision 125 improves the inverse-problem discussion by replacing a vague finite ambiguity with a finite étale map after shrinking:
\[
\tau:\mathcal W^\circ\to\mathcal K^\circ,
\qquad
\deg\tau=
[\mathbf C(\mathcal W):\mathbf C(\mathcal K)].
\]

The transitivity of geometric monodromy is also correctly stated.

But once the paper already knows that the map between irreducible varieties is generically finite in characteristic zero, the existence of a finite étale restriction after deleting branch and nonflat loci is standard.

Likewise, connectedness/irreducibility gives transitivity of the generic monodromy action.

The substantive inverse problem remains:

- What is \(d_{\mathrm{Tor}}\)?
- Is \(d_{\mathrm{Tor}}=1\)?
- If not, what is the monodromy group?
- Which compatible Enriques/Reye structures form the fibre?
- Do deeper nilpotent strata separate the fibre?
- Where does the degree jump?

Thus the theorem is a clean formalization of generic finiteness, not yet a classification of the finite packet.

# 8. Major issue M126.2 — the significance assessment must subtract standard geometry as well as classical geometry

The manuscript has correctly stopped treating the classical nine-dimensional Reye locus as a novelty signal.

The same discipline should now be applied to deformation to the normal cone.

For significance purposes one should subtract:

1. classical Reye/nodal-Enriques geometry;
2. the classical nine-dimensional moduli framework;
3. the standard Rees/deformation-to-normal-cone mechanism;
4. the formal finite-étale shrinking of a generically finite map.

The manuscript-specific core then consists approximately of:

- intrinsic reconstruction of the polarized quartic K3 from the nilpotent multiplication-failure scheme;
- the global residual-colon formula;
- the explicit mixed-regular rank-two contact algebra, including collision primary laws and containment;
- and the first decomposable mixed-kernel wall.

That is a coherent and potentially strong specialist result.

For a general top-four venue, however, the paper must show why this package reveals a broader structural principle rather than one intricate determinantal phenomenon for the Hilbert function \((1,4,6)\).

The standard Rees family does not by itself supply that breadth.

# 9. Major issue M126.3 — novelty hygiene for the Rees theorem must be corrected

The revision index calls the Rees specialization the “Principal new theorem.”

I recommend the opposite hierarchy.

## Standard mechanism

For any closed immersion defined by \(I\), the extended Rees algebra gives a flat deformation to the normal cone with special fibre
\[
\operatorname{gr}_I.
\]

This should be cited and stated efficiently.

## Manuscript-specific theorem

For the present multiplication-failure scheme, identify:

- the nilradical;
- its residual-colon filtration;
- the geometric meaning of the supports \(W_j\);
- the multiplication among graded pieces;
- and the specialization of these objects across the multiplication-specific rank strata.

That is where the novelty can lie.

Revision 126 currently gives the standard mechanism more prominence than the manuscript-specific classification.

# 10. Major issue M126.4 — the residual-colon theorem is exact but not yet an all-corank geometric classification

I regard the residual-colon theorem as useful.

But from
\[
\mathcal I_{\widehat D}
=
\mathcal I_{\widehat\Delta}\mathcal J^{\mathrm{res}},
\]
the identities
\[
\operatorname{Ann}(N^j)
=
(\mathcal J^{\mathrm{res}}:
 \mathcal I_{\widehat\Delta}^{j-1})/
\mathcal I_{\widehat D}
\]
and
\[
N^j/N^{j+1}
\simeq
\mathcal L^{\otimes j}\otimes\mathcal O_{W_j}
\]
are colon/cancellation identities.

Their geometric force begins when \(W_j\) is independently identified.

The paper succeeds at that on several rank-two loci. It should not describe the formal definition of \(W_j\) itself as an all-corank classification.

# 11. The polarized reconstruction theorem remains the strongest theorem in the paper

The strongest conceptual result is still the reconstruction theorem inherited from v123.

On the corank-one open, the failure ideal has the exact form
\[
I_D=I_\Delta I_E=I_\Delta\cap I_E^2,
\]
the nilradical is the intrinsic invertible line
\[
N\simeq\mathcal O_E(-\Delta),
\]
and its annihilator recovers \(E\).

The line-bundle calculation
\[
\omega_E\otimes N^{-(p+e-1)}
\simeq
\rho^*\mathcal O_Y(e)
\]
together with
\[
\rho_*\mathcal O_E=\mathcal O_Y
\]
recovers the section ring of \(\mathcal O_Y(e)\). In the K3 case the torsion-free Picard argument then recovers the quartic polarization itself.

This theorem extracts unexpected geometry from the nonreduced failure scheme.

It is conceptually stronger than the revision-126 Rees statement.

If the authors want a top-four case, they should build outward from this reconstruction phenomenon and prove that deeper nilpotent strata supply genuinely new global reconstruction or classification data.

# 12. Computational evidence

The branch-scoped evidence is useful and, importantly, is not oversold in the machine-readable receipts.

The v126 build receipt records:

- a generated PDF;
- no undefined references or citations;
- no LaTeX errors;
- a 36-page principal article;
- and the presence of the Rees theorem.

The exact rank-two regressions record the expected identities for repeated contact, containment, and the decomposable-kernel wall.

The K3 certificate records exact finite witnesses and explicitly says that the general proof machine is not certified.

That is the correct posture.

These calculations are valuable regression checks. They are not independent evidence that the global higher-corank classification has been proved.

I would retain them, but I would not respond to this report by adding more finite test cases. The remaining problems are structural.

# 13. What I would require for top-four reconsideration

A credible next revision should make a mathematical advance beyond the universal Rees construction.

## E126.1 — determine the special fibre, not merely construct it

Give a geometric classification of the \(W_j\) on a canonical stratification of the entire projection-corank-two boundary.

At minimum include:

- \(A_H\)-rank drop;
- failure of mixed surjectivity;
- higher-dimensional mixed kernels;
- decomposable and nontransverse kernel walls;
- collisions of these conditions with the quartic-contact discriminant;
- and the containment-line locus.

For each stratum compute radical, associated primes, nilpotency index, and local Hilbert function.

## E126.2 — extend to projection corank three and four, or prove an equally strong global replacement theorem

If a direct primary-decomposition table becomes unwieldy, an acceptable replacement would identify the entire associated graded algebra on these strata by intrinsic sheaves with explicitly determined supports.

What is not enough is a formula leaving the answer as an unspecified colon ideal.

## E126.3 — prove actual specialization laws between rank strata

The Rees parameter \(t\) specializes \(\widehat D\) to the normal cone of its reduction.

It is not the parameter along which one moves from mixed-regular rank two to a rank-drop wall, nor from projection corank two to projection corank three.

The manuscript therefore still needs one-parameter degenerations in the **rank/moduli variables** and a theorem describing how primary components, \(W_j\)'s, nilpotency indices, and multiplication maps specialize.

This is the boundary-control theorem currently missing.

## E126.4 — close the Ballico 1993 comparison

This is documentary rather than algebraic, but it remains necessary for the top-four novelty claim.

## E126.5 — advance the inverse problem beyond formal generic finiteness

Compute \(d_{\mathrm{Tor}}\), prove generic injectivity, determine a nontrivial monodromy group, or show that a newly classified deeper nilpotent stratum canonically separates the finite Torelli packet.

## E126.6 — reframe the Rees theorem as standard background

Cite classical deformation-to-normal-cone references and state precisely which geometric identifications are new here.

# 14. Editorial corrections

Even before the larger mathematical work, I recommend the following changes.

1. Replace “Across the first singular Schubert boundary we compute that special fibre explicitly” by a statement naming the exact computed loci.

2. Replace the issue-matrix labels “resolved-by-global-rees-option-C” and “resolved-by-specialization” unless the remaining \(W_j\) are actually classified.

3. In the introduction, separate three levels:
   - universal Fitting presentation;
   - universal nilradical/Rees formalism;
   - multiplication-specific geometric classification.

4. Add a standard reference for the normal cone and deformation to the normal cone.

5. Keep the current careful wording around Ballico 1993. Do not infer novelty from inaccessible theorem text.

6. Retain the explicit statement that the computational evidence is not a general proof certificate.

# 15. Final assessment

Revision 126 is not a failed revision. The project is substantially more coherent than it was at revision 124.

The progress is real:

- the residual-colon filtration is exact;
- the mixed-regular collision algebra is stronger;
- the vertex primary component is genuinely controlled through those collisions;
- the containment case is separated correctly;
- the first decomposable mixed-kernel wall is computed;
- and the paper is much more disciplined about what belongs to classical Reye geometry.

The new Rees theorem is also correct.

But correctness of the Rees construction is not the same as closure of the higher-corank problem.

The family
\[
\mathfrak D_R\to\mathbb A^1
\]
exists because deformation to the normal cone exists for every closed immersion. The hard manuscript-specific content is the geometry of its special fibre. That geometry is still explicitly known only on selected strata. The remaining rank-drop and deeper projection-corank loci are carried into the special fibre without being classified.

Consequently the central top-four objection survives in a sharper form:

> **Revision 126 has produced a canonical container for the missing higher-corank structure, but it has not yet determined the missing structure.**

Together with the unresolved theorem-level Ballico 1993 comparison and the still-formal inverse-problem monodromy statement, this prevents me from recommending publication in a general top-four mathematics journal.

**Recommendation: reject in the present form at a general top-four journal. Reconsideration would require a genuinely new geometric classification of the graded special fibre across the remaining rank strata, not another formal repackaging of the same filtration.**
