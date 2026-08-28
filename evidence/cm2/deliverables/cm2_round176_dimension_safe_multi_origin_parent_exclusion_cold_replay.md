# Round176 cold replay

Date: 2026-07-26

The canonical producer run used `PYTHONHASHSEED=17611`.  A second producer run
used `PYTHONHASHSEED=17622` and wrote to a temporary certificate path.

Both producer runs emitted result digest:

```
3090fb2f58fff50f0c9ab89b7a228042f49d5d929cd53e9c358e31a4d977254e
```

Both certificate files were byte-identical with SHA256:

```
bb255bf9dbf1c6cb6680ea32b57ad31c03f108a8af5c345a2f7ca3ab88a22fa8
```

The final canonical independent verifier run used `PYTHONHASHSEED=17631`.  A
second verifier run used `PYTHONHASHSEED=17632` and wrote to a temporary verification
path.

Both verifier runs emitted result digest:

```
b5057dcc0ff32ac6a8e619fb030ba1bf9ff1c975598ade79a282accaeac6f6f3
```

Both verification files were byte-identical with SHA256:

```
31ad065d06309b9f830c6135579672e50e4c84d6f2620419326c1cd682dd010e
```

Commands:

```bash
PYTHONDONTWRITEBYTECODE=1 PYTHONHASHSEED=17611 \
  .venv-neurips/bin/python -B \
  deliverables/cm2_round176_dimension_safe_multi_origin_parent_exclusion.py

PYTHONDONTWRITEBYTECODE=1 PYTHONHASHSEED=17622 \
  .venv-neurips/bin/python -B \
  deliverables/cm2_round176_dimension_safe_multi_origin_parent_exclusion.py \
  --output deliverables/.cm2_round176_seed17622_certificate.json

PYTHONDONTWRITEBYTECODE=1 PYTHONHASHSEED=17631 \
  .venv-neurips/bin/python -B \
  deliverables/cm2_round176_dimension_safe_multi_origin_parent_exclusion_verifier.py

PYTHONDONTWRITEBYTECODE=1 PYTHONHASHSEED=17632 \
  .venv-neurips/bin/python -B \
  deliverables/cm2_round176_dimension_safe_multi_origin_parent_exclusion_verifier.py \
  --output deliverables/.cm2_round176_seed17632_verification.json
```

The temporary replay files were removed after byte comparison.
