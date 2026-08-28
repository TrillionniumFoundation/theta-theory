# CM2 Round154 — upper endpoint continuation to 192h

Date: 2026-07-25

## Result

Round154 continues the connected typed atlas from `abs(delta_x)/h=160` to
`192`. Its exact status is

```text
CERTIFIED_TYPED_UPPER_ENDPOINT_CONTINUATION_TO_192H__D02_STILL_BLOCKED
```

The combined certified corridor is now

```text
abs(delta_x)/h in [0,192].
```

## Adaptive continuation

Five new exact x slabs cover `[160,192]`:

```text
[160,164]
[164,168]
[168,176]
[176,184]
[184,192]
```

Direct 16h-wide C24 enclosures beyond `192h` overwrap through interval
dependency. Round154 does not treat that numerical overwrap as an event.
Instead it uses dependency-controlled 4h and 8h slabs, on which the C24 and
D3 graphs remain unique, transverse, face-connected and of the same event
families as before.

Every new slab has the gap-free typed chain

```text
typed terminal-C24 event box
strict RETURN bridge
typed collision-three D3 event box.
```

Successive slabs, including the inherited `160h` face, have strict beta
overlap in all three families.

## Combined atlas

```text
exact x slabs                         33
typed C24 event boxes                 33
typed strict-RETURN bridge cells      33
typed D3 event boxes                  33
total typed boxes                     99
untyped interior event cells           0
```

The lower symmetry-axis endpoint remains terminal. The upper endpoint at
`192h` is explicitly not claimed terminal. No new event family appears on
the enlarged corridor.

## New audit census

```text
new complete R1648 C24 audits                 5
new complete R1648 bridge audits              5
new collision-stage/object pairs         16,480
new full radius-four candidate tests  2,653,280
new complete D3 event-box audits              5
```

Every new bridge is forced to `RETURN_AT_3_INNER`; all owner, official-word,
wall, chart, homogeneity, incidence, core and radius-four candidate decisions
remain strict.

## Independent verification

The verifier imports or executes neither the producer nor its result builder.
It independently reconstructs all five new C24 boxes, bridges and D3 boxes,
the exact face adjacencies, and the combined 99-box atlas.

```text
boundary engine SHA256  dca8a2bc670411074703d4a87a5557649fa3506fbcb4e62a144cb81e01a22085
bridge engine SHA256    21c3c7dbce2a288489f5de109df98f90a768d2d42db2fd3c7cc74bbb74134738
producer SHA256         e6a6d8ed366082199b619027cedd2e2dc1de29816793b9e7311924fd0a31b19d
certificate SHA256      2a57ff7f5d095f50b4de679bdc54a9221dbe70b83dfc6cab02d4e819afa84a32
certificate result      361532f74e966f26a460f3c90db59456f5d25b62947254fce3abcd3c0575289d
verifier SHA256         d07b2594c35dbf426efab6b4650cad672535accc2d6fcae753bcdfac61a4a80e
verification SHA256     b3b8ee375aea480d5571b56759a72f1da15752d98213b8f09203d6788a96b2ce
verification result     cd34e677323ffb659e34fd44b7b6569aec2ee394cd6e51eb2920ff9a92ca8af0
```

Ten semantic attacks and four strict JSON/encoding attacks are rejected.
Producer and verifier cold replays under distinct hash seeds are byte
identical.

## Strict nonpromotion

```text
Round144 D02                         BLOCKED
D03 negative oracle            unauthorized
global Gate5                         10/18
global complete blocks                   0
CM2                        NO-GO_FOR_CLAIM
```

The next core attack continues beyond `192h` with narrower C24
dependency-controlled slabs until a certified terminal exit or explicitly
typed new event family is reached, followed by disconnected exterior-sheet
exclusion.
