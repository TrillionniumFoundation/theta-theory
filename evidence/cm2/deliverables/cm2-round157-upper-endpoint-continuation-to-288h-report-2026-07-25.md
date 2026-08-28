# CM2 Round157 — upper endpoint continuation to 288h

Date: 2026-07-25

## Result

Round157 continues the connected typed atlas from `abs(delta_x)/h=256` to
`288`. Its exact status is

```text
CERTIFIED_TYPED_UPPER_ENDPOINT_CONTINUATION_TO_288H__D02_STILL_BLOCKED
```

The combined certified corridor is now `abs(delta_x)/h in [0,288]`.

## Dependency-controlled continuation

Eight exact 4h slabs cover `[256,288]`. Every slab has the certified gap-free
chain

```text
typed terminal-C24 event box
strict RETURN_AT_3_INNER bridge
typed collision-three D3 event box.
```

The C24 upper beta endpoint equals the bridge lower endpoint, and the bridge
upper endpoint equals the D3 lower endpoint, on every slab. All shared x faces,
including the inherited `256h` face, have strict beta overlap in all three
families. No new event family appears.

## Combined atlas

```text
exact x slabs                        57
typed C24 event boxes                57
typed strict-RETURN bridge cells     57
typed D3 event boxes                 57
total typed boxes                   171
untyped interior event cells          0
```

The lower symmetry-axis endpoint remains terminal. The upper endpoint at
`288h` is not claimed terminal.

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

Unlike the prior certificate schema, Round157 records the D3 and total
radius-four counts directly in the certificate census.

## Independent verification

The verifier imports or executes neither the producer nor its result builder.
It independently reconstructs all eight new C24 boxes, bridges and D3 boxes,
the inherited `256h` adjacency, the seven internal adjacencies, and the
combined 171-box atlas.

It also:

- validates and cross-binds the Round156 certificate and verification;
- checks the complete certificate wrapper, schema, result digest, status,
  scale, inherited digest, census, nonpromotion and next gate;
- uses canonical type-sensitive equality and binds embedded rows to their own
  digest and the independently reconstructed digest;
- explicitly checks every x/beta seam;
- rejects coherent row mutations and row reordering even when the attacker
  recomputes both the embedded rows digest and the top-level result digest;
- rejects floating-point JSON and seven additional JSON/encoding attacks.

```text
boundary engine SHA256  dca8a2bc670411074703d4a87a5557649fa3506fbcb4e62a144cb81e01a22085
bridge engine SHA256    21c3c7dbce2a288489f5de109df98f90a768d2d42db2fd3c7cc74bbb74134738
producer SHA256         3d50250036db578101435129f9d44d44728cdaf478ca4848a67aaf6af77ab929
certificate SHA256      3c25d0f3fc813c8e26760c54cee858a463dcafa65721129c3a58d5463af28351
certificate result      b710d5f24642219a6d66db8de8ae7b63461616bddbb1518cbe4c80f1699ee913
verifier SHA256         c32ec1384c091c9f20afc6eb77c72b3f87a909a5bd4e6041afd5390ca20e729a
verification SHA256     724e35ea187096be6dee38639e1259a90c14924c7ebc9524bfdfbc6bf4150851
verification result     ea620007fd4d919b05be3f211d08a69a2e8b4438c299665283784d18d9147d56
```

Twenty-six semantic/document attacks and eight strict JSON/encoding attacks
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

The next core attack continues beyond `288h` with 4h C24-controlled slabs
until a certified terminal exit or newly typed event family is reached, then
excludes disconnected exterior sheets.
