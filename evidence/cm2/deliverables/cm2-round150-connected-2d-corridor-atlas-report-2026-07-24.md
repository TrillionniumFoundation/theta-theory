# CM2 Round150 — connected physical 2D corridor atlas

Date: 2026-07-24

## Result

Round150 certifies a connected two-generator corridor from the Round146
central seed cell to a newly rigorous terminal C24 event graph.  Its exact
status is

```text
CERTIFIED_CONNECTED_PHYSICAL_2D_CORRIDOR_AND_UNIQUE_TERMINAL_C24_GRAPH__D02_STILL_BLOCKED
```

The physical coordinates remain

```text
delta_x    = x - x_star
delta_beta = (asin(p) - 4 r) - b_star
h          = 2^-4296.
```

## Finite connected corridor

The new regular atlas contains 17 closed physical two-dimensional cells on

```text
delta_beta/h in [-1/256,1/256].
```

Sixteen return cells cover the exact face-connected interval

```text
abs(delta_x)/h in [2,4675/32].
```

The first cell shares the exact `abs(delta_x)/h=2` face with the wider
Round146 central cell.  The last return cell shares the exact
`abs(delta_x)/h=4675/32` face with the terminal event box.  A strict survive
cell begins on the event box's opposite face at

```text
abs(delta_x)/h=1169/8.
```

There are 18 certified adjacency rows: one upstream attachment, fifteen
return-cell faces, and the two event-box faces.

## Terminal C24 graph

The event is the collision-1648 destination-core face

```text
terminal_p(delta_x,delta_beta) + 1/50 = 0.
```

Its full event box is

```text
abs(delta_x)/h in [4675/32,1169/8]
delta_beta/h    in [-1/256,1/256].
```

All 1,648 frozen owners, official words, wall margins, outgoing charts,
homogeneity labels and incidence ranks are strict on the whole box.  At the
terminal stage the expected core is the sole unresolved core, the `p=p0`
condition is the sole unresolved core inequality, and every competing core
is strictly excluded.

The complete interval variational propagation gives

```text
h * partial_event/partial_delta_x
    in [8.968069749324413e-05,8.969870993778005e-05]
h * partial_event/partial_delta_beta
    in [3.194924598417871e-05,3.195566301747233e-05].
```

Both derivatives are strictly positive.  The parametric interval-Newton
image satisfies

```text
abs(delta_x)/h
    in [146.10743976340564,146.11250592054967]
```

strictly inside the event box.  Therefore every fixed
`delta_beta` fibre in the certified strip has exactly one terminal C24 root.
The graph is transverse, with

```text
d abs(delta_x) / d delta_beta
    in [0.35618400666862726,0.35632710298523307].
```

This removes Round149's `9/256 h` continuity-only gap on the shared beta
strip.

## Audit census

Round150 independently audits 18 new objects: 17 regular cells and one
event box.

```text
new collision-stage/object pairs       29,664
radius-four candidate tests/object    265,328
new radius-four candidate tests     4,775,904
strict terminal return cells                16
terminal p0 event boxes                      1
strict terminal survive cells                 1
```

All objects have the same complete official R1648 path SHA256
`f504289edce554d47e17a90d7c886586a69f3ec4b64fafd90c718c50ca93221e`.

## Independent verification

The verifier imports or executes neither the producer nor its result
builder.  It uses the separately pinned mathematical engine, reconstructs
all 17 regular cells, the complete event-box audit, the interval Jacobian,
the parametric interval-Newton graph and all 18 adjacency rows.

```text
engine SHA256             4d80a8e3cef5e3e754e1b10221716239bc123aa228c6ab27a30b9fc76af336fc
producer SHA256           9580636d04ed1fcfe7ff60ff91da9b415ff69d6a98ba32b8649a22d099b6f224
certificate SHA256        6bb182760205190ad635ef34c21eca6221d2224e2dcdb585f70c157fad76321c
certificate result        2228116225baa95c31a7b8b0f13d222b623f5973b0f8c8e12366f9b4464681e6
verifier SHA256           5f80c85400d238fae0a697bec91312706fb6785f9dc4607edd6782d261dd9df0
verification SHA256       686e236dbe998c111a0307e3edfd34d0b26185b6f52ec54fa33e340725655ee5
verification result       2d67c62756c8b4811f7537e1ede92c8b77861caee58178ead7105958e2920d1f
```

Ten fully re-signed semantic attacks and four strict JSON/encoding attacks
are rejected.  Two producer and two verifier cold runs under distinct hash
seeds are byte-identical to the formal artifacts.

## Strict nonpromotion

Round150 joins the Round146 collision-three D0 frontier and the terminal C24
frontier to one connected certified local skeleton.  It does not exhaust the
maximal component's beta extent, every component exit, or every competing
physical event family.

```text
Round144 D02                         BLOCKED
D03 negative oracle            unauthorized
least maximal-component rank          null
component_v1_id                       null
global Gate5                         10/18
global complete blocks                   0
CM2                        NO-GO_FOR_CLAIM
```
