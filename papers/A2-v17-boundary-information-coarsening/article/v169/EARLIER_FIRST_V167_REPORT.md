# Independent harsh referee report — A2 revision 167

## Manuscript and review object

**Submission package:**

1. *Finite failure schemes and the reconstruction of quadratic pencils* (Paper I, 75 pages);
2. *Determinantal models and Hilbert limits of quadratic pencils* (Paper II, 113 pages);
3. the 180-page preservation master containing the complete mathematical bodies of both papers, explicitly not a third submission.

**Author:** Qian Qi  
**Revision reviewed:** A2 revision 167  
**Revision branch:** `revision/a2-v167-determinantal-hilbert-states-2026-09-26`  
**Locked complete branch tip:** `27101d0c3c45703e1a4fa96001d11f6b059cfc5e`  
**Authored build/source commit:** `504f78b3047ceccb0ffed5b17c6803d6c93e7398`  
**Controlling prior report:** `reviews/a2-v166-independent-harsh-top4-2026-09-26/REFEREE_REPORT.md`  
**Controlling prior-report commit:** `d5dd2e67b56c96f0a003e38e720918eba05239ca`  
**Principal new sources:**

- `papers/A2-v17-boundary-information-coarsening/article/v167/determinantal-states-v167.tex`;
- `papers/A2-v17-boundary-information-coarsening/article/v167/two-wall-slice-v167.tex`;
- `papers/A2-v17-boundary-information-coarsening/article/v167/horizontal-comparison-v167.tex`;
- `papers/A2-v17-boundary-information-coarsening/article/v167/local-algebra-clarifications-v167.tex`;
- `papers/A2-v17-boundary-information-coarsening/article/v167/effective-states-v167.tex`.

**Complete focused sources:** `reconstruction.tex` and `divisor-geometry.tex`.

**Review standard:** the proof-completeness, originality, conceptual depth, inevitability, breadth, and expository standard expected at *Annals of Mathematics*, *Acta Mathematica*, *Inventiones Mathematicae*, or *Journal of the AMS*.

This is an owner-requested independent-referee-style report, not a journal-commissioned editorial decision. I reviewed the complete materialized v167 package with particular attention to the new determinantal graph theorem, the finite-jet and decorated-chamber statements, the complete two-wall calculation, the strict-base-change comparison, the local extension and toric statements, the response to the v166 report, and the inherited theorems on which the new assertions depend. I also re-read the relevant fixed-target comparison, first nonreduced fibre, horizontal-main-component construction, universal power-ideal theorem, and sharp inverse in order to assess the actual logical and conceptual reach of the revision.

The build receipt records complete standalone sources and PDFs, clean compilation, byte-for-byte retention of all 390 predecessor mathematical blocks, and a rerun of the inherited exact checks. I use those records to identify the review object and assess reproducibility. They are not proof certificates, novelty certificates, or evidence for the editorial threshold.

## Recommendation

**Reject the v167 package in its present form for a top-four general mathematics journal.**

Revision 167 is a genuine and substantial mathematical advance over v166. It directly answers one of the strongest requests in the preceding report: the manuscript no longer stops at an all-arc substitution-and-saturation recipe. It now gives an explicit projective evaluation matrix for every polynomial contact order, identifies the retained-coefficient Hilbert graph as the Rees blow-up of its maximal-minor ideal, proves pointwise finite determination of an embedded limit, constructs a finite decorated chamber decomposition for exact monomial coefficient arcs including all residue cancellations, and completely calculates a nontrivial nonsymmetric two-parameter slice. The latter produces an exact factorization

`b^10 (b,c)^4 (b,c^2)^6`,

a smooth two-step blow-up, two genuine valuation walls, and five different embedded limit schemes with their components and multiplicities.

These are real theorems. They are not cosmetic editing, repository bookkeeping, a larger response letter, or numerical experimentation. I did **not** find a simple counterexample to the Gotzmann-degree construction, the maximal-minor graph theorem, the primitive Pluecker specialization rule, the Smith-module formulas, the finite decorated chamber theorem, the two-wall blow-up, the five-case limit table, the strict-base-change theorem, or the local toric class-group computation. My recommendation is therefore not a concealed correctness rejection.

The top-four problem is one of conceptual scale, inevitability, and reach.

The principal all-order theorem is, at its core, the universal construction attached to any rational family of Hilbert points: choose a Gotzmann degree, write the evaluation matrix, take its maximal minors as Pluecker coordinates, and identify the graph closure with the Rees blow-up of their ideal. The manuscript performs this construction correctly and explicitly for the polynomial-contact family. The existence and structural form of the construction, however, are classical consequences of Hilbert representability, the Grassmannian embedding, and the elementary graph/Rees lemma. What is new is the concrete input matrix and its use for specialization—not a new Hilbert-scheme principle.

