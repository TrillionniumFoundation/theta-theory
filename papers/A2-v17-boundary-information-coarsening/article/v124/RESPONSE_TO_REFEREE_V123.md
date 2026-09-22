# Response to the independent v123 referee

**Manuscript:** *Intrinsic nilpotent depth, Reye geometry, and higher-corank structure in multiplication failure*  
**Revision:** 124  
**Controlling report:** `reviews/a2-v123-independent-harsh-top4-2026-09-23/REFEREE_REPORT.md`  
**Reviewed predecessor:** `revision/a2-v123-polarized-k3-corank-two-2026-09-23`

We thank the referee for a report that separates correctness from theorem scale. We have not weakened the theorem, removed the v123 mathematics, or replaced an unresolved point by a negative claim. Revision 124 keeps the complete v123 arguments and adds a single structural spine: the annihilators of successive powers of the intrinsic nilradical. This spine unifies polarized reconstruction and the first higher-corank embedded support, extends the exact Fitting presentation to every projection-rank stratum, and globalizes the corank-two contact branches without choosing their roots.

## E123.1 — Ballico 1993

We agree with the referee's methodological point: lack of access is not evidence of novelty. The complete theorem text of the 1993 paper was again sought through the publisher and bibliographic mirrors but was not available to this revision. We therefore do **not** set `priority_certified=true`, and we do not state that Ballico 1993 does or does not anticipate the present theorem.

What has changed is the precision of the comparison that can be made from an inspected theorem source. Section 9 now gives a theorem-level crosswalk with Ballico's accessible 1996 continuation, *On the failure cycle for the quadratic normality of a projective variety*. The latter starts with an integral projective variety, a very ample line bundle and multiplication maps between spaces of global sections, and propagates failure of normality to suitable linear sections/finite subschemes. Our parameter point is instead a unital subspace of a fixed cube-zero algebra, our failure object is the zeroth Fitting **scheme**, and the main conclusions concern its embedded associated supports, powers of its nilradical, and the polarized K3 reconstructed from an intrinsic line on an annihilator scheme.

This does not pretend to close the unread 1993 text. It does close the logical dependence: no mathematical theorem in Revision 124 is premised on a non-anticipation assertion about that source, and the exact accessible predecessor is now compared at theorem level.

## E123.2 — the classical Reye/Enriques nine-dimensional locus

We have accepted the referee's central correction and made it structural rather than cosmetic.

The manuscript now states explicitly that the number nine is classical in this geometry. Section 9 identifies the regular-web quotient with the Reye/nodal-Enriques locus and cites Cossec, Arrondo--Sols, Dolgachev--Reider, Ingalls--Kuznetsov, Martin--Mezzedimi--Veniani, and the modern Enriques treatment. Arrondo--Sols' 24-dimensional smooth Hilbert parameter and the 15-dimensional projective-coordinate orbit give the classical tangent quotient of dimension nine; the modern nodal-Enriques theorem identifies the classical nodal locus with Reye congruences.

Accordingly, Theorem 1.3's predecessor (v123 Theorem 1.2) is no longer presented as if `24-15=9` were the novelty. The exact 25-by-25 determinant is retained for a different reason: it proves that the **specific source-Jacobian quartic polarization arising from the multiplication problem** does not collapse any of the 24 web directions at the explicit rational point. After quotienting projective coordinates, this gives the rank-nine tangent statement for the recovered polarized K3 invariant.

The theorem-level residue after the classical geometry is subtracted is now explicit:

1. the polarized quartic K3 is reconstructed from the abstract nonreduced multiplication-failure scheme;
2. the reconstruction uses the intrinsic line `omega_E tensor N^{-9}`, not a chosen web or ambient projective marking;
3. the next nilpotent-depth layer recovers the first higher-corank Schubert support;
4. the corank-two contact data form a canonical global degree-four cover with a discriminant divisor of Pluecker class `12H`.

## E123.3 — higher-corank structure beyond one admissible chart

Revision 124 adds two levels of closure.

First, Theorem 8.1 gives an exact block presentation on **every projection-rank stratum**. If the projection has image `H` of rank `r`, Schur reduction produces a transverse matrix `T` of size `4-r`, and
[
 I_{\widehat D}
 = (\det T),
   I_6[A_H, B_H(1_H\otimes T), C_H\operatorname{Sym}^2T].
]
No injectivity, mixed-rank, kernel-rank, or simple-contact hypothesis enters this identity. Thus coranks one through four are not separate guessed models: they are exact specializations of the same whole-Grassmannian Fitting theorem.

Second, on the mixed-regular projection-corank-two locus we remove the simple-root hypothesis. The residual ideal has the root-free form
[
 J=\delta\mathfrak m+(g_0,\ldots,g_4),
 qquad
 (g_0,\ldots,g_4)mod(\delta)
 =h_H(u)\operatorname{Sym}^4(v),
]
with no factorization of the binary quartic `h_H`. Therefore the nilradical still has exact index three and `Ann(N^2)` is the rank-two stratum through the collision types `1111,211,22,31,4`. What changes at the discriminant is the splitting of the contact-primary factors, not the intrinsic depth-two support.

We do not claim a closed primary-decomposition table for the mixed-rank-drop or rank-one-kernel locus. The referee explicitly allowed a “global structural replacement”; the all-corank block theorem plus the nilpotent-depth filtration is that replacement, while the paper states exactly where a finer primary classification is and is not proved.

