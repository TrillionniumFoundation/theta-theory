# Round303-B exact sealed cold-replay record

Run from the workspace root with `.venv-cm2/bin/python`.

## Frozen exact hashes

```text
producer_sha256=02ce70a560b7fa029e2c7a70a1e4627cb423ac67ba187dba059b57194a646735
b1_ledger_file_sha256=776f1164f96731a2e71b6553ac08165aaa3fe05bb051c0f6602cd8edfd73fa43
b2a_ledger_file_sha256=6095269bd2b791c78b0c305599e7dc3b518dc762e47c00aedeaebe080548e515
b2b_ledger_file_sha256=ca88dcf992c9c2a2483485109f80634376e6cc02239ffd3146f6e1dd318bca96
component_edge_ledger_file_sha256=650df67dfcc3033c42b36638a0da4b3d63ce575469cab84a5e8971ed7b23243a
wtail_unresolved_ledger_file_sha256=eaa18cdec4217e57238d8e5b4209c33295dc325dbb352f1d52347e0d18acdf8e
result_file_sha256=4bd7127f9d935cf7b334fd7660fa6332f8aa23a9c819ac7e018c8add8473eaa1
result_object_sha256=2ca258de5a58175164267bd3ca81b0da8b25a4ebffcd998805e8f7254d172fc2
verifier_sha256=420883fbc6b2ad5a8413e51635b814bac7c1f059e1ff937765e38c8ac98ff88f
attack_suite_file_sha256=c7d87135c2fd77d89855c276be98908649979793d757accadd9bf3dd974b9ab7
attack_suite_object_sha256=feaa6ce50e733dd394a5994d56857cde8a7bd73cb4a7ad814585124d8842029e
verification_file_sha256=6dde1fc938c5059290b811d297306ae16347fd93624a29d7b0ba59974cc06d5a
verification_object_sha256=a803d41e9be3513fb2b2e1ac87e22b35c83c2e678647105708a0857339cbfe57
```

## Producer formal replay

```bash
env PYTHONDONTWRITEBYTECODE=1 \
  PYTHONHASHSEED=303201 \
  .venv-cm2/bin/python -B -I \
  deliverables/cm2_round303b_source_g_unified_attachment_edge_producer.py \
  --seed 303201
```

Observed:

```text
exit=0
elapsed_seconds=1370.97
maximum_resident_set_kib=3345788
```

## Producer isolated cold replay — no write

```bash
env PYTHONDONTWRITEBYTECODE=1 \
  PYTHONHASHSEED=303997 \
  .venv-cm2/bin/python -B -I \
  deliverables/cm2_round303b_source_g_unified_attachment_edge_producer.py \
  --no-write --seed 303997
```

Observed:

```text
exit=0
elapsed_seconds=1409.19
maximum_resident_set_kib=3347784
producer_before=02ce70a560b7fa029e2c7a70a1e4627cb423ac67ba187dba059b57194a646735
producer_after=02ce70a560b7fa029e2c7a70a1e4627cb423ac67ba187dba059b57194a646735
```

The two producer replays returned the exact five ledger hashes, result-file
hash, and result-object closure listed above.

## Independent verifier formal replay

```bash
env PYTHONDONTWRITEBYTECODE=1 \
  PYTHONHASHSEED=303271 \
  .venv-cm2/bin/python -B -I \
  deliverables/cm2_round303b_source_g_unified_attachment_edge_promotion_verifier.py \
  --candidate-dir \
  /home/qian-qi/.openclaw/workspaces/telegram-bot-8449317572/deliverables
```

Observed:

```text
exit=0
elapsed_seconds=2007.38
maximum_resident_set_kib=3172476
status=PASS_EXACT_CACHELESS_EXPECTED_STATE
attack_count=55
rejected_count=55
attack_suite_file_sha256=c7d87135c2fd77d89855c276be98908649979793d757accadd9bf3dd974b9ab7
verification_file_sha256=6dde1fc938c5059290b811d297306ae16347fd93624a29d7b0ba59974cc06d5a
```

## Independent verifier isolated cold replay — no write

```bash
env PYTHONDONTWRITEBYTECODE=1 \
  PYTHONHASHSEED=303929 \
  .venv-cm2/bin/python -B -I \
  deliverables/cm2_round303b_source_g_unified_attachment_edge_promotion_verifier.py \
  --candidate-dir \
  /home/qian-qi/.openclaw/workspaces/telegram-bot-8449317572/deliverables \
  --no-write
```

Observed:

```text
exit=0
elapsed_seconds=2040.89
maximum_resident_set_kib=3172484
status=PASS_EXACT_CACHELESS_EXPECTED_STATE
attack_count=55
rejected_count=55
verification_file_sha256=6dde1fc938c5059290b811d297306ae16347fd93624a29d7b0ba59974cc06d5a
producer_before=02ce70a560b7fa029e2c7a70a1e4627cb423ac67ba187dba059b57194a646735
producer_after=02ce70a560b7fa029e2c7a70a1e4627cb423ac67ba187dba059b57194a646735
verifier_before=420883fbc6b2ad5a8413e51635b814bac7c1f059e1ff937765e38c8ac98ff88f
verifier_after=420883fbc6b2ad5a8413e51635b814bac7c1f059e1ff937765e38c8ac98ff88f
```

The verifier independently reconstructed the complete expected package before
opening candidates, treated the producer as inert bytes, and accepted no
candidate as an oracle.  Formal and no-write verifier runs produced the same
closed verification object and exact verification-file hash.

## Package check

```bash
cd deliverables
sha256sum -c \
  cm2_round303b_source_g_unified_attachment_edge_promotion_manifest.sha256
```

The manifest has exactly 12 members: producer, five ledgers, result, verifier,
attack suite, verification, report, and this cold-replay record.  The manifest
is not an input to itself.

This package grants `44,104` component-edge credits and zero DSU or downstream
credit.  Four W-tail pairs remain unresolved and are neither nonedges nor
exclusions.
