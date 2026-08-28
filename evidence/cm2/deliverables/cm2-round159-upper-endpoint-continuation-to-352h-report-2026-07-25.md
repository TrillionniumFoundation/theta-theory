# CM2 Round159 — upper endpoint continuation to 352h

Date: 2026-07-25

## Result

Round159 continues the connected typed atlas from `abs(delta_x)/h=320` to
`352`. Its exact status is

```text
CERTIFIED_TYPED_UPPER_ENDPOINT_CONTINUATION_TO_352H__D02_STILL_BLOCKED
```

The combined certified corridor is now `abs(delta_x)/h in [0,352]`.

## Dependency-controlled continuation

Eight exact 4h slabs cover `[320,352]`. Every slab has the certified gap-free
chain

```text
typed terminal-C24 event box
strict RETURN_AT_3_INNER bridge
typed collision-three D3 event box.
```

The C24 upper beta endpoint equals the bridge lower endpoint, and the bridge
upper endpoint equals the D3 lower endpoint, on every slab. All shared x faces,
including the inherited `320h` face, have strict beta overlap in all three
families. No new event family appears.

## Combined atlas

```text
exact x slabs                        73
typed C24 event boxes                73
typed strict-RETURN bridge cells     73
typed D3 event boxes                 73
total typed boxes                   219
untyped interior event cells          0
```

The lower symmetry-axis endpoint remains terminal. The upper endpoint at
`352h` is not claimed terminal.

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

The producer and verifier derive these counts from the reconstructed row
audits. Combined atlas counts are derived from the pinned Round158 atlas rather
than repeated as an independent hard-coded claim.

## Independent verification

The verifier imports or executes neither the producer nor its result builder.
It independently reconstructs all eight new C24 boxes, bridges and D3 boxes,
the inherited `320h` adjacency, the seven internal adjacencies, and the
combined 219-box atlas.

It also:

- validates and cross-binds the complete Round158 certificate and verification
  wrappers, recording both inherited result digests;
- checks that the imported boundary and bridge modules resolve to the exact
  pinned files under the deliverables directory;
- checks the complete certificate wrapper, schema, result digest, status,
  scale, inherited digests, dynamically derived census, nonpromotion and next
  gate;
- uses canonical type-sensitive equality and binds embedded rows to their own
  digest and the independently reconstructed digest;
- explicitly reconstructs every x/beta seam, including the inherited face and
  a non-first internal face;
- recursively rejects decoded NUL and Unicode surrogate code points in JSON
  keys and values, in addition to rejecting every floating-point spelling;
- rejects coherent row, inheritance, atlas-count, continuation-count,
  adjacency and census mutations even when all affected wrapper digests are
  recomputed.

```text
boundary engine SHA256  dca8a2bc670411074703d4a87a5557649fa3506fbcb4e62a144cb81e01a22085
bridge engine SHA256    21c3c7dbce2a288489f5de109df98f90a768d2d42db2fd3c7cc74bbb74134738
producer SHA256         0f09860ba205110c99aed379fc7e1b5349c005635644737a5bc9fe903ee4bda9
certificate SHA256      9af879463f5e300f07d3ec88642757c86a8cca214986eb8f1f908a511f39f142
certificate result      841c237bd774d48513061a380865dd423151129c8db651baf45f4c91f3f8b6f6
verifier SHA256         b55c6f8b1c4aea8626a26dd193cbde8622089f7cf7287ab0d367e86d053b206a
verification SHA256     d3a787d242e2cb485955553b52e1a95c9044b8075291b981f933973bfbfac059
verification result     64ac7427197b37d3da1aa3228acbf2036bdf499025e4a2fde2056b32f865805f
```

Thirty-five semantic/document attacks and twelve strict JSON/encoding attacks
are rejected. Producer and verifier cold replays under distinct hash seeds are
byte identical.

## Upper-tail method decision

A nonpromotional exact diagnostic at the 4h slab centered on `100000h` still
passes the C24 frontier, strict bridge anchor/return tests and D3 frontier. Its
C24 and D3 interval-Newton images remain separated by more than `398.8004h`.
By contrast, a single C24 box spanning `[320,100000]h` fails with interval
overwrap (`nonpositive discriminant:[+/- 0.101]`) and does not classify a
physical event.

This shows that repeating 4h slabs is not an effective route to the actual
E-chart exit. The exact initial-state map is naturally expressed in compact
angles `(A,Phi)`, and the first negative E-chart face occurs only at an
estimated scale `u_E approximately 2^4295.087` in h units. The next operational
attack therefore prioritizes a validated scale jump in compact angular
coordinates, with 4h continuation retained as the conservative fallback. The
separate scale-jump feasibility note records the formulas, diagnostic scope and
required proof obligations.

## Strict nonpromotion

```text
Round144 D02                         BLOCKED
D03 negative oracle            unauthorized
global Gate5                         10/18
global complete blocks                   0
CM2                        NO-GO_FOR_CLAIM
```

Round159 does not certify the diagnostic far slab or any tail beyond `352h`.
The next core attack is to construct a validated compact-angle scale-jump
certificate to the first chart/owner/event face, then perform disconnected
exterior-sheet exclusion over a fundamental angular domain.
