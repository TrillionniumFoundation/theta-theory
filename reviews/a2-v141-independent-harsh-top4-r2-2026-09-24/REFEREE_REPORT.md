# Independent harsh referee report — A2 revision 141, second review

## Manuscript and review scope

**Manuscript:** *Intrinsic reconstruction from nonreduced failure schemes*  
**Author:** Qian Qi  
**Reviewed revision branch:** revision/a2-v141-functorial-spectral-reconstruction-2026-09-23  
**Exact reviewed branch head:** 8cd389f4048a1047be9aa8e8e4f642595175a555  
**Native source commit recorded by the v141 build:** 9d393bcb50dcf2a8a67c3b45749d9bda04ddbdee  
**Publication-workflow trigger:** d4e37912acaae4531312c0dd6258af2d8ed05a83  
**Successful publication workflow:** GitHub Actions run 35872058050  
**Immediate predecessor reviewed in the previous substantive round:** revision/a2-v140-intrinsic-pencil-moduli-2026-09-23, head 6bac73f9ebcaadcfa135e4960de19c93323bbfd7  
**Immediate controlling report for the author response:** reviews/a2-v140-independent-harsh-top4-2026-09-23/REFEREE_REPORT.md  
**Earlier v141 review:** reviews/a2-v141-independent-harsh-top4-2026-09-23/REFEREE_REPORT.md, which reviewed the much earlier v141 head bf0d9be9e2624058d24a57c48b19ec4c38105c1f before the substantive v141 manuscript was committed  
**Review standard:** external-referee-style assessment at the level of *Annals of Mathematics*, *Acta Mathematica*, *Inventiones Mathematicae*, or *Journal of the AMS*.

This is an owner-requested, AI-assisted independent referee-style report, not a journal-commissioned editorial decision.

This second v141 report is necessary because the existing v141 report is no longer a review of the current branch state. The branch advanced materially after bf0d9be: it now contains a native v141 manuscript, a source-bound successful build, a new universal relative-neighbourhood theorem, scheme-theoretic spectral readout, and a new theorem on reciprocal likelihood that addresses Fevola–Mandelshtam–Sturmfels Conjecture 4.5. The earlier report's statement that “there is no native v141 manuscript” is therefore obsolete for the current head.

I read the current v141 principal source, with particular attention to the introduction and Sections 20–23; the v140 response; the v141 literature audit; the build receipt and source/provenance records; the prior v140 and v141 reports; and the relevant inherited coefficient/contraction results needed by the new finite-neighbourhood chain. I also checked the published formulation of Fevola–Mandelshtam–Sturmfels Conjecture 4.5 against the theorem now claimed to solve it. I have not formally verified all 364 mathematical labels in the complete 118-page compilation, and the repository's symbolic checks should not be interpreted as doing so either.

## Recommendation

**Reject in the present form for a general top-four mathematics journal, but with a materially more favorable mathematical assessment than in the previous v140/v141 reports.**

The important change is this: I no longer regard source materialization, relative gluing, the two spectral lemmas, or the absence of an external theorem as open blockers. Revision 141 genuinely closes those points. In particular, the reciprocal-likelihood theorem appears to prove the precise existence assertion of Fevola–Mandelshtam–Sturmfels Conjecture 4.5, and the proof is not a restatement of the internal reconstruction theorem.

The remaining objections are of a different kind and are now concentrated in three areas.

1. **The central historical novelty audit is still incomplete.** The closest identified historical source, Ballico 1993 on failure loci, has still not been read at theorem level. The manuscript itself correctly records this as documentary-open. A top-four referee therefore cannot certify the novelty boundary of a paper whose central object is itself a nonreduced failure scheme.
2. **The exact all-dimensional contraction theorem still lacks exhaustive map-specific priority clearance while remaining part of the paper's broad significance story.** The current literature audit is much better and accurately distinguishes nearby classical ingredients, but it explicitly stops short of determining whether an equivalent restricted kernel formula already exists.
3. **The manuscript is mathematically richer but still not sufficiently architected as one general-top-four paper.** The new likelihood theorem is a legitimate external result, but it is almost logically independent of the failure-scheme machinery. The paper now contains at least three potentially publishable theorem clusters—intrinsic failure-scheme reconstruction, the all-rank contraction/support theorem, and the real reciprocal-likelihood theorem—without yet making completely convincing why they must live in one 55-page principal article plus a 66-page supplement.

