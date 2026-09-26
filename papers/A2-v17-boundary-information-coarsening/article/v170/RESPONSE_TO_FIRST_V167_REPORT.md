# A2 v170 response to the first independent v167 report

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

### 1. General graph-from-Pluecker lemma

**Retained v169 response.**

Proposition `prop:content-v169` isolates the graph/Rees construction and credits its classical nature. The all-order marked-family factorization is proved separately in `thm:chain-model-v169`.

**v170 amendment.** The retained response continues to apply. No additional mathematical closure of this request is asserted by the ramified-boundary theorem.

### 2. Gotzmann representation

**Retained v169 response.**

Equation `eq:gotzmann-size-v169` and its preceding calculation give the complete sum of linear and constant binomial terms and the resulting number of terms.

**v170 amendment.** The retained response continues to apply. No additional mathematical closure of this request is asserted by the ramified-boundary theorem.

### 3. Segre section surjectivity

**Retained v169 response.**

Section `sec:content-v169` explains that every bidegree-(m,m) monomial is a product of Segre coordinates. This is the concrete projective-normality input needed for the smaller section space.

**v170 amendment.** The retained response continues to apply. No additional mathematical closure of this request is asserted by the ramified-boundary theorem.

### 4. Matrix dimensions

**Retained v169 response.**

The quotient map `eq:eval-covariant-v169` is followed immediately by q=(a+1)m+1 and N=(m+1) binom(m+2,2), and the matrix is explicitly q by N.

**v170 amendment.** The retained response continues to apply. No additional mathematical closure of this request is asserted by the ramified-boundary theorem.

### 5. Matrix convention

**Retained v169 response.**

Rows are coefficients in the output section basis and columns are images of input basis vectors. This quotient convention is fixed before the Fitting and valuation discussion.

**v170 amendment.** The retained response continues to apply. No additional mathematical closure of this request is asserted by the ramified-boundary theorem.

### 6. Rank and base-point-freeness

**Retained v169 response.**

Proposition `prop:incidence-content-v169` gives the named rank criterion, including the argument from a common factor and the degree-m Hilbert restriction surjectivity.

**v170 amendment.** The retained response continues to apply. No additional mathematical closure of this request is asserted by the ramified-boundary theorem.

### 7. Fixed Segre kernel

**Retained v169 response.**

Section `sec:content-v169` states that every curve ideal contains the fixed kernel of restriction from the projective ambient space to the Segre variety. This explains the Hilbert Grassmannian factorization.

**v170 amendment.** The retained response continues to apply. No additional mathematical closure of this request is asserted by the ramified-boundary theorem.

### 8. Generation of the ideal sheaf

**Retained v169 response.**

The same discussion uses the truncation consequence of m-regularity: the degree-m kernel generates the ideal sheaf. It does not claim absence of smaller-degree generators.

**v170 amendment.** The retained response continues to apply. No additional mathematical closure of this request is asserted by the ramified-boundary theorem.

### 9. Graph versus normalization

**Retained v169 response.**

Proposition `prop:degree-change-v169` and the specialization discussion explicitly distinguish them. The marked model T_a happens to be smooth; no such property is imposed on the full Gamma_a.

**v170 amendment.** This is a substantive change relative to v169: `cor:hilbert-lifts-v170` exhibits g_i different normalization points with identical retained coefficients and identical embedded Hilbert limit. Every root label is realized by an arc; at torus-fixed boundary points the lift is unique.

### 10. Natural Fitting description

**Retained v169 response.**

The evaluation map is coordinate-free in `eq:eval-covariant-v169`; its cokernel gives Fitt_0. The smaller companion-matrix basepoint module is displayed in `eq:basepoint-fitt-v169` and is not confused with the Hilbert graph ideal.

**v170 amendment.** The retained response continues to apply. No additional mathematical closure of this request is asserted by the ramified-boundary theorem.

### 11. Radical, integral closure, and Rees valuations

**Retained v169 response.**

The full-chart radical and absence of divisorial content are proved in `prop:incidence-content-v169`. On S_a, `prop:rees-v169` computes the integral closure, every power, the normal Rees algebra, and all exceptional valuations. A full-B_a integral-closure formula is not claimed.

