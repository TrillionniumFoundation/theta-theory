# CM2 Round257 Cold Replay

## Commands

```bash
.venv-cm2/bin/python -m py_compile \
  deliverables/cm2_round257_source_g_occurrence_fibre_volume_overlap_saturation.py \
  deliverables/cm2_round257_source_g_occurrence_fibre_volume_overlap_saturation_verifier.py

PYTHONHASHSEED=257071 .venv-cm2/bin/python \
  deliverables/cm2_round257_source_g_occurrence_fibre_volume_overlap_saturation.py
PYTHONHASHSEED=257071 .venv-cm2/bin/python \
  deliverables/cm2_round257_source_g_occurrence_fibre_volume_overlap_saturation_verifier.py

PYTHONHASHSEED=257929 .venv-cm2/bin/python \
  deliverables/cm2_round257_source_g_occurrence_fibre_volume_overlap_saturation.py
PYTHONHASHSEED=257929 .venv-cm2/bin/python \
  deliverables/cm2_round257_source_g_occurrence_fibre_volume_overlap_saturation_verifier.py
```

## Frozen Results

- Producer status: `CERTIFIED_53968_OCCURRENCE_GEOMETRIES__729700_X_SWEEP_CANDIDATES__17716_INTERNAL_POSITIVE_VOLUME_OVERLAPS__ZERO_CROSS_COMPONENT_OVERLAPS`.
- Independent verifier status: `PASS_INDEPENDENT_ROUND257`.
- Producer result SHA256: `0d6fe152167a7108908e8348a8e36cd52a96e83400b2a145b761b2741b26c54e`.
- Verifier result SHA256: `cf279b49bdd0cefbabcf76827fe334bb7bf35a29e48ede641491dd27aea369ba`.
- Certificate file SHA256: `320d8221dcc11d227f667a9e7efbd64c5e40f1de214b22ddd5264079b93504fb`.
- Verification file SHA256: `44587d331eba27429aee30f26066771372841c413277a50772b041a64c85dd3d`.
- Seeds `257071` and `257929` are byte-identical for both JSON outputs.
