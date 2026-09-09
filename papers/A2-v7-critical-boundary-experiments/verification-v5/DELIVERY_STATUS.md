# A2 v5 delivery and verification status

Date: September 9, 2026.

## Committed manuscript

The complete English native article, its inherited proof chapters and circular appendices, the unchanged two-collision companion, the controlling referee report, the response letter, and the proof ledger are committed under `papers/A2-v5-statistical-contact-rigidity/` on `revision/a2-v5-statistical-contact-rigidity-2026-09-09`.

The mathematical-source commit is `7fd4c925d82a5e8d3942b33354a5a5be4b4bf6d3`; its sole parent is the controlling review commit `ec861ecfcdd83a81880c1a9082becc19b0c76977`. The subsequent commit `45f6a4baed0675916935f4045789f7246c8e0f1c` only fixes Markdown rendering of the coarse-bracket hypothesis in the proof ledger. This status file adds delivery metadata only. None of these changes merges the revision into another branch.

## Checks actually completed

The standalone diagnostic script was executed in the authoring container both normally and under `python -O`. All 175 checks passed in both modes: 136 exact and 39 ordinary floating non-interval. The output files were byte-identical. Their script and result SHA256 digests are recorded in `local_checks_summary.json` and were checked again before delivery. The script's Git blob is `784dfa546b96f4eead9d7be15a72cf3ab016f52d`.

These finite tests include rational Wronskian and Jacobian identities, triangular coefficient assembly, multiplicity-sensitive matching examples, extrapolation identities, and actual nonlinear one-flight length/flux integration. They do not certify the infinite-dimensional or statistical theorems, which require review of the written proofs.

## Full-document build not verified

The branch-scoped, read-only GitHub Actions workflow was triggered for the mathematical-source commit:

- Run: https://github.com/TrillionniumFoundation/theta-theory/actions/runs/34307932167
- Initial build job: `102328406721`, reported failure.
- Retried build job: `102328629446`, also reported failure.
- The retried job's steps endpoint returned an empty steps list. The initial job's log endpoint returned HTTP 404 / BlobNotFound. The available connector did not expose a more specific failure reason.

Accordingly, a successful complete LaTeX build, full-document reference audit, page count, generated PDF, and PDF visual inspection are **not claimed** in this delivery. No PDF artifact is represented as having been produced by that run. The reproduction command remains `python tools-v5/build.py` from the manuscript directory; it is supplied for a working execution environment. The workflow has read-only contents permission and does not push, merge, or change repository settings.

This is an author revision submitted for independent re-review. It is not a journal acceptance, a theorem certificate, or a claim that remote compilation succeeded.
