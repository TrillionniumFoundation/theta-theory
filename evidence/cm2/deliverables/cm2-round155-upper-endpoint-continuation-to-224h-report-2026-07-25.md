# CM2 Round155 — upper endpoint continuation to 224h

Date: 2026-07-25

## Result

Round155 continues the connected typed atlas from `abs(delta_x)/h=192` to
`224`. Its exact status is

```text
CERTIFIED_TYPED_UPPER_ENDPOINT_CONTINUATION_TO_224H__D02_STILL_BLOCKED
```

The combined certified corridor is now `abs(delta_x)/h in [0,224]`.

## Dependency-controlled continuation

Eight exact 4h slabs cover `[192,224]`. Wider 8h C24 probes beyond `200h`
overwrap, while every 4h recut has a unique transverse C24 graph and a unique
transverse D3 graph. No numerical overwrap is reinterpreted as a physical
event.

Every slab has the gap-free chain

```text
typed terminal-C24 event box
strict RETURN bridge
typed collision-three D3 event box.
```

All inherited and new shared x faces have strict beta overlap in all three
families. No new event family appears.

## Combined atlas

```text
exact x slabs                        41
typed C24 event boxes                41
typed strict-RETURN bridge cells     41
typed D3 event boxes                 41
total typed boxes                   123
untyped interior event cells          0
```

The lower symmetry-axis endpoint remains terminal. The upper endpoint at
`224h` is not claimed terminal.

## New audit census

```text
new complete R1648 C24 audits                 8
new complete R1648 bridge audits              8
new collision-stage/object pairs         26,368
new full radius-four candidate tests  4,245,248
new complete D3 event-box audits              8
```

Every new bridge is forced to `RETURN_AT_3_INNER`; all path and candidate
decisions remain strict.

## Independent verification

The verifier imports or executes neither the producer nor its result builder.
It independently reconstructs all eight new C24 boxes, bridges and D3 boxes,
all exact-face adjacencies, and the combined 123-box atlas.

```text
boundary engine SHA256  dca8a2bc670411074703d4a87a5557649fa3506fbcb4e62a144cb81e01a22085
bridge engine SHA256    21c3c7dbce2a288489f5de109df98f90a768d2d42db2fd3c7cc74bbb74134738
producer SHA256         9d01c6572c5e0ce27362d05984acb025f83f2109b6cacc8961edcc95d259b636
certificate SHA256      5f39bf9d54469554397903cbb376ca41d7b623b13f1597cc0d2b3fd91d5f74cd
certificate result      b182a2223c5d8b9560acdb4eee8031b93b0a79bed84bb24ef8697248d6e8bf13
verifier SHA256         77a05d1fa2a53294dfbf7b430438857cad315a1af8f91846552317b44edf80d9
verification SHA256     5b0743612e83d6c805367a92bccbf9eb3dea63d1a749310db2d32826e2df5312
verification result     dd7afee6829d04a37757e94113ccd3dd8bcabc40ba7b7b7e611e85b5fbcb8cdd
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

The next core attack continues beyond `224h` with 4h C24-controlled slabs
until a certified terminal exit or newly typed event family is reached, then
excludes disconnected exterior sheets.
