# CM2 Round258 Cold Replay

## Commands

```bash
.venv-cm2/bin/python -m py_compile \
  deliverables/cm2_round258_source_g_whole_box_boundary_face_saturation.py \
  deliverables/cm2_round258_source_g_whole_box_boundary_face_saturation_verifier.py

PYTHONHASHSEED=258071 .venv-cm2/bin/python \
  deliverables/cm2_round258_source_g_whole_box_boundary_face_saturation.py
PYTHONHASHSEED=258071 .venv-cm2/bin/python \
  deliverables/cm2_round258_source_g_whole_box_boundary_face_saturation_verifier.py

PYTHONHASHSEED=258929 .venv-cm2/bin/python \
  deliverables/cm2_round258_source_g_whole_box_boundary_face_saturation.py
PYTHONHASHSEED=258929 .venv-cm2/bin/python \
  deliverables/cm2_round258_source_g_whole_box_boundary_face_saturation_verifier.py
```

## Frozen Results

- Producer status: `CERTIFIED_904_STRICT_WHOLE_BOX_BOUNDARY_FACES__468_RANK_REDUCTIONS__QUOTIENT_74012_TO_73544`.
- Independent verifier status: `PASS_INDEPENDENT_ROUND258`.
- Producer result SHA256: `257c999bb77d1f9e8993898ec2a51675e83e27879b750a160b515a60bb1e13a8`.
- Verifier result SHA256: `9b948f85f4b92a4b1ab04ecc41e255d8c1cfa1a6381e48dd89f878558fc539f2`.
- Certificate file SHA256: `11d546a00cf27ae1fe5e146a18a64436676ec73214cd15dd294bb03bfb0359bb`.
- Verification file SHA256: `bb530dd4864274ab13fcd6a7619e4a049617add52ce5ee5c84d948947a49f0c7`.
- Seeds `258071` and `258929` are byte-identical for both JSON outputs.
