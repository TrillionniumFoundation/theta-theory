# A2 revision 163 — response to the complete v162 report

## Controlling objects

The controlling report is `reviews/a2-v162-independent-harsh-top4-2026-09-25/REFEREE_REPORT.md` at `7e9c057907cc4502858a54f32ab0c0cfa264680f`. The reviewed complete v162 tip is `299a77c6f77c4d5aec6e5737e1b1ba471ce5b7c8`; its source and materialization commits are `5f0cb5538faddf20af4ebea70615058677f1c9df` and `4abda6bcfecbc66fe17576be8ea8f40d7d7b25bc`. The new branch is `revision/a2-v163-embedded-comparison-contact-fibres-2026-09-25`, based directly on the controlling report. No predecessor branch or mathematical source is overwritten.

## Principal changes

The main response is a complete scheme-fibre theorem, not an additional selected arc. Theorem `thm:complete-fibre-v163` identifies the whole first nonreduced local fibre. Its reduced components are P^4 and the Hirzebruch surface F_2, with reduced intersection P^1, the doubled-line locus. Near that intersection the full fibre is

`C[[lambda,e,A,B,C]] / (eA,eB,e^2 C)`.

This identifies its embedded associated prime, its nonzero square-zero nilradical `(eC)`, and the locus where it is not Cohen–Macaulay. The conic component has dimension exactly four; no further components occur. A Hilbert–Burch chart with a regular inverse proves the local assertion, and a proper open-and-closed exhaustion plus connectedness of the fibre proves completeness.

Theorem `thm:product-fibres-v163` covers any number of distinct regular corank-two contacts with smaller Smith exponent one or two and arbitrary larger exponents. The entire actual pencil fibre is `X_2^r x (P^1)^s` as a scheme. It has exactly `2^r` reduced components, dimensions `s+2r+2j`, all their intersections, and nilradical of exact nilpotence order `r+1`. This advances beyond the earlier primitive product open and the single `(2,2)` example.

Proposition `prop:embedded-functors-v163` separately gives the category-sensitive comparison requested in the report. It defines the fixed and relative targets, retains the pencil base, undoes each parameter-dependent congruence, and uses a precise flat-completion patching theorem allowing torsion. Algebraic coherent ideal families are constructed before their completed local rings are compared. Normalization of a total graph is never interchanged with normalization of a fibre.

The theorem/page index gives the final numbering in the independently compiled papers. All earlier mathematical blocks remain in the master and are allocated exactly once between the companions. The sharp inverse retains its domain, including singular pencils. The new complete Hilbert-fibre theorem has the explicit domain just stated; it is not asserted for every higher-contact or higher-corank pencil.

## Responses to all 44 requests

### 1. Coefficient topology

The proof of `prop:embedded-functors-v163` uses `T[[x_i]]` for Artin T. The normal-form induction is in the base maximal ideal; the x powers specify the bounded polynomial remainders, not a second convergence argument. The complete universal base is the inverse limit of these finite Artin constructions.

### 2. Coordinate-free tangent map

Lemma `lem:framed-tangent-v163` displays `dot A -> [j^* dot A j]` in the residual congruence quotient, where j is the orthogonal residual inclusion. It derives the map by differentiating the Schur complement and only then chooses Jordan coordinates to invoke the established surjectivity calculation.

### 3. Orthogonal stabilizer

The same lemma isolates the skew-adjoint centralizer. An unordered pair of equal-eigenvalue cyclic blocks contributes `min(d_i,d_j)` parameters, the opposite block is its negative adjoint, a single cyclic block contributes no skew-adjoint polynomial, and distinct eigenvalues contribute zero. No semisimplicity assumption is used.

### 4. Framed versus unframed dimensions

The exact tangent sequence from Hom(R,M) to Hom(R,M/R), with kernel End(R), is written explicitly. The four pencil-basis directions are not silently declared to vanish in the parameter-fixed contact quotient. The N count is for a fixed nonsingular member on the framed slice, with source-congruence orbit dimension subtracted; it is not a dimension assertion for a quotient by every source and parameter action.

### 5. Formal miniversality

The normal coefficient base is called a completed formally smooth chart until an algebraic ideal family has been constructed. The embedded comparison then proves a completed local isomorphism; the finite-presentation étale-monomorphism argument is a separate last step.

### 6. Residual stabilizers

