# Round180 cold replay

Date: 2026-07-26

## Frozen artifacts

The fail-closed producer source has SHA256:

```
0ddb815a036a6e351929c484a00a565ce8969286bb137977ee9470577d807955
```

The canonical producer run used `PYTHONHASHSEED=18021`.  A second producer run
used `PYTHONHASHSEED=18022` and wrote to an authorized hidden certificate
path.  Both runs emitted result digest:

```
b2d30aade1e60c3b8d1e5943a240bafc8c8a28e35e67c882026b94246dafae3b
```

Both certificate files were byte-identical with SHA256:

```
46c6f1b2e86f9aa70d9126b28febbf97a81d6a4ac8f610dc2bb82d032a1abb70
```

The independent verifier source has SHA256:

```
12e25ebe0bae92cd8bda5cc3c00c7c3c94dda01ded5042c6e7a09152f840d6a4
```

The canonical verifier run used `PYTHONHASHSEED=18031`.  A second verifier run
used `PYTHONHASHSEED=18032` and wrote to a hidden verification path.  Both runs
emitted result digest:

```
87b908b0549af255dd20fef31e3b6fbf6205860641d4ebbcf332f30271c9b1ce
```

Both verification files were byte-identical with SHA256:

```
fb1b71c3006fcf4a10ee79d324346e2065ff2002252b28a29bd5085cab7e4caf
```

A separate parent replay under `PYTHONHASHSEED=180051` completed in
15 minutes 27.95 seconds with maximum RSS 157,836 KB.  Its hidden verification
was byte-identical to the canonical and seed-18032 files, with the same file
and result digests above.

## Commands

```bash
PYTHONDONTWRITEBYTECODE=1 PYTHONHASHSEED=18021 \
  .venv-neurips/bin/python -B \
  deliverables/cm2_round180_full_multi_residual_dimension_safe_partial.py

PYTHONDONTWRITEBYTECODE=1 PYTHONHASHSEED=18022 \
  .venv-neurips/bin/python -B \
  deliverables/cm2_round180_full_multi_residual_dimension_safe_partial.py \
  --output deliverables/.cm2_round180_seed18022_certificate.json

PYTHONDONTWRITEBYTECODE=1 PYTHONHASHSEED=18031 \
  .venv-neurips/bin/python -B \
  deliverables/cm2_round180_full_multi_residual_dimension_safe_partial_verifier.py

PYTHONDONTWRITEBYTECODE=1 PYTHONHASHSEED=18032 \
  .venv-neurips/bin/python -B \
  deliverables/cm2_round180_full_multi_residual_dimension_safe_partial_verifier.py \
  --output deliverables/.cm2_round180_seed18032_verification.json
```

The temporary replay files were removed after byte comparison.  The obsolete
pre-output-guard producer and certificate hashes are not part of this replay
or manifest.
