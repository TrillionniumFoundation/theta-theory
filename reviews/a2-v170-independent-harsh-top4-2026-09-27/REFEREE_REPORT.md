# Independent harsh top-four referee report — A2 revision 170

## Status of this report and locked review object

**Author:** Qian Qi  
**Revision reviewed:** A2 revision 170  
**Revision branch:** `revision/a2-v170-ramified-contact-boundary-2026-09-26`  
**Locked revision tip:** `b8c3c1d7e59591b4e402272773d9bed5ae7c88ba`  
**Complete predecessor:** `81e0870e31078a3aaac6006b676ca54667e6d77a` (revision 169)  
**Authored build/source commit recorded by the package:** `038af5dc1703deb425764b6d6350ce3e13c31fde`  
**Controlling earlier report:** second independent v167 report at `f50f6a7b194adbb42813988d3e68a43d71ccc520`  
**Earlier independent report:** first v167 report at `be1987dd1a37064c0bea291d7ad38ccd12cc5951`  
**Date of this report:** September 27, 2026

The locked submission consists of:

1. *Finite failure schemes and the reconstruction of quadratic pencils* — Paper I, 76 pages;
2. *Conductors and ramified Hilbert boundaries of polynomial contacts* — Paper II, 135 pages;
3. a 202-page preservation master, explicitly described as an audit object rather than a third submission.

The principal v170 additions are the two source modules

- `ramified-boundary-v170.tex`;
- `conductors-and-lifts-v170.tex`;

along with revised front matter, two itemwise responses to the v167 reports, a theorem-dependency map, a theorem index, a literature addendum, exact finite checks, build receipts, and preservation manifests. I read the two new mathematical modules in full, checked their placement in the assembled Paper II, examined the front matter of both papers, the response to the controlling report, the dependency map, the literature audit, the exact-check record, the build workflow, and the relevant inherited chain-model statements on which the new theorem depends.

This report is based on the exact locked tip above. It does not amend either v167 report and does not treat those reports as reviews of v169 or v170. At the time this report was prepared, no later A2 revision branch was present.

The standard applied here is that of *Annals of Mathematics*, *Acta Mathematica*, *Inventiones Mathematicae*, or *Journal of the AMS*. At that level, correctness is necessary but not sufficient. The main theorem must also have exceptional conceptual force, an invariant formulation whose importance is visible beyond the chosen coordinates, a convincing relationship with the existing literature, and a presentation that allows an expert referee to verify the central route without navigating a cumulative repository archive.

## Recommendation

**Reject the v170 two-paper package for a top-four general mathematics journal. I would not recommend another revision round at that level.**

This recommendation is not based on a claim that v170 is cosmetic, empty, or obviously false. On the contrary, v170 contains a genuine and technically competent advance over v167 and v169. For the marked family

\[
[t^a:u^\rho s^a:v^\sigma st^{a-1}],
\qquad a\ge 2,\quad \rho,\sigma\ge 1,
\]

it computes the normalized Rees surface, all toric charts, cyclic quotient indices, the complete scheme fibre over the coefficient origin, its generic multiplicities and exact nilpotence order, the conductor through the crossings, the residue degrees and ramification indices of the normalization, and the root labels forgotten by the embedded Hilbert point. It also gives a coherent marked-root-cover compatibility statement. These are real results.

I found no immediate counterexample to the displayed fan, determinant, multiplicity, conductor, or residue-degree formulas in their stated domain. The new theorem is materially stronger than a collection of low-order examples, and the manuscript is now unusually explicit about the distinction among the unnormalized Hilbert graph, its normalized parameter surface, the scheme fibre of that surface, and the embedded universal-curve fibres.

The reason for rejection is instead structural and editorial. The central v170 theorem is an explicit toric and semigroup classification of one rigid, marked, two-parameter monomial family and its diagonal coefficient covers. The manuscript itself correctly concedes that it does **not** classify the full coefficient graph over `B_a`, higher-corank boundaries, singular Kronecker strata, simultaneous unequal contacts, or the full fibres relevant to arbitrary quadratic-pencil degenerations. The normalization and conductor calculation is useful, but its conceptual reach remains far below the breadth suggested by the surrounding two-paper package. Most of its mechanism is classical monomial blow-up, semigroup normalization, toric ramification, and a codimension-one conductor calculation, specialized carefully to the chosen family.

