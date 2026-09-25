# Independent harsh referee report — A2 revision 157

## Manuscript and review object

**Submission package:**

1. *Finite failure schemes and the reconstruction of quadratic pencils* (Paper I, 60 pages);
2. *Reciprocal power ideals, complete quadrics, and pencil degenerations* (Paper II, 43 pages);
3. the 98-page preservation master containing both bodies and the inherited material.

**Author:** Qian Qi  
**Revision reviewed:** A2 revision 157  
**Revision branch:** `revision/a2-v157-universal-power-ideals-2026-09-25`  
**Locked branch tip:** `a6d34cd2bb2075c64015f3667dbf3f391665cefd`  
**Mathematical source commit:** `b1cde8e304c0572bdb436d8484f1c9b70333fd77`  
**Controlling complete prior report:** `review/a2-v153-materialized-independent-harsh-top4-2026-09-25`  
**Controlling report commit:** `52ebb8183433ad398f61958219b2af809f721824`  
**Principal new source:** `papers/A2-v17-boundary-information-coarsening/article/v157/universal-power-ideals-v157.tex`  
**Complete focused sources:** `reconstruction.tex` and `divisor-geometry.tex`  
**Review standard:** the proof-completeness, originality, conceptual depth, inevitability, and exposition standard expected at *Annals of Mathematics*, *Acta Mathematica*, *Inventiones Mathematicae*, or *Journal of the AMS*.

This is an owner-requested independent-referee-style report, not a journal-commissioned editorial decision. I reviewed the complete materialized v157 package rather than any source-lock or encoded staging object. I read the response to the complete v153 report, the new universal determinantal formula, the complete-quadric graph theorem, the boundary-contact theorem, the proposed incidence compactification, the multiplier-ideal corollary, the focused introductions, and the build and preservation records. I also re-read the portions of the inherited reciprocal-fibre and pencil-reconstruction theories needed to evaluate the asserted bridge between the two papers.

The build receipt reports complete compilations of 60, 43, and 98 pages, preservation of the predecessor mathematical blocks, clean references, and a rerun of the v155 finite checks. I use these records to identify the object under review and to assess reproducibility. Passing computations and preservation manifests are not proof certificates and do not enter the significance judgment.

## Recommendation

**Reject the v157 package in its present form for a top-four general mathematics journal.**

Revision 157 is a serious mathematical advance over the complete v153 article. The authors have responded directly to the central complaint that the divisor-fibre theory had not been connected to a native global boundary for quadratic pencils. The universal ideal identity is elegant, the scheme-theoretic power graph is identified with complete quadrics, boundary contacts recover regular-pencil Smith exponents, and the material has finally been divided into two independently compiling papers. These are substantial improvements, not cosmetic editing.

I did **not** find a simple counterexample to the universal determinantal formula, the complete-quadric graph identification, the contact-divisor formula, or the multiplier-ideal formula. My negative recommendation is not a concealed correctness rejection.

The difficulty is that the claimed conceptual bridge is weaker than the presentation suggests. The determinant-apolar algebra `B_{n,h}` is obtained as a chosen quadratic coefficient section of a reciprocal normalization fibre after fixing a decomposition and killing all other coefficient directions. The native vector space `V` used in the complete-quadric theorem is then introduced afresh. The paper does not prove that the original unmarked failure algebra of a pencil canonically contains, canonically quotients onto, or functorially reconstructs this particular `B_{n,h}` on the original source space. For the actual common boundary fibre constructed earlier from a pencil, the complementary coefficient space has dimension `n^2-1`, not `n`. Its determinant-apolar section therefore produces complete quadrics on a much larger auxiliary space, not the native complete quadrics of the original pencil.

The authors can of course first use Paper I to recover the pencil and its source `V`, and then form the classical complete-quadric compactification of `P(Sym^2 V)`. That is a legitimate consequence of reconstruction. It is not the stronger statement that multiplication in the original failure algebra intrinsically generates the native compactification. Likewise, pulling the already constructed finite locally free failure algebra back to a Hilbert-graph closure is valid, but every finite locally free algebra can be pulled back along every morphism. This does not show that the new boundary geometry controls its multiplication or its degenerations.

