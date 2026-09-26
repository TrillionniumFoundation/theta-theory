# A2 v170 response to the second independent v167 report

This response is incremental relative to the **complete v169 manuscript**, commit
`81e0870e31078a3aaac6006b676ca54667e6d77a`. The controlling latest report is the
second v167 report at `f50f6a7b194adbb42813988d3e68a43d71ccc520`; the earlier
report is at `be1987dd1a37064c0bea291d7ad38ccd12cc5951`. Both report texts are
byte-locked in this package. Neither report is falsely described as a review of v169.

The new principal theorem treats **all a>=2 and all coefficient powers rho,sigma>=1**:
normalization of the full pulled-back Hilbert graph, complete parameter-fibre
scheme structure, a global conductor without hidden crossing conditions,
normalization root labels, and coherent marked root-cover comparisons. Its
proofs are in `ramified-boundary-v170.tex` and `conductors-and-lifts-v170.tex`.
The original embedded-curve equations and their punctual modules remain intact.

Each numbered item below first retains the v169 response verbatim, then identifies
what v170 adds or does not add. Earlier work is not relabelled as new work.
All requests have a response; not every full-B_a, higher-corank, or documentary
request has thereby been completed. See `REFEREE_CROSSWALK_V170.md` for actual
compiled theorem/page locators and `THEOREM_DEPENDENCIES_V170.md` for the proof route.

### 1. Graph versus Pluecker presentation

**Retained v169 response.**

Proposition `prop:content-v169` separates the rational map, its coordinate list, and its target embedding. The graph is canonical for the specified generic embedded problem; a raw maximal-minor ideal is not independent of all presentations.

**v170 amendment.** Theorem `thm:ramified-boundary-v170` distinguishes the integral Hilbert graph Y, its normalization Z, and the parameter fibre F. They are not identified with the raw list of maximal minors.

### 2. Divisorial content

**Retained v169 response.**

Section `sec:content-v169` defines C(I), I**, and I^pr on a regular integral base. Proposition `prop:incidence-content-v169` proves that the full B_a ideal has no height-one content, although its nonflat restriction can acquire such content.

**v170 amendment.** The retained response continues to apply. No additional mathematical closure of this request is asserted by the ramified-boundary theorem.

### 3. Primitive finite jets

**Retained v169 response.**

Proposition `prop:primitive-jet-v169` gives the content-free posterior bound. Theorem `thm:sharp-jet-v169` goes further on the all-order marked family: ord(b)+1 is sufficient and uniformly optimal, independently of a and the Hilbert degree.

**v170 amendment.** No new bound is obtained by relabelling raw content. The sharp marked-family bound from v169 is retained. The new normalized root label is additional information, not something recoverable from a Hilbert point alone; see `cor:hilbert-lifts-v170`.

### 4. Changing Hilbert degree

**Retained v169 response.**

Proposition `prop:degree-change-v169` identifies the common graph, universal curve, normalization, and exceptional divisorial valuations. It does not identify the ideals, their divisor orders, or Smith factors. Example `ex:degree-content-v169` exhibits the difference.

**v170 amendment.** The rays, conductor, fibre lengths, residue degrees, and cyclic quotient charts in `thm:ramified-boundary-v170` are independent of m. In contrast, the exponents E_j still occur in the graded Rees algebra `eq:ramified-rees-v170` and are not declared degree-independent.

### 5. Integral closure

**Retained v169 response.**

Proposition `prop:rees-v169` computes the exact normal Rees algebra and all powers of the primitive restricted ideal for every a. This is not a claimed integral-closure formula for the full B_a maximal-minor ideal; that larger computation is not completed here.

**v170 amendment.** Proposition `prop:ramified-rees-v170` computes the integral closure in every Rees degree after every diagonal coefficient cover, including unequal powers. The raw algebra need not be normal; it is not silently equated with its integral closure. A full-B_a closure formula remains outside this theorem.

### 6. Rees valuations beyond the two-wall slice

**Retained v169 response.**

Theorem `thm:chain-model-v169` and Proposition `prop:rees-v169` identify all a exceptional valuations v_i(b)=i, v_i(c)=1. For a=3 the three rays, rather than only the earlier two, are explicitly realized.

