# CM2 Round119 cold replay

Date: 2026-07-23

## Frozen code

```text
producer c384d1e3b67d4560e34de542637317e6ce9f84dcaa4b12f3fd8030ce646fc057
verifier 9749f5e15e0106f0a07c963e69bfaad75e65fc192a120c36d237687623d41ace
```

The verifier was not changed between the two independent full replays or the
canonical materialization.

## Producer replays

The canonical certificate was generated at 768 bits.  An independent
eight-worker replay and a second eight-worker replay under

```text
PYTHONHASHSEED=119731
LC_ALL=C
TZ=UTC
```

produced:

```text
9ff985c91472e0ef57ced9fc10dbb6b2aa9e9627a5ac94c999caeefeca29a749  canonical certificate
9ff985c91472e0ef57ced9fc10dbb6b2aa9e9627a5ac94c999caeefeca29a749  /tmp/cm2-round119-workers8-qmin.json
9ff985c91472e0ef57ced9fc10dbb6b2aa9e9627a5ac94c999caeefeca29a749  /tmp/cm2-round119-workers8-seeded-c.json
```

Both byte comparisons against the canonical certificate pass.  All three
documents also carry the same result digest:

```text
f984a23b741a899b4d07bdcfc46a83faf9e9d42b619e12bb6d956cbf188a0247
```

The deterministic output contains sorted ray rows and no worker-scheduling
state.

## Independent verifier replays

Two separate full eight-worker runs of the stable 1024-bit verifier wrote to
different temporary paths:

```text
PYTHONPATH=deliverables .venv-neurips/bin/python \
  deliverables/cm2_round119_rank3_eight_grazing_trace_extended_cylinder_reach_verifier.py \
  --workers 8 \
  --certificate deliverables/cm2-round119-rank3-eight-grazing-trace-extended-cylinder-reach-2026-07-23.json \
  --output /tmp/r119-verification-workers8.json

PYTHONPATH=deliverables .venv-neurips/bin/python \
  deliverables/cm2_round119_rank3_eight_grazing_trace_extended_cylinder_reach_verifier.py \
  --workers 8 \
  --certificate deliverables/cm2-round119-rank3-eight-grazing-trace-extended-cylinder-reach-2026-07-23.json \
  --output /tmp/cm2-round119-verification-workers8.json
```

Observed wall times were `123.26 s` and `120.07 s`.  Both runs passed and
produced the same bytes:

```text
c86d3694cd90c19c98f08965f0492f9f0ae41ed5f8fc272d393c9f64d1060cde  /tmp/r119-verification-workers8.json
c86d3694cd90c19c98f08965f0492f9f0ae41ed5f8fc272d393c9f64d1060cde  /tmp/cm2-round119-verification-workers8.json
```

A third direct canonical run took `123.82 s`.  The resulting canonical
verification is strict-JSON parseable and byte-identical to both temporary
outputs:

```text
c86d3694cd90c19c98f08965f0492f9f0ae41ed5f8fc272d393c9f64d1060cde  deliverables/cm2-round119-rank3-eight-grazing-trace-extended-cylinder-reach-verification-2026-07-23.json
```

Its result digest is:

```text
31e2c1e5c0f8be6954265e1912759fa946711391a5baf534d31c5f2fefab82fb
```

## Replay census

Each full verifier replay reports:

```text
verdict                                      PASS
verification precision                      1024 bits
independently replayed traces                8
independently replayed base leaves           29992
independently replayed root leaves           7168
endpoint/interior cases                      8
endpoint/endpoint cases                      8
periodic-lift cases                          8
base/root overlaps                           8
selected join depth on every ray             1
selected join factor on every ray            2
selected refined join cells per ray          1024
total selected refined join cells            8192
failed selected refinements                   0
static semantic mutations rejected           57
bounded replay-dominance mutations rejected  12
total semantic mutations rejected            69
strict-JSON attacks rejected                 15
```

The replay-dominance harness additionally evaluates ray 0 at the complete
bounded ladder:

```text
depth 1  factor 2  1024 cells
depth 2  factor 4  2048 cells
depth 3  factor 8  4096 cells
```

All twelve re-signed lower-inflation/upper-deflation mutants fail at every
permitted depth.  The ladder covers `7168` refined intervals in total.

## Final comparison

```text
producer replay A == producer replay B == canonical certificate
verifier replay A == verifier replay B == canonical verification
```

Every comparison is byte-for-byte, not merely a comparison of verdicts or
rounded numerical summaries.
