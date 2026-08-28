# Round306B1G0 exact cold-replay record

All recorded runs used the system `python3`: CPython `3.12.3`, zlib `1.3`,
on `Linux 7.0.0-28-generic x86_64`, from:

```text
/home/qian-qi/.openclaw/workspaces/telegram-bot-8449317572
```

## Frozen implementation pins and exact formal outputs

```text
producer_sha256=97f1d0736a616071dbb0dba3bf533e3fae96091fc6b165395436216bb69c9321
producer_size=90721
verifier_sha256=47d642bfd90c8f8040a7de97df88788f2295e60b50ad7c72bb8ae2e85d89004b
verifier_size=128011

graph_file_sha256=5ac33be2b7639e1d30ae14abd5a7cf4cc6d1cc65fb0730e98616434f08921cb0
graph_ledger_sha256=a684dad14281e44c9dc02a0f825af661ef152f86a436c827fc0b113d25b4d6a0
sheet_file_sha256=041328aa135a1a67cbbdc8c5d84fe2c1a9bef2231a6cb33668ab05ecd6b227e3
sheet_ledger_sha256=3686f3b90a77195dbecd08750707a32f98e07f9fdff5f59d57f09c1178a48fda
side_file_sha256=d79af13182f99cdb2df6d39731e762b0d145baf79772b99be5069669c5b80ee1
side_ledger_sha256=108bdcbe1c124de15d8f48f82a3cdb7aa545f6f61294be34e3e5b07979d6670e
correction_file_sha256=834b687845a156328873888e405793f52a12df9d6286ae07d8a572c6163a361a
correction_ledger_sha256=a4af6f87737028981be9dccae9c2c28236408aa1f112f507418b6e4516eeb671
member_file_sha256=79382a6d8c3d086aeb29eff9fcb8653f2a73d85d79aab27e71e72cc8b1165a0b
member_ledger_sha256=65493ba72be6047b7c1c4ea64045460ad8160ab05440d02204393d3697a4d541
gap_file_sha256=2ba1903e2ce6d44ee623d0ccaacce973f7327e1e36ba8f97d0ab3865f1ec9809
gap_ledger_sha256=5324319ce7b3f90f67b3e12af6848f851008fd52c7cbd7c8d433cd0652c52f9e

result_file_sha256=3f494ebc9f046bfe9f42aef16edeadaece099d7ba7547b11f07484e3f6d81b9e
result_object_sha256=7bb3def1952176cbaf98723a6a2c5126e3c9193efac36a0d9a2c07533e0ec9bd
attack_file_sha256=fc7e6fa712638ffd37c7963229d85df69d0ed7ceb219650eda44ae93627f7333
attack_object_sha256=163e7afe7b23f85bc18d040fb21bc3b1823fafe8d1f36701eff93c87467f0feb
attack_rows_sha256=f36df3913af61d66e621d4141cfe3c0aafc5eb31d25ff402c6b93c74da96ba99
verification_file_sha256=65b7a01fd82535f357dbb44b8c68a68c86afcbb75b1c1c9b9159b71f9815139a
verification_object_sha256=542de6d90a6dcb6cd8775a1caf6fe3c3e62bbae49a10e864a7820ba3d083f700
```

The six gzip ledger commitments bind the following exact row counts, row
streams, row IDs, and row hashes:

```text
graph_rows=38624
graph_rows_sha256=beda6faaf7d3be25075d8f2a7f292cba97f591d6255758b6b16efc141339673f
graph_row_ids_sha256=982ee86845f92368cee72b74c52e401eecfb6dd225a4b198910b89ce34a8a7dc
graph_row_hashes_sha256=7fde3bb652a469eb3b04fe31a80c365d010d914700348954c5d917ac1162dace

sheet_rows=38624
sheet_rows_sha256=9238a05af9a97002488576d3648ce06ee750858f156638c314ba2e0a24fe3e1f
sheet_row_ids_sha256=b36ca314b15b8b8297dfeda9cb4fe37360ff20339e7603a6388ac172cfb87300
sheet_row_hashes_sha256=a3c606a9ba302ced5593d941529946729da5d160a32384ca37060b20011a01f5

side_rows=76848
side_rows_sha256=43ee8ffd2b77231c43c0af10198bbcc1f1def12f2e6bfd28f82c66ea26a207b2
side_row_ids_sha256=9e2a2c015372aa22e5f2cfa1f11ae268496831b3118da5bd5087fc6d7f403f53
side_row_hashes_sha256=2090d073d45f0097df68a60b36085786de0db51d76219b562734465bbf6daff6

correction_rows=400
correction_rows_sha256=a3df5bc8c8a86ea6958daefa7ec9b99013a04152378e5bcb18991ec4860cac67
correction_row_ids_sha256=b3dec2b9ef34fd5ebc3701201593ca90146f6d6150e5b593284a2a974a1d8caf
correction_row_hashes_sha256=f172394acdc909f6bc58f59fd1f361c4a4c5b00d06b2a8e8369b7638a6e6c592

member_rows=115456
member_rows_sha256=35189ef67c69078e44bbd440be37ef870935a8fd67817501ae995cceae383ea6
member_row_ids_sha256=ff6c659209636eec5235a375e8f8ba1cd5bf69c39df6630e6dfaeb95b0945d72
member_row_hashes_sha256=88026547b175b4ee968f738fe1276163d364b4482d164dbc2e84377039088eae

gap_rows=154096
gap_rows_sha256=d47d29e9eccc04374851cf12a3bc08fbe62837673fe8beb5dd1c9382337ad27b
gap_row_ids_sha256=f1c3bf0bb9991f1298a3bc8ce90d55871122ef81b679f32fca21b81087ee1421
gap_row_hashes_sha256=ca9e836b8ca114ba2843a9196748128b6194adb3bd801bb9a28dfff44d28af35
```

The nine-file formal transaction consists of the attack object, six ledgers,
result object, and verification object.  Its exact file hashes are the nine
`*_file_sha256` values above.

## Lightweight contract checks

The actual lightweight commands were:

```bash
python3 \
  deliverables/cm2_round306b1g0_source_g_graph_source_inventory_and_join_freeze.py \
  --self-test

python3 \
  deliverables/cm2_round306b1g0_source_g_graph_source_inventory_and_join_freeze.py \
  --transaction-self-test

python3 \
  deliverables/cm2_round306b1g0_source_g_graph_source_inventory_and_join_freeze_promotion_verifier.py \
  --self-test
```

All returned exit `0`.  The producer contract passed 23 groups.  Its
inode-bound transaction test passed 14 named mechanisms; that test explicitly
does not claim crash/SIGKILL orphan recovery.  The verifier rejected `50 / 50`
defense-in-depth fixtures: `35` semantic contract units, `5` real temporary
filesystem transactions, and `10` strict-wire units.  Its formal suite reports
`reconstruction_attack_count=0` rather than relabeling unit fixtures as full
source reconstructions.  The verifier self-test also passed 14 marker/parser
regressions.  These lightweight runs opened no sealed large source or private
candidate and wrote no formal artifact.

## Two independent producer candidates

The actual producer commands were:

```bash
PYTHONHASHSEED=3063101 /usr/bin/time -v \
  python3 \
  deliverables/cm2_round306b1g0_source_g_graph_source_inventory_and_join_freeze.py \
  --candidate-dir .cm2-round306b1g0-private-candidates/seed3063101
```

Observed: exit `0`, elapsed `2:47.25`, maximum RSS `695,692 KiB`.

```bash
PYTHONHASHSEED=3063999 /usr/bin/time -v \
  python3 \
  deliverables/cm2_round306b1g0_source_g_graph_source_inventory_and_join_freeze.py \
  --candidate-dir .cm2-round306b1g0-private-candidates/seed3063999
```

Observed: exit `0`, elapsed `2:42.86`, maximum RSS `696,172 KiB`.

Both exact seven-file candidates are byte-for-byte equal.  Their six gzip
members pass integrity checking, have deterministic compressed bytes, and
their result object self-hashes close.  Both directories are under the
dedicated private candidate root.  Each result remains explicitly
`candidate_is_formal=false` and grants zero theorem credit.

## Fail-closed first admission and marker-stream hardening

The initial heavy admission used the actual command shape below with the
then-frozen verifier `62f1d842c7987070719d90190290c3a54ad0a1e7eb5a089c6a9ba813360c5469`
(size `120129`):

```bash
PYTHONHASHSEED=3064551 /usr/bin/time -v \
  python3 \
  deliverables/cm2_round306b1g0_source_g_graph_source_inventory_and_join_freeze_promotion_verifier.py \
  --candidate-dir .cm2-round306b1g0-private-candidates/seed3063101
```

