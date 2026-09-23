# A2 revision 138

Principal article: `geometry.pdf` (editable driver `geometry.tex`). Technical supplement: `supplement.pdf`. Complete mathematical compilation: `complete.pdf`.

Read `RESPONSE_TO_REFEREES_V137.md` for the point-by-point response and `LITERATURE_AUDIT_V138.md` for actual primary-source comparisons. `ISSUE_MATRIX.json` does not mark the unread Ballico 1993 comparison closed.

New proofs: `parts/18-natural-pencils.tex`. Operator comparison: `parts/19-operator-comparison.tex`. The accepted smooth-web theorem is unchanged. All predecessor mathematical labels are retained; modified sources are archived verbatim in `history/v137-modified-source/`.

From the repository root, run `python revisions/a2-v138/unpack.py`, `python revisions/a2-v138/assemble.py`, then `bash papers/A2-v17-boundary-information-coarsening/article/v138/build.sh`. The assembler verifies the immutable v137 source hashes at review commit `ba24a0b2d062897ee2d7a6b02add81c504fe0e71`. It alters only the new revision directory. The build runs all twelve inherited exact scripts plus `revision138_exact.py`, compiles the three PDFs, and emits `evidence/BUILD_RECEIPT.json`.

The receipt certifies executed finite checks and build integrity, not general proofs, historical priority, or journal acceptance. The complete 1993 Ballico article was not obtained in this revision.
