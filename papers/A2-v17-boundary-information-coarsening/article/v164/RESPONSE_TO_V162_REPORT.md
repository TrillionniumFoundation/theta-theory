# A2 revision 164 — response to the complete v162 referee report

## Controlling objects

The latest complete report found on the remote review branches is `reviews/a2-v162-independent-harsh-top4-2026-09-25/REFEREE_REPORT.md` at `7e9c057907cc4502858a54f32ab0c0cfa264680f`. Its reviewed manuscript is v162, final tip `299a77c6f77c4d5aec6e5737e1b1ba471ce5b7c8`. The subsequent complete v163 revision at `40a72ddfd85e16363385a1b64b922d61055e875c` is a post-report mathematical input, not a newer referee report. Revision 164 preserves that manuscript and its derivations on a new branch, `revision/a2-v164-collision-wall-crossing-2026-09-26`. No older review or revision branch is overwritten.

The report's main demands are a transparent fixed-target embedded comparison and a structural description of complete nonreduced fibres, their adjacency, and their behaviour when supports move. Revision 163 supplied a separate embedded comparison, the whole first nonreduced scheme fibre, and products at distinct supports. The present revision retains those results and computes a collision family. The earlier point-by-point v163 response is archived alongside this response so that an inherited answer is not passed off as a new v164 theorem.

## The substantive addition

For the retained-coefficient graph over triples `(f,g,r)`, consider the coefficient curve `(x^2-delta,0,0)`. Write H for the entire pullback of the normalization of the total reduced Hilbert graph, and Y for the schematic closure of H over `delta != 0`, taken after base change. The new theorem distinguishes these objects and identifies both.

Theorem `thm:collision-family-v164` gives the projective model

`Y = Bl_(Delta x {0})(P^1 x P^1 x A^1_t) / ((l_+,l_-,t) ~ (l_-,l_+,-t)), delta=t^2`.

The invariant charts are polynomial rings, so Y is smooth. It is flat and its central divisor is `E+2S`, with `E=F_2` and `S=P^2=Sym^2(P^1)`. They meet along the doubled-line curve: a conic in S and the negative section in E. The full pullback has, in addition, the vertical component `Q_P=P^4` of all conics through the attaching point. Scheme-theoretically it is the union `H=Y union_S Q_P`. Its exact base-torsion is `i_* I_(S/Q_P)`, killed by delta and equal to `Tor_1^(C[delta])(O_H,C)`.

Theorem `thm:ordered-resolution-v164` identifies the normalization after `delta=t^2` with the ordered blow-up. Its central parameter space is reduced with normal crossings; the ruling monodromy is the transposition. This is a statement about a family of parameter spaces, not a replacement of thick embedded Hilbert curves by reduced stable-map curves.

Theorem `thm:nilradical-sheaf-v164` determines the global nilpotent module of the entire first-contact fibre: `N_(X_2)=j_* O_(P^2)(-1)`, with square zero. The twist is proved from the collision divisor; the local generator alone would not determine it. The coherent cohomology of O_(X_2), and of all the already classified products, is also computed. The algebra extension is not claimed to split. Corollary `cor:multiple-collisions-v164` determines the horizontal product multiplicities `2^|J|` for independent collisions and distinguishes these pure-dimensional horizontal fibres from the full non-equidimensional pullbacks.

Proposition `prop:genuine-collision-v164` realizes this model by a genuine 4-by-4 symmetric pencil, with fixed complete-quadric target and nonsingular infinity. Its polynomial congruence is applied only on the relative incidence target and is undone. The embedded quotient is annihilated by the finite support polynomial, which makes the realization algebraic rather than an unproved algebraization of a formal gauge. The effective failure-family transfer remains explicitly through the sharp inverse.

These results answer the request for a moving-support adjacency calculation without claiming a complete compactification for higher corank or every contact length. In particular, the horizontal limit reaches only singular-at-the-attachment conics, not every conic of the full central fibre. This explains precisely why the complete fibre has a vertical excess.

