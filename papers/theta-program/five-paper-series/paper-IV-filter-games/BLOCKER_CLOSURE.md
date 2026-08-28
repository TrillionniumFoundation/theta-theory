# Paper IV blocker closure ledger

| Blocker | Resolution | Status |
|---|---|---|
| Filtering stability stated without a Bayes expansion constant | Explicit TV/weighted Bayes bound | CLOSED |
| Observation frequency not tied to prediction mixing | Strict observation-gap contraction | CLOSED |
| Slow parameter variation ignored | Geometric convolution stability estimate | CLOSED |
| Strategy-dependent controls could destroy filter bounds | Uniform pathwise constants over every strategy tree | CLOSED |
| Bounded geometric sensitivity incorrectly treated as belief independence | Vanishing slow initial layer plus exponential contraction | CLOSED_BY_CORRECTION |
| Weighted filter coupling treated as final HJB proof | Separate weighted comparison/uniqueness gate | CLOSED_BY_CORRECTION |
| No actual noncompact weighted filter | Deterministic countable full-branch innovations, unbounded AR(1), polynomial Lyapunov drift, invariant moment ball, weighted Bayes/prediction contraction | CLOSED_ACTUAL |
| Sequential and simultaneous values conflated | Separate `H^-`, `H^+`, and simultaneous relaxed Hamiltonian | CLOSED |
| Mixed Isaacs incorrectly promoted to pure saddle | Matching-pennies no-go | CLOSED_BY_REFUTATION |
| No exact general pure-strategy criterion | Compact continuous `pure saddle iff H^-=H^+` theorem plus measurable selector | CLOSED |
| No robust positive pure-saddle class | Uniform strong concave-convex and finite strict-margin theorems | CLOSED |
| No actual pure game | Four-branch quadratic-bilinear control port with unique Lipschitz pure feedback | CLOSED_ACTUAL |
| Belief collapse assumed when filtering remains macroscopic | Separate belief-state HJB theorem | CLOSED |
| Genuine path dependence forced into finite-dimensional HJB | Explicit path-state branch | CLOSED |
| No actual bounded filtering/game system | Four-branch hidden-symbol kernel with exact one-step prior forgetting | CLOSED |
| Actual bounded game lacked monotone schemes and comparison | `TECHNICAL_APPENDIX_GAME_SCHEME.md` | CLOSED_ACTUAL_SCOPED |
| K2 estimates not uniform over controls | Compact control-dependent Bernoulli triangular array | CLOSED |

## Pure-strategy closure

The normative proof is

```text
../../maximal-strengthening/PURE_STRATEGY_ISAACS.md
```

For compact actions and continuous payoff,

\[
H^-=H^+
\quad\Longleftrightarrow\quad
\text{a pure saddle exists}.
\]

This exact theorem is maximal: matching pennies has a mixed value but no pure
saddle.  Under

\[
D_{uu}^2F\le-\lambda_uI,
\qquad
D_{vv}^2F\ge\lambda_vI,
\]

the saddle is unique; the saddle operator

\[
(-D_uF,D_vF)
\]

is strongly monotone because the mixed Hessian terms cancel in its symmetric
part.  The actual four-branch quadratic-bilinear port belongs to this class.

## Weighted noncompact closure

The normative proof is

```text
../../maximal-strengthening/WEIGHTED_NONCOMPACT_PATH_ACTUALIZATION.md
```

The actual hidden signal

\[
Y_{n+1}=\alpha Y_n+S_{n+1}K_{n+1}
\]

has unbounded stationary support and satisfies

\[
PW\le\alpha^2W+b,
\qquad W(y)=1+y^2.
\]

A bounded positive `tanh` observation model preserves a weighted moment ball.
After a sufficiently long prediction gap, the weighted prediction--Bayes map
is a strict contraction.  This is an actual noncompact filter, not a bounded
surrogate.

## Exports

```text
P4-FILTER-B
P4-FILTER-W
P4-WEIGHTED-NONCOMPACT-ACTUAL
P4-SEQ
P4-MIXED
P4-PURE-GATE
P4-PURE-ISAACS-MAXIMAL
P4-BELIEF
P4-PATH
P4-ACTUAL-4B
```

## Permanent distinctions

```text
sequential lower value      != sequential upper value
mixed simultaneous value   != pure-strategy saddle
filter contraction          != initial-belief value collapse
filter contraction          != weighted HJB comparison
belief-state Markov problem != genuinely path-dependent problem
```

## Review boundary

The bounded and weighted actual models, pure-saddle classification, and game
schemes are internal drafts.  External filtering/game review has not been
performed.
