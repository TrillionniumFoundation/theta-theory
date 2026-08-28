# Round141 K4296 cold replay

Status: **PASS**

- Formal producer: `cm2_round141_recentered_affine_k4296_d0_collar_return.py`
- Centered engine: `cm2_round141_centered_affine_d0_collar_spike.py`
- Frozen certificate SHA-256: `a17660dbf106611e6ec9dc680d0d7e4075dd6504f9d727415b8c365e50d0cafe`
- Frozen result SHA-256: `48af243b2d8a77fb3f96751fbda7dc9ffeaf2f0768f8ec76426253d07702ea3f`

The formal 8192-bit producer was replayed from a separate process with
`PYTHONHASHSEED=91` to `/tmp/cm2-r141-cold-replay.json`.

- Runtime: `11:48.97`
- Maximum RSS: `223544 KB`
- Replay certificate SHA-256:
  `a17660dbf106611e6ec9dc680d0d7e4075dd6504f9d727415b8c365e50d0cafe`
- Byte comparison against the frozen certificate: identical (`cmp` exit 0)

The first pre-freeze producer attempt was deliberately interrupted after an
output-only defect was found: the terminal phase serializer used an
unpadded 128-bit dyadic outer enclosure.  That could reject a valid wide Arb
interval at the end of an otherwise successful replay.  It was not a
mathematical, candidate-owner, memory, or propagation failure.  The serializer
was changed to padded `floor-1` / `ceil+1` dyadic endpoints, all lost radius
remained enclosed, and the engine was then frozen at
`5656f33a4974b63124bda19c56716dccb7c52ad7840741668512795560007ef1`.

No Round139 or Round140 file was modified.
