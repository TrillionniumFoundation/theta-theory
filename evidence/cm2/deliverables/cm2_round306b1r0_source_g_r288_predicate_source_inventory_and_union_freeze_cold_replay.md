# Round306B1R0 exact cold-replay record

Runs used CPython `3.12.3`, zlib `1.3`, on
`Linux 7.0.0-28-generic x86_64`, from:

```text
/home/qian-qi/.openclaw/workspaces/telegram-bot-8449317572
```

## Frozen implementation pins and exact formal outputs

```text
producer_sha256=3538e17fd523384d31a2fbf46505ff4ee5bf7ba8f41db14534e55edaa04eabca
verifier_sha256=60ff7e2e65adfd76f097c46068fdd49a1d5874916f030be238658835396f5ecb

cell_file_sha256=19d13d93fc02296f673ca18cc2edbd96174985f7be8fb0e03694582b188b0f96
cell_ledger_sha256=f473914afa7d9dab1598a3259be8a4ec2b08ab7992d7a7039cff8bde5f19512b
member_file_sha256=4b3633782e4514f598cb9cce19930ba31616f7d42aab002df4f77f9b4601ddf7
member_ledger_sha256=28c6e7944f440f9fee06f9ade150de2566a3aaa85b40c49d63e3721ec4a4c4c5
gap_file_sha256=c6b1de08fc62e39d5c5cfc2d98ba5b558d467e1592cc101c19ebdbc9fab66c56
gap_ledger_sha256=6a61506040c6f48236d8f35ee393f3a1d08dc36dbbcfd5a6d58b9290ef1e8904

result_file_sha256=ca66501d42894dce364ff905045ae69f67cf52c9142ba8f7b45973f857966f04
result_object_sha256=ad2454ded68ffdcd4b37d39a43b60220ca4fbad780197e0443bcf4ce1904a46c
attack_file_sha256=a34f51d8371dbc48b444fc6eb9a1e677b496a5ed447505b04e07e61b6d64fa19
attack_object_sha256=aa0c78e10aad22cf7b719ed41f4e7439381ab8fc9a2974eb01aefb4c3c51c76e
attack_rows_sha256=136a092241293ed54dc7f67de01fad5a8af5220537f85169812607c3d638e462
verification_file_sha256=2242732077165e085f6f2e50f2d061a532a3b43d9e9bc0efc17afac3d45df040
verification_object_sha256=3cb6c976f411a4ad05369434dab8d60ff98fea7204fddd8dd628d6e67c644ea8
```

The three gzip ledger commitments also bind exact row counts, row IDs, row
hashes, and canonical row streams:

```text
cell_rows=295340
cell_rows_sha256=b89220807eef10bc8412be19c5037ea75fa3c6fdf4321c27938afec0c68c9246
cell_row_ids_sha256=b3fb242c0c130122b0e2e7e0c1e38f866f214e332aea93dc6ce03e705201fe9a
cell_row_hashes_sha256=33ce0c07cf6eeeb7e8d3d10129dad7652aec94e3d30d18d807499380b35f279d

member_rows=295336
member_rows_sha256=6665fc8e72824fba7dbd1d1b7462ae419bb31c25149037da3183d74569b62a3d
member_row_ids_sha256=6c136186cd30608304293cc91185615ba6bec6418cb2c43a48ac833055c69bfe
member_row_hashes_sha256=d106b9e68817aa9504ec176be9c679f2e4fd29948c3614f7c109030a893f289f

gap_rows=590676
gap_rows_sha256=c6bc641ea84b5a25ed851b0d13cef3b8694fcf4224b59868e641a3339496cf3d
gap_row_ids_sha256=98aca1023d164e131c4755b0f35c777f3a984c8ffac6b58aaf1640bddb2dfdba
gap_row_hashes_sha256=713e8415b88299f6db95446574f160b864f99a93ef8b12b14c8176cd12904df7
```

## Lightweight contract checks

```bash
python3 \
  deliverables/cm2_round306b1r0_source_g_r288_predicate_source_inventory_and_union_freeze.py \
  --self-test

python3 \
  deliverables/cm2_round306b1r0_source_g_r288_predicate_source_inventory_and_union_freeze.py \
  --transaction-self-test

python3 \
  deliverables/cm2_round306b1r0_source_g_r288_predicate_source_inventory_and_union_freeze_promotion_verifier.py \
  --self-test
```

