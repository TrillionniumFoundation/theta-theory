# Round264 Cold Replay

Environment: Python 3.12.3 in `.venv-cm2`.

```bash
.venv-cm2/bin/python -m py_compile \
  deliverables/cm2_round264_source_g_lower_dimensional_endpoint_correction_and_glue_closure.py \
  deliverables/cm2_round264_source_g_lower_dimensional_endpoint_correction_and_glue_closure_verifier.py
PYTHONHASHSEED=264071 .venv-cm2/bin/python \
  deliverables/cm2_round264_source_g_lower_dimensional_endpoint_correction_and_glue_closure.py
PYTHONHASHSEED=264071 .venv-cm2/bin/python \
  deliverables/cm2_round264_source_g_lower_dimensional_endpoint_correction_and_glue_closure_verifier.py
cp deliverables/cm2_round264_source_g_lower_dimensional_endpoint_correction_and_glue_closure_certificate.json \
  /tmp/r264-cert-264071.json
cp deliverables/cm2_round264_source_g_lower_dimensional_endpoint_correction_and_glue_closure_verification.json \
  /tmp/r264-verification-264071.json
PYTHONHASHSEED=264929 .venv-cm2/bin/python \
  deliverables/cm2_round264_source_g_lower_dimensional_endpoint_correction_and_glue_closure.py
PYTHONHASHSEED=264929 .venv-cm2/bin/python \
  deliverables/cm2_round264_source_g_lower_dimensional_endpoint_correction_and_glue_closure_verifier.py
cmp /tmp/r264-cert-264071.json \
  deliverables/cm2_round264_source_g_lower_dimensional_endpoint_correction_and_glue_closure_certificate.json
cmp /tmp/r264-verification-264071.json \
  deliverables/cm2_round264_source_g_lower_dimensional_endpoint_correction_and_glue_closure_verification.json
(cd deliverables && sha256sum -c \
  cm2_round264_source_g_lower_dimensional_endpoint_correction_and_glue_closure_manifest.sha256)
```

Expected statuses:

- `CERTIFIED_SOURCE_G_LOWER_DIMENSIONAL_ENDPOINT_COVER_CORRECTION__400_EMPTY_BULKS_REMOVED__248_ENDPOINT_SHEET_IDENTITIES_AND_32_ROUND204_TAIL_GLUES_CLOSED__POST_ROUND264_COMPONENTS_68312`
- `PASS_INDEPENDENT_ROUND264`
