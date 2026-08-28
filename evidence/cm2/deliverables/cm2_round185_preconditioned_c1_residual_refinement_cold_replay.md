# CM2 Round185 cold replay

Date: 2026-07-26  
Verdict: `PASS`

## Environment

- interpreter: `.venv-neurips/bin/python`
- Python: 3.12.3
- python-flint: 0.9.0
- effective Arb precision: 384 bits
- bytecode writes disabled: `PYTHONDONTWRITEBYTECODE=1` and `-B`

The workspace system `python3` has no importable `flint`; the pinned virtual
environment above is required.

## Frozen artifact identities

- producer:
  `7b48f3ee3417fcfdf5ef6c852e0ab591eb849b357e704e46ee3aaa259d20acc2`
- certificate file:
  `2034e939a6046cd36f749546ab8dc2c0a004b3325c803b5335a3f5e34831fff1`
- certificate result:
  `ae5af298b9d19b99863af600dca7f73fad4ff76f9db661ccfdf9b0e03afbeddf`
- certificate byte count: `106,100,901`
- verifier:
  `88d5b72c68ba216a1c807b868156c8e0da7e9e63db968eda5b5a66dd86d5651f`
- verification file:
  `bda1286ec582f17724b6478e3af98973280f482bf9192235f96842c55513642e`
- verification result:
  `b63c15eabc468192c113d7221c7adfd37fec94aa38f4b02c97acb25598962cf6`

## Producer replay

From the workspace root, the seed-185052 replay used:

```text
PYTHONDONTWRITEBYTECODE=1 PYTHONHASHSEED=185052 \
  /usr/bin/time -v .venv-neurips/bin/python -B \
  deliverables/cm2_round185_preconditioned_c1_residual_refinement.py \
  --output deliverables/.cm2_round185_seed185052_certificate.json
```

The replay exited zero.  `cmp` against the official certificate returned
zero, and both files had SHA256

`2034e939a6046cd36f749546ab8dc2c0a004b3325c803b5335a3f5e34831fff1`.

The replay retained the certificate-result digest

`ae5af298b9d19b99863af600dca7f73fad4ff76f9db661ccfdf9b0e03afbeddf`.

- elapsed: `16:47.02`
- maximum RSS: `724,948 kB`
- exit status: `0`

## Verifier replay

The seed-185062 verifier replay used:

```text
PYTHONDONTWRITEBYTECODE=1 PYTHONHASHSEED=185062 \
  /usr/bin/time -v .venv-neurips/bin/python -B \
  deliverables/cm2_round185_preconditioned_c1_residual_refinement_verifier.py \
  --output deliverables/.cm2_round185_seed185062_verification.json
```

The replay exited zero and returned `PASS`.  `cmp` against the official
verification returned zero, and both files had SHA256

`bda1286ec582f17724b6478e3af98973280f482bf9192235f96842c55513642e`.

The replay retained verification-result digest

`b63c15eabc468192c113d7221c7adfd37fec94aa38f4b02c97acb25598962cf6`

and independently rebuilt certificate-result digest

`ae5af298b9d19b99863af600dca7f73fad4ff76f9db661ccfdf9b0e03afbeddf`.

- elapsed: `23:43.65`
- user time: `1405.04 s`
- system time: `18.34 s`
- maximum RSS: `1,426,116 kB`
- exit status: `0`

The replay preserved the complete rejection matrix:

- re-signed semantic attacks: `32/32`;
- strict JSON attacks: `9/9`;
- path/type/output attacks: `11/11`;
- full expected-result canonical equality: true;
- Round185 producer imported or executed by the verifier: false.

The two hidden replay outputs were removed only after both byte comparisons,
hashes, result digests, timings, and maximum-RSS values were recorded.  They
are not manifest members.

## State invariant

Cold replay creates no promotion:

- `D02 = BLOCKED`;
- Gate5: `10/18`;
- complete global 18-field blocks: `0`;
- `CM2 = NO-GO_FOR_CLAIM`.
