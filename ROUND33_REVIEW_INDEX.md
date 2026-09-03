# Round 33 review entry

Controlling report commit: `e037717914a34fe7c0636743b3f5c645969bcb20`.

The canonical `papers/*/main.tex` files import only their `ROUND33_REVISION.tex` wrapper. Each wrapper imports the common preamble and one source under `round33/chapters/`. Older rounds remain historical, not active proof inputs.

| Node | Active source | Principal proved contribution |
|---|---|---|
| A1 | `round33/chapters/A1.tex` | Strong shell response, ancestry, Hilbert martingale limit, same-level covariance |
| A2 | `round33/chapters/A2.tex` | Large-frequency arithmetic and integrated Fourier budget |
| A3 | `round33/chapters/A3.tex` | Exact marked-edge divergence and stopped transition entropy |
| A4 | `round33/chapters/A4.tex` | Valid generation, domain-safe compression, fourth-order memory remainder |
| B1 | `round33/chapters/B1.tex` | Exact Gaussian momentum-energy anchors and explicit smoothing order |
| B2 | `round33/chapters/B2.tex` | Integrable analytic-scale evolution, endpoint control, uniqueness and stability |
| B3 | `round33/chapters/B3.tex` | Finite-grid tightness implication and static contact Mosco limit |
| B4 | `round33/chapters/B4.tex` | Exact attainable energy closure and sufficient path compactness criterion |
| C1 | `round33/chapters/C1.tex` | Complete cylinder-dual construction and exact adaptive diagnostic model |
| C2 | `round33/chapters/C2.tex` | Strict duality, correct likelihoods, full-path evidence estimate, fixed-basis BSDE stability |
| D1 | `round33/chapters/D1.tex` | Density normalization, conditional Laplace powers, proved near-maximizer selection |

Read `AUTHOR_RESPONSE_ROUND32.md`, then `ROUND33_PROOF_LEDGER.md`. Every chapter separates original mechanical application obligations from the proved construction. The ledger maps all 76 paper-level objections; it does not pretend these obligations have all been discharged.

Build and test: `python3 tools/verify_round33.py --build`.
The command writes 12 PDFs and execution records under `build/` and never edits the source. `build/ROUND33_BUILD_RESULTS.json` records the SHA-256 of the exact source manifest, all PDF hashes, and tool versions. `ROUND33_LOCAL_VERIFICATION.json` records an executed local build, not a claim of remote CI completion.
