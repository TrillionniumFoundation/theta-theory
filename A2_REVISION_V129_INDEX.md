# A2 revision 129 — flat colon towers and geometric primary stratification

**Branch:** `revision/a2-v129-flat-colon-primary-stratification-2026-09-23`  
**Controlling review:** `review/a2-v128-independent-harsh-top4-2026-09-23`  
**Reviewed manuscript:** `revision/a2-v128-effective-pieri-relative-primary-atlas-2026-09-23`  
**Principal source:** `papers/A2-v17-boundary-information-coarsening/article/v129/geometry.tex`  
**Referee response:** `papers/A2-v17-boundary-information-coarsening/article/v129/RESPONSE_TO_REFEREE_V128.md`

Revision 129 is based directly on the v128 review head. It preserves the reviewed v128 source and referee report and adds a new self-contained referee-facing article tree.

## Main mathematical changes

1. **Correct colon base change.** The false four-term Tor inference is replaced by two short exact sequences. Flattening (A/J) and (A/(J,f^q)) first makes (f^q(A/J)) flat; kernel formation then commutes with arbitrary base change.
2. **Geometric relative-assassin stratification.** The proof now invokes the explicit constructibility theorem Tag 05KR, tracks geometric support packets (allowing geometric splitting), and uses the canonical finite-length torsion module at associated generic points for embedded multiplicity.
3. **Generic support factors over fraction fields.** The ((2,2)) and ((1,3)) rank-drop factors, discriminants, and the length-three generic saturation quotient are computed over the same rational-function fields as the Groebner bases.
4. **Formal corank-four ideal projection.** Right-(GL(V)) stability of the maximal-minor ideal and complete reducibility are inserted before projecting to the one-dimensional ((4,4,4,4)) Cauchy line. The nonzero Pieri coefficient is written with an explicit standard-bitableau product.
5. **Global consequence.** The universal determinant exponent now feeds a general bounded principal-colon primary-stratification theorem. This connects determinant completion to the full intrinsic boundary algebra rather than using it only as a nilpotence bound.
6. **Self-contained submission source.** Every inherited proof file used by the principal article is materialized locally and recorded in `PROVENANCE_MANIFEST.md`; the v129 driver has no cross-version TeX includes.
7. **Evidence scope.** Build receipts distinguish executed scripts, exact algebra checked by scripts, and structural source proofs.

No existing theorem is deleted or weakened.
