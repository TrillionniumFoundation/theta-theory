# A2 revision 167 — response to the v166 referee report

Controlling report: `reviews/a2-v166-independent-harsh-top4-2026-09-26/REFEREE_REPORT.md`, commit `d5dd2e67b56c96f0a003e38e720918eba05239ca`, blob `881415d5ad9e719376a8b3eb14323f0fcb077e94`.

Revision branch: `revision/a2-v167-determinantal-hilbert-states-2026-09-26`.

## Principal mathematical response

The revision does not reduce the scope of the existing theorems or delete their proofs. It adds a determinantal Hilbert-state theorem for every polynomial contact order, a pointwise coefficient-jet bound for arbitrary generically nonincident DVR arcs, and a finite decorated chamber classification for exact monomial coefficient arcs. The weight fan includes residue cancellation. It is a finite family classification, not a claim that all special curves form a finite set. It concerns embedded curve limits, not the flat limits of the parameter graph's own fibres.

The new theorem is tested geometrically, not only symbolically: on the nonsymmetric slice `(f,g,r)=(x^2,b,cx)`, the degree-four evaluation matrix has maximal-minor ideal

`b^10 (b,c)^4 (b,c^2)^6`.

Its Hilbert graph is exactly the two successive point blow-ups, not merely dominated by them. Three explicit charts and their transitions give the complete five-case table separated by the two walls `p=q` and `p=2q`. The table applies to all generically nonincident DVR arcs on that slice, including units with arbitrary higher coefficients and the identically-zero c axis. It retains nonreduced tails and conics, minimal primes, component multiplicities, and the absence of embedded points. The exact minor order is `10p+4 min(p,q)+6 min(p,2q)` (and `20p` on c=0). The exceptional chain, self-intersections, and discrepancies are computed. The proof connects the general matrix directly to this surface by factoring all row ideals, rather than inferring an isomorphism from a proper birational map.

The horizontal Hilbert-main-component construction now has a strict-base-change theorem, a nonflat counterexample, normalization comparison, and coherent common refinements on a fixed generic open. It is not represented as gluing different generic Hilbert polynomials. This is a precise partial resolution of the global-compatibility request.

## Publication objects and preservation

`reconstruction.tex` remains the complete Paper I. `divisor-geometry.tex` is the complete revised Paper II, titled *Determinantal models and Hilbert limits of quadratic pencils*. `geometry.tex` is a complete preservation master, not a third submission. New statements are placed in a theorem/proof reading order; three inherited power/reciprocal sections are moved intact to appendices. All 390 predecessor theorem, lemma, proposition, corollary, definition, example, remark, and proof blocks are retained byte-for-byte. All predecessor labels are retained. The exact count is checked by `assemble_v167.py`, not estimated from page count.

The compiled `THEOREM_INDEX_V167.json` maps every label below to its paper, theorem number, and page. Finite exact checks are supplementary audits; they do not certify general proofs, historical originality, or journal acceptance.

## Item-by-item response

### 1. Consistent name for the horizontal construction
The new abstract, introduction, and comparison section use **horizontal Hilbert-main-component modification**. Historical filenames and byte-preserved predecessor proofs remain archival identifiers, not new unqualified flattening claims. The distinct embedded-curve graph is called the determinantal Hilbert graph.

### 2. Test category before the theorem
The first paragraph of `sec:comparison-v167` collects projectivity, finite presentation, integral finite-type base, locally Noetherian tests, and schematic density. It specifies the flat horizontal subfunctor and the prescribed generic embedded quotient before the new comparison theorem.

### 3. Flat schematic-density lemma
`lem:density-v167` proves the finite-localization injection argument explicitly. It shows exactly where quasi-compactness of the open and flatness enter.

### 4. Representability versus originality
`thm:determinantal-v167` attributes Gotzmann regularity and Hilbert representability; `rem:scope-states-v167` identifies graph blow-ups as classical. The claim supplied here is the explicit matrix for all polynomial contact orders, its use for specialization, and the calculated nonsymmetric model. No novel representability mechanism is asserted.

### 5. Qualified terminality
The category and prescribed generic quotient are fixed in `sec:comparison-v167`. Terminality is never promoted to a statement about all Hilbert components or the entire raw failure-algebra deformation category.

