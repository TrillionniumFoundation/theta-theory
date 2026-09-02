# Round-Thirty-One Review Index

**Controlling report:** `REFEREE_REPORT_ROUND30_GPT56_PRO_HARSH.md`  
**Controlling review branch:** `review/round30-gpt56-pro-harsh-11paper-2026-09-02`  
**Controlling review head:** `4c6aa83111d404d9139acad1699b1f31bdb792e4`  
**Reviewed mathematical source:** `76f7ae36d7f894673383ceccda41c86b1cb6ac5c`  
**Active revision branch:** `revision/round31-referee-positive-closure-11paper-2026-09-03`

Every `papers/*/main.tex` imports `ROUND31_REVISION.tex`. Every wrapper imports only `ROUND31_POSITIVE_CLOSURE.tex` and `ROUND31_PREAMBLE.tex`.

| Node | Active source | Round-31 central export | Round-30 direct regressions |
|---|---|---|---|
| A1 | `papers/A1-exact-benchmarks/ROUND31_POSITIVE_CLOSURE.tex` | loss-buffered projective response, seam projection decay, common-level trace-class FCLT | covariance derivative leaves base space; seam projection condition unproved |
| A2 | `papers/A2-sinai-homological-pressure/ROUND31_POSITIVE_CLOSURE.tex` | exact arithmetic leaf, zero-frequency spectral split, polynomial crossover, mixed Edgeworth LLT | arithmetic falsely open; `L_0^n1` contradiction; nonintegrable intermediate bound |
| A3 | `papers/A3-full-empirical-path-ldp/ROUND31_POSITIVE_CLOSURE.tex` | transition-count entropy, renewal relation, two-scale chronological current, matrix-amplitude stopped LLT | wrong entropy clock; vanished slow derivative; unjustified scalar overshoot factor |
| A4 | `papers/A4-history-memory-universal-pressure/ROUND31_POSITIVE_CLOSURE.tex` | weighted Harris/FK, certified potential bridges, resolvent-small compression, admissible memory | graph perturbation misuse; graph-observation power loss; unsupported arbitrary base potentials |
| B1 | `papers/B1-microcanonical-preparation/ROUND31_POSITIVE_CLOSURE.tex` | event-independent reserved anchors, quadratic relative-energy smoothing, exact mixed Edgeworth coefficients | impossible equal-velocity full-rank minor; event cuts anchor density |
| B2 | `papers/B2-collision-clusters-dynamic-ldp/ROUND31_POSITIVE_CLOSURE.tex` | constructed tree right inverse/pivots, simultaneous loop coarea, Ovsyannikov history evolution, joint LDP | invalid fixed-radius arbitrary-time bound; pivot rank assumed; graphwise coarea tail incomplete |
| B3 | `papers/B3-hamilton-boltzmann-cotangents/ROUND31_POSITIVE_CLOSURE.tex` | full contact normal/cycle geometry, deterministic-interval cumulants, dyadic temporal modulus, CLT/Mosco | stopping time moved under root resampling; Efron--Stein did not control drift/full increment |
| B4 | `papers/B4-nonlinear-kinetic-semigroups/ROUND31_POSITIVE_CLOSURE.tex` | ballistic energy compactification, shellwise semigroup/comparison, zero-recession W2 gate | entropy-energy shell not W2 compact; global strong continuity false |
| C1 | `papers/C1-information-risk-sensitive-saddles/ROUND31_POSITIVE_CLOSURE.tex` | normalized stratum selection, cylindrical distributional jets, observable-quotient stability, adaptive BvM | total mass equals number of strata; false projective contraction; hidden state mistyped; pointwise identification insufficient |
| C2 | `papers/C2-cotangent-rigidity-tangent-representations/ROUND31_POSITIVE_CLOSURE.tex` | Polish strict dual, full annihilator, certified rigidity, parameter-specific likelihoods, stable optional projections | common filter in likelihood; weak convergence insufficient; unavailable pressure chart; blanket BSDE |
| D1 | `papers/D1-deterministic-theta-contractions/ROUND31_POSITIVE_CLOSURE.tex` | lattice fibre/cell dichotomy, upstream Edgeworth interface, finite-memory policy approximation, epi-argmax | lattice power sign; unavailable high-order local input; inconsistent raw scaling; policy uniformity assumed |

## Primary review order

1. A2 exact arithmetic leaf and the integrated Fourier estimate.
2. A3 transition-count entropy and two-scale current relation.
3. A4 relative-resolvent compression and Hilbert-bounded memory observation.
4. B2 construction of pivots and Ovsyannikov radius accounting.
5. B1 regular/quadratic anchor split and event independence.
6. B3 deterministic-interval moment compiler and temporal chaining.
7. B4 ballistic compactification and shellwise comparison.
8. C1 normalization, projective derivatives, and induced-law observability.
9. C2 parameter-specific likelihood and quantitative filter stability.
10. A1 common-level covariance response.
11. D1 lattice convention and policy-uniform synthesis.

## Build and verification

- Consolidated source: `ROUND31_REVISION_DOSSIER.tex`
- Standalone sources: `papers/*/ROUND31_REVISION.tex`
- Verifier: `python3 tools/verify_round31.py --build`
- Workflow: `.github/workflows/verify-round31-referee-closure.yml`
- Referee response: `AUTHOR_RESPONSE_ROUND30.md`
- Dependency ledger: `ROUND31_PROOF_DEPENDENCY_LEDGER.md`
- Counterexample ledger: `ROUND31_MATHEMATICAL_REGRESSIONS.md`
