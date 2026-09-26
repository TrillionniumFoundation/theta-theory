# Independent harsh referee report — A2 revision 166

## Manuscript and review object

**Submission package:**

1. *Finite failure schemes and the reconstruction of quadratic pencils* (Paper I, 74 pages);
2. *Power ideals and the Hilbert boundary of quadratic pencils* (Paper II, 102 pages);
3. the 168-page preservation master containing the complete mathematical bodies of both papers.

**Author:** Qian Qi  
**Revision reviewed:** A2 revision 166  
**Revision branch:** `revision/a2-v166-universal-flattening-2026-09-26`  
**Locked branch tip:** `1664ebe4be5851a3566cb3c25b5cde4992f9acfb`  
**Authored mathematical/build-source commit:** `60304100b64960e8e3e3a704b23c38fb38b37a67`  
**Complete manuscript materialization commit:** `a616fe75e0a6aec0579a7583a450220b6c40579d`  
**Controlling prior report:** `reviews/a2-v164-independent-harsh-top4-2026-09-26/REFEREE_REPORT.md`  
**Controlling prior-report commit:** `e795bc76e458260f0efcc8182c292f19d0610ca0`  
**Principal new sources:**

- `papers/A2-v17-boundary-information-coarsening/article/v166/horizontal-flattening-v166.tex`;
- `papers/A2-v17-boundary-information-coarsening/article/v166/miniversal-specialization-v166.tex`;
- `papers/A2-v17-boundary-information-coarsening/article/v166/extension-and-ramification-v166.tex`;
- `papers/A2-v17-boundary-information-coarsening/article/v166/comparison-details-v166.tex`;
- `papers/A2-v17-boundary-information-coarsening/article/v166/effective-horizontal-v166.tex`.

**Complete focused sources:** `reconstruction.tex` and `divisor-geometry.tex`.

**Review standard:** the proof-completeness, originality, conceptual depth, inevitability, breadth, and expository standard expected at *Annals of Mathematics*, *Acta Mathematica*, *Inventiones Mathematicae*, or *Journal of the AMS*.

This is an owner-requested independent-referee-style report, not a journal-commissioned editorial decision. I reviewed the complete materialized v166 package, not a branch-name alias, a source-lock shell, or a staging payload. I read the new horizontal-modification theorem, its discrete-valuation-ring formulation, the seven-chart all-arc theorem, the conic-realization result, the square-zero extension calculation, the arbitrary-ramification normalization, the fixed-target comparison appendix, the effective-family descent, the response to the v164 report, the literature record, and the audit handoff for Paper I. I also re-read the inherited complete first-contact fibre, collision family, product-fibre theorem, universal power-ideal identity, and sharp inverse to determine what the new claims actually add.

The build receipt records complete standalone sources and PDFs, successful compilation, preservation of every predecessor mathematical block, and a rerun of the inherited exact checks. I use those records to identify the review object and to assess reproducibility. They are not proof certificates, priority certificates, or evidence for the editorial threshold.

## Recommendation

**Reject the v166 package in its present form for a top-four general mathematics journal.**

Revision 166 is a genuine and substantial mathematical advance over v164. It is not merely a response letter, a change of terminology, a larger test suite, or a repackaging of the first collision example. The revision now:

- formulates a terminal horizontal-flat embedded-quotient problem and represents it by the closure of the generic section in a relative Hilbert scheme;
- supplies a finite stratumwise organization through which every discrete-valuation-ring specialization of the projective graph factors;
- treats an arbitrary six-coefficient arc through the first nonreduced corank-two contact, rather than only the symmetric path `(x^2-delta,0,0)`;
- gives five conic-coordinate presentations and two primitive division presentations covering the entire pullback over every such arc;
- identifies the horizontal family by exact saturation and the entire vertical torsion by the quotient of saturated and unsaturated ideals;
- determines the square-zero algebra extension, not merely its nilradical module;
- proves local nonsplitting precisely on the doubled-line curve and identifies the local obstruction sheaf;
- proves that every conic tail is attained by a generically nonincident coefficient arc, while the double-incidence subbase reaches exactly the singular-at-the-attachment conics;
- computes arbitrary ramification of the symmetric collision, including the cyclic-invariant normalization, divisor multiplicities, and the complete torsion filtration;
- descends the horizontal universal property to the effectively rigidified failure-family image after applying the sharp inverse.

These are real theorems. I did **not** find a simple counterexample to the universal horizontal property on its stated category, the discrete-valuation-ring saturation theorem, the seven-chart covering argument, the conic-realization theorem, the local extension-class computation, the cyclic-invariant normalization, or the effective descent. My recommendation is therefore not a concealed correctness rejection.

