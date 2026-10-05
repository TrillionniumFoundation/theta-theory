# A2-DYN revision 9 — referee response

**Qian Qi, Collision records, arithmetic, and raw local inversion in a triangular Lorentz gas.**

This is the complete revised article, not an addendum standing in for the manuscript. Build `main.tex` in this directory. All 21 mathematical source files of revision 8 remain included. Three new sections establish collision covariance, actual-return Gaussian laws, and functional Gaussian limits. The original mixed-density local-limit problem, physical record, periodic geometry, critical edges, and conditional inversion theorems remain in the article.

## Source-pinned review

The controlling report is `reviews/a2-dyn-v8-external-top4-review-2026-10-05/REFEREE_REPORT.md`, at review commit `9d1904397400529aae4a5d3cccede9081b4dfb33`. It reviews author commit `36427a184ea256f0336fbc431dc76110a9b14592`. This revision descends from the review commit, so both the report and its reviewed source remain in its history.

The delivery branches are `revision/a2-dyn-v9-referee-response-2026-10-05` and `revision/a2-dyn-v9-referee-copy-2026-10-05`. The branch heads, not this document, identify the final commit. No previous manuscript directory or review report is rewritten.

## Reading the new argument

The introductory theorem summarizes the unconditional conclusions. Section labels, rather than numbers that can move during typesetting, identify the main new results:

* `thm:collision-covariance`: absolutely and uniformly convergent collision Green–Kubo matrix, continuous in the radius.
* `thm:actual-record-gaussian`: the actual return record has a uniform central characteristic-function error bounded by `C_K n^(-1/26) sqrt(log(2+n))`.
* `thm:gaussian-kernel-coboundary`: its Gaussian kernel is exactly the space of actual induced `L^2` coboundary directions.
* `thm:collision-functional`, `thm:actual-return-functional`, and `cor:physical-functional-gaussian`: uniform functional Gaussian limits, including unconditioned physical-time displacement and collision-count fluctuations.

The covariance matrices are proved continuous and positive semidefinite. Periodic regularity needed to prove positive definiteness is not assumed silently. Neither these weak limits nor the finite source checks establish the raw or weighted density LLT; its high-frequency and all-branch estimates remain explicitly separated.

## Build and verification

From the repository root:

```sh
bash papers/A2-DYN-v9-referee-response/build.sh
```

The script checks source preservation and exact finite identities in both normal and optimized Python modes, runs the six retained finite diagnostics, and compiles native LaTeX until references stabilize. Warnings, undefined references, and overfull/underfull boxes fail the build. Output is `build/main.pdf`; source-bound records are in `evidence/`.

The scoped workflow `.github/workflows/a2-dyn-v9-qualification.yml` builds the exact event SHA and archives the PDF, log, source tar, and evidence. `VALIDATION.md` records the local outcome; the workflow conclusion must be checked separately on the actual remote SHA.

`RESPONSE_TO_REFEREE.md` answers every substantive request and all ten presentation comments. `PROOF_LEDGER.md` separates proved statements from additional raw-density requirements. `COLLISION_INPUT_MAP.md` records the precise scope of the imported collision theory. The diagnostics are not continuum proof certificates or an independent specialist report.
