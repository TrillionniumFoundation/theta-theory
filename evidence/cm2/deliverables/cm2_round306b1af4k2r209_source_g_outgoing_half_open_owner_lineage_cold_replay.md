# CM2 Round306 B1AF4 K2R209 — cold replay record

All authoritative executions used isolated Python mode:

```bash
PYTHONHASHSEED=17 python -I -B \
  cm2_round306b1af4k2r209_source_g_outgoing_half_open_owner_lineage_producer.py \
  --output-directory /tmp/cm2-r209-seed17.m4vF4O

PYTHONHASHSEED=93 python -I -B \
  cm2_round306b1af4k2r209_source_g_outgoing_half_open_owner_lineage_producer.py \
  --output-directory /tmp/cm2-r209-seed93.pcauDn
```

Both runs exited `0`; all four candidate outputs were byte-identical.

| run | elapsed | peak RSS |
|---|---:|---:|
| producer seed 17 | 102.44 s | 1,228,932 KiB |
| producer seed 93 | 102.73 s | 1,230,940 KiB |
| formal publication seed 209 | 103.35 s | 1,231,104 KiB |

The repeated producer summary was identical:

```text
result_sha256 2853728a94ba4efba0ba3dc7b47cf47f3505ca4d2f0ccf56409c0909e53d4bd9
2D file         3a038e1bfa5d39cccbbf62e0713bf0a6e5e825d5a316296a901ddcec4fbb47ac
1D file         b9bce03d22ca8179b543e36865e30d4bd98430592ca0b32a3f8bf78285de44d1
0D file         317a9f01bf01851a61eb8893e35bf81918eccee7f882885bf0380c1f12a27159
counts          17716 / 20456 / 40912
```

Independent no-write replays used:

```bash
PYTHONHASHSEED=17 python -I -B \
  cm2_round306b1af4k2r209_source_g_outgoing_half_open_owner_lineage_independent_verifier.py \
  --candidate-directory /tmp/cm2-r209-seed17.m4vF4O --no-write

PYTHONHASHSEED=93 python -I -B \
  cm2_round306b1af4k2r209_source_g_outgoing_half_open_owner_lineage_independent_verifier.py \
  --candidate-directory /tmp/cm2-r209-seed93.pcauDn --no-write
```

Both exited `0` with byte-identical deterministic receipts:

```text
status              PASS_INDEPENDENT_STRICT_REPLAY
result_sha256        2853728a94ba4efba0ba3dc7b47cf47f3505ca4d2f0ccf56409c0909e53d4bd9
attack_suite_sha256  091e3fbbea19b6c7476d947858dbfa01119d21e2c762e7953f709ab8f311de0b
verification_sha256  00fa5429c2bb755defbb316c6d342b2a9e2c2411c3b65774f67a84f210872f78
```

| run | elapsed | peak RSS |
|---|---:|---:|
| verifier seed 17, no-write | 120.87 s | 1,851,264 KiB |
| verifier seed 93, no-write | 127.59 s | 1,848,388 KiB |
| formal verifier publish seed 209 | 126.60 s | 1,850,640 KiB |

The verifier pins the producer as inert bytes.  It imports/executes neither
the candidate producer nor the Round209 probe.  It freshly decodes the
Round173/Round208 formal inputs and uses the separately pinned independent
evaluator only for pure expected-row reconstruction.

The final seal audit is a no-write replay bracketed by exact SHA-256, size,
mtime_ns, ctime_ns, inode, mode, and link-count snapshots of every manifest
member plus the manifest.  Acceptance requires byte-for-byte and metadata
identity before and after replay, followed by a second full manifest check.
