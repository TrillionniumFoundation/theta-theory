# CM2 Round 135 — cold replay

Date: 2026-07-24

The formal verifier and two clean cold replays used the Python environment
containing `python-flint`:

```bash
env PYTHONHASHSEED=1 LC_ALL=C TZ=UTC PYTHONDONTWRITEBYTECODE=1 \
  .venv-neurips/bin/python \
  deliverables/cm2_round135_rank3_wide_positive_borel_local_robustness_verifier.py \
  --certificate \
  deliverables/cm2-round135-rank3-wide-positive-borel-local-robustness-2026-07-24.json \
  --output /tmp/cm2-r135-seed1.json

env PYTHONHASHSEED=987654321 LC_ALL=C TZ=UTC PYTHONDONTWRITEBYTECODE=1 \
  .venv-neurips/bin/python \
  deliverables/cm2_round135_rank3_wide_positive_borel_local_robustness_verifier.py \
  --certificate \
  deliverables/cm2-round135-rank3-wide-positive-borel-local-robustness-2026-07-24.json \
  --output /tmp/cm2-r135-seed2.json
```

Both returned exit code 0 and `PASS`. Their artifacts were byte-for-byte
identical to each other and to the formal verification artifact.

Frozen hashes:

- producer:
  `87ea759a966be5ea9762c075c9e3e8e218b0e76c74c0775f610259f8bf1fa99d`;
- certificate:
  `31b4b017ac7da341b210d28dc2296ba2499d425615f2c3bce750ccec586f67df`;
- certificate result:
  `7b221b87de96a9386f952aa1dab83c49d34c08cc4bae56ec2af302ffc6b50272`;
- verifier:
  `ca0cf023e761be7e654dcb6d50d87898301b912a105df14e2f92eec4dabd53dd`;
- verification:
  `caaebfdaa85c95d269af32c044de00c313355ddb501570e3bfbe4871231235e7`;
- verification result:
  `82c2795da41b8a44b52d4e0a3b958857784f70a8f6e5f984924016a630944ff5`.

The replay independently reconstructed:

- the `2^-17` closed collar and the exact `2^-16` boundary obstruction;
- five root-partition endpoints and the monotone full-collar root graph;
- 9 convergence rows and 192 normalized derivative-cell rows;
- all `V1/V2/V3` envelopes;
- 23 input and 192 stage-three recut roots;
- 24 common children, 215 merged cuts, and 216 output fragments;
- four complete physical subcollar audits and 16224 candidate checks;
- zero physical faces, zero residual faces, and physical `F10=0`;
- all 72 wide F17 guards;
- all 18 local field-transport templates;
- all 970 row hashes, 11 group hashes, and 970 unique primary IDs;
- the unchanged global nonpromotion state.

The verifier rejected all 59 re-signed semantic mutations and all 18
strict-JSON attacks. The formal artifact has a final newline, is canonical
pretty JSON, and its outer result digest independently recomputes to the
stored value.

Negative I/O replay covered:

- missing and byte-tampered certificates;
- certificate symlink, hardlink, and FIFO;
- output symlink, hardlink, and FIFO;
- certificate/output aliasing;
- a protected upstream used as the output target.

Every hostile case returned exit code 1. No unexpected output was created,
and all victim, certificate, and protected-upstream hashes were unchanged.

The replay preserves the strict boundary: finite rows are local family
templates, physical F10 is empty rather than positively paid, global complete
blocks remain zero, Gate5 remains `10/18` and `NOT_CERTIFIED`, and CM2 remains
`NO-GO_FOR_CLAIM`.

