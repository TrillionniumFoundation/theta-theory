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
| Genuine path state projected to Markov current state | Delay segment state and horizontal-shift generator retained | CLOSED |
| No actual noncompact path-dependent model | Deterministic fast product, stationary weighted-filter averaging, delay diffusion, entire-window payoff, pure path game, segment DPP, and BSDE | CLOSED_ACTUAL |
| Fast belief incorrectly retained as an untyped limiting coordinate | Centered filter contribution shown `O_{L2}(epsilon)`; only its stationary average enters the path drift | CLOSED_BY_CORRECTION |
| Segment PPDE omitted the delay shift generator | Added horizontal generator `S` plus present-endpoint vertical derivatives | CLOSED_BY_CORRECTION |
| Girsanov used before a law was derived | Post-calibration only, with explicit exponential integrability | CLOSED |
| Sign and `1/2` conventions inconsistent | Terminal-value and covariance ledger | CLOSED |

## Actual path theorem

The normative proof is

```text
../../maximal-strengthening/WEIGHTED_NONCOMPACT_PATH_ACTUALIZATION.md
```

The deterministic product fast system contains:

- the four-branch moving-seam factor;
- a countable full-branch factor producing unbounded centered innovations;
- a two-sided deterministic Bernoulli shift producing exact iid observation
  uniforms.

Its weighted filter is geometrically stable.  The stationary filter observable
has centered partial sums of order `N^(1/2)`, so under slow scaling

\[
\epsilon^2\sum_{n<O(\epsilon^{-2})}
[H(\pi_n)-\bar m]=O_{L^2}(\epsilon).
\]

The slow limit is a dissipative stochastic delay equation on

\[
C([-\delta,0];\mathbb R^d).
\]

For an entire-window payoff and strong concave-convex running game, the value
satisfies the segment DPP and

\[
\partial_tV+\mathcal SV
+b_*\cdot\partial_0V
+\frac12\operatorname{Tr}
(a\partial_{00}^2V)+\ell_*=0.
\]

The corresponding Lipschitz BSDE evaluates this actual path value.

## Main theorem

`Theorem 12.1` remains a typed hierarchy.  The new actual export chooses its
semilinear path/segment branch; it does not assert that every branch applies
simultaneously.

## Exports

```text
P5-SINGLE-LAW-NOGO
P5-CALIBRATED
P5-FBSDE
P5-CONTROL-BSDE
P5-SECOND-ORDER
P5-PPDE
P5-PATH-ACTUAL
P5-GIRSANOV
```

## Upstream guardrail

The following arrows are forbidden:

```text
FBSDE -> HJB homogenization
Girsanov -> theta-expectation derivation
calibrated law -> universal payoff-independent law
2BSDE -> arbitrary nonconvex Isaacs equation
Markov payoff -> claimed actual path payoff
```

## Review boundary

The calibrated algebra, actual delay model, segment DPP, and representation
classification are internal drafts.  Branch-specific external review has not
been performed.
