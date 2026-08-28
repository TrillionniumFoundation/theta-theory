# CM2 Round153 — two-sided endpoint continuation

Date: 2026-07-25

## Result

Round153 continues the complete Round152 typed strip in both x directions.
Its exact status is

```text
CERTIFIED_TWO_SIDED_TYPED_STRIP_CONTINUATION_TO_SYMMETRY_AXIS_AND_160H__D02_STILL_BLOCKED
```

The certified corridor is enlarged from

```text
abs(delta_x)/h in [1,1169/8]
```

to

```text
abs(delta_x)/h in [0,160].
```

## Endpoint continuation

Seven new exact x slabs were audited: one lower slab `[0,1]` and six upper
slabs covering `[1169/8,160]`. Every new slab has the same gap-free typed
vertical chain

```text
typed terminal-C24 event box
strict RETURN bridge
typed collision-three D3 event box.
```

All three pieces share exact beta faces within a slab. Successive upper
slabs have exact x faces and strict beta overlap in all three families. The
new lower slab has strict face overlap with the first inherited Round152
slab in the C24, bridge, and D3 families.

The lower continuation reaches `abs(delta_x)=0`, the terminal endpoint of
the absolute-x coordinate domain. The upper endpoint at `160h` is not
claimed terminal.

## Typed atlas

The combined Round152–153 atlas contains

```text
exact x slabs                         28
typed C24 event boxes                 28
typed strict-RETURN bridge cells      28
typed D3 event boxes                  28
total typed boxes                     84
untyped interior event cells           0
```

No new event family appears on the enlarged corridor. The only certified
boundary families remain

```text
COLLISION1648_TERMINAL_C24_P0_ZERO
COLLISION3_D0_TANGENCY_D3_ZERO.
```

## New audit census

```text
new complete R1648 C24 audits                 7
new complete R1648 bridge audits              7
new collision-stage/object pairs         23,072
new full radius-four candidate tests  3,714,592
new complete D3 event-box audits              7
```

Every new C24 and bridge object replays the complete 1,648-stage owner,
official-word, wall, chart, homogeneity, incidence and core path. Every
bridge is forced to `RETURN_AT_3_INNER`; all collision-three anchor and
full radius-four candidate decisions remain strict.

## Independent verification

The verifier imports or executes neither the producer nor its result
builder. It independently reconstructs all seven new C24 boxes, bridges and
D3 boxes, recomputes the 84-box connected atlas, and checks the symmetry-axis
termination.

```text
boundary engine SHA256  dca8a2bc670411074703d4a87a5557649fa3506fbcb4e62a144cb81e01a22085
bridge engine SHA256    21c3c7dbce2a288489f5de109df98f90a768d2d42db2fd3c7cc74bbb74134738
producer SHA256         dfa3ae4931472ff6d82d720a427c6119defdd67753b3587d5d0cb22ea9b7f3c6
certificate SHA256      7af5541e16abbfc5f72889b50be81000e6dbddc2123b98e4c7371432409af91d
certificate result      883c5def0f89e2fa7471d9a925e102f8e3483690833caaa9edf2e5096e98d8bf
verifier SHA256         0ca7500ce8782f8ae09dd51bfea666d31a1d65144833af0938648b961bc8e616
verification SHA256     1931acb9a753b727ce96959d0b64c36c697e7f018343cb23bb552d8a459f8e81
verification result     0755012ecfd7659ef42d213459404cff3d6be68f620c685158e46252414af783
```

Ten semantic attacks and four strict JSON/encoding attacks are rejected.
Producer and verifier cold replays under distinct hash seeds are byte
identical to the sealed outputs.

## Strict nonpromotion

Round153 closes only the lower absolute-x endpoint. The upper continuation
beyond `160h` and exclusion of disconnected exterior component sheets remain
incomplete.

```text
Round144 D02                         BLOCKED
D03 negative oracle            unauthorized
global Gate5                         10/18
global complete blocks                   0
CM2                        NO-GO_FOR_CLAIM
```

The next core attack is upper-endpoint continuation beyond `160h`, stopping
only at a certified terminal exit or an explicitly typed new event family,
while continuing the exterior-sheet exclusion.