### 6. Comparison with full flattening
The functor diagram in `sec:comparison-v167` gives full-flat pullback as a subproblem of horizontal flatness. `ex:basechange-v167` exhibits the vertical component that prevents the converse. The comparison uses the classical full-pullback definition in Stacks Tag 052F and distinguishes pure transforms in flattening by blow-up.

### 7. Base change and a counterexample
`thm:basechange-v167` identifies the new model with the schematic main component of the old model's pullback. Equality holds for flat base change, and exactly when the prescribed generic open is schematically dense in the full product. Restriction of the blow-up of the plane to a line gives a strict counterexample in `ex:basechange-v167`.

### 8. Reducedness, normality, and Cohen–Macaulayness
The general horizontal main component is integral, hence reduced. It need not be normal or Cohen–Macaulay; taking `W=B` returns an arbitrary integral base. For the computed slice, `prop:slice-geometry-v167` proves smoothness of the parameter surface and Cohen–Macaulayness of the embedded limiting curves. These different objects are not conflated.

### 9. An explicit blow-up ideal
`thm:determinantal-v167` supplies an explicit maximal-minor ideal for every `B_a`. On the two-dimensional slice, `eq:slice-minors-v167` computes its exact factorization, including the principal factor and positive powers. The proof identifies the Rees blow-up with the stated surface. This does not claim that the same ideal flattens the parameter graph's own fibres.

### 10. Polarization independence
The last paragraph of `sec:comparison-v167` explains that independence is an identification of representing modifications for one functor, not of ambient Hilbert schemes. For explicit determinants the Segre polarization is fixed and its Gotzmann degree computed.

### 11. Normalization of the base
The last assertion of `thm:basechange-v167` gives a finite birational map from the strict model over the normalized base and identifies their normalizations. It does not replace strict pullback with unrestricted base change.

### 12. Generic section versus all boundary components
`eq:comparison-closure-v167` is explicitly the closure of the generic section. Both the introduction and `rem:scope-states-v167` distinguish this graph from other Hilbert components and from its normalization branches.

### 13. Noncanonical Noetherian stratification
The paragraph after `prop:refinement-v167` explicitly preserves the noncanonical status of the inherited stratification. No canonical incidence poset is claimed from Noetherian induction.

### 14. Comparison under refinement
`thm:basechange-v167` supplies strict comparison under base change meeting the generic open, and transitivity. `prop:refinement-v167` supplies diagonal common refinements and invariance under shrinking a dense stratum with the same reduced closure. Refinements wholly inside a lower polynomial stratum remain outside this comparison theorem.

### 15. Specialization between strata
Specializations meeting a fixed generic open are governed by strict closure and the stated comparison maps. Specializations with generic point in a different polynomial stratum still require that stratum's own horizontal problem. The new introduction separates these cases. This request is partially, not globally, resolved.

### 16. Category or stack of models
`prop:refinement-v167` gives a category of proper integral modifications over a fixed generic open with canonical products, associativity, and cocycles. No stack over an unconstructed global incidence poset is asserted.

### 17. Conditions for a single full-base object
If the original parameter family is flat on the full base, its horizontal model is the base itself. Different generic fibre polynomials cannot be fibres of one connected flat family of the entire original fibres. In contrast, the **embedded curves** on each `B_a` have one fixed polynomial and the explicit graph theorem applies over all `B_a`. These statements concern different objects and are now separated.

### 18. Stratum closure versus its inherited boundary
The generic-open hypotheses in `thm:basechange-v167` and the paragraph following `prop:refinement-v167` distinguish a dense restriction from a lower stratum contained entirely in the boundary. This avoids applying a comparison theorem outside its category.

### 19. A nontrivial transition
The transitions `k=1/e, b=e^2h` and `z=1/h, c=eh`, including inverses, are written in the proof of `thm:two-wall-v167`. They connect primitive-tail and conic states through their common doubled conic. The exact determinant factorization proves these charts belong to the same Hilbert graph, rather than being unrelated local models.

### 20. Global modular compactification language
The new introduction uses explicit determinantal graph and horizontal model terminology. It does not call the stratum list a global compactification. The scope of the all-order `B_a` graph theorem is stated affirmatively and precisely; it is not inflated to the full higher-corank pencil compactification.

