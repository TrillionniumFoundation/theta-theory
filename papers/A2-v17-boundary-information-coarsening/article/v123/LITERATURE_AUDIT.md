# Primary-source audit and novelty boundary — A2 revision 123

Date: 23 September 2026. This audit records what was read, not what might follow from a title or bibliographic entry. No publisher PDF or font file is redistributed in this packet. The linked sources may have their own access conditions.

## 1. Ballico 1993: outstanding full-text comparison

E. Ballico, *On the Failure Locus of Higher Order Properties of Embeddings in Projective Spaces*, Math. Nachr. 163 (1993), 5–13, DOI 10.1002/mana.19931630102.

Publisher record checked: https://onlinelibrary.wiley.com/toc/15222616/1993/163/1 . Attempts at the publisher's full-text/PDF forms did not provide the complete theorem text. The complete article has **not** been read in this revision. The accessible record and the later 1996 failure-cycle paper mentioned in the report do not determine its theorem scope. The latter paper is not treated as a replacement for the former.

The following requested crosswalk therefore remains unfilled on the Ballico side. On the revision side the object is stated only to specify exactly what must be compared.

| Axis requested by the referee | Revision 123 object | Ballico 1993 theorem-text comparison |
|---|---|---|
| Parameter Grassmannian | `Gr(e,V⊕S_R)` of unital `(e+1)`-dimensional subspaces | Not established without full text |
| Complete/incomplete series | Algebraic subspace `C1⊕K`; not assumed to be a complete global series | Not established |
| Multiplication map | `Sym^m(O⊕K) → B_R⊗O`, all `m≥2` | Not established |
| Failure structure | Zeroth Fitting ideal; exact nonreduced scheme | Not established |
| Fixed/moving contact | Fixed cube-zero relation algebra; relative family also constructed | Not established |
| Embedded structure | Ramification support; corank-two support; intrinsic nilradical modules | Not established |
| Conductor/quotient mechanism | Quadratic quotient algebra; preceding conductor development retained | Not established |
| Higher-order embeddings/jets | No unstated jet-separation hypothesis; exact algebra map specified | Not established |
| Global hypotheses/degrees | `e=3,4`; principal reconstruction on smooth basepoint-free relation class | Not established |

No conclusion of anticipation or non-anticipation is inferred. `priority_certified=false`.

## 2. Determinantal primary decomposition

**Inspected theorem source:** W. Bruns and A. Conca, *Gröbner bases and determinantal ideals*, author preprint https://arxiv.org/pdf/math/0302058 . Proposition 2.2 and Theorem 2.4 on printed pages 13–14 state the symbolic-order description and the product-primary formula, with the characteristic assumptions and classical attribution.

**Classical works credited:** C. De Concini, D. Eisenbud, and C. Procesi, *Young diagrams and determinantal varieties*, Invent. Math. 56 (1980), DOI 10.1007/BF01392548; W. Bruns and U. Vetter, *Determinantal Rings*, LNM 1327 (1988). The author institution's DCEP record gives pp. 129–165; the EuDML record uses the terminal page 166. The manuscript follows the author institution's bibliographic record. The whole DCEP text and the full Bruns–Vetter monograph were not independently reread here. The theorem-level comparison uses the formula actually inspected in Bruns–Conca, not a claim to have inspected every original proof or all of Chapter 10 of the monograph.

**Exact comparison:** Appendix A gives the formula `I^ρ=intersection_j I_j^(γ_j(ρ))`. Adjoining the scalar `t`, symbolic order is calculated coefficientwise. For coefficient degree `u`, the weighted intersection reduces to the one-factor profile `ρ=(q+1−u)`. The retained formula is therefore a consequence of the classical order profile and the scalar coefficient rule. It is not asserted to be a new straightening theorem. A scalar block substitution, by itself, would not justify specialization of primary components; the coefficient argument does. The corank-two fixed-tensor ideal is calculated separately.

## 3. Webs of quadrics and the incidence K3

**Inspected theorem/construction source:** C. Ingalls and A. Kuznetsov, *On nodal Enriques surfaces and quartic double solids*, https://arxiv.org/pdf/1012.3530 , v1 (2010), §4. Published metadata: Math. Ann. 361 (2015), 107–133, DOI 10.1007/s00208-014-1066-y.

Their §4 recalls the web-of-quadrics construction via four bilinear equations in `P³×P³`, its K3 surface, and the involution obtained by transposing the factors. Section 7 supplies the direct identification with the present constant-corank-one Jacobian incidence. The source Jacobian quartic and the web discriminant symmetroid are written with their distinct ambient spaces and equations.

The classical construction, the free involution, and the existence of a web K3 are not claimed as new. Nor is the mere existence of a nine-dimensional web family claimed as a historical discovery. The main invariant in this manuscript is the canonical graded section ring built from the nilradical line of the multiplication-failure scheme, which recovers its quartic polarization. The new higher-corank calculation concerns an additional associated component of that failure scheme, not a newly invented web/incidence surface.

**Additional contemporary reference, metadata only:** I. Dolgachev and S. Kondō, *Enriques Surfaces II* (2025), Chapter 2, *Reye Congruences*, pp. 67–141, DOI 10.1007/978-981-96-1513-1_2. The publisher chapter record and abstract were checked; the full chapter was not read or used as a theorem-level non-overlap certificate.

## 4. Standard K3 and birational ingredients

D. Huybrechts, *Lectures on K3 Surfaces*, Cambridge 2016, DOI 10.1017/CBO9781316594193. The author's page and published contents were checked: https://www.math.uni-bonn.de/people/huybrech/K3.html . The present article supplies the short torsion-freeness argument actually needed for the fourth root and the deformation/stabilizer calculation. Chapter 5 is cited for the standard polarized moduli setting. No full rereading of the book is asserted.

J. Kollár, *Rational Curves on Algebraic Varieties*, Springer 1996, Chapter IV, §5 is cited for the MRC framework. The new polarized theorem does not depend on a stronger cancellation statement inferred from that reference: it has a direct section-ring proof. The prior elementary cancellation argument is preserved in the companion.

## 5. Audit flags

The source-access and formula checks above are distinct from comprehensive priority certification. In particular:

- `ballico_1993_complete_text_read=false`;
- `classical_determinantal_formula_compared=true` (via the inspected theorem statement and an explicit coefficient proof);
- `entire_dcep_article_independently_reread=false`;
- `entire_bruns_vetter_book_independently_reread=false`;
- `classical_incidence_construction_compared=true`;
- `priority_certified=false`.

The revision is submitted for independent mathematical and historical review. No bibliographic access failure is used as evidence of novelty.
