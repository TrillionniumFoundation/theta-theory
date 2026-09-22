# A2 revision 128 — universal determinant completion and intrinsic primary boundary laws

**Branch:** `revision/a2-v128-effective-pieri-relative-primary-atlas-2026-09-23`  
**Controlling review:** `review/a2-v127-independent-harsh-top4-2026-09-23`  
**Principal source:** `papers/A2-v17-boundary-information-coarsening/article/v128/geometry.tex`  
**Referee response:** `papers/A2-v17-boundary-information-coarsening/article/v128/RESPONSE_TO_REFEREE_V127.md`

Revision 128 is an additive referee-facing branch created directly from the latest v127 review branch.  It leaves all reviewed v127 source and the referee report untouched.

## New mathematical content

- **Universal determinant completion.** For `gamma: Sym^r V -> S`, maximal minors of `gamma Sym^r M` contain `(det M)^{binom(e+r-1,r-1)}`; the exponent is sharp in the universal class.
- **Effective corank-four Pieri step.** Actual bideterminant multiplication, rather than abstract representation occurrence, supplies the nonzero `(4,4,4,4)` projection needed for `d^4 in J`.
- **Generic nine-orbit certification.** Stabilizer slices and exact Groebner bases over rational function fields prove the generic Hilbert table.
- **Complete generic corank-two primary signatures.** All `A_H`-injective mixed-kernel types and every generic `A_H`-rank-drop type have explicit graded supports, associated primes and generic lengths.
- **Relative associated-point theorem.** Colon formation is made base-change compatible before relative assassins are used; embedded/minimal status and generic lengths become constant on a finite refinement.
- **Actual specialization laws.** Explicit one-parameter mixed-kernel orbit closures and a pure-block rank-drop family track the birth of ruling and embedded vertex components.
- **Native referee article.** The introduction, abstract and theorem hierarchy are rewritten for v128 while all prior proof blocks remain available and unchanged.

## Reproducibility

`checks/generic_boundary_atlas.py` performs the new exact stabilizer-rank and rational-function-field Groebner calculations.  The branch workflow runs it together with the inherited K3, corank-two, stratified-rank-two and v127 boundary regressions, then compiles the principal article and publishes a source-bound PDF/evidence receipt on this branch only.

## Documentary boundary

The complete Ballico 1993 text remains outside the verified source corpus.  The revision cites it and keeps the priority claim limited accordingly; this documentary point is not used to weaken any mathematical theorem.