**v170 amendment.** For all a,rho,sigma, the primitive Rees valuations are (i sigma/g_i,rho/g_i), with g_i=gcd(rho,i sigma). Their ramification indices and residue degrees are respectively rho sigma/g_i and g_i. See `prop:ramified-rees-v170` and `eq:root-residue-v170`.

### 7. Fitting and graph ideals

**Retained v169 response.**

Equation `eq:eval-covariant-v169` is the natural evaluation module; its Fitt_0 is distinguished from the primitive and unweighted graph ideals. Equation `eq:basepoint-fitt-v169` is a second, smaller finite-basepoint-module Fitting presentation, with equality asserted only for radicals.

**v170 amendment.** The retained response continues to apply. No additional mathematical closure of this request is asserted by the ramified-boundary theorem.

### 8. Incidence scheme versus support

**Retained v169 response.**

Proposition `prop:incidence-content-v169` gives the companion-matrix presentation of A[x]/(f,g,r), not only a set-theoretic description. It does not identify this Fitting scheme with the large evaluation base scheme. The marked-family formula gives the latter scheme exactly on S_a.

**v170 amendment.** The retained response continues to apply. No additional mathematical closure of this request is asserted by the ramified-boundary theorem.

### 9. Coordinate covariance

**Retained v169 response.**

Equation `eq:eval-covariant-v169` states the symmetric-power source/target action on the actual quotient map. Theorem `thm:global-gluing-v169` supplies explicit pivot charts, undo matrices, and boundary cocycles.

**v170 amendment.** Proposition `prop:log-compatibility-v170` adds coherent root-cover comparison and gluing under units on two marked Cartier boundaries. It does not assert that arbitrary unmarked coordinate changes preserve this fan; the larger fixed-degree equivariance remains the separate v169 theorem.

### 10. The meaning of raw minor order

**Retained v169 response.**

The text consistently treats raw order and Smith length as invariants of a specified evaluation presentation. Equations `eq:raw-order-v169` and `eq:all-order-factor-v169` separate them from the graph and its exceptional valuations.

**v170 amendment.** The distinction is maintained. None of the new conductor, normality, parameter-fibre, or root-label formulas uses the raw minor order.

### 11. Size estimates

**Retained v169 response.**

Section `sec:content-v169` records q, N, their asymptotics, and the logarithmic upper bound for the candidate-minor count. No practical efficiency for arbitrary full B_a is claimed.

**v170 amendment.** The retained response continues to apply. No additional mathematical closure of this request is asserted by the ramified-boundary theorem.

### 12. A structural substitute for minor enumeration

**Retained v169 response.**

Theorem `thm:chain-model-v169` proves an all-order row-ideal factorization into `a` two-generator ideals. Proposition `prop:curve-charts-v169` replaces Hilbert elimination on this family by at most a+1 uniform monic equations per chart. This is a structural theorem for all a, not a list of small numerical cases.

**v170 amendment.** The new normalization is specified by a two-dimensional fan and the finite inequalities in `eq:ramified-rees-v170`, rather than a larger matrix. The conductor is a divisorial ideal with explicit orders; all crossing conditions are settled by `lem:conductor-depth-v170`.

### 13. Lower-degree equations

**Retained v169 response.**

Equations `eq:curve-first-v169`, `eq:curve-middle-v169`, and `eq:curve-last-v169` recover the universal curve using low bidegrees and uniform syzygy reductions. The worst-case Gotzmann degree is used for identification, not for writing the curve equations.

**v170 amendment.** The universal curve on Z is the flat pullback of the same low-degree monic family. Parameter normalization does not normalize its embedded curve fibres; their original ideals and punctual modules remain in the manuscript.

### 14. Same Hilbert point, different Smith length

**Retained v169 response.**

Example `ex:degree-content-v169` varies the Hilbert degree without changing the graph. After `eq:raw-order-v169`, two order-three arcs have the same embedded limit and raw lengths 84 and 168.

**v170 amendment.** The retained response continues to apply. No additional mathematical closure of this request is asserted by the ramified-boundary theorem.

### 15. Minimality of a graph ideal

**Retained v169 response.**

Proposition `prop:degree-change-v169` explains why inclusion-minimality is the wrong condition: positive powers give smaller ideals with the same blow-up. K_a is degree-independent and has exactly the effective Newton rays, not an inclusion-minimal ideal.