The top-four problem is one of conceptual scale and mathematical necessity.

The highest-level “universal horizontal modification” is, in essence, the main-component construction obtained by taking the closure of the generic fibre section in a classical relative Hilbert scheme. Its universal property is useful and correctly proved, but much of it follows formally from Hilbert representability, schematic density, and flatness of the universal quotient. It does not by itself discover the boundary components, their singularities, their incidence complex, or their modular meaning.

The subsequent “stratumwise” theorem is not one canonical compactification of the entire coefficient space. It is a finite Noetherian-induction stratification, explicitly nonunique, together with a separate Hilbert-main-component modification over the reduced closure of each chosen stratum. The paper proves no compatibility morphisms among those modifications, no gluing into a single logarithmic or modular object, no canonical poset of walls, and no comparison of the resulting models when the stratification is refined.

The all-arc theorem is considerably stronger than the old symmetric collision, but it remains a presentation-and-saturation theorem. For an arbitrary arc, the answer is “substitute its six coefficients into one of seven charts and saturate by the uniformizer.” This is exact. It is not yet a classification of the possible saturated ideals, special fibres, irreducible components, multiplicities, singularities, adjacency relations, or valuation chambers. For arbitrary formal arcs the manuscript explicitly disclaims a finite-jet algorithm. Thus “every arc is covered” should not be confused with “every degeneration type is classified.”

The complete geometric classification still stops at smaller Smith exponent at most two. At contact length at least three the manuscript retains a primitive open, resultant strata, and conjectures. Higher corank, singular pencils in the Hilbert problem, interacting contacts of different lengths, and global wall relations remain outside the explicit theory.

The square-zero extension and ramification calculations are attractive and exact, but they are local commutative-algebra and toric-normalization results attached to the first nonreduced contact. They do not yet produce a new general theorem about Hilbert boundaries or compactifications whose consequences extend substantially beyond this example.

Paper II is now a serious and potentially strong specialist paper. Paper I contains a striking inverse theorem and deserves independent specialist scrutiny. The two-paper package nevertheless remains below the threshold of the four general journals named above.

---

## 1. What revision 166 genuinely adds

### 1.1 A precise horizontal-flat functor

The manuscript correctly distinguishes three objects:

1. the full pullback of a projective graph family;
2. the schematic closure of its generic flat part after a chosen base change;
3. the special fibre of either of those objects.

For a projective finite-presentation morphism `W -> B`, an integral finite-type base, and a dense open `U` on which the family is flat with polynomial `P`, it defines

`W_T^h = closure of W_(U_T) in W_T`

for tests on which `U_T` is schematically dense. This is the right functor for the phenomenon isolated in v164: vertical components may remain in the full pullback even when the horizontal closure is flat.

### 1.2 The relative-Hilbert main component has the claimed terminal property

The construction

`F_(W,U) = closure of s(U) in Hilb^P(W/B)`

is mathematically natural. The universal quotient restricts to a flat horizontal family. If a test has flat horizontal closure, Hilbert representability gives a map to the relative Hilbert scheme, and schematic density forces factorization through the closure of the generic section. Conversely, a map to that closure pulls back a flat quotient whose generic open is schematically dense, hence the quotient is the required horizontal closure.

This is a clean result. It is also close to formal once the relative Hilbert scheme and the precise admissible category have been chosen.

### 1.3 The discrete-valuation-ring horizontal quotient is exact

For a Noetherian algebra over a discrete valuation ring, quotienting by all uniformizer-power torsion is indeed the unique flat quotient with the same generic fibre. The saturation formula

`D/(I:tau^infinity)`

and the identification of the torsion ideal are correct. The two-term resolution of the residue field gives the stated `Tor_1` and the vanishing of higher Tor. The filtration by annihilators is also correctly described.

This is elementary but load-bearing: it turns horizontal specialization into an exact scheme calculation rather than a reduced-support operation.

### 1.4 Every arc through the double contact is placed in explicit charts

The new six-coefficient form

`f=(x-c)^2+d`, `g=u(x-c)+v`, `r=w(x-c)+z_0`

removes the symmetry and zero-jet assumptions of v164. The five Hilbert–Burch coordinate systems cover every conic through the attaching point, and the two division systems cover the primitive line-tail locus. The displayed ideals retain all five independent coefficient equations; in particular the constant coefficient of `r` is not silently discarded.

The proof that these seven recovery opens cover the full pullback is sound in outline:

- they cover the complete special fibre;
- their union is open;
- the complement is closed in a proper scheme over a local discrete valuation ring;
- a nonempty proper closed subset would meet the closed fibre;
- therefore the complement is empty.

