# Round 39 review index

## Primary manuscript

- `ROUND39_REVISION.tex`
- `round39/preamble.tex`
- `round39/introduction.tex`
- `round39/triangular.tex`
- `round39/lattice.tex`
- `round39/filter_memory.tex`
- `round39/infinite_jacobi.tex`
- `round39/preparations_verification.tex`
- `round39/appendix_uniformity.tex`
- `round39/references.tex`

## Principal results

| Result | Source | Purpose |
|---|---|---|
| Uniform nonlinear adaptive quasi-BvM | `round39/triangular.tex`, Theorem `thm:abstract-bvm` | Random realized information, horizon-dependent policies, summable misspecified Hilbert nuisance |
| Relative random-information Laplace principle | `round39/triangular.tex`, Lemma `lem:random-laplace` | Relative unnormalized \(L^1\), tails, and normalization |
| Five-parameter mechanical jet embedding | `round39/lattice.tex`, Theorem `thm:jet-embedding` | Recovers \(c,k,\epsilon,c_b,k_b\) from six durations |
| Balanced-window empirical contrast | `round39/lattice.tex`, Proposition `prop:balanced-contrast` | Removes per-block atomwise exploration lower bound |
| Mechanical quasi-BvM and evidence | `round39/lattice.tex`, Theorem `thm:lattice-bvm` | Five-dimensional posterior approximation |
| Strong dual filter jets | `round39/filter_memory.tex`, Theorem `thm:filter-jets` | Norm differentiability and exponential state forgetting |
| Functional memory posterior | `round39/filter_memory.tex`, Corollary `cor:memory-posterior` | Posterior uncertainty for the entire memory kernel |
| Complete Jacobi reconstruction | `round39/infinite_jacobi.tex`, Theorem `thm:jacobi-reconstruction` | Recovers all \(a_j,b_j\) from one boundary response |
| Infinite-sequence posterior consistency | `round39/infinite_jacobi.tex`, Theorem `thm:jacobi-consistency` | Genuine infinite-dimensional inference in product topology |
| Finite-preparation mixture | `round39/preparations_verification.tex`, Theorem `thm:preparation-mixture` | Precisely specified latent finite mixture |

## Response and audit files

- `AUTHOR_RESPONSE_ROUND38.md`
- `round39/PROOF_LEDGER.json`
- `round39/HISTORICAL_REUSE.md`
- `round39/SOURCE_MANIFEST.json`
- `ROUND39_LOCAL_VERIFICATION.json`

## Executable checks

- `tools/verify_round39.py`
- `tests/test_round39.py`
- `.github/workflows/verify-round39.yml`

The executable checks finite algebra, source integrity, and the document build. They do not constitute formal verification of the analytic proofs.