**v170 amendment.** The retained response continues to apply. No additional mathematical closure of this request is asserted by the ramified-boundary theorem.

### 16. Sufficient versus optimal bounds

**Retained v169 response.**

The primitive posterior bound is explicitly only sufficient. The distinct theorem `thm:sharp-jet-v169` proves optimality of ord(b)+1 uniformly on the marked family with prescribed ord(b). The two claims are not conflated.

**v170 amendment.** The retained response continues to apply. No additional mathematical closure of this request is asserted by the ramified-boundary theorem.

### 17. Formal oracles versus finite algorithms

**Retained v169 response.**

The discussion after `prop:primitive-jet-v169` distinguishes pointwise determination from discovering the relevant order through a formal oracle. Exact polynomial and localized-polynomial inputs admit terminating algebraic computation; no finite oracle budget is asserted.

**v170 amendment.** The retained response continues to apply. No additional mathematical closure of this request is asserted by the ramified-boundary theorem.

### 18. Content-free two-wall bound

**Retained v169 response.**

Theorem `thm:sharp-jet-v169` includes a=2 and improves on merely subtracting 10p: ord(b)+1 suffices. The primitive degree-m and unweighted ideal orders are both displayed separately in `eq:raw-order-v169` and its discussion.

**v170 amendment.** The retained response continues to apply. No additional mathematical closure of this request is asserted by the ramified-boundary theorem.

### 19. Domain of monomial classification

**Retained v169 response.**

The inherited general coefficient result remains explicitly for exact monomial profiles. Proposition `prop:fan-comparison-v169` preserves that restriction. In contrast, `thm:arc-table-v169` applies to arbitrary formal units beta and gamma on S_a.

**v170 amendment.** The root-label statement `cor:hilbert-lifts-v170` applies to arbitrary DVR arcs in the stated marked family with positive u,v orders, not merely exact monomial coefficient arcs. It is not promoted to a classification of arbitrary arcs in B_a.

### 20. Unit coordinates and nonzero centres

**Retained v169 response.**

Proposition `prop:fan-comparison-v169` allows nonnegative weights, specified units, identically zero patterns, and polynomial translation around a fixed centre. Corollary `cor:moving-v169` gives an actual moving-contact geometric family.

**v170 amendment.** The retained response continues to apply. No additional mathematical closure of this request is asserted by the ramified-boundary theorem.

### 21. Changes of decorated fans

**Retained v169 response.**

Proposition `prop:fan-comparison-v169` proves pullback refinement under monomial substitutions and comparison after polynomial composition. A polynomial change can destroy the monomial form of an arc; an isomorphism of the displayed fans is not asserted in that case.

**v170 amendment.** Successive monomial root maps are now treated geometrically: normalizing the iterated pullback canonically gives Z_(a,rho r,sigma s), with associative comparison maps. The marked-unit gluing is proved in `prop:log-compatibility-v170`.

### 22. Tropical Pluecker comparison

**Retained v169 response.**

Section `sec:equivariant-v169` compares valuations of actual minors with realizable valuated-matroid and tropical Grassmannian data, citing the precise primary-source formulation. Valuations alone forget the wall residues; not every tropical quadratic solution is declared realizable.

**v170 amendment.** The bend loci of the functions min(rho p,j sigma q) give the minimal marked normal fan. Its root residues contain information beyond those valuations. This does not identify it with the tropical Grassmannian or an intrinsic fan of all coefficient charts.

### 23. Comprehensive Groebner comparison

**Retained v169 response.**

The same section compares residue partitions with parameter-specialization systems. The proof of `prop:curve-charts-v169` is stronger on each displayed chart: all leading coefficients are units and the single monic basis specializes over every coefficient point.

**v170 amendment.** The retained response continues to apply. No additional mathematical closure of this request is asserted by the ramified-boundary theorem.

### 24. Effective rather than redundant walls

**Retained v169 response.**

Proposition `prop:rees-v169` computes the Newton facets, all with positive length; `thm:arc-table-v169` identifies their distinct embedded wall families. The marked-family fan is minimal. The full coefficient-support arrangement is still described as a potentially redundant refinement.

