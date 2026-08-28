# Round217 source-G internal-face trace/glue materialization

## Verdict

`FORMAL_BOUNDED_PREFIX__EXACT_FULL_FACE_P_S_ZERO_TRACES_AND_COMMON_REFINEMENT_GLUE_MATERIALIZED__PHYSICAL_COMPONENT_QUOTIENT_STILL_INCOMPLETE`

Round217 formally materializes the largest whole-face prefix supported by the
pinned Round208/Round211 schema:

- 448 exact full-face active-factor zero traces;
- 896 two-sided trace incidences; and
- 448 exact common-refinement glue rows.

The accepted contacts split as:

| axis/relation | accepted contacts |
|---|---:|
| exact `p`, cross-origin | 416 |
| exact `s`, same occurrence | 32 |
| **total** | **448** |

Every accepted common face has:

1. identical parent-atlas identity on both sides;
2. exactly equal rational common-face geometry;
3. identical source chart, target lift, active factor, owner cell, signature
   core, and official key ordinal;
4. strict opposite selected active-factor C0 signs on the two complete
   transverse `t` endpoint edges; and
5. a strict `d/dt` enclosure on the entire common face, oriented consistently
   with the endpoint signs.

The endpoint C0 selection uses the direct interval when strict and otherwise
the pinned centered enclosure.  A Round214 midpoint witness alone is not
accepted as a whole-face trace proof.

The 448 glue rows are local exact-equivalence evidence.  They are not called
physical components: transitive component exhaustion is incomplete, and all
component, whole-leaf, whole-origin, whole-tube, global-fibre, and exact-key
disposition credits remain zero.

## Formal artifacts

- Producer:
  `cm2_round217_source_g_internal_face_trace_glue_materialization.py`
  - SHA256:
    `687fd48134e204a99c807e1fd18954cef7633879396db5f4d291ece1568dfa66`
- Certificate:
  `cm2_round217_source_g_internal_face_trace_glue_materialization_certificate.json`
  - SHA256:
    `1ccf9b4bf65bb4f45603594ea19f47e3b2103ea682bebfff0b023234308938fd`
  - result SHA256:
    `fb4519a43f76cbc765e24b3cb0a0e25267d9664091e22139913f3899fd1e2286`
- Independent verifier:
  `cm2_round217_source_g_internal_face_trace_glue_materialization_verifier.py`
  - SHA256:
    `172167d8e0c992645e0e5f546628be052868275808a5db733f3e5507daecaf71`
- Verification:
  `cm2_round217_source_g_internal_face_trace_glue_materialization_verification.json`
  - SHA256:
    `13b6b3d3b2879d950c722e1ce92ad729f207a6abbb433d08acf0e22ae0d4cbda`
  - result SHA256:
    `48dd5123517f07bda9aa84ce76edd8e10e3baf1cc3924ad9e1398c1f3f28fb75`
  - status: `PASS_PARTIAL_FORMAL_ROUND217`

The official producer run (`PYTHONHASHSEED=217052`) completed in `2:02.04`
with maximum RSS `1,499,544 KiB`.  Isolated producer replays at seeds
`217051` and `217053` completed in `2:04.11` / `1:59.51`, with maximum RSS
`1,500,036 KiB` / `1,499,848 KiB`.  Both isolated outputs are byte-identical
to the official certificate and have the same certificate, result, and
producer-provenance hashes.

The official verifier run (`PYTHONHASHSEED=217061`) completed in `4:35.14`
with maximum RSS `3,059,048 KiB`.  Its isolated replay at seed `217062`
completed in `4:31.14` with maximum RSS `3,059,416 KiB`; the two verification
files are byte-identical.

## Frozen input boundary

The producer and verifier directly pin:

- Round204 source:
  `7e4b81846155c1edad0807362c7086a290702da7ce6680d7c449b7193635da77`
- Round204 certificate:
  `e7e1c49bebcb8c01f0fb4b33af66e4f2a8de560f121cae65f4971b2fec3e1818`
- Round204 result:
  `ef106d06399094a453eb5e66d73a0022a9bb5343f8c4788b3a3fbc9177d45ccd`
- Round208 source:
  `c9fe0cdfb4631c31702473d705b04fa89fb8d51e4c71c9b2b652dc98e4641913`
- Round208 certificate:
  `4d01fb9cee639ec59786c078f7a20b3bbcd5c18ea674fabbfce64e250e765938`
- Round208 result:
  `d00674fa4061364539ce6f36f6f8de938f50bc54afbf5497266dcfa0e078bca8`
