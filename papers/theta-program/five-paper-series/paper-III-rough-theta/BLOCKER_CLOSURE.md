# Paper III blocker closure ledger

| Blocker | Resolution | Status |
|---|---|---|
| Microscopic selector depended circularly on unknown HJB gradient | External cotangent/tilt signal and frozen Doob transform defined before HJB | CLOSED |
| Scalar WIP was used as an enhanced rough WIP | UM4--UM5 bracket/area packet and rough martingale theorem | CLOSED |
| No control of coboundary maxima | UM6 maximal negligibility | CLOSED |
| Invariant-law result was silently transferred to all initial laws | UM7 quantitative forgetting | CLOSED |
| Frozen coefficients had no parameter modulus | Paper-II common-space resolvent plus UM8 | CLOSED |
| Qualitative uniform WIP treated as a full-scale nonautonomous theorem | Full scale requires a compatible modulus or direct triangular characteristics; qualitative WIP gives only a diagonal result | CLOSED_BY_CORRECTION |
| Block errors were not accumulated | Explicit condition `N_epsilon eta(m_epsilon)->0` and total freezing/switching bounds | CLOSED |
| “Optimal enhanced-WIP rate” had no topology or test class | Step-two fractional-Sobolev topology and regular Stein--Dirichlet class `Sigma_(eta,p)` fixed explicitly | CLOSED_BY_TYPING |
| Literature rate was overread as full Lipschitz--KR | Export restricted to the second-derivative-regular Stein test class actually controlled by the finite-dimensional argument | CLOSED_BY_CORRECTION |
| No matching lower bound in the same test class | Smooth cylindrical midpoint-bridge test has uniformly bounded `Sigma_(eta,p)` norm and yields the matching `N^{-(1/2-eta)}` lower bound | CLOSED |
| Rough regularity window was too weak | Safe range `p>6`, `1/3<eta-1/p`, `eta<1/2` | CLOSED_BY_CORRECTION |
| No actual optimal-rate system | Bounded iid four-branch symbol increments with uniform covariance | CLOSED_ACTUAL |
| Nonautonomous block window not explicit | `2/(1+1/2-eta)<kappa<2` for `m_epsilon=epsilon^{-kappa}` | CLOSED |
| Area anomaly omitted | Included in enhanced limit and bracket drift `b_Gamma` | CLOSED |
| General HJB theorem lacked a named consistency/comparison packet | Explicit DPP package and comparison theorem interface | CLOSED_RELATIVE_TO_PACKET |
| Actual four-branch model lacked a DPP and comparison proof | `TECHNICAL_APPENDIX_DPP_COMPARISON.md`: monotone scheme, consistency, comparison, and convergence | CLOSED_ACTUAL_SCOPED |
| K3 incorrectly required for every HJB | Uncontrolled/one-player HJB derived directly from K2 | CLOSED |
| No actual full-scale model | Bernoulli coding plus direct predictable brackets and actual monotone DPP | CLOSED |
| Nonconvexity only formal | Explicit `delta>gamma/4`, `p=q=pi/2`, defect `4 delta` | CLOSED |

## Optimal-rate theorem

The normative proof is

```text
../../maximal-strengthening/OPTIMAL_ENHANCED_WIP_RATE.md
```

For

\[
p>6,
\qquad
1/3<\eta-1/p,
\qquad
\eta<1/2,
\]

define `d_SD^(eta,p)` using the normalized Stein--Dirichlet class
`Sigma_(eta,p)`.  Then the enriched four-branch random walk satisfies

\[
cN^{-(1/2-\eta)}
\le
d_{SD}^{\eta,p}
(\mathcal L(\mathbf W_N),\mathcal L(\mathbf B_\Sigma))
\le CN^{-(1/2-\eta)}.
\]

The lower test is a smooth sum of scaled midpoint bridge defects.  It is zero
on every mesh-affine walk, has Brownian expectation of the displayed order,
and its first three Cameron--Martin derivatives are uniformly controlled by
the disjoint interval geometry.

The export does not claim an exact rate in the full bounded-Lipschitz
Kantorovich--Rubinstein distance.  “Optimal” is permanently tied to the
declared fractional-Sobolev Stein--Dirichlet test metric.

## Exports

```text
P3-DOOB
P3-RWIP
P3-RWIP-OPTIMAL-WETA-P
P3-NAHOM
P3-HJB
P3-THETA
P3-NONCONVEX
P3-ACTUAL-4B
```

## Permanent corrections

```text
compatible quantitative modulus or direct characteristics -> full scale
qualitative uniform WIP only                              -> cofinal diagonal

Stein--Dirichlet smooth test distance -> exact typed optimal rate
full Lipschitz--KR distance            -> not claimed by this proof
```

## Review boundary

The optimal-rate proof and its uniform lower-test lemma are internal probability
proofs and have not received external rough-path review.