This upgrades a neighbourhood calculation to an exhaustion theorem over each arc.

### 1.5 The vertical conic component acquires a genuine coefficient-direction meaning

The theorem that every conic through the attaching point occurs along some generically nonincident arc is useful. The sharper comparison—that the subbase `g=r=0` reaches exactly the singular-at-the-attachment plane—explains why the remaining conics are vertical for the symmetric collision but not spurious in the full coefficient space.

This is a more satisfactory modular explanation than merely recording an excess `P^4` component.

### 1.6 The nilpotent algebra extension is computed

The inherited fibre ring

`C[lambda,e,A,B,C]/(eA,eB,e^2 C)`

has nilradical generated by `eC`. Revision 166 goes beyond the module identification. On the reduced ring cut out by `(eA,eB,eC)`, the conormal map sends the first two generators to zero and `eC` to the nilpotent generator. Modulo derivations, the local degree-one group is `N/CN`, and the actual class is its generator.

The conclusion is precise:

- the extension splits locally off the doubled-line curve;
- it is locally nonsplit at every point of that curve;
- the local obstruction sheaf is the structure sheaf of the curve;
- the global extension class maps to the nowhere-vanishing section `1`.

This closes a real scheme-theoretic gap in v164.

### 1.7 Arbitrary ramification is treated exactly

For `delta=tau^m`, the horizontal chart

`e^2 C + tau^m = 0`

has normalization described by a cyclic invariant ring with weights `(1,-2)`. The exponent-lattice argument identifies the correct fraction field and proves finiteness and normality. The parity-dependent divisor multiplicities are credible, and for even `m=2q` the equation `eh=tau^q` transparently records the residual surface singularity.

The vertical torsion is not collapsed to its first Tor layer: it is retained as the full length-`m` filtration. This is an important correction to any treatment that would identify torsion solely from `Tor_1`.

### 1.8 The effective failure-family application is responsibly scoped

The paper explicitly uses the sharp inverse first, recovers the source and pencil, constructs the horizontal model geometrically, and only then descends it to the effective failure-family image. It does not claim a boundary operation internal to an arbitrary raw Artin algebra, and it does not claim that a closed multiplication table selects a specialization direction.

This is the correct categorical limitation.

---

## 2. Correctness audit of the universal horizontal theorem

I found no direct contradiction, but the theorem should be presented with more restraint than its title currently suggests.

### 2.1 Integrality of the Hilbert closure

The schematic closure of the integral section `s(U)` in the separated relative Hilbert scheme is integral. The construction is projective over the base, and because the section is closed over `U`, the modification is an isomorphism there.

This part is standard and correct.

### 2.2 The forward universal implication is credible

If the horizontal closure over a test is flat, it has polynomial `P` on every connected component because the schematically dense open meets every nonempty open-and-closed component. Hilbert representability therefore supplies a classifying morphism. Pulling back the ideal of the main Hilbert component gives an ideal vanishing on a schematically dense open, so the map factors through the closure.

The manuscript should keep the finite-presentation and projectivity hypotheses visible at this step; they are not cosmetic.

### 2.3 The converse uses flat schematic density correctly

A flat quotient pulled back from the main Hilbert component has the generic family as a schematically dense open. Since it is a closed subscheme of the full pullback, it is the schematic closure of that open. This proves existence and uniqueness of the horizontal quotient.

The argument is credible, although a short affine lemma stating exactly when flat pullback preserves schematic density would improve readability.

### 2.4 Independence of polarization is representational, not geometric classification

The universal property identifies the constructions arising from two relatively ample line bundles. This is enough for canonical isomorphism of the representing modifications.

It does not give an intrinsic explicit ideal on `B`, a sequence of canonical blow-ups, or a boundary divisor formula. The paper should not let “independent of polarization” suggest more explicit canonicity than has been proved.

### 2.5 Shrinking the generic open is harmless

On an integral base, any nonempty smaller open is dense. Its section is schematically dense in the old section, so the closures agree. This is correct.

### 2.6 The construction is not the usual universal flattening

The manuscript correctly states that it does not flatten the full pullback. The terminology “universal horizontal modification” is defensible only if “horizontal” is always retained. The shorthand “universal flattening” in filenames, branch names, or summaries risks conflating this main-component construction with the classical flattening functor for the full sheaf.

### 2.7 The theorem is a specialized Hilbert-main-component construction

The central existence statement does not introduce a new representability mechanism. Once one asks for flat embedded quotients with fixed Hilbert polynomial and prescribed generic fibre, taking the closure of the corresponding section in the relative Hilbert scheme is the evident construction.

