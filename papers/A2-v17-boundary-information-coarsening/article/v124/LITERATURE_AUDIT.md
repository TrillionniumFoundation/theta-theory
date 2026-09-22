# Literature and priority audit — A2 revision 124

Date: 23 September 2026.

This file distinguishes (i) theorem text actually inspected, (ii) bibliographic or abstract-level records, and (iii) mathematical conclusions proved internally. A title match, metadata record, or inaccessible article is never used as evidence of non-anticipation.

## 1. Ballico failure-locus line

### E. Ballico (1993)

**Citation:** E. Ballico, *On the Failure Locus of Higher Order Properties of Embeddings in Projective Spaces*, Math. Nachr. 163 (1993), 5–13, DOI 10.1002/mana.19931630102.

**Access status:** bibliographic/publisher record verified; complete theorem text not obtained in the present audit. Repeated searches reached the Wiley issue/article entry and bibliographic mirrors, but no independently verifiable full theorem-text copy.

**Audit consequence:** no assertion is made that the 1993 article anticipates or fails to anticipate Revision 124. The flag `ballico_1993_complete_text_read` remains false.

### E. Ballico (1996)

**Citation:** E. Ballico, *On the failure cycle for the quadratic normality of a projective variety*, Pacific J. Math. 172 (1996), 307–313.

**Access status:** full article inspected from the MSP/Pacific Journal scan.

**Inspected mathematical scope:** the paper works with an integral projective variety, a very ample line bundle and the resulting complete projective embedding. It studies failure of quadratic/higher normality through multiplication maps between spaces of global sections and transfers such failure to suitable projective linear sections and finite subschemes. The final section also treats the first failed higher-normality step. The paper explicitly cites Ballico 1993 as its predecessor.

**Theorem-level crosswalk to Revision 124:**

| Axis | Ballico 1996 | Revision 124 |
|---|---|---|
| Fixed object | Projective variety and very ample line bundle | Finite local cube-zero algebra (B_R) |
| Parameter object | Projective linear sections / finite subschemes | (Kin Gr(4,Voplus S_R)), hence unital subspaces (C1oplus K) |
| Multiplication | Global-section multiplication (H^0(L^a)otimes H^0(L^b)	o H^0(L^{a+b})) | (operatorname{Sym}^m(Ooplus K)	o B_R) |
| Failure output | Failure amount/cycle and propagation to sections | Zeroth Fitting **scheme** with nonreduced embedded structure |
| Scheme structure | Not used there to reconstruct a nilpotent filtration | Nilradical powers and annihilator schemes are main invariants |
| Higher-corank theorem | Not the projection-rank stratification used here | Exact all-corank block Fitting presentation |
| Reconstruction | No K3 polarization reconstructed from a failure scheme | (omega_Eotimes N^{-9}) recovers the quartic polarization |
| Corank-two contact | Not the binary-quartic contact cover used here | Global degree-four contact cover, discriminant class (12H) |

This comparison does not substitute Ballico 1996 for the unread 1993 paper; it records the closest theorem text that was actually inspected.

## 2. Reye congruences and nodal Enriques surfaces

### Cossec (1983)

**Citation:** F. Cossec, *Reye congruences*, Trans. Amer. Math. Soc. 280 (1983), 737–751.

**Role in Revision 124:** classical source for Reye congruences. Revision 124 does not claim the Reye congruence construction itself as new.

### Arrondo–Sols (1992)

**Citation:** E. Arrondo and I. Sols, *On congruences of lines in the projective space*, Mém. Soc. Math. France (N.S.) 50 (1992).

**Inspected claim used:** their Reye-congruence Hilbert parameter is smooth of dimension 24 and rational, with an open Grassmannian description. Revision 124 uses this to explain geometrically the 24-dimensional web parameter before projective quotient.

### Dolgachev–Reider (1991)

**Citation:** I. Dolgachev and I. Reider, *On rank 2 vector bundles with (c_1^2=10) and (c_2=3) on Enriques surfaces*, LNM 1479 (1991), 39–49.

**Inspected claim used:** for a Reye polarization, the relevant stable rank-two bundle is the Reye bundle and is uniquely determined up to isomorphism; it is the Grassmannian universal-quotient bundle restricted to the Reye model. Revision 124 uses this only to interpret the generic finite Torelli packet, not to assert generic degree one.

### Ingalls–Kuznetsov (2015)