## Responses to the 44 specific requests

### 1. Coefficient topology

The preserved `prop:embedded-functors-v163` works over `T[[x_i]]` for Artin T. Its induction is in the maximal ideal of the coefficient base; bounded degrees in x specify remainder representatives. The complete base is the inverse limit of those Artin constructions. In the new collision calculation all displayed coefficient and Hilbert-chart equations are polynomial; the quotient model is constructed algebraically and does not add a convergence assumption.

### 2. Coordinate-free tangent map

The preserved `lem:framed-tangent-v163` defines the Schur derivative as `dot A -> [j^* dot A j]` in the residual congruence quotient before choosing Jordan coordinates. The new explicit pencil has a polynomial congruence whose equality is displayed in `prop:genuine-collision-v164`; its role is realization, not replacement of that coordinate-free tangent argument.

### 3. Orthogonal stabilizer

The same retained lemma isolates the skew-adjoint centralizer. An unordered pair of primary cyclic blocks contributes `min(d_i,d_j)`, the opposite block is its negative adjoint, a single cyclic block contributes no skew-adjoint polynomial, and distinct primary eigenvalues contribute zero. The full statement is retained, not reduced to semisimple pencils.

### 4. Framed and unframed dimensions

The retained tangent sequence has kernel End(R) between Hom(R,M) and Hom(R,M/R). The four pencil-basis directions are kept distinct from source-congruence directions and from parameter-fixed contact directions. The count N remains a framed normal-slice count, not a quotient dimension after every possible group action. In the collision model the root cover orders supports; the involution removes precisely that ordering.

### 5. Formal miniversality

The formal contact theorem remains formal. The algebraic embedded families precede the completed-local comparison. The new quotient construction uses two explicit polynomial invariant charts and their transition; its existence is not deduced from formal miniversality or from a formal completed-ring isomorphism alone.

### 6. Residual stabilizers and embedded objects

Hilbert objects retain their coefficient-base map and are equal only as embedded subschemes in the fixed target. A change of normal-coordinate identification is undone by the inverse identification. The involution in the new ordered collision construction acts on ordering data and on the root parameter; it does not quotient distinct fixed-target Hilbert curves by arbitrary ambient automorphisms.

### 7. Gamma_a as a graph over B_a

The new section begins with `H=tilde Gamma_2 x_(B_2) T` and names its retained coefficient morphism. Both the conic-chart and division-chart inverses use that projection. The horizontal closure is explicitly taken within that pullback. No inverse from an unlabelled Hilbert point alone is asserted.

### 8. Exact sequence of the nonreduced union

The preserved recovery lemma gives the union sequence for the coefficient-recovery line bundle and verifies surjectivity on the full Artin attachment. The new theorem adds the structure-sheaf union sequence `O_H -> O_Y + O_(Q_P) -> O_S`; the identity `(eA,eB)=(e) intersection (A,B)` proves it scheme-theoretically, including the nonflat vertical part.

### 9. Cohomology and base change near all w

The retained recovery lemma treats every central w by a pointwise neighbourhood; the resulting opens cover the central locus. It does not claim one unjustified universal affine shrinking. The new global coherent-cohomology calculation uses exact sequences for the entire proper fibre and the proved nilradical twist. It is distinct from, and does not replace, that local base-change argument.

### 10. Cokernel line and dense vanishing

The coefficient-recovery map remains a split injection with a line-bundle cokernel on an integral reduced graph neighbourhood. Its dense vanishing therefore extends as a section. The new glued quotient charts use those regular inverses; their agreement is proved on integral overlaps using the separated Hilbert target, not inferred only from a bijection on closed points.

### 11. Homogenization degrees