The finite decorated chamber theorem is likewise exact but largely formal once one has a finite list of polynomial Pluecker coordinates. Subdivide weight space by equality of monomial weights, then stratify the residue torus by the first nonvanishing coefficient after cancellation. This produces a finite answer for exact monomial arcs, but it does not classify the irreducible components, normalization, nilpotent structure, incidence complex, or adjacency geometry of the higher-contact parameter fibres. It is a finite combinatorial encoding of polynomial evaluation, not yet a geometric compactification theorem.

The strongest genuinely geometric result is the two-wall slice `(f,g,r)=(x^2,b,cx)`. It is elegant, exact, and useful. It is also one specially chosen two-dimensional slice at the first nonreduced contact. The manuscript still has no complete fibre theorem for contact length at least three, no higher-corank Hilbert-boundary classification, no singular-pencil Hilbert-fibre theorem, and no general theory of interacting contacts of unequal lengths.

The effective failure-algebra interpretation remains mediated by the sharp inverse: the finite algebra first reconstructs the source and pencil, after which the classical polynomial-contact Hilbert problem is solved. This is a legitimate functorial application. It is not a boundary operation visible internally in the closed multiplication table before reconstruction.

Paper II is now a serious and potentially strong specialist paper. Paper I contains a striking inverse theorem and deserves independent specialist scrutiny. The two-paper package nevertheless remains below the threshold of the four general journals named above.

---

## 1. What revision 167 genuinely adds

### 1.1 One explicit Hilbert graph for every polynomial contact order

For

`B_a = {(f,g,r): f monic of degree a, deg g, deg r < a}`,

the manuscript fixes the Segre Hilbert polynomial

`P_a(l)=(a+1)l+1`

and computes a Gotzmann degree

`m=a(a+1)/2+1`.

The matrix `M_a` is the degree-`m` evaluation map

`H^0(P^1 x P^2,O(m,m)) -> H^0(P^1,O((a+1)m))`.

Its maximal minors are exactly the Pluecker coordinates of the generic graph. The theorem

`Gamma_a = Bl_{a_a}(B_a)`,  `a_a = I_max(M_a)`,

is therefore a genuine global projective description of the retained-coefficient graph over the full polynomial coefficient space. It is stronger than the seven-chart presentation in the sense that it produces one graph object and one ideal rather than a collection of local recovery charts.

### 1.2 DVR specialization is reduced to one primitive exterior vector

For a generically nonincident DVR arc, division of all maximal minors by their common valuation gives a primitive Pluecker vector. Its reduction is the special embedded Hilbert point. This retains the full scheme structure of the limiting curve, not merely the support or cycle.

The Smith-normal-form reformulation is useful: the sum of invariant-factor exponents is the common maximal-minor order, the largest exponent is the annihilator exponent of the finite degree module, and the saturated row lattice gives the special exterior line without enumerating every maximal minor.

### 1.3 The pointwise finite-jet theorem is positive and exact

If two coefficient arcs agree modulo `tau^(mu+1)`, where `mu` is the least maximal-minor valuation of the first arc, then their primitive minor vectors and special embedded curves agree. This is a valid finite-determinacy theorem for each individual generically nonincident arc.

The companion negative result is also correct in spirit and useful: no contact-order-only uniform coefficient-jet bound exists even for `a=2`.

### 1.4 Exact monomial profiles receive a finite decorated classification

For exact monomial coefficient arcs

`z_i = xi_i tau^(w_i)`,

the manuscript constructs a finite rational hyperplane arrangement from the monomial supports of all nonzero minors. It then partitions each cone by all possible leading-coefficient cancellations. The resulting projective vectors classify the special embedded curves on each residue stratum.

This is more responsible than a valuation-only tropical statement: equal-weight terms are allowed to cancel, and the next surviving weight is retained. The output is finitely many algebraic families, not a false claim of finitely many curves.

### 1.5 The nonsymmetric two-wall slice is completely calculated

On

`(f,g,r)=(x^2,b,cx)`,

the maximal-minor ideal is

`b^10 (b,c)^4 (b,c^2)^6`.

After removal of the principal factor, its blow-up is the blow-up of `(b,c)(b,c^2)`, equivalently two successive point blow-ups. The three affine charts and all transition functions are explicit. The exceptional fibre is a reduced chain with self-intersections `-2` and `-1`.

For `ord(b)=p` and `ord(c)=q`, the two actual walls are

`p=q` and `p=2q`.

The five limit ideals distinguish a primitive thick tail, a residue-dependent primitive tail, a doubled conic, a smooth conic, and a reducible conic giving a chain of three lines. The paper also determines component multiplicities, Cohen--Macaulayness, absence of embedded points, and the relative canonical divisor of the parameter surface.

### 1.6 Strict base change is now separated from full pullback

The horizontal Hilbert-main-component construction has a precise strict-base-change theorem. The new model after base change is the schematic closure of the pulled-back generic open inside the full pullback of the old model. Equality holds for flat base change, and the plane-blow-up example shows that it can fail under nonflat restriction.

The common-refinement operation on one fixed generic problem is also useful and honest. It gives comparison maps and cocycles without pretending that distinct generic Hilbert polynomials glue automatically.

