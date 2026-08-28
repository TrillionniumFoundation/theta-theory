# CM2 Round183 cold replay

Date: 2026-07-26  
Python environment: `../.venv-neurips/bin/python`  
Effective Arb precision: 384 bits  
python-flint: 0.9.0

## Frozen inputs

- Round183 producer SHA256:
  `ac0e786146df08e1c8695bd9a1cfdbe0bed290d2fd77960f61ffa9e0785133ed`
- Round181 producer, certificate, verifier, verification, and manifest:
  exact pins embedded in both Round183 programs.

## Producer replay

The official certificate was generated with `PYTHONHASHSEED=1`.  A clean
replay used:

```text
PYTHONHASHSEED=987 ../.venv-neurips/bin/python \
  cm2_round183_residual_face_bracket_refinement.py \
  --output .cm2_round183_seed987_certificate.tmp.json
```

`cmp` returned zero.  Both files have SHA256:

`5863d5e7e564d3f6c145cbb2a2e7286f495fce73a40bdc8e11a47f20fd4ff74b`.

Their common result digest is:

`f37eb4f1321ef837a2d67dbfaf7d3816dc320b81d31e151422eb9b649d5a5f53`.

## Verifier replay

The official verification was generated with `PYTHONHASHSEED=1`.  A clean
replay used:

```text
PYTHONHASHSEED=987 ../.venv-neurips/bin/python \
  cm2_round183_residual_face_bracket_refinement_verifier.py \
  --output .cm2_round183_seed987_verification.tmp.json
```

`cmp` returned zero.  Both files have SHA256:

`58f5dacbab0e63185f04f63ad4fa87bf99ae12bab94da59810ad71da44773801`.

Their common verification-result digest is:

`40beacf08c2168f602c683b1e3b49d91411e90da3dc04ea42e27d95e922cbcf7`.

Both runs report `PASS`, full independently rebuilt canonical equality,
28/28 re-signed semantic attacks rejected, 9/9 strict JSON attacks rejected,
and 11/11 path attacks rejected.

## Independent parent replay

A separate parent audit used `PYTHONHASHSEED=183051` and independently
reported `cmp=0` against the official verification, the same verification
file SHA256, and the same verification-result digest.

The seed-987 temporary outputs were removed after these byte comparisons.

