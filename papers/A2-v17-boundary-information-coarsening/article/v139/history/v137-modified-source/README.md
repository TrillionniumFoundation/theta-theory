# A2 revision 137

**Intrinsic reconstruction from nonreduced failure schemes** — Qian Qi.

The principal manuscript is `geometry.pdf` (editable driver `geometry.tex`). The technical supplement is `supplement.pdf`; `complete.pdf` compiles all mathematical material. `RESPONSE_TO_REFEREES_V136.md` gives the point-by-point response, `LITERATURE_AUDIT_V137.md` records inspected sources and the unresolved Ballico full-text comparison, and `ISSUE_MATRIX.json` separates documentary from mathematical status.

The branch is `revision/a2-v137-intrinsic-coefficient-torelli-2026-09-23`, based on review commit `d15c9bcabdfc31070b773e2c8014601e75d4e641`. The predecessor manuscript and review directories are not modified. Every inherited mathematical label remains in the compiled complete manuscript; overwritten sources are archived verbatim.

From the repository root run `python revisions/a2-v137/unpack.py`, then `python revisions/a2-v137/assemble.py`, then `bash papers/A2-v17-boundary-information-coarsening/article/v137/build.sh`. The build executes twelve exact scripts, compiles all three PDFs, checks references, source hashes, preservation and page bounds, and writes a source-bound `evidence/BUILD_RECEIPT.json`. General proofs, historical priority and journal acceptance are not machine-certified.

The original four-dimensional smooth-locus theorem is retained. The arbitrary-dimensional component-pair theorem is not misrepresented as the original failure-scheme theorem in every dimension. A separate structural criterion and polar-system family now establish an additional intrinsic failure-scheme reconstruction result for every n >= 2 and d >= 1.
