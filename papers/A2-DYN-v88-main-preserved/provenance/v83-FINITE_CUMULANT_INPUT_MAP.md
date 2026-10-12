# Input map for the fixed-count inner-annulus proof

The two added sections introduce no new billiard-space theorem. Their inputs are the exact statements already in the manuscript.

| Input | Source in the article | Use |
|---|---|---|
| Collision spectral split, uniform powers and C2 multiplication | `lem:collision-spectral-input` | Finite products at each fixed order; the smoothed operator word |
| Mean-preserving BV smoothing | `lem:bv-smoothing` | Supremum and first-variation bounds independent of smoothing; L1 approximation |
| Uniform residual variance | `eq:small-bv-variance` | Removing smoothing from one whole deterministic two-sided interval |
| Analytic smoothed eigenvalue and bounded complex logarithm on radius proportional to delta squared | `lem:smooth-collision-expansion` | Fixed-scale derivative identification and the degree-Q analytic remainder |
| Positive definite collision covariance after sufficiently small smoothing | `thm:joint-uniform-nondegeneracy`, `eq:collision-covariance-limit` | Negative real quadratic part |
| Exact marked chronological product | `eq:marked-chronological-pairing` | A single multiplier between two damped collision powers, including a zero block |
| Genuine marked stopping comparison | `eq:improved-marked-stopping` | Pointwise `M_a(1+abs(v)) n^(-2/9)` cost at the prescribed count |
| Original marked central theorem | `thm:marked-return-band` | Retain the sharper old central rate and splice to the new inner annulus |
| Finite extraction and observed-count support | Sections 40--41 | The exact enlarged-cutoff raw identity and remaining edge/residual terms |

The partition formula for joint cumulants, its independence cancellation, the anchored multiplicity `(m-diameter)_+`, and the spectral derivative limit are established in `core/46_finite_order_damping.tex`. Doring, Jansen and Schubert, *Probability Surveys* 19 (2022), 185--270, DOI 10.1214/22-PS7, is cited only as general cumulant background. No all-order factorial cumulant estimate, unsmoothed analytic twist, induced spectral gap, or Tauberian inference from the spectral Cauchy limit is imported.

The highest specified derivative order is 19; its constants may be large but are fixed. The numerical regressions check finite partition algebra, a two-state Markov spectral identity, and rational margins. They do not verify continuum billiard mixing, eigenvalue bounds, or the complete raw LLT.
