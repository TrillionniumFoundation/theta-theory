# Round271 Cold Replay

```bash
python3 -m py_compile \
  deliverables/cm2_round271_source_g_wall_and_outgoing_tail_signature_materialization.py \
  deliverables/cm2_round271_source_g_wall_and_outgoing_tail_signature_materialization_verifier.py
PYTHONPATH=deliverables PYTHONHASHSEED=271071 .venv-cm2/bin/python \
  deliverables/cm2_round271_source_g_wall_and_outgoing_tail_signature_materialization.py \
  --seed 271071 --processes 40
cp deliverables/cm2_round271_source_g_wall_and_outgoing_tail_signature_materialization_certificate.json \
  /tmp/r271-cert-271071.json
PYTHONPATH=deliverables PYTHONHASHSEED=271929 .venv-cm2/bin/python \
  deliverables/cm2_round271_source_g_wall_and_outgoing_tail_signature_materialization.py \
  --seed 271929 --processes 40
cmp /tmp/r271-cert-271071.json \
  deliverables/cm2_round271_source_g_wall_and_outgoing_tail_signature_materialization_certificate.json
PYTHONPATH=deliverables PYTHONHASHSEED=271929 .venv-cm2/bin/python \
  deliverables/cm2_round271_source_g_wall_and_outgoing_tail_signature_materialization_verifier.py \
  --processes 40
(cd deliverables && sha256sum -c \
  cm2_round271_source_g_wall_and_outgoing_tail_signature_materialization_manifest.sha256)
```

Expected statuses:

- `CERTIFIED_45420_OF_45916_REMAINING_CLOSED_LEAVES__70420_COMPLETE_SIDE_SIGNATURES__ALL_12_OUTGOING_TAILS_CLOSED__496_DUAL_FACTOR_WALL_RESIDUALS__ZERO_PROMOTION`
- `PASS_INDEPENDENT_ROUND271`
