# Round306A exact cold-replay record

Runs used CPython `3.12.3`, zlib `1.3`, on
`Linux 7.0.0-28-generic x86_64`, from:

```text
/home/qian-qi/.openclaw/workspaces/telegram-bot-8449317572
```

## Frozen pins and exact outputs

```text
producer_sha256=ab798332c82f7aa3656c61e3b31698a30b0fa1a83d24900432e076e445d6f5d5
verifier_sha256=60cc0f9cec6c8f4121f7ed7fde45b11e1b72bd9adc897364d9c0937c92a54c72
schema_snapshot_sha256=abfe46bd4ce053ec78af31a1e159dfe9325dac2da9952493058c86b891d1f2ae

edge_file_sha256=6da4620a100c980f921350f162fda064580e603f8ff7221eeed768b8bd091d1f
member_file_sha256=710ebb660a7e7fad6a691c03bf845cf0081037ed09cc49a885c94c4bc472c276
r305b_promoted_file_sha256=08f9ff2f5df0210cedd8cb3f8d998846e3722bd6bb0a2216d8d6c24a95a64a41
r300a_reprojection_file_sha256=c3e62f9833c333fb89758edd5c3f1648364a70b91bd1ed85650241a4cd10b673
wtail_file_sha256=6bdcc231b3cfd67f18ff3c62c27af08fdc9eb562a2c4e24a601798c0ad6d2556
residual_file_sha256=1e79d529f3ca1fcefa170263a5d8b88929361ea27c0eeb3c6de108b870f9d8b8
result_file_sha256=febe77da4285791b54e098c80a4b868c1e5dc6e43e98a7553bfff5e065075010
result_object_sha256=6ee906cddae42e6df086cec26c7e0898ebe198519ce96605fd609a20c4f1e46a

attack_file_sha256=9e3f2bcf3f39af739bc05ca2f3acef2828f96e6f19402fe6a85bb3353f5fc25e
attack_object_sha256=215edf7d7071739d1711ad7b616b8c9f6d2e7fa51ab01f7d7c19cbf42039a7bb
attack_rows_sha256=26dafe27e0ce7ba37492abaeb0eea713cc4a458f0b886313d983ef30a201c5ea
verification_file_sha256=38fd7f9d41dcf39a2ec887d72b31da3d003cf03eda154da34d3a5d87ff12ba7e
verification_object_sha256=147372b651a11aec9101da717bbd82c2a744a801a2c581d130fe7c03464f5f9e
```

## Producer independent-process evidence

The default process used CLI seed `306101` with `PYTHONHASHSEED` unset:

```bash
/usr/bin/time -v \
  .venv-cm2/bin/python -B \
  deliverables/cm2_round306a_source_g_r305b_fresh_legal_component_dsu_rebuild.py \
  --candidate-dir <private-stage-used-by-run> \
  --seed 306101
```

Observed: exit `0`, elapsed `28:05.16`, user `1673.14`, system `9.83`,
maximum RSS `2,634,612 KiB`.  This is default/random-hash independent-process
evidence, not named hash-seed evidence.

Named seed A used both CLI seed and `PYTHONHASHSEED` `306101`.  Its terminal
receipt was lost during an interrupted turn, so no exit, timing, or RSS is
asserted.  The recovered complete candidate is:

```text
.cm2-round306a-private-candidates/seed306101_pyhash306101
```

Named seed B used:

```bash
/usr/bin/time -v env PYTHONHASHSEED=306997 \
  .venv-cm2/bin/python -B \
  deliverables/cm2_round306a_source_g_r305b_fresh_legal_component_dsu_rebuild.py \
  --candidate-dir .round306a_seed306997_stage_20260801T1149 \
  --seed 306997
```

Observed: exit `0`, elapsed `31:35.21`, user `1869.71`, system `10.95`,
maximum RSS `2,631,044 KiB`.

The default, named-seed-A, and named-seed-B seven-file candidates are
byte-for-byte identical.  All eighteen gzip integrity checks pass; every gzip
header uses `mtime=0` and an empty stored filename.  All result bytes are
canonical and the result object self-hash closes.

## Independent no-write verifier reconstruction

```bash
/usr/bin/time -v env PYTHONHASHSEED=306551 \
  .venv-cm2/bin/python -B \
  deliverables/cm2_round306a_source_g_r305b_fresh_legal_component_dsu_rebuild_promotion_verifier.py \
  --no-write-reconstruction
```

Observed:

```text
exit=0
elapsed=28:36.59
maximum_resident_set_kib=2576912
status=PASS_INDEPENDENT_CACHELESS_NO_WRITE_ROUND306A_RECONSTRUCTION
fresh_rank_reduction_count=275276
fresh_component_count=92688
incremental_Round305B_rank_reduction_count=8
Round300A_cross_component_residual_count=0
formal_maximality_credit=0
formal_fibre_credit=0
formal_global_disposition_credit=0
candidate_opened=false
candidate_or_formal_output_written=false
producer_imported_executed_parsed_or_tokenized=false
```

The independently reconstructed seven expected hashes equal the frozen hashes
above.  The timed run reported filesystem outputs `0`.

