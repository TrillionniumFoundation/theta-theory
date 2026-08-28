# Round279 cold replay

Use the workspace environment with `python-flint==0.9.0`.

```bash
python3 -m py_compile \
  deliverables/cm2_round279_source_g_depth4_face_edge_witness_materialization.py \
  deliverables/cm2_round279_source_g_collar_atom_and_face_edge_freeze.py \
  deliverables/cm2_round279_source_g_collar_atom_and_face_edge_freeze_verifier.py

PYTHONHASHSEED=279071 .venv-cm2/bin/python \
  deliverables/cm2_round279_source_g_depth4_face_edge_witness_materialization.py \
  --processes 40

PYTHONHASHSEED=279071 .venv-cm2/bin/python \
  deliverables/cm2_round279_source_g_collar_atom_and_face_edge_freeze.py \
  --seed 279071

PYTHONHASHSEED=279929 .venv-cm2/bin/python \
  deliverables/cm2_round279_source_g_collar_atom_and_face_edge_freeze.py \
  --seed 279929 \
  --certificate /tmp/cm2-r279-cert-279929.json \
  --atom-ledger /tmp/cm2-r279-atoms-279929.json.gz \
  --edge-ledger /tmp/cm2-r279-edges-279929.json.gz

cmp \
  deliverables/cm2_round279_source_g_collar_atom_and_face_edge_freeze_certificate.json \
  /tmp/cm2-r279-cert-279929.json
cmp \
  deliverables/cm2_round279_source_g_collar_atom_and_face_edge_freeze_atoms.json.gz \
  /tmp/cm2-r279-atoms-279929.json.gz
cmp \
  deliverables/cm2_round279_source_g_collar_atom_and_face_edge_freeze_edges.json.gz \
  /tmp/cm2-r279-edges-279929.json.gz

PYTHONHASHSEED=279071 .venv-cm2/bin/python \
  deliverables/cm2_round279_source_g_collar_atom_and_face_edge_freeze_verifier.py \
  --processes 40

(cd deliverables && sha256sum -c \
  cm2_round279_source_g_collar_atom_and_face_edge_freeze_manifest.sha256)
```

The recorded cache-poison replay additionally replaced
`/tmp/cm2_round277_candidate_runtime_cache.pkl` with a directory throughout
depth4 materialization, both producer seeds, and independent verification.
All commands completed without reading it.

Expected final statuses:

- `ROUND279_DEPTH4_FACE_EDGE_WITNESS_MATERIALIZATION__ZERO_CREDIT`;
- `PASS_PRODUCER_ROUND279__FORMAL_ZERO_CREDIT_FREEZE`;
- `PASS_INDEPENDENT_ROUND279`.