**v170 amendment.** Proposition `prop:ramified-rees-v170` computes the integral closure in every Rees degree after every diagonal coefficient cover, including unequal powers. The raw algebra need not be normal; it is not silently equated with its integral closure. A full-B_a closure formula remains outside this theorem.

### 12. Smaller presentation

**Retained v169 response.**

The arbitrary-order marked family now has a factorization by `a` two-generated ideals and universal-curve equations with at most a+1 generators per chart. This is proved uniformly, not inferred from finite computations. The full B_a presentation remains potentially large.

**v170 amendment.** The new normalization is specified by a two-dimensional fan and the finite inequalities in `eq:ramified-rees-v170`, rather than a larger matrix. The conductor is a divisorial ideal with explicit orders; all crossing conditions are settled by `lem:conductor-depth-v170`.

### 13. Asymptotic size

**Retained v169 response.**

Section `sec:content-v169` gives m, q, N asymptotics and log binom(N,q). The bound counts potential minors and does not say all of them are nonzero.

**v170 amendment.** The retained response continues to apply. No additional mathematical closure of this request is asserted by the ramified-boundary theorem.

### 14. Computability versus practicality

**Retained v169 response.**

The manuscript distinguishes finite presentation and algorithmic termination from practical complexity. The new marked-family formula avoids the large matrix, but does not advertise efficient full-B_a enumeration.

**v170 amendment.** The retained response continues to apply. No additional mathematical closure of this request is asserted by the ramified-boundary theorem.

### 15. Posterior bound

**Retained v169 response.**

Proposition `prop:primitive-jet-v169` labels the content-free minor bound posterior and sufficient. The separate theorem `thm:sharp-jet-v169` proves an optimal family bound in the concise marked contact invariant ord(b).

**v170 amendment.** The retained response continues to apply. No additional mathematical closure of this request is asserted by the ramified-boundary theorem.

### 16. Concise contact invariant

**Retained v169 response.**

On S_a, ord(b) is the intersection order with the marked basepoint divisor and gives the bound ord(b)+1 for every a. This is stronger than simply evaluating the raw determinantal order and does not depend on the Hilbert degree.

**v170 amendment.** The distinction is maintained. None of the new conductor, normality, parameter-fibre, or root-label formulas uses the raw minor order.

### 17. Coefficient jets versus formal families

**Retained v169 response.**

The finite-jet statements determine the embedded closed Hilbert point only. They do not identify the entire DVR family, its higher jets, or arbitrary normalization lifts.

**v170 amendment.** The retained response continues to apply. No additional mathematical closure of this request is asserted by the ramified-boundary theorem.

### 18. Ramified base change

**Retained v169 response.**

The discussion of `eq:raw-order-v169` states that ideal orders and Smith lengths scale with ramification while the closed embedded limit does not. This is one reason not to regard those lengths as invariants of the graph point.

**v170 amendment.** Successive monomial root maps are now treated geometrically: normalizing the iterated pullback canonically gives Z_(a,rho r,sigma s), with associative comparison maps. The marked-unit gluing is proved in `prop:log-compatibility-v170`.

### 19. Residue-field descent

**Retained v169 response.**

The equations and primitive-coordinate criterion are defined over the residue field. Equality means proportionality over that field; extension to an algebraic closure is a separate operation. The geometric component descriptions are stated over algebraically closed characteristic-zero k.

**v170 amendment.** The theorem is stated over an algebraically closed field of characteristic zero. The geometric root counts use that hypothesis; residue-field extensions at generic boundary points are explicitly computed, not silently replaced by k.

### 20. Polynomial-arc algorithm

**Retained v169 response.**

After `prop:primitive-jet-v169` the coefficient ring and finite exact procedure are specified: polynomial/localized-polynomial input over k, rational-function linear algebra and polynomial division. Formal-series oracles are not assigned a finite a priori query budget.

**v170 amendment.** The retained response continues to apply. No additional mathematical closure of this request is asserted by the ramified-boundary theorem.

### 21. Uniform versus pointwise determination

**Retained v169 response.**

The inherited no-uniform result and the new sufficient posterior bound remain compatible. The new theorem is uniformly optimal only after fixing ord(b) on S_a; it is not a uniform jet length over all arcs.