The preserved recovery formula is `WG-s Q_0 F`, with degrees `a-1` and `a-2`, and the recovered third-coordinate section is `s^(a-1)R`. The missing q space at a=1 is explicit. The new collision equations are written on the finite chart of the same homogeneous Hilbert family, whose infinity behaviour is already fixed.

### 12. Infinity

The Hilbert–Burch chart at s=0 forces G=H=0. In the actual pencil realization the infinity blocks are `[[0,t],[t,0]]`, hence nonsingular. Thus neither the polynomial support curve nor its genuine pencil realization creates an unexamined tail at infinity.

### 13. Repeated-root primary structure

The existing gcd strata keep one primary contact algebra for each distinct support; repeated roots are not split by a fictitious Chinese-remainder decomposition. The new collision distinguishes a reduced total pullback, a nonreduced central fibre, and the double component of the horizontal central divisor. The full central primary ideal `(eA,eB,e^2C)` is preserved before taking any radical.

### 14. Jet convention

`J_(a-1)(P^1)` represents maps from Spec C[x]/(x^a). In the new quotient model the central slope is `w=lambda+ux`; u is the first jet coefficient. Its compactification has boundary `e=1/u=0`, precisely the negative section of F_2, rather than an extra derivative order.

### 15. Weil restriction

The retained two-chart proof gives affine a-space on each reduced-direction chart and glues by inversion in the length-a algebra. The new global quotient independently proves the smooth compactification for a=2 and identifies its transition with the jet-coordinate transition. It does not assume a free involution where the exceptional divisor is fixed.

### 16. Hilbert polynomial

The retained homogeneous Hilbert–Burch resolution gives `3l+1` for O(1,1); the complete-quadric pencil has `binom(n,2)l+1` for the product exterior polarization. The genuine four-dimensional collision is checked with degree six and Euler characteristic one. The parameter-space special divisor `E+2S` must not be substituted into this curve Hilbert polynomial.

### 17. Separate embedded comparison

Proposition `prop:embedded-functors-v163` remains a separate theorem about retained-base embedded quotient functors, with equality of subschemes as the morphism convention. The new actual-pencil proposition invokes it at a precise point after constructing the algebraic quotient family. It does not conflate that theorem with a congruence classification of matrix germs.

### 18. Target diagram

The retained diagram distinguishes the universal pencil line, its relative complete-quadric incidence target, the fixed target times the framed base, and the Hilbert graph. The new proposition spells out where its explicit U(x) acts and where it is undone. Its coefficient curve is not treated as a map into a quotient of the fixed target.

### 19. Parameter-dependent congruence

The new polynomial example makes this especially explicit: `U(x)^T L_delta U(x)=diag(x^2-delta,-1)` on the relative incidence target. The finite supported quotient is transformed back before it is patched into the fixed target. Distinct directions at either support remain distinct embedded tails.

### 20. Ideal gluing and completion

The preserved ideal-patching lemma supplies existence of coherent quotient gluing, including torsion; faithful completion is used to detect equations, not manufacture a gluing theorem. The new example has quotient annihilated by f, so its construction is algebraic on the finite locally free support scheme. The completed comparison then verifies the actual inverse on all local rings.

### 21. Formal criterion for etaleness

The existing comparison retains finite presentation, Noetherian excellence and equal residue fields before applying the completed-local criterion. The new global quotient is identified with the horizontal scheme by actual regular chart inverses, so no additional unstated formal-to-etale implication is used.

### 22. Total normalization versus fibre normalization

Every statement distinguishes the normalization of the total reduced graph, its scheme fibre X_2, and normalization after the ramified base change. Theorem `thm:ordered-resolution-v164` proves the last using explicit finite integral extensions in the common fraction field. It never normalizes X_2 and calls the result the original fibre.

### 23. Algebraic one-parameter realizations

The collision coefficient curve and the displayed symmetric pencil are polynomial over A^1. Its ordered model is also algebraic. The formal fixed-target comparison is only a verification tool for that pre-existing family. The locus reached from delta nonzero is the schematic horizontal closure, not the whole pullback by assertion.

