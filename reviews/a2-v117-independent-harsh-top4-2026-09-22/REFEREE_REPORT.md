# Independent harsh referee report on A2 revision 117

**Manuscript:** *Finite quotients and primary structures of multiplication failure schemes*  
**Author:** Qian Qi  
**Repository:** TrillionniumFoundation/theta-theory  
**Reviewed revision branch:** `revision/a2-v117-finite-quotient-primary-structure-2026-09-22`  
**Frozen mathematical-source commit:** `58126b1445e57cfb16f33b6e74a7098b9223445b`  
**Frozen published/product head:** `fb999b3a43fe4331becb42646bc2faeadfa5492a`  
**Controlling R116 report:** `a65e0e92b24fe6882e60ebcf678bb2f9f5048312`  
**Date:** 22 September 2026

## Referee status and standard

This is an owner-requested, AI-assisted external-referee-style assessment. It was not commissioned by *Annals of Mathematics*, *Inventiones Mathematicae*, *Journal of the American Mathematical Society*, *Acta Mathematica*, or any other journal, and it must not be represented as a journal-issued referee report or editorial decision.

I have reviewed the new 19-page primary geometry article, the 83-page complete manuscript, the response to R116, the proof/literature audit, the source and build receipts, the new conductor, finite-quotient, three-plane, and étale-descent sections, and the relevant inherited contact material. I also checked the cited Haiman statement at theorem level rather than relying on the manuscript's paraphrase. Haiman's Corollary 3.8.3 does indeed give the all-powers identity for the alternating-polynomial ideal and the pair-diagonal ideals. I therefore do **not** regard the three-plane power statement as a citation error.

I distinguish throughout:

1. whether I found a concrete mathematical contradiction;
2. whether the arguments are written at the level required for a final research article;
3. whether the package has the originality, conceptual depth, breadth, and demonstrated mathematical importance expected at a general top-four mathematics journal.

These questions have different answers.

# Recommendation

## Reject in the present form at a general top-four mathematics journal.

This recommendation is materially different from R116. Revision 117 has genuinely answered several of the previous report's structural requests. It is no longer fair to say that the manuscript merely transports an arbitrary-(k) problem and then solves only a monogenic (k=2) family. The new hyperplane theorem treats arbitrary finite locally free commutative algebras, and the new reduced-contact three-plane theorem is a real (k=3) result with a complete stable ideal and all ordinary powers.

I also did **not** find a fatal counterexample to the new headline theorems during this review.

The remaining objection is therefore sharper and more venue-specific: after one removes the classical or externally supplied pieces—rank-two quotient/Hilbert geometry, Grassmannian cohomology, index-form/discriminant algebra, and Haiman's deep diagonal-ideal theorem—the manuscript has not yet demonstrated a new general mechanism of sufficient depth and reach for a top-four general journal. Its strongest complete theorems still live on conductor-containing finite-contact families, and the genuinely multigenerator theorem is restricted to reduced contacts in the stable range and obtains its hardest scheme-theoretic identity from Haiman.

That is substantial mathematics. It is not, in my assessment, yet a top-four case.

# 1. What revision 117 genuinely fixes

The report should begin by acknowledging the amount of real mathematical movement since R116.

### 1.1 The article now has a coherent primary object

The separate `geometry.tex` is a 19-page paper with a clear spine:

- sharp conductor reduction;
- the universal generating-hyperplane theorem;
- fixed multiplicity primary schemes;
- the smooth moving hyperplane scheme;
- the reduced-contact three-plane theorem;
- an explicit étale descent lemma;
- the retained pencil theorem and normalization;
- a finite-literature comparison.

The 83-page `paper.tex` now reads as an archival complete version with older independent developments explicitly moved to a complementary block. This is a substantial repair of the article-identity problem in R116. I no longer regard the accumulation of old material as a decisive objection to the *primary* 19-page article.

### 1.2 The conductor range is materially better

Theorem `thm:sharp-conductor` replaces the old sufficient threshold by the uniform bound
[
nge 2d-k
]
for (1le k<d), and the evaluation-kernel splitting identifies the fibrewise obstruction. The boundary monomial example at (n=2d-k-1) is correctly targeted at failure of the actual cokernel comparison in degree two, not merely failure of an intermediate proof device.

The proof is conceptually clean: for (Usubset H^0(mathbb P^1,mathcal O(n))), the evaluation kernel controls precisely when multiplication by (U) fills a complete linear series. The estimate on the maximal splitting summand gives the uniform range. I found no contradiction in this argument.