**v170 amendment.** The retained response continues to apply. No additional mathematical closure of this request is asserted by the ramified-boundary theorem.

### 22. Positive weights and centres

**Retained v169 response.**

Proposition `prop:fan-comparison-v169` identifies positive weights as arcs about the specified centre. It also treats nonnegative weights and translated coefficient polynomials without calling the original fan a decomposition around every point.

**v170 amendment.** The retained response continues to apply. No additional mathematical closure of this request is asserted by the ramified-boundary theorem.

### 23. Valuation-zero coordinates

**Retained v169 response.**

The same proposition allows prescribed units and weight zero and proves the finite weight-layer argument in that setting.

**v170 amendment.** The retained response continues to apply. No additional mathematical closure of this request is asserted by the ramified-boundary theorem.

### 24. Identically zero coordinates

**Retained v169 response.**

Zero coordinate patterns remain a separate finite choice. They are not identified with large positive valuation. The all-order arc theorem also treats c identically zero directly.

**v170 amendment.** The retained response continues to apply. No additional mathematical closure of this request is asserted by the ramified-boundary theorem.

### 25. Universal finite-polynomial lemma

**Retained v169 response.**

Proposition `prop:fan-comparison-v169` formulates the finite-support weight-layer construction for an arbitrary finite list of polynomial projective coordinates. The actual Hilbert contribution then comes from the evaluation kernel or the explicit marked-family equations.

**v170 amendment.** The retained response continues to apply. No additional mathematical closure of this request is asserted by the ramified-boundary theorem.

### 26. Groebner and tropical comparison

**Retained v169 response.**

Section `sec:equivariant-v169` compares the general support arrangement with tropical Pluecker data and classical state fans. It proves minimality only for the marked-family Newton fan, not for every syntactic hyperplane arrangement.

**v170 amendment.** The retained response continues to apply. No additional mathematical closure of this request is asserted by the ramified-boundary theorem.

### 27. Valuated matroids

**Retained v169 response.**

Actual maximal minors satisfy the Pluecker relations and yield realizable valuated-matroid data. Their valuations discard residues, as the first-wall example shows. The manuscript does not confuse tropical quadratic prevarieties with full realizability.

**v170 amendment.** The retained response continues to apply. No additional mathematical closure of this request is asserted by the ramified-boundary theorem.

### 28. Residue effects

**Retained v169 response.**

The first-wall family gives curves with identical valuation data and varying embedded ideals. For cancellation itself the general finite-support proof retains every coefficient sum; no claim that cancellation is absent on B_a is made. The marked S_a minors are monomials and thus have no internal cancellation.

**v170 amendment.** This is a substantive change relative to v169: `cor:hilbert-lifts-v170` exhibits g_i different normalization points with identical retained coefficients and identical embedded Hilbert limit. Every root label is realized by an arc; at torus-fixed boundary points the lift is unique.

### 29. Recovering the ideal without full elimination

**Retained v169 response.**

Proposition `prop:curve-charts-v169` supplies uniform monic equations and standard monomials for the complete marked family. In the general coefficient construction the degree-m kernel still determines the sheaf, but is not relabelled a small algorithm.

**v170 amendment.** The universal curve on Z is the flat pullback of the same low-degree monic family. Parameter normalization does not normalize its embedded curve fibres; their original ideals and punctual modules remain in the manuscript.

### 30. Complexity in the front matter

**Retained v169 response.**

The abstract now centres the all-order small-presentation theorem rather than calling the enormous full coefficient matrix efficiently computable. The explicit size and non-efficiency statements remain in the main text.

**v170 amendment.** The retained response continues to apply. No additional mathematical closure of this request is asserted by the ramified-boundary theorem.

### 31. Canonicity of the arrangement

**Retained v169 response.**

The general support arrangement is explicitly presentation-dependent. The marked family has an actual minimal Newton fan because its normal Rees algebra is computed; this is the limited but precise canonicity being used.

**v170 amendment.** Every bend ray is required for simultaneous principalization, and the inherited wall curves identify the corresponding Hilbert degeneration. No redundant hyperplane refinement is inserted. See `prop:log-compatibility-v170`.

