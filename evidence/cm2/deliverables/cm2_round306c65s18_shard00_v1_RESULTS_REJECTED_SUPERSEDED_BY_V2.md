# C65s18 shard 00 v1 result rejection and v2 supersession

Status: `REJECTED_FROM_FINAL_AUTHORITY_CHAIN`

The two v1 result files are retained only as immutable historical evidence:

- cold verification file SHA-256: `65fb7e85c63ed8cc04e5f10395a247dc56f2e2f8add6dc576dbc68c25d214ecb`
- cold verification object SHA-256: `fb6585fd9900b6661429c27cddc075ab4e69d05550419a3f5cf4d2e915023551`
- self-test file SHA-256: `a66a9caef2ad92b7a310b3a38daad894400beead672af62386b782f81c90cfaf`
- self-test object SHA-256: `622ef0623be52138d3b6168966f6fb72430fe20dceef7763fa4574bff21331fc`

Although both files individually report PASS, they were emitted on opposite
sides of a self-test-only exception-class correction: malformed trailing JSON
raises `ValueError`, while the first harness revision caught only the local
`Rejected` exception.  Consequently there is no single frozen v1 verifier
source that precedes both outputs.  Neither v1 result may be cited, aggregated,
promoted, or used for credit.

The correction does not alter the numeric cold-replay path.  Nevertheless, the
strict replacement is a fresh v2 source frozen before either v2 result is run:

- v2 verifier source SHA-256:
  `0468e3533d02366c4241249b3d87d99801c2c31a094d77ec3b566ab6166a45b5`

Only the v2 verifier, v2 verification, and v2 self-test may enter the final
shard-00 audit manifest.  This marker itself may enter that manifest so the
rejected history remains explicit.

All v1 and v2 audit artifacts are zero-credit development evidence.  No runtime
authority, canonical pointer, or seal was written.