Paper II could become a strong specialist article after a major reconstruction and drastic reduction. Paper I contains a striking inverse theorem that may deserve serious independent attention, but it should be evaluated as a separate submission by a referee prepared to audit that theorem from first principles. The present package asks one editorial decision to certify two long and logically distinct projects, while the repository itself acknowledges that Paper I has not received an external independent full proof audit and that a complete theorem-level comparison with a potentially relevant 1993 source has not been obtained.

---

## 1. What revision 170 genuinely achieves

### 1.1 A normalized model for every diagonal coefficient cover of the marked chain

Starting from the unramified chain model `T_a`, the revision pulls back by

\[
b=u^\rho,\qquad c=v^\sigma
\]

and normalizes. With

\[
g_i=\gcd(\rho,i\sigma),\qquad
n_i=\left(\frac{i\sigma}{g_i},\frac{\rho}{g_i}\right),
\]

the compact rays of the normalized fan are explicit for every `1 <= i <= a`. The consecutive determinants give the cyclic quotient indices. The relative divisors of `u` and `v`, the relative canonical coefficients, and the rational intersection numbers follow from the same fan.

This is the correct kind of answer for the stated monomial problem. It replaces a vague instruction to normalize chart by chart with a single global fan and a semigroup formula in every Rees degree.

### 1.2 A scheme-theoretic parameter fibre rather than only a cycle

The strongest new point is not the fan itself, but the claim that the full ideal `(u,v) O_Z` is divisorial on every normalized cone. This yields a Cohen–Macaulay pure one-dimensional fibre, no embedded associated points, generic length

\[
\ell_i=\frac{\min(\rho,i\sigma)}{g_i}
\]

along the `i`th exceptional component, and exact nilpotence order `max_i ell_i`. The reduced fibre is a chain of projective lines with nodal crossings even when the ambient toric surface has cyclic quotient singularities.

This is a meaningful strengthening over merely reading multiplicities from a divisor cycle.

### 1.3 A global conductor through the toric crossings

At the generic point of the `i`th old exceptional curve, the transverse equation is a binomial

\[
u^\rho=w v^{i\sigma}.
\]

The revision computes the branch conductor and then uses an `S_2`/depth argument to rule out an additional conductor condition supported only at a crossing. The resulting conductor on the normalization has order

\[
\kappa_i=\frac{\rho i\sigma-\rho-i\sigma}{g_i}+1
\]

along `D_i`. The equal-power case is supplemented by explicit chart generators.

This is a genuine scheme-theoretic calculation, not merely a generic ramification count.

### 1.4 Residue power maps and lost normalization labels

On the open orbit of `D_i`, the residue coordinate

\[
\zeta_i=\frac{u^{\rho/g_i}}{v^{i\sigma/g_i}}
\]

maps to its `g_i`th power on the old Hilbert boundary. Thus a general old boundary point has `g_i` normalization lifts, while a torus-fixed endpoint has one. The manuscript explains that the embedded curve remembers only the power, not the chosen root, and realizes all roots by actual coefficient arcs.

This is a clean illustration of the difference between equality of embedded Hilbert limits and equality of normalization points.

### 1.5 Marked logarithmic compatibility

The normalized model is characterized as the normal modification simultaneously principalizing the marked ideals `(u^rho,v^{j sigma})`. Successive root covers compose canonically, and unit changes of the two marked boundary parameters preserve the construction. This is the natural functoriality available in the chosen marked category.

The revision is appropriately careful not to claim invariance under arbitrary unmarked coordinate changes.

### 1.6 Documentary honesty

The package repeatedly distinguishes finite exact checks from proofs, build success from mathematical verification, and source preservation from journal merit. It also states the limits of the Ballico comparison and the absence of a full independent Paper I audit. This candour is a strength.

