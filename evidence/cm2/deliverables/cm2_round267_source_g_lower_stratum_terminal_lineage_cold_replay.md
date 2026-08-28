# Round267 Cold Replay

Environment: Python 3.12.3.

```bash
python3 -m py_compile \
  deliverables/cm2_round267_source_g_lower_stratum_terminal_lineage.py \
  deliverables/cm2_round267_source_g_lower_stratum_terminal_lineage_verifier.py
PYTHONHASHSEED=267071 python3 \
  deliverables/cm2_round267_source_g_lower_stratum_terminal_lineage.py \
  --seed 267071
cp deliverables/cm2_round267_source_g_lower_stratum_terminal_lineage_certificate.json \
  /tmp/r267-cert-267071.json
PYTHONHASHSEED=267929 python3 \
  deliverables/cm2_round267_source_g_lower_stratum_terminal_lineage.py \
  --seed 267929
cmp /tmp/r267-cert-267071.json \
  deliverables/cm2_round267_source_g_lower_stratum_terminal_lineage_certificate.json
PYTHONHASHSEED=267929 python3 \
  deliverables/cm2_round267_source_g_lower_stratum_terminal_lineage_verifier.py \
  --seed 267929
(cd deliverables && sha256sum -c \
  cm2_round267_source_g_lower_stratum_terminal_lineage_manifest.sha256)
```

Expected statuses:

- `CERTIFIED_COMPLETE_62696_ROUND174_LOWER_STRATUM_TERMINAL_LINEAGE__6120_DESCENDANT_WIDE_ABSENT__56576_CANONICAL_SUPPORTS_WITHOUT_NOMINAL_EXISTENCE_PROMOTION__ROUND266_QUOTIENT_AND_FRONTIERS_UNCHANGED`
- `PASS_INDEPENDENT_ROUND267`
