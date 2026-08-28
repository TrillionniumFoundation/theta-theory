# CM2 Round167 cold replay

Use the workspace environment:

```bash
PYTHONDONTWRITEBYTECODE=1 PYTHONHASHSEED=31091 \
  .venv-neurips/bin/python -B \
  deliverables/cm2_round167_base_r1_exact_key_deficit_registry.py

PYTHONDONTWRITEBYTECODE=1 PYTHONHASHSEED=42017 \
  .venv-neurips/bin/python -B \
  deliverables/cm2_round167_base_r1_exact_key_deficit_registry_verifier.py
```

Expected result digests:

```text
certificate result  de11046ac15949b5e69493987d3963c5547be77ba741a55bb10f9e3ad170b552
verification result 0aa1cb693105f92c77241fe1238d9cc0f494ecb82a5130a3ce23d1555fea3c5a
verification status PASS
semantic attacks    14/14 re-signed attacks rejected
```

Both outputs must be canonical single-newline JSON and byte-identical to the
published certificate and verification files.