---

## 2. Correctness audit of the new ramified-boundary theorem

I did not find a short contradiction to the central v170 formulas. The new route is substantially more coherent than the v167 all-order determinantal encoding. Nevertheless, several arguments that are probably repairable are too compressed for a theorem carrying the full scheme-theoretic weight claimed in the abstract.

### 2.1 Flat base change, integrality, and the full graph

The identification

\[
Y=T_a\times_{S_a}S'=\operatorname{Bl}_{I} S'
\]

under the finite flat map `S' -> S_a` is credible. The raw chart equations are hypersurfaces or codimension-two complete intersections, so the local complete-intersection assertion is plausible.

The integrality argument should, however, be rewritten in a completely formal way. A dense torus with a domain coordinate ring does not by itself exclude embedded or vertical structure on an arbitrary scheme. What is available here is stronger: `Y -> T_a` is finite flat, hence torsion-free over the integral source, and its generic algebra is the field extension `k(u,v)/k(b,c)`. Localizing into that field proves that the finite flat algebra is a domain. This is the argument the paper should state.

The manuscript should also explicitly prove that the displayed first, intermediate, and last raw charts cover the entire base-changed blow-up and not merely a birational model with the same generic torus.

### 2.2 Normalized Rees algebra

The inequalities for the normalized Rees algebra are consistent with the Newton polygon and the primitive rays. The observation that the degree-zero vectors together with any degree-one monomial generate the full ambient group explains why saturation occurs in the full lattice.

The proof is nevertheless too quick at the point where it passes from the rational cone to integral closure in every degree. The paper should define the exact affine semigroup, prove that its group is the claimed lattice, identify every facet including the nonnegative-coordinate facets, and then invoke the semigroup-normalization theorem. The current sentence “a rational positive combination becomes an element after clearing denominators” suppresses the distinction between saturation of a semigroup and membership in a fixed graded degree.

The raw-content shift also deserves a one-line graded-algebra isomorphism rather than the statement that it “does not change Proj.” The normalized algebra and the graph are distinct objects, and the proof should make every transition explicit.

### 2.3 The coordinate-ideal lemma

`lem:coordinate-ideal-v170` is the pivotal new lemma. Its conclusion is plausible and the elementary inequality argument is clever. It should not remain buried as a short local observation.

The revised proof should:

1. specify the character lattice and explain why negative exponents are allowed precisely when the two dual-cone inequalities hold;
2. separate the two same-side cases from the cone crossing the diagonal;
3. state explicitly why, in the crossing case, failure of divisibility by `u` can only occur at the high ray while failure of divisibility by `v` can only occur at the low ray;
4. identify the displayed monomial ideal with the intersection of the relevant height-one symbolic ideals;
5. justify reflexivity using the normal `S_2` property;
6. prove that the quotient has no zero-dimensional associated prime at every torus-fixed point.

The argument appears repairable, but the present form is not proportionate to the importance assigned to “the complete scheme fibre.”

### 2.4 Nodal crossings on a singular toric surface

The assertion that the reduced union of two adjacent invariant divisors is an ordinary node is likely correct: each invariant divisor is an affine line near the fixed point, their scheme-theoretic intersection is the reduced torus-fixed point, and the union is the corresponding fibre product over the residue field.

The current explanation through “coordinates generated by the `Delta_i`th powers” is too abbreviated. Quotients of coordinate axes by cyclic groups can easily conceal nontrivial scheme structure if the invariant-ring calculation is not written down. The paper should give the exact local quotient ring or the exact sequence

\[
0\to O_{D_i\cup D_{i+1}}\to O_{D_i}\oplus O_{D_{i+1}}\to k\to0
\]

and conclude that the completed local ring is `k[[x,y]]/(xy)`.

### 2.5 Exact nilpotence order

The upper bound follows from the divisorial orders of the radical ideal, and the lower bound follows after localization at a component of maximal generic length. This is convincing.