This does not diminish correctness. It substantially limits originality at the top-four level.

---

## 3. Audit of the stratumwise theorem

### 3.1 Finite coverage by Noetherian induction is correct

Taking disjoint dense generic-flat opens in the irreducible components and repeating on the closed complement terminates by dimension. Every discrete-valuation-ring arc has its generic point in one stratum and factors through the reduced closure of that stratum.

The argument is sound.

### 3.2 The stratification is explicitly nonunique

This is a serious conceptual limitation, not a minor presentational issue. Different choices of dense opens and different orders of refinement may produce different collections of closures and different relative Hilbert components.

The theorem proves existence of a finite atlas of horizontal models, not a canonical global boundary object.

### 3.3 Compatibility between strata is absent

Suppose one stratum specializes into the closure of another. The manuscript does not construct:

- a transition morphism between their horizontal modifications;
- a common refinement with a universal comparison map;
- a cocycle or descent theorem for the modifications;
- a logarithmic structure recording their incidence;
- a canonical boundary complex.

Without such compatibility, “global modular organization” should be read as bookkeeping by strata, not as a compactification theorem.

### 3.4 Different generic Hilbert polynomials are a real obstruction

The paper correctly notes that one cannot silently use a single Hilbert polynomial across strata. This is exactly why the theorem stops short of one full-base modification. A top-four result would need to turn this obstruction into structure rather than merely route around it by separate constructions.

### 3.5 The valuative lifting property is stratum-relative

An arc lifts uniquely after one chooses the closure determined by the stratum of its generic point. There is no assertion that all arcs with the same closed point lift to one common proper model over the original base.

The word “universal” must remain qualified accordingly.

---

## 4. Correctness audit of the seven-chart all-arc theorem

### 4.1 The coefficient normal form is complete

Writing a monic quadratic around its center and expressing the other two polynomials in the same local coordinate gives six independent coefficients. No hidden symmetry remains.

### 4.2 Five conic coordinates really cover the conic component

The five evaluation functionals recover the five coefficients of a conic through the attaching point. Their evaluation matrix is invertible. Hence every nonzero conic lies in at least one normalized recovery chart.

This is a finite coordinate cover, not a quotient by target automorphisms: the coordinate changes are undone before returning to the fixed target.

### 4.3 The two division systems cover primitive tails

A line direction over the length-two contact algebra has at least one unit homogeneous coordinate. The two standard affine charts cover it. This includes the jet boundary and its overlap with doubled lines.

### 4.4 The Hilbert–Burch equations retain the full base map

The five equations in each conic chart correctly arise by matching the coefficients in the retained base map. The constant equation involving `z_0` is essential for general arcs. This is stronger and more careful than the v164 specialization.

### 4.5 Scheme exhaustion by properness is credible

Coverage of the entire special fibre plus properness over a local discrete valuation ring does force coverage of the entire pullback. This is one of the strongest logical improvements in v166: the theorem is not merely a list of local models around selected limits.

### 4.6 Saturation gives the exact horizontal scheme

On every chart, quotienting by uniformizer-power torsion is the unique flat quotient with the same generic fibre. Flat compatibility on overlaps lets the local quotients glue. No radical or normalization of the fibre is inserted.

This is correct and important.

### 4.7 “All arcs” does not mean “all degeneration types classified”

The theorem gives a finite list of ambient presentations. It does not simplify the arbitrary saturation

`K_bullet : tau^infinity`

into a finite catalogue. The geometry may still depend on arbitrarily complicated cancellation among the six coefficient series.

For formal arcs, the manuscript itself states that no fixed finite jet is sufficient in general. Thus the result is exact but not a finite determinacy theorem.

### 4.8 No uniform bound for the saturation exponent is obtained

For each Noetherian chart the colon chain stabilizes. There is no bound in terms of contact order, matrix size, or the six coefficient valuations that works across all arcs. Such a bound, or a proof that no such bound can exist, would be a substantial structural result.

### 4.9 The theorem does not describe general special-fibre geometry

From the presentation one does not yet read a theorem classifying:

- all minimal and embedded primes;
- component dimensions;
- multiplicities;
- reducedness or Cohen–Macaulayness;
- normalization;
- adjacency to primitive and conic components;
- dependence on valuation data.

These remain calculations to be performed arc by arc.

---

## 5. Audit of the square-zero extension

### 5.1 The local ring and nilradical are correctly used

The reduced ideal is `(eA,eB,eC)`, and the quotient between it and `(eA,eB,e^2C)` is generated by the class of `eC`, annihilated by `(e,A,B)`.

### 5.2 The conormal presentation computes the relevant degree-one class