### 32. Contact chart changes

**Retained v169 response.**

Theorem `thm:global-gluing-v169` gives the source/target chart cocycles for the fixed-degree graph. Proposition `prop:fan-comparison-v169` separately explains why this does not force the coefficient fans to agree.

**v170 amendment.** Proposition `prop:log-compatibility-v170` adds coherent root-cover comparison and gluing under units on two marked Cartier boundaries. It does not assert that arbitrary unmarked coordinate changes preserve this fan; the larger fixed-degree equivariance remains the separate v169 theorem.

### 33. Redundant residue strata

**Retained v169 response.**

Different pieces of a finite-support partition may yield the same projective point. The general partition is retained as a finite computable refinement, not a minimal moduli decomposition. On T_a the wall and chamber description is minimal and identifies every point.

**v170 amendment.** Theorem `thm:ramified-boundary-v170` gives all a components, generic lengths, node adjacencies of the reduced fibre, and no embedded associated points after arbitrary ramification. The open residue strata are G_m with finite power maps of degree g_i; their endpoints and lifts are explicit.

### 34. Finite families, not finite types

**Retained v169 response.**

Both the general coefficient result and the marked-family arc theorem state that wall residues vary in algebraic families. No finite list of abstract isomorphism classes is deduced from a finite combinatorial partition.

**v170 amendment.** The wall strata remain algebraic G_m families. Root covers now have a precise finite power-map identification on each family; this is not a finite classification of all automorphism types.

### 35. Row-ideal factorization

**Retained v169 response.**

The proof of `eq:all-order-factor-v169` gives each row ideal separately in `eq:row-factor-v169`, then counts its factors. The a=2 formula is one specialization of this uniform argument.

**v170 amendment.** The retained response continues to apply. No additional mathematical closure of this request is asserted by the ramified-boundary theorem.

### 36. Powered-product blow-ups

**Retained v169 response.**

The proof of `thm:chain-model-v169` states the integral-test nonzero-ideal criterion that a positive-power product is invertible exactly when the individual fractional ideals are invertible. The normal fan gives an additional explicit verification on S_a.

**v170 amendment.** Proposition `prop:log-compatibility-v170` proves the terminal normal principalization property for the marked ideal system and compatible root covers. It extends to two specified transverse Cartier divisors; it is not an unmarked all-pencil modular universal property.

### 37. Irrelevant saturation

**Retained v169 response.**

Proposition `prop:curve-charts-v169` specifies both source charts and the target-graded ideal sheaves. It states when the first-chart extra generator is needed and identifies the source-infinity ideal. The special table refers to this exact gluing, not reduced-support homogenization.

**v170 amendment.** The retained response continues to apply. No additional mathematical closure of this request is asserted by the ramified-boundary theorem.

### 38. Affine primary decompositions

**Retained v169 response.**

Theorem `thm:punctual-v169` gives ordinary affine ideals and a primary decomposition for O_i, pure wall quotients, and exact punctual modules. Proposition `prop:terminal-v169` covers the remaining target chart and all terminal associated points.

**v170 amendment.** The parameter-fibre nilradical now has exact order max_i min(rho,i sigma)/g_i and no embedded associated points (`lem:coordinate-ideal-v170`). The separate punctual nilradical of the embedded universal curves remains as computed in v169. These two statements concern different rings.

### 39. Infinity checks

**Retained v169 response.**

Equation `eq:source-infinity-v169` is proved on every parameter chart in one proposition. It reduces the entire family there to G=b y^a F and R=c y F, excluding a hidden component at infinity.

**v170 amendment.** The retained response continues to apply. No additional mathematical closure of this request is asserted by the ramified-boundary theorem.

### 40. Exceptional rays

**Retained v169 response.**

The normal Rees algebra determines rays (i,1), in their order between the coordinate axes. They are matched to E_i, the wall p=i q, and the adjacent chamber endpoints.

**v170 amendment.** For all a,rho,sigma, the primitive Rees valuations are (i sigma/g_i,rho/g_i), with g_i=gcd(rho,i sigma). Their ramification indices and residue degrees are respectively rho sigma/g_i and g_i. See `prop:ramified-rees-v170` and `eq:root-residue-v170`.

