# CM2 Round 136 — cold replay

Date: 2026-07-24

The formal verification and two clean cold replays used the environment
containing `python-flint`. Every invocation performs both the 8192-bit
primary reconstruction and the 12288-bit semantic consistency replay.

```bash
env PYTHONHASHSEED=136001 LC_ALL=C TZ=UTC PYTHONDONTWRITEBYTECODE=1 \
  PYTHONPATH=deliverables \
  .venv-neurips/bin/python \
  deliverables/cm2_round136_rank3_positive_width_r1056_return_frontier_verifier.py \
  --certificate \
  deliverables/cm2-round136-rank3-positive-width-r1056-return-frontier-2026-07-24.json \
  --output /tmp/cm2-r136-final-seed-A.json

env PYTHONHASHSEED=987654321 LC_ALL=C TZ=UTC PYTHONDONTWRITEBYTECODE=1 \
  PYTHONPATH=deliverables \
  .venv-neurips/bin/python \
  deliverables/cm2_round136_rank3_positive_width_r1056_return_frontier_verifier.py \
  --certificate \
  deliverables/cm2-round136-rank3-positive-width-r1056-return-frontier-2026-07-24.json \
  --output /tmp/cm2-r136-final-seed-B.json
```

Both returned exit code 0 and `PASS`. The two artifacts were byte-for-byte
identical to each other and to the formal verification artifact.

Frozen hashes:

- producer:
  `4e78309d5275bf367e6df03509c40ebaaac6f344c7948446a25b3b508c8c2bc2`;
- certificate:
  `d9b7b7823dddce2dcbc16412294c8ecef42b304712d4bb968896d2221b8aa7f9`;
- certificate result:
  `407bc2dbecaacb2ed8527a3fe8a41f97ed523a43f428c37b76e14639425cf545`;
- verifier:
  `597778df1deefa34b690c4ed665fcb1f8df965aa45d9a7c03093a0e632cf23ad`;
- verification:
  `501035c235124e1c1a57fa198ee63e4f90c7a729497b600c31b2212e5260964c`;
- verification result:
  `a59b1ef17ba18862663f8f77cfde99a6db9cccf5dbf93d96ed4b6d6cea4d4bdc`.

The replay independently reconstructed:

- the 1500-step rational locator and the `2^-3815` source half-width;
- exact positive source area `2^-7628`;
- all 1056 complete retained-candidate owner searches;
- all translation-normalized official registry words;
- 1055 strict preterminal C24 exclusions and the strict terminal landing;
- 1055 central homogeneity labels and the one `H4294967295` tail label;
- every capped reciprocal-cosine incidence rank;
- all 17 strict-margin ledgers;
- 1056 row hashes, the row-group hash, and the 125-key unique census;
- the typed Round132 occurrence singleton and every nonpromotion field.

The verifier rejected all 70 re-signed semantic mutations, all 19
strict-JSON attacks, and all 13 in-process path-safety attacks. The formal
artifact has a final newline, canonical pretty JSON, and a matching outer
result digest.

Process-level hostile I/O replay covered:

- missing, byte-tampered, symlink, hardlink, and FIFO certificate inputs;
- output targets aliasing the certificate, producer, verifier, and a pinned
  upstream;
- output symlink, hardlink, and FIFO targets.

All 12 hostile cases returned exit code 1. No unexpected output was created.
The certificate, producer, verifier, and pinned-upstream hashes were unchanged
before and after the replay.

The strict boundary is preserved: the local R1056 cylinder is not a canonical
global component or owner fibre; global complete blocks remain zero; Gate5
remains `10/18` and `NOT_CERTIFIED`; CM2 remains `NO-GO_FOR_CLAIM`.
