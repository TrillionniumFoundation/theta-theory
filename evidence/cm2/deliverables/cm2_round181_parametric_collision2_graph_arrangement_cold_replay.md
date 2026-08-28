# CM2 Round181 cold replay

Date: 2026-07-26

Run from `deliverables/` with `python-flint==0.9.0`, effective 384-bit
Arb, disabled bytecode writes, and the same fixed import order:

```bash
PYTHONDONTWRITEBYTECODE=1 PYTHONHASHSEED=1 \
  ../.venv-neurips/bin/python \
  cm2_round181_parametric_collision2_graph_arrangement.py

PYTHONDONTWRITEBYTECODE=1 PYTHONHASHSEED=1 \
  ../.venv-neurips/bin/python \
  cm2_round181_parametric_collision2_graph_arrangement_verifier.py

PYTHONDONTWRITEBYTECODE=1 PYTHONHASHSEED=987654321 \
  ../.venv-neurips/bin/python \
  cm2_round181_parametric_collision2_graph_arrangement.py \
  --output \
  cm2_round181_parametric_collision2_graph_arrangement_certificate.seed987654321.tmp.json

PYTHONDONTWRITEBYTECODE=1 PYTHONHASHSEED=987654321 \
  ../.venv-neurips/bin/python \
  cm2_round181_parametric_collision2_graph_arrangement_verifier.py \
  --output \
  cm2_round181_parametric_collision2_graph_arrangement_verification.seed987654321.tmp.json
```

Both producer runs printed:

```text
fec1dc3e2c7d5145a9b6663f70b59903b0791e6f26099001296399995213f21e
```

Both verifier runs printed:

```text
4bab0cb1623371b122c67bb3f17a67a9d9a74a1d9a8d82aa0b430c2fa2d294a6
```

File-level comparisons passed:

```bash
cmp -s \
  cm2_round181_parametric_collision2_graph_arrangement_certificate.json \
  cm2_round181_parametric_collision2_graph_arrangement_certificate.seed987654321.tmp.json

cmp -s \
  cm2_round181_parametric_collision2_graph_arrangement_verification.json \
  cm2_round181_parametric_collision2_graph_arrangement_verification.seed987654321.tmp.json
```

Byte hashes:

```text
199e1793bf55062bf8ce26c7449aad4336896f3d312261f1c5c13efcdff41e77  certificate, both seeds
5511bcf66035a49917ea407140a863bc7e898428498cdac8c385b1a9473f8cf1  verification, both seeds
```

Source hashes:

```text
6e9d51229c209caacf3964d24600295375bd08e963b4e154774625707aa1524c  producer
5a4e18ea095d2f41b02b20f65cb20f230f0e51de48e176e3d39d9606ddfddd73  verifier
```
