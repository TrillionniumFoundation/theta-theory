# CM2 Round146 physical centered-jet 2D frontier — cold replay

Date: 2026-07-24

## Frozen primary producer

The formal producer was executed at 8,192-bit precision under a fixed
locale, timezone and hash seed:

```bash
env PYTHONHASHSEED=146001 LC_ALL=C TZ=UTC PYTHONDONTWRITEBYTECODE=1 \
  PYTHONPATH=deliverables /usr/bin/time -v .venv-neurips/bin/python \
  deliverables/cm2_round146_physical_centered_jet_2d_frontier.py \
  --precision-bits 8192 \
  --output deliverables/cm2-round146-physical-centered-jet-2d-frontier-2026-07-24.json
```

It returned exit code 0 in `12:27.89` wall time, used `1,030.50` user
seconds and `1.45` system seconds, and reached `65,928 KiB` maximum RSS.

```text
engine SHA256:
ac332c1cc99c96a56251a53b2432caaba951f028de810045d840b8991bdf27eb

producer SHA256:
db0241c9bae4937cd1a01f23b4951247fa69fd16d9b06a75d446e5336c9930c4

certificate SHA256:
38ad7cdd5a2af7cda94792a31a8a83275022f943e8e6b9801ee4bece73b04eac

certificate result SHA256:
66936a51409bbe87ef2a10e80f081d345954c8104a23a4a05a21019f0d3b0e67
```

## Secondary producer replay

The complete producer was separately rerun at 12,288-bit precision
under a distinct hash seed:

```bash
env PYTHONHASHSEED=987654321 LC_ALL=C TZ=UTC PYTHONDONTWRITEBYTECODE=1 \
  PYTHONPATH=deliverables /usr/bin/time -v .venv-neurips/bin/python \
  deliverables/cm2_round146_physical_centered_jet_2d_frontier.py \
  --precision-bits 12288 --output /tmp/cm2-r146-producer-secondary.json
```

The command returned exit code `0` in `22:06.96`, used `1,801.89` user
seconds and `2.44` system seconds, and reached `66,000 KiB` maximum RSS.
It atomically replaced a 28-byte sentinel: inode
`36969599 -> 36969611`.

The full cross-precision artifact was not byte-identical:

```text
12,288-bit certificate SHA256:
2a1850057be4225ad32cc32042bdae03220ac1edf3509eca89e9bd4e33562b17

12,288-bit result SHA256:
4b64c312a8e0f36a8aa9632436f5991224655ef1807d7b580d4256ca8a11d10d
```

An exact recursive comparison found only three precision-sensitive result
fields: the two per-cell model-radius ledger digests and the central
cell's 128-bit padded terminal-cosine outer interval.  Removing exactly
those three diagnostic fields gives the same canonical result-projection
SHA256 at both precisions:

```text
negative ledger:
  8192:  06c81e504a7cb791dc5b7690f4b071c63ad85b4733e9608608b21bb635a459b3
  12288: 9deef8d742a1bfbf195ecec34c41eac8f29553dfc9f385ac6f07758fcae9ceb1

central ledger:
  8192:  b1ae4b21f8007e2056ef21b6a2b72542d77ffc6232c00430d34d51f6cf95533b
  12288: ae89b41ce3fc44d3e68c4ef4764fa5613f8fa80dcd348d032670444c89620397

stable canonical projection:
e8a9c37496159e3b7d08ac81910265e8988a538896712550da4d12600ea2d8bb
```

Every status, identifier, count, path hash, classification, physical
coordinate statement, event enclosure, D02 blocker and global nonpromotion
is exactly equal.  The two central terminal-cosine outer intervals overlap
strictly and their intersection is positive.  The full 12,288-bit replay
therefore confirms the mathematical envelope but does not support a
cross-precision byte-identity claim.