### 1.7 Local extension and ramification statements are clarified

The manuscript now states the degree convention for the cotangent complex, writes an actual split algebra away from the nonsplit locus, and distinguishes the local obstruction sheaf from the global hyper-Ext group. The toric normalization calculation records primitive rays, quotient type, singular locus, and divisor class group for every ramification order.

### 1.8 The effective-family application is categorically responsible

The final corollary explicitly reconstructs the pencil first, then applies the polynomial-contact Hilbert graph. It does not claim that an arbitrary raw finite algebra contains a preferred specialization arc or an internal Hilbert state.

---

## 2. Correctness audit of the determinantal graph theorem

I found no direct correctness blocker. Several points should nevertheless be sharpened before publication.

### 2.1 The Gotzmann number is consistent

Writing `d=a+1`, the polynomial is `dl+1`. The displayed Gotzmann representation has `d` degree-one terms and `(d-1)(d-2)/2` constant terms, giving

`m=d(d-1)/2+1`.

The rank of the target degree space is `q=dm+1`, as stated. The use of the ordinary projective Hilbert scheme after the Segre embedding avoids an unproved multigraded regularity assertion.

### 2.2 The restriction to the Segre coordinate space is legitimate

Projective normality of the Segre embedding gives surjectivity

`H^0(P^5,O(m)) -> H^0(P^1 x P^2,O(m,m))`.

The fixed ideal of `P^1 x P^2` is therefore harmless when the Hilbert Grassmannian is rewritten in terms of the smaller vector space. This reduction should be stated as a named lemma rather than compressed into the main proof.

### 2.3 The evaluation matrix gives the correct Pluecker coordinates

On the base-point-free locus the graph is isomorphic to `P^1`, and restriction of `(m,m)` sections gives degree `(a+1)m` binary forms. The matrix `M_a` is exactly this evaluation map. Gotzmann regularity supplies surjectivity in the chosen degree, so its maximal minors are nonzero Pluecker coordinates.

### 2.4 Graph closure equals the Rees blow-up

For a rational map defined by generators of a nonzero ideal in a domain, the graph closure is the Proj of the Rees algebra. The manuscript proves this on affine ratio charts and correctly uses the Rees algebra rather than the symmetric algebra. Since the Hilbert scheme is closed in Pluecker space, the same graph closure lies in the Hilbert scheme.

This is correct. It is also completely classical and should remain clearly labelled as such.

### 2.5 The DVR extension argument is sound

Dividing the coordinates by their common valuation gives a primitive vector. Properness and separatedness of the Hilbert scheme yield the unique extension, and the Hilbert immersion identifies equality of projective coordinates with equality of embedded curves.

The manuscript correctly distinguishes equality on the graph from equality of points on its normalization. That distinction must remain in every summary.

### 2.6 The Smith formula is standard and useful

For a rank-`q` matrix over a DVR, the maximal-minor ideal has valuation equal to the sum of the invariant-factor valuations. The description of the finite cokernel and of the saturated row lattice follows.

The statement that the degree-`m` kernel generates the ideal sheaf should explicitly invoke the truncation consequence of `m`-regularity: the degree-`m` part generates the sheaf even though the homogeneous ideal may have lower-degree generators.

### 2.7 The pointwise jet bound is correct but intrinsically posterior

The proof that congruent coefficient jets give congruent minors is immediate and correct. The bound `mu+1`, however, is known only after computing the valuation of the same large determinantal system whose limit one is trying to understand. It is a posterior bound, not an a priori finite-determinacy theorem in Smith data, contact length, or a small list of intrinsic invariants.

This limitation is editorially important.

### 2.8 Generic base-point freeness is correctly detected by maximal rank

If the three forms have a common positive-degree factor, every evaluated section is divisible by its `m`th power, so the degree map cannot be surjective. Conversely, on the base-point-free locus regularity gives surjectivity. Thus nonvanishing of a maximal minor detects the stated generic open.

The paper should isolate this equivalence in a proposition because it is used repeatedly in the jet and chamber theorems.

---

## 3. Audit of the finite decorated chamber theorem

### 3.1 The finite subdivision is mathematically valid

Each maximal minor has finite monomial support. The hyperplanes

`(alpha-beta).w=0`

fix the weak ordering of all monomial weights on each cone. Grouping equal-weight terms and stratifying the residue torus by their successive cancellation patterns is a finite procedure. The displayed leading vector is consequently correct.

### 3.2 The theorem is essentially a universal polynomial-evaluation lemma

The same construction applies to any finite collection of polynomials defining a rational map to projective space. It is not specific to quadratic pencils, Hilbert schemes, or determinantal geometry once the minors have been written down.

The manuscript should formulate this general lemma separately and then state precisely what is special about the present matrix. Doing so would make the originality claim more, not less, credible.

### 3.3 The fan is enormous and intentionally nonminimal