**v170 amendment.** Every bend ray is required for simultaneous principalization, and the inherited wall curves identify the corresponding Hilbert degeneration. No redundant hyperplane refinement is inserted. See `prop:log-compatibility-v170`.

### 25. A minimal order-three fan

**Retained v169 response.**

Equation `eq:cubic-factor-v169` and the following table give rays (1,1),(2,1),(3,1), three exceptional curves, and seven exact embedded families. Their fan is minimal by `thm:arc-table-v169`.

**v170 amendment.** Example `ex:third-ramified-v170` has rays (3,2),(3,1),(9,2), four explicit cyclic quotient indices, and a nonreduced parameter fibre. The theorem proves these formulas for all contact orders and all powers; the order-three instance is only an illustration.

### 26. Higher-order residue-stratum geometry

**Retained v169 response.**

Each jth wall is G_m inside E_j=P1, with two explicitly identified endpoints O_(j-1),O_j. The complete parameter fibre has `a` one-dimensional components in a chain, and the closure and intersection relations are stated in `thm:arc-table-v169`.

**v170 amendment.** Theorem `thm:ramified-boundary-v170` gives all a components, generic lengths, node adjacencies of the reduced fibre, and no embedded associated points after arbitrary ramification. The open residue strata are G_m with finite power maps of degree g_i; their endpoints and lifts are explicit.

### 27. Finite algebraic families

**Retained v169 response.**

The exact monomial result is called a classification into finitely many algebraic families, not finitely many curves or automorphism types. The all-order family likewise distinguishes a+1 chamber points from `a` nonconstant one-dimensional wall families.

**v170 amendment.** The retained response continues to apply. No additional mathematical closure of this request is asserted by the ramified-boundary theorem.

### 28. Normalization branches

**Retained v169 response.**

Proposition `prop:degree-change-v169` and the comparison discussion preserve the distinction between a graph point and a normalization lift. On T_a there is no branch ambiguity because the whole surface is smooth; no analogous assertion is made for an arbitrary point of Gamma_a.

**v170 amendment.** This is a substantive change relative to v169: `cor:hilbert-lifts-v170` exhibits g_i different normalization points with identical retained coefficients and identical embedded Hilbert limit. Every root label is realized by an arc; at torus-fixed boundary points the lift is unique.

### 29. Embedded equality versus isomorphism

**Retained v169 response.**

The Hilbert kernel and residue vector determine fixed-target embedded equality only. Proposition `prop:target-equivalence-v169` treats the separate target-automorphism relation. Abstract curve isomorphism is not inferred from either finite partition.

**v170 amendment.** Embedded equality still does not imply target-automorphism or abstract isomorphism classification. The new corollary additionally separates embedded equality from equality on the normalization.

### 30. Target-automorphism criterion

**Retained v169 response.**

Proposition `prop:target-equivalence-v169` gives the invariant criterion that a symmetric-power target action identify the degree-m kernels. It is a finite rank-condition test on PGL_3. On each marked wall all nonzero residues are target-diagonally equivalent, although the embedded points differ.

**v170 amendment.** The inherited target-action criterion is unchanged. The new root labels cannot be distinguished by any invariant of the embedded curve alone, since their embedded curves are literally equal at the same coefficient centre.

### 31. Removing b^10

**Retained v169 response.**

The general content proposition and all-order formula include exactly the earlier factor b^10 when a=2,m=4. Its removal is now a stated structural step, not a parenthetical simplification.

**v170 amendment.** The retained response continues to apply. No additional mathematical closure of this request is asserted by the ramified-boundary theorem.

### 32. Newton polygon and rays

**Retained v169 response.**

Proposition `prop:rees-v169` proves the full Newton lower-boundary formula, with slopes -a through -1 and positive edge lengths E_a through E_1. Their primitive normals are the actual Rees valuations.

**v170 amendment.** The transformed Newton polygon has primitive normals (i sigma/g_i,rho/g_i). Its supporting inequalities give all normalized Rees degrees in `prop:ramified-rees-v170`.

### 33. Normalized Rees algebra

**Retained v169 response.**

Equation `eq:rees-semigroup-v169` is an explicit semigroup presentation. Every lattice point satisfying the inequalities belongs to the actual Rees algebra, so no extra normalization generators are hidden. The raw content shift is also stated.