The producer was additionally rerun at the frozen 8,192-bit precision
under `PYTHONHASHSEED=987654321`.  It returned exit code `0` in `12:26.72`,
used `1,030.04` user seconds and `1.65` system seconds, and reached
`66,304 KiB` maximum RSS.  Its artifact is byte-identical to the primary
certificate.

## Independent verifier replays

The verifier closes and hashes the Round140, Round141, Round142 and
Round144 dependency envelope.  It also invokes the frozen Round141
transitive dependency guard.  It then reconstructs both 1,648-collision
cells with independent verifier primitives, rechecks the exact shared
face, physical Jacobian, D3 corridor and parametric interval-Newton proof,
and enforces every null/nonpromotion.

Its independently reconstructed event object is canonically byte-identical
at 8,192 and 12,288 bits, with SHA256
`0abb5de2c89841646a309523a30e1522e112c2394dd8862700acec78741d2069`.

```bash
env PYTHONHASHSEED=146314 LC_ALL=C TZ=UTC PYTHONDONTWRITEBYTECODE=1 \
  PYTHONPATH=deliverables /usr/bin/time -v .venv-neurips/bin/python \
  deliverables/cm2_round146_physical_centered_jet_2d_frontier_verifier.py \
  --certificate deliverables/cm2-round146-physical-centered-jet-2d-frontier-2026-07-24.json \
  --output deliverables/cm2-round146-physical-centered-jet-2d-frontier-verification-2026-07-24.json
```

The primary verifier returned exit code `0` in `12:35.47`, used `1,035.34`
user seconds and `1.27` system seconds, and reached `62,204 KiB` maximum
RSS.  It atomically replaced a 27-byte sentinel: inode
`14549122 -> 14549394`.

A second verifier replay used `PYTHONHASHSEED=987654321` and wrote
`/tmp/cm2-r146-verification-secondary.json`.  It returned exit code `0` in
`14:49.07`, used `1,030.99` user seconds and `1.50` system seconds, and
reached `61,952 KiB` maximum RSS.  Its verification artifact is
byte-identical to the primary verification.

```text
verifier SHA256:
d75af7cc251c212a11522a8884ad9afbb983197ba9e6e0d43598ffe06916ad44

formal verification SHA256:
c25646413467deb2c1c5ea68f92e97116546eb62333596afc61973430e002dd4

verification result SHA256:
7d2fa9fdaff97bf1267ebf9c03a31f38145badeab7410c136f91aaeab3f929d7
```

## Hostile replay

The formal verifier rejected all of its built-in adversarial cases:

```text
re-signed semantic mutations:       50/50
strict-JSON payload attacks:         21/21
in-process protected-path attacks:    7/7
```

Separate process-level harnesses rejected:

```text
hostile certificate/process inputs:  5/5
hostile producer/verifier I/O cases:  6/6
expanded output-target matrix:       15/15
```

The expanded matrix included frozen source and dependency targets,
certificate/counterpart targets, hardlinks, symlinks, dangling symlinks,
parent symlinks, missing and noncanonical parents, directories, a FIFO and
`/dev/null`.  Protected hashes remained unchanged.

## Replayed mathematical envelope

The replay repeats 3,296 cell/collision stages and 530,656 complete
radius-four candidate tests.  It proves:

- two exact physical coordinates with nonzero Jacobian determinant;
- two complete R1648 cells joined at one exact artificial face;
- one fixed owner/official-word path on both certified cells;
- 3,294 strict preterminal nonreturn cell/stages and two strict returns;
- a unique transverse collision-three D0-candidate event graph in the
  prescribed positive-`delta_beta` box;
- no earlier zero of that same candidate family between the certified
  upper face and the event graph.

The positive neighbor is only event-entering; no complete path is claimed
there.  The result is not a maximal component atlas and does not exhaust
all physical event families.  Round144 D02 remains `BLOCKED`, Gate5 remains
`10/18`, `NOT_CERTIFIED`, and CM2 remains `NO-GO_FOR_CLAIM`.