The positive-genus theorem is also an improvement because it separates the finite-contact algebra from the global regularity problem. Its numerical bound is a sufficient range, not advertised as sharp.

### 1.3 R116's request for a genuine multigenerator result has been answered in a nontrivial special case

Theorem `thm:three-plane-primary` is a genuine new center of gravity relative to R116. For a reduced divisor (D=p_1+cdots+p_d), a generating three-plane is put on a unit frame
[
A=langle a,ax,ayangle,
]
and stable multiplication is identified with evaluation of polynomials in the labelled pairs ((x_i,y_i)). The total-degree truncation lemma is exactly the step needed to pass from arbitrary polynomial columns to a finite multiplication matrix.

The resulting ideal is the big pair-diagonal ideal
[
J=igcap_{i<j}(x_i-x_j,y_i-y_j),
]
and the paper asserts, for every (qge1),
[
J^q=igcap_{i<j}(x_i-x_j,y_i-y_j)^q.
]

I checked the cited source. Haiman, *Hilbert schemes, polygraphs, and the Macdonald positivity conjecture*, Corollary 3.8.3, states precisely the corresponding all-powers identity for the ideal generated by alternating polynomials. Thus the paper is using a deep theorem correctly here; the all-powers statement should not be attacked as an unsupported extrapolation.

### 1.4 The primary descent objection from R116 is substantially closed

Lemma `lem:etale-primary-descent` is now isolated and proves the needed facts in the right order: invariant orbit ideals descend, the reduced orbit union is identified with an integral Cartier divisor downstairs, and only then are powers and intersections descended. The argument explicitly allows several labelled branches in one orbit to pass through a point and does not silently call the downstairs divisor smooth or unibranch.

That is the lemma R116 asked for.

### 1.5 The manuscript is substantially more honest about classical inputs

The new finite-literature section explicitly calls the pencil determinant a classical index form, attributes the monogenerator/polygenerator constructions to Arpin–Bozlee–Herr–Smith, identifies (G_r) with a classical Grassmannian cohomology ring, and states that the all-powers diagonal identity is Haiman's theorem rather than a theorem proved here.

This makes the novelty boundary much clearer than in v116.

# 2. The universal hyperplane theorem is elegant, but its generality is deceptive if read as high-rank complexity

Theorem `thm:universal-hyperplane` is the strongest formally general new statement:

> for a finite locally free commutative algebra (B/S) of rank (d), on the generating hyperplane Grassmannian, all higher multiplication failure schemes agree and are isomorphic to rank-two quotient algebras equipped with a generating line.

I believe this is a good theorem. The proof is short for a reason.

After normalizing a unit in the hyperplane, the problem becomes: when is a unital hyperplane (A'subset B) a subalgebra? Its conductor has rank (d-2), so the quotient has rank two. Conversely a rank-two quotient recovers the hyperplane as the inverse image of the scalar line. Once (1in A'), equality of the quadratic residual ideal and every higher residual ideal follows by inserting units.

This is exactly the correct structural explanation.

But for venue assessment, one must describe what has happened honestly: the entire arbitrary-rank statement is governed by **defect two**. The algebra (B) may have arbitrarily large rank, but a hyperplane subalgebra has a conductor whose quotient is rank two. The theorem is universal in the ambient algebra, not universal in the complexity of the quotient geometry.

That distinction matters. The result is more general than the old pencil theorem, but the geometric object that controls failure remains a length-two quotient.

A top-four introduction cannot rely on the phrase “arbitrary finite locally free algebra” without simultaneously explaining that the classification mechanism collapses the problem to (operatorname{Hilb}^2).

# 3. The fixed-contact hyperplane primary classification is exact, but much of its geometry is inherited from classical length-two algebra

Theorem `thm:contact-hyperplane-primary` gives, for
[
D=sum_i d_i p_i,
]
a disjoint union of components with transverse rings
[
G_r=mathbb C[u,v]/(F_r,F_{r+1})
]
and
[
H_{r,s}=mathbb C[x,y]/(x^r,y^s).
]

The lengths and nilpotency indices are explicit, and the moving total scheme is smooth even though fixed fibres are nonreduced. These are attractive statements.

However, the proof makes very clear where the geometry comes from:

- a length-two quotient is either concentrated in one curvilinear factor or split across two factors;
- the one-factor quotient is the punctual length-two quotient problem for (mathbb C[z]/(z^r));
- the ring (G_r) is the classical cohomology ring of (operatorname{Gr}(2,r));
- the two-factor case is the elementary complete intersection (mathbb C[x,y]/(x^r,y^s)).

