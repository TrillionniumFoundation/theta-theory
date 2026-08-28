# CM2 Round156 — upper endpoint continuation to 256h

Date: 2026-07-25

## Result

Round156 continues the connected typed atlas from `abs(delta_x)/h=224` to
`256`. Its exact status is

```text
CERTIFIED_TYPED_UPPER_ENDPOINT_CONTINUATION_TO_256H__D02_STILL_BLOCKED
```

The combined certified corridor is now `abs(delta_x)/h in [0,256]`.

## Dependency-controlled continuation

Eight exact 4h slabs cover `[224,256]`. Every slab has a unique transverse C24
graph, a strict RETURN bridge, and a unique transverse D3 graph. The certified
gap-free vertical chain is

```text
typed terminal-C24 event box
strict RETURN bridge
typed collision-three D3 event box.
```

The C24 upper beta endpoint equals the bridge lower endpoint, and the bridge
upper endpoint equals the D3 lower endpoint, on every slab. All shared x faces,
including the inherited `224h` face, have strict beta overlap in all three
families. No new event family appears.

## Combined atlas

```text
exact x slabs                        49
typed C24 event boxes                49
typed strict-RETURN bridge cells     49
typed D3 event boxes                 49
total typed boxes                   147
untyped interior event cells          0
```

The lower symmetry-axis endpoint remains terminal. The upper endpoint at
`256h` is not claimed terminal.

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

Every new bridge is forced to `RETURN_AT_3_INNER`; all path and candidate
decisions remain strict.

## Independent verification

The verifier imports or executes neither the producer nor its result builder.
It independently reconstructs all eight new C24 boxes, bridges and D3 boxes,
the inherited `224h` adjacency, the seven internal adjacencies, and the
combined 147-box atlas.

The Round156 verifier also closes several inherited verifier blind spots:

- it pins and validates the Round155 certificate and verification;
- it checks the certificate schema, status, physical scale, inherited result
  digest, complete census, strict nonpromotion and next gate;
- it recomputes every exact adjacency object rather than checking only its
  count;
- it uses canonical type-sensitive equality, binds embedded rows to both their
  own digest and the independently reconstructed digest, and explicitly checks
  the gap-free x/beta chain.

```text
boundary engine SHA256  dca8a2bc670411074703d4a87a5557649fa3506fbcb4e62a144cb81e01a22085
bridge engine SHA256    21c3c7dbce2a288489f5de109df98f90a768d2d42db2fd3c7cc74bbb74134738
producer SHA256         43fd7676ab979539cffffa9077a83c3d12c252110c2bef4dac1fa59bb43480c7
certificate SHA256      3d4deffd799cfc3b01ddcd48bc8784c165a7b9778603facbcdc01d414f2ec347
certificate result      b5e6b6d9fc596f5e005c568cc4dcd3d11cca8cc9c80ce323635c02c55f0df4a5
verifier SHA256         5d98dcce0751b342586f3c977d9cc4d983b624c98dda36e08478b4ff65abc1c6
verification SHA256     f94cd81f563cb14458c50203dbc49e771d26f3dcf3bce92754e4f1dba33f6973
verification result     5e27affce89eb5743368a98c6617cdfc396f66e3af48f7e674efa461e6ad711d
```

Sixteen semantic attacks and four strict JSON/encoding attacks are rejected.
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

The next core attack continues beyond `256h` with 4h C24-controlled slabs
until a certified terminal exit or newly typed event family is reached, then
excludes disconnected exterior sheets.
