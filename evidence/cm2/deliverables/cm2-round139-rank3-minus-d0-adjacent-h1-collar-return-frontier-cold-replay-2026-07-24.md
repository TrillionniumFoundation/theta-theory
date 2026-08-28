# CM2 Round 139 — cold replay

Date: 2026-07-24

The frozen Round139 producer was replayed at both contracted precisions, and
the independent verifier was invoked twice under distinct hash seeds. All
commands ran from

```text
/home/qian-qi/.openclaw/workspaces/telegram-bot-8449317572
```

## Producer replay

Primary:

```bash
env PYTHONHASHSEED=139001 LC_ALL=C TZ=UTC PYTHONDONTWRITEBYTECODE=1 \
  PYTHONPATH=deliverables \
  /usr/bin/time -v .venv-neurips/bin/python \
  deliverables/cm2_round139_rank3_minus_d0_adjacent_h1_collar_return_frontier.py \
  --precision-bits 24576 \
  --output /tmp/cm2-r139-producer-primary.json \
  > /tmp/cm2-r139-producer-primary.log 2>&1
```

Secondary:

```bash
env PYTHONHASHSEED=987654321 LC_ALL=C TZ=UTC \
  PYTHONDONTWRITEBYTECODE=1 PYTHONPATH=deliverables \
  /usr/bin/time -v .venv-neurips/bin/python \
  deliverables/cm2_round139_rank3_minus_d0_adjacent_h1_collar_return_frontier.py \
  --precision-bits 32768 \
  --output /tmp/cm2-r139-producer-secondary.json \
  > /tmp/cm2-r139-producer-secondary.log 2>&1
```

The primary exited 0 in 6:49.76 wall time, used 324.30 seconds of user CPU
and 1.34 seconds of system CPU, and reached 222024 KiB maximum RSS. The
secondary exited 0 in 8:58.94 wall time, used 433.14 seconds of user CPU and
1.78 seconds of system CPU, and reached 220232 KiB maximum RSS.

While the secondary arithmetic build was running, before its final write,
`apply_patch` created the output target with the literal sentinel
`ROUND139_OVERWRITE_SENTINEL`. The sentinel had size 28, mode 0664, inode
36968957, and SHA-256

```text
13d72a861d4c4c246d31ec0aa3efb2ce4f029b611557c62381e93f00d34fc5ee
```

The producer's final `write_atomic` validation accepted that safe existing
regular file and replaced it. The completed output had size 7097635, mode
0600, and inode 36968972. This directly exercises the fixed existing-output
overwrite path as well as the initial fresh-output path.

The comparison commands were:

```bash
sha256sum \
  /tmp/cm2-r139-producer-primary.json \
  /tmp/cm2-r139-producer-secondary.json \
  deliverables/cm2-round139-rank3-minus-d0-adjacent-h1-collar-return-frontier-2026-07-24.json

cmp -s \
  /tmp/cm2-r139-producer-primary.json \
  /tmp/cm2-r139-producer-secondary.json

cmp -s \
  /tmp/cm2-r139-producer-secondary.json \
  deliverables/cm2-round139-rank3-minus-d0-adjacent-h1-collar-return-frontier-2026-07-24.json
```

Both `cmp` invocations exited 0. All three SHA-256 values are

```text
64e91e6b1efcb2675982fbc453b08349b003c8be5b4d236f61e1392aaee045f0
```

## Independent verifier replay

Each verifier invocation rebuilds the complete Round139 result at both 24576
and 32768 Arb precision. It neither imports nor executes the Round139
producer.

Seed A:

```bash
env PYTHONHASHSEED=139139 LC_ALL=C TZ=UTC PYTHONDONTWRITEBYTECODE=1 \
  PYTHONPATH=deliverables \
  /usr/bin/time -v .venv-neurips/bin/python \
  deliverables/cm2_round139_rank3_minus_d0_adjacent_h1_collar_return_frontier_verifier.py \
  --certificate \
  deliverables/cm2-round139-rank3-minus-d0-adjacent-h1-collar-return-frontier-2026-07-24.json \
  --output /tmp/cm2-r139-verification-A.json \
  > /tmp/cm2-r139-verification-A.log 2>&1
```

