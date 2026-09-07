# A1 v21 delivery and publication

Controlling review: `078f34222b00797203cdf6dd421eab9f9f428c59`.
Reviewed v20 submission: `6f103ad252d7c65f140720f4095585026f7bb1b9`.
New branch: `revision/a1-english-v21-causal-transfer-and-proof-hierarchy-2026-09-07`.

The five base64 parts carry an XZ-compressed JSON mapping of 18 new or changed source files. This is only the connector delivery format, not the manuscript interface. `materialize.py` verifies both transport checksums, the independently pinned 729-file v20 baseline, and the exact 748-file v21 source manifest. It creates the new directory without replacing any existing revision. The complete English manuscript, response to the referee, historical/proof ledgers and exact diagnostics were written and validated locally before delivery.

The branch-scoped workflow reconstructs readable source under `papers/A1-english-v21`, runs all eleven author suites, reruns the new suite under optimization, tests rejection of an inverse-source mutation, and compiles the full manuscript in three TeX passes. Only after success does `publish.py` commit the readable source, PDF, generated LaTeX inputs and actual receipts to this new branch. It refuses concurrent branch advances and never force-pushes, merges, edits old versions, modifies a review branch or changes repository permissions.

The subsequent publication commit, rather than this transport alone, is the referee-facing delivery. The source manifest SHA256 is `1b75e7bd6613a5c6edbe106c1572378b0cbf63a9c23d0a0d1aca28899a001d05`. Source preservation and finite execution checks do not certify mathematical correctness or journal acceptance. `LOCAL_VISUAL_INSPECTION.json` states the limited visual inspection and image-viewer limitations explicitly.
