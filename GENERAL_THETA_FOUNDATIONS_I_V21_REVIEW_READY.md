# General Theta Foundations I — v21 referee package

**Multicut Continuation Complexity and Stable Causal Certification**

Source commit: `6dafe7b7c2f40902ea506f9509b86b5c1de67c97`. Executed build run: `35929213226`.

Review baseline: `14bcfe767940f8cbd196637049524d0b14eaee19`; reviewed v20 publication: `b488b2f28bec42a555999070759d715678b87db8`.

Canonical English article: **72 pages**. Complete development: **472 pages**, including all **400 predecessor pages** with identical text and raster rendering.

Directory: `papers/GTF-I-v21-multicut-resources/`.

## Referee entry points

- [Full English article](papers/GTF-I-v21-multicut-resources/paper.pdf) and [LaTeX entry point](papers/GTF-I-v21-multicut-resources/main.tex).
- [Point-by-point response](papers/GTF-I-v21-multicut-resources/RESPONSE_TO_REFEREE.md).
- [Complete preserved development](papers/GTF-I-v21-multicut-resources/complete-development.pdf).
- [Executed build receipt](papers/GTF-I-v21-multicut-resources/evidence/BUILD_RECEIPT.json), [theorem locations](papers/GTF-I-v21-multicut-resources/evidence/THEOREM_LOCATIONS.json), and [portable submission sources](papers/GTF-I-v21-multicut-resources/evidence/SUBMISSION_SOURCES.zip).
- [Resource ledger](papers/GTF-I-v21-multicut-resources/RESOURCE_LEDGER.md), [proof status](papers/GTF-I-v21-multicut-resources/PROOF_STATUS.json), [historical audit](papers/GTF-I-v21-multicut-resources/HISTORY_AUDIT.md), and [literature crosswalk](papers/GTF-I-v21-multicut-resources/LITERATURE_CROSSWALK.md).

## Main revision

The revision develops the referee's general multicut route rather than reducing the original program. For a fixed finite alphabet of size d, strict decision-continuation complexity kappa and full-trial peak width W satisfy kappa <= W <= W_rational <= 12*d*kappa in the explicitly clocked model. Training, random-bit generation, decision, and validation cuts are included; the training length, read-only precision, and autonomous clock multiplier are separately priced. Approximate causal realization and feedback-stable resource transfer, shared-capacity multicut residual bounds, dimension-growing examples, and confidence-level tests are proved in the article.

For the same positive-noise collision experiment, the exact three-state decision-cut result is preserved. A new full-trial twelve-state construction gives 3 <= W_physical <= 12. It uses much longer but explicitly finite training; it is not an exact peak optimum or a matched memory/sample frontier. The original 399-training-reset construction remains in full as an alternative resource regime.

The source-preserving transport estimate has no training multiplier only when training preparations are unchanged. Perturbed training laws receive their explicit accumulated defect. Confidence amplification accounts for every validation pair and counter state.

Executed finite diagnostics: **233,613**, comprising **80,651** new and **152,962** inherited checks. Normal and optimized Python results agree. All **28** negative-control executions were detected. LaTeX has no undefined references or overfull boxes.

The original Norberg proof-level crosswalk remains incomplete because the original full proof text was not obtained. The manuscript does not claim the global B4/C2 historical program has been proved or make the independent A2 chain depend on this revision. Analytic proofs are supplied for independent review; successful computation and compilation are not independent mathematical certification or journal acceptance.

No predecessor manuscript, report, or other historical path was modified or deleted by this revision.
