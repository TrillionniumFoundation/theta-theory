# General Theta Foundations I — v3 referee edition

**Complete manuscript:** [papers/GTF-I-v3/paper.pdf](papers/GTF-I-v3/paper.pdf), 52 pages.  
**Author:** Qian Qi. **Date:** 22 September 2026.  
**Revision branch:** `revision/general-theta-foundations-i-v3-2026-09-22`  
**Referee snapshot branch:** `revision/general-theta-foundations-i-v3-referee-ready-2026-09-22`

This edition continues the existing v2 referee-ready source, rather than replacing it or rewriting an earlier review branch. The controlling report remains the GTF I v1 report at `01d3e78bd40985651f5b4ff24364e1dba5d481f0`; no later report is invented.

## Start the next referee pass here

| Material | Location and purpose |
|---|---|
| Integrated paper | [paper.pdf](papers/GTF-I-v3/paper.pdf): new principal theorems, retained quantitative development, and full foundational appendices |
| Point-by-point response | [RESPONSE_TO_REFEREE.md](papers/GTF-I-v3/RESPONSE_TO_REFEREE.md): every E1-E5 and M1-M7 objection, plus smaller comments |
| Proof dependencies | [PROOF_LEDGER.md](papers/GTF-I-v3/PROOF_LEDGER.md): assumptions, actual proof work, and mathematical boundaries |
| Entire-pipeline audit | [HISTORY_AUDIT.md](papers/GTF-I-v3/HISTORY_AUDIT.md): all eleven historical components, fixed source editions, and scope of consultation |
| Native TeX and build | [main.tex](papers/GTF-I-v3/main.tex), [README.md](papers/GTF-I-v3/README.md), and [SOURCE_MANIFEST.json](papers/GTF-I-v3/SOURCE_MANIFEST.json) |
| Standalone source package | [COMPILED_SOURCES.zip](papers/GTF-I-v3/evidence/COMPILED_SOURCES.zip): 40 exact repository-relative input files; independently rebuilt after download |
| Executed evidence | [BUILD_RECEIPT.json](papers/GTF-I-v3/evidence/BUILD_RECEIPT.json) and [RENDER_REVIEW.json](papers/GTF-I-v3/evidence/RENDER_REVIEW.json) |

## Principal new mathematical content

| Statement | PDF location | Content |
|---|---|---|
| Theorem 2.1 | p. 6 | A general regenerative future-orbit quantization lower bound for arbitrary randomized, nonstationary M-label causal machines |
| Theorem 3.1; Lemmas 3.2-3.3 | pp. 7-9 | Exact checkpoint risk `1/(12 M^2)` but three sharp causal rates, including the critical logarithm; a matching finite binary-suffix machine charges every persistent state |
| Theorem 4.1 | pp. 9-10 | Exact minimax elimination of unrestricted additive calibration in an actually observed correlated Gaussian pair, for every label budget and bounded loss |
| Theorem 4.2 | pp. 10-11 | Matched statistical-plus-label risk for correlated, nonlinear nonseparable contact observations, with explicit constants and a concrete example |

For the expanding regenerative experiment, with nonacquisition probability q, the causal risk is of order `M^(-2)`, `(1+log M)M^(-2)`, or `M^(-log(1/q)/log 2)` according as q is below, equal to, or above 1/4. The checkpoint distribution is exactly the same in all three regimes. The proof separates acquired geometry from the future information that must survive between acquisitions. Its lower bound is not restricted to interval quantizers, and its upper program does not know q.

The earlier nonuniform causal-resolution theorem is now Theorem 5.1 (p. 13), the every-positive-refresh HMM result is Theorem 6.2 (p. 16), and the unrestricted-control comparison is Theorem 8.1 (p. 20). All v2 quantitative proofs are retained byte for byte in `retained-results.tex`; all first-edition foundations and boundary proofs are retained through the unchanged legacy source. Their 132 mathematical labels resolve. The compiled paper contains 20 theorem, 9 lemma, 15 proposition, 4 corollary, 48 proof, and 13 example environments. These counts describe the manuscript, not its significance.

## Exact source and execution identities

- Mathematical source checkout: `50bf6fdd41ae478adce2b14c5f27af793c5d4da9`.
- Generated native proof/bibliography, PDF and evidence publication: `a4b703201308dca4cd3d09997e731263d4b44413`.
- GitHub Actions run: `35691901705`; all build, diagnostic, source-preservation and publication steps passed.
- PDF SHA-256: `6d8f0d7586c4fcd342f968f356899903b0a2a328ab35664c9e3c1db84b62ae22`.
- Source package SHA-256: `cffdb9e8dbc592c814ba07f98737d48ec96bd936da320b3734baeaea3929e3b3`.

Three TeX passes stabilized all references; there are no unresolved references or overfull boxes. Ordinary and optimized Python diagnostics agree. Negative controls removing the critical logarithm or cross-covariance terms are rejected. Both inherited diagnostic suites passed. All 40 downloaded compilation inputs match the locally authored/inherited bytes. The downloaded archive rebuilt independently, and all 52 local/published page renderings agree pixel for pixel at 72 dpi. Visual inspection of the page overviews and selected full-size pages is recorded separately.

The final snapshot adds only this index and the rendered-page verification record to the publication commit. These are documentation-only additions; they do not change any compiled mathematical input or the published PDF. Compared with the v2 base, all revision paths are new: no prior source file is modified or deleted. Main, the original review branch, and the preceding revision branches are not updated.

The paper is supplied for further mathematical refereeing. The new lower and upper bounds, rather than a build receipt, are the response to the substantive objection. No independent referee approval or four-journal acceptance is claimed.