The paper should nevertheless distinguish ordinary powers from reflexive powers. On a singular normal surface, the product of two divisorial ideals need not already be reflexive. The needed inclusion is enough, but it must be stated as an inclusion of ordinary products obtained from valuation inequalities, not as an unqualified equality of divisorial sheaves.

### 2.6 The conductor-depth lemma

The intended principle is correct: a two-dimensional Cohen–Macaulay domain is `S_2`, hence it is the intersection of its height-one localizations inside its fraction field; a finite normalization then lets one test the conductor in codimension one. Consequently no additional conductor condition can be supported only in codimension two.

The proof should be rewritten more carefully. In particular:

- the height-one primes of `A` and those of `bar A` should not be conflated;
- the semilocal normalization of each `A_p` and its maximal ideals should be identified explicitly;
- the conductor should be written as the intersection, inside `bar A`, of the corresponding valuation ideals;
- the finite-length depth-lemma argument proving `A = intersection A_p` should be stated with the exact short exact sequence and the relevant depth inequality;
- the passage from formal closed-point binomial calculations to the generic codimension-one order should be made explicit.

I believe the intended result, but this is exactly the sort of codimension-two extension argument that a top-level paper should not compress into a paragraph.

### 2.7 Binomial conductor and residue degree

The branch conductor

\[
g r'q'-r'-q'+1
\]

for `U^r-V^q`, with `g=gcd(r,q)`, is consistent with the conductor of each primitive branch plus its intersections with the other branches. The delta formula is also consistent with the sum of branch deltas and pairwise intersection multiplicities.

The residue extension `w=zeta_i^{g_i}` and the ramification relation `e_i g_i=rho sigma` agree with the lattice map. These computations are among the cleanest parts of the revision.

The manuscript should state whether “residue degree” refers to the extension at the generic point of the divisor, while “`g_i` closed lifts” uses algebraic closedness of the ground field and a general nonzero closed residue. At present the two statements are adjacent enough that a reader could mistake one for a decomposition into `g_i` prime divisors; there is in fact one prime divisor mapping with residue degree `g_i`.

### 2.8 Normality criterion

The conclusion that `Y` is normal exactly when `rho=1` is plausible. When `rho=1`, the conductor coefficients vanish; when `rho>1`, the last coefficient is positive because `a sigma >= 2`.

This asymmetry in `rho` and `sigma` is initially surprising and should be highlighted geometrically. It is a consequence of the chosen marked family and the orientation of the chain, not a symmetric theorem about arbitrary two-variable monomial covers.

### 2.9 Marked principalization and logarithmic language

The universal property is valid in the marked category described: normal integral tests, dense coefficient torus, and invertibility of each marked monomial ideal. It should be formulated as an actual categorical terminal property, with the class of morphisms and the dense-open identification written explicitly.

The log-crepant equality is a standard toric equality. Calling the pair log canonical is reasonable after toric resolution, but the paper should state the `Q`-Cartier conventions and make clear that this is a parameter-space statement, not semistable reduction of the universal curves. The manuscript already says the latter; it should remain impossible to miss.

### 2.10 Exact checks and build evidence

The finite checks are substantial regression tests: hundreds of parameter triples, nearly one million cone-membership checks, finite normalization-module representatives, binomial gap counts, and root-cover composition. They increase confidence in the formulas.

They do not verify the general proofs. The package itself acknowledges this, correctly.

There is also a documentary issue: the final published tip `b8c3c1d...` has no attached GitHub commit status and no workflow run. The branch contains a workflow that built an earlier authored source commit and then self-published the final `[skip ci]` commit together with a build receipt. That is a reproducibility record, but it is not an independently enforced required check on the exact final tip. This is not a reason for mathematical rejection, but the distinction should be preserved in any publication claim.

---

## 3. Why the result remains below the top-four threshold

### 3.1 The theorem is complete only inside a very narrow marked slice

The word “complete” is repeatedly qualified in the body, and those qualifications are essential. The theorem treats the retained-coefficient graph of

\[
[t^a:b s^a:c s t^{a-1}]
\]

and diagonal covers of its two coefficient coordinates. It does not treat:

