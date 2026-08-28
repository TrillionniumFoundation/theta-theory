# Round259 Cold Replay

Run from the workspace root with the pinned `.venv-cm2` environment.

```bash
rm -rf deliverables/__pycache__
.venv-cm2/bin/python -m py_compile \
  deliverables/cm2_round259_source_g_curved_region_full_face_saturation.py \
  deliverables/cm2_round259_source_g_curved_region_full_face_saturation_verifier.py

PYTHONHASHSEED=259071 .venv-cm2/bin/python \
  deliverables/cm2_round259_source_g_curved_region_full_face_saturation.py
PYTHONHASHSEED=259071 .venv-cm2/bin/python \
  deliverables/cm2_round259_source_g_curved_region_full_face_saturation_verifier.py

cp deliverables/cm2_round259_source_g_curved_region_full_face_saturation_certificate.json /tmp/round259-cert-259071.json
cp deliverables/cm2_round259_source_g_curved_region_full_face_saturation_verification.json /tmp/round259-verification-259071.json

PYTHONHASHSEED=259929 .venv-cm2/bin/python \
  deliverables/cm2_round259_source_g_curved_region_full_face_saturation.py
PYTHONHASHSEED=259929 .venv-cm2/bin/python \
  deliverables/cm2_round259_source_g_curved_region_full_face_saturation_verifier.py

cmp /tmp/round259-cert-259071.json \
  deliverables/cm2_round259_source_g_curved_region_full_face_saturation_certificate.json
cmp /tmp/round259-verification-259071.json \
  deliverables/cm2_round259_source_g_curved_region_full_face_saturation_verification.json

(cd deliverables && sha256sum -c \
  cm2_round259_source_g_curved_region_full_face_saturation_manifest.sha256)
```

Expected producer status:

`CERTIFIED_1988_STRICT_CURVED_REGION_FULL_FACES__1480_RANK_REDUCTIONS__QUOTIENT_73544_TO_72064`

Expected verifier status:

`PASS_INDEPENDENT_ROUND259`