I found no new fatal mathematical error in the main new v141 proofs. My negative recommendation is therefore **not** a claim that the paper is mathematically false. It is a top-four novelty, positioning, and reviewability judgment under unresolved priority evidence.

## 1. Revision 141 is now a genuine mathematical revision

The first v141 referee report reviewed head bf0d9be and correctly observed that, at that time, v141 was only a restoration layer over v140. That is no longer true.

The current branch head 8cd389f contains a native article/v141 tree with:

- geometry.tex and geometry.pdf;
- supplement.tex and supplement.pdf;
- complete.tex and complete.pdf;
- RESPONSE_TO_REFEREE_V140.md;
- REFEREE_GUIDE_V141.md;
- LITERATURE_AUDIT_V141.md;
- native checks and a source-bound build receipt;
- new source Sections 22 and 23 and substantive edits to the spectral material.

The source-bound receipt reports:

- geometry: 55 pages;
- supplement: 66 pages;
- complete compilation: 118 pages;
- 364 current mathematical labels;
- all 338 inherited labels retained;
- seventeen executed exact/symbolic scripts;
- no unresolved labels, LaTeX errors, or overfull blocks in the recorded native builds;
- source commit 9d393bcb50dcf2a8a67c3b45749d9bda04ddbdee;
- ok=true.

The successful Actions run 35872058050 is attached to the v141 revision branch. The subsequent publication commit adds the PDFs, logs, and evidence generated by that source; the source itself is not silently changed in that final publishing step.

Thus B140.1, the source-state blocker, is substantially closed.

This is worth stating explicitly because the repository currently contains two contradictory v141-era review narratives: the old review says there is no native v141 manuscript, while the current branch demonstrably contains one. Future review routing must point to the exact reviewed commit, not merely to “v141” as a moving branch name.

## 2. The sharp finite-neighbourhood theorem remains one of the strongest parts of the paper

Let N=binom(n+1,2), p=N-2, and d=n+2p=n^2+2n-4. Near the intrinsic socle Grassmannian B=Gr(n,S_R), the manuscript has the homogeneous failure ideal

I_R=(det T) I_p(gamma_R Sym^2 T)

inside Sym E^*, with E=Hom(U,V). Every generator has degree exactly d. The key theorem says that the order-d ideal-adic neighbourhood Z_R^[d] reconstructs the pencil up to projective equivalence, while every order below d is independent of R.

I rechecked the point at which a superficial “degree-counting sharpness” could be confused with intrinsic reconstruction. The paper now makes the right distinction.

- The fact that no relation appears before degree d is formal once the displayed homogeneous ideal is known.
- The nontrivial step is that the **abstract unmarked order-d scheme** recovers the first relation space, the complete normal cone, the determinant rank-one geometry, the orientation of its two rulings, the residual coefficient line, and finally the Pluecker line of R under one common projective transformation.

Lemma thm:first-relation-cone's mechanism is sound at the advertised level: the reduction is intrinsic, the nilradical gives L=n/n^2, multiplication recovers the kernel in Sym^d L, and the full graded normal-cone ideal is generated by that degree-d kernel.

Likewise, the fixed-coordinate map

Phi: Gr(2,Sym^2 V) -> Gr(M,Sym^d Hom(U,V)^*)

is convincingly factored through the Pluecker line, a line-times-fixed-space Grassmannian embedding, and one fixed coefficient inclusion. This is a genuine closed-immersion statement, not only a point-separation assertion.

I therefore continue to regard the finite-order theorem and the scheme-theoretic parameter immersion as substantial mathematical contributions.

### Required calibration

The introduction should keep the current distinction between:

- “d is the smallest **uniform** order classifying all pencils”; and
- “every inequivalent pair is first separated exactly at d.”

Only the first is proved and needed.

The numerical value d itself should also not be rhetorically presented as if it were a mysterious universal constant discovered independently of the Fitting presentation. The conceptual content lies in recovering the coefficient structure intrinsically from the unmarked finite neighbourhood.

