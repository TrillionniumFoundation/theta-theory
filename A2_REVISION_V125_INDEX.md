# A2 Revision 125 index

**Branch:** revision/a2-v125-stratified-nilpotent-contact-boundary-2026-09-23  
**Controlling review:** review/a2-v124-independent-harsh-top4-2026-09-23  
**Principal source:** papers/A2-v17-boundary-information-coarsening/article/v125/geometry.tex  
**Referee response:** papers/A2-v17-boundary-information-coarsening/article/v125/RESPONSE_TO_REFEREE_V124.md

Revision 125 is a new referee-facing branch. It does not edit the reviewed v124 source or the inherited v123 proof blocks.

## Principal mathematical changes

1. **Whole-Grassmannian residual-colon structure.** Theorem thm:global-residual-colon proves, at every projection corank and rank-drop point,
\[
 \operatorname{Ann}(N^j)
 =
 (\mathcal J^{\mathrm{res}}:\mathcal I_\Delta^{j-1})/
 \mathcal I_{\widehat D},
\]
and identifies every graded piece
\[
 N^j/N^{j+1}
 \simeq
 \mathcal L^{\otimes j}\otimes\mathcal O_{W_j}.
\]

2. **Complete mixed-regular contact specialization.**
\[
 J=I_H\cap\mathfrak m^3,\qquad
 \mathcal I_{\widehat D}=\delta I_H\cap\mathfrak m^5.
\]
The \(\mathfrak m^5\) component is genuinely primary throughout collisions, and a multiplicity-\(e\) contact has generic primary type
\[
 (\delta^2,\delta q^e,q^{e+1}).
\]

3. **Simultaneous first two nilpotent layers.**
\[
 N/N^2\simeq P/I_H,\qquad N^2\simeq P/\mathfrak m.
\]
This gives the associated-graded specialization from ramification support to contact cone and rank-two Schubert support.

4. **Containment locus.** For \(h_H\equiv0\),
\[
 \mathcal I_{\widehat D}=\delta^2\mathfrak m
 =(\delta^2)\cap\mathfrak m^5.
\]
The containment locus is the finite reduced Fano scheme \(F_1(Y_R)\).

5. **First non-mixed-regular wall.** At a transverse decomposable one-dimensional mixed kernel,
\[
 Z_2=V(c,d,a^2,ab,b^2),
\]
a length-three nonreduced vertex thickening.

6. **Inverse problem.** The generic web quotient to the polarized-K3 image is identified on dense opens as a finite étale cover of constant function-field degree with transitive geometric monodromy.

7. **Classical parameter bridge.** The regular web Grassmannian is connected explicitly to the Reye Hilbert component and its tangent quotient.

## Principal files

- geometry.tex — sole principal article driver.
- frontmatter.tex — revision-125 title and abstract.
- parts/01-introduction.tex — headline theorems and exact scope.
- parts/04-depth.tex — intrinsic annihilator filtration.
- parts/08-corank-boundary.tex — projection-rank presentation and corrected contact incidence.
- parts/09-stratified-nilpotent.tex — global residual-colon theorem, collision primary law, containment and decomposable-kernel wall.
- parts/10-reye-priority.tex — web/Hilbert bridge and finite étale Torelli monodromy.
- RESPONSE_TO_REFEREE_V124.md — issue-by-issue response.
- ISSUE_MATRIX.json — machine-readable closure map.
- LITERATURE_AUDIT.md — source-access and priority audit.
- checks/stratified_rank_two.py — deterministic symbolic regression for the new boundary identities.
- build.sh, verify_build.py — source-bound referee build.

## Preserved proof blocks

Unchanged core proofs are included from v123 by geometry.tex and remain byte-identical to the controlling review branch. This preserves the full reconstruction, moduli, original corank-two, weighted-determinantal and certificate arguments rather than abridging them.

## Build

The branch-scoped GitHub Actions workflow runs the exact K3 witness, the split corank-two regression, the new stratified rank-two regression, three LaTeX passes, reference/citation checks, and PDF rendering sanity checks. Generated geometry.pdf and evidence receipts are committed back to this revision branch with the source commit recorded.
