# Round268 Cold Replay

```bash
python3 -m py_compile \
  deliverables/cm2_round268_source_g_true_seam_candidate_geometry_exhaustion.py \
  deliverables/cm2_round268_source_g_true_seam_candidate_geometry_exhaustion_verifier.py
PYTHONHASHSEED=268071 python3 \
  deliverables/cm2_round268_source_g_true_seam_candidate_geometry_exhaustion.py \
  --seed 268071
cp deliverables/cm2_round268_source_g_true_seam_candidate_geometry_exhaustion_certificate.json \
  /tmp/r268-cert-268071.json
PYTHONHASHSEED=268929 python3 \
  deliverables/cm2_round268_source_g_true_seam_candidate_geometry_exhaustion.py \
  --seed 268929
cmp /tmp/r268-cert-268071.json \
  deliverables/cm2_round268_source_g_true_seam_candidate_geometry_exhaustion_certificate.json
PYTHONHASHSEED=268929 python3 \
  deliverables/cm2_round268_source_g_true_seam_candidate_geometry_exhaustion_verifier.py \
  --seed 268929
(cd deliverables && sha256sum -c \
  cm2_round268_source_g_true_seam_candidate_geometry_exhaustion_manifest.sha256)
```

Expected statuses:

- `CERTIFIED_COMPLETE_ROUND182_TRUE_SOURCE_SEAM_GEOMETRY_EXHAUSTION__152_POSITIVE_AREA_OWNER_SHADOW_PATCHES__13772_EXACT_EMPTY_PAIRS__ZERO_PREMATURE_COMPONENT_CREDIT`
- `PASS_INDEPENDENT_ROUND268`