The number and size of the minors grow explosively. Already at moderate contact order the matrix has thousands of rows and tens or hundreds of thousands of columns. The arrangement formed from all differences of all monomial exponents can be vastly larger than the actual Gröbner or tropical fan relevant to the graph.

No complexity bound, compressed representation, structural generating set, or minimality theorem is supplied. Calling the construction “explicit” is defensible in a formal sense but misleading if read algorithmically.

### 3.4 The exact-monomial domain is narrower than arbitrary boundary arcs

The stated arcs have positive weights for the variable coefficients, so they are centred at the distinguished origin of the chosen coefficient chart, with selected coordinates allowed to vanish identically. This does not by itself classify monomial arcs centred at an arbitrary boundary point with nonzero residue coordinates, nor does it provide coordinate-invariant chambers under translations or changes of contact chart.

One can adapt the polynomial argument locally, but that adaptation is not the theorem currently stated. The introduction and abstract should not suggest a full coefficient-space chamber decomposition without this qualification.

### 3.5 Residue cancellation is retained correctly

The locally closed residue partition is an important improvement over a generic-leading-term argument. It ensures that the theorem does not discard special coefficient relations.

Nevertheless, the result gives polynomial Pluecker vectors, not a geometric description of the curves they represent. For general `a`, the number of components, their multiplicities, singularities, and adjacency remain unreadable from the theorem without another substantial calculation.

### 3.6 “State” terminology requires a deeper literature comparison

The manuscript distinguishes coefficient weights from target-coordinate torus weights. That is necessary but not sufficient. The relevant comparison is not only with classical state polytopes but also with Gröbner fans of rational maps, tropical linear spaces and valuated matroids of the evaluation matrix, comprehensive Gröbner bases, Rees valuations, and tropicalization with coefficients.

Without that comparison, the exact novelty of the decorated chamber theorem remains uncertain.

---

## 4. Correctness audit of the two-wall slice

### 4.1 The row-monomial calculation supports the factored ideal

On the slice each column of `M_2` has one nonzero monomial entry. A nonzero maximal minor chooses one column in each row, so the maximal-minor ideal factors as the product of the row ideals. The listed thirteen row ideals multiply to

`b^10 (b,c)^4 (b,c^2)^6`.

This is a convincing structural calculation, not only a computer output.

### 4.2 The blow-up identification is credible

A principal nonzero factor does not alter a blow-up on the integral surface. The property that a positive-power product of nonzero ideals is invertible is equivalent to invertibility of the individual factors as fractional ideals. Therefore the blow-up of `(b,c)^4(b,c^2)^6` has the same universal property as the blow-up of `(b,c)(b,c^2)`.

The proof should be isolated as a general lemma; many readers will otherwise regard this step as suspicious.

### 4.3 The three affine charts and transitions are exact

The two successive point blow-ups give the charts

`(b,k)`, `(e,h)`, `(c,z)`

with transitions

`k=e^(-1), b=e^2h` and `z=h^(-1), c=eh`.

The universal curve ideals agree on overlaps after multiplication by the displayed units. The fixed target is retained throughout.

### 4.4 Flatness of the displayed curve families is adequately supported

The two Hilbert--Burch charts have height two on every fibre and the standard resolution. The primitive chart is a relative Cartier graph on the relevant affine pieces. These arguments support constant Hilbert polynomial `3l+1` and exclude an unnoticed component at infinity.

The final paper should give one compact proposition collecting the irrelevant-saturation and infinity checks for all three charts.

### 4.5 The five valued-arc limits follow from the chart valuations

The regions `p<q`, `p=q`, `q<p<2q`, `p=2q`, and `p>2q` correspond exactly to finite limits of `k=c/b`, `(e,h)=(b/c,c^2/b)`, and `z=b/c^2`. The residue parameters on the two walls are indispensable and correctly retained.

The formula

`mu=10p+4 min(p,q)+6 min(p,2q)`

follows directly from the factored ideal.

### 4.6 The component and Cohen--Macaulay statements are plausible

The primitive limits are local hypersurface models, and the conic limits have Hilbert--Burch resolutions. The listed minimal primes and multiplicities agree with the displayed ideals. The absence of embedded points follows from one-dimensional Cohen--Macaulayness.

For publication, each ideal decomposition should be written in the ordinary affine coordinate rings before being translated to ideal sheaves; the current proof moves quickly between these levels.

### 4.7 The boundary and discrepancy calculation is standard

The exceptional chain has self-intersections `-2,-1`. Pulling the first exceptional divisor through the second blow-up gives

`K_{T/S}=E_11+2E_21`.

This is correct and useful, but it remains a calculation on one smooth surface rather than a general discrepancy theorem for the all-order graph.

---

## 5. Audit of horizontal comparison and local algebra

### 5.1 Strict base change is correctly formulated

The relative Hilbert scheme commutes with base change. The new main component is the schematic closure of the generic section inside the full pullback of the old main component. The transitivity and cocycle statements follow because both routes take the same closure in the same ambient Hilbert scheme.