Because the square-zero extension is classified by the degree-one cotangent-complex group, the naive two-term presentation suffices for this calculation. The paper does not incorrectly identify this with ordinary `Ext^1` of Kähler differentials.

### 5.3 The local Hom calculation is credible

The Koszul relations force the images of `eA` and `eB` to vanish. The image of `eC` is arbitrary in the nilpotent module. Derivations contribute precisely the multiples by `C`, giving the quotient `N/CN`.

### 5.4 The actual extension is the generator

The defining algebra sends `eC` to the nilpotent generator, so its class is nonzero exactly where `C=0` on the singular-conic plane. This identifies the doubled-line curve as the nonsplitting locus.

### 5.5 The global obstruction sheaf claim is plausible

The local generators arise from one global algebra extension and are nonzero on every chart along the doubled-line curve. They therefore trivialize the local obstruction line. The statement concerns the image of the global extension in the local sheaf; it does not claim that the entire global hyper-Ext group is one-dimensional.

This scoping is correct.

### 5.6 The result is significant locally but not yet broadly exploited

The manuscript does not use the nonsplit class to derive a deformation obstruction, a derived enhancement, a canonical modification, or a numerical invariant with consequences elsewhere. At present it completes the scheme description of one fibre.

---

## 6. Audit of arbitrary ramification

### 6.1 The horizontal base change is exact

The map `delta -> tau^m` is finite free, so the flat horizontal model base-changes as claimed. The full pullback retains a vertical thickening of exact length `m`.

### 6.2 The cyclic invariant normalization is credible

The exponent lattice generated by `(m,0)`, `(0,m)`, and `(2,1)` is the character lattice for the stated cyclic action. Its saturation in the first quadrant gives the invariant semigroup. The invariant ring is finite, normal, and has the same fraction field as the original hypersurface ring.

### 6.3 The divisor multiplicities are consistent

At the `s=0` divisor, the generic stabilizer has order `gcd(m,2)`, so the order of `tau=s^2r` downstairs is `2/gcd(m,2)`. At `r=0` the generic stabilizer is trivial, giving multiplicity one.

### 6.4 The even case transparently records residual singularities

For `m=2q`, the equation `eh=tau^q` shows that the central divisor may be reduced while the total space is singular. This is a useful warning against confusing reduced central support with semistability.

### 6.5 The torsion filtration is stronger than a first-Tor statement

The full vertical torsion is the ideal of the singular-conic plane tensored with `C[tau]/(tau^m)`. Its first Tor is only the last nonzero layer. This is correctly distinguished.

### 6.6 The calculation is still one toric family

The result concerns ramification of the symmetric collision model. It is not a ramification theorem for arbitrary six-coefficient arcs, and it does not classify normalized horizontal spaces for general valuation patterns.

---

## 7. Why the top-four threshold is not met

### 7.1 The general existence theorem is too formal

The relative-Hilbert closure is useful infrastructure. It is not, by itself, a new conceptual theorem on the scale expected at a top general journal. The hard geometry has merely been moved into determining the corresponding Hilbert main component.

### 7.2 The “global” result is only stratumwise

There is no single canonical compactification of the full coefficient space. The finite stratification is noncanonical, and the separate models have no proved compatibility. The paper therefore does not yet construct the promised global boundary theory.

### 7.3 The all-arc theorem is a recipe, not a classification

Substitution plus saturation is exact, but the saturation is precisely where the difficult geometry sits. A theorem that lists the input equations without classifying their outputs does not resolve the higher-dimensional boundary problem.

### 7.4 Explicit complete fibres stop at contact length two

For smaller Smith exponent at least three, the paper has no complete component theorem, no exact nilpotent structure, and no adjacency classification. The universal existence construction does not close this gap.

### 7.5 Higher corank remains essentially outside the Hilbert theory

The all-pencil inverse and singular-pencil invariants survive, but they are not converted into a classification of higher-corank Hilbert fibres. The most difficult boundary is therefore still absent.

### 7.6 Interacting multiple contacts are not globally classified

Products handle disjoint supports. The six-parameter `B_2` model handles the first collision. There is no general theory of several contacts colliding simultaneously, unequal contact lengths, or collisions through higher corank.

### 7.7 Much of the new machinery is standard once the local equations are known

The principal tools are:

- relative Hilbert schemes;
- schematic closure;
- uniformizer saturation;
- Hilbert–Burch resolutions;
- formal patching;
- square-zero extension classes;
- finite cyclic invariant rings;
- toric normalization.

The manuscript uses them carefully. A top-four paper needs a new principle whose consequences are not largely formal from these tools plus one explicitly computed local ring.

### 7.8 No major external application is obtained