All returned exit `0`.  The producer contract passed 13 checks, its inode-bound
transaction test passed all 13 named mechanisms, and the verifier rejected
`46 / 46` defense-in-depth attacks (`20` semantic, `2` filesystem, and `24`
wire).  The verifier self-test includes two positive source-stream buffer-edge
regressions, rejection of a true trailing comma, 19 raw-gzip fixtures
(4 positive and 15 negative), and one giant-unclosed-row token fixture: 20
combined exact-wire fixtures.  These lightweight commands opened no large
source or candidate and wrote no formal artifact.

## Two independent producer candidates

```bash
PYTHONHASHSEED=3061101 /usr/bin/time -v \
  python3 \
  deliverables/cm2_round306b1r0_source_g_r288_predicate_source_inventory_and_union_freeze.py \
  --candidate-dir .cm2-round306b1r0-private-candidates/seed3061101
```

Observed: exit `0`, elapsed `8:53.08`, maximum RSS `8,072,884 KiB`.

```bash
PYTHONHASHSEED=3061999 /usr/bin/time -v \
  python3 \
  deliverables/cm2_round306b1r0_source_g_r288_predicate_source_inventory_and_union_freeze.py \
  --candidate-dir .cm2-round306b1r0-private-candidates/seed3061999
```

Observed: exit `0`, elapsed `8:18.58`, maximum RSS `8,077,368 KiB`.

Both complete four-file candidates are byte-for-byte equal.  Their three gzip
members pass integrity checking, have deterministic headers, and their result
object self-hashes close.  Each candidate is private and carries zero formal
theorem, maximality, fibre, or global-disposition credit.

## Fail-closed admission and verifier hardening history

The first heavy admission used `PYTHONHASHSEED=3062551`, candidate
`seed3061101`, and the then-frozen verifier
`692dd3bfa49abbee333196b5d7a32eb8c55344b96cb87cf88fa69f30c12c72de`.
It failed closed after approximately `2:07` while streaming the pinned
Round294 source, with:

```text
VerificationBlocked: trailing streamed comma
```

The legal comma landed exactly at the end of the 1 MiB input buffer.  The
parser consumed it and tested the empty buffer before refilling.  This was a
stream-boundary implementation defect, not a source or candidate discrepancy.
The failure occurred before the candidate path was opened and before any
formal write; the formal prefix therefore remained empty.

The parser was fixed to refill across an empty or whitespace-only boundary
after a comma while still rejecting a true trailing comma.  The intermediate
fixed verifier was
`dc0c547c36916ceadadf3f05665d119db36d2bd372eaec3578a91d655533e2a4`.
Before the heavy replay was retried, the candidate reader was additionally
hardened to validate raw gzip bytes before JSON parsing: exactly one complete
gzip member, no second empty/whitespace/JSON member, no trailing byte or NUL
padding, valid CRC32 and ISIZE, no truncation, exact independently computed
decompressed wire size, physical EOF and fd-offset closure, and a bounded row
token.  That hardened and independently audited verifier is the final
`60ff7e2e...f5ecb` pin above.  The hardening increased the honest suite to
`46 / 46`; it did not change any reconstruction count or credit boundary.

## Exact candidate admission without promotion

```bash
PYTHONHASHSEED=3062777 /usr/bin/time -v \
  python3 \
  deliverables/cm2_round306b1r0_source_g_r288_predicate_source_inventory_and_union_freeze_promotion_verifier.py \
  --candidate-dir .cm2-round306b1r0-private-candidates/seed3061101
```

Observed with the final verifier:

```text
exit=0
elapsed=8:16.58
maximum_resident_set_kib=8090700
status=PASS_EXACT_B1R0_PRIVATE_CANDIDATE_ADMISSION__ZERO_FORMAL_THEOREM_CREDIT
formal_full_support_credit=0
formal_maximality_credit=0
formal_fibre_credit=0
formal_global_disposition_credit=0
formal_artifact_written=false
predicted_attack_file_sha256=a34f51d8371dbc48b444fc6eb9a1e677b496a5ed447505b04e07e61b6d64fa19
predicted_verification_file_sha256=2242732077165e085f6f2e50f2d061a532a3b43d9e9bc0efc17afac3d45df040
```

The verifier treated the producer as inert SHA-pinned bytes and independently
reconstructed all 27 pinned sources before opening the candidate.  It then
compared every one of the `295,340` cell rows, `295,336` member rows, and
`590,676` gap rows, along with the exact result object and compressed file
hashes.  No promotion was requested in this run.

## Formal promotion

```bash
PYTHONHASHSEED=3062888 /usr/bin/time -v \
  python3 \
  deliverables/cm2_round306b1r0_source_g_r288_predicate_source_inventory_and_union_freeze_promotion_verifier.py \
  --candidate-dir .cm2-round306b1r0-private-candidates/seed3061999 \
  --promote
```

Observed:

