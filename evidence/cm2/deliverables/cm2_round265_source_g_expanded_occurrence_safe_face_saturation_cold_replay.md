# Round265 Cold Replay

Environment: Python 3.12.3 in `.venv-cm2`.

```bash
.venv-cm2/bin/python -m py_compile \
  deliverables/cm2_round265_source_g_expanded_occurrence_safe_face_saturation.py \
  deliverables/cm2_round265_source_g_expanded_occurrence_safe_face_saturation_verifier.py
PYTHONHASHSEED=265071 .venv-cm2/bin/python \
  deliverables/cm2_round265_source_g_expanded_occurrence_safe_face_saturation.py
PYTHONHASHSEED=265071 .venv-cm2/bin/python \
  deliverables/cm2_round265_source_g_expanded_occurrence_safe_face_saturation_verifier.py
cp deliverables/cm2_round265_source_g_expanded_occurrence_safe_face_saturation_certificate.json \
  /tmp/r265-cert-265071.json
cp deliverables/cm2_round265_source_g_expanded_occurrence_safe_face_saturation_verification.json \
  /tmp/r265-verification-265071.json
PYTHONHASHSEED=265929 .venv-cm2/bin/python \
  deliverables/cm2_round265_source_g_expanded_occurrence_safe_face_saturation.py
PYTHONHASHSEED=265929 .venv-cm2/bin/python \
  deliverables/cm2_round265_source_g_expanded_occurrence_safe_face_saturation_verifier.py
cmp /tmp/r265-cert-265071.json \
  deliverables/cm2_round265_source_g_expanded_occurrence_safe_face_saturation_certificate.json
cmp /tmp/r265-verification-265071.json \
  deliverables/cm2_round265_source_g_expanded_occurrence_safe_face_saturation_verification.json
(cd deliverables && sha256sum -c \
  cm2_round265_source_g_expanded_occurrence_safe_face_saturation_manifest.sha256)
```

Expected statuses:

- `CERTIFIED_EXPANDED_126468_OCCURRENCE_SAFE_FULL_SIGNATURE_FACE_SATURATION__169064_SAFE_EDGES__77000_RANK_REDUCTIONS__POST_ROUND265_COMPONENTS_63812__2652_CURVED_FACES_FAIL_CLOSED`
- `PASS_INDEPENDENT_ROUND265`