The contribution is the exact identification of these finite Hilbert-scheme pieces with the original multiplication-failure Fitting scheme, plus the global conductor transport.

That contribution is real. But the paper still needs to convince a general top-four editor that this transport creates a phenomenon of independent mathematical importance rather than packaging known finite-algebra geometry inside a new multiplication problem.

At present the manuscript proves the identification; it does not yet demonstrate a wider theory that depends on it.

# 4. The smooth moving hyperplane scheme is a useful synthesis, not yet a top-four-level surprise

Once the universal hyperplane theorem is available, the moving theorem identifies the failure scheme with the generating open of a projective-line bundle over
[
operatorname{Sym}^2 C	imesoperatorname{Sym}^{d-2}C.
]

The smoothness and irreducibility then reflect the smooth nested-divisor parameter space and the projective-line construction. The contrast with nonreduced fixed fibres is geometrically pleasant.

But this theorem is downstream from the rank-two quotient identification. Its proof does not introduce a new difficult mechanism of comparable depth. The same is true of the explicit noncurvilinear chart
[
(ab,b^2)=(b)cap(a,b)^2.
]
That chart is useful because it prevents overgeneralization of the curvilinear no-embedded-prime statement, but one chart is evidence of richer geometry, not a classification of it.

For a specialist paper, this is a strength. For a general top-four paper, it increases the pressure to go further into the noncurvilinear finite-algebra geometry rather than stopping after one embedded example.

# 5. The three-plane theorem is the most important new response to R116, but its novelty boundary must be stated even more sharply

The three-plane theorem is where v117 most clearly leaves the rank-two quotient story.

It is also where the external input is deepest.

The key decomposition
[
J^q=igcap_{i<j}P_{ij}^q
]
for all (q) is Haiman's theorem. The manuscript's new work is:

1. showing that stable multiplication for a generating three-plane on a reduced contact divisor produces the alternating-polynomial ideal;
2. proving a finite total-degree truncation compatible with the coefficient ring;
3. transporting the result back to the original global multiplication problem using the conductor theorem.

This is a legitimate theorem. It should be advertised exactly in those terms.

What it does **not** yet do is classify a genuinely new diagonal-type scheme beyond Haiman's big diagonal, or treat the nonreduced contact configurations where the new finite-algebra geometry should become substantially more complicated.

The restrictions are important:

- (D) is reduced;
- the result is in the stable range (mge d-1);
- the local scheme after choosing a unit frame is exactly the pair-diagonal arrangement whose powers are controlled by Haiman;
- no analogue is proved for general finite algebras with embedding dimension (>1);
- no primary classification is given for three-planes on nonreduced (D);
- no unrestricted ambient Grassmannian theorem follows.

Thus Route B from R116 has been **meaningfully entered**, but not exhausted.

For a top-four case, I would want the paper to use this theorem as the first instance of a new multigenerator structure theorem, not as the terminal multigenerator result.

# 6. The curve theorem is structurally useful but currently functions as a transport theorem

Theorem `thm:curve-conductor` improves the conceptual architecture because it identifies the global-to-finite comparison with cohomological multiplication obstructions rather than a special feature of binary forms.

That is the right direction.

Still, the theorem presently assumes strong hypotheses—global generation, quadratic normal generation, and a full family of (H^1)-vanishings—and then gives a familiar high-degree sufficient bound
[
deg Lge 2d+2g-1.
]

The paper explicitly does not claim positive-genus sharpness.

At the top-four level I would expect one of the following:

- a genuinely sharp intrinsic criterion on curves;
- a theorem showing new behavior as the evaluation-kernel splitting is replaced by vector-bundle geometry;
- extension to higher-dimensional varieties with a new regularity mechanism;
- or an application where this transport theorem yields a previously inaccessible geometric classification.

At present it broadens the range of applicability but does not itself provide the conceptual leap.

# 7. The nearest-source priority problem remains open, and at this venue that is not an editorial detail

Revision 117 explicitly leaves the Ballico 1993 comparison unresolved.

That is responsible, but it means the scholarly-priority question is still open.

I independently checked the public DOI route for E. Ballico, *On the Failure Locus of Higher Order Properties of Embeddings in Projective Spaces*, Math. Nachr. 163 (1993), 5–13. The public Wiley route exposes the bibliographic record and references but, in this review session, redirected the PDF route back to the abstract/metadata page rather than supplying the complete theorem pages. I therefore cannot certify either overlap or disjointness.