## 3. The v140 relative-gluing request is now genuinely closed

The new Theorem thm:universal-finite-neighbourhood is not merely a relabeling of the fixed-coordinate flat algebra from v139/v140.

The proof now writes the degree-d relation bundle through a coordinate-free morphism

det(V^*) tensor det(U) tensor det(S^*) tensor wedge^p Sym^2(U)
 -> Sym^d(E^*)

and explains why its image is a rank-M subbundle. On frame charts this is the fixed coefficient inclusion restricted to the tautological line; under right frame changes the determinant character and the Cauchy factors transform equivariantly. The local ideals therefore glue as ideals of the **actual graph neighbourhood**.

The passage to the quotient by the (d+1)-st power of the zero-section ideal then identifies the glued object with the actual ideal-adic neighbourhood, rather than merely with an abstract family of coordinate quotient algebras having the correct fibres.

The manuscript also now correctly separates:

- the specified relative socle ideal over a nonreduced base; and
- the absolute nilradical, which may contain nilpotents coming from the base.

This addresses the exact weakness identified in the v140 report. I do not regard relative gluing as an open blocker any longer.

## 4. The spectral-sheaf theorem is now properly self-contained

The v140 report asked for two short but important missing arguments.

### 4.1 Sheaf isomorphism versus similarity

Lemma lem:spectral-sheaf-similarity identifies coker(zA-B), after multiplying by A^{-1}, with the finite C[z]-module on which z acts by C=A^{-1}B. A sheaf isomorphism in a fixed affine coordinate is therefore exactly a linear similarity of C.

This is elementary, but writing it explicitly removes an ambiguity that was unacceptable in a Torelli-style statement.

### 4.2 Polynomial square roots for nonsemisimple operators

Lemma lem:artinian-polynomial-square-root is also correct in the required complex setting. The truncated binomial series in each local Artinian factor of the minimal polynomial, followed by Chinese remaindering, supplies a polynomial h with h(K)^2=K for every invertible complex K. Because h(K) is a polynomial in K, the commutation and self-adjointness properties used later are preserved.

With those lemmas, the implication from the spectral torsion sheaf to congruence of the symmetric pencil is convincing: after similarity one has the same C, and K=A^{-1}A' both commutes with C and is self-adjoint for A. Setting H=h(K) yields H^t A H=A' and H^t B H=B'.

The field is important. The argument is naturally complex and should not be casually generalized to arbitrary real or arithmetic fields without revisiting square roots and forms.

## 5. The scheme-theoretic spectral readout is a real improvement, but the Segre-closure paragraph is mostly formal

The truncated-presentation lemma

coker(wI-X) tensor D[w]/(w^a) ~= coker(X^a)

over an arbitrary commutative coefficient ring is a clean device. It gives the Fitting ideals

I_{n-h+1}((C-zI)^a)

without diagonalizing or dividing by eigenvalue differences. This is exactly the right way to package nonreduced spectral length data in families.

Theorem thm:relative-spectral-readout therefore adds something stronger than the v140 single specialization: the first relation space recovers a whole collection of scheme-theoretic spectral incidence loci, compatibly with base change.

I regard that result as mathematically useful.

By contrast, the subsection on “realizing the complete Segre stratification” must remain carefully calibrated. Once Phi is a closed immersion, transporting already known Segre-stratum closures and their intersections through Phi is formal. The manuscript explicitly admits this, which is good. That transport should not be advertised as a new classification theorem.

The genuine new content is:

- the relation-space embedding;
- realization by actual finite failure neighbourhoods;
- recovery of the spectral Fitting incidence schemes.

That is enough. The classical closure order should remain credited as classical.

## 6. The rank-preserving specialization survives scrutiny

The four-dimensional block family

C_t = [[P_t,I],[0,P_t]],  P_t=(t/2)N_0,  N_0^2=0, rank(N_0)=1

has the advertised properties.

- rank C_t=2 for every t;
- rank C_t^2=1 for t nonzero and 0 for t=0;
- C_t^3=0;
- the nilpotent partitions are therefore (3,1) and (2,2);
- det(sI+uC_t)=s^4;
- the reduced rank-degeneracy loci remain unchanged.

