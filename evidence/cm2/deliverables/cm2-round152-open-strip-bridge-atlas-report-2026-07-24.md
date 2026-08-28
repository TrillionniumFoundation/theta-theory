# CM2 Round152 — typed open-strip bridge atlas

Date: 2026-07-24

## Result

Round152 fills the complete strip between the two Round151 boundary graphs
on the certified x corridor. Its exact status is

```text
CERTIFIED_63_BOX_TYPED_OPEN_STRIP_ATLAS_AND_INTERIOR_EVENT_EXHAUSTION_ON_X_CORRIDOR__D02_STILL_BLOCKED
```

The physical coordinates remain

```text
delta_x    = x - x_star
delta_beta = (asin(p) - 4 r) - b_star
h          = 2^-4296.
```

## Typed strip

For each of the 21 exact x slabs in

```text
abs(delta_x)/h in [1,1169/8],
```

Round152 inserts one strict-return bridge cell between the upper beta face
of the lower terminal-C24 event box and the lower beta face of the upper
collision-three D3 event box.

Each slab therefore has the exact vertical chain

```text
typed C24 event box
strict RETURN bridge
typed D3 event box.
```

The adjacent pieces share exact beta faces, so every chain has no vertical
gap. The actual C24 and D3 graphs lie inside their respective event boxes;
therefore the complete graph-to-graph strip is covered by typed boxes.

The atlas contains

```text
inherited lower C24 event boxes       21
new strict RETURN bridge cells        21
inherited upper D3 event boxes        21
total typed boxes                     63
```

The bridge cells have 20 exact x-face adjacencies with strict beta overlap.
They also have 42 exact boundary attachments. Together with Round151's 40
inherited boundary-graph x adjacencies, the complete typed atlas is
connected.

## Collision-three exclusion

Raw interval evaluation of the physical anchor discriminant over a wide
bridge can overwrap. Round152 avoids that dependency loss rather than
subdividing into 149 narrow cells.

On every complete bridge, both D3 coordinate derivatives are strictly
positive. The exact upper-right parameter corner is strictly negative.
Thus

```text
D3 < 0
```

on the entire bridge, and anchor `W[0,0]` is rigorously absent.

The retained 57-candidate and complete 161-candidate collision-three
universes are then audited with the physical anchor excluded independently.
All 160 nonanchor radius-four candidates are strict and the unique frozen
winner is

```text
W[0,-1].
```

## Terminal return

Wide-bridge interval propagation can leave the terminal `p=p0` inequality
unresolved even though all other core constraints are strict. Round152
separates these issues.

For every bridge:

- all non-event margins of the expected terminal core are strict;
- every competing terminal core is strictly excluded;
- `terminal_p+1/50` is strictly positive on the lower beta face; and
- its beta derivative is strictly positive on the entire bridge.

Consequently `terminal_p+1/50` is strictly positive everywhere on the
bridge, forcing

```text
RETURN_AT_3_INNER
```

to the expected destination core.

## Event exhaustion

Every bridge replays the complete 1,648-stage owner, official-word, wall,
chart, H0 homogeneity, incidence and core path. All radius-four candidate
decisions are strict at every collision. Hence there is no untyped owner,
wall, chart, homogeneity, incidence or core event surface inside any bridge.

The only boundary event families on the certified corridor are the two
already typed by Round151:

```text
COLLISION1648_TERMINAL_C24_P0_ZERO
COLLISION3_D0_TANGENCY_D3_ZERO.
```

Thus the graph-to-graph strip has zero untyped interior event cells on the
certified x corridor.

## Audit census

```text
new full R1648 bridge audits                  21
new collision-stage/bridge pairs         34,608
new full radius-four candidate tests   5,571,888
additional retained collision-3 tests       1,197
```

Every bridge has official-path SHA256
`f504289edce554d47e17a90d7c886586a69f3ec4b64fafd90c718c50ca93221e`
and compact-path SHA256
`c37571201fa15065a7f8e4eeec9df5a79f36e077feac37a1aec7b910970e1f17`.

## Independent verification

The verifier imports or executes neither the producer nor its result
builder. It independently reconstructs all 21 full bridge audits, the 63-box
count, all 20 bridge x adjacencies, all 42 boundary attachments and the
interior-event exhaustion.

```text
engine SHA256             21c3c7dbce2a288489f5de109df98f90a768d2d42db2fd3c7cc74bbb74134738
producer SHA256           4e57731a6c2649991f04b24482fb196c7c051e4f97022e8dddc0d3747218fb7d
certificate SHA256        f5f3ff201706ecd27bee6d3c668e67fa6a549cdcdf484ae7759ccf31eb45118f
certificate result        c98f7dc36a3a1bf9aaf5527890f2d9521dd7d66ed21178fe39bdacb6b8f1c5ff
verifier SHA256           eef21b3dde024b2e0b5f9623b7d641387778702420afc329792e355cce319534
verification SHA256       0cadd6786867906a1afc4eae290fa19b9e241f72b0a4505ebb95a699060b5600
verification result       7410da7fc0fa7c692a99b7626bdd4d54031f4caa71cdd61707c361db0eb6ff14
```

Ten fully re-signed semantic attacks and four strict JSON/encoding attacks
are rejected.

## Strict nonpromotion

Round152 exhausts the graph-to-graph beta strip only on the certified x
corridor. It does not continue either endpoint to a terminal maximal-
component exit or exclude additional disconnected or exterior component
sheets.

```text
Round144 D02                         BLOCKED
D03 negative oracle            unauthorized
least maximal-component rank          null
component_v1_id                       null
global Gate5                         10/18
global complete blocks                   0
CM2                        NO-GO_FOR_CLAIM
```

The next core attack is two-sided x-endpoint continuation of the complete
typed strip, stopping only at certified terminal exits or explicitly typed
new event families.