Observed: nonzero exit, elapsed `0:01.93`, maximum RSS `70,084 KiB`.  The run
failed closed at the old fixed, bounded source-table prelude before reaching a
legal later table marker.  It failed before candidate lstat/open and before any
publication setup or formal write.  This was an implementation-boundary defect
in locating a pinned table inside a large legal source, not a candidate row or
mathematical discrepancy.

The source-table locator was replaced by a bounded rolling marker search.  It
scans no more than the exact pinned source size, retains only the current chunk
plus the longest marker overlap, detects forbidden/duplicate anchors, and
hands the unchanged strict comma/JSON state machine the bytes after the exact
array marker.  The final verifier is `47d642bf...9004b` above.  An independent
AST/delta audit found the change confined to marker streaming, the associated
array-source wrapper, contract reporting, and regressions; source counts and
all credit boundaries were unchanged.  The 14 embedded regressions and an
additional `11,596` synthetic hostile marker/parser combinations passed,
including a legal prelude beyond 32 MiB, arbitrary small chunks and short
reads, boundary-crossing markers, near/missing/wrong/truncated and duplicate
markers, and strict comma/JSON rejection.  Those `11,596` checks were a
separate hardening audit, not added to the formal `50 / 50` attack count; they
opened no sealed large source, candidate, or formal output.

## Exact no-write candidate admission

The actual final admission command was:

```bash
PYTHONHASHSEED=3064666 /usr/bin/time -v \
  python3 \
  deliverables/cm2_round306b1g0_source_g_graph_source_inventory_and_join_freeze_promotion_verifier.py \
  --candidate-dir .cm2-round306b1g0-private-candidates/seed3063101
```

Observed:

```text
exit=0
elapsed=3:25.25
maximum_resident_set_kib=700348
status=PASS_EXACT_B1G0_PRIVATE_CANDIDATE_ADMISSION__ZERO_FORMAL_THEOREM_CREDIT
formal_full_support_credit=0
formal_maximality_credit=0
formal_fibre_credit=0
formal_global_disposition_credit=0
formal_artifact_written=false
predicted_attack_file_sha256=fc7e6fa712638ffd37c7963229d85df69d0ed7ceb219650eda44ae93627f7333
predicted_verification_file_sha256=65b7a01fd82535f357dbb44b8c68a68c86afcbb75b1c1c9b9159b71f9815139a
```

The verifier treated the producer as inert SHA-pinned bytes and independently
reconstructed the inventory from 22 exact size-and-SHA-pinned source files.
It completed the `564,492`-row B0 scan before opening the candidate, then
compared every canonical row and every compressed-file hash across all six
ledgers plus the result.  The predicted attack and verification bytes equal
the later formal files.  No promotion was requested and no formal artifact was
written in this run.

## Formal promotion

The actual promotion command used the independently generated second
candidate:

```bash
PYTHONHASHSEED=3064777 /usr/bin/time -v \
  python3 \
  deliverables/cm2_round306b1g0_source_g_graph_source_inventory_and_join_freeze_promotion_verifier.py \
  --candidate-dir .cm2-round306b1g0-private-candidates/seed3063999 \
  --promote
```

Observed:

```text
exit=0
elapsed=3:33.67
maximum_resident_set_kib=695160
status=PASS_EXACT_ROUND306B1G0_GRAPH_SOURCE_INVENTORY_AND_JOIN_FREEZE__ZERO_THEOREM_CREDIT
formal_graph_definition_credit=0
formal_physical_incidence_credit=0
formal_full_support_credit=0
formal_maximality_credit=0
formal_fibre_credit=0
formal_global_disposition_credit=0
```

The content-bound, no-clobber transaction committed in this exact order:

```text
attack
-> graph-source inventory
-> graph-sheet join
-> graph-side join
-> R264 correction disposition
-> B0 member backbinding
-> gap
-> result
-> verification
```

Thus the attack suite was durable first and the verification object was
published last as the sole package marker.  Postchecks found both private
candidates byte-identical to all seven corresponding formal candidate files
(`7 / 7` for each candidate), all six formal gzip streams intact, the result,
attack, and verification self-hashes closed, all nine formal transaction files
mode `0600` with link count `1`, and no orphan promotion stage.  The
verification marker binds the complete transaction but grants no theorem
credit.  Downstream consumers must validate the entire marker-bound bundle,
not the marker alone.

## Exact inventory and zero-credit boundary

The sealed result and independent verification record exactly:

```text
graph_count=38624
graph_sheet_join_count=38624
graph_side_join_count=76848
physical_incidence_count=115472
distinct_B0_member_backbinding_count=115456
R264_correction_count=400
gap_count=154096

R242_R245_graphs=264
R242_R245_sheets=264
R242_R245_sides=528
R242_R245_incidence=792

R235_R248_graphs=38328
R235_R248_sheets=38328
R235_R248_pre_correction_sides=76656
R264_absent_owner_prunes=184
R264_present_phantom_drops=216
R235_R248_final_sides=76256
R235_R248_final_incidence=114584

R236_partitions=16
R236_graphs=32
R236_sheets=32
R236_distinct_side_members=48
R236_side_references=64
R236_incidence=96

graph_definition_gaps=38624
physical_incidence_gaps=115472
total_gaps=154096
official_key_used_as_join_or_routing_filter=false
source_free_graph_definition_complete=false
physical_incidence_theorem_complete=false
formal_graph_definition_credit=0
formal_physical_incidence_credit=0
formal_full_support_credit=0
formal_maximality_credit=0
formal_fibre_credit=0
formal_global_disposition_credit=0
D02_status=BLOCKED
CM2_status=NO-GO_FOR_CLAIM
```

The package freezes the exact graph-source inventory and source-derived joins.
It does not prove a source-free graph definition, the physical-incidence
theorem, full support, component maximality, official-fibre exhaustion,
Source-G global dispositions, D02, or CM2.  The `154,096` gap rows are explicit
unresolved obligations, not positive edge, component, maximality, or global
credit.  Official keys are used only as post-lineage metadata consistency and
never as a join or routing filter.

## Transaction and replay evidence boundary

The transaction uses `renameat2(RENAME_NOREPLACE)`, exact prefix recovery,
stage and output-directory fsync after every rename, and precise rollback only
for a marker inode owned by this transaction.  A power loss may leave a
recoverable formal prefix without a marker.  Same-UID hostile namespace races
are explicitly not cryptographically eliminated, and automatic orphan-stage
reaping after crash/SIGKILL is not claimed.  The observed completed promotion
had no orphan stage.  These residuals are operational boundaries, not theorem
credit.

Exit status, seed, elapsed time, and maximum RSS above are contemporaneous run
records; they cannot be derived from a content manifest.  Filesystem mtime and
ctime were diagnostic only and are not authentication or attack-first
evidence.  The authoritative replay evidence is the frozen implementation and
source pins, canonical ledger/object commitments, and the complete
verification-bound formal bundle.

No further 22-source heavy reconstruction was run while preparing this record.
The documentation pass used the existing frozen outputs plus lightweight
checks, file hashes, candidate/formal byte comparison, permissions/link counts,
gzip integrity, and transaction-state checks.  A future cold replay must run
the commands above rather than infer heavy execution from this narrative.

## Exact manifest checklist

The companion manifest must contain exactly these 13 members and exclude
itself:

```text
cm2_round306b1g0_source_g_graph_source_inventory_and_join_freeze.py
cm2_round306b1g0_source_g_graph_source_inventory_and_join_freeze_graph_source_inventory.json.gz
cm2_round306b1g0_source_g_graph_source_inventory_and_join_freeze_graph_sheet_join.json.gz
cm2_round306b1g0_source_g_graph_source_inventory_and_join_freeze_graph_side_join.json.gz
cm2_round306b1g0_source_g_graph_source_inventory_and_join_freeze_r264_correction_disposition.json.gz
cm2_round306b1g0_source_g_graph_source_inventory_and_join_freeze_b0_member_backbinding.json.gz
cm2_round306b1g0_source_g_graph_source_inventory_and_join_freeze_gap.json.gz
cm2_round306b1g0_source_g_graph_source_inventory_and_join_freeze_result.json
cm2_round306b1g0_source_g_graph_source_inventory_and_join_freeze_promotion_verifier.py
cm2_round306b1g0_source_g_graph_source_inventory_and_join_freeze_attack_suite.json
cm2_round306b1g0_source_g_graph_source_inventory_and_join_freeze_verification.json
cm2_round306b1g0_source_g_graph_source_inventory_and_join_freeze_report.md
cm2_round306b1g0_source_g_graph_source_inventory_and_join_freeze_cold_replay.md
```

The report and cold-replay record do not embed their own file hashes.  The
external 13-member manifest closes them without a self-reference cycle.
Including the manifest itself, the sealed Round306B1G0 package has 14 files.
