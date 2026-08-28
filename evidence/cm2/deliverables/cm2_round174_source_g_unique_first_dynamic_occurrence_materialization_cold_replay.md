# Round174 independent-verifier cold replay

Working directory:

`/home/qian-qi/.openclaw/workspaces/telegram-bot-8449317572`

Commands:

```text
PYTHONDONTWRITEBYTECODE=1 PYTHONHASHSEED=17 .venv-neurips/bin/python -B deliverables/cm2_round174_source_g_unique_first_dynamic_occurrence_materialization_verifier.py

PYTHONDONTWRITEBYTECODE=1 PYTHONHASHSEED=211 .venv-neurips/bin/python -B deliverables/cm2_round174_source_g_unique_first_dynamic_occurrence_materialization_verifier.py --output /tmp/codex-round174-seed211-6476198178.json
```

Both runs printed:

```text
PASS
full rows 72500 62012 62696
attacks 34 10 11
6c82800d41e456aeed7000bccb13bfe0e5e6d5f1637ac52a4d5c45b24ed9a23b
```

The two verification documents were compared with `cmp -s` and were
byte-identical.  Both file hashes were:

`1f65b5e02b1d1e63bd7e41d6a88d5eb180e2be92620af4b8afa2141c9f6e344c`

The verifier independently reconstructed and compared all 113,656,620
bytes of the row attachment.  Its signed result records
`producer_imported_or_executed=false`.