### 5.2 The equality criterion is useful but limited

Equality holds when the generic open remains schematically dense in the full product; flat base change supplies that condition. The blow-up-of-the-plane example is a good counterexample outside it.

This is comparison on one fixed generic Hilbert problem. It does not compare models whose generic fibres have different Hilbert polynomials.

### 5.3 Common refinements do not produce a canonical compactification

Taking the diagonal closure in a product gives a terminal common refinement of two proper integral modifications on the same dense open. This is standard birational geometry. It supplies a directed comparison category, but no minimal object, logarithmic structure, boundary complex, or canonical sequence of modifications.

### 5.4 The local extension clarification is responsible

The manuscript correctly uses only the truncation of the cotangent complex needed for `Ext^1`, writes the split multiplication after inverting `C`, and does not identify the local obstruction sheaf with the entire global hyper-Ext group.

The computation remains attached to the first nonreduced contact. No structural consequence for the global Hilbert graph or for deformation theory of all contacts is derived.

### 5.5 The toric class-group computation is credible

The saturated exponent lattice, primitive rays, cyclic quotient types, singular loci, and class group `Z/(m/gcd(m,2))` are mutually consistent. The gluing lemma for integral closures is standard and sufficient.

These are exact local consequences of the inherited ramified family, not a new all-order compactification theorem.

---

## 6. Why the top-four threshold is still not met

### 6.1 The all-order graph theorem is structurally classical

For any rational family of Hilbert points on an integral affine base, one may choose a Hilbert embedding, write homogeneous coordinate functions, and blow up their base ideal. Revision 167 instantiates this construction with a large evaluation matrix.

The theorem is useful. Its conceptual mechanism is not new at the level expected by a top general journal.

### 6.2 “Explicit” does not mean geometrically intelligible

The matrix size grows extremely rapidly. The manuscript gives no small determinantal complex, representation-theoretic reduction, minimal Fitting ideal, sparse generating set, or intrinsic formula for `a_a`.

The maximal-minor ideal is an exact answer in the same way that listing all Pluecker coordinates of a rational map is an exact answer. It does not yet expose the geometry of the boundary.

### 6.3 The chamber theorem is formal from finite polynomial data

Subdivide by monomial-weight comparisons and record residue cancellation. This proves finiteness for exact monomial profiles but does not create a new geometric classification principle.

A top-four theorem would need to identify a canonical small fan, relate its cones to contact invariants, and derive the geometry of the corresponding fibres.

### 6.4 Pointwise finite determination is not uniform or intrinsic

The bound `mu+1` depends on the valuation of the complete maximal-minor system. It is not bounded by contact order, Smith exponents, or any concise invariant provided in the theorem. The no-uniform result shows that this dependence is unavoidable in the current coefficient coordinates.

Thus the manuscript has a posterior finite-jet certificate, not a uniform finite-determinacy theory.

### 6.5 Complete higher-contact fibres remain unknown

For smaller Smith exponent at least three, the paper still does not determine:

- irreducible components;
- component dimensions;
- normalization;
- nilpotent or embedded structure;
- adjacency;
- intersection complex;
- which graph points lie on distinct normalization branches.

The determinantal graph and chamber vector encode these questions without solving them.

### 6.6 The strongest geometry remains one bespoke slice

The two-wall surface is excellent specialist mathematics. It is a two-dimensional slice at `a=2`. There is no analogous minimal fan or complete table for general `a`, even for a natural two- or three-parameter family at `a=3`.

### 6.7 Higher corank and singular-pencil Hilbert boundaries remain outside the theory

Paper I reconstructs all pencils, and inherited sections recover singular-pencil invariants. Paper II still does not turn those invariants into actual embedded Hilbert fibres or a compactification across higher-corank strata.

### 6.8 Interacting contacts are not classified

Products cover disjoint supports. Earlier sections treat the first collision. Revision 167 does not produce a general theory for several supports colliding with unequal lengths, nor a compatibility theorem when collisions pass through higher corank.

### 6.9 No single canonical global model is obtained

Strict base change and common refinements are useful. The stratumwise constructions with different generic Hilbert polynomials still do not glue into one canonical moduli space. There is no universal boundary divisor, incidence complex, logarithmic structure, or modular interpretation encompassing all strata.

### 6.10 The failure-algebra interpretation still follows reconstruction

The finite algebra is important because it reconstructs the entire pencil. Once that is done, every functorial invariant of the pencil can be transported back. Revision 167 does not find a Hilbert-state or boundary operation internal to the closed algebra before this reconstruction.

### 6.11 There is no major external application

The new results do not settle a recognized open problem about Hilbert schemes, compactifications of rational maps, complete quadrics, symmetric matrix pencils, tropical Hilbert schemes, or moduli of finite algebras. Their applications remain internal to the manuscript's own pipeline.

### 6.12 The novelty comparison is not yet adequate

The literature record responsibly avoids unsupported priority claims. It nevertheless does not perform a theorem-level comparison with several adjacent frameworks that bear directly on the new main theorem:

