# A2 Revision 127 index

**Branch:** revision/a2-v127-determinantal-boundary-atlas-2026-09-23  
**Controlling review:** review/a2-v126-independent-harsh-top4-2026-09-23  
**Parent mathematical revision:** revision/a2-v126-global-nilpotent-specialization-2026-09-23  
**Principal source:** papers/A2-v17-boundary-information-coarsening/article/v127/geometry.tex  
**Referee response:** papers/A2-v17-boundary-information-coarsening/article/v127/RESPONSE_TO_REFEREE_V126.md

Revision 127 is created directly from the latest v126 review branch.
No reviewed source is overwritten. The v123 reconstruction theorem,
v124 intrinsic primary structure, v125 collision/colon geometry, and
v126 normal-cone mechanism remain in history and are imported where
needed.

## New mathematical core

1. **Uniform all-corank depth.**
   \[
   d^5\in J,\qquad \widehat{\mathcal N}_R^6=0.
   \]
   This follows from a \(10\times10\) determinant completion and
   Laplace expansion.

2. **Explicit multiplication law.**
   Every graded multiplication map is the canonical quotient
   \(\mathcal O_{W_i}\otimes\mathcal O_{W_j}\to
   \mathcal O_{W_{i+j}}\), with the Schubert-line twist.

3. **Projection corank two.**
   The \(A_H\)-injective boundary is split into nine mixed-kernel
   orbits, including secant/tangent and the two inequivalent ruling
   families. Exact nilpotency indices and \(W_2,W_3\) Hilbert data
   are computed on coefficient-transverse opens.

4. **\(A_H\)-rank drops.**
   A finite determinant-valuation atlas replaces an unbounded colon
   tower. The lower bound
   \[
   k\ge 6-a-\lfloor b/2\rfloor
   \]
   and \(k\le5\) leave finitely many cases; \((a,b)=(0,3)\) has
   exact index six.

5. **Projection corank three.**
   \(d^3\notin J\), so the exact index is five or six, separated by
   one degree-twelve Macaulay rank condition.

6. **Projection corank four.**
   \[
   d^3\notin J,\qquad d^4\in J.
   \]
   The second statement is the Jacobian-quartic covariant of the web;
   the exact index is five.

7. **Standard DNC is separated from novelty.**
   Fulton section 5.1 and Stacks Tag 062Z are cited for deformation to
   the normal cone; Stacks Tag 052F is cited for flattening.

## Referee reading order

1. frontmatter.tex
2. parts/01b-boundary-atlas.tex
3. inherited v123/v125 structural sections in geometry.tex
4. parts/09b-boundary-atlas-proofs.tex
5. parts/09a-rees-specialization.tex
6. RESPONSE_TO_REFEREE_V126.md
7. evidence/BUILD_RECEIPT.json and
   evidence/BOUNDARY_ATLAS_CERTIFICATES.json

The build and exact regressions are source-bound to this revision
branch.
