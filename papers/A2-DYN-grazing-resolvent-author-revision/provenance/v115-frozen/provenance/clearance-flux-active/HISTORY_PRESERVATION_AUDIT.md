# Historical preservation and retrieval boundary

## Byte-verified preservation

The completed author CI archive was downloaded and verified against its reported SHA256. Its complete active source tar was extracted without editing. Every extracted active-packet file is copied unchanged into `provenance/v112-active`, and its SHA256 is checked by `tools/check_manifest.py`.

The current active manuscript additionally retains all ten original `core/260*` through `core/269*` proof bodies, `model.tex`, `inputs.tex` and `comparison-scope.tex` byte-for-byte. The new work is four additional proof modules, an audit appendix, a revised introduction/abstract, source/response/evidence records and local build tools. The original main file, original response, original tools, original evidence and original 31-page PDF remain in the frozen active copy.

The old v109–111 reports, their main files and the historical proof anchors 238/239/241 that were present in the completed artifact are also retained unchanged. Source identities and all available failed/finite-run evidence in that artifact are preserved rather than filtered for successful results.

## Remote source pinning, not local full reconstruction

The source archive supplied by completed CI deliberately excluded `archive/`. The full recursive revision-111 packet remains identified by tree `790e627efe3a89a4549123d7e9acacf24089c287` in the original repository. The new v113 source-export branch at `3d91709d12db4a292f212d07304ff036f594d892` has no downloadable artifact in the checked run 38721146248. It is not a complete mathematical manuscript and is not used as the scientific baseline.

The controlling v112 report was read through all three contiguous ranges 1–249, 250–510, 511–738. Its immutable report blob is `0ad9f500c92db32ea4fc9f6d9ee28630b4484699`. Its full native Markdown bytes were not materialized into this runtime; the original remote report is not edited. The detailed response indexes every report section and every explicitly enumerated required/minor item.

Branch-name discovery covered the A2/DYN-named branch collection, including author/copy/review and the later exporter. This is not a claim that every older branch head, every historical manuscript, every run log, every binary result or every nonstandard publication branch was fully fetched and independently reconstructed. No A2 geometry favorable review is used as A2-DYN evidence. No General Theta Foundations I source or companion paper is modified.

## Execution / publishing boundary

No remote content was written in this session. The available GitHub connection provided reads and artifact download, but no exposed write action; the local Git transport failed at DNS resolution for github.com. A new local delivery branch and additive patch are supplied separately. A local delivery commit is not represented as a descendant of the real GitHub baseline unless applied with the provided guarded worktree script in a checkout that contains that baseline.

The guarded application route creates a new branch from the immutable controlling-review commit, adds only `papers/A2-DYN-clearance-flux-2026-10-15/`, and verifies the allowlist. It does not rewrite an existing author/review branch, default branch, companion, or historical path. Its remote execution is not reported as completed.
