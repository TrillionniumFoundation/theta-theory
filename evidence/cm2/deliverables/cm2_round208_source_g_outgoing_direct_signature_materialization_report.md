# CM2 Round208 — independently verified source-G outgoing-W direct-signature materialization

Date: 2026-07-27

Verdict:
`PASS_PARTIAL_FORMAL_ROUND208`

## Scope and frozen identities

Round208 formally materializes the direct target, strict wall word, roof,
outgoing cell, target chart, and immutable local Gate5 key join for every
strict open 3D region in the frozen source-G outgoing-W scope.

This is a local open-3D result. It does not materialize lower-dimensional
half-open owners, promote an original tube, or dispose a complete global
exact-key fibre.

The six frozen artifacts are:

| Artifact | SHA-256 |
|---|---|
| producer | `c9fe0cdfb4631c31702473d705b04fa89fb8d51e4c71c9b2b652dc98e4641913` |
| certificate | `4d01fb9cee639ec59786c078f7a20b3bbcd5c18ea674fabbfce64e250e765938` |
| verifier | `718c731004fe2125511a9a52c84f45c77eab842d4c042942e91cc5881b64ee36` |
| verification | `29faabf06adab4e4a7a1cfc99d1dc2c14aa9d7bfc7e32773fad41056bb2c8f31` |
| report | recorded by the adjacent manifest |
| cold replay | recorded by the adjacent manifest |

The certificate is `193,161,618` bytes and has result SHA-256
`d00674fa4061364539ce6f36f6f8de938f50bc54afbf5497266dcfa0e078bca8`.
The verification is `6,259` bytes and has result SHA-256
`2f902656d553bea37640120a1c73ae8085f23f6a0c5fe091ecd6c45ed545117b`.
The certificate records python-flint `0.9.0` and the effective Arb precision
left by the pinned evaluator chain, `192` bits.

## Independent verifier boundary

The verifier first treats the producer as pinned inert regular bytes. It
does not import or execute the producer, Round207, or Round203. Before any
candidate certificate byte is opened, it:

1. replays the Round182 manifest and all seven exact entries;
2. loads only the individually pinned pre-Round208 evaluator stack;
3. reconstructs the outgoing-W scope from the verified Round182 attachment;
4. recomputes every face, leaf, direct signature base, strict 3D region,
   U|U side, origin completion row, and local exact-key join; and
5. closes and cross-audits the complete expected result.

Only then does it load the candidate and require full Python-object equality,
full canonical-byte equality, the exact certificate file hash, and the exact
certificate result hash.

The pre-Round208 stack includes pinned Round186/188/189/191/195/198
evaluators. It does not make the verifier fully implementation-diverse.
Normalized AST body comparison finds `8` exact lower-level overlaps:
`require`, `canonical_bytes`, `digest`, `closed_row`, `qstr`,
`regular_bytes`, `build_origin_rows`, and `build_key_rows`. The complete
`build_result` and `main` bodies do not overlap. Both source files have zero
duplicate literal dictionary keys. This package therefore claims an
independent expected reconstruction with disclosed shared lower-level
algorithm risk, not a fully implementation-diverse second derivation.

## Verified census and exact conservation

| Ledger | Closed rows |
|---|---:|
| final factor-face incidences | 18,412 |
| leaf geometry | 18,324 |
| direct leaf signature bases | 18,324 |
| strict open 3D local signatures | 36,040 |
| U\|U leaf audit | 88 |
| origin-local completion | 8,268 |
| immutable exact-key local joins | 24 |
| **total** | **99,480** |

The scope has `8,268` origins, `912` parents, `11,960` retained children,
and `18,324` outgoing residual leaves. The exact outer coordinate volume is
`861459/419430400000` before and after materialization. The leaf-count delta
and exact coordinate-volume delta are both zero.

The final leaf classes are:

- `CLIPPED_2D_BOUNDARY_1D`: `17,308`;
- `EMPTY`: `608`;
- `FULL_2D`: `408`.

The strict region census is:

- E: `9,008`;
- N: `9,012`;
- S: `9,012`;
- W: `9,008`.

There are `52` distinct local signatures. Wall-word lengths are `30,080`
at length zero and `5,960` at length one. Every region joins exactly one of
`24` immutable official Gate5 keys. The U|U cohort contains `88` leaves,
`76` origins, and `176` separately materialized side-specific regions; no
signature is copied across the seam.

## Closed-row, nonpromotion, and attack audits

Every one of the `99,480` rows was independently rehashed after removing its
`row_sha256`, and every row-list digest and cross-ledger incidence was
recomputed. The complete expected object equals the candidate object and its
canonical bytes.

A recursive strict-value audit finds:

- `99,484` global-exact-key-disposition credit fields, all integer zero;
- `62,636` whole-original-tube credit fields, all integer zero;
- `36,041` lower-dimensional half-open-owner credit fields, all integer zero;
- `8,269` lower-dimensional ownership-materialized fields, all false;
- `24` global exact-key-fibre exhaustion fields, all false.

The verifier rejected:

- `18/18` semantically changed certificates after recomputing the affected
  closed-row digest, ledger digest, and complete result digest;
- `15/15` strict JSON, encoding, canonicalization, and oversize attacks;
- `23/23` path, file-type, parent-alias, output-alias, and temporary-file
  attacks or safely bypassed prepositioning attempts.

The output writer accepts only the official verification name or a hidden
Round208 verification replay name in the exact deliverables directory. It
requires single-link regular existing outputs and uses an unpredictable
same-directory temporary, file `fsync`, atomic replace, and parent-directory
`fsync`.

## Cold reproducibility

A fresh producer seed `208073` exited zero and reproduced the frozen
`193,161,618`-byte certificate byte-for-byte. Its result SHA-256 was
`d00674fa4061364539ce6f36f6f8de938f50bc54afbf5497266dcfa0e078bca8`.

The frozen verifier was then executed from scratch with seeds `208081` and
`208082`. Both rebuilt the complete expected result before loading the
candidate, passed all attacks, emitted result SHA-256
`2f902656d553bea37640120a1c73ae8085f23f6a0c5fe091ecd6c45ed545117b`,
and produced byte-identical `6,259`-byte verification files with file
SHA-256
`29faabf06adab4e4a7a1cfc99d1dc2c14aa9d7bfc7e32773fad41056bb2c8f31`.

The compared hidden producer and verifier replay files were deleted after
their equality and hashes were recorded. Exact commands and resource data
are in the adjacent cold-replay note.

## Strict limitation and next core gate

Round208 supplies `36,040` local open-3D signature credits and `8,268`
origin-local coverage credits. It supplies no lower-dimensional,
whole-original-tube, or global-disposition credit:

- lower-dimensional half-open ownership: `NOT_MATERIALIZED`;
- source-G global exact-key dispositions: `0/224580`;
- whole-original-tube credit: `0`;
- D02: `BLOCKED`;
- Gate5: `10/18`;
- complete global 18-field blocks: `0`;
- CM2: `NO-GO_FOR_CLAIM`.

The next source-G core gate is formalization and independent verification of
the Round209 factor-derived half-open owner construction: `17,716` 2D
sheets, `20,456` 1D clipping incidences, and `40,912` 0D endpoint
incidences. It must then be joined with this Round208 open-3D ledger and the
separately formalized Round204 wall-G local replacement. No complete
whole-tube or global exact-key disposition may be claimed until those
lower-dimensional lineages and every remaining global exact-key fibre are
closed.
