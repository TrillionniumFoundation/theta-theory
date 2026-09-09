# A2 v5 proof and scope ledger

This ledger separates theorem proofs, exact finite identities, and non-interval diagnostics. It is not a proof-assistant certificate.

| Result and source label | Hypotheses | Proof inputs and new step |
|---|---|---|
| General threshold `thm:g-stability` | Periodic separated positive-curvature obstacles; compact smooth local family; common small onset collar | Geometric localization, alternating Jacobi reduction, weighted nonlinear bridge, trace-class relative determinant, full-phase residual-time integral. Original proofs retained. |
| Relative limit `thm:v4-factorization`, physical law `thm:v4-law` | Same local channel hypotheses, fixed differentiability order; selected itinerary for a nonminimal chord | Two half-line contractions, summable gluing correction, trace-norm block comparison, common Morse integration. Original proofs retained; derivative operator bounds made explicit. |
| Contact inverse `thm:v5-jets` | Identical even facing graphs; g,kappa positive and supplied or recovered from leading data | Finite-jet induction on stationary equations; top action variation coth(m gamma); trace variation D_m; radial moment assembly. Strictly nonzero triangular diagonal at every fixed order. |
| Analytic boundary corollary `cor:v5-analytic-rigidity` | Real-analytic graph in preceding class; for continuation, connected closed real-analytic boundary and fixed contact frame | Recursive equality of jets gives germ equality. Identity theorem for analytic arclength curvature and planar Frenet equations gives the participating boundary. No stability of noisy analytic continuation is asserted. |
| Physical realization `thm:v5-realization` | Any fixed finite M, small analytic support perturbations of disk on 3Z x 4Z | Area IFT using sin^(2M+2) compensator; support-to-graph diagonal -(2m)!; unchanged horizontal gap and curvatures; openness of clearance. |
| One-flight comparison `prop:v5-one-flight` | Same identical-even class | Empty interior determinant; ellipse moments give nonzero diagonal at every order. This prevents a claim of information exclusively accessible at large j. |
| Pairwise inverse `thm:v5-pairwise` | Fixed g>0; three radii near R>0, area near A0>0; first four absolute count amplitudes | Analytic symmetric contour sum; nonzero four-function Wronskian; IFT in coefficient space; Rouche matching with multiplicity. Area Lipschitz, curvature multiset 1/3-Hölder. |
| Sharpness `thm:v5-sharpness` | Realized equal-gap support family; weighted norm exponent a<gamma_- | Two-sided radius path, uniform third derivative bound polynomial(j) exp(-j gamma_-), nonzero first-amplitude cubic term. Positive upper estimate comes from four amplitudes. |
| Radial inverse `thm:v4-sequence-stability` | Comparison against the circular reference | Original Jensen-gap and whole-sequence quadratic proof retained. Its exponent 1/2 is not a pairwise assertion. |
| Timing `prop:v5-harmonic` | Fixed-order programmed-offset extrapolation | Exact binomial/harmonic identity, uniform variance derivative bound. Nonzero first timing sensitivity is retained. |
| Root calibration `lem:v5-calibration` | Coarse bracket abs(j(g-g0))<=h/4; m+1 positive-offset probabilities; small relative errors | Right Taylor polynomial of d sqrt(F_j(d)); scaled Lagrange interpolation; derivative bounded away from zero. No negative-offset probability is invoked. |
| Joint acquisition `thm:v5-self-calibration` | Independent preparations, coarse bracket, fixed selected patches, fixed m | Negative-binomial concentration; fresh endpoint sample; timing propagation. Safe root/fallback interval ensures positive actual windows even on pilot failure and finite unconditional expected cost. |

## Fixed-order and topology conventions

No constant is asserted uniform as the jet order M or extrapolation order m tends to infinity. The half-line and normalized probability results are uniform in flight number at each fixed order. The inverse sequence norm is an absolute, exponentially weighted norm with a strict margin; it is not relative noise at arbitrarily rare tail coordinates. In the physical three-channel support family, area is constrained by the inherited symmetric identity even though the ambient four-amplitude inverse allows it to be an independent nuisance parameter.

## Exact algebra versus analysis

The Wronskian and diagonal formulas are proved in the manuscript and checked separately by rational symbolic operations. The root matching, analytic continuation, infinite trace-class estimates, whole-sequence remainders, and statistical concentration arguments are written proofs, not conclusions inferred from a finite test prefix. The numerical length integrations are ordinary non-interval diagnostics. The scalar jet and fourth-amplitude statements do not establish an unrestricted mechanical local limit or an equivalence with marked length data.

## Preservation

All proof sources in `v3`, `v4`, and `sections` retain their original tree identities; all their active mathematical conclusions remain in `main.tex`. The new introduction changes organization, not the hypotheses of the general theorems. The companion and historical derivations remain source-pinned. The article and the response letter make different claims: the former states mathematics; the latter explains changes made for re-review.
