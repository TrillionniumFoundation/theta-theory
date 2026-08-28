# CM2 Round216 — independently verified source-G global key-occurrence exhaustion frontier

Date: 2026-07-27

Verdict:
`PASS_PARTIAL_FORMAL_ROUND216`

## Scope and frozen identities

Round216 reconstructs every source-G exact-key ordinal observed among the
Round179 resolved 3D children, joins the accepted Round204, Round208,
Round211, and Round213 local ledgers keywise, and identifies the exact
frontier still preventing global fibre exhaustion.

This is an occurrence and missing-evidence frontier. It is not a physical
component quotient and does not exhaust or dispose any global exact-key
fibre.

| Artifact | SHA-256 |
|---|---|
| producer | `9da9d11ec0aa16e8dcbd22c0add51f373194008afa507da0432d3fee417c68fa` |
| certificate | `fa4cfb3b209518308c61ccdfa95834dd8e6899e6232fc40a569cbab4d6ecbe34` |
| verifier | `9cafb5fdeb4fc6cd150b7d56b3298f0d808c2abfe81f173d1ccd3bed2c0d07a0` |
| verification | `6ad6f2a7ee32f0a1abc2a004e3fcb4ca0de05d4e916c211220aed5cd39f872a2` |
| report | recorded by the adjacent manifest |
| cold replay | recorded by the adjacent manifest |

The certificate is `174,708` bytes and has result SHA-256
`267a4b9aaaab6a576e1c1866cc2fa0b9dc9bf4fc6a3b08a210ed3821e45dd658`.
The verification is `5,373` bytes and has result SHA-256
`23055888339f4e42ba968706d895ff6123a6b7549cbe176de835b2e68d0c3a6d`.

## Input boundary

Both producer and verifier replay the Round179, Round182, Round204,
Round208, Round211, and Round213 manifests and all `38` entries. Round214 is
pinned only as read-only, nonpromotional obstruction evidence:

- probe SHA-256:
  `d074aa045637ce1bb31768fa551bdb73ceda6a58c760cafe3dbf92faa7c922fe`;
- report SHA-256:
  `aa48c012fa8c57df89b2bea4123467fc2c74821a03525095976cb61c709fe952`.

The immutable Round213 report erratum is independently pinned:

- erratum SHA-256:
  `a18c1641e739e01fa178fa0aafbc2956e58e27e0bf4ca087154bc47cf183a721`;
- erratum manifest SHA-256:
  `0a2d39ad8c80f5c39cd5e6b3d3917e40df6e12eaa5fcaa075fce089708b8ccc8`.

Accordingly, the `96` Round204 tail regions are treated as a tagged subset
of the `736` strict-open regions. They are reported separately but are
non-additive. The frozen Round213 six-artifact manifest remains unchanged.

Concurrent Round217 is deliberately outside this pinned boundary. The
pre-Round217 evidence has zero explicit `p/s` zero-trace incidence IDs, but
Round216 makes no assertion about trace or incidence rows created after this
boundary.

## Independent verifier boundary

The verifier parses the producer only as inert pinned bytes and never imports
or executes it. It independently reconstructs the complete expected result
from the six formal packages and immutable erratum before candidate bytes are
opened. It then requires full Python-object equality, canonical-byte
equality, exact certificate file SHA-256, and exact result SHA-256.

Both sources have zero duplicate literal dictionary keys. Normalized AST
body comparison finds one exact generic overlap, producer
`canonical_bytes` against verifier `encoded`. The package therefore claims
an independent expected reconstruction with shared generic
canonicalization risk disclosed, not a fully implementation-diverse second
derivation.

## Exact 116-key classification

Round179 contains `17,192` resolved positive-3D occurrence rows across
exactly `116` official key ordinals. Its fully-replaced clusters contain
`96` keys. The Round213 residual union contains `36` keys, and the
fully-replaced/residual intersection contains `32`.

The disjoint complete partition is:

| Classification | Keys | Key-set SHA-256 |
|---|---:|---|
| BOTH_FULLY_REPLACED_AND_RESIDUAL | 32 | `45d580bedb669875f90101d98013ba44da40e56aa6688f052dbccc1f8499efe4` |
| RESIDUAL_ONLY | 4 | `0e36044c42c8c6dfd072bda521f4d6a4f146b35c1d68cb88f7915dd43b588eb9` |
| FULLY_REPLACED_ONLY | 64 | `95868ce1cf24d57530143a73fdf95db8da3e39cad70197b09664cb9afacefa68` |
| RESOLVED_CHILD_ONLY | 16 | `5d1cf0b2165bbf8611cba5c3810a5dc1cfcbc5d5fb5faa7be23be312bd691a8b` |

The complete key-set SHA-256 is
`405ffd84f2a5a432d5dbbf2e0a1f1f3c4f8ed477f0408fd07e4d4c369ec27fdb`.
The `36` residual keys are exactly the disjoint union of Round204's `12`
ordinals and Round208/Round211's `24` ordinals.

