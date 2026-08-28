# CM2 Round202 cold replay

Date: 2026-07-26  
Verdict: `PASS`

## Environment

- interpreter: `.venv-neurips/bin/python`;
- Python: 3.12.3;
- python-flint: 0.9.0;
- effective Arb precision: 384 bits;
- bytecode writes disabled with `PYTHONDONTWRITEBYTECODE=1` and `-B`.

The workspace system `python3` does not provide the frozen numerical
environment; the project virtual environment is required.

## Frozen identities

- producer:
  `630f0e9177807499eda3a75de368d1fff3c8c3454532558703d08f0f80d33786`;
- certificate file:
  `d33bf83615b3e5917c02e42e71e5f0cbb8da8eebd2a0b52af38042e1793cfe1c`;
- certificate result:
  `fe90ce27e02d3cb9a2a20bd0b1eb60572396eef742c41637cda7f00ef512a183`;
- certificate byte count: `13,436,333`;
- verifier:
  `bee71997bfb2a04cac3deb200f83e04e4c526d5a903e6442b3cb2e0816f04dd0`;
- verification file:
  `8b53ce1c990466d522e844fb2aab89629334d132a3817207fa8b2b0aef7fae71`;
- verification result:
  `5b02b9a36485c0f97ffbd961c768bb7a673caff0de867010fb3b4b68a736ead6`.

## Producer replay

From the workspace root, the additional producer replay used:

```text
PYTHONDONTWRITEBYTECODE=1 PYTHONHASHSEED=202052 \
  /usr/bin/time -v .venv-neurips/bin/python -B \
  deliverables/cm2_round202_h2_factor_t_face_c0_absence.py \
  --output deliverables/.cm2_round202_seed202052_certificate.json
```

The replay exited zero and printed certificate-result SHA256
`fe90ce27e02d3cb9a2a20bd0b1eb60572396eef742c41637cda7f00ef512a183`.
`cmp` against the official certificate returned zero.  Both files had
SHA256
`d33bf83615b3e5917c02e42e71e5f0cbb8da8eebd2a0b52af38042e1793cfe1c`.

- elapsed: `0:43.00`;
- user time: `41.44 s`;
- system time: `1.46 s`;
- maximum RSS: `660,940 kB`;
- exit status: `0`.

## Verifier replay

The official verification used seed `202061`.  The required additional
verifier replay used:

```text
PYTHONDONTWRITEBYTECODE=1 PYTHONHASHSEED=202062 \
  /usr/bin/time -v .venv-neurips/bin/python -B \
  deliverables/cm2_round202_h2_factor_t_face_c0_absence_verifier.py \
  --output deliverables/.cm2_round202_seed202062_verification.json
```

The replay exited zero and printed verification-result SHA256
`5b02b9a36485c0f97ffbd961c768bb7a673caff0de867010fb3b4b68a736ead6`.
`cmp` against the official verification returned zero.  Both files had
SHA256
`8b53ce1c990466d522e844fb2aab89629334d132a3817207fa8b2b0aef7fae71`.
The independently rebuilt certificate result remained
`fe90ce27e02d3cb9a2a20bd0b1eb60572396eef742c41637cda7f00ef512a183`.

Official seed-202061 verification:

- elapsed: `2:04.14`;
- user time: `122.16 s`;
- system time: `1.94 s`;
- maximum RSS: `711,604 kB`;
- exit status: `0`.

Additional seed-202062 replay:

- elapsed: `2:06.17`;
- user time: `124.18 s`;
- system time: `1.93 s`;
- maximum RSS: `711,948 kB`;
- exit status: `0`.

Both runs preserved:

- status `PASS`;
- full expected-result canonical equality;
- 592 independently rebuilt selected/evidence/local rows;
- 1,568 independently rebuilt terminal centered-C0 cells;
- 52/52 re-signed semantic attacks rejected;
- 13/13 strict JSON and encoding attacks rejected;
- 18/18 filesystem, path, alias, type, and output attacks rejected;
- no Round202 producer import or execution;
- complete pre/post pins of the Round185 six-file package and manifest.

The hidden replay files are not formal manifest members.  They may be
removed only after their hashes, byte comparisons, result digests, timings,
and memory use have been recorded.

## State invariant

Cold replay creates no promotion:

- `D02 = BLOCKED`;
- Gate5 remains `10/18`;
- complete global 18-field blocks remain `0`;
- `CM2 = NO-GO_FOR_CLAIM`.
