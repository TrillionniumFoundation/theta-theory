# Author Response — Round Ten

**Referee report:** `REFEREE_REPORT_ROUND9_GPT56_PRO.md`  
**Registered controlling source:** `revision/round10-referee-final/B3_COVARIANCE_FIRST_GAUGE_PROCESS.tex`  
**Policy:** positive reconstruction; no headline theorem is replaced by a no-go statement, paper deletion, or silent scope downgrade.

## Blocker-to-proof map

| Referee blocker | Positive reconstruction | Controlling labels |
|---|---|---|
| Indefinite perspective Hessian treated as a metric | Acknowledge the sign-indefinite term and prove short-time coercivity directly on the balanced tangent by an energy estimate. | `thm:r10-b3-linear; cor:r10-b3-curvature` |
| False multiplier curvature | No curvature is attributed to the linear balance multiplier; the actual constrained second epi-derivative is used. | `cor:r10-b3-curvature; thm:r10-b3-mosco` |
| Closed range/gauge asserted | Prove backward micro--macro observability in the B2 Green graph and invoke the closed-range theorem. | `thm:r10-b3-gauge` |
| Covariance/action circularity | Construct covariance from exact finite cumulants first, then identify the rate's second epi-derivative by finite-dimensional conjugacy and Mosco passage. | `thm:r10-b3-finite; thm:r10-b3-mosco` |
| Process tightness lacked time-local estimates | Root connected graphs at an anchor time and integrate tree-decaying relative-time cumulant densities. | `lem:r10-b3-cumulants; thm:r10-b3-main` |

## Verification boundary

The response identifies the exact proof locations and the regression mechanism used by the repository verifier.  Compilation and internal hostile checks are reproducibility gates, not substitutes for independent external mathematical review.
