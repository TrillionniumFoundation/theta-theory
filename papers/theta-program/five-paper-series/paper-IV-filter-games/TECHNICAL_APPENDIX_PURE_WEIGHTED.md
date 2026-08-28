# Appendix P/W — Pure Isaacs and actual weighted filtering

This appendix is normative for

```text
P4-PURE-ISAACS-MAXIMAL
P4-WEIGHTED-NONCOMPACT-ACTUAL.
```

Full proofs:

```text
../../maximal-strengthening/PURE_STRATEGY_ISAACS.md
../../maximal-strengthening/WEIGHTED_NONCOMPACT_PATH_ACTUALIZATION.md
```

## PW.1 Pure-strategy classification

For compact continuous actions,

\[
H^-=H^+
\quad\Longleftrightarrow\quad
\text{there exists a pure saddle}.
\]

The saddle correspondence has a measurable selector under Caratheodory data.
Uniformly strong concavity in the maximizing action and strong convexity in the
minimizing action yield a unique Lipschitz saddle.  Matching pennies proves
that mixed minimax alone cannot imply a pure saddle.

The actual four-branch control port is quadratic-bilinear and belongs to the
strong concave--convex class.

## PW.2 Actual noncompact weighted filter

A deterministic countable full-branch factor produces unbounded innovations.
The hidden state

\[
Y_{n+1}=\alpha Y_n+\xi_{n+1}
\]

has unbounded stationary support and the Lyapunov drift

\[
P(1+y^2)\le\alpha^2(1+y^2)+b.
\]

A bounded positive `tanh` observation likelihood preserves a posterior moment
ball.  The prediction--Bayes cycle is a strict contraction after an explicit
observation gap.  Thus the weighted theorem has an actual noncompact system
instantiation.

## PW.3 Boundaries

- mixed value is not a pure value;
- Lyapunov drift alone is not filter contraction;
- filter contraction alone is not weighted HJB comparison;
- pure feedback is exported only with the exact pure-Isaacs or structural
  saddle certificate.