- Gröbner fans and comprehensive Gröbner bases for parameterized ideals;
- tropical Grassmannians and valuated matroids of evaluation matrices;
- Rees valuations and normalized blow-ups of determinantal/Fitting ideals;
- Hilbert and Chow main components of rational-map spaces;
- logarithmic and expanded compactifications;
- relative Quot constructions and flattening stratifications.

Until this comparison is done, the originality of the “decorated Hilbert-state” organization is not securely positioned.

### 6.13 Paper I remains without independent proof audit

The sharp inverse is indispensable to every intrinsic failure-family interpretation. The audit handoff, dependency graph, compilation, and finite checks are not an independent verification of its 75-page proof.

### 6.14 Historical positioning remains incomplete

The theorem/proof-level comparison with Ballico 1993 remains unavailable. The manuscript correctly narrows its claims, but broad historical originality cannot be certified from bibliography alone.

### 6.15 The publication architecture is still cumulative

Paper II is now 113 pages and still contains universal power ideals, complete quadrics, singular pencils, divisor conductors, reciprocal fibres, reduced incidence, higher-contact slices, complete first-contact fibres, collision families, horizontal main components, extension algebras, ramification, and the new determinantal state theory.

Moving inherited material to appendices improves the reading route but does not turn this accumulation into the forced proof of one top-four-scale theorem.

---

## 7. Specific technical and expository requests

These points should be addressed even for a strong specialist submission.

### Determinantal graph theorem

1. **State a general graph-from-Pluecker lemma separately.** Make clear which part is universal Hilbert machinery and which part is special to `M_a`.

2. **Give a self-contained proof of the Gotzmann representation.** The current calculation is short enough to isolate.

3. **State projective normality of the Segre embedding explicitly.** This is the reason the smaller section space suffices.

4. **Record all matrix dimensions in the theorem statement.** Readers should not reconstruct `q` and `N` from several definitions.

5. **Distinguish the quotient matrix from its transpose.** “Row lattice,” “quotient,” and maximal minors should use one fixed convention throughout.

6. **Prove the rank/base-point-free equivalence in a named lemma.** It is load-bearing in three later results.

7. **Explain the fixed kernel of the Segre ideal in the Hilbert Grassmannian.** This will prevent confusion about the ambient projective space.

8. **State precisely why the degree-`m` kernel generates the ideal sheaf.** Cite the truncation consequence of `m`-regularity, not only generation in degrees at most `m`.

9. **Separate the graph from its normalization in every theorem.** A primitive Pluecker vector identifies a graph point, not necessarily a normalization branch.

10. **Give an intrinsic description of `a_a` if possible.** At minimum, ask whether it is a Fitting ideal of a naturally defined sheaf.

11. **Investigate radical, integral closure, and Rees valuations of `a_a`.** The normalized graph depends on these data.

12. **Give a smaller presentation or prove that none is expected.** All maximal minors are not a satisfactory structural answer at large `a`.

13. **Provide asymptotic size estimates.** The term “explicit” should be accompanied by the growth of rows, columns, and potential minors.

14. **Do not imply practical computability for arbitrary `a`.** The present construction is finite but combinatorially enormous.

### DVR specialization and finite determinacy

15. **Call `mu+1` a posterior bound.** It is computed from the same determinantal data that determine the limit.

16. **Relate `mu` to intrinsic contact invariants where possible.** The two-wall formula is one example; a general theorem would be valuable.

17. **Distinguish coefficient-jet determination from family determination.** The result fixes the closed Hilbert point, not the entire DVR family or normalization lift.

18. **State the behavior under ramified base change.** `mu` scales, while the embedded closed limit may not change.

19. **Clarify residue-field descent.** Projective equality over `k` and geometric equality after extending `k` should be separated.

20. **Give a finite algorithm for polynomial arcs using Smith form.** Specify the coefficient ring and termination assumptions.

21. **Do not call the no-uniform theorem a failure of finite determinacy.** It is a failure of a uniform bound; every individual arc still has one.

### Decorated chambers

22. **State explicitly that positive weights centre the arcs at the chosen origin.** Do not imply a chamber decomposition around every point of `B_a`.

23. **Extend the theorem to valuation-zero coordinates or explain the local translation needed.** Boundary points with nonzero residue coefficients are otherwise omitted.

24. **Separate zero coordinates from positive-weight coordinates in the notation.** Identically zero and arbitrarily high order are different conditions.

25. **Formulate the universal finite-polynomial lemma first.** Then identify the additional Hilbert content supplied by `M_a`.

26. **Compare the fan with the Gröbner fan and tropicalization of the Pluecker ideal.** Determine whether the hyperplane arrangement is a strict refinement.

27. **Compare the primitive vectors with valuated-matroid initial data.** The maximal-minor setting makes this unavoidable.

28. **Give a minimal example with residue cancellation changing the chamber output.** The current proof is formal; one geometric example would show necessity.

