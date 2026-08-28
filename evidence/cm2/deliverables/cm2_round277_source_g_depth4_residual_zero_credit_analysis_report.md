# CM2 Round277 depth-4 residual analysis

Status: `ZERO_CREDIT_DIAGNOSTIC`

The orientation-corrected Round277 probe leaves 89,792 finite-depth face
tails.  This analysis independently replays the face search without consuming
the accepted corridor ledger and freezes the exact residual candidate-index
set.

## Reconciliation

- whole candidate universe: **330,724**
- positive MATCH patch found by depth 4: **240,932**
- no positive MATCH patch found by depth 4: **89,792**
- residual index ledger rows: **89,792**
- residual index digest:
  `421e7cfdc294f94d2a4235bfef681c9b11fea7d2490c9714acba0e96ab4e6e64`
- unique residual geometric face groups: **87,300**

The replay matches the corrected Round277 face-patch census exactly.  A
finite-depth miss remains fail-closed and is not an absence certificate.

## Main strata

By source-round pair:

- R269/R269: **56,100**
- R208/R269: **22,116**
- R208/R208: **6,068**
- R271/R271: **3,864**
- R270/R270: **1,512**
- R272/R272: **128**
- R269/R271: **4**

By face-normal axis:

- axis 2: **67,612**
- axis 0: **22,052**
- axis 1: **128**

The 1,436,672 depth-4 terminal cells split principally into:

- strict different complete signature: **739,516**
- outgoing-chart seam rejection: **676,100**
- X/Y wall endpoint or count transitions: **21,056**

This identifies exact outgoing-seam and wall arrangements—not mere numerical
precision—as the dominant remaining geometry.

## Deeper probes

A deterministic 400-edge sample spanning 136
`(round-pair, chart, axis, owner-target)` strata was replayed through face
depth 8:

- newly accepted with two correctly oriented inward corridors: **198**
- still fail-closed: **202**

Of the depth-8 survivors, a deterministic 96-edge sample at depth 12 gave:

- newly accepted: **40**
- still fail-closed: **56**

Deeper subdivision therefore closes a material fraction but does not replace
the required explicit seam/wall arrangement.

## Artifacts and hashes

- analysis source SHA256:
  `fe4ae2aa545edc2662f363ef7794a9de14ff330847413fac2dc6d08e03008aaa`
- result JSON SHA256:
  `c63c647510d9463117538cf9aea1e5c712caee2b7c17c0f2e77dfdc23510809b`
- deterministic gzip residual ledger SHA256:
  `301872ae46f5f76843c7ae141c8e95c5d21a2e6d0d0d8a0fc60c55a93f3fa306`

No occurrence, component-edge, rank, quotient, maximality, fibre,
disposition, seam, or `Jx/Jy` credit is issued.  CM2 remains
`NO-GO_FOR_CLAIM`.
