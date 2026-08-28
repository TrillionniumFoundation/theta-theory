# Paper II blocker closure ledger

| Blocker | Resolution | Status |
|---|---|---|
| Fibrewise charts do not define cross-parameter operator differences | Finite-atlas direct-sum stabilization with `R_a J_a=I` | CLOSED |
| Pressure derivatives contain moving singularity source words | Imported exact Paper-I U3/RWORDS interface | CLOSED |
| Physical-time normalization was implicit | Pressure root `P(a,q,Lambda_a(q))=0` and explicit mean-roof division | CLOSED |
| Diffusion response needs a third mixed derivative | Formula for `P_{a q_i q_j}` supplied by U3 | CLOSED |
| Collision response not yet transferred to the flow | Roof-cell renewal decomposition and centered pole cancellation | CLOSED |
| Full moving-flow BDL theorem was being treated as necessary | Replaced by the exact low-frequency suspension theorem actually used downstream | CLOSED_BY_SHARP_SCOPE |
| Green--Kubo, pressure, and martingale conventions could disagree | Equality theorem and factor `D=Sigma/2` fixed | CLOSED |
| Positive semidefinite tensor not upgraded to ellipticity | Coboundary-kernel criterion plus compact non-coboundary margin | CLOSED |
| `(x,p)` coefficient composition was ill-typed | Stabilized common space and corrected Hölder--Nemytskii lift | CLOSED |
| No actual positive example | Four-branch family with `kappa=cos(2 pi y)` and fixed-point non-coboundary witness | CLOSED |

## Permanent convention ledger

```text
collision covariance = P_qq
physical covariance  = P_qq / mean_roof
physical diffusion   = physical covariance / 2
```

The slow/cotangent selector is external at this layer.  Substituting `p=Du` is
a Paper-III operation and is not used to construct the microscopic operator.

## Exports

```text
P2-COMMON
P2-PRESSURE3
P2-SUSP0
P2-PHYS
P2-COEFF
P2-ELL
P2-ACTUAL-4B
```

## Review boundary

The new common-space and renewal proofs are internal drafts.  No external
spectral-dynamics review has yet been performed.
