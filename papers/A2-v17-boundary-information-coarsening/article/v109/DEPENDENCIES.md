# A2 v109 dependency and preservation map

## Principal dependency chain

| Result | Inputs actually used | Not used |
|---|---|---|
| Lemma 2.1: normal second jet | One embedded smooth germ; positive metric; local minimizing projection | Full conormal bundle; global phase retrieval |
| Theorem 2.2: complete partial-contact fibre | Lemma 2.1; known J; Hankel/moment duality | Quadratic parametrization; determinant discriminant |
| Proposition 3.1: native moment coordinates | Calibrated binary law; square rational score interpolation; nuisance Schur complement | Arbitrarily prescribed target metric |
| Theorem 3.2: all-dimensional native one-point realization | Proposition 3.1; sign pattern of J; explicit exponent set S; generic single-fibre separation; Theorem 2.2 | Injectivity on Sym_d; complete conormal observation; endpoint QE |
| Theorem 4.1: stable jet inversion | Full product rank; positive block bounds; least singular value gamma | Unspecified invariant numerical norms |
| Theorem 4.2: finite-offset noisy observations | Uniform analytic projection; finite contact locations; exact Gaussian mean; Theorem 4.1 conditioning | Exact derivative oracle; raw categorical sample access; Taylor-truncated estimator |

Section 5 preserves and attributes the complete-conormal discriminant argument. Section 6 preserves the exact scalar-oracle, reciprocal budget, and effective endpoint statements in their distinct input categories. Appendix A connects the new local geometry to the calibrated root observation, requiring full column rank but not full-symmetric measurement injectivity.

## Complete companion retained without deletion

The companion entry remains `article/v108/paper.tex`. Its literal input closure retains the finite-map reductions, all tensor and jet arguments, proper-real geometry, endpoint visible and first-degenerate-stratum classification, native binary/Cauchy/Hankel derivation, local probability examples, and earlier reconstruction proofs. The build manifest enumerates the actual closure instead of relying on this summary.

Four deterministic prepared copies had been absent from the reviewed mathematical commit. Their originals remain in `article/v107/parts/`. The prepared copies and `preservation.json` are included under `article/v108/prepared/`; their Git blobs are those from the independently retrieved materialized source commit `9affc52cc4eb62e5c14cffb564b380b86503aec2`.

No claim that requires full-symmetric injectivity is silently reused under the weaker loading condition. No equality-of-second-jets statement is upgraded to equality of the entire contact function in a nonidentifiable family. No effective QE description is presented as an explicit structural classification of every endpoint fibre.

## Distinct observation categories

1. Complete conormal data (classical determinant comparison).
2. Second jets at finitely many prescribed points (new exact product-space fibre).
3. Exact-real scalar dual-jet queries (linear oracle count only).
4. Noisy contact values at finitely many nonzero offsets (new statistical experiment).
5. A labelled semialgebraic scalar value graph (effective endpoint representation search).

The new noise theorem fits the exact finite-offset mean. Replacing it by the quadratic Taylor approximation would cause fixed-offset bias and is not used.
