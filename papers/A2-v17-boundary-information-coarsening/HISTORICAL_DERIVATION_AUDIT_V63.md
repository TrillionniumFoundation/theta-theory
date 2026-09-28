# Historical derivation audit — A2 revision 63

## Frozen route and coverage

The starting point is the v62 review head `a568573d1d4a5d976f6db3c54122d97c769acd38`, containing the complete reviewed source and delivery. The compiled mathematical source is `037c80dc44d8191e6f808591ea0651e813234d06`, manuscript tree `160735632f3977d47dcf708fb2292699ab79fafd`. The 767-file source archive was recovered through native artifact 10427846002. Every frozen file was checked by length, SHA-256 and Git blob identity before editing.

The latest report was read, including its distinction between correctness, observability, computation and significance. The following historical route was then followed in the actual source. This is a scoped derivation audit for the revision, not a new proof certificate for every page or every earlier branch.

| Source | Derivation inspected and use in this revision |
|---|---|
| `v4/10_boundary_layers.tex`, relative theorem and determinant argument | Two-ended gluing, trace-class perturbation and relative normalization of mixed endpoint derivatives. The normalization precedes the law; the odds ratio alone is not the main dynamical theorem. |
| `v3/20_integration.tex`, physical phase normalization | First-impact flux and residual-time integration, as retained in the finite success-mass formula. Independent preparations and selected channel events are not replaced by a stationary single-orbit sample. |
| `article/23a_signed_endpoint_rigidity_v27.tex`, weighted inverse and finite-envelope/remainder sections | Stationarity removes interior orbit variations, the terminal variation vanishes, and a summable functional remainder bound establishes finite smooth jet factorization. This is not a formal-series substitution. |
| `article/23a2_analytic_contact_inverse_v59.tex`, full inverse construction | The finite lower block and the contracted-evaluation tail are both controlled. The contribution discussion does not identify a diagonal coefficient calculation with the full analytic inverse. |
| `article/23a3_conditional_observation_inverse_v60.tex`, real-observation stability | The outer prior, protected radius and inner output disc are fixed in advance; gap/action inversion and the scalar anchor are used before analytic continuation. |
| `article/23f_single_offset_law_inverse_v42.tex` | Four-density cancellation extracts action from a realizable limiting law. Finite-bridge densities are compared to that law, not presumed to have its exact factorization. |
| `article/23f2_finite_experiment_analytic_inverse_v62.tex`, entire module | Finite approximation, measurable estimator, confidence balance, calibration perturbation and complete-budget proof. Only the final all-history time paragraph is corrected. |
| `article/25a_common_observables_v25.tex`, pilot grid and cap | The ceiling creates the extra sub-epsilon allowance. The good-history stopping theorem and the all-history programmed grid are distinct. The pilot cap already counts every point. |
| Both manuscript introductions, structural statements, v61/v62 response and dependency ledgers | The comparison is integrated at the existing literature discussion. Global matching, lattice recovery and differential results remain in place and are not assigned a new finite-sample global rate. |

## How the history resolves the present comments

The grid correction is determined by the older physical pilot, not by a new sampling argument. The relative law and smooth-envelope proofs identify the mechanism to compare with orbit-local spectral recovery. The v59/v60 distinction prevents a misleading claim that all real observations stably determine the same-disc analytic norm. The v62 construction provides the finite-experiment consequence already credited by the referee; it is retained rather than rebranded as a new v63 theorem.

Revision 63 adds no abstraction framework and removes no proof module. Modified inherited paths are explicitly authorized by `tools/check_revision_v63.py`; their byte-exact originals are archived in `history/v62-review-baseline/`. The full frozen baseline manifest is retained next to those originals. The two corrected/revised introductions share one literature-comparison module. The five finite-experiment statement bodies remain byte-identical, and every inherited active input remains reachable.

All counts and preservation results are source-level checks. They do not establish exceptional significance, authenticate authorship or substitute for a mathematical referee's judgment. The new source and native delivery are identified by their actual commits in the review-ready guide, rather than by anticipated workflow products.
