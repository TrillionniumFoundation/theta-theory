# A2 Revision 132 — packet descent and intrinsic web reconstruction

**Title:** *Intrinsic web reconstruction and primary boundary laws for multiplication-failure schemes*  
**Author:** Qian Qi  
**Branch:** `revision/a2-v132-galois-descent-higher-residual-2026-09-23`  
**Immutable review base:** `f0ac12d5ce2084fffec3a6245e3cbe8c2e2b39ff`  
**Reviewed manuscript:** v131, `1b3a82d09970ad6545c750733c80ff728a347cd4`.

## Referee-facing documents

- [Complete revision PDF](papers/A2-v17-boundary-information-coarsening/article/v132/geometry.pdf)
- [Self-contained LaTeX entry point](papers/A2-v17-boundary-information-coarsening/article/v132/geometry.tex)
- [Point-by-point response to the controlling report](papers/A2-v17-boundary-information-coarsening/article/v132/RESPONSE_TO_REFEREE_V131.md)
- [Controlling v131 referee report](reviews/a2-v131-independent-harsh-top4-2026-09-23/REFEREE_REPORT.md)
- [Issue dispositions](papers/A2-v17-boundary-information-coarsening/article/v132/ISSUE_MATRIX.json)
- [Actual build receipt and certification scope](papers/A2-v17-boundary-information-coarsening/article/v132/evidence/BUILD_RECEIPT.json)
- [Source provenance and hashes](papers/A2-v17-boundary-information-coarsening/article/v132/PROVENANCE_MANIFEST.json)
- [New exact arithmetic certificates](papers/A2-v17-boundary-information-coarsening/article/v132/evidence/REVISION132_EXACT.json)

## Principal additions

The packet proof now constructs ideals on the original strata. It supplies an explicit Galois descent datum and cocycle, a base-change-exact diagonal intersection sequence, a power-certified construction in arbitrary characteristic, and a downstairs relative torsion module. The accepted split primary models and the original noetherian-base generality are preserved.

The new generic intrinsic reconstruction theorem recovers the original relation web from the abstract full failure scheme, not just its polarized Jacobian K3. The deepest Schubert stratum and its normal cone are intrinsic. Its two global tensor rulings remove transposition, and its degree-sixteen ideal reads both irreducible Pluecker components. Two explicit Pluecker quadrics prove uniqueness on a nonempty invariant open. This separates the generic finite Torelli packet, as requested by the report's inverse-theorem alternative.

The full inherited mathematical body is retained. The locally checked manuscript has 71 pages; the published receipt gives the actual CI result. The build re-executes all six inherited scripts and the new seventh script, including all sixteen matrix-unit equivariance identities and the same independently certified smooth integral witness.

## Scope and remaining requests

The complete higher-corank W3/W4 embedded primary atlas and its complete cross-corank specialization are not claimed. The generic inverse theorem is proved from the actual transverse failure ideal instead. The K3-only map's numerical degree and reconstruction at every exceptional web are not asserted. Ballico 1993 full-text theorem comparison remains a documented open literature item. Written structural proofs remain subject to referee verification; finite symbolic checks are not machine certification of those proofs or a journal acceptance decision.

## Reproduction and preservation

`python revisions/a2-v132/assemble.py` reconstructs the entire article from the immutable reviewed v131 tree plus readable patches and new sections, verifying that transferred sources match the locally checked SHA-256 values. Run `bash papers/A2-v17-boundary-information-coarsening/article/v132/build.sh` after installing the pinned workflow dependencies. The isolated workflow publishes the expanded article, PDF, and actual receipt only on this branch. Historical article directories and all review files remain unchanged.