- the full coefficient space `B_a`;
- arbitrary deformations of the degree-`a` polynomial triple;
- higher-corank pencil strata;
- general singular Kronecker blocks;
- collisions of unequal contacts;
- simultaneous interaction among several unmarked local models;
- compactification across different generic Hilbert polynomials;
- a coordinate-free boundary object for all quadratic pencils.

These are not peripheral omissions. They are precisely the directions in which the marked chain calculation would become a general theory of the quadratic-pencil boundary.

The revision has solved the chosen slice very thoroughly. It has not transformed that slice into the general moduli statement needed to support a top-four claim.

### 3.2 The main mechanism is classical and the new conceptual layer is modest

The fan is the common refinement of the bends of

\[
\min(\rho p,j\sigma q),\qquad 1\le j\le a.
\]

The normalized Rees algebra comes from saturation of a monomial semigroup. The ramification indices come from a finite-index lattice map. The conductor is obtained from a binomial curve calculation and `S_2` extension. The log-crepant statement is toric.

The nontrivial work lies in carrying these mechanisms through the whole chosen family and keeping the parameter fibre, normalization conductor, and embedded curve fibre separate. This is valuable, but it is an explicit classification rather than a new organizing theory with broad consequences.

The corollary for the fibre of an arbitrary normal toric surface modification of the plane is elegant, but it is an elementary consequence of the coordinate-ideal lemma. It does not by itself elevate the paper to a general-journal breakthrough.

### 3.3 The manuscript does not establish a sufficiently strong external consequence

The revision provides examples with arbitrarily high contact order, nilpotence, and root-label loss. It compares the Hilbert graph with a fixed-source Quot contraction and preserves inherited discussions of tropical, Gröbner, and stable-map viewpoints.

What is missing is a theorem outside the constructed family that materially changes another subject: a new classification theorem for quadratic pencils, a new moduli compactification, a new invariant of singular pencils, a solution of a recognized problem, or a method that applies beyond monomial two-parameter surfaces. The paper explicitly avoids claiming such a consequence. That restraint is correct, but it also confirms the editorial assessment.

### 3.4 The presentation is a cumulative archive, not a publishable theorem architecture

Relative to the complete v169 package, the new mathematical core is concentrated in approximately 606 lines of two source modules. Paper II is 135 pages and the preservation master is 202 pages. The assembled source retains hundreds of earlier mathematical blocks, versioned labels, historical front matter, response crosswalks, and numerous appendices.

Preservation is useful for repository audit. It is not a substitute for editorial selection.

A reader of Paper II should encounter one self-contained chain:

1. intrinsic marked ideal system;
2. normalized blow-up theorem;
3. complete parameter fibre;
4. conductor theorem;
5. relation to embedded Hilbert limits;
6. one or two serious applications.

Instead, the central theorem remains surrounded by the residue of many revision rounds. The hard-coded cross-paper references, repeated version labels, and exhaustive preservation apparatus make it difficult to tell which statements are logically essential and which are historical accumulation.

At a top journal, the architecture must make the theorem feel inevitable. Here it still feels cumulative.

### 3.5 Paper I remains a separate, unverified high-risk theorem

Paper I claims that an unmarked, ungraded finite local algebra determines a complex quadratic pencil up to congruence, with a sharp truncation order and extensions to families. That is potentially the most conceptually striking theorem in the package.

Revision 170 does not supply a new independent proof audit of it. The package says so. The complete Ballico comparison also remains unavailable, with priority claims correspondingly narrowed.

This honesty is commendable, but an editor cannot infer correctness of Paper I from the toric completeness of Paper II. Nor should the 135-page boundary paper be used as contextual mass to raise the perceived significance of the 76-page inverse theorem. Paper I must stand alone, with its own specialist referee, its own complete literature comparison, and a proof presentation that does not depend on the repository pipeline.

### 3.6 The literature positioning is not yet adequate

The v170 literature addendum verifies the classical sources used for blow-ups, semigroup normalization, and toric ramification. It expressly says that it is not an exhaustive priority audit. The inherited audit also acknowledges a missing full comparison with a potentially relevant older paper.