### 41. Wall residues

**Retained v169 response.**

Theorem `thm:arc-table-v169` derives kappa and lambda from the regular exceptional-chart coordinates. They are exactly the nonzero coordinate on E_j minus its two endpoints, hence the actual embedded wall parameter.

**v170 amendment.** This is a substantive change relative to v169: `cor:hilbert-lifts-v170` exhibits g_i different normalization points with identical retained coefficients and identical embedded Hilbert limit. Every root label is realized by an arc; at torus-fixed boundary points the lift is unique.

### 42. Normalization of the restricted blow-up

**Retained v169 response.**

The primitive Rees algebra itself is normal and all adjacent fan cones are unimodular. The graph is already the computed smooth surface; an extra normalization is not silently inserted.

**v170 amendment.** Equation `eq:ramified-rees-v170` and chart formula `eq:normal-chart-v170` explicitly compute the normalized algebra and all overlaps for arbitrary covers. Unlike the unramified case, normality is not asserted for the raw Rees algebra.

### 43. Intersection matrix and nef cone

**Retained v169 response.**

Proposition `prop:boundary-v169` gives them for every a, together with Picard generators, axis divisor classes, discrepancies, and intermediate toric contractions.

**v170 amendment.** Proposition `prop:ramified-singularities-v170` adds all cyclic chart class groups, axis divisors, rational intersection numbers, and relative canonical coefficients. These are Weil/Q-Cartier statements where appropriate, not an unsupported Cartier Picard assertion on a singular surface.

### 44. Scope of the order-two slice

**Retained v169 response.**

The old two-wall theorem remains a marked slice theorem. The new all-order theorem and equivariant extensions are stated just as precisely; neither is called a classification of all six-coefficient order-two arcs.

**v170 amendment.** The new complete fibre theorem is for every ramified marked family and includes a=3. It does not compute the entire full-B_3 fibre. That distinction remains explicit in the theorem, abstract, and review entry, rather than being counted as closure of this broader request.

### 45. A genuinely higher-contact model

**Retained v169 response.**

The a=3 instance has three blow-ups, seven exact curve families, and length-one embedded points in its last three cases. Theorem `thm:genus-correction-v169` explains the arbitrary-order law behind those points.

**v170 amendment.** The order-three unequal-cover example is completely specified by the general theorem. Its conductor is (2,3,8), fibre lengths (2,1,2), and residue degrees (1,2,1); see `ex:third-ramified-v170`.

### 46. Strict versus ordinary base change

**Retained v169 response.**

T_a is defined as the closure of the generic slice graph, not the whole fibre product with Gamma_a. The full fixed-degree gluing uses actual isomorphisms and flat products, with the inherited strict-base-change results unchanged.

**v170 amendment.** The coefficient map b=u^rho,c=v^sigma is finite flat. Thus the full base change Y is already the Hilbert graph; no vertical component is removed. Its normalization Z is a separate finite operation with explicitly computed conductor.

### 47. Dense-open hypotheses

**Retained v169 response.**

The definitions of T_a, Gamma_a and the global graph specify their generic basepoint-free open. The final comparison subsection retains the fixed generic embedded quotient required for horizontal comparison.

**v170 amendment.** Proposition `prop:log-compatibility-v170` proves the terminal normal principalization property for the marked ideal system and compatible root covers. It extends to two specified transverse Cartier divisors; it is not an unmarked all-pencil modular universal property.

### 48. Common refinement is not a minimal model

**Retained v169 response.**

The earlier common-refinement category is not renamed a canonical terminal compactification. The new chain has its own proved marked-ideal universal property, and the fixed-degree global graph has its own explicit definition.

**v170 amendment.** Proposition `prop:log-compatibility-v170` proves the terminal normal principalization property for the marked ideal system and compatible root covers. It extends to two specified transverse Cartier divisors; it is not an unmarked all-pencil modular universal property.

### 49. Finite-type inverse limit of refinements

**Retained v169 response.**

No finite-type inverse limit or universal minimal object for all modifications is claimed. The new global gluing theorem is a separate fixed-degree construction with an explicit atlas, not an assertion about that inverse limit.