The embedded deformation functors have equality of closed subschemes as their isomorphism convention. Congruences are chosen target identifications on contact discs, not a quotient on Hilbert objects. A new choice composes the forward comparison with a change and the inverse with its inverse. The fixed-target composition is the identity, including on atlas overlaps.

### 7. Retained coefficient base

Both the new fibre theorem and the recovery lemma define Gamma_a as a graph over B_a. The inverse receives f,g,r from its projection to B_a; it does not purport to recover them from an unlabelled Hilbert point alone. The conic-chart inverse explicitly uses the linear coefficient of f to recover c.

### 8. Nonreduced union exact sequence

Lemma `lem:recovery-details-v163` writes `0 -> L -> L|C + L|T -> L|D -> 0`. The tail restriction is evaluation from the free rank-two Artin module of O(1) sections onto the attaching section and has a unit coefficient. This proves surjectivity before reducing the Artin base.

### 9. Uniform cohomology and base change

The same lemma proves H^1=0 and h^0=2a at every central w. It takes a pointwise open neighbourhood for each w; these opens cover the central locus. It does not claim one unspecified uniform affine shrinking. The new conic chart analogously treats every nonzero conic, including doubled lines, using its plane hypersurface sequence.

### 10. Cokernel line and dense vanishing

The recovery map has ranks 2a-1 and 2a and is a split injection after shrinking. Its cokernel is a line bundle on an integral reduced graph neighbourhood. The retained third-coordinate section vanishes densely and therefore vanishes as a section; coefficient recovery is regular and scheme-theoretic.

### 11. Homogenization in Psi

The displayed map is `WG - s Q_0 F`, where W has degree a-1 and Q_0 degree a-2. The recovered section is `s^(a-1) R`. The q space is zero when a=1. This makes the infinity coordinate and the absent top q coefficient explicit.

### 12. Infinity chart

For the new chart, the matrix is homogeneous in [s:t]. At s=0, its two bilinear minors give G=H=0 because t is invertible. Thus infinity is the single forced lift P; there is no hidden tail or additional Hilbert choice there. The comparison glues contact completions to this forced complement.

### 13. Primary structure of repeated roots

Proposition `prop:resultant-strata-v163` describes one primary algebra `C[x]/((x-xi)^mu)` for each distinct support. Chinese remainder decomposition is only between distinct roots. The local first nonreduced fibre has its own separate primary decomposition `(e) cap (A,B,C) cap (A,B,e^2)`, including an embedded prime.

### 14. Jet convention

The primitive chart uses maps from Spec C[x]/(x^a), hence J_(a-1)(P^1). In particular J_1(P^1) is the tangent bundle Tot O(2), not a space of second derivatives or an a-jet with a+1 coefficients.

### 15. Smoothness and irreducibility of the Weil restriction

On either reduced-direction affine chart, a map from the length-a local algebra has a slope with a arbitrary coefficients, giving A^a. The two charts overlap where the constant slope coefficient is nonzero, an irreducible nonempty open. They are smooth and glue by inversion in the Artin algebra. The first nonreduced compactification additionally gives the explicit F_2 transitions.

### 16. Hilbert polynomial of the algebraic family

The new determinantal family has the displayed bigraded Hilbert–Burch resolution; its Euler polynomial is 3l+1 for O(1,1). The actual pencil product family is explicitly checked against the complete-quadric polarization and polynomial `binom(n,2)l+1`. The tail and attachment contributions are counted over the full finite contact algebra.

### 17. Separate embedded comparison proposition

This is Proposition `prop:embedded-functors-v163`. It specifies local Artin test algebras with a retained framed base map, embedded quotient objects, equality of subschemes as morphisms, the forced punctured lift, and the specified reduced graph closure. Its inverse is ideal patching, not an abstract isomorphism of matrix congruence classes.

### 18. Target diagram

Equation `eq:incidence-diagram-v163` distinguishes the universal pencil line, its fibre product with complete quadrics, the fixed complete-quadric target times the framed base, and the embedded curve. The Hilbert graph retains the base projection. Thus the first projection recovers the actual pencil point while normal graph coordinates remain relative.

### 19. Parameter-dependent congruence

The map Theta_i acts on the completed relative incidence target over x_i. The inverse construction applies Theta_i inverse before embedding back into the fixed target. It is not treated as one constant PGL(V) element. Changes of frames act by transition identifications and are undone; they do not equate different embedded tails.

### 20. Ideal gluing and completion