For a specialist paper, this may be repairable. For a top-four journal, the authors must explain precisely which parts of the normalized blow-up, fibre, conductor, and root-cover package are new relative to the existing literature on complete ideals, normalized blow-ups of monomial ideals, toric surface fibres, conductors of semigroup rings, and logarithmic modifications. The current statement that the family-specific calculation is new is not enough.

---

## 4. Separate assessments of the two proposed papers

### 4.1 Paper I — *Finite failure schemes and the reconstruction of quadratic pencils*

**Recommendation:** reject as part of the present package; evaluate only as a separate submission after independent specialist verification.

The reconstruction theorem is bold and potentially important. Its claim is also sufficiently unusual that it requires a referee to check the entire invariant recovery chain: extraction of the first relation from an ungraded algebra, recovery of determinant rulings, support-rank orientation, nonlinear changes of generators, family descent, sharpness, and singular cases.

Nothing in v170 materially reduces that verification burden. The repository’s preservation hashes prove that the text was retained, not that the proof is correct. The boundary applications do not validate the inverse theorem.

Before resubmission, Paper I should:

1. be completely detached from Paper II except for an optional application section;
2. give a concise invariant statement and proof roadmap in the first pages;
3. isolate every place where characteristic zero or complex geometry is used;
4. provide a full theorem-level comparison with the relevant reconstruction and pencil-classification literature;
5. obtain an independent proof audit by an expert in matrix pencils, determinantal geometry, and Artin algebras;
6. remove repository-history material from the publication text.

### 4.2 Paper II — *Conductors and ramified Hilbert boundaries of polynomial contacts*

**Recommendation:** reject at the top-four level; encourage a major rewrite for a strong specialist algebraic-geometry journal.

Paper II now has a credible central theorem. Its strongest contribution is the scheme-theoretic combination of normalized Rees geometry, the nonreduced parameter fibre, the conductor through quotient-singular crossings, and the root labels forgotten by Hilbert coordinates.

To become publishable, it should be rebuilt around that theorem rather than preserving the entire development history. The marked nature of the result should be part of the title, abstract, and theorem statement. The paper should stop using the surrounding quadratic-pencil pipeline as a proxy for generality.

---

## 5. Detailed technical requests for a specialist resubmission

1. **Lock and state the exact object.** The paper should identify one submission source and one immutable commit or archive checksum. Build-generated publication commits should not be part of the mathematical exposition.

2. **Make `T_a` self-contained.** State and prove, or quote from a separately published theorem, the unramified chain model used by v170. A reader should not need a historical revision label to know what `T_a` is.

3. **Prove the raw-chart cover.** Derive the first, intermediate, and last equations from the affine charts of the chain blow-up and show that they cover `Y`.

4. **Rewrite the integrality proof.** Use finite flatness, torsion-freeness, and the generic field extension explicitly.

5. **State the precise semigroup.** Include all facets, its group, its saturation, and the grading. Explain why normalization in every degree gives the displayed algebra.

6. **Separate graph invariance from Rees presentation.** Preserve the v169 distinction among the raw evaluation ideal, its divisorial content, the primitive graph ideal, and the normalized Rees algebra.

7. **Promote the coordinate-ideal lemma.** Give it a full standalone proof with a diagram of the two cases in the cone and a precise symbolic-ideal formulation.

8. **Write the local node ring.** At every cyclic quotient crossing, compute the reduced union ring explicitly rather than relying on a sentence about invariant powers.

9. **Distinguish ordinary and reflexive powers.** This is necessary in the nilpotence argument on singular normal surfaces.

10. **Expand the conductor-depth lemma.** State the `S_2` intersection theorem, track primes under finite normalization, and identify the conductor as a divisorial intersection.

11. **Clarify generic residue degree versus number of closed lifts.** There is one divisor with a degree-`g_i` residue extension, not `g_i` divisors.

12. **Explain the asymmetric normality criterion.** Make clear why only `rho=1` appears and how this depends on the orientation of the marked family.