At the top-four level, this distinction is decisive. Most of the new global geometry is classical once the universal ideal formula is established: the graph becomes complete quadrics by a Rees-algebra calculation; smoothness, normal-crossing boundary, flags, and orbit strata are classical; the contact formula is the valuation form of symmetric Smith normal form; and the multiplier ideals are a specialization of known symmetric-determinantal formulas. The new universal identity is attractive and publishable, but its proof is assembled from the known apolar character, multiplicity-free symmetric Cauchy decomposition, and determinantal balancing. I do not see in the present package one new theorem of the scale and inevitability expected of the four general journals named above.

Paper II is now a coherent and potentially strong specialist paper. Paper I contains a striking inverse theorem and deserves serious specialist consideration if its long inherited proof is independently verified and the historical comparison is completed. The two-paper package, however, still does not reach the stated general-journal threshold.

---

## 1. What revision 157 genuinely accomplishes

### 1.1 The submission object is finally focused

The separation into a 60-page reconstruction paper and a 43-page divisor/power paper is a major expository improvement. Paper II now begins with its strongest independent algebraic statement rather than requiring the reader to traverse the entire reconstruction pipeline. The preservation master remains available without forcing it to be the primary reading object.

This substantially closes the architectural criticism in the v153 report, although Paper I still retains a very broad collection of reconstruction, moving-family, rigidification, covering, and spectral extensions.

### 1.2 The universal power-ideal formula is a clean theorem

Let `B_{n,h}` be the determinant-apolar algebra and let `J_p(A)` be the ideal generated by the coordinates of the `p`th power of the degree-one element associated with a symmetric matrix `A`. For `p=hq+s`, with `0 <= s < h`, the theorem asserts

\[
J_p(A)=I_q(A)^{h-s}I_{q+1}(A)^s
\]

for every symmetric matrix over every commutative complex algebra, including nonreduced and non-Noetherian bases.

This is stronger than a statement on closed points, radicals, integral closures, or discrete valuations. The arbitrary-base formulation is useful, and the nonreduced example correctly explains why fibrewise checking would be insufficient.

### 1.3 The whole simultaneous power graph is identified

Theorem 4.1 identifies the simultaneous graph closure of all nonzero power maps with the classical space of complete quadrics, scheme-theoretically and without an additional normalization. The exact transform

\[
J_p\mathcal O_{\mathrm{CQ}(V)}
=
\mathcal O_{\mathrm{CQ}(V)}
\left(-\sum_{r=1}^{n-1}(p-hr)_+E_r\right)
\]

is a useful compact formula. It explains precisely which common divisor must be removed from each power map and makes the independence of `h` transparent.

### 1.4 Boundary contacts do recover regular-pencil spectral exponents

For a regular pencil line, the pullbacks of the complete-quadric boundary divisors satisfy

\[
\operatorname{mult}_xD_r=e_{r+1}-e_r,
\]

where the `e_i` are the local symmetric Smith exponents. The second-difference formula recovering these contacts from power-zero lengths is correct-looking and gives a concrete relation between the power ideals and the classical elementary-divisor data.

This answers, in a literal and mathematically meaningful way, the previous request for boundary data that distinguish degeneration types rather than one common information-destroying limit.

### 1.5 The response is disciplined about classical input

The manuscript credits determinantal balancing, the apolar character, complete quadrics, symmetric determinantal multiplier ideals, and the orbit stratification as classical. It does not claim to have discovered complete quadrics or their normal-crossing boundary. This is a substantial improvement in novelty positioning.

---

## 2. Correctness audit of the universal determinantal formula

I find the proof credible, subject to several points of exposition and sourcing.

### 2.1 The representation-theoretic comparison has the right shape

The degree-`p` coefficient span of `ell_A^p` is dual to the degree-`p` piece of `B_{n,h}`. The quoted apolar character gives the multiplicity-free sum

