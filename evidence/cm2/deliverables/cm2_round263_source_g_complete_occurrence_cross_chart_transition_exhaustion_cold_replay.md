# Round263 Cold Replay

Environment: Python 3.12.3 in `.venv-cm2`.

```bash
.venv-cm2/bin/python -m py_compile \
  deliverables/cm2_round263_source_g_complete_occurrence_cross_chart_transition_exhaustion.py \
  deliverables/cm2_round263_source_g_complete_occurrence_cross_chart_transition_exhaustion_verifier.py
PYTHONHASHSEED=263071 .venv-cm2/bin/python \
  deliverables/cm2_round263_source_g_complete_occurrence_cross_chart_transition_exhaustion.py
PYTHONHASHSEED=263071 .venv-cm2/bin/python \
  deliverables/cm2_round263_source_g_complete_occurrence_cross_chart_transition_exhaustion_verifier.py
cp deliverables/cm2_round263_source_g_complete_occurrence_cross_chart_transition_exhaustion_certificate.json \
  /tmp/r263-cert-263071.json
cp deliverables/cm2_round263_source_g_complete_occurrence_cross_chart_transition_exhaustion_verification.json \
  /tmp/r263-verification-263071.json
PYTHONHASHSEED=263929 .venv-cm2/bin/python \
  deliverables/cm2_round263_source_g_complete_occurrence_cross_chart_transition_exhaustion.py
PYTHONHASHSEED=263929 .venv-cm2/bin/python \
  deliverables/cm2_round263_source_g_complete_occurrence_cross_chart_transition_exhaustion_verifier.py
cmp /tmp/r263-cert-263071.json \
  deliverables/cm2_round263_source_g_complete_occurrence_cross_chart_transition_exhaustion_certificate.json
cmp /tmp/r263-verification-263071.json \
  deliverables/cm2_round263_source_g_complete_occurrence_cross_chart_transition_exhaustion_verification.json
(cd deliverables && sha256sum -c \
  cm2_round263_source_g_complete_occurrence_cross_chart_transition_exhaustion_manifest.sha256)
```

Expected statuses:

- `CERTIFIED_COMPLETE_53968_OCCURRENCE_TRUE_SOURCE_CHART_SEAM_EXHAUSTION__ZERO_SAME_POINT_CANDIDATES__JX_JY_NON_GLUE__POST_ROUND262_QUOTIENT_AND_FRONTIERS_UNCHANGED`
- `PASS_INDEPENDENT_ROUND263`