- Round211 source:
  `9e8874672150d7585316524a7724070f4543e231de5481d1c1dfbd00ddc65a02`
- Round211 certificate:
  `bb03a39a74a237b9f4449214c698795856fce4d6be2195c4f9d7774cd1d4183f`
- Round211 result:
  `3b831c67669e52f1247ea30c0a1ed7d5c1002931a1c0f621dd934085e87c2d5b`
- Round214 probe:
  `d074aa045637ce1bb31768fa551bdb73ceda6a58c760cafe3dbf92faa7c922fe`
- Round214 report:
  `aa48c012fa8c57df89b2bea4123467fc2c74821a03525095976cb61c709fe952`
- Round214 result:
  `ddc12c8e625a5a65cc8e445d97ee89e64429a6c729efe32778a092f7e6521d09`
- Round214 canonical document:
  `9a90e2f01cf03b263803298ba1977c9ecfa6e70778698ea13e28a7fdcbc071d7`
- Round209 probe:
  `dcd8d6d2354151a0aa1c45db8f1ce78f1385b665741ee5a79521bf261cebc13f`
- Round186 interval factor evaluator:
  `5797b8f4c2ba9c8c5b42b32511f3c97a15469b59bdf00cd8430580c3429c7c64`

Round214 was additionally cold-run independently at
`PYTHONHASHSEED=214053`: the canonical stdout was `156,006` bytes with SHA256
`9a90e2f01cf03b263803298ba1977c9ecfa6e70778698ea13e28a7fdcbc071d7`,
matching seeds `214051` and `214052`; elapsed time was `54.88s`, maximum RSS
`946,276 KiB`.

Neither the Round217 verifier nor its expected-result builder imports or
executes the Round217 producer or Round214 probe.

## Independently reconstructed contact census

The producer and fresh verifier reconstruct:

- Round208 leaves: `18,324`;
- Round208 strict 3D signature regions: `36,040`;
- Round211/Round209 nonempty sheets: `17,716`;
- Round211/Round209 curve incidences: `20,456`;
- Round211/Round209 endpoint incidences: `40,912`;
- positive-area compatible contacts: `15,540`;
- exact `p/s` contacts: `7,932`
  (`5,840` exact `p` plus `2,092` exact `s`);
- partial positive-area contacts: `644`; and
- exact `t` contacts: `6,964`.

The rebuilt Round214 midpoint taxonomy is:

| contact class | count |
|---|---:|
| exact `t`, safe same-occurrence explicit curve duplicate | 4,260 |
| exact `t`, cross-occurrence exact curve carrier | 2,704 |
| exact `p`, strict midpoint witness | 3,164 |
| exact `p`, exact endpoint carrier candidate | 2,676 |
| exact `s`, strict midpoint witness | 1,184 |
| exact `s`, exact endpoint carrier candidate | 908 |
| partial, strict midpoint witness | 300 |
| partial, exact endpoint carrier candidate | 80 |
| partial, unresolved | 264 |

This exactly recovers the Round214 `4,648` strict zero witnesses and its
`3,664` endpoint-carrier candidates, while keeping those feasibility labels
separate from Round217's stricter whole-face acceptance rule.

## Formal ledgers

| ledger | rows | rows SHA256 | row-ID SHA256 |
|---|---:|---|---|
| unique full-face zero traces | 448 | `50ff0a9ffa271c4ea1dbb985c2af36d0abb37575b494bd12637af0f31a871fb3` | `cc159687acbc4dce63a6d8b4f57e8ade71e5e01c95f9d83476bc17d56c92291a` |
| two-sided incidences | 896 | `b393e359f347a6d99f7c49ee4e2bc7083fef5432e8285336c46aea76394e6316` | `4c1d008ede637ef0866f883ff255bbd9495cea8c0d33c467c78739aee3aad6cb` |
| exact common-refinement glues | 448 | `b66e6a0c17ba8628ab627f00cc15705ffe2d545008cf97a796ced01032f52020` | `0a8412a680b1fd0b02cc46d4c63bc6ab5e9b8b5dc587ef77333aa64540013a28` |

All 448 trace carrier keys are unique: carrier-contact multiplicity is
`1:448`.  All 416 cross-origin rows use exact common parent-atlas faces and
identical restricted evaluator identities.  No cross-origin join is inferred
from box touch or signature hashes alone.

## Key-ordinal census

The 448 accepted contacts cover 20 official key ordinals.  Their
per-ordinal map SHA256 is
`90884d2b425ac977a60f056ed63a8dbd521b3cf72689c36a61d2f46c164cf1a6`;
the count histogram is:

