# Paper I blocker closure ledger

## Main theorem scope

The manuscript proves a general bilateral CM2/U3 theorem on an explicit
packetized admissible class and verifies the complete finite-order packet for
an open four-branch moving-seam pinball-cylinder family.  The maximal
strengthening layer now also proves an actual source-specific U3 theorem for a
genuinely nonconjugate specular finite-horizon radial Sinai family.

| Blocker | Resolution | Status |
|---|---|---|
| Additive rather than product time decay | Crossed-envelope interpolation with strict gap `AB>CD` | CLOSED |
| Past/future graph-current asymmetry | Separate reverse/source and forward/target estimates | CLOSED |
| Occurrence re-keying and false cancellation | Stable UID, owner, side, and orientation rules | CLOSED |
| Fixed `(m,n)` DQ only | Head--tail theorem in `l1(N^2)` | CLOSED |
| First-order CM2 incorrectly treated as U3 | Third-source atom CM2 norm and directed totalization | CLOSED |
| Infinite atlas/refinement ambiguity | Vertex and seam moduli plus common-refinement cancellation | CLOSED |
| Third-order words were not composable after regularity loss | Explicit graded ladder `X4->X3->X2->X1` with level-preserving resolvents | CLOSED |
| Finite-DQ remainder through third order lacked one derivative | Fourth derivative bound on `X5` | CLOSED |
| No nonzero actual moving-seam example | Four-branch, three-moving-seam open family | CLOSED |
| Universal overclaim | Positive packet theorem plus finite-prefix no-go/maximality | CLOSED |
| No actual nonconjugate specular Sinai U3 | Radial inflation, changing period-two multiplier, differentiated-invariance complete assemblies, and exact-coboundary gauge response | CLOSED_ACTUAL_SOURCE_SPECIFIC |
| Generic noncoboundary specular U3 from geometry alone | Split-surjective face-defect/infinite-codimension theorem | CLOSED_BY_REFUTATION_AND_MAXIMALITY |

## Actual specular theorem

The normative proof is

```text
../../maximal-strengthening/SPECULAR_SINAI_RADIAL_U3.md
```

For the radial family the invariant density is explicit in fixed normalized
collision coordinates.  Differentiating `L_a rho_a=rho_a` gives the complete
order-`j` source

\[
S_j=\sum_{k=1}^j\binom jkL_0^{[k]}\rho_0^{(j-k)}
=(I-L_0)\rho_0^{(j)},
\]

so every moving-face, intersection, endpoint, and terminal current cancels
after complete physical assembly and

\[
R_0S_j=\rho_0^{(j)}.
\]

This proves actual order three, and indeed arbitrary finite order, for the
invariant-projector channel.  Exact collision coboundaries are handled by the
gauge identity

\[
L_{a,q}=M_{e^{-qg_a}}L_aM_{e^{qg_a}}.
\]

The result is not promoted to a generic centered noncoboundary pressure source.
Such a source must still submit the bilateral third-source packet.

## Exports

```text
P1-CM2
P1-FDQ
P1-U3
P1-RWORDS
P1-ACTUAL-4B
P1-SINAI-RADIAL-U3
```

## Review boundary

The proof drafts have not received external dynamical-systems review.  Their
status is internal mathematical work, not formal theorem credit.
