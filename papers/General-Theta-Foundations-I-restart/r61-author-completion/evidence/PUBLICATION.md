# Source-bound author revision publication

The complete mathematical source commit is `cdea98184278c95c29ae0898d9424487e187491e`, whose repository tree is `8923ec06b40764bc5822fdf0c14015875b4916cc`. Its paper subtree is `bd8f10420b8e67b7234807b66ac85ba0c7ba4a16`. The local native build was performed from exactly those paper bytes, verified by recomputing the complete Git blob/tree identity; the local directory was not a Git checkout.

The enclosing delivery commit adds only this publication note and `LOCAL_BUILD_RECEIPT.json` to that source commit. These post-build delivery records are intentionally outside the mathematical source manifest. This avoids claiming that a receipt knows its own future commit SHA. The current manuscript, supplement, retained sources, bibliography, diagnostics and build program are unchanged between source and delivery.

The native build produced the complete 57-page main article, 5-page current supplement and 37-page retained companion. Their hashes and the actual 388 finite diagnostic checks appear in the adjacent receipt. The full logs, recorder files, source, PDFs, historical text corpus and scan indices accompany the downloadable review package supplied with this revision.

For independent review, read `../main.tex`, `../supplement.tex`, `../RESPONSE_TO_REFEREE.md`, `../THEOREM_MAP.md` and `../PRESERVATION_MAP.md`. The original R56 report and the full retained mathematical companion remain in the source packet. Run `python3 verify.py --out /tmp/theta-r61-independent --source-commit <checked-out-SHA>` from the paper directory to rebuild. The verifier checks actual checkout HEAD when Git is available.

An isolated read-only GitHub workflow is supplied for the new author-completion branch. A queued, absent or failed run is not a successful independent rebuild. Its actual run must name the tested SHA; no preceding R59 success is attributed to R61. Native builds and finite examples do not certify formal correctness, independent human approval, priority or top-four editorial acceptance.
