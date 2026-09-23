# A2 revision 138 — natural pencil reconstruction

**Intrinsic reconstruction from nonreduced failure schemes**, Qian Qi, 23 September 2026.

Branch: `revision/a2-v138-natural-pencil-reconstruction-2026-09-23`.

Controlling review: `review/a2-v137-independent-harsh-top4-2026-09-23`, commit `ba24a0b2d062897ee2d7a6b02add81c504fe0e71`. The new branch starts at that immutable review, preserving the reviewed manuscript and the report.

## Referee reading objects

Directory: `papers/A2-v17-boundary-information-coarsening/article/v138/`.

- [Principal article — geometry.pdf](papers/A2-v17-boundary-information-coarsening/article/v138/geometry.pdf), with editable `geometry.tex` and `parts/`.
- [Technical supplement — supplement.pdf](papers/A2-v17-boundary-information-coarsening/article/v138/supplement.pdf).
- [Complete mathematics — complete.pdf](papers/A2-v17-boundary-information-coarsening/article/v138/complete.pdf).
- [Point-by-point response](papers/A2-v17-boundary-information-coarsening/article/v138/RESPONSE_TO_REFEREES_V137.md).
- [Primary-source comparison](papers/A2-v17-boundary-information-coarsening/article/v138/LITERATURE_AUDIT_V138.md) and [issue matrix](papers/A2-v17-boundary-information-coarsening/article/v138/ISSUE_MATRIX.json).
- [Source-bound build receipt](papers/A2-v17-boundary-information-coarsening/article/v138/evidence/BUILD_RECEIPT.json).

The native reading objects are published by the branch's build; source transport alone is not a claim that the remote PDFs already exist.

## New mathematics

The original multiplication-failure construction now has an automatic intrinsic coefficient theorem on the whole Grassmannian range `R in Gr(r,Sym^2 V)`, `dim V=n>=3`, `1<=r<n(n+1)/2-n`. Its two-relation specialization reconstructs every quadratic pencil, including nonregular and singular pencils, from the abstract nonreduced scheme. All reduced failure schemes remain a fixed Schubert divisor.

The pencil theorem recovers root-labelled elementary divisors; explicit pencils with the same full discriminant but different Jordan partitions have nonisomorphic failure schemes. For `n=2g+2`, the simple-discriminant locus gives a fixed-reduction invariant of a `(2g-1)`-dimensional family of hyperelliptic curve classes, using the classical pencil correspondence. The classical classifications and invariant-theory inputs are explicitly attributed.

The full smooth-web theorem is retained without extra genericity. The polar-system theorem and all boundary mathematics remain. All 292 predecessor mathematical labels are preserved; the current compilation has 310. Modified predecessor sources are archived verbatim under `history/v137-modified-source/`; the v137 directory and every review remain untouched.

## Execution and publication

Local preflight completed: principal article 42 pages, supplement 66 pages, complete manuscript 105 pages; all thirteen exact scripts and the source/label/reference/layout checks passed. This is finite reproducibility and build evidence, not machine certification of the general proofs.

<!-- REMOTE_BUILD_START -->
Remote build completed successfully: [GitHub Actions run](https://github.com/TrillionniumFoundation/theta-theory/actions/runs/35846673709).

Source commit: `b4448e6735457100b884d05977354d995bf88a70`.

PDF pages: geometry 42, supplement 66, complete 105. Thirteen exact scripts, 292 inherited mathematical labels, source hashes, references, page bounds and absence of overfull boxes passed. Structural proofs and historical priority are not machine-certified.
<!-- REMOTE_BUILD_END -->

The complete Ballico 1993 article was not obtained; its requested theorem-level comparison remains documentary-open. No historical nonanticipation or journal acceptance is certified.
