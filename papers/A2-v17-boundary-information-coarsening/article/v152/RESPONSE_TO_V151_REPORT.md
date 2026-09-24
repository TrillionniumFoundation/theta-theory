# Response to the independent A2 v151 referee report

The controlling report is `reviews/a2-v151-independent-harsh-top4-2026-09-24/REFEREE_REPORT.md`, blob `2d6737c4de6a774e1a607a1eecc09316901cc4ed`, at review commit `11c9e91135c5e8bb3ee61a067d76286d81a3df7d`. This is an owner-requested independent-referee-style report, not a journal editorial decision.

The revision preserves the all-pencil inverse, sharp finite order, arbitrary-base first-relation arguments, moving pencil and actual bundle recovery, coefficient-support asymmetry, exact determinant multiplicity, nonlinear automorphism kernels, transverse families, spectral strata, and covering-map results. Its response to the remaining mathematical objections is a new local singularity theory and a concrete boundary theorem for the motivating failure algebras.

## 1. Beyond normalization: conductor and image singularities

The report's Sections 4–5 and items 15.3, 15.5, and 17.3 ask for structure beyond a finite parametrization and selected fibres. The new section `44-conductor-and-collisions-v152.tex` supplies two theorems with full formal-local proofs.

**Split-divisor theorem (`thm:split-conductor-v152`).** At `K=abL`, where `a,b` are coprime degree-g factors, they are the only degree-g divisors of the exact gcd, and `gcd(L)=1`, the completed image ring is

`C[[z_1,...,z_t,x_1,...,x_c,y_1,...,y_c]]/(x_i y_j)`.

Here `t=2(s_g−1)+r(s_{h−g}−r)` and `c=r(s_h−s_{h−g})−(s_g−1)`. The conductor is `(x,y)`, whereas the singular Fitting ideal is `(x,y)^c`. The branches meet in a reduced smooth t-dimensional scheme; multiplicity is two, depth is t+1, and the ring is Cohen–Macaulay exactly when c=1. These statements concern the image ring, not its normalization fibre. The proof establishes simultaneous divisibility over arbitrary local Artin bases before using a conductor square. It never infers a scheme intersection from tangent dimensions alone.

**Binary collision theorem (`thm:binary-pinch-v152`).** At `K=ell^2 L`, with exact binary common divisor `ell^2`, the image is, up to an explicitly counted smooth factor,

`A_m=C[[u,Delta]] ⊕ (u_1,...,u_m)t ⊂ C[[u,t]], Delta=t^2`, where m=r−1.

The full relations are `u_i w_j−u_j w_i` and `w_i w_j−Delta u_i u_j`. The conductor is `(u,w)`, with quotient cover `C[[Delta]]→C[[t]]`, Delta↦t². The depth and Cohen–Macaulay criterion are proved. For r=2 the singular ideal is `(w,Delta u,u²)`, strictly different from the conductor. For arbitrary r the exact singular scheme is specified by the relevant Jacobian minors, without taking a radical. A Weierstrass argument proves the model is a full local model of the Grassmannian image, not merely an embedded test family.

The general conductor-square mechanism and the ordinary pinch point are classical. The revision identifies these schemes and their invariants on specified common-divisor Grassmannian strata; it does not rebrand the general mechanism as new.

## 2. Divisor-degree intersections

Item 15.4 is addressed by `prop:degree-intersections-v152`. The reduced intersection of Y_a and Y_b is the finite union of images `(c,u,v,L)↦cuvL`, indexed by the degree of the common part of two selected divisors. The statement explicitly concerns the reduced global intersection. Full scheme intersections are proved on the split stratum, and the collision model retains the nilpotent thickening. This separates a global divisor-poset description from the local scheme structures instead of conflating them.

## 3. An actual failure-algebra boundary, uniformly in dimension

Items 17.4–17.5 ask that common-divisor geometry be integrated with pencil degenerations and not be justified by the elementary closed flag orbit alone. The principal new integration is `thm:universal-boundary-v152` in `45-pencil-orbit-boundary-v152.tex`.

For every n≥3, let E have dimension n² and let `Z_R=closure(GL(E) K_R)`. These are intrinsic first-relation orbit closures, independent of markings. All Z_R contain the same explicitly constructed ramified point

`K_infinity=a^(g+k_n)L_n`, `g=n(n−1)`, `k_n=3n−4−q_n`, `q_3=3`, `q_n=4` for n≥4, and gcd(L_n)=1.

