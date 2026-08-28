# Paper IV blocker closure ledger

| Blocker | Resolution | Status |
|---|---|---|
| Filtering stability stated without a Bayes expansion constant | Explicit TV bound `C_B=2 g_+/g_-` | CLOSED |
| Observation frequency not tied to prediction mixing | Strict gap `C_B rho^{r_*}<1` | CLOSED |
| Slow parameter variation ignored | Geometric convolution stability estimate | CLOSED |
| Strategy-dependent controls could destroy filter bounds | Uniform pathwise constants over every strategy tree | CLOSED |
| Weighted filter coupling treated as final HJB proof | Separate weighted comparison/uniqueness gate | CLOSED_BY_CORRECTION |
| Sequential and simultaneous values conflated | Separate `H^-`, `H^+`, and simultaneous relaxed Hamiltonian | CLOSED |
| Isaacs equality assumed for pure controls | Mixed relaxed minimax theorem; pure saddle requires extra certificate | CLOSED_BY_TYPING |
| Belief collapse assumed when filtering remains macroscopic | Separate belief-state HJB theorem | CLOSED |
| Genuine path dependence forced into finite-dimensional HJB | Explicit PPDE/path-state branch | CLOSED |
| No actual filtering/game system | Four-branch hidden-symbol kernel with exact one-step prior forgetting | CLOSED |
| K2 estimates not uniform over controls | Compact control-dependent Bernoulli triangular array | CLOSED |

## Exports

```text
P4-FILTER-B
P4-FILTER-W
P4-SEQ
P4-MIXED
P4-PURE-GATE
P4-BELIEF
P4-PATH
P4-ACTUAL-4B
```

## Permanent distinctions

```text
sequential lower value      != sequential upper value
mixed simultaneous value   != pure-strategy saddle
filter contraction          != weighted HJB comparison
belief-state Markov problem != genuinely path-dependent problem
```

## Review boundary

The bounded hidden-symbol realization is actual and complete in scope.  The
weighted theorem remains a theorem over an explicit Lyapunov/moment/comparison
packet; it is not advertised as verified for every Lorentz observable.