### 21. Seven recovery opens
The inherited five conic evaluation charts and two primitive division charts, and their scheme-exhaustion proof, remain unchanged. The new determinant matrix gives one global projective description of the embedded graph independent of choosing those seven opens. A new exhaustive invariant pivot-minor table for the original seven charts has not been separately added.

### 22. All overlap maps
All overlaps of the new three-chart nonsymmetric surface are explicit and checked. The seven-chart all-arc cover retains its existing uniqueness/recovery comparison; a fully expanded table of every pair among those seven charts is not represented as completed.

### 23. Fixed target and inverse coordinate changes
The inherited fixed-target comparison, five target matrices, and undo cocycle are retained. The nonsymmetric calculation makes no target change at all, so its ideals and limits can be compared directly in `[F:G:R]`. `cor:effective-states-v167` applies these fixed-target comparisons after reconstruction.

### 24. Residue fields
The determinant, jet, chamber, and slice statements allow DVRs containing `C` with arbitrary residue field extension `k/C`. The exact-monomial coefficient-state theorem is formulated over `k[[tau]]` or `k[tau]_(tau)`, with its constant-field embedding specified; the general DVR and slice theorems need no such choice. Primitive minor coordinates and polynomial residue strata are defined over that field. No unqualified positive-characteristic generalization is made.

### 25. Finite presentation
The determinant model is a Rees algebra of a finitely generated ideal in a finite-type polynomial ring; its affine blow-up charts have finite presentations. The three slice charts are polynomial rings with displayed finite ideal generators. Existing finite-presentation arguments for the inherited Hilbert recovery charts are retained.

### 26. Saturation bound or no-bound theorem
`prop:smith-v167` gives exact invariant-factor exponents and minor order for the finite evaluation module. `prop:no-saturation-bound-v167` proves that exponents for saturation of full parameter-family pullbacks are unbounded even at fixed contact order two, using the exact torsion order in the inherited ramification theorem. The two assertions are deliberately not interchanged.

### 27. Monomial valuation classification
`thm:finite-fan-v167` gives a finite decorated classification for all exact monomial coefficient profiles at each fixed `a`, including cancellations. `cor:slice-chambers-v167` computes the full five-case answer on the nonsymmetric slice. The general fan is constructive but potentially enormous and is not asserted to be minimal.

### 28. Finite determinacy and high-order witnesses
`prop:jet-v167` proves the pointwise bound `mu+1` for arbitrary generically nonincident DVR coefficient arcs. `cor:no-uniform-v167` constructs arcs agreeing to any prescribed finite order but yielding different fixed-target conics. This replaces an undifferentiated absence of a finite-jet algorithm with a positive local bound and an exact nonuniformity statement.

### 29. Primes for nonsymmetric arcs
`prop:slice-geometry-v167` lists all minimal primes and multiplicities for each of the five cases. It proves there are no embedded associated points. The exact matrix checks independently confirm that the displayed ideals span the entire degree-four Hilbert kernel in representative cases from every chamber and wall.

### 30. Normality and Cohen–Macaulay criteria
The new slice parameter surface is smooth and normal; every embedded curve in its table is Cohen–Macaulay. Attached curves are not normal as whole schemes, and normalizations of their reductions are described separately. A normality/CM classification of horizontal parameter rings for every arbitrary six-coefficient formal arc is not claimed.

### 31. Generic incidence and Hilbert polynomial
For generically nonincident coefficient arcs in `B_a`, the embedded curve polynomial is `(a+1)l+1`. Parameter-family strata can have different generic fibre polynomials; this is explained before `sec:comparison-v167`. The introduction now distinguishes these polynomials before invoking either construction.

### 32. Coverage versus classification
The inherited all-arc theorem remains a presentation/exhaustion theorem. The new classification theorem has its exact monomial domain stated; the complete five-case geometric table has its two-dimensional slice stated. These are separate, stronger conclusions on their specified domains, not a renaming of chart coverage.

### 33. Same point of a model
For arcs centred at one coefficient point, `thm:determinantal-v167` proves equality of embedded limits is equivalent to proportionality of primitive Plucker vectors, hence to equality of points on the unnormalized retained-coefficient graph. `rem:scope-states-v167` explicitly excludes the inference that lifts to distinct normalization branches must coincide.