**Citation:** C. Ingalls and A. Kuznetsov, *On nodal Enriques surfaces and quartic double solids*, Math. Ann. 361 (2015), 107–133.

**Role:** modern source for the web-of-quadrics / bilinear K3 / involution picture. Revision 124 retains the direct kernel-line proof identifying its source-Jacobian K3 with the bilinear incidence K3.

### Martin–Mezzedimi–Veniani (2024)

**Citation:** G. Martin, G. Mezzedimi and D. C. Veniani, *Nodal Enriques surfaces are Reye congruences*, J. Reine Angew. Math. 808 (2024), 49–65.

**Inspected claim used:** classical nodal Enriques surfaces are Reye congruences. This supports the manuscript's explicit statement that the nine-dimensional nodal/Reye locus is classical geometry rather than a new dimension theorem.

### Dolgachev–Kondō (2025)

**Citation:** I. Dolgachev and S. Kondō, *Enriques Surfaces II*, chapter on Reye congruences.

**Role:** modern synthesis only. Revision 124 does not use it as a substitute for the primary Reye sources.

### Novelty boundary after this comparison

Revision 124 does **not** claim as new:
- the existence of the bilinear incidence K3;
- the fixed-point-free factor-exchange involution;
- the Enriques quotient / Reye congruence;
- the fact that the Reye/nodal-Enriques locus has dimension nine.

The theorem residue is:
- extraction of the polarized K3 from the abstract nonreduced multiplication-failure Fitting scheme;
- the line (omega_Eotimes N^{-9}) and its section ring;
- the intrinsic nilpotent-depth filtration whose next stage recovers the rank-two Schubert support;
- the exact all-corank residual block presentation for the multiplication scheme;
- the global contact cover and its scheme-theoretic interaction with the depth-two layer.

## 3. Nonreduced and multiple structures

### Bayer–Eisenbud (1995)

**Citation:** D. Bayer and D. Eisenbud, *Ribbons and their canonical embeddings*, Trans. Amer. Math. Soc. 347 (1995), 719–756.

**Comparison:** ribbons provide the classical multiplicity-two/square-zero conormal setting. The corank-one local model in Revision 124 also has a square-zero nilradical line on its embedded support, but the manuscript does not identify the whole failure scheme with a ribbon. Its reconstruction theorem uses the particular multiplication-induced line and the canonical bundle to recover a K3 polarization.

### Manolache (2003)

**Citation:** N. Manolache, *Cohen–Macaulay nilpotent schemes*, arXiv:math/0312514.

**Comparison:** standard source for filtrations and associated graded structures on nilpotent multiple schemes. Revision 124's annihilator filtration is intentionally defined for the Fitting scheme without assuming Cohen–Macaulayness on every higher-corank boundary.

### Drézet (2021)

**Citation:** J.-M. Drézet, *Primitive multiple schemes*, Eur. J. Math. 7 (2021), 985–1045.

**Comparison:** primitive multiple schemes have canonical lower-multiplicity filtrations. Revision 124 does not claim that the general idea of a nilpotent filtration is new. The new theorem identifies two specific annihilator layers with (i) a polarized ramification K3 reconstruction and (ii) the rank-two Schubert support of the multiplication-failure scheme.

## 4. Determinantal theory

The v123 comparison is retained without change.

- De Concini–Eisenbud–Procesi supply the classical symbolic-order framework.
- Bruns–Conca's inspected theorem statement gives the product-primary formula used in the manuscript.
- The scalar-variable weighted identity is derived coefficientwise from that classical formula.
- The fixed-tensor corank-two and all-corank block theorems are separate calculations and are not claimed to follow from generic determinantal primary decomposition.

## 5. Audit flags

```json
{
  "ballico_1993_complete_text_read": false,
  "ballico_1996_full_text_read": true,
  "ballico_1996_theorem_crosswalk_added": true,
  "reye_classical_nine_dimensionality_claimed_new": false,
  "arrondo_sols_dimension_comparison_added": true,
  "dolgachev_reider_reye_bundle_comparison_added": true,
  "nodal_enriques_reye_comparison_added": true,
  "nonreduced_multiple_structure_literature_compared": true,
  "all_corank_exact_fitting_presentation_proved": true,
  "all_corank_primary_decomposition_claimed": false,
  "priority_certified": false,
  "general_proof_machine_certified": false
}
```

The false flags are deliberate. They separate documentary access and machine certification from the written mathematical proofs.
