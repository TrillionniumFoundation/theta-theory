# A1 v7 proof ledger

Labels, rather than page positions, are the controlling anchors. Compiled numbers below refer to the local 28-page principal build. Every entry refers to a written statement and proof, not to an executable test as a substitute.

## New result dependencies

| Result | Source | Essential obligation and supplied argument |
|---|---|---|
| Theorem 5.1, `thm:confluent-law` | `sections/05_confluence.tex` | Full-future inequality `K_m-1 <= n(r-1)` is explicit. Uniform checkpoint bounds use the same physical menu, constant calibration matrix, full-support prior and retained acquisition evidence. Lower applies to streaming; a general streaming upper is not inferred. |
| Lemma 5.2, `lem:confluent-positive` | same | Exponential-polynomial zero counting establishes nonvanishing for complete multiplicity clusters. Confluent Wronskian sign and determinant integration prove strict pairing without assuming a prior density. |
| Lemma 5.3, `lem:observable-scales` | same | Simplex representation controls divided differences and derivatives at collision. Fixed formal product coefficients and Newton interpolation give an injective physical matrix times `diag(theta^nu)`. No unweighted jet norm is substituted for prediction risk. |
| Lemma 5.4, `lem:uniform-patch` | same | A common attainable binomial tuple has surjective normalized jet derivative at positive parameters and directly at zero. Compact row singular bounds and a quantitative inverse construction give a uniform cube. The command density is multiplied by actual all-failure evidence before minorization. |
| Lemma 5.5, `lem:rectangle` | same | Integer subdivisions respect the actual state budget. Projecting onto every initial coordinate block gives the matching maximum of partial-volume scales. This elementary quantization lemma is not claimed as an original general principle. |
| Theorem 7.1, `thm:uniform-streaming` | `sections/07_uniform_resolution.tex` | Stage dimensions are 2, 4, a physical `(1,1,1,1,theta)` box, and 2. Reachable representatives keep updates feasible. All transition and readout derivatives are uniformly bounded in physical coordinates; accumulated errors have no `1/theta` amplification. Lower uses the same fixed exploration protocol. |
| Lemma 7.2, `lem:five-patch` | same | At zero the tangent is all polynomials through degree six, and the confluent future space is `1,t,t^2,t^2 log(t),t^3,t^4`. Strict pairing gives rank six before and five after normalization. The explicit rejection probabilities remain inside the common cube. Compactness works on the entire interval `[0,1/2]`. |
| Corollary 7.3, `cor:uniform-bits` | same | Solve both uniform distortion inequalities, allowing integer rounding. The best all-budget five-dimensional lower constant has order `theta^(2/5)`. No leading distortion constant or exact integer crossover is asserted. |
| Proposition 8.1, `prop:ticket-identity` | `sections/08_sequential_value.tex` | The independent price and query are revealed after encoding. Conditional integration of the binary threshold payoff gives exactly half the same encoder's Brier regret. Randomized decisions cannot improve the conditional optimum. |
| Theorem 8.2, `thm:resolved-value` | same | The erased statistic is exactly the first four physical coordinates. A fixed nonzero weak-query column gives `b_* theta^2 E Var(Z|T)`. The same uniform cube bounds that conditional variance below. The streaming rate then beats even uncompressed `T` at `M >= K theta^(-4)`, with one common payoff and baseline. |

The lower-bound chain is `binomial-tangent -> confluent-positive -> uniform-patch -> rectangle -> confluent-law -> uniform-streaming`. The uniform upper needs the independent additional transition calculation in Section 7. The same-payoff chain then uses `ticket-identity -> conditional-variance minorization -> resolved-value`.

## Retained principal result inventory

All original v6 result labels are present in v7: `thm:main`, `lem:interior`, `prop:tests`, `lem:mixed-moment`, `lem:binomial-tangent`, `thm:rank`, `thm:causal`, `prop:three`, `cor:sparse-example`, `lem:lipschitz`, `thm:stream-upper`, `thm:stream-lower`, `thm:control-bound`, `thm:finite-bit-value`, `cor:threshold`.

The complete transversality and observation-algebra sections are reused byte for byte. The complete mechanical common-risk section is also reused byte for byte. The streaming section changes only the scope wording of “constructive,” retaining its full proofs, evidence accounting, separate control bound and rare-probe/calibration limitations. The introduction preserves the complete exact-law theorem and its equation labels, adding the quantitative synthesis. The experiment section adds the Borel convention.

The previous referee's positive audit remains an audit of the pinned v6 manuscript, not automatic approval of these additions. No old archival proof is silently treated as a new proof of confluence, uniform online error control, or conditional-variance nondegeneracy.

## Priority and validation boundaries

The near-collision family and base-model estimate belong to the v6 technical note. The full sparse binomial tangent was in v6. The general quantization, divided-difference and conditional-variance mechanisms are classical. The claimed additions are the attainable confluent uniform law, its uniform streaming implementation, and the resolved-direction value in the same task.

The current diagnostic suite checks finite exact identities and finite-input machines. It does not certify all priors, every budget, the quantitative inverse argument, randomized minimax quantifiers, journal significance, or exhaustive originality. Those obligations belong to the printed proofs and subsequent review.
