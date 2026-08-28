# Round304 exact cold-replay record

Run from the workspace root with `.venv-cm2/bin/python`.

## Frozen exact hashes

```text
producer_sha256=fff60d4a108355299ee6b9e3106549eca130ada2f4451d8f4deb50f0056520f5
verifier_sha256=f605191b318b7d82106d8f7a872ea8101a59ffdf39999ad48fce9d44888d13fb
schema_snapshot_sha256=90a2697d70abe3f927b5b1f08449d6dc394c4c39f3b7c10766b2c37af0e4b51e

edge_ledger_file_sha256=5018e0d9356596f7c679d2fa2ea4d84df9672a3e3d1a977faeae20edf61722fb
member_ledger_file_sha256=9a7e8c8a0ef810cfd6f29d99c0d2d6701b537ac76d1ab224dcbb60bec966dbd0
residual_ledger_file_sha256=665b61ce0f54d28106159b485cd39171590cd657a3a6d9b823762d1b42123d5f
wtail_ledger_file_sha256=d7552fe4fd03de2bd45e1586500ac438d95c00288d085ad4e270890f0e93a934
result_file_sha256=2975a8cc61c1b7812fedff6bc9dffd4db8517e822311c54a09317403b3592f7d
result_object_sha256=d9f0c8b573d8d3462091bb075711a4983219b8eb23a3ac5db91bc83e0ded5a0c

attack_suite_file_sha256=b14726d34e790a1a944778978260ca23173c3d4ab60c5580175262103bf283c8
attack_suite_object_sha256=6ba930103fe3a5202dd70712641daa31af2dcb69c32934bc4d8d5c7eb95e61c0
attack_rows_sha256=8caaff102225ceb3a42d7d510480614cb7e4dd55afa0e1877cfefa17f2811e41
verification_file_sha256=482c1124cfd9d6daaa8c5d3af4f1a5023efb368946ff01718f73360bd3e558d3
verification_object_sha256=9b5ce8aebb8a96c1b146f0adf17496b85cb5c3ed6d3d8d08bdcebd887080984a
```

## Candidate byte equality and canonical admission

The formal deliverables, repaired seed-A private staging, and repaired seed-B
private staging compare byte-for-byte equal for all five candidate files:
edge ledger, member ledger, residual ledger, W-tail ledger, and result.  Each
formal candidate is a regular file with link count one.

The initial `r304-invalid-noncanonical-*` seed-A and seed-B staging batches
were isolated and never promoted or consumed for formal credit.  Integer-keyed
histograms had been serialized before JSON keys underwent their required
string-key lexical ordering.  The repaired producer converts histogram keys
to strings before canonical sorting, recursively requires string object keys,
replays canonical bytes after parsing, and rechecks the parsed result closure
after removing `result_sha256`.

For the admitted result, raw bytes equal the canonical encoding of the parsed
object, and the parsed self-hash closes to
`d9f0c8b573d8d3462091bb075711a4983219b8eb23a3ac5db91bc83e0ded5a0c`.

## Producer formal replay

```bash
env PYTHONDONTWRITEBYTECODE=1 \
  PYTHONHASHSEED=304001 \
  .venv-cm2/bin/python -B -I \
  deliverables/cm2_round304_source_g_fresh_extended_registry_legal_component_dsu_rebuild.py \
  --candidate-dir \
  /home/qian-qi/.openclaw/workspaces/telegram-bot-8449317572/.tmp/openclaw-spikes/r304-formal-replay-fixed.K6L3lP \
  --seed 304001
```

Observed:

```text
exit=0
elapsed=23:45.36
maximum_resident_set_kib=2740664
producer_before=fff60d4a108355299ee6b9e3106549eca130ada2f4451d8f4deb50f0056520f5
producer_after=fff60d4a108355299ee6b9e3106549eca130ada2f4451d8f4deb50f0056520f5
verifier_before=f605191b318b7d82106d8f7a872ea8101a59ffdf39999ad48fce9d44888d13fb
verifier_after=f605191b318b7d82106d8f7a872ea8101a59ffdf39999ad48fce9d44888d13fb
```

The five generated files exactly match both the formal deliverables and the
repaired seed-B staging files.

## Producer isolated cold replay — no write

```bash
env PYTHONDONTWRITEBYTECODE=1 \
  PYTHONHASHSEED=304557 \
  .venv-cm2/bin/python -B -I \
  deliverables/cm2_round304_source_g_fresh_extended_registry_legal_component_dsu_rebuild.py \
  --no-write \
  --seed 304557
```

Observed:

```text
exit=0
elapsed=24:01.26
maximum_resident_set_kib=2731860
producer_before=fff60d4a108355299ee6b9e3106549eca130ada2f4451d8f4deb50f0056520f5
producer_after=fff60d4a108355299ee6b9e3106549eca130ada2f4451d8f4deb50f0056520f5
verifier_before=f605191b318b7d82106d8f7a872ea8101a59ffdf39999ad48fce9d44888d13fb
verifier_after=f605191b318b7d82106d8f7a872ea8101a59ffdf39999ad48fce9d44888d13fb
```

The no-write replay returned the exact four ledger commitments and result
closure frozen above and wrote no candidate or promotion output.

## Independent verifier formal replay