13. **Verify equal-power conductor generators on overlaps.** Write the units relating the first, intermediate, and last chart generators.

14. **Specify quotient types completely.** If cyclic quotient types are part of the theorem, give the congruence class of the weight in a consistent orientation and explain the ambiguity under coordinate exchange.

15. **State the category of the terminal property.** Objects, morphisms, dense torus, and marked ideals should all be explicit.

16. **Keep logarithmic claims proportional.** The log-crepant parameter pair is useful, but it is not a stable-reduction theorem for the curves and should not be advertised as one.

17. **Strengthen the arc-realization argument.** Verify generically base-point-free status of the whole projective map, not only nonvanishing of `u`.

18. **Add a nontrivial unequal-cover worked chart.** The `(a,rho,sigma)=(3,2,3)` numerical table is helpful; at least one affine normalization and conductor calculation should be written completely.

19. **Give a real novelty comparison.** Compare the coordinate-fibre lemma and conductor theorem with the literature on normalized monomial blow-ups and complete ideals, not only with general toric references.

20. **Separate proof from tests.** Retain the exact checks as supplementary files, but remove test counts from any argument for mathematical validity.

21. **Run read-only CI on the exact submission SHA.** A required workflow should compile and test the locked tip without committing generated outputs back to the same branch.

22. **Remove the preservation master from the submission package.** It may remain in the repository as an archive, but it should not be placed before editors or referees as a third object to inspect.

23. **Delete historical front matter from the active papers.** Prior front matters, response scripts, and version-specific source bundles are archival data, not publication content.

24. **Reduce Paper II aggressively.** The main theorem and proof should occupy the centre of a substantially shorter paper. Earlier tangential frameworks should be cited, split off, or omitted.

25. **Do not use response completeness as theorem completeness.** Answering all 66 referee items is good process hygiene; it does not imply that the resulting theorem meets the original generality or significance target.

---

## 6. Required editorial reorganization

A viable specialist submission would have the following form.

### Paper A: marked ramified Hilbert boundaries

A self-contained paper centred on:

- the marked polynomial-contact family;
- the primitive ideal system and unramified chain;
- normalized diagonal covers;
- the scheme fibre and exact nilpotence;
- the conductor and root-label map;
- marked logarithmic compatibility;
- a small number of applications and examples.

The paper should state openly that it is a classification of a marked two-parameter family, not a compactification of all pencil degenerations.

### Paper B: finite-algebra reconstruction of pencils

A completely separate paper centred on the inverse theorem, with its own literature, proof audit, and applications. The boundary paper should be at most one downstream application, not a logical support for the inverse.

The current preservation master should remain a repository object only.

---

## 7. Final assessment

Revision 170 is mathematically stronger than the versions reviewed at v167. It answers a legitimate criticism of those versions: the higher-contact marked boundary is no longer merely encoded by a huge determinantal vector or illustrated by one low-order slice. The authors now compute the normalized surface, all of its toric singularities, the complete parameter fibre, the global conductor, and the lost root labels for every contact order and every diagonal coefficient cover.

That achievement should be recognized.

It does not, however, produce a general theory of quadratic-pencil boundaries, a full higher-contact coefficient-space classification, or an external consequence of the breadth expected at the four general journals named above. The proof architecture remains cumulative, the literature positioning is incomplete, Paper I remains independently unaudited, and the package is far too large and historically layered for its actual central theorem.

**Final recommendation: reject for a top-four general mathematics journal.**

**Specialist outlook:** Paper II may become publishable after a major self-contained rewrite and a sharper novelty comparison. Paper I may merit independent consideration only after a separate expert audit and full literature positioning.

---

## Confidential note to the editor

The repository demonstrates exceptional effort, transparency, and preservation discipline. Those qualities should not be confused with the mathematical threshold of a top-four journal. I would not invite another incremental revision of this package. The next useful step is not revision 171; it is editorial decomposition into two independent papers, deletion of the historical accumulation from the active manuscripts, and fresh specialist refereeing of each central theorem.
