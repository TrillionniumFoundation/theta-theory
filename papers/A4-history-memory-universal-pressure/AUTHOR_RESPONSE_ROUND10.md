# Author Response — Round Ten

**Referee report:** `REFEREE_REPORT_ROUND9_GPT56_PRO.md`  
**Registered controlling source:** `revision/round10-referee-final/A4_DOOB_PAST_KERNEL_MEMORY.tex`  
**Policy:** positive reconstruction; no headline theorem is replaced by a no-go statement, paper deletion, or silent scope downgrade.

## Blocker-to-proof map

| Referee blocker | Positive reconstruction | Controlling labels |
|---|---|---|
| Claimed martingale difference was not centered | Solve the correctly oriented Poisson equation and use g+h_g-P h_g. | `lem:r10-a4-poisson` |
| Stable/future quotient still deterministic | Condition on a genuine past-only natural-extension history and construct its nondegenerate future kernel. | `thm:r10-a4-feller` |
| Conditional rough theorem only asserted | Use uniform conditional moments, Lindeberg, bracket convergence, and singularity-shield truncation. | `thm:r10-a4-quenched` |
| Normalized Feynman--Kac ratio not a semigroup | Normalize by the positive eigenfunction and eigenvalue, producing an exact Doob semigroup. | `thm:r10-a4-doob` |
| Finite descriptor omitted unresolved Q-space / sign issue | Retain the full Q-space and add finite principal-part modes; use Khat=zP-PLP-C(z)^{-1}. | `thm:r10-a4-memory` |

## Verification boundary

The response identifies the exact proof locations and the regression mechanism used by the repository verifier.  Compilation and internal hostile checks are reproducibility gates, not substitutes for independent external mathematical review.
