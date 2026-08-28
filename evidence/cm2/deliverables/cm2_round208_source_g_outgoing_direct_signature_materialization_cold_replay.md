# Round208 source-G outgoing direct-signature formal package cold replay

Date: 2026-07-27

## Frozen identities

- Producer:
  `cm2_round208_source_g_outgoing_direct_signature_materialization.py`
- Producer SHA-256:
  `c9fe0cdfb4631c31702473d705b04fa89fb8d51e4c71c9b2b652dc98e4641913`
- Certificate:
  `cm2_round208_source_g_outgoing_direct_signature_materialization_certificate.json`
- Certificate byte count: `193,161,618`
- Certificate SHA-256:
  `4d01fb9cee639ec59786c078f7a20b3bbcd5c18ea674fabbfce64e250e765938`
- Certificate result SHA-256:
  `d00674fa4061364539ce6f36f6f8de938f50bc54afbf5497266dcfa0e078bca8`
- Verifier:
  `cm2_round208_source_g_outgoing_direct_signature_materialization_verifier.py`
- Verifier SHA-256:
  `718c731004fe2125511a9a52c84f45c77eab842d4c042942e91cc5881b64ee36`
- Verification:
  `cm2_round208_source_g_outgoing_direct_signature_materialization_verification.json`
- Verification byte count: `6,259`
- Verification SHA-256:
  `29faabf06adab4e4a7a1cfc99d1dc2c14aa9d7bfc7e32773fad41056bb2c8f31`
- Verification result SHA-256:
  `2f902656d553bea37640120a1c73ae8085f23f6a0c5fe091ecd6c45ed545117b`

## Producer replay

The frozen producer closure recorded official seed `208052` and independent
seed `208062`. This independent verification closure also executed a fresh
seed `208073`:

```text
env PYTHONDONTWRITEBYTECODE=1 PYTHONHASHSEED=208073 \
  /usr/bin/time -v .venv-neurips/bin/python -B \
  deliverables/cm2_round208_source_g_outgoing_direct_signature_materialization.py \
  --output deliverables/.cm2_round208_seed208073_certificate.json
```

| Run | Seed | User | System | Wall | Peak RSS | Exit |
|---|---:|---:|---:|---:|---:|---:|
| recorded official producer | 208052 | 540.21 s | 2.61 s | 9:03.22 | 1,079,920 KiB | 0 |
| recorded independent producer | 208062 | 503.62 s | 2.52 s | 8:26.55 | 1,082,092 KiB | 0 |
| fresh closure re-audit | 208073 | 580.22 s | 2.82 s | 9:43.50 | 1,079,492 KiB | 0 |

The fresh output and frozen official certificate were both exactly
`193,161,618` bytes. `cmp` returned zero. Both file SHA-256 values were
`4d01fb9cee639ec59786c078f7a20b3bbcd5c18ea674fabbfce64e250e765938`,
and the printed result digest was
`d00674fa4061364539ce6f36f6f8de938f50bc54afbf5497266dcfa0e078bca8`.

## Independent verifier replays

The official verification run was:

```text
env PYTHONDONTWRITEBYTECODE=1 PYTHONHASHSEED=208081 \
  /usr/bin/time -v .venv-neurips/bin/python -B \
  deliverables/cm2_round208_source_g_outgoing_direct_signature_materialization_verifier.py
```

The independent replay was:

```text
env PYTHONDONTWRITEBYTECODE=1 PYTHONHASHSEED=208082 \
  /usr/bin/time -v .venv-neurips/bin/python -B \
  deliverables/cm2_round208_source_g_outgoing_direct_signature_materialization_verifier.py \
  --output deliverables/.cm2_round208_seed208082_verification.json
```

| Run | Seed | User | System | Wall | Peak RSS | Exit |
|---|---:|---:|---:|---:|---:|---:|
| official verifier | 208081 | 1,037.16 s | 22.99 s | 17:40.37 | 1,502,140 KiB | 0 |
| independent verifier | 208082 | 1,028.18 s | 22.95 s | 17:31.33 | 1,503,972 KiB | 0 |

Both runs printed only
`2f902656d553bea37640120a1c73ae8085f23f6a0c5fe091ecd6c45ed545117b`
to stdout. Both verification files were exactly `6,259` bytes; `cmp`
returned zero, and both file SHA-256 values were
`29faabf06adab4e4a7a1cfc99d1dc2c14aa9d7bfc7e32773fad41056bb2c8f31`.

The official and independent verifier runs each:

- rebuilt the complete expected result before loading the candidate;
- reconstructed all `99,480` closed rows;
- required complete expected Python-object and canonical-byte equality;
- rejected `18/18` re-signed semantic mutations;
- rejected `15/15` strict JSON/encoding/oversize attacks;
- rejected or safely bypassed `23/23` path/type/alias/temp attacks;
- replayed the Round182 manifest and all seven entries;
- never imported or executed the producer, Round207, or Round203; and
- retained zero lower-dimensional, whole-tube, and global-disposition credit.

## Fail-closed development correction

An earlier, unfrozen verifier draft completed the independent geometry rebuild
but rejected before candidate loading because its provenance audit asserted
the entry precision `256` rather than the effective `192` bits left by the
pinned evaluator stack. It emitted no verification artifact. The frozen
verifier corrects that observed runtime constant, canonicalizes rebuilt JSON
key types, and is the exact `718c7310...ee36` source executed in both accepted
runs.

## Cleanup and disposition

After successful `cmp`, SHA, size, and result-digest checks, the hidden
producer and verifier replay files were deleted. No attack scratch file,
symlink, FIFO, hardlink, parent alias, or prepositioned temporary remains.

The formal scope remains local:

- lower-dimensional half-open ownership: `NOT_MATERIALIZED`;
- whole-original-tube credit: `0`;
- source-G global exact-key dispositions: `0/224580`;
- D02: `BLOCKED`;
- Gate5: `10/18`;
- CM2: `NO-GO_FOR_CLAIM`.