**v170 amendment.** Equation `eq:ramified-rees-v170` and chart formula `eq:normal-chart-v170` explicitly compute the normalized algebra and all overlaps for arbitrary covers. Unlike the unramified case, normality is not asserted for the raw Rees algebra.

### 34. Picard group and boundary classes

**Retained v169 response.**

Proposition `prop:boundary-v169` gives Pic(T_a), both total axis divisors, the intersection matrix, the relative canonical divisor, and the relative nef inequalities, for all a.

**v170 amendment.** Proposition `prop:ramified-singularities-v170` adds all cyclic chart class groups, axis divisors, rational intersection numbers, and relative canonical coefficients. These are Weil/Q-Cartier statements where appropriate, not an unsupported Cartier Picard assertion on a singular surface.

### 35. Contractions

**Retained v169 response.**

The same proposition constructs contraction morphisms by deleting rays and identifies the A-type singularities of intermediate contractions. The last-ray contractions agree with the ordinary point-blowdown sequence.

**v170 amendment.** The inherited unramified contractions remain. The normalized fan supplies toric contraction maps by coarsening; the new minimality statement concerns simultaneous principalization of the marked ideals, not a claim that every contraction is smooth.

### 36. Stable maps, stable quotients, and cycles

**Retained v169 response.**

Proposition `prop:quot-contraction-v169` constructs a genuine morphism to the fixed-source Quot scheme and proves that it contracts the entire chain. Three markings verify stable-quotient stability. Corollary `cor:external-curves-v169` explains why cycle data and reduced nodal-map images do not recover the punctual nilradical.

**v170 amendment.** The same universal curve is pulled back, so the earlier Quot and cycle comparisons remain valid. Distinct normalization root labels above one Hilbert point are an additional loss of parameter information, separate from loss of a punctual curve nilradical.

### 37. Order-three analogue

**Retained v169 response.**

The a=3 factorization, seven ideals, associated-point lengths, and three-component parameter chain are all explicit. In particular the three last cases have length-one embedded points; those are not suppressed to make the answer Cohen--Macaulay.

**v170 amendment.** The order-three unequal-cover example is completely specified by the general theorem. Its conductor is (2,3,8), fibre lengths (2,1,2), and residue degrees (1,2,1); see `ex:third-ramified-v170`.

### 38. Moving f coefficients

**Retained v169 response.**

Corollary `cor:moving-v169` treats (x-alpha)^a with a varying source centre and writes the source undo map. This is an actual family with varying f, not a claim about arbitrary coefficients of a monic f.

**v170 amendment.** The inherited source-moving orbit family is retained. Marked smooth/etale coefficient charts can additionally carry the root-cover construction, but this does not turn f=(x-alpha)^a into an arbitrary monic-f coefficient slice.

### 39. Mixed constant and linear terms

**Retained v169 response.**

Equation `eq:mixed-family-v169` and its invertible target matrix give, at a=2, families where both g and r have constant and linear terms. The open condition 1-uv nonzero and the precise orbit-family scope are retained.

**v170 amendment.** The inherited invertible target changes remain applicable to the pulled-back universal curves. No arbitrary mixed-coefficient full-neighbourhood classification is claimed.

### 40. Normalization of the five earlier limits

**Retained v169 response.**

Theorem `thm:chain-model-v169` specializes to the smooth two-blow-up model when a=2. Each of its five earlier curve types lies at a point of the same integral normal surface, with the two exceptional components joined at one ordinary surface-chart point.

**v170 amendment.** The old smooth model has unique lifts. The covers now exhibit genuine multiple normalization lifts, computed on every wall by `eq:root-residue-v170`; crossings still have unique lifts. They must not be confused with different irreducible components of the integral total surface.

### 41. Local rings from the Rees algebra

**Retained v169 response.**

Equation `eq:chain-charts-v169` gives polynomial rings k[e,h] obtained from adjacent unimodular Rees cones. The wall-intersection local ring is k[e,h]_(e,h), not an unspecified normalization of a singular chart.

**v170 amendment.** Every normal local chart is the explicit semigroup ring `eq:normal-chart-v170`. The raw charts `eq:raw-cover-charts-v170` are hypersurfaces or complete intersections; their conductor has no further isolated condition at the crossing. Equal powers give explicit principal conductor generators in `cor:equal-power-v170`.