### 34. Algorithmic domain
Finite polynomial input admits matrix evaluation, Smith reduction, and finite residue-polynomial operations. The symbolic exact-monomial theorem is finite. For arbitrary formal arcs the theorem is mathematical pointwise finite determination; it is not advertised as an algorithm for an unspecified oracle for all coefficients.

### 35. Square-zero classification and degrees
`sec:local-algebra-v167` states the extension classification, the specified kernel and quotient, and cohomological degrees `-1,0` of the presentation complex.

### 36. Presentation complex and lower homology
The same section explains why the part in degrees at most `-2` cannot contribute to degree-one Ext against a module in degree zero. It does not assert a two-term model for the whole cotangent complex or a complete-intersection presentation.

### 37. Obstruction transition function
Local representatives from the same algebra extension differ by derivations under changes of polynomial lifts. After passing to the Ext sheaf, the basis defined by the actual extension has overlap function exactly `1`. This is shown in `sec:local-algebra-v167`; it is not a claim that the nilradical line bundle itself is trivial.

### 38. Ext sheaf versus global hyper-Ext
Both the inherited theorem and the new clarification identify the **image** of the global class in the local obstruction sheaf. No dimension statement for the whole global hyper-Ext group is inferred.

### 39. Multiplication in split charts
After inverting `C`, the algebra is explicitly written as `C[lambda,A,B,C,C^-1,n]/(n^2,An,Bn)`, with `e=n/C`. The multiplication law of the square-zero direct sum is displayed.

### 40. Further consequences of the nonsplit class
The class obstructs a local algebra retraction along the doubled-line curve and is distinguished from the larger support of the embedded associated plane. A new derived enhancement or global modification determined by this class is not proved here. This request remains only partially resolved.

### 41. Meaning of the embedded plane
`sec:local-algebra-v167` identifies the singular-conic plane by vanishing of the first-order part of the conic equation at the attachment, and distinguishes its discriminant-zero doubled-line curve. A new global normal-cone comparison beyond these equations is not asserted.

### 42. Extension algebra for products
The inherited exact product-fibre and nilpotence results remain complete. A new computation of all product extension classes and their cross terms is not supplied; this is listed as a remaining question rather than certified by the single-contact calculation.

### 43. Semigroup and primitive rays
`prop:toric-classes-v167` gives the saturated semigroup, dual lattice, primitive rays `(1/gcd(m,2),0)` and `(0,1)`, and the odd/even quotient types after removing the pseudoreflection in the even case.

### 44. Singular locus for every ramification order
The same proposition proves that the transverse normalized surface is smooth precisely for `m=1,2`; otherwise its only singular point is the origin. Including the independent lambda coordinate gives the corresponding singular line in the full chart.

### 45. Discrepancies and semistability terminology
The nonsymmetric smooth surface has the explicit relative canonical divisor `E11+2E21` in `prop:slice-geometry-v167`. No global semistable or stable-curve claim is made. A complete discrepancy calculation for every cyclic quotient of the inherited symmetric family is not claimed.

### 46. Divisor class group
`prop:toric-classes-v167` computes `Cl = Z/(m/gcd(m,2))` using the primitive toric-divisor pairing. This includes the smooth cases and is not a class-group computation for the unnormalized hypersurface.

### 47. Gluing normalizations
`lem:normalization-gluing-v167` proves the localization statement and the resulting overlap cocycle in one common function field. The inherited local normalizations therefore glue without choosing an extra cyclic cover.

### 48. Torsion, filtration, and Tor
The inherited exact length-m torsion module and last-layer Tor statement are retained. `prop:no-saturation-bound-v167` uses the full module, while `prop:smith-v167` concerns a different finite evaluation cokernel. Every new summary separates these objects.

### 49. Nonsymmetric ramified examples
The table for `b=beta*tau^p, c=gamma*tau^q` has `r=cx` nonzero generically and covers all positive p,q, not just one ramification order of `g=r=0`. Simultaneously multiplying p,q by a positive integer retains its embedded limit while changing the pullback orders of the parameter divisors.

