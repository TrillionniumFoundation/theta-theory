# CM2 Round149 — terminal C24 two-sided frontier

Date: 2026-07-24

## Result

Round149 certifies a second genuine local boundary type for the Round144 D02
outer-atlas problem: the collision-1648 terminal C24 return/survive frontier.

With `h=2^-4296`, both audited cells use

```text
delta_beta/h in [-1/256,1/256].
```

The return-side cell has

```text
abs(delta_x)/h in [37400/256,37401/256]
terminal classification RETURN_AT_3_INNER
destination core e47f553e...54c4c2
```

The survive-side cell has

```text
abs(delta_x)/h in [37410/256,37411/256]
terminal classification SURVIVE_THROUGH_3_INNER
destination core null
```

The strict unclassified gap is `9h/256`.  Both closed cells independently
replay the same 1,648-stage owner, official-word, chart, H0 homogeneity, and
incidence-rank-14 path.  Each cell performs all `161*1648=265328`
radius-four candidate tests, giving 530,656 tests in the two-sided proof.

Continuity of the frozen analytic composition forces a terminal C24 boundary
between the two cells.  Round149 deliberately does not claim a unique graph
on every beta fibre or classify the gap.

## Independent verification

The verifier imports neither the producer nor its result builder.  It reuses
only the pinned Round149 mathematical engine and independently reconstructs
both full cells.  It rejects eight fully re-signed semantic mutations and
four strict JSON/encoding attacks.

```text
engine SHA256             ffa02ee24969f7b9b4cbd0d81690ba209411a5a00f869a2d935135d1d2376aa8
producer SHA256           626bae52bf8cd3e16d1e4158af005453780b17ca027cc5cdd16471fa0c1ccb86
certificate SHA256        4748f90bee1c8f82a79fa7aeb936d9e13d766ad456cb95bf7f792e41107c53b7
certificate result        4e180030f437aa314cb4ed4797bd3d00058ee0eb2320b720b5bf53dc4e5fc58a
verifier SHA256           89b2b94068091c53ca4417908220be4e49a25a80ea4723b47fc485ddc9540efc
verification SHA256       c668db505c6be2c6c06e25d2610a68c68c7a38c0f6dec393b19c826969fd071a
verification result       82dd55d356aa4a374e9d685973caf17a053c6e7ff887ff6be9bb1179ea2b5631
```

Two producer and two verifier cold runs under distinct hash seeds are
byte-identical to the formal artifacts.

## D02 effect

Round146 had already certified the local collision-three D0 transverse
frontier.  Round149 adds the distinct terminal C24 frontier.  The two local
frontiers are not yet joined into a finite maximal-component atlas, and
other event families are not exhausted.

```text
D02                         BLOCKED
D03 negative oracle         unauthorized
component_v1_id             null
global Gate5                10/18
global complete blocks      0
CM2                         NO-GO_FOR_CLAIM
```

The next exact step is to construct a connected two-dimensional corridor
between the collision-three D0 frontier and this terminal C24 frontier,
subdivide every intervening event cell, and exhaust the remaining physical
event families.
