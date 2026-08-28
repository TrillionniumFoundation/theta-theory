# Appendix R — Topology-optimal enhanced-WIP rate

This appendix is normative for `P3-RWIP-OPTIMAL-WETA-P`.  The full proof is

```text
../../maximal-strengthening/OPTIMAL_ENHANCED_WIP_RATE.md
```

## R.1 Typed metric

Fix `p>4` and `1/p<eta<1/2`.  The law distance is Kantorovich--Rubinstein for
the step-two fractional-Sobolev rough metric

\[
\|x-y\|_{W^{\eta,p}}
+
\|\mathbb x-\mathbb y\|_{W^{2\eta,p/2}}^{1/2}.
\]

## R.2 Matching rate

For the affine enriched four-branch random walk,

\[
d_{KR}^{\eta,p}
(\mathbf W_N,\mathbf B_\Sigma)
\le CN^{-(1/2-\eta)}.
\]

A midpoint Brownian-bridge defect is uniformly Lipschitz in this topology,
vanishes on every mesh-affine path, and has Brownian expectation of order
`N^(-(1/2-eta))`.  Hence the exponent is optimal.

## R.3 Endpoint and path rates differ

For smooth endpoint tests with nonzero third cumulant the rate is
`N^(-1/2)`.  The slower path rate is the unavoidable cost of unresolved
Brownian bridges, not a dynamical mixing loss.

## R.4 Nonautonomous block window

Putting `delta=1/2-eta` and `m_epsilon=epsilon^(-kappa)`, accumulated block
error vanishes when

\[
\frac{2}{1+\delta}<\kappa<2.
\]

No rate is inferred from qualitative WIP alone, and no topology-free optimal
exponent is exported.