### 50. Not stable reduction of curves
The smooth toric surface, its normal-crossing boundary, and the cyclic normalized parameter charts are consistently described as parameter-space constructions. They are not called stable reduction of embedded curves or maps.

### 51. One central theorem and architecture
The abstract and introduction are rebuilt around the determinantal Hilbert-state theorem and its geometric two-wall calculation. Horizontal parameter-family comparison is secondary infrastructure. All inherited mathematics is preserved, with three power/reciprocal sections moved intact to appendices. The revision does not convert the project into a narrower specialist submission.

### 52. Reciprocal material and nondeletion
The power coefficients, universal power ideals, and reciprocal complete-quadric graph sections are moved intact to appendices. Earlier reciprocal-fibre appendices remain. The master and all prior sources stay available; the body preservation receipt checks every prior mathematical block.

### 53. Theorem-dependency graph
The introduction contains a proof-dependency display; `THEOREM_DEPENDENCIES_V167.md` gives labels and the separation from Paper I. The compiled index resolves all labels to actual page and theorem numbers.

### 54. Classical flattening and Hilbert-main-component comparison
`sec:comparison-v167` compares the represented problems and gives a counterexample to confusing them. The determinant theorem explicitly invokes classical Hilbert regularity and graph Rees algebra before calculating the input ideal. `LITERATURE_AUDIT_V167.md` distinguishes theorem statements checked, bibliography checked, and full texts not obtained.

### 55. Hilbert/Quot, logarithmic, and expanded constructions
The fixed-target embedded quotient and flat-pullback comparison are expanded. The slice gives a normal-crossing parameter boundary, but no equivalence with a logarithmic or expanded-degeneration moduli stack is established. Existing target distinctions remain; a complete theorem-level comparison across those broader frameworks is still open.

### 56. No vocabulary-based priority claims
The introduction and literature record explicitly reject the inference of nonanticipation from different terminology or from weighting coefficient variables rather than ambient coordinates. The general Hilbert/Gröbner/state-polytope background is credited.

### 57. Independent audit of Paper I
No external independent full audit was obtained. The full sharp-inverse proof, the prior handoff, and its exact dependencies are retained. `cor:effective-states-v167` is an application, not an audit. Neither this revision nor its automated checks is represented as independent certification.

### 58. Ballico 1993 limitation
The limitation appears explicitly in both papers' introductory material and in the inherited literature discussion. The legitimate complete text and theorem-by-theorem comparison have not been obtained. No new priority conclusion is drawn from the failed documentary comparison.

### 59. Finite checks versus proof
`check_v167.py` tests the exact slice minor ideal, all five degree-four Hilbert kernels, chart identities, degree formulas, and finite toric class examples. The general statements are proved in the manuscript. Every receipt marks that computation does not certify the proofs or novelty. The inherited full check chain is rerun during remote publication.

### 60. A single top-level abstract
The abstract leads with the determinantal model and its specialization/classification consequences. The two-wall slice is the full geometric calculation of that theorem's input, not an unrelated increment. The abstract no longer enumerates successive repository revisions.

### 61. Restricted terminology
The new prose distinguishes embedded graph, normalized parameter graph, horizontal Hilbert-main-component modification, monomial decorated classification, and arbitrary-arc finite determination. It does not use unqualified universal flattening, a canonical global stratum compactification, or a complete classification of all higher-corank boundaries.

### 62. Publication unit
Two complete papers are retained with distinct dependency directions. The master is explicitly an audit/preservation object, not a third journal submission or a claim that the whole package is one indivisible theorem. No contents have been removed merely to obtain a shorter page count.

## Remaining mathematical and documentary obligations

The new finite decorated classification and pointwise jet theorem directly address the report's fifth proposed route to a substantial new evaluation. The complete slice adds an actual global two-dimensional modification and wall adjacency, not only substitution-and-saturation instructions. Nonetheless, this revision does not claim a full component/normalization classification of every higher-contact parameter fibre, a higher-corank or singular-pencil Hilbert-boundary theorem, gluing all distinct generic-polynomial strata into one modular stack, an internal boundary operation before reconstruction, or a major external application. The full Paper I audit and Ballico comparison are also not complete. These obligations remain visible while the existing scope and proofs are maintained.
