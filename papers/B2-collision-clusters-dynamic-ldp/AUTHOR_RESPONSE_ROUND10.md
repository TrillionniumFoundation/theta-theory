# Author Response — Round Ten

**Referee report:** `REFEREE_REPORT_ROUND9_GPT56_PRO.md`  
**Registered controlling source:** `revision/round10-referee-final/B2_COMPATIBLE_TRACE_INTEGRATED_JACOBI_LDP.tex`  
**Policy:** positive reconstruction; no headline theorem is replaced by a no-go statement, paper deletion, or silent scope downgrade.

## Blocker-to-proof map

| Referee blocker | Positive reconstruction | Controlling labels |
|---|---|---|
| Interior/boundary measures were independent and incompatible | Define the closed graph of the kinetic transport operator with its normal trace and Green identity. | `thm:r10-b2-trace` |
| Trace hierarchy semigroup unconstructed | Build the positive boundary-renewal semigroup on the factorial graph product. | `prop:r10-b2-renewal` |
| QR reset hid physical singular values | Remove QR reset and prove an integrated flux-weighted small-singular-value estimate for the true Jacobi map. | `lem:r10-b2-jacobi; thm:r10-b2-surplus` |
| Future deleted after surplus contact | Keep the true post-collisional future and sum all later contacts by the renewal semigroup. | `thm:r10-b2-surplus` |
| One-block source theorem asserted | Compare the exact and Boltzmann renewal Duhamel expansions with explicit tree/cycle/multiple-event errors and mesh consistency. | `thm:r10-b2-block` |
| Balance-preserving smoothing absent | Use conservative shell retraction, positive background, finite-cell incidence repair, and exact weak balance. | `lem:r10-b2-repair` |
| Full lower bound incomplete | Expose smooth positive balanced pairs and pass to all finite-action pairs through the conservative recovery. | `thm:r10-b2-main` |

## Verification boundary

The response identifies the exact proof locations and the regression mechanism used by the repository verifier.  Compilation and internal hostile checks are reproducibility gates, not substitutes for independent external mathematical review.