The local spectral length profiles distinguish the two fibres, while the full discriminant multiplicity and reduced coranks do not. The conic-to-line change in reciprocal geometry is also correctly derived from the span of I,C_t,C_t^2.

The adjective **reduced** remains essential. The manuscript itself notes that the higher determinantal/Fitting structures change at the special fibre. Any summary that says “all rank loci stay constant” without the qualifier would be mathematically misleading.

The flat family proved here is the family of finite failure neighbourhoods. The reciprocal curves are not claimed to form a flat family, and the unrestricted full failure schemes are not claimed flat. The current wording respects these boundaries.

## 7. The new reciprocal-likelihood theorem is a genuine external theorem and appears correct

This is the most important positive change relative to v140.

The primary source is:

C. Fevola, Y. Mandelshtam, B. Sturmfels, *Pencils of Quadrics: Old and New*, Le Matematiche 76 (2021), 319–335, arXiv:2009.04334.

In the published/arXiv text, Conjecture 4.5 states that for a definite diagonalizable pencil with r distinct eigenvalues there exists real data s such that the reciprocal log-likelihood has 2r-3 distinct real critical points. The conjecture does **not** require all entries of the data to be positive, nor does it require all critical points to lie in the positive definite cone. Example 4.6 itself uses mixed-sign data.

Revision 141 proves exactly that existence assertion and more: nondegeneracy and a nonempty Euclidean open set of such data.

### 7.1 The algebraic reduction is clean

With distinct eigenvalues alpha_1<...<alpha_r and multiplicities m_i, set

D(t)=prod_i(t-alpha_i),

choose a degree-r-1 polynomial Q whose roots beta_j all lie to the right of alpha_r, and define

sigma_i=Q(alpha_i)/D'(alpha_i).

The partial-fraction identity gives

sum_i sigma_i/(t-alpha_i)=Q(t)/D(t).

After the chart substitution y=-xt, the x-score gives x=S(t)/n and the remaining score reduces to the rational equation F(t)/(D(t)Q(t))=0, where

F(t)=nD(t)Q'(t)-Q(t) sum_i (n-m_i)D(t)/(t-alpha_i).

The leading degree 2r-2 term cancels because sum_i(n-m_i)=n(r-1).

### 7.2 The real-root count is decisive

At alpha_i, the values of F alternate in sign because D'(alpha_i) alternates while all Q(alpha_i) have the same sign. This gives r-1 roots between consecutive alpha_i.

At beta_j, D(beta_j)>0 and Q'(beta_j) alternates, giving another r-2 roots between consecutive beta_j.

The two interval strings are disjoint. Thus there are 2r-3 distinct real roots. Since deg F is at most 2r-3 after the leading cancellation, these roots exhaust F over C and are simple.

This is a strong argument: it counts all roots directly and does not assume the generic reciprocal ML-degree formula as an upper bound.

### 7.3 The omitted chart and Hessian are actually treated

The proof also handles the two details that frequently invalidate “all critical points are real” constructions.

First, the omitted affine locus x=0 is checked separately. The two leading partial-fraction identities force y=1/n and then an impossible weighted eigenvalue equality because all beta_j lie strictly to the right of alpha_r.

Second, at each critical point, the x-x Hessian entry is nonzero and the derivative of the eliminated one-variable score is the Schur complement. Simplicity of the root of F therefore gives nondegeneracy of the full Hessian.

Finally, the residue interpolation map from degree-at-most-r-1 polynomials Q to the grouped data vector is a linear isomorphism, so the separated-root construction yields an open, nonempty set of grouped data; surjectivity of the map from original data to group sums lifts it to the full data space.

I do not see a mathematical gap in this proof.

### 7.4 What this theorem does and does not close

It **does close** the previous demand for an external theorem not reducible to “our invariant remembers a classical object.”

It **does not by itself settle historical first priority**. The v141 audit is appropriately cautious about that point. I did not find a verified later solution in the sources checked during this review, but absence from a limited search is not an exhaustive priority certificate.

It also raises a new architectural question: the proof uses only the real spectral points and an explicit residue construction. It does not materially use the nonreduced failure-neighbourhood machinery. That is not a correctness problem; it is a paper-cohesion issue discussed below.

## 8. The strongest remaining blocker is still Ballico 1993