```bash
env PYTHONDONTWRITEBYTECODE=1 \
  PYTHONHASHSEED=304271 \
  .venv-cm2/bin/python -B -I \
  deliverables/cm2_round304_source_g_fresh_extended_registry_legal_component_dsu_rebuild_promotion_verifier.py \
  --root /home/qian-qi/.openclaw/workspaces/telegram-bot-8449317572 \
  --candidate-dir /home/qian-qi/.openclaw/workspaces/telegram-bot-8449317572/deliverables \
  --producer-path /home/qian-qi/.openclaw/workspaces/telegram-bot-8449317572/deliverables/cm2_round304_source_g_fresh_extended_registry_legal_component_dsu_rebuild.py
```

Observed:

```text
exit=0
elapsed=25:57.69
maximum_resident_set_kib=2677792
status=PASS_EXACT_CACHELESS_EXPECTED_STATE
attack_fixture_count=58
rejected_count=58
attack_suite_file_sha256=b14726d34e790a1a944778978260ca23173c3d4ab60c5580175262103bf283c8
attack_suite_object_sha256=6ba930103fe3a5202dd70712641daa31af2dcb69c32934bc4d8d5c7eb95e61c0
attack_rows_sha256=8caaff102225ceb3a42d7d510480614cb7e4dd55afa0e1877cfefa17f2811e41
verification_file_sha256=482c1124cfd9d6daaa8c5d3af4f1a5023efb368946ff01718f73360bd3e558d3
verification_object_sha256=9b5ce8aebb8a96c1b146f0adf17496b85cb5c3ed6d3d8d08bdcebd887080984a
producer_before=fff60d4a108355299ee6b9e3106549eca130ada2f4451d8f4deb50f0056520f5
producer_after=fff60d4a108355299ee6b9e3106549eca130ada2f4451d8f4deb50f0056520f5
verifier_before=f605191b318b7d82106d8f7a872ea8101a59ffdf39999ad48fce9d44888d13fb
verifier_after=f605191b318b7d82106d8f7a872ea8101a59ffdf39999ad48fce9d44888d13fb
```

The verifier independently constructs the complete expected bytes before
opening candidate files and treats the producer as inert bytes only.  It
records exact five-file candidate equality, forward/reverse partition equality,
`actual_official_key_count=124`, rejection of stale count `116`, and
`all_source_and_candidate_PRE_POST_fd_identities_equal=true`.

The formal promotion wrote the required attack artifact first at
`2026-07-31 20:31:51.860677263 +0800` and the verification last marker at
`2026-07-31 20:31:51.865771185 +0800`, a separation of exactly `5,093,922 ns`.

## Independent verifier isolated cold replay — no write

```bash
env PYTHONDONTWRITEBYTECODE=1 \
  PYTHONHASHSEED=304983 \
  .venv-cm2/bin/python -B -I \
  deliverables/cm2_round304_source_g_fresh_extended_registry_legal_component_dsu_rebuild_promotion_verifier.py \
  --root /home/qian-qi/.openclaw/workspaces/telegram-bot-8449317572 \
  --candidate-dir /home/qian-qi/.openclaw/workspaces/telegram-bot-8449317572/deliverables \
  --producer-path /home/qian-qi/.openclaw/workspaces/telegram-bot-8449317572/deliverables/cm2_round304_source_g_fresh_extended_registry_legal_component_dsu_rebuild.py \
  --no-write
```

Observed:

```text
exit=0
elapsed=25:49.95
maximum_resident_set_kib=2687552
status=PASS_EXACT_CACHELESS_EXPECTED_STATE
candidate_and_promotion_outputs_written=false
attack_suite_file_sha256=b14726d34e790a1a944778978260ca23173c3d4ab60c5580175262103bf283c8
attack_suite_object_sha256=6ba930103fe3a5202dd70712641daa31af2dcb69c32934bc4d8d5c7eb95e61c0
attack_rows_sha256=8caaff102225ceb3a42d7d510480614cb7e4dd55afa0e1877cfefa17f2811e41
verification_file_sha256=482c1124cfd9d6daaa8c5d3af4f1a5023efb368946ff01718f73360bd3e558d3
verification_object_sha256=9b5ce8aebb8a96c1b146f0adf17496b85cb5c3ed6d3d8d08bdcebd887080984a
producer_before=fff60d4a108355299ee6b9e3106549eca130ada2f4451d8f4deb50f0056520f5
producer_after=fff60d4a108355299ee6b9e3106549eca130ada2f4451d8f4deb50f0056520f5
verifier_before=f605191b318b7d82106d8f7a872ea8101a59ffdf39999ad48fce9d44888d13fb
verifier_after=f605191b318b7d82106d8f7a872ea8101a59ffdf39999ad48fce9d44888d13fb
```

Formal and cold verifier runs produce the same closed attack and verification
hashes.  The suite rejects `58 / 58` concrete fixtures across `55` mechanisms;
the fixture census is `40` cascade, `11` OS/AST, and `7` wire-format attacks.

## Replay result and record boundary

The replay proves exactly `478,710` legal edge applications, `275,268` rank
reductions, one fresh component quotient, and `92,696` final components.  It
grants zero maximality, fibre, global-disposition, Jx/Jy same-point, W-tail
new-edge, or Source-W credit.  All `224,580` Source-G global dispositions remain
unresolved; `1,024` Round300A maximality pairs remain cross-component and
unwitnessed; D02 is `BLOCKED`; complete Gate5 18-field blocks remain `0`; CM2
is `NO-GO_FOR_CLAIM`.

No Round304 manifest is created by this record-writing step.  This record and
the companion report do not embed their own file hashes and are not replay
inputs, which keeps their later external file commitments free of a
self-reference cycle.
