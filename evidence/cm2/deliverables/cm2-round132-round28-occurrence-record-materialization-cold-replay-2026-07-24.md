# CM2 Round 132 — cold replay

Date: 2026-07-24

Two clean independent-verifier replays were run with:

- `PYTHONHASHSEED=0`
- `PYTHONHASHSEED=987654321`
- `LC_ALL=C`
- `TZ=UTC`
- `PYTHONDONTWRITEBYTECODE=1`

Both commands used the project environment because the frozen source replay
requires `flint`:

```bash
.venv-neurips/bin/python \
  deliverables/cm2_round132_round28_occurrence_record_materialization_verifier.py \
  --certificate deliverables/cm2-round132-round28-occurrence-record-materialization-2026-07-24.json \
  --output /tmp/round132-verification.json
```

Both returned exit code 0 and `PASS`.  Their artifacts were byte-for-byte
identical and equal to the formal verification artifact.

Frozen hashes:

- producer: `88a12779148a49f111380c0560b0cb490a4e87f00d7ba7671878eec858f87d53`
- certificate: `b5d09c7398dae4b77a6f011430286f88539e0f13ca449e50eb84fc3712d67d31`
- certificate result: `3a5b4450d838ac39e0e7f596344589b520a8060bb0131bd88fb8f2c77af4d624`
- verifier: `94e1839d9a186ec906f4c6bfc7d69b548a68f4dc050a29d839d87df14f9af4b3`
- verification: `26ef83ceb2aa484388e99a4f832670c7e13429452aec7a56945d2db4cb97f171`
- verification result: `3fbe43363f627c79f980c34998178feb2dab2278cc50e206f12539699a84e336`

The verifier rejects 58 independently re-signed semantic mutations and 18
strict-JSON attacks.

Negative tests returned nonzero and created no output or preserved the target
hash:

- missing certificate;
- wrong-byte certificate;
- certificate symlink;
- certificate hardlink;
- output symlink;
- output hardlink;
- output FIFO;
- fixed certificate used as the output target;
- a copied valid certificate used simultaneously as `--certificate` and
  `--output`;
- a protected Round28 upstream used as the output target.

The copied certificate, fixed certificate and protected upstream retained
their original byte hashes after the alias tests.
