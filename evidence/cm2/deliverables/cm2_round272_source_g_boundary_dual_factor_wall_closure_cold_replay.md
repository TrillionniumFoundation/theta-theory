# Round272 Cold Replay

```bash
python3 -m py_compile \
  deliverables/cm2_round272_source_g_boundary_dual_factor_wall_closure.py \
  deliverables/cm2_round272_source_g_boundary_dual_factor_wall_closure_verifier.py
PYTHONPATH=deliverables PYTHONHASHSEED=272071 .venv-cm2/bin/python \
  deliverables/cm2_round272_source_g_boundary_dual_factor_wall_closure.py \
  --seed 272071 --processes 40
cp deliverables/cm2_round272_source_g_boundary_dual_factor_wall_closure_certificate.json \
  /tmp/r272-cert-272071.json
PYTHONPATH=deliverables PYTHONHASHSEED=272929 .venv-cm2/bin/python \
  deliverables/cm2_round272_source_g_boundary_dual_factor_wall_closure.py \
  --seed 272929 --processes 40
cmp /tmp/r272-cert-272071.json \
  deliverables/cm2_round272_source_g_boundary_dual_factor_wall_closure_certificate.json
PYTHONPATH=deliverables PYTHONHASHSEED=272929 .venv-cm2/bin/python \
  deliverables/cm2_round272_source_g_boundary_dual_factor_wall_closure_verifier.py \
  --processes 40
(cd deliverables && sha256sum -c \
  cm2_round272_source_g_boundary_dual_factor_wall_closure_manifest.sha256)
```

Expected statuses:

- `CERTIFIED_ALL_496_APPARENT_DUAL_FACTOR_WALL_LEAVES__720_COMPLETE_SIDE_SIGNATURES__SOURCE_FACTOR_ZERO_ONLY_ON_EXCLUDED_t0_FACE__CLOSED_LEAF_RESIDUAL_ZERO__ZERO_PROMOTION`
- `PASS_INDEPENDENT_ROUND272`