Seed B:

```bash
env PYTHONHASHSEED=987654321 LC_ALL=C TZ=UTC \
  PYTHONDONTWRITEBYTECODE=1 PYTHONPATH=deliverables \
  /usr/bin/time -v .venv-neurips/bin/python \
  deliverables/cm2_round139_rank3_minus_d0_adjacent_h1_collar_return_frontier_verifier.py \
  --certificate \
  deliverables/cm2-round139-rank3-minus-d0-adjacent-h1-collar-return-frontier-2026-07-24.json \
  --output \
  deliverables/cm2-round139-rank3-minus-d0-adjacent-h1-collar-return-frontier-verification-2026-07-24.json \
  > /tmp/cm2-r139-verification-B.log 2>&1
```

Seed A exited 0 in 16:42.60, used 760.90 seconds of user CPU and 2.97
seconds of system CPU, and reached 245668 KiB maximum RSS. Seed B exited 0
in 14:37.06, used 757.04 seconds of user CPU and 2.77 seconds of system CPU,
and reached 248684 KiB maximum RSS.

The two artifacts are byte-for-byte identical:

```bash
cmp -s \
  /tmp/cm2-r139-verification-A.json \
  deliverables/cm2-round139-rank3-minus-d0-adjacent-h1-collar-return-frontier-verification-2026-07-24.json
```

That command exited 0. The verifier reports:

```text
status:                              PASS
semantic mutations rejected:       24/24
strict-JSON attacks rejected:      19/19
in-process path attacks rejected:  13/13
```

## Process-level hostile I/O

Twelve separate verifier processes used the same command shape:

```bash
env PYTHONHASHSEED=139000 LC_ALL=C TZ=UTC PYTHONDONTWRITEBYTECODE=1 \
  PYTHONPATH=deliverables \
  .venv-neurips/bin/python \
  deliverables/cm2_round139_rank3_minus_d0_adjacent_h1_collar_return_frontier_verifier.py \
  --certificate CASE_INPUT --output CASE_OUTPUT
```

The cases and terminal failures were:

| Case | Exit | Terminal reason |
|---|---:|---|
| missing certificate | 1 | `missing regular file:certificate` |
| byte-tampered certificate | 1 | `certificate byte pin` |
| symlink certificate | 1 | `symlink file:certificate` |
| hardlink certificate | 1 | `single-link regular file:certificate` |
| FIFO certificate | 1 | `missing regular file:certificate` |
| output aliases selected input | 1 | `output hardlinks protected input` |
| output aliases producer | 1 | `output hardlinks protected input` |
| output aliases verifier | 1 | `output hardlinks protected input` |
| output aliases pinned upstream | 1 | `output hardlinks protected input` |
| output symlink | 1 | `output symlink` |
| output hardlink | 1 | `existing output regular single-link` |
| output FIFO | 1 | `existing output regular single-link` |

No unexpected `out-*.json` file was created. A before/after `sha256sum`
comparison of the producer, certificate, verifier, and selected pinned
Round138 upstream exited 0.

## Frozen hashes

```text
producer:            462ffcb41ba24771ce655ddb3ad5f18d5a22c8d0cb443ec1791ea9272d3d512b
certificate:         64e91e6b1efcb2675982fbc453b08349b003c8be5b4d236f61e1392aaee045f0
certificate result:  6e8f54c34154ea5ba3c95d4e901bc643c020a0a42e180241ae9053bb24f42236
verifier:            cb96e0e1a74abcac4254f20584bab6997edb8de69f0d979f1d65d4c3fdfadd09
verification:        57093537ae3f464e276da830ee5821ffbe3576278c71adbe111b22a128f3005f
verification result: e96609b3ff1ba35c94e224c5d16897ed6d173fe69cc3cbf260ff85e5340165e1
```

The replay preserves the strict scope: the graph collar and rectangle are
local Round139 objects. It does not materialize a global Round35
restriction/component, Round50 owner, Round54 token/map, or Round67
`Omega_j`/`q_j`; Gate5 remains `10/18` and `NOT_CERTIFIED`, and CM2 remains
`NO-GO_FOR_CLAIM`.