The results do not settle a recognized open problem about compactifications of pencils, complete quadrics, Hilbert schemes, determinant representations, or moduli of finite algebras. The applications remain internal to the constructed failure-algebra pipeline.

### 7.9 The failure-algebra interpretation still follows full reconstruction

The closed finite algebra first recovers the classical pencil. The boundary construction is then performed on that recovered object. This proves invariance, but it does not reveal a new boundary operation internal to the multiplication table before reconstruction.

### 7.10 Paper I remains unaudited externally

The new `PAPER_I_AUDIT_HANDOFF.md` is useful and honest. It is not an independent proof audit. The sharp inverse is the indispensable input for every “intrinsic failure-family” interpretation, yet its most delicate 74-page proof has still not received the independent scrutiny requested by the preceding reports.

### 7.11 Historical originality remains incompletely certified

The theorem/proof-level comparison with Ballico 1993 remains unavailable. The manuscript correctly discloses this, but the broad historical claims about failure loci must remain narrow.

### 7.12 The architecture is still cumulative

The package now contains a sharp inverse, effective stack equivalence, universal power ideals, complete quadrics, singular-pencil invariants, divisor normalization, reciprocal fibres, reduced incidence, higher-contact slices, all-arc presentations, complete first-contact fibres, collisions, horizontal Hilbert modifications, nilpotent extensions, and ramification models.

The length reflects accumulation of a research programme more than the forced proof of one central theorem. That architecture is acceptable for a monograph or a sequence of specialist papers; it weakens the case for a single top-four package.

---

## 8. Specific technical and expository requests

These points should be addressed even for a strong specialist submission.

### Universal horizontal construction

1. **Rename the construction consistently.** Use “horizontal Hilbert-main-component modification” or always retain the adjective “horizontal.” Avoid the unqualified phrase “universal flattening.”

2. **State the test category before the theorem.** Include locally Noetherian, schematically dense, and finite-presentation hypotheses in one place.

3. **Isolate the schematic-density lemma.** State and prove precisely that a flat pullback of a schematically dense open remains schematically dense in the flat quotient.

4. **Separate representability from originality.** The relative Hilbert scheme is classical; the contribution is the chosen horizontal functor and its application.

5. **Clarify the sense of terminality.** It is terminal only in the admissible category with the prescribed generic embedded quotient.

6. **Give an explicit comparison with the usual flattening functor.** A commutative diagram of the two functors would prevent terminological confusion.

7. **State base-change behavior.** Identify exactly which morphisms `B' -> B` make the horizontal modification commute with base change and provide a counterexample outside that class if possible.

8. **State whether the modification is reduced, normal, or Cohen–Macaulay.** In general it need not be; the theorem should say so.

9. **Do not imply an explicit blow-up.** Unless a flattening ideal is computed, the Hilbert closure is not an explicit sequence of blow-ups.

10. **Explain independence of polarization via the representing functor.** Do not leave the impression that the two Hilbert schemes are canonically identical.

11. **Record the behavior under normalization of `B`.** This is relevant because the paper repeatedly works with normalized total graphs.

12. **Distinguish the generic section from a rational map on all of `B`.** The closure construction resolves one graph component, not every Hilbert component over the boundary.

### Strata and global organization

13. **Do not call the finite stratification canonical.** It is obtained by choices in Noetherian induction.

14. **Construct comparison maps under refinement.** Without them, different stratifications yield unrelated atlases of models.

15. **Describe specialization between strata.** State what happens when the generic point of one family approaches a lower stratum.

16. **Ask whether the models form a category or stack over the incidence poset.** At present they are merely a finite list.

17. **Identify conditions for a single full-base model.** A negative criterion would also be valuable.

18. **Separate a stratum closure from its boundary inherited from earlier strata.** The current exposition makes this hierarchy difficult to track.

19. **Compute at least one nontrivial transition between two stratumwise models.** This would test whether the proposed organization has geometric content.

20. **Avoid the phrase “global modular compactification” unless such compatibility is proved.**

### All-arc theorem

21. **List the seven recovery opens invariantly.** The rank and pivot minors should be collected in one theorem or table.

22. **Give all overlap maps among the seven charts.** Pairwise compatibility should not be delegated entirely to abstract uniqueness.

23. **Track target-coordinate changes explicitly.** State the matrices and their inverses in the fixed-target incidence diagram.

24. **State the residue-field generalization carefully.** Distinguish algebraically closed residue fields from arbitrary extensions.

25. **Prove finite presentation after every localization.** This is used by the Hilbert morphism and etaleness criteria.

26. **Give a bound or a no-bound theorem for saturation exponents.** Merely invoking Noetherian stabilization is structurally weak.