The correct conclusion is exactly the one the authors now state: failed access is not evidence of novelty.

For a specialist submission this could perhaps be handled editorially while the source is obtained. For a top-four submission whose case depends on the novelty of a broad “failure scheme” package, I would not regard the priority audit as complete until the closest historical source has been read theorem by theorem.

This is the only R116 mandatory item that the authors themselves correctly leave explicitly open.

# 8. The literature comparison around the universal hyperplane theorem is still too narrow for the new flagship claim

The manuscript now compares with the scheme of monogenic generators and polygenerators, and that is essential.

But the flagship theorem is not merely a statement about a point or tuple generating an algebra. It identifies a degeneracy locus of **hyperplane subspaces** with an incidence of length-two quotient algebras.

That formulation brings in several neighboring bodies of literature:

- moduli of subalgebras of finite algebras;
- relative Hilbert schemes of finite schemes;
- nested/flag Hilbert constructions for zero-dimensional schemes;
- generator and non-generator schemes;
- discriminant/index-form geometry.

The manuscript currently establishes the theorem internally and cites the most obvious generator-scheme comparison. It does not yet give a theorem-by-theorem audit sufficient to establish that the hyperplane/length-two quotient identification, as a closed scheme over arbitrary nonreduced bases, is new in that broader literature.

I am **not** claiming here that the theorem is known. I am saying the current literature section does not yet establish the contrary at the level needed for a top-four novelty judgment.

# 9. The strongest old unrestricted problems remain outside the new theorem package

Revision 117 is admirably explicit that it does not solve the unrestricted ambient Grassmannian.

That honesty also exposes the current limit.

The complete archival manuscript still contains:

- the unrestricted quadratic failure loci;
- the excess regime where only maximal-dimensional components are classified;
- the unrestricted hyperplane scheme with embedded evaluation-curve structure not fully determined;
- the general polar residual formalism;
- higher-product sectors not promoted to a full ambient classification.

The new finite-contact family is no longer merely monogenic, and that is important. But the hard ambient problems that originally motivated the broadest claims remain separate.

A top-four paper does not have to solve every surrounding problem. It does, however, need one theorem whose significance is not primarily “a complete tractable family inside a harder unresolved ambient theory.” I do not yet see that theorem here.

# 10. Proof-level requests independent of venue

I did not find a counterexample to the new main theorems, but several statements should be made more formally before publication anywhere at a high level.

### 10.1 Construct the line bundle in the universal hyperplane theorem explicitly

The theorem says that (mathcal C_m) is the direct image of a line bundle on (Y). The local proof shows cyclicity after a choice of unit and gives local modules (R/I).

The global line bundle should be written down canonically—e.g. in terms of the universal rank-two quotient and the (m)-th power of the universal generating line—and the transition from the unit-normalized chart should be stated. This is probably straightforward, but the theorem currently states more global structure than the proof explicitly constructs.

### 10.2 Define the generating open functorially at the beginning of the finite-algebra section

The proof uses a smooth-local choice of a unit in the hyperplane and explains that geometric fibres admit such a choice. The manuscript should state the exact equivalent definitions of “generating” for a hyperplane subbundle and explain why the open of unit sections gives a smooth surjective cover.

This will eliminate any ambiguity about the relative-base argument.

### 10.3 Separate the two uses of the symbol (d) when citing Haiman

Haiman's Corollary 3.8.3 uses one index for the number of labelled points and another for the power. The manuscript's surrounding notation also uses (d) for the length of the contact divisor. The mathematical use is correct, but a reader should not have to reverse-engineer the notational substitution to verify the citation.

### 10.4 State precise cohomology-and-base-change hypotheses in the relative curve theorem

The relative statement currently says that the assertions hold for smooth projective families with the fibrewise hypotheses and locally free direct images. A fully relative theorem should specify exactly which direct images commute with base change and which surjections are being promoted from fibres.

The fixed-curve theorem is the important part; the relative add-on should not be broader than its written proof.

### 10.5 Identify the projective-line bundle in the moving hyperplane theorem

The phrase “a generating open of a projective-line bundle” is geometrically informative but can be more canonical. State the rank-two universal quotient on the nested divisor space and identify the projectivization whose unit-line open is being used. Then the smoothness theorem becomes visibly functorial rather than coordinate dependent.

