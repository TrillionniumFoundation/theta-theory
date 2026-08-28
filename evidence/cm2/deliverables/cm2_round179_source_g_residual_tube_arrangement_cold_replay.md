# Round179 independent-verifier cold replay

Working directory:

`/home/qian-qi/.openclaw/workspaces/telegram-bot-8449317572`

Commands:

```text
PYTHONDONTWRITEBYTECODE=1 PYTHONHASHSEED=17 .venv-neurips/bin/python -B deliverables/cm2_round179_source_g_residual_tube_arrangement_verifier.py

PYTHONDONTWRITEBYTECODE=1 PYTHONHASHSEED=211 .venv-neurips/bin/python -B deliverables/cm2_round179_source_g_residual_tube_arrangement_verifier.py --output /tmp/codex-round179-seed211-6476198178.json
```

Both final-source runs printed:

```text
PASS
origins/children 62012 17192 106680
attacks 33 10 11
ca2ec32d84edf55919a26f556fd8e9dfc39566ad876b0cb5537168fee2b28229
```

The two verification documents were byte-identical.  Their common SHA256
was:

`37eaa14cd870df64a12c2434deafe5fdead5cec303f5530208f07c11836736bc`

Each run independently reconstructed and compared all 131,273,924
attachment bytes and the complete expected certificate.  The signed result
records `producer_imported_or_executed=false`.
