# CM2 Round213 — independently verified source-G Round182 residual dimensional union

Date: 2026-07-27

Verdict:
`PASS_PARTIAL_FORMAL_ROUND213`

## Scope and frozen identities

Round213 proves that the independently formalized Round204 wall-return scope
and Round208 outgoing-direct scope are an exact disjoint partition of all
Round182 residual origins:

- Round204: `64` origins and `16` parents;
- Round208: `8,268` origins and `912` parents;
- exact union: `8,332` origins and `928` parents;
- origin and parent intersections: both `0`.

The six frozen artifacts are:

| Artifact | SHA-256 |
|---|---|
| producer | `b90ea2c23d9296f2fe6f40d20d2b9655f98501014719e2b1d6ccbd647fde9b31` |
| certificate | `5ba025aa9e28d34fa913d51025ee90833632e9bca3d1f4ed4d0fa2a67efcbe05` |
| verifier | `ac3639a8237eae205da8c602a4f11890723445912453993b4c0f35d372956fb7` |
| verification | `2fa0501932bee9744c4e702398c2e436c86c2cae0289c93bcdffe7250e9ecc3d` |
| report | recorded by the adjacent manifest |
| cold replay | recorded by the adjacent manifest |

The certificate is `10,584,916` bytes and has result SHA-256
`1b2e74eedc449e2d27b8e6c92fa8d6d4e3eae1021a0b581f8f799845e3d9d13a`.
The verification is `5,576` bytes and has result SHA-256
`5e21201a1c8741fa0d33bd83d3e284ff927fcf6589e7666fcf865d74093eb5a1`.

## Independent verifier boundary

The verifier treats the frozen producer only as inert bytes and never imports
or executes it. Before opening the candidate certificate, it replays the
Round182, Round204, Round208, and Round211 manifests and all `25` entries,
then independently rebuilds the complete expected union from the accepted
certificates and the Round182 attachment.

Only after the expected result is closed does it load the candidate and
require exact Python-object equality, canonical-byte equality, certificate
file SHA-256, and certificate result SHA-256.

Both sources have zero duplicate literal dictionary keys. Normalized AST
comparison finds one exact generic-body overlap, producer `canonical_bytes`
against verifier `encoded`. No implementation-diverse second derivation is
claimed; the shared generic canonicalization risk is disclosed.

## Exact partition proof

The exact origin-set identities are:

- Round204 origin-set SHA-256:
  `5ead6a0c6f0d84f257ca43d4c3388feb1736201789e0c8d0b92ccfde829ae71e`;
- Round208 origin-set SHA-256:
  `10dd4db3aad3063bf848908eb19de2e7363b7e280d24420ec50723688eed3947`;
- disjoint union SHA-256:
  `5799c69f51d4dbdfd890fffc4b4fa260bc76f022ee37dc0c3bf036e477fc8156`;
- parent union SHA-256:
  `96aa885986f7ece9487d2ccd9b3ab291e663d11f93f2c08fa7f45ff1e243ba3d`.

The `8,332`-row closed union ledger has rows SHA-256
`f7675058cfc7764307a99dac1a8c35b989e482bc5254b5e87d621549cc93b5a7`.
It equals exactly the Round182 registry rows whose
`fully_geometrically_replaced_original_tube` field is false, joined through
the attachment's `Round179_origin_row_id`.

Round211 supplies nonempty-sheet coverage for `8,264` Round208 origins.
Exactly four Round208 origins are EMPTY-only, each with nine EMPTY leaves and
nine strict open 3D signature regions; no 2D sheet is invented for them. The
four-ID set SHA-256 is
`d19114798c695281bd7f9e8edeeffec77a703ac9a893aace4419bb6a60b0a4a3`.

## Separate dimensional gauges

The following counts are conserved in their own formal gauges:

| Scope | Formal local census |
|---|---|
| Round204 | strict open 3D `736`; tail open 3D `96`; source/target 2D `224/224`; 1D `1,024`; 0D `580`; tail glues `32` |
| Round208 | strict open 3D `36,040` |
| Round211 | 2D owner incidences `17,716`; 1D owner incidences `20,456`; 0D owner incidences `40,912` |

The disjoint strict-open 3D union is `36,776`, with region-ID union SHA-256
`f6913be76b7fe9ab6bf8d16eab9228303101b9cd07de672dd025f6de69598b78`.
The `96` Round204 tail regions are not strict-open regions. Coordinate
volumes from Round204 and Round208 use different gauges and are never summed.

Round204's `12` and Round208/Round211's `24` local exact-key ordinals are
disjoint. Their `36`-ordinal union SHA-256 is
`5ba4d5186ddb7ddb1868957f83af9d5224dbddaa619ecfedf1cdc51f7bc03763`;
the closed ordinal-row ledger SHA-256 is
`b0d8869a765489fd5acc79c6571c942901ed08a5ffa5c12505b52952eb6ea92b`.

## Attack and reproducibility audits

The verifier rejected:

- `22/22` semantically changed and re-signed candidates, including invented
  parent/tube/global/physical credit, transfer of all `8,332` local credits
  into whole-origin or whole-tube credit, an invented sheet for an EMPTY-only
  origin, actual union-row omission and duplication with ledger rehashing,
  ordinal tampering and overlap, and addition of the `96` tail regions to the
  strict-open total;
- `15/15` strict JSON, canonicalization, encoding, and oversize attacks;
- `21/21` path, type, alias, output, and temporary-file attacks or safe
  bypasses.

Producer seeds `213051` and `213052` emitted byte-identical certificates.
Verifier seeds `213061` and `213062` emitted byte-identical verifications.
The compared hidden files were deleted after their hashes and equality were
recorded. Exact commands and resource measurements are in the adjacent cold
replay note.

## Strict limitation and next gate

Round213 certifies only local dimensional materialization/completion of
`8,332` residual origins. It does not deduplicate physical components,
promote any whole origin or original tube, or exhaust any global exact-key
fibre:

- physical-component credit: `0`;
- whole-origin credit: `0`;
- whole-original-tube credit: `0`;
- global exact-key disposition credit: `0`;
- source-G global exact-key dispositions: `0/224580`;
- D02: `BLOCKED`;
- Gate5: `10/18`;
- complete global 18-field blocks: `0`;
- CM2: `NO-GO_FOR_CLAIM`.

The next core gate is a global key-occurrence exhaustion frontier across all
`116` Round179 official key ordinals. It must keep the Round179 resolved-child
3D occurrence census separate from these local dimensional gauges, enumerate
the missing Round179 lower-dimensional boundaries and cross-occurrence
physical glue, and leave every global fibre unexhausted until those rows are
formally materialized.
