# Paper II blocker closure ledger

| Blocker | Resolution | Status |
|---|---|---|
| Fibrewise charts do not define cross-parameter operator differences | Finite-atlas direct-sum stabilization with `R_a J_a=I` | CLOSED |
| Square root of an arbitrary partition may fail to be smooth | Smooth quadratic partition `sum psi_alpha^2=1` constructed explicitly | CLOSED |
| Pressure derivatives contain moving-singularity source words | Imported exact graded Paper-I U3/RWORDS interface | CLOSED |
| Physical-time normalization was implicit | Pressure root `P(a,q,Lambda_a(q))=0` and mean-roof division | CLOSED |
| Diffusion response needs a third mixed derivative | Formula for `P_{a q_i q_j}` supplied by U3 | CLOSED |
| Collision response not transferred to the flow | Roof-cell renewal decomposition and centered pole cancellation | CLOSED |
| Full high-frequency moving-family BDL missing | Strict local BDL witness packet, openness, compact finite-cover uniformization, fixed quadratic atlas, and uniform high-frequency resolvent | CLOSED_RELATIVE_TO_EXPLICIT_WITNESS |
| Compactness was used without a strict Dolgopyat witness | Openness is applied to finite-time nonintegrability witnesses before the finite-cover step | CLOSED_BY_CORRECTION |
| Moving-table high-frequency parameter derivatives lacked a common graph domain | `BDL-PARAMETER-DOMAIN-v1`: common graph core, type-A graph differentiability, domain preservation, and difference-quotient convergence | CLOSED_RELATIVE_TO_EXPLICIT_DOMAIN_PACKET |
| Twist gauge was incorrectly read as table-parameter response | Exact coboundary conjugacy exports arbitrary finite `q`-derivatives only; `a`-derivatives still require the parameter-domain packet | CLOSED_BY_CORRECTION |
| One scalar grazing weight expected to control every deformation | Unbounded consecutive-collision weight-ratio counterexample | CLOSED_BY_REFUTATION_AND_MAXIMALITY |
| No actual compact moving specular high-frequency family | Small nonconjugate radial interval contained in one strict BDL witness neighbourhood | CLOSED_ACTUAL_UNIFORM_FAMILY |
| No actual all-frequency coboundary channel | Nonconjugate radial exact-flow-coboundary gauge conjugacy in `q` | CLOSED_ACTUAL_TWIST_SPECIFIC |
| Green--Kubo, pressure, and martingale conventions could disagree | Equality theorem and factor `D=Sigma/2` fixed | CLOSED |
| Positive semidefinite tensor not upgraded to ellipticity | Coboundary-kernel criterion plus compact non-coboundary margin | CLOSED |
| `(x,p)` coefficient composition was ill-typed | Stabilized common space and corrected Hölder--Nemytskii lift | CLOSED |
| No actual positive example | Four-branch family with `kappa=cos(2 pi y)` and fixed-point witness | CLOSED |

## High-frequency theorem

The normative proof is

```text
../../maximal-strengthening/MOVING_FAMILY_HIGH_FREQUENCY_BDL.md
```

A family submits `BDL-FAMILY-WITNESS-v1`, consisting of uniform geometry,
flow boxes, temporal-distance/nonintegrability witnesses with strict positive
margins, compact embeddings, and a high-frequency strip. Strict witnesses are
open in the table parameter, so a finite cover of a compact family produces
one uniform packet. After quadratic-atlas stabilization,

\[
\sup_{a\in A}\|(z-\widehat X_a)^{-1}P_a\|
\le C(1+|\operatorname{Im}z|)^\nu
\]

on the declared strip.

This actual uniform-family estimate is distinct from differentiability in the
table parameter.  For `a`-derivatives, `BDL-PARAMETER-DOMAIN-v1` additionally
requires a common dense graph core, graph-topology `C^k` dependence, complete
generator letters, domain preservation, and symbol estimates.  Only then

\[
\partial_a^kR_a(z)
=
\sum_{j_1+\cdots+j_m=k}
\frac{k!}{j_1!\cdots j_m!}
R_aG_a^{(j_1)}R_a\cdots G_a^{(j_m)}R_a.
\]

For an exact flow coboundary, gauge conjugacy gives all finite twist derivatives
in `q` for every fixed table and uniformly over the radial family.  It does not
supply moving-table derivatives in `a`.

## Permanent convention ledger

```text
collision covariance = P_qq
physical covariance  = P_qq / mean_roof
physical diffusion   = physical covariance / 2

uniform family BDL   != table-parameter differentiability
q gauge response     != a moving-table response
```

## Exports

```text
P2-COMMON
P2-PRESSURE3
P2-SUSP0
P2-PHYS
P2-COEFF
P2-ELL
P2-ACTUAL-4B
P2-BDL-HF-FAMILY
```

## Review boundary

The common-space, renewal, and high-frequency family proofs are internal
drafts.  No external spectral-dynamics review has yet been performed.