### 42. Universal property of the chain

**Retained v169 response.**

The final paragraph of `sec:chain-model-v169` gives its universal property for integral tests making every marked ideal (b,c^j) invertible. This is intrinsic to that marked ideal system. General coefficient changes transport the system; they do not make it a canonical boundary complex for every pencil.

**v170 amendment.** Proposition `prop:log-compatibility-v170` proves the terminal normal principalization property for the marked ideal system and compatible root covers. It extends to two specified transverse Cartier divisors; it is not an unmarked all-pencil modular universal property.

### 43. The complete B_3 fibre

**Retained v169 response.**

The revision proves a complete all-order S_a fibre and universal-curve theorem, including the order-three case. It does not identify that slice fibre with the full B_3 fibre. The latter classification is not completed, and neither the abstract nor the response labels it completed.

**v170 amendment.** The new complete fibre theorem is for every ramified marked family and includes a=3. It does not compute the entire full-B_3 fibre. That distinction remains explicit in the theorem, abstract, and review entry, rather than being counted as closure of this broader request.

### 44. Components and dimensions

**Retained v169 response.**

For T_a the exact answer is `a` copies of P1, with the dimensions and all incidences in `prop:boundary-v169` and `thm:arc-table-v169`. The manuscript explicitly separates that theorem from the uncomputed complete component list over B_3.

**v170 amendment.** For the ramified marked parameter fibre, the exact answer is a one-dimensional components, all P1 after reduction, with chain incidences and lengths min(rho,i sigma)/g_i. This is proved scheme-theoretically, not asserted as the component list of the full B_3 fibre.

### 45. Nilradicals and embedded associated points

**Retained v169 response.**

Theorems `thm:punctual-v169`, `thm:genus-correction-v169` and Proposition `prop:terminal-v169` compute every relevant local ring, punctual module, generic multiplicity, and associated point on the marked family for all a. They do not present these as the nilradical of the entire B_3 parameter fibre.

**v170 amendment.** The parameter-fibre nilradical now has exact order max_i min(rho,i sigma)/g_i and no embedded associated points (`lem:coordinate-ideal-v170`). The separate punctual nilradical of the embedded universal curves remains as computed in v169. These two statements concern different rings.

### 46. Normalization and intersections

**Retained v169 response.**

The parameter surface is normal and smooth. Its fibre normalization is the disjoint union of a projective lines with the stated chain incidence. The reductions of the universal curves and the cuspidal normalization are given in `eq:cusp-normalization-v169`. These are distinct normalization operations.

**v170 amendment.** All normalization charts, branch power maps, and crossings of the marked ramified graph are computed; the global conductor records the gluing defect. This is a new example of nontrivial normalization branches, not a full-B_3 branch classification.

### 47. Smith data and geometric input

**Retained v169 response.**

The marked contact order a is the order of f at the attachment and is the smaller exponent on the relevant corank-two contact normal form. The formulas are transported only through the inherited fixed-target comparison. Smith exponents without a specified coefficient direction do not select a point of the boundary chain.

**v170 amendment.** The contact order a is unchanged by coefficient ramification. The extra integers rho,sigma specify the family direction and are not recoverable from the Smith exponent alone. The new formulas retain this data explicitly.

### 48. Higher corank

**Retained v169 response.**

The new theorems do not classify a higher-corank quadratic-pencil Hilbert fibre. The global degree-a graph applies to a nonzero triple and does not repair an identically zero adjugate tuple. The earlier inverse and singular invariants remain intact, without being recast as an unproved fibre theorem.

**v170 amendment.** The all-order ramified corank-two construction is not a higher-corank Hilbert-fibre theorem. The existing higher-corank inverse data are preserved without claiming they supply a missing adjugate graph.

### 49. Nontrivial singular Kronecker data

**Retained v169 response.**

The existing singular-pencil reconstruction and invariant statements are preserved. A new embedded Hilbert fibre theorem for arbitrary nontrivial Kronecker blocks is not claimed. This scope is stated separately from the all-order marked corank-two calculation.

**v170 amendment.** No arbitrary singular-Kronecker Hilbert fibre is asserted. Existing singular-pencil mathematics remains intact; the new graph is the nonzero marked rational-map family explicitly stated in the theorem.

### 50. Different generic Hilbert polynomials

