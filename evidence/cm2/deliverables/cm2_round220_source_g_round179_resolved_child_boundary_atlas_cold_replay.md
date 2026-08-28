# Round220 source-G Round179 resolved-child boundary-atlas cold replay

Date: 2026-07-27

## Frozen identities

- Producer SHA-256:
  `ae5c4fc259050bafeef335b88a3504ba3de49c64154f128ec26a461ebefdd3f4`
- Certificate byte count: `294,422,681`
- Certificate SHA-256:
  `569a7849b53805ff4deca0eff9a6938a897942d3d682dfef27c27559135ce974`
- Certificate result SHA-256:
  `4d8168cb25bd389f16b332798fcf9b57951deedd8d328bc5a1dac9024508669b`
- Verifier SHA-256:
  `1b61672336073c3edf3e1bfe3d5aa2c36854dbc8225e2fe69cd1e49f294a6b1c`
- Verification byte count: `2,401`
- Verification SHA-256:
  `17ede34d1494b286aba7c0daf0fbcc6e2e326736673265214acdf1f95680f2c5`
- Verification result SHA-256:
  `d753d748b344205ecdaa611b37b4adcc82868c82cf1ea008c92ba88688330ed6`

## Producer replays

```text
env PYTHONHASHSEED=220051 /usr/bin/time -v python -B \
  cm2_round220_source_g_round179_resolved_child_boundary_atlas.py \
  --output .cm2_round220_seed220051_certificate.json
```

```text
env PYTHONHASHSEED=220052 /usr/bin/time -v python -B \
  cm2_round220_source_g_round179_resolved_child_boundary_atlas.py
```

| Run | Seed | User | System | Wall | Peak RSS | Exit |
|---|---:|---:|---:|---:|---:|---:|
| independent producer | 220051 | 54.40 s | 3.49 s | 0:59.99 | 1,967,172 KiB | 0 |
| official producer | 220052 | 56.31 s | 3.10 s | 1:01.38 | 1,965,244 KiB | 0 |

Both outputs were `294,422,681` bytes.  `cmp` returned zero, both file
SHA-256 values were
`569a7849b53805ff4deca0eff9a6938a897942d3d682dfef27c27559135ce974`,
and both runs printed result SHA-256
`4d8168cb25bd389f16b332798fcf9b57951deedd8d328bc5a1dac9024508669b`.

## Frozen verifier replays

```text
env PYTHONHASHSEED=220065 /usr/bin/time -v python -B \
  cm2_round220_source_g_round179_resolved_child_boundary_atlas_verifier.py \
  --output .cm2_round220_seed220065_verification.json
```

```text
env PYTHONHASHSEED=220066 /usr/bin/time -v python -B \
  cm2_round220_source_g_round179_resolved_child_boundary_atlas_verifier.py
```

| Run | Seed | User | System | Wall | Peak RSS | Exit |
|---|---:|---:|---:|---:|---:|---:|
| independent verifier | 220065 | 165.48 s | 11.71 s | 2:57.57 | 2,123,216 KiB | 0 |
| official verifier | 220066 | 167.88 s | 12.11 s | 3:00.04 | 2,121,488 KiB | 0 |

Both outputs were `2,401` bytes.  `cmp` returned zero, both file SHA-256
values were
`17ede34d1494b286aba7c0daf0fbcc6e2e326736673265214acdf1f95680f2c5`,
and both runs printed verification result SHA-256
`d753d748b344205ecdaa611b37b4adcc82868c82cf1ea008c92ba88688330ed6`.

Every accepted verifier run:

- replayed three manifests and all `19` entries;
- independently reconstructed all `17,192` children, `103,152` faces,
  `206,304` edges, `137,536` corners, `13,076` split interfaces,
  `10,384` coordinate adjacencies, `9,830` rejected cross-parent
  coincidences, `13,092` normal forms, `17,208` normal references, and `116`
  key ledgers;
- required complete Python-object field equality and canonical result
  equality;
- never imported or executed the producer;
- rejected `10/10` attacks against the real candidate after recomputing the
  affected packed-table summaries and complete result SHA;
- rejected `15/15` malformed JSON attacks;
- rejected `34/34` path and hostile file-object attacks, including real
  candidate and output symlink, hardlink, FIFO, directory, size, missing, and
  parent-symlink cases; and
- reconfirmed zero whole-origin, physical-component, global-fibre, and
  disposition credit.

The additional `23` re-signed synthetic contract-snapshot attacks and one
unsigned snapshot attack are auxiliary and are not counted as attacks on the
complete candidate.

## Fail-closed development corrections

Two unfrozen verifier drafts were not accepted as final:

1. Seeds `220061/220062` fully reconstructed the atlas but used only a
   synthetic signed snapshot for mutation tests.
2. Seed `220063` added `10/10` truly re-signed attacks against the actual
   candidate, but its path suite had not yet instantiated every hostile file
   object.

Both drafts emitted only pre-verification artifacts.  The frozen verifier adds
the real file-object suite and was then rerun from scratch under independent
seeds `220065/220066`.

## Cleanup and claim boundary

After successful comparisons, hidden producer and verifier replay files were
deleted.  No attack scratch directory, symlink, hardlink, FIFO, directory,
oversize sparse file, output alias, or prepositioned temporary remains.

The formal claim boundary remains:

- Round179 resolved-child coordinate atlas: complete for `17,192/17,192`;
- event-sheet incidence on those resolved children: `0`;
- cross-chart event-trace glue: `0`;
- physical-component, whole-origin, whole-tube, global-fibre, and disposition
  credit: `0`;
- source-G dispositions: `0/224580`;
- D02: `BLOCKED`;
- Gate5: `10/18`; and
- CM2: `NO-GO_FOR_CLAIM`.