These are not reasons for rejection at a specialist journal. They are the remaining proof-architecture cleanups I would require before acceptance anywhere.

# 11. Assessment of the R116 mandatory items

My disposition of the previous mandatory list is as follows.

| R116 item | v117 status | Referee assessment |
|---|---|---|
| E116.1 unique manuscript identity | closed for this round | v117 has a unique branch, source commit, and product head |
| E116.2 Ballico 1993 theorem-level comparison | **open** | manuscript correctly admits this |
| E116.3 primitive-element/index-form/discriminant audit | substantially closed | ABHS and classical index-form language are now explicit |
| E116.4 standalone primary descent lemma | closed | the new étale lemma addresses the prior proof-architecture objection |
| E116.5 novelty boundary of moving normalization | substantially closed | the manuscript now distinguishes classical index-form geometry from multiplication transport |
| E116.6 exact scope language | closed | conductor-containing families and the absence of an unrestricted Grassmannian theorem are explicit |
| E116.7 article identity | substantially closed | the 19-page geometry article is coherent and the 83-page version is clearly archival/complementary |
| E116.8 conductor threshold | closed on (mathbb P^1) | the rank-dependent bound and degree-two boundary family materially improve the theorem |

This is genuine progress. A new report should not continue treating E116.1, E116.4, E116.6, or E116.8 as open merely because they were open in the previous round.

# 12. New mandatory revisions arising from v117

The following are the issues I would require in a serious next revision.

### E117.1 — Complete the Ballico 1993 theorem-level comparison

Obtain the article, quote the relevant theorem hypotheses precisely, and give a result-by-result comparison with:

- the conductor transport;
- the fixed finite-contact failure schemes;
- the moving failure schemes;
- the hyperplane/length-two quotient incidence;
- and any claims about novelty of failure loci.

Do not infer disjointness from inaccessible full text.

### E117.2 — Perform a broader theorem-level novelty audit for the universal hyperplane result

The new flagship statement is an incidence between generating hyperplanes and rank-two algebra quotients. Compare it not only with monogenerator equations but also with the nearest subalgebra/Hilbert/nested-Hilbert constructions.

The manuscript needs to identify exactly which part is new:

- the conductor rank statement?
- the functorial equivalence?
- equality of all higher Fitting schemes?
- arbitrary-base-change compatibility?
- the global-section transport?

Those should not be bundled into one novelty claim.

### E117.3 — Reframe the three-plane theorem around what is actually new relative to Haiman

The all-powers primary identity is Haiman's theorem.

The paper's contribution is the exact stable multiplication realization of Haiman's ideal plus conductor transport. State this in the theorem discussion itself, not only in the literature section.

Then explain why realizing this ideal inside multiplication failure geometry has consequences that were not already visible from the diagonal arrangement alone.

### E117.4 — Push the multigenerator theory beyond the reduced stable three-plane case

This is the most important mathematical request.

A convincing next step would be one of:

- three-planes on nonreduced curvilinear divisors, with actual primary/embedded structure;
- three-planes in a class of noncurvilinear finite algebras;
- a (kge3) quotient theorem that produces new finite schemes beyond the Haiman diagonal arrangement;
- or a substantial theorem on the unrestricted ambient Grassmannian.

Any one of these could convert the current collection of complete families into evidence for a broader structure theory.

### E117.5 — Promote the finite-algebra theorem from defect-two universality to a higher-defect mechanism

The hyperplane theorem is universal because the conductor quotient has rank two. A top-four version should explain what survives for codimension-two or higher subspaces.

Even a clean obstruction theorem showing exactly why the hyperplane equivalence fails, together with a replacement moduli object in the next codimension, would deepen the paper considerably.

### E117.6 — Formalize the remaining relative statements

Write the universal line bundle, the unit-frame smooth cover, the relative curve base-change assumptions, and the moving projective bundle canonically.

This is a correctness/presentation requirement, not a significance requirement.

### E117.7 — Keep the 19-page primary article architecture

Do not re-merge the independent quadratic/statistical developments into the proof spine. The current separation is an improvement and should be preserved.

# 13. What would materially change the top-four assessment

More finite diagnostics, build receipts, or local examples will not change the venue recommendation. Nor would another round of sharpening the same rank-two contact formulas.

A renewed top-four case would need a theorem that changes the conceptual scale of the paper. Examples include:

1. **Nonreduced multigenerator classification.** Extend the three-plane theory to arbitrary multiplicity partitions or a broad noncurvilinear class, including embedded primes and powers.