29. **Describe how to recover a curve ideal from a chamber vector without a full Hilbert-scheme elimination.** Otherwise the classification remains coordinate-level.

30. **Provide complexity bounds or explicitly disclaim efficiency in the abstract.** The present disclaimer in the body is insufficient.

31. **Do not call the arrangement canonical without qualification.** It depends on the chosen coefficient coordinates and the chosen maximal-minor presentation.

32. **Track behavior under a change of contact chart.** The fixed-target undo maps preserve Hilbert points, but they need not preserve the stated fan.

33. **State whether different residue strata can yield the same projective vector.** If so, merge them or explain why the nonminimal partition is retained.

34. **Distinguish finite families from finite combinatorial types.** The residue strata may contain continuously varying nonisomorphic curves.

### Two-wall slice

35. **Promote the row-ideal factorization to a standalone proposition.** It is the most transparent part of the determinant calculation.

36. **Prove the blow-up-of-powered-products lemma separately.** State the domain and nonzero-ideal hypotheses.

37. **Give the irrelevant saturations of all five ideals explicitly.** The table currently delegates this to convention.

38. **Write the primary decompositions in affine charts.** Then translate them to sheaf statements.

39. **Check all infinity charts in one proposition.** This is necessary for the complete fixed-target claim.

40. **Explain which exceptional component corresponds to which valuation ray.** Include the primitive fan rays and their order.

41. **State the modular meaning of the wall residues.** Explain why `k` and `h` are the only residual moduli on their walls.

42. **Compare this surface with the normalized blow-up of the restricted ideal.** Smoothness should be related to the fan regularity.

43. **Determine the intersection matrix and nef cone of the exceptional chain.** This would turn the calculation into a more complete birational model.

44. **Avoid extrapolating from this slice to all order-two arcs.** It fixes `f=x^2`, a constant `g`, and a linear `r`.

45. **Compute one genuinely three-parameter slice or an `a=3` slice.** This is the next test of whether the method yields structure rather than isolated examples.

### Horizontal comparison and local algebra

46. **Keep “strict base change” distinct from ordinary base change.** The full pullback can contain vertical components.

47. **State the dense-open hypotheses in every comparison corollary.** The comparison does not cross into a different generic Hilbert polynomial.

48. **Do not present common refinements as a canonical minimal model.** They form a directed construction, not a terminal compactification.

49. **Ask whether the refinement category has a canonical normalization or inverse limit of finite type.** At present it does not.

50. **Give a geometric consequence of the square-zero extension class.** The calculation is otherwise isolated from the main theorem.

51. **Clarify which line bundle is trivialized by the obstruction generator.** It is not the nilradical line bundle.

52. **State the toric quotient types in a uniform convention.** Explain the pseudoreflection removal in the even case before naming the quotient.

53. **Relate the class group to the boundary divisors used elsewhere.** The local computation should connect to global divisor language.

54. **Keep parameter-space normalization separate from stable reduction of curves.** The manuscript currently does this correctly and must continue to do so.

### Scope and editorial structure

55. **Make the determinantal theorem the actual centre of Paper II.** Move substantially more inherited material to a separate paper or repository supplement.

56. **Do not treat the preservation master as evidence for a journal package.** Preservation and publication architecture are different concerns.

57. **Add a theorem-level comparison with Gröbner/tropical/valuated-matroid methods.** This is essential for the new main claim.

58. **Expand the comparison with Hilbert main components of rational-map spaces and relative Quot schemes.** Target distinctions alone do not establish novelty.

59. **State plainly that complete higher-contact fibre geometry remains open.** This limitation should appear in the abstract, not only the introduction.

60. **Separate the all-order graph theorem from an all-order fibre-classification claim.** They answer different questions.

61. **Obtain an independent full audit of Paper I.** The effective-boundary corollary depends on it.

62. **Complete the legitimate Ballico comparison or permanently narrow the historical framing.**

63. **Keep finite checks separate from proof evidence.** The current receipts do this responsibly.

64. **Avoid counting responses as mathematical closure.** Sixty-two answered requests do not replace a new global theorem.

65. **State one publication-level theorem rather than a research-program inventory.** The current 113-page paper still carries too many independent threads.

66. **Provide a realistic specialist-journal version.** The determinantal graph, finite specialization, and two-wall slice could form a coherent paper if the cumulative appendices were removed.

---

## 8. Response-to-v166 scorecard

### Fully or substantially closed

- consistent use of “horizontal Hilbert-main-component modification” rather than unqualified flattening;
- precise admissible test category and schematic-density lemma;
- strict-base-change theorem and a genuine nonflat counterexample;
- normalization comparison and common refinements on a fixed generic open;
- explicit maximal-minor ideal for every polynomial contact order;
- graph/Rees identification in one projective degree;
- pointwise finite coefficient-jet determination;
- an explicit no-uniform-bound theorem;
- finite decorated classification for exact monomial coefficient profiles, including residue cancellation;
- a complete nonsymmetric two-wall slice;
- exact minimal primes, multiplicities, and Cohen--Macaulayness for the five slice limits;
- explicit overlap maps and fixed-target equations on the slice;
- clarification of the square-zero presentation complex and local multiplication;
- primitive toric rays, singular loci, class groups, and normalization gluing;
- a theorem-dependency graph and a clearer primary reading route;
- honest separation of the effective failure-family application from raw Artin-algebra deformations.

