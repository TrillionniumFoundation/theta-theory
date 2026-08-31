# Author Response — Round Ten

**Referee report:** `REFEREE_REPORT_ROUND9_GPT56_PRO.md`  
**Registered controlling source:** `revision/round10-referee-final/A2_EXPLICIT_CERTIFICATE_FOURIER_RANGES.tex`  
**Policy:** positive reconstruction; no headline theorem is replaced by a no-go statement, paper deletion, or silent scope downgrade.

## Blocker-to-proof map

| Referee blocker | Positive reconstruction | Controlling labels |
|---|---|---|
| Birth bundle undefined across the no-branch side | Use one-sided physical coefficients and a renormalized fold chart; no inverse of a vanishing current is asserted. | `lem:r10-a2-birth` |
| Moving-billiard spectral theorem only sketched | State one uniform graph theorem with expansion, distortion, multiplier, compactness, and trace-mode exclusion on the renormalized bundle. | `thm:r10-a2-spectral` |
| Arithmetic determinant not computed | List triangular/rhombic certificates and verify the determinant with a checked lower bound on the parameter interval. | `lem:r10-a2-arithmetic; A2_ROUND10_CERTIFICATE.json` |
| UNI inferred from a picture | Construct two returned inverse branches on a common interval and compute the temporal-distance derivative including moving endpoints. | `thm:r10-a2-uni` |
| Dolgopyat tail not Fourier integrable | Split compact, Gaussian, Dolgopyat, and very-high-frequency ranges; the last uses enough roof derivatives for an integrable tail. | `thm:r10-a2-four-range` |
| Sharp-window formula exceeds central LLT | Prove a density LLT and state local/central/saturated/macroscopic regimes separately with the correct sum-window factor. | `thm:r10-a2-llt` |

## Verification boundary

The response identifies the exact proof locations and the regression mechanism used by the repository verifier.  Compilation and internal hostile checks are reproducibility gates, not substitutes for independent external mathematical review.
