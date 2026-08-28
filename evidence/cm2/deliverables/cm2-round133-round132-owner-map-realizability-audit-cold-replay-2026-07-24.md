# CM2 Round 133 — cold replay

Date: 2026-07-24

Two clean verifier replays were run with:

- `PYTHONHASHSEED=133071`
- `PYTHONHASHSEED=133129`
- `LC_ALL=C`
- `TZ=UTC`
- `PYTHONDONTWRITEBYTECODE=1`

Both used:

```bash
python3 \
  deliverables/cm2_round133_round132_owner_map_realizability_audit_verifier.py \
  --certificate \
  deliverables/cm2-round133-round132-owner-map-realizability-audit-2026-07-24.json \
  --output /tmp/round133-verification.json
```

Both returned exit code 0 and `PASS`.  Their verification artifacts were
byte-for-byte identical.

Frozen hashes:

- producer:
  `3607bf2a3b2498c13d4bab27113dd151577e050cb83e68535ee32aaadbd79722`
- certificate:
  `a020ce376c1398384e5f304aff320aa214721f5f8d8bcc1e35bfa31eadd54c91`
- certificate result:
  `0e8e446fc81b1432dac31a9e7fc407b74bd6948dbd72451c67ffc43034f05ed2`
- verifier:
  `189320a0593a2d83eec6c3b69e37c087080ff3896529dfded06d4845c22e93cd`
- verification:
  `f41a45baf3cffab63a3429b66c2f3c9473394024a4ae4c9a234df13e3410794f`
- verification result:
  `2446ee1c45f8a4ae70eb44a7c566ef43936e5b800f043a48ae7c0c1ba084eb4b`

The independent replay reconstructed 64 owner-candidate requests, 5 ordered
blockers and 17 replacement-contract rows.  All 86 row closures, all three
aggregate digests and the outer result digest matched.

The verifier rejected 90 re-signed semantic mutations and 19 strict-JSON
attacks.

Negative I/O tests returned nonzero and did not create or overwrite a result:

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

A byte-identical custom certificate at a different path passed when the
output path was distinct.  The same-path rejection preserved the custom
certificate hash.