**v170 amendment.** No finite-type inverse limit of all possible refinements is asserted. The theorem gives a terminal normalized principalization for one finite marked ideal system and associative comparisons for its specified root covers.

### 50. Geometric consequence of nilpotents

**Retained v169 response.**

The new genus-correction theorem makes the punctual algebra necessary for flatness and separates it from the associated cycle and stable-map image. This is a consequence of the newly computed higher-order algebra; it does not purport to derive every deformation obstruction from the earlier first-contact square-zero class.

**v170 amendment.** The parameter-fibre nilradical now has exact order max_i min(rho,i sigma)/g_i and no embedded associated points (`lem:coordinate-ideal-v170`). The separate punctual nilradical of the embedded universal curves remains as computed in v169. These two statements concern different rings.

### 51. Obstruction line versus nilradical line

**Retained v169 response.**

The inherited local extension calculation and its precise distinction between the local obstruction sheaf, nilradical module, and global hyper-Ext are retained. The higher-order punctual ideals are written as actual multiplication ideals, not confused with that obstruction line.

**v170 amendment.** The inherited local Ext/nilradical distinction remains. The new conductor ideal and parameter-fibre nilradical are also kept separate from the square-zero obstruction sheaf and the embedded-curve genus-correction module.

### 52. Uniform toric conventions

**Retained v169 response.**

The inherited ramified cyclic-quotient calculation is retained. For the new chain, rays, lattice determinants, and contraction types are stated directly, with A_(j-i-1) meaning uv=w^(j-i). No unexplained cyclic-action convention is used.

**v170 amendment.** Proposition `prop:ramified-singularities-v170` adds all cyclic chart class groups, axis divisors, rational intersection numbers, and relative canonical coefficients. These are Weil/Q-Cartier statements where appropriate, not an unsupported Cartier Picard assertion on a singular surface.

### 53. Boundary divisor classes

**Retained v169 response.**

The new all-order boundary computation states div(b), div(c), Picard generators, and relative canonical coefficients in one convention. It does not identify these chain classes with the different ramified invariant-chart class group.

**v170 amendment.** Proposition `prop:ramified-singularities-v170` adds all cyclic chart class groups, axis divisors, rational intersection numbers, and relative canonical coefficients. These are Weil/Q-Cartier statements where appropriate, not an unsupported Cartier Picard assertion on a singular surface.

### 54. Parameter normalization versus stable curves

**Retained v169 response.**

The parameter surface normalization is kept distinct from normalization of curve reductions and from stable-map or stable-quotient moduli. The explicit Quot comparison verifies stability after three markings rather than using semistable terminology informally.

**v170 amendment.** The universal curve on Z is the flat pullback of the same low-degree monic family. Parameter normalization does not normalize its embedded curve fibres; their original ideals and punctual modules remain in the manuscript.

### 55. Main theorem and inherited architecture

**Retained v169 response.**

The new active Paper II main text is organized around one all-order chain and genus-correction theorem. The previous active sections move intact to appendices, preserving all mathematical content and labels.

**v170 amendment.** The new proof route is chain model -> normalized Rees fan -> divisorial coordinate ideal -> complete parameter fibre; and raw lci charts -> binomial conductor -> depth lemma -> global conductor. Root-lift and logarithmic consequences then follow. `THEOREM_DEPENDENCIES_V170.md` makes both routes explicit.

### 56. Role of the preservation master

**Retained v169 response.**

The master is expressly not a third submission and is not cited as evidence of mathematical significance. It is a complete preservation and cross-reference object for the two logical paper units.

**v170 amendment.** The full prior mathematical bodies remain in the papers and preservation master; the new front matter is centred on one ramified-boundary theorem. No existing content is deleted, and the master remains an audit object rather than a third submission.

### 57. Theorem-level tropical and Groebner comparison

**Retained v169 response.**

The comparison section distinguishes realizable minor valuations, residual Hilbert points, parameter-specialization bases, and the minimal computed Newton fan. It cites primary sources and proves the marked-family comparison rather than claiming novelty from vocabulary.

**v170 amendment.** The record now adds theorem-level comparisons with semigroup normalization/monomial blow-ups (Gonzalez Perez--Teissier, Proposition 5 and Section 2.6), toric cover ramification (Alexeev--Pardini, Definition 1 and Lemma 1), and the Stacks blow-up/normalization lemmas. Only consulted sources are described as consulted.