\[
\bigoplus_{|\lambda|=p,\,\lambda_1\le h}
\mathbb S_{2\lambda}(V^*).
\]

The degree-`p` generators of `I_q^{h-s}I_{q+1}^s` form a `GL(V)`-stable subspace of the same symmetric algebra. The torus-weight bound excludes every summand with first row greater than `h`.

For the reverse inclusion, the product of leading principal minors with column lengths equal to those of `lambda` is a nonzero highest-weight vector. Repeated determinantal balancing changes those lengths to `q` and `q+1` while preserving the total. Multiplicity freeness then gives the full summand.

This is a convincing proof of equality in the universal polynomial ring.

### 2.2 Arbitrary substitution is legitimate

Both sides are ideals generated by explicit polynomial coefficient spaces. Once their equality is proved for the universal symmetric matrix, applying any homomorphism to a complex algebra sends the generators to the generators of the specialized ideals. No flatness of the specialization is needed. Thus the extension to nonreduced and non-Noetherian bases is not an illicit fibrewise argument.

### 2.3 The proof should distinguish the genuinely new statement from its classical ingredients more sharply

The theorem is a concise synthesis of three known facts:

1. the character of the determinant-apolar algebra;
2. the multiplicity-free decomposition of the symmetric coordinate ring;
3. determinantal balancing for products of minor ideals.

The paper credits all three, but it does not explain whether the resulting identity has already appeared in the literature under the language of invariant ideals, products of symmetric determinantal ideals, or apolar powers. A top-four novelty claim requires more than demonstrating that the authors did not find the exact displayed formula in a quick search.

### 2.4 Conventions should be frozen in one proposition

The paper moves among `V`, `V^*`, symmetric matrices, degree-one apolar variables, and congruence actions. The theorem is correct only after these identifications and dual conventions are fixed consistently. A short proposition explicitly identifying the coefficient map with the dual multiplication quotient, including all duals and determinant twists, would make this load-bearing step easier to audit.

---

## 3. The complete-quadric theorem is correct-looking but largely formal after Theorem 3.1

### 3.1 The simultaneous graph/blow-up lemma is sound

After the Segre embedding, the simultaneous rational map defined by ideals `K_1,...,K_a` is defined by all products of one generator from each ideal. Its graph closure is therefore the blow-up of the product ideal. Replacing the product by a positive power or by an invertible twist does not change the Proj.

Applying the universal formula yields, up to invertible factors,

\[
\prod_{p=1}^{nh-1}J_p
=
\left(\prod_{q=2}^{n-1}I_q\right)^{h^2}.
\]

The same graph calculation for exterior powers gives complete quadrics. This proves the scheme-theoretic identification.

### 3.2 This mechanism limits the novelty of the result

Once Theorem 3.1 is available, Theorem 4.1 is nearly an exercise in graph closures and Rees algebras. The smoothness, simple-normal-crossing boundary, flag description, and orbit stratification are inherited wholesale from the classical complete-quadric construction.

The theorem is a pleasant new realization of a classical compactification. It is not a new compactification theorem in the usual sense, and the paper should resist language suggesting that its geometry has been newly determined.

### 3.3 The exact classical blow-up reference should be made load-bearing

The manuscript gives a self-contained graph argument but relies on the classical identification of complete quadrics with the graph/blow-up of all symmetric minor maps. The final version should cite the exact theorem or construction establishing this scheme-level identification, not only broad references to complete quadrics and their birational geometry.

### 3.4 The orbit statement is classical

The assertion that congruence orbits are indexed by subsets of the boundary divisors is the standard wonderful-compactification orbit stratification. It should be presented as a corollary recalled for interpretation, not as one of the principal new outputs.

---

## 4. Audit of the contact-divisor theorem

I do not find a correctness blocker.

### 4.1 Extension to the complete-quadric space is standard

A rational map from the nonsingular open of a smooth projective curve to a proper separated variety extends uniquely over the missing points. Thus a regular pencil line has a unique lift to complete quadrics.

