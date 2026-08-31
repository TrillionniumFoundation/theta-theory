# Author Response — Round Ten

**Referee report:** `REFEREE_REPORT_ROUND9_GPT56_PRO.md`  
**Registered controlling source:** `revision/round10-referee-final/B1_INTERIOR_SADDLE_REGENERATIVE_SHELL.tex`  
**Policy:** positive reconstruction; no headline theorem is replaced by a no-go statement, paper deletion, or silent scope downgrade.

## Blocker-to-proof map

| Referee blocker | Positive reconstruction | Controlling labels |
|---|---|---|
| Shell theorem covered exponentially rare targets | Restrict to regular interior targets satisfying affine-span and moderate-width conditions. | `cor:r10-b1-saddle; thm:r10-b1-shell` |
| Covariance derived from a fixed rare particle sector | Use linearly many typical insertion cells under the compound law. | `lem:r10-b1-covariance` |
| A local full-rank patch was mistaken for global smoothing | Use linearly many regenerative full-rank blocks; the event of too few good blocks is exponentially small. | `lem:r10-b1-goodblocks` |
| Minor/large Fourier arcs uncontrolled | Decompose into central, lattice minor, regenerative smooth, and exponentially small bad-block sectors. | `thm:r10-b1-characteristic` |
| Fixed source saddle | Center at the exact source-dependent finite-volume saddle and then pass to the limit. | `thm:r10-b1-shell; thm:r10-b1-main` |

## Verification boundary

The response identifies the exact proof locations and the regression mechanism used by the repository verifier.  Compilation and internal hostile checks are reproducibility gates, not substitutes for independent external mathematical review.