Starting from the flag pencil, use `T=aI+tau B`, B_11=0, an invertible linear change of the entire cotangent space for tau≠0. Divide an adapted primitive-relation basis by its precise tau-orders. The associated graded basis remains independent at zero; the relation subbundle therefore gives a finite-flat algebra family. Every nonzero fibre is the flag pencil's genuine failure algebra. The prior finite-flat closed-flag specialization supplies a chain from every initial pencil.

The exact filtration order is proved in all dimensions using the flag coefficient vector `delta^3(v² wedge vw)`. In dimension three the fifteen coordinates have an explicit basis with independent initial monomials of degrees at most three. In higher dimensions the degree bound is four and a displayed quartic attains it. This is a universal argument, not extrapolation from three numerical examples.

The boundary gcd degree is `D−q_n`, strictly larger than g. Thus the selected degree-g divisor is unique but ramified, with fibre tangent dimension `binomial(n²+k_n−1,k_n)−1`. The whole fibre, not only its tangent space, is computed in `prop:pure-power-fibre-v152` by the coefficients of the reciprocal forms `c_(g+1),...,c_(g+k_n)`. In the nine-generator case the limiting 15-plane is displayed, its gcd is a^8, and its unique degree-six divisor has a fibre of embedding dimension 44.

This result does not assert a classification of all GL(E) orbit closures or a Segre-poset classification. It supplies the requested link between natural failure-algebra orbit degeneration and a specific normalization-collision type. The family is explicitly two-stage for a general starting pencil; no unproved common one-parameter subgroup for all pencils is asserted.

## 4. Primary literature comparisons

Items 11, 12, 15.1, 15.6–15.7, 17.2, and 17.6 are answered in the expanded introduction and the orbit-boundary remark.

Chipalkatti 2003, Proposition 5.1, Theorem 5.4, and Corollary 5.8, already identify the uniqueness/tangent-injectivity principle and singular support for binary coincident-root loci. Kurmann 2012, Proposition 1.3 and Theorem 1.5, supplies local incidence equations and scheme equality; Proposition 2.1 gives the partition-splitting smoothness criterion. The revision explicitly credits those mechanisms. Its changed objects are multivariate r-planes and degree-prescribed divisors, with image conductors and depths computed on actual Grassmannian strata.

Hu–Lin–Shao, arXiv:math/0701255v1, Section 2.2, Corollary 3.6, and Theorem 1.1, supplies a direct comparison with tuple common-factor strata, resultant homomorphisms, and blow-up compactifications. On independent binary tuples the span map is a frame quotient. The revision does not assert equality between their determinantal scheme structure and our image structure without proving it.

Ferrand 2003 is cited for conductor squares. Abramovich–Olsson–Vistoli 2008, Appendix A, Theorem A.1, is the primary rigidification reference for compatible flat finitely presented normal inertia subgroups. The particular subgroup identifications remain proved; generic stack technology is no longer the conceptual headline.

Fevola–Mandelshtam–Sturmfels 2021 treats the regular-pencil open set. The flag pencil has identically zero determinant in dimension at least three and lies outside that open. The revision therefore separates the classical congruence classification from its new intrinsic GL(E) failure-boundary result.

## 5. Ballico 1993: documentary item still open

Items 10, 16.1, and 17.1 are **not marked closed**. The publisher volume record confirms the article and pages; the publisher PDF/ePDF access attempts in this session did not return its full text. No legitimate institutional document-delivery request was available or claimed to have been made. The six requested comparisons—failure object, nonreduced structure, infinitesimal order, bases, forgotten markings, and inverse conclusion—cannot be populated on the 1993 side from metadata. No theorem numbers, negative nonanticipation claim, or historical-priority clearance are invented.

This documentary limitation does not alter or reduce the inverse theorem or the new geometry. It remains visible to the next referee, alongside the new primary comparisons that were actually read.

## 6. Scope, style, preservation, and validation

The abstract explicitly names the maximal-lower-Hilbert-function stratum. The new geometry appears before the categorical infrastructure. No v151 mathematical part is edited in place; the updated introduction retains every old theorem, proof, equation block, and label. The old introduction, frontmatter, references, and driver remain available as historical sources. Applications and the historical archive remain separate, with their mathematical drivers unchanged.

The revision runs all 27 inherited exact scripts and a new script containing 42 finite checks. The new checks cover flag jets, exact generalized-pinch elimination, nonradical singular ideals, reciprocal equations, and an independent complementary-minor computation of the n=3 limit. The build receipt records actual outcomes and source hashes; it does not certify universal proofs, exceptional novelty, or journal acceptance. `geometry.pdf` is the principal article for re-review, and `evidence_v152/THEOREM_LOCATOR_V152.json` gives final theorem numbers and pages.