**Retained v169 response.**

Proposition `prop:conservation-v169` proves the precise constancy constraint: unaugmented graphs of two degrees cannot be fibres of one connected flat projective family. A fixed-degree compactification instead retains tails and punctual genus corrections. The global gluing theorem uses one fixed polynomial throughout.

**v170 amendment.** Root-cover compatibility preserves one generic Hilbert polynomial throughout. It does not evade the constancy obstruction for different unaugmented degrees proved in `prop:conservation-v169`.

### 51. The meaning of global

**Retained v169 response.**

Theorem `thm:global-gluing-v169` now proves one projective equivariant object over the full projective space of degree-a triples and actual patch cocycles. It is named a fixed-degree rational-map compactification, not an all-strata quadratic-pencil compactification.

**v170 amendment.** The new global result is the normalized marked root-cover model with proved overlaps and conductor gluing. It is not named a compactification of all pencil strata.

### 52. Boundary complex

**Retained v169 response.**

For the marked problem the computed dual complex is the path with vertices E_1,...,E_a and it is transported with the marked ideal system. A coordinate-free boundary complex for every contact and Kronecker stratum is not inferred from this path.

**v170 amendment.** The new marked boundary complex is the path on D_1,...,D_a with explicit multiplicities, cyclic cone indices, and root maps. Its compatibility under marked units and root covers is proved. No canonical complex for all unmarked Kronecker strata is inferred.

### 53. Complete-quadric comparison

**Retained v169 response.**

The final subsection of `sec:equivariant-v169` explains the strict pullback along a specified coefficient map and the retained fixed-target complete-quadric comparison. It does not identify all complete-quadric Hilbert components with the plane-target rational-map graph.

**v170 amendment.** The inherited fixed-target complete-quadric comparison remains a specified-family application. The toric root cover acts on coefficients and normalizes parameters, not a different complete-quadric target.

### 54. Equivariance

**Retained v169 response.**

Theorem `thm:global-gluing-v169` proves PGL_2 x PGL_3 equivariance of the graph, its universal curve, its pivot gluing, and its normalization. Equation `eq:undo-global-v169` gives the explicit parameter-dependent target undo matrices.

**v170 amendment.** The v169 full-degree equivariance is retained. The additional marked logarithmic construction is invariant under changes of boundary trivializations and admits associative root-cover maps; its smaller symmetry category is stated.

### 55. Effective-family limitation

**Retained v169 response.**

Both papers continue to reconstruct a specified effective family before applying the boundary construction. The new main chain and genus-correction theorems themselves are independent of this application and of Paper I.

**v170 amendment.** The new boundary theorem and `cor:toric-fibres-v170` do not use Paper I. The effective failure-family application still uses reconstruction first, with its original hypotheses.

### 56. No isolated-algebra boundary operator

**Retained v169 response.**

No preferred specialization direction is extracted from an isolated unframed finite multiplication table. This is stated in both introductions and in the final application subsection.

**v170 amendment.** No internal operator on an isolated finite algebra has been added or claimed. Root exponents and arc residues are data of the specified coefficient family.

### 57. External independent Paper I audit

**Retained v169 response.**

No external independent full proof audit was obtained. The complete prior proof is retained byte-for-byte. Its handoff and dependency information remain available, and neither the new application nor computational checks are counted as that audit.

**v170 amendment.** An external independent full audit has not been obtained. All 465 predecessor mathematical blocks are preserved; the new checks and proof-dependency map are not substituted for that audit.

### 58. Ballico comparison

**Retained v169 response.**

The historical framing permanently makes no priority claim requiring an unperformed full-text comparison with Ballico 1993. The documentary limitation remains in both papers and in the source-use record; no inaccessible text is represented as read.

**v170 amendment.** The permanent narrowing of historical claims is retained in both papers. The new primary-source record does not claim to have obtained the missing Ballico original text.

### 59. Expanded primary-source comparison

**Retained v169 response.**

The new comparison section uses Speyer--Sturmfels for tropicalization, Manubens--Montes for specialization systems, Marian--Oprea--Pandharipande for actual stability conditions, and Manolache for comparison spaces. The Quot contraction and reduced-image obstruction are proved, rather than inferred from different terminology.

