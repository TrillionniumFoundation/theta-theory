# A2 v7 — new complete revision for independent referee review

**Branch:** `revision/a2-v7-sharp-physical-experiments-2026-09-09`  
**Paper:** Relative Boundary Laws and Statistical Reconstruction in Periodic Dispersing Billiards  
**Author:** Qian Qi  
**Date:** September 9, 2026

This revision responds to the latest A2 v6 referee memorandum pinned at `f1728f5d96ea01b1326daf9a6a36352b2e270be1`, reviewing the actual complete submission `4ca186258c92dcbc75accc4eb576e307cc612189`.

## Referee reading entry points

1. [Complete integrated manuscript source](papers/A2-v7-sharp-physical-experiments/main.tex) and [compiled manuscript](papers/A2-v7-sharp-physical-experiments/build/main.pdf).
2. [Point-by-point response to V6-R1–V6-R4](papers/A2-v7-sharp-physical-experiments/RESPONSE_TO_REFEREE_V7.md).
3. [New theorem and proof ledger](papers/A2-v7-sharp-physical-experiments/PROOF_LEDGER_V7.md).
4. [Complete unchanged two-collision companion](papers/A2-v7-sharp-physical-experiments/two_collision.tex) and [compiled companion](papers/A2-v7-sharp-physical-experiments/build/two_collision.pdf).
5. [Source pins](papers/A2-v7-sharp-physical-experiments/SOURCE_PINS_V7.json), [reproduction instructions](papers/A2-v7-sharp-physical-experiments/README.md), and [actual build evidence](papers/A2-v7-sharp-physical-experiments/verification-v7/BUILD_V7.json).
6. [The source-pinned referee report](reviews/a2-v6-relative-transfer-harsh-independent-2026-09-09/REFEREE_REPORT.md).

The PDF/evidence links become populated only by the successful branch-scoped build; the source manuscript and response are materialized in this commit independently of that build. A source-only or failed-build state must not be represented as a completed PDF validation.

## Main additions

- A precise four-experiment map states observations, supplied information, estimands, error topologies, preparation costs, and uniformity variables.
- The attributed exact moving-support tangent calculation is proved and extended, using uniform nonlinear remainder estimates, to a sharp positive-offset experiment-size transition.
- A finite-offset, adaptive-stopped Bernoulli lower bound includes the confidence logarithm and matches the retained calibrated upper order at every fixed extrapolation order within the stated design.
- An exact Borel tie-breaking construction defines all compact minimum-discrepancy estimators while retaining the original error constants.

The entire reviewed source tree, every previously active mathematical body input, all bibliography entries, historical drafts, and the complete companion are preserved. The new article adopts an author–year, observation–identification–risk–cost exposition and a 12-point, 1.5-spaced, 1.25-inch-margin layout. It is a complete referee version, not a claim of formal journal page-limit compliance or acceptance.

This branch is a handoff for independent review. It does not merge, modify, or replace `main`, the source v6 revision, or the latest review branch. Diagnostics, compilation, and mathematical correctness are separate evidence categories.
