# A2-DYN — revision 8

**Qian Qi, Collision records, arithmetic, and raw local inversion in a triangular Lorentz gas.**

The manuscript entry point is `main.tex`. Build with `bash build.sh`; the complete article is `build/main.pdf`. The exact-SHA workflow publishes that PDF, native TeX logs, recorder file, source archive, source audit, and finite diagnostics as one artifact. The manuscript is not a supplement standing in for the article: it includes all nineteen preceding mathematical source files unchanged, together with two new sections.

## New mathematical results

`core/20_cumulative_returns.tex` proves a uniform cumulative collision-count tail `Pr(N_n>L) <= A exp(an-cL)` from the existing soft-killing theorem. It obtains fixed-strip exponential moments for the entire correlated record and changes the finite-band cutoff from order `n log(V/epsilon)` to `n + log(V/epsilon)`. On exponentially expanding bands this is a linear rather than quadratic physical-count cutoff.

`core/21_common_renewal.tex` constructs the actual induced twists on the common collision probability space, proves the exact damped renewal and Schur-complement identities, and proves a holomorphic `L^p -> L^q` realization on a fixed complex neighborhood with strong parameter continuity. It does not identify this Lebesgue-scale construction with a quasi-compact anisotropic endomorphism.

The endpoint remains the original parameter-uniform **raw four-coordinate mixed-density local limit theorem and its conditioned physical-time consequences**. Neither a smoothed theorem nor a different topic is substituted. The anisotropic phase reconstruction, covariance/cohomology and all-critical/all-singular residual estimates are not claimed proved by this revision. Their exact hypotheses remain visible in the full manuscript.

## Review and version identity

Controlling report: `reviews/a2-dyn-v4-external-top4-review-2026-10-05/REFEREE_REPORT.md`, report commit `a81eb226c013ca062a6901bb472a90668de29eec`, report blob `1af8fb198d0361782cdca21f1d91a81d48ec1300`. The report assessed mathematical v4, although the contemporaneous v5 branch was an alias. The latest v7 head `52278437b6313f1ad5eb53dd95c306f2651f30cb` was a source-preserving checkpoint, retaining the complete v6 mathematics at `ae6511dd5d63f6e12ca3997c5fe3f73357e5415c`.

This v8 is a substantive revision of that latest full source, not a version alias. Its author and referee-copy branches are `revision/a2-dyn-v8-referee-response-2026-10-05` and `revision/a2-dyn-v8-referee-copy-2026-10-05`. The exact commit is recorded by the build receipt and branch heads, avoiding a self-referential source hash.

`RESPONSE_TO_REFEREE.md` answers every numbered request. `PROOF_LEDGER.md` identifies new proofs and their dependencies. `SOURCE_MANIFEST.json` freezes all preserved core and historical diagnostic hashes. Existing papers, revisions, review reports and workflows are not modified.

## Verification scope

The native build and finite-model diagnostics are reproducibility checks, not a formal verification of the continuum theorem or a substitute for independent specialist review. No new external referee acceptance or human review is represented as having occurred. The controlling report itself is explicitly an AI-assisted referee-style assessment.
