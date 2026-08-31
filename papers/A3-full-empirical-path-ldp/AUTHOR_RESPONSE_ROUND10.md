# Author Response — Round Ten

**Referee report:** `REFEREE_REPORT_ROUND9_GPT56_PRO.md`  
**Registered controlling source:** `revision/round10-referee-final/A3_DETERMINISTIC_SPEED_PROJECTIVE_FLOW_LDP.tex`  
**Policy:** positive reconstruction; no headline theorem is replaced by a no-go statement, paper deletion, or silent scope downgrade.

## Blocker-to-proof map

| Referee blocker | Positive reconstruction | Controlling labels |
|---|---|---|
| Random total return time used as LDP speed | Use deterministic block count N for the induced LDP and deterministic collision/physical horizons after clock contraction. | `thm:r10-a3-finite; thm:r10-a3-main` |
| State did not retain branch/edge information | Retain vertices, admissible edge flow, return/roof marks, and actual excursion profiles. | `lem:r10-a3-state` |
| Projective rate and compactness unproved | Build finite-core Markov rates, exponential tightness, and the projective supremum rate. | `thm:r10-a3-finite; thm:r10-a3-projective` |
| Recession functional defined circularly | Define it by actual long-excursion epigraph limits and prove liminf plus legal recovery. | `thm:r10-a3-recession` |
| Clock inversion discarded terminal excursion | Retain the terminal profile and quantify its sublinear effect. | `lem:r10-a3-clock` |

## Verification boundary

The response identifies the exact proof locations and the regression mechanism used by the repository verifier.  Compilation and internal hostile checks are reproducibility gates, not substitutes for independent external mathematical review.