- 4 ordinals with 1 contact;
- 4 ordinals with 3 contacts;
- 4 ordinals with 12 contacts;
- 4 ordinals with 19 contacts; and
- 4 ordinals with 77 contacts.

This is only a local exact-key ordinal census.  It does not claim any global
key fibre is exhausted.

## Exact-face frontier

`7,484 / 7,932` exact `p/s` contacts do not satisfy the complete transverse
endpoint-edge proof:

| first failed predicate | count |
|---|---:|
| lower `t` boundary restriction overwraps | 3,530 |
| upper `t` boundary restriction overwraps | 3,530 |
| both `t` boundary restrictions overwrap | 424 |

Their closed frontier rows have:

- rows SHA256:
  `b214c5ff7c444ae89c67fa0d0abc26c4021ab2a72c66e699b7aed02650f7601c`
- row-ID SHA256:
  `3775b9e72338cdf0350639760669b004a830f2e42c9df771e1d68ea46f32e07f`

The full-face `d/dt` predicate is strict on these rows; the first missing data
are exact root-coordinate boundary restrictions.  Round211 endpoint rows name
boundary edges but do not carry exact root coordinates, so they cannot support
endpoint-to-curve-interior common refinements.  Round217 does not invent those
coordinates.

## Partial-face frontier

The `264` unresolved partial contacts split exactly as:

- `p`: 144;
- `t`: 120.

Their closed frontier rows have:

- rows SHA256:
  `c2b93893ec14c3f3892158cd7421edaf64cd4e83450f0bfeba7ba8692d16f09d`
- row-ID SHA256:
  `10ff7f8d96fdda3108c5e0850e3ab42adf3cd5dae6e3a4819a50b5c746682b9c`

These rows lack both a strict midpoint zero witness and an exact endpoint
carrier.  Partial-face curve restrictions and endpoint-to-interior glue remain
the next formal frontier.

## Independent verification and attacks

The verifier rebuilds the full expected Python object and demands canonical
byte equality before running:

- `25/25` re-signed semantic attacks;
- `15/15` strict JSON attacks; and
- `16/16` filesystem/path attacks.

The semantic suite includes carrier geometry/orientation/sign changes,
accepted per-key mapping and histogram tampering, stealing an overwrap
frontier into the accepted ledger, whole-origin/tube/global-disposition
credit theft, D02/CM2 promotion, provenance forgery, and duplicate/drop
trace/glue rows.  Every attacked object has affected row, ledger, result, and
envelope hashes recomputed before rejection.

The strict JSON suite rejects duplicate keys, NaN, positive/negative infinity,
BOM, NUL, invalid UTF-8, a lone surrogate, trailing bytes, missing final
newline, top-level array/scalar, empty input, and an explicit size violation.

The path suite rejects symlink/hardlink/FIFO/directory inputs, empty and
oversized files, wrong names and parent escapes, missing paths, and
symlink/hardlink/FIFO/directory/nested/unallowlisted verification outputs.

AST scans find zero duplicate literal dictionary keys in both producer and
verifier.

## Freeze note

An earlier pre-freeze certificate SHA
`1f9e9ae63d27335557b4e107906fa38a663969f17edf855d8a2d423dfca1acb2`
with result SHA
`745e1ca633fbd84f0989d17ac4cbe3b72a6b887a01d2bdf9054b42541c7abcc6`
was generated from producer SHA
`29dc995327237e58c78e6bce85edb9593c106f4170f65d7409948ba66ef7aa91`.
It was superseded when the requested complete per-key maps were added.  The
brief observation of the new source beside the old certificate occurred
between the source edit and the subsequent official regeneration; it was not
same-source nondeterminism.  The superseded object is not retained and is not
eligible for the manifest.

The frozen producer is
`687fd48134e204a99c807e1fd18954cef7633879396db5f4d291ece1568dfa66`,
and all three isolated official/replay outputs under that source are
byte-identical.

## Credit boundary and next gate

- formal local trace credit: 448;
- formal local incidence credit: 896;
- formal local common-refinement glue credit: 448;
- component-deduplication credit: 0;
- whole-leaf credit: 0;
- whole-origin credit: 0;
- whole-original-tube credit: 0;
- global-component credit: 0;
- global-fibre credit: 0;
- global exact-key disposition credit: 0;
- source-G dispositions: `0 / 224,580`;
- D02: unchanged `BLOCKED`;
- Gate5: unchanged `10/18`;
- CM2: unchanged `NO-GO`.

The next gate is exact root-coordinate endpoint-to-interior and partial-face
common-refinement materialization, followed by a complete independently
verified physical-component equivalence closure.
