# CM2 Round178 cold replay

Date: 2026-07-26

All commands were run from `deliverables/` with
`../.venv-neurips/bin/python` (`python-flint==0.9.0`) and bytecode writes
disabled.  Producer and verifier used the same module import order under
both hash seeds.

```bash
PYTHONDONTWRITEBYTECODE=1 PYTHONHASHSEED=1 \
  ../.venv-neurips/bin/python \
  cm2_round178_later_return_exact_key_bridge.py \
  --output cm2_round178_later_return_exact_key_bridge_certificate.seed1.tmp.json

PYTHONDONTWRITEBYTECODE=1 PYTHONHASHSEED=1 \
  ../.venv-neurips/bin/python \
  cm2_round178_later_return_exact_key_bridge_verifier.py \
  --output cm2_round178_later_return_exact_key_bridge_verification.seed1.tmp.json

PYTHONDONTWRITEBYTECODE=1 PYTHONHASHSEED=987654321 \
  ../.venv-neurips/bin/python \
  cm2_round178_later_return_exact_key_bridge.py \
  --output \
  cm2_round178_later_return_exact_key_bridge_certificate.seed987654321.tmp.json

PYTHONDONTWRITEBYTECODE=1 PYTHONHASHSEED=987654321 \
  ../.venv-neurips/bin/python \
  cm2_round178_later_return_exact_key_bridge_verifier.py \
  --output \
  cm2_round178_later_return_exact_key_bridge_verification.seed987654321.tmp.json
```

The producer printed the same result digest in both runs:

```text
c9da1d3312c4fe8253941e35e8113e1ac14e23e6ce58b7e0ff4ed2b0ebbda31b
```

The verifier printed the same verification-result digest in both runs:

```text
ea725103b4801814702e6112d29d1daac891c8d87b64a2bb027e9c7b83fc1e01
```

File-level comparisons, not merely result-field comparisons, passed:

```bash
cmp -s \
  cm2_round178_later_return_exact_key_bridge_certificate.json \
  cm2_round178_later_return_exact_key_bridge_certificate.seed1.tmp.json

cmp -s \
  cm2_round178_later_return_exact_key_bridge_certificate.seed1.tmp.json \
  cm2_round178_later_return_exact_key_bridge_certificate.seed987654321.tmp.json

cmp -s \
  cm2_round178_later_return_exact_key_bridge_verification.seed1.tmp.json \
  cm2_round178_later_return_exact_key_bridge_verification.seed987654321.tmp.json
```

The byte hashes were:

```text
31005b55c465db29e2e562ca8b94cde18b6c14fb830da7cbc6ef63d27a532f70  certificate (official, seed 1, seed 987654321)
ae3752a31b13f6dc2b503bab4a407af75644407b8a9686a4a01cef777ad7956b  verification (seed 1, seed 987654321)
```

The final verifier source hash embedded in the verification is:

```text
73b3229d6349021b874ecab7e9036989b519e005baac91fb3a6fb0c49650daeb
```

The effective Arb precision was 384 bits in both runs.  This is a
consequence of the fixed pinned import order: the atlas initializes the
shared context at 192 bits, and the pinned registry's transitive dependency
chain raises it to 384 bits.  Round178 does not manually raise precision.
The verifier separately checks the actual source hashes

```text
2da58e5fb5fe030023d6fade7252ec67d0e494708b32d1e32b3ce545e2052fdb  cm2_gate25_physical_return_core_registry_cert.py
18385fe423aeb38c4ea988f11b76293e573becf82c50e663030f17ae70430fc9  cm2_gate34_round26_q1_time2_frontier_cert.py
```

against the pinned Round28 registry's embedded dependency hashes.
