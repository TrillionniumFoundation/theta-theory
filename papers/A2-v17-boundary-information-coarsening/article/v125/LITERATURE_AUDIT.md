# Literature and priority audit — A2 revision 125

Date: 23 September 2026.

This audit distinguishes theorem text actually inspected, bibliographic/publisher records, and mathematical statements proved internally. No metadata-only source is used to infer anticipation or non-anticipation.

## 1. Ballico failure-locus line

### E. Ballico (1993)

**Citation:** E. Ballico, *On the Failure Locus of Higher Order Properties of Embeddings in Projective Spaces*, *Mathematische Nachrichten* **163** (1993), 5–13, DOI 10.1002/mana.19931630102.

**Publisher record:** verified again on 23 September 2026 in the Wiley volume 163 issue record. The issue lists the article on pages 5–13 and exposes a PDF action.

**Full-text status in the present environment:** the publisher PDF action accessible to this revision resolves to the article record rather than complete theorem text. Searches of bibliographic mirrors likewise produced metadata rather than an independently verifiable full-text copy. Therefore ballico_1993_complete_text_read remains false.

**Consequence:** Revision 125 makes no claim that Ballico 1993 anticipates or fails to anticipate the present theorem. In particular, the new residual-colon/associated-graded theorem is proved internally and does not depend on a historical non-anticipation premise.

### E. Ballico (1996)

**Citation:** E. Ballico, *On the failure cycle for the quadratic normality of a projective variety*, *Pacific J. Math.* **172** (1996), 307–313.

**Access status:** full MSP/Pacific Journal scan inspected.

**Inspected scope:** integral projective variety \(X\), a very ample line bundle \(L\), complete projective embedding, and failure of quadratic/higher normality under multiplication of global sections. The results propagate failure to projective linear sections and finite subschemes and treat the first failed higher-normality step. The 1996 paper explicitly cites Ballico 1993 as predecessor.

**Crosswalk to Revision 125:**

| Axis | Ballico 1996 | Revision 125 |
|---|---|---|
| Fixed object | Projective variety + very ample line bundle | Finite local cube-zero algebra \(B_R\) |
| Moving parameter | Projective linear sections / finite subschemes | Unital subspaces \(\mathbf C1\oplus K\) on \(X_R\) |
| Failure map | Global-section multiplication | \(\operatorname{Sym}^m(\mathcal O\oplus\mathcal K)\to B_R\otimes\mathcal O\) |
| Failure output | Failure amount/cycle and propagation | Zeroth Fitting scheme with embedded nilpotent structure |
| Intrinsic filtration | Not the residual-colon filtration used here | \(\operatorname{Ann}(N^j)\) and all graded pieces \(N^j/N^{j+1}\) |
| Whole-space structure | Linear-section failure framework | Global residual-colon associated-graded theorem at every projection corank |
| Reconstruction | No quartic K3 polarization recovered from failure object | \(\omega_E\otimes N^{-9}\) reconstructs the quartic polarization |
| Rank-two boundary | Not the contact algebra here | Unsplit contact ideal, collision primary types, containment, decomposable-kernel wall |

The inspected 1996 text is not used as a substitute for the unavailable 1993 theorem text.

## 2. Reye / Enriques line

Revision 125 continues to credit as classical:

- F. Cossec, *Reye congruences*, Trans. AMS 280 (1983), 737–751;
- E. Arrondo and I. Sols, *On congruences of lines in the projective space*, Mém. SMF (N.S.) 50 (1992);
- I. Dolgachev and I. Reider, rank-two bundles on Enriques surfaces, LNM 1479 (1991);
- C. Ingalls and A. Kuznetsov, *On nodal Enriques surfaces and quartic double solids*, Math. Ann. 361 (2015);
- G. Martin, G. Mezzedimi and D. C. Veniani, *Nodal Enriques surfaces are Reye congruences*, Crelle 808 (2024), 49–65;
- I. Dolgachev and S. Kondō, *Enriques Surfaces II*, Reye-congruence discussion.

The manuscript does not claim as new the bilinear incidence K3, its free factor-exchange involution, the Enriques quotient, Reye congruences, or the nine-dimensional Reye/nodal-Enriques family.

Revision 125 adds an explicit web-to-Hilbert parameter bridge: on the regular locus the universal web gives a \(\PGL(V)\)-equivariant Hilbert morphism, and under the Arrondo–Sols Grassmannian parameter the general tangent space is
\[
 \operatorname{Hom}(R,\operatorname{Sym}^2V/R).
\]
The \(24-15=9\) quotient remains classical context.

## 3. Nonreduced structures

The comparison with Bayer–Eisenbud ribbons, Manolache nilpotent schemes, and Drézet primitive multiple schemes is retained.

Revision 125 sharpens the distinction. It does not claim that nilpotent filtrations are new. Its theorem is the exact formula
\[
 \operatorname{gr}_N\mathcal O_{\widehat D_R}
 =
 \mathcal O_{\widehat\Delta_R}
 \oplus
 \bigoplus_{j\ge1}
 \mathcal L^{\otimes j}\otimes\mathcal O_{W_j}
\]
with
\[
 W_j=
 V_{\widehat\Delta_R}\!\left(
 (\mathcal J_R^{\mathrm{res}}:
  \mathcal I_{\widehat\Delta_R}^{j-1})
 +\mathcal I_{\widehat\Delta_R}\right),
\]
together with the geometric identification of the first pieces, polarized K3 reconstruction, collision primary law, containment algebra, and first decomposable-kernel wall.

## 4. Determinantal background

The De Concini–Eisenbud–Procesi / Bruns–Conca comparisons from the preceding revision remain unchanged. Generic determinantal primary formulas are not used to claim the fixed-tensor contact-boundary theorem.

## 5. Revision-125 theorem residue

After the classical geometry is removed, the theorem residue is:

1. reconstruction of the polarized quartic K3 from the abstract nonreduced multiplication-failure scheme;
2. the whole-Grassmannian residual-colon filtration and associated-graded nilpotent algebra;
3. the explicit mixed-regular identification of its first two graded supports;
4. the complete contact collision specialization law with genuine \(\mathfrak m^5\) vertex-primary component;
5. the zero-quartic containment algebra and finite reduced line scheme;
6. the first decomposable mixed-kernel wall, where \(Z_2\) becomes length-three nonreduced;
7. the finite étale Torelli-packet theorem and its transitive monodromy on dense opens.

## 6. Audit flags

- ballico_1993_complete_text_read: false
- ballico_1996_full_text_read: true
- ballico_1996_theorem_crosswalk_added: true
- reye_classical_nine_dimensionality_claimed_new: false
- web_to_reye_hilbert_bridge_added: true
- nonreduced_multiple_structure_literature_compared: true
- global_residual_colon_filtration_proved: true
- global_associated_graded_nilpotent_algebra_proved: true
- mixed_regular_collision_primary_law_proved: true
- containment_locus_computed: true
- decomposable_kernel_wall_computed: true
- torelli_finite_etale_monodromy_proved: true
- all_corank_primary_decomposition_claimed: false
- general_proof_machine_certified: false
- priority_certified: false
