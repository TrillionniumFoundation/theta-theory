# CM2 Round 143 terminal-face endpoint and recut frontier — cold replay

Date: 2026-07-24

## Producer replay

The producer was run twice from pinned inputs under distinct hash seeds.

```bash
env PYTHONHASHSEED=143143 LC_ALL=C TZ=UTC PYTHONDONTWRITEBYTECODE=1 \
  PYTHONPATH=deliverables /usr/bin/time -v .venv-neurips/bin/python \
  deliverables/cm2_round143_r1648_terminal_face_endpoint_recut_frontier.py \
  --output /tmp/cm2-r143-candidate.json

env PYTHONHASHSEED=143001 LC_ALL=C TZ=UTC PYTHONDONTWRITEBYTECODE=1 \
  PYTHONPATH=deliverables /usr/bin/time -v .venv-neurips/bin/python \
  deliverables/cm2_round143_r1648_terminal_face_endpoint_recut_frontier.py
```

Both commands returned exit code 0 and emitted byte-identical certificates:

```text
certificate SHA256:
74df2697c0db44ea5ac0a3ea9ab360100fc9750e1358b5172cd359522886ef67

certificate result SHA256:
35a9f8e0437086a2feaf294c10c621ce21319dc93aac88f33dbc4024e4507e92
```

Observed resources:

```text
seed 143143:  3:48.00 wall, 172.70 s user, 56,972 KiB maximum RSS
seed 143001:  3:43.61 wall, 174.00 s user, 56,272 KiB maximum RSS
```

The producer source SHA256 is
`bac63d0fb61965030a38b02f213ca90f580b66fc1f163f4829f2dafb57193a38`.

## Independent verifier replay

The verifier source SHA256 is
`197be350c4a6bed80a1c413822c5b838c2d0bc7da88360998fd7ad939da85601`.
It independently validates the formal fields and then runs another producer
in a clean temporary directory with `PYTHONHASHSEED=987654321`.

```bash
env PYTHONHASHSEED=143777 LC_ALL=C TZ=UTC PYTHONDONTWRITEBYTECODE=1 \
  PYTHONPATH=deliverables /usr/bin/time -v .venv-neurips/bin/python \
  deliverables/cm2_round143_r1648_terminal_face_endpoint_recut_frontier_verifier.py \
  --output /tmp/cm2-r143-verification-candidate.json

env PYTHONHASHSEED=143999001 LC_ALL=C TZ=UTC PYTHONDONTWRITEBYTECODE=1 \
  PYTHONPATH=deliverables /usr/bin/time -v .venv-neurips/bin/python \
  deliverables/cm2_round143_r1648_terminal_face_endpoint_recut_frontier_verifier.py
```

The first verification returned exit code 0 in 3:47.69 wall seconds with
56,584 KiB maximum RSS.  It rejected all 30 re-signed semantic mutations and
reported a byte-identical producer replay.  The second command was launched
only after canonical-certificate restoration and returned exit code 0 in
4:15.84 wall seconds with 57,784 KiB maximum RSS.  It also returned `PASS`.

```text
formal verification SHA256:
3ee6fe0e48bdf05a6f76726ded302aa4d632c306a4a260f444e1c2a66dfd9bd7

verification result SHA256:
51d616892452c92a4ed47586b6923ffaaf8e722e6b32d48445cbb4f762f9cf1c
```

## Hostile input and path replay

A separate harness exercised the verifier's bounded strict-JSON loader with:

```text
duplicate key, NaN, 4,097-digit integer, list root,
symlink, hardlink, directory, FIFO
```

All `8/8` were rejected.  Direct calls to the two atomic writers used seven
genuinely hostile targets each:

```text
protected source, second protected input, output symlink,
output directory, protected hardlink, symlinked parent, FIFO
```

Producer paths were rejected `7/7`; verifier paths were rejected `7/7`.
The certificate target itself was not included because it is the producer's
intended legal output.

Five process-level hostile certificate targets—missing file, symlink,
directory, duplicate-key regular file, and oversized-integer regular
file—each exited 1, created no verification output, and left all canonical
pins unchanged.

An earlier exploratory harness did mistakenly include that legal destination
and wrote a 13-byte sentinel.  The canonical file was immediately restored
from `/tmp/cm2-r143-candidate.json`, whose bytes already matched the frozen
dual-seed certificate.  The restored SHA256 is
`74df2697c0db44ea5ac0a3ea9ab360100fc9750e1358b5172cd359522886ef67`.
All protected source, verifier, dependency, and certificate hashes were then
rechecked, and the final verifier replay and manifest were run after the
restoration.

## Replayed strict boundary

The replay certifies the unique local terminal-face root, strict derivative,
complete 265,328-test radius-four owner audit, 1,647 preterminal nonreturns,
and terminal-only active face.  It reproduces both coordinate-explicit
Round137-v1 locators, `B14`, conditional `k=0`, and the conditional image
recut ledger.

It does not promote the missing face-to-D0 corridor to a maximal leaf.  All
historical ranks, parent-`W`, image rank, and restriction remain null.
Gate5 remains `10/18`, `NOT_CERTIFIED`; CM2 remains
`NO-GO_FOR_CLAIM`.
