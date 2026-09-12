# A2 v27 — observed-type information and smooth contact jets

**Boundary laws, intrinsic periodic rigidity, and global physical reconstruction in dispersing billiards**  
Qian Qi · Complete English author revision · September 12, 2026

Revision branch: `revision/a2-v27-observed-type-smooth-jets-top4-2026-09-12`.  
Mathematical source commit: `416124f13f182f8e2d876f93090865f13269c86b`.  
Review base: `a5b2d4b5a9ed31059e16e5011c8010579d713598`; reviewed v26 manuscript: `cefd89084682cc2e31d730eab1a4b8d8eaac0bbe`.

[Complete native manuscript](main.tex) · [Point-by-point response to v26](RESPONSE_TO_REFEREE_V27.md) · [Active source and preservation map](ACTIVE_SOURCE_MANIFEST_V27.md) · [Executed checks and remaining native-build requirement](VERIFICATION_V27.md) · [Latest addressed report](../../reviews/a2-v26-external-harsh-top4-2026-09-12/REFEREE_REPORT.md)

## Mathematical revision

The comparison now defines matched endpoint records and proves the exact observed-type dichotomy. For any finite positive number of successful records on an uncountable interval of anchored homotheties, scalar-to-position deficiency is one when the observed endpoints lie on the varying obstacle, with reverse deficiency zero. When both endpoints lie on the fixed facing obstacle, the matched experiments are equivalent. The explicit two-disk counterexample to the old unrestricted statement is retained with a positive-core proof. Residual-time retention is treated only when matched in both records.

The smooth signed-jet inverse now uses finite Taylor expansions and a functional interpolation/envelope lemma. Equal graph jets through degree M give an action difference of order M+1, including arbitrary smooth and flat remainders. The determinant-one all-order recursion, quantitative fixed-order inverse, analytic continuation, intrinsic gluing, metric-free rank-two lattice recovery and global physical reconstruction remain active. A small functional support-preserving example explains why one density carries more information than one support; it is not claimed as a realized global billiard family.

## Source and verification

The stable directory retains its historical v17 name. `main.tex` is the complete current manuscript; `two_collision.tex` is the unchanged companion. All prior mathematical source files and the complete active auxiliary compendium are preserved. The old complete entry page is available as [README_PRE_V27.md](README_PRE_V27.md).

884 finite diagnostics were actually executed in normal and optimized Python with identical output, and the executed script's Git blob matches the repository blob. A changed-source audit and a separately labeled revised-module typesetting fixture were also executed. They are not a full native manuscript build.

**Complete native build remains unverified.** The first v27 Actions job failed before executing any step (`steps=[]`, `runner_id=0`). This is neither compilation success nor evidence of a TeX failure. The exact observations, reproducible full-checkout commands and distinction between proof and diagnostics are in [VERIFICATION_V27.md](VERIFICATION_V27.md).

This is an author revision for further independent review, not a journal decision, and it has not been merged into `main`.