27. **Classify the saturation for monomial valuation profiles.** This is the first test toward a finite chamber theory.

28. **Identify a finite determinacy range when one exists.** If arbitrary formal arcs defeat finite determinacy, give an explicit pair of arcs agreeing to high order but producing different limits.

29. **Compute minimal and embedded primes for representative nonsymmetric arcs.** The present exact equations deserve geometric interpretation.

30. **State normality and Cohen–Macaulay criteria for the horizontal rings.**

31. **Describe how the generic incidence stratum determines the Hilbert polynomial used by the universal model.**

32. **Distinguish coverage of a pullback from classification of its fibres in every summary.**

33. **Explain whether two different arcs with isomorphic saturated charts define the same point of a global model.**

34. **Give an algorithmic statement only for polynomial/localized-polynomial arcs.** Do not use “effective” for arbitrary formal series without qualification.

### Nilpotent extension

35. **Write the square-zero extension classification theorem being used.** Include the degree convention for the cotangent complex.

36. **Give the full presentation complex.** Make clear why lower cotangent homology cannot affect the degree-one extension group.

37. **Verify transition functions for the obstruction generator.** The globalization to `O_D` should be shown on overlaps, not only inferred verbally.

38. **Distinguish the local Ext sheaf from global hyper-Ext.** The manuscript mostly does this correctly; every summary should preserve the distinction.

39. **Describe the actual algebra multiplication in local split charts.** This would make the splitting off `D` concrete.

40. **Determine whether the nonsplit class controls any deformation or modification.** Otherwise the computation remains isolated.

41. **Explain the embedded associated plane geometrically.** Relate it to first derivatives of the conic equation and to the normal cone.

42. **Check functoriality under products of first-contact fibres.** The nilpotence-order theorem suggests a richer extension algebra that is not developed.

### Ramification and toric normalization

43. **Give the semigroup saturation explicitly.** State the primitive ray generators and the quotient singularities for odd and even `m`.

44. **Describe the singular locus of the normalized total space for all `m`.**

45. **Compute discrepancies or log-canonical behavior if semistable language is retained.**

46. **State the divisor class group of the invariant chart.** This would clarify the ramification divisors.

47. **Prove global gluing of the local normalizations in a dedicated lemma.**

48. **Separate full torsion, its annihilator filtration, and Tor sheaves in every statement.**

49. **Extend one nonsymmetric ramified example beyond the path `g=r=0`.**

50. **Do not call the quadratic cover a stable reduction of curves.** It is a normalization of a parameter-space family.

### Scope, literature, and Paper I

51. **Split Paper II around one central theorem.** The horizontal functor, first-contact classification, and power-ideal theory currently compete for primacy.

52. **Move more inherited reciprocal-fibre material out of the submitted specialist paper.** Preservation in the repository does not require inclusion in the journal object.

53. **Provide a theorem-dependency graph.** The current 102-page Paper II is difficult to audit linearly.

54. **Complete a theorem-level comparison with flattening by blow-up and Hilbert main components.** The current literature discussion is mostly definitional.

55. **Expand the comparison with relative Hilbert/Quot compactifications, logarithmic modifications, and expanded degenerations.** Distinguishing targets is necessary but not sufficient for novelty positioning.

56. **Do not infer nonanticipation from a difference in vocabulary.**

57. **Obtain a genuinely independent audit of Paper I.** The audit handoff is a useful checklist, not evidence that the proof has passed review.

58. **Keep the Ballico 1993 limitation in both submitted papers.**

59. **Separate finite symbolic checks from proof evidence.** The current receipts do this responsibly and should continue to do so.

60. **State a single top-level theorem in the abstract.** At present the abstract reads as a list of successive repository achievements.

61. **Reduce terminology inflation.** “Universal,” “global,” “modular,” and “miniversal” each have restricted meanings here and should never appear without their qualifiers.

62. **Clarify the publication unit.** Two long papers plus a preservation master should not be evaluated as one indivisible top-four theorem unless the logical necessity of the package is demonstrated.

---

## 9. Response-to-v164 scorecard

### Fully or substantially closed

