# CM2 Round158 — upper endpoint continuation to 320h

Date: 2026-07-25

## Result

Round158 continues the connected typed atlas from `abs(delta_x)/h=288` to
`320`. Its exact status is

```text
CERTIFIED_TYPED_UPPER_ENDPOINT_CONTINUATION_TO_320H__D02_STILL_BLOCKED
```

The combined certified corridor is now `abs(delta_x)/h in [0,320]`.

## Dependency-controlled continuation

Eight exact 4h slabs cover `[288,320]`. Every slab has the certified gap-free
chain

```text
typed terminal-C24 event box
strict RETURN_AT_3_INNER bridge
typed collision-three D3 event box.
```

The C24 upper beta endpoint equals the bridge lower endpoint, and the bridge
upper endpoint equals the D3 lower endpoint, on every slab. All shared x faces,
including the inherited `288h` face, have strict beta overlap in all three
families. No new event family appears.

## Combined atlas

```text
exact x slabs                        65
typed C24 event boxes                65
typed strict-RETURN bridge cells     65
typed D3 event boxes                 65
total typed boxes                   195
untyped interior event cells          0
```

The lower symmetry-axis endpoint remains terminal. The upper endpoint at
`320h` is not claimed terminal.

## New audit census

```text
new complete R1648 C24 audits                       8
new complete R1648 bridge audits                    8
new collision-stage/object pairs               26,368
new R1648-path radius-four candidate tests   4,245,248
new complete D3 event-box audits                    8
new D3 event-box radius-four candidate tests    3,864
new total radius-four candidate tests       4,249,112
```

All three candidate-test census fields are directly bound into the certificate
and independently reconstructed by the verifier.

## Independent verification

The verifier imports or executes neither the producer nor its result builder.
It independently reconstructs all eight new C24 boxes, bridges and D3 boxes,
the inherited `288h` adjacency, the seven internal adjacencies, and the
combined 195-box atlas.

It also:

- validates and cross-binds the Round157 certificate and verification;
- checks the complete certificate wrapper, schema, result digest, status,
  scale, inherited digest, census, nonpromotion and next gate;
- uses canonical type-sensitive equality and binds embedded rows to their own
  digest and the independently reconstructed digest;
- explicitly checks every x/beta seam, including a coherent inherited-face
  mutation;
- rejects coherent row, census-total and row-order mutations even when the
  attacker recomputes all affected document digests;
- rejects all floating-point JSON, including finite and overflow spellings,
  plus seven other JSON/encoding attacks.

```text
boundary engine SHA256  dca8a2bc670411074703d4a87a5557649fa3506fbcb4e62a144cb81e01a22085
bridge engine SHA256    21c3c7dbce2a288489f5de109df98f90a768d2d42db2fd3c7cc74bbb74134738
producer SHA256         8731fac2ae5f89bd15736b379969f83ff3bc8e2358353acc643ab07456c763c9
certificate SHA256      9b7196d43f608a1a83f9eb98116fa8a3f7b4c41e3bc89fee2724f51dcecf53c6
certificate result      79c330cc92be3d00c7500f5e76a52fbf9180647a52ea508de1537e2410caa5b3
verifier SHA256         fc94817bd8288a54f65162750847643d6b5b475efbcb5e3cb9f7324e41d21034
verification SHA256     5c814d68f68732a527fd769db773a955f3281fc733d88fd585ffac249f03fd9b
verification result     50273f316effa92b3fd309ec0868872456e98a41de9f78b8c9bfb950e4c19e37
```

Twenty-eight semantic/document attacks and nine strict JSON/encoding attacks
are rejected. Producer and verifier cold replays under distinct hash seeds are
byte identical.

## Strict nonpromotion

```text
Round144 D02                         BLOCKED
D03 negative oracle            unauthorized
global Gate5                         10/18
global complete blocks                   0
CM2                        NO-GO_FOR_CLAIM
```

The next core attack continues beyond `320h` with 4h C24-controlled slabs
until a certified terminal exit or newly typed event family is reached, then
excludes disconnected exterior sheets.
