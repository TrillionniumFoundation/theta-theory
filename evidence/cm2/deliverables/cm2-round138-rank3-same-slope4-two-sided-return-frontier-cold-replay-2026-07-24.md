# CM2 Round 138 — cold replay

Date: 2026-07-24

Each verifier invocation independently rebuilds the complete Round138 result
at both 12288 and 16384 Arb precision.

```bash
env PYTHONHASHSEED=138001 LC_ALL=C TZ=UTC PYTHONDONTWRITEBYTECODE=1 \
  PYTHONPATH=deliverables \
  .venv-neurips/bin/python \
  deliverables/cm2_round138_rank3_same_slope4_two_sided_return_frontier_verifier.py \
  --certificate \
  deliverables/cm2-round138-rank3-same-slope4-two-sided-return-frontier-2026-07-24.json \
  --output /tmp/cm2-r138-final-seed-A.json

env PYTHONHASHSEED=987654321 LC_ALL=C TZ=UTC PYTHONDONTWRITEBYTECODE=1 \
  PYTHONPATH=deliverables \
  .venv-neurips/bin/python \
  deliverables/cm2_round138_rank3_same_slope4_two_sided_return_frontier_verifier.py \
  --certificate \
  deliverables/cm2-round138-rank3-same-slope4-two-sided-return-frontier-2026-07-24.json \
  --output /tmp/cm2-r138-final-seed-B.json
```

Both returned exit code 0 and `PASS`. Their artifacts were byte-for-byte
identical to each other and to the formal verification artifact.

Frozen hashes:

- producer:
  `42d749dccea86aa3a122707db0226def176e75047d5dcb4bf19826b50e09282b`;
- certificate:
  `c1f4d5041d810dd91d38e39bf795e5ab05536065ba8b0730530c58a91f7bf6d8`;
- certificate result:
  `a46f4122639ccb82eed2d06d916972020b81c4f566ccfb05a9644de382a2e123`;
- verifier:
  `7dfb9068696c5c868c614114c72e7c5819270c84c2c2455ad98f5e4f5321f941`;
- verification:
  `1cd9878d03bde25bceb0dcf292d47783fe697de347ca653d1994b72a509015c3`;
- verification result:
  `8dcfcc8c68fbf10ced13982f4fa86f480596f4b5d23db3351cc6afdcd0b399bb`.

The independent replay reconstructs:

- the 4096-step fixed-`p` D=0 root;
- the 4104-bit directed dyadic `b_star` enclosure;
- both 2048-step signed side roots and the positive along-leaf derivative;
- both unique `2^-4096` dyadic `p` centers;
- two exact leaf graphs inside positive-area `2^-2400` half-width squares;
- all 298 BYPASS and 349 HIT collision rows;
- all retained 55/57-candidate and full 161-candidate searches;
- every translation-normalized official word;
- every homogeneity label and incidence rank;
- 645 strict preterminal nonreturns and two strict terminal C24 returns;
- the primitive-free Round132 typed candidate and the global `j=3` timeline;
- every zero count and nonpromotion boundary.

The verifier rejects all 81 re-signed semantic mutations, all 19 strict-JSON
attacks, and all 13 path-safety self-tests. The formal artifact is canonical
pretty JSON with a final newline and a matching outer result digest.

Process-level hostile I/O replay covers:

- missing, byte-tampered, symlink, hardlink, and FIFO certificate inputs;
- output targets aliasing the certificate, producer, verifier, and a pinned
  upstream;
- output symlink, hardlink, and FIFO targets.

All 12 hostile cases return exit code 1. No unexpected output is created.
Certificate, producer, verifier, and pinned-upstream hashes remain unchanged.

The replay preserves the strict boundary: the two word-cells remain local;
global Round35/component/short-cell/image-recut counts remain zero; no owner,
`t54`, `Omega_j`, or `q_j` is materialized; Gate5 remains `10/18` and
`NOT_CERTIFIED`; CM2 remains `NO-GO_FOR_CLAIM`.