Lemma `lem:ideal-patching-v163` supplies existence as well as uniqueness, using Bhatt Proposition 5.6(4) and Example 5.8 for flat Noetherian completions. Its objects are quotient algebras with their ambient structure maps and punctured identifications. It allows contact-supported torsion. Finite presentation, flatness, surjectivity and equations descend on the resulting flat cover. Faithful completion alone is not offered as a gluing existence theorem.

### 21. Étaleness criterion

The completed comparison is applied to already constructed finite-presentation morphisms, with Noetherian local rings and equal residue fields C at closed points. Stacks Lemma 41.11.3 is cited at that use. Recovery makes the morphism a monomorphism; étale monomorphisms give the open immersion.

### 22. Total normalization versus fibre normalization

The notation is now explicit: tilde Gamma_2 normalizes the total Gamma_2, and X_2 is its scheme fibre. The theorem separately describes the normalization of `(X_2)_red` as the disjoint union of P^4 and F_2. The difference is especially visible because X_2 itself has nilpotents.

### 23. Algebraic one-parameter realizations

The doubled-line adjacency families are polynomial families in e or tau. General points of the conic chart lie in the closure of the explicit dense open `e(A^2+CB^2) != 0`; a generic algebraic line through the point and normalization of its closure provide an algebraic one-parameter specialization. Formal curves in the ambient comparison are not silently renamed algebraic without the already constructed ideal family.

### 24. Resultant strata

Proposition `prop:resultant-strata-v163` gives the gcd partition stratum of total degree d and k distinct roots dimension `3a-2d+k`, hence codimension `2d-k`. At squarefree f with d common roots the resultant is a product of d independent evaluation parameters and has multiplicity d. No normal-crossing assertion is made at multiple roots of f.

### 25. Closure of the primitive open

The complete theorem now identifies its closure as F_2, rather than only invoking the component-closure lemma. It is a proper closed immersion, with open part J_1(P^1) and explicit infinity section. The local fibre has exactly the two minimal primes displayed; exhaustion then excludes any further component globally in this fibre.

### 26. Relative conic residual family

The family is given by the intersection of the fixed main ideal with the vertical conic ideal, with constant reduced attachment. The conic is recovered as the kernel line of the degree-(0,2) restriction map; the proof also gives the local ideal quotient. This proves the relative closed immersion, including singular and doubled conics.

### 27. Unparameterized conics

A point of P^4 is a quadratic equation up to scalar, not a parametrization of its normalization. The embedded conic and its retained position are recovered from that kernel line. Parametrizations differing by source automorphisms therefore do not create additional Hilbert parameters, and distinct quadratic equations do give distinct embedded subschemes.

### 28. Finite pullback and dimension

The previous existence argument through a finite inverse image is preserved. The new proof is stronger on this class: the total Hilbert graph is regular in the explicit chart around every conic tail, so normalization is the identity there. It constructs a closed P^4 in the normalized fibre and identifies its component directly. No unjustified general lifting through normalization is used.

### 29. Exact higher component dimension

It is exactly four. Theorem `thm:complete-fibre-v163` identifies the entire conic component with P^4 and proves that there are only two components. This replaces neither the earlier proof nor its statement; it strengthens its former lower bound.

### 30. Intersections of the components

Their reduced closed structures meet scheme-theoretically in P^1, the doubled lines through the attaching point. Locally their ideal sum is `(e,A,B,C)` in the full fibre ring. The same calculation determines every intersection in a product fibre.

### 31. Doubled-line boundary

The family `(xG-eH,xH,H^2)` specializes a primitive jet of slope `lambda+x/e` to the planar doubled line `H^2=0`. The conics `H^2+tau FG=0` specialize smooth conic tails to the same point. Both are explicit flat algebraic families and include the attachment.

### 32. Reducedness

The fibre is not reduced. The exact ideal `(eA,eB,e^2C)` has radical `(eA,eB,eC)`, nilradical `(eC)` and embedded associated prime `(e,A,B)`. The nilradical is square zero and supported on conics singular at P. This is a calculation in a fibre of a regular total graph, demonstrating why total normality did not settle reducedness.

### 33. Beyond (2,2)

The complete product theorem allows contacts `(1,b)` and `(2,b)` for arbitrary permissible b, and any number of distinct supports. The factor k in the residual form is a removable generating-row factor that is undone in the fixed incidence target. It therefore does not change this fibre. For a>=3 the larger component problem is formulated as a conjecture, not inferred from degree-two calculations.

