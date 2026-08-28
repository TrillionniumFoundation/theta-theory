# Round295-B cold replay

Run from the workspace root.  The replay uses no caches and fixes
`PYTHONHASHSEED`; neither program writes bytecode.

```bash
python3 -B -m py_compile \
  deliverables/cm2_round295b_source_g_r289_terminal_face_absence_closure.py \
  deliverables/cm2_round295b_source_g_r289_terminal_face_absence_closure_verifier.py

gzip -t \
  deliverables/cm2_round295b_source_g_r289_terminal_face_absence_closure_ledger.json.gz

(cd deliverables && sha256sum -c \
  cm2_round295b_source_g_r289_terminal_face_absence_closure_manifest.sha256)

env PYTHONDONTWRITEBYTECODE=1 PYTHONHASHSEED=295201 \
  python3 -B \
  deliverables/cm2_round295b_source_g_r289_terminal_face_absence_closure.py

env PYTHONDONTWRITEBYTECODE=1 PYTHONHASHSEED=295271 \
  python3 -B \
  deliverables/cm2_round295b_source_g_r289_terminal_face_absence_closure_verifier.py \
  --output /tmp/cm2_round295b_seed_295271.json

env PYTHONDONTWRITEBYTECODE=1 PYTHONHASHSEED=295929 \
  python3 -B \
  deliverables/cm2_round295b_source_g_r289_terminal_face_absence_closure_verifier.py \
  --output /tmp/cm2_round295b_seed_295929.json

cmp /tmp/cm2_round295b_seed_295271.json \
  /tmp/cm2_round295b_seed_295929.json
```

Observed deterministic seals:

```text
producer             c970371a5e05a76d22cd41accf98848784413f9ce2c937a3dff47c43b763b86a
ledger               1714945c470607a68c9fb5e323319899faabd187ecbccd00d266ea6f9361007c
result file          b10c5caf9813887b06f2ed49796e02befc8abdc048e6909c2146bfc120e6334a
result embedded      278036958403818507e96c72bbc94cfa0cbbe50a6f0984aecb64125795974536
verifier             648ce97bba19272f2dc26f268d40c12a2dd686ade6a32d273b0b8b371707eaa8
verification file    f823fd7c7a34d39163bc887d6544ea670915e9ecb93fc2a94947f4ee777180a1
verification embedded 471e44c13d9c6594c2182185ae5e269746ded6184a6f0d802f629e8287039063
```

Observed first producer run: about 53 seconds, peak RSS about 2.87 GiB.
Observed verifier runs: about 69–71 seconds each, peak RSS about 2.88 GiB.
Both verifier seeds rejected all 53 attacks and emitted byte-identical JSON.

