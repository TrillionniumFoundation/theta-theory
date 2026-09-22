# General Theta Foundations I — tenth marked-duality revision

**Author:** Qian Qi. **Date:** 23 September 2026.

This is the full English mathematical revision responding to the ninth causal-minimax referee report, commit `e5373d129545b269ee4f5477a94542517dbfd0d1`. The new branch is `revision/general-theta-foundations-i-v10-marked-duality-2026-09-23`. It starts from `04890dfca0b7dc9fca657049fe9700330828ad95`, whose only addition to that review was a build workflow, not a v10 manuscript. Neither that branch, the review branch, the default branch nor another paper's branch is modified.

## Reading entries

[Canonical full article](paper.pdf) ([LaTeX entry](main.tex)); [complete preserved development](complete-development.pdf) ([LaTeX entry](development.tex)); [point-by-point response](RESPONSE_TO_REFEREE.md); [proof ledger](PROOF_LEDGER.md); [literature comparison](LITERATURE_COMPARISON.md); [history audit](HISTORY_AUDIT.md); [pipeline contracts](PIPELINE_DEPENDENCIES.json).

The canonical article contains the new proofs and the complete substantive v9 core. The companion additionally contains the older development and historical introductions. Two local copies make narrowly identified corrections to the v9 presentation: `report-saturation.tex` states precisely the report-only result and points to the stronger marked theorem; `delayed-gaussian.tex` preserves its original proof and adds the formal information pattern. The original v9 files remain unchanged and hash-pinned.

## Principal mathematical additions

Theorem `thm:v10-compact` establishes compact common-encoder duality for standard Borel observations and compact continuously parameterized loss effects. It proves weak-star compactness, uniform risk continuity and measurable implementation of public mixtures; it does not assume compactness of the attainable risk body. Countably many tasks and width-uniform finite-report approximation are treated separately with their correct extremum conventions.

Theorems `thm:v10-minimal` and `thm:v10-reconstruction` characterize the least source-consuming marked continuation state by operational prediction risks and reconstruct the actual joint report–target law. Theorem `thm:v10-synthesis` gives rational output-sensitive synthesis using continuation spaces, without expanding the complete history tree.

The three-task example has exact private/shared errors `1/2` and `2/9`, although each task separately needs only two labels for zero error. The delayed-query Gaussian exponent is retained and supplemented by a finite-precision acquisition/table bound. Positive Gaussian hidden Markov observations, history contraction, nonlinear finite-state semigroups with a proved resolvent range condition, and one-policy latent-phase moment recursion give model-derived consumers.

## Build and evidence

Run `python3 papers/GTF-I-v10-marked-duality/build.py` from any directory in this checkout. It requires Python 3, the inherited verifier dependencies in `requirements.txt`, `pdflatex` and `pdfinfo`. It checks all pinned source hashes, executes normal and optimized diagnostics, rejects designated incorrect variants, reruns the nine predecessor diagnostic suites, and compiles both entries to stable references. Generated evidence is in `evidence/BUILD_RECEIPT.json`, `DIAGNOSTICS.json`, `NEGATIVE_CONTROLS.json`, `PIPELINE_CONTRACT_CHECK.json`, and `COMPILED_SOURCES.zip`.

The source-bound commit is the clean mathematical checkout recorded inside the build receipt. A later publication commit adds PDFs and evidence; these two identities must not be confused. The receipt reports what actually ran. Finite diagnostics, hashes and successful typesetting are not mathematical proof certificates or referee approval.

## Pipeline scope

The new contract records four proved **model-scoped consumers** (A4, C1, B4 and D1), in addition to the two retained protocol adapters. It does not mark the historical unrestricted microscopic targets complete. The current A2 algebraic-geometric primary line is independent of GTF; its operational finite-protocol adapter is a different object. All historical model gates remain recorded, and none is used as an unproved premise of a new theorem.
