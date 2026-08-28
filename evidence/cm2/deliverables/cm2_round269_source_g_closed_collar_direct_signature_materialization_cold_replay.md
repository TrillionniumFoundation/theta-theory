# Round269 Cold Replay

```bash
python3 -m py_compile \
  deliverables/cm2_round269_source_g_closed_collar_direct_signature_materialization.py \
  deliverables/cm2_round269_source_g_closed_collar_direct_signature_materialization_verifier.py
PYTHONPATH=deliverables PYTHONHASHSEED=269071 .venv-cm2/bin/python \
  deliverables/cm2_round269_source_g_closed_collar_direct_signature_materialization.py \
  --seed 269071 --processes 40
cp deliverables/cm2_round269_source_g_closed_collar_direct_signature_materialization_certificate.json \
  /tmp/r269-cert-269071.json
PYTHONPATH=deliverables PYTHONHASHSEED=269929 .venv-cm2/bin/python \
  deliverables/cm2_round269_source_g_closed_collar_direct_signature_materialization.py \
  --seed 269929 --processes 40
cmp /tmp/r269-cert-269071.json \
  deliverables/cm2_round269_source_g_closed_collar_direct_signature_materialization_certificate.json
PYTHONPATH=deliverables PYTHONHASHSEED=269929 .venv-cm2/bin/python \
  deliverables/cm2_round269_source_g_closed_collar_direct_signature_materialization_verifier.py \
  --processes 40
(cd deliverables && sha256sum -c \
  cm2_round269_source_g_closed_collar_direct_signature_materialization_manifest.sha256)
```

Expected statuses:

- `CERTIFIED_114032_OF_184452_ROUND182_CLOSED_LEAVES__187128_OUTGOING_W_SIDE_SIGNATURES__70420_FAIL_CLOSED__ZERO_OCCURRENCE_OR_COMPONENT_PROMOTION`
- `PASS_INDEPENDENT_ROUND269`
