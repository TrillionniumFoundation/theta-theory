# Round213 source-G Round182 residual dimensional union cold replay

Date: 2026-07-27

## Frozen identities

- Producer:
  `cm2_round213_source_g_round182_residual_dimensional_union.py`
- Producer SHA-256:
  `b90ea2c23d9296f2fe6f40d20d2b9655f98501014719e2b1d6ccbd647fde9b31`
- Certificate:
  `cm2_round213_source_g_round182_residual_dimensional_union_certificate.json`
- Certificate byte count: `10,584,916`
- Certificate SHA-256:
  `5ba025aa9e28d34fa913d51025ee90833632e9bca3d1f4ed4d0fa2a67efcbe05`
- Certificate result SHA-256:
  `1b2e74eedc449e2d27b8e6c92fa8d6d4e3eae1021a0b581f8f799845e3d9d13a`
- Verifier:
  `cm2_round213_source_g_round182_residual_dimensional_union_verifier.py`
- Verifier SHA-256:
  `ac3639a8237eae205da8c602a4f11890723445912453993b4c0f35d372956fb7`
- Verification:
  `cm2_round213_source_g_round182_residual_dimensional_union_verification.json`
- Verification byte count: `5,576`
- Verification SHA-256:
  `2fa0501932bee9744c4e702398c2e436c86c2cae0289c93bcdffe7250e9ecc3d`
- Verification result SHA-256:
  `5e21201a1c8741fa0d33bd83d3e284ff927fcf6589e7666fcf865d74093eb5a1`

## Producer replay

Official producer:

```text
env PYTHONDONTWRITEBYTECODE=1 PYTHONHASHSEED=213051 \
  /usr/bin/time -v .venv-neurips/bin/python -B \
  deliverables/cm2_round213_source_g_round182_residual_dimensional_union.py
```

Independent replay:

```text
env PYTHONDONTWRITEBYTECODE=1 PYTHONHASHSEED=213052 \
  /usr/bin/time -v .venv-neurips/bin/python -B \
  deliverables/cm2_round213_source_g_round182_residual_dimensional_union.py \
  --output deliverables/.cm2_round213_seed213052_certificate.json
```

| Run | Seed | User | System | Wall | Peak RSS | Exit |
|---|---:|---:|---:|---:|---:|---:|
| official producer | 213051 | 161.29 s | 6.26 s | 6:19.72 | 1,496,144 KiB | 0 |
| independent producer | 213052 | 116.45 s | 5.30 s | 2:01.84 | 1,500,900 KiB | 0 |

The official run overlapped host load; CPU time and output are deterministic.
Both files were `10,584,916` bytes, `cmp` returned zero, and both SHA-256
values were
`5ba025aa9e28d34fa913d51025ee90833632e9bca3d1f4ed4d0fa2a67efcbe05`.
Both runs printed result SHA-256
`1b2e74eedc449e2d27b8e6c92fa8d6d4e3eae1021a0b581f8f799845e3d9d13a`.

## Independent verifier replays

Official verifier:

```text
env PYTHONDONTWRITEBYTECODE=1 PYTHONHASHSEED=213061 \
  /usr/bin/time -v .venv-neurips/bin/python -B \
  deliverables/cm2_round213_source_g_round182_residual_dimensional_union_verifier.py
```

Independent verifier:

```text
env PYTHONDONTWRITEBYTECODE=1 PYTHONHASHSEED=213062 \
  /usr/bin/time -v .venv-neurips/bin/python -B \
  deliverables/cm2_round213_source_g_round182_residual_dimensional_union_verifier.py \
  --output deliverables/.cm2_round213_seed213062_verification.json \
  --expect-result \
  5e21201a1c8741fa0d33bd83d3e284ff927fcf6589e7666fcf865d74093eb5a1
```

| Run | Seed | User | System | Wall | Peak RSS | Exit |
|---|---:|---:|---:|---:|---:|---:|
| official verifier | 213061 | 119.92 s | 4.31 s | 2:04.30 | 1,503,964 KiB | 0 |
| independent verifier | 213062 | 128.08 s | 4.65 s | 2:12.79 | 1,503,252 KiB | 0 |

Both runs printed only
`5e21201a1c8741fa0d33bd83d3e284ff927fcf6589e7666fcf865d74093eb5a1`.
Both verification files were `5,576` bytes; `cmp` returned zero, and both
file SHA-256 values were
`2fa0501932bee9744c4e702398c2e436c86c2cae0289c93bcdffe7250e9ecc3d`.

Each verifier run:

- replayed four manifests and all `25` exact entries;
- rebuilt the complete expected result before reading candidate bytes;
- independently audited all `8,332` origin rows and `36` ordinal rows;
- required full expected Python-object and canonical-byte equality;
- rejected `22/22` re-signed semantic attacks;
- rejected `15/15` strict JSON/encoding/oversize attacks;
- rejected or safely bypassed `21/21` path/type/alias/temp attacks;
- never imported or executed the producer; and
- retained zero physical-component, whole-origin, whole-tube, and global
  exact-key-disposition credit.

## Cleanup and disposition

After successful `cmp`, SHA-256, byte-count, and result-digest checks, the
hidden producer and verifier replay files were deleted. No attack scratch
file, symlink, FIFO, hardlink, parent alias, or prepositioned temporary
remains.

The formal scope remains local:

- physical-component deduplication: incomplete;
- whole-origin and whole-original-tube credit: `0`;
- source-G global exact-key dispositions: `0/224580`;
- D02: `BLOCKED`;
- Gate5: `10/18`;
- CM2: `NO-GO_FOR_CLAIM`.