### 34. Primitive open versus full fibre

The earlier primitive open is still named an open. The new complete theorem uses two proper families, local inverse charts and connectedness to prove exhaustion. Only after that argument is the fibre called completely classified, and only under its stated contact-length hypotheses.

### 35. Effective category

Corollary `cor:effective-full-fibres-v163` explicitly uses the effectively rigidified pencil-failure image. It transports the full scheme fibre through reconstruction. Neither the abstract deformation functor of arbitrary finite algebras nor a pre-reconstruction internal operation is asserted.

### 36. Automorphism extension

Proposition `prop:linearized-envelope-v163` first writes the group extension and then constructs its splitting. The GL(V) weights `2p` on B_p and `-2p` on O(2p) cancel, giving a specified PGL(V) linearization. Only that splitting justifies the semidirect product. An arbitrary automorphism extension is not claimed to split.

### 37. Algebraicity of BH_h

The fixed object is the graded source-normalized bundle and its multiplication/power diagram. Its identity-on-source automorphisms form a closed subgroup of a finite product of general linear groups, defined by finitely many multiplication equations. The explicitly split full group is affine of finite type. Its fppf torsors classify forms of this fixed object; hence BH_h is an algebraic classifying stack. This is not a classification of every algebra bundle with those ranks.

### 38. Exponent choice

The statements distinguish h=1 as requiring no auxiliary exponent. For h>1 the choice remains, even though the universal ideal identity gives the same simultaneous graph. None of the component dimensions is justified by treating different envelopes as the same graded algebra.

### 39. Broader literature

The introduction and literature record add the actual definitions and theorems on stable quotients, stable quasimaps with one parametrized component, the stable map-quotient comparison, and determinantal presentations of rational-curve Hilbert spaces. The inspected primary results are identified precisely. Their different objects and virtual theories are not identified with this embedded coefficient graph, and an exhaustive priority exclusion is not claimed.

### 40. Ballico 1993

The legitimate publisher route was attempted again but did not yield readable theorem/proof-level text. Both submitted papers retain the documentary limitation. No theorem of the inaccessible paper is invented and no nonanticipation conclusion is drawn from the access failure.

### 41. Finite checks

The new suite checks the universal matrix minors and substitution, the exact central ideal before radicals, primary intersections and nilpotent annihilator, the doubled-line family, slope transitions, Hilbert polynomial, component profiles and gcd-stratum tangent ranks. These are finite exact audits accompanying written proofs. The full inherited chain is run in the remote repository. Neither tests nor preservation receipts certify the general theorems or editorial significance.

### 42. Independent audit of Paper I

No new external independent proof audit has been obtained in this revision. This request remains explicitly open in both papers and the review entry. The current revision does not rename its own proof checking or the CI suite an independent referee audit.

### 43. Focus without deletion

Paper II's main route is now multiplication, contact comparison, the complete fibre and its products. The earlier non-equidimensionality argument, reduced incidence, higher-contact slices and reciprocal-fibre material are placed in supplementary sections with all proofs retained. Paper I's main route remains the sharp inverse; its boundary application stays supplementary. The master preserves every prior mathematical block, while the focused sources give a definite logical reading order.

### 44. Full-fibre conjecture

Conjecture `conj:contact-components-v163` is stated for the fibre X_a of the normalization of the specified total polynomial Hilbert graph. It predicts rational normalizations of reduced components, adjacency of the primitive component to repeated-line loci, and nonreducedness for a>=2. The cases a=1,2 are established here; a>=3 is explicitly conjectural. It does not assert an unproved decorated-partition classification or extrapolate a dimension formula without evidence.

## Preservation and remaining scope

The complete v162 master is pinned by SHA-256. All 490 labels and 325 mathematical environment blocks are retained; proof-block preservation is checked byte for byte, and the body is assigned exactly once across the two papers. All replaced front matter and the former root review entry are archived. The complete v163 sources compile independently, without companion auxiliary files.

The present results classify a whole nonreduced boundary class, including scheme structures and adjacency, rather than every pencil boundary. Higher contact lengths, higher corank and singular pencils in the Hilbert compactification are outside the complete-fibre theorem. The sharp inverse and singular-pencil invariant results remain intact on their original domains. The external Paper I audit and Ballico full-text comparison remain uncompleted. The revision is provided with proofs for independent scrutiny, not with a claim of formal certification or journal acceptance.
