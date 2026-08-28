# Paper V blocker closure ledger

| Blocker | Resolution | Status |
|---|---|---|
| Nonlinear semigroup represented by one classical law | Single-law linearity obstruction | CLOSED |
| Calibration could be read as an upstream derivation | Exact post-solution jet calibration and dependency guardrail | CLOSED |
| Calibrated linear PDE lacked a source term | Residual `r^u` included explicitly | CLOSED |
| PDE sign made `F_X` potentially negative in the diffusion formula | Generator orientation fixed before calibration | CLOSED_BY_CORRECTION |
| Diffusion factor convention ambiguous | `sigma sigma^T=2a^u`; Paper-III convention crosswalk fixed | CLOSED |
| HJB gradient `p` confused with BSDE `Z` | Explicit identity `Z=sigma^T Du` | CLOSED |
| All control equations forced into one FBSDE | Control/randomized BSDE branch separated | CLOSED |
| Generic fully nonlinear equation claimed to have a 2BSDE | Convex volatility branch separated from nonconvex game/nonlinear-MP branch | CLOSED_BY_TYPING |
| Sequential/simultaneous game representation blurred | Paper-IV game type preserved | CLOSED |
| Genuine path state projected to Markov state | PPDE/path-dependent branch retained | CLOSED |
| Girsanov used before a law was derived | Post-calibration only, with explicit exponential integrability | CLOSED |
| Sign and `1/2` conventions inconsistent | Terminal-value and covariance ledger | CLOSED |

## Main theorem

`Theorem 12.1` is the paper's sole umbrella theorem.  It is a typed hierarchy,
not an assertion that every branch applies simultaneously.

## Upstream guardrail

The following arrows are forbidden:

```text
FBSDE -> HJB homogenization
Girsanov -> theta-expectation derivation
calibrated law -> universal payoff-independent law
2BSDE -> arbitrary nonconvex Isaacs equation
```

## Review boundary

The calibrated algebra and dependency classification are self-contained in the
draft.  Branch-specific existence theorems require their stated regularity,
integrability, aggregation, and comparison hypotheses; none is silently
imported.