## Local 3D occurrence census

The `116` closed per-key rows have rows SHA-256
`452946676c7f18af81f0a3cc676517cdc74ffe09284b95338a899d71fd1f8d94`.

The strictly local, noncomponent census is:

| Classification | R179 | R204 | R208 | Total | Per-key min | Per-key max |
|---|---:|---:|---:|---:|---:|---:|
| BOTH | 13,612 | 736 | 35,900 | 50,248 | 194 | 6,206 |
| RESIDUAL_ONLY | 60 | 0 | 140 | 200 | 50 | 50 |
| FULLY_REPLACED_ONLY | 3,432 | 0 | 0 | 3,432 | 24 | 102 |
| RESOLVED_CHILD_ONLY | 88 | 0 | 0 | 88 | 3 | 8 |
| **Total** | **17,192** | **736** | **36,040** | **53,968** | — | — |

The `53,968` number is a local 3D occurrence count. It is not a coordinate
volume, physical component count, or exhausted global-fibre count. The `96`
Round204 tail tags are already inside its `736` rows and are never added a
second time.

## Lower-dimensional coverage

All `36` residual keys have accepted local lower-dimensional materialization:

- the Round204 `12` keys retain their separate formal gauge:
  source/target 2D `224/224`, 1D `1,024`, 0D `580`, tail glues `32`;
- the Round208/Round211 `24` keys are joined keywise through owner-region ID
  to the Round208 signature key:
  2D owner incidences `17,716`, 1D owner incidences `20,456`, and 0D owner
  incidences `40,912`.

Thus all `32` BOTH keys and all `4` RESIDUAL_ONLY keys have a local atlas.
The `64` FULLY_REPLACED_ONLY plus `16` RESOLVED_CHILD_ONLY keys, `80` total,
have no Round204/Round211 atlas.

Even the covered `36` keys remain globally unexhausted because local
incidences have not been joined into cross-occurrence physical components.

## Two independent blockers

Round216 keeps the two leading blockers separate and requires both to close.

1. **Round179 resolved-child boundary atlas**

   All `17,192` resolved children lack an explicit canonical
   lower-dimensional boundary atlas in the pinned input. The explicit atlas
   row count is `0`; the number of boundary cells is intentionally marked
   not enumerable until those rows are materialized.

2. **Internal-face trace and physical glue**

   The pinned Round214 evidence has:

   - positive-area `p/s` contacts: `8,256`
     (`5,840` exact p, `324` partial p, `2,092` exact s);
   - cross-occurrence positive-area contacts: `9,200`
     (`2,704` exact t, `320` partial t, `5,840` exact p,
     `324` partial p, `12` exact s);
   - cross-occurrence exact curve-carrier candidates: `2,704`;
   - cross-occurrence exact endpoint-carrier candidates: `6,684`;
   - explicit cross-occurrence common-refinement glue rows: `0`;
   - unresolved partial contacts: `264`
     (`144` p and `120` t).

   The `4,260` safe same-occurrence exact-t duplicate joins and `4,648`
   strict Arb zero witnesses do not substitute for explicit `p/s` trace IDs
   or cross-occurrence common-refinement glue.

## Hostile verification and cold reproducibility

The verifier rejected:

- `29/29` re-signed semantic attacks, including ordinal/class changes,
  per-key occurrence omission and duplication with row/ledger/result
  rehashing, `36↔80` atlas theft, fabricated Round179 boundary and glue
  rows, tail double-counting, treating concurrent Round217 as pinned,
  erratum tamper/omission, and component/whole/global/disposition/D02/CM2
  promotion;
- `15/15` strict JSON, encoding, canonicalization, and oversize attacks;
- `20/20` path, type, alias, output, and temporary-file attacks or safe
  bypasses.

Producer seeds `216051` and `216052` emitted byte-identical certificates.
Verifier seeds `216061` and `216062` emitted byte-identical verifications.
The hidden replay files were deleted after equality, hash, size, and result
checks. Exact commands and resource measurements are in the adjacent cold
replay note.

## Strict limitation and next gate

- global exact-key fibres exhausted: `0/116`;
- physical-component credit: `0`;
- whole-origin credit: `0`;
- whole-original-tube credit: `0`;
- source-G global exact-key dispositions: `0/224580`;
- D02: `BLOCKED`;
- Gate5: `10/18`;
- complete global 18-field blocks: `0`;
- CM2: `NO-GO_FOR_CLAIM`.

The next source-G core gate is Round220: independently materialize the
canonical half-open 2D faces, 1D edges, and 0D corners of all `17,192`
Round179 resolved children, with exact shared-face/common-refinement IDs and
a strict separation between coordinate boundary cells and physical event
sheets.