### 4.2 The local contact formula follows from symmetric Smith form

Over `C[[t]]`, a symmetric matrix can be diagonalized by congruence to

\[
\operatorname{diag}(t^{e_1},\ldots,t^{e_n})
\]

up to units, which can be absorbed by square roots. In the standard complete-quadric chart, the boundary parameters are the successive ratios, hence have orders `e_{r+1}-e_r`.

The second-difference formula for the power-zero lengths is then an elementary inversion of the piecewise-linear valuation function.

### 4.3 The theorem is useful but not conceptually deep enough to carry the package

The result translates between two established encodings of the same local Smith data: valuations of minors and contact orders with the complete-quadric boundary. It is a clean theorem and may be very useful in applications. It is not a new classification of pencils or a new orbit-closure theory.

### 4.4 The scope is regular pencils only

The theorem does not recover Kronecker minimal indices of singular pencils. The manuscript says so. Since Paper I advertises an inverse for every pencil, the central boundary theorem in Paper II covers only the regular part of that claim. Any summary stating that the new compactification organizes all pencils would be an overstatement.

---

## 5. The proposed pencil compactification is too formal to be a top-four payoff

Proposition 6.1 takes the graph closure of the map from a dense open of the pencil Grassmannian to a Hilbert scheme and normalizes it. This always produces a normal projective birational parameter space with a flat universal Hilbert family.

The scheme-theoretic incidence argument using flatness and torsion freeness is correct. The construction is also naturally equivariant.

The problem is not existence or correctness. The problem is mathematical content.

The proposition does not determine:

- the boundary of `widehat G`;
- whether `widehat G` is smooth, Cohen–Macaulay, or singular;
- its exceptional divisors or discrepancies;
- the degree or fibres of `rho` over any nontrivial stratum;
- which extra or embedded components appear in a limiting Hilbert fibre;
- a modular interpretation of those fibres;
- the relation to standard compactifications of pencils or maps;
- extension of the effective quotient stack;
- a universal property distinguishing this closure from many other graph compactifications.

Moreover, the statement that the original finite failure algebra lives on `widehat G` is obtained by pulling back an already existing finite locally free algebra along `rho`. That is automatic under arbitrary base change. It does not show that the Hilbert boundary controls the algebra or that the algebra selects this compactification.

Calling this a “projective incidence compactification carrying the actual failure family” is literally correct. Treating it as the sought-after global synthesis would be misleading. At present it is a container, not a structural theorem about the boundary.

---

## 6. The central conceptual gap: the auxiliary apolar section is not the original failure algebra

This is the most important issue in the revision.

### 6.1 The quadratic section depends on choices

The reciprocal-fibre construction begins with a decomposition

\[
E=\mathbf C a\oplus W
\]

and then sets every coefficient family except `Q_2` equal to zero. The paper explicitly acknowledges that this section is `GL(W)`-equivariant but is not invariant under an arbitrary change of the decomposition.

Thus `B_{d,h}` is a distinguished section only after auxiliary data have been selected. It is not an intrinsic quotient of the unmarked reciprocal fibre as presently formulated.

### 6.2 The native vector space is introduced independently

The complete-quadric theorem then starts with a vector space `V` of dimension `n` and the algebra `B_{n,h}`. This produces `CQ(V)`.

For the actual common boundary fibre previously obtained from an `n`-dimensional quadratic pencil, however, the complementary coefficient space has dimension `n^2-1`. Its quadratic section is `B_{n^2-1,h}`, and its complete-quadric graph would be `CQ(C^{n^2-1})`, not the native `CQ(V)` of the pencil.

The manuscript does not identify a canonical `n`-dimensional subspace inside that large coefficient space whose section is the native one. Nor does it derive such a subspace from the abstract unmarked failure algebra.

### 6.3 Reconstruction followed by an external classical construction is not the same theorem

Paper I can recover the pencil and its source vector space. Once `V` is known, one may of course form `CQ(V)` and lift the pencil line. But then complete quadrics are being constructed from the recovered pencil by their classical definition.

