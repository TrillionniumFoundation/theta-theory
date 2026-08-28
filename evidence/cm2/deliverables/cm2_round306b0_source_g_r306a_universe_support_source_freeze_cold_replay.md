# Round306B0 exact cold-replay record

Runs used CPython `3.12.3`, zlib `1.3`, on
`Linux 7.0.0-28-generic x86_64`, from:

```text
/home/qian-qi/.openclaw/workspaces/telegram-bot-8449317572
```

## Frozen pins and exact outputs

```text
producer_sha256=48f38e2b90aa2c1b934ba657f8c6e66a8cb97fa89f9439a0b11ed5fbb3d20d83
verifier_sha256=4d4fc9483b4ee65a55ccccf1ff30f4161c6f2fdd4853f64caef0291354cf1857
Round306A_manifest_sha256=35da99af5bb4c424284af2d7b396fc94b82dd6c6aa468c6a43a139107f9d9efc
Round306A_partition_sha256=a3f7ce1e28a956a46803ef466709ded0053633f5e104746c6d1e6e51b873e19c

member_file_sha256=c9a8649c8473bb6a170187e7f803e95748d2ff2198b1b846d97383dd5f0581af
component_file_sha256=d489b8480859d51ac6d98c9c59bc25c71c3cc6d0ffb1e0e13ddb988ecc80b8a7
pair_file_sha256=f8e22c93a0b070ae3ff2da557c1011ba74a214fbf4b841cdfeb219a2556f6261
source_file_sha256=39ebbf26976b3c1e7b79b043f2f801d568638583a01fff8830f8886148a23fc3
gap_file_sha256=b214bbb55a06e275c1b00f2f12e5f1e128840d3ed9b81cf474151a4e93af7f55
result_file_sha256=badc000c6fadd8807b26a7c3511edc51796c962f150b438956e4c549fd0d5735
result_object_sha256=9ffe9144bc67f9bb7bb7e9c071b29a000f7d8e89396a3250b8207bfcc950d3d2

attack_file_sha256=d3d40aad0a6cd98d936524fb2f9c786adbdcede483de185121672a514ac87cfd
attack_object_sha256=742962bf7d84709e85c41d8e45b8db7e9c2b423d76defb65ec9b1f8500c56621
attack_rows_sha256=f054ffbfa30884c1aa2383c514b6f3c504d8104af4f7b8974a76e0528599461d
verification_file_sha256=f8acc3150d4663d92976a44ab1c3b35c7264f4c4d14808f9133f1184d3f4b590
verification_object_sha256=774813f546184aa30c342840ddfa6b0566ebe4d382acd16d74ead8f03dadaddc
```

## Lightweight contract checks

```bash
.venv-cm2/bin/python -B \
  deliverables/cm2_round306b0_source_g_r306a_universe_support_source_freeze.py \
  --self-test

env -u PYTHONPATH .venv-cm2/bin/python -B -I \
  deliverables/cm2_round306b0_source_g_r306a_universe_support_source_freeze_promotion_verifier.py \
  --self-test
```

Both returned exit `0`.  The verifier rejected `27 / 27` attacks.  These
lightweight checks opened no large source or candidate and wrote no formal
artifact.

## Two independent v2 producer processes

```bash
/usr/bin/time -v env PYTHONHASHSEED=306101 \
  .venv-cm2/bin/python -B \
  deliverables/cm2_round306b0_source_g_r306a_universe_support_source_freeze.py \
  --candidate-dir \
  .cm2-round306b0-private-candidates/seed306101_v2_pyhash306101
```

Observed: exit `0`, elapsed `8:20.79`, maximum RSS `692,640 KiB`.

```bash
/usr/bin/time -v env PYTHONHASHSEED=306997 \
  .venv-cm2/bin/python -B \
  deliverables/cm2_round306b0_source_g_r306a_universe_support_source_freeze.py \
  --candidate-dir \
  .cm2-round306b0-private-candidates/seed306997_v2_pyhash306997
```

Observed: exit `0`, elapsed `5:04.06`, maximum RSS `697,124 KiB`.

The two complete six-file candidates are byte-for-byte equal.  All ten gzip
integrity checks pass, every gzip member is deterministic, and both canonical
result-object self-hashes close.

An earlier complete schema-v1 diagnostic run (`8:31.91`, maximum RSS
`698,556 KiB`) is quarantined under `.cm2-round306b0-superseded-v1/` and is not
formal input.  A second v1 diagnostic was interrupted after `5:06.27`; no
target or promotion stage survived.

## Exact candidate admission without promotion