The manuscript continues to identify:

E. Ballico, *On the Failure Locus of Higher Order Properties of Embeddings in Projective Spaces*, Mathematische Nachrichten 163 (1993), 5–13, DOI 10.1002/mana.19931630102.

The v141 audit honestly says the complete article was not obtained and leaves all six requested comparison axes unverified:

1. parameter spaces;
2. reduced versus scheme-theoretic failure locus;
3. the varied map;
4. nilpotent/infinitesimal structure;
5. relative/base-change statements;
6. inverse/reconstruction conclusions.

I was able to confirm the bibliographic record and table-of-contents entry, but I did not obtain the full theorem/proof text through the accessible route used in this review. I therefore make neither an anticipation nor a nonanticipation claim.

For an ordinary specialized-paper referee, an inaccessible old source can sometimes be treated with a carefully worded qualification. Here the situation is different. The central construction is literally a scheme-theoretic failure locus, and the closest already-identified historical source has “Failure Locus of Higher Order Properties” in its title. The burden is not to prove exhaustive global priority; it is to read the closest known source before asking a general top-four journal to certify the novelty boundary.

This remains a blocking item for me.

### Required action

Obtain the article through a lawful library/interlibrary route and give theorem numbers, hypotheses, and conclusions along the six axes above. If the source is genuinely unrelated after inspection, say precisely why. If it contains a nearby degeneracy/failure construction, explain exactly where the present inverse, nilpotent, or relative conclusions begin.

Until that comparison exists, I cannot responsibly certify the central novelty narrative at top-four level.

## 9. The all-dimensional contraction theorem is mathematically interesting, but its priority status is still not closed

The current audit is much improved. It now distinguishes the exact restricted operator

kappa_(n,q)=iota_q o j_n:
det(V) tensor Sym^n(V) -> wedge^(n-1) Sym^2(V)

from:

- harmonic decomposition;
- binary transvectants;
- unrestricted exterior contraction;
- quadratic apolar operators;
- Piola/cofactor cancellation;
- generic skew-flattening support bounds.

The manuscript proves a specific all-rank kernel formula:

- singular q: det(V) tensor Sym^n(rad q);
- nondegenerate q, n odd: zero;
- nondegenerate q, n even: the scalar line generated by (q^{-1})^(n/2).

The singular-rank proof with radical shears is genuinely more specific than simply quoting an orthogonal harmonic decomposition, and the even scalar exception is computed explicitly.

However, the audit itself states that it has **not** established that no equivalent restricted kernel formula exists elsewhere in invariant theory under another normalization or representation-theoretic description.

That caveat is honest, but it matters because this theorem is repeatedly used as evidence of dimension-uniform generality.

I see two acceptable routes.

1. Close the priority question with a serious map-specific literature comparison, ideally including expert-level references on exterior powers of Sym^2(V), Howe duality, and contraction/interior-product maps.

2. If that cannot be done, demote the theorem from the central novelty rhetoric. Present it as the explicit technical calculation needed by the reconstruction proof, with the already inspected classical antecedents fully credited.

What is not acceptable at top-four level is simultaneously to use the result as a broad novelty pillar and to leave its exact historical status explicitly unresolved.

## 10. The new external theorem improves significance, but the paper's unity is still not convincing

Revision 141 has answered my previous objection that the only external consequences were reinterpretations or explicit specializations. The reciprocal-likelihood theorem is a legitimate theorem in an independently studied problem.

Nevertheless, the way it enters the current paper exposes an architectural problem.

The main inverse-problem chain is:

intrinsic coefficient extraction -> sharp finite reconstruction -> spectral geometry.

The likelihood theorem, by contrast, starts once the real pencil has been separately normalized and its ordered real eigenvalues and multiplicities are known. Its proof then proceeds by one-variable rational function design. It does not require the finite failure neighbourhood, the intrinsic normal cone, the coefficient closed immersion, or the universal relative family.

That independence is mathematically attractive—it shows the result is not circular—but editorially it means the theorem could almost be a separate short paper.

At a general top-four journal, the authors should answer the following question explicitly:

**What single mathematical idea makes the reconstruction theorem, the all-rank contraction theorem, and the reciprocal-likelihood theorem one paper rather than three adjacent papers?**

