# CM2 Round 137 — cold replay

Date: 2026-07-24

The formal verifier and two clean replays used the frozen Python environment:

```bash
env PYTHONHASHSEED=137731 LC_ALL=C TZ=UTC PYTHONDONTWRITEBYTECODE=1 \
  .venv-neurips/bin/python \
  deliverables/cm2_round137_seed_independent_dyadic_basis_rank_contract_verifier.py \
  --certificate \
  deliverables/cm2-round137-seed-independent-dyadic-basis-rank-contract-2026-07-24.json \
  --output /tmp/cm2-r137-verification-A.json

env PYTHONHASHSEED=137947 LC_ALL=C TZ=UTC PYTHONDONTWRITEBYTECODE=1 \
  .venv-neurips/bin/python \
  deliverables/cm2_round137_seed_independent_dyadic_basis_rank_contract_verifier.py \
  --certificate \
  deliverables/cm2-round137-seed-independent-dyadic-basis-rank-contract-2026-07-24.json \
  --output /tmp/cm2-r137-verification-B.json
```

Both returned exit code 0 and `PASS`.  Their outputs are byte-for-byte
identical to each other and to the formal verification artifact.

Frozen hashes:

- producer:
  `81974ada469f8f24299d7790e16f6380f58b38df151ee67704695aa81c0d08ac`;
- certificate:
  `06918b7bbfdeed9bda41a1220a25b630df6eaaa5f06024757f25a8c9fe7b88bf`;
- certificate result:
  `7517e103dd2c22371892f1b9e560ac886a8bf4a8ad96604cab5d6702d1d8f804`;
- verifier:
  `8d359eb9d397d3c4375d2ae21cc752447f0fb9216d180b59b3517288914fba45`;
- verification:
  `53369532c293d9cb2830a362facef7e4c4040f826f5ddea70519fde9034a1a5c`;
- verification result:
  `00bb1d65f061ec93074ec36ac8fc5cce744ff8908735284ea036fcc8e8f73dca`.

The replay independently confirmed:

- 24 exact increasing affine normalization rows;
- normalization-row aggregate SHA256 `5a4d0cb4...febd1f`;
- the common-denominator primitive rule rather than a per-axis rule;
- exact `I_m` counts and zero-based offsets;
- exhaustive 2D/1D counts `11025/105`;
- three large 2D and three large 1D rank/unrank fixtures;
- Round136 contained-witness minimal level `3809`;
- upper-bound rank bit length `15234` and decimal length `4586`;
- decimal SHA256 `c6f57973...a99fd4b`;
- all historical identifiers, owner fields, q_j fields, and global upgrades
  remaining null, false, or zero.

Negative CLI replay used a missing certificate and a byte-tampered copy.  Both
returned exit code 1, produced no output, and reported a fail-closed
verification error.

Hostile path replay covered:

- producer, verifier, formal certificate, selected certificate, and every
  byte-pinned upstream as output aliases;
- input and output symlinks, hardlinks, and FIFOs;
- output-directory and symlink-parent targets;
- a byte-tampered certificate.

Every hostile case failed closed.  All protected inputs and victim files were
unchanged.  The valid artifact is canonical pretty JSON with a final newline;
its outer result digest recomputes exactly.

The strict boundary remains unchanged: the v1 witness rank is only an upper
bound, no historical component/restriction ID is minted, Gate5 remains
`10/18` and `NOT_CERTIFIED`, and CM2 remains `NO-GO_FOR_CLAIM`.