- replacement of “wall crossing” rhetoric by collision and horizontal-specialization language;
- recognition that the v165 branch was only an alias and not a new mathematical object;
- precise Artin test category and set-valued embedded deformation functor;
- explicit fixed-target undo diagram and frame cocycle;
- formal patching with contact-supported torsion;
- finite saturation under flat completion;
- algebraic construction before completed-local etaleness;
- retention of the coefficient projection in every graph chart;
- all-parameter Hilbert–Burch height and exactness checks;
- recovery ranks at singular and doubled conics;
- sign convention for `F_2`;
- connectedness and scheme-exhaustion logic;
- computation of the square-zero extension class;
- restoration of the larger Smith exponent as a smooth graph factor;
- exact quotient-chart transitions and divisor multiplicities;
- modular identification of the singular-conic plane;
- arbitrary six-coefficient arcs through the first nonreduced contact;
- realization of every conic by an actual coefficient arc;
- arbitrary ramification of the symmetric collision;
- complete vertical torsion rather than only first Tor;
- honest restriction to the effective failure-family image.

### Partially closed

- a universal organization of horizontal limits: achieved only stratumwise and noncanonically;
- modular interpretation of vertical excess: explained for the first contact, not globally;
- classification of interacting collisions: handled only in the six-dimensional first-contact model;
- higher-contact theory: universal existence is supplied, component geometry is not;
- comparison with other compactification frameworks: distinctions are stated, theorem-level novelty comparison remains incomplete;
- global geometry of the Hilbert boundary: one complete fibre and its local specializations are known, no full compactification is obtained;
- intrinsic failure-algebra boundary: functorial after reconstruction, not internal before it.

### Still open

- a canonical global modification encompassing all contact strata;
- compatibility and gluing of the stratumwise horizontal models;
- complete fibres for contact length at least three;
- higher-corank and singular-pencil Hilbert boundary classification;
- simultaneous collisions of unequal or higher contact order;
- a finite chamber or valuation classification of the all-arc saturations;
- global boundary divisors, incidence complex, and intersection theory;
- an external application of recognized independent importance;
- a boundary operation internal to the closed finite algebra before reconstruction;
- an independent full proof audit of Paper I;
- theorem/proof-level comparison with Ballico 1993;
- a top-four-scale conceptual principle not formal from relative Hilbert schemes and local commutative algebra.

---

## 10. Conditions for another top-four evaluation

I would not recommend another top-four round triggered by additional finite checks, another explicit ramification order, more response bookkeeping, or one more local chart.

A serious new evaluation should contain at least one result of a different order of magnitude, for example:

1. **One canonical global compactification theorem** covering all regular contact types and explaining how its local models glue across strata.

2. **A complete higher-contact fibre classification** for arbitrary smaller Smith exponent, including components, nilpotents, normalization, and adjacency.

3. **A higher-corank or singular-pencil Hilbert-boundary theorem** connecting Kronecker data to actual embedded fibres.

4. **A genuine wall or logarithmic structure** organizing interacting collisions and producing canonical transition maps among boundary models.

5. **A finite determinacy or valuation-chamber theorem** that turns the all-arc saturation recipe into a classification.

6. **An internal operation on the finite failure algebra** that detects boundary structure without first reconstructing the entire pencil.

7. **A major external application** solving a recognized problem beyond the manuscript's own pipeline.

8. **An independent proof audit of the sharp inverse**, together with a completed legitimate historical comparison or permanently narrowed priority claims.

Any one of these would change the editorial discussion. Further accumulation of local exact calculations, however strong, would not by itself do so.

---

## 11. Final assessment

Revision 166 deserves substantial credit. It is complete, reproducible, mathematically stronger than v164, and unusually responsive to detailed criticism. The distinction between full pullback and horizontal closure is now organized by a precise functor. Every discrete-valuation-ring arc through the first nonreduced contact has an exact finite chart presentation. The square-zero extension is computed rather than merely named. The vertical conics receive a coefficient-direction interpretation. Arbitrary ramification is handled with exact torsion and normalization formulas. The fixed-target and effective-category limitations are stated honestly.

I therefore reject any characterization of v166 as cosmetic, merely computational, or mathematically empty.

I nevertheless recommend rejection for *Annals*, *Acta*, *Inventiones*, or *JAMS*. The general horizontal theorem is a specialized relative-Hilbert main-component construction. The stratumwise models do not form one canonical global compactification. The all-arc theorem gives exact presentations but not a classification of their saturated geometry. Complete fibres are known only through the first nonreduced contact, while higher contact, higher corank, and singular-pencil Hilbert boundaries remain open. The failure-algebra interpretation still passes through full reconstruction. Paper I remains without the independent proof audit repeatedly requested, and the closest historical comparison remains incomplete.

The appropriate assessment is therefore:

**Reject the v166 package in its present form for a top-four general mathematics journal.**

**Paper II is a credible candidate for a strong specialist journal in algebraic geometry, Hilbert schemes, compactification theory, or invariant theory after substantial narrowing and reorganization. Paper I likewise deserves specialist consideration after an independent proof audit and sharper historical positioning.**