### Partially closed

- finite chamber classification: achieved for exact monomial coefficient arcs, not arbitrary formal arcs or arbitrary boundary centres;
- global compatibility: achieved for base changes and refinements on one generic open, not across different generic Hilbert polynomials;
- explicit higher-contact geometry: one all-order determinantal graph is known, but its fibres are not classified;
- literature positioning: classical Hilbert/state-polytope inputs are acknowledged, but adjacent tropical and comprehensive-Gröbner frameworks are not compared theorem by theorem;
- architecture: a main theorem is now visible, but Paper II remains cumulative and very long;
- nilpotent extension consequences: the class is clarified, but it does not yet control a global modification or deformation theorem;
- intrinsic failure-algebra boundary: functorial after reconstruction, not internal before it.

### Still open

- complete component, normalization, nilpotent, and adjacency classification for contact length at least three;
- a canonical small fan or boundary complex for general `a`;
- higher-corank and singular-pencil Hilbert boundaries;
- interacting collisions of unequal and higher contact lengths;
- a canonical global compactification across generic-polynomial strata;
- a coordinate-invariant chamber theory around arbitrary boundary points;
- a major external application of independent recognized importance;
- an internal boundary operation on the closed finite algebra before reconstruction;
- an independent full proof audit of Paper I;
- theorem/proof-level comparison with Ballico 1993;
- a top-four-scale conceptual principle beyond classical Hilbert embeddings, Rees graphs, and finite polynomial valuation bookkeeping.

---

## 9. Conditions for another top-four evaluation

I would not recommend another top-four round triggered by a larger matrix computation, another exact slice at contact order two, more finite checks, or another response document.

A serious new evaluation should contain at least one result of a different order of magnitude, for example:

1. **A complete higher-contact fibre theorem** for arbitrary `a`, determining components, normalization, nilpotents, and adjacency from intrinsic contact data.

2. **A canonical small fan or logarithmic compactification** whose cones have a direct modular interpretation and whose local charts recover the determinantal graph.

3. **A higher-corank or singular-pencil Hilbert-boundary theorem** linking Kronecker or Smith data to actual embedded fibres.

4. **A general interacting-collision theorem** covering unequal lengths and passage through higher corank, with canonical transition maps.

5. **A structural formula for the maximal-minor ideal**—for example a representation-theoretic, Fitting, or resultant description—replacing the enormous universal list of minors.

6. **A coordinate-invariant finite-determinacy theorem** expressed in concise contact invariants rather than the posterior valuation of the full Pluecker system.

7. **An internal operation on the finite failure algebra** that detects boundary structure without first reconstructing the complete pencil.

8. **A major external application** solving a recognized problem outside this manuscript's own pipeline.

9. **An independent proof audit of the sharp inverse**, together with completed legitimate historical positioning.

Any one of these could change the editorial discussion. Further accumulation of exact local computations, however competent, would not by itself do so.

---

## 10. Final assessment

Revision 167 deserves substantial credit. It is complete, reproducible, mathematically stronger than v166, and unusually responsive to detailed criticism. The retained-coefficient graph now has one explicit global Rees model at every polynomial contact order. DVR specialization is reduced to a primitive exterior vector. Exact monomial profiles receive a finite cancellation-aware organization. The nonsymmetric two-wall slice is a clean and convincing piece of birational and Hilbert-scheme geometry. The strict-base-change theorem and local algebra clarifications remove several genuine ambiguities from earlier versions.

I therefore reject any characterization of v167 as cosmetic, merely computational, or mathematically empty.

I nevertheless recommend rejection for *Annals*, *Acta*, *Inventiones*, or *JAMS*. The general determinantal theorem is an explicit instance of classical Hilbert--Pluecker and Rees-graph machinery. The decorated chamber theorem is a finite polynomial-valuation construction whose output does not yet reveal the geometry of general higher-contact fibres. The complete geometric calculation remains one specially chosen order-two slice. Higher contact, higher corank, singular pencils, interacting collisions, and a canonical global compactification remain unresolved. The failure-algebra interpretation still passes through full reconstruction. Paper I remains without the independent proof audit repeatedly requested, and the closest historical comparison remains incomplete.

The appropriate assessment is therefore:

**Reject the v167 package in its present form for a top-four general mathematics journal.**

**Paper II is a strong candidate for a specialist journal in algebraic geometry, Hilbert schemes, compactification theory, tropical/Gröbner geometry, or invariant theory after substantial narrowing around the determinantal graph and two-wall theorem. Paper I likewise deserves specialist consideration after an independent proof audit and sharper historical positioning.**
