# CM2 Round151 — dual-boundary event census

Date: 2026-07-24

## Result

Round151 continues both first beta-direction boundary families over the
entire connected Round150 x corridor. Its exact status is

```text
CERTIFIED_GLOBAL_DUAL_EVENT_GRAPH_CENSUS_ON_CONNECTED_X_CORRIDOR__D02_STILL_BLOCKED
```

The physical coordinates remain

```text
delta_x    = x - x_star
delta_beta = (asin(p) - 4 r) - b_star
h          = 2^-4296.
```

## Global graph census

The exact corridor

```text
abs(delta_x)/h in [1,1169/8]
```

is partitioned into 21 adjacent rational slabs. On every slab Round151
certifies two separate parametric interval-Newton event boxes.

The lower-beta graph is the collision-1648 terminal-core face

```text
terminal_p(delta_x,delta_beta) + 1/50 = 0.
```

Each of its 21 boxes has strictly positive x and beta derivatives, strict
opposite beta-edge signs, and an interval-Newton beta image strictly inside
the box. Therefore every fixed x fibre has exactly one C24 root. Adjacent
boxes share an exact x face and overlapping beta intervals, so uniqueness
forces one face-connected C24 graph across the complete corridor.

The upper-beta graph is the collision-three tangency

```text
D3(delta_x,delta_beta) = 0
```

for anchor candidate `W[0,0]`. Its x and beta derivatives are strictly
positive on all 21 boxes. Every fixed x fibre has exactly one D3 root, and
the same exact-face argument gives one connected D3 graph across the
complete corridor.

## Event ownership

Every C24 event box replays the same complete 1,648-stage owner, official
word, wall, chart, H0 homogeneity and incidence path. At collision 1,648 the
expected destination core

```text
core:e47f553e056452faa012129434cdbbb6a55cd9671a19ea04e6b8a9f43054c4c2
```

is the sole unresolved terminal core, its `p=p0` face is the sole unresolved
core inequality, and every competing terminal constraint is strict.

Every D3 event box fully audits the first two collisions and then both the
57-candidate retained universe and the complete 161-candidate radius-four
universe at collision three. In both universes:

```text
sole unresolved candidate          W[0,0]
frozen winner excluding anchor     W[0,-1]
unresolved event                   D3=0
```

The anchor double-root flight is strictly earlier than the frozen winner on
every box. Thus the D3 graph is an immediate owner-switch boundary rather
than a candidate-set decoration.

## Uniform separation

For each aligned slab, the lower endpoint of the D3 interval-Newton image
is compared with the upper endpoint of the C24 interval-Newton image. The
minimum rigorous difference is approximately

```text
337.37273412942886 h.
```

Consequently the two unique transverse graphs are disjoint over the entire
x corridor with the simpler certified uniform bound

```text
D3 beta - C24 beta > 300 h.
```

This does not prove that the open strip between the graphs is event-free.

## Audit census

```text
C24 full R1648 event boxes                    21
C24 collision-stage/event-box pairs       34,608
C24 radius-four candidate tests         5,571,888
D3 event boxes                                21
D3 collision-stage/event-box pairs            63
D3 radius-four candidate tests            10,143
total event boxes                              42
total collision-stage/event-box pairs      34,671
total radius-four candidate tests        5,582,031
```

All C24 boxes have official-path SHA256
`f504289edce554d47e17a90d7c886586a69f3ec4b64fafd90c718c50ca93221e`.

## Independent verification

The verifier imports or executes neither the producer nor its result
builder. It independently reconstructs all 42 event boxes, both variational
graphs, all 40 exact-face graph adjacencies, the uniform graph separation
and the complete audit census.

```text
engine SHA256             dca8a2bc670411074703d4a87a5557649fa3506fbcb4e62a144cb81e01a22085
producer SHA256           16eac5a2f8974b8908fc2c4f66c1c6625ae2f7b9da31750c47dd715c8b100acb
certificate SHA256        593188b5e9996cfa8151cd15c318a7a6136c108dba123cc91e421c83f7aea821
certificate result        66b495117aa7a31c4d221144240cb8cc1233c6c6ee8b58cf7619d0a123790744
verifier SHA256           6ff30a69afb610143ebca726589dae588ec67a232135babd6274eef05ba3c2fc
verification SHA256       61e053ca782cd030bb6d3a182e7ff4f032e4d6bb2fadf1fa82682789908ae1cd
verification result       eee4a736efd6b3cd7913fcafa28b371a77382d9c228f55b843f6be799445874d
```

Ten fully re-signed semantic attacks and four strict JSON/encoding attacks
are rejected.

## Strict nonpromotion

Round151 upgrades the two local frontier types into two global graphs on
the certified x corridor. It does not tile the open strip between them,
exclude every possible interior event surface, continue either graph beyond
the corridor endpoints, or certify a maximal two-dimensional component.

```text
Round144 D02                         BLOCKED
D03 negative oracle            unauthorized
least maximal-component rank          null
component_v1_id                       null
global Gate5                         10/18
global complete blocks                   0
CM2                        NO-GO_FOR_CLAIM
```

The next core attack is an adaptive two-dimensional tiling of the open
C24-to-D3 strip, with every residual event cell either fully classified or
given an explicit cemetery type.