## Exact candidate admission without promotion

```bash
/usr/bin/time -v env -u PYTHONPATH \
  .venv-cm2/bin/python -B -I \
  deliverables/cm2_round306a_source_g_r305b_fresh_legal_component_dsu_rebuild_promotion_verifier.py \
  --candidate-dir \
  .cm2-round306a-private-candidates/seed306101_pyhash306101
```

Observed:

```text
exit=0
elapsed=28:04.74
maximum_resident_set_kib=2575972
status=PASS_EXACT_ROUND306A_PRIVATE_CANDIDATE_ADMISSION__ZERO_FORMAL_CREDIT
formal_deliverables_written=false
attack_file_sha256=9e3f2bcf3f39af739bc05ca2f3acef2828f96e6f19402fe6a85bb3353f5fc25e
attack_object_sha256=215edf7d7071739d1711ad7b616b8c9f6d2e7fa51ab01f7d7c19cbf42039a7bb
verification_file_sha256=38fd7f9d41dcf39a2ec887d72b31da3d003cf03eda154da34d3a5d87ff12ba7e
verification_object_sha256=147372b651a11aec9101da717bbd82c2a744a801a2c581d130fe7c03464f5f9e
```

Admission reconstructs all expected bytes before opening the candidate.  It
creates and removes temporary transaction-defense fixtures but writes no
candidate or formal artifact.

## Formal promotion

```bash
/usr/bin/time -v env -u PYTHONPATH \
  .venv-cm2/bin/python -B -I \
  deliverables/cm2_round306a_source_g_r305b_fresh_legal_component_dsu_rebuild_promotion_verifier.py \
  --candidate-dir \
  .cm2-round306a-private-candidates/seed306101_pyhash306101 \
  --promote
```

Observed:

```text
exit=0
elapsed=33:06.27
maximum_resident_set_kib=2577576
status=PASS_EXACT_CACHELESS_ROUND306A_FRESH_LEGAL_COMPONENT_DSU_REBUILD
formal_attack_sha_matches_admission=true
formal_verification_sha_matches_admission=true
formal_candidate_cmp_7_of_7=true
formal_gzip_integrity_6_of_6=true
result_attack_verification_self_hashes_close=3/3
transaction_file_modes_0600_and_nlink_1=9/9
commit_order_matches_marker=true
orphan_stage_count=0
```

The content-bound marker requires the complete nine-file transaction bundle,
committed attack first and verification last.  Mtime is not authentication;
as a diagnostic, the observed attack and verification mtimes are
`2026-08-01 14:19:25.742619331 +0800` and
`2026-08-01 14:19:31.972408979 +0800`.

## Replay boundary

The sealed result proves exactly:

```text
legal_edge_applications=478718
fresh_DSU_rank_reductions=275276
fresh_component_count=92688
fresh_partition_sha256=a3f7ce1e28a956a46803ef466709ded0053633f5e104746c6d1e6e51b873e19c
Round305B_physical_witness_rows=1024
Round305B_component_edge_applications=8
Round305B_incremental_rank_reductions=8
Round300A_rows=3232
Round300A_cross_component_residual=0
formal_maximality_credit=0
formal_fibre_credit=0
formal_global_disposition_credit=0
D02_status=BLOCKED
CM2_status=NO-GO_FOR_CLAIM
```

Round300A residual zero is not a full maximality theorem.

## Exact manifest checklist

The companion manifest contains exactly the following 13 members and excludes
itself:

```text
cm2_round306a_source_g_r305b_fresh_legal_component_dsu_rebuild.py
cm2_round306a_source_g_r305b_fresh_legal_component_dsu_rebuild_edge_application_ledger.json.gz
cm2_round306a_source_g_r305b_fresh_legal_component_dsu_rebuild_member_component_ledger.json.gz
cm2_round306a_source_g_r305b_fresh_legal_component_dsu_rebuild_r305b_promoted_edge_application_ledger.json.gz
cm2_round306a_source_g_r305b_fresh_legal_component_dsu_rebuild_r300a_reprojection_ledger.json.gz
cm2_round306a_source_g_r305b_fresh_legal_component_dsu_rebuild_wtail_disposition_ledger.json.gz
cm2_round306a_source_g_r305b_fresh_legal_component_dsu_rebuild_residual_gate_ledger.json.gz
cm2_round306a_source_g_r305b_fresh_legal_component_dsu_rebuild_result.json
cm2_round306a_source_g_r305b_fresh_legal_component_dsu_rebuild_promotion_verifier.py
cm2_round306a_source_g_r305b_fresh_legal_component_dsu_rebuild_attack_suite.json
cm2_round306a_source_g_r305b_fresh_legal_component_dsu_rebuild_verification.json
cm2_round306a_source_g_r305b_fresh_legal_component_dsu_rebuild_report.md
cm2_round306a_source_g_r305b_fresh_legal_component_dsu_rebuild_cold_replay.md
```

The report and cold-replay record do not embed their own file hashes.  The
external 13-member manifest closes them without a self-reference cycle.
Including the manifest itself, the sealed Round306A package has 14 files.
