# Round266 Cold Replay

Environment: Python 3.12.3, python-flint 0.9.0, fixed Arb precision 256 bits.

```bash
.venv-cm2/bin/python -m py_compile \
  deliverables/cm2_round266_source_g_expanded_curved_face_closure.py \
  deliverables/cm2_round266_source_g_expanded_curved_face_closure_verifier.py
cmp deliverables/cm2_round266_source_g_expanded_curved_face_closure_seed266071_certificate.json \
  deliverables/cm2_round266_source_g_expanded_curved_face_closure_seed266929_certificate.json
cmp deliverables/cm2_round266_source_g_expanded_curved_face_closure_seed266071_certificate.json \
  deliverables/cm2_round266_source_g_expanded_curved_face_closure_certificate.json
PYTHONHASHSEED=266929 .venv-cm2/bin/python \
  deliverables/cm2_round266_source_g_expanded_curved_face_closure_verifier.py \
  --seed 266929 --processes 40
(cd deliverables && sha256sum -c \
  cm2_round266_source_g_expanded_curved_face_closure_manifest.sha256)
```

Expected statuses:

- `CERTIFIED_2652_EXPANDED_CURVED_FULL_FACES__5304_STRICT_INWARD_CORRIDORS__588_RANK_REDUCTIONS__QUOTIENT_63812_TO_63224`
- `PASS_INDEPENDENT_ROUND266`