2. **Higher-defect finite quotient theory.** Replace the special rank-two conductor quotient of a hyperplane by a systematic moduli description for codimension (rge2), and prove a nontrivial failure-scheme theorem from it.

3. **Unrestricted ambient geometry.** Prove a component/primary theorem on a substantial open class in an unrestricted Grassmannian, rather than after imposing conductor containment.

4. **A genuinely new diagonal-ideal theorem generated by multiplication.** Produce a scheme not already controlled by Haiman's big diagonal and prove a structural theorem about its powers, normalization, singularities, or associated primes.

5. **A new global conductor principle.** Extend the global-to-finite cokernel equivalence to a broader geometric setting where the regularity theorem itself has independent interest and yields new classifications.

The manuscript need not do all of these. But for a general top-four journal it needs at least one advance of comparable conceptual force.

# 14. Smaller comments

1. In the abstract, “for generating hyperplanes in any finite locally free algebra” should be followed immediately by “the controlling quotient has rank two,” so that formal ambient rank is not confused with quotient complexity.

2. The phrase “complete primary structure” should continue to name its base every time: fixed divisor, multiplicity stratum, or moving total scheme. v117 is much better about this than v116.

3. In the three-plane section, distinguish “the stable ideal is identified with Haiman's diagonal ideal” from “the multiplication problem proves the all-powers identity.” The latter would be misleading; the proof imports Haiman.

4. The noncurvilinear example should be presented as a warning/example, not evidence for a general embedded-component theorem.

5. The curve bound should remain explicitly sufficient rather than “sharp” language leaking from the (mathbb P^1) theorem.

6. Keep the build/test evidence in the repository but outside the mathematical argument. The current manuscript correctly says that finite tests are not proof certification.

7. The 83-page archival manuscript is useful for continuity, but a journal submission should submit the coherent primary article unless an editor specifically requests the historical complement.

# 15. Correctness assessment

I found no fatal counterexample to the following new v117 claims in the course of this review:

- the evaluation-kernel proof of the uniform (mathbb P^1) conductor bound;
- the hyperplane-subalgebra/rank-two-quotient correspondence;
- equality of the higher hyperplane failure ideals after unit normalization;
- the fixed curvilinear length-two quotient decomposition;
- the stated lengths and nilpotency indices of (G_r) and (H_{r,s});
- the smooth moving hyperplane incidence;
- the stable reduced-contact three-plane ideal;
- the all-powers three-plane identity as an application of Haiman;
- the revised étale primary descent lemma.

This is not a proof certification. It means only that my recommendation is **not** based on a discovered contradiction in these statements.

The main reason for rejection is instead that the strongest correct results have not yet been shown to exceed, in conceptual reach and novelty, a combination of:

- a sharp transport theorem;
- a defect-two conductor/Hilbert identification;
- explicit length-two finite algebra;
- and an application of a major existing theorem on diagonal ideals.

# 16. Final recommendation

Revision 117 is a substantial advance over revision 116.

The authors have:

- sharpened the conductor threshold;
- added an intrinsic curve transport theorem;
- proved a universal generating-hyperplane/rank-two quotient identification;
- computed all fixed curvilinear hyperplane primary fibres;
- identified a smooth moving total scheme;
- supplied an explicit noncurvilinear embedded example;
- added a genuine three-generator reduced-contact theorem;
- used Haiman's all-powers theorem correctly;
- supplied the missing étale descent lemma;
- and reorganized the work into a coherent primary article.

Accordingly, several criticisms in R116 should now be retired.

Nevertheless, I recommend **rejection in the present form at a general top-four mathematics journal**.

The decisive remaining reasons are:

- the formally arbitrary-rank hyperplane theorem is controlled by a rank-two quotient, so its complexity is still defect two;
- the strongest (k=3) theorem is restricted to reduced contacts in the stable range and imports its deepest primary-power identity from Haiman;
- the nonreduced multigenerator geometry is represented by an example rather than a classification;
- no substantial unrestricted ambient Grassmannian theorem has emerged;
- the positive-genus result is presently a strong transport criterion rather than a new geometry theorem;
- the novelty audit for the universal hyperplane/Hilbert incidence is not yet broad enough;
- and the nearest Ballico 1993 theorem-level comparison remains explicitly unresolved.

A strong specialist-journal paper may already be visible in the 19-page geometry article after the literature and relative-formalism issues are completed. For a renewed top-four submission, I would require a further structural theorem of the kind described in Sections 12–13, not another round of polishing or computational verification.
