# CM2 Round218 compact-q frontier cold replay

Date: 2026-07-27

## Frozen identities

The read-only probe source SHA256 is:

```text
1dadb46be62853391898314b4a9fbbf5aae2750e70a21e3d891e975f45a3cfbf
```

The safe companion materializer source SHA256 is:

```text
ed787e6927df8eb48db3168929ab66d3753076b1a32f0e0429797504f7b91b11
```

The two canonical stdout documents are byte-identical and have file SHA256:

```text
2ab74d50cb01aab51dcd16fa1541c649d93a58a7faeb5141239be1ba33090d68
```

Their result SHA256 is:

```text
f440ee0ac043067a48b8ed8e217a827ed8c0e5072778e84931090df8cd4f7000
```

The pretty canonical result contains `1,961,083` bytes, is object-identical
to both stdout documents, and has file SHA256:

```text
dc4d86f68393736c314005aff27ea2febb8072e3224c892090d8a7cf54844887
```

The frozen Round215 manifest and bounded-probe dependencies are pinned as:

```text
Round215 manifest  6a6463c2574b971ce6909593886f6ad4c23bddb232772fdacebb4ecca70a405a
Round215 probe     463dfe832b32459b356bdfa0602c5eacea82569734f7ad1016c97ffa9d6c40c1
```

All six Round215 manifest entries are replayed before the Round218 census.

## Environment and commands

Both complete runs used Python 3.12.3, python-flint 0.9.0, Arb precision 192
bits, `LC_ALL=C`, and `TZ=UTC`:

```bash
/usr/bin/time -v env PYTHONHASHSEED=218014 LC_ALL=C TZ=UTC \
  /tmp/cm2-flint-venv/bin/python \
  deliverables/cm2_round218_source_w_compact_q_source_stratum_frontier.py

/usr/bin/time -v env PYTHONHASHSEED=218015 LC_ALL=C TZ=UTC \
  /tmp/cm2-flint-venv/bin/python \
  deliverables/cm2_round218_source_w_compact_q_source_stratum_frontier.py
```

| Run | User | System | Wall | Peak RSS | Exit |
|---|---:|---:|---:|---:|---:|
| Seed `218014` | 245.08 s | 0.16 s | 4:05.29 | 140,208 KiB | 0 |
| Seed `218015` | 253.26 s | 0.18 s | 4:13.48 | 139,216 KiB | 0 |

The canonical stdout files compare byte-for-byte (`cmp = 0`).  No workspace
output path is accepted by the probe and no file is written by it.

The companion materializer reran the same pinned rebuild under seed `218016`
and wrote only the exact official result filename using same-directory
`mkstemp`, file and directory `fsync`, and `os.replace`:

| Run | User | System | Wall | Peak RSS | Exit |
|---|---:|---:|---:|---:|---:|
| Materializer, seed `218016` | 252.03 s | 0.17 s | 4:12.38 | 136,272 KiB | 0 |

Its stdout result digest is the same
`f440ee0ac043067a48b8ed8e217a827ed8c0e5072778e84931090df8cd4f7000`.

## Reconstructed frontier

Both hash seeds independently reproduce:

```text
54 frozen COMPACT_Q_PRESENT origins
114 Round176 preclosed leaves
2,230 Round176 residual roots
844 initial compact-q source-grazing roots
21,334 Round180 final children
18,782 exact-behind closed children
2,552 geometric residual children
```

The q=0 face census is:

```text
648 excluded
124 live
 48 unresolved multi-root
 24 unresolved outgoing seam
844 total
```

The exact source-face owner audit contains 844 unique 2D patches, 2,218
atomic 1D edges, and 1,428 atomic 0D corners.  No duplicate 2D
representation occurs.

The depth-ten 3D compact-q tree contains:

```text
53,550 excluded terminal cells
 2,960 live terminal cells
80,388 residual cells
136,898 terminal-or-residual leaves
136,054 internal split faces
```

No one of the 844 initial q roots closes completely.  All 54 origins retain
a 3D q-tree obstruction.  Twenty-six origins also have a nonexcluded q=0
face; the other 28 have all q=0 faces excluded but still retain an open-3D
q obstruction.

## Fail-closed development record

The first development run stopped at the eleventh origin because the proposed
registry check accumulated only frontier closures and omitted the earlier
`origin_kinds` terminal dispositions.  The replay was repaired by including
the frozen early dispositions before adding frontier closures.  No registry
equality was weakened.

The second development run completed the full 844-root q tree and then
stopped on an intentionally strong hypothesis that every compact origin
must retain a rectangular outer 3D residual.  The exact result is subtler:
26 origins retain such a residual and 28 do not, while all 54 still retain a
compact-q source-stratum obstruction.  The final probe records both supports
separately and keeps a hard per-origin q-obstruction requirement.  No whole
credit was introduced.

## Formal state

Round218 is a bounded nonpromotional frontier probe.  It does not claim a
complete cross-root 3D/2D/1D/0D partition and grants zero integer credit.
The ledger remains:

```text
74,584 excluded
 2,248 conservative live
76,832 total
252 remaining = 198 mixed + 54 compact-q
```

`D02` remains `BLOCKED`, `D03` remains `UNAUTHORIZED`, Gate5 remains
`10/18`, complete global 18-field blocks remain zero, and CM2 remains
`NO-GO_FOR_CLAIM`.
