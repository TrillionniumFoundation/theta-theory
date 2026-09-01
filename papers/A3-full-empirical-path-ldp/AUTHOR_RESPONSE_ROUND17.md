# A3 response to the Round-Sixteen referee report

The Round-Sixteen candidate was recovered and audited but was not treated as an accepted proof.  The Round-Seventeen manuscript replaces every failed mechanism positively; no theorem is deleted or converted to a no-go statement.

| # | Referee objection | Round-Seventeen proof labels |
|---:|---|---|
| 1 | The controlled-chain lemma uses spectral information that arbitrary predictable kernels do not possess | `thm:r17-a3-entropy`, `thm:r17-a3-relax` |
| 2 | The augmented terminal variable is not automatically the physical stopped path | `lem:r17-a3-terminal`, `thm:r17-a3-collision`, `thm:r17-a3-physical` |
| 3 | Exponential tightness with recession clocks is not proved | `prop:r17-a3-space`, `thm:r17-a3-tight` |
| 4 | The recovery sequence is asserted for a much larger class than is constructed | `thm:r17-a3-relax`, `thm:r17-a3-collision` |
| 5 | The theorem depends on the unproved A2 raw LLT | `thm:r17-a3-main` |

The active `ROUND17_POSITIVE_CLOSURE.tex` is byte-identical to the registered source named in `ROUND17_MATERIALIZATION_MANIFEST.json`.  Build and structural checks are reproducibility gates, not substitutes for independent external mathematical review.
