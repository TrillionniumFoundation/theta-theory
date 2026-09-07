# Proof and dependency ledger — A1 v15

All labels refer to the compiled `main.tex` expansion. Numbering below is from the 80-page local build and may change after typesetting. The v14 statements and proofs are preserved; the entries distinguish new arguments from retained ones.

| Result | Actual hypotheses and additional argument | Dependencies / review target |
|---|---|---|
| Proposition 3.1, `prop:product-criterion` | Interior command tuple; actual product in its tangent; pairing onto. Exact rank loss of one. Uniform minorization also needs a uniform neighborhood, derivative and row-singular-value bounds, positive likelihood and a command-density lower bound. | Square inverse map with complementary kernel coordinates; integrate those coordinates and the report evidence. No ambient-rank substitution. |
| Theorem 3.2, `thm:positive-attainment` | Two complete strict Chebyshev systems, one inside the actual product tangent; a fixed finite detector spans the factor space; full-support prior. Compact-family and dominated-prior uniformity are separately stated. | Determinant integration; actual-command right inverse; weak compactness of dominated measures; Proposition 3.1. |
| Theorem 1.1 and Theorems 6.3–6.4 | Original full-support monomial classification, including future additive collisions. | All original complete statements and proofs retained: separated product tangent, complete Hermite flag, global bounded-format cover and raw-moment causal recurrence. |
| Lemma 7.2, `lem:circle-attainment` | Haar prior; fixed finite circular detector; independent uniform commands; fixed finite horizon; sufficiently small known contrast. | Exact Laurent coefficient factorization, real rank of the elementary-symmetric map at distinct coordinates, continuity in contrast squared, evidence-weighted inverse map. Physical rank is zero at exactly zero contrast although the normalized extension is nonsingular. |
| Lemma 7.3, `lem:circle-query-metric` | The stated attainable, fixed, equally spaced finite query menu. | Exact coefficient formula and finite Fourier orthogonality. All future attenuation factors are retained. |
| Theorem 7.1, `thm:circle-resolution` | Same one circular experiment, with no noisy advice and no arbitrary circle prior. | Both preceding lemmas; paired thin rectangle; exact integer label budget; unconditional lower measure; reachable centers; weighted update with positive denominator and no inverse contrast. The causal conclusion is a maximum-checkpoint law, not a claim of separate optimal rates at each checkpoint under one code. |
| Corollary 7.4, `cor:circle-phases` | Positive contrast within the proved small-contrast interval. | Ordered upper envelope of the paired harmonic terms; exact transition scales. |
| Proposition 8.1, `prop:general-bounded-dual` | Bounded finite tests, positive covariance lower bound; bounded relative prior perturbations; arbitrary linear observation map. | Attributed to v14 audit A1. Exact normalized posterior-to-prior pullback; no dependence on observation singular values. |
| Proposition 8.3 and exact-prefix corollary | Original local known-calibration, fixed-history relative prior ball and exact prefix information. | Full original statements/proofs preserved. All width orders, not exact body shape or canonical axes. |
| Theorem 9.1 and implementation appendices | Original dominated prior family, interior name slack and numerical interfaces. | Full original uncertainty, stability, compiler, precision and acceptance-contract arguments preserved. No circular effective compiler is inferred. |

## Preservation boundary

`V14_PRESERVATION_MANIFEST.json` was generated from the full expanded v14 source anchored by its committed source-manifest blob `c7995cd0073733257d85f0520e1f889dbe034335`. All 77 proof blocks and 80 complete named statements are checked by SHA-256 and occurrence counts in the new expansion. The expanded v15 has 84 complete proof blocks and 87 named results. Ten pinned v9 core source bodies are unchanged. The earlier v10–v13 checks, including the previously documented v11 correction, still run.

The three compiler modules and tests v10–v14 are checked against `history/V14_SOURCE_MANIFEST.json`. Build relocation does not abridge a proof: the generated analytic and operational includes contain complete original blocks. Historical editorial files are retained in `history/V14_*`; all prior repository sources and reviews remain outside the new directory and unchanged.

## Mathematical verification boundary

The new statements have complete written proofs and finite exact diagnostics. The diagnostics do not exhaust the continuum of contrasts, certify arbitrary horizons, prove priority or constitute an independent referee report. In particular, Theorem 7.1 is asserted for each fixed finite horizon with a corresponding small-contrast interval, not uniformly as the horizon tends to infinity. Full proof review remains appropriate.
