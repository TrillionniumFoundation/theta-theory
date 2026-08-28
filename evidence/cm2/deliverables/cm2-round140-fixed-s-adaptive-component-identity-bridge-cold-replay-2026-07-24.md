# CM2 Round 140 fixed-s adaptive identity bridge — cold replay

Date: 2026-07-24

The producer and independent verifier were replayed under two clean hash
seeds.  The verifier reads the selected frozen certificate; it neither imports
nor executes the Round140 producer or the Round139 producer.

```bash
env PYTHONHASHSEED=140001 LC_ALL=C TZ=UTC PYTHONDONTWRITEBYTECODE=1 \
  python \
  deliverables/cm2_round140_fixed_s_adaptive_component_identity_bridge.py \
  --output /tmp/cm2-r140-bridge-cert-A.json

env PYTHONHASHSEED=987654321 LC_ALL=C TZ=UTC PYTHONDONTWRITEBYTECODE=1 \
  python \
  deliverables/cm2_round140_fixed_s_adaptive_component_identity_bridge.py \
  --output /tmp/cm2-r140-bridge-cert-B.json

env PYTHONHASHSEED=140001 LC_ALL=C TZ=UTC PYTHONDONTWRITEBYTECODE=1 \
  python \
  deliverables/cm2_round140_fixed_s_adaptive_component_identity_bridge_verifier.py \
  --certificate /tmp/cm2-r140-bridge-cert-A.json \
  --output /tmp/cm2-r140-bridge-verify-A.json

env PYTHONHASHSEED=987654321 LC_ALL=C TZ=UTC PYTHONDONTWRITEBYTECODE=1 \
  python \
  deliverables/cm2_round140_fixed_s_adaptive_component_identity_bridge_verifier.py \
  --certificate /tmp/cm2-r140-bridge-cert-B.json \
  --output /tmp/cm2-r140-bridge-verify-B.json
```

All four commands returned exit code 0.  The two certificates are
byte-for-byte identical to each other and to the formal certificate.  The two
verification artifacts are byte-for-byte identical to each other and to the
formal verification artifact.

Frozen upstream anchor:

- final Round139 producer:
  `462ffcb41ba24771ce655ddb3ad5f18d5a22c8d0cb443ec1791ea9272d3d512b`;
- final Round139 certificate:
  `64e91e6b1efcb2675982fbc453b08349b003c8be5b4d236f61e1392aaee045f0`;
- final Round139 certificate result:
  `6e8f54c34154ea5ba3c95d4e901bc643c020a0a42e180241ae9053bb24f42236`.

Frozen Round140 bridge hashes:

- producer:
  `838d5ffbedd88856df561f5b6343d63466d03cab89189b3bc4eb4838f65ad4e2`;
- certificate:
  `e3f08525e770829c3ce71fed872a18dbfdc3139f514c3f865d12f6abc114a353`;
- certificate result:
  `60a364ec21cc1bedf83f7287a7e8f4e9a90a2be431d04cec8fed3f9c0102496b`;
- verifier:
  `4f2c18fb476fe9754009ea7f5bba737fa95084a3e81e2b70e0043203ac774680`;
- verification:
  `75500f473e1932151bc643109187e99e88033c3b9457b584ecb1df4c0860b611`;
- verification result:
  `c9b36397f28a63f5408fc82ee474617fe54e73774382c607dc10bc3e9b6dd746`.

The independent replay reconstructs from the pinned current Round139 result:

- all 1,648 closed collision rows and their exact ordered official-word IDs;
- official-word sequence digest
  `f504289edce554d47e17a90d7c886586a69f3ec4b64fafd90c718c50ca93221e`;
- exact Round27-compatible tuple digest
  `5cec1061ec331e8f37929dfb1b2b2a78757309ba60198d571abd9e8cf6c70ed9`;
- deterministic adaptive path-cell ID
  `round140-fixed-s0-adaptive-path-cell:a4a3be3cf7115abec08f372382ca7a863838e963a7d03af400d6a6ca58812b6a`;
- the Round137-v1 normalization and first contained consecutive-grid box at
  denominator power 5883;
- its 23,530-bit, 7,084-decimal-digit primitive v1 basis rank, whose decimal
  SHA256 is
  `81ee4f795045d8478e621dbcaf2cba2437ccb168b34b770f995c012c0060927f`;
- upper-bound locator
  `round140-containing-component-upper-bound-locator:7f62e720961a65aa52b737f9cb19a1df1d6f55d44aa89ef0a6f7b13c3fee12ac`;
- witness-relative containing-component locator
  `round140-unique-containing-maximal-component-locator:028dd77208582e33185707e1ea1ca31988e3cf4f698674fb8a0f791981dce90b`.

The formal verifier rejects all 62 re-signed semantic mutations, all 18
strict-JSON attacks, and all 20 in-process path-safety attacks.  Separate
process-level replay rejected five hostile certificate inputs and seven
hostile output targets with exit code 1.  No rejected case created an
unexpected regular output, and all protected hashes remained unchanged.

The replay preserves the strict boundary.  The adaptive cell is not the
maximal Round27 path component; rank zero is only its local one-cell-registry
rank; the contained Round137-v1 rank is only an upper bound; the
witness-relative locator is not a historical canonical ID.  No Round35
restriction, historical least rank, Round50 owner, Round54 token, Round67
record, or complete Gate5 block is created.