```bash
/usr/bin/time -v env -u PYTHONPATH \
  .venv-cm2/bin/python -B -I \
  deliverables/cm2_round306b0_source_g_r306a_universe_support_source_freeze_promotion_verifier.py \
  --candidate-dir \
  .cm2-round306b0-private-candidates/seed306101_v2_pyhash306101
```

Observed after the final verifier fix:

```text
exit=0
elapsed=6:03.18
maximum_resident_set_kib=551324
status=PASS_EXACT_ROUND306B0_PRIVATE_CANDIDATE_ADMISSION__ZERO_FORMAL_CREDIT
formal_member_universe_freeze_credit=0
formal_pair_denominator_freeze_credit=0
formal_maximality_credit=0
formal_artifact_written=false
attack_file_sha256=d3d40aad0a6cd98d936524fb2f9c786adbdcede483de185121672a514ac87cfd
verification_file_sha256=f8acc3150d4663d92976a44ab1c3b35c7264f4c4d14808f9133f1184d3f4b590
```

The verifier independently reconstructs all source bindings, 564,492 member
rows, 92,688 component rows, six pair rows, and the 15-row source inventory
before candidate admission.  Its source scans are descriptor/snapshot-bound
with post-read and final pre-admission stability checks.

The first admission attempt used a pre-fix verifier and failed closed after
`6:05.93` with maximum RSS `548,308 KiB`; it wrote no formal file.  That run
exposed three missing exact-key expectations, which were fixed before the
hash-pinned admission above.

## Formal promotion

```bash
/usr/bin/time -v env -u PYTHONPATH \
  .venv-cm2/bin/python -B -I \
  deliverables/cm2_round306b0_source_g_r306a_universe_support_source_freeze_promotion_verifier.py \
  --candidate-dir \
  .cm2-round306b0-private-candidates/seed306101_v2_pyhash306101 \
  --promote
```

Observed:

```text
exit=0
elapsed=6:13.36
maximum_resident_set_kib=550616
status=PASS_EXACT_ROUND306B0_UNIVERSE_SUPPORT_SOURCE_FREEZE
formal_member_universe_freeze_credit=1
formal_pair_denominator_freeze_credit=1
formal_maximality_credit=0
formal_fibre_credit=0
formal_global_disposition_credit=0
formal_candidate_cmp=6/6
formal_gzip_integrity=5/5
result_attack_verification_self_hashes_close=3/3
transaction_file_modes_0600_and_nlink_1=8/8
orphan_stage_count=0
```

The transaction is content-bound and commits in exact order:

```text
attack -> member -> component -> pair -> source -> gap -> result -> verification
```

The verification marker requires the complete eight-file transaction bundle.
Mtime is not authentication; the observed attack and verification mtimes are
`2026-08-01 15:42:40.826646651 +0800` and
`2026-08-01 15:42:44.447262505 +0800`.

## Replay boundary

The sealed B0 result proves exactly:

```text
member_count=564492
component_count=92688
cross_component_pair_count=158838084354
source_identity_or_manifest_binding_gap_count=0
member_universe_freeze_credit=1
pair_denominator_freeze_credit=1
geometry_feature_cover_proved=false
cross_component_pair_routing_proved=false
full_maximality_proved=false
formal_maximality_credit=0
official_fibres_exhausted=0
Source_G_global_dispositions_completed=0
D02_status=BLOCKED
CM2_status=NO-GO_FOR_CLAIM
```

## Exact manifest checklist

The companion manifest contains exactly the following 12 members and excludes
itself:

```text
cm2_round306b0_source_g_r306a_universe_support_source_freeze.py
cm2_round306b0_source_g_r306a_universe_support_source_freeze_member_support_source_index.json.gz
cm2_round306b0_source_g_r306a_universe_support_source_freeze_component_census.json.gz
cm2_round306b0_source_g_r306a_universe_support_source_freeze_pair_denominator.json.gz
cm2_round306b0_source_g_r306a_universe_support_source_freeze_source_table_inventory.json.gz
cm2_round306b0_source_g_r306a_universe_support_source_freeze_coverage_gap.json.gz
cm2_round306b0_source_g_r306a_universe_support_source_freeze_result.json
cm2_round306b0_source_g_r306a_universe_support_source_freeze_promotion_verifier.py
cm2_round306b0_source_g_r306a_universe_support_source_freeze_attack_suite.json
cm2_round306b0_source_g_r306a_universe_support_source_freeze_verification.json
cm2_round306b0_source_g_r306a_universe_support_source_freeze_report.md
cm2_round306b0_source_g_r306a_universe_support_source_freeze_cold_replay.md
```

The report and cold-replay record do not embed their own file hashes.  The
external 12-member manifest closes them without a self-reference cycle.
Including the manifest itself, the sealed Round306B0 package has 13 files.