This is a valid consequence of the inverse theorem. It is not evidence that the multiplication table of the original failure algebra itself contains the universal power graph as a canonical internal object.

### 6.4 The abstract and introduction should be rewritten around the weaker, accurate claim

A defensible claim is:

> certain reciprocal normalization fibres possess determinant-apolar coefficient sections whose power maps realize complete quadrics; after independently reconstructing a pencil, the same universal ideal theory reads its regular spectral data.

The stronger suggestion that one finite failure algebra intrinsically determines the native complete-quadric boundary through its multiplication has not been proved.

A top-four revision should either prove the stronger functorial extraction or make the auxiliary nature of the construction central rather than parenthetical.

---

## 7. Multiplier ideals and thresholds

The formulas are plausible and fit the standard symmetric determinantal resolution.

The total transform of `J_p` follows from Theorem 4.1. The discrepancy along the divisor over the rank-`r` locus is the codimension minus one. The valuation ideal is the corresponding symbolic power of the symmetric determinantal prime. Intersecting these conditions gives the displayed multiplier ideal and the minimum ratio gives the log canonical threshold.

This is a useful corollary, but the manuscript itself identifies it as a specialization of the classical symmetric-determinantal calculation. It should not be counted as an independent originality pillar. The final paper should state precisely which part, if any, is not already immediate from the cited general theorem after substituting the exponents supplied by Theorem 3.1.

---

## 8. Assessment of Paper I

Paper I is much easier to read after the split. Its central statement remains striking:

> an unmarked, ungraded finite local algebra at the sharp order `n^2+2n-4` recovers every complex quadratic pencil up to congruence, including singular pencils.

The moving-family and local-algebra forms, coefficient-support orientation, and nonlinear-automorphism analysis are serious mathematics. The prior reports have repeatedly found no short counterexample to the main inverse mechanism.

Nevertheless, the top-four significance issue remains.

The failure algebra is deliberately constructed so that its first nonzero relation encodes the pencil coefficient line. The work lies in proving that this encoding remains recoverable after forgetting the grading, coordinates, tensor factors, and linearity of automorphisms. That is nontrivial. It is different from discovering unexpected Torelli power in a standard invariant of established independent importance.

Paper II was intended to make the first relation geometrically inevitable. Revision 157 improves that case, but the noncanonical-section problem above prevents the complete-quadric geometry from fully supplying the missing inevitability.

The theorem-level comparison with Ballico 1993 also remains unavailable. The authors are right not to fabricate a nonanticipation statement, but the broad historical originality of a “failure scheme to reconstruction” program remains uncertified.

My recommendation for Paper I alone would still be rejection at the four general journals and serious consideration at a strong specialist venue, subject to a genuinely independent line-by-line verification of the long inherited proof.

---

## 9. Originality and scale

Revision 157 has a clear mathematical core, but its new parts form a chain of mostly classical mechanisms:

1. a known apolar character;
2. a known multiplicity-free decomposition;
3. known determinantal balancing;
4. a Rees-algebra graph calculation;
5. the classical complete-quadric compactification;
6. local Smith normal form;
7. classical symmetric-determinantal multiplier ideals.

The synthesis is elegant. The arbitrary-base ideal identity appears to be the genuinely new theorem in this chain. The remaining global results are natural consequences and interpretations of that identity.

For a strong specialist paper, such a synthesis can be fully worthwhile. For a top-four paper, I would expect at least one of the following:

- a canonical extraction of the native compactification from the original unmarked failure algebra;
- a new compactification with a nontrivial modular boundary theory;
- a classification of limiting failure algebras or resolved pencil curves;
- a new theorem for singular pencils, including minimal indices;
- a new structural theorem about complete quadrics not already classical;
- a major external consequence solving a recognized problem.

None is presently delivered.

---

## 10. Repository and submission-object issues

The v157 directory is complete and reproducible. However, the repository root file `CURRENT_REVIEW_ENTRY.md` still declares revision 155 as the current review object and points to the v155 sources and receipts. This is inconsistent with the v157 branch and its README.

