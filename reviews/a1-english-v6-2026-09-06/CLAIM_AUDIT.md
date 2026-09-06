# A1 v6 — claim-by-claim audit

**Pinned source:** `750a65ef62422e81307b4a61fd891ee42fa2639e`. Paths below are relative to `papers/A1-english-v6/`. Line numbers are original source lines, not JSON-wrapper lines. Compiled numbers refer to the fresh 16-page build. “Supported” means no blocking defect was identified in the written argument; it does not mean formal verification or acceptance.

## Definitions controlling the assertions

| Definition | Source | Disposition |
|---|---|---|
| 2.2, `def:future` | `sections/02_experiments.tex:55–64` | Adequate future-only quantifier. Same task data, same first command, no original prefix or prefix-dependent seed. Add an explicit Borel-kernel convention for completeness. |
| 5.1, `def:finite-state` | `sections/05_streaming.tex:8–23` | Adequate persistent-index model. Old commands and seeds charged; clock, read-only exact calibration and workspace excluded. It is not a finite-precision/Turing-space model. |

## All 15 principal result labels

| Result | Source and fresh PDF | Disposition and actual proof obligation |
|---|---|---|
| Theorem 1.1, `thm:main` | `sections/01_introduction.tex:23–44`, pp. 1–2 | Supported by 2.3, 3.3 and 3.4. The continuous dimension is for history encodings and observable future laws. No uniform conditioning or arbitrary hidden-parameter losses follow. |
| Lemma 2.1, `lem:interior` | `sections/02_experiments.tex:19–42`, p. 3 | Supported. Surjective finite calibration has a linear right inverse; small perturbations of half failure lie inside the same command cube. Explicit categorical cells are positive and independent. General categorical realization is not mechanical realization. |
| Proposition 2.3, `prop:tests` | `sections/02_experiments.tex:72–99`, p. 4 | Supported. Executable failure products span all of `W_A^m`; every feedback word belongs to that space. Independent seeds can be integrated. The new future-only restriction repairs the prior ambiguity. |
| Lemma 3.1, `lem:mixed-moment` | `sections/03_transversality.tex:5–46`, p. 5 | Supported. Exponential zero counting establishes nonvanishing; the Wronskian fixes sign. Determinant integration and separated positive-mass intervals prove strictness without a density. Endpoint zero is handled by continuity. Classical positivity is properly acknowledged. |
| Lemma 3.2, `lem:binomial-tangent` | `sections/03_transversality.tex:48–88`, pp. 5–6 | Supported; central new input. Complementary binomial products form a polynomial basis. Endpoint and interior exponent strings give the complete tangent of size `n(r-1)+1`. Formal negative-root evaluation is legitimate algebra, not physical extrapolation. |
| Theorem 3.3, `thm:rank` | `sections/03_transversality.tex:90–144`, p. 6 | Supported. Mixed pairing has maximal rank, and `v -> v-p e0(v)` has exactly one-dimensional kernel on its image. Scaling gives the global upper bound; a nonzero polynomial minor gives genericity. A projected ball has a local section; the ambient image need not be flat. |
| Theorem 3.4, `thm:causal` | `sections/03_transversality.tex:151–196`, pp. 6–7 | Supported. The section and invariance of domain give the lower bound; normalized factors or moments give the global upper encoding. One monotone switch and sparse Bayes recursion give causal attainment. Past-dependent task data remain separate. |
| Proposition 4.1, `prop:three` | `sections/04_observation_algebra.tex:13–51`, pp. 7–8 | Supported. Primitive binomial relation generates all homogeneous collisions, and multiplication by it is injective. Irrational ratios remove collisions. This is a Hilbert-function application, not a new general sumset theorem. |
| Corollary 4.2, `cor:sparse-example` | `sections/04_observation_algebra.tex:53–74`, p. 8 | Supported. `A={0,2,5}` yields the stated sumsets and profile `(0,2,4,6,5,2,0)`. The v5 referee's example is credited; v6 proves the all-full-support-prior extension. |
| Lemma 5.2, `lem:lipschitz` | `sections/05_streaming.tex:42–77`, p. 9 | Supported. Factor interpolation preserves pointwise lower bounds; moment interpolation is a posterior mixture. Positive denominators and compactness bound derivatives. The constants may deteriorate with horizon and calibration. |
| Theorem 5.3, `thm:stream-upper` | `sections/05_streaming.tex:79–133`, pp. 9–10 | Supported in Definition 5.1. Reachable representatives keep updates feasible, and the recurrence includes every quantization error. No exact prefix is retained at changeover. Representative selection is existential; “constructive” should not imply effective finite-precision synthesis. |
| Theorem 5.4, `thm:stream-lower` | `sections/05_streaming.tex:135–215`, pp. 10–11 | Supported. Fixed continuous exploration, retained failure evidence and a local submersion give an unconditional minorization. At most `M` centers remain after averaging independent decoder coins. The volume bound handles arbitrary encoders. It is a prediction theorem, not an arbitrary optimal-control lower bound. |
| Theorem 5.5, `thm:control-bound` | `sections/05_streaming.tex:217–257`, pp. 11–12 | Supported. Compact action maximization and common state-Lipschitz bounds suffice; differentiability of the optimizer is unnecessary. Representative-greedy actions plus Bellman telescoping give only the stated upper power. |
| Theorem 6.1, `thm:finite-bit-value` | `sections/06_common_risk.tex:104–158`, p. 14 | Supported. Conditional means and deterministic reassignment give optimal finite partitions even with independent randomization. Three states merge one raw pair; four states are lossless. The target and total-risk baseline are common. |
| Corollary 6.2, `cor:threshold` | `sections/06_common_risk.tex:183–235`, p. 15 | Supported. Strictly ordered tag means at zero amplitude; split equal-mean signs cannot be optimal with two centers. Finitely many positive gaps persist for small amplitude. The threshold is prior-dependent and the gain may be very small. |

## Other assertions inspected

The mechanical equations in Section 6 use whole-preparation normalization, one-collision coverage and the correct flux and coefficient determinant. The covariance formula for the lossless sign gain is consistent with the pair cost. The zero forecast bound in Section 5.1 is correct and does not conflict with fixed-horizon high-resolution rates. The principal narrative distinguishes the uncensored sign postprocessing from older comparator interventions.

## Severity classification

**Blocking mathematical findings:** none identified in the principal text on this audit. This is not a guarantee of correctness.

**Major editorial findings:** the general-journal significance of the new pairing theorem and the force of its consequences remain insufficiently established; exact dimension is not a quantitative resolved-memory law; the two operational applications remain distinct. See E1–E3 in the report.

**Minor/formal findings:** published bibliography update; the meaning of constructive synthesis; explicit Borel conventions; preservation of the history-encoding and resource-model caveats. These do not invalidate the current core arguments.

## Evidence boundary

The independent 108 checks include 18 exact tangent/normalized-rank fixtures under three priors, 16 exact mixed minors, four six-report sparse update paths, finite categorical partition checks, near-collision ranks and symbolic identities. They do not certify all budgets, arbitrary priors, topology, randomized minimax quantifiers or novelty. The separately rerun author suite supplies its own finite-menu index-only test and physical interval enclosure. The legacy companion and the eleven-paper program are outside the fresh claim audit.