A satisfactory answer could be that all three are manifestations of a precise spectral/failure principle formalized in one master theorem. The current manuscript gestures in that direction but does not yet formulate such a unifying theorem.

I do not recommend deleting good mathematics merely to shorten the paper. I recommend imposing a much sharper hierarchy.

- The finite unmarked reconstruction theorem should be the unmistakable central theorem.
- The universal spectral readout should be the main structural extension.
- The likelihood theorem should be presented either as a conceptually necessary consequence of that spectral structure or clearly as an independent theorem motivated by it.
- The web/K3 and contraction material should be positioned as the earlier/high-rank mechanism that supports the general reconstruction architecture, not as a second competing main paper inside the first.
- The polar-system theorem and large boundary atlas belong to supporting architecture unless they are needed for the main logical chain.

At present the paper still asks too many theorem families to carry equal top-level significance.

## 11. Repository-level review routing is not yet clean enough for a 141-revision project

There are two concrete stale metadata objects at the exact reviewed head.

### 11.1 CURRENT_REVIEW_ENTRY.md is stale

At the root of the current v141 branch, CURRENT_REVIEW_ENTRY.md says:

- current A2 revision entry: 131;
- principal manuscript: article/v131/geometry.tex;
- controlling review: v130.

That is false for the current branch state.

### 11.2 The active v141 ISSUE_MATRIX.json is also stale

The file

papers/A2-v17-boundary-information-coarsening/article/v141/ISSUE_MATRIX.json

declares revision 139 and tracks B137-era issues. It is not a v141 issue matrix despite living in the active v141 directory.

These are not mathematical counterexamples, but they matter in a repository whose central defense is reproducibility, provenance, and exact reviewed-state control. A referee should not need to decide which top-level index is stale and which nested README is canonical.

The correct fix is simple:

- make one immutable review entry identify the exact manuscript commit;
- update the issue matrix to the current revision and current controlling report;
- keep historical matrices under history/ rather than as active files;
- do not move a branch after a referee report without making the report's exact reviewed SHA prominent.

The current second review uses exact head 8cd389f precisely because the first v141 report reviewed bf0d9be and became obsolete when the same revision branch advanced.

## 12. Build and computational evidence are strong, but should remain subordinate to proof

The v141 regression discipline is unusually extensive. The current receipt records:

- seventeen scripts;
- exact spectral and likelihood checks;
- preservation of inherited labels and predecessor source hashes;
- native article, supplement, and complete builds;
- PDF hashes and page counts;
- no unresolved references in the recorded run.

This is excellent engineering.

It is not a formal proof certificate.

In particular, the scripts cannot establish:

- the intrinsicness of every normal-cone reconstruction step;
- the global novelty of the contraction formula;
- historical nonanticipation;
- the top-four significance of the theorem package.

The manuscript and README are appropriately explicit about this distinction. Keep that language.

## 13. Additional proof-level and exposition comments

### 13.1 State the exact dependency of spectral reconstruction on regularity

The torsion-sheaf Torelli theorem is for regular pencils, i.e. pencils containing a nonsingular member. The all-pencil finite-neighbourhood theorem is stronger in scope. Summaries should not blur those two domains.

### 13.2 Keep “unmarked scheme” separate from “fixed tensor presentation”

The intrinsic theorem for Z_R^[d] is an isomorphism-class statement. The closed immersion Phi and the scheme-theoretic spectral incidence construction use fixed tensor coordinates on the parameter scheme. The paper currently states this difference, and it is essential.

### 13.3 Do not oversell the formal transport of Segre strata

As noted above, the closed immersion preserving intersections is formal. The new content is the realization by actual neighbourhoods and spectral Fitting schemes.

### 13.4 Clarify which theorem is the main top-four claim

The abstract presently lists:

- all-pencil finite reconstruction;
- flat universal families;
- spectral Fitting schemes;
- Segre strata;
- rank-preserving specialization;
- the FMS conjecture;
- web reconstruction;
- all-rank contraction;
- K3/hyperelliptic consequences;
- boundary and polar constructions.

This is too many “headline” results for one abstract. A top-four abstract should make the main theorem and one or two decisive consequences unmistakable.

### 13.5 A theorem-dependency map would materially help