### 24. Resultant stratification

The retained `prop:resultant-strata-v163` gives gcd-degree strata and their codimensions. The new calculation concerns a different boundary phenomenon: two nonempty incidence supports collide along the discriminant of f while g=r=0. It computes that specialization exactly and does not call it a new classification of every resultant stratum.

### 25. Closure of the jet component

The existing complete-fibre theorem replaces the earlier dimension-only argument by explicit charts and a proper exhaustion. The new horizontal family gives a moving-support realization of the whole F_2 component, including its negative section. It distinguishes that component from the horizontal singular-conic plane and from the vertical P^4.

### 26. Relative residual construction for conics

The retained Hilbert–Burch family and its regular inverse identify conics scheme-theoretically and in families; their ideal quotient recovers the residual conic rather than merely its support. The new union calculation uses the exact singular-at-P ideal inside that conic P^4, not just the set of singular conics.

### 27. Unparameterized conic uniqueness

The conic parameter remains its homogeneous equation up to scalar. The ordered direction product is quotiented by simultaneous exchange with t -> -t, since a loop interchanges the two labelled supports. No further ambient congruence identifies Hilbert points. At the central singular-conic plane the unordered pair is exactly Sym^2(P^1).

### 28. Finite pullback and dimension

The finite-pullback dimension argument used in v162 is retained in its supplementary proof. The complete v163 theorem already identifies the component as P^4. The new proof does not infer equality of schemes from dimension: its invariant coordinate rings and embedded recovery maps give the isomorphism.

### 29. Dimension of the conic component

It is exactly four in the established full first-contact fibre. The new collision distinguishes the two-dimensional plane S reached horizontally from the additional conics forming a four-dimensional vertical component of H. This explains the jump geometrically and identifies the base-torsion measuring it.

### 30. Intersection and adjacency

The full fibre has reduced intersection D=P^1 between P^4 and F_2. The new horizontal special divisor meets there as `E+2S`, with D a conic in S and a negative section in E. In local coordinates delta=-e^2C, the two reduced branches are e=0 and C=0. The entire moving family, not just one intersection point, is given.

### 31. Doubled-line boundary

The doubled lines form D, the diagonal image in Sym^2(P^1). They arise when the two direction lines coalesce. The blow-up of the ordered diagonal records the first relative direction, and its exceptional divisor is F_2. This explains the doubled-line adjacency without deleting the nonreduced scheme structure.

### 32. Reducedness and nilpotents

The full collision pullback H is reduced, while its central fibre X_2 is not. The horizontal family is smooth with special divisor E+2S. Theorem `thm:nilradical-sheaf-v164` proves the global nilradical `j_*O_(P^2)(-1)`, not only a local nilpotent generator. It also computes coherent cohomology. None of these facts asserts Cohen–Macaulayness of X_2 or splitting of its square-zero extension.

### 33. General contact data

The full static product theorem continues to allow arbitrary larger Smith exponents with smaller exponent one or two. The new independent-collision theorem gives every product multiplicity `2^|J|` and the ordered normal-crossing model for those collisions. It does not claim all contact lengths or passage through higher corank. The genuine-pencil example supplies an actual realization of the balanced first collision.

### 34. Primitive open versus full fibre

The primitive jet locus, its F_2 closure, the conic P^4, the full X_2, and the horizontal fibre E+2S all have separate notation and statements. In particular the new theorem explicitly says that colliding reduced incidences does not reach every conic of X_2. This prevents a flat horizontal model from being advertised as the entire proper fibre.

### 35. Effective-stack restriction

The application in `prop:genuine-collision-v164` is through the established effective inverse with its oriented source. It transfers the actual family, its saturation and its torsion. It does not identify all raw Artin-algebra deformations with pencil deformations and does not assert a boundary operation prior to reconstruction.