```text
exit=0
elapsed=9:12.30
maximum_resident_set_kib=8088608
status=PASS_EXACT_ROUND306B1R0_R288_PREDICATE_SOURCE_INVENTORY_AND_UNION_FREEZE__ZERO_THEOREM_CREDIT
formal_full_support_credit=0
formal_maximality_credit=0
formal_fibre_credit=0
formal_global_disposition_credit=0
formal_candidate_cmp=4/4
formal_gzip_integrity=3/3
result_attack_verification_self_hashes_close=3/3
transaction_file_modes_0600_and_nlink_1=6/6
orphan_stage_count=0
```

The content-bound, no-clobber transaction committed in exact order:

```text
attack -> predicate-source-cell -> member-union -> gap -> result -> verification
```

The attack suite was therefore durable first.  The verification object was
published last and is the sole package marker.  The marker binds the exact
six-file formal transaction but explicitly grants no theorem credit.  Formal
postchecks found the four promoted candidate files byte-identical to their
private source, all three gzip streams intact, all three object self-hashes
closed, all six formal files mode `0600` with link count `1`, and no orphan
promotion stage.

## Exact inventory and credit boundary

The sealed B1R0 result records exactly:

```text
Round288_atom_identity_count=332016
source_side_partition_row_count=332020
existing_Round208_identity_count=36040
Round204_exact_alias_count=640
new_Round288_member_count=295336
predicate_source_cell_count=295340
Round271_W_tail_parent_normalization_count=4
source_multiplicity_1=295332
source_multiplicity_2=4
Round269_source_cell_count=187128
Round270_source_cell_count=37712
Round271_source_cell_count=70356
Round272_source_cell_count=144
cell_gap_count=295340
member_gap_count=295336
total_gap_count=590676
Round294_member_set_equals_Round306B0_member_set=true
outer_envelope_union_exact_for_every_member=true
source_free_interval_predicate_theorem_complete=false
member_full_support_union_theorem_complete=false
formal_full_support_credit=0
formal_maximality_credit=0
formal_fibre_credit=0
formal_global_disposition_credit=0
D02_status=BLOCKED
CM2_status=NO-GO_FOR_CLAIM
```

The four-row difference between source-side rows and atom identities is exactly
the four artificial Round271 W-tail splits; it is not four additional atom
identities.  Official keys remain metadata only.  This package freezes a
source inventory and its unresolved support gaps; it does not prove the
source-free interval predicate, full support union, component maximality,
official-fibre exhaustion, Source-G global dispositions, D02, or CM2.

## Replay evidence boundary

Exit status, seed, elapsed time, and maximum RSS above are contemporaneous run
records.  They are not derivable from the package manifest.  Filesystem mtime
and ctime were observed only as operational diagnostics and are not accepted
as authentication or attack-first evidence; content hashes and the
verification-bound transaction bundle are authoritative.

After the formal package and documentation were audited, no additional
27-source heavy reconstruction was run and the million-plus ledger rows were
not reread row by row.  The post-audit checks were limited to frozen
commitments, small JSON objects, exact filenames, permissions/link counts,
gzip integrity records, transaction state, and manifest membership.  A future
cold rerun must execute the pinned commands above to regenerate the heavy
evidence rather than infer it from this narrative.

## Exact manifest checklist

The companion manifest is expected to contain exactly the following 10
members and to exclude itself:

```text
cm2_round306b1r0_source_g_r288_predicate_source_inventory_and_union_freeze.py
cm2_round306b1r0_source_g_r288_predicate_source_inventory_and_union_freeze_predicate_source_cell.json.gz
cm2_round306b1r0_source_g_r288_predicate_source_inventory_and_union_freeze_member_union.json.gz
cm2_round306b1r0_source_g_r288_predicate_source_inventory_and_union_freeze_gap.json.gz
cm2_round306b1r0_source_g_r288_predicate_source_inventory_and_union_freeze_result.json
cm2_round306b1r0_source_g_r288_predicate_source_inventory_and_union_freeze_promotion_verifier.py
cm2_round306b1r0_source_g_r288_predicate_source_inventory_and_union_freeze_attack_suite.json
cm2_round306b1r0_source_g_r288_predicate_source_inventory_and_union_freeze_verification.json
cm2_round306b1r0_source_g_r288_predicate_source_inventory_and_union_freeze_report.md
cm2_round306b1r0_source_g_r288_predicate_source_inventory_and_union_freeze_cold_replay.md
```

The report and cold-replay record do not embed their own file hashes.  The
external 10-member manifest closes them without a self-reference cycle.
Including the manifest itself, the sealed Round306B1R0 package has 11 files.