## E123.4 — unifying polarized reconstruction and higher corank

This is the principal architectural change.

For any noetherian scheme `Z` define
[
 Z_j=V(\operatorname{Ann}(N_Z^j)).
]
This is functorial under abstract scheme isomorphisms and requires no ambient marking or chosen primary decomposition.

For the multiplication-failure scheme:

- on the smooth-reduction/corank-one locus, `Z_1=E_R`; the line `N|_{E_R}` and `omega_{E_R}` recover the fourth Veronese section ring and hence the quartic polarization;
- on the mixed-regular corank-two locus, `Z_2=Sigma_R`; `N^2` is the square of the Schubert conormal line and has transverse length one.

Thus v123's reconstruction theorem and corank-two embedded component are now consecutive terms in one intrinsic nonreduced filtration.

## E123.5 — conceptual deformation theorem

Section 9 separates the classical tangent geometry from the exact arithmetic witness. At a general regular web with finite projective stabilizer,
[
 T_{[R]}M_{\mathrm{Reye}}
 \simeq
 T_R\operatorname{Gr}(4,\operatorname{Sym}^2V)/
 \mathfrak{pgl}(V),
]
which has dimension `24-15=9`. The polarized-K3 map is equivariant, so its differential factors through this quotient.

The v123 exact determinant is retained as a certificate that this factorized map has maximal rank at an explicit rational point. It is therefore no longer offered as the conceptual explanation of the nine-dimensional locus; it certifies that our source-Jacobian polarization sees the full classical Reye tangent space.

## E123.6 / M123.1 — finite ambiguity and the Torelli packet

We have not replaced a proved finite result by an unsupported generic-injectivity claim.

The new text identifies what the finite fibre represents. A relation space gives, in addition to the recovered polarized K3, the free factor-exchange involution and hence an Enriques quotient with Reye data. Dolgachev--Reider's Reye-bundle rigidity shows that once a Reye polarization on the Enriques quotient is fixed, the rank-two Grassmannian bundle is rigid in the relevant Chern class.

Moreover, the mixed-regular corank-two contact cover is the incidence
[
 \{(H,[\alpha]):H\subset\ker\alpha, [\alpha]\in Y_R\},
]
so it is already determined by the recovered quartic itself. The remaining generic finite packet is therefore localized to finite choices of compatible Enriques/Reye data and the passage back to a web, with any further separation forced into exceptional/deeper strata. We state this reduction, not a numerical degree that has not been proved.

## E123.7 / M123.2 — literature on nilpotent reconstruction

The bibliography and Section 9 now compare the construction with Bayer--Eisenbud ribbons, Manolache's nilpotent structures, and Drezet's primitive multiple schemes and canonical filtrations.

We explicitly do not claim that nilpotent filtrations as such are new. The specific theorem here is that, for this Fitting scheme of multiplication failure, the first annihilator layer carries the intrinsic line
[
 \omega_E\otimes N^{-9}
]
whose section ring recovers the quartic polarization, while the second annihilator layer is the first singular Schubert support. The ambient failure scheme is not assumed to be a ribbon or a primitive Cohen--Macaulay multiple scheme.

## M123.3 — global corank-two support

This is now a global theorem rather than an etale-local comment.

Over `G=Gr(2,V)` the ramification quartic restricts to a universal binary quartic
[
 h_R\in H^0(G,\operatorname{Sym}^4Q).
]
The contact incidence
[
 R_R=\{(H,[\alpha])\in G\times Y_R:H\subset\ker\alpha\}
]
is a `P^2`-bundle over `Y_R`, hence smooth and irreducible. On the locus where the restriction is not identically zero it is finite flat of degree four over `G`. Its discriminant is a section of `(det Q)^{12}`, so the collision divisor has Pluecker class `12H`. Away from it the cover is finite etale and its monodromy on the four sheets is transitive.

The four local `P_i` in the v123 primary decomposition are therefore the local splitting of this canonical cover, not four globally chosen components. The fifth-power rank-two component also glues globally as the fifth ordinary power of the rank-two Schubert ideal.

## M123.4 — exact Reye object

The manuscript now identifies the quotient of the bilinear incidence K3 by factor exchange as the Reye/nodal Enriques surface associated with the same regular web and treats its nine-dimensional moduli as classical. The first-projection quartic polarization is kept distinct from the target-web symmetroid.

The paper also records the Reye bundle attached to the Enriques polarization and uses its rigidity only to interpret the finite Torelli packet; it is not smuggled in as a proof of a degree-one statement.

## M123.5 — one journal object

Revision 124 has one referee-facing mathematical object:
`article/v124/geometry.tex` and its generated `geometry.pdf`.

The 147-page v123 companion is retained in history as source/evidence preservation. It is not a second v124 journal manuscript. Unchanged v123 proof blocks are included by source reference from the v124 principal article, so their mathematical text is preserved exactly while the v124 theorem architecture is a single article.

## Preservation and verification

Revision 124 does not rewrite the v123 source directory or the controlling review. The exact v123 arithmetic witnesses for the polarized K3 and simple-contact corank-two model are rerun from copies in the v124 review package. The new all-corank and collision theorems are written proofs; their validity is not inferred from finite computations.

No journal acceptance, formal proof certification, or unread-source priority certification is claimed. Those documentary flags are kept separate from the mathematical theorem statements.
