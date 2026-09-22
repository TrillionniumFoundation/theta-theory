# General Theta Foundations I — seventh structural revision

**Author:** Qian Qi. **Date:** 22 September 2026.
**Canonical article:** [paper.pdf](papers/GTF-I-v7-structural/paper.pdf), 19 pages.
**Complete preserved development:** [complete-development.pdf](papers/GTF-I-v7-structural/complete-development.pdf), 107 pages.

Working branch: `revision/general-theta-foundations-i-v7-structural-2026-09-22`.
The frozen referee branch is created separately after the published artifacts are verified.

This revision answers the latest v6 Markov report at `ff34427b2a5539ad23e2aea5cd57ce9f88d2b627`. It does not repeat the old v4/v5 responses.

## Read this revision

| Material | Location |
|---|---|
| Canonical paper | [paper.pdf](papers/GTF-I-v7-structural/paper.pdf) |
| All preceding mathematical bodies | [complete-development.pdf](papers/GTF-I-v7-structural/complete-development.pdf) |
| Native source | [main.tex](papers/GTF-I-v7-structural/main.tex), [development.tex](papers/GTF-I-v7-structural/development.tex), [README.md](papers/GTF-I-v7-structural/README.md) |
| Point-by-point response | [RESPONSE_TO_REFEREE.md](papers/GTF-I-v7-structural/RESPONSE_TO_REFEREE.md) |
| Proof assumptions and dependencies | [PROOF_LEDGER.md](papers/GTF-I-v7-structural/PROOF_LEDGER.md) |
| Entire-pipeline consultation | [HISTORY_AUDIT.md](papers/GTF-I-v7-structural/HISTORY_AUDIT.md), [HISTORY_INPUT_MANIFEST.json](papers/GTF-I-v7-structural/HISTORY_INPUT_MANIFEST.json) |
| Closest primary literature | [LITERATURE_AUDIT.md](papers/GTF-I-v7-structural/LITERATURE_AUDIT.md) |
| Standalone source archive | [COMPILED_SOURCES.zip](papers/GTF-I-v7-structural/evidence/COMPILED_SOURCES.zip) |
| Executed build | [BUILD_RECEIPT.json](papers/GTF-I-v7-structural/evidence/BUILD_RECEIPT.json) |

## Mathematical revision

Sections 2–3 restore the positive-experiment, predictive-quotient and resource-typed causal-morphism chain. Theorem 4.1 abstracts the energy-tree mechanism with both deletion and continuing-observation insertion realizations. Its applications include the retained Markov-renewal class and a genuinely nonregenerative infinite hidden shift with a sharp finite-state excess-risk law. Section 6 gives a charged Wasserstein-net implementation of a measure-valued filter and a nonlinear example without finite polynomial-moment closure.

Theorem 7.1 proves a matched M^(-2/r) Le Cam approximation law for compact r-dimensional Gaussian shifts, with a lower bound over all experiments having at most M outputs. Theorem 8.1 gives explicit Poisson/Gaussian, covariance, boundary-crossing and positive-reconstruction proofs, yielding N^(-1/2)+J/sqrt(N)+J^(-2). In its joint range this matches M^(-2/r), and attaining N^(-1/5) requires and suffices with order N^(r/10) labels.

All old theorem/proof bodies remain in the complete development. There is one canonical paper, not a second competing principal edition. Both outputs compile from the same core source.

## Source and execution

- Native mathematical source: `968f31ee652dce175002baf09865df38ca9cede7`.
- GitHub Actions run: `35735846202`.
- Canonical PDF SHA-256: `5ed72f6c0ffbf474731454352b21e5dac3df956b4713b3b25732224e2249dc41`.
- Complete-development PDF SHA-256: `0dea799c2e544b34b50f7e0f78138ce2066435c92b1b5b640d8584e709a76bf8`.
- Source archive SHA-256: `ff0a046dd48882716c2e7a916f6df7bfbf2bb2e65e926f66a88acddfb5417329`.
- Archive inputs: 133; retained mathematical labels: 337; shared identically numbered core labels: 72.
- Finite deterministic checks: 48851; ordinary/optimized outputs agree; six negative controls rejected in both modes.
- Inherited v1–v6 diagnostics passed. Both PDFs stabilize in three TeX passes without unresolved references or overfull boxes.
- Exact current source HEAD, controlling review blob, preserved Git trees and additions-only source changes verified.

The publication commit is the commit containing the generated PDFs and this index. Downloaded-artifact and rendering verification is recorded separately after publication. Build evidence is not mathematical proof, independent referee approval or journal acceptance.