For a source-bound external review, there must be one unambiguous controlling entry naming:

- revision 157;
- the branch tip `a6d34cd...`;
- the mathematical source commit `b1cde8e...`;
- the two focused PDFs;
- the controlling prior report;
- the v157 build receipt.

This is not a mathematical defect, but it is a preventable provenance defect in a repository that places unusual emphasis on auditability.

The distinction between the author source commit and the subsequent bot materialization commit should also be stated consistently. The present build receipt does this correctly; the root entry does not.

---

## 11. Specific technical and expository requests

These points should be addressed even for specialist publication.

1. **State the exact intrinsic status of `B_{n,h}`.** Is it a canonical quotient, a quotient after choosing a splitting, or merely an abstract algebra known to occur as some coefficient section? The present text supports only the latter two descriptions.

2. **Separate the source space of the pencil from the coefficient complement of the reciprocal fibre.** Do not use the same letter `V` in a way that obscures the dimension mismatch between `n` and `n^2-1` in the actual common boundary example.

3. **Temper the opening claim.** “Multiplication in a determinant-apolar algebra determines complete quadrics” is correct. “The original finite failure algebra determines its native complete quadrics through multiplication” is not proved.

4. **Isolate the coefficient-map identification.** Give one proposition fixing all duals, congruence conventions, and determinant twists used to identify `(B_{n,h})_p^*` with the universal coefficient span.

5. **Strengthen the novelty audit for Theorem 3.1.** Search and compare at theorem level with invariant-ideal and determinantal-product literature, not only the references supplying the ingredients.

6. **Cite the exact graph/blow-up theorem for complete quadrics.** The broad classical references are not a substitute for the precise scheme-level identification used in the proof.

7. **State the simultaneous graph lemma with hypotheses.** Record the common domain of definition, the Segre embedding, nonzero ideals, and the fact that the blow-up of the product lands in the Segre variety.

8. **Clarify projective twists.** On `P(Sym^2 V)`, identify the line-bundle degrees of the power coordinates and explain explicitly why invertible factors may be discarded in the blow-up calculation.

9. **Cite symmetric diagonalization over a DVR.** The contact theorem depends on congruence Smith form, not merely ordinary left-right Smith form.

10. **Define “full Segre symbol” precisely.** State whether the projective positions of the spectral points and the local partitions are both included, and under which reparametrization equivalence.

11. **Keep the regularity restriction visible.** The contact theorem does not treat singular pencils or minimal indices.

12. **Do not oversell the orbit corollary.** The complete-quadric orbit stratification is classical and should remain interpretive background.

13. **Give the compactification a universal property or compute its boundary.** Without one of these, Proposition 6.1 is a standard graph-closure construction rather than a major theorem.

14. **Do not count algebra pullback as integration.** Explain what new interaction, beyond base change, occurs between the failure multiplication and the limiting Hilbert curves.

15. **Classify at least one nontrivial limiting Hilbert fibre.** An explicit boundary calculation would materially strengthen the compactification claim.

16. **Separate the multiplier-ideal corollary from the new contribution.** Identify exactly what is inherited from the cited symmetric-determinantal theorem.

17. **Update `CURRENT_REVIEW_ENTRY.md`.** The current v155 entry is stale on the v157 branch.

18. **Pin the two review objects in the root entry.** Paper I and Paper II should be named separately; the preservation master should not be mistaken for a third submission.

19. **Keep the source/materialization distinction explicit.** The mathematical source is `b1cde8e...`; the reviewed branch tip is `a6d34cd...`.

20. **Do not use the finite checks as evidence for the general identity.** The manuscript mostly obeys this; executive summaries should do so as well.

21. **Retain the Ballico limitation in the submitted papers.** It should not live only in repository metadata.

22. **Reduce Paper I further.** Covering maps, stack rigidification, spectral specializations, and all moving variants should remain only if they are indispensable to the central sharp inverse.

23. **Explain why the two papers are mathematically independent.** Embedded cross-reference maps solve compilation, not logical dependence. Each paper should state exactly which results of the other are inputs.