### 58. Hilbert and Quot comparison

**Retained v169 response.**

Proposition `prop:quot-contraction-v169` gives an actual contraction morphism, central quotient, and stable-marked interpretation. Corollary `cor:external-curves-v169` identifies the exact punctual structure forgotten by cycle or reduced-image descriptions.

**v170 amendment.** The same universal curve is pulled back, so the earlier Quot and cycle comparisons remain valid. Distinct normalization root labels above one Hilbert point are an additional loss of parameter information, separate from loss of a punctual curve nilradical.

### 59. Higher-contact scope in the abstract

**Retained v169 response.**

The abstract explicitly says that the complete curve classification concerns the marked family rather than every fibre over the full coefficient space. The full-B_3 and higher-corank classifications are not represented as completed.

**v170 amendment.** The new complete fibre theorem is for every ramified marked family and includes a=3. It does not compute the entire full-B_3 fibre. That distinction remains explicit in the theorem, abstract, and review entry, rather than being counted as closure of this broader request.

### 60. Graph theorem versus fibre theorem

**Retained v169 response.**

The all-B_a determinantal graph remains distinct from the complete fibre theorem for T_a. The manuscript gives both objects and their different dimensions and base-change definitions explicitly.

**v170 amendment.** For the ramified marked parameter fibre, the exact answer is a one-dimensional components, all P1 after reduction, with chain incidences and lengths min(rho,i sigma)/g_i. This is proved scheme-theoretically, not asserted as the component list of the full B_3 fibre.

### 61. External audit of Paper I

**Retained v169 response.**

No external independent full audit was obtained. The inverse proof is retained unchanged and its role is limited to the later effective-family application. Its computational and provenance checks are not counted as an audit.

**v170 amendment.** An external independent full audit has not been obtained. All 465 predecessor mathematical blocks are preserved; the new checks and proof-dependency map are not substituted for that audit.

### 62. Historical framing

**Retained v169 response.**

No priority claim requiring a full Ballico 1993 comparison is made. The incomplete documentary access remains disclosed in both papers and the literature record.

**v170 amendment.** The permanent narrowing of historical claims is retained in both papers. The new primary-source record does not claim to have obtained the missing Ballico original text.

### 63. Finite checks versus proof

**Retained v169 response.**

The finite exact suite is auxiliary. The all-order factorization, flatness, local-ring, and gluing statements are supported by written arguments with explicit hypotheses, not by the number of tested values.

**v170 amendment.** The new checks use exact semigroup membership, finite normalization-module representatives, binomial gap counts, lattice indices, intersection identities, and root-cover composition. They are auxiliary finite regressions; the proofs of the general statements are in the manuscript.

### 64. Responses versus mathematical closure

**Retained v169 response.**

The two numbered response documents are navigation and accountability tools. They explicitly identify incomplete requests and are not used as a count of discharged mathematical obligations.

**v170 amendment.** The replies explicitly separate new v170 results, retained v169 results, and requests not completed. The count of 66 replies is not a claim of mathematical closure of every request.

### 65. One publication-level theorem

**Retained v169 response.**

The main route is the arbitrary-order chain model and its punctual genus-correction law, with sharp family jets and concrete comparisons as consequences. The earlier programme is preserved in appendices and the separate master.

**v170 amendment.** The advance relative to full v169 is the all-order ramified normalization, complete parameter fibre, conductor across every crossing, and all lost root labels with compatible root-cover maps. It is not merely another order-three chart or a larger test count. Its significance remains for mathematical referees to evaluate; no acceptance claim is made.

### 66. Publication target and complete content

**Retained v169 response.**

The mathematical target has not been changed to avoid the report. The active exposition is reorganized around the new central theorem, while all historical proofs remain available in the complete paper appendices and preservation master. No acceptance prediction or editorial reversal is claimed.

**v170 amendment.** The requested top-four mathematical standard is addressed through explicit hypotheses, complete proofs, a central theorem, and precise publication units. No arbitrary deletion, substitute editorial downgrading, or claim of guaranteed journal acceptance is made.

