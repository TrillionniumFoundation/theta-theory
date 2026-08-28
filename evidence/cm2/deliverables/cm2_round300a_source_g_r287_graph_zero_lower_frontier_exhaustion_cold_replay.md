# Round300-A R287 graph-zero frontier — dual-seed cold replay

## Verdict

PASS.  Producer seeds `300101` and `300929` generate byte-identical ledger
and result artifacts.  Independent-verifier seeds/hash seeds `300311` and
`300929` reconstruct the same expected package and emit identical independent
attack-suite and verification commitments.  Seeds are accepted only as replay
bookkeeping and do not select or order evidence.

## Producer replay

Canonical run:

```text
python -B \
  deliverables/cm2_round300a_source_g_r287_graph_zero_lower_frontier_exhaustion.py \
  --seed 300101
```

Isolated second run:

```text
round300a_tmpdir=$(mktemp -d)
python -B \
  deliverables/cm2_round300a_source_g_r287_graph_zero_lower_frontier_exhaustion.py \
  --seed 300929 \
  --ledger "$round300a_tmpdir/ledger.json.gz" \
  --result "$round300a_tmpdir/result.json"

cmp \
  deliverables/cm2_round300a_source_g_r287_graph_zero_lower_frontier_exhaustion_ledger.json.gz \
  "$round300a_tmpdir/ledger.json.gz"
cmp \
  deliverables/cm2_round300a_source_g_r287_graph_zero_lower_frontier_exhaustion_result.json \
  "$round300a_tmpdir/result.json"
```

Both seeds reproduce:

```text
producer SHA256
f61dccfb8a20328c80bcfaa3458a10988dae73985a2ba23daa7491f4306f5e65

ledger file SHA256
ddc1a8bc53861afeb93d3569c6efa228f17d86f161db31a39fa9b72458ab8f2d

result file SHA256
b8f7c27f8761f1eb611f8fd57a0e773572f045963560f5d63b44baa1680e7ee4

result self-closure
dbba3aaa96a494144427709c7d908fc816c12cd9f87ff13ec06a818c832d7f98
```

The exact census is unchanged:

```text
3488 R287 source pairs
6292 raw Round294 endpoint expansions
3232 canonical unordered occurrence pairs
0 self pairs
3060 duplicate source expansions
128 explicit prior R295-A lower graph-sheet witnesses
3104 endpoint-specific common-zero-trace obligations
0 new component-edge or DSU-rank credit
```

## Independent-verifier replay

Canonical independent run:

```text
PYTHONDONTWRITEBYTECODE=1 PYTHONHASHSEED=300311 /usr/bin/time -p \
  python -B \
  deliverables/cm2_round300a_source_g_r287_graph_zero_lower_frontier_exhaustion_verifier.py \
  --seed 300311
```

Second cacheless no-write run:

```text
PYTHONDONTWRITEBYTECODE=1 PYTHONHASHSEED=300929 /usr/bin/time -p \
  python -B \
  deliverables/cm2_round300a_source_g_r287_graph_zero_lower_frontier_exhaustion_verifier.py \
  --seed 300929 --no-write
```

Both runs independently stream the complete Round294/R295-A ledgers and
reconstruct expected objects before opening candidate artifacts.  Both report:

```text
PASS_INDEPENDENT_CACHELESS_ROUND300A_FAIL_CLOSED_FRONTIER_EXHAUSTION
25/25 attacks rejected
24/24 reclosed semantic attacks rejected
```

Stable commitments:

```text
verifier SHA256
b425a9836a474122a99cd76a0f4e81175c65c2f426ad7e38773cce46220c64d5

attack-suite file SHA256
59e30957150d30b796edab4afc74267d5c885d3d3caea0d52f3cfd0338b21e80

attack-suite self-closure
390a4fc6558d9cee9dc0cb3b024946e5fe4354504dd461107d4fe6f0915617c1

verification file SHA256
e976fc2912c1d902029b8c4c7d4864bd8bb1cb6895bc09c215f2a5ac2400c696

verification self-closure
fed82ab1403e0f496245066b469d686b3126a3588c27459d9b0b53f8b08e7495
```

The verifier never imports, executes, parses, or text-decodes the producer.
The producer is used only as the inert fixed byte object
`f61dccfb8a20328c80bcfaa3458a10988dae73985a2ba23daa7491f4306f5e65`.