**v170 amendment.** The record now adds theorem-level comparisons with semigroup normalization/monomial blow-ups (Gonzalez Perez--Teissier, Proposition 5 and Section 2.6), toric cover ramification (Alexeev--Pardini, Definition 1 and Lemma 1), and the Stacks blow-up/normalization lemmas. Only consulted sources are described as consulted.

### 60. Classical formalism versus calculations

**Retained v169 response.**

The introduction explicitly credits Hilbert embeddings, Rees graph closure, blow-up universal properties, and toric normalization. The all-order restricted ideal factorization, uniform curve equations, complete local-ring table, and punctual genus-correction algebra are the calculated statements being submitted for scrutiny.

**v170 amendment.** The introduction expressly treats semigroup normalization and the toric-cover lattice rule as classical. The complete parameter-fibre ideal, global conductor through crossings, and Hilbert-root identifications are proved calculations for the stated family, not claimed new representability machinery.

### 61. Publication and preservation

**Retained v169 response.**

The active main text now follows the chain-model theorem through its embedded curves and comparisons. Earlier Paper II main sections are moved intact into appendices, not deleted. The master is explicitly an archive of the two complete bodies, not a third submission or a proof of journal merit.

**v170 amendment.** The full prior mathematical bodies remain in the papers and preservation master; the new front matter is centred on one ramified-boundary theorem. No existing content is deleted, and the master remains an audit object rather than a third submission.

### 62. The active theorem route

**Retained v169 response.**

The main route is row factorization -> normal Rees algebra -> monic universal curve -> local associated-point and genus-correction calculation. Fixed-degree gluing and the Quot application follow. The dependency map separates inherited frameworks and the Paper I application.

**v170 amendment.** The new proof route is chain model -> normalized Rees fan -> divisorial coordinate ideal -> complete parameter fibre; and raw lci charts -> binomial conductor -> depth lemma -> global conductor. Root-lift and logarithmic consequences then follow. `THEOREM_DEPENDENCIES_V170.md` makes both routes explicit.

### 63. Role of finite checks

**Retained v169 response.**

The scripts verify bounded exact instances, full order-three Hilbert kernels, monic bases, punctual module bases, and semigroup inequalities. Their receipts explicitly say they are regression evidence, not general proofs, novelty certificates, or editorial judgments.

**v170 amendment.** The new checks use exact semigroup membership, finite normalization-module representatives, binomial gap counts, lattice indices, intersection identities, and root-cover composition. They are auxiliary finite regressions; the proofs of the general statements are in the manuscript.

### 64. External application

**Retained v169 response.**

Corollary `cor:external-curves-v169` constructs boundary points in the Hilbert closure of smooth rational graphs with unbounded punctual nilpotence order. Proposition `prop:quot-contraction-v169` gives an independent comparison with fixed-source Quot limits. Neither uses the finite failure-algebra pipeline; no assertion about solving a previously recognized named open problem is made.

**v170 amendment.** Corollary `cor:toric-fibres-v170` gives the entire origin fibre of any normal toric surface modification of A2, with no reconstruction input. The new result is not advertised as solving a recognized named open problem.

### 65. Why two papers

**Retained v169 response.**

Paper I establishes the reconstruction theorem. Paper II establishes geometric boundary theorems without using it, then applies them to reconstructed effective families. These are separate logical publication units, not an indivisible package whose combined length establishes importance.

**v170 amendment.** Paper I proves reconstruction. The new main boundary theorem is independent of it and belongs to Paper II; the final effective-family interpretation is the only link requiring the inverse. The master preserves both, not a claimed indivisible top-four theorem.

### 66. What warrants a new evaluation

**Retained v169 response.**

This revision is not based only on another small-order check: it proves an arbitrary-order factorization and normal Rees algebra, uniform universal-curve equations, all marked-family arc limits, and an exact nilpotent genus law. It also supplies actual fixed-degree equivariant gluing and a Quot contraction. Their significance and remaining full-fibre limitations are for the next referee to assess; no top-four acceptance claim is made.

**v170 amendment.** The advance relative to full v169 is the all-order ramified normalization, complete parameter fibre, conductor across every crossing, and all lost root labels with compatible root-cover maps. It is not merely another order-three chart or a larger test count. Its significance remains for mathematical referees to evaluate; no acceptance claim is made.

