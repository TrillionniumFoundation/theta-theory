# CM2 Round164 v2 cold replay

Use the workspace environment containing `python-flint==0.9.0`:

```bash
PYTHONDONTWRITEBYTECODE=1 PYTHONHASHSEED=31091 \
  .venv-neurips/bin/python -B \
  deliverables/cm2_round164_tangency_strata_pruning.py

PYTHONDONTWRITEBYTECODE=1 PYTHONHASHSEED=42017 \
  .venv-neurips/bin/python -B \
  deliverables/cm2_round164_tangency_strata_pruning_verifier.py
```

Expected result digests:

```text
certificate result  0f6d7f47ac20734ed294dd04cd7720ccbb9c0a1d4236980f814dd2ea2d5e79d9
verification result bb2e51bdbbd457a5782038efc527000cbf89b73c8645fd6facd126fa453af8c4
verification status PASS
semantic attacks    36/36 rejected after re-signing
strict JSON attacks  7/7 rejected.
```

The producer and verifier were replayed under separate hash seeds and were
byte-identical to their preceding temporary cold outputs.
