# Round262 Cold Replay

Environment: Python 3.12.3 and `python-flint==0.9.0` in `.venv-cm2`.

```bash
.venv-cm2/bin/python -m py_compile \
  deliverables/cm2_round262_source_g_monotone_deep_common_face_closure.py \
  deliverables/cm2_round262_source_g_monotone_deep_common_face_closure_verifier.py
PYTHONHASHSEED=262071 .venv-cm2/bin/python \
  deliverables/cm2_round262_source_g_monotone_deep_common_face_closure.py \
  --workers 40
PYTHONHASHSEED=262071 .venv-cm2/bin/python \
  deliverables/cm2_round262_source_g_monotone_deep_common_face_closure_verifier.py \
  --workers 40
cp deliverables/cm2_round262_source_g_monotone_deep_common_face_closure_certificate.json \
  /tmp/r262-cert-262071.json
cp deliverables/cm2_round262_source_g_monotone_deep_common_face_closure_verification.json \
  /tmp/r262-verification-262071.json
PYTHONHASHSEED=262929 .venv-cm2/bin/python \
  deliverables/cm2_round262_source_g_monotone_deep_common_face_closure.py \
  --workers 40
PYTHONHASHSEED=262929 .venv-cm2/bin/python \
  deliverables/cm2_round262_source_g_monotone_deep_common_face_closure_verifier.py \
  --workers 40
cmp /tmp/r262-cert-262071.json \
  deliverables/cm2_round262_source_g_monotone_deep_common_face_closure_certificate.json
cmp /tmp/r262-verification-262071.json \
  deliverables/cm2_round262_source_g_monotone_deep_common_face_closure_verification.json
(cd deliverables && sha256sum -c \
  cm2_round262_source_g_monotone_deep_common_face_closure_manifest.sha256)
```

Expected statuses:

- `CERTIFIED_1584_MONOTONE_DEEP_COMMON_FACE_PATCHES__32_EXACT_BOUNDARY_EXHAUSTIONS__32_RANK_REDUCTIONS__QUOTIENT_68748_TO_68716__0_FAIL_CLOSED`
- `PASS_INDEPENDENT_ROUND262`