I strongly recommend a compact one-page dependency chart in the paper itself, not only in repository metadata. It should separate:

- classical inputs;
- intrinsic normal-cone/coefficient extraction;
- natural pencil reconstruction;
- finite-order theorem;
- universal relative theorem;
- spectral readout;
- external likelihood theorem;
- web/contraction supporting results;
- supplement-only boundary results.

This would make the manuscript much easier to audit.

## 14. What revision 141 has actually closed from the v140 report

For clarity, my status assessment is:

### Closed or substantially closed

**B140.1 — native source and source-bound build:** closed.  
**B140.4 — external significance theorem:** substantially closed by the reciprocal-likelihood theorem, modulo ordinary historical priority caution.  
**Request 5 — relative gluing of actual ideal-adic neighbourhoods:** closed.  
**Request 6 — spectral sheaf/similarity and polynomial square-root lemmas:** closed.  
**Request 7 — reduced versus full rank/Fitting distinction:** correctly retained.  
**Request 9 — finite-order novelty boundary:** substantially better calibrated.

### Still open

**B140.2 — Ballico 1993 six-axis comparison:** open and, for me, still blocking.  
**B140.3 — exhaustive map-specific priority assessment for the contraction theorem:** open if the theorem is to remain a central novelty pillar.  
**Request 8 — one primary narrative:** improved but not closed; the paper is still structurally overfull.

### New review-object issue

**B141-R2.1 — canonical routing metadata is stale.** CURRENT_REVIEW_ENTRY.md and the active v141 ISSUE_MATRIX.json do not describe the current manuscript.

## 15. Minimum conditions for a fresh top-four recommendation

Before I could recommend acceptance, or even a final accept/reject review focused only on mathematics, I would require:

1. **Close the Ballico 1993 theorem-level comparison.** This is the most important remaining external blocker.
2. **Resolve the contraction-theorem priority status.** Either complete the map-specific comparison or narrow its novelty role.
3. **Repair the canonical review metadata.** The current manuscript, issue matrix, and controlling report must agree on one exact reviewed state.
4. **Re-architect the introduction and abstract around one primary theorem chain.** Preserve the mathematics, but make hierarchy explicit.
5. **Explain the conceptual role of the likelihood theorem.** Either integrate it through a stronger spectral principle or present its independence cleanly without pretending the failure invariant is used in its proof.
6. **Keep all scope qualifiers.** Regular versus arbitrary pencils, reduced rank loci, finite-neighbourhood flatness, complex versus real structures, and framed versus unmarked statements must remain explicit.
7. **Retain the source-bound native build discipline.** The current v141 state is a genuine improvement and should not regress.

## 16. Final assessment

The current v141 manuscript is substantially stronger than both v140 and the earlier v141 state reviewed at bf0d9be.

The main mathematical progress is real:

- the source is now natively reviewable;
- the order-d unmarked reconstruction theorem remains strong;
- the parameter closed immersion is scheme-theoretic;
- the relative finite-neighbourhood family is now actually glued and base-change compatible;
- the spectral torsion argument is properly closed;
- spectral Fitting incidence schemes are recovered in families;
- the rank-preserving specialization remains clean;
- and the new real reciprocal-likelihood theorem appears to prove the exact published FMS Conjecture 4.5 and strengthens it by nondegeneracy and openness.

I therefore do **not** repeat the old claim that v141 is merely a source-restoration revision. That claim was correct for the older head but is false for the current head.

Nevertheless, I still would not recommend publication in a general top-four journal in the present form. The closest historical failure-locus comparison is explicitly unresolved; the exact priority status of the broad contraction theorem remains uncertain; and the paper has not yet found a sufficiently unified top-four narrative for its now very large collection of results. The repository's stale canonical review metadata also needs to be fixed before the next round.

My recommendation is therefore **reject in the present form, with a serious invitation to return after the priority and architecture blockers are closed**. This is now a substantially narrower and more constructive negative recommendation than in the preceding rounds. If the Ballico comparison and contraction-priority issue come out favorably, and if the paper is reorganized around the finite-neighbourhood/spectral spine, I believe the manuscript would merit a genuinely fresh top-four evaluation rather than another incremental cleanup round.
