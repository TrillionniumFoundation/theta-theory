# Round260 Cold Replay

Run from the workspace root with `.venv-cm2`.

```bash
rm -rf deliverables/__pycache__
.venv-cm2/bin/python -m py_compile \
  deliverables/cm2_round260_source_g_curved_region_common_face_refinement.py \
  deliverables/cm2_round260_source_g_curved_region_common_face_refinement_verifier.py

PYTHONHASHSEED=260071 .venv-cm2/bin/python \
  deliverables/cm2_round260_source_g_curved_region_common_face_refinement.py
PYTHONHASHSEED=260071 .venv-cm2/bin/python \
  deliverables/cm2_round260_source_g_curved_region_common_face_refinement_verifier.py

cp deliverables/cm2_round260_source_g_curved_region_common_face_refinement_certificate.json /tmp/round260-cert-260071.json
cp deliverables/cm2_round260_source_g_curved_region_common_face_refinement_verification.json /tmp/round260-verification-260071.json

PYTHONHASHSEED=260929 .venv-cm2/bin/python \
  deliverables/cm2_round260_source_g_curved_region_common_face_refinement.py
PYTHONHASHSEED=260929 .venv-cm2/bin/python \
  deliverables/cm2_round260_source_g_curved_region_common_face_refinement_verifier.py

cmp /tmp/round260-cert-260071.json \
  deliverables/cm2_round260_source_g_curved_region_common_face_refinement_certificate.json
cmp /tmp/round260-verification-260071.json \
  deliverables/cm2_round260_source_g_curved_region_common_face_refinement_verification.json

(cd deliverables && sha256sum -c \
  cm2_round260_source_g_curved_region_common_face_refinement_manifest.sha256)
```

Expected producer status:

`CERTIFIED_6728_STRICT_DYADIC_COMMON_FACE_PATCHES__3188_RANK_REDUCTIONS__QUOTIENT_72064_TO_68876`

Expected verifier status: `PASS_INDEPENDENT_ROUND260`.
