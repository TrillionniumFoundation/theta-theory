# Round216 source-G global key-occurrence frontier cold replay

Date: 2026-07-27

## Frozen identities

- Producer SHA-256:
  `9da9d11ec0aa16e8dcbd22c0add51f373194008afa507da0432d3fee417c68fa`
- Certificate byte count: `174,708`
- Certificate SHA-256:
  `fa4cfb3b209518308c61ccdfa95834dd8e6899e6232fc40a569cbab4d6ecbe34`
- Certificate result SHA-256:
  `267a4b9aaaab6a576e1c1866cc2fa0b9dc9bf4fc6a3b08a210ed3821e45dd658`
- Verifier SHA-256:
  `9cafb5fdeb4fc6cd150b7d56b3298f0d808c2abfe81f173d1ccd3bed2c0d07a0`
- Verification byte count: `5,373`
- Verification SHA-256:
  `6ad6f2a7ee32f0a1abc2a004e3fcb4ca0de05d4e916c211220aed5cd39f872a2`
- Verification result SHA-256:
  `23055888339f4e42ba968706d895ff6123a6b7549cbe176de835b2e68d0c3a6d`

## Producer replays

```text
env PYTHONDONTWRITEBYTECODE=1 PYTHONHASHSEED=216051 \
  /usr/bin/time -v .venv-neurips/bin/python -B \
  deliverables/cm2_round216_source_g_global_key_occurrence_exhaustion_frontier.py
```

```text
env PYTHONDONTWRITEBYTECODE=1 PYTHONHASHSEED=216052 \
  /usr/bin/time -v .venv-neurips/bin/python -B \
  deliverables/cm2_round216_source_g_global_key_occurrence_exhaustion_frontier.py \
  --output deliverables/.cm2_round216_seed216052_certificate.json
```

| Run | Seed | User | System | Wall | Peak RSS | Exit |
|---|---:|---:|---:|---:|---:|---:|
| official producer | 216051 | 118.52 s | 7.12 s | 2:05.68 | 1,760,984 KiB | 0 |
| independent producer | 216052 | 108.42 s | 6.10 s | 1:55.33 | 1,762,544 KiB | 0 |

Both outputs were `174,708` bytes; `cmp` returned zero. Both file SHA-256
values were
`fa4cfb3b209518308c61ccdfa95834dd8e6899e6232fc40a569cbab4d6ecbe34`,
and both runs printed
`267a4b9aaaab6a576e1c1866cc2fa0b9dc9bf4fc6a3b08a210ed3821e45dd658`.

## Verifier replays

```text
env PYTHONDONTWRITEBYTECODE=1 PYTHONHASHSEED=216061 \
  /usr/bin/time -v .venv-neurips/bin/python -B \
  deliverables/cm2_round216_source_g_global_key_occurrence_exhaustion_frontier_verifier.py
```

```text
env PYTHONDONTWRITEBYTECODE=1 PYTHONHASHSEED=216062 \
  /usr/bin/time -v .venv-neurips/bin/python -B \
  deliverables/cm2_round216_source_g_global_key_occurrence_exhaustion_frontier_verifier.py \
  --output deliverables/.cm2_round216_seed216062_verification.json \
  --expect-result \
  23055888339f4e42ba968706d895ff6123a6b7549cbe176de835b2e68d0c3a6d
```

| Run | Seed | User | System | Wall | Peak RSS | Exit |
|---|---:|---:|---:|---:|---:|---:|
| official verifier | 216061 | 106.79 s | 6.34 s | 1:53.21 | 1,765,336 KiB | 0 |
| independent verifier | 216062 | 107.13 s | 6.22 s | 1:53.44 | 1,764,724 KiB | 0 |

Both outputs were `5,373` bytes; `cmp` returned zero. Both file SHA-256
values were
`6ad6f2a7ee32f0a1abc2a004e3fcb4ca0de05d4e916c211220aed5cd39f872a2`,
and both runs printed
`23055888339f4e42ba968706d895ff6123a6b7549cbe176de835b2e68d0c3a6d`.

Each accepted verifier run:

- replayed six manifests and all `38` entries plus the immutable Round213
  erratum;
- reconstructed the complete expected result before opening candidate bytes;
- audited all `116` closed key rows and both independent blockers;
- required full expected Python-object and canonical-byte equality;
- rejected `29/29` re-signed semantic attacks;
- rejected `15/15` strict JSON/encoding/oversize attacks;
- rejected or safely bypassed `20/20` path/type/alias/output/temp attacks;
- never imported or executed the producer; and
- retained zero component, whole, global-fibre, and disposition credit.

## Fail-closed development correction

An unfrozen verifier draft completed independent reconstruction and all
semantic/JSON attacks, then rejected its own symlink-parent input test
because the reader protected only the final path component. It emitted no
verification artifact. The frozen verifier additionally requires the exact
input directory and rejects `..` before opening. Its isolated path suite
passed `20/20`, after which both accepted full verifier seeds were run from
scratch.

## Cleanup and disposition

After successful comparisons, the hidden producer and verifier replay files
were deleted. No attack scratch file, symlink, FIFO, hardlink, output alias,
or prepositioned temporary remains.

The formal boundary remains nonpromotional:

- global exact-key fibres exhausted: `0/116`;
- physical, whole-origin, whole-tube, and global disposition credit: `0`;
- source-G dispositions: `0/224580`;
- concurrent Round217: not pinned or included;
- D02: `BLOCKED`;
- Gate5: `10/18`;
- CM2: `NO-GO_FOR_CLAIM`.
