# Round270 Cold Replay

```bash
python3 -m py_compile \
  deliverables/cm2_round270_source_g_outgoing_g_factor_signature_materialization.py \
  deliverables/cm2_round270_source_g_outgoing_g_factor_signature_materialization_verifier.py
PYTHONPATH=deliverables PYTHONHASHSEED=270071 .venv-cm2/bin/python \
  deliverables/cm2_round270_source_g_outgoing_g_factor_signature_materialization.py \
  --seed 270071 --processes 40
cp deliverables/cm2_round270_source_g_outgoing_g_factor_signature_materialization_certificate.json \
  /tmp/r270-cert-270071.json
PYTHONPATH=deliverables PYTHONHASHSEED=270929 .venv-cm2/bin/python \
  deliverables/cm2_round270_source_g_outgoing_g_factor_signature_materialization.py \
  --seed 270929 --processes 40
cmp /tmp/r270-cert-270071.json \
  deliverables/cm2_round270_source_g_outgoing_g_factor_signature_materialization_certificate.json
PYTHONPATH=deliverables PYTHONHASHSEED=270929 .venv-cm2/bin/python \
  deliverables/cm2_round270_source_g_outgoing_g_factor_signature_materialization_verifier.py \
  --processes 40
(cd deliverables && sha256sum -c \
  cm2_round270_source_g_outgoing_g_factor_signature_materialization_manifest.sha256)
```

Expected statuses:

- `CERTIFIED_24504_OF_24512_OUTGOING_G_LEAVES__37712_COMPLETE_SIDE_SIGNATURES__8_WALL_EVENT_RESIDUALS__ZERO_OCCURRENCE_OR_COMPONENT_PROMOTION`
- `PASS_INDEPENDENT_ROUND270`
