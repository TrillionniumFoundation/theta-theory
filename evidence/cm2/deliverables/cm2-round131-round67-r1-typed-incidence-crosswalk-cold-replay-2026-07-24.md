# CM2 Round 131 — cold replay

Date: 2026-07-24

Two clean verifier replays were run with:

- `PYTHONHASHSEED=131071`
- `PYTHONHASHSEED=131129`
- `LC_ALL=C`
- `TZ=UTC`
- `PYTHONDONTWRITEBYTECODE=1`

Both commands used:

```bash
python3 deliverables/cm2_round131_round67_r1_typed_incidence_crosswalk_verifier.py \
  --certificate deliverables/cm2-round131-round67-r1-typed-incidence-crosswalk-2026-07-24.json \
  --output /tmp/round131-verification.json
```

Both returned exit code 0 and `PASS`.  Their verification artifacts were
byte-for-byte identical.

Frozen hashes:

- producer: `8e7b2bae965be128a288ae38768bf746f5c33c0744449f8edea48014bd22d611`
- certificate: `a8e4b9dabb30396469f28d4df252c9f5de1d9d1620c0a18d252ef23a12f1f3d6`
- certificate result: `0fd7f419d5a0afa3fbc20db3757803ee5c2982b4428ba52a97798a6fcc28a0ab`
- verifier: `162754843be2073ad100d238a1ba54e4aaa82db4615a376b0468e5a450563801`
- verification: `d42bbc753df55fa94e4471e92a0e2f0abf13279cec1c17526a06e146d29df5e6`
- verification result: `152383956dc6300a5af089229a6868456c695989f6594bde1978c8aaf7c7a529`

Negative tests returned nonzero and did not create or overwrite a result:

- missing certificate;
- byte-tampered certificate;
- certificate symlink;
- certificate hardlink;
- output symlink;
- output hardlink;
- output FIFO;
- protected upstream output target;
- custom valid certificate used simultaneously as `--certificate` and
  `--output`.

The custom-certificate alias test preserves the input certificate hash.