24. **Remove “canonical” wherever choices remain.** In particular, a coefficient section selected by `E=Ca\oplus W` is not canonical under the full automorphism group without an additional argument.

---

## 12. Scorecard against the complete v153 report

### 12.1 Supply a global native boundary

**Substantially addressed at the level of an auxiliary universal power algebra.**

The power graph is complete quadrics and its contact divisors recover regular-pencil spectral exponents. This is real progress. The missing step is intrinsic extraction of that algebra and graph from the original unmarked failure algebra.

### 12.2 Construct a meaningful compactification carrying the failure family

**Addressed literally, but weakly.**

A normal projective Hilbert-graph closure is constructed and the existing finite flat algebra is pulled back. No substantive boundary structure or modular interpretation is proved.

### 12.3 Add higher reciprocal-fibre invariants

**Addressed in part.**

The determinant-apolar sections, Hilbert functions, lengths, socles, Lefschetz behavior, block Betti tables, and a small full-fibre resolution are meaningful additions. The whole multivariate reciprocal fibre remains largely open.

### 12.4 Split the paper

**Closed.**

Two complete focused papers are now supplied. This materially improves readability.

### 12.5 Clarify acting groups and degeneration data

**Improved.**

The native congruence action and the larger cotangent-coordinate action are distinguished. Boundary points and boundary-contact arcs are also correctly distinguished.

### 12.6 Complete the historical comparison

**Open.**

Ballico 1993 remains unavailable at theorem/proof level, and no broad nonanticipation conclusion is justified.

---

## 13. Conditions for another top-four evaluation

I would not recommend another top-four round triggered by additional exact checks, another classical invariant of `J_p`, or a further repackaging of complete quadrics.

A serious new round should contain at least one theorem of genuinely new global scale, for example:

1. a canonical, choice-free functor extracting the determinant-apolar power algebra and native complete-quadric boundary directly from the original unmarked failure algebra;
2. a compactification of the effective pencil-failure moduli problem with a computed and modularly meaningful boundary;
3. a classification of substantial families of limiting Hilbert fibres and their failure algebras;
4. an extension of the contact theory to singular pencils that detects minimal indices as well as elementary divisors;
5. a new structural theorem about complete quadrics or symmetric determinantal ideals not already formal from the classical resolution;
6. a major external application showing that the failure invariant solves an independently recognized problem.

The theorem-level historical comparison with the closest named failure-locus predecessor should also be completed through a legitimate source, or the broad priority rhetoric should be abandoned permanently.

---

## 14. Final assessment

Revision 157 deserves substantial credit. It is complete, reproducible, split into two readable objects, and mathematically stronger than every earlier A2 version I have reviewed. The universal determinantal formula is elegant. The complete-quadric realization is clean. The boundary-contact formula gives an actual degeneration invariant. The authors have answered the prior report with theorems rather than with more metadata or finite experiments.

I therefore reject any characterization of v157 as a cosmetic or merely engineered revision.

I nevertheless recommend rejection for *Annals*, *Acta*, *Inventiones*, or *JAMS*. The new global theory is built from an auxiliary determinant-apolar section whose relation to the original unmarked failure algebra is not canonical at the crucial point. Once the universal ideal identity is accepted, most of the complete-quadric, orbit, contact, and multiplier geometry follows from classical constructions. The proposed pencil compactification is a standard normalized Hilbert-graph closure with no computed boundary, and the presence of the failure algebra on it is obtained by formal base change. Paper I remains technically ambitious but centered on a deliberately information-bearing invariant, while the closest historical comparison remains incomplete.

The appropriate assessment is therefore:

**Reject the v157 package in its present form for a top-four general mathematics journal.**

**Paper II is a credible candidate for a strong specialist algebraic-geometry, commutative-algebra, or invariant-theory venue after narrowing its claims and clarifying the noncanonical auxiliary section. Paper I likewise deserves specialist consideration after independent proof verification and sharper historical positioning.**