### 36. Automorphism extension and linearization

The retained `prop:linearized-envelope-v163` distinguishes the extension from its splitting. The prescribed weight-cancelling PGL(V) linearization supplies that splitting. The collision construction adds no new splitting assertion. Its order-two quotient is proved by explicit invariant charts instead of an assumed free group action.

### 37. Algebraicity of the envelope target

The retained target is the classifying stack of forms of a specified graded bundle and power diagram. Its automorphism group is affine of finite type, defined by the finite multiplication equations, with the explicit linearization. The new family application does not enlarge that statement to all algebra bundles of the same ranks.

### 38. h=1

The exponent-free envelope h=1 remains distinguished. For higher h the graded envelope depends on an auxiliary choice, although its simultaneous graph is unchanged by the universal ideal formula. The new collision classification concerns that graph and therefore does not equate the different graded algebras.

### 39. Broader compactification literature

The preserved comparisons cover stable quotients, parameterized stable quasimaps and Hilbert presentations. This revision additionally examines Chung–Moon's theorem on Mori models for conics in Grassmannians and its explicit Hilbert locus construction. The paper distinguishes a discriminant specialization and horizontal closure from wall crossing of a stability parameter or a Mori program. Our quotient/torsion calculation is not attributed to those different moduli spaces, nor is exhaustive novelty exclusion claimed.

### 40. Ballico 1993

The legitimate publisher bibliography remains available, but the checked PDF route did not provide a readable theorem/proof-level text. The limitation remains in both papers and the literature record. This item is not marked closed, and no theorem or nonanticipation conclusion is invented.

### 41. Finite checks versus proofs

The new exact tests verify the coefficient substitution, union and saturation ideals, torsion annihilators, nilpotent primary structure, invariant chart equations, embedded chart overlap, genuine pencil and finite product multiplicities. The general global quotient, sheaf twist and coherent-cohomology arguments are written proofs, not outputs certified by those tests. The full inherited chain is executed in the remote checkout; preservation does not certify mathematical correctness.

### 42. Independent external audit of Paper I

No new independent external proof audit of the full sharp inverse has been obtained. This request remains open in both the reading entry and the scope statement. Internal examination of its application and exact CI tests are not renamed an external referee audit.

### 43. Focus without arbitrary deletion

Paper II now follows the power ideals, fixed-target comparison, complete contact fibre and collision family. The old slice and non-equidimensionality proofs, singular-pencil theory and reciprocal-fibre calculations remain in the supplementary sections. Paper I retains the sharp inverse as its main argument and the collision application as supplementary. All predecessor mathematical blocks and labels are preserved, and replaced front matter is archived rather than silently removed.

### 44. Precise conjecture beyond the proven range

The preserved `conj:contact-components-v163` remains explicitly conjectural for contact lengths at least three. The collision theorem supplies a proven adjacency mechanism in the first nonreduced range but does not convert that higher-length conjecture into a theorem. In particular neither a decorated-partition component list nor a general dimension formula is extrapolated from this calculation.

## Preservation, dependency and remaining scope

The input is the complete v163 master, locked by SHA-256, with 520 labels and 348 mathematical environment blocks. The assembler rejects missing labels, lost blocks, duplicate labels, undefined references and incomplete companion allocation. It archives the preceding front matter. The current numerical counts and page numbers are generated by the actual build, not guessed in this response.

The new collision results depend on the complete first-contact and embedded-comparison theorems, and this dependency is explicit. They add a moving-support geometric explanation and exact excess/nilpotent sheaves rather than claim a new proof of every inherited assertion. The broader Hilbert classification at higher corank, arbitrary contact length and singular pencils is not complete; the sharp inverse and singular-pencil invariant theorems retain their original domains. The external audit and Ballico full-text comparison remain uncompleted. The manuscripts contain the stated arguments for independent mathematical scrutiny, without an assertion of formal certification or editorial acceptance.
