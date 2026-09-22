# A2 revision 124 — intrinsic nilpotent depth and the Reye boundary

**Branch:** `revision/a2-v124-intrinsic-nilpotent-reye-boundary-2026-09-23`  
**Author:** Qian Qi  
**Date:** 2026-09-23  
**Parent review:** `review/a2-v123-independent-harsh-top4-2026-09-23`  
**Responds to:** `reviews/a2-v123-independent-harsh-top4-2026-09-23/REFEREE_REPORT.md`

## Referee object

The referee-facing manuscript is

- `papers/A2-v17-boundary-information-coarsening/article/v124/geometry.tex`
- generated PDF: `papers/A2-v17-boundary-information-coarsening/article/v124/geometry.pdf`

Revision 123 remains unchanged in this branch as the complete historical source/evidence companion. Revision 124 is an additive source layer: unchanged arguments are included verbatim from v123, while the new conceptual and priority-critical arguments live under `article/v124/`.

## Mathematical changes relative to v123

Revision 124 keeps the polarized reconstruction theorem and the fixed-tensor calculations, but reorganizes them around one intrinsic invariant of the nonreduced failure scheme.  If `N` is its nilradical, the closed schemes

[
  Z_j = V(\operatorname{Ann}(N^j))
]

form the **nilpotent-depth filtration**.  On the smooth-reduction (projection-corank-one) locus, `Z_1` is the ramification support and its conormal line recovers the polarized Jacobian surface.  On the mixed-regular projection-corank-two locus, `Z_2` is the rank-two Schubert support and `N^2` is the intrinsic transverse line already detected in v123.  Thus the two headline mechanisms are successive stages of one functorial filtration rather than unrelated local effects.

The corank-two theorem is also globalized in three directions.

1. The exact residual Fitting presentation
   [
   (\det T) I_6[A_H,,B_H(1\otimes T),,C_H\operatorname{Sym}^2T]
   ]
   is recorded on the entire projection-rank-two stratum; no admissibility hypothesis is needed for this presentation.
2. After the mixed tensors have maximal rank, the unsplit contact normal form remains valid when the four ramification contacts collide.  The five collision types are the partitions `1111, 211, 22, 31, 4` of a nonzero binary quartic.
3. Over `Gr(2,V)` the contact quartic is a section of `Sym^4 Q`; its discriminant is a section of `(det Q)^12`.  Hence the collision divisor has Plücker class `12H`.  Off that divisor the four branches form a degree-four finite étale cover; the primary components in the v123 local theorem are its local splittings, and the fifth-power component glues as the fifth ordinary power of the rank-two Schubert ideal.

The moduli argument is rewritten so that the nine-dimensional statement is not presented as a new dimension count.  The web quotient is related explicitly to the classical Reye/nodal-Enriques locus, which is the classical nine-dimensional divisor in Enriques moduli.  The exact 25-by-25 certificate is retained only as an arithmetic witness for the polarized-K3 map, not as the conceptual reason that Reye geometry has nine moduli.

The priority discussion is enlarged to include:

- Cossec's Reye-congruence theorem and modern nodal-Enriques results;
- Arrondo--Sols on the Hilbert scheme of Reye congruences;
- Dolgachev--Reider on the Reye bundle;
- Bayer--Eisenbud, Manolache, and Drézet on ribbons and nilpotent/multiple structures;
- Ballico's 1996 failure-cycle paper as a theorem-level accessible continuation of the 1993 paper.  The 1993 full text remains access-restricted, and the manuscript does not claim otherwise.

## Referee map

The detailed point-by-point response is in

`papers/A2-v17-boundary-information-coarsening/article/v124/RESPONSE_TO_REFEREE_V123.md`.

The main correspondence is:

- **E123.1 / P123.1 (Ballico):** theorem-level crosswalk against Ballico 1996 plus a sharply limited statement about the inaccessible 1993 text.
- **E123.2 / M123.4 (Reye/Enriques):** classical 9-dimensional Reye geometry isolated explicitly; theorem residue restated.
- **E123.3 / M123.3 (corank two):** full residual presentation on the entire rank-two stratum, collision stratification, discriminant class, intrinsic gluing, and nilpotent-depth support.
- **E123.4 (unification):** new global nilpotent-depth theorem.
- **E123.5 (moduli concept):** geometric Reye/nodal-Enriques factorization and tangent-space interpretation; determinant retained only as exact witness.
- **E123.6 / M123.1 (finite ambiguity):** the finite ambiguity is interpreted as a finite web/Reye-structure fibre on the recovered polarized K3; the manuscript makes no unsupported degree-one claim.
- **E123.7 / M123.2 (nonreduced literature):** comparison with ribbons, ropes, primitive multiple schemes, and canonical filtrations.
- **M123.5 (journal object):** v124 has one principal referee object; v123 remains a historical/evidence companion rather than a competing manuscript.

## Reproducibility

The v124 workflow compiles the principal article and reruns the exact v123 arithmetic checks that support the explicit K3 and corank-two witnesses.  It commits the generated PDF and build receipt back to this branch only.  Historical v123 source files are checked by Git diff and are not rewritten by v124.
